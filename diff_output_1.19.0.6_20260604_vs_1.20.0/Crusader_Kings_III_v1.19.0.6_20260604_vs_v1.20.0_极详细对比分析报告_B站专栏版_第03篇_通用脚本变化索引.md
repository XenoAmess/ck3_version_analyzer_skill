# CK3 1.19.0.6 → 1.20.0 极详细对比分析报告（3/4）：通用脚本变化索引

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

本篇为四篇系列的第 3 篇，内容范围：附录 A.6 中 game/common/ 下全部 1345 个变化路径。各项标明新增/删除/修改、原始增删行数与是否作过关键定义或差异的语义复核。

上面的版本信息、扫描统计和末尾的 76 个 LLM复核文件均为原分析的全局口径，不是本篇新增复核的数量。拆分只调整发布篇幅，未扩大语义分析覆盖，未删去原报告的代码证据或限制说明。

本篇 A.6 导语中的 2515 项指系列合计的脚本、事件、历史与 GUI 索引；本篇收录的具体范围以上述数量为准。A/D/M 和行数均来自自动差异证据，“未作语义复核”不能视为已确认的机制或修复结论。分组标题是源码路径前缀，与各条目拼接后得到完整相对路径。

## 附录 A: 通用脚本变化索引

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

- **分卷编号**: 3/4

- **计数口径**: 标题、正文、代码、标点、空格、换行及 Markdown 标记均计入；非 BMP 字符按两个 UTF-16 单元计，采用保守计数。

- **分卷全字符计数**: 78774

