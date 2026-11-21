"""Agora's merger review toolkit (Part 59): an Island merger reviewed as an agency and a court would, with the truth
known.

* **The Island's office-supply market** (:data:`MARKET`, :func:`town_shares`, :func:`towns`): three superstore
  chains (Alder, Birch and Cedar), the corner shops, and buying nothing, as a nested logit (the superstores share a
  nest) with Bertrand pricing in each of sixty towns; Alder is everywhere, Birch and Cedar in some towns, more often
  in big ones, where rents are higher.
* **The price map and the regression** (:func:`price_regression`, :func:`multiverse`): Alder's price against its
  rivals' presence, as the Federal Trade Commission's economists ran it in *Staples*, and the same regression under
  every reasonable specification.
* **Market definition** (:func:`critical_loss`, :func:`critical_diversion`, :func:`hmt`, :func:`cellophane`): the
  hypothetical-monopolist test with a 5% SSNIP, critical loss against actual loss, and the cellophane fallacy.
* **Concentration** (:func:`hhi`, :data:`THRESHOLDS`): the Herfindahl index and the guidelines' presumptions of 1982,
  2010 and 2023.
* **Unilateral effects** (:func:`diversion`, :func:`upp`): diversion ratios from the demand system, upward pricing
  pressure and the GUPPI, against a full merger simulation (Agora's ``io.merger``) and the cost savings that would
  offset it.
* **Pass-through** (:func:`pass_through`): how much of a cost saving reaches prices.
* **Vertical bargaining** (:func:`vertical`): a channel and two distributors; integration raises the rival's fee
  through the channel's better outside option, and removes double marginalization for its own distributor.
* **Cartels** (:func:`cartel`, :func:`variance_screen`): a price-fixing period with its overcharge estimated by
  regression, and the screen that low price variance suggests.
* **Retrospective** (:func:`retrospective`): the merger as consummated, estimated by difference in differences against
  towns where the merging chains did not overlap.
* **Labour** (:func:`labour_merger`): two employers merging in a town where workers choose by logit.
* **In court** (:func:`playit_pairs`, :func:`industries`, :func:`town_concentration`, :func:`functional_forms`,
  :func:`agency_logit`, :func:`witness`, :func:`vertical_curve`): the Play-it pairs, the guidelines applied to the
  Island's industries, the same elasticities under four demand curves, an agency's plain-logit simulation scored
  against the truth, and the cross-examination of the price regression.
* **Regulated prices** (:func:`rate_case`, :func:`price_cap`, :func:`ecpr`): a revenue requirement, a price cap with
  periodic resets, and the efficient component pricing rule for access.

numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize

from . import io as IO

# ---------------------------------------------------------------------------------------------------------------
# the market

# Prices are for a basket of office supplies, in Island dollars.  Utility of product j: base_j - alpha p_j, nested
# logit with the three superstores in one nest and the corner shops in another (sigma 0.4), and buying nothing.
MARKET = {
    "names": ("Alder", "Birch", "Cedar", "corner shops"),
    "base": (8.6, 8.5, 8.4, 7.4),
    "alpha": 0.08,
    "sigma": 0.4,
    "nests": (0, 0, 0, 1),
    "mc": (70.0, 71.0, 72.0, 78.0),
}


def share_fn(present, base_shift: float = 0.0, params: dict | None = None):
    """The nested-logit share function for the products present in a town (a boolean mask over the four)."""
    P = {**MARKET, **(params or {})}
    idx = np.flatnonzero(np.asarray(present, bool))
    base = np.asarray(P["base"], float)[idx] + base_shift
    nests = np.asarray(P["nests"])[idx]

    def f(p):
        return IO.nested_shares(base - P["alpha"] * np.asarray(p, float), nests, P["sigma"])
    return f, idx


def bertrand(f, mc, own, p0=None) -> np.ndarray:
    """Bertrand-Nash prices from the first-order conditions s + (Omega * dS/dp')(p - mc) = 0, solved by Powell's
    hybrid method (faster than Agora's damped iteration for these small markets), checked against it."""
    mc = np.asarray(mc, float)
    O = (np.asarray(own)[:, None] == np.asarray(own)[None, :]).astype(float)

    def foc(p):
        return f(p) + (O * IO.jacobian(f, p)) @ (p - mc)
    start = mc * 1.2 if p0 is None else np.asarray(p0, float)
    sol = optimize.root(foc, start, method="hybr", tol=1e-12)
    if not sol.success or np.max(np.abs(foc(sol.x))) > 1e-8:
        return IO.bertrand(f, mc, own, p0=start)
    return sol.x


def equilibrium(present, cost_shift: float = 0.0, base_shift: float = 0.0, owner=None, params: dict | None = None):
    """Bertrand-Nash prices in a town: each product its own owner unless ``owner`` says otherwise."""
    P = {**MARKET, **(params or {})}
    f, idx = share_fn(present, base_shift, P)
    mc = np.asarray(P["mc"], float)[idx] * (1.0 + cost_shift)
    own = np.arange(len(idx)) if owner is None else np.asarray(owner)[idx]
    p = bertrand(f, mc, own)
    return {"idx": idx, "p": p, "mc": mc, "s": f(p), "f": f, "owner": own}


def towns(n: int = 60, seed: int = 59) -> dict:
    """Sixty Island towns: size (log population), rents that rise with size (a cost shift), Birch present with a
    probability that rises with size, Cedar likewise; Alder and the corner shops everywhere.  Alder's equilibrium
    price in each, with a little measurement noise; the truth of what a merger of Alder and Birch would do there."""
    rng = np.random.default_rng(seed)
    size = rng.normal(0.0, 1.0, n)
    cost = 0.06 * size + rng.normal(0.0, 0.02, n)
    pb = 1 / (1 + np.exp(-(0.2 + 1.2 * size)))
    pc = 1 / (1 + np.exp(-(-0.4 + 1.0 * size)))
    birch = rng.random(n) < pb
    cedar = rng.random(n) < pc
    price, merged, share = np.zeros(n), np.full(n, np.nan), np.zeros(n)
    for t in range(n):
        pres = np.array([True, birch[t], cedar[t], True])
        eq = equilibrium(pres, cost_shift=cost[t])
        price[t] = eq["p"][0]
        share[t] = eq["s"][0]
        if birch[t]:
            own = np.array([0, 0, 2, 3])
            m = equilibrium(pres, cost_shift=cost[t], owner=own)
            merged[t] = m["p"][0] / eq["p"][0] - 1.0
    noisy = price * np.exp(rng.normal(0.0, 0.006, n))
    return {"n": n, "size": size, "cost": cost, "birch": birch, "cedar": cedar, "price": noisy, "true_price": price,
            "merger_effect": merged, "share": share}


def _ols(X, y):
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    n, k = X.shape
    XtXi = np.linalg.inv(X.T @ X)
    V = XtXi @ (X.T * e ** 2) @ X @ XtXi * n / (n - k)
    return b, np.sqrt(np.diag(V))


def price_regression(T: dict | None = None, controls: bool = True) -> dict:
    """Log of Alder's price on Birch's and Cedar's presence, with or without the town's costs and size: the FTC's
    method in *Staples* (1997).  Returns the percent effects with standard errors, and the average true effect of a
    merger of Alder and Birch in the towns where both are."""
    T = T or towns()
    y = np.log(T["price"])
    cols = [np.ones(T["n"]), T["birch"].astype(float), T["cedar"].astype(float)]
    if controls:
        cols += [T["cost"], T["size"]]
    b, se = _ols(np.column_stack(cols), y)
    return {"birch": -100 * b[1], "birch_se": 100 * se[1], "cedar": -100 * b[2], "cedar_se": 100 * se[2],
            "true_merger": 100 * float(np.nanmean(T["merger_effect"])), "controls": controls,
            "mono": 100 * float(np.mean(T["price"][~T["birch"] & ~T["cedar"]]) /
                                np.mean(T["price"][T["birch"] & T["cedar"]]) - 1)}


def multiverse(T: dict | None = None) -> list:
    """The Birch effect under each combination of choices an expert could defend: controls for costs, for size,
    the dependent variable in logs or levels, Cedar's presence in or out."""
    T = T or towns()
    out = []
    for cost in (True, False):
        for size in (True, False):
            for logs in (True, False):
                for cedar in (True, False):
                    y = np.log(T["price"]) if logs else T["price"]
                    cols = [np.ones(T["n"]), T["birch"].astype(float)]
                    if cedar:
                        cols.append(T["cedar"].astype(float))
                    if cost:
                        cols.append(T["cost"])
                    if size:
                        cols.append(T["size"])
                    b, se = _ols(np.column_stack(cols), y)
                    eff = -100 * b[1] if logs else -100 * b[1] / float(np.mean(T["price"]))
                    out.append({"cost": cost, "size": size, "logs": logs, "cedar": cedar, "effect": eff,
                                "se": 100 * se[1] if logs else 100 * se[1] / float(np.mean(T["price"]))})
    return out


# ---------------------------------------------------------------------------------------------------------------
# market definition

def critical_loss(X: float, M: float) -> float:
    """The share of sales a price rise of X can lose before it stops paying, at a margin M: X/(X + M)."""
    return X / (X + M)


def critical_diversion(X: float, M: float) -> float:
    """For a symmetric pair of single-product firms pricing optimally with linear demand, a hypothetical monopolist
    of both raises both prices by X profitably if the diversion ratio between them exceeds X/(X + M)."""
    return X / (X + M)


def hmt(present=(True, True, True, True), candidate=(0, 1, 2), X: float = 0.05, prices=None) -> dict:
    """The hypothetical-monopolist test in a town: raise the candidate products' prices by X (the others' prices held
    fixed) and ask whether the candidates' joint profit rises.  Returns the profit change, the actual and critical
    losses, and the verdict."""
    eq = equilibrium(np.asarray(present, bool))
    f, idx = eq["f"], eq["idx"]
    p0 = eq["p"] if prices is None else np.asarray(prices, float)
    pos = [int(np.flatnonzero(idx == c)[0]) for c in candidate]
    s0 = f(p0)
    p1 = p0.copy()
    p1[pos] *= 1 + X
    s1 = f(p1)
    mc = eq["mc"]
    prof0 = float(np.sum((p0[pos] - mc[pos]) * s0[pos]))
    prof1 = float(np.sum((p1[pos] - mc[pos]) * s1[pos]))
    q0, q1 = float(np.sum(s0[pos])), float(np.sum(s1[pos]))
    M = float(np.sum((p0[pos] - mc[pos]) * s0[pos]) / np.sum(p0[pos] * s0[pos]))
    return {"profit0": prof0, "profit1": prof1, "passes": prof1 > prof0, "actual_loss": 1 - q1 / q0,
            "critical_loss": critical_loss(X, M), "margin": M, "candidate": list(candidate)}


def cellophane(present=(True, True, True, True), X: float = 0.05) -> dict:
    """The cellophane fallacy: if the three superstores already behaved as one firm, the test run at their (already
    monopoly) prices would find a further 5% unprofitable, and the market would be drawn too wide."""
    own = np.array([0, 0, 0, 3])
    mono = equilibrium(np.asarray(present, bool), owner=own)
    comp = hmt(present, (0, 1, 2), X)
    at_mono = hmt(present, (0, 1, 2), X, prices=mono["p"])
    return {"competitive": comp, "monopoly": at_mono, "p_comp": equilibrium(np.asarray(present, bool))["p"].tolist(),
            "p_mono": mono["p"].tolist()}


# ---------------------------------------------------------------------------------------------------------------
# concentration

THRESHOLDS = {
    1982: {"highly": 1800, "delta": 100},
    2010: {"highly": 2500, "delta": 200},
    2023: {"highly": 1800, "delta": 100, "share": 30},
}


def hhi(shares) -> float:
    """The Herfindahl-Hirschman index of shares in percent."""
    s = np.asarray(shares, float)
    s = 100 * s / s.sum()
    return float(np.sum(s ** 2))


def presumption(shares, merging=(0, 1)) -> dict:
    """The HHI before and after combining the merging firms' shares, and whether each guideline would presume harm."""
    s = 100 * np.asarray(shares, float) / np.sum(shares)
    pre = float(np.sum(s ** 2))
    d = 2 * s[merging[0]] * s[merging[1]]
    post = pre + d
    comb = s[merging[0]] + s[merging[1]]
    verdict = {}
    for y, t in THRESHOLDS.items():
        v = post > t["highly"] and d > t["delta"]
        if "share" in t:
            v = v or (comb > t["share"] and d > t["delta"])
        verdict[y] = bool(v)
    return {"pre": pre, "post": post, "delta": d, "combined": float(comb), "verdict": verdict}


# ---------------------------------------------------------------------------------------------------------------
# unilateral effects

def diversion(eq: dict) -> np.ndarray:
    """D[j, k]: the share of j's lost sales that go to k when j's price rises, -(ds_k/dp_j)/(ds_j/dp_j)."""
    J = IO.jacobian(eq["f"], eq["p"])
    return -J / np.diag(J)[:, None]


def upp(present=(True, True, True, True), merging=(0, 1), credit: float = 0.0) -> dict:
    """Farrell and Shapiro's upward pricing pressure on each merging product: the diversion to the partner times the
    partner's margin, less a credit for cost savings (a share of marginal cost); and the GUPPI, the first term over
    the price.  With the full simulation for comparison."""
    eq = equilibrium(np.asarray(present, bool))
    idx = eq["idx"]
    a, b = [int(np.flatnonzero(idx == m)[0]) for m in merging]
    D = diversion(eq)
    p, c = eq["p"], eq["mc"]
    out = {}
    for j, k in ((a, b), (b, a)):
        val = D[j, k] * (p[k] - c[k]) - credit * c[j]
        out[MARKET["names"][idx[j]]] = {"diversion": float(D[j, k]), "partner_margin": float(p[k] - c[k]),
                                        "upp": float(val), "guppi": float(D[j, k] * (p[k] - c[k]) / p[j])}
    own = np.arange(len(idx))
    sim = IO.merger(eq["f"], p, own, [a, b])
    cm = IO.cmcr(eq["f"], p, own, [a, b])
    return {"products": out, "simulation": sim, "cmcr": [float(x) for x in np.asarray(cm)[[a, b]]],
            "prices": p.tolist(), "mc": c.tolist(), "diversion_matrix": D.tolist(),
            "names": [MARKET["names"][i] for i in idx]}


def pass_through(present=(True, True, True, True), saving: float = 0.02) -> dict:
    """Lower the merged firm's marginal costs by ``saving`` and compare its prices with and without: the share of the
    saving passed on, for the merged firm and for a single-product firm alone."""
    pres = np.asarray(present, bool)
    own = np.array([0, 0, 2, 3])
    base = equilibrium(pres, owner=own)
    P = {**MARKET}
    mc2 = list(P["mc"])
    mc2[0] *= 1 - saving
    mc2[1] *= 1 - saving
    low = equilibrium(pres, owner=own, params={"mc": tuple(mc2)})
    dp = low["p"][:2] - base["p"][:2]
    dc = np.array(mc2[:2]) - np.array(P["mc"][:2])
    solo = equilibrium(pres)
    mc3 = list(P["mc"])
    mc3[0] *= 1 - saving
    solo2 = equilibrium(pres, params={"mc": tuple(mc3)})
    return {"merged": (dp / dc).tolist(), "single": float((solo2["p"][0] - solo["p"][0]) / (mc3[0] - P["mc"][0]))}


# ---------------------------------------------------------------------------------------------------------------
# vertical

def vertical(subs: float = 1.0, fee: float = 2.0, margin_d1: float = 40.0, depart: float = 0.10,
             to_d1: float = 0.45, share_channel: float = 0.5, d1_share: float = 0.4) -> dict:
    """A channel sells to two distributors at a fee per subscriber a month.  If the channel goes dark on distributor 2,
    a fraction ``depart`` of 2's subscribers leave, ``to_d1`` of them to distributor 1.  Once the channel and
    distributor 1 are one firm, those switchers are worth distributor 1's margin to the channel, which strengthens
    its hand: with bargaining weight ``share_channel``, the fee to distributor 2 rises by weight x depart x to_d1 x
    margin (the formula behind the Justice Department's case against AT&T and Time Warner).  Distributor 1 stops
    paying the fee as a marked-up cost (the elimination of double marginalization): its marginal cost falls by the
    fee."""
    rise = share_channel * depart * to_d1 * margin_d1
    rival_cost = rise * subs * (1 - d1_share)
    edm = fee * subs * d1_share
    # the departure rate at which the rivals' higher costs equal the savings from double marginalization
    threshold = edm / (share_channel * to_d1 * margin_d1 * subs * (1 - d1_share))
    return {"fee_rise": rise, "rival_cost": rival_cost, "edm": edm, "net": rival_cost - edm,
            "rise_pct": 100 * rise / fee, "threshold": threshold}


# ---------------------------------------------------------------------------------------------------------------
# cartels

def cartel(T: int = 180, start: int = 72, end: int = 132, overcharge: float = 0.18, seed: int = 59) -> dict:
    """Monthly prices of the Island's cement: a cost index that wanders, a competitive margin with month-to-month
    noise, and from ``start`` to ``end`` a cartel that adds ``overcharge`` and smooths prices.  The before-during-after
    regression of log price on log cost and a cartel dummy estimates the overcharge; the damages are the overcharge on
    the cartel's sales."""
    rng = np.random.default_rng(seed)
    t = np.arange(T)
    cost = 50 * np.exp(np.cumsum(rng.normal(0.0, 0.02, T)))
    during = (t >= start) & (t < end)
    noise = np.where(during, rng.normal(0.0, 0.008, T), rng.normal(0.0, 0.035, T))
    price = cost * 1.25 * np.exp(np.where(during, np.log(1 + overcharge), 0.0) + noise)
    qty = 100 * (price / price.mean()) ** -0.8
    X = np.column_stack([np.ones(T), np.log(cost), during.astype(float)])
    b, se = _ols(X, np.log(price))
    est = float(np.exp(b[2]) - 1)
    but_for = price / np.where(during, 1 + est, 1.0)
    damages = float(np.sum((price - but_for)[during] * qty[during]))
    return {"t": t, "cost": cost, "price": price, "during": during, "estimate": est, "se": float(se[2]),
            "truth": overcharge, "damages": damages, "but_for": but_for, "start": start, "end": end}


def variance_screen(price, cost, window: int = 12) -> dict:
    """The coefficient of variation of the price-cost margin over rolling windows: cartels often show steadier
    prices; the screen flags the steadiest stretches for a closer look, and proves nothing by itself."""
    m = np.log(np.asarray(price) / np.asarray(cost))
    dm = np.diff(m)
    cv = np.array([np.std(dm[max(0, k - window):k + 1]) for k in range(len(dm))])
    thr = float(np.quantile(cv[window:], 0.25))
    return {"cv": cv, "threshold": thr, "flag": cv < thr}


# ---------------------------------------------------------------------------------------------------------------
# after the fact

def retrospective(T: dict | None = None, seed: int = 59) -> dict:
    """The merger of Alder and Birch, consummated: in towns where both were, prices move by the simulated effect; in
    towns where Birch was absent (the controls), they do not.  Twelve months before and after, with common shocks and
    noise; difference in differences recovers the average effect, which can be set against the simulation."""
    T = T or towns()
    rng = np.random.default_rng(seed + 1)
    treat = T["birch"]
    months = np.arange(-12, 12)
    common = np.cumsum(rng.normal(0.0, 0.003, len(months)))
    eff = np.nan_to_num(T["merger_effect"])
    logp = (np.log(T["true_price"])[:, None] + common[None, :] + rng.normal(0.0, 0.01, (T["n"], len(months))) +
            np.where((months >= 0)[None, :] & treat[:, None], np.log1p(eff)[:, None], 0.0))
    post = (months >= 0)
    d_t = logp[treat][:, post].mean() - logp[treat][:, ~post].mean()
    d_c = logp[~treat][:, post].mean() - logp[~treat][:, ~post].mean()
    est = float(np.exp(d_t - d_c) - 1)
    return {"months": months, "treated": np.exp(logp[treat].mean(axis=0)), "control": np.exp(logp[~treat].mean(axis=0)),
            "estimate": 100 * est, "predicted": 100 * float(np.mean(eff[treat])), "n_treated": int(treat.sum()),
            "n_control": int((~treat).sum())}


# ---------------------------------------------------------------------------------------------------------------
# labour

def labour_merger(base=(1.0, 1.0, 3.0), beta: float = 0.2, productivity: float = 40.0) -> dict:
    """A town's nurses choose among two hospitals and other work (logit in the wage, with an outside option): each
    hospital sets a wage below what a nurse produces (a markdown).  When the two hospitals merge, the markdown widens
    and wages fall, though no price paid by a patient need change."""
    b = np.asarray(base, float)

    def supply(w):
        u = b + beta * np.asarray(w, float)
        e = np.exp(u)
        return e / (1.0 + e.sum())

    def wages(owner):
        w = np.full(3, productivity * 0.7)
        w[2] = productivity * 0.6
        for _ in range(4000):
            s = supply(w)
            new = w.copy()
            for j in range(2):
                same = [k for k in range(2) if owner[k] == owner[j]]
                # first-order condition of employer j: (productivity - w_j) ds_j/dw_j + sum_k (productivity - w_k)
                # ds_k/dw_j = s_j  for the hospitals it owns
                ds = beta * s[j] * (1 - s[j])
                cross = sum((productivity - w[k]) * (-beta * s[j] * s[k]) for k in same if k != j)
                new[j] = productivity - (s[j] - cross) / ds
            if np.max(np.abs(new - w)) < 1e-10:
                break
            w = 0.5 * w + 0.5 * new
        return w

    w0 = wages([0, 1])
    w1 = wages([0, 0])
    return {"before": w0[:2].tolist(), "after": w1[:2].tolist(), "fall": float(100 * (w1[0] / w0[0] - 1)),
            "markdown_before": float(100 * (1 - w0[0] / productivity)),
            "markdown_after": float(100 * (1 - w1[0] / productivity))}


# ---------------------------------------------------------------------------------------------------------------
# in court

def playit_pairs(X: float = 0.05) -> list:
    """Three pairs for the viewer: is each one market?  The diversion ratio from one product to the other, the
    other's margin, and the critical diversion X/(X + M) that the hypothetical-monopolist test needs."""
    eq = equilibrium(np.ones(4, bool))
    D = diversion(eq)
    p, c = eq["p"], eq["mc"]
    marg = (p - c) / p
    pairs = [
        {"name": "Alder and Birch", "a": "Alder", "b": "Birch", "D": float(D[0, 1]), "M": float(marg[1]),
         "what": "two office superstores, a mile apart"},
        {"name": "Alder and the corner shops", "a": "Alder", "b": "the corner shops", "D": float(D[0, 3]),
         "M": float(marg[3]), "what": "a superstore and the town's small stationers"},
        {"name": "the two cement kilns", "a": "the east kiln", "b": "the west kiln", "D": 0.20, "M": 0.60,
         "what": "two kilns whose cement is costly to haul; a high margin over the cost of one more tonne"},
    ]
    for q in pairs:
        q["critical"] = critical_diversion(X, q["M"])
        q["one_market"] = q["D"] > q["critical"]
    return pairs


ISLAND_INDUSTRIES = {
    "cement kilns": ((25, 25, 25, 25), (2, 3)),
    "banks": ((30, 25, 20, 15, 10), (3, 4)),
    "grocers": ((22, 20, 18, 15, 15, 10), (4, 5)),
    "bakeries": ((12, 11, 11, 10, 10, 10, 10, 9, 9, 8), (0, 1)),
    "hospitals": ((34, 20, 16, 16, 14), (3, 4)),
}


def industries() -> list:
    """Five Island industries and a proposed merger in each, judged by the presumptions of 1982, 2010 and 2023."""
    out = []
    for name, (sh, m) in ISLAND_INDUSTRIES.items():
        r = presumption(sh, m)
        out.append({"name": name, "shares": list(sh), "merging": list(m), **r})
    return out


def town_concentration(T: dict | None = None) -> dict:
    """In each town where Alder and Birch meet, the superstores' shares of superstore sales, the Herfindahl index
    before and after a merger of the two, and its change."""
    T = T or towns()
    rows = []
    for t in np.flatnonzero(T["birch"]):
        pres = np.array([True, True, bool(T["cedar"][t]), True])
        eq = equilibrium(pres, cost_shift=float(T["cost"][t]))
        s = eq["s"][:-1]                     # the superstores present (the corner shops are last)
        r = presumption(s, (0, 1))
        rows.append({"town": int(t), "cedar": bool(T["cedar"][t]), "pre": r["pre"], "post": r["post"],
                     "delta": r["delta"], "combined": r["combined"],
                     "effect": 100 * float(T["merger_effect"][t])})
    return {"rows": rows}


def functional_forms(m: float = 0.3, D: float = 0.3, saving: float = 0.0) -> dict:
    """Crooke, Froeb, Tschantz and Werden's point (1999): two symmetric single-product firms with the same price (1),
    margin ``m`` (so own elasticity 1/m) and diversion ``D`` before the merger, under linear, logit, almost-ideal-like
    (linear in log price) and constant-elasticity demand; the merged price rise differs because the curvature does.
    ``saving`` cuts the merged firm's marginal cost by that share (the interactive's efficiency credit)."""
    e = 1.0 / m
    c = (1.0 - m) * (1.0 - saving)      # the merged firm's marginal cost, after any saving

    def merged_price(q, dq):
        # symmetric joint-profit first-order condition: q(p) + (p - c) (dq_own + dq_cross) = 0 at p1 = p2 = p
        return optimize.brentq(lambda p: q(p) + (p - c) * dq(p), c + 1e-6, 20.0)

    # linear: q_i = a - b p_i + d p_j, calibrated to q = 1, p = 1
    b, d = e, D * e
    a = 1 + b - d
    lin = merged_price(lambda p: a - (b - d) * p, lambda p: -(b - d))
    # logit with an outside good: diversion s/(1 - s) = D, own elasticity alpha p (1 - s) = e
    s = D / (1 + D)
    al = e / (1 - s)
    dl = np.log(s / (1 - 2 * s)) + al

    def ql(p):
        x = np.exp(dl - al * p)
        return x / (1 + 2 * x)

    def dql(p):
        q = ql(p)
        return -al * q * (1 - q) + al * q * q
    logit = merged_price(ql, dql)
    # linear in log prices (the almost-ideal system's shape): q_i = k - b ln p_i + d ln p_j, slopes at p = 1
    loglin = merged_price(lambda p: 1 - (b - d) * np.log(p), lambda p: -(b - d) / p)
    # constant elasticity: q_i = p_i^-e p_j^(D e)
    ce = merged_price(lambda p: p ** (-e + D * e), lambda p: (-e + D * e) * p ** (-e + D * e - 1))
    return {"m": m, "D": D, "elasticity": e, "forms": ["linear", "logit", "log-linear", "constant elasticity"],
            "rise": [100 * (x - 1) for x in (lin, logit, loglin, ce)],
            "guppi": 100 * D * m}


def _simulate(f, p0, own, merging) -> np.ndarray:
    mc = IO.costs_from_prices(f, p0, own)
    new = np.asarray(own).copy()
    for j in merging:
        new[new == new[j]] = new[merging[0]]
    return bertrand(f, mc, new, p0=p0)


def agency_logit(T: dict | None = None) -> dict:
    """An agency simulates the merger of Alder and Birch town by town with a plain logit, calibrated to each town's
    prices and shares and to Alder's true own-price elasticity there.  The plain logit sends lost sales to rivals in
    proportion to their shares, missing that the superstores are closer substitutes for each other than for the
    corner shops; its predictions are set against the truth."""
    T = T or towns()
    pred, truth, guppi, cedar = [], [], [], []
    for t in np.flatnonzero(T["birch"]):
        pres = np.array([True, True, bool(T["cedar"][t]), True])
        eq = equilibrium(pres, cost_shift=float(T["cost"][t]))
        p, s = eq["p"], eq["s"]
        J = IO.jacobian(eq["f"], p)
        eps = -J[0, 0] * p[0] / s[0]
        alpha = eps / (p[0] * (1 - s[0]))
        s0 = 1 - s.sum()
        delta = np.log(s / s0) + alpha * p
        n = len(p)

        def f(pp, delta=delta, alpha=alpha, n=n):
            return IO.nested_shares(delta - alpha * np.asarray(pp, float), np.arange(n), 0.0)
        p1 = _simulate(f, p, np.arange(n), [0, 1])
        pred.append(100 * (p1[0] / p[0] - 1))
        truth.append(100 * float(T["merger_effect"][t]))
        D = diversion(eq)
        guppi.append(100 * D[0, 1] * (p[1] - eq["mc"][1]) / p[0])
        cedar.append(bool(T["cedar"][t]))
    return {"predicted": pred, "truth": truth, "guppi": guppi, "cedar": cedar,
            "mean_predicted": float(np.mean(pred)), "mean_truth": float(np.mean(truth)),
            "mean_guppi": float(np.mean(guppi))}


def witness(T: dict | None = None) -> dict:
    """The cross-examination of the price regression: the estimate with each town left out in turn, and on the
    subsamples a defence would propose (towns with Cedar, towns without it, the bigger and the smaller half)."""
    T = T or towns()
    base = price_regression(T)

    def est(mask):
        sub = {k: (v[mask] if isinstance(v, np.ndarray) and v.shape == (T["n"],) else v) for k, v in T.items()}
        sub["n"] = int(mask.sum())
        y = np.log(sub["price"])
        X = np.column_stack([np.ones(sub["n"]), sub["birch"].astype(float), sub["cedar"].astype(float),
                             sub["cost"], sub["size"]])
        if np.ptp(sub["cedar"].astype(float)) == 0:
            X = np.delete(X, 2, axis=1)
        b, se = _ols(X, y)
        return -100 * b[1], 100 * se[1]
    loo = [est(np.arange(T["n"]) != k)[0] for k in range(T["n"])]
    big = T["size"] > np.median(T["size"])
    subs = {"towns with Cedar": est(T["cedar"]), "towns without Cedar": est(~T["cedar"]),
            "the bigger half": est(big), "the smaller half": est(~big)}
    return {"base": base["birch"], "base_se": base["birch_se"], "loo": loo, "loo_min": float(min(loo)),
            "loo_max": float(max(loo)), "subsamples": {k: {"effect": v[0], "se": v[1]} for k, v in subs.items()}}


def vertical_curve(depart=None, **kw) -> dict:
    """The net cost to rivals' customers of the vertical merger (their higher fees less the integrated distributor's
    saving) as the departure rate during a blackout varies: the input the trial turned on."""
    depart = np.linspace(0.0, 0.3, 61) if depart is None else np.asarray(depart, float)
    net = [vertical(depart=float(d), **kw)["net"] for d in depart]
    return {"depart": depart.tolist(), "net": net, "threshold": vertical(**kw)["threshold"]}


# ---------------------------------------------------------------------------------------------------------------
# regulated prices

def rate_case(rate_base: float = 500.0, allowed: float = 0.07, om: float = 40.0, depreciation: float = 20.0,
              taxes: float = 10.0, volume: float = 100.0) -> dict:
    """A cost-of-service rate case: the revenue requirement is operating costs, depreciation and taxes plus the
    allowed return on the rate base; the price is the requirement over the volume sold."""
    ret = allowed * rate_base
    req = om + depreciation + taxes + ret
    return {"om": om, "depreciation": depreciation, "taxes": taxes, "return": ret, "requirement": req,
            "price": req / volume, "allowed": allowed, "rate_base": rate_base}


def price_cap(years: int = 15, rpi: float = 0.03, X: float = 0.02, reset: int = 5, cost0: float = 1.0,
              g_cap: float = 0.04, g_cos: float = 0.01) -> dict:
    """A price cap, P_t = P_{t-1}(1 + RPI - X), reset to cost every ``reset`` years, against cost-of-service
    regulation in which the price follows cost each year.  Costs fall by ``g_cap`` a year in real terms when the
    firm keeps its savings until the next reset, and by ``g_cos`` when it passes them on at once (the effort each
    regime induces is assumed, not derived).  Nominal values; the firm's margin under the cap is the regulatory lag's
    reward."""
    t = np.arange(years + 1)
    infl = (1 + rpi) ** t
    c_cap = cost0 * infl * (1 - g_cap) ** t
    c_cos = cost0 * infl * (1 - g_cos) ** t
    p_cap = np.zeros(years + 1)
    p_cap[0] = cost0
    for k in range(1, years + 1):
        p_cap[k] = c_cap[k] if k % reset == 0 else p_cap[k - 1] * (1 + rpi - X)
    return {"t": t.tolist(), "cost_cap": c_cap.tolist(), "cost_cos": c_cos.tolist(), "price_cap": p_cap.tolist(),
            "price_cos": c_cos.tolist(), "rpi": rpi, "X": X, "reset": reset,
            "real_cap_end": float(p_cap[-1] / infl[-1]), "real_cos_end": float(c_cos[-1] / infl[-1])}


def ecpr(retail_price: float = 10.0, network_cost: float = 3.0, retail_cost: float = 2.0) -> dict:
    """Baumol and Willig's efficient component pricing rule: the access price is the incremental cost of access plus
    the incumbent's lost retail margin, so an entrant can profit only if its own retail cost is below the
    incumbent's."""
    margin = retail_price - network_cost - retail_cost
    access = network_cost + margin
    return {"retail_price": retail_price, "network_cost": network_cost, "retail_cost": retail_cost,
            "margin": margin, "access": access, "entrant_break_even": retail_price - access}


__all__ = [n for n in dir() if not n.startswith("_") and n not in ("np", "IO", "annotations")]
