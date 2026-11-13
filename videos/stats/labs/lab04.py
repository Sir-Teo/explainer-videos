"""Lab 4: the hat matrix's eigenvalues are 0 and 1, so residual sums of squares average (n - p) sigma^2."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import ols
from explainer.stats.world import World

TITLE = "The hat matrix and degrees of freedom"
GOAL = ("Build the hat matrix of a line fitted to forty of the World's families, check that it is a projection with "
        "p eigenvalues equal to one, and simulate 2,000 data sets on the same design to see the residual sum of "
        "squares average (n - p) sigma^2, for p = 2, 5 and 10.")
TASKS = [
    "Draw the errors from a centred exponential instead of a normal. Which survives: the mean of RSS / sigma^2, or "
    "its chi-squared shape?",
    "Add a column that is the mid-parent height in inches (the same variable in other units). What happens to the "
    "rank, the trace of H and the condition number?",
    "Compare kappa(X) before and after centring the mid-parent heights, and solve both by ols.normal_equations in "
    "float32. How many digits does each keep?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    f = World().families
    n = 40
    idx = rng.choice(len(f["child"]), n, replace=False)
    mid, child = (f["father"][idx] + f["mother"][idx]) / 2, f["child"][idx]
    lab = labs.Lab()

    # 1. The hat matrix of the line: symmetric, idempotent, eigenvalues 0 and 1, trace p.
    X = ols.design(mid)
    fit = ols.fit(X, child)
    H = X @ fit.XtX_inv @ X.T
    eig = np.sort(np.linalg.eigvalsh(H))[::-1]
    p = X.shape[1]
    lab.row("H is symmetric and idempotent", f"max |H - H'| = {np.abs(H - H.T).max():.1e}   max |HH - H| = {np.abs(H @ H - H).max():.1e}")
    lab.row("eigenvalues of H", f"{(eig > 0.5).sum()} ones, {(eig < 0.5).sum()} zeros   trace {np.trace(H):.6f} = p")
    assert np.allclose(H, H.T, atol=1e-10) and np.allclose(H @ H, H, atol=1e-10)
    assert np.allclose(eig[:p], 1, atol=1e-8) and np.allclose(eig[p:], 0, atol=1e-8), "p ones and n - p zeros"
    assert np.allclose(np.diag(H), fit.leverage) and np.isclose(fit.leverage.sum(), p), "leverages sum to p"

    # 2. Simulate on the same design, and on designs with extra columns: E RSS = (n - p) sigma^2.
    sigma, reps = 5.0, 2000
    results = {}
    for p_k in (2, 5, 10):
        Xk = np.column_stack([X, rng.standard_normal((n, p_k - 2))])
        Q, _ = np.linalg.qr(Xk)
        beta = rng.standard_normal(p_k)
        E = sigma * rng.standard_normal((reps, n))
        Y = Xk @ beta + E
        resid = Y - (Y @ Q) @ Q.T  # (I - H) y, with H = Q Q'
        rss = (resid ** 2).sum(1) / sigma ** 2
        fitted_part = ((E @ Q) ** 2).sum(1) / sigma ** 2  # e' H e / sigma^2
        results[p_k] = rss
        lab.row(f"p = {p_k}: mean RSS / sigma^2", f"{rss.mean():.2f}   (n - p = {n - p_k}, n = {n})")
        se = np.sqrt(2 * (n - p_k) / reps)
        assert abs(rss.mean() - (n - p_k)) < 4 * se, "the residual projection has n - p unit eigenvalues"
        assert abs(fitted_part.mean() - p_k) < 4 * np.sqrt(2 * p_k / reps), "and the fitted part has the other p"
    rss = results[2]
    naive, unbiased = (rss / n).mean(), (rss / (n - 2)).mean()
    lab.row("p = 2: RSS / n and RSS / (n - p), in units of sigma^2", f"{naive:.3f} and {unbiased:.3f}   (theory {1 - 2 / n:.3f} and 1)")
    ks = stats.kstest(rss, stats.chi2(n - 2).cdf)
    lab.row("p = 2: RSS / sigma^2 against chi-squared(38)", f"variance {rss.var():.1f} (theory {2 * (n - 2)})   KS p-value {ks.pvalue:.2f}")
    assert abs(naive - (1 - 2 / n)) < 0.02 and abs(unbiased - 1) < 0.02
    assert abs(rss.var() / (2 * (n - 2)) - 1) < 0.15 and ks.pvalue > 1e-3, "a chi-squared with n - p degrees of freedom"

    # 3. Conditioning: forming X'X squares the condition number.
    kx, kxx = np.linalg.cond(X), np.linalg.cond(X.T @ X)
    lab.row("condition numbers", f"kappa(X) = {kx:.0f}   kappa(X'X) = {kxx:.3g} = kappa(X)^2")
    assert np.isclose(kxx, kx ** 2, rtol=1e-4)
    lab.note = ("A projection's eigenvalues are 0 and 1, and degrees of freedom count the ones: the residuals live in "
                "n - p dimensions, so RSS / (n - p), not RSS / n, is centred on sigma^2.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    grid = np.linspace(10, 75, 300)
    ax[0].hist(rss, bins=45, density=True, color=labs.BLUE, alpha=0.6, label="2,000 simulated RSS / sigma^2, p = 2")
    ax[0].plot(grid, stats.chi2(n - 2).pdf(grid), color=labs.GOLD, label="chi-squared, 38 df")
    ax[0].axvline(n - 2, color=labs.GOLD, ls="--", lw=1)
    ax[0].axvline(n, color=labs.RED, ls="--", lw=1, label="n = 40")
    ax[0].set(title="Residual sum of squares on forty families", xlabel="RSS / sigma^2", ylabel="density",
              xlim=(10, 100))
    ax[0].legend(loc="upper right")
    ps = np.array(sorted(results))
    ax[1].plot([0, 12], [n, n - 12], color=labs.GOLD, label="n - p")
    ax[1].axhline(n, color=labs.RED, ls="--", lw=1, label="n")
    ax[1].errorbar(ps, [results[k].mean() for k in ps], yerr=[results[k].std() for k in ps], fmt="o", color=labs.BLUE,
                   capsize=3, label="simulated mean, with one SD of RSS / sigma^2")
    ax[1].set(title="Every fitted column uses up one dimension", xlabel="columns in the design, p",
              ylabel="RSS / sigma^2", xlim=(0, 12))
    ax[1].legend()
    lab.fig = fig
    return lab
