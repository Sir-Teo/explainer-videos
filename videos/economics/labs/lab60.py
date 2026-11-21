"""Lab 60: the price: the markup rule under uncertainty, willingness to pay from a conjoint survey, an experiment with
interference, revenue management from Littlewood to dynamic programming, versions, bundles, reference prices, a
chain's uniform price, food pass-through on FRED data, and pricing that learns."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import revenue as R

TITLE = "The price"
GOAL = ("Price the Island's flight, its survey's features and its stores' goods with the tools firms use, and check "
        "each against the truth the Island knows.")
TASKS = [
    "Raise the business fare to $600 in R.littlewood(p_hi=600). How many seats should be protected now, and why?",
    "Make rooms plentiful (R.interference(rooms=400)). What happens to the gap between the A/B test and the truth?",
    "Change the flight so business travellers arrive in the last 30 days (R.flight({'switch': 30})) and solve "
    "R.dp_prices again. How does the best single fare compare with the optimum now?",
]


def run(seed=0):
    lab = labs.Lab()
    C = R.cost_plus_robustness(seed=60 + seed)
    lab.row("markup rule with a noisy elasticity: mean, worst tenth; a fixed 50% markup (share of the best)",
            f"{100 * C['rule_mean']:.1f}%, {100 * C['rule_p10']:.1f}%; {100 * C['fixed']:.1f}%")
    J = R.conjoint(seed=60 + seed)
    lab.row("conjoint willingness to pay: wifi, legroom, bag (planted 11.25, 17.50, 7.50)",
            ", ".join(f"${J['wtp'][k]:.2f} ({J['wtp_se'][k]:.2f})" for k in ("wifi", "legroom", "bag")))
    X = R.interference(reps=40, seed=60 + seed)
    assert X["naive"] > 1.5 * X["global"]          # scarce rooms inflate the A/B test
    lab.row("discount test: A/B estimate, the true global effect, a test by city (booking-rate points)",
            f"{100 * X['naive']:.1f}, {100 * X['global']:.1f}, {100 * X['cluster']:.1f}")
    L = R.littlewood()
    lab.row("Littlewood: protection level; revenue protected, first-come first-served",
            f"{L['y_star']}; ${L['rev_star']:,.0f}, ${L['rev_none']:,.0f}")
    lab.row("EMSR-b protection levels for the top 1, 2, 3 of four fares",
            ", ".join(f"{x:.1f}" for x in R.emsr_b()["protect"]))
    O = R.overbooking()
    lab.row("overbooking: tickets for 100 seats, expected revenue, passengers bumped",
            f"{O['best']}, ${O['value_best']:,.0f}, {O['bumped_best']:.2f}")
    F = R.flight()
    D = R.dp_prices(F, grid=np.arange(40.0, 501.0, 10.0))
    lab.row("the flight: optimal expected revenue; best single fare and its revenue",
            f"${D['V0']:,.0f}; ${D['fixed']['best_price']:.0f}, ${D['fixed']['best']:,.0f}")
    M = R.menu()
    lab.row("good, better, best: qualities; profit against one version and full information",
            ", ".join(f"{q:.2f}" for q in M["q"]) + f"; {M['profit']:.3f} vs {M['profit_one']:.3f}, "
            f"{M['profit_full_info']:.3f}")
    B = R.big_bundle(ns=(1, 10, 100), consumers=10000, seed=60 + seed)
    lab.row("bundles: revenue per good with 1, 10, 100 goods", ", ".join(f"{r['revenue_per_good']:.3f}"
                                                                         for r in B["rows"]))
    H = R.hilo()
    lab.row("high-low against everyday low prices (revenue a year)", f"${H['revenue_hilo']:,.0f} vs "
            f"${H['revenue_edlp']:,.0f}")
    Ch = R.chain(seed=60 + seed)
    lab.row("a chain: uniform price; profit given up; gap between 10th and 90th percentile stores' best prices",
            f"{Ch['uniform']:.3f}; {100 * Ch['loss']:.2f}%; {100 * Ch['gap_10_90']:.1f}%")
    a, b = data.fred("CUSR0000SAF11"), data.fred("WPU02")
    A, Bp = dict(zip(a["date"], a["value"])), dict(zip(b["date"], b["value"]))
    dates = [d for d in a["date"] if d in Bp and "2000-01-01" <= d <= "2019-12-01"]
    Pt = R.passthrough_lags([A[d] for d in dates], [Bp[d] for d in dates])
    lab.row("food pass-through after 12 months, 2000-2019 (s.e.)", f"{Pt['cum'][-1]:.3f} ({Pt['cum_se']:.3f})")

    lab.note = ("The tools differ, but the habit is the same: say what you assume about buyers, measure it where you "
                "can, and check the rule against the outcome.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].plot(L["ys"], L["revenue"], color=labs.ORANGE)
    ax[0].axvline(L["y_star"], color="k", lw=1, ls="--")
    ax[0].set(title="expected revenue by seats protected", xlabel="seats protected", ylabel="$")
    pol = np.array(D["policy"])
    im = ax[1].imshow(pol[:, 1:].T, origin="lower", aspect="auto", cmap="viridis")
    fig.colorbar(im, ax=ax[1], label="fare, $")
    ax[1].set(title="optimal fare by day and seats left", xlabel="day of the sale", ylabel="seats left")
    lab.fig = fig
    return lab
