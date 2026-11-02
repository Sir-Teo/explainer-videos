"""The options quoting engine (Part 11, the volatility desk's tools): positions as Greeks, strategy P&L surfaces, the
gamma-theta trade-off, implied correlation, quotes skewed by inventory, and hedging bands under costs.  Tested in
``tests/test_quant_house.py``.

* ``Leg``, ``book_value``, ``book_greeks``: a book of options as a sum of legs, valued and risk-measured at once;
* ``pnl_surface``: the book's P&L over a grid of spot moves and implied-volatility moves after a holding period;
* ``STRATEGIES``: the standard structures (straddle, strangle, risk reversal, butterfly, call spread, calendar);
* ``implied_correlation``: the average pairwise correlation that makes an index's implied variance consistent with
  its components' (the dispersion trade's quantity);
* ``quote``: a market maker's bid and ask in volatility, centred on a fair value and skewed against inventory in vega
  (an Avellaneda-Stoikov style rule);
* ``ww_band``: Whalley and Wilmott's (1997) no-trade band around the Black-Scholes delta under proportional costs.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from explainer.quant.house import bs


@dataclass
class Leg:
    cp: int        # +1 call, -1 put
    K: float
    T: float       # years to expiry at time 0
    qty: float     # + long, - short


def book_value(legs, S, sigma, t=0.0, r=0.0):
    """The book's value at spot ``S`` (array ok), implied volatility ``sigma`` (a number, or one per leg), elapsed
    time ``t``."""
    S = np.asarray(S, float)
    sig = np.broadcast_to(np.asarray(sigma, float), (len(legs),)) if np.ndim(sigma) else [sigma] * len(legs)
    v = np.zeros_like(S)
    for leg, s in zip(legs, sig):
        v = v + leg.qty * bs.price(S, leg.K, max(leg.T - t, 0.0), s, r, 0.0, leg.cp)
    return v


def book_greeks(legs, S, sigma, t=0.0, r=0.0) -> dict:
    out = {k: 0.0 for k in ("price", "delta", "gamma", "vega", "theta", "vanna", "volga")}
    for leg in legs:
        g = bs.greeks(S, leg.K, max(leg.T - t, 0.0), sigma, r, 0.0, leg.cp)
        for k in out:
            out[k] = out[k] + leg.qty * g[k]
    return out


def pnl_surface(legs, S0, sigma0, dS, dvol, dt, r=0.0) -> np.ndarray:
    """P&L of the book (not delta-hedged) over a grid of relative spot moves ``dS`` and implied-vol moves ``dvol``
    after ``dt`` years: rows are vol moves, columns spot moves."""
    v0 = book_value(legs, S0, sigma0, 0.0, r)
    out = np.empty((len(dvol), len(dS)))
    for i, dv in enumerate(dvol):
        out[i] = book_value(legs, S0 * (1 + np.asarray(dS)), max(sigma0 + dv, 1e-4), dt, r) - v0
    return out


def strategies(S0=100.0, T=0.25, width=0.1) -> dict:
    """The standard structures, long one unit each, at spot ``S0``."""
    lo, hi = S0 * (1 - width), S0 * (1 + width)
    return {
        "straddle": [Leg(1, S0, T, 1), Leg(-1, S0, T, 1)],
        "strangle": [Leg(1, hi, T, 1), Leg(-1, lo, T, 1)],
        "risk reversal": [Leg(1, hi, T, 1), Leg(-1, lo, T, -1)],
        "butterfly": [Leg(1, lo, T, 1), Leg(1, S0, T, -2), Leg(1, hi, T, 1)],
        "call spread": [Leg(1, S0, T, 1), Leg(1, hi, T, -1)],
        "calendar": [Leg(1, S0, 2 * T, 1), Leg(1, S0, T, -1)],
    }


# ---------------------------------------------------------------------------
def implied_correlation(index_vol, weights, vols) -> float:
    """rho such that sigma_I^2 = sum w_i^2 s_i^2 + rho sum_{i != j} w_i w_j s_i s_j."""
    w, s = np.asarray(weights, float), np.asarray(vols, float)
    own = np.sum(w ** 2 * s ** 2)
    cross = np.sum(w * s) ** 2 - own
    return float((index_vol ** 2 - own) / cross)


def quote(fair_vol, inventory_vega, half_spread=0.01, skew_per_vega=0.002, vega_limit=None) -> dict:
    """Bid and ask in implied volatility around ``fair_vol``, shifted against the book's vega inventory: long vega,
    quote lower (to sell, not buy); short vega, quote higher.  Outside a vega limit, quote one side only."""
    mid = fair_vol - skew_per_vega * inventory_vega
    bid, ask = mid - half_spread, mid + half_spread
    if vega_limit is not None and inventory_vega >= vega_limit:
        bid = np.nan
    if vega_limit is not None and inventory_vega <= -vega_limit:
        ask = np.nan
    return {"bid": bid, "ask": ask, "mid": mid}


def ww_band(S, K, T, sigma, cost, gamma_risk=1.0, r=0.0, cp=1) -> dict:
    """Whalley and Wilmott's asymptotic no-trade band for a short option hedged under proportional cost ``cost``:
    delta +/- (3 cost S Gamma^2 / (2 gamma_risk))^(1/3), with ``gamma_risk`` the hedger's risk aversion."""
    g = bs.greeks(S, K, T, sigma, r, 0.0, cp)
    h = (1.5 * cost * S * g["gamma"] ** 2 * np.exp(-r * T) / gamma_risk) ** (1 / 3)
    return {"delta": g["delta"], "lo": g["delta"] - h, "hi": g["delta"] + h, "half_width": h}


def hedge_with_band(t, S, K, T, sigma, cost, band_half=None, gamma_risk=1.0, position=-1, cp=1) -> dict:
    """Run a short (``position`` = -1) option hedged only when the delta leaves a band (Whalley-Wilmott if
    ``band_half`` is None, a fixed half-width otherwise; 0 means rehedge every step).  Returns the P&L per path,
    the trading cost, and the number of trades."""
    t = np.asarray(t, float)
    S = np.atleast_2d(np.asarray(S, float))
    n_paths, n1 = S.shape
    tau = np.maximum(T - t, 1e-12)
    prem = bs.price(S[:, 0], K, T, sigma, 0.0, 0.0, cp)
    g0 = bs.greeks(S[:, 0], K, tau[0], sigma, 0.0, 0.0, cp)
    shares = -position * g0["delta"]
    cash = -position * prem - shares * S[:, 0] - cost * np.abs(shares) * S[:, 0]
    costs = cost * np.abs(shares) * S[:, 0]
    trades = np.ones(n_paths)
    for i in range(1, n1 - 1):
        g = bs.greeks(S[:, i], K, tau[i], sigma, 0.0, 0.0, cp)
        target = -position * g["delta"]
        if band_half is None:
            hw = (1.5 * cost * S[:, i] * g["gamma"] ** 2 / gamma_risk) ** (1 / 3)
        else:
            hw = np.full(n_paths, band_half)
        out = np.abs(shares - target) > hw
        # move to the nearest edge of the band (Whalley-Wilmott), or to the target with no band
        new = np.where(out, np.where(shares < target, target - hw, target + hw), shares)
        d = new - shares
        cash = cash - d * S[:, i] - cost * np.abs(d) * S[:, i]
        costs = costs + cost * np.abs(d) * S[:, i]
        trades = trades + out
        shares = new
    payoff = np.maximum(cp * (S[:, -1] - K), 0.0)
    pnl = cash + shares * S[:, -1] - cost * np.abs(shares) * S[:, -1] + position * payoff
    costs = costs + cost * np.abs(shares) * S[:, -1]
    return {"pnl": pnl, "cost": costs, "trades": trades}
