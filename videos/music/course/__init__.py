"""Music, Built as a course: the table its course site is built from (``tools/series_site.py``).

For every part: the level it starts at, its prerequisites, its story (the question it opens with, the arc, what
it hands on), what a student can do afterwards at each of four levels, its key results, which chapters belong to
which track, and its interactive.  The chapters themselves stay in each part's ``manifest.py``, the notes and
problems in its ``README.md``; this table adds only what neither says.  See :mod:`videos.coursekit`.

Every other module in this folder holds ``PARTS = [Part(...), ...]`` for some of the parts; the interactives are
in ``site/widgets/`` (they make sound, in the browser); the labs in ``videos/music/labs/``.
"""

from videos.coursekit import Course

COURSE = Course(
    series="music",
    tracks={
        "U": ("Foundations", "A first degree in music or music technology: what to hear, what to name, what to compute."),
        "M": ("Full course", "The whole lecture: every derivation, experiment and listening example."),
        "D": ("Research", "Each part's Frontier chapter: the limit computed, the open problems stated."),
        "I": ("Practice", "How the idea is used: by instrument makers and players, in the studio, on the stage, in software."),
    },
    track_intro={
        "U": "For someone who can sing a tune back and knows school mathematics. In each part watch the chapters marked Foundations, do the listening questions, and run the lab.",
        "M": "The whole course: every numbered chapter, every lab with its three extensions, and the problem set.",
        "D": "On top of the full course: each part's Frontier chapter and its research problem, and Part 67 on how music research is done.",
        "I": "For players, makers, engineers and programmers: the foundations of each part, then the chapters on how it is used and where it fails, and the labs, which run the series' own instrument.",
    },
    lab_needs="numpy, scipy, matplotlib",
    library=("Monochord", "explainer/music/monochord",
             "the instrument the series builds: one simulated string in Part 1, then instruments, a studio, and "
             "machines that listen"),
)
