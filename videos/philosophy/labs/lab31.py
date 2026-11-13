"""Lab 31: compute a simplified phi by cutting a three-gate loop, and draw a workspace's masking curve."""

import itertools
import math

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import consciousness as cs

TITLE = "Phi by cutting, and a workspace that ignites"
GOAL = ("Recompute the Reasoner's simplified integrated information for the OR, AND, XOR loop from the definition, "
        "in each of its eight states and across each cut, and check it against the library. Then run the global "
        "workspace with noise at six mask delays and check that report is all or none.")
TASKS = [
    "Replace the XOR gate by a COPY of the OR gate. Which cut now loses nothing, and what does that say about "
    "the loop?",
    "In cs.workspace, raise noise from 0.6 to 1.5. Does the half-way delay move, and does the 50 ms histogram "
    "stay bimodal?",
    "Compute phi for a ring of five XOR gates (each reading its two neighbours) in a reachable state, and "
    "compare it with the ring of four.",
]

GATES = {"OR": lambda a, b: a | b, "AND": lambda a, b: a & b, "XOR": lambda a, b: a ^ b}


def cut_loss(names, inputs, x1, part):
    """Effective information of state x1 across the cut part | rest, in bits, straight from the definition: the
    whole's distribution over its pasts against the product of each side's own, inputs across the cut being noise."""
    n = len(names)
    pasts = list(itertools.product((0, 1), repeat=n))
    step = {s: tuple(GATES[names[i]](s[inputs[i][0]], s[inputs[i][1]]) for i in range(n)) for s in pasts}
    causes = [s for s in pasts if step[s] == tuple(x1)]
    if not causes:
        return None
    sides = [tuple(part), tuple(i for i in range(n) if i not in part)]
    q = {s: 1.0 for s in pasts}
    for side in sides:
        ok = [s for s in pasts if all(step[s][i] == x1[i] for i in side)]
        count = {}
        for s in ok:
            key = tuple(s[i] for i in side)
            count[key] = count.get(key, 0) + 1
        for s in pasts:
            q[s] *= count.get(tuple(s[i] for i in side), 0) / len(ok)
    return sum(math.log2((1 / len(causes)) / q[s]) for s in causes) / len(causes)


def run(seed=0):
    lab = labs.Lab()
    names, inputs = cs.NETWORKS["OR, AND, XOR loop"]
    cuts = {name: cut_loss(names, inputs, (1, 1, 1), (i,)) for i, name in enumerate(names)}
    lab.row("state (1,1,1): bits lost cutting off OR, AND, XOR",
            ", ".join(f"{cuts[k]:.3f}" for k in names) + "   (film: 1, 2.585, 2)")
    assert abs(cuts["OR"] - 1) < 1e-9 and abs(cuts["AND"] - math.log2(6)) < 1e-9 and abs(cuts["XOR"] - 2) < 1e-9

    mine, theirs = [], []
    for x1 in itertools.product((0, 1), repeat=3):
        losses = [cut_loss(names, inputs, x1, (i,)) for i in range(3)]
        mine.append(None if losses[0] is None else round(min(losses), 4))  # each cut has a part of size one
        try:
            theirs.append(cs.phi_simple(names, inputs, x1)["phi"])
        except ValueError:
            theirs.append(None)
    show = lambda v: "none" if v is None else f"{v:g}"  # noqa: E731
    lab.row("phi in the eight states, from the definition", "  ".join(show(v) for v in mine))
    lab.row("phi in the eight states, reasoner.consciousness", "  ".join(show(v) for v in theirs))
    assert mine == theirs == [1.0, 1.0, None, None, 1.585, 1.0, 1.0, 1.0], "two states have no past; (1,0,0) has more"

    four = {k: v["phi"] for k, v in cs.phi_examples().items()}
    lab.row("phi of four systems", ";  ".join(f"{k}: {v:g}" for k, v in four.items()))
    assert four["two separate pairs"] == 0 and four["a feedforward chain"] == 0, "no loop, or two systems: phi 0"
    assert four["OR, AND, XOR loop"] == 1 and four["a ring of four XORs"] == 1

    soas, trials = (20, 40, 50, 60, 80, 100), 100
    ws = cs.workspace(soas=soas, trials=trials, seed=2001 + seed)
    seen = np.array([r["seen"] for r in ws["rows"]]) / trials
    lab.row("seen at mask delays 20, 40, 50, 60, 80, 100 ms", "  ".join(f"{s:.0%}" for s in seen))
    lab.row("at 50 ms, activity at 400 ms: low / between / high",
            f"{ws['late_low']} / {trials - ws['late_low'] - ws['late_high']} / {ws['late_high']}")
    assert seen[0] == 0 and seen[-1] >= 0.95, "never seen at 20 ms, almost always at 100 ms"
    assert np.all(np.diff(seen) > -0.05) and 0.1 < seen[2] < 0.9, "a steep sigmoid with its middle near 50 ms"
    assert ws["late_low"] + ws["late_high"] >= 0.95 * trials, "ignition is all or none"
    lab.note = ("Every way of cutting the loop loses information, so its phi is positive and depends on the state; "
                "the workspace's report jumps from never to always within a few tens of milliseconds, with almost "
                "no trial in between.")

    fig, ax = labs.figure(3, size=(12.5, 4.2))
    ax[0].bar(names, [cuts[k] for k in names], color=[labs.GOLD, labs.BLUE, labs.BLUE], width=0.6)
    ax[0].set_axisbelow(True)
    ax[0].set(title="Bits lost cutting off one gate, at (1,1,1)", xlabel="gate cut off (gold: the weakest cut, phi)",
              ylabel="effective information (bits)")
    t = np.arange(len(ws["trace_sub"])) * ws["dt_trace"]
    ax[1].plot(t, ws["trace_sub"], color=labs.RED, label="mask at 30 ms: fades")
    ax[1].plot(t, ws["trace_sup"], color=labs.GREEN, label="mask at 80 ms: ignites")
    ax[1].axhline(50, color=labs.MUTED, ls=":", lw=1)
    ax[1].set(title="The workspace without noise", xlabel="time since the stimulus (ms)", ylabel="activity w")
    ax[1].legend(loc="center right")
    ax[2].plot(soas, 100 * seen, "o-", color=labs.BLUE)
    ax[2].set(title=f"Masking curve, {trials} trials per delay", xlabel="delay between stimulus and mask (ms)",
              ylabel="trials seen (%)", ylim=(-4, 104))
    lab.fig = fig
    return lab
