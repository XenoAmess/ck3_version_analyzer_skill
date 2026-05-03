# Crusader Kings III 版本 1.18.4 vs 1.19.0 深度对比分析报告

## 版本基本信息

| 项目 | 1.18.4 | 1.19.0 |
|------|--------|--------|
| **游戏分支** | release/1.18.4 | release/1.19.0 |
| **游戏提交** | 6f57f9eb07db28b40185274899544bb29b3e579f | 2753ca4000401afbe17ad1c6cfeeb0acd0d927c1 |
| **引擎分支** | titus/release/1.18.2 | titus/release/1.19.0 |
| **引擎提交** | 72b717fb89c6be4439541b07c480f8d6ec050f0d | f22559721a07e0156b809de8da35ffdc78a47d15 |

---

## 一、整体差异统计

| 类别 | 数量 | 说明 |
|------|------|------|
| **新增文件** | 583 | 仅存在于 1.19.0 的文件 |
| **删除文件** | 207 | 仅存在于 1.18.4 的文件 |
| **修改文件** | 3,789 | 两版本都存在但内容/大小不同 |
| **未变化文件** | 45,238 | 两版本完全相同 |
| **文件总数** | 49,234 → 49,610 | 净增加 376 个文件 |

---

## 二、宗教系统重构 (核心变化)

### 2.1 目录结构重组

**1.18.4 旧结构:**
```
game/common/religion/
├── doctrines/                    ← 扁平的教条目录
│   ├── 10_doctrines_religions.txt
│   ├── 20_doctrines.txt          ← 所有教条混合在一个文件
│   ├── 20_doctrines_islam.txt
│   ├── 20_doctrines_judaism.txt
│   ├── 20_doctrines_zoroastrianism.txt
│   ├── 30_core_tenets.txt        ← 核心教义
│   ├── 40_doctrines_special.txt
│   └── _doctrines.info
└── fervor_modifiers/
    └── 00_fervor_modifiers.txt
```

**1.19.0 新结构:**
```
game/common/religion/
├── doctrine_types/               ← 独立教条类型目录
│   ├── 10_doctrines_religions.txt
│   ├── 20_doctrines.txt          ← 教条定义
│   ├── 20_doctrines_islam.txt
│   ├── 20_doctrines_judaism.txt
│   ├── 20_doctrines_zoroastrianism.txt
│   ├── 30_core_tenets.txt        ← 核心教义
│   ├── 40_doctrines_special.txt
│   └── _doctrine_types.info
├── doctrine_group_types/         ← 【新增】教条分组类型
│   ├── 00_doctrine_group_types.txt
│   └── _doctrine_group_types.info
├── holy_site_types/             ← 【新增】圣地类型
│   ├── 00_holy_site_types.txt
│   └── _holy_site_types.info
├── religion_family_types/        ← 【新增】宗教家族类型
│   ├── 00_religion_family_types.txt
│   └── _religion_family_types.info
└── religion_types/               ← 【新增】各宗教独立定义
    ├── 00_christianity.txt       ← 每个宗教独立文件
    ├── 00_islam.txt
    ├── 00_buddhism.txt
    ├── 00_hinduism.txt
    ├── 00_judaism.txt
    ├── 00_zoroastrianism.txt
    └── ... (共 51 个宗教文件)
```

### 2.2 教条分组类型 (Doctrine Group Types) - 新增概念

文件: `game/common/religion/doctrine_group_types/00_doctrine_group_types.txt`

这是 1.19.0 引入的新数据结构，将相关教条分组管理:

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

doctrine_kinslaying = {
    category = "crimes"
    doctrine_types = {
        doctrine_kinslaying_any_dynasty_member_crime
        doctrine_kinslaying_extended_family_crime
        doctrine_kinslaying_close_kin_crime
        doctrine_kinslaying_shunned
        doctrine_kinslaying_accepted
    }
}
```

**设计优势**: 
- 教条现在可以通过分组共享公共配置
- 简化了宗教定义的复杂度
- 便于批量修改相关教条

### 2.3 教条类型文件结构对比

**旧版 (doctrines/20_doctrines.txt):**
```yaml
doctrine_marriage_type = {
    group = "marriage"           # ← 嵌套在组内
    doctrine_monogamy = {
        piety_cost = { ... }
        parameters = { ... }
    }
}
```

**新版 (doctrine_types/20_doctrines.txt):**
```yaml
doctrine_monogamy = {            # ← 扁平化定义
    piety_cost = { ... }
    parameters = { ... }
}

doctrine_polygamy = {
    piety_cost = { ... }
    parameters = { ... }
}
```

### 2.4 宗教类型 (Religion Types) - 模块化定义

文件: `game/common/religion/religion_types/00_christianity.txt`

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

    # 婚姻
    doctrine = doctrine_monogamy
    doctrine = doctrine_divorce_approval
    doctrine = doctrine_bastardry_legitimization
    doctrine = doctrine_consanguinity_aunt_nephew_and_uncle_niece

    # 罪行
    doctrine = doctrine_homosexuality_shunned
    doctrine = doctrine_adultery_men_shunned
    doctrine = doctrine_adultery_women_crime
    doctrine = doctrine_kinslaying_close_kin_crime
    doctrine = doctrine_deviancy_crime
    doctrine = doctrine_witchcraft_crime

    # 宗教特性
    traits = {
        virtues = { forgiving compassionate chaste }
        sins = { vengeful sadistic lustful }
    }

    custom_faith_icons = {
        custom_faith_1 custom_faith_2 ...  # 大量自定义图标
    }
}
```

### 2.5 圣地类型 (Holy Site Types) - 新增系统

文件: `game/common/religion/holy_site_types/00_holy_site_types.txt` (3,542 行)

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

santiago = {
    county = c_santiago
    character_modifier = {
        name = holy_site_santiago_effect_name
        supply_duration = 0.2
        holy_order_hire_cost_mult = -0.1
    }
}
```

### 2.6 宗教系统变更影响

| 变更类型 | 1.18.4 | 1.19.0 | 影响 |
|----------|--------|--------|------|
| 教条存储 | 嵌套在组内 | 扁平独立定义 | 更清晰的模块化 |
| 教条分组 | 无 | doctrine_group_types | 支持批量管理 |
| 圣地定义 | 内嵌在教条中 | 独立的 holy_site_types | 圣地系统独立 |
| 宗教定义 | 混合文件 | 每个宗教独立文件 | 便于维护和扩展 |

---

## 三、用户界面 (UI) 系统变化

### 3.1 PDX Account 登录系统 (新增)

Paradox 账户集成系统，提供登录/账户管理功能:

| 文件 | 大小 | 功能 |
|------|------|------|
| `game/gui/pdx_account/base_types.gui` | 7.51 KB | 基础 UI 样式模板 |
| `game/gui/pdx_account/login_window.gui` | 14.11 KB | 登录窗口 |
| `game/gui/pdx_account/create_account_window.gui` | 106 B | 创建账户窗口 |
| `game/gui/pdx_account/legal_docs_viewer.gui` | 1.35 KB | 法律文档查看器 |
| `jomini/gui/pdx_account/base_types.gui` | 9.70 KB | Jomini 共享基础样式 |
| `jomini/gui/pdx_account/login_window.gui` | 9.54 KB | Jomini 登录窗口 |
| `jomini/gui/pdx_account/create_social_profile_window.gui` | 90 B | 社交资料创建 |

**UI 样式系统示例** (`base_types.gui`):
```gui
template SDKTextStyle
{
    using = Font_Type_Standard
    using = Font_Size_Small
    align = left
    default_format = "#medium"
}

template SDKButtonTextStyle
{
    block "sdk_button_text_style"
    {
        parentanchor = vcenter|hcenter
        font = StandardGameFont
        fontsize = 15
        fontcolor = { 0.86 0.86 0.73 1 }
        autoresize = yes
        position = { 0 0 }
        align = center
    }
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

**功能**: 玩家可以通过 PDX 账户系统登录游戏，支持云存档和多人游戏功能。

### 3.2 Ledger 窗口系统 (新增大规模 UI)

文件: `game/gui/window_ledger.gui` (246.31 KB, 9,614 行)

这是一个完整的分类账/总账界面系统:

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

    # 滚动区域
    scrollarea = {
        size = { 100% 100% }
        scrollbar_vertical = {
            using = Scrollbar_Vertical
        }
        scrollwidget = {
            flow_ledger_bookmarks = {}
        }
    }
}
```

**功能**: 显示游戏统计信息，包括:
- 地块/爵位信息 (titles)
- 文化传播数据
- 军事统计
- 经济数据
- 等

### 3.3 Accolade 骑士徽章系统扩展

大量新增骑士相关图形资源:

| 类型 | 数量 | 说明 |
|------|------|------|
| 骑士徽章图标 | 48+ | 不同颜色 (blue/green/purple/red) 和类型 |
| 徽章框架 | 2 | accolade_frame.dds, accolades_frames_background.dds |
| 扁平图标 | 38+ | flat_icons/*.dds (income, army, building 等) |

新增文件:
- `game/gui/window_accolade_attribute_selection.gui` (4.02 KB)
- `game/interface/icons/knight_badge/icons/accolade_trait_aggressive_*.dds`
- `game/interface/icons/knight_badge/icons/accolade_trait_champion_*.dds`
- `game/interface/icons/knight_badge/icons/accolade_trait_courtly_*.dds`
- 等等...

### 3.4 UI 变更总结

| 新增系统 | 文件数 | 主要功能 |
|----------|--------|----------|
| PDX Account | 9 | Paradox 账户登录/注册 |
| Ledger Window | 1 | 游戏统计信息显示 |
| Accolade System | 50+ | 骑士徽章图标和框架 |
| 总计 | 60+ | - |

---

## 四、本地化 (Localization) 变化

### 4.1 新增本地化文件

| 语言 | 新增文件数 | 主要内容 |
|------|------------|----------|
| 英语 (english) | 12 | ledger, court_visuals, debug_story, elder_events, knight_permissions, religion holy_sites |
| 法语 (french) | 12 | 同上 |
| 德语 (german) | 12 | 同上 |
| 日语 (japanese) | 12 | 同上 |
| 韩语 (korean) | 12 | 同上 |
| 波兰语 (polish) | 12 | 同上 |
| 俄语 (russian) | 12 | 同上 |
| 简体中文 (simp_chinese) | 12 | 同上 |
| 西班牙语 (spanish) | 12 | 同上 |
| **总计** | **108** | - |

### 4.2 新增本地化目录结构

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

### 4.3 本地化内容示例

**Court Visuals (庭院场景文本)**:
```yaml
l_english:
  COURT_VISUAL_BYZANTINE_1_G1_TITLE: "Chrysotriklinos"
  COURT_VISUAL_BYZANTINE_1_G1_DESC: "A domed imperial audience hall of marble and mosaic, where the emperor rules beneath the gaze of saints."
  COURT_VISUAL_CHINESE_1_G1_TITLE: "The Hall of Heaven"
  COURT_VISUAL_CHINESE_1_G1_DESC: "A stately hall of vermilion pillars and silken drapery, where the mandate reigns from a canopied throne."
  COURT_VISUAL_INDIAN_1_G1_TITLE: "Sabha Mandapa"
  COURT_VISUAL_INDIAN_1_G1_DESC: "A dignified pillared audience hall of carved stone and painted patterns where rulers hold court."
  COURT_VISUAL_JAPANESE_1_G1_TITLE: "Garden Shoin"
  COURT_VISUAL_JAPANESE_1_G1_DESC: "A serene tatami chamber where the lord receives guests beside painted screens and a quiet garden."
```

---

## 五、游戏数据 (Game Data) 变化

### 5.1 新增故事循环 (Story Cycles)

#### Debug Test Story Cycle
文件: `game/common/story_cycles/debug_test_story_cycle.txt`

```yaml
debug_test_story = {
    visible = yes
    icon = { reference = "gfx/interface/icons/pets/artifact_cat_black.dds" }
    
    visualization = {
        character = { variable_name = "debug_test_story_liege" label = "DEBUG_TEST_LIEGE" }
        character = { variable_name = "debug_test_story_enemy" label = "DEBUG_TEST_ENEMY" }
        character_list = { variable_name = "debug_test_story_courtiers" label = "DEBUG_TEST_COURTIERS" }
        title = { variable_name = "debug_test_story_test_title" label = "DEBUG_TEST_TITLE" }
        title_list = { variable_name = "debug_test_story_title_list" label = "DEBUG_TEST_TITLES" }
        artifact = { variable_name = "debug_test_story_test_artifact" label = "DEBUG_TEST_ARTIFACT" }
        artifact_list = { variable_name = "debug_test_story_artifact_list" label = "DEBUG_TEST_ARTIFACT_LIST" }
        basic_counter = { variable_name = "debug_test_story_counter" min = 0 max = 10 label = "DEBUG_TEST_VALUE_FOR_BASIC" }
        tug_of_war_counter = { variable_name = "debug_test_story_counter" min = -10 max = 10 label = "DEBUG_TEST_VALUE_FOR_TUG" }
        modifiers = { debug_test_story_prayer_modifier debug_test_story_weak_stomach_modifier }
        traits = { lifestyle_poet }
        decisions = { visit_silk_road_market_decision adopt_puppy_decision }
        custom_string_key = "DEBUG_TEST_CUSTOM_STRING_KEY"
    }
}
```

**说明**: 这是一个用于开发/测试的故事循环系统，可在调试模式下通过右键点击角色触发。

### 5.2 新增长者事件系统 (Elder Events)

文件: `game/events/elder_events.txt` (769 行)

```yaml
namespace = elder_events

suitable_elder = {
    is_physically_able_adult = yes
    has_trait = withering_mind
    is_close_family_of = root
    NOR = {
        is_sibling_of = root
        has_relation_rival = root
    }
}

elder_events.1000 = {
    type = character_event
    title = elder_events.1000.t
    desc = elder_events.1000.desc
    theme = mental_health
    override_background = { reference = relaxing_room }

    left_portrait = {
        character = root
        animation = sadness
    }

    right_portrait = {
        character = scope:elder
        animation = admiration
        camera = camera_event_center_pointing_left
    }
    
    trigger = {
        is_available = yes
        has_trait_malicious_trigger = no
        any_courtier_or_guest = { suitable_elder = yes }
        NOT = { has_trait = withering_mind }
    }
    
    cooldown = { years = 25 }
}
```

**新增内容**:
- "Withering Mind" (衰老心智) 特质相关事件
- 涉及老龄化主题的心理健康事件
- 25 年冷却时间防止重复触发

### 5.3 其他新增事件

| 文件 | 大小 | 内容 |
|------|------|------|
| `game/events/activities/hunt_activity/hunt_events_anna.txt` | 11.13 KB | 狩猎活动事件 |
| `game/events/lifestyles/intrigue_lifestyle/intrigue_events_bjorn.txt` | 21.67 KB | 阴谋生活风格事件 |
| `game/events/travel_events/travel_events_bjorn.txt` | 4.73 KB | 旅行事件 |
| `game/events/dlc/tgp/tgp_travel_danger_events.txt` | 6.91 KB | DLC 旅行危险事件 |
| `game/events/story_cycles/debug_story_cycle_test_events.txt` | 6.50 KB | 故事循环测试事件 |

### 5.4 新增修饰符 (Modifiers)

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

### 5.5 新增脚本化 GUI (Scripted GUIs)

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

**影响**: 骑士系统现在支持更灵活的文化自定义参数控制。

### 5.6 新增脚本化效果 (Scripted Effects)

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
        decaying = no
    }

    scope:newly_created_artifact = {
        set_variable = { name = historical_unique_artifact value = yes }
    }
}
```

**影响**: 实现了历史文物的彩蛋创建系统，包括著名的"Radzig Sword"。

---

## 六、图形资源 (Graphics) 变化

### 6.1 新增庭院场景背景

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

### 6.2 新增中国风格庭院资产

大量新增 `china_alt` 风格的庭院装饰资源 (100+ 文件):
- 纹理: `ep4_chinese_alt_court_*_diffuse.dds`, `_normal.dds`, `_properties.dds`
- 模型: `ep4_chinese_alt_court_beams_*.mesh`, `ep4_chinese_alt_court_pillar_*.mesh`
- 幕布: `ep4_chinese_alt_court_drapes_*.mesh`
- 地板: `ep4_chinese_alt_court_flooring_*.mesh`
- 灯笼: `ep4_chinese_alt_court_lanterns.mesh`
- 地毯: `ep4_chinese_alt_court_rug_*.mesh`

### 6.3 新增肖像装饰

- Byzantine Crown (拜占庭皇冠) 装饰 (`f_headgear_sec_sp5_byzantine_roy_01`)
- Western Crispinette (西方头饰) 装饰
- SP5 (特殊装饰) 变体纹理

### 6.4 新增宠物图标

| 文件 | 大小 | 描述 |
|------|------|------|
| `artifact_cat_black.dds` | 225.12 KB | 黑猫 |
| `artifact_cat_calico.dds` | 225.12 KB | 三色猫 |
| `artifact_cat_ginger.dds` | 226.06 KB | 橘猫 |
| `artifact_cat_gray.dds` | 225.12 KB | 灰猫 |
| `artifact_cat_white.dds` | 226.06 KB | 白猫 |
| `artifact_dog_*.dds` | 224-227 KB | 多种颜色狗 |

---

## 七、音频资源 (Audio) 变化

### 7.1 新增原声带

| 文件 | 大小 | 说明 |
|------|------|------|
| `game/sound/banks/Soundtrack_extra.bank` | 36.22 MB | 额外原声带 |

---

## 八、二进制/库文件 (Binary/Library) 变化

### 8.1 新增文件

| 文件 | 大小 | 说明 |
|------|------|------|
| `binaries/PDXSDK.dll` | 2.40 MB | Paradox SDK 库 |
| `binaries/checksum.txt` | 34 B | 校验和文件 |
| `launcher/launcher-installer-windows_2026.4.1.exe` | 167.94 MB | 新版启动器安装程序 (2026.1.1 → 2026.4.1) |

### 8.2 删除文件

| 文件 | 大小 | 说明 |
|------|------|------|
| `binaries/pops_api.dll` | 5.04 MB | 已移除 (被 PDXSDK.dll 替代) |

---

## 九、变更分布统计

### 9.1 按目录分布

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

## 十、核心变更总结

### 10.1 主要新功能

1. **宗教系统重构** (最重大变更)
   - 从扁平 `doctrines` 目录转换为模块化的 `doctrine_types/` + `doctrine_group_types/` + `holy_site_types/` + `religion_types/` 结构
   - 每个宗教有独立定义文件 (51 个宗教)
   - 新增圣地类型系统
   - 新增宗教家族类型

2. **PDX Account 登录系统**
   - 完整的 Paradox 账户登录/注册 UI
   - 法律文档查看器
   - 社交资料创建

3. **Ledger 窗口系统**
   - 246KB 的复杂 UI 系统
   - 用于显示游戏各种统计信息

4. **骑士徽章系统扩展**
   - 48+ 新图标
   - 徽章框架和样式

5. **长者/老龄化事件系统**
   - "Withering Mind" 特质相关事件
   - 新增 769 行事件代码

6. **中国风格庭院资产**
   - 完整的中国宫廷场景支持
   - 100+ 新图形资源

7. **宠物系统**
   - 猫狗宠物 Artifact 图标

8. **额外原声带**
   - 36.22 MB 新音乐

### 10.2 性能/技术变更

| 项目 | 1.18.4 | 1.19.0 | 变更说明 |
|------|--------|--------|----------|
| 引擎版本 | titus/release/1.18.2 | titus/release/1.19.0 | 主要版本升级 |
| SDK | pops_api.dll | PDXSDK.dll | 替换 |
| 启动器 | 2026.1.1 | 2026.4.1 | 升级 |

### 10.3 对玩家影响

1. **宗教系统更丰富**: 更多宗教类型，更多圣地选择
2. **UI 更完善**: 账户系统，统计界面
3. **图形提升**: 中国宫廷风格，骑士徽章
4. **音效增加**: 新增音乐内容
5. **宠物陪伴**: 可以获得猫狗宠物

---

## 附录: 关键文件路径

### 宗教系统
- `game/common/religion/doctrine_types/20_doctrines.txt` - 教条类型定义
- `game/common/religion/doctrine_group_types/00_doctrine_group_types.txt` - 教条分组
- `game/common/religion/holy_site_types/00_holy_site_types.txt` - 圣地类型
- `game/common/religion/religion_types/00_christianity.txt` - 基督教定义

### UI 系统
- `game/gui/pdx_account/base_types.gui` - 账户基础样式
- `game/gui/window_ledger.gui` - 统计窗口
- `game/gui/window_accolade_attribute_selection.gui` - 骑士徽章选择

### 游戏数据
- `game/events/elder_events.txt` - 长者事件
- `game/common/scripted_guis/knight_permissions_sguis.txt` - 骑士权限

### 本地化
- `game/localization/english/court_visuals_l_english.yml` - 庭院场景文本
- `game/localization/english/ledger/ledger_filtersorts_l_english.yml` - 统计过滤器

---

*报告生成时间: 2026-05-03*
*数据来源: compare_versions.py 自动分析 + 源代码深度审查*