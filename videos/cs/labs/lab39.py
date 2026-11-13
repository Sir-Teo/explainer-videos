"""Lab 39: measure how stale a quorum read can be, and how a fan-out turns one slow server in a hundred into most requests."""

from videos.coursekit import labs

import numpy as np

from explainer.cs.dist import scale

TITLE = "Quorums that overlap, and the tail at scale"
GOAL = ("Simulate reads that follow a write by t milliseconds on three replicas: with R + W > N no read is ever "
        "stale, and with R = W = 1 the stale share decays with t. Then fan a request out to n servers, one in a "
        "hundred of which is slow, compare the slow share with 1 - 0.99^n, and hedge.")
TASKS = [
    "Try N = 5 with (R, W) = (2, 3), (3, 3) and (1, 5). Which are never stale, and which has the cheapest reads?",
    "Make servers slow 1 time in 1,000 (p_slow=0.001). At what fan-out are half of all requests slow now?",
    "Move the hedge from 30 ms to 5 ms and to 200 ms. What does each do to the median at fan-out 100, and what does 5 ms cost in extra requests?",
]
DELAYS = (0, 5, 20, 50)
FANOUTS = (1, 3, 10, 30, 100, 300)


def run(seed=0):
    lab = labs.Lab()
    configs = [(1, 1), (2, 1), (1, 2), (2, 2), (1, 3), (3, 1)]
    stale = {(r, w): [scale.pbs(3, r, w, t, trials=6000, seed=seed + 7 * k) for k, t in enumerate(DELAYS)]
             for r, w in configs}
    for (r, w), row in stale.items():
        if (r, w) in ((1, 1), (2, 1), (2, 2)):
            lab.row(f"N = 3, R = {r}, W = {w}: stale reads at 0, 5, 20, 50 ms",
                    "   ".join(f"{p:.1%}" for p in row) + ("   (the film: 54%, 32%, 7.4%, 0.34%)" if (r, w) == (1, 1) else ""))
    for (r, w), row in stale.items():
        if r + w > 3:
            assert max(row) == 0, f"R = {r}, W = {w}: the quorums overlap, so a read always meets the write"
        else:
            assert row[0] > 0.1 and row[0] > row[1] > row[2] >= row[3], "no overlap: staleness, fading with time"
    one = stale[1, 1]
    assert abs(one[0] - 0.54) < 0.04 and abs(one[1] - 0.32) < 0.04 and abs(one[2] - 0.074) < 0.02 and one[3] < 0.012

    plain = scale.tail(FANOUTS, trials=20000, seed=seed)
    hedged = scale.tail(FANOUTS, trials=20000, hedge_at=30.0, seed=seed)
    for row, h in zip(plain, hedged):
        if row["fanout"] in (1, 10, 100):
            lab.row(f"fan-out {row['fanout']}: requests that wait a second",
                    f"{row['frac_slow']:.1%}   formula {row['formula']:.1%}   median {row['p50']:.0f} ms, hedged {h['p50']:.0f} ms")
        n = max(200, 20000 // row["fanout"])
        se = np.sqrt(row["formula"] * (1 - row["formula"]) / n)
        assert abs(row["frac_slow"] - row["formula"]) < 4 * se + 0.003, "the slow share is 1 - 0.99^n"
    at100 = [r for r in plain if r["fanout"] == 100][0], [r for r in hedged if r["fanout"] == 100][0]
    assert at100[0]["p50"] > 900 and at100[1]["p50"] < 100, "at fan-out 100 the median is a slow server; a hedge removes it"
    lab.note = ("Overlapping quorums are never stale and non-overlapping ones are stale for a while; and a request "
                "that waits for a hundred servers is slow 63% of the time although each server is slow 1% of the "
                "time, until a second copy is sent after 30 ms.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ts = np.arange(0, 61, 4)
    for (r, w), color in (((1, 1), labs.RED), ((2, 1), labs.GOLD), ((2, 2), labs.GREEN)):
        ys = [scale.pbs(3, r, w, float(t), trials=1500, seed=seed + 100 + j) for j, t in enumerate(ts)]
        ax[0].plot(ts, ys, color=color, marker="o", ms=3, label=f"R = {r}, W = {w}" + (": R + W > N" if r + w > 3 else ""))
    ax[0].set(title="Three replicas: how often a read misses the last write", xlabel="milliseconds between the write's acknowledgement and the read",
              ylabel="share of reads that are stale", ylim=(-0.02, 0.7))
    ax[0].legend(loc="upper right")
    grid = np.logspace(0, np.log10(300), 100)
    ax[1].plot(grid, 1 - 0.99 ** grid, color=labs.MUTED, ls="--", label="1 - 0.99^n")
    ax[1].scatter(FANOUTS, [r["frac_slow"] for r in plain], color=labs.RED, zorder=3, label="simulated, no hedge")
    ax[1].scatter(FANOUTS, [r["frac_slow"] for r in hedged], color=labs.GREEN, zorder=3, label="simulated, hedged at 30 ms")
    ax[1].set(title="One server in a hundred takes a second", xlabel="fan-out n (servers a request waits for)",
              ylabel="share of requests that take a second", xscale="log", ylim=(-0.03, 1.05))
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
