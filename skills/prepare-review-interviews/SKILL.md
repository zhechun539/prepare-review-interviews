---
name: prepare-review-interviews
description: Prepare candidates for interviews and review completed interviews with persistent, evidence-based personalization. Use when a user asks for 面试准备、公司与岗位分析、可能面试题、自我介绍、STAR 案例、模拟面试、反问清单、面试录音或逐字稿复盘、初面/复试/终面复盘，or supplies a company homepage, company introduction, JD, resume, portfolio, interview notes, transcript, audio, or interview-review request. On first use, collect and locally index the user's resume, portfolio, and relevant evidence; on later uses, proactively load the saved profile before researching the company and tailoring the output. Supports public-web and Xiaohongshu research while separating verified facts from user-generated experiences.
---

# Prepare and Review Interviews

把面试前准备和面试后复盘做成同一条证据链：先读用户，再读公司和岗位；面试后再把真实表现沉淀回可复用的答案与行动。

把本文件所在目录记为 `SKILL_DIR`。所有 `scripts/` 和 `references/` 相对路径都从 `SKILL_DIR` 解析，不从当前工作目录猜测。

## 每次开始

1. 运行 `python <SKILL_DIR>/scripts/profile_store.py status --profile-id default`。若 Python 命令不可用，使用当前环境可用的 Python 运行时。
2. 若状态为 `ready`，运行 `python <SKILL_DIR>/scripts/profile_store.py show --profile-id default` 并完整读取资料档案，再处理当前请求。
3. 若状态为 `stale`，先读取已保存档案；对本次岗位有影响的缺失或已变化源文件重新读取并更新档案。不要因一个无关旧链接失效而阻塞整个任务。
4. 若状态为 `missing`，要求用户首次提供：
   - 简历（必需）；
   - 作品集或代表项目材料（有则必需提供；确实没有时记录“暂无作品集”）；
   - 可选补充：目标岗位、作品链接、求职偏好、不能公开的信息。
5. 不要求用户重复提供已保存的信息。只有档案缺字段、材料发生变化或当前岗位需要关键新事实时才追问。
6. 如果用户在档案未建立前已经给了公司与 JD，先做不依赖个人资料的公司/JD初步分析，同时明确个性化部分将在资料入库后补齐。

## 首次建档或更新档案

读取 `references/profile-schema.md`。对用户提供的所有简历、作品集和证据文件使用对应文件技能完整读取；不得仅依赖文件名、摘要或单页预览。

建立结构化档案时：

- 只保存用户材料中明确出现或用户明确确认的事实；
- 给量化结果、日期、职责和项目边界附来源；
- 区分个人结果、团队结果、公司结果和无法归因结果；
- 把敏感信息与对外可用信息分开；
- 把事实、推断、待确认项分开；
- 冲突时保留各来源、日期与差异，不擅自选一个“更好看”的数字；
- 不把简历上传到搜索网站、公司网站、小红书或其他第三方。

将档案写成 UTF-8 JSON 临时文件，然后运行：

```text
python <SKILL_DIR>/scripts/profile_store.py save --profile-id default --input <profile.json> --source <resume> --source <portfolio>
```

在 Windows 上遇到中文或其他非 ASCII 路径时，把绝对路径写入 UTF-8 JSON 数组，并改用 `--source-list <sources.json>`，避免把重要中文路径直接作为外部脚本参数。

用户补充或纠正事实后重新保存档案。面试录音里的口误或机器转写不自动覆盖已确认事实。

## 判断当前模式

- 用户尚未面试，或提供公司主页、公司介绍、JD、招聘链接：执行“面试前准备”。
- 用户已经面试，或提供录音、逐字稿、问题清单、回忆笔记：执行“面试后复盘”。
- 用户同时给出新岗位和上一轮面试记录：先复盘，再把复盘得到的高价值改进应用到下一轮准备。
- 用户只想模拟：先完成最小版准备，再逐题模拟；每次只问一道题，等用户回答后再追问和反馈。

## 面试前准备

完整读取 `references/pre-interview.md` 与 `references/research-evidence.md`。

最低输入是公司名称或主页、岗位职责/JD、面试阶段。缺少阶段时可按初面假设开始，并标注假设。用户没有给公司主页时可以搜索官方来源，不要把同名公司混为一家公司。

最终材料必须同时完成四件事：

1. 讲清公司与岗位真正要解决的问题；
2. 用用户的真实经历证明匹配度；
3. 预判高概率追问并给出可说出口的回答；
4. 暴露无法靠包装掩盖的缺口，并给出补齐动作。

不要只罗列公司介绍、渠道名或通用题库。答案要连接“岗位意图—用户证据—事实边界—表达方式”。

## 面试后复盘

完整读取 `references/post-interview.md` 与 `references/output-standard.md`。

优先读取完整录音、逐字稿或用户回忆。转写不确定处标为“未可靠确认”，不要编造逐字内容。逐题分析原回答完成了什么证明、缺了什么、是否越过事实边界，再写优化回答。

复盘必须落到下一次行为变化，不能只给“表达更自信”“加强行业了解”这类空结论。把行动写成可练习、可计时、可核验的任务。

## 研究规则

优先级：公司官网/官方账号/招聘页/工商与权威媒体 → 产品与渠道事实 → 可信行业资料 → 小红书等用户生成内容。

- 搜索最新信息时注明检索日期和来源链接。
- 公司事实与员工/候选人体验分开写。
- 小红书重点搜索“公司名 + 面试/岗位/工作体验/加班/薪资/避雷”等组合；只把帖子当线索或体验证据，不当作公司事实。
- 记录帖子标题、作者或账号、发布日期、链接、是否第一手、与其他帖子是否相互印证。
- 登录、验证码、内容不可见或样本不足时直说限制，不伪造“网友普遍认为”。
- 不因负面帖直接下结论；寻找时间、岗位、地区、团队差异和反例。

## 输出与保存

默认交付 Markdown；用户要求 DOCX、PDF 或其他格式时，再使用相应文件技能生成并完成视觉验证。

完成一次准备或复盘后，把不含无必要敏感信息的会话摘要写成 UTF-8 JSON，并运行：

```text
python <SKILL_DIR>/scripts/profile_store.py record --profile-id default --mode prep --input <session.json>
python <SKILL_DIR>/scripts/profile_store.py record --profile-id default --mode review --input <session.json>
```

只有用户明确确认的新事实才更新主档案。研究结论、面试官评价推测和模型判断只进入会话记录，不写成个人事实。

## 事实与隐私底线

- 不虚构公司信息、面试题、用户经历、日期、数据、职责或因果关系。
- “高概率问题”是预测，不写成“该公司一定会问”。
- 不把团队或公司业绩写成候选人个人业绩。
- 不主动在对外答案中暴露生日、手机号、邮箱、疾病、家庭信息等敏感内容。
- 医疗、空窗、离职等敏感问题采用用户确认的口径；不得替用户撒谎。
- 每个示范答案都以用户真实证据为上限。证据不足时给结构与补证方向，不补故事。
