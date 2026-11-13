"""Lab 7: catch RANDU on its fifteen planes, then run a simulation study with its Monte Carlo errors."""

import numpy as np
from scipy import stats

from videos.coursekit import labs
from explainer.stats.kit import random as skr
from explainer.stats.kit import tests as skt

TITLE = "A bad generator and an honest simulation study"
GOAL = ("Show that RANDU passes a one-dimensional test while 9x - 6y + z takes only fifteen values on its triples, "
        "then use statkit's simulate to estimate the coverage of the textbook interval for a proportion (n = 30) "
        "and compare it, within Monte Carlo error, with the exact binomial sum.")
TASKS = [
    "Swap the method for Wilson's interval, (p + z^2/2n +/- z sqrt(p(1 - p)/n + z^2/4n^2)) / (1 + z^2/n) with "
    "z = 1.96. How near 95% does its coverage stay across p?",
    "Cut reps to 400. How wide do the bars of two Monte Carlo standard errors become, and can you still tell "
    "p = 0.3 from 95%?",
    "Replace randu by lcg(5, 3, 16, seed, n) and plot consecutive pairs. How many lines do they fall on?",
]

N_TRIALS = 30


def wald(x):
    """The textbook 95% interval for a proportion from x successes in N_TRIALS trials."""
    p = x / N_TRIALS
    half = 1.96 * np.sqrt(p * (1 - p) / N_TRIALS)
    return p, p - half, p + half


def exact_coverage(p):
    x = np.arange(N_TRIALS + 1)
    _, lo, hi = wald(x)
    return float(np.sum(stats.binom.pmf(x, N_TRIALS, p) * ((lo <= p) & (p <= hi))))


def run(seed=0):
    lab = labs.Lab()

    # 1. RANDU: uniform in one dimension, fifteen planes in three.
    ints = skr.randu(2 * seed + 1, 300_000)  # an odd seed; seed 0 is the film's
    cells = np.minimum(ints * 10 // skr.M31, 9).astype(int)
    one_d = skt.chisq_test(np.bincount(cells, minlength=10), np.full(10, 0.1))
    c3 = cells.reshape(-1, 3) @ np.array([100, 10, 1])  # each non-overlapping triple's cell in a 10 x 10 x 10 grid
    three_d = skt.chisq_test(np.bincount(c3, minlength=1000), np.full(1000, 0.001))
    k = (9 * ints[:-2] - 6 * ints[1:-1] + ints[2:]) / skr.M31
    planes = np.unique(k)
    pcg = skr.PCG32(seed + 42).random(9000)
    k_pcg = 9 * pcg[:-2] - 6 * pcg[1:-1] + pcg[2:]
    lab.row("RANDU, 300,000 numbers in 10 bins", f"chi-squared {one_d['chi2']:.1f} on 9 df, p = {one_d['p']:.2f}")
    lab.row("RANDU, 100,000 triples in 1,000 cells", f"chi-squared {three_d['chi2']:.0f} on 999 df, p = {three_d['p']:.0e}")
    lab.row("values of 9x - 6y + z on RANDU's triples", f"{len(planes)}   (from {planes.min():.0f} to {planes.max():.0f})")
    lab.row("values of 9x - 6y + z on PCG32's triples", f"{len(np.unique(k_pcg))} of {len(k_pcg)}")
    assert one_d["p"] > 0.001, "one coordinate at a time, RANDU looks uniform"
    assert three_d["p"] < 1e-6, "three at a time, it does not"
    assert len(planes) == 15 and np.all(planes == np.round(planes)), "every RANDU triple lies on one of 15 planes"
    assert len(np.unique(k_pcg)) > 0.99 * len(k_pcg), "PCG32's triples do not"

    # 2. A simulation study (ADEMP): the coverage of the Wald interval, each estimate with its Monte Carlo SE.
    reps, ps = 4000, [0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9]
    sims = []
    for i, p in enumerate(ps):
        out = skr.simulate(lambda rng, p=p: rng.binomial(N_TRIALS, p), wald, p, reps, seed=1000 * seed + i)
        truth = exact_coverage(p)
        sims.append(out)
        if p in (0.02, 0.1, 0.5):
            lab.row(f"Wald coverage at p = {p}", f"{out['coverage']:.3f} +/- {out['coverage_mcse']:.3f}   (exact {truth:.3f})")
        assert abs(out["coverage"] - truth) < 4 * np.sqrt(truth * (1 - truth) / reps), "simulation within Monte Carlo error"
        assert abs(out["bias"]) < 4 * out["bias_mcse"], "the sample share is unbiased"
    assert exact_coverage(0.02) < 0.5 and exact_coverage(0.1) < 0.85, "the textbook interval breaks its 95% promise"
    assert abs(skr.mc_se(np.r_[np.ones(3800), np.zeros(200)]) - np.sqrt(0.95 * 0.05 / 4000)) < 1e-5, "MCSE of a proportion"
    lab.note = ("A generator can pass one test and fail another, so it is tested many ways; and a simulated coverage "
                "is an estimate, here within two or three Monte Carlo standard errors of the exact answer, which "
                "is far below 95% for small p.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    trip = np.column_stack([ints[:-2], ints[1:-1], ints[2:]])[:3000] / skr.M31
    along = trip @ np.array([2, 3, 0]) / np.sqrt(13)  # a direction inside the planes
    across = trip @ np.array([9, -6, 1]) / np.sqrt(118)  # the planes' normal
    ax[0].scatter(along, across, s=3, color=labs.RED, label="RANDU")
    ptrip = np.column_stack([pcg[:-2], pcg[1:-1], pcg[2:]])[:3000]
    ax[0].scatter(ptrip @ np.array([2, 3, 0]) / np.sqrt(13) + 1.6, ptrip @ np.array([9, -6, 1]) / np.sqrt(118), s=3,
                  color=labs.GREEN, label="PCG32 (shifted right)")
    ax[0].set(title="3,000 triples seen edge-on to RANDU's planes", xlabel="(2x + 3y)/sqrt(13)",
              ylabel="(9x - 6y + z)/sqrt(118)")
    ax[0].legend(loc="upper center", ncol=2, markerscale=3)
    ax[0].set_ylim(-0.6, 1.15)
    grid = np.linspace(0.01, 0.99, 197)
    ax[1].plot(grid, [exact_coverage(p) for p in grid], color=labs.GOLD, lw=1.2, label="exact (binomial sum)")
    ax[1].errorbar(ps, [o["coverage"] for o in sims], yerr=[2 * o["coverage_mcse"] for o in sims], fmt="o",
                   color=labs.RED, capsize=3, label="simulate: 4,000 replicates, +/- 2 MCSE")
    ax[1].axhline(0.95, color=labs.MUTED, ls="--", lw=1)
    ax[1].set(title="Coverage of p-hat +/- 1.96 SE, n = 30", xlabel="true p", ylabel="coverage", ylim=(0.4, 1.0))
    ax[1].legend(loc="lower center")
    lab.fig = fig
    return lab
