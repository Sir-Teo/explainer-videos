"""The exact probability engine of *Statistics, Built* Part 2 (explainer/stats/prob.py) against known answers."""

import math
from fractions import Fraction as F

import numpy as np

from explainer.stats.prob import Dist, coin, convolve, die, faces, shuffles


def test_galileo_three_dice():
    s = (die() ** 3).map(sum)
    assert s.P(9) == F(25, 216) and s.P(10) == F(27, 216)
    assert sum(p for _, p in s.items()) == 1


def test_de_mere():
    assert (die() ** 4).P(lambda r: 6 in r) == 1 - F(5, 6) ** 4 == F(671, 1296)
    dd = (die() * die()).map(lambda r: int(r == (6, 6)))
    assert 1 - dd.iid_sum(24).P(0) == 1 - F(35, 36) ** 24


def test_conditioning_and_bayes():
    two = die() * die()
    g = two.given(lambda r: sum(r) == 8)
    assert len(g) == 5 and g.P(lambda r: 6 in r) == F(2, 5)
    kids = Dist.uniform(["BB", "BG", "GB", "GG"])
    assert kids.given(lambda w: "B" in w).P("BB") == F(1, 3)
    tree = Dist({"sick": F(1, 100), "well": F(99, 100)}).then(
        lambda s: coin(F(9, 10) if s == "sick" else F(1, 20), heads="+", tails="-"))
    assert tree.given(lambda w: w[1] == "+").P(lambda w: w[0] == "sick") == F(90, 90 + 495)


def test_derangements_and_fixed_points():
    for n in range(1, 8):
        d = shuffles(n).map(lambda s: sum(s[i] == i for i in range(len(s))))
        assert d.P(0) == sum(F((-1) ** k, math.factorial(k)) for k in range(n + 1))
        assert d.E() == 1
        if n >= 2:
            assert d.var() == 1


def test_moments_and_sums():
    assert die().E() == F(7, 2) and die().var() == F(35, 12)
    assert die().iid_sum(10).var() == 10 * F(35, 12)
    assert (die() + die()).p == (die() * die()).map(sum).p


def test_sicherman_and_pgf():
    a, b = faces([1, 2, 2, 3, 3, 4]), faces([1, 3, 4, 5, 6, 8])
    assert (a + b).p == (die() + die()).p
    assert convolve(die().pgf(), die().pgf()) == (die() + die()).pgf()


def test_sampling_matches():
    rng = np.random.Generator(np.random.PCG64(0))
    draws = die().sample(60_000, rng)
    assert abs(np.mean(np.array(draws) == 6) - 1 / 6) < 0.01
