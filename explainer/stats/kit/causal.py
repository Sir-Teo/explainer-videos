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
