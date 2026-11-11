"""Crypto and decentralised finance (Part 39): automated market makers, their liquidity providers' losses to
arbitrage, ordering attacks, perpetual futures and stablecoin runs.

* Constant-function market makers. A constant-product pool (Uniswap v2) holds x of a risky asset X and y of a
  numeraire with x y = k; its price is y/x. A concentrated position (Uniswap v3) of liquidity L on [pa, pb] holds
  x = L(1/sqrt(P) - 1/sqrt(pb)) and y = L(sqrt(P) - sqrt(pa)) inside the range.
* Loss-versus-rebalancing (Milionis, Moallemi, Roughgarden and Zhang 2022): the pool's value against a portfolio that
  holds the same amount of X but trades at the market price. For a pool whose holdings x(P) are decreasing,
  LVR accrues at (sigma^2 P^2 / 2) |x'(P)| per unit time: sigma^2 V / 8 for a constant-product pool. In discrete time
  the constant-product loss over one step is exactly (V / 2)(sqrt(P1/P0) - 1)^2.
* Fees and blocks (Milionis, Moallemi and Roughgarden 2023): a fee gamma keeps the pool price within a band around
  the market price, and arbitrageurs trade only in some blocks.
* Sandwich attacks: a front-run, the victim's trade at its slippage limit, and a back-run.
* Perpetual futures: with funding kappa (F - S) paid continuously by longs, the no-arbitrage price is
  F = kappa S / (kappa - (r - q)) (He, Manela, Ross and von Wachter 2022, in continuous form)."""

from __future__ import annotations

import math

import numpy as np


# ---------------------------------------------------------------------------
# Constant-product and concentrated liquidity
# ---------------------------------------------------------------------------
def cpmm_reserves(k: float, P):
    """Reserves (x, y) of a constant-product pool x y = k at pool price P = y / x."""
    P = np.asarray(P, float)
    return np.sqrt(k / P), np.sqrt(k * P)


def cpmm_value(k: float, P):
    """Pool value at price P (marked at its own price): x P + y = 2 sqrt(k P)."""
    return 2 * np.sqrt(k * np.asarray(P, float))


def cpmm_swap(x: float, y: float, dx: float, fee: float = 0.0) -> tuple[float, float, float]:
    """Sell ``dx`` of X into a constant-product pool (``dx`` < 0 buys X, paying Y). The fee is taken on the input and
    kept outside the curve. Returns (dy received by the trader, new x, new y); dy < 0 means Y paid."""
    k = x * y
    if dx >= 0:
        x1 = x + (1 - fee) * dx
        y1 = k / x1
        return y - y1, x1, y1
    # buying |dx| of X: the trader pays Y, of which the fee share stays outside the curve
    x1 = x + dx
    y1 = k / x1
    return -(y1 - y) / (1 - fee), x1, y1


def impermanent_loss(r):
    """A constant-product position against holding its initial assets, after the price moves by a factor r:
    2 sqrt(r) / (1 + r) - 1 (no fees)."""
    r = np.asarray(r, float)
    return 2 * np.sqrt(r) / (1 + r) - 1


def v3_reserves(L: float, P, pa: float, pb: float):
    """Holdings of a concentrated position of liquidity L on [pa, pb] at pool price P: all X below pa, all Y
    above pb."""
    P = np.clip(np.asarray(P, float), pa, pb)
    return L * (1 / np.sqrt(P) - 1 / np.sqrt(pb)), L * (np.sqrt(P) - np.sqrt(pa))


def v3_value(L: float, p, pa: float, pb: float):
    """The position's value at market price p, with the pool arbitraged to p."""
    x, y = v3_reserves(L, p, pa, pb)
    return x * np.asarray(p, float) + y


def v3_efficiency(w: float) -> float:
    """Capital efficiency of a range [P / w, P w] centred (geometrically) on P, against a constant-product position of
    the same value: 1 / (1 - w^(-1/2))."""
    return 1.0 / (1.0 - w ** -0.5)


def lvr_rate_cpmm(sigma: float, V):
    """Instantaneous LVR of a constant-product pool of value V with volatility sigma (per unit time)."""
    return sigma ** 2 / 8 * np.asarray(V, float)


def lvr_rate_v3(sigma: float, L: float, P, pa: float, pb: float):
    """Instantaneous LVR of a concentrated position: sigma^2 L sqrt(P) / 4 inside the range, zero outside."""
    P = np.asarray(P, float)
    return np.where((P > pa) & (P < pb), sigma ** 2 * L * np.sqrt(P) / 4, 0.0)


def lvr_step_cpmm(V0, p0, p1):
    """The exact constant-product loss against rebalancing over one step from p0 to p1, with the pool arbitraged to
    p1 and no fees: (V0 / 2)(sqrt(p1 / p0) - 1)^2."""
    return np.asarray(V0, float) / 2 * (np.sqrt(np.asarray(p1, float) / np.asarray(p0, float)) - 1) ** 2


# ---------------------------------------------------------------------------
# A pool against arbitrageurs
# ---------------------------------------------------------------------------
def arb_pool(prices, fee: float = 0.0, k: float = 1.0, L: float | None = None, pa: float | None = None,
             pb: float | None = None) -> dict:
    """Run a pool against a market price path ``prices`` (one entry per block). In each block an arbitrageur trades
    the pool to the edge of its no-arbitrage band: the pool price P is moved to p / (1 - fee) if the arbitrageur sells
    X (when (1 - fee) P > p) or to p (1 - fee) if it buys X (when P < (1 - fee) p); the fee on the input is paid to the
    LP outside the curve. A constant-product pool by default; with ``L``, ``pa``, ``pb`` a concentrated position.
    Returns, per block, the LP's value (curve holdings at the market price, plus fees), the rebalancing portfolio's
    value (holding the pool's X at each step, trading at market prices), the accumulated LVR (rebalancing minus curve
    value, fees excluded), fee income, the arbitrage profit, and the share of blocks with a trade."""
    p = np.asarray(prices, float)
    n = len(p)
    if L is None:
        res = lambda P: cpmm_reserves(k, P)  # noqa: E731
    else:
        res = lambda P: v3_reserves(L, P, pa, pb)  # noqa: E731
    P = p[0]
    x, y = (float(v) for v in res(P))
    V0 = x * p[0] + y
    rebal = V0
    fees = 0.0
    arb = 0.0
    trades = 0
    lp = np.empty(n)
    rb = np.empty(n)
    lv = np.empty(n)
    fe = np.empty(n)
    lp[0], rb[0], lv[0], fe[0] = V0, V0, 0.0, 0.0
    g = 1.0 - fee
    for t in range(1, n):
        rebal += x * (p[t] - p[t - 1])
        if g * P > p[t]:
            P1 = p[t] / g
        elif P < g * p[t]:
            P1 = p[t] * g
        else:
            P1 = P
        if L is not None:
            P1 = min(max(P1, pa), pb)
        if P1 != P:
            x1, y1 = (float(v) for v in res(P1))
            dx, dy = x1 - x, y1 - y
            if dx > 0:       # arbitrageur sold X into the pool; fee on X input
                f_ = dx / g - dx
                fees += f_ * p[t]
                arb += -dy - (dx / g) * p[t]
            elif dx < 0:     # arbitrageur bought X; paid Y plus fee
                f_ = dy / g - dy
                fees += f_
                arb += -dx * p[t] - dy / g
            trades += 1
            x, y, P = x1, y1, P1
        curve = x * p[t] + y
        lp[t] = curve + fees
        rb[t] = rebal
        lv[t] = rebal - curve
        fe[t] = fees
    return {"lp": lp, "rebal": rb, "lvr": lv, "fees": fe, "arb": float(arb), "p_trade": trades / max(n - 1, 1),
            "V0": float(V0)}


def p_trade_theory(fee: float, sigma: float, dt: float) -> float:
    """Milionis, Moallemi and Roughgarden's (2023) leading-order probability that a block of length dt holds an
    arbitrage trade, for a constant-product pool with fee gamma and volatility sigma: 1 / (1 + gamma sqrt(2/dt) /
    sigma), with blocks arriving as a Poisson process of rate 1/dt."""
    return 1.0 / (1.0 + fee * math.sqrt(2.0 / dt) / sigma)


# ---------------------------------------------------------------------------
# Ordering: a sandwich
# ---------------------------------------------------------------------------
def sandwich(x: float, y: float, dy_in: float, slippage: float, fee: float = 0.003, iters: int = 80) -> dict:
    """A victim buys X with ``dy_in`` of Y, accepting at least (1 - slippage) of the X it was quoted. An attacker
    buys X first with ``a`` of Y, lets the victim trade, then sells its X back. The largest ``a`` that keeps the victim
    within its limit is found by bisection. Returns the attacker's Y profit, the front-run size, the victim's
    shortfall in X, and what the victim would have received unattacked."""
    def buy_x(xx, yy, dy):            # pay dy of Y for X; fee on input stays outside the curve
        k = xx * yy
        y1 = yy + (1 - fee) * dy
        x1 = k / y1
        return xx - x1, x1, y1

    def sell_x(xx, yy, dx):
        k = xx * yy
        x1 = xx + (1 - fee) * dx
        y1 = k / x1
        return yy - y1, x1, y1

    quote, _, _ = buy_x(x, y, dy_in)
    need = (1 - slippage) * quote

    def run(a):
        got_a, x1, y1 = buy_x(x, y, a)
        got_v, x2, y2 = buy_x(x1, y1, dy_in)
        back, _, _ = sell_x(x2, y2, got_a)
        return got_v, back - a

    lo, hi = 0.0, 100.0 * dy_in
    if run(hi)[0] >= need:
        lo = hi
    else:
        for _ in range(iters):
            mid = 0.5 * (lo + hi)
            if run(mid)[0] >= need:
                lo = mid
            else:
                hi = mid
    got_v, prof = run(lo)
    return {"front": lo, "profit": prof, "victim_got": got_v, "quote": quote, "shortfall": quote - got_v}


# ---------------------------------------------------------------------------
# Perpetual futures
# ---------------------------------------------------------------------------
def perp_multiplier(kappa: float, r: float, q: float = 0.0) -> float:
    """F / S for a perpetual whose longs pay funding kappa (F - S) continuously, when cash earns r and the asset can
    be lent at q: kappa / (kappa - (r - q)). Requires kappa > r - q."""
    return kappa / (kappa - (r - q))


def binance_funding_rule(premium, interest: float = 1e-4, clamp: float = 5e-4):
    """Binance's published funding formula for a USD-margined perpetual (per 8 hours): the average premium index P
    plus clamp(interest - P, -clamp, +clamp). Inside |P - interest| < clamp the rate is exactly the interest rate,
    0.01%."""
    premium = np.asarray(premium, float)
    return premium + np.clip(interest - premium, -clamp, clamp)
