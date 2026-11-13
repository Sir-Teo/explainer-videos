"""The Variations ledger: one row per finished part (what was done to the Tune, how long it runs, what was measured).

A part's own row comes from its ``compute.py`` (``load("variation")``); the rows of the parts before it are kept
here, copied from those parts' results when they were finished, so that a part's film does not need another part's
cache."""

LEDGER = [
    {"part": 1, "title": r"on one simulated string: six positions of one bridge", "seconds": 28.65,
     "measure": r"every interval within 0.6 cents of its ratio"},
    {"part": 2, "title": r"on six bottles, tuned by how much water is in them", "seconds": 26.4,
     "measure": r"every bottle within 1 cent of its note"},
    {"part": 3, "title": r"assembled from pure tones: 1, 2, 3, 5, 8 and 16 partials, phrase by phrase", "seconds": 27.95,
     "measure": r"its brightness rises 2.2 times from the first phrase to the last"},
    {"part": 4, "title": r"with no fundamentals, then with no octaves: the notes the ear supplies", "seconds": 27.105,
     "measure": r"the pitch model finds every missing fundamental within a cent"},
]


def rows_before(part: int) -> list[dict]:
    return [r for r in LEDGER if r["part"] < part]
