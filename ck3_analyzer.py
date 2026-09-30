#!/usr/bin/env python3
"""CK3 byte comparison and evidence extraction. Python 3.10+, standard library only.

The script produces preliminary evidence, not an LLM gameplay interpretation.
Run: python ck3_analyzer.py analyze "old directory" "new directory" --help
"""

import argparse
import codecs
import csv
import difflib
import hashlib
import io
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path


COLLABORATOR = "XenoAmess"
NO_MODEL = "未执行 LLM 解读（仅脚本分析）"
IGNORED_DIRS = {".idea", ".git", ".vscode", ".ruff_cache", "__pycache__"}
BINARY_EXTENSIONS = {
    ".dll", ".exe", ".dylib", ".so", ".dds", ".tga", ".png", ".jpg", ".jpeg",
    ".gif", ".bmp", ".tiff", ".pdf", ".zip", ".tar", ".gz", ".rar", ".7z",
    ".wav", ".mp3", ".ogg", ".flac", ".aac", ".ttf", ".otf", ".woff",
    ".woff2", ".bank", ".mesh", ".anim",
}
TEXT_EXTENSIONS = {
    ".txt", ".gui", ".yml", ".yaml", ".csv", ".json", ".xml", ".asset",
    ".gfx", ".mod", ".lua", ".settings", ".manifest", ".ini",
}
DIRECTORY_SYSTEMS = {
    "localization": "localization", "events": "events", "event": "events",
    "gui": "ui", "interface": "ui", "gfx": "gfx", "sound": "audio",
    "music": "audio", "audio": "audio", "binaries": "binary", "launcher": "binary",
    "history": "history", "map_data": "map", "map": "map",
    "religion": "religion", "religions": "religion", "doctrines": "religion",
    "holy_sites": "religion", "defines": "defines", "governments": "government",
    "government_types": "government", "laws": "title", "succession_election": "title",
    "culture": "culture", "cultures": "culture", "decisions": "decisions",
    "traits": "traits", "modifiers": "modifiers", "casus_belli_types": "casus_belli",
    "scripted_effects": "scripted_effects", "scripted_triggers": "scripted_triggers",
    "script_values": "script_values", "on_action": "on_actions",
    "on_actions": "on_actions", "character_interactions": "interactions",
    "interactions": "interactions", "council_positions": "council",
    "court_positions": "court", "dynasties": "dynasty", "houses": "dynasty",
    "men_at_arms_types": "war", "combat": "war",
}
HIGH_PRIORITY_SYSTEMS = {
    "defines", "government", "title", "religion", "scripted_effects",
    "scripted_triggers", "script_values", "on_actions", "interactions",
    "decisions", "traits", "modifiers", "casus_belli",
}
MECHANIC_PATTERN = re.compile(
    r"\b(?:add_title_law|remove_title_law|add_realm_law|succession_law|"
    r"change_government|has_government|holder|fertility|pregnancy)\b", re.I
)
AI_PATTERN = re.compile(r"\b(?:ai_will_do|ai_potential|ai_frequency|ai_target)\b", re.I)
TICK = chr(96)
FENCE = TICK * 3


class AnalysisError(ValueError):
    """An input or scan failure that would invalidate the comparison."""


@dataclass
class FileInfo:
    path: str
    size: int
    sha256: str
    is_binary: bool = False
    line_count: int | None = None
    encoding: str | None = None
    text_error: str | None = None


@dataclass
class DiffHunk:
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    lines: list[str] = field(default_factory=list)

    @property
    def lines_added(self):
        return [line[1:] for line in self.lines if line.startswith("+")]

    @property
    def lines_removed(self):
        return [line[1:] for line in self.lines if line.startswith("-")]


@dataclass
class FileDeepDiff:
    path: str
    status: str
    change_type: str
    semantic_category: str
    game_impact: str
    hunks: list[DiffHunk] = field(default_factory=list)
    summary: str = ""
    old_lines_count: int = 0
    new_lines_count: int = 0
    lines_added: int = 0
    lines_removed: int = 0


@dataclass
class DiffReport:
    version_old: str
    version_new: str
    timestamp: str
    summary: dict = field(default_factory=dict)
    file_diffs: list = field(default_factory=list)
    deep_diffs: list[FileDeepDiff] = field(default_factory=list)
    schema_version: int = 2
    version_info: dict = field(default_factory=dict)
    systems: dict = field(default_factory=dict)
    coverage: dict = field(default_factory=dict)
    issues: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    artifacts: dict = field(default_factory=dict)


def configure_console():
    # Importing this module must not replace or close the host process's streams.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def text_encoding(sample: bytes, fallback: str = "utf-8") -> str:
    if sample.startswith((codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE)):
        return "utf-32"
    if sample.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        return "utf-16"
    if sample.startswith(codecs.BOM_UTF8):
        return "utf-8-sig"
    return fallback


def is_binary_file(filepath, sample=None, encoding="utf-8") -> bool:
    suffix = Path(filepath).suffix.lower()
    if suffix in BINARY_EXTENSIONS:
        return True
    if sample is None:
        with open(filepath, "rb") as stream:
            sample = stream.read(8192)
    if text_encoding(sample, encoding) in {"utf-16", "utf-32"}:
        return False
    if suffix in TEXT_EXTENSIONS:
        return False  # Invalid declared text is reported, never silently discarded.
    if b"\0" in sample:
        return True
    try:
        codecs.getincrementaldecoder(text_encoding(sample, encoding))().decode(sample, final=False)
        return False
    except UnicodeError:
        return True


def read_file_lines(filepath, encoding=None) -> list[str]:
    if encoding is None:
        with open(filepath, "rb") as stream:
            encoding = text_encoding(stream.read(4))
    with open(filepath, encoding=encoding, errors="strict") as stream:
        return stream.readlines()


def scan_directory(base_path, issues=None, encoding="utf-8") -> dict:
    base = Path(base_path).resolve()
    if not base.is_dir():
        raise AnalysisError(f"输入不是目录: {base}")
    issues = issues if issues is not None else []
    files = {}

    def walk_error(error):
        raise AnalysisError(f"无法完整扫描 {base}: {error}") from error

    for root, dirs, filenames in os.walk(base, onerror=walk_error, followlinks=False):
        # Prune ignored directories rather than traversing their children.
        for directory in dirs:
            if directory not in IGNORED_DIRS and Path(root, directory).is_symlink():
                issues.append({
                    "phase": "scan", "path": str(Path(root, directory)), "reason": "跳过符号链接目录",
                })
        dirs[:] = sorted(
            directory for directory in dirs
            if directory not in IGNORED_DIRS and not Path(root, directory).is_symlink()
        )
        for filename in sorted(filenames):
            filepath = Path(root, filename)
            rel_path = filepath.relative_to(base).as_posix()
            if filepath.is_symlink():
                issues.append({"phase": "scan", "path": str(filepath), "reason": "跳过符号链接"})
                continue
            try:
                before = filepath.stat()
                digest = hashlib.sha256()
                sample = b""
                with filepath.open("rb") as stream:
                    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                        if not sample:
                            sample = chunk[:8192]
                        digest.update(chunk)
                binary = is_binary_file(filepath, sample, encoding)
                info = FileInfo(rel_path, before.st_size, digest.hexdigest(), binary)
                if not binary:
                    info.encoding = text_encoding(sample, encoding)
                    try:
                        with filepath.open(encoding=info.encoding, errors="strict") as stream:
                            info.line_count = sum(1 for _ in stream)
                    except UnicodeError as error:
                        info.text_error = str(error)
                        issues.append({
                            "phase": "decode", "path": str(filepath), "reason": str(error),
                        })
                after = filepath.stat()
                if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                    raise AnalysisError(f"扫描期间文件发生变化，请重试: {filepath}")
                files[rel_path] = info
            except OSError as error:
                raise AnalysisError(f"无法读取 {filepath}；停止以避免错误统计: {error}") from error
    return files


def read_version_info(version_dir, issues=None) -> dict:
    result = {}
    for key, filename in {
        "game_branch": "titus_branch.txt", "game_commit": "titus_rev.txt",
        "engine_branch": "clausewitz_branch.txt", "engine_commit": "clausewitz_rev.txt",
    }.items():
        filepath = Path(version_dir, filename)
        try:
            value = "".join(read_file_lines(filepath)).strip()
            result[key] = value or "未知（文件为空）"
        except (OSError, UnicodeError) as error:
            result[key] = "未知（文件缺失或不可读）"
            if issues is not None:
                issues.append({"phase": "metadata", "path": str(filepath), "reason": str(error)})
    return result


def compare_versions(old_dir, new_dir, version_old, version_new, encoding="utf-8") -> DiffReport:
    report = DiffReport(
        version_old, version_new, datetime.now().astimezone().isoformat(timespec="seconds")
    )
    old_files = scan_directory(old_dir, report.issues, encoding)
    new_files = scan_directory(new_dir, report.issues, encoding)
    stats = {status: 0 for status in ("added", "removed", "modified", "unchanged")}
    for path in sorted(old_files.keys() | new_files.keys()):
        old, new = old_files.get(path), new_files.get(path)
        if old is None:
            status = "added"
        elif new is None:
            status = "removed"
        elif old.sha256 == new.sha256:
            status = "unchanged"
        else:
            status = "modified"
        stats[status] += 1
        old_count = old.line_count if old else 0
        new_count = new.line_count if new else 0
        added = new_count if status == "added" else None
        removed = old_count if status == "removed" else None
        if status == "added":
            removed = 0 if added is not None else None
        elif status == "removed":
            added = 0 if removed is not None else None
        report.file_diffs.append({
            "path": path, "status": status,
            "old_info": asdict(old) if old else None, "new_info": asdict(new) if new else None,
            "lines_added": added, "lines_removed": removed,
            "line_changes": added + removed if added is not None and removed is not None else None,
            "net_line_change": (
                new_count - old_count if old_count is not None and new_count is not None else None
            ),
        })
    report.summary = {**stats, "total_old": len(old_files), "total_new": len(new_files)}
    report.version_info = {
        "old": read_version_info(old_dir, report.issues),
        "new": read_version_info(new_dir, report.issues),
    }
    report.metadata = {
        "hash_algorithm": "SHA-256", "text_encoding": encoding,
        "input_directories": {"old": str(Path(old_dir).resolve()), "new": str(Path(new_dir).resolve())},
        "collaborator": COLLABORATOR, "analysis_model": NO_MODEL,
        "ignored_directories": sorted(IGNORED_DIRS),
        "llm_review": {"performed": False, "reviewed_paths": []},
    }
    return report


def systems_for_path(path: str) -> list[str]:
    normalized = path.replace("\\", "/").lower()
    parts = normalized.split("/")
    for part in parts[:-1]:
        if part in DIRECTORY_SYSTEMS:
            primary = DIRECTORY_SYSTEMS[part]
            labels = [primary]
            if primary == "history":
                for segment, secondary in (("titles", "title"), ("characters", "character"),
                                           ("provinces", "map"), ("dynasties", "dynasty")):
                    if segment in parts:
                        labels.append(secondary)
            return labels
    if Path(normalized).suffix == ".gui":
        return ["ui"]
    if re.search(r"(?:^|_)l_(?:english|simp_chinese|french|german|spanish|russian|korean|japanese)\.ya?ml$", parts[-1]):
        return ["localization"]
    if Path(normalized).suffix in BINARY_EXTENSIONS:
        return ["binary"]
    return ["unclassified"]


def compute_line_diff(old_lines, new_lines, context=3) -> list[DiffHunk]:
    hunks, current = [], None
    for line in difflib.unified_diff(old_lines, new_lines, n=context, lineterm=""):
        if line.startswith("@@"):
            match = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", line)
            if not match:
                raise AnalysisError(f"无法解析差异块: {line}")
            current = DiffHunk(
                int(match[1]), int(match[2]) if match[2] is not None else 1,
                int(match[3]), int(match[4]) if match[4] is not None else 1,
            )
            hunks.append(current)
        elif current is not None and line[:1] in {"+", "-", " "}:
            # Only the initial diff headers are ignored; source beginning +++ is valid.
            current.lines.append(line.rstrip("\r\n"))
    return hunks


def classify_change_type(path, hunks, old_content="", new_content=""):
    system = systems_for_path(path)[0]
    changed = "\n".join(line[1:] for hunk in hunks for line in hunk.lines
                        if line.startswith(("+", "-")))
    if not hunks:
        return "byte_only", system, "字节不同但解码后文本相同或为空；未确认机制变化"
    if MECHANIC_PATTERN.search(changed):
        return "mechanics_candidate", system, "涉及机制关键词；需核实作用域、条件和调用链"
    if AI_PATTERN.search(changed):
        return "ai_candidate", system, "涉及 AI 规则；权重含义与实际行为需进一步核实"
    if system == "localization":
        return "localization_candidate", system, "本地化内容变化；需核实键、插值及显示逻辑"
    if system == "ui":
        return "ui_candidate", system, "界面内容变化；需核实交互和信息显示影响"
    return "text_change", system, "已确认文本变化；目的、Bug 修复与玩法影响尚未验证"


def generate_diff_summary(hunks, max_lines=20) -> str:
    if max_lines < 0 or max_lines == 1:
        raise AnalysisError("片段行数必须为 0 或至少 2")
    added = sum(len(h.lines_added) for h in hunks)
    removed = sum(len(h.lines_removed) for h in hunks)
    result = [f"**+{added}** 行新增，**-{removed}** 行删除"]
    flattened = [(index, line) for index, hunk in enumerate(hunks) for line in hunk.lines]
    if not flattened:
        return "\n".join(result)
    selected = set(range(len(flattened) if max_lines == 0 else min(max_lines, len(flattened))))
    # A long replacement must show evidence from both versions within the budget.
    if max_lines >= 2 and len(flattened) > max_lines:
        required = set()
        for prefix in ("-", "+"):
            index = next((i for i, (_, line) in enumerate(flattened) if line.startswith(prefix)), None)
            if index is not None:
                required.add(index)
        for index in required - selected:
            selected.remove(max(selected - required))
            selected.add(index)
    longest_fence = max((len(match[0]) for _, line in flattened
                         for match in re.finditer(TICK + "+", line)), default=0)
    fence = TICK * max(3, longest_fence + 1)
    result.extend(["", f"{fence}diff"])
    current_hunk, previous = None, -1
    for index in sorted(selected):
        hunk_index, line = flattened[index]
        if index != previous + 1:
            result.append(f"...（省略 {index - previous - 1} 行）")
        if hunk_index != current_hunk:
            hunk = hunks[hunk_index]
            result.append(f"@@ -{hunk.old_start},{hunk.old_count} +{hunk.new_start},{hunk.new_count} @@")
            current_hunk = hunk_index
        result.append(line)
        previous = index
    result.append(fence)
    omitted = len(flattened) - len(selected)
    if omitted:
        result.append(f"\n片段共省略 {omitted} 行（含上下文）；统计按完整差异计算。")
    return "\n".join(result)


def review_order(item):
    labels = systems_for_path(item["path"])
    priority = 0 if set(labels) & HIGH_PRIORITY_SYSTEMS else (
        2 if labels[0] in {"localization", "ui", "gfx", "audio"} else 1
    )
    old, new = item["old_info"] or {}, item["new_info"] or {}
    return priority, 0 if item["status"] in {"added", "removed"} else 1, -abs(
        new.get("size", 0) - old.get("size", 0)
    ), item["path"]


def perform_deep_analysis(report, old_dir, new_dir, max_files=0, enabled=True, snippet_lines=20):
    if max_files < 0:
        raise AnalysisError("--max-deep-files 不能为负数")
    changed = [item for item in report.file_diffs if item["status"] != "unchanged"]
    candidates, binaries = [], []
    for item in changed:
        infos = [info for info in (item["old_info"], item["new_info"]) if info]
        (binaries if any(info["is_binary"] for info in infos) else candidates).append(item)
    skipped, analyzed = [], []
    for item in sorted(candidates, key=review_order):
        reason = None
        if not enabled:
            reason = "disabled"
        elif max_files and len(analyzed) >= max_files:
            reason = "file_limit"
        elif any(info and info.get("text_error") for info in (item["old_info"], item["new_info"])):
            reason = "decode_error"
        if reason:
            skipped.append({"path": item["path"], "reason": reason})
            continue
        sides = []
        try:
            for directory, info in ((old_dir, item["old_info"]), (new_dir, item["new_info"])):
                if info is None:
                    sides.append([])
                    continue
                filepath = Path(directory, item["path"])
                # Verify the evidence still belongs to the scanned snapshot.
                raw = filepath.read_bytes()
                if hashlib.sha256(raw).hexdigest() != info["sha256"]:
                    raise AnalysisError(f"扫描后文件发生变化，请重试: {filepath}")
                content = raw.decode(info["encoding"], errors="strict")
                content = content.replace("\r\n", "\n").replace("\r", "\n")
                sides.append(io.StringIO(content).readlines())
        except (OSError, UnicodeError) as error:
            report.issues.append({"phase": "deep_analysis", "path": item["path"], "reason": str(error)})
            skipped.append({"path": item["path"], "reason": "read_error"})
            continue
        old_lines, new_lines = sides
        hunks = compute_line_diff(old_lines, new_lines)
        kind, category, impact = classify_change_type(item["path"], hunks)
        if not hunks and item["status"] in {"added", "removed"}:
            kind, impact = "empty_file", "空文件新增或删除；影响需结合引用方核实"
        added = sum(len(h.lines_added) for h in hunks)
        removed = sum(len(h.lines_removed) for h in hunks)
        item.update(lines_added=added, lines_removed=removed, line_changes=added + removed)
        summary = generate_diff_summary(hunks, snippet_lines)
        if item["status"] == "added":
            summary = "旧版本不存在此文件。\n\n" + summary
        elif item["status"] == "removed":
            summary = "新版本不存在此文件。\n\n" + summary
        analyzed.append(FileDeepDiff(
            item["path"], item["status"], kind, category, impact, hunks, summary,
            len(old_lines), len(new_lines), added, removed,
        ))
    report.deep_diffs = analyzed
    report.coverage = {
        "enabled": enabled, "changed_files": len(changed), "candidate_files": len(candidates),
        "analyzed_files": len(analyzed), "skipped_files": len(skipped), "skipped": skipped,
        "binary_files": len(binaries), "binary_paths": [item["path"] for item in binaries],
        "all_text_files_analyzed": not skipped, "max_deep_files": max_files,
    }
    return analyzed


def detect_changed_systems(report):
    systems = {}
    for item in report.file_diffs:
        if item["status"] == "unchanged":
            continue
        labels = systems_for_path(item["path"])
        for label in labels:
            entry = systems.setdefault(label, {
                "added": [], "removed": [], "modified": [], "file_count": 0,
                "primary_file_count": 0, "lines_added": 0, "lines_removed": 0,
                "line_changes": 0, "unknown_line_files": 0,
            })
            entry[item["status"]].append(item["path"])
            entry["file_count"] += 1
            entry["primary_file_count"] += int(label == labels[0])
            if item["line_changes"] is None:
                entry["unknown_line_files"] += 1
            else:
                entry["lines_added"] += item["lines_added"]
                entry["lines_removed"] += item["lines_removed"]
                entry["line_changes"] += item["line_changes"]
    for label, entry in systems.items():
        entry["priority_candidate"] = (
            label in HIGH_PRIORITY_SYSTEMS or entry["file_count"] >= 3
            or bool(entry["added"] or entry["removed"]) or entry["line_changes"] >= 100
        )
    report.systems = systems
    return systems  # Keep small and unclassified changes visible.


def report_stem(report):
    def clean(value):
        return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value).strip(" .") or "unknown"
    return f"Crusader_Kings_III_v{clean(report.version_old)}_vs_v{clean(report.version_new)}"


def code_span(value):
    return TICK + value.replace(TICK, "'") + TICK


def generate_dynamic_report(report, systems, deep_diffs, old_dir, new_dir, output_dir,
                            author=COLLABORATOR, model=NO_MODEL):
    if author != COLLABORATOR:
        raise AnalysisError(f"协作人必须为 {COLLABORATOR}")
    report.metadata["analysis_model"] = model
    lines = [
        f"# Crusader Kings III {report.version_old} → {report.version_new} 初步分析报告",
        "", "此报告由脚本生成。分类是审查候选，未执行 LLM 玩法解读。", "",
        "## 版本基本信息", "",
    ]
    for key, label in (("game_branch", "游戏分支"), ("game_commit", "游戏提交"),
                       ("engine_branch", "引擎分支"), ("engine_commit", "引擎提交")):
        lines.extend([f"- **{label}**:",
                      f"  - 旧版本: {report.version_info['old'][key]}",
                      f"  - 新版本: {report.version_info['new'][key]}"])
    lines.extend(["", "## 整体差异统计总览", ""])
    for key, label in (("added", "新增文件"), ("removed", "删除文件"),
                       ("modified", "修改文件"), ("unchanged", "未变化文件")):
        lines.append(f"- **{label}**: {report.summary[key]} 个")
    lines.extend([
        f"- **旧版文件总数**: {report.summary['total_old']}",
        f"- **新版文件总数**: {report.summary['total_new']}",
        f"- **文件总数变化**: {report.summary['total_new'] - report.summary['total_old']:+d}",
        "- **比较口径**: 所有文件均比较 SHA-256；未变化表示扫描时内容哈希相同。",
        "", "## 分析覆盖", "",
    ])
    coverage = report.coverage
    for key, label in (("candidate_files", "候选文本文件数"), ("analyzed_files", "已分析文本文件数"),
                       ("skipped_files", "跳过文本文件数"), ("binary_files", "变化二进制文件数")):
        lines.append(f"- **{label}**: {coverage[key]}")
    lines.append("- 二进制仅确认内容变化，不能从哈希推断玩法影响。")
    if coverage["skipped"]:
        lines.extend(["", "### 跳过原因", ""])
        for item in coverage["skipped"]:
            lines.append(f"- {code_span(item['path'])}: {item['reason']}")
    lines.extend(["", "## 变化系统", "",
                  "主分类计数不重复；附加标签可能重叠，系统计数不可直接相加。行变化为新增行＋删除行；未计算不等于零。", ""])
    for name, data in sorted(systems.items(), key=lambda pair: (
        not pair[1]["priority_candidate"], -pair[1]["line_changes"], -pair[1]["file_count"], pair[0]
    )):
        lines.append(
            f"- **{name}**: +{len(data['added'])} / -{len(data['removed'])} / "
            f"~{len(data['modified'])} 文件；主分类 {data['primary_file_count']}；"
            f"已计算差异 {data['line_changes']} 行；未计算 {data['unknown_line_files']} 个文件"
        )
    lines.extend(["", "## 文本差异证据", ""])
    for index, diff in enumerate(deep_diffs, 1):
        lines.extend([
            f"### {index}. {code_span(diff.path)}", "",
            f"- **文件状态**: {diff.status}", f"- **候选分类**: {diff.change_type}",
            f"- **审查提示**: {diff.game_impact}",
            f"- **文件行数**: {diff.old_lines_count} → {diff.new_lines_count}",
            "", diff.summary, "",
        ])
    if not deep_diffs:
        lines.append("未提取文本差异证据；不能据此断言没有重要机制变化。")
    lines.extend(["", "## 扫描及读取说明", ""])
    lines.append("- 排除目录: " + "、".join(sorted(IGNORED_DIRS)))
    if report.issues:
        for issue in report.issues:
            lines.append(f"- {issue['phase']}: {code_span(issue['path'])} — {issue['reason']}")
    else:
        lines.append("- 未记录读取异常。")
    lines.extend([
        "", "## 附录 B: 生成信息", "",
        f"- **报告生成时间**: {report.timestamp}",
        f"- **分析模型**: {model}", f"- **协作人**: {COLLABORATOR}",
        f"- **深度分析文件数**: {len(deep_diffs)}", "",
    ])
    output_path = Path(output_dir, report_stem(report) + "_初步分析报告.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return str(output_path)


def markdown_prose(content):
    """Exclude fenced code; retain fence positions and require a closing fence."""
    prose, marker, length = [], None, 0
    for line in content.splitlines():
        fence = re.match(r"^\s*([~]{3,}|[" + TICK + r"]{3,})(.*)$", line)
        if fence:
            token, tail = fence.groups()
            if marker is None:
                marker, length = token[0], len(token)
            elif token[0] == marker and len(token) >= length and not tail.strip():
                marker, length = None, 0
            continue
        if marker is None:
            prose.append(line)
    return "\n".join(prose), marker is not None


def format_errors(content, standalone=False, artifact_names=()):
    prose, unclosed = markdown_prose(content)
    errors = ["代码块未闭合"] if unclosed else []
    # GFM tables may omit leading/trailing pipes. Do not inspect code blocks.
    for line in prose.splitlines():
        cells = line.strip().strip("|").split("|")
        if "|" in line and all(re.fullmatch(r"\s*:?-{3,}:?\s*", cell) for cell in cells):
            errors.append("报告正文包含 Markdown 表格")
            break
    if standalone:
        known = set(artifact_names) | {"diff_report.json", "diff_report.csv", "diff_report.md"}
        for name in sorted(known):
            if name and name in content:
                errors.append(f"B 站版引用了产物文件: {name}")
        if re.search(r"[^\s/\\]*?(?:初步分析报告|极详细对比分析报告)[^\s/\\]*?\.md", content):
            errors.append("B 站版包含其他报告产物的文件名")
    return errors


def generate_bilibili_version(source_path):
    source = Path(source_path)
    errors = format_errors(source.read_text(encoding="utf-8"), standalone=True)
    if errors:
        raise AnalysisError("；".join(errors) + "；请先整理源报告，避免转换损坏代码或丢失信息")
    if source.stem.endswith("_B站专栏版"):
        raise AnalysisError("输入已经是 B 站版，拒绝覆盖源报告")
    destination = source.with_name(source.stem + "_B站专栏版.md")
    destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    return str(destination)


def export_json(report, output_path):
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(asdict(report), ensure_ascii=False, indent=2), encoding="utf-8")


def export_csv(report, output_path):
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["Status", "Path", "Old Size", "New Size", "Old SHA256", "New SHA256",
                         "Lines Added", "Lines Removed", "Net Line Change"])
        for item in report.file_diffs:
            old, new = item["old_info"] or {}, item["new_info"] or {}
            writer.writerow([
                item["status"], item["path"], old.get("size", ""), new.get("size", ""),
                old.get("sha256", ""), new.get("sha256", ""), item["lines_added"],
                item["lines_removed"], item["net_line_change"],
            ])


def find_version_folders(base_dir, version_a, version_b):
    base = Path(base_dir).resolve()

    def resolve_version(value):
        exact = Path(value)
        if not exact.is_absolute():
            exact = base / exact
        if exact.is_dir():
            return str(exact.resolve())
        # Exact short version aliases only: 1.19.0 must never select 1.19.0.6.
        if Path(value).name == value:
            matches = [base / (prefix + value) for prefix in ("Crusader Kings III_", "CK3_")]
            matches = [path for path in matches if path.is_dir()]
            if len(matches) == 1:
                return str(matches[0].resolve())
            if len(matches) > 1:
                raise AnalysisError(f"版本 {value} 有多个匹配，请指定完整目录: {matches}")
        raise AnalysisError(f"找不到版本目录: {exact}；请指定完整目录或绝对路径")

    return resolve_version(version_a), resolve_version(version_b)


def main(argv=None):
    configure_console()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", nargs="?", default="analyze", choices=["analyze"])
    parser.add_argument("version_a", nargs="?", default="Crusader Kings III_1.18.4")
    parser.add_argument("version_b", nargs="?", default="Crusader Kings III_1.19.0")
    parser.add_argument("--base-dir", default=".", help="相对输入路径的基准，默认当前工作目录")
    parser.add_argument("--output-dir", help="默认 diff_output_<旧版本>_vs_<新版本>，相对当前工作目录")
    parser.add_argument("--author", default=COLLABORATOR, choices=[COLLABORATOR],
                        help="兼容旧命令；协作人固定为 XenoAmess")
    parser.add_argument("--model", default=NO_MODEL, help="仅记录真实模型标签，不调用或切换模型")
    parser.add_argument("--max-deep-files", type=int, default=0, help="0=全量文本分析；先排序再限制")
    parser.add_argument("--snippet-lines", type=int, default=20, help="每文件展示的原始差异行预算，0=不限")
    parser.add_argument("--no-deep-analysis", action="store_true", help="仅扫描和统计，不计算修改文件行差异")
    parser.add_argument("--encoding", default="utf-8", help="无 BOM 文本的编码；严格解码，BOM 自动识别")
    args = parser.parse_args(argv)
    if args.max_deep_files < 0 or args.snippet_lines < 0 or args.snippet_lines == 1:
        parser.error("文件数不得为负，片段行数必须为 0 或至少 2")
    try:
        codecs.lookup(args.encoding)
        old, new = find_version_folders(args.base_dir, args.version_a, args.version_b)
        if Path(old) == Path(new):
            raise AnalysisError("旧版本与新版本不能是同一个目录")
        old_name = re.sub(r"^(?:Crusader Kings III_|CK3_)", "", Path(old).name)
        new_name = re.sub(r"^(?:Crusader Kings III_|CK3_)", "", Path(new).name)
        output = Path(args.output_dir or f"diff_output_{old_name}_vs_{new_name}").resolve()
        if any(output == Path(root) or Path(root) in output.parents for root in (old, new)):
            raise AnalysisError("输出目录不得位于任一输入目录内")
        print(f"比较: {old}\n   → {new}\n输出: {output}")
        report = compare_versions(old, new, old_name, new_name, args.encoding)
        deep = perform_deep_analysis(report, old, new, args.max_deep_files,
                                     not args.no_deep_analysis, args.snippet_lines)
        systems = detect_changed_systems(report)
        preliminary = generate_dynamic_report(
            report, systems, deep, old, new, output, args.author, args.model
        )
        bilibili = generate_bilibili_version(preliminary)
        stem = report_stem(report)
        report.artifacts = {
            "json": "diff_report.json", "csv": "diff_report.csv",
            "preliminary": Path(preliminary).name, "preliminary_bilibili": Path(bilibili).name,
            "final": stem + "_极详细对比分析报告.md",
            "final_bilibili": stem + "_极详细对比分析报告_B站专栏版.md",
        }
        # Persist the completed evidence, coverage, metadata and systems together.
        export_json(report, output / "diff_report.json")
        export_csv(report, output / "diff_report.csv")
        print(f"统计: {report.summary}\n文本覆盖: {len(deep)}/{report.coverage['candidate_files']}")
        print("脚本完成初步证据提取；最终玩法报告由当前 Agent 继续撰写。")
        return 0
    except (AnalysisError, OSError, LookupError) as error:
        print(f"错误: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
