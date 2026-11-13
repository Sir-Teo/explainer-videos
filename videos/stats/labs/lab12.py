"""Lab 12: fit a line two thousand times, and see which standard error tells the truth."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import ols

TITLE = "Least squares under even and uneven noise"
GOAL = ("Simulate y = 1 + 2x + noise two thousand times, first with even noise and then with noise that is large only "
        "where x is above 3, and compare the slope's true spread with the classical and the HC3 standard errors.")
TASKS = [
    "Make the noise t-distributed with 3 degrees of freedom (even variance). Which of the three guarantees survives?",
    "Replace HC3 by HC0 (kind='HC0') at n = 20. How far below 95% does the interval's coverage fall?",
    "Add a point at x = 10 on the line, then off it. Compare its leverage, its residual and Cook's distance.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    n, reps, beta = 60, 2000, 2.0
    x = rng.uniform(0, 4, n)
    X = ols.design(x)
    lab = labs.Lab()
    out = {}
    for name, scale in (("even", np.full(n, 1.0)), ("uneven", 0.1 + 1.2 * x * (x > 3))):
        slopes, se_c, se_r, cover_c, cover_r = [], [], [], 0, 0
        for _ in range(reps):
            f = ols.fit(X, 1 + beta * x + scale * rng.standard_normal(n))
            slopes.append(f.coef[1])
            se_c.append(f.se()[1])
            se_r.append(f.se("HC3")[1])
            lo, hi = f.ci()[1]
            cover_c += lo < beta < hi
            lo, hi = f.ci(kind="HC3")[1]
            cover_r += lo < beta < hi
        out[name] = dict(slopes=np.array(slopes), sd=np.std(slopes), se_c=np.mean(se_c), se_r=np.mean(se_r),
                         cover_c=cover_c / reps, cover_r=cover_r / reps, scale=scale)
        r = out[name]
        lab.row(f"{name} noise: mean slope", f"{r['slopes'].mean():.3f}   (truth {beta})")
        lab.row(f"{name} noise: true sd of the slope", f"{r['sd']:.3f}   classical SE {r['se_c']:.3f}   HC3 SE {r['se_r']:.3f}")
        lab.row(f"{name} noise: 95% interval covers", f"classical {r['cover_c']:.1%}   HC3 {r['cover_r']:.1%}")
    lab.note = ("Uneven noise leaves the slope unbiased but makes the classical standard error too small; "
                "the sandwich estimator tracks the true spread in both worlds.")
    e, u = out["even"], out["uneven"]
    assert abs(e["slopes"].mean() - beta) < 0.02 and abs(u["slopes"].mean() - beta) < 0.03, "unbiased either way"
    assert abs(e["se_c"] / e["sd"] - 1) < 0.06 and abs(e["cover_c"] - 0.95) < 0.02, "classical theory holds"
    assert u["se_c"] / u["sd"] < 0.87 and u["cover_c"] < 0.91, "classical SE understates under heteroskedasticity"
    assert abs(u["cover_r"] - 0.95) < 0.03, "HC3 restores coverage"

    fig, ax = labs.figure(2, size=(11, 4.2))
    y = 1 + beta * x + u["scale"] * rng.standard_normal(n)
    f = ols.fit(X, y)
    grid = np.linspace(0, 4, 50)
    ax[0].scatter(x, y, s=14, color=labs.BLUE, alpha=0.8)
    ax[0].plot(grid, f.predict(ols.design(grid)), color=labs.GOLD, label=f"fit: slope {f.coef[1]:.2f}")
    ax[0].plot(grid, 1 + beta * grid, color=labs.MUTED, ls="--", label="truth: slope 2")
    ax[0].set(title="One sample with uneven noise", xlabel="x", ylabel="y")
    ax[0].legend()
    bins = np.linspace(beta - 4 * u["sd"], beta + 4 * u["sd"], 60)
    ax[1].hist(u["slopes"], bins=bins, density=True, color=labs.BLUE, alpha=0.6, label="2,000 fitted slopes")
    for se, color, name in ((u["se_c"], labs.RED, "classical SE"), (u["se_r"], labs.GREEN, "HC3 SE")):
        ax[1].plot(bins, np.exp(-0.5 * ((bins - beta) / se) ** 2) / (se * np.sqrt(2 * np.pi)), color=color,
                   label=f"normal with the {name}")
    ax[1].set(title="Uneven noise: which standard error matches the spread?", xlabel="fitted slope")
    ax[1].legend()
    lab.fig = fig
    return lab
