"""Lab 14: count beta-steps in Church arithmetic, check confluence on whole reduction graphs, and run the safety theorems."""

from videos.coursekit import labs
import random

import numpy as np

from explainer.cs.lam import App, Lam, Var, church, parse, unchurch
from explainer.cs.lang.lam import reduce as R
from explainer.cs.lang.lam import stlc

TITLE = "Church arithmetic, confluence and type safety, by machine"
GOAL = ("With the series' reducer, compute on Church numerals and count the beta-steps (the predecessor costs "
        "10n + 6); build the whole reduction graph of small terms and check that every pair of reducts meets "
        "again; then compare random untyped terms, some of which never stop, with random well-typed terms, on "
        "which progress and preservation are checked at every step.")
TASKS = [
    "Reduce R.apply(R.lib('pow'), church(2), church(n)) for n = 1..6 and plot the steps. Is the growth linear in n or in 2^n?",
    "Run r'(\\x y. y) ((\\x. x x) (\\x. x x)) z' under each of 'normal', 'applicative', 'name' and 'value'. Which strategies find the normal form?",
    "In typed_terms, raise depth from 5 to 7. How does the longest run change, and why can no depth make a typed term loop?",
]
BUDGET = 400  # beta-steps allowed to an untyped term, as in the film
FILM = ((r"(\x. x x) ((\y. y) z)", 6, 7), (r"(\x. x x) ((\y. (\z. z) y) ((\w. w) v))", 30, 93))  # terms, steps


def untyped(rng, depth, env=()):
    """A random closed lambda term (the film's generator: variables 30%, abstractions 30%, applications 40%)."""
    r = rng.random()
    if depth <= 0:
        return Var(rng.choice(env)) if env else Lam("v0", Var("v0"))
    if env and r < 0.3:
        return Var(rng.choice(env))
    if r < 0.6:
        x = f"v{len(env)}"
        return Lam(x, untyped(rng, depth - 1, env + (x,)))
    return App(untyped(rng, depth - 1, env), untyped(rng, depth - 1, env))


def typed_terms(n, seed, depth=5):
    """Steps to a value for n random closed well-typed terms; progress and preservation asserted at every step."""
    rng = random.Random(seed)
    types = [stlc.BOOL, stlc.NAT, stlc.arrow(stlc.NAT, stlc.NAT), stlc.arrow(stlc.BOOL, stlc.NAT)]
    steps = []
    for i in range(n):
        T = types[i % len(types)]
        t = stlc.gen(T, depth, rng)
        k = 0
        while not stlc.is_value(t):
            r = stlc.step(t)
            assert r is not None, f"progress fails: {stlc.show(t)} is stuck"
            t = r[0]
            assert stlc.typecheck(t)[0] == T, f"preservation fails at {stlc.show(t)}"
            k += 1
            assert k < 10_000, "a well-typed term that does not stop"
        steps.append(k)
    return np.array(steps)


def run(seed=0):
    rng = np.random.default_rng(seed)
    pyrng = random.Random(seed)
    lab = labs.Lab()

    # 1. arithmetic with functions alone, counted in beta-steps (normal order)
    for name, op in (("plus", lambda a, b: a + b), ("times", lambda a, b: a * b)):
        for _ in range(4):
            a, b = (int(v) for v in rng.integers(1, 6, 2))
            k, t = R.run(R.apply(R.lib(name), church(a), church(b)))
            assert unchurch(t) == op(a, b), f"{name} {a} {b} gave {unchurch(t)}"
        lab.row(f"{name} {a} {b}", f"{unchurch(t)} in {k} beta-steps")
    ns = np.arange(0, 11)
    pred = []
    for n in ns:
        k, t = R.run(R.apply(R.lib("pred"), church(int(n))), max_steps=5000)
        assert unchurch(t) == max(int(n) - 1, 0)
        pred.append(k)
    pred = np.array(pred)
    lab.row("predecessor of 0..10, beta-steps", " ".join(str(k) for k in pred))
    lab.row("the film's count", "9 at zero, then 10n + 6")
    assert pred[0] == 9 and np.array_equal(pred[1:], 10 * ns[1:] + 6), "Kleene's predecessor costs 10n + 6 steps"

    # 2. Church-Rosser on whole reduction graphs
    for src, terms, steps in FILM:
        nodes, edges, normal = R.graph(parse(src), limit=500)
        assert (len(nodes), len(edges), len(normal)) == (terms, steps, 1) and R.confluent(parse(src), 500)
        lab.row("reduction graph", f"{len(nodes)} terms, {len(edges)} steps, {len(normal)} normal form, confluent")
    graphs = most = 0
    while graphs < 30:
        t = untyped(pyrng, 5)
        nodes, _, normal = R.graph(t, limit=60)
        if 3 <= len(nodes) < 60:  # the whole graph was explored
            graphs += 1
            most = max(most, len(nodes))
            assert len(normal) <= 1 and R.confluent(t, 60), "two reducts that never meet"
    lab.row("random reduction graphs", f"{graphs} of {graphs} confluent, at most one normal form (largest: {most} terms)")

    # 3. untyped terms can run forever; well-typed terms cannot, and cannot get stuck
    n_untyped = 300
    stopped = np.array([k for k in (R.run(untyped(pyrng, 7), "normal", max_steps=BUDGET, max_size=3000)[0]
                                    for _ in range(n_untyped)) if k is not None])
    running = n_untyped - len(stopped)
    typed = typed_terms(400, seed + 1)
    lab.row(f"untyped terms still running after {BUDGET} steps", f"{running} of {n_untyped}   (the film: 136 of 2,000)")
    lab.row("well-typed terms that stop", f"{len(typed)} of {len(typed)}, the longest after {typed.max()} steps")
    lab.row("typed steps checked for progress and preservation", f"{typed.sum():,}, none stuck, none changing type")
    assert running >= 3, "some random untyped terms should exhaust the budget"
    assert typed.max() < BUDGET
    lab.note = ("One rule computes arithmetic, any two reduction paths can be rejoined, and a type derivation buys two "
                "guarantees an untyped term does not have: it never gets stuck and, without fix, it always stops.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].plot(ns[1:], 10 * ns[1:] + 6, color=labs.GOLD, label="10n + 6")
    ax[0].plot(ns, pred, "o", color=labs.BLUE, label="Kleene's predecessor, measured")
    ax[0].set(title="Beta-steps to compute n - 1 on Church numerals", xlabel="n", ylabel="beta-steps (normal order)")
    ax[0].legend()
    edges = np.array([0, 1, 2, 4, 8, 16, 32, 64, 128, 256, BUDGET])
    x = np.arange(len(edges))
    hu = np.append(np.histogram(stopped, edges)[0], running) / n_untyped
    ht = np.append(np.histogram(typed, edges)[0], 0) / len(typed)
    ax[1].bar(x - 0.2, ht, 0.4, color=labs.GREEN, label="well-typed (simply typed calculus)")
    ax[1].bar(x[:-1] + 0.2, hu[:-1], 0.4, color=labs.BLUE, label="untyped")
    ax[1].bar(x[-1:] + 0.2, hu[-1:], 0.4, color=labs.RED, label=f"untyped, still running at {BUDGET}")
    ax[1].set_axisbelow(True)
    ax[1].set(title="How long random terms run", xlabel="steps to a normal form or a value", ylabel="share of terms",
              xticks=x, xticklabels=["0", "1", "2-3", "4-7", "8-15", "16-31", "32-63", "64-127", "128-255", "256-399",
                                     "never?"])
    ax[1].tick_params(axis="x", labelrotation=35)
    ax[1].legend()
    lab.fig = fig
    return lab
