"""Iterative and sparse solvers (Part 52): steepest descent against conjugate gradient (Hestenes and Stiefel 1952)
on the 2D Poisson problem, with CG's bound 2((sqrt(k) - 1)/(sqrt(k) + 1))^k; Jacobi and symmetric SOR
preconditioning; GMRES on a nonsymmetric problem; CSR storage; fill-in under natural, reverse Cuthill-McKee,
minimum-degree and nested-dissection orderings; and geometric multigrid, whose V-cycle converges at a rate
independent of the grid (Briggs, Henson and McCormick, *A Multigrid Tutorial*)."""

from __future__ import annotations

import math
import time

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla


def poisson2d(m: int) -> sp.csr_matrix:
    """The 5-point Laplacian on an m x m interior grid (Dirichlet boundary), scaled by h^2."""
    T = sp.diags([-1.0, 2.0, -1.0], [-1, 0, 1], shape=(m, m))
    I = sp.identity(m)
    return (sp.kron(I, T) + sp.kron(T, I)).tocsr()


def steepest(A, b, tol=1e-8, max_iter=20000):
    b = np.asarray(b, dtype=float)
    x = np.zeros_like(b)
    r = b.copy()
    hist = [1.0]
    nb = np.linalg.norm(b)
    if nb == 0:
        return x, [0.0]
    for _ in range(max_iter):
        Ar = A @ r
        a = (r @ r) / (r @ Ar)
        x += a * r
        r -= a * Ar
        hist.append(float(np.linalg.norm(r) / nb))
        if hist[-1] < tol:
            break
    return x, hist


def cg(A, b, tol=1e-8, max_iter=20000, M=None):
    b = np.asarray(b, dtype=float)
    x = np.zeros_like(b)
    r = b.copy()
    nb = np.linalg.norm(b)
    if nb == 0:
        return x, [0.0]
    z = M(r) if M else r
    p = z.copy()
    rz = r @ z
    hist = [1.0]
    for _ in range(max_iter):
        Ap = A @ p
        curvature = p @ Ap
        if curvature <= 0 or rz <= 0:
            raise ValueError("CG requires positive definite matrix and preconditioner")
        a = rz / curvature
        x += a * p
        r -= a * Ap
        hist.append(float(np.linalg.norm(r) / nb))
        if hist[-1] < tol:
            break
        z = M(r) if M else r
        rz_new = r @ z
        p = z + (rz_new / rz) * p
        rz = rz_new
    return x, hist


def ssor(A, w: float = 1.5):
    """The symmetric SOR preconditioner M = (D/w + L) (D/w)^-1 (D/w + U) / (2 - w) / w, applied by two triangular
    solves; symmetric positive definite, so CG may use it."""
    D = sp.diags(A.diagonal())
    Lo = sp.tril(A, -1)
    Up = sp.triu(A, 1)
    M1 = (D / w + Lo).tocsr()
    M2 = (D / w + Up).tocsr()
    d = A.diagonal() / w
    c = (2 - w) / w

    def apply(r):
        y = spla.spsolve_triangular(M1, r, lower=True)
        return c * spla.spsolve_triangular(M2, d * y, lower=False)

    return apply


def krylov_experiment(ms=(16, 32, 64), seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    rows = []
    curves = {}
    for m in ms:
        A = poisson2d(m)
        b = rng.standard_normal(m * m)
        lam_max = 4 * 2 * math.sin(m * math.pi / (2 * (m + 1))) ** 2
        lam_min = 4 * 2 * math.sin(math.pi / (2 * (m + 1))) ** 2
        kappa = lam_max / lam_min
        _, hs = steepest(A, b, max_iter=40000 if m <= 32 else 8000)
        _, hc = cg(A, b)
        d = A.diagonal()
        _, hj = cg(A, b, M=lambda r: r / d)
        _, hi = cg(A, b, M=ssor(A))
        rate = (math.sqrt(kappa) - 1) / (math.sqrt(kappa) + 1)
        k_bound = math.ceil(math.log(1e-8 / 2) / math.log(rate))
        rows.append({"m": m, "n": m * m, "kappa": kappa, "steepest": len(hs) - 1 if hs[-1] < 1e-8 else None,
                     "steepest_reached": hs[-1], "cg": len(hc) - 1, "cg_bound": k_bound, "jacobi_cg": len(hj) - 1,
                     "ssor_cg": len(hi) - 1, "steepest_predicted": math.ceil(math.log(1e-8) / math.log(
                         (kappa - 1) / (kappa + 1)))})
        if m == ms[1]:
            curves = {"steepest": hs[:2000:5], "cg": hc, "ssor": hi}
    return {"rows": rows, "curves": curves}


def gmres_demo(m: int = 32, conv: float = 20.0) -> dict:
    """Convection-diffusion makes the matrix nonsymmetric: CG does not apply; GMRES minimizes the residual over the
    Krylov space."""
    A = poisson2d(m) + conv / (m + 1) * sp.kron(sp.identity(m), sp.diags([-0.5, 0.5], [-1, 1], shape=(m, m)))
    b = np.ones(m * m)
    hist = []
    spla.gmres(A, b, rtol=1e-8, restart=200, maxiter=1, callback=lambda r: hist.append(float(r)),
               callback_type="pr_norm")
    return {"residuals": hist, "iterations": len(hist), "symmetric": False}


# ---------------------------------------------------------------- sparse orderings

def nested_dissection(m: int) -> np.ndarray:
    """An ordering of an m x m grid: number the two halves recursively, then the separator last."""
    order = []

    def rec(r0, r1, c0, c1):
        if r1 - r0 <= 2 or c1 - c0 <= 2:
            order.extend(i * m + j for i in range(r0, r1) for j in range(c0, c1))
            return
        if r1 - r0 >= c1 - c0:
            mid = (r0 + r1) // 2
            rec(r0, mid, c0, c1)
            rec(mid + 1, r1, c0, c1)
            order.extend(mid * m + j for j in range(c0, c1))
        else:
            mid = (c0 + c1) // 2
            rec(r0, r1, c0, mid)
            rec(r0, r1, mid + 1, c1)
            order.extend(i * m + mid for i in range(r0, r1))

    rec(0, m, 0, m)
    return np.array(order)


def fill_in(ms=(16, 32, 64)) -> list[dict]:
    """Nonzeros in the Cholesky factor of the Poisson matrix under four orderings."""
    from scipy.sparse.csgraph import reverse_cuthill_mckee
    rows = []
    for m in ms:
        A = poisson2d(m).tocsc()
        n = A.shape[0]

        def chol_nnz(perm):
            P = A[perm][:, perm].tocsc()
            lu = spla.splu(P, permc_spec="NATURAL", diag_pivot_thresh=0.0, options={"SymmetricMode": True})
            return int(lu.L.nnz)

        rcm = reverse_cuthill_mckee(A.tocsr(), symmetric_mode=True)
        mmd = spla.splu(A, permc_spec="MMD_AT_PLUS_A", diag_pivot_thresh=0.0, options={"SymmetricMode": True})
        rows.append({"m": m, "n": n, "nnz_A": int(A.nnz), "csr_bytes": int(A.nnz * 12 + (n + 1) * 4),
                     "dense_bytes": n * n * 8, "natural": chol_nnz(np.arange(n)), "rcm": chol_nnz(rcm),
                     "min_degree": int(mmd.L.nnz), "nested": chol_nnz(nested_dissection(m))})
    return rows


# ---------------------------------------------------------------- multigrid (1D for the spectrum, 2D for the solver)

def _jacobi(A_diag, A, x, b, w=2 / 3, sweeps=1):
    for _ in range(sweeps):
        x = x + w * (b - A @ x) / A_diag
    return x


def smoothing_spectrum(n: int = 63, sweeps=(0, 1, 3, 10), seed: int = 0) -> dict:
    """1D Poisson: the error's components in the sine basis before and after weighted-Jacobi sweeps: high
    frequencies die in a few sweeps, low ones barely move."""
    rng = np.random.default_rng(seed)
    A = sp.diags([-1.0, 2.0, -1.0], [-1, 0, 1], shape=(n, n)).tocsr()
    d = A.diagonal()
    k = np.arange(1, n + 1)
    S = np.sin(np.outer(np.arange(1, n + 1), k) * np.pi / (n + 1))
    e0 = S @ (rng.standard_normal(n) / 1.0)
    out = {}
    for s in sweeps:
        e = _jacobi(d, A, e0.copy(), np.zeros(n), sweeps=s) if s else e0.copy()
        coef = np.linalg.solve(S, e)
        out[str(s)] = np.abs(coef).tolist()
    return {"n": n, "spectrum": out, "factor": [abs(1 - (2 / 3) * 2 * math.sin(kk * math.pi / (2 * (n + 1))) ** 2
                                                    ) for kk in k]}


def _restrict(r, m):
    """Full weighting from an m x m grid to (m - 1)/2 squared."""
    R = r.reshape(m, m)
    mc = (m - 1) // 2
    out = np.zeros((mc, mc))
    for i in range(mc):
        for j in range(mc):
            I, J = 2 * i + 1, 2 * j + 1
            out[i, j] = (4 * R[I, J] + 2 * (R[I - 1, J] + R[I + 1, J] + R[I, J - 1] + R[I, J + 1])
                         + R[I - 1, J - 1] + R[I - 1, J + 1] + R[I + 1, J - 1] + R[I + 1, J + 1]) / 16
    return out.ravel()


def _prolong(e, mc):
    m = 2 * mc + 1
    E = np.zeros((m + 2, m + 2))
    C = np.zeros((mc + 2, mc + 2))
    C[1:-1, 1:-1] = e.reshape(mc, mc)
    # bilinear interpolation on the fine grid including the zero boundary
    for I in range(1, m + 1):
        for J in range(1, m + 1):
            ci, cj = I / 2, J / 2
            i0, j0 = int(math.floor(ci)), int(math.floor(cj))
            fi, fj = ci - i0, cj - j0
            E[I, J] = ((1 - fi) * (1 - fj) * C[i0, j0] + fi * (1 - fj) * C[min(i0 + 1, mc + 1), j0]
                       + (1 - fi) * fj * C[i0, min(j0 + 1, mc + 1)] + fi * fj * C[min(i0 + 1, mc + 1),
                                                                               min(j0 + 1, mc + 1)])
    return E[1:-1, 1:-1].ravel()


def vcycle(m, x, b, levels):
    A = poisson2d(m)
    d = A.diagonal()
    if m <= 3 or levels == 0:
        return spla.spsolve(A.tocsc(), b)
    x = _jacobi(d, A, x, b, sweeps=2)
    r = b - A @ x
    mc = (m - 1) // 2
    rc = _restrict(r, m) * 4                      # the h^2 scaling of the coarse operator
    ec = vcycle(mc, np.zeros(mc * mc), rc, levels - 1)
    x = x + _prolong(ec, mc)
    return _jacobi(d, A, x, b, sweeps=2)


def multigrid_experiment(ms=(15, 31, 63, 127), cycles: int = 10, seed: int = 0) -> list[dict]:
    rng = np.random.default_rng(seed)
    rows = []
    for m in ms:
        A = poisson2d(m)
        b = rng.standard_normal(m * m)
        x = np.zeros(m * m)
        res = [1.0]
        t0 = time.perf_counter()
        for _ in range(cycles):
            x = vcycle(m, x, b, levels=10)
            res.append(float(np.linalg.norm(b - A @ x) / np.linalg.norm(b)))
        dt = time.perf_counter() - t0
        factors = [res[i + 1] / res[i] for i in range(1, len(res) - 1) if res[i] > 1e-13]
        rows.append({"m": m, "n": m * m, "residuals": res, "factor": float(np.median(factors)), "seconds": dt})
    return rows
