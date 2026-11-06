"""statkit.multi: the classical multivariate toolkit (Part 31 of *Statistics, Built*).

Classical (Torgerson) MDS and Procrustes alignment; Wishart draws by Bartlett's decomposition; Hotelling's T^2 (one
and two samples) and MANOVA's four statistics; PCA by the SVD with biplot coordinates; maximum-likelihood factor
analysis with varimax rotation and the likelihood-ratio test; canonical correlation with Bartlett's test; Fisher's
LDA, QDA and their cross-validated error; k-means (Lloyd, k-means++) and Gaussian mixtures by EM with BIC; the
graphical lasso by block coordinate descent; and Bai & Saranadasa's high-dimensional two-sample test.  Checked in
``tests/test_stats_kit_multi.py`` (against statsmodels where it has the method).
"""

from __future__ import annotations

import math

import numpy as np
from scipy import linalg, optimize, stats

# --------------------------------------------------------------------------------------------- distances and maps


def classical_mds(D, k: int = 2) -> dict:
    """Torgerson's (1952) classical scaling: double-centre -D^2/2 to a Gram matrix B = X X', and take its top k
    eigenvectors scaled by root eigenvalue.  Exact (up to rotation) when D is Euclidean."""
    D = np.asarray(D, float)
    n = len(D)
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ (D ** 2) @ J
    w, V = np.linalg.eigh(B)
    o = np.argsort(w)[::-1]
    w, V = w[o], V[:, o]
    X = V[:, :k] * np.sqrt(np.maximum(w[:k], 0))
    pos = w[w > 0].sum()
    return {"X": X, "eigenvalues": w, "explained": w[:k].sum() / pos, "negative_share": float(-w[w < 0].sum() / pos)}


def procrustes(A, B) -> dict:
    """Rotate, reflect, scale and translate B onto A to minimize ||A - (s B R + t)||^2 (orthogonal Procrustes)."""
    A, B = np.asarray(A, float), np.asarray(B, float)
    ma, mb = A.mean(0), B.mean(0)
    A0, B0 = A - ma, B - mb
    U, s, Vt = np.linalg.svd(B0.T @ A0)
    Rm = U @ Vt
    scale = s.sum() / np.sum(B0 ** 2)
    fitted = scale * B0 @ Rm + ma
    return {"fitted": fitted, "R": Rm, "scale": float(scale), "rmse": float(np.sqrt(np.mean(np.sum((A - fitted) ** 2, 1))))}


def mahalanobis(X, mu, S) -> np.ndarray:
    D = np.asarray(X, float) - mu
    return np.sqrt(np.einsum("ij,ij->i", D @ np.linalg.inv(S), D))


# ------------------------------------------------------------------------------------------------------ Wishart


def wishart_bartlett(Sigma, df: int, rng: np.random.Generator) -> np.ndarray:
    """One W ~ Wishart_p(df, Sigma) by Bartlett's (1933) decomposition: W = L A A' L' with L L' = Sigma, A lower
    triangular, A_ii^2 ~ chi^2_{df - i + 1}, A_ij ~ N(0, 1) below the diagonal."""
    Sigma = np.asarray(Sigma, float)
    p = len(Sigma)
    L = np.linalg.cholesky(Sigma)
    A = np.zeros((p, p))
    for i in range(p):
        A[i, i] = math.sqrt(rng.chisquare(df - i))
        A[i, :i] = rng.standard_normal(i)
    M = L @ A
    return M @ M.T


# ----------------------------------------------------------------------------------------- Hotelling and MANOVA


def hotelling_one(X, mu0) -> dict:
    """T^2 = n (xbar - mu0)' S^{-1} (xbar - mu0); (n - p)/(p(n - 1)) T^2 ~ F(p, n - p) under normality."""
    X = np.asarray(X, float)
    n, p = X.shape
    d = X.mean(0) - np.asarray(mu0, float)
    S = np.cov(X.T)
    T2 = float(n * d @ np.linalg.solve(S, d))
    F = (n - p) / (p * (n - 1)) * T2
    return {"T2": T2, "F": F, "df": (p, n - p), "p": float(stats.f.sf(F, p, n - p)), "p_chi2": float(stats.chi2.sf(T2, p))}


def hotelling_two(X, Y) -> dict:
    """The two-sample T^2 with pooled covariance; (n1 + n2 - p - 1)/(p (n1 + n2 - 2)) T^2 ~ F(p, n1 + n2 - p - 1)."""
    X, Y = np.asarray(X, float), np.asarray(Y, float)
    n1, p = X.shape
    n2 = len(Y)
    d = X.mean(0) - Y.mean(0)
    S = ((n1 - 1) * np.cov(X.T) + (n2 - 1) * np.cov(Y.T)) / (n1 + n2 - 2)
    T2 = float(n1 * n2 / (n1 + n2) * d @ np.linalg.solve(S, d))
    m = n1 + n2 - 2
    F = (m - p + 1) / (p * m) * T2
    return {"T2": T2, "F": F, "df": (p, m - p + 1), "p": float(stats.f.sf(F, p, m - p + 1)), "p_chi2": float(stats.chi2.sf(T2, p)),
            "direction": np.linalg.solve(S, d)}


def bai_saranadasa(X, Y) -> dict:
    """Bai & Saranadasa's (1996) test: drop S^{-1}; ||xbar - ybar||^2 minus its null mean, standardized by an estimate
    of its variance.  Asymptotically N(0, 1) as p, n grow together."""
    X, Y = np.asarray(X, float), np.asarray(Y, float)
    n1, p = X.shape
    n2 = len(Y)
    n = n1 + n2 - 2
    S = ((n1 - 1) * np.cov(X.T) + (n2 - 1) * np.cov(Y.T)) / n
    tau = n1 * n2 / (n1 + n2)
    d = X.mean(0) - Y.mean(0)
    trS = np.trace(S)
    B2 = n ** 2 / ((n + 2) * (n - 1)) * (np.trace(S @ S) - trS ** 2 / n)
    Z = (tau * d @ d - trS) / math.sqrt(2 * (n + 1) / n * B2)
    return {"Z": float(Z), "p": float(stats.norm.sf(Z))}


def manova(X, groups) -> dict:
    """One-way MANOVA: H (between) and E (within) SSCP matrices and the four statistics from the eigenvalues of
    E^{-1}H: Wilks's Lambda (with Rao's F), Pillai's trace, Hotelling--Lawley's trace and Roy's largest root."""
    X = np.asarray(X, float)
    g = np.asarray(groups)
    levels = np.unique(g)
    n, p = X.shape
    k = len(levels)
    m = X.mean(0)
    H = np.zeros((p, p))
    E = np.zeros((p, p))
    for lv in levels:
        Xi = X[g == lv]
        d = Xi.mean(0) - m
        H += len(Xi) * np.outer(d, d)
        C = Xi - Xi.mean(0)
        E += C.T @ C
    lam = np.sort(np.real(np.linalg.eigvals(np.linalg.solve(E, H))))[::-1]
    lam = np.maximum(lam, 0)
    wilks = float(np.prod(1 / (1 + lam)))
    pillai = float(np.sum(lam / (1 + lam)))
    hl = float(np.sum(lam))
    roy = float(lam[0])
    # Rao's F approximation for Wilks
    dh, de = k - 1, n - k
    t = math.sqrt((p ** 2 * dh ** 2 - 4) / (p ** 2 + dh ** 2 - 5)) if p ** 2 + dh ** 2 - 5 > 0 else 1.0
    df1 = p * dh
    w = de + dh - (p + dh + 1) / 2
    df2 = w * t - (p * dh - 2) / 2
    Fw = (1 - wilks ** (1 / t)) / wilks ** (1 / t) * df2 / df1
    return {"H": H, "E": E, "eigen": lam, "wilks": wilks, "pillai": pillai, "hotelling_lawley": hl, "roy": roy,
            "wilks_F": float(Fw), "wilks_df": (df1, float(df2)), "wilks_p": float(stats.f.sf(Fw, df1, df2))}


# ------------------------------------------------------------------------------------------------------------ PCA


def pca(X, standardize: bool = False) -> dict:
    """Principal components by the SVD of the centred (optionally standardized) data: X0 = U D V'.  Scores U D,
    loadings V, variances D^2/(n - 1); biplot coordinates (alpha = 1: scores U D, arrows V)."""
    X = np.asarray(X, float)
    X0 = X - X.mean(0)
    if standardize:
        X0 = X0 / X0.std(0, ddof=1)
    U, d, Vt = np.linalg.svd(X0, full_matrices=False)
    var = d ** 2 / (len(X) - 1)
    # sign convention: largest loading positive
    s = np.sign(Vt[np.arange(len(Vt)), np.argmax(np.abs(Vt), 1)])
    Vt = Vt * s[:, None]
    U = U * s[None, :]
    return {"scores": U * d, "loadings": Vt.T, "variances": var, "explained": var / var.sum(), "U": U, "d": d}


# ----------------------------------------------------------------------------------------------- factor analysis


def _fa_loadings(R, psi, k):
    """Given uniquenesses psi, the ML loadings: Psi^{1/2} times the top-k eigenvectors of Psi^{-1/2} R Psi^{-1/2},
    scaled by root(eigenvalue - 1)."""
    s = 1 / np.sqrt(psi)
    Rs = s[:, None] * R * s[None, :]
    w, V = np.linalg.eigh(Rs)
    o = np.argsort(w)[::-1][:k]
    w, V = w[o], V[:, o]
    return (np.sqrt(psi)[:, None] * V) * np.sqrt(np.maximum(w - 1, 0))[None, :]


def factor_ml(R, k: int, n: int | None = None) -> dict:
    """Maximum-likelihood factor analysis of a correlation matrix R with k factors (Lawley 1940; Jöreskog 1967):
    minimize F(Psi) = log|Sigma| + tr(Sigma^{-1} R) - log|R| - p over the uniquenesses, Sigma = L L' + Psi with the
    loadings L profiled out.  Returns loadings, uniquenesses, communalities and (if n is given) Bartlett's corrected
    likelihood-ratio test of k factors."""
    R = np.asarray(R, float)
    p = len(R)

    def F(lpsi):
        psi = np.exp(lpsi)
        L = _fa_loadings(R, psi, k)
        Sig = L @ L.T + np.diag(psi)
        sign, ld = np.linalg.slogdet(Sig)
        return ld + np.trace(np.linalg.solve(Sig, R)) - np.linalg.slogdet(R)[1] - p

    psi0 = (1 - 0.5 * k / p) / np.diag(np.linalg.inv(R))
    res = optimize.minimize(F, np.log(np.clip(psi0, 0.005, 1)), method="L-BFGS-B", bounds=[(math.log(0.005), 0.0)] * p)
    psi = np.exp(res.x)
    L = _fa_loadings(R, psi, k)
    out = {"loadings": L, "uniqueness": psi, "communality": 1 - psi, "objective": float(res.fun),
           "heywood": bool(np.any(psi <= 0.0051))}
    if n is not None:
        df = ((p - k) ** 2 - (p + k)) / 2
        chi2 = (n - 1 - (2 * p + 5) / 6 - 2 * k / 3) * res.fun
        out.update({"chi2": float(chi2), "df": float(df), "p": float(stats.chi2.sf(chi2, df)) if df > 0 else float("nan")})
    return out


def varimax(L, tol: float = 1e-10, max_iter: int = 500) -> dict:
    """Kaiser's (1958) varimax rotation: the orthogonal T maximizing the variance of the squared loadings per column."""
    L = np.asarray(L, float)
    p, k = L.shape
    T = np.eye(k)
    d = 0.0
    for _ in range(max_iter):
        Lr = L @ T
        U, s, Vt = np.linalg.svd(L.T @ (Lr ** 3 - Lr @ np.diag(np.sum(Lr ** 2, 0)) / p))
        T = U @ Vt
        dn = s.sum()
        if dn < d * (1 + tol):
            break
        d = dn
    Lr = L @ T
    return {"loadings": Lr, "rotation": T}


# -------------------------------------------------------------------------------------------------- canonical


def cca(X, Y) -> dict:
    """Canonical correlations (Hotelling 1936): the singular values of Sxx^{-1/2} Sxy Syy^{-1/2}, with canonical
    weights, and Bartlett's chi^2 test that correlations k+1, ... are all zero."""
    X, Y = np.asarray(X, float), np.asarray(Y, float)
    n = len(X)
    Xc, Yc = X - X.mean(0), Y - Y.mean(0)
    Sxx, Syy, Sxy = Xc.T @ Xc / (n - 1), Yc.T @ Yc / (n - 1), Xc.T @ Yc / (n - 1)
    Ix = linalg.inv(linalg.sqrtm(Sxx)).real
    Iy = linalg.inv(linalg.sqrtm(Syy)).real
    U, r, Vt = np.linalg.svd(Ix @ Sxy @ Iy)
    a, b = Ix @ U, Iy @ Vt.T
    p, q = X.shape[1], Y.shape[1]
    tests = []
    for k in range(len(r)):
        lam = np.prod(1 - r[k:] ** 2)
        chi = -(n - 1 - (p + q + 1) / 2) * math.log(lam)
        df = (p - k) * (q - k)
        tests.append({"k": k, "chi2": float(chi), "df": df, "p": float(stats.chi2.sf(chi, df))})
    return {"r": r, "a": a, "b": b, "u": Xc @ a, "v": Yc @ b, "tests": tests}


# ------------------------------------------------------------------------------------------------ discriminants


def lda_fit(X, y) -> dict:
    X, y = np.asarray(X, float), np.asarray(y)
    cls = np.unique(y)
    mus = np.array([X[y == c].mean(0) for c in cls])
    pri = np.array([np.mean(y == c) for c in cls])
    E = sum(((X[y == c] - mus[k]).T @ (X[y == c] - mus[k])) for k, c in enumerate(cls))
    S = E / (len(X) - len(cls))
    # Fisher's discriminant directions: eigenvectors of S^{-1} B
    m = X.mean(0)
    B = sum(np.sum(y == c) * np.outer(mus[k] - m, mus[k] - m) for k, c in enumerate(cls))
    w, V = linalg.eigh(B, S)
    o = np.argsort(w)[::-1]
    return {"classes": cls, "means": mus, "priors": pri, "S": S, "directions": V[:, o[: len(cls) - 1]], "eigen": w[o]}


def lda_predict(fit, X) -> np.ndarray:
    X = np.asarray(X, float)
    Si = np.linalg.inv(fit["S"])
    sc = np.array([X @ Si @ m - 0.5 * m @ Si @ m + math.log(p) for m, p in zip(fit["means"], fit["priors"])]).T
    return fit["classes"][np.argmax(sc, 1)]


def qda_fit(X, y) -> dict:
    X, y = np.asarray(X, float), np.asarray(y)
    cls = np.unique(y)
    return {"classes": cls, "means": [X[y == c].mean(0) for c in cls], "covs": [np.cov(X[y == c].T) for c in cls],
            "priors": [np.mean(y == c) for c in cls]}


def qda_predict(fit, X) -> np.ndarray:
    X = np.asarray(X, float)
    sc = []
    for m, S, p in zip(fit["means"], fit["covs"], fit["priors"]):
        sc.append(np.atleast_1d(stats.multivariate_normal(m, S).logpdf(X)) + math.log(p))
    return fit["classes"][np.argmax(np.array(sc).T, 1)]


def loo_error(X, y, method: str = "lda") -> float:
    X, y = np.asarray(X, float), np.asarray(y)
    wrong = 0
    for i in range(len(X)):
        m = np.ones(len(X), bool)
        m[i] = False
        if method == "lda":
            pr = lda_predict(lda_fit(X[m], y[m]), X[i:i + 1])
        else:
            pr = qda_predict(qda_fit(X[m], y[m]), X[i:i + 1])
        wrong += pr[0] != y[i]
    return wrong / len(X)


# --------------------------------------------------------------------------------------------------- clustering


def kmeans(X, k: int, rng: np.random.Generator, n_init: int = 10, max_iter: int = 300) -> dict:
    """Lloyd's algorithm from k-means++ starts (Arthur & Vassilvitskii 2007); the best of n_init runs."""
    X = np.asarray(X, float)
    n = len(X)
    best = None
    for _ in range(n_init):
        C = [X[rng.integers(n)]]
        for _ in range(1, k):
            d2 = np.min(((X[:, None, :] - np.array(C)[None]) ** 2).sum(-1), 1)
            C.append(X[rng.choice(n, p=d2 / d2.sum())])
        C = np.array(C)
        path = [C.copy()]
        for it in range(max_iter):
            lab = np.argmin(((X[:, None, :] - C[None]) ** 2).sum(-1), 1)
            newC = np.array([X[lab == j].mean(0) if np.any(lab == j) else C[j] for j in range(k)])
            path.append(newC.copy())
            if np.allclose(newC, C):
                break
            C = newC
        wss = float(np.sum((X - C[lab]) ** 2))
        if best is None or wss < best["wss"]:
            best = {"centres": C, "labels": lab, "wss": wss, "iterations": it + 1, "path": path}
    return best


def gmm_em(X, k: int, rng: np.random.Generator, n_init: int = 5, max_iter: int = 500, tol: float = 1e-8) -> dict:
    """A Gaussian mixture with full covariances by EM (Dempster, Laird & Rubin 1977; Part 22), k-means starts; the
    best log likelihood of n_init runs, with BIC."""
    X = np.asarray(X, float)
    n, p = X.shape
    best = None
    for _ in range(n_init):
        km = kmeans(X, k, rng, n_init=1)
        lab = km["labels"]
        w = np.array([max(np.mean(lab == j), 1e-3) for j in range(k)])
        mu = km["centres"].copy()
        S = np.array([np.cov(X[lab == j].T) + 1e-3 * np.eye(p) if np.sum(lab == j) > p else np.cov(X.T) for j in range(k)])
        ll_old = -np.inf
        for it in range(max_iter):
            logp = np.column_stack([np.log(w[j]) + stats.multivariate_normal(mu[j], S[j], allow_singular=True).logpdf(X) for j in range(k)])
            mx = logp.max(1, keepdims=True)
            ll = float(np.sum(mx[:, 0] + np.log(np.exp(logp - mx).sum(1))))
            r = np.exp(logp - mx)
            r /= r.sum(1, keepdims=True)
            nk = r.sum(0)
            w = nk / n
            mu = (r.T @ X) / nk[:, None]
            S = np.array([((X - mu[j]).T * r[:, j]) @ (X - mu[j]) / nk[j] + 1e-6 * np.eye(p) for j in range(k)])
            if ll - ll_old < tol * abs(ll):
                break
            ll_old = ll
        npar = k - 1 + k * p + k * p * (p + 1) / 2
        res = {"weights": w, "means": mu, "covs": S, "loglik": ll, "resp": r, "labels": np.argmax(r, 1), "iterations": it + 1,
               "bic": float(-2 * ll + npar * math.log(n)), "npar": npar}
        if best is None or res["loglik"] > best["loglik"]:
            best = res
    return best


def adjusted_rand(a, b) -> float:
    """Hubert & Arabie's (1985) adjusted Rand index between two labellings."""
    a, b = np.asarray(a), np.asarray(b)
    ua, ub = np.unique(a), np.unique(b)
    M = np.array([[np.sum((a == i) & (b == j)) for j in ub] for i in ua])
    c2 = lambda x: x * (x - 1) / 2
    s = c2(M).sum()
    sa, sb = c2(M.sum(1)).sum(), c2(M.sum(0)).sum()
    e = sa * sb / c2(len(a))
    return float((s - e) / (0.5 * (sa + sb) - e))


# -------------------------------------------------------------------------------------------- graphical models


def partial_correlations(S) -> np.ndarray:
    P = np.linalg.inv(np.asarray(S, float))
    d = np.sqrt(np.diag(P))
    out = -P / np.outer(d, d)
    np.fill_diagonal(out, 1.0)
    return out


def _lasso_cd(V, s, lam, beta, iters=500, tol=1e-10):
    """min_b  b'Vb/2 - s'b + lam ||b||_1 by coordinate descent (the graphical lasso's inner problem)."""
    p = len(s)
    for _ in range(iters):
        old = beta.copy()
        for j in range(p):
            r = s[j] - V[j] @ beta + V[j, j] * beta[j]
            beta[j] = np.sign(r) * max(abs(r) - lam, 0) / V[j, j]
        if np.max(np.abs(beta - old)) < tol:
            break
    return beta


def graphical_lasso(S, lam: float, max_iter: int = 200, tol: float = 1e-8) -> dict:
    """Friedman, Hastie & Tibshirani's (2008) graphical lasso: the precision Theta maximizing
    log det Theta - tr(S Theta) - lam ||Theta||_1 (off-diagonal), by block coordinate descent over columns of
    W = Theta^{-1}, each a lasso."""
    S = np.asarray(S, float)
    p = len(S)
    W = S + lam * np.eye(p)
    B = np.zeros((p, p - 1))
    for it in range(max_iter):
        W_old = W.copy()
        for j in range(p):
            idx = np.r_[0:j, j + 1:p]
            V = W[np.ix_(idx, idx)]
            beta = _lasso_cd(V, S[idx, j], lam, B[j].copy())
            B[j] = beta
            w12 = V @ beta
            W[idx, j] = w12
            W[j, idx] = w12
        if np.mean(np.abs(W - W_old)) < tol * np.mean(np.abs(S - np.diag(np.diag(S))) + 1e-12):
            break
    Theta = np.zeros((p, p))
    for j in range(p):
        idx = np.r_[0:j, j + 1:p]
        t = 1 / (W[j, j] - W[idx, j] @ B[j])
        Theta[j, j] = t
        Theta[idx, j] = -B[j] * t
    Theta = 0.5 * (Theta + Theta.T)
    edges = int(np.sum(np.abs(np.triu(Theta, 1)) > 1e-6 * np.max(np.abs(np.diag(Theta)))))
    return {"precision": Theta, "covariance": W, "edges": edges, "iterations": it + 1}
