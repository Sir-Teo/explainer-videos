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
               x0=(0.5, 0.2, -0.1), lo=(0.05, 1e-3, -1.0), hi=(2.0, 2.0, 1.0)),
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


def calibrate(name, quotes, x0=None, max_nfev=400):
    spec = MODELS[name]
    F, K, T, iv, cp = quotes["F"], quotes["K"], quotes["T"], quotes["iv"], quotes["cp"]
    price = np.array([float(bs.black(f, k, t, s, cp=int(c))) for f, k, t, s, c in zip(F, K, T, iv, cp)])
    d1 = np.log(F / K) / (iv * np.sqrt(T)) + 0.5 * iv * np.sqrt(T)
    pre = {"price": price, "vega": F * np.sqrt(T) * bs.npdf(d1)}
    x0 = np.asarray(x0 if x0 is not None else spec["x0"], float)
    r = least_squares(lambda p: residuals(name, p, quotes, pre), x0, bounds=(spec["lo"], spec["hi"]),
                      max_nfev=max_nfev, x_scale="jac")
    res = r.fun
    return {"model": name, "params": dict(zip(spec["names"], map(float, r.x))), "x": r.x.tolist(),
            "rmse": float(np.sqrt(np.mean(res ** 2))), "nfev": int(r.nfev), "cost": float(r.cost)}


def surface_iv(name, x, F, K, T):
    spec = MODELS[name]
    return model_iv(lambda u, TT: spec["cf"](u, TT, x), F, K, T)
