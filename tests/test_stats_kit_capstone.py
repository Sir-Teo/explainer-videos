"""statkit.capstone, the design-based regression in statkit.survey, the World's health block, the Museum's NHANES
extract, and Part 20's pipeline."""

import numpy as np
import pytest

from explainer.stats import museum
from explainer.stats.kit import capstone as C
from explainer.stats.kit import survey as SV
from explainer.stats.world import World


def test_decision_log_counts():
    log = C.DecisionLog(10)
    k = np.ones(10, bool)
    k = log.apply(k, np.arange(10) >= 2, "a")
    k = log.apply(k, np.arange(10) % 2 == 0, "b")
    t = log.table()
    assert [s["left"] for s in t] == [10, 8, 4]
    assert [s["removed"] for s in t] == [0, 2, 4]


def test_rcs_basis_is_linear_beyond_the_outer_knots():
    x = np.linspace(80, 100, 21)
    B = C.rcs_basis(x, [25, 40, 55, 70])
    assert B.shape == (21, 3)
    second = np.diff(B, 2, axis=0)
    assert np.allclose(second, 0, atol=1e-9)
    xl = np.linspace(0, 20, 21)  # below the first knot: only x is non-zero
    assert np.allclose(C.rcs_basis(xl, [25, 40, 55, 70])[:, 1:], 0)


def test_reliability_and_regression_calibration_recover_the_slope():
    g = np.random.default_rng(0)
    n = 200_000
    z = g.normal(size=n)
    x = 0.5 * z + g.normal(size=n)  # usual intake, partly explained by z
    w1, w2 = x + g.normal(0, np.sqrt(2), n), x + g.normal(0, np.sqrt(2), n)
    y = 2.5 * x + 1.0 * z + g.normal(size=n)
    assert C.reliability(w1, w2) == pytest.approx(1.25 / 3.25, abs=0.01)
    naive = np.linalg.lstsq(np.column_stack([np.ones(n), w1, z]), y, rcond=None)[0][1]
    rc = C.regression_calibration(w1, w2, z)
    fixed = np.linalg.lstsq(np.column_stack([np.ones(n), rc["xhat"], z]), y, rcond=None)[0][1]
    assert naive == pytest.approx(2.5 / 3, abs=0.03)  # lambda given z = Var(x|z) / Var(w|z) = 1 / 3
    assert rc["lam"] == pytest.approx(1 / 3, abs=0.01)
    assert fixed == pytest.approx(2.5, abs=0.05)


def test_svy_ols_design_se_reduces_to_the_sandwich_for_one_unit_per_psu():
    g = np.random.default_rng(1)
    n = 500
    X = np.column_stack([np.ones(n), g.normal(size=n)])
    y = X @ [1.0, 2.0] + g.normal(size=n) * (1 + np.abs(X[:, 1]))
    w = g.uniform(0.5, 2, n)
    r = SV.svy_ols(X, y, w, np.ones(n), np.arange(n))
    assert np.allclose(r["se_design"], r["se_hc"] * np.sqrt(n / (n - 1)))
    b = np.linalg.lstsq(X * np.sqrt(w)[:, None], y * np.sqrt(w), rcond=None)[0]
    assert np.allclose(r["b"], b)


def test_svy_mean_matches_the_linearization_formula():
    g = np.random.default_rng(2)
    strata = np.repeat([1, 2, 3], 40)
    psu = np.tile(np.repeat([1, 2], 20), 3)
    y = g.normal(size=120) + psu
    w = g.uniform(1, 3, 120)
    r = SV.svy_mean(y, w, strata, psu)
    m = np.sum(w * y) / w.sum()
    v = 0.0
    for h in (1, 2, 3):
        t = [np.sum((w * (y - m))[(strata == h) & (psu == j)]) / w.sum() for j in (1, 2)]
        v += 2 * ((t[0] - np.mean(t)) ** 2 + (t[1] - np.mean(t)) ** 2)
    assert r["mean"] == pytest.approx(m)
    assert r["se"] == pytest.approx(np.sqrt(v))


def test_rao_wu_weights_with_two_psus_per_stratum():
    strata = np.repeat([1, 2], 10)
    psu = np.tile(np.repeat([1, 2], 5), 2)
    w = np.ones(20)
    R = SV.psu_bootstrap_weights(w, strata, psu, 50, np.random.default_rng(3))
    assert R.shape == (50, 20)
    for row in R:  # one PSU doubled, the other dropped, in each stratum
        for h in (1, 2):
            vals = sorted({row[(strata == h) & (psu == j)][0] for j in (1, 2)})
            assert vals == [0.0, 2.0]
    assert np.allclose(R.sum(1), w.sum())


def test_world_health_block():
    W = World()
    h = W.health
    a = W.adult
    assert np.all(np.isnan(h["sbp"][~a])) and not h["told_high"][~a].any()
    assert W.truth("sodium_effect") == 1.5
    assert 3.3 < h["na_usual"][a].mean() / 1000 < 3.7
    assert 120 < W.truth("mean_sbp") < 128
    r = np.corrcoef(h["na_day1"][a], h["na_day2"][a])[0, 1]
    assert 0.3 < r < 0.45
    # current sodium is cut only among the told
    told = h["told_high"] & a
    assert np.allclose(h["na_current"][told], 0.9 * h["na_usual"][told])
    assert np.allclose(h["na_current"][a & ~told], h["na_usual"][a & ~told])


def test_museum_nhanes_extract():
    d = museum.nhanes()
    assert len(d["seqn"]) == 5533
    for c in ("wt_mec", "wt_diet1", "strata", "psu", "sbp1", "na1", "na2", "kcal1", "bmi", "bp_meds"):
        assert c in d
    assert np.nanmin(d["age"]) == 18 and np.nanmax(d["age"]) == 80
    assert len({(a, b) for a, b in zip(d["strata"], d["psu"])}) == 30


def test_pipeline_primary_analysis():
    from videos.stats.stats20 import pipeline as P

    d = P.nhanes_frame()
    keep, log = P.clean(d)
    t = log.table()
    assert t[-1]["left"] == keep.sum() == 3071
    assert all(a["left"] - b["removed"] == b["left"] for a, b in zip(t, t[1:]))
    r = P.fit(d, keep=keep)
    assert r["names"][1] == "sodium"
    assert abs(r["est"]) < 0.5 and 0.15 < r["est_se"] < 0.4
