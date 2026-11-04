"""Credit (Part 20): default as an option on the firm, default as a random clock, the CDS, default prediction from
accounts, the large pool behind bank capital, and copulas for baskets and tranches.

Structural: Merton (1974) prices equity as a call on the firm's assets and solves backwards from the equity's price
and volatility for the assets'; KMV's distance to default and its iterative estimate from a price history
(Crosbie and Bohn 2003; Vassalou and Xing 2004; Bharath and Shumway 2008); Black and Cox (1976) first passage.

Reduced form: a hazard rate makes survival a discount factor (Jarrow and Turnbull 1995; Duffie and Singleton 1999);
the CDS's two legs, the par spread, the bootstrap of a hazard curve and the upfront for a standard coupon (the 2009
Big Bang); the credit triangle.

Prediction: Altman's Z (1968); a logit fitted by Newton's method (Shumway 2001); gradient-boosted trees on
histogram splits with Newton leaves (Friedman 2001; Chen and Guestrin 2016); AUC, the accuracy ratio and the Brier
score.

Portfolios: Vasicek's large homogeneous pool (2002) and the Basel IRB capital formula (Gordy 2003); the one-factor
Gaussian and t copulas (Li 2000), tranche losses, expected tranche loss in the large pool, and base correlation.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq, fsolve
from scipy.stats import norm
from scipy.stats import t as student_t


# ---------------------------------------------------------------------------
# Structural models
# ---------------------------------------------------------------------------
def merton_equity(V, sigma_V, D, r, T):
    """Equity as a European call on the assets V with strike the face of debt D due at T: returns (E, N(d1))."""
    V, s = np.asarray(V, float), np.asarray(sigma_V, float)
    d1 = (np.log(V / D) + (r + 0.5 * s ** 2) * T) / (s * np.sqrt(T))
    d2 = d1 - s * np.sqrt(T)
    return V * norm.cdf(d1) - D * np.exp(-r * T) * norm.cdf(d2), norm.cdf(d1)


def merton_solve(E, sigma_E, D, r, T):
    """The assets' value and volatility implied by the equity's: E = C(V, sigma_V) and sigma_E E = N(d1) sigma_V V,
    solved in logs.  Returns (V, sigma_V)."""
    def f(z):
        V, s = np.exp(z)
        e, delta = merton_equity(V, s, D, r, T)
        return [np.log(e / E), np.log(delta * s * V / (sigma_E * E))]
    V0 = E + D * np.exp(-r * T)
    z = fsolve(f, [np.log(V0), np.log(max(sigma_E * E / V0, 1e-3))], xtol=1e-12)
    return float(np.exp(z[0])), float(np.exp(z[1]))


def distance_to_default(V, sigma_V, D, mu, T=1.0):
    """How many standard deviations the assets are expected to be above the default point at T."""
    return (np.log(np.asarray(V, float) / D) + (mu - 0.5 * sigma_V ** 2) * T) / (sigma_V * np.sqrt(T))


def merton_pd(V, sigma_V, D, mu, T=1.0):
    return norm.cdf(-distance_to_default(V, sigma_V, D, mu, T))


def merton_spread(V, sigma_V, D, r, T):
    """The risky debt's yield over r: debt = V - E, yield = -ln(debt / D) / T."""
    E, _ = merton_equity(V, sigma_V, D, r, T)
    B = np.asarray(V, float) - E
    return -np.log(B / D) / T - r


def kmv_iterate(E, D, r, T=1.0, dt=1 / 252, n_iter=50, tol=1e-6):
    """The iterative estimate: guess sigma_V, invert the call day by day for V_t from the equity value E_t, re-estimate
    sigma_V (and mu) from the log changes of V, repeat.  E and D are arrays over days (D may be constant).  Returns
    {V, sigma_V, mu, dtd}: the asset path and the one-year distance to default each day."""
    E = np.asarray(E, float)
    D = np.broadcast_to(np.asarray(D, float), E.shape)
    lr = np.diff(np.log(E))
    s = float(np.std(lr) / np.sqrt(dt) * np.mean(E / (E + D)))
    for _ in range(n_iter):
        V = np.empty_like(E)
        for i, (e, d) in enumerate(zip(E, D)):
            V[i] = brentq(lambda v: merton_equity(v, s, d, r, T)[0] - e, e, e + d * 1.5 + 1e-9)
        lv = np.diff(np.log(V))
        s_new = float(np.std(lv) / np.sqrt(dt))
        if abs(s_new - s) < tol:
            s = s_new
            break
        s = s_new
    mu = float(np.mean(lv) / dt + 0.5 * s ** 2)
    return {"V": V, "sigma_V": s, "mu": mu, "dtd": distance_to_default(V, s, D, mu, T)}


def black_cox_pd(V, sigma_V, mu, K, T):
    """Probability that GBM assets touch the barrier K before T (Black and Cox 1976): first passage, not only the
    terminal value."""
    m = mu - 0.5 * sigma_V ** 2
    s = sigma_V * np.sqrt(T)
    x = np.log(K / np.asarray(V, float))
    return norm.cdf((x - m * T) / s) + np.exp(2 * m * x / sigma_V ** 2) * norm.cdf((x + m * T) / s)


# ---------------------------------------------------------------------------
# Reduced form: hazards, risky bonds and the CDS
# ---------------------------------------------------------------------------
def survival(t, knots, hazards):
    """Q(t) = exp(-int_0^t lambda) for a piecewise-flat hazard: ``hazards[i]`` applies on (knots[i-1], knots[i]]
    (knots[-1] extends flat beyond)."""
    t = np.asarray(t, float)
    knots, hazards = np.asarray(knots, float), np.asarray(hazards, float)
    edges = np.r_[0.0, knots]
    out = np.zeros_like(t)
    for i, h in enumerate(hazards):
        lo, hi = edges[i], (edges[i + 1] if i < len(hazards) - 1 else np.inf)
        out += h * np.clip(np.minimum(t, hi) - lo, 0, None)
    return np.exp(-out)


def risky_zero(T, df, Q, R=0.4, convention="RMV"):
    """A defaultable zero paying 1 at T. Recovery of market value (Duffie and Singleton): P(T) Q(T)^(1-R) under a
    flat-hazard approximation, i.e. discount at r + (1 - R) lambda.  Recovery of face, paid at T: P(T)[Q(T) + R(1 -
    Q(T))]."""
    if convention == "RMV":
        return df * Q ** (1 - R)
    return df * (Q + R * (1 - Q))


def cds_legs(T, knots, hazards, df, R=0.4, freq=4, n_sub=12):
    """The two legs of a CDS maturing at T, per unit notional: the risky annuity (premium leg per unit spread,
    including the accrued premium paid on default) and the protection leg (1 - R paid at default), integrated on
    ``n_sub`` steps per period.  ``df`` is a function of time."""
    pay = np.arange(1, int(round(T * freq)) + 1) / freq
    prev = np.r_[0.0, pay[:-1]]
    Qp, Qprev = survival(pay, knots, hazards), survival(prev, knots, hazards)
    d = 1 / freq
    rpv01 = float(np.sum(d * df(pay) * Qp) + np.sum(0.5 * d * df(pay) * (Qprev - Qp)))
    g = np.linspace(0, T, int(round(T * freq * n_sub)) + 1)
    Qg = survival(g, knots, hazards)
    mid = 0.5 * (g[1:] + g[:-1])
    prot = float((1 - R) * np.sum(df(mid) * (Qg[:-1] - Qg[1:])))
    return rpv01, prot


def cds_par_spread(T, knots, hazards, df, R=0.4, freq=4):
    a, p = cds_legs(T, knots, hazards, df, R, freq)
    return p / a


def bootstrap_hazard(tenors, spreads, df, R=0.4, freq=4):
    """Piecewise-flat hazards that reprice each quoted par spread in turn, shortest first."""
    knots, hz = [], []
    for T, s in zip(tenors, spreads):
        knots.append(float(T))

        def f(h):
            return cds_par_spread(T, knots, hz + [h], df, R, freq) - s
        hz.append(brentq(f, 1e-8, 5.0, xtol=1e-14))
    return np.array(knots), np.array(hz)


def cds_upfront(coupon, T, knots, hazards, df, R=0.4, freq=4):
    """Since the 2009 Big Bang, CDS trade with a standard coupon (100 or 500 bp) and an upfront payment that settles
    the difference: protection leg minus coupon times the risky annuity, per unit notional (positive: buyer pays)."""
    a, p = cds_legs(T, knots, hazards, df, R, freq)
    return p - coupon * a


def credit_triangle(spread, R=0.4):
    """Spread = hazard x loss given default: lambda = s / (1 - R)."""
    return spread / (1 - R)


# ---------------------------------------------------------------------------
# Default prediction
# ---------------------------------------------------------------------------
ALTMAN_1968 = np.array([1.2, 1.4, 3.3, 0.6, 1.0])  # WC/TA, RE/TA, EBIT/TA, ME/TL, Sales/TA


def altman_z(X):
    """Altman's Z from the five ratios (columns: WC/TA, RE/TA, EBIT/TA, ME/TL, Sales/TA): below 1.81 distress, above
    2.99 safe (the 1968 zones)."""
    return np.asarray(X, float) @ ALTMAN_1968


def logit_fit(X, y, l2=1e-6, n_iter=100, tol=1e-10):
    """A logistic regression with intercept by Newton's method (IRLS) with a small ridge; returns beta (intercept
    first)."""
    X = np.c_[np.ones(len(X)), np.asarray(X, float)]
    y = np.asarray(y, float)
    b = np.zeros(X.shape[1])
    b[0] = np.log(max(y.mean(), 1e-9) / max(1 - y.mean(), 1e-9))
    I = np.eye(X.shape[1]) * l2
    I[0, 0] = 0
    for _ in range(n_iter):
        p = 1 / (1 + np.exp(-np.clip(X @ b, -35, 35)))
        g = X.T @ (p - y) + I @ b
        H = (X * (p * (1 - p))[:, None]).T @ X + I
        step = np.linalg.solve(H, g)
        b -= step
        if np.max(np.abs(step)) < tol:
            break
    return b


def logit_predict(b, X):
    return 1 / (1 + np.exp(-np.clip(b[0] + np.asarray(X, float) @ b[1:], -35, 35)))


class GBM:
    """Gradient-boosted trees for a binary target (log loss): each tree is grown depth-first on histogram bins of the
    features, splits by the second-order gain, leaves by a Newton step with an L2 penalty; rows and features may be
    subsampled.  Small, plain and deterministic for a seed."""

    def __init__(self, n_trees=300, depth=3, lr=0.05, min_leaf=20, lam=1.0, n_bins=32, subsample=0.8, colsample=1.0,
                 seed=0):
        self.n_trees, self.depth, self.lr, self.min_leaf, self.lam = n_trees, depth, lr, min_leaf, lam
        self.n_bins, self.subsample, self.colsample, self.seed = n_bins, subsample, colsample, seed

    def _bin(self, X):
        return np.stack([np.searchsorted(self.edges[j], X[:, j], side="right") for j in range(X.shape[1])], 1)

    def fit(self, X, y, X_val=None, y_val=None, early_stop=None):
        X, y = np.asarray(X, float), np.asarray(y, float)
        rng = np.random.default_rng(self.seed)
        qs = np.linspace(0, 1, self.n_bins + 1)[1:-1]
        self.edges = [np.unique(np.nanquantile(X[:, j], qs)) for j in range(X.shape[1])]
        B = self._bin(X)
        self.base = float(np.log(max(y.mean(), 1e-9) / max(1 - y.mean(), 1e-9)))
        F = np.full(len(y), self.base)
        self.trees, self.val_loss = [], []
        Bv = self._bin(np.asarray(X_val, float)) if X_val is not None else None
        Fv = np.full(len(Bv), self.base) if Bv is not None else None
        best, best_n = np.inf, 0
        for m in range(self.n_trees):
            p = 1 / (1 + np.exp(-F))
            g, h = p - y, np.maximum(p * (1 - p), 1e-12)
            rows = np.where(rng.random(len(y)) < self.subsample)[0]
            cols = np.where(rng.random(X.shape[1]) < self.colsample)[0]
            if len(cols) == 0:
                cols = np.arange(X.shape[1])
            tree = self._grow(B, g, h, rows, cols, 0)
            self.trees.append(tree)
            F += self.lr * self._apply(tree, B)
            if Bv is not None:
                Fv += self.lr * self._apply(tree, Bv)
                pv = 1 / (1 + np.exp(-Fv))
                yv = np.asarray(y_val, float)
                ll = float(-np.mean(yv * np.log(pv + 1e-12) + (1 - yv) * np.log(1 - pv + 1e-12)))
                self.val_loss.append(ll)
                if ll < best:
                    best, best_n = ll, m + 1
                elif early_stop and m + 1 - best_n >= early_stop:
                    break
        if Bv is not None and early_stop:
            self.trees = self.trees[:best_n]
        return self

    def _grow(self, B, g, h, rows, cols, d):
        G, H = g[rows].sum(), h[rows].sum()
        leaf = {"value": float(-G / (H + self.lam))}
        if d >= self.depth or len(rows) < 2 * self.min_leaf:
            return leaf
        best = (0.0, None, None)
        parent = G * G / (H + self.lam)
        for j in cols:
            b = B[rows, j]
            nb = len(self.edges[j]) + 1
            gs = np.bincount(b, weights=g[rows], minlength=nb)
            hs = np.bincount(b, weights=h[rows], minlength=nb)
            cnt = np.bincount(b, minlength=nb)
            gl, hl, cl = np.cumsum(gs)[:-1], np.cumsum(hs)[:-1], np.cumsum(cnt)[:-1]
            gr, hr, cr = G - gl, H - hl, len(rows) - cl
            ok = (cl >= self.min_leaf) & (cr >= self.min_leaf)
            if not ok.any():
                continue
            gain = np.where(ok, gl ** 2 / (hl + self.lam) + gr ** 2 / (hr + self.lam) - parent, -np.inf)
            k = int(np.argmax(gain))
            if gain[k] > best[0]:
                best = (float(gain[k]), int(j), k)
        if best[1] is None:
            return leaf
        j, k = best[1], best[2]
        left = rows[B[rows, j] <= k]
        right = rows[B[rows, j] > k]
        return {"feature": j, "bin": k, "gain": best[0], "left": self._grow(B, g, h, left, cols, d + 1),
                "right": self._grow(B, g, h, right, cols, d + 1)}

    def _apply(self, tree, B):
        out = np.empty(len(B))
        stack = [(tree, np.arange(len(B)))]
        while stack:
            node, idx = stack.pop()
            if "value" in node:
                out[idx] = node["value"]
                continue
            m = B[idx, node["feature"]] <= node["bin"]
            stack.append((node["left"], idx[m]))
            stack.append((node["right"], idx[~m]))
        return out

    def decision(self, X):
        B = self._bin(np.asarray(X, float))
        return self.base + self.lr * sum(self._apply(t, B) for t in self.trees)

    def predict_proba(self, X):
        return 1 / (1 + np.exp(-self.decision(X)))

    def importance(self, n_features):
        imp = np.zeros(n_features)

        def walk(n):
            if "value" in n:
                return
            imp[n["feature"]] += n["gain"]
            walk(n["left"])
            walk(n["right"])
        for t in self.trees:
            walk(t)
        return imp / max(imp.sum(), 1e-12)


def auc(y, score):
    """Area under the ROC curve by ranks (ties averaged): the chance a random defaulter scores above a random
    survivor.  The accuracy ratio (Gini) is 2 AUC - 1."""
    y, s = np.asarray(y, bool), np.asarray(score, float)
    order = np.argsort(s, kind="mergesort")
    ranks = np.empty(len(s))
    sorted_s = s[order]
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and sorted_s[j + 1] == sorted_s[i]:
            j += 1
        ranks[order[i:j + 1]] = 0.5 * (i + j) + 1
        i = j + 1
    n1, n0 = y.sum(), (~y).sum()
    return float((ranks[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def roc_curve(y, score):
    y, s = np.asarray(y, bool), np.asarray(score, float)
    o = np.argsort(-s)
    tp = np.r_[0, np.cumsum(y[o])] / max(y.sum(), 1)
    fp = np.r_[0, np.cumsum(~y[o])] / max((~y).sum(), 1)
    return fp, tp


def brier(y, p):
    return float(np.mean((np.asarray(p, float) - np.asarray(y, float)) ** 2))


# ---------------------------------------------------------------------------
# The large pool and bank capital
# ---------------------------------------------------------------------------
def vasicek_loss_cdf(x, pd, rho):
    """P(pool default fraction <= x) in the one-factor Gaussian large pool (Vasicek 2002)."""
    x = np.clip(np.asarray(x, float), 1e-12, 1 - 1e-12)
    return norm.cdf((np.sqrt(1 - rho) * norm.ppf(x) - norm.ppf(pd)) / np.sqrt(rho))


def vasicek_loss_pdf(x, pd, rho):
    x = np.clip(np.asarray(x, float), 1e-12, 1 - 1e-12)
    a = (np.sqrt(1 - rho) * norm.ppf(x) - norm.ppf(pd)) / np.sqrt(rho)
    return np.sqrt((1 - rho) / rho) * norm.pdf(a) / norm.pdf(norm.ppf(x))


def vasicek_quantile(q, pd, rho):
    """The default fraction not exceeded with probability q: the conditional PD at the q-th worst factor."""
    return norm.cdf((norm.ppf(pd) + np.sqrt(rho) * norm.ppf(q)) / np.sqrt(1 - rho))


def basel_corporate_rho(pd):
    w = (1 - np.exp(-50 * np.asarray(pd, float))) / (1 - np.exp(-50))
    return 0.12 * w + 0.24 * (1 - w)


def basel_irb_k(pd, lgd=0.45, M=2.5, rho=None):
    """Basel II/III IRB capital per unit exposure for corporates: the loss at the 99.9th percentile of the Vasicek
    factor less the expected loss, with the maturity adjustment.  Risk-weighted assets are 12.5 K per unit."""
    pd = np.maximum(np.asarray(pd, float), 0.0003)
    rho = basel_corporate_rho(pd) if rho is None else rho
    b = (0.11852 - 0.05478 * np.log(pd)) ** 2
    return (lgd * vasicek_quantile(0.999, pd, rho) - pd * lgd) * (1 + (M - 2.5) * b) / (1 - 1.5 * b)


# ---------------------------------------------------------------------------
# Copulas and tranches
# ---------------------------------------------------------------------------
def copula_defaults(n_names, pd, rho, n_sims, seed=0, nu=None):
    """Defaults over one horizon in the one-factor copula: X_i = sqrt(rho) M + sqrt(1 - rho) Z_i, default if X_i falls
    below the threshold that gives each name its pd.  ``nu`` switches to the t copula (all names share one
    chi-square mixing variable, which thickens the joint tail).  Returns the default count per scenario and the
    common factor."""
    rng = np.random.default_rng(seed)
    M = rng.standard_normal(n_sims)
    Z = rng.standard_normal((n_sims, n_names))
    X = np.sqrt(rho) * M[:, None] + np.sqrt(1 - rho) * Z
    if nu is None:
        thr = norm.ppf(pd)
    else:
        W = rng.chisquare(nu, n_sims) / nu
        X = X / np.sqrt(W)[:, None]
        thr = student_t.ppf(pd, nu)
    return (X < thr).sum(1), M


def tranche_loss(L, a, d):
    """The fraction of a tranche [a, d] lost when the pool loses L (fractions of the pool)."""
    L = np.asarray(L, float)
    return (np.minimum(L, d) - np.minimum(L, a)) / (d - a)


def lhp_tranche_el(pd, rho, R, a, d, n=4001):
    """Expected loss of tranche [a, d] in the large homogeneous pool: integrate the tranche loss of the pool loss
    (1 - R) p(M) over the factor M, p(M) = N((N^-1(pd) - sqrt(rho) M) / sqrt(1 - rho)), on a dense grid (the
    tranche payoff has kinks, which quadrature rules dislike)."""
    z = np.linspace(-9, 9, n)
    w = norm.pdf(z)
    w = w / w.sum()
    p = norm.cdf((norm.ppf(pd) - np.sqrt(rho) * z) / np.sqrt(1 - rho))
    return float(np.sum(w * tranche_loss((1 - R) * p, a, d)))


def base_correlation(el_equity, pd, R, d, lo=1e-4, hi=0.999):
    """The flat correlation at which the large pool gives the [0, d] tranche the expected loss ``el_equity``: the
    market's 'base correlation' for detachment d.  The equity tranche's expected loss falls as correlation rises."""
    return brentq(lambda r: lhp_tranche_el(pd, r, R, 0.0, d) - el_equity, lo, hi, xtol=1e-10)
