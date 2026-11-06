"""Precompute every number in Part 28 of *Statistics, Built* ("Which Model?").

    python -m videos.stats.stats28.compute            # everything missing (several minutes)
    python -m videos.stats.stats28.compute --force board

Results are cached in ``.cache/stats28/<name>.json``.  Stamey's prostate data and the eight schools are the Museum's;
the doctor visits are the World's; the rest are seeded simulations.

Items:
    freedman    Freedman's paradox: one run, and 1,000 runs of pure noise screened at p < 0.25
    optimism    training vs test error by polynomial degree; the optimism 2 sigma^2 df / n
    lassodf     degrees of freedom of the lasso by Monte Carlo covariance against the count of nonzeros
    tic         Takeuchi's penalty for a Poisson regression of the World's overdispersed doctor visits
    consistency AIC vs BIC: P(choose the true degree) as n grows, and prediction risk when the truth is not a polynomial
    prostate    best subset on Stamey's prostate data: AIC, BIC, CV; test errors of OLS, best subset, ridge, lasso
    cv          PRESS, GCV and 10-fold CV; what CV estimates (Bates, Hastie & Tibshirani 2024)
    loo         PSIS-LOO and WAIC for the eight schools' three models, with exact leave-one-school-out
    rlct        a singular mixture: the free energy grows like (1/2) log n, not (d/2) log n
    mdl         Shtarkov's NML regret for a coin; two-part code lengths for polynomial degree
    averaging   BMA vs stacking when the truth is a mixture of two candidate models
    subsets     best subset, forward stepwise and the lasso across signal-to-noise ratios (Hastie, Tibshirani & Tibshirani 2020)
    pit         calibrated, overconfident and biased forecasters: PIT histograms, log scores, CRPS
    stability   bootstrap the prostate selection: inclusion frequencies and how often the chosen model recurs
    prostate_pit leave-one-out PIT and log predictive density for three prostate models
    board       Coverage Board rows: confidence intervals after AIC selection, after splitting, and without selection
"""

from __future__ import annotations

from dataclasses import asdict

import numpy as np
from scipy import integrate, optimize, special, stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import bayes as B
from explainer.stats.kit import learn as Le
from explainer.stats.kit import select as Se
from explainer.stats.world import World

CACHE = Cache("stats28")
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


def ols(X, y):
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    r = y - X @ b
    return b, float(r @ r)


def compute_freedman():
    one = Se.freedman(100, 50, rng(1983))
    g = rng(1984)
    pF, nsig, kept = [], [], []
    for _ in range(1000):
        o = Se.freedman(100, 50, g)
        pF.append(o["second"]["pF"])
        nsig.append(o["second"]["n_sig05"])
        kept.append(len(o["second"]["cols"]))
    pF = np.array(pF)
    return nest({"one": {s: {k: v for k, v in one[s].items() if k != "p"} | {"p": one[s]["p"]} for s in one},
                 "share_sig": float(np.mean(pF < 0.05)), "median_kept": float(np.median(kept)),
                 "mean_sig": float(np.mean(nsig)), "pF_hist": np.histogram(pF, np.linspace(0, 1, 21))[0]})


def f_true(x):
    return np.sin(2.5 * x) + 0.5 * x


def compute_optimism():
    g = rng(1973)
    n, sigma, R = 30, 0.5, 600
    x = np.linspace(-1.5, 1.5, n)
    degs = np.arange(0, 13)
    tr, te = np.zeros(len(degs)), np.zeros(len(degs))
    for _ in range(R):
        y = f_true(x) + sigma * g.standard_normal(n)
        y2 = f_true(x) + sigma * g.standard_normal(n)  # new responses at the same x: in-sample prediction error
        for k, d in enumerate(degs):
            X = np.vander(x, d + 1, increasing=True)
            b, rss = ols(X, y)
            tr[k] += rss / n
            te[k] += np.mean((y2 - X @ b) ** 2)
    tr, te = tr / R, te / R
    theory = 2 * sigma ** 2 * (degs + 1) / n
    # one data set, for the picture
    y = f_true(x) + sigma * rng(1974).standard_normal(n)
    xx = np.linspace(-1.5, 1.5, 200)
    fits = {}
    for d in (1, 3, 10):
        b, _ = ols(np.vander(x, d + 1, increasing=True), y)
        fits[str(d)] = np.vander(xx, d + 1, increasing=True) @ b
    return nest({"degs": degs, "train": tr, "test": te, "gap": te - tr, "theory": theory, "sigma": sigma, "n": n, "x": x,
                 "y": y, "xx": xx, "truth": f_true(xx), "fits": fits})


def compute_lassodf():
    g = rng(2007)
    X, y, _, _ = museum.prostate()
    Xs = (X - X.mean(0)) / X.std(0)
    n = len(y)
    b_full, _ = ols(np.column_stack([np.ones(n), Xs]), y)
    mu = np.column_stack([np.ones(n), Xs]) @ b_full
    sigma = 0.7
    out = []
    for lam in (0.02, 0.08, 0.2, 0.4):
        nz = []

        def fp(Xm, yv, lam=lam):
            yc = yv - yv.mean()
            b = Le.lasso(Xm, yc, lam)
            nz.append(int(np.sum(np.abs(b) > 1e-8)))
            return yv.mean() + Xm @ b

        df = Se.df_monte_carlo(fp, Xs, mu, sigma, 600, g)
        out.append({"lam": lam, "df_mc": df, "mean_nonzero": float(np.mean(nz)) + 1})  # +1: the intercept
    return nest({"rows": out, "sigma": sigma})


def compute_tic():
    v = W.visits["visits"]
    ad = np.flatnonzero(v >= 0)
    smp = rng(28).choice(ad, 1000, replace=False)
    y = v[smp].astype(float)
    age = (W.age[smp] - 50) / 10
    X = np.column_stack([np.ones(len(y)), age])
    # Poisson MLE
    b = np.zeros(2)
    for _ in range(50):
        mu = np.exp(X @ b)
        b = b + np.linalg.solve(X.T @ (mu[:, None] * X), X.T @ (y - mu))
    mu = np.exp(X @ b)
    scores = (y - mu)[:, None] * X
    H = -(X.T @ (mu[:, None] * X))
    pen_p = Se.tic_penalty(scores, H)
    # the same for data that really are Poisson
    yp = rng(29).poisson(mu)
    bp = b.copy()
    for _ in range(50):
        m2 = np.exp(X @ bp)
        bp = bp + np.linalg.solve(X.T @ (m2[:, None] * X), X.T @ (yp - m2))
    m2 = np.exp(X @ bp)
    pen_true = Se.tic_penalty((yp - m2)[:, None] * X, -(X.T @ (m2[:, None] * X)))
    return nest({"k": 2, "tic_visits": pen_p, "tic_poisson": pen_true, "mean": float(y.mean()), "var": float(y.var())})


def compute_consistency():
    g = rng(2005)
    ns = [20, 50, 100, 200, 500, 1000, 3000]
    sigma = 1.0
    res = {"ns": ns, "aic": [], "bic": [], "aicc": []}
    for n in ns:
        hits = {"aic": 0, "bic": 0, "aicc": 0}
        for _ in range(300):
            x = g.uniform(-2, 2, n)
            y = 1 + 0.5 * x - 0.4 * x ** 2 + sigma * g.standard_normal(n)
            crit = {"aic": [], "bic": [], "aicc": []}
            for d in range(0, 7):
                X = np.vander(x, d + 1, increasing=True)
                _, rss = ols(X, y)
                ll = Se.gaussian_ll(rss, n)
                k = d + 2
                crit["aic"].append(Se.aic(ll, k))
                crit["bic"].append(Se.bic(ll, k, n))
                crit["aicc"].append(Se.aicc(ll, k, n))
            for c in hits:
                hits[c] += int(np.argmin(crit[c]) == 2)
        for c in hits:
            res[c].append(hits[c] / 300)
    # truth not in the candidate set: prediction risk of the selected model
    risk = {"ns": [50, 200, 1000], "aic": [], "bic": [], "aicc": []}
    for n in risk["ns"]:
        r = {"aic": 0.0, "bic": 0.0, "aicc": 0.0}
        xt = np.linspace(-2, 2, 400)
        for _ in range(200):
            x = g.uniform(-2, 2, n)
            y = np.sin(2 * x) * np.exp(0.3 * x) + 0.5 * g.standard_normal(n)
            fits = []
            for d in range(0, 13):
                X = np.vander(x, d + 1, increasing=True)
                b, rss = ols(X, y)
                ll = Se.gaussian_ll(rss, n)
                fits.append((Se.aic(ll, d + 2), Se.bic(ll, d + 2, n), Se.aicc(ll, d + 2, n), b, d))
            for c, idx in (("aic", 0), ("bic", 1), ("aicc", 2)):
                bsel = min(fits, key=lambda t: t[idx])
                pred = np.vander(xt, bsel[4] + 1, increasing=True) @ bsel[3]
                r[c] += np.mean((pred - np.sin(2 * xt) * np.exp(0.3 * xt)) ** 2)
        for c in r:
            risk[c].append(r[c] / 200)
    return nest({"select": res, "risk": risk})


def compute_prostate():
    X, y, train, names = museum.prostate()
    Xtr, ytr, Xte, yte = X[train], y[train], X[~train], y[~train]
    mu, sd = Xtr.mean(0), Xtr.std(0)
    Ztr, Zte = (Xtr - mu) / sd, (Xte - mu) / sd
    n = len(ytr)
    bs = Se.best_subset(Ztr, ytr)
    crit = []
    for b in bs:
        k = b["size"] + 2
        ll = Se.gaussian_ll(b["rss"], n)
        crit.append({"size": b["size"], "subset": [names[j] for j in b["subset"]], "rss": b["rss"], "aic": Se.aic(ll, k),
                     "bic": Se.bic(ll, k, n)})
    # 10-fold CV of best subset of each size (subsets re-chosen within each fold)
    g = rng(1989)
    folds = Le.kfold(n, 10, g)
    cv = np.zeros((10, len(bs)))
    for f, te_idx in enumerate(folds):
        tr_idx = np.setdiff1d(np.arange(n), te_idx)
        bsf = Se.best_subset(Ztr[tr_idx], ytr[tr_idx])
        for k, b in enumerate(bsf):
            cols = b["subset"]
            Xd = np.column_stack([np.ones(len(tr_idx)), Ztr[tr_idx][:, cols]])
            coef, _ = ols(Xd, ytr[tr_idx])
            pred = np.column_stack([np.ones(len(te_idx)), Ztr[te_idx][:, cols]]) @ coef
            cv[f, k] = np.mean((ytr[te_idx] - pred) ** 2)
    cv_mean, cv_se = cv.mean(0), cv.std(0, ddof=1) / np.sqrt(10)
    best_cv = int(np.argmin(cv_mean))
    one_se = int(min(k for k in range(len(bs)) if cv_mean[k] <= cv_mean[best_cv] + cv_se[best_cv]))

    def test_err(cols):
        Xd = np.column_stack([np.ones(n), Ztr[:, cols]])
        coef, _ = ols(Xd, ytr)
        return float(np.mean((yte - np.column_stack([np.ones(len(yte)), Zte[:, cols]]) @ coef) ** 2))

    picks = {"aic": int(np.argmin([c["aic"] for c in crit])), "bic": int(np.argmin([c["bic"] for c in crit])), "cv": best_cv,
             "cv1se": one_se}
    tests = {k: {"size": v, "subset": crit[v]["subset"], "test": test_err(bs[v]["subset"])} for k, v in picks.items()}
    tests["full"] = {"size": 8, "subset": names, "test": test_err(list(range(8)))}
    tests["null"] = {"size": 0, "subset": [], "test": float(np.mean((yte - ytr.mean()) ** 2))}
    # lasso and ridge tuned by the same folds
    lams = np.geomspace(0.002, 1.0, 40)

    def cv_pen(fit):
        e = np.zeros(len(lams))
        for te_idx in folds:
            tr_idx = np.setdiff1d(np.arange(n), te_idx)
            ym = ytr[tr_idx].mean()
            for i, lam in enumerate(lams):
                b = fit(Ztr[tr_idx], ytr[tr_idx] - ym, lam)
                e[i] += np.mean((ytr[te_idx] - ym - Ztr[te_idx] @ b) ** 2)
        return e / 10

    out_pen = {}
    for name, fit in (("lasso", Le.lasso), ("ridge", lambda X_, y_, l: Le.ridge(X_, y_, l * len(y_)))):
        e = cv_pen(fit)
        lam = float(lams[int(np.argmin(e))])
        b = fit(Ztr, ytr - ytr.mean(), lam)
        out_pen[name] = {"lam": lam, "coef": b, "test": float(np.mean((yte - ytr.mean() - Zte @ b) ** 2)),
                         "nonzero": int(np.sum(np.abs(b) > 1e-8))}
    return nest({"names": names, "crit": crit, "cv_mean": cv_mean, "cv_se": cv_se, "picks": picks, "tests": tests,
                 "pen": out_pen, "n_train": n, "n_test": int(len(yte))})


def compute_cv():
    g = rng(2024)
    n, p, sigma = 50, 10, 1.0
    beta = np.r_[np.ones(4), np.zeros(p - 4)]
    rows = []
    for _ in range(400):
        X = g.standard_normal((n, p))
        y = X @ beta + sigma * g.standard_normal(n)
        Xd = np.column_stack([np.ones(n), X])
        b, rss = ols(Xd, y)
        press = Se.press(Xd, y)
        gcv = Se.gcv(rss, p + 1, n)
        folds = Le.kfold(n, 10, g)
        e = []
        for te_idx in folds:
            tr = np.setdiff1d(np.arange(n), te_idx)
            bb, _ = ols(Xd[tr], y[tr])
            e.append(np.mean((y[te_idx] - Xd[te_idx] @ bb) ** 2))
        cv10 = float(np.mean(e))
        # the true conditional error of this fit, on new data
        cond = sigma ** 2 + float(np.sum((b[1:] - beta) ** 2)) + b[0] ** 2
        rows.append((press, gcv, cv10, cond))
    r = np.array(rows)
    return nest({"press": r[:, 0], "gcv": r[:, 1], "cv10": r[:, 2], "cond": r[:, 3], "mean_cond": float(r[:, 3].mean()),
                 "mean_cv": float(r[:, 2].mean()), "corr": float(np.corrcoef(r[:, 2], r[:, 3])[0, 1]),
                 "corr_press_gcv": float(np.corrcoef(r[:, 0], r[:, 1])[0, 1])})


def compute_loo():
    lab, y, s = museum.eight_schools()
    grid = np.linspace(0, 60, 3001)
    h = B.hier_normal(y, s, grid)
    g = rng(2017)
    S = 8000
    dr = h.draws(S, g)
    L_h = stats.norm.logpdf(y[None, :], dr["theta"], s[None, :])
    w = 1 / s ** 2
    pm, pse = np.sum(w * y) / w.sum(), 1 / np.sqrt(w.sum())
    mu = g.normal(pm, pse, S)
    L_c = stats.norm.logpdf(y[None, :], mu[:, None], s[None, :])
    th_np = y[None, :] + s[None, :] * g.standard_normal((S, 8))  # flat priors, each school alone
    L_n = stats.norm.logpdf(y[None, :], th_np, s[None, :])
    out = {}
    for name, L in (("hierarchical", L_h), ("pooled", L_c), ("separate", L_n)):
        lo = Se.psis_loo(L)
        wa = Se.waic(L)
        out[name] = {"elpd": lo["elpd"], "se": lo["se"], "p_loo": lo["p_loo"], "khat": lo["khat"], "waic": wa["elpd"],
                     "p_waic": wa["p_waic"]}
    # exact leave-one-school-out for the hierarchical model
    exact = 0.0
    for j in range(8):
        m = np.arange(8) != j
        hj = B.hier_normal(y[m], s[m], grid)
        dens = hj.post_tau
        # predictive for a new school: y_j ~ N(mu_hat(tau), V_mu(tau) + tau^2 + s_j^2)
        pred = stats.norm.pdf(y[j], hj.mu_hat, np.sqrt(hj.v_mu + grid ** 2 + s[j] ** 2))
        exact += np.log(np.trapezoid(dens * pred, grid))
    out["hierarchical"]["exact"] = float(exact)
    # exact LOO for complete pooling: the other seven's pooled estimate
    ex_c = 0.0
    for j in range(8):
        m = np.arange(8) != j
        ww = w[m]
        pmj, psej = np.sum(ww * y[m]) / ww.sum(), 1 / np.sqrt(ww.sum())
        ex_c += stats.norm.logpdf(y[j], pmj, np.sqrt(psej ** 2 + s[j] ** 2))
    out["pooled"]["exact"] = float(ex_c)
    out["labels"] = lab
    return nest(out)


def compute_rlct():
    """p(x | a, b) = (1 - a) N(0, 1) + a N(b, 1), a ~ U(0, 1), b ~ U(-2, 2); the truth is N(0, 1) (a b = 0).  The
    free energy F_n = -log Z_n + sum log p(x | truth) grows like lambda log n with lambda = 1/2, against d/2 = 1 for a
    regular two-parameter model."""
    g = rng(2010)
    ns = [30, 100, 300, 1000, 3000, 10000]
    A = np.linspace(0, 1, 201)
    Bg = np.linspace(-2, 2, 241)
    out = {"ns": ns, "F": [], "F_regular": []}
    for n in ns:
        Fs, Fr = [], []
        for _ in range(6):
            x = g.standard_normal(n)
            # log likelihood ratio on the grid: sum_i log(1 - a + a exp(b x_i - b^2/2)), one b at a time
            ll = np.empty((len(A), len(Bg)))
            for j, b in enumerate(Bg):
                e = np.exp(b * x - 0.5 * b * b) - 1.0
                ll[:, j] = np.sum(np.log1p(A[:, None] * e[None, :]), axis=1)
            mx = ll.max()
            Z = np.trapezoid(np.trapezoid(np.exp(ll - mx), Bg, axis=1), A) / 4.0  # uniform prior density 1/4
            Fs.append(-(np.log(Z) + mx))
            # a regular two-parameter model for comparison: N(m, s^2) with m ~ U(-2, 2), log s ~ U(-1, 1)
            ms = np.linspace(-0.6, 0.6, 301)
            ls = np.linspace(-0.4, 0.4, 301)
            M, LS = np.meshgrid(ms, ls, indexing="ij")
            xb, x2 = x.mean(), np.mean(x ** 2)
            llr = n * (-LS - 0.5 * (x2 - 2 * M * xb + M ** 2) / np.exp(2 * LS)) + 0.5 * n * x2
            mr = llr.max()
            Zr = np.trapezoid(np.trapezoid(np.exp(llr - mr), ls, axis=1), ms) / (4.0 * 2.0)
            Fr.append(-(np.log(Zr) + mr))
        out["F"].append(float(np.mean(Fs)))
        out["F_regular"].append(float(np.mean(Fr)))
    ln = np.log(ns)
    out["slope"] = float(np.polyfit(ln, out["F"], 1)[0])
    out["slope_regular"] = float(np.polyfit(ln, out["F_regular"], 1)[0])
    return nest(out)


def compute_mdl():
    ns = [10, 30, 100, 300, 1000, 3000, 10000]
    regret = [Se.nml_bernoulli_regret(n) for n in ns]
    o = load_optimism_data()
    x, y = np.asarray(o["x"]), np.asarray(o["y"])
    n = len(y)
    rows = []
    for d in range(0, 10):
        X = np.vander(x, d + 1, increasing=True)
        _, rss = ols(X, y)
        data_bits = -Se.gaussian_ll(rss, n) / np.log(2)
        param_bits = 0.5 * (d + 2) * np.log2(n)
        rows.append({"deg": d, "data": float(data_bits), "params": float(param_bits), "total": float(data_bits + param_bits)})
    return nest({"ns": ns, "regret": regret, "approx": [0.5 * np.log(n * np.pi / 2) for n in ns], "rows": rows,
                 "best": int(np.argmin([r["total"] for r in rows]))})


def load_optimism_data():
    try:
        return load("optimism")
    except Exception:
        return compute_optimism()


def compute_averaging():
    g = rng(2018)
    res = {"ns": [20, 50, 100, 200, 500], "bma": [], "stack": [], "score_bma": [], "score_stack": [], "score_best": []}
    for n in res["ns"]:
        wb, ws, sb, ss, sbest = [], [], [], [], []
        for _ in range(100):
            z = g.random(n) < 0.5
            y = np.where(z, g.normal(-2, 1, n), g.normal(2, 1, n))
            yt = np.where(g.random(2000) < 0.5, g.normal(-2, 1, 2000), g.normal(2, 1, 2000))
            le, lpd, pred = [], [], []
            for c in (-2.0, 2.0):
                # model k: y ~ N(c_k, 1), its mean all but fixed (prior SD 0.01): two candidates, neither true
                tau2 = 1e-4
                v = 1 / (1 / tau2 + n)
                m = v * (c / tau2 + y.sum())
                le.append(stats.multivariate_normal(np.full(n, c), np.eye(n) + tau2).logpdf(y) if n <= 200 else
                          _log_evidence_normal(y, c, tau2))
                # LOO predictive densities
                vi = 1 / (1 / tau2 + n - 1)
                mi = vi * (c / tau2 + y.sum() - y)
                lpd.append(stats.norm.logpdf(y, mi, np.sqrt(vi + 1)))
                pred.append(stats.norm.pdf(yt, m, np.sqrt(v + 1)))
            wbma = Se.bma_weights(le)
            wst = Se.stacking_weights(np.column_stack(lpd))
            pred = np.array(pred)
            wb.append(wbma[0])
            ws.append(wst[0])
            sb.append(np.mean(np.log(wbma @ pred)))
            ss.append(np.mean(np.log(wst @ pred)))
            sbest.append(max(np.mean(np.log(pred[0])), np.mean(np.log(pred[1]))))
        res["bma"].append(float(np.mean(np.abs(np.array(wb) - 0.5)) + 0.5))
        res["stack"].append(float(np.mean(np.abs(np.array(ws) - 0.5)) + 0.5))
        res["score_bma"].append(float(np.mean(sb)))
        res["score_stack"].append(float(np.mean(ss)))
        res["score_best"].append(float(np.mean(sbest)))
    xs = np.linspace(-6, 6, 300)
    res["xs"] = xs
    res["truth"] = 0.5 * stats.norm.pdf(xs, -2, 1) + 0.5 * stats.norm.pdf(xs, 2, 1)
    return nest(res)


def _log_evidence_normal(y, c, tau2):
    n = len(y)
    # y ~ N(c 1, I + tau2 11'): Sherman-Morrison
    r = y - c
    quad = r @ r - tau2 * r.sum() ** 2 / (1 + n * tau2)
    logdet = np.log(1 + n * tau2)
    return float(-0.5 * (n * np.log(2 * np.pi) + logdet + quad))


def compute_subsets():
    g = rng(2020)
    n, p, s, rho = 100, 10, 5, 0.35
    Sig = rho ** np.abs(np.subtract.outer(np.arange(p), np.arange(p)))
    Lc = np.linalg.cholesky(Sig)
    beta = np.zeros(p)
    beta[np.linspace(0, p - 1, s).astype(int)] = 1.0
    snrs = [0.05, 0.25, 1.0, 6.0]
    out = {"snrs": snrs, "best": [], "forward": [], "lasso": []}
    for snr in snrs:
        sigma = np.sqrt(beta @ Sig @ beta / snr)
        rr = {"best": [], "forward": [], "lasso": []}
        for _ in range(25):
            X = g.standard_normal((n, p)) @ Lc.T
            y = X @ beta + sigma * g.standard_normal(n)
            Xv = g.standard_normal((n, p)) @ Lc.T
            yv = Xv @ beta + sigma * g.standard_normal(n)

            def risk(b, b0):
                d = b - beta
                return float(d @ Sig @ d + b0 ** 2) / float(beta @ Sig @ beta)

            # tune on a validation set (as HTT do)
            for meth in ("best", "forward"):
                path = Se.best_subset(X, y) if meth == "best" else Se.forward_stepwise(X, y)
                errs, coefs = [], []
                for b_ in path:
                    cols = b_["subset"]
                    Xd = np.column_stack([np.ones(n), X[:, cols]])
                    cf, _ = ols(Xd, y)
                    full = np.zeros(p)
                    full[cols] = cf[1:]
                    coefs.append((full, cf[0]))
                    errs.append(np.mean((yv - cf[0] - Xv @ full) ** 2))
                bsel, b0 = coefs[int(np.argmin(errs))]
                rr[meth].append(risk(bsel, b0))
            lams = np.geomspace(0.001, 2.0, 40) * sigma
            best_e, best_b = np.inf, None
            for lam in lams:
                bl = Le.lasso(X - X.mean(0), y - y.mean(), lam)
                b0 = y.mean() - X.mean(0) @ bl
                e = np.mean((yv - b0 - Xv @ bl) ** 2)
                if e < best_e:
                    best_e, best_b = e, (bl, b0)
            rr["lasso"].append(risk(*best_b))
        for k in rr:
            out[k].append(float(np.mean(rr[k])))
    return nest(out)


def compute_pit():
    g = rng(1984)
    T = 2000
    mu = np.cumsum(g.normal(0, 0.3, T))
    y = mu + g.standard_normal(T)
    from explainer.stats.kit import glm as Gm
    fc = {"calibrated": (mu, 1.0), "overconfident": (mu, 0.5), "underconfident": (mu, 2.0), "biased": (mu + 0.7, 1.0)}
    out = {}
    for k, (m, s) in fc.items():
        pit = stats.norm.cdf(y, m, s)
        out[k] = {"hist": np.histogram(pit, np.linspace(0, 1, 11))[0], "log": float(-np.mean(stats.norm.logpdf(y, m, s))),
                  "crps": float(np.mean(Gm.crps_normal(m, s, y))), "cover90": float(np.mean(np.abs(y - m) <= 1.645 * s))}
    return nest(out)


def compute_board():
    """y = X beta + e, n = 100, ten independent candidate predictors, beta_1 = 0.05 and two others nonzero.  Select by
    AIC (forward stepwise); when x_1 is kept, report its usual 95% interval.  Compare with splitting (select on half,
    estimate on the other) and with the full model (no selection)."""
    g = rng(2828)
    n, p = 100, 10
    Lc = np.eye(p)  # independent predictors: beta_1 means the same in every submodel, so only selection can bias it
    beta = np.zeros(p)
    beta[0], beta[1], beta[3] = 0.05, 0.4, -0.3
    R = 2000
    hits = {"naive": 0, "split": 0, "full": 0}
    count = {"naive": 0, "split": 0, "full": 0}
    for _ in range(R):
        X = g.standard_normal((n, p)) @ Lc.T
        y = X @ beta + g.standard_normal(n)

        def aic_select(Xs, ys):
            path = Se.forward_stepwise(Xs, ys)
            m = len(ys)
            crit = [Se.aic(Se.gaussian_ll(b_["rss"], m), b_["size"] + 2) for b_ in path]
            return path[int(np.argmin(crit))]["subset"]

        def ci_for(Xs, ys, cols, j):
            Xd = np.column_stack([np.ones(len(ys)), Xs[:, cols]])
            b, rss = ols(Xd, ys)
            k = Xd.shape[1]
            se = np.sqrt(np.diag(np.linalg.inv(Xd.T @ Xd)) * rss / (len(ys) - k))
            i = cols.index(j) + 1
            t = stats.t.ppf(0.975, len(ys) - k)
            return b[i] - t * se[i], b[i] + t * se[i]

        sel = aic_select(X, y)
        if 0 in sel:
            lo, hi = ci_for(X, y, sel, 0)
            count["naive"] += 1
            hits["naive"] += int(lo <= beta[0] <= hi)
        half = g.permutation(n)
        a, b_ = half[: n // 2], half[n // 2:]
        sel2 = aic_select(X[a], y[a])
        if 0 in sel2:
            lo, hi = ci_for(X[b_], y[b_], sel2, 0)
            count["split"] += 1
            hits["split"] += int(lo <= beta[0] <= hi)
        lo, hi = ci_for(X, y, list(range(p)), 0)
        count["full"] += 1
        hits["full"] += int(lo <= beta[0] <= hi)
    rows = [
        Row(28, r"naive CI after AIC selection", r"$\beta_1 = 0.05$, \ when $x_1$ is kept", "coverage", 0.95,
            hits["naive"] / count["naive"], count["naive"]),
        Row(28, r"select on half, \ CI on the other half", r"$\beta_1 = 0.05$, \ when $x_1$ is kept", "coverage", 0.95,
            hits["split"] / count["split"], count["split"]),
        Row(28, r"full model, \ no selection", r"$\beta_1 = 0.05$", "coverage", 0.95, hits["full"] / count["full"], count["full"]),
    ]
    save_rows(28, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows], "kept_share": count["naive"] / R,
            "split_share": count["split"] / R}


def compute_stability():
    """Bootstrap the prostate training set 400 times and redo best-subset selection by AIC and by BIC each time: how often
    is each predictor kept, and how often is the original model chosen again?"""
    X, y, train, names = museum.prostate()
    Z = X[train]
    Z = (Z - Z.mean(0)) / Z.std(0)
    yt = y[train]
    n = len(yt)
    g = rng(1993)
    R = 400
    inc = {"aic": np.zeros(8), "bic": np.zeros(8)}
    models = {"aic": {}, "bic": {}}
    for _ in range(R):
        i = g.integers(0, n, n)
        bs = Se.best_subset(Z[i], yt[i])
        for c, f in (("aic", lambda ll, k: Se.aic(ll, k)), ("bic", lambda ll, k: Se.bic(ll, k, n))):
            j = int(np.argmin([f(Se.gaussian_ll(b["rss"], n), b["size"] + 2) for b in bs]))
            cols = tuple(sorted(bs[j]["subset"]))
            inc[c][list(cols)] += 1
            models[c][cols] = models[c].get(cols, 0) + 1
    orig = load("prostate")
    out = {"names": names, "R": R}
    for c in ("aic", "bic"):
        pick = orig["picks"][c]
        cols0 = tuple(sorted(names.index(v) for v in orig["crit"][pick]["subset"]))
        top = sorted(models[c].items(), key=lambda kv: -kv[1])[:3]
        out[c] = {"inclusion": inc[c] / R, "distinct": len(models[c]), "original_share": models[c].get(cols0, 0) / R,
                  "top": [{"subset": [names[j] for j in k], "share": v / R} for k, v in top]}
    return nest(out)


def compute_prostate_pit():
    """Leave-one-out PIT for normal linear models on the prostate training set.  Under the reference prior the LOO
    predictive is t with n - k - 1 df, and the PIT is the t CDF of the externally studentized residual."""
    X, y, train, names = museum.prostate()
    Z = X[train]
    Z = (Z - Z.mean(0)) / Z.std(0)
    yt = y[train]
    n = len(yt)
    out = {}
    for key, cols in (("null", []), ("two", [0, 1]), ("full", list(range(8)))):
        Xd = np.column_stack([np.ones(n), Z[:, cols]])
        k = Xd.shape[1]
        H = Xd @ np.linalg.solve(Xd.T @ Xd, Xd.T)
        h = np.diag(H)
        e = yt - H @ yt
        rss = float(e @ e)
        s2i = (rss - e ** 2 / (1 - h)) / (n - k - 1)
        scale = np.sqrt(s2i / (1 - h))
        r = (e / (1 - h)) / scale
        nu = n - k - 1
        pit = stats.t.cdf(r, nu)
        lpd = stats.t.logpdf(r, nu) - np.log(scale)
        out[key] = {"pit": pit, "hist": np.histogram(pit, np.linspace(0, 1, 6))[0], "lpd": float(np.mean(lpd)),
                    "ks_p": float(stats.kstest(pit, "uniform").pvalue), "k": k, "sd": float(np.sqrt(np.mean(scale ** 2)))}
    return nest(out)


ITEMS = {
    "freedman": compute_freedman, "optimism": compute_optimism, "lassodf": compute_lassodf, "tic": compute_tic,
    "consistency": compute_consistency, "prostate": compute_prostate, "cv": compute_cv, "loo": compute_loo,
    "rlct": compute_rlct, "mdl": compute_mdl, "averaging": compute_averaging, "subsets": compute_subsets, "pit": compute_pit,
    "board": compute_board, "stability": compute_stability, "prostate_pit": compute_prostate_pit,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
