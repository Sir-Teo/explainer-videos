"""Lab 30: run one mind in two substrates, test supervenience on random worlds, and find a law of gliders."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import mind

TITLE = "One role, two realizers; three kinds of supervenience"
GOAL = ("Feed a network of threshold units and a water tank the same 1000 inputs and compare their behaviour with "
        "each other and with the machine table's long-run prediction, check the implications between weak, strong "
        "and global supervenience on random sets of worlds, and count the live cells of Gosper's glider gun.")
TASKS = [
    "Write a third realizer of mind.TABLE (say, the state as the position of a marble in one of three cups) and "
    "run it in lockstep with the other two.",
    "Change the table so that aspirin never soothes (('hurt', 'aspirin') always stays 'hurt'). Recompute the "
    "long-run frequencies. Which output disappears?",
    "Search the random world sets for one where weak supervenience holds and global fails, and one where global "
    "holds and weak fails. What do the film's sets A and B have in common with them?",
]
WEIGHTS = {"bump": 0.3, "nothing": 0.5, "aspirin": 0.2}        # how often mind.realizers gives each input


def _long_run():
    """The table as a Markov chain on the three states: its stationary law, and the share of each output."""
    S = mind.STATES
    P = np.zeros((3, 3))
    for (s, i), opts in mind.TABLE.items():
        for p, nxt, _ in opts:
            P[S.index(s), S.index(nxt)] += WEIGHTS[i] * p
    vals, vecs = np.linalg.eig(P.T)
    pi = np.real(vecs[:, np.argmax(np.real(vals))])
    pi /= pi.sum()
    out = {}
    for (s, i), opts in mind.TABLE.items():
        for p, _, o in opts:
            out[o] = out.get(o, 0.0) + pi[S.index(s)] * WEIGHTS[i] * p
    return pi, out


def _random_worlds(rng):
    """A set of two or three worlds, each with two or three individuals with a physical and a mental state."""
    n_ind = int(rng.integers(2, 4))
    return [{f"x{k}": (f"P{rng.integers(1, 3)}", f"M{rng.integers(1, 3)}") for k in range(n_ind)}
            for _ in range(int(rng.integers(2, 4)))]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. multiple realizability
    r = mind.realizers(steps=1000, seed=seed)
    pi, theory = _long_run()
    lab.row("neural units and water tank, 1000 steps", f"outputs agree at {r['agree']} steps")
    assert r["agree"] == r["steps"], "the two substrates realize one machine table"
    first = r["trace"][:3]
    lab.row("their physical states at steps 0, 1, 2", ", ".join(f"{t['neural']} / {t['hydraulic']}" for t in first))
    worst = 0.0
    for o in ("carry on", "say ouch", "wince", "sigh"):
        got = r["outputs"].get(o, 0) / r["steps"]
        worst = max(worst, abs(got - theory[o]))
        lab.row(f"share of '{o}'", f"{got:.3f}   (the table's long run: {theory[o]:.3f})")
    assert worst < 0.07, "behaviour follows the table, whatever it is made of"
    assert abs(sum(theory.values()) - 1) < 1e-9 and abs(pi.sum() - 1) < 1e-9

    # 2. supervenience
    film = mind.supervenience()
    assert [film[k][j] for k in "ABC" for j in ("weak", "strong", "global")] == [True, False, False, False, False,
                                                                                 True, True, True, True]
    tally = {"strong": 0, "weak only": 0, "global only": 0}
    for _ in range(600):
        ws = _random_worlds(rng)
        w, s, g = mind._weak(ws), mind._strong(ws), mind._global(ws)
        assert not s or (w and g), "strong supervenience implies weak and global"
        tally["strong"] += s
        tally["weak only"] += w and not g
        tally["global only"] += g and not w
    lab.row("600 random sets of worlds", f"strong holds in {tally['strong']}, and always with weak and global")
    lab.row("weak without global / global without weak", f"{tally['weak only']} / {tally['global only']}")
    assert tally["weak only"] > 0 and tally["global only"] > 0, "weak and global are independent"

    # 3. a law at the level of gliders
    law = mind.glider_law(gens=300, size=160)
    lab.row("Gosper's gun: live cells = 36 + 5k at generation 30k", f"holds at {law['holds']} of {law['points']} checks")
    assert law["holds"] == law["points"] == 11
    lab.note = ("What the two machines share is the table, not the stuff; strong supervenience is the strongest of "
                "the three relations and the other two do not imply each other; and the gun obeys a law that "
                "mentions gliders, not cells.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    names = ["carry on", "say ouch", "wince", "sigh"]
    x = np.arange(4)
    ax[0].bar(x - 0.2, [r["outputs"].get(o, 0) / r["steps"] for o in names], 0.4, color=labs.BLUE,
              label="both realizers, 1000 steps")
    ax[0].bar(x + 0.2, [theory[o] for o in names], 0.4, color=labs.GOLD, label="the machine table's long run")
    ax[0].set_xticks(x, names)
    ax[0].set_axisbelow(True)
    ax[0].set(title="Behaviour of the pain role, in units and in water", ylabel="share of steps")
    ax[0].grid(False, axis="x")
    ax[0].legend(loc="upper right")
    gens = np.arange(len(law["pop"]))
    ax[1].plot(gens, law["pop"], color=labs.BLUE, lw=1.2, label="live cells")
    ax[1].scatter([p["gen"] for p in law["rows"]], [p["pop"] for p in law["rows"]], s=30, color=labs.GOLD, zorder=3,
                  label="every 30 generations")
    ax[1].plot(gens, 36 + gens / 6, color=labs.MUTED, ls="--", lw=1, label="36 + 5k at generation 30k")
    ax[1].set(title="Gosper's glider gun: a law about gliders", xlabel="generation", ylabel="live cells")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
