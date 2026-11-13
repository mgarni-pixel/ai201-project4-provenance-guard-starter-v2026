"""
The numbers from criteria.md, in one place.  <- UNIT 9, MILESTONE 4

`run_capstone_eval.py` reads its targets from here so that a verdict is
computed against the criterion as written, rather than against whatever the
runner's author remembered at the time. If a target changes in criteria.md,
change it here too — and if the two ever disagree, criteria.md is the one that
counts.
"""

TARGETS = {
    6: {
        "name": "Every request leaves exactly one complete record",
        "target": "30 of 30, all 11 fields",
        "requests": 30,
        "complete_records_required": 30,
    },
    7: {
        "name": "A request that fails is recorded as having failed",
        "target": "7 of 7 recorded as failures, 0 as ok",
        "failures_required": 7,
        "max_recorded_ok": 0,
    },
    8: {
        "name": "A warm submission answers in under 250 ms",
        "target": "median < 250 ms, 9 of 10 < 400 ms",
        "runs": 10,
        "median_ms_max": 250.0,
        "per_run_ms_max": 400.0,
        "per_run_min_passing": 9,
    },
    9: {
        "name": "The log survives ten times the normal rate",
        "target": "50 records, 0 malformed, 50 distinct ids",
        "requests": 50,
        "concurrency": 10,
        "records_required": 50,
        "max_malformed_lines": 0,
    },
    10: {
        "name": "The extension changed nothing about the verdicts",
        "target": "AI mean - human mean >= 0.30",
        "min_separation": 0.30,
    },
}

# The fault-injection route criterion 7 needs. Off unless the env var is set,
# so a service started the ordinary way has no endpoint that deliberately
# raises. See app.py.
FAULT_ROUTE = "/_fault/raise"
