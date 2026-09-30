#!/usr/bin/env python3
"""Validate final CK3 deliverables against schema-v2 evidence, using standard library only."""

import argparse
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ck3_analyzer import COLLABORATOR, NO_MODEL, configure_console, format_errors, markdown_prose


def validate_data(data):
    errors = []
    if data.get("schema_version") != 2:
        return ["需要 schema_version=2 的证据；旧报告必须重新扫描"]
    summary = data.get("summary", {})
    keys = ("added", "removed", "modified", "unchanged", "total_old", "total_new")
    if not isinstance(summary, dict) or any(
        type(summary.get(key)) is not int or summary[key] < 0 for key in keys
    ):
        return ["summary 字段必须是非负整数"]
    files = data.get("file_diffs", [])
    deep = data.get("deep_diffs", [])
    if not isinstance(files, list) or not isinstance(deep, list):
        return ["file_diffs 和 deep_diffs 必须是列表"]
    if any(not isinstance(item, dict) or not isinstance(item.get("path"), str)
           for item in files + deep):
        return ["文件清单项必须是含字符串 path 的对象"]
    for item in files:
        for key in ("old_info", "new_info"):
            info = item.get(key)
            if info is not None and not isinstance(info, dict):
                return [f"{key} 必须为对象或 null"]
    counts = Counter(item.get("status") for item in files)
    if any(summary[key] != counts[key] for key in keys[:4]) or set(counts) - set(keys[:4]):
        errors.append("文件状态统计与 file_diffs 不一致")
    by_path = {item.get("path"): item for item in files}
    if len(by_path) != len(files):
        errors.append("file_diffs 存在重复路径")
    for side, total in (("old_info", "total_old"), ("new_info", "total_new")):
        if sum(item.get(side) is not None for item in files) != summary[total]:
            errors.append(f"{total} 与扫描文件清单不一致")
    if summary["total_old"] != summary["unchanged"] + summary["modified"] + summary["removed"]:
        errors.append("旧版总数公式不成立")
    if summary["total_new"] != summary["unchanged"] + summary["modified"] + summary["added"]:
        errors.append("新版总数公式不成立")
    changed = {path: item for path, item in by_path.items() if item["status"] != "unchanged"}
    binaries = {
        path for path, item in changed.items()
        if any(info and info.get("is_binary") for info in (item.get("old_info"), item.get("new_info")))
    }
    candidates = set(changed) - binaries
    coverage = data.get("coverage", {})
    if not isinstance(coverage, dict):
        return ["coverage 必须是对象"]
    skipped = coverage.get("skipped", [])
    if not isinstance(skipped, list) or any(
        not isinstance(item, dict) or not isinstance(item.get("path"), str) for item in skipped
    ):
        return ["coverage.skipped 必须为带路径的对象列表"]
    deep_paths = [item.get("path") for item in deep]
    skipped_paths = [item.get("path") for item in skipped]
    if (len(set(deep_paths)) != len(deep_paths) or len(set(skipped_paths)) != len(skipped_paths)
            or set(deep_paths) & set(skipped_paths)
            or set(deep_paths) | set(skipped_paths) != candidates):
        errors.append("深度分析与跳过清单未正确划分候选文本文件")
    expected = {
        "changed_files": len(changed), "candidate_files": len(candidates),
        "analyzed_files": len(deep), "skipped_files": len(skipped), "binary_files": len(binaries),
    }
    if any(coverage.get(key) != value for key, value in expected.items()):
        errors.append("coverage 统计与证据清单不一致")
    if coverage.get("all_text_files_analyzed") is not (not skipped):
        errors.append("all_text_files_analyzed 与跳过清单不一致")
    if set(coverage.get("binary_paths", [])) != binaries:
        errors.append("变化二进制清单不一致")
    for item in deep:
        source = by_path.get(item.get("path"), {})
        if item.get("status") != source.get("status"):
            errors.append("深度分析文件状态与扫描清单不一致")
        for key in ("lines_added", "lines_removed"):
            if item.get(key) != source.get(key):
                errors.append(f"深度分析与文件统计的 {key} 不一致")
    metadata = data.get("metadata", {})
    if not isinstance(metadata, dict) or not isinstance(metadata.get("llm_review"), dict):
        return errors + ["metadata 和 llm_review 必须是对象"]
    review = metadata.get("llm_review", {})
    reviewed = review.get("reviewed_paths", [])
    if not isinstance(reviewed, list) or len(set(reviewed)) != len(reviewed) or not set(reviewed) <= candidates:
        errors.append("LLM 复核清单必须是候选文本文件的无重复子集")
    if review.get("performed") is not True:
        errors.append("尚未记录 Agent/LLM 解读完成，初步报告不能作为最终交付")
    if metadata.get("collaborator") != COLLABORATOR:
        errors.append("证据元信息的协作人不是 XenoAmess")
    model = metadata.get("analysis_model", "").strip()
    if not model or model == NO_MODEL or re.fullmatch(r"\[.*\]", model):
        errors.append("缺少真实分析模型标签")
    try:
        generated = datetime.fromisoformat(metadata.get("final_generated_at", ""))
        if generated.tzinfo is None:
            errors.append("最终生成时间缺少时区")
    except (TypeError, ValueError):
        errors.append("final_generated_at 必须是包含时区的 ISO 8601 时间")
    versions = data.get("version_info", {})
    if not isinstance(versions, dict) or any(
        not isinstance(versions.get(side), dict) for side in ("old", "new")
    ):
        return errors + ["version_info 必须包含 old 和 new 对象"]
    if any(not versions.get(side, {}).get(key) for side in ("old", "new")
           for key in ("game_branch", "game_commit", "engine_branch", "engine_commit")):
        errors.append("版本基本信息缺失；无法获取的值也应明确写为未知")
    return errors


def field_values(prose, label):
    pattern = r"^\s*-\s+\*\*" + re.escape(label) + r"\*\*[:：]\s*(.*?)\s*$"
    return re.findall(pattern, prose, re.M)


def validate_report(content, data, standalone=False):
    artifact_names = tuple(data.get("artifacts", {}).values())
    errors = format_errors(content, standalone, artifact_names)
    prose, _ = markdown_prose(content)
    if not re.search(r"^# .+极详细对比分析报告", prose, re.M):
        errors.append("缺少最终报告标题")
    appendix = re.search(r"^## 附录 B[:：]\s*生成信息\s*$", prose, re.M)
    if not appendix:
        errors.append("缺少附录 B: 生成信息")
        appendix_text = ""
    else:
        appendix_text = prose[appendix.end():]
        if re.search(r"^## ", appendix_text, re.M):
            errors.append("附录 B 必须位于报告末尾")
    metadata = data["metadata"]
    reviewed_count = len(metadata["llm_review"]["reviewed_paths"])
    expected_appendix = {
        "报告生成时间": metadata["final_generated_at"], "分析模型": metadata["analysis_model"],
        "协作人": COLLABORATOR, "深度分析文件数": str(len(data["deep_diffs"])),
        "LLM复核文件数": str(reviewed_count),
    }
    for label, expected in expected_appendix.items():
        if field_values(appendix_text, label) != [expected]:
            errors.append(f"附录字段缺失、重复或与证据不一致: {label}")
    summary, coverage = data["summary"], data["coverage"]
    expected_numbers = {
        "新增文件": summary["added"], "删除文件": summary["removed"],
        "修改文件": summary["modified"], "未变化文件": summary["unchanged"],
        "旧版文件总数": summary["total_old"], "新版文件总数": summary["total_new"],
        "文件总数变化": summary["total_new"] - summary["total_old"],
        "候选文本文件数": coverage["candidate_files"], "已分析文本文件数": coverage["analyzed_files"],
        "跳过文本文件数": coverage["skipped_files"], "变化二进制文件数": coverage["binary_files"],
        "未复核文本文件数": coverage["candidate_files"] - reviewed_count,
    }
    for label, expected in expected_numbers.items():
        values = field_values(prose, label)
        if len(values) != 1 or not re.fullmatch(r"[+-]?\d+(?:\s*个)?", values[0]):
            errors.append(f"缺少唯一的整数统计字段: {label}")
        elif int(re.match(r"[+-]?\d+", values[0])[0]) != expected:
            errors.append(f"报告统计与证据不一致: {label}")
    version_section = re.search(r"^## 版本基本信息\s*\n(.*?)(?=^## |\Z)", prose, re.M | re.S)
    if not version_section:
        errors.append("缺少版本基本信息章节")
    else:
        section = version_section[1]
        for key, label in (("game_branch", "游戏分支"), ("game_commit", "游戏提交"),
                           ("engine_branch", "引擎分支"), ("engine_commit", "引擎提交")):
            block = re.search(r"- \*\*" + label + r"\*\*[:：]\s*\n(.*?)(?=^- \*\*|\Z)",
                              section, re.M | re.S)
            if not block:
                errors.append(f"版本字段缺失: {label}")
                continue
            for side, side_label in (("old", "旧版本"), ("new", "新版本")):
                expected = data["version_info"][side][key]
                if not re.search(r"^\s+- " + side_label + r"[:：]\s*" + re.escape(expected) + r"\s*$",
                                 block[1], re.M):
                    errors.append(f"版本字段与证据不一致: {label}/{side_label}")
    return errors


def main(argv=None):
    configure_console()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--bilibili", required=True)
    args = parser.parse_args(argv)
    try:
        data = json.loads(Path(args.data).read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("JSON 根节点必须为对象")
        errors = validate_data(data)
        if not errors:
            for filename, standalone in ((args.report, False), (args.bilibili, True)):
                errors.extend(f"{filename}: {error}" for error in validate_report(
                    Path(filename).read_text(encoding="utf-8"), data, standalone
                ))
        if errors:
            print("\n".join("- " + error for error in errors), file=sys.stderr)
            return 1
        print("验证通过：证据统计、覆盖清单、版本信息、生成信息、无表格及 B 站独立交付。")
        print("格式检查不能证明玩法结论正确；仍须核实源码证据。")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"验证失败: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
