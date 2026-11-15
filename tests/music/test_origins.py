"""Monochord's origins module (Part 47): nPVI, alignment, trees, Rayleigh's test and iterated learning.

    python -m pytest -q tests/music/test_origins.py
"""

import math

import numpy as np
import pytest

from explainer.music.monochord import origins as O
from explainer.music.monochord.melody import THE_TUNE, corpus


def test_npvi():
    assert O.npvi([1, 1, 1, 1]) == 0.0
    assert O.npvi([1.5, 0.5, 1.5, 0.5]) == pytest.approx(100.0)
    assert O.npvi([2, 4, 6, 8]) == pytest.approx(O.npvi([1, 2, 3, 4]))          # scale-free


def test_align_against_brute_force():
    rng = np.random.default_rng(3)
    a = [[float(rng.integers(0, 8)), 1.0] for _ in range(5)]
    b = [x[:] for x in a]
    assert O.align(a, b)["cost"] == pytest.approx(0.0)
    b2 = [[x[0] + 5, x[1]] for x in a]                                      # transposed: free
    assert O.align(a, b2)["cost"] == pytest.approx(0.0)
    c = a[:2] + a[3:]                                                       # one note deleted: one gap
    assert O.align(a, c)["cost"] == pytest.approx(1.0)
    r = O.align(a, c)
    assert sum(1 for i, j in r["pairs"] if j is None) == 1


def test_upgma_and_robinson_foulds():
    D = np.array([[0, 1, 4, 4], [1, 0, 4, 4], [4, 4, 0, 2], [4, 4, 2, 0]], float)
    u = O.upgma(D, list("ABCD"))
    t = (("A", "B"), ("C", "D"))
    assert O.robinson_foulds(u["tree"], t) == 0
    assert O.robinson_foulds((("A", "C"), ("B", "D")), t) == 4


def test_rayleigh():
    r = O.rayleigh([0.0] * 20)
    assert r["R"] == pytest.approx(1.0) and r["p"] < 1e-6
    th = np.linspace(0, 2 * math.pi, 40, endpoint=False)
    assert O.rayleigh(th)["R"] == pytest.approx(0.0, abs=1e-9)


def test_sampling_chains_find_the_prior():
    pr = O.RhythmPrior({(1, 1, 2): 3.0, (1, 1, 1): 1.0})
    ch = O.rhythm_chains(pr, 200, 6, seed=1)
    assert pr.mass_near(ch[:, -1]) > pr.mass_near(ch[:, 0]) + 0.25


def test_the_tune_survives_and_noise_simplifies():
    t = [m for m in corpus() if m.name == THE_TUNE][0]
    mel = [[float(p), float(b)] for p, b in zip(t.pitches, t.beats)]
    rng = np.random.default_rng(0)
    out = O.transmit(mel, rng, {"pitch_noise": 0, "motor": 0, "dur_noise": 0, "dur_motor": 0, "slip": 0, "novel": 0, "pull": 0})
    assert np.allclose(out, mel)
    r = O.random_melody(np.random.default_rng(1))
    ch = O.transmission_chain(r, 30, np.random.default_rng(2))
    assert O.structure(ch[-1])["levels"] < O.structure(ch[0])["levels"]


def test_universals_and_pipes():
    u = O.universals([m for m in corpus() if m.name == THE_TUNE][0])
    assert all(u.values())
    assert O.pipe_hz(0.34, 0.008) < O.pipe_hz(0.218, 0.008)


def test_publication_bias():
    r = O.publication_bias(300, 0.0, seed=0)
    assert r["mean_published"] > r["mean_all"] + 0.05
