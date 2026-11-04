"""The House's term-structure models (Part 19, *Term-Structure Models*): the rates desk's option pricers, built on the
curve of Part 18 (:class:`explainer.quant.house.rates.Curve`).

* :func:`vasicek_zcb`, :func:`cir_zcb`, :func:`affine_zcb`: zero-coupon bond prices in one-factor affine models, in
  closed form and from the Riccati equations;
* :class:`HullWhite`: the one-factor Gaussian model fitted exactly to today's curve: bond prices, options on bonds,
  caplets, caps and (by Jamshidian's decomposition) swaptions, and exact simulation of the short rate;
* :func:`bermudan_swaption_lsm`: a Bermudan receiver or payer swaption under Hull-White by Longstaff-Schwartz;
* :func:`black_swaption`, :func:`bachelier`, :func:`normal_iv`, :func:`sabr_normal_iv`: the market's quoting formulas;
* :func:`hjm_gaussian`: Gaussian HJM with factor volatilities (from Part 18's PCA), drift from the HJM condition;
* :func:`lmm_caplets`: a forward-rate (LIBOR/SOFR) market model simulated under the terminal measure;
* :func:`cochrane_piazzesi`: the tent-shaped forecasting factor of bond excess returns;
* :func:`cpr_scurve`, :func:`mbs_price`: a stylized prepayment curve and the negative convexity it gives a
  mortgage pass-through.

Rates are decimals; times in years.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.stats import norm


# ---------------------------------------------------------------------------
# One-factor affine models
# ---------------------------------------------------------------------------
def vasicek_zcb(r0, a, b, sigma, T):
    """Vasicek (1977): dr = a(b - r)dt + sigma dW.  P(0, T) = exp(A - B r0)."""
    T = np.asarray(T, float)
    B = (1 - np.exp(-a * T)) / a
    A = (b - sigma ** 2 / (2 * a ** 2)) * (B - T) - sigma ** 2 * B ** 2 / (4 * a)
    return np.exp(A - B * r0)


def cir_zcb(r0, a, b, sigma, T):
    """Cox, Ingersoll and Ross (1985): dr = a(b - r)dt + sigma sqrt(r) dW."""
    T = np.asarray(T, float)
    g = np.sqrt(a ** 2 + 2 * sigma ** 2)
    e = np.exp(g * T) - 1
    den = (g + a) * e + 2 * g
    B = 2 * e / den
    A = (2 * a * b / sigma ** 2) * np.log(2 * g * np.exp((a + g) * T / 2) / den)
    return np.exp(A - B * r0)


def affine_zcb(r0, kappa, theta, alpha, beta, T):
    """dr = kappa(theta - r)dt + sqrt(alpha + beta r) dW (Duffie and Kan 1996, one factor).  P = exp(A(T) - B(T) r0)
    with the Riccati equations B' = 1 - kappa B - beta B^2 / 2, A' = -kappa theta B + alpha B^2 / 2, A(0) = B(0) = 0,
    solved numerically: the check on the closed forms."""
    def f(t, y):
        A, B = y
        return [-kappa * theta * B + 0.5 * alpha * B ** 2, 1 - kappa * B - 0.5 * beta * B ** 2]
    T = np.atleast_1d(np.asarray(T, float))
    sol = solve_ivp(f, (0, float(T.max())), [0.0, 0.0], t_eval=np.sort(T), rtol=1e-11, atol=1e-13)
    A, B = sol.y
    order = np.argsort(np.argsort(T))
    return np.exp(A[order] - B[order] * r0)


# ---------------------------------------------------------------------------
# Hull-White, fitted to today's curve
# ---------------------------------------------------------------------------
class HullWhite:
    """dr = (theta(t) - a r) dt + sigma dW with theta(t) chosen so the model reprices ``curve`` (a rates.Curve)
    exactly.  r = x + phi(t), x an OU process from 0 and phi(t) = f(0, t) + sigma^2 (1 - e^{-at})^2 / (2 a^2)."""

    def __init__(self, curve, a: float, sigma: float):
        self.c, self.a, self.s = curve, float(a), float(sigma)

    def B(self, t, T):
        return (1 - np.exp(-self.a * (np.asarray(T) - np.asarray(t)))) / self.a

    def phi(self, t):
        t = np.asarray(t, float)
        return self.c.inst_fwd(t) + self.s ** 2 * (1 - np.exp(-self.a * t)) ** 2 / (2 * self.a ** 2)

    def V(self, t, T):
        """Variance of int_t^T x du (Brigo and Mercurio, eq. 3.38)."""
        a, s = self.a, self.s
        d = np.asarray(T, float) - np.asarray(t, float)
        return s ** 2 / a ** 2 * (d + 2 / a * np.exp(-a * d) - 1 / (2 * a) * np.exp(-2 * a * d) - 3 / (2 * a))

    def zcb(self, t, T, x):
        """P(t, T) given the state x(t) = r(t) - phi(t)."""
        PM = self.c.df(T) / self.c.df(t)
        return PM * np.exp(0.5 * (self.V(t, T) - self.V(0, T) + self.V(0, t)) - self.B(t, T) * x)

    def zcb_option(self, K, T, S, cp=1):
        """A call (cp=1) or put (cp=-1) expiring at T on the zero-coupon bond maturing at S, strike K."""
        a, s = self.a, self.s
        PT, PS = self.c.df(T), self.c.df(S)
        sp = s * np.sqrt((1 - np.exp(-2 * a * T)) / (2 * a)) * self.B(T, S)
        h = np.log(PS / (PT * K)) / sp + sp / 2
        return cp * (PS * norm.cdf(cp * h) - K * PT * norm.cdf(cp * (h - sp)))

    def caplet(self, K, T, delta):
        """A caplet on the simple rate from T to T + delta, strike K, paid at T + delta: a put on a bond."""
        return (1 + K * delta) * self.zcb_option(1 / (1 + K * delta), T, T + delta, cp=-1)

    def cap(self, K, T_end, delta=0.25, start=None):
        start = delta if start is None else start
        Ts = np.arange(start, T_end - 1e-9, delta)
        return float(sum(self.caplet(K, t, delta) for t in Ts))

    def swaption(self, K, T, tenor, freq=1, payer=True):
        """A European swaption expiring at T into a ``tenor``-year swap paying K ``freq`` times a year, by Jamshidian:
        the coupon bond's value is monotone in x, so the option on it splits into options on each zero."""
        times = T + np.arange(1, int(round(tenor * freq)) + 1) / freq
        c = np.full(len(times), K / freq)
        c[-1] += 1
        x_star = brentq(lambda x: float(np.sum(c * self.zcb(T, times, x))) - 1, -1.0, 1.0)
        Ks = self.zcb(T, times, x_star)
        cp = -1 if payer else 1
        return float(sum(ci * self.zcb_option(ki, T, ti, cp=cp) for ci, ki, ti in zip(c, Ks, times)))

    def simulate_x(self, times, n_paths, seed=0):
        """Exact OU draws of x at ``times`` (ascending, from 0) and the discount factor along each path:
        returns (x (paths, len(times)), D (paths, len(times)) = exp(-int_0^t r))."""
        rng = np.random.default_rng(seed)
        a, s = self.a, self.s
        times = np.asarray(times, float)
        x = np.zeros((n_paths, len(times)))
        I = np.zeros((n_paths, len(times)))  # int_0^t x
        xp, Ip, tp = np.zeros(n_paths), np.zeros(n_paths), 0.0
        for j, t in enumerate(times):
            dt = t - tp
            if dt > 0:
                e = np.exp(-a * dt)
                vx = s ** 2 / (2 * a) * (1 - e ** 2)
                Bd = (1 - e) / a
                vI = s ** 2 / a ** 2 * (dt - 2 * Bd + (1 - e ** 2) / (2 * a))
                cxi = s ** 2 / (2 * a ** 2) * (1 - e) ** 2
                z1, z2 = rng.standard_normal(n_paths), rng.standard_normal(n_paths)
                rho = cxi / np.sqrt(vx * vI)
                nx = xp * e + np.sqrt(vx) * z1
                nI = Ip + xp * Bd + np.sqrt(vI) * (rho * z1 + np.sqrt(max(1 - rho ** 2, 0)) * z2)
                xp, Ip = nx, nI
            x[:, j], I[:, j], tp = xp, Ip, t
        # int_0^t phi = -log P(0,t) + sigma^2/(2a^2) int (1-e^{-au})^2 du
        def int_phi(t):
            return (-np.log(self.c.df(t)) + s ** 2 / (2 * a ** 2) *
                    (t - 2 * (1 - np.exp(-a * t)) / a + (1 - np.exp(-2 * a * t)) / (2 * a)))
        D = np.exp(-(I + np.array([int_phi(t) for t in times])[None, :]))
        return x, D


def bermudan_swaption_lsm(hw: HullWhite, K, T0, T_end, freq=1, payer=False, n_paths=40000, seed=0, deg=3):
    """A Bermudan receiver or payer swaption exercisable on each reset date from T0 into the swap to T_end, by
    Longstaff-Schwartz on exact Hull-White paths.  The exercise rule (regressions of discounted continuation on the
    state, in the money only) is fitted on one set of paths and applied to an independent set, so the price is a
    true lower bound with no look-ahead.  Returns the price and its standard error, the in-sample price, every
    European in the schedule, and the exercise boundary: the swap rate beyond which the rule exercises, per date."""
    dates = np.arange(T0, T_end - 1e-9, 1 / freq)

    def swap_value(x, i):
        t = dates[i]
        times = t + np.arange(1, int(round((T_end - t) * freq)) + 1) / freq
        P = hw.zcb(t, times[None, :], x[:, i:i + 1])
        ann = P.sum(1) / freq
        par = (1 - P[:, -1]) / ann
        v = (K - par) * ann if not payer else (par - K) * ann
        return v, par

    def run(x, D, betas=None):
        n = x.shape[0]
        v_last, _ = swap_value(x, len(dates) - 1)
        cash = np.maximum(v_last, 0) * D[:, -1]
        fitted, bound = {}, {}
        for i in range(len(dates) - 2, -1, -1):
            v, par = swap_value(x, i)
            itm = v > 0
            if itm.sum() < 50:
                continue
            Xr = np.vander(x[itm, i], deg + 1)
            if betas is None:
                beta, *_ = np.linalg.lstsq(Xr, cash[itm] / D[itm, i], rcond=None)
                fitted[i] = beta
            else:
                beta = betas.get(i)
                if beta is None:
                    continue
            ex = v[itm] > Xr @ beta
            idx = np.where(itm)[0][ex]
            cash[idx] = v[idx] * D[idx, i]
            if len(idx):
                bound[float(dates[i])] = float(np.max(par[idx]) if not payer else np.min(par[idx]))
        return cash, fitted, bound
    xa, Da = hw.simulate_x(dates, n_paths, seed)
    cash_a, betas, _ = run(xa, Da)
    xb, Db = hw.simulate_x(dates, n_paths, seed + 1000)
    cash_b, _, bound = run(xb, Db, betas)
    euro = [hw.swaption(K, t, T_end - t, freq, payer=payer) for t in dates]
    return {"price": float(cash_b.mean()), "se": float(cash_b.std() / np.sqrt(n_paths)),
            "in_sample": float(cash_a.mean()), "europeans": euro, "dates": dates,
            "boundary": sorted(bound.items())}


# ---------------------------------------------------------------------------
# Quoting formulas
# ---------------------------------------------------------------------------
def bachelier(F, K, T, sigma_n, annuity=1.0, cp=1):
    """The normal (Bachelier) model: F a forward rate with absolute volatility sigma_n (decimal a year)."""
    s = sigma_n * np.sqrt(T)
    d = (F - K) / s
    return annuity * (cp * (F - K) * norm.cdf(cp * d) + s * norm.pdf(d))


def normal_iv(price, F, K, T, annuity=1.0, cp=1):
    return float(brentq(lambda s: bachelier(F, K, T, s, annuity, cp) - price, 1e-8, 1.0, xtol=1e-14))


def black_swaption(F, K, T, sigma, annuity=1.0, cp=1):
    """Black (1976) for a swaption on a forward swap rate F > 0, lognormal volatility sigma."""
    d1 = (np.log(F / K) + 0.5 * sigma ** 2 * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return annuity * cp * (F * norm.cdf(cp * d1) - K * norm.cdf(cp * d2))


def sabr_normal_iv(F, K, T, alpha, beta, rho, nu):
    """Hagan, Kumar, Lesniewski and Woodward (2002), the normal implied volatility of SABR to first order in T;
    beta = 0 is the normal SABR used for rates that can go negative."""
    F, K = float(F), np.asarray(K, float)
    if beta == 0:
        z = nu / alpha * (F - K)
        x = np.log((np.sqrt(1 - 2 * rho * z + z ** 2) + z - rho) / (1 - rho))
        ratio = np.where(np.abs(z) < 1e-8, 1.0, z / np.where(np.abs(x) < 1e-14, 1.0, x))
        return alpha * ratio * (1 + (2 - 3 * rho ** 2) / 24 * nu ** 2 * T)
    Fm = np.sqrt(F * K)
    lfk = np.log(F / K)
    z = nu / alpha * Fm ** (1 - beta) * lfk
    x = np.log((np.sqrt(1 - 2 * rho * z + z ** 2) + z - rho) / (1 - rho))
    ratio = np.where(np.abs(z) < 1e-8, 1.0, z / np.where(np.abs(x) < 1e-14, 1.0, x))
    num = alpha * Fm ** beta * (1 + lfk ** 2 / 24 + lfk ** 4 / 1920)
    den = 1 + (1 - beta) ** 2 / 24 * lfk ** 2 + (1 - beta) ** 4 / 1920 * lfk ** 4
    corr = 1 + T * (-beta * (2 - beta) * alpha ** 2 / (24 * Fm ** (2 - 2 * beta)) + rho * alpha * beta * nu /
                    (4 * Fm ** (1 - beta)) + (2 - 3 * rho ** 2) / 24 * nu ** 2)
    return num / den * ratio * corr


# ---------------------------------------------------------------------------
# Gaussian HJM and a forward-rate market model
# ---------------------------------------------------------------------------
def hjm_gaussian(f0, tau, vols, T: float, n_steps: int, n_paths: int, seed=0) -> dict:
    """Heath, Jarrow and Morton (1992) with deterministic factor volatilities: the forward curve f(t, t + tau) on the
    maturity grid ``tau`` (Musiela parametrization), ``vols`` (factors, len(tau)) its volatilities as functions of
    time to maturity.  The no-arbitrage drift is sigma(tau) . int_0^tau sigma, plus the shift df/dtau.  Returns the
    simulated curves and the money-market account, so discounted bond prices can be checked to be martingales."""
    rng = np.random.default_rng(seed)
    tau = np.asarray(tau, float)
    vols = np.atleast_2d(np.asarray(vols, float))
    dt = T / n_steps
    dtau = np.diff(tau, prepend=0.0)
    cum = np.cumsum(vols * dtau[None, :], axis=1)  # int_0^tau sigma_k
    drift = (vols * cum).sum(0)
    f = np.tile(np.asarray(f0, float), (n_paths, 1))
    bank = np.ones(n_paths)
    curves = [f.copy()]
    for _ in range(n_steps):
        r = f[:, 0]
        bank *= np.exp(r * dt)
        dW = rng.standard_normal((n_paths, vols.shape[0])) * np.sqrt(dt)
        grad = np.gradient(f, tau, axis=1)
        f = f + (drift[None, :] + grad) * dt + dW @ vols
        curves.append(f.copy())
    return {"tau": tau, "curves": np.array(curves), "bank": bank, "dt": dt}


def lmm_caplets(L0, delta, sigma, n_paths=50000, seed=0, normal=False) -> dict:
    """A forward-rate market model: forward rates L_i over [T_i, T_i + delta], T_i = i delta, each with its own
    volatility, simulated to each reset under the terminal measure (drifts from the change of numeraire), one
    factor.  Returns the Monte Carlo caplet prices at the money against Black's (or Bachelier's) formula."""
    rng = np.random.default_rng(seed)
    L0 = np.asarray(L0, float)
    n = len(L0)
    sig = np.broadcast_to(np.asarray(sigma, float), (n,)).copy()
    L = np.tile(L0, (n_paths, 1))
    steps = 50
    out_mc = np.zeros(n)
    P0 = np.cumprod(1 / (1 + delta * L0))  # P(0, T_{i+1})
    num = np.ones(n_paths)
    pay = np.zeros((n_paths, n))
    for i in range(n):  # evolve from T_i - delta... to T_i
        dt = delta / steps
        for _ in range(steps):
            dW = rng.standard_normal(n_paths) * np.sqrt(dt)
            new = L.copy()
            for j in range(i, n):
                drift = 0.0
                for k in range(j + 1, n):
                    s_k = sig[k] if normal else sig[k] * L[:, k]
                    drift = drift - delta * s_k / (1 + delta * L[:, k])
                s_j = sig[j] if normal else sig[j] * L[:, j]
                new[:, j] = L[:, j] + s_j * drift * dt + s_j * dW
            L = new
        pay[:, i] = np.maximum(L[:, i] - L0[i], 0) * delta
    # value at 0 under the terminal measure: E[payoff_i / P(T_{i+1}, T_n)] * P(0, T_n)
    PN = np.ones(n_paths)
    for k in range(n):
        PN = PN / (1 + delta * L[:, k])
    PT = np.zeros((n_paths, n))
    for i in range(n):
        # P(T_{i+1}, T_n) from the final forwards (forwards after their reset are frozen at their fixing)
        g = np.ones(n_paths)
        for k in range(i + 1, n):
            g = g / (1 + delta * L[:, k])
        PT[:, i] = g
    mc = (pay / PT).mean(0) * P0[-1]
    Ti = np.arange(1, n + 1) * delta
    exact = np.array([P0[i] * (bachelier(L0[i], L0[i], Ti[i], sig[i]) if normal else
                               black_swaption(L0[i], L0[i], Ti[i], sig[i])) * delta for i in range(n)])
    return {"mc": mc, "exact": exact, "T": Ti}


# ---------------------------------------------------------------------------
# Bond risk premia
# ---------------------------------------------------------------------------
def cochrane_piazzesi(logp_annual) -> dict:
    """Cochrane and Piazzesi (2005) on log zero prices at 1..5 years (rows: months, overlapping annual horizon):
    regress the average of the 2- to 5-year bonds' one-year excess log returns on the 1-year yield and the four
    forward rates; returns gamma (the tent), R^2, and the single factor."""
    p = np.asarray(logp_annual, float)  # (T, 5)
    y1 = -p[:, 0]
    fwd = np.c_[y1, p[:, :-1] - p[:, 1:]]  # f(n-1 -> n), n = 2..5
    rx = np.stack([p[12:, n - 2] - p[:-12, n - 1] - y1[:-12] for n in range(2, 6)], axis=1)
    rbar = rx.mean(1)
    X = np.c_[np.ones(len(rbar)), fwd[:-12]]
    g, *_ = np.linalg.lstsq(X, rbar, rcond=None)
    e = rbar - X @ g
    return {"gamma": g, "r2": float(1 - e.var() / rbar.var()), "factor": fwd @ g[1:] + g[0], "rx": rx, "fwd": fwd}


# ---------------------------------------------------------------------------
# Mortgages: prepayment and negative convexity
# ---------------------------------------------------------------------------
def cpr_scurve(incentive, base=0.06, top=0.45, mid=0.0075, width=0.0035):
    """A stylized annual prepayment rate against the refinancing incentive (the mortgage's coupon minus the current
    mortgage rate): turnover at the bottom, refinancing saturating at the top.  Illustrative, not fitted."""
    return base + (top - base) / (1 + np.exp(-(np.asarray(incentive, float) - mid) / width))


def mbs_price(coupon, rate_shift, base_rate=0.065, T=30, n_paths=400, seed=0, a=0.05, sigma=0.01, spread=0.017):
    """A pass-through paying a fixed mortgage coupon on a balance that amortizes and prepays at :func:`cpr_scurve`
    of (coupon - current mortgage rate), priced by Monte Carlo on Vasicek short rates started at ``base_rate +
    rate_shift`` (the mortgage rate is the short rate plus ``spread``).  Monthly; per 100 of balance.  Illustrative."""
    rng = np.random.default_rng(seed)
    m, dt = 12 * T, 1 / 12
    r = np.full(n_paths, base_rate - spread + rate_shift)
    bal = np.full(n_paths, 100.0)
    disc = np.ones(n_paths)
    pv = np.zeros(n_paths)
    c = coupon / 12
    ann = c / (1 - (1 + c) ** (-m))  # level payment per unit of balance at origination
    mean = base_rate - spread + rate_shift
    for k in range(m):
        rem = m - k
        sched = bal * (c / (1 - (1 + c) ** (-rem)) - c)  # scheduled principal
        cpr = cpr_scurve(coupon - (r + spread))
        smm = 1 - (1 - cpr) ** (1 / 12)
        prep = (bal - sched) * smm
        cf = bal * c + sched + prep
        disc = disc * np.exp(-r * dt)
        pv += cf * disc
        bal = bal - sched - prep
        r = r + a * (mean - r) * dt + sigma * np.sqrt(dt) * rng.standard_normal(n_paths)
    del ann
    return float(pv.mean())
