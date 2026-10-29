"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies. ← TODO

    Returns:
        A float. Decide yourself what scale it's on and which direction means
        "more human" — then write that down, because your combining rule
        depends on knowing it.

    A hint on what you're reaching for: the standard deviation of sentence
    lengths, probably divided by the mean so a long text and a short one are
    comparable. `statistics.stdev` is imported for you.

    Watch the edge case: a one-sentence submission has no spread at all, and
    `stdev` raises on fewer than two values. Decide what that should return
    before the attack set decides for you.
    """
    # Coefficient of variation of words-per-sentence. Higher = lumpier = more human.
    # Fewer than two sentences has no spread to measure: returns 0.0, and
    # style_signal treats that as "no evidence" rather than as "very AI".
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n]
    if len(lengths) < 2:
        return 0.0
    return statistics.stdev(lengths) / statistics.mean(lengths)


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words. ← TODO

    Returns:
        A float between 0 and 1. Higher means more varied vocabulary.

    Worth knowing before you rely on it: this measure falls as text gets
    longer, because common words repeat. Two texts of different lengths aren't
    directly comparable on it, and if your test inputs vary a lot in length,
    that alone can look like a signal.
    """
    # Moving-average TTR over 50-word windows, so long and short texts compare
    # fairly. Under 50 words it falls back to plain TTR.
    ws = words(text)
    if not ws:
        return 0.0
    window = 50
    if len(ws) <= window:
        return len(set(ws)) / len(ws)
    ratios = [len(set(ws[i:i + window])) / window for i in range(len(ws) - window + 1)]
    return statistics.mean(ratios)


def punctuation_density(text: str) -> float:
    """
    How much punctuation, relative to length. ← TODO

    Returns:
        A float. Whether you count all punctuation or only some kinds — commas,
        semicolons, dashes — is a real choice. Semicolons and em dashes are
        more interesting than full stops, because they vary more between
        writers.
    """
    # "Expressive" marks per 100 words: ; : ! ? ( ) dashes, quotes, ellipses.
    # Plain . and , are left out — every writer uses those at about the same rate.
    ws = words(text)
    if not ws:
        return 0.0
    marks = len(re.findall(r"[;:!?()—–\"“”]|--|\.\.\.|…| - ", text))
    return 100 * marks / len(ws)


def _ramp(value: float, human_end: float, ai_end: float) -> float:
    """Linear 0–1 map: value at human_end -> 0.0, at ai_end -> 1.0, clipped."""
    t = (value - human_end) / (ai_end - human_end)
    return min(max(t, 0.0), 1.0)


# Calibration points for each measure: (value that reads fully human, value that reads fully AI)
SPREAD_RANGE = (0.70, 0.25)
TTR_RANGE = (0.85, 0.65)
PUNCT_RANGE = (5.0, 0.5)
STYLE_WEIGHTS = {"spread": 0.5, "ttr": 0.2, "punct": 0.3}


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.** ← TODO

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.

    Test it on the four calibration inputs from Milestone 4 — clearly AI,
    clearly human, plain conventional human writing, lightly-edited AI — before
    you trust it. Plain and ordinary, not formal: formal prose reads as *human*
    to signal one, and it is plain writing that gets accused.
    """
    n_sentences = len(sentences(text))
    parts = {
        # one sentence has no spread: neutral, not evidence either way
        "spread": _ramp(sentence_length_spread(text), *SPREAD_RANGE) if n_sentences >= 2 else 0.5,
        # under 50 words almost every word is new, so TTR says nothing: neutral
        "ttr": _ramp(type_token_ratio(text), *TTR_RANGE) if len(words(text)) > 50 else 0.5,
        "punct": _ramp(punctuation_density(text), *PUNCT_RANGE),
    }
    score = sum(STYLE_WEIGHTS[k] * v for k, v in parts.items())
    return round(score, 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
