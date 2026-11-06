"""Spin locks on Part 10's MESI caches: what each design costs in coherence traffic (Part 33).

    r = simulate("tas" | "ttas" | "backoff" | "ticket" | "mcs", cores=8, acquisitions=200)
    r["bus_per_acq"], r["cycles_per_acq"], r["fair"]

Every core runs the same loop: acquire the lock, do a short critical section (``cs`` writes to one shared data line),
release, think for ``think`` cycles, repeat.  Each cycle every core performs at most one memory access, in turn; an
atomic read-modify-write (test-and-set, fetch-and-increment, swap, compare-and-swap) is one write access.  The
caches are :class:`explainer.cs.pebble.coherence.MESI`, which counts the bus transactions: read misses, writes that
must invalidate other copies, and the transfers of Modified lines between caches.

* ``tas``: spin on test-and-set: every attempt is a write, so every waiting core keeps stealing the line.
* ``ttas``: test and test-and-set: spin on an ordinary read (a hit in your own cache), try the tas only when the
  lock looks free; one release still sets off a stampede of misses and tas attempts.
* ``backoff``: ttas, and after a failed tas wait a random time, doubling up to a limit (Anderson 1990).
* ``ticket``: take a ticket with fetch-and-increment; wait until ``now_serving`` equals it: first come, first served,
  but every release invalidates every waiter's copy of ``now_serving``.
* ``mcs``: Mellor-Crummey and Scott (1991): waiters form a linked queue; each spins on a flag in its own cache line,
  and the releaser writes only its successor's flag: O(1) transactions per handoff, whatever the number of cores.
"""

from __future__ import annotations

import random

from explainer.cs.pebble.coherence import MESI

LINE = 64
LOCK, DATA, SERVING, TAIL = 0, 64, 128, 192
NODE0 = 1024          # core i's queue node: its own line


def _node(i):
    return NODE0 + i * LINE


def _core(kind, i, cs, think, rng, mem):
    """One core's loop as a generator of memory operations: ("r", a), ("w", a, v), ("rmw", a, f) -> old,
    ("wait", k), ("acq",), ("rel",)."""
    me = i + 1
    while True:
        if kind == "tas":
            while (yield ("rmw", LOCK, lambda v: 1)) != 0:
                pass
        elif kind in ("ttas", "backoff"):
            delay = 1
            while True:
                while (yield ("r", LOCK)) != 0:
                    pass
                if (yield ("rmw", LOCK, lambda v: 1)) == 0:
                    break
                if kind == "backoff":
                    yield ("wait", rng.randrange(delay) + 1)
                    delay = min(delay * 2, 64)
        elif kind == "ticket":
            t = yield ("rmw", LOCK, lambda v: v + 1)
            while (yield ("r", SERVING)) != t:
                pass
        elif kind == "mcs":
            n = _node(i)
            yield ("w", n, 1)                      # my.locked = 1 (my.next lives in a separate word: memo below)
            mem[("next", me)] = 0
            pred = yield ("rmw", TAIL, lambda v: me)
            if pred:
                mem[("next", pred)] = me
                yield ("w", _node(pred - 1) + 8, me)   # pred.next = me: a write to pred's line
                while (yield ("r", n)) != 0:
                    pass
        yield ("acq",)
        for _ in range(cs):
            yield ("w", DATA, i)
        yield ("rel",)                             # the critical section is over; now hand the lock on
        if kind == "ticket":
            s = yield ("r", SERVING)
            yield ("w", SERVING, s + 1)
        elif kind == "mcs":
            n = _node(i)
            succ = mem.get(("next", me), 0)
            yield ("r", n + 8)
            if not succ:
                if (yield ("rmw", TAIL, lambda v: 0 if v == me else v)) == me:
                    succ = None
                else:
                    while not mem.get(("next", me), 0):
                        yield ("r", n + 8)
                    succ = mem[("next", me)]
            if succ:
                yield ("w", _node(succ - 1), 0)    # successor.locked = 0
        else:
            yield ("w", LOCK, 0)
        if think:
            yield ("wait", think)


def _needs_bus(cache, c, addr, write):
    st = cache.state(c, addr)
    return st == "I" or (write and st == "S")


def simulate(kind: str, cores: int = 8, acquisitions: int = 200, cs: int = 2, think: int = 0, seed: int = 1,
             bus_cycles: int = 8, max_cycles: int = 2_000_000) -> dict:
    """``bus_cycles``: how long one bus transaction occupies the shared interconnect; a core whose access needs the
    bus while it is busy stalls and retries (a hit in its own cache never waits)."""
    rng = random.Random(seed)
    cache = MESI(cores=cores, sets=64, ways=8, line=LINE)
    mem = {}
    gens = [_core(kind, i, cs, think, rng, mem) for i in range(cores)]
    pend = [None] * cores      # the value to send into each generator next
    wait = [0] * cores
    started = [False] * cores
    acq, order, holder = 0, [], None
    cycles = 0
    held = [None] * cores      # an operation that stalled for the bus, to retry
    bus_free = 0
    for cycles in range(1, max_cycles + 1):
        perm = list(range(cores))
        rng.shuffle(perm)              # the bus arbiter: a random order each cycle
        for c in perm:
            if wait[c]:
                wait[c] -= 1
                continue
            g = gens[c]
            while True:                # non-memory events do not take a cycle
                if held[c] is not None:
                    op, held[c] = held[c], None
                    break
                op = g.send(pend[c]) if started[c] else next(g)
                started[c] = True
                pend[c] = None
                if op[0] == "acq":
                    assert holder is None, "two holders"
                    holder = c
                    acq += 1
                    order.append(c)
                    continue
                if op[0] == "rel":
                    holder = None
                    continue
                break
            if op[0] != "wait" and _needs_bus(cache, c, op[1], op[0] != "r"):
                if bus_free > cycles:
                    held[c] = op           # stall: the interconnect is busy
                    continue
                bus_free = cycles + bus_cycles
            if op[0] == "wait":
                wait[c] = op[1] - 1
            elif op[0] == "r":
                cache.access(c, op[1], False)
                pend[c] = mem.get(op[1], 0)
            elif op[0] == "w":
                cache.access(c, op[1], True)
                mem[op[1]] = op[2]
            else:                       # rmw
                cache.access(c, op[1], True)
                old = mem.get(op[1], 0)
                mem[op[1]] = op[2](old)
                pend[c] = old
        if acq >= acquisitions:
            break
    counts = [order.count(c) for c in range(cores)]
    st = cache.stats
    return {"kind": kind, "cores": cores, "acquisitions": acq, "cycles": cycles, "bus": st["bus"],
            "invalidations": st["invalidations"], "bus_per_acq": st["bus"] / max(1, acq),
            "cycles_per_acq": cycles / max(1, acq), "per_core": counts,
            "fair": min(counts) / max(1, max(counts)), "order": order[:40]}
