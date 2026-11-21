"""Agora's estimation harness (Part 54): measuring a model's hidden parameters from the choices it predicts.

* **Random utility and maximum likelihood** (:func:`simulate_commuters`, :func:`logit_ml`, :func:`logit_shares`):
  McFadden's conditional logit, estimated by Newton's method with standard errors from the information matrix, and
  used to forecast the share of a new alternative.
* **The generalized method of moments** (:func:`gmm`, :func:`euler_data`, :func:`euler_moments`): Hansen's (1982)
  two-step GMM with the efficient weighting matrix, sandwich standard errors and the J-test; Hansen and Singleton's
  (1982) Euler-equation estimation on simulated returns and consumption.
* **Simulated moments** (:func:`lifecycle`, :func:`lifecycle_moments`, :func:`smm`): a finite-horizon buffer-stock
  household solved by the endogenous grid method, its age profiles matched by the method of simulated moments, after
  Gourinchas and Parker (2002), with standard errors corrected for simulation.
* **Indirect inference** (:func:`ma1_data`, :func:`indirect_ma1`): Gouriéroux, Monfort and Renault's (1993) estimator
  of an MA(1) through an autoregressive auxiliary model.
* **Sensitivity** (:func:`sensitivity`): Andrews, Gentzkow and Shapiro's (2017) matrix, -(G'WG)^-1 G'W.
* **Unobserved heterogeneity** (:func:`mixture_logit_em`): a two-type binary logit by the EM algorithm (Heckman and
  Singer 1984).
* **Validation** (:func:`school_villages`, :func:`validate_subsidy`): a schooling decision estimated on control
  villages and used to predict a subsidy's effect, then checked against the experiment (after Todd and Wolpin 2006).
* **Simulation-based inference** (:func:`amortized_ma1`): a regression from simulated summaries to parameters, the
  idea behind neural estimators.

numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.stats import chi2

# ---------------------------------------------------------------------------------------------------------------
# random utility and maximum likelihood


def simulate_commuters(n: int = 3000, beta=(-0.06, -0.5), asc=(0.0, -0.4), seed: int = 0) -> dict:
    """``n`` commuters choosing between car (0) and bus (1): utility = asc_j + beta_time x minutes + beta_cost x
    dollars + a Gumbel error. Attributes vary across commuters. Returns the attributes (n x J x 2), the alternative
    constants, the choices, and the truth."""
    rng = np.random.default_rng(seed)
    J = len(asc)
    time = np.column_stack([rng.uniform(15, 45, n), rng.uniform(25, 70, n)])[:, :J]
    cost = np.column_stack([rng.uniform(2, 8, n), rng.uniform(0.5, 2.5, n)])[:, :J]
    X = np.stack([time, cost], axis=2)
    v = np.asarray(asc)[None, :] + X @ np.asarray(beta)
    u = v + rng.gumbel(size=v.shape)
    y = np.argmax(u, axis=1)
    return {"X": X, "y": y, "beta": np.asarray(beta, float), "asc": np.asarray(asc, float), "n": n}


def _design(X, n_alt):
    """Stack attributes and alternative-specific constants (all but the first alternative) per alternative."""
    n, J, K = X.shape
    D = np.zeros((n, J, K + J - 1))
    D[:, :, :K] = X
    for j in range(1, J):
        D[:, j, K + j - 1] = 1.0
    return D


def logit_loglik(X, y, b) -> float:
    """The conditional logit's log likelihood at b (attribute coefficients, then constants for alternatives
    1..J-1)."""
    n, J, K = X.shape
    v = _design(X, J) @ np.asarray(b, float)
    v -= v.max(axis=1, keepdims=True)
    return float((v[np.arange(n), y] - np.log(np.exp(v).sum(axis=1))).sum())


def logit_ml(X, y, tol: float = 1e-10, max_iter: int = 100, b0=None) -> dict:
    """Conditional logit by Newton's method from ``b0`` (zeros by default). Parameters: one coefficient per
    attribute, then constants for alternatives 1..J-1. Standard errors from the inverse Hessian; ``trace`` holds
    every iterate."""
    n, J, K = X.shape
    D = _design(X, J)
    p = D.shape[2]
    b = np.zeros(p) if b0 is None else np.asarray(b0, float).copy()
    trace = [b.copy()]
    for it in range(max_iter):
        v = D @ b
        v -= v.max(axis=1, keepdims=True)
        P = np.exp(v)
        P /= P.sum(axis=1, keepdims=True)
        xbar = np.einsum("nj,njk->nk", P, D)
        g = (D[np.arange(n), y] - xbar).sum(axis=0)
        dev = D - xbar[:, None, :]
        H = -np.einsum("nj,njk,njl->kl", P, dev, dev)
        step = np.linalg.solve(H, -g)
        b = b + step
        trace.append(b.copy())
        if np.max(np.abs(step)) < tol:
            break
    v = D @ b
    v -= v.max(axis=1, keepdims=True)
    P = np.exp(v)
    P /= P.sum(axis=1, keepdims=True)
    ll = float(np.log(P[np.arange(n), y]).sum())
    cov = np.linalg.inv(-H)
    return {"b": b, "se": np.sqrt(np.diag(cov)), "cov": cov, "loglik": ll, "iters": it + 1, "K": K, "J": J,
            "trace": np.array(trace)}


def logit_shares(X, b, K: int) -> np.ndarray:
    """Predicted shares of each alternative, averaged over the commuters, for attributes X (n x J x K) and
    coefficients b (K attribute coefficients, then constants for alternatives 1..J-1)."""
    n, J, _ = X.shape
    asc = np.concatenate([[0.0], b[K:K + J - 1]])
    v = X @ b[:K] + asc[None, :]
    v -= v.max(axis=1, keepdims=True)
    P = np.exp(v)
    P /= P.sum(axis=1, keepdims=True)
    return P.mean(axis=0)


def nested_shares(V, nests, lam) -> np.ndarray:
    """Choice probabilities of a nested logit, each person's (rows of V, n x J): alternatives in ``nests`` (lists of
    column indices covering every alternative) with dissimilarity parameters ``lam`` (one per nest; 1 gives the plain
    logit). P(j) = P(nest) P(j | nest), with P(j | nest) a logit in V / lambda and P(nest) a logit in the nests'
    inclusive values lambda log sum exp(V / lambda)."""
    V = np.atleast_2d(np.asarray(V, float))
    n, J = V.shape
    P = np.zeros((n, J))
    iv = np.empty((n, len(nests)))
    for k, (nest, lm) in enumerate(zip(nests, lam)):
        z = V[:, nest] / lm
        m = z.max(axis=1, keepdims=True)
        e = np.exp(z - m)
        P[:, nest] = e / e.sum(axis=1, keepdims=True)
        iv[:, k] = lm * (m[:, 0] + np.log(e.sum(axis=1)))
    m = iv.max(axis=1, keepdims=True)
    pn = np.exp(iv - m)
    pn /= pn.sum(axis=1, keepdims=True)
    for k, nest in enumerate(nests):
        P[:, nest] *= pn[:, [k]]
    return P


# ---------------------------------------------------------------------------------------------------------------
# GMM


def gmm(moments, theta0, two_step: bool = True, method: str = "Nelder-Mead") -> dict:
    """Hansen's GMM. ``moments(theta)`` returns an n x m array of moment contributions whose mean is zero at the
    truth. First step with the identity, second with the inverse of their covariance. Returns the estimate,
    sandwich standard errors, the J statistic with its p-value, and G and W for sensitivity."""
    theta0 = np.atleast_1d(np.asarray(theta0, float))

    def obj(th, W):
        g = moments(th).mean(axis=0)
        return float(g @ W @ g)

    m = moments(theta0).shape[1]
    W = np.eye(m)
    res = minimize(obj, theta0, args=(W,), method=method, options={"xatol": 1e-10, "fatol": 1e-14,
                                                                     "maxiter": 20000})
    th = res.x
    if two_step:
        gi = moments(th)
        S = np.cov(gi, rowvar=False, bias=True)
        W = np.linalg.inv(S)
        res = minimize(obj, th, args=(W,), method=method, options={"xatol": 1e-10, "fatol": 1e-16,
                                                                   "maxiter": 20000})
        th = res.x
    gi = moments(th)
    n = gi.shape[0]
    gbar = gi.mean(axis=0)
    S = np.cov(gi, rowvar=False, bias=True)
    G = np.empty((m, len(th)))
    for k in range(len(th)):
        h = 1e-5 * max(1.0, abs(th[k]))
        e = np.zeros(len(th))
        e[k] = h
        G[:, k] = (moments(th + e).mean(axis=0) - moments(th - e).mean(axis=0)) / (2 * h)
    A = np.linalg.inv(G.T @ W @ G)
    cov = A @ G.T @ W @ S @ W @ G @ A / n
    J = float(n * gbar @ np.linalg.inv(S) @ gbar)
    df = m - len(th)
    return {"theta": th, "se": np.sqrt(np.diag(cov)), "cov": cov, "J": J, "df": df,
            "p_J": float(chi2.sf(J, df)) if df > 0 else float("nan"), "G": G, "W": W, "S": S, "n": n}


def euler_data(T: int = 2000, beta: float = 0.97, gamma: float = 3.0, rho: float = 0.3, sigma_g: float = 0.02,
               mu_g: float = 0.02, sigma_u=(0.03, 0.12), seed: int = 0) -> dict:
    """Consumption growth g_t = mu + rho (g_{t-1} - mu) + shocks, and assets whose gross returns satisfy the Euler
    equation E_t[beta exp(-gamma g_{t+1}) R_{t+1}] = 1 exactly: R = exp(c + gamma g_{t+1} + u), with u independent
    noise of s.d. sigma_u (a bond-like asset and a riskier one) and c = -log beta - sigma_u^2 / 2."""
    rng = np.random.default_rng(seed)
    g = np.empty(T + 1)
    g[0] = mu_g
    for t in range(1, T + 1):
        g[t] = mu_g + rho * (g[t - 1] - mu_g) + sigma_g * rng.standard_normal()
    R = np.empty((T, len(sigma_u)))
    for j, su in enumerate(sigma_u):
        u = su * rng.standard_normal(T)
        # R = exp(c + gamma g_{t+1} + u) gives E_t[beta exp(-gamma g_{t+1}) R] = beta exp(c + su^2/2) = 1
        c = -np.log(beta) - su ** 2 / 2
        R[:, j] = np.exp(c + gamma * g[1:] + u)
    return {"g": g, "R": R, "beta": beta, "gamma": gamma}


def euler_moments(data: dict, n_lags: int = 1):
    """Moment contributions for Hansen and Singleton: (beta exp(-gamma g_{t+1}) R_{t+1} - 1) times instruments
    (a constant, lagged consumption growth and lagged returns), for every asset."""
    g, R = data["g"], data["R"]
    T = R.shape[0]
    Z = [np.ones(T - n_lags)]
    for L in range(1, n_lags + 1):
        Z.append(g[n_lags + 1 - L:T + 1 - L])
        for j in range(R.shape[1]):
            Z.append(R[n_lags - L:T - L, j])
    Z = np.column_stack(Z)

    def f(theta):
        b, gm = theta
        sdf = b * np.exp(-gm * g[n_lags + 1:T + 1])
        e = sdf[:, None] * R[n_lags:T] - 1.0
        return np.concatenate([e[:, [j]] * Z for j in range(R.shape[1])], axis=1)

    return f


# ---------------------------------------------------------------------------------------------------------------
# simulated moments: a life-cycle household


def lifecycle(beta: float, gamma: float, T: int = 50, work: int = 40, R: float = 1.03, sigma: float = 0.15,
              n_e: int = 5, n_a: int = 120, a_max: float = 40.0, pension: float = 0.4, profile=None) -> dict:
    """A household that works for ``work`` years with income profile_t x e (e a persistent shock, Rouwenhorst with
    persistence 0.95), then receives a pension of ``pension`` times its last earnings for the remaining years, and
    consumes everything left at the end; no borrowing. Solved backward by the endogenous grid method. Returns the
    consumption rule for each age on the asset grid."""
    from . import solve as S

    z, P = S.rouwenhorst(n_e, 0.95, sigma * np.sqrt(1 - 0.95 ** 2))
    e = np.exp(z)
    pi = np.linalg.matrix_power(P, 500)[0]
    e /= pi @ e
    if profile is None:
        age = np.arange(T)
        profile = np.exp(0.03 * age - 0.0006 * age ** 2)
        profile[work:] = pension * profile[work - 1]
    a = a_max * np.linspace(0, 1, n_a) ** 2
    C = np.empty((T, n_a, n_e))
    y = profile[-1] * e
    C[-1] = R * a[:, None] + y[None, :]
    for t in range(T - 2, -1, -1):
        y = profile[t] * e
        emu = (C[t + 1] ** (-gamma)) @ P.T
        c_end = (beta * R * emu) ** (-1 / gamma)
        a_end = (c_end + a[:, None] - y[None, :]) / R
        for s in range(n_e):
            col = np.interp(a, a_end[:, s], c_end[:, s])
            bind = a < a_end[0, s]
            col[bind] = R * a[bind] + y[s]
            C[t, :, s] = col
    return {"C": C, "a": a, "e": e, "P": P, "pi": pi, "profile": profile, "R": R, "T": T}


def lifecycle_moments(sol: dict, n: int = 2000, seed: int = 0, bins: int = 10, wealth_from: int = 4,
                      per_person: bool = False):
    """Simulate ``n`` households from zero wealth with common random numbers; return mean consumption in each of
    ``bins`` age bins and mean wealth in the bins from ``wealth_from`` on (early on, most households hold almost
    nothing), or each person's contributions to those means."""
    rng = np.random.default_rng(seed)
    C, a, e, P, pi, prof, R, T = (sol[k] for k in ("C", "a", "e", "P", "pi", "profile", "R", "T"))
    cum = np.cumsum(P, axis=1)
    s = rng.choice(len(e), size=n, p=pi)
    w = np.zeros(n)
    cons = np.empty((T, n))
    wealth = np.empty((T, n))
    inc = np.empty((T, n))
    u = rng.random((T, n))
    for t in range(T):
        y = prof[t] * e[s]
        c = np.empty(n)
        for j in range(len(e)):
            sel = s == j
            c[sel] = np.interp(w[sel], a, C[t, :, j])
        cons[t], wealth[t], inc[t] = c, w, y
        w = np.maximum(R * w + y - c, 0.0)
        s = (u[t][:, None] > cum[s]).sum(axis=1)
    edges = np.linspace(0, T, bins + 1).astype(int)
    pairs = list(zip(edges[:-1], edges[1:]))
    if per_person:
        out = [cons[lo:hi].mean(axis=0) for lo, hi in pairs]
        out += [wealth[lo:hi].mean(axis=0) for lo, hi in pairs[wealth_from:]]
        return np.column_stack(out)
    mc = [float(cons[lo:hi].mean()) for lo, hi in pairs]
    mw = [float(wealth[lo:hi].mean()) for lo, hi in pairs[wealth_from:]]
    return np.array(mc + mw)


def smm(data_moments, data_contrib, simulate, theta0, step=None, S: int = 5, diagonal: bool = False) -> dict:
    """The method of simulated moments: choose theta so that the simulated moments (averaged over ``S`` simulated
    samples of the data's size, common random numbers) match the data's. Moments with no variation in the data are
    dropped; the rest are weighted by the inverse of their covariance matrix (efficient, so the J statistic is
    chi-squared), or of their variances alone with ``diagonal``. ``step`` sets the size of Nelder and Mead's first
    simplex in each parameter. Sandwich standard errors, corrected for simulation by (1 + 1/S)."""
    data_moments = np.asarray(data_moments, float)
    n = data_contrib.shape[0]
    V_full = np.cov(data_contrib, rowvar=False) / n
    keep = np.diag(V_full) > 1e-10 * np.max(np.diag(V_full))
    V = V_full[np.ix_(keep, keep)]
    W = np.diag(1 / np.diag(V)) if diagonal else np.linalg.inv(V)
    target = data_moments[keep]

    def sim(th):
        return np.asarray(simulate(th), float)[keep]

    def obj(th):
        diff = sim(th) - target
        return float(diff @ W @ diff)

    x0 = np.asarray(theta0, float)
    k = len(x0)
    step = np.full(k, 0.05) * np.maximum(np.abs(x0), 1e-3) if step is None else np.asarray(step, float)
    simplex = np.vstack([x0] + [x0 + step[j] * np.eye(k)[j] for j in range(k)])
    res = minimize(obj, x0, method="Nelder-Mead",
                   options={"xatol": 1e-7, "fatol": 1e-9, "maxiter": 4000, "initial_simplex": simplex})
    th = res.x
    G = np.empty((len(target), k))
    for j in range(k):
        h = 1e-3 * max(1.0, abs(th[j]))
        e = np.zeros(k)
        e[j] = h
        G[:, j] = (sim(th + e) - sim(th - e)) / (2 * h)
    A = np.linalg.inv(G.T @ W @ G)
    cov = (1 + 1 / S) * A @ G.T @ W @ V @ W @ G @ A
    diff = sim(th) - target
    J = float(diff @ np.linalg.inv(V) @ diff) / (1 + 1 / S)
    df = len(target) - k
    return {"theta": th, "se": np.sqrt(np.diag(cov)), "cov": cov, "G": G, "W": W, "V": V, "keep": keep,
            "J": J, "df": df, "p_J": float(chi2.sf(J, df)) if df > 0 else float("nan"), "evals": res.nfev,
            "fitted": sim(th), "target": target}


def sensitivity(G, W) -> np.ndarray:
    """Andrews, Gentzkow and Shapiro's sensitivity of the estimates to the moments: Lambda = -(G'WG)^-1 G'W, so a
    small change dm in the moments moves the estimate by Lambda dm."""
    G, W = np.asarray(G, float), np.asarray(W, float)
    return -np.linalg.inv(G.T @ W @ G) @ G.T @ W


# ---------------------------------------------------------------------------------------------------------------
# indirect inference


def ma1_data(theta: float, n: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    e = rng.standard_normal(n + 1)
    return e[1:] + theta * e[:-1]


def _ar_coef(y, p: int) -> np.ndarray:
    Y = y[p:]
    X = np.column_stack([y[p - k:len(y) - k] for k in range(1, p + 1)])
    return np.linalg.lstsq(X, Y, rcond=None)[0]


def indirect_ma1(y, p: int = 3, H: int = 10, seed: int = 1) -> dict:
    """Indirect inference for an MA(1): fit an AR(p) to the data; choose theta so that AR(p) fits to H simulated
    samples (fixed draws) give the same coefficients on average. Also the naive estimate from the first
    autocorrelation, theta solving rho_1 = theta / (1 + theta^2)."""
    n = len(y)
    target = _ar_coef(y, p)
    rng = np.random.default_rng(seed)
    E = rng.standard_normal((H, n + 1))

    def sim(th):
        return np.mean([_ar_coef(E[h, 1:] + th * E[h, :-1], p) for h in range(H)], axis=0)

    res = minimize_scalar(lambda th: float(np.sum((sim(th) - target) ** 2)), bounds=(-0.95, 0.95),
                          method="bounded", options={"xatol": 1e-8})
    r1 = float(np.corrcoef(y[1:], y[:-1])[0, 1])
    naive = float((1 - np.sqrt(max(1 - 4 * r1 * r1, 0.0))) / (2 * r1)) if abs(r1) > 1e-12 else 0.0
    return {"theta": float(res.x), "aux": target, "naive": naive, "r1": r1}


# ---------------------------------------------------------------------------------------------------------------
# unobserved heterogeneity


def mixture_logit_em(x, y, n_obs: int, groups, iters: int = 500, seed: int = 0) -> dict:
    """A binary logit with two unobserved types that differ in their constant, P(y = 1) = L(alpha_k + x b), each
    person observed ``n_obs`` times (rows grouped by ``groups``); ``x`` is one covariate or several (columns).
    Estimated by EM: type probabilities per person (E-step), then weighted logits (M-step). ``b`` is returned as a
    number for one covariate, an array for several."""
    x, y, groups = np.asarray(x, float), np.asarray(y, float), np.asarray(groups)
    one = x.ndim == 1
    X = x[:, None] if one else x
    kx = X.shape[1]
    people = np.unique(groups)
    rng = np.random.default_rng(seed)
    a = np.array([-1.0, 1.0]) + 0.1 * rng.standard_normal(2)
    b, share = np.zeros(kx), 0.5
    idx = np.searchsorted(people, groups)
    ll_old = -np.inf
    for it in range(iters):
        lp = []
        xb = X @ b
        for k in range(2):
            p = np.clip(1 / (1 + np.exp(-(a[k] + xb))), 1e-12, 1 - 1e-12)
            l_row = y * np.log(p) + (1 - y) * np.log(1 - p)
            lp.append(np.bincount(idx, weights=l_row, minlength=len(people)))
        lp = np.array(lp)
        prior = np.array([share, 1 - share])[:, None]
        m = (lp + np.log(prior)).max(axis=0)
        num = np.exp(lp + np.log(prior) - m)
        post = num / num.sum(axis=0)
        ll = float((m + np.log(num.sum(axis=0))).sum())
        share = float(post[0].mean())
        w = post[:, idx]
        th = np.concatenate([a, b])
        for _ in range(25):
            g = np.zeros(2 + kx)
            Hm = np.zeros((2 + kx, 2 + kx))
            for k in range(2):
                p = 1 / (1 + np.exp(-(th[k] + X @ th[2:])))
                r = w[k] * (y - p)
                v = w[k] * p * (1 - p)
                g[k] += r.sum()
                g[2:] += X.T @ r
                Hm[k, k] -= v.sum()
                Hm[k, 2:] -= X.T @ v
                Hm[2:, k] -= X.T @ v
                Hm[2:, 2:] -= (X * v[:, None]).T @ X
            step = np.linalg.solve(Hm, -g)
            th = th + step
            if np.max(np.abs(step)) < 1e-10:
                break
        a, b = th[:2], th[2:]
        if ll - ll_old < 1e-9:
            break
        ll_old = ll
    o = np.argsort(a)
    return {"alpha": a[o], "b": float(b[0]) if one else b, "share_low": share if o[0] == 0 else 1 - share,
            "loglik": ll, "iters": it + 1}


def pooled_logit(X, y) -> dict:
    """A binary logit with a constant, by Newton's method, with standard errors from the inverse Hessian."""
    X = np.column_stack([np.ones(len(y)), np.asarray(X, float).reshape(len(y), -1)])
    y = np.asarray(y, float)
    b = np.zeros(X.shape[1])
    for _ in range(60):
        p = 1 / (1 + np.exp(-X @ b))
        g = X.T @ (y - p)
        Hm = -(X * (p * (1 - p))[:, None]).T @ X
        step = np.linalg.solve(Hm, -g)
        b += step
        if np.max(np.abs(step)) < 1e-12:
            break
    return {"b": b, "se": np.sqrt(np.diag(np.linalg.inv(-Hm)))}


# ---------------------------------------------------------------------------------------------------------------
# validation: a schooling subsidy


def school_villages(n_villages: int = 200, per: int = 60, a0: float = 1.0, a_w: float = 0.08, a_x: float = 0.5,
                    subsidy: float = 10.0, treated_share: float = 0.5, label_effect: float = 0.0,
                    seed: int = 0) -> dict:
    """Children in villages where a child's wage varies attend school if a0 + a_x x - a_w (wage - subsidy) +
    logistic error > 0 (x a household trait). Half the villages are randomly given a subsidy for attendance. An
    optional ``label_effect`` adds to the subsidy's effect beyond its money value."""
    rng = np.random.default_rng(seed)
    wage = rng.uniform(5, 30, n_villages)
    treated = rng.random(n_villages) < treated_share
    v_id = np.repeat(np.arange(n_villages), per)
    x = rng.standard_normal(n_villages * per)
    w = wage[v_id]
    s = np.where(treated[v_id], subsidy, 0.0)
    util = a0 + a_x * x - a_w * (w - s) + np.where(treated[v_id], label_effect, 0.0) + rng.logistic(
        size=len(x))
    y = (util > 0).astype(float)
    return {"x": x, "wage": w, "subsidy": s, "treated": treated[v_id], "y": y, "village": v_id,
            "truth": {"a0": a0, "a_w": a_w, "a_x": a_x}, "subsidy_size": subsidy}


def validate_subsidy(d: dict) -> dict:
    """Estimate the schooling logit on the control villages only (wages vary, no subsidy), predict the treated
    villages' attendance with the subsidy entering as money, and compare with what the experiment shows."""
    ctrl = ~d["treated"]
    X = np.column_stack([np.ones(ctrl.sum()), d["x"][ctrl], -d["wage"][ctrl]])
    yv = d["y"][ctrl]
    b = np.zeros(3)
    for _ in range(50):
        p = 1 / (1 + np.exp(-X @ b))
        g = X.T @ (yv - p)
        Hm = -(X * (p * (1 - p))[:, None]).T @ X
        step = np.linalg.solve(Hm, -g)
        b += step
        if np.max(np.abs(step)) < 1e-12:
            break
    cov = np.linalg.inv(-Hm)
    tr = d["treated"]
    Xt = np.column_stack([np.ones(tr.sum()), d["x"][tr], -(d["wage"][tr] - d["subsidy"][tr])])
    Xt0 = np.column_stack([np.ones(tr.sum()), d["x"][tr], -d["wage"][tr]])
    pred_with = float((1 / (1 + np.exp(-Xt @ b))).mean())
    pred_without = float((1 / (1 + np.exp(-Xt0 @ b))).mean())
    # delta-method band for the predicted effect
    def eff(bb):
        return float((1 / (1 + np.exp(-Xt @ bb))).mean() - (1 / (1 + np.exp(-Xt0 @ bb))).mean())
    grad = np.array([(eff(b + 1e-6 * np.eye(3)[k]) - eff(b - 1e-6 * np.eye(3)[k])) / 2e-6 for k in range(3)])
    se_pred = float(np.sqrt(grad @ cov @ grad))
    actual_t = float(d["y"][tr].mean())
    actual_c = float(d["y"][ctrl].mean())
    # the experiment's estimate: treated minus control villages
    v = d["village"]
    vt = np.unique(v[tr])
    vc = np.unique(v[ctrl])
    mt = np.array([d["y"][v == k].mean() for k in vt])
    mc = np.array([d["y"][v == k].mean() for k in vc])
    exp_eff = float(mt.mean() - mc.mean())
    exp_se = float(np.sqrt(mt.var(ddof=1) / len(mt) + mc.var(ddof=1) / len(mc)))
    return {"b": b, "se": np.sqrt(np.diag(cov)), "predicted_effect": pred_with - pred_without,
            "predicted_se": se_pred, "experimental_effect": exp_eff, "experimental_se": exp_se,
            "treated_rate": actual_t, "control_rate": actual_c, "pred_treated_rate": pred_with}


# ---------------------------------------------------------------------------------------------------------------
# simulation-based inference


def amortized_ma1(n: int = 500, train: int = 4000, test: int = 500, seed: int = 0) -> dict:
    """Simulate many MA(1) samples with theta drawn uniformly from (-0.9, 0.9); learn a map from summaries (the first
    three autocorrelations, with squares and products) to theta by least squares; apply it to fresh samples. The
    same idea, with a neural network as the map, is a neural estimator."""
    rng = np.random.default_rng(seed)

    def summaries(y):
        y = y - y.mean()
        v = y @ y
        r = [float(y[k:] @ y[:-k] / v) for k in (1, 2, 3)]
        return r

    def features(r):
        r = np.asarray(r)
        return np.concatenate([[1.0], r, r ** 2, [r[0] * r[1], r[0] * r[2], r[1] * r[2]], r ** 3])

    th_tr = rng.uniform(-0.9, 0.9, train)
    F = np.array([features(summaries(ma1_data(t, n, int(rng.integers(1 << 30))))) for t in th_tr])
    coef = np.linalg.lstsq(F, th_tr, rcond=None)[0]
    th_te = rng.uniform(-0.9, 0.9, test)
    pred = np.array([features(summaries(ma1_data(t, n, int(rng.integers(1 << 30))))) @ coef for t in th_te])
    return {"coef": coef, "theta": th_te, "pred": pred, "rmse": float(np.sqrt(np.mean((pred - th_te) ** 2)))}


__all__ = ["simulate_commuters", "logit_loglik", "logit_ml", "pooled_logit", "nested_shares", "logit_shares", "gmm",
           "euler_data", "euler_moments", "lifecycle", "lifecycle_moments", "smm", "sensitivity", "ma1_data",
           "indirect_ma1", "mixture_logit_em", "school_villages", "validate_subsidy", "amortized_ma1"]
