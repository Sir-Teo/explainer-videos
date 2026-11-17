"""Lab 27: the criterion problem in masking, binocular rivalry from inhibition and adaptation, the workspace's
ignition, integrated information for small networks, and the readiness potential from accumulated noise."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import workspace as W

TITLE = "Consciousness"
GOAL = ("Show that 'unseen' trials can be above chance with one representation and a strict criterion; build "
        "rivalry from two inhibiting populations; find the workspace's ignition threshold; compute phi for small "
        "networks; and make a readiness potential out of noise.")
TASKS = [
    "Let the criterion for 'seen' fall as the masking interval grows (people become more liberal when stimuli are "
    "clearer). Can accuracy on unseen trials then fall as the interval grows?",
    "Compute phi for one ring of eight copying nodes and for two separate rings of four (W.network('ring_copy', 4) "
    "twice, joined into one list with indices shifted). Which is more integrated, and why?",
    "Lower the workspace's self-excitation w from 6 to 4 in W.ignition. Is late activity still all or none?",
]


def run(seed=0):
    out = labs.Lab()

    # 1. masking
    for c in (1.0, 1.5, 2.0):
        r = W.masking(1.7, c)
        out.row(f"d = 1.7, seen if |x| > {c}: P(seen), accuracy when unseen",
                f"{r['p_seen']:.2f}, {r['acc_unseen']:.3f}")
    assert W.masking(1.7, 2.0)["acc_unseen"] > W.masking(1.7, 1.0)["acc_unseen"] > 0.5

    # 2. rivalry
    r = W.rivalry(T=300.0, seed=seed)
    d = W.dominance_durations(r["u"], r["dt"])
    out.row("rivalry: dominance periods, mean (s), gamma shape", f"{len(d['all'])}, {d['mean1'] / 2 + d['mean2'] / 2:.2f}, "
            f"{d['shape']:.1f}")
    assert 1.5 < d["shape"] < 10

    # 3. ignition
    s = np.round(np.arange(0.5, 1.25, 0.05), 2)
    g = W.ignition(s, n_trials=200, seed=seed)
    k = int(np.argmin(np.abs(g["p_ignite"] - 0.5)))
    out.row("P(ignite) by strength", ", ".join(f"{x:.2f}" for x in g["p_ignite"]))
    out.row("threshold strength; late activity halfway (0.2-0.6) there",
            f"{s[k]:.2f}; {np.mean((g['late'][k] > 0.2) & (g['late'][k] < 0.6)):.3f}")

    # 4. phi
    for kind, n in (("pairs", 6), ("chain", 6), ("ring_copy", 6), ("all_or", 5)):
        p = W.phi(W.network(kind, n))
        out.row(f"phi: {kind} ({n} nodes); weakest cut", f"{p['phi']:.2f}; {p['mib']}")
    assert W.phi(W.network("ring_copy", 6))["phi"] == 2.0

    # 5. the readiness potential
    sc = W.schurger(T=600.0, seed=seed)
    b = W.back_average(sc["x"], sc["hits"], sc["dt"], 2.0)
    out.row("movements; median wait (s); averaged activity 2 s and 0 s before",
            f"{len(sc['hits'])}; {np.median(sc['waits']):.1f}; {b['mean'][0]:.3f}, {b['mean'][-1]:.3f}")

    out.note = ("A strict criterion alone produces 'unconscious perception'; inhibition and adaptation make rivalry's "
                "skewed durations; a recurrent network ignites all or none; phi is zero for parts that do not talk "
                "and two bits for a ring; and a ramp appears whenever you average backward from threshold crossings.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    soas = np.linspace(0, 150, 61)
    for c, col in ((1.0, labs.BLUE), (2.0, labs.GOLD)):
        v = W.visibility_curve(soas, c_seen=c)
        ax[0].plot(soas, v["acc_unseen"], color=col, label=f"seen if |x| > {c}")
    ax[0].axhline(0.5, ls="--", color="#888888")
    ax[0].set(title="Accuracy on 'unseen' trials", xlabel="target-mask interval (ms)", ylabel="proportion correct")
    ax[0].legend()
    ax[1].plot(b["t"], b["mean"], color=labs.GOLD)
    ax[1].set(title="A readiness potential from noise", xlabel="time before movement (s)", ylabel="mean activity")
    out.fig = fig
    return out
