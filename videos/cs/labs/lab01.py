"""Lab 1: run every two-state Turing machine, find the busy beaver, and time a palindrome checker."""

import numpy as np

from videos.coursekit import labs
from explainer.cs import turing

TITLE = "Busy beavers by brute force, and what one tape costs"
GOAL = ("Run all 20,736 two-state machines from a blank tape and find the one that halts last; rerun the 3- and "
        "4-state champions; then time a one-tape palindrome checker on random palindromes and fit its step count.")
TASKS = [
    "Raise LIMIT from 40 to 400 steps. Does any two-state machine halt later than step 6? Why can no limit prove it for three states?",
    "Count the ones each halting two-state machine leaves (r.ones()) and find the largest: Rado's Sigma(2).",
    "Write the binary incrementer of Problem 1 as a TM and check that it takes 2n + 2 steps on n ones.",
]
LIMIT = 40

# Palindromes on one tape (Chapter 5): cross off the first symbol, run to the far end, check the last, run back.
PALINDROME = turing.TM([
    ("start", "_", "_", "S", "accept"), ("start", "0", "_", "R", "have0"), ("start", "1", "_", "R", "have1"),
    ("have0", "0", "0", "R", "have0"), ("have0", "1", "1", "R", "have0"), ("have0", "_", "_", "L", "want0"),
    ("have1", "0", "0", "R", "have1"), ("have1", "1", "1", "R", "have1"), ("have1", "_", "_", "L", "want1"),
    ("want0", "0", "_", "L", "back"), ("want0", "1", "1", "S", "reject"), ("want0", "_", "_", "S", "accept"),
    ("want1", "1", "_", "L", "back"), ("want1", "0", "0", "S", "reject"), ("want1", "_", "_", "S", "accept"),
    ("back", "0", "0", "L", "back"), ("back", "1", "1", "L", "back"), ("back", "_", "_", "R", "start"),
], start="start", name="palindromes, one tape")


def all_two_state():
    """Every 2-state, 2-symbol table: each of the 4 entries writes 0 or 1, moves L or R, goes to A, B or halt (Z)."""
    acts = [f"{w}{m}{n}" for n in "ABZ" for m in "RL" for w in "01"]
    return [f"{a0}{a1}_{b0}{b1}" for a0 in acts for a1 in acts for b0 in acts for b1 in acts]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. every two-state machine, from a blank tape
    tables = all_two_state()
    halts = []
    for t in tables:
        r = turing.run(turing.TM.parse(t), max_steps=LIMIT)
        if r.state in turing.HALT:
            halts.append(r.steps)
    halts = np.array(halts)
    lab.row("two-state machines", f"{len(tables):,}   ((4n + 4)^(2n) at n = 2: {(4 * 2 + 4) ** 4:,})")
    lab.row("halt within 40 steps", f"{len(halts):,}   (the film: 9,784)")
    lab.row("longest halting run", f"{halts.max()} steps   (S(2) = 6)")
    assert len(tables) == 12 ** 4 and len(halts) == 9784
    assert halts.max() == 6, "no two-state machine halts after step 6"

    # 2. the champions, rerun
    for n in (2, 3, 4):
        table, steps, ones, _, _ = turing.CHAMPIONS[n]
        r = turing.run(turing.TM.parse(table), max_steps=1000, record=True)
        lab.row(f"{n}-state champion {table}", f"{r.steps} steps, {r.ones()} ones")
        assert r.halted and (r.steps, r.ones()) == (steps, ones)
    lo = min(h[1][0] for h in r.history) - 1
    hi = max(h[1][0] for h in r.history) + 1
    picture = turing.spacetime(r, lo, hi)

    # 3. palindromes on one tape: right answers, and about n^2 / 2 steps
    for _ in range(200):
        w = "".join(rng.choice(["0", "1"], rng.integers(0, 13)))
        assert turing.run(PALINDROME, w).state == ("accept" if w == w[::-1] else "reject"), w
    ns = np.arange(4, 61, 4)
    steps = []
    for n in ns:
        half = "".join(rng.choice(["0", "1"], n // 2))
        r1 = turing.run(PALINDROME, half + half[::-1], max_steps=10 ** 5)
        assert r1.state == "accept"
        steps.append(r1.steps)
    steps = np.array(steps)
    coef = np.polyfit(ns, steps, 2)
    lab.row("palindrome of 60 symbols", f"{steps[-1]} steps   (n^2 / 2 = {60 * 60 // 2})")
    lab.row("fitted steps", f"{coef[0]:.3f} n^2 + {coef[1]:.2f} n + {coef[2]:.1f}   (the film: about 0.50 n^2)")
    assert abs(coef[0] - 0.5) < 0.02, "the zig-zag costs n^2 / 2 to leading order"
    lab.note = ("Brute force settles S(2) = 6 because every two-state machine that has not halted by step 6 can be "
                "shown never to halt; the same search for five states took until 2024.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    from matplotlib.colors import ListedColormap

    ax[0].imshow(picture, aspect="auto", interpolation="nearest",
                 cmap=ListedColormap([labs.BG, labs.BLUE, labs.GREY, labs.GOLD]), vmin=0, vmax=3,
                 extent=(lo - 0.5, hi + 0.5, len(picture) - 0.5, -0.5))
    ax[0].grid(False)
    ax[0].set(title="The 4-state champion: 107 steps, 13 ones", xlabel="tape cell (blue: a 1, gold: the head)",
              ylabel="step")
    ax[1].plot(ns, steps, "o", color=labs.BLUE, label="one-tape palindrome machine")
    grid = np.linspace(0, 60, 100)
    ax[1].plot(grid, grid ** 2 / 2, color=labs.GOLD, label="n² / 2")
    ax[1].plot(grid, 3 * grid + 3, color=labs.GREEN, ls="--", label="two tapes: 3n + 3")
    ax[1].set(title="Steps to accept a palindrome of n symbols", xlabel="n", ylabel="steps")
    ax[1].legend()
    lab.fig = fig
    return lab
