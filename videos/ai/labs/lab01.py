"""Lab 1: compress a sampled text with the film's arithmetic coder under three models, and count the bits."""

import numpy as np
from scipy.special import gammaln

from videos.coursekit import labs
from videos.ai.ai1 import coder  # the finite-precision arithmetic coder of chapter 8 (plain Python integers)

TITLE = "Prediction is compression: an arithmetic coder under three models"
GOAL = ("Draw 3,000 symbols from a skewed 27-symbol source, encode them with the series' arithmetic coder under the "
        "true model, a wrong model and a model that learns by counting, decode them back, and compare every code "
        "length with the text's information content, with H(p) and with H(p) + KL(p || q).")
TASKS = [
    "Lower the coder's precision from 32 bits to 16 (and FREQ_BITS to 12). How many extra bits does the text cost?",
    "Replace add-one counting by add-alpha with alpha = 0.1 and alpha = 5. Which learns this source fastest?",
    "Make the source a Markov chain (the next symbol depends on the last) and give the counting model one symbol of "
    "context. How far below H of the single-symbol frequencies does the code length fall?",
]
K, N, FREQ_BITS = 27, 3000, 16
LOG2 = np.log(2.0)


def zipf(s):
    p = 1.0 / np.arange(1, K + 1) ** s
    return p / p.sum()


def compress(text, table_for):
    """Encode ``text`` with the cumulative table ``table_for(i, history)`` at each position; decode it back.
    Returns (code length in bits, information content in bits under the integer tables, running lengths)."""
    enc, info, running = coder.Encoder(32), 0.0, []
    for i, s in enumerate(text):
        cdf = table_for(i, text[:i])
        enc.encode(int(cdf[s]), int(cdf[s + 1]), int(cdf[-1]))
        info += np.log2(cdf[-1] / (cdf[s + 1] - cdf[s]))
        running.append(len(enc.bits) + enc.pending)
    bits = enc.finish()
    dec, out = coder.Decoder(bits, 32), []
    for i in range(len(text)):
        cdf = table_for(i, np.array(out, dtype=int))
        s = dec.find(cdf)
        dec.consume(int(cdf[s]), int(cdf[s + 1]), int(cdf[-1]))
        out.append(s)
    assert np.array_equal(out, text), "the decoder must return the text exactly"
    return len(bits), info, np.array(running)


def run(seed=0):
    rng = np.random.default_rng(seed)
    p, q = zipf(1.0), zipf(0.3)  # the source, and a model that is too flat
    text = rng.choice(K, size=N, p=p)
    H = -(p * np.log2(p)).sum()
    kl = (p * np.log2(p / q)).sum()
    cdf_p, cdf_q = coder.quantize(p, FREQ_BITS), coder.quantize(q, FREQ_BITS)

    res = {"true model": compress(text, lambda i, h: cdf_p),
           "wrong model": compress(text, lambda i, h: cdf_q),
           "counting": compress(text, lambda i, h: np.concatenate([[0], np.cumsum(np.bincount(h, minlength=K) + 1)]))}
    lab = labs.Lab()
    lab.row("source entropy H(p)", f"{H:.4f} bits per symbol")
    theory = {"true model": H, "wrong model": H + kl}
    for name, (bits, info, _) in res.items():
        tail = f"   (theory {theory[name]:.4f})" if name in theory else ""
        lab.row(f"{name}: coder output", f"{bits} bits = {bits / N:.4f} per symbol{tail}")
        lab.row(f"{name}: information content", f"{info:.1f} bits; the coder spends {bits - info:+.2f} more")
    n_k = np.bincount(text, minlength=K)
    multinomial = (gammaln(N + 1) - gammaln(n_k + 1).sum()) / LOG2
    mixture = (gammaln(N + K) - gammaln(N + 1) - gammaln(K)) / LOG2  # log2 of C(N + K - 1, K - 1)
    lab.row("counting: closed form", f"{multinomial + mixture:.1f} bits = log2 multinomial + log2 C(N+K-1, K-1)")
    lab.row("counting: price of learning", f"{(res['counting'][1] - res['true model'][1]) / N:.4f} bits per symbol")
    lab.note = ("Whatever the model, the coder's output is the text's surprise under that model plus at most two bits: a "
                "better predictor is a shorter file, a wrong one pays the KL divergence on every symbol, and counting "
                "pays only a logarithmic fee for not knowing the source.")

    for name, (bits, info, _) in res.items():
        assert -0.01 < bits - info < 2.5, f"{name}: within two bits of the information content"
    sd_p = np.sqrt((p * np.log2(p) ** 2).sum() - H ** 2)  # the spread of one symbol's surprise
    sd_q = np.sqrt((p * np.log2(q) ** 2).sum() - (H + kl) ** 2)
    assert abs(res["true model"][1] / N - H) < 4 * sd_p / np.sqrt(N) + 0.01, "the true model codes at H"
    assert abs(res["wrong model"][1] / N - (H + kl)) < 4 * sd_q / np.sqrt(N) + 0.01, "a wrong model codes at H + KL"
    assert abs(res["counting"][1] - (multinomial + mixture)) < 1e-6, "Laplace's rule is a uniform mixture over sources"
    assert res["true model"][0] < res["counting"][0] < res["wrong model"][0]

    fig, ax = labs.figure(2, size=(11, 4.2))
    t = np.arange(1, N + 1)
    for (name, (_, _, running)), color in zip(res.items(), (labs.GREEN, labs.RED, labs.BLUE)):
        ax[0].plot(t, running / t, color=color, label=name)
    ax[0].axhline(H, color=labs.MUTED, ls="--", lw=1, label="H(p)")
    ax[0].axhline(H + kl, color=labs.MUTED, ls=":", lw=1, label="H(p) + KL(p || q)")
    ax[0].set(title="Bits sent per symbol so far", xlabel="symbols encoded", ylabel="bits per symbol", xscale="log",
              ylim=(H - 0.6, H + kl + 1.0))
    ax[0].legend()
    names = list(res)
    ax[1].bar(np.arange(3) - 0.2, [res[k][1] / N for k in names], 0.4, color=labs.GOLD, label="information content")
    ax[1].bar(np.arange(3) + 0.2, [res[k][0] / N for k in names], 0.4, color=labs.BLUE, label="coder output")
    ax[1].axhline(H, color=labs.MUTED, ls="--", lw=1)
    ax[1].text(2.45, H, " H(p)", color=labs.MUTED, va="bottom", ha="right", fontsize=9)
    ax[1].set(title="The whole text: surprise against file size", ylabel="bits per symbol", ylim=(H - 0.6, H + kl + 0.5))
    ax[1].set_xticks(range(3), names)
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
