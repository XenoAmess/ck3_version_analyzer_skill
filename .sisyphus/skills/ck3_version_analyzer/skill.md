# CK3 Version Analyzer Skill

## Description

自动化分析 Crusader Kings III 两个版本之间的差异，生成**深入的代码级别对比分析报告**。
**核心特点**：
1. 动态识别变化的系统（考虑文件数量和行数变化）
2. **深度代码对比**：读取变更文件的实际内容，进行逐行diff分析
3. **LLM深度解读**：基于初步分析报告和源代码，AI进行游戏性层面的深入解读
4. **代码片段展示**：在报告中展示关键的变更代码片段
5. **游戏性影响详解**：解释每个变更对游戏玩法的实际影响

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
- `--max-deep-files <数量>`: 深度分析的最大文件数（默认: 0表示无限制）
- `--no-deep-analysis`: 禁用深度代码分析（仅做文件统计）

## Workflow

### Phase 1: 准备阶段

1. 查找版本文件夹
   - 扫描当前目录下的 `Crusader Kings III_*` 格式文件夹
   - 或使用指定的版本A和版本B路径

### Phase 2: 执行对比（快速扫描）

1. 扫描两个版本文件夹
   - 获取所有文件的 MD5 哈希（文本文件）或大小（二进制文件）
   - 跳过 `.idea` 目录
   - 统计每个文本文件的行数

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

### Phase 4: 深度代码分析

**核心增强**：对显著变化的文件进行**逐行代码对比分析**。

1. **文本文件逐行Diff**
   - 使用 `difflib` 计算精确的行级差异
   - 区分：新增行、删除行、修改行
   - 记录上下文行（前后各3行）

2. **变更分类**
   - **重大变更**: 涉及游戏机制、数值平衡、法律系统
   - **功能变更**: 新增/移除事件、互动、触发器
   - **Bug修复**: 修正逻辑错误、空值处理、边界情况
   - **本地化更新**: 仅文本修改，无游戏性影响
   - **格式化/代码重构**: 无实际功能变化

3. **关键词语义识别**
   - 识别PDS脚本关键概念并解释：
     - `holder`, `succession_laws`, `government` → 统治权/继承
     - `add_trait`, `remove_trait`, `has_trait` → 特质系统
     - `trigger`, `limit`, `condition` → 触发条件
     - `effect`, `add`, `set` → 游戏效果
     - `opinion`, `relation`, `has_relation_*` → 关系系统
     - `fertility`, `pregnancy`, `child` → 妊娠/继承系统
     - `ai_will_do`, `ai_potential` → AI行为

4. **新旧代码对比展示** ⭐ 重要
   - **每个变更必须展示旧代码和新代码对比**
   - 旧代码：标记为"**旧代码** (被删除的内容)"，使用 `-` 前缀
   - 新代码：标记为"**新代码** (新增的内容)"，使用 `+` 前缀
   - 除非是完全新增的文件（没有旧版本），否则必须展示旧代码
   - 每个变更最多显示20行代码片段，超出部分标注剩余数量

5. **游戏性影响评估**
   - 每个变更附带游戏性影响说明
   - 重大变更有⚠️标记和详细解释
   - 关联其他系统的变更会交叉引用

### Phase 5: 动态生成初步报告

根据 Phase 3-4 的分析结果，生成初步分析报告 `初步分析报告.md`：
- 版本基本信息（从titus_rev.txt等文件读取分支、提交信息）
- 整体差异统计总览（新增/删除/修改文件数及文件总数）
- 变化系统概览
- 各系统深度分析（含新旧代码对比片段）
- 重大变更专项分析
- 附录

### Phase 6: LLM深度解读 ⭐ 核心二次分析

**重要**：在 ck3_analyzer.py 产出 `初步分析报告.md` 后，需要**手动使用大模型进行深度解读**。

**强制要求**：最终生成的 `极详细对比分析报告.md` 开头**必须包含**以下内容：

1. **版本基本信息**（从 `diff_report.json` 或 `初步分析报告.md` 中读取）：
   - 游戏分支（game_branch）
   - 游戏提交（game_commit）
   - 引擎分支（engine_branch）
   - 引擎提交（engine_commit）

2. **整体差异统计总览**：
   - 新增/删除/修改/未变化文件数
   - 文件总数变化

**输入**：
- `初步分析报告.md` - 初步分析报告
- `diff_report.json` - 完整变更数据
- 两个版本的游戏文件夹源代码

**操作步骤**：

1. **读取初步报告**
   - 理解检测到的变更系统和文件列表
   - 识别需要深度分析的关键文件

2. **读取实际源代码**
   - 对每个关键变更文件，读取旧版本和新版本的实际内容
   - 进行逐行对比，理解代码逻辑变化

3. **深度解读要点**

   对于每个显著变更，需要回答：
   - **这是什么**：用通俗语言解释代码变更的内容
   - **为什么改**：推测 PDS 此次修改的目的
   - **影响什么**：分析对玩家游戏体验的实际影响
   - **如何应对**：如果是nerf/buff，玩家如何调整策略

4. **输出最终报告**
   - 生成 `极详细对比分析报告.md` 作为最终结果
   - 格式要求见下方"深度解读报告模板"

**深度解读报告模板**：

```markdown
# Crusader Kings III 版本 X vs Y 极详细对比分析报告

## 版本基本信息

- **游戏分支**
  - X.Y.Z: [分支名]
  - X.Y.Z: [分支名]

- **游戏提交**
  - X.Y.Z: [提交哈希]
  - X.Y.Z: [提交哈希]

- **引擎分支**
  - X.Y.Z: [分支名]
  - X.Y.Z: [分支名]

- **引擎提交**
  - X.Y.Z: [提交哈希]
  - X.Y.Z: [提交哈希]

---

## 一、整体差异统计总览

- **新增文件**: N 个（仅存在于新版本的文件）
- **删除文件**: N 个（仅存在于旧版本的文件）
- **修改文件**: N 个（两版本都存在但内容/大小不同）
- **未变化文件**: N 个（两版本完全相同）
- **文件总数**: M → N，净[增加/减少/变化] K 个文件

---

## 执行摘要

[用3-5句话概括本次更新的核心内容和对玩家的影响]

## 重大变更详解

### 1. [变更名称] ⚠️

**文件**: `path/to/file.txt`

**代码对比**:
```
旧版本代码片段
```
→
```
新版本代码片段
```

**通俗解释**:
[用非程序员也能理解的语言解释这段代码在做什么]

**游戏性影响**:
- **对谁影响大**: [例如：日本玩家、喜欢纳妾的玩家等]
- **实际影响**: [具体说明数值/机制变化]
- **建议应对**: [玩家应该如何调整策略]

**关联变更**:
- 此变更与 `其他文件` 的变更相关联，共同构成了 [某个系统] 的调整

## 次要变更

### 2. [变更名称]

[同上格式，但简化描述]

## 总结与建议

### 强势玩法
- [列出本次更新后可能变强的策略/玩法]

### 需要调整
- [列出需要改变玩法的内容]

### 待观察
- [需要实际测试才能确定影响的内容]
```

### Phase 7: B站专栏版生成

- **必选输出**
- 所有表格语法转换为列表格式
- 适配 B站专栏不支持表格的特性

## Output Files

所有输出默认保存到 `diff_output/` 目录：

### 初步分析（ck3_analyzer.py 自动生成）
- `初步分析报告.md` (~100+ KB) - **初步分析报告**（含代码片段）
- `diff_report.json` (~28 MB) - 完整 JSON 数据（包含深度diff）
- `diff_report.csv` (~7 MB) - CSV 表格格式

### 最终报告（LLM深度解读后生成）
- `极详细对比分析报告.md` (~50-5000 KB) - **最终深度分析报告**
- `极详细对比分析报告_B站专栏版.md` (~50-5000 KB) - **最终深度分析报告** B站专栏版，纯粹把【极详细对比分析报告.md】中的所有表格语法转换为列表格式，其他与【极详细对比分析报告.md】完全保持一致。

## 深度分析示例

### 示例：继承法变更

```
### 2.1 继承法改革 (Title Succession Laws) ⚠️ 重要

**版本信息**:
- **游戏分支**: 1.18.4 vs 1.19.0
- **游戏提交**: 6f57f9eb... vs 2753ca40...
- **引擎分支**: titus/release/1.18.2 vs titus/release/1.19.0
- **引擎提交**: 72b717fb... vs f2255972...

**差异统计**: +583/-207/~3789 文件

**影响文件**:
- game/history/titles/e_japan.txt
- game/history/titles/00_other_titles.txt

**变更类型**: 重大游戏机制变更

**核心变更代码**:

旧版本 (e_japan.txt):
```pdx
866.1.1 = { holder = japanese_kiyohara_22 }
```

新版本:
```pdx
866.1.1 = {
    holder = japanese_kiyohara_22
    add_title_law = single_heir_succession_law
}
```

**00_other_titles.txt 变更**:
```pdx
# 新增逻辑 - 行政制→封建制转换时的继承法处理
if = {
    limit = {
        exists = holder
        holder = { has_government = administrative_government }
    }
    change_government = feudal_government
    if = {
        limit = { NOT = { has_realm_law = single_heir_succession_law } }
        add_realm_law_skip_effects = single_heir_succession_law
    }
}
```

**游戏性影响**:
- 日本帝国现在默认拥有 `single_heir_succession_law`
- 行政制→封建制转换时自动添加单一继承人继承法
- 这意味着日本在867年后强制执行单一继承人制度
- **历史准确性**: 平安时代日本确实有相对集中的继承制度
```

## Requirements

- Python 3.6+ (ck3_analyzer.py)
-两个月版本 CK3 游戏文件夹
- 足够的磁盘空间（深度分析需要额外存储diff数据）
- 大语言模型（用于 Phase 6 的深度解读）

## Notes

- 脚本会自动跳过 `.idea` 目录
- 二进制文件使用大小比较，文本文件使用 MD5 哈希和行数统计
- 行数统计只对文本文件有效，二进制文件行数为0
- 系统检测基于路径关键词，支持任何 CK3 版本
- B站专栏版会移除所有表格语法，改用列表格式
- 深度分析默认分析所有文件，可通过 `--max-deep-files` 限制
- 使用 `--no-deep-analysis` 可跳过耗时的深度分析
- **重要**: Phase 6 需要人工触发大模型进行深度解读