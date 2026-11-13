"""Lab 27: catch a cheating sum-check prover at the rate the theory predicts, and break a fingerprint with a small field."""

from videos.coursekit import labs

import random

import numpy as np

from explainer.cs.algo import proofs as P

TITLE = "Soundness, measured: sum-check and fingerprints against their bounds"
GOAL = ("Run the film's sum-check protocol on its five-clause formula with an honest prover and with one that claims "
        "one satisfying assignment too many, over fields of growing size, and compare the cheater's survival rate with "
        "1 - (1 - d/p)^n. Then test equality of two 64-bit strings by fingerprints and compare the error with (n - 1)/q.")
TASKS = [
    "Run the cheater over the prime 1,000,003 for 300 trials. How many survive, and what does zero observed successes let you conclude?",
    "Add a sixth clause to WEB. The degree bound d rises to 6: recompute the bound and check the measured survival still matches it.",
    "Replace the hard pair by two random unequal strings. Why is the measured fingerprint error then far below (n - 1)/q?",
]
WEB = [[1, 2, -3], [-1, 3, 4], [-2, -3, -4], [1, -2, 4], [-1, 2, 3]]          # chapter 6: seven satisfying assignments
PRIMES = (13, 29, 53, 97, 197, 397)
FIELDS = (17, 41, 97, 193, 257, 401, 769)
TRIALS = 400


def run(seed=0):
    rng = random.Random(int(np.random.default_rng(seed).integers(2 ** 31)))
    lab = labs.Lab()
    n, d = 4, len(WEB)
    true = P.count_sat(WEB, n)
    assert true == 7

    # 1. completeness: the honest prover is always accepted, and the transcript's checks hold
    for p in PRIMES:
        for _ in range(20):
            ok, rounds, log = P.sumcheck(WEB, n, p, true, rng)
            assert ok and rounds == n and all((r["g"][0] + r["g"][1]) % p == r["previous"] for r in log[:-1])
    lab.row("satisfying assignments of the formula", f"{true}   (the film: seven)")
    lab.row("honest prover, true claim", f"accepted in {20 * len(PRIMES)} of {20 * len(PRIMES)} runs")

    # 2. soundness: a prover claiming 8 survives only if some challenge hits a root of its error polynomial
    surv, exact = [], []
    for p in PRIMES:
        s = sum(P.sumcheck(WEB, n, p, true + 1, rng, cheat=True)[0] for _ in range(TRIALS)) / TRIALS
        e = 1 - (1 - d / p) ** n
        se = (e * (1 - e) / TRIALS) ** 0.5
        surv.append(s)
        exact.append(e)
        lab.row(f"cheater over GF({p})", f"survives {s:.3f}   1 - (1 - d/p)^n = {e:.3f}   nd/p = {min(1, n * d / p):.3f}")
        assert abs(s - e) < 4 * se + 0.01, "the cheater survives at the sequential bound, no more"
        assert s <= min(1, n * d / p) + 4 * se
    assert surv[0] > 0.6 and surv[-1] < 0.12, "a small field is unsound, a large one is not"

    # 3. fingerprints: x = bit 16, y = bit 0, so x(r) - y(r) = r^16 - 1, padded to 64 bits
    bits = 64
    x = [1 if i == 16 else 0 for i in range(bits)]
    y = [1 if i == 0 else 0 for i in range(bits)]
    err, roots = [], []
    for q in FIELDS:
        wrong = sum(P.fingerprint_eq(x, y, q, rng)[0] for _ in range(4 * TRIALS)) / (4 * TRIALS)
        k = sum(P.poly_eval(x, r, q) == P.poly_eval(y, r, q) for r in range(q)) / q       # the exact error
        err.append(wrong)
        roots.append(k)
        assert abs(wrong - k) < 4 * (k * (1 - k) / (4 * TRIALS)) ** 0.5 + 0.005 and k <= (bits - 1) / q
        assert all(P.fingerprint_eq(x, x, q, rng)[0] for _ in range(20)), "equal strings always agree"
    lab.row("fingerprints of a hard 64-bit pair, q = 17", f"wrong {err[0]:.3f}   exact {roots[0]:.3f}   bound 63/17 > 1")
    lab.row("the same pair, q = 769", f"wrong {err[-1]:.3f}   exact {roots[-1]:.3f}   bound 63/769 = {63 / 769:.3f}")
    lab.note = ("Both protocols fail only when a random field element lands on a root of a low-degree polynomial, so "
                "the error is at most degree over field size: enlarge the field and the cheater runs out of roots.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    grid = np.geomspace(11, 450, 100)
    ax[0].plot(grid, 1 - (1 - d / grid) ** n, color=labs.GOLD, label="1 − (1 − d/p)ⁿ")
    ax[0].plot(grid, np.minimum(1, n * d / grid), color=labs.MUTED, ls="--", label="union bound nd/p")
    ax[0].plot(PRIMES, surv, "o", color=labs.RED, label=f"cheater accepted, {TRIALS} runs each")
    ax[0].set(xscale="log", title="Sum-check: a false claim survives (n = 4, d = 5)", xlabel="field size p",
              ylabel="probability the verifier accepts", ylim=(0, 1.05))
    ax[0].set_xticks(PRIMES, [str(p) for p in PRIMES])
    ax[0].set_xticks([], minor=True)
    ax[0].legend()
    qs = np.geomspace(16, 800, 100)
    ax[1].plot(qs, np.minimum(1, (bits - 1) / qs), color=labs.MUTED, ls="--", label="bound (n − 1)/q, n = 64")
    ax[1].plot(FIELDS, roots, "-", color=labs.GOLD, label="exact: roots of r¹⁶ − 1, over q")
    ax[1].plot(FIELDS, err, "o", color=labs.BLUE, label="unequal strings declared equal")
    ax[1].set(xscale="log", title="Equality by fingerprint: error against field size", xlabel="field size q",
              ylabel="error probability", ylim=(0, 1.05))
    ax[1].set_xticks(FIELDS, [str(q) for q in FIELDS])
    ax[1].set_xticks([], minor=True)
    ax[1].legend()
    lab.fig = fig
    return lab
