# CK3 Version Analyzer

比较两个 Crusader Kings III 版本目录，提取代码差异，再由当前 Agent 完成中文玩法解读。
Python 3.10+，运行脚本无需第三方依赖。

## 使用

在仓库根目录运行，明确指定旧版、新版和输出位置：

~~~powershell
py -3 ck3_analyzer.py analyze "Crusader Kings III_1.19.0.4" "Crusader Kings III_1.19.0.5" --output-dir "diff_output_1.19.0.4_vs_1.19.0.5"
~~~

其他系统可用 python。输入也可使用绝对路径；相对输入基于当前工作目录或 --base-dir。
输出路径基于当前工作目录，不能放在输入目录内。省略 --output-dir 时按版本配对命名。
历史默认配对仍为 1.18.4 → 1.19.0，执行前应确认就是要分析这组版本。

- --max-deep-files N：先排序再限制文本分析；0 为全量。
- --snippet-lines N：每文件展示最多 N 行原始差异，默认 20；0 不限制。
- --no-deep-analysis：仅扫描与统计。
- --encoding NAME：显式指定无 BOM 文本编码，默认严格 UTF-8。
- --model LABEL：记录模型标签，不调用模型。
- --author XenoAmess：保留兼容参数，协作人固定。

运行 --help 查看完整参数。

## 输出与准确性

脚本生成 diff_report.json、diff_report.csv、带版本前缀的初步报告及其 B 站版。
JSON 在分析结束后导出，含版本提交、SHA-256、完整文本差异、系统分类、异常与覆盖清单。
所有文件包括二进制都比较内容哈希，行变化使用实际新增行＋删除行，与净行数变化分开。
目录与关键词分类仅是审查候选；不自动断言 Bug 修复、开发动机或玩家策略。

初步报告之后，Agent 核实旧/新代码及相关调用，生成两份无表格的最终报告。
B 站最终版独立可读，不依赖其他产物。最终交付前运行 skill 内的 validate_report.py。
旧 schema-v1 报告仍保留；要满足新验收条件需重新扫描。

## 维护入口

- ck3_analyzer.py：唯一分析实现。
- [.sisyphus/skills/ck3_version_analyzer/SKILL.md](.sisyphus/skills/ck3_version_analyzer/SKILL.md)：唯一 skill 规则入口。
- .sisyphus 下的 references：证据口径与最终报告模板，按需读取。
- .omo 下的 skill 及两处同名脚本：兼容入口，转发到上述实现。
- tests/test_ck3_analyzer.py：核心比较、覆盖、路径及交付检查的回归测试。

保留原 skill 目录名；入口文件采用 SKILL.md 并包含 name / description frontmatter。
这是仓库内 skill，单独复制时需要同时带上根实现并调整转发路径。

## 验证

~~~powershell
py -3 -B -m unittest discover -s tests -v
~~~

测试使用隔离的临时夹具，不修改游戏目录或历史报告。

协作人：XenoAmess。
