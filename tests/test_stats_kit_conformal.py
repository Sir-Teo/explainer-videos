import math

import numpy as np
import pytest

from explainer.stats import museum
from explainer.stats.kit import conformal as CF
from explainer.stats.kit import ppi as PPI


def _friedman(n, rng):
    X = rng.uniform(size=(n, 5))
    y = 10 * np.sin(np.pi * X[:, 0] * X[:, 1]) + 20 * (X[:, 2] - 0.5) ** 2 + 10 * X[:, 3] + 5 * X[:, 4] + rng.standard_normal(n)
    return X, y


def test_tree_and_forest():
    rng = np.random.default_rng(0)
    X, y = _friedman(400, rng)
    t = CF.fit_tree(X, y, max_depth=3, min_leaf=5)
    assert len(np.unique(t.predict(X))) <= 8
    Xt, yt = _friedman(500, rng)
    f = CF.Forest(X, y, B=60, rng=rng)
    mse = np.mean((f.predict(Xt) - yt) ** 2)
    assert mse < 0.5 * np.var(yt)
    oob = f.oob()
    assert np.mean((oob - y) ** 2) < 0.6 * np.var(y)
    v = f.ij_variance(Xt[:20])
    assert np.all(v >= 0) and np.all(np.isfinite(v))
    imp = f.permutation_importance(Xt, yt, rng, reps=2)
    assert imp[3] > imp[4] > 0  # 10 x4 matters more than 5 x5
    # a subsampled forest: each tree sees 80 distinct cases; its IJ variance is finite and positive somewhere
    fs = CF.Forest(X, y, B=80, rng=rng, subsample=80)
    assert fs.N.max() == 1 and np.all(fs.N.sum(1) == 80)
    vs = fs.ij_variance(Xt[:20])
    assert np.all(vs >= 0) and np.all(np.isfinite(vs)) and vs.max() > 0


def test_boost_reduces_error():
    rng = np.random.default_rng(1)
    X, y = _friedman(300, rng)
    Xt, yt = _friedman(300, rng)
    b = CF.l2_boost(X, y, M=150, nu=0.1, depth=2, Xtest=Xt, ytest=yt)
    assert b["train"][-1] < b["train"][0] and b["test"][-1] < 0.5 * np.var(yt)


def test_calibration_tools():
    rng = np.random.default_rng(2)
    s = rng.normal(size=4000)
    y = (rng.random(4000) < 1 / (1 + np.exp(-2 * s))).astype(float)
    a, b = CF.platt(s, y)
    assert abs(b - 2) < 0.2 and abs(a) < 0.15
    T = CF.temperature(4 * s, y)
    assert abs(T - 2) < 0.25
    xs, fit = CF.isotonic(s, y)
    assert np.all(np.diff(fit) >= -1e-12)
    r = CF.reliability(1 / (1 + np.exp(-2 * s)), y)
    assert r["ece"] < 0.05


def test_split_conformal_coverage_bounds():
    rng = np.random.default_rng(3)
    n, alpha = 99, 0.1
    cov = []
    for _ in range(3000):
        r = np.abs(rng.standard_t(3, n + 1))
        q = CF.conformal_quantile(r[:n], alpha)
        cov.append(r[n] <= q)
    c = np.mean(cov)
    assert 0.9 - 0.015 < c < 0.9 + 1 / (n + 1) + 0.015
    assert CF.conformal_quantile([1, 2, 3], 0.1) == math.inf


def test_jackknife_plus_cqr_weighted_aps():
    rng = np.random.default_rng(4)
    X = rng.uniform(-1, 1, (150, 1))
    y = 2 * X[:, 0] + rng.standard_normal(150)
    Xt = np.array([[0.0], [0.5]])

    def fp(Xa, ya, Xe):
        Z = np.column_stack([np.ones(len(Xa)), Xa])
        b = np.linalg.lstsq(Z, ya, rcond=None)[0]
        return np.column_stack([np.ones(len(Xe)), Xe]) @ b

    jp = CF.jackknife_plus(fp, X, y, Xt, 0.1)
    assert np.all(jp["lo"] < jp["hi"]) and np.all(jp["hi"] - jp["lo"] < 5)
    cv = CF.jackknife_plus(fp, X, y, Xt, 0.1, K=10, rng=rng)
    assert np.all(cv["lo"] < cv["hi"])
    c = CF.cqr(np.full(50, -1.0), np.full(50, 1.0), rng.normal(0, 2, 50), np.array([-1.0]), np.array([1.0]), 0.1)
    assert c["q"] > 0
    assert CF.weighted_quantile_conformal([1, 2, 3, 4], [1, 1, 1, 1], 1.0, 0.5) == 3
    P = rng.dirichlet(np.ones(4), 200)
    yy = np.array([rng.choice(4, p=p) for p in P])
    s = CF.aps_scores(P, yy, rng)
    q = CF.conformal_quantile(s, 0.1)
    sets = CF.aps_sets(P[:5], q, rng)
    assert all(isinstance(x, list) for x in sets)
    a = CF.aci(rng.standard_normal(1000), 0.1)
    assert abs(a["err"].mean() - 0.1) < 0.03


def test_ppi_mean_and_ols():
    rng = np.random.default_rng(5)
    N, n = 20000, 300
    xu = rng.standard_normal(N)
    xl = rng.standard_normal(n)
    yl = 1 + 2 * xl + rng.standard_normal(n)
    fl, fu = 1.3 + 1.8 * xl, 1.3 + 1.8 * xu  # a biased predictor
    r = PPI.ppi_mean(yl, fl, fu, 0.1)
    c = PPI.classical_mean(yl, 0.1)
    assert r["se"] < c["se"] and r["lo"] < 1.3 < r["hi"] + 0.5
    rp = PPI.ppi_mean(yl, fl, fu, 0.1, lam=None)
    assert 0 <= rp["lam"] <= 1 and rp["se"] < c["se"]
    o = PPI.ppi_ols(xl[:, None], yl, fl, xu[:, None], fu, 0.1)
    assert abs(o["beta"][1] - 2) < 0.4


def test_breast_cancer_data():
    X, y, names = museum.breast_cancer()
    assert X.shape == (569, 30) and y.sum() == 212 and names[0] == "mean_radius"


def test_score_ladder_rank_and_threshold():
    from explainer.stats.viz import ScoreLadder

    s = np.arange(1, 20, dtype=float)  # 19 scores, alpha = 0.1: k = ceil(20 * 0.9) = 18
    lad = ScoreLadder(s, alpha=0.1)
    assert lad.kq == 18 and lad.q == 18.0
    assert lad.q == CF.conformal_quantile(s, 0.1)
    assert len(lad.bars) == 19 and len(lad.ranks) == 19
    assert len(lad.kept()) == 18
    assert lad.rank_of(0.5) == 0 and lad.rank_of(18.5) == 18 and lad.rank_of(100) == 19
    # with too few scores the threshold is infinite (the whole line)
    small = ScoreLadder([1.0, 2.0, 3.0], alpha=0.1)
    assert small.kq == 4 and not np.isfinite(small.q)
    assert small.threshold() is not None
