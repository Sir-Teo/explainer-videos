"""Lab 23: solve an LP with its dual certificate, walk the Klee-Minty cube, and measure three guarantees."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import math
import random

import numpy as np

from explainer.cs.algo import optim as op

TITLE = "A certificate, an exponential walk, and three guarantees"
GOAL = ("Run the simplex method on Chvatal's three-product LP in exact arithmetic and check its dual prices as a "
        "proof of optimality; count Dantzig's pivots on Klee-Minty cubes against 2^n - 1; then measure a factor-2 "
        "vertex cover against the exact optimum and the regret of multiplicative weights against its bound.")
TASKS = [
    "Add one unit of the first resource (b = [6, 11, 8]) and solve again. The profit rises by 1/3, not by the dual price 1: which basis changed?",
    "Run the Klee-Minty cubes with rule='bland' up to n = 10 and fit the growth of its pivot count. Is it polynomial on this family?",
    "Halve and double eta in the Hedge experiment and plot the regret: which side of the tuned value hurts more, and which term of the bound explains it?",
]
C3, A3, B3 = [5, 4, 3], [[2, 3, 1], [4, 1, 2], [3, 4, 2]], [5, 11, 8]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Chvatal's LP: the optimum and the proof that it is one
    r = op.simplex(C3, A3, B3, exact=True)
    x, y = r["x_exact"], r["duals_exact"]
    assert r["status"] == "optimal" and x == [2, 0, 1] and r["value_exact"] == 13 and r["pivots"] == 2
    assert all(sum(a * v for a, v in zip(row, x)) <= b for row, b in zip(A3, B3)), "x is feasible"
    assert all(v >= 0 for v in y) and all(sum(A3[i][j] * y[i] for i in range(3)) >= C3[j] for j in range(3)), "y is dual feasible"
    assert sum(b * v for b, v in zip(B3, y)) == sum(c * v for c, v in zip(C3, x)) == 13, "equal objectives: both optimal"
    slack = [b - sum(a * v for a, v in zip(row, x)) for row, b in zip(A3, B3)]
    assert all(s * v == 0 for s, v in zip(slack, y)), "complementary slackness"
    lab.row("three-product LP", f"x = {tuple(int(v) for v in x)}, profit {r['value_exact']} after {r['pivots']} pivots")
    lab.row("dual prices", f"y = {tuple(int(v) for v in y)}: 5 y1 + 11 y2 + 8 y3 = 13, so no plan earns more")

    # 2. Klee-Minty: 2^n - 1 pivots for Dantzig's rule, one for greatest improvement
    dims = list(range(2, 11))
    pivots = {rule: [op.simplex(*op.klee_minty(n), rule=rule, exact=True)["pivots"] for n in dims]
              for rule in ("dantzig", "bland", "steepest")}
    assert pivots["dantzig"] == [2 ** n - 1 for n in dims], "Dantzig's rule visits every vertex"
    assert pivots["steepest"] == [1] * len(dims), "greatest improvement takes one pivot on this cube"
    values = {rule: op.simplex(*op.klee_minty(8), rule=rule, exact=True)["value_exact"] for rule in pivots}
    assert len(set(values.values())) == 1 and values["dantzig"] == 5 ** 8, "every rule reaches the same optimum"
    lab.row("Klee-Minty cube, n = 10", f"Dantzig {pivots['dantzig'][-1]:,} pivots (2^10 - 1 = 1,023)   Bland {pivots['bland'][-1]}"
            f"   greatest improvement {pivots['steepest'][-1]}")

    # 3. random dense LPs: few pivots, and the same value as an independent solver
    from scipy.optimize import linprog

    counts = []
    lp_rng = random.Random(seed)
    for _ in range(30):
        c, A, b = op.random_lp(10, 10, lp_rng)
        s = op.simplex(c, A, b)
        ref = linprog([-v for v in c], A_ub=A, b_ub=b, bounds=[(0, None)] * 10, method="highs")
        assert s["status"] == "optimal" and abs(s["value"] + ref.fun) < 1e-6 * max(1, abs(ref.fun)), "agrees with HiGHS"
        counts.append(s["pivots"])
    assert max(counts) < 100, "nowhere near the 2^10 - 1 of the cube"
    lab.row("30 random LPs, 10 x 10", f"Dantzig pivots: mean {np.mean(counts):.1f}, most {max(counts)}")

    # 4. vertex cover: both ends of a maximal matching, against the exact optimum
    ratios = []
    for g in range(25):
        nv = 12
        edges = [(i, j) for i in range(nv) for j in range(i + 1, nv) if rng.random() < 0.3]
        opt = op.vertex_cover_exact(nv, edges)[0]
        cover = op.vertex_cover_matching(nv, edges, seed=g)
        assert all(u in cover or v in cover for u, v in edges) and len(cover) <= 2 * opt, "a cover within factor 2"
        if opt:
            ratios.append(len(cover) / opt)
    assert max(ratios) > 1, "and not always optimal"
    lab.row("vertex cover by matching, 25 graphs", f"mean ratio {np.mean(ratios):.2f}, worst {max(ratios):.2f}   (guarantee 2)")

    # 5. multiplicative weights: regret at most sqrt(T ln n / 2)
    n_exp, horizons, regrets = 10, [50, 100, 200, 500, 1000, 2000, 5000], []
    p = np.full(n_exp, 0.5)
    p[0] = 0.45  # one expert is slightly better, as in the film
    losses = (rng.random((horizons[-1], n_exp)) < p).astype(float)
    for T in horizons:
        alg, best, _ = op.hedge(losses[:T], math.sqrt(8 * math.log(n_exp) / T))
        regrets.append(alg - best)
        assert alg - best <= math.sqrt(T * math.log(n_exp) / 2) + 1e-9, "the regret bound holds at every horizon"
    assert regrets[-1] / horizons[-1] < 0.02, "average regret tends to zero"
    alpha, angle = op.gw_alpha()
    assert abs(alpha - 0.8786) < 1e-3 and abs(math.degrees(angle) - 133.56) < 0.5
    lab.row("Hedge, 10 experts, T = 5,000", f"regret {regrets[-1]:.1f}   (bound sqrt(T ln n / 2) = {math.sqrt(5000 * math.log(10) / 2):.1f})")
    lab.row("Goemans-Williamson constant", f"min of (theta/pi) / ((1 - cos theta)/2) = {alpha:.4f} at {math.degrees(angle):.1f} degrees")
    lab.note = ("A dual solution turns an answer into a proof; the simplex walk can be exponentially long on a "
                "crafted cube and short on random data; and a guarantee (2, sqrt(T ln n / 2), 0.878) is a bound that "
                "measurements sit inside, usually with room to spare.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    for rule, color, name in (("dantzig", labs.RED, "Dantzig: 2ⁿ − 1"), ("bland", labs.GOLD, "Bland"),
                              ("steepest", labs.GREEN, "greatest improvement")):
        ax[0].semilogy(dims, pivots[rule], "o-", color=color, label=name)
    ax[0].axhline(np.mean(counts), color=labs.BLUE, ls="--", label="random 10 × 10 LPs, mean")
    ax[0].set(title="Simplex pivots on Klee-Minty cubes", xlabel="dimension n", ylabel="pivots")
    ax[0].legend()
    ax[1].loglog(horizons, regrets, "o-", color=labs.BLUE, label="Hedge: regret against the best expert")
    ax[1].loglog(horizons, [math.sqrt(T * math.log(n_exp) / 2) for T in horizons], color=labs.GOLD, label="bound √(T ln n / 2)")
    ax[1].loglog(horizons, [0.02 * T for T in horizons], color=labs.MUTED, ls="--", label="linear regret, for scale")
    ax[1].set(title="Multiplicative weights, 10 experts", xlabel="rounds T", ylabel="expected-loss regret")
    ax[1].legend()
    lab.fig = fig
    return lab
