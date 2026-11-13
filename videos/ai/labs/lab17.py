"""Lab 17: count the numbers a matrix product moves through a small fast memory, and run a systolic array."""

from collections import OrderedDict

import numpy as np

from videos.coursekit import labs

TITLE = "Tiling, traffic and a systolic array"
GOAL = ("Multiply two 32 x 32 matrices behind a simulated fast memory that holds M numbers, count every number "
        "fetched by the untiled loop and by the tiled loop, and compare with 2n^3/b + n^2. Then pulse a product "
        "through a systolic array and check its answer, its K + 2n - 2 cycles and its n operations per number read.")
TASKS = [
    "Give the tiled loop a memory of exactly three tiles (M = 3 b^2) instead of four. How far above the formula does "
    "the least-recently-used memory land, and why?",
    "Count cache lines instead of numbers: let one fetch bring in 8 neighbours of a row. Which loop order of the "
    "textbook product improves, i-j-k or i-k-j?",
    "Make the systolic array 8 x 8 and feed it a 9 x 9 product in tiles. What share of the cells' cycles do useful work?",
]
N = 32


def traffic(accesses, M):
    """The numbers fetched from far memory when ``accesses`` run through a least-recently-used memory of M numbers."""
    held, fetched = OrderedDict(), 0
    for key in accesses:
        if key in held:
            held.move_to_end(key)
        else:
            fetched += 1
            held[key] = True
            if len(held) > M:
                held.popitem(last=False)
    return fetched


def product(n, b):
    """The accesses of C = AB computed in b x b tiles (b = n is the untiled triple loop)."""
    for i0 in range(0, n, b):
        for j0 in range(0, n, b):
            for k0 in range(0, n, b):
                for i in range(i0, i0 + b):
                    for k in range(k0, k0 + b):
                        for j in range(j0, j0 + b):
                            yield ("A", i, k)
                            yield ("B", k, j)
                            yield ("C", i, j)


def systolic(A, B):
    """An n x n grid of multiply-add cells.  Row i of A enters from the left i cycles late, column j of B from the
    top j cycles late; each cycle a cell multiplies what passes through it, adds it to its sum, and hands the A
    number right and the B number down.  Returns (C, cycles used, active cells per cycle, numbers read)."""
    n, K = A.shape[0], A.shape[1]
    ra, rb = np.full((n, n), np.nan), np.full((n, n), np.nan)
    acc, active, reads, t = np.zeros((n, n)), [], 0, 0
    while True:
        ra[:, 1:], rb[1:, :] = ra[:, :-1].copy(), rb[:-1, :].copy()
        for i in range(n):
            ra[i, 0] = A[i, t - i] if 0 <= t - i < K else np.nan
            rb[0, i] = B[t - i, i] if 0 <= t - i < K else np.nan
            reads += 2 * (0 <= t - i < K)
        live = ~np.isnan(ra) & ~np.isnan(rb)
        if not live.any() and t >= K:
            return acc, t, active, reads
        acc[live] += ra[live] * rb[live]
        active.append(int(live.sum()))
        t += 1


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    n = N

    # 1. traffic through a fast memory of M numbers
    tiles = (2, 4, 8, 16)
    Ms = [4 * b * b for b in tiles]
    tiled = [traffic(product(n, b), M) for b, M in zip(tiles, Ms)]
    naive = [traffic(product(n, n), M) for M in Ms]
    formula = [2 * n ** 3 // b + n * n for b in tiles]
    lab.row("operations in the product, 2n^3", f"{2 * n ** 3:,}")
    for b, M, t, f, v in zip(tiles, Ms, tiled, formula, naive):
        lab.row(f"M = {M:>4} numbers, tiles of {b:>2}", f"tiled fetches {t:>6,}   2n^3/b + n^2 = {f:>6,}   "
                f"untiled loop {v:,}   FLOPs per number {2 * n ** 3 / t:.1f}")
    slope = np.polyfit(np.log(Ms), np.log(np.array(tiled) - n * n), 1)[0]
    lab.row("slope of tiled traffic against M (log-log)", f"{slope:.3f}   (Hong and Kung: -1/2)")
    assert tiled == formula, "each tile step fetches one tile of A and one of B; C is fetched once"
    assert all(v >= n ** 3 for v in naive), "the untiled loop fetches at least one number per multiply-add"
    assert abs(slope + 0.5) < 0.01, "traffic falls like 1/sqrt(M)"
    assert naive[0] > 3.5 * tiled[-1]

    # 2. a systolic array: the film's 4 x 4 example, and a wider product
    for nn, K in ((4, 4), (8, 16)):
        A, B = rng.standard_normal((nn, K)), rng.standard_normal((K, nn))
        Cs, cycles, active, reads = systolic(A, B)
        ops = 2 * sum(active)
        lab.row(f"systolic {nn} x {nn}, K = {K}", f"{cycles} cycles (K + 2n - 2 = {K + 2 * nn - 2})   "
                f"max error {np.abs(Cs - A @ B).max():.1e}   {ops / reads:.0f} operations per number read (n = {nn})")
        assert np.allclose(Cs, A @ B, atol=1e-12), "every cell holds its entry of C"
        assert cycles == K + 2 * nn - 2 and sum(active) == nn * nn * K and reads == 2 * nn * K
    lab.note = ("The arithmetic is the same 2n^3 operations every time; what changes is how often a number is used "
                "while it is close. Tiles use each fetched number b times, and a systolic array uses it n times with "
                "no cache at all.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    grid = np.geomspace(Ms[0], Ms[-1], 50)
    ax[0].plot(Ms, naive, "o-", color=labs.RED, label="untiled loop")
    ax[0].plot(Ms, tiled, "o-", color=labs.BLUE, label="tiled, b = sqrt(M)/2")
    ax[0].plot(grid, 4 * n ** 3 / np.sqrt(grid) + n * n, color=labs.GOLD, ls="--", lw=1.2, label="4n^3/sqrt(M) + n^2")
    ax[0].set(title=f"Numbers fetched for a {n} x {n} product", xlabel="fast memory M (numbers)",
              ylabel="numbers fetched", xscale="log", yscale="log")
    ax[0].legend()
    ax[1].bar(np.arange(len(active)), active, color=labs.TEAL)
    ax[1].set(title=f"Systolic array {nn} x {nn}, K = {K}: the wavefront", xlabel="cycle",
              ylabel="cells multiplying this cycle")
    ax[1].axvline(K + 2 * nn - 2 - 0.5, color=labs.MUTED, ls="--", lw=1)
    ax[1].text(K + 2 * nn - 3, max(active) * 0.97, "K + 2n - 2 cycles ", color=labs.MUTED, ha="right", va="top", fontsize=9)
    lab.fig = fig
    return lab
