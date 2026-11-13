"""AI, Built as a course: the table its course site is built from (``tools/series_site.py``).

For every part: the level it starts at, its prerequisites, its story (the question it opens with, the arc, what
it hands on), what a student can do afterwards at each of four levels, its key results, which chapters belong to
which track, and its interactive.  The chapters themselves stay in each part's ``manifest.py``, the notes and
problems in its ``README.md``; this table adds only what neither says.  See :mod:`videos.coursekit`.

Every other module in this folder holds ``PARTS = [Part(...), ...]`` for some of the parts; the interactives are
in ``site/widgets/``; the labs in ``videos/ai/labs/``.
"""

from videos.coursekit import Course

COURSE = Course(
    series="ai",
    tracks={
        "U": ("Undergraduate", "A first course in how modern AI works: the ideas, the pictures, the arithmetic, the history."),
        "M": ("Master's", "The derivations and the models of a graduate machine-learning degree, each trained or probed on screen."),
        "D": ("Research", "Each part's theory in the literature's generality, its frontier, and what is still open."),
        "I": ("Engineering", "How labs and products use the idea: the systems, the published configurations, the failure cases."),
    },
    track_intro={
        "U": "For a student with calculus, a little linear algebra and some programming. In each part watch the chapters marked Undergraduate, run the lab, and do the first problems of the set.",
        "M": "The whole course at the level of a master's in machine learning: every numbered chapter, every lab with its three extensions, and the problem set.",
        "D": "On top of the master's track: the chapters that prove the part's results in generality or reach its frontier, and the hardest problems of each set.",
        "I": "For engineers: the undergraduate core of each part, then how it is built and served in practice, and the labs, which are the series' models in miniature.",
    },
    lab_needs="numpy, scipy, matplotlib",
    library=("the series' autodiff", 'explainer/ai/autodiff.py', 'a reverse-mode autodiff library in numpy, built in Part 4 and used by the models the series trains'),
)
