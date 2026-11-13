"""Lab 19: speculative sampling and tiled attention, two ways to go faster that leave the answer exactly the same."""

import numpy as np

from videos.coursekit import labs
from videos.ai.ai19 import attn  # the film's online softmax, FlashAttention tiles and traffic counts (numpy)

TITLE = "Faster, and exactly the same: speculative sampling and FlashAttention"
GOAL = ("Draft 200,000 tokens from a wrong distribution q, accept each with probability min(1, p/q) and resample "
        "rejections from what is left of p: check that the output has distribution p, that a draft is accepted with "
        "probability 1 - TV(p, q), and that a pass writes (1 - a^(k+1))/(1 - a) tokens. Then compute attention in "
        "tiles with the film's code and compare it, and its memory traffic, with the plain T x T table.")
TASKS = [
    "Replace the leftover distribution by p itself (resample a rejected draft from p). How far, in total variation, "
    "does the output move from p?",
    "Give a draft step a cost of c = 0.05 passes and plot the speed-up (1 - a^(k+1)) / ((1 - a)(1 + kc)). Which k is "
    "fastest at this lab's acceptance rate?",
    "Shrink the fast memory M passed to attn.io_flash_counted until tiled attention moves more numbers than the "
    "standard method. How does that M compare with d^2?",
]
V, N, KMAX = 12, 200_000, 8


def speculative(p, q, n, rng):
    """n tokens by speculative sampling: (tokens, accepted flags)."""
    draft = rng.choice(len(p), size=n, p=q)
    accept = rng.random(n) < np.minimum(1, p[draft] / q[draft])
    left = np.maximum(0, p - q)
    out = np.where(accept, draft, rng.choice(len(p), size=n, p=left / left.sum()))
    return out, accept


def tv(a, b):
    return 0.5 * np.abs(a - b).sum()


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. one token: the output is p, whatever the draft
    p = rng.dirichlet(np.full(V, 0.6))
    q = 0.55 * p + 0.45 * rng.dirichlet(np.full(V, 0.6))  # a drafter that is partly right
    out, accept = speculative(p, q, N, rng)
    emp = np.bincount(out, minlength=V) / N
    unchecked = np.bincount(rng.choice(V, size=N, p=q), minlength=V) / N
    alpha = 1 - tv(p, q)
    noise = np.sqrt(V / (2 * np.pi * N))  # roughly the TV between p and N of its own samples
    lab.row("TV(p, q): how wrong the draft is", f"{tv(p, q):.4f}")
    lab.row("TV(output, p): speculative sampling", f"{tv(emp, p):.4f}   (sampling noise alone: about {noise:.4f})")
    lab.row("TV(output, p): drafts kept unchecked", f"{tv(unchecked, p):.4f}")
    lab.row("drafts accepted", f"{accept.mean():.4f}   1 - TV(p, q) = {alpha:.4f}")
    assert tv(emp, p) < 4 * noise, "the output has the big model's distribution"
    assert tv(unchecked, p) > 0.5 * tv(p, q) > 4 * noise, "unchecked drafts do not"
    assert abs(accept.mean() - alpha) < 0.005, "acceptance = 1 - TV(p, q)"

    # 2. k drafts per pass: tokens written until the first rejection, plus the big model's own token
    passes = 40_000
    ok = rng.random((passes, KMAX)) < alpha
    measured, formula = [], []
    for k in range(1, KMAX + 1):
        first_no = np.where(ok[:, :k].all(axis=1), k, np.argmin(ok[:, :k], axis=1))
        measured.append(first_no.mean() + 1)
        formula.append((1 - alpha ** (k + 1)) / (1 - alpha))
    lab.row("tokens per pass, k = 4 drafts", f"measured {measured[3]:.3f}   (1 - a^5)/(1 - a) = {formula[3]:.3f}")
    assert np.abs(np.array(measured) - formula).max() < 0.06, "expected tokens per pass"

    # 3. attention in tiles: the same numbers, without the table
    T, d = 96, 16
    Q, K, Vv = (rng.standard_normal((T, d)) * 2 for _ in range(3))
    plain = attn.plain_attention(Q, K, Vv)
    err_flash = np.abs(attn.flash_attention(Q, K, Vv, Br=8, Bc=12) - plain).max()
    one, _ = attn.split_kv_decode(Q[-1], K, Vv, splits=5)
    err_split = np.abs(one - plain[-1]).max()
    lab.row("tiled attention against the table", f"largest difference {err_flash:.1e}   split in 5 chunks {err_split:.1e}")
    assert err_flash < 1e-12 and err_split < 1e-12, "the online softmax is exact"
    Ts = np.array([1024, 4096, 16384, 65536])
    d_h, M = 128, 100_000  # numbers in a head, numbers of fast memory
    std = np.array([attn.io_standard(int(t), d_h) for t in Ts], float)
    fla = np.array([attn.io_flash_counted(int(t), d_h, M) for t in Ts], float)
    assert all(attn.io_flash_counted(int(t), d_h, M) == attn.io_flash_formula(int(t), d_h, M) for t in Ts)
    lab.row(f"numbers moved at T = {Ts[-1]:,}", f"standard {std[-1]:.2e}   tiled {fla[-1]:.2e}   ({std[-1] / fla[-1]:.1f}x fewer)")
    assert np.all(fla < std) and std[-1] / fla[-1] > std[0] / fla[0] > 1, "the saving grows with length"
    lab.note = ("Checking a draft with min(1, p/q) and resampling from the leftover returns exactly the big model's "
                "distribution, so the draft only decides how many tokens a pass writes. Tiled attention returns the "
                "same output to rounding error, and at long lengths it moves fewer numbers than writing the table.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    w = 0.27
    order = np.argsort(-p)
    for j, (vals, color, name) in enumerate(((p, labs.GOLD, "the big model's p"), (emp, labs.BLUE, "speculative sampling"),
                                             (unchecked, labs.RED, "drafts, unchecked"))):
        ax[0].bar(np.arange(V) + (j - 1) * w, vals[order], w, color=color, label=name)
    ax[0].set(title=f"{N:,} tokens: the output's distribution", xlabel="token (sorted by p)", ylabel="probability")
    ax[0].set_xticks(range(V))
    ax[0].legend()
    ks = np.arange(1, KMAX + 1)
    for a_, color in ((0.6, labs.GREY), (0.9, labs.PURPLE)):
        ax[1].plot(ks, (1 - a_ ** (ks + 1)) / (1 - a_), color=color, lw=1.2, ls="--", label=f"formula, a = {a_}")
    ax[1].plot(ks, formula, color=labs.GOLD, label=f"formula, a = {alpha:.2f} (this draft)")
    ax[1].plot(ks, measured, "o", color=labs.BLUE, label="measured")
    ax[1].set(title="Tokens written per pass of the big model", xlabel="drafts per pass k", ylabel="tokens per pass")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
