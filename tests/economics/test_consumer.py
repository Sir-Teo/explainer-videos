"""Agora's consumer (Part 5): demand against brute force, revealed preference against its theorems."""

import numpy as np
import pytest

from explainer.economics.agora import consumer as cs

PREFS = [cs.Preference("cobb-douglas", a=0.3), cs.Preference("ces", a=0.4, sigma=0.5),
         cs.Preference("ces", a=0.6, sigma=2.5), cs.Preference("complements", a=1.0, b=2.0),
         cs.Preference("quasilinear", a=6.0), cs.Preference("substitutes", a=1.0, b=1.5)]


@pytest.mark.parametrize("pref", PREFS, ids=lambda p: f"{p.kind}-{p.sigma}")
def test_demand_is_the_best_point_on_the_budget(pref):
    for px, py, m in ((1.0, 2.0, 30.0), (3.0, 1.0, 24.0), (2.0, 2.0, 10.0)):
        x, y = pref.demand(px, py, m)
        assert px * x + py * y == pytest.approx(m)
        xs = np.linspace(0, m / px, 20001)
        best = cs.best_on_frontier(pref, xs, (m - px * xs) / py)
        assert float(pref.u(x, y)) >= best["u"] - 1e-6 * max(1.0, abs(best["u"]))


def test_tangency_mrs_equals_the_price_ratio():
    for pref in PREFS[:3]:
        x, y = pref.demand(2.0, 3.0, 60.0)
        assert pref.mrs(x, y) == pytest.approx(2.0 / 3.0)
    x, y = PREFS[4].demand(1.0, 1.0, 30.0)      # quasilinear, interior
    assert PREFS[4].mrs(x, y) == pytest.approx(1.0)


def test_indifference_curves_hold_utility_fixed():
    for pref in PREFS[:3] + [PREFS[4]]:
        xs = np.linspace(1, 9, 9)
        ys = pref.indifference(2.0, xs)
        ok = np.isfinite(ys)
        assert np.allclose(pref.u(xs[ok], ys[ok]), 2.0)


def _budgets(n, rng, k=2):
    P = rng.uniform(0.5, 3.0, (n, k))
    m = rng.uniform(20, 60, n)
    return P, m


def test_a_utility_maximizer_passes_and_afriat_rationalizes():
    rng = np.random.default_rng(5)
    P, m = _budgets(15, rng)
    pref = cs.Preference("ces", a=0.45, sigma=0.7)
    X = np.array([pref.demand(px, py, mm) for (px, py), mm in zip(P, m)])
    assert not cs.garp_violations(P, X) and not cs.sarp_violations(P, X) and cs.ccei(P, X) == 1.0
    sol = cs.afriat(P, X)
    assert sol is not None
    u = cs.afriat_utility(P, X, sol)
    for i, ((px, py), mm) in enumerate(zip(P, m)):
        xs = np.linspace(0, mm / px, 400)
        Z = np.column_stack([xs, (mm - px * xs) / py])
        assert u(X[i][None])[0] >= u(Z).max() - 1e-7      # the observed choice is best on its own budget


def test_afriat_has_no_solution_exactly_when_garp_fails():
    rng = np.random.default_rng(11)
    for _ in range(40):
        P, m = _budgets(6, rng)
        X = cs.random_on_budgets(P, m, rng)
        assert (cs.afriat(P, X) is None) == bool(cs.garp_violations(P, X))


def test_two_choices_that_contradict_each_other():
    P = np.array([[1.0, 1.0], [3.0, 1.0]])
    X = np.array([[1.0, 5.0], [5.0, 0.5]])   # each chose a bundle the other could also afford
    r1 = P[0] @ X[1] / (P[0] @ X[0])
    r2 = P[1] @ X[0] / (P[1] @ X[1])
    assert cs.warp_violations(P, X) == [(0, 1)]
    assert cs.ccei(P, X) == pytest.approx(max(r1, r2))
    assert len(cs.houtman_maks(P, X)) == 1


def test_ccei_against_a_plain_bisection():
    rng = np.random.default_rng(3)
    for _ in range(25):
        P, m = _budgets(8, rng, k=3)
        X = cs.random_on_budgets(P, m, rng)
        lo, hi = 0.0, 1.0
        if cs.garp_violations(P, X):
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                lo, hi = (mid, hi) if not cs.garp_violations(P, X, mid) else (lo, mid)
            assert cs.ccei(P, X) == pytest.approx(hi, abs=1e-8)
        else:
            assert cs.ccei(P, X) == 1.0


def test_warshall_closure_matches_path_search():
    rng = np.random.default_rng(0)
    R0 = rng.random((9, 9)) < 0.2
    R = cs.closure(R0)
    for i in range(9):
        seen, frontier = set(), [i]
        while frontier:
            a = frontier.pop()
            for b in np.flatnonzero(R0[a]):
                if b not in seen:
                    seen.add(int(b))
                    frontier.append(int(b))
        assert set(np.flatnonzero(R[i]).tolist()) == seen


def test_varian_bounds_bracket_the_true_indifference_curve():
    rng = np.random.default_rng(8)
    P, m = _budgets(12, rng)
    pref = cs.Preference("cobb-douglas", a=0.4)
    X = np.array([pref.demand(px, py, mm) for (px, py), mm in zip(P, m)])
    k = 0
    level = float(pref.u(*X[k]))
    xs = np.linspace(0.5, 80, 400)
    ys = pref.indifference(level, xs)
    for i in cs.revealed_worse(P, X, k):
        inside = P[i, 0] * xs + P[i, 1] * ys < P[i] @ X[i] - 1e-6
        assert not inside.any()                      # the curve never dips into a revealed-worse budget
    for z in cs.revealed_better(P, X, k):
        assert float(pref.u(*z)) >= level - 1e-9


def test_random_choosers_fail_on_crossing_budgets_and_becker_demand_slopes_down():
    P = np.array([[1, 1], [1, 3], [3, 1], [1, 2], [2, 1], [1, 4], [4, 1]], float)
    b = cs.bronars(P, np.full(len(P), 12.0), reps=400)
    assert b["power"] > 0.25 and b["ccei_mean"] < 0.99
    more = cs.bronars(np.vstack([P, P[::-1] * [1.3, 0.8]]), np.full(2 * len(P), 12.0), reps=400)
    assert more["power"] > b["power"]                # more budgets, a more powerful test
    d = cs.becker_demand([1, 2, 3, 4], 12.0, people=20000)
    assert np.all(np.diff(d["mean"]) < 0)
    assert np.allclose(d["mean"], d["theory"], rtol=0.02)


def test_lexicographic_order():
    assert cs.lexicographic_rank([(1, 9), (2, 0), (1, 10)]) == [0, 2, 1]


def test_earners_bunch_at_the_credit_kink_by_the_predicted_amount():
    rng = np.random.default_rng(2)
    n = rng.uniform(4000, 14000, 20000)
    assert np.array_equal(cs.earnings_choice(n, 0.0), n)                 # no response, no bunching
    for e in (0.25, 1.0):
        z = cs.earnings_choice(n, e)
        at_kink = np.abs(z - 8580) < 5
        lo = 8580 / 1.34 ** e                                            # these would earn above the kink, but stop
        predicted = np.mean((n >= lo) & (n <= 8580))
        assert np.mean(at_kink) == pytest.approx(predicted, abs=0.01)
        below = (n < lo - 50)
        assert np.allclose(z[below], n[below] * 1.34 ** e, atol=10)    # the phase-in subsidy raises earnings


def test_logit_recovers_planted_coefficients():
    rng = np.random.default_rng(4)
    X = np.column_stack([rng.uniform(0, 30, 50000), rng.uniform(0, 15, 50000)])
    b = np.array([0.125, -0.5])
    y = (rng.random(50000) < 1 / (1 + np.exp(-X @ b))).astype(float)
    fit = cs.logit_fit(X, y)
    assert np.allclose(fit["b"], b, atol=4 * fit["se"].max())

