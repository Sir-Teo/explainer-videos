"""Quantum error correction (Part 53): the three-qubit bit-flip code and its syndromes; the repetition code of
distance d under independent bit flips, logical against physical error rate (with a threshold at p = 1/2 for this
noise, and the d-dependence of the logical rate below it); and the scaling factor Lambda by which each step in
distance divides the logical error rate."""

from __future__ import annotations

import math

import numpy as np

from .sim import X, State


def three_qubit(alpha: float = 0.6, flip: int | None = 1) -> dict:
    """Encode a|0> + b|1> as a|000> + b|111>, flip one qubit, measure the syndromes Z0Z1 and Z1Z2 (on ancillas),
    correct, and check the state is restored."""
    beta = math.sqrt(1 - alpha ** 2)
    s = State(3)
    s.v[:] = 0
    s.v[0b000], s.v[0b111] = alpha, beta
    if flip is not None:
        s.apply(X, flip)
    # syndromes: parity of qubits (0,1) and (1,2), read from any basis state with nonzero amplitude
    idx = int(np.flatnonzero(np.abs(s.v) > 1e-12)[0])
    bits = [(idx >> (2 - q)) & 1 for q in range(3)]
    syn = (bits[0] ^ bits[1], bits[1] ^ bits[2])
    which = {(0, 0): None, (1, 0): 0, (1, 1): 1, (0, 1): 2}[syn]
    if which is not None:
        s.apply(X, which)
    ok = abs(s.v[0b000] - alpha) < 1e-12 and abs(s.v[0b111] - beta) < 1e-12
    return {"alpha": alpha, "beta": beta, "flip": flip, "syndrome": list(syn), "corrected": which, "restored": ok}


def repetition(ds=(1, 3, 5, 7, 9, 11), ps=None, trials: int = 200_000, seed: int = 0) -> dict:
    """Distance-d repetition code with majority decoding: logical error rate against physical p, simulated and
    exact (the probability that more than d/2 of d bits flip)."""
    rng = np.random.default_rng(seed)
    ps = ps if ps is not None else [0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
    rows = []
    for d in ds:
        for p in ps:
            flips = (rng.random((trials, d)) < p).sum(axis=1)
            sim = float((flips > d // 2).mean())
            exact = sum(math.comb(d, k) * p ** k * (1 - p) ** (d - k) for k in range(d // 2 + 1, d + 1))
            rows.append({"d": d, "p": p, "simulated": sim, "exact": exact})
    lam = {}
    for p in (0.01, 0.05, 0.1):
        e = {d: sum(math.comb(d, k) * p ** k * (1 - p) ** (d - k) for k in range(d // 2 + 1, d + 1)) for d in ds}
        lam[str(p)] = [e[ds[i]] / e[ds[i + 1]] for i in range(1, len(ds) - 1)]
    return {"rows": rows, "lambda": lam}
