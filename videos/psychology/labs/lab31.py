"""Lab 31: the age-period-cohort identity, three designs on a world where the truth is known, a growth-curve mixed
model fitted by EM with its shrunken lines, ACE correlations, cognitive reserve and attributable fractions."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import lifespan as L

TITLE = "The Lifespan"
GOAL = ("Show that linear age, period and cohort effects cannot be separated; run a cross-sectional, a longitudinal "
        "and a cohort-sequential design on a simulated population and compare each with the true ageing curve; fit "
        "a growth-curve mixed model by EM and watch it shrink each child's line; compute ACE correlations, a "
        "reserve model and attributable fractions.")
TASKS = [
    "Add a period effect to the simulated world (everyone tested after 1990 scores 0.3 SD higher). Which design "
    "breaks, and how does its estimate of the cohort drift change?",
    "Make drop-out depend on the current score instead of the last one. Does the longitudinal curve's bias grow or "
    "shrink?",
    "Halve the number of visits in the growth data. How do the spreads of the children's own slopes, the true slopes "
    "and the BLUPs change?",
]


def run(seed=0):
    out = labs.Lab()

    # 1. the identity
    r = L.apc_equivalent(0.0, 0.01, 0.0, 0.25, [20, 50, 80], [1970, 2000, 2030])
    out.row("APC: largest difference between (a, p, c) and (a + k, p - k, c + k), k = 0.25", f"{r['max_diff']:.1e}")
    assert r["max_diff"] < 1e-9

    # 2. three designs
    w = L.ability_world(n=40_000, seed=seed)
    cs = L.cross_sectional(w)
    lo = L.longitudinal(w)
    cq = L.cohort_sequential(w)
    i50 = list(cs["age"]).index(50.0)
    out.row("cross-section in 1990: change from 20 to 50 (true change 0)", f"{cs['mean'][i50] - cs['mean'][0]:.2f} SD")
    out.row("one cohort followed: survivors' change from 26 to 54; people left of 1,500",
            f"{lo['kept'][4] - lo['kept'][0]:+.2f} SD; {lo['n'][-1]}")
    out.row("cohort-sequential: cohort drift recovered (true 0.020)", f"{cq['cohort_gain_hat']:.3f}")
    assert cs["mean"][i50] - cs["mean"][0] < -0.3 and lo["kept"][4] > lo["kept"][0]
    assert abs(cq["cohort_gain_hat"] - 0.02) < 0.004

    # 3. growth curves
    g = L.growth_data(n=120, seed=4)
    f = L.fit_growth(g["t"], g["y"], iters=200)
    out.row("growth: beta0, beta1, sigma0, sigma1, rho, sigma (true 100, 6, 8, 2, 0.3, 5)",
            f"{f['beta'][0]:.1f}, {f['beta'][1]:.2f}, {f['sd_int']:.1f}, {f['sd_slope']:.2f}, {f['rho']:.2f}, "
            f"{f['sd_e']:.1f}")
    sd_ols, sd_blup = float(np.nanstd(f["ols"][:, 1])), float(np.std(f["blup"][:, 1]))
    out.row("spread of growth: own lines, truth, BLUPs",
            f"{sd_ols:.2f}, {np.std(g['b_true'][:, 1]):.2f}, {sd_blup:.2f}")
    assert sd_blup < sd_ols

    # 4. ACE, reserve, fractions
    for name, (h2, c2) in {"childhood": (0.4, 0.3), "adulthood": (0.6, 0.0)}.items():
        s = L.sibling_correlations(h2, c2)
        out.row(f"ACE in {name}: identical, fraternal, adoptive", f"{s['mz']:.2f}, {s['dz']:.2f}, {s['adoptive']:.2f}")
    ages = np.linspace(50, 95, 181)
    onsets = [L.reserve(ages, rv)["onset"] for rv in (0.5, 1.0, 2.0)]
    out.row("reserve 0.5, 1, 2: age at onset", ", ".join(f"{o:.0f}" for o in onsets))
    out.row("PAF for p = 0.3, RR = 1.9; four fractions 7, 7, 5, 5% combined",
            f"{L.paf(0.3, 1.9):.2f}; {100 * L.combined_paf([0.07, 0.07, 0.05, 0.05]):.1f}%")

    out.note = ("Only two of three linear clocks are identified; a cross-section turns cohort gains into ageing, a "
                "panel turns practice and drop-out into stability, and a cohort-sequential design recovers both under "
                "its assumption; the mixed model recovers the growth parameters and shrinks each child's line toward "
                "the fan; and attributable fractions combine to less than their sum.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    grid = np.arange(20, 91)
    ax[0].plot(grid, L.true_ageing(grid), color="#5BD18B", lw=3, label="truth")
    ax[0].plot(cs["age"], cs["mean"] - cs["mean"][0], "o-", color=labs.GOLD, label="cross-section")
    ax[0].plot(lo["age"], lo["kept"] - lo["kept"][0], "o-", color=labs.BLUE, label="one cohort, survivors")
    ax[0].plot(cq["age"], cq["curve"], "s--", color="#B39DDB", label="cohort-sequential")
    ax[0].set(title="Three designs, one world", xlabel="age", ylabel="score (SD)")
    ax[0].legend(fontsize=8)
    ok = ~np.isnan(f["ols"][:, 1])
    ax[1].scatter(f["ols"][ok, 1], f["blup"][ok, 1], s=12, color=labs.BLUE)
    ax[1].plot([0, 13], [0, 13], "--", color="#888888")
    ax[1].axhline(f["beta"][1], color=labs.GOLD)
    ax[1].set(title="Shrinkage of each child's growth", xlabel="own line", ylabel="BLUP")
    out.fig = fig
    return out
