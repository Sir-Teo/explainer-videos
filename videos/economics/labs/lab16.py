"""Lab 16: auctions: the four formats on the same draws, Vickrey's dominance, shading, revenue equivalence and its
failures, Myerson's reserve, the winner's curse, position auctions, the exposure problem and demand reduction."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import auctions as au
from explainer.economics.data import tables
from explainer.economics.island import truths

TITLE = "Auctions: formats, reserves and the winner's curse"
GOAL = ("Run five auction formats on the same draws of private values and see revenue equivalence; derive and check "
        "first-price shading; measure what risk aversion does to it; find Myerson's reserve and compare it with an "
        "extra bidder; measure the winner's curse; price slots by Vickrey's rule; and watch a uniform price invite "
        "demand reduction.")
TASKS = [
    "Formats: rerun the five formats with n = 2 and n = 10 bidders. Does every format still raise (n - 1)/(n + 1)? "
    "How does the spread of the first-price and second-price revenue change?",
    "Risk: set alpha = 0.25 (more risk averse). How much does the first-price auction now raise, and why is the "
    "second-price auction unchanged?",
    "The winner's curse: double the noise to 6. How does the winner's overestimate change with 2 and with 32 bidders?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(16)
    f = T["formats"]

    sim = au.simulate_formats(n=f["n"], draws=f["draws"], seed=f["seed"] + seed)
    for name, r in sim["formats"].items():
        assert abs(r["mean"] - sim["theory"]) < 5 * r["se"] + 0.002, name
    lab.row("five formats, four bidders: mean revenue (theory 0.6)",
            ", ".join(f"{k} {v['mean']:.3f}" for k, v in sim["formats"].items()))

    p = au.expected_profit(**T["playit"])
    lab.row("Play it: best bids (pay your bid / pay the next); expected profit in each",
            f"{p['best_first']:.1f} / {p['best_second']:.0f}; {p['profit_first']:.2f} / {p['profit_second']:.2f}")

    r = au.simulate_formats(n=f["n"], draws=f["draws"], seed=f["seed"] + seed, alpha=T["risk"]["alpha"])
    lab.row("risk-averse bidders (alpha 0.5): first-price / second-price revenue",
            f"{r['formats']['first-price']['mean']:.3f} / {r['formats']['second-price']['mean']:.3f}")

    m2, m3 = au.myerson(2), au.myerson(3)
    lab.row("Myerson, two bidders: best reserve, revenue with it, without it; three bidders, no reserve",
            f"{m2['r_star']:.2f}, {m2['rev_star']:.4f}, {m2['rev_zero']:.4f}; {m3['rev_zero']:.4f}")

    c = T["curse"]
    w = au.winners_curse(c["ns"], c["value"], c["noise"], seed=c["seed"] + seed)
    lab.row("the winner's overestimate for 2, 4, 8, 16, 32 bidders (exact)",
            ", ".join(f"{x['overestimate']:.2f} ({x['exact']:.2f})" for x in w["rows"]))
    j = tables.BAZERMAN_SAMUELSON_1983.data
    lab.row("the jar of coins: value, mean estimate, mean winning bid, mean loss",
            f"${j['value']:.2f}, ${j['mean_estimate']:.2f}, ${j['mean_winning_bid']:.2f}, ${j['mean_loss']:.2f}")

    g = au.gsp(**T["gsp"])
    lab.row("slots: Vickrey totals; per click; the top bidder's profit in slots 1-3 if all bid their values",
            f"{g['vcg_total']}; {[round(x, 2) for x in g['gsp_price_per_click']]}; {g['deviation_profits_top']}")

    x = T["exposure"]
    for rv in x["rivals"]:
        e = au.exposure(x["both"], x["alone"], rv)
        lab.row(f"exposure, locals {rv}: bold national profit; cautious and bold surplus; best",
                f"{e['bold']['national_profit']:.0f}; {e['cautious']['welfare']:.0f}, {e['bold']['welfare']:.0f}; "
                f"{e['efficient_welfare']:.0f}")

    b = au.multi_unit(**T["bonds"])
    lab.row("two bonds: Bo's profit bidding for two / for one / under Vickrey; revenue in each",
            f"{b['truthful']['big_profit']:.0f} / {b['best']['big_profit']:.0f} / {b['vickrey']['big_profit']:.0f}; "
            f"{b['truthful']['revenue']:.0f} / {b['best']['revenue']:.0f} / {b['vickrey']['revenue']:.0f}")

    lab.note = ("Every format raises the same on average, but the first-price auction's price varies less; risk "
                "averse bidders bid more when they pay their bids; the best reserve adds a quarter with two bidders, "
                "a third bidder adds more; the highest of many honest estimates overstates the value, more so the more "
                "bidders; Vickrey's prices for slots are 6.2, 5 and 4 a click, and truthful bidding in the "
                "second-price auction for slots is not an equilibrium; and a uniform price pays a big buyer to ask "
                "for less.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    rs = np.asarray(m2["reserve"])
    ax[0].plot(rs, m2["revenue"], color=labs.ORANGE, lw=2, label="two bidders, reserve r")
    ax[0].axhline(m3["rev_zero"], color=labs.BLUE, ls="--", label="three bidders, no reserve")
    ax[0].set(title="Myerson's reserve", xlabel="reserve price", ylabel="expected revenue")
    ax[0].legend()
    ns = [x["n"] for x in w["rows"]]
    ax[1].plot(ns, [x["overestimate"] for x in w["rows"]], color=labs.ORANGE, lw=2, marker="o", label="simulated")
    ax[1].plot(ns, [x["exact"] for x in w["rows"]], color=labs.BLUE, ls="--", label="3 (n - 1)/(n + 1)")
    ax[1].set(xscale="log", title="The winner's curse", xlabel="bidders", ylabel="winner's overestimate")
    ax[1].legend()
    lab.fig = fig
    return lab
