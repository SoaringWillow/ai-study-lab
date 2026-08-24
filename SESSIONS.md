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
