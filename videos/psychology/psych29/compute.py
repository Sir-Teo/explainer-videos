"""Precompute every number in Part 29 of *Psychology, Built* ("Emotion").

    python -m videos.psychology.psych29.compute            # everything missing (under a minute)
    python -m videos.psychology.psych29.compute --force faces

Results are cached in ``.cache/psych29/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.emotion``; the meta-analysis uses ``drive.random_effects`` and ``drive.pet``); the
data are Abelson and Sermat's facial expressions (smacof) and Coles, Larsen and Lench's facial-feedback table
(psymetadata), fetched and checked by ``explainer.psychology.opendata``.  Published numbers are quoted in the scenes
with their sources.  Simulations use fixed seeds.

Items:
    attribution  arousal attributed to the situation against the size of an explanation already given; the four
                 conditions of Schachter and Singer as Psyche reads them
    faces        classical MDS of the 13 faces, the share of variance in two dimensions, and the fit of the three
                 rated scales
    pairs        a simulated observer's same-or-different judgments of ten schematic faces, one, three and ten times
                 each, and the maps MDS recovers
    feedback     the facial-feedback meta-analysis: study-level estimates, the random-effects pool, groups by
                 manipulation and by publication, and the precision-effect test
    appraisal    six scenarios coded on six appraisal dimensions, and the labels the model gives
    fear         the two-roads circuit for a snake, a stick, and a snake without an amygdala
    forecast     an event's impact fading fast, and the forecast that it fades slowly
    income       a simulated population: mean happiness, the 10th percentile and the share who felt bad, by income
    lorenz       Lorenz's attractor, the curve the positivity ratio borrowed
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import opendata
from explainer.psychology.psyche import drive as Dr
from explainer.psychology.psyche import emotion as E

CACHE = Cache("psych29")
load = CACHE.load


def compute_attribution() -> dict:
    ex = np.linspace(0, 1.5, 61)
    curve = np.array([E.attribution(1.2, e)["mean"] for e in ex])
    cond = {"informed": E.attribution(1.2, 1.0)["mean"], "ignorant": E.attribution(1.2, 0.0)["mean"],
            "misinformed": E.attribution(1.2, 0.0)["mean"], "placebo": E.attribution(0.3, 0.0)["mean"]}
    return {"explanation": ex, "curve": curve, **{f"c_{k}": v for k, v in cond.items()}}


def compute_faces() -> dict:
    f = opendata.faces_1962()
    m = E.classical_mds(f["D"])
    X = m["X"]
    fits = {k: E.fit_scale(X, f[k]) for k in ("PU", "AR", "TS")}
    # orient: pleasantness to the right, tension up
    if fits["PU"]["direction"][0] < 0:
        X[:, 0] *= -1
    if fits["TS"]["direction"][1] < 0:
        X[:, 1] *= -1
    fits = {k: E.fit_scale(X, f[k]) for k in ("PU", "AR", "TS")}
    out = {"X": X, "labels": f["labels"], "eig": m["eig"], "share": m["share"],
           "share1": float(m["eig"][0] / m["eig"][m["eig"] > 0].sum())}
    for k, r in fits.items():
        out[f"{k}_R"] = r["R"]
        out[f"{k}_dir"] = r["direction"]
        out[k] = f[k]
    return out


def compute_pairs() -> dict:
    out = {}
    for r in (1, 3, 10):
        p = E.pairs_map(n_reps=r, seed=29)
        out[f"X{r}"] = p["X"]
        out[f"r{r}"] = p["r"]
    out["true"] = p["true"]
    out["names"] = p["names"]
    return out


def compute_feedback() -> dict:
    c = opendata.coles_2019()
    y, v, sid = c["yi"], c["vi"], c["study_id"]
    ids = sorted(set(sid.tolist()))
    ys, vs = [], []
    for i in ids:
        m = sid == i
        w = 1 / v[m]
        ys.append(float((w * y[m]).sum() / w.sum()))
        vs.append(float(1 / w.sum()))
    ys, vs = np.array(ys), np.array(vs)
    re = Dr.random_effects(ys, vs)
    pe = Dr.pet(ys, np.sqrt(vs))
    order = np.argsort(ys)
    proc = [p or "" for p in c["proc"]]
    groups = {}
    for key, name in (("exp.pose", "posing an expression"), ("suppress", "suppressing one"),
                      ("exaggerate", "exaggerating one"), ("incidental", "unobtrusive, like the pen")):
        m = np.array([key in p for p in proc])
        r = Dr.random_effects(y[m], v[m])
        groups[name] = (int(m.sum()), r["estimate"], r["lo"], r["hi"])
    fd = np.array(c["file_drawer"])
    pub = Dr.random_effects(y[fd == "no"], v[fd == "no"])
    unpub = Dr.random_effects(y[fd == "yes"], v[fd == "yes"])
    return {"g": ys[order], "se": np.sqrt(vs)[order], "k_studies": len(ids), "k_effects": int(len(y)),
            "re": re["estimate"], "re_lo": re["lo"], "re_hi": re["hi"], "I2": re["I2"], "tau2": re["tau2"],
            "pet": pe["intercept"], "pet_se": pe["se_intercept"],
            "group_names": list(groups), "group_k": [g[0] for g in groups.values()],
            "group_est": [g[1] for g in groups.values()], "group_lo": [g[2] for g in groups.values()],
            "group_hi": [g[3] for g in groups.values()],
            "pub": pub["estimate"], "pub_k": pub["k"], "unpub": unpub["estimate"], "unpub_k": unpub["k"]}


SCENARIOS = [
    ("a colleague takes credit for your work", (-0.8, 0.7, -0.3, 0.9, 0.3, 0.4)),
    ("a noise downstairs at three in the morning", (-0.7, -0.8, 0.0, 0.1, -0.7, 0.8)),
    ("you pass the exam you trained months for", (0.85, 0.7, 0.9, -0.2, 0.6, 0.0)),
    ("your old dog dies", (-0.85, 0.7, -0.2, -0.2, -0.9, 0.1)),
    ("waiting to hear about a job you want", (0.4, -0.7, 0.1, 0.0, 0.0, 0.0)),
    ("you forget a friend's birthday party", (-0.6, 0.6, 0.9, -0.4, 0.3, 0.2)),
]


def compute_appraisal() -> dict:
    out = {"scenario": [s for s, _ in SCENARIOS], "dims": list(E.APPRAISAL_DIMS), "codes": [c for _, c in SCENARIOS]}
    for i, (_, code) in enumerate(SCENARIOS):
        a = E.appraise(code)
        out[f"labels{i}"] = a["labels"][:3]
        out[f"p{i}"] = a["p"][:3]
    out["prototypes"] = {k: list(v) for k, v in E.PROTOTYPES.items()}
    return out


def compute_fear() -> dict:
    s, k, n = E.two_roads("snake"), E.two_roads("stick"), E.two_roads("snake", amygdala=False)
    step = 5
    return {"t": s["t"][::step], "snake": s["a"][::step], "stick": k["a"][::step], "lesion": n["a"][::step],
            "early": s["peak_early"], "late": s["late"]}


def compute_forecast() -> dict:
    f = E.forecast()
    step = 3
    return {"t": f["t"][::step], "actual": f["actual"][::step], "predicted": f["predicted"][::step],
            "at": f["at"], "actual_at": f["actual_at"], "predicted_at": f["predicted_at"]}


def compute_income() -> dict:
    return E.income_world()


def compute_lorenz() -> dict:
    L = E.lorenz(T=30.0)
    return {"xyz": L[::4]}


ITEMS = {"attribution": compute_attribution, "faces": compute_faces, "pairs": compute_pairs,
         "feedback": compute_feedback, "appraisal": compute_appraisal, "fear": compute_fear,
         "forecast": compute_forecast, "income": compute_income, "lorenz": compute_lorenz}


if __name__ == "__main__":
    CACHE.main(ITEMS)
