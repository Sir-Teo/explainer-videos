"""Lab 13: put the Job and nine random programs into SSA, and check that their registers colour exactly."""

from videos.coursekit import labs
import copy

import numpy as np

from explainer.cs.lang import pebble_lang as P
from explainer.cs.lang.compiler import analysis as AN
from explainer.cs.lang.compiler import check as C
from explainer.cs.lang.compiler import fuzz as F
from explainer.cs.lang.compiler import interp as IT
from explainer.cs.lang.compiler import lower as L
from explainer.cs.lang.compiler import opt as O
from explainer.cs.lang.compiler import ssa as S

TITLE = "SSA interference graphs are chordal, until the copies come back"
GOAL = ("Lower the Job and nine fuzzer-generated programs with the series' compiler, put every function into SSA, "
        "optimize it, and check three claims of the part: dominators match their definition, the SSA interference "
        "graph is chordal and colours with exactly as many registers as its largest clique, and the optimized "
        "program prints what the unoptimized one prints.")
TASKS = [
    "Skip O.optimize(f) and compare the clique sizes. Which functions need fewer registers after optimization?",
    "Pebble may allocate 13 registers. Count the functions whose SSA graph needs more, then lower the budget to 4 as in the film's register sweep.",
    "Print AN.find_hole(after) for the Job's function 'same' and find the four values in str(f). Which of them are copies that replaced a phi?",
]
PROGRAMS = 9
STEPS = 60_000  # the reference interpreter's budget per program
REGISTERS = 13  # the registers Pebble may allocate


def module(prog):
    """Lower a parsed program to three-address code on a control-flow graph (loops inverted, as at level 2)."""
    prog = copy.deepcopy(prog)
    return L.lower(prog, C.check(prog), rotate=True)


def dominators_by_deletion(f):
    """d dominates n iff n is d or n cannot be reached from the entry once d is deleted (Chapter 4's definition)."""
    lab, labels = f.labels(), [b.label for b in f.blocks]
    out = set()
    for d in labels:
        seen, stack = set(), ([] if d == labels[0] else [labels[0]])
        while stack:
            x = stack.pop()
            if x not in seen and x != d:
                seen.add(x)
                stack += lab[x].succs()
        out |= {(d, n) for n in labels if n == d or n not in seen}
    return out


def output(m):
    try:
        return bytes(IT.run(m, b"", max_steps=STEPS).out)
    except IT.Stuck:
        return None  # the reference run hit the step limit: excluded, as in the film's fuzzer


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    job = P.parse(P.JOB)
    sources = [("Job", job)] + [(f"fuzz {s}", P.parse(F.program(int(s)))) for s in rng.integers(0, 10 ** 6, PROGRAMS)]
    rows, dom_pairs, compared, same = [], 0, 0, 0
    for name, src in sources:
        m = module(src)
        before = output(module(src)) if name != "Job" else None
        for f in m.funcs:
            idom, _ = S.dominators(f)
            labels = [b.label for b in f.blocks]
            mine = {(d, n) for d in labels for n in labels if S.dominates(idom, d, n)}
            assert mine == dominators_by_deletion(f), f"dominators of {f.name} disagree with the definition"
            dom_pairs += len(labels) ** 2
            S.to_ssa(f)
            O.optimize(f)
            g = AN.interference_ssa(f)
            chordal, order, _ = AN.is_chordal(g)
            colours = max(AN.color_peo(g, order).values(), default=-1) + 1
            clique = AN.max_clique_chordal(g)
            assert chordal, f"{name}.{f.name}: an SSA interference graph with a hole"
            assert colours == clique, f"{name}.{f.name}: {colours} colours for a largest clique of {clique}"
            S.from_ssa(f)
            after = AN.interference_ssa(f)
            rows.append(dict(prog=name, fn=f.name, values=len(g), colours=colours, after=AN.is_chordal(after)[0]))
        if before is not None:
            compared += 1
            same += output(m) == before
    jobrows = [r for r in rows if r["prog"] == "Job"]
    holes = sum(not r["after"] for r in rows)
    f = module(job).func("same")
    S.to_ssa(f)
    O.optimize(f)
    S.from_ssa(f)
    hole = AN.find_hole(AN.interference_ssa(f))

    lab.row("functions checked", f"{len(rows)}   ({dom_pairs:,} dominance pairs agree with 'delete d')")
    lab.row("SSA graphs that are chordal", f"{len(rows)} of {len(rows)}   (theory: all)")
    lab.row("colours used = largest clique", f"{len(rows)} of {len(rows)}   (theory: all)")
    for r in jobrows:
        lab.row(f"Job, {r['fn']}", f"{r['values']} values, {r['colours']} registers")
    lab.row("still chordal after leaving SSA", f"{len(rows) - holes} of {len(rows)}")
    lab.row("a hole in 'same' after leaving SSA", f"a cycle of {len(hole)} values with no chord" if hole else "none")
    lab.row("optimized output = unoptimized output", f"{same} of {compared} programs that halt within the limit")
    assert holes >= 1 and not next(r for r in jobrows if r["fn"] == "same")["after"], "leaving SSA should create holes"
    assert hole is not None and len(hole) == 4, "the film's four-cycle without a chord"
    assert compared >= 3 and same == compared, "an optimization changed what a program prints"
    lab.note = ("In SSA every interference graph here is chordal, so greedy colouring along a perfect elimination "
                "order is optimal; the copies that replace phi-functions break that in "
                f"{holes} of {len(rows)} functions.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    for is_job, color, label in ((False, labs.BLUE, "fuzzed functions"), (True, labs.GOLD, "the Job's functions")):
        sel = [r for r in rows if (r["prog"] == "Job") == is_job]
        ax[0].scatter([r["values"] for r in sel], [r["colours"] for r in sel], s=26 if is_job else 14, color=color,
                      alpha=0.9, label=label, zorder=3 if is_job else 2)
    ax[0].axhline(REGISTERS, color=labs.RED, ls="--", lw=1, label=f"Pebble's {REGISTERS} allocatable registers")
    ax[0].set(title="Registers an SSA function needs = its largest clique", xscale="log",
              xlabel="values (vertices of the interference graph)", ylabel="registers (colours)")
    ax[0].set_ylim(0, REGISTERS + 3.5)
    ax[0].legend(loc="upper left", ncols=2)
    counts = [len(rows), len(rows) - holes]
    ax[1].set_axisbelow(True)
    ax[1].grid(axis="x", visible=False)
    ax[1].bar([0, 1], counts, color=[labs.GREEN, labs.ORANGE], width=0.55)
    ax[1].bar([1], [holes], bottom=[len(rows) - holes], color=labs.RED, width=0.55)
    for x, y, s in ((0, counts[0], f"{counts[0]} chordal"), (1, counts[1], f"{counts[1]} chordal"),
                    (1, len(rows), f"{holes} with a hole")):
        ax[1].text(x, y - 0.03 * len(rows), s, ha="center", va="top", color=labs.BG, fontweight="bold")
    ax[1].set(title="Chordal interference graphs, before and after the copies", ylabel="functions",
              xticks=[0, 1], xticklabels=["in SSA", "after leaving SSA"], xlim=(-0.6, 1.6))
    lab.fig = fig
    return lab
