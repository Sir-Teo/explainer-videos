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


def mc_euler_cost(eps, S0=100.0, K=100.0, T=1.0, sigma=0.2, r=0.05, seed=0):
    """The standard estimator's cost at the same accuracy: Euler bias ~ h, so h ~ eps and N ~ eps^-2, cost ~ eps^-3.
    The step count is the smallest power of two whose bias (measured against a fine reference) is below eps/sqrt 2."""
    g = np.random.default_rng(seed)
    ref = mlmc(eps / 4, S0, K, T, sigma, r, seed=seed + 7)["estimate"]
    for k in range(1, 12):
        n = 2 ** k
        y = _mlmc_level(k, 20000, S0, K, T, sigma, r, 2, g)
        yf = None
        # bias of the level-k estimator: E[P_k] - ref, estimated from the fine half of _mlmc_level's pair
        P = _plain_euler(n, 40000, S0, K, T, sigma, r, g)
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
