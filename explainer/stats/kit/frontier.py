"""statkit.frontier: frontiers of causal inference (Part 62 of *Statistics, Built*; causal III).

    the front-door formula and criterion                                          (Pearl 1995)
    marginal sensitivity model bounds for IPW means and the ATE               (Tan 2006; Zhao, Small & Bhattacharya 2019)
    proximal causal inference by two-stage least squares with two proxies      (Miao, Geng & Tchetgen Tchetgen 2018)
    interference: exposure mappings and Horvitz-Thompson / Hajek contrasts      (Aronow & Samii 2017)
    policy learning: empirical welfare maximization with doubly robust scores  (Kitagawa & Tetenov 2018; Athey & Wager 2021)
    dynamic treatment regimes: two-stage Q-learning                            (Murphy 2003; Robins 2004)
    causal discovery: the PC skeleton with Fisher-z tests; varsortability      (Spirtes & Glymour 1991; Reisach et al. 2021)
    surrogates: the surrogate index                                            (Athey, Chetty, Imbens & Kang 2019)
"""

from __future__ import annotations

import math
from itertools import combinations

import numpy as np
from scipy import stats

# ------------------------------------------------------------------------------------------------- front door


def front_door(y, a, m) -> dict:
    """Pearl's front-door formula for binary A and M and any Y: E[Y | do(a)] = sum_m P(m | a) sum_a' P(a') E[Y | m, a']."""
    y, a, m = (np.asarray(v, float) for v in (y, a, m))
    out = {}
    pa = {v: float(np.mean(a == v)) for v in (0, 1)}
    for av in (0, 1):
        tot = 0.0
        for mv in (0, 1):
            pm = float(np.mean(m[a == av] == mv))
            inner = sum(pa[ap] * float(np.mean(y[(m == mv) & (a == ap)])) for ap in (0, 1))
            tot += pm * inner
        out[av] = tot
    return {"mu0": out[0], "mu1": out[1], "ate": out[1] - out[0]}


def frontdoor_ok(dag, t, y, M) -> bool:
    """Pearl's front-door criterion on a ``DAG`` from statkit.causal: (i) M intercepts every directed path from t to
    y; (ii) no back-door path from t to M is open given nothing; (iii) every back-door path from M to y is blocked
    by t."""
    M = set(M)
    E = set(dag.edges)
    for p in dag.paths(t, y):
        directed = all((u, v) in E for u, v in zip(p, p[1:]))
        if directed and not (set(p[1:-1]) & M):
            return False
    for mm in M:
        for p in dag.paths(t, mm):
            if len(p) > 1 and p[1] in dag.parents[t] and dag.is_open(p, set()):
                return False
        for p in dag.paths(mm, y):
            if len(p) > 1 and p[1] in dag.parents[mm] and dag.is_open(p, {t}):
                return False
    return True


# ------------------------------------------------------------------------------------------------ sensitivity


def _hajek_extreme(y, lo_w, hi_w, maximize: bool) -> float:
    """max (or min) of sum w y / sum w over w in the box [lo_w, hi_w]: the optimum puts the upper weights on the
    largest (smallest) outcomes, so scan the n + 1 thresholds of the sorted outcomes."""
    o = np.argsort(y)
    if not maximize:
        o = o[::-1]
    ys, lo, hi = y[o], lo_w[o], hi_w[o]
    # weights: lo for the first k sorted points, hi for the rest
    cl_wy = np.r_[0, np.cumsum(lo * ys)]
    cl_w = np.r_[0, np.cumsum(lo)]
    ch_wy = np.r_[np.cumsum((hi * ys)[::-1])[::-1], 0]
    ch_w = np.r_[np.cumsum(hi[::-1])[::-1], 0]
    vals = (cl_wy + ch_wy) / (cl_w + ch_w)
    return float(vals.max() if maximize else vals.min())


def msm_bounds(y, t, ps, lam: float) -> dict:
    """Sharp bounds on the Hajek IPW estimates of E[Y(1)], E[Y(0)] and the ATE under Tan's marginal sensitivity
    model: the true propensity's odds are within a factor lam of the estimated propensity's odds (Zhao, Small &
    Bhattacharya 2019).  lam = 1 gives the usual point estimate."""
    y, t, ps = np.asarray(y, float), np.asarray(t, int), np.asarray(ps, float)
    res = {}
    for arm in (1, 0):
        idx = t == arm
        e = ps[idx] if arm == 1 else 1 - ps[idx]
        base = 1 / e - 1  # odds against the observed arm
        lo_w, hi_w = 1 + base / lam, 1 + base * lam
        res[f"hi{arm}"] = _hajek_extreme(y[idx], lo_w, hi_w, True)
        res[f"lo{arm}"] = _hajek_extreme(y[idx], lo_w, hi_w, False)
    res["ate_lo"] = res["lo1"] - res["hi0"]
    res["ate_hi"] = res["hi1"] - res["lo0"]
    return res


# --------------------------------------------------------------------------------------------------- proximal


def tsls(y, X, Z) -> dict:
    """Two-stage least squares of y on X with instruments Z (both with their own constant columns), with a
    heteroskedasticity-robust sandwich covariance."""
    y, X, Z = np.asarray(y, float), np.asarray(X, float), np.asarray(Z, float)
    PZ = Z @ np.linalg.pinv(Z.T @ Z) @ Z.T
    Xh = PZ @ X
    b = np.linalg.solve(Xh.T @ X, Xh.T @ y)
    e = y - X @ b
    A = np.linalg.inv(Xh.T @ Xh)
    meat = (Xh * e[:, None] ** 2).T @ Xh
    V = A @ meat @ A
    return {"b": b, "se": np.sqrt(np.diag(V)), "V": V}


def proximal_2sls(y, a, z, w, X=None) -> dict:
    """Proximal causal inference with a linear outcome bridge h(w, a, x) = b0 + b_a a + b_w w + b_x x: the moment
    E[(Y - h)(1, a, z, x)] = 0 makes the outcome proxy W endogenous and the treatment proxy Z its instrument
    (Miao, Geng & Tchetgen Tchetgen 2018; Tchetgen Tchetgen et al. 2020).  Returns the effect b_a and its SE."""
    n = len(y)
    cols = [np.ones(n), np.asarray(a, float)]
    W = np.atleast_2d(np.asarray(w, float).T).T
    Zp = np.atleast_2d(np.asarray(z, float).T).T
    Xc = np.empty((n, 0)) if X is None else np.atleast_2d(np.asarray(X, float).T).T
    Xd = np.column_stack(cols + [W, Xc])
    Zd = np.column_stack(cols + [Zp, Xc])
    r = tsls(y, Xd, Zd)
    return {"effect": float(r["b"][1]), "se": float(r["se"][1])}


def ols_adjusted(y, a, covs) -> dict:
    """OLS of y on (1, a, covs): the naive adjustment that treats the proxies as if they were the confounder."""
    n = len(y)
    X = np.column_stack([np.ones(n), np.asarray(a, float), np.atleast_2d(np.asarray(covs, float).T).T])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    A = np.linalg.inv(X.T @ X)
    V = A @ ((X * e[:, None] ** 2).T @ X) @ A
    return {"effect": float(b[1]), "se": float(math.sqrt(V[1, 1]))}


# ------------------------------------------------------------------------------------------------ interference


def exposures(z, adj) -> np.ndarray:
    """Aronow & Samii's four exposure conditions: own treatment (0/1) times whether any neighbour is treated:
    0 = (0, none), 1 = (0, some), 2 = (1, none), 3 = (1, some)."""
    z = np.asarray(z, int)
    nb = (np.asarray(adj) @ z) > 0
    return 2 * z + nb.astype(int)


def exposure_probs(adj, p: float, rng: np.random.Generator, reps: int = 4000) -> np.ndarray:
    """Each unit's probability of each exposure under Bernoulli(p) assignment, by simulating the design."""
    n = adj.shape[0]
    cnt = np.zeros((n, 4))
    for _ in range(reps):
        e = exposures(rng.random(n) < p, adj)
        cnt[np.arange(n), e] += 1
    return (cnt + 0.5) / (reps + 2)


def exposure_hajek(y, z, adj, pi) -> dict:
    """Hajek estimates of the mean outcome under each exposure, weighting each unit by 1 / P(its exposure)."""
    y = np.asarray(y, float)
    e = exposures(z, adj)
    out = {}
    for k in range(4):
        m = e == k
        w = 1 / pi[m, k]
        out[k] = float(np.sum(w * y[m]) / np.sum(w)) if m.any() else float("nan")
    return {"means": out, "direct": out[2] - out[0], "spill": out[1] - out[0], "total": out[3] - out[0]}


# --------------------------------------------------------------------------------------------- policy learning


def aipw_scores(y, t, mu0, mu1, ps) -> np.ndarray:
    """The doubly robust scores Gamma_i = mu1 - mu0 + t (y - mu1)/e - (1 - t)(y - mu0)/(1 - e)."""
    y, t = np.asarray(y, float), np.asarray(t, float)
    return mu1 - mu0 + t * (y - mu1) / ps - (1 - t) * (y - mu0) / (1 - ps)


def ewm_threshold(x, gamma) -> dict:
    """Empirical welfare maximization over threshold rules treat iff s * (x - c) >= 0, s in {+1, -1}: the rule
    maximizing the average score of the treated (Kitagawa & Tetenov 2018), by scanning every threshold."""
    x, g = np.asarray(x, float), np.asarray(gamma, float)
    best = (-np.inf, None, None)
    o = np.argsort(x)
    xs, gs = x[o], g[o]
    tail = np.r_[np.cumsum(gs[::-1])[::-1], 0.0]  # sum of scores for x >= xs[k]
    head = np.r_[0.0, np.cumsum(gs)]  # sum of scores for x < xs[k]
    cuts = np.r_[xs, np.inf]
    for k in range(len(cuts)):
        for s, val in ((1, tail[k]), (-1, head[k])):
            if val > best[0]:
                best = (val, cuts[k], s)
    return {"value": best[0] / len(x), "c": float(best[1]), "s": best[2]}


def apply_rule(x, rule) -> np.ndarray:
    x = np.asarray(x, float)
    return (x >= rule["c"]) if rule["s"] == 1 else (x < rule["c"])


def policy_value(gamma, treat, mu0_plus=None) -> float:
    """The estimated gain of a policy over treating no one: the average score of those it treats."""
    return float(np.mean(np.asarray(gamma) * np.asarray(treat, float)))


# --------------------------------------------------------------------------------------------- Q-learning


def q_learning(X1, A1, X2, A2, Y) -> dict:
    """Two-stage Q-learning with linear models: stage 2 regresses Y on (1, X2, A2, A2 X2) and picks the better A2;
    stage 1 regresses the stage-2 optimum on (1, X1, A1, A1 X1).  Returns the coefficients and the rules."""
    X1, A1, X2, A2, Y = (np.asarray(v, float) for v in (X1, A1, X2, A2, Y))
    n = len(Y)
    D2 = np.column_stack([np.ones(n), X2, A2, A2 * X2])
    b2 = np.linalg.lstsq(D2, Y, rcond=None)[0]

    def q2(x2, a2):
        return b2[0] + b2[1] * x2 + a2 * (b2[2] + b2[3] * x2)
    v2 = np.maximum(q2(X2, 0), q2(X2, 1))
    D1 = np.column_stack([np.ones(n), X1, A1, A1 * X1])
    b1 = np.linalg.lstsq(D1, v2, rcond=None)[0]
    return {"b1": b1, "b2": b2, "rule1": lambda x1: (b1[2] + b1[3] * np.asarray(x1)) > 0,
            "rule2": lambda x2: (b2[2] + b2[3] * np.asarray(x2)) > 0}


# --------------------------------------------------------------------------------------------- discovery


def fisher_z_indep(C, i, j, S, n) -> float:
    """p-value of the Gaussian test of X_i independent of X_j given X_S, from the correlation matrix C."""
    idx = [i, j] + list(S)
    P = np.linalg.inv(C[np.ix_(idx, idx)])
    r = -P[0, 1] / math.sqrt(P[0, 0] * P[1, 1])
    r = min(max(r, -0.999999), 0.999999)
    z = 0.5 * math.log((1 + r) / (1 - r)) * math.sqrt(n - len(S) - 3)
    return float(2 * stats.norm.sf(abs(z)))


def pc_skeleton(X, alpha: float = 0.01, max_cond: int = 3) -> dict:
    """The PC algorithm's skeleton phase (Spirtes & Glymour 1991): start complete, remove the edge i - j as soon as a
    conditioning set S of current neighbours makes them test independent; returns the adjacency and separating sets."""
    X = np.asarray(X, float)
    n, p = X.shape
    C = np.corrcoef(X.T)
    adj = np.ones((p, p), bool)
    np.fill_diagonal(adj, False)
    sep = {}
    for k in range(max_cond + 1):
        for i in range(p):
            for j in range(p):
                if i >= j or not adj[i, j]:
                    continue
                nb = [v for v in range(p) if adj[i, v] and v != j]
                for S in combinations(nb, k):
                    if fisher_z_indep(C, i, j, S, n) > alpha:
                        adj[i, j] = adj[j, i] = False
                        sep[(i, j)] = S
                        break
    return {"adj": adj, "sep": sep}


def random_linear_sem(p: int, edge_prob: float, rng: np.random.Generator, n: int, w_range=(0.5, 2.0), noise=1.0) -> dict:
    """A random DAG on p nodes in a random causal order, with edge weights of random sign and magnitude in w_range,
    and its linear Gaussian SEM sample.  Returns the weighted adjacency B (B[i, j] != 0 means i -> j), order, data."""
    order = rng.permutation(p)
    B = np.zeros((p, p))
    for a in range(p):
        for b in range(a + 1, p):
            if rng.random() < edge_prob:
                B[order[a], order[b]] = rng.uniform(*w_range) * rng.choice([-1, 1])
    X = np.zeros((n, p))
    for v in order:
        X[:, v] = X @ B[:, v] + noise * rng.standard_normal(n)
    return {"B": B, "order": order, "X": X}


def varsortability(X, B) -> float:
    """Reisach, Seiler & Weichwald's varsortability: the fraction of directed edges (i -> j, along paths) whose
    marginal variance increases along the edge; 1 means sorting by variance recovers the causal order."""
    v = np.var(X, axis=0)
    p = B.shape[0]
    R = (B != 0).astype(int)
    reach = R.copy()
    for _ in range(p):
        reach = ((reach + reach @ R) > 0).astype(int)
    pairs = [(i, j) for i in range(p) for j in range(p) if reach[i, j]]
    if not pairs:
        return float("nan")
    return float(np.mean([v[i] < v[j] for i, j in pairs]))


def sortnregress_order_accuracy(X, B) -> float:
    """The fraction of ancestral pairs i -> ... -> j that the variance ordering puts in the right order."""
    return varsortability(X, B)


# --------------------------------------------------------------------------------------------- surrogates


def surrogate_index(S_obs, Y_obs, S_exp, t_exp) -> dict:
    """Athey, Chetty, Imbens & Kang's surrogate index: regress the long-term outcome on the surrogates in an
    observational sample, predict it in the experiment, and difference the predictions between arms."""
    S_obs, S_exp = np.atleast_2d(np.asarray(S_obs, float).T).T, np.atleast_2d(np.asarray(S_exp, float).T).T
    n = len(Y_obs)
    D = np.column_stack([np.ones(n), S_obs])
    b = np.linalg.lstsq(D, Y_obs, rcond=None)[0]
    pred = np.column_stack([np.ones(len(S_exp)), S_exp]) @ b
    t = np.asarray(t_exp, int)
    est = float(pred[t == 1].mean() - pred[t == 0].mean())
    se = float(math.sqrt(pred[t == 1].var(ddof=1) / (t == 1).sum() + pred[t == 0].var(ddof=1) / (t == 0).sum()))
    return {"effect": est, "se": se, "b": b}
