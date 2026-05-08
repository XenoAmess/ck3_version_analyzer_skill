#!/usr/bin/env python3
"""
CK3 Version Analyzer - 自动化分析 Crusader Kings III 版本差异
增强版：深度代码对比分析

Usage:
    python ck3_analyzer.py analyze [版本A] [版本B] [选项]

Options:
    --output-dir DIR      输出目录 (默认: diff_output)
    --author NAME         报告作者 (默认: XenoAmess)
    --model MODEL         分析模型 (默认: MiniMax-M2.7)
    --max-deep-files N    深度分析的最大文件数 (默认: 20)
    --no-deep-analysis    禁用深度代码分析
"""

import os
import sys
import json
import hashlib
import argparse
import re
import difflib
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Set, Tuple
from collections import defaultdict

# Windows 编码修复
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


# PDS脚本关键词及语义分类
PDS_KEYWORDS = {
    "game_mechanics": [
        "holder", "succession_laws", "government", "add_title_law", "remove_title_law",
        "add_realm_law", "change_government", "has_government", "succession_law",
        "single_heir", "partition", "acclamation", "elector", "claim"
    ],
    "traits": [
        "add_trait", "remove_trait", "has_trait", "trait", "give_trait",
        "set_trait_flag", "has_trait_with_flag", "num_traits"
    ],
    "triggers": [
        "trigger", "limit", "condition", "is_shown", "is_valid", "can_start",
        "any_", "all_", "exists", "NOT", "OR", "AND", "NOR", "NAND"
    ],
    "effects": [
        "effect", "add", "set", "remove", "change", "create", "destroy",
        "add_opinion", "add_modifier", "set_variable", "save_scope_as"
    ],
    "relations": [
        "relation", "opinion", "has_relation_", "is_", "any_", "target =",
        "friend", "rival", "lover", "enemy", "vassal", "liege"
    ],
    "pregnancy": [
        "pregnancy", "fertility", "child", "heir", "concubine", "marriage",
        "birth", "pregnant", "is_pregnant", "any_child"
    ],
    "ai_behavior": [
        "ai_will_do", "ai_potential", "ai_frequency", "ai_target", "ai_recipient",
        "ai_", "factor", "modifier", "base =", "add ="
    ],
    "events": [
        "trigger_event", "character_event", "diarchy_event", "story_event",
        "on_action", "on_accept", "on_decline", "on_send", "namespace"
    ],
    "interactions": [
        "interaction", "offer", "accept", "decline", "send_option",
        "is_shown", "is_valid", "cost", "category", "icon"
    ],
    "values": [
        "value", "opinion_value", "modifier", "add =", "multiply =",
        "high_", "medium_", "low_", "positive_", "negative_"
    ]
}

CHANGE_TYPE_KEYWORDS = {
    "major": [
        "succession_law", "government", "add_title_law", "remove_title_law",
        "holder", "dynasty", "inheritance", "succession"
    ],
    "feature": [
        "trigger_event", "new_event", "add_trait", "new_trait",
        "decision", "new_decision", "interaction", "new_interaction"
    ],
    "bugfix": [
        "any_", "empty", "null", "none", "exists", "NOT", "limit",
        "scope:", "trigger", "fix", "correct", "error"
    ],
    "balance": [
        "ai_will_do", "factor", "modifier", "add =", "multiply =",
        "base =", "value", "weight"
    ],
    "localization": [
        "l_english", "l_simp_chinese", "l_french", "l_german", "l_",
        "_l_", "localization"
    ],
    "gui": [
        "gui", "window", "interface", "icon", "texture", "dds", "sprite"
    ]
}


@dataclass
class FileInfo:
    path: str
    size: int
    md5: str
    is_binary: bool = False
    line_count: int = 0


@dataclass
class DiffHunk:
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    lines_added: List[str] = field(default_factory=list)
    lines_removed: List[str] = field(default_factory=list)
    lines_context: List[Tuple[str, str]] = field(default_factory=list)


@dataclass
class FileDeepDiff:
    path: str
    status: str
    change_type: str
    semantic_category: str
    game_impact: str
    hunks: List[DiffHunk] = field(default_factory=list)
    summary: str = ""
    old_lines_count: int = 0
    new_lines_count: int = 0


@dataclass
class DiffReport:
    version_old: str
    version_new: str
    timestamp: str
    summary: dict = field(default_factory=dict)
    file_diffs: list = field(default_factory=list)
    deep_diffs: List[FileDeepDiff] = field(default_factory=list)


def calculate_md5(filepath: str) -> str:
    """计算文件 MD5 哈希"""
    md5_hash = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
    except Exception:
        return ""


def is_binary_file(filepath: str) -> bool:
    """判断是否为二进制文件"""
    binary_extensions = {
        ".dll", ".exe", ".dylib", ".so", ".dll.manifest",
        ".dds", ".tga", ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff",
        ".pdf", ".zip", ".tar", ".gz", ".rar", ".7z",
        ".wav", ".mp3", ".ogg", ".flac", ".aac",
        ".ttf", ".otf", ".woff", ".woff2", ".bank",
    }
    _, ext = os.path.splitext(filepath)
    return ext.lower() in binary_extensions


def count_lines(filepath: str) -> int:
    """计算文本文件的行数"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def read_file_lines(filepath: str) -> List[str]:
    """读取文件所有行"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.readlines()
    except Exception:
        return []


def scan_directory(base_path: str) -> dict:
    """扫描目录获取所有文件信息"""
    files = {}
    base = Path(base_path)

    try:
        for root, dirs, filenames in os.walk(base):
            if ".idea" in Path(root).parts:
                continue
            for filename in filenames:
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, base)
                try:
                    stat = os.stat(filepath)
                    is_bin = is_binary_file(filepath)
                    line_count = count_lines(filepath) if not is_bin else 0
                    files[rel_path] = FileInfo(
                        path=rel_path,
                        size=stat.st_size,
                        md5=calculate_md5(filepath) if not is_bin else "",
                        is_binary=is_bin,
                        line_count=line_count,
                    )
                except Exception as e:
                    print(f"  警告: 扫描 {filepath} 时出错: {e}")
                    continue
    except Exception as e:
        print(f"  错误: 遍历目录 {base_path} 时出错: {e}")
    return files


def compute_line_diff(old_lines: List[str], new_lines: List[str], context: int = 3) -> List[DiffHunk]:
    """计算两文件版本的行级差异"""
    hunks = []
    diff = difflib.unified_diff(old_lines, new_lines, n=context)

    current_hunk = None
    for line in diff:
        if line.startswith('@@'):
            if current_hunk:
                hunks.append(current_hunk)

            match = re.match(r'@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@', line)
            if match:
                old_start = int(match.group(1))
                old_count = int(match.group(2)) if match.group(2) else 1
                new_start = int(match.group(3))
                new_count = int(match.group(4)) if match.group(4) else 1
                current_hunk = DiffHunk(
                    old_start=old_start,
                    old_count=old_count,
                    new_start=new_start,
                    new_count=new_count
                )
        elif line.startswith('+') and not line.startswith('+++'):
            if current_hunk:
                current_hunk.lines_added.append(line[1:].rstrip())
        elif line.startswith('-') and not line.startswith('---'):
            if current_hunk:
                current_hunk.lines_removed.append(line[1:].rstrip())
        elif line.startswith(' '):
            if current_hunk:
                current_hunk.lines_context.append(('context', line[1:].rstrip()))

    if current_hunk:
        hunks.append(current_hunk)

    return hunks


def classify_change_type(path: str, hunks: List[DiffHunk], old_content: str, new_content: str) -> Tuple[str, str, str]:
    """分类变更类型并识别语义类别"""
    path_lower = path.lower()
    change_type = "unknown"
    semantic_category = "other"
    game_impact = "无明显游戏性影响"

    added_lines = []
    removed_lines = []
    for hunk in hunks:
        added_lines.extend(hunk.lines_added)
        removed_lines.extend(hunk.lines_removed)

    all_changed_text = " ".join(added_lines + removed_lines).lower()

    if any(kw in path_lower for kw in ["localization", "l_english", "l_simp_chinese", "l_"]):
        change_type = "localization"
        semantic_category = "localization"
        game_impact = "仅文本翻译更新，无游戏性影响"
    elif any(kw in path_lower for kw in ["gui", "window_", "interface"]):
        change_type = "gui"
        semantic_category = "ui"
        game_impact = "界面/UI调整，不影响核心游戏机制"
    elif any(kw in path_lower for kw in ["binary", "dll", "exe", "launcher"]):
        change_type = "binary"
        semantic_category = "binary"
        game_impact = "二进制文件更新，可能是版本号变更或小修复"
    elif any(kw in path_lower for kw in ["event", "story_cycle"]):
        change_type = "feature"
        semantic_category = "events"
        if any(kw in all_changed_text for kw in ["trigger", "option", "effect"]):
            game_impact = "事件逻辑调整，可能影响游戏流程"
        else:
            game_impact = "事件内容/文本调整"
    elif any(kw in path_lower for kw in ["title", "law", "succession"]):
        change_type = "major"
        semantic_category = "title_system"
        game_impact = "⚠️ 继承法/头衔系统重大调整，影响游戏核心机制"
    elif any(kw in path_lower for kw in ["character_interaction", "interaction"]):
        change_type = "balance"
        semantic_category = "interactions"
        if any(kw in all_changed_text for kw in ["ai_will_do", "ai_potential", "factor", "modifier"]):
            game_impact = "⚠️ AI行为/互动平衡性调整"
        else:
            game_impact = "互动系统调整"
    elif any(kw in path_lower for kw in ["history", "province", "character"]):
        change_type = "feature"
        semantic_category = "history"
        game_impact = "历史数据/角色调整"
    elif any(kw in path_lower for kw in ["pregnancy", "fertility"]):
        change_type = "bugfix"
        semantic_category = "pregnancy_system"
        game_impact = "⚠️ 妊娠/生育系统修复"
    else:
        for ct, keywords in CHANGE_TYPE_KEYWORDS.items():
            if any(kw in all_changed_text for kw in keywords):
                change_type = ct
                break

        if change_type == "major":
            semantic_category = "game_mechanics"
            game_impact = "⚠️ 核心游戏机制调整"
        elif change_type == "bugfix":
            semantic_category = "bugfix"
            game_impact = "Bug修复，不会改变正常游戏体验"
        elif change_type == "balance":
            semantic_category = "balance"
            game_impact = "游戏平衡性调整"
        elif change_type == "feature":
            semantic_category = "features"
            game_impact = "新功能或功能调整"

    if any(kw in all_changed_text for kw in PDS_KEYWORDS["game_mechanics"]):
        if "⚠️" not in game_impact:
            game_impact = "⚠️ " + game_impact
        semantic_category = "game_mechanics"

    return change_type, semantic_category, game_impact


def generate_diff_summary(hunks: List[DiffHunk], max_lines: int = 15) -> str:
    """生成diff摘要"""
    total_added = sum(len(h.lines_added) for h in hunks)
    total_removed = sum(len(h.lines_removed) for h in hunks)

    summary_lines = []
    summary_lines.append(f"**+{total_added}** 行新增, **-{total_removed}** 行删除")

    if hunks:
        first_hunk = hunks[0]
        if first_hunk.lines_removed:
            summary_lines.append("\n**删除的关键内容** (前5行):")
            for line in first_hunk.lines_removed[:5]:
                if line.strip():
                    summary_lines.append(f"```pdx\n-{line}\n```")

        if first_hunk.lines_added:
            summary_lines.append("\n**新增的关键内容** (前5行):")
            for line in first_hunk.lines_added[:5]:
                if line.strip():
                    summary_lines.append(f"```pdx\n+{line}\n```")

    return "\n".join(summary_lines)


def compare_versions(
    old_dir: str, new_dir: str, version_old: str, version_new: str
) -> DiffReport:
    """比较两个版本"""
    print(f"\n[1/6] 扫描版本 {version_old}...")
    old_files = scan_directory(old_dir)
    print(f"  找到 {len(old_files)} 个文件")

    print(f"\n[2/6] 扫描版本 {version_new}...")
    new_files = scan_directory(new_dir)
    print(f"  找到 {len(new_files)} 个文件")

    file_diffs = []
    all_paths = set(old_files.keys()) | set(new_files.keys())
    stats = {"added": 0, "removed": 0, "modified": 0, "unchanged": 0}

    for path in sorted(all_paths):
        old_info = old_files.get(path)
        new_info = new_files.get(path)

        if old_info and not new_info:
            status = "removed"
            stats["removed"] += 1
        elif not old_info and new_info:
            status = "added"
            stats["added"] += 1
        elif old_info and new_info:
            if old_info.md5 == new_info.md5 and old_info.size == new_info.size:
                status = "unchanged"
                stats["unchanged"] += 1
            else:
                status = "modified"
                stats["modified"] += 1

        file_diffs.append(
            {
                "path": path,
                "status": status,
                "old_info": asdict(old_info) if old_info else None,
                "new_info": asdict(new_info) if new_info else None,
            }
        )

    return DiffReport(
        version_old=version_old,
        version_new=version_new,
        timestamp=datetime.now().isoformat(),
        summary=stats,
        file_diffs=file_diffs,
    )


def detect_changed_systems(report: DiffReport) -> Dict[str, dict]:
    """自动检测哪些系统发生了变化（考虑文件数量和行数变化）"""
    print("\n[3/6] 自动检测变化的系统（分析文件数量 + 行数变化）...")

    system_keywords = {
        "religion": ["doctrine", "holy_site", "religion_family", "faith", "fervor"],
        "ui": ["gui", "window_", "pdx_account", "interface"],
        "events": ["event", "story_cycle"],
        "gfx": ["gfx", "texture", "model", "dds", "mesh", "asset"],
        "audio": ["sound", "music", "bank", "voice"],
        "binary": ["binaries", "dll", "exe", "launcher"],
        "defines": ["defines", "00_defines", "portraits"],
        "localization": ["localization", "l_english", "l_simp_chinese", "l_"],
        "history": ["history", "provinces", "characters"],
        "decisions": ["decisions", "decision"],
        "traits": ["traits", "trait"],
        "modifiers": ["modifiers", "modifier"],
        "casus_belli": ["casus_belli", "cb_"],
        "culture": ["culture", "cultural", "tradition", "innovation"],
        "council": ["council", "councillor"],
        "court": ["court", "courtier"],
        "diarchy": ["diarchy", "duchy"],
        "war": ["war", "battle", "combat"],
        "map": ["map", "terrain", "province"],
        "title": ["title", "law", "succession"],
        "dynasty": ["dynasty", "house", "lineage"],
        "character": ["character", "portrait", "DNA"],
        "trade": ["trade", "trade_route", "economy"],
        "interest": ["interest", "clan"],
        "magic": ["magic", "spell"],
        "interactions": ["interaction", "character_interaction"],
        "pregnancy": ["pregnancy", "fertility"],
    }

    systems = {}
    for system_name in system_keywords:
        systems[system_name] = {
            "added": [],
            "removed": [],
            "modified": [],
            "file_count": 0,
            "line_changes": 0,
            "total_old_lines": 0,
            "total_new_lines": 0,
        }

    for d in report.file_diffs:
        if d["status"] == "unchanged":
            continue

        path = d["path"].lower()

        line_diff = 0
        old_lines = 0
        new_lines = 0
        if d["status"] == "modified":
            old_info = d.get("old_info")
            new_info = d.get("new_info")
            if old_info and new_info:
                old_lines = old_info.get("line_count", 0) or 0
                new_lines = new_info.get("line_count", 0) or 0
                line_diff = abs(new_lines - old_lines)

        for system_name, keywords in system_keywords.items():
            for kw in keywords:
                if kw.lower() in path:
                    systems[system_name][d["status"]].append(d["path"])
                    if d["status"] == "modified":
                        systems[system_name]["line_changes"] += line_diff
                        systems[system_name]["total_old_lines"] += old_lines
                        systems[system_name]["total_new_lines"] += new_lines
                    break

    for system_name in systems:
        s = systems[system_name]
        s["file_count"] = len(s["added"]) + len(s["removed"]) + len(s["modified"])

    significant_systems = {}
    for name, s in systems.items():
        is_significant = False

        if s["file_count"] >= 3:
            is_significant = True
        elif len(s["added"]) > 0 or len(s["removed"]) > 0:
            is_significant = True
        elif s["line_changes"] >= 100:
            is_significant = True
        elif s["total_old_lines"] > 0:
            change_ratio = s["line_changes"] / s["total_old_lines"]
            if change_ratio >= 0.2 and s["line_changes"] >= 50:
                is_significant = True

        if is_significant:
            s["change_ratio"] = (
                s["line_changes"] / s["total_old_lines"]
                if s["total_old_lines"] > 0
                else 0
            )
            significant_systems[name] = s

    print(f"  检测到 {len(significant_systems)} 个显著变化的系统:")
    for name, data in sorted(
        significant_systems.items(),
        key=lambda x: x[1]["file_count"] * 100 + x[1]["line_changes"],
        reverse=True,
    ):
        ratio_str = (
            f" ({data['change_ratio'] * 100:.1f}%)"
            if data.get("change_ratio", 0) > 0
            else ""
        )
        print(
            f"    - {name}: +{len(data['added'])} -{len(data['removed'])} ~{len(data['modified'])} "
            f"(文件) | {data['line_changes']} 行变化{ratio_str}"
        )

    return significant_systems


def perform_deep_analysis(
    report: DiffReport,
    old_dir: str,
    new_dir: str,
    max_files: int = 0
) -> List[FileDeepDiff]:
    """执行深度代码分析"""
    limit_str = "无限制" if max_files == 0 else f"最多分析 {max_files} 个文件"
    print(f"\n[4/6] 执行深度代码分析 ({limit_str})...")

    deep_diffs = []
    modified_files = [d for d in report.file_diffs if d["status"] == "modified"]

    count = 0
    for d in modified_files:
        if max_files > 0 and count >= max_files:
            print(f"  已达到最大分析文件数 ({max_files})，跳过剩余文件")
            break

        path = d["path"]
        if is_binary_file(path):
            continue

        old_path = os.path.join(old_dir, path)
        new_path = os.path.join(new_dir, path)

        if not os.path.exists(old_path) or not os.path.exists(new_path):
            continue

        old_lines = read_file_lines(old_path)
        new_lines = read_file_lines(new_path)

        if not old_lines and not new_lines:
            continue

        hunks = compute_line_diff(old_lines, new_lines)
        if not hunks:
            continue

        change_type, semantic_category, game_impact = classify_change_type(path, hunks, old_lines, new_lines)

        deep_diff = FileDeepDiff(
            path=path,
            status="modified",
            change_type=change_type,
            semantic_category=semantic_category,
            game_impact=game_impact,
            hunks=hunks,
            summary=generate_diff_summary(hunks),
            old_lines_count=len(old_lines),
            new_lines_count=len(new_lines)
        )
        deep_diffs.append(deep_diff)
        count += 1

        print(f"  分析: {path} -> {change_type}")

    deep_diffs.sort(key=lambda x: (
        0 if x.change_type == "major" else
        1 if x.change_type == "bugfix" else
        2 if x.change_type == "balance" else
        3 if x.change_type == "feature" else 4
    ))

    print(f"  深度分析完成，共分析 {len(deep_diffs)} 个文件")
    return deep_diffs


def generate_dynamic_report(
    report: DiffReport,
    systems: Dict[str, dict],
    deep_diffs: List[FileDeepDiff],
    old_dir: str,
    new_dir: str,
    output_dir: str,
    author: str,
    model: str,
) -> str:
    """生成动态分析报告（深度版）"""
    print("\n[5/6] 生成详细分析报告...")

    output_path = os.path.join(
        output_dir,
        f"Crusader_Kings_III_v{report.version_old}_vs_v{report.version_new}_初步分析报告.md",
    )
    os.makedirs(output_dir, exist_ok=True)

    lines = []
    lines.append(
        f"# Crusader Kings III 版本 {report.version_old} vs {report.version_new} 深度对比分析报告\n"
    )
    lines.append("## 版本基本信息\n")
    lines.append(f"- **游戏版本**: {report.version_old} → {report.version_new}")
    lines.append(f"- **分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- **数据来源**: CK3 Version Analyzer 自动化分析 + 源代码深度审查")
    lines.append("")

    lines.append("---\n")
    lines.append("## 一、整体差异统计总览\n")

    total_changes = report.summary['added'] + report.summary['removed'] + report.summary['modified']
    if total_changes <= 10:
        scale = "微小"
    elif total_changes <= 50:
        scale = "较小"
    elif total_changes <= 200:
        scale = "中等"
    elif total_changes <= 500:
        scale = "较大"
    else:
        scale = "巨大"

    lines.append(f"- **新增文件**: {report.summary['added']} 个")
    lines.append(f"- **删除文件**: {report.summary['removed']} 个")
    lines.append(f"- **修改文件**: {report.summary['modified']} 个")
    lines.append(f"- **未变化文件**: {report.summary['unchanged']} 个")
    lines.append(
        f"- **净变化**: {'+' if report.summary['added'] > report.summary['removed'] else ''}{report.summary['added'] - report.summary['removed']} 个文件"
    )
    lines.append(f"- **变更规模**: {scale} ({total_changes} 个文件)\n")

    lines.append("---\n")
    lines.append("## 二、变化系统概览\n")
    lines.append(f"共检测到 **{len(systems)}** 个显著变化的系统：\n")

    for name, data in sorted(
        systems.items(),
        key=lambda x: x[1]["file_count"] * 100 + x[1].get("line_changes", 0),
        reverse=True,
    ):
        ratio_str = (
            f" ({data.get('change_ratio', 0) * 100:.1f}% 变化)"
            if data.get('change_ratio', 0) > 0
            else ""
        )
        importance = "⚠️" if name in ["title", "succession", "government", "religion"] else ""
        lines.append(
            f"- **{importance}{name}**: +{len(data['added'])} -{len(data['removed'])} ~{len(data['modified'])} "
            f"({data['file_count']} 个文件, {data.get('line_changes', 0)} 行变化){ratio_str}"
        )
    lines.append("")

    lines.append("---\n")
    lines.append("## 三、深度代码分析\n")
    lines.append(f"对 **{len(deep_diffs)}** 个关键修改文件进行了深度代码对比分析：\n")

    section_num = 1
    for deep_diff in deep_diffs:
        lines.append(f"### 3.{section_num} `{deep_diff.path}`\n")
        lines.append(f"**变更类型**: {deep_diff.change_type.upper()}")
        lines.append(f"**语义类别**: {deep_diff.semantic_category}")
        lines.append(f"**游戏性影响**: {deep_diff.game_impact}\n")

        lines.append(f"**行数统计**: {deep_diff.old_lines_count} → {deep_diff.new_lines_count} 行\n")

        lines.append(f"**代码对比摘要**:\n")
        lines.append(deep_diff.summary)
        lines.append("")

        section_num += 1

    lines.append("---\n")
    lines.append("## 四、重大变更专项分析\n")

    major_changes = [d for d in deep_diffs if d.change_type in ["major", "bugfix", "balance"]]
    if major_changes:
        for deep_diff in major_changes:
            lines.append(f"### ⚠️ {deep_diff.path}\n")
            lines.append(f"**类型**: {deep_diff.change_type}")
            lines.append(f"**影响**: {deep_diff.game_impact}\n")
            lines.append(deep_diff.summary)
            lines.append("")
    else:
        lines.append("未检测到重大游戏性变更。\n")

    lines.append("---\n")
    lines.append("## 五、变更类型分布\n")

    change_type_counts = defaultdict(int)
    for d in deep_diffs:
        change_type_counts[d.change_type] += 1

    for ct in ["major", "bugfix", "balance", "feature", "localization", "gui", "other"]:
        if ct in change_type_counts:
            lines.append(f"- **{ct}**: {change_type_counts[ct]} 个文件")

    lines.append("")

    lines.append("---\n")
    lines.append("## 附录 A: 完整变更文件统计\n")
    lines.append(f"- 新增文件总计: {report.summary['added']} 个")
    lines.append(f"- 删除文件总计: {report.summary['removed']} 个")
    lines.append(f"- 修改文件总计: {report.summary['modified']} 个")
    lines.append("")

    lines.append("### 新增文件 TOP 50\n")
    added_files = [d["path"] for d in report.file_diffs if d["status"] == "added"]
    for i, f in enumerate(added_files[:50], 1):
        lines.append(f"{i}. `{f}`")
    lines.append("")

    lines.append("### 删除文件 TOP 50\n")
    removed_files = [d["path"] for d in report.file_diffs if d["status"] == "removed"]
    for i, f in enumerate(removed_files[:50], 1):
        lines.append(f"{i}. `{f}`")
    lines.append("")

    lines.append("---\n")
    lines.append("## 附录 B: 生成信息\n")
    lines.append(f"- **报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- **分析模型**: {model}")
    lines.append(f"- **协作人**: {author}")
    lines.append(f"- **深度分析文件数**: {len(deep_diffs)}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  已生成: {output_path}")
    return output_path


def generate_bilibili_version(source_path: str) -> str:
    """生成 B站专栏特供版（无表格）"""
    print("  生成 B站专栏版...")

    with open(source_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    new_lines = []

    for line in lines:
        if re.match(r"\|[-:\s]+\|", line):
            continue
        elif line.startswith("|") and line.endswith("|"):
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 2:
                for i, cell in enumerate(parts[1:], 1):
                    new_lines.append(f"- **{parts[0]}**: {cell}")
                continue
        new_lines.append(line)

    new_content = "\n".join(new_lines)
    new_content = re.sub(r"\n{3,}", "\n\n", new_content)

    output_path = source_path.replace(
        "初步分析报告.md", "初步分析报告_B站专栏版.md"
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"  已生成: {output_path}")
    return output_path


def export_json(report: DiffReport, output_path: str):
    """导出 JSON 格式报告"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    report_dict = asdict(report)
    for dd in report_dict.get("deep_diffs", []):
        dd["hunks"] = [
            {
                **hunk,
                "lines_added": hunk["lines_added"],
                "lines_removed": hunk["lines_removed"],
                "lines_context": [(t, c) for t, c in hunk["lines_context"]]
            }
            for hunk in dd["hunks"]
        ] if dd.get("hunks") else []

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report_dict, f, indent=2, ensure_ascii=False)
    print(f"  已导出: {output_path}")


def export_csv(report: DiffReport, output_path: str):
    """导出 CSV 格式报告"""
    import csv

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Status", "Path", "Old Size", "New Size", "Old MD5", "New MD5"]
        )
        for d in report.file_diffs:
            old_info = d["old_info"]
            new_info = d["new_info"]
            writer.writerow(
                [
                    d["status"],
                    d["path"],
                    old_info["size"] if old_info else "",
                    new_info["size"] if new_info else "",
                    old_info["md5"] if old_info else "",
                    new_info["md5"] if new_info else "",
                ]
            )
    print(f"  已导出: {output_path}")


def find_version_folders(base_dir: str, version_a: str, version_b: str):
    """查找版本文件夹"""
    folder_a = os.path.join(base_dir, version_a)
    folder_b = os.path.join(base_dir, version_b)

    if os.path.exists(folder_a) and os.path.exists(folder_b):
        return folder_a, folder_b

    print("\n可用版本文件夹:")
    available = []
    for item in os.listdir(base_dir):
        if item.startswith("Crusader Kings III_") or item.startswith("CK3_"):
            available.append(item)
            print(f"  - {item}")

    for item in available:
        if version_a.replace(".", "").replace("_", "").replace(" ", "") in item.replace(
            ".", ""
        ).replace("_", "").replace(" ", ""):
            folder_a = os.path.join(base_dir, item)
        if version_b.replace(".", "").replace("_", "").replace(" ", "") in item.replace(
            ".", ""
        ).replace("_", "").replace(" ", ""):
            folder_b = os.path.join(base_dir, item)

    if os.path.exists(folder_a) and os.path.exists(folder_b):
        return folder_a, folder_b

    return None, None


def main():
    parser = argparse.ArgumentParser(
        description="CK3 Version Analyzer - 自动化分析 Crusader Kings III 版本差异"
    )
    parser.add_argument(
        "command", nargs="?", default="analyze", help="命令 (默认: analyze)"
    )
    parser.add_argument(
        "version_a", nargs="?", default="Crusader Kings III_1.18.4", help="旧版本文件夹"
    )
    parser.add_argument(
        "version_b", nargs="?", default="Crusader Kings III_1.19.0", help="新版本文件夹"
    )
    parser.add_argument("--output-dir", default="diff_output", help="输出目录")
    parser.add_argument("--author", default="XenoAmess", help="报告作者")
    parser.add_argument("--model", default="MiniMax-M2.7", help="分析模型")
    parser.add_argument("--max-deep-files", type=int, default=0, help="深度分析的最大文件数 (默认: 0表示无限制)")
    parser.add_argument("--no-deep-analysis", action="store_true", help="禁用深度代码分析")

    args = parser.parse_args()
    base_dir = os.path.dirname(os.path.abspath(__file__))

    print("=" * 60)
    print("  CK3 Version Analyzer (Enhanced)")
    print("  Crusader Kings III 版本差异对比工具")
    print("=" * 60)

    folder_a, folder_b = find_version_folders(base_dir, args.version_a, args.version_b)

    if not folder_a:
        print(f"\n错误: 找不到版本 A ({args.version_a})")
        return 1
    if not folder_b:
        print(f"\n错误: 找不到版本 B ({args.version_b})")
        return 1

    print(f"\n版本 A: {folder_a}")
    print(f"版本 B: {folder_b}")
    print(f"输出目录: {args.output_dir}")

    version_a_name = (
        os.path.basename(folder_a)
        .replace("Crusader Kings III_", "")
        .replace("CK3_", "")
    )
    version_b_name = (
        os.path.basename(folder_b)
        .replace("Crusader Kings III_", "")
        .replace("CK3_", "")
    )

    report = compare_versions(folder_a, folder_b, version_a_name, version_b_name)

    print(f"\n差异统计:")
    print(f"  新增: {report.summary['added']}")
    print(f"  删除: {report.summary['removed']}")
    print(f"  修改: {report.summary['modified']}")
    print(f"  未变: {report.summary['unchanged']}")

    export_json(report, os.path.join(args.output_dir, "diff_report.json"))
    export_csv(report, os.path.join(args.output_dir, "diff_report.csv"))

    systems = detect_changed_systems(report)

    deep_diffs = []
    if not args.no_deep_analysis:
        deep_diffs = perform_deep_analysis(report, folder_a, folder_b, args.max_deep_files)
        report.deep_diffs = deep_diffs

    report_path = generate_dynamic_report(
        report, systems, deep_diffs, folder_a, folder_b, args.output_dir, args.author, args.model
    )

    generate_bilibili_version(report_path)

    print("\n" + "=" * 60)
    print("  完成!")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())