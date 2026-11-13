"""Lab 22: catch floating point giving wrong orientation signs, then check Delaunay against the lifted hull."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import numpy as np

from explainer.cs.algo import geometry as geo

TITLE = "One predicate, and the shadow of a hull"
GOAL = ("Ask the orientation test on a grid of neighbouring doubles and compare every sign with exact arithmetic; "
        "build a Delaunay triangulation by random insertion with exact integer predicates and check it against the "
        "lower hull of the points lifted to a paraboloid; then count how often Seidel's planar LP moves its optimum.")
TASKS = [
    "Move q and r to (2, 2) and (3, 3) in the grid experiment. How does the number of wrong signs change, and why does the size of the coordinates matter?",
    "Insert the Delaunay points in sorted order (order=sorted(range(n), key=pts.__getitem__)) and compare D.created with the random order.",
    "Sort 200 random integers by lifting each x to (x, x*x) and walking geo.monotone_chain's hull: check that the walk is the sorted order.",
]


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. Kettner's grid: 128 x 128 successive doubles from (1/2, 1/2), against the line through (12, 12), (24, 24)
    q, r, size = (12.0, 12.0), (24.0, 24.0), 128
    fl, ex = geo.kettner_grid((0.5, 0.5), q, r, size)
    wrong = int((fl != ex).sum())
    assert (ex == np.sign(np.arange(size)[:, None] - np.arange(size)[None, :])).all(), "the exact sign is the diagonal"
    assert wrong > 0.1 * fl.size, "rounding gets a large share of these signs wrong"
    xs = 0.5 + np.arange(size) * 2.0 ** -53
    exact_runs = 0
    for _ in range(2000):
        i, j = (int(v) for v in rng.integers(0, size, 2))
        sign, used_exact = geo.orient_adaptive((xs[i], xs[j]), q, r)
        assert sign == ex[j, i], "the filtered predicate always returns the exact sign"
        exact_runs += used_exact
    far = [geo.orient_adaptive(tuple(rng.uniform(-1, 1, 2)), q, r)[1] for _ in range(2000)]
    assert not any(far), "far from the line the floating filter certifies its own answer"
    lab.row("orientation on 128 x 128 neighbouring doubles", f"{wrong:,} of {fl.size:,} floating signs wrong ({wrong / fl.size:.0%})")
    lab.row("filtered predicate", f"0 wrong; exact fallback on {exact_runs / 2000:.0%} of grid points, {np.mean(far):.0%} of random points")

    # 2. hulls: the monotone chain against scipy, and the hull of a parabola as a sorting network
    from scipy.spatial import ConvexHull

    pts = list(dict.fromkeys((int(a), int(b)) for a, b in rng.integers(0, 10_000, (400, 2))))
    n = len(pts)
    ctr = geo.Counter()
    hull = geo.monotone_chain(pts, ctr)
    assert set(hull) == {pts[i] for i in ConvexHull(np.array(pts)).vertices}, "the same hull vertices as Qhull"
    values = [int(v) for v in rng.choice(10_000, 200, replace=False)]
    lifted = geo.monotone_chain([(x, x * x) for x in values])
    start = lifted.index(min(lifted))
    assert [p[0] for p in lifted[start:] + lifted[:start]] == sorted(values), "a hull algorithm sorts"
    lab.row(f"hull of {n} points", f"{len(hull)} vertices, {ctr.n:,} orientation tests and {ctr.cmp:,} sort comparisons")

    # 3. Delaunay by random insertion (exact integer predicates) against the lifting map
    D = geo.delaunay(pts, seed=seed)
    tris = D.triangles()
    assert tris == geo.lifting_delaunay(pts), "Delaunay = the lower hull of (x, y, x^2 + y^2)"
    assert len(tris) == 2 * n - 2 - len(hull), "Euler: 2n - 2 - h triangles"
    for a, b, c in tris[:60]:  # the empty-circle property, exactly, on a sample
        A, B, C = pts[a], pts[b], pts[c]
        if geo.orient_int(A, B, C) < 0:
            B, C = C, B
        assert all(geo.incircle_exact(A, B, C, pts[d]) <= 0 for d in rng.integers(0, n, 40)), "an empty circle"
    edges = 3 * n - 3 - len(hull)
    lab.row("Delaunay, random insertion", f"{len(tris)} triangles = 2n - 2 - h; equal to the lifted lower hull")
    lab.row("mean degree of a site", f"{2 * edges / n:.2f}   (Euler: below 6)")
    assert 2 * edges / n < 6

    # 4. Seidel's LP: the optimum moves at most 2 H_n times in expectation
    m, orders = 200, 200
    theta = rng.uniform(0, 2 * np.pi, m)
    H = [(float(np.cos(t)), float(np.sin(t)), 1.0) for t in theta]  # half-planes tangent to the unit circle
    c = (0.6, 0.8)
    moves = [geo.seidel_lp(H, c, seed=s)[1] for s in range(orders)]
    x = geo.seidel_lp(H, c, seed=seed)[0]
    from scipy.optimize import linprog

    ref = linprog([-c[0], -c[1]], A_ub=[h[:2] for h in H], b_ub=[h[2] for h in H], bounds=[(None, None)] * 2)
    assert abs(c[0] * x[0] + c[1] * x[1] + ref.fun) < 1e-6, "the same optimum as scipy's LP"
    harmonic = 2 * sum(1 / i for i in range(1, m + 1))
    assert 3 < np.mean(moves) < harmonic + 0.5, "backwards analysis: at most 2 H_n moves in expectation"
    lab.row("Seidel's LP, 200 constraints", f"optimum moved {np.mean(moves):.1f} times on average over {orders} orders   (2 H_n = {harmonic:.1f})")
    lab.note = ("Near a line the floating determinant's sign is noise, and a filter with an exact fallback repairs it; "
                "with exact predicates the triangulation built by flips is the lifted hull's shadow, triangle for "
                "triangle.")

    fig, ax = labs.figure(2, size=(11, 4.8))
    from matplotlib.colors import ListedColormap

    shown = np.where(fl != ex, 3, fl + 1)  # 0 right, 1 on the line, 2 left, 3 wrong
    ax[0].imshow(shown, origin="lower", interpolation="nearest", vmin=0, vmax=3,
                 cmap=ListedColormap([labs.GREEN, labs.GREY, labs.BLUE, labs.RED]))
    ax[0].grid(False)
    ax[0].set(title="Floating orientation near (1/2, 1/2): red is a wrong sign",
              xlabel="x: doubles after 1/2   (blue: left, green: right, grey: on the line)", ylabel="y: doubles after 1/2")
    P = np.array(pts)
    ax[1].triplot(P[:, 0], P[:, 1], tris, color=labs.BLUE, lw=0.6)
    H2 = np.array(hull + hull[:1])
    ax[1].plot(H2[:, 0], H2[:, 1], color=labs.GOLD, lw=1.6)
    ax[1].plot(P[:, 0], P[:, 1], ".", color=labs.INK, ms=3)
    ax[1].set(title=f"Delaunay triangulation of {n} integer points (gold: the hull)", xlabel="x", ylabel="y",
              aspect="equal")
    lab.fig = fig
    return lab
