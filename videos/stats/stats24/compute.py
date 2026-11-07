"""Precompute every number in Part 24 of *Statistics, Built* ("Generalized Linear Models").

    python -m videos.stats.stats24.compute            # everything missing (a few minutes)
    python -m videos.stats.stats24.compute --force board

Results are cached in ``.cache/stats24/<name>.json``.  Bliss's beetles are the Museum's; doctor visits, health and
schools are the World's; the rest are seeded simulations.

Items:
    bliss       logit, probit and cloglog fits to the beetles; deviances; LD50 with delta and Fieller intervals
    irls        the IRLS path for the beetles from a cold start: coefficients and deviance per step
    binary_dev  the deviance's chi-squared approximation: grouped (good) vs binary (useless)
    visits      a sample of the World's doctor visits: Poisson, NB, ZIP and hurdle; zeros; quantile residuals
    devtable    analysis of deviance for the visits, Poisson and NB
    separation  a separated toy: IRLS slopes running away, Firth's finite answer
    loglinear   sex x age group x told-high in the World: log-linear models as Poisson GLMs
    ordinal     BMI category on age and sex: proportional odds, against separate cut-point logits
    gee         one sample of 40 schools: naive logistic, GEE independence and exchangeable
    scoring     expected scores against the reported probability: log, Brier, absolute
    board       Coverage Board rows
"""

from __future__ import annotations

from dataclasses import asdict

import numpy as np
from scipy import special, stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import glm as G
from explainer.stats.world import World

CACHE = Cache("stats24")
load = CACHE.load
W = World()


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



def glm_fit(X, y, fam, n=None, offset=None, tol=1e-12, max_iter=150, start=None):
    """IRLS with a checked, recomputed line search and explicit convergence.

    Working least squares uses QR. A failed line search or iteration budget
    raises rather than returning an unverified coefficient path.
    """
    X, y = np.asarray(X, float), np.asarray(y, float)
    if X.ndim != 2 or y.shape != (len(X),) or not np.isfinite(X).all() or not np.isfinite(y).all():
        raise ValueError("finite compatible design and response required")
    if np.linalg.matrix_rank(X) != X.shape[1]:
        raise ValueError("full-rank design required")
    n = np.ones_like(y) if n is None else np.broadcast_to(np.asarray(n, float), y.shape).copy()
    off = np.zeros_like(y) if offset is None else np.broadcast_to(np.asarray(offset, float), y.shape).copy()
    if np.any(n <= 0) or not np.isfinite(n).all() or not np.isfinite(off).all():
        raise ValueError("positive finite prior weights and finite offsets required")
    if fam.name == "binomial" and np.any((y < 0) | (y > 1)):
        raise ValueError("binomial responses must be proportions")
    initial = G.glm_fit(X, y, fam, n=n, offset=off, max_iter=0, start=start)
    beta = initial.coef.copy()
    path, devs, halvings = [beta.copy()], [initial.deviance], []
    if not np.isfinite(devs[0]):
        raise ValueError("initial predictor is outside the family domain")
    for _ in range(max_iter):
        eta = X @ beta + off
        mu, deriv = fam.ginv(eta), fam.dmu(eta)
        w = n * deriv ** 2 / fam.V(mu)
        if np.any(w <= 0) or not np.isfinite(w).all() or np.any(deriv == 0):
            raise RuntimeError("degenerate IRLS information; check separation or mean domain")
        z = eta - off + (y - mu) / deriv
        Q, R = np.linalg.qr(np.sqrt(w)[:, None] * X, mode="reduced")
        proposal = np.linalg.solve(R, Q.T @ (np.sqrt(w) * z))
        accepted = False
        for h in range(61):
            new = beta + (proposal - beta) * 2. ** -h
            candidate = G.GlmFit(fam, new, X, y, n, off)
            with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
                dv = candidate.deviance
            if np.isfinite(dv) and dv <= devs[-1] + 1e-12 * (1 + abs(devs[-1])):
                accepted = True
                break
        if not accepted:
            raise RuntimeError("IRLS line search failed to find a non-increasing deviance")
        path.append(new.copy()); devs.append(dv); halvings.append(h)
        done = np.max(np.abs(new - beta)) <= tol * (1 + np.max(np.abs(beta)))
        beta = new
        if done:
            result = G.GlmFit(fam, beta, X, y, n, off, path, devs)
            result.halvings = halvings
            return result
    raise RuntimeError("IRLS did not converge within its iteration budget")


def gee_logistic(X, y, groups, corstr="exchangeable", iters=100, tol=1e-10):
    """Binary GEE using the analytic inverse of an exchangeable correlation.

    Explicitly constrain the moment correlation to a positive-definite working
    matrix. This numerical safeguard is recorded, not hidden in the estimate.
    Covariances below use the usual model derivative bread.
    """
    X, y, groups = np.asarray(X, float), np.asarray(y, float), np.asarray(groups)
    if corstr not in ("independence", "exchangeable"):
        raise ValueError("unsupported working correlation")
    if X.ndim != 2 or y.shape != (len(X),) or groups.shape != y.shape:
        raise ValueError("incompatible shapes")
    if not np.isfinite(X).all() or not np.isfinite(y).all() or np.any((y < 0) | (y > 1)):
        raise ValueError("finite binary responses and design required")
    labels, idx = np.unique(groups, return_inverse=True)
    if len(labels) < 2:
        raise ValueError("at least two independent clusters required")
    members = [np.flatnonzero(idx == j) for j in range(len(labels))]
    size = np.array([len(m) for m in members])
    b = glm_fit(X,y,G.family("binomial")).coef
    constrained = 0
    def pieces(beta, alpha):
        mu = special.expit(X @ beta)
        v = mu * (1-mu)
        if np.any(v <= 0):
            raise RuntimeError("degenerate binary GEE variance")
        sv = np.sqrt(v)
        D = X * sv[:,None]
        r = (y-mu)/sv
        A, M, U = np.zeros((X.shape[1],X.shape[1])), np.zeros((X.shape[1],X.shape[1])), np.zeros(X.shape[1])
        for m in members:
            # R^-1 = (I - alpha/(1-alpha+k*alpha) 11')/(1-alpha).
            a = alpha/(1-alpha+len(m)*alpha)
            d, e = D[m], r[m]
            vd = (d-a*d.sum(0))/(1-alpha)
            score = d.T @ ((e-a*e.sum())/(1-alpha))
            A += d.T @ vd
            U += score
            M += np.outer(score,score)
        return A,M,U,r
    alpha=0.
    for _ in range(iters):
        _,_,_,r = pieces(b,alpha)
        if corstr == "exchangeable":
            num=sum(r[m].sum()**2 - r[m]@r[m] for m in members)
            den=np.sum(size*(size-1))
            if den == 0:
                raise ValueError("exchangeable correlation needs at least one non-singleton cluster")
            phi=r@r/(len(y)-X.shape[1])
            raw=float(num/den/phi)
            lower=-1/(size.max()-1)+1e-8
            alpha=float(np.clip(raw,lower,1-1e-8))
            constrained += int(raw != alpha)
        A,_,U,_=pieces(b,alpha)
        step=np.linalg.solve(A,U)
        b=b+step
        if not np.isfinite(b).all():
            raise RuntimeError("non-finite GEE iteration")
        if np.max(np.abs(step)) < tol:
            break
    else:
        raise RuntimeError("GEE did not converge")
    A,M,U,_=pieces(b,alpha);Ai=np.linalg.inv(A)
    return {"coef":b,"alpha":alpha,"se_model":np.sqrt(np.diag(Ai)),
            "se_robust":np.sqrt(np.diag(Ai@M@Ai)),
            "constrained_updates":constrained,"score_norm":float(np.max(abs(U)))}


def calibration_bins(p,y,bins=10):
    """Quantile-bin means, counts and Wilson intervals; omit empty tied bins."""
    p,y=np.asarray(p,float),np.asarray(y,float)
    edges=np.quantile(p,np.linspace(0,1,bins+1))
    idx=np.clip(np.searchsorted(edges,p,side="right")-1,0,bins-1)
    pred,obs,count,lo,hi=[],[],[],[],[]
    for k in range(bins):
        m=idx==k
        if not np.any(m):
            continue
        n=int(m.sum()); hits=int(y[m].sum()); z=stats.norm.ppf(.975)
        ph=hits/n;den=1+z*z/n;center=(ph+z*z/(2*n))/den
        half=z*np.sqrt(ph*(1-ph)/n+z*z/(4*n*n))/den
        pred.append(float(p[m].mean()));obs.append(ph);count.append(n)
        lo.append(center-half);hi.append(center+half)
    return {"pred":pred,"obs":obs,"count":count,"lo":lo,"hi":hi}


def bliss_X():
    x, n, k = museum.bliss()
    return np.column_stack([np.ones(8), x]), x, n, k


def compute_bliss():
    X, x, n, k = bliss_X()
    grid = np.linspace(1.65, 1.92, 200)
    Xg = np.column_stack([np.ones(200), grid])
    out = {"x": x, "n": n, "k": k, "grid": grid, "fits": {}}
    for link in ("logit", "probit", "cloglog"):
        f = glm_fit(X, k / n, G.family("binomial", link), n=n)
        out["fits"][link] = {"coef": f.coef, "se": f.se(), "deviance": f.deviance, "df": f.df_resid,
                             "p": float(stats.chi2.sf(f.deviance, f.df_resid)), "curve": G.family("binomial", link).ginv(Xg @ f.coef),
                             "fitted": f.mu * n, "pearson": f.pearson, "devres": f.deviance_resid, "ld50": G.ld50(f),
                             "aic": float(-2 * f.loglik_binomial + 4)}
    out["probits"] = stats.norm.ppf(np.clip(k / n, 0.005, 0.995)) + 5  # Bliss's probits: the normal deviate plus 5
    return nest(out)


def compute_irls():
    X, x, n, k = bliss_X()
    f = glm_fit(X, k / n, G.family("binomial"), n=n, start=np.zeros(2))
    P = np.asarray(f.path)
    # working response and weights at the start (beta = 0): what the first weighted regression sees
    mu0 = np.full(8, 0.5)
    w0 = n * mu0 * (1 - mu0)
    z0 = (k / n - mu0) / (mu0 * (1 - mu0))
    return nest({"path": P, "deviance": f.deviance_path, "z0": z0, "w0": w0, "iters": len(P) - 1, "final": f.coef, "halvings": f.halvings})


def compute_binary_dev():
    g = rng(2401)
    R = 2000
    # grouped: Bliss-like doses and trials, true logit model; deviance vs chi2_6
    X, x, n, k = bliss_X()
    p_true = special.expit(X @ np.array([-60.7, 34.27]))
    grouped = []
    for _ in range(R):
        kk = g.binomial(n.astype(int), p_true)
        grouped.append(glm_fit(X, kk / n, G.family("binomial"), n=n).deviance)
    # binary: 200 individuals, a true logistic model; the deviance's spread is tiny and its centre depends on beta
    nb = 200
    binary = []
    for _ in range(R):
        xb = g.normal(size=nb)
        Xb = np.column_stack([np.ones(nb), xb])
        yb = (g.random(nb) < special.expit(0.3 + 1.0 * xb)).astype(float)
        binary.append(glm_fit(Xb, yb, G.family("binomial")).deviance)
    return nest({"grouped": grouped, "binary": binary, "df_grouped": 6, "df_binary": nb - 2,
                 "grouped_reject": float(np.mean(np.asarray(grouped) > stats.chi2.ppf(0.95, 6))),
                 "binary_reject": float(np.mean(np.asarray(binary) > stats.chi2.ppf(0.95, nb - 2))),
                 "binary_mean": float(np.mean(binary)), "binary_sd": float(np.std(binary))})


def visits_design(idx):
    h = W.health
    a = W.age[idx].astype(float)
    X = np.column_stack([np.ones(len(idx)), (a - 50) / 10, (h["bmi"][idx] - 27) / 5, h["told_high"][idx].astype(float),
                         (~W.male[idx]).astype(float)])
    return X, W.visits["visits"][idx].astype(float)


VNAMES = ["intercept", "age (per 10 y)", "BMI (per 5)", "told high BP", "female"]


def compute_visits():
    idx = W.sample(2000, among=W.adult & (W.age <= 85), seed=2402)
    X, y = visits_design(idx)
    po = glm_fit(X, y, G.family("poisson"))
    nb = G.negbin_fit(X, y)
    zp = G.zip_em(X, y)
    hu = G.hurdle(X, y)
    ks = np.arange(0, 16)
    obs = np.array([np.mean(y == k) for k in ks])
    mu_p = po.mu
    exp_p = np.array([np.mean(stats.poisson.pmf(k, mu_p)) for k in ks])
    kk = nb["k"]
    exp_nb = np.array([np.mean(stats.nbinom.pmf(k, kk, kk / (kk + nb["mu"]))) for k in ks])
    lam = np.exp(X @ zp["beta"])
    exp_zip = np.array([np.mean(np.where(k == 0, zp["pi"] + (1 - zp["pi"]) * np.exp(-lam), (1 - zp["pi"]) * stats.poisson.pmf(k, lam)))
                        for k in ks])
    gq = rng(1996)
    qp = po.quantile_resid(gq)
    # NB quantile residuals
    a = stats.nbinom.cdf(y - 1, kk, kk / (kk + nb["mu"]))
    b = stats.nbinom.cdf(y, kk, kk / (kk + nb["mu"]))
    qnb = stats.norm.ppf(np.clip(a + gq.random(len(y)) * (b - a), 1e-12, 1 - 1e-12))
    ll_p = float(np.sum(stats.poisson.logpmf(y, mu_p)))
    return nest({"n": len(y), "mean": float(y.mean()), "var": float(y.var()), "zeros": float(np.mean(y == 0)),
                 "ks": ks, "obs": obs, "exp_p": exp_p, "exp_nb": exp_nb, "exp_zip": exp_zip,
                 "poisson": {"coef": po.coef, "se": po.se(), "se_sand": po.se("sandwich"), "phi": po.pearson_phi, "ll": ll_p,
                             "deviance": po.deviance, "df": po.df_resid},
                 "nb": {"coef": nb["coef"], "se": nb["se"], "k": kk, "ll": nb["loglik"]},
                 "zip": {"beta": zp["beta"], "pi": float(zp["pi"][0]), "ll": zp["loglik"]},
                 "hurdle": {"ll": hu["loglik"]}, "q_pois": np.sort(qp), "q_nb": np.sort(qnb),
                 "true_never": W.VISITS_NEVER, "true_k": W.VISITS_K, "names": VNAMES})


def compute_devtable():
    idx = W.sample(2000, among=W.adult & (W.age <= 85), seed=2402)
    X, y = visits_design(idx)
    rows = []
    for j in range(1, X.shape[1] + 1):
        Xj = X[:, :j]
        po = glm_fit(Xj, y, G.family("poisson"))
        rows.append({"terms": VNAMES[j - 1], "dev": po.deviance, "df": po.df_resid, "phi": po.pearson_phi})
    for i in range(1, len(rows)):
        rows[i]["drop"] = rows[i - 1]["dev"] - rows[i]["dev"]
        rows[i]["F"] = rows[i]["drop"] / rows[-1]["phi"]
    return nest({"rows": rows})


def compute_separation():
    x = np.array([-2.1, -1.6, -1.2, -0.9, -0.4, -0.1, 0.3, 0.6, 1.0, 1.3, 1.8, 2.2])
    y = (x > 0).astype(float)
    X = np.column_stack([np.ones(len(x)), x])
    run = G.logistic_path_separated(X, y, 25)
    fr = G.firth_logistic(X, y)
    y2 = y.copy()
    y2[5], y2[6] = 1.0, 0.0  # two overlapping points: the MLE exists
    ok = glm_fit(X, y2, G.family("binomial"))
    return nest({"x": x, "y": y, "slopes": run["slope"], "loglik": run["loglik"], "firth": fr["coef"], "firth_se": fr["se"],
                 "y2": y2, "overlap": ok.coef, "overlap_se": ok.se()})


def compute_loglinear():
    idx = W.sample(5000, among=W.adult & (W.age <= 89), seed=2403)
    sex = (~W.male[idx]).astype(int)  # 0 men, 1 women
    ag = np.digitize(W.age[idx], [40, 60])  # 18-39, 40-59, 60+
    t = W.health["told_high"][idx].astype(int)
    cells = [(s, a, tt) for s in (0, 1) for a in (0, 1, 2) for tt in (0, 1)]
    count = np.array([np.sum((sex == s) & (ag == a) & (t == tt)) for s, a, tt in cells], float)
    S = np.array([c[0] for c in cells], float)
    A1 = np.array([c[1] == 1 for c in cells], float)
    A2 = np.array([c[1] == 2 for c in cells], float)
    T = np.array([c[2] for c in cells], float)
    one = np.ones(12)
    base = [one, S, A1, A2, T, S * A1, S * A2]
    models = {
        "[SA][T]": base,
        "[SA][AT]": base + [A1 * T, A2 * T],
        "[SA][AT][ST]": base + [A1 * T, A2 * T, S * T],
        "saturated": base + [A1 * T, A2 * T, S * T, S * A1 * T, S * A2 * T],
    }
    out = {"count": count, "cells": cells, "models": {}}
    for name, cols in models.items():
        f = glm_fit(np.column_stack(cols), count, G.family("poisson"))
        out["models"][name] = {"deviance": max(f.deviance, 0.0), "df": f.df_resid,
                               "p": float(stats.chi2.sf(f.deviance, f.df_resid)) if f.df_resid > 0 else 1.0,
                               "fitted": f.mu}
    f3 = glm_fit(np.column_stack(models["[SA][AT][ST]"]), count, G.family("poisson"))
    out["st_or"] = float(np.exp(f3.coef[-1]))
    out["st_ci"] = np.exp(f3.coef[-1] + np.array([-1.96, 1.96]) * f3.se()[-1])
    return nest(out)


def compute_ordinal():
    idx = W.sample(3000, among=W.adult & (W.age <= 85), seed=2404)
    bmi = W.health["bmi"][idx]
    cat = np.digitize(bmi, [18.5, 25, 30])  # under, normal, over, obese
    age = (W.age[idx].astype(float) - 50) / 10
    fem = (~W.male[idx]).astype(float)
    Xo = np.column_stack([age, fem])
    po = G.proportional_odds(Xo, cat, 4)
    sep = []
    for j in range(3):  # separate logits for P(cat > j): the proportional-odds check
        f = glm_fit(np.column_stack([np.ones(len(cat)), Xo]), (cat > j).astype(float), G.family("binomial"))
        sep.append({"coef": f.coef, "se": f.se()})
    counts = np.bincount(cat, minlength=4)
    ages = np.arange(18, 86)
    a_s = (ages - 50) / 10
    probs = {}
    for f_ in (0.0, 1.0):
        eta = po["beta"][0] * a_s + po["beta"][1] * f_
        cdf = special.expit(po["theta"][None, :] - eta[:, None])
        P = np.diff(np.column_stack([np.zeros(len(ages)), cdf, np.ones(len(ages))]), axis=1)
        probs[str(int(f_))] = P
    return nest({"theta": po["theta"], "beta": po["beta"], "se_beta": po["se_beta"], "separate": sep, "counts": counts,
                 "ages": ages, "probs": probs, "n": len(cat)})


def school_sample(G_, g):
    s = W.schools
    pick = np.sort(g.choice(W.N_SCHOOLS, G_, replace=False))
    m = np.isin(s["school"], pick)
    sch = s["school"][m]
    X = np.column_stack([np.ones(m.sum()), s["programme"][sch].astype(float), s["ses"][m]])
    y = (s["score"][m] > 550).astype(float)
    return X, y, sch


def school_truth():
    s = W.schools
    X = np.column_stack([np.ones(len(s["school"])), s["programme"][s["school"]].astype(float), s["ses"]])
    y = (s["score"] > 550).astype(float)
    return float(glm_fit(X, y, G.family("binomial")).coef[1])


def compute_gee():
    g = rng(2405)
    X, y, sch = school_sample(40, g)
    f = glm_fit(X, y, G.family("binomial"))
    ind = gee_logistic(X, y, sch, "independence")
    ex = gee_logistic(X, y, sch, "exchangeable")
    truth = school_truth()
    census = W.schools
    Xc = np.column_stack([np.ones(len(census["school"])), census["programme"][census["school"]].astype(float), census["ses"]])
    yc = (census["score"] > 550).astype(float)
    truth_ex = float(gee_logistic(Xc, yc, census["school"], "exchangeable")["coef"][1])
    # the conditional (random-intercept) effect is larger than the marginal: logistic attenuation
    s = W.schools
    u_sd = W.SCHOOL_SD / W.PUPIL_SD
    return nest({"n": len(y), "G": 40, "naive": {"coef": f.coef, "se": f.se()}, "ind": ind, "ex": ex, "truth": truth, "truth_exchangeable": truth_ex,
                 "mean_y": float(y.mean()), "u_sd": u_sd,
                 "attenuation": float(1 / np.sqrt(1 + (np.pi ** 2 / 3) ** -1 * 0 + 0.346 * (1.7 * u_sd) ** 2))})


def compute_scoring():
    p = 0.3
    q = np.linspace(0.01, 0.99, 197)
    log_ = -(p * np.log(q) + (1 - p) * np.log(1 - q))
    brier = p * (1 - q) ** 2 + (1 - p) * q ** 2
    absl = p * (1 - q) + (1 - p) * q
    # two forecasters of told-high on a holdout: a calibrated logistic and an overconfident version of it
    idx = W.sample(4000, among=W.adult & (W.age <= 85), seed=2406)
    h = W.health
    a = (W.age[idx].astype(float) - 50) / 10
    X = np.column_stack([np.ones(len(idx)), a, (h["bmi"][idx] - 27) / 5, (~W.male[idx]).astype(float)])
    y = h["told_high"][idx].astype(float)
    tr, te = np.arange(2000), np.arange(2000, 4000)
    f = glm_fit(X[tr], y[tr], G.family("binomial"))
    p_cal = special.expit(X[te] @ f.coef)
    p_over = special.expit(2.0 * (X[te] @ f.coef - np.log(y[tr].mean() / (1 - y[tr].mean()))) + np.log(y[tr].mean() / (1 - y[tr].mean())))
    p_base = np.full(len(te), y[tr].mean())
    sc = {}
    for name, pp in (("calibrated", p_cal), ("overconfident", p_over), ("base rate", p_base)):
        sc[name] = {"log": G.log_score(pp, y[te]), "brier": G.brier(pp, y[te]),
                    "auc": float(stats.rankdata(pp)[y[te] > 0].sum() - np.sum(y[te] > 0)*(np.sum(y[te] > 0)+1)/2) / (np.sum(y[te] > 0)*np.sum(y[te] == 0)),
                    "acc": float(np.mean((pp > 0.5) == (y[te] > 0.5)))}
    crps = {"right": float(np.mean(G.crps_normal(0, 1, rng(7).normal(size=20000)))),
            "too_narrow": float(np.mean(G.crps_normal(0, 0.5, rng(7).normal(size=20000)))),
            "too_wide": float(np.mean(G.crps_normal(0, 2.0, rng(7).normal(size=20000))))}
    return nest({"p": p, "q": q, "log": log_, "brier": brier, "abs": absl, "scores": sc, "crps": crps,
                 "prevalence": float(y[te].mean())})


def compute_extras():
    """Gamma regression of incomes on age; Bliss's Pearson dispersion; a calibration plot for the scoring chapter."""
    idx = W.sample(1500, among=W.adult & (W.age >= 25) & (W.age <= 64), seed=2407)
    inc = W.income[idx] / 1000
    a = (W.age[idx].astype(float) - 45) / 10
    X = np.column_stack([np.ones(len(idx)), a])
    gm = glm_fit(X, inc, G.family("gamma", "log"))
    gauss = glm_fit(X, np.log(inc), G.family("gaussian"))
    X0, x, n, k = bliss_X()
    cl = glm_fit(X0, k / n, G.family("binomial", "cloglog"), n=n)
    lg = glm_fit(X0, k / n, G.family("binomial"), n=n)
    # calibration of the two told-high forecasters
    sc_idx = W.sample(4000, among=W.adult & (W.age <= 85), seed=2406)
    h = W.health
    aa = (W.age[sc_idx].astype(float) - 50) / 10
    Xs = np.column_stack([np.ones(len(sc_idx)), aa, (h["bmi"][sc_idx] - 27) / 5, (~W.male[sc_idx]).astype(float)])
    y = h["told_high"][sc_idx].astype(float)
    tr, te = np.arange(2000), np.arange(2000, 4000)
    f = glm_fit(Xs[tr], y[tr], G.family("binomial"))
    base = np.log(y[tr].mean() / (1 - y[tr].mean()))
    p_cal = special.expit(Xs[te] @ f.coef)
    p_over = special.expit(2.0 * (Xs[te] @ f.coef - base) + base)
    cal = calibration_bins(p_cal, y[te], 10)
    over = calibration_bins(p_over, y[te], 10)
    return nest({"gamma": {"coef": gm.coef, "se": gm.se(), "phi": gm.phi, "cv": float(np.sqrt(gm.phi))},
                 "lognormal": {"coef": gauss.coef, "se": gauss.se()}, "n_inc": len(idx),
                 "bliss_phi": {"cloglog": cl.pearson_phi, "logit": lg.pearson_phi},
                 "cal": cal, "over": over})


def compute_board():
    g = rng(2424)
    # (1-3) Poisson regression of visits, n = 500: the target is the World's own Poisson fit (a projection)
    ad = np.flatnonzero(W.adult & (W.age <= 85))
    Xa, ya = visits_design(ad)
    target = float(glm_fit(Xa, ya, G.family("poisson")).coef[3])
    R = 1000
    hit = {"model": 0, "quasi": 0, "sandwich": 0}
    for r in range(R):
        i = np.sort(g.choice(ad, 500, replace=False))
        X, y = visits_design(i)
        f = glm_fit(X, y, G.family("poisson"))
        for k in hit:
            hit[k] += abs(f.coef[3] - target) <= 1.96 * f.se(k)[3]
    # (4-6) GEE on 40 schools: binary score > 550
    truth = school_truth()
    census = W.schools
    Xc = np.column_stack([np.ones(len(census["school"])), census["programme"][census["school"]].astype(float), census["ses"]])
    yc = (census["score"] > 550).astype(float)
    truth_ex = float(gee_logistic(Xc, yc, census["school"], "exchangeable")["coef"][1])
    R2 = 500
    gh = {"naive": 0, "ind": 0, "ex": 0}
    for r in range(R2):
        X, y, sch = school_sample(40, g)
        f = glm_fit(X, y, G.family("binomial"))
        gh["naive"] += abs(f.coef[1] - truth) <= 1.96 * f.se()[1]
        a = gee_logistic(X, y, sch, "independence")
        gh["ind"] += abs(a["coef"][1] - truth) <= stats.t.ppf(0.975, 39) * a["se_robust"][1]
        b = gee_logistic(X, y, sch, "exchangeable")
        gh["ex"] += abs(b["coef"][1] - truth_ex) <= stats.t.ppf(0.975, 39) * b["se_robust"][1]
    rows = [
        Row(24, r"Poisson model SE", r"doctor visits, \ $n = 500$", "coverage", 0.95, hit["model"] / R, R),
        Row(24, r"quasi-Poisson SE", r"doctor visits, \ $n = 500$", "coverage", 0.95, hit["quasi"] / R, R),
        Row(24, r"sandwich SE", r"doctor visits, \ $n = 500$", "coverage", 0.95, hit["sandwich"] / R, R),
        Row(24, r"logistic, \ iid SE", r"40 schools, \ pupils clustered", "coverage", 0.95, gh["naive"] / R2, R2),
        Row(24, r"GEE, \ independence", r"40 schools, \ robust SE", "coverage", 0.95, gh["ind"] / R2, R2),
        Row(24, r"GEE, \ exchangeable", r"40 schools, \ robust SE", "coverage", 0.95, gh["ex"] / R2, R2),
    ]
    save_rows(24, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows], "target": target, "truth_gee": truth, "truth_gee_exchangeable": truth_ex}


ITEMS = {
    "bliss": compute_bliss, "irls": compute_irls, "binary_dev": compute_binary_dev, "visits": compute_visits,
    "devtable": compute_devtable, "separation": compute_separation, "loglinear": compute_loglinear,
    "ordinal": compute_ordinal, "gee": compute_gee, "extras": compute_extras, "scoring": compute_scoring, "board": compute_board,
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
