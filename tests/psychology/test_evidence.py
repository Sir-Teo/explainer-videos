"""The false-positive lab (``explainer/psychology/evidence.py``): each tool gives the number theory says it should."""

from __future__ import annotations

import math

import numpy as np
import pytest

from explainer.psychology import evidence as E


def test_effect_sizes():
    rng = np.random.default_rng(1)
    a, b = 0.5 + rng.standard_normal(200_000), rng.standard_normal(200_000)
    assert E.cohen_d(a, b) == pytest.approx(0.5, abs=0.01)
    assert E.overlap(0) == 1 and E.overlap(0.8) == pytest.approx(0.689, abs=0.001)
    assert E.superiority(0.5) == pytest.approx(np.mean(a[:50_000] > b[:50_000]), abs=0.01)
    assert E.r_to_d(E.d_to_r(0.4)) == pytest.approx(0.4)
    assert E.p_for(0.02, 100_000) < 1e-4 < E.p_for(0.5, 10)  # tiny and "significant"; large and not


def test_power_and_sample_size():
    assert E.power(0, 50) == pytest.approx(0.05, abs=1e-6)
    assert E.power(0.5, E.n_for(0.5)) >= 0.8 > E.power(0.5, E.n_for(0.5) - 2)
    assert E.n_for(0.5) == 63 and E.n_for(0.2) == 393
    lit = E.literature(20_000, 0.5, 20, np.random.default_rng(2))
    assert lit["significant"].mean() == pytest.approx(E.power(0.5, 20), abs=0.012)


def test_peeking_inflates_false_positives():
    once = E.peeking(1, batch=100, reps=4000, rng=np.random.default_rng(3))
    many = E.peeking(10, batch=10, reps=4000, rng=np.random.default_rng(3))
    assert once["rate"] == pytest.approx(0.05, abs=0.012)
    assert 0.15 < many["rate"] < 0.25 and len(many["example"]) == 10


def test_forking_paths():
    f = E.forks(7)
    assert len(f["table"]) == 16 and f["best_p"] <= f["planned"][0]
    assert E.forks(7)["table"] == f["table"]  # seeded
    out = E.any_significant(range(600))
    assert out["planned"] == pytest.approx(0.05, abs=0.025)
    assert out["any"] > 2.5 * out["planned"] and all(s >= out["planned"] for s in out["single"])
    assert 0.13 < out["any"] < 0.24


def test_published_literature_overstates_and_null_pcurve_is_flat():
    rng = np.random.default_rng(4)
    null = E.literature(40_000, 0.0, 20, rng)
    assert null["published"].mean() == pytest.approx(0.025, abs=0.004)  # significant, and in the hoped-for direction
    assert null["est"][null["published"]].mean() > 0.6  # a literature of pure noise reports a large effect
    assert np.allclose(E.pcurve(null["p"][null["published"]]), 0.2, atol=0.03)
    real = E.literature(40_000, 0.5, 30, rng)
    curve = E.pcurve(real["p"][real["published"]])
    assert curve[0] > 0.4 and (np.diff(curve) < 0).all()
    assert real["est"][real["published"]].mean() > 0.5 > real["est"].mean() - 0.01
    pushed = E.literature(40_000, 0.0, 20, rng, hack=0.3)
    assert E.pcurve(pushed["p"][pushed["published"]])[-1] > 0.5


def test_replication_of_a_filtered_literature():
    rng = np.random.default_rng(5)
    null = E.replicate(E.literature(20_000, 0.0, 20, rng), rng)
    assert null["rate"] == pytest.approx(0.025, abs=0.012) and abs(null["ratio"]) < 0.1
    real = E.replicate(E.literature(20_000, 0.5, 100, rng), rng)
    assert real["rate"] > 0.85 and 0.85 < real["ratio"] < 1.0
    assert E.ppv(0.1, 0.35) == pytest.approx(0.4375)


def test_claiming_an_absence():
    se = 2 / math.sqrt(3289)
    assert E.tost(0.04, se, 0.2)["p"] < 0.001 < E.tost(0.04, se, 0.05)["p"]
    assert E.bf01(0.04, se) > 5 and E.bf01(0.5, se) < 1e-6
    assert E.bf01(0.0, 0.5, 0.5) == pytest.approx(math.sqrt(2))
