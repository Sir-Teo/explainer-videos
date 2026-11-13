"""Lab 46: count a late, out-of-order stream in event-time windows, crash a checkpointed counter, and round-trip nested records through Dremel's levels."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import numpy as np

from explainer.cs.data import columnar as col
from explainer.cs.data import log as plog
from explainer.cs.data import stream as st

TITLE = "Watermarks, checkpoints and repetition levels"
GOAL = ("Run the series' stream processor over 3,000 events that arrive late, out of order and sometimes twice: trade "
        "completeness against latency with the watermark's lag, escape the trade with allowed lateness, recover a "
        "keyed counter from a crash with exactly-once state, and rebuild nested records from Dremel's levels alone.")
TASKS = [
    "Raise late_share in st.make_events from 0.05 to 0.2 and rerun the trade-off. Which lag now gives 99% completeness, and what does it cost in latency?",
    "Call st.run_windows with dedup=False and a 60 s lag. How many windows are still exact, and by how much is the total over-counted?",
    "Append a book whose only chapter has no keywords and a book with no chapters to the records, write their (r, d) levels by hand, and check them against col.dremel.",
]

PATH = [("chapters", "repeated"), ("keywords", "repeated")]


def random_books(rng, n):
    books = []
    for _ in range(n):
        chapters = [{"keywords": [f"w{int(rng.integers(100))}" for _ in range(int(rng.integers(0, 4)))]}
                    for _ in range(int(rng.integers(0, 4)))]
        books.append({"chapters": chapters})
    return books


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the watermark's lag: completeness against latency
    events = st.make_events(n=3000, seed=seed)
    lags = [0.0, 1.0, 2.0, 5.0, 10.0, 20.0, 60.0]
    runs = [st.run_windows(events, watermark_lag=lag) for lag in lags]
    dropped = [r["dropped"] for r in runs]
    latency = [r["mean_latency"] for r in runs]
    assert all(a >= b for a, b in zip(dropped, dropped[1:])), "waiting longer never drops more"
    assert all(a < b for a, b in zip(latency, latency[1:])), "and always answers later"
    assert dropped[0] > 300 and dropped[-1] <= 5 and latency[-1] > 55
    for lag, r in zip(lags, runs):
        if lag in (0.0, 5.0, 60.0):
            lab.row(f"watermark lag {lag:g} s", f"{r['dropped']} of 3,000 events dropped, {r['exact']} of "
                                                f"{r['windows']} windows exact, answers {r['mean_latency']:.1f} s after the window ends")
    late = st.run_windows(events, watermark_lag=5.0, allowed_late=90.0)
    assert late["dropped"] == 0 and late["exact"] == late["windows"] and late["refinements"] > 0
    assert abs(late["mean_latency"] - runs[3]["mean_latency"]) < 1e-9, "the first answer is as early as before"
    lab.row("lag 5 s, 90 s of allowed lateness", f"0 dropped, {late['exact']} of {late['windows']} windows exact, "
                                                 f"first answers after {late['mean_latency']:.1f} s, {late['refinements']} refinements")

    # 2. a keyed counter crashed between checkpoints
    crash = int(rng.integers(600, 2900))
    snap = st.barrier_snapshot(events, checkpoint_every=500, crash_at=crash)
    assert snap["exact_with_snapshots"], "restore the snapshot, replay from its offset: the counts are exact"
    assert snap["restored_from"] == (crash - 1) // 500 * 500 and snap["replayed"] == crash - snap["restored_from"]
    assert snap["naive_overcount"] == snap["replayed"] > 0, "replaying without restoring state counts those twice"
    lab.row(f"crash at offset {crash:,}", f"restored from {snap['restored_from']:,}, {snap['replayed']} events replayed, "
                                         f"counts exact; without the snapshot, {snap['naive_overcount']} over-counted")

    # 3. Dremel: nested records to (value, r, d) and back
    books = random_books(rng, 300)
    levels = col.dremel(books, PATH)
    assert col.reassemble(levels) == [[c["keywords"] for c in b["chapters"]] for b in books], "rebuilt from levels alone"
    values = sum(len(c["keywords"]) for b in books for c in b["chapters"])
    assert sum(1 for _, _, d in levels if d == 2) == values and sum(1 for _, r, _ in levels if r == 0) == len(books)
    assert all(0 <= r <= 2 and 0 <= d <= 2 for _, r, d in levels)
    lab.row("Dremel, 300 random books", f"{len(levels)} slots for {values} values; every record rebuilt from 2-bit levels")

    # 4. the join crossover and a compacted log
    cost = col.join_cost(big_rows=1e9, small_rows=1e6, workers=100)
    at = col.join_cost(big_rows=1e9, small_rows=cost["crossover_small_rows"], workers=100)
    assert abs(at["broadcast_bytes"] / at["shuffle_bytes"] - 1) < 1e-9 and cost["broadcast_bytes"] < cost["shuffle_bytes"]
    assert abs(cost["crossover_small_rows"] / (1e9 / 100) - 1) < 0.01, "about B / N"
    comp = plog.compaction_demo(seed=seed)
    assert comp["same_state"] and comp["after_compaction"] == comp["keys"]
    lab.row("broadcast = shuffle at", f"{cost['crossover_small_rows']:,.0f} small rows (B/N = 10,000,000); "
                                      f"{comp['events']:,} updates compact to {comp['after_compaction']} records, same state")
    lab.note = ("A watermark is a guess about time: a short lag answers early and drops late events, a long one "
                "is complete and slow, and allowed lateness keeps the early answer and corrects it. Checkpoints "
                "make the state exact after a crash only because state and source offset are restored together.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    pts = st.plot_points(seed=seed + 1)
    et, at = np.array(pts["points"]).T
    ax[0].plot([0, 60], [0, 60], color=labs.MUTED, ls="--", lw=1, label="no delay")
    ax[0].scatter(et, at, s=12, color=labs.BLUE, label="event")
    wm = np.array(pts["watermark"])
    ax[0].step(wm[:, 1], wm[:, 0], where="post", color=labs.GOLD, label="watermark: newest event time - 3 s")
    ax[0].set(title="120 events: when they happened and when they arrived", xlabel="event time (s)",
              ylabel="arrival time (s)")
    ax[0].legend(loc="upper left")
    share = [100 * d / 3000 for d in dropped]
    ax[1].plot(latency, share, "o-", color=labs.RED, label="watermark lag only")
    for lag, x, y in zip(lags, latency, share):
        ax[1].annotate(f"{lag:g} s", (x, y), textcoords="offset points", xytext=(6, 6), color=labs.MUTED, fontsize=9)
    ax[1].plot([late["mean_latency"]], [0], "*", ms=14, color=labs.GREEN, label="lag 5 s + 90 s allowed lateness")
    ax[1].set(title="Completeness against latency (labels: the lag)", xlabel="mean delay of a window's first answer (s)",
              ylabel="events dropped (%)")
    ax[1].legend()
    lab.fig = fig
    return lab
