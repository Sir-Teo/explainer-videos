"""Lab 24: run the Kac ring forwards, round and backwards, and price Szilard's engine."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import physlaws

TITLE = "A reversible ring with an arrow"
GOAL = ("Run Kac's ring of 4,000 balls: compare the decay of its colour imbalance with (1 - 2 mu)^t, check that it "
        "returns exactly after 2N steps and retraces itself when reversed, run a typical low-entropy state both "
        "ways in time, and compare a Szilard engine's simulated work with kT times the measurement's entropy.")
TASKS = [
    "Shrink the ring to N = 50. How far does the decay now stray from (1 - 2 mu)^t, and at which t does the "
    "theory first fail badly?",
    "In physlaws.kac_both_ways, start from white = 0.99 instead of 0.8. Is the present still an entropy minimum, "
    "and how many steps does either direction take to reach equilibrium?",
    "Put the Szilard partition at x = 0.01. How much work does the rare outcome yield, and what is the average?",
]


def run(seed=0):
    lab = labs.Lab()
    N = 4000
    ring = physlaws.kac_ring(N=N, marker_fraction=0.1, steps=2 * N, seed=seed)
    delta, theory = np.array(ring["delta"]), np.array(ring["theory"])
    early = slice(0, 16)
    gap = float(np.max(np.abs(delta[early] - theory[early])))
    late = float(np.max(np.abs(delta[40:N - 40])))
    lab.row("markers", f"{ring['markers']} of {N} edges (mu = {ring['mu']:.3f})")
    lab.row("imbalance at t = 5", f"{delta[5]:+.3f}   (theory (1 - 2 mu)^5 = {theory[5]:+.3f})")
    lab.row("largest gap from the theory, t <= 15", f"{gap:.3f}")
    lab.row("imbalance at t = N and t = 2N", f"{delta[N]:+.0f} and {delta[2 * N]:+.0f}   (theory {(-1) ** ring['markers']:+d} and +1)")
    assert gap < 0.12, "early decay follows (1 - 2 mu)^t"
    assert late < 0.25, "in between the ring sits near equilibrium"
    assert delta[N] == (-1) ** ring["markers"], "after N steps every ball has crossed every marker once"
    assert delta[2 * N] == 1.0 and ring["returns"], "Zermelo: exact recurrence at 2N, where the theory says 0"
    assert abs(theory[2 * N]) < 1e-3
    assert ring["reverse_returns"], "Loschmidt: the reversed motion goes back to all white"

    both = physlaws.kac_both_ways(N=4000, seed=seed)
    lab.row("entropy now, 30 steps later, 30 steps earlier", f"{both['now']:.3f}, {both['future_end']:.3f}, "
            f"{both['past_end']:.3f} bits")
    assert both["future_end"] > both["now"] + 0.15 and both["past_end"] > both["now"] + 0.15, "a dip, both ways"

    engine = physlaws.szilard(seed=seed)["rows"]
    worst = max(abs(r["simulated_kT"] - r["theory_kT"]) for r in engine)
    half = next(r for r in engine if r["x"] == 0.5)
    lab.row("Szilard engine, partition at 1/2", f"{half['simulated_kT']:.4f} kT   (theory ln 2 = {np.log(2):.4f} kT)")
    lab.row("Szilard engine, worst gap over five partitions", f"{worst:.4f} kT")
    assert worst < 0.03 and all(r["theory_kT"] <= np.log(2) + 1e-9 for r in engine)
    lab.note = ("The same deterministic, reversible ring decays like a dissipative system, comes back exactly, and "
                "from a typical low-entropy present gains entropy in both directions: the dynamics alone gives no "
                "arrow.")

    fig, ax = labs.figure(3, size=(12.5, 4.2))
    t = np.arange(41)
    ax[0].plot(t, delta[:41], "o-", ms=3, color=labs.BLUE, label="the ring")
    ax[0].plot(t, theory[:41], "--", color=labs.GOLD, label="(1 - 2 mu)^t")
    ax[0].set(title="Decay: the first 40 steps", xlabel="step t", ylabel="imbalance (white - black) / N")
    ax[0].legend()
    ax[1].plot(np.arange(2 * N + 1), delta, color=labs.BLUE, lw=1)
    ax[1].axvline(N, color=labs.MUTED, ls=":")
    ax[1].axvline(2 * N, color=labs.RED, ls=":")
    ax[1].set(title=f"Recurrence: {'black' if delta[N] < 0 else 'white'} at N, white at 2N", xlabel="step t",
              ylim=(-1.08, 1.08))
    ax[2].plot(both["t"], both["entropy"], color=labs.GREEN)
    ax[2].axvline(0, color=labs.MUTED, ls=":")
    ax[2].set(title="An 80%-white present, run both ways", xlabel="steps from now", ylabel="entropy (bits)")
    lab.fig = fig
    return lab
