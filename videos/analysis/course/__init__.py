"""Analysis, Built as a course: the table its course site is built from (``tools/series_site.py``).

For every part: the level it starts at, its prerequisites, its story (the question it opens with, the arc, what
it hands on), what a student can do afterwards at each of four levels, its key results, which chapters belong to
which track, and its interactive.  The chapters themselves stay in each part's ``manifest.py``, the notes and
problems in its ``README.md``; this table adds only what neither says.  See :mod:`videos.coursekit`.

Every other module in this folder holds ``PARTS = [Part(...), ...]`` for some of the parts; the interactives are
in ``site/widgets/``; the labs in ``videos/analysis/labs/``.
"""

from videos.coursekit import Course

COURSE = Course(
    series="analysis",
    tracks={
        "U": ("Undergraduate", "A first course in real analysis: the definitions, the pictures, the standard theorems with their proofs."),
        "M": ("Graduate", "The full lecture, at the level of Rudin's three books: every proof and every counterexample."),
        "D": ("Qualifying exam", "The hardest theorems, the sharp counterexamples and the problems of a PhD qualifying exam in analysis."),
        "I": ("Applications", "Where the theorem is used: numerical analysis, signal processing, probability, physics, machine learning."),
    },
    track_intro={
        "U": "For a student with calculus and some experience of proof. Watch the chapters marked Undergraduate, run the lab, and work the lab's three extensions.",
        "M": "The whole course: every chapter, at the level of Principles of Mathematical Analysis, Real and Complex Analysis and Functional Analysis.",
        "D": "On top of the graduate track: the chapters with the deepest theorems and the sharpest counterexamples, the ones a qualifying exam asks for.",
        "I": "For users of analysis: the undergraduate core of each part, then the chapters whose theorems carry numerical methods, Fourier analysis, probability and quantum mechanics, and the labs, which compute them.",
    },
    lab_needs="numpy, scipy, matplotlib",
    library=(),
)
