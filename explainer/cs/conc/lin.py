"""Linearizability (Herlihy and Wing 1990), checked (Part 33).

    h = [Op(thread, "enq", 1, None, start, end), Op(thread, "deq", None, 1, start, end), ...]
    check(h, "queue")        # a linearization (the order of operations), or None if there is none

A concurrent history is linearizable if each operation can be given a single instant between its invocation and its
response, so that the operations, in the order of those instants, are a legal run of the sequential object.  The
checker is Wing and Gong's search (1993) with Lowe's memoisation (2017): repeatedly pick an operation that no
remaining operation finished before (it may be linearized next), apply it to the sequential specification, and
backtrack when its result disagrees; a (remaining set, object state) pair seen before is not explored again.  In the
worst case this is exponential, and the problem is NP-complete (Gibbons and Korach 1997).

Specifications: ``register`` (write v / read -> v), ``queue`` (enq v / deq -> v or None), ``stack`` (push v / pop ->
v or None), ``counter`` (inc -> the old value).
"""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Op:
    thread: int
    kind: str
    arg: object
    ret: object
    start: float
    end: float


def apply(spec: str, state, op: Op):
    """(ok, new state) for one operation on the sequential object."""
    if spec == "register":
        if op.kind == "write":
            return True, op.arg
        return op.ret == state, state
    if spec == "counter":
        return op.ret == state, state + 1
    if spec in ("queue", "stack"):
        if op.kind in ("enq", "push"):
            return True, state + (op.arg,)
        if not state:
            return op.ret is None, state
        if spec == "queue":
            return op.ret == state[0], state[1:]
        return op.ret == state[-1], state[:-1]
    raise ValueError(spec)


INIT = {"register": 0, "counter": 0, "queue": (), "stack": ()}


class TooHard(Exception):
    pass


def check(history: list[Op], spec: str, stats: dict | None = None, limit: int | None = None):
    """A linearization (list of indices into ``history``) or None.  ``limit``: give up (raise TooHard) after that many
    search steps."""
    n = len(history)
    seen = set()
    order = []
    calls = [0]

    def go(remaining: frozenset, state):
        calls[0] += 1
        if limit is not None and calls[0] > limit:
            raise TooHard
        if not remaining:
            return True
        key = (remaining, state)
        if key in seen:
            return False
        seen.add(key)
        first_end = min(history[i].end for i in remaining)
        for i in sorted(remaining, key=lambda i: history[i].start):
            op = history[i]
            if op.start > first_end:
                break                      # some remaining op finished before this one began
            ok, st = apply(spec, state, op)
            if ok:
                order.append(i)
                if go(remaining - {i}, st):
                    return True
                order.pop()
        return False
    found = go(frozenset(range(n)), INIT[spec])
    if stats is not None:
        stats["calls"] = calls[0]
    return list(order) if found else None


def random_history(spec: str, threads: int, ops: int, rng: random.Random, bug: float = 0.0) -> list[Op]:
    """Operations on a correct atomic object, each taking effect at a random instant inside its own random interval;
    with probability ``bug`` a read or removal instead returns what an earlier, stale view of the object held."""
    t = [0.0] * threads
    pending = []
    for k in range(ops):
        th = rng.randrange(threads)
        start = t[th] + rng.random()
        end = start + 0.2 + rng.random() * 3
        t[th] = end
        point = start + rng.random() * (end - start)
        if spec in ("queue", "stack"):
            kind = (("enq" if spec == "queue" else "push") if rng.random() < 0.55 else
                    ("deq" if spec == "queue" else "pop"))
            arg = k if kind in ("enq", "push") else None
        elif spec == "register":
            kind = "write" if rng.random() < 0.5 else "read"
            arg = k if kind == "write" else None
        else:
            kind, arg = "inc", None
        pending.append((point, th, kind, arg, start, end))
    pending.sort()
    state = INIT[spec]
    hist = []
    prev = state
    for point, th, kind, arg, start, end in pending:
        op = Op(th, kind, arg, None, start, end)
        if spec in ("queue", "stack") and kind in ("deq", "pop"):
            use = prev if (bug and rng.random() < bug) else state
            ret = None if not use else (use[0] if spec == "queue" else use[-1])
            ok, new = apply(spec, state, Op(th, kind, None, ret, 0, 0))
            if not ok:                     # the stale answer: remove it anyway if present
                new = tuple(x for x in state if x != ret) if ret in state else state
            op = Op(th, kind, arg, ret, start, end)
        elif spec == "register" and kind == "read":
            ret = prev if (bug and rng.random() < bug) else state
            op = Op(th, kind, arg, ret, start, end)
            new = state
        elif spec == "counter":
            ret = prev if (bug and rng.random() < bug) else state
            op = Op(th, kind, arg, ret, start, end)
            new = state + 1
        else:
            _, new = apply(spec, state, op)
        hist.append(op)
        prev, state = state, new
    return sorted(hist, key=lambda o: o.start)
