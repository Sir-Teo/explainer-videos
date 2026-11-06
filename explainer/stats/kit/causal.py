"""statkit.causal (I): randomized experiments in the potential-outcomes framework (Part 35 of *Statistics, Built*).

Design-based inference for a finite population of n units with potential outcomes y0, y1, of which a completely
randomized (or blocked, paired, clustered) assignment z reveals one each:

* Neyman (1923): the difference in means, its exact variance S1^2/n1 + S0^2/n0 - S_tau^2/n, and the conservative
  estimate that drops the last term;
* Fisher (1935): the randomization test of the sharp null, exact by enumeration or by Monte Carlo, and its inversion
  into an interval for a constant effect;
* blocked and paired estimators; regression adjustment as Freedman (2008) criticized it and Lin (2013) repaired it
  (the fully interacted regression with HC2 standard errors);
* cluster-randomized trials: cluster-level and cluster-robust analyses, the design effect;
* noncompliance: intention to treat, the Wald / IV estimator of the complier effect (Imbens & Angrist 1994; Angrist,
  Imbens & Rubin 1996) with its delta-method SE;
* interference: Hudgens & Halloran's (2008) direct, indirect, total and overall effects under two-stage randomization;
* group-sequential designs: Pocock (1977) and O'Brien & Fleming (1979) boundaries and Lan & DeMets (1983) alpha
  spending, by numerical integration of the partial-sum density (Armitage, McPherson & Rowe 1969);
* surrogates: Prentice's (1989) criteria; transporting a trial's effect to a target population by inverse odds of
  participation weighting (Stuart et al. 2011; Dahabreh et al. 2019).

Checked in ``tests/test_stats_kit_causal.py``.
"""

from __future__ import annotations

import itertools
import math

import numpy as np
from scipy import stats

# --------------------------------------------------------------------------------------------- Neyman and Fisher


def diff_means(y, z, alpha: float = 0.1) -> dict:
    """Neyman's estimator and conservative variance s1^2/n1 + s0^2/n0, with a normal interval."""
    y, z = np.asarray(y, float), np.asarray(z, bool)
    y1, y0 = y[z], y[~z]
    est = y1.mean() - y0.mean()
    se = math.sqrt(y1.var(ddof=1) / len(y1) + y0.var(ddof=1) / len(y0))
    q = stats.norm.ppf(1 - alpha / 2)
    return {"est": float(est), "se": float(se), "lo": float(est - q * se), "hi": float(est + q * se)}


def neyman_true_var(y0, y1, n1: int) -> dict:
    """The exact randomization variance of the difference in means under complete randomization with n1 treated:
    S1^2/n1 + S0^2/n0 - S_tau^2/n (finite-population variances with divisor n - 1), and the expectation of the
    conservative estimator, S1^2/n1 + S0^2/n0."""
    y0, y1 = np.asarray(y0, float), np.asarray(y1, float)
    n = len(y0)
    n0 = n - n1
    s1, s0, st = y1.var(ddof=1), y0.var(ddof=1), (y1 - y0).var(ddof=1)
    return {"true": float(s1 / n1 + s0 / n0 - st / n), "conservative": float(s1 / n1 + s0 / n0),
            "S_tau2": float(st), "ate": float((y1 - y0).mean())}


def complete_assignments(n: int, n1: int, rng=None, reps: int | None = None):
    """All C(n, n1) assignments (as boolean arrays) if ``reps`` is None, else ``reps`` random ones."""
    if reps is None:
        for c in itertools.combinations(range(n), n1):
            z = np.zeros(n, bool)
            z[list(c)] = True
            yield z
    else:
        rng = rng or np.random.default_rng(0)
        for _ in range(reps):
            z = np.zeros(n, bool)
            z[rng.choice(n, n1, replace=False)] = True
            yield z


def fisher_test(y, z, stat=None, reps: int | None = None, rng=None, tau0: float = 0.0) -> dict:
    """Fisher's randomization test of the sharp null Y_i(1) - Y_i(0) = tau0 for every unit: impute both potential
    outcomes, re-randomize, and compare |stat|.  Exact (all assignments) if ``reps`` is None."""
    y, z = np.asarray(y, float), np.asarray(z, bool)
    stat = stat or (lambda yy, zz: yy[zz].mean() - yy[~zz].mean())
    y0 = y - tau0 * z
    obs = stat(y, z) - tau0
    dist = []
    for zz in complete_assignments(len(y), int(z.sum()), rng, reps):
        dist.append(stat(y0 + tau0 * zz, zz) - tau0)
    dist = np.array(dist)
    p = float(np.mean(np.abs(dist) >= abs(obs) - 1e-12))
    if reps is not None:
        p = float((1 + np.sum(np.abs(dist) >= abs(obs) - 1e-12)) / (1 + len(dist)))
    return {"obs": float(obs), "p": p, "dist": dist}


def fisher_ci(y, z, grid, reps: int = 2000, alpha: float = 0.1, rng=None) -> dict:
    """Invert the sharp-null test over a grid of constant effects: the set of tau0 with p > alpha."""
    rng = rng or np.random.default_rng(0)
    keep = [t for t in grid if fisher_test(y, z, reps=reps, rng=np.random.default_rng(rng.integers(1 << 30)), tau0=t)["p"] > alpha]
    return {"lo": float(min(keep)) if keep else np.nan, "hi": float(max(keep)) if keep else np.nan, "kept": keep}


# --------------------------------------------------------------------------------------------- blocks and pairs


def blocked(y, z, block, alpha: float = 0.1) -> dict:
    """Stratified difference in means: block estimates weighted by block size, variance sum w_b^2 V_b."""
    y, z, b = np.asarray(y, float), np.asarray(z, bool), np.asarray(block)
    n = len(y)
    est, var = 0.0, 0.0
    for k in np.unique(b):
        m = b == k
        r = diff_means(y[m], z[m])
        w = m.sum() / n
        est += w * r["est"]
        var += w ** 2 * r["se"] ** 2
    q = stats.norm.ppf(1 - alpha / 2)
    se = math.sqrt(var)
    return {"est": est, "se": se, "lo": est - q * se, "hi": est + q * se}


def paired(y, z, pair, alpha: float = 0.1) -> dict:
    """Matched pairs: the mean of within-pair differences, with variance s_d^2 / J (conservative)."""
    y, z, p = np.asarray(y, float), np.asarray(z, bool), np.asarray(pair)
    d = np.array([y[(p == k) & z][0] - y[(p == k) & ~z][0] for k in np.unique(p)])
    se = d.std(ddof=1) / math.sqrt(len(d))
    q = stats.norm.ppf(1 - alpha / 2)
    return {"est": float(d.mean()), "se": float(se), "lo": float(d.mean() - q * se), "hi": float(d.mean() + q * se),
            "d": d}


# --------------------------------------------------------------------------------------------- regression adjustment


def _hc(Xd, e, kind="HC2"):
    XtXi = np.linalg.inv(Xd.T @ Xd)
    if kind == "HC2":
        h = np.einsum("ij,jk,ik->i", Xd, XtXi, Xd)
        w = e ** 2 / (1 - h)
    else:
        w = e ** 2
    return XtXi @ (Xd * w[:, None]).T @ Xd @ XtXi


def ancova(y, z, X, alpha: float = 0.1) -> dict:
    """Freedman's (2008) object: OLS of y on 1, z and the covariates, with the conventional (homoskedastic) SE."""
    y, z, X = np.asarray(y, float), np.asarray(z, float), np.atleast_2d(np.asarray(X, float).T).T
    D = np.column_stack([np.ones(len(y)), z, X])
    b = np.linalg.lstsq(D, y, rcond=None)[0]
    e = y - D @ b
    s2 = e @ e / (len(y) - D.shape[1])
    V = s2 * np.linalg.inv(D.T @ D)
    se = math.sqrt(V[1, 1])
    q = stats.norm.ppf(1 - alpha / 2)
    return {"est": float(b[1]), "se": se, "lo": float(b[1] - q * se), "hi": float(b[1] + q * se)}


def lin(y, z, X, alpha: float = 0.1) -> dict:
    """Lin's (2013) estimator: OLS of y on 1, z, centred covariates and their interactions with z, with HC2
    standard errors; asymptotically never less efficient than the difference in means, and its SE is consistent or
    conservative."""
    y, z = np.asarray(y, float), np.asarray(z, float)
    X = np.atleast_2d(np.asarray(X, float).T).T
    Xc = X - X.mean(0)
    D = np.column_stack([np.ones(len(y)), z, Xc, Xc * z[:, None]])
    b = np.linalg.lstsq(D, y, rcond=None)[0]
    e = y - D @ b
    V = _hc(D, e, "HC2")
    se = math.sqrt(V[1, 1])
    q = stats.norm.ppf(1 - alpha / 2)
    return {"est": float(b[1]), "se": se, "lo": float(b[1] - q * se), "hi": float(b[1] + q * se)}


# --------------------------------------------------------------------------------------------- clusters


def cluster_diff(y, z_cluster, cluster, alpha: float = 0.1) -> dict:
    """A cluster-randomized trial: the difference in mean cluster means (each cluster one unit), and the naive
    individual-level difference in means with its (wrong) SE for comparison."""
    y, c = np.asarray(y, float), np.asarray(cluster)
    zc = np.asarray(z_cluster, bool)
    ks = np.unique(c)
    means = np.array([y[c == k].mean() for k in ks])
    zk = zc[ks]
    r = diff_means(means, zk, alpha)
    naive = diff_means(y, zc[c], alpha)
    return {"cluster": r, "naive": naive}


def design_effect(m_bar: float, icc: float) -> float:
    """Kish's design effect for equal clusters of size m: 1 + (m - 1) ICC."""
    return 1 + (m_bar - 1) * icc


# --------------------------------------------------------------------------------------------- noncompliance


def iv_late(y, z, d, alpha: float = 0.1) -> dict:
    """The Wald estimator ITT_Y / ITT_D of the complier average causal effect, with its delta-method SE (treating the
    two ITTs as estimated from independent arms)."""
    y, z, d = np.asarray(y, float), np.asarray(z, bool), np.asarray(d, float)
    ity = y[z].mean() - y[~z].mean()
    itd = d[z].mean() - d[~z].mean()
    late = ity / itd
    # residual of y - late d in each arm
    r = y - late * d
    var = (r[z].var(ddof=1) / z.sum() + r[~z].var(ddof=1) / (~z).sum()) / itd ** 2
    se = math.sqrt(var)
    q = stats.norm.ppf(1 - alpha / 2)
    return {"itt_y": float(ity), "itt_d": float(itd), "est": float(late), "se": se, "lo": float(late - q * se),
            "hi": float(late + q * se)}


# --------------------------------------------------------------------------------------------- interference


def two_stage(y, v, group, psi_group, psi_values=(0, 1)) -> dict:
    """Hudgens & Halloran (2008): groups randomized to strategy psi (a vaccination share), individuals randomized
    within.  Returns the group-averaged mean outcomes ybar(v, psi), and the direct effect at each psi
    (ybar(0, psi) - ybar(1, psi)), the indirect effect (ybar(0, psi0) - ybar(0, psi1)), the total effect
    (ybar(0, psi0) - ybar(1, psi1)) and the overall effect (ybar(psi0) - ybar(psi1)), with risk differences
    oriented so that protection is positive."""
    y, v, gr = np.asarray(y, float), np.asarray(v, bool), np.asarray(group)
    psi_group = np.asarray(psi_group)
    out = {}
    for k, ps in enumerate(psi_values):
        gs = np.flatnonzero(psi_group == ps)
        m1 = [y[(gr == j) & v].mean() for j in gs if np.any((gr == j) & v)]
        m0 = [y[(gr == j) & ~v].mean() for j in gs if np.any((gr == j) & ~v)]
        ma = [y[gr == j].mean() for j in gs]
        out[k] = {"y1": float(np.mean(m1)), "y0": float(np.mean(m0)), "all": float(np.mean(ma))}
    a, b = out[0], out[1]
    return {"means": out, "direct0": a["y0"] - a["y1"], "direct1": b["y0"] - b["y1"], "indirect": a["y0"] - b["y0"],
            "total": a["y0"] - b["y1"], "overall": a["all"] - b["all"]}


# --------------------------------------------------------------------------------------------- group-sequential


def crossing_probs(bounds, info=None, h: float = 0.01, drift: float = 0.0) -> np.ndarray:
    """P(first crossing |Z_k| >= c_k at look k), k = 1..K, for z-boundaries ``bounds`` at equally spaced looks (or
    information fractions ``info``).  Works on the Brownian scale B(t) = Z(t) sqrt(t), whose increments over dt are
    N(drift dt, dt): the density of B is propagated through the continuation region by convolution on a grid."""
    c = np.asarray(bounds, float)
    K = len(c)
    t = np.arange(1, K + 1) / K if info is None else np.asarray(info, float)
    L = 8.0 + 2 * abs(drift)
    s = np.arange(-L, L + h / 2, h)
    out = np.zeros(K)
    f = None
    tprev = 0.0
    for k in range(K):
        dt = t[k] - tprev
        if f is None:
            f = stats.norm.pdf(s, drift * dt, math.sqrt(dt)) * h
        else:
            half = int(np.ceil(7 * math.sqrt(dt) / h))
            kx = np.arange(-half, half + 1) * h
            ker = stats.norm.pdf(kx, drift * dt, math.sqrt(dt)) * h
            f = np.convolve(f, ker, mode="same")
        cross = np.abs(s) >= c[k] * math.sqrt(t[k])
        out[k] = float(f[cross].sum())
        f = np.where(cross, 0.0, f)
        tprev = t[k]
    return out


def pocock(K: int, alpha: float = 0.05) -> float:
    """Pocock's (1977) constant boundary c: P(any |Z_k| >= c, k = 1..K) = alpha (two-sided)."""
    from scipy.optimize import brentq

    return float(brentq(lambda c: crossing_probs([c] * K).sum() - alpha, 1.5, 4.0, xtol=1e-6))


def obrien_fleming(K: int, alpha: float = 0.05) -> np.ndarray:
    """O'Brien & Fleming's (1979) boundaries c_k = C sqrt(K / k)."""
    from scipy.optimize import brentq

    f = lambda C: crossing_probs([C * math.sqrt(K / k) for k in range(1, K + 1)]).sum() - alpha  # noqa: E731
    C = brentq(f, 1.5, 4.0, xtol=1e-6)
    return np.array([C * math.sqrt(K / k) for k in range(1, K + 1)])


def spending(t, alpha: float = 0.05, kind: str = "obf") -> np.ndarray:
    """Lan & DeMets (1983) two-sided spending functions: 'obf' 4 - 4 Phi(z_{1 - alpha/4} / sqrt t) (each side spends
    2 - 2 Phi(z_{1 - alpha/4} / sqrt t)); 'pocock' alpha log(1 + (e - 1) t).  Both equal alpha at t = 1."""
    t = np.asarray(t, float)
    if kind == "obf":
        return 4 - 4 * stats.norm.cdf(stats.norm.ppf(1 - alpha / 4) / np.sqrt(t))
    return alpha * np.log(1 + (math.e - 1) * t)


def spending_bounds(info, alpha: float = 0.05, kind: str = "obf") -> np.ndarray:
    """Boundaries at information fractions ``info`` spending alpha(t_k) - alpha(t_{k-1}) at look k."""
    from scipy.optimize import brentq

    info = np.asarray(info, float)
    a = spending(info, alpha, kind)
    inc = np.diff(np.r_[0.0, a])
    c = []
    for k in range(len(info)):
        f = lambda x: crossing_probs(c + [x], info[:k + 1])[-1] - inc[k]  # noqa: E731
        c.append(brentq(f, 0.5, 12.0, xtol=1e-6))
    return np.array(c)


def peeking_sim(K: int, reps: int, rng, bound=None, n_per_look: int = 50) -> float:
    """Monte Carlo: the share of null trials that ever cross |Z_k| >= bound (1.96 by default) at K equally spaced
    looks."""
    bound = np.full(K, 1.96) if bound is None else np.asarray(bound, float)
    x = rng.standard_normal((reps, K * n_per_look))
    hit = np.zeros(reps, bool)
    for k in range(1, K + 1):
        m = k * n_per_look
        z = x[:, :m].sum(1) / math.sqrt(m)
        hit |= np.abs(z) >= bound[k - 1]
    return float(hit.mean())


# --------------------------------------------------------------------------------------------- surrogates, transport


def prentice(y, s, z) -> dict:
    """Prentice's (1989) criteria for a surrogate S of outcome Y under treatment Z, checked by regressions: (1) Z
    affects S; (2) S predicts Y; (3) given S, Z no longer predicts Y.  Returns the coefficients and t-statistics."""
    y, s, z = (np.asarray(a, float) for a in (y, s, z))

    def ols(yy, cols):
        D = np.column_stack([np.ones(len(yy))] + cols)
        b = np.linalg.lstsq(D, yy, rcond=None)[0]
        e = yy - D @ b
        V = (e @ e / (len(yy) - D.shape[1])) * np.linalg.inv(D.T @ D)
        return b[1:], b[1:] / np.sqrt(np.diag(V)[1:])

    b1, t1 = ols(s, [z])
    b2, t2 = ols(y, [s])
    b3, t3 = ols(y, [s, z])
    return {"z_on_s": (float(b1[0]), float(t1[0])), "s_on_y": (float(b2[0]), float(t2[0])),
            "z_given_s": (float(b3[1]), float(t3[1]))}


def transport(y, z, X_trial, X_target, alpha: float = 0.1, ridge: float = 1e-6) -> dict:
    """Transport a trial's ATE to a target population (Westreich et al. 2017; Dahabreh et al. 2019): fit
    P(in trial | x) by logistic regression on the stacked trial and target covariates, weight trial units by the
    inverse odds (1 - p)/p, and take the weighted difference in means (Hajek)."""
    Xt, Xg = np.asarray(X_trial, float), np.asarray(X_target, float)
    X = np.vstack([Xt, Xg])
    s = np.r_[np.ones(len(Xt)), np.zeros(len(Xg))]
    mu, sd = X.mean(0), X.std(0) + 1e-12
    D = np.column_stack([np.ones(len(X)), (X - mu) / sd])
    w = np.zeros(D.shape[1])
    for _ in range(50):
        p = 1 / (1 + np.exp(-D @ w))
        g = D.T @ (s - p) - ridge * w
        H = D.T @ (D * (p * (1 - p))[:, None]) + ridge * np.eye(len(w))
        st = np.linalg.solve(H, g)
        w += st
        if np.max(np.abs(st)) < 1e-9:
            break
    pt = 1 / (1 + np.exp(-D[: len(Xt)] @ w))
    wt = (1 - pt) / pt
    y, z = np.asarray(y, float), np.asarray(z, bool)
    est = np.sum(wt[z] * y[z]) / wt[z].sum() - np.sum(wt[~z] * y[~z]) / wt[~z].sum()
    return {"est": float(est), "weights": wt, "ess": float(wt.sum() ** 2 / (wt ** 2).sum())}


# =============================================================================================== statkit.causal (II)
# Part 36: causes without experiments.  Graphs, propensity scores, weighting, double robustness, double machine
# learning, heterogeneous effects, sensitivity analysis, time-varying treatments.


class DAG:
    """A directed acyclic graph given as (parent, child) edges, with d-separation by the moralized ancestral graph
    (Lauritzen et al. 1990): X and Y are d-separated by Z iff they are disconnected in the moral graph of the
    ancestors of X, Y and Z after deleting Z."""

    def __init__(self, edges):
        self.edges = [tuple(e) for e in edges]
        self.nodes = sorted({v for e in self.edges for v in e})
        self.parents = {v: {a for a, b in self.edges if b == v} for v in self.nodes}
        self.children = {v: {b for a, b in self.edges if a == v} for v in self.nodes}

    def ancestors(self, S) -> set:
        out, stack = set(S), list(S)
        while stack:
            v = stack.pop()
            for p in self.parents.get(v, ()):
                if p not in out:
                    out.add(p)
                    stack.append(p)
        return out

    def descendants(self, v) -> set:
        out, stack = set(), [v]
        while stack:
            u = stack.pop()
            for c in self.children.get(u, ()):
                if c not in out:
                    out.add(c)
                    stack.append(c)
        return out

    def d_separated(self, X, Y, Z=()) -> bool:
        X, Y, Z = set(X), set(Y), set(Z)
        A = self.ancestors(X | Y | Z)
        nbr = {v: set() for v in A}
        for a, b in self.edges:
            if a in A and b in A:
                nbr[a].add(b)
                nbr[b].add(a)
        for v in A:  # marry parents
            ps = [p for p in self.parents[v] if p in A]
            for i in range(len(ps)):
                for j in range(i + 1, len(ps)):
                    nbr[ps[i]].add(ps[j])
                    nbr[ps[j]].add(ps[i])
        seen, stack = set(X), list(X)
        while stack:
            v = stack.pop()
            for u in nbr[v]:
                if u in Z or u in seen:
                    continue
                if u in Y:
                    return False
                seen.add(u)
                stack.append(u)
        return True

    def paths(self, x, y) -> list:
        """All simple paths between x and y, ignoring direction, as lists of nodes."""
        und = {v: self.parents[v] | self.children[v] for v in self.nodes}
        out = []

        def walk(p):
            v = p[-1]
            if v == y:
                out.append(list(p))
                return
            for u in und[v]:
                if u not in p:
                    walk(p + [u])

        walk([x])
        return out

    def is_open(self, path, Z=()) -> bool:
        """Whether a path is d-connecting given Z: every collider on it is in Z or has a descendant in Z, and no
        non-collider is in Z."""
        Z = set(Z)
        for i in range(1, len(path) - 1):
            a, v, b = path[i - 1], path[i], path[i + 1]
            collider = (a in self.parents[v]) and (b in self.parents[v])
            if collider:
                if v not in Z and not (self.descendants(v) & Z):
                    return False
            elif v in Z:
                return False
        return True

    def backdoor_ok(self, t, y, Z) -> bool:
        """Pearl's back-door criterion: no element of Z descends from t, and Z blocks every path from t to y that
        starts with an arrow into t."""
        Z = set(Z)
        if Z & self.descendants(t):
            return False
        for p in self.paths(t, y):
            if len(p) > 1 and p[1] in self.parents[t] and self.is_open(p, Z):
                return False
        return True


def logit_fit(X, y, ridge: float = 1e-6, iters: int = 100) -> np.ndarray:
    """Logistic regression by Newton's method with an intercept (and a tiny ridge for separation); returns the
    coefficient vector [intercept, slopes]."""
    X = np.column_stack([np.ones(len(X)), np.asarray(X, float)])
    y = np.asarray(y, float)
    w = np.zeros(X.shape[1])
    pen = ridge * np.r_[0, np.ones(X.shape[1] - 1)]
    for _ in range(iters):
        z = np.clip(X @ w, -35, 35)
        p = 1 / (1 + np.exp(-z))
        g = X.T @ (y - p) - pen * w
        H = X.T @ (X * (p * (1 - p))[:, None]) + np.diag(pen)
        step = np.linalg.solve(H, g)
        w += step
        if np.max(np.abs(step)) < 1e-9:
            break
    return w


def logit_predict(w, X) -> np.ndarray:
    z = np.column_stack([np.ones(len(X)), np.asarray(X, float)]) @ w
    return 1 / (1 + np.exp(-np.clip(z, -35, 35)))


def propensity(X, t, ridge: float = 1e-6) -> np.ndarray:
    return logit_predict(logit_fit(X, t, ridge), X)


def smd(x, t, w=None) -> float:
    """Standardized mean difference of covariate x between treated and controls (pooled-SD denominator from the
    unweighted groups), optionally weighted."""
    x, t = np.asarray(x, float), np.asarray(t, bool)
    w = np.ones(len(x)) if w is None else np.asarray(w, float)
    m1 = np.sum(w[t] * x[t]) / w[t].sum()
    m0 = np.sum(w[~t] * x[~t]) / w[~t].sum()
    s = math.sqrt((x[t].var(ddof=1) + x[~t].var(ddof=1)) / 2)
    return float((m1 - m0) / s) if s > 0 else 0.0


def g_computation(y, t, X, estimand: str = "ate") -> float:
    """Robins's g-formula with linear outcome models fitted separately in each arm (the T-learner with OLS)."""
    y, t = np.asarray(y, float), np.asarray(t, bool)
    D = np.column_stack([np.ones(len(y)), np.asarray(X, float)])
    b1 = np.linalg.lstsq(D[t], y[t], rcond=None)[0]
    b0 = np.linalg.lstsq(D[~t], y[~t], rcond=None)[0]
    d = D @ b1 - D @ b0
    return float(d[t].mean() if estimand == "att" else d.mean())


def ps_match(y, t, ps, caliper: float | None = None) -> dict:
    """One-to-one nearest-neighbour matching on the propensity score, with replacement, for the ATT; matches farther
    than ``caliper`` (in PS units) are dropped.  SE from the matched differences (ignores the reuse of controls)."""
    y, t, ps = np.asarray(y, float), np.asarray(t, bool), np.asarray(ps, float)
    it, ic = np.flatnonzero(t), np.flatnonzero(~t)
    o = np.argsort(ps[ic])
    sc = ps[ic][o]
    pos = np.clip(np.searchsorted(sc, ps[it]), 1, len(sc) - 1)
    left, right = sc[pos - 1], sc[pos]
    j = np.where(np.abs(ps[it] - left) <= np.abs(ps[it] - right), pos - 1, pos)
    dist = np.abs(ps[it] - sc[j])
    keep = np.ones(len(it), bool) if caliper is None else dist <= caliper
    d = y[it][keep] - y[ic][o][j][keep]
    se = d.std(ddof=1) / math.sqrt(len(d))
    return {"est": float(d.mean()), "se": float(se), "n_matched": int(keep.sum()), "controls_used": int(len(np.unique(j[keep]))),
            "matched_controls": ic[o][j][keep]}


def subclassify(y, t, ps, k: int = 5, estimand: str = "ate") -> dict:
    """Cochran's (1968) subclassification on propensity-score quantiles: within-stratum differences averaged with
    stratum weights (all units for the ATE, treated units for the ATT)."""
    y, t, ps = np.asarray(y, float), np.asarray(t, bool), np.asarray(ps, float)
    edges = np.quantile(ps, np.linspace(0, 1, k + 1))
    s = np.clip(np.searchsorted(edges, ps, side="right") - 1, 0, k - 1)
    est, wsum, parts = 0.0, 0.0, []
    for b in range(k):
        m = s == b
        if (m & t).sum() == 0 or (m & ~t).sum() == 0:
            continue
        dlt = y[m & t].mean() - y[m & ~t].mean()
        w = (m & t).sum() if estimand == "att" else m.sum()
        est += w * dlt
        wsum += w
        parts.append(float(dlt))
    return {"est": float(est / wsum), "strata": parts}


def ipw(y, t, ps, estimand: str = "ate", normalize: bool = True, alpha: float = 0.1) -> dict:
    """Inverse probability weighting: Horvitz-Thompson (normalize=False) or Hajek (normalized) estimates of the ATE
    or ATT, with an influence-function SE that treats the propensity scores as known (conservative when they were
    estimated by maximum likelihood; Lunceford & Davidian 2004)."""
    y, t, e = np.asarray(y, float), np.asarray(t, float), np.asarray(ps, float)
    n = len(y)
    if estimand == "att":
        w1, w0 = t, (1 - t) * e / (1 - e)
    else:
        w1, w0 = t / e, (1 - t) / (1 - e)
    if normalize:
        m1, m0 = np.sum(w1 * y) / w1.sum(), np.sum(w0 * y) / w0.sum()
        phi = w1 * (y - m1) / w1.mean() - w0 * (y - m0) / w0.mean()
    else:
        d = t.mean() if estimand == "att" else 1.0
        m1, m0 = np.sum(w1 * y) / n / d, np.sum(w0 * y) / n / d
        phi = (w1 * y - w0 * y) / d - (m1 - m0)
    est = m1 - m0
    se = math.sqrt(np.var(phi, ddof=1) / n)
    q = stats.norm.ppf(1 - alpha / 2)
    return {"est": float(est), "se": float(se), "lo": float(est - q * se), "hi": float(est + q * se),
            "max_weight": float(max(w1.max(), w0.max())), "ess1": float(w1.sum() ** 2 / (w1 ** 2).sum()),
            "ess0": float(w0.sum() ** 2 / (w0 ** 2).sum())}


def aipw(y, t, mu0, mu1, ps, alpha: float = 0.1) -> dict:
    """The augmented IPW (doubly robust) estimator of the ATE (Robins, Rotnitzky & Zhao 1994), with its
    influence-function SE: consistent if either the outcome models (mu0, mu1) or the propensity score is right."""
    y, t, e = np.asarray(y, float), np.asarray(t, float), np.asarray(ps, float)
    mu0, mu1 = np.asarray(mu0, float), np.asarray(mu1, float)
    psi = mu1 - mu0 + t * (y - mu1) / e - (1 - t) * (y - mu0) / (1 - e)
    est = psi.mean()
    se = psi.std(ddof=1) / math.sqrt(len(y))
    q = stats.norm.ppf(1 - alpha / 2)
    return {"est": float(est), "se": float(se), "lo": float(est - q * se), "hi": float(est + q * se), "psi": psi}


def dml_ate(y, t, X, fit_reg, fit_prob, K: int = 2, rng=None, clip: float = 0.01, alpha: float = 0.1) -> dict:
    """Double/debiased machine learning (Chernozhukov et al. 2018) for the ATE in the interactive model: K-fold
    cross-fitting of the outcome regressions (``fit_reg(Xtr, ytr, Xte)``) and the propensity (``fit_prob(Xtr, ttr,
    Xte)``), plugged into the AIPW score."""
    y, t, X = np.asarray(y, float), np.asarray(t, bool), np.asarray(X, float)
    n = len(y)
    rng = rng or np.random.default_rng(0)
    folds = rng.permutation(np.arange(n) % K)
    mu0, mu1, e = np.zeros(n), np.zeros(n), np.zeros(n)
    for k in range(K):
        te, tr = folds == k, folds != k
        mu1[te] = fit_reg(X[tr & t], y[tr & t], X[te])
        mu0[te] = fit_reg(X[tr & ~t], y[tr & ~t], X[te])
        e[te] = fit_prob(X[tr], t[tr].astype(float), X[te])
    e = np.clip(e, clip, 1 - clip)
    r = aipw(y, t, mu0, mu1, e, alpha)
    r.update({"mu0": mu0, "mu1": mu1, "ps": e})
    return r


def dml_plr(y, t, X, fit_reg, K: int = 2, rng=None, alpha: float = 0.1) -> dict:
    """The partially linear model y = theta t + g(X) + e by Robinson's residual-on-residual regression with
    cross-fitted nuisance functions (Chernozhukov et al. 2018, the 'DML2' estimator)."""
    y, t, X = np.asarray(y, float), np.asarray(t, float), np.asarray(X, float)
    n = len(y)
    rng = rng or np.random.default_rng(0)
    folds = rng.permutation(np.arange(n) % K)
    ry, rt = np.zeros(n), np.zeros(n)
    for k in range(K):
        te, tr = folds == k, folds != k
        ry[te] = y[te] - fit_reg(X[tr], y[tr], X[te])
        rt[te] = t[te] - fit_reg(X[tr], t[tr], X[te])
    th = float(np.sum(rt * ry) / np.sum(rt * rt))
    psi = (ry - th * rt) * rt
    se = math.sqrt(np.mean(psi ** 2) / np.mean(rt * rt) ** 2 / n)
    q = stats.norm.ppf(1 - alpha / 2)
    return {"est": th, "se": se, "lo": th - q * se, "hi": th + q * se}


# --------------------------------------------------------------------------------------------- heterogeneous effects


def t_learner(X, y, t, Xte, fit_reg):
    t = np.asarray(t, bool)
    return fit_reg(X[t], y[t], Xte) - fit_reg(X[~t], y[~t], Xte)


def s_learner(X, y, t, Xte, fit_reg):
    Xa = np.column_stack([X, np.asarray(t, float)])
    return fit_reg(Xa, y, np.column_stack([Xte, np.ones(len(Xte))])) - fit_reg(Xa, y, np.column_stack([Xte, np.zeros(len(Xte))]))


def x_learner(X, y, t, Xte, fit_reg, ps: float | np.ndarray = 0.5):
    """Kunzel, Sekhon, Bickel & Yu (2019): impute each unit's effect with the other arm's model, regress the imputed
    effects on X in each arm, and blend with the propensity score."""
    t = np.asarray(t, bool)
    d1 = y[t] - fit_reg(X[~t], y[~t], X[t])
    d0 = fit_reg(X[t], y[t], X[~t]) - y[~t]
    t1 = fit_reg(X[t], d1, Xte)
    t0 = fit_reg(X[~t], d0, Xte)
    g = np.broadcast_to(np.asarray(ps, float), (len(Xte),))
    return g * t0 + (1 - g) * t1


def dr_learner(X, y, t, Xte, fit_reg, ps: float | np.ndarray = 0.5, K: int = 2, rng=None):
    """Kennedy's (2023) DR-learner: regress cross-fitted AIPW pseudo-outcomes on X."""
    t = np.asarray(t, bool)
    n = len(y)
    rng = rng or np.random.default_rng(0)
    folds = rng.permutation(np.arange(n) % K)
    mu0, mu1 = np.zeros(n), np.zeros(n)
    for k in range(K):
        te, tr = folds == k, folds != k
        mu1[te] = fit_reg(X[tr & t], y[tr & t], X[te])
        mu0[te] = fit_reg(X[tr & ~t], y[tr & ~t], X[te])
    e = np.broadcast_to(np.asarray(ps, float), (n,))
    psi = mu1 - mu0 + t * (y - mu1) / e - (~t) * (y - mu0) / (1 - e)
    return fit_reg(X, psi, Xte)


class CausalForest:
    """A causal forest in the spirit of Wager & Athey (2018) and Athey, Tibshirani & Wager's (2019) generalized
    random forest: outcomes and treatments are first centred by out-of-bag regression forests (local centring);
    each tree, on a half-sample, chooses splits on one half to maximize n_L n_R / n^2 (tau_L - tau_R)^2, where tau in
    a node is the residual-on-residual slope sum(w y) / sum(w^2), and estimates leaf effects on the other half
    (honesty).  Predictions average the trees' leaf effects."""

    def __init__(self, X, y, t, B: int = 200, min_leaf: int = 20, mtry: int | None = None, rng=None, max_depth: int = 12,
                 centre: bool = True):
        from explainer.stats.kit import conformal as CF

        X, y, t = np.asarray(X, float), np.asarray(y, float), np.asarray(t, float)
        n, p = X.shape
        rng = rng or np.random.default_rng(0)
        if centre:
            fy = CF.Forest(X, y, B=100, min_leaf=5, rng=rng)
            ft = CF.Forest(X, t, B=100, min_leaf=5, rng=rng)
            my, mt = fy.oob(), ft.oob()
            my = np.where(np.isnan(my), y.mean(), my)
            mt = np.where(np.isnan(mt), t.mean(), mt)
        else:
            my, mt = np.full(n, y.mean()), np.full(n, t.mean())
        self.ry, self.rt = y - my, t - mt
        self.mtry = mtry or max(1, int(math.ceil(p / 2)))
        self.min_leaf, self.max_depth = min_leaf, max_depth
        self.trees = []
        for _ in range(B):
            s = rng.choice(n, n // 2, replace=False)
            h = len(s) // 2
            self.trees.append(self._grow(X, s[:h], s[h:], rng))

    def _tau(self, idx):
        w, r = self.rt[idx], self.ry[idx]
        d = np.sum(w * w)
        return float(np.sum(w * r) / d) if d > 1e-9 else 0.0

    def _grow(self, X, split_idx, est_idx, rng):
        nodes = []  # (feature, threshold, left, right, value)

        def build(si, ei, depth):
            k = len(nodes)
            nodes.append([-1, 0.0, -1, -1, self._tau(ei) if len(ei) else 0.0])
            if depth >= self.max_depth or len(si) < 2 * self.min_leaf or len(ei) < 2 * self.min_leaf:
                return k
            best = (0.0, -1, 0.0)
            feats = rng.choice(X.shape[1], self.mtry, replace=False)
            w, r = self.rt[si], self.ry[si]
            m = len(si)
            for j in feats:
                xj = X[si, j]
                o = np.argsort(xj, kind="stable")
                xs, ww, wr = xj[o], (w * w)[o], (w * r)[o]
                cw, cr = np.cumsum(ww), np.cumsum(wr)
                kk = np.arange(1, m)
                ok = (kk >= self.min_leaf) & (m - kk >= self.min_leaf) & (xs[:-1] < xs[1:])
                if not ok.any():
                    continue
                tl = cr[:-1] / np.maximum(cw[:-1], 1e-9)
                tr = (cr[-1] - cr[:-1]) / np.maximum(cw[-1] - cw[:-1], 1e-9)
                crit = np.where(ok, kk * (m - kk) / m ** 2 * (tl - tr) ** 2, -np.inf)
                i = int(np.argmax(crit))
                if crit[i] > best[0]:
                    best = (float(crit[i]), int(j), float((xs[i] + xs[i + 1]) / 2))
            if best[1] < 0:
                return k
            _, j, thr = best
            ls, rs = si[X[si, j] <= thr], si[X[si, j] > thr]
            le, re = ei[X[ei, j] <= thr], ei[X[ei, j] > thr]
            if len(le) < self.min_leaf // 2 or len(re) < self.min_leaf // 2:
                return k
            nodes[k][0], nodes[k][1] = j, thr
            nodes[k][2] = build(ls, le, depth + 1)
            nodes[k][3] = build(rs, re, depth + 1)
            return k

        build(np.asarray(split_idx), np.asarray(est_idx), 0)
        return np.array(nodes, dtype=float)

    def predict(self, X) -> np.ndarray:
        X = np.asarray(X, float)
        out = np.zeros(len(X))
        for T in self.trees:
            node = np.zeros(len(X), int)
            for _ in range(self.max_depth + 1):
                f = T[node, 0].astype(int)
                inner = f >= 0
                if not inner.any():
                    break
                idx = np.flatnonzero(inner)
                go = X[idx, f[idx]] <= T[node[idx], 1]
                node[idx] = np.where(go, T[node[idx], 2], T[node[idx], 3]).astype(int)
            out += T[node, 4]
        return out / len(self.trees)


# --------------------------------------------------------------------------------------------- sensitivity


def e_value(rr: float) -> float:
    """VanderWeele & Ding (2017): the minimum strength of association (risk-ratio scale) an unmeasured confounder
    would need with both treatment and outcome to explain away an observed risk ratio rr."""
    rr = rr if rr >= 1 else 1 / rr
    return float(rr + math.sqrt(rr * (rr - 1)))


def robustness_value(t_stat: float, dof: int, q: float = 1.0, alpha: float | None = None) -> float:
    """Cinelli & Hazlett (2020): the partial R^2 an unmeasured confounder would need with both treatment and outcome
    to reduce the estimate by 100q% (or, with ``alpha``, to make it insignificant)."""
    f = q * abs(t_stat) / math.sqrt(dof)
    if alpha is not None:
        f = q * abs(t_stat) / math.sqrt(dof) - stats.t.ppf(1 - alpha / 2, dof - 1) / math.sqrt(dof - 1)
        if f < 0:
            return 0.0
    return float(0.5 * (math.sqrt(f ** 4 + 4 * f ** 2) - f ** 2))


def partial_r2(t_stat: float, dof: int) -> float:
    return float(t_stat ** 2 / (t_stat ** 2 + dof))


def rosenbaum_bound(d, gamma: float) -> float:
    """Rosenbaum's (2002) sensitivity analysis for matched pairs with Wilcoxon's signed-rank statistic: the largest
    one-sided p-value consistent with hidden bias of at most Gamma (each pair's odds of treatment within [1/Gamma,
    Gamma]), by the normal approximation."""
    d = np.asarray(d, float)
    d = d[d != 0]
    r = stats.rankdata(np.abs(d))
    T = float(r[d > 0].sum())
    p = gamma / (1 + gamma)
    mu = p * r.sum()
    var = p * (1 - p) * np.sum(r ** 2)
    return float(stats.norm.sf((T - mu) / math.sqrt(var)))


def cornfield_ratio(rr: float) -> float:
    """Cornfield et al. (1959): a binary confounder that fully explains an observed risk ratio rr must be at least
    rr times as prevalent among the exposed as among the unexposed."""
    return float(rr)


def stabilized_weights(a, p_a_given_past, p_a_marginal) -> np.ndarray:
    """Stabilized inverse probability of treatment weights for a marginal structural model (Robins, Hernan &
    Brumback 2000): prod_t P(A_t | A_{t-1}) / P(A_t | A_{t-1}, L_t), given the per-period probabilities of the
    treatment actually received (arrays of shape n x T)."""
    return np.prod(np.asarray(p_a_marginal, float) / np.asarray(p_a_given_past, float), axis=1)
