"""Lab 34: crash a small file system at every write, then measure a flash drive's write amplification."""

from videos.coursekit import labs  # noqa: I001  (first, so the library imports without manim)

import numpy as np

from explainer.cs.store import flash
from explainer.cs.store.fs import crash_test

TITLE = "Crash at every write, and what spare flash buys"
GOAL = ("Run append, create, unlink and rename on PebbleFS under four commit modes, crash at every point a disk "
        "could stop, and count the states that fsck or the file's bytes reject. Then simulate a flash translation "
        "layer and compare its write amplification with the estimate (1 + p) / 2p for spare fraction p.")
TASKS = [
    "Add the mode 'data' and compare its writes with 'ordered'. What does journaling the data buy for the cost?",
    "Pass barriers=False to the ordered mode, then also jcsum=True. Which crash states does the checksum rescue?",
    "Call flash.ftl with hot=(0.9, 0.1) and compare r['erase_max'] with r['erase_mean']. What does wear levelling have to fix?",
]
STALE = b"PASSWORD=hunter2 "            # what a deleted file left in the free blocks
OLD, NEW = b"A" * 2000, b"B" * 3000
MODES = ("none", "careful", "writeback", "ordered")
SPARE = (0.07, 0.14, 0.28, 0.5)


def operations():
    """The part's four operations (Chapter 7): (setup, operation, check of the bytes afterwards)."""
    def setup(f):
        f.mkdir("/d")
        f.create("/d/f")
        f.append("/d/f", OLD)

    def torn(c):
        return "garbage" if STALE[:8] in c else "torn"

    def after_append(f):
        c = f.read("/d/f")
        return None if c in (OLD, OLD + NEW) else torn(c)

    def after_create(f):
        if not f.exists("/d/g"):
            return None
        c = f.read("/d/g")
        return None if c in (b"", NEW) else torn(c)

    def after_unlink(f):
        return None if not f.exists("/d/f") or f.read("/d/f") == OLD else "torn"

    def after_rename(f):
        a, b = f.exists("/d/f"), f.exists("/d/h")
        if a == b:
            return "both" if a else "lost"
        return None if f.read("/d/f" if a else "/d/h") == OLD else "torn"

    return [(setup, lambda f: f.append("/d/f", NEW), after_append),
            (setup, lambda f: (f.create("/d/g"), f.append("/d/g", NEW)), after_create),
            (setup, lambda f: f.unlink("/d/f"), after_unlink),
            (setup, lambda f: f.rename("/d/f", "/d/h"), after_rename)]


def run(seed=0):
    lab = labs.Lab()

    # 1. crash consistency (Chapters 7 and 8)
    keys = ("states", "ok", "leak_only", "corrupt", "bad_data", "writes", "flushes")
    crash = {}
    for mode in MODES:
        tot = dict.fromkeys(keys, 0)
        for setup, op, check in operations():
            r = crash_test(setup, op, check, mode=mode, stale=STALE)
            for k in keys:
                tot[k] += r[k]
        crash[mode] = tot
        lab.row(f"{mode}: {tot['states']} crash points", f"corrupt {tot['corrupt']}   wrong bytes {tot['bad_data']}"
                f"   leaks only {tot['leak_only']}   ({tot['writes']} writes, {tot['flushes']} flushes)")
    none, careful, wb, ordered = (crash[m] for m in MODES)
    assert (none["states"], none["corrupt"], none["bad_data"]) == (126, 34, 22), "the film's count with no ordering"
    assert careful["corrupt"] == 0 and careful["bad_data"] == 0 and careful["flushes"] > none["flushes"]
    assert wb["corrupt"] == 0 and wb["bad_data"] > 0, "writeback keeps the structure and loses the bytes"
    assert ordered["ok"] == ordered["states"] == 150, "ordered journaling: every crash state intact"

    # 2. flash: write amplification against over-provisioning (Chapter 3)
    wa = [flash.ftl(blocks=256, pages=64, op=p, writes=3, seed=seed)["wa"] for p in SPARE]
    est = [flash.wa_greedy_estimate(p) for p in SPARE]
    lab.row("write amplification at 7%, 14%, 28%, 50% spare", "  ".join(f"{w:.2f}" for w in wa))
    lab.row("the estimate (1 + p) / 2p", "  ".join(f"{e:.2f}" for e in est) + "   (the film: 7.5 and 2.4 measured)")
    seq = flash.ftl(blocks=256, pages=64, op=0.07, writes=3, seed=seed, pattern="sequential")["wa"]
    lab.row("sequential writes at 7% spare", f"{seq:.2f}   (whole erase blocks die together)")
    assert all(a > b for a, b in zip(wa, wa[1:])), "more spare, less copying"
    assert all(abs(w / e - 1) < 0.15 for w, e in zip(wa, est)), "within 15% of the estimate"
    assert abs(seq - 1) < 0.01
    lab.note = ("With no ordering, a quarter of the crash points corrupt the file system; a journal with ordered "
                "data leaves none. On flash, every host write costs (1 + p) / 2p flash writes, so spare is speed.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    x = np.arange(len(MODES))
    bottom = np.zeros(len(MODES))
    for key, name, c in (("ok", "intact", labs.GREEN), ("corrupt", "fsck finds corruption", labs.RED),
                         ("bad_data", "consistent, wrong bytes", labs.GOLD)):
        h = np.array([crash[m][key] / crash[m]["states"] for m in MODES])
        ax[0].bar(x, h, bottom=bottom, color=c, label=name, width=0.6)
        bottom += h
    ax[0].set_xticks(x, [f"{m}\n{crash[m]['states']} points" for m in MODES])
    ax[0].set(title="Four operations crashed at every point", ylabel="fraction of crash states", ylim=(0, 1.25))
    ax[0].legend(loc="upper center", ncols=3)
    grid = np.linspace(0.05, 0.6, 100)
    ax[1].plot(grid, (1 + grid) / (2 * grid), color=labs.GOLD, label="estimate (1 + p) / 2p")
    ax[1].plot(SPARE, wa, "o", color=labs.BLUE, label="simulated FTL, greedy collector")
    ax[1].plot([0.07], [seq], "s", color=labs.GREEN, label="sequential writes")
    ax[1].set(title="Flash writes per host write", xlabel="over-provisioning p (spare / user capacity)",
              ylabel="write amplification", ylim=(0, 11))
    ax[1].legend()
    lab.fig = fig
    return lab
