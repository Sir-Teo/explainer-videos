"""Lab 45: pack containers against the exact optimum, find where a delayed autoscaler goes unstable, and check Erlang C and the mean time to data loss."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import math

import numpy as np

from explainer.cs.cloud import control as ct
from explainer.cs.cloud import durability as du
from explainer.cs.cloud import packing as pk

TITLE = "Bin packing bounds, a delayed control loop, and the nines"
GOAL = ("Run the series' four packing heuristics against its exact branch-and-bound optimum and check the proved "
        "bounds; drive its autoscaler on both sides of the stability limit K < 2 cos(d pi / (2d + 1)); and compare "
        "Erlang C and the mean time to data loss with a direct sum and a Monte Carlo run.")
TASKS = [
    "Draw the item sizes from uniform(0.34, 0.5) instead of (0.05, 0.7). Which heuristic is now furthest from the optimum, and why can no bin hold three items?",
    "Set delay=2 in ct.autoscale and find by bisection the largest gain for which the last 100 steps swing by less than half the ideal size. Compare it with 2 cos(2 pi / 5) = 0.618.",
    "Compute du.mttdl(14, 10) with repair_hours of 24, 72 and 240. By what factor do the mean years to loss fall each time, and which power of the repair time is that?",
]


def boundary(delay):
    """The largest stable gain of e[t+1] = e[t] - K e[t-d]."""
    return 2 * math.cos(delay * math.pi / (2 * delay + 1))


def swing(gain, delay, seed):
    """How far the autoscaler's server count still moves in the last 100 of 300 steps, in units of the ideal size."""
    r = ct.autoscale(gain=gain, delay=delay, steps=300, seed=seed)
    tail = [s["servers"] for s in r["series"][-100:]]
    return (max(tail) - min(tail)) / r["ideal"], r


def linear_tail(gain, delay, steps=4000):
    e = [1.0] * (delay + 1)
    for _ in range(steps):
        e.append(e[-1] - gain * e[-1 - delay])
    return max(abs(x) for x in e[-50:])


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. four heuristics against the exact optimum on 80 random instances of 16 containers
    rules = {"next fit": pk.next_fit, "first fit": pk.first_fit, "best fit": pk.best_fit, "first fit decreasing": pk.ffd}
    excess = {name: [] for name in rules}
    for _ in range(80):
        items = [round(float(x), 3) for x in rng.uniform(0.05, 0.7, 16)]
        opt = pk.optimum(items)
        assert opt >= math.ceil(sum(items) - 1e-9), "the optimum cannot beat the total size"
        for name, rule in rules.items():
            bins = rule(items)
            assert all(sum(b) <= 1 + 1e-9 for b in bins) and sorted(x for b in bins for x in b) == sorted(items)
            assert len(bins) >= opt, "no heuristic beats the optimum"
            excess[name].append(len(bins) / opt - 1)
        assert len(pk.next_fit(items)) <= 2 * opt - 1, "next fit: at most 2 OPT - 1"
        assert len(pk.ffd(items)) <= 11 / 9 * opt + 6 / 9 + 1e-9, "first fit decreasing: at most 11/9 OPT + 6/9"
    mean = {name: float(np.mean(v)) for name, v in excess.items()}
    assert mean["first fit decreasing"] < mean["first fit"] < mean["next fit"]
    lab.row("bins above the optimum, mean (worst)", "   ".join(
        f"{name} +{mean[name]:.0%} (+{max(excess[name]):.0%})" for name in rules))
    bad = pk.next_fit_bad(200)
    assert bad["next_fit"] <= 2 * bad["optimum"] - 1 and bad["ratio"] > 1.9
    lab.row("halves alternating with tiny items", f"next fit {bad['next_fit']} bins, optimum {bad['optimum']} "
                                                  f"(ratio {bad['ratio']:.2f}; the bound is 2)")

    # 2. the autoscaler: stable below K = 2 cos(d pi / (2d + 1)), unstable above
    delays = list(range(6))
    for d in delays:
        k = boundary(d)
        assert linear_tail(0.98 * k, d) < 1e-3 < 1e3 < linear_tail(1.02 * k, d), "the linear loop's exact limit"
        assert swing(0.6 * k, d, seed)[0] < 0.5 and swing(1.3 * k, d, seed)[0] > 1.5, "and the simulator agrees"
    lab.row("largest stable gain, delay 0, 1, 3", "   ".join(f"{boundary(d):.2f}" for d in (0, 1, 3))
            + "   (the simulator settles at 0.6x and oscillates at 1.3x for every delay 0..5)")

    # 3. Erlang C against the M/M/c sum, and square-root staffing
    for c, a in ((2, 1.0), (14, 10.0), (58, 50.0)):
        tail = a ** c / math.factorial(c) * c / (c - a)
        direct = tail / (sum(a ** k / math.factorial(k) for k in range(c)) + tail)
        assert abs(ct.erlang_c(c, a) - direct) < 1e-9
    assert abs(ct.erlang_c(2, 1.0) - 1 / 3) < 1e-12
    table = ct.erlang_table()
    margins = [(r["servers"] - r["load"]) / math.sqrt(r["load"]) for r in table]
    assert max(margins) < 1.5 and min(margins) > 0.9 and table[-1]["utilization"] > table[0]["utilization"]
    lab.row("servers for 10, 100, 1,000 erlangs", "   ".join(
        f"{r['servers']} ({r['utilization']:.0%} busy)" for r in (table[0], table[2], table[4]))
        + f"   (c - a)/sqrt(a) between {min(margins):.2f} and {max(margins):.2f}")

    # 4. mean time to data loss: the birth-death chain against a Monte Carlo run with exaggerated rates
    sim = du.simulate(n=3, k=1, afr=0.5, repair_hours=500.0, trials=3000, seed=seed)
    assert abs(sim["simulated_years"] / sim["exact_years"] - 1) < 0.12
    nines = {(n, k): du.mttdl(n, k)["nines"] for n, k in ((3, 1), (14, 10))}
    assert nines[(14, 10)] > nines[(3, 1)] > 9, "RS(10, 4) stores 1.4x and beats three copies at 3x"
    lab.row("three copies, exaggerated rates", f"simulated {sim['simulated_years']:.0f} years to loss, exact {sim['exact_years']:.0f}")
    lab.row("nines a year at 2% and a day's repair", f"three copies {nines[(3, 1)]:.1f}, RS(10, 4) {nines[(14, 10)]:.1f}")
    lab.note = ("Sorting before packing comes within a few percent of the optimum, a control loop acting on old "
                "measurements has a hard gain limit that shrinks with the delay, and pooled servers need only a "
                "square-root safety margin.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    for gain, color in ((0.2, labs.GREEN), (0.6, labs.RED)):
        r = ct.autoscale(gain=gain, delay=3, steps=80, seed=seed)
        ax[0].plot([s["t"] for s in r["series"]], [s["servers"] for s in r["series"]], color=color,
                   label=f"gain {gain}: {'below' if gain < boundary(3) else 'above'} the limit 0.45")
    ax[0].axhline(r["ideal"], color=labs.MUTED, ls="--", label="right size: 16.7 servers")
    ax[0].set(title="Autoscaler on a measurement three steps old", xlabel="step (load jumps at step 10)",
              ylabel="servers", yscale="log", ylim=(1, 5000))
    ax[0].legend(loc="upper right")
    dd = np.arange(0, 9)
    ax[1].plot(dd, [boundary(int(d)) for d in dd], "o-", color=labs.GOLD, label="limit: 2 cos(dπ / (2d + 1))")
    ax[1].plot(delays, [0.6 * boundary(d) for d in delays], "v", color=labs.GREEN, label="simulated: settles")
    ax[1].plot(delays, [1.3 * boundary(d) for d in delays], "^", color=labs.RED, label="simulated: oscillates")
    ax[1].set(title="Largest stable gain against delay", xlabel="delay d (steps)", ylabel="gain K")
    ax[1].legend()
    lab.fig = fig
    return lab
