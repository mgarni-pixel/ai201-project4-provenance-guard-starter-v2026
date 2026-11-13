# Capstone run log — before

- Produced by: `run_capstone_eval.py::main`
- Targets read from: `capstone_targets.py`, which mirrors `criteria.md`
- Durations are the service's own, from `logs/requests.jsonl`
- 3 trials per criterion · 2026-11-12 19:29

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 6. Every request leaves exactly one complete record | 30 of 30, all 11 fields | 30/30 | 30/30 | 30/30 | MET |
| 7. A request that fails is recorded as having failed | 7 of 7 recorded as failures, 0 as ok | 7/7 | 7/7 | 7/7 | MET |
| 8. A warm submission answers in under 250 ms | median < 250 ms, 9 of 10 < 400 ms | 149.57 ms | 150.13 ms | 154.0 ms | MET |
| 9. The log survives ten times the normal rate | 50 records, 0 malformed, 50 distinct ids | 50/50, 0 bad | 50/50, 0 bad | 50/50, 0 bad | MET |
| 10. The extension changed nothing about the verdicts | AI mean - human mean >= 0.30 | 0.4837 | 0.4837 | 0.4837 | MET |

---

## What actually came back

Real output, as recorded. Each block is one trial's measurements for
one criterion, straight from the runner.

### Criterion 6 — Every request leaves exactly one complete record

**Trial 1**

```json
{
  "requests_sent": 30,
  "records_gained": 30,
  "complete_records": 30,
  "incomplete_records": 0,
  "passed": true,
  "evidence": [
    {
      "timestamp": "2026-11-13T03:29:00.635+00:00",
      "request_id": "e4be63be7a13",
      "method": "GET",
      "route": "/health",
      "status": 200,
      "duration_ms": 2.73,
      "creator_id": null,
      "content_id": null,
      "outcome": "ok",
      "stages": {},
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:29:00.662+00:00",
      "request_id": "5b42f297f8c7",
      "method": "GET",
      "route": "/no-such-route-192849516621",
      "status": 404,
      "duration_ms": 0.4,
      "creator_id": null,
      "content_id": null,
      "outcome": "ok",
      "stages": {},
      "exception": null
    }
  ]
}
```

**Trial 2**

```json
{
  "requests_sent": 30,
  "records_gained": 30,
  "complete_records": 30,
  "incomplete_records": 0,
  "passed": true,
  "evidence": [
    {
      "timestamp": "2026-11-13T03:29:13.448+00:00",
      "request_id": "3bf90464a47a",
      "method": "GET",
      "route": "/health",
      "status": 200,
      "duration_ms": 3.94,
      "creator_id": null,
      "content_id": null,
      "outcome": "ok",
      "stages": {},
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:29:13.451+00:00",
      "request_id": "c4c1d3488e21",
      "method": "GET",
      "route": "/no-such-route-192910139984",
      "status": 404,
      "duration_ms": 0.28,
      "creator_id": null,
      "content_id": null,
      "outcome": "ok",
      "stages": {},
      "exception": null
    }
  ]
}
```

**Trial 3**

```json
{
  "requests_sent": 30,
  "records_gained": 30,
  "complete_records": 30,
  "incomplete_records": 0,
  "passed": true,
  "evidence": [
    {
      "timestamp": "2026-11-13T03:29:26.653+00:00",
      "request_id": "055ddd42c280",
      "method": "GET",
      "route": "/health",
      "status": 200,
      "duration_ms": 4.43,
      "creator_id": null,
      "content_id": null,
      "outcome": "ok",
      "stages": {},
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:29:26.657+00:00",
      "request_id": "359d329f6710",
      "method": "GET",
      "route": "/no-such-route-192923203174",
      "status": 404,
      "duration_ms": 0.26,
      "creator_id": null,
      "content_id": null,
      "outcome": "ok",
      "stages": {},
      "exception": null
    }
  ]
}
```

### Criterion 7 — A request that fails is recorded as having failed

**Trial 1**

```json
{
  "requests_sent": 7,
  "fault_route_available": true,
  "response_statuses": [
    400,
    400,
    400,
    400,
    400,
    400,
    500
  ],
  "records_gained": 7,
  "recorded_as_failure": 7,
  "recorded_as_ok": 0,
  "status_400_records": 6,
  "status_500_records": 1,
  "500s_naming_exception": 1,
  "passed": true,
  "evidence": [
    {
      "timestamp": "2026-11-13T03:29:00.744+00:00",
      "request_id": "2597419a40b5",
      "method": "POST",
      "route": "/submit",
      "status": 400,
      "duration_ms": 1.87,
      "creator_id": "cap_bad_huge",
      "content_id": null,
      "outcome": "text_too_long",
      "stages": {},
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:29:00.762+00:00",
      "request_id": "e2ea702f9d35",
      "method": "POST",
      "route": "/_fault/raise",
      "status": 500,
      "duration_ms": 1.73,
      "creator_id": null,
      "content_id": null,
      "outcome": "error",
      "stages": {},
      "exception": "RuntimeError"
    }
  ]
}
```

**Trial 2**

```json
{
  "requests_sent": 7,
  "fault_route_available": true,
  "response_statuses": [
    400,
    400,
    400,
    400,
    400,
    400,
    500
  ],
  "records_gained": 7,
  "recorded_as_failure": 7,
  "recorded_as_ok": 0,
  "status_400_records": 6,
  "status_500_records": 1,
  "500s_naming_exception": 1,
  "passed": true,
  "evidence": [
    {
      "timestamp": "2026-11-13T03:29:13.498+00:00",
      "request_id": "73fe4baa72c1",
      "method": "POST",
      "route": "/submit",
      "status": 400,
      "duration_ms": 3.82,
      "creator_id": "cap_bad_huge",
      "content_id": null,
      "outcome": "text_too_long",
      "stages": {},
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:29:13.530+00:00",
      "request_id": "89b33dbe4b5b",
      "method": "POST",
      "route": "/_fault/raise",
      "status": 500,
      "duration_ms": 2.25,
      "creator_id": null,
      "content_id": null,
      "outcome": "error",
      "stages": {},
      "exception": "RuntimeError"
    }
  ]
}
```

**Trial 3**

```json
{
  "requests_sent": 7,
  "fault_route_available": true,
  "response_statuses": [
    400,
    400,
    400,
    400,
    400,
    400,
    500
  ],
  "records_gained": 7,
  "recorded_as_failure": 7,
  "recorded_as_ok": 0,
  "status_400_records": 6,
  "status_500_records": 1,
  "500s_naming_exception": 1,
  "passed": true,
  "evidence": [
    {
      "timestamp": "2026-11-13T03:29:26.785+00:00",
      "request_id": "5d9d0b52e450",
      "method": "POST",
      "route": "/submit",
      "status": 400,
      "duration_ms": 1.5,
      "creator_id": "cap_bad_huge",
      "content_id": null,
      "outcome": "text_too_long",
      "stages": {},
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:29:26.810+00:00",
      "request_id": "ce81121f408f",
      "method": "POST",
      "route": "/_fault/raise",
      "status": 500,
      "duration_ms": 2.05,
      "creator_id": null,
      "content_id": null,
      "outcome": "error",
      "stages": {},
      "exception": "RuntimeError"
    }
  ]
}
```

### Criterion 8 — A warm submission answers in under 250 ms

**Trial 1**

```json
{
  "runs": 10,
  "median_ms": 149.57,
  "min_ms": 145.58,
  "max_ms": 163.49,
  "under_400ms": 10,
  "mean_model_signal_ms": 132.39,
  "passed": true,
  "evidence": [
    {
      "timestamp": "2026-11-13T03:29:02.408+00:00",
      "request_id": "14fe3d8ef534",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 163.49,
      "creator_id": "c8_192900967530_8",
      "content_id": "1bded654-9a60-430a-a896-7fb85155143c",
      "outcome": "decided",
      "stages": {
        "model_signal": 145.47,
        "style_signal": 0.32,
        "phrase_signal": 0.27,
        "scoring": 0.01
      },
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:29:02.564+00:00",
      "request_id": "62bff58224e3",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 151.18,
      "creator_id": "c8_192900967530_9",
      "content_id": "fcc69dcf-dc2f-4321-9cc2-07fd910943fd",
      "outcome": "decided",
      "stages": {
        "model_signal": 130.55,
        "style_signal": 0.4,
        "phrase_signal": 0.29,
        "scoring": 0.01
      },
      "exception": null
    }
  ]
}
```

**Trial 2**

```json
{
  "runs": 10,
  "median_ms": 150.13,
  "min_ms": 147.18,
  "max_ms": 153.54,
  "under_400ms": 10,
  "mean_model_signal_ms": 130.96,
  "passed": true,
  "evidence": [
    {
      "timestamp": "2026-11-13T03:29:15.105+00:00",
      "request_id": "e5669ad18161",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 147.33,
      "creator_id": "c8_192913715007_8",
      "content_id": "4dd3e7c0-88b2-46d8-8bf6-19a942a26050",
      "outcome": "decided",
      "stages": {
        "model_signal": 128.34,
        "style_signal": 0.43,
        "phrase_signal": 0.3,
        "scoring": 0.0
      },
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:29:15.264+00:00",
      "request_id": "81b9cca5f06a",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 153.54,
      "creator_id": "c8_192913715007_9",
      "content_id": "0135118a-206b-47be-8663-c6681789b29d",
      "outcome": "decided",
      "stages": {
        "model_signal": 133.34,
        "style_signal": 0.34,
        "phrase_signal": 0.37,
        "scoring": 0.01
      },
      "exception": null
    }
  ]
}
```

**Trial 3**

```json
{
  "runs": 10,
  "median_ms": 154.0,
  "min_ms": 151.89,
  "max_ms": 168.59,
  "under_400ms": 10,
  "mean_model_signal_ms": 135.67,
  "passed": true,
  "evidence": [
    {
      "timestamp": "2026-11-13T03:29:28.439+00:00",
      "request_id": "2d01986bf114",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 156.63,
      "creator_id": "c8_192926982926_8",
      "content_id": "470b1db5-5782-4327-a824-02654d9f36f2",
      "outcome": "decided",
      "stages": {
        "model_signal": 136.76,
        "style_signal": 0.34,
        "phrase_signal": 0.28,
        "scoring": 0.01
      },
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:29:28.605+00:00",
      "request_id": "c8acb7ff2d34",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 160.76,
      "creator_id": "c8_192926982926_9",
      "content_id": "3fd5c020-29d5-4d62-a341-9b2d8785b6a8",
      "outcome": "decided",
      "stages": {
        "model_signal": 140.98,
        "style_signal": 0.32,
        "phrase_signal": 0.28,
        "scoring": 0.01
      },
      "exception": null
    }
  ]
}
```

### Criterion 9 — The log survives ten times the normal rate

**Trial 1**

```json
{
  "requests_sent": 50,
  "concurrency": 10,
  "http_200": 50,
  "non_200": [],
  "records_gained": 50,
  "distinct_request_ids": 50,
  "malformed_lines_added": 0,
  "lines_added": 50,
  "slowest_ms": 1265.27,
  "median_ms_under_load": 1101.65,
  "passed": true,
  "evidence": [
    {
      "timestamp": "2026-11-13T03:29:08.254+00:00",
      "request_id": "54f9779305bf",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 1054.95,
      "creator_id": "c9_192902574481_48",
      "content_id": "f85454a4-b199-471c-8a9a-7a981d9de67f",
      "outcome": "decided",
      "stages": {
        "model_signal": 1030.07,
        "style_signal": 0.37,
        "phrase_signal": 0.34,
        "scoring": 0.01
      },
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:29:08.271+00:00",
      "request_id": "2f949ec4a5c7",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 1049.05,
      "creator_id": "c9_192902574481_49",
      "content_id": "43f27120-8b52-4465-a17c-c1d39d39869d",
      "outcome": "decided",
      "stages": {
        "model_signal": 1019.01,
        "style_signal": 0.34,
        "phrase_signal": 0.29,
        "scoring": 0.0
      },
      "exception": null
    }
  ]
}
```

**Trial 2**

```json
{
  "requests_sent": 50,
  "concurrency": 10,
  "http_200": 50,
  "non_200": [],
  "records_gained": 50,
  "distinct_request_ids": 50,
  "malformed_lines_added": 0,
  "lines_added": 50,
  "slowest_ms": 1289.94,
  "median_ms_under_load": 1137.57,
  "passed": true,
  "evidence": [
    {
      "timestamp": "2026-11-13T03:29:21.309+00:00",
      "request_id": "1d80e87accea",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 1134.48,
      "creator_id": "c9_192915276605_48",
      "content_id": "d8e06ab2-bedc-4b84-a407-d845665cf975",
      "outcome": "decided",
      "stages": {
        "model_signal": 1088.12,
        "style_signal": 0.37,
        "phrase_signal": 0.34,
        "scoring": 0.01
      },
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:29:21.326+00:00",
      "request_id": "594148f370e1",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 1133.17,
      "creator_id": "c9_192915276605_49",
      "content_id": "573fee55-97d4-4922-9fb8-9042957dcf96",
      "outcome": "decided",
      "stages": {
        "model_signal": 1106.87,
        "style_signal": 0.34,
        "phrase_signal": 0.26,
        "scoring": 0.0
      },
      "exception": null
    }
  ]
}
```

**Trial 3**

```json
{
  "requests_sent": 50,
  "concurrency": 10,
  "http_200": 50,
  "non_200": [],
  "records_gained": 50,
  "distinct_request_ids": 50,
  "malformed_lines_added": 0,
  "lines_added": 50,
  "slowest_ms": 1246.62,
  "median_ms_under_load": 1143.51,
  "passed": true,
  "evidence": [
    {
      "timestamp": "2026-11-13T03:29:34.560+00:00",
      "request_id": "03c1b5458599",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 1184.12,
      "creator_id": "c9_192928618642_48",
      "content_id": "8674590e-4281-4c90-a24d-d1c12a552dde",
      "outcome": "decided",
      "stages": {
        "model_signal": 1131.91,
        "style_signal": 0.36,
        "phrase_signal": 0.37,
        "scoring": 0.01
      },
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:29:34.578+00:00",
      "request_id": "b25fc46207ce",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 1112.5,
      "creator_id": "c9_192928618642_49",
      "content_id": "fcbdab40-9cd0-4878-b5df-79989caaed9b",
      "outcome": "decided",
      "stages": {
        "model_signal": 1079.79,
        "style_signal": 0.33,
        "phrase_signal": 0.29,
        "scoring": 0.0
      },
      "exception": null
    }
  ]
}
```

### Criterion 10 — The extension changed nothing about the verdicts

**Trial 1**

```json
{
  "ai_scores": [
    0.8798,
    0.8734,
    0.8829,
    0.8395,
    0.8552
  ],
  "human_scores": [
    0.2546,
    0.5052,
    0.3327,
    0.3818,
    0.4382
  ],
  "ai_mean": 0.8662,
  "human_mean": 0.3825,
  "separation": 0.4837,
  "passed": true,
  "evidence": []
}
```

**Trial 2**

```json
{
  "ai_scores": [
    0.8798,
    0.8734,
    0.8829,
    0.8395,
    0.8552
  ],
  "human_scores": [
    0.2546,
    0.5052,
    0.3327,
    0.3818,
    0.4382
  ],
  "ai_mean": 0.8662,
  "human_mean": 0.3825,
  "separation": 0.4837,
  "passed": true,
  "evidence": []
}
```

**Trial 3**

```json
{
  "ai_scores": [
    0.8798,
    0.8734,
    0.8829,
    0.8395,
    0.8552
  ],
  "human_scores": [
    0.2546,
    0.5052,
    0.3327,
    0.3818,
    0.4382
  ],
  "ai_mean": 0.8662,
  "human_mean": 0.3825,
  "separation": 0.4837,
  "passed": true,
  "evidence": []
}
```
