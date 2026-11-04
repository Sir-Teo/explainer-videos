"""The House's rates desk (Part 18, *Money, Bonds and the Curve*): the curve builder every later rates, credit and
macro part prices off, and the desk's first tools.

* :func:`bond_price`, :func:`bond_yield`, :func:`bond_risk`: a fixed-coupon bullet bond on a coupon date: price per
  100 from a yield, the yield from a price, and its Macaulay and modified duration, convexity and DV01;
* :class:`Curve`: discount factors from zero rates at nodes, interpolated linearly in ``r(t) * t`` (piecewise-flat
  forwards); zero, forward and par rates off it;
* :func:`bootstrap_par`: the curve that reprices a set of par bonds exactly, node by node;
* :func:`nss`, :func:`fit_nss`: the Nelson-Siegel(-Svensson) yield curve and its least-squares fit;
* :func:`curve_pca`: principal components of daily curve changes (level, slope, curvature);
* :func:`fly_weights`: a butterfly whose wings neutralize chosen components;
* :func:`key_rate_dv01`: the sensitivity of a set of cash flows to a 1 bp bump of each key rate;
* :func:`par_swap_rate`, :func:`swap_value`: a fixed-for-floating swap off a single curve;
* :func:`conversion_factor`: the CBOT conversion factor of a deliverable note or bond (the 6% notional coupon);
* :func:`compound_in_arrears`: a SOFR period rate compounded in arrears from the daily fixings;
* :func:`taylor_rule`: Taylor's (1993) rule for the policy rate;
* :func:`ldi_spiral`: a leveraged liability hedge selling into its own price impact (Part 18's gilt chapter).

Rates are decimals (0.04 is 4%) unless a docstring says percent.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq, least_squares


# ---------------------------------------------------------------------------
# A bond on a coupon date
# ---------------------------------------------------------------------------
def _flows(coupon: float, T: float, freq: int = 2):
    n = max(int(round(T * freq)), 1)
    t = np.arange(1, n + 1) / freq
    cf = np.full(n, 100 * coupon / freq)
    cf[-1] += 100
    return t, cf


def bond_price(coupon: float, y: float, T: float, freq: int = 2) -> float:
    """Price per 100 of a bullet bond with ``T`` years left (a whole number of periods), coupon ``coupon`` a year paid
    ``freq`` times, at yield ``y`` compounded ``freq`` times a year."""
    t, cf = _flows(coupon, T, freq)
    return float(np.sum(cf * (1 + y / freq) ** (-freq * t)))


def bond_yield(price: float, coupon: float, T: float, freq: int = 2) -> float:
    """The yield that gives ``price``: the root of a decreasing function, found by bisection-safe Brent."""
    return float(brentq(lambda y: bond_price(coupon, y, T, freq) - price, -0.5, 2.0, xtol=1e-14))


def bond_risk(coupon: float, y: float, T: float, freq: int = 2) -> dict:
    """``price``, ``macaulay`` (the PV-weighted average time of the cash flows, years), ``modified`` (-dP/dy / P),
    ``convexity`` (d2P/dy2 / P) and ``dv01`` (the price change per 100 for a 1 bp fall in yield)."""
    t, cf = _flows(coupon, T, freq)
    v = 1 + y / freq
    pv = cf * v ** (-freq * t)
    P = pv.sum()
    mac = float(np.sum(t * pv) / P)
    mod = mac / v
    conv = float(np.sum(pv * t * (t + 1 / freq)) / (P * v ** 2))
    return {"price": float(P), "macaulay": mac, "modified": mod, "convexity": conv, "dv01": mod * P * 1e-4}


# ---------------------------------------------------------------------------
# The curve
# ---------------------------------------------------------------------------
class Curve:
    """Zero rates ``z`` (continuously compounded) at times ``t`` (years); between nodes ``z(t) * t`` is linear, so
    the instantaneous forward is flat on each interval; before the first node the first rate holds, beyond the last
    the last forward does."""

    def __init__(self, t, z):
        self.t = np.asarray(t, float)
        self.z = np.asarray(z, float)

    def _rt(self, s):
        s = np.asarray(s, float)
        rt = self.z * self.t
        out = np.interp(s, self.t, rt)
        lo = s < self.t[0]
        out = np.where(lo, self.z[0] * s, out)
        if len(self.t) > 1:
            f_last = (rt[-1] - rt[-2]) / (self.t[-1] - self.t[-2])
            out = np.where(s > self.t[-1], rt[-1] + f_last * (s - self.t[-1]), out)
        return out

    def df(self, s):
        return np.exp(-self._rt(s))

    def zero(self, s):
        s = np.asarray(s, float)
        return self._rt(s) / np.maximum(s, 1e-12)

    def fwd(self, a, b):
        """The continuously compounded forward rate from ``a`` to ``b``."""
        return (self._rt(b) - self._rt(a)) / (np.asarray(b, float) - np.asarray(a, float))

    def inst_fwd(self, s, h=1e-4):
        s = np.asarray(s, float)
        return (self._rt(s + h) - self._rt(np.maximum(s - h, 0))) / (s + h - np.maximum(s - h, 0))

    def par(self, T, freq: int = 2):
        """The coupon that prices a ``T``-year bullet bond at par off this curve."""
        t = np.arange(1, int(round(T * freq)) + 1) / freq
        d = self.df(t)
        return float(freq * (1 - d[-1]) / d.sum())

    def price(self, t, cf) -> float:
        return float(np.sum(np.asarray(cf, float) * self.df(t)))


def bootstrap_par(tenors, par, freq: int = 2) -> Curve:
    """The curve that reprices each par bond exactly.  Tenors of a year or less are single payments at their
    coupon-equivalent yield, ``(1 + y/2)^(-2t)``, as Treasury quotes bills; longer tenors pay coupons ``freq`` times a
    year, and each new node's zero rate is the one that prices that bond at 100, the coupons between known nodes read
    off the interpolated curve built so far."""
    T = np.asarray(tenors, float)
    y = np.asarray(par, float)
    ts, zs = [], []
    for Ti, yi in zip(T, y):
        if Ti <= 1.0 + 1e-9:
            ts.append(Ti)
            zs.append(2 * np.log1p(yi / 2))
            continue
        t, cf = _flows(yi, Ti, freq)

        def miss(z):
            c = Curve(ts + [Ti], zs + [z])
            return c.price(t, cf) - 100.0
        zs.append(float(brentq(miss, -0.2, 0.5, xtol=1e-14)))
        ts.append(Ti)
    return Curve(ts, zs)


# ---------------------------------------------------------------------------
# Nelson-Siegel-Svensson
# ---------------------------------------------------------------------------
def nss_loadings(t, tau1: float, tau2: float | None = None):
    """The level, slope, curvature (and Svensson's second hump) loadings at maturities ``t``: columns of the
    regression that is linear in the betas once the taus are fixed."""
    t = np.maximum(np.asarray(t, float), 1e-9)
    x1 = t / tau1
    a = (1 - np.exp(-x1)) / x1
    cols = [np.ones_like(t), a, a - np.exp(-x1)]
    if tau2 is not None:
        x2 = t / tau2
        cols.append((1 - np.exp(-x2)) / x2 - np.exp(-x2))
    return np.stack(cols, axis=-1)


def nss(t, beta, tau) -> np.ndarray:
    """The Nelson-Siegel (``len(beta) == 3``) or Svensson (4 betas, 2 taus) zero yield at ``t``, in the units of the
    betas; the Fed's GSW file gives betas in percent and continuously compounded yields."""
    beta = np.asarray(beta, float)
    L = nss_loadings(t, tau[0], tau[1] if len(beta) == 4 else None)
    return L @ beta


def fit_nss(t, y, svensson: bool = True, taus=None) -> dict:
    """Least-squares Nelson-Siegel(-Svensson) fit to zero yields ``y`` at ``t``: for each pair of taus on a grid the
    betas are a linear regression; the best pair seeds a joint non-linear polish.  Returns ``beta``, ``tau``, the
    fitted ``yhat`` and the ``rmse``."""
    t = np.asarray(t, float)
    y = np.asarray(y, float)
    grid = taus if taus is not None else np.geomspace(0.3, 30, 25)
    best = None
    pairs = [(a, b) for a in grid for b in grid if b > a * 1.5] if svensson else [(a, None) for a in grid]
    for a, b in pairs:
        L = nss_loadings(t, a, b)
        beta, *_ = np.linalg.lstsq(L, y, rcond=None)
        r = float(np.sum((L @ beta - y) ** 2))
        if best is None or r < best[0]:
            best = (r, beta, a, b)
    _, beta, a, b = best
    k = len(beta)

    def res(p):
        tau = (np.exp(p[k]), np.exp(p[k + 1]) if svensson else None)
        return nss_loadings(t, *tau) @ p[:k] - y
    p0 = np.r_[beta, np.log(a), np.log(b)] if svensson else np.r_[beta, np.log(a)]
    sol = least_squares(res, p0, method="lm", xtol=1e-12, ftol=1e-12, max_nfev=4000)
    p = sol.x
    tau = (float(np.exp(p[k])), float(np.exp(p[k + 1]))) if svensson else (float(np.exp(p[k])),)
    yhat = nss(t, p[:k], tau if svensson else (tau[0], None))
    return {"beta": p[:k], "tau": tau, "yhat": yhat, "rmse": float(np.sqrt(np.mean((yhat - y) ** 2)))}


# ---------------------------------------------------------------------------
# Factors, flies and key rates
# ---------------------------------------------------------------------------
def curve_pca(dy) -> dict:
    """Principal components of curve changes ``dy`` (days, maturities): ``loadings`` (components, maturities; each
    unit length, signed so the level loads positively and the slope rises with maturity), the ``share`` of variance
    each explains, and the daily ``scores``."""
    X = np.asarray(dy, float)
    X = X - X.mean(axis=0)
    C = np.cov(X, rowvar=False)
    w, V = np.linalg.eigh(C)
    o = np.argsort(w)[::-1]
    w, V = w[o], V[:, o]
    if V[:, 0].sum() < 0:
        V[:, 0] *= -1
    if V.shape[1] > 1 and V[-1, 1] - V[0, 1] < 0:
        V[:, 1] *= -1
    if V.shape[1] > 2 and V[len(V) // 2, 2] < 0.5 * (V[0, 2] + V[-1, 2]):
        V[:, 2] *= -1
    return {"loadings": V.T, "share": w / w.sum(), "scores": X @ V, "var": w}


def fly_weights(loadings, legs, neutral=(0, 1)) -> np.ndarray:
    """DV01 weights on the three maturities ``legs`` (indices into the loadings' columns): +1 on the belly, and wings
    chosen so the trade has no exposure to the components in ``neutral`` (by default level and slope)."""
    L = np.asarray(loadings, float)[list(neutral)][:, list(legs)]  # components x legs
    wings = np.linalg.solve(L[:, [0, 2]], -L[:, 1])
    return np.array([wings[0], 1.0, wings[1]])


def key_rate_dv01(t, cf, curve: Curve, keys) -> np.ndarray:
    """The value change of cash flows ``cf`` at ``t`` when the zero curve is bumped down 1 bp in a triangle centred on
    each key rate (zero at the neighbouring keys, flat beyond the ends): the bumps sum to a parallel 1 bp, so the key
    rate DV01s sum to the parallel DV01."""
    keys = np.asarray(keys, float)
    t = np.asarray(t, float)
    base = curve.price(t, cf)
    out = []
    for i, k in enumerate(keys):
        e = np.zeros(len(keys))
        e[i] = 1.0

        def bump(s):
            return np.interp(s, keys, e)
        df = curve.df(t) * np.exp(bump(t) * 1e-4 * t)
        out.append(float(np.sum(np.asarray(cf) * df) - base))
    return np.array(out)


# ---------------------------------------------------------------------------
# Swaps, futures, SOFR, policy
# ---------------------------------------------------------------------------
def par_swap_rate(curve: Curve, T: float, freq: int = 1) -> float:
    """The fixed rate of a ``T``-year swap paying ``freq`` times a year against the floating rate, valued off one
    curve: the floating leg is worth 1 - P(T), so the par rate is (1 - P(T)) / annuity."""
    t = np.arange(1, int(round(T * freq)) + 1) / freq
    d = curve.df(t)
    return float((1 - d[-1]) / (d.sum() / freq))


def swap_value(curve: Curve, T: float, fixed: float, freq: int = 1, notional: float = 1.0) -> float:
    """Value to the fixed-rate receiver: fixed leg minus floating leg."""
    t = np.arange(1, int(round(T * freq)) + 1) / freq
    d = curve.df(t)
    return float(notional * (fixed * d.sum() / freq - (1 - d[-1])))


def conversion_factor(coupon: float, years: int, months: int, product: str = "10y") -> float:
    """The CBOT conversion factor: the price per 1 of the deliverable at a 6% yield, with time to maturity cut down to
    whole quarters ("10y", T-note and bond futures) or whole months ("2y", "3y", "5y"), as CME publishes it.
    ``coupon`` decimal; ``years`` and ``months`` the remaining term from the first day of the delivery month."""
    n = years
    z = months - months % 3 if product == "10y" else months
    v = z if z < 7 else (3 if product == "10y" else z - 6)
    a = 1 / 1.03 ** (v / 6)
    b = coupon / 2 * (6 - v) / 6
    c = 1 / 1.03 ** (2 * n) if z < 7 else 1 / 1.03 ** (2 * n + 1)
    d = coupon / 0.06 * (1 - c)
    return float(round(a * (coupon / 2 + c + d) - b, 4))


def compound_in_arrears(rates, days) -> float:
    """A period rate from overnight fixings (decimal) each applying for ``days[i]`` calendar days, ACT/360, as SOFR
    is compounded in arrears: (prod(1 + r_i d_i / 360) - 1) * 360 / sum(d_i)."""
    r = np.asarray(rates, float)
    d = np.asarray(days, float)
    return float((np.prod(1 + r * d / 360) - 1) * 360 / d.sum())


def taylor_rule(inflation, gap, r_star: float = 2.0, pi_star: float = 2.0):
    """Taylor (1993), percent: i = r* + pi + 0.5 (pi - pi*) + 0.5 gap; his own numbers were r* = pi* = 2."""
    p = np.asarray(inflation, float)
    return r_star + p + 0.5 * (p - pi_star) + 0.5 * np.asarray(gap, float)


# ---------------------------------------------------------------------------
# A leveraged liability hedge in a falling market
# ---------------------------------------------------------------------------
def ldi_spiral(shock_bp: float, leverage: float = 3.0, duration: float = 20.0, impact_bp_per_pct: float = 1.0,
               buffer: float | None = None, rounds: int = 30) -> dict:
    """A pension fund's leveraged LDI pool: assets ``leverage`` x NAV in long gilts (and repo or swaps) of modified
    duration ``duration``, NAV 1.  A yield shock cuts the NAV by leverage x duration x dy; the manager restores the
    pool's ``buffer`` (the yield rise it can absorb before NAV is gone, in percentage points; by default the one it
    started with, 100 / (leverage x duration)) by selling gilts and repaying the borrowing, and
    every 1% of the pool's assets sold pushes yields up ``impact_bp_per_pct`` more.  Returns the yield path (bp), NAV
    and the gilts sold each round; the spiral stops when the extra rise is under 0.1 bp, or NAV hits zero."""
    nav, assets, dy_total = 1.0, leverage, 0.0
    buf = (buffer if buffer is not None else 100.0 / (leverage * duration)) * 1e-2
    dy = shock_bp
    path, navs, sold = [0.0], [nav], [0.0]
    for _ in range(rounds):
        nav -= assets * duration * dy * 1e-4
        assets *= 1 - duration * dy * 1e-4
        dy_total += dy
        path.append(dy_total)
        navs.append(max(nav, 0.0))
        if nav <= 0:
            sold.append(0.0)
            break
        # the buffer is nav / (assets x duration) in yield terms: restore it by cutting assets
        target_assets = nav / (duration * buf)
        sell = max(assets - target_assets, 0.0)
        sold.append(sell)
        dy = impact_bp_per_pct * 100 * sell / max(assets, 1e-12)
        assets -= sell
        if dy < 0.1:
            break
    return {"dy_bp": np.array(path), "nav": np.array(navs), "sold": np.array(sold)}
