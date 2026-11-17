"""Psyche's development module (Part 30)."""
from __future__ import annotations

import numpy as np
import pytest
from scipy.stats import norm

from explainer.psychology.psyche import develop as D


def test_habituation_falls_and_recovers_for_novelty():
    h = D.habituation(noise=0.0)
    looks = np.asarray(h["looks"])
    assert np.all(np.diff(looks) < 0)
    assert h["criterion"] is not None
    assert h["novel"] > h["familiar"]
    assert D.habituation(noise=0.0, novelty=0.0)["novel"] == pytest.approx(h["familiar"])


def test_surprisal_is_the_dirichlet_predictive():
    s = D.surprisal_trace([0, 0, 1], k=3, alpha=1.0)
    assert s[0] == pytest.approx(np.log2(3))
    assert s[1] == pytest.approx(-np.log2(2 / 4))
    assert s[2] == pytest.approx(-np.log2(1 / 5))


def test_goldilocks_rate_is_u_shaped():
    g = D.goldilocks(n_seq=200)
    r, s = np.asarray(g["rate"]), np.asarray(g["surprisal"])
    ok = np.isfinite(r)
    i = int(np.nanargmin(r))
    assert abs(s[i] - g["best"]) < 0.5
    assert r[ok][0] > r[i] and r[ok][-1] > r[i]


def test_ans_matches_its_formula_and_depends_on_ratio():
    w = 0.3
    assert float(D.ans_correct(12, 8, w)) == pytest.approx(norm.cdf(4 / (w * np.hypot(12, 8))))
    assert float(D.ans_correct(16, 8, w)) == pytest.approx(float(D.ans_correct(32, 16, w)))
    assert D.ratio_threshold(D.WEBER["6 months"]) == pytest.approx(2.0, abs=0.05)
    assert D.ratio_threshold(D.WEBER["9 months"]) == pytest.approx(1.5, abs=0.05)
    ts = [D.ratio_threshold(w_) for w_ in D.WEBER.values()]
    assert all(a > b for a, b in zip(ts, ts[1:]))


def test_sample_surprise():
    a, b = D.sample_surprise(0.1, 4, 5), D.sample_surprise(0.1, 1, 5)
    assert b["p"] / a["p"] == pytest.approx(9.0 ** 3)
    assert a["bits"] == pytest.approx(-np.log2(a["p"]))


def test_field_makes_and_outgrows_the_error():
    assert D.a_not_b(-6.0, 0.0, n=60)["error"] < 0.1
    assert D.a_not_b(-6.0, 3.0, n=60)["error"] > 0.7
    assert D.a_not_b(-3.0, 3.0, n=60)["error"] < 0.05
    many = D.a_not_b(-6.0, 3.0, n_a=8, n=60, seed=1)["error"]
    one = D.a_not_b(-6.0, 3.0, n_a=1, n=60, seed=1)["error"]
    assert many > one


def test_meta_regression_recovers_a_slope():
    rng = np.random.default_rng(0)
    x = rng.uniform(0, 10, 400)
    v = np.full(400, 0.02)
    y = 0.2 + 0.05 * x + rng.normal(0, np.sqrt(v + 0.01))
    m = D.meta_regression(y, v, np.column_stack([np.ones_like(x), x]))
    assert m["b"][1] == pytest.approx(0.05, abs=0.01)
    assert m["tau2"] == pytest.approx(0.01, abs=0.006)
    # with no heterogeneity and one column, it is the fixed-effect mean
    m0 = D.meta_regression([0.1, 0.3], [0.01, 0.01], np.ones((2, 1)))
    assert m0["b"][0] == pytest.approx(0.2)
