"""statkit.multiple: many tests at once (Part 33 of *Statistics, Built*).

Family-wise error control (Bonferroni, Šidák, Holm, Hochberg, closed testing, Westfall--Young's permutation maxT); the
false discovery rate (Benjamini--Hochberg, Benjamini--Yekutieli, Storey's pi0 and q-values); Efron's empirical Bayes
(local fdr by Lindsey's method, the empirical null by central matching); the FDP's spread under dependence;
model-X Gaussian knockoffs with the knockoff+ filter; the false coverage rate (Benjamini & Yekutieli 2005); and the
research-practice side: Simmons, Nelson & Simonsohn's p-hacking simulator, Ioannidis's positive predictive value,
funnel plots, Egger's test, PET, and the p-curve.  Checked in ``tests/test_stats_kit_multiple.py`` (against
statsmodels' multipletests).
"""

from __future__ import annotations

import itertools
import math

import numpy as np
from scipy import stats

# ------------------------------------------------------------------------------------------------- adjusted p-values


def adjust(p, method: str = "bh") -> np.ndarray:
    """Adjusted p-values: 'bonferroni', 'sidak', 'holm', 'hochberg', 'bh', 'by'.  Reject H_i at level a iff
    adjusted p_i <= a."""
    p = np.asarray(p, float)
    m = len(p)
    o = np.argsort(p)
    ps = p[o]
    if method == "bonferroni":
        adj = np.minimum(1, m * ps)
    elif method == "sidak":
        adj = 1 - (1 - ps) ** m
    elif method == "holm":
        adj = np.minimum(1, np.maximum.accumulate((m - np.arange(m)) * ps))
    elif method == "hochberg":
        adj = np.minimum(1, np.minimum.accumulate(((m - np.arange(m)) * ps)[::-1])[::-1])
    elif method in ("bh", "by"):
        c = np.sum(1.0 / np.arange(1, m + 1)) if method == "by" else 1.0
        adj = np.minimum(1, np.minimum.accumulate((c * m / np.arange(1, m + 1) * ps)[::-1])[::-1])
    else:
        raise ValueError(method)
    out = np.empty(m)
    out[o] = adj
    return out


def bh(p, q: float = 0.1, by: bool = False) -> dict:
    """Benjamini & Hochberg (1995): reject the k smallest p-values, k = max{i : p_(i) <= q i / m} (with the
    Benjamini--Yekutieli factor sum 1/i if ``by``).  Returns the rejection mask, k and the threshold."""
    p = np.asarray(p, float)
    m = len(p)
    c = np.sum(1.0 / np.arange(1, m + 1)) if by else 1.0
    o = np.sort(p)
    ok = np.flatnonzero(o <= q * np.arange(1, m + 1) / (m * c))
    k = int(ok.max() + 1) if len(ok) else 0
    thr = q * k / (m * c) if k else 0.0
    return {"reject": p <= thr if k else np.zeros(m, bool), "k": k, "threshold": thr}


def closed_testing_bonferroni(p) -> np.ndarray:
    """Marcus, Peritz & Gabriel's (1976) closed testing with Bonferroni local tests, by brute force over all
    intersections (small m): H_i is rejected at level a iff every intersection containing i has min p <= a/|I|.
    Returns adjusted p-values, which equal Holm's."""
    p = np.asarray(p, float)
    m = len(p)
    adj = np.zeros(m)
    for i in range(m):
        worst = 0.0
        others = [j for j in range(m) if j != i]
        for r in range(m):
            for S in itertools.combinations(others, r):
                I = (i,) + S
                worst = max(worst, min(1.0, len(I) * min(p[list(I)])))
        adj[i] = worst
    return adj


def westfall_young(X, group, B: int = 1000, rng=None) -> dict:
    """Westfall & Young's (1993) step-down maxT: two-sample t statistics for each column of X, and adjusted
    p-values from the permutation distribution of the successive maxima, which respects the dependence."""
    X = np.asarray(X, float)
    g = np.asarray(group, bool)
    rng = rng or np.random.default_rng(0)

    def tstats(gg):
        a, b = X[gg], X[~gg]
        n1, n2 = len(a), len(b)
        s2 = (a.var(0, ddof=1) * (n1 - 1) + b.var(0, ddof=1) * (n2 - 1)) / (n1 + n2 - 2)
        return (a.mean(0) - b.mean(0)) / np.sqrt(s2 * (1 / n1 + 1 / n2))

    t = np.abs(tstats(g))
    o = np.argsort(-t)
    m = len(t)
    count = np.zeros(m)
    for _ in range(B):
        tb = np.abs(tstats(rng.permutation(g)))[o]
        mx = np.maximum.accumulate(tb[::-1])[::-1]
        count += mx >= t[o]
    adj_o = np.maximum.accumulate((count + 1) / (B + 1))
    adj = np.empty(m)
    adj[o] = adj_o
    return {"t": t, "adj": adj}


# ------------------------------------------------------------------------------------------------- adaptive FDR


def storey_pi0(p, lam: float = 0.5) -> float:
    """Storey's (2002) estimate of the null proportion: #{p > lam} / (m (1 - lam)), capped at 1."""
    p = np.asarray(p, float)
    return float(min(1.0, np.mean(p > lam) / (1 - lam)))


def qvalues(p, pi0: float | None = None) -> np.ndarray:
    """Storey's q-values: pi0 times the BH adjusted p-values."""
    pi0 = storey_pi0(p) if pi0 is None else pi0
    return pi0 * adjust(p, "bh")


# ------------------------------------------------------------------------------------------------- empirical Bayes


def locfdr(z, df: int = 7, bins: int = 90, null: str = "theoretical", center_width: float = 1.5) -> dict:
    """Efron's local false discovery rate fdr(z) = pi0 f0(z) / f(z).  The mixture density f is estimated by Lindsey's
    method (a Poisson regression of histogram counts on a degree-``df`` polynomial in z); f0 is N(0, 1)
    (``null='theoretical'``) or fitted by central matching (a quadratic in log f over |z - median| < center_width,
    ``null='empirical'``), which also estimates pi0."""
    z = np.asarray(z, float)
    N = len(z)
    lo, hi = min(float(z.min()) - 0.1, -4.5), max(float(z.max()) + 0.1, 4.5)
    edges = np.linspace(lo, hi, bins + 1)
    mids = (edges[:-1] + edges[1:]) / 2
    w = edges[1] - edges[0]
    counts = np.histogram(z, edges)[0].astype(float)
    s = (mids - mids.mean()) / mids.std()
    B = np.column_stack([s ** k for k in range(df + 1)])
    beta = np.zeros(df + 1)
    beta[0] = math.log(max(counts.mean(), 1e-3))
    for _ in range(100):
        eta = B @ beta
        mu = np.exp(eta)
        g = B.T @ (counts - mu)
        H = B.T @ (B * mu[:, None])
        step = np.linalg.solve(H + 1e-10 * np.eye(df + 1), g)
        beta += step
        if np.max(np.abs(step)) < 1e-10:
            break
    fhat = np.exp(B @ beta) / (N * w)
    if null == "empirical":
        c = np.abs(mids - np.median(z)) < center_width
        A = np.column_stack([np.ones(c.sum()), mids[c], mids[c] ** 2])
        coef = np.linalg.lstsq(A, np.log(fhat[c]), rcond=None)[0]
        s0 = math.sqrt(-1 / (2 * coef[2]))
        d0 = coef[1] * s0 ** 2
        logpi0 = coef[0] + d0 ** 2 / (2 * s0 ** 2) + math.log(math.sqrt(2 * math.pi) * s0)
        pi0 = min(1.0, math.exp(logpi0))
    else:
        d0, s0 = 0.0, 1.0
        c = np.abs(mids) < center_width
        pi0 = min(1.0, float(np.sum(fhat[c]) / np.sum(stats.norm.pdf(mids[c]))))
    f0 = stats.norm.pdf(mids, d0, s0)
    fdr_m = np.minimum(1.0, pi0 * f0 / fhat)
    return {"mids": mids, "counts": counts, "f": fhat, "f0": f0, "fdr": fdr_m, "pi0": pi0, "delta0": d0, "sigma0": s0,
            "fdr_at": lambda x: np.interp(x, mids, fdr_m), "width": w}


# ------------------------------------------------------------------------------------------------- the FDP's spread


def equicorrelated_z(m: int, rho: float, rng) -> np.ndarray:
    """m standard normals with common correlation rho >= 0: sqrt(rho) W + sqrt(1 - rho) e_i."""
    return math.sqrt(rho) * rng.standard_normal() + math.sqrt(1 - rho) * rng.standard_normal(m)


def fdp_sim(m: int, pi0: float, effect: float, rho: float, q: float, reps: int, rng, method: str = "bh") -> dict:
    """The false discovery proportion of BH (or BY) at level q over ``reps`` simulated families of one-sided z-tests:
    m0 = pi0 m nulls N(0, 1), the rest N(effect, 1), equicorrelated with rho."""
    m0 = int(round(pi0 * m))
    fdp, R, pw = [], [], []
    for _ in range(reps):
        z = equicorrelated_z(m, rho, rng)
        z[m0:] += effect
        p = stats.norm.sf(z)
        r = bh(p, q, by=(method == "by"))["reject"]
        V = int(r[:m0].sum())
        k = int(r.sum())
        fdp.append(V / max(k, 1))
        R.append(k)
        pw.append(r[m0:].mean() if m0 < m else 0.0)
    fdp = np.array(fdp)
    return {"fdp": fdp, "fdr": float(fdp.mean()), "R": np.array(R), "power": float(np.mean(pw)),
            "p_fdp_gt_2q": float(np.mean(fdp > 2 * q)), "p_zero": float(np.mean(np.array(R) == 0))}


# ------------------------------------------------------------------------------------------------- knockoffs


def gaussian_knockoffs(X, Sigma, rng) -> np.ndarray:
    """Model-X Gaussian knockoffs (Candès, Fan, Janson & Lv 2018) for rows of X ~ N(0, Sigma) with unit variances,
    equicorrelated: s = min(1, 2 lambda_min(Sigma)) (shrunk slightly for stability); X_tilde | X is normal with mean
    X - X Sigma^{-1} D and covariance 2D - D Sigma^{-1} D, D = s I."""
    X = np.asarray(X, float)
    S = np.asarray(Sigma, float)
    p = S.shape[0]
    s = min(1.0, 2 * float(np.linalg.eigvalsh(S).min())) * 0.999
    D = s * np.eye(p)
    Si = np.linalg.inv(S)
    mean = X - X @ Si @ D
    C = 2 * D - D @ Si @ D
    L = np.linalg.cholesky(C + 1e-10 * np.eye(p))
    return mean + rng.standard_normal(X.shape) @ L.T


def knockoff_threshold(W, q: float = 0.1, plus: bool = True) -> float:
    """The knockoff(+) threshold: the smallest t > 0 with (offset + #{W <= -t}) / max(1, #{W >= t}) <= q
    (Barber & Candès 2015), offset 1 for knockoff+."""
    W = np.asarray(W, float)
    ts = np.sort(np.abs(W[W != 0]))
    off = 1 if plus else 0
    for t in ts:
        if (off + np.sum(W <= -t)) / max(1, np.sum(W >= t)) <= q:
            return float(t)
    return float("inf")


def lasso_W(X, Xk, y, lam: float) -> np.ndarray:
    """The lasso coefficient-difference statistic W_j = |b_j| - |b_j~| from one lasso on [X, X_tilde]."""
    from explainer.stats.kit.sparse import lasso_cd

    Z = np.column_stack([X, Xk])
    Z = Z - Z.mean(0)
    b = lasso_cd(Z, y - y.mean(), lam)
    p = X.shape[1]
    return np.abs(b[:p]) - np.abs(b[p:])


# ------------------------------------------------------------------------------------------------- the FCR


def fcr_intervals(est, se, selected, alpha: float = 0.1) -> dict:
    """Benjamini & Yekutieli's (2005) FCR-adjusted intervals: for R selected of m, use level 1 - R alpha / m
    instead of 1 - alpha."""
    est, se, sel = np.asarray(est, float), np.asarray(se, float), np.asarray(selected, bool)
    m, R = len(est), int(sel.sum())
    a = alpha * max(R, 1) / m
    zq = stats.norm.ppf(1 - a / 2)
    return {"lo": est - zq * se, "hi": est + zq * se, "z": float(zq), "level": 1 - a}


# ------------------------------------------------------------------------------------------------- research practice


def _cond_p(y, cond, gender=None, interaction=False) -> list:
    """p-values for the condition effect (and the interaction) in y ~ condition [+ gender [+ condition:gender]]."""
    n = len(y)
    cols = [np.ones(n), cond]
    if gender is not None:
        cols.append(gender)
        if interaction:
            cols.append(cond * gender)
    X = np.column_stack(cols)
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    df = n - X.shape[1]
    V = (e @ e / df) * np.linalg.inv(X.T @ X)
    idx = [1] + ([3] if interaction else [])
    return [float(2 * stats.t.sf(abs(b[j] / math.sqrt(V[j, j])), df)) for j in idx]


def phack(reps: int, rng, n: int = 20, extra: int = 10, r: float = 0.5) -> dict:
    """Simmons, Nelson & Simonsohn's (2011) simulation of researcher degrees of freedom, with no true effect, in
    three conditions of ``n`` subjects (plus ``extra`` more each if the first look fails), two dependent variables
    correlated ``r``, and a gender covariate.  The strategies:
    A choose among DV1, DV2 and their mean; B add subjects if not yet significant; C control for gender, or for
    gender and its interaction with condition; D compare any two of the three conditions, or test the linear trend.
    Returns the false-positive rate (p < .05 for any analysis tried) of no flexibility, each strategy, and A+B+C and
    A+B+C+D (every combination of the choices)."""
    L = np.linalg.cholesky(np.array([[1, r], [r, 1]]))
    combos = {"none": dict(dv=[0], cov=[0], cmp=["ab"], stages=1), "A": dict(dv=[0, 1, 2], cov=[0], cmp=["ab"], stages=1),
              "B": dict(dv=[0], cov=[0], cmp=["ab"], stages=2), "C": dict(dv=[0], cov=[0, 1, 2], cmp=["ab"], stages=1),
              "D": dict(dv=[0], cov=[0], cmp=["ab", "ac", "bc", "trend"], stages=1),
              "ABC": dict(dv=[0, 1, 2], cov=[0, 1, 2], cmp=["ab"], stages=2),
              "ABCD": dict(dv=[0, 1, 2], cov=[0, 1, 2], cmp=["ab", "ac", "bc", "trend"], stages=2)}
    out = {k: 0 for k in combos}
    for _ in range(reps):
        Y = rng.standard_normal((3, n + extra, 2)) @ L.T
        G = rng.integers(0, 2, (3, n + extra)).astype(float)
        cache = {}

        def p_of(stage, dv, cov, cmp):
            key = (stage, dv, cov, cmp)
            if key not in cache:
                k = n if stage == 1 else n + extra
                vals = [Y[c, :k, 0] if dv == 0 else Y[c, :k, 1] if dv == 1 else Y[c, :k].mean(1) for c in range(3)]
                gens = [G[c, :k] for c in range(3)]
                if cmp == "trend":
                    yv, cond, gv = np.concatenate(vals), np.repeat([0.0, 1.0, 2.0], k), np.concatenate(gens)
                else:
                    i1, i2 = {"ab": (0, 1), "ac": (0, 2), "bc": (1, 2)}[cmp]
                    yv, cond, gv = np.r_[vals[i1], vals[i2]], np.r_[np.zeros(k), np.ones(k)], np.r_[gens[i1], gens[i2]]
                if cov == 0:
                    ps = _cond_p(yv, cond)
                elif cov == 1:
                    ps = _cond_p(yv, cond, gv)
                else:
                    ps = _cond_p(yv, cond, gv, interaction=True)
                cache[key] = min(ps)
            return cache[key]

        for name, c in combos.items():
            hit = False
            for stage in range(1, c["stages"] + 1):
                if any(p_of(stage, dv, cov, cmp) < 0.05 for dv in c["dv"] for cov in c["cov"] for cmp in c["cmp"]):
                    hit = True
                    break
            out[name] += hit
    return {k: v / reps for k, v in out.items()}


def ppv(prior: float, power: float, alpha: float = 0.05, bias: float = 0.0) -> float:
    """Ioannidis (2005): the share of claimed findings that are true, with R = prior/(1 - prior) the pre-study odds
    and u the share of analyses turned 'positive' by bias:
    PPV = ((1 - beta) R + u beta R) / (R + alpha - beta R + u - u alpha + u beta R)."""
    R = prior / (1 - prior)
    b = 1 - power
    u = bias
    return float(((1 - b) * R + u * b * R) / (R + alpha - b * R + u - u * alpha + u * b * R))


def egger(est, se) -> dict:
    """Egger's (1997) regression test for funnel asymmetry: regress est/se on 1/se; the intercept's t-test.  The
    slope (PET, Stanley & Doucouliagos) estimates the effect at infinite precision."""
    est, se = np.asarray(est, float), np.asarray(se, float)
    y, x = est / se, 1 / se
    X = np.column_stack([np.ones(len(x)), x])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    s2 = e @ e / (len(y) - 2)
    V = s2 * np.linalg.inv(X.T @ X)
    t = b[0] / math.sqrt(V[0, 0])
    return {"intercept": float(b[0]), "slope": float(b[1]), "p": float(2 * stats.t.sf(abs(t), len(y) - 2)),
            "slope_se": float(math.sqrt(V[1, 1]))}


def publication_sim(k: int, effect: float, rng, tau: float = 0.0, n_range=(10, 200), publish_p: float = 0.05,
                    publish_null: float = 0.1) -> dict:
    """k studies of a two-group difference with per-group sizes uniform on n_range; every significant (two-sided,
    in the positive direction) study is published, others with probability ``publish_null``."""
    n = rng.integers(n_range[0], n_range[1] + 1, k)
    se = np.sqrt(2 / n)
    theta = effect + tau * rng.standard_normal(k)
    est = theta + se * rng.standard_normal(k)
    p = 2 * stats.norm.sf(np.abs(est / se))
    pub = ((p < publish_p) & (est > 0)) | (rng.random(k) < publish_null)
    return {"est": est, "se": se, "p": p, "published": pub}


def pcurve_density(delta: float, n: int, grid) -> np.ndarray:
    """The density of significant two-sided p-values (p < .05) for a two-sample z-test with standardized effect
    delta and n per group, on ``grid`` in (0, .05): flat for delta = 0, right-skewed for real effects."""
    grid = np.asarray(grid, float)
    ncp = delta * math.sqrt(n / 2)
    zc = stats.norm.isf(grid / 2)
    dens = (stats.norm.pdf(zc - ncp) + stats.norm.pdf(zc + ncp)) / (2 * stats.norm.pdf(zc))
    power = stats.norm.sf(1.959964 - ncp) + stats.norm.cdf(-1.959964 - ncp)
    return dens / power
