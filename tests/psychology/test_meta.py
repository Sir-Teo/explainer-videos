"""Psyche's meta-science (Part 50): pooling, filters, corrections, forensics, specification curves."""

import numpy as np
import pytest

from explainer.psychology.psyche import meta as M


def test_random_effects_known_values():
    y = np.array([0.2, 0.5, 0.3])
    v = np.array([0.01, 0.04, 0.02])
    r = M.random_effects(y, v)
    w = 1 / v
    assert r["fixed"] == pytest.approx(np.sum(w * y) / w.sum())
    assert r["tau2"] >= 0 and 0 <= r["I2"] <= 1
    assert r["pi_lo"] <= r["lo"] <= r["mu"] <= r["hi"] <= r["pi_hi"]


def test_filter_inflates_and_registration_does_not():
    lit = M.literature(k=400, true_d=0.2, tau=0.0, publish_null=0.1, seed=1)
    pub = lit["published"]
    assert M.random_effects(lit["d"][pub], lit["v"][pub])["mu"] > 0.3
    assert abs(M.random_effects(lit["d"], lit["v"])["mu"] - 0.2) < 0.05


def test_egger_detects_filter():
    lit = M.literature(k=400, true_d=0.2, n_lo=10, n_hi=300, publish_null=0.1, seed=2)
    pub = lit["published"]
    assert M.egger(lit["d"][pub], lit["se"][pub])["p"] < 0.05


def test_selection_model_recovers_under_its_own_filter():
    ests = []
    for s in range(5):
        lit = M.literature(k=300, true_d=0.2, publish_null=0.15, seed=10 + s)
        pub = lit["published"]
        ests.append(M.selection_model(lit["d"][pub], lit["se"][pub])["est"])
    assert abs(np.mean(ests) - 0.2) < 0.08


def test_meta_regression_finds_a_big_moderator():
    rng = np.random.default_rng(3)
    x = np.repeat([0.0, 1.0], 60)
    v = np.full(120, 0.02)
    y = rng.normal(0.2 + 0.4 * x, np.sqrt(v))
    r = M.meta_regression(y, v, x)
    assert abs(r["slope"] - 0.4) < 0.1 and r["p"] < 0.001


def test_grim():
    assert not M.grim(5.19, 28)
    assert M.grim(5.18, 28)
    assert not M.grim(3.48, 17)
    s = M.sprite(3.5, 1.0, 20, 1, 7, tries=20000, seed=1)
    assert s is not None and abs(s.mean() - 3.5) < 1e-9 and round(s.std(ddof=1), 2) == 1.0


def test_statcheck():
    out = M.statcheck([(1.80, 30, 0.04, "="), (2.10, 28, 0.04, "=")])
    assert out[0]["gross"] and not out[0]["consistent"]
    assert out[1]["consistent"]


def test_spec_curve_and_audit():
    s = M.spec_curve(seed=4)
    assert s["n_specs"] == 96 and np.all(np.diff(s["est"]) >= 0)
    from explainer.psychology import ledger
    a = M.ledger_audit(ledger.rows(upto=10))
    assert a["n"] == sum(a["total"].values())
