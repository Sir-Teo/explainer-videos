"""Lab 31: test equal mean vectors as the number of variables grows, and see which calibration of T-squared survives."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import multi

TITLE = "Hotelling's T-squared when p approaches n"
GOAL = ("Draw two samples of 50 from the same p-variate normal two thousand times for p = 2, 10, 25 and 40, and compare "
        "the size of the two-sample T-squared test under its chi-squared and its exact F calibration with the size "
        "theory predicts.")
TASKS = [
    "Shift every coordinate of the second sample by 0.15 and add multi.bai_saranadasa. At which p does it overtake the exact F in power?",
    "Give the two samples different covariance matrices (multiply one sample by 2). Does the exact F keep its 5%?",
    "Replace the normal draws by t with 5 degrees of freedom. Which calibration is hurt more at p = 2, and at p = 40?",
]

N1 = N2 = 50
PS = (2, 10, 25, 40)


def chi2_size(p, m=N1 + N2 - 2, alpha=0.05):
    """The exact size of 'reject when T2 exceeds the chi-squared_p critical value': T2 is a multiple of an F."""
    return float(stats.f.sf(stats.chi2.ppf(1 - alpha, p) * (m - p + 1) / (p * m), p, m - p + 1))


def run(seed=0):
    rng = np.random.default_rng(seed)
    reps = 2000
    lab = labs.Lab()

    # the opening claim first: classical scaling is exact for Euclidean distances
    towns = rng.uniform(0, 10, (40, 2))
    D = np.linalg.norm(towns[:, None] - towns[None], axis=2)
    mds = multi.classical_mds(D)
    rmse = multi.procrustes(towns, mds["X"])["rmse"]
    lab.row("classical scaling from exact distances: RMSE of the map", f"{rmse:.1e}   (theory 0)")
    assert rmse < 1e-8 and mds["negative_share"] < 1e-10, "a Euclidean distance table is reproduced exactly"

    size_chi, size_f, t2 = {}, {}, {}
    for p in PS:
        out = [multi.hotelling_two(rng.standard_normal((N1, p)), rng.standard_normal((N2, p))) for _ in range(reps)]
        size_chi[p] = np.mean([o["p_chi2"] < 0.05 for o in out])
        size_f[p] = np.mean([o["p"] < 0.05 for o in out])
        t2[p] = np.array([o["T2"] for o in out])
        lab.row(f"p = {p:>2}: size at 5%", f"chi-squared {size_chi[p]:.1%} (theory {chi2_size(p):.1%})   "
                                           f"exact F {size_f[p]:.1%} (theory 5.0%)")
        se = np.sqrt(max(chi2_size(p) * (1 - chi2_size(p)), 0.05 * 0.95) / reps)
        assert abs(size_chi[p] - chi2_size(p)) < 4 * se, "the chi-squared calibration's size is the F tail it implies"
        assert abs(size_f[p] - 0.05) < 4 * np.sqrt(0.05 * 0.95 / reps), "the exact F keeps its level at every p"
    assert size_chi[2] < 0.08 and size_chi[40] > 0.6, "fine at p = 2, broken at p = 40"
    lab.note = ("With two samples of 50 the chi-squared calibration is a fixed-p approximation: it rejects one true null "
                "in three at p = 25 and most of them at p = 40, while the exact F holds its 5% throughout.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    grid = np.arange(1, 61)
    ax[0].plot(grid, [chi2_size(p) for p in grid], color=labs.RED, label="chi-squared calibration, theory")
    ax[0].plot(PS, [size_chi[p] for p in PS], "o", color=labs.RED, label="chi-squared calibration, simulated")
    ax[0].plot(PS, [size_f[p] for p in PS], "s", color=labs.GREEN, label="exact F, simulated")
    ax[0].axhline(0.05, color=labs.MUTED, ls="--", label="nominal 5%")
    ax[0].set(title="Size of the two-sample test, n1 = n2 = 50", xlabel="number of variables p",
              ylabel="share of true nulls rejected")
    ax[0].legend()
    p, m = 40, N1 + N2 - 2
    xs = np.linspace(0, np.quantile(t2[p], 0.995), 300)
    c = p * m / (m - p + 1)
    ax[1].hist(t2[p], bins=60, range=(0, xs[-1]), density=True, color=labs.BLUE, alpha=0.6, label="2,000 simulated T-squared")
    ax[1].plot(xs, stats.chi2.pdf(xs, p), color=labs.RED, label="chi-squared with 40 df")
    ax[1].plot(xs, stats.f.pdf(xs / c, p, m - p + 1) / c, color=labs.GREEN, label="scaled F(40, 59)")
    ax[1].axvline(stats.chi2.ppf(0.95, p), color=labs.RED, ls=":", lw=1.2)
    ax[1].set(title="p = 40: the null law of T-squared", xlabel="T-squared", ylabel="density")
    ax[1].legend()
    lab.fig = fig
    return lab
