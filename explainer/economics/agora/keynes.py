"""Agora's Keynesian economy (Part 27): the babysitting co-op, the Keynesian cross and Kahn's multiplier, the paradox of
thrift, IS-LM with a zero lower bound, aggregate demand and supply, Phillips's hydraulic machine, and wages that do not
fall.  numpy only.

The co-op (Sweeney and Sweeney 1977, retold by Krugman 1998): couples pay for an evening of babysitting with a coupon.
Each wants a reserve of coupons; a couple below its reserve offers to sit and seldom goes out, a couple above it goes
out and seldom sits.  An evening needs one couple going out and one sitting, so the number of evenings is the smaller
of the two queues.  With too few coupons for everyone's reserve, everyone tries to earn and nobody spends: a recession
with nothing wrong except the quantity of money.
"""

from __future__ import annotations

import numpy as np


# --- the co-op ----------------------------------------------------------------------------------------------------
def coop(n: int = 150, coupons: float = 4.0, target: float = 10.0, weeks: int = 300, p: float = 0.3, seed: int = 0,
         print_at: int | None = None, print_to: float | None = None) -> dict:
    """Simulate the co-op.  ``coupons`` per couple to start; each couple wants a reserve of ``target``.  Each week a
    couple wants to go out with probability ``p * min(1, b / target)`` (it needs at least one coupon) and is willing to
    sit with probability ``p * clip(2 - b / target, 0, 1)``; a couple that wants both goes out.  Evenings pair goers and
    sitters at random; each pays one coupon.  If ``print_at`` is given, the board raises coupons to ``print_to`` per
    couple that week (handing the new coupons out equally).  Returns weekly evenings per couple, the queues, and the
    distribution of balances at the end."""
    rng = np.random.default_rng(seed)
    b = np.full(n, int(round(coupons)), dtype=int)
    extra = coupons * n - b.sum()
    if extra > 0:
        b[rng.choice(n, int(round(extra)), replace=False)] += 1
    evenings, goers, sitters, money = [], [], [], []
    for w in range(weeks):
        if print_at is not None and w == print_at and print_to is not None:
            add = int(round(print_to * n - b.sum()))
            if add > 0:
                b += add // n
                b[rng.choice(n, add % n, replace=False)] += 1
        go_p = p * np.minimum(1.0, b / target) * (b >= 1)
        sit_p = p * np.clip(2.0 - b / target, 0.0, 1.0)
        go = rng.random(n) < go_p
        sit = (rng.random(n) < sit_p) & ~go
        g_idx, s_idx = np.flatnonzero(go), np.flatnonzero(sit)
        k = min(len(g_idx), len(s_idx))
        if k:
            gi = rng.choice(g_idx, k, replace=False)
            si = rng.choice(s_idx, k, replace=False)
            b[gi] -= 1
            b[si] += 1
        evenings.append(k / n)
        goers.append(len(g_idx) / n)
        sitters.append(len(s_idx) / n)
        money.append(b.mean())
    # at the reserve everyone wants out with probability p and sits with p (1 - p): the most evenings a week
    return {"evenings": evenings, "goers": goers, "sitters": sitters, "money": money, "balances": b.tolist(),
            "potential": float(p * (1 - p))}


def coop_curve(levels, n: int = 150, target: float = 10.0, weeks: int = 260, burn: int = 60, p: float = 0.3,
               seed: int = 0) -> dict:
    """Evenings per couple per week, averaged after ``burn`` weeks, at each level of coupons per couple."""
    out, go, sit = [], [], []
    for k, m in enumerate(levels):
        r = coop(n=n, coupons=float(m), target=target, weeks=weeks, p=p, seed=seed + k)
        out.append(float(np.mean(r["evenings"][burn:])))
        go.append(float(np.mean(r["goers"][burn:])))
        sit.append(float(np.mean(r["sitters"][burn:])))
    return {"coupons": [float(m) for m in levels], "evenings": out, "goers": go, "sitters": sit}


# --- the Keynesian cross and the multiplier ---------------------------------------------------------------------
def cross(a: float, b: float, I: float, G: float, T: float = 0.0) -> dict:
    """Planned spending ``E = a + b (Y - T) + I + G``; equilibrium where ``E = Y``: ``Y = (a - bT + I + G)/(1 - b)``."""
    Y = (a - b * T + I + G) / (1 - b)
    return {"Y": float(Y), "C": float(a + b * (Y - T)), "S": float(Y - T - (a + b * (Y - T))),
            "multiplier": 1 / (1 - b), "tax_multiplier": -b / (1 - b)}


def multiplier_rounds(dG: float, b: float, rounds: int = 12) -> dict:
    """Kahn's multiplier as a geometric series: round k adds ``b^k dG``; the total tends to ``dG / (1 - b)``."""
    adds = dG * b ** np.arange(rounds)
    return {"adds": adds.tolist(), "cumulative": np.cumsum(adds).tolist(), "limit": dG / (1 - b)}


def paradox_of_thrift(a: float, b: float, I0: float, G: float, da: float, h: float = 0.0) -> dict:
    """Households try to save ``da`` more at every income (autonomous consumption falls by ``da``).  With investment
    ``I = I0 + hY``, income is ``(a + I0 + G)/(1 - b - h)``.  Returns income and saving before and after: with ``h = 0``
    saving does not change (it must equal investment), with ``h > 0`` it falls."""
    def solve(aa):
        Y = (aa + I0 + G) / (1 - b - h)
        return float(Y), float(Y - (aa + b * Y)), float(I0 + h * Y)
    Y0, S0, I_0 = solve(a)
    Y1, S1, I_1 = solve(a - da)
    return {"Y0": Y0, "Y1": Y1, "S0": S0, "S1": S1, "I0": I_0, "I1": I_1, "dY": Y1 - Y0, "dS": S1 - S0}


# --- IS-LM with a zero lower bound -------------------------------------------------------------------------------
def islm(G: float, M: float, P: float = 1.0, a: float = 200.0, b: float = 0.6, T: float = 100.0, I0: float = 300.0,
         d: float = 25.0, k: float = 0.5, h: float = 50.0, pe: float = 0.0) -> dict:
    """IS: ``Y = (a - bT + I0 + G - d r)/(1 - b)`` with ``r = i - pe``.  LM: ``M/P = kY - h i`` with ``i >= 0``.
    Solved jointly; if the solution needs a negative nominal rate, ``i = 0`` and output is read off the IS curve: the
    liquidity trap, where more money changes nothing."""
    A = a - b * T + I0 + G
    # Y = (A - d (i - pe))/(1-b); i = (kY - M/P)/h
    # Y (1-b) = A + d pe - d (kY - M/P)/h  =>  Y = (A + d pe + d M/(P h)) / (1 - b + d k / h)
    Y = (A + d * pe + d * M / (P * h)) / (1 - b + d * k / h)
    i = (k * Y - M / P) / h
    trap = bool(i < 0)
    if trap:
        i = 0.0
        Y = (A - d * (0.0 - pe)) / (1 - b)
    return {"Y": float(Y), "i": float(i), "r": float(i - pe), "trap": trap, "A": float(A)}


def is_curve(G: float, i, a=200.0, b=0.6, T=100.0, I0=300.0, d=25.0, pe=0.0):
    i = np.asarray(i, float)
    return (a - b * T + I0 + G - d * (i - pe)) / (1 - b)


def lm_curve(M: float, Y, P=1.0, k=0.5, h=50.0):
    """The LM curve's interest rate at each income, floored at zero."""
    Y = np.asarray(Y, float)
    return np.maximum((k * Y - M / P) / h, 0.0)


def ad_curve(P, G: float, M: float, **kw):
    """Aggregate demand: IS-LM's output at each price level."""
    return np.array([islm(G, M, P=float(p), **kw)["Y"] for p in np.atleast_1d(P)])


def as_curve(P, Ystar: float, Pe: float, kappa: float):
    """Short-run aggregate supply with sticky wages: ``Y = Y* + kappa (P - Pe)``; vertical in the long run."""
    return Ystar + kappa * (np.asarray(P, float) - Pe)


def asad(G: float, M: float, Ystar: float, Pe: float, kappa: float, cost: float = 0.0, **kw) -> dict:
    """The short-run equilibrium price and output where AD meets the AS curve (shifted up by a cost shock ``cost`` in
    the price level), found by bisection on ``P``."""
    lo, hi = 0.05, 20.0
    for _ in range(100):
        P = 0.5 * (lo + hi)
        gap = float(ad_curve(P, G, M, **kw)[0]) - float(as_curve(P - cost, Ystar, Pe, kappa))
        if gap > 0:
            lo = P
        else:
            hi = P
    P = 0.5 * (lo + hi)
    return {"P": P, "Y": float(ad_curve(P, G, M, **kw)[0])}


# --- Phillips's machine -------------------------------------------------------------------------------------------
def moniac(b: float = 0.6, tax: float = 0.2, I: float = 150.0, G: float = 200.0, Y0: float = 600.0,
           speed: float = 0.25, steps: int = 60, shock_at: int | None = 10, dG: float = 50.0) -> dict:
    """A water version of the multiplier: income is the level in the main tank, which drains at a rate ``speed`` into
    spending; households spend ``b`` of disposable income and the rest leaks to saving, ``tax`` of income leaks to the
    treasury; investment and government purchases pump back in.  ``Y' = Y + speed (b (1 - tax) Y + I + G - Y)``.
    Returns the path of income and its flows, with ``G`` raised by ``dG`` at ``shock_at``."""
    Y = Y0
    path, cons, save, taxes, gg = [], [], [], [], []
    for t in range(steps):
        g = G + (dG if shock_at is not None and t >= shock_at else 0.0)
        C = b * (1 - tax) * Y
        path.append(Y)
        cons.append(C)
        save.append((1 - b) * (1 - tax) * Y)
        taxes.append(tax * Y)
        gg.append(g)
        Y = Y + speed * (C + I + g - Y)
    m = 1 / (1 - b * (1 - tax))
    return {"Y": path, "C": cons, "S": save, "T": taxes, "G": gg, "multiplier": m,
            "start": (I + G) * m, "end": (I + G + dG) * m}


# --- wages that do not fall --------------------------------------------------------------------------------------
def wage_changes(n: int = 20000, mean: float = 0.01, sd: float = 0.04, rigid: float = 0.8, seed: int = 0) -> dict:
    """Notional nominal pay changes ``N(mean, sd)``; a share ``rigid`` of the cuts are not made (the pay is frozen
    instead), the rest go through.  Returns both distributions and the share of exact zeros."""
    rng = np.random.default_rng(seed)
    want = rng.normal(mean, sd, n)
    cut = want < 0
    frozen = cut & (rng.random(n) < rigid)
    got = np.where(frozen, 0.0, want)
    return {"want": want.tolist(), "got": got.tolist(), "share_cut_wanted": float(cut.mean()),
            "share_zero": float((got == 0).mean()), "share_cut": float((got < 0).mean()),
            "mean_want": float(want.mean()), "mean_got": float(got.mean())}


# --- the business cycle's shape ---------------------------------------------------------------------------------
def spells(indicator, dates) -> dict:
    """Lengths, in months, of the completed recessions (runs of 1) and expansions (runs of 0) in a monthly 0/1
    indicator, with the year each began.  Spells cut off by the start or end of the series are dropped."""
    x = np.asarray(indicator, int)
    out = {"recessions": [], "expansions": [], "rec_start": [], "exp_start": []}
    start = 0
    for t in range(1, len(x) + 1):
        if t == len(x) or x[t] != x[start]:
            if start > 0 and t < len(x):
                key = "recessions" if x[start] == 1 else "expansions"
                out[key].append(t - start)
                out["rec_start" if x[start] == 1 else "exp_start"].append(int(str(dates[start])[:4]))
            start = t
    return out
