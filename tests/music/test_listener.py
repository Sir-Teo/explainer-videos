"""Monochord's listener (Part 46): PPM, surprise and uncertainty, the combined listener, syncopation and statistical
learning.

    python -m pytest -q tests/music/test_listener.py
"""

import math

import numpy as np
import pytest

from explainer.music.monochord import listener as L


def test_ppm_distribution_is_a_distribution_and_learns():
    m = L.PPM(2).fit([[0, 2, 4, 0, 2, 4, 0, 2, 4]])
    d = m.distribution([0, 2])
    assert abs(sum(d.values()) - 1) < 1e-9 and min(d.values()) > 0
    assert max(d, key=d.get) == 4 and d[4] > 0.5
    u = L.PPM(2).distribution([])                                         # nothing learned: uniform
    assert max(u.values()) == pytest.approx(1 / len(L.ALPHABET))


def test_entropy_bounds():
    n = 8
    assert L.entropy({i: 1 / n for i in range(n)}) == pytest.approx(math.log2(n))
    assert L.entropy({0: 1.0}) == 0.0


def test_listener_surprise_falls_with_repetition():
    corpus = [[0, 2, 4, 5, 7, 5, 4, 2, 0]] * 3
    lis = L.Listener(corpus, 3)
    r = lis.listen([0, 2, 4, 5, 7, 5, 4, 2, 0])
    assert r["mean_ic"] < 1.5
    odd = lis.listen([0, 2, 4, 5, 11, 5, 4, 2, 0])
    assert odd["ic"][4] > r["ic"][4] + 3                                  # an unexpected note costs bits
    rep = lis.listen([0, 6, 0, 6, 0, 6, 0, 6])
    assert rep["ic"][-1] < rep["ic"][1]                                   # the short-term model learns the piece


def test_syncopation_index():
    assert L.syncopation([0, 4, 8, 12]) == 0
    assert L.syncopation([0, 3, 6, 10, 12, 14]) > L.syncopation([0, 4, 7, 10, 12]) > 0
    assert L.syncopation([]) == 0


def test_saffran_transitional_probabilities():
    words = [(60, 66, 64), (69, 62, 71), (65, 61, 68), (63, 70, 67)]
    s = L.saffran(words, 60, np.random.default_rng(0))
    assert s["tp_inside"] == pytest.approx(1.0) and 0.2 < s["tp_across"] < 0.5
    assert len(s["sequence"]) == 180
