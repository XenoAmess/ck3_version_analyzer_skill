#!/usr/bin/env python3
"""
CK3 Version Analyzer - 自动化分析 Crusader Kings III 版本差异

Usage:
    python ck3_analyzer.py analyze [版本A] [版本B] [选项]

Options:
    --output-dir DIR      输出目录 (默认: diff_output)
    --author NAME         报告作者 (默认: XenoAmess)
    --model MODEL         分析模型 (默认: MiniMax-M2.7)
"""

import os
import sys
import json
import hashlib
import argparse
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Set
from collections import defaultdict

# Windows 编码修复
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


@dataclass
class FileInfo:
    path: str
    size: int
    md5: str
    is_binary: bool = False
    line_count: int = 0  # 文本文件的行数


@dataclass
class DiffReport:
    version_old: str
    version_new: str
    timestamp: str
    summary: dict = field(default_factory=dict)
    file_diffs: list = field(default_factory=list)


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
        ".dll",
        ".exe",
        ".dylib",
        ".so",
        ".dll.manifest",
        ".dds",
        ".tga",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".bmp",
        ".tiff",
        ".pdf",
        ".zip",
        ".tar",
        ".gz",
        ".rar",
        ".7z",
        ".wav",
        ".mp3",
        ".ogg",
        ".flac",
        ".aac",
        ".ttf",
        ".otf",
        ".woff",
        ".woff2",
        ".bank",
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


def compare_versions(
    old_dir: str, new_dir: str, version_old: str, version_new: str
) -> DiffReport:
    """比较两个版本"""
    print(f"\n[1/5] 扫描版本 {version_old}...")
    old_files = scan_directory(old_dir)
    print(f"  找到 {len(old_files)} 个文件")

    print(f"\n[2/5] 扫描版本 {version_new}...")
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
    print("\n[3/5] 自动检测变化的系统（分析文件数量 + 行数变化）...")

    # 游戏核心系统关键词
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
    }

    # 初始化系统数据结构
    systems = {}
    for system_name in system_keywords:
        systems[system_name] = {
            "added": [],
            "removed": [],
            "modified": [],
            "file_count": 0,
            "line_changes": 0,  # 新增：行数变化
            "total_old_lines": 0,
            "total_new_lines": 0,
        }

    # 对每个改变的路径进行分类并计算行数变化
    for d in report.file_diffs:
        if d["status"] == "unchanged":
            continue

        path = d["path"].lower()

        # 计算行数变化（仅对文本文件有效）
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

        # 归类到系统
        for system_name, keywords in system_keywords.items():
            for kw in keywords:
                if kw.lower() in path:
                    systems[system_name][d["status"]].append(d["path"])
                    if d["status"] == "modified":
                        systems[system_name]["line_changes"] += line_diff
                        systems[system_name]["total_old_lines"] += old_lines
                        systems[system_name]["total_new_lines"] += new_lines
                    break

    # 计算每个系统的总变化（文件数 + 行数权重）
    for system_name in systems:
        s = systems[system_name]
        s["file_count"] = len(s["added"]) + len(s["removed"]) + len(s["modified"])

    # 显著性过滤：考虑文件数和行数变化
    # 条件：
    # 1. 变化文件数 >= 3
    # 2. 或有新增/删除文件
    # 3. 或行数变化 >= 100 行
    # 4. 或行数变化比例 >= 20% 且绝对行数变化 >= 50 行
    significant_systems = {}
    for name, s in systems.items():
        is_significant = False

        # 条件1: 文件数足够多
        if s["file_count"] >= 3:
            is_significant = True
        # 条件2: 有新增或删除文件
        elif len(s["added"]) > 0 or len(s["removed"]) > 0:
            is_significant = True
        # 条件3: 行数变化足够大
        elif s["line_changes"] >= 100:
            is_significant = True
        # 条件4: 行数变化比例大且绝对值可观
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


def generate_dynamic_report(
    report: DiffReport,
    systems: Dict[str, dict],
    old_dir: str,
    new_dir: str,
    output_dir: str,
    author: str,
    model: str,
) -> str:
    """生成动态分析报告"""
    print("\n[4/5] 生成详细分析报告...")

    output_path = os.path.join(
        output_dir,
        f"Crusader_Kings_III_v{report.version_old}_vs_v{report.version_new}_极详细分析报告.md",
    )
    os.makedirs(output_dir, exist_ok=True)

    lines = []
    lines.append(
        f"# Crusader Kings III 版本 {report.version_old} vs {report.version_new} 极详细对比分析报告\n"
    )
    lines.append("## 版本基本信息\n")
    lines.append(f"- **游戏分支**: {report.version_old} → {report.version_new}")
    lines.append(f"- **分析时间**: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"- **数据来源**: compare_versions.py 自动分析 + 源代码深度审查")
    lines.append("")

    # 整体统计
    lines.append("---\n")
    lines.append("## 一、整体差异统计总览\n")
    lines.append(f"- **新增文件**: {report.summary['added']} 个")
    lines.append(f"- **删除文件**: {report.summary['removed']} 个")
    lines.append(f"- **修改文件**: {report.summary['modified']} 个")
    lines.append(f"- **未变化文件**: {report.summary['unchanged']} 个")
    lines.append(
        f"- **净变化**: {'+' if report.summary['added'] > report.summary['removed'] else ''}{report.summary['added'] - report.summary['removed']} 个文件\n"
    )

    # 变化系统列表（按综合评分排序：文件数*100 + 行数变化）
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
            if data.get("change_ratio", 0) > 0
            else ""
        )
        lines.append(
            f"- **{name}**: +{len(data['added'])} -{len(data['removed'])} ~{len(data['modified'])} "
            f"({data['file_count']} 个文件, {data.get('line_changes', 0)} 行变化){ratio_str}"
        )
    lines.append("")

    # 每个系统的详细分析
    section_num = 3
    for name, data in sorted(
        systems.items(),
        key=lambda x: x[1]["file_count"] * 100 + x[1].get("line_changes", 0),
        reverse=True,
    ):
        if data["file_count"] == 0 and data.get("line_changes", 0) == 0:
            continue

        lines.append("---\n")
        lines.append(f"## {section_num}、{system_name.upper()} 系统变化\n")

        # 变化统计摘要
        lines.append(
            f"**文件变化**: +{len(data['added'])} -{len(data['removed'])} ~{len(data['modified'])}"
        )
        lines.append(f"**行数变化**: {data.get('line_changes', 0)} 行")
        if data.get("change_ratio", 0) > 0:
            lines.append(f"**变化比例**: {data['change_ratio'] * 100:.1f}%")
        lines.append("")

        # 新增文件
        if data["added"]:
            lines.append(f"### {section_num}.1 新增文件 ({len(data['added'])} 个)\n")
            shown = data["added"][:20]  # 最多显示20个
            for f in shown:
                lines.append(f"- `{f}`")
            if len(data["added"]) > 20:
                lines.append(f"- ... 还有 {len(data['added']) - 20} 个新增文件")
            lines.append("")

        # 删除文件
        if data["removed"]:
            lines.append(f"### {section_num}.2 删除文件 ({len(data['removed'])} 个)\n")
            shown = data["removed"][:20]
            for f in shown:
                lines.append(f"- `{f}`")
            if len(data["removed"]) > 20:
                lines.append(f"- ... 还有 {len(data['removed']) - 20} 个删除文件")
            lines.append("")

        # 修改文件
        if data["modified"]:
            lines.append(f"### {section_num}.3 修改文件 ({len(data['modified'])} 个)\n")
            shown = data["modified"][:20]
            for f in shown:
                lines.append(f"- `{f}`")
            if len(data["modified"]) > 20:
                lines.append(f"- ... 还有 {len(data['modified']) - 20} 个修改文件")
            lines.append("")

        section_num += 1

    # 附录
    lines.append("---\n")
    lines.append("## 附录 A: 完整变更文件统计\n")
    lines.append(f"- 新增文件总计: {len(report.summary['added'])} 个")
    lines.append(f"- 删除文件总计: {len(report.summary['removed'])} 个")
    lines.append(f"- 修改文件总计: {len(report.summary['modified'])} 个")
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
    lines.append(f"- **报告生成时间**: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"- **分析模型**: {model}")
    lines.append(f"- **协作人**: {author}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  已生成: {output_path}")
    return output_path


def generate_bilibili_version(source_path: str) -> str:
    """生成 B站专栏特供版（无表格）"""
    print("  生成 B站专栏版...")

    with open(source_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 移除表格语法，转换为列表
    lines = content.split("\n")
    new_lines = []

    for line in lines:
        # 检测表格分隔线
        if re.match(r"\|[-:\s]+\|", line):
            continue
        # 检测表格行
        elif line.startswith("|") and line.endswith("|"):
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 2:
                for i, cell in enumerate(parts[1:]):
                    new_lines.append(f"- **{parts[0]}: {cell}**")
                continue
        new_lines.append(line)

    new_content = "\n".join(new_lines)
    # 移除多余的连续空行
    new_content = re.sub(r"\n{3,}", "\n\n", new_content)

    output_path = source_path.replace(
        "极详细分析报告.md", "极详细分析报告_B站专栏版.md"
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"  已生成: {output_path}")
    return output_path


def export_json(report: DiffReport, output_path: str):
    """导出 JSON 格式报告"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(asdict(report), f, indent=2, ensure_ascii=False)
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

    args = parser.parse_args()
    base_dir = os.path.dirname(os.path.abspath(__file__))

    print("=" * 60)
    print("  CK3 Version Analyzer")
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

    # 执行对比
    report = compare_versions(folder_a, folder_b, version_a_name, version_b_name)

    print(f"\n差异统计:")
    print(f"  新增: {report.summary['added']}")
    print(f"  删除: {report.summary['removed']}")
    print(f"  修改: {report.summary['modified']}")
    print(f"  未变: {report.summary['unchanged']}")

    # 导出基础格式（必选）
    export_json(report, os.path.join(args.output_dir, "diff_report.json"))
    export_csv(report, os.path.join(args.output_dir, "diff_report.csv"))

    # 自动检测变化的系统
    systems = detect_changed_systems(report)

    # 生成动态报告
    report_path = generate_dynamic_report(
        report, systems, folder_a, folder_b, args.output_dir, args.author, args.model
    )

    # 生成 B站专栏版（必选）
    generate_bilibili_version(report_path)

    print("\n" + "=" * 60)
    print("  完成!")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
