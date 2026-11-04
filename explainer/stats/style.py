"""The colours of *Statistics, Built*: one meaning per colour, for the whole series (videos/stats/SYLLABUS.md, §1).

    from explainer.stats import S
    dot.set_color(S.TRUTH)     # the true parameter: gold, in every part

A symbol keeps its colour in every equation and in the picture it describes: theta is always gold, theta-hat always
blue, the null distribution always grey.  Parts add their own names for local objects in their ``common.py``, built
from these where the meaning is the same.
"""

from __future__ import annotations

from types import SimpleNamespace

from manim import GREY_A, GREY_B, GREY_C, GREY_D, WHITE

S = SimpleNamespace(
    # the two sides of every statistical problem
    TRUTH="#F2C14E",  # theta, mu, the population, the true curve: gold
    EST="#5DADEC",  # theta-hat, x-bar, a fitted curve, a sample's summary: blue
    DATA=WHITE,  # observations, the sample
    POP=GREY_C,  # the population behind the sample (unseen in real life; visible in the World)
    # testing
    NULL=GREY_B,  # H0 and its distribution
    ALT="#4FD1C5",  # H1 and its distribution
    # Bayes
    PRIOR="#B48EF0",
    LIK="#7BD88F",
    POST="#FF9F5A",
    # models
    RESID="#F26D6D",  # residuals, errors, misfit
    FIT="#5DADEC",  # = EST: a fitted model is an estimate
    # causation
    TREAT="#FF7F6E",  # treated units
    CTRL="#7EC8F5",  # controls
    # the Coverage Board's verdicts
    KEPT="#5BD18B",  # the promise is kept
    BROKEN="#F25F5C",  # the promise is broken
    CONS="#6F8FF2",  # conservative: kept with room to spare
    # bookkeeping
    MISSING=GREY_D,  # hollow markers for what was not observed
    ACCENT="#F7D154",  # the series' accent: chapter cards, the lit timeline, the Transcript
    WORLD="#8FD3A6",  # the World: tags and the map
    MUSEUM="#E3B98A",  # the Museum: historical data, with its source
    GRID=GREY_D,
    TEXT_DIM=GREY_A,
)
