"""Lab 48: predict an LRU cache's hit rate with Che's approximation, then check a token bucket's envelope and a stampede."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import numpy as np

from explainer.cs.design import blocks

TITLE = "Three blocks against their formulas: a cache, a rate limiter, an expiring key"
GOAL = ("Run the series' LRU cache on a Zipf trace and compare its hit rate with Che's approximation at five sizes, "
        "check every interval of a token bucket's output against the envelope sigma + rho s, and count the rebuilds "
        "of one hot key with and without probabilistic early expiration.")
TASKS = [
    "Change the Zipf exponent from 0.9 to 0.6 and to 1.2. Where does Che's formula stay within a point of the simulation, and how does the hit rate at 1,000 entries move?",
    "Replace blocks.lru_hits by blocks.tinylfu_hits in the first loop. At which sizes does admission by frequency beat Che's LRU prediction, and how close does it come to the best static set?",
    "Raise beta in blocks.stampede from 1 to 3 and count the rebuilds in 300 s. What does the earlier refresh cost, and what does it buy?",
]

ITEMS, REQUESTS, S = 20_000, 120_000, 0.9
SIZES = (30, 100, 300, 1000, 3000)
SIGMA, RHO = 20, 100 / 60.0


def bursty(rng, horizon=600.0):
    """Arrival times that alternate 30 s at four a second with 60 s at 0.8 a second."""
    t, out = 0.0, []
    while t < horizon:
        t += rng.exponential(1 / (4.0 if int(t / 30) % 3 == 0 else 0.8))
        out.append(float(t))
    return out


def worst_excess(allowed, rate, burst, longest=10.0):
    """Brute force: the largest count in any interval [t_i, t_j] of at most `longest` seconds, minus its allowance."""
    a = np.array(allowed)
    worst = -np.inf
    for i in range(len(a)):
        j = np.searchsorted(a, a[i] + longest, side="right")
        span = a[i:j] - a[i]
        worst = max(worst, float(np.max(np.arange(1, j - i + 1) - (burst + rate * span))))
    return worst


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. LRU on Zipf traffic against Che's approximation
    trace, p = blocks.zipf_trace(REQUESTS, ITEMS, S, seed)
    tr = trace.tolist()
    lru = [blocks.lru_hits(tr, c) for c in SIZES]
    che = [blocks.che(p, c) for c in SIZES]
    static = [float(np.sort(p)[::-1][:c].sum()) for c in SIZES]
    for c, a, b, st in zip(SIZES, lru, che, static):
        lab.row(f"cache of {c:>5,} entries: LRU hit rate", f"{a:.1%}   Che {b:.1%}   best static set {st:.1%}")
        assert abs(a - b) < 0.015, "Che's approximation is within 1.5 points of the simulated LRU"
        assert a < st, "no LRU beats the best static set under independent references"

    # 2. a token bucket never exceeds sigma + rho s, in any interval; fixed windows do exceed their limit
    arrivals = bursty(rng)
    allowed = blocks.token_bucket(arrivals, RHO, SIGMA)
    ok, _ = blocks.envelope_ok(allowed, RHO, SIGMA)
    excess = worst_excess(allowed, RHO, SIGMA)
    assert ok and excess <= 1e-9, "every interval of the bucket's output is under the envelope"
    assert worst_excess(arrivals, RHO, SIGMA) > 0, "the raw trace does break the envelope, so the check can fail"
    lab.row("token bucket (sigma 20, rho 100 a minute)", f"admitted {len(allowed)} of {len(arrivals)}; "
            f"worst interval is {-excess:.2f} under sigma + rho s")

    # 3. one hot key: a stampede at every expiry, against XFetch's early refresh
    plain = blocks.stampede(seed=seed + 3)
    early = blocks.stampede(seed=seed + 3, early=True)
    assert plain["recomputations"] > 100 * early["recomputations"] and early["misses"] == 0
    assert abs(plain["recomputations"] / plain["expiries"] - 400) < 60, "about rate x rebuild time = 400 per expiry"
    lab.row("hot key, 300 s: rebuilds", f"{plain['recomputations']:,} without early expiration "
            f"(about 200 x 2 = 400 per expiry), {early['recomputations']} with it; misses {plain['misses']:,} against {early['misses']}")
    lab.note = ("A formula with one unknown, the characteristic time, predicts the LRU hit rate to within a point; "
                "the bucket's guarantee holds on every interval; a random early refresh replaces 400 rebuilds by one.")

    fig, ax = labs.figure(2, size=(11, 4.3))
    grid = np.unique(np.round(np.geomspace(20, 5000, 24)).astype(int))
    ax[0].semilogx(grid, [blocks.che(p, int(c)) for c in grid], color=labs.GOLD, label="Che's approximation")
    ax[0].semilogx(grid, [float(np.sort(p)[::-1][:int(c)].sum()) for c in grid], color=labs.MUTED, ls="--",
                   label="best static set")
    ax[0].semilogx(SIZES, lru, "o", color=labs.BLUE, label="simulated LRU")
    ax[0].set(title=f"Hit rate on Zipf traffic (s = {S}, {ITEMS:,} items)", xlabel="cache size (entries)",
              ylabel="hit rate", ylim=(0, 0.85))
    ax[0].legend(loc="upper left")
    a = np.array(allowed)
    start = int(np.argmax([np.searchsorted(a, t + 10.0) - i for i, t in enumerate(a)]))  # the busiest ten seconds
    window = a[start:np.searchsorted(a, a[start] + 10.0)] - a[start]
    s = np.linspace(0, 10, 50)
    ax[1].plot(s, SIGMA + RHO * s, color=labs.RED, label="envelope: 20 + (100/60) s")
    ax[1].step(window, np.arange(1, len(window) + 1), where="post", color=labs.GREEN, label="admitted, busiest 10 s")
    ax[1].set(title="The token bucket's busiest ten seconds", xlabel="seconds since the interval began",
              ylabel="requests admitted", xlim=(0, 10), ylim=(0, 42))
    ax[1].legend(loc="lower right")
    lab.fig = fig
    return lab
