# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. Human writing is rarely called AI

Of 10 pieces of human writing (5 I wrote myself, 5 plain human paragraphs such
as student essays and forum posts), **at most 1** gets the high-confidence AI
label (`guess == "ai"`), and this holds in **each** of three trials.

**Why this target:** On a writing site, calling a real writer a cheat costs
that person far more than a missed AI piece costs the site. One in ten is
already a lot of people to wrong; I won't accept more, and the unsure band plus
the appeal path exist to catch the rest. Half the set is *plain* writing on
purpose: my model signal (GPT-2 perplexity) rewards short sentences and common
words, so plain human writers are the people most likely to be wrongly accused.

---

## 2. Clearly-AI and clearly-human text score far apart

The mean combined score of 5 clearly-AI texts (unedited chatbot output) is
**at least 0.30 higher** than the mean combined score of 5 clearly-human texts
(personal, informal writing), in each of three trials.

**Why this target:** If the two groups sit closer than 0.30 on a 0–1 scale,
they'd both sit inside my unsure band (0.35–0.85, half the whole scale), and
the labels would be telling readers almost nothing.

---

## 3. All three labels are reachable

Across the calibration set (clearly AI, clearly human, plain human, lightly
edited AI, plus the texts from criteria 1–2), **each of the three labels
(`ai`, `unsure`, `human`) appears at least once**, and every response's
`confidence` maps to exactly one label using the ranges in the README.

**Why this target:** A label nobody can reach is a promise the system never
keeps. If "human" can never appear, every honest writer is at best "unsure".
My AI threshold sits deliberately high (0.85), and a weighted average can only
land between its inputs, so the AI label is the one at real risk of being
unreachable. This criterion checks I didn't push the threshold out of range.

---

## 4. Every appeal is recorded and changes status — 5 of 5

For 5 appeals sent with real `content_id`s, **5 of 5** return HTTP 200 with
`status: "under_review"`, and `GET /log` shows a new `appeal` entry for that
`content_id` with the writer's reasoning, while the original `decided` entry is
still present unchanged. An appeal with an unknown `content_id` returns 404 and
writes no appeal entry.

**Why this target:** The appeal is the only thing between a wrong accusation
and nothing. It has to work every time, not most of the time, and the
original decision must survive so the review can see what was decided.

---

## 5. Bad input gets a clear 400, never a crash

For these 6 inputs to `/submit` — no body, `text` missing, `text` empty or
only spaces, `text` not a string, `creator_id` missing, and `text` over
20,000 characters — **6 of 6** return HTTP 400 with a JSON `error` code and a
`message`, **0** return a 500, and each one writes a `rejected` entry to the
audit log.

**Why this target:** A 500 on malformed input is the most common real failure
there is, and it tells the caller nothing. A rejection that leaves no log
trace is an attack I could never see afterwards. The 20,000-character cap
exists because GPT-2 runs inline in the request; an enormous body would tie
up the service for everyone else.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Capstone criteria — Unit 9

<!-- TODO (Manuel): these five were DRAFTED, not written by you. Milestone 4
     says the criteria must be yours and that a criterion you didn't write is
     one you can't defend. Rewrite each sentence and each reason in your own
     words — keep, tighten or loosen the numbers as you see fit — then delete
     this comment. The runner reads its targets from capstone_targets.py, so
     change a number there too if you change one here. -->

Five criteria for the capstone extension — the observability layer added in
unit 9. Written before any of the capstone test runs.

**Four of the five are about the extension.** The fifth is a regression check:
an extension that breaks what it extends is a regression, and the point of
instrumenting a service is to learn about it without changing what it decides.

The cold-start measurement in Milestone 3 came before these, which is the order
the brief sets — Milestone 3 measures the cost, Milestone 4 writes the
criteria. So the latency targets below are informed by a measured warm median
of about 147 ms and a cold start between 9 and 40 seconds, and I say so rather
than pretending the numbers came from nowhere.

---

## 6. Every request leaves exactly one complete record

Across one trial of 30 requests to the service — a mix of `/submit`,
`/appeal`, `/content/<id>`, `/health` and one call to a URL that doesn't
exist — `logs/requests.jsonl` gains **exactly 30 records**, and **30 of 30**
carry all eleven fields (`timestamp`, `request_id`, `method`, `route`,
`status`, `duration_ms`, `creator_id`, `content_id`, `outcome`, `stages`,
`exception`), with `null` where a field doesn't apply. This holds in **each**
of three trials.

**Why this target:** Thirty of thirty, not twenty-nine. This is the criterion
the whole extension rests on — every later claim about latency, cost or
failure reads its numbers out of this file, so a log that drops one request in
thirty makes every other number in the submission approximate in a way I
couldn't quantify. One shape for every record is part of the same point: a
file I have to parse two ways is one I will eventually parse wrongly. The
unknown URL is in the set deliberately, because a request that matches no
route is the case most likely to slip past a hook that assumes one did.

---

## 7. A request that fails is recorded as having failed

For seven deliberately broken requests — the six bad inputs from criterion 5
(no text, text missing, text empty, text not a string, creator_id missing,
text over 20,000 characters) plus one request that makes a handler raise —
**7 of 7** leave a record whose `outcome` names the failure rather than
reading `ok`. The six bad inputs record `status` 400 and an `outcome` matching
the error code in the response body; the raising request records `status` 500
and the exception's type name in `exception`. **0 of 7** are recorded as
successes. This holds in **each** of three trials.

**Why this target:** Seven of seven because a failure recorded as a success is
worse than no record at all — it is a number that will be quietly wrong in
every count I make afterwards, and nothing about it looks wrong. Unit 8's
audit log already proved the version of this that matters for attacks: a
rejection that leaves no trace looks exactly like a quiet afternoon. The
raising request is included because that path is the one Flask handles
differently — the response is finalized before the exception reaches teardown,
so an instrumentation layer can report a 500 with `outcome: "ok"` and look
fine while being useless.

---

## 8. A warm submission answers in under 250 ms

Over 10 consecutive `/submit` requests after the model is already loaded, the
**median** `duration_ms` recorded by the service is **under 250 ms**, and
**at least 9 of 10** individual runs are under 400 ms. Measured warm only —
the first submission after a start is excluded and covered by what the README
says about cold starts. This holds in **each** of three trials.

**Why this target:** 250 ms is a little under twice the measured warm median,
which leaves room for an ordinary laptop doing other things without passing
anything that would feel slow to a person waiting on a verdict. I state warm
explicitly because the brief warns that a latency criterion which doesn't say
warm or cold has measured something its author didn't intend, and on this
service the gap is roughly three hundred to one — a target that silently
included the cold start would describe neither case. The median rather than the
mean, because one 9-second cold run would drag a mean of ten past any target I
could defend while nine of the ten were fine.

---

## 9. The log survives ten times the normal rate

With 50 `/submit` requests issued at roughly ten times the pace of
criterion 8 — ten at a time rather than one after another — the log gains
**exactly 50 records**, **0** lines fail to parse as JSON, and **50 of 50**
carry a distinct `request_id`. This holds in **each** of three trials.

**Why this target:** Appending from several threads at once is where a log
like this actually breaks, and it breaks by interleaving two half-written
lines into one unparseable row — which takes out not just the two requests
involved but my ability to read the file at all. Zero malformed lines is the
only target worth setting, because one is already a corrupted evidence trail.
Distinct ids matter because the only way I match a measurement back to a
request is by that id, and a duplicate would silently merge two runs into one.
Ten at a time is a modest load, and that is the point: if it fails here it
would certainly fail anywhere real.

---

## 10. The extension changed nothing about the verdicts

Unit 7's criterion 2, re-run against the instrumented service: the mean
combined score of the 5 clearly-AI texts is **at least 0.30 higher** than the
mean combined score of the 5 clearly-human texts, in **each** of three trials.

**Why this target:** Same target as the original on purpose — a regression
check is only a check if the bar doesn't move. The observability layer wraps
the three signals in timers and writes a second log file, and neither of those
should be able to touch a score. If this one misses, the extension broke the
system it was supposed to be watching, and that outranks everything else in
this submission.
