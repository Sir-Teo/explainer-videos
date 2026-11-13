"""Lab 58: run one language three ways, climb Kleene's chain to factorial, and break a free theorem."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import math
import random

import numpy as np

from explainer.cs.semantics import meaning

TITLE = "Three interpreters, one meaning"
GOAL = ("Generate 300 random terminating programs and run each by small steps, by the big-step evaluator and on the "
        "CEK machine; then compute the Kleene chain of the factorial functional, and test two free theorems, one of "
        "which must fail for a map that does not preserve order.")
TASKS = [
    "Change big() so that it evaluates the right operand of an operation first. Does agreement() notice, and why not "
    "until the language has an effect such as an exception?",
    "Write the functional whose least fixed point is Fibonacci and iterate it from the empty function. On which "
    "inputs is the k-th iterate defined?",
    "In free_theorems(), replace g(x) = x * x by g(x) = -x. Sorting no longer commutes with map g: which property of "
    "g does Wadler's theorem need?",
]


def run(seed=0):
    lab = labs.Lab()

    # 1. three operational semantics on the same random programs
    rng = random.Random(seed)
    n, small_steps, cek_steps, agree = 300, [], [], 0
    for _ in range(n):
        p = meaning.random_program(rng)
        v1, ns, _ = meaning.small(p)
        v2 = meaning.big(p)
        v3, nc = meaning.cek(p)
        agree += meaning._val(v1) == meaning._val(v2) == meaning._val(v3)
        small_steps.append(ns)
        cek_steps.append(nc)
    small_steps, cek_steps = np.array(small_steps), np.array(cek_steps)
    lab.row("programs on which the three semantics agree", f"{agree} of {n}   (the theory says all)")
    lab.row("mean steps per program", f"small-step {small_steps.mean():.1f}   CEK transitions {cek_steps.mean():.1f}")
    assert agree == n, "small-step, big-step and the CEK machine must give the same value"
    assert cek_steps.mean() > 2 * small_steps.mean(), "the machine takes more, but cheaper, transitions"

    # 2. fact n by small steps: deterministic, so the run is one line; its length is 5 n + 3
    runs = [meaning.fact_trace(k) for k in range(7)]
    lab.row("small steps of fact 0 ... fact 6", "  ".join(str(r["steps"]) for r in runs) + "   (5n + 3)")
    assert all(r["value"] == math.factorial(r["n"]) and r["steps"] == 5 * r["n"] + 3 for r in runs)

    # 3. the Kleene chain: F^k(bottom) is factorial on 0 .. k-1 and undefined elsewhere
    chain = meaning.kleene(k_max=7, domain=8)
    for row in chain:
        expect = [math.factorial(m) if m < row["k"] else None for m in range(8)]
        assert row["table"] == expect, f"F^{row['k']}(bottom) is factorial exactly on 0 .. k - 1"
    lab.row("F^7(bottom) on 0 ... 7", "  ".join("⊥" if v is None else str(v) for v in chain[7]["table"]))

    # 4. free theorems, and the one that needs a hypothesis
    ft = meaning.free_theorems(trials=2000, seed=seed)
    worst = min(ft["rearrangements"].values())
    c = ft["sort_counterexample"]
    lab.row("map f . r = r . map f, four rearrangements", f"{worst:.0%} of 2,000 random lists each   (theory 100%)")
    lab.row("sort commutes with f(x) = 2x + 1", f"{ft['sort_monotone']:.0%}   (f preserves order)")
    lab.row("sort against g(x) = x * x", f"fails on {c['xs']}" if c else "no counterexample found")
    assert worst == 1.0 and ft["sort_monotone"] == 1.0, "a free theorem holds on every input"
    assert c is not None and c["sort_then_map"] != c["map_then_sort"], "squaring does not preserve order"
    assert sorted(c["sort_then_map"]) == c["map_then_sort"], "the two sides hold the same numbers, in different order"

    # 5. the same traces, not bisimilar
    b = meaning.bisim_examples()
    ch, ve = b["choice"], b["vending"]
    lab.row("a.(b + c) against a.b + a.c", f"same traces: {ch['same_traces']}   bisimilar: {ch['bisimilar']}   "
                                           f"({ch['blocks']} blocks after {ch['rounds']} rounds)")
    assert ch["same_traces"] and not ch["bisimilar"] and ve["bisimilar"]
    lab.note = ("Three definitions of running a program give one answer on every program tried, the Kleene iterates "
                "climb to factorial one input at a time, and a free theorem holds on every list until its hypothesis "
                "(an order-preserving map) is dropped.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].scatter(small_steps, cek_steps, s=12, color=labs.BLUE, alpha=0.7, label="one random program")
    hi = max(small_steps.max(), 2)
    grid = np.array([1, hi])
    ax[0].plot(grid, grid, color=labs.MUTED, ls="--", label="one transition per small step")
    ax[0].plot(grid, cek_steps.mean() / small_steps.mean() * grid, color=labs.GOLD,
               label=f"ratio of the means: {cek_steps.mean() / small_steps.mean():.1f}")
    ax[0].set(xscale="log", yscale="log", xlabel="small steps to a value", ylabel="CEK transitions",
              title=f"The same {n} programs on two machines")
    ax[0].legend(loc="upper left")
    table = np.array([[np.nan if v is None else np.log10(v) for v in row["table"]] for row in chain])
    ax[1].set_facecolor(labs.PANEL)
    ax[1].imshow(np.ma.masked_invalid(table), cmap="cividis", aspect="auto", vmin=-3.0, vmax=4.5)
    for k, row in enumerate(chain):
        for m, v in enumerate(row["table"]):
            ax[1].text(m, k, "⊥" if v is None else str(v), ha="center", va="center", fontsize=9,
                       color=labs.MUTED if v is None else labs.INK)
    ax[1].set(xlabel="input n", ylabel="iterate k", title="Kleene's chain: F^k(⊥) is factorial on 0 … k − 1",
              xticks=range(8), yticks=range(8))
    ax[1].grid(False)
    lab.fig = fig
    return lab
