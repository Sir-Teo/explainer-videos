"""Agora's solver harness (Part 51): the Bellman operator's contraction, value and policy iteration, interpolation,
the endogenous grid method, projection, perturbation, accuracy, quadrature, continuous time, the zero bound and
sparse grids."""

import numpy as np
import pytest

from explainer.economics.agora import solve as S


@pytest.fixture(scope="module")
def m():
    return S.growth()


def test_steady_state(m):
    assert S.mpk(m["kss"], m) == pytest.approx(1 / m["beta"])
    assert m["css"] == pytest.approx(S.resources(m["kss"], m) - m["kss"])


def test_contraction_and_blackwell(m):
    g = S.kgrid(m, 120)
    cp = S.contraction_path(m, g, 80)
    assert cp["ratio"][-1] == pytest.approx(m["beta"], abs=1e-3)
    b = S.blackwell(m, g)
    assert b["monotone"] and b["discount_error"] < 1e-12


def test_vfi_and_howard_agree(m):
    g = S.kgrid(m, 150)
    v = S.vfi(m, g, tol=1e-9)
    h = S.howard(m, g)
    assert np.array_equal(v["j"], h["j"])
    assert h["iters"] < v["iters"] / 5
    assert np.max(np.abs(v["V"] - h["V"])) < 1e-6


def test_finer_grids_and_interpolation_are_more_accurate(m):
    errs = []
    for n in (30, 300):
        g = S.kgrid(m, n)
        r = S.vfi(m, g, tol=1e-8)
        errs.append(S.euler_errors(m, lambda k, g=g, r=r: S.resources(k, m) - np.interp(k, g, r["kprime"]))["max"])
    assert errs[1] < errs[0]
    cub = S.vfi_continuous(m, S.kgrid(m, 40), "cubic")
    assert S.euler_errors(m, cub["c"])["max"] < -5


def test_collocation_converges_and_galerkin_agrees(m):
    e = [S.euler_errors(m, S.collocation(m, n)["c"])["max"] for n in (3, 6, 9)]
    assert e[0] > e[1] > e[2] and e[2] < -6
    g = S.galerkin(m, 6)
    c = S.collocation(m, 6)
    k = np.linspace(0.6, 1.4, 9) * m["kss"]
    assert np.max(np.abs(g["c"](k) - c["c"](k))) < 1e-4


def test_perturbation_matches_the_accurate_rule_near_the_steady_state(m):
    acc = S.collocation(m, 11)
    p1, p2 = S.perturbation(m, 1), S.perturbation(m, 2)
    h = 1e-4 * m["kss"]
    slope = ((S.resources(m["kss"] + h, m) - acc["c"](m["kss"] + h))
             - (S.resources(m["kss"] - h, m) - acc["c"](m["kss"] - h))) / (2 * h)
    assert p1["g1"] == pytest.approx(slope, abs=1e-5)
    k = 1.3 * m["kss"]
    true = S.resources(k, m) - acc["c"](k)
    assert abs(p2["kprime"](k) - true) < abs(p1["kprime"](k) - true)


def test_implicit_derivative_matches_finite_differences(m):
    r = S.collocation_derivative(m, 8, "beta")
    assert r["dc_ift"] == pytest.approx(r["dc_fd"], rel=1e-5)


def test_egm_beats_grid_vfi_on_the_household():
    h = S.household(n_a=150)
    e = S.egm(h)
    v = S.household_vfi(h)
    assert S.household_euler_errors(h, e["c"])["max"] < S.household_euler_errors(h, v["c"])["max"] - 1
    assert np.max(np.abs(e["c"] - v["c"])) < 0.5
    # the borrowing limit binds at the bottom of the grid for the lowest income
    assert e["c"][0, 0] == pytest.approx(h["R"] * h["a"][0] + h["y"][0] - h["a_min"])


def test_precautionary_saving():
    risky = S.egm(S.household(sigma=0.2))["c"]
    safe = S.egm(S.household(sigma=1e-4))["c"]
    assert np.all(risky[10:150, 2] < safe[10:150, 2] + 1e-9)


def test_quadrature_beats_monte_carlo():
    q = S.quadrature_error(lambda x: np.exp(0.5 * x), float(np.exp(0.125)), ns=(3, 7), draws=(10000,))
    assert q["gh"][1] < 1e-10 and q["mc"][0] > 1e-4


def test_hjb_and_its_distribution():
    r = S.hjb_household(n=200)
    a = np.array(r["a"])
    g = np.array(r["g"])
    assert (g.sum() * (a[1] - a[0])) == pytest.approx(1.0)
    s = np.array(r["s"])
    assert s[-1, 0] < 0 and s[0, 1] > 0       # the rich low earner dissaves; the poor high earner saves
    assert r["nnz"] < 4 * r["size"]


def test_zero_bound_by_guess_and_verify():
    z = S.zlb_occbin(T=4, rn_low=-2.0)
    i = np.array(z["i"])
    assert np.all(i >= -1e-9)
    assert min(z["i_free"]) < 0
    assert z["x"][0] < z["x_free"][0]
    assert z["bound_quarters"] >= 1


def test_smolyak_counts_and_exactness():
    assert [S.smolyak_count(d, 2) for d in (1, 2, 3, 10)] == [5, 13, 25, 221]
    assert S.tensor_count(3, 2) == 125
    rng = np.random.default_rng(0)
    X = rng.uniform(-1, 1, (40, 3))
    f = lambda Z: 1 + Z[:, 0] ** 2 * Z[:, 1] ** 2 - Z[:, 2] ** 3  # noqa: E731
    r = S.smolyak_interpolate(f, 3, 3, X)
    assert np.max(np.abs(r["values"] - f(X))) < 1e-10
