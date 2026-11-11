"""Flash (Part 34): a page-mapped flash translation layer, with garbage collection.

Flash is written a page at a time but erased only a whole block (here 64 pages) at a time, and a page cannot be
rewritten until its block is erased.  So the FTL never overwrites: every write goes to the next free page, the old
copy is marked invalid, and a map from logical to physical pages keeps track.  When free blocks run low, the
**garbage collector** picks a victim block, copies its still-valid pages forward, and erases it.  Those copies are
**write amplification**: flash writes per host write.  Spare capacity, **over-provisioning**, gives the collector
emptier victims.  TRIM tells the FTL that the file system no longer needs some pages, which act as more spare.

    r = ftl(op=0.28, writes=10, policy="greedy")
    r["wa"]          # write amplification in the steady state
"""
from __future__ import annotations

import random


def ftl(blocks: int = 256, pages: int = 64, op: float = 0.28, writes: float = 8.0, policy: str = "greedy",
        hot: tuple[float, float] | None = None, trim: float = 0.0, seed: int = 0, sample: int = 0,
        pattern: str = "random") -> dict:
    """Simulate ``writes`` x (logical capacity) random page writes after the drive is filled once.

    ``op``: over-provisioning, spare / user capacity.  ``policy``: "greedy" (the block with fewest valid pages) or
    "fifo" (the oldest).  ``pattern`` "sequential": the host rewrites its pages in order, as a log or a zoned
    drive's host does (whole erase blocks die together).  ``hot`` = (fraction of writes, fraction of logical pages): skewed traffic.  ``trim``: a
    fraction of logical pages the file system has freed and trimmed (never written again).  Returns the write
    amplification, the erase counts, and (with ``sample``) the free-block count over time."""
    rng = random.Random(seed)
    P = blocks * pages
    L = int(P / (1 + op))
    live_L = int(L * (1 - trim))
    l2p = [-1] * L
    p2l = [-1] * P
    valid = [0] * blocks
    erases = [0] * blocks
    written_at = [0] * blocks
    free = list(range(blocks))
    active = free.pop(0)
    wp = 0
    host = flash = 0
    clock = 0
    trace = []

    is_free = [False] + [True] * (blocks - 1)

    def place(lp):
        nonlocal active, wp, flash
        if wp == pages:
            active = free.pop(0)
            is_free[active] = False
            wp = 0
        pp = active * pages + wp
        wp += 1
        l2p[lp] = pp
        p2l[pp] = lp
        valid[active] += 1
        written_at[active] = clock
        flash += 1

    def invalidate(lp):
        pp = l2p[lp]
        if pp >= 0:
            p2l[pp] = -1
            valid[pp // pages] -= 1
            l2p[lp] = -1

    def gc():
        while len(free) < 2:
            cands = [b for b in range(blocks) if b != active and not is_free[b]]
            if policy == "greedy":
                v = min(cands, key=lambda b: (valid[b], written_at[b]))
            else:
                v = min(cands, key=lambda b: written_at[b])
            for k in range(pages):
                lp = p2l[v * pages + k]
                if lp >= 0:
                    p2l[v * pages + k] = -1
                    valid[v] -= 1
                    l2p[lp] = -1
                    place(lp)
            erases[v] += 1
            free.append(v)
            is_free[v] = True

    def write(lp):
        nonlocal host, clock
        clock += 1
        invalidate(lp)
        place(lp)
        host += 1
        if wp == pages and len(free) < 2:
            gc()
    for lp in range(L):                      # fill the drive once
        write(lp)
    for lp in range(live_L, L):              # TRIM: the file system says these pages are free
        invalidate(lp)
    h0, f0 = host, flash
    e0 = list(erases)
    n = int(writes * L)
    hot_n = int(live_L * hot[1]) if hot else 0
    for i in range(n):
        if pattern == "sequential":
            lp = i % live_L
        elif hot and rng.random() < hot[0]:
            lp = rng.randrange(hot_n)
        elif hot:
            lp = hot_n + rng.randrange(live_L - hot_n)
        else:
            lp = rng.randrange(live_L)
        write(lp)
        if sample and i % sample == 0:
            trace.append((i, (flash - f0) / max(1, host - h0)))
    ed = [a - b for a, b in zip(erases, e0)]
    return {"wa": (flash - f0) / (host - h0), "host": host - h0, "flash": flash - f0, "erases": ed,
            "erase_max": max(ed), "erase_mean": sum(ed) / blocks, "op": op, "policy": policy, "trace": trace,
            "logical": L, "physical": P}


def wa_greedy_estimate(op: float) -> float:
    """A common back-of-the-envelope for greedy collection under uniform random writes: (1 + OP) / (2 OP)."""
    return (1 + op) / (2 * op)
