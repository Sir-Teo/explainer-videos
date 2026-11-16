"""Precompute every number in Part 47 of *Psychology, Built* ("People over Time").

    python -m videos.psychology.psych47.compute            # everything missing (several minutes)
    python -m videos.psychology.psych47.compute --force fpr

Results are cached in ``.cache/psych47/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.within``), with mixed models from *Statistics, Built*'s ``statkit.mixed``.

Items:
    example     one simulated priming study (30 participants, 20 items, no effect): the by-participant, by-item and
                min F' analyses
    fpr         the false-positive rate of each analysis over 200 simulated studies with no effect
    stimpower   power of the crossed analysis for a real effect as the number of items grows (30 participants)
    slopes      40 people, 15 observations each: their own regression slopes against the multilevel model's
    simpson     12 people: a negative slope between people and a positive slope within each
    ergodic     200 people, 100 occasions: cross-sectional correlations against each person's own
    inertia     the bias of a person's autoregression estimated from T occasions
    tipping     a double-well system tipping, with rolling autocorrelation and variance; hit and false-alarm rates
                from a continuous record and from a noisy daily diary
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import within as Wi

CACHE = Cache("psych47")
load = CACHE.load


def compute_example() -> dict:
    d = Wi.priming_study(seed=47)
    m = Wi.min_f_test(d)
    return {"F1": Wi.by_subject_test(d), "F2": Wi.by_item_test(d), "minF_p": m["p"],
            "item_means": np.array([d["y"][d["item"] == j].mean() for j in range(20)]),
            "item_cond": np.array([d["cond"][d["item"] == j][0] for j in range(20)])}


def compute_fpr() -> dict:
    return Wi.false_positive_rates(reps=200, seed=4700)


def compute_stimpower() -> dict:
    return Wi.stimulus_power(0.4, [8, 12, 20, 32, 48], n_subj=30, reps=80, seed=4800)


def compute_slopes() -> dict:
    return Wi.person_slopes(n_obs=15, seed=47)


def compute_simpson() -> dict:
    return Wi.simpson_cloud(between=-1.0, within=0.6, seed=47)


def compute_ergodic() -> dict:
    r = Wi.nonergodic(seed=47)
    return {"cross_mean": r["cross_mean"], "within": r["within"], "share_near": r["share_near"],
            "within_hist": np.histogram(r["within"], bins=np.linspace(-1, 1, 21))[0],
            "share_negative": float(np.mean(r["within"] < 0))}


def compute_inertia() -> dict:
    return Wi.inertia_bias(phi=0.4, Ts=(10, 20, 30, 50, 100, 200), reps=2000, seed=47)


def compute_tipping() -> dict:
    d = Wi.double_well(T=3000, seed=4)
    ind = Wi.rolling_indicators(d["x"], 300)
    end = max(350, d["tip"] - 50)
    tau_ac = Wi.kendall_trend(ind["ac"][:end])
    tau_var = Wi.kendall_trend(ind["var"][:end])
    rates = Wi.warning_rates(n=100, window=300, threshold=0.5, seed=4900)
    diary = Wi.warning_rates(n=100, window=30, threshold=0.3, seed=4900, thin=15, noise_obs=0.3)
    return {"diary_hit": diary["hit"], "diary_false": diary["false_alarm"],"x": d["x"], "c": d["c"], "tip": d["tip"], "ac": ind["ac"], "var": ind["var"], "tau_ac": tau_ac,
            "tau_var": tau_var, **rates}


def compute_shrinkw() -> dict:
    """How much partial pooling trusts a person's own slope: G / (G + sigma^2 / (n var x)), with the planted slope
    variance 0.09 and noise variance 1, by observations per person."""
    n = np.arange(2, 61)
    return {"n": n, "w": 0.09 / (0.09 + 1.0 / n)}


def compute_slopefpr() -> dict:
    """Participants who differ in the effect (SD 0.5) and words that barely differ (SD 0.2): with no average effect,
    the by-item test is now the one fooled."""
    return Wi.false_positive_rates(reps=200, seed=4710, item_sd=0.2, slope_sd=0.5)


def compute_powergrid() -> dict:
    subj, items = [15, 30, 60, 120], [10, 20, 40]
    P = np.zeros((len(subj), len(items)))
    for i, s in enumerate(subj):
        P[i] = Wi.stimulus_power(0.4, items, n_subj=s, reps=40, seed=4720 + i)["power"]
    return {"subj": np.array(subj), "items": np.array(items), "power": P}


def compute_growth() -> dict:
    return Wi.growth_split(seed=47)


def compute_ownslopes() -> dict:
    d = load("simpson")
    x, y, g = d["x"], d["y"], d["g"]
    return {"slopes": np.array([np.polyfit(x[g == i], y[g == i], 1)[0] for i in range(g.max() + 1)]),
            "pooled": d["pooled"]}


def compute_owngroup() -> dict:
    return Wi.own_vs_group(seed=47)


def compute_waves() -> dict:
    return Wi.crosslag_waves(seed=47)


def compute_neff() -> dict:
    """100 people, m observations each, intraclass correlation 0.3: the variance of the grand mean over 4,000
    simulated studies, as an effective number of independent observations, against N m / (1 + (m - 1) ICC)."""
    rng = np.random.default_rng(4701)
    icc, N = 0.3, 100
    ms = np.array([1, 2, 5, 10, 20, 50])
    sim = []
    for m in ms:
        u = rng.normal(0, np.sqrt(icc), (4000, N, 1))
        e = rng.normal(0, np.sqrt(1 - icc), (4000, N, int(m)))
        g = (u + e).mean(axis=(1, 2))
        sim.append(1 / g.var())
    return {"m": ms, "neff_sim": np.array(sim), "neff": N * ms / (1 + (ms - 1) * icc), "icc": icc, "N": N}


def compute_naive() -> dict:
    """30 people, 20 occasions, each with their own slope (mean 0, SD 0.3): the pooled regression's naive test
    against a t-test on the 30 person slopes, false positives at 5% over 2,000 studies."""
    from scipy import stats
    rng = np.random.default_rng(4702)
    P, T, reps = 30, 20, 2000
    naive = summary = 0
    for r in range(reps):
        x = rng.normal(size=(P, T))
        b = rng.normal(0, 0.3, (P, 1))
        a = rng.normal(0, 1, (P, 1))
        y = a + b * x + rng.normal(size=(P, T))
        naive += stats.linregress(x.ravel(), y.ravel()).pvalue < 0.05
        sl = np.array([np.polyfit(x[i], y[i], 1)[0] for i in range(P)])
        summary += stats.ttest_1samp(sl, 0).pvalue < 0.05
    return {"naive": naive / reps, "summary": summary / reps, "reps": reps}


def compute_relmean() -> dict:
    """The reliability of a person's average mood from k prompts when the intraclass correlation of single prompts
    is 0.4 (Spearman-Brown), checked on 500 simulated people."""
    rng = np.random.default_rng(4703)
    icc = 0.4
    ks = np.array([1, 3, 7, 14, 28, 56])
    sim = []
    for k in ks:
        u = rng.normal(0, np.sqrt(icc), 500)
        a = u[:, None] + rng.normal(0, np.sqrt(1 - icc), (500, int(k)))
        b = u[:, None] + rng.normal(0, np.sqrt(1 - icc), (500, int(k)))
        sim.append(np.corrcoef(a.mean(1), b.mean(1))[0, 1])
    return {"k": ks, "rel": ks * icc / (1 + (ks - 1) * icc), "rel_sim": np.array(sim), "icc": icc}


def compute_windows() -> dict:
    """Early-warning hit and false-alarm rates on the continuous record, by the width of the rolling window."""
    ws = np.array([100, 200, 300, 500])
    hit, fa = [], []
    for w in ws:
        r = Wi.warning_rates(n=60, window=int(w), seed=4704)
        hit.append(r["hit"]); fa.append(r["false_alarm"])
    return {"window": ws, "hit": np.array(hit), "false_alarm": np.array(fa)}


ITEMS = {"shrinkw": compute_shrinkw, "slopefpr": compute_slopefpr, "powergrid": compute_powergrid,
         "growth": compute_growth, "ownslopes": compute_ownslopes, "owngroup": compute_owngroup, "waves": compute_waves,
         "neff": compute_neff, "naive": compute_naive, "relmean": compute_relmean, "windows": compute_windows,
         "example": compute_example, "fpr": compute_fpr, "stimpower": compute_stimpower, "slopes": compute_slopes,
         "simpson": compute_simpson, "ergodic": compute_ergodic, "inertia": compute_inertia, "tipping": compute_tipping}

if __name__ == "__main__":
    CACHE.main(ITEMS)
