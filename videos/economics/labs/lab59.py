"""Lab 59: the expert witness: a merger of two office-supply chains reviewed as an agency and a court would, with the
truth known: market definition, concentration, pricing pressure, simulation under four demand curves, pass-through,
a vertical bargaining model, a cartel's overcharge, a labour-market merger and the price regression."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import merger as M

TITLE = "The expert witness"
GOAL = ("Review the Island's merger of Alder and Birch as an agency economist would, then check each tool against the "
        "truth the Island knows.")
TASKS = [
    "Run the hypothetical-monopolist test for Alder and Cedar (M.hmt(candidate=(0, 2))). Is that pair a market too?",
    "Change the nesting parameter to 0.1 (params={'sigma': 0.1} in M.equilibrium) and recompute the diversion from "
    "Alder to Birch. Why does it fall, and what happens to the GUPPI?",
    "In the vertical model, find the departure rate that makes the merger neutral when the channel's bargaining weight "
    "is 0.3 instead of 0.5 (M.vertical(share_channel=0.3)['threshold']).",
]


def run(seed=0):
    lab = labs.Lab()
    eq = M.equilibrium(np.ones(4, bool))
    lab.row("a town with all three chains: prices of Alder, Birch, Cedar, the shops",
            ", ".join(f"{p:.2f}" for p in eq["p"]))
    for q in M.playit_pairs():
        lab.row(f"{q['name']}: diversion, margin, critical diversion, one market?",
                f"{q['D']:.2f}, {q['M']:.2f}, {q['critical']:.2f}, {'yes' if q['one_market'] else 'no'}")
    for name, c in (("Alder alone", (0,)), ("Alder and Birch", (0, 1)), ("the three superstores", (0, 1, 2))):
        h = M.hmt(candidate=c)
        lab.row(f"hypothetical monopolist of {name}: actual loss, critical loss, passes?",
                f"{100 * h['actual_loss']:.1f}%, {100 * h['critical_loss']:.1f}%, {'yes' if h['passes'] else 'no'}")
    for r in M.industries():
        lab.row(f"{r['name']}: HHI after, its rise; presumed in 1982, 2010, 2023",
                f"{r['post']:.0f}, {r['delta']:.0f}; " + ", ".join("yes" if r["verdict"][y] else "no"
                                                                   for y in (1982, 2010, 2023)))
    U = M.upp()
    a, b = U["products"]["Alder"], U["products"]["Birch"]
    lab.row("GUPPI of Alder and Birch; simulated price rises", f"{100 * a['guppi']:.1f}%, {100 * b['guppi']:.1f}%; "
            f"{100 * U['simulation']['dp'][0]:.1f}%, {100 * U['simulation']['dp'][1]:.1f}%")
    lab.row("cost cuts that would hold prices (compensating marginal-cost reductions)",
            ", ".join(f"{100 * x:.1f}%" for x in U["cmcr"]))
    F = M.functional_forms()
    lab.row("one data set, four curves: linear, logit, log-linear, constant elasticity",
            ", ".join(f"{x:.1f}%" for x in F["rise"]))
    P = M.pass_through()
    lab.row("pass-through of a 2% saving: Alder alone; Alder and Birch merged",
            f"{100 * P['single']:.0f}%; {100 * P['merged'][0]:.0f}%, {100 * P['merged'][1]:.0f}%")
    V = M.vertical()
    lab.row("vertical: the rival's fee rise; rivals' extra cost against the saving; break-even departure rate",
            f"${V['fee_rise']:.2f} ({V['rise_pct']:.0f}%); {V['rival_cost']:.2f} vs {V['edm']:.2f}; "
            f"{100 * V['threshold']:.1f}%")
    C = M.cartel(seed=59 + seed)
    assert abs(C["estimate"] - C["truth"]) < 0.02    # the before-during-after regression finds the planted overcharge
    lab.row("the cement cartel: estimated overcharge (planted 18%); damages, $ millions; trebled",
            f"{100 * C['estimate']:.1f}%; {C['damages'] / 1e3:.0f}; {3 * C['damages'] / 1e3:.0f}")
    L = M.labour_merger()
    lab.row("two hospitals merge: nurses' wage before and after; the markdown before and after",
            f"{L['before'][0]:.2f} to {L['after'][0]:.2f}; {L['markdown_before']:.0f}% to {L['markdown_after']:.0f}%")
    T = M.towns(n=30, seed=59 + seed)
    R0, R1 = M.price_regression(T, controls=False), M.price_regression(T)
    lab.row("thirty towns: Birch's effect on Alder's price, without and with controls; the merger's true effect",
            f"{R0['birch']:.1f}%, {R1['birch']:.1f}%; {R1['true_merger']:.1f}%")

    lab.note = ("Every tool answers a narrower question than the law's: the screen asks about diversion and margins, "
                "the simulation about a demand curve no one has seen away from today's prices, the regression about "
                "the towns in its sample. The retrospective is how they are scored.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].bar(range(4), F["rise"], color=[labs.GREEN, labs.BLUE, labs.ORANGE, labs.RED])
    ax[0].axhline(F["guppi"], color="k", lw=1, ls="--")
    ax[0].set_xticks(range(4), ["linear", "logit", "log-linear", "const. el."])
    ax[0].set(title="the same data, four simulated price rises (dashed: GUPPI)", ylabel="%")
    ax[1].plot(C["t"], C["price"], color="k", lw=1, label="price")
    ax[1].plot(C["t"], C["but_for"], color=labs.GREEN, lw=1, label="but-for")
    ax[1].axvspan(C["start"], C["end"], color=labs.RED, alpha=0.1)
    ax[1].set(title="the cement cartel and its but-for price", xlabel="month", ylabel="$ a tonne")
    ax[1].legend(frameon=False)
    lab.fig = fig
    return lab
