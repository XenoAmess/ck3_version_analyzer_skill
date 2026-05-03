# CK3 Version Analyzer Skill

## Description

自动化分析 Crusader Kings III 两个版本之间的差异，生成详细的对比分析报告。
**核心特点**：根据实际版本对比结果，动态识别变化的系统，并考虑文件数量和行数变化。

## Triggers

- "分析 CK3 版本差异"
- "对比 CK3 版本"
- "生成 CK3 版本报告"
- "ck3_version_analyzer"
- 对两个 CK3 版本文件夹进行差异分析

## Commands

### analyze
分析两个 CK3 版本文件夹的差异

**Usage**: `/ck3_version_analyzer analyze <版本A> <版本B> [选项]`

**Arguments**:
- `版本A`: 旧版本文件夹名称（默认: Crusader Kings III_1.18.4）
- `版本B`: 新版本文件夹名称（默认: Crusader Kings III_1.19.0）

**Options**:
- `--output-dir <目录>`: 输出目录（默认: diff_output）
- `--author <名字>`: 报告作者（默认: XenoAmess）
- `--model <模型>`: 分析模型（默认: MiniMax-M2.7）

## Workflow

### Phase 1: 准备阶段

1. 查找版本文件夹
   - 扫描当前目录下的 `Crusader Kings III_*` 格式文件夹
   - 或使用指定的版本A和版本B路径

### Phase 2: 执行对比

1. 扫描两个版本文件夹
   - 获取所有文件的 MD5 哈希（文本文件）或大小（二进制文件）
   - 跳过 `.idea` 目录
   - **新增**：统计每个文本文件的行数

2. 分类文件差异
   - **新增文件**: 仅存在于新版本
   - **删除文件**: 仅存在于旧版本
   - **修改文件**: 两版本都存在但内容不同
   - **未变化文件**: 两版本完全相同

3. 生成输出：
   - `diff_report.json` - 完整 JSON 数据
   - `diff_report.csv` - CSV 表格

### Phase 3: 自动检测变化的系统

**核心创新**：动态识别变化的系统，**同时考虑文件数量和行数变化**。

1. **文件扫描**
   - 对每个文件计算行数（文本文件）
   - 记录每个修改文件的旧行数和新行数

2. **系统归类**
   - 使用关键词匹配自动归类到系统：
     - religion: doctrine, holy_site, religion_family, faith, fervor
     - ui: gui, window_, pdx_account, interface
     - events: event, story_cycle
     - gfx: gfx, texture, model, dds, mesh, asset
     - audio: sound, music, bank, voice
     - binary: binaries, dll, exe, launcher
     - defines: defines, 00_defines, portraits
     - localization: localization, l_english, l_simp_chinese, l_
     - history: history, provinces, characters
     - decisions: decisions, decision
     - traits: traits, trait
     - modifiers: modifiers, modifier
     - culture: culture, cultural, tradition, innovation
     - ...（更多系统根据实际文件自动检测）

3. **显著性过滤（多条件判定）**

   系统被视为显著变化需满足以下任一条件：

   | 条件 | 阈值 | 说明 |
   |------|------|------|
   | 文件数量 | >= 3 个变化文件 | 变化文件数足够多 |
   | 新增/删除 | > 0 | 有新增或删除的文件 |
   | 行数绝对值 | >= 100 行 | 总行数变化较大 |
   | 行数比例 | >= 20% 且 >= 50 行 | 变化比例大且绝对值可观 |

4. **排序**
   - 按综合评分排序：`文件数 * 100 + 行数变化`
   - 确保文件数量多和行数变化大的系统排在前面

### Phase 4: 动态生成报告

根据 Phase 3 检测到的实际变化系统，动态生成报告结构：

1. **版本基本信息**
   - 游戏分支
   - 分析时间
   - 数据来源

2. **整体差异统计总览**
   - 新增/删除/修改/未变化文件数
   - 净变化数

3. **变化系统概览**
   - 按综合评分排序的所有显著变化系统
   - 每个系统显示：文件变化数、行数变化、变化比例

4. **各系统详细分析**（动态生成）
   - 每个变化系统的独立章节
   - 文件变化统计摘要（文件数 + 行数 + 变化比例）
   - 新增文件列表（最多显示20个）
   - 删除文件列表（最多显示20个）
   - 修改文件列表（最多显示20个）

5. **附录 A**: 完整变更文件统计 + TOP 50 新增/删除文件

6. **附录 B**: 生成信息
   - 报告生成时间
   - 分析模型
   - 协作人

### Phase 5: B站专栏版生成

- **必选输出**
- 所有表格语法转换为列表格式
- 适配 B站专栏不支持表格的特性

## Output Files

所有输出默认保存到 `diff_output/` 目录：

- `diff_report.json` (~28 MB) - 完整机器可读数据
- `diff_report.csv` (~7 MB) - CSV 表格格式
- `极详细分析报告.md` (~40 KB) - 动态分析报告
- `极详细分析报告_B站专栏版.md` (~40 KB) - B站专栏版

## Significance Detection Examples

### 场景1：多文件变化
```
religion: +45 -12 ~89 (146 文件, 12500 行变化, 8.5%)
→ 必然显著（文件数远超阈值）
```

### 场景2：少文件大改动
```
defines: +0 -0 ~1 (1 文件, 3500 行变化, 22.3%)
→ 显著（行数变化 >= 100 且比例 >= 20%）
```

### 场景3：单文件巨大改动
```
某新系统: +0 -0 ~1 (1 文件, 8000 行变化, 100%)
→ 显著（行数变化远超阈值）
```

### 场景4：新增文件
```
new_feature: +3 -0 ~0 (3 文件, 0 行变化)
→ 显著（有新增文件）
```

### 场景5：小改动（不显著）
```
tiny_change: +1 -0 ~2 (3 文件, 20 行变化, 1.2%)
→ 不显著（文件数达标但行数太少）
```

## Requirements

- Python 3.6+
- 两个月版本 CK3 游戏文件夹
- 足够的磁盘空间

## Notes

- 脚本会自动跳过 `.idea` 目录
- 二进制文件使用大小比较，文本文件使用 MD5 哈希和行数统计
- 行数统计只对文本文件有效，二进制文件行数为0
- 系统检测基于路径关键词，支持任何 CK3 版本
- B站专栏版会移除所有表格语法，改用列表格式