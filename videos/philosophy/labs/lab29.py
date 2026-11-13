"""Lab 29: test three kinds of present on every melody, plan for Dennett's robots, and wait for a world to return."""

import itertools
import math

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import phenomenology as ph

TITLE = "A present with a tail, a planner with a frame, a world that returns"
GOAL = ("Count the melodies that a knife-edge, a two-note and a fading present can tell apart, let a planner fetch "
        "the battery from Dennett's room as irrelevant fluents are added, and run reversible cellular automata "
        "with random rules until their first state comes back.")
TASKS = [
    "Allow repeated notes: call _fading_states(3, 5, d) for decays d from 0.5 to 0.7. Where do collisions start, "
    "and what equation does 0.618 satisfy?",
    "Give R1 the full model but forbid 'remove_bomb' (filter it out of ph._actions). Is there still a plan, and "
    "what does the planner report?",
    "Run ph.reversible_ca(n, 150) for n = 12 to 20 and plot the return times. Which ring sizes return quickly, and "
    "can you say why?",
]


def _fading_states(n_pitches, length, decay):
    """How many melodies with repeated notes a fading present tells apart (the library's test uses distinct notes)."""
    seen = set()
    for m in itertools.product(range(n_pitches), repeat=length):
        w = np.zeros(n_pitches)
        for age, note in enumerate(reversed(m)):
            w[note] += decay ** age
        seen.add(tuple(np.round(w, 9)))
    return len(seen)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the living present
    film = ph.retention(5, 0.5)
    d = film["distinct"]
    lab.row("120 melodies of five notes", f"knife-edge {d['knife']}, two-note window {d['window']}, fading trace "
            f"{d['retention']}   (theory 5, 20, 120)")
    assert (d["knife"], d["window"], d["retention"], film["decoded"]) == (5, 20, 120, 120)
    tried = []
    for _ in range(6):
        n, decay = int(rng.integers(3, 7)), float(rng.uniform(0.1, 0.9))
        r = ph.retention(n, decay)
        tried.append((n, round(decay, 2)))
        assert r["distinct"]["retention"] == r["decoded"] == math.factorial(n), "any decay in (0, 1) keeps the order"
        assert r["distinct"]["knife"] == n and r["distinct"]["window"] == n * (n - 1)
    lab.row("six random (notes, decay) pairs", f"every ordering told apart and read back: {tried}")
    edge = (ph.retention(5, 0.0)["distinct"]["retention"], ph.retention(5, 1.0)["distinct"]["retention"])
    lab.row("at the ends: decay 0 and decay 1", f"{edge[0]} and {edge[1]} melodies told apart")
    assert edge == (5, 1), "no tail is the knife-edge; a tail that does not fade keeps the notes and loses the order"
    half, golden = _fading_states(3, 5, 0.5), _fading_states(3, 5, (math.sqrt(5) - 1) / 2)
    lab.row("243 melodies with repeated notes", f"decay 0.5 tells apart {half}, decay 0.618 only {golden}")
    assert half == 243 and golden < 243, "with repeats the order survives at 1/2 and not at the golden ratio"

    # 2. the frame problem
    ax_rows = ph.axiom_counts()["rows"]
    lab.row("100 actions, 1000 fluents", f"{ax_rows[-1]['frame_axioms']} frame axioms against {ax_rows[-1]['ssa']} "
            f"successor-state axioms")
    rob = ph.robots(irrelevant=tuple(range(0, 9)))
    lab.row("R1's plan", f"{rob['r1_plan']}: bomb out = {rob['r1_outcome']['bomb_out']}")
    lab.row("with successor-state axioms", f"{rob['plan']}")
    assert rob["r1_outcome"]["bomb_out"] and rob["plan"] == ["open_door", "remove_bomb", "pull_wagon_out"]
    rows = rob["rows"]
    lab.row("states expanded, 0 and 8 irrelevant fluents", f"{rows[0]['expanded']} and {rows[-1]['expanded']}; told what "
            f"is relevant: {rows[-1]['expanded_relevant']}")
    assert all(a["expanded"] < b["expanded"] and a["derived"] < b["derived"] for a, b in zip(rows, rows[1:]))
    assert all(r["expanded_relevant"] == rows[0]["expanded"] and r["plan_len"] == 3 for r in rows)

    # 3. recurrence: any rule, made reversible, returns on a finite ring
    worlds = []
    for _ in range(12):
        n, rule = int(rng.integers(5, 10)), int(rng.integers(0, 256))
        t, _ = ph.reversible_ca(n, rule)
        assert t is not None and t <= 4 ** n, "a finite reversible world returns within its number of states"
        worlds.append((n, rule, t))
    lab.row("12 random reversible worlds", f"all return; longest wait {max(w[2] for w in worlds)} steps "
            f"(rule {max(worlds, key=lambda w: w[2])[1]})")
    t11, _ = ph.reversible_ca(11, 150)
    simmel = ph.recurrence(sizes=(5,))["simmel"][-1]
    lab.row("rule 150 on 11 cells returns after", f"{t11} steps   (film: 93)")
    lab.row("Simmel's wheels up to time 100000", f"closest approach {simmel['closest']} of a turn, at time {simmel['at']}")
    assert t11 == 93 and simmel["closest"] > 0
    lab.note = ("A present needs a fading tail to hold a melody's order; a planner with complete axioms still does "
                "work that grows with everything irrelevant; and a finite reversible world must return, while "
                "three wheels with an irrational ratio never do.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    k = [r["irrelevant"] for r in rows]
    ax[0].plot(k, [r["derived"] for r in rows], "o-", color=labs.RED, label="facts deduced, every action considered")
    ax[0].plot(k, [r["derived_relevant"] for r in rows], "o-", color=labs.GREEN, label="facts deduced, told what is relevant")
    ax[0].plot(k, [r["expanded"] for r in rows], "s--", color=labs.GOLD, label="states expanded, every action considered")
    ax[0].set(title="Dennett's room: the same three-step plan, more work", xlabel="irrelevant fluents in the room",
              ylabel="count", yscale="log")
    ax[0].legend(loc="upper left")
    sizes = list(range(5, 17))
    for rule, color in ((150, labs.BLUE), (90, labs.PURPLE), (30, labs.ORANGE)):
        ax[1].plot(sizes, [ph.reversible_ca(n, rule)[0] for n in sizes], "o-", color=color, label=f"rule {rule}")
    ax[1].plot(sizes, [4.0 ** n for n in sizes], color=labs.MUTED, ls="--", label="number of states, 4^n")
    ax[1].set(title="Steps until a reversible ring of n cells returns", xlabel="cells n", ylabel="return time", yscale="log")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
