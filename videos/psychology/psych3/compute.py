"""Precompute every number in Part 3 of *Psychology, Built* ("The Measure").

    python -m videos.psychology.psych3.compute            # everything missing (under a minute)
    python -m videos.psychology.psych3.compute --force longer

Results are cached in ``.cache/psych3/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Historical and
published numbers come from the Archive (``explainer.psychology.archive``, each with its source); scores come
from the Pool (seed 1850), where a person's true value is stored, so every estimate can be set beside the truth;
the estimators are those of ``explainer.psychology.measure``.  Every random choice here is seeded.

Items:
    scales       two groups' answers to one five-point item, in a case where every increasing recoding of the
                 five categories keeps the order of the two means and in a case where a recoding reverses it;
                 how much a ten-item sum score changes under such recodings
    conjoint     a table of chances of a correct answer for three people and three items that has an additive
                 scale behind it, and one that has not: independence and double cancellation, checked
    truescore    one person answering the same ten-item scale 300 times; in 20,000 people, the variance of the
                 scores split into true and error; two parallel forms
    attenuation  two traits that correlate 0.84, seen through scales of 2 to 40 items: the observed correlation,
                 Spearman's corrected value, and what the correction does in studies of 60 people
    longer       reliability against test length beside the Spearman-Brown curve; alpha when its assumptions
                 hold, with unequal items, and for a test of two unrelated traits; a mood on the day (alpha
                 against retest); two raters and a rare diagnosis (agreement against kappa)
    validity     three traits, each measured by three methods that leave their own mark: the multitrait-
                 multimethod matrix and its three kinds of correlation, with and without the planted method
                 variance
    jingle       grit and conscientiousness through twelve-item scales: their correlation beside the
                 correlation of two forms of the same conscientiousness scale
    latent       six variables that all push one another, and six that share one hidden cause: the two
                 correlation matrices
    paradox      the conflict task: how often a study of 20 people finds the effect, the retest reliability of
                 a person's effect against the number of trials, and the trade between the two as people differ
                 more
"""

from __future__ import annotations

import math

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.psychology import archive
from explainer.psychology import measure as M
from explainer.psychology import pool as pool_mod
from explainer.psychology.pool import Pool

CACHE = Cache("psych3")
load = CACHE.load

LOADING = 0.6  # every item of the film's scales: answer = 0.6 trait + error, so one item's reliability is 0.36
N_BIG = 20_000  # people, where the film wants the population value


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def shares(answers, points: int = 5) -> list:
    return [float(np.mean(answers == c)) for c in range(1, points + 1)]


# ---------------------------------------------------------------------------
def compute_scales() -> dict:
    pool = Pool()
    ids = pool.sample(N_BIG, seed=301)
    z = pool.extravert[ids]
    item = pool.items("extravert", ids, 1, seed=1, loading=0.8)[:, 0]
    # case 1: one group answers higher throughout (the upper and lower halves of the trait)
    hi, lo = item[z > np.median(z)], item[z <= np.median(z)]
    # case 2: a group in the middle against a group at the two ends (the middle half of the trait against the
    # outer quarters), which has slightly the higher mean on equally spaced categories
    q1, q3 = np.quantile(z, [0.25, 0.75])
    middle, ends = item[(z > q1) & (z < q3)], item[(z <= q1) | (z >= q3 - 0.12)]
    g = rng(302)
    out = {}
    for name, a, b in (("shifted", hi, lo), ("crossed", middle, ends)):
        pa, pb = shares(a), shares(b)
        v = np.arange(1, 6.0)
        out[name] = {"pa": pa, "pb": pb, "mean_a": float(np.dot(pa, v)), "mean_b": float(np.dot(pb, v)),
                     "can_flip": M.order_can_flip(pa, pb), "flip_share": M.flip_share(pa, pb, 20_000, g)}
    assert not out["shifted"]["can_flip"] and out["shifted"]["flip_share"] == 0
    c = out["crossed"]
    assert c["can_flip"] and c["mean_b"] > c["mean_a"] and 0.05 < c["flip_share"] < 0.95
    # one explicit recoding that reverses the crossed case: the same five answers, with "strongly disagree"
    # counted as further from "disagree" than the other steps
    stretched = [-1.0, 2.0, 3.0, 4.0, 5.0]
    c["stretched"] = stretched
    c["stretched_a"], c["stretched_b"] = float(np.dot(c["pa"], stretched)), float(np.dot(c["pb"], stretched))
    assert c["stretched_a"] > c["stretched_b"]
    # a ten-item scale: the sum under equal spacing against the sum under 2,000 random increasing recodings
    ten = pool.items("extravert", ids, 10, seed=2, loading=LOADING)
    plain = ten.sum(axis=1)
    rs, with_truth = [], []
    for _ in range(2000):
        code = M.recode("ordinal", np.arange(1, 6.0), g)
        s = code[ten - 1].sum(axis=1)
        rs.append(np.corrcoef(plain, s)[0, 1])
        with_truth.append(np.corrcoef(z, s)[0, 1])
    return {**out, "n": N_BIG, "sum_r_median": float(np.median(rs)), "sum_r_p05": float(np.quantile(rs, 0.05)),
            "truth_r_plain": float(np.corrcoef(z, plain)[0, 1]), "truth_r_p05": float(np.quantile(with_truth, 0.05)),
            "scales": {k: list(v) for k, v in archive.STEVENS_1946.data["scales"].items()}}


def compute_conjoint() -> dict:
    """Three people of abilities -1, 0, 1.2 meet three items of difficulties -0.8, 0.1, 1.0.  If the chance of
    a correct answer depends only on ability minus difficulty, the nine chances can be ordered, the order is the
    same in every row and column, and double cancellation holds: an additive scale exists, and it is found from
    the order alone.  If items also differ in how sharply they discriminate, the columns cross and it does not."""
    ability, difficulty = np.array([-1.0, 0.0, 1.2]), np.array([-0.8, 0.1, 1.0])
    additive = 1 / (1 + np.exp(-(ability[:, None] - difficulty[None, :])))
    slopes = np.array([0.4, 1.0, 2.6])  # the items no longer discriminate equally
    crossing = 1 / (1 + np.exp(-slopes[None, :] * (ability[:, None] - difficulty[None, :])))
    out = {"ability": ability.tolist(), "difficulty": difficulty.tolist(), "additive": additive.tolist(),
           "crossing": crossing.tolist(),
           "additive_ok": [M.independence(additive), M.double_cancellation(additive)],
           "crossing_ok": [M.independence(crossing), M.double_cancellation(crossing)]}
    assert out["additive_ok"] == [True, True] and not all(out["crossing_ok"])
    return out


def compute_truescore() -> dict:
    pool = Pool()
    k = 10
    ids = pool.sample(N_BIG, seed=311)
    truth = pool.conscientious[ids]
    a, b = pool.scale("conscientious", ids, k, seed=11), pool.scale("conscientious", ids, k, seed=12)
    rel = M.reliability(truth, a)
    # 4,000 of them on 60 occasions: a person's true score is their mean over occasions, the error what is left
    occasions = np.array([pool.scale("conscientious", ids[:4000], k, seed=100 + j) for j in range(60)])
    var_x = float(occasions.var(axis=1).mean())
    var_e = float(occasions.var(axis=0, ddof=1).mean())
    var_t = var_x - var_e
    # one person, the one whose trait is nearest to +0.5, answering 300 times
    who = ids[np.argmin(np.abs(truth - 0.5))]
    retakes = np.array([pool.scale("conscientious", [who], k, seed=1000 + j)[0] for j in range(300)])
    show = rng(312).choice(N_BIG, 500, replace=False)
    out = {"k": k, "n": N_BIG, "reliability": rel, "parallel_r": float(np.corrcoef(a, b)[0, 1]),
           "var_x": var_x, "var_t": var_t, "var_e": var_e, "sd_x": float(a.std()),
           "sem": M.sem(float(a.std()), rel), "person_true": float(retakes.mean()), "person_sd": float(retakes.std()),
           "person_min": float(retakes.min()), "person_max": float(retakes.max()),
           "retakes": retakes, "form_a": a[show], "form_b": b[show], "mean": float(a.mean())}
    assert abs(out["parallel_r"] - rel) < 0.01 and abs(var_t / var_x - rel) < 0.02
    assert abs(out["person_sd"] - out["sem"]) < 0.5
    return out


def compute_attenuation() -> dict:
    pool = Pool()
    ids = pool.sample(N_BIG, seed=321)
    true_r = float(np.corrcoef(pool.conscientious[ids], pool.grit[ids])[0, 1])
    lengths = [2, 4, 6, 10, 15, 20, 30, 40]
    observed, rels, corrected = [], [], []
    for k in lengths:
        x = pool.scale("conscientious", ids, k, seed=20 + k)
        y = pool.scale("grit", ids, k, seed=60 + k)
        rx = float(np.corrcoef(x, pool.scale("conscientious", ids, k, seed=120 + k))[0, 1])
        ry = float(np.corrcoef(y, pool.scale("grit", ids, k, seed=160 + k))[0, 1])
        r = float(np.corrcoef(x, y)[0, 1])
        observed.append(r), rels.append((rx + ry) / 2), corrected.append(M.disattenuate(r, rx, ry))
    assert max(abs(c - true_r) for c in corrected) < 0.02
    # studies of 60 people with six-item scales: the correction is right on average and noisy in one study
    k, n, studies = 6, 60, 4000
    g = rng(322)
    raw, fixed = [], []
    for s in range(studies):
        sub = g.choice(ids, n, replace=False)
        ix, iy = pool.items("conscientious", sub, k, seed=5000 + s), pool.items("grit", sub, k, seed=9000 + s)
        r = np.corrcoef(ix.sum(axis=1), iy.sum(axis=1))[0, 1]
        raw.append(r), fixed.append(M.disattenuate(r, M.cronbach_alpha(ix), M.cronbach_alpha(iy)))
    raw, fixed = np.array(raw), np.array(fixed)
    return {"true_r": true_r, "lengths": lengths, "observed": observed, "reliabilities": rels,
            "corrected": corrected, "n": N_BIG, "study_k": k, "study_n": n, "studies": studies,
            "raw_median": float(np.median(raw)), "fixed_median": float(np.median(fixed)),
            "raw_lo": float(np.quantile(raw, 0.025)), "raw_hi": float(np.quantile(raw, 0.975)),
            "fixed_lo": float(np.quantile(fixed, 0.025)), "fixed_hi": float(np.quantile(fixed, 0.975)),
            "above_one": float(np.mean(fixed > 1)), "raw": raw, "fixed": fixed,
            "six_item_reliability": rels[lengths.index(6)]}


def compute_longer() -> dict:
    pool = Pool()
    ids = pool.sample(N_BIG, seed=331)
    truth = pool.conscientious[ids]
    lengths = [1, 2, 4, 6, 10, 15, 20, 30, 40]
    one = M.reliability(truth, pool.scale("conscientious", ids, 1, seed=31))  # one five-point item
    simulated = [M.reliability(truth, pool.scale("conscientious", ids, k, seed=31 + k)) for k in lengths]
    curve_k = np.arange(1, 41)
    curve = np.array([M.spearman_brown(one, k) for k in curve_k])
    assert max(abs(s - M.spearman_brown(one, k)) for s, k in zip(simulated, lengths)) < 0.012
    # alpha, three ways
    equal = pool.items("conscientious", ids, 10, seed=41)
    unequal_loadings = np.linspace(0.3, 0.85, 10)
    unequal = pool.items("conscientious", ids, 10, seed=42, loading=unequal_loadings)
    two = np.hstack([pool.items("conscientious", ids, 10, seed=43), pool.items("extravert", ids, 10, seed=44)])
    halves_r = float(np.corrcoef(two[:, :10].sum(axis=1), two[:, 10:].sum(axis=1))[0, 1])
    alpha = {
        "equal": {"alpha": M.cronbach_alpha(equal), "truth": M.reliability(truth, equal.sum(axis=1))},
        "unequal": {"alpha": M.cronbach_alpha(unequal), "truth": M.reliability(truth, unequal.sum(axis=1))},
        "two_traits": {"alpha": M.cronbach_alpha(two), "halves_r": halves_r, "items": 20},
    }
    assert abs(alpha["equal"]["alpha"] - alpha["equal"]["truth"]) < 0.01
    assert alpha["unequal"]["alpha"] < alpha["unequal"]["truth"] and alpha["two_traits"]["alpha"] > 0.7
    # a mood on the day: every item of an occasion shares it, so alpha counts it as true score and a retest
    # a month later does not
    g = rng(332)
    mood_loading, k = 0.4, 10
    rest = math.sqrt(1 - LOADING ** 2 - mood_loading ** 2)

    def occasion():
        y = LOADING * truth[:, None] + mood_loading * g.standard_normal((len(ids), 1)) + rest * g.standard_normal((len(ids), k))
        return 1 + np.searchsorted(np.asarray(pool_mod.CUTS[5]), y)

    first, second = occasion(), occasion()
    mood = {"alpha": M.cronbach_alpha(first), "retest": float(np.corrcoef(first.sum(axis=1), second.sum(axis=1))[0, 1]),
            "truth": M.reliability(truth, first.sum(axis=1)), "mood_loading": mood_loading}
    assert mood["alpha"] > mood["retest"] + 0.1 and abs(mood["retest"] - mood["truth"]) < 0.02
    # two raters, a diagnosis present in 1 case in 20: each misses 4 in 10 and raises a false alarm in 1 of 20
    cases, prevalence, hit, false_alarm = 20_000, 0.05, 0.6, 0.05
    present = g.random(cases) < prevalence
    rate = lambda: np.where(present, g.random(cases) < hit, g.random(cases) < false_alarm)  # noqa: E731
    r1, r2 = rate(), rate()
    kappa = {"prevalence": prevalence, "hit": hit, "false_alarm": false_alarm, "agreement": M.agreement(r1, r2),
             "kappa": M.cohen_kappa(r1, r2), "both_yes": float(np.mean(r1 & r2)), "both_no": float(np.mean(~r1 & ~r2)),
             "split": float(np.mean(r1 != r2))}
    assert kappa["agreement"] > 0.85 and kappa["kappa"] < 0.3
    return {"one_item": one, "lengths": lengths, "simulated": simulated, "curve_k": curve_k, "curve": curve,
            "for_80": M.length_for(one, 0.8), "for_90": M.length_for(one, 0.9), "alpha": alpha, "mood": mood,
            "kappa": kappa, "unequal_loadings": unequal_loadings.tolist(), "n": N_BIG}


def compute_validity() -> dict:
    pool = Pool()
    ids = pool.sample(N_BIG, seed=341)
    k, method_loading = 8, 0.45

    def scores(ml):
        return {(t, m): pool.scale(t, ids, k, seed=400 + 10 * i + j, method=m, method_loading=ml)
                for i, t in enumerate(pool_mod.TRAITS) for j, m in enumerate(pool_mod.METHODS)}

    planted, clean = M.mtmm(scores(method_loading)), M.mtmm(scores(0.0))
    assert planted["convergent"] > planted["same_method"] > planted["neither"] + 0.05
    assert abs(clean["same_method"] - clean["neither"]) < 0.02
    keep = ("convergent", "same_method", "neither")
    return {"traits": list(pool_mod.TRAITS), "methods": list(pool_mod.METHODS), "k": k,
            "method_loading": method_loading, "r": planted["r"], "r_clean": clean["r"],
            "planted": {key: planted[key] for key in keep}, "clean": {key: clean[key] for key in keep},
            "labels": [list(x) for x in planted["labels"]], "n": N_BIG,
            "true_r": {f"{a}-{b}": r for (a, b), r in pool_mod.TRAIT_R.items()}}


def compute_jingle() -> dict:
    pool = Pool()
    ids = pool.sample(N_BIG, seed=351)
    k = 12
    c1, c2 = pool.scale("conscientious", ids, k, seed=51), pool.scale("conscientious", ids, k, seed=52)
    grit = pool.scale("grit", ids, k, seed=53)
    g2 = pool.scale("grit", ids, k, seed=54)
    r_forms, r_grit = float(np.corrcoef(c1, c2)[0, 1]), float(np.corrcoef(c1, grit)[0, 1])
    rel_g = float(np.corrcoef(grit, g2)[0, 1])
    corrected = M.disattenuate(r_grit, r_forms, rel_g)
    cr = archive.CREDE_2017.data
    assert abs(corrected - cr["grit_conscientiousness"]["rho"]) < 0.02
    show = rng(352).choice(N_BIG, 500, replace=False)
    return {"k": k, "r_forms": r_forms, "r_grit": r_grit, "reliability_grit": rel_g, "corrected": corrected,
            "rho": cr["grit_conscientiousness"]["rho"], "k_samples": cr["grit_conscientiousness"]["k"],
            "n_people": cr["grit_conscientiousness"]["n"], "rho_performance": cr["grit_academic_performance"]["rho"],
            "shared": cr["grit_conscientiousness"]["rho"] ** 2,
            "c1": c1[show], "c2": c2[show], "grit": grit[show], "n": N_BIG}


def compute_latent() -> dict:
    p, b = 6, 0.12
    net = M.mutualism(p, b)
    fit = M.one_factor(net)
    factor = np.outer(fit["loadings"], fit["loadings"])
    np.fill_diagonal(factor, 1.0)
    out = {"p": p, "b": b, "r": float(net[0, 1]), "loading": float(fit["loadings"][0]),
           "largest_difference": float(np.abs(net - factor).max()), "network": net, "factor": factor}
    assert out["largest_difference"] < 1e-6
    return out


def compute_paradox() -> dict:
    pool = Pool()
    h = archive.HEDGE_2018.data
    ids = pool.sample(N_BIG, seed=361)
    trials = [20, 40, 80, 120, 240, 480]
    cost_icc, level_icc = [], []
    for nt in trials:
        s1, s2 = pool.conflict_task(ids, nt, seed=70 + nt), pool.conflict_task(ids, nt, seed=700 + nt)
        cost_icc.append(M.icc(s1["cost"], s2["cost"])), level_icc.append(M.icc(s1["congruent"], s2["congruent"]))
    nt = 120
    s1 = pool.conflict_task(ids, nt, seed=70 + nt)
    # the experimentalist's question: does a study of 20 people find the effect?
    g, n, studies = rng(362), 20, 2000
    found, ts = 0, []
    for s in range(studies):
        sub = g.choice(ids, n, replace=False)
        cost = pool.conflict_task(sub, nt, seed=20_000 + s)["cost"]
        t = cost.mean() / (cost.std(ddof=1) / math.sqrt(n))
        ts.append(t)
        found += stats.t.sf(t, n - 1) * 2 < 0.05 and t > 0
    # the trade: with the same task and the same trial noise, let people differ more or less in their effect
    sds = np.linspace(2, 60, 59)
    err = 2 * pool_mod.CONFLICT_TRIAL_SD ** 2 / nt
    trade_rel = sds ** 2 / (sds ** 2 + err)
    trade_dz = pool_mod.CONFLICT_MEAN / np.sqrt(sds ** 2 + err)
    i = trials.index(nt)
    show = rng(363).choice(N_BIG, 400, replace=False)
    s2 = pool.conflict_task(ids, nt, seed=700 + nt)
    out = {"n_trials": nt, "trials": trials, "cost_icc": cost_icc, "level_icc": level_icc,
           "mean_cost": float(s1["cost"].mean()), "sd_cost_true": float(pool.conflict[ids].std()),
           "sd_cost_observed": float(s1["cost"].std()), "sd_level": float(s1["congruent"].std()),
           "dz": float(s1["cost"].mean() / s1["cost"].std()), "study_n": n, "studies": studies,
           "found": found / studies, "t_median": float(np.median(ts)), "icc_at": cost_icc[i],
           "level_icc_at": level_icc[i], "trade_sd": sds, "trade_rel": trade_rel, "trade_dz": trade_dz,
           "planted_sd": pool_mod.CONFLICT_SD, "cost_1": s1["cost"][show], "cost_2": s2["cost"][show],
           "level_1": s1["congruent"][show], "level_2": s2["congruent"][show],
           "hedge": {"stroop": list(h["stroop_rt_cost"]), "flanker": h["flanker_rt_cost"],
                     "flanker_components": list(h["flanker_components"]), "range": list(h["icc_range"]),
                     "weeks": h["retest_weeks"], "tasks": len(h["tasks"])}}
    assert out["found"] == 1.0 and 0.55 < out["icc_at"] < 0.7 and out["level_icc_at"] > 0.9
    return out


ITEMS = {
    "scales": compute_scales,
    "conjoint": compute_conjoint,
    "truescore": compute_truescore,
    "attenuation": compute_attenuation,
    "longer": compute_longer,
    "validity": compute_validity,
    "jingle": compute_jingle,
    "latent": compute_latent,
    "paradox": compute_paradox,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
