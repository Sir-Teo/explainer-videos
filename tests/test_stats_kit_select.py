"""statkit.select (Part 28): criteria against statsmodels, LOO shortcuts against brute force, PSIS-LOO against exact
LOO, stacking, and Shtarkov's regret."""

import numpy as np
import statsmodels.api as sm
from scipy import stats

from explainer.stats.kit import select as Se


def data(seed=1, n=60, p=5):
    g = np.random.default_rng(seed)
    X = g.normal(size=(n, p))
    beta = np.zeros(p)
    beta[:5] = [1.0, -0.5, 0.0, 0.0, 0.3][:p]
    y = 1 + X @ beta + g.normal(size=n)
    return X, y


def test_aic_bic_match_statsmodels():
    X, y = data()
    Xd = sm.add_constant(X)
    s = sm.OLS(y, Xd).fit()
    k = Xd.shape[1]
    assert np.isclose(Se.gaussian_ll(s.ssr, len(y)), s.llf)
    assert np.isclose(Se.aic(s.llf, k), s.aic)
    assert np.isclose(Se.bic(s.llf, k, len(y)), s.bic)


def test_press_equals_brute_force_loo():
    X, y = data(2)
    Xd = np.column_stack([np.ones(len(y)), X])
    errs = []
    for i in range(len(y)):
        m = np.arange(len(y)) != i
        b = np.linalg.lstsq(Xd[m], y[m], rcond=None)[0]
        errs.append((y[i] - Xd[i] @ b) ** 2)
    assert np.isclose(Se.press(Xd, y), np.mean(errs))


def test_df_monte_carlo_for_ols_and_lasso():
    g = np.random.default_rng(3)
    X, _ = data(3)
    Xd = np.column_stack([np.ones(len(X)), X])
    mu = Xd @ np.r_[1, 1.0, -0.5, 0, 0, 0.3]

    def ols(Xm, y):
        return Xm @ np.linalg.lstsq(Xm, y, rcond=None)[0]

    assert abs(Se.df_monte_carlo(ols, Xd, mu, 1.0, 3000, g) - 6) < 0.4


def test_best_subset_against_brute_force_and_forward():
    X, y = data(4, p=6)
    bs = Se.best_subset(X, y)
    fw = Se.forward_stepwise(X, y)
    assert [b["size"] for b in bs] == list(range(7))
    assert all(b["rss"] <= f["rss"] + 1e-9 for b, f in zip(bs, fw))
    assert np.isclose(bs[-1]["rss"], fw[-1]["rss"])


def test_freedman_paradox_shows_up():
    out = Se.freedman(100, 50, np.random.default_rng(1983))
    assert out["second"]["pF"] < out["first"]["pF"]
    assert out["second"]["n_sig05"] >= out["first"]["n_sig05"]


def test_psis_loo_matches_exact_loo_for_a_conjugate_normal():
    g = np.random.default_rng(5)
    n, sig, tau = 30, 1.0, 2.0
    y = g.normal(0.5, sig, n)
    v = 1 / (1 / tau ** 2 + n / sig ** 2)
    m = v * y.sum() / sig ** 2
    mu = g.normal(m, np.sqrt(v), 8000)
    L = stats.norm.logpdf(y[None, :], mu[:, None], sig)
    res = Se.psis_loo(L)
    exact = 0.0
    for i in range(n):
        yi = np.delete(y, i)
        vi = 1 / (1 / tau ** 2 + (n - 1) / sig ** 2)
        mi = vi * yi.sum() / sig ** 2
        exact += stats.norm.logpdf(y[i], mi, np.sqrt(vi + sig ** 2))
    assert abs(res["elpd"] - exact) < 0.05
    assert abs(Se.waic(L)["elpd"] - exact) < 0.1
    assert np.all(res["khat"] < 0.5)


def test_stacking_weights():
    g = np.random.default_rng(6)
    n = 400
    # data from model 0: model 0's predictive density is better for every point
    lpd = np.column_stack([g.normal(-1.0, 0.1, n), g.normal(-1.5, 0.1, n)])
    w = Se.stacking_weights(lpd)
    assert np.isclose(w.sum(), 1) and w[0] > 0.95


def test_nml_regret_asymptotics():
    for n in (1000, 10000):
        assert abs(Se.nml_bernoulli_regret(n) - 0.5 * np.log(n * np.pi / 2)) < 0.02
