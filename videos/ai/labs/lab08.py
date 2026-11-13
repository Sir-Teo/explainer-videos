"""Lab 8: watch gradient descent land on the minimum-norm fit, then find the double-descent peak at p = n."""

import numpy as np

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor

TITLE = "The smallest fit, and the peak at the interpolation threshold"
GOAL = ("Run gradient descent from zero on 20 equations in 60 unknowns and compare it with the pseudoinverse; then fit "
        "p random ReLU features to n = 40 noisy examples by the minimum-norm rule and trace the test error as p passes n.")
TASKS = [
    "Set the label noise to 0. What is left of the peak at p = n, and which factor in the noise formula explains it?",
    "Fix p = 40 features and vary the number of examples n from 10 to 160. Where does more data make the test error worse?",
    "Start gradient descent from a random point instead of zero, and show that the weights it forgets to remove are orthogonal to every row of X.",
]


def descend(X, y, w0, steps=1500):
    """Gradient descent on half the squared error, with the gradient from the series' autodiff."""
    w = Tensor(w0.copy(), requires_grad=True)
    eta = 1 / np.linalg.eigvalsh(X @ X.T)[-1]  # 1 / the largest squared singular value
    for _ in range(steps):
        w.grad[:] = 0
        r = Tensor(X) @ w - y
        ((r * r).sum() * 0.5).backward()
        w.data -= eta * w.grad
    return w.data


def features(x, A, b):
    return np.maximum(x @ A + b, 0) / np.sqrt(A.shape[1])


def min_norm(F, y, ridge=1e-10):
    """Least squares on F's columns; beyond p = n the fit of smallest norm, F'(FF')^-1 y.  (ridge > 0: ridge regression.)"""
    n, p = F.shape
    if p <= n:
        return np.linalg.solve(F.T @ F + ridge * np.eye(p), F.T @ y)
    return F.T @ np.linalg.solve(F @ F.T + ridge * np.eye(n), y)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. implicit bias: gradient descent from zero stays in the row space and stops at X^+ y
    X, y = rng.standard_normal((20, 60)), rng.standard_normal(20)
    pinv = X.T @ np.linalg.inv(X @ X.T)  # X+ for a wide matrix of full row rank
    w_min = pinv @ y
    w_gd = descend(X, y, np.zeros(60))
    start = rng.standard_normal(60)
    w_far = descend(X, y, start)
    null_part = start - pinv @ (X @ start)  # the start's component outside the row space
    d_zero, d_far = np.linalg.norm(w_gd - w_min), np.linalg.norm(w_far - w_min)
    lab.row("GD from zero: distance to the min-norm fit X+ y", f"{d_zero:.1e}   (residual {np.abs(X @ w_gd - y).max():.1e})")
    lab.row("GD from a random start: distance to X+ y", f"{d_far:.4f}   (the start's null-space part: {np.linalg.norm(null_part):.4f})")
    assert d_zero < 1e-8, "from zero, gradient descent finds the minimum-norm interpolant"
    assert abs(d_far - np.linalg.norm(null_part)) < 1e-8, "what gradient descent cannot see, it leaves untouched"

    # 2. double descent: least squares on p random ReLU features, minimum norm beyond p = n
    n, d, noise, draws = 40, 8, 0.5, 30
    ps = np.array([4, 8, 12, 16, 20, 26, 32, 36, 39, 40, 41, 44, 50, 60, 80, 120, 200, 400])
    beta = rng.standard_normal(d) / np.sqrt(d)
    err, err_ridge, smin = (np.zeros((draws, len(ps))) for _ in range(3))
    for k in range(draws):
        xtr, xte = rng.standard_normal((n, d)), rng.standard_normal((200, d))
        ytr, yte = xtr @ beta + noise * rng.standard_normal(n), xte @ beta
        A, b = rng.standard_normal((d, ps.max())), rng.standard_normal(ps.max())
        for j, p in enumerate(ps):
            F, G = features(xtr, A[:, :p], b[:p]), features(xte, A[:, :p], b[:p])
            err[k, j] = np.mean((G @ min_norm(F, ytr) - yte) ** 2)
            err_ridge[k, j] = np.mean((G @ min_norm(F, ytr, ridge=0.1) - yte) ** 2)
            gram = F.T @ F if p <= n else F @ F.T  # its eigenvalues are the squared singular values
            smin[k, j] = np.sqrt(max(np.linalg.eigvalsh(gram)[0], 0.0))
    med, med_ridge, med_smin = np.median(err, 0), np.median(err_ridge, 0), np.median(smin, 0)
    at_n = int(np.flatnonzero(ps == n)[0])
    bottom = med[:at_n].min()
    lab.row("test error at the U's bottom (p < n)", f"{bottom:.3f}   at p = {ps[np.argmin(med[:at_n])]}")
    lab.row("test error at p = n = 40", f"{med[at_n]:.1f}   (ridge 0.1: {med_ridge[at_n]:.3f})")
    lab.row("test error at p = 400", f"{med[-1]:.3f}")
    lab.row("smallest singular value of the features", f"{med_smin[at_n]:.4f} at p = n   ({med_smin[at_n - 4]:.3f} at p = {ps[at_n - 4]}, {med_smin[-1]:.3f} at p = 400)")
    lab.note = ("The minimum-norm fit divides the noise by each singular value; at p = n the smallest one is nearly "
                "zero, so the error peaks there and falls again as more features push the spectrum away from zero.")
    assert np.argmax(med) == at_n and med[at_n] > 5 * bottom, "the peak sits at the interpolation threshold"
    assert med[-1] < med[at_n] / 5, "past the threshold the error comes back down"
    assert np.argmin(med_smin) == at_n, "the smallest singular value is smallest at p = n"
    assert med_ridge[at_n] < med[at_n] / 5, "a little ridge removes the peak"

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].loglog(ps, med, "o-", color=labs.GOLD, ms=4, label="minimum-norm least squares")
    ax[0].loglog(ps, med_ridge, "o-", color=labs.BLUE, ms=3, label="ridge, penalty 0.1")
    ax[0].axvline(n, color=labs.MUTED, ls=":", lw=1)
    ax[0].text(n * 1.08, med.max() * 0.6, "p = n", color=labs.MUTED)
    ax[0].set(title="Test error against the number of features", xlabel="random ReLU features p (n = 40 examples)",
              ylabel="test mean squared error (median of 30 draws)")
    ax[0].legend(loc="upper left")
    ax[1].loglog(ps, med_smin, "o-", color=labs.RED, ms=4)
    ax[1].axvline(n, color=labs.MUTED, ls=":", lw=1)
    ax[1].set(title="Why: the smallest singular value touches zero at p = n", xlabel="random ReLU features p",
              ylabel="smallest singular value of the feature matrix")
    lab.fig = fig
    return lab
