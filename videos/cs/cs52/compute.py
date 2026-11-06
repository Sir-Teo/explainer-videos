"""Precompute everything numerical in Part 52 of *Computer Science, Built* ("Computing with Real Numbers").

    python -m videos.cs.cs52.compute              # everything missing
    python -m videos.cs.cs52.compute --force qr

Results are cached in ``.cache/cs52/<name>.json`` (arrays as .npz); scenes call ``load(name)``.  The instruments
are in ``explainer/cs/numeric/`` (linalg, eigen, iterative, analysis, speed); tests in tests/test_cs52_numeric.py.

Items:
    cond        condition numbers of functions and of Hilbert matrices
    backward    forward against backward error on Hilbert systems: forward <= kappa x backward
    pivot       [[eps, 1], [1, 1]] without and with partial pivoting
    growth      growth factors: 2^(n-1) on Wilkinson's matrix, small on random ones
    smoothed    Wilkinson's matrix perturbed by sigma: the worst case vanishes
    mirrors     Householder QR of a small matrix, each mirror kept for drawing
    ortho       loss of orthogonality: classical and modified Gram-Schmidt against Householder
    lsq         least squares: the normal equations square kappa, QR does not
    svd         deblurring by truncated SVD: the best rank against the naive solve
    qr          the QR algorithm, unshifted against Wilkinson-shifted: iterations, subdiagonal decay, cubic order
    krylov      steepest descent, CG, Jacobi- and SSOR-preconditioned CG on the Poisson problem; CG's bound
    gmres       GMRES on a nonsymmetric convection-diffusion problem
    fill        Cholesky fill-in under four orderings; CSR storage
    spectrum    weighted-Jacobi smoothing of the error's sine modes
    multigrid   V-cycle convergence factors, independent of the grid
    roots       digits per iteration: bisection, secant, Newton
    fractal     Newton's method for z^3 - 1: basins, and two zooms
    runge       Runge's phenomenon: equispaced against Chebyshev points
    quad        trapezoid, Simpson, Gauss, Monte Carlo; adaptive Simpson
    stiff       explicit RK45 against backward Euler as stiffness grows
    stability   stability regions of Euler, RK4 and backward Euler
    kepler      a thousand Kepler orbits: RK4 against leapfrog energy
    blas        BLAS levels 1, 2 and 3 timed on this machine
    refine      mixed-precision iterative refinement
    rsvd        randomized SVD against the optimal rank-k error and a full SVD
"""

from __future__ import annotations

from explainer.ai.cache import Cache

CACHE = Cache("cs52")
load = CACHE.load


def compute_cond() -> dict:
    from explainer.cs.numeric import linalg as L
    return L.cond_examples()


def compute_backward() -> dict:
    from explainer.cs.numeric import linalg as L
    return {"rows": L.forward_vs_backward()}


def compute_pivot() -> dict:
    from explainer.cs.numeric import linalg as L
    return {"rows": L.pivot_failure()}


def compute_growth() -> dict:
    from explainer.cs.numeric import linalg as L
    return {"rows": L.growth()}


def compute_smoothed() -> dict:
    from explainer.cs.numeric import linalg as L
    return {"rows": L.smoothed_growth()}


def compute_mirrors() -> dict:
    import numpy as np
    from explainer.cs.numeric import linalg as L
    A = np.array([[3.0, 1.0, 2.0], [4.0, 2.0, 1.0], [0.0, 2.0, 5.0]])
    Q, R, mirrors = L.householder(A, keep=True)
    A2 = np.array([[3.0, 1.0], [4.0, 3.0]])
    Q2, R2, m2 = L.householder(A2, keep=True)
    return {"A": A.tolist(), "Q": Q.tolist(), "R": R.tolist(), "mirrors": mirrors, "A2": A2.tolist(),
            "R2": R2.tolist(), "mirror2": m2, "givens_rotations": L.givens(A)[2]}


def compute_ortho() -> dict:
    from explainer.cs.numeric import linalg as L
    return {"rows": L.orthogonality()}


def compute_lsq() -> dict:
    from explainer.cs.numeric import linalg as L
    return {"rows": L.least_squares()}


def compute_svd() -> dict:
    from explainer.cs.numeric import linalg as L
    return L.svd_regularize()


def compute_qr() -> dict:
    from explainer.cs.numeric import eigen as E
    return E.qr_experiment()


def compute_krylov() -> dict:
    from explainer.cs.numeric import iterative as I
    return I.krylov_experiment()


def compute_gmres() -> dict:
    from explainer.cs.numeric import iterative as I
    return I.gmres_demo()


def compute_fill() -> dict:
    from explainer.cs.numeric import iterative as I
    return {"rows": I.fill_in()}


def compute_spectrum() -> dict:
    from explainer.cs.numeric import iterative as I
    return I.smoothing_spectrum()


def compute_multigrid() -> dict:
    from explainer.cs.numeric import iterative as I
    return {"rows": I.multigrid_experiment()}


def compute_roots() -> dict:
    from explainer.cs.numeric import analysis as A
    return A.root_race()


def compute_fractal() -> dict:
    from explainer.cs.numeric import analysis as A
    out = {}
    for name, c, w in (("full", (0.0, 0.0), 3.0), ("zoom1", (-0.5, 0.29), 0.2), ("zoom2", (-0.535, 0.306), 0.01)):
        r = A.newton_fractal(n=360, center=c, width=w)
        out[name + "_which"] = r["which"]
        out[name + "_steps"] = r["steps"]
        out[name + "_meta"] = {"center": list(c), "width": w, "unconverged": r["unconverged"]}
    return out


def compute_runge() -> dict:
    from explainer.cs.numeric import analysis as A
    return A.runge()


def compute_quad() -> dict:
    from explainer.cs.numeric import analysis as A
    r = A.quadrature()
    return {"exact": r["exact"], "adaptive": {k: float(v) for k, v in r["adaptive"].items()},
            "rows": [{k: (None if v is None else float(v)) for k, v in row.items()} for row in r["rows"]]}


def compute_stiff() -> dict:
    from explainer.cs.numeric import analysis as A
    return {"rows": A.stiffness()}


def compute_stability() -> dict:
    from explainer.cs.numeric import analysis as A
    return A.stability_regions()


def compute_kepler() -> dict:
    from explainer.cs.numeric import analysis as A
    return A.kepler()


def compute_blas() -> dict:
    from explainer.cs.numeric import speed as P
    return {"rows": P.blas_levels()}


def compute_refine() -> dict:
    from explainer.cs.numeric import speed as P
    return {"rows": P.refinement()}


def compute_rsvd() -> dict:
    from explainer.cs.numeric import linalg as L
    return L.randomized_svd()


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
