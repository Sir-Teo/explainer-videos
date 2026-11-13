"""Lab 14: a GPT-style and a BERT-style model on the same tokens, and three ways to fill in a blank."""

import numpy as np

from videos.coursekit import labs
from explainer.ai.autodiff import Tensor, cross_entropy

TITLE = "Next word against fill in the blank, at equal compute"
GOAL = ("On text from a 12-symbol Markov chain, train a causal model (predict the next symbol) and a masked model "
        "(fill in 15% of the symbols from both neighbours) on the same batches with the series' autodiff. Then give "
        "both a cloze test, and compare each score with the entropy the chain's own probabilities allow.")
TASKS = [
    "Raise the masking rate from 0.15 to 0.5. How much faster does the masked model reach its floor?",
    "Make the chain second order (the next symbol depends on the last two). Which of the three scorers falls short?",
    "Score the cloze with the causal model reading right to left only. Is it as good as left to right?",
]

V, MASK, STEPS, BATCH = 12, 0.15, 600, 512


def floors(T):
    """Bits per symbol the chain allows: knowing the left neighbour only, and knowing both neighbours."""
    w, vec = np.linalg.eig(T.T)
    pi = np.real(vec[:, np.argmax(np.real(w))])
    pi /= pi.sum()
    left = -np.sum(pi[:, None] * T * np.log2(T))
    joint = pi[:, None, None] * T[:, :, None] * T[None, :, :]  # P(a, b, c)
    both = -np.sum(joint * np.log2(joint / joint.sum(axis=1, keepdims=True)))
    return left, both


def bits(logits, target):
    z = logits - logits.max(axis=1, keepdims=True)
    lp = z - np.log(np.exp(z).sum(axis=1, keepdims=True))
    return -lp[np.arange(len(target)), target].mean() / np.log(2)


def log_softmax(z):
    z = z - z.max(axis=1, keepdims=True)
    return z - np.log(np.exp(z).sum(axis=1, keepdims=True))


def run(seed=0):
    rng = np.random.default_rng(seed)
    T = rng.dirichlet(np.full(V, 0.4), size=V) * 0.97 + 0.03 / V  # each symbol's own next-symbol probabilities
    text = np.zeros(80_000, dtype=int)
    for t, u in enumerate(rng.random(len(text) - 1)):
        text[t + 1] = min(np.searchsorted(np.cumsum(T[text[t]]), u), V - 1)
    train, test = text[:60_000], text[60_000:]
    a, b, c = test[:-2], test[1:-1], test[2:]  # left neighbour, the blank, right neighbour
    h_left, h_both = floors(T)

    W = Tensor(np.zeros((V, V)), requires_grad=True)  # causal: scores for the next symbol given this one
    A = Tensor(np.zeros((V, V)), requires_grad=True)  # masked: scores for the blank from its left neighbour ...
    B = Tensor(np.zeros((V, V)), requires_grad=True)  # ... plus scores from its right neighbour
    params = [W, A, B]
    m = [np.zeros((V, V)) for _ in params]
    v = [np.zeros((V, V)) for _ in params]
    targets = {"causal": 0, "masked": 0}
    curve = []
    for step in range(1, STEPS + 1):
        pos = rng.integers(1, len(train) - 1, BATCH)  # both models read the same BATCH tokens
        hidden = pos[rng.random(BATCH) < MASK]  # the masked model is asked about 15% of them
        for p in params:
            p.grad = np.zeros((V, V))
        cross_entropy(W[train[pos - 1]], train[pos]).backward()
        if len(hidden):
            cross_entropy(A[train[hidden - 1]] + B[train[hidden + 1]], train[hidden]).backward()
        targets["causal"] += BATCH
        targets["masked"] += len(hidden)
        lr = 0.2 * (1 - step / STEPS) + 0.005
        for i, p in enumerate(params):  # Adam
            m[i] = 0.9 * m[i] + 0.1 * p.grad
            v[i] = 0.999 * v[i] + 0.001 * p.grad ** 2
            p.data -= lr * (m[i] / (1 - 0.9 ** step)) / (np.sqrt(v[i] / (1 - 0.999 ** step)) + 1e-9)
        if step % 20 == 0 or step == 1:
            curve.append((step, bits(W.data[a], b), bits(A.data[a] + B.data[c], b)))
    curve = np.array(curve)

    lp = log_softmax(W.data)  # the causal model's log p(next | this)
    cloze = {
        "causal, left side only": bits(lp[a], b),
        "causal, scoring the whole sequence": bits(lp[a] + lp[:, c].T, b),  # log p(x | left) + log p(right | x)
        "masked": bits(A.data[a] + B.data[c], b),
    }
    lab = labs.Lab()
    lab.row("floor with the left neighbour / with both", f"{h_left:.3f} / {h_both:.3f} bits")
    for name, value in cloze.items():
        lab.row(f"cloze: {name}", f"{value:.3f} bits")
    ratio = targets["causal"] / targets["masked"]
    lab.row("prediction targets, causal / masked", f"{targets['causal']:,} / {targets['masked']:,}   ({ratio:.1f} times fewer; 1/0.15 = {1 / MASK:.1f})")
    lab.row("fill-in loss above its floor after 40 steps / at the end", f"{curve[2, 2] - h_both:.3f} / {curve[-1, 2] - h_both:.3f} bits")
    lab.note = ("Reading left to right, the causal model cannot use the right neighbour and stops at the one-sided "
                "floor; asked to score every candidate's whole sequence, the same model reaches the two-sided floor, "
                "where the masked model also lands, with a sixth of the targets per token read.")
    assert h_left - h_both > 0.25, "the right neighbour carries information"
    assert abs(cloze["causal, left side only"] - h_left) < 0.05, "left to right reaches the one-sided entropy"
    assert abs(cloze["causal, scoring the whole sequence"] - h_both) < 0.05, "whole-sequence scoring is Bayes's rule"
    assert abs(cloze["masked"] - h_both) < 0.08, "the masked model reaches the two-sided entropy"
    assert abs(ratio - 1 / MASK) < 0.8, "a masked model gets about 1/0.15 times fewer targets"

    fig, ax = labs.figure(2, size=(11, 4.2))
    names = ["causal,\nleft only", "causal,\nwhole sequence", "masked"]
    ax[0].bar(names, list(cloze.values()), color=[labs.BLUE, labs.TEAL, labs.GOLD], width=0.6)
    ax[0].axhline(h_left, color=labs.BLUE, ls="--", lw=1.2, label=f"floor, left neighbour only: {h_left:.2f}")
    ax[0].axhline(h_both, color=labs.GOLD, ls="--", lw=1.2, label=f"floor, both neighbours: {h_both:.2f}")
    ax[0].set(title="Filling in a blank on held-out text", ylabel="bits per blank", ylim=(0, h_left * 1.45))
    ax[0].legend(loc="upper right")
    ax[0].set_axisbelow(True)
    ax[1].plot(curve[:, 0], np.maximum(curve[:, 1] - h_left, 2e-3), color=labs.BLUE, label="causal: next symbol, above its floor")
    ax[1].plot(curve[:, 0], np.maximum(curve[:, 2] - h_both, 2e-3), color=labs.GOLD, label="masked: fill-in, above its floor")
    ax[1].set(title="The same tokens read, a sixth of the targets", xlabel="training step (512 tokens each)",
              ylabel="bits above the chain's floor", yscale="log")
    ax[1].legend()
    lab.fig = fig
    return lab
