"""Lab 13: lemons and signals: unravelling, guarantees, signalling, screening, selection measured, testing for
private information, credit rationing and reputation."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import info
from explainer.economics.data import tables
from explainer.economics.island import truths

TITLE = "Lemons and signals: markets with private information"
GOAL = ("Solve Akerlof's market with an additive and a proportional premium; find a single buyer's best blind offer; "
        "check a guarantee's separation; solve Spence's signalling game and Rothschild and Stiglitz's screening "
        "market with its existence condition; rebuild the Einav-Finkelstein diagram from Alcoa's published estimates; "
        "simulate a death spiral and the positive-correlation test; find a bank's rationing rate; and update a "
        "seller's reputation review by review.")
TASKS = [
    "Lemons: make quality uniform on [20, 100] instead of [0, 100] with a $30 premium. Where does the price settle, "
    "and what share of boats trades? Why does raising the worst quality help the best boats?",
    "Rothschild and Stiglitz: lower the careless owners' loss probability from 0.4 to 0.25. Does the separating menu "
    "still exist with 30% careless, and how much cover do the careful now get?",
    "Einav-Finkelstein: double the cost curve's slope (0.155 to 0.31). How do the competitive price, the efficient "
    "price and the welfare triangle change?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(13)
    b = T["boats"]

    add = info.lemons(b["lo"], b["hi"], b["premium"], "add")
    mult = info.lemons(b["lo"], b["hi"], 1.5, "mult")
    assert abs(add["p_eq"] - 2 * b["premium"]) < 1e-6 and mult["share_traded"] == 0
    lab.row("lemons: price and share traded (+$30); with Akerlof's x1.5", f"{add['p_eq']:.0f}, "
            f"{add['share_traded']:.2f}; {mult['share_traded']:.2f}")
    offers = info.lemons_offers(np.arange(0, 101), b["lo"], b["hi"], b["premium"])
    best = max(offers, key=lambda o: o["expected_gain"])
    lab.row("a single buyer's best blind offer and its expected gain", f"{best['p']:.0f}, {best['expected_gain']:.2f}")

    w = T["warranty"]
    g = info.warranty(w["good"], w["bad"], w["share_good"], w["fix"], w["break_good"], w["break_bad"])
    lab.row("guarantee: good sellers offer it; bad ones copy; it separates",
            f"{g['good_offers']}, {g['bad_mimics']}, {g['separates']}")

    sp = T["spence"]
    s = info.spence(sp["theta_low"], sp["theta_high"], sp["cost_low"], sp["cost_high"], sp["share_high"])
    lab.row("Spence: separating range; pooling wage", f"[{s['e_min']:.1f}, {s['e_max']:.1f}]; {s['pool_wage']:.2f}")

    sc = T["screen"]
    rs = info.rothschild_stiglitz(sc["W"], sc["d"], sc["p_low"], sc["p_high"], sc["share_high"])
    lab.row("Rothschild-Stiglitz: careful cover and premium; exists; threshold share",
            f"{rs['x_low']:.2f}, {rs['prem_low']:.3f}; {rs['exists']}; {rs['share_threshold']:.3f}")

    d = tables.EFC_2010.data
    e = info.einav_finkelstein(d["demand"][0], d["demand"][1], d["cost"][0], d["cost"][1])
    assert abs(e["loss"] - d["loss"]) < 0.3
    lab.row("Einav-Finkelstein-Cullen: competitive and efficient prices; triangle (paper $9.55)",
            f"{e['p_eq']:.1f}, {e['p_eff']:.1f}; {e['loss']:.2f}")

    rows = info.death_spiral(**{**T["spiral"], "seed": T["spiral"]["seed"] + seed})["rows"]
    lab.row("death spiral: share enrolled, year by year", ", ".join(f"{r['share']:.3f}" for r in rows))

    dr = T["drivers"]
    pc = {k: info.positive_correlation(dr["n"], k, dr["seed"] + seed)["corr"] for k in ("adverse", "none",
                                                                                         "advantageous")}
    lab.row("positive-correlation test: adverse, none, advantageous",
            ", ".join(f"{pc[k]:.3f}" for k in ("adverse", "none", "advantageous")))

    c = T["credit"]
    sw = info.stiglitz_weiss(c["s_safe"], c["y_safe"], c["s_risky"], c["y_risky"], c["share_safe"],
                             c["collection_cost"])
    lab.row("credit: the bank's best rate and expected repayment per $100", f"{sw['R_star']:.1f}, "
            f"{sw['return_star']:.2f}")

    rp = T["reputation"]
    rep = info.reputation(rp["prior"], rp["honest_good"], rp["cheat_good"], rp["feedback"], rp["value_honest"],
                          rp["value_cheat"])
    lab.row("reputation: price at the start, before and after the bad review, at the end",
            f"{rep['price'][0]:.1f}, {rep['price'][3]:.1f}, {rep['price'][4]:.1f}, {rep['price'][-1]:.1f}")
    lab.note = ("Bad boats drive out good: with a $30 premium only the worst 60% trade, and with Akerlof's x1.5 nothing "
                "does; a guarantee separates because it is cheap only for good sellers; schooling can sort without "
                "teaching; insurers' menus sort but may have no equilibrium when the careless are rare; the Alcoa "
                "triangle is under ten dollars a head; generous plans can spiral away; the correlation test can come "
                "out zero or negative despite private information; banks ration credit at the rate the safe borrowers "
                "can bear; and one bad review costs a new seller dearly.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].plot(add["prices"], add["value_offered"], color=labs.BLUE, lw=2, label="+$30")
    ax[0].plot(mult["prices"], mult["value_offered"], color=labs.ORANGE, lw=2, label="x1.5")
    ax[0].plot([0, 100], [0, 100], color="grey", ls="--")
    ax[0].set(title="Akerlof: what the average boat offered is worth", xlabel="price", ylabel="value to a buyer")
    ax[0].legend()
    ax[1].plot(e["D"], e["demand"], color="black", lw=2, label="demand")
    ax[1].plot(e["D"], e["ac"], color=labs.ORANGE, lw=2, label="average cost")
    ax[1].plot(e["D"], e["mc"], color=labs.BLUE, lw=2, label="marginal cost")
    ax[1].set(ylim=(0, 1000), title="Einav-Finkelstein: Alcoa", xlabel="share insured", ylabel="$ a year")
    ax[1].legend()
    lab.fig = fig
    return lab
