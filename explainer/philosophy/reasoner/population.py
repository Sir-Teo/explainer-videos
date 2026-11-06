"""Population ethics and the far future, built (Part 36).

* Axiologies over populations (lists of (size, welfare) groups): total, average, critical-level, variable value
  (Hurka; Ng), and a prioritarian total.
* Parfit's sequence A, B, C, ..., Z: each step doubles the population and lowers welfare by slightly less than half.
* The mere addition paradox, step by step, and the Price List of the repugnant conclusion.
* An exhaustive check of each axiology against six conditions in the spirit of Arrhenius (2000), over small
  populations: the counterexample found for each violation.
* The non-identity problem: two policies, two different future populations.
* Discounting: the Ramsey rule with Stern's and Nordhaus's parameters; present values; Weitzman's declining
  certainty-equivalent rate.
* Existential risk: the value of reducing this century's risk under constant risk and under a time of perils
  (Thorstad 2023).
* Fanaticism: a chain of ever longer shots (Beckstead and Thomas), under expected value, bounded utility and
  probability discounting.
* Infinite streams: Pareto, anonymity, and the overtaking criterion; the Basu-Mitra construction on enumerated
  rationals.
* Cost-effectiveness with QALYs, and the value of a statistical life from a wage-risk trade-off.
* Broome's argument against neutrality; one climate policy under two discount rates; Parfit's three outcomes;
  QALYs against fair innings and priority.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

import numpy as np


# ---------------------------------------------------------------------------
# Axiologies
# ---------------------------------------------------------------------------
def _flat(pop):
    return [(int(n), float(w)) for n, w in pop if n > 0]


def total(pop) -> float:
    return sum(n * w for n, w in _flat(pop))


def average(pop) -> float:
    p = _flat(pop)
    N = sum(n for n, _ in p)
    return total(p) / N if N else 0.0


def critical_level(pop, c: float = 2.0) -> float:
    return sum(n * (w - c) for n, w in _flat(pop))


def variable_value(pop, k: float = 50.0) -> float:
    """Hurka (1983); Ng (1989): the average times a bounded, increasing function of the number of people."""
    p = _flat(pop)
    N = sum(n for n, _ in p)
    return average(p) * k * (1 - math.exp(-N / k)) if N else 0.0


def prioritarian(pop) -> float:
    """A prioritarian total: the sum of 10 (1 - exp(-w / 10)), increasing and concave at every welfare level, zero
    at zero."""
    return sum(n * 10 * (1 - math.exp(-w / 10)) for n, w in _flat(pop))


VIEWS = {"total": total, "average": average, "critical level": critical_level, "variable value": variable_value,
         "prioritarian": prioritarian}


# ---------------------------------------------------------------------------
# Parfit's sequence and the repugnant conclusion
# ---------------------------------------------------------------------------
def parfit_sequence(steps: int = 10, n0: int = 1, w0: float = 100.0, shrink: float = 0.55) -> dict:
    """A, B, C, ... : each step doubles the population and multiplies welfare by 0.55, so the total grows by 10% a
    step. After ten steps, Z: 1024 times the people, each with a life barely worth living."""
    rows = []
    for k in range(steps + 1):
        n, w = n0 * 2 ** k, w0 * shrink ** k
        pop = [(n, w)]
        rows.append({"name": "ABCDEFGHIJK"[k] if k < steps else "Z", "n": n, "w": round(w, 4),
                     **{v: round(f(pop), 4) for v, f in VIEWS.items()}})
    best = {v: max(rows, key=lambda r: r[v])["name"] for v in VIEWS}
    return {"rows": rows, "best": best, "growth": round(2 * shrink, 4)}


def mere_addition() -> dict:
    """Parfit's mere addition paradox. A: 10 people at 10. A+: the same, plus 10 people at 4 who affect no one.
    B: 20 people at 7.5, more total and more average than A+, and equal. B+: B plus 20 at 3; C: 40 at 5.5; and so
    on down. Each view's verdict at each step."""
    steps = [("A", [(10, 10.0)]), ("A+", [(10, 10.0), (10, 4.0)]), ("B", [(20, 7.5)]),
             ("B+", [(20, 7.5), (20, 3.0)]), ("C", [(40, 5.5)])]
    rows = []
    for name, pop in steps:
        rows.append({"name": name, "groups": [list(g) for g in pop], **{v: round(f(pop), 4) for v, f in VIEWS.items()}})
    verdicts = {}
    for v in VIEWS:
        vals = [r[v] for r in rows]
        verdicts[v] = {"A+ vs A": "better" if vals[1] > vals[0] else ("equal" if vals[1] == vals[0] else "worse"),
                       "B vs A+": "better" if vals[2] > vals[1] else "worse",
                       "B vs A": "better" if vals[2] > vals[0] else "worse",
                       "C vs A": "better" if vals[4] > vals[0] else "worse"}
    return {"rows": rows, "verdicts": verdicts}


# ---------------------------------------------------------------------------
# Arrhenius-style conditions, checked exhaustively on small populations
# ---------------------------------------------------------------------------
LEVELS = [10, 8, 4, 2, 1, -1, -2, -4]


def _pops(max_groups: int = 2, sizes=(1, 2, 5, 10, 20)):
    for g in range(1, max_groups + 1):
        for combo in itertools.product(sizes, LEVELS, repeat=g):
            yield [(combo[2 * i], float(combo[2 * i + 1])) for i in range(g)]


CONDITIONS = {
    "quality": "avoid the repugnant conclusion: no number of lives barely worth living beats 10 lives at 10",
    "mere addition": "adding lives worth living, affecting no one else, never makes things worse",
    "non-anti-egalitarianism": "same number of people, equal and larger in total: better",
    "non-sadism": "adding lives worth living is never worse than adding lives not worth living",
    "negative addition": "adding lives not worth living always makes things worse",
    "dominance": "everyone better off, same people: better",
}


def check(view: str) -> dict:
    """For each condition, search small populations for a counterexample against the given axiology."""
    f = VIEWS[view]
    out = {}
    A = [(10, 10.0)]
    # quality: Z = N lives at welfare 1, N up to a million
    z = next((N for N in [10 ** k for k in range(1, 7)] + [2 * 10 ** 6] if f([(N, 1.0)]) > f(A)), None)
    out["quality"] = {"holds": z is None, "example": None if z is None else f"{z} lives at 1 beat 10 lives at 10"}
    ex = None
    for base in _pops(1):
        for add_n in (1, 5, 20):
            for w in [x for x in LEVELS if x > 0]:
                if f(base + [(add_n, float(w))]) < f(base) - 1e-9:
                    ex = f"adding {add_n} at {w} to {base[0][0]} at {base[0][1]:g} makes it worse"
                    break
            if ex:
                break
        if ex:
            break
    out["mere addition"] = {"holds": ex is None, "example": ex}
    ex = None
    for n in (2, 4, 10):
        for a, b in itertools.combinations([x for x in LEVELS], 2):
            unequal = [(n // 2, float(a)), (n // 2, float(b))]
            tot = total(unequal)
            eq = [(n, tot / n + 0.5)]
            if f(eq) <= f(unequal) + 1e-9:
                ex = f"{n} people at {tot / n + 0.5:g} not better than half at {a}, half at {b}"
                break
        if ex:
            break
    out["non-anti-egalitarianism"] = {"holds": ex is None, "example": ex}
    ex = None
    for base in _pops(1):
        for pn, pw in itertools.product((1, 5, 20, 100), [x for x in LEVELS if x > 0]):
            for nn, nw in itertools.product((1, 5), [x for x in LEVELS if x < 0]):
                if f(base + [(nn, float(nw))]) > f(base + [(pn, float(pw))]) + 1e-9:
                    ex = (f"adding {nn} at {nw} beats adding {pn} at {pw}, to {base[0][0]} at {base[0][1]:g}")
                    break
            if ex:
                break
        if ex:
            break
    out["non-sadism"] = {"holds": ex is None, "example": ex}
    ex = None
    for strict in (True, False):
        for base in _pops(1):
            for nn, nw in itertools.product((1, 5), [x for x in LEVELS if x < 0]):
                after, before = f(base + [(nn, float(nw))]), f(base)
                if (after > before + 1e-9) if strict else (after >= before - 1e-9):
                    ex = (f"adding {nn} at {nw} to {base[0][0]} at {base[0][1]:g} makes it "
                          f"{'better' if strict else 'no worse'}")
                    break
            if ex:
                break
        if ex:
            break
    out["negative addition"] = {"holds": ex is None, "example": ex}
    ex = None
    for base in _pops(2):
        better = [(n, w + 1) for n, w in base]
        if f(better) <= f(base) + 1e-9:
            ex = f"raising everyone in {base} by 1 is not better"
            break
    out["dominance"] = {"holds": ex is None, "example": ex}
    return out


def arrhenius_table() -> dict:
    table = {v: check(v) for v in VIEWS}
    return {"conditions": CONDITIONS, "table": table,
            "violations": {v: [c for c, r in t.items() if not r["holds"]] for v, t in table.items()}}


# ---------------------------------------------------------------------------
# Non-identity
# ---------------------------------------------------------------------------
def non_identity() -> dict:
    """Parfit's depletion case. Depletion: we gain 10 each; in three centuries a different set of people exists,
    each at 40. Conservation: we gain nothing; different people exist, each at 60. No one who exists under depletion
    would have existed under conservation, and their lives are worth living."""
    now = 100
    later = 1000
    pol = {"depletion": {"now_gain": 10, "later_welfare": 40}, "conservation": {"now_gain": 0, "later_welfare": 60}}
    rows = []
    for name, p in pol.items():
        rows.append({"policy": name, "total": now * p["now_gain"] + later * p["later_welfare"],
                     "now": p["now_gain"], "later": p["later_welfare"]})
    # narrow person-affecting: is anyone worse off under depletion than they would otherwise be?
    harmed = 0          # the later people under depletion would not otherwise exist; the present gain
    return {"rows": rows, "now_people": now, "later_people": later, "harmed_by_depletion": harmed,
            "total_prefers": max(rows, key=lambda r: r["total"])["policy"]}


# ---------------------------------------------------------------------------
# Discounting
# ---------------------------------------------------------------------------
def ramsey() -> dict:
    """The Ramsey rule r = delta + eta g, with the parameters of the Stern Review (2006) and of Nordhaus's DICE
    (2008): present values of a million dollars of damage at several horizons; and Weitzman's (1998) certainty-
    equivalent rate when the rate is 1% or 5% with equal chance."""
    params = {"Stern": {"delta": 0.1, "eta": 1.0, "g": 1.3}, "Nordhaus": {"delta": 1.5, "eta": 2.0, "g": 2.0}}
    out = {}
    for k, p in params.items():
        r = p["delta"] + p["eta"] * p["g"]
        pv = {t: round(1e6 / (1 + r / 100) ** t, 0) for t in (50, 100, 200)}
        out[k] = {**p, "r": round(r, 3), "pv": pv,
                  "curve": [round(1 / (1 + r / 100) ** t, 5) for t in range(0, 201, 5)]}
    ratio = out["Stern"]["pv"][100] / out["Nordhaus"]["pv"][100]
    ts = list(range(1, 401, 4))
    ce = [round(-math.log(0.5 * math.exp(-0.01 * t) + 0.5 * math.exp(-0.05 * t)) / t * 100, 4) for t in ts]
    return {"views": out, "ratio_100": round(ratio, 1), "weitzman": {"t": ts, "rate": ce,
                                                                     "at": {t: round(-math.log(
                                                                         0.5 * math.exp(-0.01 * t) +
                                                                         0.5 * math.exp(-0.05 * t)) / t * 100, 3)
                                                                            for t in (1, 50, 100, 400)}}}


# ---------------------------------------------------------------------------
# Existential risk
# ---------------------------------------------------------------------------
def existential(risk: float = 1 / 6, low: float = 1e-4, cut: float = 0.01, centuries: int = 100000) -> dict:
    """Value of the future, in centuries of present value v = 1, if each century carries extinction risk r. Reducing
    this century's risk by an absolute amount d adds d / r_after: with constant risk 1/6, a point of reduction is
    worth 0.06 of a century; if risk then falls to 1 in 10,000 (a time of perils), it is worth 100 centuries
    (Thorstad 2023). Checked by summing the series."""
    def value(r1, r_after):
        s, alive = 0.0, 1.0 - r1
        for _ in range(centuries):
            s += alive
            alive *= (1 - r_after)
            if alive < 1e-12:
                break
        return s
    const = value(risk - cut, risk) - value(risk, risk)
    perils = value(risk - cut, low) - value(risk, low)
    return {"risk": risk, "low": low, "cut": cut, "constant_gain": round(const, 4), "perils_gain": round(perils, 2),
            "closed_constant": round(cut / risk, 4), "closed_perils": round(cut / low, 2),
            "future_constant": round(value(risk, risk), 3), "future_perils": round(value(risk, low), 1)}


# ---------------------------------------------------------------------------
# Fanaticism
# ---------------------------------------------------------------------------
def fanaticism(steps: int = 12, shrink: float = 0.5, grow: float = 10.0, bound: float = 1000.0,
               threshold: float = 1e-3) -> dict:
    """A chain of lotteries (Beckstead and Thomas): L0 is a sure 1; each next lottery halves the chance and
    multiplies the prize by ten. Expected value prefers every step, so by transitivity a 1-in-4096 shot at 10^12 beats
    the sure thing. A bounded utility u(x) = x / (x + K) stops climbing; discounting probabilities below 1/1000 to
    zero stops at a threshold, and so breaks a step that looks no different from the others."""
    rows = []
    for k in range(steps + 1):
        p, x = shrink ** k, grow ** k
        ev = p * x
        bu = p * x / (x + bound)
        pd = 0.0 if p < threshold else p * x
        rows.append({"k": k, "p": p, "prize": x, "ev": ev, "bounded": round(bu, 6), "discounted": pd})
    peak_bounded = max(rows, key=lambda r: r["bounded"])["k"]
    first_drop = next(r["k"] for r in rows if r["discounted"] == 0.0)
    return {"rows": rows, "peak_bounded": peak_bounded, "discount_breaks_at": first_drop, "bound": bound,
            "threshold": threshold}


# ---------------------------------------------------------------------------
# Infinite streams
# ---------------------------------------------------------------------------
def _rationals(n: int):
    """The first n rationals in (0, 1), by the Calkin-Wilf-like enumeration of reduced fractions p/q, q = 2, 3, ..."""
    out = []
    q = 2
    while len(out) < n:
        for p in range(1, q):
            if math.gcd(p, q) == 1:
                out.append(Fraction(p, q))
                if len(out) == n:
                    break
        q += 1
    return out


def infinite(n: int = 40, r: float = 0.3, s: float = 0.45) -> dict:
    """Two streams that are permutations of each other, (1, 0, 1, 0, ...) and (0, 1, 0, 1, ...): the catching-up
    criterion ranks the first above the second, though an infinite permutation maps one onto the other. And the
    Basu-Mitra construction (2003): enumerate the rationals q_1, q_2, ...; x(r)_n = 1 if q_n < r. For r < s, x(s) is
    at least x(r) everywhere and above it infinitely often."""
    T = 40
    a = [1 if t % 2 == 0 else 0 for t in range(T)]
    b = [1 - v for v in a]
    diff = list(itertools.accumulate(x - y for x, y in zip(a, b)))
    qs = _rationals(n)
    xr = [1 if q < r else 0 for q in qs]
    xs = [1 if q < s else 0 for q in qs]
    m = next(i for i, q in enumerate(qs) if q >= r)          # y(r): one more 1, at the first q_n >= r
    j = next(i for i, q in enumerate(qs) if r <= q < s)      # a place between r and s to swap it into
    yr = list(xr)
    yr[m] = 1
    swapped = list(yr)
    swapped[m], swapped[j] = swapped[j], swapped[m]
    if qs[m] < s:
        swapped = list(yr)                                   # no swap needed: y(r) is already below x(s)
    dominated = all(u <= v for u, v in zip(swapped, xs)) and sum(v - u for u, v in zip(swapped, xs)) > 0
    return {"a": a, "b": b, "partial_diff": diff, "liminf_ab": min(diff[10:]), "liminf_ba": min(-d for d in diff[10:]),
            "rationals": [str(q) for q in qs], "x_r": xr, "x_s": xs, "y_r": yr, "m": m, "j": j, "swapped": swapped,
            "dominated_after_swap": dominated, "r": r, "s": s}


# ---------------------------------------------------------------------------
# Cost-effectiveness and the value of a statistical life
# ---------------------------------------------------------------------------
def cost_effectiveness(n: int = 200, seed: int = 2009, budget: float = 1e6) -> dict:
    """A toy portfolio of 200 interventions, with cost per QALY drawn log-normally (a heavy tail, as in the
    published surveys of health interventions). Fund in order of cost-effectiveness: the QALYs a fixed budget buys if
    spent on the best, the median, or spread evenly."""
    rng = np.random.default_rng(seed)
    cost = np.exp(rng.normal(math.log(5000), 1.6, n))          # dollars per QALY
    eff = 1 / cost
    best = float(budget * eff.max())
    median = float(budget / np.median(cost))
    spread = float(budget * eff.mean())
    order = np.sort(cost)
    return {"n": n, "budget": budget, "best_cost": round(float(order[0]), 1), "median_cost": round(float(np.median(cost)), 0),
            "worst_cost": round(float(order[-1]), 0), "qalys_best": round(best, 0), "qalys_median": round(median, 1),
            "qalys_spread": round(spread, 1), "ratio_best_median": round(best / median, 1),
            "sorted_log10": [round(float(math.log10(c)), 3) for c in order]}


def vsl(premium: float = 1200.0, risk: float = 1e-4) -> dict:
    """The value of a statistical life from a wage-risk trade-off: workers who accept 1 in 10,000 more annual risk of
    death for 1,200 dollars more a year value a statistical life at 1,200 / 0.0001 = 12 million dollars. A safety rule
    costing 20 million dollars that prevents 2 expected deaths passes; one costing 40 million that prevents 3 does not
    at 12 million per life, but would at 14 million."""
    v = premium / risk
    rules = [{"rule": "guard rails", "cost": 20e6, "lives": 2.0}, {"rule": "rear cameras", "cost": 40e6, "lives": 3.0}]
    for r in rules:
        r["benefit"] = r["lives"] * v
        r["passes"] = r["benefit"] >= r["cost"]
        r["breakeven_vsl"] = r["cost"] / r["lives"]
    return {"premium": premium, "risk": risk, "vsl": v, "rules": rules}


def very_repugnant(agony: float = -50.0, barely: float = 0.25) -> dict:
    """Arrhenius's very repugnant conclusion on the total view: A, one unit of population at 100, is worse than a
    world with as many lives in agony at -50 plus enough lives barely worth living. The least number of units."""
    A = [(1, 100.0)]
    N = next(n for n in range(1, 10 ** 6) if total([(1, agony), (n, barely)]) > total(A))
    return {"A": total(A), "agony": agony, "barely": barely, "units": N, "z_total": total([(1, agony), (N, barely)])}


# ---------------------------------------------------------------------------
# Neutrality (Broome 2004)
# ---------------------------------------------------------------------------
def neutrality(base: float = 10.0, levels=(2, 4, 6, 8)) -> dict:
    """The intuition of neutrality: adding a person at any level in a range is equally as good as not adding her.
    A: one person at 10. A_l: the same, plus a new person at level l. Neutrality says A ~ A_l for every l in the
    range; transitivity of `equally good' then gives A_l ~ A_m; but A_m is better than A_l for m > l (the same
    people, the new person better off). Every pair is a contradiction, so the neutral range can hold at most one
    level (Broome)."""
    pairs = [(l, m) for i, l in enumerate(levels) for m in levels[i + 1:]]
    contradictions = [{"lower": l, "higher": m, "neutrality_says": "equal", "pareto_says": f"{m} better"}
                      for l, m in pairs]
    return {"base": base, "levels": list(levels), "contradictions": contradictions, "count": len(contradictions)}


# ---------------------------------------------------------------------------
# One climate policy, two discount rates
# ---------------------------------------------------------------------------
def climate_policy(cost_share: float = 0.01, damage_share: float = 0.05, horizon: int = 100) -> dict:
    """Spend 1% of today's output to avoid a loss of 5% of output in 100 years. Output grows at g; the benefit is
    discounted at the Ramsey rate. Stern's parameters say yes; Nordhaus's say no."""
    out = {}
    for k, (delta, eta, g) in {"Stern": (0.1, 1.0, 1.3), "Nordhaus": (1.5, 2.0, 2.0)}.items():
        r = delta + eta * g
        gdp_later = 100 * (1 + g / 100) ** horizon
        benefit = damage_share * gdp_later
        pv = benefit / (1 + r / 100) ** horizon
        out[k] = {"r": round(r, 3), "gdp_later": round(gdp_later, 1), "benefit": round(benefit, 2),
                  "pv": round(pv, 3), "cost": 100 * cost_share, "worth_it": pv > 100 * cost_share}
    return out


# ---------------------------------------------------------------------------
# Parfit's three outcomes
# ---------------------------------------------------------------------------
def three_outcomes(present: float = 8e9, future: float = 1e16) -> dict:
    """Reasons and Persons, p. 453: (1) peace; (2) a war that kills 99% of the world's existing population; (3) a war
    that kills 100%. Which difference is greater, (1)-(2) or (2)-(3)? Count lives lost. A narrow person-affecting
    view counts only existing people; the total view also counts the future that (3) prevents (Bostrom's
    conservative 10^16 lives; humanity recovers after (2))."""
    pa_12, pa_23 = 0.99 * present, 0.01 * present
    tot_12, tot_23 = 0.99 * present, 0.01 * present + future
    return {"present": present, "future": future,
            "person_affecting": {"d12": pa_12, "d23": pa_23, "ratio_23_12": round(pa_23 / pa_12, 5)},
            "total": {"d12": tot_12, "d23": tot_23, "ratio_23_12": round(tot_23 / tot_12, 0)}}


# ---------------------------------------------------------------------------
# QALYs and fairness
# ---------------------------------------------------------------------------
def qaly_allocation() -> dict:
    """One course of treatment, three patients who would each die without it (Harris 1987's double jeopardy).
    QALY maximization treats the one with the most quality-weighted years to gain; a fair-innings weighting
    (Williams 1997) and a prioritarian weighting by how badly off each patient's life would otherwise go change
    the answer."""
    pts = [{"patient": "aged 30", "years": 40, "quality": 1.0, "lived": 30},
           {"patient": "aged 30, with a disability", "years": 40, "quality": 0.5, "lived": 30},
           {"patient": "aged 70", "years": 12, "quality": 1.0, "lived": 70}]
    for p in pts:
        p["qalys"] = p["years"] * p["quality"]
        # fair innings: weight gains to those short of 70 years more heavily
        p["fair_innings"] = round(p["qalys"] * (2.0 if p["lived"] < 70 else 0.5), 2)
        # priority to the worse off: weight by 1 / (QALYs the patient would have over a whole life)
        lifetime = p["lived"] * p["quality"] + p["qalys"]
        p["priority"] = round(p["qalys"] * (100 / lifetime), 2)
    best = {k: max(pts, key=lambda p: p[k])["patient"] for k in ("qalys", "fair_innings")}
    return {"patients": pts, "best": best}


def sadistic_example(c: float = 2.0) -> dict:
    """Arrhenius's sadistic conclusion on a critical-level view: to a world of one person at 10, adding one life in
    misery at -1 scores higher than adding five lives worth living at 1, since each life below c counts against."""
    base = [(1, 10.0)]
    neg, pos = base + [(1, -1.0)], base + [(5, 1.0)]
    return {"c": c, "base": critical_level(base, c), "with_misery": critical_level(neg, c),
            "with_good_lives": critical_level(pos, c), "total_with_misery": total(neg), "total_with_good": total(pos)}


def stern_hazard(delta: float = 0.1, ord_century: float = 1 / 6) -> dict:
    """Stern's pure time preference of 0.1% a year, read as an annual chance of extinction: the chance of surviving a
    century, and a millennium; and the annual rate implied by Ord's 1 in 6 for this century."""
    h = delta / 100
    return {"delta": delta, "survive_100": round((1 - h) ** 100, 4), "survive_1000": round((1 - h) ** 1000, 4),
            "ord_annual": round(-math.log(1 - ord_century) / 100 * 100, 4),
            "ord_survive_100": round(1 - ord_century, 4)}


def benign_addition() -> dict:
    """Arrhenius's benign addition, pressed by Huemer (2008): from A, ten people at 10, to A++, the same ten at 10.5
    plus ten new people at 4. Everyone who exists in A is better off, and the added lives are good; the average view
    still calls A++ worse."""
    A, App = [(10, 10.0)], [(10, 10.5), (10, 4.0)]
    return {"A": {v: round(f(A), 4) for v, f in VIEWS.items()}, "A++": {v: round(f(App), 4) for v, f in VIEWS.items()},
            "worse_by": [v for v, f in VIEWS.items() if f(App) < f(A)]}


def moral_weights() -> dict:
    """Who counts? A toy: expected moral weight = numbers x probability of sentience x welfare range, per human.
    Three invented kinds of being, increasingly numerous and increasingly unlikely to be sentient."""
    kinds = [{"kind": "humans", "n": 1, "p": 1.0, "range": 1.0},
             {"kind": "kind B", "n": 3, "p": 0.9, "range": 0.5},
             {"kind": "kind C", "n": 100, "p": 0.3, "range": 0.05},
             {"kind": "kind D", "n": 10 ** 6, "p": 0.01, "range": 0.001}]
    for k in kinds:
        k["weight"] = round(k["n"] * k["p"] * k["range"], 4)
    return {"kinds": kinds, "largest": max(kinds, key=lambda k: k["weight"])["kind"]}


def harm_minimizing() -> dict:
    """Meacham's harm-minimizing view (2012), simplified. People in different outcomes are matched one to one by
    their places (a saturating counterpart relation). A person is harmed in an outcome by the amount her counterpart
    does better elsewhere; people with no counterpart, living good lives, are not harmed. Choose the outcome with
    the least total harm. Run on Parfit's depletion case and on A against Z."""
    def harms(groups_w, groups_alt):
        # groups: lists of welfare levels in place order; counterparts by index
        h = 0.0
        for i, w in enumerate(groups_w):
            if i < len(groups_alt):
                h += max(0.0, groups_alt[i] - w)
        return h
    dep = [10.0] * 100 + [40.0] * 1000
    con = [0.0] * 100 + [60.0] * 1000
    A = [100.0] * 10
    Z = [0.25] * 10240
    return {"depletion_harm": harms(dep, con), "conservation_harm": harms(con, dep),
            "A_harm": harms(A, Z), "Z_harm": harms(Z, A),
            "choose_depletion_case": "conservation" if harms(con, dep) < harms(dep, con) else "depletion",
            "choose_AZ": "A" if harms(A, Z) < harms(Z, A) else "Z"}


def vsl_transfer(vsl_us: float = 12e6, ratios=(1.0, 0.2, 0.05, 0.02), elasticities=(0.8, 1.0, 1.2)) -> dict:
    """Benefit transfer: the value of a statistical life in a country with income a fraction y of the United States',
    VSL_US x y^e, for income elasticities e. The ratio of lives' prices across countries is the ratio of incomes to
    the power e."""
    rows = []
    for y in ratios:
        rows.append({"ratio": y, **{str(e): round(vsl_us * y ** e, -3) for e in elasticities}})
    return {"vsl_us": vsl_us, "elasticities": list(elasticities), "rows": rows}
