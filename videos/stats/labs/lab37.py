"""Lab 37: run two-way fixed effects on a staggered rollout, take its coefficient apart, and repair it."""

import numpy as np

from videos.coursekit import labs
from explainer.stats.kit import quasi
from explainer.stats.world import World

TITLE = "Staggered adoption: the regression that gets the sign wrong"
GOAL = ("Draw the World's rollout (200 towns adopt a jobs programme in 2004, 2009, 2014 or never, with effects that "
        "grow), fit the two-way fixed-effects regression, decompose it into Goodman-Bacon's two-by-two comparisons, "
        "and compare it with Callaway and Sant'Anna's estimator and with a world where the effect is constant.")
TASKS = [
    "Make every cohort's effect grow at the same rate (edit tau so each slope is 0.3). Is TWFE still negative, and why not?",
    "Drop the 20 never-treated towns before fitting. Which estimators still run, and what does TWFE become?",
    "Use quasi.event_study on the panel and compare its leads (event times below 0) with callaway_santanna's 'event' entries.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    p = World.rollout_panel(rng)
    Y, D, G, years, att = p["y"], p["D"], p["G"], p["years"], p["att"]
    tw = quasi.twfe(Y, D)
    cs = quasi.callaway_santanna(Y, G, years)
    imp = quasi.imputation(Y, G, years)
    parts = quasi.bacon(Y, G, years)
    kinds = ("vs never", "early vs later", "later vs earlier")
    w = {k: sum(o["w"] for o in parts if o["kind"] == k) for k in kinds}
    est = {k: sum(o["w"] * o["est"] for o in parts if o["kind"] == k) / w[k] for k in kinds}
    total = sum(o["w"] * o["est"] for o in parts)
    # the same towns, shocks and adoption dates, but an effect of 2 for every treated town-year
    Yc = p["y0"] + 2.0 * D
    tw_c, cs_c = quasi.twfe(Yc, D), quasi.callaway_santanna(Yc, G, years)

    lab = labs.Lab()
    lab.row("true ATT over treated town-years", f"{att:.2f}")
    lab.row("TWFE coefficient (clustered SE)", f"{tw['beta']:.2f} ({tw['se']:.2f})")
    for k in kinds:
        lab.row(f"  2x2s, {k}", f"weight {w[k]:.2f}, average {est[k]:+.2f}")
    lab.row("  weighted sum of the 2x2s", f"{total:.2f}")
    lab.row("Callaway-Sant'Anna (90% CI)", f"{cs['att']:.2f} ({cs['ci'][0]:.2f} to {cs['ci'][1]:.2f})")
    lab.row("imputation estimator", f"{imp['att']:.2f}")
    lab.row("constant effect 2: TWFE, Callaway-Sant'Anna", f"{tw_c['beta']:.2f}, {cs_c['att']:.2f}")
    lab.note = ("With growing effects the later-versus-earlier comparisons subtract the early towns' rising effect, "
                "carry almost half the weight and drag the regression below zero; with a constant effect the same "
                "regression is fine.")

    assert abs(total - tw["beta"]) < 1e-8, "the decomposition reproduces the regression exactly"
    assert tw["beta"] < 0 and att - tw["beta"] > 3, "TWFE is negative though every effect is positive"
    assert est["later vs earlier"] < 0 < min(est["vs never"], est["early vs later"]) and w["later vs earlier"] > 0.4
    assert abs(cs["att"] - att) < 4 * cs["se"] and abs(imp["att"] - att) < 0.6, "the repaired estimators find the ATT"
    assert abs(tw_c["beta"] - 2) < 0.4 and abs(cs_c["att"] - 2) < 0.5, "a constant effect breaks nothing"

    fig, ax = labs.figure(2, size=(11, 4.2))
    cohorts = [(2004.0, labs.BLUE, "adopt 2004"), (2009.0, labs.GOLD, "adopt 2009"), (2014.0, labs.GREEN, "adopt 2014"),
               (np.inf, labs.GREY, "never")]
    for g, color, name in cohorts:
        k = G == g
        ax[0].plot(years, Y[k].mean(0), color=color, label=name)
        if np.isfinite(g):
            ax[0].axvline(g - 0.5, color=color, lw=0.8, ls=":")
    ax[0].set(title="Mean employment rate by adoption cohort", xlabel="year", ylabel="employment rate (%)")
    ax[0].set_xticks(years[::4])
    ax[0].legend()
    names = ["truth", "TWFE", "vs never", "early vs\nlater", "later vs\nearlier", "Callaway-\nSant'Anna", "imputation"]
    vals = [att, tw["beta"], est["vs never"], est["early vs later"], est["later vs earlier"], cs["att"], imp["att"]]
    colors = [labs.GREY, labs.RED, labs.BLUE, labs.BLUE, labs.ORANGE, labs.GREEN, labs.GREEN]
    ax[1].bar(range(len(vals)), vals, color=colors, width=0.7)
    for i, v in enumerate(vals):
        ax[1].text(i, v + (0.15 if v >= 0 else -0.15), f"{v:.2f}", ha="center", va="bottom" if v >= 0 else "top", fontsize=9)
    ax[1].axhline(0, color=labs.MUTED, lw=0.8)
    ax[1].set_axisbelow(True)
    ax[1].set_xticks(range(len(vals)))
    ax[1].set_xticklabels(names, fontsize=8)
    ax[1].set_ylim(min(vals) - 0.9, max(vals) + 0.9)
    ax[1].set(title="TWFE (red) averages three kinds of 2x2", ylabel="effect (points of employment)")
    lab.fig = fig
    return lab
