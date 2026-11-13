"""Precompute every number in Part 4 of *Psychology, Built* ("The Evidence").

    python -m videos.psychology.psych4.compute            # everything missing (about a minute)
    python -m videos.psychology.psych4.compute --force drawer

Results are cached in ``.cache/psych4/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Published numbers
come from the Archive (``explainer.psychology.archive``, each with its source); every simulated study comes from
the false-positive lab (``explainer.psychology.evidence``) or from the laboratory on the Pool
(``explainer.psychology.lab``), where the truth is known.  Every random choice here is seeded.

Items:
    effects      what d = 0.2, 0.5 and 0.8 look like (overlap, chance of superiority, the equivalent r), beside
                 Bem's 0.22; the p-value of one fixed small effect as the sample grows
    pvalue       one randomized study on the Pool with a real effect of -8 ms, and the distribution of its
                 result under "the treatment does nothing", by 20,000 reshuffles
    power        power against sample size for small, medium and large effects; a literature of 2,000 studies
                 of a real d = 0.4 with 20 people a group: how often it is found, and what the studies that find
                 it report
    forking      the forking-paths exercise: false-positive rates of the plan, of each choice alone and of all
                 sixteen analyses over 3,000 null datasets; one dataset picked by rule, with all sixteen p-values;
                 Simmons, Nelson and Simonsohn's four flexibilities recomputed
    drawer       a thousand laboratories on a true d = 0 and on a true d = 0.2, with a file drawer: what is
                 published, the funnel, the p-curves, and the size of a published effect against sample size
    stopping     a null study tested after every ten people per group: the false-positive rate against the
                 number of looks, and two paths of p-values
    meehl        how often a correlation of 0.05 is declared significant as the sample grows
    rpp          literatures in which a share of the tested hypotheses are true, filtered at p < .05 and then
                 replicated at 90% power: the replication rate and the shrinkage of the effect
    absence      two replications that find nothing, one of 10,000 people and one of 100: the interval, an
                 equivalence test and a Bayes factor for the null in each
    dashboard    the chance of at least one "significant" metric among k metrics on which nothing changed
"""

from __future__ import annotations

import math

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.psychology import archive, lab
from explainer.psychology import evidence as E
from explainer.psychology.pool import Pool

CACHE = Cache("psych4")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
def compute_effects() -> dict:
    bem = archive.BEM_2011.data["mean_d"]
    ds = [0.2, 0.5, 0.8]
    rows = {f"{d:.1f}": {"d": d, "overlap": E.overlap(d), "superiority": E.superiority(d), "r": E.d_to_r(d),
                         "n_for_80": E.n_for(d)} for d in ds}
    ns = [20, 50, 100, 500, 2000, 10_000, 100_000]
    small = 0.05
    out = {"rows": rows, "bem": {"d": bem, "overlap": E.overlap(bem), "superiority": E.superiority(bem),
                                 "r": E.d_to_r(bem), "n_for_80": E.n_for(bem)},
           "small_d": small, "ns": ns, "p_small": [E.p_for(small, n) for n in ns],
           "n_sig_small": int(math.ceil(2 * (E.Z975 / small) ** 2)),
           "x": np.linspace(-3.5, 4.5, 241)}
    out["pdf"] = stats.norm.pdf(out["x"])
    assert abs(rows["0.5"]["superiority"] - 0.638) < 0.002 and abs(rows["0.8"]["overlap"] - 0.689) < 0.002
    return out


def compute_pvalue() -> dict:
    pool = Pool()
    L = lab.Lab(pool)
    n, effect = 200, -8.0
    # the median study of 101 by its estimate, as in Part 2: an example is picked by rule, never by its result
    ests = [L.randomized(n=n, effect=effect, study=s).effect for s in range(101)]
    study = int(np.argsort(ests)[50])
    ids = pool.sample(n, seed=L.seed * 7919 + study)
    g = lab.randomize(n, 2, L._rng(1, study))
    y = L._rt(ids, 0, 100 + study, shift=effect * g)
    rt = lab.randomization_test(y, g, n_perm=20_000, rng=rng(401))
    null = rt["null"]
    edges = np.linspace(-14, 14, 57)
    dens = np.histogram(null, bins=edges, density=True)[0]
    out = {"n": n, "effect": effect, "observed": rt["observed"], "p": rt["p"], "edges": edges, "density": dens,
           "null_sd": float(null.std()), "shuffles": 20_000,
           "as_extreme": int(np.sum(np.abs(null) >= abs(rt["observed"])))}
    assert 0.001 < out["p"] < 0.05
    return out


def compute_power() -> dict:
    ns = np.arange(5, 401)
    curves = {f"{d:.1f}": np.array([E.power(d, int(n)) for n in ns]) for d in (0.2, 0.5, 0.8)}
    d_true, n = 0.4, 20
    lit = E.literature(2000, d_true, n, rng(411))
    sig = lit["significant"]
    edges = np.linspace(-0.8, 1.6, 49)
    out = {"ns": ns, **{f"curve_{k}": v for k, v in curves.items()}, "d_true": d_true, "n": n,
           "power": E.power(d_true, n), "found": float(sig.mean()), "studies": 2000,
           "mean_all": float(lit["est"].mean()), "mean_significant": float(lit["est"][sig].mean()),
           "smallest_significant": float(E.Z975 * math.sqrt(2 / n)), "n_for_80": E.n_for(d_true),
           "edges": edges, "hist_all": np.histogram(lit["est"], bins=edges)[0].astype(float),
           "hist_sig": np.histogram(lit["est"][sig], bins=edges)[0].astype(float),
           "cohen": dict(archive.COHEN_1962.data)}
    assert abs(out["found"] - out["power"]) < 0.03 and out["mean_significant"] > 1.8 * d_true
    return out


def compute_forking() -> dict:
    rates = E.any_significant(range(3000))
    # the dataset shown: the first, in order, whose planned analysis fails and some other analysis "works"
    seed = next(s for s in range(200) if E.forks(s)["planned"][0] > 0.10 and E.forks(s)["best_p"] < 0.05)
    f = E.forks(seed)
    keys = sorted(f["table"])
    sns = E.flexibility(3000, rng(421))
    out = {"rates": rates, "seed": seed, "planned_p": f["planned"][0], "planned_d": f["planned"][1],
           "best": list(f["best"]), "best_p": f["best_p"], "best_d": f["table"][f["best"]][1],
           "keys": [list(k) for k in keys], "ps": [f["table"][k][0] for k in keys],
           "significant_paths": int(sum(f["table"][k][0] < 0.05 for k in keys)),
           "forks": [[name, list(opts)] for name, opts in E.FORKS], "sns": sns,
           "sns_published": archive.SIMMONS_2011.data["combined"]}
    assert abs(sns["ABCD"] - out["sns_published"]) < 0.04 and 0.03 < rates["planned"] < 0.07
    return out


def compute_drawer() -> dict:
    k = 1000
    g = rng(431)
    n = g.integers(10, 101, k)
    out = {"k": k, "n_lo": 10, "n_hi": 100}
    for name, d in (("null", 0.0), ("small", 0.2)):
        lit = E.literature(k, d, n, rng(432 + int(10 * d)))
        pub = lit["published"]
        out[name] = {"d": d, "published": int(pub.sum()), "mean_published": float(lit["est"][pub].mean()),
                     "mean_all": float(lit["est"].mean()), "pcurve": E.pcurve(lit["p"][pub]).tolist()}
        out[f"{name}_est"], out[f"{name}_se"], out[f"{name}_pub"] = lit["est"], lit["se"], pub
    # the winner's curse: the mean published estimate of a true 0.2, by sample size
    ns = np.array([10, 15, 20, 30, 50, 80, 120, 200, 400])
    curse = []
    for m in ns:
        lit = E.literature(40_000, 0.2, int(m), rng(440 + int(m)))
        curse.append(float(lit["est"][lit["published"]].mean()))
    out.update(curse_n=ns, curse=np.array(curse), curse_d=0.2)
    # p-curves need many studies to be smooth: 60,000 laboratories each, 30 people a group
    big = {"nothing": E.literature(60_000, 0.0, 30, rng(451)), "real": E.literature(60_000, 0.5, 30, rng(452)),
           "pushed": E.literature(60_000, 0.0, 30, rng(453), hack=0.2)}
    out["pcurves"] = {name: E.pcurve(lit["p"][lit["published"]]).tolist() for name, lit in big.items()}
    assert out["null"]["mean_published"] > 0.4 and abs(out["null"]["mean_all"]) < 0.03
    assert out["small"]["mean_published"] > 2 * 0.2 and curse[0] > curse[-1] > 0.2
    return out


def compute_stopping() -> dict:
    looks = [1, 2, 3, 5, 10, 20]
    rates = [E.peeking(k, batch=10, reps=20_000, rng=rng(450 + k))["rate"] for k in looks]
    one = E.peeking(10, batch=10, reps=4000, rng=rng(461))
    out = {"looks": looks, "rates": rates, "batch": 10, "path_n": one["n"], "path_typical": one["example"],
           "path_lucky": one["lucky"], "rate_10": rates[looks.index(10)]}
    assert abs(rates[0] - 0.05) < 0.006 and rates[-1] > rates[-2] > rates[1]
    return out


def compute_meehl() -> dict:
    r = 0.05
    ns = np.array([50, 100, 200, 500, 1000, 2000, 5000, 10_000, 20_000, 50_000, 100_000])
    z = np.arctanh(r) * np.sqrt(ns - 3)
    sig = stats.norm.sf(E.Z975 - z) + stats.norm.cdf(-E.Z975 - z)
    n80 = int(math.ceil(((E.Z975 + stats.norm.ppf(0.8)) / math.atanh(r)) ** 2 + 3))
    return {"r": r, "ns": ns, "significant": sig, "n_for_80": n80, "variance_explained": r * r}


def compute_rpp() -> dict:
    """A literature in which a share ``prior`` of the tested hypotheses are true with effect ``d`` and the rest
    are null; 30 people a group; only significant results published; each then replicated with 90% power for
    the effect the original reported."""
    osc = archive.OSC_2015.data
    k, n = 60_000, 30
    grid = []
    for prior in (0.1, 0.25, 0.5):
        for d in (0.3, 0.4, 0.5):
            g = rng(470 + int(100 * prior) + int(10 * d))
            true = g.random(k) < prior
            truth = np.where(true, d, 0.0)
            se = math.sqrt(2 / n)
            est = truth + se * g.standard_normal(k)
            sig = est / se > E.Z975
            lit = {"est": est, "se": np.full(k, se), "published": sig, "significant": sig, "truth": truth, "d": d}
            rep = E.replicate(lit, g)
            grid.append({"prior": prior, "d": d, "true_share_published": float(true[sig].mean()),
                         "rate": rep["rate"], "ratio": rep["ratio"]})
    near = min(grid, key=lambda r_: abs(r_["rate"] - osc["replication_significant"]) + abs(r_["ratio"] - osc["effect_ratio"]))
    return {"grid": grid, "n": n, "nearest": near, "osc": {k_: osc[k_] for k_ in (
        "studies", "original_significant", "replication_significant", "original_in_replication_ci", "rated_replicated",
        "effect_ratio")}}


def compute_absence() -> dict:
    # two replications that both "find nothing": 10,000 people (two groups; se = 2 / sqrt(N)) and 100 people
    est, se, bound = 0.01, 0.02, 0.1
    t = E.tost(est, se, bound)
    return {"est": est, "se": se, "n_large": 10_000, "n_small": 100, "ci95": [est - E.Z975 * se, est + E.Z975 * se], "bound": bound, "tost_p": t["p"],
            "p_null": float(2 * stats.norm.sf(est / se)), "bf01": E.bf01(est, se, archive.BEM_2011.data["mean_d"]),
            "prior_sd": archive.BEM_2011.data["mean_d"],
            "small_study": {"se": 0.2, "ci95": [est - E.Z975 * 0.2, est + E.Z975 * 0.2],
                            "tost_p": E.tost(est, 0.2, bound)["p"], "bf01": E.bf01(est, 0.2, archive.BEM_2011.data["mean_d"])}}


def compute_dashboard() -> dict:
    ks = np.arange(1, 41)
    return {"k": ks, "any": 1 - 0.95 ** ks, "at_20": float(1 - 0.95 ** 20), "at_5": float(1 - 0.95 ** 5),
            "bonferroni_20": 0.05 / 20}


ITEMS = {
    "effects": compute_effects,
    "pvalue": compute_pvalue,
    "power": compute_power,
    "forking": compute_forking,
    "drawer": compute_drawer,
    "stopping": compute_stopping,
    "meehl": compute_meehl,
    "rpp": compute_rpp,
    "absence": compute_absence,
    "dashboard": compute_dashboard,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
