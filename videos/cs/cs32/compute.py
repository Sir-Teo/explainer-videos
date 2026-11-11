"""Precompute everything numerical in Part 32 of *Computer Science, Built* ("Virtual Memory").

    python -m videos.cs.cs32.compute              # everything missing
    python -m videos.cs.cs32.compute --force tlb

Results are cached in ``.cache/cs32/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/os/`` (mmu.py: Pebble's MMU and TLB; vmos.py: PebbleOS with paging; paging.py: replacement, working
sets, allocators; virt.py: trap-and-emulate) and the C program below, run on this machine; tests in
tests/test_cs32_vm.py.

Items:
    sameva      two processes write their pid to the same virtual address, then read it back: each sees its own;
                the walk of that address in both page tables
    segments    base and bounds; variable partitions under first fit: external fragmentation
    tables      the size of flat and multi-level tables, 32-bit to 57-bit
    tlb         the Job as tok | job under paged PebbleOS: TLB hits and walks against TLB size, flushing or tagged
    staircase   this machine: a pointer chase over 1 to 131,072 pages, 4 KiB against 2 MiB pages; fault costs
    eat         effective access time against the fault rate
    belady      FIFO, LRU and OPT on Belady's string; random strings with the anomaly; a CLOCK sweep
    curves      every policy on the Job's page trace and on a hot-set-plus-scans trace; LRU from stack distances
    wset        the working set along the Job's trace; thrashing against the number of processes
    cow         this machine: fork with 256 MiB, then the child writes every page
    alloc       a buddy allocator under random traffic; slab against buddy for small objects
    protect     paged PebbleOS: a write to code, a wild read, a read of the kernel, a growing heap
    virt        PebbleOS unmodified on a trap-and-emulate hypervisor: exits by kind; nested-walk counts
    dirty       LRU on the Job's trace with dirty bits: evictions that must write back first
    competitive the cyclic adversary; LRU with 2h frames against OPT with h, and Sleator and Tarjan's bound
    buddyinfo   this machine's buddy free lists
    pebblevm    PebbleOS with and without paging: kernel size, the pipeline's cost, lazy against eager
    kernelmap   this machine's Meltdown status (whether its kernel needs KPTI)
    containers  this machine: a new PID namespace with unshare; this process's namespaces and cgroups
    frontier    TLB reach for real TLBs and page sizes; huge pages on the staircase
"""

from __future__ import annotations

import math
import os
import random
import subprocess
import tempfile
from pathlib import Path

from explainer.ai.cache import Cache

CACHE = Cache("cs32")
load = CACHE.load

SAMEVA = """
main:   addi sp, sp, -16
        sw   ra, 12(sp)
        li   a5, 3
        ecall                   # getpid
        la   t0, cell
        sw   a0, 0(t0)          # cell = my pid
        li   a5, 4
        ecall                   # yield: the other process writes its pid to the same address
        la   t0, cell
        lw   a0, 0(t0)          # what is there now?
        addi a0, a0, 48
        call __putc
        li   a0, 10
        call __putc
        lw   ra, 12(sp)
        addi sp, sp, 16
        li   a0, 0
        ret
"""
CELL = "cell:   .word 7"

CODEWRITE = """
main:   la   t0, main
        sw   zero, 0(t0)        # overwrite my own code
        ret
"""
WILD = """
main:   li   t0, 0x600000
        lw   t1, 0(t0)          # beyond my memory
        ret
"""
KREAD = """
main:   lw   t1, 0x100(zero)    # the kernel: mapped, but not for user mode
        ret
"""
GROWER = """
main:   addi sp, sp, -16
        sw   ra, 12(sp)
        la   t0, _heap
        li   t1, 0
        li   t2, 16
grow:   sw   t1, 0(t0)          # touch a new page
        li   t3, 4096
        add  t0, t0, t3
        addi t1, t1, 1
        blt  t1, t2, grow
        li   a0, 71             # 'G'
        call __putc
        li   a0, 10
        call __putc
        lw   ra, 12(sp)
        addi sp, sp, 16
        li   a0, 0
        ret
"""

VM_C = r"""
#define _GNU_SOURCE
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>
static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + 1e-9 * t.tv_nsec; }
static uint64_t rs = 88172645463325252ull;
static uint64_t rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static double chase(long npages, int huge) {
  size_t sz = (size_t)npages * 4096; if (sz < (2u << 20)) sz = 2u << 20;
  char *m = mmap(0, sz + (2u << 20), PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
  char *b = (char *)(((uintptr_t)m + (2u << 20) - 1) & ~((uintptr_t)(2u << 20) - 1));
  madvise(b, sz, huge ? MADV_HUGEPAGE : MADV_NOHUGEPAGE);
  memset(b, 0, sz);
  long *perm = malloc(sizeof(long) * npages);
  for (long i = 0; i < npages; i++) perm[i] = i;
  for (long i = npages - 1; i > 0; i--) { long j = rnd() % (i + 1); long t = perm[i]; perm[i] = perm[j]; perm[j] = t; }
  for (long i = 0; i < npages; i++) {
    long a = perm[i], c = perm[(i + 1) % npages];
    char **pa = (char **)(b + a * 4096 + (a % 64) * 64);
    *pa = b + c * 4096 + (c % 64) * 64;
  }
  char **p = (char **)(b + perm[0] * 4096 + (perm[0] % 64) * 64);
  long N = 4000000;
  for (long i = 0; i < N / 10; i++) p = (char **)*p;
  double t = now();
  for (long i = 0; i < N; i++) p = (char **)*p;
  double dt = now() - t;
  if (p == 0) printf("x");
  munmap(m, sz + (2u << 20)); free(perm);
  return 1e9 * dt / N;
}
int main(int argc, char **argv) {
  if (!strcmp(argv[1], "tlb")) {
    for (long n = 1; n <= 131072; n *= 2) printf("tlb %ld %.3f %.3f\n", n, chase(n, 0), chase(n, 1));
    return 0;
  }
  if (!strcmp(argv[1], "fault")) {
    size_t sz = 256u << 20;
    for (int rep = 0; rep < 3; rep++) {
      char *m = mmap(0, sz, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
      madvise(m, sz, MADV_NOHUGEPAGE);
      double t = now();
      for (size_t i = 0; i < sz; i += 4096) m[i] = 1;
      double dt = now() - t;
      t = now();
      for (size_t i = 0; i < sz; i += 4096) m[i] = 2;
      double dt2 = now() - t;
      printf("fault %.1f %.2f\n", 1e9 * dt / (sz / 4096), 1e9 * dt2 / (sz / 4096));
      munmap(m, sz);
    }
    return 0;
  }
  if (!strcmp(argv[1], "cow")) {
    size_t sz = 256u << 20;
    char *m = mmap(0, sz, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    madvise(m, sz, MADV_NOHUGEPAGE);
    memset(m, 1, sz);
    int fd[2]; if (pipe(fd)) return 1;
    double t0 = now();
    pid_t p = fork();
    if (p == 0) {
      double t = now();
      for (size_t i = 0; i < sz; i += 4096) m[i] = 2;
      double dt = now() - t;
      t = now();
      for (size_t i = 0; i < sz; i += 4096) m[i] = 3;
      double dt2 = now() - t;
      char buf[100]; int n = snprintf(buf, 100, "cow %.1f %.2f\n", 1e9 * dt / (sz / 4096), 1e9 * dt2 / (sz / 4096));
      if (write(fd[1], buf, n) < 0) _exit(1);
      _exit(0);
    }
    double fk = now() - t0;
    waitpid(p, 0, 0);
    char buf[100]; int n = read(fd[0], buf, 99); buf[n > 0 ? n : 0] = 0;
    printf("%sforkms %.2f\n", buf, 1e3 * fk);
    return 0;
  }
  return 2;
}
"""


def _exe(d):
    Path(d, "vm.c").write_text(VM_C)
    subprocess.run(["gcc", "-O2", "-o", "vm", "vm.c"], cwd=d, check=True, capture_output=True)
    return str(Path(d, "vm"))


def _meas(exe, arg):
    out = subprocess.run([exe, arg], capture_output=True, text=True, check=True).stdout
    return [ln.split() for ln in out.splitlines()]


def _cpu():
    for ln in Path("/proc/cpuinfo").read_text().splitlines():
        if ln.startswith("model name"):
            return ln.split(":", 1)[1].strip()
    return "unknown"


def _split(va):
    return {"va": va, "l1": va >> 22, "l2": (va >> 12) & 0x3FF, "off": va & 0xFFF}


# -----------------------------------------------------------------------------------------------------------------
def compute_sameva() -> dict:
    from explainer.cs.os import vmos as V
    procs = [V.user_asm_vm("P1", SAMEVA, data=CELL), V.user_asm_vm("P2", SAMEVA, data=CELL)]
    m = V.boot_vm(procs)
    m.run(1_000_000)
    va = procs[0].labels["cell"]
    walks = []
    for p in procs:
        m.csr[9] = p.root
        e1 = m.word(p.root + ((va >> 22) << 2))
        e2, a2, refs, big = m.walk(va)
        pa = ((e2 >> 12) << 12) | (va & 0xFFF)
        walks.append({"name": p.name, "root": p.root, "l2": p.l2, "e1": e1, "e2": e2, "pa": pa, "value": m.word(pa),
                      "maps": [list(x) for x in V.mappings(m, p)]})
    r = V.report_vm(m)
    return {"output": bytes(m.output).decode(), "va": va, "split": _split(va), "walks": walks,
            "report": {k: v for k, v in r.items() if k != "procs"}, "same_main": procs[0].labels["main"] ==
            procs[1].labels["main"]}


def compute_segments() -> dict:
    """Variable partitions in 1,024 units under first fit: allocate and free random segments until a request fails."""
    rng = random.Random(3)
    M = 1024
    holes = [(0, M)]
    live = []
    fails = []
    for step in range(4000):
        if live and rng.random() < 0.45:
            a, n = live.pop(rng.randrange(len(live)))
            holes.append((a, n))
            holes.sort()
            merged = []
            for h in holes:
                if merged and merged[-1][0] + merged[-1][1] == h[0]:
                    merged[-1] = (merged[-1][0], merged[-1][1] + h[1])
                else:
                    merged.append(h)
            holes = merged
            continue
        n = rng.randint(8, 96)
        for i, (a, sz) in enumerate(holes):
            if sz >= n:
                live.append((a, n))
                holes[i] = (a + n, sz - n)
                if holes[i][1] == 0:
                    holes.pop(i)
                break
        else:
            free = sum(s for _, s in holes)
            fails.append({"step": step, "want": n, "free": free, "largest": max([s for _, s in holes], default=0),
                          "holes": len(holes)})
    snap = sorted(live)
    free = sum(s for _, s in holes)
    return {"M": M, "fails": len(fails), "first_fail": fails[0] if fails else None, "live": snap, "holes": holes,
            "free": free, "largest": max([s for _, s in holes], default=0)}


def compute_tables() -> dict:
    rows = []
    for name, bits, levels, pte in (("32-bit, two levels (ours, Sv32)", 32, 2, 4), ("x86-64, four levels", 48, 4, 8),
                                    ("x86-64, five levels", 57, 5, 8)):
        flat = (2 ** (bits - 12)) * pte
        rows.append({"name": name, "bits": bits, "levels": levels, "flat_bytes": flat})
    return {"rows": rows}


def _pipeline_tape():
    from videos.cs.cs17.compute import _passages
    return _passages(n=32, lo=200, hi=90000, seed=31)[16]


def compute_tlb() -> dict:
    from explainer.cs.algo import job2 as J
    from explainer.cs.os import vmos as V
    from explainer.cs.pebble import programs as PR
    from videos.cs.cs31.compute import TOK
    t = _pipeline_tape()
    rows = []
    for size, asid, q in ((4, False, None), (8, False, None), (16, False, None), (32, False, None), (64, False, None),
                          (16, False, 500), (16, True, 500), (64, False, 500), (64, True, 500)):
        procs = [V.user_vm("tok", TOK, stdout="pipe"), V.user_vm("job", J.JOB_HASH, stdin="pipe")]
        m = V.boot_vm(procs, tape=t, tlb_size=size, **({"quantum": q} if q else {}))
        m.asid = asid
        m.run(500_000_000)
        assert bytes(m.output) == PR.job_reference(t)
        r = V.report_vm(m)
        acc = r["tlb_hits"] + r["tlb_misses"]
        rows.append({"size": size, "asid": asid, "quantum": q or 20000, "hits": r["tlb_hits"], "misses": r["tlb_misses"],
                     "miss_rate": r["tlb_misses"] / acc, "walk_refs": r["walk_refs"], "accesses": acc,
                     "flushes": r["flushes"], "page_faults": r["page_faults"], "frames": r["frames_used"],
                     "eager": r["eager_frames"], "steps": r["steps"], "switches": r["switches"]})
    return {"bytes": len(t), "rows": rows}


def compute_staircase() -> dict:
    with tempfile.TemporaryDirectory() as d:
        exe = _exe(d)
        tl = [(int(r[1]), float(r[2]), float(r[3])) for r in _meas(exe, "tlb")]
        fa = [(float(r[1]), float(r[2])) for r in _meas(exe, "fault")]
    return {"rows": tl, "fault_ns": min(f[0] for f in fa), "touch_ns": min(f[1] for f in fa), "cpu": _cpu()}


def compute_eat() -> dict:
    mem = 100e-9
    rows = []
    for p in (1e-3, 1e-4, 1e-5, 1e-6, 1e-7):
        for dev, t in (("hdd", 8e-3), ("ssd", 100e-6)):
            rows.append({"p": p, "dev": dev, "eat_ns": ((1 - p) * mem + p * t) * 1e9})
    return {"mem_ns": 100, "rows": rows}


def compute_belady() -> dict:
    from explainer.cs.os import paging as P
    s = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    table = [{"k": k, "fifo": P.faults(s, k, "fifo"), "lru": P.faults(s, k, "lru"), "opt": P.faults(s, k, "opt")}
             for k in range(1, 6)]
    rng = random.Random(5)
    found = P.anomalies(12, 5, 3, rng, trials=20000)
    rng = random.Random(6)
    found4 = P.anomalies(20, 6, 4, rng, trials=20000)
    lru_anom = 0
    rng = random.Random(7)
    for _ in range(5000):
        st = [rng.randrange(6) for _ in range(20)]
        if any(P.faults(st, k + 1, "lru") > P.faults(st, k, "lru") for k in range(1, 6)):
            lru_anom += 1
    # FIFO's frames, step by step, for 3 and 4 frames
    def fifo_steps(k):
        mem, q, out = [], [], []
        for p_ in s:
            hit = p_ in mem
            if not hit:
                if len(mem) == k:
                    mem.remove(q.pop(0))
                mem.append(p_)
                q.append(p_)
            out.append({"p": p_, "frames": list(q), "hit": hit})
        return out
    clk = []
    P._clock([1, 2, 3, 1, 4, 5, 2, 1, 6, 3], 4, 0, trace_hand=clk)
    return {"string": s, "table": table, "random_found": len(found), "random_example": found[0] if found else None,
            "random_trials": 20000, "found4": len(found4), "lru_anomalies": lru_anom, "fifo3": fifo_steps(3),
            "fifo4": fifo_steps(4), "clock": clk, "clock_string": [1, 2, 3, 1, 4, 5, 2, 1, 6, 3]}


def _job_trace(page_bits=10, writes=False):
    from explainer.cs.algo import job2 as J
    from explainer.cs.pebble.emu import Machine
    from videos.cs.cs17.compute import _passages

    class TM(Machine):
        def __post_init__(self):
            super().__post_init__()
            self.pages = []
            self.w = []

        def load(self, a, s, signed_=False):
            if a < (1 << 20):
                self.pages.append(a >> page_bits)
                self.w.append(False)
            return super().load(a, s, signed_)

        def store(self, a, s, v):
            if a < (1 << 20):
                self.pages.append(a >> page_bits)
                self.w.append(True)
            super().store(a, s, v)
    c = J.compile_job()
    t = _passages()[-12]
    m = TM(image=c.program.image, tape=t)
    m.run(200_000_000)
    tr, wr = [], []
    for p, w in zip(m.pages, m.w):
        if not tr or tr[-1] != p:
            tr.append(p)
            wr.append(w)
        elif w:
            wr[-1] = True
    if writes:
        return tr, wr, len(t), len(m.pages)
    return tr, len(t), len(m.pages)


def compute_curves() -> dict:
    from explainer.cs.os import paging as P
    tr, nbytes, raw = _job_trace()
    sizes = [2, 4, 6, 8, 12, 16, 20, 24, 32, 40]
    pol = ("opt", "lru", "fifo", "clock", "2q", "arc", "lirs", "random")
    job = {p: P.curve(tr, sizes, p) for p in pol}
    stack = P.lru_curve(tr, sizes)
    rng = random.Random(11)
    t2 = []
    for r in range(200):
        t2 += [rng.randrange(20) for _ in range(50)] + list(range(1000, 1060))
    s2 = [16, 24, 32, 48, 64, 80]
    scan = {p: P.curve(t2, s2, p) for p in pol}
    return {"job_sizes": sizes, "job": job, "job_refs": len(tr), "job_raw": raw, "job_pages": len(set(tr)),
            "job_bytes": nbytes, "stack": stack, "scan_sizes": s2, "scan": scan, "scan_refs": len(t2),
            "page_bytes": 1024}


def compute_wset() -> dict:
    from explainer.cs.os import paging as P
    tr, _, _ = _job_trace()
    ws = {str(tau): P.working_set(tr, tau)[::200] for tau in (100, 1000, 10000)}
    th = [{"n": n, "util": P.thrash(n, 64, 20)} for n in (1, 2, 3, 4, 5, 6, 8, 10)]
    return {"ws": ws, "thrash": th, "frames": 64, "wset": 20}


def compute_cow() -> dict:
    with tempfile.TemporaryDirectory() as d:
        exe = _exe(d)
        r = {x[0]: [float(v) for v in x[1:]] for x in _meas(exe, "cow")}
    return {"cow_ns": r["cow"][0], "after_ns": r["cow"][1], "fork_ms": r["forkms"][0], "mib": 256}


def compute_alloc() -> dict:
    from explainer.cs.os import paging as P
    rng = random.Random(2)
    b = P.Buddy(10)
    live = []
    series = []
    fails = 0
    for step in range(3000):
        if live and rng.random() < 0.48:
            a = live.pop(rng.randrange(len(live)))
            b.release(a)
        else:
            n = rng.choice([1, 1, 1, 2, 2, 3, 4, 5, 8, 12, 16, 30])
            a = b.malloc(n)
            if a is None:
                fails += 1
            else:
                live.append(a)
        if step % 30 == 0:
            series.append({"step": step, "free": b.free_pages(), "largest": b.largest_free()})
    # a worked split: one 3-page request into an empty 16-page pool
    w = P.Buddy(4)
    a = w.malloc(3)
    split = {k: sorted(v) for k, v in w.free.items()}
    # small objects: 72-byte objects, 10,000 of them
    n, size = 10000, 72
    buddy_bytes = n * 4096
    slab_pages = math.ceil(n / (4096 // size))
    return {"series": series, "fails": fails, "splits": b.splits, "merges": b.merges, "split_demo": split,
            "split_addr": a, "obj": size, "n": n, "buddy_bytes": buddy_bytes, "slab_bytes": slab_pages * 4096,
            "per_slab": 4096 // size}


def compute_protect() -> dict:
    from explainer.cs.os import vmos as V
    from videos.cs.cs31.compute import LETTERS
    procs = [V.user_asm_vm("good", LETTERS.format(spin=100, count=8)), V.user_asm_vm("codewrite", CODEWRITE),
             V.user_asm_vm("wild", WILD), V.user_asm_vm("grower", GROWER)]
    m = V.boot_vm(procs, quantum=3000)
    m.run(5_000_000)
    r = V.report_vm(m)
    m2 = V.boot_vm([V.user_asm_vm("kread", KREAD)])
    m2.run(100_000)
    from explainer.cs.os.machine import CAUSES
    ev = [(s, CAUSES.get(c, str(c)), pc) for s, c, pc, _ in m.events if c not in (0, 8, 16)]
    return {"output": bytes(m.output).decode(), "procs": [{k: v for k, v in p.items() if k != "regs"}
                                                          for p in r["procs"]],
            "page_faults": r["page_faults"], "events": ev, "kread_exit": V.report_vm(m2)["procs"][0]["exit"]}


def compute_virt() -> dict:
    from explainer.cs.algo import job2 as J
    from explainer.cs.os import kernel as K
    from explainer.cs.os import virt as Vt
    from explainer.cs.pebble import programs as PR
    from videos.cs.cs31.compute import LETTERS, TOK
    src = LETTERS.format(spin=40, count=24)
    n = K.boot([K.user_asm("A", src, 0), K.user_asm("B", src, 1)], quantum=900)
    n.run(5_000_000)
    v = Vt.boot_virt([K.user_asm("A", src, 0), K.user_asm("B", src, 1)], quantum=900)
    v.run(5_000_000)
    t = _pipeline_tape()
    procs = lambda: [K.user("tok", TOK, 0, stdout="pipe"), K.user("job", J.JOB_HASH, 1, stdin="pipe")]
    n2 = K.boot(procs(), tape=t)
    n2.run(500_000_000)
    v2 = Vt.boot_virt(procs(), tape=t)
    v2.run(500_000_000)
    assert bytes(v2.output) == PR.job_reference(t)
    nested = [{"n": a, "m": b, "refs": (a + 1) * (b + 1) - 1} for a, b in ((2, 2), (4, 4), (5, 5), (4, 5))]
    return {"letters": {"same": bytes(n.output) == bytes(v.output), "native_steps": n.steps, "virt_steps": v.steps,
                        "exits": v.exits, "output": bytes(v.output).decode(), "native_traps": len([e for e in n.events
                                                                                               if e[1] != 0])},
            "pipeline": {"same": bytes(n2.output) == bytes(v2.output), "native_steps": n2.steps,
                         "virt_steps": v2.steps, "exits": v2.exits, "bytes": len(t),
                         "native_traps": len([e for e in n2.events if e[1] != 0])},
            "nested": nested}


def compute_containers() -> dict:
    out = subprocess.run(["unshare", "--user", "--pid", "--fork", "--mount-proc", "--map-root-user", "sh", "-c",
                          "echo pid $$; echo uid $(id -u); ps -e -o pid,comm | head -5"], capture_output=True,
                         text=True)
    ns = sorted(os.listdir("/proc/self/ns"))
    links = {n: os.readlink(f"/proc/self/ns/{n}") for n in ns}
    cg = sorted({ln.split(":")[1] for ln in Path("/proc/self/cgroup").read_text().splitlines()
                 if ln.split(":")[1]})          # the controllers only: their paths name this sandbox
    host_pids = len([p for p in os.listdir("/proc") if p.isdigit()])
    return {"inside": out.stdout.strip().splitlines(), "ok": out.returncode == 0, "ns": links, "cgroup": cg,
            "host_pids": host_pids}


def compute_kernelmap() -> dict:
    vul = {}
    base = Path("/sys/devices/system/cpu/vulnerabilities")
    for n in ("meltdown", "spectre_v1", "spectre_v2"):
        f = base / n
        vul[n] = f.read_text().strip() if f.exists() else "unknown"
    return {"vulnerabilities": vul, "cpu": _cpu()}


def compute_pebblevm() -> dict:
    """PebbleOS with and without paging: kernel size, and the pipeline's instructions, faults and frames."""
    from explainer.cs.algo import job2 as J
    from explainer.cs.os import kernel as K
    from explainer.cs.os import vmos as V
    from explainer.cs.pebble import programs as PR
    from explainer.cs.pebble.asm import assemble
    from videos.cs.cs31.compute import TOK

    def ninstr(src):
        return assemble(src).labels["kend"] // 4
    procs = [K.user("tok", TOK, 0, stdout="pipe"), K.user("job", J.JOB_HASH, 1, stdin="pipe")]
    t = _pipeline_tape()
    n = K.boot(procs, tape=t)
    n.run(500_000_000)
    out = {"native_steps": n.steps, "bytes": len(t), "kernel": ninstr(K.kernel_source(procs)),
           "kernel_vm": ninstr(K.kernel_source(procs, vm={"nextframe": 0, "frame_end": 1}))}
    for lazy in (True, False):
        vp = [V.user_vm("tok", TOK, stdout="pipe"), V.user_vm("job", J.JOB_HASH, stdin="pipe")]
        m = V.boot_vm(vp, tape=t, lazy=lazy)
        m.run(500_000_000)
        assert bytes(m.output) == PR.job_reference(t)
        r = V.report_vm(m)
        out["lazy" if lazy else "eager"] = {"steps": m.steps, "page_faults": r["page_faults"],
                                            "frames": r["frames_used"], "eager": r["eager_frames"],
                                            "pages": {p.name: (p.hi - p.lo) // 4096 for p in vp}}
    return out


def compute_dirty() -> dict:
    """LRU on the Job's trace with dirty bits: how many evictions must first write the page back."""
    from collections import OrderedDict
    tr, wr, _, _ = _job_trace(writes=True)
    rows = []
    for k in (4, 8, 16, 24):
        mem, faults, ev, dirty = OrderedDict(), 0, 0, 0
        for p, w in zip(tr, wr):
            if p in mem:
                mem.move_to_end(p)
                mem[p] = mem[p] or w
                continue
            faults += 1
            if len(mem) == k:
                _, d = mem.popitem(last=False)
                ev += 1
                dirty += d
            mem[p] = w
        rows.append({"k": k, "faults": faults, "evictions": ev, "dirty": dirty})
    written = len({p for p, w in zip(tr, wr) if w})
    return {"rows": rows, "pages": len(set(tr)), "written_pages": written, "refs": len(tr)}


def compute_competitive() -> dict:
    """Sleator and Tarjan: the cyclic adversary, and LRU with k frames against OPT with h on the Job's trace."""
    from explainer.cs.os import paging as P
    cyc = [i % 4 for i in range(120)]
    cyclic = {p: P.faults(cyc, 3, p) for p in ("lru", "fifo", "opt")}
    tr, _, _ = _job_trace()
    rows = []
    for h in (2, 4, 8, 16):
        k = 2 * h
        lru, opt = P.faults(tr, k, "lru"), P.faults(tr, h, "opt")
        rows.append({"h": h, "k": k, "lru_k": lru, "opt_h": opt, "ratio": lru / opt, "bound": k / (k - h + 1)})
    return {"cyclic": cyclic, "cyc_len": len(cyc), "rows": rows}


def compute_buddyinfo() -> dict:
    """This machine's buddy free lists (the Normal zone): free blocks of each order."""
    rows = {}
    for ln in Path("/proc/buddyinfo").read_text().splitlines():
        f = ln.split()
        rows[f[3]] = [int(x) for x in f[4:]]
    z = rows.get("Normal") or max(rows.values(), key=sum)
    return {"zone": "Normal" if "Normal" in rows else "largest", "counts": z,
            "free_mib": [c * (4 << k) / 1024 for k, c in enumerate(z)]}


def compute_frontier() -> dict:
    rows = []
    for name, entries in (("L1 data TLB", 64), ("second-level TLB", 1536)):
        for page, label in ((4096, "4 KiB"), (2 << 20, "2 MiB"), (1 << 30, "1 GiB")):
            rows.append({"tlb": name, "entries": entries, "page": label, "reach": entries * page})
    return {"rows": rows, "memories": [("a laptop", 16 << 30), ("a large server", 4 << 40)]}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
