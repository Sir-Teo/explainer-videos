"""The watch kit of *Statistics, Built* (explainer/stats/watch.py, videos/stats/SYLLABUS.md 1.2): the entrances it
gives plain fades, its cards, and the degree strip under the title."""

import os

import pytest

manim = pytest.importorskip("manim")

from explainer.stats import PARTS, STAGES, MILESTONES  # noqa: E402
from explainer.stats import watch  # noqa: E402


def test_lively_gives_each_fade_the_entrance_its_content_suggests(monkeypatch):
    monkeypatch.delenv("EXPLAINER_PLAIN_FADES", raising=False)
    M = manim
    assert isinstance(watch.lively(M.FadeIn(M.Arrow(M.LEFT, M.RIGHT))), M.GrowArrow)
    assert isinstance(watch.lively(M.FadeIn(M.Line(M.LEFT, M.RIGHT))), M.Create)
    assert isinstance(watch.lively(M.FadeIn(M.MathTex(r"\hat\beta = (X^\top X)^{-1}X^\top y"))), M.Write)
    assert isinstance(watch.lively(M.FadeIn(M.VGroup(M.Square(), M.Circle()))), M.LaggedStart)
    dot = M.FadeIn(M.Dot())
    assert watch.lively(dot) is dot  # a dot keeps its fade
    shifted = M.FadeOut(M.Square())
    assert watch.lively(shifted) is shifted  # exits are left alone
    monkeypatch.setenv("EXPLAINER_PLAIN_FADES", "1")
    arrow = M.FadeIn(M.Arrow(M.LEFT, M.RIGHT))
    assert watch.lively(arrow) is arrow


def test_predict_card_fits_the_frame():
    card = watch.predict_card(r"What fraction of 95\% intervals from repeated samples contain $\theta$?",
                              [r"exactly 95\%", r"about 95\%, if the model holds", r"it depends on $\theta$",
                               r"none of them, once computed"])
    assert len(card.options) == 4
    assert card.width <= 12.6 + 1e-6 and card.height <= 7.2 + 1e-6


@pytest.mark.parametrize("part", [1, 12, 20, 42, 43, 55, 65])
def test_degree_strip(part):
    strip = watch.degree_strip(part)
    assert len(strip.groups) == len(STAGES) == 5
    assert sum(len(g) for g in strip.groups) == len(PARTS) == 65
    name = next(n for n, (a, b) in STAGES if a <= part <= b)
    assert strip.current in strip.groups[[n for n, _ in STAGES].index(name)]
    assert strip.width <= 12.4 + 1e-6
    assert set(MILESTONES) == {20, 42, 55, 65}
