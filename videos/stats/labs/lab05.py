"""Lab 5: Galton's table recomputed, a Gaussian sliced and renormalized, and regression to the mean in the World."""

import numpy as np

from videos.coursekit import labs
from explainer.stats import museum
from explainer.stats.world import World

TITLE = "Slicing an ellipse: conditional means, Eve's law and regression to the mean"
GOAL = ("Recompute Galton's correlation and slope from his 1886 table, split the children's variance into within and "
        "between mid-parent rows, then slice a simulated bivariate normal with Galton's moments and compare each "
        "slice's mean and SD with the conditioning formula.")
TASKS = [
    "Slice on the child's height instead and predict the mid-parent. Is the slope the reciprocal of 0.646?",
    "Set the correlation of the simulated cloud to 0.9, then to 0.1. How does the conditional SD change, and the "
    "share of the variance that lies between rows?",
    "In the World, follow the shortest tenth of mid-parents instead of the tallest. How far below average are their "
    "sons, in centimetres and as a share of the parents' deficit?",
]


def galton_points():
    """One (mid-parent, child) pair per child, in inches, from Galton's grouped table."""
    P, C, T = np.array(museum.GALTON_PARENT), np.array(museum.GALTON_CHILD), np.array(museum.GALTON_TABLE)
    return np.repeat(np.repeat(P, len(C)), T.ravel()), np.repeat(np.tile(C, len(P)), T.ravel())


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Galton's table: correlation, slope, and Eve's law over its rows.
    x, y = galton_points()
    mx, my, S = x.mean(), y.mean(), np.cov(np.vstack([x, y]), ddof=0)
    r = S[0, 1] / np.sqrt(S[0, 0] * S[1, 1])
    slope = S[0, 1] / S[0, 0]
    rows = np.unique(x)
    wts = np.array([np.mean(x == k) for k in rows])
    row_mean = np.array([y[x == k].mean() for k in rows])
    row_var = np.array([y[x == k].var() for k in rows])
    within, between, total = (wts * row_var).sum(), (wts * (row_mean - my) ** 2).sum(), y.var()
    eta2 = between / total
    lab.row("Galton: children, correlation, slope", f"{len(x)}   r = {r:.3f}   slope = {slope:.3f}   (Galton's two-thirds)")
    lab.row("Eve's law on Galton's rows", f"{total:.2f} = {within:.2f} within + {between:.2f} between")
    lab.row("correlation ratio and r squared", f"eta^2 = {eta2:.3f}   r^2 = {r * r:.3f}")
    assert len(x) == 928 and abs(r - 0.459) < 0.001 and abs(slope - 0.646) < 0.001, "the film's numbers"
    assert np.isclose(total, within + between) and abs(within - 4.93) < 0.01 and abs(between - 1.40) < 0.01
    assert eta2 >= r * r, "the conditional mean explains at least as much as the best line"

    # 2. A bivariate normal with Galton's moments, sliced at three mid-parent heights.
    n = 400_000
    xy = rng.multivariate_normal([mx, my], S, n)
    cond_sd = np.sqrt(S[1, 1] - S[0, 1] ** 2 / S[0, 0])  # the Schur complement
    slices = []
    for x0 in (66.0, 68.3, 70.5):
        near = np.abs(xy[:, 0] - x0) < 0.1
        ys = xy[near, 1]
        cond_mean = my + slope * (x0 - mx)
        slices.append((x0, ys, cond_mean))
        lab.row(f"slice at mid-parent {x0}: mean, SD", f"{ys.mean():.2f}, {ys.std():.2f}   formula {cond_mean:.2f}, {cond_sd:.2f}   ({len(ys):,} points)")
        assert abs(ys.mean() - cond_mean) < 5 * cond_sd / np.sqrt(len(ys)) + 0.01, "the conditional mean is linear in x0"
        assert abs(ys.std() / cond_sd - 1) < 0.05, "the conditional SD does not depend on x0"
    assert cond_sd < np.sqrt(S[1, 1])

    # 3. Regression to the mean in the World: the tallest tenth of mid-parents and their sons.
    f = World().families
    son = f["son"]
    mid, child = ((f["father"] + f["mother"]) / 2)[son], f["child"][son]
    top = mid >= np.quantile(mid, 0.9)
    mid_dev, son_dev = mid[top].mean() - mid.mean(), child[top].mean() - child.mean()
    w_slope = np.cov(mid, child, ddof=0)[0, 1] / mid.var()
    lab.row("World: tallest tenth of mid-parents", f"+{mid_dev:.2f} cm; their sons +{son_dev:.2f} cm   (ratio {son_dev / mid_dev:.3f}, slope {w_slope:.3f})")
    sd_fathers, sd_sons = f["father"][son].std(), child.std()
    lab.row("World: SD of the fathers and of their sons", f"{sd_fathers:.2f} and {sd_sons:.2f} cm   (no shrinking)")
    assert 0 < son_dev < mid_dev and abs(son_dev / mid_dev - w_slope) < 0.03, "the sons fall back by the slope"
    assert abs(sd_sons / sd_fathers - 1) < 0.02, "yet the sons are as spread out as their fathers"
    lab.note = ("Slicing a Gaussian gives a normal whose mean moves along a line flatter than the diagonal and whose "
                "spread is the same in every slice: regression to the mean is the shape of the ellipse, not a force.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    P, C, T = np.array(museum.GALTON_PARENT), np.array(museum.GALTON_CHILD), np.array(museum.GALTON_TABLE)
    gp, gc = np.meshgrid(P, C, indexing="ij")
    ax[0].scatter(gp[T > 0], gc[T > 0], s=6 * T[T > 0], color=labs.BLUE, alpha=0.45, label="Galton's counts (area)")
    line = np.array([63.5, 73.5])
    ax[0].plot(line, line - mx + my, color=labs.MUTED, ls="--", label="children as extreme as parents")
    ax[0].plot(line, my + slope * (line - mx), color=labs.GOLD, label=f"regression line, slope {slope:.2f}")
    ax[0].plot(rows, row_mean, "o", color=labs.RED, ms=4, label="mean child in each row")
    ax[0].set(title="Galton's table, 1886 (inches)", xlabel="mid-parent height", ylabel="adult child's height")
    ax[0].legend(loc="lower right")
    grid = np.linspace(60, 77, 300)
    for (x0, ys, cond_mean), color in zip(slices, (labs.TEAL, labs.GOLD, labs.PURPLE)):
        ax[1].hist(ys, bins=40, density=True, color=color, alpha=0.3)
        ax[1].plot(grid, np.exp(-0.5 * ((grid - cond_mean) / cond_sd) ** 2) / (cond_sd * np.sqrt(2 * np.pi)), color=color,
                   label=f"mid-parent {x0}: N({cond_mean:.1f}, {cond_sd:.2f}$^2$)")
    ax[1].plot(grid, np.exp(-0.5 * ((grid - my) / np.sqrt(S[1, 1])) ** 2) / np.sqrt(2 * np.pi * S[1, 1]), color=labs.MUTED,
               ls="--", label="all children")
    ax[1].set(title="Three slices of the fitted Gaussian, renormalized", xlabel="child's height", ylabel="density",
              ylim=(0, 0.26))
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
