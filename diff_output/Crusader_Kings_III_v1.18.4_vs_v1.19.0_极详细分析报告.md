# Crusader Kings III 版本 1.18.4 vs 1.19.0 极详细对比分析报告

## 版本基本信息

| 项目 | 1.18.4 | 1.19.0 |
|------|--------|--------|
| **游戏分支** | release/1.18.4 | release/1.19.0 |
| **游戏提交** | 6f57f9eb07db28b40185274899544bb29b3e579f | 2753ca4000401afbe17ad1c6cfeeb0acd0d927c1 |
| **引擎分支** | titus/release/1.18.2 | titus/release/1.19.0 |
| **引擎提交** | 72b717fb89c6be4439541b07c480f8d6ec050f0d | f22559721a07e0156b809de8da35ffdc78a47d15 |

---

## 一、整体差异统计总览

| 类别 | 数量 | 说明 |
|------|------|------|
| **新增文件** | 583 | 仅存在于 1.19.0 的文件 |
| **删除文件** | 207 | 仅存在于 1.18.4 的文件 |
| **修改文件** | 3,789 | 两版本都存在但内容/大小不同 |
| **未变化文件** | 45,238 | 两版本完全相同 |
| **文件总数** | 49,234 → 49,610 | 净增加 376 个文件 |

---

## 二、宗教系统重构 (最核心变化)

### 2.1 目录结构重组

**1.18.4 旧结构 (doctrines/ 目录):**
```
game/common/religion/
├── doctrines/                    ← 扁平的教条目录
│   ├── 10_doctrines_religions.txt  (敌对教条组 - 嵌套结构)
│   ├── 20_doctrines.txt            (婚姻/罪行教条 - 嵌套在 wrapper 中)
│   ├── 20_doctrines_islam.txt
│   ├── 20_doctrines_judaism.txt
│   ├── 20_doctrines_zoroastrianism.txt
│   ├── 30_core_tenets.txt          (核心教义)
│   ├── 40_doctrines_special.txt
│   └── _doctrines.info
└── fervor_modifiers/
    └── 00_fervor_modifiers.txt
```

**1.19.0 新结构 (doctrine_types/ + doctrine_group_types/ + religion_types/):**
```
game/common/religion/
├── doctrine_types/               ← 独立教条类型 (扁平化)
│   ├── 10_doctrines_religions.txt  (敌对教条 - 现在是独立 block)
│   ├── 20_doctrines.txt            (婚姻/罪行 - 独立 block)
│   ├── 20_doctrines_islam.txt
│   ├── 20_doctrines_judaism.txt
│   ├── 20_doctrines_zoroastrianism.txt
│   ├── 30_core_tenets.txt          (核心教义 - 独立 block)
│   ├── 40_doctrines_special.txt
│   └── _doctrine_types.info
├── doctrine_group_types/         ← 【新增】教条分组类型
│   ├── 00_doctrine_group_types.txt (587 行)
│   └── _doctrine_group_types.info
├── holy_site_types/              ← 【新增】圣地类型
│   ├── 00_holy_site_types.txt     (3542 行)
│   └── _holy_site_types.info
├── religion_family_types/        ← 【新增】宗教家族类型
│   ├── 00_religion_family_types.txt (26 行)
│   └── _religion_family_types.info
└── religion_types/               ← 【新增】各宗教独立定义 (50 个文件)
    ├── 00_christianity.txt       (1154 行)
    ├── 00_islam.txt              (977 行)
    ├── 00_buddhism.txt
    ├── 00_hinduism.txt
    ├── 00_judaism.txt
    ├── 00_zoroastrianism.txt
    └── ... (共 50 个宗教文件)
```

### 2.2 教条结构变化详解

#### 2.2.1 敌对教条 (Hostility Doctrines) 变化

**1.18.4 (doctrines/10_doctrines_religions.txt):**
```yaml
hostility_group = {
    group = "not_creatable"
    
    abrahamic_hostility_doctrine = {
        parameters = {
            hostility_same_religion = 2
            hostility_same_family = 3
            hostility_others = 3
        }
    }
    
    pagan_hostility_doctrine = {
        visible = no
        parameters = {
            hostility_same_religion = 1
            hostility_same_family = 2
            hostility_others = 3
        }
    }
    
    eastern_hostility_doctrine = {
        parameters = {
            hostility_same_religion = 1
            hostility_same_family = 1
            hostility_others = 2
        }
    }
    
    sinitic_hostility_doctrine = {
        parameters = {
            hostility_same_religion = 1
            hostility_same_family = 1
            hostility_others = 2
        }
    }
}
```

**1.19.0 (doctrine_types/10_doctrines_religions.txt) - 扁平化:**
```yaml
abrahamic_hostility_doctrine = {
    parameters = {
        hostility_same_religion = 2
        hostility_same_family = 3
        hostility_others = 3
    }
}

pagan_hostility_doctrine = {
    visible = no
    parameters = {
        hostility_same_religion = 1
        hostility_same_family = 2
        hostility_others = 3
    }
}

eastern_hostility_doctrine = {
    parameters = {
        hostility_same_religion = 1
        hostility_same_family = 1
        hostility_others = 2
    }
}

sinitic_hostility_doctrine = {
    parameters = {
        hostility_same_religion = 1
        hostility_same_family = 1
        hostility_others = 2
    }
}
```

**变化**: wrapper `hostility_group` 被移除，每个敌对教条成为独立顶层 block。

#### 2.2.2 婚姻/罪行教条变化

**1.18.4 (doctrines/20_doctrines.txt):**
```yaml
doctrine_marriage_type = {
    group = "marriage"
    
    doctrine_monogamy = {
        piety_cost = { value = faith_doctrine_cost_mid }
        parameters = { number_of_spouses = 1 }
    }
    
    doctrine_polygamy = {
        piety_cost = { value = faith_doctrine_cost_mid }
        parameters = { number_of_spouses = 4 }
    }
    
    doctrine_concubines = {
        piety_cost = { value = faith_doctrine_cost_mid }
        parameters = { number_of_consorts = 3 }
    }
}

doctrine_divorce = {
    group = "marriage"
    doctrine_divorce_disallowed = { ... }
    doctrine_divorce_approval = { ... }
    doctrine_divorce_allowed = { ... }
}
```

**1.19.0 (doctrine_types/20_doctrines.txt) - 扁平化:**
```yaml
doctrine_monogamy = {
    piety_cost = { value = faith_doctrine_cost_mid }
    parameters = { number_of_spouses = 1 }
}

doctrine_polygamy = {
    piety_cost = { value = faith_doctrine_cost_mid }
    parameters = { number_of_spouses = 4 }
}

doctrine_concubines = {
    piety_cost = { value = faith_doctrine_cost_mid }
    parameters = { number_of_consorts = 3 }
}

doctrine_divorce_disallowed = { ... }
doctrine_divorce_approval = { ... }
doctrine_divorce_allowed = { ... }
```

### 2.3 新增: 教条分组类型 (Doctrine Group Types)

文件: `doctrine_group_types/00_doctrine_group_types.txt` (587 行)

```yaml
# 分组示例
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

doctrine_witchcraft = {
    category = "crimes"
    doctrine_types = {
        doctrine_witchcraft_crime
        doctrine_witchcraft_shunned
        doctrine_witchcraft_accepted
        doctrine_witchcraft_virtuous
    }
}

doctrine_gender = {
    category = "main_group"
    doctrine_types = {
        doctrine_gender_male_dominated
        doctrine_gender_equal
        doctrine_gender_female_dominated
    }
}

doctrine_pluralism = {
    category = "main_group"
    doctrine_types = {
        doctrine_pluralism_fundamentalist
        doctrine_pluralism_righteous
        doctrine_pluralism_pluralistic
    }
}

doctrine_theocracy = {
    category = "main_group"
    doctrine_types = {
        doctrine_theocracy_temporal
        doctrine_theocracy_lay_clergy
    }
}

doctrine_head_of_faith = {
    category = "main_group"
    doctrine_types = {
        doctrine_no_head
        doctrine_spiritual_head
        doctrine_temporal_head
    }
}

doctrine_pilgrimage = {
    category = "main_group"
    doctrine_types = {
        doctrine_pilgrimage_forbidden
        doctrine_pilgrimage_encouraged
        doctrine_pilgrimage_local_rites
        doctrine_pilgrimage_mandatory
        doctrine_pilgrimage_mandatory_hajj
    }
}
```

### 2.4 新增: 宗教家族类型 (Religion Family Types)

文件: `religion_family_types/00_religion_family_types.txt` (26 行)

```yaml
rf_abrahamic = {
    graphical_faith = "orthodox_gfx"
    hostility_doctrine = abrahamic_hostility_doctrine
    doctrine_background_icon = core_tenet_banner_christian.dds
}

rf_eastern = {  # Dharmic
    piety_icon_group = "eastern"
    graphical_faith = "dharmic_gfx"
    hostility_doctrine = eastern_hostility_doctrine
    doctrine_background_icon = core_tenet_banner_eastern.dds
}

rf_sinitic = {
    piety_icon_group = "taoism"
    graphical_faith = "dharmic_gfx"
    hostility_doctrine = eastern_hostility_doctrine
    doctrine_background_icon = core_tenet_banner_eastern.dds
}

rf_pagan = {
    piety_icon_group = "pagan"
    graphical_faith = "pagan_gfx"
    hostility_doctrine = pagan_hostility_doctrine
    doctrine_background_icon = core_tenet_banner_pagan.dds
}
```

### 2.5 新增: 圣地类型 (Holy Site Types)

文件: `holy_site_types/00_holy_site_types.txt` (3542 行)

定义了所有宗教的圣地，每个圣地包含:
- `county` / `barony`: 位置
- `character_modifier`: 对角色的加成
- `parameters`: 特殊效果

```yaml
# 基督教圣地示例
jerusalem = {
    county = c_jerusalem
    character_modifier = {
        monthly_piety_gain_mult = 0.2
    }
    parameters = {
        jerusalem_conversion_bonus  # +20% County Conversion
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

# 佛教圣地示例
lumbini = {
    county = c_nepal
    character_modifier = {
        name = holy_site_lumbini_effect_name
        monthly_piety_gain_mult = 0.15
        monthly_lifestyle_xp_gain_mult = 0.1
    }
}

# 印度教圣地示例
varanasi = {
    county = c_kashi
    character_modifier = {
        name = holy_site_varanasi_effect_name
        monthly_piety_gain_mult = 0.2
        learning_per_piety_level = 1
    }
}
```

### 2.6 宗教类型文件示例 (Religion Types)

文件: `religion_types/00_christianity.txt` (1154 行) 关键结构:

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

    traits = {
        virtues = { forgiving compassionate chaste }
        sins = { vengeful sadistic lustful }
    }

    reserved_male_names = {
        Andrew Antoninus Bartolomeus Benedict Christian Christopher Clement
        Constantine David Demetrius Eustace George Gregory Hans Isaac
        # ... 更多名字
    }

    custom_faith_icons = {
        custom_faith_1 custom_faith_2 custom_faith_3 ...
    }

    holy_order_names = {
        { name = "holy_order_knights_of_the_chalice" }
        { name = "holy_order_order_of_the_holy_communion" }
        # ...
    }

    localization = {
        HighGodName = christianity_high_god_name
        HighGodNamePossessive = christianity_high_god_name_possessive
        CreatorName = christianity_creator_god_name
        # ... 更多本地化键
    }
}
```

文件: `religion_types/00_islam.txt` (977 行) 关键结构:

```yaml
islam_religion = {
    family = rf_abrahamic
    graphical_faith = "islamic_gfx"
    doctrine_background_icon = core_tenet_banner_islam.dds
    
    # 标准教条
    doctrine = doctrine_monotheist
    doctrine = abrahamic_hostility_doctrine
    doctrine = doctrine_polygamy  # 允许一夫多妻
    doctrine = doctrine_gender_male_dominated
    doctrine = doctrine_consanguinity_cousins
    doctrine = doctrine_divorce_approval
    doctrine = doctrine_bastardry_none
    doctrine = doctrine_homosexuality_shunned
    doctrine = doctrine_adultery_men_shunned
    doctrine = doctrine_adultery_women_shunned
    doctrine = doctrine_kinslaying_accepted  # 血亲杀戮可接受
    doctrine = doctrine_deviancy_shunned
    doctrine = doctrine_witchcraft_crime
    doctrine = doctrine_pluralism_righteous
    doctrine = doctrine_theocracy_lay_clergy
    doctrine = doctrine_pilgrimage_mandatory_hajj  # 强制朝觐
    
    traits = {
        virtues = { temperate generous just }
        sins = { gluttonous greedy arbitrary drunkard }
    }
    
    reserved_male_names = {
        Abbas Abdul Abdullah Abolhassan Abu-Bakr Ahmad Akbar
        # ...
    }
}
```

### 2.7 宗教系统变更影响总结

| 变更类型 | 1.18.4 | 1.19.0 | 玩家影响 |
|----------|--------|--------|----------|
| 教条存储 | 嵌套在组 wrapper 中 | 扁平独立定义 | 更清晰的模块化 |
| 教条分组 | 内嵌在文件结构中 | doctrine_group_types 显式管理 | 便于批量修改 |
| 圣地定义 | 内嵌在教条/宗教中 | 独立的 holy_site_types | 圣地系统独立化 |
| 宗教定义 | 混合文件 | 50 个独立文件 | 便于维护和扩展 |
| 家族定义 | 无 | rf_abrahamic/eastern/sinitic/pagan | 统一家族系统 |

---

## 三、用户界面 (UI) 系统变化

### 3.1 PDX Account 登录系统 (新增)

Paradox 账户集成系统，提供完整的账户管理功能:

| 文件 | 大小 | 功能 |
|------|------|------|
| `game/gui/pdx_account/base_types.gui` | 7.51 KB | 基础 UI 样式模板 |
| `game/gui/pdx_account/login_window.gui` | 14.11 KB | 登录窗口 |
| `game/gui/pdx_account/create_account_window.gui` | 106 B | 创建账户窗口 |
| `game/gui/pdx_account/legal_docs_viewer.gui` | 1.35 KB | 法律文档查看器 |
| `jomini/gui/pdx_account/base_types.gui` | 9.70 KB | Jomini 共享基础样式 |
| `jomini/gui/pdx_account/login_window.gui` | 9.54 KB | Jomini 登录窗口 |
| `jomini/gui/pdx_account/create_account_window.gui` | 5.87 KB | Jomini 创建账户 |
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
        name = "sdk_button_text"
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

template sdk_dropdown_enum
{
    # 下拉框模板
    active_item = {
        widget = {
            size = { 250 30 }
            button = { using = SDKDropdownButtonStyle }
            editor_textbox = { ... }
        }
    }
    list = {
        scrollarea = { ... }
    }
}
```

### 3.2 Ledger 窗口系统 (新增大规模 UI)

文件: `game/gui/window_ledger.gui` (246.31 KB, 9614 行)

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
        scrollbar_vertical = { using = Scrollbar_Vertical }
        scrollwidget = { flow_ledger_bookmarks = {} }
    }

    vbox = {
        header_pattern = {
            blockoverride "header_text" { text = "LEDGER_WINDOW_TITLE" }
            blockoverride "button_close" { onclick = "[CloseGameView('ledger')]" }
        }

        # 战争账本
        vbox_ledger = {
            visible = "[GetVariableSystem.HasValue('ledger_tab', 'ongoing_wars')]"
            datamodel = "[LedgerWindow.GetWars]"
            # ...
        }

        # 文物账本
        vbox_ledger = {
            visible = "[GetVariableSystem.HasValue('ledger_tab', 'artifacts')]"
            datamodel = "[LedgerWindow.GetArtifacts]"
            # ...
        }
    }
}
```

**Ledger 包含的标签页**:
- `ongoing_wars` - 进行中的战争
- `artifacts` - 文物
- `titles` - 爵位
- `cultures` - 文化
- 等

### 3.3 Accolade 骑士徽章系统扩展

文件: `game/gui/window_accolade_attribute_selection.gui` (159 行)

```gui
window = {
    name = "accolade_attribute_selection_view"
    size = { 540 780 }
    parentanchor = top|right
    position = { -630 170 }
    layer = middle

    vbox = {
        datacontext = "[AccoladeAttributeSelectionView.GetAccolade]"

        header_pattern = {
            blockoverride "header_text" { text = "[Accolade.GetNameNoTooltip]" }
            blockoverride "button_close" { onclick = "[AccoladeAttributeSelectionView.Close]" }
        }

        scrollbox = {
            fixedgridbox = {
                name = "types_grid"
                datamodel = "[AccoladeAttributeSelectionView.GetOtherAttributes]"
                datamodel_wrap = 3
                addcolumn = 180
                addrow = 164

                item = {
                    button_standard = {
                        enabled = "[StringIsEmpty( AccoladeType.GetKnightValidForAccoladeTypeDesc )]"
                        onclick = "[AccoladeAttributeSelectionView.OnClick( AccoladeType.Self )]"
                        highlight_icon = {
                            texture = "[AccoladeType.GetIcon]"
                        }
                    }
                }
            }
        }

        button_standard = {  # 确认按钮
            onclick = "[AccoladeAttributeSelectionView.ConfirmSelection]"
            enabled = "[IsValidCommand( Accolade.MakeAddAccoladeTypeCommand( AccoladeAttributeSelectionView.GetSelectedType ) )]"
        }
    }
}
```

**新增图形资源**:
- 48+ 骑士徽章图标 (`accolade_trait_aggressive_*.dds`, `accolade_trait_champion_*.dds` 等)
- 徽章框架: `accolade_frame.dds`, `accolades_frames_background.dds`
- 38+ 扁平图标 (`flat_icons/*.dds`)

---

## 四、游戏数据 (Game Data) 变化

### 4.1 长者事件系统 (Elder Events)

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

# 事件 1000: Withering Mind - 亲属忘记你的名字
elder_events.1000 = {
    type = character_event
    title = elder_events.1000.t
    desc = elder_events.1000.desc
    theme = mental_health
    override_background = { reference = relaxing_room }

    left_portrait = { character = root animation = sadness }
    right_portrait = { character = scope:elder animation = admiration }

    trigger = {
        is_available = yes
        has_trait_malicious_trigger = no
        any_courtier_or_guest = { suitable_elder = yes }
        NOT = { has_trait = withering_mind }
    }

    cooldown = { years = 25 }

    option = {
        name = elder_events.1000.a
        scope:elder = { add_stress = medium_stress_impact_gain }
        stress_impact = { base = minor_stress_impact_gain honest = minor_stress_impact_loss }
    }

    option = {
        name = elder_events.1000.b
        scope:elder = { add_trait_xp = { trait = withering_mind track = withering_mind value = 10 } }
        stress_impact = { base = minor_stress_impact_gain honest = medium_stress_impact_gain }
    }
}

# 事件 1100: Fragile Bones - 摔倒
elder_events.1100 = {
    type = character_event
    title = elder_events.1100.t
    desc = elder_events.1100.desc
    theme = physical_health
    override_background = corridor_day

    trigger = {
        has_trait = fragile_bones
        prowess < 10
        is_landed_or_landless_administrative = yes
        is_available_adult = yes
        NOT = { has_trait = athletic }
        location = {
            NOR = {
                has_holding_type = nomad_holding
                has_holding_type = herder_holding
                has_holding_type = tribal_holding
            }
        }
    }

    cooldown = { years = 25 }

    option = {
        name = elder_events.1100.bodyguard
        # 事件逻辑...
    }

    option = {
        name = elder_events.1100.nobodyguard
        # 事件逻辑...
    }
}
```

**新增特质相关事件**:
- `elder_events.1000` - Withering Mind (衰老心智)
- `elder_events.1100` - Fragile Bones (脆弱骨骼)
- `elder_events.1200` - Clouded Eyes (浑浊双眼)
- `elder_events.1300` - Faltering Heart (衰弱心脏)

### 4.2 其他新增事件

| 文件 | 大小 | 内容 |
|------|------|------|
| `game/events/activities/hunt_activity/hunt_events_anna.txt` | 11.13 KB | 狩猎活动事件 |
| `game/events/lifestyles/intrigue_lifestyle/intrigue_events_bjorn.txt` | 21.67 KB | 阴谋生活风格事件 |
| `game/events/travel_events/travel_events_bjorn.txt` | 4.73 KB | 旅行事件 |
| `game/events/dlc/tgp/tgp_travel_danger_events.txt` | 6.91 KB | DLC 旅行危险事件 |
| `game/events/story_cycles/debug_story_cycle_test_events.txt` | 6.50 KB | 故事循环测试事件 |

### 4.3 新增脚本化 GUI (Scripted GUIs)

文件: `game/common/scripted_guis/knight_permissions_sguis.txt` (17 行)

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

### 4.4 新增修饰符 (Modifiers)

文件: `game/common/modifiers/decision_modifiers.txt` (13 行)

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

### 4.5 新增脚本化效果 (Scripted Effects)

文件: `game/common/scripted_effects/easteregg_historical_artifact_creation_effects.txt` (25 行)

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

### 4.6 调试故事循环 (Debug Story Cycle)

文件: `game/common/story_cycles/debug_test_story_cycle.txt` (94 行)

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
        basic_counter = { variable_name = "debug_test_story_counter" min = 0 max = 10 }
        tug_of_war_counter = { variable_name = "debug_test_story_counter" min = -10 max = 10 }
        modifiers = { debug_test_story_prayer_modifier debug_test_story_weak_stomach_modifier }
        traits = { lifestyle_poet }
        decisions = { visit_silk_road_market_decision adopt_puppy_decision }
    }
}
```

### 4.7 新增肖像装饰

**新增头饰装饰**:
- Byzantine Crown (拜占庭皇冠): `f_headgear_sec_sp5_byzantine_roy_01`, `m_headgear_sec_sp5_byzantine_roy_01`
- Western Crispinette (西方头饰): `sp5_western_crispinette_01`
- SP5 变体纹理

**新增胡须/发型**:
- `m_beard_sp5_western_01` - 西方胡须变体
- `m_hair_sp5_western_01` - 西方发型变体

---

## 五、图形资源 (Graphics) 变化

### 5.1 庭院场景背景

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

### 5.2 中国风格庭院资产 (china_alt)

**新增目录**: `game/gfx/models/court/rooms/china_alt/` 和 `game/gfx/models/court/materials/china_alt/`

**新增文件类型**:
- 纹理: `_diffuse.dds`, `_normal.dds`, `_properties.dds`
- 模型: `.mesh` 文件
- 资产: `.asset` 文件

**资源列表**:
```
ep4_chinese_alt_court_atlas_01_a_diffuse.dds (512.12 KB)
ep4_chinese_alt_court_atlas_01_a_normal.dds (1.33 MB)
ep4_chinese_alt_court_atlas_01_a_properties.dds (1.00 MB)
ep4_chinese_alt_court_beams_01.mesh (502.93 KB)
ep4_chinese_alt_court_beams_dougong_01.mesh (172.22 KB)
ep4_chinese_alt_court_beams_dougong_02.mesh (96.19 KB)
ep4_chinese_alt_court_dividers_01.mesh (206.54 KB)
ep4_chinese_alt_court_drapes_01.mesh (2.44 MB)
ep4_chinese_alt_court_drapes_02.mesh (370.48 KB)
ep4_chinese_alt_court_flooring_01.mesh (241.14 KB)
ep4_chinese_alt_court_lanterns.mesh (527.50 KB)
ep4_chinese_alt_court_pillars_01.mesh (293.18 KB)
ep4_chinese_alt_court_rug_01_a.mesh (17.08 KB)
```

### 5.3 新增宠物图标

| 文件 | 大小 | 描述 |
|------|------|------|
| `artifact_cat_black.dds` | 225.12 KB | 黑猫 |
| `artifact_cat_calico.dds` | 225.12 KB | 三色猫 |
| `artifact_cat_ginger.dds` | 226.06 KB | 橘猫 |
| `artifact_cat_gray.dds` | 225.12 KB | 灰猫 |
| `artifact_cat_white.dds` | 226.06 KB | 白猫 |
| `artifact_dog_black.dds` | 225.12 KB | 黑狗 |
| `artifact_dog_blonde.dds` | 225.12 KB | 金毛狗 |
| `artifact_dog_brown.dds` | 224.19 KB | 棕狗 |
| `artifact_dog_gray.dds` | 227.00 KB | 灰狗 |
| `artifact_dog_pointed_ears_*.dds` | ~225 KB | 多种颜色尖耳狗 |
| `artifact_dog_white.dds` | 225.12 KB | 白狗 |

### 5.4 新增高分辨率图标

| 类型 | 数量 | 大小 |
|------|------|------|
| 扁平图标 (flat_icons) | 38+ | 14.19 KB each |
| 骑士徽章图标 | 48+ | 11.39-45.12 KB |
| DLC 图标 | 2 | 56.38 KB each |
| 故事循环图标 | 4 | 56.38-64.12 KB |

---

## 六、本地化 (Localization) 变化

### 6.1 新增本地化文件统计

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
| **总计** | **108** | - |

### 6.2 本地化内容示例

**Court Visuals (庭院场景文本)**:
```yaml
l_english:
  COURT_VISUAL_BYZANTINE_1_G1_TITLE: "Chrysotriklinos"
  COURT_VISUAL_BYZANTINE_1_G1_DESC: "A domed imperial audience hall of marble and mosaic, where the emperor rules beneath the gaze of saints."
  COURT_VISUAL_CHINESE_1_G1_TITLE: "The Hall of Heaven"
  COURT_VISUAL_CHINESE_1_G1_DESC: "A stately hall of vermilion pillars and silken drapery, where the mandate reigns from a canopied throne."
  COURT_VISUAL_JAPANESE_1_G1_TITLE: "Garden Shoin"
  COURT_VISUAL_JAPANESE_1_G1_DESC: "A serene tatami chamber where the lord receives guests beside painted screens and a quiet garden."
```

**Elder Events (长者事件)**:
```yaml
l_english:
  elder_events.1000.t: "Withering Mind"
  elder_events.1000.desc: "My beloved [elder.GetFirstNameNoTooltip] looked at me with confusion today, unable to recall my name..."
  elder_events.1100.t: "Fragile Bones"
  elder_events.1100.desc: "As I was walking down the stairs, my [elder.GetFirstNameNoTooltip] suddenly stumbled and fell..."
```

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
| `binaries/PDXSDK.dll` | 2.40 MB | Paradox SDK 库 (替代 pops_api.dll) |
| `binaries/checksum.txt` | 34 B | 校验和: `2a2e8b0448c7ef8afedb7a50a8aee575` |
| `launcher/launcher-installer-windows_2026.4.1.exe` | 167.94 MB | 新版启动器 (2026.1.1 → 2026.4.1) |

### 8.2 删除文件

| 文件 | 大小 | 说明 |
|------|------|------|
| `binaries/pops_api.dll` | 5.04 MB | 已移除 (被 PDXSDK.dll 替代) |

---

## 九、游戏平衡 (Defines) 变化

### 9.1 定义文件对比

**核心定义文件位置**:
- `game/common/defines/00_defines.txt` - 1.18.4 (1796 行) vs 1.19.0 (1827 行)
- `game/common/defines/jomini/portraits.txt` - 新增

### 9.2 关键定义差异

**NGame (游戏设置)**:
```yaml
NGame = {
    END_DATE = "1453.1.1"  # 保持不变
    GAME_SPEED_TICKS = { 2 1 0.5 0.2 0.0 }  # 保持不变
    LAG_DECREASE_SPEED_DAYS = 15  # 保持不变
    LAG_PAUSE_DAYS = 30  # 保持不变
    MULTIPLAYER_EVENT_TIME_OUT = 90  # 保持不变
    COURT_EVENT_TIME_OUT = 180  # 保持不变
    BENCHMARK_VIEWS_TEST_DURATION = 135  # 保持不变
    BENCHMARK_INTERFACE_INTERVAL = 5.0  # 保持不变
    MERIT_GUI_UPDATE_INTERVAL = 60  # 保持不变
}
```

**NCharacter (角色属性)**:
```yaml
NCharacter = {
    # 年龄设置
    MALE_RANDOM_AGE_BASE = 16
    MALE_RANDOM_AGE_SPAN = 20
    FEMALE_RANDOM_AGE_BASE = 16
    FEMALE_RANDOM_AGE_SPAN = 16

    # 技能范围
    RANDOM_CHARACTER_DIPLOMACY_MIN = 0
    RANDOM_CHARACTER_DIPLOMACY_MAX = 10
    # ... 其他技能相同

    # 健康
    RANDOM_CHARACTER_MIN_HEALTH = 4.0
    RANDOM_CHARACTER_MAX_HEALTH = 5.0
    RANDOM_CHARACTER_AGE_MIN_HEALTH = 2.5

    # 压力
    MAX_STRESS_LEVEL = 3
    STRESS_PER_LEVEL = 100

    # 恐惧
    MAX_DREAD = 100
    BASE_DREAD = 0
    DREAD_MONTHLY_CHANGE = 0.5

    # 暴政
    MAX_TYRANNY = 1000
    TYRANNY_MONTHLY_CHANGE = -0.25

    # 年龄阈值
    TODDLER_AGE = 3
    CHILDHOOD_AGE = 6
    ADOLESCENCE_AGE = 12
    MALE_ADULT_AGE = 16
    FEMALE_ADULT_AGE = 16
    MALE_ELDERLY_AGE = 50
    FEMALE_ELDERLY_AGE = 50
}
```

**NSkills (技能上限)**:
```yaml
NSkills = {
    MAX_DIPLOMACY = 100
    MAX_MARTIAL = 100
    MAX_STEWARDSHIP = 100
    MAX_INTRIGUE = 100
    MAX_LEARNING = 100
    MAX_PROWESS = 100  # 新增 - 威望技能
}
```

**NPortraits (肖像设置)** - 新增文件:
```yaml
NJominiPortraits = {
    DEFAULT_PORTRAIT_GROUP = "human"
    CHILDGENERATOR_NUM_GENERATIONS = 4
    CHILDGENERATOR_GENERATED_PER_GENERATION = 6
    CHILDGENERATOR_PORTRAIT_TYPES = { "male" "female" }
    PORTRAIT_CACHE_EXPIRE_FRAMES = 30

    ACCESSORY_PREFIXES_BLOCK_0 = {
        "female_clothing" "male_clothing" "female_clothes" "male_clothes"
    }
    ACCESSORY_PREFIXES_BLOCK_1 = {
        "female_headgear" "male_headgear" "f_headgear" "m_headgear"
    }
    ACCESSORY_PREFIXES_BLOCK_2 = {
        "female_cloaks" "male_cloaks" "male_capes" "f_cloak" "m_cloak"
    }
    ACCESSORY_PREFIXES_BLOCK_3 = {
        "female_legwear" "male_legwear" "f_legwear" "m_legwear"
    }
}
```

---

## 十、历史数据 (History) 变化

### 10.1 新增中国省份历史

文件: `game/history/provinces/h_china.txt` (5807 行)

新增大量中国地区的省份定义:
- 吐浑 (tuyuhun) 文化
- 汉 (han) 文化
- 多种宗教: zhengyi, daoxue, dhyana, sukhavati 等

```yaml
# 示例省份
9472 = {  # Aksay (Gonghe)
    culture = tuyuhun
    religion = tengri_pagan
    holding = tribal_holding
}

9770 = {  # Bazhou (Huacheng)
    culture = han
    religion = zhengyi
    holding = castle_holding
}

9750 = {  # Kaizhou (Kaijiang)
    culture = han
    religion = jingxue
    holding = castle_holding
    1000.1.1 = { religion = daoxue }  # 宗教随时间变化
}
```

### 10.2 新增越南/大理省份

文件: `game/history/provinces/k_viet.txt` (2360 行) 和 `k_dali.txt` (5.36 KB)

---

## 十一、变更分布统计

### 11.1 按目录分布

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

## 十二、核心变更总结

### 12.1 主要新功能

| 序号 | 功能 | 描述 |
|------|------|------|
| 1 | **宗教系统重构** | 从扁平 doctrines/ 目录转换为模块化的 doctrine_types/ + doctrine_group_types/ + holy_site_types/ + religion_types/ 结构 |
| 2 | **PDX Account 登录系统** | 完整的 Paradox 账户登录/注册 UI，支持云存档和多人游戏 |
| 3 | **Ledger 窗口系统** | 246KB 的复杂统计信息界面，显示战争、文物、爵位等 |
| 4 | **骑士徽章系统扩展** | 48+ 新图标，支持更多骑士个性化定制 |
| 5 | **长者/老龄化事件系统** | "Withering Mind" 等新特质相关事件，增加老龄化深度 |
| 6 | **中国风格庭院资产** | 完整的中国宫廷场景支持，100+ 新图形资源 |
| 7 | **宠物系统** | 猫狗宠物 Artifact 图标 |
| 8 | **额外原声带** | 36.22 MB 新音乐 |
| 9 | **圣地系统独立化** | 3542 行定义所有宗教的圣地 |
| 10 | **宗教家族系统** | 4 个家族 (rf_abrahamic, rf_eastern, rf_sinitic, rf_pagan) |

### 12.2 性能/技术变更

| 项目 | 1.18.4 | 1.19.0 | 变更说明 |
|------|--------|--------|----------|
| 引擎版本 | titus/release/1.18.2 | titus/release/1.19.0 | 主要版本升级 |
| SDK | pops_api.dll | PDXSDK.dll | 替换 |
| 启动器 | 2026.1.1 | 2026.4.1 | 升级 |
| 游戏定义行数 | 1796 | 1827 | +31 行 |
| 宗教文件数 | ~15 | ~60 | +45 文件 |

### 12.3 对玩家影响

1. **宗教系统更丰富**: 更多宗教类型 (50 个)，更多圣地选择
2. **UI 更完善**: 账户系统，统计界面 (Ledger)
3. **图形提升**: 中国宫廷风格，骑士徽章
4. **音效增加**: 新增音乐内容
5. **宠物陪伴**: 猫狗宠物

### 12.4 对 MOD 作者影响

1. **宗教系统重构**: 旧版 mod 的 doctrine 路径需要适配新结构
2. **新的分组机制**: doctrine_group_types 引入了新的分组方式
3. **holy_site_types**: 圣地定义现在独立
4. **religion_types**: 每个宗教独立文件

---

## 附录 A: 文件路径速查

### 宗教系统
| 类型 | 1.19.0 路径 |
|------|--------------|
| 教条类型 | `game/common/religion/doctrine_types/*.txt` |
| 教条分组 | `game/common/religion/doctrine_group_types/00_doctrine_group_types.txt` |
| 圣地类型 | `game/common/religion/holy_site_types/00_holy_site_types.txt` |
| 宗教家族 | `game/common/religion/religion_family_types/00_religion_family_types.txt` |
| 宗教定义 | `game/common/religion/religion_types/00_*.txt` |

### UI 系统
| 类型 | 路径 |
|------|------|
| PDX Account | `game/gui/pdx_account/*.gui` |
| Ledger | `game/gui/window_ledger.gui` |
| Accolade 选择 | `game/gui/window_accolade_attribute_selection.gui` |

### 游戏数据
| 类型 | 路径 |
|------|------|
| 长者事件 | `game/events/elder_events.txt` |
| 骑士权限 GUI | `game/common/scripted_guis/knight_permissions_sguis.txt` |
| 决策修饰符 | `game/common/modifiers/decision_modifiers.txt` |

---

## 附录 B: 生成信息

| 项目 | 内容 |
|------|------|
| 报告生成时间 | 2026-05-03 |
| 数据来源 | compare_versions.py 自动分析 + 源代码深度审查 |
| 分析模型 | MiniMax-M2.7 (minimax-cn-coding-plan/MiniMax-M2.7) |
| 协作人 | XenoAmess |