"""Lab 18: social choice and welfare: five voting rules on one profile, the agenda in Condorcet's cycle, Borda's
failure of independence, Arrow's pivotal voter, single peaks, bloc manipulation, Atkinson's family, the two veils,
Scitovsky's reversal, distributional weights, discounting and the value of a statistical life."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import dials
from explainer.economics.agora import choice as ch
from explainer.economics.island import truths

TITLE = "Social choice and welfare: voting rules and welfare functions"
GOAL = ("Count one island's ballots under five rules and get five winners; let the agenda pick the winner of a cycle; "
        "break Borda's independence; find Arrow's pivotal voter; watch the median win on a line; find the blocs that "
        "gain by lying; measure inequality with Atkinson's epsilon; choose between two societies behind two veils; "
        "pass Kaldor's test both ways; and see how weights, discount rates and a statistical life change a decision.")
TASKS = [
    "The ballots: move two voters from the fruit-first group to the dance-first group. How many different winners do "
    "the five rules now give, and is there still a Condorcet winner?",
    "The veil: change society B to (10, 30, 30, 30, 30). At what epsilon does Harsanyi's chooser now switch to A?",
    "The jetty: at what epsilon does the weighted net value of the jetty turn negative? (Solve "
    "30 (31/80)^e = 10 (31/5)^e.)",
]


def run(seed=0):
    lab = labs.Lab()
    T = truths(18)
    prof = [(n, tuple(r)) for n, r in T["playit"]["profile"]]

    w = ch.all_rules(prof)
    assert len(set(w.values())) == 5                                   # five rules, five winners
    lab.row("the 38 ballots: plurality, runoff, instant runoff, Borda, Condorcet",
            ", ".join(f"{k} {v}" for k, v in w.items()))
    bd = ch.borda(prof)["points"]
    lab.row("Borda's points", ", ".join(f"{c} {bd[c]}" for c in sorted(bd)))

    cyc = ch.majority_cycle()
    ag = ch.agendas(cyc["profile"])
    assert all(len(v) == 2 for v in ag.values())                       # each plan wins under two of six agendas
    lab.row("Condorcet's cycle: agendas won by each plan (of six)", ", ".join(f"{c} {len(v)}" for c, v in ag.items()))

    iia = ch.iia_violation(prof)
    lab.row("Borda breaks independence: fish voters' new ballot; pair that flips",
            f"{''.join(iia['after'])}; {''.join(iia['pair'])}")

    pv = ch.geanakoplos_pivot(**T["arrow"])
    lab.row("Arrow: position of b in society as b rises voter by voter (2 = bottom); pivotal voter",
            f"{pv['positions']}; voter {pv['pivot'] + 1}")

    sp = ch.single_peaked(**T["peaks"])
    assert sp["condorcet"] == sp["median"]                              # Black: the median is the Condorcet winner
    lab.row("single peaks: median, mean, Condorcet winner", f"{sp['median']:g}, {sp['mean']:g}, {sp['condorcet']:g}")

    for rule in ("plurality", "instant runoff", "Borda"):
        m = ch.manipulations(prof, rule)[0]
        lab.row(f"{rule}: a bloc's lie", f"the {m['count']} with {''.join(m['truth'])} vote {''.join(m['lie'])}: "
                f"{m['honest_winner']} -> {m['new_winner']}")

    inc = T["incomes"]
    eps = (0.0, 0.5, 1.0, 2.0, 5.0, 50.0)
    wf = ch.welfare(inc, eps)
    assert abs(wf["ede"][1.0] - np.exp(np.mean(np.log(inc)))) < 1e-9   # epsilon one is the geometric mean
    lab.row("Atkinson: equally distributed equivalent at epsilon 0, 0.5, 1, 2, 5, 50",
            ", ".join(f"{wf['ede'][e]:.2f}" for e in eps))

    v = ch.veil(T["veil"]["A"], T["veil"]["B"], (0.0, 1.0, 1.8, 2.0, 5.0))
    lab.row("veils: Rawls chooses; Harsanyi chooses at epsilon 0, 1, 1.8, 2, 5",
            f"{v['rawls']}; " + ", ".join(v["harsanyi"][e] for e in (0.0, 1.0, 1.8, 2.0, 5.0)))

    sc = ch.scitovsky()
    assert sc["1_to_2"] and sc["2_to_1"]                                # the test approves a move and its reverse
    lab.row("Scitovsky: Kaldor's test passes from 1 to 2; from 2 to 1", f"{sc['1_to_2']}; {sc['2_to_1']}")

    mean = float(np.mean(inc))
    jetty = {e: 30 * (mean / max(inc)) ** e - 10 * (mean / min(inc)) ** e for e in (0.0, 0.25, 0.5, 1.0)}
    lab.row("the jetty's weighted net value at epsilon 0, 0.25, 0.5, 1", ", ".join(f"{x:.1f}" for x in jetty.values()))

    d = T["discount"]
    pv_ = {r: d["amount"] / (1 + r) ** d["years"] for r in d["rates"]}
    lab.row(f"a million dollars in {d['years']} years, today, at {', '.join(f'{r:.1%}' for r in d['rates'])}",
            ", ".join(f"${x:,.0f}" for x in pv_.values()))
    t = T["vsl"]
    lab.row("a statistical life: $1,000 for 1 in 10,000", f"${t['extra_pay'] / t['extra_risk'] / 1e6:.0f} million")
    lab.row("the dial (2024 $ million)", ", ".join(f"{e.who} {e.value:.1f}" for e in dials.DIALS["vsl"].estimates))

    lab.note = ("Five rules give five winners from the same 38 ballots, and only the market fair, the Condorcet winner, "
                "is safe from every bloc's lie. Atkinson's equivalent falls from the mean, 31, to 20 at epsilon one and "
                "toward the minimum, 5; Harsanyi's veil chooses the unequal, richer society until epsilon passes about "
                "1.9, while Rawls's always chooses equality. Compensation tests can approve a move and its reverse, "
                "and the jetty that passes unweighted fails at epsilon one half.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    e = np.linspace(0, 8, 161)
    ede = ch.welfare(inc, tuple(float(x) for x in e))["ede"]
    ax[0].plot(e, [ede[float(x)] for x in e], color=labs.BLUE, label="the island's incomes")
    va = ch.welfare(T["veil"]["A"], tuple(float(x) for x in e))["ede"]
    vb = ch.welfare(T["veil"]["B"], tuple(float(x) for x in e))["ede"]
    ax[0].plot(e, [va[float(x)] for x in e], color=labs.ORANGE, ls="--", label="society A (equal)")
    ax[0].plot(e, [vb[float(x)] for x in e], color=labs.ORANGE, label="society B")
    ax[0].axhline(min(inc), color="black", lw=0.8, ls=":")
    ax[0].set(title="Atkinson's family", xlabel="inequality aversion epsilon", ylabel="equally distributed equivalent")
    ax[0].legend()
    yrs = np.arange(0, d["years"] + 1)
    for r in d["rates"]:
        ax[1].plot(yrs, (1 + r) ** -yrs, label=f"{r:.1%}")
    ax[1].set(title="Discounting a century", xlabel="years from now", ylabel="value today of $1 then")
    ax[1].legend()
    lab.fig = fig
    return lab
