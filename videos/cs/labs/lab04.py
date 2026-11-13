"""Lab 4: race a ripple-carry adder against a Kogge-Stone adder gate by gate, then sum floats three ways."""

import numpy as np

from videos.coursekit import labs
from explainer.cs.pebble import blocks, hdl

TITLE = "Carries in a chain and in a tree; rounding error in a sum"
GOAL = ("Build ripple-carry and Kogge-Stone adders of 4 to 64 bits as netlists, check them against integer "
        "addition on random and worst-case inputs, and time them in unit gate delays. Then add 100,000 float32 "
        "numbers naively, pairwise and with Kahan's compensation, and compare the errors.")
TASKS = [
    "Add 'brent-kung' and 'sklansky' to KINDS. Which has the fewest gates, and what does it pay in delay or fan-out?",
    "Time blocks.carry_skip_adder(32) with settle() and compare with its depth(): why is the deepest path never exercised?",
    "Sort the numbers by decreasing size before the naive sum, then by increasing size. Which order loses less?",
]
KINDS = ("ripple", "kogge-stone")


def adder(n, kind):
    return blocks.ripple_adder(n) if kind == "ripple" else blocks.prefix_adder(n, kind)


def kahan(x):
    """Kahan's compensated sum in float32; returns the running sums."""
    s, c, out = np.float32(0), np.float32(0), np.empty(len(x), np.float32)
    for i, v in enumerate(x):
        y = v - c
        t = s + y
        c = (t - s) - y  # what the addition just lost, recovered exactly
        s = t
        out[i] = s
    return out


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the adders: correct on every test vector, and timed
    widths = [4, 8, 16, 32, 64]
    delay = {k: [] for k in KINDS}
    gates = {k: [] for k in KINDS}
    for n in widths:
        a = rng.integers(0, 2 ** n, 2000, dtype=np.uint64, endpoint=False)
        b = rng.integers(0, 2 ** n, 2000, dtype=np.uint64, endpoint=False)
        cin = rng.integers(0, 2, 2000, dtype=np.uint64)
        a[:2], b[:2], cin[:2] = (2 ** n - 1, 0), (0, 2 ** n - 1), (1, 1)  # a carry that travels the whole word
        want = [int(x) + int(y) + int(z) for x, y, z in zip(a, b, cin)]
        for kind in KINDS:
            c = adder(n, kind)
            out = hdl.simulate(c, {"a": a, "b": b, "cin": cin})
            got = [int(s) + (int(co) << n) for s, co in zip(out["s"], out["cout"])]
            assert got == want, f"{n}-bit {kind} adder disagrees with integer addition"
            t = c.settle({"a": a.view(np.int64), "b": b.view(np.int64), "cin": cin.view(np.int64)})
            delay[kind].append(int(t.max()))
            gates[kind].append(c.size())
    for kind in KINDS:
        lab.row(f"64-bit {kind} adder", f"{gates[kind][-1]:,} gates, settles in {delay[kind][-1]} gate delays")
    lab.row("ripple delay at 4 ... 64 bits", f"{delay['ripple']}   (2n + 1: {[2 * n + 1 for n in widths]})")
    lab.row("Kogge-Stone delay", f"{delay['kogge-stone']}   (2 log2 n + 3: {[2 * int(np.log2(n)) + 3 for n in widths]})")
    assert delay["ripple"] == [2 * n + 1 for n in widths], "the carry ripples through two gates per bit"
    assert delay["kogge-stone"] == [2 * int(np.log2(n)) + 3 for n in widths], "one prefix level per doubling"
    assert (gates["ripple"][-1], gates["kogge-stone"][-1]) == (320, 1094), "the film's gate counts at 64 bits"

    # 2. summing float32 numbers: naive, pairwise, Kahan
    x = rng.uniform(0, 1, 100_000).astype(np.float32)
    exact = np.cumsum(x.astype(np.float64))
    naive = np.cumsum(x)  # float32, one after another
    comp = kahan(x)
    marks = np.unique(np.geomspace(100, len(x), 25).astype(int)) - 1
    pair = np.array([np.sum(x[:k + 1]) for k in marks])  # numpy's sum is pairwise

    def err(s, ref):
        return np.abs(s.astype(np.float64) - ref) / ref

    e_naive, e_pair, e_kahan = err(naive, exact)[-1], err(pair, exact[marks])[-1], err(comp, exact)[-1]
    u = 2.0 ** -24
    lab.row("sum of 100,000 float32: naive", f"relative error {e_naive:.1e}   (bound n u = {len(x) * u:.1e})")
    lab.row("pairwise", f"relative error {e_pair:.1e}   (bound log2(n) u = {np.log2(len(x)) * u:.1e})")
    lab.row("Kahan", f"relative error {e_kahan:.1e}   (about 2u = {2 * u:.1e})")
    assert e_naive < len(x) * u and e_pair < np.log2(len(x)) * u and e_kahan <= 2 * u
    worst_naive, worst_kahan = err(naive, exact)[10_000:].max(), err(comp, exact)[10_000:].max()
    lab.row("worst from 10,000 numbers on", f"naive {worst_naive:.1e}, Kahan {worst_kahan:.1e}")
    assert worst_kahan <= 2 * u and worst_naive > 5 * worst_kahan, "compensation recovers what the naive sum loses"
    lab.note = ("The same sum takes 129 gate delays in a chain and 15 in a prefix tree, at three times the gates; "
                "and the same numbers added in a different order lose about two decimal digits or none.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].plot(widths, delay["ripple"], "o-", color=labs.RED, label="ripple carry: 2n + 1")
    ax[0].plot(widths, delay["kogge-stone"], "o-", color=labs.GREEN, label="Kogge-Stone: 2 log2 n + 3")
    ax[0].set_xscale("log", base=2)
    ax[0].set_xticks(widths, [str(n) for n in widths])
    ax[0].set(title="Measured delay of two adders", xlabel="bits n", ylabel="gate delays until the sum settles")
    ax[0].legend()
    ks = marks + 1
    floor = u / 8  # an error of exactly zero is drawn at the bottom of the log axis
    ax[1].loglog(ks, np.maximum(err(naive, exact)[marks], floor), "o-", ms=3, color=labs.RED, label="naive, in order")
    ax[1].loglog(ks, np.maximum(err(pair, exact[marks]), floor), "o-", ms=3, color=labs.GOLD, label="pairwise")
    ax[1].loglog(ks, np.maximum(err(comp, exact)[marks], floor), "o-", ms=3, color=labs.GREEN, label="Kahan")
    ax[1].axhline(u, color=labs.MUTED, ls="--", lw=1)
    ax[1].text(ks[-1], u * 1.15, "u = 2^-24", color=labs.MUTED, fontsize=9, ha="right", va="bottom")
    ax[1].set(title="Relative error of a float32 sum", xlabel="numbers added", ylabel="relative error")
    ax[1].legend()
    lab.fig = fig
    return lab
