"""Tests for statkit.dfree, the distribution-free toolkit of Part 57."""

import numpy as np
from scipy import stats

from explainer.stats.kit import dfree as F


def rng(seed=0):
    return np.random.default_rng(seed)


def test_bahadur_savage_and_quantile_lemma():
    r = rng(1)
    for eps in (0.03, 0.003):
        ub = F.bahadur_savage_coverage(50, eps)["upper"]
        sim = F.bahadur_savage_sim(50, eps, r, reps=4000)
        assert sim <= ub + 0.02
    assert F.bahadur_savage_sim(50, 0.003, r, reps=4000) < 0.2  # coverage can be driven toward zero
    # the no-atom term is the exact noncentral-t probability, checked by simulating N(0, 1) samples of size 5
    b = F.bahadur_savage_coverage(5, 0.01, shift=0.7)
    x = rng(2).standard_normal((200_000, 5))
    hit = np.abs(x.mean(1) - 0.7) <= stats.t.ppf(0.975, 4) * x.std(1, ddof=1) / np.sqrt(5)
    assert abs(hit.mean() - b["no_atom_coverage"]) < 4 * hit.std() / np.sqrt(len(hit))
    assert abs(b["upper"] - (1 - b["p_none"] * (1 - b["no_atom_coverage"]))) < 1e-12
    q = F.quantile_lemma_coverage(19, 0.1)
    assert q["exact"] == 0.9 and q["lower"] <= q["exact"] <= q["upper"]
    # split conformal's coverage is exactly k/(n+1)
    n, hits = 30, 0
    for _ in range(20000):
        s = r.standard_normal(n + 1)
        thr = np.sort(s[:n])[F.quantile_lemma_coverage(n, 0.1)["k"] - 1]
        hits += s[n] <= thr
    assert abs(hits / 20000 - F.quantile_lemma_coverage(n, 0.1)["exact"]) < 0.01


def test_full_conformal_and_jackknife_plus():
    r = rng(2)
    cov = 0
    for _ in range(150):
        X = r.standard_normal((30, 3))
        b = np.array([1.0, 0.5, 0.0])
        y = X @ b + r.standard_normal(30)
        x0 = r.standard_normal(3)
        y0 = x0 @ b + r.standard_normal()
        fc = F.full_conformal_ridge(X, y, x0, 1.0, 0.2, grid=np.linspace(-8, 8, 641))
        cov += fc["lo"] <= y0 <= fc["hi"]
    assert cov / 150 > 0.7
    n, p = 40, 40
    cj = cp = 0.0
    for _ in range(15):
        X = r.standard_normal((n, p)) / np.sqrt(p)
        bb = r.standard_normal(p)
        y = X @ bb + 0.5 * r.standard_normal(n)
        Xt = r.standard_normal((50, p)) / np.sqrt(p)
        yt = Xt @ bb + 0.5 * r.standard_normal(50)
        J = F.jackknife_intervals(F.min_norm_fit_predict, X, y, Xt, 0.1)
        cj += np.mean((J["jack_lo"] <= yt) & (yt <= J["jack_hi"]))
        cp += np.mean((J["plus_lo"] <= yt) & (yt <= J["plus_hi"]))
    assert cj / 15 < 0.75 and cp / 15 > 0.8  # the jackknife fails for an unstable fit; jackknife+ >= 1 - 2 alpha


def test_group_conditional_and_risk_control():
    r = rng(3)
    G = np.column_stack([np.ones(300), r.random(300) < 0.25]).astype(float)
    s = np.abs(r.standard_normal(300) * (1 + 2 * G[:, 1]))
    t1 = F.gcc_group_threshold(s, G, np.array([1.0, 1.0]), 0.1)
    t0 = F.gcc_group_threshold(s, G, np.array([1.0, 0.0]), 0.1)
    assert t1 > t0
    assert abs(t1 - np.quantile(s[G[:, 1] == 1], 0.9)) < 1.0
    # nonexchangeable weights: equal weights reduce to split conformal
    sc = r.standard_normal(99)
    assert abs(F.nexcp_threshold(sc, np.ones(99), 0.1) - np.sort(sc)[89]) < 1e-12
    # risk control: losses 1{y not in [-lam, lam]}
    lam = np.linspace(0, 4, 401)
    L = (np.abs(r.standard_normal(500))[:, None] > lam[None, :]).astype(float)
    lh = F.conformal_risk_control(L, lam, 0.1)
    test = np.abs(r.standard_normal(20000))
    assert np.mean(test > lh) <= 0.11
    p = F.outlier_pvalues(r.standard_normal(500), r.standard_normal(20000))
    assert np.mean(p <= 0.1) <= 0.11
