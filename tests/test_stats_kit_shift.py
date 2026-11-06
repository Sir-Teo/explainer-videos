"""statkit.shift (Part 60): depth, robust means, list decoding, median of means, covariate and label shift, DRO,
invariance, transfer and shift detection."""

import math

import numpy as np

from explainer.stats.kit import shift as H


def test_depth_and_robust_means():
    rng = np.random.default_rng(1)
    X = rng.standard_normal((400, 2))
    D = H.tukey_depth_2d(np.array([[0.0, 0.0], [5.0, 5.0]]), X)
    assert D[0] > 0.4 and D[1] == 0.0
    tm = H.tukey_median_2d(X, grid=30)
    assert np.linalg.norm(tm["median"]) < 0.25
    # with 10% planted at (6, 6), the mean moves far, the Tukey median barely
    Xc = np.vstack([X, np.full((44, 2), 6.0) + 0.05 * rng.standard_normal((44, 2))])
    assert np.linalg.norm(Xc.mean(0)) > 0.6
    assert np.linalg.norm(H.tukey_median_2d(Xc, grid=30)["median"]) < 0.4
    # in d = 100: mean and coordinatewise median grow like eps sqrt(d); the filter stays near the oracle
    e = H.robust_mean_errors(2000, 100, 0.1, rng)
    assert e["mean"] > 1.8 and e["coord_median"] > 1.0
    assert e["filter"] < 1.6 * e["oracle"] + 0.05
    assert e["removed_bad"] > 0.95 and e["removed_good"] < 0.1
    # Weiszfeld: the geometric median of collinear points is their median
    g = H.geometric_median(np.array([[0.0, 0], [1, 0], [5, 0]]))
    assert np.allclose(g, [1, 0], atol=1e-4)


def test_list_decoding_and_median_of_means():
    rng = np.random.default_rng(2)
    inl = rng.standard_normal((90, 2)) * 0.6 + 1.0
    outs = [rng.standard_normal((70, 2)) * 0.5 + c for c in ([-3, 2], [3.5, -2.5], [-2, -3])]
    L = H.list_decode(np.vstack([inl] + outs), 0.3, rng)
    assert len(L) == 4 and np.min(np.linalg.norm(L - 1.0, axis=1)) < 0.3
    # median of means under heavy tails: its 99th percentile error beats the mean's
    em, eg = [], []
    for _ in range(200):
        X = rng.standard_t(2.5, (600, 10))
        em.append(np.linalg.norm(X.mean(0)))
        eg.append(np.linalg.norm(H.median_of_means(X, 30, rng)))
    assert np.quantile(eg, 0.99) < np.quantile(em, 0.99)


def test_covariate_shift_weights():
    rng = np.random.default_rng(3)
    # source N(0, 1), target N(1, 1): the true ratio is exp(x - 1/2), linear in the logit
    xs, xt = rng.standard_normal(4000), rng.standard_normal(4000) + 1.0
    w = H.logistic_density_ratio(xs[:, None], xt[:, None])
    grid = np.array([[-1.0], [0.0], [1.0], [2.0]])
    assert np.allclose(np.log(w(grid)), grid[:, 0] - 0.5, atol=0.12)
    # the weighted mean of y = x recovers the target mean 1
    r = H.weighted_mean_ci(xs, w(xs[:, None]))
    assert abs(r["mean"] - 1.0) < 0.1 and r["lo"] < 1.0 < r["hi"]
    assert H.kish_ess(np.ones(10)) == 10 and abs(H.kish_ess([1, 1, 2]) - 16 / 6) < 1e-12


def test_label_shift_bbse_and_em():
    rng = np.random.default_rng(4)
    # a noisy classifier: TPR 0.8, FPR 0.2; source prevalence 0.3, target 0.7
    def draw(n, q):
        y = (rng.random(n) < q).astype(int)
        pred = np.where(y == 1, rng.random(n) < 0.8, rng.random(n) < 0.2).astype(int)
        return y, pred
    ys, ps = draw(20000, 0.3)
    yt, pt = draw(20000, 0.7)
    cc = pt.mean()
    assert abs(cc - (0.7 * 0.8 + 0.3 * 0.2)) < 0.01  # classify and count is attenuated
    b = H.bbse_weights(ps, ys, pt, 2)
    assert abs(b["q"][1] - 0.7) < 0.02
    # two classes: BBSE is Forman's adjusted count
    tpr = ps[ys == 1].mean()
    fpr = ps[ys == 0].mean()
    assert abs(b["q"][1] - (cc - fpr) / (tpr - fpr)) < 0.01
    # EM with calibrated posteriors from the source model
    lik1 = np.where(pt == 1, 0.8, 0.2)
    lik0 = np.where(pt == 1, 0.2, 0.8)
    post1 = 0.3 * lik1 / (0.3 * lik1 + 0.7 * lik0)
    e = H.em_label_shift(np.column_stack([1 - post1, post1]), np.array([0.7, 0.3]))
    assert abs(e["q"][1] - 0.7) < 0.02


def test_dro_duality():
    rng = np.random.default_rng(5)
    l = rng.exponential(1.0, 500)
    # small rho: the chi-square worst case is mean + sqrt(2 rho var)
    for rho in (0.001, 0.01):
        assert abs(H.dro_chi2(l, rho) - (l.mean() + math.sqrt(2 * rho * l.var()))) < 1e-9
    # both are monotone, start at the mean, and never exceed the largest loss
    for f in (H.dro_chi2, H.dro_kl):
        v = [f(l, r) for r in (0.0, 0.1, 0.5, 2.0)]
        assert abs(v[0] - l.mean()) < 0.02 and all(a <= b + 1e-8 for a, b in zip(v, v[1:])) and v[-1] <= l.max() + 1e-8
    # KL: the dual equals the primal's exponential tilt at the optimal temperature (check by brute force over tilts)
    rho = 0.2
    best = 0.0
    for t in np.linspace(0, 3, 3001):
        q = np.exp(t * (l - l.max()))
        q /= q.sum()
        if np.sum(q * np.log(q * len(l) + 1e-300)) <= rho:
            best = max(best, float(q @ l))
    assert abs(H.dro_kl(l, rho) - best) < 2e-3


def test_invariance_anchor_and_icp():
    rng = np.random.default_rng(6)
    n = 3000
    A = rng.standard_normal(n)
    Hh = rng.standard_normal(n)
    X = A + Hh + rng.standard_normal(n)
    Y = 2.0 * X + 3 * Hh + rng.standard_normal(n)
    X1 = np.column_stack([np.ones(n), X])
    A1 = np.column_stack([np.ones(n), A])
    ols = np.linalg.lstsq(X1, Y, rcond=None)[0]
    assert np.allclose(H.anchor_regression(X1, Y, A1, 1.0), ols)
    # gamma -> infinity: the IV estimator cov(A, Y)/cov(A, X)
    iv = np.cov(A, Y)[0, 1] / np.cov(A, X)[0, 1]
    assert abs(H.anchor_regression(X1, Y, A1, 1e8)[1] - iv) < 1e-3
    assert abs(iv - 2.0) < 0.15 and ols[1] > 2.5  # confounding biases OLS
    # ICP finds the parent and not the child
    Xs, ys, es = [], [], []
    for e, s in enumerate([0.0, 1.5, -1.5]):
        x1 = rng.normal(s, 1, 400)
        y = 1.5 * x1 + rng.standard_normal(400)
        x2 = y + rng.normal(s, 1, 400)
        Xs.append(np.column_stack([x1, x2]))
        ys.append(y)
        es.append(np.full(400, e))
    assert H.icp(np.vstack(Xs), np.concatenate(ys), np.concatenate(es))["estimate"] == [0]


def test_transfer_and_detection():
    rng = np.random.default_rng(7)
    p = 100
    b = np.zeros(p)
    b[:5] = 1.0
    w = b.copy()
    w[50:53] += 1.0  # a dissimilar source
    Xs = rng.standard_normal((800, p))
    ys = Xs @ w + rng.standard_normal(800)
    Xt = rng.standard_normal((120, p))
    yt = Xt @ b + rng.standard_normal(120)
    o = H.trans_lasso(Xs, ys, Xt, yt)
    err = {k: float(np.sum((v - b) ** 2)) for k, v in o.items()}
    assert err["transfer"] < err["pooled"] and err["transfer"] < err["target"]
    # MMD: exact-size permutation test; detects a mean shift, not a null
    X0, X1 = rng.standard_normal((150, 2)), rng.standard_normal((150, 2))
    assert H.mmd_test(X0, X1, rng, 200)["p"] > 0.01
    assert H.mmd_test(X0, X1 + 0.6, rng, 200)["p"] < 0.01
    assert abs(H.mmd2(X0, X0 + 0.0) + H.mmd2(X0, X0) - 2 * H.mmd2(X0, X0)) < 1e-12
