#!/usr/bin/env python3
"""
Crusader Kings III 版本差异对比工具
比较 1.18.4 和 1.19.0 两个版本的文件夹差异
"""

import os
import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional

# 确保 Windows 终端输出编码正确
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


@dataclass
class FileInfo:
    """文件信息"""

    path: str
    size: int
    md5: str
    is_binary: bool = False


@dataclass
class FileDiff:
    """文件差异"""

    path: str
    status: str  # 'added', 'removed', 'modified', 'unchanged'
    old_info: Optional[FileInfo] = None
    new_info: Optional[FileInfo] = None


@dataclass
class DiffReport:
    """差异报告"""

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
    }
    _, ext = os.path.splitext(filepath)
    return ext.lower() in binary_extensions


def scan_directory(base_path: str, relative_to: str = None) -> dict:
    """扫描目录获取所有文件信息"""
    files = {}
    base = Path(base_path)

    try:
        for root, dirs, filenames in os.walk(base):
            # 跳过 .idea 目录
            if ".idea" in Path(root).parts:
                continue

            for filename in filenames:
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, base)

                try:
                    stat = os.stat(filepath)
                    is_bin = is_binary_file(filepath)

                    files[rel_path] = FileInfo(
                        path=rel_path,
                        size=stat.st_size,
                        md5=calculate_md5(filepath) if not is_bin else "",
                        is_binary=is_bin,
                    )
                except Exception as e:
                    print(f"Error scanning {filepath}: {e}")
                    continue
    except Exception as e:
        print(f"Error walking directory {base_path}: {e}")

    return files


def compare_versions(
    old_dir: str, new_dir: str, version_old: str = "1.18.4", version_new: str = "1.19.0"
) -> DiffReport:
    """比较两个版本"""
    print(f"Scanning {version_old}...")
    old_files = scan_directory(old_dir)
    print(f"Found {len(old_files)} files in {version_old}")

    print(f"Scanning {version_new}...")
    new_files = scan_directory(new_dir)
    print(f"Found {len(new_files)} files in {version_new}")

    # 比较差异
    file_diffs = []
    all_paths = set(old_files.keys()) | set(new_files.keys())

    # 分类统计
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
            FileDiff(path=path, status=status, old_info=old_info, new_info=new_info)
        )

    return DiffReport(
        version_old=version_old,
        version_new=version_new,
        timestamp=datetime.now().isoformat(),
        summary=stats,
        file_diffs=[asdict(d) for d in file_diffs],
    )


def format_size(size: int) -> str:
    """格式化文件大小"""
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"


def print_report(report: DiffReport, show_unchanged: bool = False):
    """打印报告"""
    print("\n" + "=" * 80)
    print(f"  Crusader Kings III 版本差异报告")
    print(f"  {report.version_old} vs {report.version_new}")
    print("=" * 80)

    print(f"\n生成时间: {report.timestamp}")

    print("\n" + "-" * 80)
    print("  摘要统计")
    print("-" * 80)
    print(f"  新增文件:     {report.summary['added']:>6}")
    print(f"  删除文件:     {report.summary['removed']:>6}")
    print(f"  修改文件:     {report.summary['modified']:>6}")
    print(f"  未变化文件:   {report.summary['unchanged']:>6}")
    print("-" * 80)

    # 分类输出
    categories = [
        ("added", "[NEW] 新增文件"),
        ("removed", "[DEL] 删除文件"),
        ("modified", "[MOD] 修改文件"),
    ]

    for status_key, title in categories:
        diffs = [d for d in report.file_diffs if d["status"] == status_key]
        if diffs:
            print(f"\n{title} ({len(diffs)} 个)")
            print("-" * 80)
            for d in diffs:
                if status_key == "added":
                    info = d["new_info"]
                    size_str = format_size(info["size"]) if info else "?"
                    print(f"  + {d['path']} ({size_str})")
                elif status_key == "removed":
                    info = d["old_info"]
                    size_str = format_size(info["size"]) if info else "?"
                    print(f"  - {d['path']} ({size_str})")
                else:  # modified
                    old_info = d["old_info"]
                    new_info = d["new_info"]
                    old_size = format_size(old_info["size"]) if old_info else "?"
                    new_size = format_size(new_info["size"]) if new_info else "?"
                    if old_size != new_size:
                        print(f"  ~ {d['path']}")
                        print(f"      {old_size} -> {new_size}")
                    else:
                        print(f"  ~ {d['path']} ({old_size})")

    if show_unchanged:
        diffs = [d for d in report.file_diffs if d["status"] == "unchanged"]
        if diffs:
            print(f"\n[EQUAL] 未变化文件 ({len(diffs)} 个)")
            print("-" * 80)
            for d in diffs:
                print(f"  = {d['path']}")


def export_json(report: DiffReport, output_path: str):
    """导出 JSON 格式报告"""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(asdict(report), f, indent=2, ensure_ascii=False)
    print(f"\nJSON 报告已导出: {output_path}")


def export_csv(report: DiffReport, output_path: str):
    """导出 CSV 格式报告"""
    import csv

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
    print(f"CSV 报告已导出: {output_path}")


def export_markdown(report: DiffReport, output_path: str):
    """导出 Markdown 格式报告"""
    lines = [
        "# Crusader Kings III 版本差异报告",
        "",
        f"**版本对比**: {report.version_old} -> {report.version_new}",
        f"**生成时间**: {report.timestamp}",
        "",
        "## 摘要统计",
        "",
        f"| 类别 | 数量 |",
        f"|------|------:|",
        f"| [NEW] 新增 | {report.summary['added']} |",
        f"| [DEL] 删除 | {report.summary['removed']} |",
        f"| [MOD] 修改 | {report.summary['modified']} |",
        f"| [EQ] 未变 | {report.summary['unchanged']} |",
        "",
    ]

    # 分类输出
    categories = [
        ("added", "## [NEW] 新增文件"),
        ("removed", "## [DEL] 删除文件"),
        ("modified", "## [MOD] 修改文件"),
    ]

    for status_key, title in categories:
        diffs = [d for d in report.file_diffs if d["status"] == status_key]
        if diffs:
            lines.append(title)
            lines.append("")
            lines.append(f"共 {len(diffs)} 个文件")
            lines.append("")
            for d in diffs:
                if status_key == "added":
                    info = d["new_info"]
                    size_str = format_size(info["size"]) if info else "?"
                    lines.append(f"- `+ {d['path']}` ({size_str})")
                elif status_key == "removed":
                    info = d["old_info"]
                    size_str = format_size(info["size"]) if info else "?"
                    lines.append(f"- `- {d['path']}` ({size_str})")
                else:
                    old_info = d["old_info"]
                    new_info = d["new_info"]
                    old_size = format_size(old_info["size"]) if old_info else "?"
                    new_size = format_size(new_info["size"]) if new_info else "?"
                    lines.append(f"- `~ {d['path']}` ({old_size} -> {new_size})")
            lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Markdown 报告已导出: {output_path}")


def main():
    """主函数"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    version_18 = os.path.join(base_dir, "Crusader Kings III_1.18.4")
    version_19 = os.path.join(base_dir, "Crusader Kings III_1.19.0")

    # 如果目录不存在，尝试向上查找
    if not os.path.exists(version_18):
        version_18 = os.path.join(
            os.path.dirname(base_dir), "Crusader Kings III_1.18.4"
        )
    if not os.path.exists(version_19):
        version_19 = os.path.join(
            os.path.dirname(base_dir), "Crusader Kings III_1.19.0"
        )

    print("=" * 80)
    print("  Crusader Kings III 版本差异对比工具")
    print("=" * 80)
    print(f"\n版本 1.18.4: {version_18}")
    print(f"版本 1.19.0: {version_19}")

    if not os.path.exists(version_18):
        print(f"\n❌ 错误: 版本 1.18.4 目录不存在")
        return
    if not os.path.exists(version_19):
        print(f"\n❌ 错误: 版本 1.19.0 目录不存在")
        return

    # 执行比较
    report = compare_versions(version_18, version_19, "1.18.4", "1.19.0")

    # 打印报告
    print_report(report, show_unchanged=False)

    # 导出各种格式
    export_dir = os.path.join(base_dir, "diff_output")
    os.makedirs(export_dir, exist_ok=True)

    export_json(report, os.path.join(export_dir, "diff_report.json"))
    export_csv(report, os.path.join(export_dir, "diff_report.csv"))
    export_markdown(report, os.path.join(export_dir, "diff_report.md"))

    print(f"\n所有报告已导出到: {export_dir}")


if __name__ == "__main__":
    main()
