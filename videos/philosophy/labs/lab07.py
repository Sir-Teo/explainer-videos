"""Lab 7: run every two-state Turing machine, check the champions, and test Löb's axiom on every small GL frame."""

import numpy as np

from videos.coursekit import labs
from explainer.philosophy.reasoner import arith

TITLE = "Busy beavers, the β-function and provability logic, computed"
GOAL = ("Run all 20,736 two-state Turing machines and compare the longest halting run with the published busy beaver "
        "number; code a random list with Gödel's β-function; and check on every finite GL frame with up to four "
        "worlds that Löb's axiom and the second incompleteness theorem hold while reflection fails.")
TASKS = [
    "Raise CAP from 50 to 200. Does any further machine halt? Explain why that is evidence and not yet a proof.",
    "Run arith.CHAMPIONS[5] with arith.run_tm_fast and confirm 47,176,870 steps and 4,098 ones (a few seconds).",
    "Check the formula '[]p -> [][]p' with arith.gl_valid, then '[][]p -> []p'. Which one does GL prove, and why?",
]
CAP = 50


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # every two-state machine, run from a blank tape
    halt_steps, running = [], 0
    for tm in arith.all_machines(2):
        r = arith.run_tm(tm, CAP)
        if r["halted"]:
            halt_steps.append(r["steps"])
        else:
            running += 1
    halt_steps = np.array(halt_steps)
    total = len(halt_steps) + running
    search = arith.busy_beaver_search(2, CAP)
    lab.row("two-state machines", f"{total:,}   (12 choices for each of 4 rules: 12^4 = {12 ** 4:,})")
    lab.row(f"halt within {CAP} steps", f"{len(halt_steps):,}   still running: {running:,}")
    lab.row("longest halting run, most ones", f"{search['max_steps']} steps, {search['max_ones']} ones   (Radó 1962: 6, 4)")
    assert total == 12 ** 4 == search["machines"] and len(halt_steps) == search["halting"] == 9784
    assert halt_steps.max() == search["max_steps"] == 6 and search["max_ones"] == 4

    # the champions, simulated
    published = {2: (6, 4), 3: (21, 5), 4: (107, 13)}
    for n, (steps, ones) in published.items():
        r = arith.run_tm(arith.parse_tm(arith.CHAMPIONS[n]))
        assert r["halted"] and (r["steps"], r["ones"]) == (steps, ones), n
    lab.row("champions for 2, 3, 4 states", "6, 21, 107 steps; 4, 5, 13 ones   (as published)")

    # Gödel's beta function on a random list, and a formula numbered and decoded
    seq = [int(a) for a in rng.integers(0, 12, size=int(rng.integers(3, 6)))]
    c, d = arith.beta_code(seq)
    decoded = [arith.beta(c, d, i) for i in range(len(seq))]
    assert decoded == seq
    moduli = [1 + (i + 1) * d for i in range(len(seq))]
    assert all(np.gcd(a, b) == 1 for i, a in enumerate(moduli) for b in moduli[i + 1:]), "pairwise coprime moduli"
    lab.row(f"the list {seq}", f"d = {d:,}, c has {len(str(c))} digits; β(c, d, i) gives back {decoded}")
    formula = "∀x(x+0=x)"
    g = arith.godel_number(formula)
    assert arith.godel_decode(g) == formula and arith.godel_number("0=0") == 2 ** 21 * 3 ** 15 * 5 ** 21
    lab.row(f"Gödel number of {formula}", f"{len(str(g))} digits, decoded back to {arith.godel_decode(g)}")

    # provability logic on every finite GL frame with up to four worlds
    verdict = {k: arith.gl_valid(arith.GL_FACTS[k]) for k in ("lob", "second", "reflection")}
    assert verdict["lob"] == (True, 242) and verdict["second"] == (True, 242) and not verdict["reflection"][0]
    lab.row("Löb's axiom, Gödel II as a formula", f"valid on all {verdict['lob'][1]} GL frames with at most 4 worlds")
    lab.row("reflection, []p -> p", f"fails on frame number {verdict['reflection'][1]}: soundness is not provable")
    lab.note = ("Six steps is the most any halting two-state machine takes, but the search alone cannot show that the "
                f"{running:,} machines still running never halt: that needs a proof for each, which is why BB is not "
                "computable.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    from matplotlib.colors import ListedColormap
    counts = np.bincount(halt_steps, minlength=8)[1:8]
    ax[0].bar(np.arange(1, 8), counts, color=labs.BLUE, label="machines halting at exactly this step")
    for k, v in enumerate(counts, start=1):
        ax[0].text(k, v + 80, f"{v:,}", ha="center", color=labs.INK, fontsize=9)
    ax[0].annotate("BB(2) = 6: the last step\nat which any machine halts", xy=(6, counts[5] + 350), xytext=(4.6, counts.max() * 0.55),
                   color=labs.GOLD, ha="center", arrowprops=dict(arrowstyle="->", color=labs.GOLD))
    ax[0].set_axisbelow(True)
    ax[0].set(title=f"All {total:,} two-state machines: when the halting ones halt", xlabel="step at which the machine halts",
              ylabel="machines", ylim=(0, counts.max() * 1.25))
    ax[0].legend(loc="upper right")
    rows = arith.space_time(arith.CHAMPIONS[4], 107)
    grid = np.array([r[0] for r in rows], dtype=float)
    ax[1].imshow(grid, aspect="auto", cmap=ListedColormap([labs.PANEL, labs.GOLD]), interpolation="nearest", vmin=0, vmax=1,
                 extent=(-0.5, grid.shape[1] - 0.5, len(rows) - 0.5, -0.5))
    ax[1].plot([r[1] for r in rows], np.arange(len(rows)), color=labs.BLUE, lw=1.2, label="the head")
    ax[1].grid(False)
    ax[1].set(title="Brady's four-state champion: 107 steps, 13 ones", xlabel="tape cell", ylabel="step")
    ax[1].legend(loc="lower left")
    lab.fig = fig
    return lab
