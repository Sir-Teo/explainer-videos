"""Measuring risk (Part 40): value at risk and expected shortfall, how to estimate them, how to backtest them, and what
can and cannot be checked.

Conventions: ``r`` are returns; losses are L = -r; VaR and ES are reported as positive losses at confidence ``alpha``
(0.99 means the 1% left tail of returns). VaR_alpha is the alpha-quantile of L and ES_alpha = E[L | L >= VaR_alpha].

* Estimators: Gaussian and Student-t, historical simulation, RiskMetrics' EWMA, filtered historical simulation on
  EWMA or GJR-GARCH residuals (Barone-Adesi et al. 1999), and McNeil and Frey's (2000) GARCH with a generalised Pareto
  tail; CAViaR (Engle and Manganelli 2004) and a quantile network, both fitted by the pinball loss.
* Backtests: Kupiec's coverage, Christoffersen's independence and conditional coverage, the Basel traffic light, and
  Acerbi and Szekely's (2014) Z2 test of ES.
* Tails and dependence: the generalised Pareto fit by maximum likelihood, Hill's estimator, empirical tail
  dependence, the t copula's tail-dependence coefficient.
* Stress and uncertainty: the most plausible scenario for a given loss (a Mahalanobis reverse stress test), and the
  rearrangement algorithm's bound on VaR under unknown dependence (Embrechts, Puccetti and Rüschendorf 2013).
* Scoring: the pinball loss (which elicits a quantile) and Fissler and Ziegel's joint VaR-ES score in the FZ0 form of
  Patton, Ziegel and Chen (2019)."""

from __future__ import annotations

import math

import numpy as np
from scipy import optimize, stats


# ---------------------------------------------------------------------------
# Static estimators
# ---------------------------------------------------------------------------
def var_es_normal(mu: float, sd: float, alpha: float = 0.99) -> tuple[float, float]:
    z = stats.norm.ppf(alpha)
    return float(-mu + sd * z), float(-mu + sd * stats.norm.pdf(z) / (1 - alpha))


def var_es_t(mu: float, scale: float, nu: float, alpha: float = 0.99) -> tuple[float, float]:
    """Student-t with ``scale`` (not the standard deviation): VaR = -mu + scale t_nu^{-1}(alpha), ES from the closed
    form scale (nu + q^2)/(nu - 1) f_nu(q)/(1 - alpha)."""
    q = stats.t.ppf(alpha, nu)
    es = scale * (nu + q ** 2) / (nu - 1) * stats.t.pdf(q, nu) / (1 - alpha)
    return float(-mu + scale * q), float(-mu + es)


def var_es_hist(r, alpha: float = 0.99) -> tuple[float, float]:
    L = -np.asarray(r, float)
    v = float(np.quantile(L, alpha))
    return v, float(L[L >= v].mean())


def ewma_sigma(r, lam: float = 0.94, init: float | None = None) -> np.ndarray:
    """RiskMetrics' volatility: sigma_t^2 = lam sigma_{t-1}^2 + (1 - lam) r_{t-1}^2, each known at t - 1."""
    r = np.asarray(r, float)
    s2 = np.empty(len(r))
    s2[0] = np.var(r[:250]) if init is None else init
    for t in range(1, len(r)):
        s2[t] = lam * s2[t - 1] + (1 - lam) * r[t - 1] ** 2
    return np.sqrt(s2)


def rolling_forecasts(r, alpha: float = 0.99, window: int = 500, start: int = 500, refit: int = 250,
                      methods=("normal", "hs", "ewma", "fhs", "gjr_fhs", "evt")) -> dict:
    """One-day-ahead VaR and ES for every day from ``start``, each from data before it.

    * ``normal``: Gaussian with the trailing ``window``'s mean and standard deviation;
    * ``hs``: historical simulation on the trailing window;
    * ``ewma``: Gaussian with RiskMetrics' volatility (lambda 0.94) and zero mean;
    * ``fhs``: EWMA-filtered historical simulation: the window's standardised residuals, rescaled by today's volatility;
    * ``gjr_fhs``: the same on GJR-GARCH residuals, refitted every ``refit`` days on all data so far;
    * ``evt``: McNeil and Frey: GJR residuals with a generalised Pareto tail above their 90th loss percentile."""
    from explainer.quant.house import vol as V
    r = np.asarray(r, float)
    n = len(r)
    out = {m: {"var": np.full(n, np.nan), "es": np.full(n, np.nan)} for m in methods}
    sig = ewma_sigma(r)
    z_e = r / sig
    gj_sig = np.full(n, np.nan)
    if "gjr_fhs" in methods or "evt" in methods:
        for a in range(start, n, refit):
            fit = V.garch_fit(r[:a] - r[:a].mean(), kind="gjr")
            seg = r[:min(a + refit, n)] - r[:a].mean()
            h = V.garch_filter(fit["params"], seg, kind="gjr")
            gj_sig[a:min(a + refit, n)] = np.sqrt(h[a:min(a + refit, n)])
            if a == start:
                gj_sig[:a] = np.sqrt(h[:a])
        gj_z = (r - np.nanmean(r[:start])) / gj_sig
    evt_cache = {}
    for t in range(start, n):
        w = r[t - window:t]
        if "normal" in methods:
            out["normal"]["var"][t], out["normal"]["es"][t] = var_es_normal(w.mean(), w.std(ddof=1), alpha)
        if "hs" in methods:
            out["hs"]["var"][t], out["hs"]["es"][t] = var_es_hist(w, alpha)
        if "ewma" in methods:
            out["ewma"]["var"][t], out["ewma"]["es"][t] = var_es_normal(0.0, sig[t], alpha)
        if "fhs" in methods:
            v, e = var_es_hist(z_e[t - window:t], alpha)
            out["fhs"]["var"][t], out["fhs"]["es"][t] = sig[t] * v, sig[t] * e
        if "gjr_fhs" in methods:
            zz = gj_z[max(0, t - 2500):t]
            v, e = var_es_hist(zz, alpha)
            out["gjr_fhs"]["var"][t], out["gjr_fhs"]["es"][t] = gj_sig[t] * v, gj_sig[t] * e
        if "evt" in methods:
            k = (t - start) // refit
            if k not in evt_cache:
                L = -gj_z[:t]
                L = L[np.isfinite(L)]
                u = float(np.quantile(L, 0.90))
                xi, beta = gpd_fit(L[L > u] - u)
                evt_cache[k] = evt_var_es(u, xi, beta, len(L), int((L > u).sum()), alpha)
            v, e = evt_cache[k]
            out["evt"]["var"][t], out["evt"]["es"][t] = gj_sig[t] * v, gj_sig[t] * e
    return out


def sqrt_time(r, h: int = 10, alpha: float = 0.99) -> dict:
    """The square-root-of-time rule against the h-day VaR read from overlapping h-day returns."""
    r = np.asarray(r, float)
    one, _ = var_es_hist(r, alpha)
    rh = np.convolve(r, np.ones(h), "valid")
    direct, _ = var_es_hist(rh, alpha)
    return {"one_day": one, "scaled": one * math.sqrt(h), "direct": direct}


# ---------------------------------------------------------------------------
# Backtests
# ---------------------------------------------------------------------------
def hits(r, var) -> np.ndarray:
    """1 on days whose loss exceeded the VaR forecast."""
    r, var = np.asarray(r, float), np.asarray(var, float)
    ok = np.isfinite(var)
    return ((-r[ok]) > var[ok]).astype(int)


def kupiec(I, p: float) -> dict:
    I = np.asarray(I, int)
    T, x = len(I), int(I.sum())
    ph = x / T
    ll0 = (T - x) * math.log(1 - p) + x * math.log(p)
    ll1 = (T - x) * math.log(1 - ph) + (x * math.log(ph) if x > 0 else 0.0) if 0 < ph < 1 else 0.0
    lr = float(-2 * (ll0 - ll1))
    return {"T": T, "x": x, "rate": ph, "LR": lr, "p_value": float(stats.chi2.sf(lr, 1))}


def christoffersen(I, p: float) -> dict:
    """Independence (a first-order Markov chain of hits against an independent one) and conditional coverage
    (Kupiec plus independence, two degrees of freedom)."""
    I = np.asarray(I, int)
    a, b = I[:-1], I[1:]
    n00, n01 = int(((a == 0) & (b == 0)).sum()), int(((a == 0) & (b == 1)).sum())
    n10, n11 = int(((a == 1) & (b == 0)).sum()), int(((a == 1) & (b == 1)).sum())
    p01 = n01 / max(n00 + n01, 1)
    p11 = n11 / max(n10 + n11, 1)
    p1 = (n01 + n11) / max(n00 + n01 + n10 + n11, 1)

    def ll(q, k0, k1):
        return (k0 * math.log(1 - q) if k0 and q < 1 else 0.0) + (k1 * math.log(q) if k1 and q > 0 else 0.0)
    lr_ind = -2 * (ll(p1, n00 + n10, n01 + n11) - ll(p01, n00, n01) - ll(p11, n10, n11))
    lr_uc = kupiec(I, p)["LR"]
    return {"p01": p01, "p11": p11, "LR_ind": float(lr_ind), "p_ind": float(stats.chi2.sf(lr_ind, 1)),
            "LR_cc": float(lr_uc + lr_ind), "p_cc": float(stats.chi2.sf(lr_uc + lr_ind, 2)), "n11": n11}


def traffic_light(x: int) -> str:
    """The Basel traffic light for exceptions of a 99% VaR in 250 days: green to 4, yellow 5 to 9, red from 10."""
    return "green" if x <= 4 else ("yellow" if x <= 9 else "red")


def acerbi_szekely_z2(r, var, es, alpha: float = 0.99) -> float:
    """Z2 = sum_t L_t 1{L_t > VaR_t} / (T (1 - alpha) ES_t) - 1, in losses: zero when ES is right, positive when it is
    underestimated. Acerbi and Szekely found its critical values nearly distribution-free: about 0.70 at 5% and 1.8
    at 0.01%."""
    r, var, es = (np.asarray(x, float) for x in (r, var, es))
    ok = np.isfinite(var) & np.isfinite(es)
    L, v, e = -r[ok], var[ok], es[ok]
    I = L > v
    return float(np.sum(L * I / e) / (len(L) * (1 - alpha)) - 1)


# ---------------------------------------------------------------------------
# Tails
# ---------------------------------------------------------------------------
def gpd_fit(excess) -> tuple[float, float]:
    """Maximum-likelihood generalised Pareto (xi, beta) for exceedances over a threshold."""
    y = np.asarray(excess, float)
    y = y[y > 0]

    def nll(p):
        xi, lb = p
        b = math.exp(lb)
        if abs(xi) < 1e-8:
            return len(y) * lb + y.sum() / b
        z = 1 + xi * y / b
        if np.any(z <= 0):
            return 1e12
        return len(y) * lb + (1 + 1 / xi) * np.sum(np.log(z))
    best = None
    for x0 in ((0.1, math.log(y.mean())), (0.3, math.log(y.mean())), (-0.05, math.log(y.mean()))):
        res = optimize.minimize(nll, x0, method="Nelder-Mead", options={"xatol": 1e-9, "fatol": 1e-9, "maxiter": 4000})
        if best is None or res.fun < best.fun:
            best = res
    return float(best.x[0]), float(math.exp(best.x[1]))


def evt_var_es(u: float, xi: float, beta: float, n: int, n_u: int, alpha: float) -> tuple[float, float]:
    """Peaks over threshold: VaR = u + beta/xi ((n/n_u (1 - alpha))^(-xi) - 1), ES = (VaR + beta - xi u)/(1 - xi)."""
    v = u + beta / xi * ((n / n_u * (1 - alpha)) ** (-xi) - 1)
    return float(v), float((v + beta - xi * u) / (1 - xi))


def hill_series(x, ks) -> np.ndarray:
    """Hill's estimator of the tail exponent from the k largest losses, for each k."""
    s = np.sort(np.asarray(x, float))[::-1]
    s = s[s > 0]
    out = []
    for k in ks:
        out.append(1.0 / np.mean(np.log(s[:k] / s[k])))
    return np.asarray(out)


def tail_dependence(x, y, q: float = 0.01) -> float:
    """Empirical lower-tail dependence at level q: P(X below its q-quantile | Y below its q-quantile)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    a, b = x < np.quantile(x, q), y < np.quantile(y, q)
    return float((a & b).sum() / max(b.sum(), 1))


def t_copula_lambda(rho: float, nu: float) -> float:
    """Tail-dependence coefficient of a t copula: 2 t_{nu+1}(-sqrt((nu + 1)(1 - rho)/(1 + rho))); zero for the Gaussian."""
    return float(2 * stats.t.cdf(-math.sqrt((nu + 1) * (1 - rho) / (1 + rho)), nu + 1))


# ---------------------------------------------------------------------------
# Stress and model uncertainty
# ---------------------------------------------------------------------------
def reverse_stress(w, Sigma, loss: float) -> dict:
    """The most plausible move x (smallest Mahalanobis distance x' Sigma^-1 x) that costs a linear portfolio w exactly
    ``loss``: x* = -loss Sigma w / (w' Sigma w), at distance loss / sqrt(w' Sigma w) standard deviations."""
    w = np.asarray(w, float)
    S = np.asarray(Sigma, float)
    s2 = float(w @ S @ w)
    x = -loss * (S @ w) / s2
    return {"x": x, "distance": loss / math.sqrt(s2)}


def rearrangement(Q, iters: int = 200) -> float:
    """The rearrangement algorithm: rearrange each column of the N x d matrix Q (each a marginal's quantiles over the
    upper tail) to be oppositely ordered to the sum of the others, until no change; the minimum row sum is the
    estimate of the worst-case VaR."""
    X = np.array(Q, float)
    for _ in range(iters):
        changed = False
        for j in range(X.shape[1]):
            rest = X.sum(1) - X[:, j]
            order = np.argsort(rest)
            col = np.sort(X[:, j])[::-1]
            new = np.empty_like(col)
            new[order] = col
            if not np.array_equal(new, X[:, j]):
                X[:, j] = new
                changed = True
        if not changed:
            break
    return float(X.sum(1).min())


def worst_var_pareto(theta: float, d: int, alpha: float, N: int = 2000) -> dict:
    """Bounds for the VaR of a sum of d Pareto(theta) losses (survival (1 + x)^-theta) with unknown dependence: the
    rearrangement algorithm's worst case, against comonotonic and independent sums (the latter by simulation)."""
    def q(p):
        return (1 - p) ** (-1 / theta) - 1
    lo = alpha + (1 - alpha) * np.arange(N) / N
    hi = alpha + (1 - alpha) * (np.arange(N) + 1) / N
    hi[-1] = alpha + (1 - alpha) * (N - 0.5) / N
    under = rearrangement(np.column_stack([q(lo)] * d))
    over = rearrangement(np.column_stack([q(hi)] * d))
    rng = np.random.default_rng(0)
    U = rng.random((400_000, d))
    indep = float(np.quantile(q(U).sum(1), alpha))
    return {"worst_lo": under, "worst_hi": over, "comonotonic": float(d * q(alpha)), "independent": indep}


# ---------------------------------------------------------------------------
# Scoring and learned quantiles
# ---------------------------------------------------------------------------
def pinball(q, r, tau: float) -> np.ndarray:
    """The pinball (quantile) loss of a return quantile forecast q at level tau: (1{r < q} - tau)(q - r)."""
    q, r = np.asarray(q, float), np.asarray(r, float)
    return ((r < q).astype(float) - tau) * (q - r)


def fz0(v, e, r, tau: float) -> np.ndarray:
    """Patton, Ziegel and Chen's FZ0 loss for the return quantile v and expected shortfall e (both negative, the
    left-tail convention) at level tau: -1{r <= v}(v - r)/(tau e) + v/e + log(-e) - 1. Consistent for the pair
    (Fissler and Ziegel 2016)."""
    v, e, r = (np.asarray(x, float) for x in (v, e, r))
    return -((r <= v) * (v - r)) / (tau * e) + v / e + np.log(-e) - 1


def caviar_fit(r, tau: float = 0.01, start: int = 250, x0=None) -> dict:
    """Engle and Manganelli's symmetric-absolute-value CAViaR: q_t = b0 + b1 q_{t-1} + b2 |r_{t-1}| for the return
    quantile at level tau, fitted by minimising the pinball loss (Nelder-Mead from several starts)."""
    r = np.asarray(r, float)
    q0 = float(np.quantile(r[:start], tau))

    def path(b):
        q = np.empty(len(r))
        q[0] = q0
        for t in range(1, len(r)):
            q[t] = b[0] + b[1] * q[t - 1] + b[2] * abs(r[t - 1])
        return q

    def obj(b):
        if not (0 <= b[1] < 1):
            return 1e9
        return float(np.mean(pinball(path(b), r, tau)[1:]))
    starts = [x0] if x0 is not None else [(q0 * 0.1, 0.9, -0.1), (q0 * 0.05, 0.95, -0.2), (0.0, 0.8, -0.4)]
    best = None
    for s in starts:
        res = optimize.minimize(obj, s, method="Nelder-Mead", options={"maxiter": 3000, "xatol": 1e-8, "fatol": 1e-12})
        if best is None or res.fun < best.fun:
            best = res
    return {"beta": best.x, "loss": float(best.fun), "q": path(best.x)}


def caviar_path(r, beta, q0: float) -> np.ndarray:
    r = np.asarray(r, float)
    q = np.empty(len(r))
    q[0] = q0
    for t in range(1, len(r)):
        q[t] = beta[0] + beta[1] * q[t - 1] + beta[2] * abs(r[t - 1])
    return q


def quantile_mlp(X, y, tau: float, hidden: int = 16, epochs: int = 60, lr: float = 3e-3, batch: int = 512,
                 seed: int = 0, l2: float = 1e-4):
    """A one-hidden-layer network for the tau-quantile of y given X, trained by Adam on the pinball loss. Returns a
    predict function."""
    rng = np.random.default_rng(seed)
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    mx, sx = X.mean(0), X.std(0) + 1e-12
    sy = float(y.std())
    Xs, ys = (X - mx) / sx, y / sy
    d = X.shape[1]
    P = {"W1": rng.normal(0, 1 / math.sqrt(d), (d, hidden)), "b1": np.zeros(hidden),
         "W2": rng.normal(0, 1 / math.sqrt(hidden), hidden), "b2": np.array(float(np.quantile(ys, tau)))}
    m = {k: np.zeros_like(v) for k, v in P.items()}
    s = {k: np.zeros_like(v) for k, v in P.items()}
    step = 0
    for _ in range(epochs):
        idx = rng.permutation(len(ys))
        for a in range(0, len(ys), batch):
            b = idx[a:a + batch]
            H = np.tanh(Xs[b] @ P["W1"] + P["b1"])
            q = H @ P["W2"] + P["b2"]
            g = (((ys[b] < q).astype(float) - tau)) / len(b)          # d pinball / d q
            G = {"W2": H.T @ g + l2 * P["W2"], "b2": np.array(g.sum())}
            dH = np.outer(g, P["W2"]) * (1 - H ** 2)
            G["W1"] = Xs[b].T @ dH + l2 * P["W1"]
            G["b1"] = dH.sum(0)
            step += 1
            for k in P:
                m[k] = 0.9 * m[k] + 0.1 * G[k]
                s[k] = 0.999 * s[k] + 0.001 * G[k] ** 2
                P[k] = P[k] - lr * (m[k] / (1 - 0.9 ** step)) / (np.sqrt(s[k] / (1 - 0.999 ** step)) + 1e-8)

    def predict(Xn):
        H = np.tanh(((np.asarray(Xn, float) - mx) / sx) @ P["W1"] + P["b1"])
        return (H @ P["W2"] + P["b2"]) * sy
    return predict


# ---------------------------------------------------------------------------
# Elicitability: level sets
# ---------------------------------------------------------------------------
def mixture_var_es(x1, p1, x2, p2, lam: float, alpha: float) -> dict:
    """VaR and ES (of losses) of two discrete loss distributions (atoms x, probabilities p) and of their mixture
    lam F1 + (1 - lam) F2: the check that VaR's level sets are convex and ES's are not."""
    def ve(x, p):
        x, p = np.asarray(x, float), np.asarray(p, float)
        o = np.argsort(x)
        x, p = x[o], p[o]
        c = np.cumsum(p)
        k = int(np.searchsorted(c, alpha - 1e-12))
        v = float(x[k])
        # ES as the average of the upper (1 - alpha) tail, splitting the atom at VaR (Acerbi-Tasche)
        tail = (c[k] - alpha) * v + float(np.sum(x[k + 1:] * p[k + 1:]))
        return v, tail / (1 - alpha)
    v1, e1 = ve(x1, p1)
    v2, e2 = ve(x2, p2)
    xm = np.r_[x1, x2]
    pm = np.r_[lam * np.asarray(p1, float), (1 - lam) * np.asarray(p2, float)]
    vm, em = ve(xm, pm)
    return {"var": (v1, v2, vm), "es": (e1, e2, em)}
