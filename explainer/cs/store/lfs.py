"""The log-structured file system's cleaner (Part 34), after Rosenblum & Ousterhout's simulator (1992).

The disk is a row of segments.  Every write, new or overwrite, is appended to the current segment; the old copy of
the block becomes dead.  When clean segments run low the **cleaner** reads some segments, writes their live blocks
back out compactly, and frees them.  Cleaning a segment whose live fraction is u costs reading it (1) and writing
u of it back, to gain (1 - u) of free space: per block of new data, the **write cost** is

    (read 1 + write u + write the new 1 - u) / (1 - u) = 2 / (1 - u),

so the cleaner wants nearly empty segments.  **Greedy** cleans the emptiest.  **Cost-benefit** weighs free space
against its stability: benefit / cost = (1 - u) * age / (1 + u), so a cold segment is cleaned at a higher u than a
hot one, whose blocks are still dying on their own.  With hot-and-cold traffic, greedy does worse than with uniform
traffic, and cost-benefit gives the bimodal distribution of segment utilizations the paper found.

    r = simulate(util=0.75, policy="cost-benefit", hot=(0.9, 0.1))
    r["write_cost"], r["cleaned_u"]
"""
from __future__ import annotations

import random


def simulate(util: float = 0.75, policy: str = "greedy", hot: tuple[float, float] | None = None,
             segments: int = 200, seg_blocks: int = 64, writes: float = 20.0, clean_at: int = 4, clean_to: int = 10,
             seed: int = 0) -> dict:
    """``util``: the live fraction of the disk (files / capacity).  ``hot`` = (fraction of writes, fraction of the
    files).  Runs ``writes`` x (number of files) overwrites after filling.  Returns the write cost, and the
    utilizations of the segments as they were cleaned, and of all segments at the end."""
    rng = random.Random(seed)
    nfiles = int(segments * seg_blocks * util)
    where = [-1] * nfiles                  # segment holding each file's live block
    live = [0] * segments
    stamp = [0] * segments                 # youngest modified time in each segment (its "age" is now - stamp)
    members: list[set[int]] = [set() for _ in range(segments)]
    clean = list(range(segments))
    cur = clean.pop(0)
    used = 0                               # blocks written into the current segment
    t = 0
    new = read = rewritten = 0
    cleaned_u = []

    cleaning = False

    def append(f, is_new):
        nonlocal cur, used, new, rewritten
        if used >= seg_blocks:
            cur = clean.pop(0)
            used = 0
        old = where[f]
        if old >= 0:
            live[old] -= 1
            members[old].discard(f)
        where[f] = cur
        live[cur] += 1
        members[cur].add(f)
        stamp[cur] = max(stamp[cur], age_of[f])
        used += 1
        if is_new:
            new += 1
        else:
            rewritten += 1
        if used >= seg_blocks and len(clean) < clean_at and not cleaning:
            cleaner()

    def cleaner():
        nonlocal read, cleaning
        cleaning = True
        while len(clean) < clean_to:
            free = set(clean)
            cands = [s for s in range(segments) if s != cur and s not in free]
            if policy == "greedy":
                v = min(cands, key=lambda s: live[s])
            else:
                def score(s):
                    u = live[s] / seg_blocks
                    return (1 - u) * (t - stamp[s] + 1) / (1 + u)
                v = max(cands, key=score)
            cleaned_u.append(live[v] / seg_blocks)
            if live[v]:
                read += seg_blocks
            movers = sorted(members[v], key=lambda f: age_of[f])          # oldest first, as in the paper
            for f in movers:                  # out of the victim; it is then clean
                where[f] = -1
            members[v] = set()
            live[v] = 0
            stamp[v] = 0
            clean.append(v)
            for f in movers:
                append(f, False)
        cleaning = False

    age_of = [0] * nfiles                  # when each file was last written by the user
    for f in range(nfiles):                # fill
        t += 1
        age_of[f] = t
        append(f, True)
    new = read = rewritten = 0
    cleaned_u.clear()
    hot_n = int(nfiles * hot[1]) if hot else 0
    for _ in range(int(writes * nfiles)):
        t += 1
        if hot and rng.random() < hot[0]:
            f = rng.randrange(hot_n)
        elif hot:
            f = hot_n + rng.randrange(nfiles - hot_n)
        else:
            f = rng.randrange(nfiles)
        age_of[f] = t
        append(f, True)
    wc = (new + read + rewritten) / new
    return {"write_cost": wc, "cleaned_u": cleaned_u, "final_u": [live[s] / seg_blocks for s in range(segments)],
            "util": util, "policy": policy, "hot": hot, "mean_cleaned_u": sum(cleaned_u) / max(1, len(cleaned_u))}


def formula(u: float) -> float:
    """The write cost of cleaning segments at utilization u."""
    return 2 / (1 - u) if u < 1 else float("inf")
