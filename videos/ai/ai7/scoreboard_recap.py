"""Presentation contract for the original, differently scored counting rows.

This validates display inputs, not the empirical scores or historical training.
Keep the original values; these rows are not a matched-cohort experiment.
"""

import math


def recap_rows(scoreboard):
    names = (("best", r"Part 1 best"), ("kn", r"Kneser--Ney"),
             ("infini", r"Capped suffix + KN"))
    rows = []
    for key, name in names:
        matches = [r for r in scoreboard["rows"] if r.get("key") == key]
        if len(matches) != 1:
            raise ValueError(f"Expected exactly one counting row: {key}")
        bits = matches[0]["bits"]
        if isinstance(bits, bool) or not isinstance(bits, (int, float)) or not math.isfinite(bits) or bits < 0:
            raise ValueError(f"Invalid bits per character: {key}")
        rows.append((key, name, bits))
    return rows


COHORT_NOTE = (
    r"Bits per scored character; original, different starting positions. \\ "
    r"Part 1 order: passage-selected; KN order: validation-selected. \\ "
    r"Not a matched-cohort comparison with Part 1."
)
