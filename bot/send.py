#!/usr/bin/env python3
"""Send one rendered card to Lark.

  send.py --slot morning --dry-run     # print the exact request, send nothing
  send.py --slot morning               # actually send

Config comes from the environment (never from the repo):
  LARK_APP_ID, LARK_APP_SECRET, LARK_RECEIVE_ID
  LARK_DOMAIN       open.larksuite.com (international) | open.feishu.cn (国内)
  LARK_RECEIVE_TYPE optional; inferred from LARK_RECEIVE_ID when omitted

HTTP goes through stdlib urllib so the only dependency is pyyaml (pulled in by
render). Nothing here needs installing beyond that.

NOTE ON VERIFICATION: the two endpoint paths below could not be checked against
the official docs from the machine this was written on — its egress proxy
blocks open.larksuite.com and open.feishu.cn outright. They are the documented
v3/v1 paths; if the first live send returns a non-zero `code`, the request
shape is printed by --dry-run and the paths are the two constants below.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request

import render

TOKEN_PATH = "/open-apis/auth/v3/tenant_access_token/internal"
MESSAGE_PATH = "/open-apis/im/v1/messages"


def infer_receive_type(receive_id: str) -> str:
    if "@" in receive_id:
        return "email"
    if receive_id.startswith("ou_"):
        return "open_id"
    if receive_id.startswith("oc_"):
        return "chat_id"
    return "user_id"


def post(url: str, payload: dict, token: str | None = None) -> dict:
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        # Lark puts a machine-readable code in the body even on 4xx; surface it
        # rather than a bare stack trace.
        body = exc.read().decode("utf-8", "replace")
        raise SystemExit(f"HTTP {exc.code} from {url}\n{body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"cannot reach {url}: {exc.reason}") from exc


def tenant_token(domain: str, app_id: str, app_secret: str) -> str:
    out = post(f"https://{domain}{TOKEN_PATH}",
               {"app_id": app_id, "app_secret": app_secret})
    if out.get("code") != 0:
        raise SystemExit(f"token failed: code={out.get('code')} msg={out.get('msg')}")
    return out["tenant_access_token"]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--date", help="target study date, YYYY-MM-DD")
    p.add_argument("--slot", choices=("morning", "evening"), default="morning")
    p.add_argument("--weekly", action="store_true", help="send the weekly report instead")
    p.add_argument("--dry-run", action="store_true",
                   help="print the request and exit; secrets redacted")
    a = p.parse_args()

    today = render.today_cst()
    date = (dt.date.fromisoformat(a.date) if a.date
            else today + dt.timedelta(days=1) if a.slot == "evening" else today)
    if a.weekly:
        _, _, state = render.load()
        start = dt.date.fromisoformat(str(state["start_date"]))
        week = render.week_and_day(today, start)[0]
        card = render.as_weekly_card(render.weekly_summary(week))
        label = f"W{week} weekly"
    else:
        card = render.as_card(render.build(date, a.slot, today=today))
        label = f"{date} {a.slot}"

    # `or`, not a get() default: CI passes vars.LARK_DOMAIN as an EMPTY string
    # when the variable is unset, which a default value would never see.
    domain = os.environ.get("LARK_DOMAIN") or "open.larksuite.com"
    receive_id = os.environ.get("LARK_RECEIVE_ID", "")
    receive_type = os.environ.get("LARK_RECEIVE_TYPE") or (
        infer_receive_type(receive_id) if receive_id else "email")
    url = f"https://{domain}{MESSAGE_PATH}?receive_id_type={receive_type}"
    body = {
        "receive_id": receive_id,
        "msg_type": "interactive",
        # content is a JSON *string*, not a nested object
        "content": json.dumps(card, ensure_ascii=False),
    }

    if a.dry_run:
        print(f"POST {url}")
        print("Authorization: Bearer <tenant_access_token>")
        redacted = dict(body, receive_id=receive_id or "<LARK_RECEIVE_ID unset>")
        print(json.dumps(redacted, ensure_ascii=False, indent=2))
        print("\n--- card, expanded for reading ---")
        print(json.dumps(card, ensure_ascii=False, indent=2))
        return 0

    missing = [k for k in ("LARK_APP_ID", "LARK_APP_SECRET", "LARK_RECEIVE_ID")
               if not os.environ.get(k)]
    if missing:
        raise SystemExit(f"missing env: {', '.join(missing)} (use --dry-run to preview)")

    token = tenant_token(domain, os.environ["LARK_APP_ID"], os.environ["LARK_APP_SECRET"])
    out = post(url, body, token)
    print(json.dumps(out, ensure_ascii=False))
    if out.get("code") != 0:
        raise SystemExit(f"send failed: code={out.get('code')} msg={out.get('msg')}")
    print(f"sent {label} -> {receive_type}:{receive_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
