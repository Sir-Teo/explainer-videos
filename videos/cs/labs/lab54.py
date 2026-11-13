"""Lab 54: let the SAT solver judge five binary-search midpoints, and check its verdicts against every 8-bit input."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import numpy as np

from explainer.cs.verify import absint, bdd, hoare

TITLE = "Five midpoints, one solver, and every 8-bit input"
GOAL = ("Ask the series' verifier whether each of five midpoint formulas meets lo <= mid < hi for all signed 8-bit "
        "inputs, compare each verdict with a brute-force run over all 65,536 pairs, then count the rounds interval "
        "analysis needs with and without widening and the nodes of one BDD under two variable orders.")
TASKS = [
    "Change W to 10 and to 12. Do the five verdicts change, and how do the solver's clause counts and times grow against the brute-force count of 4^W pairs?",
    "Run hoare.verify(hoare.midpoint_program('hi - ((hi - lo) >> 1)'), 8). Does this midpoint meet lo <= mid < hi? Read the counterexample and say what it does to the search loop.",
    "Analyze absint.two_counter_program() with widen=False and max_iter=60, then with widening. Which bound never settles, and why can no interval prove j == 20?",
]

W = 8


def machine_mid(index, lo, hi):
    """The five midpoints of hoare.MIDPOINTS on numpy arrays of signed W-bit values, written out independently."""
    mask, half = (1 << W) - 1, 1 << (W - 1)

    def wrap(v):
        return ((v + half) & mask) - half

    if index == 0:
        return wrap(lo + hi) >> 1                          # the textbook: the sum can wrap
    if index in (1, 3):
        return wrap(lo + (wrap(hi - lo) >> 1))             # the first fix: the difference can wrap if lo < 0
    if index == 2:
        return wrap((wrap(lo + hi) & mask) >> 1)           # the unsigned shift reads the carry
    return wrap(lo + ((wrap(hi - lo) & mask) >> 1))        # the difference read as unsigned


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the solver's verdict on each midpoint, against all 4^W inputs
    grid = np.arange(-(1 << (W - 1)), 1 << (W - 1))
    lo, hi = np.meshgrid(grid, grid, indexing="ij")
    study = hoare.midpoint_study(W)
    fails = []
    for k, row in enumerate(study):
        pre = (lo < hi) & ((lo >= 0) if "0 <= lo" in row["pre"] else True)
        mid = machine_mid(k, lo, hi)
        bad = pre & ~((lo <= mid) & (mid < hi))
        fails.append(bad)
        assert (row["status"] == "valid") == (not bad.any()), "the solver and the brute force agree on every formula"
        cex = row["counterexample"]
        if cex is not None:
            assert bad[cex["lo"] + (1 << (W - 1)), cex["hi"] + (1 << (W - 1))], "the counterexample is a real failure"
        lab.row(f"{row['mid']:<24} given {row['pre']}",
                f"solver: {row['status']:<7} ({row['clauses']:,} clauses)   brute force: {int(bad.sum()):,} of "
                f"{int(pre.sum()):,} inputs fail" + (f"   e.g. lo = {cex['lo']}, hi = {cex['hi']}" if cex else ""))
    assert [r["status"] for r in study] == ["invalid", "valid", "valid", "invalid", "valid"]

    # 2. random testing of the textbook midpoint on small arrays never sees the bug
    n = rng.integers(1, 1 << (W - 2), 2000)                 # array lengths below a quarter of the range
    a, b = np.sort(rng.integers(0, n + 1, (2, 2000)), axis=0)
    ok = a < b
    small_fail = int(fails[0][a[ok] + (1 << (W - 1)), b[ok] + (1 << (W - 1))].sum())
    assert small_fail == 0 and fails[0].sum() > 0, "the overflow needs lo + hi >= 2^(W-1): small tests cannot reach it"
    lab.row("textbook midpoint, random tests with hi < 2^(W-2)", f"{small_fail} failures in {int(ok.sum()):,} tests")

    # 3. interval analysis: plain iteration against widening and narrowing
    plain = absint.analyze(absint.counter_program(), widen=False, max_iter=200)
    wide = absint.analyze(absint.counter_program(), widen=True)
    lp, lw = plain["loops"][0], wide["loops"][0]
    assert lp["head"] == lw["head"] == {"x": [0, 100]} and plain["asserts"][0]["proved"] and wide["asserts"][0]["proved"]
    assert lp["ascending"] == 101 and lw["ascending"] + lw["narrowing"] <= 4
    lab.row("count to 100: rounds to the fixpoint [0, 100]", f"{lp['ascending']} by plain iteration, "
            f"{lw['ascending']} + {lw['narrowing']} with widening and narrowing")
    two = absint.analyze(absint.two_counter_program(), widen=True)
    assert not two["asserts"][0]["proved"], "intervals lose j = 2i, so j == 20 is a false alarm"
    lab.row("i counts to 10, j = 2i: assert j == 20", f"not proved; head {two['loops'][0]['head']}")

    # 4. one function, two variable orders
    orders = bdd.order_effect(range(1, 11))
    for r in orders:
        assert r["interleaved"] == 3 * r["n"] and r["separated"] == 3 * 2 ** r["n"] - 3
    lab.row("equality of two 10-bit words as a BDD", f"{orders[-1]['interleaved']} nodes interleaved (3n), "
            f"{orders[-1]['separated']:,} separated (3 * 2^n - 3)")
    lab.note = ("The solver's five verdicts are the truth about all 65,536 inputs; tests on small arrays never reach "
                "the overflow; widening trades 101 rounds for 4; a BDD's size is a matter of variable order.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    shade = np.zeros(lo.shape)
    shade[lo < hi] = 1
    shade[(lo < hi) & (lo >= 0)] = 2
    shade[fails[0]] = 3
    from matplotlib.colors import ListedColormap
    ax[0].imshow(shade.T, origin="lower", extent=(grid[0], grid[-1] + 1, grid[0], grid[-1] + 1), interpolation="nearest",
                 cmap=ListedColormap([labs.BG, labs.GRID, labs.BLUE, labs.RED]), vmin=0, vmax=3)
    c = study[0]["counterexample"]
    ax[0].plot([c["lo"]], [c["hi"]], "o", color=labs.GOLD, label=f"the solver's counterexample ({c['lo']}, {c['hi']})")
    ax[0].plot([], [], "s", color=labs.BLUE, label="0 <= lo < hi, mid in range")
    ax[0].plot([], [], "s", color=labs.RED, label="lo + hi wraps: mid < lo")
    ax[0].plot([], [], "s", color=labs.GRID, label="lo < 0: outside the precondition")
    ax[0].grid(False)
    ax[0].set(title="(lo + hi) >> 1 on every signed 8-bit pair", xlabel="lo", ylabel="hi")
    ax[0].legend(loc="lower right")
    for res, color, name in ((plain, labs.BLUE, "plain iteration"), (wide, labs.GOLD, "widening, then narrowing")):
        tr = [t for t in res["trace"] if "head" in t]
        ub = [150 if t["head"]["x"][1] == "+inf" else t["head"]["x"][1] for t in tr]
        ax[1].plot(range(len(ub)), ub, "o-" if len(ub) < 10 else "-", color=color, label=name, ms=5)
    ax[1].axhline(100, color=labs.MUTED, ls="--", lw=1)
    ax[1].set(title="Upper bound of x at the loop head, round by round", xlabel="round", ylabel="upper bound",
              yticks=[0, 50, 100, 150], yticklabels=["0", "50", "100", "+inf"], ylim=(-5, 160))
    ax[1].legend(loc="lower right")
    lab.fig = fig
    return lab
