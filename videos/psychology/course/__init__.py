"""Psychology, Built as a course: the table its course site is built from (``tools/series_site.py``).

For every part: the level it starts at, its prerequisites, its story (the question it opens with, the arc, what
it hands on), what a student can do afterwards at each of four levels, its key results, which chapters belong to
which track, and its interactive.  The chapters themselves stay in each part's ``manifest.py``, the notes and
problems in its ``README.md``; this table adds only what neither says.  See :mod:`videos.coursekit`.

Every other module in this folder holds ``PARTS = [Part(...), ...]`` for some of the parts; the interactives are
in ``site/widgets/`` (for this series each one is an experiment the reader takes part in); the labs are in
``videos/psychology/labs/``.
"""

from videos.coursekit import Course

COURSE = Course(
    series="psychology",
    tracks={
        "U": ("Psych 101 and the major", "The phenomena, the classic experiments and the demonstrations on you: an "
                                         "introductory course, then the major."),
        "M": ("Graduate", "The models, derived and fitted: mathematical and quantitative psychology."),
        "D": ("Research", "What is open: each part's frontier chapter, and the research-level acts."),
        "I": ("Practice", "Where the idea is a job: design, assessment, policy, the clinic, and how to audit a claim."),
    },
    track_intro={
        "U": "For anyone. No mathematics beyond school algebra is assumed at the start. Watch the chapters marked "
             "for this track, take the experiment on each part's page, and do the first problems. Together these "
             "chapters are an introductory course and then the core of a psychology degree.",
        "M": "For a psychology graduate, or anyone with calculus, linear algebra and probability. On top of the "
             "first track: the chapters that derive a model, test it against data and fit it, every lab with its "
             "three extensions, and the graduate toolkit of Act XI.",
        "D": "For a PhD student. On top of the graduate track: each part's frontier chapter, with what is not "
             "known and the research problem, and Act XIII.",
        "I": "For people who use psychology at work: UX and human-factors engineers, behavioural scientists, "
             "psychometricians, people in education, policy and care. The first track's core of each part, then "
             "the practice chapters and the labs, which call the series' own library.",
    },
    lab_needs="numpy, scipy, matplotlib",
    library=("Psyche, the Pool and the Archive", "explainer/psychology",
             "the series' model subject (explainer/psychology/psyche, numpy and scipy only), with the simulated "
             "participant pool, the Battery's task format, the Replication Ledger and the Archive's historical "
             "data beside it"),
)
