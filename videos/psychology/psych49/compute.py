"""Precompute every number in Part 49 of *Psychology, Built* ("Modelling the Brain's Data").

    python -m videos.psychology.psych49.compute            # everything missing (a few minutes)
    python -m videos.psychology.psych49.compute --force multiverse

Results are cached in ``.cache/psych49/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.neurodata``, with Part 8's synthetic brain from ``psyche.imaging``).

Items:
    multiverse  one synthetic group study (30 people, five regional hypotheses) through 72 pipelines
    groupmap    the group's truth, one subject's map and the group t map, for display
    fixed       fixed against random effects when subjects differ
    clusterfwe  cluster-extent inference calibrated on Gaussian noise against permutation, in long-tailed noise
    motion      head motion's distance-dependent artefact in connectivity, before and after censoring
    gsr         global-signal regression and the anticorrelations it makes
    decoding    cross-validated decoding of noise and of a weak signal, with and without leakage
    rsa         representational similarity: a category model, a size model and the noise ceiling
    encoding    a ridge encoding model's prediction against each voxel's noise ceiling
    erp         ERP windows fixed in advance, chosen from the difference, or from an orthogonal localizer
    popvec      the population vector's error by number of neurons
    manifold    the variance of a hundred neurons in their principal components
    itr         a brain-computer interface's information rate for some targets and accuracies
    bwas        brain-behaviour correlations at 25 to 4,000 people
    thresholds  the group map under four thresholding rules; the sample for 80% power at r = 0.1
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import neurodata as N

CACHE = Cache("psych49")
load = CACHE.load


def compute_multiverse() -> dict:
    m = N.multiverse(n=30, seed=49)
    th = [p.split(" / ")[1] for p in m["paths"]]
    sm = [p.split(" / ")[0] for p in m["paths"]]
    by_th = {t: m["yes"][[i for i, x in enumerate(th) if x == t]].mean(0) for t in N.PIPELINE["threshold"]}
    by_sm = {s: m["yes"][[i for i, x in enumerate(sm) if x == s]].mean(0) for s in sorted(set(sm))}
    return {"yes": m["yes"].astype(int), "share": m["share"], "effects": np.array(m["effects"]),
            "distinct": m["distinct_maps"], "n_paths": m["n_paths"], "paths": m["paths"],
            "by_threshold": np.array([by_th[t] for t in N.PIPELINE["threshold"]]),
            "thresholds": list(N.PIPELINE["threshold"]), "by_smoothing": np.array(list(by_sm.values())),
            "smoothings": list(by_sm)}


def compute_groupmap() -> dict:
    d = N.subject_maps(n=30, long_tail=0.3, seed=49)
    t, df = N.one_sample_t(d["maps"], d["mask"])
    return {"truth": d["truth"], "one": d["maps"][0], "two": d["maps"][1], "t": t, "mask": d["mask"].astype(int),
            "df": df, "motion": d["motion"]}


def compute_fixed() -> dict:
    return N.fixed_vs_random(reps=200, seed=4901)


def compute_clusterfwe() -> dict:
    a = N.cluster_fwe(n_sets=200, perms=200, long_tail=0.6, primary_p=0.01, seed=4902)
    b = N.cluster_fwe(n_sets=200, perms=200, long_tail=0.6, primary_p=0.001, seed=4903)
    return {"lenient_parametric": a["parametric"], "lenient_permutation": a["permutation"], "lenient_extent": a["extent"],
            "strict_parametric": b["parametric"], "strict_permutation": b["permutation"], "strict_extent": b["extent"],
            "sets": a["sets"]}


def compute_motion() -> dict:
    return N.motion_connectivity(seed=4904)


def compute_gsr() -> dict:
    return N.global_signal(seed=4905)


def compute_decoding() -> dict:
    a = N.decoding(reps=100, signal=0.0, seed=4906)
    b = N.decoding(reps=100, signal=0.3, seed=4907)
    return {"null_" + k: v for k, v in a.items() if k != "signal"} | {"sig_" + k: v for k, v in b.items()
                                                                       if k != "signal"}


def compute_rsa() -> dict:
    return N.rsa(seed=4908)


def compute_encoding() -> dict:
    e = N.encoding(seed=4909)
    resp = e["responsive"]
    return {"r": e["r"], "ceiling": e["ceiling"], "responsive": resp.astype(int), "lambda": e["lambda"],
            "median_r": float(np.median(e["r"][resp])), "median_ceiling": float(np.median(e["ceiling"][resp])),
            "median_fraction": float(np.median(e["r"][resp] / e["ceiling"][resp]))}


def compute_erp() -> dict:
    return N.erp_windows(reps=2000, seed=4910)


def compute_popvec() -> dict:
    return N.population_vector_error(seed=4911)


def compute_manifold() -> dict:
    return N.manifold(seed=4912)


def compute_itr() -> dict:
    cases = [("two targets, 90% right, 4 s each", 2, 0.90, 4.0),
             ("four targets, 80% right, 3 s each", 4, 0.80, 3.0),
             ("26 letters, 95% right, 1.5 s each", 26, 0.95, 1.5)]
    return {"labels": [c[0] for c in cases], "bits_per_min": np.array([N.wolpaw_itr(*c[1:]) for c in cases]),
            "acc": np.linspace(0.3, 1.0, 50),
            "curve": np.array([N.wolpaw_itr(4, a, 3.0) if a > 0.25 else 0.0 for a in np.linspace(0.3, 1.0, 50)])}


def compute_bwas() -> dict:
    b = N.bwas(true_r=0.1, seed=4913)
    return b | {"attenuated": N.attenuated(0.2, 0.4, 0.8)}


def compute_thresholds() -> dict:
    """The group study at 4 mm, no exclusion, no covariate, under four rules, for display; and the people needed
    for 80% power at r = 0.1."""
    from explainer.psychology.psyche import imaging as Im
    d = N.subject_maps(n=30, long_tail=0.3, seed=49)
    ext = N.gaussian_extents(30, seed=50)
    cache = {}
    out = {"truth": d["truth"], "mask": d["mask"].astype(int)}
    for key, rule in (("unc", "p<0.001"), ("fdr", "FDR 5%"), ("clus", "cluster p<0.01"), ("perm", "permutation")):
        out[key] = N.run_pipeline(d, 4.0, rule, "none", "none", ext, cache).astype(int)
    out["n_r01"] = Im.n_for_correlation(0.1)
    return out


ITEMS = {"multiverse": compute_multiverse, "groupmap": compute_groupmap, "fixed": compute_fixed,
         "clusterfwe": compute_clusterfwe, "motion": compute_motion, "gsr": compute_gsr, "decoding": compute_decoding,
         "rsa": compute_rsa, "encoding": compute_encoding, "erp": compute_erp, "popvec": compute_popvec,
         "manifold": compute_manifold, "itr": compute_itr, "bwas": compute_bwas,
         "thresholds": compute_thresholds}

if __name__ == "__main__":
    CACHE.main(ITEMS)
