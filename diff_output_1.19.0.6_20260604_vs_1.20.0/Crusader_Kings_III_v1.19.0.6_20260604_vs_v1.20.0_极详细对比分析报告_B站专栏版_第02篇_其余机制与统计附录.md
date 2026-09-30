# CK3 1.19.0.6 → 1.20.0 极详细对比分析报告（2/4）：其余机制与统计附录

比较方向：旧目录 Crusader Kings III_1.19.0.6_20260604 → 新目录 Crusader Kings III_1.20.0。本文分析的是用户指定的两份本地文件快照，所有玩法结论以这两份代码为依据。未核验它们是否与发行平台原始安装包完全一致，因此不能将本地特有脚本自动当作官方更新公告。

**版本标识特别说明：新版目录名为 1.20.0，但 launcher/launcher-settings.json 内部记录为 1.20.0.2 (Crozier)；旧版记录为 1.19.0.6 (Scribe)。本文沿用用户指定目录名作为报告标题，实际证据对应下列分支、提交及内部版本号。**

## 版本基本信息

- **游戏分支**:
  - 旧版本: q2-26/fix/dlc_fix
  - 新版本: release/1.20.0

- **游戏提交**:
  - 旧版本: 6b540d23dbb0ae5f6a2ccc155338feabbaf64bbc
  - 新版本: f3f2d8163f60c70685010ca1441d93781aaeb5e7

- **引擎分支**:
  - 旧版本: titus/release/1.19.0
  - 新版本: titus/release/1.20.0

- **引擎提交**:
  - 旧版本: dd929f86eb389a5a01102593e080f181b5c01986
  - 新版本: 08d257dc90e97970ad3aeeaea5c56e13c40810d4

## 整体差异统计总览

- **新增文件**: 3248

- **删除文件**: 218

- **修改文件**: 7707

- **未变化文件**: 41685

- **旧版文件总数**: 49610

- **新版文件总数**: 52640

- **文件总数变化**: +3030

共有 11173 个路径发生内容或存在性变化。新增与删除按路径统计，没有把重命名、迁移或拆分文件当作同一路径；所以“删除文件”不直接等于删除功能。修改以 SHA-256 内容差异判定，未把时间戳变化计为修改。

## 分析覆盖

- **候选文本文件数**: 7765

- **已分析文本文件数**: 7727

- **跳过文本文件数**: 38

- **变化二进制文件数**: 3408

- **未复核文本文件数**: 7689

“已分析文本文件数”是脚本完整提取增删行和差异块的数量；“LLM复核文件数”是本报告实际检查过关键差异或定义的文件数量，见末尾。复核是有明确主题的源代码审查，部分大文件只审查相关定义及调用，不能理解为逐行验证整个文件。附录中的自动清单也不增加语义复核数量。

扫描包括新增、删除与修改的文本；未设置文件数量上限。排除 .git、.idea、.vscode、.ruff_cache、__pycache__ 目录及符号链接。文本默认严格 UTF-8，并识别 BOM；38 个变化的历史文件未通过解码，仍计入字节级差异。补查时只以 ASCII 语句及非 ASCII 字节转义核对明确规则，未猜测编码、未丢弃非法字节。扫描 issues 共 112 条，其中包含未变化文件的解码诊断，不能写成 112 个变化文本全部漏分析。

正文的“代码事实”直接对应脚本、配置或资源；“影响推断”说明它在给定条件下可能影响玩法；“待运行验证”保留引擎解释、事件链和实际 UI 行为的不确定性。没有执行 CK3、读取存档或进行性能跑分。


## 分卷与本篇范围

本篇为四篇系列的第 2 篇，内容范围：第 23—40 章及附录 A.1—A.5：修会、兵种、研究计谋、学识、宗族传承、继承与任命、东亚、帝国规则、AI、小改动、历史、资源、验证建议，以及全局统计、解码限制和实际复核清单。

上面的版本信息、扫描统计和末尾的 76 个 LLM复核文件均为原分析的全局口径，不是本篇新增复核的数量。拆分只调整发布篇幅，未扩大语义分析覆盖，未删去原报告的代码证据或限制说明。

## 23. 军事骑士团与隐修修会分开

代码事实：旧 holy_order_government 保留，并增加 military_holy_order 标记；新增 monastic_holy_order_government（简体中文本地化为“隐修修会”）。隐修修会没有配偶或议会、不采用常规婚姻目标，只支持教会地产；学习生活方式经验 +25%，骑士、兵士数量及规模限制修正 -100。它仍带 holy_order 标记，所以不是玩家可选的神权角色通用替代品。

create_holy_order_monastic_decision 新增：显示要求有地、至少公爵、Faith 满足 monasticism 判断且操作者未已经赞助同类隐修修会；已有军事骑士团赞助身份不阻止另建隐修修会。执行要求成年、和平、有合格教会租赁地点；玩家虔诚等级至少 3，AI 至少 1；冷却 10 年，成本根据是否有国库支付 gold 或 treasury，并支付虔诚。

拥有 By God Alone 时还要求自身神权政体或有教士代理人；无 DLC 分支没有在这一处增加同样条件。军团创建入口也被改写，不能仅按旧“国王可创团”的口诀判断。

借款入口现在检查军事骑士团标记，隐修修会不是同样的借款来源。取消租约入口改为年龄至少 12 和和平等条件，并增加相应虔诚成本及局势催化剂。定义中的最低赞助等级由 4 调至 3，也不能替代各决议的其他要求。

影响推断：宗教组织分成军事与修道两条路线，经济、招募、信仰发展用途需要分开评估。军力限制是隐修修会本身的修正，不能理解为玩家创建后自身兵士全部消失。

**新版证据**: `game/common/governments/00_government_types.txt`，第 401—445 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
monastic_holy_order_government = {
	government_rules = {
		council = no
		court_generate_spouses = no
		inherit_from_dynastic_government = no
		allow_accolades = no
	}

	character_modifier = {
		monthly_learning_lifestyle_xp_gain_add = 25
		knight_limit = -100
		men_at_arms_cap = -100
		men_at_arms_limit = -100
	}

	court_generate_commanders = 0

	ai = {
		arrange_marriage = no
		use_goals = no
		use_scripted_guis = no
		perform_religious_reformation = no
		use_legends = no
	}

	valid_holdings = { church_holding }

	# Use flags instead of has_government for moddability if possible (i.e., wherever not visible to the player).
	flags = {
		government_uses_crown_authority
		cannot_be_vassal_or_liege
		government_is_holy_order
		government_is_monastic_holy_order
	}

	mechanic_type = holy_order

	# prevent barons holding temple baronies from randomly getting holy order gov type
	can_get_government = {
		primary_title = {
			is_holy_order = yes
		}
	}

	color = hsv{ 0.00 0.00 0.66 }
~~~

该定义完整范围为第 401—448 行；节选在上述位置截断。本文结论所需的其他条件另以正文或补充片段说明。

**新版证据**: `game/common/decisions/00_holy_order_decisions.txt`，第 603—621 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	cooldown = { years = 10 }

	is_shown = {
		is_landed = yes
		highest_held_title_tier >= tier_duchy
		faith ?= {
			faith_has_monasticism_trigger = yes
			NOT = {
				any_faith_holy_order = {
					#Can be military patron and found monastic order
					leader ?= {
						government_has_flag = government_is_monastic_holy_order
					}
					holy_order_patron ?= root
				}
			}
			
		}
	}
~~~

**新版证据**: `game/common/decisions/00_holy_order_decisions.txt`，第 678—705 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
		trigger_if = {
			limit = {
				has_pam_dlc_trigger = yes
			}
			OR = {
				custom_tooltip = {
					text = government_is_theocracy
					government_has_flag = government_is_theocracy
				}
				custom_tooltip = {
					text = has_clerical_puppet_tt
					OR = {
						exists = root.puppet:theological_agent_puppet
						exists = root.puppet:external_theological_agent_puppet
					}
				}
			}
		}
		
		trigger_if = {
			limit = {
				is_ai = yes
			}
			piety_level >= 1
		}
		trigger_else = {
			piety_level >= 3
		}
~~~

## 24. 骑士团兵种：旧重步兵改名与新重骑兵

代码事实：旧 teutonic_knights（heavy_infantry）迁移为 order_serjeants，伤害仍 36，坚韧 26 → 24，单队仍 100；新增西方基督教 Rite、quilted_armor 革新及没有 strength_in_numbers_heavy_maa_ban 的招募条件。

新 order_knights 为重骑兵，伤害 112、坚韧 36、追击 20、单队 50；平原与旱地伤害 +30，丘陵 -20，山地/沙漠山地/湿地 -75，湿地另有坚韧及追击 -10；有冬季惩罚。招募要求西方基督教 Rite、arched_saddle 革新、没有重兵士禁用参数。

两个兵种都是 special_recruit_only = yes，不是所有世俗角色获得创新后可以直接在普通兵士菜单无限招募。112 与 36 是两种单位的基础单体伤害，队伍人数、克制、地形及修正不同，不能据此宣布总战力直接三倍。

影响推断：重步兵同类基础坚韧小幅下降；新重骑兵适合平原/旱地但地形代价明确。是否能取得、谁能扩编和实际骑士团构成，需要结合招募调用与运行局面。

**旧版证据**: `game/common/men_at_arms_types/00_holy_order_maa_types.txt`，第 19—28 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
teutonic_knights = { # Actually all Christian knightly orders, not just the Teutons.
	type = heavy_infantry

	special_recruit_only = yes

	# Slightly stronger than normal Heavy Infantry MaA, to represent zeal & dedication to the cause.
	damage = 36 
	toughness = 26
	pursuit = 0
	screen = 0
~~~

**新版证据**: `game/common/men_at_arms_types/00_holy_order_maa_types.txt`，第 19—50 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
order_serjeants = { # for all Christian knightly orders
	type = heavy_infantry

	special_recruit_only = yes

	# Slightly stronger than normal Heavy Infantry MaA, to represent zeal & dedication to the cause.
	damage = 36 
	toughness = 24
	pursuit = 0
	screen = 0

	buy_cost = { gold = heavy_infantry_recruitment_cost }
	low_maintenance_cost = { gold = heavy_infantry_low_maint_cost }
	high_maintenance_cost = { gold = heavy_infantry_high_maint_cost }
	provision_cost = @provisions_cost_infantry_expensive
		
	counters = {
		pikemen = 1
		peasant_militia = 2
	}

	can_recruit = {
		rite = {
			rite_has_doctrine = special_doctrine_is_western_christian_faith
		}
		culture = {
			has_innovation = innovation_quilted_armor
		}
		NOT = {
			culture = { has_cultural_parameter = strength_in_numbers_heavy_maa_ban }
		}
	}
~~~

**新版证据**: `game/common/men_at_arms_types/00_holy_order_maa_types.txt`，第 69—109 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
order_knights = {
	type = heavy_cavalry # for all Christian knightly orders

	special_recruit_only = yes

	# Slightly stronger than normal Heavy Cavalry MaA, to represent zeal & dedication to the cause.
	damage = 112
	toughness = 36
	pursuit = 20
	screen = 0

	terrain_bonus = {
		plains = { damage = 30 }
		drylands = { damage = 30 }
		hills = { damage = -20 }
		mountains = { damage = -75 }
		desert_mountains = { damage = -75 }
		wetlands = { damage = -75 toughness = -10 pursuit = -10 }
	}

	counters = {
		archers = 1
		gunpowder = 1
	}

	can_recruit = {
		rite = {
			rite_has_doctrine = special_doctrine_is_western_christian_faith
		}
		culture = {
			has_innovation = innovation_arched_saddle
		}
		NOT = {
			culture = { has_cultural_parameter = strength_in_numbers_heavy_maa_ban }
		}
	}

	winter_bonus = {
		normal_winter = { damage = -10 toughness = -5 }
		harsh_winter = { damage = -20 toughness = -10 }
	}
~~~

## 25. 新研究计谋与学者特质：旧能力不是被删除

代码事实：新增 study_faith，以他人为研究目标、非秘密、不使用抵抗、基础进度目标 365、最大成功 95、最小 5、冷却 12 个月；入口成年且未监禁，不能研究自己当前 Faith、不能同时进行第二项同类研究，已经完全了解目标 Rite 也不允许。有效性包括自己至少伯爵、非无能及外交距离检查。

新增 study_scripture 为个人、自我目标计谋，年龄至少 12、非监禁/无能，旅行期间冻结；基础进度目标 300。学识、相关 Tenet、住所及上级学识等可影响其预测/成功计算。365 或 300 是基础进度目标，不保证实际总时长就是相同数量的天数。

旧 scholar 特质改名为 erudite：学识 +3、己方个人与敌对计谋成功率 +10、发展增长 +15%、发展衰退 -15%、伯爵领肥力增长 +15% 等主要修正保留；特质迁移表明确 scholar = erudite。另新增 lifestyle_scholar，基础学识 +1、生活方式经验 +10%，并有 20/40/60/80/100 经验档与依赖 scholasticism 的附加修正。

影响推断：既有学识树终点被迁移，额外又出现渐进的研究成长路线，不能写成“删除学者特质和全部学者奖励”。存档里如何执行迁移表需要载入验证；lookup 的存在仅提供了明确兼容处理入口。

**新版证据**: `game/common/schemes/scheme_types/study_faith_scheme.txt`，第 1—38 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
study_faith = {
	# Basic Setup
	skill = learning
	desc = study_faith_desc_general
	success_desc = "STUDY_FAITH_SUCCESS_DESC"
	icon = icon_scheme_study_faith
	illustration = "gfx/interface/illustrations/event_scenes/pam_romanesque_church_interior.dds"
	target_type = character
	is_secret = no
	is_basic = yes
	cooldown = { months = 12 }
	
	# Parameters
	speed_per_skill_point = t1_spsp_owner_value
	spymaster_speed_per_skill_point = 0
	uses_resistance = no
	base_progress_goal = 365
	base_maximum_success = 95
	minimum_success = 5
	
	# Core Triggers
	allow = {
		age >= 16
		NOR = {
			faith = scope:target.faith # You can't study within your own faith
			custom_description = { # Should not be able to study more than a single faith at once
				text = scheme_target_more_than_one_faith_to_study_scheme
				any_scheme = {
					type = study_faith
				}
			}
			knows_rite_level = {
				target = scope:target.rite
				value >= 1 # you know every detail about the target faith
			}
		}

		is_imprisoned = no
~~~

**新版证据**: `game/common/schemes/scheme_types/pam_study_scheme.txt`，第 8—39 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	category = personal
	target_type = character

	is_secret = no
	is_basic = yes

	hide_target_name = yes
	freeze_scheme_when_traveling = yes

	# Parameters
	speed_per_skill_point = -1
	spymaster_speed_per_skill_point = 0
	uses_resistance = no
	base_progress_goal = 300
	base_maximum_success = 95
	minimum_success = 5

	# Core Triggers
	allow = {
		age >= 12
		is_imprisoned = no
		is_incapable = no
	}

	valid = {
		scope:target = scope:owner
		NOT = {
			has_character_modifier = partially_mute_modifier
		}
		is_imprisoned = no
		is_incapable = no
	}
~~~

**完整文件差异**: `game/common/traits/trait_conversion.lookup`。

~~~diff
--- 旧版/game/common/traits/trait_conversion.lookup
+++ 新版/game/common/traits/trait_conversion.lookup
@@ -18,4 +18,7 @@
 archer_3 = tourney_participant
 reveler_1 = lifestyle_reveler
 reveler_2 = lifestyle_reveler
 reveler_3 = lifestyle_reveler
+scholar = erudite
+eunuch = eunuch_1
+poet = lifestyle_poet
~~~

**旧版证据**: `game/common/traits/00_traits.txt`，第 1795—1805 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
scholar = {
	category = lifestyle

	learning = 3
	owned_personal_scheme_success_chance_add = 10
	owned_hostile_scheme_success_chance_add = 10
	development_growth_factor = 0.15
	development_decline_factor = -0.15
	county_fertility_growth_mult = 0.15
	
	ruler_designer_cost = 50
~~~

**新版证据**: `game/common/traits/00_traits.txt`，第 1798—1808 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
erudite = {
	category = lifestyle

	learning = 3
	owned_personal_scheme_success_chance_add = 10
	owned_hostile_scheme_success_chance_add = 10
	development_growth_factor = 0.15
	development_decline_factor = -0.15
	county_fertility_growth_mult = 0.15

	ruler_designer_cost = 50
~~~

**新版证据**: `game/common/traits/00_traits.txt`，第 17955—17990 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	minimum_age = 16
	category = fame

	learning = 1

	monthly_lifestyle_xp_gain_mult = 0.1

	ruler_designer_cost = 15

	rite_modifier = {
		parameter = scholasticism_is_holy
		monthly_piety_gain_mult = 0.1
		zealot_opinion = 10
		learning = 1
	}

	track = {
		20 = {
			monthly_lifestyle_xp_gain_mult = 0.05
			rite_modifier = {
				parameter = scholasticism_is_holy
				monthly_piety_gain_mult = 0.1
				zealot_opinion = 10
				learning = 1
			}
		}
		40 = {
			monthly_lifestyle_xp_gain_mult = 0.05
			clergy_opinion = 5
			rite_modifier = {
				parameter = scholasticism_is_holy
				monthly_piety_gain_mult = 0.1
				zealot_opinion = 10
				learning = 1
			}
		}
~~~

## 26. 学识生活方式有具体平衡变化

代码事实：prophet_perk 在非 merit 政体分支中，monthly_piety_gain_per_knight_mult 从 0.02 改为 0.01，并移除这个块的 faith_creation_piety_cost_mult = -0.5。新版效果描述增加教义解锁、符合 DLC 等条件的其他用途；不能继续宣称此节点仍直接提供原来 -50% 创建信仰成本。完整新收益需沿描述参数消费者核对，本章不将其简单判成整体削弱。

scholarly_circles_perk 的 learning_per_piety_level = 1 改为 learning_per_prestige_level = 1，无地冒险者抵消项也同步迁移。触发来源从虔诚等级改为威望等级，这是实质变化，不是纯翻译。不同角色威望/虔诚分布不同，收益高低不能一概而论。

Scholarship 树终点 scholar_perk 迁移为 erudite_perk；神权角色新增研究圣典阶段时长、异 Faith 伯爵领好感及少数群体税贡等专用修正。Wilwatikta Palace 的宗教创建成本修正由旧 faith_creation_piety_cost_mult = -0.2 改为 rite_creation_piety_cost_mult = -0.1：对象和数值都变了，不能继续套用旧 -20%。

影响推断：准备宗教创建及学识成长的节点选择需要重新比较；原以虔诚等级获得学识的世俗角色，会更看重威望等级。不能将这些条件化变化扩展为整棵学识树统一增强或削弱。

**旧版证据**: `game/common/lifestyle_perks/00_learning_3_theology_tree_perks.txt`，第 183—194 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	government_character_modifier = {
		flag = government_has_merit
		invert_check = yes
		monthly_piety_gain_per_knight_mult = 0.02
		faith_creation_piety_cost_mult = -0.5
	}

	government_character_modifier = {
		flag = government_has_merit
		monthly_merit_mult = 0.2
		stress_loss_per_piety_level = 0.1
	}
~~~

**新版证据**: `game/common/lifestyle_perks/00_learning_3_theology_tree_perks.txt`，第 208—223 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	government_character_modifier = {
		flag = government_has_merit
		invert_check = yes
		monthly_piety_gain_per_knight_mult = 0.01
	}

	government_character_modifier = {
		flag = government_has_merit
		monthly_merit_mult = 0.2
		stress_loss_per_piety_level = 0.1
	}
	
	effect = {
		custom_description_no_bullet = {
			text = prophet_perk_unlock_tenets_effect
		}
~~~

**旧版证据**: `game/common/lifestyle_perks/00_learning_2_scholarship_tree_perks.txt`，第 255—263 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	character_modifier = {
		learning_per_piety_level = 1
	}
	government_character_modifier = {
		flag = government_is_landless_adventurer
		enemy_terrain_advantage = -0.5
		knight_effectiveness_per_learning = 0.005
		learning_per_piety_level = -1
	}
~~~

**新版证据**: `game/common/lifestyle_perks/00_learning_2_scholarship_tree_perks.txt`，第 268—276 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	character_modifier = {
		learning_per_prestige_level = 1
	}
	government_character_modifier = {
		flag = government_is_landless_adventurer
		enemy_terrain_advantage = -0.5
		knight_effectiveness_per_learning = 0.005
		learning_per_prestige_level = -1
	}
~~~

**完整文件差异**: `game/common/buildings/cp8_special_buildings.txt`。

~~~diff
--- 旧版/game/common/buildings/cp8_special_buildings.txt
+++ 新版/game/common/buildings/cp8_special_buildings.txt
@@ -645,9 +645,9 @@
 	can_construct_potential = { building_requirement_tribal = no }
 	can_construct = { building_requirement_tribal = no }
 	cost_gold = 1000
 	county_holder_character_modifier = {
-		faith_creation_piety_cost_mult = -0.2
+		rite_creation_piety_cost_mult = -0.1
 		monthly_dynasty_prestige_mult = 0.05
 		tributary_opinion = 5
 	}
 	county_modifier = {
~~~

## 27. 新宗族传承：五级 PAM 路线

代码事实：09_pam_dynasty_perks.txt 新增 pam_legacy_1 至 pam_legacy_5。选择资格要求 By God Alone；默认宗族首领为基督教或已拥有第一级，也可通过不限宗族传承规则的替代分支。

第一级：起始精神满足度 +10、满足度损失倍率 -10%，获得时对满足指定 available/advanced_ruler 条件的现有宗族成员立即加 10。第二级：教会地产建筑/地产建造金钱成本各 -15%，并附相关请求/国库效果描述。第三级：个人 Tenet 槽 +1、圣战骑士团雇佣成本 -20%。第四级：theocracy 与 ecclesiastical 税贡倍率各 +10%，附候选和枢机相关描述。第五级：piety_level_impact_mult +25%，附 papabile 与教会塑造效果描述。

影响推断：家系可沿精神满足度、宗教建设、个人教义与教士政治长期投资。修正和描述型参数应分开：代码明确的百分比可确认，而描述所指的全部互动效果尚未逐项追踪。

**新版证据**: `game/common/scripted_triggers/pam_scripted_triggers.txt`，第 6751—6762 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
eligible_for_pam_legacy_trigger = {
	has_pam_dlc_trigger = yes
	OR = {
		game_rule_unrestricted_dynasty_legacies_trigger = yes
		dynasty = {
			OR = {
				dynast = { faith.religion = religion:christianity_religion }
				has_dynasty_perk = pam_legacy_1
			}
		}
	}
}
~~~

**新版证据**: `game/common/dynasty_perks/09_pam_dynasty_perks.txt`，第 65—107 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text

	can_be_picked = { eligible_for_pam_legacy_trigger = yes }

	effect = {
		custom_description_no_bullet = { text = pam_legacy_3_evangelize_effect }
	}

	character_modifier = {
		personal_tenet_slot_add = 1
		holy_order_hire_cost_mult = -0.2
	}
}

pam_legacy_4 = { # Mitre and Crosier
	legacy = pam_legacy_track

	can_be_picked = { eligible_for_pam_legacy_trigger = yes }

	effect = {
		custom_description_no_bullet = { text = pam_legacy_4_candidacy_effect }
		custom_description_no_bullet = { text = pam_legacy_4_cardinal_effect }
	}

	character_modifier = {
		theocracy_government_tax_contribution_mult = 0.1
		ecclesiastical_government_tax_contribution_mult = 0.1
	}
}

pam_legacy_5 = { # Princes of the Church
	legacy = pam_legacy_track

	can_be_picked = { eligible_for_pam_legacy_trigger = yes }

	effect = {
		custom_description_no_bullet = { text = pam_legacy_5_papabile_effect }
		custom_description_no_bullet = { text = pam_legacy_5_shape_church_effect }
	}

	character_modifier = {
		piety_level_impact_mult = 0.25
	}
}
~~~

## 28. 法律结构拆分与初始长子继承规则

代码事实：新增 7 个 law_groups 文件，法律条目通过 law_group_type 与 index 关联。旧法律组属性迁移和缩进重排产生大量增删行，不能把每个变化行都算成继承平衡更新。

已确认的实际变化：high_partition_succession_law 的 should_start_with 在 heraldry 等条件之外新增 NOT innovation_primogeniture；single_heir_succession_law 的 should_start_with 从只检查历史单一继承权限改为“历史权限或文化有 innovation_primogeniture”。这两个分支共同改变初始化时的默认选择。

影响推断：具备长子继承革新的文化在满足其他适用条件时，更可能初始化为单一继承路线，而不是先落入高分割。should_start_with 是开局/初始化选择，不证明中途获得革新后所有现存头衔立即自动换法；切换法律的有效性、成本和已有法处理是另一组条件。

大量 government_allows = administrative / government_is_administrative 检查改用 government_has_mechanic = administrative，作用于法律和同步判断。行政机制并未因旧字段删除而被移除。

**旧版证据**: `game/common/laws/00_succession_laws.txt`，第 52—62 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
					government_has_flag = government_is_feudal
					culture = {
						NOR = {
							has_innovation = innovation_hereditary_rule
							has_innovation = innovation_heraldry
						}
					}
				}
				government_has_flag = government_is_tribal
			}
		}
~~~

**新版证据**: `game/common/laws/00_succession_laws.txt`，第 41—54 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
				government_has_flag = government_is_feudal
				culture = {
					NOR = {
						has_innovation = innovation_hereditary_rule
						has_innovation = innovation_heraldry
					}
				}
			}
			government_has_flag = government_is_tribal
		}
	}
	succession = {
		order_of_succession = inheritance
		traversal_order = children
~~~

**旧版证据**: `game/common/laws/00_succession_laws.txt`，第 44—51 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
		should_start_with = {
			NOR = {
				historical_succession_access_single_heir_succession_law_trigger = yes
				historical_succession_access_single_heir_succession_law_youngest_trigger = yes
				historical_succession_access_single_heir_dynasty_house_trigger = yes
			}
			OR = {
				AND = {
~~~

**新版证据**: `game/common/laws/00_succession_laws.txt`，第 32—43 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	}
	should_start_with = {
		NOR = {
			historical_succession_access_single_heir_succession_law_trigger = yes
			historical_succession_access_single_heir_succession_law_youngest_trigger = yes
			historical_succession_access_single_heir_dynasty_house_trigger = yes
		}
		OR = {
			AND = {
				government_has_flag = government_is_feudal
				culture = {
					NOR = {
~~~

## 29. 权威同步与任命评分共享

代码事实：should_synchronize_liege_law 新增。它要求自己不是最高领主、与领主符合日本官僚制关系或同处行政机制，以及 use_same_authority_with_liege。各法律改为调用该判断；不能将它写成所有政体封臣必定同步领主法律。

admin_emperor 候选分新增 appointment_score_base。新共享函数包含威望/宗族威望（依赖候选评分法律）、影响力等级、宗族传承、家族抱负、负面特质及犯罪等因素。旧任命文件中删除的犯罪扣分在共享函数中仍存在，且按 state_rite 或最高领主 Rite 判定罪行。因此不能误判成“犯罪者任命不再扣分”。

共享基础分将若干 infirm 判断推广为 age_related_ailment 标记。缺陷特质、是否神职和特定继承法仍有不同条件。将它抽到基础分后，各调用方是否与旧版完全等价，需要比较完整最终分数，不能仅凭少了几百行宣布候选人普遍增强。

新增 clerical_christian 任命类型：不允许儿童、不用投资上限、allowed_candidate_tier = any、最高层头衔保持在一起、允许无地外部投资、有冷却；默认候选人包括持有者的议员、宫廷职位、直属下属和教会区域教士，未使用家族默认候选分类。它的评分中学识及教育有明确权重，武力相关分还依赖 Rite 是否重视军事教士。

**新版证据**: `game/common/scripted_triggers/00_law_triggers.txt`，第 126—141 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
should_synchronize_liege_law = {
	top_liege != this
	OR = {
		trigger_if = {
			limit = { realm_law_use_japanese_bureaucracy = yes }
			liege = { realm_law_use_japanese_bureaucracy = yes }
		}
		trigger_else = {
			government_has_mechanic = administrative
			top_liege = {
				government_has_mechanic = administrative
			}
		}
	}
	use_same_authority_with_liege = yes
}
~~~

**新版证据**: `game/common/succession_appointment/admin_emperor.txt`，第 5—13 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text

	candidate_score = {
		value = {
			add = appointment_score_base
			# AGE
			if = {
				limit = { age <= 5 }
				subtract = {
					value = 100
~~~

**新版证据**: `game/common/script_values/07_appointment_values.txt`，第 549—583 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	# RITE BASED
	if = {
		limit = {
			exists = top_liege.primary_title.state_rite
		}
		top_liege.primary_title.state_rite = {
			save_temporary_scope_as = target_rite
		}
	}
	else = {
		top_liege.rite = {
			save_temporary_scope_as = target_rite
		}
	}
	# CRIMINAL
	if = {
		limit = {
			has_trait = deviant
			trait_is_criminal_in_rite_trigger = { TRAIT = trait:deviant RITE = scope:target_rite GENDER_CHARACTER = root }
		}
		subtract = {
			value = appointment_score_crime_penalty
			desc = "deviant_and_criminal_desc"
		}
	}
	if = {
		limit = {
			has_trait = incestuous
			trait_is_criminal_in_rite_trigger = { TRAIT = trait:incestuous RITE = scope:target_rite GENDER_CHARACTER = root }
		}
		subtract = {
			value = appointment_score_crime_penalty
			desc = "incestuous_and_criminal_desc"
		}
	}
~~~

**新版证据**: `game/common/succession_appointment/clerical_christian.txt`，第 1—30 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
clerical_christian = {
	allow_children = no
	use_investment_cap = no
	allowed_candidate_tier = any
	keep_top_tier_titles_together = yes
	allow_out_of_realm_investment = landless
	cooldown = yes

	# An inherited clerical region leaves the realm if no counties overlap, unless its holder heads the faith

	# No family categories, because a clerical office is not an inheritance
	default_candidates = { holder_councilor holder_court_position direct_subject clerical_region_clergy clerical_region_clergy_councilor }

	candidate_score = {
		value = {
			# A see wants a scholar first, but not so much more than a diplomat that nothing else can compete.
			add = {
				value = learning
				desc = learning_skill_bonus_desc
			}

			if = { # Diplomacy skill
				limit = {
					diplomacy > 1
				}
				add = {
					value = diplomacy
					multiply = 0.8
					round = yes
					desc = diplomacy_skill_bonus_desc
~~~

## 30. 东亚行政、国教与丝路：可确认的变化

代码事实：日本政体与 Celestial 等行政检查改为 mechanic_type / government_has_mechanic；省份契约新增 province_civilian、province_military 标记。administrative 契约的一处 AI 同国教偏好检查由 faith = state_faith 改为 rite = state_rite，宗教一致性更细。

Celestial metropolitan 的 AI 距离检查从 subject 的 realm_to_title_distance_squared 改为 subject.capital_county 对领主 capital_county 的 squared_distance，阈值仍 60000。比较对象由领域到首都改为首都对首都，不能视作纯缩进迁移；阈值单位和最后效果未做实机测量。

丝路 adopt 创新中的 sinophilic 分支，旧检查 c_jingzhao 的文化已有革新；新检查 culture:han 或 h_china 当前持有者文化已有革新，同时保留 may_adopt_silk_road_innovations 与 DLC 条件。这避免把革新来源只绑定某一个伯爵领，但是否扩大/缩小具体局面的可获得集合取决于文化和皇帝状态。

自然灾害局势参与区域检查原仅比较首都县，新加入角色当前位置县或当前活动地点县，均使用可空比较 ?=。影响推断：旅行、参与活动及无固定首都的相关角色也可能匹配所在地区，不能只检查首都所在区域。

中国、日本人物历史的巨量变化包含宗教到 Rite 的字段迁移、日期与注释重排。全文行规模不证明同等规模的新增东亚人物；个别家系和首都规则变化见源码，未逐个历史角色解读。

**完整文件差异**: `game/common/scripted_triggers/tgp_silk_road_triggers.txt`。

~~~diff
--- 旧版/game/common/scripted_triggers/tgp_silk_road_triggers.txt
+++ 新版/game/common/scripted_triggers/tgp_silk_road_triggers.txt
@@ -34,10 +34,13 @@
 			this = culture_innovation:innovation_$INNOVATION$
 		}
 		# Sinophilic
 		AND = {
-			title:c_jingzhao.culture ?= { has_innovation = innovation_$INNOVATION$ }
 			has_cultural_parameter = may_adopt_silk_road_innovations
+			OR = {
+				culture:han ?= { has_innovation = innovation_$INNOVATION$ }
+				title:h_china.holder.culture ?= { has_innovation = innovation_$INNOVATION$ }
+			}
 		}
 	}
 	has_tgp_dlc_trigger = yes
 }
~~~

**完整文件差异**: `game/common/scripted_triggers/10_tgp_natural_disaster_triggers.txt`。

~~~diff
--- 旧版/game/common/scripted_triggers/10_tgp_natural_disaster_triggers.txt
+++ 新版/game/common/scripted_triggers/10_tgp_natural_disaster_triggers.txt
@@ -90,9 +90,13 @@
 
 tpg_character_in_any_situation_sub_region_trigger = {
 	any_situation_sub_region = {
 		any_situation_sub_region_county = {
-			root.capital_province.county = this
+			OR = {
+				root.capital_province.county ?= this
+				root.location.county ?= this
+				root.involved_activity.activity_location.county ?= this
+			}
 		}
 	}
 }
 
~~~

**旧版证据**: `game/common/subject_contracts/contracts/celestial.txt`，第 193—201 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
					if = {
						limit = {
							scope:subject = {
								realm_to_title_distance_squared = { target = scope:liege.capital_county value < 60000 }
							}
						}
						add = 3
					}

~~~

**新版证据**: `game/common/subject_contracts/contracts/celestial.txt`，第 195—203 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
					if = {
						limit = {
							scope:subject.capital_county = {
								squared_distance = { target = scope:liege.capital_county value < 60000 }
							}
						}
						add = 3
					}

~~~

## 31. 非宗教兵种限制：东方攻城与弩炮战象

代码事实：普通和东亚兵种文件将东方攻城文化检查统一到 culture_uses_eastern_siege_weapons_trigger。该函数不仅包含 Chinese、Korean、Japonic，还加入 Buyeo、Viet 文化传承。旧手工列举只含前三者的入口，实际允许范围因而有扩展；仍需满足对应攻城科技及其他招募条件。

ballista_elephant 新增 NOT strength_in_numbers_heavy_maa_ban 条件，其伤害 180、坚韧 75 等基础数值在已核对块中保留。影响推断：有相应文化重兵士禁用参数的角色不应继续绕过该限制招募弩炮战象；这不是全体战象的基础伤害削弱。

多个普通兵士入口从分别排除 nomad/herder 政体改为排除 government_is_in_steppe。它对现有带标记的政体及模组政体更通用；不能仅看到判断写法变短就认为游牧全面获得重兵士。

完整兵种收益还取决于队伍规模、补给、地形、克制与招募路径，本报告只对明确变化判定条件或数值。

**新版证据**: `game/common/scripted_triggers/10_tgp_triggers.txt`，第 1107—1115 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
culture_uses_eastern_siege_weapons_trigger = {
	OR = {
		has_cultural_pillar = heritage_chinese
		has_cultural_pillar = heritage_korean
		has_cultural_pillar = heritage_japonic
		has_cultural_pillar = heritage_buyeo
		has_cultural_pillar = heritage_viet
	}
}
~~~

**旧版证据**: `game/common/men_at_arms_types/10_tgp_maa_types.txt`，第 224—240 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
ballista_elephant = {
	type = elephant_cavalry
	
	damage = 180
	toughness = 75
	pursuit = 30
	screen = 20
	
	siege_value = 0.1

	can_recruit = {
		culture ?= { 
			has_innovation = innovation_elephantry 
			has_innovation = innovation_advanced_bowmaking
		}
		NOT = { is_landless_adventurer = yes }
	}
~~~

**新版证据**: `game/common/men_at_arms_types/10_tgp_maa_types.txt`，第 224—243 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
ballista_elephant = {
	type = elephant_cavalry
	
	damage = 180
	toughness = 75
	pursuit = 30
	screen = 20
	
	siege_value = 0.1

	can_recruit = {
		culture ?= { 
			has_innovation = innovation_elephantry 
			has_innovation = innovation_advanced_bowmaking
		}
		NOT = { is_landless_adventurer = yes }
		NOT = {
			culture = { has_cultural_parameter = strength_in_numbers_heavy_maa_ban }
		}
	}
~~~

## 32. 默认关闭的帝国信仰限制：创建入口确实接入

代码事实：新增 empire_faith_gate 游戏规则，默认 empire_faith_gate_off，另有 on 与 no_hof_exempt。它已被接入 rule_title_creation_imperial_power_projection_title_creation_trigger、相关 GUI、开局/年份/头衔事件，不能仅把它当作从未使用的闲置定义；但默认关闭意味着通常开局不会启用这一组新增条件。

适用政体为带 feudal、clan、tribal、japan_feudal 标记者；can_create_empire_faith_gate_trigger 要求 Faith 非 unreformed。教首审批路径：有精神教首时，教首对创建者好感 >0 且至少 50% 强力封臣对创建者好感 >0；世俗教首时可以自己就是教首或教首对自己好感 >0，仍要求相应强力封臣比例。无教首的免除选项只免相应审批路径，不能推成免除全部组织化信仰条件。

影响推断：在用户主动启用这项本地规则后，帝国创建准备会包含宗教认可和内部支持。它在本次快照中存在，但没有来源证明它是官方发行的新标准规则。本文单列以免把本地扩展误写成 1.20 的普遍默认行为。

**完整文件差异**: `game/common/game_rules/01_empire_faith_gate_rules.txt`。

~~~diff
--- 旧版/game/common/game_rules/01_empire_faith_gate_rules.txt
+++ 新版/game/common/game_rules/01_empire_faith_gate_rules.txt
@@ -0,0 +1,11 @@
+empire_faith_gate = {
+	categories = { titles tweaks }
+
+	default = empire_faith_gate_off
+
+	empire_faith_gate_on = {}
+
+	empire_faith_gate_no_hof_exempt = {}
+
+	empire_faith_gate_off = {}
+}
~~~

**新版证据**: `game/common/scripted_triggers/00_empire_faith_gate_triggers.txt`，第 27—54 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
# Subject governments: feudal, clan, tribal, Japan feudal and Soryo
# Not theocratic, ecclesiastical, adventurer, or republic
government_subject_to_faith_empire_trigger = {
	OR = {
		government_has_flag = government_is_feudal
		government_has_flag = government_is_clan
		government_has_flag = government_is_tribal
		government_has_flag = government_is_japan_feudal
	}
}

faith_allows_empire_trigger = {
	NOT = { faith = { has_doctrine_parameter = unreformed } }
}

# Rulers subject to the rule must have an organized faith, and other governments pass
can_create_empire_faith_gate_trigger = {
	trigger_if = {
		limit = {
			empire_faith_gate_enabled_trigger = yes
			government_subject_to_faith_empire_trigger = yes
		}
		custom_tooltip = {
			text = empire_faith_gate_organized_faith_required
			faith_allows_empire_trigger = yes
		}
	}
}
~~~

**新版证据**: `game/common/scripted_triggers/00_empire_faith_gate_triggers.txt`，第 251—305 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
		trigger_if = {
			limit = {
				faith = { has_doctrine = doctrine_spiritual_head }
				exists = faith.religious_head
			}
			custom_tooltip = {
				text = empire_faith_gate_hof_spiritual_good_terms
				faith.religious_head = {
					opinion = {
						target = root
						value > 0
					}
				}
			}
			custom_tooltip = {
				text = empire_faith_gate_powerful_vassals_approve
				any_powerful_vassal = {
					percent >= 0.5
					opinion = {
						target = root
						value > 0
					}
				}
			}
		}
		# Temporal head path
		trigger_else_if = {
			limit = {
				faith = { has_doctrine = doctrine_temporal_head }
				exists = faith.religious_head
			}
			OR = {
				custom_tooltip = {
					text = empire_faith_gate_hof_temporal_is_hof
					this = faith.religious_head
				}
				custom_tooltip = {
					text = empire_faith_gate_hof_temporal_good_terms
					faith.religious_head = {
						opinion = {
							target = root
							value > 0
						}
					}
				}
			}
			custom_tooltip = {
				text = empire_faith_gate_powerful_vassals_approve
				any_powerful_vassal = {
					percent >= 0.5
					opinion = {
						target = root
						value > 0
					}
				}
~~~

## 33. 同 Faith 多帝国竞争与解散帝国战争

代码事实：规则启用时，同 Faith 的独立帝国持有者会进入竞争判断，且检查适用政体、组织化信仰和霸权层级例外。这里计数的是其他合格帝国持有者，不是简单数一位角色手里有多少帝国头衔。

竞争修正分 1/2/3 档，月度合法性分别 -1/-2/-3。新进入竞争状态的事件会安排 1095 天后再处理修正，并为玩家设置 current_year + 3 的宽限变量；事件与 AI 绝罚/战争可用性判断的宽限不能混为一谈。既有状态重算、失去头衔和改变 Faith 有清理/刷新路径。

新增 dissolve_empire CB：要求规则已启用及相关绝罚能力、进攻方未被绝罚、防守方为同 Faith、独立、至少帝国且被绝罚等条件；AI 和较低阶玩家还有不同判断。胜利时销毁防守者所有 tier >= empire 的持有头衔，而不是把这些帝国转移给攻击者。次级王国/公国如何重新组织需要运行验证。

影响推断：争夺宗教首领认可可能延伸到帝国合法性与政治解体。它默认不生效，且销毁帝国与侵占帝国是不同战争目标，不能按普通征服预期收益。

**新版证据**: `game/events/empire_faith_gate_events.txt`，第 69—96 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
							add = 3
						}
					}
				}
				scope:efg_toast_other_emperor = { save_temporary_scope_as = efg_other_emperor }
				
				# Modifier is applied 3 years later via empire_faith_gate.0002.
				set_variable = {
					name = efg_modifier_pending_end_year
					value = {
						value = current_year
						add = 3
					}
				}
				trigger_event = { id = empire_faith_gate.0002 days = 1095 }
				send_interface_toast = {
					type = event_toast_effect_bad
					title = empire_faith_gate_contested_legitimacy_applied
					left_icon = scope:efg_other_emperor
					right_icon = scope:title
					custom_tooltip = empire_faith_gate_contested_legitimacy_applied_desc
				}
			}
		}
		# Apply the same tier to all other same-faith empire holders (iterate global list with limit).
		every_in_global_list = {
			variable = efg_empire_holders
			limit = {
~~~

**新版证据**: `game/common/modifiers/00_empire_faith_gate_modifiers.txt`，第 3—6 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
multi_empire_same_faith_penalty_1 = {
	icon = legitimacy_negative
	monthly_legitimacy_add = -1
}
~~~

**新版证据**: `game/common/casus_belli_types/00_dissolve_empire_cb.txt`，第 114—131 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	on_victory = {
		scope:attacker = { show_pow_release_message_effect = yes }

		add_legitimacy_attacker_victory_effect = yes

		scope:attacker = { accolade_attacker_war_end_glory_gain_med_effect = yes }

		scope:attacker = {
			add_prestige = major_prestige_gain
		}

		scope:defender = {
			every_held_title = {
				limit = { tier >= tier_empire }
				save_temporary_scope_as = empire_to_destroy
				scope:defender = { destroy_title = scope:empire_to_destroy }
			}
		}
~~~

## 34. AI：宗教战争意愿与大型领地处理

代码事实：00_conquest 等战争入口新增 pam_peace_of_god_coreligionist_war_ai_score_value 和 zealous_war_on_head_of_faith_ai_score_value 乘数。前者在同 Faith、满足狂热 + 组织 Tenet 参数或个人 Tenet 标记条件时乘 0.15；后者在狂热攻击者面对自己的教首时乘 0.15。都是 AI 评分修正，不是禁止玩家宣战，更不是实际每场战争概率固定下降 85%。

大型领地 AI 任命处理新增缩减参数：realm_size 超过 150 开始按规模降低处理频率，600 达最大，MAX_SKIP_PERMILLE = 900，即最大每次尝试 90% 的跳过机会。这项只针对任命/候选处理，不是让全部 AI 90% 不行动。

AI 宗教资金保留增加国库专用阈值：教会区域持有者 0、精神教首 750、骑士团 1500；原金钱阈值仍分别有其定义。大圣战集结省份重算至少间隔 7 天；有地统治者重新评估 Rite 最少间隔 5 年。

影响推断：战争意愿更受宗教教义约束，宗教经济 AI 区分金钱与国库，大型领地候选处理减少重复成本。没有进行帧率/日历速度跑分，不能将这些改动换算为整体性能提升百分比。

**新版证据**: `game/common/script_values/00_war_values.txt`，第 544—576 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
pam_peace_of_god_coreligionist_war_ai_score_value = {
	value = 1
	if = {
		limit = {
			exists = scope:defender
			scope:defender = { faith = scope:attacker.faith }
			scope:attacker = {
				OR = {
					AND = {
						has_trait = zealous
						rite ?= { rite_has_parameter = tenet_peace_of_god_coreligionist_war_reluctance }
					}
					has_personal_tenet_flag = tenet_peace_of_god_personal_coreligionist_war_reluctance
				}
			}
		}
		multiply = 0.15
	}
}

zealous_war_on_head_of_faith_ai_score_value = {
	value = 1
	if = {
		limit = {
			exists = scope:defender
			scope:attacker = {
				has_trait = zealous
				faith.religious_head ?= scope:defender
			}
		}
		multiply = 0.15
	}
}
~~~

**新版证据**: `game/common/defines/00_defines.txt`，第 1853—1855 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	AI_APPOINTMENT_REALM_SIZE_SCALEDOWN_START = 150 # Above this top-liege realm_size, AI appointment/candidacy processing is increasingly skipped per attempt (CPU scaledown for huge realms)
	AI_APPOINTMENT_REALM_SIZE_SCALEDOWN_FULL = 600 # At/above this top-liege realm_size, AI appointment/candidacy processing is skipped at the maximum rate
	AI_APPOINTMENT_MAX_SKIP_PERMILLE = 900 # Maximum chance (per 1000) to skip an AI appointment/candidacy attempt in the largest realms
~~~

**新版证据**: `game/common/defines/ai/00_ai.txt`，第 158—162 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	# instead of MIN_RESERVED_GOLD_HOLY_ORDER by holy order leaders whose
	# government uses a treasury
	#
	MIN_RESERVED_TREASURY_HOLY_ORDER = 1500

~~~

## 35. 有实际含义的小改动：成就、活动与建筑判断

已经核对以下小差异，避免报告只覆盖大文件：

- The True Royal Court 成就的 happened 条件，从自己恰好王国且领主恰好帝国，变为自己至少王国；保留有领主与宫廷显赫度高于领主的条件。这是达成阶段门槛放宽，不证明初始资格或所有更高头衔角色都能无条件达成。
- coronation_seize_advantages 意图新增至少伯爵的有效性条件。
- 宴会中“客人被宫廷宝物打动”脉冲现在明确保存已装备宫廷宝物 scope，并把活动日志的 target 角色字段改为 artifact 字段；这是宝物对象的上下文修正。它不能证明修复全部宴会错误。
- 标准经济建筑文件的一处 AI 修正改为行政 mechanic 检查；标准军事建筑的一处判断从具体 theocracy_government 改为神权 flag，覆盖新 ecclesiastical 的相同标记。并未在这些小块里改变建筑面板全部基础税收/军力。
- INTENDED_MAX_PERSONALITY_TRAITS = 6 注释说明超过会写错误日志；不能证明所有角色最多只能持有六个性格特质。
- 移除 CONVERGENCE_DELAY = 31 的旧定义，无法从文本证明现在好感修正一定立即开始衰减；需要引擎默认值或运行结果。

**完整文件差异**: `game/common/achievements/ep1_achievements.txt`。

~~~diff
--- 旧版/game/common/achievements/ep1_achievements.txt
+++ 新版/game/common/achievements/ep1_achievements.txt
@@ -337,12 +337,9 @@
 	happened = {
 		custom_description = {
 			text = the_true_royal_court_achievement_trigger
 			root.liege != root
-			highest_held_title_tier = tier_kingdom
-			root.liege = {
-				highest_held_title_tier = tier_empire
-			}
+			highest_held_title_tier >= tier_kingdom
 			root.court_grandeur_current > root.liege.court_grandeur_current
 		}
 	}
 }
~~~

**完整文件差异**: `game/common/activities/intents/coronation_intents.txt`。

~~~diff
--- 旧版/game/common/activities/intents/coronation_intents.txt
+++ 新版/game/common/activities/intents/coronation_intents.txt
@@ -88,8 +88,12 @@
 coronation_seize_advantages = {
 	icon = seize_advantages_intent
 	scripted_animation = { animation = interested }
 
+	is_valid = {
+		highest_held_title_tier >= tier_county
+	}
+
 	auto_complete = yes
 
 	ai_will_do = {
 		value = 0
~~~

**完整文件差异**: `game/common/activities/pulse_actions/feast_pulse_actions_oltner.txt`。

~~~diff
--- 旧版/game/common/activities/pulse_actions/feast_pulse_actions_oltner.txt
+++ 新版/game/common/activities/pulse_actions/feast_pulse_actions_oltner.txt
@@ -893,8 +893,15 @@
 
 	effect = {
 		scope:host = {
 			save_scope_as = root_scope
+			random_character_artifact = {
+				limit = {
+					ep1_artifact_is_court_artifact_trigger = yes
+					is_equipped = yes
+				}
+				save_scope_as = artifact
+			}
 		}
 		
 		scope:host = {
 			save_scope_as = second
@@ -911,9 +918,9 @@
 		add_activity_log_entry = {
 			key = guest_impressed_by_court_artifact
 			tags = { pulse_action }
 			character = scope:first
-			target = scope:second
+			artifact = scope:artifact
 			
 			scope:host = {
 				add_prestige = minor_prestige_gain
 			}
~~~

## 36. 历史数据：字段迁移之外也有日期和政体修订

代码事实：history 共修改 443、新增 29 个文件，涉及人物、省份、头衔和新教会局势。已核对的大量变化为 religion/faith → rite 与天主教/正教历史分支名称变化，属于初始化数据迁移。

38 个严格解码失败的变化文件中，有些非 ASCII 差异只在注释中，但也有可识别的实际脚本变化。字节转义补查已看到 k_norway 的 Nidaros/Skalholt 主教领从 theocracy 改为 ecclesiastical；k_sweden 的 Skara 主教领作同类变更；k_east_francia 内若干持有者日期修订，例如 939.1.1 → 939.10.2、1004.11.30 → 1004.11.4、1056.5.10 → 1056.10.5。这些是源数据变化，不代表本文确认其真实历史考据正确。

省份 k_east_francia 中可见旧 Catholic 初始化被替换成相应 Rite，并在部分记录中追加 1054.7.16 后的 roman_rite。东亚 han/japanese 等人物文件也包含相同结构迁移。历史日期只影响适用开局/日期，不直接构成所有局面的永久规则。

未按可靠编码恢复的全文不用于翻译名字或判断含义模糊的非 ASCII 内容。完整跳过清单在附录内嵌；脚本已分析数量保持 7727，未因为补查而改写成零跳过。

**完整文件差异**: `game/history/titles/k_norway.txt`。

~~~diff
--- 旧版/game/history/titles/k_norway.txt
+++ 新版/game/history/titles/k_norway.txt
@@ -1724,9 +1724,9 @@
 		holder = 202512 # Inge Krokrygg, son of Harald Gille
 	}
 	1161.1.1 = {
 		holder = nidaros_bishop_1 # Eysteinn Erlendsson, archbishop of Nidaros; "Archbishop Eystein, who controlled all the north"
-		government = theocracy_government
+		government = ecclesiastical_government
 	}
 	1184.6.15 = {
 		holder = 202500 # Sverre Sigurdsson
 	}
@@ -2159,9 +2159,9 @@
 		holder = 202024
 	}
 	1178.1.1 = {
 		holder = 202018 # Thorlakur, bishop of Skalholt
-		government = theocracy_government
+		government = ecclesiastical_government
 	}
 	1197.1.1 = {
 		holder = 202028
 	}
~~~

**完整文件差异**: `game/history/titles/k_sweden.txt`。

~~~diff
--- 旧版/game/history/titles/k_sweden.txt
+++ 新版/game/history/titles/k_sweden.txt
@@ -717,9 +717,9 @@
 	}
 
 	# Bishops of Skara
 	1014.1.1={
-		government = theocracy_government
+		government = ecclesiastical_government
 		holder = 242500 # Thurgot
 	}
 	1030.1.1={
 		holder = 242501 # Sigfrid
~~~

**旧版证据**: `game/history/provinces/k_east_francia.txt`，第 23—29 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
###c_halberstadt
2916 = {	#HALBERSTADT
	culture = saxon
	religion = catholic
	holding = castle_holding
}
2917 = {	#WERNINGERODE
~~~

**新版证据**: `game/history/provinces/k_east_francia.txt`，第 23—33 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
###c_halberstadt
2916 = {	#HALBERSTADT
	culture = saxon
	rite = carolingian_christianity
	holding = castle_holding
	1054.7.16 = {
		rite = roman_rite
	}
}
2917 = {	#WERNINGERODE
	holding = none
~~~

## 37. 图形、界面、本地化与死者肖像

代码事实：game/gfx 新增 2216、删除 125、修改 1368；game/gui 新增 44、删除 1、修改 124；game/localization 新增 695、删除 88、修改 4092。图形数量主要反映资源覆盖，不能据此衡量玩法重要性。

图形定义新增 ILLUSTRATION_STREAM_PATHS：插画、成就图标、宝物图标、文化传统/支柱图标、肖像环境等资源按需加载；注释说明框和部分 mask 不走相同过期机制。可以确认加载策略配置改变，不能确认峰值内存或帧率下降多少。

新增 Rite 地图显示、动态教义/美德罪恶图标相关配置，以及教会、圣地、代理人、候选人等相关 UI 文件。本文没有启动界面，所以只确认定义/文件变化，没有评估实际布局、可读性或交互漏洞。

死者肖像新增 DEAD_PORTRAIT_AGE_THRESHOLD = 30、APPARENT_AGE = 27；注释称超过年龄阈值的死者按 27 的外观年龄渲染，而显示死亡年龄不变。这是肖像显示行为配置，不是改变死亡时间、人物寿命或年龄。

语言文件的精确变化数量见后文。简体中文有新增 77、删除 14、修改 432，不能因某些英文源文件新增就断言新版没有中文翻译；文件数也无法证明新增 key 的翻译完整性、质量或游戏最终回退效果。

**新版证据**: `game/common/defines/graphic/00_graphics.txt`，第 32—34 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	# Situational textures load on demand, and masks and frames stay out because they never expire
	ILLUSTRATION_STREAM_PATHS = { "/illustrations/" "icons/achievements/" "icons/artifact/" "icons/culture_tradition/" "gfx/portraits/environments/" "/icons/culture_pillars/" "/icons/powerful_family_bonus/" "/icons/tutorial_" "gfx/portraits/portrait_glow" "gfx/portraits/portrait_editor_mask" "gfx/portraits/portrait_prison_" "gfx/portraits/portrait_rank" "gfx/portraits/portrait_main_menu_shadow" }
}
~~~

**新版证据**: `game/common/defines/00_defines.txt`，第 1444—1449 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	GRACEFUL_AGING_END = 70		# This is the apparent age at which life expectancy stops slowing down visual aging (each year onwards ages you visually 1 year)
	MAX_AGE = 100.0				# At this age portraits will use the special age gene at full strength
	DEAD_PORTRAIT_AGE_THRESHOLD = 30	# A dead character who died older than this is rendered at DEAD_PORTRAIT_APPARENT_AGE instead of their age at death (their displayed age at death is unaffected)
	DEAD_PORTRAIT_APPARENT_AGE = 27		# The apparent age used for the portraits of dead characters who died older than DEAD_PORTRAIT_AGE_THRESHOLD
	PORTRAIT_MALE_ADULT_AGE = 18	# The boy -> male portrait change happens at this age
	PORTRAIT_FEMALE_ADULT_AGE = 18	# The girl -> female portrait change happens at this age
~~~

## 38. 二进制、音频与启动器：只确认字节和体积

代码事实：变化二进制文件总数 3408。ck3.exe 的内容哈希变化，启动器安装包路径更换，多个音频银行及图形资源改变。下列体积和摘要来自同一次扫描，不把文件大小等同于功能数量。

不能从这些字节差异证明引擎具体修复了哪些崩溃、实际改善了 AI、提高了帧率、关闭了漏洞或可以直接兼容旧存档。也不能根据音频 bank 的体积推导全部曲名、配音内容或声效数量。本文没有反编译、解包音频或运行安装器。

- `binaries/ck3.exe`：新增0、删除0、修改1。

旧版：95206008 字节；SHA-256 `2d00ff3101ef70b566f2fcbae292f09263199c80e9dc8f139b82d7d96f83db86`。

新版：101039736 字节；SHA-256 `ae1ba6ff060ba603842f6f4a2ded0af4b7d3666b3dd271f75fb01b0da8e81b2d`。

- `launcher/launcher-installer-windows_2026.6.exe`：新增0、删除1、修改0。

旧版：176135144 字节；SHA-256 `3fd732eacf7059e30057c18e96b959955e9f31670f635403c72a941bd656e2a7`。

新版：不存在。

- `launcher/launcher-installer-windows_2026.11.1.exe`：新增1、删除0、修改0。

旧版：不存在。

新版：184474856 字节；SHA-256 `903b1a8ce7f993a6972099c26bf4ddc8e22cc164479e0ab8a4d50c1ade7d1082`。

- `game/sound/banks/ce3.bank`：新增1、删除0、修改0。

旧版：不存在。

新版：20714048 字节；SHA-256 `5df478ed4e2b826d7f54356ce5a0e7016f5fc756da501f7cd4527362a02be8f2`。

- `game/dlc/dlc030_ce3/sound/banks/ce3Music.bank`：新增1、删除0、修改0。

旧版：不存在。

新版：9875520 字节；SHA-256 `0e763fde3aaa9c3ae19ecc9f183849bc86991d02908e793553f4deb23ac367cc`。

- `game/sound/banks/Master Bank.bank`：新增0、删除0、修改1。

旧版：80864 字节；SHA-256 `8e3fbb2643739ba907835a2e82aecd622a154a4a9aad3af0b9eef29854fd22c9`。

新版：80864 字节；SHA-256 `5518c2cc870d3fe4e69cb9a20816a30833ff3fb7eebb334595b1d11717e04908`。

## 39. 对玩家与模组维护者的实际含义

对宗教玩法：先区分 Faith 和 Rite，再判断改宗、教首/分支首领、核心/许可/个人 Tenet 与圣地效果的作用域。国教例外有明确适用范围；宗教创业与个人教义替换需要重新检查成本、冷却及权限。

对神权路线：确认 DLC、角色可玩性、住所、教会区域和选举法。普通指定继承人与枢机选举是不同系统；教会国库与世俗金钱、军事骑士团与隐修修会也需要分别规划。

对继承/行政玩法：不要把法律文件拆分读成统一 buff。优先检查长子继承文化的初始化、国教 Rite、最终任命总分与候选资格，尤其是共享函数中仍保留的犯罪和负面特质。

对东亚玩法：丝路革新的来源判断、东方攻城文化传承集合、弩炮战象的文化禁用条件有直接意义；行政契约的首都距离与通用标记也值得在实际领域验证。

对模组维护：重点审计历史 religion 字段、Faith/Rite ID、has_doctrine/rite_has_tenet、doctrine:/tenet:、state_faith/state_rite、government flag/mechanic、law_group_type、候选人接口和特质迁移。先比较上下文，再迁移调用。代码可说明需适配的接口，但本报告不是对现有模组或存档兼容的完整验证。

## 40. 待运行验证及本报告未逐项解读的范围

建议优先用同一开局与同一 DLC 组合验证以下场景，这些是验证建议，并非已完成的测试：

1. 无 By God Alone 时，天主教/正教的 Tenet 回退、主分支归属及改宗菜单。
2. 40%/50%/60% 知识边界、近期改宗标记、采纳国教的例外。
3. 同性格在不同个人/许可/核心 Tenet 下的精神满足度，最高档敌方计谋成功率修正。
4. 神权及无地教士可玩性、指定继承人的收养和候选分、枢机选举法排除。
5. 普通会议与叙任会议互斥、25 年倒计时、主持人死亡/无人在场以及存档恢复。
6. 圣髑稀有度、三个槽、升级/采纳/创建权限、免费圣地行动与冷却消费。
7. 隐修修会与军事骑士团的赞助、借款、租约及特殊兵种构成。
8. 具备 primogeniture 革新的不同开局及加载旧存档的继承法。
9. 启用/关闭 empire_faith_gate 的创建预览、宽限、合法性刷新、绝罚与解散战争。
10. 大领域任命处理与按需纹理加载的实际性能；旧版本存档/模组载入。

仍有大量事件、互动、活动、GUI、本地化和图形文件只完成自动差异提取，未逐项审查全部运行语义。下面的目录统计与源码清单覆盖这些变化，但不会把其存在包装成已确认的 gameplay 修复。关键词“candidate”只用于定位候选，并不证明是新增机制或 bug fix。

## 附录 A: 统计、覆盖限制与变化文件索引

本附录给出可独立阅读的目录/语言/资源统计、完整解码跳过名单、已复核路径及脚本/历史/UI 文件索引。文件索引是自动证据清单，未复核项目明确标注；它不表示对所有内容已完成语义解读。

符号：A 新增、D 删除、M 修改。“+/-行”是原始文本差异行数，不是语义变化条数；格式调整、迁移和注释同样计入。二进制或文本解码失败时不把未计算的行数写成零。

### A.1 全部变化目录分类

分类按相对路径前缀，common 下保留子系统，其他目录按前两级；孤立文件独立归类。下列分类互不重叠，合计为 11173 个变化路径。这是文件布局分类，不是已确认机制的重要性评级。

- `game/localization`：新增695、删除88、修改4092；合计 4875。

- `game/gfx`：新增2216、删除125、修改1368；合计 3709。

- `game/events`：新增41、删除1、修改487；合计 529。

- `game/history`：新增29、删除0、修改443；合计 472。

- `game/gui`：新增44、删除1、修改124；合计 169。

- `game/common/scripted_effects`：新增19、删除0、修改120；合计 139。

- `game/common/scripted_triggers`：新增13、删除0、修改98；合计 111。

- `game/common/religion`：新增16、删除1、修改63；合计 80。

- `game/common/decisions`：新增7、删除0、修改66；合计 73。

- `game/common/script_values`：新增9、删除0、修改64；合计 73。

- `game/common/customizable_localization`：新增9、删除0、修改59；合计 68。

- `game/common/on_action`：新增8、删除0、修改60；合计 68。

- `game/common/character_interactions`：新增10、删除0、修改57；合计 67。

- `game/common/activities`：新增7、删除0、修改44；合计 51。

- `game/common/schemes`：新增3、删除0、修改43；合计 46。

- `game/common/scripted_character_templates`：新增2、删除0、修改37；合计 39。

- `game/common/culture`：新增0、删除0、修改34；合计 34。

- `game/common/modifiers`：新增9、删除0、修改20；合计 29。

- `game/common/casus_belli_types`：新增2、删除0、修改26；合计 28。

- `game/common/scripted_modifiers`：新增2、删除0、修改17；合计 19。

- `game/common/trigger_localization`：新增3、删除1、修改15；合计 19。

- `game/common/artifacts`：新增5、删除0、修改13；合计 18。

- `jomini/localization`：新增0、删除0、修改18；合计 18。

- `game/common/important_actions`：新增2、删除0、修改14；合计 16。

- `game/common/story_cycles`：新增1、删除0、修改15；合计 16。

- `game/common/buildings`：新增1、删除0、修改14；合计 15。

- `game/common/court_positions`：新增0、删除0、修改15；合计 15。

- `game/common/lifestyle_perks`：新增0、删除0、修改15；合计 15。

- `game/common/landed_titles`：新增3、删除0、修改11；合计 14。

- `clausewitz/localization`：新增11、删除0、修改1；合计 12。

- `game/common/opinion_modifiers`：新增5、删除0、修改7；合计 12。

- `game/common/coat_of_arms`：新增3、删除0、修改7；合计 10。

- `game/common/effect_localization`：新增1、删除0、修改9；合计 10。

- `game/common/succession_appointment`：新增1、删除0、修改9；合计 10。

- `game/common/achievements`：新增1、删除0、修改8；合计 9。

- `game/common/bookmark_portraits`：新增9、删除0、修改0；合计 9。

- `game/common/messages`：新增3、删除0、修改6；合计 9。

- `game/common/succession_election`：新增1、删除0、修改8；合计 9。

- `game/common/genes`：新增0、删除0、修改8；合计 8。

- `game/common/domiciles`：新增1、删除0、修改6；合计 7。

- `game/common/game_concepts`：新增2、删除0、修改5；合计 7。

- `game/common/law_groups`：新增7、删除0、修改0；合计 7。

- `game/common/laws`：新增1、删除0、修改6；合计 7。

- `game/common/men_at_arms_types`：新增0、删除0、修改7；合计 7。

- `game/common/situation`：新增2、删除0、修改5；合计 7。

- `game/common/subject_contracts`：新增0、删除0、修改7；合计 7。

- `game/dlc`：新增7、删除0、修改0；合计 7。

- `game/common/factions`：新增0、删除0、修改6；合计 6。

- `game/common/flavorization`：新增1、删除0、修改5；合计 6。

- `game/common/pool_character_selectors`：新增0、删除0、修改6；合计 6。

- `game/common/task_contracts`：新增0、删除0、修改6；合计 6。

- `game/data_binding`：新增2、删除0、修改4；合计 6。

- `game/sound`：新增1、删除0、修改5；合计 6。

- `game/common/council_tasks`：新增0、删除0、修改5；合计 5。

- `game/common/dynasty_perks`：新增1、删除0、修改4；合计 5。

- `game/common/great_projects`：新增1、删除0、修改4；合计 5。

- `game/common/character_memory_types`：新增2、删除0、修改2；合计 4。

- `game/common/defines`：新增0、删除0、修改4；合计 4。

- `game/common/dynasties`：新增0、删除0、修改4；合计 4。

- `game/common/governments`：新增1、删除0、修改3；合计 4。

- `game/common/holy_orders`：新增4、删除0、修改0；合计 4。

- `game/common/modifier_definition_formats`：新增0、删除0、修改4；合计 4。

- `game/common/puppets`：新增4、删除0、修改0；合计 4。

- `game/common/traits`：新增0、删除0、修改4；合计 4。

- `game/common/travel`：新增1、删除0、修改3；合计 4。

- `game/common/accolade_types`：新增0、删除0、修改3；合计 3。

- `game/common/dynasty_houses`：新增0、删除0、修改3；合计 3。

- `game/common/dynasty_legacies`：新增1、删除0、修改2；合计 3。

- `game/common/legends`：新增0、删除0、修改3；合计 3。

- `game/common/morpheme_strip_rules`：新增3、删除0、修改0；合计 3。

- `game/common/scripted_guis`：新增2、删除0、修改1；合计 3。

- `game/common/scripted_rules`：新增2、删除0、修改1；合计 3。

- `game/common/secret_types`：新增0、删除0、修改3；合计 3。

- `game/common/struggle`：新增0、删除0、修改3；合计 3。

- `clausewitz/gfx`：新增0、删除0、修改2；合计 2。

- `game/common/bookmarks`：新增0、删除0、修改2；合计 2。

- `game/common/combat_phase_events`：新增0、删除0、修改2；合计 2。

- `game/common/council_positions`：新增0、删除0、修改2；合计 2。

- `game/common/dna_data`：新增0、删除0、修改2；合计 2。

- `game/common/ethnicities`：新增0、删除0、修改2；合计 2。

- `game/common/event_backgrounds`：新增0、删除0、修改2；合计 2。

- `game/common/game_rules`：新增1、删除0、修改1；合计 2。

- `game/common/house_aspirations`：新增0、删除0、修改2；合计 2。

- `game/common/lease_contracts`：新增0、删除0、修改2；合计 2。

- `game/common/message_filter_types`：新增1、删除0、修改1；合计 2。

- `game/common/nicknames`：新增1、删除0、修改1；合计 2。

- `game/common/scripted_animations`：新增1、删除0、修改1；合计 2。

- `game/common/spiritual_fulfillment`：新增2、删除0、修改0；合计 2。

- `game/common/suggestions`：新增1、删除0、修改1；合计 2。

- `game/map_data`：新增1、删除0、修改1；合计 2。

- `game/tests`：新增0、删除0、修改2；合计 2。

- `jomini/gfx`：新增0、删除0、修改2；合计 2。

- `jomini/gui`：新增0、删除0、修改2；合计 2。

- `binaries/checksum.txt`：新增0、删除0、修改1；合计 1。

- `binaries/ck3.exe`：新增0、删除0、修改1；合计 1。

- `clausewitz_branch.txt`：新增0、删除0、修改1；合计 1。

- `clausewitz_rev.txt`：新增0、删除0、修改1；合计 1。

- `game/_commandline_options.info`：新增1、删除0、修改0；合计 1。

- `game/common/accolade_names`：新增0、删除0、修改1；合计 1。

- `game/common/achievement_groups.txt`：新增0、删除0、修改1；合计 1。

- `game/common/casus_belli_groups`：新增0、删除0、修改1；合计 1。

- `game/common/character_interaction_categories`：新增0、删除0、修改1；合计 1。

- `game/common/confederation_types`：新增0、删除0、修改1；合计 1。

- `game/common/court_types`：新增0、删除0、修改1；合计 1。

- `game/common/courtier_guest_management`：新增0、删除0、修改1；合计 1。

- `game/common/deathreasons`：新增0、删除0、修改1；合计 1。

- `game/common/decision_group_types`：新增0、删除0、修改1；合计 1。

- `game/common/diarchies`：新增0、删除0、修改1；合计 1。

- `game/common/dynasty_house_motto_inserts`：新增0、删除0、修改1；合计 1。

- `game/common/epidemics`：新增0、删除0、修改1；合计 1。

- `game/common/event_themes`：新增0、删除0、修改1；合计 1。

- `game/common/focuses`：新增0、删除0、修改1；合计 1。

- `game/common/hook_types`：新增0、删除0、修改1；合计 1。

- `game/common/inspirations`：新增0、删除0、修改1；合计 1。

- `game/common/legitimacy`：新增0、删除0、修改1；合计 1。

- `game/common/lifestyles`：新增0、删除0、修改1；合计 1。

- `game/common/menu_scenes`：新增1、删除0、修改0；合计 1。

- `game/common/named_colors`：新增0、删除0、修改1；合计 1。

- `game/common/playable_difficulty_infos`：新增0、删除0、修改1；合计 1。

- `game/common/raids`：新增0、删除0、修改1；合计 1。

- `game/common/scripted_costs`：新增0、删除0、修改1；合计 1。

- `game/common/tax_slots`：新增0、删除0、修改1；合计 1。

- `game/common/terrain_types`：新增0、删除0、修改1；合计 1。

- `game/common/tutorial_lessons`：新增0、删除0、修改1；合计 1。

- `game/common/vassal_stances`：新增0、删除0、修改1；合计 1。

- `game/credit_portraits.txt`：新增0、删除0、修改1；合计 1。

- `game/credits.txt`：新增0、删除0、修改1；合计 1。

- `game/dlc_metadata`：新增0、删除0、修改1；合计 1。

- `game/settings_layout.txt`：新增0、删除0、修改1；合计 1。

- `game/tools`：新增0、删除0、修改1；合计 1。

- `launcher/launcher-installer-windows_2026.11.1.exe`：新增1、删除0、修改0；合计 1。

- `launcher/launcher-installer-windows_2026.6.exe`：新增0、删除1、修改0；合计 1。

- `launcher/launcher-settings.json`：新增0、删除0、修改1；合计 1。

- `titus_branch.txt`：新增0、删除0、修改1；合计 1。

- `titus_rev.txt`：新增0、删除0、修改1；合计 1。

### A.2 游戏本地化语言

- english：新增77、删除0、修改452；合计 529。

- french：新增77、删除12、修改439；合计 528。

- german：新增77、删除14、修改430；合计 521。

- japanese：新增77、删除3、修改444；合计 524。

- jomini：新增0、删除0、修改9；合计 9。

- korean：新增77、删除14、修改504；合计 595。

- polish：新增77、删除3、修改496；合计 576。

- russian：新增78、删除14、修改440；合计 532。

- simp_chinese：新增77、删除14、修改432；合计 523。

- spanish：新增77、删除14、修改446；合计 537。

game/localization/workbench.json 另为新增的一个非语言文件，不计作新语言。Jomini/Clausewitz 自带本地化在目录分类中单列。以上不统计所有键的译文质量，也不能据文件数量证明语言资源完全等价。

### A.3 图形资源按扩展名

- `.dds`：新增1705、删除105、修改978；合计 2788。

- `.mesh`：新增295、删除3、修改51；合计 349。

- `.anim`：新增78、删除0、修改152；合计 230。

- `.asset`：新增99、删除4、修改89；合计 192。

- `.txt`：新增5、删除0、修改53；合计 58。

- `.png`：新增22、删除1、修改0；合计 23。

- `.particle2`：新增0、删除0、修改22；合计 22。

- `.shader`：新增1、删除0、修改10；合计 11。

- `.fxh`：新增0、删除0、修改10；合计 10。

- `.compound`：新增4、删除4、修改0；合计 8。

- `.editordata`：新增4、删除4、修改0；合计 8。

- `.tga`：新增0、删除4、修改0；合计 4。

- `.bk2`：新增2、删除0、修改0；合计 2。

- `.info`：新增0、删除0、修改2；合计 2。

- `.modifierpack`：新增0、删除0、修改1；合计 1。

- `.skin`：新增1、删除0、修改0；合计 1。

扩展名用于说明资源规模；是否二进制按扫描结果决定，并不简单按后缀猜测。文本 asset、shader、gfx 与纹理/mesh 等资源混在 game/gfx 的总数中。

### A.4 38 个文本解码跳过路径

这些文件自动深度差异仍被标记 decode_error。少量明确 ASCII 语句的补查不改变原扫描覆盖。每一项至少一侧解码失败；“UTF-8 不合法”不等于该文件无法被游戏自己的读取器使用。

- `game/history/provinces/k_andalusia.txt`：decode_error（旧版）。

- `game/history/provinces/k_angara.txt`：decode_error（旧版、新版）。

- `game/history/provinces/k_aragon.txt`：decode_error（旧版）。

- `game/history/provinces/k_badajoz.txt`：decode_error（旧版）。

- `game/history/provinces/k_bulgaria.txt`：decode_error（旧版）。

- `game/history/provinces/k_buryatia.txt`：decode_error（旧版、新版）。

- `game/history/provinces/k_caspian_steppe.txt`：decode_error（旧版）。

- `game/history/provinces/k_croatia.txt`：decode_error（旧版、新版）。

- `game/history/provinces/k_cuman.txt`：decode_error（旧版、新版）。

- `game/history/provinces/k_dzungaria.txt`：decode_error（旧版）。

- `game/history/provinces/k_east_francia.txt`：decode_error（旧版）。

- `game/history/provinces/k_epirus.txt`：decode_error（旧版、新版）。

- `game/history/provinces/k_hungary.txt`：decode_error（旧版、新版）。

- `game/history/provinces/k_kipchak.txt`：decode_error（旧版、新版）。

- `game/history/provinces/k_lotharingia.txt`：decode_error（旧版、新版）。

- `game/history/provinces/k_norway.txt`：decode_error（旧版）。

- `game/history/provinces/k_ob.txt`：decode_error（旧版、新版）。

- `game/history/provinces/k_oghuz_il.txt`：decode_error（旧版）。

- `game/history/provinces/k_pomerania.txt`：decode_error（旧版、新版）。

- `game/history/provinces/k_qara_dala.txt`：decode_error（旧版、新版）。

- `game/history/provinces/k_sapmi.txt`：decode_error（旧版、新版）。

- `game/history/provinces/k_saryarka.txt`：decode_error（旧版、新版）。

- `game/history/provinces/k_serbia.txt`：decode_error（旧版、新版）。

- `game/history/provinces/k_sweden.txt`：decode_error（旧版、新版）。

- `game/history/provinces/k_thessalonika.txt`：decode_error（旧版、新版）。

- `game/history/provinces/k_u.txt`：decode_error（旧版）。

- `game/history/provinces/k_volga_bulgaria.txt`：decode_error（旧版）。

- `game/history/titles/k_aragon.txt`：decode_error（旧版）。

- `game/history/titles/k_bavaria.txt`：decode_error（旧版）。

- `game/history/titles/k_burgundy.txt`：decode_error（旧版）。

- `game/history/titles/k_denmark.txt`：decode_error（旧版）。

- `game/history/titles/k_east_francia.txt`：decode_error（旧版）。

- `game/history/titles/k_england.txt`：decode_error（旧版）。

- `game/history/titles/k_france.txt`：decode_error（旧版、新版）。

- `game/history/titles/k_lotharingia.txt`：decode_error（旧版）。

- `game/history/titles/k_norway.txt`：decode_error（旧版、新版）。

- `game/history/titles/k_romagna.txt`：decode_error（旧版、新版）。

- `game/history/titles/k_sweden.txt`：decode_error（旧版、新版）。

### A.5 实际源码复核路径

本次登记 76 个变化文本文件。正文中的主张来自已检查的定义、差异块与关联入口；大文件按主题复核。没有把整个候选文本集合或整个附录文件索引登记为人工/LLM 已审阅。

- `game/common/achievements/ep1_achievements.txt`

- `game/common/activities/activity_types/ecumenical_council.txt`

- `game/common/activities/activity_types/pam_investiture_council.txt`

- `game/common/activities/intents/coronation_intents.txt`

- `game/common/activities/pulse_actions/feast_pulse_actions_oltner.txt`

- `game/common/artifacts/slots/01_holy_site.txt`

- `game/common/artifacts/templates/pam_saint_relic_templates.txt`

- `game/common/buildings/00_standard_economy_buildings.txt`

- `game/common/buildings/00_standard_military_buildings.txt`

- `game/common/buildings/cp8_special_buildings.txt`

- `game/common/casus_belli_types/00_dissolve_empire_cb.txt`

- `game/common/character_interactions/00_puppet_interactions.txt`

- `game/common/character_interactions/pam_interactions.txt`

- `game/common/decisions/00_holy_order_decisions.txt`

- `game/common/decisions/50_holy_site_decisions.txt`

- `game/common/decisions/dlc_decisions/pam/pam_antipope_decisions.txt`

- `game/common/defines/00_defines.txt`

- `game/common/defines/ai/00_ai.txt`

- `game/common/defines/graphic/00_graphics.txt`

- `game/common/dynasty_perks/09_pam_dynasty_perks.txt`

- `game/common/game_rules/01_empire_faith_gate_rules.txt`

- `game/common/governments/00_government_types.txt`

- `game/common/governments/01_japan_government_types.txt`

- `game/common/governments/02_theocratic_government_types.txt`

- `game/common/great_projects/types/01_pam_projects.txt`

- `game/common/laws/00_realm_laws.txt`

- `game/common/laws/00_succession_laws.txt`

- `game/common/lifestyle_perks/00_learning_2_scholarship_tree_perks.txt`

- `game/common/lifestyle_perks/00_learning_3_theology_tree_perks.txt`

- `game/common/men_at_arms_types/00_holy_order_maa_types.txt`

- `game/common/men_at_arms_types/00_maa_types.txt`

- `game/common/men_at_arms_types/10_tgp_maa_types.txt`

- `game/common/modifiers/00_empire_faith_gate_modifiers.txt`

- `game/common/religion/doctrine_types/30_core_tenets.txt`

- `game/common/religion/faith_types/00_faith_types.txt`

- `game/common/religion/faith_types/_faith_types.info`

- `game/common/religion/rite_types/00_rite_types.txt`

- `game/common/religion/rite_types/_rite_types.info`

- `game/common/religion/tenet_types/00_pam_tenets.txt`

- `game/common/religion/tenet_types/00_tenet_types.txt`

- `game/common/religion/tenet_types/_tenet_types.info`

- `game/common/schemes/scheme_types/pam_study_scheme.txt`

- `game/common/schemes/scheme_types/study_faith_scheme.txt`

- `game/common/script_values/00_holy_site_values.txt`

- `game/common/script_values/00_war_values.txt`

- `game/common/script_values/07_appointment_values.txt`

- `game/common/script_values/pam_values.txt`

- `game/common/scripted_effects/00_empire_faith_gate_effects.txt`

- `game/common/scripted_rules/00_rules.txt`

- `game/common/scripted_rules/02_holy_sites.txt`

- `game/common/scripted_triggers/00_empire_faith_gate_triggers.txt`

- `game/common/scripted_triggers/00_game_rule_triggers.txt`

- `game/common/scripted_triggers/00_has_dlc_scripted_triggers.txt`

- `game/common/scripted_triggers/00_law_triggers.txt`

- `game/common/scripted_triggers/00_religious_triggers.txt`

- `game/common/scripted_triggers/10_tgp_natural_disaster_triggers.txt`

- `game/common/scripted_triggers/10_tgp_triggers.txt`

- `game/common/scripted_triggers/pam_scripted_triggers.txt`

- `game/common/scripted_triggers/tgp_silk_road_triggers.txt`

- `game/common/situation/situations/pam_christian_situation.txt`

- `game/common/spiritual_fulfillment/00_spiritual_fulfillment_types.txt`

- `game/common/subject_contracts/contracts/administrative.txt`

- `game/common/subject_contracts/contracts/celestial.txt`

- `game/common/subject_contracts/contracts/japan_administrative.txt`

- `game/common/succession_appointment/_succession_appointment.info`

- `game/common/succession_appointment/admin_emperor.txt`

- `game/common/succession_appointment/clerical_christian.txt`

- `game/common/traits/00_traits.txt`

- `game/common/traits/trait_conversion.lookup`

- `game/dlc/dlc030_ce3/dlc030.dlc`

- `game/events/empire_faith_gate_events.txt`

- `game/history/provinces/k_east_francia.txt`

- `game/history/situations/pam_the_christian_church_history.txt`

- `game/history/titles/k_norway.txt`

- `game/history/titles/k_sweden.txt`

- `launcher/launcher-settings.json`

## 附录 B: 生成信息

- **报告生成时间**: 2026-10-01T00:02:24+08:00

- **分析模型**: Codex（基于 GPT-6；完整模型名称及版本未提供）

- **协作人**: XenoAmess

- **深度分析文件数**: 7727

- **LLM复核文件数**: 76

- **证据扫描时间**: 2026-09-30T22:47:58+08:00（原扫描时间原样记录；最终报告时间另见上项）

- **使用的 skill**: .sisyphus/skills/ck3_version_analyzer/SKILL.md

- **方法**: 全量 SHA-256 比较、全部可解码变化文本差异提取、当前 Agent 按主题继续复核旧/新源码和相关入口；未启动游戏。

- **覆盖声明**: 本报告为重点机制的详细静态分析，剩余文本仅有自动差异证据。无代理人协作、无外部更新公告核验、无实机/存档/性能测试。

- **分卷整理时间**: 2026-10-01T00:57:36+08:00

- **分卷编号**: 2/4

- **计数口径**: 标题、正文、代码、标点、空格、换行及 Markdown 标记均计入；非 BMP 字符按两个 UTF-16 单元计，采用保守计数。

- **分卷全字符计数**: 59338

