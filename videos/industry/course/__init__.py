"""Industry, Built as a course: the table its course site is built from (``tools/series_site.py``).

For every part: the level it starts at, its prerequisites, its story, what a viewer can do afterwards at each of four
levels, its key results, which chapters belong to which track, and its interactive.  The chapters stay in each part's
``manifest.py``, the notes and problems in its ``README.md``.  See :mod:`videos.coursekit`.

Every other module in this folder holds ``PARTS = [Part(...), ...]`` for some of the parts; the interactives are in
``site/widgets/``; the labs are in ``videos/industry/labs/``.
"""

from videos.coursekit import Course

COURSE = Course(
    series="industry",
    tracks={
        "U": ("Curious", "How each industry works, for anyone: the product, the money, the companies, the landscape."),
        "M": ("Student", "The accounts, the arithmetic and the models behind each industry, for students of business "
                         "and economics."),
        "D": ("Research", "What is not known: the estimates that disagree, the open questions, and the forecasts the "
                          "series has made and will score."),
        "I": ("Practice", "Reading filings, sizing markets and drawing landscapes, for analysts, investors, "
                          "consultants and people entering an industry."),
    },
    track_intro={
        "U": "For anyone. No mathematics beyond percentages. Watch the chapters marked for this track and try the "
             "interactive on each part's page.",
        "M": "For a student of business or economics. On top of the first track: the chapters that build the "
             "arithmetic (value added, margins, unit costs), every lab and its three extensions.",
        "D": "For researchers and analysts who want the uncertainty: the ranges behind each estimate, where sources "
             "disagree, and the series' own dated forecasts.",
        "I": "For people who analyse industries at work: how each figure is read from a filing or a tracker, how a "
             "landscape is drawn and dated, and where the numbers mislead.",
    },
    lab_needs="numpy, scipy, matplotlib",
    library=("The Works and the Register", "explainer/industry",
             "the model companies' arithmetic (explainer/industry/works, numpy only) and the Register of every figure "
             "the films show, each with its source and dates"),
)
