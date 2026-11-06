"""The partitioned log (Part 46): topics split into partitions, each an append-only sequence of segments with
offsets; keys hashed to partitions so that order holds per key; consumer groups that divide partitions among their
members and rebalance when one joins or leaves; retention by time and log compaction by key."""

from __future__ import annotations

import zlib
from collections import defaultdict


def partition_of(key: str, n: int) -> int:
    return zlib.crc32(key.encode()) % n


class Topic:
    def __init__(self, partitions=4, segment_size=100):
        self.parts = [[] for _ in range(partitions)]   # list of (offset, key, value, time)
        self.segment_size = segment_size

    def append(self, key, value, t):
        p = partition_of(key, len(self.parts))
        off = len(self.parts[p])
        self.parts[p].append((off, key, value, t))
        return p, off

    def segments(self, p):
        log = self.parts[p]
        return [log[i:i + self.segment_size] for i in range(0, len(log), self.segment_size)]

    def compact(self, p):
        """Keep only the last value for each key (a changelog compacted into a snapshot), preserving offsets."""
        last = {}
        for off, k, v, t in self.parts[p]:
            last[k] = off
        return [r for r in self.parts[p] if last[r[1]] == r[0]]

    def retain(self, p, now, keep):
        """Delete whole segments older than keep (time-based retention): returns the first offset still kept."""
        kept = [s for s in self.segments(p) if s and s[-1][3] >= now - keep]
        return kept[0][0][0] if kept else len(self.parts[p])


def assign(partitions: int, members: list):
    """Range assignment: partitions divided into contiguous runs among the sorted members."""
    ms = sorted(members)
    out = {m: [] for m in ms}
    per, extra = divmod(partitions, len(ms))
    p = 0
    for i, m in enumerate(ms):
        k = per + (1 if i < extra else 0)
        out[m] = list(range(p, p + k))
        p += k
    return out


def sticky(prev: dict, partitions: int, members: list):
    """A sticky rebalance: members keep what they had where they can, and only orphaned or excess partitions move."""
    ms = sorted(members)
    target = {m: partitions // len(ms) + (1 if i < partitions % len(ms) else 0) for i, m in enumerate(ms)}
    out = {m: [p for p in prev.get(m, [])][:target[m]] for m in ms}
    taken = {p for v in out.values() for p in v}
    free = [p for p in range(partitions) if p not in taken]
    for m in ms:
        while len(out[m]) < target[m]:
            out[m].append(free.pop(0))
    return out


def moved(a: dict, b: dict):
    owner_a = {p: m for m, ps in a.items() for p in ps}
    owner_b = {p: m for m, ps in b.items() for p in ps}
    return sum(1 for p in owner_b if owner_a.get(p) != owner_b[p])


def rebalance_demo(partitions=12):
    a = assign(partitions, ["c1", "c2", "c3"])
    b_range = assign(partitions, ["c1", "c2", "c3", "c4"])
    b_sticky = sticky(a, partitions, ["c1", "c2", "c3", "c4"])
    c_range = assign(partitions, ["c1", "c3", "c4"])
    c_sticky = sticky(b_sticky, partitions, ["c1", "c3", "c4"])
    return {"three": a, "join_range": b_range, "join_sticky": b_sticky, "moved_range": moved(a, b_range),
            "moved_sticky": moved(a, b_sticky), "leave_range": c_range, "leave_sticky": c_sticky,
            "moved_leave_range": moved(b_range, c_range), "moved_leave_sticky": moved(b_sticky, c_sticky)}


def ordering_demo(words, partitions=4):
    """Per-key order: events for one key keep their order because they land in one partition; across keys a
    consumer of several partitions sees an interleaving that depends on timing."""
    t = Topic(partitions)
    for i, w in enumerate(words):
        t.append(w, i, i)
    by_part = defaultdict(list)
    for p, log in enumerate(t.parts):
        for off, k, v, _ in log:
            by_part[p].append((k, v))
    per_key_sorted = all(
        [v for k2, v in by_part[partition_of(k, partitions)] if k2 == k] == sorted(
            v for k2, v in by_part[partition_of(k, partitions)] if k2 == k) for k in set(words))
    return {"partitions": {p: v for p, v in by_part.items()}, "per_key_in_order": per_key_sorted}


def compaction_demo(n_events=2000, keys=50, seed=0):
    import random
    rng = random.Random(seed)
    t = Topic(1, segment_size=200)
    state = {}
    for i in range(n_events):
        k = f"user{rng.randrange(keys)}"
        v = rng.randrange(1000)
        t.append(k, v, i)
        state[k] = v
    c = t.compact(0)
    rebuilt = {k: v for _, k, v, _ in c}
    return {"events": n_events, "after_compaction": len(c), "keys": len(state), "same_state": rebuilt == state}
