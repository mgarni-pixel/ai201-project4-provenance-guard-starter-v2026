#!/usr/bin/env python3
"""
Self-check for the Unit 9 instrumentation.

    python test_obs.py

Runs against a throwaway log file and a tiny Flask app, so it needs no server
and never loads GPT-2 — the point is the recording, not the detector. Three
things are worth checking and none of them is obvious:

  1. a successful request leaves exactly one record, with every field present
  2. a handler that *raises* still leaves one, with status 500 and the
     exception type — this is the teardown path, and it is the one that would
     silently do nothing if the hook were wired wrong
  3. stage timings land on the record, and a stage entered twice accumulates

Exits non-zero on the first failure, so it is usable in a pipeline.
"""

import sys
import tempfile
from pathlib import Path

import config

# Redirect the log BEFORE obs is imported anywhere that caches the path.
# obs reads config.REQUEST_LOG at write time, so reassigning here is enough.
_tmp = Path(tempfile.mkdtemp(prefix="obs_selfcheck_"))
config.LOG_DIR = _tmp
config.REQUEST_LOG = _tmp / "requests.jsonl"

import obs  # noqa: E402  — after the redirect, on purpose

from flask import Flask  # noqa: E402

failures = []


def check(label: str, condition: bool, detail: str = ""):
    if condition:
        print(f"  ok    {label}")
    else:
        print(f"  FAIL  {label}{f' — {detail}' if detail else ''}")
        failures.append(label)


def build_app():
    app = Flask("obs_selfcheck")
    obs.install(app)

    @app.post("/good")
    def good():
        with obs.stage("work"):
            pass
        with obs.stage("work"):  # same stage twice — should accumulate
            pass
        obs.note(content_id="abc-123", outcome="decided")
        return {"ok": True}

    @app.post("/bad")
    def bad():
        raise RuntimeError("deliberate")

    return app


def main():
    app = build_app()
    client = app.test_client()

    print("A successful request")
    response = client.post("/good", json={"creator_id": "selfcheck_1"})
    check("returns 200", response.status_code == 200, f"got {response.status_code}")
    check("carries an X-Request-ID header", bool(response.headers.get("X-Request-ID")))

    records = obs.read_records()
    check("left exactly one record", len(records) == 1, f"got {len(records)}")
    if not records:
        report()
        return

    record = records[0]
    missing = [f for f in obs.REQUIRED_FIELDS if f not in record]
    check("record has every required field", not missing, f"missing {missing}")
    check("route is the matched rule", record["route"] == "/good", record["route"])
    check("creator_id came off the body", record["creator_id"] == "selfcheck_1")
    check("content_id came from note()", record["content_id"] == "abc-123")
    check("outcome came from note()", record["outcome"] == "decided")
    check("duration_ms is a number", isinstance(record["duration_ms"], (int, float)))
    check("request_id matches the header",
          record["request_id"] == response.headers.get("X-Request-ID"))

    print("Stage timings")
    check("the stage was recorded", "work" in record["stages"], str(record["stages"]))
    check("entering a stage twice accumulates one entry",
          len(record["stages"]) == 1, str(record["stages"]))

    print("A handler that raises")
    try:
        client.post("/bad", json={"creator_id": "selfcheck_2"})
    except RuntimeError:
        pass  # test_client re-raises; the record should already be written

    records = obs.read_records()
    check("left a second record", len(records) == 2, f"got {len(records)}")
    if len(records) == 2:
        failed = records[1]
        check("status is 500", failed["status"] == 500, str(failed["status"]))
        check("exception type is recorded", failed["exception"] == "RuntimeError",
              str(failed["exception"]))
        check("outcome is error", failed["outcome"] == "error", str(failed["outcome"]))
        check("creator_id survived the failure", failed["creator_id"] == "selfcheck_2")

    print("Reading the log back")
    check("limit keeps the most recent", len(obs.read_records(limit=1)) == 1)
    config.REQUEST_LOG.write_text(
        config.REQUEST_LOG.read_text(encoding="utf-8") + "{not json\n", encoding="utf-8")
    check("a malformed line is skipped, not raised on", len(obs.read_records()) == 2)

    report()


def report():
    print()
    if failures:
        print(f"{len(failures)} check(s) failed: {', '.join(failures)}")
        sys.exit(1)
    print("All checks passed.")


if __name__ == "__main__":
    main()
