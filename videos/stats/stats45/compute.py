"""Precompute every number in Part 45 of *Statistics, Built* ("The Theory of Estimation").

    OMP_NUM_THREADS=1 python -m videos.stats.stats45.compute            # everything missing (a few minutes)
    python -m videos.stats.stats45.compute --force board

Results are cached in ``.cache/stats45/<name>.json``.  Ruggles & Brodie's tanks, Efron & Morris's hitters and Efron &
Hastie's insurance claims are the Museum's; everything else is exact arithmetic or a seeded simulation.

Items:
    hook        James-Stein's exact risk against the MLE's in 3, 5 and 10 dimensions
    decision    a finite problem (a fair or a biased coin): 16 rules, the risk set, Bayes rules, minimax
    binomial    exact risk functions for a proportion: the MLE, Bayes rules, the constant-risk minimax rule
    complete    Bayes rules tracing the boundary; Beta(eps, eps) rules converging to the MLE; S^2's inadmissibility
    expfam      A, A', A'' and A* for the Bernoulli and Poisson families; KL as a Bregman divergence
    suff        the tank estimators exactly; Rao-Blackwell given the maximum; the absurd unbiased estimator
    basu        xbar and s^2 independent; Cox's instruments; the uniform location family given its range
    info        Cramer-Rao for the normal; Bhattacharyya for theta^2; Chapman-Robbins for the uniform
    pitman      mean, median and Pitman estimators under four location families
    stein       Stein's lemma checked; James-Stein's exact risk; SURE against the loss on Efron-Morris's hitters
    brown       Brown's integrals and Brownian hitting probabilities in one, two and three dimensions
    minimax     Baranchik's family, positive-part James-Stein and Strawderman's proper Bayes rule in five dimensions
    eb          Robbins, the gamma fit and the NPMLE on the insurance claims; normal-means regret by n
    board       Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np
from scipy import stats, optimize
from scipy.integrate import quad

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import decision as DK
from explainer.stats.kit import shrink as SH

CACHE = Cache("stats45")
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


def coverage_row(method,setting,covered):
    covered=np.asarray(covered,float)
    return Row(45,method,setting,"coverage",.9,float(covered.mean()),len(covered),
               mc_se=float(covered.std(ddof=1)/np.sqrt(len(covered))))


def uniform_midrange_halfwidth(n,level=.9):
    """Exact unconditional quantile: P(|midrange-theta|>c)=(1-2c)**n."""
    return (1-(1-level)**(1/n))/2


def poisson_mixture(counts,tolerance=1e-7):
    """Fit a continuous-support Poisson mixture and certify its likelihood gap.

    The directional score is exp(-theta) times a degree-max(x) polynomial.
    Its stationary points and endpoints give the global KKT maximum; moving
    atoms above max(x) down to max(x) increases every observed probability.
    A normalized score gap bounds the per-observation log-likelihood gap.
    """
    f=np.asarray(counts,float);n=f.sum();x=np.arange(len(f));upper=float(x[f>0].max())
    atoms=np.unique([0.,np.dot(x,f)/n,upper]);weights=np.full(len(atoms),1/len(atoms))
    last=None
    for iteration in range(80):
        k=len(atoms)
        def objective(z,gradient=False):
            w,t=z[:k],z[k:];L=stats.poisson.pmf(x[:,None],t[None,:]);m=np.maximum(L@w,1e-300)
            value=-np.dot(f/n,np.log(m));gw=-((f/n)/m)@L
            derivative=np.empty_like(L)
            positive=t>1e-12
            derivative[:,positive]=L[:,positive]*(x[:,None]/t[None,positive]-1)
            derivative[:,~positive]=0.
            derivative[0,~positive]=-1.
            if len(x)>1:derivative[1,~positive]=1.
            gt=-(((f/n)/m)@derivative)*w
            return (value,np.r_[gw,gt])
        fit=optimize.minimize(objective,np.r_[weights,atoms],jac=True,method="SLSQP",
            bounds=[(0,1)]*k+[(0,upper)]*k,
            constraints=[dict(type="eq",fun=lambda z:z[:k].sum()-1,jac=lambda z:np.r_[np.ones(k),np.zeros(k)])],
            options=dict(ftol=1e-13,maxiter=2000))
        weights=np.maximum(fit.x[:k],0);weights/=weights.sum();atoms=fit.x[k:]
        active=weights>1e-9;weights,atoms=weights[active],atoms[active];weights/=weights.sum()
        L=stats.poisson.pmf(x[:,None],atoms[None,:]);m=L@weights
        # coefficients of P, with no numerical differentiation of the score.
        coefficients=(f/n)/m/np.array([math.factorial(int(j)) for j in x])
        polynomial=np.polynomial.Polynomial(coefficients)
        roots=(polynomial.deriv()-polynomial).roots()
        candidates=np.r_[0.,upper,[z.real for z in roots if abs(z.imag)<1e-7 and 0<z.real<upper]]
        scores=np.exp(-candidates)*polynomial(candidates)
        best=int(np.argmax(scores));gap=max(0.,float(scores[best]-1))
        last=dict(grid=atoms,w=weights,post_mean=(L*weights)@atoms/m,
                  loglik=float(np.dot(f,np.log(m))),kkt_gap_per_observation=gap,
                  loglik_gap_bound=float(n*gap),iterations=iteration+1,
                  support_domain=[0.,upper],optimizer_success=bool(fit.success))
        if gap<tolerance:return last
        location=float(candidates[best])
        if np.min(abs(atoms-location))<1e-8:break
        atoms=np.r_[atoms,location];weights=np.r_[weights*.99,.01]
    raise RuntimeError(f"Poisson mixture likelihood certificate did not converge: {last}")


def oracle_normal_risk(weight=.1,signal=4.):
    """Population Bayes risk E Var(theta|X) under the stated two-point prior."""
    def integrand(x):
        f0=(1-weight)*stats.norm.pdf(x);f1=weight*stats.norm.pdf(x-signal)
        return signal**2*f0*f1/(f0+f1) if f0+f1>0 else 0.
    return quad(integrand,-np.inf,np.inf,epsabs=1e-11)[0]


# ---------------------------------------------------------------------------------------------------------------
def compute_hook():
    nrm = np.linspace(0, 30, 61)
    out = {"norm2": nrm}
    for p in (3, 5, 10):
        out[f"js{p}"] = DK.js_risk(p, nrm)
    # simulated James-Stein on Efron & Morris's hitters (Part 25), for the hook's reminder
    names, h, ab, avg = museum.efron_morris()
    out["js0_10"] = float(DK.js_risk(10, 0.0)[0])
    out["js0_3"] = float(DK.js_risk(3, 0.0)[0])
    out["n_hitters"] = len(names)
    return out


def coin_problem():
    px = np.array([stats.binom.pmf(range(4), 3, 0.5), stats.binom.pmf(range(4), 3, 0.8)])
    loss = np.array([[0.0, 1.0], [2.0, 0.0]])
    return px, loss


def compute_decision():
    px, loss = coin_problem()
    rp = DK.risk_points(px, loss)
    R = rp["R"]
    lb = DK.lower_boundary(R)
    bayes = {}
    for pi in (0.25, 0.5, 0.75):
        b = DK.bayes_rule(R, pi)
        bayes[str(pi)] = {"rule": rp["rules"][b["index"]], "point": b["point"], "risk": b["bayes_risk"]}
    mm = DK.minimax(R)
    # the threshold rules 'say biased when X >= c' are the boundary's vertices
    thresholds = {}
    for c in range(5):
        rule = tuple(int(x >= c) for x in range(4))
        thresholds[str(c)] = R[rp["rules"].index(rule)]
    # admissible non-randomized rules: on the lower boundary
    on_lb = [i for i, r in enumerate(R) if any(np.allclose(r, v) for v in lb)]
    return {"px": px, "loss": loss, "rules": rp["rules"], "R": R, "lower": lb, "bayes": bayes, "minimax": mm["value"],
            "minimax_point": mm["point"], "least_favourable": mm["least_favourable"][0], "weights": mm["weights"],
            "thresholds": thresholds, "admissible": on_lb}


def compute_binomial():
    n = 16
    p = np.linspace(0, 1, 201)
    a = math.sqrt(n) / 2
    out = {"n": n, "p": p, "mle": DK.binomial_mse(n, p), "bayes11": DK.binomial_mse(n, p, 1, 1),
           "minimax": DK.binomial_mse(n, p, a, a), "a": a}
    out["max_mle"] = 1 / (4 * n)
    out["max_minimax"] = 1 / (4 * (1 + math.sqrt(n)) ** 2)
    out["bayes_mle"] = DK.binomial_bayes_risk(n, 0, 0)
    out["bayes_11"] = DK.binomial_bayes_risk(n, 1, 1)
    out["bayes_minimax"] = DK.binomial_bayes_risk(n, a, a)
    # where the minimax rule beats the MLE, for several n
    region = {}
    for m in (16, 100, 1000):
        am = math.sqrt(m) / 2
        radius=.5*math.sqrt(1-m/(1+math.sqrt(m))**2)
        region[str(m)]=[.5-radius,.5+radius]
    out["region"] = region
    return out


def compute_complete():
    n = 16
    p = np.linspace(0, 1, 201)
    eps = [4.0, 1.0, 0.25, 0.05]
    curves = {str(e): DK.binomial_mse(n, p, e, e) for e in eps}
    # the boundary traced by Bayes rules of the coin problem as the prior moves
    px, loss = coin_problem()
    R = DK.risk_points(px, loss)["R"]
    pis = np.linspace(0.01, 0.99, 99)
    traced = np.array([DK.bayes_rule(R, q)["point"] for q in pis])
    # S^2 for sigma^2: the unbiased divisor n - 1 against n and n + 1
    n2 = 10
    c = np.linspace(0.04, 0.14, 101)
    return {"n": n, "p": p, "eps": eps, "curves": curves, "mle": DK.binomial_mse(n, p), "pis": pis, "traced": traced,
            "n2": n2, "c": c, "scale": DK.scale_mse(n2, c), "s_unbiased": float(DK.scale_mse(n2, 1 / (n2 - 1))),
            "s_mle": float(DK.scale_mse(n2, 1 / n2)), "s_best": float(DK.scale_mse(n2, 1 / (n2 + 1)))}


def compute_expfam():
    eta = np.linspace(-4, 4, 161)
    b = DK.expfam("bernoulli", eta)
    mu = np.linspace(0.005, 0.995, 199)
    astar = mu * np.log(mu) + (1 - mu) * np.log(1 - mu)
    eta_p = np.linspace(-2.5, 1.8, 161)
    po = DK.expfam("poisson", eta_p)
    # KL(Ber(m1) || Ber(m2)) as a Bregman divergence of A*
    m1, m2 = 0.3, 0.7
    kl = m1 * math.log(m1 / m2) + (1 - m1) * math.log((1 - m1) / (1 - m2))
    As = lambda m: m * math.log(m) + (1 - m) * math.log(1 - m)  # noqa: E731
    dAs = lambda m: math.log(m / (1 - m))  # noqa: E731
    breg = As(m1) - As(m2) - dAs(m2) * (m1 - m2)
    return {"eta": eta, "A": b["A"], "mu_eta": b["mu"], "V": b["V"], "mu": mu, "Astar": astar, "eta_p": eta_p,
            "A_p": po["A"], "V_p": po["V"], "m1": m1, "m2": m2, "kl": kl, "bregman": breg,
            "slope_at": 0.8, "A_at": float(np.logaddexp(0, 0.8)), "mu_at": float(1 / (1 + math.exp(-0.8)))}


def compute_suff():
    N, k = 300, 6
    t = DK.tank_estimators(N, k)
    g = rng(4501)
    reps = 20000
    draws = np.array([g.choice(N, k, replace=False) + 1 for _ in range(reps)])
    one = 2 * draws[:, 0] - 1
    mom = 2 * draws.mean(1) - 1
    M = draws.max(1)
    umvue = M * (k + 1) / k - 1
    # Rao-Blackwell picture: one serial against the maximum
    sel = slice(0, 600)
    ms = np.arange(k, N + 1)
    cond = {}
    for m in (150, 200, 250, 280, 300):
        s = M == m
        cond[str(m)] = float(np.mean(one[s])) if s.any() else None
    tanks = [{"month": r[0], "stat": r[1], "intel": r[2], "records": r[3]} for r in museum.TANKS]
    lam = np.linspace(0.01, 3, 120)
    ab = DK.absurd_umvue(lam)
    return {"N": N, "k": k, "sd": t, "sim_sd": {"one": float(one.std()), "mom": float(mom.std()), "umvue": float(umvue.std())},
            "sim_mean": {"one": float(one.mean()), "mom": float(mom.mean()), "umvue": float(umvue.mean())},
            "scatter_M": M[sel], "scatter_one": one[sel], "line_m": ms, "line": ms * (k + 1) / k - 1, "cond": cond,
            "tanks": tanks, "lam": lam, "absurd": ab}


def compute_basu():
    g = rng(4502)
    n = 10
    x = g.normal(0, 1, (4000, n))
    xb, s2 = x.mean(1), x.var(1, ddof=1)
    r = float(np.corrcoef(xb, s2)[0, 1])
    e = g.exponential(1, (4000, n))
    r_exp = float(np.corrcoef(e.mean(1), e.var(1, ddof=1))[0, 1])
    cox = DK.cox_instruments()
    # uniform location: midrange with its unconditional 90% half-width, coverage by range
    m = 5
    u = g.random((200000, m)) - 0.5
    mid = (u.max(1) + u.min(1)) / 2
    rng_ = u.max(1) - u.min(1)
    c_unc = uniform_midrange_halfwidth(m)
    bins = np.linspace(0, 1, 11)
    idx = np.digitize(rng_, bins) - 1
    cover_unc = [float(np.mean(np.abs(mid[idx == b]) <= c_unc)) for b in range(10)]
    cover_cond = [float(np.mean(np.abs(mid[idx == b]) <= 0.9 * (1 - rng_[idx == b]) / 2)) for b in range(10)]
    share = [float(np.mean(idx == b)) for b in range(10)]
    return {"n": n, "xbar": xb[:800], "s2": s2[:800], "r": r, "r_exp": r_exp, "cox": cox, "m": m, "c_unc": c_unc,
            "bins": bins, "cover_unc": cover_unc, "cover_cond": cover_cond, "share": share,
            "overall_unc": float(np.mean(np.abs(mid) <= c_unc)),
            "correlation_replicates":len(x), "scatter_replicates":800, "interval_calibration":"exact unconditional midrange law",
            "bin_counts":[int(np.sum(idx==b)) for b in range(10)],
            "overall_cond": float(np.mean(np.abs(mid) <= 0.9 * (1 - rng_) / 2))}


def compute_info():
    n = 10
    theta = np.linspace(0, 2, 81)
    b = DK.bhattacharyya_theta2(theta, n)
    ns = np.array([2, 3, 5, 10, 20, 50, 100])
    cr = [DK.chapman_robbins_uniform(int(m)) for m in ns]
    # the normal: S^2's variance against the multiparameter bound
    eff_s2 = [(m - 1) / m for m in (5, 10, 50)]
    return {"n": n, "theta": theta, "var_umvue": b["var_umvue"], "cr": b["cr"], "bhatt2": b["bhatt2"], "ns": ns,
            "cr_bound": [c["bound"] for c in cr], "cr_umvue": [c["var_umvue"] for c in cr], "cr_t": [c["t"] for c in cr],
            "eff_s2": eff_s2}


def pitman_estimate(sample,family):
    """Closed forms or whole-line quadrature split at all likelihood knots.

    Avoid a fixed window around the median: even a normal likelihood peak
    may lie outside it when observations have unequal extreme values.
    """
    sample=np.asarray(sample,float)
    if family=="normal":return float(sample.mean())
    if family=="uniform":return float((sample.min()+sample.max())/2)
    logf=(lambda z:-np.abs(z)) if family=="Laplace" else (lambda z:-np.log1p(z*z))
    center=float(np.median(sample));shifted=sample-center
    knots=np.unique(shifted)
    offset=max(float(np.sum(logf(shifted-point))) for point in knots)
    def likelihood(t):return float(np.exp(np.sum(logf(shifted-t))-offset))
    intervals=np.r_[-np.inf,knots,np.inf]
    denominator=numerator=0.
    for lo,hi in zip(intervals[:-1],intervals[1:]):
        denominator+=quad(likelihood,lo,hi,epsabs=1e-11,epsrel=1e-9,limit=150)[0]
        numerator+=quad(lambda t:t*likelihood(t),lo,hi,epsabs=1e-11,epsrel=1e-9,limit=150)[0]
    if not denominator>0:raise ArithmeticError("Pitman posterior normalizer must be positive")
    return center+numerator/denominator


def compute_pitman():
    g = rng(4503)
    n, reps = 5, 4000
    fams = {
        "normal": (lambda size: g.normal(0, 1, size), lambda z: -z ** 2 / 2),
        "Laplace": (lambda size: g.laplace(0, 1, size), lambda z: -np.abs(z)),
        "uniform": (lambda size: g.random(size) - 0.5, None),
        "Cauchy": (lambda size: g.standard_cauchy(size), lambda z: -np.log1p(z ** 2)),
    }
    out = {}
    for name, (draw, logf) in fams.items():
        x = draw((reps, n))
        mean, med = x.mean(1), np.median(x, 1)
        if logf is None:
            pit = (x.max(1) + x.min(1)) / 2
        else:
            pit = np.array([pitman_estimate(r,name) for r in x])
        mse = lambda e: float(np.mean(e ** 2))  # noqa: E731
        out[name] = {"mean": mse(mean) if name != "Cauchy" else None, "median": mse(med), "pitman": mse(pit),
                     "mean_med": float(np.median(np.abs(mean))), "rel": mse(pit) / mse(med)}
    out["uniform_exact"] = {"mean": 1 / (12 * n), "pitman": 1 / (2 * (n + 1) * (n + 2))}
    return {"n": n, "reps": reps, "fams": out, "integration":"closed forms for normal/uniform; whole-line adaptive quadrature split at observations for Laplace/Cauchy"}


def compute_stein():
    g = rng(4504)
    # Stein's lemma: E[(X - theta) h(X)] = E h'(X) for h = sin, theta = 0.7
    th = 0.7
    x = g.normal(th, 1, 400000)
    lhs, rhs = float(np.mean((x - th) * np.sin(x))), float(np.mean(np.cos(x)))
    exact = float(math.exp(-0.5) * math.cos(th))
    # Efron-Morris: arcsine-transformed batting averages, SURE against the realized loss
    names, h, ab, avg = museum.efron_morris()
    n = 45
    z = np.sqrt(n) * np.arcsin(2 * h / n - 1)
    truth = np.sqrt(n) * np.arcsin(2 * avg - 1)
    p = len(z)
    zb = z.mean()
    s = np.sum((z - zb) ** 2)
    js = zb + (1 - (p - 3) / s) * (z - zb)
    loss_mle, loss_js = float(np.sum((z - truth) ** 2)), float(np.sum((js - truth) ** 2))
    sure_js = float(p - (p - 3) ** 2 / s)
    # risk curves: exact James-Stein vs simulated positive part, p = 10
    pp = 10
    nrm = np.linspace(0, 40, 21)
    exact_js = DK.js_risk(pp, nrm)
    plus = []
    Z = g.normal(0, 1, (20000, pp))
    for v in nrm:
        theta = np.zeros(pp)
        theta[0] = math.sqrt(v)
        xx = Z + theta
        ss = np.sum(xx ** 2, 1, keepdims=True)
        est = np.maximum(0, 1 - (pp - 2) / ss) * xx
        plus.append(float(np.mean(np.sum((est - theta) ** 2, 1))))
    # SURE across replications at one theta: unbiased for the risk, scattered around the loss
    theta = np.full(pp, 1.0)
    xx = g.normal(theta, 1, (400, pp))
    ss = np.sum(xx ** 2, 1)
    sure_vals = pp - (pp - 2) ** 2 / ss
    losses = np.sum(((1 - (pp - 2) / ss)[:, None] * xx - theta) ** 2, 1)
    return {"lemma": {"lhs": lhs, "rhs": rhs, "exact": exact}, "em": {"loss_mle": loss_mle, "loss_js": loss_js,
            "sure_js": sure_js, "p": p, "risk_mle": float(p), "shrink": float(1 - (p - 3) / s)},
            "nrm": nrm, "exact_js": exact_js, "plus": plus, "sure": sure_vals, "loss": losses,
            "sure_mean": float(sure_vals.mean()), "loss_mean": float(losses.mean()),
            "risk_at": float(DK.js_risk(pp, 10.0)[0])}


def compute_brown():
    R = np.logspace(0.05, 6, 120)
    out = {"R": R}
    for p in (1, 2, 3):
        out[f"int{p}"] = DK.brown_integral(p, R) if p != 1 else R - 1
        out[f"hit{p}"] = DK.bm_hit_ball(p, 2.0, R[R>=2.])
    out["hit_R"] = R[R>=2.]
    out["hit3_inf"] = 0.5
    out["hit5_inf"] = 2.0 ** -3
    # the flat-prior marginal and Brown's condition for a proper-tailed prior: pi(theta) ~ |theta|^{-k}
    return out


def compute_minimax():
    g = rng(4505)
    p, a = 5, 0.5
    nrm = np.linspace(0, 40, 21)
    Z = g.normal(0, 1, (40000, p))
    risks = {"mle": [], "js": [], "jsplus": [], "straw": [], "bar": []}
    for v in nrm:
        theta = np.zeros(p)
        theta[0] = math.sqrt(v)
        x = Z + theta
        s = np.sum(x ** 2, 1)
        loss = lambda est: float(np.mean(np.sum((est - theta) ** 2, 1)))  # noqa: E731
        risks["mle"].append(loss(x))
        risks["js"].append(loss((1 - (p - 2) / s)[:, None] * x))
        risks["jsplus"].append(loss(np.maximum(0, 1 - (p - 2) / s)[:, None] * x))
        sh = DK.strawderman_shrink(s, p, a)
        risks["straw"].append(loss((1 - sh)[:, None] * x))
        r = lambda ss: np.minimum(1.0, ss / (p + 1))  # noqa: E731  Baranchik with r(s) = min(1, s/(p+1))
        risks["bar"].append(loss(DK.baranchik(x, r)))
    s = np.linspace(0.05, 30, 120)
    return {"p": p, "a": a, "nrm": nrm, "risks": risks, "s": s, "shrink_straw": 1 - DK.strawderman_shrink(s, p, a),
            "shrink_js": np.maximum(0, 1 - (p - 2) / s), "shrink_js_raw": 1 - (p - 2) / s}


def compute_eb():
    f = np.asarray(museum.INSURANCE_CLAIMS, float)
    rob = DK.robbins(f)
    gp = DK.gamma_poisson(f)
    npm = poisson_mixture(f)
    atoms = [(float(t), float(w)) for t, w in zip(npm["grid"], npm["w"]) if w > 1e-3]
    # normal means: regret of empirical Bayes estimators against the oracle Bayes rule, by n
    g = rng(4506)
    regret = {"n": [], "js": [], "npmle": [], "oracle": [], "replicates":[], "mc_se":[], "excess_npmle":[]}
    for n in (50, 200, 1000, 5000):
        js_l, np_l, or_l = [], [], []
        for rep in range(12 if n < 5000 else 4):
            mu = np.where(g.random(n) < 0.1, 4.0, 0.0)  # a sparse two-point prior: 10% at 4
            x = mu + g.normal(0, 1, n)
            s = np.sum((x - x.mean()) ** 2)
            js = x.mean() + max(0, 1 - (n - 3) / s) * (x - x.mean())
            fit = SH.npmle(x, 1.0, grid=np.linspace(-3, 8, 221), iters=1500)
            post = stats.norm.pdf(x, 4, 1) * 0.1
            orc = 4 * post / (post + 0.9 * stats.norm.pdf(x, 0, 1))
            js_l.append(np.mean((js - mu) ** 2))
            np_l.append(np.mean((fit["post_mean"] - mu) ** 2))
            or_l.append(np.mean((orc - mu) ** 2))
        regret["replicates"].append(len(np_l))
        regret["mc_se"].append({name:float(np.std(values,ddof=1)/np.sqrt(len(values))) for name,values in [("js",js_l),("npmle",np_l),("oracle",or_l)]})
        regret["excess_npmle"].append(float(np.mean(np.asarray(np_l)-or_l)))
        regret["n"].append(n)
        regret["js"].append(float(np.mean(js_l)))
        regret["npmle"].append(float(np.mean(np_l)))
        regret["oracle"].append(float(np.mean(or_l)))
    return {"counts": f, "robbins": rob, "gamma": gp["post_mean"], "nu": gp["nu"], "scale": gp["scale"],
            "npmle": npm["post_mean"], "atoms": atoms, "loglik_gamma": gp["loglik"], "loglik_npmle": npm["loglik"],
            "poisson_fit_certificate":{k:npm[k] for k in ("kkt_gap_per_observation","loglik_gap_bound","iterations","support_domain","optimizer_success")},
            "oracle_population_risk":oracle_normal_risk(),"normal_fit_scope":"221-point fixed-grid EM approximation; legacy regret key contains raw per-coordinate risks, not oracle-subtracted regret",
            "total": int(f.sum()), "mean": float(np.sum(np.arange(len(f)) * f) / f.sum()), "regret": regret}


def compute_board():
    g = rng(4599)
    rows = []
    reps = 20000
    cox = DK.cox_instruments()
    sd = np.where(g.random(reps) < 0.5, 1.0, 10.0)
    x = g.normal(0, 1, reps) * sd
    hit_unc = np.abs(x) <= cox["c"]
    hit_cond = np.abs(x) <= cox["z"] * sd
    precise = sd == 1.0
    rows.append(coverage_row("Cox's instruments, unconditional interval","given the precise instrument (SD 1)",hit_unc[precise]))
    rows.append(coverage_row("Cox's instruments, unconditional interval","given the rough instrument (SD 10)",hit_unc[~precise]))
    rows.append(coverage_row("Cox's instruments, conditional interval","given either instrument",hit_cond))
    # uniform location, conditional on the range
    m = 5
    u = g.random((reps, m)) - 0.5
    hit = np.array([lo <= 0 <= hi for lo, hi in (DK.uniform_location_interval(r) for r in u)])
    rows.append(coverage_row("uniform location, interval given the range","U(theta - 1/2, theta + 1/2), n = 5",hit))
    # James-Stein-centred intervals, p = 10, one large mean
    p = 10
    theta = np.zeros(p)
    theta[-1] = 5.0
    X = g.normal(theta, 1, (reps, p))
    s = np.sum(X ** 2, 1, keepdims=True)
    js = np.maximum(0, 1 - (p - 2) / s) * X
    cov = np.abs(js - theta) <= 1.645
    rows.append(coverage_row(r"positive-part James--Stein $\pm 1.645$, the large mean","p = 10, theta = (0, ..., 0, 5)",cov[:,-1]))
    rows.append(coverage_row(r"positive-part James--Stein $\pm 1.645$, a zero mean","p = 10, theta = (0, ..., 0, 5)",cov[:,0]))
    save_rows(45, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]}


ITEMS = {
    "hook": compute_hook, "decision": compute_decision, "binomial": compute_binomial, "complete": compute_complete,
    "expfam": compute_expfam, "suff": compute_suff, "basu": compute_basu, "info": compute_info, "pitman": compute_pitman,
    "stein": compute_stein, "brown": compute_brown, "minimax": compute_minimax, "eb": compute_eb, "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
