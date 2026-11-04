"""Heap allocators on real traces (Part 11): free lists, boundary tags, coalescing, segregated fits, buddies.

    tr = read_mtrace(path)                      # a malloc/free trace recorded with LD_PRELOAD (see Part 11's compute)
    ev = events(tr)                             # ("a", id, size) and ("f", id) in program order
    r = simulate(ev, FirstFit())                # heap high-water mark, peak live bytes, search steps, ...

Every allocator here manages one contiguous heap that grows at the top (like ``sbrk``): a block is a header (8 bytes,
holding the size and an in-use bit, as in Knuth's boundary-tag method) plus a payload rounded up to 16 bytes.  Freed
blocks are coalesced with free neighbours at once.  The policies differ in which free block they choose:

    first fit    the lowest-addressed free block that is big enough (Knuth 2.5, Algorithm A)
    next fit     the same, but the search starts where the last one ended (a "roving pointer")
    best fit     the smallest free block that is big enough
    segregated   size classes (powers of two); first fit within the request's class, then larger classes
    buddy        blocks of power-of-two sizes, split in halves and merged with their "buddy" (Knowlton 1965)

The figure of merit is *fragmentation*: the heap's high-water mark divided by the most bytes ever live at once.
"""

from __future__ import annotations

import bisect
import struct
from dataclasses import dataclass

HEADER = 8
ALIGN = 16


def block_size(n: int) -> int:
    return max(32, (n + HEADER + ALIGN - 1) // ALIGN * ALIGN)


def read_mtrace(path) -> list[tuple]:
    """Records of the tracer: (op, a, b, c) with op in m(alloc) c(calloc) r(realloc) f(free)."""
    data = open(path, "rb").read()
    rec = struct.Struct("<BQQQ")
    return [rec.unpack_from(data, k) for k in range(0, len(data) - rec.size + 1, rec.size)]


def events(tr) -> list[tuple]:
    """The trace as an allocator sees it: ("a", id, size), ("f", id); realloc is a free and an alloc.  Frees of
    pointers the trace never allocated (made before tracing began) are dropped."""
    live: dict[int, int] = {}
    out = []
    nid = 0
    for op, a, b, c in tr:
        op = chr(op)
        if op in "mc":
            if a:
                live[a] = nid
                out.append(("a", nid, b))
                nid += 1
        elif op == "r":
            if c and c in live:
                out.append(("f", live.pop(c)))
            if a:
                live[a] = nid
                out.append(("a", nid, b))
                nid += 1
        elif op == "f":
            if a in live:
                out.append(("f", live.pop(a)))
    return out


# ---------------------------------------------------------------------------
# the free-list allocators: one heap, address-ordered free blocks, immediate coalescing
# ---------------------------------------------------------------------------
class FreeList:
    name = "first fit"

    def __init__(self):
        self.top = 0  # the heap's high-water mark (bytes)
        self.addrs: list[int] = []  # free block addresses, sorted
        self.size: dict[int, int] = {}  # free block address -> size
        self.used: dict[int, int] = {}  # allocated block address -> size
        self.steps = 0

    # choose a free block of at least n bytes, or None
    def choose(self, n: int):
        for i, a in enumerate(self.addrs):
            self.steps += 1
            if self.size[a] >= n:
                return i
        return None

    def malloc(self, n: int) -> int:
        need = block_size(n)
        i = self.choose(need)
        if i is None:
            # extend the heap; a free block at the top is used as the start of the new one
            if self.addrs and self.addrs[-1] + self.size[self.addrs[-1]] == self.top:
                a = self.addrs.pop()
                have = self.size.pop(a)
                self.top += need - have
            else:
                a = self.top
                self.top += need
            self.used[a] = need
            return a
        a = self.addrs[i]
        have = self.size.pop(a)
        if have - need >= 32:  # split: the remainder stays free
            self.addrs[i] = a + need
            self.size[a + need] = have - need
            self.after_split(i)
        else:
            self.addrs.pop(i)
            need = have
            self.after_take(i)
        self.used[a] = need
        return a

    def after_split(self, i):
        pass

    def after_take(self, i):
        pass

    def free(self, a: int) -> None:
        n = self.used.pop(a)
        i = bisect.bisect_left(self.addrs, a)
        # coalesce with the next block, then the previous (the boundary tags make both O(1) in a real heap)
        if i < len(self.addrs) and self.addrs[i] == a + n:
            n += self.size.pop(self.addrs[i])
            self.addrs.pop(i)
        if i > 0 and self.addrs[i - 1] + self.size[self.addrs[i - 1]] == a:
            p = self.addrs[i - 1]
            self.size[p] += n
            return
        self.addrs.insert(i, a)
        self.size[a] = n


class FirstFit(FreeList):
    name = "first fit"


class NextFit(FreeList):
    name = "next fit"

    def __init__(self):
        super().__init__()
        self.rove = 0

    def choose(self, n):
        k = len(self.addrs)
        if not k:
            return None
        start = min(self.rove, k - 1)
        for j in range(k):
            i = (start + j) % k
            self.steps += 1
            if self.size[self.addrs[i]] >= n:
                self.rove = i
                return i
        return None


class BestFit(FreeList):
    name = "best fit"

    def choose(self, n):
        best, bi = None, None
        for i, a in enumerate(self.addrs):
            self.steps += 1
            s = self.size[a]
            if s >= n and (best is None or s < best):
                best, bi = s, i
                if s == n:
                    break
        return bi


class Segregated(FreeList):
    """Size classes by powers of two; a request searches its own class first, then larger ones (first fit inside
    each class, address order).  The steps counted are only those within the classes searched."""

    name = "segregated fits"

    def choose(self, n):
        cls = max(5, (n - 1).bit_length())
        best = None
        for i, a in enumerate(self.addrs):  # simulated: count only the blocks a real segregated list would visit
            s = self.size[a]
            c = max(5, (s - 1).bit_length()) if s > 32 else 5
            if c < cls or s < n:
                continue
            self.steps += 1
            if best is None or c < best[0]:
                best = (c, i)
                if c == cls:
                    break
        return None if best is None else best[1]


class Buddy:
    """The binary buddy system: every block is 2^k bytes (k >= 5), aligned to its size; a free block's buddy is at
    address ^ size, and two free buddies merge into their parent.  The heap grows by doubling its top-level block."""

    name = "buddy"

    def __init__(self):
        self.free: dict[int, set[int]] = {}
        self.used: dict[int, int] = {}
        self.top = 0
        self.steps = 0

    def malloc(self, n: int) -> int:
        k = max(5, (n + HEADER - 1).bit_length())
        j = k
        while j < 48 and not self.free.get(j):
            self.steps += 1
            j += 1
        if j >= 48 or not self.free.get(j):
            # grow: add a fresh block of size 2^k at the top, aligned
            size = 1 << k
            a = (self.top + size - 1) // size * size
            # the gap before it becomes free blocks too (rare)
            self.top = a + size
            self.used[a] = k
            return a
        a = min(self.free[j])
        self.free[j].discard(a)
        while j > k:
            j -= 1
            self.free.setdefault(j, set()).add(a + (1 << j))
        self.used[a] = k
        return a

    def free_(self, a: int) -> None:
        k = self.used.pop(a)
        while True:
            b = a ^ (1 << k)
            if b in self.free.get(k, ()):
                self.free[k].discard(b)
                a = min(a, b)
                k += 1
            else:
                break
        self.free.setdefault(k, set()).add(a)

    def free_block(self, a):
        self.free_(a)


@dataclass
class Result:
    name: str
    peak_live: int  # bytes requested, live at once (the lower bound any allocator faces)
    peak_heap: int  # the heap's high-water mark
    steps: int
    allocs: int
    internal: float  # at the moment of peak live: (block bytes - requested bytes) / requested bytes

    @property
    def fragmentation(self) -> float:
        return self.peak_heap / self.peak_live


def simulate(ev, alloc) -> Result:
    addr: dict[int, int] = {}
    req: dict[int, int] = {}
    live = blocks = 0
    peak = peak_blocks_req = 0
    internal = 0.0
    n = 0
    for e in ev:
        if e[0] == "a":
            _, i, size = e
            a = alloc.malloc(size)
            addr[i] = a
            req[i] = size
            live += size
            n += 1
            if live > peak:
                peak = live
        else:
            _, i = e
            a = addr.pop(i)
            live -= req.pop(i)
            if isinstance(alloc, Buddy):
                alloc.free_(a)
            else:
                alloc.free(a)
    return Result(alloc.name, peak, alloc.top, alloc.steps, n, internal)
