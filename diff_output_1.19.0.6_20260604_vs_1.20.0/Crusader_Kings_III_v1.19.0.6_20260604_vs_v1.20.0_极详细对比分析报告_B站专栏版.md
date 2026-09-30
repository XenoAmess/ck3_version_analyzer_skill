# Crusader Kings III 1.19.0.6_20260604 → 1.20.0 目录快照极详细对比分析报告

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

## 执行摘要

这次本地快照之间最大的变化是宗教数据与玩法共同重构：新增 Faith、Rite、Tenet 的独立结构；改宗与创建宗教分支增加知识、身份和组织条件；狂热、个人核心教义及精神满足度相互关联。变化覆盖基督教，也影响伊斯兰、东亚宗教及历史数据。

By God Alone 的新 DLC 描述文件、可游玩的神权/教会政体、教会局势、枢机任命、宗教会议、圣地与圣髑，以及教士代理人的政治互动形成了明确的新内容链。不同机制有不同 DLC 门槛与回退路径，不能统一写成“所有宗教变化都只在购买 DLC 后生效”。

继承和行政方面，法律组元数据独立成文件，候选人评分转为共享基础函数，国教关联大量改为 state_rite。存在可核实的实际规则变化，例如长子继承文化的初始继承法、学识生活方式数值、部分兵种招募条件及丝路革新来源。

新增帝国信仰限制是一组默认关闭的本地规则。启用后才涉及教首认可、强力封臣意见、同信仰帝国竞争与解散帝国战争。它必须与通常默认局面分开解读。

资源变化主要集中在本地化和图形；可执行文件、启动器和音频银行也改变。文件数量及体积可以确认，画面质量、帧率、稳定性和存档兼容性尚不能由静态差异证明。

**完整文件差异**: `launcher/launcher-settings.json`。

~~~diff
--- 旧版/launcher/launcher-settings.json
+++ 新版/launcher/launcher-settings.json
@@ -2,10 +2,10 @@
 	"formatVersion": 0,
 	"modsCompatibilityVersion": "1",
 	"gameId": "ck3",
 	"displayName": "Crusader Kings III",
-	"version": "1.19.0.6 (Scribe)",
-	"rawVersion": "1.19.0.6",
+	"version": "1.20.0.2 (Crozier)",
+	"rawVersion": "1.20.0.2",
 	"distPlatform": "steam",
 	"gameDataPath": "%USER_DOCUMENTS%/Paradox Interactive/Crusader Kings III",
 	"dlcPath": "../game",
 	"ingameSettingsLayoutPath": "settings-layout.json",
~~~

## 1. DLC 与功能开关：新包是 By God Alone

代码事实：新增 game/dlc/dlc030_ce3，其中 DLC 描述名为 By God Alone；has_pam_dlc_trigger 检查 has_dlc_feature = by_god_alone。新包 affects_checksum = yes。目录中本次共新增 7 个 DLC 文件，其中包含加载画面、缩略图与音频。

Songs of the Realm 的 dlc029 在旧快照中已经存在，不能把它列为这次比较新增的 DLC。中文显示名称需要以游戏本地化为准；本文不臆造 By God Alone 的官方中文译名。

影响推断：检查 has_pam_dlc_trigger 能证明具体调用入口的限制；只看到文件位于 pam 子目录并不足以证明整个定义只在该 DLC 中启用。下文分别指出明确检查 DLC 的入口与有回退路径的入口。

**完整文件差异**: `game/dlc/dlc030_ce3/dlc030.dlc`。

~~~diff
--- 旧版/game/dlc/dlc030_ce3/dlc030.dlc
+++ 新版/game/dlc/dlc030_ce3/dlc030.dlc
@@ -0,0 +1,8 @@
+name = "By God Alone"
+path = "dlc/dlc030_ce3"
+steam_id = "4232900"
+pops_id = "ck3_dlc030_ce3"
+msgr_id = "9PHZC0PS79S5"
+affects_checksum = yes
+localizable_name = "DLC030_CE3"
+checksum = "50a417d4c4e27d33d34ecdf47e954a99"
~~~

**新版证据**: `game/common/scripted_triggers/00_has_dlc_scripted_triggers.txt`，第 95—98 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
has_pam_dlc_trigger = {
	has_dlc_feature = by_god_alone
}

~~~

## 2. 宗教数据层：信仰、分支与核心教义独立

代码事实：新版新增 religion/faith_types、religion/rite_types、religion/tenet_types；旧的 doctrine_types/30_core_tenets.txt 被移除。Faith 负责宗教归属、圣地、内在教义和 main_rite；Rite 指向 Faith，携带分支教义与核心 Tenet；Tenet 增加个人修正、参数以及加权美德/罪恶。原来嵌入宗教定义的旧条目和历史中的 religion 字段大量迁移为这些对象。

已核对的例子：hanafi 分支归属 sunni；jingxue 归属 confucian_faith；roman_rite 与 byzantine_rite 的默认定义先归属 christian_faith，而 catholic、orthodox 的 Faith 定义指定各自主分支，并有按日期处理的结构。旧名称不能机械地全部替换成“名称 + _faith”：新版 catholic 和 orthodox 本身就是 Faith ID。

影响推断：模组中对 has_doctrine = tenet_x、doctrine:tenet_x、state_faith、历史 religion 字段的调用都需要逐项检查对象和作用域。简单搜索替换不能保证兼容，尤其需要区别宗教、信仰与同信仰内分支。历史字段迁移造成的巨大增删行不等于新增了同等数量的人物或省份。

**新版证据**: `game/common/religion/rite_types/00_rite_types.txt`，第 567—586 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
hanafi = { # Hanafi madhhab, prominent Sunni
	name = hanafi
	desc = hanafi_desc
	faith = sunni
	icon = islam_rub_el_hizb_arch_01
	founder = d_sunni

	color = { 0.0 0.33 0.23 }

	tenets = {
		tenet_struggle_submission
		tenet_religious_legal_pronouncements
		tenet_legalism
	}

	doctrines = {
		muhammad_succession_sunni_doctrine
		doctrine_temporal_head
	}
}
~~~

**新版证据**: `game/common/religion/rite_types/00_rite_types.txt`，第 1182—1195 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
jingxue = {
	name = jingxue
	desc = jingxue_desc
	faith = confucian_faith

	color = { 236 190 85 }
	icon = jingxue

	tenets = {
		tenet_benevolent_governance
		tenet_filial_piety
		tenet_harmonious_society
	}
}
~~~

**新版证据**: `game/common/religion/faith_types/00_faith_types.txt`，第 535—545 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
catholic = {
	# Scripted main Rite by start date: roman_rite from 1054.7.16. Core tenets and Rite-specific doctrines are defined on that Rite; faith-intrinsic doctrines remain inline.
	main_rite = roman_rite
	faith_details = {
		religion = christianity_religion
		color = { 0.8 0.8 0.6 }
		graphical_faith = "catholic_gfx"
	}

	origin = christian_faith

~~~

**新版证据**: `game/common/religion/faith_types/00_faith_types.txt`，第 656—680 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
orthodox = {
	# Scripted main Rite by start date: byzantine_rite from 1054.7.16. Core tenets and Rite-specific doctrines are defined on that Rite; faith-intrinsic doctrines remain inline.
	main_rite = byzantine_rite
	faith_details = {
		religion = christianity_religion
		color = { 0.7 0 0.5 }
		graphical_faith = "orthodox_gfx"
	}

	origin = christian_faith

	eminent_holy_sites = {
		constantinople
		jerusalem
	}

	holy_sites = {
		rome
		antioch
		alexandria
	}

	doctrines = {
		special_doctrine_ecumenical_christian
	}
~~~

## 3. 基督教分支与无 DLC 回退

代码事实：roman_rite 保留 communion；其另外两个教义位置通过 tenet_selection_pair 选择。拥有 by_god_alone 时使用 dulia 与 apostolic_succession，否则回退到 armed_pilgrimages 与 communal_identity。byzantine_rite 保留 pentarchy，另两项在 celestial_hierarchy / communion 和 divine_liturgy / communal_identity 之间按 DLC 选择。

因此新宗教结构有明确的无 DLC 回退路径；这些定义不能被解释为未购买 DLC 就没有天主教/正教核心教义。具体日期的 Faith 归属还受历史初始化影响。

在圣地数据中，catholic 的 eminent_holy_sites 为 Jerusalem、Rome、Santiago，普通 holy_sites 为 Cologne、Kent；orthodox 的 eminent 为 Constantinople、Jerusalem，其余三处为 Rome、Antioch、Alexandria。普通与 eminent 的效果范围不同，不能继续用旧版“所有圣地都提供同一类全信仰奖励”的假设解读。

**新版证据**: `game/common/religion/rite_types/00_rite_types.txt`，第 1—33 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
roman_rite = {
	name = roman_rite
	desc = roman_rite_desc
	founder = k_papal_state
	faith = christian_faith

	color = { 0.8 0.8 0.6 }
	icon = christianity_papal_cross_01
    tenets = {
        tenet_communion
    }

	tenet_selection_pair = {
		requires_dlc_flag = by_god_alone
		tenet = tenet_dulia
		fallback_tenet = tenet_armed_pilgrimages
	}
	tenet_selection_pair = {
		requires_dlc_flag = by_god_alone
		tenet = tenet_apostolic_succession
		fallback_tenet = tenet_communal_identity
	}

	doctrines = {
		special_doctrine_is_western_christian_faith
		doctrine_clerical_marriage_disallowed
		doctrine_adultery_men_shunned
		doctrine_homosexuality_shunned
	}

	# TODO_PAM_DESIGN TIT-72804
	cultures = { italian roman lombard langobard cisalpine }
}
~~~

**新版证据**: `game/common/religion/rite_types/00_rite_types.txt`，第 264—291 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
byzantine_rite = {
	name = byzantine_rite
	desc = byzantine_rite_desc
	founder = d_et_constantinople
	faith = christian_faith

	color = { 0.7 0 0.5 }
	icon = christianity_byzantine_cross_05

	tenets = {
		tenet_pentarchy
	}
	tenet_selection_pair = {
		requires_dlc_flag = by_god_alone
		tenet = tenet_celestial_hierarchy
		fallback_tenet = tenet_communion
	}
	tenet_selection_pair = {
		requires_dlc_flag = by_god_alone
		tenet = tenet_divine_liturgy
		fallback_tenet = tenet_communal_identity
	}

	doctrines = {
		special_doctrine_is_eastern_christian_faith
		doctrine_clerical_marriage_disallowed
	}
}
~~~

**新版证据**: `game/common/religion/faith_types/00_faith_types.txt`，第 595—609 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	eminent_holy_sites = {
		jerusalem
		rome
		santiago
	}

	holy_sites = {
		cologne
		kent
	}

	doctrines = {
		special_doctrine_ecumenical_christian
		special_doctrine_has_clerical_electors
	}
~~~

## 4. 狂热：基础增长下降，分支分歧成为新变量

代码事实：NFaith.YEARLY_FERVOR_GROWTH 从 3.5 改为 0.5，即基础项减少 3，数值比例下降约 85.7%。原来的 MINIMUM_FAITH_SIZE_FERVOR_MODIFIER 定义删除；日志保留期从 10 年改为 1 年。基础狂热仍为 50，上限仍为 100。

新版引入每分支 100 个伯爵领的规模参数、低狂热阈值 40、异端分支耗损倍率 1、免费异端数量 0、超额分支保护系数 0.5，以及每非异端但分歧分支最多 0.9 的损耗。注释中的计算例子：3 个异端通常耗损 9/年；250 个伯爵领、5 个分支时，按 100/分支需要 3 个分支，额外 2 个分支产生 1 的保护，计入耗损的异端降为 2，示例耗损为 4/年。

影响推断：被动增长明显减少，但不能说“所有宗教每年固定只涨 0.5”或“所有大信仰必定崩溃”。最终狂热仍受新分支数量、分歧、事件和引擎实现共同决定。上述平方公式是定义注释给出的意图与示例，没有运行游戏复现。日志变短也不等于狂热效果持续时间统一缩短。

旧 fervor_events 文件被移除，同时新增狂热/异端相关事件模块；删除旧文件不能证明异端机制整体被删除。对应新增与删除路径列在附录。

**旧版证据**: `game/common/defines/00_defines.txt`，第 789—800 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text

NFaith = {
	BASE_FERVOR = 50.0				# Default fervor
	MAX_FERVOR = 100.0				# Max amount of fervor
	YEARLY_FERVOR_GROWTH = 3.5		# Fervor yearly change, can be negative
	MINIMUM_FAITH_SIZE_FERVOR_MODIFIER = 10 # Adjusts the size modifier for monthly fervor gain for a faith according to the following formula: 1/squareroot(max(define_value, faith_size)/define_value) where define value is the value of MINIMUM_FAITH_SIZE_FERVOR_MODIFIER and faith_size is the current amount of provinces that follows the faith.
	FERVOR_CHANGELOG_DURATION = 10 # After how many years do fervor changelog entries get deleted?
	FAITH_CREATION_FERVOR_DISCOUNT_PER_MISSING_FERVOR = 1 # How much cheaper does creating a faith get per fervor below 100%? 1 means 1% per point
	FAITH_CREATION_FERVOR_DISCOUNT_MAX = 50 # What percentage does the discount cap out at? With these numbers, 0-50 fervor means a 50% discount. Above 50 means between 0% and 50% discount
}

NReligion = {
~~~

**新版证据**: `game/common/defines/00_defines.txt`，第 793—824 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text

NFaith = {
	MAX_VIRTUES_SINS = 7			# Virtues and sins are taken from core and approved tenets. only keep this number, giving priority to higher weights

	BASE_FERVOR = 50.0				# Default fervor
	MAX_FERVOR = 100.0				# Max amount of fervor
	YEARLY_FERVOR_GROWTH = 0.5		# Fervor yearly change, can be negative
	FERVOR_CHANGELOG_DURATION = 1 # After how many years do fervor changelog entries get deleted?

	# Counties per rite before a new rite is likely to spawn
	MAX_FAITH_SIZE_PER_RITE = 100

	# when fervor is below this value, rites will start becoming more divergent and potentially split off to new faiths
	LOW_FERVOR_THREASHOLD = 40

	# Yearly fervor loss grows faster with each extra heresy, and zero here turns depletion off
	HERESY_FERVOR_DEPLETION_MULTIPLIER = 1

	# a faith will be allowed to have this many heresies before the squared heresy depletion will start kicking in
	FREE_HERETICAL_RITES_BEFORE_DEPLETION = 0

	# if the faith has more rites than it needs (see MAX_FAITH_SIZE_PER_RITE), the number of heresies that counts towards the yearly depletion is reduced
	# by the excess rites multiplied by this number.
	# e.g. a faith that has 3 heresies would normally lose 9 fervor per year.
	# but if it has 5 branched rites and 250 counties (2 rites over the 3 needed to cover <=300 counties), the loss protection is 1 = (2 * 0.5)
	# then the heresies that count are 2 instead of 3, and the fervor loss is 4 instead of 9
	OVER_NEEDED_RITES_FERVOR_LOSS_PROTECTION_MULT = 0.5

	# every non-heretical divergent rite will provide at most this fervor loss
	MAX_FERVOR_LOSS_PER_DIVERGENT_RITE = 0.9

	# how many relics can be extracted from a saint? must be positive
~~~

## 5. 分歧阈值与创建分支：100、65、50% 的含义

代码事实：NRite 中创建分支分歧达到 100 的定义阈值会转为创建新 Faith；异端分歧阈值为 65。Tenet 状态分歧数组按 Unknown、Known、Prohibited、Permitted、Core 排列为 15、15、30、5、-5，核心教义双向检查。不要把这一数组当作五个宗教敌意等级。

原 Faith 创建的狂热折扣定义迁移为 Rite 创建：每缺 1 点狂热折扣 1%，最大 50%。低狂热使创建便宜的基础方向保留，但作用对象已经迁移。RITE_CREATION_PIETY_COST = 1.0 在定义中确实存在；各 Tenet/教义又有 piety_cost，因此这里不据此声称“创建任何宗教只需 1 虔诚”。

新版的 can_edit_rite、can_create_rite 指向宗教触发器。已核对的主要限制包括成年、和平、没有进行中的宗教会议、身份/头衔条件、教首或分支首脑相关权限、编辑标记，以及未改革宗教的圣地要求。帝国信仰限制启用时存在单独改革分支，不能把它当成默认改革条件。

影响推断：核心教义的选择会同时影响分歧、身份权限和精神满足度，旧版只按三个 Tenet 的收益优化宗教的策略需要重新评估。创建/编辑能否成功仍要以完整触发器和成本预览为准。

**新版证据**: `game/common/defines/00_defines.txt`，第 828—847 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
NRite = {
	RITE_CREATION_FERVOR_DISCOUNT_PER_MISSING_FERVOR = 1 # How much cheaper does creating a faith get per fervor below 100%? 1 means 1% per point
	RITE_CREATION_FERVOR_DISCOUNT_MAX = 50 # What percentage does the discount cap out at? With these numbers, 0-50 fervor means a 50% discount. Above 50 means between 0% and 50% discount
	RITE_CREATION_DIVERGENCE_FAITH_THRESHOLD = 100 # when creating a Rite, divergence values at or over this threshold will result in a Faith being created instead of a Rite
	RITE_CREATION_PIETY_COST = 1.0	# Fixed cost how much piety it costs to branch off a Faith with new Rite
	RITE_DIVERGENCE_HERETICAL_THRESHOLD = 65 # Divergence above which a Rite is considered heretical
	RITE_DIVERGENCE_HOSTILITY_THRESHOLD = 1 # Divergence below that will lower faith hostility by 1 level
	RITE_DIVERGENCE_GRACE_THRESHOLD = 0 # rites below this divergence will not add to the yearly fervor decrease

	# Values are Unknown, Known, Prohibited, Permitted, Core
	# Core tenets are checked both ways
	TENET_STATUS_DIVERGENCE = { 15 15 30 5 -5 }

	# Dynamic rite color interval vs the faith, two values 0-1, second larger
	RITE_COLOR_DEVIATION = { 0.1 0.6 }
}

NReligion = {
	TIME_AT_PEACE_FOR_PIETY = 730	# For faiths with a doctrine with piety_from_long_peace, how long do they need to be at peace (in days)

~~~

**新版证据**: `game/common/scripted_rules/00_rules.txt`，第 1—36 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
# Determines who can command troops; filters who shows up in the list
# Root is the potential commander
# scope:army_owner is who owns the army to command
can_command_troops = {
	can_be_commander_basic_trigger = { ARMY_OWNER = scope:army_owner }
}

# Determines who can command troops; will still show up in the list, with a breakdown explaining why they can't command
# Root is the potential commander
# scope:army_owner is who owns the army to command
can_command_troops_now = {
	can_be_commander_now_trigger = { ARMY_OWNER = scope:army_owner }
}

# Determines if a barony should be handed to a GHW beneficiary, or instead have a baron generated. If true, goes to a beneficiary
# Root is barony province
# scope:faith is the faith controlling the GHW
ghw_give_barony_to_beneficiary = {
	has_holding_type = castle_holding
}

# Determines if a rite can be edited, on top of the piety requirement, and the doctrine requirements
# Root is the rite editor
can_edit_rite = {
	can_edit_rite_trigger = yes
}

# Determines if a rite can be created, on top of the piety requirement, and the doctrine requirements
# Also handles reforming a rite, check for the unreformed doctrine to enable those additional checks
# Root is the rite creator
can_create_rite = {
	can_create_rite_trigger = yes
}

# Determines if a character can convert faith via the convert faith UI, on top of the piety requirement
# Root is the character that would convert
~~~

## 6. 改宗：知识门槛、冷却与国教例外

代码事实：旧 faith_conversion 主要检查成年、非教首、没有进行中的大圣战及目标信仰特殊封锁。新版保留这些检查，并增加“非对立教宗”、目标 main_rite 已启用且可改宗的条件。

普通路径要求没有 faith_conversion_recently_converted 标记，并检查目标分支知识：同一 Faith 内换 Rite 要严格大于 0.4；同一 Religion 跨 Faith 严格大于 0.5；其他 Religion 严格大于 0.6。“严格大于”意味着正好 40%/50%/60% 不满足这些比较。pam_values 的 UI 改宗冷却值为 5 年，实际标记的所有施加/清理调用没有逐项验证。

重要例外：若目标 Faith 等于最高领主 primary_title.state_rite.faith，或目标 Rite 正是其 state_rite，则绕过的是近期改宗与知识检查。成年、非教首、非对立教宗、大圣战与目标可转换性等前置条件仍在，不能写成“国教改宗无条件可用”。

影响推断：研究宗教、先形成知识、再改宗的准备阶段更重要；采纳领地国教可能更快捷。知识不是单纯的虔诚成本修正，而是明确的可用性门槛。

**旧版证据**: `game/common/scripted_rules/00_rules.txt`，第 88—105 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
faith_conversion = {
	is_adult = yes
	faith.religious_head != root
	is_in_ongoing_great_holy_war = no
	# Can't (or shouldn't) convert to faiths that are meant to be resurrected via decision, event, etc.
	custom_tooltip = {
		text = faith_conversion_cost_conversion_blocked_till_decision_taken
		NOT = {
			scope:new_faith = { has_variable = block_conversion_till_decision_taken }
		}
	}
	custom_tooltip = {
		text = faith_conversion_cost_conversion_blocked_till_nebulous_circumstances
		NOT = {
			scope:new_faith = { has_variable = block_conversion_till_nebulous_circumstances }
		}
	}
}
~~~

**新版证据**: `game/common/scripted_rules/00_rules.txt`，第 65—87 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	# The realm teaches its own State Rite: converting to its faith skips the recency and knowledge gates
	trigger_if = {
		limit = {
			exists = top_liege.primary_title.state_rite
			scope:new_faith = top_liege.primary_title.state_rite.faith
		}
		always = yes
	}
	trigger_else = {
		custom_tooltip = {
			text = faith_conversion_recently_converted
			NOT = {
				has_character_flag = faith_conversion_recently_converted
			}
		}

		OR = {
			AND = {
				faith.religion = scope:new_faith.religion
				"knows_rite_level(scope:new_faith.main_rite)" > pam_same_religion_rite_knowledge_requirement
			}
			"knows_rite_level(scope:new_faith.main_rite)" > pam_other_religion_rite_knowledge_requirement
		}
~~~

**新版证据**: `game/common/scripted_rules/00_rules.txt`，第 94—126 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
rite_conversion = {
	is_adult = yes
	faith.religious_head != root
	custom_tooltip = {
		text = is_antipope_tt
		pam_is_antipope_trigger = no
	}
	is_in_ongoing_great_holy_war = no
	scope:new_rite = {
		is_rite_enabled = yes
		can_convert_to_rite = yes
	}
	faith = scope:new_rite.faith

	# The realm teaches its own State Rite: adopting it skips the recency and knowledge gates
	trigger_if = {
		limit = {
			exists = top_liege.primary_title.state_rite
			scope:new_rite = top_liege.primary_title.state_rite
		}
		always = yes
	}
	trigger_else = {
		custom_tooltip = {
			text = faith_conversion_recently_converted
			NOT = {
				has_character_flag = faith_conversion_recently_converted
			}
		}

		"knows_rite_level(scope:new_rite)" > pam_same_faith_rite_knowledge_requirement
	}
}
~~~

**新版证据**: `game/common/script_values/pam_values.txt`，第 166—170 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
# years before being able to convert again
pam_ui_conversion_cooldown = 5
pam_same_faith_rite_knowledge_requirement = 0.4
pam_same_religion_rite_knowledge_requirement = 0.5
pam_other_religion_rite_knowledge_requirement = 0.6
~~~

## 7. 个人核心教义与精神满足度的基础数值

代码事实：精神满足度范围 -100 至 +100；个人 Tenet 与核心 Tenet 的性格权重倍率均为 2，获许可 Tenet 的权重倍率 0.5，宗教性格协同倍率 1。基础个人 Tenet 槽位 1，注释说明还可随虔诚等级增加；Faith 核心教义上限 3。

移除或替换个人 Tenet 的冷却为 1095 天；把 Tenet 放入空槽不会启动这个冷却，这是定义注释明确区分的行为。压力对精神满足度的换算除数 100，最低触发变化阈值 5 是最终满足度变化，不是原始压力值。

影响推断：角色特质、个人教义与组织教义有多层加权，不能用“虔诚越高就一定满足度越高”代替实际计算。一个新槽和替换已有槽也不是同一操作。此处确认配置结构及参数，没有从引擎二进制还原完整计算公式。

**新版证据**: `game/common/defines/00_defines.txt`，第 887—917 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text

	# Spiritual fulfillment
	MIN_SPIRITUAL_FULFILLMENT = -100
	MAX_SPIRITUAL_FULFILLMENT = 100

	# Resting fulfillment from traits affected by personal tenets is multiplied by this
	SPIRITUAL_FULFILLMENT_MULT_PERSONAL_TENET = 2
	# same for tenets set as Core by Rites
	SPIRITUAL_FULFILLMENT_MULT_CORE_TENET = 2
	# Permitted Tenets also contribute to virtues, but the weight of their trait is multiplied by this
	SPIRITUAL_FULFILLMENT_MULT_PERMITTED_TENET = 0.5
	# Religion-type traits are overwritten unless synergistic with a tenet/doctrine
	# Synergy adds religion weight multiplied by this, instead of keeping only the highest
	SPIRITUAL_FULFILLMENT_MULT_RELIGION_TRAIT = 1

	# base amount of personal tenets a playable character can subscribe to. Cannot be less than 1. Can be increased with piety levels
	BASE_PERSONAL_TENETS_CAP = 1
	# how many days player must wait before removing or swapping a personal tenet again after doing so. Adopting a tenet into a free slot does not start this cooldown. Set to 0 to disable.
	PERSONAL_TENET_CHANGE_COOLDOWN_DAYS = 1095
	# max amount of core tenets a faith can have
	FAITH_CORE_TENETS_CAP = 3
	# stress gain due to traits is going to be multiplied by tenet weight and divided by this number to yield the Spiritual Fulfillment change.
	SPIRITUAL_FULFILLMENT_FOR_STRESS_DIVIDE_FACTOR = 100
	# Threshold is on the final fulfillment change from negative stress, not the raw stress impact
	MIN_FULFILLMENT_CHANGE_FOR_EFFECT = 5

	# Monthly percent progress for same-faith rite spread in a clerical region, per neighbor
	MONTHLY_RITE_CONVERSION_PROCESS_PER_NEIGHBORING_COUNTY = 2

	# if set to yes, clerical region will not convert counties held by a ruler with a chaplain of a different rite than the region holder.
	REQUIRE_SAME_CHAPLAIN_RITE_FOR_REGION_CONVERSION = no
~~~

## 8. 精神满足度：基督教七档与非基督教五档

代码事实：christian_fulfillment 的阈值为 -95、-65、-30、0、30、65、95。负档压力获取倍率分别 +50%、+25%、+10%，最低两档每月虔诚获取倍率 -10%、-5%；正档压力减轻倍率 +10%、+25%、+50%。档位还提供朝圣、教士关系、代理人、传道、导师等标记，具体互动仍受各自条件约束。

最高档配置 enemy_hostile_scheme_success_chance_add = 20，最低档为 -20；这项从名称看作用于敌对方的敌对计谋成功率。因而不应把最高满足度归纳为所有方面无代价的全面增益；实际计谋面板及叠加要进游戏确认。

default_fulfillment 是非基督教回退：阈值 -65、-30、0、30、65。最低档有改宗虔诚成本 -50%、创建 Rite 成本 -20%、压力获取 +25%、同信仰好感 -10；最高档改宗成本 +50%、压力减轻 +25%、同信仰好感 +10。低档还有更换个人 Tenet 无压力的标记。

影响推断：低满足度可能伴随更便宜的改宗，却增加压力与社会代价；高满足度可能强化宗教稳定性。此定义本身没有 DLC 触发器，不能仅凭它宣布所有非基督教角色都必须购买 By God Alone 才有这些定义。

**新版证据**: `game/common/spiritual_fulfillment/00_spiritual_fulfillment_types.txt`，第 4—22 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	level = { # 0
		threshold = -95
		modifier = {
			stress_gain_mult = 0.5
			monthly_piety_gain_mult = -0.1
			enemy_hostile_scheme_success_chance_add = -20
		}
		flags = {
			dread_puppet_option
			sp_flagellant_decision
			sp_harder_conversion
			sp_fabricate_hook_court_chaplain
			sp_fabricate_hook_hor
			sp_hostile_schemes_minus_murder_no_stress_loss
			sp_ceremonial_humbling
			sp_murder_yields_no_sp_or_stress_loss
			sp_suicide_available
			sp_clerical_vassals_faction_more
		}
~~~

**新版证据**: `game/common/spiritual_fulfillment/00_spiritual_fulfillment_types.txt`，第 92—110 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	level = { # 6
		threshold = 95
		modifier = {
			stress_loss_mult = 0.5
			enemy_hostile_scheme_success_chance_add = 20
		}
		flags = {
			sp_befriend_chaplain
			sp_befriend_hor
			sp_befriend_hof
			positive_relation_puppet_option
			sp_cheaper_tithe_legate_major
			sp_cheaper_pilgrimage_major
			sp_act_of_devotion_decision
			pious_puppet_option
			sp_easier_conversion
			sp_mentor_in_sp
			sp_suicide_blocked
		}
~~~

**新版证据**: `game/common/spiritual_fulfillment/00_spiritual_fulfillment_types.txt`，第 115—129 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
# fallback for non-christian characters
default_fulfillment = {

	level = {
		threshold = -65
		modifier = {
			faith_conversion_piety_cost_mult = -0.5
			rite_creation_piety_cost_mult = -0.20
			stress_gain_mult = 0.25
			same_faith_opinion = -10
		}
		flags = {
			default_sf_personal_tenet_change_no_stress
			sp_harder_conversion
		}
~~~

**新版证据**: `game/common/spiritual_fulfillment/00_spiritual_fulfillment_types.txt`，第 164—174 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	level = {
		threshold = 65
		modifier = {
			faith_conversion_piety_cost_mult = 0.5
			stress_loss_mult = 0.25
			same_faith_opinion = 10
		}
		flags = {
			sp_cheaper_pilgrimage_major
			sp_easier_conversion
		}
~~~

## 9. Tenet 迁移同时有实际重做：Communion 示例

代码事实：旧 30_core_tenets 中的 Communion 使用 seek_indulgences_active、seek_indulgences_active_2、excommunication_active 参数；新版独立 Tenet 定义不再在这个块里直接设置这三项，而设置 tenet_communion_denied_sacrament。

新版新增伯爵领修正：战争期间控制力衰减倍率 -0.2、同 Rite 伯爵领好感 +5；个人 Tenet 修正包含同 Faith 征召兵补员 +25%；Honest / Deceitful 的美德和罪恶明确带 weight = 20、scale = 1。宗教首领和绝罚的能力还可能由其他 Tenet、Doctrine 与触发器提供，因此不能据此推成“新版本全面删除绝罚和赎罪券”。

影响推断：这不仅是文件位置改动。把旧 Communion 的组织能力直接套给新版会遗漏新的领地及个人收益，也会误判其他机制的能力来源。模组应检查参数消费者，而非只迁移定义路径。

**旧版证据**: `game/common/religion/doctrine_types/30_core_tenets.txt`，第 325—334 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	parameters = {
		seek_indulgences_active = yes
		seek_indulgences_active_2 = yes
		excommunication_active = yes
	}

	traits = {
		virtues = { honest }
		sins = { deceitful }
	}
~~~

**新版证据**: `game/common/religion/tenet_types/00_tenet_types.txt`，第 637—660 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	parameters = {
		tenet_communion_denied_sacrament
	}

	county_modifier = {
		monthly_county_control_decline_at_war_factor = -0.2
		same_rite_county_opinion_add = 5
	}

	personal_tenet_parameters = {
		tenet_communion_shared_table
	}

	personal_tenet_modifier = {
		levy_reinforcement_rate_same_faith = 0.25
	}

	traits = {
		virtues = {
			honest = { weight = 20 scale = 1 }
		}
		sins = {
			deceitful = { weight = 20 scale = 1 }
		}
~~~

## 10. 新增 26 个 PAM Tenet：以 Simony、Scholasticism 为例

新版 00_pam_tenets.txt 定义 26 个顶层 Tenet，完整标识为：peace_of_god、dulia、transubstantiation、ora_et_labora、hyperdulia、simony、monophysitism、acts_of_apostles、purgatory、be_fruitful_and_multiply、apostolic_succession、confession、original_sin、celestial_hierarchy、miles_christi、philanthropia、scholasticism、adoptionism、love_thy_neighbour、divine_liturgy、miaphysitism、hesychasm、anachoresis、mortification_of_the_flesh、holy_myron、khachkar。标识均带 tenet_ 前缀。此列表是定义数量，未逐项判断平衡。

已深入核对的 Simony：requires_dlc_flag = by_god_alone 且 is_shown 检查 DLC，can_pick 要求基督教；分歧倍率 2。组织修正包括每虔诚等级管理 +1、税率 +5%、伯爵领好感 -5。个人 Tenet 包括管理生活方式经验 +25%、收入 +5%、压力减轻倍率 -50%；Greedy 为加权美德，Generous 为罪恶。它同时有收益和代价。

Scholasticism 同样有明确 DLC 和基督教门槛。组织修正包括文化领袖偏好革新速度 +10%、学习计谋阶段时长 -15、学习计谋抵抗 +10；个人生活方式经验 +10%。参数关联大学、成人教育、宫廷学者、圣典研究与宝物知识，但参数存在不等于所有这些效果对任何角色无条件生效。

**新版证据**: `game/common/religion/tenet_types/00_pam_tenets.txt`，第 499—505 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	is_shown = {
		has_pam_dlc_trigger = yes
	}

	can_pick = {
		religion = religion:christianity_religion
	}
~~~

**新版证据**: `game/common/religion/tenet_types/00_pam_tenets.txt`，第 517—557 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	parameters = {
		tenet_tax_increase_per_piety_level
		tenet_simony_paid_vows
		tenet_simony_ecclesiastical_purchase
		tenet_simony_gold_donations
		tenet_simony_wealth_fulfillment
		tenet_simony_venal_head_of_faith
	}

	divergence_multiplier = 2

	character_modifier = {
		stewardship_per_piety_level = 1
	}

	county_modifier = {
		tax_mult = 0.05
		county_opinion_add = -5
	}
	
	personal_tenet_modifier = {
		monthly_stewardship_lifestyle_xp_gain_mult = 0.25
		monthly_income_mult = 0.05
		# Gift stress payout is doubled to survive this
		stress_loss_mult = -0.5
	}

	personal_tenet_parameters = {
		tenet_simony_personal_gifts
		tenet_simony_ecclesiastical_purchase
		tenet_simony_wealth_fulfillment
	}

	traits = {
		# Designed virtue/sin inversion - selling the sacred. https://en.wikipedia.org/wiki/Simony
		virtues = {
			greedy = { weight = 35 scale = 2 }
		}
		sins = {
			generous = { weight = 35 scale = 2 }
		}
~~~

**新版证据**: `game/common/religion/tenet_types/00_pam_tenets.txt`，第 1539—1572 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	parameters = {
		tenet_scholasticism_muslim_hebrew_greek_poi
		tenet_scholasticism_university_bonus
		tenet_scholasticism_cheaper_adult_education
		tenet_scholasticism_court_scholar
		tenet_scholasticism_study_scripture_bonus
		sanctify_artifacts_knowledge
	}

	character_modifier = {
		cultural_head_fascination_mult = 0.1
		learning_scheme_phase_duration = -15
		learning_scheme_resistance = 10
	}
	
	personal_tenet_modifier = {
		monthly_lifestyle_xp_gain_mult = 0.1
	}

	personal_tenet_parameters = {
		tenet_scholasticism_scholar_trait
		tenet_scholasticism_travelling_studium
		tenet_scholasticism_university_chance
		tenet_scholasticism_study_scripture_bonus
	}

	traits = {
		virtues = {
			diligent = { weight = 20 scale = 1 }
		}
		sins = {
			lazy = { weight = 20 scale = 1 }
		}
	}
~~~

## 11. 可游玩神权与教会制：权限入口确实改变

代码事实：旧 player_allowed 把 government_is_theocracy 一并放在排除条件内。新版改为在没有 By God Alone 时排除 ecclesiastical 与其他神权政体。购买该 DLC 因而开放了这一类政体的玩家入口，但仍须满足其余 player_allowed 条件。

共和国、雇佣兵、圣战骑士团仍被排除；新出现的隐修修会不等于可作为玩家政体。无地神权角色若没有 clerical_elector_title，还需要对应住所条件；现有行政和无地冒险者 DLC 检查也保留。

新版 02_theocratic_government_types.txt 将 theocracy 从旧通用政体文件独立出来，同时新增 ecclesiastical_government。两者都带神权标记，允许教会地产、限制王朝自动继承并使用神权任命机制。是否能取得政体还经过 theocratic_lay_clergy_trigger：在 lay clergy 的 Rite 下，要求枢机头衔、教会区域或无地教士身份中的一项。

影响推断：宗教政治成为可以直接游玩的路线，但不能概括为“所有神权角色、所有宗教骑士团都解锁”。选角入口、身份、DLC 与住所需要一起看。

**旧版证据**: `game/common/scripted_rules/00_rules.txt`，第 158—166 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
			scope:will_override_government = no
		}
		custom_description = {
			text = "GAME_OVER_CANNOT_PLAY_THEOCRACY"
			NOT = { government_has_flag = government_is_theocracy }
		}

		custom_description = {
			text = "GAME_OVER_CANNOT_PLAY_REPUBLIC"
~~~

**新版证据**: `game/common/scripted_rules/00_rules.txt`，第 177—203 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
				text = "GAME_OVER_CANNOT_PLAY_ADMIN"
				NOT = { government_has_flag = government_is_administrative }
			}
		}

		trigger_if = {
			limit = {
				NOT = { has_dlc_feature = by_god_alone }
			}
			trigger_if = {
				limit = { government_has_flag = government_is_ecclesiastical }
				custom_description = {
					text = "GAME_OVER_CANNOT_PLAY_ECCLESIASTICAL"
					NOT = { government_has_flag = government_is_ecclesiastical }
				}
			}
			trigger_else = {
				custom_description = {
					text = "GAME_OVER_CANNOT_PLAY_THEOCRACY"
					NOT = { government_has_flag = government_is_theocracy }
				}
			}
		}

		# We cannot become landless adventurers
		trigger_if = {
			limit = {
~~~

**新版证据**: `game/common/governments/02_theocratic_government_types.txt`，第 77—104 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
ecclesiastical_government = {
	government_rules = {
		inherit_from_dynastic_government = no
		treasury = yes
		replace_gold_cost_by_treasury = yes
		add_religious_subordinates_for_treasury = yes
		use_as_base_on_landed = yes
		disable_regnal_numbers = yes
		sticky_government = yes
		allow_accolades = yes
		landless_playable = yes
	}

	royal_court = landed

	primary_holding = church_holding
	valid_holdings = { castle_holding tribal_holding nomad_holding herder_holding temple_citadel_holding }
	required_county_holdings = { church_holding castle_holding city_holding }

	ai = {
		use_legends = no
	}

	can_get_government = {
		theocratic_lay_clergy_trigger = yes
		#The LAAMP Construct Holding decision
		trigger_if = {
			limit = {
~~~

该定义完整范围为第 77—161 行；节选在上述位置截断。本文结论所需的其他条件另以正文或补充片段说明。

**新版证据**: `game/common/scripted_triggers/pam_scripted_triggers.txt`，第 6598—6615 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
theocratic_lay_clergy_trigger = {
	trigger_if = {
		limit = {
			rite = { rite_has_doctrine = doctrine_theocracy_lay_clergy }
		}
		OR = {
			# Cardinals
			exists = clerical_elector_title
			# Archdioceses
			primary_title ?= { has_clerical_region = yes }
			# Other landless explicit clergy
			AND = {
				is_landed = no
				is_clergy = yes
			}
		}
	}
}
~~~

## 12. 教会制经济与军力：国库收益及军事限制

代码事实：ecclesiastical_government 使用 treasury 并可用国库替换金钱成本；宗教下属向国库贡献。其政体修正含 monthly_treasury_from_vassals = 0.85、monthly_treasury_from_non_vassals = 0.85、每月虔诚 +0.25。

军力相关修正为 accolades -1、骑士上限 -3、兵士上限/规模限制各 -3；mercenary_hire_cost_mult = 2 是 +200% 的雇佣兵成本修正。其他来源的修正仍可能叠加，因此不保证实际所有雇佣都正好为旧价三倍。

影响推断：教会制资源获取和扩张更依赖宗教组织、任命与国库，常规兵士/骑士路线受到明确限制。这是政体级修正，不是所有拥有神权封臣的世俗统治者都会承受的惩罚。实际国库收入基数和工资预算需要运行验证。

**新版证据**: `game/common/governments/02_theocratic_government_types.txt`，第 114—131 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	vassal_contract_group = theocracy_vassal

	character_modifier = {
		monthly_treasury_from_vassals = 0.85
		monthly_treasury_from_non_vassals = 0.85
		monthly_piety = 0.25
		accolades = -1
		knight_limit = -3
		men_at_arms_cap = -3
		men_at_arms_limit = -3
		mercenary_hire_cost_mult = 2
	}

	# Use flags instead of has_government for moddability if possible (i.e., wherever not visible to the player).
	flags = {
		government_is_ecclesiastical
		government_is_theocracy
		government_is_settled
~~~

## 13. 神权指定继承人：任命与收养，不能套普通世袭

代码事实：新增 designate_theocratic_heir_interaction，要求 By God Alone、神权标记、clerical_appointment_law、王朝等条件，并排除 theocratic_elective_succession_law。候选人必须不是统治者、同 Faith、与宫廷/家族等关系相关且可获授神权头衔；有效性进一步要求成年和 birth_date >= 指定人的出生日期，不能只比较整数年龄。

接受后：若候选人不是直接子女，先执行 adopt_effect；向 primary_title 的任命投资加入候选分，参考现任继承人分数的 1.1 倍再扣候选人原分数，最低投资 4；随后 set_designated_heir。相关威望、宗族威望和虔诚成本由值函数及代理人作用域决定，本文没有把它简化为免费继承。

影响推断：这是解决神权任命和玩家家系延续的明确路径。枢机选举的领域被排除，不能据此说“玩家可以直接指定下一任教宗，无视枢机投票”。指定也不是所有神权头衔从此变成普通长子继承。

**新版证据**: `game/common/character_interactions/pam_interactions.txt`，第 41—62 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	is_available = {
		has_pam_dlc_trigger = yes
	}

	is_shown = {
		scope:puppet_or_actor ?= {
			has_realm_law = clerical_appointment_law
			exists = dynasty
			trigger_if = {
				limit = { exists = player_heir }
				OR = {
					NOT = { exists = player_heir.dynasty }
					player_heir.dynasty ?= {
						this != scope:puppet_or_actor.dynasty
					}
				}
			}
			is_adult = yes
			# Cardinal-elective realms have no designated-heir concept; pre-College Popes may still designate
			NOT = { has_realm_law = theocratic_elective_succession_law }
			government_has_flag = government_is_theocracy
		}
~~~

**新版证据**: `game/common/character_interactions/pam_interactions.txt`，第 84—95 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	is_valid_showing_failures_only = {
		scope:recipient = {
			is_adult = yes # Children are not valid for Theocratic succession
			custom_tooltip = {
				text = designate_theocratic_heir_interaction_older_tt
				# The adoption below compares birth dates, not whole years, so equal ages are not enough
				birth_date >= scope:puppet_or_actor.birth_date
			}
		}
		scope:puppet_or_actor = {
			is_valid_designated_heir = scope:recipient
		}
~~~

**新版证据**: `game/common/character_interactions/pam_interactions.txt`，第 170—200 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
				if = { # set_designated_heir only accepts direct descendants, so everyone else is adopted in first
					limit = {
						scope:recipient = {
							NOT = { is_child_of = scope:puppet_or_actor }
						}
					}
					adopt_effect = {
						CHILD = scope:recipient
						ADOPTER = scope:puppet_or_actor
					}
				}

				primary_title = { # Enough to put them first
					change_appointment_investment = {
						target = scope:recipient
						investor = scope:puppet_or_actor
						value = {
							if = { # An appointment title without eligible candidates has no current heir to outbid
								limit = { exists = scope:puppet_or_actor.primary_title.current_heir }
								add = {
									value = "scope:puppet_or_actor.primary_title.current_heir.appointment_candidate_score(scope:puppet_or_actor.primary_title)"
									multiply = 1.1
								}
								subtract = "scope:recipient.appointment_candidate_score(scope:puppet_or_actor.primary_title)"
							}
							min = 4 # We do this to prevent cases when the default score of the candidate is already much higher than that the heir
						}
					}
				}

				set_designated_heir = scope:recipient
~~~

## 14. 枢机与宗教首领政治

代码事实：catholic Faith 新增 clerical_elector_titles 列表及 has_clerical_electors 特殊教义。pam_interactions 新增任命枢机、请求宫廷司祭枢机席位、撤销席位、影响教宗投票、增加 papabile 评分等定义。

已核对的 appoint_cardinal_interaction：要求 DLC，操作者或代理人必须领导枢机团；双方同 Faith；目标须满足对应教士资格、可持有及可获得枢机席位、宗教首领/分支首领关系条件，且尚无 clerical_elector_title。Faith 内已有至少 70 个选举头衔时不能继续任命。目标还不能被绝罚、不能与操作者交战，年龄、能力与人身状态有额外检查。

影响推断：宗教影响力可以通过候选分数、枢机席位和投票组织。70 是该任命入口的数量限制，不等于任何时代的实际枢机数量都固定为 70。候选算法和所有历史席位没有逐一模拟。

**新版证据**: `game/common/character_interactions/pam_interactions.txt`，第 4477—4495 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	is_available = {
		has_pam_dlc_trigger = yes
	}

	is_shown = {
		scope:puppet_or_actor ?= {
			this != scope:recipient
			faith ?= { has_doctrine_parameter = has_clerical_electors }
			faith = scope:recipient.faith
			pam_leads_college_of_cardinals_trigger = yes
		}
		scope:recipient = {
			# is_clergy alone misses PAM's landed archbishops, whose organization does not match the faith's
			pam_is_investiture_clergy_trigger = yes
			pam_can_hold_cardinalate_trigger = yes
			pam_can_receive_cardinalate_trigger = yes
			pam_pope_is_head_of_faith_or_rite_trigger = yes
			NOT = { exists = clerical_elector_title } # already a cardinal
		}
~~~

**新版证据**: `game/common/character_interactions/pam_interactions.txt`，第 4513—4542 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
		custom_tooltip = {
			text = appoint_cardinal_interaction_max_cardinals_tt
			scope:puppet_or_actor.faith ?= {
				NOT = { any_clerical_elector_title = { count >= 70 } }
			}
		}
		scope:puppet_or_actor = {
			is_available_quick = {
				adult = yes
				incapable = no
				imprisoned = no
				hostage = no
			}
		}
		scope:recipient = {
			is_available_quick = {
				adult = yes
				incapable = no
				imprisoned = no
				hostage = no
			}
			NOR = {
				is_at_war_with = scope:puppet_or_actor
				has_trait = excommunicated
			}
		}
		custom_tooltip = {
			text = pam_interaction_clerical_gender_tt
			scope:puppet_or_actor.rite = { rite_has_allowed_gender_for_clergy = scope:recipient }
		}
~~~

## 15. 神学代理人/傀儡：有资格和关系门槛

代码事实：新增 theological_agent_puppet、external_theological_agent_puppet、external_ruler_puppet 类型，以及建立/解除关系和借其权限执行请求的互动。

以外部教士代理人为例：必须拥有 By God Alone，操作者成年且有相应资格；目标为同 Faith 的教士统治者，允许无地但持有教士头衔者，不包括普通无地非统治教士。目标必须为 AI、成年、非无能且没有其他 puppeteer；操作者不能已有另一名外部教士代理人，也不能赞助其他对立教宗。对同一目标冷却 10 年。

可发送条件并非单一“好感足够”：王国及以上目标的把柄路径要求强把柄，较低阶级可以普通把柄；此外还有领主并受恐惧、家族首领、明确良好关系、囚禁、宗教下属关系或曾有操控记录等替代路径。发送资格不等于目标一定接受，仍有接受权重与后续事件。

影响推断：世俗统治者获得借助宗教角色完成动作的新途径，但不能对任意其他玩家角色无条件施加控制。代理行动的权限和付款作用域也需要看实际操作者。

**新版证据**: `game/common/character_interactions/00_puppet_interactions.txt`，第 256—284 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	is_available = {
		is_adult = yes
        can_have_theological_agent_puppet_trigger = yes
		NOT = { has_trait = incapable }
        trigger_if = {
            limit = {
                is_ai = yes
            }
            NOT = {
                exists = puppet:external_theological_agent_puppet
            }
        }
		has_pam_dlc_trigger = yes
	}

	cooldown_against_recipient = { years = 10 } # Spam prevention

	is_shown = {
		scope:actor != scope:recipient
		scope:actor.faith ?= scope:recipient.faith
		scope:recipient = {
			is_clergy = yes
			is_ruler = yes # Hide against unlanded non-ruler clergy; landless clerical title-holders remain valid
			NOR = {
				scope:actor.puppet:theological_agent_puppet ?= scope:recipient
				scope:actor.cp:councillor_court_chaplain ?= scope:recipient
			}
		}
	}
~~~

**新版证据**: `game/common/character_interactions/00_puppet_interactions.txt`，第 303—359 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
		scope:recipient = {
			is_ai = yes
			NOR = {
				is_adult = no
				has_trait = incapable
			}
            custom_tooltip = {
                text = pam_recipient_already_puppet_tt
                NOT = { exists = puppeteer }
            }
		}
	}

	can_send = {
		scope:actor = {
			custom_tooltip = {
				text = external_theocratic_puppet_reqs_tt
				OR = {
					trigger_if = {
						limit = {
							scope:recipient = {
								highest_held_title_tier >= tier_kingdom
							}
						}
						has_strong_hook = scope:recipient
					}
					trigger_else = {
						has_hook = scope:recipient
					}
					AND = {
						is_liege_or_above_of = scope:recipient
						scope:recipient = {
							has_dread_level_towards = {
								target = scope:actor
								level >= 2
							}
						}
					}
					AND = {
						exists = scope:recipient.house
						scope:recipient.house.house_head = scope:actor
					}
					has_any_moderate_good_relationship_with_character_trigger = { CHARACTER = scope:recipient }
					scope:recipient = {
						is_imprisoned_by = scope:actor
					}
					any_subordinate = {
						this = scope:recipient
					}
					scope:recipient = {
						has_variable_list = puppeteers
						any_in_list = {
							variable = puppeteers
							this = scope:actor
						}
					}
				}
~~~

## 16. 教会局势：开局阶段与行为催化剂

代码事实：新增 the_christian_church 局势，历史入口在 has_pam_dlc_trigger 为真时启动。867 初始化 fragile_unity；1054.7.16 设置大分裂相关全局标记；1066 初始化 reform_phase；1178 初始化 crusade_phase。这些是历史日期初始化，不能据此宣布每局都在固定年份必然切换同样阶段。

局势定义包含 fragile_unity、saeculum_obscurum、conversion_phase、reform_phase、investiture_crisis、crusade_phase、concord 等阶段，区分主要信仰、次要及异端、世俗与教士参加者。主要信仰选择涉及伯爵领追随者规模。

新增催化剂关联教士裙带关系、买卖圣职、婚姻、国库挪用、杀害教士、任命、教宗选举、圣战、枢机、会议、修会与异端等行为。催化剂能影响局势走向，不是仅添加事件文案；各阶段的催化剂权重不同，本文没有用单一权重覆盖全部阶段。

影响推断：宗教政治的结果会反馈到区域性阶段和对不同参加者的修正。对不拥有 DLC 或不在相关参加者组的角色，不能直接套用这些阶段加成。

**完整文件差异**: `game/history/situations/pam_the_christian_church_history.txt`。

~~~diff
--- 旧版/game/history/situations/pam_the_christian_church_history.txt
+++ 新版/game/history/situations/pam_the_christian_church_history.txt
@@ -0,0 +1,62 @@
+###################
+# CHRISTIAN CHURCH  #
+###################
+
+-1.1.1 = {
+	effect = {
+		if = {
+			limit = { has_pam_dlc_trigger = yes } 
+			start_situation = {
+				type = the_christian_church
+			}
+		}		
+	}
+}
+
+867.1.1 = {
+	effect = {
+		if = {
+			limit = { has_pam_dlc_trigger = yes }
+			situation:the_christian_church = {
+				situation_top_sub_region = {
+					change_phase = { phase = fragile_unity }
+				}
+			}
+		}		
+	}
+}
+
+1054.7.16 = {
+	effect = {
+		if = {
+			limit = { has_pam_dlc_trigger = yes }
+			set_global_variable = pam_great_schism_decision_taken
+		}
+	}
+}
+
+1066.1.1 = {
+	effect = {
+		if = {
+			limit = { has_pam_dlc_trigger = yes }
+			situation:the_christian_church = {
+				situation_top_sub_region = {
+					change_phase = { phase = reform_phase }
+				}
+			}
+		}		
+	}
+}
+
+1178.1.1 = {
+	effect = {
+		if = {
+			limit = { has_pam_dlc_trigger = yes }
+			situation:the_christian_church = {
+				situation_top_sub_region = {
+					change_phase = { phase = crusade_phase }
+				}
+			}
+		}
+	}
+}
~~~

**新版证据**: `game/common/situation/situations/pam_christian_situation.txt`，第 1—7 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
@saeculum_obscurum_points = 1250
@conversion_phase_points = 1250
@reform_phase_points = 1250
@investiture_crisis_points = 1250
@crusade_phase_points = 1250
@investiture_council_outcome_points = 1250

~~~

## 17. 叙任权危机：25 年计时后召开会议，效果按阵营区分

代码事实：pam_investiture_crisis_duration_days 为 9125 天，按 365 天/年即 25 年。进入 investiture_crisis 时设置日期、倒计时及投票估计；月度入口在倒计时到期后启动叙任会议，而不是简单自动结束阶段。

该阶段主要教士统治者对封建政体好感 -25；主要世俗统治者 clergy_opinion -25，次要阵营相应为 -15。主要教士组的封建税贡修正 -25%；主要世俗组的教会制税贡修正 -25%、伯爵领控制力增长倍率 -50%、衰减倍率 +50%；次要阵营税贡修正 -10%。这些都属于具体 participant group，不能概括成全世界统一掉税 25%。

未来阶段的分支由会议结果催化剂触发：spiritual 结果指向 reform_phase，temporal 结果指向 fragile_unity，所需及授予的催化剂点数为 1250。

影响推断：危机不仅是叙事标签，还会影响教士与世俗间关系、税贡及地方控制。计时与会期结束之间有明确的活动链；失效处理及无人在场的兜底需要实机验证。

**新版证据**: `game/common/script_values/pam_values.txt`，第 1—18 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
# The Christian Church situation bonuses
pam_the_christian_church_county_conversion_bonus_value = 1.5
pam_the_christian_church_county_conversion_malus_value = 0.75
pam_the_christian_church_faster_county_control_task_value = 1.25

# Investiture Controversy length in days, read by both the on_monthly timer and the years-left UI
pam_investiture_crisis_duration_days = 9125

# The same duration expressed in years, used to cap the "years left" label.
pam_investiture_crisis_duration_years = {
	value = pam_investiture_crisis_duration_days
	divide = 365
}

# Years left falls back to the full duration if the start-date variable is unset
pam_investiture_crisis_years_left_value = {
	value = pam_investiture_crisis_duration_days
	if = {
~~~

**新版证据**: `game/common/situation/situations/pam_christian_situation.txt`，第 40—55 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	# Timer expiry convenes the council rather than ending the phase
	# The in-absentia fallback decides a faith's doctrine but never moves the chapter
	on_monthly = {
		if = {
			limit = {
				has_situation_top_phase_parameter = the_christian_church_investiture_controversy
				NOT = { has_variable = investiture_awaiting_council }
				pam_investiture_crisis_years_left_value <= 0
			}
			set_variable = investiture_awaiting_council
			if = { limit = { has_variable = investiture_council_countdown } remove_variable = investiture_council_countdown }
			# Announces 0058 per faith that actually gets a council, then nudges each host.
			pam_start_investiture_council_effect = yes
			pam_investiture_maybe_end_crisis_effect = yes
		}
		pam_investiture_end_uncontested_crisis_effect = yes
~~~

**新版证据**: `game/common/situation/situations/pam_christian_situation.txt`，第 1324—1345 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
					christian_clerical_main_power_rulers = {
						parameters = {
							the_christian_church_no_coronation = yes
							the_christian_church_cheaper_clerical_appointment = yes
							the_christian_church_clergy_puppeting_malus_major = yes
						}
						character_modifier = {
							# Unique to IC
							feudal_government_opinion = -25
						}
					}
					christian_regular_main_power_rulers = {
						parameters = {
							the_christian_church_cheaper_clerical_appointment = yes
							the_christian_church_antipope_coronations = yes
							the_christian_church_secular_puppeting_bonus_minor = yes
						}
						character_modifier = {
							# Unique to IC
							clergy_opinion = -25
						}
					}
~~~

**新版证据**: `game/common/situation/situations/pam_christian_situation.txt`，第 1415—1429 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
			future_phases = {
				reform_phase = {
					takeover_type = points
					takeover_points = @investiture_council_outcome_points
					catalysts = {
						catalyst_investiture_council_settled_spiritual = @investiture_council_outcome_points
					}
				}
				fragile_unity = {
					takeover_type = points
					takeover_points = @investiture_council_outcome_points
					catalysts = {
						catalyst_investiture_council_settled_temporal = @investiture_council_outcome_points
					}
				}
~~~

## 18. 宗教会议与叙任会议：两种入口，有并发保护

代码事实：新增 activity_ecumenical_council；其 is_shown 要求 DLC 和 can_hold_ecumenical_council_trigger。若 Faith 有 investiture_council_pending，普通会议被阻止；若已有 ecumenical_council_ongoing，也不能再开第二场。主持人须具备教首、主要教士组、教会政体或神学代理人等至少一种相关资格；拥有教会区域的 Faith 还有最低参与区域检查，活动阶段要通过出席及法定人数检查。

新增 activity_investiture_council 是专用会议：要求 DLC 和 investiture_council_nominated 标记，启动时还要求 Faith 的 pending 标记。它与普通会议的入口不同，不是玩家在活动规划器中随意开启的一场普通教义辩论。

两个定义都对主持人或活动失效做了清理/重新提示处理；这是可见的保护逻辑。不能仅凭存在清理代码就宣称已彻底修复所有死锁；没有完成活动链、存档恢复及无地主持人场景的运行测试。

**新版证据**: `game/common/activities/activity_types/ecumenical_council.txt`，第 7—44 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	is_shown = {
		has_pam_dlc_trigger = yes
		can_hold_ecumenical_council_trigger = yes
		# Don't offer a regular ecumenical council while this faith has an Investiture Council pending (it would preempt it).
		NOT = { faith = { has_variable = investiture_council_pending } }
	}
	
	can_start_showing_failures_only = {
		is_available_adult = yes
		NOT = { is_activity_type_on_cooldown = activity_ecumenical_council }
		# Same guard as is_shown: block a routine council while the special one is pending.
		NOT = { faith = { has_variable = investiture_council_pending } }
		# Hard block, unlike the AI-only window below: two councils at once would fight over the same rite.
		custom_tooltip = {
			text = ecumenical_council_already_ongoing_tt
			NOT = { faith = { has_variable = ecumenical_council_ongoing } }
		}
		custom_tooltip = {
			text = can_host_ecumenical_council_tt
			OR = {
				any_held_title = { is_head_of_faith = yes }
				top_participant_group:the_christian_church ?= { participant_group_type = christian_clerical_main_power_rulers }
				government_has_flag = government_is_ecclesiastical
				has_theological_agent_puppet_trigger = yes
			}
		}
		trigger_if = {
			limit = { faith ?= { has_doctrine_parameter = has_clerical_regions } }
			custom_tooltip = {
				text = ecumenical_council_faith_needs_clerical_region_holders_tt
				faith = {
					any_faith_ruler = {
						count >= ecumenical_council_min_clerical_region_holders
						pam_is_clerical_region_holder_trigger = yes
					}
				}
			}
		}
~~~

**新版证据**: `game/common/activities/activity_types/pam_investiture_council.txt`，第 14—42 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	# Only visible to the AI host the situation nominates, so a player never sees it in the planner.
	is_shown = {
		has_pam_dlc_trigger = yes
		has_character_flag = investiture_council_nominated
	}

	# The pending-council flag limits starting to the nominated host, not every eligible cleric
	can_start_showing_failures_only = {
		is_available_adult = yes
		has_pam_dlc_trigger = yes
		can_hold_ecumenical_council_trigger = yes
		has_character_flag = investiture_council_nominated
		faith = { has_variable = investiture_council_pending }
		custom_tooltip = {
			text = can_host_ecumenical_council_tt
			OR = {
				any_held_title = { is_head_of_faith = yes }
				top_participant_group:the_christian_church ?= { participant_group_type = christian_clerical_main_power_rulers }
				is_clergy = yes
				has_theological_agent_puppet_trigger = yes
				# We match pam_valid_investiture_council_host_trigger because clergy or group can change after nomination
				government_has_flag = government_is_ecclesiastical
				any_held_title = {
					tier >= tier_duchy
					has_clerical_region = yes
				}
			}
		}
	}
~~~

## 19. 对立教宗：新增决议与费用分支

代码事实：新增 declare_antipope_decision 等决议。已核对的世俗赞助入口要求有地、spiritual_head_of_faith、已有宗教首领、自己不是首领/赞助者/对立教宗、Rite 没有 no_head_of_faith 参数；执行有效性要求至少王国，以及 antipope_requirements_trigger 或特定解锁标记。神权角色使用另一个自立入口。

选取教士的判断有 DLC 和无 DLC 两条分支：拥有 DLC 可经过外部教士代理人的路径；无 DLC 仍有合格教士封臣或宫廷司祭的分支。因此不能仅因文件位于 pam 目录就写成“此决议所有路径必须购买 DLC”。

基础成本片段中金钱或国库为 500，虔诚基础 1000，存在被拒教宗相关 0.75 和阶段相关 0.67 的折扣乘数；完整虔诚后续和其他条件还需按最终预览确认。本文不宣布它是无条件、固定成本的替代教宗按钮。

**新版证据**: `game/common/decisions/dlc_decisions/pam/pam_antipope_decisions.txt`，第 29—56 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	is_shown = {
		is_landed = yes
		faith ?= { has_doctrine_parameter = spiritual_head_of_faith }
		NOT = { government_has_flag = government_is_theocracy } # They use declare_yourself_antipope_decision
		exists = faith.religious_head
		this != faith.religious_head
		pam_is_antipope_sponsor_trigger = no
		pam_is_antipope_trigger = no
		NOT = {
			rite = { rite_has_parameter = no_head_of_faith }
		}
	}

	is_valid = {
		highest_held_title_tier >= tier_kingdom
		trigger_if = {
			limit = {
				has_variable = antipope_squabble_unlock
			}
			custom_tooltip = {
				text = antipope_title_threatened_tt
				has_variable = antipope_squabble_unlock
			}
		}
		trigger_else = { 
			antipope_requirements_trigger = { AMOUNT = 2 }
		}
	}
~~~

**新版证据**: `game/common/decisions/dlc_decisions/pam/pam_antipope_decisions.txt`，第 58—85 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	is_valid_showing_failures_only = {
		is_available_adult = yes
		trigger_if = {
			limit = { has_pam_dlc_trigger = yes }
			custom_tooltip = {
				text = declare_antipope_decision_select_clergy_tt
				OR = {
					any_vassal_or_below = {
						pam_valid_antipope_clergy_vassal_trigger = { LIEGE = scope:actor }
					}
					exists = cp:councillor_court_chaplain
					puppet:external_theological_agent_puppet ?= {
						NOT = { any_held_title = { is_head_of_faith = yes } }
					}
				}
			}
		}
		trigger_else = {
			custom_tooltip = {
				text = declare_antipope_decision_select_clergy_no_puppet_tt
				OR = {
					any_vassal_or_below = {
						pam_valid_antipope_clergy_vassal_trigger = { LIEGE = scope:actor }
					}
					exists = cp:councillor_court_chaplain
				}
			}
		}
~~~

## 20. 动态圣地与圣髑：普通、重要圣地和供奉区分

代码事实：Faith 新增 eminent_holy_sites 与普通 holy_sites 的分层。默认重要圣地上限 3、总圣地上限 9，最低分别为 1；Religion 可以覆盖默认值，所以这些并非所有宗教永远不可改变的固定数量。

创建圣地的圣髑稀有度门槛 3、效果稀有度总和上限 12。圣地有 3 个供奉槽；稀有度值 common/masterwork/famed/illustrious 分别 1/2/3/4，计入条件经过“圣髑”等判断，不是任何普通宝物都可拿来凑数。每位圣人最多提取圣髑的定义值为 4。

供奉的管理规则同时要求控制关系和 Faith 对圣地的归属；不是拿到宝物就能向任何宗教圣地随意供奉。供奉中的宝物耐久损耗新增为 0。圣人圣髑的 can_benefit 检查持有者 Religion 与被埋圣人的 Religion 相同，部分受益条件比“必须同一 Faith”更宽。

影响推断：圣髑可以成为圣地建设和长期保存的资源，原来只看宫廷陈列加成的宝物策略不再覆盖全部用途。圣地效果及所有槽位类型的运行限制尚未逐项验证。

**新版证据**: `game/common/script_values/00_holy_site_values.txt`，第 1—11 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
# Scope: holy_site
# Returns: the sum of Artifact Rarity values of every artifact enshrined in
# the holy site whose is_holy_relic trigger passes for the controlling faith.
# (And the controlling faith also has this holy site as one of their own)
# Each artifact contributes 1=Common, 2=Masterwork, 3=Famed, 4=Illustrious.
# 0 if nothing qualifies.
# Backed by the `total_active_artifact_rarity_sum` trigger registered in
# holy_site_artifact_trigger_impl.cpp.
holy_site_total_artifact_rarity = {
	value = root.total_active_artifact_rarity_sum
}
~~~

**新版证据**: `game/common/defines/00_defines.txt`，第 919—936 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	# How many eminent holy sites can a Faith have? (unless overridden by Religion)
	FAITH_EMINENT_HOLY_SITES_MAX_DEFAULT = 3
	# How many holy sites in total, eminent ones included, can a Faith have? (unless overridden by Religion)
	FAITH_HOLY_SITES_MAX_DEFAULT = 9
	# Minimum number of eminent holy sites a Faith must retain (unless overridden by Religion)
	FAITH_EMINENT_HOLY_SITES_MIN_DEFAULT = 1
	# Minimum number of holy sites in total a Faith must retain (unless overridden by Religion)
	FAITH_HOLY_SITES_MIN_DEFAULT = 1

	# How many rarity levels are required for a Ruler to create a holy site
	CREATE_HOLY_SITE_RARITY_REQUIRED = 3

	# How many rarity levels can be used to scale holy site effects (should match with holy site slots)
	MAX_HOLY_SITE_RARITY_TOTAL = 12
}

NTitle = {
	CREATE_TITLE_OR_TIER_HEGEMONY = { -1 -1 -1 -1 -1 2 1 }
~~~

**新版证据**: `game/common/defines/00_defines.txt`，第 1576—1580 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	ARTIFACT_DURABILITY_DECAY_STORAGE = 1.0 # yearly decay, unequipped
	ARTIFACT_DURABILITY_DECAY_EQUIPPED = 1.0 # yearly decay, equipped to person
	ARTIFACT_DURABILITY_DECAY_DISPLAY = 0.0 # yearly decay, on display in court
	ARTIFACT_DURABILITY_DECAY_ENSHRINED = 0.0 # yearly decay, enshrined in a holy site (disabled in code too)
	ARTIFACT_HOUSE_CLAIM_YEARS = 50 # Number of years a house member must hold an artifact before a house artifact claim is generated
~~~

**新版证据**: `game/common/artifacts/slots/01_holy_site.txt`，第 1—20 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
###################
# HOLY SITE SLOTS #
###################
# Artifact slots available on holy sites
###

holy_relic_1 = {
	holy_site = yes
	allow_any_type_or_category = yes
}

holy_relic_2 = {
	holy_site = yes
	allow_any_type_or_category = yes
}

holy_relic_3 = {
	holy_site = yes
	allow_any_type_or_category = yes
}
~~~

## 21. 圣地管理决议：升级、采纳与冷却

代码事实：新增 elevate、demote、abandon、adopt 等圣地管理决议。elevate_holy_site_decision 的基本成本 1000 虔诚；若 Faith 有免费圣地行动，成本乘零并消耗该行动。它要求能管理 Faith 圣地、目标原为普通圣地、未达到重要圣地上限、县持有者同 Faith，并满足宗教首领或领域控制关系。

adopt_holy_site_decision 要求独立、相应管理权限、未达总数上限、目标在领域内且持有者同 Faith、该 Faith 可使用目标所在王国等条件；还要求允许采纳任意圣地的参数或目标满足共享/融合资格，目标必须属于尚有追随者的活跃 Faith。不能解读为任意皇帝可无限复制圣地。

相关冷却值普通为 5 年；有免费行动时为 0。创建圣地与升级/采纳已有圣地是不同入口，稀有度门槛不能套给所有圣地操作，1000 虔诚也不是全部圣地操作的统一价格。

**新版证据**: `game/common/decisions/50_holy_site_decisions.txt`，第 25—54 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	is_valid = {
		save_temporary_scope_as = root
		exists = scope:selected_item

		can_manage_faith_holy_sites_trigger = yes

		scope:selected_item ?= {
			root.faith = {
				is_faith_holy_site = prev
				NOT = { is_faith_eminent_holy_site = prev }
				save_temporary_scope_as = faith
				custom_tooltip = {
					text = elevate_holy_site_decision_under_eminent_holy_sites_max
					list_size:eminent_holy_site < root.faith.religion.eminent_holy_sites_max
				}
			}
			custom_tooltip = {
				text = elevate_holy_site_decision_target_in_realm_or_head_of_faith
				OR = {
					root.faith.religious_head ?= root
					holy_site_barony.holder = {
						target_is_same_character_or_above = root
					}
				}
			}
			custom_tooltip = {
				text = elevate_holy_site_decision_county_holder_correct_faith
				holy_site_county.holder.faith = root.faith
			}
		}
~~~

**新版证据**: `game/common/decisions/50_holy_site_decisions.txt`，第 62—84 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	cost = {
		piety = {
			value = 1000
			if = {
				limit = { faith = { faith_has_free_holy_site_action_trigger = yes } }
				multiply = 0
			}
		}
	}

	cooldown = { years = holy_site_decision_cooldown_value }

	effect = {
		scope:selected_item.holy_site_county.holder = {
			save_scope_as = county_holder
		}
		root.faith = {
			make_holy_site_eminent = {
				target = scope:selected_item
				actor = root
			}
			consume_free_holy_site_action_effect = yes
		}
~~~

**新版证据**: `game/common/script_values/00_holy_site_values.txt`，第 22—28 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
holy_site_decision_cooldown_value = {
	value = holy_site_action_cooldown_years
	if = {
		limit = { faith = { faith_has_free_holy_site_action_trigger = yes } }
		value = 0
	}
}
~~~

## 22. 主教座堂与集体分支转化工程

代码事实：新增 pam_cathedral_01/02/03，文件注释分别称 Romanesque、Gothic、Flamboyant，并新增 pam_mass_rite_conversion。主教座堂入口要求 By God Alone、至少公爵和 christian_fulfillment 类型；集体转化入口要求 DLC 与至少公爵。

第一阶主教座堂的选址过滤器为 clerical_region_theocracy_capitals，所有者为对应教会区域或神权持有者。已核对的世俗规划分支要求虔诚等级至少 2、宫廷司祭对操作者好感 >0、领地内有合适省份且没有被绝罚。AI 对同类在建工程设置少量并发限制。

影响推断：新工程把宗教组织、选址和成本结合起来，不是给全体公爵直接添加永久建筑奖励。三个层级具体竣工效果、全部费用系数、集体转化执行范围及其事件链没有逐项核实，本章只确认类型、入口与第一阶重要规划条件。

**新版证据**: `game/common/scripted_triggers/pam_scripted_triggers.txt`，第 787—791 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
pam_cathedral_project_requirements_trigger = {
	has_pam_dlc_trigger = yes
	highest_held_title_tier >= tier_duchy
	has_spiritual_fulfillment_type = christian_fulfillment
}
~~~

**新版证据**: `game/common/scripted_triggers/pam_scripted_triggers.txt`，第 215—218 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
pam_mass_rite_conversion_requirements_trigger = {
	has_pam_dlc_trigger = yes
	highest_held_title_tier >= tier_duchy
}
~~~

**新版证据**: `game/common/great_projects/types/01_pam_projects.txt`，第 27—43 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
	is_shown = {
		pam_cathedral_project_requirements_trigger = yes
		trigger_if = { # The AI should not have more than a handful of new cathedrals rising at the same time
			limit = {
				is_ai = yes
			}
			NOT = {
				any_great_project = {
					count >= 3
					great_project_type = pam_cathedral_01
				}
			}
		}
	}

	province_filter = clerical_region_theocracy_capitals
	owner = province_clerical_region_or_theocracy_holder
~~~

**新版证据**: `game/common/great_projects/types/01_pam_projects.txt`，第 71—97 行。以下为连续原文节选；未展示的其他块不等于没有条件。

~~~text
		#secular rulers can only build inside their realm
		trigger_if = {
			limit = {
				root = {
					NOT = { faith.religious_head ?= this }
					is_clergy = no
				}
			}
			piety_level >= 2
			cp:councillor_court_chaplain ?= {
				opinion = {
					target = root
					value > 0
				}
			}
			custom_tooltip = {
				text = valid_cathedral_spot_in_sub_realm_tt
				any_sub_realm_county = {
					any_county_province = {
						is_valid_cathedral_spot_in_province_trigger = yes
					}
				}
			}
			NOT = {
				has_trait = excommunicated
			}
		}
~~~

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

### A.6 脚本、事件、历史与游戏 GUI 的完整变化路径

本清单包含上述四个前缀下全部 2515 个变化路径。源目录之外的资源按 A.1—A.3 汇总，二进制关键项另在正文说明。为减少重复，分组标题给出路径前缀，各行路径按该前缀继续拼接；所有标识都可还原为源码相对路径。

#### game/common/accolade_names/（1 个变化路径）

- M `00_accolade_names.txt`；+12/-20 行；未作语义复核。

#### game/common/accolade_types/（3 个变化路径）

- M `04_ep2_common_attributes.txt`；+52/-52 行；未作语义复核。
- M `04_ep2_eminent_attributes.txt`；+20/-18 行；未作语义复核。
- M `04_ep2_maa_attributes.txt`；+3/-3 行；未作语义复核。

#### game/common/achievement_groups.txt/（1 个变化路径）

- M ``；+16/-2 行；未作语义复核。

#### game/common/achievements/（9 个变化路径）

- A `ce3_achievements.txt`；+161/-0 行；未作语义复核。
- M `ep1_achievements.txt`；+1/-4 行；已复核关键定义/差异。
- M `ep2_achievements.txt`；+1/-1 行；未作语义复核。
- M `ep3_achievements.txt`；+21/-21 行；未作语义复核。
- M `fp1_achievements.txt`；+1/-1 行；未作语义复核。
- M `fp2_achievements.txt`；+2/-2 行；未作语义复核。
- M `fp3_achievements.txt`；+7/-11 行；未作语义复核。
- M `msgrdk_achievements.json`；+40/-0 行；未作语义复核。
- M `standard_achievements.txt`；+9/-15 行；未作语义复核。

#### game/common/activities/（51 个变化路径）

- M `activity_types/_activity_type.info`；+48/-1 行；未作语义复核。
- M `activity_types/camp_party.txt`；+25/-27 行；未作语义复核。
- M `activity_types/chariot_race.txt`；+34/-52 行；未作语义复核。
- M `activity_types/coronation.txt`；+239/-229 行；未作语义复核。
- M `activity_types/debate.txt`；+33/-109 行；未作语义复核。
- A `activity_types/ecumenical_council.txt`；+2183/-0 行；已复核关键定义/差异。
- M `activity_types/feast.txt`；+374/-146 行；未作语义复核。
- M `activity_types/festival.txt`；+28/-78 行；未作语义复核。
- M `activity_types/funeral.txt`；+224/-117 行；未作语义复核。
- M `activity_types/gruesome_festival.txt`；+186/-237 行；未作语义复核。
- M `activity_types/hike.txt`；+45/-16 行；未作语义复核。
- M `activity_types/hunt.txt`；+80/-200 行；未作语义复核。
- M `activity_types/imperial_examination.txt`；+63/-69 行；未作语义复核。
- M `activity_types/inspection.txt`；+83/-88 行；未作语义复核。
- M `activity_types/local_examination.txt`；+48/-109 行；未作语义复核。
- M `activity_types/monument_expedition.txt`；+80/-24 行；未作语义复核。
- A `activity_types/pam_investiture_council.txt`；+760/-0 行；已复核关键定义/差异。
- M `activity_types/pilgrimage.txt`；+1108/-414 行；未作语义复核。
- M `activity_types/playdate.txt`；+24/-107 行；未作语义复核。
- M `activity_types/tour.txt`；+112/-53 行；未作语义复核。
- M `activity_types/tournament.txt`；+147/-127 行；未作语义复核。
- M `activity_types/university_visit.txt`；+301/-145 行；未作语义复核。
- M `activity_types/wedding.txt`；+141/-118 行；未作语义复核。
- M `activity_types/witch_ritual.txt`；+39/-155 行；未作语义复核。
- M `guest_invite_rules/_invite_rules.info`；+5/-0 行；未作语义复核。
- M `guest_invite_rules/activity_invite_rules.txt`；+185/-12 行；未作语义复核。
- M `intents/chariot_race_intents.txt`；+15/-15 行；未作语义复核。
- M `intents/coronation_intents.txt`；+4/-0 行；已复核关键定义/差异。
- A `intents/ecumenical_council_intents.txt`；+279/-0 行；未作语义复核。
- M `intents/education_intents.txt`；+2/-2 行；未作语义复核。
- M `intents/imperial_examination_intents.txt`；+10/-10 行；未作语义复核。
- M `intents/journey_intents.txt`；+1/-1 行；未作语义复核。
- M `intents/shared_intents.txt`；+1/-0 行；未作语义复核。
- A `intents/spread_tenet_intents.txt`；+114/-0 行；未作语义复核。
- M `intents/tour_intents.txt`；+6/-6 行；未作语义复核。
- M `intents/tournament_intents.txt`；+1/-1 行；未作语义复核。
- M `intents/wedding_intents.txt`；+2/-0 行；未作语义复核。
- M `pulse_actions/education_actions.txt`；+131/-135 行；未作语义复核。
- M `pulse_actions/feast_pulse_actions.txt`；+6/-6 行；未作语义复核。
- M `pulse_actions/feast_pulse_actions_oltner.txt`；+8/-1 行；已复核关键定义/差异。
- M `pulse_actions/festival_actions.txt`；+10/-28 行；未作语义复核。
- M `pulse_actions/hunt_pulse_actions.txt`；+3/-1 行；未作语义复核。
- M `pulse_actions/imperial_examination_actions.txt`；+2/-2 行；未作语义复核。
- M `pulse_actions/journey_actions.txt`；+12/-12 行；未作语义复核。
- A `pulse_actions/pam_mendicant_preachers_apa.txt`；+46/-0 行；未作语义复核。
- A `pulse_actions/passive_rite_learning_apa.txt`；+190/-0 行；未作语义复核。
- M `pulse_actions/pilgrimage_actions.txt`；+4/-4 行；未作语义复核。
- M `pulse_actions/roaming_actions.txt`；+40/-38 行；未作语义复核。
- A `pulse_actions/spread_tenet_apa.txt`；+150/-0 行；未作语义复核。
- M `pulse_actions/tour_actions.txt`；+3/-24 行；未作语义复核。
- M `pulse_actions/wedding_pulse_actions.txt`；+37/-9 行；未作语义复核。

#### game/common/artifacts/（18 个变化路径）

- M `features/00_features.txt`；+46/-17 行；未作语义复核。
- M `slots/00_default.txt`；+68/-9 行；未作语义复核。
- A `slots/01_holy_site.txt`；+20/-0 行；已复核关键定义/差异。
- A `slots/_slots.info`；+47/-0 行；未作语义复核。
- A `templates/00_badge_templates.txt`；+14/-0 行；未作语义复核。
- M `templates/00_event_templates.txt`；+33/-4 行；未作语义复核。
- M `templates/00_historical_artifacts_templates.txt`；+257/-37 行；未作语义复核。
- M `templates/00_type_templates.txt`；+38/-0 行；未作语义复核。
- M `templates/02_ep3_templates.txt`；+5/-5 行；未作语义复核。
- M `templates/_templates.info`；+24/-7 行；未作语义复核。
- A `templates/pam_saint_relic_templates.txt`；+72/-0 行；已复核关键定义/差异。
- M `types/00_types.txt`；+8/-3 行；未作语义复核。
- M `types/_types.info`；+1/-1 行；未作语义复核。
- M `visuals/00_court_artifacts.txt`；+14/-9 行；未作语义复核。
- M `visuals/00_historical.txt`；+14/-14 行；未作语义复核。
- M `visuals/00_personal_misc.txt`；+42/-13 行；未作语义复核。
- M `visuals/06_ce1_artifacts.txt`；+1/-1 行；未作语义复核。
- A `visuals/10_ce3_artifacts.txt`；+103/-0 行；未作语义复核。

#### game/common/bookmark_portraits/（9 个变化路径）

- A `bookmark_adalwin_salzburg.txt`；+171/-0 行；未作语义复核。
- A `bookmark_bulgaria_boris.txt`；+162/-0 行；未作语义复核。
- A `bookmark_bulgaria_boris_alt_son.txt`；+162/-0 行；未作语义复核。
- A `bookmark_bulgaria_boris_alt_wife.txt`；+163/-0 行；未作语义复核。
- A `bookmark_hamburg_rimbert.txt`；+175/-0 行；未作语义复核。
- A `bookmark_lupus_aquileia.txt`；+172/-0 行；未作语义复核。
- A `bookmark_moravia_rostislav.txt`；+171/-0 行；未作语义复核。
- A `bookmark_moravia_rostislav_alt_svatopluk.txt`；+167/-0 行；未作语义复核。
- A `historical_export_easteregg_thea_ariens.txt`；+149/-0 行；未作语义复核。

#### game/common/bookmarks/（2 个变化路径）

- M `bookmarks/00_bookmarks.txt`；+465/-318 行；未作语义复核。
- M `challenge_characters/00_challenge_characters.txt`；+33/-33 行；未作语义复核。

#### game/common/buildings/（15 个变化路径）

- M `00_castle_buildings.txt`；+60/-4 行；未作语义复核。
- M `00_common_buildings.txt`；+80/-0 行；未作语义复核。
- M `00_duchy_capital_buildings.txt`；+32/-32 行；未作语义复核。
- M `00_special_buildings.txt`；+27/-17 行；未作语义复核。
- M `00_standard_economy_buildings.txt`；+1/-1 行；已复核关键定义/差异。
- M `00_standard_military_buildings.txt`；+1/-1 行；已复核关键定义/差异。
- M `00_temple_buildings.txt`；+204/-86 行；未作语义复核。
- M `00_tribal_buildings.txt`；+26/-14 行；未作语义复核。
- M `_buildings.info`；+14/-19 行；未作语义复核。
- M `ccp3_special_buildings.txt`；+4/-2 行；未作语义复核。
- M `cp6_special_buildings.txt`；+6/-4 行；未作语义复核。
- M `cp8_special_buildings.txt`；+1/-1 行；已复核关键定义/差异。
- A `pam_buildings.txt`；+542/-0 行；未作语义复核。
- M `temple_citadel_buildings.txt`；+77/-24 行；未作语义复核。
- M `tgp_great_project_buildings.txt`；+1/-1 行；未作语义复核。

#### game/common/casus_belli_groups/（1 个变化路径）

- M `00_casus_belli_groups.txt`；+33/-0 行；未作语义复核。

#### game/common/casus_belli_types/（28 个变化路径）

- M `00_civil_war.txt`；+56/-173 行；未作语义复核。
- M `00_claim.txt`；+38/-28 行；未作语义复核。
- M `00_conquest.txt`；+10/-2 行；未作语义复核。
- M `00_dejure_war.txt`；+14/-2 行；未作语义复核。
- A `00_dissolve_empire_cb.txt`；+262/-0 行；已复核关键定义/差异。
- M `00_event_war.txt`；+23/-20 行；未作语义复核。
- M `00_invasion_war.txt`；+26/-16 行；未作语义复核。
- M `00_nomadic_conquest.txt`；+3/-2 行；未作语义复核。
- M `00_peasant_war_new.txt`；+7/-4 行；未作语义复核。
- M `00_religious_war.txt`；+398/-371 行；未作语义复核。
- M `00_struggle_war.txt`；+2/-2 行；未作语义复核。
- M `00_subjugation.txt`；+84/-59 行；未作语义复核。
- M `00_tributarize.txt`；+6/-4 行；未作语义复核。
- M `00_vassalization.txt`；+6/-25 行；未作语义复核。
- M `01_ep1_wars.txt`；+16/-16 行；未作语义复核。
- M `01_fp1_wars.txt`；+2/-2 行；未作语义复核。
- M `03_fp2_wars.txt`；+6/-6 行；未作语义复核。
- M `05_fp3_wars.txt`；+8/-7 行；未作语义复核。
- M `06_ce1_wars.txt`；+5/-26 行；未作语义复核。
- M `07_ep3_admin_cbs.txt`；+49/-49 行；未作语义复核。
- M `07_ep3_wars.txt`；+154/-190 行；未作语义复核。
- M `09_mpo_wars.txt`；+29/-28 行；未作语义复核。
- M `10_tgp_china_wars.txt`；+20/-38 行；未作语义复核。
- M `10_tgp_faction_wars.txt`；+8/-8 行；未作语义复核。
- M `10_tgp_japan_wars.txt`；+207/-315 行；未作语义复核。
- M `_casus_belli.info`；+14/-0 行；未作语义复核。
- A `pam_wars.txt`；+833/-0 行；未作语义复核。
- M `tgp_eastasia_wars.txt`；+45/-109 行；未作语义复核。

#### game/common/character_interaction_categories/（1 个变化路径）

- M `00_character_interaction_categories.txt`；+38/-16 行；未作语义复核。

#### game/common/character_interactions/（67 个变化路径）

- A `00_accolade_interactions.txt`；+177/-0 行；未作语义复核。
- M `00_adoption.txt`；+148/-133 行；未作语义复核。
- M `00_alliance.txt`；+1043/-1486 行；未作语义复核。
- M `00_artifact_interactions.txt`；+510/-456 行；未作语义复核。
- M `00_blackmail_interactions.txt`；+48/-47 行；未作语义复核。
- M `00_ce1_interactions.txt`；+58/-26 行；未作语义复核。
- M `00_character_interactions.txt`；+327/-1093 行；未作语义复核。
- M `00_choose_favorite_interaction.txt`；+9/-3 行；未作语义复核。
- M `00_court_amenities_interactions.txt`；+17/-16 行；未作语义复核。
- M `00_courtier_and_guest_interactions.txt`；+79/-21 行；未作语义复核。
- M `00_culture_interactions.txt`；+13/-18 行；未作语义复核。
- M `00_debug_interactions.txt`；+408/-59 行；未作语义复核。
- A `00_demand_church_succession_interactions.txt`；+552/-0 行；未作语义复核。
- M `00_diarch_interactions.txt`；+505/-468 行；未作语义复核。
- M `00_dynast_interactions.txt`；+544/-352 行；未作语义复核。
- M `00_education_interactions.txt`；+511/-373 行；未作语义复核。
- M `00_faction_interactions.txt`；+24/-22 行；未作语义复核。
- M `00_fp3_interactions.txt`；+95/-82 行；未作语义复核。
- M `00_gift.txt`；+262/-140 行；未作语义复核。
- M `00_grant_titles_interaction.txt`；+446/-208 行；未作语义复核。
- M `00_heir.txt`；+80/-52 行；未作语义复核。
- M `00_house_head_interactions.txt`；+93/-78 行；未作语义复核。
- M `00_invite_agent_to_scheme.txt`；+19/-19 行；未作语义复核。
- M `00_invite_to_activity.txt`；+42/-13 行；未作语义复核。
- M `00_lease_interactions.txt`；+157/-12 行；未作语义复核。
- M `00_lover_interactions.txt`；+1/-1 行；未作语义复核。
- M `00_marriage_interactions.txt`；+2349/-679 行；未作语义复核。
- M `00_modifiy_vassal_contract.txt`；+285/-313 行；未作语义复核。
- M `00_mongol_interactions.txt`；+9/-8 行；未作语义复核。
- M `00_perk_interactions.txt`；+351/-272 行；未作语义复核。
- M `00_poetry_interactions.txt`；+36/-21 行；未作语义复核。
- M `00_prison_interactions.txt`；+1614/-1165 行；未作语义复核。
- A `00_puppet_interactions.txt`；+1233/-0 行；已复核关键定义/差异。
- M `00_religious_interactions.txt`；+6862/-2181 行；未作语义复核。
- M `00_revoke_title_interaction.txt`；+438/-453 行；未作语义复核。
- M `00_scheme_interactions.txt`；+1181/-493 行；未作语义复核。
- M `00_test_interactions.txt`；+107/-78 行；未作语义复核。
- M `00_tradition_interactions.txt`；+45/-28 行；未作语义复核。
- M `00_trait_interactions.txt`；+61/-52 行；未作语义复核。
- M `00_tribal_interactions.txt`；+87/-381 行；未作语义复核。
- M `00_tributary_interactions.txt`；+833/-714 行；未作语义复核。
- M `00_vassal_interactions.txt`；+583/-419 行；未作语义复核。
- M `00_war.txt`；+332/-515 行；未作语义复核。
- M `00_witch_interactions.txt`；+13/-11 行；未作语义复核。
- M `01_fp1_interactions.txt`；+106/-105 行；未作语义复核。
- A `01_puppet_interactions.txt`；+2486/-0 行；未作语义复核。
- M `02_ep1_interactions.txt`；+28/-18 行；未作语义复核。
- M `03_fp2_interactions.txt`；+507/-322 行；未作语义复核。
- M `05_bp2_interactions.txt`；+205/-186 行；未作语义复核。
- M `06_ep3_interactions.txt`；+732/-598 行；未作语义复核。
- M `06_ep3_laamp_interactions.txt`；+889/-314 行；未作语义复核。
- M `06_ep3_scheme_interactions.txt`；+459/-336 行；未作语义复核。
- M `06_ep3_test_interactions_.txt`；+9/-8 行；未作语义复核。
- M `09_mpo_interactions.txt`；+749/-1704 行；未作语义复核。
- M `10_ach_interactions.txt`；+140/-48 行；未作语义复核。
- M `10_tgp_interactions.txt`；+766/-510 行；未作语义复核。
- M `10_tgp_japan_interactions.txt`；+91/-92 行；未作语义复核。
- M `10_tgp_test_interactions.txt`；+6/-6 行；未作语义复核。
- A `11_petition_head_of_faith_interactions.txt`；+146/-0 行；未作语义复核。
- M `_character_interactions.info`；+101/-34 行；未作语义复核。
- A `clerical_chastity_interaction.txt`；+500/-0 行；未作语义复核。
- A `demand_child_as_monk_interaction.txt`；+939/-0 行；未作语义复核。
- A `pam_interactions.txt`；+28989/-0 行；已复核关键定义/差异。
- A `sanctify_artifact_interaction.txt`；+494/-0 行；未作语义复核。
- A `spiritual_counsel_interaction.txt`；+524/-0 行；未作语义复核。
- M `tgp_east_asia_interactions.txt`；+106/-93 行；未作语义复核。
- M `tgp_tribute_mission_interactions.txt`；+28/-22 行；未作语义复核。

#### game/common/character_memory_types/（4 个变化路径）

- M `character_memories_1.txt`；+80/-0 行；未作语义复核。
- M `ep3_memories.txt`；+4/-0 行；未作语义复核。
- A `pam_memories.txt`；+354/-0 行；未作语义复核。
- A `pam_secular_faith_memories.txt`；+93/-0 行；未作语义复核。

#### game/common/coat_of_arms/（10 个变化路径）

- A `coat_of_arms/01_cardinal_coas.txt`；+748/-0 行；未作语义复核。
- A `coat_of_arms/01_clerical_region_coas.txt`；+1279/-0 行；未作语义复核。
- M `coat_of_arms/01_holy_order_coas.txt`；+1135/-15 行；未作语义复核。
- M `coat_of_arms/01_landed_titles.txt`；+118/-32 行；未作语义复核。
- M `coat_of_arms/03_religious_icons.txt`；+899/-0 行；未作语义复核。
- M `coat_of_arms/90_dynasties.txt`；+1256/-86 行；未作语义复核。
- M `coat_of_arms/99_historical_character_coa.txt`；+87/-0 行；未作语义复核。
- A `coat_of_arms/pam_hegemony_titles.txt`；+27/-0 行；未作语义复核。
- M `template_lists/coa_templates.txt`；+192/-4 行；未作语义复核。
- M `template_lists/colored_emblem_lists.txt`；+544/-325 行；未作语义复核。

#### game/common/combat_phase_events/（2 个变化路径）

- M `00_commander_phase_events.txt`；+6/-6 行；未作语义复核。
- M `00_knight_phase_events.txt`；+13/-15 行；未作语义复核。

#### game/common/confederation_types/（1 个变化路径）

- M `00_confederation_types.txt`；+5/-6 行；未作语义复核。

#### game/common/council_positions/（2 个变化路径）

- M `00_council_positions.txt`；+250/-192 行；未作语义复核。
- M `01_ministry_positions.txt`；+14/-38 行；未作语义复核。

#### game/common/council_tasks/（5 个变化路径）

- M `00_chancellor_tasks.txt`；+0/-41 行；未作语义复核。
- M `00_court_chaplain_tasks.txt`；+300/-711 行；未作语义复核。
- M `00_kurultai_tasks.txt`；+8/-200 行；未作语义复核。
- M `00_marshal_tasks.txt`；+14/-1 行；未作语义复核。
- M `00_spymaster_tasks.txt`；+22/-0 行；未作语义复核。

#### game/common/court_positions/（15 个变化路径）

- M `tasks/00_court_guru_tasks.txt`；+1/-1 行；未作语义复核。
- M `tasks/00_court_physician_tasks.txt`；+1/-1 行；未作语义复核。
- M `tasks/00_executioner_tasks.txt`；+1/-1 行；未作语义复核。
- M `tasks/00_food_taster_tasks.txt`；+0/-10 行；未作语义复核。
- M `tasks/00_harem_manager_tasks.txt`；+12/-6 行；未作语义复核。
- M `tasks/00_seneschal_tasks.txt`；+13/-1 行；未作语义复核。
- M `tasks/00_stargazer_tasks.txt`；+1/-9 行；未作语义复核。
- M `tasks/00_wet_nurse_tasks.txt`；+1/-1 行；未作语义复核。
- M `types/00_admin_court_position.txt`；+22/-52 行；未作语义复核。
- M `types/00_camp_officers.txt`；+131/-356 行；未作语义复核。
- M `types/00_celestial_court_positions.txt`；+45/-152 行；未作语义复核。
- M `types/00_court_positions.txt`；+505/-1051 行；未作语义复核。
- M `types/00_mandala_court_positions.txt`；+17/-82 行；未作语义复核。
- M `types/00_mpo_court_positions.txt`；+70/-448 行；未作语义复核。
- M `types/_court_positions.info`；+2/-2 行；未作语义复核。

#### game/common/court_types/（1 个变化路径）

- M `00_court_types.txt`；+4/-4 行；未作语义复核。

#### game/common/courtier_guest_management/（1 个变化路径）

- M `guest_management.txt`；+21/-3 行；未作语义复核。

#### game/common/culture/（34 个变化路径）

- M `_cultural_traits.info`；+106/-48 行；未作语义复核。
- M `creation_names/_creation_names.info`；+30/-17 行；未作语义复核。
- M `cultures/00_baltic.txt`；+3/-3 行；未作语义复核。
- M `cultures/00_balto_finnic.txt`；+2/-2 行；未作语义复核。
- M `cultures/00_chinese.txt`；+2/-0 行；未作语义复核。
- M `cultures/00_latin.txt`；+2/-0 行；未作语义复核。
- M `cultures/00_magyar.txt`；+1/-0 行；未作语义复核。
- M `cultures/00_mongolic.txt`；+6/-0 行；未作语义复核。
- M `cultures/00_north_germanic.txt`；+3/-3 行；未作语义复核。
- M `cultures/00_turkic.txt`；+128/-112 行；未作语义复核。
- M `cultures/00_west_slavic.txt`；+5/-5 行；未作语义复核。
- M `cultures/_cultures.info`；+54/-32 行；未作语义复核。
- M `name_equivalency/00_names.txt`；+37/-34 行；未作语义复核。
- M `name_lists/00_balhae.txt`；+4/-0 行；未作语义复核。
- M `name_lists/00_chinese.txt`；+191/-0 行；未作语义复核。
- M `name_lists/00_east_slavic.txt`；+1/-1 行；未作语义复核。
- M `name_lists/00_frankish.txt`；+2/-2 行；未作语义复核。
- M `name_lists/00_goidelic.txt`；+2/-2 行；未作语义复核。
- M `name_lists/00_japanese.txt`；+1/-1 行；未作语义复核。
- M `name_lists/00_korean.txt`；+20/-0 行；未作语义复核。
- M `name_lists/00_mongolic.txt`；+2/-9 行；未作语义复核。
- M `pillars/00_ethos.txt`；+2/-1 行；未作语义复核。
- M `pillars/_pillars.info`；+53/-19 行；未作语义复核。
- M `traditions/00_combat_traditions.txt`；+1/-4 行；未作语义复核。
- M `traditions/00_maa_traditions.txt`；+7/-57 行；未作语义复核。
- M `traditions/00_realm_traditions.txt`；+34/-87 行；未作语义复核。
- M `traditions/00_regional_traditions.txt`；+13/-52 行；未作语义复核。
- M `traditions/00_ritual_traditions.txt`；+26/-22 行；未作语义复核。
- M `traditions/00_societal_traditions.txt`；+7/-7 行；未作语义复核。
- M `traditions/03_fp2_traditions.txt`；+3/-3 行；未作语义复核。
- M `traditions/03_fp3_traditions.txt`；+7/-5 行；未作语义复核。
- M `traditions/07_ep3_traditions.txt`；+40/-62 行；未作语义复核。
- M `traditions/_traditions.info`；+29/-34 行；未作语义复核。
- M `traditions/tgp_traditions.txt`；+109/-106 行；未作语义复核。

#### game/common/customizable_localization/（68 个变化路径）

- M `00_activity_loc.txt`；+164/-16 行；未作语义复核。
- M `00_adventurer_names.txt`；+51/-56 行；未作语义复核。
- M `00_appropriate_generic_words.txt`；+0/-10 行；未作语义复核。
- M `00_artifact_court_custom_loc.txt`；+289/-273 行；未作语义复核。
- M `00_artifact_custom_loc.txt`；+24/-11 行；未作语义复核。
- M `00_building_custom_localization.txt`；+32/-0 行；未作语义复核。
- M `00_casus_belli.txt`；+8/-2 行；未作语义复核。
- M `00_character_descriptions.txt`；+5528/-10 行；未作语义复核。
- M `00_character_interaction_categories.txt`；+5/-5 行；未作语义复核。
- M `00_compliment_custom_loc.txt`；+1570/-4 行；未作语义复核。
- M `00_conversation_subjects.txt`；+47/-1 行；未作语义复核。
- M `00_councillor_custom_loc.txt`；+52/-0 行；未作语义复核。
- M `00_curses_custom_loc.txt`；+24/-0 行；未作语义复核。
- M `00_diarchy_custom_loc.txt`；+15/-15 行；未作语义复核。
- M `00_divinity_custom_loc.txt`；+1829/-190 行；未作语义复核。
- M `00_es_custom_loc.txt`；+6/-6 行；未作语义复核。
- M `00_event_custom_loc.txt`；+4/-4 行；未作语义复核。
- M `00_food_custom_loc.txt`；+757/-223 行；未作语义复核。
- M `00_generic_character_words.txt`；+270/-314 行；未作语义复核。
- M `00_government_custom_loc.txt`；+208/-20 行；未作语义复核。
- M `00_greeting_custom_loc.txt`；+1661/-8 行；未作语义复核。
- M `00_historical_character_loc.txt`；+500/-6 行；未作语义复核。
- M `00_hold_court_custom_joe.txt`；+12/-12 行；未作语义复核。
- M `00_insult_custom_loc.txt`；+2541/-105 行；未作语义复核。
- M `00_interactions_custom_loc.txt`；+5/-3 行；未作语义复核。
- M `00_language_custom_loc.txt`；+94/-58 行；未作语义复核。
- M `00_love_letter_custom_loc.txt`；+27/-2 行；未作语义复核。
- M `00_lover_custom_localization.txt`；+341/-4 行；未作语义复核。
- M `00_martial_lifestyle_custom_loc.txt`；+30/-0 行；未作语义复核。
- M `00_pet_custom_loc.txt`；+243/-0 行；未作语义复核。
- M `00_pilgrimage_custom_loc.txt`；+1/-1 行；未作语义复核。
- M `00_pl_custom_loc_extra.txt`；+204/-204 行；未作语义复核。
- M `00_regional_custom_localization.txt`；+1273/-27 行；未作语义复核。
- M `00_relations.txt`；+269/-109 行；未作语义复核。
- M `00_rich_presence_flavor_status.txt`；+46/-46 行；未作语义复核。
- A `00_rite_desc_custom_loc.txt`；+1082/-0 行；未作语义复核。
- M `00_ruler_transition_loc.txt`；+69/-39 行；未作语义复核。
- M `00_servants.txt`；+87/-87 行；未作语义复核。
- M `00_task_contract_custom_loc.txt`；+2/-2 行；未作语义复核。
- M `00_title_custom_loc.txt`；+7/-0 行；未作语义复核。
- M `00_trait_custom_loc.txt`；+35/-35 行；未作语义复核。
- M `00_travel.txt`；+32/-0 行；未作语义复核。
- M `00_unfriendly_custom_loc.txt`；+74/-0 行；未作语义复核。
- M `00_war_custom_loc.txt`；+264/-25 行；未作语义复核。
- M `01_bp1_custom_loc.txt`；+7/-0 行；未作语义复核。
- M `01_ep1_custom_loc.txt`；+77/-12 行；未作语义复核。
- M `01_fp1_custom_loc.txt`；+5/-5 行；未作语义复核。
- M `04_ep2_custom_loc.txt`；+18/-5 行；未作语义复核。
- M `04_ep2_hunt_custom_loc.txt`；+7/-1 行；未作语义复核。
- M `05_bp2_custom_loc.txt`；+21/-3 行；未作语义复核。
- M `06_ce1_legends_custom_loc.txt`；+0/-2 行；未作语义复核。
- M `07_ep3_custom_loc.txt`；+3/-3 行；未作语义复核。
- M `08_bp3_experimental_brew_loc.txt`；+2/-2 行；未作语义复核。
- M `09_mpo_custom_loc.txt`；+2/-1 行；未作语义复核。
- M `10_ach_custom_loc.txt`；+49/-54 行；未作语义复核。
- M `10_tgp_custom_loc.txt`；+74/-5 行；未作语义复核。
- M `99_fr_custom_loc.txt`；+6/-6 行；未作语义复核。
- M `99_ru_custom_loc.txt`；+3890/-0 行；未作语义复核。
- A `ecumenical_council_debate_status_loc.txt`；+475/-0 行；未作语义复核。
- A `pam_bible_quotes.txt`；+11639/-0 行；未作语义复核。
- A `pam_custom_loc.txt`；+467/-0 行；未作语义复核。
- A `pam_saint_custom_loc.txt`；+599/-0 行；未作语义复核。
- A `pam_study_scripture_custom_loc.txt`；+176/-0 行；未作语义复核。
- A `pam_sway_to_rite_custom_loc.txt`；+121/-0 行；未作语义复核。
- A `pam_tenet_popularity.txt`；+33/-0 行；未作语义复核。
- A `sanctify_artifact_custom_loc.txt`；+57/-0 行；未作语义复核。
- M `tgp_custom_loc.txt`；+8/-8 行；未作语义复核。
- M `tgp_mandala_custom_loc.txt`；+8/-8 行；未作语义复核。

#### game/common/deathreasons/（1 个变化路径）

- M `00_event_deaths.txt`；+21/-2 行；未作语义复核。

#### game/common/decision_group_types/（1 个变化路径）

- M `00_decision_group_types.txt`；+4/-0 行；未作语义复核。

#### game/common/decisions/（73 个变化路径）

- M `00_artifact_decisions.txt`；+109/-14 行；未作语义复核。
- M `00_cultural_tradition_decisions.txt`；+72/-51 行；未作语义复核。
- M `00_diarchy_decisions.txt`；+3/-3 行；未作语义复核。
- M `00_dynasty_decisions.txt`；+94/-90 行；未作语义复核。
- M `00_fp3_decisions.txt`；+117/-89 行；未作语义复核。
- M `00_guest_decisions.txt`；+4/-4 行；未作语义复核。
- M `00_holy_order_decisions.txt`；+845/-70 行；已复核关键定义/差异。
- M `00_lifestyle_decisions.txt`；+15/-9 行；未作语义复核。
- M `00_major_decisions_east_europe.txt`；+295/-211 行；未作语义复核。
- M `00_major_decisions_iberia_north_africa.txt`；+51/-463 行；未作语义复核。
- M `00_trait_decisions.txt`；+8/-4 行；未作语义复核。
- M `00_unity_decisions.txt`；+29/-28 行；未作语义复核。
- M `06_ce1_decisions.txt`；+20/-29 行；未作语义复核。
- M `10_ach_oath_decisions.txt`；+27/-27 行；未作语义复核。
- M `10_culture_conversion_decisions.txt`；+13/-13 行；未作语义复核。
- M `10_nomad_culture_and_faith_decisions.txt`；+27/-26 行；未作语义复核。
- M `10_nomad_other_decisions.txt`；+19/-21 行；未作语义复核。
- M `10_religious_decisions.txt`；+1698/-687 行；未作语义复核。
- M `30_activity_decisions.txt`；+4/-15 行；未作语义复核。
- M `30_court_decisions.txt`；+6/-6 行；未作语义复核。
- M `30_mongol_invasion_decisions.txt`；+7/-10 行；未作语义复核。
- M `40_japan_decisions.txt`；+18/-18 行；未作语义复核。
- A `50_holy_site_decisions.txt`；+908/-0 行；已复核关键定义/差异。
- M `80_major_decisions.txt`；+282/-155 行；未作语义复核。
- M `80_major_decisions_british_isles.txt`；+105/-106 行；未作语义复核。
- M `80_major_decisions_central_asia.txt`；+29/-30 行；未作语义复核。
- M `80_major_decisions_east_asia.txt`；+23/-19 行；未作语义复核。
- M `80_major_decisions_middle_east.txt`；+88/-86 行；未作语义复核。
- M `80_major_decisions_middle_europe.txt`；+214/-245 行；未作语义复核。
- M `80_major_decisions_roman.txt`；+181/-168 行；未作语义复核。
- M `80_major_decisions_south_asia.txt`；+59/-58 行；未作语义复核。
- M `90_minor_decisions.txt`；+116/-46 行；未作语义复核。
- M `_decisions.info`；+269/-83 行；未作语义复核。
- A `clerical_chastity_decisions.txt`；+45/-0 行；未作语义复核。
- M `dlc_decisions/03_fp2_decisions.txt`；+103/-112 行；未作语义复核。
- M `dlc_decisions/bp3/00_bp3_other_decisions.txt`；+37/-37 行；未作语义复核。
- M `dlc_decisions/bp_2/00_bp2_other_decisions.txt`；+39/-26 行；未作语义复核。
- M `dlc_decisions/ep3_decisions.txt`；+252/-265 行；未作语义复核。
- M `dlc_decisions/ep_1/00_ep1_court_grandeur_and_amenity_decisions.txt`；+23/-23 行；未作语义复核。
- M `dlc_decisions/ep_1/00_ep1_other_decisions.txt`；+23/-23 行；未作语义复核。
- M `dlc_decisions/ep_2/00_ep2_other_decisions.txt`；+8/-8 行；未作语义复核。
- M `dlc_decisions/ep_3/06_ep3_admin_decisions.txt`；+87/-120 行；未作语义复核。
- M `dlc_decisions/ep_3/06_ep3_hasan_story_cycle_decisions.txt`；+33/-36 行；未作语义复核。
- M `dlc_decisions/ep_3/06_ep3_laamp_decisions.txt`；+233/-165 行；未作语义复核。
- M `dlc_decisions/ep_3/06_ep3_separatist_uprising_decision.txt`；+9/-6 行；未作语义复核。
- M `dlc_decisions/fp3_decisions.txt`；+55/-52 行；未作语义复核。
- M `dlc_decisions/fp_1/00_fp1_major_decisions.txt`；+88/-82 行；未作语义复核。
- M `dlc_decisions/fp_1/00_fp1_other_decisions.txt`；+5/-5 行；未作语义复核。
- M `dlc_decisions/fp_3/fp3_dynasty_decisions.txt`；+4/-4 行；未作语义复核。
- M `dlc_decisions/fp_3/fp3_islamic_decisions.txt`；+52/-78 行；未作语义复核。
- M `dlc_decisions/fp_3/fp3_scholarship_decisions.txt`；+3/-3 行；未作语义复核。
- M `dlc_decisions/fp_3/fp3_zoroastrian_decisions.txt`；+42/-44 行；未作语义复核。
- M `dlc_decisions/mpo/09_mpo_decisions_2.txt`；+7/-7 行；未作语义复核。
- M `dlc_decisions/mpo/mpo_court_astrologer_decision.txt`；+1/-1 行；未作语义复核。
- M `dlc_decisions/mpo/mpo_decisions.txt`；+115/-407 行；未作语义复核。
- M `dlc_decisions/mpo/mpo_flavor_decision.txt`；+52/-37 行；未作语义复核。
- M `dlc_decisions/mpo/mpo_pax_mongolica_decision.txt`；+1/-1 行；未作语义复核。
- A `dlc_decisions/pam/bulls_decisions.txt`；+945/-0 行；未作语义复核。
- A `dlc_decisions/pam/pam_adorcism_decisions.txt`；+279/-0 行；未作语义复核。
- A `dlc_decisions/pam/pam_antipope_decisions.txt`；+572/-0 行；已复核关键定义/差异。
- A `dlc_decisions/pam/pam_decisions.txt`；+6517/-0 行；未作语义复核。
- A `dlc_decisions/pam/pam_saint_decisions.txt`；+646/-0 行；未作语义复核。
- M `dlc_decisions/tgp/tgp_china_decisions.txt`；+82/-31 行；未作语义复核。
- M `dlc_decisions/tgp/tgp_culture_decisions.txt`；+3/-3 行；未作语义复核。
- M `dlc_decisions/tgp/tgp_dynastic_cycle_decisions.txt`；+50/-50 行；未作语义复核。
- M `dlc_decisions/tgp/tgp_east_asia_decisions.txt`；+81/-62 行；未作语义复核。
- M `dlc_decisions/tgp/tgp_japan_decisions.txt`；+92/-98 行；未作语义复核。
- M `dlc_decisions/tgp/tgp_korea_decisions.txt`；+16/-17 行；未作语义复核。
- M `dlc_decisions/tgp/tgp_silk_road_decisions.txt`；+6/-5 行；未作语义复核。
- M `dlc_decisions/tgp/tgp_steppe_decisions.txt`；+13/-19 行；未作语义复核。
- M `dlc_decisions/tgp/tgp_tenet_decisions.txt`；+5/-1 行；未作语义复核。
- M `dlc_decisions/tgp/tgp_tribute_mission_decisions.txt`；+2/-2 行；未作语义复核。
- M `tutorial_decisions.txt`；+6/-25 行；未作语义复核。

#### game/common/defines/（4 个变化路径）

- M `00_defines.txt`；+108/-11 行；已复核关键定义/差异。
- M `ai/00_ai.txt`；+39/-0 行；已复核关键定义/差异。
- M `audio/00_audio.txt`；+2/-0 行；未作语义复核。
- M `graphic/00_graphics.txt`；+47/-4 行；已复核关键定义/差异。

#### game/common/diarchies/（1 个变化路径）

- M `diarchy_types/00_primeministerships.txt`；+2/-1 行；未作语义复核。

#### game/common/dna_data/（2 个变化路径）

- M `00_dna.txt`；+352/-0 行；未作语义复核。
- M `01_easteregg_dna.txt`；+918/-0 行；未作语义复核。

#### game/common/domiciles/（7 个变化路径）

- M `buildings/00_camp_buildings.txt`；+6/-2 行；未作语义复核。
- M `buildings/00_chinese_estate_buildings.txt`；+53/-52 行；未作语义复核。
- M `buildings/00_estate_buildings.txt`；+180/-159 行；未作语义复核。
- M `buildings/00_yurt_buildings.txt`；+6/-19 行；未作语义复核。
- M `buildings/10_japanese_manor_buildings.txt`；+78/-78 行；未作语义复核。
- A `buildings/11_ecclesiastical_domicile_buildings.txt`；+11946/-0 行；未作语义复核。
- M `types/00_domicile_types.txt`；+834/-4 行；未作语义复核。

#### game/common/dynasties/（4 个变化路径）

- M `00_dynasties.txt`；+220/-63 行；未作语义复核。
- M `01_vanity_dynasties.txt`；+48/-0 行；未作语义复核。
- M `04_ep3_dynasties.txt`；+2/-2 行；未作语义复核。
- M `05_historical_character_dynasties.txt`；+165/-0 行；未作语义复核。

#### game/common/dynasty_house_motto_inserts/（1 个变化路径）

- M `00_inserts.txt`；+1/-1 行；未作语义复核。

#### game/common/dynasty_houses/（3 个变化路径）

- M `00_dynasty_houses.txt`；+91/-2 行；未作语义复核。
- M `99_historical_character_houses.txt`；+155/-0 行；未作语义复核。
- M `ep3_dynasty_houses.txt`；+1/-1 行；未作语义复核。

#### game/common/dynasty_legacies/（3 个变化路径）

- A `81_pam_legacies.txt`；+18/-0 行；未作语义复核。
- M `83_ep3_legacies.txt`；+1/-1 行；未作语义复核。
- M `96_fp2_legacies.txt`；+8/-2 行；未作语义复核。

#### game/common/dynasty_perks/（5 个变化路径）

- M `00_dynasty_perks.txt`；+8/-8 行；未作语义复核。
- M `05_ce1_dynasty_perks.txt`；+2/-2 行；未作语义复核。
- M `06_ep3_dynasty_perks.txt`；+1/-1 行；未作语义复核。
- A `09_pam_dynasty_perks.txt`；+107/-0 行；已复核关键定义/差异。
- M `_dynasty_perks.info`；+1/-1 行；未作语义复核。

#### game/common/effect_localization/（10 个变化路径）

- M `00_additional_effects.txt`；+1/-0 行；未作语义复核。
- M `00_character_effects.txt`；+67/-0 行；未作语义复核。
- M `00_custom_effects.txt`；+6/-10 行；未作语义复核。
- M `00_dynasty_effects.txt`；+2/-1 行；未作语义复核。
- M `00_perk_effects.txt`；+53/-0 行；未作语义复核。
- M `00_religion_effects.txt`；+40/-10 行；未作语义复核。
- M `00_title_effects.txt`；+1/-0 行；未作语义复核。
- M `00_war_effects.txt`；+6/-0 行；未作语义复核。
- M `09_situation_effects.txt`；+2/-0 行；未作语义复核。
- A `pam_effects.txt`；+71/-0 行；未作语义复核。

#### game/common/epidemics/（1 个变化路径）

- M `00_epidemics.txt`；+4/-6 行；未作语义复核。

#### game/common/ethnicities/（2 个变化路径）

- M `00_ethnicities_templates.txt`；+246/-242 行；未作语义复核。
- M `00_ethnicities_vanity_characters.txt`；+8/-4 行；未作语义复核。

#### game/common/event_backgrounds/（2 个变化路径）

- M `01_event_backgrounds.txt`；+1839/-147 行；未作语义复核。
- M `activity_backgrounds.txt`；+78/-3 行；未作语义复核。

#### game/common/event_themes/（1 个变化路径）

- M `00_event_themes.txt`；+86/-4 行；未作语义复核。

#### game/common/factions/（6 个变化路径）

- M `00_factions.txt`；+63/-101 行；未作语义复核。
- M `00_nation_fracturing_faction.txt`；+29/-29 行；未作语义复核。
- M `00_nomadic_faction.txt`；+1/-0 行；未作语义复核。
- M `00_peasant_faction_new.txt`；+6/-7 行；未作语义复核。
- M `00_populist_faction.txt`；+102/-90 行；未作语义复核。
- M `10_tgp_factions.txt`；+10/-17 行；未作语义复核。

#### game/common/flavorization/（6 个变化路径）

- M `00_title_holders.txt`；+1206/-374 行；未作语义复核。
- M `01_domicile.txt`；+52/-0 行；未作语义复核。
- M `10_tgp_japan_flavorization.txt`；+24/-24 行；未作语义复核。
- M `10_tgp_korea_flavorization.txt`；+1/-1 行；未作语义复核。
- A `20_pam_flavorization.txt`；+394/-0 行；未作语义复核。
- M `_flavourization.info`；+56/-3 行；未作语义复核。

#### game/common/focuses/（1 个变化路径）

- M `00_lifestyle_focuses.txt`；+1/-1 行；未作语义复核。

#### game/common/game_concepts/（7 个变化路径）

- M `00_game_concepts.txt`；+85/-26 行；未作语义复核。
- M `04_ep2_game_concepts.txt`；+1/-2 行；未作语义复核。
- M `07_ep3_game_concepts.txt`；+1/-1 行；未作语义复核。
- A `10_empire_faith_gate_game_concepts.txt`；+4/-0 行；未作语义复核。
- M `mpo_game_concepts.txt`；+1/-1 行；未作语义复核。
- A `pam_game_concepts.txt`；+464/-0 行；未作语义复核。
- M `tgp_game_concepts.txt`；+19/-21 行；未作语义复核。

#### game/common/game_rules/（2 个变化路径）

- M `00_game_rules.txt`；+108/-0 行；未作语义复核。
- A `01_empire_faith_gate_rules.txt`；+11/-0 行；已复核关键定义/差异。

#### game/common/genes/（8 个变化路径）

- M `01_genes_morph.txt`；+3/-0 行；未作语义复核。
- M `02_genes_accessories_misc.txt`；+55/-54 行；未作语义复核。
- M `03_genes_special_accessories_hairstyles.txt`；+82/-16 行；未作语义复核。
- M `04_genes_special_accessories_beards.txt`；+48/-0 行；未作语义复核。
- M `05_genes_special_accessories_clothes.txt`；+477/-91 行；未作语义复核。
- M `06_genes_special_accessories_headgear.txt`；+300/-103 行；未作语义复核。
- M `07_genes_special_accessories_misc.txt`；+196/-2 行；未作语义复核。
- M `08_genes_special_visual_traits.txt`；+13/-0 行；未作语义复核。

#### game/common/governments/（4 个变化路径）

- M `00_government_types.txt`；+181/-77 行；已复核关键定义/差异。
- M `01_japan_government_types.txt`；+14/-8 行；已复核关键定义/差异。
- A `02_theocratic_government_types.txt`；+161/-0 行；已复核关键定义/差异。
- M `_governments.info`；+60/-23 行；未作语义复核。

#### game/common/great_projects/（5 个变化路径）

- M `types/00_great_project_types.txt`；+584/-514 行；未作语义复核。
- M `types/00_ministry_projects.txt`；+342/-363 行；未作语义复核。
- M `types/00_natural_disasters.txt`；+30/-26 行；未作语义复核。
- A `types/01_pam_projects.txt`；+6432/-0 行；已复核关键定义/差异。
- M `types/_great_project_types.info`；+30/-2 行；未作语义复核。

#### game/common/holy_orders/（4 个变化路径）

- A `00_christian_holy_orders.txt`；+9785/-0 行；未作语义复核。
- A `00_generic_holy_orders.txt`；+7149/-0 行；未作语义复核。
- A `00_muslim_holy_orders.txt`；+789/-0 行；未作语义复核。
- A `_holy_orders.info`；+108/-0 行；未作语义复核。

#### game/common/hook_types/（1 个变化路径）

- M `00_hook_types.txt`；+22/-2 行；未作语义复核。

#### game/common/house_aspirations/（2 个变化路径）

- M `00_admin_house_powers.txt`；+156/-234 行；未作语义复核。
- M `10_tgp_celestial_house_powers.txt`；+5/-5 行；未作语义复核。

#### game/common/important_actions/（16 个变化路径）

- M `00_inheritance_actions.txt`；+100/-33 行；未作语义复核。
- M `00_marriage_actions.txt`；+1/-1 行；未作语义复核。
- M `00_personal_actions.txt`；+22/-3 行；未作语义复核。
- M `00_reactive_advice.txt`；+167/-25 行；未作语义复核。
- M `00_realm_actions.txt`；+31/-34 行；未作语义复核。
- M `00_title_actions.txt`；+8/-4 行；未作语义复核。
- M `00_war_actions.txt`；+7/-7 行；未作语义复核。
- M `01_bp1_actions.txt`；+1/-1 行；未作语义复核。
- M `01_ep1_actions.txt`；+5/-2 行；未作语义复核。
- M `01_fp1_actions.txt`；+4/-2 行；未作语义复核。
- M `06_ce1_actions.txt`；+1/-1 行；未作语义复核。
- M `07_ep3_actions.txt`；+4/-2 行；未作语义复核。
- M `09_mpo_actions.txt`；+5/-1 行；未作语义复核。
- A `10_empire_faith_gate_actions.txt`；+79/-0 行；未作语义复核。
- A `pam_actions.txt`；+1574/-0 行；未作语义复核。
- M `tgp_actions.txt`；+25/-22 行；未作语义复核。

#### game/common/inspirations/（1 个变化路径）

- M `00_inspirations.txt`；+206/-35 行；未作语义复核。

#### game/common/landed_titles/（14 个变化路径）

- M `00_landed_titles.txt`；+1523/-335 行；未作语义复核。
- M `01_japan.txt`；+19/-1 行；未作语义复核。
- M `01_japan_noble_family.txt`；+364/-2 行；未作语义复核。
- M `01_korea_noble_family.txt`；+174/-2 行；未作语义复核。
- M `01_other_noble_family.txt`；+398/-2 行；未作语义复核。
- M `02_china.txt`；+73/-6 行；未作语义复核。
- M `03_seasia.txt`；+4/-0 行；未作语义复核。
- M `04_china_noble_families.txt`；+1560/-2 行；未作语义复核。
- M `05_goryeo.txt`；+342/-341 行；未作语义复核。
- M `06_philippines.txt`；+4/-0 行；未作语义复核。
- A `07_pam_ecclesiastical_titles.txt`；+1514/-0 行；未作语义复核。
- A `07_pam_hegemony_titles.txt`；+20/-0 行；未作语义复核。
- M `_landed_titles.info`；+62/-49 行；未作语义复核。
- A `title_conversion.lookup`；+4/-0 行；未作语义复核。

#### game/common/law_groups/（7 个变化路径）

- A `00_realm_law_groups.txt`；+76/-0 行；未作语义复核。
- A `00_succession_law_groups.txt`；+30/-0 行；未作语义复核。
- A `01_title_succession_law_groups.txt`；+5/-0 行；未作语义复核。
- A `02_admininistrative_law_groups.txt`；+95/-0 行；未作语义复核。
- A `03_imperial_policie_groups.txt`；+10/-0 行；未作语义复核。
- A `04_pam_ecclesiastical_law_groups.txt`；+22/-0 行；未作语义复核。
- A `_law_groups.info`；+45/-0 行；未作语义复核。

#### game/common/laws/（7 个变化路径）

- M `00_realm_laws.txt`；+3454/-3092 行；已复核关键定义/差异。
- M `00_succession_laws.txt`；+2457/-2060 行；已复核关键定义/差异。
- M `01_title_succession_laws.txt`；+371/-339 行；未作语义复核。
- M `02_admininistrative_laws.txt`；+3451/-3350 行；未作语义复核。
- M `03_imperial_policies.txt`；+377/-365 行；未作语义复核。
- A `04_pam_ecclesiastical_laws.txt`；+47/-0 行；未作语义复核。
- M `_laws.info`；+287/-301 行；未作语义复核。

#### game/common/lease_contracts/（2 个变化路径）

- M `00_theocracy_lease.txt`；+297/-64 行；未作语义复核。
- M `_lease_contracts.info`；+106/-30 行；未作语义复核。

#### game/common/legends/（3 个变化路径）

- M `chronicles/00_chronicles.txt`；+1/-1 行；未作语义复核。
- M `legend_seeds/00_legend_seeds.txt`；+1/-1 行；未作语义复核。
- M `legend_types/00_legends.txt`；+6/-3 行；未作语义复核。

#### game/common/legitimacy/（1 个变化路径）

- M `00_legitimacy.txt`；+41/-2 行；未作语义复核。

#### game/common/lifestyle_perks/（15 个变化路径）

- M `00_diplomacy_1_foreign_affairs_tree_perks.txt`；+35/-35 行；未作语义复核。
- M `00_diplomacy_2_majesty_tree_perks.txt`；+42/-42 行；未作语义复核。
- M `00_diplomacy_3_family_tree_perks.txt`；+23/-23 行；未作语义复核。
- M `00_intrigue_1_skulduggery_tree_perks.txt`；+11/-0 行；未作语义复核。
- M `00_intrigue_2_temptation_tree_perks.txt`；+1/-1 行；未作语义复核。
- M `00_learning_2_scholarship_tree_perks.txt`；+44/-12 行；已复核关键定义/差异。
- M `00_learning_3_theology_tree_perks.txt`；+78/-15 行；已复核关键定义/差异。
- M `00_martial_2_authority_tree_perks.txt`；+40/-40 行；未作语义复核。
- M `00_martial_3_chivalry_tree_perks.txt`；+28/-13 行；未作语义复核。
- M `00_stewardship_1_wealth_tree_perks.txt`；+10/-0 行；未作语义复核。
- M `00_stewardship_2_domain_tree_perks.txt`；+8/-0 行；未作语义复核。
- M `00_stewardship_3_duty_tree_perks.txt`；+53/-53 行；未作语义复核。
- M `00_wanderer_1_surveyor_tree_perks.txt`；+1/-1 行；未作语义复核。
- M `00_wanderer_2_wayfarer_tree_perks.txt`；+5/-0 行；未作语义复核。
- M `_lifestyle_perks.info`；+1/-1 行；未作语义复核。

#### game/common/lifestyles/（1 个变化路径）

- M `_lifestyles.info`；+2/-2 行；未作语义复核。

#### game/common/men_at_arms_types/（7 个变化路径）

- M `00_holy_order_maa_types.txt`；+93/-3 行；已复核关键定义/差异。
- M `00_maa_types.txt`；+19/-68 行；已复核关键定义/差异。
- M `00_regional_maa_types.txt`；+3/-0 行；未作语义复核。
- M `01_accolade_maa_types.txt`；+6/-0 行；未作语义复核。
- M `07_ep3_maa_types.txt`；+4/-1 行；未作语义复核。
- M `10_tgp_maa_types.txt`；+15/-40 行；已复核关键定义/差异。
- M `_men_at_arms_types.info`；+8/-2 行；未作语义复核。

#### game/common/menu_scenes/（1 个变化路径）

- A `_default_menu_scenes.info`；+38/-0 行；未作语义复核。

#### game/common/message_filter_types/（2 个变化路径）

- M `00_message_filter_types.txt`；+73/-4 行；未作语义复核。
- A `passive_rite_learning_message_filter_types.txt`；+8/-0 行；未作语义复核。

#### game/common/messages/（9 个变化路径）

- M `01_family_messages.txt`；+7/-0 行；未作语义复核。
- A `01_interaction_messages.txt`；+15/-0 行；未作语义复核。
- M `01_religious_messages.txt`；+84/-5 行；未作语义复核。
- M `01_title_messages.txt`；+22/-0 行；未作语义复核。
- M `01_vassal_messages.txt`；+15/-1 行；未作语义复核。
- M `04_ep2_messages.txt`；+7/-0 行；未作语义复核。
- A `10_pam_messages.txt`；+162/-0 行；未作语义复核。
- A `passive_rite_learning_messages.txt`；+39/-0 行；未作语义复核。
- M `tgp_messages.txt`；+14/-0 行；未作语义复核。

#### game/common/modifier_definition_formats/（4 个变化路径）

- M `00_definitions.txt`；+137/-2 行；未作语义复核。
- M `00_government_definitions.txt`；+37/-0 行；未作语义复核。
- M `00_religion_definitions.txt`；+7/-5 行；未作语义复核。
- M `00_scheme_definitions.txt`；+62/-6 行；未作语义复核。

#### game/common/modifiers/（29 个变化路径）

- M `00_activity_hunt_modifiers.txt`；+4/-0 行；未作语义复核。
- M `00_activity_pilgrimage_modifiers.txt`；+1/-1 行；未作语义复核。
- M `00_artifact_modifiers.txt`；+32/-1 行；未作语义复核。
- M `00_basic_modifiers.txt`；+6/-0 行；未作语义复核。
- M `00_court_position_modifiers.txt`；+16/-4 行；未作语义复核。
- A `00_empire_faith_gate_modifiers.txt`；+35/-0 行；已复核关键定义/差异。
- M `00_ep2_travel_modifiers.txt`；+6/-1 行；未作语义复核。
- M `00_governance_lifestyle_modifiers.txt`；+1/-0 行；未作语义复核。
- M `00_health_modifiers.txt`；+0/-5 行；未作语义复核。
- M `00_holy_order_modifiers.txt`；+17/-2 行；未作语义复核。
- M `00_laamp_modifiers.txt`；+24/-0 行；未作语义复核。
- M `00_martial_lifestyle_modifiers.txt`；+13/-0 行；未作语义复核。
- M `00_religion_modifiers.txt`；+45/-1 行；未作语义复核。
- M `00_scheme_modifiers.txt`；+29/-0 行；未作语义复核。
- M `00_yearly_event_modifiers.txt`；+1/-0 行；未作语义复核。
- M `01_dlc_fp3_modifiers.txt`；+1/-4 行；未作语义复核。
- M `01_inventory_modifiers.txt`；+1/-1 行；未作语义复核。
- M `03_dlc_fp2_modifiers.txt`；+7/-4 行；未作语义复核。
- M `04_ep2_modifiers.txt`；+5/-0 行；未作语义复核。
- M `07_ep3_laamp_flavor_modifiers.txt`；+5/-0 行；未作语义复核。
- M `07_ep3_modifiers.txt`；+19/-33 行；未作语义复核。
- A `11_pam_study_faith_modifiers.txt`；+64/-0 行；未作语义复核。
- A `11_pam_study_scripture_modifiers.txt`；+122/-0 行；未作语义复核。
- A `12_pam_modifiers.txt`；+1286/-0 行；未作语义复核。
- A `clerical_chastity_modifiers.txt`；+10/-0 行；未作语义复核。
- A `pam_county_modifiers.txt`；+11/-0 行；未作语义复核。
- A `pam_secular_faith_modifiers.txt`；+596/-0 行；未作语义复核。
- A `sanctify_artifact_modifiers.txt`；+5/-0 行；未作语义复核。
- A `titus_natural_primitivism_modifiers.txt`；+17/-0 行；未作语义复核。

#### game/common/morpheme_strip_rules/（3 个变化路径）

- A `00_morpheme_strip_rules.info`；+57/-0 行；未作语义复核。
- A `00_morpheme_strip_rules.txt`；+60/-0 行；未作语义复核。
- A `99_morpheme_strip_russian.txt`；+96/-0 行；未作语义复核。

#### game/common/named_colors/（1 个变化路径）

- M `culture_colors.txt`；+2/-2 行；未作语义复核。

#### game/common/nicknames/（2 个变化路径）

- M `00_nicknames.txt`；+47/-0 行；未作语义复核。
- A `11_pam_nicknames.txt`；+4/-0 行；未作语义复核。

#### game/common/on_action/（68 个变化路径）

- A `11_petition_head_of_faith_on_actions.txt`；+45/-0 行；未作语义复核。
- M `accolade_on_actions.txt`；+1/-1 行；未作语义复核。
- A `activities/ecumenical_council_on_actions.txt`；+122/-0 行；未作语义复核。
- M `activities/feast_on_actions.txt`；+7/-0 行；未作语义复核。
- M `activities/hunt_on_actions.txt`；+2/-0 行；未作语义复核。
- M `activities/pilgrimage_on_actions.txt`；+12/-6 行；未作语义复核。
- M `army_on_actions.txt`；+83/-10 行；未作语义复核。
- A `character_created_on_actions.txt`；+22/-0 行；未作语义复核。
- M `character_levels.txt`；+17/-16 行；未作语义复核。
- M `child_birth_on_actions.txt`；+470/-111 行；未作语义复核。
- M `childhood_on_actions.txt`；+156/-4 行；未作语义复核。
- M `combat_on_actions.txt`；+10/-4 行；未作语义复核。
- M `confederation_on_actions.txt`；+3/-5 行；未作语义复核。
- M `councillor_on_actions.txt`；+26/-12 行；未作语义复核。
- M `county_on_actions.txt`；+30/-0 行；未作语义复核。
- M `court_events.txt`；+2/-1 行；未作语义复核。
- M `court_maintenance_on_actions.txt`；+23/-1 行；未作语义复核。
- M `culture_on_actions.txt`；+19/-0 行；未作语义复核。
- M `death.txt`；+701/-412 行；未作语义复核。
- M `dlc/bp2/bp2_hostage_on_actions.txt`；+8/-5 行；未作语义复核。
- M `dlc/ce1/ce1_funeral_on_actions.txt`；+3/-0 行；未作语义复核。
- M `dlc/ep1/ep1_pay_homage_on_actions.txt`；+9/-9 行；未作语义复核。
- M `dlc/ep2/ep2_tournament_on_actions.txt`；+2/-0 行；未作语义复核。
- M `dlc/ep2/ep2_wedding_on_actions.txt`；+4/-3 行；未作语义复核。
- M `dlc/mpo/mpo_on_actions_2.txt`；+11/-98 行；未作语义复核。
- M `dlc/mpo/mpo_the_great_steppe_on_actions.txt`；+23/-24 行；未作语义复核。
- A `dlc/pam/pam_on_actions.txt`；+544/-0 行；未作语义复核。
- M `dlc/tgp/tgp_mandala_on_actions.txt`；+1/-1 行；未作语义复核。
- M `dlc/tgp/tgp_tribute_mission_on_actions.txt`；+3/-3 行；未作语义复核。
- M `dynasty_on_actions.txt`；+46/-4 行；未作语义复核。
- M `ep1_inspirations_on_actions.txt`；+1/-0 行；未作语义复核。
- M `ep3_on_actions.txt`；+3/-3 行；未作语义复核。
- M `game_start.txt`；+648/-1274 行；未作语义复核。
- M `governance_on_actions.txt`；+8/-16 行；未作语义复核。
- A `government_on_actions.txt`；+116/-0 行；未作语义复核。
- M `health_on_actions.txt`；+9/-3 行；未作语义复核。
- M `holy_order_on_actions.txt`；+503/-23 行；未作语义复核。
- M `inventory_on_actions.txt`；+428/-5 行；未作语义复核。
- M `lifestyles/diplomacy_lifestyle_on_actions.txt`；+5/-6 行；未作语义复核。
- M `lifestyles/intrigue_lifestyle_on_actions.txt`；+3/-4 行；未作语义复核。
- M `lifestyles/learning_lifestyle_on_actions.txt`；+3/-4 行；未作语义复核。
- M `lifestyles/martial_lifestyle_on_actions.txt`；+12/-55 行；未作语义复核。
- M `lifestyles/stewardship_lifestyle_on_actions.txt`；+5/-6 行；未作语义复核。
- M `marriage_concubinage.txt`；+76/-9 行；未作语义复核。
- M `mercenary_on_actions.txt`；+2/-0 行；未作语义复核。
- A `player_change_on_actions.txt`；+49/-0 行；未作语义复核。
- M `player_select_destiny_on_actions.txt`；+173/-29 行；未作语义复核。
- M `prison_on_actions.txt`；+16/-0 行；未作语义复核。
- M `province_on_actions.txt`；+180/-16 行；未作语义复核。
- M `relations/relation_on_actions.txt`；+14/-3 行；未作语义复核。
- M `relations/vassal_on_actions.txt`；+2/-2 行；未作语义复核。
- M `religion_on_actions.txt`；+1205/-157 行；未作语义复核。
- M `ruler_designer.txt`；+30/-2 行；未作语义复核。
- M `scheme_on_actions.txt`；+1/-0 行；未作语义复核。
- M `schemes/learn_language_on_actions.txt`；+6/-0 行；未作语义复核。
- M `schemes/murder_on_actions.txt`；+1/-1 行；未作语义复核。
- M `schemes/steal_back_artifact_on_actions.txt`；+4/-3 行；未作语义复核。
- A `schemes/study_faith_on_actions.txt`；+98/-0 行；未作语义复核。
- A `schemes/study_scripture_on_actions.txt`；+45/-0 行；未作语义复核。
- M `schemes/sway_on_actions.txt`；+29/-0 行；未作语义复核。
- M `stress_on_actions.txt`；+65/-0 行；未作语义复核。
- M `title_on_actions.txt`；+723/-90 行；未作语义复核。
- M `traits_on_actions.txt`；+77/-1 行；未作语义复核。
- M `travel_on_actions.txt`；+126/-22 行；未作语义复核。
- M `tutorial.txt`；+3/-3 行；未作语义复核。
- M `war_on_actions.txt`；+114/-1 行；未作语义复核。
- M `yearly_groups_on_actions.txt`；+127/-0 行；未作语义复核。
- M `yearly_on_actions.txt`；+657/-54 行；未作语义复核。

#### game/common/opinion_modifiers/（12 个变化路径）

- M `00_council_task_opinions.txt`；+1/-2 行；未作语义复核。
- M `00_crime_and_prison_opinions.txt`；+31/-3 行；未作语义复核。
- M `00_doctrinal_crime_opinions.txt`；+8/-1 行；未作语义复核。
- M `00_opinion_modifiers.txt`；+206/-1 行；未作语义复核。
- M `00_prison_opinions.txt`；+16/-2 行；未作语义复核。
- M `00_religious_opinions.txt`；+96/-8 行；未作语义复核。
- M `00_title_opinions.txt`；+7/-1 行；未作语义复核。
- A `clerical_chastity_opinions.txt`；+11/-0 行；未作语义复核。
- A `dlc/pam/pam_opinion_modifiers.txt`；+40/-0 行；未作语义复核。
- A `pam_opinions.txt`；+192/-0 行；未作语义复核。
- A `pam_secular_faith_opinions.txt`；+15/-0 行；未作语义复核。
- A `titus_natural_primitivism_opinions.txt`；+11/-0 行；未作语义复核。

#### game/common/playable_difficulty_infos/（1 个变化路径）

- M `00_playable_difficulty_infos.txt`；+8/-3 行；未作语义复核。

#### game/common/pool_character_selectors/（6 个变化路径）

- M `00_auto_characters.txt`；+12/-8 行；未作语义复核。
- M `00_city.txt`；+6/-19 行；未作语义复核。
- M `00_clergy.txt`；+10/-21 行；未作语义复核。
- M `00_herders.txt`；+8/-20 行；未作语义复核。
- M `00_holy_order.txt`；+284/-7 行；未作语义复核。
- M `00_mercenary.txt`；+1/-2 行；未作语义复核。

#### game/common/puppets/（4 个变化路径）

- A `actions/_puppet_actions.info`；+35/-0 行；未作语义复核。
- A `actions/puppet_actions.txt`；+657/-0 行；未作语义复核。
- A `types/_puppet_types.info`；+57/-0 行；未作语义复核。
- A `types/pam_puppet_types.txt`；+332/-0 行；未作语义复核。

#### game/common/raids/（1 个变化路径）

- M `intents/raid_intents.txt`；+38/-0 行；未作语义复核。

#### game/common/religion/（80 个变化路径）

- A `doctrine_category_types/00_doctrine_category_types.txt`；+26/-0 行；未作语义复核。
- A `doctrine_category_types/_doctrine_category_types.info`；+22/-0 行；未作语义复核。
- M `doctrine_group_types/00_doctrine_group_types.txt`；+125/-387 行；未作语义复核。
- M `doctrine_group_types/_doctrine_group_types.info`；+28/-15 行；未作语义复核。
- M `doctrine_types/10_doctrines_religions.txt`；+40/-16 行；未作语义复核。
- M `doctrine_types/20_doctrines.txt`；+1521/-742 行；未作语义复核。
- M `doctrine_types/20_doctrines_islam.txt`；+37/-15 行；未作语义复核。
- M `doctrine_types/20_doctrines_judaism.txt`；+54/-20 行；未作语义复核。
- M `doctrine_types/20_doctrines_zoroastrianism.txt`；+14/-4 行；未作语义复核。
- D `doctrine_types/30_core_tenets.txt`；+0/-4234 行；已复核关键定义/差异。
- M `doctrine_types/40_doctrines_special.txt`；+359/-137 行；未作语义复核。
- M `doctrine_types/_doctrine_types.info`；+230/-67 行；未作语义复核。
- A `faith_types/00_faith_types.txt`；+4867/-0 行；已复核关键定义/差异。
- A `faith_types/_faith_types.info`；+78/-0 行；已复核关键定义/差异。
- M `holy_site_types/00_holy_site_types.txt`；+5595/-821 行；未作语义复核。
- A `holy_site_types/01_dynamic_holy_site_types.txt`；+250/-0 行；未作语义复核。
- M `holy_site_types/_holy_site_types.info`；+45/-4 行；未作语义复核。
- M `religion_family_types/00_religion_family_types.txt`；+17/-5 行；未作语义复核。
- M `religion_family_types/_religion_family_types.info`；+7/-2 行；未作语义复核。
- M `religion_types/00_akom.txt`；+101/-30 行；未作语义复核。
- M `religion_types/00_aluk.txt`；+102/-26 行；未作语义复核。
- M `religion_types/00_baltic.txt`；+102/-29 行；未作语义复核。
- M `religion_types/00_basque_paganism.txt`；+102/-25 行；未作语义复核。
- M `religion_types/00_bilikuism.txt`；+108/-83 行；未作语义复核。
- M `religion_types/00_bimoism.txt`；+103/-25 行；未作语义复核。
- M `religion_types/00_bon.txt`；+100/-46 行；未作语义复核。
- M `religion_types/00_buddhism.txt`；+100/-553 行；未作语义复核。
- M `religion_types/00_christianity.txt`；+112/-930 行；未作语义复核。
- M `religion_types/00_confucianism.txt`；+107/-68 行；未作语义复核。
- M `religion_types/00_dayawism.txt`；+102/-25 行；未作语义复核。
- M `religion_types/00_donyipoloism.txt`；+106/-80 行；未作语义复核。
- M `religion_types/00_dualism.txt`；+101/-727 行；未作语义复核。
- M `religion_types/00_finno_ugric.txt`；+102/-35 行；未作语义复核。
- M `religion_types/00_germanic.txt`；+105/-39 行；未作语义复核。
- M `religion_types/00_hantuism.txt`；+105/-27 行；未作语义复核。
- M `religion_types/00_hellenism.txt`；+104/-25 行；未作语义复核。
- M `religion_types/00_hinduism.txt`；+99/-435 行；未作语义复核。
- M `religion_types/00_hmongism.txt`；+105/-27 行；未作语义复核。
- M `religion_types/00_islam.txt`；+109/-738 行；未作语义复核。
- M `religion_types/00_jainism.txt`；+103/-84 行；未作语义复核。
- M `religion_types/00_judaism.txt`；+103/-244 行；未作语义复核。
- M `religion_types/00_kaharingan.txt`；+105/-32 行；未作语义复核。
- M `religion_types/00_kamuyism.txt`；+105/-36 行；未作语义复核。
- M `religion_types/00_kushitism.txt`；+104/-32 行；未作语义复核。
- M `religion_types/00_magyarism.txt`；+102/-25 行；未作语义复核。
- M `religion_types/00_moism.txt`；+102/-25 行；未作语义复核。
- M `religion_types/00_muism.txt`；+99/-26 行；未作语义复核。
- M `religion_types/00_mundhumism.txt`；+106/-91 行；未作语义复核。
- M `religion_types/00_north_african.txt`；+105/-29 行；未作语义复核。
- M `religion_types/00_paganism.txt`；+105/-27 行；未作语义复核。
- M `religion_types/00_qiangic.txt`；+106/-178 行；未作语义复核。
- M `religion_types/00_satsana_phi.txt`；+102/-25 行；未作语义复核。
- M `religion_types/00_shamanism.txt`；+105/-33 行；未作语义复核。
- M `religion_types/00_shintoism.txt`；+99/-57 行；未作语义复核。
- M `religion_types/00_siberian.txt`；+106/-30 行；未作语义复核。
- M `religion_types/00_slavic.txt`；+102/-30 行；未作语义复核。
- M `religion_types/00_taoism.txt`；+100/-71 行；未作语义复核。
- M `religion_types/00_tengrism.txt`；+102/-29 行；未作语义复核。
- M `religion_types/00_tolotang.txt`；+107/-29 行；未作语义复核。
- M `religion_types/00_utaki.txt`；+102/-22 行；未作语义复核。
- M `religion_types/00_waaqism.txt`；+105/-208 行；未作语义复核。
- M `religion_types/00_west_african.txt`；+105/-147 行；未作语义复核。
- M `religion_types/00_west_african_bori.txt`；+105/-32 行；未作语义复核。
- M `religion_types/00_west_african_orisha.txt`；+105/-27 行；未作语义复核。
- M `religion_types/00_west_african_roog.txt`；+105/-32 行；未作语义复核。
- M `religion_types/00_yazidi.txt`；+103/-67 行；未作语义复核。
- M `religion_types/00_zoroastrianism.txt`；+103/-262 行；未作语义复核。
- M `religion_types/00_zunism.txt`；+103/-29 行；未作语义复核。
- M `religion_types/_religion_types.info`；+24/-48 行；未作语义复核。
- A `rite_icons/00_rite_icons.txt`；+993/-0 行；未作语义复核。
- A `rite_icons/_rite_icons.info`；+25/-0 行；未作语义复核。
- A `rite_names/00_rite_names.txt`；+519/-0 行；未作语义复核。
- A `rite_names/_rite_names.info`；+31/-0 行；未作语义复核。
- A `rite_types/00_rite_types.txt`；+2012/-0 行；已复核关键定义/差异。
- A `rite_types/01_christian_heresy_rite_types.txt`；+255/-0 行；未作语义复核。
- A `rite_types/02_mainline_rite_types.txt`；+1236/-0 行；未作语义复核。
- A `rite_types/_rite_types.info`；+82/-0 行；已复核关键定义/差异。
- A `tenet_types/00_pam_tenets.txt`；+2494/-0 行；已复核关键定义/差异。
- A `tenet_types/00_tenet_types.txt`；+5958/-0 行；已复核关键定义/差异。
- A `tenet_types/_tenet_types.info`；+160/-0 行；已复核关键定义/差异。

#### game/common/schemes/（46 个变化路径）

- M `agent_types/agent_types.txt`；+62/-119 行；未作语义复核。
- M `scheme_countermeasures/00_basic_countermeasures.txt`；+30/-30 行；未作语义复核。
- M `scheme_types/_schemes.info`；+4/-0 行；未作语义复核。
- M `scheme_types/abduct_scheme.txt`；+3/-42 行；未作语义复核。
- M `scheme_types/befriend_scheme.txt`；+14/-23 行；未作语义复核。
- M `scheme_types/challenge_status_scheme.txt`；+17/-44 行；未作语义复核。
- M `scheme_types/claim_throne_scheme.txt`；+11/-41 行；未作语义复核。
- M `scheme_types/coerce_contribution_scheme.txt`；+4/-17 行；未作语义复核。
- M `scheme_types/coerce_tributary_scheme.txt`；+2/-6 行；未作语义复核。
- M `scheme_types/convert_to_witchcraft_scheme.txt`；+16/-18 行；未作语义复核。
- M `scheme_types/court_scheme.txt`；+100/-31 行；未作语义复核。
- M `scheme_types/damage_legitimacy_scheme.txt`；+4/-26 行；未作语义复核。
- M `scheme_types/depose_scheme.txt`；+12/-45 行；未作语义复核。
- M `scheme_types/diarch_schemes.txt`；+2/-5 行；未作语义复核。
- M `scheme_types/disbelieve_mandala_scheme.txt`；+1/-1 行；未作语义复核。
- M `scheme_types/elope_scheme.txt`；+1/-4 行；未作语义复核。
- M `scheme_types/ep3_dispute_border_scheme.txt`；+24/-97 行；未作语义复核。
- M `scheme_types/ep3_found_despotate_scheme.txt`；+14/-52 行；未作语义复核。
- M `scheme_types/ep3_ingratiate_family_scheme.txt`；+11/-7 行；未作语义复核。
- M `scheme_types/ep3_prepare_fire_dromons_scheme.txt`；+6/-24 行；未作语义复核。
- M `scheme_types/ep3_raid_estate_scheme.txt`；+9/-102 行；未作语义复核。
- M `scheme_types/ep3_subsume_province_scheme.txt`；+23/-99 行；未作语义复核。
- M `scheme_types/ep3_teach_governor_scheme.txt`；+2/-2 行；未作语义复核。
- M `scheme_types/expand_power_base_scheme.txt`；+7/-26 行；未作语义复核。
- M `scheme_types/fabricate_hook_scheme.txt`；+50/-21 行；未作语义复核。
- A `scheme_types/find_follower_of_faith.txt`；+169/-0 行；未作语义复核。
- M `scheme_types/foster_legitimacy_scheme.txt`；+3/-10 行；未作语义复核。
- M `scheme_types/generate_claim_scheme.txt`；+11/-25 行；未作语义复核。
- M `scheme_types/laamp_base_contract_schemes.txt`；+18/-0 行；未作语义复核。
- M `scheme_types/laamp_extra_contract_schemes.txt`；+25/-21 行；未作语义复核。
- M `scheme_types/learn_language_scheme.txt`；+10/-0 行；未作语义复核。
- M `scheme_types/leverage_contribution_scheme.txt`；+4/-15 行；未作语义复核。
- M `scheme_types/murder_scheme.txt`；+14/-48 行；未作语义复核。
- A `scheme_types/pam_study_scheme.txt`；+407/-0 行；已复核关键定义/差异。
- M `scheme_types/promote_scheme.txt`；+10/-35 行；未作语义复核。
- M `scheme_types/seduce_scheme.txt`；+111/-23 行；未作语义复核。
- M `scheme_types/seize_realm_scheme.txt`；+3/-27 行；未作语义复核。
- M `scheme_types/slander_scheme.txt`；+12/-31 行；未作语义复核。
- M `scheme_types/steal_back_artifact_scheme.txt`；+1/-1 行；未作语义复核。
- M `scheme_types/steal_herd_scheme.txt`；+2/-5 行；未作语义复核。
- A `scheme_types/study_faith_scheme.txt`；+525/-0 行；已复核关键定义/差异。
- M `scheme_types/sway_scheme.txt`；+26/-23 行；未作语义复核。
- M `scheme_types/tgp_coup_ceremonial_liege.txt`；+4/-28 行；未作语义复核。
- M `scheme_types/tgp_dynastic_cycle_schemes.txt`；+40/-151 行；未作语义复核。
- M `scheme_types/tgp_mentoring_scheme.txt`；+20/-20 行；未作语义复核。
- M `scheme_types/tgp_study_scheme.txt`；+8/-3 行；未作语义复核。

#### game/common/script_values/（73 个变化路径）

- M `00_activity_values.txt`；+162/-42 行；未作语义复核。
- M `00_ai_values.txt`；+141/-151 行；未作语义复核。
- M `00_artifact_values.txt`；+29/-1 行；未作语义复核。
- M `00_basic_values.txt`；+116/-0 行；未作语义复核。
- M `00_bastardy_values.txt`；+8/-1 行；未作语义复核。
- M `00_combat_values.txt`；+1/-0 行；未作语义复核。
- M `00_council_values.txt`；+2/-2 行；未作语义复核。
- M `00_court_amenities_values.txt`；+79/-167 行；未作语义复核。
- M `00_court_position_values.txt`；+270/-91 行；未作语义复核。
- M `00_culture_values.txt`；+46/-14 行；未作语义复核。
- M `00_decision_values.txt`；+35/-1 行；未作语义复核。
- M `00_diarchy_values.txt`；+187/-239 行；未作语义复核。
- M `00_difficulty_values.txt`；+18/-10 行；未作语义复核。
- M `00_dlc_fp3_script_values.txt`；+12/-8 行；未作语义复核。
- M `00_ep1_artifact_values.txt`；+4/-0 行；未作语义复核。
- M `00_ep1_script_values.txt`；+32/-5 行；未作语义复核。
- M `00_faction_values.txt`；+2/-2 行；未作语义复核。
- M `00_goverment_values.txt`；+10/-15 行；未作语义复核。
- M `00_hold_court_values.txt`；+1/-1 行；未作语义复核。
- M `00_holy_order_values.txt`；+194/-18 行；未作语义复核。
- A `00_holy_site_values.txt`；+28/-0 行；已复核关键定义/差异。
- M `00_interaction_values.txt`；+336/-115 行；未作语义复核。
- M `00_law_values.txt`；+56/-141 行；未作语义复核。
- M `00_legitimacy_values.txt`；+50/-8 行；未作语义复核。
- M `00_lifestyle_values.txt`；+36/-0 行；未作语义复核。
- M `00_men_at_arms_values.txt`；+10/-0 行；未作语义复核。
- M `00_mongol_values.txt`；+10/-10 行；未作语义复核。
- M `00_scheme_values.txt`；+100/-212 行；未作语义复核。
- M `00_stress_values.txt`；+3/-3 行；未作语义复核。
- M `00_title_tiers_values.txt`；+107/-83 行；未作语义复核。
- M `00_unity_values.txt`；+2/-2 行；未作语义复核。
- M `00_war_values.txt`；+44/-0 行；已复核关键定义/差异。
- M `01_dlc_fp1_script_values.txt`；+11/-35 行；未作语义复核。
- M `01_dynamic_values.txt`；+228/-98 行；未作语义复核。
- M `01_starting_values.txt`；+9/-9 行；未作语义复核。
- M `02_religion_values.txt`；+631/-378 行；未作语义复核。
- M `02_vassal_values.txt`；+20/-50 行；未作语义复核。
- M `03_dlc_fp2_script_values.txt`；+53/-16 行；未作语义复核。
- M `04_ep2_accolade_values.txt`；+161/-3 行；未作语义复核。
- M `04_ep2_hunt_values.txt`；+9/-4 行；未作语义复核。
- M `04_ep2_wedding_values.txt`；+26/-18 行；未作语义复核。
- M `06_ce1_legends_values.txt`；+6/-0 行；未作语义复核。
- A `07_appointment_values.txt`；+1702/-0 行；已复核关键定义/差异。
- M `07_ep3_values.txt`；+95/-462 行；未作语义复核。
- M `09_mpo_values.txt`；+192/-165 行；未作语义复核。
- M `10_ach_values.txt`；+14/-8 行；未作语义复核。
- M `10_health_values.txt`；+8/-0 行；未作语义复核。
- M `10_tgp_dynastic_cycle_values.txt`；+27/-62 行；未作语义复核。
- M `10_tgp_japan_values.txt`；+3/-3 行；未作语义复核。
- A `11_petition_head_of_faith_values.txt`；+61/-0 行；未作语义复核。
- M `50_major_decision_values.txt`；+1/-1 行；未作语义复核。
- M `50_pilgrimage_values.txt`；+198/-0 行；未作语义复核。
- M `50_tribal_values.txt`；+67/-3 行；未作语义复核。
- M `99_casus_belli_values.txt`；+88/-28 行；未作语义复核。
- M `99_chancellor_values.txt`；+19/-8 行；未作语义复核。
- M `99_court_chaplain_values.txt`；+760/-149 行；未作语义复核。
- M `99_spouse_councillor_values.txt`；+70/-0 行；未作语义复核。
- M `99_spymaster_values.txt`；+11/-0 行；未作语义复核。
- M `99_steward_values.txt`；+37/-3 行；未作语义复核。
- M `court_events_values.txt`；+1/-1 行；未作语义复核。
- M `destiny_score_interest_value.txt`；+26/-6 行；未作语义复核。
- A `pam_heresy_values.txt`；+155/-0 行；未作语义复核。
- A `pam_saint_values.txt`；+216/-0 行；未作语义复核。
- A `pam_tenet_values.txt`；+316/-0 行；未作语义复核。
- A `pam_values.txt`；+10367/-0 行；已复核关键定义/差异。
- A `passive_rite_learning_values.txt`；+43/-0 行；未作语义复核。
- A `situation_values.txt`；+73/-0 行；未作语义复核。
- M `tgp_imperial_examination_values.txt`；+12/-12 行；未作语义复核。
- M `tgp_japan_values.txt`；+18/-47 行；未作语义复核。
- M `tgp_mandala_values.txt`；+15/-3 行；未作语义复核。
- M `tgp_natural_disaster_values.txt`；+18/-0 行；未作语义复核。
- M `tgp_tribute_mission_values.txt`；+19/-18 行；未作语义复核。
- M `tgp_values.txt`；+12/-0 行；未作语义复核。

#### game/common/scripted_animations/（2 个变化路径）

- M `00_scripted_animations.txt`；+161/-1 行；未作语义复核。
- A `pam_scripted_animations.txt`；+161/-0 行；未作语义复核。

#### game/common/scripted_character_templates/（39 个变化路径）

- M `00_court_character_templates.txt`；+6/-1 行；未作语义复核。
- M `00_court_position_templates.txt`；+4/-4 行；未作语义复核。
- M `00_foundling_templates.txt`；+1/-0 行；未作语义复核。
- M `00_hold_court_character_templates.txt`；+11/-1 行；未作语义复核。
- M `00_holy_order_character_templates.txt`；+174/-29 行；未作语义复核。
- M `00_invader_templates.txt`；+7/-5 行；未作语义复核。
- M `00_knight_templates.txt`；+3/-0 行；未作语义复核。
- M `00_lifestyle_friend_templates.txt`；+16/-1 行；未作语义复核。
- M `00_mongol_templates.txt`；+2/-2 行；未作语义复核。
- M `00_mystic_templates.txt`；+83/-42 行；未作语义复核。
- M `00_officials_templates.txt`；+6/-3 行；未作语义复核。
- M `00_peasant_leader_templates.txt`；+6/-4 行；未作语义复核。
- M `00_peasants_template.txt`；+77/-1 行；未作语义复核。
- M `00_physician_character_template.txt`；+3/-0 行；未作语义复核。
- M `00_pool_repopulation_character_templates.txt`；+73/-35 行；未作语义复核。
- M `00_priest_character_template.txt`；+373/-289 行；未作语义复核。
- M `00_scholar_template.txt`；+6/-2 行；未作语义复核。
- M `00_soldier_character_templates.txt`；+1/-0 行；未作语义复核。
- M `00_terrain_specialist_templates.txt`；+1/-0 行；未作语义复核。
- M `01_bp1_character_templates.txt`；+2/-0 行；未作语义复核。
- M `01_bp1_filippa_character_templates.txt`；+10/-4 行；未作语义复核。
- M `01_bp2_character_templates.txt`；+1/-0 行；未作语义复核。
- M `01_ep1_character_templates.txt`；+78/-30 行；未作语义复核。
- M `01_fp1_character_templates.txt`；+93/-40 行；未作语义复核。
- M `01_tgp_japan_character_templates.txt`；+5/-3 行；未作语义复核。
- M `03_fp2_character_templates.txt`；+67/-30 行；未作语义复核。
- M `04_ep2_accolade_character_templates.txt`；+46/-226 行；未作语义复核。
- M `04_ep2_character_templates.txt`；+15/-6 行；未作语义复核。
- M `04_ep2_character_templates_james.txt`；+1/-0 行；未作语义复核。
- M `04_fp3_character_templates.txt`；+13/-8 行；未作语义复核。
- M `05_bp2_character_templates.txt`；+12/-5 行；未作语义复核。
- M `05_ce1_character_templates.txt`；+1/-0 行；未作语义复核。
- M `06_ce1_character_templates.txt`；+1/-0 行；未作语义复核。
- M `07_ep3_character_templates.txt`；+22/-11 行；未作语义复核。
- M `09_mpo_character_templates.txt`；+14/-4 行；未作语义复核。
- M `10_ach_character_templates.txt`；+4/-0 行；未作语义复核。
- A `pam_character_templates.txt`；+252/-0 行；未作语义复核。
- A `pam_secular_faith_character_templates.txt`；+47/-0 行；未作语义复核。
- M `tgp_character_templates.txt`；+91/-75 行；未作语义复核。

#### game/common/scripted_costs/（1 个变化路径）

- M `00_costs.txt`；+86/-48 行；未作语义复核。

#### game/common/scripted_effects/（139 个变化路径）

- M `00_accolades_scripted_effects.txt`；+5083/-383 行；未作语义复核。
- M `00_achievement_effects.txt`；+36/-0 行；未作语义复核。
- M `00_activity_effects.txt`；+229/-26 行；未作语义复核。
- M `00_administrative_effects.txt`；+13/-33 行；未作语义复核。
- M `00_adultery_effects.txt`；+5/-5 行；未作语义复核。
- M `00_ai_budget_effects.txt`；+7/-1 行；未作语义复核。
- M `00_ai_conqueror_effects.txt`；+24/-433 行；未作语义复核。
- M `00_ai_value_effects.txt`；+2/-2 行；未作语义复核。
- M `00_almohad_invasion_effects.txt`；+1/-1 行；未作语义复核。
- M `00_animal_effects.txt`；+26/-8 行；未作语义复核。
- M `00_antiquarian_artifact_improvement_effects.txt`；+8/-9 行；未作语义复核。
- A `00_artifact_badge_scripted_effects.txt`；+400/-0 行；未作语义复核。
- M `00_bastard_effects.txt`；+17/-14 行；未作语义复核。
- M `00_building_effects.txt`；+315/-306 行；未作语义复核。
- M `00_childhood_effects.txt`；+1/-1 行；未作语义复核。
- M `00_commander_effects.txt`；+1/-0 行；未作语义复核。
- M `00_councillor_effects.txt`；+183/-78 行；未作语义复核。
- M `00_court_position_effects.txt`；+148/-12 行；未作语义复核。
- M `00_courtier_guest_management_effects.txt`；+6/-15 行；未作语义复核。
- M `00_culture_effects.txt`；+48/-374 行；未作语义复核。
- M `00_death_management_effects.txt`；+30/-17 行；未作语义复核。
- M `00_decisions_effects.txt`；+312/-428 行；未作语义复核。
- M `00_diarchy_scripted_effects.txt`；+59/-46 行；未作语义复核。
- M `00_diplomacy_lifestyle_effects.txt`；+2/-9 行；未作语义复核。
- M `00_dummy_gender_effects.txt`；+18/-18 行；未作语义复核。
- M `00_education_effects.txt`；+84/-22 行；未作语义复核。
- A `00_empire_faith_gate_effects.txt`；+80/-0 行；已复核关键定义/差异。
- M `00_ep1_artifact_creation_effects.txt`；+85/-45 行；未作语义复核。
- M `00_ep1_artifact_effects.txt`；+11/-5 行；未作语义复核。
- M `00_ep1_court_type_effects.txt`；+71/-0 行；未作语义复核。
- M `00_ep1_inspiration_effects.txt`；+16/-27 行；未作语义复核。
- M `00_ep1_inspiration_effects_sean.txt`；+39/-12 行；未作语义复核。
- M `00_ep3_decision_effects.txt`；+2/-2 行；未作语义复核。
- M `00_faction_effects.txt`；+170/-246 行；未作语义复核。
- M `00_feast_scripted_effects.txt`；+45/-7 行；未作语义复核。
- M `00_funeral_scripted_effects.txt`；+6/-0 行；未作语义复核。
- M `00_game_rule_effects.txt`；+130/-27 行；未作语义复核。
- A `00_government_effects.txt`；+165/-0 行；未作语义复核。
- M `00_historical_characters_scripted_effects.txt`；+3016/-164 行；未作语义复核。
- M `00_history_effects.txt`；+24/-0 行；未作语义复核。
- A `00_holding_effects.txt`；+85/-0 行；未作语义复核。
- M `00_holy_order_effects.txt`；+6531/-18 行；未作语义复核。
- M `00_hunt_effects.txt`；+111/-57 行；未作语义复核。
- M `00_interaction_effects.txt`；+1591/-774 行；未作语义复核。
- M `00_intrigue_perk_effects.txt`；+3/-3 行；未作语义复核。
- M `00_journey_effects.txt`；+1/-0 行；未作语义复核。
- M `00_laamp_effects.txt`；+23/-13 行；未作语义复核。
- M `00_learning_lifestyle_effects.txt`；+37/-43 行；未作语义复核。
- M `00_lifestyle_focus_effects.txt`；+5/-4 行；未作语义复核。
- M `00_major_decisions_scripted_effects.txt`；+502/-100 行；未作语义复核。
- M `00_major_decisions_scripted_effects_2.txt`；+24/-134 行；未作语义复核。
- M `00_major_decisions_scripted_effects_3.txt`；+334/-105 行；未作语义复核。
- M `00_marriage_interaction_effects.txt`；+174/-145 行；未作语义复核。
- M `00_martial_lifestyle_effects.txt`；+60/-0 行；未作语义复核。
- M `00_mongol_invasion_effects.txt`；+348/-322 行；未作语义复核。
- M `00_murder_effects.txt`；+9/-9 行；未作语义复核。
- M `00_nickname_effects.txt`；+110/-22 行；未作语义复核。
- M `00_personal_details_effects.txt`；+3/-9 行；未作语义复核。
- M `00_personality_trait_effects.txt`；+35/-35 行；未作语义复核。
- M `00_petition_liege_effects.txt`；+26/-23 行；未作语义复核。
- M `00_pilgrimage_effects.txt`；+286/-80 行；未作语义复核。
- M `00_playdate_scripted_effects.txt`；+1/-1 行；未作语义复核。
- M `00_poetry_effects.txt`；+70/-0 行；未作语义复核。
- M `00_pool_effects.txt`；+5/-0 行；未作语义复核。
- M `00_pregnancy_effects.txt`；+13/-9 行；未作语义复核。
- M `00_prison_effects.txt`；+613/-108 行；未作语义复核。
- M `00_realm_effects.txt`；+48/-149 行；未作语义复核。
- M `00_regional_scripted_effects.txt`；+5/-7 行；未作语义复核。
- M `00_relation_effects.txt`；+87/-86 行；未作语义复核。
- M `00_religion_effects.txt`；+968/-223 行；未作语义复核。
- M `00_religious_interaction_effects.txt`；+748/-111 行；未作语义复核。
- M `00_roaming_effects.txt`；+3/-3 行；未作语义复核。
- M `00_romance_effects.txt`；+17/-8 行；未作语义复核。
- M `00_scheme_scripted_effects.txt`；+595/-127 行；未作语义复核。
- M `00_secret_effects.txt`；+156/-46 行；未作语义复核。
- M `00_setup_tests_effect.txt`；+22/-1 行；未作语义复核。
- M `00_single_combat_effects.txt`；+6/-6 行；未作语义复核。
- M `00_spouse_effects.txt`；+2/-2 行；未作语义复核。
- M `00_stewardship_lifestyle_effects.txt`；+3/-0 行；未作语义复核。
- M `00_stress_effects.txt`；+15/-1 行；未作语义复核。
- M `00_travel_effects.txt`；+7/-0 行；未作语义复核。
- M `00_tributary_setup_effects.txt`；+1204/-1184 行；未作语义复核。
- M `00_unity_effects.txt`；+26/-26 行；未作语义复核。
- M `00_wanderer_lifestyle_effects.txt`；+50/-3 行；未作语义复核。
- M `00_war_effects.txt`；+187/-45 行；未作语义复核。
- M `00_witch_effects.txt`；+1/-0 行；未作语义复核。
- M `01_dlc_bp1_filippa_scripted_effects.txt`；+14/-14 行；未作语义复核。
- M `01_dlc_fp1_scripted_effects.txt`；+53/-5 行；未作语义复核。
- M `01_dlc_fp3_scripted_effects.txt`；+25/-21 行；未作语义复核。
- M `01_ep1_court_artifact_creation_effects.txt`；+333/-223 行；未作语义复核。
- M `01_exp1_historical_artifacts_creation_effect.txt`；+73/-68 行；未作语义复核。
- M `02_dlc_ep1_decision_scripted_effects.txt`；+1/-1 行；未作语义复核。
- A `02_starting_holy_site_relics_effects.txt`；+1601/-0 行；未作语义复核。
- M `03_bp1_scripted_effects.txt`；+7/-4 行；未作语义复核。
- M `03_dlc_fp2_scripted_effects.txt`；+98/-47 行；未作语义复核。
- M `03_dlc_fp3_artifact_creation_effects.txt`；+6/-6 行；未作语义复核。
- M `03_dlc_fp3_scripted_effects.txt`；+9/-9 行；未作语义复核。
- M `04_dlc_ep2_tour_effects.txt`；+3/-2 行；未作语义复核。
- M `04_dlc_ep2_tournament_effects.txt`；+175/-52 行；未作语义复核。
- M `04_dlc_ep2_wedding_effects.txt`；+15/-7 行；未作语义复核。
- M `05_bp2_hostage_effects.txt`；+7/-4 行；未作语义复核。
- M `05_dlc_bp2_effects.txt`；+149/-77 行；未作语义复核。
- M `05_dlc_fp3_scripted_effects.txt`；+35/-29 行；未作语义复核。
- M `06_dlc_ce1_epidemics_effects.txt`；+13/-2 行；未作语义复核。
- M `06_dlc_ce1_legend_effects.txt`；+19/-15 行；未作语义复核。
- M `06_dlc_ce1_legitimacy_effects.txt`；+7/-46 行；未作语义复核。
- M `07_dlc_ep3_scripted_effects.txt`；+708/-726 行；未作语义复核。
- M `07_frankokratia_scripted_effects.txt`；+68/-91 行；未作语义复核。
- M `08_bp3_effects.txt`；+123/-227 行；未作语义复核。
- M `09_dlc_mpo_scripted_effects.txt`；+208/-168 行；未作语义复核。
- M `09_mpo_greatest_of_khans_effects.txt`；+196/-225 行；未作语义复核。
- M `10_ach_effects.txt`；+303/-243 行；未作语义复核。
- M `10_dlc_tgp_dynastic_cycle_scripted_effects.txt`；+18/-9 行；未作语义复核。
- A `10_dlc_tgp_history_effects.txt`；+243/-0 行；未作语义复核。
- M `10_dlc_tgp_house_bloc_scripted_effects.txt`；+41/-8 行；未作语义复核。
- M `10_dlc_tgp_house_relation_scripted_effects.txt`；+1/-1 行；未作语义复核。
- M `10_dlc_tgp_japan_scripted_effects.txt`；+177/-240 行；未作语义复核。
- M `10_dlc_tgp_korea_scripted_effects.txt`；+13/-14 行；未作语义复核。
- M `10_dlc_tgp_natural_disaster_scripted_effects.txt`；+128/-23 行；未作语义复核。
- M `10_dlc_tgp_scripted_effects.txt`；+70/-82 行；未作语义复核。
- M `10_dlc_tgp_silk_road_scripted_effects.txt`；+0/-17 行；未作语义复核。
- A `11_dlc_pam_scripted_effects.txt`；+1592/-0 行；未作语义复核。
- A `11_petition_head_of_faith_effects.txt`；+934/-0 行；未作语义复核。
- M `20_health_effects.txt`；+169/-51 行；未作语义复核。
- A `pam_antipope_effects.txt`；+927/-0 行；未作语义复核。
- A `pam_ecumenical_council_effects.txt`；+1223/-0 行；未作语义复核。
- A `pam_effects.txt`；+14558/-0 行；未作语义复核。
- A `pam_heresy_historical_founder_effects.txt`；+697/-0 行；未作语义复核。
- A `pam_heresy_shared_effects.txt`；+729/-0 行；未作语义复核。
- A `pam_investiture_council_effects.txt`；+783/-0 行；未作语义复核。
- A `pam_saint_effects.txt`；+846/-0 行；未作语义复核。
- A `pam_secular_faith_effects.txt`；+149/-0 行；未作语义复核。
- A `passive_rite_learning_effects.txt`；+1575/-0 行；未作语义复核。
- A `sanctify_artifact_effects.txt`；+42/-0 行；未作语义复核。
- M `tgp_debate_scripted_effects.txt`；+6/-4 行；未作语义复核。
- M `tgp_imperial_examination_scripted_effects.txt`；+43/-31 行；未作语义复核。
- M `tgp_mandala_scripted_effects.txt`；+24/-49 行；未作语义复核。
- M `tgp_tribute_mission_scripted_effects.txt`；+19/-3 行；未作语义复核。
- A `titus_natural_primitivism_effects.txt`；+118/-0 行；未作语义复核。

#### game/common/scripted_guis/（3 个变化路径）

- A `00_empire_faith_gate_guis.txt`；+153/-0 行；未作语义复核。
- M `00_religion.txt`；+0/-31 行；未作语义复核。
- A `pam_scripted_guis.txt`；+92/-0 行；未作语义复核。

#### game/common/scripted_modifiers/（19 个变化路径）

- M `00_activity_scripted_modifiers.txt`；+117/-17 行；未作语义复核。
- M `00_ai_value_modifiers.txt`；+6/-6 行；未作语义复核。
- A `00_character_interaction_modifiers.txt`；+1511/-0 行；未作语义复核。
- M `00_elective_successions_scripted_modifiers.txt`；+965/-105 行；未作语义复核。
- M `00_faction_modifiers.txt`；+235/-185 行；未作语义复核。
- M `00_marriage_scripted_modifiers.txt`；+918/-1017 行；未作语义复核。
- M `00_religion_scripted_modifiers.txt`；+5015/-51 行；未作语义复核。
- M `00_romance_and_seduction_scripted_modifiers.txt`；+1/-1 行；未作语义复核。
- M `00_scheme_scripted_modifiers.txt`；+529/-33 行；未作语义复核。
- M `01_bp1_scripted_modifiers.txt`；+16/-0 行；未作语义复核。
- M `02_ep1_scripted_modifiers.txt`；+3/-3 行；未作语义复核。
- M `03_fp2_scripted_modifiers.txt`；+2/-4 行；未作语义复核。
- M `05_bp2_scripted_modifiers.txt`；+28/-28 行；未作语义复核。
- M `07_ep3_scripted_modifiers.txt`；+13/-22 行；未作语义复核。
- M `09_mpo_scripted_modifiers.txt`；+29/-28 行；未作语义复核。
- M `10_tgp_japan_modifiers.txt`；+40/-44 行；未作语义复核。
- M `10_tgp_scripted_modifiers.txt`；+1/-0 行；未作语义复核。
- A `pam_scripted_modifiers.txt`；+27/-0 行；未作语义复核。
- M `tgp_mandala_scripted_modifiers.txt`；+4/-4 行；未作语义复核。

#### game/common/scripted_rules/（3 个变化路径）

- M `00_rules.txt`；+164/-124 行；已复核关键定义/差异。
- A `01_grant_title_rules.txt`；+175/-0 行；未作语义复核。
- A `02_holy_sites.txt`；+64/-0 行；已复核关键定义/差异。

#### game/common/scripted_triggers/（111 个变化路径）

- M `00_activity_triggers.txt`；+37/-26 行；未作语义复核。
- M `00_adultery_triggers.txt`；+5/-5 行；未作语义复核。
- M `00_ai_value_triggers.txt`；+6/-3 行；未作语义复核。
- A `00_artifact_badge_triggers.txt`；+8/-0 行；未作语义复核。
- M `00_artifact_triggers.txt`；+111/-132 行；未作语义复核。
- M `00_auto_character_triggers.txt`；+19/-8 行；未作语义复核。
- M `00_available_for_events_triggers.txt`；+292/-215 行；未作语义复核。
- M `00_bastard_triggers.txt`；+12/-12 行；未作语义复核。
- M `00_birth_triggers.txt`；+12/-4 行；未作语义复核。
- M `00_board_game_scripted_triggers.txt`；+5/-3 行；未作语义复核。
- M `00_building_requirement_triggers.txt`；+70/-4 行；未作语义复核。
- M `00_childhood_triggers.txt`；+2/-35 行；未作语义复核。
- M `00_clan_triggers.txt`；+0/-9 行；未作语义复核。
- M `00_clothing_triggers.txt`；+447/-90 行；未作语义复核。
- M `00_coa_triggers.txt`；+197/-193 行；未作语义复核。
- M `00_commander_triggers.txt`；+0/-22 行；未作语义复核。
- M `00_councillor_triggers.txt`；+370/-40 行；未作语义复核。
- M `00_county_corruption_triggers.txt`；+0/-2 行；未作语义复核。
- M `00_court_position_triggers.txt`；+257/-80 行；未作语义复核。
- M `00_court_scheme_triggers.txt`；+2/-2 行；未作语义复核。
- M `00_courtier_guest_management_triggers.txt`；+16/-5 行；未作语义复核。
- M `00_crime_triggers.txt`；+71/-6 行；未作语义复核。
- M `00_cultural_triggers.txt`；+16/-4 行；未作语义复核。
- M `00_death_management_triggers.txt`；+2/-0 行；未作语义复核。
- M `00_diarchy_scripted_triggers.txt`；+37/-27 行；未作语义复核。
- M `00_dynasty_triggers.txt`；+53/-0 行；未作语义复核。
- M `00_economic_triggers.txt`；+2/-2 行；未作语义复核。
- M `00_elective_triggers.txt`；+38/-30 行；未作语义复核。
- A `00_empire_faith_gate_triggers.txt`；+325/-0 行；已复核关键定义/差异。
- M `00_faction_triggers.txt`；+142/-97 行；未作语义复核。
- M `00_family_triggers.txt`；+35/-20 行；未作语义复核。
- M `00_food_scripted_triggers.txt`；+0/-3 行；未作语义复核。
- M `00_funeral_and_body_disposal_triggers.txt`；+6/-0 行；未作语义复核。
- M `00_game_rule_triggers.txt`；+133/-142 行；已复核关键定义/差异。
- M `00_general_trait_triggers.txt`；+1/-1 行；未作语义复核。
- M `00_generic_event_sensibility_triggers.txt`；+132/-83 行；未作语义复核。
- M `00_government_triggers.txt`；+3/-4 行；未作语义复核。
- M `00_great_holy_war_triggers.txt`；+63/-52 行；未作语义复核。
- M `00_has_dlc_scripted_triggers.txt`；+4/-0 行；已复核关键定义/差异。
- M `00_hunt_triggers.txt`；+4/-9 行；未作语义复核。
- M `00_illustration_triggers.txt`；+18/-19 行；未作语义复核。
- M `00_important_actions_triggers.txt`；+23/-0 行；未作语义复核。
- M `00_interaction_triggers.txt`；+75/-31 行；未作语义复核。
- M `00_laamp_triggers.txt`；+19/-11 行；未作语义复核。
- M `00_law_triggers.txt`；+243/-31 行；已复核关键定义/差异。
- M `00_legal_triggers.txt`；+11/-11 行；未作语义复核。
- M `00_lifestyle_triggers.txt`；+4/-4 行；未作语义复核。
- M `00_major_decision_triggers.txt`；+21/-1 行；未作语义复核。
- M `00_marriage_triggers.txt`；+52/-58 行；未作语义复核。
- M `00_pet_triggers.txt`；+3/-3 行；未作语义复核。
- M `00_relation_triggers.txt`；+25/-8 行；未作语义复核。
- A `00_religion_faith_rite_triggers.txt`；+563/-0 行；未作语义复核。
- M `00_religious_triggers.txt`；+2281/-765 行；已复核关键定义/差异。
- M `00_roaming_activity_triggers.txt`；+12/-0 行；未作语义复核。
- M `00_romance_and_seduction_triggers.txt`；+391/-253 行；未作语义复核。
- M `00_scheme_triggers.txt`；+210/-25 行；未作语义复核。
- M `00_scripted_rule_triggers.txt`；+3/-1 行；未作语义复核。
- M `00_scripted_triggers.txt`；+42/-25 行；未作语义复核。
- M `00_secret_type_triggers.txt`；+82/-45 行；未作语义复核。
- M `00_sibling_triggers.txt`；+1/-1 行；未作语义复核。
- M `00_single_combat_scripted_triggers.txt`；+0/-1 行；未作语义复核。
- M `00_stress_triggers.txt`；+50/-10 行；未作语义复核。
- M `00_succession_triggers.txt`；+4/-4 行；未作语义复核。
- M `00_title_triggers.txt`；+4/-3 行；未作语义复核。
- M `00_travel_triggers.txt`；+3/-2 行；未作语义复核。
- M `00_vassal_stance_triggers.txt`；+5/-9 行；未作语义复核。
- M `00_war_and_peace_triggers.txt`；+291/-48 行；未作语义复核。
- M `00_weather_triggers.txt`；+18/-4 行；未作语义复核。
- M `00_witch_triggers.txt`；+2/-2 行；未作语义复核。
- M `01_fp1_scripted_triggers.txt`；+9/-9 行；未作语义复核。
- M `02_ep1_scripted_triggers.txt`；+2/-1 行；未作语义复核。
- M `03_bp1_scripted_triggers.txt`；+5/-5 行；未作语义复核。
- M `03_bp2_scripted_triggers.txt`；+2/-2 行；未作语义复核。
- M `03_fp2_scripted_triggers.txt`；+20/-20 行；未作语义复核。
- M `04_ep2_accolade_triggers.txt`；+116/-2 行；未作语义复核。
- M `04_ep2_tour_triggers.txt`；+1/-2 行；未作语义复核。
- M `04_ep2_tournament_triggers.txt`；+15/-11 行；未作语义复核。
- M `04_ep2_wedding_triggers.txt`；+5/-3 行；未作语义复核。
- M `05_bp2_hostage_triggers.txt`；+9/-3 行；未作语义复核。
- M `05_bp2_triggers.txt`；+8/-3 行；未作语义复核。
- M `06_bp3_triggers.txt`；+16/-16 行；未作语义复核。
- M `06_ce1_epidemic_triggers.txt`；+1/-3 行；未作语义复核。
- M `06_ce1_legend_triggers.txt`；+20/-0 行；未作语义复核。
- M `06_ce1_legitimacy_triggers.txt`；+1/-1 行；未作语义复核。
- M `06_fp3_scripted_triggers.txt`；+4/-4 行；未作语义复核。
- M `07_ep3_petition_triggers.txt`；+3/-3 行；未作语义复核。
- M `07_ep3_triggers.txt`；+81/-19 行；未作语义复核。
- M `07_frankokratia_triggers.txt`；+25/-18 行；未作语义复核。
- M `09_mpo_greatest_of_khans_triggers.txt`；+7/-27 行；未作语义复核。
- M `10_ach_scripted_triggers.txt`；+125/-8 行；未作语义复核。
- M `10_tgp_dynastic_cycle_triggers.txt`；+1/-1 行；未作语义复核。
- M `10_tgp_house_relation_triggers.txt`；+2/-2 行；未作语义复核。
- M `10_tgp_japan_triggers.txt`；+31/-28 行；未作语义复核。
- M `10_tgp_natural_disaster_triggers.txt`；+5/-1 行；已复核关键定义/差异。
- M `10_tgp_triggers.txt`；+74/-24 行；已复核关键定义/差异。
- A `11_petition_head_of_faith_triggers.txt`；+377/-0 行；未作语义复核。
- M `20_health_triggers.txt`；+43/-39 行；未作语义复核。
- A `clerical_chastity_triggers.txt`；+65/-0 行；未作语义复核。
- M `mpo_scripted_triggers.txt`；+94/-85 行；未作语义复核。
- M `music_triggers.txt`；+6/-3 行；未作语义复核。
- A `pam_antipope_triggers.txt`；+278/-0 行；未作语义复核。
- A `pam_heresy_triggers.txt`；+378/-0 行；未作语义复核。
- A `pam_saint_triggers.txt`；+230/-0 行；未作语义复核。
- A `pam_scripted_triggers.txt`；+6937/-0 行；已复核关键定义/差异。
- A `pam_secular_faith_triggers.txt`；+60/-0 行；未作语义复核。
- A `pam_spread_tenet_triggers.txt`；+72/-0 行；未作语义复核。
- A `passive_rite_learning_triggers.txt`；+317/-0 行；未作语义复核。
- A `sanctify_artifact_triggers.txt`；+225/-0 行；未作语义复核。
- M `tgp_imperial_examination_triggers.txt`；+2/-2 行；未作语义复核。
- M `tgp_silk_road_triggers.txt`；+4/-1 行；已复核关键定义/差异。
- M `tgp_tribute_mission_triggers.txt`；+9/-9 行；未作语义复核。

#### game/common/secret_types/（3 个变化路径）

- M `00_bastard_secrets.txt`；+18/-5 行；未作语义复核。
- M `00_secret_types.txt`；+48/-2 行；未作语义复核。
- M `dynastic_cycle_secrets.txt`；+28/-12 行；未作语义复核。

#### game/common/situation/（7 个变化路径）

- M `catalysts/10_tgp_dynastic_cycle_catalysts.txt`；+1/-1 行；未作语义复核。
- A `catalysts/pam_the_christian_church_catalysts.txt`；+166/-0 行；未作语义复核。
- M `situations/_situations.info`；+16/-4 行；未作语义复核。
- M `situations/debug_situation.txt`；+5/-5 行；未作语义复核。
- A `situations/pam_christian_situation.txt`；+1992/-0 行；已复核关键定义/差异。
- M `situations/tgp_dynastic_cycle.txt`；+8/-4 行；未作语义复核。
- M `situations/tgp_silk_road.txt`；+3/-3 行；未作语义复核。

#### game/common/spiritual_fulfillment/（2 个变化路径）

- A `00_spiritual_fulfillment_types.txt`；+178/-0 行；已复核关键定义/差异。
- A `_spiritual_fulfillment_type.info`；+42/-0 行；未作语义复核。

#### game/common/story_cycles/（16 个变化路径）

- M `bp2_story_cycle_pet_rock.txt`；+1/-4 行；未作语义复核。
- M `ce1_story_cycle_black_death.txt`；+9/-9 行；未作语义复核。
- M `ep3_story_cycle_adventurer_ai_contract.txt`；+10/-6 行；未作语义复核。
- M `ep3_story_cycle_el_cid.txt`；+1/-1 行；未作语义复核。
- M `ep3_story_cycle_hasan_sabbah.txt`；+10/-23 行；未作语义复核。
- M `ep3_story_cycle_violet_poet.txt`；+1/-1 行；未作语义复核。
- A `pam_story_cycle_slavic_rite.txt`；+342/-0 行；未作语义复核。
- M `story_cycle_murders_at_court.txt`；+6/-6 行；未作语义复核。
- M `story_cycle_peasant_affair.txt`；+4/-3 行；未作语义复核。
- M `story_cycle_pet_cat.txt`；+2/-4 行；未作语义复核。
- M `story_cycle_pet_dog.txt`；+15/-31 行；未作语义复核。
- M `story_cycle_take_mandate_of_heaven.txt`；+2/-0 行；未作语义复核。
- M `story_cycle_tax_rivalry.txt`；+2/-2 行；未作语义复核。
- M `story_cycle_warfare_lifestyle_warhorse.txt`；+1/-4 行；未作语义复核。
- M `tgp_story_cycle_mandala.txt`；+1/-1 行；未作语义复核。
- M `tgp_story_cycle_tai_migrations.txt`；+1/-1 行；未作语义复核。

#### game/common/struggle/（3 个变化路径）

- M `struggles/_struggles.info`；+2/-2 行；未作语义复核。
- M `struggles/iberian_struggle_script.txt`；+3/-3 行；未作语义复核。
- M `struggles/persian_struggle_script.txt`；+5/-10 行；未作语义复核。

#### game/common/subject_contracts/（7 个变化路径）

- M `contracts/administrative.txt`；+7/-1 行；已复核关键定义/差异。
- M `contracts/celestial.txt`；+7/-2 行；已复核关键定义/差异。
- M `contracts/clan.txt`；+20/-20 行；未作语义复核。
- M `contracts/japan_administrative.txt`；+3/-0 行；已复核关键定义/差异。
- M `contracts/meritocratic.txt`；+20/-17 行；未作语义复核。
- M `contracts/special_contracts.txt`；+56/-38 行；未作语义复核。
- M `groups/subject_contract_groups.txt`；+5/-1 行；未作语义复核。

#### game/common/succession_appointment/（10 个变化路径）

- M `_succession_appointment.info`；+48/-4 行；已复核关键定义/差异。
- M `admin_emperor.txt`；+19/-357 行；已复核关键定义/差异。
- M `admin_governor.txt`；+5/-468 行；未作语义复核。
- M `celestial_governor.txt`；+15/-1341 行；未作语义复核。
- M `celestial_minister.txt`；+6/-191 行；未作语义复核。
- A `clerical_christian.txt`；+786/-0 行；已复核关键定义/差异。
- M `japanese_admin_governor.txt`；+13/-937 行；未作语义复核。
- M `japanese_admin_regent.txt`；+8/-545 行；未作语义复核。
- M `meritocratic_governor.txt`；+53/-1204 行；未作语义复核。
- M `meritocratic_regent.txt`；+9/-566 行；未作语义复核。

#### game/common/succession_election/（9 个变化路径）

- M `00_feudal_elective.txt`；+57/-47 行；未作语义复核。
- A `00_pam_clerical_elective.txt`；+88/-0 行；未作语义复核。
- M `01_princely_elective.txt`；+52/-46 行；未作语义复核。
- M `02_gaelic_elective.txt`；+35/-25 行；未作语义复核。
- M `04_saxon_elective.txt`；+34/-28 行；未作语义复核。
- M `05_scandinavian_elective.txt`；+32/-26 行；未作语义复核。
- M `06_tribal_elective.txt`；+39/-33 行；未作语义复核。
- M `09_confederation_elective.txt`；+54/-48 行；未作语义复核。
- M `_succession_election.info`；+58/-13 行；未作语义复核。

#### game/common/suggestions/（2 个变化路径）

- M `01_suggestions.txt`；+7/-7 行；未作语义复核。
- A `02_sanctify_artifact_suggestion.txt`；+89/-0 行；未作语义复核。

#### game/common/task_contracts/（6 个变化路径）

- M `admin_contracts.txt`；+6/-1 行；未作语义复核。
- M `laamp_base_contracts.txt`；+80/-5 行；未作语义复核。
- M `laamp_extra_contracts.txt`；+167/-136 行；未作语义复核。
- M `laamp_nm_contracts.txt`；+27/-10 行；未作语义复核。
- M `laamp_transport_contracts.txt`；+85/-24 行；未作语义复核。
- M `tgp_admin_contracts.txt`；+8/-8 行；未作语义复核。

#### game/common/tax_slots/（1 个变化路径）

- M `types/00_tax_slot_types.txt`；+4/-4 行；未作语义复核。

#### game/common/terrain_types/（1 个变化路径）

- M `_terrains.info`；+2/-2 行；未作语义复核。

#### game/common/traits/（4 个变化路径）

- M `00_traits.txt`；+2639/-996 行；已复核关键定义/差异。
- M `_traits.info`；+16/-7 行；未作语义复核。
- M `old_trait_indexes.lookup`；+1/-1 行；未作语义复核。
- M `trait_conversion.lookup`；+3/-0 行；已复核关键定义/差异。

#### game/common/travel/（4 个变化路径）

- M `point_of_interest_types/_travel_point_of_interest_types.info`；+8/-0 行；未作语义复核。
- A `point_of_interest_types/pam_saint_point_of_interest_types.txt`；+138/-0 行；未作语义复核。
- M `point_of_interest_types/travel_point_of_interest_types.txt`；+724/-158 行；未作语义复核。
- M `travel_options/travel_options.txt`；+17/-8 行；未作语义复核。

#### game/common/trigger_localization/（19 个变化路径）

- A `00_artifact_triggers.txt`；+54/-0 行；未作语义复核。
- M `00_character_relation_triggers.txt`；+35/-0 行；未作语义复核。
- M `00_character_triggers.txt`；+118/-9 行；未作语义复核。
- M `00_culture_triggers.txt`；+1/-0 行；未作语义复核。
- M `00_custom_triggers.txt`；+30/-7 行；未作语义复核。
- M `00_debug_triggers.txt`；+6/-0 行；未作语义复核。
- M `00_dlc_triggers.txt`；+9/-0 行；未作语义复核。
- M `00_doctrine_triggers.txt`；+29/-3 行；未作语义复核。
- M `00_dynasty_triggers.txt`；+3/-0 行；未作语义复核。
- M `00_faction_triggers.txt`；+4/-0 行；未作语义复核。
- M `00_government_triggers.txt`；+19/-0 行；未作语义复核。
- M `00_religion_triggers.txt`；+29/-0 行；未作语义复核。
- A `00_scope_comparison_triggers.txt`；+229/-0 行；未作语义复核。
- D `00_scope_comparison_triggers_l_english.txt`；+0/-190 行；未作语义复核。
- M `00_script_list_triggers.txt`；+18/-0 行；未作语义复核。
- M `01_character_interaction_triggers.txt`；+105/-8 行；未作语义复核。
- M `01_decision_triggers.txt`；+7/-9 行；未作语义复核。
- M `06_bp2_hostage_triggers.txt`；+0/-3 行；未作语义复核。
- A `10_ce3_achievement_triggers.txt`；+39/-0 行；未作语义复核。

#### game/common/tutorial_lessons/（1 个变化路径）

- M `00_tutorial_lessons_reactive.txt`；+1059/-9 行；未作语义复核。

#### game/common/vassal_stances/（1 个变化路径）

- M `00_vassal_stances.txt`；+5/-60 行；未作语义复核。

#### game/events/（529 个变化路径）

- M `_events.info`；+34/-0 行；未作语义复核。
- M `accolade_events.txt`；+341/-0 行；未作语义复核。
- M `activities/activity_system_events.txt`；+115/-28 行；未作语义复核。
- M `activities/chariot_race_activity/chariot_ongoing_events_jp.txt`；+45/-24 行；未作语义复核。
- M `activities/chariot_race_activity/chariot_race_events.txt`；+28/-28 行；未作语义复核。
- M `activities/chariot_race_activity/chariot_race_ongoing_events.txt`；+140/-147 行；未作语义复核。
- M `activities/coronation_activity/coronation_events.txt`；+89/-70 行；未作语义复核。
- M `activities/coronation_activity/coronation_events_02.txt`；+142/-7 行；未作语义复核。
- M `activities/coronation_activity/coronation_events_1.txt`；+3988/-4030 行；未作语义复核。
- M `activities/coronation_activity/coronation_events_6.txt`；+292/-220 行；未作语义复核。
- M `activities/coronation_activity/coronation_events_klank.txt`；+158/-141 行；未作语义复核。
- M `activities/coronation_activity/guest_intent_coronation_events.txt`；+185/-183 行；未作语义复核。
- M `activities/coronation_activity/prelude_events.txt`；+296/-297 行；未作语义复核。
- M `activities/debate_activity/az_debate_events.txt`；+36/-36 行；未作语义复核。
- M `activities/debate_activity/debate_events.txt`；+18/-19 行；未作语义复核。
- A `activities/ecumenical_council_activity/pam_ecumemincal_council_summons_events.txt`；+2177/-0 行；未作语义复核。
- A `activities/ecumenical_council_activity/pam_ecumenical_council_events.txt`；+14870/-0 行；未作语义复核。
- A `activities/ecumenical_council_activity/pam_ecumenical_council_events_josh.txt`；+2048/-0 行；未作语义复核。
- A `activities/ecumenical_council_activity/pam_investiture_council_events.txt`；+605/-0 行；未作语义复核。
- M `activities/feast_activity/feast_default_events_axel.txt`；+26/-6 行；未作语义复核。
- M `activities/feast_activity/feast_default_events_jason.txt`；+4/-4 行；未作语义复核。
- M `activities/feast_activity/feast_default_events_joe.txt`；+40/-8 行；未作语义复核。
- M `activities/feast_activity/feast_default_events_laurence.txt`；+5/-5 行；未作语义复核。
- M `activities/feast_activity/feast_events.txt`；+546/-59 行；未作语义复核。
- M `activities/feast_activity/feast_events_ewan.txt`；+17/-17 行；未作语义复核。
- M `activities/feast_activity/feast_events_flavor.txt`；+56/-67 行；未作语义复核。
- M `activities/feast_activity/feast_events_klank.txt`；+2/-4 行；未作语义复核。
- M `activities/feast_activity/feast_events_mkc.txt`；+3/-3 行；未作语义复核。
- M `activities/feast_activity/feast_events_tova.txt`；+3/-3 行；未作语义复核。
- M `activities/feast_activity/main_events/feast_default_events.txt`；+1133/-492 行；未作语义复核。
- M `activities/feast_activity/main_events/feast_default_events_alex.txt`；+12/-11 行；未作语义复核。
- M `activities/feast_activity/main_events/feast_lifestyle_events.txt`；+6/-6 行；未作语义复核。
- M `activities/feast_activity/main_events/feast_main_befriend_events.txt`；+2/-2 行；未作语义复核。
- M `activities/feast_activity/main_events/feast_main_live_fowl_events.txt`；+6/-5 行；未作语义复核。
- M `activities/feast_activity/main_events/feast_main_stable_breakin_events.txt`；+4/-4 行；未作语义复核。
- M `activities/feast_activity/main_events/feast_main_stew_flood_events.txt`；+10/-6 行；未作语义复核。
- M `activities/feast_activity/main_events/feast_tsagaan_sar_events.txt`；+76/-70 行；未作语义复核。
- M `activities/feast_activity/murder_feast_events.txt`；+13/-11 行；未作语义复核。
- M `activities/festival_activity/festival_events.txt`；+28/-17 行；未作语义复核。
- M `activities/funeral_activity/funeral_events.txt`；+248/-177 行；未作语义复核。
- M `activities/hold_court_activity/hold_court_events_general.txt`；+639/-576 行；未作语义复核。
- M `activities/hold_court_activity/hold_court_events_james.txt`；+9/-9 行；未作语义复核。
- M `activities/hold_court_activity/hold_court_events_joe.txt`；+38/-35 行；未作语义复核。
- M `activities/hunt_activity/hunt_events.txt`；+656/-347 行；未作语义复核。
- M `activities/hunt_activity/jb_hunt_events.txt`；+69/-62 行；未作语义复核。
- M `activities/hunt_activity/mpo_hunt_events.txt`；+56/-58 行；未作语义复核。
- M `activities/hunt_activity/mpo_nerge_events.txt`；+36/-36 行；未作语义复核。
- M `activities/hunt_activity/tgp_hunt_events.txt`；+32/-28 行；未作语义复核。
- M `activities/imperial_examination_activity/az_examination_events.txt`；+57/-57 行；未作语义复核。
- M `activities/imperial_examination_activity/emperor_prep_phase_imperial_examination_events.txt`；+10/-8 行；未作语义复核。
- M `activities/imperial_examination_activity/imperial_examination_events.txt`；+159/-147 行；未作语义复核。
- M `activities/imperial_examination_activity/imperial_examination_events_jay.txt`；+13/-13 行；未作语义复核。
- M `activities/petition_liege_activity/petition_liege_events.txt`；+93/-93 行；未作语义复核。
- M `activities/pilgrimage_activity/hajj_events.txt`；+42/-30 行；未作语义复核。
- M `activities/pilgrimage_activity/pilgrimage_events.txt`；+1258/-520 行；未作语义复核。
- M `activities/pilgrimage_activity/pilgrimage_events_seasia.txt`；+65/-62 行；未作语义复核。
- M `activities/pilgrimage_activity/pilgrimage_intent_events.txt`；+75/-61 行；未作语义复核。
- M `activities/playdate_activity/playdate_events.txt`；+107/-111 行；未作语义复核。
- M `activities/tour_activity/az_tour_events.txt`；+433/-430 行；未作语义复核。
- M `activities/tour_activity/claudia_tour_grounds_events.txt`；+4/-4 行；未作语义复核。
- M `activities/tour_activity/filippa_tour_general_events.txt`；+49/-50 行；未作语义复核。
- M `activities/tour_activity/tour_general_events.txt`；+59/-59 行；未作语义复核。
- M `activities/tour_activity/tour_general_events_james.txt`；+6/-6 行；未作语义复核。
- M `activities/tour_activity/tour_grounds_events_chad.txt`；+38/-33 行；未作语义复核。
- M `activities/tour_activity/tour_phase_cultural_festival.txt`；+264/-207 行；未作语义复核。
- M `activities/tour_activity/tour_phase_cultural_festival_james.txt`；+49/-59 行；未作语义复核。
- M `activities/tour_activity/tour_phase_host_a_dinner.txt`；+247/-263 行；未作语义复核。
- M `activities/tour_activity/tour_phase_tour_grounds.txt`；+113/-106 行；未作语义复核。
- M `activities/tour_activity/tour_travel_events.txt`；+70/-65 行；未作语义复核。
- M `activities/tour_activity/tour_travel_events_dan.txt`；+70/-78 行；未作语义复核。
- M `activities/tour_activity/tour_travel_events_james.txt`；+86/-35 行；未作语义复核。
- M `activities/tournaments/contest_events.txt`；+161/-122 行；未作语义复核。
- M `activities/tournaments/ep2_locale_events.txt`；+376/-318 行；未作语义复核。
- M `activities/tournaments/james_tournament_events.txt`；+15/-15 行；未作语义复核。
- M `activities/tournaments/jason_first_race_event.txt`；+13/-5 行；未作语义复核。
- M `activities/tournaments/jason_locale_events.txt`；+38/-38 行；未作语义复核。
- M `activities/tournaments/jason_race_events.txt`；+26/-18 行；未作语义复核。
- M `activities/tournaments/jb_recital_contest_events.txt`；+22/-20 行；未作语义复核。
- M `activities/tournaments/passive_tournament_events_oltner.txt`；+38/-29 行；未作语义复核。
- M `activities/tournaments/tournament_events.txt`；+379/-323 行；未作语义复核。
- M `activities/tournaments/veronica_local_events_2.txt`；+42/-33 行；未作语义复核。
- M `activities/tournaments/veronica_locale_events.txt`；+49/-46 行；未作语义复核。
- M `artifacts/artifact_events.txt`；+143/-205 行；未作语义复核。
- M `artifacts/historical_artifacts_events.txt`；+115/-29 行；未作语义复核。
- M `birth_events.txt`；+183/-50 行；未作语义复核。
- M `blackmail_events.txt`；+8/-4 行；未作语义复核。
- M `board_game_events.txt`；+6/-6 行；未作语义复核。
- M `bookmark_events.txt`；+20/-11 行；未作语义复核。
- M `bp1_dan_events.txt`；+78/-54 行；未作语义复核。
- A `clerical_chastity_vow_events.txt`；+23/-0 行；未作语义复核。
- M `councillor_task_events/chancellor_task_events.txt`；+75/-178 行；未作语义复核。
- M `councillor_task_events/councillor_spouse_background_events.txt`；+2/-6 行；未作语义复核。
- M `councillor_task_events/councillor_spouse_events/councillor_spouse_diplomacy_events.txt`；+3/-4 行；未作语义复核。
- M `councillor_task_events/councillor_spouse_events/councillor_spouse_intrigue_events.txt`；+3/-17 行；未作语义复核。
- M `councillor_task_events/councillor_spouse_events/councillor_spouse_learning_events.txt`；+17/-19 行；未作语义复核。
- M `councillor_task_events/councillor_spouse_events/councillor_spouse_stewardship_events.txt`；+9/-10 行；未作语义复核。
- M `councillor_task_events/court_chaplain_task_events.txt`；+245/-16 行；未作语义复核。
- M `councillor_task_events/marshal_task_events.txt`；+76/-100 行；未作语义复核。
- M `councillor_task_events/spymaster_task_events.txt`；+9/-9 行；未作语义复核。
- M `councillor_task_events/steward_task_events.txt`；+43/-91 行；未作语义复核。
- M `court_events/01_ep3_court_events.txt`；+24/-24 行；未作语义复核。
- M `court_events/01_ep3_court_events_3.txt`；+63/-62 行；未作语义复核。
- M `court_events/court_events_ceremonial.txt`；+13/-13 行；未作语义复核。
- M `court_events/court_events_general.txt`；+2488/-2446 行；未作语义复核。
- M `court_events/court_events_general_1.txt`；+7/-7 行；未作语义复核。
- M `court_events/court_events_new.txt`；+3/-2 行；未作语义复核。
- M `court_events/introduce_court_fashion_events.txt`；+2/-2 行；未作语义复核。
- M `court_events/sumptuary_debate_events.txt`；+21/-21 行；未作语义复核。
- M `court_maintenance_events.txt`；+17/-3 行；未作语义复核。
- M `courtier_guest_management_events/courtier_guest_management_events.txt`；+17/-28 行；未作语义复核。
- M `culture_events/culture_emergence_events.txt`；+4/-2 行；未作语义复核。
- M `culture_events/culture_notification_events.txt`；+114/-34 行；未作语义复核。
- M `culture_events/culture_tradition_events.txt`；+69/-72 行；未作语义复核。
- M `culture_events/language_events.txt`；+6/-6 行；未作语义复核。
- M `death_events/death_management_events.txt`；+385/-160 行；未作语义复核。
- M `decisions_events/bp3_decisions_events.txt`；+5/-2 行；未作语义复核。
- M `decisions_events/british_isles_events.txt`；+8/-13 行；未作语义复核。
- M `decisions_events/ce1_decision_events.txt`；+8/-10 行；未作语义复核。
- M `decisions_events/culture_conversion_events.txt`；+1/-1 行；未作语义复核。
- M `decisions_events/east_europe_events.txt`；+93/-92 行；未作语义复核。
- M `decisions_events/ep2_decision_events.txt`；+1/-1 行；未作语义复核。
- M `decisions_events/ep4_decision_events.txt`；+6/-6 行；未作语义复核。
- M `decisions_events/iberia_north_africa_events.txt`；+39/-585 行；未作语义复核。
- M `decisions_events/major_decisions_events.txt`；+51/-21 行；未作语义复核。
- M `decisions_events/middle_east_decisions_events.txt`；+40/-43 行；未作语义复核。
- M `decisions_events/middle_europe_decisions_events.txt`；+65/-8 行；未作语义复核。
- M `decisions_events/minor_decision_events.txt`；+15/-15 行；未作语义复核。
- M `decisions_events/mpo_greatest_of_khans_events.txt`；+16/-18 行；未作语义复核。
- M `decisions_events/pay_homage_events.txt`；+23/-9 行；未作语义复核。
- M `decisions_events/pledge_loyalty_to_liege_events.txt`；+2/-2 行；未作语义复核。
- M `decisions_events/roman_restoration_events.txt`；+256/-43 行；未作语义复核。
- M `decisions_events/south_asia_events.txt`；+134/-166 行；未作语义复核。
- M `decisions_events/tgp_decision_events.txt`；+27/-15 行；未作语义复核。
- M `diarchy_events/diarchy_events.txt`；+149/-176 行；未作语义复核。
- M `diarchy_events/vizierate_events.txt`；+4/-4 行；未作语义复核。
- M `dlc/ach/ach_coronation_events.txt`；+219/-216 行；未作语义复核。
- M `dlc/ach/ach_maintenance_events.txt`；+19/-5 行；未作语义复核。
- M `dlc/ach/ach_yearly_events.txt`；+18/-17 行；未作语义复核。
- M `dlc/bp1/bp1_filippa_yearly_events.txt`；+37/-41 行；未作语义复核。
- M `dlc/bp1/bp1_henrik_events.txt`；+14/-14 行；未作语义复核。
- M `dlc/bp1/bp1_house_feud.txt`；+82/-62 行；未作语义复核。
- M `dlc/bp1/bp1_yearly.txt`；+391/-373 行；未作语义复核。
- M `dlc/bp1/bp1_yearly_develop.txt`；+11/-9 行；未作语义复核。
- M `dlc/bp1/bp1_yearly_events_chad.txt`；+31/-31 行；未作语义复核。
- M `dlc/bp1/bp1_yearly_events_claudia.txt`；+63/-69 行；未作语义复核。
- M `dlc/bp1/bp1_yearly_events_nick.txt`；+53/-62 行；未作语义复核。
- M `dlc/bp1/bp1_yearly_oltner.txt`；+50/-52 行；未作语义复核。
- M `dlc/bp2/bp2_adult_education_activity_events.txt`；+169/-158 行；未作语义复核。
- M `dlc/bp2/bp2_adult_education_activity_events_oltner.txt`；+60/-57 行；未作语义复核。
- M `dlc/bp2/bp2_character_interaction_events.txt`；+2/-2 行；未作语义复核。
- M `dlc/bp2/bp2_child_of_destiny_events.txt`；+28/-27 行；未作语义复核。
- M `dlc/bp2/bp2_decision_events.txt`；+37/-11 行；未作语义复核。
- M `dlc/bp2/bp2_hostage_system.txt`；+1/-1 行；未作语义复核。
- M `dlc/bp2/bp2_yearly.txt`；+79/-76 行；未作语义复核。
- M `dlc/bp2/bp2_yearly_0_5.txt`；+42/-46 行；未作语义复核。
- M `dlc/bp2/bp2_yearly_1_events.txt`；+43/-39 行；未作语义复核。
- M `dlc/bp2/bp2_yearly_2.txt`；+51/-82 行；未作语义复核。
- M `dlc/bp2/bp2_yearly_3.txt`；+7/-7 行；未作语义复核。
- M `dlc/bp2/bp2_yearly_4.txt`；+38/-39 行；未作语义复核。
- M `dlc/bp2/bp2_yearly_5.txt`；+58/-60 行；未作语义复核。
- M `dlc/bp2/bp2_yearly_7.txt`；+79/-81 行；未作语义复核。
- M `dlc/bp2/bp2_yearly_events_6.txt`；+238/-198 行；未作语义复核。
- M `dlc/bp2/bp2_yearly_extra.txt`；+2/-2 行；未作语义复核。
- M `dlc/bp2/story_cycles/story_cycle_pet_rock_events.txt`；+12/-12 行；未作语义复核。
- M `dlc/bp3/bp3_journey_events.txt`；+200/-119 行；未作语义复核。
- M `dlc/bp3/bp3_mapmaking.txt`；+2/-4 行；未作语义复核。
- M `dlc/bp3/bp3_roaming_events.txt`；+42/-39 行；未作语义复核。
- M `dlc/bp3/bp3_survey_events.txt`；+59/-28 行；未作语义复核。
- M `dlc/ce1/epidemic_events.txt`；+814/-226 行；未作语义复核。
- M `dlc/ce1/epidemic_events_2.txt`；+19/-19 行；未作语义复核。
- M `dlc/ce1/legend_ending_events.txt`；+3/-0 行；未作语义复核。
- M `dlc/ce1/legend_events.txt`；+11/-18 行；未作语义复核。
- M `dlc/ce1/legend_spread_events_8.txt`；+90/-83 行；未作语义复核。
- M `dlc/ce1/legend_spread_events_nick.txt`；+150/-148 行；未作语义复核。
- M `dlc/ce1/legend_spread_events_veronica.txt`；+52/-55 行；未作语义复核。
- M `dlc/ce1/physician_epidemic_events.txt`；+11/-11 行；未作语义复核。
- M `dlc/ep1/ep1_character_interaction_events.txt`；+3/-3 行；未作语义复核。
- M `dlc/ep1/ep1_decision_events.txt`；+39/-13 行；未作语义复核。
- M `dlc/ep1/ep1_flavor_events.txt`；+86/-84 行；未作语义复核。
- M `dlc/ep1/ep1_fund_inspiration_events.txt`；+381/-281 行；未作语义复核。
- M `dlc/ep2/ep2_accolade_events.txt`；+16/-16 行；未作语义复核。
- M `dlc/ep2/ep2_tournament_events.txt`；+259/-266 行；未作语义复核。
- M `dlc/ep2/wedding_events/ep2_bloody_wedding_events.txt`；+10/-6 行；未作语义复核。
- M `dlc/ep2/wedding_events/ep2_wedding_events.txt`；+317/-258 行；未作语义复核。
- M `dlc/ep2/wedding_events/ep2_wedding_events_ewan.txt`；+48/-48 行；未作语义复核。
- M `dlc/ep3/ep3_admin_events.txt`；+41/-29 行；未作语义复核。
- M `dlc/ep3/ep3_akolouthos_events.txt`；+3/-0 行；未作语义复核。
- M `dlc/ep3/ep3_camp_party_events.txt`；+52/-41 行；未作语义复核。
- M `dlc/ep3/ep3_camp_temperament_events.txt`；+24/-24 行；未作语义复核。
- M `dlc/ep3/ep3_contract_events.txt`；+545/-132 行；未作语义复核。
- M `dlc/ep3/ep3_councillor_events.txt`；+11/-11 行；未作语义复核。
- M `dlc/ep3/ep3_decisions_events.txt`；+286/-255 行；未作语义复核。
- M `dlc/ep3/ep3_emperor_yearly_2.txt`；+186/-156 行；未作语义复核。
- M `dlc/ep3/ep3_emperor_yearly_3.txt`；+83/-75 行；未作语义复核。
- M `dlc/ep3/ep3_emperor_yearly_8.txt`；+39/-51 行；未作语义复核。
- M `dlc/ep3/ep3_eparch_events.txt`；+27/-26 行；未作语义复核。
- M `dlc/ep3/ep3_frankokratia_events.txt`；+200/-220 行；未作语义复核。
- M `dlc/ep3/ep3_governor_yearly_3.txt`；+280/-224 行；未作语义复核。
- M `dlc/ep3/ep3_governor_yearly_8.txt`；+70/-65 行；未作语义复核。
- M `dlc/ep3/ep3_interactions_events.txt`；+191/-115 行；未作语义复核。
- M `dlc/ep3/ep3_laamp_decision_events.txt`；+456/-550 行；未作语义复核。
- M `dlc/ep3/ep3_laamp_events.txt`；+398/-366 行；未作语义复核。
- M `dlc/ep3/ep3_laamp_events_8.txt`；+45/-40 行；未作语义复核。
- M `dlc/ep3/ep3_laamp_flavor.txt`；+15/-11 行；未作语义复核。
- M `dlc/ep3/ep3_laamp_flavor_oltner.txt`；+3/-3 行；未作语义复核。
- M `dlc/ep3/ep3_laamp_flavour_ewan_events.txt`；+382/-353 行；未作语义复核。
- M `dlc/ep3/ep3_laamps_provisions.txt`；+13/-13 行；未作语义复核。
- M `dlc/ep3/ep3_landless_admin_events.txt`；+90/-85 行；未作语义复核。
- M `dlc/ep3/ep3_powerful_families_8.txt`；+59/-44 行；未作语义复核。
- M `dlc/ep3/ep3_roman_restoration_events.txt`；+37/-6 行；未作语义复核。
- M `dlc/ep3/ep3_story_cycle_admin_eunuch_events.txt`；+95/-87 行；未作语义复核。
- M `dlc/ep3/ep3_story_cycle_grand_ambitions_events.txt`；+93/-93 行；未作语义复核。
- M `dlc/ep3/ep3_story_cycle_harrying_of_the_north_events.txt`；+92/-81 行；未作语义复核。
- M `dlc/ep3/ep3_story_cycle_violet_poet_events.txt`；+59/-38 行；未作语义复核。
- M `dlc/ep3/ep3_travel_events_3.txt`；+51/-68 行；未作语义复核。
- M `dlc/ep3/ep3_travel_events_8.txt`；+7/-7 行；未作语义复核。
- M `dlc/ep3/ep3_wedding_events.txt`；+95/-208 行；未作语义复核。
- M `dlc/fp1/fp1_jomsvikings_events.txt`；+25/-25 行；未作语义复核。
- M `dlc/fp1/fp1_major_decision_events.txt`；+10/-10 行；未作语义复核。
- M `dlc/fp1/fp1_other_decision_events.txt`；+83/-114 行；未作语义复核。
- M `dlc/fp1/fp1_scandinavian_adventurer_events.txt`；+3/-3 行；未作语义复核。
- M `dlc/fp1/fp1_shieldmaiden_events.txt`；+9/-9 行；未作语义复核。
- M `dlc/fp1/fp1_trade_events.txt`；+32/-32 行；未作语义复核。
- M `dlc/fp1/fp1_trial_by_combat_events.txt`；+97/-55 行；未作语义复核。
- M `dlc/fp1/fp1_yearly_events.txt`；+218/-215 行；未作语义复核。
- M `dlc/fp1/fp1_yearly_events_oltner.txt`；+46/-45 行；未作语义复核。
- M `dlc/fp2/fp2_el_cid_events.txt`；+4/-4 行；未作语义复核。
- M `dlc/fp2/fp2_lyonese_monk_events.txt`；+182/-108 行；未作语义复核。
- M `dlc/fp2/fp2_other_decision_events.txt`；+61/-113 行；未作语义复核。
- M `dlc/fp2/fp2_struggle_events.txt`；+251/-219 行；未作语义复核。
- M `dlc/fp2/fp2_yearly_events.txt`；+131/-118 行；未作语义复核。
- M `dlc/fp3/fp3_clan_events_2000.txt`；+24/-21 行；未作语义复核。
- M `dlc/fp3/fp3_clan_events_hugo.txt`；+4/-4 行；未作语义复核。
- M `dlc/fp3/fp3_clan_events_ola.txt`；+37/-36 行；未作语义复核。
- M `dlc/fp3/fp3_clan_events_persia_specific_ola.txt`；+13/-13 行；未作语义复核。
- M `dlc/fp3/fp3_dynasty_decision_events.txt`；+8/-8 行；未作语义复核。
- M `dlc/fp3/fp3_extra_flavor_events.txt`；+39/-37 行；未作语义复核。
- M `dlc/fp3/fp3_frontier_story_cycle.txt`；+38/-34 行；未作语义复核。
- M `dlc/fp3/fp3_heritage_events.txt`；+86/-83 行；未作语义复核。
- M `dlc/fp3/fp3_misc_decision_events.txt`；+7/-5 行；未作语义复核。
- M `dlc/fp3/fp3_religious_decision_events.txt`；+30/-30 行；未作语义复核。
- M `dlc/fp3/fp3_scholarship_events.txt`；+55/-51 行；未作语义复核。
- M `dlc/fp3/fp3_story_cycle_zanj_rebellion_events.txt`；+10/-9 行；未作语义复核。
- M `dlc/fp3/fp3_struggle_events.txt`；+26/-14 行；未作语义复核。
- M `dlc/fp3/fp3_tax_collector_events_ola.txt`；+19/-20 行；未作语义复核。
- M `dlc/fp3/fp3_tax_collector_flavor_events.txt`；+10/-10 行；未作语义复核。
- M `dlc/fp3/fp3_yearly_events_eren.txt`；+96/-91 行；未作语义复核。
- M `dlc/fp3/fp3_yearly_events_hugo.txt`；+8/-8 行；未作语义复核。
- M `dlc/fp3/fp3_yearly_events_ola_batch_1.txt`；+66/-75 行；未作语义复核。
- M `dlc/fp3/fp3_yearly_frontier_chains.txt`；+9/-9 行；未作语义复核。
- M `dlc/mpo/court_astrologer_events.txt`；+6/-6 行；未作语义复核。
- M `dlc/mpo/mpo_decisions_events.txt`；+135/-102 行；未作语义复核。
- M `dlc/mpo/mpo_events_anna.txt`；+30/-20 行；未作语义复核。
- M `dlc/mpo/mpo_events_ariana.txt`；+51/-57 行；未作语义复核。
- M `dlc/mpo/mpo_events_tova.txt`；+37/-25 行；未作语义复核。
- M `dlc/mpo/mpo_flavor_events_settled.txt`；+18/-14 行；未作语义复核。
- M `dlc/mpo/mpo_interactions_events.txt`；+40/-11 行；未作语义复核。
- M `dlc/mpo/mpo_jamukha_flavor_events.txt`；+9/-6 行；未作语义复核。
- M `dlc/mpo/mpo_migration_contract_events.txt`；+1/-0 行；未作语义复核。
- M `dlc/mpo/mpo_migration_events.txt`；+97/-70 行；未作语义复核。
- M `dlc/mpo/mpo_migration_travel_events.txt`；+24/-21 行；未作语义复核。
- M `dlc/mpo/mpo_nomad_events_1.txt`；+77/-72 行；未作语义复核。
- M `dlc/mpo/mpo_nomads_blood_brothers_windy.txt`；+1/-1 行；未作语义复核。
- M `dlc/mpo/mpo_nomads_flavour_events.txt`；+146/-121 行；未作语义复核。
- M `dlc/mpo/mpo_nomads_flavour_events_oltner.txt`；+6/-6 行；未作语义复核。
- M `dlc/mpo/mpo_nomads_season_events.txt`；+8/-8 行；未作语义复核。
- M `dlc/mpo/mpo_story_cycle_temujin_flavor_events.txt`；+86/-43 行；未作语义复核。
- A `dlc/pam/heresy/pam_heresy_dangerous_rite_events.txt`；+640/-0 行；未作语义复核。
- A `dlc/pam/heresy/pam_heresy_historical_events.txt`；+870/-0 行；未作语义复核。
- A `dlc/pam/heresy/pam_heresy_light_events.txt`；+519/-0 行；未作语义复核。
- A `dlc/pam/heresy/pam_heresy_pulse.txt`；+177/-0 行；未作语义复核。
- A `dlc/pam/pam_adorcism_events.txt`；+194/-0 行；未作语义复核。
- A `dlc/pam/pam_antipope_events.txt`；+978/-0 行；未作语义复核。
- A `dlc/pam/pam_bull_events.txt`；+328/-0 行；未作语义复核。
- A `dlc/pam/pam_christian_situation_events.txt`；+1332/-0 行；未作语义复核。
- A `dlc/pam/pam_clergy_events.txt`；+972/-0 行；未作语义复核。
- A `dlc/pam/pam_decision_events.txt`；+3485/-0 行；未作语义复核。
- A `dlc/pam/pam_generic_events.txt`；+1899/-0 行；未作语义复核。
- A `dlc/pam/pam_great_projects_events.txt`；+3305/-0 行；未作语义复核。
- A `dlc/pam/pam_holy_myron_events.txt`；+722/-0 行；未作语义复核。
- A `dlc/pam/pam_interactions_events.txt`；+5397/-0 行；未作语义复核。
- A `dlc/pam/pam_kingdom_of_heaven_events.txt`；+54/-0 行；未作语义复核。
- A `dlc/pam/pam_monastic_funeral_events.txt`；+118/-0 行；未作语义复核。
- A `dlc/pam/pam_religious_artifact_events.txt`；+340/-0 行；未作语义复核。
- A `dlc/pam/pam_ritual_celebrations_events.txt`；+286/-0 行；未作语义复核。
- A `dlc/pam/pam_saint_events.txt`；+498/-0 行；未作语义复核。
- A `dlc/pam/pam_secular_faith_events.txt`；+8442/-0 行；未作语义复核。
- A `dlc/pam/pam_spread_tenet_activity_events.txt`；+844/-0 行；未作语义复核。
- A `dlc/pam/pam_tenet_events.txt`；+802/-0 行；未作语义复核。
- A `dlc/pam/pam_theocratic_budget_events.txt`；+25/-0 行；未作语义复核。
- A `dlc/pam/pam_theocratic_ruler_events.txt`；+3144/-0 行；未作语义复核。
- M `dlc/tgp/tgp_ceremonial_liege_events.txt`；+21/-21 行；未作语义复核。
- M `dlc/tgp/tgp_child_personality_events.txt`；+381/-833 行；未作语义复核。
- M `dlc/tgp/tgp_china_career_events.txt`；+1/-1 行；未作语义复核。
- M `dlc/tgp/tgp_china_decision_events.txt`；+6/-5 行；未作语义复核。
- M `dlc/tgp/tgp_china_ministry_events.txt`；+14/-3 行；未作语义复核。
- M `dlc/tgp/tgp_china_yearly_events.txt`；+20/-18 行；未作语义复核。
- M `dlc/tgp/tgp_commission_book.txt`；+7/-4 行；未作语义复核。
- M `dlc/tgp/tgp_dynastic_cycle_events.txt`；+20/-4 行；未作语义复核。
- M `dlc/tgp/tgp_dynastic_cycle_flavor_events.txt`；+22/-19 行；未作语义复核。
- M `dlc/tgp/tgp_east_asia_decision_events.txt`；+1/-11 行；未作语义复核。
- M `dlc/tgp/tgp_east_asia_interaction_events.txt`；+18/-11 行；未作语义复核。
- M `dlc/tgp/tgp_faction_events.txt`；+2/-2 行；未作语义复核。
- M `dlc/tgp/tgp_genpei_character_events.txt`；+10/-17 行；未作语义复核。
- M `dlc/tgp/tgp_governor_contract_events.txt`；+14/-0 行；未作语义复核。
- M `dlc/tgp/tgp_governor_contract_events_2000.txt`；+3/-2 行；未作语义复核。
- M `dlc/tgp/tgp_house_blocs.txt`；+9/-2 行；未作语义复核。
- M `dlc/tgp/tgp_interaction_events.txt`；+4/-4 行；未作语义复核。
- M `dlc/tgp/tgp_japan_decision_events.txt`；+19/-54 行；未作语义复核。
- M `dlc/tgp/tgp_japan_general_events.txt`；+16/-15 行；未作语义复核。
- M `dlc/tgp/tgp_japan_yearly_events.txt`；+104/-90 行；未作语义复核。
- M `dlc/tgp/tgp_japan_yearly_events_ariana.txt`；+93/-84 行；未作语义复核。
- M `dlc/tgp/tgp_mandala_capital_events.txt`；+1/-0 行；未作语义复核。
- M `dlc/tgp/tgp_mandala_devaraja_events.txt`；+27/-18 行；未作语义复核。
- M `dlc/tgp/tgp_mandala_events.txt`；+28/-13 行；未作语义复核。
- M `dlc/tgp/tgp_mandala_task_contract_events.txt`；+116/-59 行；未作语义复核。
- M `dlc/tgp/tgp_movement_events.txt`；+68/-61 行；未作语义复核。
- M `dlc/tgp/tgp_natural_disaster_flavor_events.txt`；+13/-12 行；未作语义复核。
- M `dlc/tgp/tgp_silk_road_events.txt`；+1/-1 行；未作语义复核。
- M `dlc/tgp/tgp_tai_migration_events.txt`；+5/-4 行；未作语义复核。
- M `dlc/tgp/tgp_travel_danger_events.txt`；+5/-4 行；未作语义复核。
- M `dlc/tgp/tgp_tribute_mission_events.txt`；+80/-43 行；未作语义复核。
- M `education_and_childhood/child_personality_events.txt`；+422/-592 行；未作语义复核。
- M `education_and_childhood/child_personality_events_2.txt`；+313/-658 行；未作语义复核。
- M `education_and_childhood/childhood_education_events.txt`；+18/-18 行；未作语义复核。
- M `education_and_childhood/childhood_events.txt`；+95/-83 行；未作语义复核。
- M `education_and_childhood/childhood_events_oltner.txt`；+29/-30 行；未作语义复核。
- M `education_and_childhood/chinese_disciple_events.txt`；+21/-21 行；未作语义复核。
- M `education_and_childhood/coming_of_age_events.txt`；+91/-7 行；未作语义复核。
- M `elder_events.txt`；+6/-6 行；未作语义复核。
- A `empire_faith_gate_events.txt`；+278/-0 行；已复核关键定义/差异。
- M `error_suppression_events.txt`；+84/-2 行；未作语义复核。
- M `factions/faction_demands.txt`；+24/-61 行；未作语义复核。
- M `game_rule_events.txt`；+19/-19 行；未作语义复核。
- M `global_religion_events.txt`；+230/-112 行；未作语义复核。
- M `government_events/clan_events.txt`；+4/-3 行；未作语义复核。
- M `harm_events.txt`；+138/-133 行；未作语义复核。
- M `health_events.txt`；+196/-142 行；未作语义复核。
- M `historical_character_events.txt`；+19/-24 行；未作语义复核。
- M `interaction_events/bastard_interaction_events.txt`；+5/-5 行；未作语义复核。
- M `interaction_events/character_interaction_events.txt`；+255/-152 行；未作语义复核。
- A `interaction_events/demand_church_succession_events.txt`；+243/-0 行；未作语义复核。
- M `interaction_events/marriage_interaction_events.txt`；+27/-27 行；未作语义复核。
- M `interaction_events/perk_interaction_events.txt`；+2/-2 行；未作语义复核。
- M `interaction_events/vassal_interaction_events.txt`；+6/-6 行；未作语义复核。
- M `jester_stress_relief_events.txt`；+54/-54 行；未作语义复核。
- M `lifestyles/commission_epic_events.txt`；+39/-37 行；未作语义复核。
- M `lifestyles/governance_lifestyle/stewardship_domain_events.txt`；+112/-117 行；未作语义复核。
- M `lifestyles/governance_lifestyle/stewardship_duty_events.txt`；+69/-72 行；未作语义复核。
- M `lifestyles/governance_lifestyle/stewardship_general_events.txt`；+186/-243 行；未作语义复核。
- M `lifestyles/governance_lifestyle/stewardship_wealth_events.txt`；+54/-61 行；未作语义复核。
- M `lifestyles/intrigue_lifestyle/intrigue_dread_events.txt`；+80/-76 行；未作语义复核。
- M `lifestyles/intrigue_lifestyle/intrigue_scheming_events.txt`；+52/-68 行；未作语义复核。
- M `lifestyles/intrigue_lifestyle/intrigue_temptation_events.txt`；+61/-68 行；未作语义复核。
- M `lifestyles/intrigue_lifestyle/intrigue_temptation_events_2.txt`；+85/-139 行；未作语义复核。
- M `lifestyles/mystic_lifestyle_events.txt`；+26/-4 行；未作语义复核。
- M `lifestyles/scholarship_lifestyle/learning_medicine_events.txt`；+74/-73 行；未作语义复核。
- M `lifestyles/scholarship_lifestyle/learning_scholarship_events.txt`；+73/-63 行；未作语义复核。
- M `lifestyles/scholarship_lifestyle/learning_theology_events.txt`；+95/-79 行；未作语义复核。
- M `lifestyles/sell_titles_events.txt`；+11/-6 行；未作语义复核。
- M `lifestyles/statecraft_lifestyle/diplomacy_family_events.txt`；+52/-64 行；未作语义复核。
- M `lifestyles/statecraft_lifestyle/diplomacy_foreign_events.txt`；+88/-89 行；未作语义复核。
- M `lifestyles/statecraft_lifestyle/diplomacy_generic_events.txt`；+10/-9 行；未作语义复核。
- M `lifestyles/statecraft_lifestyle/diplomacy_majesty_events.txt`；+39/-39 行；未作语义复核。
- M `lifestyles/wanderer_lifestyle/wanderer_destination_events.txt`；+9/-24 行；未作语义复核。
- M `lifestyles/wanderer_lifestyle/wanderer_generic_events.txt`；+17/-15 行；未作语义复核。
- M `lifestyles/wanderer_lifestyle/wanderer_internal_affairs_events.txt`；+18/-17 行；未作语义复核。
- M `lifestyles/wanderer_lifestyle/wanderer_journey_events.txt`；+14/-13 行；未作语义复核。
- M `lifestyles/warfare_lifestyle/historical_commander_trait_events.txt`；+33/-33 行；未作语义复核。
- M `lifestyles/warfare_lifestyle/learn_commander_trait_events.txt`；+404/-1833 行；未作语义复核。
- M `lifestyles/warfare_lifestyle/martial_authority_events.txt`；+47/-33 行；未作语义复核。
- M `lifestyles/warfare_lifestyle/martial_authority_events_2.txt`；+2/-2 行；未作语义复核。
- M `lifestyles/warfare_lifestyle/martial_chivalry_events.txt`；+338/-102 行；未作语义复核。
- M `lifestyles/warfare_lifestyle/martial_strategy_events.txt`；+31/-30 行；未作语义复核。
- M `lifestyles/warfare_lifestyle/martial_strategy_events_2.txt`；+8/-8 行；未作语义复核。
- M `lifestyles/warfare_lifestyle/warhorse_events.txt`；+6/-6 行；未作语义复核。
- M `marriage_effect_events.txt`；+34/-33 行；未作语义复核。
- M `mpo_chaotic_kurultai_succession.txt`；+1/-0 行；未作语义复核。
- M `mpo_flavor_events.txt`；+2/-2 行；未作语义复核。
- M `nickname_events/nickname_events.txt`；+10/-10 行；未作语义复核。
- M `notification_events/ep1_notification_events.txt`；+1/-0 行；未作语义复核。
- A `passive_rite_learning_events/passive_rite_learning_travel_events.txt`；+189/-0 行；未作语义复核。
- M `pregnancy_events.txt`；+23/-22 行；未作语义复核。
- M `prison_events/dungeon_ongoing_events.txt`；+25/-25 行；未作语义复核。
- M `prison_events/house_arrest_ongoing_events.txt`；+17/-24 行；未作语义复核。
- M `prison_events/prison_events.txt`；+70/-43 行；未作语义复核。
- M `realm_maintenance_events.txt`；+1/-1 行；未作语义复核。
- M `relations_events/adultery_events.txt`；+36/-35 行；未作语义复核。
- M `relations_events/bishop_events.txt`；+31/-24 行；未作语义复核。
- M `relations_events/friendship_events.txt`；+72/-75 行；未作语义复核。
- M `relations_events/lover_events.txt`；+78/-132 行；未作语义复核。
- M `relations_events/parent_events.txt`；+7/-7 行；未作语义复核。
- M `relations_events/relation_upgrade_events.txt`；+49/-49 行；未作语义复核。
- M `relations_events/rivalry_events.txt`；+17/-17 行；未作语义复核。
- M `relations_events/sibling_events.txt`；+24/-26 行；未作语义复核。
- M `relations_events/spouse_events.txt`；+31/-15 行；未作语义复核。
- M `relations_events/vassal_events.txt`；+135/-79 行；未作语义复核。
- M `religion_events/faith_conversion_events.txt`；+172/-100 行；未作语义复核。
- M `religion_events/faith_creation_events.txt`；+840/-95 行；未作语义复核。
- M `religion_events/false_conversion_events.txt`；+47/-46 行；未作语义复核。
- D `religion_events/fervor_events.txt`；+0/-1938 行；未作语义复核。
- M `religion_events/great_holy_war_events.txt`；+219/-84 行；未作语义复核。
- A `religion_events/great_schism_events.txt`；+80/-0 行；未作语义复核。
- M `religion_events/head_of_faith_events.txt`；+286/-86 行；未作语义复核。
- M `religion_events/heresy_events.txt`；+1/-1355 行；未作语义复核。
- M `religion_events/holy_order_events.txt`；+3219/-72 行；未作语义复核。
- M `religion_events/human_sacrifice_events.txt`；+4/-3 行；未作语义复核。
- M `religion_events/jewish_events.txt`；+1/-1 行；未作语义复核。
- M `religion_events/local_shrine_events.txt`；+8/-13 行；未作语义复核。
- A `religion_events/natural_primitivism_events.txt`；+300/-0 行；未作语义复核。
- A `religion_events/petition_head_of_faith_events.txt`；+1820/-0 行；未作语义复核。
- M `religion_events/religious_decision_events.txt`；+205/-130 行；未作语义复核。
- M `religion_events/religious_interaction_events.txt`；+814/-90 行；未作语义复核。
- A `religion_events/rite_growth_events.txt`；+668/-0 行；未作语义复核。
- M `scheme_events/adbuct_scheme/abduct_outcome_events.txt`；+90/-6 行；未作语义复核。
- M `scheme_events/agent_events.txt`；+46/-41 行；未作语义复核。
- M `scheme_events/befriend_scheme/befriend_ongoing_dislike_events.txt`；+15/-15 行；未作语义复核。
- M `scheme_events/befriend_scheme/befriend_ongoing_events.txt`；+133/-132 行；未作语义复核。
- M `scheme_events/befriend_scheme/befriend_ongoing_rival_events.txt`；+1/-1 行；未作语义复核。
- M `scheme_events/befriend_scheme/befriend_scheme_outcome_events.txt`；+31/-11 行；未作语义复核。
- M `scheme_events/claim_throne_scheme/claim_throne_ongoing_events.txt`；+13/-10 行；未作语义复核。
- M `scheme_events/claim_throne_scheme/claim_throne_outcome_events.txt`；+9/-9 行；未作语义复核。
- M `scheme_events/court_scheme/court_scheme_ongoing_events.txt`；+45/-44 行；未作语义复核。
- M `scheme_events/court_scheme/court_scheme_outcome_events.txt`；+13/-7 行；未作语义复核。
- M `scheme_events/diplomatic_scheme_lifestyle_events.txt`；+4/-4 行；未作语义复核。
- M `scheme_events/elope_scheme/elope_scheme_events.txt`；+8/-8 行；未作语义复核。
- M `scheme_events/fabricate_hook_scheme/fabricate_hook_ongoing_events.txt`；+1/-1 行；未作语义复核。
- M `scheme_events/fabricate_hook_scheme/fabricate_hook_outcome_events.txt`；+40/-15 行；未作语义复核。
- M `scheme_events/governor_contract_events.txt`；+18/-9 行；未作语义复核。
- M `scheme_events/intrigue_scheme_lifestyle_events.txt`；+2/-2 行；未作语义复核。
- M `scheme_events/intrigue_scheme_ongoing_events.txt`；+51/-44 行；未作语义复核。
- M `scheme_events/laamp_base_contract_scheme_events.txt`；+328/-320 行；未作语义复核。
- M `scheme_events/laamp_base_learning_contract_events.txt`；+42/-26 行；未作语义复核。
- M `scheme_events/laamp_extra_contract_scheme_events.txt`；+10/-10 行；未作语义复核。
- M `scheme_events/learn_language_scheme/learn_language_ongoing_events.txt`；+55/-62 行；未作语义复核。
- M `scheme_events/learn_language_scheme/learn_language_outcome_events.txt`；+29/-9 行；未作语义复核。
- M `scheme_events/mandala_schemes/coerce_and_leverage_contribution_scheme_events.txt`；+11/-8 行；未作语义复核。
- M `scheme_events/mandala_schemes/coerce_tributary_scheme_events.txt`；+5/-5 行；未作语义复核。
- M `scheme_events/mandala_schemes/disbelieve_mandala_scheme_events.txt`；+6/-6 行；未作语义复核。
- M `scheme_events/murder_scheme/assassination_ongoing_events.txt`；+41/-44 行；未作语义复核。
- M `scheme_events/murder_scheme/murder_ongoing_events.txt`；+2/-2 行；未作语义复核。
- M `scheme_events/murder_scheme/murder_outcome_events.txt`；+10/-10 行；未作语义复核。
- M `scheme_events/murder_scheme/murder_outcome_reworked_events.txt`；+5/-3 行；未作语义复核。
- M `scheme_events/murder_scheme/murder_save_events.txt`；+5/-5 行；未作语义复核。
- M `scheme_events/murder_scheme/murder_scheme_maintenance_events.txt`；+6/-18 行；未作语义复核。
- M `scheme_events/personal_scheme_ongoing_events.txt`；+3/-3 行；未作语义复核。
- M `scheme_events/scheme_critical_moments_events.txt`；+155/-198 行；未作语义复核。
- M `scheme_events/seduce_scheme/seduce_ongoing_events.txt`；+17/-17 行；未作语义复核。
- M `scheme_events/seduce_scheme/seduce_scheme_outcome_events.txt`；+136/-50 行；未作语义复核。
- M `scheme_events/steal_back_artifact_scheme/steal_back_artifact_ongoing_events.txt`；+2/-2 行；未作语义复核。
- M `scheme_events/steal_herd_scheme/steal_herd_ongoing_events.txt`；+7/-5 行；未作语义复核。
- M `scheme_events/steal_herd_scheme/steal_herd_outcome_events.txt`；+3/-3 行；未作语义复核。
- M `scheme_events/study_confucian_classics_scheme/study_confucian_classics_events.txt`；+39/-39 行；未作语义复核。
- A `scheme_events/study_faith_scheme/study_faith_ongoing_events.txt`；+4300/-0 行；未作语义复核。
- A `scheme_events/study_faith_scheme/study_faith_outcome_events.txt`；+1384/-0 行；未作语义复核。
- A `scheme_events/study_scripture_scheme/study_scripture_events.txt`；+4190/-0 行；未作语义复核。
- M `scheme_events/sway_scheme/sway_ongoing_events.txt`；+43/-40 行；未作语义复核。
- M `scheme_events/sway_scheme/sway_outcome_events.txt`；+15/-8 行；未作语义复核。
- M `scheme_events/tgp_governor_contract_events_tova.txt`；+1/-0 行；未作语义复核。
- M `secret_events/secrets_events.txt`；+135/-76 行；未作语义复核。
- M `siege_events.txt`；+168/-28 行；未作语义复核。
- M `single_combat_events.txt`；+79/-77 行；未作语义复核。
- M `situation_events/mpo_the_great_steppe_events.txt`；+25/-3 行；未作语义复核。
- M `situation_events/tgp_natural_disaster_events.txt`；+8/-5 行；未作语义复核。
- M `story_cycles/ep3_story_cycle_el_cid.txt`；+15/-4 行；未作语义复核。
- M `story_cycles/ep3_story_cycle_hasan.txt`；+79/-58 行；未作语义复核。
- M `story_cycles/fp2_story_cycle_bell_of_huesca.txt`；+4/-8 行；未作语义复核。
- M `story_cycles/murders_at_court/story_cycle_murders_at_court_events.txt`；+23/-1 行；未作语义复核。
- A `story_cycles/pam_story_cycle_slavic_rite_events.txt`；+1236/-0 行；未作语义复核。
- M `story_cycles/peasant_affair/story_cycle_peasant_affair_events.txt`；+25/-22 行；未作语义复核。
- M `story_cycles/story_cycle_conqueror_events.txt`；+6/-1 行；未作语义复核。
- M `story_cycles/story_cycle_hunt_mystical_animal_events.txt`；+16/-6 行；未作语义复核。
- M `story_cycles/story_cycle_infidelity_confrontation_events.txt`；+19/-19 行；未作语义复核。
- M `story_cycles/story_cycle_mongol_invasion_events.txt`；+1/-0 行；未作语义复核。
- M `story_cycles/story_cycle_party_baron_events.txt`；+8/-8 行；未作语义复核。
- M `story_cycles/story_cycle_pet_animal_events.txt`；+87/-47 行；未作语义复核。
- M `story_cycles/story_cycle_tax_rivalry_events.txt`；+21/-23 行；未作语义复核。
- M `stress_events/stress_threshold_events.txt`；+607/-376 行；未作语义复核。
- M `stress_events/stress_threshold_prison_events.txt`；+25/-24 行；未作语义复核。
- M `stress_events/stress_threshold_special_events.txt`；+19/-14 行；未作语义复核。
- M `stress_events/stress_trait_coping_decisions_events.txt`；+90/-27 行；未作语义复核。
- M `stress_events/stress_trait_ongoing_events.txt`；+32/-34 行；未作语义复核。
- M `test_events/debug.txt`；+31/-32 行；未作语义复核。
- M `title_events.txt`；+75/-22 行；未作语义复核。
- M `trait_specific_events/trait_specific_events.txt`；+22/-16 行；未作语义复核。
- M `trait_specific_events/trait_specific_interaction_events.txt`；+6/-6 行；未作语义复核。
- M `trait_specific_events/trait_specific_ongoing_events.txt`；+68/-23 行；未作语义复核。
- M `travel_events/test_events.txt`；+2/-2 行；未作语义复核。
- M `travel_events/tgp_travel_events.txt`；+30/-30 行；未作语义复核。
- M `travel_events/travel_completion_events.txt`；+1/-10 行；未作语义复核。
- M `travel_events/travel_danger_events.txt`；+29/-17 行；未作语义复核。
- M `travel_events/travel_danger_events_ariana.txt`；+17/-17 行；未作语义复核。
- M `travel_events/travel_danger_events_arky.txt`；+12/-12 行；未作语义复核。
- M `travel_events/travel_danger_events_chad.txt`；+5/-5 行；未作语义复核。
- M `travel_events/travel_danger_events_dan.txt`；+5/-5 行；未作语义复核。
- M `travel_events/travel_danger_events_filippa.txt`；+17/-17 行；未作语义复核。
- M `travel_events/travel_danger_events_joe.txt`；+44/-30 行；未作语义复核。
- M `travel_events/travel_danger_events_klank.txt`；+36/-21 行；未作语义复核。
- M `travel_events/travel_danger_events_oltner.txt`；+6/-6 行；未作语义复核。
- M `travel_events/travel_events.txt`；+174/-154 行；未作语义复核。
- M `travel_events/travel_events_bjorn.txt`；+4/-4 行；未作语义复核。
- M `travel_events/travel_events_bp3.txt`；+133/-190 行；未作语义复核。
- M `travel_events/travel_events_cities.txt`；+41/-38 行；未作语义复核。
- M `travel_events/travel_events_cultural_traditions.txt`；+40/-35 行；未作语义复核。
- M `travel_events/travel_events_filippa.txt`；+1114/-297 行；未作语义复核。
- M `travel_events/travel_events_fp3.txt`；+61/-56 行；未作语义复核。
- M `travel_events/travel_events_james.txt`；+270/-290 行；未作语义复核。
- M `travel_events/travel_events_mpo.txt`；+11/-11 行；未作语义复核。
- M `travel_events/travel_events_oltner_2.txt`；+131/-181 行；未作语义复核。
- M `travel_events/travel_events_veronica.txt`；+142/-133 行；未作语义复核。
- M `travel_events/travel_start_events.txt`；+19/-10 行；未作语义复核。
- A `uprising_events/emelie_events.txt`；+328/-0 行；未作语义复核。
- M `varangian_events.txt`；+17/-37 行；未作语义复核。
- M `war_events/combat_events.txt`；+6/-9 行；未作语义复核。
- M `war_events/raid_events.txt`；+74/-28 行；未作语义复核。
- M `war_events/war_events.txt`；+4/-14 行；未作语义复核。
- M `witch_events.txt`；+173/-58 行；未作语义复核。
- M `yearly_events/bp1_yearly_james.txt`；+242/-272 行；未作语义复核。
- M `yearly_events/bp1_yearly_jason.txt`；+67/-143 行；未作语义复核。
- M `yearly_events/court_yearly_events.txt`；+136/-101 行；未作语义复核。
- M `yearly_events/yearly_events.txt`；+34/-32 行；未作语义复核。
- M `yearly_events/yearly_events_2.txt`；+102/-105 行；未作语义复核。
- M `yearly_events/yearly_events_3.txt`；+29/-23 行；未作语义复核。
- M `yearly_events/yearly_events_4.txt`；+25/-22 行；未作语义复核。
- M `yearly_events/yearly_events_5.txt`；+104/-110 行；未作语义复核。
- M `yearly_events/yearly_events_6.txt`；+19/-13 行；未作语义复核。
- M `yearly_events/yearly_events_7.txt`；+51/-53 行；未作语义复核。
- M `yearly_events/yearly_events_persia.txt`；+3/-3 行；未作语义复核。
- M `yearly_events/yearly_events_sahara.txt`；+28/-43 行；未作语义复核。

#### game/gui/（169 个变化路径）

- A `activity_planner_widgets/activity_planner_tenet_doctrine_selection.gui`；+593/-0 行；未作语义复核。
- M `activity_window_widgets/chariot_race_widget_types.gui`；+3/-3 行；未作语义复核。
- M `activity_window_widgets/coronation_supporter_detractor_widget.gui`；+279/-9 行；未作语义复核。
- M `activity_window_widgets/coronation_widget_types.gui`；+4/-2 行；未作语义复核。
- M `activity_window_widgets/imperial_examination_widget_types.gui`；+4/-4 行；未作语义复核。
- M `activity_window_widgets/tournament_contest_information.gui`；+1/-1 行；未作语义复核。
- M `activity_window_widgets/tournament_contest_selection.gui`；+1/-1 行；未作语义复核。
- M `activity_window_widgets/tournament_widget_types.gui`；+3/-3 行；未作语义复核。
- M `debug/placeholder_types_templates.gui`；+315/-329 行；未作语义复核。
- M `debug/window_component_library.gui`；+1/-1 行；未作语义复核。
- A `decision_view_widgets/decision_view_generic_title_selector_widget.gui`；+58/-0 行；未作语义复核。
- M `decision_view_widgets/decision_view_widget_create_holy_order.gui`；+12/-12 行；未作语义复核。
- A `decision_view_widgets/decision_view_widget_petition_head_of_faith.gui`；+84/-0 行；未作语义复核。
- A `decision_view_widgets/decision_view_widget_select_artifact.gui`；+76/-0 行；未作语义复核。
- A `decision_view_widgets/decision_view_widget_select_character.gui`；+68/-0 行；未作语义复核。
- A `decision_view_widgets/decision_view_widget_select_holy_site.gui`；+73/-0 行；未作语义复核。
- A `decision_view_widgets/decision_view_widget_select_realm_county.gui`；+73/-0 行；未作语义复核。
- A `decision_view_widgets/decision_view_widget_select_rite.gui`；+67/-0 行；未作语义复核。
- A `decision_view_widgets/decision_view_widget_select_tenet.gui`；+68/-0 行；未作语义复核。
- A `decision_view_widgets/decision_view_widget_select_title.gui`；+6/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_name_pope.gui`；+85/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_rite.gui`；+69/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_rite_founder.gui`；+8/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_rite_new_pope.gui`；+8/-0 行；未作语义复核。
- M `event_window_widgets/event_window_widget_situation_info.gui`；+1/-1 行；未作语义复核。
- A `event_window_widgets/event_window_widget_situation_info_christian_church.gui`；+196/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_vfx_background_double_vision_milder.gui`；+13/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_vfx_background_double_vision_severe.gui`；+13/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_vfx_background_flickering_candlelight.gui`；+13/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_vfx_background_flickering_candlelight_dark.gui`；+13/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_vfx_background_night_scene.gui`；+12/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_vfx_left_character_double_vision_milder.gui`；+15/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_vfx_left_character_double_vision_severe.gui`；+15/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_vfx_left_character_flickering_candlelight.gui`；+15/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_vfx_left_character_flickering_candlelight_dark.gui`；+15/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_vfx_left_character_night_scene.gui`；+15/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_vfx_right_character_double_vision_milder.gui`；+15/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_vfx_right_character_double_vision_severe.gui`；+15/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_vfx_right_character_flickering_candlelight.gui`；+15/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_vfx_right_character_flickering_candlelight_dark.gui`；+15/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_vfx_right_character_night_scene.gui`；+15/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_vfx_stained_glass.gui`；+9/-0 行；未作语义复核。
- A `event_window_widgets/event_window_widget_vfx_stained_glass_foreground.gui`；+9/-0 行；未作语义复核。
- M `event_windows/anonymous_letter_event.gui`；+1/-25 行；未作语义复核。
- M `event_windows/big_event_window.gui`；+292/-302 行；未作语义复核。
- M `event_windows/character_event.gui`；+12/-5 行；未作语义复核。
- M `event_windows/duel_event.gui`；+4/-4 行；未作语义复核。
- M `event_windows/fullscreen_event.gui`；+164/-15 行；未作语义复核。
- M `event_windows/letter_event.gui`；+1/-25 行；未作语义复核。
- M `event_windows/scheme_conclusion_event_no_header.gui`；+1/-0 行；未作语义复核。
- M `event_windows/scheme_preparations_event.gui`；+4/-25 行；未作语义复核。
- M `frontend_bookmarks.gui`；+44/-4 行；未作语义复核。
- M `frontend_ingame_menu.gui`；+5/-0 行；未作语义复核。
- M `frontend_load.gui`；+32/-11 行；未作语义复核。
- M `frontend_main.gui`；+1/-0 行；未作语义复核。
- M `hud.gui`；+947/-443 行；未作语义复核。
- M `hud_bottom.gui`；+28/-390 行；未作语义复核。
- M `hud_notification_templates.gui`；+109/-1 行；未作语义复核。
- M `interaction_concubine.gui`；+1/-1 行；未作语义复核。
- M `interaction_confirmation.gui`；+120/-20 行；未作语义复核。
- M `interaction_council_task.gui`；+1/-1 行；未作语义复核。
- M `interaction_court_task.gui`；+2/-2 行；未作语义复核。
- M `interaction_create_claimant_faction.gui`；+4/-4 行；未作语义复核。
- M `interaction_declare_war.gui`；+105/-77 行；未作语义复核。
- M `interaction_grant_titles.gui`；+48/-3 行；未作语义复核。
- M `interaction_marriage.gui`；+1/-1 行；未作语义复核。
- M `interaction_menu_window.gui`；+426/-179 行；未作语义复核。
- M `interaction_revoke_title.gui`；+13/-2 行；未作语义复核。
- M `interaction_templates.gui`；+128/-81 行；未作语义复核。
- M `map_icon_layer.gui`；+518/-35 行；未作语义复核。
- M `multiplayer_lobby.gui`；+18/-16 行；未作语义复核。
- M `pdx_account/login_window.gui`；+1/-1 行；未作语义复核。
- M `preload/defaults.gui`；+11/-0 行；未作语义复核。
- M `shared/animation.gui`；+11/-0 行；未作语义复核。
- M `shared/buttons.gui`；+1836/-1498 行；未作语义复核。
- M `shared/coat_of_arms.gui`；+251/-103 行；未作语义复核。
- M `shared/cooltip.gui`；+1018/-144 行；未作语义复核。
- M `shared/event_windows.gui`；+173/-35 行；未作语义复核。
- M `shared/icons.gui`；+10/-32 行；未作语义复核。
- M `shared/lists.gui`；+70/-19 行；未作语义复核。
- M `shared/mapmodes.gui`；+343/-53 行；未作语义复核。
- M `shared/misc_components.gui`；+337/-2 行；未作语义复核。
- M `shared/portraits.gui`；+180/-11 行；未作语义复核。
- M `shared/progressbars.gui`；+119/-18 行；未作语义复核。
- M `shared/sounds.gui`；+338/-237 行；未作语义复核。
- A `shared/succession_election_widgets.gui`；+212/-0 行；未作语义复核。
- M `shared/texticons_religion.gui`；+245/-164 行；未作语义复核。
- M `shared/value_breakdown.gui`；+173/-11 行；未作语义复核。
- A `shared/vertical_progressbars.gui`；+452/-0 行；未作语义复核。
- M `shortcuts.shortcuts`；+15/-1 行；未作语义复核。
- M `texticons.gui`；+260/-15 行；未作语义复核。
- M `texticons_religion.gui`；+20/-0 行；未作语义复核。
- M `window_accolade.gui`；+33/-0 行；未作语义复核。
- M `window_activity.gui`；+68/-4 行；未作语义复核。
- M `window_activity_guest_list.gui`；+4/-1 行；未作语义复核。
- M `window_activity_list.gui`；+80/-77 行；未作语义复核。
- M `window_activity_planner.gui`；+217/-13 行；未作语义复核。
- M `window_admin_vassal_detail.gui`；+252/-122 行；未作语义复核。
- M `window_appoint_tax_collector.gui`；+1/-1 行；未作语义复核。
- M `window_army.gui`；+1/-1 行；未作语义复核。
- M `window_army_select_commander.gui`；+2/-2 行；未作语义复核。
- M `window_artifact_details.gui`；+41/-10 行；未作语义复核。
- M `window_barbershop.gui`；+2/-2 行；未作语义复核。
- M `window_battle_summary.gui`；+2/-2 行；未作语义复核。
- A `window_cardinals.gui`；+918/-0 行；未作语义复核。
- M `window_character.gui`；+533/-384 行；未作语义复核。
- M `window_character_filter.gui`；+31/-1 行；未作语义复核。
- M `window_character_lifestyle.gui`；+5/-5 行；未作语义复核。
- M `window_confederation.gui`；+2/-2 行；未作语义复核。
- M `window_council.gui`；+37/-23 行；未作语义复核。
- M `window_county_view.gui`；+36/-29 行；未作语义复核。
- M `window_court_positions.gui`；+0/-1 行；未作语义复核。
- M `window_culture.gui`；+6/-6 行；未作语义复核。
- M `window_decisions.gui`；+68/-7 行；未作语义复核。
- M `window_decisions_detail.gui`；+10/-9 行；未作语义复核。
- M `window_diverge_culture.gui`；+1/-1 行；未作语义复核。
- M `window_domicile.gui`；+25/-4 行；未作语义复核。
- M `window_dynasty_legacy.gui`；+1/-1 行；未作语义复核。
- M `window_dynasty_tree.gui`；+9/-0 行；未作语义复核。
- M `window_factions.gui`；+1/-1 行；未作语义复核。
- M `window_faith.gui`；+5662/-1104 行；未作语义复核。
- M `window_faith_conversion.gui`；+62/-29 行；未作语义复核。
- D `window_faith_creation.gui`；+0/-1449 行；未作语义复核。
- M `window_find_title.gui`；+1/-1 行；未作语义复核。
- M `window_find_vassal.gui`；+2/-2 行；未作语义复核。
- A `window_geographical_regions.gui`；+140/-0 行；未作语义复核。
- M `window_government_administration.gui`；+30/-22 行；未作语义复核。
- M `window_great_project.gui`；+9/-7 行；未作语义复核。
- M `window_hired_troops_detail.gui`；+205/-198 行；未作语义复核。
- A `window_holy_site.gui`；+1278/-0 行；未作语义复核。
- A `window_holy_site_creation.gui`；+900/-0 行；未作语义复核。
- M `window_hybridize_culture.gui`；+13/-1 行；未作语义复核。
- M `window_intrigue.gui`；+1801/-924 行；未作语义复核。
- M `window_inventory.gui`；+95/-20 行；未作语义复核。
- M `window_knights.gui`；+134/-133 行；未作语义复核。
- M `window_lease_out_baronies.gui`；+1/-1 行；未作语义复核。
- M `window_ledger.gui`；+735/-126 行；未作语义复核。
- M `window_manage_tax_slots.gui`；+1/-1 行；未作语义复核。
- M `window_message_popup.gui`；+50/-0 行；未作语义复核。
- M `window_message_settings.gui`；+100/-0 行；未作语义复核。
- M `window_military.gui`；+284/-236 行；未作语义复核。
- M `window_my_realm.gui`；+124/-125 行；未作语义复核。
- A `window_organization.gui`；+119/-0 行；未作语义复核。
- A `window_pam_christian_church.gui`；+2408/-0 行；未作语义复核。
- A `window_personal_beliefs.gui`；+1134/-0 行；未作语义复核。
- M `window_plan_great_project.gui`；+77/-54 行；未作语义复核。
- A `window_puppet_selection.gui`；+177/-0 行；未作语义复核。
- M `window_replace_pillar.gui`；+4/-4 行；未作语义复核。
- A `window_rite_creation.gui`；+1862/-0 行；未作语义复核。
- M `window_ruler_designer.gui`；+332/-139 行；未作语义复核。
- M `window_ruler_designer_load.gui`；+5/-4 行；未作语义复核。
- M `window_silk_road.gui`；+1/-1 行；未作语义复核。
- M `window_situation.gui`；+3/-3 行；未作语义复核。
- M `window_situation_list.gui`；+1/-1 行；未作语义复核。
- M `window_situation_participation.gui`；+1/-1 行；未作语义复核。
- M `window_situation_participation_debug.gui`；+1/-1 行；未作语义复核。
- M `window_struggle_involvement.gui`；+1/-1 行；未作语义复核。
- M `window_succession_event.gui`；+25/-3 行；未作语义复核。
- M `window_tax_slot_vassals.gui`；+4/-2 行；未作语义复核。
- M `window_tgp_dynastic_cycle.gui`；+56/-54 行；未作语义复核。
- M `window_the_great_steppe.gui`；+3/-7 行；未作语义复核。
- M `window_title.gui`；+1572/-344 行；未作语义复核。
- M `window_title_appointment.gui`；+257/-141 行；未作语义复核。
- M `window_title_claimants.gui`；+1/-1 行；未作语义复核。
- M `window_title_election.gui`；+33/-192 行；未作语义复核。
- M `window_title_history.gui`；+1/-1 行；未作语义复核。
- A `window_title_selector.gui`；+99/-0 行；未作语义复核。
- M `window_treasury_budget_change.gui`；+11/-0 行；未作语义复核。
- M `window_war_overview.gui`；+35/-1 行；未作语义复核。

#### game/history/（472 个变化路径）

- M `_characters.info`；+40/-0 行；未作语义复核。
- M `_provinces.info`；+30/-25 行；未作语义复核。
- M `characters/afar.txt`；+22/-22 行；未作语义复核。
- M `characters/afghan.txt`；+52/-52 行；未作语义复核。
- M `characters/ainu.txt`；+108/-108 行；未作语义复核。
- M `characters/akan.txt`；+84/-84 行；未作语义复核。
- M `characters/alan.txt`；+124/-91 行；未作语义复核。
- M `characters/albanian.txt`；+1/-1 行；未作语义复核。
- M `characters/amis.txt`；+36/-36 行；未作语义复核。
- M `characters/andalusian.txt`；+363/-366 行；未作语义复核。
- M `characters/anglo_saxon.txt`；+836/-447 行；未作语义复核。
- M `characters/aragonese.txt`；+83/-44 行；未作语义复核。
- M `characters/armenian.txt`；+707/-644 行；未作语义复核。
- M `characters/assamese.txt`；+79/-79 行；未作语义复核。
- M `characters/asturleonese.txt`；+1361/-752 行；未作语义复核。
- M `characters/avar.txt`；+54/-54 行；未作语义复核。
- M `characters/bai.txt`；+140/-140 行；未作语义复核。
- M `characters/balhae.txt`；+152/-152 行；未作语义复核。
- M `characters/baloch.txt`；+19/-19 行；未作语义复核。
- M `characters/bashkir.txt`；+42/-42 行；未作语义复核。
- M `characters/basque.txt`；+719/-556 行；未作语义复核。
- M `characters/bavarian.txt`；+2185/-889 行；未作语义复核。
- M `characters/bavlim.txt`；+14/-14 行；未作语义复核。
- M `characters/bedouin.txt`；+1068/-1053 行；未作语义复核。
- M `characters/beja.txt`；+83/-83 行；未作语义复核。
- M `characters/bengali.txt`；+280/-277 行；未作语义复核。
- M `characters/berber.txt`；+686/-638 行；未作语义复核。
- M `characters/bobo.txt`；+91/-91 行；未作语义复核。
- M `characters/bodpa.txt`；+1572/-1566 行；未作语义复核。
- M `characters/bolghar.txt`；+163/-163 行；未作语义复核。
- M `characters/bosnian.txt`；+28/-28 行；未作语义复核。
- M `characters/bouxcuengh.txt`；+7/-7 行；未作语义复核。
- M `characters/bozo.txt`；+31/-31 行；未作语义复核。
- M `characters/breton.txt`；+504/-343 行；未作语义复核。
- M `characters/bugis.txt`；+42/-42 行；未作语义复核。
- M `characters/bulgarian.txt`；+165/-122 行；未作语义复核。
- M `characters/burmese.txt`；+117/-117 行；未作语义复核。
- M `characters/buryat.txt`；+123/-123 行；未作语义复核。
- M `characters/butr.txt`；+250/-250 行；未作语义复核。
- M `characters/carantanian.txt`；+1/-1 行；未作语义复核。
- M `characters/castilian.txt`；+1692/-1314 行；未作语义复核。
- M `characters/catalan.txt`；+1296/-880 行；未作语义复核。
- M `characters/cham.txt`；+69/-69 行；未作语义复核。
- M `characters/cisalpine.txt`；+3330/-2065 行；未作语义复核。
- M `characters/croatian.txt`；+208/-160 行；未作语义复核。
- M `characters/cuman.txt`；+306/-303 行；未作语义复核。
- M `characters/cumbrian.txt`；+61/-57 行；未作语义复核。
- M `characters/czech.txt`；+270/-203 行；未作语义复核。
- M `characters/daju.txt`；+30/-30 行；未作语义复核。
- M `characters/danish.txt`；+282/-191 行；未作语义复核。
- M `characters/dayak.txt`；+141/-141 行；未作语义复核。
- M `characters/daylamite.txt`；+152/-145 行；未作语义复核。
- M `characters/dutch.txt`；+637/-507 行；未作语义复核。
- M `characters/east_bantu.txt`；+17/-17 行；未作语义复核。
- M `characters/easteregg_non_developers.txt`；+46/-8 行；未作语义复核。
- M `characters/eastereggs.txt`；+993/-162 行；未作语义复核。
- A `characters/ecclesiastical.txt`；+15266/-0 行；未作语义复核。
- M `characters/edo.txt`；+18/-18 行；未作语义复核。
- M `characters/egyptian.txt`；+222/-125 行；未作语义复核。
- M `characters/emishi.txt`；+9/-9 行；未作语义复核。
- M `characters/english.txt`；+818/-754 行；未作语义复核。
- M `characters/estonian.txt`；+34/-34 行；未作语义复核。
- M `characters/ethiopian.txt`；+246/-212 行；未作语义复核。
- M `characters/ewe.txt`；+30/-30 行；未作语义复核。
- M `characters/filipino.txt`；+84/-84 行；未作语义复核。
- M `characters/finnish.txt`；+81/-81 行；未作语义复核。
- M `characters/franconian.txt`；+4551/-1896 行；未作语义复核。
- M `characters/frankish.txt`；+347/-320 行；未作语义复核。
- M `characters/french.txt`；+4094/-3043 行；未作语义复核。
- M `characters/frisian.txt`；+29/-26 行；未作语义复核。
- M `characters/gaelic.txt`；+212/-138 行；未作语义复核。
- M `characters/galician.txt`；+1335/-809 行；未作语义复核。
- M `characters/georgian.txt`；+333/-206 行；未作语义复核。
- M `characters/german.txt`；+44/-44 行；未作语义复核。
- M `characters/greek.txt`；+2765/-1873 行；未作语义复核。
- M `characters/guan.txt`；+43/-43 行；未作语义复核。
- M `characters/gujarati.txt`；+82/-82 行；未作语义复核。
- M `characters/gur.txt`；+97/-97 行；未作语义复核。
- M `characters/han.txt`；+14304/-14295 行；未作语义复核。
- M `characters/hausa.txt`；+113/-115 行；未作语义复核。
- M `characters/hindustani.txt`；+208/-208 行；未作语义复核。
- M `characters/hmong.txt`；+40/-40 行；未作语义复核。
- M `characters/hungarian.txt`；+846/-556 行；未作语义复核。
- M `characters/igbo.txt`；+37/-37 行；未作语义复核。
- M `characters/irish.txt`；+1483/-1358 行；未作语义复核。
- M `characters/italian.txt`；+3161/-2398 行；未作语义复核。
- M `characters/japanese.txt`；+6943/-6903 行；未作语义复核。
- M `characters/javanese.txt`；+159/-149 行；未作语义复核。
- M `characters/jurchen.txt`；+200/-200 行；未作语义复核。
- M `characters/kannada.txt`；+366/-366 行；未作语义复核。
- M `characters/kanuri.txt`；+51/-51 行；未作语义复核。
- M `characters/karelian.txt`；+21/-21 行；未作语义复核。
- M `characters/karluk.txt`；+276/-272 行；未作语义复核。
- M `characters/kashmiri.txt`；+91/-91 行；未作语义复核。
- M `characters/kerait.txt`；+49/-49 行；未作语义复核。
- M `characters/khanty.txt`；+199/-199 行；未作语义复核。
- M `characters/khazar.txt`；+90/-90 行；未作语义复核。
- M `characters/khitan.txt`；+264/-264 行；未作语义复核。
- M `characters/khmer.txt`；+126/-122 行；未作语义复核。
- M `characters/khwarezmian.txt`；+34/-34 行；未作语义复核。
- M `characters/kimek.txt`；+116/-116 行；未作语义复核。
- M `characters/kipchak.txt`；+84/-84 行；未作语义复核。
- M `characters/kirati.txt`；+81/-81 行；未作语义复核。
- M `characters/kirghiz.txt`；+143/-143 行；未作语义复核。
- M `characters/komi.txt`；+42/-42 行；未作语义复核。
- M `characters/korean.txt`；+1269/-1270 行；未作语义复核。
- M `characters/kru.txt`；+100/-100 行；未作语义复核。
- M `characters/kurdish.txt`；+132/-132 行；未作语义复核。
- M `characters/laktan.txt`；+27/-27 行；未作语义复核。
- M `characters/latgalian.txt`；+26/-26 行；未作语义复核。
- M `characters/levantine.txt`；+1109/-923 行；未作语义复核。
- M `characters/lhomon.txt`；+153/-153 行；未作语义复核。
- M `characters/lithuanian.txt`；+187/-186 行；未作语义复核。
- M `characters/lombard.txt`；+1061/-624 行；未作语义复核。
- M `characters/maghrebi.txt`；+59/-43 行；未作语义复核。
- M `characters/malay.txt`；+122/-115 行；未作语义复核。
- M `characters/malinke.txt`；+152/-152 行；未作语义复核。
- M `characters/maluku.txt`；+134/-134 行；未作语义复核。
- M `characters/marathi.txt`；+184/-184 行；未作语义复核。
- M `characters/mari.txt`；+15/-15 行；未作语义复核。
- M `characters/marka.txt`；+25/-25 行；未作语义复核。
- M `characters/mel.txt`；+91/-91 行；未作语义复核。
- M `characters/merya.txt`；+8/-8 行；未作语义复核。
- M `characters/meshchera.txt`；+24/-21 行；未作语义复核。
- M `characters/mohe.txt`；+130/-130 行；未作语义复核。
- M `characters/mon.txt`；+133/-133 行；未作语义复核。
- M `characters/mongol.txt`；+641/-640 行；未作语义复核。
- M `characters/mordvin.txt`；+42/-42 行；未作语义复核。
- M `characters/mossi.txt`；+24/-24 行；未作语义复核。
- M `characters/muroma.txt`；+13/-13 行；未作语义复核。
- M `characters/naiman.txt`；+42/-42 行；未作语义复核。
- M `characters/nepali.txt`；+358/-358 行；未作语义复核。
- M `characters/nivkh.txt`；+40/-40 行；未作语义复核。
- M `characters/norman.txt`；+1036/-536 行；未作语义复核。
- M `characters/norse.txt`；+493/-414 行；未作语义复核。
- M `characters/norwegian.txt`；+419/-263 行；未作语义复核。
- M `characters/nubian.txt`；+141/-141 行；未作语义复核。
- M `characters/nupe.txt`；+64/-64 行；未作语义复核。
- M `characters/occitan.txt`；+1961/-1518 行；未作语义复核。
- M `characters/oirat.txt`；+20/-20 行；未作语义复核。
- M `characters/old_saxon.txt`；+24/-24 行；未作语义复核。
- M `characters/ongud.txt`；+31/-31 行；未作语义复核。
- M `characters/oriya.txt`；+251/-251 行；未作语义复核。
- M `characters/papuan.txt`；+12/-12 行；未作语义复核。
- M `characters/pecheneg.txt`；+115/-115 行；未作语义复核。
- M `characters/persian.txt`；+606/-589 行；未作语义复核。
- M `characters/pictish.txt`；+107/-107 行；未作语义复核。
- M `characters/polabian.txt`；+92/-86 行；未作语义复核。
- M `characters/polish.txt`；+634/-462 行；未作语义复核。
- M `characters/pommeranian.txt`；+121/-118 行；未作语义复核。
- M `characters/portrait_debug_characters.txt`；+13/-13 行；未作语义复核。
- M `characters/portuguese.txt`；+1302/-1083 行；未作语义复核。
- M `characters/prussian.txt`；+22/-22 行；未作语义复核。
- M `characters/punjabi.txt`；+208/-208 行；未作语义复核。
- M `characters/qiang.txt`；+30/-30 行；未作语义复核。
- M `characters/rajput.txt`；+764/-763 行；未作语义复核。
- M `characters/roman.txt`；+341/-193 行；未作语义复核。
- M `characters/romanian.txt`；+185/-134 行；未作语义复核。
- M `characters/russian.txt`；+1220/-863 行；未作语义复核。
- M `characters/ryukyuan.txt`；+30/-30 行；未作语义复核。
- A `characters/saints.txt`；+675/-0 行；未作语义复核。
- M `characters/saka.txt`；+124/-124 行；未作语义复核。
- M `characters/sami.txt`；+84/-84 行；未作语义复核。
- M `characters/samoyed.txt`；+39/-39 行；未作语义复核。
- M `characters/sao.txt`；+95/-95 行；未作语义复核。
- M `characters/sardinian.txt`；+310/-205 行；未作语义复核。
- M `characters/saxon.txt`；+3471/-1266 行；未作语义复核。
- M `characters/scottish.txt`；+779/-738 行；未作语义复核。
- M `characters/sephardi.txt`；+102/-23 行；未作语义复核。
- M `characters/serbian.txt`；+207/-156 行；未作语义复核。
- M `characters/shatuo.txt`；+26/-26 行；未作语义复核。
- M `characters/shiwei.txt`；+128/-128 行；未作语义复核。
- M `characters/sicilian.txt`；+179/-163 行；未作语义复核。
- M `characters/sindhi.txt`；+47/-47 行；未作语义复核。
- M `characters/sinhala.txt`；+87/-87 行；未作语义复核。
- M `characters/slovien.txt`；+61/-58 行；未作语义复核。
- M `characters/sogdian.txt`；+111/-111 行；未作语义复核。
- M `characters/somali.txt`；+175/-175 行；未作语义复核。
- M `characters/songhai.txt`；+40/-40 行；未作语义复核。
- M `characters/soninke.txt`；+108/-108 行；未作语义复核。
- M `characters/sorko.txt`；+30/-30 行；未作语义复核。
- M `characters/suebi.txt`；+1/-1 行；未作语义复核。
- M `characters/sumpa.txt`；+256/-256 行；未作语义复核。
- M `characters/swabian.txt`；+1930/-767 行；未作语义复核。
- M `characters/swahili.txt`；+77/-77 行；未作语义复核。
- M `characters/swedish.txt`；+651/-455 行；未作语义复核。
- M `characters/tai.txt`；+62/-62 行；未作语义复核。
- M `characters/tajik.txt`；+164/-162 行；未作语义复核。
- M `characters/tamil.txt`；+138/-138 行；未作语义复核。
- M `characters/tangut.txt`；+344/-332 行；未作语义复核。
- M `characters/telugu.txt`；+153/-153 行；未作语义复核。
- M `characters/tocharian.txt`；+57/-57 行；未作语义复核。
- M `characters/toraja.txt`；+20/-20 行；未作语义复核。
- M `characters/tsangpa.txt`；+174/-174 行；未作语义复核。
- M `characters/turkish.txt`；+913/-865 行；未作语义复核。
- M `characters/tuyuhun.txt`；+157/-157 行；未作语义复核。
- M `characters/uriankhai.txt`；+57/-57 行；未作语义复核。
- M `characters/uyghur.txt`；+277/-268 行；未作语义复核。
- M `characters/vepsian.txt`；+29/-29 行；未作语义复核。
- M `characters/viet.txt`；+119/-119 行；未作语义复核。
- M `characters/visigothic.txt`；+144/-144 行；未作语义复核。
- M `characters/welayta.txt`；+90/-90 行；未作语义复核。
- M `characters/welsh.txt`；+809/-561 行；未作语义复核。
- M `characters/wolof.txt`；+101/-101 行；未作语义复核。
- M `characters/yemeni.txt`；+146/-146 行；未作语义复核。
- M `characters/yi.txt`；+14/-14 行；未作语义复核。
- M `characters/yoruba.txt`；+45/-45 行；未作语义复核。
- M `characters/yughur.txt`；+62/-62 行；未作语义复核。
- M `characters/zaghawa.txt`；+79/-79 行；未作语义复核。
- M `characters/zhangzhung.txt`；+266/-256 行；未作语义复核。
- A `cultures/bouxcuengh.txt`；+44/-0 行；未作语义复核。
- M `cultures/heritage_chinese.txt`；+25/-45 行；未作语义复核。
- M `cultures/heritage_hmongic.txt`；+21/-35 行；未作语义复核。
- M `cultures/heritage_mongolic.txt`；+1/-2 行；未作语义复核。
- M `cultures/heritage_qiangic.txt`；+7/-23 行；未作语义复核。
- M `cultures/heritage_tai.txt`；+12/-23 行；未作语义复核。
- M `cultures/heritage_tungusic.txt`；+4/-2 行；未作语义复核。
- M `cultures/heritage_turkic.txt`；+2/-2 行；未作语义复核。
- A `cultures/jurchen.txt`；+61/-0 行；未作语义复核。
- A `cultures/kachin.txt`；+18/-0 行；未作语义复核。
- A `cultures/khitan.txt`；+55/-0 行；未作语义复核。
- A `cultures/ongud.txt`；+55/-0 行；未作语义复核。
- M `cultures/ryukyuan.txt`；+6/-46 行；未作语义复核。
- A `cultures/shatuo.txt`；+54/-0 行；未作语义复核。
- M `cultures/tangut.txt`；+2/-0 行；未作语义复核。
- A `cultures/tuyuhun.txt`；+38/-0 行；未作语义复核。
- M `cultures/uyghur.txt`；+29/-9 行；未作语义复核。
- A `cultures/yughur.txt`；+55/-0 行；未作语义复核。
- A `faiths/00_abrahimic.txt`；+75/-0 行；未作语义复核。
- A `faiths/00_biliku.txt`；+18/-0 行；未作语义复核。
- A `faiths/00_buddhism.txt`；+81/-0 行；未作语义复核。
- A `faiths/00_christianity.txt`；+634/-0 行；未作语义复核。
- A `faiths/00_dualism.txt`；+45/-0 行；未作语义复核。
- A `faiths/00_eastern_misc.txt`；+46/-0 行；未作语义复核。
- A `faiths/00_hinduism.txt`；+73/-0 行；未作语义复核。
- A `faiths/00_islam.txt`；+113/-0 行；未作语义复核。
- A `faiths/00_mundhum.txt`；+20/-0 行；未作语义复核。
- A `faiths/00_pagan.txt`；+327/-0 行；未作语义复核。
- A `faiths/00_qiangic.txt`；+21/-0 行；未作语义复核。
- A `faiths/00_tani.txt`；+21/-0 行；未作语义复核。
- A `faiths/00_taoism.txt`；+40/-0 行；未作语义复核。
- A `faiths/00_waaqism.txt`；+17/-0 行；未作语义复核。
- A `faiths/00_west_african.txt`；+17/-0 行；未作语义复核。
- A `faiths/00_zoroastrianism.txt`；+97/-0 行；未作语义复核。
- A `faiths/_faith_history.info`；+91/-0 行；未作语义复核。
- M `provinces/e_japan.txt`；+86/-86 行；未作语义复核。
- M `provinces/e_kambuja.txt`；+40/-40 行；未作语义复核。
- M `provinces/h_china.txt`；+963/-844 行；未作语义复核。
- M `provinces/k_abyssinia.txt`；+31/-28 行；未作语义复核。
- M `provinces/k_adal.txt`；+23/-23 行；未作语义复核。
- M `provinces/k_africa.txt`；+59/-56 行；未作语义复核。
- M `provinces/k_ajuraan.txt`；+28/-28 行；未作语义复核。
- M `provinces/k_akan.txt`；+2/-2 行；未作语义复核。
- M `provinces/k_amdo.txt`；+376/-365 行；未作语义复核。
- M `provinces/k_amur.txt`；+23/-26 行；未作语义复核。
- M `provinces/k_anatolia.txt`；+587/-416 行；未作语义复核。
- M `provinces/k_anbiya.txt`；+72/-72 行；未作语义复核。
- M `provinces/k_andalusia.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_andhra.txt`；+67/-72 行；未作语义复核。
- M `provinces/k_angara.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_aquitaine.txt`；+199/-87 行；未作语义复核。
- M `provinces/k_arabia.txt`；+43/-43 行；未作语义复核。
- M `provinces/k_aragon.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_armenia.txt`；+89/-79 行；未作语义复核。
- M `provinces/k_badajoz.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_bale.txt`；+11/-11 行；未作语义复核。
- M `provinces/k_balhae.txt`；+143/-105 行；未作语义复核。
- M `provinces/k_bashkiria.txt`；+37/-37 行；未作语义复核。
- M `provinces/k_bavaria.txt`；+217/-87 行；未作语义复核。
- M `provinces/k_bengal.txt`；+66/-66 行；未作语义复核。
- M `provinces/k_bihar.txt`；+52/-52 行；未作语义复核。
- M `provinces/k_bjarmaland.txt`；+15/-15 行；未作语义复核。
- M `provinces/k_blemmyia.txt`；+39/-39 行；未作语义复核。
- M `provinces/k_bohemia.txt`；+97/-51 行；未作语义复核。
- M `provinces/k_borgu.txt`；+6/-6 行；未作语义复核。
- M `provinces/k_borneo.txt`；+29/-29 行；未作语义复核。
- M `provinces/k_brittany.txt`；+32/-8 行；未作语义复核。
- M `provinces/k_bulgaria.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_burgundy.txt`；+103/-38 行；未作语义复核。
- M `provinces/k_buryatia.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_caspian_steppe.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_castille.txt`；+53/-15 行；未作语义复核。
- M `provinces/k_caucasus.txt`；+58/-42 行；未作语义复核。
- M `provinces/k_croatia.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_cuman.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_cyprus.txt`；+24/-12 行；未作语义复核。
- M `provinces/k_dacia.txt`；+128/-92 行；未作语义复核。
- M `provinces/k_dali.txt`；+25/-25 行；未作语义复核。
- M `provinces/k_damot.txt`；+14/-14 行；未作语义复核。
- M `provinces/k_darfur.txt`；+193/-193 行；未作语义复核。
- M `provinces/k_daylam.txt`；+58/-58 行；未作语义复核。
- M `provinces/k_delhi.txt`；+46/-47 行；未作语义复核。
- M `provinces/k_denmark.txt`；+102/-63 行；未作语义复核。
- M `provinces/k_dvaravati.txt`；+27/-27 行；未作语义复核。
- M `provinces/k_dzungaria.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_east_francia.txt`；文本未解码；行数未计算；已复核关键定义/差异。
- M `provinces/k_egypt.txt`；+43/-43 行；未作语义复核。
- M `provinces/k_england.txt`；+223/-79 行；未作语义复核。
- M `provinces/k_epirus.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_esthonia.txt`；+85/-85 行；未作语义复核。
- M `provinces/k_finland.txt`；+212/-213 行；未作语义复核。
- M `provinces/k_france.txt`；+256/-94 行；未作语义复核。
- M `provinces/k_frisia.txt`；+60/-27 行；未作语义复核。
- M `provinces/k_galicia-volhynia.txt`；+104/-68 行；未作语义复核。
- M `provinces/k_georgia.txt`；+309/-222 行；未作语义复核。
- M `provinces/k_ghana.txt`；+197/-197 行；未作语义复核。
- M `provinces/k_gobi.txt`；+18/-18 行；未作语义复核。
- M `provinces/k_gondwana.txt`；+34/-34 行；未作语义复核。
- M `provinces/k_goryeo.txt`；+91/-82 行；未作语义复核。
- M `provinces/k_guge.txt`；+269/-258 行；未作语义复核。
- M `provinces/k_guinea.txt`；+4/-4 行；未作语义复核。
- M `provinces/k_gujarat.txt`；+51/-52 行；未作语义复核。
- M `provinces/k_gur.txt`；+3/-3 行；未作语义复核。
- M `provinces/k_gurma.txt`；+99/-99 行；未作语义复核。
- M `provinces/k_gyalrong.txt`；+298/-283 行；未作语义复核。
- M `provinces/k_hausaland.txt`；+31/-31 行；未作语义复核。
- M `provinces/k_hellas.txt`；+31/-8 行；未作语义复核。
- M `provinces/k_himalaya.txt`；+50/-50 行；未作语义复核。
- M `provinces/k_hujung_medini.txt`；+13/-15 行；未作语义复核。
- M `provinces/k_hungary.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_igbo-benue.txt`；+10/-10 行；未作语义复核。
- M `provinces/k_ireland.txt`；+82/-74 行；未作语义复核。
- M `provinces/k_italy.txt`；+159/-64 行；未作语义复核。
- M `provinces/k_jazira.txt`；+160/-137 行；未作语义复核。
- M `provinces/k_jenne.txt`；+77/-77 行；未作语义复核。
- M `provinces/k_jerusalem.txt`；+56/-50 行；未作语义复核。
- M `provinces/k_kabulistan.txt`；+10/-10 行；未作语义复核。
- M `provinces/k_kamarupa.txt`；+34/-34 行；未作语义复核。
- M `provinces/k_kanem.txt`；+97/-97 行；未作语义复核。
- M `provinces/k_karnata.txt`；+50/-73 行；未作语义复核。
- M `provinces/k_kashmir.txt`；+23/-23 行；未作语义复核。
- M `provinces/k_khakassia.txt`；+16/-16 行；未作语义复核。
- M `provinces/k_kham.txt`；+426/-404 行；未作语义复核。
- M `provinces/k_khitan.txt`；+80/-80 行；未作语义复核。
- M `provinces/k_khorasan.txt`；+70/-70 行；未作语义复核。
- M `provinces/k_khotan.txt`；+180/-180 行；未作语义复核。
- M `provinces/k_kipchak.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_kong.txt`；+1/-1 行；未作语义复核。
- M `provinces/k_kosala.txt`；+65/-65 行；未作语义复核。
- M `provinces/k_krete.txt`；+26/-8 行；未作语义复核。
- M `provinces/k_lanka.txt`；+4/-4 行；未作语义复核。
- M `provinces/k_leon.txt`；+45/-7 行；未作语义复核。
- M `provinces/k_lhomon.txt`；+18/-18 行；未作语义复核。
- M `provinces/k_lithuania.txt`；+42/-42 行；未作语义复核。
- M `provinces/k_lotharingia.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_luzhen.txt`；+73/-72 行；未作语义复核。
- M `provinces/k_maghreb.txt`；+89/-89 行；未作语义复核。
- M `provinces/k_maharastra.txt`；+72/-85 行；未作语义复核。
- M `provinces/k_makran.txt`；+85/-85 行；未作语义复核。
- M `provinces/k_malayadvipa.txt`；+26/-26 行；未作语义复核。
- M `provinces/k_mali.txt`；+128/-128 行；未作语义复核。
- M `provinces/k_maluku.txt`；+16/-16 行；未作语义复核。
- M `provinces/k_malwa.txt`；+106/-111 行；未作语义复核。
- M `provinces/k_maryul.txt`；+304/-296 行；未作语义复核。
- M `provinces/k_mesopotamia.txt`；+145/-141 行；未作语义复核。
- M `provinces/k_moldavia.txt`；+116/-83 行；未作语义复核。
- M `provinces/k_mongolia.txt`；+37/-37 行；未作语义复核。
- M `provinces/k_mordvinia.txt`；+25/-25 行；未作语义复核。
- M `provinces/k_naimania.txt`；+53/-53 行；未作语义复核。
- M `provinces/k_navarra.txt`；+42/-9 行；未作语义复核。
- M `provinces/k_nikaea.txt`；+467/-329 行；未作语义复核。
- M `provinces/k_norway.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_novgorod.txt`；+53/-38 行；未作语义复核。
- M `provinces/k_nubia.txt`；+24/-24 行；未作语义复核。
- M `provinces/k_ob.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_oghuz_il.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_opolye.txt`；+70/-52 行；未作语义复核。
- M `provinces/k_orissa.txt`；+63/-69 行；未作语义复核。
- M `provinces/k_pagan.txt`；+138/-123 行；未作语义复核。
- M `provinces/k_permia.txt`；+11/-11 行；未作语义复核。
- M `provinces/k_persia.txt`；+153/-164 行；未作语义复核。
- M `provinces/k_philippines.txt`；+30/-30 行；未作语义复核。
- M `provinces/k_poland.txt`；+294/-179 行；未作语义复核。
- M `provinces/k_pomerania.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_pontic_steppe.txt`；+75/-72 行；未作语义复核。
- M `provinces/k_pontus.txt`；+551/-380 行；未作语义复核。
- M `provinces/k_punjab.txt`；+223/-223 行；未作语义复核。
- M `provinces/k_qara_dala.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_rajputana.txt`；+63/-65 行；未作语义复核。
- M `provinces/k_romagna.txt`；+101/-32 行；未作语义复核。
- M `provinces/k_ruthenia.txt`；+169/-106 行；未作语义复核。
- M `provinces/k_sahara.txt`；+26/-26 行；未作语义复核。
- M `provinces/k_sakhalin.txt`；+3/-3 行；未作语义复核。
- M `provinces/k_sao.txt`；+48/-48 行；未作语义复核。
- M `provinces/k_sapmi.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_sardinia.txt`；+44/-14 行；未作语义复核。
- M `provinces/k_saryarka.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_scotland.txt`；+171/-64 行；未作语义复核。
- M `provinces/k_serbia.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_shiwei.txt`；+33/-33 行；未作语义复核。
- M `provinces/k_sibir.txt`；+12/-12 行；未作语义复核。
- M `provinces/k_sicily.txt`；+102/-53 行；未作语义复核。
- M `provinces/k_sindh.txt`；+109/-109 行；未作语义复核。
- M `provinces/k_songhay.txt`；+70/-70 行；未作语义复核。
- M `provinces/k_spanish_galicia.txt`；+97/-49 行；未作语义复核。
- M `provinces/k_sulawesi.txt`；+15/-15 行；未作语义复核。
- M `provinces/k_sweden.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_syr_darya.txt`；+62/-62 行；未作语义复核。
- M `provinces/k_syria.txt`；+209/-162 行；未作语义复核。
- M `provinces/k_tahert.txt`；+75/-75 行；未作语义复核。
- M `provinces/k_takrur.txt`；+81/-81 行；未作语义复核。
- M `provinces/k_tamilakam.txt`；+182/-197 行；未作语义复核。
- M `provinces/k_telingana.txt`；+33/-33 行；未作语义复核。
- M `provinces/k_thessalonika.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_transoxiana.txt`；+121/-121 行；未作语义复核。
- M `provinces/k_tsang.txt`；+76/-69 行；未作语义复核。
- M `provinces/k_tuva.txt`；+11/-11 行；未作语义复核。
- M `provinces/k_u.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_valencia.txt`；+82/-82 行；未作语义复核。
- M `provinces/k_venice.txt`；+8/-2 行；未作语义复核。
- M `provinces/k_viet.txt`；+11/-11 行；未作语义复核。
- M `provinces/k_volga_bulgaria.txt`；文本未解码；行数未计算；未作语义复核。
- M `provinces/k_wales.txt`；+101/-25 行；未作语义复核。
- M `provinces/k_white_rus.txt`；+116/-65 行；未作语义复核。
- M `provinces/k_yavakadvipa.txt`；+11/-11 行；未作语义复核。
- M `provinces/k_yemen.txt`；+16/-16 行；未作语义复核。
- M `provinces/k_yorubaland.txt`；+3/-3 行；未作语义复核。
- M `provinces/k_yugra.txt`；+12/-12 行；未作语义复核。
- M `provinces/k_zanj.txt`；+27/-27 行；未作语义复核。
- M `provinces/k_zhetysu.txt`；+93/-93 行；未作语义复核。
- A `situations/pam_the_christian_church_history.txt`；+62/-0 行；已复核关键定义/差异。
- M `titles/00_other_titles.txt`；+578/-126 行；未作语义复核。
- M `titles/01_admin_titles.txt`；+0/-349 行；未作语义复核。
- M `titles/01_admin_titles_tgp.txt`；+4/-4124 行；未作语义复核。
- M `titles/01_laamp_titles.txt`；+82/-236 行；未作语义复核。
- M `titles/02_japan_noble_family.txt`；+12/-1351 行；未作语义复核。
- M `titles/02_korea_noble_family.txt`；+5/-532 行；未作语义复核。
- M `titles/02_other_noble_family.txt`；+11/-521 行；未作语义复核。
- A `titles/ce3/00_ecclesiastical_titles.txt`；+4515/-0 行；未作语义复核。
- M `titles/e_china.txt`；+14/-131 行；未作语义复核。
- M `titles/e_goryeo.txt`；+0/-6 行；未作语义复核。
- M `titles/e_japan.txt`；+31/-19 行；未作语义复核。
- M `titles/e_khmer.txt`；+26/-26 行；未作语义复核。
- M `titles/k_amur.txt`；+5/-5 行；未作语义复核。
- M `titles/k_andalusia.txt`；+1/-1 行；未作语义复核。
- M `titles/k_aquitaine.txt`；+22/-22 行；未作语义复核。
- M `titles/k_aragon.txt`；文本未解码；行数未计算；未作语义复核。
- M `titles/k_badajoz.txt`；+9/-9 行；未作语义复核。
- M `titles/k_balhae.txt`；+38/-31 行；未作语义复核。
- M `titles/k_bavaria.txt`；文本未解码；行数未计算；未作语义复核。
- M `titles/k_bohemia.txt`；+1/-1 行；未作语义复核。
- M `titles/k_borneo.txt`；+1/-1 行；未作语义复核。
- M `titles/k_burgundy.txt`；文本未解码；行数未计算；未作语义复核。
- M `titles/k_croatia.txt`；+1/-1 行；未作语义复核。
- M `titles/k_denmark.txt`；文本未解码；行数未计算；未作语义复核。
- M `titles/k_dvaravati.txt`；+5/-5 行；未作语义复核。
- M `titles/k_east_francia.txt`；文本未解码；行数未计算；未作语义复核。
- M `titles/k_egypt.txt`；+7/-3 行；未作语义复核。
- M `titles/k_england.txt`；文本未解码；行数未计算；未作语义复核。
- M `titles/k_france.txt`；文本未解码；行数未计算；未作语义复核。
- M `titles/k_frisia.txt`；+83/-81 行；未作语义复核。
- M `titles/k_hungary.txt`；+3/-3 行；未作语义复核。
- M `titles/k_italy.txt`；+249/-284 行；未作语义复核。
- M `titles/k_jerusalem.txt`；+3/-3 行；未作语义复核。
- M `titles/k_khitan.txt`；+3/-0 行；未作语义复核。
- M `titles/k_lotharingia.txt`；文本未解码；行数未计算；未作语义复核。
- M `titles/k_luzhen.txt`；+24/-21 行；未作语义复核。
- M `titles/k_naimania.txt`；+339/-245 行；未作语义复核。
- M `titles/k_norway.txt`；文本未解码；行数未计算；已复核关键定义/差异。
- M `titles/k_otuken.txt`；+0/-1024 行；未作语义复核。
- M `titles/k_poland.txt`；+10/-7 行；未作语义复核。
- M `titles/k_pomerania.txt`；+17/-11 行；未作语义复核。
- M `titles/k_romagna.txt`；文本未解码；行数未计算；未作语义复核。
- M `titles/k_sardinia.txt`；+2/-2 行；未作语义复核。
- M `titles/k_sicily.txt`；+13/-12 行；未作语义复核。
- M `titles/k_spanish_galicia.txt`；+11/-10 行；未作语义复核。
- M `titles/k_sweden.txt`；文本未解码；行数未计算；已复核关键定义/差异。
- M `titles/k_syria.txt`；+1/-1 行；未作语义复核。
- M `titles/k_thessalonika.txt`；+1/-1 行；未作语义复核。
- M `titles/k_transoxiana.txt`；+8/-8 行；未作语义复核。
- M `titles/k_valencia.txt`；+18/-19 行；未作语义复核。
- M `titles/k_xia.txt`；+3/-1 行；未作语义复核。

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

