# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## Stretch Features (declared before building)

I'm adding all three stretch features. I declared them here before writing
any of their code:

1. **A third signal: stock-phrase density** (`phrases.py::phrase_signal`).
   It counts stock transition phrases per 100 words ("additionally", "overall",
   "it is important to", "furthermore", and so on). This measures *word choice*,
   which is different from predictability (signal one) and shape (signal two).
   I'll write a note on how I weight the three.
2. **`GET /content/<id>`** returns one item's current status: its decision,
   whether it's `decided` or `under_review`, any appeals, and whether the
   writer is verified.
3. **A verified-human path.** `POST /verify` is an extra step where a writer
   sends a signed attestation plus a writing sample of at least 50 words. Once
   they pass, they hold a credential, and every item they submit carries a
   `verified_human` badge in `/submit` and `/content/<id>`.

What each one changed is covered in the sections below: **Signals and Scoring**
for the third signal, and **Stretch: GET /content/<id>** and **Stretch:
verified-human path** after the Sample Run.

---

## What This Does

Provenance Guard is a small backend a writing site can call to estimate whether
a piece of text was written by a person or an AI tool, and to let the writer
push back. A submission takes this path:

1. **Arrives.** The site POSTs `{"text", "creator_id"}` to `/submit` (`app.py::submit`).
2. **Input is checked.** Missing/empty/non-string text, missing `creator_id`,
   text over 20,000 characters, or text too short to judge gets a 400 with an
   `error` code and a `message`. Each rejection is written to the audit log.
3. **It gets a `content_id`** (a UUID), the handle the writer needs to appeal.
4. **Signal one** (`detector.py::model_signal`): GPT-2, running locally, measures
   how predictable the text is → `model_score` (0–1, higher = more AI-like).
5. **Signal two** (`stylometry.py::style_signal`): measures the text's shape
   (sentence-length spread, vocabulary variety, punctuation variety) →
   `style_score` (0–1, higher = more AI-like).
6. **Signal three** (`phrases.py::phrase_signal`): stock-phrase density →
   `phrase_score` (0–1, higher = more AI-like).
7. **Combine** (`scoring.py::combine_signals`): one `confidence` score, 0–1.
8. **Label** (`scoring.py::score_to_label`): the score becomes `human` /
   `unsure` / `ai` plus a plain-English sentence.
9. **Log and answer.** All three signal scores, the combined score, the guess,
   the label, status `decided` and the writer's `verified_human` flag are
   appended to `logs/audit.jsonl`, and the JSON response goes back.

If the writer disagrees, `POST /appeal` with the `content_id` and their
reasoning appends an `appeal` entry and moves the item to `under_review`. The
original decision is never overwritten. `GET /content/<id>` shows the item's
current status at any time.

My first trace, signal notes and endpoint contracts are in
[design.md](design.md).

---

## Signals and Scoring

### Signal one — the model signal

**What it measures:** Perplexity under GPT-2: how surprised a language model is
by each next word. It's squashed onto 0–1 with a logistic curve (perplexity
45 → 0.5). Low perplexity → high score.

**Why that might differ between human and AI writing:** A model writes by
picking likely next words, so its output is easy for a model to predict. People
make odder word choices and abrupt turns.

**What it can't see:** Who wrote it. It rewards *plain* writing: short
sentences, common words. A second-language writer, a young writer, or anyone
writing simply scores as AI. In calibration my plain human paragraph scored
**0.862**, close to the real AI text's **0.932**. The reverse also holds:
ornate prose full of rare words scores as human whoever wrote it.

### Signal two — the style signal

**What it measures:** The shape of the text, with no understanding of the
words. Three measures, each mapped to 0–1 (higher = more AI-like) with a linear
ramp between a "fully human" and a "fully AI" value, then weighted
(`stylometry.py`):

| Measure | What it is | Human end → AI end | Weight |
|---|---|---|---|
| Sentence-length spread | stdev / mean of words per sentence | 0.70 → 0.25 | 0.5 |
| Type-token ratio | unique / total words, averaged over 50-word windows | 0.85 → 0.65 | 0.2 |
| Punctuation density | `; : ! ? ( ) — – " …` per 100 words (not `.` or `,`) | 5.0 → 0.5 | 0.3 |

Edge cases: one sentence has no spread, and under 50 words almost every word
is new, so either case scores that measure a neutral 0.5 instead of
pretending it's evidence.

**Why that might differ between human and AI writing:** Generated prose
marches in even, mid-length sentences punctuated with commas and full stops.
People are lumpier: a three-word sentence next to a forty-word one, a dash, a
question to themselves.

**What it can't see:** Meaning. Anything that changes the shape without
changing the author moves it: adding a few dashes or exclamation marks,
chopping sentences up, pasting in a quotation, typos. It also can't tell a
plain writer from a model. My plain human paragraph has even sentences and no
expressive punctuation, so it scored **0.803**, the same as the AI text (0.800).
Modern chatbots that love em dashes would read as *more* human on this signal.

### Signal three — the stock-phrase signal (stretch)

**What it measures:** Word choice. It counts 23 stock transitions and filler
phrases ("additionally", "furthermore", "overall", "it is important to",
"plays a crucial role", "for example", "however", ...) per 100 words, mapped
linearly from 0 per 100 words (score 0) to 4 or more per 100 words (score 1).

**Why that might differ between human and AI writing:** Assistant models are
tuned toward tidy, signposted essays, so these connectives turn up far more
often than in most human writing. My clearly-AI text had **10 per 100 words**.
Every human text I tried had **0**.

**What it can't see:** Anything not on its list. An AI told to "avoid clichés"
sails through, deleting five words defeats it completely, and a human who
writes formal reports full of "however" and "furthermore" gets pushed toward AI.

### The combining rule

**The rule:** A weighted average, then fixed thresholds.

**The numbers:** `confidence = 0.5 × model_score + 0.3 × style_score + 0.2 × phrase_score`;
`human` ≤ 0.35 < `unsure` < 0.85 ≤ `ai`. All in `config.py`.

**How I weighted the three:** The model signal gets the most weight (0.5)
because it's the steadiest. Style comes next (0.3), because a few dashes or
typos can swing it. Stock phrases get the least (0.2): a word list is the
easiest of the three to dodge and the likeliest to hit formal human writers.

**What happens when they disagree:** I don't need a separate disagreement rule,
because the AI threshold is high enough to force agreement. Any two signals at
1.0 with the third at 0 total at most 0.80 (model + style), which is below 0.85.
**The AI label needs all three signals leaning AI.** One signal, or even two,
can never accuse a writer on their own. A split lands in `unsure` or `human`.

**Where it lives:** `scoring.py::combine_signals` (weights and thresholds in
`config.py`, label text in `scoring.py::score_to_label`).

**Calibration run** (each signal separately, same five inputs):

| Input | model | style | phrase | combined | label |
|---|---|---|---|---|---|
| clearly AI (generic chatbot essay) | 0.932 | 0.800 | 1.000 | 0.906 | ai |
| clearly human (informal rant about a radiator) | 0.507 | 0.004 | 0.000 | 0.255 | human |
| plain human (short sentences, simple words) | 0.862 | 0.803 | 0.000 | 0.672 | unsure |
| formal human (legal-style prose) | 0.481 | 0.493 | 0.000 | 0.388 | unsure |
| lightly-edited AI | 0.742 | 0.567 | 0.362 | 0.614 | unsure |

**A case where my signals split, and what my rule does with it:** The
clearly-human rant: model **0.507** (coin-flip, because its words are fairly
common) vs. style **0.004** (wildly uneven sentences, `!`, `;`, quotes). The
weighted average gives 0.255, so `human`. The style signal pulled an undecided
model reading to the right answer.

**What set the AI threshold, and what the third signal changed:** I started
with two signals (0.6 model / 0.4 style) and an AI threshold of 0.70. The plain
human paragraph then scored 0.838 and was labelled **AI**. That's exactly the
false positive I traced in design.md, and both signals fell for it. I raised
the AI threshold to 0.85, which moved it to `unsure`, but only 0.04 below the
real AI text (0.879). Adding the stock-phrase signal widened that gap a lot.
The plain human paragraph has no stock phrases, so it dropped to **0.672**,
while the AI text rose to **0.906**.

**The known weakness:** AI text with its stock phrases edited out and a few
dashes added would fool both signals two and three at once. The lightly-edited
AI sample already lands in `unsure` (0.614). I expect the unit 8 attack set to
hit exactly this.

---

## Label Variants

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | This reads like it was written by a person. Our automated check found nothing that suggests it was produced by an AI tool. |
| unsure | 0.35 – 0.85 | We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way. |
| high-confidence AI | 0.85 – 1.00 | This looks a lot like text produced by an AI writing tool. This is an automated estimate, not a final judgment, and it can be wrong. If you wrote this yourself, you can appeal and a person will review it. |

Boundaries: exactly 0.35 is `human`, exactly 0.85 is `ai`, everything strictly
between is `unsure`, so every score from 0 to 1 maps to one label. All three
were reached through the live service: clearly AI → `ai` (0.9061), clearly
human → `human` (0.2546), plain human → `unsure` (0.6718).

**Why I worded the "unsure" one this way:** The unsure band is wide (0.35–0.85),
and a lot of real people land in it, including the plain writer this system is
most likely to misjudge. So the label says the *tool* is uncertain, not that the
writer is suspect. It says outright that mixed results are common for human
writing, and it makes no claim either way. The AI label never states
authorship as fact, and it tells the writer they can appeal.

---

## Sample Run

**A submission:** the plain-writer case I traced in design.md.

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "My grandmother lived in a small town. She had a big garden with many vegetables. Every summer I went to her house and helped her in the garden. We picked tomatoes and beans together. She taught me how to cook her soup. It was very good and I still make it today. She was a kind person and everyone in the town knew her. I miss her very much. When I cook her soup I think about her and the summers in her garden.", "creator_id": "maria-07"}'
```

```json
{
  "confidence": 0.6718,
  "content_id": "08f190eb-b6fe-40f6-8f2e-ad3d7d61396e",
  "guess": "unsure",
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "model_score": 0.8618,
  "phrase_score": 0.0,
  "status": "decided",
  "style_score": 0.8029,
  "verified_human": false
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "08f190eb-b6fe-40f6-8f2e-ad3d7d61396e", "reasoning": "I wrote this myself about my grandmother. English is my second language, so I use simple words and short sentences."}'
```

```json
{
  "content_id": "08f190eb-b6fe-40f6-8f2e-ad3d7d61396e",
  "message": "Thanks — your appeal is recorded. A person will review this piece, and the label stays marked as under review until they do.",
  "status": "under_review"
}
```

**What the log shows afterwards:** the original decision, unchanged, then the
appeal.

```bash
$ curl "http://127.0.0.1:5000/log?limit=4"
```

```json
{"count":4,"entries":[
  {"combined_score":0.6718,"content_id":"08f190eb-b6fe-40f6-8f2e-ad3d7d61396e","creator_id":"maria-07","guess":"unsure","label":"We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.","model_score":0.8618,"phrase_score":0.0,"status":"decided","style_score":0.8029,"timestamp":"2026-10-29T01:06:26+00:00","verified_human":false},
  {"content_id":"08f190eb-b6fe-40f6-8f2e-ad3d7d61396e","creator_id":"maria-07","event":"appeal","reasoning":"I wrote this myself about my grandmother. English is my second language, so I use simple words and short sentences.","status":"under_review","timestamp":"2026-10-29T01:06:26+00:00"},
  {"attestation":"I confirm that I write my own work and that I am a person.","creator_id":"maria-07","event":"verified","sample":"The committee's deliberations, protracted as they were, ultimately foundered on a question of jurisdiction rather than of substance. Whether the municipal ordinance pre-empted the older county statute was never squarely resolved; counsel for both parties seemed content to leave the matter ambiguous. In retrospect, that ambiguity proved costly. Three years and two appeals later, the parcel remains undeveloped, its title clouded by an easement nobody can locate.","status":"verified","timestamp":"2026-10-29T01:06:26+00:00"},
  {"combined_score":0.3885,"content_id":"a18a8886-ccd3-4e6d-9d9d-a98369a9766d","creator_id":"maria-07","guess":"unsure","label":"We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.","model_score":0.4812,"phrase_score":0.0,"status":"decided","style_score":0.4929,"timestamp":"2026-10-29T01:06:26+00:00","verified_human":true}
]}
```

The last two entries come from the verified-human stretch below.

**Error paths** (each returns JSON `{"error", "message"}` and logs a
`rejected` entry): no body, missing `text`, whitespace-only `text`, numeric
`text`, missing `creator_id`, 20,001-character `text`, a JSON list body, and
`"Hi"` (too short) all returned **400**. An appeal for an unknown
`content_id` returned **404** `unknown_content_id`. An appeal without
`reasoning` returned **400** `missing_reasoning`.

---

## Stretch: GET /content/<id>

`app.py::content` rebuilds one item's current state from the append-only log:
the original decision, every appeal, the latest status, and whether the writer
is verified. **What it changed:** a writer or the site can check an item
without reading the whole log. Here's the same item after the appeal above:

```bash
$ curl http://127.0.0.1:5000/content/08f190eb-b6fe-40f6-8f2e-ad3d7d61396e
```

```json
{
  "appeals": [
    {
      "reasoning": "I wrote this myself about my grandmother. English is my second language, so I use simple words and short sentences.",
      "timestamp": "2026-10-29T01:06:26+00:00"
    }
  ],
  "confidence": 0.6718,
  "content_id": "08f190eb-b6fe-40f6-8f2e-ad3d7d61396e",
  "creator_id": "maria-07",
  "guess": "unsure",
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "model_score": 0.8618,
  "phrase_score": 0.0,
  "status": "under_review",
  "style_score": 0.8029,
  "submitted_at": "2026-10-29T01:06:26+00:00",
  "verified_human": false
}
```

An unknown id returns **404** `unknown_content_id`.

---

## Stretch: verified-human path

**The extra step:** `POST /verify` (`app.py::verify`) with the writer's
`creator_id`, an attestation that must read exactly *"I confirm that I write
my own work and that I am a person."*, and a writing sample of at least 50
words. A wrong attestation returns **400** `attestation_mismatch`, and a short
sample returns **400** `sample_too_short`. On success, a `verified` entry with
the attestation and sample goes into the audit log (`audit.py::log_verification`),
so a reviewer can look at the sample later.

The sample is kept but **deliberately not scored**. Plain writers are the
people my detector misjudges most, and the same detector shouldn't shut them
out of the credential.

**What it changed:** every later submission and `/content/<id>` response from
that writer carries `"verified_human": true`. The credential shows *alongside*
the label. It doesn't change the score, because the detector's estimate and
the writer's credential are separate facts, and a reader should see both.

```bash
$ curl -X POST http://127.0.0.1:5000/verify \
  -H "Content-Type: application/json" \
  -d '{"creator_id": "maria-07", "attestation": "I confirm that I write my own work and that I am a person.", "sample": "The committee'"'"'s deliberations, protracted as they were, ultimately foundered on a question of jurisdiction rather than of substance. Whether the municipal ordinance pre-empted the older county statute was never squarely resolved; counsel for both parties seemed content to leave the matter ambiguous. In retrospect, that ambiguity proved costly. Three years and two appeals later, the parcel remains undeveloped, its title clouded by an easement nobody can locate."}'
```

```json
{
  "creator_id": "maria-07",
  "message": "You're verified. Everything you submit now shows a verified-human badge.",
  "verified_at": "2026-10-29T01:06:26+00:00",
  "verified_human": true
}
```

**The credential showing on an item:** maria-07's next submission. Her
earlier item (above) still shows `false` in its log entry, because that's what
was true when it was decided.

```bash
$ curl http://127.0.0.1:5000/content/a18a8886-ccd3-4e6d-9d9d-a98369a9766d
```

```json
{
  "appeals": [],
  "confidence": 0.3885,
  "content_id": "a18a8886-ccd3-4e6d-9d9d-a98369a9766d",
  "creator_id": "maria-07",
  "guess": "unsure",
  "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.",
  "model_score": 0.4812,
  "phrase_score": 0.0,
  "status": "decided",
  "style_score": 0.4929,
  "submitted_at": "2026-10-29T01:06:26+00:00",
  "verified_human": true
}
```

**Its blind spot:** an attestation is a promise, not proof. Anyone can type
the sentence. What it does buy is accountability: the claim and the sample sit
in the audit log under that `creator_id`.

---

## How I Used AI

**Moment 1**

- *What I asked for:* I had Claude (Claude Code) wire the signals into
  `/submit` and run the calibration inputs plus a plain-human paragraph through
  each signal separately.
- *What came back:* A table showing the plain human paragraph scored 0.838
  combined, labelled **AI** under the starting 0.70 threshold, with both
  signals fooled (model 0.862, style 0.803).
- *What I changed:* I raised `AI_THRESHOLD` to 0.85 so only near-unanimous
  evidence earns the AI label. I then added the stock-phrase signal, which
  dropped that paragraph to 0.672. The remaining weakness is written up above
  instead of being tuned away.

**Moment 2**

- *What I asked for:* A combining rule that stops one signal from accusing
  a writer by itself. The first version capped the score below the AI threshold
  whenever either signal was under 0.5.
- *What came back:* After the threshold moved to 0.85, the math showed the
  cap could never fire. A weighted average can't reach 0.85 unless every signal
  leans AI.
- *What I changed:* I deleted the dead guard. The threshold now carries
  that rule, and the README shows the arithmetic.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 200 per day, on `POST /submit`
(`config.py::RATE_LIMIT_PER_MINUTE` / `RATE_LIMIT_PER_DAY`, the
`@limiter.limit(...)` decorator on `app.py::submit`). Limiting is on by default
(`RATE_LIMITING_ENABLED`).

**Why those numbers and not others:** A real writer submits a piece, reads the
label, maybe fixes a typo and resubmits. That's a handful an hour, so 10 a
minute never touches them, even someone pasting a batch of old poems. A script
mapping my thresholds needs hundreds of variations of one text to find where
`unsure` turns into `human`. At 10 a minute and 200 a day, one creator gets 200
probes a day at most, and each one leaves a log line. 200 a day is still far
above any honest writer's day.

**What a caller counts as — per creator_id (the stretch).**
`app.py::rate_limit_key` keys the limit on `creator_id`, and falls back to the
caller's address only when `creator_id` is missing or isn't a string. That is
right for the writer: a whole classroom or a family behind one home router
shares an IP address, and a per-address limit would lock all of them out
because of one busy person. It is wrong against an attacker who invents a new
`creator_id` for every request. The attack set does exactly that, so its 32 text
attacks never tripped the limit. A per-address limit fails the other way: one
script on a botnet looks like a thousand callers. I picked per-creator because
on a writing site a creator_id belongs to a signed-in account, so minting new
ones costs an attacker a sign-up each time. In production the fix is both: a
per-creator limit plus a generous per-address ceiling (say 60 a minute).

**The run of status codes when I pushed past it** (`python run_attacks.py --flood 15`,
`results/flood_2026-11-06_2220.md`):

```
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

The attack set's own flood family (`FL01`, 12 rapid submissions from one
creator) got the same result: 10 × 200, then 429, 429. Every 429 leaves a
`rejected` entry in the log (`app.py::rate_limited` → `audit.log_rejection`):

```json
{"creator_id":"flood_tester","event":"rejected","limit":"10 per 1 minute","reason":"rate_limited","status":"rejected","timestamp":"2026-11-07T06:20:08+00:00"}
```

---

## Attack Run — Before

`python run_attacks.py --set attack_set --label before` → full table with
content ids in `results/attack_run_2026-11-06_2220_before.md`. **56 attacks,
0 crashes, 6 broke.**

**How I judged held/broke.** I can't judge an evasion against "did it get
the AI label", because the clean, unedited AI essay these attacks are built
from scores **0.634, unsure**, *before any attack is applied* (model 0.669,
style 0.800, phrase 0.294). So an evasion **broke** only if it moved that text
from `unsure` down to `human`, and held if it stayed `unsure`. A
false-positive attack broke if human writing was labelled `ai`. A malformed
input broke if it got a label at all instead of a refusal, since a writing
label on emoji or control characters is a wrong answer. A prompt injection
broke if it moved the label the way the injection asked.

| ID | Family | Targeting | Status | Guess | Score | Verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.381 | HELD |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.386 | HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.490 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.604 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | **human** | 0.244 | **BROKE** |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.431 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.570 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.382 | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.565 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | unsure | 0.742 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.493 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | unsure | 0.633 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | unsure | 0.626 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | unsure | 0.700 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | unsure | 0.691 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.619 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.591 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | 0.370 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.364 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | **human** | 0.204 | **BROKE** |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.416 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.373 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.426 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.465 | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | **human** | 0.195 | **BROKE** |
| MF04 | malformed | text is only punctuation | 200 | **human** | 0.276 | **BROKE** |
| MF05 | malformed | text is a very long single word | 200 | unsure | 0.694 | **BROKE** |
| MF06 | malformed | text is emoji only | 200 | unsure | 0.694 | **BROKE** |
| MF07 | malformed | text is right-to-left script | 200 | unsure | 0.648 | HELD |
| MF08 | malformed | text is 60,000 characters | 400 | — | — | HELD |
| RQ01–RQ12 | malformed | no text, no creator_id, number/list/null text, object creator_id, array body, unparseable JSON, empty body, form-encoded, wrong content type, deeply nested | 400 ×12 | — | — | HELD ×12 |
| FL01_01–10 | flood_same_creator | 20 rapid submissions from one creator | 200 ×10 | human | 0.209 | HELD |
| FL01_11–12 | flood_same_creator | (same) | **429** ×2 | — | — | HELD |

| Family | Attacks | Held | Broke |
|---|---|---|---|
| evasion | 10 | 9 | 1 |
| false_positive | 8 | 8 | 0 |
| prompt_injection | 6 | 5 | 1 |
| malformed (text) | 8 | 4 | 4 |
| malformed (request) | 12 | 12 | 0 |
| flood_same_creator | 12 | 12 | 0 |
| **total** | **56** | **50** | **6** |

PI04 held because the label is fixed text chosen by `score_to_label`, so
nothing from the submission reaches it, and Flask escapes the JSON. PI05 held
because the audit log never stores the submitted text and `json.dumps` escapes
quotes, so the log line stays one valid JSON object (see the PI05 entry below).

**Ten audit log entries from the run** (`results/audit_extract.json`), picked
to show the failures and the near-misses:

```json
{"timestamp": "2026-11-07T06:20:15+00:00", "content_id": "0a786128-c238-4562-9b58-c788cf331d7c", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.2795, "combined_score": 0.2445, "label": "This reads like it was written by a person. Our automated check found nothing that suggests it was produced by an AI tool.", "status": "decided", "phrase_score": 0.0, "verified_human": false}
{"timestamp": "2026-11-07T06:20:17+00:00", "content_id": "f91b59f6-6ff8-4dc0-b7a8-72eadbd8a51f", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.3387, "combined_score": 0.2038, "label": "This reads like it was written by a person. Our automated check found nothing that suggests it was produced by an AI tool.", "status": "decided", "phrase_score": 0.0, "verified_human": false}
{"timestamp": "2026-11-07T06:20:18+00:00", "content_id": "234599ce-70c3-4a9a-82d6-a610638626ca", "creator_id": "attacker_MF03", "guess": "human", "model_score": 0.0, "style_score": 0.65, "combined_score": 0.195, "label": "This reads like it was written by a person. Our automated check found nothing that suggests it was produced by an AI tool.", "status": "decided", "phrase_score": 0.0, "verified_human": false}
{"timestamp": "2026-11-07T06:20:18+00:00", "content_id": "20a23e85-6ccb-4f1c-b7e6-bda29042e5bd", "creator_id": "attacker_MF04", "guess": "human", "model_score": 0.0112, "style_score": 0.9, "combined_score": 0.2756, "label": "This reads like it was written by a person. Our automated check found nothing that suggests it was produced by an AI tool.", "status": "decided", "phrase_score": 0.0, "verified_human": false}
{"timestamp": "2026-11-07T06:20:18+00:00", "content_id": "b09d0d67-5f9f-4747-a181-79dea03b78af", "creator_id": "attacker_MF05", "guess": "unsure", "model_score": 0.9976, "style_score": 0.65, "combined_score": 0.6938, "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.", "status": "decided", "phrase_score": 0.0, "verified_human": false}
{"timestamp": "2026-11-07T06:20:19+00:00", "content_id": "a76cafc0-af4f-43a8-85d8-e4517226c325", "creator_id": "attacker_MF06", "guess": "unsure", "model_score": 0.9969, "style_score": 0.65, "combined_score": 0.6935, "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.", "status": "decided", "phrase_score": 0.0, "verified_human": false}
{"timestamp": "2026-11-07T06:20:14+00:00", "content_id": "2a2f7c36-2fe3-43dc-9ed7-30a76f482dce", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.1635, "style_score": 0.8, "combined_score": 0.3806, "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.", "status": "decided", "phrase_score": 0.2941, "verified_human": false}
{"timestamp": "2026-11-07T06:20:16+00:00", "content_id": "d7d3e718-e749-42d6-9ada-d311348d843e", "creator_id": "attacker_FP04", "guess": "unsure", "model_score": 0.8329, "style_score": 0.6993, "combined_score": 0.6998, "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.", "status": "decided", "phrase_score": 0.3676, "verified_human": false}
{"timestamp": "2026-11-07T06:20:16+00:00", "content_id": "06f5f223-1319-40eb-b447-f16eb71679b8", "creator_id": "attacker_EV10", "guess": "unsure", "model_score": 0.9792, "style_score": 0.8401, "combined_score": 0.7416, "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.", "status": "decided", "phrase_score": 0.0, "verified_human": false}
{"timestamp": "2026-11-07T06:20:17+00:00", "content_id": "f6a907c2-bf67-4766-b59e-dbf42c79e3b2", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.6401, "style_score": 0.354, "combined_score": 0.4263, "label": "We can't tell how this was written. Our automated check gave mixed results, which happens with a lot of genuine human writing, so we are not making any claim about it either way.", "status": "decided", "phrase_score": 0.0, "verified_human": false}
```

**The single worst outcome:** **MF03**, a string of control characters with
two real words in it (`\x00\x01\x02 test \x1b[31mred\x1b[0m`), got *"This reads
like it was written by a person."* The service vouched for something that
isn't writing at all. A writer would read that label as a judgment the system
earned. If garbage can get it, the label tells you nothing, and that includes
when an honest writer gets it.

---

## Run Log and Verdicts

My five criteria across three trials. Text criteria: `run_eval.py --label before`
(`results/run_2026-11-06_2223_before.md`, scenarios in `scenarios.py`).
Criterion 4 needs a submit-then-appeal, which `run_eval.py` can't express, so I
extended the test with `check_appeals.py` (`results/appeal_check_2026-11-06_2223_before.md`).

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Human writing rarely called AI | ≤ 1 of 10 labelled `ai` | 0 / 10 | 0 / 10 | 0 / 10 | **MET** |
| 2. AI vs human scores far apart | mean(AI) − mean(human) ≥ 0.30 | 0.866 − 0.294 = 0.572 | 0.572 | 0.572 | **MET** |
| 3. All three labels reachable | each label ≥ 1 | ai 2, unsure 2, human 2 | same | same | **MET** |
| 4. Appeals recorded, 5 of 5 | 5/5 + unknown id → 404 | 5/5, 404 | 5/5, 404 | 5/5, 404 | **MET** |
| 5. Bad input → 400, never 500 | 6/6 400, 0 × 500, all logged | 6/6 | 6/6 | 6/6 | **MET** |

All three trials came back identical, to four decimal places. GPT-2 runs in
eval mode with no sampling, so for the same text it gives the same perplexity
every time. The "identical input can score differently" risk the brief warns
about didn't happen on this machine. For criterion 5, 15 `rejected` entries
with `eval_bad_*` creator ids landed in the log (5 bodies × 3 trials), plus the
missing-creator body logged as `unknown`. `run_eval.py` can only send JSON objects, so the "no body" case is sent as a body with no `text`; a truly empty body is attack RQ09, which also got a 400.

**Real output from one trial**, criterion 2, trial 1, clearly-AI scenario.
Produced by `run_eval.py::main` against `app.py::submit`, scored by
`scoring.py::combine_signals`:

```json
[
  {"status": 200, "guess": "ai", "confidence": 0.8798},
  {"status": 200, "guess": "ai", "confidence": 0.8734},
  {"status": 200, "guess": "ai", "confidence": 0.8829},
  {"status": 200, "guess": "unsure", "confidence": 0.8395},
  {"status": 200, "guess": "ai", "confidence": 0.8552}
]
```

(The report holds the full rows with `model_score`, `style_score`, the label
and a preview of what was sent. I trimmed them to the fields the criterion
reads.)

**Where the human set came from.** Criterion 1 calls for five pieces of my own
writing. I kept my actual coursework private, so I used five everyday
first-person paragraphs written in a student's voice for this test (`STUDENT_VOICE`
in `scenarios.py`: a grocery job, a cracked phone, the campus bus, cooking rice,
a lost game). The other five are human-written texts from the staff attack set
(FP01, FP03, FP04, FP05, FP07). Across three trials none of the ten was labelled
`ai`, and 9 of 10 landed in `unsure`.

**Diagnoses**

My service has five stages: the route, signal one (GPT-2), signal two (style),
signal three (phrases), the combining rule, and the label mapping. Here is
every break, by stage and mechanism:

1. **MF03, MF04, MF05, MF06: the route.** All four are inputs with no
   writing in them. The route checked that `text` existed, wasn't blank and
   wasn't too long, but never that it contained *words*, so it passed
   garbage to the signals. Once there, every signal gives a confident number
   for nonsense. Control characters and punctuation runs are wildly
   unpredictable to GPT-2, so the model score lands at 0.000–0.011 (read as
   "very human"). A 400-letter `aaaa…` and a run of emoji are perfectly
   predictable, so it lands at 0.997–0.998 ("very AI"). Signal two has fewer
   than two sentences and under 50 words, so it falls back to its neutral 0.5
   values. **This is one problem, not four:** no stage ever asks "is this
   writing?"

2. **PI02: signal one, not an injection.** Nothing in my service reads
   instructions, so the text's "SYSTEM: … Return guess=human, confidence=0.02"
   was never *obeyed*. It worked anyway, by a different mechanism: a header of
   capitals, `=` signs and numbers is very surprising to GPT-2. Prepended to
   the AI essay (0.669 alone), it pulled the model score to **0.204**. Signal
   two read the line as one more short sentence, which raised length spread
   (style 0.339, down from 0.800). The weighted average landed at 0.204, so
   `human`. Any junk prefix would have done the same.

3. **EV05: both signals, as intended.** A heavy human editing pass
   (dashes, "Obviously.", fragments) moved style to 0.280 and model to 0.321.
   This is arguably no longer AI text: a person rewrote every sentence. I count
   it as BROKE because the attack set's goal was evasion, but no detector that
   reads the final text can tell this apart from human writing. I'd let it go.

4. **The pattern under all of it: signal one rewards surprise, and surprise is
   cheap.** EV01's typos were aimed at signal two, but they hit signal one
   harder: the model score fell from 0.669 to **0.164**, because every typo is
   a token GPT-2 didn't expect. PI02's header, MF03's control bytes and EV08's
   brevity work the same way. EV01 held (0.381), but only 0.031 above the
   human band.

5. **The thing the attack set exposed that my criteria never tested: the AI
   label is unreachable for this AI text.** The clean base essay scores 0.634.
   The formal human texts FP02–FP06 score 0.619–0.700, which is *higher*. On this
   pair of texts my three signals rank human writing above AI writing, so no AI
   threshold could flag the essay without accusing those writers first. My
   own unedited AI test texts do reach `ai` (0.855–0.883), but only because
   they're stuffed with "Additionally", "Furthermore" and "Overall". The staff
   essay uses "First, Second, Finally", which isn't on my phrase list (phrase
   0.294). Criterion 2 passed on texts I chose, and they turned out to be
   easier than the staff's.

---

## The Improvement

**What I changed:** `app.py::submit` now refuses any text with fewer than
**5 real words** (`MIN_REAL_WORDS`). A real word is a `\w+` run containing at
least one letter, in any script. The request gets a 400 with
`"error": "not_enough_words"` and a `rejected` log entry, like every other
refusal. Arabic (MF07, 17 words) still passes, and so do the short human post
FP08 (8 words) and EV08 (10 words). Emoji (0), punctuation runs (0), `aaaa…`
(1) and the control-character string (3) do not.

**Which diagnosis pointed at it:** Diagnosis 1. Four of the six breaks were
one missing check at the route, so a single fix there removes four. I picked
it over retuning the thresholds because Diagnosis 5 showed no threshold can
separate the staff AI essay from formal human writing. Lowering the AI
threshold would have broken the false-positive family, which the system got
completely right.

### Attack Run — After

`python run_attacks.py --set attack_set --label after` →
`results/attack_run_2026-11-06_2223_after.md`. Only the rows that changed are
shown here; every other row matches the before run exactly.

| ID | Targeting | Before | After | Verdict |
|---|---|---|---|---|
| MF03 | text is control characters | 200 human 0.195 — BROKE | **400** | **HELD** |
| MF04 | text is only punctuation | 200 human 0.276 — BROKE | **400** | **HELD** |
| MF05 | text is a very long single word | 200 unsure 0.694 — BROKE | **400** | **HELD** |
| MF06 | text is emoji only | 200 unsure 0.694 — BROKE | **400** | **HELD** |
| MF07 | right-to-left script | 200 unsure 0.648 — HELD | 200 unsure 0.648 | HELD |
| EV05 | heavy human editing pass | human 0.244 — BROKE | human 0.244 | BROKE |
| PI02 | instruction as system message | human 0.204 — BROKE | human 0.204 | BROKE |

| | Held | Broke |
|---|---|---|
| Before | 50 | 6 |
| After | **54** | **2** |

**Did it help, and how do I know:** Yes, for that family and nothing else.
Four BROKE rows became 400s. The other 52 rows came back with the same
status, guess and score to three decimals, because the check runs before any
signal does. I also re-ran my own criteria (`results/run_2026-11-06_2224_after.md`,
`results/appeal_check_2026-11-06_2224_after.md`): all five still met in all three
trials, with identical scores.

The trade I made: a genuine four-word submission ("Went for a run.") is now
refused. A writer gets a clear message to send at least five words, rather
than a label the system can't back up on that little text.

---

## What's Still Broken

- **PI02 and any junk-prefix attack (signal one).** Prepending anything
  surprising (a fake header, random tokens, a block of code) drags GPT-2's
  score down and can carry AI text into `human`. What I'd do: score the
  text in windows and take the most AI-like window, so a bolted-on prefix
  can't dilute the rest, or strip lines that look like markup or headers
  before scoring. I stopped because both change what signal one measures,
  and that needs its own calibration run against the false-positive family.
- **EV05 (heavy human edit).** I'd leave it. Once a person has rewritten every
  sentence, the text really has a human author, and a detector that reads the
  final text can't see the history.
- **EV01 near-miss.** Typos sit 0.031 above the human band. A few more typos
  would break it. The fix belongs to the same work as PI02 (signal one treats
  misspellings as surprise), plus spell-normalising before GPT-2 scores.
- **The AI label can't catch the staff's AI essay (0.634).** This is the big
  one. My phrase list misses "First / Second / Finally"-style signposting, and
  the model signal scores formal human writing (FP02–FP06) higher than this AI
  text. What I'd do: widen the phrase list, then calibrate the whole
  system against a few hundred labelled texts instead of five. I stopped
  because five hand-picked calibration texts can't support moving a threshold
  safely. Doing it on these numbers would accuse the FP writers first.
- **Most honest writers get `unsure`, not `human`.** 9 of 10 texts in the
  human set land in the unsure band. Criterion 1 passes because nobody gets
  *accused*, but I never wrote a criterion for how often a writer gets the
  reassurance they deserve. That's a gap in my criteria, not just the code.

**The trade I'd make if this ran for real:** I'd keep the AI threshold high and
accept that most AI text comes back "unsure" instead of "AI". The cost of that
choice falls on the site and on readers, who can't fully trust an unflagged
piece. The cost of the opposite choice falls on plain, formal and
second-language writers, who'd be told their own work was machine-made.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

---

## Capstone

<!-- TODO (Manuel): one thing in here is still DRAFTED and must become yours
     before you submit — the five criteria in criteria.md. Milestone 4 says a
     criterion you didn't write is one you can't defend, and the numbers are
     mirrored in capstone_targets.py, so change both if you change one.
     Everything else below is measured output from runs that really happened;
     the result files in results/ are the originals. Delete this comment once
     the criteria are yours. -->

**What This Extends**

Project 4, **Provenance Guard** — the Flask safety service from units 7 and 8
that scores a piece of text on three signals, labels it, logs the decision and
takes appeals. Same repository, same system, no new project.

What's new is an **observability layer**: a second structured log that records
one entry per HTTP request rather than per decision, with per-stage timings
inside the request, a measured cost-per-run figure taken from those timings,
and a documented single-command run path that a stranger can follow. New files
are `obs.py` (the layer), `measure_cost.py` (the cost measurement),
`run_capstone_eval.py` and `capstone_targets.py` (the test harness) and
`test_obs.py` (a self-check for the layer). `app.py` gained the request hooks,
per-signal timers, a startup preload and a fault-injection route that is off
unless an environment variable turns it on. `config.py` gained one path.

Nothing about the detector, the signals, the weights, the thresholds, the
labels or the appeal path was touched. That was the point — criterion 10
checks it.

**The Shape**

**Shape A — deploy and instrument.** The extension *is* the operational layer:
the run path, the instrumentation, and the numbers that come out of it.

I picked A over C because the two things the brief requires in every shape —
a run path that isn't an editor and a structured log — are the two things this
service had least of. It wrote a decision trail from unit 7 and had no idea
how long anything took, what a request cost, or whether a request that never
became a decision happened at all. Adding a fourth signal (shape C) would have
been a more impressive sentence and a less honest answer to "can you see what
this is doing."

What I decided is **out of scope**, having thought about each one:

- **No fourth detection signal.** It would change what the system decides,
  which makes the regression check meaningless and turns one unit into two.
- **No hosting on Render.** Not a time problem — an arithmetic one. `torch`
  plus the `gpt2` weights are over a 512 MB free tier before a request
  arrives, and RUNNING.md has the table. Path B is the right answer here and
  the rubric treats it the same.
- **No dashboard or metrics UI.** A log you can read with `json.loads` answers
  the questions I wrote criteria about. A chart would be a second project.
- **No swap to a production WSGI server.** `gunicorn` is pinned in
  `requirements.txt` and cannot run on Windows at all — it imports `fcntl`.
  Replacing it with `waitress` means a new dependency in a file that pins
  everything on purpose, and buys nothing Path B asks for. RUNNING.md records
  the attempt and the traceback instead.

**Running It**

**Path B — local, with logs.** The full run path, the environment it needs,
the gunicorn finding and the clean-tree test are in
[RUNNING.md](RUNNING.md#the-capstone-run-path--path-b-local-with-logs). The
short version:

```bash
python -m venv .venv && . .venv/Scripts/activate && pip install -r requirements.txt
AI201_DEBUG=0 AI201_PRELOAD=1 python app.py
```

Startup loads the detector before it binds, so `/health` reports
`"detector_loaded": true` from the first request. It takes about six seconds
to come up for that reason — see The Improvement.

**Instrumentation**

Two logs, deliberately separate. `logs/audit.jsonl` is unit 7's decision trail
— what the service concluded, and the record a reviewer reads when a writer
appeals. `logs/requests.jsonl` is new: one record per HTTP request, whatever
became of it. Mixing them would spoil both, because the audit log is graded
evidence whose shape unit 8's tooling depends on.

Each request record holds eleven fields, every one present on every record and
`null` where it doesn't apply, so the file has exactly one shape:

| Field | What it holds |
|---|---|
| `timestamp` | when the request finished, UTC, to the millisecond |
| `request_id` | a short id, also returned to the caller in `X-Request-ID` |
| `method` | `GET` or `POST` |
| `route` | the matched rule (`/content/<content_id>`), not the filled-in path, so records group |
| `status` | the HTTP status actually sent |
| `duration_ms` | the whole request, measured around the handler |
| `creator_id` | who called, when the body carried one |
| `content_id` | the decision this produced, when it produced one |
| `outcome` | `decided`, `ok`, `error`, or the error code the handler chose |
| `stages` | per-stage milliseconds inside the handler |
| `exception` | the exception's type name, when the handler raised |

The submitted text is **not** copied here. It is already in the audit trail,
and a second copy in an operational log is a second place it can leak from.

Twelve entries from real runs, one of each kind the service produces. Taken
from `logs/requests.jsonl`, written by `obs.py::_write`, and also saved as
`results/log_extract.json`:

```json
{"timestamp": "2026-11-13T03:31:50.750+00:00", "request_id": "a64355882000", "method": "POST", "route": "/submit", "status": 200, "duration_ms": 154.76, "creator_id": "c10_hu_193148852126_4", "content_id": "9df6468b-8127-40b2-9b8a-ad0159a8a88d", "outcome": "decided", "stages": {"model_signal": 118.48, "style_signal": 0.41, "phrase_signal": 0.33, "scoring": 0.01}, "exception": null}
{"timestamp": "2026-11-13T03:30:31.943+00:00", "request_id": "a6a766a995d3", "method": "POST", "route": "/submit", "status": 200, "duration_ms": 4775.14, "creator_id": "cost_193027_1", "content_id": "3b2835e5-a53e-4f5b-9ccc-d9bbefc97fa1", "outcome": "decided", "stages": {"model_signal": 4748.4, "style_signal": 0.8, "phrase_signal": 0.61, "scoring": 0.01}, "exception": null}
{"timestamp": "2026-11-13T03:31:44.716+00:00", "request_id": "6ad0024ac92c", "method": "POST", "route": "/submit", "status": 200, "duration_ms": 591.78, "creator_id": "c9_193144109300_3", "content_id": "c4862bde-ab20-445e-a612-26a582462828", "outcome": "decided", "stages": {"model_signal": 525.16, "style_signal": 0.41, "phrase_signal": 0.36, "scoring": 0.01}, "exception": null}
{"timestamp": "2026-11-13T03:31:48.541+00:00", "request_id": "15de04b02bfa", "method": "POST", "route": "/submit", "status": 200, "duration_ms": 1009.91, "creator_id": "c9_193144109300_43", "content_id": "ffa50473-a124-470f-ad0a-9d2c2924f2fe", "outcome": "decided", "stages": {"model_signal": 960.18, "style_signal": 0.46, "phrase_signal": 0.36, "scoring": 0.01}, "exception": null}
{"timestamp": "2026-11-13T03:31:42.355+00:00", "request_id": "9a45b679ca61", "method": "POST", "route": "/submit", "status": 400, "duration_ms": 1.5, "creator_id": "cap_bad_number", "content_id": null, "outcome": "missing_text", "stages": {}, "exception": null}
{"timestamp": "2026-11-13T03:31:42.386+00:00", "request_id": "3238f5b066d4", "method": "POST", "route": "/submit", "status": 400, "duration_ms": 1.47, "creator_id": "cap_bad_huge", "content_id": null, "outcome": "text_too_long", "stages": {}, "exception": null}
{"timestamp": "2026-11-13T03:31:42.370+00:00", "request_id": "894eb294ff34", "method": "POST", "route": "/submit", "status": 400, "duration_ms": 1.42, "creator_id": null, "content_id": null, "outcome": "missing_creator_id", "stages": {}, "exception": null}
{"timestamp": "2026-11-13T03:31:42.402+00:00", "request_id": "8031c9ef5f1d", "method": "POST", "route": "/_fault/raise", "status": 500, "duration_ms": 1.18, "creator_id": null, "content_id": null, "outcome": "error", "stages": {}, "exception": "RuntimeError"}
{"timestamp": "2026-11-13T03:31:42.139+00:00", "request_id": "5ed154173949", "method": "POST", "route": "/appeal", "status": 200, "duration_ms": 19.15, "creator_id": null, "content_id": null, "outcome": "ok", "stages": {}, "exception": null}
{"timestamp": "2026-11-13T03:31:42.216+00:00", "request_id": "0090cd75f88b", "method": "GET", "route": "/content/<content_id>", "status": 200, "duration_ms": 16.14, "creator_id": null, "content_id": null, "outcome": "ok", "stages": {}, "exception": null}
{"timestamp": "2026-11-13T03:31:42.264+00:00", "request_id": "1fb9a92747bd", "method": "GET", "route": "/health", "status": 200, "duration_ms": 4.04, "creator_id": null, "content_id": null, "outcome": "ok", "stages": {}, "exception": null}
{"timestamp": "2026-11-13T03:31:42.268+00:00", "request_id": "c50cc906f368", "method": "GET", "route": "/no-such-route-193139272296", "status": 404, "duration_ms": 0.25, "creator_id": null, "content_id": null, "outcome": "ok", "stages": {}, "exception": null}
```

**Four failed runs are in there on purpose.** Three are refusals — `status`
400 with `outcome` naming which check rejected the input (`missing_text`,
`text_too_long`, `missing_creator_id`) and `stages` empty, because the request
never reached a signal. The fourth is a handler that raised: `status` 500,
`outcome: "error"`, `exception: "RuntimeError"`, from the fault-injection route
that exists only when `AI201_FAULT_INJECTION=1`. Criterion 7 is about exactly
these, and a crash recorded as a success would be worse than no record at all.

Two entries are worth reading side by side. The 4775 ms one is a cold start,
with 4748 ms of it inside `model_signal` — 99.4%. The 154 ms one is the same
work warm. The 1009 ms one is a warm request during the 10-at-a-time load of
criterion 9, where contention for the CPU stretched the same stage to 960 ms.
None of that was visible before this unit.

**What It Costs**

Nothing here calls a paid API. All three signals run on this machine — GPT-2
through `transformers`, and two pure-Python passes — so the real cost of a run
is **seconds of compute**, and that is what I measured.

**Measured: 0.118 seconds of compute per warm run.**

How I got it, which is `measure_cost.py::main`: it sends 10 submissions of one
fixed text, one at a time, each with its own `creator_id` so the per-creator
rate limit never fires, then reads each request's duration back out of
`logs/requests.jsonl` by matching the `X-Request-ID` the service returned. The
durations are therefore the service's own measurements, not timings taken from
the client, so curl and loopback overhead are not in the number. The run is
`results/cost_2026-11-12_1935_final.md`:

| | ms |
|---|---|
| mean | 117.69 |
| median | 116.69 |
| min | 105.58 |
| max | 131.76 |
| mean `model_signal` | 89.18 — **75.8% of a run** |

The first request after a start is excluded and reported separately, because
it carries the one-time model load and is not a per-run cost. Averaging it in
would give a number describing neither a cold run nor a warm one.

**A hundred submissions a day**: 100 × 0.118 s = **11.8 seconds of compute per
day**. On one laptop core that is free in money and unnoticeable in time; what
it actually buys is headroom. A hundred a day is 0.0014 requests per second,
and the service handled 10 concurrent requests in criterion 9 with the slowest
at 1.01 s, so the limit here is nowhere near arithmetic — it is the 550 MB of
resident model that stops this fitting a free host at all.

One honest note on the cold start: it is not a stable number. Measured across
restarts it ran 39.9 s the very first time, then 9.1 s, then 4.8 s as the
operating system's file cache warmed. Any claim about it is a range, not a
figure.

**Run Log and Verdicts**

Five criteria, three trials each, produced by `run_capstone_eval.py::main`
with targets read from `capstone_targets.py`. Full output with per-trial
measurements is in `results/capstone_run_2026-11-12_1929_before.md`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 6. Every request leaves exactly one complete record | 30 of 30, all 11 fields | 30/30 | 30/30 | 30/30 | MET |
| 7. A request that fails is recorded as having failed | 7 of 7 as failures, 0 as ok | 7/7 | 7/7 | 7/7 | MET |
| 8. A warm submission answers in under 250 ms | median < 250 ms, 9 of 10 < 400 ms | 149.57 ms | 150.13 ms | 154.0 ms | MET |
| 9. The log survives ten times the normal rate | 50 records, 0 malformed, 50 distinct ids | 50/50, 0 bad | 50/50, 0 bad | 50/50, 0 bad | MET |
| 10. The extension changed nothing about the verdicts | AI mean − human mean ≥ 0.30 | 0.4837 | 0.4837 | 0.4837 | MET |

Real output, criterion 7, trial 1, from `run_capstone_eval.py::criterion_7`:

```json
{
  "requests_sent": 7,
  "fault_route_available": true,
  "response_statuses": [400, 400, 400, 400, 400, 400, 500],
  "records_gained": 7,
  "recorded_as_failure": 7,
  "recorded_as_ok": 0,
  "status_400_records": 6,
  "status_500_records": 1,
  "500s_naming_exception": 1,
  "passed": true
}
```

**All five met, so the honest question is whether the targets were low.** Two
of them were, and one was not.

- **Criterion 8 was too loose.** I set 250 ms against a measured warm median
  of about 147 ms — nearly 1.7× headroom, so the target could only have failed
  if something went badly wrong rather than slightly wrong. It never came
  within 60% of the line in six trials across both runs.
- **Criterion 10 is loose by construction and I'd keep it.** It re-uses unit
  7's target deliberately: a regression check works only if the bar doesn't
  move, and the measured separation of 0.4837 against a 0.30 target is the
  margin the original criterion already had. Tightening it would make it a
  different criterion rather than a stricter one.
- **Criteria 6, 7 and 9 are at their floors.** 30 of 30, 0 recorded as ok, 0
  malformed lines. There is no stricter version of "no record is missing" — the
  only way these get harder is a larger or nastier set of requests, not a
  different number, and that is the thing I'd change rather than the target.

Nothing was missed, so there is no stage-and-mechanism diagnosis to write
under this table. The one diagnosis this unit produced came out of the
instrumentation rather than a failed criterion, and it is in The Improvement.

**The Improvement**

**What I changed:** `app.py::main` now calls `detector.warm_up()` at startup,
before the server binds, so GPT-2 is loaded before the first request instead
of during it. Gated by `AI201_PRELOAD`, default on. Nine lines.

**The diagnosis it followed.** This came from the request log, not from a
missed criterion. Every cold start recorded a `/submit` between 4.8 and 39.9
seconds with 99.4% of the duration inside the `model_signal` stage, against a
warm median near 150 ms. **The stage is the model load and the mechanism is
lazy loading**: `detector._load()` runs on first use, so whichever request
arrived first paid for every request after it. The function to fix it already
existed — `detector.warm_up()`, shipped in the starter and called by nothing.

The fix does not make the load cheaper. It moves who waits: the operator, who
is already waiting for the service to come up, instead of a writer who is not.
Startup goes from instant to about six seconds, which is the cost, and
RUNNING.md says so.

**Before and after, each measured on a freshly restarted service** —
`results/cost_2026-11-12_1930_coldstart_before.md` and
`results/cost_2026-11-12_1931_coldstart_after.md`:

| | First `/submit` after start |
|---|---|
| Before | **4775.14 ms** (4748 ms in `model_signal`) |
| After | **310.92 ms** |

**15× faster on the first request.** And the full criterion set, re-run three
trials in the same format — `results/capstone_run_2026-11-12_1931_after.md`:

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 6. Every request leaves exactly one complete record | 30 of 30, all 11 fields | 30/30 | 30/30 | 30/30 | MET |
| 7. A request that fails is recorded as having failed | 7 of 7 as failures, 0 as ok | 7/7 | 7/7 | 7/7 | MET |
| 8. A warm submission answers in under 250 ms | median < 250 ms, 9 of 10 < 400 ms | 106.34 ms | 112.45 ms | 140.89 ms | MET |
| 9. The log survives ten times the normal rate | 50 records, 0 malformed, 50 distinct ids | 50/50, 0 bad | 50/50, 0 bad | 50/50, 0 bad | MET |
| 10. The extension changed nothing about the verdicts | AI mean − human mean ≥ 0.30 | 0.4837 | 0.4837 | 0.4837 | MET |

**Did it help?** Yes, and slightly more than I expected. The cold start was the
target and it fell 15×. Criterion 8's warm median also improved, from
149.57/150.13/154.0 ms to 106.34/112.45/140.89 ms — about 25% — which I did
not predict and can only partly explain: the model's pages are fully resident
before any request arrives, so warm requests stop competing with a first
request that is still faulting weights in from disk. Criterion 10 came out
identically to four decimal places, which is the result I wanted there: the
change moved when work happens, not what the service decides.

**The trade.** Startup is now six seconds slower, and `AI201_PRELOAD=0`
restores the old behaviour for anyone who wants a fast start and is willing to
make the first caller pay.

**What's Still Broken**

Every criterion was met, so this section is about what the targets didn't ask
and what I found anyway.

**The target I'd tighten, and to what.** Criterion 8, from "median under
250 ms" to **"median under 150 ms and 10 of 10 under 250 ms"**. The measured
median after the improvement is 106–141 ms, so 150 ms is a real line rather
than a formality, and moving the per-run clause from 9-of-10-under-400 to
10-of-10-under-250 removes the free pass for one slow run. I would not have
set that before measuring, which is the honest reason it isn't the target
above.

**The one thing I'd do first.** A request that matched no route is recorded
with `status: 404` and `outcome: "ok"` — visible in the twelfth log entry
above. `outcome` defaults to `"ok"` for anything that didn't raise, and only
handlers that call `obs.note()` say otherwise, so every 404 and every error
produced by Flask rather than by my code reads as a success. Criterion 7 did
not catch it because all seven of its requests go through handlers that do
call `note()`. The fix is three lines — derive the default from the status code
instead of from whether an exception fired — and I'd do it first because it is
the one case where this log currently says something untrue, and the whole
extension rests on the log being trustworthy.

**What else is left, and why I stopped.**

- **Per-run cost isn't a field in the log.** It is computed afterwards by
  `measure_cost.py` from `duration_ms`. Writing it into each record would let
  anyone read the cost of a single request without re-deriving it. I stopped
  because the criteria I wrote are answerable from the timings as they are,
  and adding a field changes the record shape that criterion 6 checks.
- **In-memory rate limiting still forgets everything on restart.** Unit 8
  named this and it is still true; the storage backend is `memory://`. Out of
  scope on purpose — it needs Redis, which is a dependency and a service.
- **The load observation is 10 concurrent, not sustained.** Criterion 9 fires
  50 requests ten at a time and the log holds up, but nothing here runs for an
  hour. A slow leak or a log that degrades at the millionth line would not
  show up in a 50-request burst.
- **Nothing is hosted.** Path B by arithmetic, not by preference, and
  RUNNING.md has the memory table. The consequence is that no claim in this
  submission covers a sleeping instance, a cold container or a network hop.

**If this were real and I had another unit**, the one thing I'd do first is
make the log answer "was the decision any good" rather than only "did the
request finish." Right now I can prove the service is fast and that it records
everything; I cannot query, from the logs alone, how often it labels a human
as AI — the thing the whole system exists to get right and the thing unit 7's
criterion 1 says costs a real person the most when it goes wrong. That means
joining the request log to the audit log on `content_id` and keeping a running
false-positive rate over the appeals that get upheld. Everything else here is
plumbing by comparison.

**How I Used AI**

**Moment 1**

- *What I asked for:* Request-level logging that would record a handler which
  raised, with the exception's type, and a self-check alongside it to prove the
  recording worked.
- *What came back:* An `obs.py` hooking `before_request`, `after_request` and
  `teardown_request`, with the exception captured in the teardown hook. It read
  correctly and it was wrong: two of the self-check's 21 assertions failed,
  because the record for a raising handler came out `status: 500` but
  `outcome: "ok"` and `exception: null`.
- *What I changed:* Flask turns an uncaught exception into a 500 and then
  finalizes that response, so `after_request` runs and writes the record before
  `teardown_request` is ever handed the exception. I moved the capture onto the
  `got_request_exception` signal, which fires while the exception is still in
  hand, and kept teardown as the fallback for when the response is never
  finalized at all. The only reason this surfaced is that the test was asked
  for in the same breath as the code — without it every crash would have been
  logged as a success, and criterion 7 would have passed while measuring
  nothing.

**Moment 2**

- *What I asked for:* The Path B run path written into `RUNNING.md`, including
  the milestone's step about cloning into a new folder and following my own
  instructions.
- *What came back:* A section headed "Tested from a clean checkout" reporting a
  first failure of `ModuleNotFoundError: No module named 'flask'` and two
  further steps — plausible, fluent, and the output of nothing. No clean
  checkout had been made.
- *What I changed:* I ran it. The real first failure was
  `ModuleNotFoundError: No module named 'flask_limiter'` at `app.py` line 77,
  because this machine's system Python already had `flask` — a worse failure
  than the invented one, since it breaks forty lines into the file rather than
  on the first import, and it is the version a reader with some of the packages
  actually hits. I rewrote the section from the real transcript, moved
  `pip install -r requirements.txt` above the run command because of it, and
  recorded that the copy was of the working tree rather than a `git clone`,
  since this unit's work wasn't committed when the test ran. The lesson I'm
  keeping is that a generated write-up will describe a test it never ran, and
  the tell is that it reads better than real output does.
