"""The House's treasury and funding desk (Part 2, *The Machinery of Markets*): what it costs, in cash and collateral,
to hold a position, and what the market's plumbing does with an order.  Every later backtest charges these.

* :func:`margin_account`: a leveraged futures or perpetual position marked to market bar by bar, with variation
  margin, funding payments and the exchange's liquidation rule;
* :func:`netting`: what a central counterparty saves: gross, bilateral-net and multilateral-net obligations of a
  set of trades;
* :func:`call_auction`: the single clearing price of an opening or closing auction (the price that executes the most);
* :func:`fund_fees`: management and performance fees with a high-water mark, period by period;
* :func:`max_leverage`: the leverage a repo or margin haircut allows.
"""

from __future__ import annotations

import numpy as np


def margin_account(prices, qty: float, leverage: float, maintenance: float, funding=None, fee: float = 0.0) -> dict:
    """A position of ``qty`` units (negative: short) opened at ``prices[0]`` with initial margin notional / leverage.
    Each bar the account gains qty * dP (variation margin) and pays ``funding[i]`` * notional (positive funding:
    longs pay shorts).  Liquidated at the first bar where equity < ``maintenance`` * notional: the account is closed
    at that bar's price, and whatever equity is left (possibly negative, absorbed by the exchange's insurance fund) is
    reported.  ``fee``: a trading fee per unit of notional, paid on opening."""
    p = np.asarray(prices, float)
    n = len(p)
    f = np.zeros(n) if funding is None else np.asarray(funding, float)
    notional0 = abs(qty) * p[0]
    margin0 = notional0 / leverage
    equity = np.empty(n)
    equity[0] = margin0 - fee * notional0
    paid_funding = 0.0
    liq = None
    for i in range(1, n):
        pay = f[i] * qty * p[i - 1]
        paid_funding += pay
        equity[i] = equity[i - 1] + qty * (p[i] - p[i - 1]) - pay
        if equity[i] < maintenance * abs(qty) * p[i]:
            liq = i
            equity[i + 1:] = np.nan
            break
    req = maintenance * abs(qty) * p
    return {"equity": equity, "maintenance_req": req, "initial_margin": margin0, "liquidated_at": liq,
            "funding_paid": paid_funding, "left": float(equity[liq]) if liq is not None else float(equity[-1])}


def liquidation_price(entry: float, leverage: float, maintenance: float, side: int = 1) -> float:
    """The price at which a fresh position opened at ``entry`` with margin entry/leverage hits the maintenance level
    (no funding, no fees): for a long, P (1 - m) = entry (1 - 1/L); for a short, P (1 + m) = entry (1 + 1/L)."""
    if side > 0:
        return entry * (1 - 1 / leverage) / (1 - maintenance)
    return entry * (1 + 1 / leverage) / (1 + maintenance)


def netting(payer, receiver, amount, n: int) -> dict:
    """Obligations among ``n`` members from trades (payer i owes receiver j ``amount``): the gross total, the total
    after each pair nets its trades (bilateral), and after a central counterparty nets everything (each member owes or
    is owed only its net position)."""
    payer, receiver, amount = map(np.asarray, (payer, receiver, amount))
    gross = float(amount.sum())
    M = np.zeros((n, n))
    np.add.at(M, (payer, receiver), amount)
    bilateral = float(np.abs(np.triu(M - M.T, 1)).sum())
    net = M.sum(axis=1) - M.sum(axis=0)
    multilateral = float(net[net > 0].sum())
    return {"gross": gross, "bilateral": bilateral, "multilateral": multilateral, "net_position": net}


def call_auction(bid_px, bid_qty, ask_px, ask_qty) -> dict:
    """The clearing price of a call auction: at each candidate price, demand = bids at or above it, supply = asks at
    or below it; the price that maximizes the executed volume min(demand, supply), ties broken by the smallest
    imbalance and then the midpoint of the tied prices."""
    bp, bq, ap, aq = map(lambda x: np.asarray(x, float), (bid_px, bid_qty, ask_px, ask_qty))
    cands = np.unique(np.concatenate([bp, ap]))
    demand = np.array([bq[bp >= c].sum() for c in cands])
    supply = np.array([aq[ap <= c].sum() for c in cands])
    vol = np.minimum(demand, supply)
    best = vol.max()
    m = vol == best
    imb = np.abs(demand - supply)
    m &= imb == imb[m].min()
    price = float(np.mean(cands[m]))
    return {"price": price, "volume": float(best), "candidates": cands, "demand": demand, "supply": supply}


def fund_fees(gross_returns, mgmt: float = 0.02, perf: float = 0.20, periods_per_year: int = 1) -> dict:
    """Net returns of a fund charging ``mgmt`` a year on assets and ``perf`` of gains above its high-water mark,
    period by period (fees crystallized each period).  Returns net returns, fees per period, and the high-water mark."""
    g = np.asarray(gross_returns, float)
    nav, hwm = 1.0, 1.0
    net, fees, marks = [], [], []
    for r in g:
        before = nav * (1 + r) - nav * mgmt / periods_per_year
        pf = perf * max(before - hwm, 0.0)
        after = before - pf
        fees.append((nav * (1 + r) - after) / nav)
        net.append(after / nav - 1)
        nav = after
        hwm = max(hwm, nav)
        marks.append(hwm)
    return {"net": np.array(net), "fees": np.array(fees), "hwm": np.array(marks), "nav": nav}


def max_leverage(haircut: float) -> float:
    """With a haircut h, every dollar of collateral funds 1 - h dollars of borrowing: repeated, a dollar of equity
    supports at most 1/h dollars of assets."""
    return 1.0 / haircut
