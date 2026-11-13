"""Lab 60: clock a systolic array at gate level, check its wave against 3N - 2, and multiply in eight bits."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import numpy as np

from explainer.cs.hw import systolic

TITLE = "A matrix product as a wave"
GOAL = ("Simulate a 4 by 4 output-stationary systolic array gate by gate on 16 random products, then run both "
        "dataflows as integer models up to 64 by 64 and compare their cycles and utilization with the closed forms; "
        "finally push a Gaussian product through int8.")
TASKS = [
    "Build the cells with kind='array' (an array multiplier and a ripple-carry adder). The products stay exact: what "
    "changes in gates and in depth (cell_stats())?",
    "Stream M = N, 4N and 64N rows through the weight-stationary grid. At what M does its utilization pass the "
    "output-stationary grid's N / (3N - 2)?",
    "Quantize to 4 and to 6 bits (systolic.quantize(x, bits)) and plot the product's relative error against bits. "
    "By what factor does each extra bit shrink it?",
]


def run(seed=0):
    lab = labs.Lab()

    # 1. gate level: 16 random 4 x 4 products at once, clocked for 3N - 2 cycles
    g = systolic.output_stationary(4, trials=16, seed=seed)
    busy = [sum(k is not None for row in step["k"] for k in row) for step in g["trace"]]
    lab.row("4 x 4 grid at gate level", f"{g['gates']:,} gates, {g['cycles']} cycles, 16 of 16 products exact: "
                                        f"{g['correct']}")
    lab.row("busy cells per cycle", " ".join(str(b) for b in busy) + f"   (sum {sum(busy)} = N^3)")
    assert g["correct"], "the grid's accumulators must hold A B exactly"
    assert g["cycles"] == 3 * 4 - 2 and g["gates"] == 16 * 723, "3N - 2 cycles; N^2 cells of 723 gates"
    assert sum(busy) == 4 ** 3 == g["macs"], "every multiply-add of the product happens exactly once"
    wave = [sum(0 <= t - i - j < 4 for i in range(4) for j in range(4)) for t in range(10)]
    assert busy == wave, "cell (i, j) works on k = t - i - j: a diagonal wave"

    # 2. the same dataflows on integers, for larger grids, against the closed forms
    ns = (4, 8, 16, 32, 64)
    os_u, ws_u = [], []
    for n in ns:
        a = systolic.dataflow_model(n, dataflow="os", seed=seed + n)
        b = systolic.dataflow_model(n, 16 * n, "ws", seed=seed + n)
        assert a["correct"] and b["correct"], "both dataflows must reproduce numpy's product"
        assert a["cycles"] == 3 * n - 2 and abs(a["utilization"] - n / (3 * n - 2)) < 1e-12
        assert abs(b["utilization"] - 16 * n / (16 * n + 3 * n - 2)) < 1e-12
        os_u.append(a["utilization"])
        ws_u.append(b["utilization"])
    lab.row("output-stationary utilization, N = 4 ... 64", "  ".join(f"{u:.3f}" for u in os_u) + "   (N/(3N-2) -> 1/3)")
    lab.row("weight-stationary, a stream of 16N rows", "  ".join(f"{u:.3f}" for u in ws_u) + "   (M/(M+3N-2))")
    assert os_u[-1] < 0.34 < 0.8 < ws_u[-1], "one product keeps a third of the cells busy, a long stream over 80%"

    # 3. fewer bits: the same product through int8, with int32 accumulators
    q = systolic.quantized_matmul(n=128, seed=seed, systolic_n=32)
    lab.row("relative error of a 128 x 128 Gaussian product", f"float32 {q['float32_rel_error']:.1e}   int8 "
                                                              f"{q['int8_rel_error']:.1e}")
    lab.row("largest int32 accumulator", f"{q['max_abs_int32_acc']:,}   ({q['int32_headroom_bits']:.0f} bits of "
                                         f"headroom); a 32 x 32 int8 slice through the grid is exact: "
                                         f"{q['systolic_int8_exact']}")
    assert q["float32_rel_error"] < 1e-5 and 2e-3 < q["int8_rel_error"] < 5e-2, "int8 costs about a percent"
    assert q["systolic_int8_exact"] and q["max_abs_int32_acc"] < 128 * 127 * 127, "128 products of at most 127^2"
    lab.note = ("The grid computes every product exactly in 3N - 2 cycles, but one product alone keeps only a third "
                "of the cells busy; holding the weights still and streaming rows through fills the grid, and eight "
                "bits lose about a percent of a product's accuracy.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    n = 8
    t = np.arange(3 * n - 2)
    profile = [sum(0 <= c - i - j < n for i in range(n) for j in range(n)) for c in t]
    ax[0].bar(t, profile, color=labs.GOLD, width=0.8, label="cells doing a multiply-add")
    ax[0].axhline(n * n, color=labs.MUTED, ls="--", label=f"all {n * n} cells")
    ax[0].set_axisbelow(True)
    ax[0].set(xlabel="cycle", ylabel="busy cells", ylim=(0, n * n * 1.3),
              title=f"The wave through an {n} x {n} grid: {3 * n - 2} cycles")
    ax[0].legend(loc="upper left")
    grid = np.arange(2, 65)
    ax[1].plot(grid, grid / (3 * grid - 2), color=labs.BLUE, label="output-stationary: N / (3N - 2)")
    ax[1].plot(grid, 16 * grid / (16 * grid + 3 * grid - 2), color=labs.GREEN,
               label="weight-stationary, M = 16N: M / (M + 3N - 2)")
    ax[1].plot(ns, os_u, "o", color=labs.BLUE)
    ax[1].plot(ns, ws_u, "o", color=labs.GREEN, label="simulated (dots)")
    ax[1].axhline(1 / 3, color=labs.MUTED, ls="--", lw=1)
    ax[1].set(xlabel="grid size N", ylabel="share of cell-cycles doing work", ylim=(0, 1.19),
              title="Utilization: simulation on the closed forms")
    ax[1].legend(loc="upper right", ncol=1)
    lab.fig = fig
    return lab
