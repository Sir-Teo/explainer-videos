"""Precompute every number in Part 37 of *Statistics, Built* ("Natural Experiments").

    OMP_NUM_THREADS=1 python -m videos.stats.stats37.compute            # everything missing (about ten minutes)
    python -m videos.stats.stats37.compute --force board

Results are cached in ``.cache/stats37/<name>.json``.  Snow's Table IX, Card & Krueger's means and the Prop 99 panel
are the Museum's; the schooling survey, the scholarship and the rollout are the World's; the rest are seeded
simulations.

Items:
    iv          quarter of birth as an instrument for schooling in the World: first stage, reduced form, Wald, 2SLS, OLS
    weak        weak instruments: 2SLS across samples, the t-test's size against instrument strength, AR sets, LIML
    many        thirty instruments, fake instruments (Bound, Jaeger & Baker), and Mendelian randomization
    rd          the World's scholarship: binned means, local fits, bandwidths, conventional and robust estimates
    rdvalid     McCrary's test after re-marking, covariate balance, the fuzzy design
    did         Card & Krueger's 2x2; the rollout's 2009 cohort against the never-treated; its event study
    didinf      Bertrand, Duflo & Mullainathan's placebo laws on the World's towns: OLS vs clustered SEs
    staggered   the World's rollout: TWFE, the Goodman-Bacon decomposition, Callaway-Sant'Anna, imputation
    honest      a cohort with a pre-trend: event study and Rambachan-Roth sets
    synth       Prop 99: California's synthetic control, its weights and the placebo states
    sdid        synthetic DiD on Prop 99, with SC and DiD, and placebo standard errors
    panel       fixed effects as FWL; Nickell's bias and Anderson-Hsiao
    bounds      Manski's worst-case bounds and Lee's trimming bounds
    board       Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import quasi as Q
from explainer.stats.world import World

CACHE = Cache("stats37")
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


# ----------------------------------------------------------------------------------------------------------------------
# Instruments
# ----------------------------------------------------------------------------------------------------------------------


def schooling_arrays():
    S = World().schooling
    q, reg = S["q"], S["region"]
    Z1 = (q == 1).astype(float)
    Zq = np.column_stack([(q == j).astype(float) for j in (1, 2, 3)])
    Zm = np.column_stack([((q == j) & (reg == r)).astype(float) for j in (1, 2, 3) for r in range(10)])
    Xr = np.column_stack([(reg == r).astype(float) for r in range(1, 10)])
    return S, Z1, Zq, Zm, Xr


def compute_iv():
    S, Z1, Zq, Zm, Xr = schooling_arrays()
    y, d, q = S["logwage"], S["school"], S["q"]
    byq = {int(j): {"school": float(d[q == j].mean()), "wage": float(y[q == j].mean()), "n": int((q == j).sum())}
           for j in (1, 2, 3, 4)}
    dS = d[q == 1].mean() - d[q != 1].mean()
    dW = y[q == 1].mean() - y[q != 1].mean()
    full1 = Q.tsls(y, d, Z1)
    full3 = Q.tsls(y, d, Zq)
    k = np.sort(rng(3701).choice(len(y), 5000, replace=False))
    s1 = Q.tsls(y[k], d[k], Z1[k])
    ar = Q.ar_set(y[k], d[k], Z1[k], grid=np.linspace(-0.3, 0.5, 161))
    s3 = Q.tsls(y[k], d[k], Zq[k])
    return nest({"truth": World.RETURN_TO_SCHOOLING, "byq": byq, "dS": dS, "dW": dW, "wald": dW / dS, "n": len(y),
                 "full1": full1, "full3": full3, "sample1": s1, "sample3": s3, "ar": ar,
                 "corr_s_ability": float(np.corrcoef(d, S["ability"])[0, 1]), "sd_school": float(d.std())})


def size_curve(rhos=(0.2, 0.5, 0.9), mu2s=(1, 2, 4, 8, 16, 32, 64, 128), n=400, reps=4000, seed=3702):
    """The rejection rate of the nominal 5% 2SLS t-test with one instrument, by the concentration parameter mu^2
    (the expected first-stage F is about 1 + mu^2) and the endogeneity rho."""
    g = rng(seed)
    out = {}
    for rho in rhos:
        row = []
        for mu2 in mu2s:
            z = g.standard_normal((reps, n))
            v = g.standard_normal((reps, n))
            u = rho * v + math.sqrt(1 - rho * rho) * g.standard_normal((reps, n))
            pi = math.sqrt(mu2 / n)
            dd = pi * z + v
            yy = u  # beta = 0
            zz = (z * z).sum(1)
            b = (z * yy).sum(1) / (z * dd).sum(1)
            e = yy - b[:, None] * dd
            s2 = (e * e).sum(1) / (n - 1)
            pz = (z * dd).sum(1)
            se = np.sqrt(s2 * zz / (pz * pz))
            row.append(float(np.mean(np.abs(b / se) > 1.96)))
        out[str(rho)] = row
    return {"mu2": list(mu2s), "size": out}


def compute_weak():
    S, Z1, Zq, Zm, Xr = schooling_arrays()
    y, d = S["logwage"], S["school"]
    g = rng(3703)
    reps = 1000
    b1, F1, b30, F30, bl, ols = [], [], [], [], [], []
    kinds = {"interval": 0, "outside": 0, "line": 0, "empty": 0}
    for _ in range(reps):
        k = g.choice(len(y), 5000, replace=False)
        t1 = Q.tsls(y[k], d[k], Z1[k])
        b1.append(t1["beta"]), F1.append(t1["F"]), ols.append(t1["ols"])
        kinds[Q.ar_set(y[k], d[k], Z1[k])["kind"]] += 1
        t30 = Q.tsls(y[k], d[k], Zm[k], Xr[k])
        b30.append(t30["beta"]), F30.append(t30["F"])
        bl.append(Q.liml(y[k], d[k], Zm[k], Xr[k])["beta"])
    b1, b30, bl = np.array(b1), np.array(b30), np.array(bl)
    edges = np.linspace(-0.3, 0.5, 41)
    hist = lambda v: np.histogram(np.clip(v, edges[0], edges[-1] - 1e-9), edges)[0]
    return nest({"truth": World.RETURN_TO_SCHOOLING, "reps": reps, "edges": edges,
                 "h1": hist(b1), "h30": hist(b30), "hl": hist(bl),
                 "med1": float(np.median(b1)), "med30": float(np.median(b30)), "medl": float(np.median(bl)),
                 "medF1": float(np.median(F1)), "medF30": float(np.median(F30)), "med_ols": float(np.median(ols)),
                 "share_F_below_10": float(np.mean(np.array(F1) < 10)), "ar_kinds": kinds,
                 "iqr1": [float(np.percentile(b1, 25)), float(np.percentile(b1, 75))],
                 "size": size_curve()})


def compute_many():
    S, Z1, Zq, Zm, Xr = schooling_arrays()
    y, d = S["logwage"], S["school"]
    full30 = Q.tsls(y, d, Zm, Xr)
    full30_liml = Q.liml(y, d, Zm, Xr)
    # Bound, Jaeger & Baker (1995): quarters of birth drawn at random, the same thirty interactions
    g = rng(3704)
    fq = g.integers(1, 5, len(y))
    reg = S["region"]
    Zf = np.column_stack([((fq == j) & (reg == r)).astype(float) for j in (1, 2, 3) for r in range(10)])
    fake = []
    for s in range(20):
        k = g.choice(len(y), 20000, replace=False)
        fake.append(Q.tsls(y[k], d[k], Zf[k], Xr[k])["beta"])
    fake_full = Q.tsls(y, d, Zf, Xr)
    # Mendelian randomization: 40 variants for BMI, outcome SBP (both in SD units); 10 with direct effects
    g = rng(3705)
    J = 40
    beta = 0.30
    bx = np.abs(0.05 + 0.025 * g.standard_normal(J)) + 0.01
    se_bx = np.full(J, 0.003)
    alpha = np.zeros(J)
    pleio = g.choice(J, 10, replace=False)
    alpha[pleio] = 0.012 + 0.004 * g.standard_normal(10)
    se_by = np.full(J, 0.004)
    by = beta * bx + alpha + se_by * g.standard_normal(J)
    bx_obs = bx + se_bx * g.standard_normal(J)
    clean = np.setdiff1d(np.arange(J), pleio)
    ivw_clean = Q.mr_ivw(bx_obs[clean], by[clean], se_by[clean])
    ivw = Q.mr_ivw(bx_obs, by, se_by)
    egger = Q.mr_egger(bx_obs, by, se_by)
    return nest({"truth": World.RETURN_TO_SCHOOLING, "full30": full30, "full30_liml": full30_liml,
                 "fake_mean": float(np.mean(fake)), "fake_sd": float(np.std(fake)), "fake_full": fake_full,
                 "mr": {"beta": beta, "bx": bx_obs, "by": by, "pleio": pleio, "ivw": ivw, "ivw_clean": ivw_clean,
                        "egger": egger}})


# ----------------------------------------------------------------------------------------------------------------------
# Regression discontinuity
# ----------------------------------------------------------------------------------------------------------------------


def scholarship_arrays():
    R = World().scholarship
    r = R["score"]
    y = np.where(R["offer"], R["y1"], R["y0"])
    return R, r, y


def binned(x, y, lo, hi, w):
    edges = np.arange(lo, hi + w / 2, w)
    mids = (edges[:-1] + edges[1:]) / 2
    idx = np.digitize(x, edges) - 1
    m = np.full(len(mids), np.nan)
    for i in range(len(mids)):
        k = idx == i
        if k.sum() >= 5:
            m[i] = y[k].mean()
    return mids, m


def compute_rd():
    R, r, y = scholarship_arrays()
    c = World.SCHOLARSHIP_CUTOFF
    mids, means = binned(r, y, 20, 96, 1.0)
    h = Q.ik_bandwidth(r, y, c)
    conv = Q.rd(r, y, c, h, 1)
    rob = Q.rd(r, y, c, h, 2)
    narrow = Q.rd(r, y, c, 8.0, 1)
    hs = np.arange(3, 36, 1.0)
    sens = {"h": hs, "ll": [Q.rd(r, y, c, hh, 1) for hh in hs], "lq": [Q.rd(r, y, c, hh, 2) for hh in hs]}
    sens = {"h": hs, "ll_tau": [o["tau"] for o in sens["ll"]], "ll_se": [o["se"] for o in sens["ll"]],
            "lq_tau": [o["tau"] for o in sens["lq"]], "lq_se": [o["se"] for o in sens["lq"]]}
    # one study of 2,000 school-leavers
    k = np.sort(rng(3706).choice(len(r), 2000, replace=False))
    study = Q.rd_robust(r[k], y[k], c)
    near = np.abs(r - c) < 1
    # the naive comparison of scholars and others
    naive = float(y[R["offer"]].mean() - y[~R["offer"]].mean())
    return nest({"c": c, "mids": mids, "means": means, "h": h, "conv": conv, "robust": rob, "narrow": narrow,
                 "sens": sens, "study": study, "truth": World.SCHOLARSHIP_EFFECT,
                 "truth_near": float((R["y1"] - R["y0"])[near].mean()), "naive": naive, "n": len(r),
                 "share_offer": float(R["offer"].mean())})


def compute_rdvalid():
    R, r, y = scholarship_arrays()
    c = World.SCHOLARSHIP_CUTOFF
    clean = Q.mccrary(r, c, 0.5, 10.0)
    rem = Q.mccrary(R["remarked"], c, 0.5, 10.0)
    keep = (clean["mids"] >= 40) & (clean["mids"] <= 80)
    a = R["aptitude"]
    bal_clean = Q.rd(r, a, c, 10.0)
    bal_rem = Q.rd(R["remarked"], a, c, 10.0)
    # outcomes under the re-marked scores: the scholarship goes to those re-marked above the line
    offer_rem = R["remarked"] >= c
    y_rem = np.where(offer_rem, R["y1"], R["y0"])
    h = Q.ik_bandwidth(R["remarked"], y_rem, c)
    out_rem = Q.rd(R["remarked"], y_rem, c, h, 2)
    # fuzzy: take-up
    took = R["took"].astype(float)
    yt = np.where(R["took"], R["y1"], R["y0"])
    tm, tmeans = binned(r, took, 20, 96, 1.0)
    hf = Q.ik_bandwidth(r, yt, c)
    fz = Q.rd_fuzzy(r, yt, took, c, hf, p=2)
    fz1 = Q.rd_fuzzy(r, yt, took, c, hf, p=1)
    sharp_itt = Q.rd(r, yt, c, hf, 2)
    naive = float(yt[R["took"]].mean() - yt[~R["took"]].mean())
    return nest({"c": c, "clean": {k: clean[k] for k in ("theta", "se", "z", "p")},
                 "rem": {k: rem[k] for k in ("theta", "se", "z", "p")},
                 "mids": clean["mids"][keep], "dens_clean": clean["dens"][keep], "dens_rem": rem["dens"][keep],
                 "bal_clean": bal_clean, "bal_rem": bal_rem, "out_rem": out_rem, "share_bumped": float((R["remarked"] != r).mean()),
                 "take_mids": tm, "take_means": tmeans, "hf": hf, "fuzzy": fz, "fuzzy_ll": fz1, "itt": sharp_itt,
                 "naive_took": naive, "truth": World.SCHOLARSHIP_EFFECT})


# ----------------------------------------------------------------------------------------------------------------------
# Difference-in-differences
# ----------------------------------------------------------------------------------------------------------------------


def compute_did():
    ck = museum.CARD_KRUEGER
    did = (ck["NJ"][1] - ck["NJ"][0]) - (ck["PA"][1] - ck["PA"][0])
    R = World().rollout
    years, G, Y = R["years"], R["G"], R["y"]
    c09, nev = G == 2009, ~np.isfinite(G)
    path09, pathN = Y[c09].mean(0), Y[nev].mean(0)
    cf09 = R["y0"][c09].mean(0)
    pre, post = (years == 2008), (years >= 2009) & (years <= 2013)
    two = (Y[c09][:, post].mean() - Y[c09][:, pre].mean()) - (Y[nev][:, post].mean() - Y[nev][:, pre].mean())
    truth_two = float(R["tau"][c09][:, post].mean())
    cs = Q.callaway_santanna(Y, G, years)
    ev09 = [c for c in cs["cells"] if c["g"] == 2009]
    return nest({"ck": ck, "ck_did": did, "years": years, "path09": path09, "pathN": pathN, "cf09": cf09,
                 "two": float(two), "truth_two": truth_two, "n09": int(c09.sum()), "nN": int(nev.sum()),
                 "ev09": {"e": [c["e"] for c in ev09], "att": [c["att"] for c in ev09], "se": [c["se"] for c in ev09],
                          "truth": [float(R["tau"][c09][:, j].mean()) for j in range(len(years))]}})


def placebo_laws(Y0, reps, g):
    N, T = Y0.shape
    rej_ols, rej_cl, betas, s1, s2 = [], [], [], [], []
    for _ in range(reps):
        tr = np.zeros(N, bool)
        tr[g.choice(N, N // 2, replace=False)] = True
        start = g.integers(5, 16)
        D = (tr[:, None] & (np.arange(T)[None, :] >= start)).astype(float)
        o = Q.twfe(Y0, D)
        rej_ols.append(abs(o["beta"] / o["se_conv"]) > 1.96)
        rej_cl.append(abs(o["beta"] / o["se"]) > 1.96)
        betas.append(o["beta"]), s1.append(o["se_conv"]), s2.append(o["se"])
    return np.array(rej_ols), np.array(rej_cl), np.array(betas), float(np.mean(s1)), float(np.mean(s2))


def compute_didinf():
    R = World().rollout
    Y0 = R["y0"]
    ro, rc, b, se_ols, se_cl = placebo_laws(Y0, 1000, rng(3707))
    resid = Y0 - Y0.mean(1, keepdims=True) - Y0.mean(0, keepdims=True) + Y0.mean()
    ac = float(np.mean([np.corrcoef(resid[:, t], resid[:, t + 1])[0, 1] for t in range(Y0.shape[1] - 1)]))
    return nest({"reps": 1000, "rej_ols": float(ro.mean()), "rej_cl": float(rc.mean()), "sd_beta": float(b.std()),
                 "autocorr": ac, "betas": np.histogram(np.clip(b, -0.6, 0.5999), np.linspace(-0.6, 0.6, 25))[0],
                 "se_ols": se_ols, "se_cl": se_cl, "resid_towns": resid[:6]})


def compute_staggered():
    R = World().rollout
    years, G, Y = R["years"], R["G"], R["y"]
    tw = Q.twfe(Y, R["D"])
    bac = Q.bacon(Y, G, years)
    cs = Q.callaway_santanna(Y, G, years)
    im = Q.imputation(Y, G, years)
    es = Q.event_study(Y, G, years, (-6, 10))
    rel = years[None, :] - G[:, None]
    D = R["D"]
    truth_e = {int(e): float(R["tau"][D & (rel == e)].mean()) for e in range(0, 16)}
    by_kind = {}
    for o in bac:
        k = o["kind"]
        by_kind.setdefault(k, {"w": 0.0, "wx": 0.0})
        by_kind[k]["w"] += o["w"]
        by_kind[k]["wx"] += o["w"] * o["est"]
    by_kind = {k: {"w": v["w"], "est": v["wx"] / v["w"]} for k, v in by_kind.items()}
    counts = {str(c): int((G == c).sum()) for c in World.ROLLOUT_COHORTS} | {"never": int((~np.isfinite(G)).sum())}
    cohort_truth = {str(c): float(R["tau"][(G == c)[:, None] & D].mean()) for c in World.ROLLOUT_COHORTS}
    return nest({"truth": R["att"], "twfe": tw, "bacon": bac, "by_kind": by_kind, "cs": {k: cs[k] for k in ("att", "se", "ci")},
                 "cs_event": cs["event"], "imputation": im["att"], "es": es, "truth_e": truth_e, "counts": counts,
                 "slopes": World.ROLLOUT_SLOPES, "cohort_truth": cohort_truth})


def compute_honest():
    """A seeded panel (the World's draw is too noisy to show this cleanly): 150 towns adopt in 2010 and 150 never do,
    2000-2016.  The adopters were chosen because they were already improving: their untreated outcomes rise by 0.2
    points a year more than the others'.  The programme adds 1.0 point from adoption on."""
    g = rng(3714)
    years = np.arange(2000, 2017)
    N, T = 300, len(years)
    G = np.where(np.arange(N) < 150, 2010.0, np.inf)
    trend = 0.2
    a = 60 + 5 * g.standard_normal(N)
    e = np.zeros((N, T))
    e[:, 0] = 0.5 * g.standard_normal(N)
    for t in range(1, T):
        e[:, t] = 0.5 * e[:, t - 1] + 0.45 * g.standard_normal(N)
    y0 = a[:, None] + 0.1 * np.arange(T)[None, :] + e + np.where(np.isfinite(G)[:, None], trend * (years[None, :] - 2010), 0.0)
    tau = np.where(years[None, :] >= G[:, None], 1.0, 0.0)
    Y = y0 + tau
    cs = Q.callaway_santanna(Y, G, years)
    cells = [c for c in cs["cells"] if c["g"] == 2010]
    ev = np.array([c["e"] for c in cells])
    att = np.array([c["att"] for c in cells])
    se = np.array([c["se"] for c in cells])
    i0 = int(np.flatnonzero(ev == 0)[0])
    pre = ev < -1
    Ms = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]
    sd = {str(M): Q.honest_sd(ev[pre], att[pre], se[pre], att[i0], se[i0], M) for M in Ms}
    rm = {str(Mb): Q.honest_rm(att[ev < 0], att[i0], se[i0], Mb) for Mb in (0.5, 1.0, 2.0)}
    breakdown = next((float(M) for M in np.arange(0, 3, 0.01)
                      if Q.honest_sd(ev[pre], att[pre], se[pre], att[i0], se[i0], M)["ci"][0] <= 0), None)
    pre_p = float(stats.chi2.sf(np.sum((att[pre] / se[pre]) ** 2), pre.sum()))
    return nest({"e": ev, "att": att, "se": se, "trend": trend, "truth0": 1.0, "est0": float(att[i0]),
                 "se0": float(se[i0]), "naive_ci": (att[i0] - 1.645 * se[i0], att[i0] + 1.645 * se[i0]), "sd": sd,
                 "rm": rm, "Ms": Ms, "breakdown": breakdown, "pre_p": pre_p, "truth_path": tau[0] + trend * (years - 2010) - 0.0})


# ----------------------------------------------------------------------------------------------------------------------
# Synthetic control, SDID, panels, bounds
# ----------------------------------------------------------------------------------------------------------------------


def prop99_arrays():
    d = museum.prop99()
    Y = d["cigsale"]
    j = d["states"].index("California")
    T0 = int(np.flatnonzero(d["years"] == 1989)[0])
    return d, Y, j, T0


def compute_synth():
    d, Y, j, T0 = prop99_arrays()
    sc = Q.synth(Y, j, T0)
    names = [d["states"][i] for i in sc["donors"]]
    top = sorted(zip(sc["w"], names), reverse=True)
    weights = [(n, float(w)) for w, n in top if w > 0.005]
    plac = []
    for i in range(Y.shape[0]):
        s = sc if i == j else Q.synth(Y, i, T0)
        plac.append({"state": d["states"][i], "gap": s["gap"], "pre": s["rmspe_pre"], "post": s["rmspe_post"],
                     "ratio": s["ratio"]})
    ratios = np.array([p["ratio"] for p in plac])
    rank = int(1 + np.sum(ratios > ratios[j]))
    avg_cal = float(np.nanmean(Y[[k for k in range(Y.shape[0]) if k != j]], 0)[-1])
    return nest({"years": d["years"], "cal": Y[j], "synth": sc["path"], "gap": sc["gap"], "weights": weights,
                 "rmspe_pre": sc["rmspe_pre"], "ratio": sc["ratio"], "gap2000": float(sc["gap"][-1]),
                 "gap_post_mean": float(sc["gap"][T0:].mean()), "placebo": plac, "rank": rank, "n_states": Y.shape[0],
                 "p": rank / Y.shape[0], "avg_others": np.mean(np.delete(Y, j, 0), 0), "avg_others_2000": avg_cal,
                 "cal_1988": float(Y[j, T0 - 1]), "cal_2000": float(Y[j, -1])})


def compute_sdid():
    d, Y, j, T0 = prop99_arrays()
    s = Q.sdid(Y, j, T0)
    names = [d["states"][i] for i in s["donors"]]
    omega = sorted([(n, float(w)) for w, n in zip(s["omega"], names) if w > 0.005], key=lambda t: -t[1])
    w_sc = sorted([(n, float(w)) for w, n in zip(s["w_sc"], names) if w > 0.005], key=lambda t: -t[1])
    lam = [(int(y), float(l)) for y, l in zip(d["years"][:T0], s["lam"]) if l > 0.005]
    # placebo standard errors: pretend each control state was treated, using the other controls
    Yc = np.delete(Y, j, 0)
    pl = {"sdid": [], "sc": [], "did": []}
    for i in range(Yc.shape[0]):
        o = Q.sdid(Yc, i, T0)
        pl["sdid"].append(o["tau"]), pl["sc"].append(o["sc"]), pl["did"].append(o["did"])
    se = {k: float(np.std(v, ddof=1)) for k, v in pl.items()}
    return nest({"tau": s["tau"], "sc": s["sc"], "did": s["did"], "omega": omega, "w_sc": w_sc, "lam": lam,
                 "se": se, "n_omega": int(np.sum(s["omega"] > 0.005)), "zeta": s["zeta"], "years": d["years"]})


def compute_panel():
    # fixed effects remove a time-invariant confounder: pooled OLS vs within vs dummies (FWL)
    g = rng(3708)
    N, T = 300, 8
    a = g.standard_normal(N)
    x = 0.8 * a[:, None] + g.standard_normal((N, T))
    y = 1.0 * x + 2.0 * a[:, None] + g.standard_normal((N, T))
    unit = np.repeat(np.arange(N), T)
    pooled = Q.ols(y.ravel(), x.ravel()[:, None])
    fe = Q.within(y.ravel(), x.ravel()[:, None], unit)
    dummies = np.zeros((N * T, N))
    dummies[np.arange(N * T), unit] = 1.0
    lsdv = np.linalg.lstsq(np.column_stack([x.ravel(), dummies]), y.ravel(), rcond=None)[0][0]
    xbar = np.repeat(x.mean(1), T)
    mundlak = Q.ols(y.ravel(), np.column_stack([x.ravel(), xbar]), cluster=unit)
    # Nickell: y_it = rho y_i,t-1 + a_i + e_it, N = 500, T = 6 (5 usable lags)
    g = rng(3709)
    rho, N2, T2, reps = 0.5, 500, 6, 500
    fe_r, ah_r = [], []
    for _ in range(reps):
        aa = g.standard_normal(N2)
        Yp = np.zeros((N2, T2))
        Yp[:, 0] = aa / (1 - rho) + g.standard_normal(N2) / math.sqrt(1 - rho * rho)
        for t in range(1, T2):
            Yp[:, t] = rho * Yp[:, t - 1] + aa + g.standard_normal(N2)
        yv, xv = Yp[:, 1:].ravel(), Yp[:, :-1].ravel()
        uu = np.repeat(np.arange(N2), T2 - 1)
        fe_r.append(Q.within(yv, xv[:, None], uu)["b"][0])
        ah_r.append(Q.anderson_hsiao(Yp)["rho"])
    return nest({"pooled": float(pooled["b"][1]), "fe": float(fe["b"][0]), "fe_se": float(fe["se"][0]),
                 "lsdv": float(lsdv), "mundlak": float(mundlak["b"][1]), "truth": 1.0,
                 "pooled_theory": 1 + 2 * 0.8 / (0.64 + 1),
                 "nickell": {"rho": rho, "T": T2 - 1, "fe_mean": float(np.mean(fe_r)), "fe_sd": float(np.std(fe_r)),
                             "ah_mean": float(np.mean(ah_r)), "ah_sd": float(np.std(ah_r)),
                             "formula": rho + Q.nickell_bias(rho, T2 - 1),
                             "hist_fe": np.histogram(fe_r, np.linspace(0, 1, 41))[0],
                             "hist_ah": np.histogram(np.clip(ah_r, 0, 0.999), np.linspace(0, 1, 41))[0]}})


def compute_bounds():
    g = rng(3710)
    n = 4000
    t = np.zeros(n, bool)
    t[g.choice(n, n // 2, replace=False)] = True
    # always-employed (60%), employed only if trained (12%), never (28%)
    u = g.random(n)
    always, marginal = u < 0.60, (u >= 0.60) & (u < 0.72)
    w0 = np.where(always, 16 + 4 * g.standard_normal(n), 11 + 2.5 * g.standard_normal(n))
    w1 = w0 + np.where(always, 1.0, 0.0)
    emp = always | (marginal & t)
    w = np.where(t, w1, w0)
    lee = Q.lee_bounds(w, t, emp)
    naive = float(w[t & emp].mean() - w[~t & emp].mean())
    # Manski: employment (0/1) with a follow-up survey that misses 20% of the trained and 30% of the others
    resp = np.where(t, g.random(n) < 0.80, g.random(n) < 0.70)
    e = emp.astype(float)
    man = Q.manski(e, t, resp, 0.0, 1.0)
    truth_emp = float(e[t].mean() - e[~t].mean())
    resp_naive = float(e[t & resp].mean() - e[~t & resp].mean())
    return nest({"lee": lee, "naive": naive, "truth": 1.0, "share_marginal": 0.12, "emp1": float(emp[t].mean()),
                 "emp0": float(emp[~t].mean()), "manski": man, "truth_emp": truth_emp, "resp_naive": resp_naive,
                 "resp1": float(resp[t].mean()), "resp0": float(resp[~t].mean())})


# ----------------------------------------------------------------------------------------------------------------------
# The Board
# ----------------------------------------------------------------------------------------------------------------------


def compute_board():
    rows = []
    # weak instruments: thirty quarter-of-birth x region instruments, samples of 5,000
    S, Z1, Zq, Zm, Xr = schooling_arrays()
    y, d = S["logwage"], S["school"]
    b = World.RETURN_TO_SCHOOLING
    g = rng(3711)
    reps = 500
    c2, ca = [], []
    for _ in range(reps):
        k = g.choice(len(y), 5000, replace=False)
        t = Q.tsls(y[k], d[k], Zm[k], Xr[k])
        c2.append(t["ci"][0] <= b <= t["ci"][1])
        ca.append(Q.anderson_rubin(y[k], d[k], Zm[k], Xr[k], b)["p"] > 0.1)
    rows.append(Row(37, r"2SLS, \ 30 weak instruments", r"World survey: \ quarter $\times$ region, \ $n = 5{,}000$",
                    "coverage", 0.9, float(np.mean(c2)), reps))
    rows.append(Row(37, r"Anderson--Rubin set", r"World survey: \ quarter $\times$ region, \ $n = 5{,}000$",
                    "coverage", 0.9, float(np.mean(ca)), reps))
    # RD: conventional vs robust at the IK bandwidth, samples of 2,000 school-leavers
    R, r, yy = scholarship_arrays()
    c = World.SCHOLARSHIP_CUTOFF
    g = rng(3712)
    reps_rd = 1000
    cc, cr = [], []
    for _ in range(reps_rd):
        k = g.choice(len(r), 2000, replace=False)
        o = Q.rd_robust(r[k], yy[k], c)
        cc.append(o["conv"]["ci"][0] <= World.SCHOLARSHIP_EFFECT <= o["conv"]["ci"][1])
        cr.append(o["robust"]["ci"][0] <= World.SCHOLARSHIP_EFFECT <= o["robust"]["ci"][1])
    rows.append(Row(37, r"local linear RD, \ conventional CI", r"World scholarship, \ $n = 2{,}000$", "coverage", 0.9,
                    float(np.mean(cc)), reps_rd))
    rows.append(Row(37, r"robust bias-corrected RD", r"World scholarship, \ $n = 2{,}000$", "coverage", 0.9,
                    float(np.mean(cr)), reps_rd))
    # staggered adoption: fresh draws of the rollout
    g = rng(3713)
    reps_st = 500
    z = stats.norm.ppf(0.95)
    ct, ccs = [], []
    for _ in range(reps_st):
        P = World.rollout_panel(g)
        tw = Q.twfe(P["y"], P["D"])
        ct.append(abs(tw["beta"] - P["att"]) <= z * tw["se"])
        cs = Q.callaway_santanna(P["y"], P["G"], P["years"])
        ccs.append(cs["ci"][0] <= P["att"] <= cs["ci"][1])
    rows.append(Row(37, r"TWFE, \ clustered CI", r"World rollout: \ staggered, \ 200 towns", "coverage", 0.9,
                    float(np.mean(ct)), reps_st, extra="for the ATT"))
    rows.append(Row(37, r"Callaway--Sant'Anna", r"World rollout: \ staggered, \ 200 towns", "coverage", 0.9,
                    float(np.mean(ccs)), reps_st, extra="for the ATT"))
    # placebo laws
    di = load("didinf")
    rows.append(Row(37, r"DiD test, \ OLS standard errors", r"placebo laws on the World's towns", "size", 0.05,
                    di["rej_ols"], di["reps"]))
    rows.append(Row(37, r"DiD test, \ town-clustered SEs", r"placebo laws on the World's towns", "size", 0.05,
                    di["rej_cl"], di["reps"]))
    save_rows(37, rows)
    return nest({"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]})


ITEMS = {
    "iv": compute_iv, "weak": compute_weak, "many": compute_many, "rd": compute_rd, "rdvalid": compute_rdvalid,
    "did": compute_did, "didinf": compute_didinf, "staggered": compute_staggered, "honest": compute_honest,
    "synth": compute_synth, "sdid": compute_sdid, "panel": compute_panel, "bounds": compute_bounds,
    "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
