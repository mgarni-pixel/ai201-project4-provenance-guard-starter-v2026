# Cost per run — coldstart_after

- Produced by: `measure_cost.py::main`
- Measured from: `logs/requests.jsonl`, matched by `X-Request-ID`
- 2026-11-12 19:31 · 2 warm runs averaged

The cost of one run here is seconds of compute. Nothing in this service
calls a paid API — GPT-2 runs locally — so there is no bill to read, and
this is the real resource one submission consumes.

| Run | Status | Total ms | model_signal ms | Everything else ms |
|---|---|---|---|---|
| 1 | 200 | 310.92 | 286.26 | 24.66 |
| 2 | 200 | 95.31 | 74.54 | 20.77 |
| 3 | 200 | 100.33 | 78.64 | 21.69 |

## Summary

```json
{
  "runs_sent": 3,
  "runs_measured": 2,
  "cold_start_ms": 310.92,
  "mean_ms": 97.82,
  "median_ms": 97.82,
  "min_ms": 95.31,
  "max_ms": 100.33,
  "mean_model_signal_ms": 76.59,
  "model_share": 0.783,
  "cold_included": false,
  "seconds_per_run": 0.0978,
  "seconds_per_100_per_day": 9.78
}
```

Run 1 is the cold start and is excluded from the average unless
`--include-cold` was passed. It carries the one-time model load.