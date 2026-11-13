"""Lab 53: run Grover, the QFT, Shor's order finding, the CHSH game and the repetition code on the series' simulator."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import math

import numpy as np

from explainer.cs.quantum import algorithms, qec

TITLE = "Five quantum claims, each checked on a state-vector simulator"
GOAL = ("Search 64 items with Grover's two reflections and compare every round with sin^2((2k+1) theta), check the "
        "QFT circuit against numpy's FFT, factor 15 and 21 from sampled measurements by continued fractions, play "
        "the CHSH game, and measure how fast a repetition code suppresses errors.")
TASKS = [
    "Run algorithms.grover with n = 8 and max_iters = 40. Where is the first peak, where is the first trough, and what do pi/4 times sqrt(N) and the formula's period predict?",
    "Factor 21 with a = 5 instead of a = 2. What is the order, does it give factors, and which values of a fail because the order is odd or a^(r/2) = -1?",
    "In qec.repetition, read the logical error at p = 0.4 and at p = 0.6 for distances 3 to 11. On which side of p = 1/2 does adding distance help, and why?",
]


def order_from_samples(o):
    """The classical half of Shor: the smallest denominator r from the continued fractions with a^r = 1 mod N."""
    good = [s["r"] for s in o["samples"] if s["ok"]]
    return min(good) if good else None


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Grover: a rotation by 2 theta each round, so the success probability is sin^2((2k + 1) theta), exactly
    marked = int(rng.integers(0, 64))
    g = algorithms.grover(n=6, marked=marked, max_iters=20)
    gap = max(abs(a - b) for a, b in zip(g["probs"], g["formula"]))
    assert gap < 1e-9, "the simulated amplitudes follow the rotation formula"
    assert g["best_iters"] == 6 and g["p_best"] > 0.99 and g["probs"][12] < 0.01, "six rounds, and twelve overshoot"
    lab.row(f"Grover, 64 items, marked item {marked}", f"success after 0, 3, 6, 12 rounds: {g['probs'][0]:.3f}, "
            f"{g['probs'][3]:.3f}, {g['probs'][6]:.4f}, {g['probs'][12]:.4f}; largest gap to the formula {gap:.0e}")
    scale = algorithms.grover_scaling()
    assert all(abs(r["iterations"] - math.pi / 4 * math.sqrt(r["N"])) < 1 for r in scale)
    lab.row("rounds for N = 16 ... 65,536", ", ".join(str(r["iterations"]) for r in scale) + "   (pi/4 sqrt N)")

    # 2. the QFT circuit is the discrete Fourier transform, in n(n+1)/2 + n/2 gates
    q = algorithms.qft_check(n=6, seed=seed)
    assert q["max_diff_fft"] < 1e-12 and q["gates"] == 24
    lab.row("QFT on 6 qubits against numpy's FFT", f"largest difference {q['max_diff_fft']:.1e}; {q['gates']} gates "
                                                   f"against {q['fft_ops']} operations for the FFT")

    # 3. Shor: sampled measurements, continued fractions, then two gcds
    shor = {}
    for N, a in ((15, 7), (21, 2)):
        o = algorithms.order_finding(a, N, shots=20, seed=seed)
        r = order_from_samples(o)
        assert r == o["r"], "the continued fractions recover the order"
        assert sum(o["probs"][y] for y in o["peaks"]) > 0.6, "the probability sits on multiples of Q / r"
        f = sorted({math.gcd(pow(a, r // 2) - 1, N), math.gcd(pow(a, r // 2) + 1, N)})
        assert f[0] * f[1] == N and 1 < f[0] < N
        shor[N] = o
        lab.row(f"Shor, N = {N}, a = {a}, {o['t']} counting qubits", f"order {r} from {sum(s['ok'] for s in o['samples'])} of 20 "
                f"shots; gcd({a}^{r // 2} ± 1, {N}) = {f[0]} and {f[1]}")

    # 4. CHSH: a shared Bell pair beats every classical strategy
    c = algorithms.chsh(trials=100_000, seed=seed)
    assert abs(c["quantum"] - math.cos(math.pi / 8) ** 2) < 1e-12 and c["classical"] == 0.75
    assert abs(c["sampled"] - c["quantum"]) < 4 * math.sqrt(0.125 / 100_000)
    lab.row("CHSH game", f"best of 16 classical strategies {c['classical']:.2f}; Bell pair {c['quantum']:.4f} = cos^2(pi/8), "
                         f"sampled {c['sampled']:.4f}")

    # 5. the repetition code: below threshold, each step in distance divides the logical error rate
    ps = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
    rep = qec.repetition(ds=(1, 3, 5, 7), ps=ps, trials=100_000, seed=seed)
    for r in rep["rows"]:
        assert abs(r["simulated"] - r["exact"]) < 5 * math.sqrt(max(r["exact"], 1e-6) / 100_000), (r["d"], r["p"])
    at = {(r["d"], r["p"]): r["exact"] for r in rep["rows"]}
    assert all(abs(at[(d, 0.5)] - 0.5) < 1e-12 for d in (1, 3, 5, 7)), "no distance helps at p = 1/2"
    lam = rep["lambda"]["0.01"][0]
    assert 25 < lam < 35
    lab.row("repetition code at p = 1%", f"logical error {at[(3, 0.01)]:.1e} at distance 3, {at[(5, 0.01)]:.1e} at 5: "
                                         f"each step divides it by {lam:.0f}")
    lab.note = ("Grover's search is a rotation and stops paying after pi/4 sqrt(N) rounds; Shor's measurements land "
                "on multiples of Q/r and arithmetic does the rest; and error correction works only below a "
                "threshold, where distance buys an exponential suppression.")

    fig, ax = labs.figure(2, size=(11, 4.3))
    k = np.arange(21)
    fine = np.linspace(0, 20, 300)
    ax[0].plot(fine, np.sin((2 * fine + 1) * g["theta"]) ** 2, color=labs.GOLD, label="sin^2((2k + 1) theta)")
    ax[0].plot(k, g["probs"], "o", color=labs.BLUE, label="simulated, 6 qubits")
    ax[0].plot(k, 1 - np.cumprod(np.concatenate([[1.0], (63 - k[:-1]) / (64 - k[:-1])])), color=labs.MUTED, ls="--",
               label="classical: k looks")
    ax[0].set(title="Grover's search among 64 items", xlabel="rounds k", ylabel="chance of finding the marked item",
              ylim=(-0.03, 1.38))
    ax[0].set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax[0].legend(loc="upper left", ncol=3, fontsize=8)
    o = shor[21]
    ax[1].plot(np.arange(o["Q"]), o["probs"], color=labs.BLUE, lw=1.0, label="P(measure y)")
    ax[1].plot(o["peaks"], [o["probs"][y] for y in o["peaks"]], "o", color=labs.GOLD, label="multiples of 2048 / 6")
    ax[1].set(title="Shor on 21 with a = 2: the counting register", xlabel="measured value y (of 2,048)",
              ylabel="probability", ylim=(0, 0.215))
    ax[1].legend(loc="upper right", ncol=2)
    lab.fig = fig
    return lab
