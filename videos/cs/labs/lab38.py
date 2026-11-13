"""Lab 38: attack the series' Raft with random storms, plant a bug, and take the randomness out of its elections."""

from videos.coursekit import labs

import numpy as np

from explainer.cs.dist.raft import Cluster, random_faults

TITLE = "Raft under attack: invariants, a planted bug, and split votes"
GOAL = ("Run five-node Raft clusters through seeded storms of crashes, restarts, partitions and message loss, and "
        "check the paper's four safety invariants after every event: correct Raft must never break one, and Raft "
        "without the voters' log check must. Then start clusters with election timeouts spread over 0%, 2% and 100% "
        "of the base timeout and count how many elect a leader within a second.")
TASKS = [
    "Plant bug='commit-old-term' (the paper's Figure 8) instead. How many of the storms expose it, and why so few?",
    "Raise the loss from 0.1 to 0.4 on correct Raft. Which changes: safety, or the number of commands committed?",
    "Run seven nodes instead of five with the timeouts spread by 0.02. Does a larger cluster split its votes more or less often?",
]
STORMS, STARTS = 60, 60
SPREADS = (0.0, 0.02, 0.1, 0.5, 1.0)


def storm(seed, bug=None):
    """One cluster, six simulated seconds, about eight faults a second, as in the film's campaign."""
    c = Cluster(5, seed=seed, loss=0.1, bug=bug, delay=(0.005, 0.08))
    random_faults(c, 6, rate=8)
    c.run(until=6, client_rate=40)
    return c


def run(seed=0):
    base = 10_000 * seed
    lab = labs.Lab()
    kinds, results = {}, {}
    for bug in (None, "no-log-check"):
        broken, committed = 0, []
        for k in range(STORMS):
            c = storm(base + k, bug)
            broken += bool(c.violations)
            committed.append(len(c.committed))
            if bug:
                for kind in {v[1] for v in c.violations}:
                    kinds[kind] = kinds.get(kind, 0) + 1
        results[bug] = (broken, np.mean(committed))
    ok, bad = results[None], results["no-log-check"]
    lab.row(f"correct Raft, {STORMS} storms", f"{ok[0]} broke an invariant   (mean {ok[1]:.0f} commands committed)   the film: 0 of 1,000")
    lab.row(f"votes granted without the log check, {STORMS} storms", f"{bad[0]} broke an invariant   the film: 877 of 1,000")
    lab.row("invariants the bug broke (storms)", ", ".join(f"{k} {v}" for k, v in sorted(kinds.items())))
    assert ok[0] == 0, "correct Raft keeps all four invariants in every storm"
    assert ok[1] > 20, "and it still commits commands between the faults"
    assert bad[0] > 0.6 * STORMS, "without the election restriction a stale candidate wins and overwrites committed entries"
    assert "leader completeness" in kinds

    leaderless = []
    for sp in SPREADS:
        none = 0
        for k in range(STARTS):
            c = Cluster(5, seed=base + k, spread=sp, delay=(0.002, 0.012))
            c.run(until=1.0, client_rate=0)
            none += not any(nd.role == "leader" for nd in c.nodes)
        leaderless.append(none)
        if sp in (0.0, 0.02, 1.0):
            lab.row(f"timeouts in [T, {1 + sp:g} T]: no leader after 1 s", f"{none} of {STARTS} clusters")
    assert leaderless[0] == STARTS, "identical timeouts: every election is a split vote, for ever"
    assert leaderless[-1] == 0, "timeouts spread over [T, 2T]: every cluster elects a leader"
    assert leaderless[1] > leaderless[-2] >= leaderless[-1], "a little randomness is not enough"
    lab.note = ("Safety held in every storm and failed as soon as one line of the voting rule was removed; liveness "
                "is the part FLP says cannot be guaranteed, and randomized timeouts buy it with probability.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    names = ["correct Raft", "no log check\nwhen voting"]
    ax[0].set_axisbelow(True)
    ax[1].set_axisbelow(True)
    ax[0].bar(names, [STORMS, STORMS], color=labs.GRID)
    ax[0].bar(names, [ok[0], bad[0]], color=labs.RED)
    for k, v in enumerate((ok[0], bad[0])):
        ax[0].text(k, v + 1.5, f"{v} of {STORMS} broke an invariant", ha="center", color=labs.INK)
    ax[0].set(title="Six seconds of crashes, partitions and loss", ylabel="storms (grey: run, red: broke an invariant)", ylim=(0, STORMS * 1.15))
    ax[1].bar(range(len(SPREADS)), np.array(leaderless) / STARTS, color=labs.GOLD)
    ax[1].set(title="Clusters with no leader after one second", xlabel="spread of the election timeout (fraction of T)",
              ylabel="share of clusters", ylim=(0, 1.1), xticks=range(len(SPREADS)), xticklabels=[f"{s:g}" for s in SPREADS])
    for k, v in enumerate(leaderless):
        ax[1].text(k, v / STARTS + 0.03, f"{v}/{STARTS}", ha="center", color=labs.INK)
    lab.fig = fig
    return lab
