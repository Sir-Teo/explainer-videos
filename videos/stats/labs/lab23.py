"""Lab 23: assign a programme by school, and compare the iid and the cluster-robust standard errors."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import ols

TITLE = "Moulton's factor, and cluster-robust errors with few clusters"
GOAL = ("Simulate pupils in schools with an intraclass correlation of 0.15 and a programme assigned by school, and "
        "compare the estimate's true spread with the iid and the cluster-robust (CR1) standard errors, first with "
        "forty schools and then with eight.")
TASKS = [
    "Assign the programme pupil by pupil instead of school by school. What is Moulton's factor now, and who covers?",
    "Make the school sizes unequal (say 10 to 90 pupils). Does CR1 with eight schools get better or worse?",
    "Add ols.wild_cluster_boot for the eight-school case and compare its rejection rate under the null with CR1's.",
]


def study(G, m, rho, reps, rng):
    """reps data sets: G schools of m pupils, half the schools treated (true effect 0), unit total variance."""
    school = np.repeat(np.arange(G), m)
    treat = (school < G // 2).astype(float)
    X = ols.design(treat)
    tq = stats.t.ppf(0.975, G - 1)
    est, se_i, se_c = np.empty(reps), np.empty(reps), np.empty(reps)
    for r in range(reps):
        y = np.sqrt(rho) * rng.standard_normal(G)[school] + np.sqrt(1 - rho) * rng.standard_normal(G * m)
        f = ols.fit(X, y)
        est[r], se_i[r] = f.coef[1], f.se()[1]
        se_c[r] = np.sqrt(ols.cluster_cov(f, school)[1, 1])
    return dict(est=est, sd=est.std(), se_i=se_i.mean(), se_c=se_c.mean(),
                cov_i=np.mean(np.abs(est) < stats.t.ppf(0.975, G * m - 2) * se_i), cov_c=np.mean(np.abs(est) < tq * se_c))


def run(seed=0):
    rng = np.random.default_rng(seed)
    m, rho = 30, 0.15
    factor = ols.moulton(m, 1.0, rho)  # the regressor is constant within schools: rho_x = 1
    big, small = study(40, m, rho, 600, rng), study(8, m, rho, 1500, rng)
    lab = labs.Lab()
    lab.row("Moulton's factor 1 + (m - 1) rho", f"{factor:.2f}   (SE ratio {np.sqrt(factor):.2f})")
    for name, r in (("40 schools", big), ("8 schools", small)):
        lab.row(f"{name}: true sd of the estimate", f"{r['sd']:.4f}   iid SE {r['se_i']:.4f}   CR1 SE {r['se_c']:.4f}")
        lab.row(f"{name}: true sd / iid SE", f"{r['sd'] / r['se_i']:.2f}   (Moulton {np.sqrt(factor):.2f})")
        lab.row(f"{name}: 95% interval covers", f"iid {r['cov_i']:.1%}   CR1 with t(G-1) {r['cov_c']:.1%}")
    lab.note = ("Ignoring the schools understates the standard error by the square root of Moulton's factor; the "
                "cluster-robust error repairs it with forty schools and is itself too small with eight.")
    assert abs(big["sd"] / big["se_i"] / np.sqrt(factor) - 1) < 0.12, "the iid SE is off by Moulton's factor"
    assert big["cov_i"] < 0.72 and small["cov_i"] < 0.75, "iid intervals are broken"
    assert abs(big["se_c"] / big["sd"] - 1) < 0.1 and abs(big["cov_c"] - 0.95) < 0.03, "CR1 works with 40 clusters"
    assert small["se_c"] / small["sd"] < 0.97 and small["cov_c"] < 0.95, "CR1 is too small with 8"

    fig, ax = labs.figure(2, size=(11, 4.2))
    bins = np.linspace(-4 * big["sd"], 4 * big["sd"], 50)
    ax[0].hist(big["est"], bins=bins, density=True, color=labs.BLUE, alpha=0.6, label="600 estimates (true effect 0)")
    for se, color, name in ((big["se_i"], labs.RED, "iid SE"), (big["se_c"], labs.GREEN, "CR1 SE")):
        ax[0].plot(bins, stats.norm.pdf(bins, 0, se), color=color, label=f"normal with the {name}")
    ax[0].set(title="Forty schools: which SE matches the spread?", xlabel="estimated programme effect (SD units)",
              ylabel="density")
    ax[0].legend(loc="upper left", fontsize=8)
    names = ["iid\n40 schools", "CR1\n40 schools", "iid\n8 schools", "CR1\n8 schools"]
    vals = [big["cov_i"], big["cov_c"], small["cov_i"], small["cov_c"]]
    bars = ax[1].bar(names, vals, color=[labs.RED, labs.GREEN, labs.RED, labs.GREEN], width=0.6)
    for b, v in zip(bars, vals):
        ax[1].text(b.get_x() + b.get_width() / 2, v - 0.07, f"{v:.1%}", ha="center", fontsize=10, color=labs.BG, fontweight="bold")
    ax[1].axhline(0.95, color=labs.MUTED, ls="--", lw=1)
    ax[1].set(title="Coverage of nominal 95% intervals", ylabel="coverage", ylim=(0, 1.1))
    lab.fig = fig
    return lab
