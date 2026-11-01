"""Delta hedging: run a hedged option book along price paths and account for every dollar.

    out = delta_hedge(t, S, K=100, T=1.0, sigma_hedge=0.2, position=-1, sigma_price=0.2, cost=0.0005,
                      record=[0, 1, 2])
    out["pnl"]                      # final P&L of each path (premium, hedge trades, financing, costs, payoff)
    out["gamma"], out["theta"]      # the cumulative gamma and theta terms of each recorded path

The book holds ``position`` options (+1 long, -1 short), bought or sold at time 0 at the Black–Scholes price with
volatility ``sigma_price`` (default: the hedge volatility), and holds -position x delta shares, delta computed at
``sigma_hedge``, rebalanced every ``hedge_every`` steps.  Cash earns ``r``; the shares pay the carry ``q``; each
share traded costs ``cost`` x its price (a proportional cost: half the bid-ask spread plus fees), including the
first hedge and the unwind at expiry (``cost_ends=False`` charges only the rebalancing trades, as Leland's
formula does).

The accounting identity behind the decomposition: marked at the hedge volatility, the book's P&L over one step is

    dPnL = position x (dV - delta dS - r (V - delta S) dt + q delta S dt)
         ~ position x 1/2 Gamma S^2 [ (dS/S)^2 - sigma_hedge^2 dt ]        (Black–Scholes PDE, Ito)

so ``gamma`` (per recorded path; ``gamma_total`` for all) accumulates position x 1/2 Gamma dS^2, ``theta`` accumulates the rest of the bracket (minus
position x 1/2 Gamma S^2 sigma^2 dt, which at r = q = 0 is exactly theta dt), and ``residual`` is what the second-order
expansion misses (it shrinks as the steps do).  ``edge`` is the time-0 difference between the value at the hedge
volatility and the price paid.
"""

from __future__ import annotations

import numpy as np

from explainer.quant.house import bs


def delta_hedge(t, S, K, T, sigma_hedge, *, cp=1, position=1, r=0.0, q=0.0, sigma_price=None, cost=0.0,
                hedge_every=1, record=None, cost_ends=True) -> dict:
    t = np.asarray(t, float)
    S = np.atleast_2d(np.asarray(S, float))
    n_paths, n1 = S.shape
    n = n1 - 1
    w = float(position)
    sig_p = sigma_hedge if sigma_price is None else sigma_price
    sig_h = np.broadcast_to(np.asarray(sigma_hedge, float), (n_paths,)) if np.ndim(sigma_hedge) else sigma_hedge
    tau = np.maximum(T - t, 0.0)
    rec = np.asarray(record if record is not None else [], int)

    g0 = bs.greeks(S[:, 0], K, tau[0], sig_h, r, q, cp)
    premium = bs.price(S[:, 0], K, tau[0], sig_p, r, q, cp)
    edge = w * (g0["price"] - premium)
    delta = g0["delta"]
    shares = -w * delta
    k_end = cost if cost_ends else 0.0
    cash = -w * premium - shares * S[:, 0] - k_end * np.abs(shares) * S[:, 0]
    v_prev, s_prev, gam_prev = g0["price"], S[:, 0], g0["gamma"]

    mtm = np.zeros(n_paths)
    gam_acc, the_acc, cost_acc = np.zeros(n_paths), np.zeros(n_paths), k_end * np.abs(shares) * S[:, 0]
    series = {k: np.zeros((len(rec), n1)) for k in ("value", "delta", "book", "gamma", "theta", "cost", "shares")}

    def snap(i, value, d):
        if len(rec):
            series["value"][:, i] = value[rec]
            series["delta"][:, i] = d[rec]
            series["book"][:, i] = (edge + mtm - cost_acc)[rec]
            series["gamma"][:, i] = gam_acc[rec]
            series["theta"][:, i] = the_acc[rec]
            series["cost"][:, i] = cost_acc[rec]
            series["shares"][:, i] = shares[rec]

    snap(0, g0["price"], delta)
    for i in range(1, n1):
        dt = t[i] - t[i - 1]
        # cash earns r; the shares held earn (or, held short, pay) the carry q on their value
        cash = cash * np.exp(r * dt) + shares * S[:, i - 1] * q * dt
        gi = bs.greeks(S[:, i], K, tau[i], sig_h, r, q, cp)
        dS = S[:, i] - s_prev
        step = w * (gi["price"] - v_prev - delta * dS - r * (v_prev - delta * s_prev) * dt + q * delta * s_prev * dt)
        mtm += step
        g_term = w * 0.5 * gam_prev * dS ** 2
        gam_acc += g_term
        the_acc += -w * 0.5 * gam_prev * s_prev ** 2 * np.square(sig_h) * dt
        if i % hedge_every == 0 or i == n:
            new_delta = gi["delta"] if i < n else delta  # at expiry the hedge is unwound below
            if i < n:
                trade = -w * new_delta - shares
                cash -= trade * S[:, i] + cost * np.abs(trade) * S[:, i]
                cost_acc += cost * np.abs(trade) * S[:, i]
                shares = shares + trade
                delta = new_delta
        v_prev, s_prev, gam_prev = gi["price"], S[:, i], gi["gamma"]
        snap(i, gi["price"], delta)
    # expiry: settle the option and unwind the shares
    payoff = np.maximum(cp * (S[:, -1] - K), 0.0) if tau[-1] <= 0 else bs.price(S[:, -1], K, tau[-1], sig_h, r, q, cp)
    unwind_cost = k_end * np.abs(shares) * S[:, -1]
    cash += shares * S[:, -1] - unwind_cost
    cost_acc += unwind_cost
    pnl = cash + w * payoff
    out = {
        "pnl": pnl,
        "edge": edge,
        "mtm": mtm,
        "gamma_total": gam_acc,
        "theta_total": the_acc,
        "cost_total": cost_acc,
        "residual_total": mtm - gam_acc - the_acc,
        "premium": premium,
    }
    if len(rec):
        series["book"][:, -1] = pnl[rec] * np.exp(-r * (t[-1] - t[0]))  # the last mark is the settled P&L
        series["cost"][:, -1] = cost_acc[rec]
        out.update(series)
    return out
