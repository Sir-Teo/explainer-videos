"""Lab 36: score Parfit's sequence under four views, search for each view's counterexample, and discount a century."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import population as pop

TITLE = "Four best worlds, a cross in every row, and two discount rates"
GOAL = ("Score Parfit's sequence A to Z under the total, average, critical-level and variable-value views and "
        "recompute each view's best world from its formula; test the average view's verdict on 500 random mere "
        "additions; run the search for violations of six conditions; and check the Ramsey present values and the "
        "value of a point of extinction risk against their closed forms.")
TASKS = [
    "Change the sequence so that each step keeps 45% of the welfare (shrink=0.45). Which views change their "
    "best world, and why does the total view no longer reach Z?",
    "Raise the critical level from 2 to 20. Where on the sequence does the critical-level view now stop, and "
    "what does the sadistic example (pop.sadistic_example) score?",
    "Discount at Weitzman's declining rate instead: average the factors exp(-0.01 t) and exp(-0.05 t). What is "
    "a million dollars in 100 and in 400 years worth, against the constant 3% rate?",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    seq = pop.parfit_sequence()
    k = np.arange(11)
    n, w = 2.0 ** k, 100 * 0.55 ** k
    mine = {"total": n * w, "average": w, "critical level": n * (w - 2), "variable value": w * 50 * (1 - np.exp(-n / 50))}
    names = [r["name"] for r in seq["rows"]]
    best = {v: names[int(np.argmax(x))] for v, x in mine.items()}
    lab.row("best world on Parfit's sequence, from the formulas", ",  ".join(f"{v}: {b}" for v, b in best.items()))
    assert best == {"total": "Z", "average": "A", "critical level": "D", "variable value": "E"}, "four views, four worlds"
    assert all(seq["best"][v] == best[v] for v in best), "the Reasoner agrees"
    for v, x in mine.items():
        assert np.allclose([r[v] for r in seq["rows"]], x, atol=1e-3), v
    z = seq["rows"][-1]
    lab.row("Z against A", f"{z['n']} people at {z['w']:.2f} each: total {z['total']:.0f} against 100")
    assert z["w"] < 0.3 and z["total"] > 2.5 * seq["rows"][0]["total"], "the repugnant conclusion, on the total view"

    agree = 0
    for _ in range(500):
        base = [(int(rng.integers(1, 30)), float(rng.uniform(-5, 15)))]
        add = (int(rng.integers(1, 30)), float(rng.uniform(-5, 15)))
        worse = pop.average(base + [add]) < pop.average(base)
        agree += worse == (add[1] < pop.average(base))
    lab.row("average view: 'worse' exactly when the added lives are below average", f"{agree} of 500 random additions")
    assert agree == 500

    table = pop.arrhenius_table()["violations"]
    lab.row("conditions each view violates", ";  ".join(f"{v}: {len(c)}" for v, c in table.items()))
    assert all(len(c) >= 1 for c in table.values()), "a cross in every row"
    assert table["total"] == ["quality"] and len(table["average"]) == 3 and "non-sadism" in table["critical level"]
    assert not any(c in ("dominance", "non-anti-egalitarianism") for cs in table.values() for c in cs)
    sad = pop.sadistic_example()
    lab.row("critical level 2: add one life at -1, or five at +1", f"{sad['with_misery']:g} against "
            f"{sad['with_good_lives']:g}   (total view: {sad['total_with_misery']:g} against {sad['total_with_good']:g})")
    assert sad["with_misery"] > sad["with_good_lives"] and sad["total_with_misery"] < sad["total_with_good"]

    ram = pop.ramsey()["views"]
    pv = {}
    for name, (delta, eta, g) in (("Stern", (0.1, 1.0, 1.3)), ("Nordhaus", (1.5, 2.0, 2.0))):
        r = delta + eta * g
        pv[name] = 1e6 / (1 + r / 100) ** 100
        assert abs(ram[name]["r"] - r) < 1e-9 and abs(ram[name]["pv"][100] - pv[name]) < 1
    lab.row("a million dollars in a century, today", f"Stern (1.4%) ${pv['Stern']:,.0f};  Nordhaus (5.5%) "
            f"${pv['Nordhaus']:,.0f};  ratio {pv['Stern'] / pv['Nordhaus']:.0f}")
    assert round(pv["Stern"]) == 249003 and round(pv["Nordhaus"]) == 4729

    ex = pop.existential()
    lab.row("one point less extinction risk this century is worth", f"{ex['constant_gain']:.3f} centuries if risk "
            f"stays 1 in 6;  {ex['perils_gain']:.0f} if it then falls to 1 in 10,000")
    assert abs(ex["constant_gain"] - 0.01 / (1 / 6)) < 1e-3 and abs(ex["perils_gain"] - 0.01 / 1e-4) < 0.5
    lab.note = ("Each view is one line of arithmetic and each picks a different world; each also fails at least "
                "one condition that seems undeniable, which is what Arrhenius's theorems say must happen. How "
                "much the far future weighs then turns on two numbers: the discount rate and the risk that "
                "follows this century.")

    fig, ax = labs.figure(2, size=(11.5, 4.4))
    for (v, x), color in zip(mine.items(), (labs.RED, labs.BLUE, labs.GOLD, labs.GREEN)):
        ax[0].plot(k, x / x.max(), "o-", ms=4, color=color, label=f"{v}: best {best[v]}")
    ax[0].axhline(0, color=labs.MUTED, lw=1)
    ax[0].set(title="Parfit's sequence, each view as a share of its best", xlabel="world (each step: twice the "
              "people, 55% of the welfare)", ylabel="value / best value", xticks=k, xticklabels=names,
              ylim=(-0.6, 1.5))
    ax[0].legend(loc="upper center", ncol=2)
    t = np.arange(0, 201)
    ax[1].plot(t, 1e6 / 1.014 ** t, color=labs.GREEN, label="Stern: r = 0.1 + 1 x 1.3 = 1.4%")
    ax[1].plot(t, 1e6 / 1.055 ** t, color=labs.RED, label="Nordhaus: r = 1.5 + 2 x 2 = 5.5%")
    ax[1].axvline(100, color=labs.MUTED, ls=":")
    ax[1].set(title="Present value of $1 million of future damage", xlabel="years from now",
              ylabel="dollars today", yscale="log")
    ax[1].legend(loc="lower left")
    lab.fig = fig
    return lab
