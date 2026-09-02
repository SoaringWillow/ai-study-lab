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
