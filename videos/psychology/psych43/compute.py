"""Precompute every number in Part 43 of *Psychology, Built* ("The Replication").

    python -m videos.psychology.psych43.compute            # everything missing (a minute)
    python -m videos.psychology.psych43.compute --force confirm

Results are cached in ``.cache/psych43/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The pipeline is
``explainer.psychology.capstone``.  The order of the items is the order of the study: the plans are frozen first
(``plans``), the analysis is run on simulated labs (``dryrun``), and only then are the real lab-level data read
(``confirm``, ``verdict``, ``multiverse``).  The scenes' narration about the results is templated over these items,
so it says what the data say.

Items:
    plans       the two preregistrations: verbal overshadowing (RRR 2, description after a 20-minute filler, as in
                the original's Study 1; risk difference in correct line-up identifications) and ego depletion (the
                multi-lab protocol; Hedges's g on reaction-time variability); each original's estimate and SE, d33,
                the smallest effect of interest, and the sample size for 95% power at it
    dryrun      the frozen analysis on simulated labs (the planned number and size of labs): the share significant
                with no effect, at the smallest effect of interest and at the original effect, 200 runs each
    confirm     the confirmatory analyses on the open lab-level data: per-lab effects, the random-effects estimate
                and interval, tau^2, I^2, the one-sided p
    verdict     the three registered criteria and the replication Bayes factor for each target
    multiverse  the labelled exploratory analyses: estimator x exclusion rule x subset (English-speaking labs, for
                ego depletion; study 1 of the overshadowing report, for verbal overshadowing)
    powercurve  power against the true effect: the original study, one study of 2,600 per group, the pooled labs
    labs        each lab's size in the two replications
    garden      300 simulated replications with no effect: how often at least one of 14 analyses is significant,
                against the single planned analysis
    abtest      a product experiment planned the same way: people per arm for a 0.5-point lift on 5% conversion
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import capstone as C
from explainer.psychology import opendata

CACHE = Cache("psych43")
load = CACHE.load


def _vo(study: int) -> dict:
    d = opendata.overshadowing_rrr(study)
    v, c = d["verbal"], d["control"]
    return {"k1": v[:, 0], "n1": v[:, 1], "k2": c[:, 0], "n2": c[:, 1]}, d


def _ed() -> tuple:
    e = opendata.ego_depletion_rrr()
    rep = ~e["original"]
    data = {k: e[kk][rep] for k, kk in (("m1", "m_dep"), ("s1", "sd_dep"), ("n1", "n_dep"), ("m2", "m_ctl"),
                                         ("s2", "sd_ctl"), ("n2", "n_ctl"))}
    return data, e


def _plans() -> dict:
    _, d = _vo(2)
    o = d["original"]
    rd, rv = C.risk_difference(o[0, 0], o[0, 1], o[1, 0], o[1, 1])
    vo = C.Plan("verbal overshadowing", "difference in correct identifications (describe minus control)", -1,
                float(rd), float(np.sqrt(rv)), 0.05)
    _, e = _ed()
    orig = e["original"]
    g, v = C.hedges_g(e["m_dep"][orig], e["sd_dep"][orig], e["n_dep"][orig], e["m_ctl"][orig], e["sd_ctl"][orig],
                      e["n_ctl"][orig])
    ed = C.Plan("ego depletion", "Hedges's g on reaction-time variability (depleted minus control)", 1,
                float(g[0]), float(np.sqrt(v[0])), 0.1)
    return {"vo": (vo, int(o[0, 1]), int(o[1, 1]), float(o[1, 0] / o[1, 1])),
            "ed": (ed, int(e["n_dep"][orig][0]), int(e["n_ctl"][orig][0]), None)}


def compute_plans() -> dict:
    p = _plans()
    vo, n1, n0, p0 = p["vo"]
    ed, m1, m0, _ = p["ed"]
    return {"vo_orig": vo.original, "vo_se": vo.original_se, "vo_n1": n1, "vo_n0": n0, "vo_p0": p0,
            "vo_d33": C.d33_rd(p0, n1, n0), "vo_sesoi": vo.sesoi,
            "ed_orig": ed.original, "ed_se": ed.original_se, "ed_n1": m1, "ed_n0": m0, "ed_d33": C.d33(m1, m0),
            "ed_sesoi": ed.sesoi, "ed_n95": C.n_per_group(ed.sesoi, 0.95), "ed_power_orig": C.power2(0.2, m1, m0)}


def compute_dryrun() -> dict:
    p = _plans()
    ed = p["ed"][0]
    r = C.dry_run(ed, 23, 46, effects=(0.0, ed.sesoi, round(ed.original, 2)), reps=200, seed=43)
    keys = list(r)
    return {"effects": np.array(keys), "share": np.array([r[k] for k in keys]), "k": 23, "n": 46}


def compute_confirm() -> dict:
    p = _plans()
    out = {}
    for key, (data, plan) in (("vo", (_vo(2)[0], p["vo"][0])), ("ed", (_ed()[0], p["ed"][0]))):
        r = C.analyse(data, plan)
        out.update({f"{key}_{k}": v for k, v in r.items()})
        out[f"{key}_N"] = int(np.sum(data["n1"]) + np.sum(data["n2"]))
    return out


def compute_verdict() -> dict:
    p = _plans()
    c = load("confirm")
    out = {}
    for key in ("vo", "ed"):
        plan = p[key][0]
        res = {k: c[f"{key}_{k}"] for k in ("est", "se", "lo", "hi", "p_one")}
        d33 = load("plans")[f"{key}_d33"]
        v = C.verdict(res, plan, d33)
        out.update({f"{key}_{k}": (float(x) if not isinstance(x, bool) else x) for k, x in v.items()})
    return out


def compute_multiverse() -> dict:
    p = _plans()
    data, e = _ed()
    rep = ~e["original"]
    ed = C.multiverse(data, p["ed"][0], {"all labs": np.ones(int(rep.sum()), bool),
                                         "English-speaking labs": e["language"][rep] == "English"})
    v2, _ = _vo(2)
    v1, _ = _vo(1)
    vo = C.multiverse(v2, p["vo"][0]) + [dict(r, subset="study 1 (no filler)")
                                         for r in C.multiverse(v1, p["vo"][0])]
    pack = lambda rows, pre: {f"{pre}_{k}": np.array([r[k] for r in rows]) for k in ("est", "lo", "hi", "k", "min_n")}  # noqa: E731
    out = {**pack(ed, "ed"), **pack(vo, "vo")}
    out["ed_label"] = np.array([f"{r['subset']}, {r['method']}, n >= {r['min_n']}" for r in ed])
    out["vo_label"] = np.array([f"{r['subset']}, {r['method']}, n >= {r['min_n']}" for r in vo])
    return out


def compute_powercurve() -> dict:
    """Power against the true effect for the original ego-depletion study (23 and 24 per group), one large study of
    2,600 per group, and the pooled multi-lab design (23 labs of about 23 per group, as one study)."""
    p = load("plans")
    d = np.linspace(0.0, 0.8, 81)
    c = load("confirm")
    n_pool = int(c["ed_N"] // 2)
    return {"d": d, "orig": np.array([C.power2(x, p["ed_n1"], p["ed_n0"]) for x in d]),
            "big": np.array([C.power2(x, 2600, 2600) for x in d]),
            "pooled": np.array([C.power2(x, n_pool, n_pool) for x in d]), "n_pool": n_pool}


def compute_labs() -> dict:
    """The size of each lab in the two replications, and the share of people in the largest and smallest labs."""
    v, _ = _vo(2)
    e, _ = _ed()
    nv = np.asarray(v["n1"]) + np.asarray(v["n2"])
    ne = np.asarray(e["n1"]) + np.asarray(e["n2"])
    return {"vo_n": np.sort(nv)[::-1], "ed_n": np.sort(ne)[::-1], "vo_total": int(nv.sum()), "ed_total": int(ne.sum())}


def compute_garden(reps: int = 300) -> dict:
    """The forking paths, simulated: 23 labs of 46 with no effect at all; a multiverse of 14 analyses (fixed or
    random effects; all labs, or either half of three different splits of the labs); the share of
    null datasets in which at least one analysis is significant in the predicted direction, against the frozen
    plan's single analysis."""
    p = _plans()
    ed = p["ed"][0]
    any_sig = one_sig = 0
    n_an = 0
    for r in range(reps):
        sim = C.simulate_labs(23, 23, 0.0, seed=4300 + r)
        k = len(sim["n1"])
        rng = np.random.default_rng(r)
        subsets = {"all": np.ones(k, bool)}
        for split in range(3):  # three ways a reader might argue the labs should be divided
            half = rng.permutation(k) < k // 2
            subsets[f"split {split}a"], subsets[f"split {split}b"] = half, ~half
        rows = C.multiverse(sim, ed, subsets)
        n_an = len(rows)
        any_sig += any(row["lo"] > 0 for row in rows)
        one_sig += C.analyse(sim, C.Plan(ed.target, ed.outcome, ed.sign, ed.original, ed.original_se, ed.sesoi,
                                         ed.alpha, 0))["p_one"] < ed.alpha
    return {"any": any_sig / reps, "one": one_sig / reps, "n_analyses": n_an, "reps": reps}


def compute_abtest() -> dict:
    """A product experiment planned like a replication: a 5% conversion rate, the smallest effect worth shipping
    0.5 percentage points, two-sided 5%, 80% power: people per arm; and how that grows if the effect is halved."""
    from scipy import stats
    z = stats.norm.ppf(0.975) + stats.norm.ppf(0.8)

    def n(p1, p2):
        return int(np.ceil(z ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / (p2 - p1) ** 2))

    return {"p0": 0.05, "mde": 0.005, "n": n(0.05, 0.055), "n_half": n(0.05, 0.0525), "n_double": n(0.05, 0.06)}


ITEMS = {"plans": compute_plans, "dryrun": compute_dryrun, "confirm": compute_confirm, "verdict": compute_verdict,
         "multiverse": compute_multiverse, "powercurve": compute_powercurve, "labs": compute_labs,
         "garden": compute_garden, "abtest": compute_abtest}

if __name__ == "__main__":
    CACHE.main(ITEMS)
