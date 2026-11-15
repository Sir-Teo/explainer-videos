"""Precompute every number in Part 32 of *Psychology, Built* ("Intelligence").

    python -m videos.psychology.psych32.compute            # everything missing (about a minute)
    python -m videos.psychology.psych32.compute --force worlds

Results are cached in ``.cache/psych32/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.traits``; factor analysis by ``explainer.stats.kit.multi``); the data are Spearman's
1904 correlations (the Archive) and Holzinger and Swineford's 1939 test scores (lavaan, fetched and checked by
``explainer.psychology.opendata``).  Published numbers are quoted in the scenes with their sources.  Simulations
use fixed seeds.

Items:
    spearman    Spearman's six-by-six matrix: one-factor loadings, residuals and tetrad differences
    holzinger   301 children, nine tests: the correlation matrix, one to three ML factors with their tests, varimax
                loadings, and the correlations among the three composite scores (the second order)
    worlds      common cause, Thomson's sampling and mutualism: matrices and one-factor fits at n = 300, how often
                a one-factor test rejects each over 200 samples; training one ability in two of them
    scale       ratio and deviation IQs, and the standard error of a score at three reliabilities
    validity    a selected group's validity against the population's, and Thorndike's correction
    matrices    three example items, and a rule-tracking solver's accuracy by rules and capacity
    groups      overlap of two distributions; a latent gap against a biased test
    practice    the chance of scoring below 70 near it, Kelley's estimate, Brogden's selection gain at two
                validities, and two groups' selection-rate ratio by how selective the cut is
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import archive, opendata
from explainer.psychology.psyche import traits as T
from explainer.stats.kit import multi

CACHE = Cache("psych32")
load = CACHE.load


def compute_spearman() -> dict:
    d = archive.SPEARMAN_1904.data
    R = np.array(d["R"])
    f = T.one_factor(R, n=None)
    tet = T.tetrads(R)
    return {"names": d["names"], "R": R, "loadings": f["loadings"], "residual": f["residual"], "rmsr": f["rmsr"],
            "tetrads": tet, "tetrad_mean_abs": float(np.mean(np.abs(tet))), "share": f["share"]}


def compute_holzinger() -> dict:
    h = opendata.holzinger_1939()
    X = h["X"]
    R = T.corr(X)
    n = len(X)
    fits = {}
    for k in (1, 2, 3):
        f = multi.factor_ml(R, k, n=n)
        fits[k] = f
    L3 = multi.varimax(fits[3]["loadings"])["loadings"]
    # order the three factors as visual, verbal, speed by which tests load most
    order = [int(np.argmax(np.abs(L3[i0:i0 + 3]).sum(0))) for i0 in (0, 3, 6)]
    L3 = L3[:, order] * np.sign(L3[:, order].sum(0))
    comp = np.column_stack([((X[:, i0:i0 + 3] - X[:, i0:i0 + 3].mean(0)) / X[:, i0:i0 + 3].std(0)).sum(1)
                            for i0 in (0, 3, 6)])
    Rc = T.corr(comp)
    one = T.one_factor(R, n=n)
    off = R[~np.eye(9, dtype=bool)]
    return {"R": R, "n": n, "min_r": float(off.min()), "mean_r": float(off.mean()), "neg": int((off < 0).sum() // 2),
            "L1": one["loadings"], "share1": one["share"], "rmsr1": one["rmsr"], "L3": L3,
            "chi2": [fits[k]["chi2"] for k in (1, 2, 3)], "df": [fits[k]["df"] for k in (1, 2, 3)],
            "p": [fits[k]["p"] for k in (1, 2, 3)], "Rc": Rc, "second": T.one_factor(Rc)["loadings"]}


def compute_worlds() -> dict:
    out = {}
    for name, X in (("common", T.common_cause(n=300, seed=10)), ("sampling", T.sampling(n=300, seed=11)),
                    ("mutualism", T.mutualism(n=300, seed=12))):
        R = T.corr(X)
        f = T.one_factor(R, n=300)
        out[f"R_{name}"] = R
        out[f"L_{name}"] = f["loadings"]
        out[f"p_{name}"] = f["p"]
        out[f"rmsr_{name}"] = f["rmsr"]
        out[f"min_{name}"] = float(R[~np.eye(len(R), dtype=bool)].min())
    gens = {"common": lambda s: T.common_cause(n=300, seed=s), "sampling": lambda s: T.sampling(n=300, seed=s),
            "mutualism": lambda s: T.mutualism(n=300, seed=s)}
    reps = 200
    for name, fn in gens.items():
        out[f"reject_{name}"] = float(np.mean([T.one_factor(T.corr(fn(1000 + s)), n=300)["p"] < 0.05
                                               for s in range(reps)]))
    out["reps"] = reps
    out["train_common"] = T.train_one("common")["change"]
    out["train_mutualism"] = T.train_one("mutualism")["change"]
    return out


def compute_scale() -> dict:
    ma = np.array([6.0, 8.0, 10.0, 12.0])
    return {"ratio_child": float(T.ratio_iq(10, 8)), "ratio_adult": float(T.ratio_iq(16, 40)),
            "rel": [0.80, 0.90, 0.95], "sem": [T.sem_interval(100, r)["sem"] for r in (0.80, 0.90, 0.95)],
            "dev_example": float(T.deviation_iq(42, 34, 6)), "ma": ma}


def compute_validity() -> dict:
    rng = np.random.default_rng(32)
    n = 200_000
    r = 0.5
    test = rng.normal(size=n)
    perf = r * test + np.sqrt(1 - r ** 2) * rng.normal(size=n)
    cut = np.quantile(test, 0.7)
    sel = test > cut
    r_sel = float(np.corrcoef(test[sel], perf[sel])[0, 1])
    u = float(test[sel].std() / test.std())
    idx = rng.choice(n, 1500, replace=False)
    return {"r_pop": float(np.corrcoef(test, perf)[0, 1]), "r_sel": r_sel, "u": u,
            "r_corrected": T.restriction_corrected(r_sel, u), "x": test[idx], "y": perf[idx], "cut": float(cut),
            "sel_idx": sel[idx]}


def compute_matrices() -> dict:
    rng = np.random.default_rng(2032)
    out = {}
    for k in (1, 2, 3):
        it = T.matrix_item(rng, k, n_options=4)
        out[f"grid{k}"] = it["grid"]
        out[f"options{k}"] = np.array(it["options"])
        out[f"correct{k}"] = it["correct"]
        out[f"rules{k}"] = [it["rules"][a] for a in T.ATTRS]
    caps = (1, 2, 3, 4)
    for c in caps:
        out[f"acc_cap{c}"] = [T.solver_accuracy(c, k, trials=400, seed=c) for k in range(5)]
    w = np.array([0.15, 0.35, 0.35, 0.15])
    out["acc_pop"] = list(np.sum([w[i] * np.array(out[f"acc_cap{c}"]) for i, c in enumerate(caps)], axis=0))
    out["weights"] = w
    return out


def compute_groups() -> dict:
    out = {"d": [0.2, 0.5, 1.0]}
    out["overlap"] = [T.overlap(d)["overlap"] for d in out["d"]]
    out["above"] = [T.overlap(d)["above_mean"] for d in out["d"]]
    a = T.invariance_demo(latent_gap=0.4, bias=0.0)
    b = T.invariance_demo(latent_gap=0.0, bias=0.6)
    out.update({"latent_tests": a["d_tests"], "latent_total": a["d_total"], "bias_tests": b["d_tests"],
                "bias_total": b["d_total"], "loadings": a["loadings"]})
    return out


def compute_practice() -> dict:
    true = np.arange(64, 81)
    rels = [0.80, 0.90, 0.95]
    out = {"true": true, "rels": rels}
    for r in rels:
        out[f"below_{int(r * 100)}"] = T.below_cut(true, 70, r)
    out["at72"] = [float(T.below_cut(72, 70, r)) for r in rels]
    out["at68"] = [float(T.below_cut(68, 70, r)) for r in rels]
    out["kelley69"] = [float(T.kelley(69, r)) for r in rels]
    ratio = np.linspace(0.02, 1.0, 50)
    out["ratio"] = ratio
    out["validities"] = [0.31, 0.51]
    out["gain31"] = T.selection_gain(0.31, ratio)
    out["gain51"] = T.selection_gain(0.51, ratio)
    out["gain_at"] = {f"{v}_{s_}": float(T.selection_gain(v, s_)) for v in (0.31, 0.51) for s_ in (0.1, 0.5)}
    out["impact_d"] = 0.5
    imp = T.impact_ratio(0.5, ratio)
    out["impact"] = imp["ratio"]
    out["impact_at"] = {f"{s_}": float(T.impact_ratio(0.5, s_)["ratio"]) for s_ in (0.1, 0.3, 0.5, 0.8)}
    # where the ratio crosses four-fifths
    fine = np.linspace(0.01, 0.999, 2000)
    rr = T.impact_ratio(0.5, fine)["ratio"]
    out["four_fifths_at"] = float(fine[np.argmax(rr >= 0.8)])
    return out


ITEMS = {"spearman": compute_spearman, "holzinger": compute_holzinger, "worlds": compute_worlds,
         "scale": compute_scale, "validity": compute_validity, "matrices": compute_matrices, "groups": compute_groups,
         "practice": compute_practice}


if __name__ == "__main__":
    CACHE.main(ITEMS)
