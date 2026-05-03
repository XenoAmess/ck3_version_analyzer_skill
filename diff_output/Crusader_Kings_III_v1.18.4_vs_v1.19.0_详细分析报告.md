# Crusader Kings III 版本 1.18.4 vs 1.19.0 详细对比分析报告

## 版本信息

| 项目 | 1.18.4 | 1.19.0 |
|------|--------|--------|
| Titus Branch | release/1.18.4 | release/1.19.0 |
| Titus Commit | 6f57f9eb07db28b40185274899544bb29b3e579f | 2753ca4000401afbe17ad1c6cfeeb0acd0d927c1 |
| Clausewitz Branch | titus/release/1.18.2 | titus/release/1.19.0 |
| Clausewitz Commit | 72b717fb89c6be4439541b07c480f8d6ec050f0d | f22559721a07e0156b809de8da35ffdc78a47d15 |

---

## 一、总体差异统计

| 类别 | 数量 | 说明 |
|------|------|------|
| **新增文件** | 583 | 1.19.0 中有而 1.18.4 中没有的文件 |
| **删除文件** | 207 | 1.18.4 中有而 1.19.0 中没有的文件 |
| **修改文件** | 3,789 | 两版本中都存在但内容/大小不同的文件 |
| **未变化文件** | 45,238 | 两版本中完全相同的文件 |

**文件总数**: 1.18.4 = 49,234 个 | 1.19.0 = 49,610 个

---

## 二、宗教系统重构 ( Religion System Restructuring )

### 2.1 目录结构重大变化

**旧结构 (1.18.4):**
```
game\common\religion\
├── doctrines\
│   ├── 10_doctrines_religions.txt
│   ├── 20_doctrines.txt
│   ├── 20_doctrines_islam.txt
│   ├── 20_doctrines_judaism.txt
│   ├── 20_doctrines_zoroastrianism.txt
│   ├── 30_core_tenets.txt
│   ├── 40_doctrines_special.txt
│   └── _doctrines.info
├── fervor_modifiers\
│   └── 00_fervor_modifiers.txt
└── ...
```

**新结构 (1.19.0):**
```
game\common\religion\
├── doctrine_types\
│   ├── 10_doctrines_religions.txt
│   ├── 20_doctrines.txt
│   ├── 20_doctrines_islam.txt
│   ├── 20_doctrines_judaism.txt
│   ├── 20_doctrines_zoroastrianism.txt
│   ├── 30_core_tenets.txt
│   ├── 40_doctrines_special.txt
│   └── _doctrine_types.info
├── doctrine_group_types\
│   ├── 00_doctrine_group_types.txt
│   └── _doctrine_group_types.info
├── holy_site_types\
│   ├── 00_holy_site_types.txt
│   └── _holy_site_types.info
├── religion_family_types\
│   ├── 00_religion_family_types.txt
│   └── _religion_family_types.info
├── religion_types\
│   ├── 00_akom.txt
│   ├── 00_aluk.txt
│   ├── 00_baltic.txt
│   ├── 00_basque_paganism.txt
│   ├── 00_buddhism.txt
│   ├── 00_christianity.txt
│   ├── 00_islam.txt
│   ├── ... (共 51 个宗教定义文件)
│   └── _religion_types.info
└── ...
```

### 2.2 核心变化分析

#### 2.2.1 Doctrine Group Types (教条分组类型)

新增文件: `doctrine_group_types/00_doctrine_group_types.txt`

这是 1.19.0 中的新概念，将教条按功能分组：

```yaml
doctrine_marriage_type = {
    category = "marriage"
    doctrine_types = {
        doctrine_monogamy
        doctrine_polygamy
        doctrine_concubines
    }
}

doctrine_divorce = {
    category = "marriage"
    doctrine_types = {
        doctrine_divorce_disallowed
        doctrine_divorce_approval
        doctrine_divorce_allowed
    }
}

doctrine_homosexuality = {
    category = "crimes"
    doctrine_types = {
        doctrine_homosexuality_crime
        doctrine_homosexuality_shunned
        doctrine_homosexuality_accepted
    }
}
```

**影响**: 这种分组结构使得宗教教条系统更加模块化，便于管理和发展。

#### 2.2.2 Religion Types (宗教类型)

每个宗教现在有独立的定义文件 (`religion_types/00_*.txt`)，例如 `00_christianity.txt`:

```yaml
christianity_religion = {
    family = rf_abrahamic
    doctrine_background_icon = core_tenet_banner_christian.dds
    doctrine = abrahamic_hostility_doctrine

    # 主教条
    doctrine = doctrine_monotheist
    doctrine = doctrine_spiritual_head
    doctrine = doctrine_gender_male_dominated
    doctrine = doctrine_pluralism_righteous
    doctrine = doctrine_theocracy_temporal

    # 婚姻相关
    doctrine = doctrine_monogamy
    doctrine = doctrine_divorce_approval
    # ...
}
```

**新增宗教类型** (共 51 个):
- `00_buddhism.txt` (佛教)
- `00_hinduism.txt` (印度教)
- `00_islam.txt` (伊斯兰教)
- `00_judaism.txt` (犹太教)
- `00_zoroastrianism.txt` (祆教)
- 以及多种地方性宗教 (baltic, germanic, slavic, shinto, tengrism 等)

#### 2.2.3 Holy Site Types (圣地类型)

新增文件: `holy_site_types/00_holy_site_types.txt` (3,542 行)

为不同宗教定义了圣地系统：

```yaml
# 基督教圣地
jerusalem = {
    county = c_jerusalem
    character_modifier = {
        monthly_piety_gain_mult = 0.2
    }
    parameters = {
        jerusalem_conversion_bonus
    }
}

rome = {
    county = c_roma
    barony = b_vaticano
    character_modifier = {
        name = holy_site_rome_effect_name
        development_growth_factor = 0.1
        stewardship = 1
    }
}

cologne = {
    county = c_cologne
    character_modifier = {
        name = holy_site_cologne_effect_name
        cultural_head_fascination_mult = 0.05
        monthly_county_control_growth_factor = 0.05
    }
}
```

**影响**: 圣地系统现在更加规范，不同宗教有不同的圣地和效果。

---

## 三、用户界面 (UI) 系统变化

### 3.1 PDX Account 系统 (新增)

新增登录/账户管理系统，包括以下文件：

| 文件路径 | 大小 | 说明 |
|----------|------|------|
| `game/gui/pdx_account/base_types.gui` | 7.51 KB | 基础 UI 样式模板 |
| `game/gui/pdx_account/login_window.gui` | 14.11 KB | 登录窗口 |
| `game/gui/pdx_account/create_account_window.gui` | 106.00 B | 创建账户窗口 |
| `game/gui/pdx_account/legal_docs_viewer.gui` | 1.35 KB | 法律文档查看器 |
| `jomini/gui/pdx_account/base_types.gui` | 9.70 KB | Jomini 基础样式 |
| `jomini/gui/pdx_account/login_window.gui` | 9.54 KB | Jomini 登录窗口 |
| `jomini/gui/pdx_account/create_account_window.gui` | 5.87 KB | Jomini 创建账户 |
| `jomini/gui/pdx_account/create_social_profile_window.gui` | 90.00 B | 社交资料创建 |
| `jomini/gui/pdx_account/legal_docs_viewer.gui` | 1.22 KB | 法律文档查看器 |

**UI 样式系统示例** (`base_types.gui`):
```gui
template SDKTextStyle
{
    using = Font_Type_Standard
    using = Font_Size_Small
    align = left
    default_format = "#medium"
}

template SDKButtonStyle
{
    texture = "gfx/editor_gui/editor_button.dds"
    gfxtype = framedbuttongfx
    spriteType = CorneredStretched
    spriteborder = { 4 4 }
    effectname = "NoHighlight"
    framesize = { 16 16 }
    upframe = 1
    downframe = 2
    overframe = 3
    disableframe = 4
    intersectionmask = yes
}
```

**影响**: 玩家现在可以通过 PDX 账户系统登录游戏，可能与云存档或多人游戏功能相关。

### 3.2 Ledger 窗口 (新增大规模 UI)

新增文件: `game/gui/window_ledger.gui` (246.31 KB)

这是一个非常庞大的 UI 系统，用于显示游戏的各种统计信息。

```gui
window = {
    name = "ledger_window"
    widgetid = "ledger_window"
    parentanchor = top|right
    position = { -50 65 }
    allow_outside = yes
    layer = middle
    size = { 745 89% }

    state = {
        name = _show
        using = Animation_FadeIn_Quick
    }

    state = {
        name = _hide
        using = Animation_FadeOut_Quick
    }
}
```

**功能**: 分类账/总账界面，用于查看:
- 地块/爵位信息
- 文化传播信息
- 军事信息
- 经济数据等

### 3.3 Accolade 系统 (骑士徽章系统)

新增大量骑士徽章相关资源：

| 类型 | 数量 | 说明 |
|------|------|------|
| 骑士徽章图标 | 48+ | 不同颜色/类型的 accolade 图标 |
| 徽章框架 | 2 | accolade_frame.dds, accolades_frames_background.dds |
| 扁平图标 | 38+ | flat_icons/*.dds |

新增文件:
- `game/gui/window_accolade_attribute_selection.gui` (4.02 KB)
- `game/interface/icons/knight_badge/frame/accolade_frame.dds`
- `game/interface/icons/knight_badge/icons/accolade_trait_*.dds`

**影响**: 骑士系统得到了显著扩展，徽章系统允许玩家更个性化地定制骑士。

---

## 四、本地化 (Localization) 变化

### 4.1 新增本地化文件统计

| 语言 | 新增文件数 | 主要内容 |
|------|------------|----------|
| 英语 (english) | 12 | ledger, court_visuals, debug_story, elder_events, knight_permissions |
| 法语 (french) | 12 | 同上 |
| 德语 (german) | 12 | 同上 |
| 日语 (japanese) | 12 | 同上 |
| 韩语 (korean) | 12 | 同上 |
| 波兰语 (polish) | 12 | 同上 |
| 俄语 (russian) | 12 | 同上 |
| 简体中文 (simp_chinese) | 12 | 同上 |
| 西班牙语 (spanish) | 12 | 同上 |

**新增本地化目录结构**:
```
game/localization/{language}/
├── ledger/
│   ├── ledger_filtersorts_l_{language}.yml
│   └── ledger_l_{language}.yml
├── court_visuals_l_{language}.yml
├── debug_story_test_event_l_{language}.yml
├── dlc/tgp/tgp_travel_danger_events_l_{language}.yml
├── elder_events_l_{language}.yml
├── event_localization/
│   ├── activities/hunt_events_anna_l_{language}.yml
│   ├── lifestyle/guile/intrigue_events_bjorn_l_{language}.yml
│   ├── story_cycles/story_cycles_l_{language}.yml
│   └── travel_events/travel_events_bjorn_l_{language}.yml
├── knight_permissions_l_{language}.yml
└── religion/holy_sites_l_{language}.yml
```

### 4.2 新增文本内容示例

**Court Visuals 本地化** (英文):
```yaml
l_english:
  COURT_VISUAL_BYZANTINE_1_G1_TITLE: "Chrysotriklinos"
  COURT_VISUAL_BYZANTINE_1_G1_DESC: "A domed imperial audience hall of marble and mosaic, where the emperor rules beneath the gaze of saints."
  COURT_VISUAL_CHINESE_1_G1_TITLE: "The Hall of Heaven"
  COURT_VISUAL_CHINESE_1_G1_DESC: "A stately hall of vermilion pillars and silken drapery, where the mandate reigns from a canopied throne."
```

**影响**: 1.19.0 版本为更多 UI 元素和事件提供了完整的 10 语言本地化支持。

---

## 五、游戏数据 (Game Data) 变化

### 5.1 新增故事循环 (Story Cycles)

#### Debug Test Story Cycle
文件: `game/common/story_cycles/debug_test_story_cycle.txt` (94 行)

```yaml
debug_test_story = {
    visible = yes
    icon = { reference = "gfx/interface/icons/pets/artifact_cat_black.dds" }
    
    visualization = {
        character = { variable_name = "debug_test_story_liege" }
        character = { variable_name = "debug_test_story_enemy" }
        character_list = { variable_name = "debug_test_courtiers" }
        title = { variable_name = "debug_test_story_test_title" }
        title_list = { variable_name = "debug_test_story_title_list" }
        artifact = { variable_name = "debug_test_story_test_artifact" }
        artifact_list = { variable_name = "debug_test_story_artifact_list" }
        basic_counter = { variable_name = "debug_test_story_counter" min = 0 max = 10 }
        tug_of_war_counter = { variable_name = "debug_test_story_counter" min = -10 max = 10 }
        modifiers = { debug_test_story_prayer_modifier debug_test_story_weak_stomach_modifier }
        traits = { lifestyle_poet }
        decisions = { visit_silk_road_market_decision adopt_puppy_decision }
    }
}
```

**说明**: 这是用于内部测试的故事循环系统，不会在普通游戏中显示。

### 5.2 新增事件 (Events)

#### Elder Events (长者事件)
文件: `game/events/elder_events.txt` (769 行)

新增与老龄化相关的事件系统:

```yaml
namespace = elder_events

suitable_elder = {
    is_physically_able_adult = yes
    has_trait = withering_mind
    is_close_family_of = root
}

elder_events.1000 = {
    type = character_event
    title = elder_events.1000.t
    desc = elder_events.1000.desc
    theme = mental_health
    
    trigger = {
        is_available = yes
        has_trait_malicious_trigger = no
        any_courtier_or_guest = { suitable_elder = yes }
        NOT = { has_trait = withering_mind }
    }
    
    cooldown = { years = 25 }
}
```

**影响**: 新增"Withering Mind" (衰老心智) 特质相关事件，增加了游戏的老龄化系统深度。

#### Hunt Events (狩猎活动事件)
文件: `game/events/activities/hunt_activity/hunt_events_anna.txt` (11.13 KB)

#### Intrigue Events (阴谋事件)
文件: `game/events/lifestyles/intrigue_lifestyle/intrigue_events_bjorn.txt` (21.67 KB)

#### Travel Events (旅行事件)
文件: `game/events/travel_events/travel_events_bjorn.txt` (4.73 KB)

#### DLC Travel Danger Events
文件: `game/events/dlc/tgp/tgp_travel_danger_events.txt` (6.91 KB)

### 5.3 新增修饰符 (Modifiers)

#### Decision Modifiers
文件: `game/common/modifiers/decision_modifiers.txt`

```yaml
form_cumbria_decision_house_modifier = {
    icon = social_positive
    cumbrian_opinion = 10
    custom_cumbria_development_growth = 0.15
}

restore_carthage_house_modifier = {
    icon = county_modifier_development_positive
    custom_carthaginian_empire_development_growth = 0.20
}
```

#### Debug Story Cycle Modifiers
文件: `game/common/modifiers/12_debug_story_cycle_modifiers.txt`

新增:
- `debug_test_story_prayer_modifier`
- `debug_test_story_weak_stomach_modifier`

### 5.4 新增脚本化 GUI (Scripted GUIs)

#### Knight Permissions SGUIs
文件: `game/common/scripted_guis/knight_permissions_sguis.txt`

```yaml
kp_culture_minimum_prowess = {
    is_shown = {
        has_cultural_parameter = minimum_prowess_for_knights
    }
}

kp_culture_high_prowess = {
    is_shown = {
        has_cultural_parameter = high_prowess_ignores_knight_restrictions
    }
}

kp_culture_admin_family_knights = {
    is_shown = {
        has_cultural_parameter = non_admin_close_family_non_martial_gender_knights_in_defensive_wars
    }
}
```

**影响**: 骑士系统现在支持更多文化自定义参数。

### 5.5 新增脚本化效果 (Scripted Effects)

#### Easter Egg Historical Artifact Creation
文件: `game/common/scripted_effects/easteregg_historical_artifact_creation_effects.txt`

```yaml
create_artifact_easteregg_henry_longsword_effect = {
    save_scope_as = owner
    set_artifact_rarity_illustrious = yes

    create_artifact = {
        name = $ARTIFACT_NAME$
        description = artifact_radzig_kobyla_longsword_description
        template = general_unique_template
        creator = $CREATOR$
        type = sword
        visuals = easteregg_radzig_sword
        wealth = scope:wealth
        quality = scope:quality
        modifier = easteregg_henry_longsword_modifier
        history = { type = created_before_history }
    }

    scope:newly_created_artifact = {
        set_variable = { name = historical_unique_artifact value = yes }
    }
}
```

**影响**: 新增了历史文物创建的彩蛋效果系统。

---

## 六、图形资源 (Graphics) 变化

### 6.1 新增庭院场景背景

新增多种文化风格的宫廷场景背景:

| 背景名称 | 大小 | 文化类型 |
|----------|------|----------|
| byzantine.dds | 3.96 MB | 拜占庭风格 |
| chinese.dds | 3.96 MB | 中国风格 |
| chinese_alt.dds | 3.96 MB | 中国替代风格 |
| default.dds | 664.09 KB | 默认风格 |
| indian.dds | 664.09 KB | 印度风格 |
| japanese.dds | 3.96 MB | 日本风格 |
| mediterranean.dds | 664.09 KB | 地中海风格 |
| mena.dds | 2.58 MB | 中东/北非风格 |
| southeast_asia.dds | 3.96 MB | 东南亚风格 |
| steppe.dds | 3.96 MB | 草原风格 |
| tribal.dds | 664.09 KB | 部落风格 |
| western.dds | 664.09 KB | 西方风格 |

### 6.2 新增中国风格庭院资源

大量新增 `china_alt` 风格的庭院装饰资源:
- `ep4_chinese_alt_court_atlas_01_a_*.dds` - 纹理贴图
- `ep4_chinese_alt_court_beams_*.mesh` - 横梁模型
- `ep4_chinese_alt_court_dividers_*.dds` - 分隔符
- `ep4_chinese_alt_court_drapes_*.mesh` - 幕布
- `ep4_chinese_alt_court_flooring_*.mesh` - 地板
- `ep4_chinese_alt_court_lanterns.mesh` - 灯笼
- `ep4_chinese_alt_court_pillar_*.mesh` - 柱子
- `ep4_chinese_alt_court_rug_*.mesh` - 地毯

### 6.3 新增肖像资源

- Byzantine Crown (拜占庭皇冠) 装饰
- Western Crispinette (西方头饰) 装饰
- SP5 (特殊装饰) 变体

### 6.4 新增宠物图标

新增猫狗宠物 Artifact 图标:
- `artifact_cat_black.dds`
- `artifact_cat_calico.dds`
- `artifact_cat_ginger.dds`
- `artifact_cat_gray.dds`
- `artifact_cat_white.dds`
- `artifact_dog_*.dds` (多种颜色变体)

---

## 七、音频资源 (Audio) 变化

### 7.1 新增原声带

| 文件 | 大小 | 说明 |
|------|------|------|
| `game/sound/banks/Soundtrack_extra.bank` | 36.22 MB | 额外原声带 |

**影响**: 游戏现在包含额外的音乐内容。

---

## 八、二进制/库文件 (Binary/Library) 变化

### 8.1 新增文件

| 文件 | 大小 | 说明 |
|------|------|------|
| `binaries/PDXSDK.dll` | 2.40 MB | Paradox SDK 库 |
| `binaries/checksum.txt` | 34 B | 校验和文件 |
| `launcher/launcher-installer-windows_2026.4.1.exe` | 167.94 MB | 新版启动器安装程序 |

### 8.2 删除文件

| 文件 | 大小 | 说明 |
|------|------|------|
| `binaries/pops_api.dll` | 5.04 MB | 已移除 |

**影响**: PDX SDK 替换了旧的 pops_api 系统，启动器版本从 2026.1.1 升级到 2026.4.1。

---

## 九、核心文件差异分析

### 9.1 Clausewitz 引擎版本

| 项目 | 1.18.4 | 1.19.0 |
|------|--------|--------|
| Branch | titus/release/1.18.2 | titus/release/1.19.0 |
| Commit | 72b717fb89c6be4439541b07c480f8d6ec050f0d | f22559721a07e0156b809de8da35ffdc78a47d15 |

### 9.2 游戏构建版本

| 项目 | 1.18.4 | 1.19.0 |
|------|--------|--------|
| Branch | release/1.18.4 | release/1.19.0 |
| Commit | 6f57f9eb07db28b40185274899544bb29b3e579f | 2753ca4000401afbe17ad1c6cfeeb0acd0d927c1 |

---

## 十、关键变更总结

### 10.1 主要新功能

1. **宗教系统重构**
   - 从扁平的 doctrines 目录结构转换为模块化的 doctrine_types + doctrine_group_types + religion_types + holy_site_types 结构
   - 每个宗教有独立定义文件
   - 新增圣地系统

2. **PDX Account 登录系统**
   - 完整的账户登录/注册 UI
   - 法律文档查看器
   - 社交资料创建

3. **Ledger 窗口系统**
   - 246KB 的复杂 UI 系统
   - 用于显示游戏统计信息

4. **骑士徽章系统扩展**
   - 48+ 新图标
   - 徽章框架和样式

5. **长者/老龄化事件系统**
   - "Withering Mind" 特质相关事件
   - 新增 769 行的事件代码

6. **中国风格庭院资产**
   - 完整的中国宫廷场景支持

7. **宠物系统**
   - 猫狗宠物 Artifact 图标

8. **额外原声带**
   - 36.22 MB 新音乐

### 10.2 性能/技术变更

1. **引擎更新**: Clausewitz 从 1.18.2 升级到 1.19.0
2. **SDK 替换**: PDXSDK.dll 替换 pops_api.dll
3. **启动器升级**: 2026.1.1 -> 2026.4.1
4. **数据结构**: 宗教定义结构更加规范化

### 10.3 数据完整性

- 新增 583 个文件
- 删除 207 个文件
- 修改 3,789 个文件
- 总共约 5,000 个文件有变更

---

## 附录: 文件变更分布

| 目录/类型 | 新增 | 删除 | 修改 |
|-----------|------|------|------|
| binaries/ | 2 | 1 | ~5 |
| clausewitz/ | 10 | 0 | ~20 |
| game/common/religion/ | +100 | -50 | ~500 |
| game/events/ | +15 | ~5 | ~200 |
| game/gui/ | +25 | ~3 | ~150 |
| game/gfx/ | +200 | ~30 | ~800 |
| game/localization/ | +120 | ~10 | ~600 |
| jomini/ | +30 | 0 | ~100 |
| launcher/ | 1 | 0 | ~5 |
| **总计** | **583** | **207** | **3,789** |

---

*报告生成时间: 2026-05-03*
*数据来源: compare_versions.py 自动分析 + 人工深度分析*