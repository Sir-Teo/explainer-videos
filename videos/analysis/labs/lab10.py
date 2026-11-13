"""Lab 10: measure spectra by invertibility: Gelfand's formula, the Volterra operator, and the shift's lying eigenvalues."""

import math

import numpy as np

from videos.coursekit import labs

TITLE = "The resolvent tells the truth"
GOAL = ("Check Gelfand's formula |A^n|^(1/n) -> max |eigenvalue| on a random non-normal matrix, watch n! |V^n| -> 1/2 "
        "for the Volterra operator (spectrum {0}, no eigenvalue), and see that a finite section of the shift has the "
        "single eigenvalue 0 while its resolvent is enormous on the whole open disc.")
TASKS = [
    "Make the random matrix normal (A = Q diag(d) Q* with Q unitary). How does |A^n|^(1/n) behave now, and why is it constant?",
    "For the shift's section, print the smallest singular value of S - lam at |lam| = 0.9 for N = 20, 40, 80 and compare with 0.9^N.",
    "Apply the truncated vector (1, lam, lam^2, ...) to the backward shift: how small is |(S* - lam) x| / |x|, and what does it say about lam?",
]


def opnorm(M):
    return np.linalg.norm(M, 2)


def volterra(N):
    """The Volterra operator (Vf)(x) = int_0^x f on L^2[0, 1], by the midpoint rule on N cells."""
    return (np.tril(np.ones((N, N)), -1) + 0.5 * np.eye(N)) / N


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Gelfand's spectral radius formula on a random real 8 x 8 matrix (not normal).
    A = rng.normal(size=(8, 8))
    rho = np.abs(np.linalg.eigvals(A)).max()
    ns = np.unique(np.round(np.logspace(0, 3, 40)).astype(int))
    roots = []
    for n in ns:
        P = np.linalg.matrix_power(A / rho, int(n))  # scaled so the powers neither overflow nor underflow
        roots.append(rho * opnorm(P) ** (1 / n))
    roots = np.array(roots)
    assert np.all(roots >= rho * (1 - 1e-9)), "|A^n|^(1/n) is never below the spectral radius"
    assert roots[0] > 1.1 * rho and abs(roots[-1] / rho - 1) < 0.01, "and it converges to it"
    lab.row("random 8 x 8 matrix: |A|, largest |eigenvalue|", f"{roots[0]:.4f}  {rho:.4f}")
    lab.row("|A^n|^(1/n) at n = 10, 100, 1000", "  ".join(f"{roots[np.searchsorted(ns, n)]:.4f}" for n in (10, 100, 1000)))

    # 2. The Volterra operator: norm 2/pi, n! |V^n| -> 1/2, so the spectral radius is 0.
    V = volterra(200)
    norms, P = [], np.eye(200)
    for n in range(1, 13):
        P = P @ V
        norms.append(opnorm(P))
    norms = np.array(norms)
    scaled = norms * np.array([math.factorial(n) for n in range(1, 13)])
    vroots = norms ** (1 / np.arange(1, 13))
    assert abs(norms[0] - 2 / np.pi) < 1e-5, "the Volterra operator has norm 2/pi"
    assert abs(scaled[-1] - 0.5) < 0.03 and np.all(np.diff(np.abs(scaled - 0.5)) < 0), "n! |V^n| -> 1/2"
    assert np.all(np.diff(vroots) < 0) and vroots[-1] < 0.2, "|V^n|^(1/n) -> 0: the spectrum is {0}"
    lab.row("Volterra: |V|", f"{norms[0]:.6f}   (2/pi = {2 / np.pi:.6f})")
    lab.row("Volterra: n! |V^n| at n = 1, 4, 8, 12", "  ".join(f"{scaled[n - 1]:.4f}" for n in (1, 4, 8, 12)) + "   (limit 1/2)")
    lab.row("Volterra: |V^n|^(1/n) at n = 1, 4, 8, 12", "  ".join(f"{vroots[n - 1]:.4f}" for n in (1, 4, 8, 12)) + "   (limit 0)")

    # 3. The shift: an N x N section is a Jordan block with the single eigenvalue 0, but 1/smin(S - lam) is the
    #    size of the resolvent, and it is huge on the whole open disc.
    N = 40
    S = np.diag(np.ones(N - 1), -1)
    assert np.abs(np.linalg.eigvals(S)).max() < 1e-12
    radii = np.linspace(0.05, 1.6, 63)
    phase = np.exp(2j * np.pi * rng.uniform())  # the resolvent norm depends only on |lam|: any direction will do
    smin = {n: np.array([np.linalg.svd(np.diag(np.ones(n - 1), -1) - r * phase * np.eye(n), compute_uv=False)[-1]
                         for r in radii]) for n in (10, 20, 40)}
    inside, outside = radii < 0.8, radii > 1.05
    assert np.all(smin[40][inside] < np.maximum(2 * radii[inside] ** 40, 1e-12)), "inside the disc S - lam is within |lam|^N of singular"
    assert np.all(smin[40][outside] >= radii[outside] - 1 - 1e-9), "outside, |(S - lam) x| >= (|lam| - 1) |x|"
    r_half = np.argmin(np.abs(radii - 0.5))
    lab.row("shift, 40 x 40 section: eigenvalues", "all 0")
    lab.row("smallest singular value of S - lam at |lam| = 0.5", f"{smin[40][r_half]:.2e}   (0.5^40 = {0.5 ** 40:.2e})")
    lab.row("... and at |lam| = 1.6", f"{smin[40][-1]:.4f}   (at least 0.6)")
    lab.note = ("Eigenvalues of a finite section say the shift's spectrum is {0}; the resolvent says every point of "
                "the open disc is within |lam|^N of the spectrum, and in the limit the spectrum is the closed disc. "
                "Gelfand's formula reads the spectral radius off the norms of powers, with or without eigenvectors.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].semilogx(ns, roots, color=labs.BLUE, label="random 8 x 8 matrix: |A^n|^(1/n)")
    ax[0].axhline(rho, color=labs.GOLD, ls="--", label=f"its largest |eigenvalue| = {rho:.3f}")
    ax[0].semilogx(np.arange(1, 13), vroots, "o-", color=labs.GREEN, ms=4, label="Volterra operator: |V^n|^(1/n) -> 0")
    ax[0].set(title="Gelfand's formula", xlabel="n", ylabel="n-th root of the norm of the n-th power", ylim=(0, None))
    ax[0].legend()
    for n, color in ((10, labs.TEAL), (20, labs.PURPLE), (40, labs.RED)):
        ax[1].semilogy(radii, 1 / np.maximum(smin[n], 1e-15), color=color, label=f"N = {n}")
    ax[1].axvline(1, color=labs.MUTED, ls="--", lw=1)
    ax[1].text(1.02, 1e13, "unit circle", color=labs.MUTED, fontsize=9)
    ax[1].text(0.06, 3e15, "capped at 1e15: beyond double precision", color=labs.MUTED, fontsize=9)
    ax[1].set(title="Size of the resolvent of the N x N shift", xlabel="|lambda|", ylabel="norm of (S - lambda)^-1", ylim=(0.5, 1e17))
    ax[1].legend(title="only eigenvalue: 0")
    lab.fig = fig
    return lab
