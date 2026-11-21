"""Lab 64: machines that learn: the Island's bail courts with a random forest, the policy frontier, contraction and
selective labels, targeting by risk against by effect, double machine learning, prediction-powered inference, a neural
network trained on Euler errors, pricing agents, fairness by group, and the value of what the judge can see."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import learn as L

TITLE = "Machines that learn"
GOAL = ("Train a model on the decisions of the Island's judges, evaluate it without the outcomes they hid, and use "
        "machine learning for causal effects, measurement, model solving and markets, with the truth known.")
TASKS = [
    "Make the judges see more in court (L.courts(signal=1.2)). Does the algorithm still beat them, and does the "
    "contraction design notice?",
    "Use a weaker classifier (L.text_measure(sens=0.7, spec=0.9)). How much narrower is prediction-powered inference "
    "than the hand labels now?",
    "Raise the discount factor in the Euler network (L.euler_net(beta=0.99)). Does it still find alpha beta?",
]


def run(seed=0):
    lab = labs.Lab()
    C = L.courts(seed=64 + seed)
    P = L.policy_curves(C)
    lab.row("the courts: judges' detention and failures per 100; the forest's failures at the same detention",
            f"{100 * P['judges']['detain']:.0f}%, {100 * P['judges']['crime']:.1f}; {100 * P['alg_at_judges']:.1f} "
            f"({100 * P['crime_cut']:.0f}% fewer)")
    K = L.contraction(C)
    lab.row("contraction: the algorithm against stricter judges (failures per 100)",
            ", ".join(f"{100 * r['algorithm']:.1f} vs {100 * r['judges']:.1f}" for r in K["rows"]))
    lab.row("filling in the detained's outcomes: naive against true failures per 100",
            f"{100 * K['naive']:.1f} against {100 * K['truth']:.1f}")
    T = L.targeting(seed=64 + seed)
    lab.row("a job programme, unemployment averted per 100 places: random, by risk, by estimated effect, best",
            ", ".join(f"{T['per100'][k]:.1f}" for k in ("at random", "highest risk", "largest effect (estimated)",
                                                         "largest effect (truth)")))
    D = L.dml_study(reps=8, seed=64 + seed)
    lab.row("double ML over 8 samples: no controls, linear controls, plug-in, double ML (truth 1)",
            ", ".join(f"{D[k]['mean']:.2f}" for k in ("no controls", "linear controls", "plug-in ML", "double ML")))
    X = L.text_measure(reps=200, seed=64 + seed)
    lab.row("the share of layoff news (truth 12%): classifier; hand labels and PPI with their interval widths",
            f"{100 * X['classifier']['mean']:.1f}%; {100 * X['hand-labelled']['width']:.1f} and "
            f"{100 * X['prediction-powered']['width']:.1f} points")
    E = L.euler_net(seed=64 + seed)
    assert E["max_err"] < 0.01                                   # Brock and Mirman's closed form, found
    lab.row("the Euler network's saving rate against alpha beta", f"largest gap {E['max_err']:.5f}")
    A = L.pricing_agents(sessions=3, seed=seed)
    lab.row("Q-learning price setters: profit gain in three sessions (0 Nash, 1 monopoly)",
            ", ".join(f"{r['gain']:.2f}" for r in A["rows"]))
    F = L.fairness()
    lab.row("a calibrated score, two groups: false positive and false negative rates",
            f"A {100 * F['A']['fpr']:.0f}% and {100 * F['A']['fnr']:.0f}%, B {100 * F['B']['fpr']:.0f}% and "
            f"{100 * F['B']['fnr']:.0f}%")
    S = L.signal_sweep(signals=(0.0, 0.9, 1.8), n=20000, trees=40, seed=64 + seed)
    lab.row("the algorithm's advantage as the judges see more (signal 0, 0.9, 1.8)",
            ", ".join(f"{100 * r['crime_cut']:+.0f}%" for r in S["rows"]))
    t = data.transistors()
    b = np.polyfit(t["year"], np.log2(t["transistors"]), 1)[0]
    lab.row("transistors per microprocessor: doubling time, 1971-2021", f"{1 / b:.2f} years")

    lab.note = ("The forest predicts; the designs (random judges, contraction, trials, cross-fitting, a hand-labelled "
                "sample) are what make its predictions answer questions.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].plot(100 * np.array(P["grid"]), 100 * np.array(P["crime"]), color="tab:blue", label="algorithm")
    ax[0].scatter([100 * q["detain"] for q in P["quintiles"]], [100 * q["crime"] for q in P["quintiles"]],
                  color=labs.ORANGE, label="judges by leniency")
    ax[0].set(title="the bail frontier", xlabel="share detained, %", ylabel="failures per 100")
    ax[0].legend(fontsize=8)
    for k, col in (("linear controls", labs.ORANGE), ("double ML", "tab:green")):
        ax[1].hist(D[k]["draws"], bins=8, alpha=0.7, color=col, label=k)
    ax[1].axvline(1.0, color="k", ls="--", lw=1)
    ax[1].set(title="double machine learning", xlabel="estimate of theta (truth 1)", ylabel="samples")
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
