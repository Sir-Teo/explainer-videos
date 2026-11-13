"""Philosophy, Built as a course: the table its course site is built from (``tools/series_site.py``).

For every part: the level it starts at, its prerequisites, its story (the question it opens with, the arc, what
it hands on), what a student can do afterwards at each of four levels, its key results, which chapters belong to
which track, and its interactive.  The chapters themselves stay in each part's ``manifest.py``, the notes and
problems in its ``README.md``; this table adds only what neither says.  See :mod:`videos.coursekit`.

Every other module in this folder holds ``PARTS = [Part(...), ...]`` for some of the parts; the interactives are
in ``site/widgets/``; the labs in ``videos/philosophy/labs/``.
"""

from videos.coursekit import Course

COURSE = Course(
    series="philosophy",
    tracks={
        "U": ("Introductory", "A first course in philosophy: the questions, the classic arguments, and the toy that makes each precise."),
        "M": ("Advanced", "The full lecture at the level of an advanced undergraduate or master's seminar: the formal results and the debates."),
        "D": ("Research", "The theorems in full, the current literature, and the open problems, at qualifying-exam level."),
        "I": ("Applied", "Where the philosophy is now engineering or policy: verification, statistics, AI, law, medicine, institutions."),
    },
    track_intro={
        "U": "No prerequisites beyond curiosity and school mathematics. In each part watch the chapters marked Introductory, run the lab, and try the first problems.",
        "M": "The whole course: every numbered chapter, every lab with its three extensions, and the problems.",
        "D": "On top of the advanced track: the chapters that prove the impossibility theorems in full or reach the current literature.",
        "I": "For readers who want the uses: the introductory core of each part, then the chapters where the idea is built into software, science, law or institutions, and the labs, which call the Reasoner.",
    },
    lab_needs="numpy, scipy, matplotlib",
    library=('the Reasoner', 'explainer/philosophy/reasoner', "the series' tested reasoning library: SAT, first-order tableaux, modal and epistemic model checking, credences, causal models, decision, games, voting and more"),
)
