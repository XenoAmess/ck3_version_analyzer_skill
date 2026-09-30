# 证据格式与统计口径

当前 schema_version 为 2。历史 schema-v1 报告保留为历史产物，不静默转换：
旧报告没有可靠的二进制哈希、完整深度分析和覆盖清单，需要重新扫描才能满足新交付检查。

## JSON

- version_old / version_new：从选定目录名称提取的标签，不能替代提交信息。
- timestamp：自动化证据生成时间，含时区。
- version_info.old / new：game_branch、game_commit、engine_branch、engine_commit。分别读取 titus_branch.txt、titus_rev.txt、clausewitz_branch.txt、clausewitz_rev.txt；缺失或不可读时明确写为未知。
- summary：added、removed、modified、unchanged、total_old、total_new。
- file_diffs：全量扫描文件清单，包括未变化文件。路径统一为相对输入根目录的正斜杠路径。
- old_info / new_info：不存在的一侧为 null；存在时记录 size、sha256、is_binary、line_count、encoding、text_error。
- deep_diffs：新增、删除、修改文本文件的证据。hunks 中保存旧/新起始行、范围和按原顺序排列的 lines；前缀为空格、减号、加号，分别表示上下文、删除、新增。
- systems：所有变化系统，包括小改动及 unclassified。目录给出主分类；历史头衔等可有附加标签。
- coverage：候选文本、已分析、跳过、变化二进制计数，以及 skipped、binary_paths、all_text_files_analyzed 和限制参数。
- issues：解码、版本元信息读取或其他异常。无法完整读取或扫描文件时，命令直接失败，避免把扫描遗漏计成删除。
- metadata：SHA-256 比较口径、文本编码、协作人、模型标签、LLM 复核状态。完成最终报告时追加 final_generated_at 和实际 reviewed_paths。
- artifacts：本次各输出文件的文件名，最终文件由当前 Agent 撰写。

## 数量不变量

~~~text
total_old = unchanged + modified + removed
total_new = unchanged + modified + added
total_new - total_old = added - removed
changed_files = added + removed + modified
changed_files = candidate_files + binary_files
candidate_files = analyzed_files + skipped_files
~~~

lines_added 和 lines_removed 是实际行级差异计数；line_changes 是两者之和。
net_line_change 是文件总行数差，两者必须区分。等行数替换的净变化可以是 0，实际差异仍大于 0。
未经行级对比的修改文件，其增删行数为 null；二进制行数也为 null。
新增、删除的有效文本可以直接按全部内容计数。

主分类 primary_file_count 可相加；含附加标签的 file_count 不可相加代替全局总数。
priority_candidate 表示审查优先级，不能作为已确认重大玩法变化的结论。
即使没有任何重要候选，也保留小改动清单，不能直接声称没有重要机制变化。

脚本按机制相关目录、新增/删除状态、大小差异、路径进行确定性排序，再应用 --max-deep-files。
这不代表最终重要性；模型核实语义后可以调整报告顺序。

## 读取与恢复

文本严格解码；已知非 UTF-8 编码时用 --encoding 显式重新运行。编码错误不应通过 errors=ignore 隐藏。
扫描和提取证据之间重新校验文本哈希；源文件发生变化时停止并要求重新扫描。
仅 BOM/换行等字节差异而解码后文本相同的文件标为 byte_only，不推断其有功能变化。

复用 JSON 前核实 metadata.input_directories、两版提交和当前目录快照。
SHA-256 的用途是版本内容比较；没有执行游戏，也没有反编译引擎。
二进制变化的玩法影响和部分脚本行为需要额外证据或实际运行验证。

CSV 使用 SHA256 列替代历史 MD5 列，同时包含实际增删行数和净变化。
未计算的值留空，不转换为 0。
