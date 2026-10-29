"""
Turning two numbers into one, and one number into something a person can read.
← YOU BUILD THIS IN MILESTONES 4 AND 5

Two functions live here, and both are stubs.

`combine_signals` is where your false-positive decision from Milestone 1
actually gets made. Everything above it — the labels, the appeal path — is
downstream of a number this function produced.

`score_to_label` is where you stop writing for a machine and start writing for
a person. A score of 0.62 means nothing to a writer.

⚠️ Your README's **Signals and Scoring** section has to name the file and
function holding your combining rule. The grader checks your code against what
you claim, so that line should read `scoring.py::combine_signals`.
"""

import config


def combine_signals(model_score: float, style_score: float, phrase_score: float = 0.0) -> float:
    """
    Combine the 0–1 signals into one 0–1 score. Higher = more likely AI.

    Rule: weighted average — model 0.5, style 0.3, stock phrases 0.2
    (config.py). No separate disagreement rule is needed: with AI_THRESHOLD at
    0.85, any two signals maxed out with the third at zero top out at 0.80, so
    the AI label needs all three leaning AI. One signal, or even two, can never
    accuse a writer on their own; a split lands in "unsure" or "human".
    """
    score = (
        config.WEIGHT_MODEL_SIGNAL * model_score
        + config.WEIGHT_STYLE_SIGNAL * style_score
        + config.WEIGHT_PHRASE_SIGNAL * phrase_score
    )
    return min(max(score, 0.0), 1.0)


def score_to_label(score: float) -> tuple[str, str]:
    """
    Turn a score into a guess and the text a reader actually sees.
    ← TODO (Milestone 5)

    Returns:
        (guess, label_text) — where `guess` is a short machine-readable string
        like "ai" / "human" / "unsure", and `label_text` is the full sentence
        shown to a person.

    ⚠️ Write the label text for someone who has never heard the word
    "threshold".

        ✗ "human, 0.81 confidence"
        ✓ "We think this was probably written by a person."

    All three labels have to be **reachable**. If no score can produce one of
    them, your ranges have a gap — and Milestone 5 asks you to submit text that
    produces each one, which is how you'd find out.

    The hardest one to write is "unsure". It has to admit uncertainty without
    sounding like an accusation, because the person reading it may well have
    written every word themselves. Your breakout asks your group what they'd
    think if they got it on their own work. That question is the whole
    milestone.
    """
    if score >= config.AI_THRESHOLD:
        return "ai", LABEL_AI
    if score <= config.HUMAN_THRESHOLD:
        return "human", LABEL_HUMAN
    return "unsure", LABEL_UNSURE


LABEL_HUMAN = (
    "This reads like it was written by a person. Our automated check found "
    "nothing that suggests it was produced by an AI tool."
)
LABEL_UNSURE = (
    "We can't tell how this was written. Our automated check gave mixed "
    "results, which happens with a lot of genuine human writing, so we are "
    "not making any claim about it either way."
)
LABEL_AI = (
    "This looks a lot like text produced by an AI writing tool. This is an "
    "automated estimate, not a final judgment, and it can be wrong. If you "
    "wrote this yourself, you can appeal and a person will review it."
)


def label_ranges() -> list[tuple[str, str]]:
    """
    The score range each label covers. Your README needs these beside the
    label text — given to you so the numbers can't drift apart from config.py.
    """
    return [
        ("high-confidence human", f"0.00 – {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f"{config.HUMAN_THRESHOLD:.2f} – {config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00"),
    ]
