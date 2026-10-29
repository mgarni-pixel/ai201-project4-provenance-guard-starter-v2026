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
