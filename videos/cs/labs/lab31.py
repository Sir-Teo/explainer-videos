"""Lab 31: run the convoy through four schedulers, then check a queue against Pollaczek-Khinchine."""

from videos.coursekit import labs  # noqa: I001  (first, so the library imports without manim)

import itertools

import numpy as np

from explainer.cs.os import queueing as Q
from explainer.cs.os import sched as S

TITLE = "The convoy, and why a busy server is slow"
GOAL = ("Schedule one long job and two short ones under FCFS, SJF and round robin; check by brute force that "
        "shortest-job-first has the least mean turnaround of every order; then simulate a single-server queue at "
        "load 0.8 with three job-size laws and compare each mean response time with Pollaczek-Khinchine's formula.")
TASKS = [
    "Let B and C arrive at tick 10 instead of 0 and compare 'sjf' with 'srtf'. Which one still reaches 50?",
    "Change discipline='fcfs' to 'srpt' for the hyperexponential sizes. How far below 23 does the mean fall?",
    "Raise the load in the right panel to 0.95 and 0.98. How many jobs does the simulation need before it settles?",
]
LOADS = (0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)


def mean_turnaround(order):
    """All jobs arrive at 0 and run to completion in this order."""
    return float(np.mean(np.cumsum(order)))


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the convoy (Chapter 7): one job of 100 ticks ahead of two of 10
    convoy = [S.Job("A", 0, [100]), S.Job("B", 0, [10]), S.Job("C", 0, [10])]
    runs = {p: S.simulate(convoy, p, quantum=5) for p in ("fcfs", "sjf", "rr")}
    turn = {p: r.metrics()["mean"]["turnaround"] for p, r in runs.items()}
    resp = {p: r.metrics()["mean"]["response"] for p, r in runs.items()}
    lab.row("convoy, mean turnaround", f"FCFS {turn['fcfs']:.0f}   SJF {turn['sjf']:.0f}   RR(5) {turn['rr']:.1f}"
                                       "   (the film: 110 and 50)")
    lab.row("convoy, mean response", f"FCFS {resp['fcfs']:.0f}   SJF {resp['sjf']:.0f}   RR(5) {resp['rr']:.1f}")
    assert turn["fcfs"] == 110 and turn["sjf"] == 50
    assert resp["rr"] < resp["sjf"] < resp["fcfs"], "round robin answers first"

    # 2. the exchange argument, by brute force: no order of six random jobs beats shortest first
    bursts = [int(b) for b in rng.integers(1, 60, 6)]
    best = min(mean_turnaround(p) for p in itertools.permutations(bursts))
    worst = max(mean_turnaround(p) for p in itertools.permutations(bursts))
    sjf = S.simulate([S.Job(f"j{i}", 0, [b]) for i, b in enumerate(bursts)], "sjf").metrics()["mean"]["turnaround"]
    lab.row("six random jobs, 720 orders", f"best {best:.2f}   worst {worst:.2f}   SJF {sjf:.2f}")
    assert abs(sjf - best) < 1e-9, "SJF is the best of all 720 orders"

    # 3. Pollaczek-Khinchine at load 0.8 (Chapter 12): the mean size is 1 in all three, only E[S^2] differs
    pk = []
    for name, size, es2 in (("deterministic", Q.det(1.0), 1.0), ("exponential", Q.expo(1.0), 2.0),
                            ("hyperexponential", Q.hyper(1.0, 10.0), 11.0)):
        r = Q.mg1(0.8, size, n=400_000, seed=seed + 3)
        theory = Q.pk(0.8, 1.0, es2)
        pk.append((name, r["mean"], theory))
        lab.row(f"M/G/1 at load 0.8, {name}", f"simulated {r['mean']:.2f}   formula {theory:.0f}")
        assert abs(r["mean"] / theory - 1) < 0.12, name
    lab.row("Little's law, the last run", f"L = {r['L']:.2f}   lambda W = {r['lam_hat'] * r['W_all']:.2f}")
    assert pk[0][1] < pk[1][1] < pk[2][1], "more variable sizes wait longer at the same load"

    # 4. the hockey stick: M/M/1 against 1/(mu - lambda)
    sim = [Q.mg1(rho, Q.expo(1.0), n=60_000, seed=seed + 10 + i)["mean"] for i, rho in enumerate(LOADS)]
    for rho, m in zip(LOADS, sim):
        if rho <= 0.8:
            assert abs(m * (1 - rho) - 1) < 0.10, rho
    lab.row("M/M/1 mean response at load 0.5, 0.9", f"{sim[2]:.2f}, {sim[-1]:.2f}   (1/(1 - rho): 2, 10)")
    lab.note = ("At the same load of 0.8 the mean response is 3, 5 or 23 service times: Pollaczek-Khinchine says "
                "the wait grows with the second moment of the job size, and with 1/(1 - rho) as the load rises.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    colors = {"A": labs.RED, "B": labs.BLUE, "C": labs.GREEN}
    for row, p in enumerate(("fcfs", "sjf", "rr")):
        for a, b, name in runs[p].segments:
            if name in colors:
                ax[0].barh(row, b - a, left=a, color=colors[name], height=0.6, edgecolor=labs.BG, linewidth=0.4)
    ax[0].set_yticks(range(3), [f"FCFS\nmean {turn['fcfs']:.0f}", f"SJF\nmean {turn['sjf']:.0f}",
                                f"RR, q = 5\nmean {turn['rr']:.0f}"])
    ax[0].set_ylim(3.15, -0.5)
    for name, c in colors.items():
        ax[0].plot([], [], color=c, lw=6, label=f"job {name}")
    ax[0].legend(loc="lower center", ncols=3)
    ax[0].set(title="The convoy: A needs 100 ticks, B and C 10 each", xlabel="tick")
    grid = np.linspace(0.05, 0.95, 200)
    ax[1].plot(grid, 1 / (1 - grid), color=labs.GOLD, label="M/M/1: 1/(1 − ρ)")
    ax[1].plot(LOADS, sim, "o", color=labs.BLUE, label="simulated, exponential sizes")
    for (name, m, theory), c in zip(pk, (labs.GREEN, labs.BLUE, labs.RED)):
        ax[1].plot([0.8], [theory], "_", color=c, ms=16, mew=2)
        ax[1].plot([0.8], [m], "s", color=c, ms=5, label=f"{name}: {m:.1f} (formula {theory:.0f})")
    ax[1].set(title="Mean response time against load (mean job size 1)", xlabel="load ρ", ylabel="service times",
              yscale="log")
    ax[1].set_ylim(0.8, 600)
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
