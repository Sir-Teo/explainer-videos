"""A small transcription network (Part 61): log-frequency frames in, one probability per pitch out.

It is a multilayer perceptron over a few neighbouring frames, trained with binary cross-entropy, the simplest
member of the family that runs from Sigtia, Benetos and Dixon (2016) to Onsets and Frames (Hawthorne et al., 2018).
Torch is imported only here.  Checked in ``tests/music/test_transcribe.py``.
"""

from __future__ import annotations

import numpy as np


def features(S, context: int = 2) -> np.ndarray:
    """Log-compressed frames, each with ``context`` neighbours either side, normalized per frame: (frames x dims)."""
    L = np.log1p(100.0 * np.asarray(S, float) / (np.max(S) + 1e-12))
    pad = np.pad(L, ((0, 0), (context, context)), mode="edge")
    cols = [pad[:, k:k + L.shape[1]] for k in range(2 * context + 1)]
    X = np.concatenate(cols, axis=0).T
    X = X - X.mean(axis=1, keepdims=True)
    return X / (X.std(axis=1, keepdims=True) + 1e-6)


def train(X, Y, hidden: int = 256, epochs: int = 30, lr: float = 1e-3, seed: int = 0, batch: int = 256, weight: float = 3.0) -> dict:
    """Fit an MLP (two hidden layers, ReLU, dropout) to frames X and piano-roll targets Y (frames x pitches), with
    positive frames weighted ``weight`` times (notes are rarer than silence).  Returns the model and the loss per
    epoch."""
    import torch
    torch.manual_seed(seed)
    torch.set_num_threads(4)
    Xt = torch.tensor(np.asarray(X, np.float32))
    Yt = torch.tensor(np.asarray(Y, np.float32))
    model = torch.nn.Sequential(torch.nn.Linear(Xt.shape[1], hidden), torch.nn.ReLU(), torch.nn.Dropout(0.2),
                                torch.nn.Linear(hidden, hidden), torch.nn.ReLU(), torch.nn.Dropout(0.2),
                                torch.nn.Linear(hidden, Yt.shape[1]))
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    lossf = torch.nn.BCEWithLogitsLoss(pos_weight=torch.full((Yt.shape[1],), float(weight)))
    g = torch.Generator().manual_seed(seed)
    losses = []
    for _ in range(epochs):
        model.train()
        perm = torch.randperm(len(Xt), generator=g)
        tot = 0.0
        for k in range(0, len(Xt), batch):
            i = perm[k:k + batch]
            opt.zero_grad()
            loss = lossf(model(Xt[i]), Yt[i])
            loss.backward()
            opt.step()
            tot += float(loss.detach()) * len(i)
        losses.append(tot / len(Xt))
    model.eval()
    return {"model": model, "losses": losses}


def predict(fit, X) -> np.ndarray:
    """Probabilities, pitches x frames."""
    import torch
    with torch.no_grad():
        p = torch.sigmoid(fit["model"](torch.tensor(np.asarray(X, np.float32)))).numpy()
    return p.T
