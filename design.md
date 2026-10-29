# Milestone 1 — Trace a submission before building one

## The path

1. **Arrive.** A writing site POSTs `{"text", "creator_id"}` to `/submit`.
2. **Check the input.** The route rejects missing/empty/non-string text, missing
   creator_id, or text over 20,000 characters with a 400 and a clear error. Every
   rejection is written to the audit log so it leaves a trace.
3. **Name it.** The route gives the submission a `content_id` (a UUID). This is
   the handle the writer needs later to appeal.
4. **Signal one (detector.py).** GPT-2 measures how predictable the text is
   (perplexity) → `model_score`, 0–1, higher = more AI-like.
5. **Signal two (stylometry.py).** Measures the text's shape — sentence-length
   spread, word variety, punctuation variety → `style_score`, 0–1, higher = more AI-like.
6. **Combine (scoring.py::combine_signals).** The two scores become one
   `confidence` score.
7. **Label (scoring.py::score_to_label).** The score maps to `ai` / `unsure` /
   `human` and a plain-English sentence.
8. **Log and answer.** Everything (both signals, combined score, label, status
   `decided`) is appended to `logs/audit.jsonl`, and the JSON response goes back.

## The two signals

| | Signal one — model | Signal two — style |
|---|---|---|
| Measures | How predictable each next word is to GPT-2 (perplexity) | Shape: how much sentence lengths vary, how varied the vocabulary is, how varied the punctuation is |
| Why it might differ | Models write by picking likely words, so their text is easy for a model to predict | Generated prose marches in even, mid-length sentences with commas and full stops; people are lumpier |
| Blind spot | Rewards plain writing: second-language writers, young writers, anyone writing simply score as AI. Ornate rare-word AI text scores as human | Can't read. Typos, chopped-up sentences, a pasted quote, or a dash or two move it without changing who wrote it. Very short text has almost no shape to measure |

## The false positive, traced

Maria writes a short, plain essay about her grandmother in her second language.
She uses words she is sure of, in short sentences. GPT-2 finds it easy to
predict → `model_score` around 0.8. Her sentences vary a bit in length, so
`style_score` lands around 0.45. If I averaged evenly she'd get ~0.62.

What she must **not** see is "this was written by AI". So:

- The AI label needs **every** signal to point at AI, not just the model one
  (see the combining rule), and the AI threshold sits high (0.85).
- The label never says "AI-generated" as fact. Even the AI label says it
  "looks a lot like" AI writing and tells her she can appeal.
- She can POST `/appeal` with her `content_id` and her reasoning. The item
  moves to `under_review` and a person looks at it. The original decision stays
  in the log so nobody can quietly rewrite what happened.

## Endpoint contracts

### `POST /submit`

In:

| field | type | required | notes |
|---|---|---|---|
| `text` | string | yes | 1–20,000 characters after trimming |
| `creator_id` | string | yes | non-empty |

Out (200):

| field | type | meaning |
|---|---|---|
| `content_id` | string | UUID; use it to appeal |
| `guess` | `"ai"` / `"human"` / `"unsure"` | machine-readable call |
| `confidence` | float 0–1 | combined score; higher = more AI-like |
| `label` | string | the sentence a reader sees |
| `model_score` | float 0–1 | signal one |
| `style_score` | float 0–1 | signal two |
| `status` | `"decided"` | lifecycle state |

Errors (400): `{"error": "<code>", "message": "<what to fix>"}` — codes
`invalid_json`, `missing_text`, `empty_text`, `text_too_long`,
`text_too_short`, `missing_creator_id`.

### `POST /appeal`

In:

| field | type | required |
|---|---|---|
| `content_id` | string | yes — from a `/submit` response |
| `reasoning` | string | yes, non-empty — the writer's explanation |

Out (200): `{"content_id", "status": "under_review", "message"}`.
Errors: 400 for missing fields, 404 `unknown_content_id` if the id was never
submitted.
