#!/usr/bin/env python3
"""
Criterion 4, three trials: every appeal is recorded and changes status.

run_eval.py can only send texts, and an appeal needs a content_id from a real
submission first — so this does submit → appeal → read the log, per trial:

    python app.py                       # in one terminal
    python check_appeals.py --label before

A trial passes when 5 of 5 appeals return 200 + under_review, each has a new
appeal entry in the log with the reasoning, the original decided entry is
still there unchanged, and an unknown content_id gets a 404 with no entry.
"""

import argparse
import datetime as dt

import requests

import audit
import config

URL = f"http://{config.HOST}:{config.PORT}"
TEXT = ("The bus to campus takes forty minutes if nothing goes wrong, and something always goes wrong. "
        "Last week a guy got on with a bike and argued with the driver about where to put it.")


def trial(n: int) -> tuple[bool, str]:
    ok = 0
    for i in range(5):
        creator = f"appeal_t{n}_{i}"
        sub = requests.post(f"{URL}/submit", json={"text": TEXT, "creator_id": creator}).json()
        cid = sub["content_id"]
        before = [e for e in audit.entries_for(cid) if e.get("status") == "decided"]
        reason = f"I wrote this myself (trial {n}, appeal {i})."
        r = requests.post(f"{URL}/appeal", json={"content_id": cid, "reasoning": reason})
        entries = audit.entries_for(cid)
        appeals = [e for e in entries if e.get("event") == "appeal" and e.get("reasoning") == reason]
        decided = [e for e in entries if e.get("status") == "decided"]
        if (r.status_code == 200 and r.json().get("status") == "under_review"
                and len(appeals) == 1 and decided == before and len(decided) == 1):
            ok += 1

    bogus = f"no-such-id-{n}"
    r = requests.post(f"{URL}/appeal", json={"content_id": bogus, "reasoning": "x"})
    unknown_ok = r.status_code == 404 and not audit.entries_for(bogus)
    return ok == 5 and unknown_ok, f"{ok}/5 appeals recorded, unknown id → {r.status_code}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="")
    args = parser.parse_args()

    lines = []
    for n in (1, 2, 3):
        passed, detail = trial(n)
        lines.append(f"| {n} | {detail} | {'PASS' if passed else 'FAIL'} |")
        print(lines[-1])

    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    path = config.RESULTS_DIR / f"appeal_check_{stamp}{'_' + args.label if args.label else ''}.md"
    path.write_text(
        "# Criterion 4 — appeals, three trials\n\n- Produced by: `check_appeals.py::main`\n\n"
        "| Trial | Result | Verdict |\n|---|---|---|\n" + "\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
