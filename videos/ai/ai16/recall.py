"""A recall task for sparse attention (associative recall, after Zoology's MQAR, Arora et al. 2023).

Each sequence: a start token; 8 facts, each one token that binds a key to a value (key 3 is value 11, say); 40
filler tokens; then the 8 keys asked in a new order, each followed by its answer.  The model is scored on the answers:
the fact it needs is at least 40 tokens back, so a sliding window of 8 keys cannot see it; full attention can, and a
sparse pattern can only if it chooses the right keys.
"""

from __future__ import annotations

import numpy as np

NK, NV, NF = 16, 16, 16  # keys, values, filler symbols
FACT0 = 0  # facts: NK * NV tokens, (key, value) -> key * NV + value
ASK0 = NK * NV  # a question: which value goes with key k?
VAL0 = ASK0 + NK  # an answer: value v
FILL0 = VAL0 + NV
BOS = FILL0 + NF
VOCAB = BOS + 1
FACTS, FILL = 8, 40
T = 1 + FACTS + FILL + 2 * FACTS - 1  # 64 positions read, 65 tokens


def sequences(g: np.random.Generator, B: int):
    seq = np.empty((B, T + 1), np.int64)
    w = np.zeros((B, T), np.float32)
    for b in range(B):
        keys = g.choice(NK, FACTS, replace=False)
        vals = g.integers(0, NV, FACTS)
        facts = FACT0 + keys * NV + vals
        fill = g.integers(FILL0, FILL0 + NF, FILL)
        order = g.permutation(FACTS)
        qa = np.stack([ASK0 + keys[order], VAL0 + vals[order]], 1).reshape(-1)
        seq[b] = np.concatenate([[BOS], facts, fill, qa])
        w[b, 1 + FACTS + FILL::2] = 1.0  # the model reads a question here and must give the answer next
    return seq, w


def batch(g: np.random.Generator, B: int):
    import torch

    seq, w = sequences(g, B)
    s = torch.from_numpy(seq)
    return s[:, :-1], s[:, 1:], torch.from_numpy(w)


def accuracy(model, seed=99, n=256, **kw) -> float:
    """The share of answers that are right (the model's most likely next token), on ``n`` fresh sequences."""
    import torch

    g = np.random.default_rng(seed)
    x, y, w = batch(g, n)
    model.eval()
    with torch.no_grad():
        z = model(x, **kw)
    model.train()
    ok = (z.argmax(-1) == y).float()
    return float((ok * w).sum() / w.sum())
