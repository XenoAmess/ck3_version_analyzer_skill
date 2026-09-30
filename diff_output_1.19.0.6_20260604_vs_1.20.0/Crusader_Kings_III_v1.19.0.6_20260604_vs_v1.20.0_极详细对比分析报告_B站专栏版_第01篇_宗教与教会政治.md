# CK3 1.19.0.6 → 1.20.0 极详细对比分析报告（1/4）：宗教与教会政治

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

本篇为四篇系列的第 1 篇，内容范围：执行摘要与第 1—22 章：DLC、Faith/Rite/Tenet、狂热、改宗、个人教义、精神满足度、神权、继承人、枢机、代理人、教会局势、宗教会议、对立教宗、圣地及主教座堂。

上面的版本信息、扫描统计和末尾的 76 个 LLM复核文件均为原分析的全局口径，不是本篇新增复核的数量。拆分只调整发布篇幅，未扩大语义分析覆盖，未删去原报告的代码证据或限制说明。

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

- **分卷编号**: 1/4

- **计数口径**: 标题、正文、代码、标点、空格、换行及 Markdown 标记均计入；非 BMP 字符按两个 UTF-16 单元计，采用保守计数。

- **分卷全字符计数**: 59855

