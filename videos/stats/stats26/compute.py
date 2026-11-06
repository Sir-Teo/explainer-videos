"""Precompute every number in Part 26 of *Statistics, Built* ("Bayesian Data Analysis").

    python -m videos.stats.stats26.compute            # everything missing (a few minutes)
    python -m videos.stats.stats26.compute --force board

Results are cached in ``.cache/stats26/<name>.json``.  The eight schools and the PEAR data are the Museum's; schools,
doctor visits and health are the World's; the rest are seeded simulations.

Items:
    schools     the eight schools: no pooling, complete pooling, and the hierarchical posterior on a grid
    priors      tau's posterior under four priors, for all eight schools and for three; an improper posterior
    jeffreys    Jeffreys's prior for a proportion: invariance under reparametrization
    conjugate   Diaconis-Ylvisaker: Poisson-gamma posterior means as weighted averages, for the World's doctor visits
    bvm         Bernstein-von Mises for a Poisson rate: posterior vs sampling distribution; exact coverage against n
    bf          a normal mean's Bayes factor against the prior scale (Bartlett), and BIC
    lindley     the PEAR data; BF at fixed p = 0.05 as n grows; the Sellke-Bayarri-Berger bound
    occam       the evidence for polynomial degree (MacKay), with the Occam factor
    decision    adopt coaching? expected utility, EVPI and EVSI from the eight schools' posterior
    ppc         posterior predictive checks: the eight schools, and Poisson vs negative binomial for doctor visits
    priorpred   prior predictive checks for a logistic regression: N(0, 10^2) vs N(0, 1) priors
    sbc         simulation-based calibration of a correct and a buggy posterior
    dp          the Chinese restaurant process and stick-breaking
    board       Coverage Board rows: credible intervals for 8 of the World's schools
"""

from __future__ import annotations

from dataclasses import asdict

import numpy as np
from scipy import special, stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import bayes as B
from explainer.stats.world import World

CACHE = Cache("stats26")
load = CACHE.load
W = World()
TAU = np.linspace(0, 40, 4001)


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


def compute_schools():
    lab, y, s = museum.eight_schools()
    w = 1 / s ** 2
    pooled = float(np.sum(w * y) / w.sum())
    pooled_se = float(1 / np.sqrt(w.sum()))
    Q = float(np.sum(w * (y - pooled) ** 2))
    h = B.hier_normal(y, s, TAU)
    mean, var = h.cond_theta()
    d = h.draws(200_000, rng(1981))
    th = d["theta"]
    q = lambda a, p: np.percentile(a, p, axis=0)  # noqa: E731
    best = np.bincount(np.argmax(th, 1), minlength=8) / len(th)
    keep = np.linspace(0, len(TAU) - 1, 401).astype(int)
    return nest({"labels": lab, "y": y, "sigma": s, "pooled": pooled, "pooled_se": pooled_se, "Q": Q,
                 "p_Q": float(stats.chi2.sf(Q, 7)), "tau": TAU[keep], "post_tau": h.post_tau[keep],
                 "cond_mean": mean[keep], "cond_sd": np.sqrt(var[keep]), "mu_hat": h.mu_hat[keep],
                 "theta_mean": th.mean(0), "theta_med": np.median(th, 0), "theta_lo": q(th, 2.5), "theta_hi": q(th, 97.5),
                 "mu_mean": float(d["mu"].mean()), "mu_lo": float(np.percentile(d["mu"], 2.5)), "mu_hi": float(np.percentile(d["mu"], 97.5)),
                 "tau_med": float(np.median(d["tau"])), "tau_lo": float(np.percentile(d["tau"], 2.5)),
                 "tau_hi": float(np.percentile(d["tau"], 97.5)), "tau_mode": float(TAU[np.argmax(h.post_tau)]),
                 "p_A_gt_C": float(np.mean(th[:, 0] > th[:, 2])), "p_best": best,
                 "draws_theta": th[:20], "draws_tau": d["tau"][:20], "draws_mu": d["mu"][:20],
                 "tau_hist": np.histogram(d["tau"], np.linspace(0, 40, 41), density=True)[0]})


def compute_priors():
    lab, y, s = museum.eight_schools()
    priors = {
        "uniform": lambda t: np.zeros_like(t),
        "halfcauchy": lambda t: stats.halfcauchy.logpdf(t, scale=25),
        # inverse-gamma(eps, eps) on tau^2, as a density for tau: p(tau) = p(tau^2) 2 tau
        "ig1": lambda t: stats.invgamma.logpdf(np.maximum(t, 1e-6) ** 2, 1, scale=1) + np.log(2 * np.maximum(t, 1e-6)),
        "ig001": lambda t: stats.invgamma.logpdf(np.maximum(t, 1e-6) ** 2, 0.001, scale=0.001) + np.log(2 * np.maximum(t, 1e-6)),
    }
    grid = np.linspace(0, 40, 801)
    gfine = np.concatenate([np.geomspace(1e-4, 0.05, 200), np.linspace(0.05, 40, 4000)[1:]])
    out = {"tau": grid}
    for subset, idx in (("eight", slice(None)), ("three", slice(0, 3))):
        out[subset] = {}
        for k, f in priors.items():
            h = B.hier_normal(y[idx], s[idx], gfine, f)
            dens = np.interp(grid, gfine, h.post_tau)
            cdf = np.cumsum(h.post_tau * np.gradient(gfine))
            cdf /= cdf[-1]
            out[subset][k] = {"dens": dens, "median": float(np.interp(0.5, cdf, gfine)),
                              "q95": float(np.interp(0.95, cdf, gfine)), "prior": np.exp(f(np.maximum(grid, 1e-3)))}
    # improper: p(log tau) flat, i.e. p(tau) ∝ 1/tau; the marginal posterior of log tau tends to a constant at -inf
    lt = np.linspace(-12, 4, 400)
    h = B.hier_normal(y, s, np.exp(lt))  # flat in tau, evaluated on exp grid; converting: p(log tau) = p(tau) tau
    like = h.post_tau  # ∝ likelihood in tau (flat prior)
    out["improper"] = {"logtau": lt, "dens_logtau": like / like.max()}
    return nest(out)


def compute_jeffreys():
    p = np.linspace(0.001, 0.999, 500)
    eta = np.linspace(-6, 6, 500)
    # uniform on p, viewed on the log-odds scale: density e^eta / (1 + e^eta)^2; uniform on eta is not normalizable
    jef_p = stats.beta.pdf(p, 0.5, 0.5)
    jef_eta = np.sqrt(special.expit(eta) * (1 - special.expit(eta))) / np.pi  # Beta(1/2,1/2) on the logit scale
    unif_eta = special.expit(eta) * (1 - special.expit(eta))
    return nest({"p": p, "eta": eta, "jef_p": jef_p, "jef_eta": jef_eta, "unif_eta": unif_eta})


def compute_conjugate():
    v = W.visits["visits"]
    ad = np.flatnonzero(v >= 0)
    g = rng(1979)
    a0, b0 = 4.0, 1.0  # prior mean 4 visits, worth one adult
    rows = []
    truth = float(v[ad].mean())
    for n in (1, 5, 25, 100, 1000):
        smp = g.choice(ad, n, replace=False)
        xb = float(v[smp].mean())
        a, b = B.gamma_update(a0, b0, float(v[smp].sum()), float(n))
        w = n / (n + b0)
        rows.append({"n": n, "xbar": xb, "post_mean": a / b, "weight": w, "lo": float(stats.gamma.ppf(0.025, a, scale=1 / b)),
                     "hi": float(stats.gamma.ppf(0.975, a, scale=1 / b))})
    return nest({"rows": rows, "a0": a0, "b0": b0, "truth": truth})


def compute_bvm():
    lam = 2.0
    out = {"lam": lam, "panels": []}
    g = rng(1949)
    for n in (3, 30, 300):
        x = g.poisson(lam, n)
        a, b = 0.5 + x.sum(), n  # Jeffreys prior Gamma(1/2, 0)
        mle = x.mean()
        grid = np.linspace(max(mle - 5 * np.sqrt(max(mle, 0.3) / n), 1e-3), mle + 5 * np.sqrt(max(mle, 0.3) / n), 300)
        post = stats.gamma.pdf(grid, a, scale=1 / b)
        approx = stats.norm.pdf(grid, mle, np.sqrt(mle / n))
        tv = 0.5 * np.trapezoid(np.abs(post - approx), grid)
        out["panels"].append({"n": n, "grid": grid, "post": post, "approx": approx, "mle": mle, "tv": float(tv)})
    # exact frequentist coverage of the 95% equal-tailed Jeffreys interval at lam = 2, as n grows
    ns = np.arange(1, 101)
    cov = []
    for n in ns:
        k = np.arange(0, int(lam * n + 12 * np.sqrt(lam * n) + 30))
        lo = stats.gamma.ppf(0.025, k + 0.5, scale=1 / n)
        hi = stats.gamma.ppf(0.975, k + 0.5, scale=1 / n)
        cov.append(float(np.sum(stats.poisson.pmf(k, lam * n) * ((lo <= lam) & (lam <= hi)))))
    out["ns"], out["coverage"] = ns, cov
    return nest(out)


def compute_bf():
    n, sigma, z = 50, 1.0, 2.5
    xbar = z * sigma / np.sqrt(n)
    taus = np.geomspace(0.01, 1000, 300)
    bf = np.array([B.bf01_normal(xbar, n, sigma, t) for t in taus])
    k = int(np.argmin(bf))
    bic01 = float(np.exp(0.5 * (np.log(n) - z ** 2)))  # BIC approximation to BF_01 (unit-information prior)
    unit = B.bf01_normal(xbar, n, sigma, sigma)
    return nest({"n": n, "z": z, "p": float(2 * stats.norm.sf(z)), "taus": taus, "bf01": bf, "tau_min": float(taus[k]),
                 "bf_min": float(bf[k]), "bic01": bic01, "unit01": unit})


def compute_lindley():
    n, s = museum.PEAR_N, museum.PEAR_S
    phat = s / n
    z = (s - n / 2) / np.sqrt(n / 4)
    p = float(2 * stats.norm.sf(z))
    # BF_01 with a uniform prior on p under H1: m1 = 1/(n+1) (with the binomial coefficient), m0 = C(n,s) 2^-n
    log_m0 = special.gammaln(n + 1) - special.gammaln(s + 1) - special.gammaln(n - s + 1) - n * np.log(2)
    log_m1 = -np.log(n + 1)
    bf01 = float(np.exp(log_m0 - log_m1))
    post_h0 = bf01 / (1 + bf01)
    ns = np.geomspace(10, 1e8, 60)
    z05 = 1.959964
    bf_n = [B.bf01_normal(z05 / np.sqrt(m), int(m), 1.0, 1.0) for m in ns]
    ps = np.array([0.1, 0.05, 0.01, 0.005, 0.001])
    sbb = B.sbb_bound(ps)
    return nest({"n": n, "s": s, "phat": phat, "z": float(z), "p": p, "bf01": bf01, "post_h0": post_h0,
                 "ns": ns, "bf_n": bf_n, "ps": ps, "sbb": sbb, "min_post": sbb / (1 + sbb)})


def compute_occam():
    g = rng(1992)
    n = 20
    x = np.sort(g.uniform(-1, 1, n))
    f = lambda t: 0.5 - 1.2 * t + 0.4 * t ** 2 + 1.5 * t ** 3  # noqa: E731
    sigma = 0.25
    y = f(x) + sigma * g.normal(size=n)
    alpha = 1.0
    degs = list(range(0, 9))
    ev, fit_ll, fits = [], [], []
    xx = np.linspace(-1, 1, 200)
    for dg in degs:
        X = np.vander(x, dg + 1, increasing=True)
        ev.append(B.blr_log_evidence(X, y, alpha, sigma))
        m, S = B.blr_posterior(X, y, alpha, sigma)
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        fit_ll.append(float(np.sum(stats.norm.logpdf(y, X @ beta, sigma))))
        fits.append(np.vander(xx, dg + 1, increasing=True) @ m)
    return nest({"x": x, "y": y, "xx": xx, "truth": f(xx), "degs": degs, "log_ev": ev, "max_ll": fit_ll, "fits": fits,
                 "sigma": sigma, "alpha": alpha, "best": int(degs[int(np.argmax(ev))])})


def compute_decision():
    lab, y, s = museum.eight_schools()
    h = B.hier_normal(y, s, TAU)
    d = h.draws(400_000, rng(2620))
    g = rng(2621)
    theta_new = d["mu"] + d["tau"] * g.standard_normal(len(d["mu"]))
    cost = 5.0  # points of SAT the programme must deliver to repay its cost
    gain = theta_new - cost
    eu_adopt = float(gain.mean())
    evpi = float(np.mean(np.maximum(gain, 0)) - max(eu_adopt, 0.0))
    # EVSI: run one more experiment in the new school with SE 10, then decide
    se = 10.0
    ynew = theta_new + se * g.standard_normal(len(theta_new))
    # posterior mean of theta_new given ynew, by binning ynew (pre-posterior analysis by simulation)
    bins = np.quantile(ynew, np.linspace(0, 1, 201))
    k = np.clip(np.searchsorted(bins, ynew) - 1, 0, 199)
    cond = np.bincount(k, gain, 200) / np.bincount(k, minlength=200)
    evsi = float(np.mean(np.maximum(cond[k], 0)) - max(eu_adopt, 0.0))
    return nest({"cost": cost, "p_exceed": float(np.mean(theta_new > cost)), "mean_new": float(theta_new.mean()),
                 "sd_new": float(theta_new.std()), "eu_adopt": eu_adopt, "evpi": evpi, "evsi": evsi, "se": se,
                 "hist": np.histogram(theta_new, np.linspace(-40, 50, 46), density=True)[0], "edges": np.linspace(-40, 50, 46)})


def compute_ppc():
    lab, y, s = museum.eight_schools()
    h = B.hier_normal(y, s, TAU)
    g = rng(1984)
    d = h.draws(20_000, g)
    yrep = d["theta"] + s[None, :] * g.standard_normal(d["theta"].shape)
    T = {"max": (yrep.max(1), y.max()), "min": (yrep.min(1), y.min()), "sd": (yrep.std(1), y.std()),
         "range": (yrep.max(1) - yrep.min(1), y.max() - y.min())}
    school = {k: {"p": float(np.mean(a >= b)), "obs": float(b), "hist": np.histogram(a, 40)[0], "edges": np.histogram(a, 40)[1]}
              for k, (a, b) in T.items()}
    # doctor visits: Poisson (gamma posterior on the mean) vs negative binomial (posterior by normal approximation)
    v = W.visits["visits"]
    ad = np.flatnonzero(v >= 0)
    smp = rng(24).choice(ad, 500, replace=False)
    x = v[smp]
    n = len(x)
    lam = rng(25).gamma(0.5 + x.sum(), 1 / n, 4000)
    zero_obs = float(np.mean(x == 0))
    zp = np.array([np.mean(rng(100 + i).poisson(l, n) == 0) for i, l in enumerate(lam[:2000])])
    # NB by moments with parameter uncertainty from a parametric bootstrap
    m, v2 = x.mean(), x.var(ddof=1)
    k_hat = m ** 2 / max(v2 - m, 1e-6)
    gnb = rng(26)
    znb = []
    for i in range(2000):
        xb = gnb.choice(x, n)
        mb, vb = xb.mean(), xb.var(ddof=1)
        kb = mb ** 2 / max(vb - mb, 1e-6)
        znb.append(np.mean(gnb.negative_binomial(kb, kb / (kb + mb), n) == 0))
    znb = np.array(znb)
    return nest({"school": school, "zero_obs": zero_obs, "zero_pois": np.histogram(zp, np.linspace(0, 0.6, 61))[0],
                 "zero_nb": np.histogram(znb, np.linspace(0, 0.6, 61))[0], "edges": np.linspace(0, 0.6, 61),
                 "p_pois": float(np.mean(zp >= zero_obs)), "p_nb": float(np.mean(znb >= zero_obs)), "mean": float(m),
                 "var": float(v2), "k_hat": float(k_hat), "n": n})


def compute_priorpred():
    g = rng(2006)
    n, p = 1000, 5
    X = g.standard_normal((n, p))
    out = {}
    for name, sd in (("wide", 10.0), ("weak", 1.0)):
        probs = []
        for _ in range(200):
            b = g.normal(0, sd, p + 1)
            probs.append(special.expit(b[0] + X @ b[1:]))
        probs = np.concatenate(probs)
        out[name] = {"hist": np.histogram(probs, np.linspace(0, 1, 41), density=True)[0], "extreme": float(np.mean((probs < 0.01) | (probs > 0.99)))}
    out["edges"] = np.linspace(0, 1, 41)
    return nest(out)


def compute_sbc():
    g = rng(2018)
    n_obs, L = 2, 19

    def prior(r):
        return r.normal(0, 1)

    def data(th, r):
        return th + r.normal(size=n_obs)

    def good(yv, L_, r):
        v = 1 / (1 + n_obs)
        return v * yv.sum() + np.sqrt(v) * r.normal(size=L_)

    def overconfident(yv, L_, r):  # the right centre, but half the right variance
        v = 1 / (1 + n_obs)
        return v * yv.sum() + np.sqrt(0.5 * v) * r.normal(size=L_)

    def biased(yv, L_, r):  # a coding slip: the posterior uses prior mean 1 instead of 0
        v = 1 / (1 + n_obs)
        return v * (1.0 + yv.sum()) + np.sqrt(v) * r.normal(size=L_)

    out = {}
    for k, f in (("good", good), ("overconfident", overconfident), ("biased", biased)):
        r = B.sbc_ranks(prior, data, f, 4000, L, g)
        c = np.bincount(r, minlength=L + 1)
        out[k] = {"counts": c, "p": float(stats.chisquare(c).pvalue)}
    out["L"] = L
    return nest(out)


def compute_dp():
    g = rng(1973)
    z = B.crp(200, 2.0, g)
    sizes = np.sort(np.bincount(z))[::-1]
    ns = np.unique(np.geomspace(1, 10_000, 40).astype(int))
    exp_tables = {str(a): [B.crp_expected_tables(int(m), a) for m in ns] for a in (1.0, 5.0)}
    sticks = {str(a): B.stick_breaking(a, 30, rng(int(a * 10))) for a in (1.0, 5.0)}
    first = z[:30]
    return nest({"z": z, "sizes": sizes, "tables": int(len(sizes)), "expected": B.crp_expected_tables(200, 2.0), "ns": ns,
                 "exp_tables": exp_tables, "sticks": sticks, "first": first})


def compute_board():
    """Credible intervals for the mean scores of 8 of the World's schools, each estimated from 10 sampled pupils."""
    s = W.schools
    sch_all = s["school"]
    score = s["score"]
    n_sch = int(sch_all.max()) + 1
    means = np.bincount(sch_all, score, n_sch) / np.bincount(sch_all, minlength=n_sch)
    within = float(np.sqrt(np.mean((score - means[sch_all]) ** 2)))
    members = [np.flatnonzero(sch_all == k) for k in range(n_sch)]
    g = rng(2626)
    R, J, m = 1000, 8, 10
    hits = {"none": 0, "pooled": 0, "hier": 0}
    width = {"none": 0.0, "pooled": 0.0, "hier": 0.0}
    grid = np.linspace(0, 200, 801)
    by_rank = np.zeros(J)
    for _ in range(R):
        pick = g.choice(n_sch, J, replace=False)
        yj, sj, tj = [], [], []
        for k in pick:
            mem = members[k]
            take = g.choice(mem, m, replace=False)
            fpc = 1 - m / len(mem)
            yj.append(score[take].mean())
            sj.append(within * np.sqrt(fpc / m))
            tj.append(means[k])
        yj, sj, tj = map(np.asarray, (yj, sj, tj))
        lo, hi = yj - 1.96 * sj, yj + 1.96 * sj
        hits["none"] += np.sum((lo <= tj) & (tj <= hi))
        width["none"] += np.mean(hi - lo)
        w = 1 / sj ** 2
        pm, pse = np.sum(w * yj) / w.sum(), 1 / np.sqrt(w.sum())
        hits["pooled"] += np.sum(np.abs(tj - pm) <= 1.96 * pse)
        width["pooled"] += 2 * 1.96 * pse
        h = B.hier_normal(yj, sj, grid)
        dr = h.draws(2000, g)["theta"]
        lo, hi = np.percentile(dr, 2.5, 0), np.percentile(dr, 97.5, 0)
        hit = (lo <= tj) & (tj <= hi)
        hits["hier"] += np.sum(hit)
        order = np.argsort(np.abs(yj - yj.mean()))  # 0 = nearest the middle
        by_rank += hit[order]
        width["hier"] += np.mean(hi - lo)
    N = R * J
    rows = [
        Row(26, r"no pooling, \ $\bar y_j \pm 1.96\sigma_j$", r"8 schools, \ 10 pupils each", "coverage", 0.95, hits["none"] / N, N),
        Row(26, r"complete pooling", r"8 schools, \ 10 pupils each", "coverage", 0.95, hits["pooled"] / N, N),
        Row(26, r"hierarchical, \ 95\% credible", r"8 schools, \ 10 pupils each", "coverage", 0.95, hits["hier"] / N, N),
    ]
    save_rows(26, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows], "width": {k: v / R for k, v in width.items()},
            "within": within, "by_rank": by_rank / R}


ITEMS = {
    "schools": compute_schools, "priors": compute_priors, "jeffreys": compute_jeffreys, "conjugate": compute_conjugate,
    "bvm": compute_bvm, "bf": compute_bf, "lindley": compute_lindley, "occam": compute_occam, "decision": compute_decision,
    "ppc": compute_ppc, "priorpred": compute_priorpred, "sbc": compute_sbc, "dp": compute_dp, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
