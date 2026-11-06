"""Precompute everything in Part 40 of *Philosophy, Built* ("Beauty").

    python -m videos.philosophy.philosophy40.compute            # everything missing (seconds)

Items:
    tuning        the Pythagorean comma, the spiral of fifths, and equal temperament
    temper        Pythagorean, quarter-comma meantone and equal temperament compared
    curve         the dissonance curve of two harmonic tones, and its minima
    stretched     the same with stretched partials: the minima move
    wallpaper     the seventeen wallpaper groups, generated and classified
    patterns      a motif under each group's operations, for drawing
    elements      the mirrors, glides and rotation centres of p4m, for drawing
    compress      how far zlib can compress five images
    progress      compression progress of a learning observer (Schmidhuber's interestingness, as a toy)
    golden        Fibonacci ratios, and how often random lengths contain a golden ratio
    sunflower     Vogel's model of a sunflower head at the golden angle and near it
    critics       Hume's true judges, as an analogy
    taste         the Price List for the paradox of taste
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import aesthetics as A
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy40")
load = CACHE.load

TASTE = [
    ("DG", r"there is no disputing about taste: \ no taste is better than another"),
    ("BETTER", r"some works of art are better than others"),
    ("FEEL", r"judgments of beauty rest on feeling, \ not on concepts or proof"),
]


def compute_taste():
    claims = {k: prop.Var(k) for k, _ in TASTE}
    bg = [prop.Imp(prop.And(prop.Var("FEEL"), prop.Var("DG")), prop.Not(prop.Var("BETTER")))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t in TASTE], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


def compute_patterns():
    return {g: A.pattern(g, cells=2) for g in A.ORBIFOLD}


ITEMS = {"tuning": A.tuning, "temper": A.temperaments, "elements": lambda: A.elements("p4m"),
         "sunflower": A.phyllotaxis, "curve": A.dissonance_curve, "stretched": lambda: A.dissonance_curve(stretch=2.1),
         "wallpaper": A.wallpaper, "patterns": compute_patterns, "compress": A.compressibility,
         "progress": A.compression_progress, "golden": A.golden, "critics": A.critics, "taste": compute_taste}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
