"""The capstone pipeline of *Psychology, Built* (Part 43): a replication planned as code before the data are read.

A :class:`Plan` is the preregistration: the target, the original estimate, the smallest effect of interest, the
estimator, the exclusion rule and the three criteria for calling the result a replication.  :func:`dry_run` runs
the frozen analysis on labs simulated from the Pool's kind of data (no effect, the original effect, the smallest
effect of interest), before any real data are touched.  :func:`analyse` applies the same frozen analysis to the
real lab-level data and returns the confirmatory result; :func:`verdict` applies the three criteria; and
:func:`multiverse` is the labelled exploratory analysis.

* :func:`d33` and :func:`power2`: Simonsohn's (2015) small-telescopes benchmark, the effect an original study of
  two groups had 33% power to detect, and two-group power by the noncentral t distribution.
* :func:`n_per_group`: the sample size per group for a power target at a given effect.
* :func:`replication_bf`: Verhagen and Wagenmakers's (2014) replication Bayes factor, in its normal approximation:
  the density of the replication estimate under the original study's posterior, against its density under no
  effect.
* :func:`risk_difference` and :func:`hedges_g`: per-lab effects for a binary and a continuous outcome.
* :func:`pool`: DerSimonian and Laird's random-effects estimate with its 95% interval.

Everything is deterministic given its seed; nothing here reads the real data except :func:`analyse`, which is
called once, after the plan is frozen.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy import optimize, stats

__all__ = ["Plan", "power2", "d33", "d33_rd", "n_per_group", "replication_bf", "risk_difference", "hedges_g", "pool",
           "simulate_labs", "dry_run", "analyse", "verdict", "multiverse"]


@dataclass(frozen=True)
class Plan:
    """A preregistration.  ``sign`` is the direction the original predicts (+1 or -1) in the effect's units;
    ``original`` and ``original_se`` its estimate; ``sesoi`` the smallest effect of interest, in the same units
    (positive, compared with sign * effect); ``alpha`` the one-sided level of the test in the predicted
    direction; ``min_n`` the smallest lab kept (the exclusion rule)."""

    target: str
    outcome: str
    sign: int
    original: float
    original_se: float
    sesoi: float
    alpha: float = 0.05
    min_n: int = 0
    estimator: str = "random effects (DerSimonian-Laird)"
    criteria: tuple = field(default=("significant in the predicted direction",
                                     "the original estimate inside the 95% interval",
                                     "the interval's upper end not below the small-telescopes benchmark d33"))


def power2(d: float, n1: int, n2: int, alpha: float = 0.05) -> float:
    """Two-sided power of a two-group t test for a standardized effect d."""
    df = n1 + n2 - 2
    nc = d * np.sqrt(n1 * n2 / (n1 + n2))
    t = stats.t.ppf(1 - alpha / 2, df)
    upper, lower = stats.nct.sf(t, df, nc), stats.nct.cdf(-t, df, nc)
    return float(np.nan_to_num(upper, nan=1.0) + np.nan_to_num(lower, nan=0.0))


def d33(n1: int, n2: int) -> float:
    """The effect the original two-group study had 33% power to detect (Simonsohn's small telescopes)."""
    return float(optimize.brentq(lambda d: power2(d, n1, n2) - 1 / 3, 1e-6, 2.5))


def d33_rd(p0: float, n1: int, n0: int) -> float:
    """The difference in proportions (from a control rate p0, in either direction toward 0.5) that a two-group
    study had 33% power to detect, by the normal approximation."""
    z = stats.norm.ppf(0.975)

    def pw(rd):
        p1 = p0 - rd
        se = np.sqrt(p1 * (1 - p1) / n1 + p0 * (1 - p0) / n0)
        return stats.norm.sf(z - rd / se) + stats.norm.cdf(-z - rd / se)

    return float(optimize.brentq(lambda rd: pw(rd) - 1 / 3, 1e-6, min(p0, 0.99) - 1e-6))


def n_per_group(d: float, target: float = 0.95, alpha: float = 0.05) -> int:
    """The smallest equal group size giving two-sided power ``target`` at effect d."""
    n = 2
    while power2(d, n, n, alpha) < target:
        n += 1
    return n


def replication_bf(orig: float, orig_se: float, rep: float, rep_se: float) -> float:
    """BF_r0: N(rep; orig, orig_se^2 + rep_se^2) / N(rep; 0, rep_se^2).  Above 1 favours the effect the original
    reported, below 1 favours no effect."""
    num = stats.norm.pdf(rep, orig, np.sqrt(orig_se ** 2 + rep_se ** 2))
    den = stats.norm.pdf(rep, 0.0, rep_se)
    return float(num / den)


def risk_difference(k1, n1, k2, n2):
    """Per-lab difference in proportions (group 1 minus group 2) and its variance."""
    p1, p2 = np.asarray(k1, float) / n1, np.asarray(k2, float) / n2
    return p1 - p2, p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2


def hedges_g(m1, s1, n1, m2, s2, n2):
    """Per-lab Hedges's g (group 1 minus group 2) and its variance."""
    m1, s1, n1, m2, s2, n2 = (np.asarray(x, float) for x in (m1, s1, n1, m2, s2, n2))
    sp = np.sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2))
    g = (1 - 3 / (4 * (n1 + n2) - 9)) * (m1 - m2) / sp
    return g, (n1 + n2) / (n1 * n2) + g ** 2 / (2 * (n1 + n2))


def pool(y, v, method: str = "DL") -> dict:
    """Fixed ("FE") or DerSimonian-Laird random-effects ("DL") pooling: estimate, SE, 95% interval, tau^2, I^2."""
    y, v = np.asarray(y, float), np.asarray(v, float)
    w = 1 / v
    fe = float(np.sum(w * y) / w.sum())
    Q = float(np.sum(w * (y - fe) ** 2))
    k = len(y)
    tau2 = 0.0 if method == "FE" else float(max(0.0, (Q - (k - 1)) / (w.sum() - (w ** 2).sum() / w.sum())))
    ws = 1 / (v + tau2)
    est = float(np.sum(ws * y) / ws.sum())
    se = float(np.sqrt(1 / ws.sum()))
    return {"est": est, "se": se, "lo": est - 1.96 * se, "hi": est + 1.96 * se, "tau2": tau2,
            "I2": max(0.0, (Q - (k - 1)) / Q) if Q > 0 else 0.0, "k": k}


def simulate_labs(k: int, n: int, d: float, tau: float = 0.05, seed: int = 0) -> dict:
    """k labs of n per group with a continuous outcome, true standardized effect d and between-lab SD tau."""
    rng = np.random.default_rng(seed)
    th = rng.normal(d, tau, k)
    a = [rng.normal(t, 1, n) for t in th]
    b = [rng.normal(0, 1, n) for _ in th]
    return {"m1": np.array([x.mean() for x in a]), "s1": np.array([x.std(ddof=1) for x in a]), "n1": np.full(k, n),
            "m2": np.array([x.mean() for x in b]), "s2": np.array([x.std(ddof=1) for x in b]), "n2": np.full(k, n)}


def _effects(data: dict, plan: Plan):
    if "k1" in data:
        y, v = risk_difference(data["k1"], data["n1"], data["k2"], data["n2"])
    else:
        y, v = hedges_g(data["m1"], data["s1"], data["n1"], data["m2"], data["s2"], data["n2"])
    keep = (np.asarray(data["n1"]) + np.asarray(data["n2"])) >= plan.min_n
    return y[keep], v[keep]


def analyse(data: dict, plan: Plan) -> dict:
    """The confirmatory analysis exactly as planned: per-lab effects, the exclusion rule, random-effects pooling,
    and a one-sided test in the predicted direction."""
    y, v = _effects(data, plan)
    r = pool(y, v, "DL")
    z = plan.sign * r["est"] / r["se"]
    r.update({"y": y, "v": v, "z": float(z), "p_one": float(stats.norm.sf(z))})
    return r


def verdict(result: dict, plan: Plan, d33_value: float) -> dict:
    """The three registered criteria and the replication Bayes factor."""
    sig = result["p_one"] < plan.alpha
    inside = result["lo"] <= plan.original <= result["hi"]
    upper = max(plan.sign * result["lo"], plan.sign * result["hi"])  # the interval's end in the predicted direction
    telescope = upper >= d33_value
    bf = replication_bf(plan.sign * plan.original, plan.original_se, plan.sign * result["est"], result["se"])
    return {"significant": bool(sig), "original_inside": bool(inside), "not_below_d33": bool(telescope),
            "bf_r0": bf, "n_met": int(sig) + int(inside) + int(telescope)}


def dry_run(plan: Plan, k: int, n: int, effects=(0.0,), reps: int = 200, seed: int = 0) -> dict:
    """The frozen analysis on simulated labs before any real data: for each true effect (in the sign of the
    plan), the share of runs that are significant in the predicted direction."""
    out = {}
    for d in effects:
        hits = 0
        for r in range(reps):
            sim = simulate_labs(k, n, plan.sign * d, seed=seed + 1000 * r)
            hits += analyse(sim, Plan(plan.target, plan.outcome, plan.sign, plan.original, plan.original_se,
                                      plan.sesoi, plan.alpha, 0))["p_one"] < plan.alpha
        out[float(d)] = hits / reps
    return out


def multiverse(data: dict, plan: Plan, subsets: dict | None = None) -> list:
    """The labelled exploratory analysis: every combination of estimator (fixed or random), exclusion rule (none,
    the planned one, at least 60 people) and subset (all labs, or each named subset) gives one estimate."""
    subsets = subsets or {"all labs": np.ones(len(np.asarray(data["n1"])), bool)}
    rows = []
    for name, mask in subsets.items():
        sub = {k: np.asarray(v)[mask] for k, v in data.items() if np.ndim(v) and len(np.asarray(v)) == len(mask)}
        for min_n in sorted({0, plan.min_n, 60}):
            p = Plan(plan.target, plan.outcome, plan.sign, plan.original, plan.original_se, plan.sesoi, plan.alpha,
                     min_n)
            y, v = _effects(sub, p)
            if len(y) < 2:
                continue
            for method in ("FE", "DL"):
                r = pool(y, v, method)
                rows.append({"subset": name, "min_n": min_n, "method": method, "est": r["est"], "lo": r["lo"],
                             "hi": r["hi"], "k": r["k"]})
    return rows
