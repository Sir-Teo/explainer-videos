"""The surface builder (Part 12, the volatility desk): arbitrage-free parametrizations of implied total variance,
the butterfly and calendar checks in total-variance form, Dupire's local volatility, the variance-swap strike, and
the VIX formula.  Tested in ``tests/test_quant_house.py``.

* ``ssvi_w``, ``fit_ssvi``: Gatheral and Jacquier's (2014) surface SVI, w(k, theta) = theta/2 (1 + rho phi k +
  sqrt((phi k + rho)^2 + 1 - rho^2)) with the power-law phi(theta) = eta / (theta^g (1 + theta)^(1 - g)); free of
  calendar arbitrage when theta rises with T, and of butterfly arbitrage when eta (1 + |rho|) <= 2;
* ``g_function``: Gatheral's density condition on a smile w(k): g >= 0 everywhere, or a butterfly is negative;
* ``dupire_local_var``: local variance from total variance and its derivatives (Gatheral 2006, eq. 1.10);
* ``var_swap_strike``: the fair variance from a strip of out-of-the-money options weighted 1/K^2 (Carr and Madan
  1998; Demeterfi, Derman, Kamal and Zou 1999);
* ``vix``: the CBOE's discretization of the same integral, with its forward correction.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize


def phi_power(theta, eta, gam):
    theta = np.asarray(theta, float)
    return eta / (theta ** gam * (1 + theta) ** (1 - gam))


def ssvi_w(k, theta, rho, eta, gam):
    k, theta = np.asarray(k, float), np.asarray(theta, float)
    p = phi_power(theta, eta, gam)
    return 0.5 * theta * (1 + rho * p * k + np.sqrt((p * k + rho) ** 2 + 1 - rho ** 2))


def fit_ssvi(k, T, w, weights=None, theta_atm=None) -> dict:
    """Fit (rho, eta, gamma) and one ATM total variance theta per maturity to quotes (k, T, w = iv^2 T).  ``theta``
    is kept non-decreasing in T (no calendar arbitrage) and eta (1 + |rho|) <= 2 (no butterfly arbitrage)."""
    k, T, w = (np.asarray(a, float) for a in (k, T, w))
    wt = np.ones_like(w) if weights is None else np.asarray(weights, float)
    Ts = np.unique(T)
    if theta_atm is None:
        theta0 = np.array([max(np.interp(0.0, np.sort(k[T == t]), w[T == t][np.argsort(k[T == t])]), 1e-4) for t in Ts])
    else:
        theta0 = np.asarray(theta_atm, float)
    theta0 = np.maximum.accumulate(theta0)
    inc0 = np.diff(np.concatenate([[0.0], theta0]))

    def unpack(x):
        rho, eta, gam = np.tanh(x[0]), np.exp(x[1]), 1 / (1 + np.exp(-x[2]))
        eta = min(eta, 2 / (1 + abs(rho)))
        theta = np.cumsum(np.exp(x[3:]))
        return rho, eta, gam, theta

    def resid(x):
        rho, eta, gam, theta = unpack(x)
        th = theta[np.searchsorted(Ts, T)]
        return np.sqrt(wt) * (ssvi_w(k, th, rho, eta, gam) - w)

    x0 = np.concatenate([[np.arctanh(-0.3), np.log(1.0), 0.0], np.log(np.maximum(inc0, 1e-6))])
    r = optimize.least_squares(resid, x0, max_nfev=5000)
    rho, eta, gam, theta = unpack(r.x)
    return {"rho": float(rho), "eta": float(eta), "gamma": float(gam), "theta": theta, "T": Ts,
            "rmse": float(np.sqrt(np.mean((resid(r.x) / np.sqrt(wt)) ** 2)))}


def theta_at(fit: dict, T):
    """The ATM total variance of an SSVI fit at any maturity: linear between the fitted expiries, from zero at T = 0
    (so the short end keeps its forward variance), and extended past the last expiry at the last forward variance.
    Clamping instead would make the forward variance zero outside the quoted range, and Dupire's local volatility
    with it."""
    Tn = np.concatenate([[0.0], np.asarray(fit["T"], float)])
    th = np.concatenate([[0.0], np.asarray(fit["theta"], float)])
    T = np.asarray(T, float)
    slope = (th[-1] - th[-2]) / (Tn[-1] - Tn[-2])
    return np.where(T > Tn[-1], th[-1] + slope * (T - Tn[-1]), np.interp(T, Tn, th))


def ssvi_surface_w(fit: dict, k, T):
    """Total variance w(k, T) of an SSVI fit at any (k, T)."""
    return ssvi_w(k, theta_at(fit, T), fit["rho"], fit["eta"], fit["gamma"])


def local_vol_fn(fit: dict):
    """Dupire's local volatility sigma(k, t) of an SSVI fit, by finite differences (k = log S/F, zero rates)."""
    f = lambda k, T: ssvi_surface_w(fit, k, T)  # noqa: E731

    def lv(k, t):
        t = max(t, 0.25 / 365)
        w, dw, d2w, dT = numeric_derivs(f, k, t, h=2e-3, hT=min(2e-3, 0.5 * t))
        return np.sqrt(np.clip(dupire_local_var(k, w, dw, d2w, dT), 1e-4, 25.0))
    return lv


def local_vol_paths(fit: dict, days: int, n_paths: int, seed=0, substeps=4) -> np.ndarray:
    """Daily log(S_t/S_0) under Dupire's local volatility of an SSVI fit (log-Euler, ``substeps`` per day: the short
    end is steep, and a daily step underprices by about a vol point). Returns (days + 1, n_paths)."""
    lv = local_vol_fn(fit)
    g = np.random.default_rng(seed)
    h = 1 / 365 / substeps
    X = np.zeros((days + 1, n_paths))
    x = np.zeros(n_paths)
    for i in range(days):
        for j in range(substeps):
            s = lv(np.clip(x, -1.2, 1.2), (i * substeps + j + 1) * h)
            x = x - 0.5 * s * s * h + s * np.sqrt(h) * g.standard_normal(n_paths)
        X[i + 1] = x
    return X


# ---------------------------------------------------------------------------
def g_function(k, w, dw, d2w):
    """Gatheral's g(k) = (1 - k w'/(2w))^2 - (w'^2/4)(1/w + 1/4) + w''/2; the implied density is proportional to g
    times a positive factor, so g < 0 anywhere is a butterfly arbitrage."""
    k, w, dw, d2w = (np.asarray(a, float) for a in (k, w, dw, d2w))
    return (1 - k * dw / (2 * w)) ** 2 - dw ** 2 / 4 * (1 / w + 0.25) + d2w / 2


def dupire_local_var(k, w, dw, d2w, dwdT):
    """Local variance at log-moneyness k from total implied variance w(k, T): dw/dT divided by g(k)."""
    return np.asarray(dwdT, float) / g_function(k, w, dw, d2w)


def numeric_derivs(f, k, T, h=1e-3, hT=1e-4):
    """w, dw/dk, d2w/dk2 and dw/dT of a total-variance function f(k, T) by central differences."""
    w = f(k, T)
    dw = (f(k + h, T) - f(k - h, T)) / (2 * h)
    d2w = (f(k + h, T) - 2 * w + f(k - h, T)) / h ** 2
    dT = (f(k, T + hT) - f(k, T - hT)) / (2 * hT)
    return w, dw, d2w, dT


# ---------------------------------------------------------------------------
def var_swap_strike(K, otm_prices, F, T, df=1.0) -> float:
    """Fair variance (annualized) of a variance swap: (2 / (T df)) * integral of OTM option prices / K^2 dK, by the
    trapezoid rule, on the given strikes (puts below F, calls above)."""
    K, P = np.asarray(K, float), np.asarray(otm_prices, float)
    return float(2.0 / (T * df) * np.trapezoid(P / K ** 2, K))


def vix(K, calls, puts, F, T, r=0.0) -> float:
    """The CBOE VIX formula on one expiry: sigma^2 = (2/T) sum dK_i / K_i^2 e^{rT} Q(K_i) - (1/T)(F/K0 - 1)^2, with
    K0 the first strike at or below F, Q the put below K0, the call above, and their average at K0.  Returns the
    volatility (not x 100)."""
    K, C, P = (np.asarray(a, float) for a in (K, calls, puts))
    o = np.argsort(K)
    K, C, P = K[o], C[o], P[o]
    i0 = int(np.searchsorted(K, F, side="right") - 1)
    K0 = K[i0]
    Q = np.where(K < K0, P, C)
    Q[i0] = 0.5 * (P[i0] + C[i0])
    dK = np.empty_like(K)
    dK[1:-1] = (K[2:] - K[:-2]) / 2
    dK[0], dK[-1] = K[1] - K[0], K[-1] - K[-2]
    s2 = 2 / T * np.sum(dK / K ** 2 * np.exp(r * T) * Q) - (F / K0 - 1) ** 2 / T
    return float(np.sqrt(max(s2, 0.0)))


# ---------------------------------------------------------------------------
# Part 12's expansion: the trader's SVI, Lee's moments, SSVI's sufficient condition, how surfaces move,
# Gyöngy's projection, replication, the VIX's interpolation, risk-neutral moments, VIX futures and short-vol notes,
# and dealer gamma
# ---------------------------------------------------------------------------
def svi_jw(p: dict, T: float) -> dict:
    """Raw SVI (a, b, rho, m, s) to the "jump-wings" numbers a desk quotes (Gatheral 2004; Gatheral and Jacquier
    2014, sec. 3.3): ATM variance v, ATM skew psi, put-wing slope pw, call-wing slope cw, minimum variance vt."""
    a, b, rho, m, s = (float(p[x]) for x in ("a", "b", "rho", "m", "s"))
    w0 = a + b * (-rho * m + np.sqrt(m * m + s * s))
    sw = np.sqrt(w0)
    return {"v": w0 / T, "psi": b / (2 * sw) * (rho - m / np.sqrt(m * m + s * s)), "pw": b * (1 - rho) / sw,
            "cw": b * (1 + rho) / sw, "vt": (a + b * s * np.sqrt(1 - rho * rho)) / T}


def svi_from_jw(jw: dict, T: float) -> dict:
    """The inverse of :func:`svi_jw` (Gatheral and Jacquier 2014, Lemma 3.2); needs m != 0."""
    v, psi, pw, cw, vt = (float(jw[x]) for x in ("v", "psi", "pw", "cw", "vt"))
    w = v * T
    sw = np.sqrt(w)
    b = sw / 2 * (cw + pw)
    rho = 1 - pw * sw / b
    beta = rho - 2 * psi * sw / b
    alpha = np.sign(beta) * np.sqrt(1 / beta ** 2 - 1)
    m = (v - vt) * T / (b * (-rho + np.sign(alpha) * np.sqrt(1 + alpha ** 2) - alpha * np.sqrt(1 - rho ** 2)))
    s = alpha * m
    a = vt * T - b * s * np.sqrt(1 - rho ** 2)
    return {"a": float(a), "b": float(b), "rho": float(rho), "m": float(m), "s": float(s)}


def lee_moment(beta):
    """Lee's (2004) moment formula, inverted: a total-variance wing of slope ``beta`` (<= 2) means the moments
    E[S^(1+p)] (right wing) or E[S^(-q)] (left wing) are finite up to p = (2 - beta)^2 / (8 beta)."""
    beta = np.asarray(beta, float)
    with np.errstate(divide="ignore"):
        return np.where(beta > 0, (2 - beta) ** 2 / (8 * np.maximum(beta, 1e-300)), np.inf)


def lee_slope(p):
    """Lee's formula: the largest wing slope of total variance when moments are finite up to ``p``:
    beta = 2 - 4 (sqrt(p^2 + p) - p)."""
    p = np.asarray(p, float)
    return 2 - 4 * (np.sqrt(p * p + p) - p)


def ssvi_butterfly_bound(fit: dict, lo=1e-14, hi=50.0) -> float:
    """The smallest theta above which Gatheral and Jacquier's sufficient conditions for no butterfly arbitrage
    (Theorem 4.2: theta phi (1 + |rho|) < 4 and theta phi^2 (1 + |rho|) <= 4) hold for a power-law SSVI; 0 when they
    hold for every theta (gamma <= 1/2 and eta (1 + |rho|) <= 2)."""
    rho, eta, gam = fit["rho"], fit["eta"], fit["gamma"]

    def bad(th):
        p = phi_power(th, eta, gam)
        return (th * p * (1 + abs(rho)) >= 4) | (th * p * p * (1 + abs(rho)) > 4)

    th = np.logspace(np.log10(lo), np.log10(hi), 4001)
    b = bad(th)
    if not b.any():
        return 0.0
    i = int(np.nonzero(b)[0].max())
    if i == len(th) - 1:
        return float("inf")
    a_, c_ = th[i], th[i + 1]
    for _ in range(80):  # bisect the last crossing
        mid = np.sqrt(a_ * c_)
        a_, c_ = (mid, c_) if bad(mid) else (a_, mid)
    return float(c_)


def fit_ssvi_path(k, T, w, weights=None, x0=None) -> dict:
    """:func:`fit_ssvi`, recording every parameter vector the optimizer tries (for replaying the fit): returns the
    fit, plus ``path`` (rho, eta, gamma, theta...) and ``rmse_path`` (total-variance RMSE) per evaluation. ``x0``
    (unconstrained, as in :func:`fit_ssvi`) starts it elsewhere."""
    k, T, w = (np.asarray(a, float) for a in (k, T, w))
    wt = np.ones_like(w) if weights is None else np.asarray(weights, float)
    Ts = np.unique(T)
    theta0 = np.array([max(np.interp(0.0, np.sort(k[T == t]), w[T == t][np.argsort(k[T == t])]), 1e-4) for t in Ts])
    theta0 = np.maximum.accumulate(theta0)
    inc0 = np.diff(np.concatenate([[0.0], theta0]))

    def unpack(x):
        rho, eta, gam = np.tanh(x[0]), np.exp(x[1]), 1 / (1 + np.exp(-x[2]))
        eta = min(eta, 2 / (1 + abs(rho)))
        return rho, eta, gam, np.cumsum(np.exp(x[3:]))

    path, rm = [], []

    def resid(x):
        rho, eta, gam, theta = unpack(x)
        r = np.sqrt(wt) * (ssvi_w(k, theta[np.searchsorted(Ts, T)], rho, eta, gam) - w)
        path.append(np.concatenate([[rho, eta, gam], theta]))
        rm.append(float(np.sqrt(np.mean((r / np.sqrt(wt)) ** 2))))
        return r

    if x0 is None:
        x0 = np.concatenate([[np.arctanh(-0.3), np.log(1.0), 0.0], np.log(np.maximum(inc0, 1e-6))])
    r = optimize.least_squares(resid, np.asarray(x0, float), max_nfev=5000)
    rho, eta, gam, theta = unpack(r.x)
    return {"rho": float(rho), "eta": float(eta), "gamma": float(gam), "theta": theta, "T": Ts,
            "rmse": float(np.sqrt(np.mean((resid(r.x) / np.sqrt(wt)) ** 2))), "path": np.array(path[:-1]),
            "rmse_path": np.array(rm[:-1]), "nfev": int(r.nfev)}


def skew_stickiness(dlnS, datm, skew) -> dict:
    """The skew-stickiness ratio R = (d sigma_ATM / d ln S) / (d sigma / dk at the money) (Bergomi): 1 for sticky
    strike, 0 for sticky moneyness, about 2 for local volatility. The slope is a regression of ATM-vol changes on log
    spot changes; ``t`` is its ordinary t-statistic and ``corr`` the correlation."""
    x, y = np.asarray(dlnS, float), np.asarray(datm, float)
    xc, yc = x - x.mean(), y - y.mean()
    beta = float(xc @ yc / (xc @ xc))
    res = yc - beta * xc
    se = float(np.sqrt(res @ res / (len(x) - 2) / (xc @ xc)))
    sk = float(np.mean(skew))
    return {"R": beta / sk, "beta": beta, "skew": sk, "t": beta / se if se > 0 else np.inf,
            "corr": float(np.corrcoef(x, y)[0, 1]) if yc.std() > 0 else 0.0}


def surface_pca(X) -> dict:
    """Principal components of surface moves (Cont and da Fonseca 2002): ``X`` is (observations, grid points) of
    changes; returns the explained-variance shares, the components (rows) and the scores."""
    X = np.asarray(X, float)
    Xc = X - X.mean(0)
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    for i in range(len(Vt)):  # a sign convention: each component's largest loading is positive
        if Vt[i, np.argmax(np.abs(Vt[i]))] < 0:
            Vt[i], U[:, i] = -Vt[i], -U[:, i]
    return {"explained": S ** 2 / np.sum(S ** 2), "components": Vt, "scores": U * S}


def conditional_variance(x, v, k, width=0.025, min_count=50):
    """Gyöngy's projection, estimated: the mean of the instantaneous variance ``v`` over paths whose log price ``x``
    ends within ``width`` of each ``k`` (NaN where fewer than ``min_count`` paths land)."""
    x, v = np.asarray(x, float), np.asarray(v, float)
    out = np.full(len(np.atleast_1d(k)), np.nan)
    for i, kq in enumerate(np.atleast_1d(k)):
        m = np.abs(x - kq) < width
        if m.sum() >= min_count:
            out[i] = v[m].mean()
    return out


def strip_replication(K, otm, F, T, path) -> dict:
    """Replicate a variance swap along a price ``path`` (from inception to expiry, any sampling): buy the static strip
    (2/T) dK/K^2 of each out-of-the-money option at its price ``otm`` (its cost is the variance strike), then hold
    (2/T)(1/S_i - 1/F) of the underlying between rebalancing dates. Returns the strike, the strip's payoff, the hedge's
    gains, their sum (the replicated variance), the path's realized variance (sum of squared log returns over T) and
    the replication error."""
    K, P, S = np.asarray(K, float), np.asarray(otm, float), np.asarray(path, float)
    dK = np.gradient(K)
    q = 2 / T * dK / K ** 2
    kvar = float(np.sum(q * P))
    ST = S[-1]
    strip = float(np.sum(q * np.where(K < F, np.maximum(K - ST, 0), np.maximum(ST - K, 0))))
    hedge = float(2 / T * np.sum((1 / S[:-1] - 1 / F) * np.diff(S)))
    rv = float(np.sum(np.diff(np.log(S)) ** 2) / T)
    return {"kvar": kvar, "strip": strip, "hedge": hedge, "replicated": strip + hedge, "rv": rv,
            "error": strip + hedge - rv}


def vol_swap_convexity(rv) -> dict:
    """The vol swap's convexity: for realized variances ``rv``, E[sqrt V] against sqrt(E V), and the second-order
    approximation sqrt(E V) - var(V) / (8 (E V)^(3/2)) (Demeterfi et al. 1999; Carr and Lee 2009)."""
    rv = np.asarray(rv, float)
    m = float(rv.mean())
    es = float(np.sqrt(rv).mean())
    return {"E_sqrt": es, "sqrt_E": float(np.sqrt(m)), "gap": float(np.sqrt(m) - es),
            "approx": float(np.sqrt(m) - rv.var() / (8 * m ** 1.5)), "approx_gap": float(rv.var() / (8 * m ** 1.5))}


def vix_30d(T1, s1, T2, s2, target=30 / 365) -> float:
    """The VIX's last step: interpolate total variance linearly in time between two expiries (T1 < target < T2,
    volatilities s1, s2) and annualize at the target horizon."""
    w = T1 * s1 ** 2 * (T2 - target) / (T2 - T1) + T2 * s2 ** 2 * (target - T1) / (T2 - T1)
    return float(np.sqrt(w / target))


def rn_moments(K, otm, F, T) -> dict:
    """Bakshi, Kapadia and Madan (2003), from a strip of out-of-the-money (undiscounted) option prices: the
    risk-neutral mean, variance (annualized), skewness and kurtosis of r = ln(S_T/F), each moment a strip with the
    weight f''(K) of its payoff (Carr and Madan)."""
    K, P = np.asarray(K, float), np.asarray(otm, float)
    x = np.log(K / F)
    mu = -np.trapezoid(P / K ** 2, K)
    V = np.trapezoid(2 * (1 - x) / K ** 2 * P, K)
    W = np.trapezoid((6 * x - 3 * x * x) / K ** 2 * P, K)
    X = np.trapezoid((12 * x * x - 4 * x ** 3) / K ** 2 * P, K)
    var = V - mu ** 2
    return {"mean": float(mu), "var": float(var / T), "skew": float((W - 3 * mu * V + 2 * mu ** 3) / var ** 1.5),
            "kurt": float((X - 4 * mu * W + 6 * mu * mu * V - 3 * mu ** 4) / var ** 2)}


def vx_index(days, settle: dict, expiries) -> dict:
    """A short-term VIX futures index (the S&P 500 VIX Short-Term Futures Index's rule): hold the first and second
    month, moving weight from the first to the second day by day over each roll period (which ends the business day
    before the first month's expiry), w1 = (days left in the period) / (days in the period). ``days``: sorted trading
    days; ``settle[e][d]``: the settlement price of expiry e on day d. Returns daily returns (from the second day),
    the first-month weight used, and the index level (100 at the first day)."""
    days, expiries = list(days), sorted(expiries)
    pos = {d: i for i, d in enumerate(days)}
    roll_end = {e: max(d for d in days if d < e) if any(d < e for d in days) else None for e in expiries}

    def weights(d):
        e1 = next(e for e in expiries if roll_end[e] is not None and d <= roll_end[e])
        e0 = [e for e in expiries if e < e1]
        e2 = expiries[expiries.index(e1) + 1]
        start = pos[e0[-1]] if e0 and e0[-1] in pos else 0  # the period runs from the last expiry to the day before e1
        end = pos[roll_end[e1]]
        return e1, e2, (end - pos[d]) / (end - start + 1)

    ret, w1s = [], []
    for i in range(1, len(days)):
        p, d = days[i - 1], days[i]
        e1, e2, w1 = weights(p)
        if w1 > 0:
            num = w1 * settle[e1][d] + (1 - w1) * settle[e2][d]
            den = w1 * settle[e1][p] + (1 - w1) * settle[e2][p]
        else:  # the day before expiry: everything is already in the second month
            num, den = settle[e2][d], settle[e2][p]
        ret.append(num / den - 1)
        w1s.append(w1)
    ret = np.array(ret)
    return {"ret": ret, "w1": np.array(w1s), "level": 100 * np.concatenate([[1.0], np.cumprod(1 + ret)])}


def inverse_note(ret, L=-1.0, floor=0.0) -> np.ndarray:
    """A daily-reset leveraged note on an index with daily returns ``ret``: N_t = N_{t-1} (1 + L r_t), starting at 1,
    never below ``floor`` (a loss of everything ends it)."""
    out, n = [1.0], 1.0
    for r in np.asarray(ret, float):
        n = max(n * (1 + L * r), floor)
        out.append(n)
    return np.array(out)


def rebalance_flow(L, r, N):
    """The hedge a daily-reset note of leverage ``L`` and value ``N`` must trade at the close after an index return
    ``r`` to restore its exposure L N': (L^2 - L) r N (Cheng and Madhavan 2009). Positive means buy; for L = -1 and
    L = 2 alike, the hedger buys after a rise."""
    return (L * L - L) * np.asarray(r, float) * np.asarray(N, float)


def gamma_day(eps, k, close_share=0.5, n_close=30):
    """Dealer gamma in a toy day. ``eps`` (days, minutes): fundamental returns. Dealers with gamma k (in units of
    impact: k = lambda Gamma S; k > 0 long gamma, k < 0 short) hedge a share 1 - c of each move at once, which feeds back
    as r = eps / (1 + (1 - c) k), and leave the rest c for the close, trading -c k R in the last ``n_close`` minutes
    (R the day's return so far). Returns the minute returns, the return before the close and the last-minutes return."""
    eps = np.atleast_2d(np.asarray(eps, float))
    n = eps.shape[1]
    r = np.empty_like(eps)
    r[:, :n - n_close] = eps[:, :n - n_close] / (1 + (1 - close_share) * k)
    rest = r[:, :n - n_close].sum(1)
    r[:, n - n_close:] = eps[:, n - n_close:] - close_share * k * rest[:, None] / n_close
    return {"r": r, "rest": rest, "last": r[:, n - n_close:].sum(1)}
