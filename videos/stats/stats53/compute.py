"""Precompute every number in Part 53 of *Statistics, Built* ("Bayesian Asymptotics and Nonparametric Bayes").

    OMP_NUM_THREADS=1 python -m videos.stats.stats53.compute            # everything missing (several minutes)
    python -m videos.stats.stats53.compute --force board

Results are cached in ``.cache/stats53/<name>.json``.  Newcomb's light and Old Faithful are the Museum's; everything
else is exact arithmetic or a seeded simulation.

Items:
    doob      Beta-Bernoulli posterior means for truths drawn from the prior
    schwartz  posteriors with and without KL support of the truth
    rates     the sequence model's posterior risk and spread by n, alpha = beta and mismatched
    bvm       total variation between Beta posteriors and their normal approximations; two priors merging
    semipar   exact coverage of credible intervals for two linear functionals, and of credible balls, by alpha
    dp        Newcomb's light: the DP posterior CDF and band; Polya-urn table counts; Old Faithful by a DP mixture
    gp        the empirical contraction exponent by prior smoothness alpha against min(alpha, beta)/(2 alpha + 1)
    bands     EB credible-ball coverage by n, polished and inconvenient truths
    adapt     empirical Bayes: the marginal likelihood in alpha, alpha_hat by n, risk against the oracle
    hdbayes   sparse normal means: spike-and-slab and horseshoe coverage by signal size
    misspec   a Poisson model for overdispersed counts: credible and tempered intervals
    board     Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict
from functools import lru_cache

import numpy as np
from scipy import stats, integrate, special, optimize
from explainer.stats.kit import ppl as PPL

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import bnp as BN

CACHE = Cache("stats53")
load = CACHE.load


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


def empirical_mcse(values):
    a=np.asarray(values,float)
    return float(a.std(ddof=1)/math.sqrt(len(a)))


def bvm_tv_beta(k,n,a=1.,b=1.):
    """TV versus the MLE normal; at support endpoints that normal is a point mass."""
    if not 0<=k<=n or n<1:
        raise ValueError("0<=k<=n, n>=1 required")
    if k in (0,n):
        return 1.
    ph=k/n;sd=math.sqrt(ph*(1-ph)/n);post=stats.beta(a+k,b+n-k)
    lo,hi=-ph/sd,(1-ph)/sd
    knots=sorted(set([lo,hi,*[z for z in (-12,-8,-4,0,4,8,12) if lo<z<hi]]))
    inside=sum(integrate.quad(lambda z:abs(sd*post.pdf(ph+sd*z)-stats.norm.pdf(z)),u,v,epsabs=1e-10,limit=200)[0]
               for u,v in zip(knots[:-1],knots[1:]))
    return float(.5*(inside+stats.norm.cdf(lo)+stats.norm.sf(hi)))


_RADIUS_CACHE={}
def credible_radii(n,Kk,grid,reps=12000):
    """Independent MC reference with simultaneous 95% order-statistic uncertainty."""
    grid=np.asarray(grid,float);key=(int(n),Kk,tuple(grid),reps)
    if key in _RADIUS_CACHE:return _RADIUS_CACHE[key]
    pv=np.column_stack([BN.prior_var(Kk,a)/(1+n*BN.prior_var(Kk,a)) for a in grid])
    reference=rng(5340+int(n)+Kk)
    draws=[]
    for start in range(0,reps,128):
        z=reference.standard_normal((min(128,reps-start),Kk))
        draws.append((z*z)@pv)
    draws=np.sort(np.vstack(draws),axis=0)
    error=.05/len(grid)
    low=int(stats.binom.ppf(error/2,reps,.95));high=int(stats.binom.ppf(1-error/2,reps,.95))+1
    out={"q":np.quantile(draws,.95,axis=0),"lo":draws[max(low-1,0)],"hi":draws[min(high-1,reps-1)],
         "reference_reps":reps,"simultaneous_reference_level":.95,"grid":grid,"order_statistic_indices":[low,high]}
    _RADIUS_CACHE[key]=out
    return out


def spike_slab_interval(incl,slab_mean,slab_var,level=.95):
    """Exact mixture quantiles, preserving the atom at zero regardless of slab location."""
    if not 0<=incl<=1 or slab_var<=0 or not 0<level<1:
        raise ValueError("invalid mixture parameters")
    if incl==0:return (0.,0.)
    sd=math.sqrt(slab_var);left=incl*stats.norm.cdf(-slab_mean/sd)
    def q(p):
        if p<left:return float(slab_mean+sd*stats.norm.ppf(p/incl))
        if p<=left+1-incl:return 0.
        return float(slab_mean+sd*stats.norm.ppf((p-1+incl)/incl))
    return q((1-level)/2),q((1+level)/2)


def posterior_mean_squared_loss(Y,theta0,n,lam):
    """Realized loss; valid also when lam was selected from Y."""
    return np.sum((BN.posterior(Y,n,lam)["mean"]-theta0)**2,axis=-1)


@lru_cache(maxsize=8)
def _legendre_nodes(nk):
    return np.polynomial.legendre.leggauss(nk)


def horseshoe_posterior(y,tau,nk=256,level=.95):
    """Gauss-Legendre on u=sqrt(1-kappa), with no finite log-scale cutoff."""
    z,w=_legendre_nodes(nk);u=(z+1)/2
    logw=np.log(w/2)-np.log(tau*tau+(1-tau*tau)*u*u)-.5*(1-u*u)*y*y
    weights=np.exp(logw-special.logsumexp(logw))
    means=u*u*y;sd=u
    cdf=lambda x:float(weights@stats.norm.cdf((x-means)/sd))
    quant=lambda q:float(optimize.brentq(lambda x:cdf(x)-q,-abs(y)-20,abs(y)+20))
    return {"mean":float(weights@means),"lo":quant((1-level)/2),"hi":quant((1+level)/2)}


K = 3000


def compute_doob():
    r = rng(5301)
    ns = np.unique(np.round(np.geomspace(1, 3000, 80)).astype(int))
    paths, truths = [], []
    for _ in range(24):
        p = r.random()
        x = r.random(3000) < p
        s = np.cumsum(x)
        paths.append([(1 + s[n - 1]) / (2 + n) for n in ns])
        truths.append(p)
    return {"ns": ns, "paths": paths, "truths": truths}


def compute_schwartz():
    r = rng(5302)
    x = r.standard_normal(3000)  # truth theta0 = 0
    th = np.unique(np.r_[np.linspace(-1.5,3.2,600),1.,1+np.geomspace(1e-6,.2,400),np.nextafter(1.,-np.inf)])
    out = {}
    for n in (10, 100, 1000):
        m, v = x[:n].mean(), 1 / n
        # prior N(0, 10): posterior N(n xbar / (n + 0.1), 1 / (n + 0.1))
        pm, pv = n * m / (n + 0.1), 1 / (n + 0.1)
        good = stats.norm.pdf(th, pm, math.sqrt(pv))
        # prior Uniform[1, 3]: posterior N(xbar, 1/n) truncated to [1, 3]
        a, b = (1 - m) / math.sqrt(v), (3 - m) / math.sqrt(v)
        bad = np.where((th >= 1) & (th <= 3), stats.truncnorm.pdf(th, a, b, loc=m, scale=math.sqrt(v)), 0.0)
        out[str(n)] = {"good": good, "bad": bad, "bad_mean": float(stats.truncnorm.mean(a, b, loc=m, scale=math.sqrt(v)))}
    return {"theta": th, "post": out}


def compute_rates():
    beta = 1.0
    th = BN.sobolev_truth(K, beta)
    ns = np.geomspace(1e2, 1e6, 13)
    rows = {}
    for a in (0.5, 1.0, 2.0):
        lam = BN.prior_var(K, a)
        rows[str(a)] = [BN.risk(th, int(n), lam) for n in ns]
    slopes = {a: float(np.polyfit(np.log10(ns), 0.5 * np.log10([q["risk"] for q in v]), 1)[0]) for a, v in rows.items()}
    return {"beta": beta, "ns": ns, "rows": rows, "slopes": slopes,
            "theory": {str(a): -min(a, beta) / (1 + 2 * a) for a in (0.5, 1.0, 2.0)}}


def compute_bvm():
    ns = [10, 30, 100, 300, 1000, 3000, 10000]
    tv = {str(p): [bvm_tv_beta(int(round(p * n)), n) for n in ns] for p in (0.3, 0.02)}
    # two priors merging: Beta(1, 1) and Beta(20, 2), the truth p = 0.3
    r = rng(5303)
    x = r.random(10000) < 0.3
    merge = []
    for n in ns:
        k = int(x[:n].sum())
        a = stats.beta(1 + k, 1 + n - k)
        b = stats.beta(20 + k, 2 + n - k)
        g = np.linspace(0, 1, 20001)
        merge.append(0.5 * float(np.trapezoid(np.abs(a.pdf(g) - b.pdf(g)), g)))
    return {"ns": ns, "tv": tv, "merge": merge}


def compute_semipar():
    n = 10000
    beta = 1.0
    th = BN.sobolev_truth(K, beta)
    alphas = np.linspace(0.25, 3.0, 23)
    k = np.arange(1, K + 1)
    smooth = k ** -1.0
    rough = k ** -0.6
    cov_s = [BN.functional_coverage(th, n, BN.prior_var(K, a), smooth)["coverage"] for a in alphas]
    cov_r = [BN.functional_coverage(th, n, BN.prior_var(K, a), rough)["coverage"] for a in alphas]
    r=rng(5304);reference=credible_radii(n,K,alphas)
    balls=[];mcse=[];ranges=[]
    for j,a in enumerate(alphas):
        lam=BN.prior_var(K,a);w=n*lam/(1+n*lam)
        error=-(1-w)*th+w*r.standard_normal((1500,K))/math.sqrt(n)
        d2=np.sum(error**2,axis=1);hits=d2<=reference["q"][j]
        balls.append(float(hits.mean()));mcse.append(empirical_mcse(hits))
        ranges.append([float(np.mean(d2<=reference[key][j])) for key in ["lo","hi"]])
    return {"n":n,"beta":beta,"K":K,"alphas":alphas,"smooth":cov_s,"rough":cov_r,"ball":balls,
            "ball_mcse":mcse,"ball_reference_coverage_range":ranges,"reference":reference,
            "scope":"finite-coordinate experiment; functional coverage exact, ball coverage Monte Carlo"}


def compute_dp():
    x = np.asarray(museum.newcomb(), float)
    m, s = float(np.median(x)), float(stats.median_abs_deviation(x, scale="normal"))
    base = lambda t: stats.norm.cdf(t, m, 3 * s)  # noqa: E731
    grid = np.unique(np.r_[np.linspace(x.min()-3,x.max()+3,400),x,np.nextafter(x,-np.inf)])
    H = BN.dp_posterior_cdf(grid, x, 1.0, base)
    lo, hi = BN.dp_band(grid, x, 1.0, base)
    r = rng(5305)
    tables = {}
    for a in (1.0, 5.0, 25.0):
        tables[str(a)] = [int(len(np.unique(BN.polya_urn(nn, a, lambda g: g.standard_normal(), r)))) for nn in (10, 100, 1000)]
    ex = {str(a): [float(sum(a / (a + i) for i in range(nn))) for nn in (10, 100, 1000)] for a in (1.0, 5.0, 25.0)}
    er, _ = museum.faithful()
    g2 = np.linspace(1.0, 6.0, 300)
    chains=[BN.dp_mixture_gibbs(np.asarray(er,float),1.,1000,rng(5350+j),burn=300,grid=g2) for j in range(3)]
    traces=np.array([out["k_trace"][300:] for out in chains]);kt=traces.ravel()
    hist,edges=np.histogram(er,bins=np.linspace(1.,6.,41))
    hist=hist/(len(er)*np.diff(edges))
    return {"x":x,"grid":grid,"H":H,"lo":lo,"hi":hi,"n":len(x),"tables":tables,"tables_exp":ex,
            "faithful_grid":g2,"faithful_density":np.mean([out["density"] for out in chains],axis=0),
            "k_counts":np.bincount(kt),"k_mean":float(kt.mean()),"f_hist":hist,"f_edges":edges,
            "chain_cluster_means":traces.mean(axis=1),"cluster_rhat":PPL.rhat(traces),
            "cluster_ess":PPL.ess_bulk(traces),"cluster_traces":traces,
            "base_scope":"empirical Bayes: Newcomb base center/MAD and Faithful NIG hyperparameters estimated from data",
            "kept_per_chain":700,"chains":3}


def compute_gp():
    beta = 1.0
    Kg = 200000  # rough priors at n = 10^6 use ~n^(1/(1 + 2 alpha)) coordinates: K must not cap them
    th = BN.sobolev_truth(Kg, beta)
    ns = np.geomspace(1e3, 1e6, 7)
    alphas = np.linspace(0.25, 3.0, 23)
    emp = []
    for a in alphas:
        lam = BN.prior_var(Kg, a)
        rr = [math.sqrt(BN.risk(th, int(n), lam)["risk"]) for n in ns]
        emp.append(-float(np.polyfit(np.log(ns), np.log(rr), 1)[0]))
    theory = [min(a, beta) / (1 + 2 * a) for a in alphas]
    return {"beta": beta, "alphas": alphas, "empirical": emp, "theory": theory, "minimax": beta / (1 + 2 * beta)}


def compute_adapt():
    beta = 1.0
    th = BN.sobolev_truth(K, beta)
    r = rng(5306)
    n = 10000
    Y = th + r.standard_normal(K) / math.sqrt(n)
    grid = np.linspace(0.2, 3.0, 57)
    ll = [BN.log_marginal(Y, n, a) for a in grid]
    rows = []
    for nn in (100, 1000, 10000, 100000, 1000000):
        ah = []
        rk, frozen = [], []
        for _ in range(200):
            Yn = th + r.standard_normal(K) / math.sqrt(nn)
            a = BN.eb_alpha(Yn, nn, grid)
            ah.append(a)
            lam=BN.prior_var(K,a)
            rk.append(float(posterior_mean_squared_loss(Yn,th,nn,lam)))
            frozen.append(BN.risk(th,nn,lam)["risk"])
        oracle = min(BN.risk(th, nn, BN.prior_var(K, a))["risk"] for a in grid)
        rows.append({"n": nn, "alpha_hat": float(np.mean(ah)), "alpha_sd": float(np.std(ah)), "risk": float(np.mean(rk)), "oracle": oracle,"risk_mcse":empirical_mcse(rk),"frozen_alpha_surrogate":float(np.mean(frozen)),"reps":len(rk),
                     "minimax_rate": nn ** (-2 * beta / (1 + 2 * beta))})
    return {"beta": beta, "n": n, "grid": grid, "ll": ll, "alpha_hat": float(grid[int(np.argmax(ll))]), "rows": rows}


def inconvenient_truth(Kk: int,beta:float):
    """Truncation of an infinite growing-gap hyperrectangle-beta boundary sequence."""
    k=np.arange(1,Kk+1);th=np.zeros(Kk);j=0
    while (N:=2**(j*(j+1)))<=Kk:
        hi=min(2*N,Kk+1);th[N-1:hi-1]=k[N-1:hi-1]**(-.5-beta);j+=1
    return th


def eb_ball_coverage(theta0,n,reps,rng_,grid,L=1.):
    Kk=len(theta0);reference=credible_radii(n,Kk,grid)
    distances=[];radii=[];lows=[];highs=[];alphas=[]
    for _ in range(reps):
        Y=theta0+rng_.standard_normal(Kk)/math.sqrt(n)
        a=BN.eb_alpha(Y,n,grid);j=int(np.argmin(abs(np.asarray(grid)-a)));alphas.append(a)
        post=BN.posterior(Y,n,BN.prior_var(Kk,a))
        distances.append(float(np.sum((post["mean"]-theta0)**2)))
        radii.append(reference["q"][j]);lows.append(reference["lo"][j]);highs.append(reference["hi"][j])
    d2=np.asarray(distances);r2=np.asarray(radii);hits=d2<=L*L*r2
    return {"coverage":float(hits.mean()),"alpha_mean":float(np.mean(alphas)),"mcse":empirical_mcse(hits),
            "reference_coverage_range":[float(np.mean(d2<=L*L*np.asarray(v))) for v in [lows,highs]],
            "distance_squared":distances,"radius_squared":radii,"alphas":alphas,
            "reference_reps":reference["reference_reps"],"reference":reference,"K":Kk}


def compute_bands():
    r = rng(5310)
    Kk = 1500
    grid = np.linspace(0.2, 3.0, 29)
    ns = [300, 1000, 3000, 10000, 30000]
    pol, inc, ahat, details = [], [], [], []
    for n in ns:
        a = eb_ball_coverage(BN.sobolev_truth(Kk, 1.0), n, 150, r, grid)
        b = eb_ball_coverage(inconvenient_truth(Kk, 1.0), n, 150, r, grid)
        pol.append(a["coverage"])
        inc.append(b["coverage"])
        ahat.append(b["alpha_mean"])
        details.append({"n":n,"polished":a,"inconvenient":b})
    return {"ns": ns, "polished": pol, "inconvenient": inc, "alpha_inc": ahat,"details":details,"block_starts":"N_j=2^(j(j+1)); infinite continuation, displayed experiment truncated to K=1500"}


def compute_hdbayes():
    r = rng(5307)
    n = 400
    strengths = {"zero": 0.0, "small": 1.0, "intermediate": 2.5, "large": 6.0}
    theta = np.concatenate([np.zeros(n - 40), np.full(10, 1.0), np.full(10, 2.5), np.full(20, 6.0)])
    groups = np.array(["zero"] * (n - 40) + ["small"] * 10 + ["intermediate"] * 10 + ["large"] * 20)
    reps = 60
    cov = {"slab": {g: [] for g in strengths}, "hs": {g: [] for g in strengths}}
    dataset_coverage={m:{g:[] for g in strengths} for m in cov}
    tau = 40 / n
    for _ in range(reps):
        y = theta + r.standard_normal(n)
        previous={m:{g:len(v) for g,v in groups_.items()} for m,groups_ in cov.items()}
        ss = BN.spike_slab_posterior(y, tau=3.0)
        for i in range(n):
            lo, hi = spike_slab_interval(float(ss["incl"][i]), float(ss["slab_mean"][i]), float(ss["slab_var"]))
            cov["slab"][groups[i]].append(lo - 1e-9 <= theta[i] <= hi + 1e-9)
        for i in np.r_[0:40, n - 40:n]:
            h = horseshoe_posterior(float(y[i]),tau)
            cov["hs"][groups[i]].append(h["lo"] <= theta[i] <= h["hi"])
        for method,groups_ in cov.items():
            for group,values in groups_.items():
                dataset_coverage[method][group].append(float(np.mean(values[previous[method][group]:])))
    return {"n": n, "reps": reps, "strengths": strengths, "tau": tau,"tau_scope":"oracle true sparsity proportion",
            "dataset_coverage":dataset_coverage,"mcse":{m:{g:empirical_mcse(v) for g,v in groups_.items()} for m,groups_ in dataset_coverage.items()},
            "coverage": {m: {g: float(np.mean(v)) for g, v in d.items()} for m, d in cov.items()}}


def compute_misspec():
    r = rng(5308)
    n, reps = 200, 4000
    mu, size = 8.0, 2.0
    p = size / (size + mu)
    c1 = c2 = 0
    w1 = w2 = 0.0
    for _ in range(reps):
        y = r.negative_binomial(size, p, n)
        lo, hi = BN.poisson_gamma_ci(y)
        c1 += lo <= mu <= hi
        w1 += hi - lo
        e = BN.calibrated_eta(y)
        lo, hi = BN.poisson_gamma_ci(y, eta=e)
        c2 += lo <= mu <= hi
        w2 += hi - lo
    return {"n": n, "mu": mu, "var": mu + mu ** 2 / size, "reps": reps, "cov_plain": c1 / reps, "cov_tempered": c2 / reps,
            "w_plain": w1 / reps, "w_tempered": w2 / reps, "eta_true": mu / (mu + mu ** 2 / size)}


def compute_board():
    r = rng(5309)
    Kk = 1500
    n = 10000
    grid = np.linspace(0.2, 3.0, 29)
    pol = eb_ball_coverage(BN.sobolev_truth(Kk, 1.0), n, 300, r, grid)
    inc = eb_ball_coverage(inconvenient_truth(Kk, 1.0), n, 300, r, grid)
    inflated=np.asarray(pol["distance_squared"])<=2.25*np.asarray(pol["radius_squared"])
    pol_l={"coverage":float(inflated.mean()),"mcse":empirical_mcse(inflated)}
    hd = load("hdbayes")
    ms = load("misspec")
    reps_hd = hd["reps"]
    rows = [
        Row(53, r"EB credible ball, polished truth", r"sequence model, $\beta = 1$, \ $n = 10^4$", "coverage", 0.95, pol["coverage"],300,mc_se=pol["mcse"]),
        Row(53, r"EB credible ball, inconvenient truth", r"sequence model, $\beta = 1$, \ $n = 10^4$", "coverage", 0.95, inc["coverage"],300,mc_se=inc["mcse"]),
        Row(53, r"EB credible ball inflated $1.5\times$, polished truth", r"sequence model, $\beta = 1$, \ $n = 10^4$", "coverage", 0.95, pol_l["coverage"],300,mc_se=pol_l["mcse"]),
        Row(53, r"horseshoe interval, intermediate signals", r"sparse means, $\theta_i = 2.5$, \ $n = 400$", "coverage", 0.95, hd["coverage"]["hs"]["intermediate"],reps_hd,mc_se=hd["mcse"]["hs"]["intermediate"]),
        Row(53, r"Poisson credible interval, overdispersed counts", r"NB, mean 8, var 40, \ $n = 200$", "coverage", 0.95, ms["cov_plain"],ms["reps"],mc_se=math.sqrt(ms["cov_plain"]*(1-ms["cov_plain"])/(ms["reps"]-1))),
        Row(53, r"tempered (generalized) posterior interval", r"NB, mean 8, var 40, \ $n = 200$", "coverage", 0.95, ms["cov_tempered"],ms["reps"],mc_se=math.sqrt(ms["cov_tempered"]*(1-ms["cov_tempered"])/(ms["reps"]-1))),
    ]
    save_rows(53, rows)
    return {"rows": [asdict(q) | {"verdict": q.verdict, "se": q.se} for q in rows], "alpha_pol": pol["alpha_mean"], "alpha_inc": inc["alpha_mean"],"polished":pol,"inconvenient":inc,"inflation_paired":True}


ITEMS = {
    "doob": compute_doob, "schwartz": compute_schwartz, "rates": compute_rates, "bvm": compute_bvm, "semipar": compute_semipar,
    "dp": compute_dp, "gp": compute_gp, "adapt": compute_adapt, "bands": compute_bands, "hdbayes": compute_hdbayes, "misspec": compute_misspec,
    "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
