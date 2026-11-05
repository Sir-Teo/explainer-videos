"""The capstone pipeline of Part 20 of *Statistics, Built* ("The Analysis"): one function per stage, run unchanged on
NHANES 2017-2018 (the Museum) and on surveys of the World, where the truth is known.

    d = nhanes_frame()                      # or world_frame(World(), seed)
    keep, log = clean(d)                    # the decision log of chapter three
    r = fit(d, keep, SPEC)                  # the pre-specified model of chapter five, with design-based SEs

Every frame is a dict of numpy arrays with NHANES's column names (see ``tools/nhanes_extract.py``).
"""

from __future__ import annotations

import numpy as np

from explainer.stats import museum
from explainer.stats.kit import capstone as C
from explainer.stats.kit import survey as SV

SPEC = {"meds": "exclude", "energy": True, "log_na": False, "age_spline": False, "exposure": "day1", "weights": True,
        "readings": "2+"}
KCAL_RANGE = (500, 5000)


def nhanes_frame() -> dict:
    return museum.nhanes()


def world_frame(W, seed: int, towns_per_region: int = 2, per_town: int = 250, old_boost: float = 2.0) -> dict:
    """A survey of the World shaped like NHANES: the 10 regions are strata; in each, ``towns_per_region`` towns (PSUs)
    drawn with replacement, with probability proportional to their adult population; in each drawn town ``per_town``
    adults by simple random sampling, adults 60+ ``old_boost`` times as likely to be chosen (NHANES oversamples the
    old too).  Weights are the inverse selection probabilities.  Columns follow NHANES's names and codes."""
    g = np.random.Generator(np.random.PCG64(np.random.SeedSequence([20, seed])))
    h, ad = W.health, W.adult
    town, region = W.town, W.towns["region"]
    adults = np.flatnonzero(ad & (W.age >= 18))
    t_of = town[adults]
    n_t = np.bincount(t_of, minlength=len(region)).astype(float)
    rows, wts, strata, psus = [], [], [], []
    for r in range(len(np.unique(region))):
        ts = np.flatnonzero(region == r)
        p = n_t[ts] / n_t[ts].sum()
        for j, t in enumerate(g.choice(ts, towns_per_region, replace=True, p=p)):
            pool = adults[t_of == t]
            old = W.age[pool] >= 60
            pr = np.where(old, old_boost, 1.0)
            pick = g.choice(len(pool), per_town, replace=False, p=pr / pr.sum())
            # inclusion probability within the town, by the usual approximation per_town * pr_i / sum(pr)
            pi_in = np.minimum(1.0, per_town * pr[pick] / pr.sum())
            pi_town = towns_per_region * p[ts == t][0]
            rows.append(pool[pick])
            wts.append(1.0 / (pi_town * pi_in))
            strata.append(np.full(per_town, r + 1))
            psus.append(np.full(per_town, j + 1))
    i = np.concatenate(rows)
    w = np.concatenate(wts)
    reads = h["sbp_read"][i]
    nan = np.full(len(i), np.nan)
    return {"seqn": i.astype(float), "sex": np.where(W.male[i], 1.0, 2.0), "age": np.minimum(W.age[i], 80).astype(float),
            "pregnant": nan.copy(), "wt_mec": w, "wt_diet1": w, "strata": np.concatenate(strata).astype(float),
            "psu": np.concatenate(psus).astype(float), "sbp1": reads[:, 0], "sbp2": reads[:, 1], "sbp3": reads[:, 2],
            "sbp4": nan.copy(), "bmi": h["bmi"][i], "na1": h["na_day1"][i], "kcal1": h["kcal_day1"][i],
            "diet1_ok": np.ones(len(i)), "na2": h["na_day2"][i], "kcal2": h["kcal_day2"][i], "diet2_ok": np.ones(len(i)),
            "told_high": np.where(h["told_high"][i], 1.0, 2.0), "bp_meds": np.where(h["bp_meds"][i], 1.0, 2.0),
            "na_true": h["na_current"][i]}


def sbp(d: dict, readings: str = "2+") -> np.ndarray:
    """Systolic pressure: the mean of readings 2-4 when there are at least two readings (the first is often high:
    the 'white-coat' effect), else the single reading; ``readings='all'`` averages every reading."""
    R = np.column_stack([d[f"sbp{k}"] for k in range(1, 5)])
    n = np.isfinite(R).sum(1)
    tot, cnt = np.nansum(R, 1), np.isfinite(R).sum(1)
    tot2, cnt2 = np.nansum(R[:, 1:], 1), np.isfinite(R[:, 1:]).sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        allm = tot / cnt
        later = tot2 / cnt2
    if readings == "all":
        return np.where(n > 0, allm, np.nan)
    return np.where(n >= 2, later, np.where(n == 1, allm, np.nan))


def clean(d: dict, meds: str = "exclude") -> tuple[np.ndarray, C.DecisionLog]:
    """The cleaning funnel, each step logged.  ``meds='exclude'`` (the pre-specified primary analysis) drops adults
    taking blood-pressure medicine, whose pressure no longer reflects their diet; ``'keep'`` keeps them."""
    n = len(d["age"])
    log = C.DecisionLog(n)
    k = np.ones(n, bool)
    k = log.apply(k, d["age"] >= 20, "adults 20+", "the estimand's population")
    k = log.apply(k, d["pregnant"] != 1, "not pregnant", "pregnancy changes blood pressure")
    with np.errstate(invalid="ignore"):
        s = sbp(d)
    k = log.apply(k, np.isfinite(s), "a blood-pressure reading", "the outcome")
    k = log.apply(k, d["diet1_ok"] == 1, "a reliable day-1 recall", "the exposure")
    k = log.apply(k, (d["kcal1"] >= KCAL_RANGE[0]) & (d["kcal1"] <= KCAL_RANGE[1]), "energy 500-5,000 kcal",
                  "implausible recalls")
    k = log.apply(k, np.isfinite(d["bmi"]), "BMI measured", "a confounder")
    if meds == "exclude":
        k = log.apply(k, d["bp_meds"] != 1, "not on BP medicine", "pre-specified: drugs mask diet")
    return k, log


def design(d: dict, keep: np.ndarray, spec: dict, xhat=None) -> tuple[np.ndarray, list]:
    """The design matrix of a specification: sodium (g/day, or log2 for 'per doubling'), age (linear, or a
    restricted cubic spline with knots at 25, 40, 55, 70), female, BMI, and optionally energy (1,000 kcal)."""
    m = keep
    if spec["exposure"] == "day1":
        na = d["na1"][m] / 1000
    elif spec["exposure"] == "mean2":
        na = (d["na1"][m] + d["na2"][m]) / 2000
    else:
        na = np.asarray(xhat, float)
    na = np.log2(np.maximum(na, 0.1)) if spec.get("log_na") else na
    cols, names = [np.ones(m.sum()), na], ["intercept", "sodium"]
    if spec["age_spline"]:
        B = C.rcs_basis(d["age"][m], [25, 40, 55, 70])
        cols += list(B.T)
        names += ["age"] + [f"age_s{j}" for j in range(1, B.shape[1])]
    else:
        cols.append(d["age"][m])
        names.append("age")
    cols += [(d["sex"][m] == 2).astype(float), d["bmi"][m]]
    names += ["female", "bmi"]
    if spec["energy"]:
        kc = (d["kcal1"][m] + d["kcal2"][m]) / 2 if spec["exposure"] == "mean2" else d["kcal1"][m]
        cols.append(kc / 1000)
        names.append("energy")
    return np.column_stack(cols), names


def fit(d: dict, spec: dict | None = None, keep=None, xhat=None) -> dict:
    """Clean (unless ``keep`` is given), build the design and fit by weighted least squares with design-based SEs."""
    spec = {**SPEC, **(spec or {})}
    if keep is None:
        keep, _ = clean(d, spec["meds"])
    if spec["exposure"] == "mean2":
        keep = keep & (d["diet2_ok"] == 1)
    X, names = design(d, keep, spec, xhat)
    y = sbp(d, spec["readings"])[keep]
    w = d["wt_diet1"][keep] if spec["weights"] else np.ones(keep.sum())
    r = SV.svy_ols(X, y, w, d["strata"][keep], d["psu"][keep])
    j = names.index("sodium")
    return {"names": names, "b": r["b"], "se": r["se_design"], "se_model": r["se_model"], "se_hc": r["se_hc"],
            "est": float(r["b"][j]), "est_se": float(r["se_design"][j]), "n": int(keep.sum()), "keep": keep,
            "resid": r["resid"], "X": X, "y": y, "w": w}


def calibrated(d: dict, spec: dict | None = None) -> dict:
    """Regression calibration: among those with two reliable recalls, predict day-2 sodium from day-1 sodium and the
    outcome model's own covariates, then use that prediction as the exposure (Carroll et al. 2006, ch. 4)."""
    spec = {**SPEC, **(spec or {})}
    keep, _ = clean(d, spec["meds"])
    keep = keep & (d["diet2_ok"] == 1)
    zc = [d["age"][keep], (d["sex"][keep] == 2).astype(float), d["bmi"][keep]]
    if spec["energy"]:
        zc.append(d["kcal1"][keep] / 1000)
    Z = np.column_stack(zc)  # exactly the outcome model's covariates
    rc = C.regression_calibration(d["na1"][keep] / 1000, d["na2"][keep] / 1000, Z, d["wt_diet1"][keep])
    r = fit(d, {**spec, "exposure": "calib"}, keep=keep, xhat=rc["xhat"])
    r["lam"] = rc["lam"]
    return r
