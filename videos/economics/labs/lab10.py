"""Lab 10: the price maker: one price, discrimination, durability, Ramsey prices, pass-through and personal prices."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import pricing as pr
from explainer.economics.island import truths

TITLE = "The price maker: monopoly, discrimination and pass-through"
GOAL = ("Find Bo's best fare against a hundred islanders' values and what it turns away; check the monopoly price, "
        "the Lerner rule and pass-through against their closed forms; price students and townsfolk separately; "
        "solve the screening menu and Oi's two-part tariff; watch the Coase conjecture as price changes come faster; "
        "find Ramsey prices; measure pass-through from the bean to the shelf; apply Littlewood's rule; and learn "
        "personal prices from a price experiment.")
TASKS = [
    "Third degree: make the students' demand 80 - 10p. Does one fare now serve both groups? Do two fares still raise "
    "total welfare, and does Varian's output test agree?",
    "Pass-through: write a small demand class for q = (10 - p)^2, with q(p), elasticity(p), and a = 10, b = 1 so "
    "the price search stops at 10. Predict the pass-through from 1 / (2 + q P''/P'), and check it with "
    "pricing.pass_through.",
    "Personal prices: give the buyers' willingness to pay a spread (scale) of 0.6 instead of 0.35. How do the profit "
    "gain, the share who pay less and the fall in consumer surplus change, and what share of buyers buy?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(10)

    # the ferry
    f = T["ferry"]
    v = np.random.default_rng(f["seed"]).uniform(0, f["top"], f["people"])
    fe = pr.ferry(v, f["fares"])
    lab.row("the ferry: best fare; takings; total value of all crossings",
            f"${fe['best_fare']:.2f}; ${fe['best_revenue']:.2f}; ${fe['total_value']:.2f}")
    assert fe["best_revenue"] <= fe["total_value"]

    # one price, the Lerner rule, pass-through
    d0 = T["demand"]
    lin = pr.Linear(d0["a"], d0["b"])
    m = pr.monopoly(lin, d0["c"])
    assert abs(m["p"] - (d0["a"] / d0["b"] + d0["c"]) / 2) < 1e-9 and abs(m["lerner"] - m["inv_elasticity"]) < 1e-9
    ce = pr.ConstantElasticity(1000.0, d0["eps"])
    rho = (pr.pass_through(lin, d0["c"]), pr.pass_through(ce, d0["c"]))
    assert abs(rho[0] - 0.5) < 1e-6 and abs(rho[1] - d0["eps"] / (d0["eps"] - 1)) < 1e-6
    lab.row("monopoly with a $2 cost: price, quantity, Lerner index", f"${m['p']:.2f}, {m['q']:.0f}, {m['lerner']:.3f}")
    lab.row("pass-through: straight-line demand, constant elasticity 3", f"{rho[0]:.3f}, {rho[1]:.3f}")

    # third degree
    g = T["groups"]
    th = pr.third_degree(pr.Linear(*g["students"]), pr.Linear(*g["town"]), g["c"])
    lab.row("third degree: fares; welfare with one fare and with two",
            f"${th['discriminate']['p'][0]:.2f} and ${th['discriminate']['p'][1]:.2f}; "
            f"{th['uniform']['welfare']:.2f} and {th['discriminate']['welfare']:.2f}")
    assert th["discriminate"]["q"] > th["uniform"]["q"]          # Varian: welfare can rise only if output does

    # second degree and two-part tariffs
    s = T["screen"]
    sc = pr.screening(s["lo"], s["hi"], s["share_hi"])
    assert abs(sc["qL"] - (s["lo"] - s["share_hi"] / (1 - s["share_hi"]) * (s["hi"] - s["lo"]))) < 1e-9
    lab.row("screening: low quality, high quality, information rent", f"{sc['qL']:.3f}, {sc['qH']:.3f}, "
                                                                     f"{sc['rent']:.3f}")
    r = T["rides"]
    ns, nb = r["mix"]
    tp = pr.two_part([pr.Linear(*r["small"])] * ns + [pr.Linear(*r["big"])] * nb, r["c"])
    lab.row("two-part tariff for two ordinary visitors and a keen one: ride price, fee, profit; keen one alone",
            f"${tp['p']:.2f}, ${tp['fee']:.2f}, ${tp['profit']:.2f}; ${tp['profit_without_smallest']:.2f}")

    # durability
    du = T["durable"]
    firsts = []
    for n in du["per_year"]:
        c = pr.coase(np.exp(-du["r"] / n), periods=du["years"] * n)
        firsts.append(c["first_price"])
    lab.row("Coase: first price (thousands) with 1, 4, 12, 52, 365 price changes a year",
            ", ".join(f"{x:.3f}" for x in firsts))
    assert all(a > b for a, b in zip(firsts, firsts[1:]))

    # Ramsey prices
    ra = T["ramsey"]
    rm = pr.ramsey(pr.ConstantElasticity(ra["A"][0], ra["eps"][0]), pr.ConstantElasticity(ra["A"][1], ra["eps"][1]),
                   ra["c"][0], ra["c"][1], ra["F"])
    lab.row("Ramsey: markups as shares of the price; loss against a uniform markup",
            f"{rm['markups'][0]:.3f}, {rm['markups'][1]:.3f}; {rm['loss_ramsey']:.2f} against {rm['loss_uniform']:.2f}")
    assert rm["loss_ramsey"] <= rm["loss_uniform"]

    # pass-through from bean to shelf
    shelf = data.fred("APU0000717311")
    bean = data.pinksheet("arabica")
    sm = {dt[:7]: x for dt, x in zip(shelf["date"], shelf["value"])}
    bm = dict(zip(bean["month"], bean["value"]))
    months = [k for k in sorted(sm) if k in bm and np.isfinite(sm[k]) and np.isfinite(bm[k])]
    S = np.log([sm[k] for k in months])
    B = np.log([bm[k] for k in months])
    dS, dB = np.diff(S), np.diff(B)
    L = 18                                                       # eighteen months of lags, on monthly data
    X = np.column_stack([np.ones(len(dS) - L)] + [dB[L - j:len(dB) - j] for j in range(L + 1)])
    beta, *_ = np.linalg.lstsq(X, dS[L:], rcond=None)
    cum = np.cumsum(beta[1:])
    lab.row("coffee, monthly: shelf on bean, cumulative elasticity after 0, 6, 12, 18 months",
            ", ".join(f"{cum[k]:.3f}" for k in (0, 6, 12, 18)))

    # Littlewood
    lw = pr.littlewood(40, 4.0, 10.0, 12, 5)
    lab.row("Littlewood: seats to protect (rule, simulation); expected takings", f"{lw['protect_rule']}, "
                                                                               f"{lw['protect_best']}; "
                                                                               f"${lw['revenue_best']:.2f}")
    assert lw["protect_rule"] == lw["protect_best"]

    # personal prices
    pp = pr.personalized(n_test=100_000)
    lab.row("personal prices: profit gain, share paying less, change in consumer surplus",
            f"{100 * pp['profit_gain']:.1f}%, {100 * pp['share_pay_less']:.1f}%, {100 * pp['cs_change']:.1f}%")
    assert pp["personal"]["profit"] > pp["uniform"]["profit"]
    lab.note = ("The best fare leaves value on the table that a price for every buyer would collect; the monopoly "
                "price and the Lerner rule match their closed forms; two fares raise output and welfare when they "
                "open a market; the screening menu cuts the low type's quality; time erodes a durable-goods "
                "monopolist's power; Ramsey prices lose less than a uniform markup; coffee's shelf price takes up "
                "about half of a change in the bean price, slowly; and personal prices raise profit while most "
                "buyers pay less.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    grid = np.linspace(0, f["top"], 401)
    ax[0].plot(grid, [x * np.sum(v >= x) for x in grid], color=labs.ORANGE, lw=2)
    ax[0].axvline(fe["best_fare"], color="goldenrod", ls="--")
    ax[0].set(title="Bo's takings against the fare", xlabel="fare ($)", ylabel="takings ($)")
    ax[1].bar(np.arange(L + 1), cum, color=labs.BLUE)
    ax[1].set(title="Coffee: cumulative pass-through, monthly", xlabel="months after the bean price moves",
              ylabel="shelf % per bean %")
    lab.fig = fig
    return lab
