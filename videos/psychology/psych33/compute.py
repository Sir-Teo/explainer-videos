"""Precompute every number in Part 33 of *Psychology, Built* ("Personality").

    python -m videos.psychology.psych33.compute            # everything missing (about a minute; fetches psychTools once)
    python -m videos.psychology.psych33.compute --force acts

Results are cached in ``.cache/psych33/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.personality``; factor analysis by ``explainer.stats.kit.multi``); the data are the SAPA
project's 25 IPIP items for 2,800 people and the EPI/BFI sample of 231 (psychTools, fetched and checked by
``explainer.psychology.opendata``).  Published numbers are quoted in the scenes with their sources.  Simulations use
fixed seeds.

Items:
    factors     the 25 items: correlations, eigenvalues against parallel analysis, five ML factors with varimax
                loadings, Cronbach's alpha for each scale, the scales' intercorrelations
    types       extraversion's distribution and its median split; same-type shares at three reliabilities; the share
                of a correlation a median split keeps
    acts        a person-and-situation world: single-act and aggregated consistency against Spearman-Brown, the
                same act on two occasions, variance components, two people's if-then signatures
    ages        scale means by age band (a cross-section, so cohort and age are confounded)
    eysenck     the EPI against the BFI: a small multitrait-multimethod matrix
    outcomes    the binomial effect-size display for three correlations
    sexes       d for each scale and each item; Mahalanobis D for 5 scales and 25 items, its overlap, and D as
                items are added
    likes       a simulated footprint world: accuracy of ridge predictions by number of likes
    faking      applicants who inflate conscientiousness, and who gets hired
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import measure, opendata
from explainer.psychology.psyche import personality as P
from explainer.stats.kit import multi

CACHE = Cache("psych33")
load = CACHE.load


def _bfi():
    d = opendata.bfi()
    return d["X"], d["items"], d


def compute_factors() -> dict:
    X, items, d = _bfi()
    ok = ~np.isnan(X).any(axis=1)
    Xc = X[ok]
    R = np.corrcoef(Xc, rowvar=False)
    pa = P.parallel(X, n_iter=50, seed=33)
    f = multi.factor_ml(R, 5, n=int(ok.sum()))
    v = multi.varimax(f["loadings"])
    L = np.asarray(v["loadings"])
    # order and sign the factors to match A, C, E, N, O: each factor named by the trait whose items load most
    order, signs = [], []
    for t in P.TRAITS:
        cols = [j for j, nm in enumerate(items) if nm[0] == t]
        key = np.array([P.KEYS[items[j]] for j in cols])
        score = [abs(np.sum(L[cols, k] * key)) for k in range(5)]
        k = int(np.argmax(score))
        order.append(k)
        signs.append(1.0 if np.sum(L[cols, k] * key) > 0 else -1.0)
    L = L[:, order] * np.array(signs)
    sc = P.score(X, items)
    alphas = {}
    for t in P.TRAITS:
        cols = [j for j, nm in enumerate(items) if nm[0] == t]
        Y = Xc[:, cols].copy()
        for k, j in enumerate(cols):
            if P.KEYS[items[j]] < 0:
                Y[:, k] = 7 - Y[:, k]
        alphas[t] = float(measure.cronbach_alpha(Y))
    S5 = np.column_stack([sc[t] for t in P.TRAITS])
    S5 = S5[~np.isnan(S5).any(axis=1)]
    Rs = np.corrcoef(S5, rowvar=False)
    own = np.array([L[j, P.TRAITS.index(nm[0])] for j, nm in enumerate(items)])
    return {"items": items, "R": R, "n": int(ok.sum()), "n_all": int(len(X)), "eigen": pa["eigen"],
            "random": pa["random"], "keep": pa["keep"], "L": L, "own": own, "alpha": [alphas[t] for t in P.TRAITS],
            "Rs": Rs, "chi2": f.get("chi2"), "df": f.get("df")}


def compute_types() -> dict:
    X, items, d = _bfi()
    e = P.score(X, items)["E"]
    e = e[~np.isnan(e)]
    med = float(np.median(e))
    hist, edges = np.histogram(e, bins=np.arange(0.9, 6.4, 0.6))  # each bin holds three possible five-item means
    near = float(np.mean(np.abs(e - med) < 0.5 * e.std()))
    rows = {r: P.type_agreement(r, dims=4) for r in (0.7, 0.8, 0.9)}
    return {"hist": hist, "edges": edges, "median": med, "sd": float(e.std()), "near": near, "n": int(len(e)),
            "rel": [0.7, 0.8, 0.9], "one": [rows[r]["one"] for r in (0.7, 0.8, 0.9)],
            "all4": [rows[r]["all"] for r in (0.7, 0.8, 0.9)], "all4_sim": [rows[r]["all_sim"] for r in (0.7, 0.8, 0.9)],
            "keep": P.dichotomy_loss()}


def compute_acts() -> dict:
    w = P.act_world(n=4000, situations=40, seed=33)
    a = P.aggregate_curve(w, ks=(1, 2, 4, 8, 16), seed=1)
    comp = P.components(w["sd"])
    rng = np.random.default_rng(5)
    idx = rng.choice(len(w["b1"]), 1200, replace=False)
    # two people with the same average across eight situations but different signatures
    S = 8
    b = (w["b1"][:, :S] + w["b2"][:, :S]) / 2
    m = b.mean(1)
    i0 = int(np.argmin(np.abs(m - 0.5)))
    cand = np.where(np.abs(m - m[i0]) < 0.05)[0]
    prof = b[cand] - b[cand].mean(1, keepdims=True)
    j = int(cand[np.argmin(prof @ prof[list(cand).index(i0)])])
    return {"k": a["k"], "observed": a["observed"], "sb": a["spearman_brown"], "single": a["single"],
            "same": a["same_situation"], "comp": [comp[k] for k in ("person", "situation", "signature", "noise")],
            "x": w["b1"][idx, 0], "y": w["b1"][idx, 1], "p1": b[i0], "p2": b[j], "pull": w["pull"][:S]}


def compute_ages() -> dict:
    X, items, d = _bfi()
    sc = P.score(X, items)
    age = d["age"]
    bands = [(16, 20), (20, 25), (25, 30), (30, 40), (40, 50), (50, 66)]
    mids, n, means = [], [], {t: [] for t in P.TRAITS}
    for lo, hi in bands:
        k = (age >= lo) & (age < hi)
        mids.append((lo + hi - 1) / 2)
        n.append(int(k.sum()))
        for t in P.TRAITS:
            means[t].append(float(np.nanmean(sc[t][k])))
    sd = {t: float(np.nanstd(sc[t])) for t in P.TRAITS}
    return {"bands": bands, "mid": mids, "n": n, **{f"m_{t}": means[t] for t in P.TRAITS},
            "sd": [sd[t] for t in P.TRAITS], "median_age": float(np.nanmedian(age))}


def compute_eysenck() -> dict:
    e = opendata.epi_bfi()
    cols = ["epiE", "epiNeur", "bfext", "bfneur"]
    M = np.column_stack([e[c] for c in cols])
    M = M[~np.isnan(M).any(axis=1)]
    return {"names": cols, "R": np.corrcoef(M, rowvar=False), "n": int(len(M))}


def compute_outcomes() -> dict:
    rs = [0.1, 0.2, 0.3]
    return {"r": rs, "hi": [P.besd(r)[0] for r in rs], "lo": [P.besd(r)[1] for r in rs]}


def compute_sexes() -> dict:
    X, items, d = _bfi()
    g = d["gender"]
    sc = P.score(X, items)
    S5 = np.column_stack([sc[t] for t in P.TRAITS])
    m5 = P.mahalanobis(S5[g == 1], S5[g == 2])
    m25 = P.mahalanobis(X[g == 1], X[g == 2])
    ok = ~np.isnan(X).any(axis=1)
    curve = P.d_by_dimensions(X[ok & (g == 1)], X[ok & (g == 2)], [1, 2, 3, 5, 8, 12, 18, 25], reps=60, seed=33)
    return {"d5": m5["d"], "D5": m5["D"], "ovl5": P.overlap_d(m5["D"]), "n": list(m5["n"]), "d25": m25["d"],
            "D25": m25["D"], "ovl25": P.overlap_d(m25["D"]), "items": items, "k": curve["k"], "D_k": curve["D"],
            "absd_k": curve["mean_abs_d"], "ovl_dg": P.overlap_d(2.71)}


def compute_likes() -> dict:
    w = P.likes_world(n=6000, likes=2000, seed=33)
    ks = [5, 10, 20, 40, 70, 100, 150, 200, 300, 500, 1000, 2000]
    acc = P.likes_accuracy(w, ks, trait=4)
    density = float(w["L"].mean())
    return {"k": ks, "r": acc["r"], "density": density, "per_person": float(w["L"].sum(1).mean())}


def compute_faking() -> dict:
    out = {}
    for share in (0.1, 0.3, 0.5):
        f = P.faking(share=share, lift=0.8, validity=0.25, select=0.1, seed=33)
        out[f"s{int(share * 100)}"] = f
    return out


ITEMS = {"factors": compute_factors, "types": compute_types, "acts": compute_acts, "ages": compute_ages,
         "eysenck": compute_eysenck, "outcomes": compute_outcomes, "sexes": compute_sexes, "likes": compute_likes,
         "faking": compute_faking}


if __name__ == "__main__":
    CACHE.main(ITEMS)
