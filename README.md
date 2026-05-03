# CK3 Version Analyzer

自动化分析 Crusader Kings III 两个版本之间的差异，生成详细的对比分析报告。

## 功能特性

- **动态系统检测**：根据实际文件变化自动识别变化的系统，而非固定分析项目
- **多维度评估**：同时考虑文件数量和行数变化，确保不遗漏重大改动
- **多种输出格式**：JSON、CSV、Markdown 详细报告
- **B站专栏适配**：自动生成无表格的 B站专栏特供版
- **零配置使用**：默认参数即可分析 1.18.4 vs 1.19.0

## 快速开始

### 基本用法

```bash
# 使用默认版本 (1.18.4 vs 1.19.0)
python ck3_analyzer.py analyze

# 指定版本
python ck3_analyzer.py analyze "Crusader Kings III_1.18.4" "Crusader Kings III_1.19.0"

# 指定输出目录
python ck3_analyzer.py analyze --output-dir my_output
```

### 输出文件

```
diff_output/
├── diff_report.json                                  # 完整数据 (机器可读)
├── diff_report.csv                                   # CSV 表格
├── Crusader_Kings_III_v1.18.4_vs_v1.19.0_极详细分析报告.md           # 详细报告
└── Crusader_Kings_III_v1.18.4_vs_v1.19.0_极详细分析报告_B站专栏版.md  # B站专栏版
```

## 显著性检测逻辑

系统被视为显著变化需满足以下任一条件：

| 条件 | 阈值 | 说明 |
|------|------|------|
| 文件数量 | >= 3 个变化文件 | 变化文件数足够多 |
| 新增/删除 | > 0 | 有新增或删除的文件 |
| 行数绝对值 | >= 100 行 | 总行数变化较大 |
| 行数比例 | >= 20% 且 >= 50 行 | 变化比例大且绝对值可观 |

**示例**：

```
# 场景1：多文件变化 → 显著
religion: +45 -12 ~89 (146 文件, 12500 行变化)

# 场景2：少文件大改动 → 显著（行数变化触发）
defines: +0 -0 ~1 (1 文件, 3500 行变化, 22.3%)

# 场景3：小改动 → 不显著
tiny_change: +1 -0 ~2 (3 文件, 20 行变化, 1.2%)
```

## 系统归类

文件按路径关键词归类到不同系统：

| 系统 | 关键词 |
|------|--------|
| religion | doctrine, holy_site, religion_family, faith, fervor |
| ui | gui, window_, pdx_account, interface |
| events | event, story_cycle |
| gfx | gfx, texture, model, dds, mesh, asset |
| audio | sound, music, bank, voice |
| binary | binaries, dll, exe, launcher |
| defines | defines, 00_defines, portraits |
| localization | localization, l_english, l_simp_chinese |
| history | history, provinces, characters |
| decisions | decisions, decision |
| traits | traits, trait |
| modifiers | modifiers, modifier |
| culture | culture, cultural, tradition, innovation |
| council | council, councillor |
| court | court, courtier |
| war | war, battle, combat |
| map | map, terrain, province |
| trade | trade, trade_route, economy |

## 报告示例

```markdown
# Crusader Kings III 版本 1.18.4 vs 1.19.0 极详细对比分析报告

## 一、整体差异统计总览

- **新增文件**: 583 个
- **删除文件**: 207 个
- **修改文件**: 3,789 个
- **净变化**: +376 个文件

## 二、变化系统概览

共检测到 8 个显著变化的系统：

- **religion**: +50 -25 ~100 (175 文件, 15000 行变化, 12.5%)
- **ui**: +15 -5 ~40 (60 文件, 8000 行变化, 8.2%)
- **defines**: +1 -0 ~2 (3 文件, 3500 行变化, 22.3%)
- **gfx**: +200 -30 ~100 (330 文件, 0 行变化)
- ...

## 三、RELIGION 系统变化

**文件变化**: +50 -25 ~100
**行数变化**: 15000 行
**变化比例**: 12.5%

### 3.1 新增文件 (50 个)

- `game/common/religion/doctrine_types/10_doctrines_religions.txt`
- `game/common/religion/doctrine_types/20_doctrines.txt`
- ...

### 3.2 删除文件 (25 个)

- `game/common/religion/doctrines/10_doctrines_religions.txt`
- ...

### 3.3 修改文件 (100 个)

- `game/common/religion/doctrine_group_types/00_doctrine_group_types.txt`
- ...
```

## 项目结构

```
.sisyphus/skills/ck3_version_analyzer/
├── ck3_analyzer.py    # 主分析脚本
├── skill.md           # Sisyphus Skill 定义
└── README.md          # 本文档
```

## 技术细节

### 文件扫描

- 文本文件：计算 MD5 哈希 + 行数
- 二进制文件：仅计算大小（.dll, .dds, .bank 等）
- 自动跳过 `.idea` 目录

### 行数统计

- 只对文本文件有效
- 变化比例 = |新行数 - 旧行数| / 旧行数
- 二进制文件的行数变化计为 0

### 排序算法

综合评分 = `文件数 * 100 + 行数变化`

确保文件数量多和行数变化大的系统排在前面。

## 依赖

- Python 3.6+
- 无需第三方库（标准库 only）

## 作者

- **XenoAmess**

## 分析模型

- MiniMax-M2.7 (minimax-cn-coding-plan/MiniMax-M2.7)