"""The pricing engine (Part 16): Monte Carlo and its variance reduction, quasi-Monte Carlo with the Brownian bridge,
multilevel Monte Carlo, Longstaff-Schwartz with a duality bound, Greeks three ways and by adjoint differentiation,
finite differences (theta schemes, Rannacher, the American put as a complementarity problem), ADI for Heston, and
Carr-Madan's FFT.

Conventions: Black-Scholes with rate r unless said; prices for one unit of the underlying started at S0.
"""
from __future__ import annotations

import time

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import splu
from scipy.special import ndtri
from scipy.stats import qmc

from explainer.quant.house import bs

# ---------------------------------------------------------------- Monte Carlo and variance reduction


def mc_call(S0, K, T, sigma, r, n, method="plain", seed=0):
    """A European call by Monte Carlo on the terminal value: 'plain', 'antithetic', 'control' (the stock itself as
    control variate, E[e^{-rT} S_T] = S0), or 'is' (importance sampling: the normal shifted to the strike).
    Returns (price, standard error)."""
    g = np.random.default_rng(seed)
    disc = np.exp(-r * T)
    drift = (r - 0.5 * sigma ** 2) * T
    vol = sigma * np.sqrt(T)
    if method == "antithetic":
        z = g.standard_normal(n // 2)
        a = disc * np.maximum(S0 * np.exp(drift + vol * z) - K, 0)
        b = disc * np.maximum(S0 * np.exp(drift - vol * z) - K, 0)
        y = 0.5 * (a + b)
        return float(y.mean()), float(y.std(ddof=1) / np.sqrt(len(y)))
    z = g.standard_normal(n)
    if method == "is":
        theta = max((np.log(K / S0) - drift) / vol, 0.0)  # shift the normal so the strike sits at its centre
        zz = z + theta
        w = np.exp(-theta * zz + 0.5 * theta ** 2)
        y = disc * np.maximum(S0 * np.exp(drift + vol * zz) - K, 0) * w
        return float(y.mean()), float(y.std(ddof=1) / np.sqrt(n))
    ST = S0 * np.exp(drift + vol * z)
    y = disc * np.maximum(ST - K, 0)
    if method == "control":
        c = disc * ST
        b = np.cov(y, c)[0, 1] / np.var(c, ddof=1)
        y = y - b * (c - S0)
    return float(y.mean()), float(y.std(ddof=1) / np.sqrt(n))


def normals(n_paths, dim, kind="mc", seed=0):
    """Standard normals (n_paths, dim): pseudo-random, or scrambled Sobol through the inverse normal."""
    if kind == "mc":
        return np.random.default_rng(seed).standard_normal((n_paths, dim))
    u = qmc.Sobol(d=dim, scramble=True, seed=seed).random(n_paths)
    return ndtri(np.clip(u, 1e-12, 1 - 1e-12))


def brownian_bridge(z, T):
    """Brownian increments from normals by the Brownian bridge: the first normal fixes W_T, the next the midpoint,
    and so on, so the leading Sobol dimensions carry most of the path's variance (Caflisch, Morokoff and Owen 1997).
    n (columns) must be a power of two. Returns W at the n grid points."""
    n_paths, n = z.shape
    W = np.zeros((n_paths, n + 1))
    W[:, n] = np.sqrt(T) * z[:, 0]
    used = 1
    h = n
    while h > 1:
        half = h // 2
        for left in range(0, n, h):
            right, mid = left + h, left + half
            tl, tr, tm = left * T / n, right * T / n, mid * T / n
            mean = W[:, left] + (tm - tl) / (tr - tl) * (W[:, right] - W[:, left])
            sd = np.sqrt((tm - tl) * (tr - tm) / (tr - tl))
            W[:, mid] = mean + sd * z[:, used]
            used += 1
        h = half
    return W[:, 1:]


def asian_call_paths(S0, K, T, sigma, r, n_paths, n_steps=64, kind="mc", bridge=False, seed=0):
    """An arithmetic-average Asian call, priced from mc or Sobol normals, with or without the Brownian bridge."""
    z = normals(n_paths, n_steps, kind, seed)
    dt = T / n_steps
    W = brownian_bridge(z, T) if bridge else np.cumsum(np.sqrt(dt) * z, axis=1)
    t = dt * np.arange(1, n_steps + 1)
    S = S0 * np.exp((r - 0.5 * sigma ** 2) * t + sigma * W)
    return float(np.exp(-r * T) * np.maximum(S.mean(axis=1) - K, 0).mean())


# ---------------------------------------------------------------- multilevel Monte Carlo (Giles 2008)


def _mlmc_level(l, n, S0, K, T, sigma, r, M, g):
    """Samples of P_l - P_{l-1} for an Asian call under Euler-Maruyama with M^l steps (coarse path uses the same
    Brownian increments summed in pairs)."""
    nf = M ** l
    hf = T / nf
    dW = np.sqrt(hf) * g.standard_normal((n, nf))
    Sf = np.full(n, S0)
    sf = np.zeros(n)
    for i in range(nf):
        Sf = Sf + r * Sf * hf + sigma * Sf * dW[:, i]
        sf += Sf
    Pf = np.exp(-r * T) * np.maximum(sf / nf - K, 0)
    if l == 0:
        return Pf
    nc = nf // M
    hc = T / nc
    dWc = dW.reshape(n, nc, M).sum(axis=2)
    Sc = np.full(n, S0)
    sc = np.zeros(n)
    for i in range(nc):
        Sc = Sc + r * Sc * hc + sigma * Sc * dWc[:, i]
        sc += Sc
    Pc = np.exp(-r * T) * np.maximum(sc / nc - K, 0)
    return Pf - Pc


def mlmc(eps, S0=100.0, K=100.0, T=1.0, sigma=0.2, r=0.05, M=2, L0=2, n0=4000, seed=0, max_level=10):
    """Giles's (2008) multilevel estimator to root-mean-square accuracy eps: level variances V_l estimated from n0
    pilot samples, optimal N_l = 2 eps^-2 sqrt(V_l / C_l) sum sqrt(V_k C_k), levels added until the bias test passes.
    Returns the estimate, the cost (in Euler steps) and the per-level statistics."""
    g = np.random.default_rng(seed)
    L = L0
    sums = {}
    while True:
        for l in range(L + 1):
            if l not in sums:
                y = _mlmc_level(l, n0, S0, K, T, sigma, r, M, g)
                sums[l] = [y.sum(), (y * y).sum(), n0]
        V = np.array([max(sums[l][1] / sums[l][2] - (sums[l][0] / sums[l][2]) ** 2, 1e-14) for l in range(L + 1)])
        C = np.array([M ** l + (M ** (l - 1) if l else 0) for l in range(L + 1)], float)
        Nl = np.ceil(2 * eps ** -2 * np.sqrt(V / C) * np.sum(np.sqrt(V * C))).astype(int)
        for l in range(L + 1):
            extra = Nl[l] - sums[l][2]
            if extra > 0:
                y = _mlmc_level(l, int(extra), S0, K, T, sigma, r, M, g)
                sums[l][0] += y.sum()
                sums[l][1] += (y * y).sum()
                sums[l][2] += int(extra)
        means = np.array([abs(sums[l][0] / sums[l][2]) for l in range(L + 1)])
        bias = max(means[-1] / (M - 1), means[-2] / (M - 1) / M) if L >= 2 else means[-1]
        if bias < eps / np.sqrt(2) or L >= max_level:
            break
        L += 1
    est = sum(sums[l][0] / sums[l][2] for l in range(L + 1))
    cost = sum(sums[l][2] * C[l] for l in range(L + 1))
    return {"estimate": float(est), "cost": float(cost), "levels": L,
            "N": [int(sums[l][2]) for l in range(L + 1)], "V": V.tolist()}


def mc_euler_cost(eps, S0=100.0, K=100.0, T=1.0, sigma=0.2, r=0.05, seed=0, ref=None):
    """The standard estimator's cost at the same accuracy: Euler bias ~ h, so h ~ eps and N ~ eps^-2, cost ~ eps^-3.
    The step count is the smallest power of two whose bias (measured against a fine reference) is below eps/sqrt 2."""
    g = np.random.default_rng(seed)
    ref = ref if ref is not None else mlmc(eps / 4, S0, K, T, sigma, r, seed=seed + 7)["estimate"]
    for k in range(1, 12):
        n = 2 ** k
        P = _plain_euler(n, 40000, S0, K, T, sigma, r, g)  # the plain estimator with n steps; its bias vs ref
        bias = abs(P.mean() - ref)
        if bias < eps / np.sqrt(2):
            N = int(np.ceil(2 * P.var() / eps ** 2))
            return {"steps": n, "N": N, "cost": float(N * n), "bias": float(bias)}
    return {"steps": n, "N": 0, "cost": float("nan"), "bias": float(bias)}


def _plain_euler(nf, n, S0, K, T, sigma, r, g):
    hf = T / nf
    S = np.full(n, S0)
    s = np.zeros(n)
    for _ in range(nf):
        S = S + r * S * hf + sigma * S * np.sqrt(hf) * g.standard_normal(n)
        s += S
    return np.exp(-r * T) * np.maximum(s / nf - K, 0)


# ---------------------------------------------------------------- American options: LSM and a duality bound


def lsm_put(S0, K, T, sigma, r, n_steps=50, n_paths=100000, seed=0, degree=3, return_policy=False):
    """Longstaff and Schwartz (2001): regress discounted future cash flows on polynomials of the in-the-money spot,
    exercise where the payoff beats the fitted continuation. A lower bound (the policy is suboptimal)."""
    g = np.random.default_rng(seed)
    dt = T / n_steps
    z = g.standard_normal((n_steps, n_paths // 2))
    z = np.concatenate([z, -z], axis=1)
    S = S0 * np.exp(np.cumsum((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z, axis=0))
    S = np.vstack([np.full(S.shape[1], S0), S])
    cash = np.maximum(K - S[-1], 0)
    coefs = [None] * (n_steps + 1)
    for i in range(n_steps - 1, 0, -1):
        cash *= np.exp(-r * dt)
        itm = K - S[i] > 0
        if itm.sum() > degree + 1:
            x = S[i, itm] / K
            X = np.vander(x, degree + 1)
            beta, *_ = np.linalg.lstsq(X, cash[itm], rcond=None)
            coefs[i] = beta
            cont = X @ beta
            ex = (K - S[i, itm]) > cont
            idx = np.flatnonzero(itm)[ex]
            cash[idx] = K - S[i, idx]
    price = float(np.exp(-r * dt) * cash.mean())
    price = max(price, K - S0)
    return (price, coefs) if return_policy else price


def andersen_broadie_put(S0, K, T, sigma, r, coefs, n_steps=50, n_outer=1000, n_inner=200, seed=1, degree=3):
    """Andersen and Broadie's (2004) upper bound. Along each outer path, the LSM policy's value L_t is the payoff where
    the policy exercises and its continuation value C_t (by n_inner inner paths following the policy) where it does
    not. The martingale pi_{t+1} = pi_t + e^{-r(t+1)dt} L_{t+1} - e^{-r t dt} C_t, since C_t = E_t[e^{-r dt} L_{t+1}];
    then E[max_t (e^{-r t dt} h_t - pi_t)] bounds the American price from above (Rogers 2002; Haugh and Kogan 2004).
    Returns (upper bound, standard error)."""
    g = np.random.default_rng(seed)
    dt = T / n_steps

    def exercise(i, s):
        if i == n_steps:
            return K - s > 0
        b = coefs[i]
        if b is None or i == 0:
            return np.zeros_like(s, bool)
        itm = K - s > 0
        return itm & ((K - s) > np.vander(s / K, degree + 1) @ b)

    def continuation(i, s):
        """E_i[e^{-r(tau - i)dt} h_tau] for the policy's stopping time tau > i, by inner simulation."""
        if i == n_steps:
            return np.zeros_like(s)
        m = len(s)
        cur = np.repeat(s, n_inner)
        val = np.zeros(m * n_inner)
        alive = np.ones(m * n_inner, bool)
        for j in range(i + 1, n_steps + 1):
            cur = cur * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * g.standard_normal(m * n_inner))
            ex = alive & exercise(j, cur)
            val[ex] = (K - cur[ex]) * np.exp(-r * (j - i) * dt)
            alive &= ~ex
        return val.reshape(m, n_inner).mean(axis=1)

    S = np.full(n_outer, float(S0))
    C = continuation(0, S)
    pi = np.zeros(n_outer)
    best = np.maximum(K - S, 0) - pi
    for i in range(1, n_steps + 1):
        S = S * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * g.standard_normal(n_outer))
        h = np.maximum(K - S, 0)
        C_new = continuation(i, S)
        L = np.where(exercise(i, S), h, C_new)
        pi = pi + np.exp(-r * i * dt) * L - np.exp(-r * (i - 1) * dt) * C
        best = np.maximum(best, np.exp(-r * i * dt) * h - pi)
        C = C_new
    return float(best.mean()), float(best.std(ddof=1) / np.sqrt(n_outer))


# ---------------------------------------------------------------- Greeks


def greeks_three_ways(S0, K, T, sigma, r, n, payoff="call", seed=0, h=None):
    """Delta and vega of a call or a digital (pays 1 above K) by finite-difference bumps (common random numbers),
    the pathwise method, and the likelihood-ratio method (Broadie and Glasserman 1996). Returns estimates and their
    standard errors."""
    g = np.random.default_rng(seed)
    z = g.standard_normal(n)
    disc = np.exp(-r * T)
    sT = np.sqrt(T)

    def ST(s, v):
        return s * np.exp((r - 0.5 * v ** 2) * T + v * sT * z)

    def pay(x):
        return np.maximum(x - K, 0) if payoff == "call" else (x > K).astype(float)

    out = {}
    hS = h or 0.01 * S0
    hv = 0.001
    d_b = disc * (pay(ST(S0 + hS, sigma)) - pay(ST(S0 - hS, sigma))) / (2 * hS)
    v_b = disc * (pay(ST(S0, sigma + hv)) - pay(ST(S0, sigma - hv))) / (2 * hv)
    out["bump"] = (d_b, v_b)
    S = ST(S0, sigma)
    if payoff == "call":
        ind = (S > K).astype(float)
        d_p = disc * ind * S / S0
        v_p = disc * ind * S * (-sigma * T + sT * z)
        out["pathwise"] = (d_p, v_p)
    f = disc * pay(S)
    score_S = z / (S0 * sigma * sT)
    score_v = (z * z - 1) / sigma - z * sT
    out["likelihood ratio"] = (f * score_S, f * score_v)
    res = {}
    for k, (d, v) in out.items():
        res[k] = {"delta": float(d.mean()), "delta_se": float(d.std(ddof=1) / np.sqrt(n)),
                  "vega": float(v.mean()), "vega_se": float(v.std(ddof=1) / np.sqrt(n))}
    return res


def aad_greeks(S0, K, T, sigma, r, n_paths=20000, n_steps=50, seed=0):
    """Every first-order sensitivity of an arithmetic Asian call priced by Monte Carlo, in one backward pass of the
    series' own reverse-mode autodiff (AI Part 4), and the same by bumping each input. Returns prices, Greeks and
    the wall-clock times."""
    from explainer.ai.autodiff import Tensor

    g = np.random.default_rng(seed)
    z = g.standard_normal((n_steps, n_paths))
    dt = T / n_steps

    def price_np(s0, k, t, v, rr):
        d = t / n_steps
        x = np.log(s0) + np.cumsum((rr - 0.5 * v * v) * d + v * np.sqrt(d) * z, axis=0)
        return float(np.exp(-rr * t) * np.maximum(np.exp(x).mean(axis=0) - k, 0).mean())

    t0 = time.perf_counter()
    p0 = price_np(S0, K, T, sigma, r)
    t_price = time.perf_counter() - t0

    t0 = time.perf_counter()
    s0, k, t, v, rr = (Tensor(np.array(a, float), requires_grad=True) for a in (S0, K, T, sigma, r))
    d = t * (1.0 / n_steps)
    lx = s0.log()
    acc = None
    drift = (rr - v * v * 0.5) * d
    sdt = d ** 0.5
    for i in range(n_steps):
        lx = lx + drift + v * sdt * Tensor(z[i])
        e = lx.exp()
        acc = e if acc is None else acc + e
    avg = acc * (1.0 / n_steps)
    pay = (avg - k).relu()
    price = (pay.mean() * (rr * t * -1.0).exp())
    price.backward()
    t_aad = time.perf_counter() - t0
    aad = {"delta": float(s0.grad), "dK": float(k.grad), "theta_T": float(t.grad), "vega": float(v.grad),
           "rho": float(rr.grad)}

    t0 = time.perf_counter()
    eps = {"delta": 1e-2 * S0, "dK": 1e-2 * K, "theta_T": 1e-3, "vega": 1e-3, "rho": 1e-4}
    base = [S0, K, T, sigma, r]
    names = ["delta", "dK", "theta_T", "vega", "rho"]
    bump = {}
    for i, nm in enumerate(names):
        up, dn = list(base), list(base)
        up[i] += eps[nm]
        dn[i] -= eps[nm]
        bump[nm] = (price_np(*up) - price_np(*dn)) / (2 * eps[nm])
    t_bump = time.perf_counter() - t0
    return {"price": p0, "price_aad": float(price.data), "aad": aad, "bump": bump, "t_price": t_price, "t_aad": t_aad,
            "t_bump": t_bump}


# ---------------------------------------------------------------- finite differences


def fd_european(S0, K, T, sigma, r, nS=200, nt=50, scheme="cn", payoff="call", rannacher=0, Smax_mult=4.0):
    """The Black-Scholes PDE on a uniform S grid by the theta method: 'explicit' (theta 0), 'implicit' (1), 'cn'
    (1/2); ``rannacher`` fully implicit half-steps first, which damp the oscillations Crank-Nicolson leaves from a
    kinked or discontinuous payoff (Rannacher 1984). Returns the price at S0 and the grid solution."""
    Smax = Smax_mult * K
    S = np.linspace(0, Smax, nS + 1)
    dS = S[1] - S[0]
    dt = T / nt
    V = np.maximum(S - K, 0) if payoff == "call" else (S > K) + 0.5 * np.isclose(S, K)  # the jump's midpoint
    V = V.astype(float)
    i = np.arange(1, nS)
    a = 0.5 * sigma ** 2 * S[i] ** 2 / dS ** 2 - 0.5 * r * S[i] / dS
    b = -sigma ** 2 * S[i] ** 2 / dS ** 2 - r
    c = 0.5 * sigma ** 2 * S[i] ** 2 / dS ** 2 + 0.5 * r * S[i] / dS
    L = sp.diags([a[1:], b, c[:-1]], [-1, 0, 1], shape=(nS - 1, nS - 1), format="csc")
    I = sp.identity(nS - 1, format="csc")

    def bc(tau):
        hi = Smax - K * np.exp(-r * tau) if payoff == "call" else np.exp(-r * tau)
        return 0.0, hi

    steps = []
    for k in range(rannacher):
        steps.append((1.0, dt / 2))
        steps.append((1.0, dt / 2))
    th = {"explicit": 0.0, "implicit": 1.0, "cn": 0.5}[scheme]
    steps += [(th, dt)] * (nt - rannacher)
    tau = 0.0
    lus = {}
    for theta, h in steps:
        lo0, hi0 = bc(tau)
        tau += h
        lo1, hi1 = bc(tau)
        inner = V[1:-1]
        rhs = inner + (1 - theta) * h * (L @ inner)
        rhs[0] += h * a[0] * ((1 - theta) * lo0 + theta * lo1)
        rhs[-1] += h * c[-1] * ((1 - theta) * hi0 + theta * hi1)
        if theta == 0:
            new = rhs
        else:
            key = (theta, h)
            if key not in lus:
                lus[key] = splu((I - theta * h * L).tocsc())
            new = lus[key].solve(rhs)
        V = np.concatenate([[lo1], new, [hi1]])
    return float(np.interp(S0, S, V)), S, V


def fd_american_put(S0, K, T, sigma, r, nS=400, nt=400, omega=1.2, tol=1e-8):
    """The American put as a linear complementarity problem, by Crank-Nicolson with projected SOR at each step
    (Brennan and Schwartz 1977 posed it; Wilmott, Howison and Dewynne's textbook form)."""
    Smax = 4 * K
    S = np.linspace(0, Smax, nS + 1)
    dS = S[1] - S[0]
    dt = T / nt
    payoff = np.maximum(K - S, 0)
    V = payoff.copy()
    i = np.arange(1, nS)
    a = 0.5 * dt * (sigma ** 2 * i ** 2 - r * i)
    b = -dt * (sigma ** 2 * i ** 2 + r)
    c = 0.5 * dt * (sigma ** 2 * i ** 2 + r * i)
    for _ in range(nt):
        rhs = V[1:-1] + 0.5 * (a * V[:-2] + b * V[1:-1] + c * V[2:])
        x = V[1:-1].copy()
        lo = K  # V(0) = K for the American put
        for _it in range(500):
            err = 0.0
            for j in range(nS - 1):
                left = x[j - 1] if j > 0 else lo
                right = x[j + 1] if j < nS - 2 else 0.0
                y = (rhs[j] + 0.5 * (a[j] * left + c[j] * right)) / (1 - 0.5 * b[j])
                y = max(payoff[j + 1], x[j] + omega * (y - x[j]))
                err += (y - x[j]) ** 2
                x[j] = y
            if err < tol:
                break
        V = np.concatenate([[lo], x, [0.0]])
    return float(np.interp(S0, S, V))


# ---------------------------------------------------------------- ADI for Heston (Craig-Sneyd)


def _weights(x, i):
    """Three-point weights at node i of a non-uniform grid: first and second derivatives."""
    hm, hp = x[i] - x[i - 1], x[i + 1] - x[i]
    d1 = (-hp / (hm * (hm + hp)), (hp - hm) / (hm * hp), hm / (hp * (hm + hp)))
    d2 = (2 / (hm * (hm + hp)), -2 / (hm * hp), 2 / (hp * (hm + hp)))
    return d1, d2


def heston_adi(S0, K, T, v0, kappa, theta, xi, rho, r=0.0, nS=80, nv=40, nt=50, scheme="cs", Smax_mult=8.0,
               vmax=5.0, uniform=False):
    """A European call under Heston by an ADI scheme: Douglas ('do') or Craig-Sneyd ('cs'; Craig and Sneyd 1988),
    theta = 1/2, the mixed derivative explicit, on in 't Hout and Foulon's (2010) non-uniform grids, dense around the
    strike and near zero variance (``uniform`` for plain grids). Returns the price at (S0, v0)."""
    Smax = Smax_mult * K
    if uniform:
        S = np.linspace(0, Smax, nS + 1)
        v = np.linspace(0, vmax, nv + 1)
    else:
        c = K / 5
        xi_ = np.linspace(np.arcsinh(-K / c), np.arcsinh((Smax - K) / c), nS + 1)
        S = K + c * np.sinh(xi_)
        S[0] = 0.0
        d = vmax / 500
        eta = np.linspace(0, np.arcsinh(vmax / d), nv + 1)
        v = d * np.sinh(eta)
    NS, NV = nS + 1, nv + 1
    N = NS * NV
    idx = lambda i, j: i + NS * j  # noqa: E731
    R0, C0, V0_, R1, C1, V1, R2, C2, V2 = ([] for _ in range(9))
    for j in range(NV):
        for i in range(1, nS):
            if j == nv:
                continue
            k = idx(i, j)
            s, vv = S[i], v[j]
            d1S, d2S = _weights(S, i)
            for o, w1, w2 in zip((-1, 0, 1), d1S, d2S):
                R1.append(k)
                C1.append(idx(i + o, j))
                V1.append(0.5 * vv * s * s * w2 + r * s * w1 - (0.5 * r if o == 0 else 0.0))
            if j == 0:
                q = kappa * theta / (v[1] - v[0])
                R2 += [k, k]
                C2 += [k, idx(i, 1)]
                V2 += [-q - 0.5 * r, q]
                continue
            d1v, d2v = _weights(v, j)
            for o, w1, w2 in zip((-1, 0, 1), d1v, d2v):
                R2.append(k)
                C2.append(idx(i, j + o))
                V2.append(0.5 * xi * xi * vv * w2 + kappa * (theta - vv) * w1 - (0.5 * r if o == 0 else 0.0))
            m = rho * xi * vv * s
            for oi, wi in zip((-1, 0, 1), d1S):
                for oj, wj in zip((-1, 0, 1), d1v):
                    R0.append(k)
                    C0.append(idx(i + oi, j + oj))
                    V0_.append(m * wi * wj)
    A0 = sp.csc_matrix((V0_, (R0, C0)), shape=(N, N))
    A1 = sp.csc_matrix((V1, (R1, C1)), shape=(N, N))
    A2 = sp.csc_matrix((V2, (R2, C2)), shape=(N, N))
    A = A0 + A1 + A2
    dt = T / nt
    I = sp.identity(N, format="csc")
    lu1 = splu((I - 0.5 * dt * A1).tocsc())
    lu2 = splu((I - 0.5 * dt * A2).tocsc())
    SS = np.tile(S, NV)
    U = np.maximum(SS - K, 0)

    def apply_bc(Uv, tau):
        Uv = Uv.copy()
        for j in range(NV):
            Uv[idx(0, j)] = 0.0
            Uv[idx(nS, j)] = S[nS] - K * np.exp(-r * tau)
        for i in range(NS):
            Uv[idx(i, nv)] = S[i]  # very high variance: the call is worth the stock
        return Uv

    tau = 0.0
    for _ in range(nt):
        tau += dt
        Y0 = U + dt * (A @ U)
        Y1 = lu1.solve(Y0 - 0.5 * dt * (A1 @ U))
        Y2 = lu2.solve(Y1 - 0.5 * dt * (A2 @ U))
        if scheme == "cs":
            Yh = Y0 + 0.5 * dt * (A0 @ (Y2 - U))
            Y1 = lu1.solve(Yh - 0.5 * dt * (A1 @ U))
            Y2 = lu2.solve(Y1 - 0.5 * dt * (A2 @ U))
        U = apply_bc(Y2, tau)
    grid = U.reshape(NV, NS)
    from scipy.interpolate import RegularGridInterpolator
    return float(RegularGridInterpolator((v, S), grid, method="cubic")((v0, S0)))


# ---------------------------------------------------------------- Fourier: Carr-Madan


def carr_madan(cf, S0, T, r=0.0, N=4096, eta=0.25, alpha=1.5):
    """Carr and Madan (1999): the damped call transform, inverted by one FFT for N log-strikes at once. ``cf(u, T)``
    is the characteristic function of log(S_T / F). Returns strikes and call prices."""
    F = S0 * np.exp(r * T)
    lam = 2 * np.pi / (N * eta)
    b = N * lam / 2
    j = np.arange(N)
    u = eta * j
    k = -b + lam * j
    phi = cf(u - (alpha + 1) * 1j, T) * np.exp(1j * (u - (alpha + 1) * 1j) * np.log(F))
    psi = np.exp(-r * T) * phi / (alpha ** 2 + alpha - u ** 2 + 1j * (2 * alpha + 1) * u)
    w = eta / 3 * (3 + (-1) ** (j + 1) - (j == 0))  # Simpson's weights
    x = np.exp(1j * b * u) * psi * w
    C = np.exp(-alpha * k) / np.pi * np.real(np.fft.fft(x))
    return np.exp(k), C


# ================================================================ Part 16, expanded: the further tools of the engine
# (appended; the functions above are unchanged, so every cached number that uses them stays valid)

# ---------------------------------------------------------------- variance reduction: controls, strata, shifts


def geometric_asian_call(S0, K, T, sigma, r, n_fix):
    """The discretely monitored geometric-average Asian call in closed form (Kemna and Vorst 1990): with fixings at
    t_i = iT/n, log G is normal with mean log S0 + (r - sigma^2/2) T (n+1)/(2n) and variance
    sigma^2 T (n+1)(2n+1)/(6n^2), so the price is a Black-Scholes formula."""
    n = n_fix
    mu = np.log(S0) + (r - 0.5 * sigma ** 2) * T * (n + 1) / (2 * n)
    s2 = sigma ** 2 * T * (n + 1) * (2 * n + 1) / (6 * n * n)
    s = np.sqrt(s2)
    d1 = (mu - np.log(K) + s2) / s
    d2 = d1 - s
    from scipy.stats import norm
    return float(np.exp(-r * T) * (np.exp(mu + 0.5 * s2) * norm.cdf(d1) - K * norm.cdf(d2)))


def asian_control(S0, K, T, sigma, r, n_paths, n_fix=64, seed=0, control="geometric"):
    """The arithmetic Asian call with a control variate: 'geometric' (the geometric Asian, known exactly; Kemna and
    Vorst 1990), 'stock' (the discounted final price, worth S0) or 'none'. b* = cov(Y, C)/var(C) from the same
    sample. Returns the price, its standard error, corr(Y, C), b* and the variance ratio var(Y)/var(Y - b*C)."""
    g = np.random.default_rng(seed)
    dt = T / n_fix
    t = dt * np.arange(1, n_fix + 1)
    W = np.cumsum(np.sqrt(dt) * g.standard_normal((n_paths, n_fix)), axis=1)
    S = S0 * np.exp((r - 0.5 * sigma ** 2) * t + sigma * W)
    disc = np.exp(-r * T)
    Y = disc * np.maximum(S.mean(axis=1) - K, 0)
    if control == "none":
        return {"price": float(Y.mean()), "se": float(Y.std(ddof=1) / np.sqrt(n_paths)), "rho": 0.0, "b": 0.0,
                "ratio": 1.0}
    if control == "geometric":
        C = disc * np.maximum(np.exp(np.log(S).mean(axis=1)) - K, 0)
        EC = geometric_asian_call(S0, K, T, sigma, r, n_fix)
    else:
        C = disc * S[:, -1]
        EC = S0
    b = np.cov(Y, C)[0, 1] / np.var(C, ddof=1)
    Z = Y - b * (C - EC)
    return {"price": float(Z.mean()), "se": float(Z.std(ddof=1) / np.sqrt(n_paths)),
            "rho": float(np.corrcoef(Y, C)[0, 1]), "b": float(b), "ratio": float(Y.var() / Z.var())}


def stratified_call(S0, K, T, sigma, r, n, n_strata, seed=0):
    """A European call with the terminal normal stratified: [0, 1] cut into n_strata equal pieces, n / n_strata
    uniforms in each (proportional allocation), mapped through the inverse normal. The between-strata variance is
    gone, so var <= plain var. Returns (price, standard error)."""
    g = np.random.default_rng(seed)
    m = n // n_strata
    k = np.arange(n_strata)[:, None]
    u = (k + g.random((n_strata, m))) / n_strata
    z = ndtri(u)
    y = np.exp(-r * T) * np.maximum(S0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * z) - K, 0)
    mk = y.mean(axis=1)
    vk = y.var(axis=1, ddof=1) if m > 1 else np.zeros(n_strata)
    return float(mk.mean()), float(np.sqrt(np.sum(vk / m)) / n_strata)


def is_cross_entropy(f, theta0=0.0, n=20000, iters=4, seed=0):
    """The cross-entropy method for a normal mean shift (Rubinstein 1997): sample Z ~ N(theta_k, 1), weight by the
    likelihood ratio w = e^{-theta Z + theta^2/2} and by the payoff f(Z) >= 0, and move theta to the weighted mean
    of Z (the maximiser of E[f w log q_theta] in the normal family). Returns the iterates theta_0, theta_1, ..."""
    g = np.random.default_rng(seed)
    th = float(theta0)
    out = [th]
    for _ in range(iters):
        z = g.standard_normal(n) + th
        ww = f(z) * np.exp(-th * z + 0.5 * th * th)
        if ww.sum() > 0:
            th = float((ww * z).sum() / ww.sum())
        out.append(th)
    return out


# ---------------------------------------------------------------- paths, discrepancy, effective dimension


def path_matrix(n_steps, T=1.0, kind="step"):
    """A matrix L with W = L Z (W at the grid t_k = kT/n, Z standard normals) and L L' = C, C_ij = min(t_i, t_j):
    'step' (cumulative sums: the random walk), 'bridge' (the Brownian bridge's construction) or 'pca' (C's
    eigenvectors scaled by root eigenvalues, largest first). Any such L gives the same law; they differ in which
    normals carry the variance."""
    dt = T / n_steps
    if kind == "step":
        return np.sqrt(dt) * np.tril(np.ones((n_steps, n_steps)))
    if kind == "bridge":
        return brownian_bridge(np.eye(n_steps), T).T
    i = np.arange(1, n_steps + 1)
    C = np.minimum.outer(i, i) * dt
    ev, V = np.linalg.eigh(C)
    o = np.argsort(ev)[::-1]
    return V[:, o] * np.sqrt(np.maximum(ev[o], 0))


def variance_captured(a, L):
    """For the linear functional a'W = (a'L) Z: the share of its variance carried by the first k normals, k = 1..n
    (each Z_j independent, so the shares are the squared entries of a'L, normalised and accumulated)."""
    c = (np.asarray(a, float) @ L) ** 2
    return np.cumsum(c) / c.sum()


def l2_star_discrepancy(x, chunk=2048):
    """The L2-star discrepancy of points x (n, d) in [0, 1]^d by Warnock's (1972) closed form:
    T^2 = 3^-d - 2^{1-d}/n sum_i prod_k (1 - x_ik^2) + 1/n^2 sum_{i,j} prod_k (1 - max(x_ik, x_jk))."""
    x = np.asarray(x, float)
    n, d = x.shape
    t1 = 3.0 ** -d
    t2 = 2.0 ** (1 - d) / n * np.prod(1 - x * x, axis=1).sum()
    t3 = 0.0
    for a in range(0, n, chunk):
        xa = x[a:a + chunk]
        p = np.ones((len(xa), n))
        for k in range(d):
            p *= 1 - np.maximum(xa[:, k][:, None], x[:, k][None, :])
        t3 += p.sum()
    return float(np.sqrt(max(t1 - t2 + t3 / n ** 2, 0.0)))


# ---------------------------------------------------------------- multilevel Monte Carlo, Euler or Milstein


def _mlmc_level_scheme(l, n, S0, K, T, sigma, r, M, g, scheme="euler", payoff="asian"):
    """P_l - P_{l-1} for an Asian ('asian', the average of the grid values) or a European ('call') call under Euler or
    Milstein steps (Milstein adds sigma^2 S (dW^2 - h)/2, strong order 1, so V_l falls like h^2 instead of h).
    With scheme 'euler' and payoff 'asian' it draws the same numbers as _mlmc_level."""
    nf = M ** l
    hf = T / nf
    dW = np.sqrt(hf) * g.standard_normal((n, nf))
    mil = scheme == "milstein"

    def run(dw, h, steps):
        S = np.full(n, float(S0))
        s = np.zeros(n)
        for i in range(steps):
            d = dw[:, i]
            S = S + r * S * h + sigma * S * d + (0.5 * sigma ** 2 * S * (d * d - h) if mil else 0.0)
            s += S
        x = s / steps if payoff == "asian" else S
        return np.exp(-r * T) * np.maximum(x - K, 0)

    Pf = run(dW, hf, nf)
    if l == 0:
        return Pf
    nc = nf // M
    return Pf - run(dW.reshape(n, nc, M).sum(axis=2), T / nc, nc)


def mlmc_run(eps, S0=100.0, K=100.0, T=1.0, sigma=0.2, r=0.05, M=2, L0=2, n0=4000, seed=0, max_level=10,
             scheme="euler", payoff="asian", trace=False):
    """Giles's multilevel estimator as :func:`mlmc` (with scheme 'euler' and payoff 'asian' it is the same estimator
    and draws the same numbers), for Euler or Milstein paths and an Asian or a European call. With ``trace`` the
    adaptive loop is logged: after each pass the levels, the samples N_l, the variances V_l, the corrections' means,
    the bias estimate and the cost so far."""
    g = np.random.default_rng(seed)
    L = L0
    sums = {}
    log = []
    while True:
        for l in range(L + 1):
            if l not in sums:
                y = _mlmc_level_scheme(l, n0, S0, K, T, sigma, r, M, g, scheme, payoff)
                sums[l] = [y.sum(), (y * y).sum(), n0]
        V = np.array([max(sums[l][1] / sums[l][2] - (sums[l][0] / sums[l][2]) ** 2, 1e-14) for l in range(L + 1)])
        C = np.array([M ** l + (M ** (l - 1) if l else 0) for l in range(L + 1)], float)
        Nl = np.ceil(2 * eps ** -2 * np.sqrt(V / C) * np.sum(np.sqrt(V * C))).astype(int)
        for l in range(L + 1):
            extra = Nl[l] - sums[l][2]
            if extra > 0:
                y = _mlmc_level_scheme(l, int(extra), S0, K, T, sigma, r, M, g, scheme, payoff)
                sums[l][0] += y.sum()
                sums[l][1] += (y * y).sum()
                sums[l][2] += int(extra)
        means = np.array([abs(sums[l][0] / sums[l][2]) for l in range(L + 1)])
        bias = max(means[-1] / (M - 1), means[-2] / (M - 1) / M) if L >= 2 else means[-1]
        if trace:
            log.append({"L": L, "N": [int(sums[l][2]) for l in range(L + 1)], "V": V.tolist(),
                        "mean": means.tolist(), "bias": float(bias),
                        "cost": float(sum(sums[l][2] * C[l] for l in range(L + 1)))})
        if bias < eps / np.sqrt(2) or L >= max_level:
            break
        L += 1
    est = sum(sums[l][0] / sums[l][2] for l in range(L + 1))
    cost = sum(sums[l][2] * C[l] for l in range(L + 1))
    out = {"estimate": float(est), "cost": float(cost), "levels": L, "N": [int(sums[l][2]) for l in range(L + 1)],
           "V": V.tolist()}
    if trace:
        out["trace"] = log
    return out


# ---------------------------------------------------------------- American: LSM traced, a Bermudan tree, five assets


def lsm_put_trace(S0, K, T, sigma, r, n_steps=25, n_paths=200000, seed=1, degree=3, n_show=2000, regress="cash"):
    """Longstaff-Schwartz as :func:`lsm_put`, recording each date's regression: the shown paths' in-the-money spots and
    realised discounted cash flows, the coefficients, and the exercise boundary (the highest spot below K where the
    payoff beats the fitted continuation). ``regress='value'`` regresses the estimated value max(h, fit) instead of
    the realised cash flow (Tsitsiklis and Van Roy 2001), which is biased high. Returns the in-sample price, the
    policy (coefficients by date), the boundary and the per-date records."""
    g = np.random.default_rng(seed)
    dt = T / n_steps
    z = g.standard_normal((n_steps, n_paths // 2))
    z = np.concatenate([z, -z], axis=1)
    S = S0 * np.exp(np.cumsum((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z, axis=0))
    S = np.vstack([np.full(S.shape[1], S0), S])
    cash = np.maximum(K - S[-1], 0)
    coefs = [None] * (n_steps + 1)
    bnd = np.full(n_steps + 1, np.nan)
    bnd[-1] = K
    recs = {}
    for i in range(n_steps - 1, 0, -1):
        cash *= np.exp(-r * dt)
        itm = K - S[i] > 0
        if itm.sum() <= degree + 1:
            continue
        X = np.vander(S[i, itm] / K, degree + 1)
        beta, *_ = np.linalg.lstsq(X, cash[itm], rcond=None)
        coefs[i] = beta
        cont = X @ beta
        ex = (K - S[i, itm]) > cont
        show = itm[:n_show]
        recs[i] = {"S": S[i, :n_show][show].tolist(), "Y": cash[:n_show][show].tolist(), "coef": beta.tolist()}
        idx = np.flatnonzero(itm)
        if regress == "value":
            cash[idx] = np.maximum(K - S[i, idx], cont)
        else:
            cash[idx[ex]] = K - S[i, idx[ex]]
        grid = np.linspace(max(0.5 * K, S[i, itm].min()), K, 2001)  # only where the regression saw data
        better = (K - grid) > np.vander(grid / K, degree + 1) @ beta
        if better.any():
            bnd[i] = grid[better].max()
    price = max(float(np.exp(-r * dt) * cash.mean()), K - S0)
    return {"price": price, "coefs": [None if c is None else c.tolist() for c in coefs], "boundary": bnd.tolist(),
            "records": recs, "paths": S[:, :n_show].T.tolist() if n_show else []}


def lsm_put_eval(coefs, S0, K, T, sigma, r, n_steps=25, n_paths=200000, seed=7, degree=3):
    """The value of a regression policy on fresh, independent paths: exercise at the first date where the put is in
    the money and the payoff beats the fitted continuation. An unbiased estimate of a lower bound (no foresight).
    Returns (price, standard error)."""
    g = np.random.default_rng(seed)
    dt = T / n_steps
    S = np.full(n_paths, float(S0))
    val = np.zeros(n_paths)
    alive = np.ones(n_paths, bool)
    for i in range(1, n_steps + 1):
        S = S * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * g.standard_normal(n_paths))
        h = np.maximum(K - S, 0)
        if i == n_steps:
            ex = alive & (h > 0)
        elif coefs[i] is None:
            ex = np.zeros(n_paths, bool)
        else:
            ex = alive & (h > 0) & (h > np.vander(S / K, degree + 1) @ np.asarray(coefs[i]))
        val[ex] = h[ex] * np.exp(-r * i * dt)
        alive &= ~ex
    return float(val.mean()), float(val.std(ddof=1) / np.sqrt(n_paths))


def bermudan_tree(S0, K, T, sigma, r, n_dates, n_steps, cp=-1):
    """A Bermudan option on a CRR tree of n_steps steps that may be exercised only on the n_dates equally spaced
    dates (n_steps a multiple of n_dates): the reference that a 25-date Longstaff-Schwartz price should be compared
    with (a fine tree that allows exercise at every step prices the American option instead)."""
    if n_steps % n_dates:
        raise ValueError("n_steps must be a multiple of n_dates")
    dt = T / n_steps
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    disc = np.exp(-r * dt)
    every = n_steps // n_dates
    V = np.maximum(cp * (S0 * u ** (2 * np.arange(n_steps + 1) - n_steps) - K), 0.0)
    for n in range(n_steps - 1, -1, -1):
        V = disc * (p * V[1:] + (1 - p) * V[:-1])
        if n % every == 0 and n > 0:
            V = np.maximum(V, cp * (S0 * u ** (2 * np.arange(n + 1) - n) - K))
    return float(V[0])


def _max_call_paths(p, n, g):
    dt = p["T"] / p["N"]
    z = g.standard_normal((p["N"], n, p["d"]))
    return p["s0"] * np.exp(np.cumsum((p["r"] - p["div"] - 0.5 * p["sigma"] ** 2) * dt
                                      + p["sigma"] * np.sqrt(dt) * z, axis=0))  # (dates 1..N, n, d)


def _max_call_basis(S, K):
    s = np.sort(S, axis=1)[:, ::-1] / K
    d = S.shape[1]
    q = np.maximum(s[:, 0] - 1, 0)
    cols = [np.ones(len(S))] + [s[:, i] for i in range(d)] + [s[:, i] ** 2 for i in range(d)]
    cols += [s[:, 0] * s[:, 1] if d > 1 else s[:, 0] ** 2, q, q * q, s[:, 0] ** 3]
    return np.stack(cols, axis=1)


def lsm_max_call(p, n_fit=200000, n_eval=400000, seed=1, chunk=50000):
    """Longstaff-Schwartz for the Bermudan max-call on d assets (Broadie and Glasserman's benchmark; the parameters
    of ``deep.MAX_CALL``): regress on the sorted prices, their squares, the two largest's product, the payoff and its
    square and the largest cubed, then evaluate the policy on n_eval independent paths (in chunks). Returns the
    in-sample price, the out-of-sample lower bound and its standard error, and the number of basis functions."""
    g = np.random.default_rng(seed)
    K, N, dt = p["K"], p["N"], p["T"] / p["N"]
    S = _max_call_paths(p, n_fit, g)
    pay = np.maximum(S.max(axis=2) - K, 0)
    cash = pay[-1].copy()
    betas = [None] * N
    for i in range(N - 2, -1, -1):
        cash *= np.exp(-p["r"] * dt)
        itm = pay[i] > 0
        X = _max_call_basis(S[i][itm], K)
        b, *_ = np.linalg.lstsq(X, cash[itm], rcond=None)
        betas[i] = b
        ex = pay[i][itm] > X @ b
        idx = np.flatnonzero(itm)[ex]
        cash[idx] = pay[i][idx]
    ins = float(np.exp(-p["r"] * dt) * cash.mean())
    del S, pay, cash
    ge = np.random.default_rng(seed + 1000)
    vals = []
    for a in range(0, n_eval, chunk):
        m = min(chunk, n_eval - a)
        S = _max_call_paths(p, m, ge)
        pay = np.maximum(S.max(axis=2) - K, 0)
        val = np.zeros(m)
        alive = np.ones(m, bool)
        for i in range(N):
            if i < N - 1:
                itm = alive & (pay[i] > 0)
                ex = np.zeros(m, bool)
                ex[itm] = pay[i][itm] > _max_call_basis(S[i][itm], K) @ betas[i]
            else:
                ex = alive & (pay[i] > 0)
            val[ex] = pay[i][ex] * np.exp(-p["r"] * (i + 1) * dt)
            alive &= ~ex
        vals.append(val)
    v = np.concatenate(vals)
    return {"in_sample": ins, "lower": float(v.mean()), "se": float(v.std(ddof=1) / np.sqrt(len(v))),
            "n_basis": int(len(betas[0]))}


# ---------------------------------------------------------------- AAD against bumping, by the number of inputs


def aad_basket(d, n_paths=4000, n_steps=12, seed=0, reps=5, T=1.0, r=0.05, K=100.0, bump_reps=None):
    """An arithmetic Asian basket call on d assets (spots 100, volatilities 20%, independent), priced by Monte Carlo;
    all 2d first derivatives (every spot and every volatility) by one reverse sweep of the series' autodiff, and by
    central bumps (4d extra pricings). Wall-clock times are the best of ``reps``; the machine-independent counts are
    the tape's nodes and element operations: forward ops (one per output element of every node) and backward ops (one
    multiply-add per input element of every edge). Returns both, and the largest delta disagreement. ``bump_reps``
    (default ``reps``) times the bumping fewer times when it is slow."""
    from explainer.ai.autodiff import Tensor, topological_order

    g = np.random.default_rng(seed)
    z = g.standard_normal((n_steps, n_paths, d))
    dt = T / n_steps
    S0 = np.full(d, 100.0)
    sig = np.full(d, 0.2)

    def price_np(s0, v):
        x = np.log(s0) + np.cumsum((r - 0.5 * v ** 2) * dt + v * np.sqrt(dt) * z, axis=0)
        return float(np.exp(-r * T) * np.maximum(np.exp(x).mean(axis=(0, 2)) - K, 0).mean())

    def price_ad():
        s = Tensor(S0.copy(), requires_grad=True)
        v = Tensor(sig.copy(), requires_grad=True)
        lx = s.log()
        acc = None
        for i in range(n_steps):
            lx = lx + (v * v * (-0.5) + r) * dt + v * np.sqrt(dt) * Tensor(z[i])
            e = lx.exp()
            acc = e if acc is None else acc + e
        avg = acc.sum(axis=1) * (1.0 / (n_steps * d))
        pr = (avg - K).relu().mean() * np.exp(-r * T)
        return pr, s, v

    def best(fn, k=None):
        b, out = np.inf, None
        for _ in range(k or reps):
            t0 = time.perf_counter()
            out = fn()
            b = min(b, time.perf_counter() - t0)
        best.last = out
        return b

    t_price = best(lambda: price_np(S0, sig))

    def aad():
        pr, s, v = price_ad()
        pr.backward()
        return s, v

    t_aad = best(aad)
    s, v = aad()

    def bump():
        out = []
        for j in range(d):
            e = np.zeros(d)
            e[j] = 1.0
            out.append((price_np(S0 + e, sig) - price_np(S0 - e, sig)) / 2.0)
            out.append((price_np(S0, sig + 1e-3 * e) - price_np(S0, sig - 1e-3 * e)) / 2e-3)
        return out

    t_bump = best(bump, bump_reps)
    gb = best.last
    pr, _, _ = price_ad()
    order = topological_order(pr)
    fwd = sum(t.data.size for t in order)
    bwd = sum(p_.data.size for t in order for p_, _ in t.parents)
    return {"d": d, "inputs": 2 * d, "t_price": t_price, "t_aad": t_aad, "t_bump": t_bump,
            "nodes": len(order), "fwd_ops": int(fwd), "bwd_ops": int(bwd),
            "max_delta_diff": float(np.abs(np.array(gb[0::2]) - s.grad).max()),
            "max_vega_diff": float(np.abs(np.array(gb[1::2]) - v.grad).max())}


# ---------------------------------------------------------------- the American put by the penalty method


def fd_american_penalty(S0, K, T, sigma, r, nS=400, nt=400, rho=1e8, rannacher=2, Smax_mult=4.0, keep=0):
    """The American put as a linear complementarity problem by the penalty method (Forsyth and Vetzal 2002): each
    time step solves (I - theta dt L + P) V = rhs + P g, P = rho where V < g (the payoff), Newton on the active set
    until it stops changing; Crank-Nicolson after ``rannacher`` fully implicit steps. Returns the price, the Newton
    iterations per step, the free boundary S*(tau) (the highest grid spot where V sits on the payoff), and with
    ``keep`` every keep-th time slice of V for drawing."""
    from scipy.sparse.linalg import spsolve
    Smax = Smax_mult * K
    S = np.linspace(0, Smax, nS + 1)
    dS = S[1] - S[0]
    dt = T / nt
    i = np.arange(1, nS)
    a = 0.5 * sigma ** 2 * S[i] ** 2 / dS ** 2 - 0.5 * r * S[i] / dS
    b = -sigma ** 2 * S[i] ** 2 / dS ** 2 - r
    c = 0.5 * sigma ** 2 * S[i] ** 2 / dS ** 2 + 0.5 * r * S[i] / dS
    L = sp.diags([a[1:], b, c[:-1]], [-1, 0, 1], format="csc")
    I = sp.identity(nS - 1, format="csc")
    gp = np.maximum(K - S[1:-1], 0)
    V = gp.copy()
    its, bnd, slices = [], [], []
    if keep:
        slices.append(np.concatenate([[K], V, [0.0]]).tolist())
    for n in range(nt):
        th = 1.0 if n < rannacher else 0.5
        rhs = V + (1 - th) * dt * (L @ V)
        rhs[0] += dt * a[0] * K
        x = V.copy()
        for k in range(50):
            P = rho * (x < gp)
            x_new = spsolve((I - th * dt * L + sp.diags(P)).tocsc(), rhs + P * gp)
            same = np.array_equal(x_new < gp, x < gp)
            x = x_new
            if same and k > 0:
                break
        its.append(k + 1)
        V = x
        on = np.flatnonzero((V - gp) <= 1e-6 * K)
        on = on[S[1:-1][on] < K]
        bnd.append(float(S[1:-1][on].max()) if len(on) else float("nan"))
        if keep and (n + 1) % keep == 0:
            slices.append(np.concatenate([[K], V, [0.0]]).tolist())
    Vf = np.concatenate([[K], V, [0.0]])
    return {"price": float(np.interp(S0, S, Vf)), "iterations": its, "boundary": bnd, "S": S.tolist(),
            "slices": slices}


# ---------------------------------------------------------------- Fourier: Lewis's single integral


def lewis_call(cf, S0, K, T, r=0.0, upper=200.0):
    """Lewis (2001): with the contour at Im u = -1/2, the call is one real integral,
    C = S0 - e^{-rT} sqrt(F K)/pi int_0^inf Re[e^{iuk} phi(u - i/2)] du / (u^2 + 1/4), k = log(F/K), F = S0 e^{rT};
    ``cf(u, T)`` is the characteristic function of log(S_T / F). Adaptive quadrature (scipy's quad)."""
    from scipy.integrate import quad
    F = S0 * np.exp(r * T)
    k = np.log(F / K)
    f = lambda u: float((np.exp(1j * u * k) * cf(np.asarray(u - 0.5j), T)).real / (u * u + 0.25))  # noqa: E731
    I, _ = quad(f, 0.0, upper, limit=500, epsabs=1e-13, epsrel=1e-13)
    return float(S0 - np.exp(-r * T) * np.sqrt(F * K) / np.pi * I)


# ---------------------------------------------------------------- quantum amplitude estimation, simulated


def mlae(a, powers=(0, 1, 2, 4, 8), shots=50, seed=0, n_grid=20001, n_fine=2001):
    """Maximum-likelihood amplitude estimation without phase estimation (Suzuki et al. 2020), simulated exactly: the
    state sits at angle theta, sin^2 theta = a; after m Grover iterations a measurement reads 'good' with probability
    sin^2((2m+1) theta), so each power m gets Binomial(shots, that) hits. After each power the likelihood is
    maximised, on a full grid at first and then on a fine grid around the last estimate (the likelihood's peaks
    narrow like 1/m). Oracle calls count 2m+1 per shot. Returns the estimate and the cumulative calls after each
    power, and the hits."""
    g = np.random.default_rng(seed)
    th = np.arcsin(np.sqrt(a))
    hits, ests, calls = [], [], []
    tot = 0
    est = None
    for m in powers:
        p = np.sin((2 * m + 1) * th) ** 2
        hits.append(int(g.binomial(shots, p)))
        tot += shots * (2 * m + 1)
        if est is None:
            grid = np.linspace(1e-6, np.pi / 2 - 1e-6, n_grid)
        else:
            w = np.pi / (2 * (2 * m + 1))
            grid = np.linspace(max(est - w, 1e-9), min(est + w, np.pi / 2 - 1e-9), n_fine)
        for _ in range(3):
            ll = np.zeros_like(grid)
            for mk, h in zip(powers, hits):
                q = np.clip(np.sin((2 * mk + 1) * grid) ** 2, 1e-300, 1 - 1e-16)
                ll += h * np.log(q) + (shots - h) * np.log1p(-q)
            j = int(np.argmax(ll))
            step = grid[1] - grid[0]
            est = float(grid[j])
            grid = np.linspace(max(est - 2 * step, 1e-12), min(est + 2 * step, np.pi / 2 - 1e-12), 401)
        ests.append(float(np.sin(est) ** 2))
        calls.append(tot)
    return {"estimates": ests, "calls": calls, "hits": hits, "theta": float(th)}


# ---------------------------------------------------------------- Chebyshev interpolation of a pricer


def chebyshev2d(f, box, n):
    """Tensor Chebyshev interpolation of f(x, y) on box ((x_lo, x_hi), (y_lo, y_hi)) with n x n Chebyshev points of
    the first kind (Gass, Glau, Mahlstedt and Mair 2018 for option prices): n^2 calls to f, then any point by a
    double Chebyshev sum. Returns the model (box, coefficients, nodes)."""
    from numpy.polynomial import chebyshev as Ch
    t = np.cos(np.pi * (np.arange(n) + 0.5) / n)
    (xa, xb), (ya, yb) = box
    xs = xa + (xb - xa) * (t + 1) / 2
    ys = ya + (yb - ya) * (t + 1) / 2
    P = np.array([[f(x, y) for y in ys] for x in xs])
    cx = Ch.chebfit(t, P, n - 1)               # (n coefficients in x, n values in y)
    coef = Ch.chebfit(t, cx.T, n - 1).T         # (n in x, n in y)
    return {"box": box, "coef": coef, "x": xs, "y": ys}


def chebyshev2d_eval(model, x, y):
    """The interpolant of :func:`chebyshev2d` at points (x, y) (arrays of the same shape)."""
    from numpy.polynomial import chebyshev as Ch
    (xa, xb), (ya, yb) = model["box"]
    u = 2 * (np.asarray(x, float) - xa) / (xb - xa) - 1
    v = 2 * (np.asarray(y, float) - ya) / (yb - ya) - 1
    return Ch.chebval2d(u, v, model["coef"])


# ---------------------------------------------------------------- the ADI solution on its whole grid


def heston_adi_grid(*args, **kwargs):
    """:func:`heston_adi`'s whole final grid instead of one interpolated price: the price surface u(S, v) at expiry
    tau = T, for drawing it and reading Greeks off it. (heston_adi interpolates its grid at (S0, v0) as its last step;
    this captures the grid it hands to the interpolator.) Returns (S, v, grid[v, S])."""
    import scipy.interpolate as si

    seen = {}
    real = si.RegularGridInterpolator

    class _Capture:
        def __init__(self, points, values, **kw):
            seen["v"], seen["S"] = (np.asarray(p) for p in points)
            seen["grid"] = np.asarray(values)

        def __call__(self, x):
            return 0.0

    si.RegularGridInterpolator = _Capture
    try:
        heston_adi(*args, **kwargs)
    finally:
        si.RegularGridInterpolator = real
    return seen["S"], seen["v"], seen["grid"]
