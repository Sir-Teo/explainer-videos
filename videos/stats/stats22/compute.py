"""Precompute every number in Part 22 of *Statistics, Built* ("Likelihood in Depth").

    python -m videos.stats.stats22.compute            # everything missing (a few minutes)
    python -m videos.stats.stats22.compute --force board

Results are cached in ``.cache/stats22/<name>.json``.  Weldon's crabs and Bortkiewicz's horse kicks are the Museum's;
incomes are the World's; the rest are seeded simulations.

Items:
    crabs       EM for the crabs: the path, the log likelihood, the rate; Pearson's moment solutions; SEs
    consistency average log likelihood curves for Poisson samples of growing size, against the expected curve
    asymp       the Cauchy location MLE vs the median over many samples: the CLT for the MLE
    efron       observed vs expected information for the Cauchy (Efron & Hinkley 1978)
    gamma       a two-parameter gamma likelihood for the World's incomes: contours, ridge, profile and Wald intervals
    trinity     Wald, score and LR for 14 successes in 20 trials
    hauck       the Hauck-Donner effect: the Wald z shrinks as the logistic slope grows
    neyman      Neyman-Scott pairs: the MLE of sigma^2 converges to half the truth
    kl          a log-normal fitted to the World's incomes: the KL projection and the tail it misses
    sandwich    Poisson regression of overdispersed counts: model, sandwich and quasi SEs
    misbehave   the crab likelihood as one component collapses onto a point; label switching
    ising       an Ising lattice and Besag's pseudo-likelihood
    principle   binomial vs negative-binomial stopping for 9 heads and 3 tails
    board       Coverage Board rows
"""

from __future__ import annotations

from dataclasses import asdict

import numpy as np
from scipy import stats, optimize
from scipy.special import expit, logsumexp, digamma, polygamma

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import mle as M
from explainer.stats.world import World

CACHE = Cache("stats22")
load = CACHE.load
W = World()
START = [0.5, 0.6343, 0.0190, 0.6551, 0.0121]  # mixdist's starting values for these data


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


def logistic_slope_tests(x, y):
    """Stable finite logistic fit; explicitly identify separation in one continuous predictor."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    X = np.column_stack([np.ones(len(x)), x])
    ll0 = float(np.sum(stats.bernoulli.logpmf(y, y.mean())))
    separated = len(np.unique(y)) == 1
    direction = 0
    if not separated:
        if x[y == 0].max() < x[y == 1].min():
            separated, direction = True, 1
        elif x[y == 1].max() < x[y == 0].min():
            separated, direction = True, -1
    if separated:
        return dict(b=np.array([np.nan, direction*np.inf if direction else np.nan]),
                    se=np.inf, z=np.nan, ll=0., lr=-2*ll0, finite=False, direction=direction)
    b = np.zeros(2)
    loglik = lambda v: float(np.sum(y*(X@v)-np.logaddexp(0, X@v)))
    for _ in range(100):
        pr = expit(X@b)
        score = X.T@(y-pr)
        info = X.T@((pr*(1-pr))[:,None]*X)
        step = np.linalg.solve(info, score)
        scale, old = 1., loglik(b)
        while loglik(b+scale*step) < old-1e-12:
            scale *= .5
            if scale < 1e-12:
                raise RuntimeError("Logistic line search failed")
        b += scale*step
        if np.max(np.abs(score)) < 1e-9:
            break
    else:
        raise RuntimeError("Logistic fit did not converge")
    pr = expit(X@b)
    info = X.T@((pr*(1-pr))[:,None]*X)
    se = float(np.sqrt(np.linalg.inv(info)[1,1]))
    return dict(b=b, se=se, z=b[1]/se, ll=loglik(b), lr=2*(loglik(b)-ll0),
                finite=True, direction=0)


def logistic_profile_ci(x, y, level=.95):
    """Profile by monotone intercept-score roots, then bracket slope LR roots."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    fit = logistic_slope_tests(x, y)
    if len(np.unique(y)) == 1:
        return -np.inf, np.inf
    cut = fit["ll"]-stats.chi2.ppf(level,1)/2
    def profile(b):
        bx = b*x
        a = optimize.brentq(lambda a: np.sum(y-expit(a+bx)),
                            -bx.max()-40, -bx.min()+40, xtol=1e-12)
        return float(np.sum(y*(a+bx)-np.logaddexp(0,a+bx)))
    if fit["finite"]:
        center = fit["b"][1]
        width = fit["se"]
    else:
        center, width = float(fit["direction"]), 1.
        while profile(center) < cut:
            center *= 2
    roots = []
    for sign in (-1,1):
        if not fit["finite"] and sign == fit["direction"]:
            roots.append(sign*np.inf)
            continue
        width_ = width
        for _ in range(60):
            edge = center+sign*width_
            if profile(edge) < cut:
                roots.append(optimize.brentq(lambda b: profile(b)-cut,
                                             *sorted([center,edge]),xtol=1e-10))
                break
            width_ *= 2
        else:
            raise RuntimeError("Profile endpoint could not be bracketed")
    return tuple(roots)


def louis_mixture_information(x, w, theta):
    """Observed information via E[-H_complete|x] - Cov(score_complete|x)."""
    p,m1,s1,m2,s2 = np.asarray(theta,float)
    x,w = np.asarray(x,float),np.asarray(w,float)
    logparts = np.array([np.log(p)+stats.norm.logpdf(x,m1,s1),
                         np.log1p(-p)+stats.norm.logpdf(x,m2,s2)])
    resp = np.exp(logparts-logsumexp(logparts,axis=0))
    scores = np.zeros((2,len(x),5))
    hess = np.zeros((2,len(x),5,5))
    for k,(mean,sd,weight,sgn,mi,si) in enumerate(
        [(m1,s1,p,1,1,2),(m2,s2,1-p,-1,3,4)]):
        u = x-mean
        scores[k,:,0] = sgn/weight
        scores[k,:,mi] = u/sd**2
        scores[k,:,si] = -1/sd+u**2/sd**3
        hess[k,:,0,0] = -1/weight**2
        hess[k,:,mi,mi] = -1/sd**2
        hess[k,:,mi,si] = hess[k,:,si,mi] = -2*u/sd**3
        hess[k,:,si,si] = 1/sd**2-3*u**2/sd**4
    avg = np.einsum("kn,knj->nj",resp,scores)
    complete = -np.einsum("n,kn,knij->ij",w,resp,hess)
    meat = np.einsum("n,kn,kni,knj->ij",w,resp,scores,scores)
    missing = meat-np.einsum("n,ni,nj->ij",w,avg,avg)
    return complete-missing


def binned_counts(y, upper):
    """Include the entire real line in the first and last displayed classes."""
    return np.bincount(np.searchsorted(np.asarray(upper)[:-1],y),minlength=len(upper)).astype(float)


def midpoint_em(x, counts, starts, min_sd=.002, iters=3000, tol=1e-10):
    """A specified multistart, SD-constrained midpoint-density fit, not an unrestricted LR."""
    x, counts = np.asarray(x,float),np.asarray(counts,float)
    best = None
    for start in starts:
        th = np.asarray(start,float).copy()
        old = -np.inf
        for _ in range(iters):
            p,m1,s1,m2,s2 = th
            parts = np.array([np.log(p)+stats.norm.logpdf(x,m1,s1),
                              np.log1p(-p)+stats.norm.logpdf(x,m2,s2)])
            r = np.exp(parts[0]-logsumexp(parts,axis=0))
            w1,w2 = counts*r,counts*(1-r)
            n1,n2 = w1.sum(),w2.sum()
            if min(n1,n2) <= 1e-12:
                break
            a,b = w1@x/n1,w2@x/n2
            th = np.array([n1/(n1+n2),a,max(min_sd,np.sqrt(w1@(x-a)**2/n1)),
                           b,max(min_sd,np.sqrt(w2@(x-b)**2/n2))])
            ll = M.mix_loglik(x,th,counts)
            if abs(ll-old) < tol:
                break
            old = ll
        candidate = dict(theta=th,loglik=M.mix_loglik(x,th,counts))
        if best is None or candidate["loglik"] > best["loglik"]:
            best = candidate
    return best


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

def compute_crabs():
    x, w = museum.crabs()
    em = M.em_mixture(x, START, w=w, iters=5000, tol=1e-13)
    th = em["theta"]
    info = louis_mixture_information(x,w,th)
    se = np.sqrt(np.diag(np.linalg.inv(info)))
    pm = M.pearson_moments(x, w)
    order = np.argsort([-v[0] for v in pm["solutions"]])
    pm["solutions"] = [pm["solutions"][j] for j in order]
    pm["sixth"] = [pm["sixth"][j] for j in order]
    em["resp"] = th[0]*stats.norm.pdf(x,th[1],th[2])/(th[0]*stats.norm.pdf(x,th[1],th[2])+(1-th[0])*stats.norm.pdf(x,th[3],th[4]))
    one_mu = (w @ x) / w.sum()
    one_sd = np.sqrt((w @ (x - one_mu) ** 2) / w.sum())
    ll_one = float(np.sum(w * stats.norm.logpdf(x, one_mu, one_sd)))
    grid = np.linspace(0.575, 0.70, 400)
    dens = th[0] * stats.norm.pdf(grid, th[1], th[2]) + (1 - th[0]) * stats.norm.pdf(grid, th[3], th[4])
    keep = [0, 1, 2, 3, 5, 10, 20, 50, 100, 200, 400, 800, len(em["path"]) - 1]
    return nest({"x": x, "w": w, "theta": th, "se": se, "loglik": em["loglik"], "iters": len(em["loglik"]) - 1,
                 "rate": em["rate"], "path_keep": keep, "path": em["path"][keep], "resp": em["resp"],
                 "pearson": pm["solutions"], "sixth": pm["sixth"], "sixth_data": pm["sixth_data"],
                 "ll_pearson": [M.mix_loglik(x, s_, w) for s_ in pm["solutions"]], "one": [one_mu, one_sd], "ll_one": ll_one,
                 "grid": grid, "dens": dens, "comp1": th[0] * stats.norm.pdf(grid, th[1], th[2]),
                 "comp2": (1 - th[0]) * stats.norm.pdf(grid, th[3], th[4])})


def compute_consistency():
    lam0 = float(np.dot(museum.HORSEKICK_K, museum.HORSEKICK_N) / np.sum(museum.HORSEKICK_N))
    stream = rng(4).poisson(lam0, 10000)  # one growing sample: its first 10, 100, 1,000 and 10,000 draws
    th = np.linspace(0.05, 2.0, 300)
    curves = {}
    for n in (10, 100, 1000, 10000):
        x = stream[:n]
        s = x.sum()
        curves[str(n)] = {"ll": (s * np.log(th) - n * th) / n, "argmax": float(x.mean())}
    expected = lam0 * np.log(th) - th
    return nest({"lam0": lam0, "theta": th, "curves": curves, "expected": expected})


def compute_asymp():
    g = rng(1922)
    n, R = 50, 4000
    mles, meds = [], []
    for _ in range(R):
        x = g.standard_cauchy(n)
        mles.append(M.cauchy_mle(x))
        meds.append(float(np.median(x)))
    return nest({"n": n, "R": R, "mle": np.asarray(mles), "med": np.asarray(meds), "sd_mle": float(np.std(mles)),
                 "sd_med": float(np.std(meds)), "theory_mle": float(np.sqrt(2 / n)), "theory_med": float(np.pi / (2 * np.sqrt(n)))})


def compute_efron():
    g = rng(1978)
    n, R = 20, 8000
    t, J = [], []
    for _ in range(R):
        x = g.standard_cauchy(n)
        m = M.cauchy_mle(x)
        t.append(m)
        J.append(M.cauchy_observed_info(x, m))
    t, J = np.asarray(t), np.asarray(J)
    q = np.quantile(J, [0, 0.25, 0.5, 0.75, 1.0])
    bins = []
    for k in range(4):
        m = (J >= q[k]) & (J <= q[k + 1])
        bins.append({"J": float(J[m].mean()), "var": float(np.var(t[m])), "inv_J": float(np.mean(1 / J[m]))})
    return nest({"n": n, "R": R, "expected_var": 2 / n, "bins": bins, "J_q": q, "overall_var": float(np.var(t))})


def compute_gamma():
    idx = W.sample(150, among=W.adult, seed=2201)
    x = W.income[idx] / 1000
    # Retain the entire seeded sample, including any upper-tail observations.
    a_grid = np.linspace(0.8, 4.5, 140)
    b_grid = np.linspace(0.01, 0.12, 140)
    ll = np.array([[M.gamma_loglik(x, a, b) for a in a_grid] for b in b_grid])
    pr = M.gamma_profile(x, np.linspace(0.8, 4.5, 3701))
    mean, meanlog = float(x.mean()),float(np.log(x).mean())
    a_hat = optimize.brentq(lambda a: np.log(a)-digamma(a)-np.log(mean)+meanlog,1e-4,1e4)
    b_hat = a_hat/mean
    H = len(x)*np.array([[-polygamma(1,a_hat),1/b_hat],[1/b_hat,-a_hat/b_hat**2]])
    se = np.sqrt(np.diag(np.linalg.inv(-H)))
    top = M.gamma_loglik(x,a_hat,b_hat)
    cut = top-stats.chi2.ppf(.95,1)/2
    f = lambda a: M.gamma_loglik(x,a,a/mean)-cut
    inside = [optimize.brentq(f,1e-5,a_hat),optimize.brentq(f,a_hat,10*a_hat)]
    corr = float(np.linalg.inv(-H)[0, 1] / (se[0] * se[1]))
    return nest({"n": len(x), "a_grid": a_grid, "b_grid": b_grid, "ll": ll, "a_hat": a_hat, "b_hat": b_hat, "se": se,
                 "wald": [a_hat - 1.96 * se[0], a_hat + 1.96 * se[0]], "profile_ci": [float(min(inside)), float(max(inside))],
                 "loglik_max":top, "prof_a": pr["shapes"][::10], "prof_ll": pr["profile"][::10], "corr": corr, "mean": float(x.mean())})


def compute_trinity():
    r = M.binomial_trinity(14, 20, 0.5)
    p = np.linspace(0.3, 0.92, 300)
    ll = 14 * np.log(p) + 6 * np.log(1 - p)
    return nest({**r, "x": 14, "n": 20, "p0": 0.5, "grid": p, "ll": ll,
                 "score0": 14 / 0.5 - 6 / 0.5, "info0": 20 / (0.5 * 0.5), "info_hat": 20 / (0.7 * 0.3)})


def compute_hauck():
    g = rng(1977)
    n, R = 60, 300
    betas = [0, 1, 2, 3, 4, 5, 6, 7]
    z, lr, retained = [], [], []
    for b in betas:
        zs, ls = [], []
        for _ in range(R):
            x = g.normal(size=n)
            y = (g.random(n) < 1 / (1 + np.exp(-b * x))).astype(float)
            r = logistic_slope_tests(x, y)
            if not r["finite"]:  # Complete separation: no finite MLE; disclose exclusions.
                continue
            zs.append(abs(r["z"]))
            ls.append(np.sqrt(max(r["lr"], 0)))
        retained.append(len(zs))
        z.append(float(np.median(zs)))
        lr.append(float(np.median(ls)))
    return nest({"n": n, "betas": betas, "wald_z": z, "lr_root": lr, "retained": retained, "attempted":R})


def compute_neyman():
    g = rng(1948)
    ests = [M.neyman_scott(1000, 1.0, g) for _ in range(300)]
    return nest({"pairs": 1000, "sigma2": 1.0, "mle": float(np.mean([e["mle"] for e in ests])),
                 "fixed": float(np.mean([e["fixed"] for e in ests])), "mle_sd": float(np.std([e["mle"] for e in ests])),
                 "mles": [e["mle"] for e in ests], "fixeds": [e["fixed"] for e in ests]})


def compute_kl():
    idx = W.sample(5000, among=W.adult, seed=2202)
    x = W.income[idx]
    lx = np.log(x)
    mu, sd = float(lx.mean()), float(lx.std())
    pop = W.income[W.adult]
    true_mean = float(pop.mean())
    implied_mean = float(np.exp(mu + sd ** 2 / 2))
    tail_true = float(np.mean(pop > 300_000))
    tail_model = float(stats.norm.sf((np.log(300_000) - mu) / sd))
    e = np.linspace(np.log(3000), np.log(2_000_000), 61)
    h, _ = np.histogram(lx, e, density=True)
    gr = (e[:-1] + e[1:]) / 2
    return nest({"mu": mu, "sd": sd, "true_mean": true_mean, "implied_mean": implied_mean, "tail_true": tail_true,
                 "tail_model": tail_model, "edges": e, "hist": h, "grid": gr, "dens": stats.norm.pdf(gr, mu, sd),
                 "median": float(np.median(x)), "true_median": float(np.median(pop))})


def nb_data(n, g, b=(0.5, 0.4), k=1.5):
    x = g.normal(size=n)
    mu = np.exp(b[0] + b[1] * x)
    y = g.negative_binomial(k, k / (k + mu))
    return np.column_stack([np.ones(n), x]), y


def compute_sandwich():
    g = rng(1967)
    X, y = nb_data(400, g)
    r = M.poisson_regression(X, y)
    return nest({"b": r["b"], "se_model": r["se_model"], "se_sandwich": r["se_sandwich"], "se_quasi": r["se_quasi"],
                 "phi": r["phi"], "mean": float(y.mean()), "var": float(y.var()), "y_hist": np.bincount(y.astype(int))[:15]})


def grouped_mix_loglik(upper, counts, theta):
    """Actual interval-probability likelihood, including both unbounded tail classes."""
    p,m1,s1,m2,s2 = theta
    edges = np.r_[-np.inf,np.asarray(upper,float)]
    prob = p*np.diff(stats.norm.cdf(edges,m1,s1))+(1-p)*np.diff(stats.norm.cdf(edges,m2,s2))
    counts = np.asarray(counts,float)
    use = counts>0
    return float(np.sum(counts[use]*np.log(np.maximum(prob[use],np.finfo(float).tiny))))


def compute_misbehave():
    x, w = museum.crabs()
    th = load("crabs")["theta"]
    j = int(np.argmax(w))  # put component 1's mean on the busiest interval
    sig = np.logspace(-1.5, -12, 80)
    ll = [M.mix_loglik(x, [th[0], x[j], s, th[3], th[4]], w) for s in sig]
    grouped = [grouped_mix_loglik(museum.CRAB_UPPER,w,[th[0],x[j],v,th[3],th[4]]) for v in sig]
    swapped = M.em_mixture(x, [1 - START[0], START[3], START[4], START[1], START[2]], w=w, iters=5000, tol=1e-13)["theta"]
    return nest({"sigma": sig, "ll": ll, "grouped_ll": grouped, "mu_at": float(x[j]), "ll_mle": float(load("crabs")["loglik"][-1]), "swapped": swapped})


def compute_ising():
    g = rng(1975)
    lat = M.ising_gibbs(48, 0.3, 400, g)
    hot = M.ising_gibbs(48, 0.6, 400, rng(1976))
    ests = [M.ising_pseudo_mle(M.ising_gibbs(48, 0.3, 300, rng(2000 + r)))["beta"] for r in range(12)]
    return nest({"lattice": lat, "lattice_strong": hot, "beta": 0.3, "est": ests, "est_mean": float(np.mean(ests)),
                 "est_sd": float(np.std(ests, ddof=1)), "one": M.ising_pseudo_mle(lat)["beta"], "sites": 48 * 48})


def compute_principle():
    p_bin = float(stats.binom.sf(8, 12, 0.5))  # P(X >= 9 | n = 12)
    p_nb = float(stats.nbinom.sf(8, 3, 0.5))  # heads before the 3rd tail: P(H >= 9)
    th = np.linspace(0.3, 0.98, 200)
    lik = th ** 9 * (1 - th) ** 3
    return nest({"p_binomial": p_bin, "p_negbin": p_nb, "theta": th, "lik": lik / lik.max()})


def compute_em_mm():
    """EM as minorize-maximize, along the mixing proportion alone (the other four held at the MLE)."""
    x, w = museum.crabs()
    th = np.asarray(load("crabs")["theta"])
    ps = np.linspace(0.02, 0.98, 300)

    def ll(p):
        return M.mix_loglik(x, [p, *th[1:]], w)

    f1, f2 = stats.norm.pdf(x, th[1], th[2]), stats.norm.pdf(x, th[3], th[4])
    pt, steps = 0.9, []
    for _ in range(4):
        r = pt * f1 / (pt * f1 + (1 - pt) * f2)
        a, b = w @ r, w @ (1 - r)
        q = lambda p: a * np.log(p) + b * np.log(1 - p)  # noqa: E731
        bound = ll(pt) + q(ps) - q(pt)  # touches ll at pt and lies below it everywhere
        nxt = a / (a + b)
        steps.append({"p": pt, "bound": bound, "next": float(nxt), "ll": ll(pt)})
        pt = float(nxt)
    return nest({"p": ps, "ll": np.array([ll(p) for p in ps]), "steps": steps, "p_hat": float(th[0])})


def compute_lrboot():
    """Parametric-bootstrap calibration of a specified SD-constrained EM improvement statistic."""
    x,w = museum.crabs()
    upper = np.asarray(museum.CRAB_UPPER)
    def statistic(counts):
        mu = float(counts@x/counts.sum())
        sd = float(np.sqrt(counts@(x-mu)**2/counts.sum()))
        starts = [[.5,mu-.5*sd,.8*sd,mu+.5*sd,.8*sd],
                  [.3,mu-sd,.7*sd,mu+.3*sd,.8*sd]]
        fit = midpoint_em(x,counts,starts)
        one = float(np.sum(counts*stats.norm.logpdf(x,mu,sd)))
        return max(0.,2*(fit["loglik"]-one))
    mu,sd = load("crabs")["one"]
    gen = rng(1985)
    lrs = np.array([statistic(binned_counts(gen.normal(mu,sd,int(w.sum())),upper)) for _ in range(200)])
    obs = statistic(w)
    exceed = int(np.sum(lrs>=obs))
    upper95 = float(stats.beta.ppf(.95,exceed+1,len(lrs)-exceed)) if exceed<len(lrs) else 1.
    return nest(dict(lr=lrs,q95=float(np.quantile(lrs,.95)),obs=obs,R=len(lrs),exceedances=exceed,
                     p_boot=(1+exceed)/(len(lrs)+1), exceedance_upper95=upper95,
                     min_sd=.002,statistic="same two-start SD-constrained midpoint-density EM improvement",
                     chi2_1=3.84,chi2_3=7.81))


def compute_board():
    g = rng(2222)
    R = 1000
    # (1) logistic slope, strong effect: Wald vs profile-likelihood intervals
    n, b_true = 50, 2.5
    wald_hit = lr_hit = 0
    for _ in range(R):
        x = g.normal(size=n)
        y = (g.random(n) < 1 / (1 + np.exp(-b_true * x))).astype(float)
        r = logistic_slope_tests(x, y)
        wald_hit += r["finite"] and abs(r["b"][1] - b_true) <= 1.96 * r["se"]
        lo, hi = logistic_profile_ci(x, y)
        lr_hit += lo <= b_true <= hi
    # (2) Neyman-Scott: Wald interval for sigma^2 from the MLE, 200 pairs
    ns_hit = 0
    for _ in range(R):
        e = M.neyman_scott(200, 1.0, g)
        se = e["mle"] / np.sqrt(200)  # inverse curvature of the n-pair profile likelihood
        ns_hit += abs(e["mle"] - 1.0) <= 1.96 * se
    # (3) Poisson regression of overdispersed counts: model-based vs sandwich
    mod_hit = sand_hit = 0
    for _ in range(R):
        X, y = nb_data(400, g)
        r = M.poisson_regression(X, y)
        mod_hit += abs(r["b"][1] - 0.4) <= 1.96 * r["se_model"][1]
        sand_hit += abs(r["b"][1] - 0.4) <= 1.96 * r["se_sandwich"][1]
    rows = [
        Row(22, r"Wald CI, logistic slope", r"$\beta = 2.5$, \ $n = 50$", "coverage", 0.95, wald_hit / R, R),
        Row(22, r"profile-likelihood CI", r"$\beta = 2.5$, \ $n = 50$", "coverage", 0.95, lr_hit / R, R),
        Row(22, r"MLE of $\sigma^2$, Wald CI", r"Neyman--Scott, \ 200 pairs", "coverage", 0.95, ns_hit / R, R),
        Row(22, r"Poisson model SE", r"overdispersed counts, \ $n = 400$", "coverage", 0.95, mod_hit / R, R),
        Row(22, r"sandwich SE", r"overdispersed counts, \ $n = 400$", "coverage", 0.95, sand_hit / R, R),
    ]
    save_rows(22, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]}


ITEMS = {
    "crabs": compute_crabs, "consistency": compute_consistency, "asymp": compute_asymp, "efron": compute_efron,
    "gamma": compute_gamma, "trinity": compute_trinity, "hauck": compute_hauck, "neyman": compute_neyman, "kl": compute_kl,
    "sandwich": compute_sandwich, "misbehave": compute_misbehave, "ising": compute_ising, "principle": compute_principle,
    "em_mm": compute_em_mm, "lrboot": compute_lrboot, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
