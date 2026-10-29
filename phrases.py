"""
Signal three: the stock-phrase signal. (Stretch feature.)

Signal one measures how predictable the text is. Signal two measures its
shape. This one measures *word choice*: how often the text leans on the stock
transitions chat assistants reach for — "additionally", "overall", "it is
important to", "furthermore", "plays a crucial role".

Why that might differ: assistant models are tuned toward tidy, signposted
essays, so these connectives turn up far more often than in most human writing.

⚠️ **The blind spot.** It's a word list. It can't see anything not on the list,
so an AI told to "avoid clichés" sails through, and a human who writes formal
reports full of "however" and "furthermore" gets pushed toward AI. Deleting
five words defeats it completely.

    python phrases.py "some text to look at"
"""

import re

from stylometry import words

STOCK_PHRASES = [
    "additionally", "furthermore", "moreover", "overall", "in conclusion",
    "it is important to", "it is essential to", "it is worth noting",
    "plays a crucial role", "plays a vital role", "a wide range of",
    "a variety of", "in today's", "ensure that", "significant impact",
    "potential to", "by working together", "for example", "however",
    "in summary", "on the other hand", "as a result", "delve",
]

# Stock phrases per 100 words: 0 reads fully human, 4+ reads fully AI.
AI_END = 4.0


def phrase_density(text: str) -> float:
    """Stock phrases per 100 words."""
    ws = words(text)
    if not ws:
        return 0.0
    lowered = " ".join(ws)
    hits = sum(len(re.findall(rf"\b{re.escape(p)}\b", lowered)) for p in STOCK_PHRASES)
    return 100 * hits / len(ws)


def phrase_signal(text: str) -> float:
    """0–1 score. **Higher means more likely AI.**"""
    return round(min(phrase_density(text) / AI_END, 1.0), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "Additionally, it is important to note that technology plays a crucial "
        "role in society. Overall, it has the potential to help everyone."
    )
    print(f"phrase_density   {phrase_density(text):.2f} per 100 words")
    print(f"phrase_signal    {phrase_signal(text)}   (higher = more likely AI)")
