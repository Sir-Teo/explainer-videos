"""Precompute everything numerical in Part 11 of *Computer Science, Built* ("The Running Program").

    python -m videos.cs.cs11.compute              # everything missing
    python -m videos.cs.cs11.compute --force heap

Results are cached in ``.cache/cs11/<name>.json``; scenes call ``load(name)``.  Pebble's side is
``explainer/cs/pebble/link.py`` (object files, the linker, the loader), ``jobv1.py`` (the Job in four linked files),
``heap.py`` (allocators on traces) and ``smash.py`` (the stack smash), tested in tests/test_cs11_link.py and
tests/test_cs11_running.py.  This machine's side compiles small C programs with the system gcc and reads them with
readelf and objdump; those numbers belong to whatever computer runs this file.

Items:
    tools      gcc, readelf and the C library on this machine
    layout     endianness, and the size and padding of three structs, compiled here
    switch     a dense switch compiled by gcc -O2: the jump table
    stack      recursive Pebble programs (factorial, Ackermann, a sum and its tail-call version): depth and calls
    ackermann  ack(2, n) and ack(3, n): calls and the deepest stack
    heap       a real allocation trace (Perl counting the words of Pride and Prejudice, recorded with LD_PRELOAD)
               run through first fit, next fit, best fit, segregated fits and the buddy system
    fifty      Knuth's fifty-percent rule, by simulation: holes against blocks, and p / 2
    robson     an adversary that makes any allocator's heap grow like M (1/2 log2 n + 1) (Robson)
    elf        two C files compiled here: sections, symbols, relocations (readelf), and the linked program
    pebblelink the same story on Pebble: two object files, every relocation patched
    dynamic    static against dynamic linking here: sizes, imported functions, start-up time; interposition
    aslr       one program run three times: where main, a global, the heap and the stack land
    maps       a process's address space (/proc/self/maps)
    ub         signed overflow and a null check, at -O0 and -O2
    smash      the Pebble stack smash: the attack, a canary, a no-execute stack
    job        the Job in four linked files with frames and a heap list, against JOB_V0
    frontier   a capability (CHERI-style) machine catching the overflow; Robson's bound at scale
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
import time
from pathlib import Path

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("cs11")
load = CACHE.load


def _sh(cmd, **kw) -> str:
    return subprocess.run(cmd, shell=isinstance(cmd, str), check=True, capture_output=True, text=True, **kw).stdout


def compute_tools() -> dict:
    return {"gcc": _sh("gcc --version").splitlines()[0], "readelf": _sh("readelf --version").splitlines()[0],
            "libc": _sh("ldd --version").splitlines()[0]}


# ---------------------------------------------------------------------------
# data in memory
# ---------------------------------------------------------------------------
LAYOUT_C = r"""
#include <stdio.h>
#include <stddef.h>
#include <stdint.h>
struct a { char c; int i; char d; };          /* as written */
struct b { int i; char c; char d; };          /* the same fields, largest first */
struct node { struct node *next; char *letters; int length; int count; };   /* the Job's list node */
int main(void) {
  uint32_t x = 0x0A0B0C0D; unsigned char *p = (unsigned char *)&x;
  printf("%02x %02x %02x %02x\n", p[0], p[1], p[2], p[3]);
  printf("%zu %zu %zu %zu\n", sizeof(struct a), offsetof(struct a, c), offsetof(struct a, i), offsetof(struct a, d));
  printf("%zu %zu %zu %zu\n", sizeof(struct b), offsetof(struct b, i), offsetof(struct b, c), offsetof(struct b, d));
  printf("%zu %zu %zu %zu %zu\n", sizeof(struct node), offsetof(struct node, next), offsetof(struct node, letters),
         offsetof(struct node, length), offsetof(struct node, count));
  return 0;
}
"""


def _cc_run(src: str, flags=("-O2",), args=()) -> str:
    with tempfile.TemporaryDirectory() as d:
        c, exe = Path(d) / "m.c", Path(d) / "m"
        c.write_text(src)
        subprocess.run(["gcc", *flags, "-o", str(exe), str(c)], check=True)
        return subprocess.run([str(exe), *map(str, args)], check=True, capture_output=True, text=True).stdout


def compute_layout() -> dict:
    out = _cc_run(LAYOUT_C).split("\n")
    return {"bytes": out[0].split(), "a": list(map(int, out[1].split())), "b": list(map(int, out[2].split())),
            "node": list(map(int, out[3].split()))}


SWITCH_C = r"""
void up(void), down(void), left(void), right(void), fire(void), jump(void), quit(void), help(void);
void key(int c) {
  switch (c) {
  case 0: up(); break;    case 1: down(); break;  case 2: left(); break;  case 3: right(); break;
  case 4: fire(); break;  case 5: jump(); break;  case 6: quit(); break;  case 7: help(); break;
  }
}
"""


def compute_switch() -> dict:
    with tempfile.TemporaryDirectory() as d:
        c = Path(d) / "s.c"
        c.write_text(SWITCH_C)
        asm = _sh(["gcc", "-O2", "-fno-asynchronous-unwind-tables", "-fcf-protection=none", "-S", "-o", "-", str(c)])
    lines = [l.rstrip() for l in asm.splitlines() if l.strip() and not l.strip().startswith((".file", ".ident",
                                                                                              ".section .note"))]
    body = [l for l in lines if not l.strip().startswith((".globl", ".type", ".size", ".p2align", ".text"))]
    return {"asm": body, "table": any("jmp\t*" in l or "notrack jmp" in l for l in body),
            "source": SWITCH_C.strip()}


# ---------------------------------------------------------------------------
# the stack
# ---------------------------------------------------------------------------
REC = {
    "fact": """
        li   a0, 10
        call fact
        halt
fact:   addi sp, sp, -16      # fact(n) = n * fact(n - 1)
        sw   ra, 12(sp)
        sw   a0, 8(sp)
        li   t0, 2
        blt  a0, t0, base
        addi a0, a0, -1
        call fact
        lw   t0, 8(sp)
        mul  a0, a0, t0
        j    fdone
base:   li   a0, 1
fdone:  lw   ra, 12(sp)
        addi sp, sp, 16
        ret
""",
    "sum": """
        li   a0, 100
        li   a1, 0
        call sum
        halt
sum:    addi sp, sp, -16      # sum(n, acc): calls itself, then returns
        sw   ra, 12(sp)
        beqz a0, sdone0
        add  a1, a1, a0
        addi a0, a0, -1
        call sum
        j    sret
sdone0: mv   a0, a1
sret:   lw   ra, 12(sp)
        addi sp, sp, 16
        ret
""",
    "sum_tail": """
        li   a0, 100
        li   a1, 0
        call sum
        halt
sum:    beqz a0, done         # the tail call made a jump: no frame, a flat stack
        add  a1, a1, a0
        addi a0, a0, -1
        j    sum
done:   mv   a0, a1
        ret
""",
}

ACK = """
        li   a0, {m}
        li   a1, {n}
        call ack
        halt
ack:    addi sp, sp, -16
        sw   ra, 12(sp)
        sw   a0, 8(sp)
        bnez a0, a1z
        addi a0, a1, 1
        j    adone
a1z:    bnez a1, rec
        addi a0, a0, -1
        li   a1, 1
        call ack
        j    adone
rec:    addi a1, a1, -1
        call ack
        mv   a1, a0
        lw   a0, 8(sp)
        addi a0, a0, -1
        call ack
adone:  lw   ra, 12(sp)
        addi sp, sp, 16
        ret
"""


def _stack_trace(src: str, keep: bool = True, limit: int = 50_000_000, mem: int = 1 << 20):
    from explainer.cs.pebble import assemble
    from explainer.cs.pebble.emu import Machine

    m = Machine(image=assemble(src).image, mem_size=mem)
    top = m.regs[2]
    depth = []
    calls = deepest = 0
    while not m.halted and m.steps < limit:
        w = m.word(m.pc)
        if (w >> 26) == 31 and ((w >> 22) & 15) == 1:
            calls += 1
        m.step()
        d = top - m.regs[2]
        deepest = max(deepest, d)
        if keep:
            depth.append(d)
    return {"result": m.regs[3], "deepest": deepest, "calls": calls, "steps": m.steps,
            "depth": depth if keep else None}


def compute_stack() -> dict:
    out = {}
    for k, src in REC.items():
        out[k] = _stack_trace(src)
        out[k]["source"] = src
    out["ackermann"] = _stack_trace(ACK.format(m=2, n=3))
    out["ackermann"]["source"] = ACK.format(m=2, n=3)
    return out


def compute_ackermann() -> dict:
    rows = []
    for m_, ns in ((1, range(1, 6)), (2, range(1, 6)), (3, range(1, 7))):
        for n in ns:
            r = _stack_trace(ACK.format(m=m_, n=n), keep=False, mem=1 << 22)
            rows.append({"m": m_, "n": n, "value": r["result"], "calls": r["calls"], "frames": r["deepest"] // 16})
            print(rows[-1])
    return {"rows": rows}


# ---------------------------------------------------------------------------
# the heap: a real trace, and five allocators
# ---------------------------------------------------------------------------
MTRACE_C = r"""
#define _GNU_SOURCE
#include <dlfcn.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
static void *(*real_malloc)(size_t), *(*real_calloc)(size_t, size_t), *(*real_realloc)(void *, size_t);
static void (*real_free)(void *);
static int fd = -1, busy;
static char boot[1 << 16]; static size_t boot_used;
struct rec { uint8_t op; uint64_t a, b, c; } __attribute__((packed));
static void put(uint8_t op, uint64_t a, uint64_t b, uint64_t c) {
  if (fd < 0 || busy) return; busy = 1; struct rec r = {op, a, b, c}; if (write(fd, &r, sizeof r) < 0) {} busy = 0; }
static void init(void) {
  if (real_malloc) return;
  real_malloc = dlsym(RTLD_NEXT, "malloc"); real_calloc = dlsym(RTLD_NEXT, "calloc");
  real_realloc = dlsym(RTLD_NEXT, "realloc"); real_free = dlsym(RTLD_NEXT, "free");
  const char *p = getenv("MTRACE_OUT");
  if (p) { char name[512]; snprintf(name, sizeof name, "%s.%d", p, getpid()); fd = open(name, O_WRONLY | O_CREAT | O_TRUNC, 0644); } }
void *malloc(size_t n) { if (!real_malloc) { init(); if (!real_malloc) { void *q = boot + boot_used; boot_used += (n + 15) & ~15; return q; } }
  void *p = real_malloc(n); put('m', (uint64_t)p, n, 0); return p; }
void *calloc(size_t k, size_t n) { if (!real_calloc) { void *q = boot + boot_used; boot_used += (k * n + 15) & ~15; memset(q, 0, k * n); return q; }
  void *p = real_calloc(k, n); put('c', (uint64_t)p, k * n, 0); return p; }
void *realloc(void *o, size_t n) { init(); void *p = real_realloc(o, n); put('r', (uint64_t)p, n, (uint64_t)o); return p; }
void free(void *p) { if ((char *)p >= boot && (char *)p < boot + sizeof boot) return; init(); put('f', (uint64_t)p, 0, 0); real_free(p); }
__attribute__((constructor)) static void ctor(void) { init(); }
"""

PERL = r"for (split) { $c{lc $_}++ } END { print scalar(keys %c), qq(\n) }"


def record_trace() -> Path:
    """Record Perl counting the words of Pride and Prejudice, every malloc and free, with an interposed malloc."""
    import videos.ai.ai1.compute as A

    out = CACHE.dir / "perl.mtrace"
    if out.exists():
        return out
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    book = A.BOOK_DIR / "1342.txt"
    with tempfile.TemporaryDirectory() as d:
        so = Path(d) / "mtrace.so"
        src = Path(d) / "mtrace.c"
        src.write_text(MTRACE_C)
        subprocess.run(["gcc", "-O2", "-shared", "-fPIC", "-o", str(so), str(src), "-ldl"], check=True)
        env = dict(os.environ, MTRACE_OUT=str(Path(d) / "tr"), LD_PRELOAD=str(so))
        subprocess.run(["perl", "-ne", PERL, str(book)], check=True, env=env, capture_output=True)
        f = next(Path(d).glob("tr.*"))
        out.write_bytes(f.read_bytes())
    return out


def compute_heap() -> dict:
    from explainer.cs.pebble import heap as H

    tr = H.read_mtrace(record_trace())
    ev = H.events(tr)
    sizes = [e[2] for e in ev if e[0] == "a"]
    hist = {}
    for s in sizes:
        b = 1 << max(0, (max(s, 1) - 1).bit_length())
        hist[b] = hist.get(b, 0) + 1
    # live bytes over time, sampled
    live = 0
    req = {}
    series = []
    for k, e in enumerate(ev):
        if e[0] == "a":
            req[e[1]] = e[2]
            live += e[2]
        else:
            live -= req.pop(e[1])
        if k % max(1, len(ev) // 400) == 0:
            series.append([k, live])
    rows = []
    for A in (H.FirstFit, H.NextFit, H.BestFit, H.Segregated, H.Buddy):
        r = H.simulate(ev, A())
        rows.append({"name": r.name, "peak_live": r.peak_live, "peak_heap": r.peak_heap,
                     "fragmentation": r.fragmentation, "steps": r.steps / r.allocs})
        print(rows[-1])
    return {"records": len(tr), "allocs": len(sizes), "frees": sum(1 for e in ev if e[0] == "f"), "hist": hist,
            "series": series, "rows": rows, "program": "perl -ne '" + PERL + "' 1342.txt"}


def compute_fifty() -> dict:
    import random
    import statistics as st

    from explainer.cs.pebble import heap as H

    class Counting(H.FirstFit):
        def __init__(self):
            super().__init__()
            self.splits = self.whole = self.ext = 0

        def after_split(self, i):
            self.splits += 1

        def after_take(self, i):
            self.whole += 1

        def malloc(self, n):
            t = self.top
            a = super().malloc(n)
            if self.top != t:
                self.ext += 1
            return a

    rows = []
    for N in (200, 1000, 3000):
        rng = random.Random(2)
        A = Counting()
        live = [A.malloc(rng.randint(16, 2000)) for _ in range(N)]
        A.splits = A.whole = A.ext = 0
        holes, blocks = [], []
        for t in range(40000):
            A.free(live.pop(rng.randrange(len(live))))
            live.append(A.malloc(rng.randint(16, 2000)))
            if t > 10000 and t % 50 == 0:
                holes.append(len(A.addrs))
                blocks.append(len(A.used))
        p = A.splits / (A.splits + A.whole + A.ext)
        rows.append({"N": N, "holes": st.mean(holes), "blocks": st.mean(blocks), "ratio": st.mean(holes) /
                     st.mean(blocks), "p": p})
    return {"rows": rows, "sizes": [16, 2000]}


def compute_robson() -> dict:
    import bisect

    from explainer.cs.pebble import heap as H

    def adversary(Alloc, M_units=4096, phases=8, U=32):
        A = Alloc()
        M = M_units * U
        live = {}
        s = 1
        out = []
        for k in range(phases):
            size = s * U
            while sum(live.values()) + size <= M:
                a = A.malloc(size - 8)
                live[a] = A.used[a]
            nxt = 2 * size
            for a in sorted(live):
                if sum(live.values()) <= M // 2:
                    break
                n = live[a]
                left = right = 0
                i = bisect.bisect_left(A.addrs, a)
                if i > 0 and A.addrs[i - 1] + A.size[A.addrs[i - 1]] == a:
                    left = A.size[A.addrs[i - 1]]
                if i < len(A.addrs) and A.addrs[i] == a + n:
                    right = A.size[A.addrs[i]]
                if left + n + right < nxt:
                    A.free(a)
                    del live[a]
            out.append({"phase": k, "block": size, "heap_over_M": A.top / M, "bound": 1 + k / 2})
            s *= 2
        return out

    return {"first_fit": adversary(H.FirstFit), "best_fit": adversary(H.BestFit), "M_units": 4096}


# ---------------------------------------------------------------------------
# object files and linking, on this machine and on Pebble
# ---------------------------------------------------------------------------
ELF_MAIN = r"""
#include <stdio.h>
extern int count(const char *s);       /* defined in lib.c */
extern int total;                      /* a global from lib.c */
static int calls;                      /* local to this file: .bss */
const char *greeting = "hello";        /* initialised data: .data, pointing into .rodata */
int main(void) {
  calls++;
  int n = count(greeting);
  printf("%d %d\n", n, total);
  return 0;
}
"""
ELF_LIB = r"""
int total = 0;                          /* global, zero: .bss (a strong definition) */
int __attribute__((weak)) verbose;      /* weak */
int count(const char *s) { int n = 0; while (*s++) n++; total += n; return n; }
"""


def _readelf_sections(path) -> list[dict]:
    out = _sh(["readelf", "-SW", str(path)])
    rows = []
    for l in out.splitlines():
        m = re.match(r"\s*\[\s*(\d+)\]\s+(\S+)\s+(\S+)\s+([0-9a-f]+)\s+([0-9a-f]+)\s+([0-9a-f]+)", l)
        if m and m.group(2) != "NULL" and m.group(2) != "":
            rows.append({"name": m.group(2), "type": m.group(3), "size": int(m.group(6), 16)})
    return rows


def _readelf_symbols(path) -> list[dict]:
    out = _sh(["readelf", "-sW", str(path)])
    rows = []
    for l in out.splitlines():
        p = l.split()
        if len(p) >= 8 and p[0].endswith(":") and p[0][:-1].isdigit():
            rows.append({"value": p[1], "size": int(p[2]), "type": p[3], "bind": p[4], "ndx": p[6], "name": p[7]})
    return rows


def _readelf_relocs(path) -> list[dict]:
    out = _sh(["readelf", "-rW", str(path)])
    rows = []
    sec = None
    for l in out.splitlines():
        m = re.match(r"Relocation section '(\S+)'", l)
        if m:
            sec = m.group(1)
            continue
        p = l.split()
        if len(p) >= 5 and re.fullmatch(r"[0-9a-f]{8,16}", p[0]):
            rows.append({"section": sec, "offset": p[0], "type": p[2], "symbol": p[4] if len(p) > 4 else ""})
    return rows


def compute_elf() -> dict:
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "main.c").write_text(ELF_MAIN)
        (d / "lib.c").write_text(ELF_LIB)
        for f in ("main", "lib"):
            subprocess.run(["gcc", "-O2", "-fno-asynchronous-unwind-tables", "-c", "-o", str(d / f"{f}.o"),
                            str(d / f"{f}.c")], check=True)
        subprocess.run(["gcc", "-o", str(d / "prog"), str(d / "main.o"), str(d / "lib.o")], check=True)
        run = _sh([str(d / "prog")]).strip()
        out = {}
        for f in ("main", "lib"):
            o = d / f"{f}.o"
            out[f] = {"sections": _readelf_sections(o), "symbols": _readelf_symbols(o), "relocs": _readelf_relocs(o),
                      "bytes": o.stat().st_size}
        prog = d / "prog"
        syms = {s["name"]: s["value"] for s in _readelf_symbols(prog) if s["name"] in ("main", "count", "total",
                                                                                      "greeting", "calls")}
        # an undefined reference, and a duplicate strong symbol
        errs = {}
        for name, files in (("undefined", ["main.o"]), ("duplicate", ["main.o", "lib.o", "lib.o"])):
            r = subprocess.run(["gcc", "-o", str(d / "bad"), *[str(d / f) for f in files]], capture_output=True,
                               text=True)
            errs[name] = [l.split(": ", 1)[-1] for l in r.stderr.splitlines() if "undefined" in l or "multiple" in l][:2]
        return {"objects": out, "run": run, "linked_symbols": syms, "errors": errs,
                "sources": {"main.c": ELF_MAIN.strip(), "lib.c": ELF_LIB.strip()}}


def compute_pebblelink() -> dict:
    from explainer.cs.pebble import jobv1
    from explainer.cs.pebble.link import LinkError, assemble_object, link

    objs, exe = jobv1.build()

    def obj_view(o):
        return {"name": o.name, "text": len(o.sections[".text"]), "data": len(o.sections[".data"]), "bss": o.bss_size,
                "defined": [[s.name, s.section, s.offset, s.binding] for s in o.defined().values()
                            if s.binding != "local" or s.name in ("head", "tail", "brk", "heap")],
                "undefined": o.undefined(),
                "relocs": [[r.section, r.offset, r.kind, r.symbol] for r in o.relocs]}

    errors = {}
    try:
        link([o for o in objs if o.name != "alloc.o"])
    except LinkError as e:
        errors["undefined"] = str(e)
    try:
        link(objs + [assemble_object(jobv1.ALLOC_S, "alloc2.o")])
    except LinkError as e:
        errors["duplicate"] = str(e)
    return {"objects": [obj_view(o) for o in objs], "layout": exe.layout, "symbols": exe.symbols,
            "patches": exe.patches, "entry": exe.entry, "bss": exe.bss, "image": len(exe.image), "errors": errors}


HELLO_C = r"""
#include <stdio.h>
int main(void) { puts("hello"); return 0; }
"""


def compute_dynamic() -> dict:
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "h.c").write_text(HELLO_C)
        out = {}
        for kind, flags in (("dynamic", []), ("static", ["-static"])):
            exe = d / f"h_{kind}"
            r = subprocess.run(["gcc", "-O2", *flags, "-o", str(exe), str(d / "h.c")], capture_output=True, text=True)
            if r.returncode:
                out[kind] = {"error": r.stderr[:300]}
                continue
            t = []
            for _ in range(5):
                t0 = time.perf_counter()
                for _ in range(100):
                    subprocess.run([str(exe)], stdout=subprocess.DEVNULL, check=True)
                t.append((time.perf_counter() - t0) / 100)
            needed = re.findall(r"\(NEEDED\).*\[(.+)\]", _sh(["readelf", "-d", str(exe)]))
            plt = [r_["symbol"] for r_ in _readelf_relocs(exe) if r_["section"] and "plt" in r_["section"]]
            out[kind] = {"bytes": exe.stat().st_size, "start_ms": 1000 * min(t), "needed": needed, "plt": plt}
        out["ldd"] = [l.strip() for l in _sh(["ldd", str(d / "h_dynamic")]).splitlines()]
        return out


ADDR_C = r"""
#include <stdio.h>
#include <stdlib.h>
int global = 1;
int main(void) {
  int local = 2; void *heap = malloc(16);
  printf("%p %p %p %p %p\n", (void *)main, (void *)&global, heap, (void *)&local, (void *)printf);
  return 0;
}
"""


def compute_aslr() -> dict:
    with tempfile.TemporaryDirectory() as d:
        c, exe = Path(d) / "a.c", Path(d) / "a"
        c.write_text(ADDR_C)
        subprocess.run(["gcc", "-O2", "-o", str(exe), str(c)], check=True)
        runs = [_sh([str(exe)]).split() for _ in range(3)]
        # without ASLR (setarch -R), if the system allows it
        try:
            fixed = [_sh(["setarch", os.uname().machine, "-R", str(exe)]).split() for _ in range(2)]
        except Exception:  # noqa: BLE001
            fixed = None
    return {"names": ["main", "global", "heap", "stack", "printf"], "runs": runs, "fixed": fixed}


MAPS_C = r"""
#include <stdio.h>
#include <stdlib.h>
int main(void) {
  void *p = malloc(1 << 20); (void)p;
  FILE *f = fopen("/proc/self/maps", "r"); char line[512];
  while (fgets(line, sizeof line, f)) fputs(line, stdout);
  return 0;
}
"""


def compute_maps() -> dict:
    out = _cc_run(MAPS_C, flags=("-O2",))
    rows = []
    for l in out.splitlines():
        p = l.split(None, 5)
        lo, hi = (int(x, 16) for x in p[0].split("-"))
        rows.append({"lo": lo, "hi": hi, "perms": p[1], "name": p[5].strip() if len(p) > 5 else ""})
    return {"rows": rows}


UB_C = r"""
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
__attribute__((noinline)) int bigger(int x) { return x + 1 > x; }
__attribute__((noinline)) int deref(int *p) { int v = *p; if (!p) return -1; return v; }
int main(int argc, char **argv) {
  volatile int m = INT_MAX;
  printf("%d\n", bigger(m));
  long n = 0; for (int i = atoi(argv[1]); i > 0; i += 1000000000) n++;
  printf("%ld\n", n);
  return 0;
}
"""


def compute_ub() -> dict:
    out = {}
    with tempfile.TemporaryDirectory() as d:
        c = Path(d) / "u.c"
        c.write_text(UB_C)
        for name, flags in (("O0", ["-O0"]), ("O2", ["-O2"]), ("O2 -fwrapv", ["-O2", "-fwrapv"])):
            exe = Path(d) / "u"
            subprocess.run(["gcc", *flags, "-o", str(exe), str(c)], check=True)
            r = _sh([str(exe), "1"]).split()
            asm = _sh(["gcc", *flags, "-fno-asynchronous-unwind-tables", "-fcf-protection=none", "-S", "-o", "-",
                       str(c)])
            body = asm.split("deref:")[1].split("\t.size")[0] if "deref:" in asm else ""
            ins = [l.strip() for l in body.splitlines() if l.startswith("\t") and not l.strip().startswith(".")]
            out[name] = {"bigger": int(r[0]), "loop": int(r[1]), "deref_asm": ins}
    return out


# ---------------------------------------------------------------------------
# Pebble: the smash, the Job, a capability machine
# ---------------------------------------------------------------------------
def compute_smash() -> dict:
    from explainer.cs.pebble import smash as S

    exe = S.build()
    benign = S.run(exe, b"Ada\n")
    tape = S.exploit(exe)
    attack = S.run(exe, tape)
    exe_c = S.build(canary=True)
    canary = S.run(exe_c, S.exploit(exe_c))
    nx = S.run(exe, tape, nx=True)
    return {"benign": benign, "attack": attack, "canary": canary, "nx": nx, "payload": list(tape),
            "buffer": S.frame_sp(exe), "frame": S.FRAME, "ra_off": S.RA_OFF, "source": S.source(),
            "shellcode": S.SHELLCODE}


def compute_job() -> dict:
    from explainer.cs.pebble import assemble
    from explainer.cs.pebble import jobv1
    from explainer.cs.pebble import programs as P
    from explainer.cs.pebble.emu import run
    from explainer.cs.pebble.link import load as pload
    from videos.cs.cs6.compute import novels

    objs, exe = jobv1.build()
    pp = novels()[1342]
    i = pp.index("It is a truth universally acknowledged")
    j = pp.index("Mr. Bennet was among the earliest")
    chapter = pp[i:j].rstrip()
    rows = []
    for name, text in (("a paragraph", chapter[:chapter.index("\n", 600)]), ("chapter 1", chapter),
                       ("20,000 bytes", pp[5000:25000])):
        tape = P.job_tape(text)
        m = pload(exe, tape=tape)
        top = m.regs[2]
        deepest = 0
        while not m.halted:
            m.step()
            deepest = max(deepest, top - m.regs[2])
        v0 = run(assemble(P.JOB_V0), tape=tape)
        rows.append({"name": name, "bytes": len(tape), "same": bytes(m.output) == P.job_reference(tape),
                     "v1": m.steps, "v0": v0.steps, "stack": deepest, "output": bytes(m.output).decode()})
        print(rows[-1]["name"], rows[-1]["same"], rows[-1]["v1"], rows[-1]["v0"])
    return {"rows": rows, "files": {k: v.strip("\n") for k, v in jobv1.FILES.items()},
            "objects": [{"name": o.name, "text": len(o.sections[".text"]), "relocs": len(o.relocs)} for o in objs]}


def compute_frontier() -> dict:
    """A capability machine in miniature (the idea of CHERI): every pointer register carries the bounds of the
    object it was derived from, set where the object is created; a store outside them traps.  Here greet's buffer
    gets bounds [sp, sp + 64) when its address is taken (``mv a0, sp`` at greet's call to gets), and they travel with
    the pointer through ``addi``; the attack's 65th byte traps, before the return address is touched."""
    from explainer.cs.pebble import smash as S
    from explainer.cs.pebble.emu import Machine, MachineError
    from explainer.cs.pebble.isa import decode

    class CapMachine(Machine):
        def step(self):
            ins = decode(self.word(self.pc))
            cap = getattr(self, "cap", {})
            self.cap = cap
            if ins.op == "addi" and ins.rs1 == 2 and ins.rd == 3 and ins.imm == 0 and self.pc == self.buf_pc:
                cap[3] = (self.regs[2], self.regs[2] + 64)  # the buffer's capability
            elif ins.op == "addi" and ins.rs1 in cap:
                cap[ins.rd] = cap[ins.rs1]
            elif ins.op in ("sb", "sw") and ins.rs1 in cap:
                lo, hi = cap[ins.rs1]
                a = (self.regs[ins.rs1] + ins.imm) & 0xFFFF_FFFF
                if not lo <= a < hi:
                    raise MachineError(f"capability fault: store to {a:#x} outside [{lo:#x}, {hi:#x})")
            elif ins.op not in ("beq", "bne", "blt", "bge", "bltu", "bgeu", "jal", "jalr", "sb", "sw") and \
                    ins.rd in cap:
                cap.pop(ins.rd, None)  # any other write to the register drops its capability
            return super().step()

    from explainer.cs.pebble.link import assemble_object, load as pload

    exe = S.build()
    obj = assemble_object(S.source(), "greet.o")
    # the `mv a0, sp` in greet: the first addi a0, sp, 0 after greet's label
    pc = obj.symbols["greet"].offset
    while True:
        ins = decode(int.from_bytes(exe.image[pc:pc + 4], "little"))
        if ins.op == "addi" and ins.rs1 == 2 and ins.rd == 3 and ins.imm == 0:
            break
        pc += 4
    tape = S.exploit(exe)
    m = pload(exe, tape=tape)
    m.__class__ = CapMachine
    m.buf_pc = pc
    fault = None
    try:
        while not m.halted and m.steps < 100_000:
            m.step()
    except MachineError as e:
        fault = str(e)
    benign = pload(exe, tape=b"Ada\n")
    benign.__class__ = CapMachine
    benign.buf_pc = pc
    benign.run()
    return {"attack": {"output": bytes(m.output).decode("latin-1"), "fault": fault},
            "benign": bytes(benign.output).decode(), "robson": [{"n": n, "factor": 0.5 * np.log2(n) + 1}
                                                                 for n in (2 ** k for k in range(1, 21, 3))]}


# ---------------------------------------------------------------------------
# practice: a debugger's backtrace, static archives and link order, sanitizers
# ---------------------------------------------------------------------------
BT_C = r"""
#include <stdio.h>
#include <stdlib.h>
long fact(long n) {
  if (n <= 1) return 1;
  return n * fact(n - 1);
}
int main(int argc, char **argv) {
  printf("%ld\n", fact(argc > 1 ? atol(argv[1]) : 5));
  return 0;
}
"""


def compute_backtrace() -> dict:
    """gdb stops fact(5) at its deepest call and walks the frames, printing each frame's stack pointer."""
    with tempfile.TemporaryDirectory() as d:
        c, exe = Path(d) / "fact.c", Path(d) / "fact"
        c.write_text(BT_C)
        subprocess.run(["gcc", "-O0", "-g", "-fno-omit-frame-pointer", "-o", str(exe), str(c)], check=True)
        cmds = ["-ex", "set pagination off", "-ex", "break fact if n == 1", "-ex", "run", "-ex", "bt"]
        for k in range(6):
            cmds += ["-ex", f"frame {k}", "-ex", "p/x $sp", "-ex", "p/x *(long *)($rbp + 8)"]
        out = subprocess.run(["gdb", "-q", "-batch", "-nx", *cmds, str(exe)], capture_output=True, text=True).stdout
    bt = [l for l in out.splitlines() if l.startswith("#")]
    vals = [l.split("=", 1)[1].strip() for l in out.splitlines() if l.startswith("$")]
    sps = [int(v, 16) for v in vals[0::2]]
    ras = [int(v, 16) for v in vals[1::2]]
    seen, frames = set(), []
    for line in bt:
        k = int(line.split()[0][1:])
        if k in seen:
            continue
        seen.add(k)
        frames.append(line)
    return {"bt": frames[:6], "sp": sps[:6], "ra": ras[:6], "frame_bytes": sps[1] - sps[0] if len(sps) > 1 else None,
            "source": BT_C.strip()}


AR_MAIN = "int count(const char *s);\nint main(void) { return count(\"hello\") == 5 ? 0 : 1; }\n"
AR_COUNT = "int count(const char *s) { int n = 0; while (*s++) n++; return n; }\n"
AR_UNUSED = "static char table[100000] = {1};\nint unused(int i) { return table[i]; }\n"


def compute_archive() -> dict:
    """A static library is an archive of object files; the linker pulls in a member only if it resolves a symbol
    that is undefined at that point of its left-to-right scan."""
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        for n, src in (("main", AR_MAIN), ("count", AR_COUNT), ("unused", AR_UNUSED)):
            (d / f"{n}.c").write_text(src)
            subprocess.run(["gcc", "-O2", "-c", "-o", str(d / f"{n}.o"), str(d / f"{n}.c")], check=True)
        subprocess.run(["ar", "rcs", str(d / "libjob.a"), str(d / "count.o"), str(d / "unused.o")], check=True)
        members = _sh(["ar", "t", str(d / "libjob.a")]).split()
        res = {}
        for name, order in (("objects", ["main.o", "count.o", "unused.o"]), ("archive", ["main.o", "libjob.a"]),
                            ("archive first", ["libjob.a", "main.o"])):
            exe = d / "p"
            r = subprocess.run(["gcc", "-o", str(exe), *[str(d / f) for f in order]], capture_output=True, text=True)
            row = {"order": order, "ok": r.returncode == 0,
                   "error": [l.split(": ", 1)[-1] for l in r.stderr.splitlines() if "undefined" in l][:1]}
            if r.returncode == 0:
                syms = _sh(["nm", str(exe)])
                row.update(bytes=exe.stat().st_size, has_count=" count\n" in syms, has_unused=" unused\n" in syms)
                exe.unlink()
            res[name] = row
    return {"members": members, "links": res}


SAN = {
    "overflow": ("-fsanitize=undefined", r"""
#include <limits.h>
#include <stdio.h>
int main(int argc, char **argv) { int x = INT_MAX - 1 + argc; printf("%d\n", x + 1); return 0; }
"""),
    "heap": ("-fsanitize=address", r"""
#include <stdlib.h>
int main(void) { int *a = malloc(16 * sizeof(int)); for (int i = 0; i <= 16; i++) a[i] = i; free(a); return 0; }
"""),
    "freed": ("-fsanitize=address", r"""
#include <stdlib.h>
int main(void) { int *a = malloc(16 * sizeof(int)); free(a); return a[3]; }
"""),
    "stack": ("-fsanitize=address", r"""
#include <string.h>
int main(void) { char buf[64]; for (int i = 0; i <= 64; i++) buf[i] = 'A'; return buf[3]; }
"""),
}

SAN_BENCH = r"""
#include <stdio.h>
#include <stdlib.h>
struct node { struct node *next; long v; };
int main(void) {
  long total = 0;
  for (int round = 0; round < 40; round++) {
    struct node *head = 0;
    for (long i = 0; i < 200000; i++) { struct node *n = malloc(sizeof *n); n->v = i; n->next = head; head = n; }
    while (head) { struct node *n = head; total += n->v; head = n->next; free(n); }
  }
  printf("%ld\n", total);
  return 0;
}
"""


SAN_WORDS = r"""
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 65536
static char *key[N]; static int cnt[N];
int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "rb"); fseek(f, 0, SEEK_END); long n = ftell(f); rewind(f);
  char *t = malloc(n + 1); fread(t, 1, n, f); t[n] = 0; fclose(f);
  long words = 0; int distinct = 0;
  for (int rep = 0; rep < 20; rep++)
    for (long i = 0; i < n;) {
      while (i < n && !isalpha((unsigned char)t[i])) i++;
      long s = i; unsigned h = 2166136261u;
      while (i < n && isalpha((unsigned char)t[i])) { h = (h ^ (unsigned char)tolower(t[i])) * 16777619u; i++; }
      if (i == s) break;
      int len = i - s; words++;
      for (unsigned j = h & (N - 1);; j = (j + 1) & (N - 1)) {
        if (!key[j]) { key[j] = malloc(len + 1); for (int k = 0; k < len; k++) key[j][k] = tolower(t[s + k]);
                       key[j][len] = 0; cnt[j] = 1; distinct++; break; }
        if ((int)strlen(key[j]) == len && !strncasecmp(key[j], t + s, len)) { cnt[j]++; break; }
      }
    }
  printf("%ld %d\n", words, distinct);
  return 0;
}
"""


def compute_sanitize() -> dict:
    import resource
    import videos.ai.ai1.compute as A

    out = {}
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        for name, (flag, src) in SAN.items():
            c, exe = d / f"{name}.c", d / name
            c.write_text(src)
            subprocess.run(["gcc", "-O0", "-g", flag, "-o", str(exe), str(c)], check=True)
            r = subprocess.run([str(exe)], capture_output=True, text=True,
                               env={**os.environ, "ASAN_OPTIONS": "detect_leaks=0"})
            lines = [l for l in r.stderr.splitlines() if "ERROR" in l or "runtime error" in l or "located" in l]
            first = lines[0] if lines else ""
            if "ERROR: AddressSanitizer:" in first:
                first = first.split("ERROR: AddressSanitizer: ", 1)[1].split(" on address")[0]
            elif "runtime error:" in first:
                first = first.split("runtime error: ", 1)[1]
            loc = next((l.strip() for l in lines if "located" in l), "")
            out[name] = {"report": first, "where": loc, "exit": r.returncode}
        book = str(A.BOOK_DIR / "1342.txt")
        bench = {}
        for bname, src, args in (("words", SAN_WORDS, [book]), ("malloc", SAN_BENCH, [])):
            c = d / f"{bname}.c"
            c.write_text(src)
            times = {}
            for name, flags in (("plain", []), ("asan", ["-fsanitize=address"])):
                exe = d / f"{bname}_{name}"
                subprocess.run(["gcc", "-O2", *flags, "-o", str(exe), str(c)], check=True)
                best = None
                for _ in range(5):
                    t0 = time.perf_counter()
                    r = subprocess.run([str(exe), *args], check=True, capture_output=True, text=True,
                                       env={**os.environ, "ASAN_OPTIONS": "detect_leaks=0"})
                    dt = time.perf_counter() - t0
                    best = dt if best is None else min(best, dt)
                times[name] = best
                times[name + "_out"] = r.stdout.strip()
            bench[bname] = {**times, "slowdown": times["asan"] / times["plain"]}
    return {"cases": out, "bench": bench}


ITEMS = {
    "tools": compute_tools, "layout": compute_layout, "switch": compute_switch, "stack": compute_stack,
    "ackermann": compute_ackermann, "heap": compute_heap, "fifty": compute_fifty, "robson": compute_robson,
    "elf": compute_elf, "pebblelink": compute_pebblelink, "dynamic": compute_dynamic, "aslr": compute_aslr,
    "maps": compute_maps, "ub": compute_ub, "smash": compute_smash, "job": compute_job, "frontier": compute_frontier,
    "backtrace": compute_backtrace, "archive": compute_archive, "sanitize": compute_sanitize,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
