"""LSM trees (Part 34): log-structured merge trees (O'Neil, Cheng, Gawlick & O'Neil 1996), against a B-tree.

Writes go to an in-memory **memtable**; when it fills it is written out as a sorted, immutable run (an SSTable).
Runs are merged in the background, by one of two policies, with size ratio T between levels:

* **leveled** (LevelDB, RocksDB's default): each level is one run, T times larger than the one above; a run arriving
  at a full level is merged into it.  Few runs to search; each entry is rewritten about T/2 times per level.
* **tiered** (Cassandra's size-tiered, ScyllaDB): each level collects up to T runs, then merges them into one run on
  the next level.  Each entry is rewritten once per level; reads may search T runs per level.

A lookup checks the memtable and then each run from newest to oldest, one disk read per run (the run's index of
first keys sits in memory), unless the run's **Bloom filter** (Part 20) says the key is absent.  The three
amplifications (write: bytes written per byte inserted; read: disk reads per lookup; space: stored entries per live
key) cannot all be minimal at once: the RUM conjecture (Athanassoulis et al. 2016).

:func:`btree_write_amp` is the comparison: a B-tree updates a leaf in place, and writes the whole page back.
"""
from __future__ import annotations

import random
from collections import OrderedDict

from explainer.cs.algo.randomized import Bloom


class Run:
    __slots__ = ("data", "bloom")

    def __init__(self, data: dict, bits_per_key: float):
        self.data = data
        self.bloom = None
        if bits_per_key and data:
            m = max(8, int(bits_per_key * len(data)))
            k = max(1, round(bits_per_key * 0.6931))
            self.bloom = Bloom(m, k, key=b"lsm")
            for key in data:
                self.bloom.add(key.to_bytes(8, "little"))


class LSM:
    def __init__(self, memtable: int = 1000, ratio: int = 10, policy: str = "leveled", bloom_bits: float = 10.0):
        assert policy in ("leveled", "tiered")
        self.M, self.T, self.policy, self.bits = memtable, ratio, policy, bloom_bits
        self.mem: dict[int, int] = {}
        self.levels: list[list[Run]] = []          # levels[i]: runs, oldest first
        self.inserted = 0
        self.written = 0                           # entries written to disk, flushes and merges
        self.compactions = 0
        self.log: list[tuple[str, int, int]] = []  # ("flush" | "merge", level, entries) for drawing

    def put(self, k: int, v: int) -> None:
        self.mem[k] = v
        self.inserted += 1
        if len(self.mem) >= self.M:
            self.flush()

    def _write(self, data: dict) -> Run:
        self.written += len(data)
        return Run(data, self.bits)

    def flush(self) -> None:
        if not self.mem:
            return
        run = self._write(dict(sorted(self.mem.items())))
        self.log.append(("flush", 0, len(run.data)))
        self.mem = {}
        self._add(0, run)

    def _cap(self, level: int) -> int:
        return self.M * self.T ** (level + 1)

    def _add(self, level: int, run: Run) -> None:
        while len(self.levels) <= level:
            self.levels.append([])
        lv = self.levels[level]
        if self.policy == "tiered":
            lv.append(run)
            if len(lv) >= self.T:
                merged = _merge(lv)
                self.levels[level] = []
                self.compactions += 1
                out = self._write(merged)
                self.log.append(("merge", level + 1, len(out.data)))
                self._add(level + 1, out)
            return
        if lv:                                     # leveled: merge into the level's one run
            merged = _merge(lv + [run])
            self.compactions += 1
            run = self._write(merged)
            self.log.append(("merge", level, len(run.data)))
        self.levels[level] = [run]
        if len(run.data) > self._cap(level):
            self.levels[level] = []
            self._add(level + 1, run)

    def get(self, k: int, stats: dict | None = None):
        if k in self.mem:
            return self.mem[k]
        kb = k.to_bytes(8, "little")
        for lv in self.levels:
            for run in reversed(lv):
                if run.bloom is not None and kb not in run.bloom:
                    continue
                if stats is not None:
                    stats["reads"] = stats.get("reads", 0) + 1
                if k in run.data:
                    return run.data[k]
        return None

    def runs(self) -> int:
        return sum(len(lv) for lv in self.levels)

    def stored(self) -> int:
        return sum(len(r.data) for lv in self.levels for r in lv) + len(self.mem)

    def shape(self) -> list[list[int]]:
        return [[len(r.data) for r in lv] for lv in self.levels]


def _merge(runs: list[Run]) -> dict:
    """Merge runs, oldest first: a newer value of a key replaces an older one."""
    out: dict[int, int] = {}
    for r in runs:
        out.update(r.data)
    return dict(sorted(out.items()))


def workload(policy: str, n: int = 100_000, keys: int = 50_000, memtable: int = 1000, ratio: int = 10,
             bloom_bits: float = 10.0, lookups: int = 5000, seed: int = 0) -> dict:
    """Insert n random keys from [0, keys) (so many are updates), then look up keys that are present and keys that
    are not."""
    rng = random.Random(seed)
    t = LSM(memtable, ratio, policy, bloom_bits)
    for i in range(n):
        t.put(rng.randrange(keys), i)
    present = sorted({k for lv in t.levels for r in lv for k in r.data} | set(t.mem))
    live = len(present)
    hit, miss = {}, {}
    for _ in range(lookups):
        t.get(rng.choice(present), hit)
        t.get(keys + rng.randrange(10 * keys), miss)
    return {"policy": policy, "write_amp": t.written / t.inserted, "read_hit": hit.get("reads", 0) / lookups,
            "read_miss": miss.get("reads", 0) / lookups, "space_amp": t.stored() / live, "runs": t.runs(),
            "levels": t.shape(), "compactions": t.compactions, "live": live, "bloom_bits": bloom_bits}


def btree_write_amp(n: int = 100_000, keys: int = 50_000, record: int = 100, page: int = 4096,
                    cache_pages: int = 64, fill: float = 0.69, seed: int = 0) -> dict:
    """Random updates to a B-tree's leaves, with an LRU buffer pool of ``cache_pages`` pages: each eviction of a dirty
    leaf writes a whole page.  Returns bytes written per byte updated."""
    rng = random.Random(seed)
    per = int(page / record * fill)
    leaves = -(-keys // per)
    pool: OrderedDict[int, bool] = OrderedDict()
    writes = 0
    for _ in range(n):
        p = rng.randrange(keys) // per
        if p in pool:
            pool.move_to_end(p)
        else:
            if len(pool) >= cache_pages:
                _, dirty = pool.popitem(last=False)
                writes += dirty
            pool[p] = False
        pool[p] = True
    writes += sum(pool.values())
    return {"write_amp": writes * page / (n * record), "leaves": leaves, "per_page": per,
            "cache_fraction": cache_pages / leaves}
