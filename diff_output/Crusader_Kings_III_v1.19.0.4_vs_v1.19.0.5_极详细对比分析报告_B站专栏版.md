# Crusader Kings III 版本 1.19.0.4 vs 1.19.0.5 极详细对比分析报告

## 版本基本信息

- **游戏分支**
  - 1.19.0.4: release/1.19.0
  - 1.19.0.5: release/1.19.0

- **游戏提交**
  - 1.19.0.4: 2753ca4000401afbe17ad1c6cfeeb0acd0d927c1
  - 1.19.0.5: b4d50bd6ed562ef00fd6a35a6ed38a9483d224be

- **引擎分支**
  - 1.19.0.4: titus/release/1.19.0
  - 1.19.0.5: titus/release/1.19.0

- **引擎提交**
  - 1.19.0.4: f22559721a07e0156b809de8da35ffdc78a47d15
  - 1.19.0.5: f22559721a07e0156b809de8da35ffdc78a47d15

---

## 一、整体差异统计总览

- **新增文件**: 1 个（仅存在于 1.19.0.5 的文件）— 启动器安装程序更新: launcher-installer-windows_2026.4.3.exe
- **删除文件**: 1 个（仅存在于 1.19.0.4 的文件）— 旧版启动器安装程序: launcher-installer-windows_2026.4.1.exe
- **修改文件**: 48 个（两版本都存在但内容/大小不同）
- **未变化文件**: 49561 个（两版本完全相同）
- **文件总数**: 49610 → 49610，净变化 0 个文件
- **二进制变更**: ck3.exe 大小增加 2,560 字节（约 0.0027%）

### 变化系统概览

共检测到 **6** 个显著变化的系统（按综合评分排序）：

- **localization**: 30 个文件, 50 行变化 (0.2%) — 多语言本地化同步更新
- **events**: 14 个文件, 83 行变化 (0.2%) — 狩猎事件、妊娠事件、El Cid故事循环调整
- **interactions**: 11 个文件, 54 行变化 (0.2%) — 购买土地互动、婚姻互动调整
- **binary**: 5 个文件, 0 行变化 — 可执行文件、校验和更新
- **character**: 3 个文件, 45 行变化 (0.2%) — 角色相关代码微调
- **⚠️ title**: 3 个文件, 44 行变化 (0.4%) — 继承法、头衔系统调整

---

## 执行摘要

1.19.0.5 是一个针对 1.19.0 (Roads to Power / 权力之路) 的**小版本热修复补丁**，核心变更围绕**东罗马（拜占庭）继承法清理**、**日本政体从封建制正式迁移至行政制**、**Legacy of the Abbasid (FP3) 购买土地机制的完整控制检查增强**以及**El Cid 故事循环的作用域重构**。此外还包含了多项本地化翻译更新、UI 多人游戏可见性修复以及狩猎事件的神秘动物故事功能增强。这些变更整体偏向于**代码架构清理和bug修复**，对大多数玩家的实际游戏体验影响有限，但对**拜占庭玩家**、**日本玩家**和**使用购买土地互动**的玩家有直接实质性影响。

---

## 重大变更详解

### 1. 拜占庭帝国单一继承人继承法移除 ⚠️

**文件**: `game/common/laws/00_succession_laws.txt`

**代码对比**:

旧版本中被删除的逻辑：
```pdx
can_title_have = {
    this = title:e_byzantium
    OR {
        can_have_single_heir_succession_law_trigger = yes
        historical_succession_access_single_heir_succession_law_trigger = yes
    }
}
```

新版本中替换为：
```pdx
can_have_single_heir_succession_law_trigger = yes
```

**通俗解释**:
拜占庭帝国（e_byzantium）之前有特例，允许通过"历史继承访问"触发器绕过某些限制来获得单一继承人继承法。此次更新移除了这个特例，让拜占庭与其他所有头衔一样，统一通过标准的 `can_have_single_heir_succession_law_trigger` 判断是否能拥有单一继承人继承法。

**游戏性影响**:
- **对谁影响大**: 拜占庭玩家、罗马帝国重建者
- **实际影响**: 拜占庭帝国不再自动有资格直接获得单一继承人继承法。这意味着拜占庭皇帝可能需要先满足其他条件才能获得长子继承。对于非 Roads to Power DLC 玩家，这意味着拜占庭将更容易保持分割继承制。
- **建议应对**: 如果需要单一继承人继承法，需要通过文化创新、法律改革或特定决议来解锁，不再有拜占庭特赦通道。

**关联变更**:
- 此变更是《权力之路》大版本中行政制继承法重构的后续清理工作。

---

### 2. 日本政体从封建/书签依赖重构为正式行政制 ⚠️

**涉及文件**:
- `game/history/titles/00_other_titles.txt` (167 行净变化 — 重排历史持有者数据)
- `game/history/titles/e_japan.txt` (11 行删除, 2 行新增)
- `game/common/on_action/game_start.txt` (46 行删除, 2 行新增)

**代码对比 — e_japan.txt**:

旧版本：
```pdx
# Feudal + primogeniture-style title succession for bookmark load when TGP/AuH is off or incomplete.
# All Under Heaven: on_game_start upgrades the Kampaku back to Ritsuryō + regency realm law.
government = feudal_government
succession_laws = { single_heir_succession_law }
```

新版本：
```pdx
government = japan_administrative_government
```

**代码对比 — game_start.txt**：

旧版本中被删除的大段逻辑：
- 检查 `has_dlc_feature = all_under_heaven` 来决定是否设置日本行政政府
- 在 `game_start` 中动态决定日本天皇/关白的政体
- 处理 AuH DLC 开启/关闭的不同路径

新版本：
- 移除了所有 AuH 条件判断
- 将 BLOCS 设置统一前置到 `noble_family_title_realm_setup` 之前
- 始终执行 `tgp_setup_historical_house_bloc_effect = yes`

**代码对比 — 00_other_titles.txt**（拜占庭历史数据重构）：

旧版本中，866.9.24 时间点（巴西尔一世登基）有大段条件逻辑：
```pdx
holder = 1700
    if = { # 检查 RtP DLC
        limit = { ... }
        change_government = administrative_government
        add_title_law = acclamation_succession_law
        set_state_faith = faith:orthodox
    }
    else = { # 无 RtP DLC
        change_government = feudal_government
        add_realm_law_skip_effects = single_heir_succession_law
        if = { has_title_law = acclamation_succession_law }
            remove_title_law = acclamation_succession_law
        add_title_law = single_heir_succession_law
    }
```

新版本中替换为：
```pdx
866.1.1 = {
    government = administrative_government
    succession_laws = { acclamation_succession_law }
}
# 后来在 866.9.24 或之后：
if = { limit = { exists = holder } }
    set_state_faith = faith:orthodox
if = { limit = { exists = holder NOT = { has_dlc_feature = roads_to_power } } }
    holder = { change_government = feudal_government add_realm_law_skip_effects = single_heir_succession_law }
```

**通俗解释**:
这是一次重大的历史数据重构。旧版本中，日本帝国在游戏启动时从封建制起步，然后根据是否安装 All Under Heaven DLC，由 `on_game_start` 事件动态决定是否升级为行政制。新版本中，日本天皇/关白直接默认使用日本行政政府（japan_administrative_government）。

同时，拜占庭帝国的历史启动数据也被重构：之前 866 年巴西尔一世登基时的条件判断逻辑被移到游戏启动时处理，历史文件中不再包含 DLC 条件检查。

**游戏性影响**:
- **对谁影响大**: 日本玩家、拥有 RtP 的拜占庭玩家
- **实际影响**:
  1. **日本**: 现在从 867 年开局就直接是日本行政制，不再需要 AuH DLC 来激活。这对于没有 AuH DLC 的玩家变化最大——日本现在始终以行政制运作，继承法也更清晰。
  2. **拜占庭**: 历史数据中的条件逻辑被清理，启动时的 DLC 检测后移到 `on_action` 中处理。减少了历史加载时的逻辑复杂度。
  3. **BLOCS 系统**: 贵族家族设置现在统一在所有情况下执行，不再区分是否启用 AuH。
- **建议应对**: 日本玩家需要注意新的继承规则——行政制的继承方式与封建制完全不同。没有"权力之路"DLC 的玩家拥有拜占庭领土时，现在会直接转为封建制。

**关联变更**:
- 此变更与拜占庭继承法调整（变更1）协同工作，共同简化了启动时的政体/继承法设置逻辑。

---

### 3. 复兴哈里发家族征服 CB 绕过行政限制 ⚠️

**文件**: `game/common/casus_belli_types/00_subjugation.txt`

**代码对比**:

旧版本：
```pdx
government_allows = administrative
```

新版本：
```pdx
AND = { # FP3: Renewed Caliphate houses with subjugations_expanded bypass the admin restriction
    government_allows = administrative
    NOT = {
        house ?= {
            has_variable = subjugations_expanded
        }
    }
}
```

**通俗解释**:
之前行政制政府完全不能使用征服 CB。现在，"复兴哈里发"（FP3 / Legacy of the Abbasid 内容包）的子嗣家族如果拥有 `subjugations_expanded` 变量，就能够绕过行政限制使用征服 CB。

**游戏性影响**:
- **对谁影响大**: 阿巴斯复兴王朝玩家、行政制下的穆斯林统治者
- **实际影响**: 复兴哈里发路线的玩家现在即使采用行政制政府，仍然可以使用征服 CB 进行领土扩张。这与此前的设计（行政制禁止征服）形成对比。
- **建议应对**: 选择复兴哈里发路线时，可以更放心地转为行政制——不会因此失去征服能力。

---

### 4. 购买土地互动增强（完整控制检查 + 附庸处理） ⚠️

**涉及文件**:
- `game/common/character_interactions/06_ep3_laamp_interactions.txt` (+54/-12 行)
- `game/common/scripted_effects/07_dlc_ep3_scripted_effects.txt` (+44/-17 行)
- `game/common/trigger_localization/08_ep3_laamp_triggers.txt` (+6 行)

**代码对比**:

旧版本中，购买土地的成本计算和附庸处理简单直接：
```
every_in_list = { list = purchased_titles }
    if = { limit = { tier = tier_county } add = purchase_land_county_cost_value }
    else_if = { limit = { tier = tier_duchy } add = purchase_land_duchy_cost_value }
```

新版本中，增加了完整的控制检查层：
```pdx
custom_tooltip = {
    text = PURCHASE_LAND_COMPLETE_CONTROL_TT
    trigger_if = {
        limit = { scope:target = { tier = tier_duchy } }
        scope:recipient = { completely_controls = scope:target }
    }
}
```

对于附庸级别低于购买目标等级的持有者，不再直接添加到 purchased_titles，而是：
- 将低级持有者记录到 `purchase_land_vassals_taken` 列表
- 在 `07_dlc_ep3_scripted_effects.txt` 中新增专门逻辑处理这些附庸的领主权变更
- 增加了 `scope:ascended_throne_value = flag:purchased` 和 `$REASON$ = flag:purchased` 检查

**通俗解释**:
购买土地互动（Legacy of the Abbasid 内容包的功能）现在增加了几个重要改进：
1. **完整控制检查**: 如果目标是一个公爵领，卖方必须完全控制该公爵领的所有法理伯爵领才能出售。
2. **附庸流转**: 如果目标土地的持有者等级低于买方，这些持有者会被追加为买方的附庸，而不是被直接吞并。
3. **王座购买检测**: 区分"正常购买"和"王座购买"两种场景，避免已购买的王座再次触发附庸转移。

**游戏性影响**:
- **对谁影响大**: 使用 FP3 购买土地系统的玩家
- **实际影响**: 购买公爵领的成本更合理——现在会考虑买方对每个法理伯爵领的控制权。附庸在领土买卖后的归属更符合直觉。
- **建议应对**: 购买公爵领之前，确保卖方完全控制所有法理伯爵领，否则交易可能被阻止。

---

### 5. El Cid 故事循环作用域重构

**文件**: `game/events/story_cycles/ep3_story_cycle_el_cid.txt` (+44/-28 行)
**辅助文件**: `game/common/story_cycles/ep3_story_cycle_el_cid.txt` (+1 行)

**代码对比**:

旧版本中，所有变量操作直接使用：
```pdx
change_variable = { name = cid_loyalty_counter add = 1 }
root.var:cid_liege
```

新版本中，改为作用域限定：
```pdx
scope:story = {
    change_variable = { name = cid_loyalty_counter add = 1 }
}
holder = scope:story.var:cid_liege
```

**通俗解释**:
El Cid 故事循环中所有变量操作从全局作用域迁移到 `scope:story` 作用域中。这是一个代码架构清理，确保故事状态与特定故事实例绑定，而不是全局共享。

**游戏性影响**:
- **影响很小**: 对玩家来说，El Cid 故事应该表现得和之前一样。主要是防止了当多个 El Cid 故事同时运行时可能发生的变量冲突。
- 对于有多条故事线同时在进行的玩家，这个修复能防止变量互相污染。

---

### 6. 狩猎神秘动物故事 — 玩家触发机制增强

**文件**: `game/events/activities/hunt_activity/hunt_events.txt` (+14 行)

**新增逻辑**:
```pdx
if = {
    limit = {
        this = scope:host
        is_ai = no
        NOT = { has_character_flag = had_mystical_animal_story }
        NOT = { any_owned_story = { type = story_cycle_hunt_mystical_animal } }
        exists = scope:activity.var:animal_type
    }
    set_variable = {
        name = animal_type
        value = scope:activity.var:animal_type
    }
    start_hunt_mystical_animal_story_cycle_effect = yes
}
```

**通俗解释**:
当玩家角色（非 AI）主持狩猎活动、遇到神秘动物时，现在会触发一条专属的故事循环。之前这个触发机制可能只对 AI 角色有效。

**游戏性影响**:
- **对谁影响大**: 喜欢狩猎活动的玩家
- **实际影响**: 玩家现在在狩猎中遇到神秘动物（如白鹿、独角兽等）时，会进入一条完整的叙事线，而不仅仅是得到一个事件弹窗。
- **建议应对**: 如果你想体验神秘动物故事，多举办狩猎活动！

---

### 7. 伊比利亚斗争决策 Bug 修复

**文件**: `game/common/decisions/dlc_decisions/03_fp2_decisions.txt` (+1 行)

**新增代码**:
```pdx
exists = struggle:iberian_struggle
```

**通俗解释**:
Fate of Iberia (FP2) 内容包的某个决策现在会先检查"伊比利亚斗争"是否存在，避免在斗争已经结束后仍然显示或执行该决策。

**游戏性影响**:
- 修复了一个罕见 bug：在伊比利亚斗争结束后，相关决策可能仍然可用。

---

### 8. 妊娠事件修复 — consort 列表检查

**文件**: `game/events/pregnancy_events.txt` (+1 行)

**新增代码**:
```pdx
any_consort = { } # count = all returns true if list is empty!
```

**通俗解释**:
在妊娠事件中，对 consort（侍妾）列表的检查之前存在一个逻辑 bug：如果列表为空，`count = all` 会返回 true。新增的 `any_consort` 检查先确保列表非空才开始后续判断。

**游戏性影响**:
- 修复了一个潜在 bug：无侍妾的角色在某些情况下可能错误触发与侍妾相关的妊娠事件。

---

### 9. UI — 多人游戏大厅可见性修复

**文件**: `game/gui/window_character.gui` (+2/-2 行)

**代码对比**:

旧版本：
```pdx
visible = "[Not( And( GameIsMultiplayer, IsPreparationLobby ) )]"
```

新版本：
```pdx
visible = "[Or( HasGameStartedForTheFirstTime, Not( And( GameIsMultiplayer, IsPreparationLobby ) ) )]"
```

**通俗解释**:
角色窗口中的某些元素（如皇家宫廷按钮）在多人游戏准备大厅被隐藏了。新版本增加了 `HasGameStartedForTheFirstTime` 检查——如果是已经开始过的游戏，即使在多人模式下也正常显示。

**游戏性影响**:
- **对谁影响大**: 多人游戏玩家
- **实际影响**: 修复了多人游戏中重新加载存档后某些 UI 元素不显示的问题。

---

### 10. 婚姻互动 — 妾室数量限制移除

**文件**: `game/common/character_interactions/00_marriage_interactions.txt` (-3 行)

**删除逻辑**:
```pdx
scope:actor = {
    allowed_more_concubines = yes
}
```

**通俗解释**:
在婚姻互动中，之前检查了角色是否"允许更多妾室"。这个条件现在被移除了。

**游戏性影响**:
- **对谁影响大**: 使用妾室机制的玩家（特定文化/宗教）
- **实际影响**: 婚姻互动不再受"是否允许更多妾室"条件限制。这可能是为了让互动更简洁，或者在当前版本中该检查已经被集中管理。
- **建议应对**: 无需特殊应对，如果之前被此条件限制的互动现在可用，属于合理变更。

---

### 11. 神明临凡 — 新技能等级 "Godlike"

**涉及文件**:
- `game/common/defines/00_defines.txt` (+2 行)
- 所有 10 种语言的 `core_l_*.yml` 文件（各 +1 行）

**新增内容**:
```
99 #godlike
"SKILL_GODLIKE"
```

**翻译对照**:
- **English**: Godlike
- **简体中文**: 神明临凡
- **French**: Divinité
- **German**: Gottgleich
- **Japanese**: 神格者
- **Korean**: 화신 (化身)
- **Polish**: Postać nadludzka
- **Russian**: Подобие бога
- **Spanish**: (同步更新)

**通俗解释**:
PDS 在 defines 中新增了一个值为 99 的技能等级 "Godlike"（神明临凡），这超过了当前最高的 "Legendary"（传奇）等级（推测为 60-70 左右）。

**游戏性影响**:
- 目前还没有发现直接使用该等级的游戏机制。可能是为未来内容/DLC 预留的更高技能等级。
- 如果这个等级实装，意味着未来角色可以在某项技能上达到比"传奇"更高的层级，带来更强大的加成。

---

### 12. 启动器更新

**变更**:
- 删除: `launcher\launcher-installer-windows_2026.4.1.exe`
- 新增: `launcher\launcher-installer-windows_2026.4.3.exe`
- 修改: `launcher\launcher-settings.json`

**影响**:
- 标准启动器更新，从 2026.4.1 升级到 2026.4.3，包含启动器层面的 bug 修复和改进。
- **对游戏性无影响**。

---

## 次要变更

### bp2 决策退款机制调整

**文件**: `game/events/dlc/bp2/bp2_decision_events.txt` (+2/-44 行)

旧版本中，退出 rites_of_passage 决策会退款金币和威望，且不移除决策冷却。新版本改为"不退款的押金"制度——退出决策不会退款，但会触发决策冷却。

本地化中新增了警示文案：
```
@alert_icon! #alert_trial You will not be refunded the cost of this decision!
```
（各语言同步翻译）

**游戏性影响**: 这是一个 nerf（削弱）。选择"rite of passage"决策现在如果中途退出，不会得到退款。玩家需要更谨慎地决定是否开始该决策。

---

## 本地化更新（全部 10 种语言）

本次更新覆盖了所有 10 种支持语言的同步本地化：

- **SKILL_GODLIKE**: 新技能等级名称
- **PURCHASE_LAND_COMPLETE_CONTROL_TT**: 购买土地完整控制提示
- **bp2_decision.0002.tt**: BP2 决策退款政策提示

**涉及语言**: 英语、法语、德语、西班牙语、俄语、波兰语、简体中文、日语、韩语（巴西葡萄牙语未变化？）

---

## 变更类型分布

- **major** (核心游戏机制): 6 个文件
- **bugfix** (Bug修复): 1 个文件
- **balance** (平衡性): 2 个文件
- **feature** (功能): 3 个文件
- **localization** (本地化): 31 个文件
- **gui** (界面): 1 个文件

---

## 总结与建议

### 强势玩法
- **阿巴斯复兴哈里发**: 现在即使走行政制也能使用征服 CB，扩张路线更灵活。
- **日本行政制**: 不再依赖 AuH DLC，867 开局直接体验日本行政制，继承规则更明确。
- **狩猎爱好者**: 神秘动物故事对玩家角色可用，新增沉浸式叙事体验。

### 需要调整
- **拜占庭继承**: 单一继承人继承法不再有拜占庭特赦通道，需要走常规解锁路径。
- **Rite of Passage 决策**: 退出不再退款，需要更谨慎地选择。
- **购买土地**: 完整控制检查意味着公爵领购买前需要卖方清理法理领土的控制权。

### 待观察
- **Godlike 技能等级**: 值为 99 但暂时没有被任何游戏机制引用。可能是为未来的 DLC 内容预留。
- **El Cid 重构**: scope:story 作用域重构是架构层面的改进，对玩家的实际影响需要游戏内验证。
- **拜占庭/日本历史数据清理**: 减少了 DLC 条件依赖，理论上提高了 mod 兼容性，但具体效果需要观察。

---

## 附录

### 修改文件完整列表（47 个深度分析文件）

**核心机制变更**:
1. `game/common/casus_belli_types/00_subjugation.txt` — 复兴哈里发征服 CB
2. `game/common/laws/00_succession_laws.txt` — 拜占庭继承法
3. `game/common/on_action/game_start.txt` — 启动逻辑重构
4. `game/common/scripted_effects/07_dlc_ep3_scripted_effects.txt` — 购买土地附属效果
5. `game/history/titles/00_other_titles.txt` — 历史数据重构
6. `game/history/titles/e_japan.txt` — 日本政体变更

**Bug修复**:
7. `game/common/decisions/dlc_decisions/03_fp2_decisions.txt` — 伊比利亚斗争检查

**平衡性**:
8. `game/common/character_interactions/00_marriage_interactions.txt` — 妾室条件移除
9. `game/common/character_interactions/06_ep3_laamp_interactions.txt` — 土地购买增强

**功能**:
10. `game/events/activities/hunt_activity/hunt_events.txt` — 神秘动物故事
11. `game/events/dlc/bp2/bp2_decision_events.txt` — 决策退款机制
12. `game/events/pregnancy_events.txt` — 妊娠修复

**界面**:
13. `game/gui/window_character.gui` — 多人大厅可见性

**常量**:
14. `game/common/defines/00_defines.txt` — Godlike 技能等级
15. `game/common/story_cycles/ep3_story_cycle_el_cid.txt` — El Cid 作用域
16. `game/common/trigger_localization/08_ep3_laamp_triggers.txt` — 触发本地化
17. `game/events/story_cycles/ep3_story_cycle_el_cid.txt` — 故事循环事件
18. `binaries/checksum.txt` — 校验和更新
19. `launcher/launcher-settings.json` — 启动器配置

**本地化 (31 个文件、10 种语言)**:
20-49. `game/localization/*/core_l_*.yml` — SKILL_GODLIKE 翻译
50-79. `game/localization/*/dlc/ep3/ep3_interactions_l_*.yml` — PURCHASE_LAND 翻译
80-109. `game/localization/*/event_localization/relation_events/wet_nurse_events_l_*.yml` — bp2 退款文案

---

- **报告生成时间**: 2026-05-09 01:27:26 + LLM深度解读
- **分析模型**: CK3 Version Analyzer + DeepSeek/big-pickle 深度解读
- **协作人**: XenoAmess
- **深度分析文件数**: 47
