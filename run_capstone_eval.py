#!/usr/bin/env python3
"""
Run the five capstone criteria, three trials each.  <- UNIT 9, MILESTONE 5

    AI201_FAULT_INJECTION=1 python app.py      # in one terminal
    python run_capstone_eval.py --label before # in another
    python run_capstone_eval.py --label after

Unit 8's `run_eval.py` sends text and records what came back, leaving the
verdict to a person because a verdict depends on the criterion. These five
criteria are different: four of them are about the *log*, and what they ask is
arithmetic over records — exactly 30 records, 0 malformed lines, a median under
250 ms. So this runner computes the verdict too, reading its targets from
`capstone_targets.py` so the number it checks is the number in criteria.md.

It reads `logs/requests.jsonl` off the disk directly, which is sound because
the service runs on this machine. The durations it reports are the service's
own measurements, not timings taken from out here, so nothing in the numbers
is network or client overhead.

Criterion 7 needs a handler that raises, so the service must be started with
AI201_FAULT_INJECTION=1. Without it the runner says so and that criterion
cannot be judged.
"""

import argparse
import concurrent.futures
import datetime as dt
import json
import statistics
import sys

import capstone_targets as T
import config
import obs
import scenarios

DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"

SAMPLE = scenarios.STUDENT_VOICE[2]

BAD_BODIES = [
    ({}, "invalid_json_or_missing"),
    ({"creator_id": "cap_bad_missing"}, "missing_text"),
    ({"text": "    ", "creator_id": "cap_bad_spaces"}, "empty_text"),
    ({"text": 42, "creator_id": "cap_bad_number"}, "missing_text"),
    ({"text": SAMPLE}, "missing_creator_id"),
    ({"text": "word " * 4001, "creator_id": "cap_bad_huge"}, "text_too_long"),
]

REQUIRED = obs.REQUIRED_FIELDS


# ── reading the log ──────────────────────────────────────────────────────────

def record_count() -> int:
    return len(obs.read_records())


def raw_line_stats() -> tuple[int, int]:
    """(total non-blank lines, lines that don't parse) — criterion 9 needs both."""
    if not config.REQUEST_LOG.exists():
        return 0, 0
    total = malformed = 0
    for line in config.REQUEST_LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        total += 1
        try:
            json.loads(line)
        except json.JSONDecodeError:
            malformed += 1
    return total, malformed


def records_since(start: int) -> list[dict]:
    return obs.read_records()[start:]


# ── the five criteria ────────────────────────────────────────────────────────

def criterion_6(session, url, timeout):
    """Every request leaves exactly one complete record."""
    spec = T.TARGETS[6]
    before = record_count()
    stamp = dt.datetime.now().strftime("%H%M%S%f")[:12]

    content_ids = []
    sent = 0
    for i in range(20):  # 20 submissions
        response = session.post(f"{url}/submit", timeout=timeout,
                                json={"text": SAMPLE, "creator_id": f"c6_{stamp}_{i}"})
        sent += 1
        if response.status_code == 200:
            content_ids.append(response.json()["content_id"])

    for i, content_id in enumerate(content_ids[:3]):  # 3 appeals
        session.post(f"{url}/appeal", timeout=timeout,
                     json={"content_id": content_id, "reasoning": "I wrote this myself."})
        sent += 1
    for content_id in content_ids[:3]:  # 3 status reads
        session.get(f"{url}/content/{content_id}", timeout=timeout)
        sent += 1
    for _ in range(3):  # 3 health checks
        session.get(f"{url}/health", timeout=timeout)
        sent += 1
    session.get(f"{url}/no-such-route-{stamp}", timeout=timeout)  # 1 unmatched URL
    sent += 1

    new = records_since(before)
    incomplete = [r for r in new if any(f not in r for f in REQUIRED)]
    complete = len(new) - len(incomplete)

    return {
        "requests_sent": sent,
        "records_gained": len(new),
        "complete_records": complete,
        "incomplete_records": len(incomplete),
        "passed": (sent == spec["requests"]
                   and len(new) == spec["requests"]
                   and complete == spec["complete_records_required"]),
        "evidence": new[-2:],
    }


def criterion_7(session, url, timeout, fault_available):
    """A request that fails is recorded as having failed."""
    spec = T.TARGETS[7]
    before = record_count()

    statuses = []
    for body, _expected in BAD_BODIES:
        response = session.post(f"{url}/submit", json=body, timeout=timeout)
        statuses.append(response.status_code)

    raised = False
    if fault_available:
        try:
            response = session.post(f"{url}{T.FAULT_ROUTE}", json={}, timeout=timeout)
            statuses.append(response.status_code)
            raised = True
        except Exception:  # noqa: BLE001 — a dropped connection still counts as sent
            raised = True

    new = records_since(before)
    recorded_ok = [r for r in new if r.get("outcome") == "ok"]
    named_failure = [r for r in new if r.get("outcome") not in (None, "ok")]
    four_hundreds = [r for r in new if r.get("status") == 400]
    five_hundreds = [r for r in new if r.get("status") == 500]
    with_exception = [r for r in five_hundreds if r.get("exception")]

    return {
        "requests_sent": len(statuses),
        "fault_route_available": fault_available,
        "response_statuses": statuses,
        "records_gained": len(new),
        "recorded_as_failure": len(named_failure),
        "recorded_as_ok": len(recorded_ok),
        "status_400_records": len(four_hundreds),
        "status_500_records": len(five_hundreds),
        "500s_naming_exception": len(with_exception),
        "passed": (fault_available
                   and len(named_failure) == spec["failures_required"]
                   and len(recorded_ok) <= spec["max_recorded_ok"]
                   and len(four_hundreds) == 6
                   and len(with_exception) == 1
                   and raised),
        "evidence": new[-2:],
    }


def criterion_8(session, url, timeout):
    """A warm submission answers in under 250 ms."""
    spec = T.TARGETS[8]
    # One throwaway request first, so the model is certainly loaded and this
    # measures what the criterion says it measures.
    session.post(f"{url}/submit", timeout=timeout,
                 json={"text": SAMPLE, "creator_id": "c8_warmup"})

    before = record_count()
    stamp = dt.datetime.now().strftime("%H%M%S%f")[:12]
    for i in range(spec["runs"]):
        session.post(f"{url}/submit", timeout=timeout,
                     json={"text": SAMPLE, "creator_id": f"c8_{stamp}_{i}"})

    new = [r for r in records_since(before) if r.get("route") == "/submit"]
    durations = [r["duration_ms"] for r in new]
    if not durations:
        return {"passed": False, "note": "no /submit records found", "evidence": []}

    median = round(statistics.median(durations), 2)
    under = [d for d in durations if d < spec["per_run_ms_max"]]
    return {
        "runs": len(durations),
        "median_ms": median,
        "min_ms": round(min(durations), 2),
        "max_ms": round(max(durations), 2),
        "under_400ms": len(under),
        "mean_model_signal_ms": round(statistics.mean(
            [r["stages"].get("model_signal", 0) for r in new]), 2),
        "passed": (median < spec["median_ms_max"]
                   and len(under) >= spec["per_run_min_passing"]
                   and len(durations) == spec["runs"]),
        "evidence": new[-2:],
    }


def criterion_9(session_factory, url, timeout):
    """The log survives ten times the normal rate."""
    spec = T.TARGETS[9]
    before = record_count()
    lines_before, malformed_before = raw_line_stats()
    stamp = dt.datetime.now().strftime("%H%M%S%f")[:12]

    def one(i):
        # A session per thread: requests.Session is not thread-safe.
        session = session_factory()
        try:
            response = session.post(f"{url}/submit", timeout=timeout,
                                    json={"text": SAMPLE, "creator_id": f"c9_{stamp}_{i}"})
            return response.status_code
        except Exception as exc:  # noqa: BLE001
            return f"{type(exc).__name__}"

    with concurrent.futures.ThreadPoolExecutor(max_workers=spec["concurrency"]) as pool:
        statuses = list(pool.map(one, range(spec["requests"])))

    new = records_since(before)
    lines_after, malformed_after = raw_line_stats()
    ids = [r.get("request_id") for r in new]
    distinct = len(set(ids))

    ok = sum(1 for s in statuses if s == 200)
    return {
        "requests_sent": len(statuses),
        "concurrency": spec["concurrency"],
        "http_200": ok,
        "non_200": [s for s in statuses if s != 200][:10],
        "records_gained": len(new),
        "distinct_request_ids": distinct,
        "malformed_lines_added": malformed_after - malformed_before,
        "lines_added": lines_after - lines_before,
        "slowest_ms": round(max([r["duration_ms"] for r in new], default=0), 2),
        "median_ms_under_load": round(statistics.median(
            [r["duration_ms"] for r in new]), 2) if new else None,
        "passed": (len(new) == spec["records_required"]
                   and (malformed_after - malformed_before) <= spec["max_malformed_lines"]
                   and distinct == spec["records_required"]),
        "evidence": new[-2:],
    }


def criterion_10(session, url, timeout):
    """The extension changed nothing about the verdicts."""
    spec = T.TARGETS[10]
    stamp = dt.datetime.now().strftime("%H%M%S%f")[:12]

    def scores(texts, tag):
        out = []
        for i, text in enumerate(texts):
            response = session.post(f"{url}/submit", timeout=timeout,
                                    json={"text": text, "creator_id": f"c10_{tag}_{stamp}_{i}"})
            if response.status_code == 200:
                out.append(response.json()["confidence"])
        return out

    ai = scores(scenarios.AI_UNEDITED, "ai")
    human = scores([scenarios.CALIB_INFORMAL] + scenarios.STUDENT_VOICE[:4], "hu")
    if not ai or not human:
        return {"passed": False, "note": "a set came back empty", "evidence": []}

    ai_mean = round(statistics.mean(ai), 4)
    human_mean = round(statistics.mean(human), 4)
    separation = round(ai_mean - human_mean, 4)
    return {
        "ai_scores": ai,
        "human_scores": human,
        "ai_mean": ai_mean,
        "human_mean": human_mean,
        "separation": separation,
        "passed": separation >= spec["min_separation"],
        "evidence": [],
    }


# ── driving it ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--timeout", type=float, default=180.0)
    args = parser.parse_args()

    try:
        import requests
    except ImportError:
        print("The `requests` package isn't installed.\n"
              "Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}. Start it:  python app.py", file=sys.stderr)
        sys.exit(1)

    session = requests.Session()
    fault = session.post(f"{args.url}{T.FAULT_ROUTE}", json={}, timeout=10)
    fault_available = fault.status_code != 404
    if not fault_available:
        print(f"!! {T.FAULT_ROUTE} is not registered, so criterion 7 cannot be judged.\n"
              f"   Restart the service with AI201_FAULT_INJECTION=1 and run this again.\n")

    if args.trials < 3:
        print(f"!! {args.trials} trial(s). The submission asks for three.\n")

    trials = []
    for trial in range(1, args.trials + 1):
        print(f"\n=== Trial {trial} of {args.trials} ===")
        results = {}
        print("  criterion 6  — 30 requests, one record each")
        results[6] = criterion_6(session, args.url, args.timeout)
        print(f"    {'PASS' if results[6]['passed'] else 'FAIL'} "
              f"{results[6]['records_gained']} records, "
              f"{results[6]['complete_records']} complete")

        print("  criterion 7  — failures recorded as failures")
        results[7] = criterion_7(session, args.url, args.timeout, fault_available)
        print(f"    {'PASS' if results[7]['passed'] else 'FAIL'} "
              f"{results[7]['recorded_as_failure']} as failure, "
              f"{results[7]['recorded_as_ok']} as ok")

        print("  criterion 8  — warm latency")
        results[8] = criterion_8(session, args.url, args.timeout)
        print(f"    {'PASS' if results[8]['passed'] else 'FAIL'} "
              f"median {results[8].get('median_ms')} ms")

        print("  criterion 9  — 50 requests, 10 at a time")
        results[9] = criterion_9(lambda: requests.Session(), args.url, args.timeout)
        print(f"    {'PASS' if results[9]['passed'] else 'FAIL'} "
              f"{results[9]['records_gained']} records, "
              f"{results[9]['malformed_lines_added']} malformed, "
              f"{results[9]['distinct_request_ids']} distinct ids")

        print("  criterion 10 — signal separation unchanged")
        results[10] = criterion_10(session, args.url, args.timeout)
        print(f"    {'PASS' if results[10]['passed'] else 'FAIL'} "
              f"separation {results[10].get('separation')}")

        trials.append(results)

    write_report(trials, args, fault_available)


def verdict_for(number, trials):
    """MET only if every trial passed — the target has to hold, not turn up."""
    passes = [t[number]["passed"] for t in trials]
    return "MET" if all(passes) else "MISSED"


def cell(number, result):
    """The one number that matters for this criterion, for the run-log table."""
    if number == 6:
        return f"{result['complete_records']}/{result['requests_sent']}"
    if number == 7:
        return f"{result['recorded_as_failure']}/{result['requests_sent']}"
    if number == 8:
        return f"{result.get('median_ms', '—')} ms"
    if number == 9:
        return (f"{result['records_gained']}/{result['requests_sent']}, "
                f"{result['malformed_lines_added']} bad")
    if number == 10:
        return f"{result.get('separation', '—')}"
    return "—"


def write_report(trials, args, fault_available):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now()
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"capstone_run_{stamp:%Y-%m-%d_%H%M}{label}.md"

    n = len(trials)
    headers = " | ".join(f"Run {i}" for i in range(1, n + 1))
    divider = "|".join(["---"] * n)

    lines = [
        f"# Capstone run log{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `run_capstone_eval.py::main`",
        "- Targets read from: `capstone_targets.py`, which mirrors `criteria.md`",
        "- Durations are the service's own, from `logs/requests.jsonl`",
        f"- {n} trials per criterion · {stamp:%Y-%m-%d %H:%M}",
        "",
    ]
    if not fault_available:
        lines += ["> ⚠️ The fault-injection route was not registered, so criterion 7",
                  "> was judged without a raising handler and is reported MISSED.", ""]

    lines += [f"| Criterion | Target | {headers} | Verdict |", f"|---|---|{divider}|---|"]
    for number in sorted(T.TARGETS):
        spec = T.TARGETS[number]
        cells = " | ".join(cell(number, t[number]) for t in trials)
        lines.append(f"| {number}. {spec['name']} | {spec['target']} | {cells} "
                     f"| {verdict_for(number, trials)} |")

    lines += ["", "---", "", "## What actually came back", "",
              "Real output, as recorded. Each block is one trial's measurements for",
              "one criterion, straight from the runner.", ""]

    for number in sorted(T.TARGETS):
        lines += [f"### Criterion {number} — {T.TARGETS[number]['name']}", ""]
        for i, trial in enumerate(trials, 1):
            lines += [f"**Trial {i}**", "", "```json",
                      json.dumps(trial[number], indent=2), "```", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")
    for number in sorted(T.TARGETS):
        print(f"  criterion {number}: {verdict_for(number, trials)}")


if __name__ == "__main__":
    main()
