"""Lab 39: krige simulated fields with the right covariance, along the unidentifiable ridge, and off it."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import spatial

TITLE = "Kriging along the ridge: what need not be learned"
GOAL = ("Simulate 60 exponential (Matérn, nu = 1/2) fields at 200 sites in the unit square, krige 50 held-back sites "
        "with the true variance and range, with both doubled (the same sigma^2 / rho), and with the range alone "
        "wrong, and compare the RMSE and the coverage of the 90% prediction intervals.")
TASKS = [
    "Move along the ridge the other way (rho x 0.5 with sigma^2 x 0.5), then further (x 8 with x 8). When does coverage finally move?",
    "Set nu = 1.5 in both the simulation and the kriging. The ridge is now sigma^2 / rho^3: check that rho x 2 needs sigma^2 x 8.",
    "Replace the simple kriging (mean=0.0) by ordinary kriging (drop the mean argument) and compare the variances it reports.",
]

NU, RHO, SIGMA2, NUGGET = 0.5, 0.3, 1.0, 0.01
SETTINGS = [  # (label, range multiplier, variance multiplier)
    ("the truth", 1.0, 1.0),
    ("ridge: rho x 2, sigma^2 x 2", 2.0, 2.0),
    ("off it: rho x 2 alone", 2.0, 1.0),
    ("off it: rho x 0.5 alone", 0.5, 1.0),
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    n, m, reps = 200, 50, 60
    cover = {s[0]: [] for s in SETTINGS}
    mse = {s[0]: [] for s in SETTINGS}
    sds = {}
    for _ in range(reps):
        xy = rng.random((n + m, 2))
        K = spatial.matern(spatial.dists(xy), SIGMA2, RHO, NU)
        field = np.linalg.cholesky(K + 1e-10 * np.eye(n + m)) @ rng.standard_normal(n + m)
        z = field[:n] + np.sqrt(NUGGET) * rng.standard_normal(n)
        for name, a, b in SETTINGS:
            out = spatial.krige(xy[:n], z, xy[n:], lambda d: spatial.matern(d, SIGMA2 * b, RHO * a, NU),
                                nugget=NUGGET, mean=0.0)
            err = field[n:] - out["pred"]
            sd = np.sqrt(out["var"])
            cover[name].append(np.mean(np.abs(err) < 1.645 * sd))
            mse[name].append(np.mean(err ** 2))
            sds[name] = sd  # the last field's, for the figure
    cov = {k: float(np.mean(v)) for k, v in cover.items()}
    rmse = {k: float(np.sqrt(np.mean(v))) for k, v in mse.items()}

    lab = labs.Lab()
    for name, a, b in SETTINGS:
        lab.row(name, f"RMSE {rmse[name]:.3f}   90% intervals cover {cov[name]:.1%}   (sigma^2/rho = {SIGMA2 * b / (RHO * a):.2f})")
    lab.note = ("The predictions hardly depend on the parameters at all, and the intervals depend only on "
                "sigma^2 / rho: doubling both changes nothing, which is why dense data in a fixed region cannot "
                "tell them apart, while the range alone wrong gives intervals too narrow or too wide.")
    truth, ridge, long_, short = (s[0] for s in SETTINGS)
    assert abs(cov[truth] - 0.90) < 0.03, "the true covariance gives calibrated intervals"
    assert abs(cov[ridge] - cov[truth]) < 0.02 and abs(rmse[ridge] / rmse[truth] - 1) < 0.02, "the ridge changes nothing"
    assert cov[long_] < 0.82 and cov[short] > 0.95, "off the ridge the intervals are wrong in each direction"
    assert max(rmse.values()) / min(rmse.values()) < 1.05, "the point predictions barely move"

    fig, ax = labs.figure(2, size=(11, 4.2))
    names = [s[0] for s in SETTINGS]
    colors = [labs.GREY, labs.GREEN, labs.RED, labs.ORANGE]
    ax[0].barh(range(4), [100 * cov[k] for k in names], color=colors, height=0.6)
    ax[0].axvline(90, color=labs.INK, ls="--", lw=1)
    for i, k in enumerate(names):
        ax[0].text(100 * cov[k] - 1.5, i, f"{cov[k]:.1%}", ha="right", va="center", color=labs.BG, fontsize=9, fontweight="bold")
    ax[0].set_axisbelow(True)
    ax[0].set_yticks(range(4))
    ax[0].set_yticklabels(["the truth", "ridge: both x 2", "rho x 2 alone", "rho x 0.5 alone"])
    ax[0].invert_yaxis()
    ax[0].set(title="Coverage of 90% kriging intervals (dashed: 90%)", xlabel="coverage over 60 fields (%)", xlim=(50, 100))
    top = 1.05 * max(v.max() for v in sds.values())
    ax[1].plot([0, top], [0, top], color=labs.MUTED, ls="--", lw=1)
    for k, color in zip(names[1:], colors[1:]):
        ax[1].scatter(sds[truth], sds[k], s=14, color=color, alpha=0.85, label=k)
    ax[1].set(title="Kriging sd at 50 sites of one field", xlabel="sd under the true parameters",
              ylabel="sd under the wrong parameters", xlim=(0, top), ylim=(0, top))
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
