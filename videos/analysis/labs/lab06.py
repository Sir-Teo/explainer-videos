"""Lab 6: project e^x onto the quadratics in L^2[0, 1] two ways, and fill Bessel's bar for the sign function."""

import numpy as np
from scipy.special import eval_legendre

from videos.coursekit import labs

TITLE = "The nearest quadratic, and Pythagoras with many sides"
GOAL = ("Find the point of span{1, x, x^2} nearest to e^x in L^2[0, 1] from the normal equations and from an "
        "orthonormal basis, check that the error is perpendicular to the subspace and that no other quadratic is "
        "closer, then expand the sign function in Legendre polynomials and watch Bessel's sum climb toward 2.")
TASKS = [
    "Raise the degree from 2 to 8 and print the condition number of the Hilbert matrix beside the error of each method.",
    "Measure the distance in L^1 instead of L^2 (integrate |f - q|). Is the L^2 projection still the nearest quadratic?",
    "Drop e_1 from the Legendre basis and expand f(x) = x: every coefficient is 0. Which line of Parseval's proof fails?",
]

X, W = np.polynomial.legendre.leggauss(60)  # Gauss-Legendre nodes and weights on [-1, 1]
T, WT = (X + 1) / 2, W / 2  # ... and on [0, 1]


def inner(f, g):
    """The inner product of L^2[0, 1], for smooth f and g given as values at the nodes T."""
    return float(np.sum(WT * f * g))


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    f = np.exp(T)
    powers = np.array([T**k for k in range(3)])

    # 1. The normal equations: the error is perpendicular to 1, x, x^2.  Their matrix is the Hilbert matrix.
    hilbert = np.array([[1 / (i + j + 1) for j in range(3)] for i in range(3)])
    rhs = np.array([np.e - 1, 1.0, np.e - 2])  # the integrals of e^x, x e^x, x^2 e^x over [0, 1]
    coef = np.linalg.solve(hilbert, rhs)
    proj = coef @ powers

    # 2. An orthonormal basis of the same subspace: the shifted Legendre polynomials.
    basis = np.array([np.sqrt(2 * n + 1) * eval_legendre(n, 2 * T - 1) for n in range(3)])
    c = np.array([inner(f, e) for e in basis])
    proj_on = c @ basis
    assert np.allclose(proj, proj_on, atol=1e-10), "the two constructions give the same point"

    err = proj - f
    perp = [inner(err, p) for p in powers]
    assert max(abs(v) for v in perp) < 1e-12, "the error is perpendicular to the subspace"
    dist = np.sqrt(inner(err, err))
    norm2 = (np.e**2 - 1) / 2
    assert abs(norm2 - (np.sum(c**2) + dist**2)) < 1e-12, "Pythagoras: |f|^2 = |Pf|^2 + |f - Pf|^2"

    # 3. Nearest: 2,000 other quadratics, and Taylor's, are all farther away.
    others = coef + rng.normal(0, 0.05, (2000, 3))
    d_others = np.sqrt(np.sum(WT * (others @ powers - f) ** 2, axis=1))
    taylor = 1 + T + T**2 / 2
    d_taylor = np.sqrt(inner(taylor - f, taylor - f))
    assert d_others.min() > dist and d_taylor > 10 * dist, "the projection is the nearest point"
    # each perturbed quadratic q = Pf + d obeys Pythagoras again: |q - f|^2 = |d|^2 + |Pf - f|^2
    d_pert = np.sqrt(np.sum(WT * ((others - coef) @ powers) ** 2, axis=1))
    assert np.allclose(d_others**2, d_pert**2 + dist**2, atol=1e-12)

    lab.row("best quadratic", f"{coef[0]:.4f} + {coef[1]:.4f} x + {coef[2]:.4f} x^2")
    lab.row("<error, 1>, <error, x>, <error, x^2>", "  ".join(f"{v:+.1e}" for v in perp))
    lab.row("distance from e^x: projection", f"{dist:.5f}")
    lab.row("distance from e^x: Taylor 1 + x + x^2/2", f"{d_taylor:.5f}   ({d_taylor / dist:.1f} times the projection's)")
    lab.row("nearest of 2,000 perturbed quadratics", f"{d_others.min():.5f}   (never below {dist:.5f})")

    # 4. Bessel: the sign function on [-1, 1] in the normalized Legendre polynomials e_n = sqrt((2n+1)/2) P_n.
    N = 41
    n = np.arange(N)
    # <sign, e_n> = 2 sqrt((2n+1)/2) int_0^1 P_n for odd n (0 for even n); int_0^1 P_n = (P_{n-1}(0) - P_{n+1}(0)) / (2n+1)
    half = np.where(n % 2 == 1, (eval_legendre(np.maximum(n - 1, 0), 0.0) - eval_legendre(n + 1, 0.0)) / (2 * n + 1), 0.0)
    b = 2 * np.sqrt((2 * n + 1) / 2) * half
    bessel = np.cumsum(b**2)
    grid = (np.arange(200000) + 0.5) / 100000 - 1  # midpoints: the squared error by direct integration
    s = sum(b[k] * np.sqrt((2 * k + 1) / 2) * eval_legendre(k, grid) for k in range(N) if b[k])
    err2 = float(np.mean((np.sign(grid) - s) ** 2) * 2)
    assert abs(b[1] ** 2 - 1.5) < 1e-12 and np.all(np.diff(bessel) >= 0) and bessel[-1] < 2, "Bessel's inequality"
    assert abs(bessel[-1] + err2 - 2) < 1e-3, "the leftover of Bessel's sum is the squared error"
    lab.row("Bessel's sum for sign, 1 / 3 / 5 odd terms", "  ".join(f"{bessel[k]:.3f}" for k in (1, 5, 9)) + "   (bound 2)")
    lab.row("Bessel's sum with e_0 ... e_40", f"{bessel[-1]:.4f}   squared error by integration {err2:.4f}   sum {bessel[-1] + err2:.4f}")
    lab.note = ("The error of the projection is perpendicular to the subspace, so every other quadratic is farther "
                "by Pythagoras; for the sign function the same right triangle makes Bessel's sum plus the squared "
                "error equal 2, with the sum creeping up because the function has a jump.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    t = np.linspace(0, 1, 300)
    ax[0].axhline(0, color=labs.MUTED, lw=0.8)
    ax[0].plot(t, coef[0] + coef[1] * t + coef[2] * t**2 - np.exp(t), color=labs.GOLD, label=f"projection (L2 error {dist:.4f})")
    ax[0].plot(t, 1 + t + t**2 / 2 - np.exp(t), color=labs.RED, label=f"Taylor at 0 (L2 error {d_taylor:.4f})")
    ax[0].set(title="Quadratic minus e^x on [0, 1]", xlabel="x", ylabel="error", ylim=(-0.23, 0.05))
    ax[0].legend(loc="lower left")
    ax[1].step(n, bessel, where="post", color=labs.BLUE, label="sum of squared coefficients")
    ax[1].fill_between(n, bessel, 2, step="post", color=labs.RED, alpha=0.25, label="squared error of the partial sum")
    ax[1].axhline(2, color=labs.GOLD, ls="--", label="squared norm of sign: 2")
    ax[1].set(title="Bessel's bar for the sign function", xlabel="highest Legendre degree used", ylim=(0, 2.15))
    ax[1].legend(loc="lower right")
    lab.fig = fig
    return lab
