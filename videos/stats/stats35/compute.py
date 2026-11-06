"""Precompute every number in Part 35 of *Statistics, Built* ("What If? Experiments and Potential Outcomes").

    OMP_NUM_THREADS=1 python -m videos.stats.stats35.compute            # everything missing (a few minutes)
    python -m videos.stats.stats35.compute --force board

Results are cached in ``.cache/stats35/<name>.json``.  The patients are the World's clinic trial (``World.trial``),
with both potential outcomes; the schools and the epidemic are the World's; the Salk, ISIS-2 and CAST numbers are the
Museum's; the rest are seeded simulations.

Items:
    science     the science table: the first patients' Y(0), Y(1), tau; the trial's and the pool's average effects
    selection   a doctor chooses who is treated vs a coin: the naive comparison's bias
    fisher      the sharp null, exactly, on 12 patients; by Monte Carlo on all 2,000; the inverted interval
    neyman      Neyman's exact and conservative variances; the randomization distribution over re-randomizations
    blocks      complete vs blocked vs matched-pair designs: the estimator's SD
    adjust      adjustment on the trial; Freedman's small unbalanced design: ANCOVA vs Lin
    cluster     the schools' tutoring programme re-randomized: pupil-level vs school-level analysis
    noncomp     compliance types; ITT, as-treated, per-protocol and the IV estimate of the complier effect
    interfere   the epidemic's two-stage design: direct, indirect, total and overall effects
    subgroups   twelve 'zodiac' subgroups of a trial with one true effect
    sequential  peeking; Pocock, O'Brien-Fleming and Lan-DeMets boundaries; their power and expected size
    surrogate   two drugs that lower pressure equally; one also harms: Prentice's criteria
    transport   the trial's effect transported to the pool by inverse odds of participation
    board       Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import causal as CA
from explainer.stats.world import World

CACHE = Cache("stats35")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def nest(obj):
    if isinstance(obj, np.ndarray):
        return nest(obj.tolist())
    if isinstance(obj, dict):
        return {str(k): nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, float) and not np.isfinite(obj):
        return None
    return obj


def eff_reps(per_rep, nominal=0.9) -> int:
    v = np.var(np.asarray(per_rep, float), ddof=1) / len(per_rep)
    return int(round(nominal * (1 - nominal) / max(v, 1e-12)))


def complete(n, n1, g):
    z = np.zeros(n, bool)
    z[g.choice(n, n1, replace=False)] = True
    return z


# ------------------------------------------------------------------------------------------------- items


def compute_science():
    t = World().trial
    y0, y1, tau = t["y0"], t["y1"], t["tau"]
    first = [{"age": int(t["age"][i]), "base": float(t["base"][i]), "y0": float(y0[i]), "y1": float(y1[i]),
              "tau": float(tau[i])} for i in range(8)]
    h, e = np.histogram(tau, bins=24, range=(-28, 8))
    return nest({"first": first, "ate": float(tau.mean()), "ate_pool": float(t["tau_pool"].mean()),
                 "sd_tau": float(tau.std()), "harmed": float(np.mean(tau > 0)), "n": len(tau),
                 "n_pool": len(t["pool"]), "hist": h, "edges": e, "mean_y0": float(y0.mean()),
                 "mean_y1": float(y1.mean()), "age_trial": float(t["age"].mean()), "age_pool": float(t["age_pool"].mean())})


def compute_selection():
    t = World().trial
    y0, y1, doc = t["y0"], t["y1"], t["doctor"]
    g = rng(351)
    zd = g.random(len(y0)) < doc
    yd = np.where(zd, y1, y0)
    zr = complete(len(y0), 1000, g)
    yr = np.where(zr, y1, y0)
    naive = CA.diff_means(yd, zd)
    rand = CA.diff_means(yr, zr)
    # the decomposition: E[Y(1)|treated] - E[Y(0)|untreated] = ATT + selection bias
    att = float((y1 - y0)[zd].mean())
    bias = float(y0[zd].mean() - y0[~zd].mean())
    return nest({"naive": naive, "rand": rand, "ate": float((y1 - y0).mean()), "att": att, "sel_bias": bias,
                 "share_treated": float(zd.mean()), "base_treated": float(t["base"][zd].mean()),
                 "base_untreated": float(t["base"][~zd].mean()), "y_treated": float(yd[zd].mean()),
                 "y_untreated": float(yd[~zd].mean())})


def compute_fisher():
    t = World().trial
    g = rng(352)
    pick = g.choice(len(t["y0"]), 12, replace=False)
    y0, y1 = t["y0"][pick], t["y1"][pick]
    z = np.zeros(12, bool)
    z[g.choice(12, 6, replace=False)] = True
    y = np.where(z, y1, y0)
    r = CA.fisher_test(y, z)
    ci = CA.fisher_ci(y, z, np.arange(-30, 15.5, 0.5), reps=2000, rng=g)
    hist, edges = np.histogram(r["dist"], bins=30)
    # all 2,000, Monte Carlo
    Z = complete(len(t["y0"]), 1000, g)
    Y = np.where(Z, t["y1"], t["y0"])
    big = CA.fisher_test(Y, Z, reps=10000, rng=g)
    return nest({"y": y, "z": z, "obs": r["obs"], "p": r["p"], "n_assign": len(r["dist"]), "hist": hist,
                 "edges": edges, "ci": [ci["lo"], ci["hi"]], "big_obs": big["obs"], "big_p": big["p"],
                 "big_max": float(np.max(np.abs(big["dist"]))), "big_sd": float(np.std(big["dist"]))})


def compute_neyman():
    t = World().trial
    y0, y1 = t["y0"], t["y1"]
    n, n1 = len(y0), 1000
    v = CA.neyman_true_var(y0, y1, n1)
    g = rng(353)
    ests, ses, cover = [], [], []
    ate = v["ate"]
    for _ in range(4000):
        z = complete(n, n1, g)
        r = CA.diff_means(np.where(z, y1, y0), z)
        ests.append(r["est"])
        ses.append(r["se"])
        cover.append(r["lo"] <= ate <= r["hi"])
    ests = np.array(ests)
    h, e = np.histogram(ests, bins=30)
    # a constant-effect science with the same Y(0): the conservative estimator is exact
    yc1 = y0 + ate
    vc = CA.neyman_true_var(y0, yc1, n1)
    return nest({"ate": ate, "true_sd": math.sqrt(v["true"]), "cons_sd": math.sqrt(v["conservative"]),
                 "S_tau": math.sqrt(v["S_tau2"]), "S1": float(y1.std(ddof=1)), "S0": float(y0.std(ddof=1)),
                 "sim_sd": float(ests.std()), "mean_se": float(np.mean(ses)), "cover": float(np.mean(cover)),
                 "cover_per": np.array(cover, float), "hist": h, "edges": e, "const_true": math.sqrt(vc["true"]),
                 "const_cons": math.sqrt(vc["conservative"])})


def compute_blocks():
    t = World().trial
    y0, y1, base = t["y0"], t["y1"], t["base"]
    n = len(y0)
    g = rng(354)
    order = np.argsort(base)
    blocks = np.empty(n, int)
    blocks[order] = np.arange(n) * 10 // n  # ten blocks by baseline pressure
    pairs = np.empty(n, int)
    pairs[order] = np.arange(n) // 2
    out = {"complete": [], "blocked": [], "paired": []}
    se = {"complete": [], "blocked": [], "paired": []}
    for _ in range(1500):
        z = complete(n, n // 2, g)
        r = CA.diff_means(np.where(z, y1, y0), z)
        out["complete"].append(r["est"])
        se["complete"].append(r["se"])
        zb = np.zeros(n, bool)
        for b in range(10):
            idx = np.flatnonzero(blocks == b)
            zb[g.choice(idx, len(idx) // 2, replace=False)] = True
        r = CA.blocked(np.where(zb, y1, y0), zb, blocks)
        out["blocked"].append(r["est"])
        se["blocked"].append(r["se"])
        zp = np.zeros(n, bool)
        flip = g.random(n // 2) < 0.5
        first = order[0::2]
        second = order[1::2]
        zp[np.where(flip, first, second)] = True
        yp = np.where(zp, y1, y0)
        d = np.array([yp[a] - yp[b] if zp[a] else yp[b] - yp[a] for a, b in zip(first, second)])
        out["paired"].append(float(d.mean()))
        se["paired"].append(float(d.std(ddof=1) / math.sqrt(len(d))))
    return nest({k: {"sd": float(np.std(v)), "mean": float(np.mean(v)), "mean_se": float(np.mean(se[k]))}
                 for k, v in out.items()} | {"ate": float((y1 - y0).mean()), "corr_base_y0": float(np.corrcoef(base, y0)[0, 1])})


def _freedman_pop(g, n=60):
    """A small finite population for Freedman's critique: one covariate, effects that grow with it, noise that
    grows with it too."""
    x = g.gamma(2.0, 1.0, n)
    x = (x - x.mean()) / x.std()
    y0 = 10 + 3 * x + (1 + 0.8 * np.abs(x)) * g.standard_normal(n)
    y1 = y0 + 2 + 4 * x + (1 + 0.8 * np.abs(x)) * g.standard_normal(n)
    return x, y0, y1


def compute_adjust():
    t = World().trial
    y0, y1, base, age = t["y0"], t["y1"], t["base"], t["age"]
    n = len(y0)
    g = rng(355)
    X = np.column_stack([base, age])
    unadj, anc, lin = [], [], []
    for _ in range(600):
        z = complete(n, n // 2, g)
        y = np.where(z, y1, y0)
        unadj.append(CA.diff_means(y, z)["est"])
        anc.append(CA.ancova(y, z, X)["est"])
        lin.append(CA.lin(y, z, X)["est"])
    # Freedman's design: 200 units, only 50 treated
    x, f0, f1 = _freedman_pop(g, 200)
    ate = float((f1 - f0).mean())
    ca, cl, ea, el, sa, sl, eu = [], [], [], [], [], [], []
    for _ in range(4000):
        z = complete(200, 50, g)
        y = np.where(z, f1, f0)
        a, l_ = CA.ancova(y, z, x), CA.lin(y, z, x)
        eu.append(CA.diff_means(y, z)["est"])
        ca.append(a["lo"] <= ate <= a["hi"])
        cl.append(l_["lo"] <= ate <= l_["hi"])
        ea.append(a["est"])
        el.append(l_["est"])
        sa.append(a["se"])
        sl.append(l_["se"])
    return nest({"sd_unadj": float(np.std(unadj)), "sd_ancova": float(np.std(anc)), "sd_lin": float(np.std(lin)),
                 "ate": float((y1 - y0).mean()), "f_ate": ate, "f_cover_ancova": float(np.mean(ca)),
                 "f_cover_lin": float(np.mean(cl)), "f_bias_ancova": float(np.mean(ea) - ate),
                 "f_bias_lin": float(np.mean(el) - ate), "f_sd_ancova": float(np.std(ea)), "f_sd_lin": float(np.std(el)),
                 "f_se_ancova": float(np.mean(sa)), "f_se_lin": float(np.mean(sl)), "f_sd_unadj": float(np.std(eu)),
                 "reps": 4000})


def compute_cluster():
    w = World()
    s = w.schools
    eff = 100 * w.PROGRAMME_EFFECT
    prog = s["programme"]
    sch = s["school"]
    y0 = s["score"] - eff * prog[sch]
    y1 = y0 + eff
    k = len(prog)
    g = rng(356)
    cn, cc, wn, wc = [], [], [], []
    for _ in range(1000):
        zc = np.zeros(k, bool)
        zc[g.choice(k, k // 2, replace=False)] = True
        y = np.where(zc[sch], y1, y0)
        r = CA.cluster_diff(y, zc, sch)
        cn.append(r["naive"]["lo"] <= eff <= r["naive"]["hi"])
        cc.append(r["cluster"]["lo"] <= eff <= r["cluster"]["hi"])
        wn.append(r["naive"]["se"])
        wc.append(r["cluster"]["se"])
    sizes = s["size"]
    icc = w.SCHOOL_SD ** 2 / (w.SCHOOL_SD ** 2 + w.PUPIL_SD ** 2)
    return nest({"effect": eff, "k": k, "n": len(sch), "mean_size": float(sizes.mean()), "icc": icc,
                 "deff": CA.design_effect(float(sizes.mean()), icc), "cover_naive": float(np.mean(cn)),
                 "cover_cluster": float(np.mean(cc)), "se_naive": float(np.mean(wn)), "se_cluster": float(np.mean(wc)),
                 "reps": 1000})


def _noncomp_rep(t, g):
    n = len(t["y0"])
    z = complete(n, n // 2, g)
    ct = t["ctype"]
    d = np.where(ct == 0, z, ct == 2)
    y = np.where(d, t["y1"], t["y0"])
    itt = CA.diff_means(y, z)
    iv = CA.iv_late(y, z, d)
    at = CA.diff_means(y, d.astype(bool))
    keep = (z & d) | (~z & ~d)
    pp = CA.diff_means(y[keep], z[keep])
    return itt, iv, at, pp


def compute_noncomp():
    t = World().trial
    ct = t["ctype"]
    tau = t["tau"]
    cace = float(tau[ct == 0].mean())
    g = rng(357)
    itt, iv, at, pp = _noncomp_rep(t, g)
    shares = np.bincount(ct, minlength=3) / len(ct)
    return nest({"shares": shares, "cace": cace, "ate": float(tau.mean()), "itt": itt, "iv": iv, "as_treated": at,
                 "per_protocol": pp, "age_by_type": [float(t["age"][ct == k].mean()) for k in range(3)],
                 "y0_by_type": [float(t["y0"][ct == k].mean()) for k in range(3)],
                 "tau_by_type": [float(tau[ct == k].mean()) for k in range(3)]})


def compute_interfere():
    w = World()
    e = w.epidemic
    town = e["town"]
    K = 200
    g = rng(358)
    shares = (0.3, 0.7)

    def run(psi_town, g):
        target = np.where(psi_town == 1, shares[1], shares[0])
        v = np.zeros(len(town), bool)
        for j in range(K):
            idx = np.flatnonzero(town == j)
            v[g.choice(idx, int(round(target[j] * len(idx))), replace=False)] = True
        share = np.bincount(town, weights=v, minlength=K) / np.bincount(town, minlength=K)
        return v, w.infected(v, share).astype(float)

    psi = np.zeros(K, int)
    psi[g.choice(K, K // 2, replace=False)] = 1
    v, y = run(psi, g)
    est = CA.two_stage(y, v, town, psi)
    # the truth for this population: average over many within-town assignments with every town on each strategy
    truth = {}
    for k in (0, 1):
        ys1, ys0, ya = [], [], []
        for _ in range(60):
            vv, yy = run(np.full(K, k), g)
            ys1.append(yy[vv].mean())
            ys0.append(yy[~vv].mean())
            ya.append(yy.mean())
        truth[k] = {"y1": float(np.mean(ys1)), "y0": float(np.mean(ys0)), "all": float(np.mean(ya))}
    tr = {"direct0": truth[0]["y0"] - truth[0]["y1"], "direct1": truth[1]["y0"] - truth[1]["y1"],
          "indirect": truth[0]["y0"] - truth[1]["y0"], "total": truth[0]["y0"] - truth[1]["y1"],
          "overall": truth[0]["all"] - truth[1]["all"]}
    # an individually randomized trial at 50% everywhere: what it sees
    v50 = g.random(len(town)) < 0.5
    share50 = np.bincount(town, weights=v50, minlength=K) / np.bincount(town, minlength=K)
    y50 = w.infected(v50, share50).astype(float)
    none = w.infected(np.zeros(len(town)), np.zeros(K)).mean()
    allv = w.infected(np.ones(len(town)), np.ones(K)).mean()
    return nest({"est": est, "truth": truth, "true_effects": tr, "rct50": float(y50[~v50].mean() - y50[v50].mean()),
                 "none": float(none), "all": float(allv), "rate_mean": float(e["rate"].mean())})


def compute_subgroups():
    """A trial the size of ISIS-2 (8,600 per arm, death 11.8% vs 9.4%), split at random into 12 'zodiac' subgroups:
    how often does at least one subgroup show no benefit (or harm), and how often does one show a 'significant'
    interaction?"""
    g = rng(359)
    n, p0, p1 = 8600, 0.118, 0.094
    reps = 2000
    any_harm, any_sig_int, worst = 0, 0, []
    for _ in range(reps):
        s0 = g.integers(0, 12, n)
        s1 = g.integers(0, 12, n)
        d0 = g.random(n) < p0
        d1 = g.random(n) < p1
        r0 = np.bincount(s0, weights=d0, minlength=12) / np.bincount(s0, minlength=12)
        r1 = np.bincount(s1, weights=d1, minlength=12) / np.bincount(s1, minlength=12)
        diff = r0 - r1
        any_harm += int(np.any(diff <= 0))
        n0, n1 = np.bincount(s0, minlength=12), np.bincount(s1, minlength=12)
        se = np.sqrt(r0 * (1 - r0) / n0 + r1 * (1 - r1) / n1)
        zi = (diff - (p0 - p1)) / se
        any_sig_int += int(np.any(np.abs(zi) > 1.96))
        worst.append(float(diff.min()))
    # one example draw
    s0 = g.integers(0, 12, n)
    s1 = g.integers(0, 12, n)
    d0 = g.random(n) < p0
    d1 = g.random(n) < p1
    r0 = np.bincount(s0, weights=d0, minlength=12) / np.bincount(s0, minlength=12)
    r1 = np.bincount(s1, weights=d1, minlength=12) / np.bincount(s1, minlength=12)
    return nest({"p_any_no_benefit": any_harm / reps, "p_any_sig_interaction": any_sig_int / reps,
                 "example_diff": r0 - r1, "true_diff": p0 - p1, "reps": reps,
                 "p_sig_interaction_one": 0.05})


def compute_sequential():
    K = 5
    poc = CA.pocock(K)
    obf = CA.obrien_fleming(K)
    ld = CA.spending_bounds(np.arange(1, K + 1) / K)
    g = rng(360)
    peek = {k: CA.peeking_sim(k, 20000, g) for k in (1, 2, 3, 5, 10, 20)}
    # power and expected stopping look under a drift giving 80% power for the fixed design
    theta = stats.norm.ppf(0.975) + stats.norm.ppf(0.8)
    res = {}
    for name, b in (("fixed", [np.inf] * (K - 1) + [1.96]), ("pocock", [poc] * K), ("obf", list(obf))):
        cp = CA.crossing_probs(b, drift=theta)
        power = float(cp.sum())
        # expected information used: stop at look k with prob cp[k]; else run to K
        e_looks = float(np.sum(cp * np.arange(1, K + 1)) + (1 - power) * K) / K
        res[name] = {"power": power, "e_info": e_looks, "alpha": float(CA.crossing_probs(b).sum())}
    # a z-path for illustration: one simulated trial under the alternative
    x = g.standard_normal(K * 40) + theta / math.sqrt(K * 40)
    zpath = [float(x[: 40 * k].sum() / math.sqrt(40 * k)) for k in range(1, K + 1)]
    xs0 = g.standard_normal(K * 40)
    zpath0 = [float(xs0[: 40 * k].sum() / math.sqrt(40 * k)) for k in range(1, K + 1)]
    return nest({"K": K, "pocock": poc, "obf": obf, "ld": ld, "peek": peek, "res": res, "theta": theta,
                 "zpath": zpath, "zpath0": zpath0, "spend_t": np.linspace(0.01, 1, 60),
                 "spend_obf": CA.spending(np.linspace(0.01, 1, 60)), "spend_poc": CA.spending(np.linspace(0.01, 1, 60), kind="pocock")})


def compute_surrogate():
    """Two drugs lower 12-week pressure equally.  Drug A protects against stroke only through pressure; drug B also
    has an off-target harm (as encainide and flecainide suppressed arrhythmias while raising deaths).  Five-year
    stroke risk: logistic(-3.2 + 0.035 (y - 140)) (+ 0.9 for drug B)."""
    t = World().trial
    g = rng(361)
    n = len(t["y0"])
    out = {}
    for drug, harm in (("A", 0.0), ("B", 0.9)):
        z = complete(n, n // 2, g)
        s = np.where(z, t["y1"], t["y0"])
        lp = -3.2 + 0.035 * (s - 140) + harm * z
        y = (g.random(n) < 1 / (1 + np.exp(-lp))).astype(float)
        pr = CA.prentice(y, s, z)
        out[drug] = {"prentice": pr, "s_diff": float(s[z].mean() - s[~z].mean()), "risk_t": float(y[z].mean()),
                     "risk_c": float(y[~z].mean())}
    return nest(out | {"cast": {"drug": 63, "placebo": 26}})


def compute_transport():
    t = World().trial
    g = rng(362)
    n = len(t["y0"])
    z = complete(n, n // 2, g)
    y = np.where(z, t["y1"], t["y0"])
    Xt = np.column_stack([t["age"], t["base"], t["female"], t["bmi"]])
    # the target: a random 20,000 of the pool
    k = g.choice(len(t["pool"]), 20000, replace=False)
    Xg = np.column_stack([t["age_pool"][k], t["base_pool"][k], t["female_pool"][k], t["bmi_pool"][k]])
    tr = CA.transport(y, z, Xt, Xg)
    trial = CA.diff_means(y, z)
    ages = np.arange(40, 100, 5)
    h_t = np.histogram(t["age"], bins=ages)[0]
    h_p = np.histogram(t["age_pool"], bins=ages)[0]
    return nest({"trial": trial, "transported": tr["est"], "ess": tr["ess"], "ate_trial": float(t["tau"].mean()),
                 "ate_pool": float(t["tau_pool"].mean()), "ages": ages, "h_trial": h_t / h_t.sum(),
                 "h_pool": h_p / h_p.sum()})


def compute_board():
    rows = []
    t = World().trial
    y0, y1, doc = t["y0"], t["y1"], t["doctor"]
    ate = float((y1 - y0).mean())
    g = rng(370)
    reps = 1000
    cd, cr = [], []
    for _ in range(reps):
        zd = g.random(len(y0)) < doc
        r = CA.diff_means(np.where(zd, y1, y0), zd)
        cd.append(r["lo"] <= ate <= r["hi"])
        zr = complete(len(y0), 1000, g)
        r = CA.diff_means(np.where(zr, y1, y0), zr)
        cr.append(r["lo"] <= ate <= r["hi"])
    rows.append(Row(35, r"doctor chooses, \ difference in means", r"World trial, \ $n = 2{,}000$", "coverage", 0.9,
                    float(np.mean(cd)), reps))
    rows.append(Row(35, r"randomized, \ Neyman 90\% CI", r"World trial, \ $n = 2{,}000$", "coverage", 0.9,
                    float(np.mean(cr)), reps))
    ad = load("adjust")
    rows.append(Row(35, r"ANCOVA, \ conventional SE", r"Freedman's design: \ $n = 200$, \ 50 treated", "coverage", 0.9,
                    ad["f_cover_ancova"], ad["reps"]))
    rows.append(Row(35, r"Lin, \ HC2 SE", r"Freedman's design: \ $n = 200$, \ 50 treated", "coverage", 0.9,
                    ad["f_cover_lin"], ad["reps"]))
    cl = load("cluster")
    rows.append(Row(35, r"pupil-level CI, \ school-randomized", r"World schools, \ 400 schools", "coverage", 0.9,
                    cl["cover_naive"], cl["reps"]))
    rows.append(Row(35, r"school-level CI", r"World schools, \ 400 schools", "coverage", 0.9, cl["cover_cluster"],
                    cl["reps"]))
    # noncompliance: as-treated vs IV, coverage of the complier effect
    ct = t["ctype"]
    cace = float(t["tau"][ct == 0].mean())
    ca_, ci_ = [], []
    for _ in range(reps):
        itt, iv, at, pp = _noncomp_rep(t, g)
        ca_.append(at["lo"] <= cace <= at["hi"])
        ci_.append(iv["lo"] <= cace <= iv["hi"])
    rows.append(Row(35, r"as-treated comparison", r"World trial, \ with never- and always-takers", "coverage", 0.9,
                    float(np.mean(ca_)), reps, extra="for the complier effect"))
    rows.append(Row(35, r"IV (Wald) estimate", r"World trial, \ with never- and always-takers", "coverage", 0.9,
                    float(np.mean(ci_)), reps, extra="for the complier effect"))
    sq = load("sequential")
    nrep = 20000
    rows.append(Row(35, r"peeking: \ $|z| > 1.96$ at 5 looks", r"null trials", "size", 0.05, sq["peek"]["5"], nrep))
    gq = rng(371)
    rows.append(Row(35, r"Pocock boundary, \ 5 looks", r"null trials", "size", 0.05,
                    CA.peeking_sim(5, nrep, gq, [sq["pocock"]] * 5), nrep))
    rows.append(Row(35, r"O'Brien--Fleming, \ 5 looks", r"null trials", "size", 0.05,
                    CA.peeking_sim(5, nrep, gq, sq["obf"]), nrep))
    save_rows(35, rows)
    return nest({"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]})


ITEMS = {
    "science": compute_science, "selection": compute_selection, "fisher": compute_fisher, "neyman": compute_neyman,
    "blocks": compute_blocks, "adjust": compute_adjust, "cluster": compute_cluster, "noncomp": compute_noncomp,
    "interfere": compute_interfere, "subgroups": compute_subgroups, "sequential": compute_sequential,
    "surrogate": compute_surrogate, "transport": compute_transport, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
