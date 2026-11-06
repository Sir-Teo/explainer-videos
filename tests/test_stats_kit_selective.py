"""Tests for statkit.selective, the inference-after-selection toolkit of Part 56."""

import math

import numpy as np
from scipy import stats

from explainer.stats.kit import selective as Z


def rng(seed=0):
    return np.random.default_rng(seed)


def test_truncated_normal_pivot():
    # untruncated: the ordinary normal survival function and interval
    assert abs(Z.truncnorm_sf(1.0, 0.0, 1.0, -np.inf, np.inf) - stats.norm.sf(1.0)) < 1e-12
    lo, hi = Z.truncnorm_interval(0.3, 1.0, -np.inf, np.inf)
    assert abs(lo - (0.3 - 1.959964)) < 1e-5 and abs(hi - (0.3 + 1.959964)) < 1e-5
    # truncated: matches scipy's truncnorm
    a, b, mu = 1.0, 3.0, 0.5
    ref = stats.truncnorm.sf(1.7, a - mu, b - mu, loc=mu)
    assert abs(Z.truncnorm_sf(1.7, mu, 1.0, a, b) - ref) < 1e-10
    # stable far in the tail
    assert 0 < Z.truncnorm_sf(40.2, 0.0, 1.0, 40.0, np.inf) < 1


def test_polyhedral_lemma_and_lasso_coverage():
    r = rng(1)
    n, p = 50, 10
    X = r.standard_normal((n, p))
    X /= np.linalg.norm(X, axis=0)
    beta = np.zeros(p)
    beta[:2] = 3.0
    y = X @ beta + r.standard_normal(n)
    ev = Z.lasso_event(X, y, 2.0)
    assert np.all(ev["A"] @ y <= ev["b"] + 1e-8)  # y lies in its own selection polyhedron
    lim = Z.polyhedral_limits(ev["A"], ev["b"], y, ev["pinv"][0])
    assert lim["lo"] <= lim["stat"] <= lim["hi"]
    cov = cnt = 0
    for _ in range(200):
        y = X @ beta + r.standard_normal(n)
        res = Z.lasso_selective_intervals(X, y, 2.0)
        if len(res["E"]) == 0:
            continue
        target = np.linalg.pinv(X[:, res["E"]]) @ (X @ beta)
        for k, iv in enumerate(res["intervals"]):
            cnt += 1
            cov += iv["lo"] <= target[k] <= iv["hi"]
    assert abs(cov / cnt - 0.95) < 0.035


def test_winners_posi_and_carving():
    r = rng(2)
    K = 10
    mu = np.zeros(K)
    mu[0] = 1.0
    cc = cn = ch = 0
    for _ in range(600):
        y = mu + r.standard_normal(K)
        w = Z.winner_conditional(y)
        h = Z.winner_hybrid(y)
        j = w["j"]
        cc += w["lo"] <= mu[j] <= w["hi"]
        cn += w["naive"][0] <= mu[j] <= w["naive"][1]
        ch += h["lo"] <= mu[j] <= h["hi"]
        assert h["hi"] - h["lo"] <= h["projection"][1] - h["projection"][0] + 1e-9
    assert cn / 600 < 0.86 and abs(cc / 600 - 0.95) < 0.03 and ch / 600 > 0.92
    X = r.standard_normal((30, 4))
    pc = Z.posi_constant(X, r, reps=4000)
    assert pc["z"] < pc["K"] < pc["bonferroni"]
    hard = Z.threshold_selective(2.2, 2.0, gamma=0.0)
    soft = Z.threshold_selective(2.2, 2.0, gamma=1.0)
    assert soft["hi"] - soft["lo"] < hard["hi"] - hard["lo"]


def test_fission_thinning_conformal_clustering():
    r = rng(3)
    x = r.normal(2.0, 1.0, 200000)
    f, g = Z.fission_normal(x, 1.0, 1.0, r)
    assert abs(np.corrcoef(f, g)[0, 1]) < 0.01 and abs(f.var() - 2) < 0.05 and abs(g.var() - 2) < 0.05
    xp = r.poisson(6.0, 200000)
    a, b = Z.thin_poisson(xp, 0.3, r)
    assert abs(np.corrcoef(a, b)[0, 1]) < 0.01 and abs(a.mean() - 1.8) < 0.02
    # conformal selection controls the FDR
    fdp = []
    for _ in range(100):
        xc, xt = r.standard_normal(500), r.standard_normal(200)
        yc, yt = xc + r.standard_normal(500), xt + r.standard_normal(200)
        out = Z.conformal_selection(xc, yc, xt, c=1.0, q=0.2)
        s = out["selected"]
        fdp.append(np.sum(s & (yt <= 1.0)) / max(1, s.sum()))
    assert np.mean(fdp) < 0.22
    # post-clustering p-values are uniform under the null; naive ones are not
    ps = [Z.clustering_pvalues(r.normal(0, 1, 30), grid=601) for _ in range(150)]
    sel = np.array([q["selective"] for q in ps])
    naive = np.array([q["naive"] for q in ps])
    assert np.mean(naive < 0.05) > 0.9 and abs(np.mean(sel < 0.2) - 0.2) < 0.08
