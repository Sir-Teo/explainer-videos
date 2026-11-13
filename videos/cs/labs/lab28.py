"""Lab 28: measure Hamming(7,4) on a noisy channel, and find the exact edge of what Reed-Solomon can repair."""

from videos.coursekit import labs

import random

import numpy as np

from explainer.cs.algo import codes as C

TITLE = "Hamming(7,4) against its exact curve, and Reed-Solomon's 2e + f rule"
GOAL = ("Send random 4-bit words through a binary symmetric channel with Hamming(7,4) and compare the decoded bit-error "
        "rate with the exact value from all 128 error patterns; then damage RS(30,20) codewords over GF(256) with e "
        "errors and f erasures and check that the decoder always recovers them when 2e + f <= 10 and almost never beyond.")
TASKS = [
    "Add the overall parity bit (C.secded_decode) and count how many double errors are detected instead of miscorrected.",
    "Change NSYM from 10 to 16 with K fixed. Where does the boundary of the green region move, and what is the new rate?",
    "At p = 0.2 compare Hamming(7,4) with no code at all. Which is better, and what does the capacity 1 - H(0.2) say is possible?",
]
K, NSYM = 20, 10
WORDS = 25_000


def hamming_bit_error(p):
    """Exact: by linearity, decode each of the 128 error patterns alone and count the data bits it leaves wrong."""
    total = 0.0
    for e in range(128):
        pattern = [(e >> i) & 1 for i in range(7)]
        w = sum(pattern)
        total += p ** w * (1 - p) ** (7 - w) * sum(C.hamming74_decode(pattern)[0]) / 4
    return total


def run(seed=0):
    rng = random.Random(int(np.random.default_rng(seed).integers(2 ** 31)))
    lab = labs.Lab()

    # 1. Hamming(7,4): every single error is corrected, and the syndrome is its position
    for d in range(16):
        data = [(d >> i) & 1 for i in range(4)]
        word = C.hamming74_encode(data)
        assert C.hamming74_syndrome(word) == 0
        for pos in range(7):
            bad = list(word)
            bad[pos] ^= 1
            fixed, s = C.hamming74_decode(bad)
            assert fixed == data and s == pos + 1
    lab.row("Hamming(7,4), single errors", "all 16 x 7 corrected; the syndrome is the flipped position")
    sim, exact = {}, {}
    for p in (0.01, 0.05, 0.1):
        errs = 0
        for _ in range(WORDS):
            d = [rng.randrange(2) for _ in range(4)]
            dec, _ = C.hamming74_decode(C.bsc(C.hamming74_encode(d), p, rng))
            errs += sum(a != b for a, b in zip(d, dec))
        sim[p], exact[p] = errs / (4 * WORDS), hamming_bit_error(p)
        lab.row(f"bit error after decoding, p = {p}", f"simulated {sim[p]:.5f}   exact {exact[p]:.5f}   "
                f"no code {p}   3 copies {C.repetition_error(3, p):.5f}")
    assert abs(exact[0.01] - 8.7e-4) < 2e-5, "the film's value at p = 0.01"
    assert 0.5 < sim[0.01] / exact[0.01] < 1.6 and abs(sim[0.05] / exact[0.05] - 1) < 0.15
    assert abs(sim[0.1] / exact[0.1] - 1) < 0.1 and exact[0.1] < 0.1, "simulation matches the exact curve"

    # 2. Reed-Solomon over GF(256): e errors (positions unknown) and f erasures (positions known)
    E, F, trials = 8, 13, 5
    grid, lucky = np.zeros((E, F)), 0
    for e in range(E):
        for f in range(F):
            good = 0
            for _ in range(trials):
                msg = [rng.randrange(256) for _ in range(K)]
                cw = C.rs_encode(msg, NSYM)
                pos = rng.sample(range(K + NSYM), e + f)
                rx = list(cw)
                for q in pos[:e]:
                    rx[q] ^= rng.randrange(1, 256)
                for q in pos[e:]:
                    rx[q] = rng.randrange(256)
                try:
                    out, _ = C.rs_decode(rx, NSYM, pos[e:])
                    good += out == cw
                except ValueError:
                    pass
            grid[e, f] = good / trials
            if 2 * e + f <= NSYM:
                assert good == trials, (e, f, good)
            else:
                lucky += good
    inside = sum(1 for e in range(E) for f in range(F) if 2 * e + f <= NSYM)
    outside = (E * F - inside) * trials
    assert lucky <= 0.03 * outside, "past the bound the decoder is right only by luck"
    lab.row(f"RS({K + NSYM},{K}) over GF(256)", f"rate {K / (K + NSYM):.2f}, distance {NSYM + 1}")
    lab.row("damage with 2e + f <= 10", f"recovered in {inside * trials} of {inside * trials} trials")
    lab.row("damage with 2e + f > 10", f"recovered in {lucky} of {outside} trials   (only by a lucky guess)")
    lab.note = ("An error costs two check symbols (find it, then fix it) and an erasure one, so n - k = 10 checks buy "
                "any mix with 2e + f <= 10; one step past the edge the decoder fails or returns another codeword.")

    fig, ax = labs.figure(2, size=(11, 4.3))
    ps = np.geomspace(0.003, 0.25, 60)
    ax[0].loglog(ps, ps, color=labs.MUTED, ls="--", label="no code (rate 1)")
    ax[0].loglog(ps, [C.repetition_error(3, p) for p in ps], color=labs.GREEN, label="3 copies (rate 1/3)")
    ax[0].loglog(ps, [hamming_bit_error(p) for p in ps], color=labs.GOLD, label="Hamming(7,4), exact (rate 4/7)")
    ax[0].loglog(list(sim), list(sim.values()), "o", color=labs.BLUE, label=f"Hamming(7,4), {WORDS:,} simulated words")
    ax[0].set(title="Bit error after decoding on a binary symmetric channel", xlabel="channel flip probability p",
              ylabel="decoded bit-error rate")
    ax[0].legend()
    from matplotlib.colors import ListedColormap

    ax[1].imshow(grid, origin="lower", aspect="auto", cmap=ListedColormap([labs.RED, labs.GREEN]), vmin=0.25, vmax=0.75,
                 extent=(-0.5, F - 0.5, -0.5, E - 0.5), alpha=0.75)
    ax[1].grid(False)
    f = np.linspace(-0.5, 11.5, 50)
    ax[1].plot(f, (NSYM + 0.5 - f) / 2, color=labs.INK, ls="--", label="2e + f ≤ 10 below this line")
    ax[1].set(title="RS(30,20): green recovered, red lost", xlabel="erasures f (positions known)",
              ylabel="errors e (positions unknown)", xlim=(-0.5, F - 0.5), ylim=(-0.5, E - 0.5))
    ax[1].legend(loc="upper right")
    lab.fig = fig
    return lab
