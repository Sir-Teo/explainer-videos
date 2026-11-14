"""Precompute every number in Part 12 of *Psychology, Built* ("Signal and Noise").

    python -m videos.psychology.psych12.compute            # everything missing (about a minute), into .cache/psych12/
    python -m videos.psychology.psych12.compute --force roc

Results are cached in ``.cache/psych12/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The observer is
Psyche's (``explainer.psychology.psyche.sdt``): evidence that is normal on noise trials and shifted (and sometimes
wider) on signal trials, and a criterion.  Every simulated study the film shows alone is picked by rule (the median
of many), never by its result.

Items:
    watch       a two-hour watch in 15-minute blocks, by an observer whose criterion creeps up and by one whose
                sensitivity falls: the same falling hit rate, different false alarms
    payoffs     one observer under five payoff schemes: the "threshold" moves, d' does not
    model       the two distributions, a criterion, and d' and c from a pair of rates
    roc         ROCs for several d'; the area under them; a rating-scale study and its points
    onyou       the in-film recognition test: twelve old and twelve new words; d' and c for any count
    ideal       the likelihood ratio; optimal criteria for base rates and payoffs; expected value against criterion
    fitroc      a rating study from an unequal-variance observer fitted with equal and unequal variances
    afc         two-interval and m-alternative choice: d' from percent correct, the root-two factor
    rivals      high-threshold, signal-detection and dual-process ROCs fitted to the same rating data
    baserates   the mammogram in natural frequencies; the share of alarms that are real against prevalence
    prevalence  misses against prevalence for an observer who moves its criterion; the published 2005 misses
    classifier  a spam filter's scores: ROC and precision-recall at a common and a rare base rate
    confidence  confidence about one's own answers: a type-2 ROC for an observer whose confidence is noisier
"""

from __future__ import annotations

import math

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.psychology import archive
from explainer.psychology.psyche import sdt as D

CACHE = Cache("psych12")
load = CACHE.load

Phi, Z = stats.norm.cdf, stats.norm.ppf


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def _median_pick(values) -> int:
    v = np.asarray(values, float)
    return int(np.argsort(v)[len(v) // 2])


# ---------------------------------------------------------------------------
def compute_watch() -> dict:
    """Eight blocks of 15 minutes; 25 signals and 225 blanks a block.  Two observers start alike (d' 2.0,
    c 0.3).  A: the criterion rises by 0.12 a block.  B: d' falls by 0.24 a block, criterion fixed in c.  Their hit
    rates fall by nearly the same amount; their false alarms go opposite ways."""
    blocks = np.arange(8)
    out = {"minutes": (blocks + 1) * 15, "n_signal": 25, "n_noise": 225}
    for name, d, c in (("criterion", np.full(8, 2.0), 0.3 + 0.12 * blocks),
                       ("sensitivity", 2.0 - 0.24 * blocks, np.full(8, 0.3))):
        k = d / 2 + c  # absolute criterion
        hit, fa = D.rates(d, k)
        out[f"{name}_d"], out[f"{name}_c"], out[f"{name}_hit"], out[f"{name}_fa"] = d, c, hit, fa
    return out


def compute_payoffs() -> dict:
    d = 1.5
    schemes = [  # (name, p_signal, payoffs)
        ("misses cost a lot", 0.5, {"c_miss": 4.0}),
        ("misses cost more", 0.5, {"c_miss": 1.5}),
        ("even", 0.5, {}),
        ("false alarms cost more", 0.5, {"c_fa": 1.5}),
        ("false alarms cost a lot", 0.5, {"c_fa": 4.0}),
    ]
    ks = np.array([D.optimal_criterion(d, p, **pay) for _, p, pay in schemes])
    hit, fa = D.rates(d, ks)
    return {"d": d, "names": [s[0] for s in schemes], "criteria": ks, "hit": hit, "fa": fa,
            "dprime": np.array([D.dprime(h, f) for h, f in zip(hit, fa)]),
            "c": np.array([D.criterion_c(h, f) for h, f in zip(hit, fa)])}


def compute_model() -> dict:
    d, k = 1.5, 1.0
    hit, fa = D.rates(d, k)
    x = np.linspace(-4, 5.5, 400)
    return {"d": d, "k": k, "hit": float(hit), "fa": float(fa), "z_hit": float(Z(hit)), "z_fa": float(Z(fa)),
            "dprime": D.dprime(hit, fa), "c": D.criterion_c(hit, fa), "beta": D.beta(hit, fa),
            "x": x, "noise": stats.norm.pdf(x), "signal": stats.norm.pdf(x, d)}


def compute_roc() -> dict:
    ds = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 3.0])
    fa_grid = np.linspace(1e-4, 1 - 1e-4, 300)
    curves = np.array([1 - Phi(Z(1 - fa_grid) - d) for d in ds])
    obs = D.Observer(d=1.5)
    crit = [-0.3, 0.3, 0.9, 1.5, 2.1]
    studies = [D.simulate_ratings(obs, crit, 150, 150, rng(100 + j)) for j in range(101)]
    aucs = [np.trapezoid(*reversed(_pts(cs, cn))) for cs, cn in studies]
    j = _median_pick(aucs)
    cs, cn = studies[j]
    h, f = D.rating_rates(cs, cn)
    return {"ds": ds, "fa_grid": fa_grid, "curves": curves, "aucs": np.array([D.auc(d) for d in ds]),
            "counts_signal": cs, "counts_noise": cn, "hit": h, "fa": f, "auc_15": D.auc(1.5),
            "pc_15": D.pc_2afc(1.5)}


def _pts(cs, cn):
    h, f = D.rating_rates(cs, cn)
    return np.concatenate([[1.0], f, [0.0]]), np.concatenate([[1.0], h, [0.0]])


def compute_onyou() -> dict:
    old = ["candle", "harbour", "violin", "pepper", "ladder", "comet", "garden", "button", "tunnel", "feather",
           "anchor", "orange"]
    new = ["mirror", "basket", "thunder", "pillow", "rocket", "saddle", "island", "kettle", "marble", "lantern",
           "cactus", "wallet"]
    order = rng(7).permutation(24)
    test = [(old + new)[i] for i in order]
    is_old = np.array([i < 12 for i in order])
    hits = np.arange(13)
    table = np.array([[D.from_counts(h, 12, f, 12)["d"] for f in range(13)] for h in hits])
    ctab = np.array([[D.from_counts(h, 12, f, 12)["c"] for f in range(13)] for h in hits])
    # what Psyche gets: a typical memory, d' 1.2, criterion neutral
    psyche = D.from_counts(9, 12, 3, 12)
    return {"old": old, "new": new, "test": test, "is_old": is_old, "dtable": table, "ctable": ctab,
            "example_hits": 9, "example_fas": 3, "example_d": psyche["d"], "example_c": psyche["c"]}


def compute_ideal() -> dict:
    d = 1.5
    x = np.linspace(-3, 5, 400)
    lr = D.likelihood_ratio(x, d)
    prev = np.array([0.5, 0.2, 0.05])
    ks = np.array([D.optimal_criterion(d, p) for p in prev])
    grid = np.linspace(-2, 5, 701)
    ev = np.array([D.expected_value(d, grid, p) for p in prev])
    hit, fa = D.rates(d, ks)
    return {"d": d, "x": x, "lr": lr, "prev": prev, "criteria": ks, "grid": grid, "ev": ev, "hit": hit, "fa": fa,
            "beta": np.array([D.optimal_beta(p) for p in prev]), "acc_neutral_05": float(D.expected_value(d, d / 2, 0.05)),
            "acc_opt_05": float(D.expected_value(d, ks[2], 0.05)), "acc_always_no_05": 0.95}


def compute_fitroc() -> dict:
    obs = D.Observer(d=1.25, sigma_s=1.25)
    crit = [-0.4, 0.2, 0.7, 1.2, 1.8]
    studies = [D.simulate_ratings(obs, crit, 300, 300, rng(300 + j)) for j in range(41)]
    fits = [D.fit_rating(cs, cn) for cs, cn in studies]
    j = _median_pick([f["sigma_s"] for f in fits])
    cs, cn = studies[j]
    unequal, equal = fits[j], D.fit_rating(cs, cn, equal_variance=True)
    h, f = D.rating_rates(cs, cn)
    lr = 2 * (unequal["loglik"] - equal["loglik"])
    return {"counts_signal": cs, "counts_noise": cn, "hit": h, "fa": f, "zhit": Z(h), "zfa": Z(f),
            "d_u": unequal["d"], "s_u": unequal["sigma_s"], "slope_u": unequal["slope"], "d_e": equal["d"],
            "lr": lr, "p": float(stats.chi2.sf(lr, 1)), "true_d": 1.25, "true_s": 1.25,
            "slopes": np.array([f["slope"] for f in fits]), "recognition_slope": archive.RATCLIFF_1992.data["slope"]}


def compute_afc() -> dict:
    ds = np.linspace(0, 3, 121)
    out = {"ds": ds, "yesno_unbiased": Phi(ds / 2), "two": Phi(ds / math.sqrt(2))}
    for m in (4, 8):
        out[f"m{m}"] = np.array([D.pc_mafc(d, m) for d in ds])
    out["pc_at_1"] = D.pc_2afc(1.0)
    out["yn_at_1"] = float(Phi(0.5))
    out["d_from_75"] = D.d_from_2afc(0.75)
    return out


def compute_rivals() -> dict:
    """Rating data from an unequal-variance observer; three models' ROCs fitted by least squares in ROC space
    (the high-threshold line, the dual-process curve, the unequal-variance curve)."""
    from scipy import optimize
    r = load("fitroc")
    h, f = r["hit"], r["fa"]
    # high threshold: H = p + (1-p) F
    p_ht = float(np.clip(np.sum((h - f) * (1 - f)) / np.sum((1 - f) ** 2), 0, 1))
    sse_ht = float(np.sum((h - (p_ht + (1 - p_ht) * f)) ** 2))

    def dp(theta):
        rr, dd = theta
        k = Z(1 - f)
        return np.sum((h - (rr + (1 - rr) * (1 - Phi(k - dd)))) ** 2)
    res = optimize.minimize(dp, [0.2, 1.0], bounds=[(0, 0.95), (0, 4)])
    rr, dd = res.x
    fa_grid = np.linspace(1e-4, 1 - 1e-4, 300)
    k = Z(1 - fa_grid)
    sdt_curve = 1 - Phi((k - r["d_u"]) / r["s_u"])
    sse_sdt = float(np.sum((h - (1 - Phi((Z(1 - f) - r["d_u"]) / r["s_u"]))) ** 2))
    return {"hit": h, "fa": f, "fa_grid": fa_grid, "ht_p": p_ht, "ht_curve": p_ht + (1 - p_ht) * fa_grid,
            "sse_ht": sse_ht, "dp_r": float(rr), "dp_d": float(dd),
            "dp_curve": rr + (1 - rr) * (1 - Phi(k - dd)), "sse_dp": float(res.fun),
            "sdt_curve": sdt_curve, "sse_sdt": sse_sdt}


def compute_baserates() -> dict:
    g = archive.GIGERENZER_HOFFRAGE_1995.data
    nf = D.natural_frequencies(g["prevalence"], g["sensitivity"], g["false_positive"])
    prev = np.logspace(-3, -0.3, 120)
    d = Z(g["sensitivity"]) - Z(g["false_positive"])
    k = Z(1 - g["false_positive"])
    ppv = np.array([D.ppv(p, d, k) for p in prev])
    return {**{f"nf_{a}": b for a, b in nf.items()}, "prevalence": prev, "ppv": ppv, "d": float(d),
            "correct_prob": g["correct_prob"], "correct_freq": g["correct_freq"],
            "ppv_at_10": float(D.ppv(0.10, d, k)), "ppv_at_01": float(D.ppv(0.01, d, k))}


def compute_prevalence() -> dict:
    """An observer with d' 2.5 that moves its criterion half of the way to the accuracy-maximizing one."""
    w = archive.WOLFE_2005.data
    d = 2.5
    prev = np.logspace(-2, np.log10(0.5), 80)
    out = {"d": d, "prevalence": prev, "published_prev": np.array(w["prevalence"]),
           "published_miss": np.array(w["miss"])}
    for name, shift in (("none", 0.0), ("half", 0.5), ("full", 1.0)):
        k = D.prevalence_criteria(d, prev, shift)
        hit, fa = D.rates(d, k)
        out[f"miss_{name}"], out[f"fa_{name}"] = 1 - hit, fa
        kp = D.prevalence_criteria(d, w["prevalence"], shift)
        out[f"miss_{name}_at"] = 1 - D.rates(d, kp)[0]
    return out


def compute_classifier() -> dict:
    """Spam scores: legitimate mail ~ N(0, 1), spam ~ N(2, 1).  ROC is the same at any base rate; precision is not."""
    d = 2.0
    k = np.linspace(-3, 6, 400)
    hit, fa = D.rates(d, k)
    out = {"d": d, "fa": fa, "hit": hit, "auc": D.auc(d)}
    for name, p in (("common", 0.5), ("rare", 0.01)):
        prec = p * hit / (p * hit + (1 - p) * fa)
        out[f"precision_{name}"] = prec
        out[f"prec_at_80_{name}"] = float(np.interp(0.8, hit[::-1], prec[::-1]))
    return out


def compute_confidence() -> dict:
    """An observer decides from evidence x; its confidence reads x plus extra noise (sd 0, 0.7 or 1.5).  The
    type-2 ROC: P(high confidence | correct) against P(high confidence | wrong)."""
    g = rng(900)
    n = 200000
    d = 1.5
    signal = g.random(n) < 0.5
    x = np.where(signal, d, 0.0) + g.standard_normal(n)
    say = x > d / 2
    correct = say == signal
    out = {"d": d}
    for name, extra in (("perfect", 0.0), ("noisy", 0.7), ("noisier", 1.5)):
        conf = np.abs(x + extra * g.standard_normal(n) - d / 2)
        cuts = np.quantile(conf, np.linspace(0.02, 0.98, 49))
        h2 = np.array([np.mean(conf[correct] > c) for c in cuts])
        f2 = np.array([np.mean(conf[~correct] > c) for c in cuts])
        fx, hx = np.concatenate([[1.0], f2, [0.0]]), np.concatenate([[1.0], h2, [0.0]])
        out[f"{name}_h2"], out[f"{name}_f2"] = hx, fx
        out[f"{name}_area"] = float(-np.trapezoid(hx, fx))
    out["accuracy"] = float(np.mean(correct))
    return out


def compute_crossing() -> dict:
    """Two tests with the same area under the ROC: A with equal spreads (d' = 1.5), B whose signal is twice as
    wide.  Their ROCs cross; which is better depends on where the criterion will sit."""
    auc = D.auc(1.5)
    d_b = math.sqrt(1 + 2.0 ** 2) * Z(auc)
    fa = np.linspace(1e-4, 1 - 1e-4, 400)
    k = Z(1 - fa)
    ha, hb = 1 - Phi(k - 1.5), 1 - Phi((k - d_b) / 2.0)
    diff = ha - hb
    i = int(np.argmin(np.abs(diff[20:-20]))) + 20
    at = lambda f: (float(1 - Phi(Z(1 - f) - 1.5)), float(1 - Phi((Z(1 - f) - d_b) / 2.0)))  # noqa: E731
    return {"auc": auc, "auc_b": D.auc(d_b, 2.0), "d_b": d_b, "fa": fa, "hit_a": ha, "hit_b": hb,
            "cross_fa": float(fa[i]), "at_02": at(0.02), "at_30": at(0.30)}


def compute_guessing() -> dict:
    """The old correction for guessing, p = (H - F)/(1 - F): the high-threshold model's detection probability.
    Applied to one signal-detection observer at five criteria, it is not constant."""
    d = 1.5
    ks = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
    hit, fa = D.rates(d, ks)
    corr = (hit - fa) / (1 - fa)
    return {"d": d, "criteria": ks, "hit": hit, "fa": fa, "corrected": corr,
            "dprime": np.array([D.dprime(h, f) for h, f in zip(hit, fa)])}


def compute_odds() -> dict:
    g = archive.GIGERENZER_HOFFRAGE_1995.data
    lr = g["sensitivity"] / g["false_positive"]
    prior = g["prevalence"] / (1 - g["prevalence"])
    post = prior * lr
    lr_neg = (1 - g["sensitivity"]) / (1 - g["false_positive"])
    second = post * lr
    return {"lr": lr, "prior_odds": prior, "post_odds": post, "post_p": post / (1 + post), "lr_neg": lr_neg,
            "second_p": second / (1 + second), "neg_p": prior * lr_neg / (1 + prior * lr_neg)}


def compute_readers() -> dict:
    """Two radiologists, each with d' = 1.5.  Averaging their evidence: d' / sqrt((1 + rho)/2).  The 'either says
    yes' rule raises hits and false alarms together."""
    d = 1.5
    rho = np.linspace(0, 1, 101)
    avg = d / np.sqrt((1 + rho) / 2)
    k = d / 2
    h1, f1 = D.rates(d, k)
    either_h, either_f = 1 - (1 - h1) ** 2, 1 - (1 - f1) ** 2  # independent readers
    both_h, both_f = h1 ** 2, f1 ** 2
    return {"d": d, "rho": rho, "avg": avg, "avg_0": float(avg[0]), "avg_05": float(avg[50]), "one_h": float(h1),
            "one_f": float(f1), "either_h": float(either_h), "either_f": float(either_f), "both_h": float(both_h),
            "both_f": float(both_f)}


def compute_lineups() -> dict:
    """The diagnosticity ratio (correct identifications over false ones) along one ROC: a stricter criterion
    raises it with no change in d'."""
    m = archive.MICKES_2012.data
    d = 1.2
    fa = np.linspace(0.005, 0.995, 300)
    hit = 1 - Phi(Z(1 - fa) - d)
    pts = {}
    for name, f in (("lax", 0.30), ("strict", 0.10)):
        h = float(1 - Phi(Z(1 - f) - d))
        pts[name] = (f, h, h / f)
    return {"d": d, "fa": fa, "hit": hit, "lax": pts["lax"], "strict": pts["strict"],
            "seq": m["sequential"], "sim": m["simultaneous"],
            "ratio_seq": m["sequential"][0] / m["sequential"][1], "ratio_sim": m["simultaneous"][0] / m["simultaneous"][1]}


ITEMS = {
    "watch": compute_watch,
    "payoffs": compute_payoffs,
    "model": compute_model,
    "roc": compute_roc,
    "onyou": compute_onyou,
    "ideal": compute_ideal,
    "fitroc": compute_fitroc,
    "afc": compute_afc,
    "rivals": compute_rivals,
    "baserates": compute_baserates,
    "prevalence": compute_prevalence,
    "classifier": compute_classifier,
    "confidence": compute_confidence,
    "crossing": compute_crossing,
    "guessing": compute_guessing,
    "odds": compute_odds,
    "readers": compute_readers,
    "lineups": compute_lineups,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
