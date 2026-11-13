"""Lab 26: test the CHSH inequality on every local strategy, on random angles, and in the game."""

import math

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import quantum as qm

TITLE = "Bell's inequality, tested three ways"
GOAL = ("Compute the singlet's correlations from its state vector at random measurement angles, compare S with the "
        "local bound 2 and Tsirelson's bound 2 sqrt 2, mix local strategies with shared randomness, and play the CHSH "
        "game with a shared Bell pair.")
TASKS = [
    "Replace the singlet by the product state |01> (state=np.array([0, 1, 0, 0], complex) in qm.correlation). "
    "What is the largest |S| over the same random angles?",
    "Change Bob's angles in the game from plus and minus 45 degrees to plus and minus 30 degrees (copy "
    "qm.chsh_game and edit ang_b). What is the winning rate, and what does the formula predict?",
    "Extend qm.ghz to four particles with the state (|0000> + |1111>)/sqrt 2: find four products of X and Y whose "
    "eigenvalues no assignment of values can reproduce.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    tsirelson = 2 * math.sqrt(2)

    # 1. every local deterministic strategy, and mixtures of them (shared randomness)
    base = qm.chsh()
    lab.row("16 local deterministic strategies", f"S takes the values {base['local_values']}   (bound: |S| <= 2)")
    assert base["local_max"] == 2
    outcomes = rng.choice([-1, 1], size=(4000, 4))                 # A0, A1, B0, B1 for each hidden state
    weights = rng.dirichlet(np.ones(4000))
    A0, A1, B0, B1 = outcomes.T
    s_mix = float(weights @ (A0 * B0 + A0 * B1 + A1 * B0 - A1 * B1))
    lab.row("a random mixture of 4000 instruction sets", f"S = {s_mix:+.3f}")
    assert abs(s_mix) <= 2 + 1e-12, "shared randomness cannot pass the local bound"

    # 2. the singlet at random angles: S from the state vector
    angles = rng.uniform(0, 2 * math.pi, size=(3000, 4))
    S = np.empty(len(angles))
    for i, (a, a2, b, b2) in enumerate(angles[:300]):                # the first 300 from the 4 x 4 matrices
        S[i] = (qm.correlation(a, b) + qm.correlation(a, b2) + qm.correlation(a2, b) - qm.correlation(a2, b2))
        closed = -(math.cos(a - b) + math.cos(a - b2) + math.cos(a2 - b) - math.cos(a2 - b2))
        assert abs(S[i] - closed) < 1e-9, "the singlet's correlation is -cos(a - b)"
    a, a2, b, b2 = angles[300:].T
    S[300:] = -(np.cos(a - b) + np.cos(a - b2) + np.cos(a2 - b) - np.cos(a2 - b2))
    above = float(np.mean(np.abs(S) > 2))
    lab.row("singlet, 3000 random angle choices", f"largest |S| = {np.abs(S).max():.3f}   (Tsirelson: {tsirelson:.3f})")
    lab.row("share of angle choices with |S| > 2", f"{above:.1%}")
    lab.row("singlet at 0, 90, 45, -45 degrees", f"|S| = {base['abs_S']}   (theory {base['tsirelson']})")
    assert np.abs(S).max() <= tsirelson + 1e-9 and np.abs(S).max() > 2.5, "above the local bound, never above Tsirelson's"
    assert 0.05 < above < 0.6, "most angle choices show no violation: the angles have to be chosen"
    assert abs(base["abs_S"] - tsirelson) < 1e-3

    # 3. the game
    trials = 4000
    game = qm.chsh_game(trials=trials, seed=seed)
    theory = math.cos(math.pi / 8) ** 2
    se = math.sqrt(theory * (1 - theory) / trials)
    counts = sorted({s["wins_of_4"] for s in game["strategies"]})
    lab.row("classical strategies: wins out of 4", f"{counts}, so the best wins {game['classical_best']:.2f}")
    lab.row(f"quantum strategy, {trials} games", f"{game['quantum_rate']:.3f}   (theory {theory:.3f}, s.e. {se:.3f})")
    assert game["classical_best"] == 0.75
    assert abs(game["quantum_rate"] - theory) < 4 * se and game["quantum_rate"] > 0.75 + 8 * se
    gz, pm = qm.ghz(), qm.peres_mermin()
    lab.row("GHZ: consistent local assignments", f"{gz['consistent_assignments']} of {gz['assignments']}")
    lab.row("Peres-Mermin: consistent assignments", f"{pm['consistent_assignments']} of {pm['assignments']}, "
            f"best meets {pm['best_constraints_met']} of 6")
    assert gz["consistent_assignments"] == 0 and pm["consistent_assignments"] == 0 and pm["best_constraints_met"] == 5
    lab.note = ("No assignment of predetermined local answers passes |S| = 2 or wins the game more than 3/4 of the "
                "time; the singlet does both, and stops at 2 sqrt 2.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    deg = np.array([r["angle_deg"] for r in base["curve"]])
    keep = deg <= 180
    ax[0].plot(deg[keep], np.array([r["quantum"] for r in base["curve"]])[keep], color=labs.BLUE,
               label="singlet: -cos(angle)")
    ax[0].plot(deg[keep], np.array([r["linear"] for r in base["curve"]])[keep], color=labs.GOLD, ls="--",
               label="a local model: straight line")
    pts = np.array([0, 30, 45, 60, 90, 120, 135, 150, 180])
    ax[0].scatter(pts, [qm.correlation(0.0, math.radians(d)) for d in pts], s=28, color=labs.INK, zorder=3,
                  label="computed from the state vector")
    ax[0].set(title="Correlation against the angle between the detectors", xlabel="angle between settings (degrees)",
              ylabel="E(a, b)")
    ax[0].legend(loc="upper left")
    counts, _, _ = ax[1].hist(np.abs(S), bins=np.linspace(0, 3, 61), color=labs.BLUE, alpha=0.75,
                             label="singlet, random angles")
    ax[1].set_ylim(0, 1.4 * counts.max())
    ax[1].axvline(2, color=labs.GOLD, lw=1.6, label="local bound 2")
    ax[1].axvline(tsirelson, color=labs.RED, lw=1.6, label="Tsirelson's bound 2.83")
    ax[1].set(title="|S| over 3000 random choices of four angles", xlabel="|S|", ylabel="angle choices")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
