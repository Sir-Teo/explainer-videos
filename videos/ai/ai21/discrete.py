"""Masked diffusion's bound, checked exactly on a language small enough to enumerate (the ``discrete`` item).

Strings of L = 4 letters from {a, b, c}, drawn from a Markov chain that likes a -> b -> c -> a: 81 strings, every
probability known.  Noise blanks each letter with probability t (absorbing, "masked" diffusion, linear schedule).  A
model predicts each blank from the letters still showing.  Three models: the exact conditionals, the exact ones
blurred towards uniform, and one that ignores the context (each position's letter frequencies).  For each, three
numbers that the derivation says agree, computed by enumeration over every string and every blank pattern:

    discrete-time bound  the variational bound of a T-step chain (D3PM), for T = 1 ... 1024
    weighted cross-entropy  int_0^1 (1/t) E[sum over blanks of -log q(x_i | the rest)] dt, in closed form
                         (the integral of t^k (1 - t)^(L - k) / t is a Beta function)
    any-order AR         the average, over all 24 orders, of the autoregressive loss in that order

and the true entropy.  The bound of the exact model equals the entropy: the bound is tight.
"""

from __future__ import annotations

import itertools
import math

import numpy as np

V, L = 3, 4
PI = np.array([0.5, 0.3, 0.2])
P = np.array([[0.1, 0.8, 0.1], [0.1, 0.1, 0.8], [0.7, 0.2, 0.1]])
TS = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]


def joint():
    xs = list(itertools.product(range(V), repeat=L))
    p = np.array([PI[x[0]] * np.prod([P[x[i], x[i + 1]] for i in range(L - 1)]) for x in xs])
    return xs, p / p.sum()


def model(kind):
    """q(x_i = v | the letters at positions outside M): a function (x, M, i) -> probabilities over V."""
    xs, p = joint()
    idx = {x: k for k, x in enumerate(xs)}

    def exact(x, M, i):
        keep = [j for j in range(L) if j not in M]
        w = np.zeros(V)
        for y, py in zip(xs, p):
            if all(y[j] == x[j] for j in keep):
                w[y[i]] += py
        return w / w.sum()

    marg = np.array([[sum(py for y, py in zip(xs, p) if y[i] == v) for v in range(V)] for i in range(L)])
    if kind == "exact":
        return exact
    if kind == "blurred":
        return lambda x, M, i: 0.7 * exact(x, M, i) + 0.3 / V
    if kind == "nocontext":
        return lambda x, M, i: marg[i]
    raise ValueError(kind)


def compute_discrete():
    xs, p = joint()
    H = float(-(p * np.log(p)).sum())
    masks = [M for k in range(1, L + 1) for M in itertools.combinations(range(L), k)]
    out = dict(V=V, L=L, H_bits=H / L / math.log(2), Ts=TS, kinds=["exact", "blurred", "nocontext"], n_strings=len(xs),
               probs=p, strings=["".join("abc"[c] for c in x) for x in xs], pi=PI, P=P)
    for kind in out["kinds"]:
        q = model(kind)
        # the cross-entropy of every blank, for every string and every blank pattern
        ce = {(k, M): {i: -math.log(q(x, M, i)[x[i]]) for i in M} for k, x in enumerate(xs) for M in masks}

        def term(k, M):
            return sum(ce[(k, M)].values())

        # the continuous-time bound: weight of pattern M is int_0^1 t^(|M|-1) (1-t)^(L-|M|) dt = B(|M|, L-|M|+1)
        cont = sum(p[k] * sum(math.gamma(len(M)) * math.gamma(L - len(M) + 1) / math.gamma(L + 1) * term(k, M)
                              for M in masks) for k in range(len(xs)))
        # the same, any order: reveal the letters one at a time in order sigma; each step predicts one blank
        orders = list(itertools.permutations(range(L)))
        anyorder = sum(p[k] * np.mean([sum(ce[(k, tuple(sorted(o[j:])))][o[j]] for j in range(L)) for o in orders])
                       for k in range(len(xs)))
        # left to right only
        l2r = sum(p[k] * sum(ce[(k, tuple(range(j, L)))][j] for j in range(L)) for k in range(len(xs)))
        # the T-step chain's bound: sum over steps of (1/T)/t_j times the expected blanks' cross-entropy at t_j
        A = p @ np.array([[term(k, M) for M in masks] for k in range(len(xs))])  # expected over strings, per pattern
        sz = np.array([len(M) for M in masks])
        disc = []
        for T in TS:
            t = np.arange(1, T + 1)[:, None] / T
            disc.append(float(((1 / T) / t[:, 0] * (t ** sz * (1 - t) ** (L - sz) @ A)).sum()))
        bits = lambda v: v / L / math.log(2)
        out[f"{kind}_cont"], out[f"{kind}_anyorder"], out[f"{kind}_l2r"] = bits(cont), bits(anyorder), bits(l2r)
        out[f"{kind}_disc"] = [bits(v) for v in disc]
        print(f"    {kind:9s}: weighted CE {bits(cont):.6f}, any-order {bits(anyorder):.6f}, left-to-right "
              f"{bits(l2r):.6f}; T-step " + " ".join(f"{bits(v):.4f}" for v in disc) + f"; entropy {out['H_bits']:.6f}",
              flush=True)
        assert abs(cont - anyorder) < 1e-9  # the identity derived on screen
    assert abs(out["exact_cont"] - out["H_bits"]) < 1e-9  # with the exact conditionals the bound is tight
    # the weight 1/t, and how the blanks' expected count k = tL turns it into 1/k
    out["beta_check"] = [float(math.comb(L, k) * math.gamma(k) * math.gamma(L - k + 1) / math.gamma(L + 1) * k)
                         for k in range(1, L + 1)]
    return out
