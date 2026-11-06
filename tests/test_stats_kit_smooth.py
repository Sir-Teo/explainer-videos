"""statkit.smooth against closed forms, SciPy, and published tables."""

import math

import numpy as np
import pytest
from scipy import integrate, interpolate, stats

from explainer.stats.kit import smooth as Sm


def test_silverman_table():
    # Silverman (1986), Table 4.2
    assert [Sm.silverman_table(d) for d in range(1, 6)] == [4, 19, 67, 223, 768]


def test_kernel_constants_and_efficiency():
    for name, (K, R, m2) in Sm.KERNELS.items():
        assert integrate.quad(K, -1.5 if name != "gaussian" else -10, 1.5 if name != "gaussian" else 10)[0] == pytest.approx(1, abs=1e-8)
        lim = 10 if name == "gaussian" else 1
        assert integrate.quad(lambda u: float(K(u)) ** 2, -lim, lim)[0] == pytest.approx(R, rel=1e-6)
        assert integrate.quad(lambda u: u * u * float(K(u)), -lim, lim)[0] == pytest.approx(m2, rel=1e-6)
    assert Sm.kernel_efficiency("gaussian") == pytest.approx(0.951, abs=1e-3)
    assert Sm.kernel_efficiency("uniform") == pytest.approx(0.930, abs=1e-3)


def test_mixture_functionals_and_mise():
    mix = Sm.NormalMixture([0.5, 0.5], [-1.5, 1.5], [0.6, 0.6])
    assert mix.R(0) == pytest.approx(integrate.quad(lambda t: float(mix.pdf(t)) ** 2, -10, 10)[0], rel=1e-8)
    assert mix.R(2) == pytest.approx(integrate.quad(lambda t: float(mix.d2(t)) ** 2, -10, 10)[0], rel=1e-8)
    g = np.random.default_rng(1)
    n, h = 200, 0.3
    grid = np.linspace(-6, 6, 1201)
    ise = [np.trapezoid((Sm.kde(mix.rvs(n, g), grid, h) - mix.pdf(grid)) ** 2, grid) for _ in range(600)]
    assert abs(np.mean(ise) - mix.kde_mise(h, n)) < 3.5 * np.std(ise) / math.sqrt(600)
    edges = np.arange(-6, 6.01, 0.5)

    def hist_ise(x):
        d = Sm.histogram_density(x, edges)
        i = np.clip(np.searchsorted(edges, grid, side="right") - 1, 0, len(d) - 1)
        v = np.where((grid >= edges[0]) & (grid < edges[-1]), d[i], 0)
        return np.trapezoid((v - mix.pdf(grid)) ** 2, grid)

    hi = [hist_ise(mix.rvs(n, g)) for _ in range(600)]
    assert abs(np.mean(hi) - Sm.histogram_mise(mix.cdf, edges, n, mix.R(0))) < 3.5 * np.std(hi) / math.sqrt(600)


def test_bandwidths():
    g = np.random.default_rng(2)
    x = g.standard_normal(2000)
    hopt = Sm.amise_h(2000, 3 / (8 * math.sqrt(math.pi)))
    assert Sm.sheather_jones_h(x) == pytest.approx(hopt, rel=0.1)
    assert Sm.normal_reference_h(x) == pytest.approx(hopt, rel=0.05)
    # LSCV in closed form against the definition
    y = g.standard_normal(40)
    h = 0.4
    grid = np.linspace(-8, 8, 8001)
    a = np.trapezoid(Sm.kde(y, grid, h) ** 2, grid)
    loo = np.mean([Sm.kde(np.delete(y, i), [y[i]], h)[0] for i in range(40)])
    assert Sm.lscv(y, h) == pytest.approx(a - 2 * loo, rel=1e-6)


def test_modes():
    g = np.random.default_rng(4)
    x = np.concatenate([g.normal(-2, 0.5, 150), g.normal(2, 0.5, 150)])
    h1 = Sm.critical_bandwidth(x, 1)
    grid = np.linspace(-6, 6, 801)
    assert Sm.modes_at(x, h1 * 1.01, grid) <= 1 and Sm.modes_at(x, h1 * 0.95, grid) >= 2
    r = Sm.silverman_test(x, 1, 50, g)
    assert r["p"] < 0.05
    u = g.standard_normal(200)
    assert Sm.silverman_test(u, 1, 50, g)["p"] > 0.05


def test_smoothing_spline_against_scipy():
    g = np.random.default_rng(3)
    x = np.sort(g.uniform(0, 1, 60))
    y = np.sin(2 * np.pi * x) + 0.3 * g.standard_normal(60)
    sp = Sm.SmoothingSpline(x, y)
    for lam in (1e-6, 1e-4, 1e-2):
        s = interpolate.make_smoothing_spline(x, y, lam=lam)
        xx = np.linspace(x[0], x[-1], 300)
        assert np.max(np.abs(sp.predict(lam, xx) - s(xx))) < 1e-8
    f = sp.fit(1e-4)
    t = np.linspace(x[0], x[-1], 40001)
    s = interpolate.make_smoothing_spline(x, y, lam=1e-4)
    assert f @ sp.K @ f == pytest.approx(np.trapezoid(s.derivative(2)(t) ** 2, t), rel=1e-5)
    d, U = sp.eigen()
    S = sp.smoother(1e-3)
    assert np.allclose(S, U @ np.diag(1 / (1 + 1e-3 * d)) @ U.T, atol=1e-8)
    assert 2 < sp.df(sp.choose("gcv")) < 20 and 2 < sp.df(sp.choose("reml")) < 20
    assert sp.df(sp.lam_for_df(6.0)) == pytest.approx(6.0, abs=1e-6)
    # ties pooled with weights give the same fit as the weighted problem
    xt = np.repeat(x[:20], 2)
    yt = np.concatenate([[a, b] for a, b in zip(y[:20], y[20:40])])
    st = Sm.SmoothingSpline(xt, yt)
    sw = Sm.SmoothingSpline(x[:20], (y[:20] + y[20:40]) / 2, w=np.full(20, 2.0))
    assert np.allclose(st.fit(1e-3), sw.fit(1e-3))


def test_local_poly_reproduces_lines_and_loess():
    g = np.random.default_rng(5)
    x = np.sort(g.uniform(0, 1, 80))
    lp = Sm.local_poly(x, 2 + 3 * x, [0.0, 0.3, 1.0], 0.1, 1)
    assert np.allclose(lp["fit"], 2 + 3 * np.array([0.0, 0.3, 1.0]))
    assert np.allclose(lp["weights"].sum(1), 1)
    nw = Sm.local_poly(x, 2 + 3 * x, [0.0], 0.1, 0)["fit"][0]
    assert nw > 2.1  # Nadaraya--Watson's boundary bias
    y = np.sin(4 * x) + 0.1 * g.standard_normal(80)
    y[10] = 8.0
    assert abs(Sm.loess(x, y, [x[10]], 0.3, 1, 3)[0] - np.sin(4 * x[10])) < 0.2


def test_wavelets():
    g = np.random.default_rng(6)
    z = g.standard_normal(256)
    for h in (Sm.HAAR, Sm.D4):
        c = Sm.dwt(z, h)
        assert np.allclose(Sm.idwt(c, h), z)
        assert sum(np.sum(a ** 2) for a in c) == pytest.approx(np.sum(z ** 2))
    n = 1024
    f = Sm.dj_function("doppler", n)
    y = f + g.standard_normal(n)
    v, s = Sm.wavelet_denoise(y, "visu"), Sm.wavelet_denoise(y, "sure")
    assert v["sigma"] == pytest.approx(1, abs=0.15)
    # at SNR 7 soft VisuShrink shrinks the many large coefficients too far; SURE adapts level by level
    assert np.mean((s["fit"] - f) ** 2) < 0.6 * np.mean((v["fit"] - f) ** 2)
    assert np.mean((s["fit"] - f) ** 2) < 0.6 * np.mean((y - f) ** 2)
    h = Sm.wavelet_denoise(Sm.dj_function("heavisine", n) + g.standard_normal(n), "visu")
    assert np.mean((h["fit"] - Sm.dj_function("heavisine", n)) ** 2) < 0.6


def test_backfit_and_kernel_ridge():
    g = np.random.default_rng(7)
    X = g.uniform(-1, 1, (200, 2))
    y = np.sin(3 * X[:, 0]) + X[:, 1] ** 2 + 0.2 * g.standard_normal(200)
    b = Sm.backfit(X, y, [1e-3, 1e-3])
    assert np.corrcoef(b["f"][:, 0], np.sin(3 * X[:, 0]))[0, 1] > 0.99
    assert np.corrcoef(b["f"][:, 1], X[:, 1] ** 2)[0, 1] > 0.97
    x = np.sort(g.uniform(0, 1, 50))
    yy = np.sin(2 * np.pi * x) + 0.3 * g.standard_normal(50)
    kr = Sm.kernel_ridge(x, yy, 0.1, 0.1, x)
    K = Sm.gaussian_kernel_matrix(x, x, 0.1)
    assert np.allclose(kr["pred"], kr["fit"])
    assert np.allclose(K @ kr["alpha"] + 0.1 * kr["alpha"], yy)


def test_kde_intervals_and_grenander():
    g = np.random.default_rng(8)
    mix = Sm.NormalMixture([0.5, 0.5], [-1.5, 1.5], [0.6, 0.6])
    x0 = 1.5
    n = 500
    h = Sm.pointwise_mse_h(float(mix.pdf(x0)), float(mix.d2(x0)), n)
    hit = {False: 0, True: 0}
    for _ in range(400):
        x = mix.rvs(n, g)
        for rb in (False, True):
            lo, hi, _ = Sm.kde_ci(x, x0, h, robust=rb)
            hit[rb] += lo <= mix.pdf(x0) <= hi
    assert hit[True] / 400 > hit[False] / 400 + 0.05
    assert hit[True] / 400 > 0.9
    est = [Sm.grenander_at(Sm.grenander(g.exponential(1, 400)), [1.0])[0] for _ in range(200)]
    assert np.mean(est) == pytest.approx(math.exp(-1), abs=0.03)
    G = Sm.grenander(g.exponential(1, 300))
    assert np.all(np.diff(G["density"]) <= 1e-12)
    assert np.sum(G["density"] * np.diff(G["knots"])) == pytest.approx(1)
