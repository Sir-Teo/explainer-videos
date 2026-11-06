"""Precompute everything numerical in Part 31 of *Computer Science, Built* ("The Kernel").

    python -m videos.cs.cs31.compute              # everything missing
    python -m videos.cs.cs31.compute --force sched

Results are cached in ``.cache/cs31/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/os/`` (machine.py: Pebble with a kernel mode; kernel.py: PebbleOS; sched.py, queueing.py, rt.py) and
the C programs below, run on this machine; tests in tests/test_cs31_os.py.

Items:
    boot        PebbleOS running two processes that print their letters: the interleaving and the timeline
    history     time-sharing as a closed queue: N users thinking and computing, response time against N
    protect     four processes, three misbehaving (halt, a store into the kernel, an endless loop): who survives
    trap        one getpid system call traced through the kernel, phase by phase; this machine's call, system call
                and vDSO costs; read() with buffers of 1 byte to 1 MiB; strace -c of wc
    process     the memory of the job's process, region by region; the PCB's fields
    switch      PebbleOS's yield ping-pong; a pipe ping-pong between two processes on this machine
    fork        fork, fork + exec, posix_spawn, and fork with 64 MiB to 1 GiB resident; a 25-line shell, run
    sched       FCFS's convoy, SJF, SRTF and RR on the textbook workloads; a random workload; the quantum sweep
    mlfq        MLFQ with an interactive job and two hogs; a job gaming the old rule; starvation and the boost
    share       lottery against stride at 3:1; lottery's unfairness against job length; CFS at nice 0 and 5
    smp         work stealing on a fork-join tree, 1 to 32 workers, against T1/P + Tinf
    realtime    the Liu-Layland bound; random task sets under RMS (exact) and EDF; a set RMS fails; Pathfinder
    queue       Little's law measured; M/M/1 simulated against 1/(mu - lambda); two sample paths; P-K; SRPT
    pebbleos    the Job as a pipeline, tok | job, under PebbleOS: per-process instructions on passages, the fit,
                the corpus, the timeline and the pipe's fill; ledger row 11
    frontier    tail latency on 16 cores with a bimodal service time (99.5% take 0.5 us, 0.5% take 500 us): the
                short requests' p99.9 under d-FCFS, c-FCFS, and preemption every 5 us; the quantum swept
"""

from __future__ import annotations

import json
import math
import random
import re
import subprocess
import tempfile
from pathlib import Path

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("cs31")
load = CACHE.load

TOK = r"""
// tok: the text in, one lower-case word per line out
fn main() -> int {
    var inword: int = 0;
    var c: int = getc();
    while c != -1 {
        if c >= 'A' && c <= 'Z' { c = c + 32; }
        if c >= 'a' && c <= 'z' {
            putc(c);
            inword = 1;
        } else if inword == 1 {
            putc('\n');
            inword = 0;
        }
        c = getc();
    }
    if inword == 1 { putc('\n'); }
    return 0;
}
"""

# a process that prints its letter (A for pid 1, B for pid 2, ...) `count` times, one write per letter
LETTERS = """
main:   addi sp, sp, -16
        sw   ra, 12(sp)
        li   a5, 3
        ecall                   # getpid
        addi t0, a0, 64         # 'A' - 1 + pid
        sw   t0, 0(sp)          # the byte to write
        li   s1, 0
loop:   li   t0, 0
spin:   addi t0, t0, 1          # some work
        li   t1, {spin}
        blt  t0, t1, spin
        li   a0, 1              # write(1, sp, 1)
        mv   a1, sp
        li   a2, 1
        li   a5, 2
        ecall
        addi s1, s1, 1
        li   t1, {count}
        blt  s1, t1, loop
        lw   ra, 12(sp)
        addi sp, sp, 16
        li   a0, 0
        ret
"""

HALTER = """
main:   li   t0, 7
        halt                    # privileged: only the kernel may stop the machine
        ret
"""
SCRIBBLER = """
main:   li   t0, 0x100
        li   t1, 0
        sw   t1, 0(t0)          # into the kernel's memory
        ret
"""
HOG = """
main:   li   t0, 0
hog:    addi t0, t0, 1          # never yields, never calls the kernel
        li   t1, {n}
        blt  t0, t1, hog
        li   a0, 0
        ret
"""
YIELDER = """
main:   li   s0, 0
yl:     li   a5, 4
        ecall                   # yield
        addi s0, s0, 1
        li   t1, {n}
        blt  s0, t1, yl
        li   a0, 0
        ret
"""
GETPID_ONCE = """
main:   li   a5, 3
        ecall                   # getpid
        li   a0, 0
        ret
"""

MEAS_C = r"""
#define _GNU_SOURCE
#include <fcntl.h>
#include <sched.h>
#include <spawn.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>
extern char **environ;
static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + 1e-9 * t.tv_nsec; }
__attribute__((noinline)) static long f(long x) { __asm__ volatile(""); return x + 1; }
static void pin(int cpu) { cpu_set_t s; CPU_ZERO(&s); CPU_SET(cpu, &s); sched_setaffinity(0, sizeof s, &s); }
static double best(double *v, int n) { double b = v[0]; for (int i = 1; i < n; i++) if (v[i] < b) b = v[i]; return b; }
int main(int argc, char **argv) {
  const char *mode = argv[1];
  if (!strcmp(mode, "call")) {
    long N = 20000000, s = 0; double r[5];
    for (int k = 0; k < 5; k++) { double t = now(); for (long i = 0; i < N; i++) s = f(s); r[k] = (now() - t) / N; }
    printf("call %.3f\n", 1e9 * best(r, 5));
    N = 2000000;
    for (int k = 0; k < 5; k++) { double t = now(); for (long i = 0; i < N; i++) s += syscall(SYS_getpid); r[k] = (now() - t) / N; }
    printf("getpid %.3f\n", 1e9 * best(r, 5));
    for (int k = 0; k < 5; k++) { double t = now(); for (long i = 0; i < N; i++) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); s += ts.tv_nsec; } r[k] = (now() - t) / N; }
    printf("vdso %.3f\n", 1e9 * best(r, 5));
    return s == 42;
  }
  if (!strcmp(mode, "read")) {
    int fd = open(argv[2], O_RDONLY); long total = atol(argv[3]);
    char *buf = malloc(1 << 20);
    int sizes[] = {1, 4, 16, 64, 256, 1024, 4096, 16384, 65536, 262144, 1048576};
    for (int k = 0; k < 11; k++) {
      int bs = sizes[k]; double r[3]; long calls = 0;
      for (int rep = 0; rep < 3; rep++) {
        long left = bs < 64 ? total / 16 : total; lseek(fd, 0, SEEK_SET); calls = 0;
        double t = now(); long got = 0;
        while (got < left) { long n = read(fd, buf, bs); if (n <= 0) { lseek(fd, 0, SEEK_SET); continue; } got += n; calls++; }
        r[rep] = (now() - t) / got;
      }
      printf("read %d %.4f %ld\n", bs, 1e9 * best(r, 3), calls);
    }
    return 0;
  }
  if (!strcmp(mode, "pingpong")) {
    int same = atoi(argv[2]); int N = 200000;
    int a[2], b[2]; if (pipe(a) || pipe(b)) return 1;
    pid_t p = fork();
    char c = 'x';
    if (p == 0) { pin(same ? 0 : 1); for (int i = 0; i < N; i++) { if (read(a[0], &c, 1) != 1) _exit(1); if (write(b[1], &c, 1) != 1) _exit(1); } _exit(0); }
    pin(0);
    double t = now();
    for (int i = 0; i < N; i++) { if (write(a[1], &c, 1) != 1) return 1; if (read(b[0], &c, 1) != 1) return 1; }
    double dt = now() - t; waitpid(p, 0, 0);
    printf("roundtrip %d %.1f\n", same, 1e9 * dt / N);
    return 0;
  }
  if (!strcmp(mode, "fork")) {
    int N = 2000; double r[3];
    for (int k = 0; k < 3; k++) { double t = now(); for (int i = 0; i < N; i++) { pid_t p = fork(); if (!p) _exit(0); waitpid(p, 0, 0); } r[k] = (now() - t) / N; }
    printf("fork_exit %.1f\n", 1e6 * best(r, 3));
    for (int k = 0; k < 3; k++) { double t = now(); for (int i = 0; i < N / 4; i++) { pid_t p = fork(); if (!p) { execl("/bin/true", "true", (char *)0); _exit(1); } waitpid(p, 0, 0); } r[k] = (now() - t) / (N / 4); }
    printf("fork_exec %.1f\n", 1e6 * best(r, 3));
    for (int k = 0; k < 3; k++) { double t = now(); for (int i = 0; i < N / 4; i++) { pid_t p; char *av[] = {"true", 0}; posix_spawn(&p, "/bin/true", 0, 0, av, environ); waitpid(p, 0, 0); } r[k] = (now() - t) / (N / 4); }
    printf("spawn %.1f\n", 1e6 * best(r, 3));
    int mbs[] = {0, 64, 256, 1024};
    for (int k = 0; k < 4; k++) {
      size_t sz = (size_t)mbs[k] << 20; char *mem = 0;
      if (sz) { mem = mmap(0, sz, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0); memset(mem, 1, sz); }
      int M = 200; double t = now();
      for (int i = 0; i < M; i++) { pid_t p = fork(); if (!p) _exit(0); waitpid(p, 0, 0); }
      printf("fork_mem %d %.1f\n", mbs[k], 1e6 * (now() - t) / M);
      if (sz) munmap(mem, sz);
    }
    return 0;
  }
  return 2;
}
"""

SHELL_C = r"""#include <stdio.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
static void run(char *cmd, int in, int out) {     /* in the child: wire up 0 and 1, then become cmd */
  char *argv[16]; int n = 0;
  for (char *w = strtok(cmd, " \n"); w && n < 15; w = strtok(0, " \n")) argv[n++] = w;
  argv[n] = 0;
  if (in != 0) { dup2(in, 0); close(in); }
  if (out != 1) { dup2(out, 1); close(out); }
  execvp(argv[0], argv);
  _exit(127);
}
int main(void) {
  char line[256];
  while (printf("$ "), fflush(stdout), fgets(line, sizeof line, stdin)) {
    char *bar = strchr(line, '|');
    if (!bar) { if (fork() == 0) run(line, 0, 1); wait(0); continue; }
    *bar = 0; int p[2]; if (pipe(p)) continue;
    if (fork() == 0) { close(p[0]); run(line, 0, p[1]); }
    if (fork() == 0) { close(p[1]); run(bar + 1, p[0], 1); }
    close(p[0]); close(p[1]); wait(0); wait(0);
  }
  return 0;
}
"""


def _build(d, name, src):
    Path(d, name + ".c").write_text(src)
    subprocess.run(["gcc", "-O2", "-o", name, name + ".c"], cwd=d, check=True, capture_output=True)
    return str(Path(d, name))


def _meas(exe, *args) -> list[list[str]]:
    out = subprocess.run([exe, *map(str, args)], capture_output=True, text=True, check=True).stdout
    return [ln.split() for ln in out.splitlines()]


def _full_text():
    from videos.cs.cs16.compute import _full_text as f
    return f()


def _cpu():
    for ln in Path("/proc/cpuinfo").read_text().splitlines():
        if ln.startswith("model name"):
            return ln.split(":", 1)[1].strip()
    return "unknown"


# ---------------------------------------------------------------------------------------------------------------
def compute_boot() -> dict:
    from explainer.cs.os import kernel as K
    src = LETTERS.format(spin=40, count=24)
    procs = [K.user_asm("A", src, 0), K.user_asm("B", src, 1)]
    m = K.boot(procs, quantum=900)
    m.run(5_000_000)
    tl = K.timeline(m)
    rep = K.report(m)
    att = K.attribute(m)
    # a longer quantum: the same two processes, fewer switches
    m2 = K.boot([K.user_asm("A", src, 0), K.user_asm("B", src, 1)], quantum=20_000)
    m2.run(5_000_000)
    return {"output": bytes(m.output).decode(), "output_long": bytes(m2.output).decode(), "timeline": tl,
            "steps": m.steps, "quantum": 900, "report": {k: v for k, v in rep.items() if k != "procs"},
            "attr": att, "kernel_words": rep["kernel_words"], "switches_long": K.report(m2)["switches"]}


def _closed_ps(N, Z, S, T=200_000.0, seed=1):
    """N terminals: think (exponential, mean Z), then a job (exponential, mean S) on a processor-shared CPU."""
    rng = random.Random(seed)
    t = 0.0
    thinking = sorted(rng.expovariate(1 / Z) for _ in range(N))
    jobs = {}                    # id -> [remaining, start]
    nid = 0
    resp, busy = [], 0.0
    import bisect
    while t < T:
        k = len(jobs)
        nt = thinking[0] if thinking else math.inf
        if k:
            j, r = min(jobs.items(), key=lambda kv: kv[1][0])
            nf = t + r[0] * k
        else:
            nf = math.inf
        nxt = min(nt, nf)
        if k:
            d = (nxt - t) / k
            for v in jobs.values():
                v[0] -= d
            busy += nxt - t
        t = nxt
        if nf <= nt:
            st = jobs.pop(j)[1]
            resp.append(t - st)
            bisect.insort(thinking, t + rng.expovariate(1 / Z))
        else:
            thinking.pop(0)
            jobs[nid] = [rng.expovariate(1 / S), t]
            nid += 1
    return float(np.mean(resp[200:])), busy / t, len(resp) / t


def compute_history() -> dict:
    Z, S = 10.0, 0.5
    rows = []
    for N in (1, 2, 5, 10, 15, 20, 25, 30, 40, 50, 60):
        R, U, X = _closed_ps(N, Z, S)
        rows.append({"N": N, "R": R, "U": U, "X": X, "law": N / X - Z})
    return {"Z": Z, "S": S, "rows": rows, "nstar": (S + Z) / S, "idle_one": Z / (S + Z)}


def compute_protect() -> dict:
    from explainer.cs.os import kernel as K
    from explainer.cs.pebble.asm import assemble
    from explainer.cs.pebble.emu import Machine
    good = LETTERS.format(spin=200, count=12)
    procs = [K.user_asm("good", good, 0), K.user_asm("halter", HALTER, 1), K.user_asm("scribbler", SCRIBBLER, 2),
             K.user_asm("hog", HOG.format(n=60_000), 3)]
    m = K.boot(procs, quantum=2000)
    m.run(10_000_000)
    from explainer.cs.os.machine import CAUSES
    rep = K.report(m)
    faults = [(s, CAUSES[c], pc) for s, c, pc, _ in m.events if c not in (0, 8, 16)]
    # the same halt on the bare machine: everyone stops
    bare = Machine(image=assemble("        li t0, 7\n        halt\n        li t0, 8\n").image).run(100)
    return {"output": bytes(m.output).decode(), "procs": [{k: v for k, v in p.items() if k != "regs"}
                                                          for p in rep["procs"]],
            "faults": faults, "ticks": rep["ticks"], "bare_halted_at": bare.steps,
            "report": {k: v for k, v in rep.items() if k != "procs"}}


def _phase(labels, pc):
    order = sorted(((a, n) for n, a in labels.items() if n in PHASES), key=lambda x: x[0])
    name = None
    for a, n in order:
        if pc >= a:
            name = n
    return PHASES.get(name, "kernel")


PHASES = {"trap": "save", "syscall": "dispatch", "sys_getpid": "handle", "resume": "restore",
          "bad": "dispatch", "sys_exit": "handle", "schedule": "schedule", "found": "schedule"}


def compute_trap() -> dict:
    from explainer.cs.os import kernel as K
    from explainer.cs.os.machine import ECALL, ERET
    from explainer.cs.pebble.isa import disasm
    procs = [K.user_asm("p", GETPID_ONCE, 0)]
    m = K.boot(procs, trace=True)
    m.run(100_000)
    ev = [e for e in m.events]
    i0 = next(k for k, e in enumerate(ev) if e[1] == ECALL)
    s0 = ev[i0][0]
    s1 = next(e[0] for e in ev[i0:] if e[1] == ERET)
    L = m.kernel.labels
    steps = m.log[s0:s1 + 1]
    rows = [(st.pc, disasm(st.word, st.pc, m.kernel.addr_labels), _phase(L, st.pc)) for st in steps]
    counts = {}
    for _, _, ph in rows:
        counts[ph] = counts.get(ph, 0) + 1
    src = K.kernel_source(procs)
    out = {"rows": rows, "counts": counts, "kernel_instructions": len(rows), "ecall_pc": m.log[s0 - 1].pc,
           "source_lines": len([ln for ln in src.splitlines() if ln.strip() and not ln.strip().startswith("#")])}
    with tempfile.TemporaryDirectory() as d:
        exe = _build(d, "meas", MEAS_C)
        c = {r[0]: float(r[1]) for r in _meas(exe, "call")}
        full = _full_text()
        f = Path(d, "corpus")
        f.write_bytes(full[:8 << 20])
        subprocess.run(["cat", str(f)], stdout=subprocess.DEVNULL, check=True)   # into the page cache
        reads = [(int(r[1]), float(r[2]), int(r[3])) for r in _meas(exe, "read", f, 8 << 20)]
        st = subprocess.run(["strace", "-c", "-o", str(Path(d, "s.txt")), "wc", "-w", str(f)], capture_output=True,
                            text=True)
        stxt = Path(d, "s.txt").read_text() if st.returncode == 0 else ""
    sc = []
    for ln in stxt.splitlines():
        p = ln.split()
        if len(p) >= 5 and p[0][0].isdigit() and p[-1] != "total":
            sc.append({"name": p[-1], "calls": int(p[3])})
    out.update({"call_ns": c["call"], "getpid_ns": c["getpid"], "vdso_ns": c["vdso"], "reads": reads,
                "strace": sc, "strace_total": sum(x["calls"] for x in sc), "file_bytes": 8 << 20, "cpu": _cpu()})
    return out


def compute_switch() -> dict:
    from explainer.cs.os import kernel as K
    n = 500
    procs = [K.user_asm("a", YIELDER.format(n=n), 0), K.user_asm("b", YIELDER.format(n=n), 1)]
    m = K.boot(procs)
    m.run(2_000_000)
    rep = K.report(m)
    att = K.attribute(m)
    per = att["kernel"] / rep["switches"]
    with tempfile.TemporaryDirectory() as d:
        exe = _build(d, "meas", MEAS_C)
        same = [float(_meas(exe, "pingpong", 1)[0][2]) for _ in range(3)]
        cross = [float(_meas(exe, "pingpong", 0)[0][2]) for _ in range(3)]
    return {"yields": 2 * n, "switches": rep["switches"], "kernel_per_switch": per,
            "user_per_yield": sum(att["user"].values()) / (2 * n), "trap_cycles": 35,
            "same_cpu_ns": min(same), "cross_cpu_ns": min(cross), "pcb_bytes": K.PCB, "saved_words": 15 + 1 + 2}


def compute_fork() -> dict:
    with tempfile.TemporaryDirectory() as d:
        exe = _build(d, "meas", MEAS_C)
        rows = _meas(exe, "fork")
        sh = _build(d, "sh", SHELL_C)
        r = subprocess.run([sh], input="echo hello world\necho the cat sat | tr a-z A-Z\n", capture_output=True,
                           text=True, check=True)
    v = {r_[0]: float(r_[1]) for r_ in rows if r_[0] != "fork_mem"}
    mem = [(int(r_[1]), float(r_[2])) for r_ in rows if r_[0] == "fork_mem"]
    return {"fork_exit_us": v["fork_exit"], "fork_exec_us": v["fork_exec"], "spawn_us": v["spawn"], "mem": mem,
            "shell_src": SHELL_C.strip().splitlines(), "shell_out": r.stdout, "shell_lines": len(SHELL_C.strip()
                                                                                            .splitlines())}


def compute_process() -> dict:
    """The memory of one PebbleOS process (the job), region by region, and its PCB's fields."""
    from explainer.cs.algo import job2 as J
    from explainer.cs.os import kernel as K
    p = K.user("job", J.JOB_HASH, 1, stdin="pipe")
    L = p.labels
    main = L["main"] if "main" in L else min(v for k, v in L.items() if not k.startswith("_") and k not in
                                              ("alloc",) and v > L["__out"])
    parts = [("library", p.lo, L["__in"]), ("buffers", L["__in"], L["__out"] + 4100),
             ("compiled code", L["__out"] + 4100, L["_brk"]), ("globals", L["_brk"], L["_heap"]),
             ("free", L["_heap"], p.hi - 4096), ("stack", p.hi - 4096, p.hi)]
    fields = [("state", "ready, running, blocked, exited"), ("registers", "r1 .. r15, saved at every trap"),
              ("pc", "where it resumes"), ("lo, hi", "its memory"), ("pid", "its number"),
              ("stdin, stdout", "the tape, the console, or the pipe"),
              ("counters", "dispatches, system calls, timer ticks")]
    return {"lo": p.lo, "hi": p.hi, "parts": parts, "image": len(p.image), "fields": fields, "pcb_bytes": K.PCB,
            "nproc": K.NPROC, "main": main}


def compute_sched() -> dict:
    from explainer.cs.os.sched import Job, simulate
    out = {}
    W = [Job("A", 0, [100]), Job("B", 0, [10]), Job("C", 0, [10])]
    for p in ("fcfs", "sjf"):
        r = simulate(W, p)
        out[f"convoy_{p}"] = {"segments": r.segments, "metrics": r.metrics()}
    W2 = [Job("A", 0, [100]), Job("B", 10, [10]), Job("C", 10, [10])]
    for p in ("sjf", "srtf"):
        r = simulate(W2, p)
        out[f"late_{p}"] = {"segments": r.segments, "metrics": r.metrics()}
    W3 = [Job("A", 0, [30]), Job("B", 0, [30]), Job("C", 0, [30])]
    for p, q in (("fcfs", 0), ("rr", 5)):
        r = simulate(W3, p, quantum=q or 10)
        out[f"rr_{p}"] = {"segments": r.segments, "metrics": r.metrics()}
    # a random workload: Poisson arrivals at load 0.8, exponential bursts of mean 10
    rng = random.Random(4)
    t, jobs = 0.0, []
    for k in range(400):
        t += rng.expovariate(0.08)
        jobs.append(Job(f"j{k}", int(t), [max(1, int(rng.expovariate(0.1)) + 1)]))
    rand = {}
    for p in ("fcfs", "sjf", "srtf", "rr"):
        r = simulate(jobs, p, quantum=4)
        m = r.metrics()["mean"]
        rand[p] = {"turnaround": m["turnaround"], "response": m["response"]}
    out["random"] = rand
    # the quantum: mean response time against switching overhead, one tick per switch
    sweep = []
    for q in (1, 2, 3, 5, 8, 12, 20, 30, 50, 80):
        r = simulate(jobs, "rr", quantum=q, switch=1)
        m = r.metrics()["mean"]
        busy = sum(j.bursts[0] for j in jobs)
        sweep.append({"q": q, "response": m["response"], "turnaround": m["turnaround"],
                      "overhead": r.switches / (busy + r.switches)})
    out["sweep"] = sweep
    return out


def compute_mlfq() -> dict:
    from explainer.cs.os.sched import Job, simulate
    kw = dict(quanta=(10, 20, 40), levels=3)
    inter = Job("I", 30, [1, 9] * 30 + [1])
    hogs = [Job("H1", 0, [400]), Job("H2", 0, [400])]
    r = simulate(hogs + [inter], "mlfq", track=True, **kw)
    m = r.metrics()
    basic = {"segments": r.segments[:80], "levels": {k: v[:330] for k, v in r.levels.items()},
             "resp_I": m["I"]["response"], "turn_I": m["I"]["turnaround"]}
    rr = simulate(hogs + [inter], "rr", quantum=10)
    basic["rr_turn_I"] = rr.metrics()["I"]["turnaround"]
    game = {}
    for rule in (True, False):
        J = [Job("hog", 0, [2000]), Job("gamer", 0, [9, 1] * 200)]
        g = simulate(J, "mlfq", rule4a=rule, horizon=1000, track=True, **kw)
        game["old" if rule else "new"] = {"hog": g.cpu["hog"][999], "gamer": g.cpu["gamer"][999]}
    starve = {}
    for b in (None, 200):
        J = [Job("long", 0, [300])] + [Job(f"i{k}", 0, [2, 1] * 300) for k in range(3)]
        s = simulate(J, "mlfq", boost=b, horizon=1500, track=True, rule4a=True, **kw)
        starve["none" if b is None else str(b)] = {"long": s.cpu["long"][1499], "curve": s.cpu["long"][::15]}
    return {"basic": basic, "game": game, "starve": starve, "quanta": [10, 20, 40]}


def compute_share() -> dict:
    from explainer.cs.os.sched import NICE_WEIGHT, Job, simulate
    H = 1200
    J = [Job("A", 0, [10 ** 6], tickets=300), Job("B", 0, [10 ** 6], tickets=100)]
    lot = []
    for seed in range(1, 6):
        r = simulate(J, "lottery", quantum=10, seed=seed, horizon=H, track=True)
        lot.append([r.cpu["A"][t] / (t + 1) for t in range(9, H, 10)])
    st = simulate(J, "stride", quantum=10, horizon=H, track=True)
    stride = [st.cpu["A"][t] / (t + 1) for t in range(9, H, 10)]
    # unfairness: two equal jobs of length L quanta; U = first finish / second finish (1 is fair)
    unf = []
    for L in (1, 2, 5, 10, 20, 50, 100, 200):
        us = []
        for seed in range(200):
            Jx = [Job("x", 0, [L * 10], tickets=100), Job("y", 0, [L * 10], tickets=100)]
            rr = simulate(Jx, "lottery", quantum=10, seed=seed)
            f = sorted(j.finish for j in rr.jobs)
            us.append(f[0] / f[1])
        us_s = []
        Jx = [Job("x", 0, [L * 10], tickets=100), Job("y", 0, [L * 10], tickets=100)]
        rs = simulate(Jx, "stride", quantum=10)
        f = sorted(j.finish for j in rs.jobs)
        unf.append({"L": L, "lottery": float(np.mean(us)), "stride": f[0] / f[1]})
        del us_s
    J2 = [Job("n0", 0, [10 ** 6], nice=0), Job("n5", 0, [10 ** 6], nice=5)]
    c = simulate(J2, "cfs", horizon=3000, track=True)
    J3 = [Job("a", 0, [10 ** 6]), Job("b", 0, [10 ** 6]), Job("c", 40, [10 ** 6])]
    c3 = simulate(J3, "cfs", horizon=200, track=True)
    return {"lottery": lot, "stride": stride, "unfair": unf, "cfs_n0": c.cpu["n0"][2999] / 3000,
            "cfs_n5": c.cpu["n5"][2999] / 3000, "cfs_expect": 1024 / (1024 + 335),
            "weights": {str(n): NICE_WEIGHT[n + 20] for n in (-20, -10, -5, 0, 5, 10, 19)},
            "cfs3": {"segments": c3.segments, "cpu": {k: v for k, v in c3.cpu.items()}}}


def compute_smp() -> dict:
    from explainer.cs.os.sched import fork_join, work_stealing
    T1, Ti, tree = fork_join(11, 20, seed=2)
    rows = []
    for P in (1, 2, 4, 8, 16, 32, 64):
        r = work_stealing(tree, P, seed=P)
        rows.append({"P": P, "makespan": r["makespan"], "bound": T1 / P + Ti, "speedup": T1 / r["makespan"],
                     "steals": r["steals"], "attempts": r["attempts"]})
    return {"T1": T1, "Tinf": Ti, "parallelism": T1 / Ti, "rows": rows}


def compute_realtime() -> dict:
    from explainer.cs.os import rt
    bounds = [(n, rt.ll_bound(n)) for n in range(1, 11)]
    rng = random.Random(7)
    curve = []
    for U in np.arange(0.5, 1.001, 0.05):
        ok_rta = ok_ll = 0
        trials = 400
        for _ in range(trials):
            us = rt.uunifast(4, float(U), rng)
            Ts = [rng.choice([10, 20, 25, 40, 50, 100, 125, 200]) for _ in us]
            tasks = [(max(1, round(u * T)), T) for u, T in zip(us, Ts)]
            Ureal = sum(c / t for c, t in tasks)
            ok_rta += all(r is not None for r in rt.rta(tasks)) and Ureal <= 1
            ok_ll += Ureal <= rt.ll_bound(4)
        curve.append({"U": float(U), "rms": ok_rta / trials, "ll": ok_ll / trials, "edf": 1.0})
    ts = [(2, 5), (4, 7)]
    rms = rt.schedule(ts, "rms", 35)
    edf = rt.schedule(ts, "edf", 35)
    return {"bounds": bounds, "ln2": math.log(2), "curve": curve, "tasks": ts, "U": sum(c / t for c, t in ts),
            "rms": rms, "edf": edf, "rta": rt.rta(ts), "pf_no": rt.pathfinder(False), "pf_pi": rt.pathfinder(True),
            "harmonic": rt.rta([(5, 10), (5, 20), (5, 40)])}


def compute_queue() -> dict:
    from explainer.cs.os import queueing as Q
    mm1 = []
    for rho in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.93, 0.95):
        r = Q.mg1(rho, Q.expo(1.0), n=1_000_000, seed=int(rho * 100))
        mm1.append({"rho": rho, "sim": r["mean"], "formula": 1 / (1 - rho), "p99": r["p99"], "L": r["L"],
                    "lamW": r["lam_hat"] * r["W_all"]})
    paths = {str(rho): Q.path(rho, 1.0, 300.0, seed=5) for rho in (0.5, 0.9)}
    pk = []
    for name, size, es2 in (("deterministic", Q.det(1.0), 1.0), ("exponential", Q.expo(1.0), 2.0),
                            ("hyperexponential", Q.hyper(1.0, 10.0), 11.0)):
        r = Q.mg1(0.8, size, n=400_000, seed=3)
        pk.append({"name": name, "scv": es2 - 1, "sim": r["mean"], "formula": Q.pk(0.8, 1.0, es2)})
    disc = []
    for name, size in (("exponential", Q.expo(1.0)), ("heavy-tailed", Q.pareto(1.0, 1.5, cap=1000.0))):
        row = {"name": name}
        for dsc in ("fcfs", "ps", "srpt"):
            row[dsc] = Q.mg1(0.8, size, n=150_000, discipline=dsc, seed=9)["mean"]
        disc.append(row)
    return {"mm1": mm1, "paths": paths, "pk": pk, "disc": disc}


# ---- the Job under PebbleOS: ledger row 11 ----------------------------------------------------------------
def _tokstream(t: bytes) -> bytes:
    from explainer.cs.pebble import programs as PR
    return b"".join(w + b"\n" for w in PR.job_words(t))


def _run_pipeline(t: bytes, sample: int = 0):
    from explainer.cs.algo import job2 as J
    from explainer.cs.os import kernel as K
    procs = [K.user("tok", TOK, 0, stdout="pipe"), K.user("job", J.JOB_HASH, 1, stdin="pipe")]
    m = K.boot(procs, tape=t)
    fill = []
    if sample:
        pc = m.kernel.labels["pcount"]
        while not m.halted:
            for _ in range(sample):
                m.step()
                if m.halted:
                    break
            fill.append(m.word(pc))
    else:
        m.run(2_000_000_000)
    return m, fill


def compute_pebbleos() -> dict:
    from explainer.cs.algo import job2 as J
    from explainer.cs.os import kernel as K
    from explainer.cs.pebble import programs as PR
    from videos.cs.cs17.compute import _passages
    tapes = _passages(n=32, lo=200, hi=90000, seed=31)
    samples = []
    for t in tapes:
        m, _ = _run_pipeline(t)
        assert bytes(m.output) == PR.job_reference(t)
        a = K.attribute(m)
        r = K.report(m)
        f = J.features(t)
        ts = _tokstream(t)
        samples.append({"bytes": len(t), "tok": a["user"]["tok"], "job": a["user"]["job"], "kernel": a["kernel"],
                        "traps": a["traps"], "erets": a["erets"], "switches": r["switches"], "ticks": r["ticks"],
                        "blocks": r["blocks"], "syscalls": r["syscalls"],
                        "ftok": {k: f[k] for k in ("bytes", "letters", "capitals", "words")},
                        "fjob": J.features(ts), "out": len(ts)})
    held = [i for i in range(len(samples)) if i % 4 == 2]
    train = [s for i, s in enumerate(samples) if i not in held]

    def fit(key, feat):
        mdl = J.fit([(feat(s), s[key]) for s in train])
        err = max(abs(J.predict(mdl, feat(samples[i])) - samples[i][key]) / samples[i][key] for i in held)
        return mdl, err
    m_tok, e_tok = fit("tok", lambda s: s["ftok"])
    m_job, e_job = fit("job", lambda s: s["fjob"])
    m_ker, e_ker = fit("kernel", lambda s: {"bytes": s["bytes"], "out": s["out"]})
    m_trp, e_trp = fit("traps", lambda s: {"bytes": s["bytes"], "out": s["out"]})
    full = _full_text()
    ff, out = J.features_native(full)
    assert out == PR.job_reference(full)
    ts = _tokstream(full)
    fj, out2 = J.features_native(ts)
    assert out2 == PR.job_reference(full)
    ins = {"tok": J.predict(m_tok, {k: ff[k] for k in ("bytes", "letters", "capitals", "words")}),
           "job": J.predict(m_job, fj),
           "kernel": J.predict(m_ker, {"bytes": len(full), "out": len(ts)})}
    traps = J.predict(m_trp, {"bytes": len(full), "out": len(ts)})
    led = json.loads((Cache("cs24").dir / "ledger.json").read_text())
    led = [r for r in led if r["part"] != 31]
    row8 = next(r for r in led if r["part"] == 17)
    trap_cycles = 35
    total = sum(ins.values())
    cycles = total / row8["ipc"] + row8["stall_cycles"] + 2 * traps * trap_cycles
    seconds = cycles / (row8["clock_mhz"] * 1e6)
    led.append({"part": 31, "label": r"under PebbleOS: \ tok $|$ job", "seconds": seconds, "cycles": cycles,
                "clock_mhz": row8["clock_mhz"], "instructions": total, "ipc": row8["ipc"],
                "kernel_instructions": ins["kernel"], "traps": traps})
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(led, indent=1))
    # the job alone under PebbleOS, reading the tape: the price of read() and the library alone
    one = []
    for t in tapes[-6:]:
        mm = K.boot([K.user("job", J.JOB_HASH, 0)], tape=t)
        mm.run(2_000_000_000)
        assert bytes(mm.output) == PR.job_reference(t)
        bare = J.run(J.compile_job(), t).steps
        one.append({"bytes": len(t), "os": mm.steps, "bare": bare, "kernel": K.attribute(mm)["kernel"]})
    alone_ratio = sum(o["os"] for o in one) / sum(o["bare"] for o in one)
    # a short run, drawn: the timeline and the pipe's fill
    tshort = tapes[18]
    m, fill = _run_pipeline(tshort, sample=500)
    tl = K.timeline(m)
    rep = K.report(m)
    return {"samples": samples, "errors": {"tok": e_tok, "job": e_job, "kernel": e_ker, "traps": e_trp},
            "n_train": len(train), "n_held": len(held), "bytes": len(full), "tok_bytes": len(ts),
            "instructions": ins, "total": total, "traps": traps, "cycles": cycles, "seconds": seconds,
            "row8": row8, "ledger": led, "alone": one, "alone_ratio": alone_ratio,
            "per_byte": {k: v / len(full) for k, v in ins.items()}, "row8_per_byte": row8["instructions"] / len(full),
            "short": {"bytes": len(tshort), "timeline": tl, "fill": fill, "sample": 500, "steps": m.steps,
                      "report": {k: v for k, v in rep.items() if k != "procs"},
                      "procs": [{k: v for k, v in p.items() if k != "regs"} for p in rep["procs"]]},
            "trap_cycles": trap_cycles, "kernel_words": rep["kernel_words"]}


def compute_frontier() -> dict:
    from explainer.cs.os import queueing as Q
    size = Q.bimodal(0.5, 500.0, 0.005)
    mean = 0.995 * 0.5 + 0.005 * 500.0
    c = 16
    rows = []
    for load_ in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8):
        lam = load_ * c / mean
        row = {"load": load_}
        for pol in ("dfcfs", "cfcfs"):
            row[pol] = Q.multi(lam, size, c, pol, n=200_000)["short_p999"]
        row["ps"] = Q.multi(lam, size, c, "ps", n=200_000, quantum=5.0, overhead=1.0)["short_p999"]
        rows.append(row)
    qs = []
    lam = 0.6 * c / mean
    for q in (1, 2, 5, 10, 20, 50, 100, 500):
        r = Q.multi(lam, size, c, "ps", n=200_000, quantum=float(q), overhead=1.0)
        qs.append({"q": q, "p999": r["short_p999"], "long_mean": r["long_mean"]})
    return {"rows": rows, "quanta": qs, "mean": mean, "cores": c}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
