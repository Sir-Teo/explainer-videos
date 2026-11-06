"""Precompute everything numerical in Part 33 of *Computer Science, Built* ("Concurrency").

    python -m videos.cs.cs33.compute              # everything missing
    python -m videos.cs.cs33.compute --force race

Results are cached in ``.cache/cs33/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/conc/`` (mc.py: the interleaving model checker under SC, TSO and PSO; lin.py: the linearizability
checker; locks.py: spin locks on Part 10's MESI caches), Pebble's atomic extension (``cas``, ``amoadd``) and
PebbleOS threads (``explainer/cs/os/vmos.threads_vm``), and ``conc.c``, run on this machine; tests in
tests/test_cs33_conc.py.

Items:
    tree        counter++ by two threads: all 20 schedules, each with the final count
    race        the model checker on counter++: outcomes for k increments each, and with fetch-and-add or a lock
    racec       this machine: 1, 2 and 4 threads adding 10^7 each, plain, atomic and under a mutex
    mutex       the naive flag lock (a violation), Peterson under SC (states; the region grid), the bakery
    tso         Peterson and the bakery under SC, TSO and PSO, with and without fences; the shortest bad schedules
    litmus      store buffering and message passing under SC, TSO and PSO; and Part 10's run on this machine
    lockssim    TAS, TTAS, backoff, ticket and MCS on simulated MESI caches, 2 to 32 cores: traffic, time, fairness
    locksc      this machine: the same locks and pthread_mutex, 1, 2 and 4 threads
    sema        the bounded buffer with and without its mutex: every reachable final count
    monitor     a Mesa monitor with `if` and with `while`: can a consumer take from an empty buffer?
    deadlock    five philosophers, left fork first and with a lock order; the banker's algorithm
    drf         a data-race-free version of store buffering: TSO gives only SC outcomes
    lin         linearizability: two hand histories; random correct and buggy histories; the checker's cost
    aba         the Treiber stack with a plain and a tagged CAS: every final stack, and the ABA schedule
    consensus   test-and-set for 2 and 3, compare-and-swap for 3, registers for 2: agreement checked
    tsx         this machine: hardware transactions (Intel RTM) that commit
    hoist       this machine: gcc -O2 on a spin loop over a plain flag (it hoists the load) and an atomic one
    tsan        this machine: ThreadSanitizer on the hook's racy program, and on the atomic version
    spawn       this machine: creating and joining a thread against forking and waiting for a process
    pebble      PebbleOS threads: a racy counter, amoadd, and a CAS lock, under three quanta
    frontier    state explosion (Peterson rounds, bakery threads, three models); linearizability checking time
"""

from __future__ import annotations

import random
import subprocess
import tempfile
import time
from pathlib import Path

from explainer.ai.cache import Cache

CACHE = Cache("cs33")
load = CACHE.load
HERE = Path(__file__).parent


def _exe(d):
    out = str(Path(d, "conc"))
    subprocess.run(["gcc", "-O2", "-pthread", "-o", out, str(HERE / "conc.c")], check=True, capture_output=True)
    return out


def _run(exe, *args):
    return subprocess.run([exe, *map(str, args)], capture_output=True, text=True, check=True).stdout.split()


def _mem(s, prog):
    return dict(zip(prog.vars, s[2]))


def compute_tree() -> dict:
    """Every schedule of two threads each doing  ld r, c;  addi r, r, 1;  st c, r."""
    from explainer.cs.conc import mc as M
    p = M.counter(2, 1)
    out = []

    def go(s, path):
        succ = list(M.successors(p, s, "sc"))
        if not succ:
            out.append({"order": path, "c": _mem(s, p)["c"]})
            return
        for label, t in succ:
            go(t, path + label[1])
    go(M.initial(p, "sc"), "")
    return {"schedules": out, "n": len(out), "formula": M.interleavings([3, 3]),
            "lost": sum(1 for o in out if o["c"] == 1)}


def compute_race() -> dict:
    from explainer.cs.conc import mc as M
    rows = []
    for k in (1, 2, 3, 4):
        p = M.counter(2, k)
        r = M.explore(p, project=lambda s, q: _mem(s, q)["c"])
        sch = M.schedules(p, project=lambda s, q: _mem(s, q)["c"])
        rows.append({"k": k, "states": r.states, "outcomes": sorted(r.finals), "schedules": sum(sch.values()),
                     "by_outcome": {str(a): b for a, b in sorted(sch.items())},
                     "formula": M.interleavings([3 * k, 3 * k])})
    three = M.explore(M.counter(3, 1), project=lambda s, q: _mem(s, q)["c"])
    fixed = {}
    for how in ("fai", "lock"):
        r = M.explore(M.counter(2, 3, how), project=lambda s, q: _mem(s, q)["c"])
        fixed[how] = {"outcomes": sorted(r.finals), "states": r.states}
    return {"rows": rows, "three": {"outcomes": sorted(three.finals), "states": three.states}, "fixed": fixed}


def compute_racec() -> dict:
    with tempfile.TemporaryDirectory() as d:
        exe = _exe(d)
        rows = []
        for t in (1, 2, 4):
            out = _run(exe, "race", t, 10_000_000)
            for i in range(0, len(out), 5):
                rows.append({"mode": out[i], "threads": int(out[i + 1]), "value": int(out[i + 2]),
                             "expected": int(out[i + 3]), "ns": float(out[i + 4])})
    return {"rows": rows}


def compute_mutex() -> dict:
    from explainer.cs.conc import mc as M
    nv = M.explore(M.naive_flags(1), "sc", M.mutex)
    pet = M.explore(M.peterson(False, 1), "sc", M.mutex)
    pet2 = M.explore(M.peterson(False, 2), "sc", M.mutex)
    # Peterson's states drawn by where each thread is: before (0), announced (1), waiting (2), inside (3), after (4)
    p = M.peterson(False, 1)

    def region(pc, inc):
        if inc:
            return 3
        return 0 if pc == 0 else 1 if pc == 1 else 2 if pc <= 6 else 4
    assert len(p.code[0]) == 9
    cells = set()
    for s in pet.parent:
        cells.add((region(s[0][0], s[4][0]), region(s[0][1], s[4][1])))
    bak = {n: M.explore(M.bakery(n, 1), "sc", M.mutex) for n in (2, 3)}
    return {"naive": {"states": nv.states, "trace": nv.trace(nv.violation)},
            "peterson": {"states": pet.states, "edges": pet.edges, "ok": pet.violation is None,
                         "states2": pet2.states, "ok2": pet2.violation is None, "cells": sorted(cells)},
            "bakery": {str(n): {"states": r.states, "ok": r.violation is None} for n, r in bak.items()}}


def compute_tso() -> dict:
    from explainer.cs.conc import mc as M
    rows = []
    for name, mk in (("Peterson", lambda f: M.peterson(f, 2)), ("bakery", lambda f: M.bakery(2, 1, bool(f)))):
        for model in ("sc", "tso", "pso"):
            for f in (False, True, "both"):
                if name == "bakery" and f == "both":
                    continue
                r = M.explore(mk(f), model, M.mutex)
                rows.append({"alg": name, "model": model, "fence": str(f), "states": r.states,
                             "ok": r.violation is None,
                             "trace": r.trace(r.violation) if r.violation else None})
    return {"rows": rows}


def compute_litmus() -> dict:
    from explainer.cs.conc import mc as M
    out = {}
    for model in ("sc", "tso", "pso"):
        for f in (False, True):
            sb = M.explore(M.litmus_sb(f), model, project=lambda s, q: (_mem(s, q)["r1"], _mem(s, q)["r2"]))
            mp = M.explore(M.litmus_mp(f), model, project=lambda s, q: _mem(s, q)["r"])
            out[f"{model}{'_fence' if f else ''}"] = {"sb": [list(x) for x in sorted(sb.finals)],
                                                      "mp": sorted(mp.finals)}
    r = M.explore(M.litmus_sb(False), "tso", invariant=lambda s, q: not (
        all(pc >= len(c) for pc, c in zip(s[0], q.code)) and _mem(s, q)["r1"] == 0 and _mem(s, q)["r2"] == 0
        and not any(s[3])))
    from videos.cs.cs10.compute import load as load10
    l10 = load10("litmus")
    return {"models": out, "sb_trace": r.trace(r.violation), "machine": {"plain": l10["plain"],
                                                                         "mfence": l10["mfence"],
                                                                         "trials": l10["trials"]}}


def compute_lockssim() -> dict:
    from explainer.cs.conc import locks as K
    rows = []
    for n in (2, 4, 8, 16, 32):
        for kind in ("tas", "ttas", "backoff", "ticket", "mcs"):
            r = K.simulate(kind, n, 300, cs=4, think=40)
            rows.append({k: r[k] for k in ("kind", "cores", "bus_per_acq", "cycles_per_acq", "fair")})
    return {"rows": rows, "bus_cycles": 8, "cs": 4, "think": 40}


def compute_locksc() -> dict:
    with tempfile.TemporaryDirectory() as d:
        exe = _exe(d)
        rows = []
        for kind in ("tas", "ttas", "ticket", "mcs", "mutex"):
            for t in (1, 2, 4):
                best = None
                for _ in range(3):
                    o = _run(exe, "lock", kind, t, 0.5)
                    r = {"kind": o[0], "threads": int(o[1]), "acq": int(o[2]), "ns": float(o[3]),
                         "fair": float(o[4]), "data": int(o[5])}
                    if best is None or r["ns"] < best["ns"]:
                        best = r
                rows.append(best)
    from videos.cs.cs32.compute import _cpu
    return {"rows": rows, "cpu": _cpu(), "cores": len([1 for ln in Path("/proc/cpuinfo").read_text().splitlines()
                                                     if ln.startswith("processor")])}


def compute_sema() -> dict:
    from explainer.cs.conc import mc as M
    out = {}
    for broken in (False, True):
        r = M.explore(M.bounded_buffer(1, 1, 3, 2, broken), project=lambda s, q: _mem(s, q)["count"])
        out["broken" if broken else "correct"] = {"finals": {str(k): v for k, v in sorted(r.finals.items())},
                                                  "states": r.states}
    return out


def monitor_program(use_while: bool):
    """A Mesa monitor: one producer adds two items; two consumers take one each.  wait(cv) is: count yourself a
    waiter, unlock, sleep on the semaphore, lock again; signal wakes one waiter if there is one."""
    from explainer.cs.conc import mc as M
    cons = []
    for i in range(2):
        code = [("lock", "m"), ("label", "chk"), ("ld", "c", "count"), ("bne", "c", 0, "take"),
                ("ld", "w", "waiters"), ("addi", "w", "w", 1), ("st", "waiters", "w"), ("unlock", "m"),
                ("P", "cv"), ("lock", "m")]
        code += [("jmp", "chk")] if use_while else []
        code += [("label", "take"), ("ld", "c", "count"), ("addi", "c", "c", -1), ("st", "count", "c"),
                 ("unlock", "m")]
        cons.append(code)
    prod = []
    for k in range(2):
        prod += [("lock", "m"), ("ld", "c", "count"), ("addi", "c", "c", 1), ("st", "count", "c"),
                 ("ld", "w", "waiters"), ("beq", "w", 0, f"ns{k}"), ("addi", "w", "w", -1), ("st", "waiters", "w"),
                 ("V", "cv"), ("label", f"ns{k}"), ("unlock", "m")]
    return M.Program({"m": 0, "count": 0, "waiters": 0, "cv": 0}, [prod] + cons, ["producer", "C1", "C2"])


def compute_monitor() -> dict:
    from explainer.cs.conc import mc as M
    out = {}
    for w in (False, True):
        p = monitor_program(w)
        r = M.explore(p, invariant=lambda s, q: _mem(s, q)["count"] >= 0)
        out["while" if w else "if"] = {"states": r.states, "ok": r.violation is None,
                                       "trace": r.trace(r.violation) if r.violation else None,
                                       "deadlocks": len(r.deadlocks)}
    return out


def banker(avail, maxm, alloc):
    """The banker's algorithm (Dijkstra 1965): a safe order, or None."""
    n = len(maxm)
    need = [[m - a for m, a in zip(maxm[i], alloc[i])] for i in range(n)]
    work, done, order = list(avail), [False] * n, []
    while len(order) < n:
        for i in range(n):
            if not done[i] and all(x <= w for x, w in zip(need[i], work)):
                work = [w + a for w, a in zip(work, alloc[i])]
                done[i] = True
                order.append(i)
                break
        else:
            return None
    return order


def compute_deadlock() -> dict:
    from explainer.cs.conc import mc as M
    out = {}
    for ordered in (False, True):
        r = M.explore(M.philosophers(5, ordered))
        out["ordered" if ordered else "naive"] = {"states": r.states, "deadlocks": len(r.deadlocks),
                                                  "trace": r.trace(r.deadlocks[0]) if r.deadlocks else None}
    # Silberschatz's example: 5 processes, 3 resource types (10, 5, 7)
    maxm = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
    alloc = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
    total = [10, 5, 7]
    avail = [t - sum(a[j] for a in alloc) for j, t in enumerate(total)]
    safe = banker(avail, maxm, alloc)
    # P1 asks for (1, 0, 2): grant if the result is still safe; then P4 asks for (3, 3, 0); then P0 for (0, 2, 0)
    reqs = []
    a, al = list(avail), [row[:] for row in alloc]
    for pi, req in ((1, [1, 0, 2]), (4, [3, 3, 0]), (0, [0, 2, 0])):
        if any(r > x for r, x in zip(req, a)):
            reqs.append({"p": pi, "req": req, "granted": False, "why": "not available"})
            continue
        a2 = [x - r for x, r in zip(a, req)]
        al2 = [row[:] for row in al]
        al2[pi] = [x + r for x, r in zip(al2[pi], req)]
        s = banker(a2, maxm, al2)
        if s is None:
            reqs.append({"p": pi, "req": req, "granted": False, "why": "unsafe"})
        else:
            reqs.append({"p": pi, "req": req, "granted": True, "order": s})
            a, al = a2, al2
    out["banker"] = {"total": total, "max": maxm, "alloc": alloc, "avail": avail, "safe": safe, "requests": reqs}
    return out


def compute_drf() -> dict:
    """Store buffering with every shared access under a lock (data-race-free): TSO and PSO give only SC outcomes."""
    from explainer.cs.conc import mc as M

    def sb_locked():
        return M.Program({"x": 0, "y": 0, "r1": 0, "r2": 0, "m": 0},
                         [[("lock", "m"), ("st", "x", 1), ("unlock", "m"), ("lock", "m"), ("ld", "a", "y"),
                           ("unlock", "m"), ("st", "r1", "a")],
                          [("lock", "m"), ("st", "y", 1), ("unlock", "m"), ("lock", "m"), ("ld", "b", "x"),
                           ("unlock", "m"), ("st", "r2", "b")]])
    out = {}
    for model in ("sc", "tso", "pso"):
        r = M.explore(sb_locked(), model, project=lambda s, q: (_mem(s, q)["r1"], _mem(s, q)["r2"]))
        out[model] = [list(x) for x in sorted(r.finals)]
    return {"locked": out}


def compute_lin() -> dict:
    from explainer.cs.conc import lin as L
    Op = L.Op
    good = [Op(0, "enq", "x", None, 0.0, 2.0), Op(1, "enq", "y", None, 1.0, 3.5), Op(2, "deq", None, "y", 2.5, 4.0),
            Op(0, "deq", None, "x", 4.5, 6.0)]
    bad = [Op(0, "enq", "x", None, 0.0, 1.5), Op(1, "enq", "y", None, 2.0, 3.0), Op(2, "deq", None, "y", 3.5, 4.5),
           Op(0, "deq", None, "x", 5.0, 6.0)]
    hand = []
    for name, h in (("overlapping", good), ("ordered", bad)):
        lin = L.check(h, "queue")
        hand.append({"name": name, "ops": [o.__dict__ for o in h], "lin": lin})
    rng = random.Random(4)
    stats = {}
    for spec in ("queue", "stack", "register", "counter"):
        for bug in (0.0, 0.3):
            ok = 0
            for _ in range(500):
                ok += L.check(L.random_history(spec, 3, 12, rng, bug), spec) is not None
            stats[f"{spec}_{bug}"] = {"linearizable": ok, "of": 500}
    return {"hand": hand, "random": stats}


def compute_aba() -> dict:
    from explainer.cs.conc import mc as M
    out = {}
    for tagged in (False, True):
        p = M.treiber_aba(tagged)
        T = 100 if tagged else None

        def proj(s, q, T=T):
            popped = [v for o in s[5] for v in o if v > 0]
            pushed = [-v for o in s[5] for v in o if v < 0]
            st = M.stack_of(s, q, T)
            return (tuple(st), tuple(sorted(popped)), bool((set(popped) - set(pushed)) & set(st)))

        def bad(s, q, T=T):
            if not M.halted(q, s):
                return True
            return not proj(s, q)[2]
        r = M.explore(p, invariant=bad, project=proj)
        out["tagged" if tagged else "plain"] = {
            "states": r.states, "finals": [[list(a), list(b), c] for (a, b, c) in sorted(r.finals)],
            "trace": r.trace(r.violation) if r.violation else None}
    return out


def compute_consensus() -> dict:
    from explainer.cs.conc import mc as M
    out = {}
    for name, p in (("tas2", M.consensus_tas(2)), ("tas3", M.consensus_tas(3)), ("cas3", M.consensus_cas(3)),
                    ("reg2", M.consensus_registers(2))):
        def proj(s, q):
            return tuple(o[0] if o else None for o in s[5])
        r = M.explore(p, invariant=lambda s, q: M.agreement(s, q) and all(
            (not o) or o[0] in range(10, 10 + len(q.threads)) for o in s[5]), project=proj)
        out[name] = {"states": r.states, "ok": r.violation is None, "finals": [list(f) for f in sorted(
            r.finals, key=str)], "trace": r.trace(r.violation) if r.violation else None}
    return out


def compute_spawn() -> dict:
    with tempfile.TemporaryDirectory() as d:
        exe = _exe(d)
        best = None
        for _ in range(3):
            o = _run(exe, "spawn", 2000)
            r = (float(o[1]), float(o[2]))
            best = r if best is None or r[0] < best[0] else best
    return {"thread_us": best[0], "process_us": best[1]}


RACE_C = r"""#include <pthread.h>
#include <stdio.h>
long count = 0;
void *work(void *a) { for (int i = 0; i < 1000000; i++) count = count + 1; return a; }
int main(void) {
    pthread_t t[2];
    for (int i = 0; i < 2; i++) pthread_create(&t[i], NULL, work, NULL);
    for (int i = 0; i < 2; i++) pthread_join(t[i], NULL);
    printf("%ld\n", count);
    return 0;
}
"""


def compute_tsan() -> dict:
    """ThreadSanitizer (a happens-before race detector) on the hook's program; on it with an atomic variable but the
    same load-then-store (no data race, still lost updates); and with an atomic increment."""
    import re
    out = {}
    with tempfile.TemporaryDirectory() as d:
        atomic = RACE_C.replace("long count = 0;", "_Atomic long count = 0;")
        for name, src in (("racy", RACE_C), ("atomic_rw", atomic),
                          ("atomic_inc", atomic.replace("count = count + 1", "count += 1"))):
            Path(d, "race.c").write_text(src)
            subprocess.run(["gcc", "-g", "-O1", "-fsanitize=thread", "-pthread", "race.c", "-o", "race"], cwd=d,
                           check=True, capture_output=True)
            r = subprocess.run(["./race"], cwd=d, capture_output=True, text=True)
            keep = []
            for ln in r.stderr.splitlines():
                ln = re.sub(r"/\S*/race\.c", "race.c", ln)
                ln = re.sub(r" \(race\+0x[0-9a-f]+\).*", "", ln)
                ln = re.sub(r"0x[0-9a-f]{8,}", "0x...", ln)
                ln = re.sub(r"\(pid=\d+\)", "", ln).rstrip()
                if any(k in ln for k in ("WARNING", " of size 8 at", "#0 work", "Location is",
                                          "reported")):
                    keep.append(ln.strip())
            out[name] = {"lines": keep, "warnings": sum("WARNING: ThreadSanitizer" in x for x in keep),
                         "printed": r.stdout.strip()}
    return out


HOIST = {"plain": "int done;\nint data;\nint wait_for(void) {\n    while (!done)\n        ;\n    return data;\n}\n",
         "atomic": "#include <stdatomic.h>\natomic_int done;\nint data;\nint wait_for(void) {\n"
                   "    while (!atomic_load_explicit(&done, memory_order_acquire))\n        ;\n    return data;\n}\n"}


def compute_hoist() -> dict:
    """What gcc -O2 makes of a spin loop on a plain flag, and on an atomic one."""
    out = {}
    with tempfile.TemporaryDirectory() as d:
        for name, src in HOIST.items():
            Path(d, "w.c").write_text(src)
            asm = subprocess.run(["gcc", "-O2", "-S", "-masm=intel", "-o", "-", "w.c"], cwd=d, capture_output=True,
                                 text=True, check=True).stdout.splitlines()
            body, on = [], False
            for ln in asm:
                if ln.startswith("wait_for:"):
                    on = True
                    continue
                if on:
                    t = ln.strip()
                    if t.startswith((".cfi", ".LFB", ".LFE", "endbr64", ".p2align", ".size")) or not t:
                        if t.startswith(".LFE"):
                            break
                        continue
                    body.append(t.replace("\t", " "))
                    if t == "ret":
                        break
            out[name] = {"src": src.splitlines(), "asm": body}
    out["gcc"] = subprocess.run(["gcc", "--version"], capture_output=True, text=True).stdout.splitlines()[0]
    return out


def compute_tsx() -> dict:
    with tempfile.TemporaryDirectory() as d:
        exe = _exe(d)
        o = _run(exe, "tsx", 1_000_000)
    flags = set()
    for ln in Path("/proc/cpuinfo").read_text().splitlines():
        if ln.startswith("flags"):
            flags = set(ln.split(":")[1].split())
            break
    taa = Path("/sys/devices/system/cpu/vulnerabilities/tsx_async_abort")
    return {"status": o[1], "committed": int(o[2]), "tried": int(o[3]), "rtm_flag": "rtm" in flags,
            "taa": taa.read_text().strip() if taa.exists() else "unknown"}


RACE_BODY = {
    "race": """
        lw   t1, 0(t0)          # load
        addi t1, t1, 1          # add
        sw   t1, 0(t0)          # store""",
    "amoadd": """
        li   t1, 1
        amoadd t2, t0, t1       # one indivisible add""",
    "lock": """
        la   s1, mutex
spin:   li   t1, 0
        li   t2, 1
        cas  t1, s1, t2         # t1 <- the old value; we hold the lock if it was 0
        beq  t1, zero, got
        la   s2, nspin
        li   t3, 1
        amoadd t3, s2, t3       # count the failed attempt
        li   a5, 4              # yield
        ecall
        j    spin
got:    lw   t1, 0(t0)
        addi t1, t1, 1
        sw   t1, 0(t0)
        sw   zero, 0(s1)        # unlock""",
}

THREAD = """
main:   addi sp, sp, -16
        sw   ra, 12(sp)
        la   t0, counter
        li   s0, {n}
loop:
{body}
        addi s0, s0, -1
        bne  s0, zero, loop
        la   t0, done
        li   t1, 1
        amoadd t2, t0, t1       # how many threads finished before me?
        li   t3, {last}
        bne  t2, t3, quit       # not the last: exit quietly
        la   t0, counter
        lw   a0, 0(t0)
        call print
        li   a0, 10
        call __putc
        lw   ra, 12(sp)
        addi sp, sp, 16
        ret
quit:   li   a5, 0
        li   a0, 0
        ecall
print:  addi sp, sp, -32        # a0 in decimal
        sw   ra, 28(sp)
        li   t1, 0
        li   t2, 10
pd:     rem  t3, a0, t2
        addi t3, t3, 48
        add  a1, sp, t1
        sb   t3, 0(a1)
        addi t1, t1, 1
        div  a0, a0, t2
        bne  a0, zero, pd
pe:     addi t1, t1, -1
        add  a1, sp, t1
        lbu  a0, 0(a1)
        sw   t1, 24(sp)
        call __putc
        lw   t1, 24(sp)
        bne  t1, zero, pe
        lw   ra, 28(sp)
        addi sp, sp, 32
        ret
"""
TDATA = "counter: .word 0\ndone: .word 0\nmutex: .word 0\nnspin: .word 0"


def thread_src(kind: str, n: int, threads: int) -> str:
    return THREAD.format(n=n, body=RACE_BODY[kind], last=threads - 1)


def _va_word(m, root, va):
    m.csr[9] = root
    e2, a2, refs, big = m.walk(va)
    return m.word(((e2 >> 12) << 12) | (va & 0xFFF))


def compute_pebble() -> dict:
    from explainer.cs.os import vmos as V
    rows = []
    for kind in ("race", "amoadd", "lock"):
        for q in (97, 500, 3000):
            th = V.threads_vm("w", thread_src(kind, 2000, 2), 2, data=TDATA)
            m = V.boot_vm(th, quantum=q)
            m.run(50_000_000)
            r = V.report_vm(m)
            spins = _va_word(m, th[0].root, th[0].labels["nspin"])
            rows.append({"kind": kind, "quantum": q, "output": bytes(m.output).decode().strip(), "steps": r["steps"],
                         "switches": r["switches"], "spins": spins, "exits": [p["exit"] for p in r["procs"]]})
    sweep = []
    for q in range(40, 3001, 40):
        th = V.threads_vm("w", thread_src("race", 2000, 2), 2, data=TDATA)
        m = V.boot_vm(th, quantum=q)
        m.run(50_000_000)
        sweep.append({"quantum": q, "count": int(bytes(m.output).decode().strip())})
    return {"rows": rows, "n": 2000, "threads": 2, "src": {k: RACE_BODY[k].strip("\n") for k in RACE_BODY},
            "sweep": sweep}


def compute_frontier() -> dict:
    from explainer.cs.conc import lin as L
    from explainer.cs.conc import mc as M
    growth = []
    for rounds in (1, 2):
        for model in ("sc", "tso", "pso"):
            t = time.time()
            r = M.explore(M.peterson("both", rounds), model, M.mutex)
            growth.append({"alg": "Peterson", "size": rounds, "model": model, "states": r.states,
                           "secs": time.time() - t})
    for n, model in ((2, "sc"), (2, "tso"), (3, "sc")):
        if True:
            t = time.time()
            r = M.explore(M.bakery(n, 1, True), model, M.mutex)
            growth.append({"alg": "bakery", "size": n, "model": model, "states": r.states, "secs": time.time() - t})
    rng = random.Random(9)
    lin = []
    cap = 300_000
    for ops in (10, 20, 30, 40, 50, 60, 70, 80):
        calls, gave_up = [], 0
        for _ in range(20):
            st = {}
            try:
                L.check(L.random_history("queue", 4, ops, rng), "queue", st, limit=cap)
                calls.append(st["calls"])
            except L.TooHard:
                gave_up += 1
                calls.append(cap)
        calls.sort()
        lin.append({"ops": ops, "median": calls[len(calls) // 2], "max": calls[-1], "gave_up": gave_up})
    return {"growth": growth, "lin": lin, "cap": cap}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
