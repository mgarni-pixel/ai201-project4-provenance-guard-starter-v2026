#!/usr/bin/env python3
"""
What one run of this service actually costs.  <- UNIT 9, MILESTONE 3

    python app.py                     # in one terminal
    python measure_cost.py            # in another

There is no API bill to read here. Every signal runs on this machine: GPT-2
through `detector.model_signal`, and two pure-Python passes after it. So the
real cost is **seconds of compute**, and the brief says to measure that rather
than quote it from a pricing page.

How it measures. It sends N submissions of the same text, one at a time, each
with its own `creator_id` so the per-creator rate limit never fires, and reads
the duration back out of `logs/requests.jsonl` by request id — the number the
service recorded for itself, not one timed from out here, so network and curl
overhead stay out of it.

The first request after a start is excluded from the average and reported on
its own line. It carries the one-time GPT-2 load, which is not a per-run cost
and is about three hundred times the warm figure; averaging it in would give a
number that describes neither a cold run nor a warm one.

    --runs N        how many warm submissions to average (default 10)
    --include-cold  average every run instead, cold start included
"""

import argparse
import datetime as dt
import json
import statistics
import sys

import config
import obs

DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"

# One fixed text for every run. A cost-per-run number only means something if
# the run is the same each time, and length drives the model signal directly.
SAMPLE = (
    "The bus to campus takes forty minutes if nothing goes wrong, and something always goes "
    "wrong. Last week a guy got on with a bike and argued with the driver about where to put "
    "it for ten minutes. I missed the start of my statistics class and had to borrow notes "
    "from someone I barely know. She has very neat handwriting."
)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--label", default="")
    parser.add_argument("--include-cold", action="store_true")
    parser.add_argument("--timeout", type=float, default=120.0)
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

    stamp = dt.datetime.now()
    sent = []
    print(f"Sending {args.runs} submissions to {args.url}/submit")
    for i in range(1, args.runs + 1):
        body = {"text": SAMPLE, "creator_id": f"cost_{stamp:%H%M%S}_{i}"}
        try:
            response = requests.post(f"{args.url}/submit", json=body, timeout=args.timeout)
        except Exception as exc:  # noqa: BLE001
            print(f"  run {i}: {type(exc).__name__}: {exc}")
            continue
        request_id = response.headers.get("X-Request-ID")
        sent.append({"run": i, "request_id": request_id, "status": response.status_code})
        print(f"  run {i}: HTTP {response.status_code}  request_id {request_id}")

    # Pull the service's own numbers back out of the operational log.
    by_id = {r["request_id"]: r for r in obs.read_records()}
    rows = []
    for item in sent:
        record = by_id.get(item["request_id"])
        if record is None:
            print(f"  !! run {item['run']} left no log record", file=sys.stderr)
            continue
        rows.append({
            "run": item["run"],
            "status": item["status"],
            "duration_ms": record["duration_ms"],
            "model_ms": record["stages"].get("model_signal"),
            "other_ms": round(record["duration_ms"]
                              - (record["stages"].get("model_signal") or 0), 2),
        })

    if not rows:
        print("No runs produced a log record. Nothing to measure.", file=sys.stderr)
        sys.exit(1)

    cold = rows[0]
    warm = rows if args.include_cold else rows[1:]
    if not warm:
        print("Only one run — not enough to average. Use --runs 10.", file=sys.stderr)
        sys.exit(1)

    durations = [r["duration_ms"] for r in warm]
    model_times = [r["model_ms"] for r in warm if r["model_ms"] is not None]
    summary = {
        "runs_sent": len(sent),
        "runs_measured": len(warm),
        "cold_start_ms": cold["duration_ms"],
        "mean_ms": round(statistics.mean(durations), 2),
        "median_ms": round(statistics.median(durations), 2),
        "min_ms": round(min(durations), 2),
        "max_ms": round(max(durations), 2),
        "mean_model_signal_ms": round(statistics.mean(model_times), 2) if model_times else None,
        "model_share": (round(statistics.mean(model_times) / statistics.mean(durations), 3)
                        if model_times else None),
        "cold_included": args.include_cold,
    }
    # Compute-seconds per run, then the brief's hundred-a-day arithmetic.
    summary["seconds_per_run"] = round(summary["mean_ms"] / 1000, 4)
    summary["seconds_per_100_per_day"] = round(summary["seconds_per_run"] * 100, 2)

    print()
    for key, value in summary.items():
        print(f"  {key}: {value}")

    write_report(rows, cold, summary, args, stamp)


def write_report(rows, cold, summary, args, stamp):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"cost_{stamp:%Y-%m-%d_%H%M}{label}.md"

    lines = [
        f"# Cost per run{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `measure_cost.py::main`",
        "- Measured from: `logs/requests.jsonl`, matched by `X-Request-ID`",
        f"- {stamp:%Y-%m-%d %H:%M} · {summary['runs_measured']} warm runs averaged",
        "",
        "The cost of one run here is seconds of compute. Nothing in this service",
        "calls a paid API — GPT-2 runs locally — so there is no bill to read, and",
        "this is the real resource one submission consumes.",
        "",
        "| Run | Status | Total ms | model_signal ms | Everything else ms |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['run']} | {row['status']} | {row['duration_ms']} | "
                     f"{row['model_ms']} | {row['other_ms']} |")

    lines += [
        "",
        "## Summary",
        "",
        "```json",
        json.dumps(summary, indent=2),
        "```",
        "",
        "Run 1 is the cold start and is excluded from the average unless",
        "`--include-cold` was passed. It carries the one-time model load.",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
