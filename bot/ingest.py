#!/usr/bin/env python3
"""Rebuild schedule/state.yaml from daily-log issues (plus notes/ as a safety net).

  ingest.py            # rewrite state.yaml
  ingest.py --dry-run  # print what it would write

Rebuilds the log from scratch every run rather than appending, so re-running it
is safe and an edited issue is picked up on the next pass.

The safety net matters: if you wrote notes/2026-09-03.md but forgot to file the
issue, the chain is NOT counted as broken. The debt rule exists to keep you
going, not to catch you out.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

import yaml

import render

STATUS_FROM_TITLE = {"交产出": "done", "卡住了": "stuck", "20 分钟版": "degraded"}
KEEPS_CHAIN = {"done", "degraded"}  # a 20-minute day still counts as unbroken
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def fetch_issues(slug: str, token: str | None) -> list[dict]:
    url = (f"https://api.github.com/repos/{slug}/issues"
           "?labels=daily-log&state=all&per_page=100")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError) as exc:
        print(f"warning: could not read issues ({exc}); using notes/ only",
              file=sys.stderr)
        return []


def parse_sections(body: str) -> dict[str, str]:
    """Issue forms render as `### <label>` followed by the value."""
    out, label = {}, None
    for line in (body or "").splitlines():
        if line.startswith("### "):
            label = line[4:].strip()
            out[label] = ""
        elif label:
            out[label] += line + "\n"
    return {k: v.strip() for k, v in out.items()}


def from_issues(issues: list[dict]) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for issue in issues:
        # Presence, not truthiness: the API's `pull_request` object can be
        # empty, and an empty dict is falsy.
        if "pull_request" in issue:
            continue
        title = issue.get("title") or ""
        if not (m := DATE_RE.search(title)):
            continue
        date = m.group(1)
        status = next((v for k, v in STATUS_FROM_TITLE.items() if k in title), "done")
        s = parse_sections(issue.get("body") or "")
        layer = s.get("卡在哪一层", "")
        row = {"date": date, "status": status, "issue": issue.get("number")}
        if status == "stuck" and layer and layer != "没卡住":
            row["layer"] = layer.split("（")[0]
        if minutes := s.get("实际花了多少分钟", "").strip():
            if minutes.isdigit():
                row["minutes"] = int(minutes)
        if evidence := s.get("产出在哪", "").strip():
            row["evidence"] = evidence.splitlines()[0][:120]
        # Newest issue for a date wins (the API returns newest first).
        rows.setdefault(date, row)
    return rows


def from_notes() -> dict[str, dict]:
    """notes/YYYY-MM-DD.md counts as an artifact even with no issue filed."""
    rows = {}
    for path in sorted((render.ROOT / "notes").glob("*.md")):
        if m := DATE_RE.fullmatch(path.stem):
            rows[m.group(1)] = {"date": m.group(1), "status": "done",
                                "evidence": f"notes/{path.name}"}
    return rows


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()

    slug = render.repo_slug()
    rows = from_notes()
    # Issues win over the notes/ fallback: they carry status, layer and minutes.
    rows.update(from_issues(fetch_issues(slug, os.environ.get("GITHUB_TOKEN"))))

    log = [rows[d] for d in sorted(rows)]
    chain = [r["date"] for r in log if r["status"] in KEEPS_CHAIN]

    state_path = render.SCHEDULE / "state.yaml"
    state = yaml.safe_load(state_path.read_text(encoding="utf-8")) or {}
    state["last_output_date"] = max(chain) if chain else None
    state["log"] = log

    text = yaml.safe_dump(state, allow_unicode=True, sort_keys=False, width=100)
    header = (
        "# Runtime state. Rewritten by bot/ingest.py from daily-log issues and\n"
        "# notes/*.md; safe to hand-edit, it will be rebuilt on the next run.\n"
        "# last_output_date: latest day that produced an artifact — a degraded\n"
        "# (20-minute) day counts, which is the point of having one.\n\n"
    )
    if a.dry_run:
        print(header + text)
        return 0
    state_path.write_text(header + text, encoding="utf-8")
    stuck = [r for r in log if r["status"] == "stuck"]
    print(f"{len(log)} logged day(s), {len(stuck)} stuck, "
          f"last artifact {state['last_output_date']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
