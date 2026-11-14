"""Precompute every number in Part 9 of *Psychology, Built* ("Genes and Evolution").

    python -m videos.psychology.psych9.compute            # everything missing (about a minute), into .cache/psych9/
    python -m videos.psychology.psych9.compute --force gwas

Results are cached in ``.cache/psych9/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The models are
Psyche's (``explainer.psychology.psyche.genes``); the published figures they are set beside come from the
Archive.  Every random choice is seeded.

Items:
    coincide   how many of a long list of traits two strangers share by chance
    confound   a world of genes and a world of homes with the same parent-child correlation, and what adoption shows
    loci       a trait as the sum of 1, 2, 5 and 50 loci; children against the average of their parents
    twins      identical and fraternal pairs with planted components; Falconer's estimates
    recover    the twin design repeated 2,000 times at four sample sizes; one study fitted by maximum likelihood
    violate    the same design with each assumption broken in turn
    guess      six traits and their published twin heritabilities
    fields     seed from one sack in two fields; heritability against the spread of environments
    candidate  what a thousand people can detect; a gene that does nothing, analysed flexibly
    gwas       a genome-wide association study of a planted polygenic trait at three sample sizes
    score      a polygenic score in new people; what it says about one person; within and between families
    embryo     the expected gain from choosing the top-scoring of k embryos
    strata     an association made by two groups that differ in a variant's frequency and in the trait
"""

from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.psychology import archive
from explainer.psychology.psyche import genes as G

CACHE = Cache("psych9")
load = CACHE.load

TRUE = dict(a2=0.5, c2=0.2, e2=0.3)  # the components planted in the Pool's twin registry


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def _corr(x, y) -> float:
    return float(np.corrcoef(x, y)[0, 1])


# ---------------------------------------------------------------------------
def compute_coincide() -> dict:
    items, chance = 200, 0.05
    out = G.coincidences(np.full(items, chance), 20_000, rng(900))
    m = out["matches"]
    return {"items": items, "chance": chance, "expected": out["expected"], "hist": np.bincount(m, minlength=26)[:26] / len(m),
            "median": float(np.median(m)), "at_least_5": float((m >= 5).mean()), "at_least_8": float((m >= 8).mean()),
            "pairs": len(m)}


def compute_confound() -> dict:
    """Two worlds in which parents and their children correlate 0.4: in one the cause is genes, in the other the
    home.  Family data cannot tell them apart; a child raised by other parents can."""
    n, g = 100_000, rng(901)
    # the world of genes: additive variance 0.8, no shared home
    a = np.sqrt(0.8) * g.standard_normal(n)
    parent_g = a + np.sqrt(0.2) * g.standard_normal(n)
    child_g = a / 2 + np.sqrt(0.6) * g.standard_normal(n) + np.sqrt(0.2) * g.standard_normal(n)   # other parent + segregation
    adoptive_g = np.sqrt(0.8) * g.standard_normal(n) + np.sqrt(0.2) * g.standard_normal(n)          # an unrelated adult
    # the world of homes: no genes, a home with variance 0.4 that parent and child share
    f = np.sqrt(0.4) * g.standard_normal(n)
    parent_h = f + np.sqrt(0.6) * g.standard_normal(n)
    child_h = f + np.sqrt(0.6) * g.standard_normal(n)
    f2 = np.sqrt(0.4) * g.standard_normal(n)                                                         # the adoptive home
    adoptee_h = f2 + np.sqrt(0.6) * g.standard_normal(n)
    adoptive_h = f2 + np.sqrt(0.6) * g.standard_normal(n)
    k = 500
    return {"genes_parent": parent_g[:k], "genes_child": child_g[:k], "homes_parent": parent_h[:k], "homes_child": child_h[:k],
            "r_genes": _corr(parent_g, child_g), "r_homes": _corr(parent_h, child_h),
            # a child raised from birth by other people: with the parent who gave the genes, with the parent who gave the home
            "genes_biological": _corr(parent_g, child_g), "genes_adoptive": _corr(adoptive_g, child_g),
            "homes_biological": _corr(parent_h, adoptee_h), "homes_adoptive": _corr(adoptive_h, adoptee_h)}


def compute_loci() -> dict:
    out = {}
    for L in (1, 2, 5, 50):
        k, p = G.allele_sum(L)
        out[f"k_{L}"], out[f"p_{L}"] = k, p
    mid, child = G.midparent_offspring(100_000, 0.6, 0.4, rng(902))
    slope, icpt = np.polyfit(mid, child, 1)
    return {**out, "mid": mid[:1200], "child": child[:1200], "slope": float(slope), "intercept": float(icpt), "h2": 0.6,
            "tall_mid": 1.0, "tall_child": float(slope * 1.0 + icpt)}


def compute_twins() -> dict:
    show = G.twin_study(300, 300, **TRUE, rng=rng(903))
    big = G.twin_study(200_000, 200_000, **TRUE, rng=rng(904))
    f = G.falconer(big.r_mz, big.r_dz)
    bm = archive.BOUCHARD_MCGUE_1981.data
    classic = G.falconer(bm["r_mz"], bm["r_dz"])
    return {"mz": show.mz, "dz": show.dz, "r_mz_shown": show.r_mz, "r_dz_shown": show.r_dz, "r_mz": big.r_mz,
            "r_dz": big.r_dz, **{f"est_{k}": v for k, v in f.items()}, **TRUE,
            "classic_r_mz": bm["r_mz"], "classic_r_dz": bm["r_dz"], **{f"classic_{k}": v for k, v in classic.items()}}


def compute_recover() -> dict:
    sizes, reps = (50, 200, 1000, 5000), 2000
    g = rng(905)
    est = np.empty((len(sizes), reps))
    for i, n in enumerate(sizes):
        for r in range(reps):
            d = G.twin_study(n, n, **TRUE, rng=g)
            est[i, r] = 2 * (d.r_mz - d.r_dz)
    edges = np.linspace(-0.6, 1.6, 67)
    out = {"sizes": np.array(sizes), "reps": reps, "edges": edges, "mean": est.mean(axis=1), "sd": est.std(axis=1),
           "lo": np.percentile(est, 2.5, axis=1), "hi": np.percentile(est, 97.5, axis=1),
           "impossible": ((est < 0) | (est > 1)).mean(axis=1),
           "theory_sd": np.array([G.falconer_se(0.7, 0.45, n, n) for n in sizes])}
    for i, n in enumerate(sizes):
        out[f"hist_{n}"] = np.histogram(est[i], edges)[0] / reps
    # one study of 1,000 + 1,000 pairs, chosen by rule: of 101 studies, the one with the median estimate
    g2 = rng(906)
    studies = [G.twin_study(1000, 1000, **TRUE, rng=g2) for _ in range(101)]
    h = np.array([2 * (d.r_mz - d.r_dz) for d in studies])
    d = studies[int(np.argsort(h)[50])]
    fit = G.ace_fit(d)
    g3 = rng(907)
    boot = []
    for _ in range(300):
        i, j = g3.integers(0, 1000, 1000), g3.integers(0, 1000, 1000)
        b = G.ace_fit(G.TwinData(d.mz[i], d.dz[j]))
        boot.append((b["a2"], b["c2"], b["e2"]))
    boot = np.array(boot)
    return {**out, **TRUE, "one_r_mz": d.r_mz, "one_r_dz": d.r_dz, **{f"one_{k}": v for k, v in G.falconer(d.r_mz, d.r_dz).items()},
            "fit_a2": fit["a2"], "fit_c2": fit["c2"], "fit_e2": fit["e2"],
            "fit_lo": np.percentile(boot, 2.5, axis=0), "fit_hi": np.percentile(boot, 97.5, axis=0)}


def compute_violate() -> dict:
    n = 150_000
    cases = [
        ("as assumed", dict(TRUE), {}),
        ("identical twins treated more alike", dict(TRUE), dict(mz_extra=0.4)),
        ("like marries like", dict(TRUE), dict(assort=0.5)),
        ("genes that do not simply add", dict(a2=0.2, c2=0.1, e2=0.3), dict(d2=0.4)),
        ("parents' genes shape the home", dict(TRUE), dict(rge=0.5)),
    ]
    names, h2, c2, e2, truth_g, truth_c = [], [], [], [], [], []
    for k, (name, comp, kw) in enumerate(cases):
        d = G.twin_study(n, n, **comp, **kw, rng=rng(910 + k))
        f = G.falconer(d.r_mz, d.r_dz)
        var = float(np.var(d.dz))
        d2 = kw.get("d2", 0.0)
        # the genetic variance among the children: spouses who resemble each other add to it
        spouse = kw.get("assort", 0.0) * comp["a2"] / (comp["a2"] + d2 + comp["c2"] + comp["e2"])
        genetic = comp["a2"] * (1 + spouse / 2) + d2
        names.append(name)
        h2.append(f["h2"])
        c2.append(f["c2"])
        e2.append(f["e2"])
        truth_g.append(genetic / var)
        truth_c.append(comp["c2"] / var)
    adopt = G.adoption_study(200_000, **TRUE, rng=rng(916))
    placed = G.adoption_study(200_000, **TRUE, placement=0.5, rng=rng(917))
    return {"names": names, "est_h2": np.array(h2), "est_c2": np.array(c2), "est_e2": np.array(e2),
            "truth_genes": np.array(truth_g),
            "truth_home": np.array(truth_c), **{f"adopt_{k}": v for k, v in adopt.items()},
            "placed_mz_apart": placed["mz_apart"], **TRUE}


def compute_guess() -> dict:
    t = archive.HERITABILITY_TABLE.data["traits"]
    return {"names": [x[0] for x in t], "h2": np.array([x[1] for x in t]), "sources": [x[2] for x in t],
            "all_traits": archive.POLDERMAN_2015.data["h2"]}


def compute_fields() -> dict:
    f = G.two_fields(100_000, h2_within=0.9, gap=3.0, rng=rng(920))
    k = 250
    ve = np.linspace(0.05, 4.0, 80)
    hw = archive.HAWORTH_2010.data
    return {"rich": f["rich"][:k], "poor": f["poor"][:k], "h2_rich": f["h2_rich"], "h2_poor": f["h2_poor"], "gap": f["gap"],
            "genetic_gap": f["genetic_gap"], "ve": ve, "h2_curve": 1.0 / (1.0 + ve), "h2_at_small": float(1 / (1 + 0.25)),
            "h2_at_large": float(1 / (1 + 3.0)), "ages": np.array(hw["ages"]), "h2_age": np.array(hw["h2"])}


def compute_candidate() -> dict:
    r2 = archive.RIETVELD_2013.data["r2_per_snp"]
    ns = np.unique(np.round(np.logspace(2, 6, 120)).astype(int))
    g = rng(930)
    out = [G.candidate_gene_study(800, g) for _ in range(2000)]
    planned = np.array([o["planned"] for o in out])
    smallest = np.array([o["smallest"] for o in out])
    return {"r2": r2, "ns": ns, "power": np.array([G.power_for_r2(int(n), r2) for n in ns]),
            "power_gws": np.array([G.power_for_r2(int(n), r2, alpha=5e-8) for n in ns]),
            "power_1000": G.power_for_r2(1000, r2), "need": G.n_for_r2(r2), "need_gws": G.n_for_r2(r2, alpha=5e-8),
            "studies": len(out), "n_each": 800, "analyses": len(out[0]["p"]), "rate_planned": float((planned < 0.05).mean()),
            "rate_any": float((smallest < 0.05).mean()), "smallest": smallest,
            "p_hist": np.histogram(smallest, np.linspace(0, 1, 21))[0] / len(out)}


def _genome():
    X = G.simulate_genotypes(20_000, 2_500, rng(940))
    y, beta = G.polygenic_trait(X, 0.5, 500, rng(941))
    return X, y, beta


def compute_gwas() -> dict:
    X, y, beta = _genome()
    m = X.shape[1]
    line = 0.05 / m
    out = {"m": m, "causal": int((beta != 0).sum()), "h2": 0.5, "line": line, "logline": float(-np.log10(line)),
           "is_causal": beta != 0, "sizes": np.array([2_000, 6_000, 20_000])}
    for n in out["sizes"]:
        res = G.gwas(X[:n], y[:n])
        hit = res["p"] < line
        out[f"logp_{n}"] = np.minimum(-np.log10(np.maximum(res["p"], 1e-300)), 60.0).astype(np.float32)
        out[f"hits_{n}"] = int(hit.sum())
        out[f"false_{n}"] = int((hit & (beta == 0)).sum())
        real = hit & (beta != 0)
        out[f"inflation_{n}"] = float(np.mean(np.abs(res["beta"][real]) / np.abs(beta[real]))) if real.any() else float("nan")
    lee, rv = archive.LEE_2018.data, archive.RIETVELD_2013.data
    return {**out, "real_n": np.array([rv["n"], lee["n"], lee["okbay_n"]]),
            "real_hits": np.array([rv["snps"], lee["snps"], lee["okbay_snps"]])}


def compute_score() -> dict:
    X, y, beta = _genome()
    train, m = 16_000, X.shape[1]
    res = G.gwas(X[:train], y[:train])
    s = G.polygenic_score(X[train:], res["beta"])
    yt = y[train:]
    r2 = _corr(s, yt) ** 2
    order = np.argsort(s)
    deciles = np.array([yt[idx].mean() for idx in np.array_split(order, 10)])
    ns = np.unique(np.round(np.logspace(2.5, 6.5, 100)).astype(int))
    # what a score that predicts 14% of a trait says about one person (the middle of the published 12 to 16%)
    lee = archive.LEE_2018.data
    real = float(np.mean(lee["okbay_r2"]))
    r = np.sqrt(real)
    g = rng(950)
    sc = g.standard_normal(400_000)
    tr = r * sc + np.sqrt(1 - r * r) * g.standard_normal(400_000)
    top, bottom = sc > np.quantile(sc, 0.9), sc < np.quantile(sc, 0.1)
    real_deciles = np.array([tr[idx].mean() for idx in np.array_split(np.argsort(sc), 10)])
    fam = G.sibling_design(400_000, rng(951), direct=0.3, nurture=0.4)
    yg = archive.YENGO_2022.data
    k = 1500
    return {"r2": r2, "expected": G.expected_r2(train, m, 0.5), "train": train, "test": len(yt), "s": s[:k], "y": yt[:k],
            "deciles": deciles, "ns": ns, "curve": np.array([G.expected_r2(int(n), m, 0.5) for n in ns]), "h2": 0.5,
            "real_r2": real, "real_r": float(r), "top_above": float((tr[top] > 0).mean()),
            "bottom_above": float((tr[bottom] > 0).mean()), "top_mean": float(tr[top].mean()),
            "interval": float(1.96 * np.sqrt(1 - real)), "sc": sc[:k], "tr": tr[:k], "real_deciles": real_deciles,
            "is_top": top[:k], "is_bottom": bottom[:k],
            "population": fam["population"], "within": fam["within"], "ratio": fam["ratio"],
            "lee_smaller": lee["within_family_smaller"], "kong": archive.KONG_2018.data["share_of_transmitted"],
            "height_twin": yg["twin_h2"], "height_snp": yg["variance_all_common"]}


def compute_embryo() -> dict:
    """Choosing the top-scoring of k embryos.  The score's accuracy between strangers is the top of the published
    range for cognitive performance; between siblings its effect is the published 40% smaller, so the share of the
    differences it predicts there is 0.6 squared of that."""
    lee, kv = archive.LEE_2018.data, archive.KARAVANI_2019.data
    r2 = float(lee["cognitive_r2"][1])
    direct = r2 * (1 - lee["within_family_smaller"]) ** 2
    ks = np.arange(1, 101)
    out = {"ks": ks, "emax": np.array([G.expected_max(int(k)) for k in ks]), "r2": r2, "r2_direct": direct,
           "gain": np.array([G.embryo_gain(int(k), direct) for k in ks]), "published_k": kv["embryos"],
           "published_gain": kv["iq_points"], "gain_10": G.embryo_gain(10, direct), "gain_100": G.embryo_gain(100, direct),
           "gain_naive_10": G.embryo_gain(10, r2)}
    # one adult, scored: the 95% prediction interval around the predicted IQ, and the chance of being above average
    out["interval_iq"] = float(1.96 * 15 * np.sqrt(1 - r2))
    z90 = stats.norm.isf(0.1)
    out["above_avg_top"] = float(stats.norm.cdf(np.sqrt(r2) * z90 / np.sqrt(1 - r2)))
    return out


def compute_strata() -> dict:
    g = rng(960)
    one = G.stratified_association(4_000, g)
    reps = [G.stratified_association(4_000, g) for _ in range(400)]
    fam = G.sibling_design(400_000, rng(961), direct=0.3, nurture=0.0, strata_gap=1.0, strata_env=1.0)
    mt = archive.MARTIN_2019.data
    return {"pooled_p": one["pooled"], "within_a_p": one["within_a"], "within_b_p": one["within_b"], "r_pooled": one["r_pooled"],
            "rate_pooled": float(np.mean([r["pooled"] < 0.05 for r in reps])),
            "rate_within": float(np.mean([r["within_a"] < 0.05 for r in reps])), "f_a": 0.2, "f_b": 0.6,
            "population": fam["population"], "within": fam["within"],
            "fold_african": mt["fold_lower_african"], "fold_east_asian": mt["fold_lower_east_asian"]}


ITEMS = {
    "coincide": compute_coincide,
    "confound": compute_confound,
    "loci": compute_loci,
    "twins": compute_twins,
    "recover": compute_recover,
    "violate": compute_violate,
    "guess": compute_guess,
    "fields": compute_fields,
    "candidate": compute_candidate,
    "gwas": compute_gwas,
    "score": compute_score,
    "embryo": compute_embryo,
    "strata": compute_strata,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
