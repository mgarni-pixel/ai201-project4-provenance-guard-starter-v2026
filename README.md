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

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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
