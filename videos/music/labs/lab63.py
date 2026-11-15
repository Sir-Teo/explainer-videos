"""Lab 63: finding music, computed: a fingerprinter over a small library of rendered pieces, queried through noise;
the false-match arithmetic; implicit matrix factorization on simulated listeners against a popularity baseline; and
the feedback loop of a recommender that recommends what is already played."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import SR, Clip, concat
from explainer.music.monochord.mir import finder as F
from explainer.music.monochord.partkit import organ_tone

TITLE = "Finding music, computed"
GOAL = ("Fingerprint a library of pieces and name noisy five-second excerpts with their offsets, check how rarely chance "
        "produces a false match, learn listeners' tastes from their plays, and watch popularity feed on itself.")
TASKS = [
    "Change SNRS. At what noise level does the fingerprinter start to fail on this library?",
    "Change ALPHA, the confidence given to repeated plays. Does recall at 10 rise or fall?",
    "Change EXPLORE. How much exploration does it take to keep the top 1% of songs under a third of all plays?",
]
SNRS = [20, 5, 0, -5]
ALPHA = 20.0
EXPLORE = 0.2


def piece(seed, seconds=12.0):
    rng = np.random.default_rng(seed)
    y = np.zeros(int(seconds * SR))
    t = 0.0
    while t < seconds - 0.5:
        d = float(rng.choice([0.25, 0.5]))
        z = organ_tone(110 * 2 ** (int(rng.integers(0, 48)) / 12), d, partials=3 + seed % 5, rolloff=0.6 + 0.07 * (seed % 4))
        k = int(t * SR)
        y[k:k + len(z)] += z[: len(y) - k]
        t += d
    return y / np.max(np.abs(y)) * 0.8


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    idx = F.Index()
    songs = [piece(s) for s in range(12)]
    for k, y in enumerate(songs):
        idx.add(f"piece {k}", y, SR)
    lab.row("library: pieces, hashes", f"{len(songs)}, {idx.size:,}")
    clips, answers = [], []
    for snr in SNRS:
        ok = 0
        for k in range(len(songs)):
            a = float(rng.uniform(0, 6))
            q = songs[k][int(a * SR):int((a + 5) * SR)]
            q = q + rng.standard_normal(len(q)) * np.std(q) * 10 ** (-snr / 20)
            r = idx.query(q, SR)
            ok += r[0]["track"] == f"piece {k}"
            if k == 0:
                clips.append(Clip(q / np.max(np.abs(q)) * 0.8, SR))
                answers.append("named" if r[0]["track"] == "piece 0" else "missed")
        lab.row(f"five-second queries at {snr:+d} dB: named", f"{ok} of {len(songs)}")
        if snr == SNRS[0]:
            assert ok >= len(songs) - 1
    fm = F.false_match_rate(bits=24, query_hashes=400, db_hashes=idx.size, tracks=len(songs), offsets=400)
    lab.row("chance hits for a query, in all; at least 6 in one place", f"{fm['chance_hits']:.3f}, p = {fm['p_some_bin_at_least'][6]:.1e}")
    L = F.listeners(n_users=300, n_items=150, seed=seed, popularity=0.3)
    train, held = F.split(L["R"], 0.2, seed=1)
    fit = F.implicit_als(train, k=8, alpha=ALPHA, iters=8)
    S = fit["X"] @ fit["Y"].T
    pop = np.tile(train.sum(axis=0), (train.shape[0], 1)).astype(float)
    r_als, r_pop = F.recall_at_k(S, held, train), F.recall_at_k(pop, held, train)
    lab.row("recall at 10: popularity, implicit ALS", f"{r_pop:.3f}, {r_als:.3f}")
    assert r_als > r_pop
    loop = F.feedback_loop(n_users=200, n_items=100, rounds=15, seed=seed, explore=EXPLORE)
    lab.row(f"feedback loop (explore {EXPLORE}): Gini, top 1% share; without a recommender",
            f"{loop['gini'][-1]:.2f}, {loop['top1']:.2f}; {loop['gini_own'][-1]:.2f}, {loop['top1_own']:.2f}")
    lab.audio = concat(clips, gap=0.6)
    lab.row("ear problem: the same piece at each noise level; was it named? (listen first)", ", ".join(f"{s:+d} dB: {a}" for s, a in zip(SNRS, answers)))
    fig, (ax1, ax2) = labs.figure(2)
    S0 = F.spectrogram(F.to_8k(songs[0][: 5 * SR], SR))
    pts = F.peaks(S0)
    ax1.imshow(S0[:256], origin="lower", aspect="auto", cmap="magma")
    ax1.plot(pts[:, 0], pts[:, 1], ".", color="white", ms=3)
    ax1.set_ylim(0, 256)
    ax1.set_xlabel("frame")
    ax1.set_ylabel("bin")
    ax2.plot(loop["gini"], color=labs.GOLD, label="recommender")
    ax2.plot(loop["gini_own"], color="0.6", label="none")
    ax2.set_xlabel("round")
    ax2.set_ylabel("Gini of plays")
    ax2.legend(fontsize=7)
    lab.fig = fig
    lab.note = ("Fingerprints keep only spectrogram peaks, paired into hashes whose votes must agree in time; chance rarely "
                "piles them up; plays alone reveal tastes; and a recommender that learns from its own recommendations "
                "concentrates attention unless it explores.")
    return lab
