"""Lab 7: run a sort on Pebble's five-stage pipeline and account for every cycle above one per instruction."""

from videos.coursekit import labs

import numpy as np

from explainer.cs.pebble import assemble
from explainer.cs.pebble import predict as PR
from explainer.cs.pebble import programs as P
from explainer.cs.pebble.emu import run as emulate
from explainer.cs.pebble.pipe import Pipeline

TITLE = "Every bubble counted: a sort on the five-stage pipeline"
GOAL = ("Assemble an insertion sort of sixty random words, run it on the instruction emulator and on three pipelines "
        "(no forwarding, forwarding, forwarding with a target buffer and 2-bit counters), and check that each "
        "pipeline's cycles are instructions + 4 + the bubbles it reports. Then count a loop branch's misses under "
        "1-bit and 2-bit counters.")
TASKS = [
    "Sort an array that is already in order (values = sorted(values)). Which bubbles disappear, and which stay?",
    "Replace PR.TwoBit() by PR.GShare() and by PR.Perceptron(). Does either beat the counters on this sort?",
    "Change the loop trace to trips of 3 instead of 10. How do the 1-bit and 2-bit miss counts compare now?",
]

CONFIGS = [
    ("no forwarding, predict not taken", dict(forwarding=False, btb_entries=0, ras_depth=0)),
    ("forwarding, predict not taken", dict(btb_entries=0, ras_depth=0)),
    ("forwarding, BTB and 2-bit counters", dict()),
]


def misses(predictor, trace):
    """Where an online predictor is wrong on a branch trace [(pc, taken), ...]: predict, then update."""
    out = []
    for pc, t in trace:
        out.append(bool(predictor.predict(pc)) != t)
        predictor.update(pc, t)
    return np.array(out)


def pipelines(seed):
    rng = np.random.default_rng(seed)
    values = [int(v) for v in rng.integers(0, 1000, 60)]
    image = assemble(P.insertion_sort(values)).image
    ref = emulate(image, mem_size=8192)  # the emulator: the meaning of the program
    rows = []
    for name, kw in CONFIGS:
        if name.endswith("counters"):
            kw = dict(kw, predictor=PR.TwoBit())
        q = Pipeline(image, mem_size=8192, **kw).run()
        s = q.stats
        data = s["load_use"] + s["raw"]
        control = s["branch_flush"] + s["jump_redirect"] + s["jalr_flush"]
        assert q.regs == ref.regs and bytes(q.mem) == bytes(ref.mem), "the pipeline computes what the emulator does"
        assert q.retired == ref.steps
        assert q.cycles == q.retired + 4 + q.bubbles and q.bubbles == data + control, "every lost cycle is a counted bubble"
        rows.append((name, q, data, control))
    return values, ref, rows


def run(seed=0):
    values, ref, rows = pipelines(seed)
    lab = labs.Lab()
    n = ref.steps
    lab.row("instructions executed (emulator)", f"{n:,}")
    for name, q, data, control in rows:
        lab.row(name, f"{q.cycles:,} cycles = {n:,} + 4 + {data:,} data + {control:,} control   CPI {q.cpi:.3f}")
    cpis = [q.cpi for _, q, _, _ in rows]
    assert cpis[0] > cpis[1] > cpis[2] > 1, "forwarding, then prediction, each lower the CPI; none reaches 1"
    assert rows[1][1].stats["raw"] == 0 and rows[1][1].stats["load_use"] > 0, "forwarding leaves only load-use bubbles"

    # Chapter 7's loop: a branch taken nine times and then not, four times over
    trace = [(0x40, k % 10 != 9) for k in range(40)]
    m1, m2 = misses(PR.OneBit(), trace), misses(PR.TwoBit(), trace)
    lab.row("loop of 10, run 4 times: 1-bit misses", f"{m1.sum()} of 40   (the film: 8)")
    lab.row("loop of 10, run 4 times: 2-bit misses", f"{m2.sum()} of 40   (the film: 5)")
    assert m1.sum() == 8 and m2.sum() == 5
    lab.note = ("Cycles are instructions + 4 + bubbles exactly: forwarding removes the data waits except after a "
                "load, a target buffer with 2-bit counters removes most redirects, and a 2-bit counter misses a "
                "loop once per run where a 1-bit one misses twice.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    names = ["no forwarding", "forwarding", "forwarding,\nBTB + 2-bit"]
    base = np.ones(3)
    data = np.array([d / n for _, _, d, _ in rows])
    control = np.array([c / n for _, _, _, c in rows])
    ax[0].bar(names, base, color=labs.GREY, label="one cycle per instruction")
    ax[0].bar(names, data, bottom=base, color=labs.BLUE, label="data bubbles")
    ax[0].bar(names, control, bottom=base + data, color=labs.RED, label="flushes and redirects")
    for k, c in enumerate(cpis):
        ax[0].text(k, c + 0.03, f"CPI {c:.2f}", ha="center", color=labs.INK)
    ax[0].set(title=f"Insertion sort of {len(values)} words: cycles per instruction", ylabel="cycles per instruction",
              ylim=(0, max(cpis) + 0.45))
    ax[0].legend(loc="upper right")
    ks = np.arange(40)
    ax[1].step(ks, [t for _, t in trace], where="mid", color=labs.GREY, lw=1.2, label="outcome (1 = taken)")
    ax[1].scatter(ks[m1], np.full(m1.sum(), 1.35), color=labs.RED, marker="x", s=40, label=f"1-bit wrong ({m1.sum()})")
    ax[1].scatter(ks[m2], np.full(m2.sum(), 1.2), color=labs.GOLD, marker="o", s=30, label=f"2-bit wrong ({m2.sum()})")
    ax[1].set(title="A ten-trip loop branch, four runs", xlabel="branch execution", yticks=[0, 1], ylim=(-0.15, 2.1))
    ax[1].legend(loc="upper center", ncols=3)
    lab.fig = fig
    return lab
