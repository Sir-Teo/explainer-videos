"""PebbleOS with virtual memory (Part 32): every process at the same virtual addresses, each in its own page table.

    procs = [user_vm("tok", TOK, stdout="pipe"), user_vm("job", JOB_HASH, stdin="pipe")]
    m = boot_vm(procs, tape=text)        # a VMMachine: kernel at physical 0, frames above 1 MiB
    m.run(); report_vm(m)

The boot loader (this module, playing the part of the program that loads the kernel) builds each address space:

* L1 slot 0: physical memory 0-4 MiB, mapped once as a supervisor-only superpage, in every address space.  The
  kernel's code, data, page tables and every frame live there, so the kernel runs translated with any process's
  table installed, and copies a process's buffers by their virtual addresses.  User mode cannot touch it (no U).
* L1 slot 1 (virtual 4-5 MiB): the process, through its own L2 table.  Code pages are mapped R+X, data pages R+W:
  writing to code is a protection fault.  The I/O buffers, every page with initial data and the top stack page are
  mapped at boot; the zero pages (most of the job's hash table, the rest of the stack) are not, and the kernel maps a
  zeroed frame the first time each is touched: **demand-zero paging**.
* Faults outside the process's range, or protection faults, kill it, as in Part 31.

Frames are handed out by a bump pointer and never freed (a real kernel keeps free lists, and reclaims).
"""
from __future__ import annotations

from explainer.cs.os import kernel as K
from explainer.cs.os.mmu import PAGE, PTE_A, PTE_D, PTE_R, PTE_U, PTE_V, PTE_W, PTE_X, VMMachine, pte
from explainer.cs.os.ulib import ULIB_VM, VBASE, VSIZE
from explainer.cs.pebble.asm import assemble

PMEM = 4 << 20
FRAME_BASE = 1 << 20


def _proc(name, prog, stdin, stdout):
    L = prog.labels
    p = K.Proc(name, prog.image[VBASE:], L["_start"], VBASE, VBASE + VSIZE, stdin, stdout, L)
    p.code = [(VBASE, L["__in"]), (L["__ucode"], L["_brk"])]
    p.eager = [(L["__in"], L["__ucode"])]
    return p


def user_vm(name: str, src: str, stdin: str = "tape", stdout: str = "console", level: int = 2) -> K.Proc:
    from explainer.cs.lang.compiler.driver import compile_program
    c = compile_program(src, level, target="vm", origin=VBASE)
    return _proc(name, c.program, stdin, stdout)


def user_asm_vm(name: str, src: str, stdin: str = "tape", stdout: str = "console", data: str = "") -> K.Proc:
    """An assembly process; ``data`` (labels and directives) goes on the data pages, after ``_brk``."""
    p = assemble(f".org {VBASE:#x}\n{ULIB_VM}\n{src}\n        .align 4096\n_brk: .word 0\n{data}\n        .align 4\n"
                 f"_heap:\n")
    return _proc(name, p, stdin, stdout)


def threads_vm(name: str, src: str, n: int, data: str = "", stdin: str = "tape", stdout: str = "console",
               stack_pages: int = 4) -> list[K.Proc]:
    """Part 33: ``n`` threads of one assembly program in **one** address space.  Each is its own PCB (registers,
    pc, its own stack: thread k's stack top is k * ``stack_pages`` pages below the region's top), but all share the
    page table, so they share code, data and heap."""
    import dataclasses
    p = user_asm_vm(f"{name}0", src, stdin, stdout, data)
    out = [p]
    for k in range(1, n):
        q = dataclasses.replace(p, name=f"{name}{k}", hi=p.hi - k * stack_pages * PAGE)
        q.code, q.eager, q.parent = p.code, p.eager, p
        out.append(q)
    return out


def boot_vm(procs: list[K.Proc], tape: bytes = b"", quantum: int = K.QUANTUM, tlb_size: int = 16,
            lazy: bool = True, trace: bool = False) -> VMMachine:
    nxt = [FRAME_BASE]

    def frame():
        a = nxt[0]
        nxt[0] += PAGE
        return a
    layout = []
    for p in procs:
        par = getattr(p, "parent", None)
        if par is not None:          # a thread: its parent's tables, and a stack page of its own
            p.root, p.l2 = par.root, par.l2
            layout.append((p, {p.hi - PAGE: (b"", PTE_V | PTE_U | PTE_R | PTE_W)}))
            continue
        p.root, p.l2 = frame(), frame()
        pages = {}
        n = (len(p.image) + PAGE - 1) // PAGE
        for i in range(n):
            va = VBASE + i * PAGE
            chunk = p.image[i * PAGE:(i + 1) * PAGE]
            code = any(a <= va < b for a, b in p.code)
            eager = code or any(a <= va < b for a, b in p.eager) or any(chunk) or not lazy
            if eager:
                pages[va] = (chunk, PTE_V | PTE_U | (PTE_R | PTE_X if code else PTE_R | PTE_W))
        pages[p.hi - PAGE] = (b"", PTE_V | PTE_U | PTE_R | PTE_W)     # the top of the stack
        layout.append((p, pages))
    k = assemble(K.kernel_source(procs, quantum, vm={"nextframe": 0, "frame_end": PMEM}))
    m = VMMachine(image=k.image, tape=tape, mem_size=PMEM, trace=trace)
    m.tlb_size = tlb_size
    eager_frames = {}
    for p, pages in layout:
        m.mem[p.root:p.root + 4] = pte(0, PTE_V | PTE_R | PTE_W | PTE_X | PTE_A | PTE_D).to_bytes(4, "little")
        a1 = p.root + ((VBASE >> 22) << 2)
        m.mem[a1:a1 + 4] = pte(p.l2, PTE_V).to_bytes(4, "little")
        for va, (chunk, flags) in sorted(pages.items()):
            f = frame()
            m.mem[f:f + len(chunk)] = chunk
            a2 = p.l2 + (((va >> 12) & 0x3FF) << 2)
            m.mem[a2:a2 + 4] = pte(f, flags).to_bytes(4, "little")
        eager_frames[p.name] = len(pages)
    m.mem[k.labels["nextframe"]:k.labels["nextframe"] + 4] = nxt[0].to_bytes(4, "little")
    m.kernel, m.procs = k, procs
    m.eager_frames = eager_frames
    return m


def report_vm(m: VMMachine) -> dict:
    r = K.report(m)
    L = m.kernel.labels
    r.update({"page_faults": m.word(L["npfault"]), "frames_used": (m.word(L["nextframe"]) - FRAME_BASE) // PAGE,
              "eager_frames": m.eager_frames, **m.stats})
    return r


def mappings(m: VMMachine, p: K.Proc) -> list[tuple[int, int, int]]:
    """(virtual page, physical frame, flags) for every mapped page of p."""
    out = []
    for i in range(1024):
        e = m.word(p.l2 + 4 * i)
        if e & PTE_V:
            out.append((VBASE + i * PAGE, (e >> 12) << 12, e & 0xFFF))
    return out
