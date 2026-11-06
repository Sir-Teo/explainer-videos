"""statkit.conformal: prediction with guarantees (Part 34 of *Statistics, Built*).

Fast regression trees (cumulative-sum split search), random forests with in-bag counts, out-of-bag error, impurity and
permutation importance and Wager, Hastie & Efron's infinitesimal-jackknife variance; L2 boosting by stagewise
additive trees; calibration (reliability, ECE, Platt, isotonic, temperature); and conformal prediction: split
conformal, jackknife+ and CV+ (Barber, Candès, Ramdas & Tibshirani 2021), conformalized quantile regression (Romano,
Patterson & Candès 2019), weighted conformal under covariate shift (Tibshirani, Barber, Candès & Ramdas 2019),
adaptive conformal inference online (Gibbs & Candès 2021), adaptive prediction sets for classification (Romano,
Sesia & Candès 2020), Mondrian (group-conditional) conformal and conformal p-values.  Checked in
``tests/test_stats_kit_conformal.py``.
"""

from __future__ import annotations

import math

import numpy as np

# ------------------------------------------------------------------------------------------------------------- trees


class Tree:
    """A regression tree stored as arrays (feature, threshold, left, right, value); leaves have feature -1."""

    def __init__(self):
        self.feature, self.threshold, self.left, self.right, self.value = [], [], [], [], []
        self.gain = None

    def _new(self, value):
        self.feature.append(-1)
        self.threshold.append(0.0)
        self.left.append(-1)
        self.right.append(-1)
        self.value.append(value)
        return len(self.value) - 1

    def finalize(self, p):
        self.feature = np.array(self.feature)
        self.threshold = np.array(self.threshold)
        self.left = np.array(self.left)
        self.right = np.array(self.right)
        self.value = np.array(self.value)
        return self

    def predict(self, X) -> np.ndarray:
        X = np.asarray(X, float)
        node = np.zeros(len(X), int)
        while True:
            f = self.feature[node]
            inner = f >= 0
            if not inner.any():
                break
            idx = np.flatnonzero(inner)
            go_left = X[idx, f[idx]] <= self.threshold[node[idx]]
            node[idx] = np.where(go_left, self.left[node[idx]], self.right[node[idx]])
        return self.value[node]


def fit_tree(X, y, max_depth: int = 30, min_leaf: int = 5, mtry: int | None = None, rng=None) -> Tree:
    """CART for squared error (Breiman et al. 1984): at each node, for ``mtry`` randomly chosen features (all if
    None), sort and scan every split with cumulative sums; split on the best.  Records each feature's total
    reduction in squared error (``gain``, the impurity importance)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    rng = rng or np.random.default_rng(0)
    t = Tree()
    gain = np.zeros(p)
    stack = [(np.arange(n), 0, t._new(float(y.mean())))]
    while stack:
        idx, depth, node = stack.pop()
        m = len(idx)
        if depth >= max_depth or m < 2 * min_leaf:
            continue
        yy = y[idx]
        tot = yy.sum()
        sse0 = float(((yy - yy.mean()) ** 2).sum())
        if sse0 <= 1e-12:
            continue
        feats = rng.choice(p, mtry, replace=False) if mtry and mtry < p else np.arange(p)
        best = (0.0, -1, 0.0)
        for j in feats:
            xj = X[idx, j]
            o = np.argsort(xj, kind="stable")
            xs, ys = xj[o], yy[o]
            cs = np.cumsum(ys)
            k = np.arange(1, m)
            sl = cs[:-1]
            red = sl ** 2 / k + (tot - sl) ** 2 / (m - k) - tot ** 2 / m  # decrease in SSE
            ok = (k >= min_leaf) & (m - k >= min_leaf) & (xs[:-1] < xs[1:])
            if not ok.any():
                continue
            red = np.where(ok, red, -np.inf)
            i = int(np.argmax(red))
            if red[i] > best[0]:
                best = (float(red[i]), int(j), float((xs[i] + xs[i + 1]) / 2))
        if best[1] < 0:
            continue
        r, j, thr = best
        gain[j] += r
        mask = X[idx, j] <= thr
        li, ri = idx[mask], idx[~mask]
        ln, rn = t._new(float(y[li].mean())), t._new(float(y[ri].mean()))
        t.feature[node], t.threshold[node], t.left[node], t.right[node] = j, thr, ln, rn
        stack.append((li, depth + 1, ln))
        stack.append((ri, depth + 1, rn))
    t.finalize(p)
    t.gain = gain
    return t


class Forest:
    """Breiman's (2001) random forest for regression: B trees on bootstrap samples with mtry features per split.
    Keeps the in-bag counts N[b, i] for out-of-bag predictions and the infinitesimal jackknife."""

    def __init__(self, X, y, B: int = 200, mtry: int | None = None, min_leaf: int = 5, rng=None, max_depth: int = 30,
                 subsample: int | None = None):
        X, y = np.asarray(X, float), np.asarray(y, float)
        n, p = X.shape
        rng = rng or np.random.default_rng(0)
        self.mtry = mtry or max(1, p // 3)
        self.subsample = subsample
        self.trees, self.N = [], np.zeros((B, n), int)
        for b in range(B):
            s = rng.choice(n, subsample, replace=False) if subsample else rng.integers(0, n, n)
            self.N[b] = np.bincount(s, minlength=n)
            self.trees.append(fit_tree(X[s], y[s], max_depth, min_leaf, self.mtry, rng))
        self.X, self.y = X, y

    def tree_preds(self, X) -> np.ndarray:
        return np.array([t.predict(X) for t in self.trees])

    def predict(self, X) -> np.ndarray:
        return self.tree_preds(X).mean(0)

    def oob(self) -> np.ndarray:
        P = self.tree_preds(self.X)
        out = self.N == 0
        return np.where(out.sum(0) > 0, (P * out).sum(0) / np.maximum(out.sum(0), 1), np.nan)

    def ij_variance(self, X) -> np.ndarray:
        """Wager, Hastie & Efron's (2014) bias-corrected infinitesimal jackknife: sum_i Cov_b(N_bi, t_b(x))^2 minus
        the Monte Carlo bias n Var(N) Var_b(t_b) / B (n/B^2 sum_b (t_b - mean)^2 for the bootstrap).  For forests on
        subsamples of size s without replacement, Wager & Athey's (2018) version, scaled by (n-1)/n (n/(n-s))^2."""
        T = self.tree_preds(X)
        B, n = self.N.shape
        Tc = T - T.mean(0)
        Nc = self.N - self.N.mean(0)
        cov = Nc.T @ Tc / B
        v = (cov ** 2).sum(0)
        if self.subsample:
            q = self.subsample / n
            v = v - n * q * (1 - q) * (Tc ** 2).sum(0) / B ** 2
            return np.maximum(v * (n - 1) / n * (n / (n - self.subsample)) ** 2, 0.0)
        return np.maximum(v - n / B ** 2 * (Tc ** 2).sum(0), 0.0)

    def impurity_importance(self) -> np.ndarray:
        g = np.sum([t.gain for t in self.trees], axis=0)
        return g / g.sum()

    def permutation_importance(self, X, y, rng=None, reps: int = 5) -> np.ndarray:
        rng = rng or np.random.default_rng(0)
        X, y = np.asarray(X, float), np.asarray(y, float)
        base = np.mean((self.predict(X) - y) ** 2)
        out = []
        for j in range(X.shape[1]):
            d = []
            for _ in range(reps):
                Xp = X.copy()
                Xp[:, j] = rng.permutation(Xp[:, j])
                d.append(np.mean((self.predict(Xp) - y) ** 2) - base)
            out.append(np.mean(d))
        return np.array(out)


def l2_boost(X, y, M: int = 300, nu: float = 0.1, depth: int = 2, min_leaf: int = 5, Xtest=None, ytest=None) -> dict:
    """Friedman's (2001) gradient boosting for squared error, as forward stagewise additive modelling (Friedman,
    Hastie & Tibshirani 2000): F_m = F_{m-1} + nu * tree fitted to the current residuals."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    F = np.full(len(y), y.mean())
    Ft = None if Xtest is None else np.full(len(Xtest), y.mean())
    trees, tr, te = [], [], []
    for _ in range(M):
        t = fit_tree(X, y - F, depth, min_leaf)
        F = F + nu * t.predict(X)
        trees.append(t)
        tr.append(float(np.mean((y - F) ** 2)))
        if Ft is not None:
            Ft = Ft + nu * t.predict(Xtest)
            te.append(float(np.mean((ytest - Ft) ** 2)))
    return {"trees": trees, "nu": nu, "f0": float(y.mean()), "train": np.array(tr), "test": np.array(te), "fit": F,
            "pred": Ft}


# ------------------------------------------------------------------------------------------------------------- calibration


def reliability(p, y, bins: int = 10) -> dict:
    """Mean predicted probability and observed frequency in equal-width bins; ECE = sum_b (n_b/n) |obs - pred|."""
    p, y = np.asarray(p, float), np.asarray(y, float)
    e = np.linspace(0, 1, bins + 1)
    k = np.clip(np.digitize(p, e[1:-1]), 0, bins - 1)
    pred, obs, cnt = np.zeros(bins), np.zeros(bins), np.zeros(bins, int)
    for b in range(bins):
        m = k == b
        cnt[b] = m.sum()
        if cnt[b]:
            pred[b], obs[b] = p[m].mean(), y[m].mean()
    ece = float(np.sum(cnt / len(p) * np.abs(obs - pred)))
    return {"pred": pred, "obs": obs, "n": cnt, "ece": ece}


def platt(score, y, iters: int = 100) -> tuple:
    """Platt (1999) scaling: logistic regression of the label on the raw score; returns (a, b) with
    p = 1/(1 + exp(-(a + b s)))."""
    s, y = np.asarray(score, float), np.asarray(y, float)
    w = np.zeros(2)
    Z = np.column_stack([np.ones(len(s)), s])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-Z @ w))
        g = Z.T @ (y - p)
        H = Z.T @ (Z * (p * (1 - p))[:, None]) + 1e-9 * np.eye(2)
        step = np.linalg.solve(H, g)
        w += step
        if np.max(np.abs(step)) < 1e-10:
            break
    return float(w[0]), float(w[1])


def isotonic(score, y) -> tuple:
    """Isotonic calibration (Zadrozny & Elkan 2002): the pool-adjacent-violators fit of y on the sorted score.
    Returns (sorted scores, fitted values) for interpolation."""
    s, y = np.asarray(score, float), np.asarray(y, float)
    o = np.argsort(s)
    vals = list(y[o].astype(float))
    wts = [1.0] * len(vals)
    blocks = [[v, w, 1] for v, w in zip(vals, wts)]
    out = []
    for b in blocks:
        out.append(b)
        while len(out) > 1 and out[-2][0] > out[-1][0]:
            v2, w2, c2 = out.pop()
            v1, w1, c1 = out.pop()
            out.append([(v1 * w1 + v2 * w2) / (w1 + w2), w1 + w2, c1 + c2])
    fit = np.concatenate([[v] * c for v, w, c in out])
    return s[o], fit


def temperature(logit, y, grid=None) -> float:
    """Guo et al.'s (2017) temperature scaling: the T minimizing the log loss of sigmoid(logit / T)."""
    z, y = np.asarray(logit, float), np.asarray(y, float)
    grid = np.exp(np.linspace(-3, 4, 1401)) if grid is None else grid
    best, bt = np.inf, 1.0
    for T in grid:
        p = 1 / (1 + np.exp(-z / T))
        p = np.clip(p, 1e-12, 1 - 1e-12)
        ll = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
        if ll < best:
            best, bt = ll, float(T)
    return bt


# ------------------------------------------------------------------------------------------------------------- conformal


def conformal_quantile(scores, alpha: float) -> float:
    """The ceil((n + 1)(1 - alpha))-th smallest of n calibration scores (+inf if that exceeds n): the quantile lemma's
    threshold, giving coverage at least 1 - alpha for an exchangeable test point."""
    s = np.sort(np.asarray(scores, float))
    n = len(s)
    k = math.ceil((n + 1) * (1 - alpha))
    return float(s[k - 1]) if k <= n else float("inf")


def split_conformal(pred_cal, y_cal, pred_test, alpha: float = 0.1) -> dict:
    """Split conformal with absolute residuals (Papadopoulos et al. 2002; Lei et al. 2018)."""
    r = np.abs(np.asarray(y_cal, float) - np.asarray(pred_cal, float))
    q = conformal_quantile(r, alpha)
    pt = np.asarray(pred_test, float)
    return {"lo": pt - q, "hi": pt + q, "q": q}


def jackknife_plus(fit_predict, X, y, Xtest, alpha: float = 0.1, K: int | None = None, rng=None) -> dict:
    """Jackknife+ (K = None: leave-one-out) or CV+ (K folds) of Barber et al. (2021).  ``fit_predict(Xtr, ytr, Xev)``
    returns predictions at Xev.  Interval [q_lo{mu_{-i}(x) - R_i}, q_hi{mu_{-i}(x) + R_i}] with R_i the held-out
    residual of point i under the model that excluded it; coverage >= 1 - 2 alpha always."""
    X, y, Xt = np.asarray(X, float), np.asarray(y, float), np.asarray(Xtest, float)
    n = len(y)
    rng = rng or np.random.default_rng(0)
    folds = np.arange(n) if K is None else rng.permutation(np.arange(n) % K)
    lo_parts, hi_parts = np.zeros((n, len(Xt))), np.zeros((n, len(Xt)))
    for f in np.unique(folds):
        te = folds == f
        both = fit_predict(X[~te], y[~te], np.vstack([X[te], Xt]))
        r = np.abs(y[te] - both[:te.sum()])
        mt = both[te.sum():]
        lo_parts[te] = mt[None, :] - r[:, None]
        hi_parts[te] = mt[None, :] + r[:, None]
    k = math.ceil((n + 1) * (1 - alpha))
    lo = -np.sort(-lo_parts, axis=0)[k - 1] if k <= n else np.full(len(Xt), -np.inf)
    hi = np.sort(hi_parts, axis=0)[k - 1] if k <= n else np.full(len(Xt), np.inf)
    return {"lo": lo, "hi": hi}


def cqr(lo_cal, hi_cal, y_cal, lo_test, hi_test, alpha: float = 0.1) -> dict:
    """Conformalized quantile regression (Romano, Patterson & Candès 2019): scores max(lo - y, y - hi) on the
    calibration set; the test band is [lo - q, hi + q]."""
    s = np.maximum(np.asarray(lo_cal) - np.asarray(y_cal), np.asarray(y_cal) - np.asarray(hi_cal))
    q = conformal_quantile(s, alpha)
    return {"lo": np.asarray(lo_test) - q, "hi": np.asarray(hi_test) + q, "q": q}


def weighted_quantile_conformal(scores, w_cal, w_test: float, alpha: float = 0.1) -> float:
    """Tibshirani et al. (2019): under covariate shift with likelihood ratio w(x), the (1 - alpha) quantile of the
    calibration scores weighted by w(X_i), with the test point's weight w(x) placed at +inf."""
    s, w = np.asarray(scores, float), np.asarray(w_cal, float)
    o = np.argsort(s)
    s, w = s[o], w[o]
    tot = w.sum() + w_test
    cw = np.cumsum(w) / tot
    i = np.searchsorted(cw, 1 - alpha)
    return float(s[i]) if i < len(s) else float("inf")


def aci(scores, alpha: float = 0.1, gamma: float = 0.005, window: int = 200, warm: int = 50) -> dict:
    """Adaptive conformal inference (Gibbs & Candès 2021) on a stream of nonconformity scores: at time t, predict with
    the 1 - alpha_t quantile of the last ``window`` scores, then update alpha_{t+1} = alpha_t + gamma (alpha - err_t)."""
    s = np.asarray(scores, float)
    a = alpha
    thr, err, alphas = [], [], []
    for t in range(warm, len(s)):
        past = s[max(0, t - window):t]
        q = np.inf if a <= 0 else (np.quantile(past, min(1.0, max(0.0, 1 - a))) if a < 1 else -np.inf)
        e = float(s[t] > q)
        thr.append(q)
        err.append(e)
        alphas.append(a)
        a = a + gamma * (alpha - e)
    return {"threshold": np.array(thr), "err": np.array(err), "alpha_t": np.array(alphas)}


def aps_scores(probs, y, rng, randomized: bool = True) -> np.ndarray:
    """Adaptive prediction sets (Romano, Sesia & Candès 2020): the total probability of the classes ranked at or
    above the true one, with the true class's own mass randomized by U."""
    P = np.asarray(probs, float)
    out = np.empty(len(P))
    for i, (pr, yi) in enumerate(zip(P, y)):
        o = np.argsort(-pr)
        cs = np.cumsum(pr[o])
        r = int(np.flatnonzero(o == yi)[0])
        u = rng.random() if randomized else 1.0
        out[i] = cs[r] - (1 - u) * pr[o][r]
    return out


def aps_sets(probs, q: float, rng, randomized: bool = True) -> list:
    """The APS prediction set at threshold q for each row of probabilities."""
    P = np.asarray(probs, float)
    sets = []
    for pr in P:
        o = np.argsort(-pr)
        cs = np.cumsum(pr[o])
        u = rng.random() if randomized else 1.0
        keep = [o[k] for k in range(len(o)) if cs[k] - (1 - u) * pr[o][k] <= q]
        sets.append(keep if keep else [])
    return sets


def mondrian_quantiles(scores, groups, alpha: float = 0.1) -> dict:
    """Group-conditional (Mondrian) conformal: a separate conformal quantile in each group (Vovk et al. 2005)."""
    s, g = np.asarray(scores, float), np.asarray(groups)
    return {k: conformal_quantile(s[g == k], alpha) for k in np.unique(g)}


def conformal_pvalue(scores_cal, score_test, rng=None) -> float:
    """The (smoothed) conformal p-value: (#{cal >= test} + U (1 + #{cal == test})) / (n + 1); uniform under
    exchangeability (Vovk et al. 2005; Bates et al. 2023 for outlier detection)."""
    s = np.asarray(scores_cal, float)
    u = 1.0 if rng is None else rng.random()
    return float((np.sum(s > score_test) + u * (1 + np.sum(s == score_test))) / (len(s) + 1))
