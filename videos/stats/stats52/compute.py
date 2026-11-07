"""Precompute every number in Part 52 of *Statistics, Built* ("High-Dimensional Statistics").

    OMP_NUM_THREADS=1 python -m videos.stats.stats52.compute            # everything missing (several minutes)
    python -m videos.stats.stats52.compute --force board

Results are cached in ``.cache/stats52/<name>.json``.  The diabetes data and Harman's 24 tests are the Museum's;
everything else is exact arithmetic or a seeded simulation.

Items:
    hook      PCA on pure noise, n = 1,000, p = 500: the spectrum against Marchenko-Pastur
    oracle    the lasso's l2 error by n against sqrt(s log p / n); the error by the penalty's multiplier
    support   exact signed-support recovery along the LARS path by Wainwright's rescaled n; an irrepresentable failure
    complete  matrix completion by SoftImpute by sampling fraction; the degrees-of-freedom line
    cov       banding, thresholding and Ledoit-Wolf against the sample covariance, AR(1), p = 200
    dk        Davis-Kahan's sin-theta bound against the actual angle, by spike size
    laws      Stieltjes inversion at several eta; Wigner's semicircle
    bbp       the top eigenvalue and the eigenvector overlap by spike, gamma = 1/2, against the BBP limits
    tw        the scaled top eigenvalue under the null against Tracy-Widom (beta = 1); Roy's test
    spca      sparse PCA: diagonal thresholding against PCA; neighbourhood selection on a chain graph
    harman    Harman's 24 tests: the correlation spectrum, MP edge, BBP-corrected spikes and overlaps
    diabetes  the LARS diabetes data with interactions (p = 64): lasso by CV and debiased intervals
    board     Coverage Board rows
"""

from __future__ import annotations

import math
from dataclasses import asdict
from scipy import linalg, stats

import numpy as np

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import hdstat as HS
from explainer.stats.kit import sparse as SPK

CACHE = Cache("stats52")
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


def lasso_lambda(X, sigma=1., delta=.05):
    """Conditional Gaussian union-bound penalty: lambda >=2||X'eps/n||inf with prob >=1-delta."""
    X = np.asarray(X, float)
    n,p = X.shape
    return 2*sigma*np.max(np.linalg.norm(X,axis=0))/n*math.sqrt(2*math.log(2*p/delta))


def checked_lasso(X,y,lam):
    b = SPK.lasso_cd(X,y,lam)
    grad = X.T@(y-X@b)/len(y)
    active = abs(b)>1e-9
    violation = max(np.max(abs(grad[active]-lam*np.sign(b[active])),initial=0),
                    np.max(np.maximum(abs(grad[~active])-lam,0),initial=0))
    if violation>1e-6*max(1.,lam):
        raise ArithmeticError(f"Lasso KKT residual {violation:g}")
    return b


def full_model_ols(X,y):
    """SVD covariance avoids squaring an already severe condition number."""
    U,d,Vh = np.linalg.svd(X,full_matrices=False)
    tol = np.finfo(float).eps*max(X.shape)*d[0]
    if d[-1]<=tol:
        raise ArithmeticError("Full model is rank deficient; unique coefficient intervals do not exist")
    b = Vh.T@((U.T@y)/d)
    residual = y-X@b
    sigma2 = residual@residual/(len(y)-X.shape[1]-1)  # fitted intercept
    cov = (Vh.T*(sigma2/d**2))@Vh
    return b,cov,float(d[0]/d[-1])


def nodewise_diagnostics(X,j,lam_node):
    others=np.delete(np.arange(X.shape[1]),j)
    g=SPK.lasso_cd(X[:,others],X[:,j],lam_node)
    residual=X[:,j]-X[:,others]@g
    tau2=residual@residual/len(X)+lam_node*abs(g).sum()
    theta=np.zeros(X.shape[1]);theta[j]=1;theta[others]=-g;theta/=tau2
    target=np.eye(X.shape[1])[j]
    return {"inverse_residual_inf":float(abs(theta@(X.T@X/len(X))-target).max()),
            "tau2":float(tau2),"node_selected":int(np.count_nonzero(g))}


def soft_impute_checked(M, observed, lam, Z0=None, max_iter=10000, tol=2e-7):
    """Accelerated proximal gradient for the stated masked nuclear-norm objective."""
    M=np.asarray(M,float);observed=np.asarray(observed,bool)
    Z=np.zeros_like(M) if Z0 is None else np.asarray(Z0,float).copy()
    Y=Z.copy();t=1.
    def prox(A):
        U,d,Vh=np.linalg.svd(A,full_matrices=False)
        return (U*np.maximum(d-lam,0))@Vh
    for iteration in range(1,max_iter+1):
        Zn=prox(np.where(observed,M,Y))
        tn=(1+math.sqrt(1+4*t*t))/2
        Yn=Zn+(t-1)/tn*(Zn-Z)
        # Restart on a direction that opposes the current gradient mapping.
        if np.sum((Y-Zn)*(Zn-Z))>0:
            tn=1.;Yn=Zn.copy()
        Z,Y,t=Zn,Yn,tn
        if iteration%10==0:
            residual=float(np.linalg.norm(Z-prox(np.where(observed,M,Z)))/max(1,np.linalg.norm(Z)))
            if residual<tol:
                return {"Z":Z,"iterations":iteration,"fixed_point_residual":residual}
    raise ArithmeticError(f"SoftImpute did not converge: residual={residual:g}")


def compute_hook():
    r = rng(5201)
    n, p = 1000, 500
    X = r.standard_normal((n, p))
    ev = np.sort(np.linalg.eigvalsh(X.T @ X / n))[::-1]
    g = p / n
    edges = np.linspace(0, 3.2, 65)
    counts, _ = np.histogram(ev, bins=edges)
    h = counts/(len(ev)*np.diff(edges))
    x = np.linspace(0.01, 3.2, 400)
    return {"n": n, "p": p, "gamma": g, "ev_max": ev[0], "ev_min": ev[-1], "mp": HS.mp_edges(g), "edges": edges, "hist": h,
            "x": x, "pdf": HS.mp_pdf(x, g), "top5": ev[:5], "share_top": ev[0] / ev.sum(), "share_true": 1 / p}


def compute_oracle():
    r = rng(5202)
    p, s = 500, 10
    ns = [100, 150, 200, 300, 400, 600, 800, 1200]
    rows = []
    for n in ns:
        errs, sizes = [], []
        for _ in range(12):
            X = r.standard_normal((n, p))
            beta = np.zeros(p)
            beta[:s] = r.choice([-1.0, 1.0], s)
            y = X @ beta + r.standard_normal(n)
            b = checked_lasso(X, y, lasso_lambda(X))
            errs.append(np.linalg.norm(b - beta))
            sizes.append(int(np.sum(b != 0)))
        rows.append({"n": n, "err": float(np.mean(errs)), "rate": HS.oracle_rate(n, p, s), "size": float(np.mean(sizes))})
    n = 400
    mults = [0.125, 0.25, 0.5, 1.0, 2.0, 4.0]
    lam_rows = []
    for c in mults:
        errs, sizes = [], []
        for _ in range(12):
            X = r.standard_normal((n, p))
            beta = np.zeros(p)
            beta[:s] = r.choice([-1.0, 1.0], s)
            y = X @ beta + r.standard_normal(n)
            b = checked_lasso(X, y, c * lasso_lambda(X))
            errs.append(np.linalg.norm(b - beta))
            sizes.append(int(np.sum(b != 0)))
        lam_rows.append({"mult": c, "err": float(np.mean(errs)), "size": float(np.mean(sizes))})
    return {"p": p, "s": s, "rows": rows, "lam_n": n, "lam_rows": lam_rows, "penalty_delta": .05, "penalty": "2 sigma max_j ||X_j|| sqrt(2 log(2p/delta))/n"}


def compute_support():
    r = rng(5203)
    s = 8
    thetas = [0.4, 0.6, 0.8, 1.0, 1.25, 1.5, 2.0]
    curves = {}
    for p in (128, 256, 512):
        succ = []
        for th in thetas:
            n = int(round(th * 2 * s * math.log(p - s)))
            ok = 0
            reps = 30
            for _ in range(reps):
                X = r.standard_normal((n, p))
                X = (X - X.mean(0)) / X.std(0)
                beta = np.zeros(p)
                beta[:s] = 0.5 * r.choice([-1.0, 1.0], s)
                y = X @ beta + 0.5 * r.standard_normal(n)
                y = y - y.mean()
                ok += HS.signed_support_on_path(X, y, beta)
            succ.append(ok / reps)
        curves[str(p)] = succ
    # an irrepresentable failure: a null column built from the signal columns
    n, p = 400, 50
    good, bad, irr_good, irr_bad = 0, 0, [], []
    for _ in range(30):
        X = r.standard_normal((n, p))
        beta = np.zeros(p)
        beta[:3] = 1.0
        Xb = X.copy()
        Xb[:, 3] = (X[:, 0] + X[:, 1] + X[:, 2]) / 3 * 1.2 + 0.4 * r.standard_normal(n)
        for M, tag in ((X, "good"), (Xb, "bad")):
            Z = (M - M.mean(0)) / M.std(0)
            bz = beta * M.std(0)
            y = M @ beta + 0.5 * r.standard_normal(n)
            y = y - y.mean()
            hit = HS.signed_support_on_path(Z, y, bz)
            v = HS.irrepresentable(Z, np.arange(3), np.ones(3))
            if tag == "good":
                good += hit
                irr_good.append(v)
            else:
                bad += hit
                irr_bad.append(v)
    return {"s": s, "thetas": thetas, "curves": curves, "reps_per_point": 30, "mcse": {key:[math.sqrt(v*(1-v)/29) for v in values] for key,values in curves.items()}, "irr": {"n": n, "p": p, "good": good / 30, "bad": bad / 30,
                                                               "irr_good": float(np.mean(irr_good)), "irr_bad": float(np.mean(irr_bad))}}


def compute_complete():
    r = rng(5204)
    n1 = n2 = 100
    rk = 3
    fracs = [0.04, 0.06, 0.08, 0.1, 0.15, 0.2, 0.3, 0.5]
    rows = []
    for f in fracs:
        errs, residuals, iterations = [], [], []
        for _ in range(4):
            M = HS.low_rank(n1,n2,rk,r)
            obs = r.random((n1,n2))<f
            Z=None
            for lam in (5.,2.,1.,.5,.2,.05):
                out=soft_impute_checked(M,obs,lam,Z0=Z);Z=out["Z"]
                residuals.append(out["fixed_point_residual"]);iterations.append(out["iterations"])
            errs.append(float(np.linalg.norm(Z-M)/np.linalg.norm(M)))
        rows.append({"frac":f,"err":float(np.median(errs)),"errors":errs,
                     "max_fixed_point_residual":max(residuals),"max_iterations":max(iterations)})
    dof = rk * (n1 + n2 - rk)
    return {"n": n1, "r": rk, "rows": rows, "dof": dof, "dof_frac": dof / (n1 * n2)}


def compute_cov():
    r = rng(5205)
    p, rho = 200, 0.7
    Sig = HS.ar1_cov(p, rho)
    L = np.linalg.cholesky(Sig)
    rows = []
    for n in (50, 100, 200, 400, 800):
        acc = {"sample": [], "band": [], "thresh": [], "lw": []}
        for _ in range(6):
            X = r.standard_normal((n, p)) @ L.T
            S = X.T @ X / n
            acc["sample"].append(HS.op_norm(S - Sig))
            acc["band"].append(min(HS.op_norm(HS.band(S, k) - Sig) for k in (2, 4, 6, 8, 12, 16)))
            acc["thresh"].append(min(HS.op_norm(HS.threshold(S, t) - Sig) for t in (0.05, 0.1, 0.15, 0.2, 0.3, 0.4)))
            acc["lw"].append(HS.op_norm(HS.ledoit_wolf(X)[0] - Sig))
        rows.append({"n": n, **{k: float(np.mean(v)) for k, v in acc.items()}})
    return {"p": p, "rho": rho, "rows": rows, "sig_norm": HS.op_norm(Sig), "tuning": "band and threshold levels minimize true operator error: oracle benchmark, unavailable on real data"}


def compute_dk():
    r = rng(5206)
    n, p = 500, 200
    rows = []
    for ell in (0.25, 0.5, 1.0, 2.0, 4.0, 8.0):
        ang, bnd = [], []
        for _ in range(10):
            X = HS.spiked_sample(n, p, ell, r)
            S = X.T @ X / n
            Sig = np.eye(p)
            Sig[0, 0] = 1 + ell
            _, v = HS.top_eig(X)
            ang.append(HS.sin_theta(v, np.eye(p)[0]))
            bnd.append(HS.davis_kahan(HS.op_norm(S - Sig), ell))
        rows.append({"ell": ell, "sin": float(np.mean(ang)), "bound": float(np.mean(bnd)),
                     "bbp": math.sqrt(max(0.0, 1 - float(HS.spike_overlap(ell, p / n))))})
    return {"n": n, "p": p, "rows": rows}


def compute_laws():
    g = 0.5
    a, b = HS.mp_edges(g)
    x = np.linspace(0.0, 3.4, 500)
    st = {str(eta): HS.density_from_stieltjes(x, g, eta) for eta in (0.2, 0.05, 1e-6)}
    r = rng(5207)
    ev = HS.wigner(1000, r)
    edges = np.linspace(-2.4, 2.4, 49)
    counts, _ = np.histogram(ev, bins=edges)
    h = counts/(len(ev)*np.diff(edges))
    xs = np.linspace(-2.4, 2.4, 400)
    return {"gamma": g, "edges_mp": [a, b], "x": x, "stieltjes": st, "mp": HS.mp_pdf(x, g), "w_edges": edges, "w_hist": h,
            "w_x": xs, "semi": HS.semicircle_pdf(xs), "w_max": float(ev.max()), "w_min": float(ev.min())}


def compute_bbp():
    r = rng(5208)
    n, p = 1000, 500
    g = p / n
    ells = [0.0, 0.25, 0.5, 0.6, 0.7, 0.8, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0]
    rows = []
    for ell in ells:
        tops, ovs = [], []
        for _ in range(12):
            X = HS.spiked_sample(n, p, ell, r)
            l, v = HS.top_eig(X)
            tops.append(l)
            ovs.append(v[0] ** 2)
        rows.append({"ell": ell, "top": float(np.mean(tops)), "overlap": float(np.mean(ovs)),
                     "top_theory": float(HS.spike_eigenvalue(ell, g)) if ell > 0 else (1 + math.sqrt(g)) ** 2,
                     "ov_theory": float(HS.spike_overlap(ell, g)) if ell > 0 else 0.0, "pop": 1 + ell})
    u = np.linspace(0.01, 3.0, 300)
    return {"n": n, "p": p, "gamma": g, "rows": rows, "u": u, "top_curve": HS.spike_eigenvalue(u, g), "ov_curve": HS.spike_overlap(u, g),
            "threshold": math.sqrt(g), "edge": (1 + math.sqrt(g)) ** 2}


def compute_tw():
    r = rng(5209)
    n, p = 400, 200
    mu, sig = HS.johnstone_center_scale(n, p)
    z = []
    for _ in range(1500):
        X = r.standard_normal((n, p))
        z.append((np.linalg.eigvalsh(X.T @ X)[-1] - mu) / sig)
    z = np.asarray(z)
    edges = np.linspace(-5, 4, 46)
    counts, _ = np.histogram(z, bins=edges)
    h = counts/(len(z)*np.diff(edges))
    s = np.linspace(-5, 4, 200)
    q95 = HS.tracy_widom_quantile(0.95, 1)
    m1 = HS.tracy_widom_moments(1)
    return {"n": n, "p": p, "mu": mu, "sigma": sig, "edges": edges, "hist": h, "s": s, "pdf1": HS.tracy_widom_pdf(s, 1),
            "pdf2": HS.tracy_widom_pdf(s, 2), "q95": q95, "size": float(np.mean(z > q95)), "outside_plot": int(np.sum((z<edges[0])|(z>edges[-1]))), "z_mean": float(z.mean()), "z_sd": float(z.std()),
            "tw_mean": m1["mean"], "tw_sd": m1["sd"]}


def compute_spca():
    r = rng(5210)
    p, k, ell = 1000, 10, 2.0
    rows = []
    for n in (50, 100, 200, 400, 800):
        pc, dt = [], []
        for _ in range(8):
            X, v = HS.sparse_spike_sample(n, p, k, ell, r)
            _, vp = HS.top_eig(X)
            vd = HS.diagonal_thresholding(X, k)
            pc.append((vp @ v) ** 2)
            dt.append((vd @ v) ** 2)
        rows.append({"n": n, "pca": float(np.mean(pc)), "dt": float(np.mean(dt)), "gamma": p / n,
                     "bbp": float(HS.spike_overlap(ell, p / n))})
    q = 30
    Q = HS.chain_precision(q, 0.4)
    C = np.linalg.cholesky(np.linalg.inv(Q))
    truth = np.abs(Q) > 0
    np.fill_diagonal(truth, False)
    off = ~truth & ~np.eye(q, dtype=bool)
    g_rows = []
    for n in (25, 50, 100, 200, 400):
        tp, fp = [], []
        for _ in range(6):
            Xg = r.standard_normal((n, q)) @ C.T
            E = HS.neighbourhood_selection(Xg, math.sqrt(2 * math.log(q) / n) * 0.6)
            tp.append(np.mean(E[truth]))
            fp.append(np.mean(E[off]))
        g_rows.append({"n": n, "tpr": float(np.mean(tp)), "fpr": float(np.mean(fp))})
    return {"p": p, "k": k, "ell": ell, "rows": rows, "graph_p": q, "graph": g_rows}


def compute_harman():
    names, R, n = museum.harman74()
    R = np.asarray(R, float)
    p = R.shape[0]
    ev = np.sort(np.linalg.eigvalsh(R))[::-1]
    g = p / (n-1)  # centered-Gaussian reference for a correlation matrix
    a, b = HS.mp_edges(g)
    above = int(np.sum(ev > b))
    spikes = [1 + HS.spike_invert(float(l), g) for l in ev[:above]]
    overlaps = [float(HS.spike_overlap(s - 1, g)) for s in spikes]
    w, V = np.linalg.eigh(R)
    v1 = V[:, -1] * np.sign(V[:, -1].sum())
    return {"names": names, "n": n, "p": p, "gamma": g, "ev": ev, "mp_lo": a, "mp_hi": b, "above": above, "spikes": spikes,
            "overlaps": overlaps, "v1": v1, "share_top": ev[0] / p}


def compute_diabetes():
    X0, y, names = museum.diabetes()
    X0 = np.asarray(X0, float)
    Z = (X0 - X0.mean(0)) / X0.std(0)
    cols, labels = [Z[:, j] for j in range(10)], list(names)
    for i in range(10):
        for j in range(i, 10):
            if i == 1 and j == 1:
                continue  # sex squared is sex
            cols.append(Z[:, i] * Z[:, j])
            labels.append(f"{names[i]}*{names[j]}" if i != j else f"{names[i]}^2")
    X = np.column_stack(cols)
    X = (X - X.mean(0)) / X.std(0)
    yc = np.asarray(y, float) - np.mean(y)
    n, p = X.shape
    lams = np.geomspace(SPK.lam_max(X, yc), SPK.lam_max(X, yc) * 1e-3, 60)
    cv = SPK.cv_lasso(X, yc, lams, K=10, rng=rng(5211))
    lam = float(cv["lam_1se"]) if "lam_1se" in cv else float(cv["lam_min"])
    b = SPK.lasso_cd(X, yc, lam)
    deb, ols = [], []
    beta_ols, cov_ols, condition = full_model_ols(X,yc)
    lam_node = math.sqrt(2 * math.log(p) / n)  # the nodewise regressions are on standardized columns
    for j in range(10):
        d = SPK.debiased_lasso(X, yc, j, lam, lam_node=lam_node)
        deb.append({"name": labels[j], "b": d["b"], "lo": d["lo"], "hi": d["hi"], "lasso": float(b[j]), **nodewise_diagnostics(X,j,lam_node)})
        se = math.sqrt(cov_ols[j, j])
        ols.append({"name": labels[j], "b": float(beta_ols[j]), "lo": float(beta_ols[j] - 1.96 * se), "hi": float(beta_ols[j] + 1.96 * se)})
    return {"n": n, "p": p, "lam": lam, "lam_node": lam_node, "selected": int(np.sum(b != 0)), "selected_names": [labels[j] for j in np.flatnonzero(b)],
            "deb": deb, "ols": ols, "cv_keys": sorted(cv.keys()), "design_condition": condition, "sparsity_scale": math.sqrt(n)/math.log(p), "target": "original full linear-interaction-model coefficient; no finite-sample coverage guarantee is established"}


def compute_board():
    """Inference for the top eigenvalue in a spiked model with p/n = 1/2: Anderson's classical interval (built for fixed p)
    against the BBP-corrected interval; and a test for any spike at all: a normal approximation for the top eigenvalue
    against Roy's largest-root test with Johnstone's Tracy-Widom calibration."""
    r = rng(5212)
    n, p = 200, 100
    g = p / n
    ell = 3.0
    reps = 2000
    a_cov, s_cov = 0, 0
    for _ in range(reps):
        X = HS.spiked_sample(n, p, ell, r)
        lhat, _ = HS.top_eig(X)
        lo, hi = HS.anderson_ci(lhat, n)
        a_cov += lo <= 1 + ell <= hi
        lo, hi = HS.spike_ci(lhat, n, g)
        s_cov += lo <= 1 + ell <= hi
    mu, sig = HS.johnstone_center_scale(n, p)
    q95 = HS.tracy_widom_quantile(0.95, 1)
    naive, roy = 0, 0
    for _ in range(reps):
        X = r.standard_normal((n, p))
        top = np.linalg.eigvalsh(X.T @ X)[-1]
        naive += top / n > 1 + 1.645 * math.sqrt(2 / n)
        roy += (top - mu) / sig > q95
    rows = [
        Row(52, r"Anderson's interval for the top eigenvalue", r"spike $1 + \ell = 4$, \ $n = 200$, \ $p = 100$", "coverage", 0.95, a_cov / reps, reps, mc_se=math.sqrt((a_cov/reps)*(1-a_cov/reps)/(reps-1))),
        Row(52, r"BBP-corrected interval for the spike", r"spike $1 + \ell = 4$, \ $n = 200$, \ $p = 100$", "coverage", 0.95, s_cov / reps, reps, mc_se=math.sqrt((s_cov/reps)*(1-s_cov/reps)/(reps-1))),
        Row(52, r"normal test for a spike (size)", r"null $\Sigma = I$, \ $n = 200$, \ $p = 100$", "size", 0.05, naive / reps, reps, mc_se=math.sqrt((naive/reps)*(1-naive/reps)/(reps-1))),
        Row(52, r"Roy's test, Tracy--Widom calibration (size)", r"null $\Sigma = I$, \ $n = 200$, \ $p = 100$", "size", 0.05, roy / reps, reps, mc_se=math.sqrt((roy/reps)*(1-roy/reps)/(reps-1))),
    ]
    save_rows(52, rows)
    return {"rows": [asdict(q) | {"verdict": q.verdict, "se": q.se} for q in rows], "q95": q95, "psi": float(HS.spike_eigenvalue(ell, g))}


ITEMS = {
    "hook": compute_hook, "oracle": compute_oracle, "support": compute_support, "complete": compute_complete, "cov": compute_cov,
    "dk": compute_dk, "laws": compute_laws, "bbp": compute_bbp, "tw": compute_tw, "spca": compute_spca, "harman": compute_harman,
    "diabetes": compute_diabetes, "board": compute_board,
}


if __name__ == "__main__":
    CACHE.main({k: (lambda f=f: nest(f())) for k, f in ITEMS.items()}, __doc__)
