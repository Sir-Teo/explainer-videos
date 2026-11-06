"""Precompute every number in Part 58 of *Statistics, Built* ("Anytime-Valid Inference and Adaptive Experiments").

    OMP_NUM_THREADS=1 python -m videos.stats.stats58.compute            # everything missing (a few minutes)
    python -m videos.stats.stats58.compute --force board

Results are cached in ``.cache/stats58/<name>.json``.  The Nile and CAST are the Museum's; the A/B platform is the
World's (seeded); everything else is exact arithmetic or a seeded simulation.

Items:
    hook      Wald's SPRT for a defective rate: exact error rates and average sample numbers against a fixed sample
    oc        the SPRT's operating characteristic and ASN curves, exact and by Wald's approximations
    paths     sample log-LR paths of the SPRT under each hypothesis
    gs        group-sequential boundaries and the bias of the mean at stopping
    ville     peeking at a z-test against Ville's inequality; null likelihood-ratio paths
    evalues   calibrators, e-to-p, and growth rates of e-values
    ui        universal inference against the t-test: size and power
    cs        confidence sequences: widths over time and time-uniform coverage
    cast      CAST as a betting test: a mixture e-process on the order of deaths
    ebh       e-BH against BH under dependence
    nile      CUSUM and Bayesian online changepoint detection on the Nile
    arl       CUSUM's average run lengths
    bandit    Thompson sampling against a balanced design: regret and allocation
    adapt     inference after Thompson sampling: naive against adaptively weighted intervals
    ope       off-policy evaluation of a fixed policy from the adaptive logs
    board     Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import causal as CA
from explainer.stats.kit import sequential as Q

CACHE = Cache("stats58")
load = CACHE.load

P0, P1, ALPHA, BETA = 0.10, 0.20, 0.05, 0.10  # the ordnance example: a defective rate of 10% is fine, 20% is not


def rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def nest(obj):
    if isinstance(obj, np.ndarray):
        return nest(obj.tolist())
    if isinstance(obj, dict):
        return {str(k): nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, (np.floating, float)):
        v = float(obj)
        return v if math.isfinite(v) else None
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj


def compute_hook():
    e0 = Q.sprt_bernoulli_exact(P0, P0, P1, ALPHA, BETA)
    e1 = Q.sprt_bernoulli_exact(P1, P0, P1, ALPHA, BETA)
    fx = Q.fixed_n_binomial(P0, P1, ALPHA, BETA)
    th = Q.sprt_bounds(ALPHA, BETA)
    q0 = np.cumsum(e0["stop_n"])
    q1 = np.cumsum(e1["stop_n"])
    return {"p0": P0, "p1": P1, "alpha": ALPHA, "beta": BETA, "A": th["A"], "B": th["B"], "a": e0["a"], "b": e0["b"],
            "size": e0["accept_h1"], "power": e1["accept_h1"], "asn0": e0["asn"], "asn1": e1["asn"], "fixed": fx,
            "saving0": 1 - e0["asn"] / fx["n"], "saving1": 1 - e1["asn"] / fx["n"],
            "q90_0": int(np.searchsorted(q0, 0.9)) , "q90_1": int(np.searchsorted(q1, 0.9)),
            "beyond_fixed0": float(1 - q0[min(fx["n"], len(q0) - 1)]), "beyond_fixed1": float(1 - q1[min(fx["n"], len(q1) - 1)])}


def compute_oc():
    ps = np.round(np.arange(0.04, 0.3201, 0.01), 3)
    rows = []
    for p in ps:
        ex = Q.sprt_bernoulli_exact(float(p), P0, P1, ALPHA, BETA)
        wa = Q.sprt_wald_approx(float(p), P0, P1, ALPHA, BETA)
        rows.append({"p": float(p), "accept_h1": ex["accept_h1"], "asn": ex["asn"], "wald_accept_h1": wa["accept_h1"], "wald_asn": wa["asn"]})
    return {"rows": rows, "fixed_n": Q.fixed_n_binomial(P0, P1, ALPHA, BETA)["n"]}


def compute_paths():
    r = rng(5801)
    out = {}
    for name, p in (("h0", P0), ("h1", P1)):
        paths = []
        for _ in range(12):
            x = r.random(600) < p
            s = Q.sprt_simulate(x, P0, P1, ALPHA, BETA)
            paths.append({"llr": s["llr"][: s["n"]], "n": s["n"], "decision": s["decision"]})
        out[name] = paths
    th = Q.sprt_bounds(ALPHA, BETA)
    out["logA"], out["logB"] = th["logA"], th["logB"]
    return out


def compute_gs():
    K = 5
    obf = CA.obrien_fleming(K)
    poc = CA.pocock(K)
    r = rng(5802)
    thetas = [0.0, 0.1, 0.2, 0.3, 0.4]
    rows = []
    for th in thetas:
        b = Q.stopped_mean_bias(th, obf, 40, 40000, r)
        rows.append({"theta": th, **{k: v for k, v in b.items() if k != "stop_look"}, "stop_look": b["stop_look"]})
    return {"K": K, "obf": obf, "pocock": poc, "n_per_look": 40, "rows": rows}


def compute_ville():
    r = rng(5803)
    ns = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
    curve = Q.peeking_curve(ns, 0.05, 20000, r)
    v = Q.ville_check(1000, 0.3, 0.05, 20000, r)
    X = r.standard_normal((40, 1000))
    logM = np.cumsum(0.3 * X - 0.045, axis=1) / math.log(10)
    Xa = r.standard_normal((12, 1000)) + 0.3
    logMa = np.cumsum(0.3 * Xa - 0.045, axis=1) / math.log(10)
    return {"ns": ns, "curve": curve, **v, "null_paths": logM[:, ::5], "alt_paths": logMa[:, ::5], "t": np.arange(1, 1001)[::5],
            "null_cross": float(np.mean(logM.max(1) >= math.log10(20)))}


def compute_evalues():
    ps = [0.1, 0.05, 0.01, 0.005, 0.001]
    rows = [{"p": p, "e_half": float(Q.calibrate_p_to_e(p, 0.5)), "e_tenth": float(Q.calibrate_p_to_e(p, 0.1)),
             "e_sharp": float(1 / (p * math.log(1 / p) ** 2)) if p < math.exp(-2) else None} for p in ps]
    # growth: expected log e per observation for the normal likelihood ratio, by the bet mu1, when the truth is mu
    mus = np.linspace(0, 1, 11)
    bets = [0.2, 0.5, 1.0]
    growth = {str(b): [float(b * m - b * b / 2) for m in mus] for b in bets}
    # merging five independent studies' e-values (each the LR at mu1 = 0.5 for n = 20 observations of N(0.4, 1))
    r = rng(5804)
    es = np.exp(0.5 * r.normal(0.4 * 20, math.sqrt(20), (20000, 5)) - 0.125 * 20)
    return {"rows": rows, "mus": mus, "growth": growth, "prod_ge20": float(np.mean(np.prod(es, 1) >= 20)),
            "mean_ge20": float(np.mean(es.mean(1) >= 20)), "single_ge20": float(np.mean(es[:, 0] >= 20))}


def compute_ui():
    r = rng(5805)
    n, reps = 40, 4000
    mus = [0.0, 0.25, 0.5, 0.75, 1.0]
    rows = []
    for mu in mus:
        e = np.array([Q.split_lrt_normal_mean(r.normal(mu, 1.0, n), r) for _ in range(reps)])
        x = r.normal(mu, 1.0, (reps, n))
        t = x.mean(1) / (x.std(1, ddof=1) / math.sqrt(n))
        rows.append({"mu": mu, "ui_reject": float(np.mean(e >= 20)), "t_reject": float(np.mean(np.abs(t) >= stats.t.isf(0.025, n - 1))),
                     "median_e": float(np.median(e))})
    return {"n": n, "reps": reps, "rows": rows}


def compute_cs():
    r = rng(5806)
    T = 5000
    t = np.arange(1, T + 1)
    p = 0.12  # a conversion rate on the World's A/B platform
    x = (r.random(T) < p).astype(float)
    xbar = np.cumsum(x) / t
    hf = Q.hoeffding_fixed(xbar, t, 0.05)
    hu = Q.hoeffding_union(xbar, t, 0.05)
    nm = Q.normal_mixture_cs(xbar, t, 0.05, tau2=0.01 / 0.25, sigma=0.5)
    sb = Q.stitched_boundary(t, 0.05, two_sided=True) * 0.5 / t
    bc = Q.betting_cs(x, 0.05)
    clt = 1.96 * np.sqrt(np.maximum(xbar * (1 - xbar), 1e-4) / t)
    idx = np.unique(np.round(np.geomspace(1, T, 160)).astype(int)) - 1
    widths = {"t": t[idx], "xbar": xbar[idx], "clt_lo": (xbar - clt)[idx], "clt_hi": (xbar + clt)[idx],
              "hoeff_lo": hf[0][idx], "hoeff_hi": hf[1][idx], "union_lo": hu[0][idx], "union_hi": hu[1][idx],
              "mix_lo": nm[0][idx], "mix_hi": nm[1][idx], "stitch_lo": (xbar - sb)[idx], "stitch_hi": (xbar + sb)[idx],
              "bet_lo": bc["lo"][idx], "bet_hi": bc["hi"][idx]}
    final = {k: float(v[-1]) for k, v in widths.items()}
    # time-uniform coverage over 300 streams of T = 2,000
    Tc, reps = 2000, 300
    tc = np.arange(1, Tc + 1)
    samp = lambda g, n: (g.random(n) < p).astype(float)  # noqa: E731
    cov = {}
    cov["clt"] = Q.cs_coverage(lambda z: (np.cumsum(z) / tc - 1.96 * np.sqrt(np.maximum(np.cumsum(z) / tc * (1 - np.cumsum(z) / tc), 1e-4) / tc),
                                          np.cumsum(z) / tc + 1.96 * np.sqrt(np.maximum(np.cumsum(z) / tc * (1 - np.cumsum(z) / tc), 1e-4) / tc)), samp, Tc, reps, p, r, t_min=20)
    cov["hoeffding"] = Q.cs_coverage(lambda z: Q.hoeffding_fixed(np.cumsum(z) / tc, tc, 0.05), samp, Tc, reps, p, r, t_min=20)
    cov["betting"] = Q.cs_coverage(lambda z: (lambda d: (d["lo"], d["hi"]))(Q.betting_cs(z, 0.05)), samp, Tc, reps, p, r, t_min=20)
    cov["mixture"] = Q.cs_coverage(lambda z: Q.normal_mixture_cs(np.cumsum(z) / tc, tc, 0.05, tau2=0.04, sigma=0.5), samp, Tc, reps, p, r, t_min=20)
    return {"p": p, "T": T, "series": widths, "final": final, "coverage": cov, "Tc": Tc, "reps": reps, "t_min": 20}


def compute_cast():
    """CAST's 89 deaths (63 drug, 26 placebo; arms of nearly equal size).  Under H0 each death falls in the drug arm with
    probability 1/2.  A gambler who mixes over the death rate's share q ~ Uniform(0, 1) holds wealth
    B(s + 1, n - s + 1)/2^(-n) after s of n deaths fell in the drug arm: a test martingale.  The order in which the
    deaths occurred is not in the Museum, so 2,000 random orders consistent with the totals are drawn."""
    from math import lgamma, log

    n, s = museum.CAST["deaths_drug"] + museum.CAST["deaths_placebo"], museum.CAST["deaths_drug"]
    r = rng(5807)

    def logw(k, m):
        return lgamma(k + 1) + lgamma(m - k + 1) - lgamma(m + 2) + m * log(2)

    final = math.exp(logw(s, n))
    paths, first = [], []
    for i in range(2000):
        order = r.permutation(np.r_[np.ones(s), np.zeros(n - s)])
        ks = np.cumsum(order)
        lw = np.array([logw(int(k), m + 1) for m, k in enumerate(ks)]) / math.log(10)
        hit = np.flatnonzero(lw >= math.log10(20))
        first.append(int(hit[0]) + 1 if len(hit) else -1)
        if i < 30:
            paths.append(lw)
    first = np.asarray(first)
    z = (s - n / 2) / math.sqrt(n / 4)
    return {"n": n, "s": s, "final_e": final, "p_from_e": 1 / final, "z": z, "p_z": float(2 * stats.norm.sf(z)),
            "paths": paths, "first_median": float(np.median(first[first > 0])), "first_q10": float(np.quantile(first[first > 0], 0.1)),
            "first_q90": float(np.quantile(first[first > 0], 0.9)), "ever": float(np.mean(first > 0))}


def compute_ebh():
    r = rng(5808)
    m, k, reps, q = 50, 10, 4000, 0.1
    from explainer.stats.kit.multiple import bh

    res = {"bh": {"fdp": [], "pow": []}, "ebh": {"fdp": [], "pow": []}}
    for _ in range(reps):
        rho = 0.6
        z0 = r.standard_normal()
        z = math.sqrt(rho) * z0 + math.sqrt(1 - rho) * r.standard_normal(m)
        mu = np.r_[np.zeros(m - k), np.full(k, 3.0)]
        x = z + mu
        pv = stats.norm.sf(x)
        e = np.exp(3.0 * x - 4.5)
        rb = np.asarray(bh(pv, q)["reject"], bool)
        re = Q.ebh(e, q)["reject"]
        for nm, rj in (("bh", rb), ("ebh", re)):
            res[nm]["fdp"].append(rj[: m - k].sum() / max(1, rj.sum()))
            res[nm]["pow"].append(rj[m - k:].mean())
    return {"m": m, "k": k, "rho": 0.6, "q": q, **{nm: {"fdr": float(np.mean(v["fdp"])), "power": float(np.mean(v["pow"]))} for nm, v in res.items()}}


def compute_nile():
    years, flow = museum.nile()
    pre = flow[:28]
    mu0, sd = float(pre.mean()), float(pre.std(ddof=1))
    z = (flow - mu0) / sd
    c = Q.cusum(-z, 0.0, 1.0, 4.0)  # a downward shift of one SD
    R = Q.bocpd_normal(z, 1 / 100, mu0=0.0, kappa0=0.5, sigma=1.0)
    rl = np.argmax(R[1:], axis=1)
    cp_year = [int(years[t] - rl[t] + 1) for t in range(len(years))]
    last = R[-1]
    return {"years": years, "flow": flow, "mu0": mu0, "sd": sd, "W": c["W"], "alarm_year": int(years[c["alarm"]]) if c["alarm"] >= 0 else None,
            "h": 4.0, "R_top": R[1:, :60], "map_cp": cp_year, "final_cp": int(years[-1] - int(np.argmax(last)) + 1),
            "pre_mean": float(flow[years < 1899].mean()), "post_mean": float(flow[years >= 1899].mean())}


def compute_arl():
    r = rng(5809)
    rows = []
    for h in (2.0, 3.0, 4.0, 5.0):
        rows.append({"h": h, "arl0": Q.cusum_arl(0.0, 0.0, 1.0, h, 400, r), "arl1": Q.cusum_arl(1.0, 0.0, 1.0, h, 2000, r)})
    return {"rows": rows}


def compute_bandit():
    r = rng(5810)
    means = [0.10, 0.12]  # two page designs on the World's A/B platform: conversion 10% and 12%
    T, reps = 4000, 60
    regret_ts, alloc = [], []
    for _ in range(reps):
        d = Q.thompson_bernoulli(means, T, r, floor=0.0, n_mc=60)
        regret_ts.append(np.cumsum(means[1] - np.asarray(means)[d["arm"]]))
        alloc.append(d["e"][:, 1])
    regret_ts = np.mean(regret_ts, 0)
    alloc = np.mean(alloc, 0)
    lr = (means[1] - means[0]) / (means[0] * math.log(means[0] / means[1]) + (1 - means[0]) * math.log((1 - means[0]) / (1 - means[1])))
    idx = np.unique(np.round(np.geomspace(1, T, 120)).astype(int)) - 1
    return {"means": means, "T": T, "t": np.arange(1, T + 1)[idx], "regret_ts": regret_ts[idx], "regret_balanced": (0.5 * 0.02 * np.arange(1, T + 1))[idx],
            "alloc": alloc[idx], "lai_robbins_coef": lr, "final_ts": float(regret_ts[-1]), "final_bal": 0.5 * 0.02 * T}


def compute_adapt():
    r = rng(5811)
    means = [0.5, 0.5]  # no difference: the case where the sample mean is not asymptotically normal
    T, reps = 1000, 1000
    out = {"naive": [], "aw": [], "naive_est": [], "aw_est": [], "n0": []}
    for _ in range(reps):
        d = Q.thompson_bernoulli(means, T, r, floor=0.01, n_mc=100)
        est = Q.arm_estimates(d["arm"], d["y"], d["e"], 2)[0]
        out["naive"].append(est["naive_lo"] <= means[0] <= est["naive_hi"])
        out["aw"].append(est["aw_lo"] <= means[0] <= est["aw_hi"])
        out["naive_est"].append(est["naive"])
        out["aw_est"].append(est["aw"])
        out["n0"].append(est["n"])
    ne, ae = np.asarray(out["naive_est"]), np.asarray(out["aw_est"])
    return {"means": means, "T": T, "reps": reps, "floor": 0.01, "naive_cov": float(np.mean(out["naive"])), "aw_cov": float(np.mean(out["aw"])),
            "naive_bias": float(ne.mean() - 0.5), "aw_bias": float(ae.mean() - 0.5), "naive_est": ne, "aw_est": ae,
            "n0_q10": float(np.quantile(out["n0"], 0.1)), "n0_q90": float(np.quantile(out["n0"], 0.9))}


def compute_ope():
    r = rng(5812)
    means = [0.10, 0.12]
    T, reps = 4000, 200
    ipw, dr, cov_ipw, cov_dr = [], [], 0, 0
    for _ in range(reps):
        d = Q.thompson_bernoulli(means, T, r, floor=0.05, n_mc=60)
        P = np.tile([1.0, 0.0], (T, 1))  # the policy "always show design A"
        v = Q.policy_value(d["y"], d["arm"], d["e"], P, mhat=np.array([0.11, 0.11]))
        ipw.append(v["ipw"])
        dr.append(v["dr"])
        cov_ipw += abs(v["ipw"] - means[0]) <= 1.96 * v["ipw_se"]
        cov_dr += abs(v["dr"] - means[0]) <= 1.96 * v["dr_se"]
    return {"means": means, "T": T, "reps": reps, "ipw_mean": float(np.mean(ipw)), "ipw_sd": float(np.std(ipw)), "dr_mean": float(np.mean(dr)),
            "dr_sd": float(np.std(dr)), "ipw_cov": cov_ipw / reps, "dr_cov": cov_dr / reps}


def compute_board():
    rows = []
    cs = load("cs")
    cov = cs["coverage"]
    rows.append(Row(58, r"fixed-$n$ CLT interval, \ checked every visit", r"conversion 12\%, \ visitors 20 to 2{,}000", "coverage", 0.95, cov["clt"]["uniform"], cs["reps"]))
    rows.append(Row(58, r"betting confidence sequence", r"conversion 12\%, \ visitors 20 to 2{,}000", "coverage", 0.95, cov["betting"]["uniform"], cs["reps"]))
    ad = load("adapt")
    rows.append(Row(58, r"naive interval after Thompson sampling", r"two equal arms, \ 1{,}000 visitors", "coverage", 0.95, ad["naive_cov"], ad["reps"]))
    rows.append(Row(58, r"adaptively weighted AIPW interval", r"two equal arms, \ 1{,}000 visitors", "coverage", 0.95, ad["aw_cov"], ad["reps"]))
    save_rows(58, rows)
    return {"rows": [asdict(q) | {"verdict": q.verdict, "se": q.se} for q in rows]}


ITEMS = {
    "hook": compute_hook, "oc": compute_oc, "paths": compute_paths, "gs": compute_gs, "ville": compute_ville,
    "evalues": compute_evalues, "ui": compute_ui, "cs": compute_cs, "cast": compute_cast, "ebh": compute_ebh,
    "nile": compute_nile, "arl": compute_arl, "bandit": compute_bandit, "adapt": compute_adapt, "ope": compute_ope,
    "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
