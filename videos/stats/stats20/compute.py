"""Precompute every number in Part 20 of *Statistics, Built* ("The Analysis", the BSc capstone).

    python -m videos.stats.stats20.compute            # everything missing (several minutes: the World replays)
    python -m videos.stats.stats20.compute --force board

Results are cached in ``.cache/stats20/<name>.json``.  The data are NHANES 2017-2018 (CDC/NCHS, public domain; the
Museum's ``nhanes()``, extracted by ``tools/nhanes_extract.py``); the replays use the World's health block, whose
sodium effect is known (``World.SODIUM_EFFECT`` = 1.5 mm Hg per g/day).  The analysis itself is ``pipeline.py``.

Items:
    hook        the analytic sample's sodium and pressure, a scatter subsample, the crude slope
    design      NHANES's strata, PSUs and weights: who is oversampled; weighted vs unweighted means; the design effect
    clean       the decision log: every exclusion and how many it removed; codes and implausible values
    explore     weighted distributions of pressure and sodium; pressure by age and sex; sodium vs energy; deciles
    model       the pre-specified model: coefficients, design-based SEs and t(15) intervals
    checks      residuals, a Q-Q plot, an age spline, a sodium x age interaction, influence
    uncert      four SEs for the sodium slope and the mean: model, sandwich, linearization, PSU bootstrap
    spec        the specification curve: 64 reasonable analyses
    meas        two recalls: reliability, regression calibration
    reverse     who was told their pressure is high, and what they eat
    world       the same pipeline on one World survey, and on 200 of them, against the truth
    trial       a randomized sodium trial run on the World
    report      the headline numbers for the one-page report
    repro       provenance: the data file's hash, top-coding, the seeds
    board       Coverage Board rows: 95% intervals for the World's sodium effect
"""

from __future__ import annotations

import hashlib
from dataclasses import asdict
from pathlib import Path

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import capstone as C
from explainer.stats.kit import survey as SV
from explainer.stats.world import World

from . import pipeline as P

CACHE = Cache("stats20")
load = CACHE.load
W = World()
R_WORLD = 200
RACE = {1: "Mexican American", 2: "other Hispanic", 3: "White", 4: "Black", 6: "Asian", 7: "other / multiracial"}


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


def frame():
    d = P.nhanes_frame()
    keep, log = P.clean(d)
    return d, keep, log


def wmean(y, w):
    return float(np.sum(w * y) / np.sum(w))


def df_design(d, keep) -> int:
    s, p = d["strata"][keep], d["psu"][keep]
    return len({(a, b) for a, b in zip(s, p)}) - len(np.unique(s))


def compute_hook():
    d, k, _ = frame()
    na, y = d["na1"][k] / 1000, P.sbp(d)[k]
    g = rng(20)
    sub = g.choice(k.sum(), 700, replace=False)
    b = np.polyfit(na, y, 1)
    return nest({"n": int(k.sum()), "na": na[sub], "sbp": y[sub], "slope": b[0], "intercept": b[1],
                 "mean_na": wmean(na, d["wt_diet1"][k]), "guideline": 2.3})


def compute_design():
    d = P.nhanes_frame()
    a = (d["age"] >= 20) & (d["pregnant"] != 1)
    w = d["wt_mec"][a]
    race = d["race"][a]
    shares = {RACE[c]: {"sample": float(np.mean(race == c)), "weighted": float(np.sum(w * (race == c)) / w.sum())}
              for c in RACE}
    old = d["age"][a] >= 60
    s = P.sbp(d)[a]
    ok = np.isfinite(s)
    sw = SV.svy_mean(s[ok], w[ok], d["strata"][a][ok], d["psu"][a][ok])
    na = d["na1"][a]
    okn = np.isfinite(na) & (d["diet1_ok"][a] == 1)
    wn = d["wt_diet1"][a][okn]
    nw = SV.svy_mean(na[okn], wn, d["strata"][a][okn], d["psu"][a][okn])
    srs_se = float(np.std(s[ok], ddof=1) / np.sqrt(ok.sum()))
    return nest({"n": int(a.sum()), "strata": int(len(np.unique(d["strata"]))), "psus": int(len({(x, y) for x, y in zip(d["strata"], d["psu"])})),
                 "pop": float(w.sum()), "w_min": float(w.min()), "w_max": float(w.max()), "w_median": float(np.median(w)),
                 "shares": shares, "old_sample": float(old.mean()), "old_weighted": float(np.sum(w * old) / w.sum()),
                 "sbp_unweighted": float(s[ok].mean()), "sbp_weighted": sw["mean"], "sbp_se": sw["se"], "sbp_srs_se": srs_se,
                 "deff": sw["deff"], "neff": float(ok.sum() / sw["deff"]), "na_unweighted": float(na[okn].mean()),
                 "na_weighted": nw["mean"], "kish": SV.kish_neff(w[ok])})


def compute_clean():
    d, k, log = frame()
    a = (d["age"] >= 20)
    R = np.column_stack([d[f"sbp{j}"] for j in range(1, 5)])
    D = np.column_stack([d[f"dbp{j}"] for j in range(1, 5)])
    nread = np.isfinite(R[a]).sum(1)
    first_vs_later = np.nanmean(R[a][nread >= 3][:, 0] - np.nanmean(R[a][nread >= 3][:, 1:3], 1))
    return nest({"log": log.table(), "dbp_zero": int(np.sum(D[a] == 0)), "n_read": {str(i): int(np.sum(nread == i)) for i in range(5)},
                 "first_minus_later": float(first_vs_later), "na_zero": int(np.sum(d["na1"][a] == 0)),
                 "kcal_low": int(np.sum(d["kcal1"][a] < 500)), "kcal_high": int(np.sum(d["kcal1"][a] > 5000)),
                 "na_max": float(np.nanmax(d["na1"][a])), "diet_codes": {str(c): int(np.sum(d["diet1_ok"][a] == c)) for c in (1, 2, 5)},
                 "age80": int(np.sum(d["age"] == 80)), "meds": int(np.sum(d["bp_meds"][a] == 1))})


def wquant(y, w, qs):
    o = np.argsort(y)
    cw = np.cumsum(w[o]) / w.sum()
    return [float(y[o][np.searchsorted(cw, q)]) for q in qs]


def compute_explore():
    d, k, _ = frame()
    w = d["wt_diet1"][k]
    y = P.sbp(d)[k]
    na = d["na1"][k] / 1000
    age, fem, kc = d["age"][k], d["sex"][k] == 2, d["kcal1"][k] / 1000
    e_s = np.arange(80, 202, 4)
    h_s = [float(np.sum(w[(y >= a) & (y < a + 4)]) / w.sum()) for a in e_s[:-1]]
    e_n = np.arange(0, 10.01, 0.25)
    h_n = [float(np.sum(w[(na >= a) & (na < a + 0.25)]) / w.sum()) for a in e_n[:-1]]
    bands = [(20, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 81)]
    by_age = {sx: [wmean(y[(age >= a) & (age < b) & (fem == (sx == "women"))], w[(age >= a) & (age < b) & (fem == (sx == "women"))])
                   for a, b in bands] for sx in ("men", "women")}
    na_age = {sx: [wmean(na[(age >= a) & (age < b) & (fem == (sx == "women"))], w[(age >= a) & (age < b) & (fem == (sx == "women"))])
                   for a, b in bands] for sx in ("men", "women")}
    cuts = wquant(na, w, np.linspace(0.1, 0.9, 9))
    dec = np.digitize(na, cuts)
    decs = [{"na": wmean(na[dec == j], w[dec == j]), "sbp": wmean(y[dec == j], w[dec == j]),
             "se": float(np.std(y[dec == j], ddof=1) / np.sqrt(np.sum(dec == j)))} for j in range(10)]
    g = rng(21)
    sub = g.choice(k.sum(), 700, replace=False)
    return nest({"edges_sbp": e_s, "hist_sbp": h_s, "edges_na": e_n, "hist_na": h_n, "bands": bands, "by_age": by_age,
                 "na_by_age": na_age, "deciles": decs, "kcal_sub": kc[sub], "na_sub": na[sub], "r_na_kcal": float(np.corrcoef(na, kc)[0, 1]),
                 "q_sbp": wquant(y, w, [0.1, 0.5, 0.9]), "q_na": wquant(na, w, [0.1, 0.5, 0.9]),
                 "share_over_2300": float(np.sum(w * (na > 2.3)) / w.sum()), "share_130": float(np.sum(w * (y >= 130)) / w.sum()),
                 "mean_sbp": wmean(y, w), "mean_na": wmean(na, w), "r_na_age": float(np.corrcoef(na, age)[0, 1])})


def compute_model():
    d, k, _ = frame()
    r = P.fit(d, keep=k)
    df = df_design(d, k)
    t = float(stats.t.ppf(0.975, df))
    lo, hi = r["b"] - t * r["se"], r["b"] + t * r["se"]
    return nest({"names": r["names"], "b": r["b"], "se": r["se"], "lo": lo, "hi": hi, "n": r["n"], "df": df, "t": t,
                 "est": r["est"], "est_se": r["est_se"], "p": float(2 * stats.t.sf(abs(r["est"] / r["est_se"]), df))})


def compute_checks():
    d, k, _ = frame()
    r = P.fit(d, keep=k)
    fitted = r["y"] - r["resid"]
    e = r["resid"]
    o = np.argsort(fitted)
    bins = np.array_split(o, 20)
    ww = r["w"]
    rvf = [{"fit": wmean(fitted[b], ww[b]), "res": wmean(e[b], ww[b]), "sd": float(np.sqrt(wmean((e[b] - wmean(e[b], ww[b])) ** 2, ww[b]))),
            "se": float(e[b].std() / np.sqrt(len(b)))} for b in bins]
    z = (e - e.mean()) / e.std()
    qs = np.linspace(0.005, 0.995, 80)
    qq = {"theory": stats.norm.ppf(qs), "sample": np.quantile(z, qs)}
    rs = P.fit(d, {"age_spline": True}, keep=k)
    ages = np.arange(20, 81)
    B = C.rcs_basis(ages, [25, 40, 55, 70])
    js = [rs["names"].index(n) for n in rs["names"] if n.startswith("age")]
    curve_s = B @ rs["b"][js]
    curve_l = ages * r["b"][r["names"].index("age")]
    curve_s, curve_l = curve_s - curve_s[0], curve_l - curve_l[0]
    # the spline's extra terms: design-based Wald test
    jj = [rs["names"].index(n) for n in rs["names"] if n.startswith("age_s")]
    X, y, w = rs["X"], rs["y"], rs["w"]
    full = SV.svy_ols(X, y, w, d["strata"][k], d["psu"][k])
    V = full["cov_design"][np.ix_(jj, jj)]
    bb = full["b"][jj]
    wald = float(bb @ np.linalg.solve(V, bb))
    # a sodium x age interaction (age centred at 50)
    Xi = np.column_stack([r["X"], r["X"][:, 1] * (d["age"][k] - 50)])
    ri = SV.svy_ols(Xi, r["y"], r["w"], d["strata"][k], d["psu"][k])
    # influence: Cook's-style leverage x residual, the top 1% dropped
    Xw = r["X"] * np.sqrt(r["w"])[:, None]
    H = np.einsum("ij,jk,ik->i", Xw, np.linalg.inv(Xw.T @ Xw), Xw)
    cook = (r["w"] * e ** 2) * H / (1 - H) ** 2
    top = np.argsort(-cook)[: max(1, int(0.01 * len(e)))]
    kk = k.copy()
    kk[np.flatnonzero(k)[top]] = False
    rd = P.fit(d, keep=kk)
    return nest({"rvf": rvf, "qq": qq, "skew": float(stats.skew(e)), "ages": ages, "curve_spline": curve_s, "curve_linear": curve_l,
                 "wald": wald, "wald_df": len(jj), "wald_p": float(stats.chi2.sf(wald, len(jj))),
                 "inter": float(ri["b"][-1]), "inter_se": float(ri["se_design"][-1]), "n_drop": len(top),
                 "est_drop": rd["est"], "est_drop_se": rd["est_se"], "est": r["est"], "cook_top": np.sort(cook)[::-1][:10]})


def compute_uncert():
    d, k, _ = frame()
    r = P.fit(d, keep=k)
    j = r["names"].index("sodium")
    Wb = SV.psu_bootstrap_weights(d["wt_diet1"][k], d["strata"][k], d["psu"][k], 1000, rng(1988))
    Xs, y = r["X"], r["y"]
    bs = []
    for wb in Wb:
        sw = np.sqrt(wb)
        bs.append(np.linalg.lstsq(Xs * sw[:, None], y * sw, rcond=None)[0][j])
    bs = np.asarray(bs)
    # the mean pressure
    s = SV.svy_mean(y, r["w"], d["strata"][k], d["psu"][k])
    mb = np.array([np.sum(wb * y) / wb.sum() for wb in Wb])
    df = df_design(d, k)
    return nest({"est": r["est"], "se_model": float(r["se_model"][j]), "se_hc": float(r["se_hc"][j]), "se_design": float(r["se"][j]),
                 "se_boot": float(bs.std(ddof=1)), "boot": bs, "mean": s["mean"], "mean_se": s["se"], "mean_se_boot": float(mb.std(ddof=1)),
                 "mean_se_srs": float(np.std(y, ddof=1) / np.sqrt(len(y))), "df": df, "t": float(stats.t.ppf(0.975, df)), "z": 1.96})


SPEC_AXES = [("meds", ["exclude", "keep"]), ("energy", [True, False]), ("weights", [True, False]),
             ("age_spline", [False, True]), ("readings", ["2+", "all"]), ("exposure", ["day1", "mean2"])]


def compute_spec():
    d = P.nhanes_frame()
    out = []
    import itertools
    for combo in itertools.product(*[v for _, v in SPEC_AXES]):
        spec = dict(zip([a for a, _ in SPEC_AXES], combo))
        keep, _ = P.clean(d, spec["meds"])
        r = P.fit(d, spec, keep=keep)
        out.append({"spec": spec, "est": r["est"], "se": r["est_se"], "n": r["n"]})
    est = np.array([o["est"] for o in out])
    return nest({"axes": [a for a, _ in SPEC_AXES], "runs": out, "min": est.min(), "max": est.max(), "median": float(np.median(est)),
                 "n_pos_sig": int(sum(o["est"] - 2 * o["se"] > 0 for o in out)), "n_neg_sig": int(sum(o["est"] + 2 * o["se"] < 0 for o in out))})


def compute_meas():
    d, k, _ = frame()
    k2 = k & (d["diet2_ok"] == 1)
    n1, n2 = d["na1"][k2] / 1000, d["na2"][k2] / 1000
    rel = C.reliability(n1, n2)
    c = P.calibrated(d)
    c0 = P.calibrated(d, {"energy": False})
    r0 = P.fit(d, {"energy": False})
    r = P.fit(d)
    g = rng(22)
    sub = g.choice(k2.sum(), 600, replace=False)
    return nest({"n2": int(k2.sum()), "reliability": rel, "day1": n1[sub], "day2": n2[sub], "lam": c["lam"], "calib": c["est"],
                 "calib_se": c["est_se"], "lam_noenergy": c0["lam"], "calib_noenergy": c0["est"], "calib_noenergy_se": c0["est_se"],
                 "naive": r["est"], "naive_se": r["est_se"], "naive_noenergy": r0["est"], "naive_noenergy_se": r0["est_se"],
                 "sd_day1": float(n1.std()), "sd_diff": float((n1 - n2).std() / np.sqrt(2))})


def compute_reverse():
    d = P.nhanes_frame()
    keep, _ = P.clean(d, "keep")
    w = d["wt_diet1"][keep]
    told = d["told_high"][keep] == 1
    meds = d["bp_meds"][keep] == 1
    na, kc = d["na1"][keep] / 1000, d["kcal1"][keep] / 1000
    y = P.sbp(d)[keep]
    dens = lambda m: float(np.sum(w[m] * na[m]) / np.sum(w[m] * kc[m]))  # noqa: E731
    return nest({"told_share": float(np.sum(w * told) / w.sum()), "meds_share": float(np.sum(w * meds) / w.sum()),
                 "na_told": wmean(na[told], w[told]), "na_not": wmean(na[~told], w[~told]),
                 "dens_told": dens(told), "dens_not": dens(~told), "sbp_meds": wmean(y[meds], w[meds]),
                 "sbp_told_nomeds": wmean(y[told & ~meds], w[told & ~meds]), "sbp_not": wmean(y[~told], w[~told]),
                 "age_told": wmean(d["age"][keep][told], w[told]), "age_not": wmean(d["age"][keep][~told], w[~told])})


def world_runs(seed: int) -> dict:
    f = P.world_frame(W, seed)
    r = P.fit(f)
    c = P.calibrated(f)
    rn = P.fit(f, {"energy": False})
    cn = P.calibrated(f, {"energy": False})
    k, _ = P.clean(f)
    # the oracle: the same model with each person's true current intake (as if measured perfectly)
    kk = k.copy()
    ro = P.fit(f, {"exposure": "calib"}, keep=kk, xhat=f["na_true"][kk] / 1000)
    dfree = df_design(f, k)
    return {"naive": (r["est"], r["est_se"]), "calib": (c["est"], c["est_se"]), "naive_ne": (rn["est"], rn["est_se"]),
            "calib_ne": (cn["est"], cn["est_se"]), "oracle": (ro["est"], ro["est_se"]), "lam": c["lam"], "df": dfree, "n": r["n"]}


def compute_world():
    one = world_runs(0)
    reps = [world_runs(s) for s in range(1, R_WORLD + 1)]
    beta = W.SODIUM_EFFECT
    summary = {}
    for key in ("naive", "calib", "naive_ne", "calib_ne", "oracle"):
        e = np.array([r[key][0] for r in reps])
        s = np.array([r[key][1] for r in reps])
        t = np.array([stats.t.ppf(0.975, r["df"]) for r in reps])
        summary[key] = {"mean": float(e.mean()), "sd": float(e.std(ddof=1)), "cover": float(np.mean(np.abs(e - beta) <= t * s)),
                        "mean_se": float(s.mean()), "est": e}
    return nest({"one": one, "summary": summary, "beta": beta, "reps": R_WORLD, "lam_mean": float(np.mean([r["lam"] for r in reps]))})


def compute_trial():
    """A parallel-group trial on the World: 400 adults aged 30-70 not on BP medicine, half assigned 1.15 g/day
    (50 mmol) and half 3.45 g/day (150 mmol) for a month, as in DASH-Sodium; pressure from three readings."""
    h = W.health
    pool = np.flatnonzero(W.adult & (W.age >= 30) & (W.age <= 70) & ~h["bp_meds"])
    beta = W.SODIUM_EFFECT
    lo_g, hi_g = 1.15, 3.45

    def one(seed, n=400):
        g = rng(seed)
        i = g.choice(pool, n, replace=False)
        arm = g.permutation(np.repeat([0, 1], n // 2))
        assigned = np.where(arm == 1, hi_g, lo_g)
        sbp = h["sbp"][i] - beta * (h["na_current"][i] / 1000 - assigned)
        reads = sbp[:, None] + 5.0 * g.standard_normal((n, 3))
        y = reads[:, 1:].mean(1)
        diff = y[arm == 1].mean() - y[arm == 0].mean()
        se = np.sqrt(y[arm == 1].var(ddof=1) / (n // 2) + y[arm == 0].var(ddof=1) / (n // 2))
        return diff / (hi_g - lo_g), se / (hi_g - lo_g), diff, se, y, arm

    b, s, diff, se, y, arm = one(2001)
    reps = [one(3000 + r)[:2] for r in range(2000)]
    e = np.array([x[0] for x in reps])
    ss = np.array([x[1] for x in reps])
    return nest({"est": b, "se": s, "diff": diff, "diff_se": se, "y_low": y[arm == 0][:120], "y_high": y[arm == 1][:120],
                 "mean_low": float(y[arm == 0].mean()), "mean_high": float(y[arm == 1].mean()), "lo_g": lo_g, "hi_g": hi_g,
                 "cover": float(np.mean(np.abs(e - beta) <= 1.96 * ss)), "reps": len(reps), "beta": beta, "sd_est": float(e.std())})


def compute_report():
    m = load("model")
    ex = load("explore")
    me = load("meas")
    return nest({"est": m["est"], "lo": m["lo"][1], "hi": m["hi"][1], "n": m["n"], "mean_na": ex["mean_na"],
                 "share_over": ex["share_over_2300"], "mean_sbp": ex["mean_sbp"], "reliability": me["reliability"]})


def compute_repro():
    p = Path(__file__).resolve().parents[3] / "explainer" / "stats" / "data" / "nhanes_bp.csv"
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    d = P.nhanes_frame()
    return nest({"sha256": h, "bytes": p.stat().st_size, "rows": len(d["age"]), "cols": len(d),
                 "age80": int(np.sum(d["age"] == 80)), "pir5": int(np.sum(d["pir"] == 5)),
                 "psus_masked": int(len({(a, b) for a, b in zip(d["strata"], d["psu"])}))})


def compute_board():
    wd = load("world")
    tr = load("trial")
    rows = [
        Row(20, r"one-day recall, design $t$ CI", r"the World's sodium effect, \ 5,000 surveyed", "coverage", 0.95,
            wd["summary"]["naive"]["cover"], wd["reps"]),
        Row(20, r"regression calibration, design $t$ CI", r"the World's sodium effect, \ 5,000 surveyed", "coverage", 0.95,
            wd["summary"]["calib"]["cover"], wd["reps"]),
        Row(20, r"randomized trial, $z$ CI", r"the World's sodium effect, \ 400 randomized", "coverage", 0.95,
            tr["cover"], tr["reps"]),
    ]
    save_rows(20, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]}


ITEMS = {
    "hook": compute_hook, "design": compute_design, "clean": compute_clean, "explore": compute_explore,
    "model": compute_model, "checks": compute_checks, "uncert": compute_uncert, "spec": compute_spec, "meas": compute_meas,
    "reverse": compute_reverse, "world": compute_world, "trial": compute_trial, "report": compute_report,
    "repro": compute_repro, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
