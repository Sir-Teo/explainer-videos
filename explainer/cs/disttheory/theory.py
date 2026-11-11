"""Distributed computing theory (Part 59), computed.  Cole and Vishkin's 3-colouring of an oriented ring in
O(log* n) rounds, run on a million nodes; log* n against Linial's lower bound; the hexagon argument that three
processes cannot tolerate one Byzantine liar, run against a concrete protocol; FloodSet's f + 1 rounds (Part 38);
Ben-Or's randomized consensus rounds; Sperner's lemma on subdivided triangles; and a population protocol for
exact majority.  After Lynch, *Distributed Algorithms*, and Attiya and Welch, *Distributed Computing*."""

from __future__ import annotations

import math
import random

import numpy as np


def log_star(n: float) -> int:
    if not n > 0 or n == math.inf:
        raise ValueError("log-star needs a positive finite input")
    k = 0
    while n > 1:
        n = math.log2(n)
        k += 1
    return k


# ---------------------------------------------------------------- Cole-Vishkin

def cole_vishkin(n: int = 1_000_000, seed: int = 0, keep: int = 24) -> dict:
    """Each node of an oriented ring starts with a unique id (its colour).  In a round, a node compares its colour
    with its successor's, finds the lowest bit index i where they differ, and takes 2 i + (its own bit i): adjacent
    colours stay different, and b-bit colours shrink to about log2 b + 1 bits.  When colours are below 6, three more
    rounds remove colours 5, 4 and 3 (each node with that colour picks the smallest of {0, 1, 2} its neighbours do
    not use).  Returns the rounds, the number of colours after each, and the first ``keep`` nodes' colours per
    round (for drawing)."""
    if n < 2 or keep < 0:
        raise ValueError("a properly coloured ring needs at least two nodes and a nonnegative trace length")
    rng = np.random.default_rng(seed)
    c = rng.permutation(n).astype(np.int64) + rng.integers(0, 2 ** 20)    # distinct ids
    trace = [c[:keep].tolist()]
    counts = [int(len(np.unique(c)))]
    rounds = 0
    while c.max() >= 6:
        succ = np.roll(c, -1)
        diff = c ^ succ
        i = np.zeros(n, dtype=np.int64)
        low = diff & (-diff)                                   # lowest set bit
        i = np.log2(low).astype(np.int64)
        bit = (c >> i) & 1
        c = 2 * i + bit
        rounds += 1
        trace.append(c[:keep].tolist())
        counts.append(int(len(np.unique(c))))
        assert np.all(c != np.roll(c, -1))
    for col in (5, 4, 3):
        pred, succ = np.roll(c, 1), np.roll(c, -1)
        mask = c == col
        new = c.copy()
        for k in (0, 1, 2):
            pick = mask & (pred != k) & (succ != k) & (new == col)
            new[pick] = k
        c = new
        rounds += 1
        trace.append(c[:keep].tolist())
        counts.append(int(len(np.unique(c))))
    ok = bool(np.all(c != np.roll(c, -1)) and c.max() <= 2)
    return {"n": n, "rounds": rounds, "log_star": log_star(n), "colours": counts, "trace": trace, "proper": ok}


def cv_scaling(ns=(10, 100, 10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6)) -> list[dict]:
    return [{"n": n, "rounds": cole_vishkin(n)["rounds"], "log_star": log_star(n)} for n in ns]


def log_star_table() -> list[dict]:
    rows = []
    for e, name in ((1, "2"), (2, "4"), (4, "16"), (16, "65,536"), (65536, r"2^65536")):
        rows.append({"n": name, "log_star": log_star(2.0 ** e) if e < 1024 else 5})
    return rows


# ---------------------------------------------------------------- the hexagon

def _protocol(my_value, heard):
    """A natural deterministic 3-process protocol: decide the majority of my value and what my two neighbours told
    me in two rounds (round 1 their values, round 2 what each says the third said)."""
    vals = [my_value] + heard
    return int(sum(vals) * 2 > len(vals))


def hexagon() -> dict:
    """Fischer, Lynch and Merritt (1986): wire six copies A0 B0 C0 A1 B1 C1 in a ring, inputs 0 0 0 1 1 1, each
    running the 3-process protocol as if its two ring neighbours were the other two processes.  Every adjacent pair
    sees exactly what it would see in some 3-process run where the third process is Byzantine.  Validity forces
    (A0, B0) to decide 0 and (A1, B1) to decide 1 (both their inputs agree), and agreement forces every adjacent
    pair to agree: impossible around a ring.  Here the protocol's actual decisions show where it fails."""
    names = ["A0", "B0", "C0", "A1", "B1", "C1"]
    inputs = [0, 0, 0, 1, 1, 1]
    n = 6
    # round 1: each hears its two ring neighbours' inputs; round 2: each hears what each neighbour heard from its
    # other neighbour
    r1 = {i: (inputs[(i - 1) % n], inputs[(i + 1) % n]) for i in range(n)}
    r2 = {i: (r1[(i - 1) % n][0], r1[(i + 1) % n][1]) for i in range(n)}
    decide = {names[i]: _protocol(inputs[i], list(r1[i]) + list(r2[i])) for i in range(n)}
    pairs = []
    for i in range(n):
        a, b = names[i], names[(i + 1) % n]
        third = names[(i + 2) % n][0]
        same_input = inputs[i] == inputs[(i + 1) % n]
        ok_validity = (not same_input) or (decide[a] == inputs[i] and decide[b] == inputs[i])
        ok_agree = decide[a] == decide[b]
        pairs.append({"pair": [a, b], "byzantine": third, "inputs": [inputs[i], inputs[(i + 1) % n]],
                      "decisions": [decide[a], decide[b]], "agreement": ok_agree, "validity": ok_validity})
    bad = [p for p in pairs if not (p["agreement"] and p["validity"])]
    return {"names": names, "inputs": inputs, "decisions": decide, "pairs": pairs, "violations": bad}


# ---------------------------------------------------------------- synchronous and randomized consensus

def floodset_table() -> list[dict]:
    from explainer.cs.dist.consensus import floodset
    rows = []
    for n, f in ((3, 1), (4, 1), (4, 2)):
        for r in range(1, f + 2):
            res = floodset(n=n, f=f, rounds=r)
            rows.append({"n": n, "f": f, "rounds": r, "agreement": res.get("ok", res.get("agreement")),
                         "summary": {k: v for k, v in res.items() if k in ("ok", "agreement", "checked")}})
    return rows


def ben_or_rounds(cases=((4, 1), (6, 2), (8, 3), (10, 4)), trials: int = 200, seed: int = 0) -> list[dict]:
    from explainer.cs.dist.consensus import ben_or
    rows = []
    for n, f in cases:
        rs, agree = [], 0
        for t in range(trials):
            inputs = [i % 2 for i in range(n)]          # split inputs: the hard case
            r = ben_or(n=n, f=f, inputs=inputs, seed=seed + t)
            if r["rounds"] is not None:
                rs.append(r["rounds"])
                agree += r["agreement"]
        rows.append({"n": n, "f": f, "mean_rounds": float(np.mean(rs)), "max_rounds": int(max(rs)),
                     "agreement": agree / len(rs), "terminated": len(rs) / trials})
    return rows


# ---------------------------------------------------------------- Sperner

def sperner(k: int = 8, seed: int = 0) -> dict:
    """Subdivide a triangle into k^2 small triangles; colour corner i with i, each boundary vertex with one of the
    colours of its edge's ends, interior vertices at random.  Sperner's lemma: the number of small triangles with
    all three colours is odd, so at least one exists; a walk through doors (edges coloured 0-1) finds one."""
    rng = random.Random(seed)
    col = {}
    for i in range(k + 1):
        for j in range(k + 1 - i):
            l = k - i - j
            if (i, j) == (k, 0):
                col[(i, j)] = 0
            elif (i, j) == (0, k):
                col[(i, j)] = 1
            elif (i, j) == (0, 0):
                col[(i, j)] = 2
            elif l == 0:                         # edge between corners 0 and 1
                col[(i, j)] = rng.choice((0, 1))
            elif j == 0:                         # edge between 0 and 2
                col[(i, j)] = rng.choice((0, 2))
            elif i == 0:                         # edge between 1 and 2
                col[(i, j)] = rng.choice((1, 2))
            else:
                col[(i, j)] = rng.randrange(3)
    tris = []
    for i in range(k):
        for j in range(k - i):
            tris.append(((i, j), (i + 1, j), (i, j + 1)))
            if i + j + 1 < k:
                tris.append(((i + 1, j), (i + 1, j + 1), (i, j + 1)))
    full = [t for t in tris if {col[v] for v in t} == {0, 1, 2}]
    return {"k": k, "colours": [[i, j, c] for (i, j), c in col.items()], "triangles": len(tris),
            "rainbow": [list(map(list, t)) for t in full], "count": len(full), "odd": len(full) % 2 == 1}


def sperner_check(trials: int = 200) -> dict:
    counts = [sperner(k=10, seed=s)["count"] for s in range(trials)]
    return {"trials": trials, "all_odd": all(c % 2 for c in counts), "min": min(counts), "max": max(counts)}


# ---------------------------------------------------------------- population protocols

def majority(n: int = 200, margin: int = 2, trials: int = 50, seed: int = 0) -> dict:
    """The four-state exact-majority protocol (Draief and Vojnovic 2012; Mertzios et al. 2014): strong opinions A, B
    and weak a, b.  A + B -> a + b (they cancel); A + b -> A + a; B + a -> B + b (the strong convert the weak).  With
    any positive margin, all agents end up holding the majority's opinion; interactions are random pairs."""
    if n < 1 or not 0 < margin <= n or (n + margin) % 2 or trials <= 0:
        raise ValueError("need a realizable positive A-majority margin and positive trials")
    rng = random.Random(seed)
    rows = []
    out_steps, correct = [], 0
    trace = None
    for t in range(trials):
        nA = (n + margin) // 2
        state = ["A"] * nA + ["B"] * (n - nA)
        steps = 0
        hist = []
        while not all(s in "Aa" for s in state):
            i, j = rng.sample(range(n), 2)
            x, y = state[i], state[j]
            if {x, y} == {"A", "B"}:
                state[i], state[j] = "a", "b"
            elif x == "A" and y == "b":
                state[j] = "a"
            elif y == "A" and x == "b":
                state[i] = "a"
            elif x == "B" and y == "a":
                state[j] = "b"
            elif y == "B" and x == "a":
                state[i] = "b"
            steps += 1
            if steps % n == 0:
                c = {s: state.count(s) for s in "ABab"}
                hist.append(c)
                if c["B"] == 0 and c["b"] == 0 and c["A"] > 0:
                    break
                if steps > 2000 * n:
                    break
        final_counts = {s: state.count(s) for s in "ABab"}
        if not hist or hist[-1] != final_counts:
            hist.append(final_counts)
        out_steps.append(steps / n)
        correct += all(s in "Aa" for s in state)
        if trace is None:
            trace = hist
    rows = {"n": n, "margin": margin, "parallel_time_mean": float(np.mean(out_steps)), "correct": correct / trials,
            "trace": trace}
    return rows


def majority_scaling(ns=(50, 100, 200, 400), margin: int = 2) -> list[dict]:
    return [{k: v for k, v in majority(n=n, margin=margin, trials=20).items() if k != "trace"} for n in ns]
