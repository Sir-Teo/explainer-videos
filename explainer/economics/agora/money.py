"""Agora's money (Part 25 of *Economics, Built*): why a medium of exchange emerges, how much money people hold, and what
happens when there is too much of it.

* :func:`kw_simulate`: Kiyotaki and Wright's (1989) economy, model A: three types of trader; type i eats good i and
  produces good i + 1; goods cost c1 < c2 < c3 a period to store; traders meet in random pairs and swap when both want
  to.  Under the *fundamental* strategies everyone accepts only goods cheaper to store than the one held (or the good
  they eat); under the *speculative* ones type 1 also accepts good 3, the costly good, because it is easier to trade.
  Returns who holds what and which goods circulate as media of exchange.
* :func:`kw_best_response`: whether type 1 should accept good 3, from its two-state Bellman equation given everyone
  else's holdings and strategies: the equilibrium check.
* :func:`barter_matches`: the chance of a double coincidence of wants among n goods, against a medium of exchange.
* :func:`quantity`: the quantity equation's growth rates, money growth less output growth against inflation.
* :func:`cagan_laffer`: steady-state seigniorage ``mu exp(-alpha mu)`` and its maximum at ``1/alpha``.
* :func:`cagan_deficit`: a deficit financed by printing money, with adaptive expectations: the two steady states and
  the path, which converges or explodes.
* :func:`baumol_tobin`: trips to the bank and average money holdings: the square-root rule.
* :func:`cia`: a cash-in-advance economy: consumption, the nominal rate, welfare and its cost against the Friedman rule.
* :func:`taccounts`: the balance sheets of a central bank, a bank and a household when the bank makes a loan.

numpy only.
"""

from __future__ import annotations

import numpy as np

# Kiyotaki and Wright's model A: type i eats good i and produces good i+1 (goods 0, 1, 2 here for 1, 2, 3)
EATS = (0, 1, 2)
MAKES = (1, 2, 0)


def _accepts(kind: int, held: int, offered: int, speculative: bool) -> bool:
    """Does a trader of type ``kind`` holding good ``held`` accept good ``offered``?  Its own good always; otherwise
    only a good cheaper to store (a lower index), except that under the speculative strategies type 1 (index 0)
    trades its good 2 (index 1) for good 3 (index 2)."""
    if offered == held:
        return False
    if offered == EATS[kind]:
        return True
    if speculative and kind == 0:
        if held == 1 and offered == 2:      # good 3 for good 2: the speculative trade
            return True
        if held == 2 and offered == 1:      # and never back again
            return False
    return offered < held


def kw_simulate(n: int = 300, periods: int = 400, speculative: bool = False, seed: int = 0) -> dict:
    """Random pairwise meetings among ``3n`` traders for ``periods`` periods.  Each holds one good; a trader who gets
    the good it eats consumes it at once and produces its own good.  Returns the share of each type holding each good
    (averaged over the second half), and for each good the share of trades in which it was accepted by someone who
    does not eat it (that is, used as a medium of exchange)."""
    rng = np.random.default_rng(seed)
    kind = np.repeat(np.arange(3), n)
    hold = np.array([MAKES[k] for k in kind])
    dist = np.zeros((3, 3))
    medium = np.zeros(3)
    trades = 0
    half = periods // 2
    for t in range(periods):
        order = rng.permutation(3 * n)
        for a, b in zip(order[0::2], order[1::2]):
            ga, gb = hold[a], hold[b]
            if _accepts(kind[a], ga, gb, speculative) and _accepts(kind[b], gb, ga, speculative):
                trades += 1
                for who, got in ((a, gb), (b, ga)):
                    if got == EATS[kind[who]]:
                        hold[who] = MAKES[kind[who]]
                    else:
                        hold[who] = got
                        if t >= half:
                            medium[got] += 1
        if t >= half:
            for k in range(3):
                dist[k] += np.bincount(hold[kind == k], minlength=3) / n
    dist /= periods - half
    return {"dist": dist.tolist(), "medium": (medium / max(medium.sum(), 1)).tolist(), "trades": trades,
            "speculative": speculative}


def kw_best_response(dist, c=(0.1, 0.2, 0.6), u: float = 1.0, beta: float = 0.9, speculative: bool = False) -> dict:
    """Type 1's values of holding good 2 and good 3, given the population's holdings ``dist[type][good]`` (shares
    within each type, each type a third of the population) and everyone else's strategies.  Each period a type-1
    trader meets one random trader; storage is paid every period.  Returns the two values and whether accepting good
    3 for good 2 pays (``V3 > V2``)."""
    dist = np.asarray(dist, float)
    meet = dist / 3.0                         # the chance of meeting a trader of type j holding good h
    c2, c3 = c[1], c[2]
    V = {1: 0.0, 2: 0.0}                      # holding good index 1 (good 2) or 2 (good 3)
    for _ in range(5000):
        new = {}
        for held in (1, 2):
            val = 0.0
            for j in range(3):
                for h in range(3):
                    p = meet[j, h]
                    if p == 0:
                        continue
                    # does the other side accept my good?
                    they = _accepts(j, h, held, speculative)
                    if h == 0 and they:      # I get good 1, eat it, make good 2
                        val += p * (u + V[1])
                    elif h == 2 and held == 1 and they:   # good 3 offered for my good 2: take the better
                        val += p * max(V[1], V[2])
                    elif h == 1 and held == 2 and they:   # good 2 offered for my good 3
                        val += p * max(V[1], V[2])
                    else:
                        val += p * V[held]
            cost = c2 if held == 1 else c3
            new[held] = -cost + beta * val
        if max(abs(new[k] - V[k]) for k in V) < 1e-12:
            V = new
            break
        V = new
    return {"V2": V[1], "V3": V[2], "accept_3": bool(V[2] > V[1]), "gain": V[2] - V[1]}


def barter_matches(n_goods: int) -> dict:
    """With n goods, a trader holding one and wanting another meets a random trader: the chance the other has what
    the first wants and wants what the first has is ``1/(n-1)^2`` under barter, against ``1/(n-1)`` with money (only
    one side of the coincidence is needed)."""
    k = max(n_goods - 1, 1)
    return {"barter": 1 / k ** 2, "money": 1 / k, "trips_barter": k ** 2, "trips_money": 2 * k}


def quantity(money_growth, output_growth, velocity_growth=0.0):
    """``M V = P Y`` in growth rates: inflation = money growth + velocity growth - output growth (all in logs)."""
    return np.asarray(money_growth, float) + velocity_growth - np.asarray(output_growth, float)


def cagan_laffer(alpha: float, mus=None) -> dict:
    """Steady-state seigniorage as a share of output, ``mu m(mu)`` with real balances ``m = exp(-alpha mu)``
    (Cagan's semi-log demand, ``alpha`` in periods): the inflation tax's Laffer curve, highest at ``mu = 1/alpha``."""
    mus = np.linspace(0, 6 / alpha, 301) if mus is None else np.asarray(mus, float)
    rev = mus * np.exp(-alpha * mus)
    k = int(np.argmax(rev))
    return {"mu": mus.tolist(), "revenue": rev.tolist(), "best": float(mus[k]), "max": float(rev[k]),
            "best_exact": 1 / alpha, "max_exact": float(np.exp(-1) / alpha)}


def cagan_deficit(alpha: float, deficit: float, lam: float, periods: int = 120, pi0: float = 0.01) -> dict:
    """A deficit (a share of real balances' scale) financed by printing money: real balances ``m = exp(-alpha pe)``
    and seigniorage ``(1 - 1/(1 + pi)) m``; expectations adapt, ``pe' = pe + lam (pi - pe)``.  The steady states solve
    ``(pi/(1 + pi)) exp(-alpha pi) = deficit``; the low one is reached when expectations adapt slowly, and inflation
    explodes when they adapt fast (``lam alpha`` large) or the deficit exceeds the Laffer maximum."""
    grid = np.linspace(0, 20 / alpha, 20001)
    rev = grid / (1 + grid) * np.exp(-alpha * grid)
    above = rev >= deficit
    steady = []
    if above.any():
        idx = np.where(above)[0]
        steady = [float(grid[idx[0]]), float(grid[idx[-1]])]
    pe, path = pi0, []
    m_prev = np.exp(-alpha * pe)
    for _ in range(periods):
        m = np.exp(-alpha * pe)
        if m < 1e-12:                         # real balances have vanished: the currency is abandoned
            path.append(float("inf"))
            break
        # money printed covers the deficit: M'/M = 1 + deficit/m, and P'/P follows from m'/m: (1 + pi) = (M'/M) m/m'
        growth = 1 + deficit / m
        pi = growth * m_prev / m - 1 if path else growth - 1
        pi = float(max(pi, -0.99))
        path.append(pi)
        pe = pe + lam * (pi - pe)
        m_prev = m
        if pi > 1e6:
            break
    finite = [x for x in path if np.isfinite(x)]
    return {"steady": steady, "path": finite, "exploded": bool(len(finite) < len(path) or
                                                               path[-1] > 10 * (steady[-1] if steady else 1)),
            "laffer_max": float(rev.max())}


def baumol_tobin(Y: float, i, b: float) -> dict:
    """Income Y a period spent evenly; each trip to the bank costs b; money held earns nothing while bonds earn i.
    Trips ``n = sqrt(i Y / (2 b))``, average money ``M = Y / (2 n) = sqrt(b Y / (2 i))``: an income elasticity of a half
    and an interest elasticity of minus a half."""
    i = np.asarray(i, float)
    n = np.sqrt(i * Y / (2 * b))
    M = Y / (2 * n)
    return {"trips": n.tolist() if n.ndim else float(n), "money": M.tolist() if M.ndim else float(M),
            "cost": (i * M + b * n).tolist() if n.ndim else float(i * M + b * n)}


def cia(mu, beta: float = 0.96, a: float = 1.0) -> dict:
    """A cash-in-advance economy: utility ``ln c - a n``, output ``c = n``, consumption bought with money carried
    from the last period, money growing at ``mu``.  In a steady state inflation is ``mu``, the nominal rate is
    ``i = (1 + mu)/beta - 1``, and the first-order condition gives ``c = 1/(a (1 + i))``.  Welfare is ``ln c - a c``;
    the cost of inflation is the share of consumption that would compensate a household for moving from the Friedman
    rule (``i = 0``, ``mu = beta - 1``)."""
    mu = np.asarray(mu, float)
    i = (1 + mu) / beta - 1
    c = 1 / (a * (1 + i))
    w = np.log(c) - a * c
    c0 = 1 / a
    w0 = np.log(c0) - a * c0
    # the consumption-equivalent loss: ln((1 - x) c0) - a c0 = w
    loss = 1 - np.exp(w - w0)
    return {"mu": mu.tolist(), "i": i.tolist(), "c": c.tolist(), "welfare": w.tolist(), "loss": loss.tolist(),
            "friedman_mu": beta - 1}


def taccounts(loan: float = 100.0, cash_share: float = 0.0) -> dict:
    """When a bank lends ``loan`` to a household, both balance sheets grow at once: the bank gains a loan (an asset)
    and a deposit (a liability); the household gains the deposit and the debt.  Broad money (deposits plus currency)
    rises by the loan; reserves, the central bank's money, do not change unless the borrower withdraws cash
    (``cash_share`` of the loan), which the bank must obtain from the central bank against reserves."""
    cash = loan * cash_share
    return {"bank": {"assets": {"loan": loan, "reserves": -cash}, "liabilities": {"deposit": loan - cash}},
            "household": {"assets": {"deposit": loan - cash, "currency": cash}, "liabilities": {"loan": loan}},
            "central_bank": {"assets": {}, "liabilities": {"reserves": -cash, "currency": cash}},
            "broad_money": loan, "base_money": 0.0}
