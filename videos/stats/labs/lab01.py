"""Lab 1: find the centre of a sample by minimizing a loss, then watch the sample mean itself vary."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.world import World

TITLE = "Centres as minimizers, and a statistic that is random"
GOAL = ("Draw 200 incomes from the World and find, by brute force, the c that minimizes the sum of |x - c|^p: it is "
        "the median at p = 1 and the mean at p = 2. Then draw 2,000 samples of 100 heights and compare the spread of "
        "their means with sigma / sqrt(n).")
TASKS = [
    "Replace the largest income in the sample by ten times its value. Which of the centres move, and by how much?",
    "Change the sample size of the height samples from 100 to 400. By what factor does the spread of the means fall?",
    "Repeat the second half with the sample median of incomes instead of the mean of heights. Is its spread still "
    "sigma / sqrt(n)?",
]


def lp_centre(x, p, grid):
    """The grid point c that minimizes sum |x_i - c|^p (brute force: every candidate is tried)."""
    loss = (np.abs(x[:, None] - grid[None, :]) ** p).sum(0)
    return grid[np.argmin(loss)], loss


def run(seed=0):
    rng = np.random.default_rng(seed)
    w = World()
    lab = labs.Lab()

    # 1. Centres of 200 incomes (in thousands) as minimizers of a loss.
    income = w.income[w.adult] / 1000
    x = np.sort(rng.choice(income, 200, replace=False))
    grid = np.linspace(x[0], x[-1], 20001)
    step = grid[1] - grid[0]
    c1, loss1 = lp_centre(x, 1, grid)
    c2, loss2 = lp_centre(x, 2, grid)
    c8, _ = lp_centre(x, 8, grid)
    mean, median, midrange = x.mean(), np.median(x), (x[0] + x[-1]) / 2
    lab.row("p = 1: brute-force minimizer", f"{c1:.2f}   median {median:.2f}   (n even: any c in [{x[99]:.2f}, {x[100]:.2f}])")
    lab.row("p = 2: brute-force minimizer", f"{c2:.2f}   mean {mean:.2f}")
    lab.row("p = 8: brute-force minimizer", f"{c8:.2f}   midrange {midrange:.2f}")
    assert x[99] - step <= c1 <= x[100] + step, "absolute loss is minimized between the two middle values"
    assert abs(c2 - mean) <= step, "squared loss is minimized at the mean"
    assert median < mean < c8 < midrange, "on right-skewed data the centre slides toward the midrange as p grows"

    # 2. Pythagoras: the squared loss at any c is the loss at the mean plus n (mean - c)^2.
    lhs = ((x - median) ** 2).sum()
    rhs = ((x - mean) ** 2).sum() + len(x) * (mean - median) ** 2
    lab.row("sum of squares about the median", f"{lhs:.1f}   = {((x - mean) ** 2).sum():.1f} + {len(x) * (mean - median) ** 2:.1f}")
    assert np.isclose(lhs, rhs, rtol=1e-10)

    # 3. The sample mean is random: 2,000 disjoint simple random samples of 100 adult heights.
    height = w.height[w.adult]
    n, reps = 100, 2000
    samples = height[rng.choice(len(height), n * reps, replace=False)].reshape(reps, n)
    means = samples.mean(1)
    mu, sigma = w.truth("mean_height"), w.truth("sd_height")
    se = sigma / np.sqrt(n)
    lab.row("mean of the 2,000 sample means", f"{means.mean():.2f} cm   (the World's mean {mu:.2f})")
    lab.row("SD of the 2,000 sample means", f"{means.std(ddof=1):.3f} cm   (sigma / sqrt(n) = {se:.3f})")
    inside = np.mean(np.abs(means - mu) < 2 * se)
    lab.row("means within 2 SE of the truth", f"{inside:.1%}   (normal: 95.4%)")
    assert abs(means.mean() - mu) < 0.1, "the sample mean is centred on the truth"
    assert abs(means.std(ddof=1) / se - 1) < 0.07, "its spread is sigma / sqrt(n)"
    assert abs(inside - 0.954) < 0.025
    lab.note = ("The median and the mean are the answers to two optimization problems, and only the second follows "
                "the long right tail; the mean of a sample is itself a draw from a distribution of width sigma / sqrt(n).")

    fig, ax = labs.figure(2, size=(11, 4.2))
    keep = (grid > x[0]) & (grid < np.quantile(x, 0.97))
    ax[0].plot(grid[keep], loss1[keep] / loss1.min(), color=labs.GREEN, label="absolute loss, p = 1")
    ax[0].plot(grid[keep], loss2[keep] / loss2.min(), color=labs.RED, label="squared loss, p = 2")
    ax[0].axvline(median, color=labs.GREEN, ls="--", lw=1)
    ax[0].axvline(mean, color=labs.RED, ls="--", lw=1)
    ax[0].plot(x[x < np.quantile(x, 0.97)], np.full((x < np.quantile(x, 0.97)).sum(), 0.97), "|", color=labs.BLUE, ms=7,
               label="the incomes (top 3% off the axis)")
    ax[0].set(title="Loss against the candidate centre c", xlabel="c, thousands a year",
              ylabel="loss / minimum loss", ylim=(0.94, 1.6))
    ax[0].legend(loc="upper center")
    bins = np.linspace(mu - 4.2 * se, mu + 4.2 * se, 45)
    ax[1].hist(means, bins=bins, density=True, color=labs.BLUE, alpha=0.6, label="2,000 sample means, n = 100")
    ax[1].plot(bins, np.exp(-0.5 * ((bins - mu) / se) ** 2) / (se * np.sqrt(2 * np.pi)), color=labs.GOLD,
               label="normal, SD sigma / sqrt(n)")
    ax[1].axvline(mu, color=labs.GOLD, ls="--", lw=1)
    ax[1].set(title="The sampling distribution of the mean height", xlabel="sample mean, cm", ylabel="density")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
