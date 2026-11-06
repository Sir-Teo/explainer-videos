"""Speed (Part 52): BLAS levels 1, 2 and 3 timed on this machine through NumPy (which calls an optimized BLAS), with
their arithmetic intensity (flops per byte moved); and mixed-precision iterative refinement: factor in single
precision, correct the residual in double, and reach double-precision accuracy (Wilkinson 1963; Carson and Higham
2018)."""

from __future__ import annotations

import time

import numpy as np
import scipy.linalg as sla


def _best(f, reps=5):
    best = float("inf")
    for _ in range(reps):
        t = time.perf_counter()
        f()
        best = min(best, time.perf_counter() - t)
    return best


def blas_levels(ns=(256, 512, 1024, 2048)) -> list[dict]:
    rng = np.random.default_rng(0)
    rows = []
    for n in ns:
        x, y = rng.standard_normal(n * n), rng.standard_normal(n * n)
        A, B = rng.standard_normal((n, n)), rng.standard_normal((n, n))
        v = rng.standard_normal(n)
        t1 = _best(lambda: np.add(x, 2.0 * y))                 # axpy on n^2 elements: 2 n^2 flops, 24 n^2 bytes
        t2 = _best(lambda: A @ v)                               # gemv: 2 n^2 flops, 8 n^2 bytes
        t3 = _best(lambda: A @ B, reps=3)                       # gemm: 2 n^3 flops, 24 n^2 bytes
        rows.append({"n": n, "axpy_gflops": 2 * n * n / t1 / 1e9, "gemv_gflops": 2 * n * n / t2 / 1e9,
                     "gemm_gflops": 2 * n ** 3 / t3 / 1e9, "axpy_intensity": 2 / 24, "gemv_intensity": 2 / 8,
                     "gemm_intensity": 2 * n / 24})
    return rows


def refinement(n: int = 400, kappas=(1e2, 1e5, 1e8), iters: int = 6, seed: int = 0) -> list[dict]:
    """Solve A x = b with an LU factorization computed in float32, refining with float64 residuals."""
    rng = np.random.default_rng(seed)
    rows = []
    for k in kappas:
        U, _ = np.linalg.qr(rng.standard_normal((n, n)))
        V, _ = np.linalg.qr(rng.standard_normal((n, n)))
        A = U @ np.diag(np.logspace(0, -np.log10(k), n)) @ V.T
        x = rng.standard_normal(n)
        b = A @ x
        lu32 = sla.lu_factor(A.astype(np.float32))
        xk = sla.lu_solve(lu32, b.astype(np.float32)).astype(np.float64)
        errs = [float(np.linalg.norm(xk - x) / np.linalg.norm(x))]
        for _ in range(iters):
            r = b - A @ xk
            d = sla.lu_solve(lu32, r.astype(np.float32)).astype(np.float64)
            xk = xk + d
            errs.append(float(np.linalg.norm(xk - x) / np.linalg.norm(x)))
        x64 = np.linalg.solve(A, b)
        rows.append({"kappa": k, "errors": errs, "double_solve": float(np.linalg.norm(x64 - x) / np.linalg.norm(x)),
                     "single_eps": float(np.finfo(np.float32).eps)})
    return rows
