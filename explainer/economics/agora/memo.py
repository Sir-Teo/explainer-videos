"""Agora's policy memo (Part 50): a child allowance for the Island, analysed from the question to the advice.

* **The two credits** (:func:`ctc_2020`, :func:`allowance_2021`), on top of the 2021 earned income tax credit
  (:func:`eitc_2021`), which both systems keep: the child tax credit as it stood before 2021
  (2,000 a child, of which at most 1,400 refundable, phased in at 15% of earnings above 2,500) against a fully
  refundable allowance (3,600 a child under six, 3,000 for older children, the extra above 2,000 phased out at 5% above
  75,000 for a single parent and 150,000 for a couple); with :func:`income_tax`, a simple version of the 2021 federal
  income tax for the nonrefundable part.
* **The Island's families** (:func:`families`): parents with children, single or married, with earnings potentials,
  work decisions and children of each age, calibrated loosely to the United States.
* **Behaviour** (:func:`simulate`): parents decide whether to work by comparing what work adds to what it costs them;
  the change in that net return, through a participation elasticity, and an income effect move them; the results:
  child poverty against an Island line, the budget cost, earnings.
* **One number and its uncertainty** (:func:`mvpf`, :func:`tornado`): the marginal value of public funds with the
  fiscal externalities of changed work and, if counted, of children's later earnings; how each dial moves the answer.

numpy only.
"""

from __future__ import annotations

import numpy as np

# 2021 federal income tax, a simplified schedule (standard deduction, brackets) for single heads of household and
# married couples filing jointly
STD = {0: 18800.0, 1: 25100.0}
BRACKETS = {0: ((14200.0, 0.10), (54200.0, 0.12), (86350.0, 0.22), (164900.0, 0.24), (np.inf, 0.32)),
            1: ((19900.0, 0.10), (81050.0, 0.12), (172750.0, 0.22), (329850.0, 0.24), (np.inf, 0.32))}


def income_tax(earnings, married):
    """Income tax before credits, 2021 schedule, simplified (no other income, deductions or credits)."""
    e = np.asarray(earnings, float)
    m = np.asarray(married, int)
    out = np.zeros_like(e)
    for k in (0, 1):
        sel = m == k
        taxable = np.maximum(e[sel] - STD[k], 0.0)
        t = np.zeros_like(taxable)
        lo = 0.0
        for hi, r in BRACKETS[k]:
            t += r * np.clip(taxable - lo, 0.0, hi - lo)
            lo = hi
        out[sel] = t
    return out


EITC = {1: (0.34, 10640.0, 3618.0, 0.1598), 2: (0.40, 14950.0, 5980.0, 0.2106), 3: (0.45, 14950.0, 6728.0, 0.2106)}


def eitc_2021(earnings, kids, married):
    """The earned income tax credit for families with children, 2021: phased in with earnings (34%, 40% or 45% for
    one, two, three or more children) to a maximum, flat, then phased out above 19,520 (25,470 for a couple)."""
    e = np.asarray(earnings, float)
    k = np.minimum(np.asarray(kids, int), 3)
    m = np.asarray(married, int)
    out = np.zeros_like(e)
    for c, (r_in, _, mx, r_out) in EITC.items():
        sel = k == c
        start = 19520.0 + 5950.0 * m[sel]
        out[sel] = np.maximum(np.minimum(r_in * e[sel], mx) - r_out * np.maximum(e[sel] - start, 0.0), 0.0)
    return out


def ctc_2020(earnings, kids, married):
    """The child tax credit before 2021: 2,000 a child; the refundable part at most 1,400 a child and 15% of earnings
    above 2,500; the rest only against income tax; phased out at 5% above 200,000 (400,000 for a couple)."""
    e = np.asarray(earnings, float)
    k = np.asarray(kids, float)
    m = np.asarray(married, int)
    full = 2000.0 * k
    start = np.where(m == 1, 400000.0, 200000.0)
    full = np.maximum(full - 0.05 * np.maximum(e - start, 0.0), 0.0)
    refundable = np.minimum(1400.0 * k, 0.15 * np.maximum(e - 2500.0, 0.0))
    liability = income_tax(e, m)
    return np.minimum(full, np.maximum(refundable, np.minimum(full, liability + refundable)))


def allowance_2021(earnings, young, older, married):
    """The 2021 design made permanent: 3,600 a child under six and 3,000 for children six to seventeen, fully
    refundable; the amount above 2,000 a child phased out at 5% above 75,000 (150,000 for a couple), and the rest as
    before 2021 above 200,000 (400,000)."""
    e = np.asarray(earnings, float)
    y, o = np.asarray(young, float), np.asarray(older, float)
    m = np.asarray(married, int)
    extra = 1600.0 * y + 1000.0 * o
    extra = np.maximum(extra - 0.05 * np.maximum(e - np.where(m == 1, 150000.0, 75000.0), 0.0), 0.0)
    base = 2000.0 * (y + o)
    base = np.maximum(base - 0.05 * np.maximum(e - np.where(m == 1, 400000.0, 200000.0), 0.0), 0.0)
    return base + extra


def hybrid_2021(earnings, young, older, married):
    """The allowance with a work requirement kept: the old credit exactly as before (phased in with earnings), plus
    the 2021 extra (1,600 a child under six, 1,000 an older child) paid whatever the family earns, phased out as in
    :func:`allowance_2021`."""
    e = np.asarray(earnings, float)
    y, o = np.asarray(young, float), np.asarray(older, float)
    m = np.asarray(married, int)
    extra = 1600.0 * y + 1000.0 * o
    extra = np.maximum(extra - 0.05 * np.maximum(e - np.where(m == 1, 150000.0, 75000.0), 0.0), 0.0)
    return ctc_2020(e, y + o, m) + extra


def families(n: int = 40000, married_share: float = 0.65, seed: int = 0) -> dict:
    """The Island's families with children: married or single; one to four children, each under six with probability
    0.35; the potential earnings of the family's main worker log-normal (median 52,000 for a couple, 28,000 for a single
    parent, log-sd 0.75), plus a second earner in six couples in ten; whether the main worker works is decided by
    :func:`simulate`, calibrated so that about 85% of single parents and 95% of couples' main earners work under
    the old credit."""
    rng = np.random.default_rng(seed)
    married = (rng.random(n) < married_share).astype(int)
    kids = rng.choice([1, 2, 3, 4], size=n, p=[0.42, 0.37, 0.15, 0.06])
    young = rng.binomial(kids, 0.35)
    older = kids - young
    med = np.where(married == 1, 52000.0, 28000.0)
    pot = med * np.exp(0.75 * rng.standard_normal(n))
    second = np.where(married == 1, 0.6 * med * np.exp(0.8 * rng.standard_normal(n)) * (rng.random(n) < 0.6), 0.0)
    return {"n": n, "married": married, "kids": kids, "young": young, "older": older, "potential": pot,
            "second": second}


def _net_income(F, work, policy):
    e = np.where(work, F["potential"], 0.0) + F["second"]
    tax = income_tax(e, F["married"]) - eitc_2021(e, F["kids"], F["married"])
    if policy == "ctc":
        credit = ctc_2020(e, F["kids"], F["married"])
    elif policy == "hybrid":
        credit = hybrid_2021(e, F["young"], F["older"], F["married"])
    else:
        credit = allowance_2021(e, F["young"], F["older"], F["married"])
    return e - tax + credit, e, tax, credit


def poverty_line(married, kids, base: float = 24000.0):
    """The Island's poverty line: ``base`` for two adults and two children, scaled by the square root of family
    size."""
    size = 1 + np.asarray(married) + np.asarray(kids)
    return base * np.sqrt(size / 4.0)


def simulate(F: dict, policy: str, elasticity: float = 0.25, income_effect: float = 0.0, take_up: float = 1.0,
             line_base: float = 24000.0, seed: int = 0) -> dict:
    """Who works under ``policy`` ("ctc", "allowance" or "hybrid"), and the outcomes.  A main worker's probability
    of working is
    a logistic function of the log net gain from work (net income working minus not working, against potential
    earnings) with slope set so that the participation elasticity at the old credit is ``elasticity``; an income
    effect lowers it by ``income_effect`` x (unearned transfer / potential earnings).  With ``take_up`` < 1 some
    families do not receive the allowance (the old credit is assumed received).  Returns poverty, cost and work."""
    rng = np.random.default_rng(seed)
    n = F["n"]
    u_work = rng.random(n)                 # the same draws under every policy: the comparison is like for like
    u_take = rng.random(n)
    y1, _, _, _ = _net_income(F, np.ones(n, bool), "ctc")
    y0, _, _, _ = _net_income(F, np.zeros(n, bool), "ctc")
    gain_ctc = np.maximum(y1 - y0, 1.0) / F["potential"]
    # calibrate the intercept so that 85% of single parents and 95% of couples' main earners work under the old credit
    target = np.where(F["married"] == 1, 0.95, 0.85)
    # participation probability P = 1 / (1 + exp(-(a + b log gain)))
    # elasticity dP/dlog(gain) / P = b (1 - P); set b so that the average elasticity is ``elasticity``
    b = elasticity / max(float(np.mean(1 - target)), 1e-9)
    a = np.log(target / (1 - target)) - b * np.log(gain_ctc)
    if policy == "ctc":
        gain = gain_ctc
        transfer0 = 0.0
    else:
        z1, _, _, _ = _net_income(F, np.ones(n, bool), policy)
        z0, _, _, _ = _net_income(F, np.zeros(n, bool), policy)
        gain = np.maximum(z1 - z0, 1.0) / F["potential"]
        transfer0 = (z0 - y0) / F["potential"]
    index = a + b * np.log(gain) - income_effect * transfer0
    p_work = 1.0 / (1.0 + np.exp(-index))
    work = u_work < p_work
    got = u_take < take_up if policy != "ctc" else np.ones(n, bool)
    inc, e, tax, credit = _net_income(F, work, policy)
    if policy != "ctc":
        inc_old, _, _, credit_old = _net_income(F, work, "ctc")
        inc = np.where(got, inc, inc_old)
        credit = np.where(got, credit, credit_old)
    line = poverty_line(F["married"], F["kids"], line_base)
    poor = inc < line
    kids = F["kids"]
    return {"work": work, "income": inc, "earnings": e, "tax": tax, "credit": credit, "poor": poor,
            "child_poverty": float(np.sum(kids * poor) / np.sum(kids)),
            "deep": float(np.sum(kids * (inc < 0.5 * line)) / np.sum(kids)),
            "work_single": float(np.mean(work[F["married"] == 0])),
            "work_married": float(np.mean(work[F["married"] == 1])), "p_work": p_work}


def compare(F: dict, elasticity: float = 0.25, income_effect: float = 0.0, take_up: float = 1.0,
            line_base: float = 24000.0, seed: int = 0, policy: str = "allowance") -> dict:
    """The old credit against the allowance (or ``policy``) for the same families and the same random draws: child
    poverty, deep poverty, the budget cost (credits paid plus taxes lost), work, and the change in earnings.  The
    static numbers (``static_child_poverty``, ``static_cost``) hold work at the old credit's and assume full
    take-up."""
    old = simulate(F, "ctc", elasticity, income_effect, 1.0, line_base, seed=seed)
    new = simulate(F, policy, elasticity, income_effect, take_up, line_base, seed=seed)
    cost = float(np.sum(new["credit"] - old["credit"]) - np.sum(new["tax"] - old["tax"]))
    mech = old["work"]
    static_new = _net_income(F, mech, policy)
    static_cost = float(np.sum(static_new[3] - old["credit"]))
    line = poverty_line(F["married"], F["kids"], line_base)
    static_poor = static_new[0] < line
    kids = F["kids"]
    return {"old": {k: old[k] for k in ("child_poverty", "deep", "work_single", "work_married")},
            "new": {k: new[k] for k in ("child_poverty", "deep", "work_single", "work_married")},
            "static_child_poverty": float(np.sum(kids * static_poor) / np.sum(kids)),
            "cost": cost, "static_cost": static_cost, "per_child": cost / float(np.sum(kids)),
            "exits": float(np.sum(old["work"]) - np.sum(new["work"])), "parents": int(F["n"]),
            "earnings_change": float(np.sum(new["earnings"] - old["earnings"])),
            "old_income": old["income"], "new_income": new["income"], "old_work": old["work"],
            "new_work": new["work"]}


def mvpf(wtp: float, cost: float, child_return: float = 0.0) -> float:
    """Willingness to pay over net cost, with an optional fiscal return from children's later earnings (in the same
    units, discounted) that lowers the net cost."""
    net = cost - child_return
    return float("inf") if net <= 0 else wtp / net


def top_mcpf(tau: float, a: float, e: float) -> float:
    """The marginal cost of public funds raised by the top rate ``tau``: with Pareto incomes of exponent ``a`` above
    the threshold and an elasticity of taxable income ``e``, each dollar of mechanical revenue loses tau a e/(1 - tau)
    to smaller reported incomes, so a dollar of net revenue costs top earners (1 - tau)/(1 - tau - tau a e)."""
    den = 1.0 - tau - tau * a * e
    return float("inf") if den <= 0 else (1.0 - tau) / den


def tornado(F: dict, base: dict, ranges: dict, metric: str = "child_poverty", seed: int = 0) -> list:
    """How the child poverty rate under the allowance (or another metric of :func:`compare`) moves as each dial takes
    its low and high value with the others at ``base``."""
    out = []
    for name, (lo, hi) in ranges.items():
        vals = []
        for v in (lo, hi):
            kw = {**base, name: v}
            r = compare(F, seed=seed, **kw)
            vals.append(r["new"][metric] if metric in r["new"] else r[metric])
        out.append({"dial": name, "low": lo, "high": hi, "at_low": vals[0], "at_high": vals[1]})
    return out


__all__ = ["income_tax", "eitc_2021", "ctc_2020", "allowance_2021", "hybrid_2021", "families", "poverty_line",
           "simulate",
           "compare", "mvpf", "top_mcpf", "tornado"]
