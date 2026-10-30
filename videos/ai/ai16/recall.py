"""A recall task for sparse attention (multi-query associative recall, as in Zoology, Arora et al. 2023).

Each sequence: a start token, 16 key-value pairs, 64 filler tokens, then the 16 keys again in a new order, each
followed by its value.  The model is scored on the values it must recall: the nearest copy of the answer is at least
64 tokens back, so a window of 16 keys cannot see it; full attention can, and a sparse pattern can only if it chooses
the right keys.
"""

from __future__ import annotations

import numpy as np

NK, NV, NF = 64, 64, 32  # key symbols, value symbols, filler symbols
BOS = NK + NV + NF
VOCAB = BOS + 1
PAIRS, FILL = 16, 64
T = 1 + 2 * PAIRS + FILL + 2 * PAIRS - 1  # 128 positions read, 129 tokens


def sequences(g: np.random.Generator, B: int):
    seq = np.empty((B, T + 1), np.int64)
    w = np.zeros((B, T), np.float32)
    for b in range(B):
        keys = g.choice(NK, PAIRS, replace=False)
        vals = g.integers(NK, NK + NV, PAIRS)
        pairs = np.stack([keys, vals], 1).reshape(-1)
        fill = g.integers(NK + NV, NK + NV + NF, FILL)
        order = g.permutation(PAIRS)
        qs = np.stack([keys[order], vals[order]], 1).reshape(-1)
        seq[b] = np.concatenate([[BOS], pairs, fill, qs])
        w[b, 1 + 2 * PAIRS + FILL::2] = 1.0  # the model reads a query key here and must say its value next
    return seq, w


def batch(g: np.random.Generator, B: int):
    import torch

    seq, w = sequences(g, B)
    s = torch.from_numpy(seq)
    return s[:, :-1], s[:, 1:], torch.from_numpy(w)


def accuracy(model, seed=99, n=256, **kw) -> float:
    """The share of recalled values that are right (the model's most likely next token), on ``n`` fresh sequences."""
    import torch

    g = np.random.default_rng(seed)
    x, y, w = batch(g, n)
    model.eval()
    with torch.no_grad():
        z = model(x, **kw)
    model.train()
    ok = (z.argmax(-1) == y).float()
    return float((ok * w).sum() / w.sum())
