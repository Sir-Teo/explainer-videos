"""Lab 15: spillovers: the externality and Pigou's tax, Coase's bargain, public goods, free riding with and without
punishment, the commons, prices against quantities, the bottleneck, and lock-in."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import public as pb
from explainer.economics.data import tables
from explainer.economics.island import truths

TITLE = "Spillovers: externalities, public goods and the commons"
GOAL = ("Find the market and efficient output with a spillover and Pigou's tax; run Coase's cattle and corn under each "
        "liability rule, with and without transaction costs; solve a public good by Samuelson's condition, voluntary "
        "provision and Lindahl's prices; play the shared pot with Agora's typed players; find open-access and "
        "efficient fishing effort; compare a tax and a cap under uncertainty; price Vickrey's bottleneck; and watch "
        "two standards lock in.")
TASKS = [
    "The kiln: double the marginal damage (d = 1). How many pots are efficient now, what is Pigou's tax, and how much "
    "larger is the triangle the market leaves?",
    "The fishery: raise the cost of a boat from 0.3 to 0.6. How do open-access effort, the efficient effort and the "
    "stock left at open access change? Why does a higher cost leave more fish?",
    "The bottleneck: double the cost of arriving late (gamma = 80). How long is the longest queue, and what is the "
    "equilibrium cost per commuter?",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(15)

    k = pb.externality(**T["kiln"])
    assert abs(k["q_with_tax"] - k["q_social"]) < 1e-12
    lab.row("kiln: market and efficient pots; Pigou's tax; triangle", f"{k['q_market']:.0f}, {k['q_social']:.0f}; "
            f"{k['tax']:.0f}; {k['dwl']:.2f}")

    c0 = pb.coase(T["coase"]["values"])
    c2 = pb.coase(T["coase"]["values"], transaction_cost=2.0)
    assert tables.COASE_1960.data["crop_loss_tons"] == (1, 3, 6, 10)
    lab.row("Coase: best herd; liable / not liable; with a $2 transaction cost", f"{c0['k_star']}; {c0['liable']} / "
            f"{c0['not_liable']}; {c2['liable']} / {c2['not_liable']}")

    g = pb.public_good(T["lighthouse"]["thetas"], T["lighthouse"]["mc"])
    lab.row("lighthouse: Samuelson's G; voluntary G; Lindahl shares", f"{g['g_star']:.0f}; {g['g_nash']:.0f}; "
            + ", ".join(f"{x:.1f}" for x in g["lindahl_shares"]))

    v = dict(T["vcm"])
    v["seed"] = v["seed"] + seed
    a, b = pb.vcm(**v, punish=False), pb.vcm(**v, punish=True)
    lab.row("shared pot: share given in rounds 1 and 10, without / with punishment",
            f"{a['share'][0]:.2f} -> {a['share'][-1]:.2f} / {b['share'][0]:.2f} -> {b['share'][-1]:.2f}")

    f = pb.fishery(**T["fishery"])
    lab.row("fishery: open-access, efficient and max-yield effort; stock at open access and efficient",
            f"{f['e_oa']:.1f}, {f['e_mey']:.1f}, {f['e_msy']:.1f}; {f['stock_oa']:.2f}, {f['stock_mey']:.2f}")

    for mb, mc in T["weitzman"]["cases"]:
        w = pb.prices_quantities(mb, mc, T["weitzman"]["sigma"], seed=1974 + seed)
        lab.row(f"Weitzman, benefit slope {mb}, cost slope {mc}: loss with tax / quota (simulated)",
                f"{w['loss_tax']:.4f} / {w['loss_quota']:.4f} ({w['loss_tax_sim']:.4f} / {w['loss_quota_sim']:.4f})")

    bt = pb.bottleneck(**T["bottleneck"])
    lab.row("bottleneck: longest queue (minutes); cost per commuter; total, queue and schedule cost",
            f"{bt['max_wait_min']:.0f}; {bt['cost_each']:.1f}; {bt['total_cost']:,.0f}, {bt['queue_cost']:,.0f}, "
            f"{bt['schedule_cost']:,.0f}")

    li = pb.lock_in(**{**T["lockin"], "seed": T["lockin"]["seed"] + seed})
    lab.row("lock-in: winners of 12 runs; adopters before each run locked in",
            "".join(li["winners"]) + "; " + ", ".join(str(x) for x in li["lock_at"]))

    ch = tables.CHEUNG_1973.data
    lab.row("Cheung's rents per hive: spring (money + nectar), summer",
            f"{ch['pollination_season']['money']:.2f} + {ch['pollination_season']['nectar']:.2f}, "
            f"{ch['honey_season']['money']:.2f} + {ch['honey_season']['nectar']:.2f}")
    lab.note = ("The kiln overproduces until Pigou's tax of 18 restores 36 pots; Coase's herd is 2 under either rule "
                "when bargaining is free, and 3 when it costs more than the bargain gains; a lighthouse worth 9 hours "
                "gets 3 from volunteers; giving decays without punishment and holds with it; open access dissipates "
                "the fishery's rent; a tax beats a cap when costs are steeper than benefits, and loses when they are "
                "not; a toll halves the bottleneck's cost; and which standard wins is the luck of the first adopters.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].plot(f["effort"], f["revenue"], color=labs.BLUE, lw=2, label="the catch's value")
    ax[0].plot(f["effort"], f["cost"], color=labs.ORANGE, lw=2, label="the boats' cost")
    ax[0].axvline(f["e_oa"], color="grey", ls="--")
    ax[0].axvline(f["e_mey"], color="green", ls="--")
    ax[0].set(title="Gordon's fishery", xlabel="boats", ylabel="shells a season")
    ax[0].legend()
    ax[1].plot(a["rounds"], a["share"], color=labs.ORANGE, lw=2, marker="o", label="no punishment")
    ax[1].plot(b["rounds"], b["share"], color=labs.BLUE, lw=2, marker="o", label="punishment allowed")
    ax[1].set(ylim=(0, 1), title="The shared pot", xlabel="round", ylabel="share given")
    ax[1].legend()
    lab.fig = fig
    return lab
