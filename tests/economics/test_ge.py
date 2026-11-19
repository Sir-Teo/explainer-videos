"""Agora's general equilibrium (Part 9), each result checked against a closed form or a second method."""

import numpy as np
import pytest

from explainer.economics.agora import ge

ANA = ge.Trader((0.4, 0.6), (8.0, 1.5), name="Ana")
BO = ge.Trader((0.6, 0.4), (2.0, 8.5), name="Bo")


def test_demands_and_walras_law():
    rng = np.random.default_rng(0)
    traders = [ge.Trader((0.2, 0.5, 0.3), (1, 2, 0)), ge.Trader((0.3, 0.3, 0.4), (0, 1, 3), kind="ces", rho=-1.0),
               ge.Trader((1, 2, 1), (2, 0, 1), kind="leontief")]
    for _ in range(20):
        p = rng.uniform(0.1, 3, 3)
        for t in traders:
            assert np.dot(p, t.demand(p)) == pytest.approx(t.wealth(p))
        assert np.dot(p, ge.excess(traders, p)) == pytest.approx(0, abs=1e-10)
    # CES demand maximizes utility on the budget line
    t = traders[1]
    p = np.array([1.0, 2.0, 0.5])
    x = t.demand(p)
    for d in rng.normal(0, 0.05, (50, 3)):
        d -= np.dot(p, d) / np.dot(p, p) * p          # stay on the budget line
        if np.all(x + d > 0):
            assert t.utility(x + d) <= t.utility(x) + 1e-12


def test_box_equilibrium_and_contract_curve():
    eq = ge.box_equilibrium(ANA, BO)
    assert np.allclose(ge.excess([ANA, BO], [eq["p"], 1.0]), 0, atol=1e-12)
    # the equilibrium allocation is on the contract curve, and MRS = price for both
    x = eq["xA"]
    assert x[1] == pytest.approx(float(ge.contract_curve(ANA, BO, x[0])))
    mrsA = ANA.a[0] / ANA.a[1] * x[1] / x[0]
    xb = eq["xB"]
    mrsB = BO.a[0] / BO.a[1] * xb[1] / xb[0]
    assert mrsA == pytest.approx(eq["p"]) and mrsB == pytest.approx(eq["p"])
    lo, hi = ge.lens_ends(ANA, BO)
    assert lo < x[0] < hi


def test_core_shrinks_to_the_competitive_allocation():
    xw = ge.box_equilibrium(ANA, BO)["xA"][0]
    widths = []
    for r in (1, 2, 4, 8):
        lo, hi = ge.core_interval(ANA, BO, r)
        assert lo <= xw + 1e-9 and hi >= xw - 1e-9
        widths.append(hi - lo)
    assert all(a > b for a, b in zip(widths, widths[1:]))
    assert widths[-1] < 0.1 * widths[0]
    # the competitive allocation itself is never blocked
    assert all(ge.blocks(ANA, BO, xw, s, t) < 1e-8 for s in range(1, 6) for t in range(1, 6))


def test_sperner_walk_finds_an_approximate_equilibrium():
    T3 = [ge.Trader((0.5, 0.3, 0.2), (2, 0, 0)), ge.Trader((0.1, 0.6, 0.3), (0, 1, 0)),
          ge.Trader((0.3, 0.2, 0.5), (0, 0, 1.5))]
    z = lambda p: ge.excess(T3, p)  # noqa: E731
    exact = np.array(ge.newton(z, [1.0, 0.7, 0.4])["p"])
    exact /= exact.sum()
    errs = []
    for N in (10, 40, 160):
        lab = ge.sperner_labels(z, N)
        # Sperner's rule on the boundary
        for (i, j), k in lab.items():
            p = ge.simplex_point((i, j), N)
            assert p[k] > 0
        w = ge.sperner_walk(lab, N)
        assert sorted(lab[tuple(v)] for v in w["room"]) == [0, 1, 2]
        errs.append(np.max(np.abs(np.array(w["p"]) - exact)))
    assert errs[-1] < 0.02 and errs[-1] < errs[0]


def test_newton_and_tatonnement_agree_on_gross_substitutes():
    rng = np.random.default_rng(3)
    traders = [ge.Trader(tuple(rng.dirichlet(np.ones(4))), tuple(rng.uniform(0, 2, 4))) for _ in range(6)]
    z = lambda p: ge.excess(traders, p)  # noqa: E731
    nw = ge.newton(z, [1, 1, 1, 1])
    assert nw["history"][-1]["err"] < 1e-10
    p0 = np.array([0.9, 0.2, 0.5, 0.6])
    ta = ge.tatonnement(z, p0, T=200)
    P = np.array(ta["p"])
    assert np.sum(P[-1] ** 2) == pytest.approx(np.sum(p0 ** 2), rel=1e-6)   # Walras's law conserves |p|
    assert np.allclose(P[-1] / P[-1][0], np.array(nw["p"]), rtol=1e-4)


def test_scarf_cycles_for_ever():
    out = ge.scarf_path([0.5, 0.7, 0.5196], T=80)
    P = np.array(out["p"])
    assert np.ptp(out["norm"]) < 1e-6 and np.ptp(out["product"]) < 1e-6
    dist = np.linalg.norm(P - P.mean(axis=1, keepdims=True), axis=1)
    assert dist.min() > 0.05                        # never approaches equal prices
    assert np.allclose(ge.scarf_excess([1, 1, 1]), 0)


def test_crusoe_market_equals_plan():
    c = ge.crusoe(2.0, 0.5, 12.0, 0.6)
    assert c["market"]["L"] == pytest.approx(c["plan"]["L"], rel=1e-9)
    assert c["market"]["w"] == pytest.approx(c["market"]["mpl"]) == pytest.approx(c["mrs"])


def test_three_equilibria():
    q = ge.quasilinear_three()
    roots = ge.equilibria_2good(q["z2"], 0.05, 20)
    assert np.allclose(roots, [0.5, 1.0, 2.0], atol=1e-9)


def test_arrow_securities_share_risk_and_a_bond_does_not():
    e0, E = [50, 50], [[80, 20], [20, 80]]
    ad = ge.arrow_debreu(e0, E, [0.5, 0.5], 0.95, [2, 2])
    C = np.array(ad["c"])
    assert np.allclose(C[:, 0], C[:, 1], rtol=1e-8)          # no aggregate risk: full insurance
    assert np.allclose(C.sum(axis=0), np.sum(E, axis=0))
    bo = ge.bond_only(e0, E, [0.5, 0.5], 0.95, [2, 2])
    assert all(a > b for a, b in zip(ad["ce"], bo["ce"]))
    assert np.allclose(np.sum(bo["b"]), 0, atol=1e-9)


def test_kantorovich_duals_decentralize_the_plan():
    k = ge.kantorovich([[3, 1], [2, 2], [1, 3]], [1, 1])
    assert k["sets"] == pytest.approx(4.0)
    t, v, mv = np.array(k["plan"]), np.array(k["value_per_day"]), np.array(k["machine_value"])
    assert np.all(v <= mv[:, None] + 1e-9)                   # no machine could earn more elsewhere
    assert np.all((t < 1e-9) | (np.abs(v - mv[:, None]) < 1e-9))   # and each works only where it earns the most
    # strong duality: the value of the machines equals the value of the sets
    assert float(mv.sum()) == pytest.approx(k["sets"] * float(np.dot(k["part_value"], [1, 1])))


def test_misallocation_matches_hsieh_klenow_formula():
    rng = np.random.default_rng(1)
    la, lt = rng.normal(0, 0.2, 400_000), rng.normal(0, 0.63, 400_000)
    m = ge.misallocation(la, lt, 3.0)
    assert m["gain"] == pytest.approx(m["lognormal"], rel=0.02)
    assert ge.misallocation(la, np.zeros_like(la), 3.0)["gain"] == pytest.approx(0, abs=1e-12)


def test_top_trading_cycles_is_in_the_core():
    rng = np.random.default_rng(5)
    for _ in range(30):
        n = 6
        prefs = [list(rng.permutation(n)) for _ in range(n)]
        a = ge.top_trading_cycles(prefs)["assign"]
        assert sorted(a) == list(range(n))
        rank = lambda i, h: prefs[i].index(h)  # noqa: E731
        assert all(rank(i, a[i]) <= rank(i, i) for i in range(n))          # nobody worse than keeping their hut
        # no pair can both do better by swapping their original huts
        for i in range(n):
            for j in range(n):
                if i != j:
                    assert not (rank(i, j) < rank(i, a[i]) and rank(j, i) < rank(j, a[j]))
