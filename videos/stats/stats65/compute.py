"""Precompute every number in Part 65 of *Statistics, Built* ("The Dissertation").

    OMP_NUM_THREADS=1 python -m videos.stats.stats65.compute            # everything missing (several minutes)
    python -m videos.stats.stats65.compute --force board

Results are cached in ``.cache/stats65/<name>.json``.  The simulation study follows the protocol written down in the
part's README before it was run (the preregistration); the application uses the Museum's NHANES extract with a
selection mechanism designed in advance, so the true weights are known.

Items:
    bound      the theorem's lower bound for tempered Gaussian-tilt weights, against the temper lambda
    pilot      a small pilot run, used only to check the code and the Monte Carlo error (not the results)
    study      the preregistered study: 3 shifts x 3 heteroscedasticities x 5 methods, 1,000 replicates per cell
    nhanes     the application: blood pressure intervals for all adults from a sample that under-represents the old
    fullboard  every Coverage Board row of the degree, summarized
    board      Coverage Board rows
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import asdict

import numpy as np

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, load_all, save_rows
from explainer.stats.kit import thesis as T
from explainer.stats.kit.conformal import weighted_quantile_conformal

CACHE = Cache("stats65")
load = CACHE.load

MUS = [0.5, 1.0, 1.5]
GAMMAS = [0.0, 0.5, 1.0]
METHODS = ["none", "oracle", "estimated", "tempered", "misspecified"]
ALPHA = 0.1


def rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def nest(obj):
    if isinstance(obj, dict):
        return {k: nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return nest(obj.tolist())
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, float) and not math.isfinite(obj):
        return None
    return obj


def compute_bound():
    lam = np.linspace(0, 1.2, 121)
    return {"lam": lam, "alpha": ALPHA, "curves": {str(mu): [T.coverage_bound(ALPHA, mu, l) for l in lam] for mu in MUS}}


def compute_pilot():
    r = rng(6501)
    res = T.study([1.0], [0.5], METHODS, 50, 500, 500, ALPHA, r)
    return {"rows": res, "reps": 50}


def compute_study():
    r = rng(6502)
    res = T.study(MUS, GAMMAS, METHODS, 1000, 500, 500, ALPHA, r)
    return {"rows": res, "reps": 1000, "n_cal": 500, "n_tgt": 500, "n_test": 200, "alpha": ALPHA}


def _fit(X, y):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    return b


def _design(age, bmi):
    a, m = (age - 50) / 15, (bmi - 28) / 6
    return np.column_stack([np.ones(len(a)), a, a * a, m, a * m])


def compute_nhanes():
    d = museum.nhanes()
    sbp = np.nanmean(np.column_stack([d["sbp1"], d["sbp2"], d["sbp3"]]), axis=1)
    ok = np.isfinite(sbp) & np.isfinite(d["bmi"]) & np.isfinite(d["age"])
    age, bmi, y = d["age"][ok].astype(float), d["bmi"][ok].astype(float), sbp[ok]
    N = len(y)
    pi = T.selection_probs(age)
    r = rng(6503)
    out = {m: [] for m in ("none", "oracle", "estimated")}
    widths = {m: [] for m in out}
    sizes = []
    ess, wmax, corr_w, ncal = {"oracle": [], "estimated": []}, {"oracle": [], "estimated": []}, [], []
    by_age = {m: {"lo": [], "hi": []} for m in out}
    for _ in range(200):
        sel = r.random(N) < pi
        idx = np.flatnonzero(sel)
        r.shuffle(idx)
        tr, ca = idx[: len(idx) // 2], idx[len(idx) // 2:]
        test = np.flatnonzero(~sel)  # the target: everyone the study missed
        b = _fit(_design(age[tr], bmi[tr]), y[tr])
        pred = _design(age, bmi) @ b
        s = np.abs(y[ca] - pred[ca])
        # estimated weights: a logistic classifier of 'in the source sample' on age and BMI, fitted on everyone (the
        # covariates of the target population are observed, its outcomes not); w = (1 - p) / p, the odds of being missed
        F = np.column_stack([np.ones(N), (age - 50) / 15, ((age - 50) / 15) ** 2, (bmi - 28) / 6])
        lab = sel.astype(float)
        beta = np.zeros(F.shape[1])
        for _ in range(40):
            p = 1 / (1 + np.exp(-F @ beta))
            H = (F * (p * (1 - p))[:, None]).T @ F + 1e-6 * np.eye(F.shape[1])
            beta += np.linalg.solve(H, F.T @ (lab - p))
        ph = 1 / (1 + np.exp(-F @ beta))
        wts = {"none": None, "oracle": (1 - pi) / pi, "estimated": (1 - ph) / ph}
        sizes.append(len(idx))
        for m in ("oracle", "estimated"):
            wc = wts[m][ca]
            ess[m].append(float(wc.sum() ** 2 / np.sum(wc ** 2)))
            wmax[m].append(float(wc.max() / wc.sum()))
        corr_w.append(float(np.corrcoef(np.log(wts["oracle"]), np.log(wts["estimated"]))[0, 1]))
        ncal.append(len(ca))
        old = age[test] >= 65
        for m, w in wts.items():
            if w is None:
                n = len(s)
                q = np.sort(s)[math.ceil((n + 1) * (1 - ALPHA)) - 1]
                h = np.full(len(test), q)
            else:
                h = np.array([weighted_quantile_conformal(s, w[ca], float(v), ALPHA) for v in w[test]])
            cov = np.abs(y[test] - pred[test]) <= h
            out[m].append(float(cov.mean()))
            widths[m].append(float(np.median(2 * h[np.isfinite(h)])))
            by_age[m]["hi"].append(float(cov[old].mean()))
            by_age[m]["lo"].append(float(cov[~old].mean()))
    return {"N": N, "reps": 200, "mean_selected": float(np.mean(sizes)), "frac_old_pop": float(np.mean(age >= 65)),
            "frac_old_sel": float(np.sum(pi * (age >= 65)) / np.sum(pi)),
            "coverage": {m: float(np.mean(v)) for m, v in out.items()}, "mcse": {m: float(np.std(v, ddof=1) / math.sqrt(len(v))) for m, v in out.items()},
            "width": {m: float(np.mean(v)) for m, v in widths.items()},
            "old": {m: float(np.mean(v["hi"])) for m, v in by_age.items()}, "young": {m: float(np.mean(v["lo"])) for m, v in by_age.items()},
            "ess": {m: float(np.mean(v)) for m, v in ess.items()}, "wmax": {m: float(np.mean(v)) for m, v in wmax.items()},
            "corr_logw": float(np.mean(corr_w)), "n_cal": float(np.mean(ncal))}


def compute_fullboard():
    rows = load_all(upto=65)
    stage = lambda p: 1 if p <= 10 else 2 if p <= 20 else 3 if p <= 42 else 4 if p <= 55 else 5  # noqa: E731
    out = {"n": len(rows), "parts": len({r.part for r in rows}), "verdict": Counter(r.verdict for r in rows),
           "kind": Counter(r.kind for r in rows),
           "by_stage": {s: Counter(r.verdict for r in rows if stage(r.part) == s) for s in range(1, 6)},
           "rows": [{"part": r.part, "method": r.method, "kind": r.kind, "nominal": r.nominal, "achieved": r.achieved,
                     "verdict": r.verdict} for r in rows]}
    return {k: (dict(v) if isinstance(v, Counter) else ({s: dict(c) for s, c in v.items()} if k == "by_stage" else v)) for k, v in out.items()}


def compute_board():
    st = {(x["mu"], x["gamma"], x["method"]): x for x in load("study")["rows"]}
    nh = load("nhanes")
    a, b = st[(1.0, 1.0, "none")], st[(1.0, 1.0, "estimated")]
    rows = [Row(65, r"split conformal, \ no weights, \ under shift", r"$\mu = 1$, \ $\gamma = 1$, \ $n = 500$", "coverage", 0.9, a["coverage"], 1000),
            Row(65, r"weighted conformal, \ estimated weights", r"$\mu = 1$, \ $\gamma = 1$, \ $n = 500$", "coverage", 0.9, b["coverage"], 1000),
            Row(65, r"NHANES blood pressure, \ no weights", r"a sample short of the old", "coverage", 0.9, nh["coverage"]["none"], nh["reps"]),
            Row(65, r"NHANES blood pressure, \ estimated weights", r"a sample short of the old", "coverage", 0.9, nh["coverage"]["estimated"], nh["reps"])]
    save_rows(65, rows)
    return {"rows": [asdict(x) | {"verdict": x.verdict, "se": x.se} for x in rows]}


ITEMS = {"bound": compute_bound, "pilot": compute_pilot, "study": compute_study, "nhanes": compute_nhanes,
         "fullboard": compute_fullboard, "board": compute_board}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
