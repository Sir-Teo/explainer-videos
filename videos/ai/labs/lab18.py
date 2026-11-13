"""Lab 18: catch near-duplicates with MinHash bands, and measure a pipeline's bubble on the film's own simulator."""

import numpy as np

from videos.coursekit import labs
from videos.ai.ai18 import sched  # the film's exact pipeline simulator (plain Python)

TITLE = "MinHash bands and the pipeline bubble"
GOAL = ("Two claims of the part, each derived on screen, each checked here. Draw 2,400 pairs of shingle sets with "
        "known Jaccard similarity s, hash them 112 times, and compare how often a pair shares a band with "
        "1 - (1 - s^8)^14. Then run GPipe, 1F1B, interleaved 1F1B and ZB-H1 schedules through the film's simulator "
        "and compare each bubble with its formula.")
TASKS = [
    "Change the banding to 20 bands of 5 (100 hashes). Where does the S-curve cross one half, and what does it do to "
    "pairs at s = 0.5?",
    "Make the backward pass three times as long as the forward (dur = {'F': 1, 'B': 3}). Does GPipe's bubble change?",
    "Hold p = 8 and find the number of micro-batches m at which 1F1B's bubble falls under 5%; then read its peak "
    "memory and GPipe's at that m.",
]
BANDS, ROWS, UNION, PAIRS = 14, 8, 100, 300


def minhash_pair(shared, rng):
    """A pair of sets whose union has UNION shingles, ``shared`` of them in both: (signatures agree per hash)."""
    h = rng.random((BANDS * ROWS, UNION))  # one random hash value per shingle, per hash function
    only = (UNION - shared) // 2
    both = h[:, :shared].min(axis=1)
    a = np.minimum(both, h[:, shared:shared + only].min(axis=1))
    b = np.minimum(both, h[:, shared + only:].min(axis=1))
    return a == b


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. MinHash: Pr[minima agree] = J, and banding's S-curve
    levels = np.array([30, 50, 60, 66, 70, 76, 84, 92])  # shared shingles out of 100: Jaccard 0.30 ... 0.92
    s = levels / UNION
    predicted = 1 - (1 - s ** ROWS) ** BANDS
    agree, caught = [], []
    for c in levels:
        eq = np.array([minhash_pair(int(c), rng) for _ in range(PAIRS)])
        agree.append(eq.mean())
        caught.append(eq.reshape(PAIRS, BANDS, ROWS).all(axis=2).any(axis=1).mean())
    agree, caught = np.array(agree), np.array(caught)
    half = (1 - 2 ** (-1 / BANDS)) ** (1 / ROWS)
    lab.row("per-hash agreement against Jaccard", f"largest gap {np.abs(agree - s).max():.4f} over {len(s)} levels")
    for k in (1, 4, 6):
        lab.row(f"s = {s[k]:.2f}: pair shares a band", f"measured {caught[k]:.3f}   1 - (1 - s^{ROWS})^{BANDS} = "
                f"{predicted[k]:.3f}")
    lab.row("similarity caught half the time", f"{half:.3f}   ({BANDS} bands of {ROWS})")
    assert np.abs(agree - s).max() < 0.015, "a minhash agrees with probability J"
    assert np.abs(caught - predicted).max() < 0.12, "the S-curve"
    assert caught[0] < 0.02 and caught[-1] > 0.98, "dissimilar pairs are almost never compared, near-copies always"

    # 2. the pipeline bubble, on the film's simulator
    p, ms = 4, (4, 8, 16, 32, 64)
    sims = {"GPipe": [], "1F1B": [], "interleaved, v = 2": [], "ZB-H1": []}
    peaks = {}
    for m in ms:
        runs = {"GPipe": (sched.gpipe(p, m), 1, {"F": 1, "B": 2}), "1F1B": (sched.one_f_one_b(p, m), 1, {"F": 1, "B": 2}),
                "interleaved, v = 2": (sched.interleaved(p, m, 2), 2, {"F": 1, "B": 2}),
                "ZB-H1": (sched.zb_h1(p, m), 1, {"F": 1, "B": 1, "W": 1})}
        for name, (orders, v, dur) in runs.items():
            r = sched.stats(*sched.simulate_fixed(orders, p, v, dur), p, v)
            sims[name].append(r["bubble"])
            peaks[name, m] = r["peak"][0]
    ms_a = np.array(ms)
    formulas = {"GPipe": (p - 1) / (ms_a + p - 1), "1F1B": (p - 1) / (ms_a + p - 1),
                "interleaved, v = 2": (p - 1) / (2 * ms_a + p - 1), "ZB-H1": (p - 1) / (3 * ms_a + p - 1)}
    for name in sims:
        lab.row(f"{name}: bubble at p = {p}, m = 8", f"simulated {sims[name][1]:.4f}   formula {formulas[name][1]:.4f}")
        assert np.allclose(sims[name], formulas[name], atol=1e-9), name
    lab.row("micro-batches held on the first GPU, m = 64", f"GPipe {peaks['GPipe', 64]:.0f}   1F1B {peaks['1F1B', 64]:.0f}"
            f"   (p = {p})")
    assert peaks["GPipe", 64] == 64 and peaks["1F1B", 64] == p, "1F1B's memory stops growing with m"
    lab.note = ("Banding turns 112 noisy coin flips per pair into a sharp threshold near s = 0.69, so only likely "
                "duplicates are ever compared. A pipeline wastes (p - 1)/(m + p - 1) of its GPUs' time; 1F1B has the "
                "same bubble as GPipe but holds p micro-batches instead of m.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    grid = np.linspace(0.2, 1, 200)
    ax[0].plot(grid, 1 - (1 - grid ** ROWS) ** BANDS, color=labs.GOLD, label=f"1 - (1 - s^{ROWS})^{BANDS}")
    ax[0].plot(s, caught, "o", color=labs.BLUE, label=f"measured, {PAIRS} pairs per level")
    ax[0].plot(grid, grid, color=labs.MUTED, ls=":", lw=1, label="one minhash: probability s")
    ax[0].axvline(half, color=labs.MUTED, ls="--", lw=1)
    ax[0].set(title="Chance a pair shares a band", xlabel="Jaccard similarity s", ylabel="probability")
    ax[0].legend(loc="upper left")
    for (name, vals), color in zip(sims.items(), (labs.RED, labs.BLUE, labs.GREEN, labs.PURPLE)):
        ax[1].plot(ms, formulas[name], color=color, lw=1.2, ls="--" if name == "GPipe" else "-")
        ax[1].plot(ms, vals, "o", color=color, label=name, ms=8 if name == "GPipe" else 4)
    ax[1].set(title=f"The pipeline bubble against micro-batches, p = {p}", xlabel="micro-batches m",
              ylabel="idle share of GPU time", xscale="log")
    ax[1].set_xticks(ms, [str(m) for m in ms])
    ax[1].minorticks_off()
    ax[1].legend(title="dots simulated, lines formulas")
    lab.fig = fig
    return lab
