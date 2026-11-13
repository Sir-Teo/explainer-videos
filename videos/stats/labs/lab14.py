"""Lab 14: fit the Challenger flights by logistic regression, then check that a case-control sample keeps the slope."""

import numpy as np
from scipy import optimize

from videos.coursekit import labs
from explainer.stats import museum
from explainer.stats.kit import glm

TITLE = "The Challenger fit, and what sampling on the outcome preserves"
GOAL = ("Fit distress against launch temperature on all 23 flights by IRLS and check it against a direct "
        "maximization; then draw 400 cases and 400 controls from a simulated cohort, 300 times, and compare the "
        "slope and the intercept with what the theory of case-control sampling predicts.")
TASKS = [
    "Fit only the flights at 66 F or warmer. What happens to the slope's standard error and to the interval at 31 F?",
    "Fit the number of distressed rings out of 6 (n_trials=6) instead of any distress. How does p-hat at 31 F per ring compare?",
    "Draw 400 cases and 4,000 controls instead. Predict the intercept shift before you run it.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    # ---- the 23 flights ------------------------------------------------------------------------------------
    temp = np.array(museum.CHALLENGER_TEMP, float)
    y = (np.array(museum.CHALLENGER_DISTRESS) > 0).astype(float)
    X = np.column_stack([np.ones_like(temp), temp])
    fit = glm.logistic(X, y)
    nll = lambda b: float(np.sum(np.logaddexp(0.0, X @ b) - y * (X @ b)))  # noqa: E731
    direct = optimize.minimize(nll, np.zeros(2), method="Nelder-Mead", options={"xatol": 1e-9, "fatol": 1e-12, "maxiter": 4000})
    path = [-nll(b) for b in fit.path]
    line = np.linalg.lstsq(X, y, rcond=None)[0]
    x31 = np.array([1.0, museum.CHALLENGER_LAUNCH_F])
    p31 = float(fit.predict(x31))
    lo, _, hi = fit.predict_ci(x31)
    lab.row("logit p-hat = b0 + b1 T", f"{fit.coef[0]:.2f} {fit.coef[1]:+.3f} T   (direct maximization {direct.x[0]:.2f} {direct.x[1]:+.3f} T)")
    lab.row("log-likelihood after each IRLS step", "  ".join(f"{v:.2f}" for v in path[:5]))
    lab.row("p-hat at 31 F: least squares, logistic", f"{float(x31 @ line):.2f}, {p31:.4f}   (Wald interval on the logit scale [{lo[0]:.2f}, {hi[0]:.2f}])")
    lab.row("odds ratio per 10 F colder", f"{np.exp(-10 * fit.coef[1]):.1f}")
    assert np.allclose(fit.coef, direct.x, atol=2e-3), "IRLS finds the maximum of the likelihood"
    assert all(b >= a - 1e-9 for a, b in zip(path, path[1:])), "every IRLS step raises the likelihood"
    assert abs(fit.coef[0] - 15.04) < 0.01 and abs(fit.coef[1] + 0.232) < 0.001 and abs(path[0] + 15.94) < 0.01
    assert float(x31 @ line) > 1 and 0.999 < p31 < 1, "the line leaves [0, 1]; the logistic curve cannot"

    # ---- a cohort, and case-control samples from it --------------------------------------------------------
    N, b0, b1, m, reps = 200_000, -4.0, 0.5, 400, 300
    x = rng.standard_normal(N)
    d = rng.random(N) < 1 / (1 + np.exp(-(b0 + b1 * x)))
    D = np.column_stack([np.ones(N), x])
    cohort = glm.logistic(D, d.astype(float))
    cases, controls = np.flatnonzero(d), np.flatnonzero(~d)
    shift = np.log((m / len(cases)) / (m / len(controls)))  # log of the ratio of sampling fractions
    cc = np.empty((reps, 2))
    for r in range(reps):
        idx = np.r_[rng.choice(cases, m, replace=False), rng.choice(controls, m, replace=False)]
        cc[r] = glm.logistic(D[idx], d[idx].astype(float)).coef
    slope = cc[:, 1].mean()
    lab.row("cohort of 200,000: cases, slope", f"{len(cases)}, {cohort.coef[1]:.3f}   (truth {b1})")
    lab.row("400 + 400 case-control: mean slope", f"{slope:.3f}   (sd across samples {cc[:, 1].std(ddof=1):.3f})")
    lab.row("intercept shift, case-control minus cohort", f"{cc[:, 0].mean() - cohort.coef[0]:.2f}   (predicted log(pi1/pi0) = {shift:.2f})")
    lab.note = ("Sampling on the outcome moves only the intercept, by the log ratio of the sampling fractions: the "
                "slope, a log odds ratio, is the same in the cohort and in the case-control study.")
    assert abs(slope - cohort.coef[1]) < 0.03 and abs(slope - b1) < 0.06, "the slope survives outcome-dependent sampling"
    assert abs(cc[:, 0].mean() - cohort.coef[0] - shift) < 0.05, "the intercept shifts by log(pi1/pi0)"
    assert abs(cc[:, 0].mean() - cohort.coef[0]) > 3, "and the shift is large: risks cannot be read off"

    fig, ax = labs.figure(2, size=(11, 4.2))
    grid = np.linspace(28, 84, 200)
    G = np.column_stack([np.ones_like(grid), grid])
    jitter = np.where(y > 0, -1, 1) * 0.012 * (np.arange(len(y)) % 4)
    ax[0].scatter(temp, y + jitter, s=22, color=labs.BLUE, zorder=3, label="23 flights (1 = distress)")
    ax[0].plot(grid, fit.predict(G), color=labs.GOLD, label="logistic fit")
    ax[0].plot(grid, G @ line, color=labs.RED, ls="--", label="least squares line")
    ax[0].axvline(31, color=labs.MUTED, ls=":", lw=1)
    ax[0].text(31.8, 0.42, "forecast 31 F", color=labs.MUTED, fontsize=9)
    ax[0].set(title="Challenger: any O-ring distress against temperature", xlabel="launch temperature (F)",
              ylabel="probability of distress", ylim=(-0.35, 1.85))
    ax[0].legend(loc="upper right")
    ax[1].hist(cc[:, 1], bins=30, color=labs.BLUE, alpha=0.7, label="slopes of 300 case-control fits")
    ax[1].axvline(cohort.coef[1], color=labs.GOLD, lw=2, label=f"the cohort's slope {cohort.coef[1]:.3f}")
    ax[1].axvline(b1, color=labs.MUTED, ls="--", lw=1, label=f"truth {b1}")
    ax[1].set(title="Case-control sampling keeps the slope", xlabel="fitted slope (log odds ratio per unit of x)", ylabel="samples")
    ax[1].legend(loc="upper right")
    ax[1].set_ylim(0, ax[1].get_ylim()[1] * 1.35)
    lab.fig = fig
    return lab
