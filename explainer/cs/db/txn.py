"""Transactions (Part 35): schedules and serializability, two-phase locking, snapshot isolation, and the anomalies
that each isolation level allows.

**Schedules.**  A schedule is a list of steps (transaction, action, item), action one of "r", "w", "c" (commit),
"a" (abort).  ``precedence(s)`` draws an edge Ti -> Tj for each pair of conflicting steps (same item, different
transactions, at least one a write) with Ti's first; ``conflict_serializable`` is true exactly when that graph has no
cycle, and a topological order is an equivalent serial schedule.  ``view_serializable`` tries every serial order
(the problem is NP-complete; Papadimitriou 1979).

**Two-phase locking.**  ``run_2pl`` executes transactions step by step in a requested interleaving with shared and
exclusive locks held to commit (strict 2PL); a step that must wait is retried later; a cycle of waits is a deadlock,
broken by aborting the youngest (or, with ``policy`` "wait-die" / "wound-wait", prevented by timestamps).

**Isolation levels.**  ``run_level(level, programs, order)`` interprets small transaction programs under
READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ (item locks, no predicate locks), SNAPSHOT (multiversion reads,
first committer wins), SNAPSHOT + SSI (Cahill et al. 2008: abort on a pivot with rw-antidependencies in and out) and
SERIALIZABLE (locks on items and on predicates).  ``anomaly(level, case)`` runs one of the classic histories and
compares the outcome with every serial order of the committed transactions.
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass, field


# ---- schedules ------------------------------------------------------------------------------------------------------
def committed(s) -> set:
    return {t for t, a, _ in s if a == "c"} or {t for t, _, _ in s}


def precedence(s) -> set:
    keep = committed(s)
    ops = [(t, a, x) for t, a, x in s if t in keep and a in "rw"]
    edges = set()
    for i, (ti, ai, xi) in enumerate(ops):
        for tj, aj, xj in ops[i + 1:]:
            if ti != tj and xi == xj and "w" in (ai, aj):
                edges.add((ti, tj))
    return edges


def find_cycle(nodes, edges):
    adj = {n: [b for a, b in edges if a == n] for n in nodes}
    color = {n: 0 for n in nodes}
    stack = []

    def dfs(u):
        color[u] = 1
        stack.append(u)
        for v in adj[u]:
            if color[v] == 1:
                return stack[stack.index(v):] + [v]
            if color[v] == 0:
                c = dfs(v)
                if c:
                    return c
        color[u] = 2
        stack.pop()
        return None
    for n in nodes:
        if color[n] == 0:
            c = dfs(n)
            if c:
                return c
    return None


def conflict_serializable(s):
    """(True, a serial order) or (False, a cycle)."""
    nodes = sorted(committed(s))
    edges = precedence(s)
    cyc = find_cycle(nodes, edges)
    if cyc:
        return False, cyc
    order, indeg = [], {n: 0 for n in nodes}
    for _, b in edges:
        indeg[b] += 1
    ready = [n for n in nodes if not indeg[n]]
    while ready:
        n = ready.pop(0)
        order.append(n)
        for a, b in sorted(edges):
            if a == n:
                indeg[b] -= 1
                if not indeg[b]:
                    ready.append(b)
    return True, order


def _view(s):
    """Reads-from pairs and final writers: what view equivalence compares."""
    last = {}
    rf = []
    for t, a, x in s:
        if a == "r":
            rf.append((t, x, last.get(x)))
        elif a == "w":
            last[x] = t
    return sorted(rf, key=str), sorted(last.items())


def view_serializable(s):
    keep = committed(s)
    s = [st for st in s if st[0] in keep and st[1] in "rw"]
    want = _view(s)
    txns = sorted(keep)
    for perm in itertools.permutations(txns):
        serial = [st for t in perm for st in s if st[0] == t]
        if _view(serial) == want:
            return True, list(perm)
    return False, None


# ---- strict two-phase locking ------------------------------------------------------------------------------------
def run_2pl(txns: dict, order: list, policy: str = "detect", strict: bool = True) -> dict:
    """``txns``: {t: [(action, item)]} ("r"/"w", item); ``order``: the transaction to try at each turn (repeated as
    needed).  Returns the executed schedule, aborts, waits and deadlocks."""
    locks: dict = {}                                   # item -> (mode, set of holders)
    pc = {t: 0 for t in txns}
    done, aborted = set(), set()
    sched, waits, deadlocks = [], 0, 0
    ts = {t: k for k, t in enumerate(sorted(txns))}    # timestamps: lower is older
    waiting: dict = {}

    def can(t, a, x):
        m = locks.get(x)
        if not m or not m[1] or m[1] == {t}:
            return True, set()
        if a == "r" and m[0] == "S":
            return True, set()
        return False, m[1] - {t}

    def grant(t, a, x):
        m = locks.get(x)
        if a == "w":
            locks[x] = ("X", {t})
        elif not m or not m[1]:
            locks[x] = ("S", {t})
        elif m[0] == "S" or m[1] == {t}:
            locks[x] = (m[0], m[1] | {t})

    def release(t):
        for x in list(locks):
            mode, hs = locks[x]
            hs = hs - {t}
            locks[x] = (mode, hs) if hs else None
            if not hs:
                del locks[x]

    def abort(t):
        aborted.add(t)
        sched.append((t, "a", None))
        release(t)
        waiting.pop(t, None)

    turns = list(order)
    k, idle = 0, 0
    while len(done | aborted) < len(txns):
        if k >= len(turns):
            turns += [t for t in sorted(txns) if t not in done | aborted]
        t = turns[k]
        k += 1
        if t in done or t in aborted:
            continue
        if pc[t] == len(txns[t]):
            done.add(t)
            sched.append((t, "c", None))
            release(t)
            waiting.pop(t, None)
            idle = 0
            continue
        a, x = txns[t][pc[t]]
        ok, blockers = can(t, a, x)
        if ok:
            grant(t, a, x)
            sched.append((t, a, x))
            pc[t] += 1
            waiting.pop(t, None)
            idle = 0
            if not strict and pc[t] == len(txns[t]):
                pass
            continue
        waits += 1
        if policy == "wait-die" and any(ts[t] > ts[b] for b in blockers):
            abort(t)                                   # younger asks older: die
            continue
        if policy == "wound-wait":
            for b in [b for b in blockers if ts[t] < ts[b]]:
                abort(b)                               # older asks younger: wound it
            continue
        waiting[t] = blockers
        cyc = find_cycle(list(waiting), {(u, v) for u, bs in waiting.items() for v in bs if v in waiting})
        if cyc:
            deadlocks += 1
            victim = max(set(cyc), key=lambda u: ts[u])
            abort(victim)
        idle += 1
        if idle > 4 * len(txns) + 4:
            break
    return {"schedule": sched, "aborted": sorted(aborted), "committed": sorted(done), "waits": waits,
            "deadlocks": deadlocks}


# ---- isolation levels ------------------------------------------------------------------------------------------------
LEVELS = ("read uncommitted", "read committed", "repeatable read", "snapshot", "snapshot + SSI", "serializable")


@dataclass
class Txn:
    tid: int
    prog: list
    pc: int = 0
    env: dict = field(default_factory=dict)
    writes: dict = field(default_factory=dict)
    reads: list = field(default_factory=list)          # what it saw, in order
    start: int = 0
    state: str = "active"
    rset: set = field(default_factory=set)
    wset: set = field(default_factory=set)
    preds: list = field(default_factory=list)


def run_level(level: str, init: dict, programs: dict, order: list) -> dict:
    """Interpret ``programs`` ({tid: [step]}) under an isolation level.  Steps:
    ("r", item, var); ("w", item, fn(env)); ("count", pred(key, value), var): how many items satisfy pred;
    ("ins", item, fn(env)); ("abort",).  Every program ends with an implicit commit."""
    assert level in LEVELS
    db = dict(init)                                    # latest committed values (and, for RU, dirty ones)
    versions = {k: [(0, v)] for k, v in init.items()}  # MVCC: (commit time, value)
    clock = 1
    T = {t: Txn(t, list(p) + [("commit",)]) for t, p in programs.items()}
    locks: dict = {}
    plocks: list = []                                  # predicate locks: (tid, pred)
    rw_in, rw_out = set(), set()                       # SSI: transactions with an incoming / outgoing rw edge
    log = []
    undo: dict = {t: [] for t in T}

    def lock(t, x, mode):
        if level in ("read uncommitted", "read committed") and mode == "S":
            return True
        if level.startswith("snapshot"):
            return True
        m = locks.get(x)
        if not m or m[1] == {t} or (mode == "S" and m[0] == "S"):
            if not m:
                locks[x] = (mode, {t})
            elif m[1] == {t}:
                locks[x] = ("X" if mode == "X" or m[0] == "X" else "S", {t})
            else:
                locks[x] = ("S", m[1] | {t})
            return True
        return False

    def release(t):
        for x in list(locks):
            mode, hs = locks[x]
            hs = hs - {t}
            if hs:
                locks[x] = (mode, hs)
            else:
                del locks[x]
        plocks[:] = [(u, p) for u, p in plocks if u != t]

    def snapshot_value(tx, x):
        if x in tx.writes:
            return tx.writes[x]
        vs = [v for ts, v in versions.get(x, []) if ts <= tx.start]
        return vs[-1] if vs else None

    def finish(tx, ok=True):
        nonlocal clock
        if ok:
            if level.startswith("snapshot"):
                for x in tx.wset:                      # first committer wins
                    if any(ts > tx.start for ts, _ in versions.get(x, [])):
                        return finish(tx, ok=False)
                if level == "snapshot + SSI" and tx.tid in rw_in and tx.tid in rw_out:
                    return finish(tx, ok=False)
                for x, v in tx.writes.items():
                    versions.setdefault(x, []).append((clock, v))
                    db[x] = v
                clock += 1
            elif level != "read uncommitted":
                for x, v in tx.writes.items():
                    db[x] = v
            tx.state = "committed"
            log.append((tx.tid, "commit"))
        else:
            if level == "read uncommitted":
                for x, old in reversed(undo[tx.tid]):
                    if old is None:
                        db.pop(x, None)
                    else:
                        db[x] = old
            tx.state = "aborted"
            log.append((tx.tid, "abort"))
        release(tx.tid)

    def read(tx, x):
        if level == "read uncommitted":
            return db.get(x)
        if level.startswith("snapshot"):
            if level == "snapshot + SSI":
                for u in T.values():                   # tx read a version u is overwriting: tx -rw-> u
                    if u is not tx and u.state != "aborted" and x in u.wset and (
                            u.state == "active" or u.start >= tx.start):
                        rw_out.add(tx.tid)
                        rw_in.add(u.tid)
            tx.rset.add(x)
            return snapshot_value(tx, x)
        return tx.writes.get(x, db.get(x))

    def step(tx) -> bool:
        """Try the next step; False if it must wait."""
        op = tx.prog[tx.pc]
        kind = op[0]
        if kind == "commit":
            finish(tx)
            return True
        if kind == "abort":
            finish(tx, ok=False)
            return True
        if kind == "r":
            _, x, var = op
            if not lock(tx.tid, x, "S"):
                return False
            tx.env[var] = read(tx, x)
            tx.reads.append((x, tx.env[var]))
        elif kind == "count":
            _, pred, var = op
            if level == "serializable":
                for u, p in plocks:
                    pass
                if any(locks.get(x, ("S", set()))[0] == "X" and locks[x][1] - {tx.tid} for x in db):
                    return False
                plocks.append((tx.tid, pred))
            keys = set(db) | set(tx.writes)
            if level.startswith("snapshot"):
                keys = {k for k in versions if snapshot_value(tx, k) is not None} | set(tx.writes)
            n = 0
            for k in sorted(keys, key=str):
                if level == "repeatable read" or level == "serializable":
                    if not lock(tx.tid, k, "S"):
                        return False
                v = read(tx, k)
                if v is not None and pred(k, v):
                    n += 1
            tx.env[var] = n
            tx.reads.append(("count", n))
        elif kind in ("w", "ins"):
            _, x, fn = op
            if level == "serializable" and kind == "ins":
                if any(u != tx.tid and p(x, fn(tx.env)) for u, p in plocks):
                    return False
            if not lock(tx.tid, x, "X"):
                return False
            v = fn(tx.env)
            tx.wset.add(x)
            if level == "snapshot + SSI":
                for u in T.values():                   # someone read x before this write: u -rw-> tx
                    if u is not tx and u.state != "aborted" and x in u.rset:
                        rw_out.add(u.tid)
                        rw_in.add(tx.tid)
            if level == "read uncommitted":
                undo[tx.tid].append((x, db.get(x)))
                db[x] = v
            tx.writes[x] = v
        tx.pc += 1
        log.append((tx.tid, kind))
        return True
    turns = list(order)
    k = stall = 0
    started = set()
    while any(t.state == "active" for t in T.values()):
        if k >= len(turns):
            turns += [t for t in sorted(T) if T[t].state == "active"]
        t = turns[k]
        k += 1
        tx = T[t]
        if tx.state != "active":
            continue
        if t not in started:
            tx.start = clock - 1 if level.startswith("snapshot") else 0
            started.add(t)
        if step(tx):
            stall = 0
        else:
            stall += 1
            log.append((t, "wait"))
            if stall > 2 * len(T) + 2:                 # everyone is waiting: a deadlock; abort the youngest
                victim = max(u for u in T if T[u].state == "active")
                finish(T[victim], ok=False)
                stall = 0
    return {"db": dict(sorted(db.items(), key=lambda kv: str(kv[0]))), "reads": {t: T[t].reads for t in T},
            "committed": sorted(t for t in T if T[t].state == "committed"),
            "aborted": sorted(t for t in T if T[t].state == "aborted"), "log": log}


def serial_outcomes(init: dict, programs: dict, txns) -> list:
    out = []
    for perm in itertools.permutations(txns):
        r = run_level("serializable", init, {t: programs[t] for t in perm}, [t for t in perm for _ in range(50)])
        out.append((r["db"], {t: r["reads"][t] for t in perm}))
    return out


def anomaly(level: str, case: dict) -> str:
    """"prevented" when the outcome matches some serial order of the transactions that committed (or every
    transaction but one was stopped), "allowed" when it matches none."""
    r = run_level(level, case["init"], case["programs"], case["order"])
    progs = {t: [s for s in p if s[0] != "abort"] for t, p in case["programs"].items()}
    if case.get("dirty"):                              # the writer aborts: its write must never have been seen
        seen = r["reads"][case["dirty"]["reader"]]
        bad = any(v == case["dirty"]["value"] for _, v in seen)
        return "allowed" if bad else "prevented"
    ok = r["committed"]
    if len(ok) < 2:
        return "prevented"
    serial = serial_outcomes(case["init"], progs, ok)
    mine = (r["db"], {t: r["reads"][t] for t in ok})
    return "prevented" if mine in serial else "allowed"


def CASES() -> dict:
    """The classic anomalies, each as programs and an interleaving (the transaction to step at each turn)."""
    inc = lambda var: (lambda e: e[var] + 1)  # noqa: E731
    return {
        "dirty read": {"init": {"x": 0}, "programs": {
            1: [("w", "x", lambda e: 99), ("abort",)],
            2: [("r", "x", "v")]}, "order": [1, 2, 1, 2], "dirty": {"reader": 2, "value": 99}},
        "non-repeatable read": {"init": {"x": 0}, "programs": {
            1: [("r", "x", "a"), ("r", "x", "b")],
            2: [("w", "x", lambda e: 1)]}, "order": [1, 2, 2, 1, 1]},
        "lost update": {"init": {"x": 0}, "programs": {
            1: [("r", "x", "v"), ("w", "x", inc("v"))],
            2: [("r", "x", "v"), ("w", "x", inc("v"))]}, "order": [1, 2, 1, 2, 1, 2]},
        "phantom": {"init": {"a": 1, "b": 1}, "programs": {
            1: [("count", lambda k, v: v == 1, "n1"), ("count", lambda k, v: v == 1, "n2")],
            2: [("ins", "c", lambda e: 1)]}, "order": [1, 2, 2, 1, 1]},
        "write skew": {"init": {"alice": 1, "bob": 1}, "programs": {
            1: [("r", "alice", "a"), ("r", "bob", "b"), ("w", "alice", lambda e: 0 if e["a"] + e["b"] >= 2 else 1)],
            2: [("r", "alice", "a"), ("r", "bob", "b"), ("w", "bob", lambda e: 0 if e["a"] + e["b"] >= 2 else 1)]},
            "order": [1, 2, 1, 2, 1, 2, 1, 2]},
    }


def anomaly_table() -> dict:
    cases = CASES()
    return {lv: {name: anomaly(lv, c) for name, c in cases.items()} for lv in LEVELS}
