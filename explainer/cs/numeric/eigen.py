"""Eigenvalues by iteration (Part 52): power and inverse iteration; the QR algorithm (Francis 1961; Kublanovskaya
1961) on a Hessenberg matrix, unshifted against shifted, with deflation; the subdiagonal entries decaying, linearly
without shifts and cubically with Wilkinson shifts on a symmetric matrix."""

from __future__ import annotations

import numpy as np


def power(A, iters=60, seed=0, shift=None):
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(A.shape[0])
    lam_true = np.linalg.eigvals(A)
    target = max(lam_true, key=abs) if shift is None else min(lam_true, key=lambda l: abs(l - shift))
    errs = []
    M = A if shift is None else np.linalg.inv(A - shift * np.eye(A.shape[0]))
    for _ in range(iters):
        x = M @ x
        x /= np.linalg.norm(x)
        lam = x @ A @ x
        errs.append(float(abs(lam - target.real)))
    return {"errors": errs, "target": float(target.real)}


def hessenberg(A):
    A = np.array(A, float)
    n = A.shape[0]
    for k in range(n - 2):
        x = A[k + 1:, k]
        v = x.copy()
        v[0] += np.copysign(np.linalg.norm(x), x[0] if x[0] != 0 else 1.0)
        if np.linalg.norm(v) == 0:
            continue
        v /= np.linalg.norm(v)
        A[k + 1:, :] -= 2 * np.outer(v, v @ A[k + 1:, :])
        A[:, k + 1:] -= 2 * np.outer(A[:, k + 1:] @ v, v)
    return A


def qr_algorithm(A, shifted: bool, max_iter: int = 500, tol: float = 1e-14):
    """Returns the eigenvalues found (by deflation) and, per iteration, |h_{m,m-1}| of the active block's last
    subdiagonal entry, and the sequence of full matrices' subdiagonal magnitudes for the first iterations."""
    H = hessenberg(A)
    n = H.shape[0]
    m = n
    found = []
    trace = []
    snapshots = []
    it = 0
    while m > 1 and it < max_iter:
        B = H[:m, :m]
        if shifted:
            a, b, c = B[-2, -2], B[-1, -2], B[-1, -1]
            d = (a - c) / 2
            mu = c - np.sign(d if d != 0 else 1.0) * b * b / (abs(d) + np.hypot(d, b))   # Wilkinson shift
        else:
            mu = 0.0
        Q, R = np.linalg.qr(B - mu * np.eye(m))
        H[:m, :m] = R @ Q + mu * np.eye(m)
        it += 1
        sub = abs(H[m - 1, m - 2])
        trace.append({"iter": it, "m": m, "sub": float(sub)})
        if len(snapshots) < 40:
            snapshots.append(np.abs(np.diag(H, -1)).tolist())
        if sub < tol * (abs(H[m - 1, m - 1]) + abs(H[m - 2, m - 2])):
            found.append(float(H[m - 1, m - 1]))
            m -= 1
    if m == 1:
        found.append(float(H[0, 0]))
    return {"eigenvalues": sorted(found), "iterations": it, "trace": trace, "snapshots": snapshots}


def qr_experiment(n: int = 8, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, n))
    A = X + X.T
    true = sorted(np.linalg.eigvalsh(A).tolist())
    un = qr_algorithm(A, shifted=False, max_iter=3000)
    sh = qr_algorithm(A, shifted=True)
    # convergence order of the first deflation with shifts: log|h_k+1| / log|h_k|
    first = [t["sub"] for t in sh["trace"] if t["m"] == n]
    orders = [np.log(first[i + 1]) / np.log(first[i]) for i in range(len(first) - 1) if 0 < first[i] < 0.5
              and first[i + 1] > 0]
    return {"n": n, "true": true, "unshifted": {"iterations": un["iterations"], "error": float(np.max(np.abs(
        np.array(un["eigenvalues"]) - true))) if len(un["eigenvalues"]) == n else None,
        "trace": un["trace"][:400], "snapshots": un["snapshots"]},
        "shifted": {"iterations": sh["iterations"], "error": float(np.max(np.abs(np.array(sh["eigenvalues"]) - true))),
                    "trace": sh["trace"], "snapshots": sh["snapshots"], "first_block": first,
                    "orders": [float(o) for o in orders]},
        "power": power(A), "inverse": power(A, iters=12, shift=true[0] + 0.3)}
