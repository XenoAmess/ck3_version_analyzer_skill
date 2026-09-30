"""Behavioral regression tests. Fixtures and generated reports stay outside the repository."""

import contextlib
from copy import deepcopy
from dataclasses import asdict
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import ck3_analyzer as analyzer

validator_path = ROOT / ".sisyphus/skills/ck3_version_analyzer/scripts/validate_report.py"
spec = importlib.util.spec_from_file_location("ck3_report_validator", validator_path)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class AnalyzerTests(unittest.TestCase):
    def setUp(self):
        self.fixture = Path(tempfile.mkdtemp(prefix="ck3-analyzer-tests-")).resolve()
        self.assertEqual(self.fixture.parent, Path(tempfile.gettempdir()).resolve())
        self.addCleanup(self.remove_fixture)
        self.old, self.new = self.fixture / "old", self.fixture / "new"
        self.old.mkdir()
        self.new.mkdir()

    def remove_fixture(self):
        # Check the absolute cleanup target before recursively deleting it.
        target = self.fixture.resolve()
        if target.parent != Path(tempfile.gettempdir()).resolve() or not target.name.startswith("ck3-analyzer-tests-"):
            raise RuntimeError(f"Unexpected cleanup target: {target}")
        shutil.rmtree(target)

    def write(self, root, relative, content):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode("utf-8") if isinstance(content, str) else content)
        return path

    def compare(self, deep=True, limit=0):
        report = analyzer.compare_versions(self.old, self.new, "old", "new")
        analyzer.perform_deep_analysis(report, self.old, self.new, limit, enabled=deep)
        analyzer.detect_changed_systems(report)
        return report

    def final_data(self, report):
        data = asdict(report)
        data["metadata"].update(
            analysis_model="TestModel 1.0（测试夹具）", final_generated_at="2026-09-30T12:00:00+08:00",
            llm_review={"performed": True, "reviewed_paths": [item["path"] for item in data["deep_diffs"]]},
        )
        return data

    def final_text(self, data):
        # This fixture represents a final report, independently of the preliminary writer.
        lines = ["# Crusader Kings III old → new 极详细对比分析报告", "", "## 版本基本信息", ""]
        for key, label in (("game_branch", "游戏分支"), ("game_commit", "游戏提交"),
                           ("engine_branch", "引擎分支"), ("engine_commit", "引擎提交")):
            lines.extend([f"- **{label}**:", f"  - 旧版本: {data['version_info']['old'][key]}",
                          f"  - 新版本: {data['version_info']['new'][key]}"])
        lines.extend(["", "## 整体差异统计总览", ""])
        for key, label in (("added", "新增文件"), ("removed", "删除文件"),
                           ("modified", "修改文件"), ("unchanged", "未变化文件"),
                           ("total_old", "旧版文件总数"), ("total_new", "新版文件总数")):
            lines.append(f"- **{label}**: {data['summary'][key]}")
        lines.append(f"- **文件总数变化**: {data['summary']['total_new'] - data['summary']['total_old']:+d}")
        lines.extend(["", "## 分析覆盖", ""])
        for key, label in (("candidate_files", "候选文本文件数"), ("analyzed_files", "已分析文本文件数"),
                           ("skipped_files", "跳过文本文件数"), ("binary_files", "变化二进制文件数")):
            lines.append(f"- **{label}**: {data['coverage'][key]}")
        reviewed = len(data["metadata"]["llm_review"]["reviewed_paths"])
        lines.append(f"- **未复核文本文件数**: {data['coverage']['candidate_files'] - reviewed}")
        lines.extend(["", "## 关键变更", "", "测试报告；不对真实游戏机制作结论。", "",
                      "## 附录 B: 生成信息", "",
                      f"- **报告生成时间**: {data['metadata']['final_generated_at']}",
                      f"- **分析模型**: {data['metadata']['analysis_model']}",
                      "- **协作人**: XenoAmess",
                      f"- **深度分析文件数**: {len(data['deep_diffs'])}",
                      f"- **LLM复核文件数**: {reviewed}", ""])
        return "\n".join(lines)

    def test_same_size_binary_content_change(self):
        self.write(self.old, "binaries/test.exe", b"ABCD")
        self.write(self.new, "binaries/test.exe", b"WXYZ")
        report = self.compare()
        self.assertEqual(report.summary["modified"], 1)
        self.assertEqual(report.coverage["binary_files"], 1)
        self.assertEqual(report.coverage["candidate_files"], 0)
        item = report.file_diffs[0]
        self.assertNotEqual(item["old_info"]["sha256"], item["new_info"]["sha256"])
        self.assertIsNone(item["line_changes"])

    def test_equal_line_count_replacement_is_counted(self):
        relative = "game/common/defines/00_defines.txt"
        self.write(self.old, relative, "balance = 10\n")
        self.write(self.new, relative, "balance = 20\n")
        report = self.compare()
        self.assertEqual(report.file_diffs[0]["net_line_change"], 0)
        self.assertEqual(report.file_diffs[0]["line_changes"], 2)
        self.assertEqual(report.systems["defines"]["line_changes"], 2)
        self.assertTrue(report.systems["defines"]["priority_candidate"])

    def test_added_and_removed_have_evidence(self):
        self.write(self.old, "game/events/removed.txt", "namespace = old\n")
        self.write(self.new, "game/events/added.txt", "namespace = new\n")
        report = self.compare()
        self.assertEqual({item.status for item in report.deep_diffs}, {"added", "removed"})
        self.assertEqual(report.coverage["analyzed_files"], 2)
        added = next(item for item in report.deep_diffs if item.status == "added")
        removed = next(item for item in report.deep_diffs if item.status == "removed")
        self.assertEqual((added.lines_added, added.lines_removed), (1, 0))
        self.assertEqual((removed.lines_added, removed.lines_removed), (0, 1))
        self.assertIn("旧版本不存在", added.summary)
        self.assertIn("新版本不存在", removed.summary)

    def test_empty_file_addition_is_not_called_encoding_change(self):
        self.write(self.new, "game/events/empty.txt", "")
        report = self.compare()
        self.assertEqual(report.deep_diffs[0].change_type, "empty_file")
        self.assertEqual(report.coverage["analyzed_files"], 1)

    def test_cultural_effects_is_not_localization(self):
        path = "game/common/scripted_effects/cultural_effects.txt"
        hunks = analyzer.compute_line_diff(["fertility = 0.2\n"], ["fertility = 0.3\n"])
        kind, system, impact = analyzer.classify_change_type(path, hunks)
        self.assertEqual(system, "scripted_effects")
        self.assertEqual(kind, "mechanics_candidate")
        self.assertNotIn("仅文本翻译", impact)

    def test_exists_does_not_prove_bugfix(self):
        hunks = analyzer.compute_line_diff(["always = yes\n"], ["exists = scope:actor\n"])
        kind, _, impact = analyzer.classify_change_type("game/common/scripted_triggers/test.txt", hunks)
        self.assertEqual(kind, "text_change")
        self.assertIn("尚未验证", impact)

    def test_priority_applied_before_file_limit(self):
        for relative in ("game/localization/a_l_english.yml", "game/common/laws/z.txt"):
            self.write(self.old, relative, "value = 1\n")
            self.write(self.new, relative, "value = 2\n")
        report = self.compare(limit=1)
        self.assertEqual(report.deep_diffs[0].path, "game/common/laws/z.txt")
        self.assertEqual(report.coverage["skipped"], [
            {"path": "game/localization/a_l_english.yml", "reason": "file_limit"}
        ])
        self.assertFalse(report.coverage["all_text_files_analyzed"])

    def test_stats_mode_does_not_claim_zero_churn(self):
        self.write(self.old, "game/common/defines/test.txt", "value = 1\n")
        self.write(self.new, "game/common/defines/test.txt", "value = 2\n")
        report = self.compare(deep=False)
        self.assertIsNone(report.file_diffs[0]["line_changes"])
        self.assertEqual(report.coverage["skipped"][0]["reason"], "disabled")
        self.assertEqual(report.systems["defines"]["unknown_line_files"], 1)

    def test_invalid_utf8_is_reported_and_skipped(self):
        self.write(self.old, "game/events/test.txt", b"value = 1\n")
        self.write(self.new, "game/events/test.txt", b"value = \xff\n")
        report = self.compare()
        self.assertEqual(report.summary["modified"], 1)
        self.assertEqual(report.coverage["skipped"][0]["reason"], "decode_error")
        self.assertIsNone(report.file_diffs[0]["new_info"]["line_count"])
        self.assertTrue(any(issue["phase"] == "decode" for issue in report.issues))

    def test_utf16_bom_is_text(self):
        self.write(self.old, "game/events/test.txt", "value = 1\n".encode("utf-16"))
        self.write(self.new, "game/events/test.txt", "value = 2\n".encode("utf-16"))
        report = self.compare()
        self.assertEqual(report.coverage["analyzed_files"], 1)
        self.assertEqual(report.file_diffs[0]["old_info"]["encoding"], "utf-16")

    def test_bom_and_newline_changes_are_byte_only(self):
        self.write(self.old, "game/events/test.txt", b"value = 1\r\n")
        self.write(self.new, "game/events/test.txt", b"\xef\xbb\xbfvalue = 1\n")
        report = self.compare()
        self.assertEqual(report.summary["modified"], 1)
        self.assertEqual(report.deep_diffs[0].change_type, "byte_only")
        self.assertEqual(report.file_diffs[0]["line_changes"], 0)

    def test_unreadable_file_aborts_scan(self):
        self.write(self.old, "test.txt", "value = 1\n")
        with patch.object(Path, "open", side_effect=PermissionError("fixture denied")):
            with self.assertRaisesRegex(analyzer.AnalysisError, "停止以避免错误统计"):
                analyzer.scan_directory(self.old)

    def test_changed_snapshot_aborts_deep_analysis(self):
        self.write(self.old, "test.txt", "value = 1\n")
        self.write(self.new, "test.txt", "value = 2\n")
        report = analyzer.compare_versions(self.old, self.new, "old", "new")
        self.write(self.new, "test.txt", "value = 3\n")
        with self.assertRaisesRegex(analyzer.AnalysisError, "扫描后文件发生变化"):
            analyzer.perform_deep_analysis(report, self.old, self.new)

    def test_ignored_directory_is_pruned(self):
        for root in (self.old, self.new):
            self.write(root, ".idea/subdir/ignored.txt", "ignore")
            self.write(root, ".git/private", "ignore")
            self.write(root, "game/events/included.txt", "include")
        report = self.compare()
        self.assertEqual(report.summary["total_old"], 1)
        self.assertEqual(report.summary["unchanged"], 1)

    def test_diff_retains_order_context_and_plus_prefixes(self):
        hunks = analyzer.compute_line_diff(
            ["context\n", "++old\n", "tail\n"], ["context\n", "++new\n", "tail\n"]
        )
        self.assertEqual(hunks[0].lines, [" context", "-++old", "+++new", " tail"])
        self.assertEqual(hunks[0].lines_added, ["++new"])
        self.assertEqual(hunks[0].lines_removed, ["++old"])
        self.assertEqual(hunks[0].old_start, 1)

    def test_snippet_budget_shows_both_versions(self):
        hunks = analyzer.compute_line_diff(
            [f"old{i}\n" for i in range(40)], [f"new{i}\n" for i in range(40)]
        )
        summary = analyzer.generate_diff_summary(hunks, 20)
        self.assertIn("-old0", summary)
        self.assertIn("+new0", summary)
        self.assertIn("省略 60 行", summary)
        shown = [line for line in summary.splitlines() if line.startswith(("+", "-"))]
        self.assertEqual(len(shown), 20)

    def test_diff_code_fences_remain_balanced(self):
        hunks = analyzer.compute_line_diff(
            [analyzer.FENCE + "\n", "old\n"], [analyzer.FENCE + "\n", "new\n"]
        )
        summary = analyzer.generate_diff_summary(hunks)
        self.assertEqual(analyzer.format_errors(summary), [])

    def test_unknown_system_stays_visible_and_primary_counts_are_unique(self):
        self.write(self.new, "unknown/test.txt", "new\n")
        self.write(self.new, "game/history/titles/test.txt", "holder = actor\n")
        report = self.compare()
        self.assertIn("unclassified", report.systems)
        self.assertIn("title", report.systems)
        self.assertEqual(sum(item["primary_file_count"] for item in report.systems.values()), 2)
        self.assertGreater(sum(item["file_count"] for item in report.systems.values()), 2)

    def test_missing_metadata_is_explicit(self):
        report = self.compare()
        self.assertTrue(report.version_info["old"]["game_commit"].startswith("未知"))
        self.assertTrue(any(issue["phase"] == "metadata" for issue in report.issues))
        self.assertEqual(report.metadata["input_directories"]["old"], str(self.old))

    def test_exact_version_alias_and_ambiguity(self):
        (self.fixture / "CK3_1.19.0.6").mkdir()
        with self.assertRaises(analyzer.AnalysisError):
            analyzer.find_version_folders(self.fixture, "1.19.0", "1.19.0.6")
        (self.fixture / "CK3_1.19.0").mkdir()
        old, _ = analyzer.find_version_folders(self.fixture, "1.19.0", "1.19.0.6")
        self.assertEqual(Path(old).name, "CK3_1.19.0")
        (self.fixture / "Crusader Kings III_1.19.0").mkdir()
        with self.assertRaisesRegex(analyzer.AnalysisError, "多个匹配"):
            analyzer.find_version_folders(self.fixture, "1.19.0", "1.19.0.6")

    def test_cli_persists_completed_evidence_and_version_info(self):
        self.write(self.old, "game/events/a.txt", "value = 1\n")
        self.write(self.new, "game/events/a.txt", "value = 2\n")
        for root in (self.old, self.new):
            self.write(root, "titus_branch.txt", "test-branch\n")
            self.write(root, "titus_rev.txt", "test-commit\n")
        output = self.fixture / "output with spaces"
        with contextlib.redirect_stdout(io.StringIO()):
            exit_code = analyzer.main(["analyze", str(self.old), str(self.new), "--output-dir", str(output)])
        self.assertEqual(exit_code, 0)
        data = json.loads((output / "diff_report.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["deep_diffs"]), 1)
        self.assertEqual(data["version_info"]["new"]["game_commit"], "test-commit")
        self.assertEqual(data["coverage"]["analyzed_files"], 1)
        self.assertIn("SHA256", (output / "diff_report.csv").read_text(encoding="utf-8"))
        self.assertTrue((output / data["artifacts"]["preliminary_bilibili"]).exists())
        self.assertFalse((output / data["artifacts"]["final"]).exists())

    def test_cli_rejects_output_inside_input(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(analyzer.main([
                "analyze", str(self.old), str(self.new), "--output-dir", str(self.old / "output")
            ]), 1)

    def test_compatibility_entrypoints_use_cwd(self):
        self.write(self.new, "game/events/new.txt", "namespace = test\n")
        for prefix in (".sisyphus", ".omo"):
            output = self.fixture / prefix.lstrip(".")
            completed = subprocess.run([
                sys.executable, "-B", str(ROOT / prefix / "skills/ck3_version_analyzer/ck3_analyzer.py"),
                "analyze", "old", "new", "--output-dir", str(output),
            ], cwd=self.fixture, capture_output=True, encoding="utf-8")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            data = json.loads((output / "diff_report.json").read_text(encoding="utf-8"))
            self.assertEqual(data["coverage"]["analyzed_files"], 1)

    def test_markdown_tables_detected_but_code_pipes_preserved(self):
        for table in ("A | B\n--- | ---\n1 | 2", "| A |\n| --- |\n| 1 |"):
            self.assertTrue(analyzer.format_errors(table))
        code = f"{analyzer.FENCE}pdx\n| A | B |\n| --- | --- |\n{analyzer.FENCE}\n"
        self.assertEqual(analyzer.format_errors(code), [])

    def test_bilibili_refuses_cross_artifact_links_and_unclosed_code(self):
        self.assertTrue(analyzer.format_errors("详见 diff_report.json", standalone=True))
        self.assertTrue(analyzer.format_errors("见 版本_初步分析报告.md", standalone=True))
        self.assertTrue(analyzer.format_errors(analyzer.FENCE + "diff\n+new\n"))
        self.assertEqual(analyzer.format_errors(
            "源码: game/common/defines/test.txt，见本报告关键变更章节", standalone=True
        ), [])

    def test_bilibili_generator_preserves_code_and_rejects_lossy_conversion(self):
        source = self.fixture / "final.md"
        text = "# 报告\n\n" + analyzer.FENCE + "pdx\n| A | B |\n" + analyzer.FENCE + "\n"
        source.write_text(text, encoding="utf-8")
        destination = Path(analyzer.generate_bilibili_version(source))
        self.assertEqual(destination.read_text(encoding="utf-8"), text)
        source.write_text("A | B\n--- | ---\n1 | 2", encoding="utf-8")
        with self.assertRaises(analyzer.AnalysisError):
            analyzer.generate_bilibili_version(source)

    def test_final_validation_accepts_consistent_self_contained_reports(self):
        self.write(self.new, "game/events/new.txt", "namespace = new\n")
        data = self.final_data(self.compare())
        self.assertEqual(validator.validate_data(data), [])
        self.assertEqual(validator.validate_report(self.final_text(data), data), [])
        self.assertEqual(validator.validate_report(self.final_text(data), data, standalone=True), [])

    def test_final_validation_rejects_fabricated_counts_and_missing_review(self):
        self.write(self.new, "game/events/new.txt", "namespace = new\n")
        report = self.compare()
        self.assertTrue(validator.validate_data(asdict(report)))
        data = self.final_data(report)
        text = self.final_text(data).replace("**新增文件**: 1", "**新增文件**: 99")
        self.assertTrue(any("新增文件" in error for error in validator.validate_report(text, data)))
        broken = deepcopy(data)
        broken["coverage"]["skipped"] = [{"path": "not-real.txt", "reason": "file_limit"}]
        self.assertTrue(validator.validate_data(broken))
        broken = deepcopy(data)
        broken["metadata"]["llm_review"]["reviewed_paths"] = ["binaries/not-real.exe"]
        self.assertTrue(validator.validate_data(broken))

    def test_final_validation_rejects_invalid_schema_shapes(self):
        for data in ({"schema_version": 1}, {"schema_version": 2, "summary": None}):
            self.assertTrue(validator.validate_data(data))
        data = self.final_data(self.compare())
        data["coverage"]["skipped"] = [None]
        self.assertTrue(validator.validate_data(data))

    def test_final_validation_cli(self):
        data = self.final_data(self.compare())
        json_path, final, bilibili = [self.fixture / name for name in ("data.json", "final.md", "bilibili.md")]
        json_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        for path in (final, bilibili):
            path.write_text(self.final_text(data), encoding="utf-8")
        completed = subprocess.run([
            sys.executable, "-B", str(validator_path), "--data", str(json_path),
            "--report", str(final), "--bilibili", str(bilibili),
        ], capture_output=True, encoding="utf-8")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("验证通过", completed.stdout)


if __name__ == "__main__":
    unittest.main()
