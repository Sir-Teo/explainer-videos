"""Lab 20: measure four randomized algorithms against their bounds: Freivalds, Karger, Miller-Rabin and a Bloom filter."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import random

import numpy as np

from explainer.cs.algo import randomized as rz

TITLE = "Coins against their bounds"
GOAL = ("Let a wrong matrix product through Freivalds' check, contract a two-cluster graph to its minimum cut, count "
        "the bases that lie to Fermat and to Miller-Rabin, fill a Bloom filter at ten bits per word, and throw balls "
        "into bins with one and two choices; compare every rate with the bound or formula the part proves.")
TASKS = [
    "Corrupt a whole row of C instead of one entry. The pass rate falls far below 2^-k: which step of the deferred-decisions proof is no longer tight?",
    "Replace the two-cluster graph by a ring of ten vertices and tabulate which pair of edges each run cuts. How many different minimum cuts appear, and how often each?",
    "Give the Bloom filter 16 bits per word, find the best k by experiment, and compare with (m/n) ln 2 and 0.6185^(m/n).",
]


def two_clusters(size=6, bridges=3):
    """Two complete graphs on ``size`` vertices joined by ``bridges`` disjoint edges: the minimum cut is the bridges."""
    edges = [(a + off, b + off) for off in (0, size) for a in range(size) for b in range(a + 1, size)]
    return 2 * size, edges + [(i, size + i) for i in range(bridges)]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Freivalds: one wrong entry passes k rounds with probability exactly 2^-k
    n, trials = 30, 3000
    A, B = rng.integers(-9, 10, (n, n)), rng.integers(-9, 10, (n, n))
    C = A @ B
    assert all(rz.freivalds(A, B, C, rounds=3, rng=rng) for _ in range(200)), "a correct product always passes"
    bad = C.copy()
    bad[rng.integers(n), rng.integers(n)] += 1
    rounds = np.arange(1, 7)
    passed = np.array([np.mean([rz.freivalds(A, B, bad, rounds=int(k), rng=rng) for _ in range(trials)]) for k in rounds])
    for k, p in zip(rounds, passed):
        q = 0.5 ** k
        assert abs(p - q) < 4.5 * np.sqrt(q * (1 - q) / trials) + 1e-9, f"{k} rounds: {p:.4f} against {q:.4f}"
    lab.row("Freivalds, one wrong entry", "passes " + ", ".join(f"{p:.1%}" for p in passed[:4])
            + " of trials after 1, 2, 3, 4 rounds   (2^-k: 50%, 25%, 12.5%, 6.25%)")

    # 2. Karger: the minimum cut of a two-cluster graph, against 2 / (n (n - 1))
    nv, edges = two_clusters()
    runs = 3000
    cuts = np.array([rz.karger(nv, edges, rng) for _ in range(runs)])
    success, bound = float(np.mean(cuts == 3)), 2 / (nv * (nv - 1))
    assert cuts.min() == 3, "contraction never reports less than the minimum cut"
    assert bound < success < 0.9, "at least the bound, and not always right"
    lab.row("Karger, two clusters of 6", f"minimum cut found in {success:.1%} of {runs:,} runs   (bound 2/(n(n-1)) = {bound:.1%})")

    # 3. primes: 561 fools Fermat on every coprime base; Miller-Rabin's liars are at most a quarter
    fermat = sum(rz.fermat_liar(a, 561) for a in range(1, 561))
    strong = sum(rz.mr_liar(a, 561) for a in range(1, 561))
    worst = max((sum(rz.mr_liar(a, m) for a in range(1, m)) / (m - 1), m) for m in range(9, 2000, 2)
                if any(m % p == 0 for p in range(3, int(m ** 0.5) + 1, 2)))
    assert fermat == 320, "every base coprime to 561 = 3 * 11 * 17 is a Fermat liar"
    assert strong <= 560 // 4 and worst == (0.25, 9), "Rabin's quarter, attained at 9"
    prime_rng = random.Random(seed)
    assert rz.miller_rabin(2 ** 127 - 1, rng=prime_rng) and not rz.miller_rabin(2 ** 127 + 1, rng=prime_rng)
    lab.row("561 = 3 x 11 x 17", f"{fermat} Fermat liars of 560 bases, {strong} Miller-Rabin liars")
    lab.row("worst odd composite below 2,000", f"n = {worst[1]}: {worst[0]:.0%} of bases lie   (Rabin: at most 25%)")

    # 4. a Bloom filter at ten bits per word, against (1 - e^(-kn/m))^k
    words = [f"word{i}".encode() for i in range(2000)]
    others = [f"other{i}".encode() for i in range(5000)]
    ks, measured, theory = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12], [], []
    for k in ks:
        f = rz.Bloom(10 * len(words), k, key=b"lab20-%d" % seed)
        for w in words:
            f.add(w)
        if k == 7:
            assert all(w in f for w in words), "no false negatives"
            full = float(f.bits.mean())
        measured.append(float(np.mean([w in f for w in others])))
        theory.append(rz.bloom_theory(len(words), f.m, k))
    m7, t7 = measured[ks.index(7)], theory[ks.index(7)]
    assert abs(m7 - t7) < 0.006 and m7 < measured[0] / 4, "k = 7 is near 0.82%, far below one hash"
    assert abs(full - 0.5) < 0.03, "at the best k about half the bits are set"
    lab.row("Bloom, 10 bits per word, k = 7", f"false positives {m7:.2%}   (formula {t7:.2%}); bits set {full:.1%}")

    # 5. balls into bins
    one, two = rz.max_load(50_000, 1, rng), rz.max_load(50_000, 2, rng)
    assert two <= 4 and one >= two + 2, "two choices flatten the fullest bin"
    lab.row("50,000 balls, fullest bin", f"one choice {one}, two choices {two}")
    lab.note = ("Each bound is a statement about the algorithm's own coins on a fixed input: tight for Freivalds with "
                "one wrong entry, a worst case for Karger, and an idealized model for the Bloom filter's hashes.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].semilogy(rounds, passed, "o", color=labs.GOLD, ms=7, label=f"wrong product passed ({trials:,} trials each)")
    ax[0].semilogy(rounds, 0.5 ** rounds, color=labs.BLUE, label="2^-k")
    ax[0].set(title="Freivalds: false acceptance against rounds", xlabel="independent rounds k", ylabel="share of trials passed")
    ax[0].legend()
    grid = np.linspace(1, 12, 100)
    ax[1].plot(grid, 100 * (1 - np.exp(-grid / 10)) ** grid, color=labs.PURPLE, label="(1 − e^(−kn/m))^k")
    ax[1].plot(ks, 100 * np.array(measured), "o", color=labs.GREEN, label="measured, 5,000 non-words")
    ax[1].axvline(10 * np.log(2), color=labs.MUTED, ls="--", label="k = (m/n) ln 2")
    ax[1].set(title="Bloom filter, 10 bits per word", xlabel="hash functions k", ylabel="false positives (%)")
    ax[1].legend()
    lab.fig = fig
    return lab
