"""Page replacement, working sets and kernel allocators (Part 32, chapters 7, 8 and 11).

    faults(trace, frames, "lru")            # also opt, fifo, clock, 2q, arc, lirs, random
    curve(trace, sizes, policy)             # faults for each memory size
    lru_curve(trace, sizes)                 # every LRU size at once, from stack distances (Mattson et al., 1970)
    anomalies(n, pages, frames, rng)        # FIFO reference strings where more frames give more faults
    working_set(trace, tau)                 # Denning's W(t, tau) along the trace
    thrash(...)                             # CPU utilisation against the number of processes sharing memory
    Buddy(order)                            # Knowlton's buddy allocator: split and coalesce
    Slab(obj_size)                          # Bonwick's object caches

A trace is a sequence of page numbers.  ARC follows Megiddo and Modha (2003); LIRS follows Jiang and Zhang (2002)
with the usual 1% of frames for high-inter-reference-recency-resident pages... see the notes; 2Q is Johnson and
Shasha's (1994) full version with A1in at 25% and A1out holding half the frame count of ghost entries.
"""
from __future__ import annotations

import random
from collections import OrderedDict, deque


def faults(trace, frames: int, policy: str, seed: int = 0) -> int:
    if not isinstance(frames, int) or frames < 0:
        raise ValueError("frame count must be a nonnegative integer")
    if policy not in FAULTS:
        raise ValueError("unknown replacement policy: " + str(policy))
    trace = list(trace)
    return len(trace) if frames == 0 else FAULTS[policy](trace, frames, seed)


def _fifo(t, k, seed):
    mem, q, f = set(), deque(), 0
    for p in t:
        if p in mem:
            continue
        f += 1
        if len(mem) == k:
            mem.discard(q.popleft())
        mem.add(p)
        q.append(p)
    return f


def _lru(t, k, seed):
    mem, f = OrderedDict(), 0
    for p in t:
        if p in mem:
            mem.move_to_end(p)
            continue
        f += 1
        if len(mem) == k:
            mem.popitem(last=False)
        mem[p] = 1
    return f


def _random(t, k, seed):
    rng = random.Random(seed)
    mem, lst, f = set(), [], 0
    for p in t:
        if p in mem:
            continue
        f += 1
        if len(mem) == k:
            i = rng.randrange(k)
            mem.discard(lst[i])
            lst[i] = p
        else:
            lst.append(p)
        mem.add(p)
    return f


def _opt(t, k, seed):
    """Belady (1966): evict the page used farthest in the future."""
    n = len(t)
    nxt = [n] * n
    last = {}
    for i in range(n - 1, -1, -1):
        nxt[i] = last.get(t[i], n + 1 + i)
        last[t[i]] = i
    import heapq
    mem = {}                     # page -> next use
    heap = []
    f = 0
    for i, p in enumerate(t):
        if p in mem:
            mem[p] = nxt[i]
            heapq.heappush(heap, (-nxt[i], p))
            continue
        f += 1
        if len(mem) == k:
            while True:
                nu, q = heapq.heappop(heap)
                if q in mem and mem[q] == -nu:
                    del mem[q]
                    break
        mem[p] = nxt[i]
        heapq.heappush(heap, (-nxt[i], p))
    return f


def _clock(t, k, seed, trace_hand=None):
    """Second chance: a hand sweeps the frames, clearing reference bits, and evicts the first page found clear."""
    frames = [None] * k
    ref = [0] * k
    where = {}
    hand = f = 0
    for p in t:
        if p in where:
            ref[where[p]] = 1
            continue
        f += 1
        while True:
            if frames[hand] is None or not ref[hand]:
                break
            ref[hand] = 0
            hand = (hand + 1) % k
        if frames[hand] is not None:
            del where[frames[hand]]
        frames[hand] = p
        where[p] = hand
        ref[hand] = 1
        if trace_hand is not None:
            trace_hand.append((hand, list(frames), list(ref)))
        hand = (hand + 1) % k
    return f


def _2q(t, k, seed):
    kin = max(1, k // 4)
    kout = max(1, k // 2)
    am, a1in, a1out = OrderedDict(), OrderedDict(), OrderedDict()
    f = 0
    for p in t:
        if p in am:
            am.move_to_end(p)
            continue
        if p in a1in:
            continue
        f += 1
        if len(am) + len(a1in) >= k:
            if len(a1in) > kin or not am:
                q, _ = a1in.popitem(last=False)
                a1out[q] = 1
                if len(a1out) > kout:
                    a1out.popitem(last=False)
            else:
                am.popitem(last=False)
        if p in a1out:
            del a1out[p]
            am[p] = 1
        else:
            a1in[p] = 1
    return f


def _arc(t, c, seed):
    """Adaptive replacement cache (Megiddo and Modha, 2003): T1 recent, T2 frequent, ghosts B1, B2 steer p."""
    T1, T2, B1, B2 = OrderedDict(), OrderedDict(), OrderedDict(), OrderedDict()
    p_ = 0.0
    f = 0

    def replace(x):
        if T1 and (len(T1) > p_ or (x in B2 and len(T1) == p_)):
            y, _ = T1.popitem(last=False)
            B1[y] = 1
        else:
            y, _ = T2.popitem(last=False)
            B2[y] = 1
    for x in t:
        if x in T1:
            del T1[x]
            T2[x] = 1
            continue
        if x in T2:
            T2.move_to_end(x)
            continue
        f += 1
        if x in B1:
            p_ = min(c, p_ + max(len(B2) / max(len(B1), 1), 1))
            replace(x)
            del B1[x]
            T2[x] = 1
            continue
        if x in B2:
            p_ = max(0, p_ - max(len(B1) / max(len(B2), 1), 1))
            replace(x)
            del B2[x]
            T2[x] = 1
            continue
        if len(T1) + len(B1) == c:
            if len(T1) < c:
                B1.popitem(last=False)
                replace(x)
            else:
                T1.popitem(last=False)
        elif len(T1) + len(B1) < c and len(T1) + len(T2) + len(B1) + len(B2) >= c:
            if len(T1) + len(T2) + len(B1) + len(B2) == 2 * c:
                B2.popitem(last=False)
            replace(x)
        T1[x] = 1
    return f


def _lirs(t, k, seed):
    """LIRS (Jiang and Zhang, 2002): pages with low inter-reference recency (LIR) stay; a small HIR resident set
    (1% of the frames, at least 1) takes the rest.  The stack S holds recency; Q the resident HIR pages."""
    lhir = max(1, k // 100)
    llir = k - lhir
    S = OrderedDict()            # page -> is_lir (most recent at the end)
    Q = OrderedDict()            # resident HIR pages
    lir = set()
    resident = set()
    f = 0

    def prune():
        while S:
            bottom = next(iter(S))
            if bottom in lir:
                break
            del S[bottom]
    for x in t:
        if x in lir:
            S.pop(x, None)
            S[x] = True
            prune()
            continue
        if x in resident:            # a resident HIR page
            if x in S:               # its recency beats the bottom LIR page: promote it
                S.pop(x)
                S[x] = True
                lir.add(x)
                Q.pop(x, None)
                b = next(iter(S))
                lir.discard(b)
                S.pop(b)
                Q[b] = 1
                prune()
            else:
                S[x] = False
                Q.pop(x)
                Q[x] = 1
            continue
        f += 1
        if len(lir) < llir:
            lir.add(x)
            resident.add(x)
            S.pop(x, None)
            S[x] = True
            continue
        if len(Q) >= lhir:
            v, _ = Q.popitem(last=False)
            resident.discard(v)
        resident.add(x)
        if x in S:                   # a non-resident HIR page still in the stack: it becomes LIR
            S.pop(x)
            S[x] = True
            lir.add(x)
            b = next(iter(S))
            lir.discard(b)
            S.pop(b)
            Q[b] = 1
            prune()
        else:
            S[x] = False
            Q[x] = 1
        if len(S) > 4 * k:           # bound the ghost history
            for key in list(S)[: len(S) - 4 * k]:
                if key not in lir:
                    S.pop(key)
    return f


FAULTS = {"fifo": _fifo, "lru": _lru, "opt": _opt, "clock": _clock, "2q": _2q, "arc": _arc, "lirs": _lirs,
          "random": _random}


def curve(trace, sizes, policy):
    return [faults(trace, k, policy) for k in sizes]


def stack_distances(trace):
    """Mattson's stack algorithm: the LRU stack depth of every reference (inf for a first touch)."""
    stack = []
    out = []
    for p in trace:
        if p in stack:
            d = len(stack) - stack.index(p)
            stack.remove(p)
            out.append(d)
        else:
            out.append(None)
        stack.append(p)
    return out


def lru_curve(trace, sizes):
    """LRU faults at every size from one pass: a reference faults with k frames iff its stack distance > k.  This is
    the inclusion property, which also rules out Belady's anomaly for LRU."""
    ds = stack_distances(trace)
    return [sum(1 for d in ds if d is None or d > k) for k in sizes]


def anomalies(n: int, pages: int, frames: int, rng: random.Random, trials: int = 2000):
    """Random reference strings of length n over `pages` pages for which FIFO with frames+1 faults more than with
    frames.  Returns (string, faults at frames, faults at frames+1) for each found."""
    out = []
    for _ in range(trials):
        s = [rng.randrange(pages) for _ in range(n)]
        a, b = _fifo(s, frames, 0), _fifo(s, frames + 1, 0)
        if b > a:
            out.append((s, a, b))
    return out


def working_set(trace, tau: int) -> list[int]:
    """|W(t, tau)|: distinct pages among the last tau references, at every t."""
    out, counts, win = [], {}, deque()
    for p in trace:
        win.append(p)
        counts[p] = counts.get(p, 0) + 1
        if len(win) > tau:
            q = win.popleft()
            counts[q] -= 1
            if not counts[q]:
                del counts[q]
        out.append(len(counts))
    return out


def thrash(nprocs: int, frames: int, wset: int, refs: int = 20000, fault_time: int = 200, seed: int = 1,
           io_every: int = 60, io_time: int = 180) -> float:
    """CPU utilisation with nprocs processes sharing `frames` frames under global LRU.  Each process cycles through
    its own working set of `wset` pages (with some randomness), and every `io_every` references waits `io_time` for
    ordinary I/O (which more processes can overlap).  A page fault blocks it for `fault_time` while the one paging disk
    works, and faults queue for that disk.  The CPU runs whichever process is ready.  Returns busy / elapsed."""
    rng = random.Random(seed)
    mem = OrderedDict()
    ready_at = [0] * nprocs
    pos = [0] * nprocs
    t = busy = done = 0
    disk_free = 0
    while done < refs:
        runnable = [i for i in range(nprocs) if ready_at[i] <= t]
        if not runnable:
            t = min(ready_at)
            continue
        i = runnable[t % len(runnable)]
        page = (i, (pos[i] + (rng.randrange(3) == 0) * rng.randrange(wset)) % wset)
        pos[i] += 1
        if page in mem:
            mem.move_to_end(page)
            t += 1
            busy += 1
            done += 1
            if pos[i] % io_every == 0:
                ready_at[i] = t + io_time
        else:
            if len(mem) >= frames:
                mem.popitem(last=False)
            mem[page] = 1
            start = max(t, disk_free)           # one disk: faults queue
            disk_free = start + fault_time
            ready_at[i] = disk_free
            t += 1
    return busy / t


class Buddy:
    """Knowlton (1965): blocks of 2^k pages; split the smallest big-enough block in halves, and on free merge with the
    buddy (the block whose address differs in bit k) whenever it is free too."""

    def __init__(self, order: int):
        if not isinstance(order, int) or order < 0:
            raise ValueError("buddy order must be a nonnegative integer")
        self.order = order
        self.free = {k: set() for k in range(order + 1)}
        self.free[order].add(0)
        self.alloc = {}
        self.splits = self.merges = 0

    def malloc(self, pages: int):
        if not isinstance(pages, int) or pages < 1:
            raise ValueError("allocation size must be a positive number of pages")
        k = max(0, (pages - 1).bit_length())
        j = k
        while j <= self.order and not self.free[j]:
            j += 1
        if j > self.order:
            return None
        a = min(self.free[j])
        self.free[j].discard(a)
        while j > k:
            j -= 1
            self.free[j].add(a + (1 << j))
            self.splits += 1
        self.alloc[a] = k
        return a

    def release(self, a: int):
        k = self.alloc.pop(a)
        while k < self.order:
            b = a ^ (1 << k)
            if b not in self.free[k]:
                break
            self.free[k].discard(b)
            a = min(a, b)
            k += 1
            self.merges += 1
        self.free[k].add(a)

    def free_pages(self):
        return sum(len(v) << k for k, v in self.free.items())

    def largest_free(self):
        return max([1 << k for k, v in self.free.items() if v], default=0)


class Slab:
    """Occupancy model of Bonwick's slab caches: alloc returns a slab index, not an object address.

    Counts slots in one-page slabs; it does not store object bytes or run constructors.
    """

    def __init__(self, obj_size: int, page: int = 4096):
        if not isinstance(obj_size, int) or not isinstance(page, int) or not 1 <= obj_size <= page:
            raise ValueError("object size must be positive and fit in a positive page")
        self.per = page // obj_size
        self.slabs = []          # [free count]
        self.objs = {}

    def alloc(self):
        for i, s in enumerate(self.slabs):
            if s:
                self.slabs[i] -= 1
                return i
        self.slabs.append(self.per - 1)
        return len(self.slabs) - 1

    def release(self, slab: int):
        if not isinstance(slab, int) or not 0 <= slab < len(self.slabs) or self.slabs[slab] >= self.per:
            raise ValueError("no allocated slot to release in that slab")
        self.slabs[slab] += 1
