"""Stochastic volatility, jumps and Lévy models: characteristic functions, COS pricing, SABR, Andersen's QE scheme,
and the calibrator (Part 13).

Conventions: zero rates, prices in the forward measure; X = log(S_T / F) and every characteristic function is
phi(u) = E[exp(i u X)], with phi(-i) = 1 (the forward is a martingale).
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import least_squares

from explainer.quant.house import bs

# ---------------------------------------------------------------- characteristic functions


def heston_cf(u, T, v0, kappa, theta, xi, rho):
    """Heston (1993) in the 'little trap' form of Albrecher, Mayer, Schoutens and Tistaert (2007), which keeps the
    complex logarithm on its principal branch."""
    u = np.asarray(u, complex)
    iu = 1j * u
    b = kappa - rho * xi * iu
    d = np.sqrt(b * b + xi * xi * (iu + u * u))
    g = (b - d) / (b + d)
    e = np.exp(-d * T)
    C = kappa * theta / xi ** 2 * ((b - d) * T - 2.0 * np.log((1.0 - g * e) / (1.0 - g)))
    D = (b - d) / xi ** 2 * (1.0 - e) / (1.0 - g * e)
    return np.exp(C + D * v0)


def merton_jump_cf(u, T, lam, mj, sj):
    """The compensated compound-Poisson part of Merton (1976): log-normal jumps N(mj, sj^2) at rate lam."""
    u = np.asarray(u, complex)
    k = np.exp(mj + 0.5 * sj * sj) - 1.0
    return np.exp(lam * T * (np.exp(1j * u * mj - 0.5 * sj * sj * u * u) - 1.0 - 1j * u * k))


def kou_jump_cf(u, T, lam, p, eta1, eta2):
    """Kou (2002): double-exponential jumps, up with probability p and rate eta1 (> 1), down with rate eta2."""
    u = np.asarray(u, complex)
    k = p * eta1 / (eta1 - 1.0) + (1 - p) * eta2 / (eta2 + 1.0) - 1.0
    psi = p * eta1 / (eta1 - 1j * u) + (1 - p) * eta2 / (eta2 + 1j * u) - 1.0
    return np.exp(lam * T * (psi - 1j * u * k))


def bs_cf(u, T, sigma):
    u = np.asarray(u, complex)
    return np.exp(-0.5 * sigma * sigma * T * (u * u + 1j * u))


def bates_cf(u, T, v0, kappa, theta, xi, rho, lam, mj, sj):
    """Bates (1996): Heston plus Merton's jumps."""
    return heston_cf(u, T, v0, kappa, theta, xi, rho) * merton_jump_cf(u, T, lam, mj, sj)


def vg_cf(u, T, sigma, nu, th):
    """Variance gamma (Madan, Carr and Chang 1998): Brownian motion with drift th and volatility sigma, run on a
    gamma clock of variance rate nu; drift-corrected so the forward is a martingale."""
    u = np.asarray(u, complex)
    w = np.log(1.0 - th * nu - 0.5 * sigma * sigma * nu) / nu
    return (1.0 - 1j * u * th * nu + 0.5 * sigma * sigma * nu * u * u) ** (-T / nu) * np.exp(1j * u * w * T)


def nig_cf(u, T, alpha, beta, delta):
    """Normal inverse Gaussian (Barndorff-Nielsen 1997), drift-corrected."""
    u = np.asarray(u, complex)
    g0 = np.sqrt(alpha ** 2 - beta ** 2)
    w = delta * (np.sqrt(alpha ** 2 - (beta + 1.0) ** 2) - g0)
    return np.exp(T * delta * (g0 - np.sqrt(alpha ** 2 - (beta + 1j * u) ** 2)) + 1j * u * w * T)


def cumulants(cf, T, h=1e-3):
    """First two cumulants of X from the characteristic function, by central differences of log phi."""
    f = lambda t: np.log(cf(np.array([-1j * t]), T)[0]).real  # the cumulant generating function K(t) = log E[e^{tX}]
    k1 = (f(h) - f(-h)) / (2 * h)
    k2 = (f(h) - 2 * f(0.0) + f(-h)) / (h * h)
    return float(k1), float(max(k2, 1e-8))


# ---------------------------------------------------------------- pricing


def cos_price(cf, F, K, T, cp=1, N=1024, L=20.0):
    """Fang and Oosterlee's (2008) COS method: expand the density of X in cosines on [a, b]. Puts are priced by the
    series (bounded payoff), calls by parity. cf(u, T) is the characteristic function of X = log(S_T / F)."""
    K = np.atleast_1d(np.asarray(K, float))
    x = np.log(F / K)
    c1, c2 = cumulants(cf, T)
    a = c1 - L * np.sqrt(c2) + min(float(x.min()), 0.0)  # the range must cover y = log(S_T / K) = x + X
    b = c1 + L * np.sqrt(c2) + max(float(x.max()), 0.0)
    k = np.arange(N)
    w = k * np.pi / (b - a)
    # puts on y = x + X: payoff K (1 - e^y)+ ; the coefficients for e^y on [a, 0] and 1 on [a, 0]
    chi = (np.cos(w * (0 - a)) * 1.0 - np.cos(0.0) * np.exp(a) + w * np.sin(w * (0 - a)) * 1.0) / (1 + w * w)
    psi = np.where(k == 0, -a, np.sin(w * (0 - a)) / np.where(k == 0, 1, w))
    Vk = 2.0 / (b - a) * (psi - chi)
    phi = cf(w, T)
    terms = (phi[None, :] * np.exp(1j * w[None, :] * (x[:, None] - a))).real * Vk[None, :]
    terms[:, 0] *= 0.5
    put = K * terms.sum(axis=1)
    put = np.maximum(put, np.maximum(K - F, 0.0))
    out = np.where(np.broadcast_to(np.asarray(cp), put.shape) == 1, put + F - K, put)
    return np.maximum(out, 0.0)


def implied_vols(prices, F, K, T, cp=1):
    p = np.atleast_1d(prices)
    K = np.atleast_1d(K)
    cps = np.broadcast_to(cp, K.shape)
    return np.array([bs.implied_vol(pi, F, ki, T, 0.0, 0.0, int(c)) for pi, ki, c in zip(p, K, cps)], float)


def model_iv(cf, F, K, T):
    """Implied vols of a model at strikes K (out-of-the-money options)."""
    K = np.atleast_1d(np.asarray(K, float))
    cp = np.where(K >= F, 1, -1)
    return implied_vols(cos_price(cf, F, K, T, cp), F, K, T, cp)


# ---------------------------------------------------------------- SABR


def sabr_iv(F, K, T, alpha, beta, rho, nu):
    """Hagan, Kumar, Lesniewski and Woodward (2002): the lognormal implied vol of SABR to first order in T."""
    F = float(F)
    K = np.atleast_1d(np.asarray(K, float))
    fk = F * K
    lfk = np.log(F / K)
    om = 1.0 - beta
    pre = alpha / (fk ** (om / 2) * (1 + om ** 2 / 24 * lfk ** 2 + om ** 4 / 1920 * lfk ** 4))
    z = nu / alpha * fk ** (om / 2) * lfk
    xz = np.log((np.sqrt(1 - 2 * rho * z + z * z) + z - rho) / (1 - rho))
    ratio = np.where(np.abs(z) < 1e-8, 1.0, z / np.where(np.abs(xz) < 1e-12, 1.0, xz))
    corr = 1 + (om ** 2 / 24 * alpha ** 2 / fk ** om + rho * beta * nu * alpha / (4 * fk ** (om / 2))
                + (2 - 3 * rho ** 2) / 24 * nu ** 2) * T
    return pre * ratio * corr


def sabr_density(F, K, T, alpha, beta, rho, nu, h=None):
    """The risk-neutral density implied by Hagan's formula (Breeden-Litzenberger); negative where the expansion
    breaks down, typically at low strikes and long maturities."""
    K = np.asarray(K, float)
    h = h or 1e-3 * F
    c = lambda k: bs.black(F, k, T, sabr_iv(F, k, T, alpha, beta, rho, nu))
    return (c(K + h) - 2 * c(K) + c(K - h)) / (h * h)


# ---------------------------------------------------------------- simulation


def heston_qe(S0, v0, kappa, theta, xi, rho, T, n, n_paths, seed=0, psi_c=1.5, return_v=False):
    """Andersen's (2008) quadratic-exponential scheme for the variance, with the martingale-corrected log step
    (central weights gamma1 = gamma2 = 1/2). Zero rates."""
    rng = np.random.default_rng(seed)
    dt = T / n
    E = np.exp(-kappa * dt)
    g1 = g2 = 0.5
    k0 = -rho * kappa * theta / xi * dt
    k1 = g1 * dt * (kappa * rho / xi - 0.5) - rho / xi
    k2 = g2 * dt * (kappa * rho / xi - 0.5) + rho / xi
    k3 = g1 * dt * (1 - rho ** 2)
    k4 = g2 * dt * (1 - rho ** 2)
    A = k2 + 0.5 * k4
    x = np.full(n_paths, np.log(S0))
    v = np.full(n_paths, float(v0))
    xs = np.empty((n + 1, n_paths))
    vs = np.empty((n + 1, n_paths)) if return_v else None
    xs[0] = x
    if return_v:
        vs[0] = v
    for i in range(n):
        m = theta + (v - theta) * E
        s2 = v * xi ** 2 * E / kappa * (1 - E) + theta * xi ** 2 / (2 * kappa) * (1 - E) ** 2
        psi = s2 / (m * m)
        vn = np.empty_like(v)
        quad = psi <= psi_c
        # quadratic branch: v' = a (b + Z)^2
        pq = psi[quad]
        b2 = 2 / pq - 1 + np.sqrt(2 / pq) * np.sqrt(2 / pq - 1)
        aq = m[quad] / (1 + b2)
        Z = rng.standard_normal(quad.sum())
        vn[quad] = aq * (np.sqrt(b2) + Z) ** 2
        # exponential branch: a point mass at zero and an exponential tail
        pe = psi[~quad]
        p = (pe - 1) / (pe + 1)
        beta = (1 - p) / m[~quad]
        U = rng.random((~quad).sum())
        vn[~quad] = np.where(U <= p, 0.0, np.log((1 - p) / np.maximum(1 - U, 1e-300)) / beta)
        # martingale correction (Andersen's K0*): E[exp(A v')] computed per branch
        K0 = np.empty_like(v)
        K0[quad] = -A * b2 * aq / (1 - 2 * A * aq) + 0.5 * np.log(1 - 2 * A * aq) - (k1 + 0.5 * k3) * v[quad]
        K0[~quad] = -np.log(p + beta * (1 - p) / (beta - A)) - (k1 + 0.5 * k3) * v[~quad]
        x = x + K0 + k1 * v + k2 * vn + np.sqrt(np.maximum(k3 * v + k4 * vn, 0.0)) * rng.standard_normal(n_paths)
        v = vn
        xs[i + 1] = x
        if return_v:
            vs[i + 1] = v
    S = np.exp(xs)
    return (S, vs) if return_v else S


def bates_paths(S0, v0, kappa, theta, xi, rho, lam, mj, sj, T, n, n_paths, seed=0):
    S = heston_qe(S0, v0, kappa, theta, xi, rho, T, n, n_paths, seed=seed)
    rng = np.random.default_rng(seed + 1)
    dt = T / n
    k = np.exp(mj + 0.5 * sj * sj) - 1
    N = rng.poisson(lam * dt, (n, n_paths))
    J = mj * N + sj * np.sqrt(N) * rng.standard_normal((n, n_paths)) - lam * k * dt
    return S * np.exp(np.vstack([np.zeros(n_paths), np.cumsum(J, axis=0)]))


def vg_paths(S0, sigma, nu, th, T, n, n_paths, seed=0):
    rng = np.random.default_rng(seed)
    dt = T / n
    w = np.log(1.0 - th * nu - 0.5 * sigma * sigma * nu) / nu
    G = rng.gamma(dt / nu, nu, (n, n_paths))
    dX = th * G + sigma * np.sqrt(G) * rng.standard_normal((n, n_paths)) + w * dt
    return S0 * np.exp(np.vstack([np.zeros(n_paths), np.cumsum(dX, axis=0)]))


def forward_start(paths, i1, i2, m=1.0):
    """A forward-start call: at time i1, strike m times the then-spot, paid at i2, per unit of the then-spot."""
    r = paths[i2] / paths[i1]
    return float(np.mean(np.maximum(r - m, 0.0)))


def cliquet(paths, idx, cap=0.08, floor=0.0, gfloor=0.0):
    """A cliquet: the sum of period returns, each capped and floored, with a global floor."""
    r = np.diff(np.log(paths[idx]), axis=0)
    r = np.exp(r) - 1
    return float(np.mean(np.maximum(np.clip(r, floor, cap).sum(axis=0), gfloor)))


# ---------------------------------------------------------------- calibration

MODELS = {
    "Heston": dict(cf=lambda u, T, p: heston_cf(u, T, *p), names=("v0", "kappa", "theta", "xi", "rho"),
                   x0=(0.25, 2.0, 0.25, 1.0, -0.2), lo=(1e-3, 0.05, 1e-3, 0.05, -0.99), hi=(4.0, 20.0, 4.0, 6.0, 0.99)),
    "Bates": dict(cf=lambda u, T, p: bates_cf(u, T, *p), names=("v0", "kappa", "theta", "xi", "rho", "lam", "mj", "sj"),
                  x0=(0.2, 2.0, 0.2, 1.0, -0.1, 1.0, -0.05, 0.1),
                  lo=(1e-3, 0.05, 1e-3, 0.05, -0.99, 0.0, -0.5, 0.01), hi=(4.0, 20.0, 4.0, 6.0, 0.99, 20.0, 0.5, 0.6)),
    "VG": dict(cf=lambda u, T, p: vg_cf(u, T, *p), names=("sigma", "nu", "theta"),
               x0=(0.5, 0.2, -0.1), lo=(0.05, 1e-3, -5.0), hi=(2.0, 2.0, 5.0)),
    "NIG": dict(cf=lambda u, T, p: nig_cf(u, T, *p), names=("alpha", "beta", "delta"),
                x0=(5.0, -1.0, 1.0), lo=(1.05, -20.0, 0.01), hi=(60.0, 20.0, 10.0)),
}


def _feasible(name, p):
    if name == "VG":
        s, nu, th = p
        return 1.0 - th * nu - 0.5 * s * s * nu > 1e-6
    if name == "NIG":
        a, b, d = p
        return abs(b) + 1.0 < a
    return True


def residuals(name, p, quotes, pre=None):
    """Vega-weighted implied-vol errors, approximated as price errors over vega (in vol points)."""
    spec = MODELS[name]
    if not _feasible(name, p):
        return np.full(len(quotes["K"]), 50.0)
    out = np.empty(len(quotes["K"]))
    for T in np.unique(quotes["T"]):
        m = quotes["T"] == T
        F = float(quotes["F"][m][0])
        K = quotes["K"][m]
        cp = quotes["cp"][m]
        cf = lambda u, TT: spec["cf"](u, TT, p)
        with np.errstate(all="ignore"):
            pm = cos_price(cf, F, K, T, cp)
        pk = pre["price"][m] if pre else bs.black(F, K, T, quotes["iv"][m], cp=cp)
        vg = pre["vega"][m] if pre else F * np.sqrt(T) * bs.npdf(np.log(F / K) / (quotes["iv"][m] * np.sqrt(T))
                                                                     + 0.5 * quotes["iv"][m] * np.sqrt(T))
        e = (pm - pk) / np.maximum(vg, 1e-8) * 100
        out[m] = np.where(np.isfinite(e), e, 50.0)
    w = np.sqrt(quotes["vega"] / quotes["vega"].mean())
    return out * w


def calibrate(name, quotes, x0=None, max_nfev=400, trace=False, lo=None, hi=None):
    """Least-squares fit of a model to quotes. ``trace=True`` also returns every residual evaluation the optimizer
    made, as ``trace`` = [(evaluation, rmse, x), ...], for replays; ``lo``/``hi`` override the model's bounds (a
    parameter is held fixed by a bound of zero width, e.g. lo = hi = 15 for kappa)."""
    spec = MODELS[name]
    F, K, T, iv, cp = quotes["F"], quotes["K"], quotes["T"], quotes["iv"], quotes["cp"]
    price = np.array([float(bs.black(f, k, t, s, cp=int(c))) for f, k, t, s, c in zip(F, K, T, iv, cp)])
    d1 = np.log(F / K) / (iv * np.sqrt(T)) + 0.5 * iv * np.sqrt(T)
    pre = {"price": price, "vega": F * np.sqrt(T) * bs.npdf(d1)}
    x0 = np.asarray(x0 if x0 is not None else spec["x0"], float)
    lo = np.asarray(spec["lo"] if lo is None else lo, float)
    hi = np.asarray(spec["hi"] if hi is None else hi, float)
    free = hi > lo  # zero-width bounds hold a parameter fixed (least_squares needs lo < hi)
    full = lambda q: _embed(q, free, lo)  # noqa: E731
    log = []

    def fun(q):
        r_ = residuals(name, full(q), quotes, pre)
        if trace:
            log.append((len(log), float(np.sqrt(np.mean(r_ ** 2))), [float(v) for v in full(q)]))
        return r_

    q0 = np.clip(x0[free], lo[free], hi[free])
    r = least_squares(fun, q0, bounds=(lo[free], hi[free]), max_nfev=max_nfev, x_scale="jac")
    x = full(r.x)
    res = r.fun
    out = {"model": name, "params": dict(zip(spec["names"], map(float, x))), "x": x.tolist(),
           "rmse": float(np.sqrt(np.mean(res ** 2))), "nfev": int(r.nfev), "cost": float(r.cost)}
    if trace:
        out["trace"] = log
    return out


def _embed(q, free, fixed):
    x = np.array(fixed, float)
    x[free] = q
    return x


def surface_iv(name, x, F, K, T):
    spec = MODELS[name]
    return model_iv(lambda u, TT: spec["cf"](u, TT, x), F, K, T)


# ---------------------------------------------------------------- Part 13, expanded: more models, exact series,
# regularised calibration, the particle SLV, the vol index of Heston, forward starts, arbitrage-free SABR, hedging


def cgmy_cf(u, T, C, G, M, Y):
    """CGMY (Carr, Geman, Madan and Yor 2002): the tempered stable process with Levy density
    C e^{-G|x|}/|x|^{1+Y} (x < 0) and C e^{-Mx}/x^{1+Y} (x > 0). Y < 0 finite activity, 0 <= Y < 1 infinite activity
    of finite variation, 1 < Y < 2 infinite variation; Y -> 0 is variance gamma with C = 1/nu. Drift-corrected (M > 1)."""
    from scipy.special import gamma as _G

    u = np.asarray(u, complex)

    def psi(z):  # log E[e^{z X_1}] of the jump part, z = iu
        if abs(Y) < 1e-8:
            return -C * (np.log((M - z) / M) + np.log((G + z) / G))
        return C * _G(-Y) * ((M - z) ** Y - M ** Y + (G + z) ** Y - G ** Y)

    return np.exp(T * (psi(1j * u) - 1j * u * psi(1.0 + 0j)))


def _merton_cf(u, T, p):
    return bs_cf(u, T, p[0]) * merton_jump_cf(u, T, *p[1:])


def _kou_cf(u, T, p):
    return bs_cf(u, T, p[0]) * kou_jump_cf(u, T, *p[1:])


MODELS["Merton"] = dict(cf=_merton_cf, names=("sigma", "lam", "mj", "sj"), x0=(0.4, 2.0, -0.1, 0.15),
                        lo=(0.05, 0.0, -0.6, 0.01), hi=(2.0, 50.0, 0.6, 0.8))
MODELS["Kou"] = dict(cf=_kou_cf, names=("sigma", "lam", "p", "eta1", "eta2"), x0=(0.4, 3.0, 0.4, 10.0, 8.0),
                     lo=(0.05, 0.0, 0.0, 1.5, 0.5), hi=(2.0, 50.0, 1.0, 100.0, 100.0))
# CGMY's Y is fitted on one side of Y = 1 at a time (Gamma(-Y) has a pole there): finite variation by default; the
# bounds lo=(1e-4, 0.5, 1.5, 1.05), hi=(50, 60, 60, 1.95) passed to calibrate fit the infinite-variation side
MODELS["CGMY"] = dict(cf=lambda u, T, p: cgmy_cf(u, T, *p), names=("C", "G", "M", "Y"), x0=(1.0, 5.0, 8.0, 0.8),
                      lo=(0.01, 0.5, 1.5, 0.1), hi=(50.0, 60.0, 60.0, 0.95))


def merton_series(F, K, T, sigma, lam, mj, sj, cp=1, n_max=80):
    """Merton (1976) by his series: condition on the number of jumps n (Poisson, mean lam T); given n, ln S_T is
    normal with variance sigma^2 T + n sj^2 and the forward F e^{-lam kbar T + n (mj + sj^2/2)}; average Black's price
    with the Poisson weights. Zero rates, forward measure."""
    from scipy.special import gammaln

    K = np.atleast_1d(np.asarray(K, float))
    kbar = np.exp(mj + 0.5 * sj * sj) - 1.0
    out = np.zeros_like(K)
    lt = lam * T
    for n in range(n_max + 1):
        w = np.exp(-lt + (n * np.log(lt) if lt > 0 else (0.0 if n == 0 else -np.inf)) - gammaln(n + 1))
        if w < 1e-300:
            continue
        Fn = F * np.exp(-lam * kbar * T + n * (mj + 0.5 * sj * sj))
        sn = np.sqrt(sigma * sigma + n * sj * sj / T)
        out = out + w * bs.black(Fn, K, T, sn, cp=cp)
    return out


def _pre(quotes):
    F, K, T, iv, cp = quotes["F"], quotes["K"], quotes["T"], quotes["iv"], quotes["cp"]
    price = np.array([float(bs.black(f, k, t, s, cp=int(c))) for f, k, t, s, c in zip(F, K, T, iv, cp)])
    d1 = np.log(F / K) / (iv * np.sqrt(T)) + 0.5 * iv * np.sqrt(T)
    return {"price": price, "vega": F * np.sqrt(T) * bs.npdf(d1)}


def calibrate_reg(name, quotes, x_prev, lam, W=None, x0=None, max_nfev=400):
    """Tikhonov-regularised calibration (Cont and Tankov 2004 use relative entropy; this is the quadratic cousin):
    minimise |r(x)|^2 + lam n |W (x - x_prev)|^2, with r the calibrator's vega-weighted residuals over n quotes and W
    the inverse scale of each parameter (default 1 / max(|x_prev|, 0.05): relative changes). lam = 0 is calibrate;
    a large lam returns last week's x_prev."""
    spec = MODELS[name]
    pre = _pre(quotes)
    x_prev = np.asarray(x_prev, float)
    W = 1.0 / np.maximum(np.abs(x_prev), 0.05) if W is None else np.asarray(W, float)
    n = len(quotes["K"])
    s = np.sqrt(lam * n)

    def fun(p):
        return np.concatenate([residuals(name, p, quotes, pre), s * W * (p - x_prev)])

    q0 = np.clip(np.asarray(x_prev if x0 is None else x0, float), spec["lo"], spec["hi"])
    r = least_squares(fun, q0, bounds=(spec["lo"], spec["hi"]), max_nfev=max_nfev, x_scale="jac")
    res = r.fun[:n]
    return {"model": name, "params": dict(zip(spec["names"], map(float, r.x))), "x": r.x.tolist(),
            "rmse": float(np.sqrt(np.mean(res ** 2))), "nfev": int(r.nfev), "cost": float(r.cost), "lam": lam}


def slv_paths(lv_fn, heston_x, days, n_paths, mix=0.5, substeps=4, n_sub=8000, seed=0, info=None, grid=None,
              snap_days=(), n_snap=1500):
    """Stochastic local volatility by the particle method (Guyon and Henry-Labordere 2012): Heston's variance with
    its vol of vol scaled by the mixing fraction ``mix``, times a leverage function L(x, t) = sigma_loc(x, t) /
    sqrt(E[v | x]) estimated at every sub-step across the particles themselves (Nadaraya-Watson on a grid of
    log-moneyness, Silverman's bandwidth, from a subsample of ``n_sub`` particles). Zero rates. Returns the daily
    paths of log(S / S0), shape (days + 1, n_paths). ``info`` (a dict) receives the leverage every 10 days and, on
    ``snap_days``, ``n_snap`` particles (x, v) with that day's E[v | x] and L on the grid."""
    g = np.random.default_rng(seed)
    dt = 1 / 365
    X = np.zeros((days + 1, n_paths))
    x = np.zeros(n_paths)
    m = substeps
    h = dt / m
    v0, kappa, theta, xi, rho = heston_x
    xi = xi * mix
    v = np.full(n_paths, v0)
    grid = np.linspace(-1.0, 1.0, 81) if grid is None else np.asarray(grid, float)
    n_sub = min(n_sub, n_paths)
    Ls, snaps = [], []
    for i in range(days):
        for j in range(m):
            t = i * dt + (j + 1) * h
            sub = g.choice(n_paths, n_sub, replace=False)
            bw = 1.06 * np.std(x[sub]) * n_sub ** (-0.2) + 1e-3
            Wk = np.exp(-0.5 * ((grid[:, None] - x[None, sub]) / bw) ** 2)
            Ev = (Wk @ v[sub]) / np.maximum(Wk.sum(axis=1), 1e-300)
            Lg = lv_fn(grid, t) / np.sqrt(np.maximum(Ev, 1e-6))
            Lx = np.interp(x, grid, Lg)
            z1 = g.standard_normal(n_paths)
            z2 = rho * z1 + np.sqrt(1 - rho ** 2) * g.standard_normal(n_paths)
            vp = np.maximum(v, 0)
            x = x - 0.5 * Lx ** 2 * vp * h + Lx * np.sqrt(vp * h) * z1
            v = v + kappa * (theta - vp) * h + xi * np.sqrt(vp * h) * z2
        if i % 10 == 9:
            Ls.append({"t": (i + 1) * dt, "L": Lg.copy()})
        if (i + 1) in snap_days:
            snaps.append({"day": i + 1, "x": x[:n_snap].copy(), "v": v[:n_snap].copy(), "Ev": Ev.copy(),
                          "L": Lg.copy(), "bw": float(bw)})
        X[i + 1] = x
    if info is not None:
        info["L"] = Ls
        info["grid"] = grid
        info["snaps"] = snaps
    return X


def _cir_quantiles(v0, kappa, theta, xi, T, n):
    """n equally weighted points of Heston's v_T: the mid-quantiles of its scaled non-central chi-squared law."""
    from scipy.stats import ncx2

    E = np.exp(-kappa * T)
    c = xi * xi * (1 - E) / (4 * kappa)
    df = 4 * kappa * theta / (xi * xi)
    nc = 4 * kappa * E * v0 / (xi * xi * (1 - E))
    return c * ncx2.ppf((np.arange(n) + 0.5) / n, df, nc)


def heston_vix2(v, kappa, theta, tau=30 / 365):
    """Heston's squared vol index: the tau-day variance-swap rate given today's variance v, theta + (v - theta) b,
    b = (1 - e^{-kappa tau}) / (kappa tau) (the forward variance curve, averaged)."""
    b = (1 - np.exp(-kappa * tau)) / (kappa * tau)
    return theta + (np.asarray(v, float) - theta) * b


def heston_vix_options(v0, kappa, theta, xi, T, K, tau=30 / 365, n=4000):
    """Futures and options on Heston's tau-day vol index at T: E[VIX_T], calls and puts on VIX_T, by quadrature
    against the law of v_T. Also sqrt(E[VIX_T^2]), the forward variance-swap vol, which the future cannot exceed
    (Jensen)."""
    vT = _cir_quantiles(v0, kappa, theta, xi, T, n)
    vix = np.sqrt(np.maximum(heston_vix2(vT, kappa, theta, tau), 0))
    K = np.atleast_1d(np.asarray(K, float))
    return {"future": float(vix.mean()), "var_swap_vol": float(np.sqrt(np.mean(vix ** 2))),
            "call": np.maximum(vix[None, :] - K[:, None], 0).mean(1), "put": np.maximum(K[:, None] - vix[None, :], 0).mean(1),
            "floor": float(np.sqrt(theta * (1 - (1 - np.exp(-kappa * tau)) / (kappa * tau))))}


def heston_forward_start(x, T1, tau, k, n=200):
    """A forward-start call in Heston: at T1, struck at e^k times the then-spot, expiring tau later, per unit of
    spot. By scaling its T1-value is Heston's tau-call with today's variance replaced by v_{T1}; average over the law
    of v_{T1} (tower property)."""
    v0, kappa, theta, xi, rho = x
    K = np.exp(np.atleast_1d(np.asarray(k, float)))
    out = np.zeros_like(K)
    vs = _cir_quantiles(v0, kappa, theta, xi, T1, n)
    for v in vs:
        out += cos_price(lambda u, TT: heston_cf(u, TT, max(v, 1e-8), kappa, theta, xi, rho), 1.0, K, tau, 1)
    return out / len(vs)


def sabr_pde_density(f, alpha, beta, rho, nu, T, n=400, f_max=None, n_t=2000, snaps=(), K=None):
    """Arbitrage-free SABR (Hagan, Kumar, Lesniewski and Woodward 2014): the density Q(T, F) solves the effective
    forward equation Q_T = 1/2 (D^2(F) E(T, F) Q)_FF with D = sqrt(alpha^2 + 2 alpha rho nu y + nu^2 y^2) F^beta,
    y = (F^{1-beta} - f^{1-beta}) / (1 - beta), E = exp(rho nu alpha Gamma T), Gamma = (F^beta - f^beta) / (F - f),
    absorbed at 0 and at f_max (the masses Q_L, Q_R). Finite volumes, implicit Euler in T: the density stays
    non-negative and the total mass is exactly 1. Returns the cell centres, the density at T (and at ``snaps``),
    Q_L, Q_R, and call prices at ``K``."""
    from scipy.linalg import solve_banded

    f_max = f_max or 8 * f
    m0 = max(int(round(n * f / f_max - 0.5)), 1)
    h = f / (m0 + 0.5)  # f sits at the centre of cell m0
    Fc = (np.arange(n) + 0.5) * h
    fb = f ** beta
    y = (Fc ** (1 - beta) - f ** (1 - beta)) / (1 - beta)
    D2 = (alpha ** 2 + 2 * alpha * rho * nu * y + nu ** 2 * y ** 2) * Fc ** (2 * beta)
    dF = Fc - f
    Gam = np.where(np.abs(dF) < 1e-14, beta * f ** (beta - 1), (Fc ** beta - fb) / np.where(np.abs(dF) < 1e-14, 1, dF))
    q = np.zeros(n)
    q[m0] = 1 / h
    QL = QR = 0.0
    dt = T / n_t
    out_snaps = []
    snaps = sorted(snaps)
    for s in range(1, n_t + 1):
        t = s * dt
        Mt = 0.5 * D2 * np.exp(rho * nu * alpha * Gam * t)
        r = dt / h ** 2
        ab = np.zeros((3, n))  # (I - dt L) q_new = q_old, with absorbing ghosts M_ghost q_ghost = -M_edge q_edge
        ab[1] = 1 + 2 * r * Mt
        ab[1, 0] = 1 + 3 * r * Mt[0]
        ab[1, -1] = 1 + 3 * r * Mt[-1]
        ab[0, 1:] = -r * Mt[1:]
        ab[2, :-1] = -r * Mt[:-1]
        q = solve_banded((1, 1), ab, q)
        QL += dt * 2 * Mt[0] * q[0] / h
        QR += dt * 2 * Mt[-1] * q[-1] / h
        while snaps and t >= snaps[0] - 1e-12:
            out_snaps.append({"T": snaps.pop(0), "Q": q.copy(), "QL": QL, "QR": QR})
    res = {"F": Fc, "Q": q, "QL": float(QL), "QR": float(QR), "h": h, "f_max": n * h, "snaps": out_snaps,
           "mass": float(q.sum() * h + QL + QR), "mean": float((q * Fc).sum() * h + QR * n * h)}
    if K is not None:
        K = np.atleast_1d(np.asarray(K, float))
        res["call"] = (np.maximum(Fc[None, :] - K[:, None], 0) * q[None, :]).sum(1) * h + QR * np.maximum(n * h - K, 0)
    return res


def mv_delta(delta, vega, beta, S):
    """The minimum-variance delta (Hull and White 2017): the Black-Scholes delta plus vega times the expected move
    in implied vol per unit of spot, beta / S, where beta is the regression slope of d(sigma) on dS / S."""
    return np.asarray(delta, float) + np.asarray(vega, float) * np.asarray(beta, float) / np.asarray(S, float)
