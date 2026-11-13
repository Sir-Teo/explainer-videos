"""Statistics, Built as a course: the table its course site is built from (``tools/series_site.py``).

For every part: the level it starts at, its prerequisites, its story (the question it opens with, the arc, what
it hands on), what a student can do afterwards at each of four levels, its key results, which chapters belong to
which track, and its interactive.  The chapters themselves stay in each part's ``manifest.py``, the notes and
problems in its ``README.md``; this table adds only what neither says.  See :mod:`videos.coursekit`.

Every other module in this folder holds ``PARTS = [Part(...), ...]`` for some of the parts; the interactives are
in ``site/widgets/``; the labs in ``videos/stats/labs/``.
"""

from videos.coursekit import Course

COURSE = Course(
    series="stats",
    tracks={
        "U": ("Bachelor's", "A first degree in statistics: the ideas, the pictures, and analysis of real data."),
        "M": ("Master's", "The modern toolkit, with its derivations, computation and conditions stated precisely."),
        "D": ("PhD", "The theory that justifies the methods, measure-theoretic and exact, and the research frontier."),
        "I": ("Practice", "What an applied statistician does with it: design, diagnostics, reporting, and the cases where it went wrong."),
    },
    track_intro={
        "U": "For a student with calculus and a first look at matrices. Stages I and II are written at this level throughout; later parts open with chapters a bachelor's student can follow. Watch the chapters marked Bachelor's, run the lab, and do the first problems.",
        "M": "The whole of Stages I to III at master's level, and the accessible chapters of the PhD stages: every lab with its three extensions and the problem sets.",
        "D": "On top of the master's track: the measure-theoretic chapters, the proofs with their exact conditions and counterexamples, the frontier chapters, and the qualifying-exam problems.",
        "I": "For working analysts: the bachelor's core of each part, then the chapters on practice (design, diagnostics, what to report, the historical failures), and the labs, which call the series' own library.",
    },
    lab_needs="numpy, scipy, matplotlib",
    library=('statkit and the World', 'explainer/stats/kit', "the series' statistics library (numpy and scipy only), with the simulated World, the exact probability engine and the Museum's datasets beside it in explainer/stats"),
)
