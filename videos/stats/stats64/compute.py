"""Precompute every number in Part 64 of *Statistics, Built* ("Statistics in the Age of AI").

    OMP_NUM_THREADS=1 python -m videos.stats.stats64.compute            # everything missing (a few minutes)
    python -m videos.stats.stats64.compute --force board

Results are cached in ``.cache/stats64/<name>.json``.  Everything is a seeded simulation or exact arithmetic: no real
model or benchmark is evaluated, so every number is a lesson about the method, not a claim about a system.

Items:
    leaderboard two models, 85.2% against 84.7% on 1,000 questions: intervals, McNemar, how often the ranking flips
    clustered   a benchmark of passages: iid against cluster-robust standard errors (Board)
    paired      two correlated models: unpaired against paired intervals (Board), and power against n
    multiple    the leaderboard's winner's curse with k equal models
    arena       Bradley-Terry on simulated battles: model, sandwich and bootstrap SEs; Elo's order dependence; style
    irt         a 2PL IRT fit to 60 models x 1,000 items; estimating a new model from 100 items
    holdout     Dwork et al.'s adaptive overfitting experiment: reused holdout against Thresholdout
    judges      model-judged labels: the judge's naive accuracy, the human-only interval, PPI
    collapse    a Gaussian refit to its own samples, with and without accumulation
    factual     conformal factuality: the probability that every kept claim is true, and how many are kept
    watermark   green-list detection: power against length, entropy and edits
    sbi         amortized posteriors: coverage with in-sample against held-out calibration
    diffusion   the probability-flow sampler with the true, the empirical and a smoothed empirical score
    market      a two-sided market: the naive A/B estimate against the global effect, and market-level randomization
    board       Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats.board import Row, save_rows
from . import checked as E

CACHE = Cache("stats64")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def nest(obj):
    if isinstance(obj, dict):
        return {k: nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return nest(obj.tolist())
    if isinstance(obj, (np.floating,)):
        return float(obj) if math.isfinite(float(obj)) else None
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if isinstance(obj, float) and not math.isfinite(obj):
        return None
    return obj


def compute_leaderboard():
    r=rng(6401);n=1000
    # Explicit pedagogical 2x2 table, not a searched-for stochastic realization.
    a=np.array([1]*776+[1]*76+[0]*71+[0]*77,float)
    b=np.array([1]*776+[0]*76+[1]*71+[0]*77,float)
    pc=E.paired_compare(a,b);mc=E.mcnemar(a,b);sa,sb=E.mean_se(a),E.mean_se(b)
    flips=ties=0;reps=4000
    for _ in range(reps):
        x,y=E.correlated_pair(n,.852,.847,.8,r);delta=x.sum()-y.sum();flips+=delta<0;ties+=delta==0
    return dict(n=n,acc_a=float(a.mean()),acc_b=float(b.mean()),se_a=sa['se'],se_b=sb['se'],paired=pc,mcnemar=mc,flip=flips/reps,reps=reps,ties=ties,flip_mcse=np.sqrt((flips/reps)*(1-flips/reps)/reps),scope='Constructed headline table; separate seeded fresh-benchmark experiment with latent probit coefficient .8.')



def compute_clustered():
    r = rng(6402)
    G, m, acc, tau = 100, 10, 0.8, 1.2
    reps = 2000
    cov_n = cov_c = 0
    se_n, se_c, means = [], [], []
    exact=E.clustered_truth(acc,tau,m,G)
    truth=exact['mean']
    for _ in range(reps):
        b = E.clustered_benchmark(G, m, acc, tau, r)
        a1, a2 = E.mean_se(b["x"]), E.cluster_se(b["x"], b["cluster"])
        cov_n += abs(a1["mean"] - truth) <= 1.96 * a1["se"]
        cov_c += abs(a2["mean"] - truth) <= 1.96 * a2["se"]
        se_n.append(a1["se"])
        se_c.append(a2["se"])
        means.append(a1["mean"])
    sdm = float(np.std(means,ddof=1))
    # the intraclass correlation implied: deff = (se_c / se_n)^2 = 1 + (m - 1) icc
    deff = exact["deff"]
    return {"G": G, "m": m, "acc": acc, "tau": tau, "truth": truth, "reps": reps, "cov_naive": cov_n / reps,
            "cov_cluster": cov_c / reps, "se_naive": float(np.mean(se_n)), "se_cluster": float(np.mean(se_c)), "sd_mean": sdm,
            "deff": float(deff), "icc": exact["icc"], "true_sd": exact["sd"], "mcse_naive": np.sqrt((cov_n/reps)*(1-cov_n/reps)/reps), "mcse_cluster": np.sqrt((cov_c/reps)*(1-cov_c/reps)/reps)}


def compute_paired():
    r = rng(6403)
    n, reps = 1000, 2000
    da = 0.852 - 0.847
    cov_u = cov_p = 0
    wu, wp, corr = [], [], []
    truth = da
    for _ in range(reps):
        a, b = E.correlated_pair(n, 0.852, 0.847, 0.8, r)
        pc = E.paired_compare(a, b)
        cov_u += pc["unpaired"][0] <= truth <= pc["unpaired"][1]
        cov_p += pc["paired"][0] <= truth <= pc["paired"][1]
        wu.append(pc["se_unpaired"])
        wp.append(pc["se_paired"])
        corr.append(pc["corr"])
    # power to detect a 2-point gap at 5%: paired (McNemar-like z) against unpaired, over n
    ns = [250, 500, 1000, 2000, 4000, 8000]
    pw = []
    for nn in ns:
        hu = hp = 0
        for _ in range(400):
            a, b = E.correlated_pair(nn, 0.86, 0.84, 0.8, r)
            pc = E.paired_compare(a, b)
            hu += pc["unpaired"][0] > 0 or pc["unpaired"][1] < 0
            hp += pc["paired"][0] > 0 or pc["paired"][1] < 0
        pw.append({"n": nn, "unpaired": hu / 400, "paired": hp / 400, "reps": 400, "mcse_paired": np.sqrt((hp/400)*(1-hp/400)/400)})
    return {"n": n, "reps": reps, "truth": truth, "design_gap": da, "cov_unpaired": cov_u / reps, "cov_paired": cov_p / reps,
            "se_unpaired": float(np.mean(wu)), "se_paired": float(np.mean(wp)), "corr": float(np.mean(corr)), "power": pw, "mcse_paired": np.sqrt((cov_p/reps)*(1-cov_p/reps)/reps), "mcse_unpaired": np.sqrt((cov_u/reps)*(1-cov_u/reps)/reps)}


def compute_multiple():
    r = rng(6404)
    ks = [1, 2, 5, 10, 20, 50, 100]
    rows = [{"k": k, **E.winners_curse(k, 1000, 0.85, 4000, r)} for k in ks]
    return {"n": 1000, "acc": 0.85, "rows": rows}


def compute_arena():
    r = rng(6405)
    theta = np.array([0.0, 0.15, 0.3, 0.35, 0.5, 0.7, 0.75, 1.0])
    K, n = len(theta), 6000
    s = E.simulate_battles(theta, n, r)
    f = E.bt_fit(s["i"], s["j"], s["y"], K)
    boot = E.bt_bootstrap(s["i"], s["j"], s["y"], K, 300, r)
    # coverage of the sandwich interval for theta_7 - theta_6 over fresh arenas
    cov = 0
    reps = 300
    for _ in range(reps):
        t = E.simulate_battles(theta, n, r)
        g = E.bt_fit(t["i"], t["j"], t["y"], K, ref=6)
        cov += abs(g["theta"][7] - (theta[7] - theta[6])) <= 1.96 * g["se_sandwich"][7]
    # Elo: the same battles in 50 random orders
    elos = []
    for _ in range(50):
        o = r.permutation(n)
        elos.append(E.elo(s["i"][o], s["j"][o], s["y"][o], K, 4.0) * math.log(10) / 400)
    elos = np.array(elos)
    # style control: model 3 writes longer answers, and voters like length
    mean_len = np.zeros(K)
    mean_len[3] = 1.0
    gamma = 0.6
    i, j = s["i"], s["j"]
    sty = ((mean_len[i] + 0.5 * r.standard_normal(n)) - (mean_len[j] + 0.5 * r.standard_normal(n)))[:, None]
    y = (r.random(n) < 1 / (1 + np.exp(-(theta[i] - theta[j] + gamma * sty[:, 0])))).astype(float)
    raw = E.bt_fit(i, j, y, K)["theta"]
    ctl = E.bt_style_fit(i, j, y, K, sty)
    return {"theta": theta, "n": n, "fit": f["theta"], "se": f["se"], "se_sandwich": f["se_sandwich"],
            "se_boot": boot.std(0,ddof=1), "cov_sandwich": cov / reps, "reps": reps, "elo_mean": elos.mean(0), "elo_sd": elos.std(0),
            "elo_lo": elos.min(0), "elo_hi": elos.max(0), "style_raw": raw, "style_ctl": ctl["theta"], "gamma": float(ctl["gamma"][0]),
            "gamma_true": gamma, "covariance": f["cov_sandwich"], "rank_one": E.rank_one_set(f["theta"], f["cov_sandwich"]), "score_max": f["score_max"], "mcse_coverage": np.sqrt((cov/reps)*(1-cov/reps)/reps)}


def compute_irt():
    r = rng(6406)
    M, J = 60, 1000
    th = r.standard_normal(M)
    a = np.exp(r.normal(0.6, 0.4, J))
    b = r.normal(-0.5, 1.2, J)
    P = 1 / (1 + np.exp(-a[None] * (th[:, None] - b[None])))
    R = (r.random((M, J)) < P).astype(float)
    fit = E.fit_2pl(R, iters=25)
    corr_a = float(np.corrcoef(fit["a"], a)[0, 1])
    corr_b = float(np.corrcoef(fit["b"], b)[0, 1])
    # new models: true accuracy on the 1,000 items; estimate from 100 random items by the raw mean and by IRT
    err_raw, err_irt, err_anchor = [], [], []
    # anchors: 100 items spread over the fitted difficulties, the most discriminating item in each of 100 strata
    order = np.argsort(fit["b"])
    anchors = np.array([blk[np.argmax(fit["a"][blk])] for blk in np.array_split(order, 100)])
    for _ in range(300):
        t = r.standard_normal()
        p = 1 / (1 + np.exp(-a * (t - b)))
        resp = (r.random(J) < p).astype(float)
        full = resp.mean()
        k = r.choice(J, 100, replace=False)
        err_raw.append(resp[k].mean() - full)
        tt = E.irt_ability(resp[k], fit["a"][k], fit["b"][k])
        err_irt.append(E.irt_accuracy(tt, fit["a"], fit["b"]) - full)
        ta = E.irt_ability(resp[anchors], fit["a"][anchors], fit["b"][anchors])
        err_anchor.append(E.irt_accuracy(ta, fit["a"], fit["b"]) - full)
    # informativeness: Fisher information of each item at ability 0
    p0 = 1 / (1 + np.exp(-fit["a"] * (0 - fit["b"])))
    info = fit["a"] ** 2 * p0 * (1 - p0)
    return {"M": M, "J": J, "corr_a": corr_a, "corr_b": corr_b, "rmse_raw": float(np.sqrt(np.mean(np.square(err_raw)))),
            "rmse_irt": float(np.sqrt(np.mean(np.square(err_irt)))), "rmse_anchor": float(np.sqrt(np.mean(np.square(err_anchor)))),
            "err_raw": err_raw, "err_irt": err_irt, "err_anchor": err_anchor,
            "frac_easy": float(np.mean(R.mean(0) > 0.95)), "info_top10": float(np.sort(info)[-100:].sum() / info.sum()),
            "theta_corr": float(np.corrcoef(fit["theta"], th)[0, 1]), "fit_diagnostics": {k:fit[k] for k in ["objective","projected_score","iterations","scope"]}}


def compute_holdout():
    r = rng(6407)
    ks = [10, 25, 50, 100, 200, 300, 500]
    runs = 5
    out = {}
    for m in ("reuse", "thresholdout"):
        h, f = [], []
        for run in range(runs):
            o = E.adaptive_overfit(3000, 3000, ks, rng(640700+run), m, T=0.04, sigma=0.01)
            h.append(o["holdout"])
            f.append(o["fresh"])
        out[m] = {"holdout": np.mean(h, 0), "fresh": np.mean(f, 0)}
    return {"n": 3000, "d": 3000, "ks": ks, "runs": runs, "scope": "Paired Gaussian-feature simulation of a noisy-threshold heuristic, not budgeted Thresholdout or a DP certificate; correlations are unbounded.", **out}


def compute_judges():
    r = rng(6408)
    N, n, reps = 5000, 200, 2000
    true_acc = 0.70
    sens, spec = 0.95, 0.80
    cov = {"judge": 0, "human": 0, "ppi": 0}
    wid = {"judge": [], "human": [], "ppi": []}
    est = {"judge": [], "human": [], "ppi": []}
    for _ in range(reps):
        t = (r.random(N + n) < true_acc).astype(float)
        f = E.judged_labels(t, sens, spec, r)
        res = {"judge": E.wald_ci(f[:N]), "human": E.wald_ci(t[N:]), "ppi": E.ppi_mean_ci(t[N:], f[N:], f[:N])}
        for k, v in res.items():
            cov[k] += v["ci"][0] <= true_acc <= v["ci"][1]
            wid[k].append(v["ci"][1] - v["ci"][0])
            est[k].append(v["est"])
    bias = true_acc * sens + (1 - true_acc) * (1 - spec) - true_acc
    return {"N": N, "n": n, "reps": reps, "true": true_acc, "sens": sens, "spec": spec, "judge_bias": bias,
            "mcse_cov": {k: np.sqrt((v/reps)*(1-v/reps)/reps) for k,v in cov.items()}, "cov": {k: v / reps for k, v in cov.items()}, "width": {k: float(np.mean(v)) for k, v in wid.items()},
            "mean": {k: float(np.mean(v)) for k, v in est.items()}}


def compute_collapse():
    r = rng(6409)
    n, T = 20, 300
    rep = E.gaussian_collapse(n, T, 400, r)
    acc = E.gaussian_collapse(n, T, 100, r, accumulate=True)
    p = rep["paths"]
    q = acc["paths"]
    keep = list(range(0, T + 1, 5))
    return {"n": n, "T": T, "t": keep, "median": np.median(p, 0)[keep], "q10": np.quantile(p, 0.1, 0)[keep],
            "q90": np.quantile(p, 0.9, 0)[keep], "expected": rep["expected"][keep], "drift": rep["drift"],
            "acc_median": np.median(q, 0)[keep], "acc_q10": np.quantile(q, 0.1, 0)[keep], "acc_q90": np.quantile(q, 0.9, 0)[keep],
            "examples": p[:6][:, keep], "below_1pct": float(np.mean(p[:, -1] < 0.01)), "initial_scope": "Both initial fitted moments mu0=0, variance0=1; accumulation begins with a standardized initial sample.", "reps": 400, "acc_reps": 100}


def compute_factual():
    r = rng(6410)
    alphas = [0.05, 0.1, 0.2, 0.3]
    rows = []
    for al in alphas:
        safe, kept, run_safe, run_kept = [], [], [], []
        for _ in range(300):
            cs, ct = E.claim_responses(500, 8, 0.8, 2.0, r)
            ts, tt = E.claim_responses(200, 8, 0.8, 2.0, r)
            o = E.conformal_factuality(cs, ct, ts, al)
            one_safe=[];one_kept=[]
            for k, tr in zip(o["kept"], tt):
                safe.append(all(t for kk, t in zip(k, tr) if kk));one_safe.append(safe[-1])
                kept.append(np.mean(k));one_kept.append(kept[-1])
            run_safe.append(np.mean(one_safe));run_kept.append(np.mean(one_kept))
        rows.append({"alpha": al, "safe": float(np.mean(safe)), "kept": float(np.mean(kept)), "mcse_safe": float(np.std(run_safe,ddof=1)/np.sqrt(300)), "mcse_kept": float(np.std(run_kept,ddof=1)/np.sqrt(300)), "calibrations": 300, "tests_per_calibration": 200})
    base = .8**8
    return {"rows": rows, "claims": 8, "p_true": 0.8, "unfiltered_safe": base}


def compute_watermark():
    Ts = [5, 10, 20, 40, 80, 160, 320]
    g, dl, z = 0.25, 2.0, 4.0
    out = {"T": Ts, "gamma": g, "delta": dl, "z": z, "green": E.green_prob(g, dl),
           "full": [E.watermark_power(T, g, dl, z) for T in Ts],
           "low_entropy": [E.watermark_power(T, g, dl, z, entropy_frac=0.4) for T in Ts],
           "edited": [E.watermark_power(T, g, dl, z, edit_frac=0.5) for T in Ts],
           "fpr": float(stats.norm.sf(z))}
    # the exact false-positive rate of the z > 4 rule for human text, by T
    out["exact_fpr"] = [float(stats.binom.sf((math.floor(g * T + z * math.sqrt(T * g * (1 - g))) + 1) - 1, T, g)) for T in Ts]
    return out


def compute_sbi():
    r=rng(6411);rows=[]
    for n in [30,60,120,250,500,1000,4000]:
        draws=[E.sbi_comparison(n,8,.9,2000,r) for _ in range(20)]
        row=dict(n_sim=n)
        for key in ['insample','heldout','exact']:
            vals=np.array([d[key] for d in draws]);row[key]=vals.mean();row[key+'_mcse']=vals.std(ddof=1)/np.sqrt(20)
        rows.append(row)
    return dict(rows=rows,level=.9,p_feat=8,scope='Prior-predictive coverage, paired same fitted mean and test draws; held-out residual RMS is a heuristic, not exact posterior calibration.')



def compute_diffusion():
    r = rng(6412)
    mus, s, w = np.array([-2.0, 1.5]), 0.5, np.array([0.4, 0.6])
    comp = r.random(20) < w[1]
    train = np.where(comp, mus[1], mus[0]) + s * r.standard_normal(20)
    sig = np.geomspace(8, 0.01, 200)
    component_u=r.random(4000);noise0=r.standard_normal(4000);noise1=r.standard_normal(4000)
    def initial(centers,base_sd,weights):
        ids=np.searchsorted(np.cumsum(weights),component_u,side='right')
        return np.asarray(centers)[ids]+base_sd*noise0+sig[0]*noise1
    specs=[('true',mus,s,w),('emp',train,0.,np.full(20,.05)),('smooth',train,.35,np.full(20,.05))]
    samples={};refinement={}
    for name,centers,spread,weights in specs:
        fn=lambda x,t:E.mixture_score(x,t,centers,spread,weights)
        x0=initial(centers,spread,weights)
        coarse=E.probability_flow(fn,sig,4000,r,initial=x0)
        fine=E.probability_flow(fn,np.geomspace(8,.01,400),4000,r,initial=x0)
        samples[name]=fine;refinement[name]=float(np.sqrt(np.mean((fine-coarse)**2)))
    true,emp,smo=samples['true'],samples['emp'],samples['smooth']

    def nearest(x):
        return np.min(np.abs(x[:, None] - train[None]), 1)
    xs = np.linspace(-5, 5, 400)

    def kde(v, h=0.12):
        return np.exp(-0.5 * ((xs[:, None] - v[None]) / h) ** 2).sum(1) / (len(v) * h * math.sqrt(2 * math.pi))
    dens = w[0] * stats.norm.pdf(xs, mus[0], s) + w[1] * stats.norm.pdf(xs, mus[1], s)
    # Tweedie at one noise level: the denoiser of the noised mixture
    y = np.linspace(-5, 5, 200)
    tw = E.tweedie(y, 1.0, E.mixture_score(y, 1.0, mus, s, w))
    return {"train": train, "xs": xs, "density": dens, "kde_true": kde(true), "kde_emp": kde(emp), "kde_smooth": kde(smo),
            "near_emp": float(np.median(nearest(emp))), "near_smooth": float(np.median(nearest(smo))),
            "near_true": float(np.median(nearest(true))), "y": y, "tweedie": tw, "ode_rms_refinement": refinement, "initialization": "exact noised target mixture per score; common uniforms and normals", "endpoint_sigma": .01, "steps": 399}


def compute_market():
    r = rng(6413)
    n, supply, base, lift = 4000, 1800, 0.4, 0.5
    naive, glob, mk = [], [], []
    for _ in range(300):
        o = E.market_ab(n, supply, base, lift, 0.5, r)
        naive.append(o["naive"])
        glob.append(o["global"])
        mk.append(E.market_randomized(20, n, supply, base, lift, r))
    return {"n": n, "supply": supply, "base": base, "lift": lift, "naive": float(np.mean(naive)), "naive_sd": float(np.std(naive)),
            "global": float(np.mean(glob)), "global_sd": float(np.std(glob)), "markets": float(np.mean(mk)), "markets_sd": float(np.std(mk)),
            "n_markets": 20, "reps": 300, "naive_mcse": np.std(naive,ddof=1)/np.sqrt(300), "global_mcse": np.std(glob,ddof=1)/np.sqrt(300), "markets_mcse": np.std(mk,ddof=1)/np.sqrt(300), "allocation": "weighted random sampling among wanting buyers, proportional to treatment-specific demand"}


def compute_board():
    c, p = load("clustered"), load("paired")
    rows = [Row(64, r"iid error bar on a benchmark", rf"{c['G']} passages $\times$ {c['m']} questions", "coverage", 0.95, c["cov_naive"], c["reps"]),
            Row(64, r"cluster-robust error bar", rf"{c['G']} passages $\times$ {c['m']} questions", "coverage", 0.95, c["cov_cluster"], c["reps"]),
            Row(64, r"unpaired interval for a model difference", r"two models, \ same 1{,}000 questions", "coverage", 0.95, p["cov_unpaired"], p["reps"]),
            Row(64, r"paired interval for a model difference", r"two models, \ same 1{,}000 questions", "coverage", 0.95, p["cov_paired"], p["reps"])]
    save_rows(64, rows)
    return {"rows": [asdict(x) | {"verdict": x.verdict, "se": x.se} for x in rows]}


ITEMS = {
    "leaderboard": compute_leaderboard, "clustered": compute_clustered, "paired": compute_paired, "multiple": compute_multiple,
    "arena": compute_arena, "irt": compute_irt, "holdout": compute_holdout, "judges": compute_judges, "collapse": compute_collapse,
    "factual": compute_factual, "watermark": compute_watermark, "sbi": compute_sbi, "diffusion": compute_diffusion,
    "market": compute_market, "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
