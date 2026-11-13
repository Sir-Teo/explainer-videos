"""Dense linear algebra (Part 52): conditioning and backward error; LU with and without pivoting and its growth
factor; Cholesky; least squares by the normal equations, Householder QR and Givens; classical against modified
Gram-Schmidt; the SVD for rank and regularization.  After Trefethen and Bau, *Numerical Linear Algebra* (1997), and
Higham, *Accuracy and Stability of Numerical Algorithms* (2002)."""

from __future__ import annotations

import numpy as np

EPS = float(np.finfo(float).eps)


# ---------------------------------------------------------------- conditioning

def cond_examples() -> dict:
    """Condition numbers of f(x) (relative: |x f'(x) / f(x)|) and of matrices."""
    def kf(f, df, x):
        return abs(x * df(x) / f(x))
    scalar = [{"f": "x - 1 near x = 1.000001", "kappa": kf(lambda x: x - 1, lambda x: 1.0, 1.000001)},
              {"f": "sqrt(x)", "kappa": kf(np.sqrt, lambda x: 0.5 / np.sqrt(x), 2.0)},
              {"f": "exp(x) at x = 100", "kappa": kf(np.exp, np.exp, 100.0)},
              {"f": "tan(x) near pi/2", "kappa": kf(np.tan, lambda x: 1 / np.cos(x) ** 2, 1.5707)}]
    hil = [{"n": n, "kappa": float(np.linalg.cond(hilbert(n)))} for n in (4, 8, 12)]
    return {"scalar": scalar, "hilbert": hil}


def hilbert(n: int) -> np.ndarray:
    i = np.arange(n)
    return 1.0 / (i[:, None] + i[None, :] + 1)


def forward_vs_backward(ns=(4, 6, 8, 10, 12), seed: int = 0) -> list[dict]:
    """Solve H x = b for the Hilbert matrix with a known x: the backward error ||b - H x^|| / (||H|| ||x^||) stays near
    machine epsilon, while the forward error grows with kappa; forward <= kappa * backward (Wilkinson).

    ``backward`` is the residual as computed in floating point and ``bound`` is kappa times it.  Wilkinson's
    inequality is about the exact residual of the exact b; here b = H x was rounded and so is b - H x^, which can
    come out exactly 0.  So for some seeds ``bound`` is 0, or a little below ``forward`` (not for the default seed,
    the film's); kappa * (backward + eps) always holds."""
    rng = np.random.default_rng(seed)
    out = []
    for n in ns:
        H = hilbert(n)
        x = rng.standard_normal(n)
        b = H @ x
        xh = np.linalg.solve(H, b)
        k = float(np.linalg.cond(H))
        back = float(np.linalg.norm(b - H @ xh) / (np.linalg.norm(H, 2) * np.linalg.norm(xh)))
        fwd = float(np.linalg.norm(xh - x) / np.linalg.norm(x))
        out.append({"n": n, "kappa": k, "backward": back, "forward": fwd, "bound": k * back})
    return out


# ---------------------------------------------------------------- LU

def lu(A: np.ndarray, pivot: bool = True):
    """Gaussian elimination as P A = L U.  Returns P (as a permutation), L, U and the growth factor
    max |u_ij| / max |a_ij|."""
    A = np.array(A, dtype=float)
    n = A.shape[0]
    U = A.copy()
    L = np.eye(n)
    perm = np.arange(n)
    big = np.abs(A).max()
    grow = big
    for k in range(n - 1):
        if pivot:
            p = k + int(np.argmax(np.abs(U[k:, k])))
            if p != k:
                U[[k, p], k:] = U[[p, k], k:]
                L[[k, p], :k] = L[[p, k], :k]
                perm[[k, p]] = perm[[p, k]]
        m = U[k + 1:, k] / U[k, k]
        L[k + 1:, k] = m
        U[k + 1:, k:] -= np.outer(m, U[k, k:])
        U[k + 1:, k] = 0.0
        grow = max(grow, np.abs(U).max())
    return perm, L, U, grow / big


def solve_lu(A, b, pivot=True):
    perm, L, U, g = lu(A, pivot)
    y = np.linalg.solve(L, np.asarray(b, float)[perm]) if True else None
    return np.linalg.solve(U, y), g


def pivot_failure(eps_values=(1e-4, 1e-8, 1e-12, 1e-16, 1e-20)) -> list[dict]:
    """[[eps, 1], [1, 1]] x = [1, 2]: the exact solution is close to (1, 1).  Without pivoting the multiplier 1/eps
    swamps the 1 in the (2, 2) entry and x1 comes out wrong; with partial pivoting it is right."""
    rows = []
    for e in eps_values:
        A = np.array([[e, 1.0], [1.0, 1.0]])
        b = np.array([1.0, 2.0])
        exact = np.array([1 / (1 - e), (1 - 2 * e) / (1 - e)])
        xn, _ = solve_lu(A, b, pivot=False)
        xp, _ = solve_lu(A, b, pivot=True)
        perm, L, U, _ = lu(A, pivot=False)
        rows.append({"eps": e, "no_pivot": xn.tolist(), "pivot": xp.tolist(), "exact": exact.tolist(),
                     "err_no_pivot": float(np.abs(xn - exact).max()), "err_pivot": float(np.abs(xp - exact).max()),
                     "U22": float(U[1, 1]), "L21": float(L[1, 0])})
    return rows


def wilkinson_matrix(n: int) -> np.ndarray:
    A = np.eye(n) - np.tril(np.ones((n, n)), -1)
    A[:, -1] = 1.0
    return A


def growth(ns=(4, 8, 16, 32, 64), trials: int = 50, seed: int = 0) -> list[dict]:
    """Partial pivoting's growth factor: 2^(n-1) on Wilkinson's matrix, about n^(2/3) on random matrices (Trefethen
    and Schreiber 1990)."""
    rng = np.random.default_rng(seed)
    rows = []
    for n in ns:
        worst = lu(wilkinson_matrix(n))[3]
        rand = [lu(rng.standard_normal((n, n)))[3] for _ in range(trials)]
        rows.append({"n": n, "wilkinson": float(worst), "two_n_minus_1": 2.0 ** (n - 1), "random_mean": float(
            np.mean(rand)), "random_max": float(np.max(rand)), "n_two_thirds": n ** (2 / 3)})
    return rows


def flops(n: int) -> dict:
    return {"lu": 2 * n ** 3 / 3, "cholesky": n ** 3 / 3, "qr_householder": 4 * n ** 3 / 3}


def cholesky(A: np.ndarray) -> np.ndarray:
    A = np.array(A, float)
    n = A.shape[0]
    L = np.zeros_like(A)
    for j in range(n):
        s = A[j, j] - L[j, :j] @ L[j, :j]
        if s <= 0:
            raise ValueError("not positive definite")
        L[j, j] = np.sqrt(s)
        L[j + 1:, j] = (A[j + 1:, j] - L[j + 1:, :j] @ L[j, :j]) / L[j, j]
    return L


# ---------------------------------------------------------------- QR and least squares

def householder(A: np.ndarray, keep: bool = False):
    """Householder QR: each step reflects a column onto a multiple of e1 through the mirror with normal
    v = x + sign(x1) ||x|| e1.  Returns Q, R (and the mirrors, for drawing)."""
    A = np.array(A, float)
    m, n = A.shape
    R = A.copy()
    Q = np.eye(m)
    mirrors = []
    for k in range(min(m - 1, n)):
        x = R[k:, k]
        v = x.copy()
        v[0] += np.copysign(np.linalg.norm(x), x[0] if x[0] != 0 else 1.0)
        v /= np.linalg.norm(v)
        R[k:, k:] -= 2 * np.outer(v, v @ R[k:, k:])
        Q[:, k:] -= 2 * np.outer(Q[:, k:] @ v, v)
        if keep:
            mirrors.append({"k": k, "x": x.tolist(), "v": v.tolist(), "after": R[k:, k].tolist()})
    return (Q, R, mirrors) if keep else (Q, R)


def givens(A: np.ndarray):
    A = np.array(A, float)
    m, n = A.shape
    R = A.copy()
    Q = np.eye(m)
    rotations = 0
    for j in range(n):
        for i in range(m - 1, j, -1):
            a, b = R[i - 1, j], R[i, j]
            if b == 0:
                continue
            r = np.hypot(a, b)
            c, s = a / r, b / r
            G = np.array([[c, s], [-s, c]])
            R[[i - 1, i], :] = G @ R[[i - 1, i], :]
            Q[:, [i - 1, i]] = Q[:, [i - 1, i]] @ G.T
            rotations += 1
    return Q, R, rotations


def gram_schmidt(A: np.ndarray, modified: bool):
    A = np.array(A, float)
    m, n = A.shape
    Q = np.zeros((m, n))
    for j in range(n):
        v = A[:, j].copy()
        for i in range(j):
            r = Q[:, i] @ (v if modified else A[:, j])
            v -= r * Q[:, i]
        Q[:, j] = v / np.linalg.norm(v)
    return Q


def orthogonality(ns=(4, 6, 8, 10, 12)) -> list[dict]:
    """||I - Q^T Q|| for Q from classical and modified Gram-Schmidt and Householder, on Hilbert matrices: CGS loses
    orthogonality like kappa^2 eps, MGS like kappa eps, Householder stays at eps (Bjorck)."""
    rows = []
    for n in ns:
        A = hilbert(n)
        I = np.eye(n)
        cgs = gram_schmidt(A, False)
        mgs = gram_schmidt(A, True)
        qh, _ = householder(A)
        rows.append({"n": n, "kappa": float(np.linalg.cond(A)), "cgs": float(np.linalg.norm(I - cgs.T @ cgs)),
                     "mgs": float(np.linalg.norm(I - mgs.T @ mgs)), "householder": float(np.linalg.norm(
                         I - qh.T @ qh))})
    return rows


def least_squares(kappas=(1e2, 1e4, 1e6, 1e8), m: int = 50, n: int = 10, seed: int = 0) -> list[dict]:
    """Fit with a matrix of prescribed condition number: the normal equations square kappa; QR does not."""
    rng = np.random.default_rng(seed)
    rows = []
    for k in kappas:
        U, _ = np.linalg.qr(rng.standard_normal((m, n)))
        V, _ = np.linalg.qr(rng.standard_normal((n, n)))
        s = np.logspace(0, -np.log10(k), n)
        A = U @ np.diag(s) @ V.T
        x = rng.standard_normal(n)
        b = A @ x + 1e-10 * rng.standard_normal(m)
        xt = np.linalg.lstsq(A, b, rcond=None)[0]
        xn = np.linalg.solve(A.T @ A, A.T @ b)
        Q, R = householder(A)
        xq = np.linalg.solve(R[:n], (Q.T @ b)[:n])
        e = lambda y: float(np.linalg.norm(y - xt) / np.linalg.norm(xt))  # noqa: E731
        rows.append({"kappa": k, "normal": e(xn), "qr": e(xq), "kappa_AtA": float(np.linalg.cond(A.T @ A))})
    return rows


def svd_regularize(n: int = 80, noise: float = 1e-3, width: float = 0.05, seed: int = 0) -> dict:
    """Deblurring a 1D signal: the blur matrix's singular values decay fast; the naive solve amplifies noise by
    1/sigma_min; truncating the SVD at k terms trades bias for noise (the L-curve's corner)."""
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 1, n)
    K = np.exp(-((t[:, None] - t[None, :]) ** 2) / (2 * width ** 2))
    K /= K.sum(axis=1, keepdims=True)
    x = ((t > 0.2) & (t < 0.45)).astype(float) + 0.5 * ((t > 0.6) & (t < 0.8))
    b = K @ x + noise * rng.standard_normal(n)
    U, s, Vt = np.linalg.svd(K)
    rows = []
    for k in range(1, n + 1):
        xk = Vt[:k].T @ ((U[:, :k].T @ b) / s[:k])
        rows.append({"k": k, "error": float(np.linalg.norm(xk - x) / np.linalg.norm(x)),
                     "residual": float(np.linalg.norm(K @ xk - b))})
    best = min(rows, key=lambda r: r["error"])
    kb = best["k"]
    return {"sigma": s.tolist(), "rows": rows, "best_k": kb, "x": x.tolist(), "b": b.tolist(),
            "x_best": (Vt[:kb].T @ ((U[:, :kb].T @ b) / s[:kb])).tolist(),
            "x_naive_error": rows[-1]["error"], "kappa": float(s[0] / s[-1])}


def smoothed_growth(n: int = 32, sigmas=(0.0, 1e-8, 1e-6, 1e-4, 1e-2), trials: int = 20, seed: int = 0) -> list[dict]:
    """Wilkinson's worst case, perturbed: partial pivoting's growth factor on W + sigma G, G Gaussian.  A tiny
    random perturbation destroys the 2^(n-1) growth (it needs exact ties in every pivot column), which is why it never
    appears in practice; proving a polynomial
    bound in this smoothed sense is open."""
    rng = np.random.default_rng(seed)
    W = wilkinson_matrix(n)
    rows = []
    for s in sigmas:
        g = [lu(W + s * rng.standard_normal((n, n)))[3] for _ in range(trials if s else 1)]
        rows.append({"sigma": s, "median": float(np.median(g)), "max": float(np.max(g))})
    return rows


def randomized_svd(m: int = 1200, n: int = 600, k: int = 20, decay: float = 0.8, oversample=(0, 5, 10),
                   power_iters=(0, 1, 2), seed: int = 0) -> dict:
    """Halko, Martinsson and Tropp (2011): multiply A by a random n x (k + p) matrix, orthonormalize the result,
    and take the SVD of the small projected matrix.  The spectral-norm error against the optimal rank-k error
    sigma_{k+1}, for a matrix with geometrically decaying singular values, and the time against a full SVD."""
    import time
    rng = np.random.default_rng(seed)
    U, _ = np.linalg.qr(rng.standard_normal((m, n)))
    V, _ = np.linalg.qr(rng.standard_normal((n, n)))
    s = decay ** np.arange(n)
    A = (U * s) @ V.T
    t0 = time.perf_counter()
    np.linalg.svd(A, full_matrices=False)
    t_full = time.perf_counter() - t0
    rows = []
    for p in oversample:
        for q in power_iters:
            t0 = time.perf_counter()
            Y = A @ rng.standard_normal((n, k + p))
            for _ in range(q):
                Y = A @ (A.T @ Y)
            Q, _ = np.linalg.qr(Y)
            Ub, sb, Vbt = np.linalg.svd(Q.T @ A, full_matrices=False)
            Ak = (Q @ Ub[:, :k]) * sb[:k] @ Vbt[:k]
            dt = time.perf_counter() - t0
            err = float(np.linalg.norm(A - Ak, 2))
            rows.append({"oversample": p, "power": q, "error": err, "ratio": err / s[k], "seconds": dt})
    return {"rows": rows, "optimal": float(s[k]), "full_seconds": t_full, "m": m, "n": n, "k": k}
