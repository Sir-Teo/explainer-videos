"""Precompute everything numerical in Part 15 of *Computer Science, Built* ("Runtimes").

    python -m videos.cs.cs15.compute              # everything missing
    python -m videos.cs.cs15.compute --force gc

Results are cached in ``.cache/cs15/<name>.json``; scenes call ``load(name)``.  The instruments are in
``explainer/cs/runtime/``: ``bytecode`` (the λ-core compiled to a stack bytecode with flat closures), ``vm`` (the
reference VM and four collectors), ``pvm`` (the same VM in the Pebble language, run on the Pebble emulator),
``tricolor``, ``cek`` and ``prolog``; tested in tests/test_cs15_runtime.py.  Items that time real systems (CPython,
V8, the JVM, Go, C) run them on this machine and say which versions they found.

Items:
    hook       the Job in the λ-core on Pebble: words allocated, the heap filling and emptying
    interp     the Job three ways (tree-walking interpreter, bytecode VM, compiled); fib on this machine's runtimes
    scope      lexical against dynamic scope; an escaping closure; a closure-converted function
    cps        direct and CPS factorial on the VM; the Job with and without tail calls; call/cc's early exit
    vm         the Job's bytecode and opcode mix; the Pebble VM's cost per bytecode; dispatch order; C dispatch
    rc         reference-count traffic on the Job; CPython's cycles and its collector's thresholds
    tracing    a Cheney collection traced on a small heap; four collectors on the Job
    cost       collector work against heap size, measured and modelled
    gen        object lifetimes in the Job; nurseries of several sizes
    tricolor   incremental marking with and without write barriers; the scripted loss
    pauses     pause times of the JVM's collectors and Go's on this machine
    jit        V8: inline caches against shapes, hidden classes, deoptimization, tiers
    dispatch   virtual against direct calls; the cost of try and of throw (C++ on this machine)
    wasm       a hand-assembled WebAssembly module run in node; a module that fails validation
    prolog     append run backwards; unification counted
    job        the Job on the Pebble VM, priced on Part 8's core: ledger row 6, and what the collector costs
"""

from __future__ import annotations

import json
import math
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from explainer.ai.cache import Cache
from explainer.cache_lock import locked_item
from .measurements import (ObservedCheney, checked_churn_result, go_pause_events,
                           java_pause_events, measure_dispatch, positive_seconds)

SCHEMAS = {"cps": 2, "tracing": 2, "gen": 2, "pauses": 2, "dispatch": 2, "jit": 2, "rc": 2}


class RuntimeCache(Cache):
    @locked_item(lambda self, name: self.path(name))
    def load(self, name):
        if not cache_current(name, self.path(name)):
            self.save(name, ITEMS[name]())
        return super().load(name)


CACHE = RuntimeCache("cs15")


def cache_current(name, path=None):
    path = CACHE.path(name) if path is None else path
    return name not in SCHEMAS or (path.exists() and
        json.loads(path.read_text()).get("schema") == SCHEMAS[name])


def load(name):
    # Resolve at call time so cached-only QA rejects stale schemas before computation.
    return CACHE.load(name)


def _job():
    from explainer.cs.runtime import bytecode as B
    return B.job_program()


def _chapter():
    from videos.cs.cs13.compute import _chapter as ch
    return ch()


def _sh(cmd, cwd=None, env=None, timeout=600):
    r = subprocess.run(cmd, cwd=cwd, env={**os.environ, **(env or {})}, capture_output=True, text=True,
                       timeout=timeout, check=True)
    return r.stdout + r.stderr


def _version(cmd):
    try:
        lines = _sh(cmd, env={"JAVA_TOOL_OPTIONS": ""}).strip().splitlines()
        return next(l for l in lines if not l.startswith("Picked up"))
    except Exception:  # noqa: BLE001
        return "?"


# ---------------------------------------------------------------------------------------------------------------
def compute_hook() -> dict:
    from explainer.cs.pebble import programs as PR
    from explainer.cs.runtime import vm as V
    p, t = _job(), _chapter()
    h = V.Cheney(64000)
    vm = V.VM(p, h, tape=t).run()
    assert bytes(vm.output) == PR.job_reference(t)
    kinds = {}
    return {"bytes": len(t), "allocated_words": h.clock, "gcs": len(h.log), "log": h.log, "semispace": h.S,
            "ops": vm.stats["ops"], "output": bytes(vm.output).decode().splitlines(), "calls": vm.stats["calls"],
            "tailcalls": vm.stats["tailcalls"], "closures": vm.stats["closures"], "words_per_byte": h.clock / len(t),
            "peak_live": max(r["live"] for r in h.log)}


FIB = {
    "c": ("fib.c", "#include <stdio.h>\n#include <time.h>\nint fib(int n){return n<2?n:fib(n-1)+fib(n-2);}\n"
          "int main(){struct timespec a,b;clock_gettime(CLOCK_MONOTONIC,&a);volatile int r=fib(32);"
          "clock_gettime(CLOCK_MONOTONIC,&b);printf(\"%d %.6f\\n\",r,(b.tv_sec-a.tv_sec)+(b.tv_nsec-a.tv_nsec)/1e9);}"),
    "py": ("fib.py", "import time\ndef fib(n):\n    return n if n < 2 else fib(n - 1) + fib(n - 2)\n"
           "t = time.perf_counter(); r = fib(32); print(r, time.perf_counter() - t)\n"),
    "js": ("fib.js", "function fib(n){return n<2?n:fib(n-1)+fib(n-2);}\n"
           "const t=process.hrtime.bigint();const r=fib(32);console.log(r, Number(process.hrtime.bigint()-t)/1e9);"),
    "java": ("Fib.java", "public class Fib{static int fib(int n){return n<2?n:fib(n-1)+fib(n-2);}"
             "public static void main(String[] a){long t=System.nanoTime();int r=fib(32);"
             "System.out.println(r+\" \"+(System.nanoTime()-t)/1e9);}}"),
    "go": ("fib.go", "package main\nimport (\"fmt\";\"time\")\nfunc fib(n int) int { if n < 2 { return n }; "
           "return fib(n-1) + fib(n-2) }\nfunc main(){ t := time.Now(); r := fib(32); "
           "fmt.Println(r, time.Since(t).Seconds()) }\n"),
}


def compute_interp() -> dict:
    """The Job three ways on Pebble's terms, and one function on every runtime this machine has."""
    from explainer.cs.lang.lam import ml as M
    from explainer.cs.runtime import vm as V
    p, t = _job(), _chapter()
    prog = M.parse(M.JOB_ML + "\n;; job text")
    st = {}
    t0 = time.perf_counter()
    M.evaluate(prog, env={"text": M.from_list(list(t))}, stats=st)
    tree_s = time.perf_counter() - t0
    t0 = time.perf_counter()
    vm = V.VM(p, V.Cheney(64000), tape=t).run()
    vm_s = time.perf_counter() - t0
    rows = []
    with tempfile.TemporaryDirectory() as d:
        for k, (fn, src) in FIB.items():
            Path(d, fn).write_text(src)
        _sh(["gcc", "-O2", "-o", "fibc", "fib.c"], cwd=d)
        _sh(["javac", "Fib.java"], cwd=d)
        _sh(["go", "build", "-o", "fibgo", "fib.go"], cwd=d, env={"GOCACHE": str(Path(d, "gocache"))})
        runs = [
            ("C, gcc -O2 (compiled ahead of time)", ["./fibc"], "aot"),
            ("Go (compiled ahead of time)", ["./fibgo"], "aot"),
            ("Java, HotSpot (JIT)", ["java", "-Xss8m", "Fib"], "jit"),
            ("Java, -Xint (interpreter only)", ["java", "-Xint", "Fib"], "interp"),
            ("JavaScript, V8 (all tiers)", ["node", "fib.js"], "jit"),
            ("JavaScript, V8 --jitless (Ignition only)", ["node", "--jitless", "fib.js"], "interp"),
            ("Python, CPython 3.12 (bytecode interpreter)", [shutil.which("python3.12") or "python3", "fib.py"],
             "interp"),
        ]
        for name, cmd, kind in runs:
            best = None
            for _ in range(3):
                out = _sh(cmd, cwd=d, env={"JAVA_TOOL_OPTIONS": ""}).split()
                nums = [x for x in out if re.fullmatch(r"[\d.e-]+", x)]
                val, sec = int(nums[0]), positive_seconds(nums[1])
                assert val == 2178309
                best = sec if best is None else min(best, sec)
            assert val == 2178309
            rows.append({"runtime": name, "seconds": best, "kind": kind})
            print(name, best)
    versions = {"gcc": _version(["gcc", "--version"]), "java": _version(["java", "-version"]),
                "node": _version(["node", "--version"]), "go": _version(["go", "version"]),
                "python": _version([shutil.which("python3.12") or "python3", "--version"])}
    return {"tree": {"apps": st["apps"], "alloc": st["alloc"], "seconds": tree_s},
            "vm": {"ops": vm.stats["ops"], "seconds": vm_s}, "fib": rows, "fib_n": 32, "versions": versions}


SCOPE = r"""
let x = 1 ;;
let f = fun y -> x + y in
let x = 10 in
f 0
"""

ADDER = r"""
let make_adder n = let add = fun x -> x + n in add
;;
let add5 = make_adder 5 in
let add7 = make_adder 7 in
(add5 1, add7 1)
"""


def compute_scope() -> dict:
    from explainer.cs.lang.lam import ml as M
    from explainer.cs.runtime import bytecode as B
    from explainer.cs.runtime import vm as V
    src = "let f = fun y -> x + y in let x = 10 in f 0"
    lexical = M.evaluate(M.parse("let x = 1 ;; " + src))

    # dynamic scope: a function body sees the caller's variables
    def dyn(e, env):
        k = e[0]
        if k == "int":
            return e[1]
        if k == "var":
            return env[e[1]]
        if k == "fun":
            return ("dynfun", e[1], e[2])
        if k == "app":
            f, a = dyn(e[1], env), dyn(e[2], env)
            return dyn(f[2], {**env, f[1]: a})
        if k == "let":
            return dyn(e[3], {**env, e[1]: dyn(e[2], env)})
        if k == "op":
            return dyn(e[2], env) + dyn(e[3], env)
        raise ValueError(k)
    dynamic = dyn(M.parse_expr(src), {"x": 1})
    p = B.compile_program(M.parse(ADDER))
    vm = V.VM(p, V.Cheney(1000)).run()
    mem = vm.heap.mem
    res = vm.stack[vm.sp - 1] >> 1
    pair = (mem[res + 1] >> 1, mem[res + 2] >> 1)
    lam = next(f for f in p.fns if f.name.startswith("make_adder.λ"))
    return {"lexical": lexical, "dynamic": dynamic, "source": src, "adder_source": ADDER.strip().splitlines(),
            "adder": pair, "make_adder": p.listing("make_adder"), "inner": p.listing(lam.name),
            "inner_free": lam.free}


FACT = r"""
let rec fact n = if n = 0 then 1 else n * fact (n - 1)
let rec fact_cps n k = if n = 0 then k 1 else fact_cps (n - 1) (fun r -> k (n * r))
let rec fact_acc n acc = if n = 0 then acc else fact_acc (n - 1) (n * acc)
;;
"""


def compute_cps() -> dict:
    from explainer.cs.lang.lam import ml as M
    from explainer.cs.pebble import programs as PR
    from explainer.cs.runtime import bytecode as B
    from explainer.cs.runtime import cek
    from explainer.cs.runtime import vm as V
    rows = []
    for n in (10, 100, 1000):
        r = {"n": n}
        for name, body in (("direct", f"fact {n}"), ("cps", f"fact_cps {n} (fun r -> r)"),
                           ("accumulator", f"fact_acc {n} 1")):
            p = B.compile_program(M.parse(FACT + body))
            vm = V.VM(p, V.Cheney(200000)).run()
            assert vm.stack[vm.sp - 1] >> 1 == math.factorial(n)
            r[name] = {"max_stack": vm.stats["max_stack"], "closures": vm.stats["closures"],
                       "words": vm.heap.clock, "ops": vm.stats["ops"]}
        rows.append(r)
    p, t = _job(), _chapter()
    tco = {}
    for flag in (True, False):
        vm = V.VM(p, V.Cheney(1000000), tape=t, tco=flag).run()
        assert bytes(vm.output) == PR.job_reference(t)
        tco["on" if flag else "off"] = {"max_stack": vm.stats["max_stack"], "tailcalls": vm.stats.get("tailcalls", 0),
                                        "calls": vm.stats["calls"]}
    vocabulary = []
    for count in (20, 80, 200):
        tape = b" ".join(bytes((97 + i // 26, 97 + i % 26)) for i in range(count)) + b" "
        machine = V.VM(p, V.Cheney(20000), tape=tape).run()
        assert bytes(machine.output) == PR.job_reference(tape)
        vocabulary.append(dict(distinct_words=count, bytes=len(tape),
                               max_stack=machine.stats["max_stack"]))
    lst = "[3; 1; 4; 1; 0; 9; 2; 6; 5; 3; 5; 8]"
    _, plain = cek.run(M.parse(cek.PRODUCT + "product " + lst))
    _, esc = cek.run(M.parse(cek.PRODUCT + "product_exit " + lst))
    return {"schema": SCHEMAS["cps"], "fact": rows, "fact_source": FACT.strip().splitlines(),
            "tco": tco, "bytes": len(t), "vocabulary": vocabulary,
            "integer_model": "Python arbitrary-precision integers; counts are logical VM slots, not bignum storage/time",
            "product": {"list": lst, "plain": plain, "exit": esc, "source": cek.PRODUCT.strip().splitlines()}}


DISPATCH_C = r"""
#include <stdio.h>
#include <time.h>
enum { PUSH, ADD, DEC, JNZ, DUP, POP, HALT };
static const int prog[] = { PUSH, 100000000, PUSH, 0, /* loop: */ ADD, DEC, JNZ, 4, HALT };
static double now(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec / 1e9; }
long run_switch(void){
  long st[8]; int sp = 0, pc = 0;
  for (;;) {
    switch (prog[pc++]) {
      case PUSH: st[sp++] = prog[pc++]; break;
      case ADD:  st[sp-1] += st[sp-2] & 7; break;
      case DEC:  st[sp-2] -= 1; break;
      case JNZ:  { int t = prog[pc++]; if (st[sp-2]) pc = t; } break;
      case DUP:  st[sp] = st[sp-1]; sp++; break;
      case POP:  sp--; break;
      case HALT: return st[sp-1];
    }
  }
}
long run_threaded(void){
  static void *L[] = { &&push, &&add, &&dec, &&jnz, &&dup, &&pop, &&halt };
  long st[8]; int sp = 0, pc = 0;
  #define NEXT goto *L[prog[pc++]]
  NEXT;
  push: st[sp++] = prog[pc++]; NEXT;
  add:  st[sp-1] += st[sp-2] & 7; NEXT;
  dec:  st[sp-2] -= 1; NEXT;
  jnz:  { int t = prog[pc++]; if (st[sp-2]) pc = t; } NEXT;
  dup:  st[sp] = st[sp-1]; sp++; NEXT;
  pop:  sp--; NEXT;
  halt: return st[sp-1];
}
int main(void){
  double best_s = 1e9, best_t = 1e9; long a = 0, b = 0;
  for (int r = 0; r < 3; r++) {
    double t0 = now(); a = run_switch(); double t1 = now(); b = run_threaded(); double t2 = now();
    if (t1 - t0 < best_s) best_s = t1 - t0;
    if (t2 - t1 < best_t) best_t = t2 - t1;
  }
  printf("%ld %ld %.6f %.6f\n", a, b, best_s, best_t);
}
"""


def compute_vm() -> dict:
    from explainer.cs.pebble import programs as PR
    from explainer.cs.runtime import bytecode as B
    from explainer.cs.runtime import pvm
    from explainer.cs.runtime import vm as V
    from videos.cs.cs13.compute import _tapes
    p = _job()
    t = _tapes(6, 1200, 2600)[1]
    vm = V.VM(p, V.Cheney(40000), tape=t).run()
    mix = sorted(vm.ops.items(), key=lambda kv: -kv[1])
    rows = []
    for name, order in (("most frequent first", pvm.DEFAULT_ORDER), ("in opcode order", list(B.OPS)),
                        ("least frequent first", list(reversed(pvm.DEFAULT_ORDER)))):
        c = pvm.build(40000, order=order)
        m = pvm.run(c, p, t)
        assert bytes(m.output) == PR.job_reference(t)
        st = pvm.stats(m, c)
        rows.append({"order": name, "steps": m.steps, "per_bytecode": m.steps / vm.stats["ops"], **st})
        print(rows[-1])
    assert rows[0]["gcs"] == len(vm.heap.log) and rows[0]["copied"] == sum(r["work"] for r in vm.heap.log)
    with tempfile.TemporaryDirectory() as d:
        Path(d, "d.c").write_text(DISPATCH_C)
        _sh(["gcc", "-O2", "-o", "d", "d.c"], cwd=d)
        out = _sh(["./d"], cwd=d).split()
    py = _sh([shutil.which("python3.12") or "python3", "-c",
              "import dis\ndef bump(w, table):\n    if not table: return [(w, 1)]\n    p = table[0]\n"
              "    return [(w, p[1] + 1)] + table[1:] if p[0] == w else [p] + bump(w, table[1:])\ndis.dis(bump)"])
    return {"listing": p.listing("bump"), "insert": p.listing("insert"), "mix": mix, "ops": vm.stats["ops"],
            "bytes": len(t), "orders": rows, "code_size": len(p.code), "functions": len(p.fns),
            "c_dispatch": {"bytecodes": 3 * 10 ** 8, "switch": float(out[2]), "threaded": float(out[3])},
            "cpython_dis": py.strip().splitlines()[:40], "gcc": _version(["gcc", "--version"])}


CYCLES_PY = r"""
import gc, sys, time
print("threshold", gc.get_threshold())
class Node:
    pass
a = Node(); print("refcount", sys.getrefcount(a) - 1)
b = a; print("refcount", sys.getrefcount(a) - 1)
del b; print("refcount", sys.getrefcount(a) - 1)
gc.disable()
for i in range(100000):
    x = Node(); y = Node(); x.other = y; y.other = x
t = time.perf_counter(); n = gc.collect(); dt = time.perf_counter() - t
print("collected", n, dt)
gc.enable()
print("stats", gc.get_stats())
"""


def compute_rc() -> dict:
    from explainer.cs.runtime import vm as V
    p, t = _job(), _chapter()
    vm = V.VM(p, V.Cheney(1000000, track_ages=True), tape=t, count_rc=True).run()
    objs = len(vm.heap.lifetimes)
    out = {}
    for py in ("python3.12", "python3.13"):
        exe = shutil.which(py) or ("/usr/local/bin/python3" if py == "python3.13" else None)
        if not exe:
            continue
        o = _sh([exe, "-c", CYCLES_PY])
        out[py] = {"raw": o.strip().splitlines(), "version": _version([exe, "--version"])}
    return {"schema": SCHEMAS["rc"], "rc_stack": vm.stats["rc_stack"], "rc_heap": vm.stats["rc_heap"], "allocated_words": vm.heap.clock,
            "objects": objs, "ops": vm.stats["ops"], "cpython": out}


def cheney_trace():
    """Cheney on a small heap drawn in the scene: a list [1; 2; 3] held by a pair, the pair held by a root, and
    three dead objects.  Returns the objects and every event (root forwarded, object copied, slot scanned)."""
    objs = {  # name: (kind, fields), fields are names or ints
        "p": ("pair", ["c1", 7]),
        "c1": ("cons", [1, "c2"]),
        "d1": ("cons", [9, "d2"]),
        "c2": ("cons", [2, "c3"]),
        "d2": ("cons", [8, None]),
        "c3": ("cons", [3, None]),
        "k": ("closure", ["f", "d1"]),
    }
    order = list(objs)                       # from-space address order
    roots = ["p", "c2"]
    to, events, fwd = [], [], {}

    def forward(n):
        if n not in fwd:
            fwd[n] = len(to)
            to.append(n)
            events.append(("copy", n, len(to) - 1))
        return fwd[n]
    for r in roots:
        forward(r)
        events.append(("root", r))
    scan = 0
    while scan < len(to):
        n = to[scan]
        events.append(("scan", n, scan))
        for f in objs[n][1]:
            if isinstance(f, str) and f in objs:
                forward(f)
        scan += 1
    events.append(("done", len(to)))
    return {"objects": {k: [v[0], v[1]] for k, v in objs.items()}, "from_order": order, "roots": roots,
            "to_order": to, "events": events, "dead": [n for n in order if n not in fwd]}


def compute_tracing() -> dict:
    from explainer.cs.pebble import programs as PR
    from explainer.cs.runtime import vm as V
    p, t = _job(), _chapter()
    H = 128000
    rows = []
    for heap in (V.Cheney(H // 2), V.MarkSweep(H), V.MarkCompact(H), V.Generational(8192, (H - 8192) // 2)):
        t0 = time.perf_counter()
        vm = V.VM(p, heap, tape=t).run()
        assert bytes(vm.output) == PR.job_reference(t)
        log = heap.log
        rows.append({"collector": heap.name, "collections": len(log), "work": sum(r["work"] for r in log),
                     "max_pause": max(r["work"] for r in log) if log else 0,
                     "mean_pause": sum(r["work"] for r in log) / max(len(log), 1),
                     "free_blocks": max((r.get("free_blocks", 0) for r in log), default=0),
                     "moves": heap.name not in ("mark–sweep",), "seconds": time.perf_counter() - t0,
                     "allocated": heap.clock})
        print(rows[-1])
    return {"schema": SCHEMAS["tracing"], "rows": rows, "heap_words": H,
            "trace": cheney_trace(), "allocated": rows[0]["allocated"]}


def compute_cost() -> dict:
    from explainer.cs.runtime import vm as V
    p, t = _job(), _chapter()
    big = V.VM(p, V.Cheney(1000000, track_ages=False), tape=t).run()
    alloc = big.heap.clock
    # the live data over time, sampled by collecting often
    probe = V.Cheney(60000)
    V.VM(p, probe, tape=t).run()
    rows = []
    for S in (36000, 40000, 48000, 56000, 64000, 80000, 96000, 128000, 192000, 256000, 384000):
        h = V.Cheney(S)
        try:
            V.VM(p, h, tape=t).run()
        except V.OutOfMemory:
            rows.append({"semispace": S, "oom": True})
            continue
        work = sum(r["work"] for r in h.log)
        mean_live = sum(r["live"] for r in h.log) / max(len(h.log), 1)
        rows.append({"semispace": S, "collections": len(h.log), "work": work, "mean_live": mean_live,
                     "model": alloc * mean_live / (S - mean_live) if h.log else 0.0,
                     "per_word": work / alloc})
        print(rows[-1])
    ms = []
    for H in (80000, 96000, 128000, 192000, 256000, 384000, 512000):
        h = V.MarkSweep(H)
        V.VM(p, h, tape=t).run()
        ms.append({"heap": H, "collections": len(h.log), "work": sum(r["work"] for r in h.log),
                   "marked": sum(r["live"] for r in h.log)})
    peak = max(r["live"] for r in probe.log)
    return {"allocated": alloc, "rows": rows, "mark_sweep": ms, "peak_live": peak}


def compute_gen() -> dict:
    from explainer.cs.runtime import vm as V
    p, t = _job(), _chapter()
    h = ObservedCheney(40000)
    V.VM(p, h, tape=t).run()
    life = h.lifetimes
    n = len(life)
    thresholds = [0, 100, 300, 1000, 3000, 10000, 30000, 100000, 300000]
    surv = [{"age": a, "fraction": sum(1 for x in life if x > a) / n} for a in thresholds]
    rows = []
    for N in (1024, 2048, 4096, 8192, 16384, 32768):
        g = V.Generational(N, 64000)
        V.VM(p, g, tape=t).run()
        minors = [r for r in g.log if r["kind"] == "minor"]
        majors = [r for r in g.log if r["kind"] == "major"]
        rows.append({"nursery": N, "minor": len(minors), "major": len(majors),
                     "work": sum(r["work"] for r in g.log), "minor_work": sum(r["work"] for r in minors),
                     "major_work": sum(r["work"] for r in majors), "promoted": g.promoted,
                     "minor_nursery_words": sum(r["nursery_used"] for r in minors),
                     "survival": sum(r["live"] for r in minors) / max(sum(r["nursery_used"] for r in minors), 1),
                     "survival_unit": "promoted words / nursery words consumed in minor cycles",
                     "max_pause": max((r["work"] for r in g.log), default=0), "barrier_hits": g.barrier_hits})
        print(rows[-1])
    c = V.Cheney(64000 + 0)
    V.VM(p, c, tape=t).run()
    from explainer.cs.lang.lam import ml as M
    from explainer.cs.runtime import bytecode as B
    witness = ObservedCheney(1000)
    V.VM(B.compile_program(M.parse("[1; 2; 3]")), witness).run()
    return {"schema": SCHEMAS["gen"], "objects": n, "survival": surv, "rows": rows,
            "gc_interval": 40000, "observations": h.observation_summary(),
            "unobserved_live_witness": witness.observation_summary(),
            "cheney": {"work": sum(r["work"] for r in c.log), "collections": len(c.log),
                       "max_pause": max(r["work"] for r in c.log)}}


def compute_tricolor() -> dict:
    from explainer.cs.runtime import tricolor as T
    names, frames = T.scripted()
    exp = T.experiment(2000, n=50)
    return {"names": names, "frames": [[d, c, sorted(e)] for d, c, e in frames], "experiment": exp}


PAUSE_JAVA = r"""
import java.util.*;
public class Churn {
  static final class Node { long v; Node next; Node(long v, Node n){ this.v = v; this.next = n; } }
  public static void main(String[] a) {
    Node[] live = new Node[200000];                 // a live set of ~200k short lists
    Random r = new Random(15);
    long t = System.nanoTime(), sum = 0;
    for (int i = 0; i < 60_000_000; i++) {
      int k = r.nextInt(live.length);
      live[k] = new Node(i, (i & 7) == 0 ? null : live[k]);   // mostly young garbage, some survivors
      sum += live[k].v;
    }
    System.out.println(sum + " " + (System.nanoTime() - t) / 1e9);
  }
}
"""

PAUSE_GO = r"""
package main
import ("fmt"; "math/rand"; "time")
type Node struct { v int; next *Node }
func main() {
  live := make([]*Node, 200000)
  r := rand.New(rand.NewSource(15))
  t := time.Now(); sum := 0
  for i := 0; i < 60000000; i++ {
    k := r.Intn(len(live))
    var n *Node
    if i&7 != 0 { n = live[k] }
    live[k] = &Node{i, n}
    sum += live[k].v
  }
  fmt.Println(sum, time.Since(t).Seconds())
}
"""


def compute_pauses() -> dict:
    rows = []
    with tempfile.TemporaryDirectory() as directory:
        Path(directory, "Churn.java").write_text(PAUSE_JAVA)
        _sh(["javac", "Churn.java"], cwd=directory, env={"JAVA_TOOL_OPTIONS": ""})
        for name, flags in (("Serial", ["-XX:+UseSerialGC"]), ("Parallel", ["-XX:+UseParallelGC"]),
                            ("G1", ["-XX:+UseG1GC"]),
                            ("ZGC (generational)", ["-XX:+UseZGC", "-XX:+ZGenerational"])):
            command = ["java", "-Xmx1g", "-Xms1g", "-XX:ActiveProcessorCount=4", *flags,
                       "-Xlog:gc,gc+phases:stdout", "Churn"]
            raw = _sh(command, cwd=directory, env={"JAVA_TOOL_OPTIONS": ""})
            seconds = checked_churn_result(raw)
            events = java_pause_events(raw)
            values = [event["ms"] for event in events]
            rows.append(dict(collector="JVM " + name, pauses=len(values), max_ms=max(values),
                             mean_ms=sum(values)/len(values), total_pause_ms=sum(values),
                             seconds=seconds, command=command, events=events, raw_log=raw))
            print({k:v for k,v in rows[-1].items() if k not in ('raw_log','events')})
        Path(directory, "churn.go").write_text(PAUSE_GO)
        _sh(["go", "build", "-o", "churn", "churn.go"], cwd=directory,
            env={"GOCACHE": str(Path(directory, "gocache"))})
        settings = dict(GODEBUG="gctrace=1", GOGC="100", GOMEMLIMIT="1GiB", GOMAXPROCS="4")
        raw = _sh(["./churn"], cwd=directory, env=settings)
        seconds = checked_churn_result(raw)
        events = go_pause_events(raw)
        values = [event["ms"] for event in events]
        rows.append(dict(collector="Go (concurrent mark–sweep)", pauses=len(values), max_ms=max(values),
                         mean_ms=sum(values)/len(values), total_pause_ms=sum(values), seconds=seconds,
                         settings=settings, events=events, raw_log=raw))
        print({k:v for k,v in rows[-1].items() if k not in ('raw_log','events')})
    return dict(schema=SCHEMAS["pauses"], rows=rows, java=_version(["java", "-version"]),
                go=_version(["go", "version"]),
                workload="60 million allocations; 200,000 list heads; JVM fixed 1 GiB; Go GOGC=100, soft limit 1 GiB",
                scope="One host/run per configuration; Go and JVM heap policies differ. "
                      "Go events count the two STW phases separately; concurrent work/assists are excluded.")


JIT_JS = r"""
function getX(o) { return o.x; }
function make(k, i) {           // k different shapes: the same x, different other properties first
  const o = {};
  for (let j = 0; j < k; j++) o["p" + j] = j;
  o.x = i;
  return o;
}
function bench(shapes) {
  const objs = [];
  for (let i = 0; i < 1024; i++) objs.push(make(i % shapes, i));
  let s = 0;
  const t = process.hrtime.bigint();
  for (let r = 0; r < 20000; r++) for (let i = 0; i < 1024; i++) s += getX(objs[i]);
  return [s, Number(process.hrtime.bigint() - t) / 1e9];
}
const out = [];
for (const k of [1, 2, 4, 8, 16, 32]) { bench(k); const [s, t] = bench(k); out.push([k, t, s]); }
console.log(JSON.stringify(out));
"""

SHAPES_JS = r"""
const a = {x: 1, y: 2}, b = {x: 3, y: 4}, c = {y: 5, x: 6};
const d = {x: 1}; d.y = 2;
console.log(JSON.stringify({ab: %HaveSameMap(a, b), ac: %HaveSameMap(a, c), ad: %HaveSameMap(a, d)}));
"""

DEOPT_JS = r"""
function add(a, b) { return a + b; }
let s = 0;
for (let i = 0; i < 200000; i++) s += add(i, 1);
console.log(add("a", "b"));
for (let i = 0; i < 200000; i++) s += add(i, 1);
console.log(s);
"""

TIERS_JS = r"""
function fib(n) { return n < 2 ? n : fib(n - 1) + fib(n - 2); }
const t = process.hrtime.bigint();
const r = fib(32);
console.log(r, Number(process.hrtime.bigint() - t) / 1e9);
"""


def compute_jit() -> dict:
    with tempfile.TemporaryDirectory() as d:
        for fn, src in (("ic.js", JIT_JS), ("shapes.js", SHAPES_JS), ("deopt.js", DEOPT_JS), ("tiers.js", TIERS_JS)):
            Path(d, fn).write_text(src)
        ic = json.loads(_sh(["node", "ic.js"], cwd=d).strip().splitlines()[-1])
        assert [r[0] for r in ic] == [1, 2, 4, 8, 16, 32]
        for _, seconds, checksum in ic:
            positive_seconds(seconds)
            assert checksum == 20000 * 1024 * 1023 // 2
        shapes = json.loads(_sh(["node", "--allow-natives-syntax", "shapes.js"], cwd=d).strip().splitlines()[-1])
        deopt = _sh(["node", "--trace-deopt", "deopt.js"], cwd=d)
        deopt_values = [line for line in deopt.splitlines() if line == "ab" or line.isdigit()]
        assert deopt_values == ["ab", "40000200000"], deopt_values
        dl = [l.strip() for l in deopt.splitlines() if "bailout" in l or "deoptimiz" in l.lower()]
        tiers = _sh(["node", "--trace-opt", "tiers.js"], cwd=d)
        tl = [l.strip() for l in tiers.splitlines() if "fib" in l and ("compiling" in l or "completed" in l)]
        ladder = []
        for name, flags in (("Ignition (interpreter)", ["--jitless"]),
                            ("+ Sparkplug (baseline)", ["--no-maglev", "--no-turbofan"]),
                            ("+ Maglev (mid-tier)", ["--no-turbofan"]), ("+ TurboFan (optimizing)", [])):
            best = None
            for _ in range(3):
                out = _sh(["node", *flags, "tiers.js"], cwd=d).split()
                assert out[0] == "2178309", out
                dt = positive_seconds(out[1])
                best = dt if best is None else min(best, dt)
            ladder.append({"tier": name, "seconds": best})
            print(ladder[-1])
    return {"schema": SCHEMAS["jit"],
            "ic": [{"shapes": k, "seconds": t, "checksum": checksum} for k, t, checksum in ic],
            "ic_calls": 20000 * 1024, "shapes": shapes, "deopt": dl[:12],
            "deopt_values": deopt_values, "deopt_raw": deopt,
            "tiers_trace": tl[:12], "ladder": ladder, "node": _version(["node", "--version"])}


DISPATCH_CPP = '#include <chrono>\n#include <cstdint>\n#include <cstdio>\n#include <csetjmp>\n#include <stdexcept>\n#ifndef N\n#define N 20000000\n#endif\n#ifndef M\n#define M 100000\n#endif\n#define OPAQUE __attribute__((noipa))\nusing Word = std::uint64_t;\nstruct Shape { virtual Word area(Word x) const = 0; virtual ~Shape() {} };\nstruct Sq : Shape { OPAQUE Word area(Word x) const override { return x*x; } };\nstruct Tri : Shape { OPAQUE Word area(Word x) const override { return x*x/2; } };\nOPAQUE Word direct(Word x) { return x*x; }\nOPAQUE Word plain(Word x) { return x+1; }\nOPAQUE Word may_throw(Word x, bool fail) { if(fail) throw std::runtime_error("x"); return x+1; }\nextern "C" OPAQUE Word run_virtual(Shape **table) {\n  Word sum=0; for(Word i=0; i<N; ++i) sum += table[i&1]->area(i); return sum;\n}\nstatic std::jmp_buf jump_env;\nstatic volatile Word sink;\ntemplate<class F> void measure(const char *name, Word iterations, F body) {\n  double best=1e100; Word checksum=0;\n  for(int r=0; r<3; ++r) {\n    auto a=std::chrono::steady_clock::now(); Word value=body();\n    auto b=std::chrono::steady_clock::now(); sink=value;\n    double elapsed=std::chrono::duration<double>(b-a).count();\n    if(elapsed<best) { best=elapsed; checksum=value; }\n  }\n  std::printf("%s %.9f %llu %llu\\n",name,best,\n              (unsigned long long)checksum,(unsigned long long)iterations);\n}\nint main() {\n  Sq sq; Tri tri; Shape *one[]={&sq,&sq}, *two[]={&sq,&tri};\n  measure("direct",N,[]{ Word s=0; for(Word i=0;i<N;++i) s+=direct(i); return s; });\n  measure("virtual_mono",N,[&]{ return run_virtual(one); });\n  measure("virtual_poly",N,[&]{ return run_virtual(two); });\n  measure("plain",N,[]{ Word s=0; for(Word i=0;i<N;++i) s+=plain(i); return s; });\n  measure("try",N,[]{ Word s=0; for(Word i=0;i<N;++i) { try { s+=may_throw(i,false); } catch(...) { --s; } } return s; });\n  measure("setjmp",N/10,[]{ Word s=0; for(Word i=0;i<N/10;++i) { if(setjmp(jump_env)==0) s+=plain(i); else --s; } return s; });\n  measure("throw",M,[]{ Word s=0; for(Word i=0;i<M;++i) { try { s+=may_throw(i,true); } catch(...) { --s; } } return s; });\n}\n'


def compute_dispatch() -> dict:
    return dict(schema=SCHEMAS["dispatch"],
                **measure_dispatch(_sh, DISPATCH_CPP, _version(["g++", "--version"])))


def _leb(n):
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if (n == 0 and not b & 0x40) or (n == -1 and b & 0x40):
            out.append(b)
            return bytes(out)
        out.append(b | 0x80)


def _vec(items):
    return _leb(len(items)) + b"".join(items)


def _section(k, body):
    return bytes([k]) + _leb(len(body)) + body


def wasm_module(body: bytes) -> bytes:
    """One function, (i64) -> i64, exported as "fact"."""
    types = _vec([b"\x60" + _vec([b"\x7e"]) + _vec([b"\x7e"])])
    funcs = _vec([b"\x00"])
    exports = _vec([_leb(4) + b"fact" + b"\x00\x00"])
    code = _vec([_leb(len(b"\x00" + body + b"\x0b")) + b"\x00" + body + b"\x0b"])
    return b"\x00asm\x01\x00\x00\x00" + _section(1, types) + _section(3, funcs) + _section(7, exports) + \
        _section(10, code)


FACT_WASM = bytes([0x20, 0, 0x50, 0x04, 0x7E, 0x42, 1, 0x05, 0x20, 0, 0x20, 0, 0x42, 1, 0x7D, 0x10, 0, 0x7E, 0x0B])
BAD_WASM = bytes([0x20, 0, 0x50, 0x04, 0x7E, 0x42, 1, 0x05, 0x20, 0, 0x7E, 0x0B])   # i64.mul with one operand
FACT_WAT = """(module
  (func $fact (export "fact") (param $n i64) (result i64)
    local.get $n
    i64.eqz
    if (result i64)
      i64.const 1
    else
      local.get $n
      local.get $n
      i64.const 1
      i64.sub
      call $fact
      i64.mul
    end))"""
BAD_WAT = """    else
      local.get $n
      i64.mul        ;; needs two i64s: only one is there
    end"""

WASM_JS = r"""
const fs = require("fs");
const good = fs.readFileSync("good.wasm"), bad = fs.readFileSync("bad.wasm");
const out = {valid_good: WebAssembly.validate(good), valid_bad: WebAssembly.validate(bad)};
const inst = new WebAssembly.Instance(new WebAssembly.Module(good));
out.fact20 = inst.exports.fact(20n).toString();
try { new WebAssembly.Module(bad); } catch (e) { out.error = String(e.message); }
console.log(JSON.stringify(out));
"""


def compute_wasm() -> dict:
    good, bad = wasm_module(FACT_WASM), wasm_module(BAD_WASM)
    with tempfile.TemporaryDirectory() as d:
        Path(d, "good.wasm").write_bytes(good)
        Path(d, "bad.wasm").write_bytes(bad)
        Path(d, "w.js").write_text(WASM_JS)
        res = json.loads(_sh(["node", "w.js"], cwd=d).strip().splitlines()[-1])
    return {"bytes": list(good), "size": len(good), "wat": FACT_WAT.splitlines(), "bad_wat": BAD_WAT.splitlines(),
            "node": _version(["node", "--version"]), **res}


def compute_prolog() -> dict:
    from explainer.cs.runtime import prolog as P
    ans, st = P.solve(P.PROGRAM_APPEND, ("append", "X", "Y", P.plist([1, 2, 3])))
    fwd, st2 = P.solve(P.PROGRAM_APPEND, ("append", P.plist([1, 2]), P.plist([3]), "Z"))
    return {"program": P.PROGRAM_APPEND_TEXT.splitlines(),
            "backwards": [[P.unlist(a["X"]), P.unlist(a["Y"])] for a in ans], "stats": st,
            "forwards": P.unlist(fwd[0]["Z"]), "stats_fwd": st2}


def compute_job() -> dict:
    """Row 6: the Job in the λ-core, run by the Pebble VM (with Cheney's collector) on six passages, priced like
    row 5 at row 3's cost per hand-written cycle; the collector's share measured by rerunning with a heap so large
    that it never collects."""
    from explainer.cs.pebble import programs as PR
    from explainer.cs.runtime import pvm
    from explainer.cs.runtime import vm as V
    from videos.cs.cs8.compute import core
    from videos.cs.cs13.compute import _tapes
    p = _job()
    c = pvm.build(40000)
    big = pvm.build(260000)                 # never collects on these passages; needs 2 MiB, so a bigger memory
    j13 = json.loads((Cache("cs13").dir / "job.json").read_text())
    hand = {r["bytes"]: r for r in j13["core"]}
    rows = []
    for t in _tapes(6, 1200, 2600):
        m = pvm.run(c, p, t)
        assert bytes(m.output) == PR.job_reference(t)
        st = pvm.stats(m, c)
        m2 = pvm.run(big, p, t, mem_size=1 << 22)
        st2 = pvm.stats(m2, big)
        assert st2["gcs"] == 0
        vm = V.VM(p, V.Cheney(40000), tape=t).run()
        rows.append({"bytes": len(t), "steps": m.steps, "steps_nogc": m2.steps, "gcs": st["gcs"],
                     "copied": st["copied"], "bytecodes": vm.stats["ops"], "words": vm.heap.clock,
                     "hand_cycles": hand[len(t)]["hand"], "hand_instr": hand[len(t)]["hand_instr"],
                     "o2_cycles": hand[len(t)]["O2"]})
        print(rows[-1])
    # instructions per cycle of the VM's own code on the out-of-order core, from a short passage
    short = _tapes(6, 1200, 2600)[1][:400]
    q = core(c.program.image, p.encode() + short)
    assert bytes(q.output) == PR.job_reference(short)
    ipc = q.committed / q.cycles
    steps = sum(r["steps"] for r in rows)
    vm_cycles = steps / ipc
    ratio = vm_cycles / sum(r["hand_cycles"] for r in rows)
    gc_share = 1 - sum(r["steps_nogc"] for r in rows) / steps
    led = json.loads((Cache("cs13").dir / "ledger.json").read_text())[:6]
    row3, row5 = led[3], led[5]
    led.append({"part": 15, "label": r"the $\lambda$-core, collected", "seconds": row3["seconds"] * ratio,
                "cycles": row3["cycles"] * ratio, "clock_mhz": row3["clock_mhz"], "ratio_to_row3": ratio,
                "ratio_to_row5": ratio / row5["ratio_to_row3"], "gc_share": gc_share})
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(led, indent=1))
    return {"rows": rows, "ipc": ipc, "ipc_sample": {"bytes": len(short), "cycles": q.cycles,
                                                     "instructions": q.committed},
            "ratio": ratio, "gc_share": gc_share, "ledger": led,
            "per_bytecode": steps / sum(r["bytecodes"] for r in rows)}


ITEMS = {
    "hook": compute_hook, "interp": compute_interp, "scope": compute_scope, "cps": compute_cps, "vm": compute_vm,
    "rc": compute_rc, "tracing": compute_tracing, "cost": compute_cost, "gen": compute_gen,
    "tricolor": compute_tricolor, "pauses": compute_pauses, "jit": compute_jit, "dispatch": compute_dispatch,
    "wasm": compute_wasm, "prolog": compute_prolog, "job": compute_job,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
