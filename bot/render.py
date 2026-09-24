#!/usr/bin/env python3
"""Compile schedule/*.yaml into a Lark interactive card for one study day.

Pure: reads yaml, writes JSON or text. No network. That is deliberate — the
whole card can be developed and checked without Lark credentials, and the only
thing send.py adds is the HTTP call.

  render.py --date 2026-09-02 --preview     # human-readable
  render.py --date 2026-09-02               # card JSON
  render.py --slot evening                  # defaults to tomorrow
  render.py --check-all                     # lint every unit in curriculum
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.parse
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEDULE = ROOT / "schedule"

# Weekday kinds from PLAN.md §7, used only by --check-all to flag units whose
# `kind` does not match their weekday. W1 has a documented exception.
EXPECTED_KIND = {
    1: "课程主线", 2: "课程主线", 3: "论文日",
    4: "课程主线", 5: "市场日", 6: "动手日",
}
KIND_COLOR = {
    "课程主线": "blue", "论文日": "purple",
    "市场日": "turquoise", "动手日": "orange",
}
DEBT_BREAK = 3  # PLAN.md §7 rule 3: >=3 days broken -> shrink scope, never catch up


def load() -> tuple[dict, dict, dict]:
    def read(name: str) -> dict:
        return yaml.safe_load((SCHEDULE / name).read_text(encoding="utf-8")) or {}

    return read("curriculum.yaml"), read("resources.yaml"), read("state.yaml")


def repo_slug() -> str:
    """owner/repo, for building issue links."""
    if env := os.environ.get("GITHUB_REPOSITORY"):
        return env
    try:
        url = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "SoaringWillow/ai-study-lab"
    return url.removesuffix(".git").split("github.com")[-1].lstrip("/:")


# ---------- schedule arithmetic ----------

def week_and_day(date: dt.date, start: dt.date) -> tuple[int, int]:
    """Week number (1-based, aligned to the start date) and ISO weekday."""
    return (date - start).days // 7 + 1, date.isoweekday()


def find_unit(curriculum: dict, week: int, day: int) -> dict | None:
    for u in curriculum.get("units", []):
        if u["week"] == week and u["day"] == day:
            return u
    return None


def scheduled_dates(curriculum: dict, start: dt.date, lo: dt.date, hi: dt.date):
    """Dates in [lo, hi) that have a unit. Used to count broken days."""
    d = lo
    while d < hi:
        w, wd = week_and_day(d, start)
        if find_unit(curriculum, w, wd):
            yield d
        d += dt.timedelta(days=1)


def previous_unit(curriculum: dict, date: dt.date, start: dt.date) -> dict | None:
    """Walk back up to 14 days for the last scheduled unit — used for `recall`."""
    for back in range(1, 15):
        d = date - dt.timedelta(days=back)
        if d < start:
            return None
        u = find_unit(curriculum, *week_and_day(d, start))
        if u:
            return u
    return None


def today_cst() -> dt.date:
    return dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).date()


def broken_days(curriculum: dict, state: dict, date: dt.date, start: dt.date,
                today: dt.date) -> int:
    """Scheduled days already past that produced no artifact.

    Bounded by `today`, not by `date`: the evening card plans tomorrow, and a
    day that has not happened yet is not a broken day.
    """
    last = state.get("last_output_date")
    lo = start if last is None else dt.date.fromisoformat(str(last)) + dt.timedelta(days=1)
    hi = min(date, today)
    return len(list(scheduled_dates(curriculum, start, lo, hi))) if lo < hi else 0


# ---------- context ----------

def issue_url(slug: str, date: dt.date, unit: dict, status: str, ask: str) -> str:
    """Prefilled daily-log issue. Field names must match .github/ISSUE_TEMPLATE/daily-log.yml."""
    label = {"done": "交产出", "stuck": "卡住了", "degraded": "20 分钟版"}[status]
    q = urllib.parse.urlencode({
        "template": "daily-log.yml",
        "labels": "daily-log",
        "title": f"{date.isoformat()} · {label} · {unit['topic']}",
        "unit": f"W{unit['week']} D{unit['day']} · {unit['kind']} · {unit['topic']}",
        "answer": ask if status != "degraded" else f"（20 分钟版）{unit.get('fallback', '')}",
    })
    return f"https://github.com/{slug}/issues/new?{q}"


def resource_url(resource: dict, slug: str) -> str:
    """Absolute, tappable URL. Repo-relative paths become GitHub blob links —
    a button whose href is `./ENGINEERING.md` opens nothing on a phone."""
    url = str(resource["url"])
    if not url.startswith("./"):
        return url
    branch = os.environ.get("REPO_BRANCH", "main")
    path = urllib.parse.quote(url[2:].rstrip("/"))
    kind = "tree" if url.endswith("/") else "blob"
    return f"https://github.com/{slug}/{kind}/{branch}/{path}"


def build(date: dt.date, slot: str, today: dt.date | None = None) -> dict[str, Any]:
    curriculum, resources, state = load()
    start = dt.date.fromisoformat(str(state["start_date"]))
    today = today or today_cst()
    week, day = week_and_day(date, start)
    unit = find_unit(curriculum, week, day)
    slug = repo_slug()

    ctx: dict[str, Any] = {
        "date": date, "slot": slot, "week": week, "day": day,
        "unit": unit, "resources": resources, "slug": slug,
        "rest": day == 7, "broken": 0, "degraded": False,
    }
    if date < start:
        ctx["before_start"] = True
        return ctx
    if unit is None:
        return ctx  # Sunday, or curriculum not yet extended this far

    ctx["broken"] = broken_days(curriculum, state, date, start, today)
    ctx["degraded"] = ctx["broken"] >= DEBT_BREAK

    # recall: explicit, else auto-derived from the previous unit's ask
    if unit.get("recall"):
        ctx["recall"] = unit["recall"]
    elif prev := previous_unit(curriculum, date, start):
        ctx["recall"] = f"先不看资料，回答上次那一问：{prev['output']['ask']}"
    else:
        ctx["recall"] = "不看资料，写下上次学到的三点。"

    ask = unit["output"]["ask"]
    ctx["ask"] = ask
    ctx["output_file"] = unit["output"]["file"].replace("{date}", date.isoformat())
    # One button per distinct resource — two deep items citing the same file
    # must not produce two identical buttons.
    links: list[tuple[str, str]] = []
    for i in unit["deep"]:
        if (r := resources.get(i["res"])) is None:
            continue
        pair = (r["title"], resource_url(r, slug))
        if pair not in links:
            links.append(pair)
    ctx["links"] = links
    ctx["buttons"] = {
        s: issue_url(slug, date, unit, s, ask) for s in ("done", "stuck", "degraded")
    }
    return ctx


# ---------- rendering ----------

def _weekday_cn(date: dt.date) -> str:
    return "一二三四五六日"[date.isoweekday() - 1]


def _body_lines(ctx: dict) -> list[str]:
    """The three time boxes, shared by the card and the text preview."""
    unit = ctx["unit"]
    if ctx["degraded"]:
        return [
            f"**断链 {ctx['broken']} 天 —— 按债务规则不补课，直接缩小范围。**",
            f"今天只做这个（约 30 分钟）：{unit.get('fallback', unit['topic'])}",
            f"产出仍然要交：`{ctx['output_file']}`",
        ]
    total = sum(i["minutes"] for i in unit["deep"])
    out_min = unit["output"].get("minutes", 20)
    lines = [f"**回忆 10′** {ctx['recall']}", f"**深工作 {total}′**"]
    lines += [
        f"　{n}. {ctx['resources'][i['res']]['title']} —— {i['span']}（{i['minutes']}′）"
        for n, i in enumerate(unit["deep"], 1)
    ]
    lines += [f"**输出 {out_min}′** 写进 `{ctx['output_file']}`", f"　要回答：{ctx['ask']}"]
    if hb := unit.get("handbook"):
        lines.append(f"_手册：{hb}_")
    return lines


def as_text(ctx: dict) -> str:
    d = ctx["date"]
    head = f"{d.isoformat()} 周{_weekday_cn(d)}"
    if ctx.get("before_start"):
        return f"{head}\n计划起算日是 2026-09-02，这天在起算日之前。"
    if ctx["rest"]:
        return (f"{head} · W{ctx['week']} 复盘日\n"
                "30 分钟：本周实际产出几件？卡点属于哪一层？下周要砍什么？其余真的休息。")
    if ctx["unit"] is None:
        return (f"{head} · W{ctx['week']}\n课程表还没排到这周 —— "
                "去 replan issue 里回一句话，下次会话我补上。")
    u = ctx["unit"]
    title = f"{head} · W{ctx['week']} D{ctx['day']} · {u['kind']}"
    if ctx["slot"] == "evening":
        title = "【明日安排】" + title
    out = [title, u["topic"], ""] + _body_lines(ctx) + [""]
    out += [f"资源：{t} → {url}" for t, url in ctx["links"]]
    if ctx["slot"] == "morning":
        out += ["", "回执（三个按钮都要写一行字，没有纯打勾的选项）:"]
        for k, v in ctx["buttons"].items():
            # Prefilled issue URLs are ~1KB of percent-encoding; showing them in
            # full buries the actual plan. --urls prints them for link testing.
            out.append(f"  {k}: {v if ctx.get('show_urls') else v[:72] + '…'}")
    return "\n".join(out)


def _md(content: str) -> dict:
    return {"tag": "div", "text": {"tag": "lark_md", "content": content}}


def as_card(ctx: dict) -> dict:
    """Lark interactive card (schema 1.0).

    The exact schema could not be verified from this environment (the egress
    proxy blocks open.larksuite.com / open.feishu.cn), so card construction is
    kept in this one function: if the first live send from a networked machine
    rejects it, this is the only place to fix.
    """
    d = ctx["date"]
    if ctx["rest"] or ctx["unit"] is None or ctx.get("before_start"):
        return {
            "config": {"wide_screen_mode": True},
            "header": {"template": "grey",
                       "title": {"tag": "plain_text",
                                 "content": f"{d.isoformat()} 周{_weekday_cn(d)}"}},
            "elements": [_md(as_text(ctx))],
        }

    u = ctx["unit"]
    prefix = "明日安排" if ctx["slot"] == "evening" else "今日开工"
    elements: list[dict] = []

    if ctx["degraded"]:
        elements.append(_md(f"⚠️ **断链 {ctx['broken']} 天** · 已自动切成 20 分钟版"))
    elif ctx["broken"]:
        elements.append(_md(f"欠 {ctx['broken']} 天 · 按债务规则**不补课**，直接继续"))

    total = (30 if ctx["degraded"] else
             sum(i["minutes"] for i in u["deep"]) + 10 + u["output"].get("minutes", 20))
    elements += [
        _md(f"**{u['topic']}**\n`W{ctx['week']} D{ctx['day']} · {u['kind']} · ⏱ {total} min`"),
        {"tag": "hr"},
        _md("\n".join(_body_lines(ctx))),
    ]

    if ctx["links"]:
        elements += [{"tag": "hr"}, {"tag": "action", "actions": [
            {"tag": "button", "text": {"tag": "plain_text", "content": f"打开 {t}"},
             "url": url, "type": "default"}
            for t, url in ctx["links"][:3]
        ]}]

    if ctx["slot"] == "morning":
        b = ctx["buttons"]
        elements.append({"tag": "action", "actions": [
            {"tag": "button", "text": {"tag": "plain_text", "content": "✅ 交产出"},
             "url": b["done"], "type": "primary"},
            {"tag": "button", "text": {"tag": "plain_text", "content": "⚠️ 卡住了"},
             "url": b["stuck"], "type": "danger"},
            {"tag": "button", "text": {"tag": "plain_text", "content": "⏭ 20 分钟版"},
             "url": b["degraded"], "type": "default"},
        ]})
        elements.append(_md("三个按钮都要写一行字 —— 回执是产物，不是一个勾。"))

    return {
        "config": {"wide_screen_mode": True},
        "header": {"template": KIND_COLOR.get(u["kind"], "blue"),
                   "title": {"tag": "plain_text",
                             "content": f"{prefix} · {d.strftime('%m-%d')} 周{_weekday_cn(d)}"}},
        "elements": elements,
    }


# ---------- lint ----------

def weekly_summary(week: int) -> dict[str, Any]:
    """What actually happened in one week, from state.yaml."""
    curriculum, resources, state = load()
    start = dt.date.fromisoformat(str(state["start_date"]))
    lo = start + dt.timedelta(days=(week - 1) * 7)
    hi = lo + dt.timedelta(days=7)

    rows = [r for r in (state.get("log") or [])
            if lo <= dt.date.fromisoformat(str(r["date"])) < hi]
    scheduled = len(list(scheduled_dates(curriculum, start, lo, hi)))
    produced = [r for r in rows if r["status"] in ("done", "degraded")]
    layers: dict[str, int] = {}
    for r in rows:
        if r.get("layer"):
            layers[r["layer"]] = layers.get(r["layer"], 0) + 1
    mins = sorted(r["minutes"] for r in rows if r.get("minutes"))

    return {
        "week": week, "scheduled": scheduled,
        "produced": len(produced),
        "degraded": sum(1 for r in produced if r["status"] == "degraded"),
        "stuck": sum(1 for r in rows if r["status"] == "stuck"),
        "layers": sorted(layers.items(), key=lambda kv: -kv[1]),
        "median_minutes": mins[len(mins) // 2] if mins else None,
        "next_topics": [
            u["topic"] for d in (1, 2, 3, 4, 5, 6)
            if (u := find_unit(curriculum, week + 1, d))
        ],
        "slug": repo_slug(),
    }


def weekly_lines(s: dict) -> list[str]:
    out = [f"**本周产出 {s['produced']}/{s['scheduled']} 天**"
           + (f"（其中 {s['degraded']} 天是 20 分钟版）" if s["degraded"] else "")]
    if s["stuck"]:
        out.append(f"卡住 {s['stuck']} 次")
    if s["layers"]:
        out.append("卡点分层：" + " · ".join(f"{k} ×{v}" for k, v in s["layers"]))
    if s["median_minutes"]:
        out.append(f"实际耗时中位数 {s['median_minutes']}′"
                   + ("（排得太满了，下周该砍）" if s["median_minutes"] > 100 else ""))
    if s["produced"] == 0:
        out.append("这周一件都没交 —— 按债务规则不补课，下周直接缩小范围继续。")
    if s["next_topics"]:
        out.append(f"\n**下周 W{s['week'] + 1}**")
        out += [f"　· {t}" for t in s["next_topics"]]
    else:
        out.append(f"\n课程表还没排到 W{s['week'] + 1} —— 在 replan issue 里回一句话。")
    return out


def replan_url(s: dict) -> str:
    q = urllib.parse.urlencode({
        "labels": "replan",
        "title": f"replan: W{s['week'] + 1}",
        "body": (
            f"W{s['week']} 实际产出 {s['produced']}/{s['scheduled']} 天，"
            f"卡住 {s['stuck']} 次。\n\n"
            "回答这三个问题就够了，Claude 下次会话据此改 curriculum.yaml：\n\n"
            "1. 哪天没做？为什么（没时间 / 没兴趣 / 卡住了 / 排得太满）？\n"
            "2. 卡点集中在哪一层？需要为它单独排一天吗？\n"
            f"3. W{s['week'] + 1} 要不要砍范围？砍范围不是失败（PLAN.md §13）。\n"
        ),
    })
    return f"https://github.com/{s['slug']}/issues/new?{q}"


def as_weekly_card(s: dict) -> dict:
    return {
        "config": {"wide_screen_mode": True},
        "header": {"template": "wathet",
                   "title": {"tag": "plain_text", "content": f"W{s['week']} 周报 · 复盘 30 分钟"}},
        "elements": [
            _md("\n".join(weekly_lines(s))),
            {"tag": "hr"},
            {"tag": "action", "actions": [{
                "tag": "button",
                "text": {"tag": "plain_text", "content": f"回一句话 → 排 W{s['week'] + 1}"},
                "url": replan_url(s), "type": "primary"}]},
        ],
    }


def _check_debt_rule(curriculum: dict, start: dt.date) -> list[str]:
    """The debt rule is the one piece of logic with real consequences (it can
    silently shrink every card), so pin its behaviour here rather than in a
    separate test file.

    Cases: (last_output_date, target date, today) -> expected broken days.
    """
    # Dates are tied to the start date in state.yaml (2026-09-28, Monday), so
    # these move whenever the start date does — which is the point: a stale
    # calendar should fail loudly rather than silently mis-count debt.
    d = dt.date.fromisoformat
    cases = [
        # first day, nothing logged yet: no debt, and no accusation
        (None, "2026-09-28", "2026-09-28", 0),
        # planning tomorrow on day one: tomorrow has not happened -> still 0
        (None, "2026-09-29", "2026-09-28", 0),
        # logged yesterday, nothing owed
        ("2026-09-30", "2026-10-01", "2026-10-01", 0),
        # logged on day one, then went quiet: 09-29 and 09-30 missed
        ("2026-09-28", "2026-10-01", "2026-10-01", 2),
        # never logged all week; Sunday 10-04 has no unit and must not count
        (None, "2026-10-05", "2026-10-05", 6),
    ]
    problems = []
    for last, date, today, expected in cases:
        got = broken_days(curriculum, {"last_output_date": last},
                          d(date), start, d(today))
        if got != expected:
            problems.append(
                f"debt rule: last={last} date={date} today={today} "
                f"-> {got}, expected {expected}")
    return problems


def check_all() -> int:
    curriculum, resources, state = load()
    start = dt.date.fromisoformat(str(state["start_date"]))
    units, problems = curriculum.get("units", []), []
    seen: set[tuple[int, int]] = set()

    for u in units:
        tag = f"W{u.get('week')} D{u.get('day')}"
        key = (u.get("week"), u.get("day"))
        if key in seen:
            problems.append(f"{tag}: duplicate unit")
        seen.add(key)
        if not (1 <= u.get("day", 0) <= 6):
            problems.append(f"{tag}: day must be 1..6 (7 = rest, no unit)")
        for field in ("topic", "kind", "deep", "output"):
            if not u.get(field):
                problems.append(f"{tag}: missing `{field}`")
        if not u.get("fallback"):
            problems.append(f"{tag}: missing `fallback` (needed by the debt rule)")
        for i in u.get("deep", []):
            if i.get("res") not in resources:
                problems.append(f"{tag}: unknown resource id `{i.get('res')}`")
            if not i.get("span") or not i.get("minutes"):
                problems.append(f"{tag}: deep item needs both `span` and `minutes`")
        mins = sum(i.get("minutes", 0) for i in u.get("deep", []))
        budget = 240 if u.get("long_block") else 60
        if mins > budget:
            problems.append(f"{tag}: deep work {mins}′ over the {budget}′ box")
        for field in ("file", "ask"):
            if not (u.get("output") or {}).get(field):
                problems.append(f"{tag}: output.{field} missing")
        expected = EXPECTED_KIND.get(u.get("day"))
        if expected and u.get("kind") != expected and u.get("week") != 1:
            problems.append(f"{tag}: kind `{u.get('kind')}` != `{expected}` for that weekday")

    # every week present must cover days 1..6
    for week in sorted({u["week"] for u in units}):
        if missing := {1, 2, 3, 4, 5, 6} - {u["day"] for u in units if u["week"] == week}:
            problems.append(f"W{week}: missing day(s) {sorted(missing)}")

    # every unit must render
    for u in units:
        offset = (u["week"] - 1) * 7
        for k in range(7):
            d = start + dt.timedelta(days=offset + k)
            if d.isoweekday() == u["day"]:
                try:
                    # today=d keeps the lint deterministic (no accrued debt)
                    as_card(build(d, "morning", today=d))
                    as_text(build(d, "evening", today=d))
                except Exception as exc:  # noqa: BLE001 - report, don't crash the lint
                    problems.append(f"W{u['week']} D{u['day']} ({d}): render failed: {exc}")
                break

    for r_id, r in resources.items():
        url = str(r.get("url", ""))
        if r.get("kind") == "local":
            if not url.startswith("./"):
                problems.append(f"resource `{r_id}`: local resource must start with ./")
        elif not url.startswith("http"):
            problems.append(f"resource `{r_id}`: non-local resource without an http url")

    problems += _check_debt_rule(curriculum, start)

    print(f"{len(units)} units, {len(resources)} resources")
    for p in problems:
        print(f"  ✗ {p}")
    if unverified := [i for i, r in resources.items() if r.get("unverified")]:
        print(f"  ! 未实测链接（用到前先点一下）: {', '.join(unverified)}")
    print("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--date", help="target study date, YYYY-MM-DD")
    p.add_argument("--slot", choices=("morning", "evening"), default="morning")
    p.add_argument("--preview", action="store_true", help="human-readable text")
    p.add_argument("--urls", action="store_true", help="with --preview, print full issue URLs")
    p.add_argument("--check-all", action="store_true", help="lint the curriculum")
    p.add_argument("--today", help="override today's date (for testing the debt rule)")
    p.add_argument("--weekly", action="store_true", help="weekly report card")
    p.add_argument("--week", type=int, help="with --weekly; defaults to the current week")
    a = p.parse_args()

    if a.check_all:
        return check_all()

    if a.weekly:
        _, _, state = load()
        start = dt.date.fromisoformat(str(state["start_date"]))
        today = dt.date.fromisoformat(a.today) if a.today else today_cst()
        s = weekly_summary(a.week or week_and_day(today, start)[0])
        print("\n".join([f"W{s['week']} 周报"] + weekly_lines(s) +
                        ["", f"replan: {replan_url(s)}"]) if a.preview
              else json.dumps(as_weekly_card(s), ensure_ascii=False, indent=2))
        return 0

    today = dt.date.fromisoformat(a.today) if a.today else today_cst()
    # No date given: morning plans today, evening plans tomorrow.
    date = (dt.date.fromisoformat(a.date) if a.date
            else today + dt.timedelta(days=1) if a.slot == "evening" else today)

    ctx = build(date, a.slot, today=today)
    ctx["show_urls"] = a.urls
    print(as_text(ctx) if a.preview
          else json.dumps(as_card(ctx), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
