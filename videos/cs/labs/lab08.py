"""Lab 8: schedule four trips of a table scan on an oracle machine, then run the scan on Pebble's out-of-order core."""

from videos.coursekit import labs

import math

import numpy as np

from explainer.cs.pebble import assemble
from explainer.cs.pebble import predict as PR
from explainer.cs.pebble.emu import run as emulate
from explainer.cs.pebble.limits import LAT, Trace, schedule, trace
from explainer.cs.pebble.ooo import OutOfOrder

TITLE = "The dataflow limit of a table scan"
GOAL = ("Record a scan over a table of word lengths (the shape of the Job's search loop), schedule four of its trips "
        "with 1 to 8 starts a cycle, and compare each schedule with the bound max(ceil(N/W), L). Then run the "
        "whole scan on the functional out-of-order core with a one-entry and a 64-entry issue queue.")
TASKS = [
    "Give loads a latency of 4 (schedule(sub, width=w, latency={'load': 4})). What is the new span L, and at which width is it reached?",
    "Schedule the whole trace with branches='barrier' (no speculation). How far does the IPC fall, and why?",
    "Run the core with width=8 and with rob_size=16. Which of the two changes the cycle count on this scan?",
]

SCAN = """
        la   t0, table
        li   a2, 0
        li   s1, {n}
        li   a1, 99          # a length no entry has: every trip takes the fast path
scan:   beq  a2, s1, done    # end of the table?
        lw   t1, 4(t0)       # this entry's length
        bne  t1, a1, next    # a different length: next entry
        j    done
next:   addi t0, t0, 12
        addi a2, a2, 1
        j    scan
done:   halt
        .align 4
table:
{rows}
"""


def run(seed=0):
    rng = np.random.default_rng(seed)
    n = int(rng.integers(40, 80))
    rows = "\n".join(f"        .word 0, {int(v)}, 0" for v in rng.integers(1, 12, n))
    prog = assemble(SCAN.format(n=n, rows=rows))
    tr = trace(prog.image, mem_size=8192)
    i0 = int(np.flatnonzero(tr.pc == prog.labels["scan"])[10])  # four trips from the middle of the scan
    sub = Trace(*(x[i0:i0 + 24] for x in (tr.pc, tr.kind, tr.srcs, tr.dst, tr.addr, tr.taken, tr.load_value)))
    N, A, L = len(sub), sum(LAT[k] for k in sub.kind), schedule(sub).cycles
    lab = labs.Lab()
    lab.row("four trips: instructions N, work A, span L", f"{N}, {A}, {L}   (the film: 24, 28, 6)")
    assert (N, A, L) == (24, 28, 6)

    widths = list(range(1, 9))
    cycles = [schedule(sub, width=w).cycles for w in widths]
    bounds = [max(math.ceil(N / w), L) for w in widths]
    for w in (1, 2, 4, 8):
        lab.row(f"{w} start{'s' if w > 1 else ''} a cycle", f"{cycles[w - 1]} cycles   (bound {bounds[w - 1]})")
    assert all(c >= b for c, b in zip(cycles, bounds)), "no schedule beats max(ceil(N/W), L)"
    assert [cycles[w - 1] for w in (1, 2, 4, 8)] == [24, 12, 7, 6], "the film's four schedules"
    assert all(a >= b for a, b in zip(cycles, cycles[1:])), "more start slots never hurt"

    free, named = schedule(tr), schedule(tr, rename=False)
    lab.row("whole scan, unlimited width: IPC", f"{free.ipc:.2f} renamed, {named.ipc:.2f} with register names reused")
    assert 5 < free.ipc <= 6 and named.ipc < 0.7 * free.ipc, "one trip a cycle, unless names are reused"

    ref = emulate(prog.image, mem_size=8192)
    cores = {}
    for iq in (1, 64):
        c = OutOfOrder(prog.image, mem_size=8192, iq_size=iq, predictor=PR.Tournament()).run()
        assert c.regs == ref.regs and c.committed == ref.steps, "the core computes what the emulator does"
        cores[iq] = c
    lab.row("functional core, 1-entry issue queue", f"{cores[1].cycles} cycles, IPC {cores[1].ipc:.2f}")
    lab.row("functional core, 64-entry issue queue", f"{cores[64].cycles} cycles, IPC {cores[64].ipc:.2f}")
    assert cores[64].cycles < 0.6 * cores[1].cycles and cores[64].ipc < free.ipc
    lab.note = ("Width helps until the longest dependency chain is reached: 24, 12, 7 and then 6 cycles, the span. "
                "The real core, with a finite front end and in-order retirement, sits between the in-order machine "
                "and the oracle.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    colors = {"load": labs.BLUE, "branch": labs.RED, "alu": labs.GREEN, "jump": labs.GREY}
    s4 = schedule(sub, width=4).start
    seen = set()
    for i in range(N):
        k = sub.kind[i]
        ax[0].barh(i, LAT[k], left=int(s4[i]), color=colors[k], height=0.8, label=None if k in seen else k)
        seen.add(k)
    ax[0].invert_yaxis()
    ax[0].set(title="Four trips, four starts a cycle: 7 cycles", xlabel="cycle", ylabel="instruction, in program order")
    ax[0].legend(loc="upper right")
    ax[1].plot(widths, cycles, "o-", color=labs.GOLD, label="scheduled cycles")
    ax[1].plot(widths, bounds, "--", color=labs.BLUE, label="bound max(ceil(N/W), L)")
    ax[1].axhline(L, color=labs.RED, ls=":", label=f"span L = {L}")
    ax[1].set(title="Cycles against start width", xlabel="starts per cycle W", ylabel="cycles", ylim=(0, 26))
    ax[1].legend()
    lab.fig = fig
    return lab
