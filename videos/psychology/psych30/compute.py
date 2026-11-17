"""Precompute every number in Part 30 of *Psychology, Built* ("The Infant Mind").

    python -m videos.psychology.psych30.compute            # everything missing (under a minute)
    python -m videos.psychology.psych30.compute --force anotb

Results are cached in ``.cache/psych30/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.develop``; the pooled estimates use ``drive.random_effects``); the data are ManyBabies
1's lab-level effect sizes (psymetadata), fetched and checked by ``explainer.psychology.opendata``.  Published
numbers are quoted in the scenes with their sources.  Simulations use fixed seeds.

Items:
    habituation  looks across familiarization trials, the criterion, and the first test looks
    goldilocks   an ideal learner's surprisal on three kinds of sequence, and the U-shaped look-away rate
    manybabies   ManyBabies 1: each lab's effect, the pooled estimate, by method, by age group, and the age slope
    number       the chance of telling two numbers apart by age, the 75% ratio thresholds, 8 v 16 and 8 v 12
    statistics   the infant statistician's sample probabilities
    anotb        the dynamic field's A-not-B errors against delay for a younger and an older field, against the
                 number of A trials, and one field on the B trial
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import opendata
from explainer.psychology.psyche import develop as D
from explainer.psychology.psyche import drive as Dr

CACHE = Cache("psych30")
load = CACHE.load

YOUNG, OLD = -6.0, -3.0  # the field's resting level: less and more cooperative


def compute_habituation() -> dict:
    h = D.habituation(seed=3)
    return {"trial": h["trial"], "looks": h["looks"], "criterion": h["criterion"], "first3": h["first3"],
            "familiar": h["familiar"], "novel": h["novel"]}


def compute_goldilocks() -> dict:
    rng = np.random.default_rng(30)
    out = {}
    for kind, p in D.KINDS.items():
        seq = rng.choice(3, size=24, p=p)
        out[f"seq_{kind}"] = seq
        out[f"s_{kind}"] = D.surprisal_trace(seq)
    g = D.goldilocks()
    out.update({"surprisal": g["surprisal"], "rate": g["rate"], "best": g["best"],
                "len_predictable": g["mean_length"]["predictable"],
                "len_intermediate": g["mean_length"]["intermediate"], "len_random": g["mean_length"]["random"]})
    return out


def compute_manybabies() -> dict:
    d = opendata.manybabies_2020()
    y, v, n = d["yi"], d["vi"], d["ni"]
    age, meth, grp = d["age_mo"], np.array(d["method"]), np.array(d["age_group"])
    re = Dr.random_effects(y, v)
    order = np.argsort(y)
    out = {"y": y[order], "se": np.sqrt(v[order]), "method_sorted": list(meth[order]), "age": age, "yall": y,
           "k": int(len(y)), "labs": len(set(d["lab"])), "infants": int(n.sum()), "re": re["estimate"],
           "re_lo": re["lo"], "re_hi": re["hi"], "I2": re["I2"], "tau2": re["tau2"]}
    names = ["Central fixation", "Eye tracking", "HPP"]
    out["method_names"] = names
    for key, vals in (("method", names), ("group", ["3-6 mo", "6-9 mo", "9-12 mo", "12-15 mo"])):
        arr = meth if key == "method" else grp
        est, lo, hi, kk, nn = [], [], [], [], []
        for nm in vals:
            m = arr == nm
            r = Dr.random_effects(y[m], v[m])
            est.append(r["estimate"]), lo.append(r["lo"]), hi.append(r["hi"])
            kk.append(int(m.sum())), nn.append(int(n[m].sum()))
        out[f"{key}_est"], out[f"{key}_lo"], out[f"{key}_hi"] = est, lo, hi
        out[f"{key}_k"], out[f"{key}_n"] = kk, nn
    out["group_names"] = ["3-6 mo", "6-9 mo", "9-12 mo", "12-15 mo"]
    X = np.column_stack([np.ones_like(y), age - age.mean(), (meth == "HPP").astype(float),
                         (meth == "Eye tracking").astype(float)])
    mr = D.meta_regression(y, v, X)
    out["age_slope"], out["age_slope_se"] = float(mr["b"][1]), float(mr["se"][1])
    out["hpp_b"], out["hpp_se"] = float(mr["b"][2]), float(mr["se"][2])
    out["age_mean"] = float(age.mean())
    nae = d["nae"] == 1
    for k_, m in (("nae", nae), ("other", ~nae)):
        r = Dr.random_effects(y[m], v[m])
        out[f"{k_}_est"], out[f"{k_}_k"] = r["estimate"], int(m.sum())
    return out


def compute_number() -> dict:
    ratios = np.linspace(1.0, 4.0, 121)
    out = {"ratio": ratios, "ages": list(D.WEBER)}
    for i, (age, w) in enumerate(D.WEBER.items()):
        out[f"p{i}"] = D.ans_correct(ratios, 1.0, w)
        out[f"thr{i}"] = D.ratio_threshold(w)
        out[f"w{i}"] = w
    w6 = D.WEBER["6 months"]
    out["p_8_16"] = float(D.ans_correct(16, 8, w6))
    out["p_8_12"] = float(D.ans_correct(12, 8, w6))
    out["p_8_12_9mo"] = float(D.ans_correct(12, 8, D.WEBER["9 months"]))
    return out


def compute_statistics() -> dict:
    out = {"p_white": 0.9}
    for k, (nr, n) in {"mostly_red": (4, 5), "mostly_white": (1, 5)}.items():
        s = D.sample_surprise(0.1, nr, n)
        out[f"{k}_p"], out[f"{k}_bits"] = s["p"], s["bits"]
    out["ratio"] = out["mostly_white_p"] / out["mostly_red_p"]
    return out


def compute_anotb() -> dict:
    delays = np.arange(0.0, 10.5, 1.0)
    out = {"delays": delays}
    for key, h in (("young", YOUNG), ("old", OLD)):
        res = [D.a_not_b(h, float(dl), n=300, seed=7) for dl in delays]
        out[f"err_{key}"] = np.array([r["error"] for r in res])
        out[f"acc_{key}"] = np.array([r["a_correct"] for r in res])
    nas = [1, 2, 4, 6, 8, 10]
    out["n_a"] = nas
    out["err_by_na"] = np.array([D.a_not_b(YOUNG, 3.0, n_a=k, n=300, seed=8)["error"] for k in nas])
    for key, h in (("young", YOUNG), ("old", OLD)):
        f = D.field_snapshot(h, 3.0)
        out[f"field_{key}"] = f["u"]
        out[f"reach_{key}"] = f["reach"]
    out["x"] = D.FIELD_X
    out["h_young"], out["h_old"] = YOUNG, OLD
    return out


ITEMS = {"habituation": compute_habituation, "goldilocks": compute_goldilocks, "manybabies": compute_manybabies,
         "number": compute_number, "statistics": compute_statistics, "anotb": compute_anotb}


if __name__ == "__main__":
    CACHE.main(ITEMS)
