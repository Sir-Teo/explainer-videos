"""Psyche's latent-variable models (Part 44): path analysis, confirmatory factor analysis and structural equation
models by maximum likelihood, their fit, measurement invariance, and the models that fit equally.

* :func:`path_implied`: Wright's path model, Sigma = (I - B)^-1 Psi (I - B)^-T, for a matrix of direct effects B
  (B[i, j] is the arrow from j to i) and the covariance Psi of the disturbances.  For standardized recursive models
  this is Wright's tracing rule: a correlation is the sum over the paths that link two variables.
* :func:`cfa_implied`: Sigma = Lambda Phi Lambda^T + Theta.
* :func:`fit_cfa`: a confirmatory factor model by maximum likelihood.  ``pattern`` (p x m, 0/1) says which
  loadings are free; each factor's first indicator is fixed at 1 (the marker-variable scaling), factor variances and
  covariances are free (or ``phi_free`` says which), residuals are uncorrelated.  The discrepancy
  F = log|Sigma| + tr(S Sigma^-1) - log|S| - p is minimized from S with divisor n, and T = n F is the chi-square
  test on p(p + 1)/2 - q degrees of freedom.  Returns the estimates, T, df, p and RMSEA, CFI, TLI and SRMR against
  the independence model.
* :func:`fit_multigroup`: the same model in several groups at once, with loadings (metric) and intercepts (scalar)
  optionally held equal: the invariance ladder.
* :func:`markov_equivalent`: three diagrams for three variables (a chain each way and a fork) and their implied
  covariances, which are identical, and the collider, which is not.
* :func:`factor_as_network`: the partial correlations implied by a one-factor model: a fully connected network that
  reproduces exactly the same covariance matrix.
* :func:`mediation`: a simulated randomized X, a mediator M and outcome Y, with an unmeasured confounder of M and Y;
  the product-of-coefficients indirect effect, its bootstrap interval, and the true one.

Everything is numpy and scipy; the fits are checked in the tests against lavaan's published results for Holzinger and
Swineford's data.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize, stats

__all__ = ["path_implied", "cfa_implied", "fit_cfa", "fit_multigroup", "markov_equivalent", "factor_as_network",
           "mediation", "ml_discrepancy"]


def path_implied(B, Psi) -> np.ndarray:
    B, Psi = np.asarray(B, float), np.asarray(Psi, float)
    A = np.linalg.inv(np.eye(len(B)) - B)
    return A @ Psi @ A.T


def cfa_implied(L, Phi, theta) -> np.ndarray:
    L = np.asarray(L, float)
    return L @ np.asarray(Phi, float) @ L.T + np.diag(np.asarray(theta, float))


def ml_discrepancy(S, Sigma) -> float:
    p = len(S)
    sign, logdet = np.linalg.slogdet(Sigma)
    if sign <= 0:
        return 1e10
    return float(logdet + np.trace(S @ np.linalg.inv(Sigma)) - np.linalg.slogdet(S)[1] - p)


class _Model:
    """Parameter bookkeeping for a CFA: free loadings (all but each factor's marker), Phi (lower triangle where
    free) and residual variances."""

    def __init__(self, pattern, phi_free=None):
        self.P = np.asarray(pattern, int)
        p, m = self.P.shape
        self.marker = [int(np.flatnonzero(self.P[:, k])[0]) for k in range(m)]
        self.lam_idx = [(i, k) for k in range(m) for i in range(p) if self.P[i, k] and i != self.marker[k]]
        free = np.ones((m, m), bool) if phi_free is None else np.asarray(phi_free, bool)
        self.phi_idx = [(i, j) for i in range(m) for j in range(i + 1) if free[i, j]]
        self.p, self.m = p, m

    @property
    def q(self):
        return len(self.lam_idx) + len(self.phi_idx) + self.p

    def unpack(self, x):
        L = np.zeros((self.p, self.m))
        for k, i in enumerate(self.marker):
            L[i, k] = 1.0
        o = 0
        for (i, k) in self.lam_idx:
            L[i, k] = x[o]
            o += 1
        Phi = np.zeros((self.m, self.m))
        for (i, j) in self.phi_idx:
            Phi[i, j] = Phi[j, i] = x[o]
            o += 1
        theta = x[o:o + self.p]
        return L, Phi, theta

    def start(self, S):
        x = [0.8] * len(self.lam_idx)
        for (i, j) in self.phi_idx:
            x.append(0.5 * S[self.marker[i], self.marker[i]] if i == j else 0.05)
        x += list(0.5 * np.diag(S))
        return np.array(x, float)


def _indices(T, df, T0, df0, n):
    rmsea = float(np.sqrt(max(T - df, 0.0) / (df * n))) if df > 0 else 0.0
    cfi = 1 - max(T - df, 0.0) / max(T0 - df0, T - df, 1e-12)
    tli = ((T0 / df0) - (T / df)) / ((T0 / df0) - 1) if df > 0 else 1.0
    return rmsea, float(cfi), float(tli)


def _srmr(S, Sigma) -> float:
    d = np.sqrt(np.diag(S))
    R = (S - Sigma) / np.outer(d, d)
    iu = np.tril_indices(len(S))
    return float(np.sqrt(np.mean(R[iu] ** 2)))


def fit_cfa(S, n: int, pattern, phi_free=None) -> dict:
    """Maximum-likelihood CFA from the covariance matrix S (divisor n) of n people."""
    S = np.asarray(S, float)
    mod = _Model(pattern, phi_free)
    f = lambda x: ml_discrepancy(S, cfa_implied(*mod.unpack(x)))  # noqa: E731
    bounds = [(None, None)] * (len(mod.lam_idx) + len(mod.phi_idx)) + [(1e-6, None)] * mod.p
    res = optimize.minimize(f, mod.start(S), method="L-BFGS-B", bounds=bounds,
                            options={"maxiter": 20000, "maxfun": 200000, "ftol": 1e-14, "gtol": 1e-10})
    L, Phi, theta = mod.unpack(res.x)
    Sigma = cfa_implied(L, Phi, theta)
    p = len(S)
    T = n * res.fun
    df = p * (p + 1) // 2 - mod.q
    T0 = n * ml_discrepancy(S, np.diag(np.diag(S)))
    df0 = p * (p - 1) // 2
    rmsea, cfi, tli = _indices(T, df, T0, df0, n)
    return {"L": L, "Phi": Phi, "theta": theta, "Sigma": Sigma, "T": float(T), "df": int(df),
            "p": float(stats.chi2.sf(T, df)) if df > 0 else 1.0, "rmsea": rmsea, "cfi": cfi, "tli": tli,
            "srmr": _srmr(S, Sigma), "T0": float(T0), "df0": int(df0), "F": float(res.fun)}


def fit_multigroup(groups, pattern, level: str = "configural") -> dict:
    """The CFA in several groups at once, with means.  ``groups`` is a list of data matrices (people x p).
    ``level``: "configural" (all free), "metric" (loadings equal) or "scalar" (loadings and intercepts equal, with
    the first group's factor means at 0 and the others free).  Returns T, df and the factor means of the later
    groups (scalar only)."""
    P = np.asarray(pattern, int)
    p, m = P.shape
    G = len(groups)
    Ss = [np.cov(X.T, bias=True) for X in groups]
    ms = [X.mean(0) for X in groups]
    ns = [len(X) for X in groups]
    mod = _Model(P)
    nl, nphi = len(mod.lam_idx), len(mod.phi_idx)
    share_l = level in ("metric", "scalar")
    share_tau = level == "scalar"

    def split(x):
        o = 0
        out = []
        lam_shared = x[o:o + nl] if share_l else None
        o += nl if share_l else 0
        tau_shared = x[o:o + p] if share_tau else None
        o += p if share_tau else 0
        for g in range(G):
            lam = lam_shared if share_l else x[o:o + nl]
            o += 0 if share_l else nl
            phi = x[o:o + nphi]
            o += nphi
            th = x[o:o + p]
            o += p
            if share_tau:
                tau = tau_shared
                if g == 0:
                    kappa = np.zeros(m)
                else:
                    kappa = x[o:o + m]
                    o += m
            else:
                tau = x[o:o + p]
                o += p
                kappa = np.zeros(m)
            out.append((np.concatenate([lam, phi, th]), tau, kappa))
        return out

    def f(x):
        tot = 0.0
        for g, (xg, tau, kappa) in enumerate(split(x)):
            L, Phi, theta = mod.unpack(xg)
            Sig = cfa_implied(L, Phi, theta)
            mu = tau + L @ kappa
            d = ms[g] - mu
            sign, logdet = np.linalg.slogdet(Sig)
            if sign <= 0:
                return 1e10
            Si = np.linalg.inv(Sig)
            Fg = logdet + np.trace(Ss[g] @ Si) - np.linalg.slogdet(Ss[g])[1] - p + d @ Si @ d
            tot += ns[g] * Fg
        return tot

    x0 = []
    st = mod.start(Ss[0])
    if share_l:
        x0 += list(st[:nl])
    if share_tau:
        x0 += list(ms[0])
    for g in range(G):
        stg = mod.start(Ss[g])
        if not share_l:
            x0 += list(stg[:nl])
        x0 += list(stg[nl:nl + nphi]) + list(stg[nl + nphi:])
        if share_tau:
            if g > 0:
                x0 += [0.0] * m
        else:
            x0 += list(ms[g])
    res = optimize.minimize(f, np.array(x0, float), method="L-BFGS-B",
                            options={"maxiter": 50000, "maxfun": 500000, "ftol": 1e-15, "gtol": 1e-10})
    q = len(x0)
    moments = G * (p * (p + 1) // 2 + p)
    out = {"T": float(res.fun), "df": int(moments - q), "level": level}
    if share_tau:
        out["kappa"] = [split(res.x)[g][2] for g in range(1, G)]
    out["p"] = float(stats.chi2.sf(out["T"], out["df"]))
    return out


def markov_equivalent(a: float = 0.5, b: float = 0.6) -> dict:
    """Standardized implied correlations of X -> M -> Y, Y -> M -> X, X <- M -> Y and the collider X -> M <- Y, with
    path coefficients chosen so that the first three imply the same matrix."""
    def std(S):
        d = np.sqrt(np.diag(S))
        return S / np.outer(d, d)

    chain = path_implied([[0, 0, 0], [a, 0, 0], [0, b, 0]], np.diag([1, 1 - a * a, 1 - b * b]))
    rev = path_implied([[0, a, 0], [0, 0, b], [0, 0, 0]], np.diag([1 - a * a, 1 - b * b, 1]))
    fork = path_implied([[0, a, 0], [0, 0, 0], [0, b, 0]], np.diag([1 - a * a, 1, 1 - b * b]))
    coll = path_implied([[0, 0, 0], [a, 0, b], [0, 0, 0]], np.diag([1, 1 - a * a - b * b, 1]))
    return {"chain": std(chain), "reverse": std(rev), "fork": std(fork), "collider": std(coll)}


def factor_as_network(loadings) -> dict:
    """A one-factor model with standardized loadings; its correlation matrix and the partial correlations of the
    Gaussian graphical model that reproduces it exactly (every pair connected)."""
    lam = np.asarray(loadings, float)
    R = np.outer(lam, lam)
    np.fill_diagonal(R, 1.0)
    K = np.linalg.inv(R)
    d = np.sqrt(np.diag(K))
    pc = -K / np.outer(d, d)
    np.fill_diagonal(pc, 1.0)
    back = np.linalg.inv(-pc * np.outer(d, d) + np.diag(2 * np.diag(K)))
    return {"R": R, "partial": pc, "reproduced": back}


def mediation(n: int = 500, a: float = 0.5, b: float = 0.0, c: float = 0.0, confound: float = 0.6, boots: int = 1000,
              seed: int = 0) -> dict:
    """X randomized (0/1); M = a X + confound U + e; Y = b M + c X + confound U + e, with U unmeasured.  The
    product-of-coefficients estimate a_hat * b_hat (b_hat from regressing Y on M and X), its percentile bootstrap
    interval, and the true indirect effect a * b."""
    rng = np.random.default_rng(seed)
    X = rng.integers(0, 2, n).astype(float)
    U = rng.normal(0, 1, n)
    M = a * X + confound * U + rng.normal(0, 1, n)
    Y = b * M + c * X + confound * U + rng.normal(0, 1, n)

    def est(idx):
        x, m, y = X[idx], M[idx], Y[idx]
        A = np.column_stack([np.ones(len(idx)), x])
        ah = np.linalg.lstsq(A, m, rcond=None)[0][1]
        Bm = np.column_stack([np.ones(len(idx)), m, x])
        bh = np.linalg.lstsq(Bm, y, rcond=None)[0][1]
        return ah * bh

    idx = np.arange(n)
    point = est(idx)
    bs = np.array([est(rng.integers(0, n, n)) for _ in range(boots)])
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return {"indirect": float(point), "lo": float(lo), "hi": float(hi), "true": a * b}
