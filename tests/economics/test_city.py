"""Agora's city (Part 37): each model checked against something it does not compute itself."""

import numpy as np

from explainer.economics.agora import city
from explainer.economics.island import truths

T = truths(37)


def test_schelling_sorts_and_settles():
    r = city.schelling(30, 0.1, 1 / 3, seed=1)
    assert r["settled"] and r["moves"] > 0
    assert r["final_like"] > r["like"][0] + 0.15
    g = np.array(r["frames"][-1])
    assert g.shape == (30, 30) and set(np.unique(g)) <= {0, 1, 2}
    assert abs(city.like_share(g) - r["final_like"]) < 1e-12
    # counts of each kind are conserved
    a0, a1 = np.array(r["frames"][0]), g
    assert all((a0 == k).sum() == (a1 == k).sum() for k in (0, 1, 2))
    # nobody moves when nobody minds
    assert city.schelling(20, 0.1, 0.0, seed=2)["moves"] == 0


def test_schelling_tolerance_curve_rises():
    sw = city.schelling_sweep([0.1, 0.3, 0.5], seeds=(0, 1), n=20)
    assert sw["like"][0] < sw["like"][1] < sw["like"][2]


def test_thunen_envelope_and_rings():
    x = np.linspace(0, 110, 1101)
    th = city.thunen(list(T["thunen"]), x)
    assert [n for n, _, _ in th["rings"]] == ["vegetables and milk", "firewood", "grain", "cattle"]
    assert np.allclose(th["rent"], np.maximum(np.max(th["bids"], axis=0), 0))
    assert abs(th["rings"][1][1] - 3.0) < 0.15 and abs(th["rings"][2][2] - 35.0) < 0.15


def test_monocentric_muth_and_population():
    M = T["mono"]
    kw = {k: M[k] for k in ("N", "y", "t", "alpha", "theta", "i")}
    m = city.monocentric(**kw)
    x, p, h, D = (np.array(m[k]) for k in ("x", "p", "h", "D"))
    inside = np.isfinite(p)
    # Muth's condition: p'(x) h(x) = -t
    dp = np.gradient(p[inside], x[inside])
    assert np.allclose((dp * h[inside])[5:-5], -M["t"], rtol=2e-3)
    # the households add up
    assert abs(np.trapezoid(D * 2 * np.pi * x, x) / M["N"] - 1) < 1e-6
    car = city.monocentric(**{**kw, "t": M["t"] * 0.5})
    lift = city.monocentric(**{**kw, "i": M["i"] * 0.6})
    assert car["edge"] > m["edge"] and car["centre_density"] < m["centre_density"]
    assert abs(lift["edge"] - m["edge"]) < 0.2 and lift["u"] > m["u"]


def test_agglomeration_movers_recover_the_truth():
    A = T["agglo"]
    r = city.agglomeration_panel(gamma=A["gamma"], sort=A["sort"], seed=A["seed"])
    assert r["naive"] > A["gamma"] + 0.01
    assert abs(r["movers"] - A["gamma"]) < 0.006


def test_zipf_fit_on_a_pareto_sample():
    rng = np.random.default_rng(0)
    s = (1 - rng.random(4000)) ** (-1 / 1.2)
    f = city.zipf_fit(s, top=400)
    assert abs(f["zeta"] - 1.2) < 3 * f["se"]


def test_gibrat_with_a_floor_is_close_to_zipf():
    g = city.gibrat(n=8000, T=2500, sigma=0.2, floor=0.05, seed=3)
    assert abs(g["zeta"] - g["theory"]) < 0.25
    assert np.nanmax(g["growth_sd_by_quintile"][1:]) / np.nanmin(g["growth_sd_by_quintile"][1:]) < 1.5


def test_core_periphery_break_point():
    P = T["cp"]
    b = city.cp_break(P["mu"], P["sigma"])
    # the symmetric spread is an equilibrium, and the gap's slope there changes sign at the break point
    e = city.cp_solve(0.5, 1.7, P["mu"], P["sigma"])
    assert abs(e["omega1"] - e["omega2"]) < 1e-10
    lo = city.cp_gap(b - 0.03, [0.49, 0.51], P["mu"], P["sigma"])
    hi = city.cp_gap(b + 0.03, [0.49, 0.51], P["mu"], P["sigma"])
    assert lo[1] - lo[0] > 0 > hi[1] - hi[0]
    assert city.cp_sustain(P["mu"], P["sigma"]) > b
    tom = city.cp_tomahawk([1.4, 2.0], P["mu"], P["sigma"], n_lam=41)
    assert (0.5, False) in [(lam, st) for lam, st in tom["points"][0]["eq"]]
    assert tom["points"][1]["eq"] == [(0.5, True)]


def test_roback_equal_utility_and_quality_of_life():
    t = T["towns"]
    R = city.roback(t["a"], t["q"], t["eta"], b=t["b"], alpha=t["alpha"])
    u = np.array(R["logw"]) - t["alpha"] * np.array(R["logr"]) + np.array(t["q"])
    assert np.allclose(u, R["v"]) and abs(sum(R["N"]) - 1) < 1e-10
    assert np.allclose(R["qol"], np.array(t["q"]) - np.mean(t["q"]))
    sh = city.roback_shock(t["a"], t["q"], t["eta"], 0, deta=3.0, b=t["b"], alpha=t["alpha"])
    assert sh["dlogr"] < 0 < sh["dlogN"] and sh["dv"] > 0


def test_wall_experiment():
    W = city.wall_experiment(**T["berlin"])
    d = np.array(W["division"])
    assert d[-1] < -0.1 and d.max() > 0.1 and abs(d.mean()) < 1e-12
    assert np.allclose(W["reunification"], -d)
    assert W["integrated"]["converged"] and W["divided"]["converged"]
