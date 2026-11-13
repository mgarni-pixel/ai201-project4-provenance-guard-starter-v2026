# Capstone run log — after

- Produced by: `run_capstone_eval.py::main`
- Targets read from: `capstone_targets.py`, which mirrors `criteria.md`
- Durations are the service's own, from `logs/requests.jsonl`
- 3 trials per criterion · 2026-11-12 19:31

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 6. Every request leaves exactly one complete record | 30 of 30, all 11 fields | 30/30 | 30/30 | 30/30 | MET |
| 7. A request that fails is recorded as having failed | 7 of 7 recorded as failures, 0 as ok | 7/7 | 7/7 | 7/7 | MET |
| 8. A warm submission answers in under 250 ms | median < 250 ms, 9 of 10 < 400 ms | 106.34 ms | 112.45 ms | 140.89 ms | MET |
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
      "timestamp": "2026-11-13T03:31:23.652+00:00",
      "request_id": "d87538eb8005",
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
      "timestamp": "2026-11-13T03:31:23.679+00:00",
      "request_id": "64ab2eef43b1",
      "method": "GET",
      "route": "/no-such-route-193121263915",
      "status": 404,
      "duration_ms": 0.2,
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
      "timestamp": "2026-11-13T03:31:32.620+00:00",
      "request_id": "b2748cbf8fa2",
      "method": "GET",
      "route": "/health",
      "status": 200,
      "duration_ms": 3.54,
      "creator_id": null,
      "content_id": null,
      "outcome": "ok",
      "stages": {},
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:31:32.633+00:00",
      "request_id": "8c0e24e62a4b",
      "method": "GET",
      "route": "/no-such-route-193129805885",
      "status": 404,
      "duration_ms": 0.25,
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
      "timestamp": "2026-11-13T03:31:42.264+00:00",
      "request_id": "1fb9a92747bd",
      "method": "GET",
      "route": "/health",
      "status": 200,
      "duration_ms": 4.04,
      "creator_id": null,
      "content_id": null,
      "outcome": "ok",
      "stages": {},
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:31:42.268+00:00",
      "request_id": "c50cc906f368",
      "method": "GET",
      "route": "/no-such-route-193139272296",
      "status": 404,
      "duration_ms": 0.25,
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
      "timestamp": "2026-11-13T03:31:23.721+00:00",
      "request_id": "a7c7b7911136",
      "method": "POST",
      "route": "/submit",
      "status": 400,
      "duration_ms": 0.66,
      "creator_id": "cap_bad_huge",
      "content_id": null,
      "outcome": "text_too_long",
      "stages": {},
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:31:23.724+00:00",
      "request_id": "bd561a18aa8b",
      "method": "POST",
      "route": "/_fault/raise",
      "status": 500,
      "duration_ms": 0.96,
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
      "timestamp": "2026-11-13T03:31:32.729+00:00",
      "request_id": "75baab02c95e",
      "method": "POST",
      "route": "/submit",
      "status": 400,
      "duration_ms": 1.64,
      "creator_id": "cap_bad_huge",
      "content_id": null,
      "outcome": "text_too_long",
      "stages": {},
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:31:32.733+00:00",
      "request_id": "132969e768fe",
      "method": "POST",
      "route": "/_fault/raise",
      "status": 500,
      "duration_ms": 1.07,
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
      "timestamp": "2026-11-13T03:31:42.386+00:00",
      "request_id": "3238f5b066d4",
      "method": "POST",
      "route": "/submit",
      "status": 400,
      "duration_ms": 1.47,
      "creator_id": "cap_bad_huge",
      "content_id": null,
      "outcome": "text_too_long",
      "stages": {},
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:31:42.402+00:00",
      "request_id": "8031c9ef5f1d",
      "method": "POST",
      "route": "/_fault/raise",
      "status": 500,
      "duration_ms": 1.18,
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
  "median_ms": 106.34,
  "min_ms": 97.65,
  "max_ms": 129.71,
  "under_400ms": 10,
  "mean_model_signal_ms": 85.14,
  "passed": true,
  "evidence": [
    {
      "timestamp": "2026-11-13T03:31:24.861+00:00",
      "request_id": "3154eb6c7f9e",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 110.32,
      "creator_id": "c8_193123847319_8",
      "content_id": "4a3a4f21-519c-4aaa-8bcd-daca49a5b7d8",
      "outcome": "decided",
      "stages": {
        "model_signal": 85.47,
        "style_signal": 0.36,
        "phrase_signal": 0.3,
        "scoring": 0.01
      },
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:31:24.974+00:00",
      "request_id": "d2351ae02768",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 108.18,
      "creator_id": "c8_193123847319_9",
      "content_id": "d3b58271-fbc8-40da-86ab-2702a18becfb",
      "outcome": "decided",
      "stages": {
        "model_signal": 84.49,
        "style_signal": 0.32,
        "phrase_signal": 0.26,
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
  "runs": 10,
  "median_ms": 112.45,
  "min_ms": 106.9,
  "max_ms": 113.93,
  "under_400ms": 10,
  "mean_model_signal_ms": 86.73,
  "passed": true,
  "evidence": [
    {
      "timestamp": "2026-11-13T03:31:33.959+00:00",
      "request_id": "c642a4f953cc",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 113.53,
      "creator_id": "c8_193132889281_8",
      "content_id": "e59382ed-83ff-4e09-98ec-8a719f0473c4",
      "outcome": "decided",
      "stages": {
        "model_signal": 88.78,
        "style_signal": 0.31,
        "phrase_signal": 0.27,
        "scoring": 0.0
      },
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:31:34.078+00:00",
      "request_id": "eeffa3f514ce",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 113.84,
      "creator_id": "c8_193132889281_9",
      "content_id": "e47ae579-25b6-410e-be61-a4ffc0c423b5",
      "outcome": "decided",
      "stages": {
        "model_signal": 89.25,
        "style_signal": 0.32,
        "phrase_signal": 0.29,
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
  "runs": 10,
  "median_ms": 140.89,
  "min_ms": 113.16,
  "max_ms": 161.33,
  "under_400ms": 10,
  "mean_model_signal_ms": 103.49,
  "passed": true,
  "evidence": [
    {
      "timestamp": "2026-11-13T03:31:43.925+00:00",
      "request_id": "930db504368d",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 138.47,
      "creator_id": "c8_193142575334_8",
      "content_id": "1b67f9af-2d5d-44f3-bcdf-ee8a92dc45ff",
      "outcome": "decided",
      "stages": {
        "model_signal": 103.68,
        "style_signal": 0.43,
        "phrase_signal": 0.35,
        "scoring": 0.01
      },
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:31:44.075+00:00",
      "request_id": "f6dde3654251",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 140.59,
      "creator_id": "c8_193142575334_9",
      "content_id": "a531ac41-4e3e-46d4-8a60-7cd1f6936f7d",
      "outcome": "decided",
      "stages": {
        "model_signal": 103.38,
        "style_signal": 0.47,
        "phrase_signal": 0.43,
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
  "slowest_ms": 847.04,
  "median_ms_under_load": 621.36,
  "passed": true,
  "evidence": [
    {
      "timestamp": "2026-11-13T03:31:28.274+00:00",
      "request_id": "ec4746f9b156",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 604.6,
      "creator_id": "c9_193124992847_48",
      "content_id": "aed59810-f674-4cfb-8f60-a93137ac4623",
      "outcome": "decided",
      "stages": {
        "model_signal": 567.64,
        "style_signal": 0.46,
        "phrase_signal": 0.35,
        "scoring": 0.01
      },
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:31:28.311+00:00",
      "request_id": "bdacdb3d7156",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 576.17,
      "creator_id": "c9_193124992847_49",
      "content_id": "4a114d83-15dc-4bbf-ac3e-314ec740dc28",
      "outcome": "decided",
      "stages": {
        "model_signal": 550.95,
        "style_signal": 0.31,
        "phrase_signal": 0.26,
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
  "slowest_ms": 856.46,
  "median_ms_under_load": 678.76,
  "passed": true,
  "evidence": [
    {
      "timestamp": "2026-11-13T03:31:37.645+00:00",
      "request_id": "260d8d287194",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 588.39,
      "creator_id": "c9_193134098829_49",
      "content_id": "16b02816-c604-4cde-bf79-eb2b03c441b6",
      "outcome": "decided",
      "stages": {
        "model_signal": 555.21,
        "style_signal": 0.32,
        "phrase_signal": 0.26,
        "scoring": 0.0
      },
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:31:37.663+00:00",
      "request_id": "e4eb1504e2c2",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 660.75,
      "creator_id": "c9_193134098829_48",
      "content_id": "5c04502f-6501-4cb8-a444-160a39ffb222",
      "outcome": "decided",
      "stages": {
        "model_signal": 619.28,
        "style_signal": 0.38,
        "phrase_signal": 0.27,
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
  "slowest_ms": 1156.27,
  "median_ms_under_load": 882.44,
  "passed": true,
  "evidence": [
    {
      "timestamp": "2026-11-13T03:31:48.783+00:00",
      "request_id": "0ad41024e7dd",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 836.34,
      "creator_id": "c9_193144109300_48",
      "content_id": "05072090-a309-4c34-9313-ee3a1d08a38b",
      "outcome": "decided",
      "stages": {
        "model_signal": 781.73,
        "style_signal": 0.5,
        "phrase_signal": 0.38,
        "scoring": 0.02
      },
      "exception": null
    },
    {
      "timestamp": "2026-11-13T03:31:48.817+00:00",
      "request_id": "329cc9e3452b",
      "method": "POST",
      "route": "/submit",
      "status": 200,
      "duration_ms": 744.27,
      "creator_id": "c9_193144109300_49",
      "content_id": "f973d522-18aa-4741-a736-99a785c438ab",
      "outcome": "decided",
      "stages": {
        "model_signal": 675.36,
        "style_signal": 0.53,
        "phrase_signal": 0.36,
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
