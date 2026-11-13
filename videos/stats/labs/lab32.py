"""Lab 32: recover a sparse vector from too few equations by l1 and by l2, and find where l1 stops working."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import sparse

TITLE = "Basis pursuit, least norm, and the phase transition"
GOAL = ("Measure a 10-sparse vector of length 200 with 60 random combinations and solve for it by minimum l1 norm and by "
        "minimum l2 norm; then, with half as many equations as unknowns, raise the sparsity until l1 recovery fails and "
        "compare the breaking point with the Donoho-Tanner curve.")
TASKS = [
    "Add noise of SD 0.05 to y and replace basis pursuit by sparse.lasso_cd on standardized columns. How does the error grow with the noise?",
    "Change delta from 0.5 to 0.25 in the phase experiment. Where does sparse.phase_curve put the new breaking point, and do the trials agree?",
    "Make the nonzero entries all +1 instead of random signs, and add the constraint x >= 0 to the linear program. Does the transition move?",
]

P, DELTA = 100, 0.5
RHOS = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    p, n, s = 200, 60, 10
    A = rng.standard_normal((n, p)) / np.sqrt(n)
    x = np.zeros(p)
    x[rng.choice(p, s, replace=False)] = rng.choice([-1.0, 1.0], s) * rng.uniform(1, 2, s)
    y = A @ x
    x1 = sparse.basis_pursuit(A, y)
    x2 = np.linalg.pinv(A) @ y  # the minimum-energy solution
    err1, err2 = (np.linalg.norm(v - x) / np.linalg.norm(x) for v in (x1, x2))
    lab.row("p = 200, n = 60, s = 10: relative error of minimum l1", f"{err1:.1e}   (theory: exact)")
    lab.row("relative error of minimum l2", f"{err2:.0%}   (expected sqrt(1 - n/p) = {np.sqrt(1 - n / p):.0%})")
    lab.row("nonzero entries (above 1e-6)", f"l1: {int(np.sum(np.abs(x1) > 1e-6))}   l2: {int(np.sum(np.abs(x2) > 1e-6))}   truth: {s}")
    assert err1 < 1e-6, "basis pursuit recovers a 10-sparse vector from 60 Gaussian measurements"
    assert abs(err2 - np.sqrt(1 - n / p)) < 0.1 and np.allclose(A @ x2, y), "least norm fits the data and misses the signal"

    rho_star = float(sparse.phase_curve([DELTA])[0])
    rate = sparse.phase_grid(P, [DELTA], RHOS, reps=20, rng=rng)[:, 0]
    lab.row("Donoho-Tanner breaking point at n/p = 0.5", f"s/n = {rho_star:.3f}")
    for r, ok in zip(RHOS, rate):
        lab.row(f"s/n = {r:.1f} (s = {int(round(r * DELTA * P))}): exact recoveries in 20 trials", f"{ok:.0%}")
    assert abs(rho_star - 0.386) < 0.005, "the curve's value at delta = 0.5"
    assert rate[RHOS <= 0.2].min() >= 0.9 and rate[RHOS >= 0.6].max() <= 0.1, "success below the curve, failure above"
    cross = RHOS[np.argmax(rate < 0.5)]
    assert 0.3 <= cross <= 0.5, "the empirical 50% point brackets the asymptotic curve"
    lab.note = ("The l1 solution is the sparse truth to solver precision while the l2 solution spreads over every "
                "coordinate; with n = p/2, recovery switches from nearly always to nearly never around s/n = 0.39.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    idx = np.arange(p)
    ax[0].vlines(idx, 0, x2, color=labs.RED, lw=1, label=f"minimum l2 (error {err2:.0%})")
    ax[0].plot(idx[x != 0], x[x != 0], "o", ms=8, mfc="none", color=labs.MUTED, label="truth (10 nonzero)")
    ax[0].plot(idx[np.abs(x1) > 1e-6], x1[np.abs(x1) > 1e-6], ".", ms=7, color=labs.GOLD, label=f"minimum l1 (error {err1:.0e})")
    ax[0].set(title="200 unknowns from 60 equations", xlabel="coordinate", ylabel="value", ylim=(-2.4, 3.4))
    ax[0].legend(loc="upper center", ncol=3, fontsize=8)
    ax[1].plot(RHOS, rate, "o-", color=labs.BLUE, label="basis pursuit, 20 trials each (p = 100, n = 50)")
    ax[1].axvline(rho_star, color=labs.GOLD, ls="--", label=f"Donoho-Tanner: s/n = {rho_star:.3f}")
    ax[1].set(title="Exact recovery against sparsity, n/p = 0.5", xlabel="sparsity s/n", ylabel="share of exact recoveries",
              ylim=(-0.05, 1.45))
    ax[1].legend(loc="upper right")
    lab.fig = fig
    return lab
