# 本地接手说明

这份文件是给「在 Mac 上开一个本地 Claude Code 会话继续干」准备的。云端会话把不需要联网的部分全做完了，剩下的必须在能连 Lark 的机器上做。

**当前状态一句话**：渲染、债务规则、回执表单、两个 workflow 全部写完并自检通过；**课程表只有 W1（6 个单元）**，Lark 一条消息都还没真发过。

---

## 0. 为什么必须换到本地

云端会话的出网代理在 CONNECT 层就拒了 Lark：

```
open.larksuite.com  ->  403 CONNECT tunnel failed
open.feishu.cn      ->  403 CONNECT tunnel failed
```

装 CLI 没用，这是网络策略不是缺依赖。同理被封的还有 `arxiv.org`、`pytorch.org`、`docs.astral.sh`。另外那个云端容器**不是你的 Mac** —— 它没有 `/Users` 目录，`~/Documents/WorldEngine Claude folder` 里的 Lark MCP 够不到。

所以：**内容和逻辑在云端做（已完成），真发和真机验证在本地做（待做）。**

---

## 1. 拉下来

```bash
cd ~/Documents          # 或你放仓库的地方
git clone https://github.com/SoaringWillow/ai-study-lab.git
cd ai-study-lab
git checkout claude/session-003-handoff-plan-s1nqt8
```

> 分支名就是这个 —— 不是方案里提过的 `claude/lark-daily-brief`（那个没建，harness 指定了前者）。

已经 clone 过的话：

```bash
git fetch origin claude/session-003-handoff-plan-s1nqt8
git checkout claude/session-003-handoff-plan-s1nqt8
git pull
```

---

## 2. 环境

只需要 `pyyaml`（HTTP 走标准库 `urllib`，刻意不引 `requests`）。

```bash
python3 -V                    # 需要 3.11+
python3 -c "import yaml" || pip3 install pyyaml
```

用 uv 的话：`uv venv --python 3.11 && source .venv/bin/activate && uv pip install pyyaml`

---

## 3. 先验不需要 Lark 的部分（应该全绿）

```bash
# 全量 lint：字段完整性、资源 id、时间盒预算、周次覆盖、债务规则自检
python3 bot/render.py --check-all
# 预期：6 units, 18 resources / 4 个 unverified 链接提醒 / OK

# 看某天渲染成什么样
python3 bot/render.py --date 2026-09-02 --slot morning --preview
python3 bot/render.py --date 2026-09-05 --slot evening --today 2026-09-02 --preview

# 打出将要发出的完整请求体，脱敏，不发送
python3 bot/send.py --date 2026-09-02 --slot morning --dry-run
```

这一步跑通就说明代码是好的，后面只剩凭据和 Lark 侧配置。

---

## 4. Lark 自建应用

在开放平台（国际版 `open.larksuite.com`，国内租户 `open.feishu.cn`）：

1. **创建自建应用**，记下「凭证与基础信息」里的 `App ID` 和 `App Secret`。
2. **添加「机器人」能力** —— 这一步漏了的话消息发不出去，报错会说应用没有机器人能力。
3. **权限管理**里开「以应用的身份发送消息」（scope 名类似 `im:message:send_as_bot`）。你说租户权限随便开，那就直接开全 `im` 相关的，省得来回试。
4. **发布版本**并等审批通过（你是管理员的话自审即可）。**没发布的应用调 API 会一直失败**，这是最常见的坑。
5. 在 Lark 客户端里搜应用名，**和这个机器人建立一次会话**（或把它加进一个群）。

### receive_id 用哪个

| 类型 | 值长什么样 | 说明 |
|---|---|---|
| `email` | 你的 Lark 账号邮箱 | 最省事，`send.py` 会自动识别（含 `@` 就当 email）。可能需要通讯录读取权限 |
| `open_id` | `ou_xxxx` | email 因权限失败时用这个。开放平台的 API 调试台里查得到 |
| `chat_id` | `oc_xxxx` | 发到群里。建一个只有你和机器人的群，需要的权限最少 |

`send.py` 按前缀自动判断；判断不对就显式设 `LARK_RECEIVE_TYPE`。

---

## 5. 第一次真发

```bash
export LARK_APP_ID=cli_xxxxxxxx
export LARK_APP_SECRET=xxxxxxxx
export LARK_RECEIVE_ID=你的Lark邮箱          # 或 ou_xxx / oc_xxx
export LARK_DOMAIN=open.larksuite.com       # 国内租户改成 open.feishu.cn

python3 bot/send.py --date 2026-09-02 --slot morning
```

成功长这样：

```
{"code":0,"msg":"success","data":{...}}
sent 2026-09-02 morning -> email:...
```

**看两件事**（第二件只有真机能验，云端渲染的 JSON 看不出来）：

1. `code` 是 `0`。
2. **手机上卡片的实际排版** —— 三个按钮会不会换行挤成一坨、中文断行难看不难看、深色模式下读不读得清。

### 报错怎么读

`code` 非 0 时 `msg` 会一起打出来，按 `msg` 提到的字段改。三个最可能的原因，按概率排：

| 现象 | 大概率原因 |
|---|---|
| 拿 token 就失败 | `app_id`/`app_secret` 错，或**应用没发布** |
| token 拿到了、发消息失败且 msg 提 receive_id | `receive_id` 或 `receive_id_type` 不匹配 → 换成 `open_id` 或 `chat_id` |
| msg 提 permission / scope | 权限没开，或开了但**没重新发布版本** |

**如果是卡片格式被拒**（msg 提 card / content / schema）：卡片构造全部集中在 `bot/render.py` 的 `as_card()` 一个函数里，只改那里。这套 schema 是照 1.0 的 `config` / `header` / `elements` 写的，但**没能对着官方文档核对过**（写它的机器连不上 Lark 文档站）—— 所以这是最可能需要改的地方，也是特意把它收在一个函数里的原因。

---

## 6. 接上定时器

真发通了之后：

1. GitHub 仓库 → Settings → Secrets and variables → Actions：
   - **Secrets**：`LARK_APP_ID`、`LARK_APP_SECRET`、`LARK_RECEIVE_ID`
   - **Variables**：`LARK_DOMAIN`
2. Actions 页面手动跑一次 `daily brief`（先勾 `dry_run` 看日志，再不勾真发一次），确认 runner 侧也通。
3. 之后 cron 自动跑：**21:20 明日安排 / 06:20 今日开工**（北京时间）。排早 10 分钟是因为 GitHub Actions 的 cron 高峰期会延迟。
4. `weekly replan` 每周日 21:00 自动跑，不用管。

> 注意：cron 只在**默认分支**上生效。所以这个分支合进 `main` 之后定时器才会真正开始跑；在分支上只能手动 `workflow_dispatch`。

---

## 7. 已完成 / 待做

**已完成**

- `schedule/curriculum.yaml` —— W1 六个单元，每个精确到集数/章节
- `schedule/resources.yaml` —— 18 个资源，arXiv 编号逐个核对过
- `bot/render.py` —— 渲染 + 债务规则 + `--check-all` lint（含债务规则的用例自检）
- `bot/send.py` —— 发送 + `--dry-run`
- `bot/ingest.py` —— issues + `notes/*.md` → `state.yaml`（解析用合成数据测过）
- 两个 workflow + 回执 issue 表单

**待做**

| # | 谁做 | 事 |
|---|---|---|
| 1 | **你** | 看 W1 六张卡的粒度：太细？太粗？时间估得准不准？ |
| 2 | Claude | 粒度确认后补完 **W2–W8 的 42 个单元** |
| 3 | **你** | Lark 应用 + 第一次真发（第 4–5 节） |
| 4 | **你** | 配 secrets + 手动触发 + 合进 main 开 cron |
| 5 | Claude | 顺手核掉 `resources.yaml` 里 4 个 `unverified` 链接（你本机能连） |

第 1 步是最便宜的纠错点 —— 第 5 周才发现排得太满，代价大得多。

---

## 8. 给本地 Claude 会话的第一句话

直接粘这段：

```
读 schedule/HANDOFF.md 和 SESSIONS.md 的 Session 004（含末尾「追加 · 每日 Lark 简报机器人」那节），
然后读 schedule/curriculum.yaml 和 bot/render.py。

先跑 python3 bot/render.py --check-all 确认环境没问题。

我要做三件事，按顺序：
1. 把 W1 六天的卡片渲染出来给我看，我确认粒度。
2. 帮我把 Lark 自建应用配通，第一次真发。你这边能连 Lark 和 arxiv，
   顺便把 resources.yaml 里标了 unverified 的 4 个链接核掉。
3. 粒度确认后补完 W2–W8 的 42 个单元。

注意 CLAUDE.md 的分界线：论文笔记、5 问的答案、预测内容、notes/ 正文都不许你代写。
课程表只给「读哪篇、在哪个文件交、交什么形式」。
```

---

## 9. 已知的坑

- **`resources.yaml` 里标 `unverified:` 的 4 个链接没实测过**（`pytorch-basics`、`zero-to-hero`、`nanogpt`、`mujoco`）—— 云端封了那些域名。你本机能连，让本地 Claude 核一遍。`--check-all` 会把它们列出来。
- **Lark 卡片 schema 未对文档核对** —— 见第 5 节。
- **cron 只在默认分支生效**，且仓库连续 60 天无提交会被 GitHub 自动停用定时任务；每周日 replan 的那次 commit 顺带解决了后者。
- **债务规则只按已经过去的日子算**。晚上那张卡规划的是明天，明天还没发生，所以不算欠 —— 这是一个修过的 bug，别改回去（`bot/render.py` 里 `broken_days()` 的 `hi = min(date, today)`，`--check-all` 有用例钉住）。
- **卡片上没有纯打勾的「完成」按钮，这是刻意的。** 三个按钮全部通向要写一行字的 issue。理由见 `schedule/README.md` —— 一个能靠点一下关闭的提醒机器人，会退化成「已读即完成」。别为了方便加回一个勾。
