"""Computer Science, Built as a course: the table its course site is built from (``tools/series_site.py``).

For every part: the level it starts at, its prerequisites, its story (the question it opens with, the arc, what
it hands on), what a student can do afterwards at each of four levels, its key results, which chapters belong to
which track, and its interactive.  The chapters themselves stay in each part's ``manifest.py``, the notes and
problems in its ``README.md``; this table adds only what neither says.  See :mod:`videos.coursekit`.

Every other module in this folder holds ``PARTS = [Part(...), ...]`` for some of the parts; the interactives are
in ``site/widgets/``; the labs in ``videos/cs/labs/``.
"""

from videos.coursekit import Course

COURSE = Course(
    series="cs",
    tracks={
        "U": ("Degree", "The undergraduate computer-science degree: the ideas, the machine, the algorithms, the proofs."),
        "M": ("Graduate", "The full lecture: every derivation, model and measurement, at first-year graduate depth."),
        "D": ("Research", "Each part's Frontier chapter and research tier: limits computed, open problems stated."),
        "I": ("Industry", "Where the idea lives in production: the systems, the trade-offs, the incidents, the interview questions."),
    },
    track_intro={
        "U": "For a student who can program and knows school mathematics. In each part watch the chapters marked Degree, run the lab, and do the first problems of the set.",
        "M": "The whole course: every numbered chapter, every lab with its three extensions, and the problem set.",
        "D": "On top of the graduate track: each part's Frontier chapter, the research-tier parts of Act XI, and the research problems.",
        "I": "For engineers and interview preparation: the degree core of each part, then how industry uses it and what it costs when it fails, and the labs, which run the series' own machine and tools.",
    },
    lab_needs="numpy, scipy, matplotlib",
    library=('Pebble and its tools', 'explainer/cs', 'the computer the series builds from NAND gates, with its assembler, emulators, compilers, algorithms and systems models'),
)
