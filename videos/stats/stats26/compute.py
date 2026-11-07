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
from scipy import integrate, optimize, special, stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows, load_all as _load_board
from explainer.stats.kit import bayes as B
from explainer.stats.world import World

CACHE = Cache("stats26")
load = CACHE.load
W = World()
TAU = np.r_[np.linspace(0, .1, 101), np.geomspace(.101, 1e6, 10000)]


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


class Hier(B.Hier):
    """Independent conditional draws from a checked, finite numerical tau approximation."""
    def draws(self, n, rng):
        cdf = integrate.cumulative_trapezoid(self.post_tau, self.tau, initial=0.)
        tau = np.interp(rng.random(n), cdf/cdf[-1], self.tau)
        t2 = tau[:, None]**2
        s2 = self.sigma[None, :]**2
        w = 1/(s2+t2)
        mp = getattr(self, "mu_prior", None)
        m0, p0 = (0., 0.) if mp is None else (mp[0], 1/mp[1]**2)
        vm = 1/(w.sum(1)+p0)
        mu = vm*((w*self.y).sum(1)+p0*m0)+np.sqrt(vm)*rng.standard_normal(n)
        own = t2/(t2+s2)
        mean = own*self.y+(1-own)*mu[:, None]
        theta = mean+np.sqrt(s2*own)*rng.standard_normal((n,len(self.y)))
        return dict(tau=tau, mu=mu, theta=theta)


def hier_normal(y, sigma, grid=TAU, log_prior_tau=None):
    """Flat-mean hierarchy on a wide nonuniform grid; no endpoint atoms or cell jitter."""
    y,sigma,grid=map(lambda x:np.asarray(x,float),(y,sigma,grid))
    if y.ndim!=1 or not len(y) or sigma.shape!=y.shape or np.any(sigma<=0) or not np.all(np.isfinite(y+sigma)):
        raise ValueError("finite observations and positive finite known SDs required")
    if grid.ndim!=1 or len(grid)<2 or grid[0]<0 or not np.all(np.isfinite(grid)) or np.any(np.diff(grid)<=0):
        raise ValueError("strictly increasing finite nonnegative tau grid required")
    base=B.hier_normal(y,sigma,grid,log_prior_tau)
    return Hier(base.y,base.sigma,base.tau,base.post_tau,base.mu_hat,base.v_mu)


def tau_kernel(tau, y, sigma):
    y,sigma=np.asarray(y),np.asarray(sigma)
    v=sigma**2+tau**2;w=1/v;vm=1/w.sum();mu=vm*(w*y).sum()
    return float(.5*np.log(vm)-.5*np.log(v).sum()-.5*(w*(y-mu)**2).sum())


def tau_reference(y,sigma,log_prior=None):
    """Adaptive infinite-range reference for quantiles and omitted tail mass."""
    if log_prior is None and len(y)<3:raise ValueError("flat mean and flat tau give an improper posterior with fewer than three groups")
    prior=(lambda t:np.zeros_like(t)) if log_prior is None else log_prior
    kernel=lambda t:tau_kernel(t,y,sigma)+float(np.asarray(prior(np.array([t]))).reshape(-1)[0])
    shift=max(kernel(t) for t in [.01,.1,1.,5.,10.,30.])
    f=lambda t:float(np.exp(kernel(t)-shift))
    normalizer=integrate.quad(f,0,np.inf,epsabs=1e-10,epsrel=1e-9,limit=300)[0]
    def quantile(q):
        cdf=lambda t:integrate.quad(f,0,t,epsabs=1e-10,epsrel=1e-9,limit=300)[0]/normalizer-q
        upper=40.
        while cdf(upper)<0:upper*=2
        return optimize.brentq(cdf,0,upper,xtol=1e-7)
    return dict(median=quantile(.5),q95=quantile(.95),
                tail_over40=integrate.quad(f,40,np.inf,epsabs=1e-11,limit=300)[0]/normalizer,
                tail_over_grid=integrate.quad(lambda u:f(1/u)/u**2,0,1/TAU[-1],
                                               epsabs=1e-14,limit=300)[0]/normalizer)


def integration_weights(grid):
    d=np.diff(grid)
    return np.r_[d[0]/2,(d[:-1]+d[1:])/2,d[-1]/2]


def normal_mixture_information(mean,variance,weights,cost,se):
    """Linear adopt/reject utility and information value, integrated without binning pilot results."""
    mean,variance,weights=map(np.asarray,(mean,variance,weights))
    weights=weights/weights.sum()
    if np.any(variance<=0) or se<0:raise ValueError("positive component variances and nonnegative pilot SE required")
    sd=np.sqrt(variance);gain=mean-cost
    now=max(float(weights@gain),0.)
    perfect=float(weights@(gain*special.ndtr(gain/sd)+sd*stats.norm.pdf(gain/sd)))
    if se==0:return dict(eu_adopt=float(weights@gain),evpi=perfect-now,evsi=perfect-now,threshold=cost)
    pv=variance+se**2;ps=np.sqrt(pv)
    def conditional_gain(value):
        logw=np.log(np.maximum(weights,1e-300))+stats.norm.logpdf(value,mean,ps)
        a=np.exp(logw-logw.max());a/=a.sum()
        return float(a@(gain+variance/pv*(value-mean)))
    lower=min(float(mean.min()),cost)-10*float(ps.max())
    upper=max(float(mean.max()),cost)+10*float(ps.max())
    while conditional_gain(lower)>0:lower=cost-2*(cost-lower)
    while conditional_gain(upper)<0:upper=cost+2*(upper-cost)
    threshold=optimize.brentq(conditional_gain,lower,upper,xtol=1e-9)
    z=(threshold-mean)/ps
    sample=float(weights@(gain*stats.norm.sf(z)+variance/ps*stats.norm.pdf(z)))
    return dict(eu_adopt=float(weights@gain),evpi=perfect-now,evsi=sample-now,threshold=threshold)


def nb_posterior_grid(x,points=241):
    """Proper NB2 posterior on log mean and log shape, with explicit normal priors on both."""
    x=np.asarray(x)
    if x.ndim!=1 or not len(x) or np.any(x<0) or np.any(x!=np.floor(x)):
        raise ValueError("nonnegative integer counts required")
    lm=np.linspace(np.log(.05),np.log(20),points)
    lk=np.linspace(np.log(.02),np.log(30),points)
    mu=np.exp(lm[:,None]);shape=np.exp(lk[None,:]);den=np.log(shape+mu)
    counts=np.bincount(x.astype(int))
    lp=np.zeros((points,points))
    for value,count in enumerate(counts):
        if count:
            lp+=count*(special.gammaln(value+shape)-special.gammaln(shape)-special.gammaln(value+1)
                       +shape*(lk[None,:]-den)+value*(lm[:,None]-den))
    lp+=stats.norm.logpdf(lm,np.log(3),1)[:,None]+stats.norm.logpdf(lk,0,1.5)[None,:]
    weights=np.exp(lp-lp.max())*np.outer(integration_weights(lm),integration_weights(lk))
    weights/=weights.sum()
    edge=float(weights[[0,-1],:].sum()+weights[:,[0,-1]].sum())
    if edge>1e-4:raise ValueError("NB posterior reaches numerical grid boundary; expand the grid")
    return dict(logmu=lm,logshape=lk,weights=weights,edge_mass=edge,
                prior="log(mu) ~ N(log(3),1); log(shape) ~ N(0,1.5^2)")


# The shared Board preserves this empirical SE when later parts reload the row.
CoverageRow=Row


def coverage_rows():
    return _load_board(upto=26)


def compute_schools():
    lab, y, s = museum.eight_schools()
    w = 1 / s ** 2
    pooled = float(np.sum(w * y) / w.sum())
    pooled_se = float(1 / np.sqrt(w.sum()))
    Q = float(np.sum(w * (y - pooled) ** 2))
    h = hier_normal(y, s, TAU)
    mean, var = h.cond_theta()
    d = h.draws(200_000, rng(1981))
    th = d["theta"]
    q = lambda a, p: np.percentile(a, p, axis=0)  # noqa: E731
    best = np.bincount(np.argmax(th, 1), minlength=8) / len(th)
    plot_tau = np.linspace(0,40,401)
    plot_mean = np.column_stack([np.interp(plot_tau,TAU,col) for col in mean.T])
    plot_sd = np.column_stack([np.interp(plot_tau,TAU,col) for col in np.sqrt(var).T])
    reference = tau_reference(y,s)
    return nest({"labels": lab, "y": y, "sigma": s, "pooled": pooled, "pooled_se": pooled_se, "Q": Q,
                 "p_Q": float(stats.chi2.sf(Q, 7)), "tau": plot_tau, "post_tau": np.interp(plot_tau,TAU,h.post_tau),
                 "cond_mean": plot_mean, "cond_sd": plot_sd, "mu_hat": np.interp(plot_tau,TAU,h.mu_hat),
                 "theta_mean": th.mean(0), "theta_med": np.median(th, 0), "theta_lo": q(th, 2.5), "theta_hi": q(th, 97.5),
                 "mu_mean": float(d["mu"].mean()), "mu_lo": float(np.percentile(d["mu"], 2.5)), "mu_hi": float(np.percentile(d["mu"], 97.5)),
                 "tau_med": reference["median"], "tau_infinite_reference": reference, "tau_lo": float(np.percentile(d["tau"], 2.5)),
                 "tau_hi": float(np.percentile(d["tau"], 97.5)), "tau_mode": float(TAU[np.argmax(h.post_tau)]),
                 "p_A_gt_C": float(np.mean(th[:, 0] > th[:, 2])), "p_best": best,
                 "draws_theta": th[:20], "draws_tau": d["tau"][:20], "draws_mu": d["mu"][:20],
                 "tau_hist": np.histogram(d["tau"], np.linspace(0, 40, 41))[0]/len(d["tau"])})


def compute_priors():
    lab, y, s = museum.eight_schools()
    priors = {
        "uniform": lambda t: np.zeros_like(t),
        "halfcauchy": lambda t: stats.halfcauchy.logpdf(t, scale=25),
        # inverse-gamma(eps, eps) on tau^2, as a density for tau: p(tau) = p(tau^2) 2 tau
        "ig1": lambda t: stats.invgamma.logpdf(np.maximum(t, 1e-6) ** 2, 1, scale=1) + np.log(2 * np.maximum(t, 1e-6)),
        "ig001": lambda t: stats.invgamma.logpdf(np.maximum(t, 1e-6) ** 2, 0.001, scale=0.001) + np.log(2 * np.maximum(t, 1e-6)),
    }
    grid = np.geomspace(1e-3,1e3,1201)
    gfine = TAU
    out = {"tau": grid}
    for subset, idx in (("eight", slice(None)), ("three", slice(0, 3))):
        out[subset] = {}
        for k, f in priors.items():
            h = hier_normal(y[idx], s[idx], gfine, f)
            dens = np.interp(grid, gfine, h.post_tau)
            cdf = integrate.cumulative_trapezoid(h.post_tau,gfine,initial=0.)
            cdf /= cdf[-1]
            reference = tau_reference(y[idx],s[idx],f)
            out[subset][k] = {"dens": dens, "median": reference["median"], "infinite_reference": reference,
                              "q95": reference["q95"], "prior": np.exp(f(np.maximum(grid, 1e-3)))}
    # improper: p(log tau) flat, i.e. p(tau) ∝ 1/tau; the marginal posterior of log tau tends to a constant at -inf
    lt = np.linspace(-12, 4, 400)
    h = hier_normal(y, s, np.exp(lt))  # The likelihood kernel is also the log-tau posterior kernel for a flat log-tau prior.
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
        difference=lambda t:abs(stats.gamma.pdf(t,a,scale=1/b)-stats.norm.pdf(t,mle,np.sqrt(mle/n)))
        tv=.5*(integrate.quad(difference,0,mle,epsabs=1e-10,limit=200)[0]
               +integrate.quad(difference,mle,np.inf,epsabs=1e-10,limit=200)[0]
               +stats.norm.cdf(0,mle,np.sqrt(mle/n)))
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
    tau_min=sigma*np.sqrt(max(z*z-1,0)/n)
    bic01 = float(np.exp(0.5 * (np.log(n) - z ** 2)))  # BIC approximation to BF_01 (unit-information prior)
    unit = B.bf01_normal(xbar, n, sigma, sigma)
    return nest({"n": n, "z": z, "p": float(2 * stats.norm.sf(z)), "taus": taus, "bf01": bf, "tau_min": float(tau_min),
                 "bf_min": B.bf01_normal(xbar,n,sigma,tau_min), "bic01": bic01, "unit01": unit})


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
    ns = np.unique(np.geomspace(10, 1e8, 60).astype(int))
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
    h = hier_normal(y, s, TAU)
    d = h.draws(400_000, rng(2620))
    g = rng(2621)
    theta_new = d["mu"] + d["tau"] * g.standard_normal(len(d["mu"]))
    cost = 5.0  # points of SAT the programme must deliver to repay its cost
    gain = theta_new - cost
    eu_adopt = float(gain.mean())
    evpi = float(np.mean(np.maximum(gain, 0)) - max(eu_adopt, 0.0))
    se=10.
    weights=h.post_tau*integration_weights(h.tau)
    information=normal_mixture_information(h.mu_hat,h.tau**2+h.v_mu,weights,cost,se)
    eu_adopt=information["eu_adopt"];evpi=information["evpi"];evsi=information["evsi"]
    return nest({"cost": cost, "p_exceed": float(np.mean(theta_new > cost)), "mean_new": float(theta_new.mean()),
                 "sd_new": float(theta_new.std()), "integration": information, "eu_adopt": eu_adopt, "evpi": evpi, "evsi": evsi, "se": se,
                 "hist": np.histogram(theta_new, np.linspace(-40, 50, 46))[0]/len(theta_new)/2, "edges": np.linspace(-40, 50, 46)})


def compute_ppc():
    lab, y, s = museum.eight_schools()
    h = hier_normal(y, s, TAU)
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
    m,v2=x.mean(),x.var(ddof=1)
    posterior=nb_posterior_grid(x)
    gnb=rng(26)
    selected=gnb.choice(posterior["weights"].size,2000,p=posterior["weights"].ravel())
    mi,ki=np.unravel_index(selected,posterior["weights"].shape)
    mus=np.exp(posterior["logmu"][mi]);ks=np.exp(posterior["logshape"][ki])
    znb=(gnb.negative_binomial(ks[:,None],(ks/(ks+mus))[:,None],size=(2000,n))==0).mean(1)
    k_hat=float(posterior["weights"].sum(0)@np.exp(posterior["logshape"]))
    return nest({"school": school, "zero_obs": zero_obs, "zero_pois": np.histogram(zp, np.linspace(0, 0.6, 61))[0],
                 "zero_nb": np.histogram(znb, np.linspace(0, 0.6, 61))[0], "edges": np.linspace(0, 0.6, 61),
                 "replicates": len(zp), "pois_exceedances": int(np.sum(zp>=zero_obs)),
                 "nb_prior": posterior["prior"], "nb_edge_mass": posterior["edge_mass"],
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
    grid = TAU
    by_rank = np.zeros(J)
    replicate_coverage={key:[] for key in hits}
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
        hit=(lo<=tj)&(tj<=hi)
        hits["none"] += np.sum(hit)
        replicate_coverage["none"].append(float(hit.mean()))
        width["none"] += np.mean(hi - lo)
        w = 1 / sj ** 2
        pm, pse = np.sum(w * yj) / w.sum(), 1 / np.sqrt(w.sum())
        hit=np.abs(tj-pm)<=1.96*pse
        hits["pooled"] += np.sum(hit)
        replicate_coverage["pooled"].append(float(hit.mean()))
        width["pooled"] += 2 * 1.96 * pse
        h = hier_normal(yj, sj, grid)
        dr = h.draws(2000, g)["theta"]
        lo, hi = np.percentile(dr, 2.5, 0), np.percentile(dr, 97.5, 0)
        hit = (lo <= tj) & (tj <= hi)
        hits["hier"] += np.sum(hit)
        replicate_coverage["hier"].append(float(hit.mean()))
        order = np.argsort(np.abs(yj - yj.mean()))  # 0 = nearest the middle
        by_rank += hit[order]
        width["hier"] += np.mean(hi - lo)
    N = R * J
    rows = [
        CoverageRow(26, r"no pooling, \ $\bar y_j \pm 1.96\sigma_j$", r"8 schools, \ 10 pupils each", "coverage", 0.95, hits["none"] / N, R, mc_se=float(np.std(replicate_coverage["none"],ddof=1)/np.sqrt(R))),
        CoverageRow(26, r"complete pooling", r"8 schools, \ 10 pupils each", "coverage", 0.95, hits["pooled"] / N, R, mc_se=float(np.std(replicate_coverage["pooled"],ddof=1)/np.sqrt(R))),
        CoverageRow(26, r"hierarchical, \ 95\% credible", r"8 schools, \ 10 pupils each", "coverage", 0.95, hits["hier"] / N, R, mc_se=float(np.std(replicate_coverage["hier"],ddof=1)/np.sqrt(R))),
    ]
    save_rows(26, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows], "width": {k: v / R for k, v in width.items()},
            "within": within, "by_rank": by_rank / R, "intervals": N,
            "replicate_coverage": replicate_coverage,
            "mc_scope": "1000 independent simulated datasets; eight correlated intervals per dataset"}


ITEMS = {
    "schools": compute_schools, "priors": compute_priors, "jeffreys": compute_jeffreys, "conjugate": compute_conjugate,
    "bvm": compute_bvm, "bf": compute_bf, "lindley": compute_lindley, "occam": compute_occam, "decision": compute_decision,
    "ppc": compute_ppc, "priorpred": compute_priorpred, "sbc": compute_sbc, "dp": compute_dp, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)


def clipped_segments(xs, ys, rectangle):
    """Intersect segments with the viewport, preserving crossings and missing breaks."""
    xmin, xmax, ymin, ymax = rectangle
    points = np.column_stack((xs, ys))
    result = []
    for start, end in zip(points[:-1], points[1:]):
        if not np.isfinite([start, end]).all():
            continue
        delta = end-start
        lo, hi = 0., 1.
        for j, lower, upper in ((0, xmin, xmax), (1, ymin, ymax)):
            if delta[j] == 0:
                if not lower <= start[j] <= upper:
                    hi = -1
                    break
            else:
                a, b = sorted(((lower-start[j])/delta[j], (upper-start[j])/delta[j]))
                lo, hi = max(lo, a), min(hi, b)
        if lo <= hi:
            result.append((start+lo*delta, start+hi*delta))
    return result
