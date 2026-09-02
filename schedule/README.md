# 课程表与每日简报

> **要在本机接手、把 Lark 那条路打通？看 [HANDOFF.md](./HANDOFF.md)** —— 拉分支、建 Lark 应用、第一次真发、配 cron，以及给本地 Claude 会话的第一句话。

`PLAN.md` 是给人读的战略；这一层是它的**编译产物** —— 把 12 个月路线切成一个个「打开就能开始」的 90 分钟单元，每天两次推到 Lark。

**分层判断**：仓库当编译器（内容、每周重排、版本留痕），Lark 当运行时（推送、提醒）。课程表**不放在 Lark 里** —— 它需要被反复重排（多维表格的自动化没有判断力）、需要 `git log` 记住「我当时为什么砍掉这一讲」、并且不能随一个群或一个应用的停用而消失。

## 三个文件

| 文件 | 是什么 | 谁改 |
|---|---|---|
| `curriculum.yaml` | **真相源。** 每个 90 分钟单元：主题、资源与精确范围、时间盒、产出、降级版 | 每周日的 replan 由 Claude 改；你也可以手改 |
| `resources.yaml` | 资源库，`id → {标题, url}`。课程表只引 id —— 链接失效只改一处 | 谁发现谁改 |
| `state.yaml` | 运行时状态：起算日、`last_output_date`、每日日志 | `bot/ingest.py` 自动写 |

## 每天怎么用

1. **前一晚 21:30** 收到「明日安排」卡 —— 资料链接头一晚就点开，第二天零启动摩擦。
2. **当天 06:30** 收到「今日开工」卡 —— 按三段时间盒做。
3. 做完点卡片底部三个按钮之一，都会打开一个**预填好的 GitHub issue**：

| 按钮 | 什么时候点 |
|---|---|
| ✅ 交产出 | 正常完成。答那一问，贴产出路径 |
| ⚠️ 卡住了 | 卡住了。选「卡在哪一层」—— 这一栏会汇总成分层统计 |
| ⏭ 20 分钟版 | 低能量日。**不算断链** —— 链条不断比进度重要 |

**没有纯打勾的「完成」按钮，这是刻意的。** `PLAN.md` 反模式第一条是「只看视频不敲键盘」；一个提醒机器人最容易退化成「已读即完成」—— 连点 30 天卡片、感觉良好、什么都没学会。所以三个按钮全都要写一行字：**回执必须是 artifact，不是一个勾。**

## 债务规则是机器执行的

`state.yaml` 记 `last_output_date`，渲染时按 `PLAN.md` §7 硬规则 3 自动处理：

| 断链 | 卡片行为 |
|---|---|
| 0 天 | 正常 90 分钟 |
| 1–2 天 | 顶部标「欠 N 天 · 不补课，直接继续」，内容不变 |
| ≥3 天 | **自动切成 30 分钟的 `fallback` 版** |

「先把落下的补回来」是弃坑头号原因 —— 所以补课这个选项在系统里根本不存在。断链只按**已经过去**的日子算：晚上那张卡规划的是明天，明天还没发生，不算欠。

## 每周回路

每周日 `weekly-replan.yml`：汇总本周 issues → 更新 `state.yaml` → 推周报卡 → 开一个 `replan: Wn` issue。你在那个 issue 里回一句话（哪天没做、卡在哪、要不要砍范围），下次会话 Claude 据此改 `curriculum.yaml`。

**日常靠按钮（摩擦接近零），每周靠一个 issue（那次才需要判断）。**

## 改课程表

```bash
# 改完必跑：校验字段、资源 id、时间盒预算、周次覆盖、债务规则自检
python3 bot/render.py --check-all

# 看某天渲染成什么样
python3 bot/render.py --date 2026-09-03 --slot evening --preview
python3 bot/render.py --date 2026-09-03 --slot morning --preview --urls   # 带完整 issue 链接

# 测债务降级（不用改 state.yaml）
python3 bot/render.py --date 2026-09-08 --today 2026-09-08 --preview
```

`--check-all` 会拦住的错：资源 id 打错、`fallback` 漏写（债务规则要用）、深工作超时间盒（普通日 60′、动手日 240′）、某周缺天、`kind` 和星期对不上。

### 字段

```yaml
- week: 1          # 周次，按起算日对齐（W1 = 2026-09-02 至 09-08）
  day: 4           # ISO 星期，1=周一 … 6=周六。7=周日不排单元
  kind: 课程主线    # 课程主线 | 论文日 | 市场日 | 动手日
  topic: ...
  recall: ...      # 可省略 —— 省略时自动取上一单元的 output.ask
  deep:            # 10–70 分钟。span 精确到集数/章节，不写「看一下线代」
    - {res: 3b1b-linalg, span: 第 3 集「线性变换与矩阵」, minutes: 11}
  output:
    file: notes/{date}.md     # {date} 会替换成当天日期
    ask: ...                  # 当天 issue 里要回答的那一句，也是唯一能关闭这一天的东西
  fallback: ...    # 20–30 分钟降级版（低能量日 / 断链 ≥3 天）
  long_block: true # 仅动手日：时间盒放宽到 240 分钟
```

## 已知的坑

- **`resources.yaml` 里标了 `unverified:` 的链接没实测过** —— 本会话的出网代理封了那几个域名。用到那一周之前先点一下，坏了就改。`--check-all` 会把它们列出来提醒。
- **Lark 卡片 schema 没能对着官方文档核对**（`open.larksuite.com` / `open.feishu.cn` 在写这套东西的机器上都是 403）。卡片构造集中在 `bot/render.py` 的 `as_card()` 一个函数里 —— 第一次真发被拒的话，只改那里。
- **GitHub Actions 的 cron 会延迟**（高峰期几分钟到半小时），所以排的是 21:20 / 06:20，留 10 分钟缓冲。另外仓库连续 60 天无提交会让 cron 自动停用 —— 每周日的 replan 提交顺带解决了这件事。

## 起步（第一次配）

1. Lark 建自建应用，开「发送单聊消息给用户」权限，发布启用，把机器人加为联系人。
2. **先在能连 Lark 的机器上真发一次**（不要在 Action 里首调）：
   ```bash
   export LARK_APP_ID=... LARK_APP_SECRET=... LARK_RECEIVE_ID=你的邮箱
   export LARK_DOMAIN=open.larksuite.com   # 国内租户用 open.feishu.cn
   python3 bot/send.py --slot morning
   ```
   看两件事：返回 `code: 0`；**手机上卡片的实际排版**（按钮换行、中文断行、深色模式）—— 这一步只有真机能验。
3. 通了之后在 GitHub 配 secrets `LARK_APP_ID` / `LARK_APP_SECRET` / `LARK_RECEIVE_ID` 和 variable `LARK_DOMAIN`。
4. 手动跑一次 `daily-brief` workflow（`workflow_dispatch`，可先勾 `dry_run`）确认 runner 侧也通，然后就交给 cron。

推送通不通，不该成为今天不开工的理由 —— `--preview` 出来的文本可以直接抄进 Lark 自己发给自己。
