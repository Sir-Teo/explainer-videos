"""Precompute every number in Part 40 of *Statistics, Built* ("Time to Event").

    OMP_NUM_THREADS=1 python -m videos.stats.stats40.compute            # everything missing (about twenty minutes)
    python -m videos.stats.stats40.compute --force board

Results are cached in ``.cache/stats40/<name>.json``.  Gehan's 6-MP trial, Mayo's PBC trial, the Stanford heart
transplants, MGUS, the veterans' lung cancer trial and the kidney infections are the Museum's; the cohort is the
World's; the rest are seeded simulations.

Items:
    gehan       KM, Greenwood and log-log bands, medians, redistribute-to-the-right, Nelson-Aalen, log-rank, Cox, RMST
    life        Graunt's table; the World cohort's true hazards by age and its true survival curve
    censor      naive treatments of censoring vs KM on the cohort; delayed entry on the age scale
    counting    a counting process and its compensator; the martingale's mean and variance over many paths
    pbc         the Mayo model by Cox; the trial arm; Breslow's baseline; Schoenfeld tests
    veteran     the Karnofsky score's non-proportional hazard; a time-varying coefficient; AFT fits
    hr          Hernan's point: a constant individual HR drifts when frail people die first; RMST differences
    immortal    the Stanford heart transplants and the cohort's statins: ever-treated vs time-varying Cox
    competing   MGUS2's progression vs death: Aalen-Johansen vs 1 - KM; Fine-Gray; the cohort's true CIFs
    frailty     kidney infections by the gamma frailty Weibull; the cohort's marginal HR for men by period
    predict     PBC: Cox vs a random survival forest by concordance and Brier score; a conformal lower bound
    board       Coverage Board rows
"""

from __future__ import annotations

import math
import json
from dataclasses import asdict
from pathlib import Path

import numpy as np

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import survival as SV
from explainer.stats.world import World

CACHE = Cache("stats40")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def nest(obj):
    if isinstance(obj, np.ndarray):
        return nest(obj.tolist())
    if isinstance(obj, dict):
        return {str(k): nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, float) and not np.isfinite(obj):
        return None
    return obj


def mean_mc_se(per_rep):
    """Monte Carlo standard error across independently calibrated datasets."""
    return float(np.std(per_rep, ddof=1) / math.sqrt(len(per_rep)))


def delayed_entry_sample(C, g, population=200_000, observed=4000):
    """Separate age-40 population, independently scheduled entry, retained only while alive.

    Covariate triples preserve their empirical joint distribution. Frailty is drawn at
    age 40 and survivor selection changes its distribution among later entrants.
    """
    W = World()
    idx = g.integers(0, len(C['age']), population)
    male, sbp, bmi = (np.asarray(C[k])[idx] for k in ('male', 'sbp', 'bmi'))
    Z = g.gamma(1 / W.FRAILTY_VAR, W.FRAILTY_VAR, population)
    r1 = Z * np.exp(np.log(.006) - 20 * W.CVD_GOMPERTZ + W.CVD_SBP * (sbp - 140)
                    + W.CVD_MALE * male + W.CVD_BMI * (bmi - 27))
    r2 = np.exp(np.log(.006) - 20 * W.OTHER_GOMPERTZ + W.OTHER_MALE * male)
    T1 = np.log1p(W.CVD_GOMPERTZ * g.exponential(1, population) / r1) / W.CVD_GOMPERTZ
    T2 = np.log1p(W.OTHER_GOMPERTZ * g.exponential(1, population) / r2) / W.OTHER_GOMPERTZ
    lifetime = 40 + np.minimum(T1, T2)
    entry = g.uniform(40, 80, population)
    eligible = np.flatnonzero(lifetime > entry)
    sample = g.choice(eligible, observed, replace=False)
    censor = entry[sample] + np.minimum(g.exponential(1 / W.DROPOUT, observed), 15)
    exit = np.minimum(lifetime[sample], censor)
    return dict(lifetime=lifetime, entry=entry[sample], exit=exit,
                event=(lifetime[sample] <= censor).astype(int))


def km_dict(km):
    return {"t": km["t"], "n": km["n"], "d": km["d"], "surv": km["surv"], "se": km["se"], "plain_lo": km["plain"][0],
            "plain_hi": km["plain"][1], "ll_lo": km["loglog"][0], "ll_hi": km["loglog"][1]}


def paired_remission_bootstrap(reps=3999, pairs=None):
    """Resample the original 21 matched pairs, preserving each pair's two arms."""
    if pairs is None:
        pairs = json.loads(Path(__file__).with_name("gehan_pairs.json").read_text())["pairs"]
    times = {arm: np.array([p[arm]["time"] for p in pairs]) for arm in ("mp", "placebo")}
    events = {arm: np.array([p[arm]["event"] for p in pairs]) for arm in times}
    g = rng(4011)
    differences = []
    for _ in range(reps):
        draw = g.integers(0, len(pairs), len(pairs))
        means = {arm: SV.rmst(SV.kaplan_meier(times[arm][draw], events[arm][draw]), 35.)["rmst"]
                 for arm in times}
        differences.append(means["mp"] - means["placebo"])
    return np.asarray(differences)


def compute_gehan():
    g = museum.gehan()
    t, e, grp = g["time"], g["event"], g["group"]
    out = {"time": t, "event": e, "group": grp}
    for name, k in (("mp", grp == 1), ("pl", grp == 0)):
        km = SV.kaplan_meier(t[k], e[k])
        out[name] = km_dict(km) | {"median": SV.km_median(km), "median_ci": SV.km_quantile_ci(km), "rmst": SV.rmst(km, 35.0)}
        na = SV.nelson_aalen(t[k], e[k])
        out[name + "_na"] = {"t": na["t"], "H": na["H"], "var": na["var"]}
    rd = SV.redistribute_right(t[grp == 1], e[grp == 1])
    out["rd"] = {"t": rd["t"], "mass": rd["mass"], "history": rd["history"], "order": rd["order"]}
    lr = SV.logrank(t, e, grp)
    gw = SV.logrank(t, e, grp, weight="gehan")
    out["logrank"] = {"chi2": lr["chi2"], "p": lr["p"], "O_mp": lr["O"], "E_mp": lr["E"], "rows": lr["rows"],
                      "gehan_chi2": gw["chi2"], "gehan_p": gw["p"]}
    x = (grp == 0).astype(float)
    for ties in ("breslow", "efron"):
        f = SV.cox_fit(t, e, x, ties=ties)
        out["cox_" + ties] = {"beta": f["beta"][0], "se": f["se"][0], "hr": math.exp(f["beta"][0]),
                              "ci": [math.exp(f["beta"][0] - 1.96 * f["se"][0]), math.exp(f["beta"][0] + 1.96 * f["se"][0])],
                              "lr": f["lr"], "score": f["score"], "wald": f["wald"]}
    d_rmst = out["mp"]["rmst"]["rmst"] - out["pl"]["rmst"]["rmst"]
    draws = paired_remission_bootstrap()
    out["rmst_diff"] = {"diff": d_rmst, "se": float(draws.std(ddof=1)),
                        "ci": np.quantile(draws, [.025, .975]), "bootstrap_reps": len(draws),
                        "uncertainty_scope": "matched-pair percentile bootstrap; 35-week KM tail extension",
                        "bootstrap_differences": draws}
    # the naive analyses: drop the censored; treat censored as relapses
    mp = grp == 1
    out["naive"] = {"mean_all_as_events": float(t[mp].mean()), "mean_events_only": float(t[mp & (e == 1)].mean()),
                    "n_cens": int((mp & (e == 0)).sum())}
    return nest(out)


def cohort_truth(C, grid):
    """The cohort's true all-cause survival, from the latent times (no censoring): an exact finite-population curve."""
    tmin = np.minimum(C["t_cvd"], C["t_other"])
    return np.array([(tmin > u).mean() for u in grid])


def compute_life():
    W = World()
    C = W.cohort
    ages = np.arange(40, 96)
    # hazards for a typical man and woman (sbp 130, bmi 27, frailty 1), by attained age
    lp = lambda male, a: (np.log(0.006) + W.CVD_GOMPERTZ * (a - 60) + W.CVD_SBP * (130 - 140) + W.CVD_MALE * male)  # noqa: E731
    lo = lambda male, a: np.log(0.006) + W.OTHER_GOMPERTZ * (a - 60) + W.OTHER_MALE * male  # noqa: E731
    haz = {"men": np.exp(lp(1, ages)) + np.exp(lo(1, ages)), "women": np.exp(lp(0, ages)) + np.exp(lo(0, ages))}
    grid = np.linspace(0, 15, 61)
    S = cohort_truth(C, grid)
    # a 60-year-old man's survival from 60, exactly (frailty integrated): S(t) = E[exp(-Z A1(t))] exp(-A2(t))
    t = np.linspace(0, 40, 161)
    A1 = np.exp(lp(1, 60)) / W.CVD_GOMPERTZ * (np.exp(W.CVD_GOMPERTZ * t) - 1)
    A2 = np.exp(lo(1, 60)) / W.OTHER_GOMPERTZ * (np.exp(W.OTHER_GOMPERTZ * t) - 1)
    th = W.FRAILTY_VAR
    S60 = (1 + th * A1) ** (-1 / th) * np.exp(-A2)
    from scipy.optimize import brentq
    def survival60(u):
        a1 = np.exp(lp(1, 60)) * np.expm1(W.CVD_GOMPERTZ * u) / W.CVD_GOMPERTZ
        a2 = np.exp(lo(1, 60)) * np.expm1(W.OTHER_GOMPERTZ * u) / W.OTHER_GOMPERTZ
        return (1 + th * a1) ** (-1 / th) * np.exp(-a2)
    median60 = brentq(lambda u: survival60(u) - .5, 0, 100)
    return nest({"graunt_ages": museum.GRAUNT_AGES, "graunt_alive": museum.GRAUNT_ALIVE, "ages": ages, "haz": haz,
                 "grid": grid, "truth": S, "t60": t, "S60": S60, "median60": median60,
                 "n": len(C["time"]), "deaths": int((C["status"] > 0).sum()), "censored": int((C["status"] == 0).sum()),
                 "admin": int((C["time"] >= W.COHORT_YEARS - 1e-9).sum()), "lost": int(((C["status"] == 0) & (C["time"] < W.COHORT_YEARS - 1e-6)).sum())})


def compute_censor():
    W = World()
    C = W.cohort
    t, d = C["time"], (C["status"] > 0).astype(int)
    grid = np.linspace(0, 15, 61)
    truth = cohort_truth(C, grid)
    km = SV.kaplan_meier(t, d)
    s_km = SV.km_at(km, grid)
    # naive 1: censored treated as deaths at their censoring time
    s_dead = np.array([(t > u).mean() for u in grid])
    # naive 2: drop the censored (only those whose fate is known)
    k = d == 1
    s_drop = np.array([(t[k] > u).mean() for u in grid])
    # naive 3: censored treated as survivors to the end
    s_surv = np.array([((t > u) | (d == 0)).mean() for u in grid])
    at10 = lambda s: float(s[np.argmin(np.abs(grid - 10))])  # noqa: E731
    # The baseline World cohort resets frailty at recruitment, so it is unsuitable
    # for an age-40 left-truncation demonstration. Generate the latter separately.
    entry_data = delayed_entry_sample(C, rng(4001))
    kma = SV.kaplan_meier(entry_data['exit'], entry_data['event'], entry=entry_data['entry'])
    kmn = SV.kaplan_meier(entry_data['exit'], entry_data['event'])
    ag = np.arange(40, 95)
    s_age_true = np.array([(entry_data['lifetime'] > a).mean() for a in ag])
    return nest({"grid": grid, "truth": truth, "km": s_km, "km_lo": SV.step_at(grid, km["t"], km["loglog"][0]),
                 "km_hi": SV.step_at(grid, km["t"], km["loglog"][1]), "as_dead": s_dead, "drop": s_drop, "as_alive": s_surv,
                 "at10": {"truth": at10(truth), "km": at10(s_km), "as_dead": at10(s_dead), "drop": at10(s_drop), "as_alive": at10(s_surv)},
                 "ages": ag, "age_entry": SV.step_at(ag, kma["t"], kma["surv"]), "age_naive": SV.step_at(ag, kmn["t"], kmn["surv"]),
                 "age_truth": s_age_true, "age_med": {"entry": SV.km_median(kma), "naive": SV.km_median(kmn),
                                                      "truth": float(np.median(entry_data['lifetime']))},
                 "entry_sample": {k: v for k, v in entry_data.items() if k != 'lifetime'},
                 "entry_population": len(entry_data['lifetime']),
                 "entry_scope": "separate age-40 simulation, independent scheduled entry, retained if alive"})


def compute_counting():
    g = rng(4002)
    # one path: N(t) for a cohort of 50 exponential(1) lifetimes with uniform censoring; Lambda(t) = sum int_0^t Y(s) ds
    n = 50
    T, Cc = g.exponential(1.0, n), g.uniform(0, 2.5, n)
    t, e = np.minimum(T, Cc), (T <= Cc).astype(int)
    grid = np.linspace(0, 2.5, 251)
    N = np.array([((t <= u) & (e == 1)).sum() for u in grid])
    Y = np.array([(t >= u).sum() for u in grid])
    Lam = np.minimum(t[:, None], grid).sum(axis=0)  # exact integrated risk time, hazard one
    # many paths: M(1) = N(1) - Lambda(1) has mean 0 and variance E Lambda(1)
    Ms, Ls = [], []
    for _ in range(4000):
        T, Cc = g.exponential(1.0, n), g.uniform(0, 2.5, n)
        tt, ee = np.minimum(T, Cc), (T <= Cc)
        Ms.append(((tt <= 1) & ee).sum() - np.minimum(tt, 1).sum())
        Ls.append(np.minimum(tt, 1).sum())
    Ms = np.array(Ms)
    return nest({"grid": grid, "N": N, "Y": Y, "Lam": Lam, "M_mean": float(Ms.mean()), "M_var": float(Ms.var()),
                 "Lam_mean": float(np.mean(Ls)), "M_values": Ms, "M_outside_hist": int(np.sum((Ms < -20.5) | (Ms > 20.5))), "hist": np.histogram(Ms, np.arange(-20.5, 21.5, 1.0))[0], "n": n})


def pbc_design(rand_only=True):
    p = museum.pbc()
    keep = ~np.isnan(p["trt"]) if rand_only else np.ones(len(p["time"]), bool)
    for k in ("age", "edema", "bili", "albumin", "protime"):
        keep &= ~np.isnan(p[k])
    X = np.column_stack([p["age"][keep] / 10, p["edema"][keep], np.log(p["bili"][keep]), np.log(p["albumin"][keep]),
                         np.log(p["protime"][keep])])
    names = ["age (per decade)", "edema", "log bilirubin", "log albumin", "log prothrombin time"]
    t = p["time"][keep] / 365.25
    d = (p["status"][keep] == 2).astype(int)  # transplant counted as censoring, as Dickson et al. did
    return t, d, X, names, p["trt"][keep]


def compute_pbc():
    t, d, X, names, trt = pbc_design()
    f = SV.cox_fit(t, d, X)
    km_trt = {str(int(a)): km_dict(SV.kaplan_meier(t[trt == a], d[trt == a])) for a in (1, 2)}
    ft = SV.cox_fit(t, d, (trt == 1).astype(float))
    lr = SV.logrank(t, d, trt)
    zph = SV.schoenfeld(t, d, X, f)
    # a person at the median of each covariate vs one with high bilirubin
    xm = np.median(X, 0)
    xh = xm.copy()
    xh[2] = np.log(8.0)
    grid = np.linspace(0, 12, 121)
    S = SV.cox_survival(f, np.vstack([xm, xh]), grid)
    return nest({"names": names, "beta": f["beta"], "se": f["se"], "hr": np.exp(f["beta"]),
                 "lo": np.exp(f["beta"] - 1.96 * f["se"]), "hi": np.exp(f["beta"] + 1.96 * f["se"]), "n": len(t),
                 "events": int(d.sum()), "lr": f["lr"], "km_trt": km_trt, "trt_hr": math.exp(ft["beta"][0]),
                 "trt_ci": [math.exp(ft["beta"][0] - 1.96 * ft["se"][0]), math.exp(ft["beta"][0] + 1.96 * ft["se"][0])],
                 "trt_logrank_p": lr["p"], "zph_chi2": zph["chi2"], "zph_p": zph["p"], "grid": grid, "S_med": S[0], "S_high": S[1],
                 "bili_med": float(np.exp(xm[2]))})


def compute_veteran():
    v = museum.veteran()
    t, d = v["time"], v["status"].astype(int)
    karno = v["karno"]
    X = np.column_stack([karno / 10, (v["trt"] == 2).astype(float)])
    f = SV.cox_fit(t, d, X)
    zph = SV.schoenfeld(t, d, X, f)
    # binned smooth of the scaled residuals for karno against time
    o = np.argsort(zph["t"])
    tt, sc = zph["t"][o], zph["scaled"][o, 0]
    bins = np.quantile(tt, np.linspace(0, 1, 9))
    mids, means = [], []
    for a, b in zip(bins[:-1], bins[1:]):
        k = (tt >= a) & (tt <= b)
        mids.append(float(np.median(tt[k])))
        means.append(float(sc[k].mean()))
    # time-varying coefficient: split at 90 days
    cut = 90.0
    a = t > cut
    T2 = np.concatenate([np.minimum(t, cut), t[a]])
    E2 = np.concatenate([np.where(a, 0, d), d[a]])
    EN = np.concatenate([np.zeros(len(t)), np.full(a.sum(), cut)])
    k10 = np.concatenate([X[:, 0], X[a, 0]])
    late = np.concatenate([np.zeros(len(t)), np.ones(a.sum())])
    X2 = np.column_stack([k10 * (1 - late), k10 * late, np.concatenate([X[:, 1], X[a, 1]])])
    f2 = SV.cox_fit(T2, E2, X2, entry=EN)
    # KM by Karnofsky group
    hi = karno >= 60
    kms = {"hi": km_dict(SV.kaplan_meier(t[hi], d[hi])), "lo": km_dict(SV.kaplan_meier(t[~hi], d[~hi]))}
    # AFT fits on karno + trt
    afts = {dist: SV.aft_fit(t, d, X, dist) for dist in ("exponential", "weibull", "lognormal", "loglogistic")}
    aft = {k: {"coef": a["coef"], "sigma": a["sigma"], "loglik": a["loglik"], "aic": a["aic"], "se": a["se"]} for k, a in afts.items()}
    # median survival curves for karno 40 / 80 (trt standard) from each AFT vs KM groups
    grid = np.linspace(1, 600, 120)
    curves = {k: {str(kv): SV.aft_survival(afts[k], [kv / 10, 0.0], grid) for kv in (40, 80)} for k in afts}
    w = afts["weibull"]
    return nest({"beta": f["beta"], "se": f["se"], "hr_karno10": math.exp(f["beta"][0]), "zph_chi2": zph["chi2"], "zph_p": zph["p"],
                 "zt": tt, "zs": sc, "bin_t": mids, "bin_s": means, "early_hr": math.exp(f2["beta"][0]), "late_hr": math.exp(f2["beta"][1]),
                 "early_se": f2["se"][0], "late_se": f2["se"][1], "cut": cut, "km": kms, "aft": aft, "grid": grid, "curves": curves,
                 "weibull_hr_karno": math.exp(-w["coef"][1] / w["sigma"]), "n": len(t), "events": int(d.sum())})


def compute_hr():
    """Hernan (2010): a trial with a constant individual hazard ratio 0.5 and a gamma frailty (variance 1)."""
    g = rng(4003)
    n = 20_000
    a = np.repeat([0, 1], n // 2)
    Z = g.gamma(1.0, 1.0, n)
    T = g.exponential(1.0, n) / (Z * np.where(a == 1, 0.5, 1.0))
    periods = [(0, 0.5), (0.5, 1), (1, 2), (2, 4)]
    hrs = []
    for lo, hi in periods:
        def rate(arm):
            k = a == arm
            at = T[k] > lo
            ev = ((T[k] > lo) & (T[k] <= hi)).sum()
            exposure = np.sum(np.clip(T[k][at], lo, hi) - lo)
            return ev / exposure
        hrs.append(rate(1) / rate(0))
    # the share of frail (Z > 2) among survivors, by arm, over time
    ts = np.linspace(0, 4, 41)
    frail = {str(arm): [float(np.mean(Z[(a == arm) & (T > u)] > 2)) for u in ts] for arm in (0, 1)}
    # marginal survival curves (exact): S_a(t) = 1 / (1 + c_a t), c = 1 or 0.5
    s0, s1 = 1 / (1 + ts), 1 / (1 + 0.5 * ts)
    # RMST difference to tau = 4: int 1/(1+0.5t) - 1/(1+t) = 2 ln 3 - ln 5
    rmst = {"treated": 2 * math.log(3.0), "control": math.log(5.0)}
    return nest({"periods": periods, "hrs": hrs, "ts": ts, "frail": frail, "s0": s0, "s1": s1, "rmst": rmst,
                 "cox_n": len(a[::20]), "cox_hr": math.exp(SV.cox_fit(np.minimum(T, 4.0)[::20], (T <= 4.0).astype(int)[::20], a[::20].astype(float),
                                               ties="breslow")["beta"][0])})


def compute_immortal():
    h = museum.stanford_heart()
    ids = np.unique(h["id"])
    # one row per patient: total follow-up, death, ever transplanted, waiting time
    fu = np.array([h["stop"][h["id"] == i].max() for i in ids])
    dead = np.array([h["event"][h["id"] == i][-1] for i in ids]).astype(int)
    ever = np.array([h["transplant"][h["id"] == i].max() for i in ids])
    wait = np.array([h["start"][(h["id"] == i) & (h["transplant"] == 1)].min() if ever[k] else np.nan for k, i in enumerate(ids)])
    age = np.array([h["age"][h["id"] == i][0] for i in ids])
    fu = np.where(fu == 0, 0.5, fu)
    naive = SV.cox_fit(fu, dead, ever.astype(float))
    stop = np.where(h["stop"] == h["start"], h["stop"] + 0.5, h["stop"])
    tv = SV.cox_fit(stop, h["event"].astype(int), np.column_stack([h["transplant"]]), entry=h["start"])
    tva = SV.cox_fit(stop, h["event"].astype(int), np.column_stack([h["transplant"], h["age"]]), entry=h["start"])
    stan = {"n": len(ids), "deaths": int(dead.sum()), "transplanted": int(ever.sum()), "median_wait": float(np.nanmedian(wait)),
            "naive_hr": math.exp(naive["beta"][0]), "naive_ci": [math.exp(naive["beta"][0] - 1.96 * naive["se"][0]),
                                                                  math.exp(naive["beta"][0] + 1.96 * naive["se"][0])],
            "tv_hr": math.exp(tv["beta"][0]), "tv_ci": [math.exp(tv["beta"][0] - 1.96 * tv["se"][0]), math.exp(tv["beta"][0] + 1.96 * tv["se"][0])],
            "tva_hr": math.exp(tva["beta"][0]), "tva_ci": [math.exp(tva["beta"][0] - 1.96 * tva["se"][0]), math.exp(tva["beta"][0] + 1.96 * tva["se"][0])],
            "died_waiting": int(((ever == 0) & (dead == 1)).sum()), "fu": fu, "dead": dead, "ever": ever, "wait": wait,
            "km_ever": km_dict(SV.kaplan_meier(fu[ever == 1], dead[ever == 1])), "km_never": km_dict(SV.kaplan_meier(fu[ever == 0], dead[ever == 0]))}
    # the World cohort's statins (no effect at all)
    C = World().cohort
    t, d = C["time"], (C["status"] > 0).astype(int)
    st = C["statin"]
    ev = np.isfinite(st)
    nv = SV.cox_fit(t, d, ev.astype(float))
    sp = np.where(ev, st, t)
    T2 = np.concatenate([np.where(ev, sp, t), t[ev]])
    E2 = np.concatenate([np.where(ev, 0, d), d[ev]])
    EN = np.concatenate([np.zeros(len(t)), sp[ev]])
    X2 = np.concatenate([np.zeros(len(t)), np.ones(ev.sum())])
    adj = np.concatenate([C["sbp"], C["sbp"][ev]]) / 10
    agec = np.concatenate([C["age"], C["age"][ev]]) / 10
    T2 = np.where(T2 <= EN, EN + 1e-3, T2)
    tv = SV.cox_fit(T2, E2, np.column_stack([X2, adj, agec]), entry=EN)
    tv0 = SV.cox_fit(T2, E2, X2, entry=EN)
    stat = {"users": int(ev.sum()), "naive_hr": math.exp(nv["beta"][0]),
            "naive_ci": [math.exp(nv["beta"][0] - 1.96 * nv["se"][0]), math.exp(nv["beta"][0] + 1.96 * nv["se"][0])],
            "tv_hr": math.exp(tv0["beta"][0]), "tv_ci": [math.exp(tv0["beta"][0] - 1.96 * tv0["se"][0]), math.exp(tv0["beta"][0] + 1.96 * tv0["se"][0])],
            "tva_hr": math.exp(tv["beta"][0]), "tva_ci": [math.exp(tv["beta"][0] - 1.96 * tv["se"][0]), math.exp(tv["beta"][0] + 1.96 * tv["se"][0])],
            "median_start": float(np.median(st[ev]))}
    return nest({"stanford": stan, "statin": stat})


def compute_competing():
    m = museum.mgus2()
    prog = m["pstat"] == 1
    t = np.where(prog, m["ptime"], m["futime"]) / 12.0
    st = np.where(prog, 1, np.where(m["death"] == 1, 2, 0))
    aj = SV.aalen_johansen(t, st)
    at = lambda arr, u: float(SV.step_at([u], aj["t"], arr, 0.0)[0])  # noqa: E731
    male = (m["sex"] == "M").astype(float)
    age10 = m["age"] / 10
    X = np.column_stack([male, age10])
    fg = SV.fine_gray(t, st, X, cause=1)
    # Resample whole patients and refit the censoring distribution in each draw.
    # The toolkit's inverse conditional information omits that uncertainty.
    bootstrap_rng = rng(4010)
    fg_bootstrap = []
    for _ in range(399):
        draw = bootstrap_rng.integers(0, len(t), len(t))
        fg_bootstrap.append(SV.fine_gray(t[draw], st[draw], X[draw], cause=1)["beta"])
    fg_bootstrap = np.asarray(fg_bootstrap)
    fg_se = fg_bootstrap.std(axis=0, ddof=1)
    cs = SV.cox_fit(t, (st == 1).astype(int), X)
    cs2 = SV.cox_fit(t, (st == 2).astype(int), X)
    fg2 = SV.fine_gray(t, st, X, cause=2)
    # the World cohort: true cumulative incidence from the latent times
    C = World().cohort
    tc, sc = C["time"], C["status"]
    ajc = SV.aalen_johansen(tc, sc)
    grid = np.linspace(0, 15, 61)
    tmin = np.minimum(C["t_cvd"], C["t_other"])
    true1 = np.array([((tmin <= u) & (C["t_cvd"] <= C["t_other"])).mean() for u in grid])
    true2 = np.array([((tmin <= u) & (C["t_other"] < C["t_cvd"])).mean() for u in grid])
    return nest({"t": aj["t"], "cif1": aj["cif1"], "cif2": aj["cif2"], "naive1": aj["naive1"], "naive2": aj["naive2"],
                 "at20": {"cif1": at(aj["cif1"], 20), "naive1": at(aj["naive1"], 20), "cif2": at(aj["cif2"], 20)},
                 "at30": {"cif1": at(aj["cif1"], 30), "naive1": at(aj["naive1"], 30)},
                 "n": len(t), "n_prog": int(prog.sum()), "n_death": int((st == 2).sum()), "median_age": float(np.median(m["age"])),
                 "fg": {"beta": fg["beta"], "se": fg_se, "se_method": "399 patient-pairs bootstrap fits, censoring KM refitted",
                        "bootstrap_beta": fg_bootstrap, "conditional_information_se": fg["se"]},
                 "cs": {"beta": cs["beta"], "se": cs["se"]},
                 "cs2": {"beta": cs2["beta"], "se": cs2["se"]}, "fg2": {"beta": fg2["beta"], "se": fg2["se"]},
                 "world": {"grid": grid, "true1": true1, "true2": true2,
                           "aj1": SV.step_at(grid, ajc["t"], ajc["cif1"], 0.0), "naive1": SV.step_at(grid, ajc["t"], ajc["naive1"], 0.0),
                           "aj2": SV.step_at(grid, ajc["t"], ajc["cif2"], 0.0)}})


def compute_frailty():
    k = museum.kidney()
    t, d, cl = k["time"], k["status"].astype(int), k["id"]
    female = (k["sex"] == 2).astype(float)
    f = SV.gamma_frailty_weibull(t, d, cl, female[:, None])
    f0 = SV.aft_fit(t, d, female[:, None], "weibull")
    cx = SV.cox_fit(t, d, female)
    # cluster correlation: first and second times within patient
    first = np.array([t[cl == i][0] for i in np.unique(cl)])
    second = np.array([t[cl == i][1] for i in np.unique(cl)])
    from scipy import stats as st
    rho = float(st.spearmanr(first, second).correlation)
    # the World cohort: the marginal hazard ratio for men, cardiovascular death, by period (latent times, no censoring)
    C = World().cohort
    T1, T2 = C["t_cvd"], C["t_other"]
    male = C["male"]
    periods = [(0, 3), (3, 6), (6, 9), (9, 12), (12, 15)]
    hrs = []
    for lo, hi in periods:
        def rate(mask):
            tmin = np.minimum(T1[mask], T2[mask])
            at = tmin > lo
            ev = ((T1[mask] > lo) & (T1[mask] <= hi) & (T1[mask] <= T2[mask])).sum()
            expo = np.sum(np.clip(tmin[at], lo, hi) - lo)
            return ev / expo
        hrs.append(rate(male) / rate(~male))
    # population hazard with gamma frailty (Vaupel): h_pop(t) = h(t) / (1 + theta H(t))
    W = World()
    ages = np.arange(60, 101)
    a0 = np.exp(np.log(0.006) + W.CVD_GOMPERTZ * (ages - 60))
    H = 0.006 / W.CVD_GOMPERTZ * (np.exp(W.CVD_GOMPERTZ * (ages - 60)) - 1)
    hpop = a0 / (1 + W.FRAILTY_VAR * H)
    return nest({"theta": f["theta"], "se_log_theta": f["se_log_theta"], "k": f["k"], "beta_female": f["beta"][0],
                 "hr_female_frailty": math.exp(f["beta"][0]), "hr_female_weibull": math.exp(-f0["coef"][1] / f0["sigma"]),
                 "hr_female_cox": math.exp(cx["beta"][0]), "ll": f["loglik"], "ll0": f0["loglik"], "rho": rho,
                 "first": first, "second": second, "n": len(np.unique(cl)), "periods": periods, "hrs": hrs,
                 "true_hr": math.exp(W.CVD_MALE), "ages": ages, "h_ind": a0, "h_pop": hpop})


def brier_score(time, event, survival, horizon):
    """IPCW Brier with G(T-) for deaths and right-continuous G(t) for survivors.

    Uses a pooled censoring KM, appropriate under unconditional independent
    censoring and adequate censoring support at the evaluation horizon.
    """
    time, event, survival = np.asarray(time), np.asarray(event), np.asarray(survival)
    censor = SV.kaplan_meier(time, 1 - event)
    before = np.searchsorted(censor["t"], time, side="left") - 1
    g_before = np.r_[1., censor["surv"]][before + 1]
    g_horizon = float(SV.km_at(censor, [horizon])[0]) if len(censor["t"]) else 1.
    if g_horizon <= 0:
        raise ValueError("No censoring support at the Brier evaluation horizon")
    died, alive = (time <= horizon) & (event == 1), time > horizon
    return float(np.mean(died * survival**2 / np.maximum(g_before, 1e-12)
                         + alive * (1 - survival)**2 / g_horizon))


def compute_predict():
    t, d, X, names, _ = pbc_design(rand_only=False)
    n = len(t)
    g = rng(4004)
    test = np.zeros(n, bool)
    test[g.choice(n, n // 3, replace=False)] = True
    tr = ~test
    f = SV.cox_fit(t[tr], d[tr], X[tr])
    risk = X @ f["beta"]
    c_cox_tr = SV.concordance(t[tr], d[tr], risk[tr])
    c_cox = SV.concordance(t[test], d[test], risk[test])
    c_bili = SV.concordance(t[test], d[test], X[test, 2])
    forest = SV.survival_forest(t[tr], d[tr], X[tr], n_trees=150, min_leaf=10, max_depth=6, rng=rng(4005))
    grid = np.linspace(0, 12, 49)
    chf = SV.forest_chf(forest, X[test], grid)
    c_rsf = SV.concordance(t[test], d[test], chf[:, -1])
    # Brier at 5 years
    t5 = 5.0
    S_cox = SV.cox_survival(f, X[test], [t5])[:, 0]
    S_rsf = np.exp(-chf[:, np.argmin(np.abs(grid - t5))])
    km = SV.kaplan_meier(t[tr], d[tr])
    S_km = np.full(test.sum(), float(SV.km_at(km, [t5])[0]))
    b = {k: brier_score(t[test], d[test], s, t5) for k, s in (("km", S_km), ("cox", S_cox), ("rsf", S_rsf))}
    # Brier over time
    bt = {"cox": [], "rsf": [], "km": []}
    times = np.arange(1, 11)
    for u in times:
        j = np.argmin(np.abs(grid - u))
        bt["cox"].append(brier_score(t[test], d[test], SV.cox_survival(f, X[test], [u])[:, 0], u))
        bt["rsf"].append(brier_score(t[test], d[test], np.exp(-chf[:, j]), u))
        bt["km"].append(brier_score(t[test], d[test], np.full(test.sum(), float(SV.km_at(km, [u])[0])), u))
    return nest({"n": n, "n_test": int(test.sum()), "c_cox_train": c_cox_tr, "c_cox": c_cox, "c_bili": c_bili, "c_rsf": c_rsf,
                 "brier5": b, "times": times, "brier_t": bt, "beta": f["beta"], "names": names})


def compute_conformal():
    """A seeded example: lifetimes T ~ Weibull with a covariate, censoring C ~ Exp; the Cox-based 10% quantile as q(x),
    conformalized (Candes, Lei & Ren 2023) at c0 = 6."""
    g = rng(4006)

    def draw(n):
        x = g.uniform(0, 2, n)
        T = (g.exponential(1, n) * np.exp(-0.8 * x)) ** (1 / 1.5) * 5
        C = g.exponential(8.0, n)
        return x, T, C

    x, T, C = draw(1500)
    tr, cal = np.arange(500), np.arange(500, 1500)
    t, d = np.minimum(T, C), (T <= C).astype(int)
    f = SV.cox_fit(t[tr], d[tr], x[tr])
    grid = np.linspace(0.01, 20, 2000)

    def q10(xs):
        S = SV.cox_survival(f, xs[:, None], grid)
        crossed = np.any(S <= .9, axis=1)
        return np.where(crossed, grid[np.argmax(S <= .9, axis=1)], grid[-1])

    xt, Tt, Ct = draw(2000)
    q_cal, q_test = q10(x[cal]), q10(xt)
    lpb = SV.conformal_lpb(T[cal], C[cal], q_cal, q_test, c0=6.0, alpha=0.1)
    return nest({"cover_raw": float(np.mean(Tt >= q_test)), "cover_conf": float(np.mean(Tt >= lpb)),
                 "x": xt[:300], "T": Tt[:300], "q": q_test[:300], "lpb": lpb[:300], "censored_share": float(1 - d.mean())})


def board_greenwood(g, n, reps, t0):
    """KM 90% CIs at t0 for exponential(1) lifetimes with uniform(0, 4) censoring: plain vs log-log; and the naive
    proportion that drops the censored."""
    S0 = math.exp(-t0)
    plain, ll, naive = [], [], []
    from scipy import stats as st
    z = st.norm.ppf(0.95)
    for _ in range(reps):
        T, C = g.exponential(1, n), g.uniform(0, 4, n)
        t, e = np.minimum(T, C), (T <= C).astype(int)
        km = SV.kaplan_meier(t, e, level=0.90)
        k = np.searchsorted(km["t"], t0, side="right") - 1
        if k < 0:
            plain.append(1.0)
            ll.append(1.0)
        else:
            s = km["surv"][k]
            plain.append(float(km["plain"][0][k] <= S0 <= km["plain"][1][k]) if s > 0 else 0.0)
            lo, hi = km["loglog"][0][k], km["loglog"][1][k]
            ll.append(float(lo <= S0 <= hi) if (s > 0 and s < 1) else float(s == 1 and S0 > 0.9))
        known = (e == 1) | (t > t0)
        p = (t[known] > t0).mean()
        se = math.sqrt(p * (1 - p) / known.sum())
        naive.append(float(abs(p - S0) <= z * se))
    return np.array(plain), np.array(ll), np.array(naive)


def compute_board():
    g = rng(4009)
    reps = 4000
    plain, ll, naive = board_greenwood(g, 20, reps, t0=1.2)
    _, _, naive200 = board_greenwood(g, 200, 2000, t0=1.0)
    # Cox Wald CI, n = 60, log HR 0.7
    cw = []
    from scipy import stats as st
    z = st.norm.ppf(0.95)
    for _ in range(1500):
        x = g.standard_normal(60)
        T = g.exponential(1 / np.exp(0.7 * x))
        C = g.exponential(2.0, 60)
        f = SV.cox_fit(np.minimum(T, C), (T <= C).astype(int), x)
        cw.append(abs(f["beta"][0] - 0.7) <= z * f["se"][0])
    # immortal time: a null treatment started at a random time while alive; ever-treated vs time-varying
    imm_n, imm_tv = [], []
    for _ in range(400):
        n = 400
        T = g.exponential(1.0, n)
        C = np.full(n, 3.0)
        S = g.exponential(1.5, n)
        t, d = np.minimum(T, C), (T <= C).astype(int)
        ev = S < t
        fn = SV.cox_fit(t, d, ev.astype(float), ties="breslow")
        imm_n.append(abs(fn["beta"][0]) <= z * fn["se"][0])
        T2 = np.concatenate([np.where(ev, S, t), t[ev]])
        E2 = np.concatenate([np.where(ev, 0, d), d[ev]])
        EN = np.concatenate([np.zeros(n), S[ev]])
        X2 = np.concatenate([np.zeros(n), np.ones(ev.sum())])
        ft = SV.cox_fit(T2, E2, X2, entry=EN, ties="breslow")
        imm_tv.append(abs(ft["beta"][0]) <= z * ft["se"][0])
    # conformal lower bounds (seeded, 200 replications of the calibration)
    conf = []
    for _ in range(200):
        nn = 400
        x = g.uniform(0, 2, 2 * nn)
        T = (g.exponential(1, 2 * nn) * np.exp(-0.8 * x)) ** (1 / 1.5) * 5
        C = g.exponential(8.0, 2 * nn)
        q = 5 * (-np.log(0.9) * np.exp(-0.8 * x)) ** (1 / 1.5) * 1.6  # a deliberately wrong (too high) quantile
        lpb = SV.conformal_lpb(T[:nn], C[:nn], q[:nn], q[nn:], c0=6.0, alpha=0.1)
        conf.append(np.mean(T[nn:] >= lpb))
    rows = [
        Row(40, r"S($t$) from the known fates only \ (censored dropped)", r"exponential lifetimes, \ uniform censoring, \ $n = 200$", "coverage",
            0.9, float(np.mean(naive200)), len(naive200)),
        Row(40, r"KM 90\% CI, \ plain Greenwood", r"exponential lifetimes, \ $n = 20$, \ $S(t) = 0.30$", "coverage", 0.9,
            float(np.mean(plain)), reps),
        Row(40, r"KM 90\% CI, \ log-log", r"exponential lifetimes, \ $n = 20$, \ $S(t) = 0.30$", "coverage", 0.9,
            float(np.mean(ll)), reps),
        Row(40, r"Cox Wald 90\% CI for $\beta$", r"exponential, \ $n = 60$, \ about 33\% censored", "coverage", 0.9,
            float(np.mean(cw)), len(cw)),
        Row(40, r"Cox CI, \ ever-treated \ (immortal time)", r"a null treatment started during follow-up, \ $n = 400$", "coverage", 0.9,
            float(np.mean(imm_n)), len(imm_n)),
        Row(40, r"Cox CI, \ treatment as time-varying", r"a null treatment started during follow-up, \ $n = 400$", "coverage", 0.9,
            float(np.mean(imm_tv)), len(imm_tv)),
        Row(40, r"conformal lower bound for $T$ \ (90\%)", r"Weibull lifetimes, \ exponential censoring, \ a wrong $q(x)$", "coverage", 0.9,
            float(np.mean(conf)), len(conf), mc_se=mean_mc_se(conf)),
    ]
    save_rows(40, rows)
    return nest({"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows], "conformal_replicates": conf})


ITEMS = {
    "gehan": compute_gehan, "life": compute_life, "censor": compute_censor, "counting": compute_counting, "pbc": compute_pbc,
    "veteran": compute_veteran, "hr": compute_hr, "immortal": compute_immortal, "competing": compute_competing,
    "frailty": compute_frailty, "predict": compute_predict, "conformal": compute_conformal, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
