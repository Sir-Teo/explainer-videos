"""Lab 28: find the words that move prices: screening a planted vocabulary out of noise."""

import numpy as np

from videos.quant import labs
from explainer.quant.house import text

TITLE = "Screening for the words that carry sentiment"
GOAL = ("Generate documents from a 1,500-word vocabulary in which 30 words are planted with a tone that drives the "
        "return. Screen every word by how often its documents precede a rise (Ke, Kelly and Xiu's first step) and "
        "count how many planted words come back as the corpus grows.")
TASKS = [
    "Weaken the tone's effect on returns (noise sd from 1 to 3). How many documents restore the recall?",
    "Screen with a fixed alpha instead of the z-threshold. What goes wrong for rare words?",
    "Score a held-out document with text.sestm_topics and text.sestm_score and correlate the score with its return.",
]


def corpus(n_docs, seed, vocab=1500, planted=30, length=60):
    """Documents as word-count rows; half the planted words are positive, half negative; returns follow the tone."""
    rng = np.random.default_rng(seed)
    freq = 1.0 / np.arange(1, vocab + 1) ** 0.9  # a Zipf-like vocabulary
    words = rng.choice(np.arange(50, 600), planted, replace=False)
    pos, neg = words[: planted // 2], words[planted // 2:]
    tone = rng.uniform(0, 1, n_docs)
    D = np.zeros((n_docs, vocab), int)
    for i, p in enumerate(tone):
        w = freq.copy()
        w[pos] *= 1 + 3 * p
        w[neg] *= 1 + 3 * (1 - p)
        D[i] = rng.multinomial(length, w / w.sum())
    y = (tone - 0.5) * 4 + rng.standard_normal(n_docs)  # the return: tone plus noise
    return D, y, pos, neg


def run(seed=0):
    sizes = [250, 500, 1000, 2000, 4000, 8000]
    lab = labs.Lab()
    recall, precision = [], []
    for n in sizes:
        D, y, pos, neg = corpus(n, seed)
        out = text.sestm_screen(D, y, kappa=5, z=3.0)
        found = set(out["pos"]) | set(out["neg"])
        truth = set(pos) | set(neg)
        hits = len(found & truth)
        signed = len(set(out["pos"]) & set(pos)) + len(set(out["neg"]) & set(neg))
        recall.append(hits / len(truth))
        precision.append(hits / max(len(found), 1))
        lab.row(f"{n:>5,} documents", f"kept {len(found):>3} words: {hits:>2} of 30 planted ({signed} with the right sign), "
                                      f"{len(found) - hits} false")
        assert signed == hits
    lab.note = "Screening is 1,500 tests at once: the threshold z = 3 trades a few false words for the planted ones."
    assert recall[-1] > 0.9 and recall[0] < recall[-1] and precision[-1] > 0.8

    D, y, pos, neg = corpus(4000, seed)
    out = text.sestm_screen(D, y, kappa=5, z=3.0)
    fig, ax = labs.figure(2, size=(11, 4.2))
    k = np.maximum(out["k"], 1)
    colors = np.full(D.shape[1], labs.MUTED, dtype=object)
    colors[pos], colors[neg] = labs.GAIN, labs.LOSS
    order = np.argsort(np.isin(np.arange(D.shape[1]), np.concatenate([pos, neg])))
    ax[0].scatter(k[order], out["f"][order], c=list(colors[order]), s=8)
    kk = np.logspace(0.7, np.log10(k.max()), 100)
    half = 3.0 * np.sqrt(out["pi"] * (1 - out["pi"]) / kk)
    ax[0].plot(kk, out["pi"] + half, color=labs.P, lw=1)
    ax[0].plot(kk, out["pi"] - half, color=labs.P, lw=1)
    ax[0].set_xscale("log")
    ax[0].set(title="Each word: share of its documents before a rise", xlabel="documents containing the word",
              ylabel="share with a positive return", ylim=(0.2, 0.8))
    ax[1].plot(sizes, 100 * np.array(recall), "o-", color=labs.GAIN, label="planted words recovered")
    ax[1].plot(sizes, 100 * np.array(precision), "o-", color=labs.P, label="kept words that are real")
    ax[1].set_xscale("log")
    ax[1].set(title="Recovery against the size of the corpus", xlabel="documents", ylabel="%", ylim=(0, 105))
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
