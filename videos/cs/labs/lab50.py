"""Lab 50: check availability arithmetic by simulation, tip a server into a retry storm, and test a quantile sketch's guarantee."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import numpy as np

from explainer.cs.ops import observe, overload, reliability

TITLE = "Availability, a retry storm, and a sketch that keeps its promise"
GOAL = ("Compare the series, parallel and k-of-n availability formulas with a Monte Carlo of independent failures, "
        "run the series' overloaded server with and without retries after a ten-second loss of half its capacity, "
        "and check DDSketch's relative-error guarantee at five quantiles against a sample of 1,000.")
TASKS = [
    "Change the trigger from (30, 40, 0.5) to (30, 35, 0.7) and to (30, 32, 0.5). Which of them does the retrying server survive, and what decides it?",
    "Replace the policy 'budget' by 'shed' and by 'breaker'. Which answers the most requests in time over the run, and which is never stuck?",
    "Build the sketch with alpha = 0.05 instead of 0.01. How many buckets does it need now, and does the measured relative error still stay under alpha at every quantile?",
]

A = 0.99
QS = (0.5, 0.9, 0.99, 0.999, 0.9999)


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. availability: formulas against independent coin flips
    trials = 400_000
    up = rng.random((trials, 13)) < A                              # thirteen parts, each up 99% of the time
    cases = [
        ("10 parts in series", ("series", [A] * 10), up[:, :10].all(axis=1)),
        ("2 parts in parallel", ("parallel", [A] * 2), up[:, :2].any(axis=1)),
        ("10 needed of 11 (N + 1)", ("kofn", 10, [A] * 11), up[:, :11].sum(axis=1) >= 10),
        ("10 needed of 12 (N + 2)", ("kofn", 10, [A] * 12), up[:, :12].sum(axis=1) >= 10),
        ("a majority of 5", ("kofn", 3, [A] * 5), up[:, :5].sum(axis=1) >= 3),
    ]
    for name, tree, sim in cases:
        formula, measured = reliability.evaluate(tree), float(sim.mean())
        sd = np.sqrt(max(formula * (1 - formula), 1e-9) / trials)
        assert abs(measured - formula) < 5 * sd + 2e-5, name
        lab.row(f"{name}, parts up 99%", f"formula {formula:.5%} ({reliability.nines(formula):.1f} nines)   "
                                         f"simulated {measured:.5%}")
    ren = reliability.renewal(seed=seed)
    assert abs(ren["measured"] - ren["formula"]) < 5e-4, "time up is MTBF / (MTBF + MTTR)"
    lab.row("up 720 h, repair 2 h, 200 simulated years", f"{ren['measured']:.3%} up   MTBF/(MTBF+MTTR) = {ren['formula']:.3%}")

    # 2. a metastable failure: the same trigger, three client policies
    runs = {p: overload.overload(p, seconds=100, seed=seed) for p in ("none", "retries", "budget")}
    late = {p: float(np.mean(r["goodput"][70:])) for p, r in runs.items()}
    assert runs["none"]["recovered_s"] is not None and late["none"] > 70, "without retries the server recovers"
    assert runs["retries"]["recovered_s"] is None and late["retries"] < 5, "with retries the overload outlasts its cause"
    assert max(runs["retries"]["offered"]) > 3 * runs["retries"]["base"], "retries multiply the load"
    assert runs["budget"]["recovered_s"] is not None and late["budget"] > 70, "a retry budget lets it recover"
    for p, label in (("none", "no retries"), ("retries", "three immediate retries"), ("budget", "a 10% retry budget")):
        r = runs[p]
        rec = "never" if r["recovered_s"] is None else f"{r['recovered_s']:.0f} s after the trigger"
        lab.row(f"overload, {label}", f"answered in time {sum(r['goodput']):,.0f}; peak load sent {max(r['offered']):.0f}/s; "
                                      f"recovers {rec}")

    # 3. DDSketch: every quantile within a relative error alpha, where a sample of 1,000 loses the tail
    x = observe.latencies(40_000, seed)
    sketch = observe.DDSketch(0.01)
    for v in x:
        sketch.add(float(v))
    sample = np.sort(rng.choice(x, 1000, replace=False))
    true = [float(np.quantile(x, q, method="lower")) for q in QS]
    err_dd = [abs(sketch.quantile(q) - t) / t for q, t in zip(QS, true)]
    err_s = [abs(float(np.quantile(sample, q)) - t) / t for q, t in zip(QS, true)]
    assert max(err_dd) <= 0.01 + 1e-9, "DDSketch's guarantee: relative error at most alpha, at every quantile"
    assert max(err_s) > 0.05, "a sample of 1,000 cannot see the far tail"
    lab.row(f"DDSketch, alpha 1%, {sketch.buckets} buckets", "relative error at p50, p90, p99, p99.9, p99.99: "
            + ", ".join(f"{e:.2%}" for e in err_dd))
    lab.row("a sample of 1,000 values", "relative error: " + ", ".join(f"{e:.1%}" for e in err_s))
    lab.note = ("Independent parts obey the formulas to the last digit a simulation can see; the same ten-second "
                "trigger is survived without retries and never with them; and a sketch that bounds relative error "
                "keeps the tail that a sample loses.")

    fig, ax = labs.figure(2, size=(11, 4.3))
    t = np.arange(100)
    ax[0].axvspan(30, 40, color=labs.RED, alpha=0.15, label="capacity halved")
    for p, color, label in (("none", labs.BLUE, "no retries"), ("budget", labs.GREEN, "10% retry budget"),
                            ("retries", labs.GOLD, "three immediate retries")):
        ax[0].plot(t, runs[p]["goodput"], color=color, label=label)
    ax[0].plot(t, runs["retries"]["offered"], color=labs.GOLD, ls=":", lw=1.2, label="load sent, with retries")
    ax[0].set(title="Requests answered in time, each second", xlabel="seconds", ylabel="requests a second")
    ax[0].legend(loc="center right", fontsize=8)
    pos = np.arange(len(QS))
    ax[1].bar(pos - 0.2, [max(e, 1e-5) for e in err_dd], 0.4, color=labs.BLUE, label="DDSketch (alpha = 1%)")
    ax[1].bar(pos + 0.2, [max(e, 1e-5) for e in err_s], 0.4, color=labs.ORANGE, label="sample of 1,000")
    ax[1].axhline(0.01, color=labs.RED, ls="--", lw=1.2, label="the guarantee, 1%")
    ax[1].set_yscale("log")
    ax[1].set_xticks(pos, ["p50", "p90", "p99", "p99.9", "p99.99"])
    ax[1].set(title="Relative error of each latency quantile", ylabel="relative error")
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
