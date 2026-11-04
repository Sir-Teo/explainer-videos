"""Caches for Pebble (Part 9): set-associative caches, a hierarchy, and the analyses of a memory trace.

    c = SetAssoc(32 * 1024, line=64, ways=8)              # a 32 KB, 8-way, LRU, write-back, write-allocate cache
    c.access(addr, write=False)                           # True on a hit
    h = Hierarchy([SetAssoc(32 << 10, hit=4, name="L1"), SetAssoc(256 << 10, hit=12, name="L2")], dram=200)
    h.access(addr)                                        # the latency of this access, in cycles

    t = memtrace(image, tape)                             # every data access of a run: byte address, size, store?
    d = stack_distances(t.addr // 64)                     # LRU stack distance of each access (Mattson et al. 1970)
    miss_curve(d, [64, 512, 4096])                        # the miss ratio of a fully associative LRU cache, any size
    three_c(t.addr // 64, sets=64, ways=8)                # compulsory, capacity and conflict misses (Hill 1987)
    belady(t.addr // 64, capacity=512)                    # misses of the optimal replacement policy (Belady 1966)

A hierarchy is also what the out-of-order core of Part 8 accepts as its ``cache`` (``access``, ``present``,
``flush``, ``flush_line``), so the same core can run with realistic memory.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

import numpy as np

from .emu import Machine
from .isa import IO_BASE, decode
from .pipe import LOADS, STORES


class SetAssoc:
    """A set-associative cache of ``size`` bytes in lines of ``line`` bytes, ``ways`` lines per set.

    ``policy``: "lru", "plru" (tree pseudo-LRU, as most hardware does), "fifo" or "random".
    ``write``: "back" (dirty lines are written when evicted) or "through" (every store goes on to the next level).
    ``allocate``: whether a store miss brings the line in (write-allocate).
    ``hit``: this level's latency in cycles, used by ``Hierarchy``."""

    def __init__(self, size: int, line: int = 64, ways: int = 8, policy: str = "lru", write: str = "back",
                 allocate: bool = True, hit: int = 4, name: str = "cache", seed: int = 1):
        assert size % (line * ways) == 0
        self.size, self.line, self.ways, self.policy = size, line, ways, policy
        self.write, self.allocate, self.hit, self.name = write, allocate, hit, name
        self.sets = size // (line * ways)
        self.rng = random.Random(seed)
        self.flush()

    def flush(self):
        self.tags = [[] for _ in range(self.sets)]  # per set: line numbers, most recently used last (LRU, FIFO)
        self.dirty = [set() for _ in range(self.sets)]
        self.plru = [0] * self.sets  # tree bits per set (ways - 1 of them, packed)
        self.ways_of = [dict() for _ in range(self.sets)]  # line -> way (for PLRU)
        self.accesses = self.misses = self.writebacks = self.write_throughs = 0

    def _set(self, ln: int) -> int:
        return ln % self.sets

    def present(self, addr: int) -> bool:
        ln = addr // self.line
        return ln in self.ways_of[self._set(ln)] if self.policy == "plru" else ln in self.tags[self._set(ln)]

    def flush_line(self, addr: int):
        ln = addr // self.line
        s = self._set(ln)
        if self.policy == "plru":
            self.ways_of[s].pop(ln, None)
        elif ln in self.tags[s]:
            self.tags[s].remove(ln)
        self.dirty[s].discard(ln)

    # -- tree pseudo-LRU: ways - 1 bits; each internal node points to the half that was used less recently -------
    def _plru_touch(self, s: int, way: int):
        bits, node, lo, hi = self.plru[s], 0, 0, self.ways
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if way < mid:
                bits |= 1 << node  # used the left half: point right
                node, hi = 2 * node + 1, mid
            else:
                bits &= ~(1 << node)
                node, lo = 2 * node + 2, mid
        self.plru[s] = bits

    def _plru_victim(self, s: int) -> int:
        bits, node, lo, hi = self.plru[s], 0, 0, self.ways
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if bits >> node & 1:
                node, lo = 2 * node + 2, mid
            else:
                node, hi = 2 * node + 1, mid
        return lo

    def access(self, addr: int, write: bool = False) -> bool:
        """Look up ``addr``; on a miss, bring the line in (unless it is a store and the cache does not allocate).
        Returns True on a hit.  ``self.evicted`` is the line pushed out by this access (or None)."""
        self.accesses += 1
        ln = addr // self.line
        s = self._set(ln)
        self.evicted = None
        if write and self.write == "through":
            self.write_throughs += 1
        if self.policy == "plru":
            ways = self.ways_of[s]
            if ln in ways:
                self._plru_touch(s, ways[ln])
                if write and self.write == "back":
                    self.dirty[s].add(ln)
                return True
            self.misses += 1
            if write and not self.allocate:
                return False
            if len(ways) < self.ways:
                way = len(ways)
            else:
                way = self._plru_victim(s)
                old = next(k for k, v in ways.items() if v == way)
                del ways[old]
                self._evict(s, old)
            ways[ln] = way
            self._plru_touch(s, way)
        else:
            tags = self.tags[s]
            if ln in tags:
                if self.policy == "lru":
                    tags.remove(ln)
                    tags.append(ln)
                if write and self.write == "back":
                    self.dirty[s].add(ln)
                return True
            self.misses += 1
            if write and not self.allocate:
                return False
            if len(tags) >= self.ways:
                k = self.rng.randrange(len(tags)) if self.policy == "random" else 0
                self._evict(s, tags.pop(k))
            tags.append(ln)
        if write and self.write == "back":
            self.dirty[s].add(ln)
        return False

    def _evict(self, s: int, ln: int):
        self.evicted = ln
        if ln in self.dirty[s]:
            self.dirty[s].discard(ln)
            self.writebacks += 1

    @property
    def miss_rate(self) -> float:
        return self.misses / max(self.accesses, 1)


class Hierarchy:
    """Levels of cache in front of DRAM.  ``access`` returns the latency: each level's hit time down to the level
    that has the line, plus ``dram`` cycles if none does; every level the access missed in is filled (inclusive).
    ``prefetch="next"`` brings the following line into the last level on every miss there; ``"stride"`` detects a
    constant stride per access stream (here: per 4 KB page) and fetches ``degree`` lines ahead into every level."""

    def __init__(self, levels: list, dram: int = 200, prefetch: str | None = None, degree: int = 2):
        self.levels, self.dram, self.prefetch, self.degree = levels, dram, prefetch, degree
        self.dram_accesses = 0
        self.prefetches = 0
        self._last: dict[int, tuple[int, int]] = {}  # page -> (last line, stride)

    @property
    def line(self) -> int:
        return self.levels[0].line

    def access(self, addr: int, write: bool = False) -> int:
        lat = 0
        for lv in self.levels:
            lat += lv.hit
            if lv.access(addr, write):
                break
        else:
            lat += self.dram
            self.dram_accesses += 1
        if self.prefetch:
            self._prefetch(addr)
        return lat

    def _prefetch(self, addr: int):
        ln = addr // self.line
        if self.prefetch == "next":
            nxt = [ln + 1]
        else:
            page = addr >> 12
            last, stride = self._last.get(page, (None, 0))
            nxt = []
            if last is not None:
                d = ln - last
                if d != 0 and d == stride:
                    nxt = [ln + d * k for k in range(1, self.degree + 1)]
                if d != 0:
                    stride = d
            self._last[page] = (ln, stride)
        for n in nxt:
            a = n * self.line
            if not self.levels[0].present(a):
                self.prefetches += 1
                for lv in self.levels:
                    if not lv.present(a):
                        lv.access(a)
                        lv.accesses -= 1  # a prefetch is not a demand access
                        lv.misses -= 1

    # the interface of ooo.Cache
    def present(self, addr: int) -> bool:
        return self.levels[0].present(addr)

    def flush(self):
        for lv in self.levels:
            lv.flush()

    def flush_line(self, addr: int):
        for lv in self.levels:
            lv.flush_line(addr)


# ---------------------------------------------------------------------------
# traces
# ---------------------------------------------------------------------------
@dataclass
class MemTrace:
    addr: np.ndarray  # byte address of each data access
    size: np.ndarray  # 1 or 4
    store: np.ndarray  # bool
    pc: np.ndarray  # the instruction that made it
    step: np.ndarray  # the instruction count at which it happened
    instructions: int

    def __len__(self):
        return len(self.addr)


def memtrace(image: bytes, tape: bytes = b"", mem_size: int = 1 << 20, max_steps: int = 50_000_000) -> MemTrace:
    """Every load and store a run makes to memory (device accesses left out), in order."""
    m = Machine(image, tape=tape, mem_size=mem_size)
    addr, size, store, pcs, steps = [], [], [], [], []
    dec: dict[int, object] = {}
    while not m.halted and m.steps < max_steps:
        pc = m.pc
        ins = dec.get(pc)
        if ins is None:
            ins = decode(m.word(pc))
            dec[pc] = ins
        if ins.op in LOADS or ins.op in STORES:
            a = (m.regs[ins.rs1] + ins.imm) & 0xFFFF_FFFF
            if a < IO_BASE:
                addr.append(a)
                size.append(4 if ins.op in ("lw", "sw") else 1)
                store.append(ins.op in STORES)
                pcs.append(pc)
                steps.append(m.steps)
            if ins.op in STORES:
                dec.pop(a & ~3, None)
        m.step()
    return MemTrace(np.array(addr, np.int64), np.array(size, np.int8), np.array(store, bool),
                    np.array(pcs, np.int64), np.array(steps, np.int64), m.steps)


# ---------------------------------------------------------------------------
# analyses
# ---------------------------------------------------------------------------
def stack_distances(lines) -> np.ndarray:
    """The LRU stack distance of every access (Mattson, Gecsei, Slutz and Traiger, 1970): how many distinct lines
    were touched since this line's previous access (0 if it is the most recent), or -1 for a first touch.  A fully
    associative LRU cache of C lines hits exactly the accesses with 0 <= distance < C.  O(n log n), with a Fenwick
    tree over the times of each line's latest access."""
    lines = np.asarray(lines)
    n = len(lines)
    tree = np.zeros(n + 1, np.int64)

    def add(i, v):
        i += 1
        while i <= n:
            tree[i] += v
            i += i & -i

    def prefix(i):  # sum over [0, i)
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & -i
        return s

    last: dict[int, int] = {}
    out = np.empty(n, np.int64)
    total = 0
    for t in range(n):
        ln = int(lines[t])
        p = last.get(ln)
        if p is None:
            out[t] = -1
        else:
            out[t] = total - prefix(p + 1)  # distinct lines whose latest access is after p
            add(p, -1)
            total -= 1
        add(t, 1)
        total += 1
        last[ln] = t
    return out


def miss_curve(distances: np.ndarray, capacities) -> list[float]:
    """Miss ratio of a fully associative LRU cache of each capacity (in lines), from the stack distances."""
    d = np.asarray(distances)
    n = len(d)
    out = []
    for c in capacities:
        hits = int(((d >= 0) & (d < c)).sum())
        out.append(1 - hits / max(n, 1))
    return out


def belady(lines, capacity: int) -> int:
    """Misses of Belady's optimal policy (1966) in a fully associative cache of ``capacity`` lines: on a miss with
    the cache full, evict the line whose next use is furthest in the future."""
    import heapq

    lines = [int(x) for x in lines]
    n = len(lines)
    nxt = [n] * n
    seen: dict[int, int] = {}
    for t in range(n - 1, -1, -1):
        nxt[t] = seen.get(lines[t], n + t + 1)  # never again: further than anything
        seen[lines[t]] = t
    cache: dict[int, int] = {}  # line -> its next use
    heap: list[tuple[int, int]] = []  # (-next use, line), lazily invalidated
    misses = 0
    for t, ln in enumerate(lines):
        if ln in cache:
            cache[ln] = nxt[t]
            heapq.heappush(heap, (-nxt[t], ln))
            continue
        misses += 1
        if len(cache) >= capacity:
            while True:
                negu, victim = heapq.heappop(heap)
                if victim in cache and cache[victim] == -negu:
                    del cache[victim]
                    break
        cache[ln] = nxt[t]
        heapq.heappush(heap, (-nxt[t], ln))
    return misses


def three_c(lines, sets: int, ways: int) -> dict:
    """Hill's classification of the misses of a ``sets`` x ``ways`` LRU cache: compulsory (first touch of a
    line), capacity (also missed by a fully associative LRU cache of the same size), conflict (the rest)."""
    lines = np.asarray(lines)
    d = stack_distances(lines)
    cap = sets * ways
    full_miss = (d < 0) | (d >= cap)
    c = SetAssoc(sets * ways * 64, line=64, ways=ways)
    miss = np.zeros(len(lines), bool)
    for i, ln in enumerate(lines):
        miss[i] = not c.access(int(ln) * 64)
    compulsory = int((d < 0).sum())
    capacity = int((full_miss & (d >= 0)).sum())
    total = int(miss.sum())
    return {"accesses": len(lines), "misses": total, "compulsory": compulsory, "capacity": capacity,
            "conflict": total - compulsory - capacity}
