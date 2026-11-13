# Cost per run — coldstart_before

- Produced by: `measure_cost.py::main`
- Measured from: `logs/requests.jsonl`, matched by `X-Request-ID`
- 2026-11-12 19:30 · 2 warm runs averaged

The cost of one run here is seconds of compute. Nothing in this service
calls a paid API — GPT-2 runs locally — so there is no bill to read, and
this is the real resource one submission consumes.

| Run | Status | Total ms | model_signal ms | Everything else ms |
|---|---|---|---|---|
| 1 | 200 | 4775.14 | 4748.4 | 26.74 |
| 2 | 200 | 105.73 | 83.22 | 22.51 |
| 3 | 200 | 102.23 | 81.86 | 20.37 |

## Summary

```json
{
  "runs_sent": 3,
  "runs_measured": 2,
  "cold_start_ms": 4775.14,
  "mean_ms": 103.98,
  "median_ms": 103.98,
  "min_ms": 102.23,
  "max_ms": 105.73,
  "mean_model_signal_ms": 82.54,
  "model_share": 0.794,
  "cold_included": false,
  "seconds_per_run": 0.104,
  "seconds_per_100_per_day": 10.4
}
```

Run 1 is the cold start and is excluded from the average unless
`--include-cold` was passed. It carries the one-time model load.