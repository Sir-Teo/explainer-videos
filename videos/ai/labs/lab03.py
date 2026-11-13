"""Lab 3: find the top singular direction by power iteration, and test Eckart-Young against random competitors."""

import numpy as np

from videos.coursekit import labs

TITLE = "Power iteration and the best low-rank copy"
GOAL = ("Build a 60 x 80 matrix with six strong directions under noise. Run power iteration on its Gram matrix and "
        "compare the measured convergence rate with the eigenvalue ratio; then check that the rank-k truncation of "
        "the SVD has error equal to the dropped singular values and beats 400 other rank-k matrices.")
TASKS = [
    "Set the two largest singular values to 10 and 9.9. How many steps does power iteration now need, and what "
    "does the Rayleigh quotient still get right?",
    "Raise the noise from 0.3 to 3. At what rank does the error curve stop falling quickly, and why?",
    "Replace the Frobenius norm by the spectral norm (np.linalg.norm(X, 2)) and check that the rank-k error is "
    "the next singular value.",
]
STRONG = np.array([10.0, 8.0, 6.0, 4.5, 3.0, 2.0])


def orthonormal(rng, n, k):
    return np.linalg.qr(rng.standard_normal((n, k)))[0]


def run(seed=0):
    rng = np.random.default_rng(seed)
    m, n, steps = 60, 80, 45
    A = orthonormal(rng, m, 6) @ np.diag(STRONG) @ orthonormal(rng, n, 6).T + 0.3 * rng.standard_normal((m, n)) / np.sqrt(n)
    U, sig, Vt = np.linalg.svd(A, full_matrices=False)  # the reference: LAPACK's SVD
    lab = labs.Lab()

    # Power iteration on G = A^T A, whose eigenvalues are the squared singular values.
    G, x = A.T @ A, rng.standard_normal(n)
    x /= np.linalg.norm(x)
    angle, gap = [], []
    for _ in range(steps):
        x = G @ x
        x /= np.linalg.norm(x)
        angle.append(np.linalg.norm(x - (x @ Vt[0]) * Vt[0]))  # the sine of the angle to the true direction
        gap.append(sig[0] ** 2 - x @ G @ x)  # the Rayleigh quotient, from below
    angle, gap, t = np.array(angle), np.array(gap), np.arange(1, steps + 1)
    window = slice(8, 28)  # after the transient, before round-off
    rate = np.exp(np.polyfit(t[window], np.log(angle[window]), 1)[0])
    rate_rq = np.exp(np.polyfit(t[window], np.log(gap[window]), 1)[0])
    ratio = (sig[1] / sig[0]) ** 2
    lab.row("largest singular values", f"{sig[0]:.3f}, {sig[1]:.3f}   (eigenvalue ratio of the Gram matrix {ratio:.4f})")
    lab.row("power iteration: error factor per step", f"{rate:.4f}   (predicted {ratio:.4f})")
    lab.row("Rayleigh quotient: error factor per step", f"{rate_rq:.4f}   (predicted {ratio ** 2:.4f}, the square)")
    lab.row("singular value from the Rayleigh quotient", f"{np.sqrt(x @ G @ x):.10f}   (SVD {sig[0]:.10f})")
    assert abs(rate / ratio - 1) < 0.03, "the direction converges at lambda_2 / lambda_1"
    assert abs(rate_rq / ratio ** 2 - 1) < 0.05, "the Rayleigh quotient converges at the squared rate"
    assert abs(np.sqrt(x @ G @ x) - sig[0]) < 1e-8

    # Eckart-Young: the truncated SVD against other rank-k matrices.
    total = (sig ** 2).sum()
    ranks = np.arange(0, 13)
    svd_err, random_err, near_err = [], [], []
    for k in ranks:
        Ak = (U[:, :k] * sig[:k]) @ Vt[:k]
        err = np.linalg.norm(A - Ak, "fro") ** 2
        assert abs(err - (sig[k:] ** 2).sum()) < 1e-9 * total, "the error is the tail of the singular values"
        svd_err.append(err)
        if k == 0:
            random_err.append(err)
            near_err.append(err)
            continue
        rivals, near = [], []
        for _ in range(200):
            Q = orthonormal(rng, m, k)  # the best copy of A whose columns lie in a random k-dimensional subspace
            rivals.append(np.linalg.norm(A - Q @ (Q.T @ A), "fro") ** 2)
            Q = np.linalg.qr(U[:, :k] + 0.01 * rng.standard_normal((m, k)))[0]  # ... and in a nudged optimal one
            near.append(np.linalg.norm(A - Q @ (Q.T @ A), "fro") ** 2)
        assert min(rivals) > err and min(near) > err, "no rank-k competitor beats the truncated SVD"
        random_err.append(np.mean(rivals))
        near_err.append(np.min(near))
    svd_err, random_err, near_err = (np.array(v) / total for v in (svd_err, random_err, near_err))
    lab.row("rank 6: squared error / total", f"{svd_err[6]:.5f}   (dropped singular values {(sig[6:] ** 2).sum() / total:.5f})")
    lab.row("rank 6: best of 200 nudged rivals", f"{near_err[6]:.5f};   random subspaces average {random_err[6]:.3f}")
    assert svd_err[6] < 0.02 < svd_err[3], "six directions carry the matrix; three do not"
    lab.note = ("Multiplying by the matrix over and over finds its top direction at the rate set by the ratio of the "
                "top two eigenvalues, and cutting the SVD at rank k leaves exactly the dropped singular values as "
                "error, which no other rank-k matrix improves on.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].semilogy(t, angle, color=labs.BLUE, label="angle to the top direction (sine)")
    ax[0].semilogy(t, np.maximum(gap, 1e-15) / sig[0] ** 2, color=labs.GOLD, label="Rayleigh quotient's relative gap")
    ax[0].semilogy(t, angle[8] * ratio ** (t - 9.0), "--", color=labs.MUTED, lw=1, label=r"slopes $\lambda_2/\lambda_1$ and its square")
    ax[0].semilogy(t, gap[8] / sig[0] ** 2 * ratio ** (2 * (t - 9.0)), "--", color=labs.MUTED, lw=1)
    ax[0].set(title="Power iteration on the Gram matrix", xlabel="step", ylabel="error", ylim=(1e-17, 3))
    ax[0].legend(loc="upper right")
    ax[1].plot(ranks, random_err, "o-", ms=4, color=labs.RED, label="random k-dimensional subspace (mean of 200)")
    ax[1].plot(ranks, near_err, "o-", ms=4, color=labs.BLUE, label="nudged optimal subspace (best of 200)")
    ax[1].plot(ranks, svd_err, "o-", ms=4, color=labs.GREEN, label="truncated SVD = dropped singular values")
    ax[1].set(title="Squared error of rank-k copies, as a share of the whole", xlabel="rank k", ylabel="relative squared error",
              yscale="log")
    ax[1].legend(loc="center right")
    lab.fig = fig
    return lab
