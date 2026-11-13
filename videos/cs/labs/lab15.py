"""Lab 15: run the Job on the series' VM under Cheney's collector in semispaces of several sizes, and price the copying."""

from videos.coursekit import labs
import numpy as np

from explainer.cs.pebble import programs as PR
from explainer.cs.runtime import bytecode as B
from explainer.cs.runtime import tricolor as T
from explainer.cs.runtime import vm as V

TITLE = "What a copying collector costs, and what a missing barrier loses"
GOAL = ("Compile the Job in the lambda core to bytecode, run it on the reference VM with Cheney's collector in "
        "semispaces from tight to roomy, and compare the words copied with the film's L / (S - L) per allocated "
        "word. Then let a mutator rewrite pointers during a tri-colour mark with no barrier, with Dijkstra's and "
        "with Yuasa's, and count the live objects the collector would have freed.")
TASKS = [
    "Replace V.Cheney(S) by V.MarkSweep(2 * S) (the same total memory). Its work is marking plus sweeping the whole heap: where does it cost less than copying?",
    "Use V.Generational(4096, S) and compare the words it copies with Cheney's at the same S. What does the nursery save, and why?",
    "In T.trial set mut_per_step=1 and then 8. How does the share of unbarriered cycles that lose an object change with the mutator's speed?",
]
WORDS = ("it is a truth universally acknowledged that single man in possession of good fortune must be want wife "
         "however little known the feelings or views such may on his first entering neighbourhood this so well "
         "fixed minds surrounding families he considered rightful property some one other their daughters").split()
SIZES = (30000, 34000, 38000, 44000, 52000, 64000, 80000)  # semispace sizes, in words
CYCLES = 200  # marking cycles per barrier


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    text = " ".join(rng.choice(WORDS, 700)) + " "
    prog, tape = B.job_program(), PR.job_tape(text)
    want = PR.job_reference(tape)

    # 1. the same program in seven semispaces
    rows = []
    for S in SIZES:
        heap = V.Cheney(S)
        try:
            vm = V.VM(prog, heap, tape=tape).run()
        except V.OutOfMemory:
            continue  # the live data does not fit: no collector can run the Job here
        assert bytes(vm.output) == want, f"the Job printed something else in a semispace of {S}"
        log = heap.log
        A, n = heap.clock, len(log)
        work = sum(r["work"] for r in log)
        L = sum(r["live"] for r in log) / max(n, 1)
        rows.append(dict(S=S, n=n, log=log, A=A, work=work, L=L, film=A * L / (S - L) if n else 0.0,
                         model=(A - S) * L / (S - L) if n else 0.0,
                         slack=(S - log[-1]["live"]) / (A - S) if n else 0.0))
    assert len(rows) >= 5, "most of the semispaces should hold the live data"
    A = rows[0]["A"]
    lab.row("text", f"{len(text):,} bytes, {A:,} words allocated ({A / len(text):.1f} per byte)")
    for r in rows:
        lab.row(f"semispace {r['S']:,}", f"{r['n']:>2} collections, {r['work']:>7,} words copied   "
                                         f"(model (A - S) L / (S - L): {r['model']:>7,.0f})")
    work = [r["work"] for r in rows]
    assert all(a >= b for a, b in zip(work, work[1:])), "more memory should never mean more copying"
    # Every collection but the last is paid back by the S - live words allocated after it (the first S words are
    # free), so the copying is (A - S) L / (S - L) with L the mean live size, short by at most the last cycle.
    for r in rows:
        if r["n"]:
            assert 0.98 * r["model"] <= r["work"] <= 1.02 * r["model"] * (1 + r["slack"]), \
                f"semispace {r['S']}: copied {r['work']}, the model says {r['model']:.0f}"
    assert sum(r["n"] >= 5 for r in rows) >= 2, "the tight semispaces should collect many times"
    assert all(r["work"] <= 1.05 * r["film"] for r in rows if r["n"]), "the film's A L / (S - L) is an upper estimate"
    assert work[0] > 4 * work[-1], "a tight heap should cost several times a roomy one"

    # 2. marking while the program runs
    lost = {}
    for barrier in (None, "dijkstra", "yuasa"):
        trials = [T.trial(1000 * seed + s, barrier=barrier) for s in range(CYCLES)]
        lost[barrier] = (sum(1 for t in trials if t["lost"]), sum(t["floating"] for t in trials) / CYCLES)
    for barrier, name in ((None, "no barrier"), ("dijkstra", "Dijkstra's insertion barrier"), ("yuasa", "Yuasa's deletion barrier")):
        lab.row(name, f"{lost[barrier][0]:>3} of {CYCLES} cycles lose a live object, "
                      f"{lost[barrier][1]:.1f} dead objects kept per cycle")
    assert lost[None][0] > CYCLES // 10, "a hostile mutator should hide objects from an unbarriered collector"
    assert lost["dijkstra"][0] == 0 and lost["yuasa"][0] == 0, "a barrier must never lose a live object"
    lab.note = ("Copying costs nothing for garbage and L words per collection for live data, so the price per "
                "allocated word falls as L / (S - L) when memory grows; a barrier trades a little floating garbage "
                "for never freeing an object the program can still reach.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    S = np.array([r["S"] for r in rows])
    ax[0].plot(S / 1000, [r["film"] / r["A"] for r in rows], color=labs.GREY, ls="--", label="L / (S - L)")
    ax[0].plot(S / 1000, [r["model"] / r["A"] for r in rows], color=labs.GOLD, label="(1 - S/A) L / (S - L)")
    ax[0].plot(S / 1000, [r["work"] / r["A"] for r in rows], "o", color=labs.BLUE, label="measured on the VM")
    ax[0].set(title="Cheney's collector: words copied per word allocated", xlabel="semispace S (thousand words)",
              ylabel="copied / allocated", ylim=(0, None))
    ax[0].legend()
    tight = rows[0]["log"]
    xs, ys, last, base = [0], [0], 0, 0
    for r in tight:  # fill to the collection, then drop to what survived it
        xs += [r["clock"], r["clock"]]
        ys += [base + r["clock"] - last, r["live"]]
        last, base = r["clock"], r["live"]
    xs.append(A)
    ys.append(base + A - last)
    ax[1].plot(np.array(xs) / 1000, np.array(ys) / 1000, color=labs.BLUE, label="words in use")
    ax[1].plot([r["clock"] / 1000 for r in tight], [r["live"] / 1000 for r in tight], "o", ms=4,
               color=labs.GREEN, label="live after a collection")
    ax[1].axhline(rows[0]["S"] / 1000, color=labs.RED, ls="--", lw=1, label=f"semispace: {rows[0]['S']:,} words")
    ax[1].set(title="The Job's heap in the tightest semispace", xlabel="words allocated so far (thousands)",
              ylabel="thousand words")
    ax[1].legend(loc="lower right")
    lab.fig = fig
    return lab
