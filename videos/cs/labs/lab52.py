"""Lab 52: separate conditioning from stability on four solvers: elimination, least squares, conjugate gradients, multigrid."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import math

import numpy as np
import scipy.sparse.linalg as spla

from explainer.cs.numeric import iterative, linalg

TITLE = "Which answers to trust: backward error, pivoting, and two fast solvers"
GOAL = ("Solve Hilbert systems and compare the forward error with kappa times the backward error, break elimination "
        "with a tiny pivot and with Wilkinson's matrix, check conjugate gradients against its bound at every step, "
        "and measure multigrid's convergence factor on three grids.")
TASKS = [
    "Call linalg.least_squares() and plot both errors against kappa on log axes. Which method's error grows like kappa and which like kappa squared, and where do the normal equations lose every digit?",
    "Pass M=iterative.ssor(A, 1.5) to iterative.cg. How many steps does it save on the 32 x 32 grid, and what condition number would explain that through the bound?",
    "Add 1e-8 times a Gaussian matrix to linalg.wilkinson_matrix(32) and factor it with linalg.lu. What happens to the growth factor of 2^31, and what does that say about worst cases in practice?",
]


def a_norm(A, e):
    return float(np.sqrt(e @ (A @ e)))


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. forward error <= kappa x backward error: the algorithm is stable, the problem is not
    rows = linalg.forward_vs_backward(seed=seed)
    eps = np.finfo(float).eps
    for r in rows:
        r["bound"] = r["kappa"] * (r["backward"] + eps)  # eps: the right-hand side b = Hx was itself rounded
        assert r["backward"] < 4e-16, "pivoted elimination is backward stable on every size"
        assert r["forward"] <= r["bound"], "forward error is at most kappa times the backward error"
    assert rows[-1]["forward"] > 1e6 * rows[0]["forward"], "the forward error grows with the condition number"
    for r in (rows[0], rows[2], rows[-1]):
        lab.row(f"Hilbert system, n = {r['n']}: kappa {r['kappa']:.1e}",
                f"backward error {r['backward']:.1e}   forward error {r['forward']:.1e}   kappa x (backward + eps) {r['bound']:.1e}")

    # 2. an unstable algorithm on a well-conditioned problem, and the worst case of the stable one
    piv = linalg.pivot_failure()[-1]  # eps = 1e-20
    assert piv["err_no_pivot"] > 0.5 and piv["err_pivot"] < 1e-15
    lab.row("[[1e-20, 1], [1, 1]] x = (1, 2)", f"error without pivoting {piv['err_no_pivot']:.2f}, with partial pivoting "
                                              f"{piv['err_pivot']:.1e}")
    sizes = (8, 16, 32, 48)
    wilk = [float(linalg.lu(linalg.wilkinson_matrix(n))[3]) for n in sizes]
    rand = [[float(linalg.lu(rng.standard_normal((n, n)))[3]) for _ in range(12)] for n in sizes]
    assert wilk == [2.0 ** (n - 1) for n in sizes], "Wilkinson's matrix attains the bound 2^(n-1)"
    assert max(max(r) for r in rand) < 30, "random matrices grow by a small factor"
    lab.row("growth factor at n = 48", f"Wilkinson's matrix {wilk[-1]:.2e} = 2^47; 12 random matrices: mean "
                                       f"{np.mean(rand[-1]):.1f}, largest {max(rand[-1]):.1f}")

    # 3. conjugate gradients on the 16 x 16 Poisson problem against its bound, step by step
    m = 16
    A = iterative.poisson2d(m)
    b = rng.standard_normal(m * m)
    exact = spla.spsolve(A.tocsc(), b)
    kappa = 1 / math.tan(math.pi / (2 * (m + 1))) ** 2  # lambda_max / lambda_min of the five-point Laplacian
    rate = (math.sqrt(kappa) - 1) / (math.sqrt(kappa) + 1)
    e0 = a_norm(A, exact)
    ks = list(range(1, 46))
    err = [a_norm(A, exact - iterative.cg(A, b, tol=0.0, max_iter=k)[0]) / e0 for k in ks]
    bound = [2 * rate ** k for k in ks]
    assert all(e <= bd * (1 + 1e-9) for e, bd in zip(err, bound)), "CG's error is under 2 ((sqrt k - 1)/(sqrt k + 1))^k"
    _, h_cg = iterative.cg(A, b)
    _, h_sd = iterative.steepest(A, b)
    assert len(h_sd) > 8 * len(h_cg)
    lab.row(f"Poisson, 256 unknowns, kappa {kappa:.0f}: steps to 1e-8", f"steepest descent {len(h_sd) - 1}, conjugate "
            f"gradients {len(h_cg) - 1}; A-norm error after 30 steps {err[29]:.1e}, bound {bound[29]:.1e}")

    # 4. multigrid: the same factor per cycle on every grid
    mg = iterative.multigrid_experiment(ms=(15, 31, 63), cycles=8, seed=seed)
    factors = [r["factor"] for r in mg]
    assert max(factors) < 0.3 and max(factors) - min(factors) < 0.05, "the V-cycle's rate does not depend on the grid"
    lab.row("multigrid V-cycle, residual factor per cycle", ", ".join(f"{r['n']:,} unknowns: {r['factor']:.2f}" for r in mg))
    lab.note = ("A backward error near rounding level on every Hilbert system says the solver is stable; the lost "
                "digits belong to the problem. CG's steps grow like the square root of kappa, and multigrid's do "
                "not grow at all.")

    fig, ax = labs.figure(2, size=(11, 4.3))
    ns = [r["n"] for r in rows]
    ax[0].semilogy(ns, [r["bound"] for r in rows], "o--", color=labs.MUTED, label="kappa x (backward error + eps)")
    ax[0].semilogy(ns, [r["forward"] for r in rows], "o-", color=labs.RED, label="forward error")
    ax[0].semilogy(ns, [max(r["backward"], 1e-18) for r in rows], "o-", color=labs.GREEN, label="backward error")
    ax[0].set(title="Hilbert systems: a stable solver, an ill-conditioned problem", xlabel="matrix size n",
              ylabel="relative error")
    ax[0].legend()
    ax[1].semilogy(ks, bound, color=labs.MUTED, ls="--", label="CG's bound")
    ax[1].semilogy(ks, err, color=labs.GOLD, label="conjugate gradients, A-norm error")
    ax[1].semilogy(range(len(h_sd[:46])), h_sd[:46], color=labs.ORANGE, label="steepest descent, residual")
    for r, color in zip(mg, (labs.BLUE, labs.TEAL, labs.PURPLE)):
        ax[1].semilogy(range(len(r["residuals"])), r["residuals"], "o-", ms=3, color=color,
                       label=f"multigrid, {r['n']:,} unknowns")
    ax[1].set(title="Poisson's equation: error against steps or cycles", xlabel="step (CG, descent) or V-cycle",
              ylabel="relative error or residual", ylim=(1e-9, 3))
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
