# 会话日志

> 每次和 Claude 的工作在这里留一条：做了什么、依据是什么、下次从哪继续。

---

## Session 001 · 2026-08-24 —— 计划成型

**产出**

- `PLAN.md` —— 12 个月具身智能学习 + 市场敏锐度作战计划（13 节）
- 网页版发布为 Artifact：**https://claude.ai/code/artifact/ed18a729-7ebe-40d0-97f7-3a1e13ad44f8**（源文件在 `site/embodied-ai-plan.html`）
- 本仓库脚手架：`notes/ papers/ predictions/ experiments/` 四本账 + `CLAUDE.md` 上下文

**背景是怎么推断出来的**（计划的全部前提，有错要改）

原始需求是「我希望深度了解 AI 行业，以具身入手；假如我要到科学家研究院水准，同时有 acute 市场敏锐性」，并要求「不确定就去找我的背景」。推断依据：

- 邮箱域名 → WorldEngine AI；公开资料（PitchBook / Tracxn）显示：深圳，2023 成立，Physical AGI 数据平台 —— 大规模机器人部署、数据采集与管理，团队来自自动驾驶 / 云 AI / 机器人，竞对被列为 ABB、Agile Robots、Flexiv。→ **产业链位置在数据层，不在模型层。**
- 已有的 `interview-summary` 工作流 → 在面运营/BD 候选人（北美渠道、丰疆智能北美、Purdue Robot Lab 这类背景），把「机器人行业认知」当独立评分维度打分，自己关心获客/渠道/谈判/单位经济。→ **商业侧是主职，且手里有一条候选人情报管道。**
- TravelPanel 仓库（45K 字 PRODUCT_STRATEGY.md、North Star metric、状态机、护城河论述）→ **产品与商业直觉是已有资产，工程读写在线，ML/机器人学的形式化训练是缺口。**

**三个关键决策**

1. **目标校准**：1.5h×6 天 ≈ 400h/年，博士四年 ≈ 8000h + 实验室。所以放弃「一年内拼架构」，目标身份定为 **research-literate operator**。
2. **战场选「数据与评测」**：架构层已是千卡竞赛；而遥操作数据集至今没有公认基准、真机评测普遍不可复现（VLA 出分布掉点，但**模型排序稳定** → 数据/评测设计本身是可研究变量）。这个空位公认重要却没人占，且它吃判断力 + 数据访问权 + 工程严谨性，不吃 10k GPU —— 业余时间唯一能通到研究院水准的通道。**用公司的数据当研究护照。**
3. **验收全部可被别人判 false**：L0 表达关 → L1 复现关 → L2 实验关（被研究者认真反驳才算过）→ L3 研究关 → L4 标准关；市场侧用预测日志（70% 置信度档命中率 ≥60%）。

**事实来源**（2026-08 检索）

PitchBook / Tracxn（WorldEngine 画像）· arXiv 2405.14093 / 2505.04769 / 2507.01925 / 2605.12090（VLA 与世界模型综述）· 甲子光年《2026 中国具身智能行业洞察报告》· 机器人大讲堂 × 立德智库《2026 具身智能与人形机器人产业研究报告》· IDC 2026 出货预测（全球人形破 5 万台、+178%）· manipulation.csail.mit.edu（MIT 6.421）· rail.eecs.berkeley.edu/deeprlcourse（CS285）· hades.mech.northwestern.edu（Modern Robotics 免费 PDF）· huggingface/lerobot 与 NVIDIA「Train an SO-101 From Sim-to-Real With Isaac」教程 · 深蓝学院具身智能方向 · 智源大会 2026（主题：世界模型 × 具身智能）

**待定**

- **Phase 0（第 1–6 周数学地板）的长度取决于线代/概率/优化底子。**若已经熟，压到 2 周直接进 Tedrake 6.421，整条路线前移一个月。

**下次从这里继续**

1. 写 `notes/` 第一条（今天学了什么）。
2. 把本季度 10 条预测填进 `predictions/2026Q3.md` 并封存。
3. 日历上锁死每天 90 分钟；下单 SO-101 一对。
4. MuJoCo + LeRobot quickstart 跑通（P1 起步）。

---

## Session 002 · 2026-08-24 —— 背景校正：C 类（读得懂、写不强）

**触发**：owner 追问「能亲手把产品从 0 推到有护城河论述」这句是从哪读出来的。核对后确认：证据（`TravelPanel/CLAUDE.md` 的技术决策表、`:113` North Star Metric、`:57` state machines、`:21` anti-patterns、`SESSIONS.md:17` #1 moat）只能支撑「设定标准 + 运维 agent 队伍并验收」，**不能**支撑「逐字写了代码」—— `TravelPanel/SESSIONS.md:3` 明写 "Auto-maintained by Claude"。原判断「工程读写能力在线」是过度推断。

owner 自陈：**C 类 —— 定方向和标准、Claude 落地、读 diff 和 review，能读懂基础代码但写和调不强。**

**据此改了什么**

| 位置 | 改动 |
|---|---|
| `PLAN.md` §0 | 技术姿态改成校正后的描述，并标注第二个缺口是「读→跑→改」的工程手感 |
| `PLAN.md` §3 | 能力树新增 **L0 工程手感**（2 周 + 贯穿），标准是「2 小时内独立跑通陌生研究仓库，全程不问 AI」 |
| `PLAN.md` §4 | Phase 0：6 周 → **8 周**；Phase 1/2/3 各后移 2 周（L3 落第 54 周）。Phase 1 加「读→改→修」三级台阶 |
| `PLAN.md` §5 | 必修表最前面加 ENGINEERING.md 与 uv / PyTorch 官方 basics / numpy-100 前 40 题；明确 Karpathy Zero-to-Hero 对 C 类是双重收益（micrograd 100 行 = 最好的 Python + 张量训练） |
| `PLAN.md` §7 | 硬规则 五条 → **六条**，新增**逐行可复述 + 报错 60 秒规则** |
| `PLAN.md` §10 | 验证阶梯新增 **L0.5 工程关**（第 8 周）；L1/L2/L3 时点顺延 |
| `PLAN.md` §12 | 第一周第 4 件事换成「读完 ENGINEERING.md 然后开 P0」 |
| `ENGINEERING.md` | **新增。** 7 节：跑起陌生仓库的固定套路 / 读 traceback 的 60 秒规则 / 张量形状思维（含机器人策略的标准形状约定）/ 故意造 bug / 租 GPU 三命令 / AI 结对边界表 / 明确不学清单 |
| `experiments/README.md` | 新增 **P0 工具链**；P2 改成读-改-修三级台阶 |
| `CLAUDE.md` | 技术姿态校正；Claude 的「不允许」从 1 条扩到 3 条（加逐行可复述、加 60 秒规则） |
| `site/` + Artifact | 同步全部改动并重新发布（URL 不变） |

**取舍说明（不是折中，是判断）**：新增的 2 周从 Modern Robotics 编程作业（只做 Ch 3 那批）和 CS285（8–10 讲 → 6 讲）里挤。理由：对「数据与评测」这个终局，能跑能改的边际收益大于多学一门课；卡在 CUDA 报错上的一周，损失比少听两讲大得多。代价：L3 从第 52 周推到第 54 周。

**下次从这里继续**：`notes/` 第一条 + `predictions/2026Q3.md` 填满 + P0 开工。

---

## Session 003 · 2026-09-02 —— 收尾迁移 + 会话交接

**做了**

- 关闭 TravelPanel PR #179（净变更只有 2 行自动会话日志，计划内容已在本仓库）。
- **未完成**：删除远端分支 `claude/ai-career-development-plan-qwj1d6`。`git push origin --delete` 两次都被中断（`send-pack: unexpected disconnect`），会话的 GitHub App token 似乎没有 delete_ref 权限，MCP 也没有删分支的工具。**需要在 GitHub 网页上手动删**：https://github.com/SoaringWillow/TravelPanel/branches —— 或在已关闭的 PR #179 页面点 "Delete branch"。删掉后 TravelPanel 与本计划再无关联。

**当前状态（新会话接手时先看这里）**

| 项 | 状态 |
|---|---|
| 计划本体 `PLAN.md` | 已按「C 类：读得懂、写不强」校正过（见 Session 002），含 L0 工程手感层、P0 项目、L0.5 验收关 |
| `ENGINEERING.md` | 已写好，7 节，Phase 0 第 1 周就要读 |
| 网页版 Artifact | https://claude.ai/code/artifact/ed18a729-7ebe-40d0-97f7-3a1e13ad44f8 （与 `site/embodied-ai-plan.html` 同步） |
| `notes/` | **空** —— 一条都还没写 |
| `predictions/2026Q3.md` | **空**，且 Q3 只剩 4 周 |
| `experiments/` | **P0 未开工** |
| 计划起算日 | **尚未确定** —— Phase 0 第 1 周从哪天算，需要 owner 定 |

**关于预测日志的建议（等 owner 拍板）**：Q3 只剩 4 周，现在填 10 条季度级预测不合适。建议改成：现在写 **5 条短周期预测（9/30 到期）**当校准热身 —— 反馈快、便于建立打分习惯；10 月 1 日再按正式格式开 `2026Q4.md` 写满 10 条。

**下一步（优先级顺序）**

1. 定起算日，把每天 90 分钟锁进日历。
2. 读 `ENGINEERING.md`（1 小时），开 P0：uv 建环境 → LeRobot quickstart → 踩坑日志。
3. 写 `notes/` 第一条。
4. 按上面的建议处理预测日志。

---

## Session 004 · 2026-09-02 —— 起算日落地 + P0 开工

**两个挂起的决策，owner 当场拍板**

| 决策 | 结果 |
|---|---|
| 计划起算日 | **2026-09-02（周三）**。不等下周一 —— 「下周一开始」是弃坑率最高的一句话 |
| 预测日志 | **从零开「第 0 期」校准热身**：5 条、9/30 到期，不计入 12 个月 ≥60% 的目标；正式季度日志从 `2026Q4.md`（10-01 开、10 条）起 |

**做了**

| 位置 | 改动 |
|---|---|
| `PLAN.md` §4 | 新增起算日与**周次→真实日期对照表**（Phase 0–3 + L0/L0.5/L1/L2/L3 五个关口）。Phase 0 = 09-02→10-27，L0.5 工程关 = 10-27，L3 研究关 = 2027-09-14 |
| `PLAN.md` §4 | **修一个真 bug**：Phase 2/3 的周次还是迁移前的「第 19–34 / 35–52 周」。Session 002 把各阶段后移 2 周时只改了 Phase 1 的标题，§10 验收表和 `README.md` 都已是正确的 21–36 / 37–54 —— §4 是唯一漏掉的地方，三处口径现已一致 |
| `experiments/P0-toolchain/README.md` | **新增。** P0 的目标、三个仓库的顺序与「什么算跑通」、L0.5 自测记录表 |
| `experiments/P0-toolchain/踩坑日志.md` | **新增。** 条目表（含**「自读时长」一列** —— 把 60 秒规则做成可自我审计的）+ 每仓库复盘 + **坑的分层统计**（环境隔离 / 系统依赖 / 数据 / 显存 / 代码），用来回答「我到底弱在哪一层」 |
| `predictions/2026Q3.md` | 重写为第 0 期：合格预测的四个条件、好/坏写法对照、题材信息量排序、5 条空表、打分口径 |
| `README.md` · `experiments/README.md` · `site/` | 同步起算日、日期、P0 状态 |

**两个刻意的设计选择（不是省事，是判断）**

1. **P0 的 README 故意不给命令。** ENGINEERING.md 第一节已有那套固定套路，剩下每个坑都得自己踩 —— 替 owner 查掉的报错练不出任何东西。README 给的是**验收标准**（什么算「出第一个数字」）和时间盒，不是 copy-paste 的命令行。
2. **三个仓库的顺序改成 micrograd → MuJoCo demo → LeRobot quickstart**（`experiments/README.md` 原来的列举顺序是 LeRobot 打头）。每个仓库考一类坑：纯 Python 环境隔离 → 二进制/渲染依赖 → 研究仓库全套（大依赖树 + 数据下载 + 显存）。倒过来做，会在第一天被一个 CUDA 报错埋掉，然后**分不清是哪一层的问题** —— 而分层能力正是 P0 要练的东西。

**Claude 明确没做的事**（按 `CLAUDE.md` 的分界线：AI 可以替 owner 打字，不能替 owner 判断）

- 没写 `notes/` 第一条 —— 那是 owner 的输出，代写等于把这条规则作废。
- 没填那 5 条预测的内容 —— 预测日志度量的是 owner 的判断力，Claude 填了就没有校准价值。给的是格式和判据。
- 没有替 owner 跑 P0 的三个仓库。

**当前状态**

| 项 | 状态 |
|---|---|
| 起算日 | **2026-09-02**，日期表在 `PLAN.md` §4 |
| `experiments/P0-toolchain/` | 脚手架就绪，**等 owner 开跑**（先读 ENGINEERING.md 1 小时） |
| `predictions/2026Q3.md` | 表格就绪，**等 owner 填 5 条** |
| `notes/` | 仍然空 —— 第一条还没写 |
| 遗留（Session 003 带过来的） | 远端分支 `claude/ai-career-development-plan-qwj1d6`（TravelPanel 仓库）仍需**在网页上手动删**：https://github.com/SoaringWillow/TravelPanel/branches 。本会话的仓库权限只覆盖 ai-study-lab，删不了 |

**下一步（优先级顺序）**

1. 读 `ENGINEERING.md`（1 小时）—— Phase 0 第 1 周的第一件事。
2. 开 P0 仓库 1（micrograd，时间盒 1h），踩坑记进日志。
3. 写 `notes/2026-09-02.md` 第一条（三段：我原以为 / 现在知道 / 还不懂）。
4. 填 `predictions/2026Q3.md` 的 5 条并封存 —— 记得至少 1 条是「希望它是错的」。
5. 把每天 90 分钟锁进日历；下单 SO-101 一对（Phase 1 第 9 周要用，即 10-28）。

### 追加 · 每日 Lark 简报机器人

owner 追问：能不能每天在 Lark 上把「今日安排 + 资源」推过来，无痛直接开始；以及这套提示是不是活在 Lark 里更稳。

**架构判断（回答「活在 Lark 里更稳吗」）**：一半对。**推送和回执该在 Lark**（无痛 = 零跳转），**课程表本体不该** —— 它要被反复重排（多维表格的自动化没有判断力）、要用 `git log` 记住「当时为什么砍这一讲」、不能随一个群或应用的停用而消失。所以：**仓库当编译器，Lark 当运行时。**

**这次会话踩到的三个真实边界**（都实测过，不是猜的）

| 边界 | 实测结果 |
|---|---|
| Claude 侧有没有 Lark 连接器 | **没有**。账号已装的是 Canva/Gmail/Google Calendar/Drive/Notion/Slack/robinhood；MCP 目录搜 lark、feishu、bitable 只返回 Slack |
| 这个会话在哪台机器 | **云端 Linux 容器**（`hostname: vm`），不是 owner 的 Mac —— 连 `/Users` 目录都没有，所以 `~/Documents/WorldEngine Claude folder` 里的东西够不到；`~/.claude.json` 的 `mcpServers` 为空 |
| 能不能从这里发 Lark | **不能**。`open.larksuite.com` 与 `open.feishu.cn` 在 CONNECT 层就 403（装 CLI 也没用）。arxiv.org、docs.astral.sh、pytorch.org 同样被封 —— 所以第一次真发必须在 owner 本机 |

**建的东西**

| 文件 | 作用 |
|---|---|
| `schedule/curriculum.yaml` | 真相源。W1 六个单元，每个精确到集数/章节 + 三段时间盒 + 产出文件 + 降级版 |
| `schedule/resources.yaml` | 资源库 id → {标题, url}，链接失效只改一处 |
| `schedule/state.yaml` | 运行时状态：`last_output_date` + 每日日志 |
| `bot/render.py` | yaml → 卡片（纯函数，不联网）。含 `--check-all` 全量 lint |
| `bot/send.py` | stdlib urllib 发送，`--dry-run` 脱敏打印请求体 |
| `bot/ingest.py` | daily-log issues + `notes/*.md` → 重建 state.yaml |
| `.github/workflows/daily-brief.yml` | cron ×2（21:20 / 06:20 北京，留 10 分钟吸收 Actions 延迟）+ 手动触发 |
| `.github/workflows/weekly-replan.yml` | 周日 21:00：ingest → 周报卡 → replan issue |
| `.github/ISSUE_TEMPLATE/daily-log.yml` | 回执表单，含「卡在哪一层」六选 |

**三个刻意的设计决定**

1. **卡片上没有纯打勾的「完成」按钮。** 三个按钮（交产出 / 卡住了 / 20 分钟版）全部通向一个要写一行字的预填 issue。理由：`PLAN.md` §11 反模式第一条是「只看视频不敲键盘」，而提醒机器人最容易退化成「已读即完成」—— 连点 30 天卡片、感觉良好、什么都没学会。**回执必须是 artifact，不是一个勾。**
2. **债务规则交给机器执行**，不靠意志力：断 1–2 天只标「不补课，直接继续」；断 ≥3 天卡片**自动切成 30 分钟降级版**。「先把落下的补回来」这个选项在系统里根本不存在。20 分钟版**不算断链** —— 链条不断比进度重要。
3. **W1 刻意偏离周节奏**：起算日恰好是周三，而周三本该是论文日 —— 那样计划的第一个 90 分钟就是硬读 ACT/ALOHA，此时既没有 transformer 也没有形状思维，只会读成名词背诵。所以 W1 周三换成 ENGINEERING.md，论文日挪到周二。W2 起恢复标准节奏。

**先渲染后接推送，因此在写代码阶段抓到 4 个 bug**（不是上线后才发现）

| bug | 后果 |
|---|---|
| 债务规则拿目标日期当上界 | 把**还没到的日子**算成断链，晚上那张卡会指控你欠它明天 |
| 本地路径直接当按钮 url | `./ENGINEERING.md` 在手机上点了打不开 —— 「无痛」直接不成立。改成 GitHub blob 链接 |
| 同一资源出现两个相同按钮 | 两个 deep 项引同一文件时 |
| `issue.get("pull_request")` 判 PR | **空 dict 是 falsy**，PR 会被当成学习日记入 |

另外 arXiv 编号（ACT 2304.13705 / Diffusion Policy 2303.04137 / OpenVLA 2406.09246）逐个核对过；3B1B 找到**B 站官方双语合集 `BV1ys411472E`**，比 YouTube 链接对国内可靠。`resources.yaml` 里 4 个封了域名验不了的链接标了 `unverified:`，`--check-all` 会列出来提醒。

**待办**

1. **owner 先看 W1 六张卡的粒度** —— 确认后 Claude 补完 W2–W8 的 42 个单元（现在只有 W1）。粒度不对现在改比第 5 周改便宜。
2. owner 在 Mac 上跑一次真发（`bot/send.py --slot morning`），看 `code: 0` + **手机上卡片的实际排版**（这一步只有真机能验）。
3. GitHub 配 secrets `LARK_APP_ID` / `LARK_APP_SECRET` / `LARK_RECEIVE_ID` + variable `LARK_DOMAIN`，手动跑一次 workflow，再开 cron。

**推送通不通，不该成为 9 月 2 日不开工的理由** —— `--preview` 出来的文本可以直接抄进 Lark 自己发给自己。

---

## Session 005 · 2026-09-24 —— 诊断空窗三周的真实原因，补上缺的那一层

**触发**：owner 要一份「怎么在这台 Mac mini 上真正动手」的 PDF。

**先说诊断**：起算日 2026-09-02 到 09-24，三周过去，`notes/` 仍是空的、P0 一个仓库没跑、`last_output_date` 还是 `null`、课程表停在 W1、Lark 一条消息没真发过。

**所以卡点从来不是「没有安排」** —— 安排、卡片、债务规则、回执表单在 9 月 2 日就全建好了。卡点是**「我知道今天该跑 micrograd，但不知道第一条命令敲什么」**。计划和键盘之间缺了一层，这次补的就是它。

**四个用工具查实的事实**（都会让「照着现有文档走」当场卡住）

| 事实 | 影响 |
|---|---|
| `lerobot 0.6.1` 要求 **Python ≥ 3.12** | `ENGINEERING.md` 写的 `uv venv --python 3.11` 直接装不上 —— 已改 3.12 |
| `lerobot` 锁 `torch<2.12`，最新 torch 是 2.14 | 先装 torch 再装 lerobot 必打架，手册里写死了顺序 |
| macOS 的 MuJoCo 交互式 viewer **必须用 `mjpython`**（渲染要在主线程） | 直接 `python xxx.py` 必失败 |
| **`mjpython` 和 uv 自带的 Python 冲突**（找不到 `libpython3.x.dylib`，MuJoCo issue #1923 未关） | 而我们正推荐 uv —— 手册改成「先离屏渲染（必通），viewer 作可选 + 用 Homebrew 的 python 建 venv」 |

另外核实了 `mujoco 3.14.0` 有 arm64 轮子、torch 在 lerobot 允许区间内 macOS 11+ 即可、`torchcodec` 支持 darwin/arm64、`lerobot-info` 是最小的「出第一个数字」命令。

**起算日重置 2026-09-02 → 2026-09-28（周一）**

owner 原选 09-21，但今天已是周四 —— 按 09-21 起算，债务规则会**立刻**判断链 3 天并把每张卡片降级。改 09-28，把 09-24～09-27 当作**第 0 周：装机**（正是手册第 1–2 章）。三个连带好处：环境配置不占用学习日；周次与自然周对齐；**W1 那处「周三换课程主线」的特例可以撤掉了**（周一起算后 §7 的节奏直接成立）。

新日期：Phase 0 = 09-28 → 11-22 · L0 表达关 11-08 · L0.5 工程关 11-22 · L3 研究关 2027-10-10。
**W1 的周四至周六落在国庆（10-01～10-03）**，不为此推迟 —— 出不来就用 20 分钟版，链条不断比进度重要。

**产出**

- `docs/mac-handbook/`（HTML 源 + **31 页 PDF**）。十章：怎么用 → 认识机器 → 装地基 → micrograd → MuJoCo → LeRobot → P1 IK → P2 租卡 → 排错 → 速查卡。
- 全书统一三段式：**① 敲什么 ② 应该看到什么 ③ 没看到怎么办**。第二段最重要 —— 不知道「对」长什么样，就分不清「还在装」和「已经卡住了」。
- 重排 W1（周一起算的标准节奏），并修掉一个**倒置依赖**：原 day 4 引用「周六跑通的 micrograd」，而动手日现在排在它之后 —— 改成用自写的 10 行 numpy 脚本造 bug，自包含。
- `curriculum.yaml` 每个单元加 `handbook` 字段指向手册章节，`render.py` 渲染进卡片。
- 同步：`PLAN.md` §4 · `README.md` · `state.yaml` · `site/`（Artifact 网页版）。

**两条刻意的诚实度规则**

1. **不编数字。**「训练要几小时」「占多少显存」这类没测过的一律不写，第 7 章改成**教 owner 自己测**（本地跑 100 步计时，按比例外推）。既得到真数，又练了估算。
2. **每条命令标 `已验证` / `未实测`。**写文档的机器是 Linux 云容器不是那台 Mac，且出网受限 —— 所有命令都没在真机跑过。文档里明确写「凡与实际输出不符，一律以终端为准」。

**自检抓到的回归**：债务规则的用例还钉在旧起算日的日历上，`--check-all` 当场报 3 条失败。按新日历重钉（含「周日不计入断链」那条）。这正是当初把用例写进 lint 的用途。

**下一步**

1. owner 在 Mac 上照手册第 1–2 章装环境（第 0 周，09-24～09-27），把和文档对不上的地方记下来 —— **第一版必然有要修的，手册的价值在第二版**。
2. 09-28 周一正式开课，W1 D1 是 ENGINEERING.md 前两节。
3. Lark 推送仍未接通（见 `schedule/HANDOFF.md`），**但它不是开工的前提** —— `render.py --preview` 的文本可以直接抄进 Lark 自己发给自己。
4. 课程表仍只有 W1；W2–W8 的 42 个单元等 owner 确认粒度后补。
