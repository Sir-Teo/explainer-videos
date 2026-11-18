"""Economics, Built as a course: the table its course site is built from (``tools/series_site.py``).

For every part: the level it starts at, its prerequisites, its story (the question it opens with, the arc, what it
hands on), what a student can do afterwards at each of four levels, its key results, which chapters belong to which
track, and its interactive.  The chapters themselves stay in each part's ``manifest.py``, the notes and problems in
its ``README.md``; this table adds only what neither says.  See :mod:`videos.coursekit`.

Every other module in this folder holds ``PARTS = [Part(...), ...]`` for some of the parts; the interactives are in
``site/widgets/`` (for this series each one is a game the reader plays, on the kit in ``00_games.js``); the labs are
in ``videos/economics/labs/``.
"""

from videos.coursekit import Course

COURSE = Course(
    series="economics",
    tracks={
        "U": ("Principles and the major", "The puzzle, the game, the picture: a principles course, then intermediate "
                                          "micro, macro and the fields."),
        "M": ("Graduate", "The models derived, solved and estimated: the first-year PhD core."),
        "D": ("Research", "What is open: each part's frontier chapter, and the research-level act."),
        "I": ("Practice", "Where the idea is a job: central banks, treasuries, competition cases, pricing, platforms, "
                          "evaluation."),
    },
    track_intro={
        "U": "For anyone. School algebra at the start, calculus from Part 5. Watch the chapters marked for this "
             "track, play the game on each part's page, and do the first problems. Together these chapters are a "
             "principles course and then the core of an economics degree.",
        "M": "For an economics graduate, or anyone with multivariable calculus, linear algebra and probability. On "
             "top of the first track: the chapters that derive, solve and estimate a model, every lab with its three "
             "extensions, and the graduate core of Act X.",
        "D": "For a PhD student. On top of the graduate track: each part's frontier chapter, with what is not known "
             "and the research problem, and Act XII.",
        "I": "For people who use economics at work: central-bank and treasury staff, competition economists, pricing "
             "and platform teams, evaluators and analysts. The first track's core of each part, then the practice "
             "chapters and the labs, which call the series' own library.",
    },
    lab_needs="numpy, scipy, matplotlib",
    library=("Agora and the Data Room", "explainer/economics",
             "the economy the series builds (explainer/economics/agora, numpy and scipy only), with the Island's "
             "planted truths, the Facts, the Dials and the Data Room's frozen, cited data beside it"),
)
