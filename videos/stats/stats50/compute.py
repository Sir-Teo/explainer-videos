"""Precompute every number in Part 50 of *Statistics, Built* ("Minimax Theory: the Limits of Estimation").

    OMP_NUM_THREADS=1 python -m videos.stats.stats50.compute            # everything missing (a few minutes)
    python -m videos.stats.stats50.compute --force board

Results are cached in ``.cache/stats50/<name>.json``.  Everything is exact arithmetic or a seeded simulation; the
Museum's motorcycle-crash data appear as the regression example.

Items:
    hook      Stone's rates n^(-2s/(2s+d)) for several (s, d); simulated pointwise KDE risk against n
    gsm       a regression function's Fourier coefficients against the noise level; the sequence-model picture
    pinsker   Pinsker's shrinkage weights and risk by eps; the asymptotic constant; the least favourable prior
    lecam     divergences; the two-point bound for a density at a point against a kernel estimator's risk
    fano      a Varshamov-Gilbert packing; sparse means: the s log(p/s) bound against soft thresholding
    assouad   the hypercube bound for Hoelder regression by n
    upper     risks over the ellipsoid: Pinsker, truncation, blockwise James-Stein, soft thresholding
    lepski    Lepski's bandwidth choice at a point: risk against the oracle and a fixed bandwidth
    detect    the detection boundary; higher criticism's power on a grid of (beta, r)
    clique    planted clique: the total-degree test's power by clique size
    mcycle    the motorcycle data: Lepski at three points
    board     Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict

import numpy as np
from scipy import stats, integrate, optimize

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import gsm as GK

CACHE = Cache("stats50")
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


def bernoulli_se(values):
    return float(np.std(values,ddof=1)/math.sqrt(len(values)))


def polynomial_bump(u):
    """C2 compact bump with supremum 1 and |second derivative| <= 6."""
    u=np.asarray(u,float)
    return np.maximum(1-u*u,0)**3


def lecam_density_pair(x,w,L=1.):
    if not 0<w<=.5 or L<1:raise ValueError("Use w in (0,.5] and L>=1")
    x=np.asarray(x,float);h=(L-stats.norm.pdf(0))*w*w/6
    if h>=stats.norm.pdf(1.5):raise ValueError("Positivity bound exceeded")
    base=stats.norm.pdf(x)
    return base,base+h*(polynomial_bump(x/w)-polynomial_bump((x-1)/w)),h


def lecam_density_point(n,s=2.,L=1.):
    """Valid C2 norm-one Gaussian-baseline density pair and product-TV bound."""
    if s!=2 or L!=1:raise ValueError("This explicit construction is for C2 norm one")
    nodes,weights=np.polynomial.legendre.leggauss(64)
    def candidate(w):
        h=(1-stats.norm.pdf(0))*w*w/6
        chi2=h*h*w*np.dot(weights,polynomial_bump(nodes)**2*(1/stats.norm.pdf(w*nodes)+1/stats.norm.pdf(1+w*nodes)))
        tv=min(1.,math.sqrt(n*chi2))
        return {"w":float(w),"h":float(h),"chi2":float(chi2),"tv":tv,"bound":h*h*(1-tv)/8}
    opt=optimize.minimize_scalar(lambda w:-candidate(w)["bound"],bounds=(1e-7,.5),method="bounded",options={"xatol":1e-12})
    best=max((candidate(opt.x),candidate(.5)),key=lambda x:x["bound"])
    return best|{"rate":n**(-.8),"class":"densities on R with max(||f||inf,||f prime||inf,||f second||inf)<=1","support_centres":[0.,1.],"bump":"(1-u squared)^3 positive part"}


def kde_uniform_upper(n):
    h=(1/(2*math.sqrt(math.pi)*n))**.2
    return {"h":h,"bound":h**4/4+1/(2*math.sqrt(math.pi)*n*h)}


def kde_normal_mse(n,h):
    mean=stats.norm.pdf(0)/math.sqrt(1+h*h)
    second=1/(2*math.pi*h*math.sqrt(h*h+2))
    return float((mean-stats.norm.pdf(0))**2+(second-mean*mean)/n)


def varshamov_gilbert(d,generator,trials=3000):
    """Exact original candidate stream and distance checks, accelerated by bit counts."""
    encoded=[];points=[]
    for _ in range(trials):
        v=generator.integers(0,2,d);code=sum(int(bit)<<j for j,bit in enumerate(v))
        if all((code^other).bit_count()>=d/8 for other in encoded):encoded.append(code);points.append(v)
    return {"M":len(points),"guarantee":2**(d/8),"pts":np.array(points),"trials":trials,"scope":"random finite search, existence theorem does not guarantee its output size"}


def assouad_holder(n,s=1.,L=1.):
    """Disjoint 0/1 bumps, exact fixed-design KL, conservative decision reduction."""
    if s not in (1.,2.):raise ValueError("Explicit Lipschitz or C2 construction only")
    x=np.arange(1,n+1)/n;best={"bound":0.}
    integral=2/3 if s==1 else integrate.quad(lambda u:float(polynomial_bump(u)**2),-1,1,epsabs=1e-13)[0]
    for m in range(1,400):
        cell=np.minimum((x*m).astype(int),m-1);u=2*m*x-(2*cell+1)
        b=np.maximum(1-np.abs(u),0) if s==1 else polynomial_bump(u)
        h_max=L*(1/(2*m))**s/(1 if s==1 else 6)
        unit_norms=np.bincount(cell,weights=b*b,minlength=m)
        tv_per_height=math.sqrt(float(unit_norms.max())/4)
        h=min(h_max,2/(3*tv_per_height)) if tv_per_height>0 else h_max
        norms=h*h*unit_norms
        kl=float(norms.max()/2);tv=min(1.,math.sqrt(kl/2))
        sep=h*h*integral/(2*m);bound=m*sep*(1-tv)/8
        if bound>best["bound"]:best={"bound":bound,"m":m,"h":h,"max_neighbour_kl":kl,"tv_upper":tv,"coordinate_l2_separation_squared":sep}
    return best|{"rate":n**(-2*s/(2*s+1)),"loss":"integrated squared error; unrestricted estimates reduced to binary decisions"}


def lepski(ests,sds,kappa=2.2):
    """Largest admissible index; a rejected intermediate index does not stop search."""
    return max(j for j in range(len(ests)) if all(abs(ests[j]-ests[i])<=kappa*sds[i] for i in range(j)))


def higher_criticism(x,alpha0=.5):
    """Positive sup of standardized CDF excess over t in [1/n,alpha0]."""
    x=np.atleast_2d(np.asarray(x,float));n=x.shape[1];p=np.sort(stats.norm.sf(x),axis=1)
    lo=1/n
    if not lo<=alpha0<1:raise ValueError("Need 1/n <= alpha0 < 1")
    ranks=np.arange(1,n+1)/n
    valid=(p>=lo)&(p<=alpha0)
    denom=np.sqrt(np.clip(p,lo,alpha0)*(1-np.clip(p,lo,alpha0)))
    interior=np.where(valid,math.sqrt(n)*(ranks[None,:]-p)/denom,-np.inf).max(axis=1)
    lower=math.sqrt(n)*((p<=lo).mean(axis=1)-lo)/math.sqrt(lo*(1-lo))
    upper=math.sqrt(n)*((p<=alpha0).mean(axis=1)-alpha0)/math.sqrt(alpha0*(1-alpha0))
    return np.maximum.reduce([interior,lower,upper,np.zeros(len(x))])


def fixed_window_risks(f,x0,n,hs):
    x=np.arange(1,n+1)/n;truth=float(f(np.array([x0]))[0]);result=[]
    for h in hs:
        values=f(x[np.abs(x-x0)<=h]);result.append(float((values.mean()-truth)**2+1/len(values)))
    return np.array(result)


def bias_aware_radius(x,x0,h,L1,L2,alpha=.05):
    dx=np.asarray(x)[np.abs(np.asarray(x)-x0)<=h]-x0
    bias=L1*abs(dx.mean())+L2*np.mean(dx*dx)/2
    return float(bias+stats.norm.ppf(1-alpha/2)/math.sqrt(len(dx))),float(bias)


# ---------------------------------------------------------------------------------------------------------------
def kde_at(x, x0, h):
    return np.mean(np.exp(-0.5 * ((x - x0) / h) ** 2), axis=-1) / (math.sqrt(2 * math.pi) * h)


def compute_hook():
    ns = np.logspace(2, 6, 41)
    curves = {}
    for s, d in ((2, 1), (2, 2), (2, 4), (2, 8), (4, 8)):
        curves[f"{s}_{d}"] = (ns ** (-2 * s / (2 * s + d))).tolist()
    # a normal density at 0, kernel estimate with the MSE-optimal bandwidth: risk ~ n^(-4/5)
    r = rng(5001)
    f0 = 1 / math.sqrt(2 * math.pi)
    sim = []
    for n in (100, 400, 1600, 6400):
        h = 1.06 * n ** (-0.2)
        reps = 2000 if n <= 1600 else 600
        e = [kde_at(r.standard_normal(n), 0.0, h) - f0 for _ in range(reps)]
        sim.append({"n": n, "mse": float(np.mean(np.square(e))),"exact_mse":kde_normal_mse(n,h),"reps":reps,"bandwidth":h})
    return {"ns": ns, "curves": curves, "sim": sim}


def compute_gsm():
    t = np.linspace(0, 1, 512, endpoint=False)
    f = np.sin(4 * np.pi * t) * np.exp(-2 * t) + 0.5 * np.abs(t - 0.5)
    K = 64
    k = np.arange(1, K + 1)
    basis = np.sqrt(2) * np.cos(np.pi * np.outer(k, t))
    theta = basis @ f / len(t)
    out = {"t": t, "f": f, "k": k, "theta": np.abs(theta)}
    for n in (100, 10000):
        out[f"eps{n}"] = 1 / math.sqrt(n)
    r = rng(5002)
    out["y100"] = np.abs(theta + r.standard_normal(K) / 10)
    return out


def compute_pinsker():
    a = GK.sobolev_weights(4000, 1.0)
    eps_list = [0.1, 0.03, 0.01, 0.003, 0.001]
    rows = []
    for eps in eps_list:
        p = GK.pinsker(eps, a, 1.0)
        rows.append({"eps": eps, "risk": p["risk"], "asym": GK.pinsker_asymptotic(eps, 1.0, 1.0), "N": p["N"], "bayes": p["bayes"]})
    w = {}
    for eps in (0.03, 0.003):
        p = GK.pinsker(eps, a[:200], 1.0)
        w[str(eps)] = p["shrink"][:120]
        w[f"prior{eps}"] = np.sqrt(p["prior_var"][:120])
    return {"rows": rows, "weights": w, "const": GK.pinsker_constant(1.0), "const2": GK.pinsker_constant(2.0), "k": np.arange(1, 121)}


def compute_lecam():
    div = []
    for d in (0.25, 0.5, 1.0, 2.0, 3.0):
        div.append({"d": d, "tv": GK.tv_normal(d), "h2": GK.hellinger2_normal(d), "kl": GK.kl_normal(d), "pinsker": min(1, math.sqrt(GK.kl_normal(d) / 2))})
    ns = [250, 1000, 4000, 16000, 64000]
    lower = [lecam_density_point(n, s=2.0, L=1.0)["bound"] for n in ns]
    # an upper bound: the kernel estimate of a smooth density at a point, its simulated MSE
    r = rng(5003)
    upper = []
    f0 = 1 / math.sqrt(2 * math.pi)
    for n in ns:
        h = 1.06 * n ** (-0.2)
        reps = 1000 if n <= 4000 else 200
        e = [kde_at(r.standard_normal(n), 0.0, h) - f0 for _ in range(reps)]
        upper.append(float(np.mean(np.square(e))))
    best = lecam_density_point(4000, s=2.0, L=1.0)
    return {"div": div, "ns": ns, "lower": lower, "normal_mse_mc": upper,"upper":[kde_uniform_upper(n)["bound"] for n in ns], "best": best,"scope":"valid C2 norm-one pair lower bound and uniform Gaussian-KDE upper bound; normal risk stored separately"}


def compute_fano():
    r = rng(5004)
    vg = varshamov_gilbert(24, r, trials=3000)
    p, n = 1000, 1
    rows = []
    for s in (1, 5, 20, 50, 100):
        th = np.zeros(p)
        th[:s] = 3.0 * math.sqrt(2 * math.log(p / s))  # well above the threshold: the worst case is near here
        lam = math.sqrt(2 * math.log(p / s))
        y = th[None, :] + r.standard_normal((400, p))
        risk_soft = float(np.mean(np.sum((GK.est_soft(y, lam) - th) ** 2, axis=1)))
        risk_mle = float(p)
        rows.append({"s": s, "rate": GK.sparse_means_rate(n, p, s), "soft": risk_soft, "mle": risk_mle, "lam": lam})
    return {"vg_M": vg["M"], "vg_guarantee": vg["guarantee"], "d": 24, "p": p, "rows": rows}


def compute_assouad():
    ns = [100, 1000, 10000, 100000]
    out = {"ns": ns, "s1": [assouad_holder(n, 1.0)["bound"] for n in ns], "s2": [assouad_holder(n, 2.0)["bound"] for n in ns],
           "m1": [assouad_holder(n, 1.0)["m"] for n in ns]}
    return out


def compute_upper():
    a = GK.sobolev_weights(1024, 1.0)
    r = rng(5005)
    rows = []
    for eps in (0.05, 0.02, 0.008, 0.003):
        p = GK.pinsker(eps, a, 1.0)
        th = GK.hardest_theta(eps, a, 1.0)
        y = th[None, :] + eps * r.standard_normal((300, len(a)))
        risk = lambda e: float(np.mean(np.sum((e - th) ** 2, axis=1)))  # noqa: E731
        cutoffs=np.arange(len(a)+1)
        trunc_risk=cutoffs*eps**2+np.r_[np.cumsum(th[::-1]**2)[::-1],0.]
        cutoff=int(np.argmin(trunc_risk));trunc=risk(GK.est_truncation(y,cutoff))
        rows.append({"eps": eps, "bound": p["risk"], "pinsker": risk(GK.est_linear(y, p["shrink"])), "trunc_best": trunc,"oracle_cutoff":cutoff,"oracle_truth_risk":float(trunc_risk[cutoff]),"scope":"risk at one Pinsker-worst truth, not supremum risk for every estimator",
                     "bjs": risk(GK.est_block_js(y, eps)), "soft": risk(GK.est_soft(y, eps * math.sqrt(2 * math.log(len(a)))))})
    return {"rows": rows}


def lepski_rep(f, x0, n, hs, r, kappa=2.2):
    ests, sds = [], []
    x = np.arange(1, n + 1) / n
    y = f(x) + r.standard_normal(n)
    for h in hs:
        m = np.abs(x - x0) <= h
        ests.append(y[m].mean())
        sds.append(1 / math.sqrt(m.sum()))
    ests, sds = np.array(ests), np.array(sds)
    j = lepski(ests, sds, kappa)
    return ests, sds, j


def compute_lepski():
    r = rng(5006)
    hs = np.array([0.0025, 0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32])
    funcs = {"smooth": (lambda x: np.sin(2 * np.pi * x), 0.25), "kink": (lambda x: 3 * np.abs(x - 0.5) ** 0.5, 0.5)}
    n = 4000
    out = {"hs": hs, "n": n}
    for name, (f, x0) in funcs.items():
        risk_by_h = np.zeros(len(hs))
        lep, chosen = [], []
        reps = 1500
        f0 = f(np.array([x0]))[0]
        for _ in range(reps):
            e, sd, j = lepski_rep(f, x0, n, hs, r)
            risk_by_h += (e - f0) ** 2
            lep.append((e[j] - f0) ** 2)
            chosen.append(j)
        risk_mc=risk_by_h/reps
        risk_by_h=fixed_window_risks(f,x0,n,hs)
        out[name] = {"risk_by_h": risk_by_h,"risk_by_h_mc":risk_mc,"kappa":2.2,"reps":reps, "lepski": float(np.mean(lep)), "oracle": float(risk_by_h.min()), "fixed": float(risk_by_h[4]),
                     "chosen": np.bincount(chosen, minlength=len(hs)) / reps}
    return out


def compute_detect():
    r = rng(5007)
    n = 10000
    betas = np.linspace(0.5, 1.0, 51)
    boundary = [GK.detection_boundary(b) for b in betas]
    null = higher_criticism(r.standard_normal((400, n)))
    crit = float(np.quantile(null, 0.95))
    nullmax = np.max(r.standard_normal((400, n)), axis=1)
    critmax = float(np.quantile(nullmax, 0.95))
    grid = []
    for b in (0.6, 0.7, 0.8, 0.9):
        for rr in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8):
            x = GK.sparse_mixture(n, b, rr, r, reps=150)
            hc = higher_criticism(x)
            mx = np.max(x, axis=1)
            grid.append({"beta": b, "r": rr, "hc": float(np.mean(hc > crit)), "max": float(np.mean(mx > critmax)),
                         "above": rr > GK.detection_boundary(b)})
    return {"n": n, "betas": betas, "boundary": boundary, "grid": grid, "crit": crit}


def compute_clique():
    r=rng(5008);n=400;N=n*(n-1)//2;reps=150
    cutoff=int(stats.binom.ppf(.95,N,.5));rows=[]
    for k in (0,10,20,30,40,60,80):
        planted=k*(k-1)//2
        st=np.array([GK.degree_stat(GK.planted_clique(n,k,r)) for _ in range(reps)])
        hit=st>(cutoff-N/2)/math.sqrt(N/4)
        rows.append({"k":k,"power":float(hit.mean()),"exact_power":float(stats.binom.sf(cutoff-planted,N-planted,.5)),"mc_se":bernoulli_se(hit)})
    return {"n":n,"rows":rows,"sqrt_n":math.sqrt(n),"log_n":2*math.log2(n),"null_edge_cutoff":cutoff,"reps":reps,"null_size":float(stats.binom.sf(cutoff,N,.5))}


def compute_mcycle():
    x, y = museum.mcycle()
    x, y = np.asarray(x, float), np.asarray(y, float)
    o = np.argsort(x)
    x, y = x[o], y[o]
    sigma = float(np.std(np.diff(y)) / math.sqrt(2))
    hs = np.array([1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0, 16.0])
    out = {"x": x, "y": y, "sigma": sigma, "hs": hs, "points": []}
    for x0 in (14.0, 22.0, 40.0):
        ests, sds = [], []
        for h in hs:
            m = np.abs(x - x0) <= h
            if m.sum() < 2:
                ests.append(np.nan)
                sds.append(np.inf)
                continue
            ests.append(float(y[m].mean()))
            sds.append(sigma / math.sqrt(m.sum()))
        ests, sds = np.array(ests), np.array(sds)
        ok = np.isfinite(ests)
        j = lepski(ests[ok], sds[ok])
        out["points"].append({"x0": x0, "h": float(hs[ok][j]), "est": float(ests[ok][j]), "se": float(sds[ok][j])})
    return out


def compute_board():
    r = rng(5010)
    n, reps = 2000, 1500
    f = lambda x: np.sin(2 * np.pi * x) + 2 * np.exp(-200 * (x - 0.5) ** 2)  # noqa: E731
    x0 = 0.5
    truth = float(f(np.array([x0]))[0])
    x = np.arange(1, n + 1) / n
    hs = np.array([0.0025, 0.005, 0.01, 0.02, 0.04, 0.08, 0.16])
    # Preserve an independent pilot comparison; choose the oracle using exact bias plus variance.
    risk = np.zeros(len(hs))
    for _ in range(400):
        y = f(x) + r.standard_normal(n)
        risk += np.array([(y[np.abs(x - x0) <= h].mean() - truth) ** 2 for h in hs])
    pilot_risk_mc=risk/400
    risk=fixed_window_risks(f,x0,n,hs)
    h_opt=float(hs[int(np.argmin(risk))])
    idx = list(hs).index(h_opt)
    h_under = float(hs[max(0, idx - 2)])
    L1=2*math.pi+40*math.exp(-.5);L2=4*math.pi**2+800
    radii=[bias_aware_radius(x,x0,h,L1,L2)[0] for h in hs]
    h_bias=float(hs[int(np.argmin(radii))]);bias_radius,bias_bound=bias_aware_radius(x,x0,h_bias,L1,L2)
    hit = {"opt": [], "under": [], "lepski": [],"bias_aware":[]}
    for _ in range(reps):
        y = f(x) + r.standard_normal(n)
        for key, h in (("opt", h_opt), ("under", h_under)):
            m = np.abs(x - x0) <= h
            e, se = y[m].mean(), 1 / math.sqrt(m.sum())
            hit[key].append(abs(e - truth) <= 1.96 * se)
        ests = np.array([y[np.abs(x - x0) <= h].mean() for h in hs])
        sds = np.array([1 / math.sqrt(np.sum(np.abs(x - x0) <= h)) for h in hs])
        j = lepski(ests, sds)
        hit["lepski"].append(abs(ests[j] - truth) <= 1.96 * sds[j])
        hit["bias_aware"].append(abs(y[np.abs(x-x0)<=h_bias].mean()-truth)<=bias_radius)
    rows = [Row(50, r"pointwise CI, \ MSE-optimal bandwidth", r"a peak at $x_0$, \ $n = 2{,}000$", "coverage", 0.95, float(np.mean(hit["opt"])), reps,mc_se=bernoulli_se(hit["opt"])),
            Row(50, r"pointwise CI, \ undersmoothed (bandwidth / 4)", r"a peak at $x_0$, \ $n = 2{,}000$", "coverage", 0.95, float(np.mean(hit["under"])), reps,mc_se=bernoulli_se(hit["under"])),
            Row(50, r"pointwise CI, \ Lepski's bandwidth", r"a peak at $x_0$, \ $n = 2{,}000$", "coverage", 0.95, float(np.mean(hit["lepski"])), reps,mc_se=bernoulli_se(hit["lepski"])),
            Row(50,r"pointwise CI, bias-aware fixed bandwidth",r"known Gaussian noise; derivative-bounded class","coverage",.95,float(np.mean(hit["bias_aware"])),reps,mc_se=bernoulli_se(hit["bias_aware"]))]
    # higher criticism: the asymptotic critical value (sqrt(2 log log n)) against a simulated one
    nn = 2000
    null = higher_criticism(r.standard_normal((3000, nn)))
    asym = math.sqrt(2 * math.log(math.log(nn)))
    sim_crit = float(np.quantile(higher_criticism(r.standard_normal((3000, nn))), 0.95))
    rows.append(Row(50, r"higher criticism, \ leading null scale (not 5-percent calibrated)", r"null $N(0,1)$, \ $n = 2{,}000$", "size", 0.05, float(np.mean(null > asym)), 3000,extra="5-percent comparison benchmark only; leading scale is not a level-specific cutoff",mc_se=bernoulli_se(null>asym)))
    rows.append(Row(50, r"higher criticism, \ simulated critical value", r"null $N(0,1)$, \ $n = 2{,}000$", "size", 0.05, float(np.mean(null > sim_crit)), 3000,mc_se=bernoulli_se(null>sim_crit)))
    save_rows(50, rows)
    return {"rows": [asdict(q) | {"verdict": q.verdict, "se": q.se} for q in rows], "h_opt": h_opt, "h_under": h_under, "hs": hs,
            "risk_by_h": risk,"pilot_risk_mc":pilot_risk_mc,"h_bias_aware":h_bias,"bias_aware_radius":bias_radius,"bias_bound":bias_bound,"derivative_bounds":{"L1":L1,"L2":L2},"independent_datasets":reps,"hc_evaluation_datasets":3000,"hc_calibration_datasets":3000,"asym_scope":"leading null scale, not a nominal 5-percent critical value", "asym": asym, "sim_crit": sim_crit}


ITEMS = {
    "hook": compute_hook, "gsm": compute_gsm, "pinsker": compute_pinsker, "lecam": compute_lecam, "fano": compute_fano,
    "assouad": compute_assouad, "upper": compute_upper, "lepski": compute_lepski, "detect": compute_detect,
    "clique": compute_clique, "mcycle": compute_mcycle, "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
