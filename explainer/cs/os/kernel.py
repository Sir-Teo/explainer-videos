"""PebbleOS (Part 31): a kernel of about two hundred Pebble instructions.

    procs = [user("tok", TOK, 0, stdout="pipe"), user("job", JOB_HASH, 1, stdin="pipe")]
    m = boot(procs, tape=text)          # an OSMachine with the kernel at 0 and each process in its own region
    m.run()                             # until every process has exited (the kernel halts the machine)
    m.output, report(m)

What it does, in the order the part draws it:

* **boot** sets the trap vector, picks the first process, starts the timer, and drops to user mode with ``eret``;
* **every trap** enters at ``trap``: the user's fifteen registers and pc go into its process control block (PCB),
  and the cause picks a path;
* **system calls** (``a5`` = number): ``exit``, ``read`` and ``write`` (fd 0 and 1; the tape, the console or the
  pipe), ``getpid``, ``yield``.  Buffers are checked against the caller's bounds before the kernel touches them;
* **the pipe**: a 4 KiB ring.  A reader finding it empty, or a writer finding it full, is **blocked**: its pc is
  moved back to the ``ecall`` so the call restarts when it next runs, and every blocked process is made ready
  again whenever the pipe changes (simple, and a little wasteful: the thundering herd);
* **the timer** preempts a process after ``quantum`` instructions; the scheduler is round robin over the table;
* **faults** (a bad address, an illegal or privileged instruction, division by zero) kill the process, with exit
  code -cause; the others carry on;
* when no process is left, the kernel halts the machine.

The kernel runs with interrupts off (it is not preemptible), so a ``write`` of a whole buffer is atomic.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from explainer.cs.os.machine import OSMachine
from explainer.cs.pebble.asm import assemble
from explainer.cs.pebble.isa import IO_CONSOLE, IO_TAPE

NPROC = 4
PCB = 128
QUANTUM = 20_000
PIPESZ = 4096
KSTACK = 0x8000
MEM = (NPROC + 1) << 20
# PCB fields (registers r1..r15 at 4*r)
ST, EPC_, LO_, HI_, PID, STDIN, STDOUT, NDISP, NSYS, XCODE, NTICK = 0, 64, 68, 72, 76, 80, 84, 88, 92, 96, 100
FREE, READY, RUNNING, BLOCKED, EXITED = 0, 1, 2, 3, 4
STATES = {FREE: "free", READY: "ready", RUNNING: "running", BLOCKED: "blocked", EXITED: "exited"}
KIND = {"tape": 0, "console": 0, "pipe": 1}

KERNEL = """
# PebbleOS: boot, traps, system calls, a pipe, and a round-robin scheduler
        .equ NPROC, {NPROC}
        .equ PCBSZ, {PCB}
        .equ QUANTUM, {quantum}
        .equ PMASK, {pmask}
        .equ KSTACK, {KSTACK}
_kstart: la  t0, trap
        csrw tvec, t0           # where every trap goes
        li   sp, KSTACK
        la   t0, procs
        sw   t0, curpcb(zero)
        li   t1, 2
        sw   t1, 0(t0)          # the first process is running
        lw   t1, {NDISP}(t0)
        addi t1, t1, 1
        sw   t1, {NDISP}(t0)
        li   t1, QUANTUM
        csrw timer, t1
        j    resume

# ---- every trap: save the user's registers in its PCB ----------------------------------
trap:   sw   t0, ksave(zero)    # one register freed, to hold the PCB's address
        lw   t0, curpcb(zero)
        sw   ra, 4(t0)
        sw   sp, 8(t0)
        sw   a0, 12(t0)
        sw   a1, 16(t0)
        sw   a2, 20(t0)
        sw   a3, 24(t0)
        sw   a4, 28(t0)
        sw   a5, 32(t0)
        sw   t1, 40(t0)
        sw   t2, 44(t0)
        sw   t3, 48(t0)
        sw   s0, 52(t0)
        sw   s1, 56(t0)
        sw   s2, 60(t0)
        lw   t1, ksave(zero)
        sw   t1, 36(t0)         # the user's t0
        csrr t1, epc
        sw   t1, {EPC}(t0)
        li   sp, KSTACK         # the kernel's own stack
        csrr t1, cause
        li   t2, 8
        beq  t1, t2, syscall
        li   t2, 16
        beq  t1, t2, tick
        sub  t1, zero, t1       # any other cause is a fault: kill the process
        sw   t1, {XCODE}(t0)
        lw   t1, nfault(zero)
        addi t1, t1, 1
        sw   t1, nfault(zero)
        j    kill

tick:   lw   t1, ntick(zero)    # the timer: this process has had its quantum
        addi t1, t1, 1
        sw   t1, ntick(zero)
        lw   t1, {NTICK}(t0)
        addi t1, t1, 1
        sw   t1, {NTICK}(t0)
preempt: li  t1, 1              # running -> ready
        sw   t1, 0(t0)
        j    schedule

# ---- system calls ------------------------------------------------------------------------
syscall: lw  t1, {EPC}(t0)
        addi t1, t1, 4          # return past the ecall
        sw   t1, {EPC}(t0)
        lw   t1, nsys(zero)
        addi t1, t1, 1
        sw   t1, nsys(zero)
        lw   t1, {NSYS}(t0)
        addi t1, t1, 1
        sw   t1, {NSYS}(t0)
        lw   a0, 12(t0)         # the arguments
        lw   a1, 16(t0)
        lw   a2, 20(t0)
        lw   t1, 32(t0)         # a5: which call
        beqz t1, sys_exit
        li   t2, 1
        beq  t1, t2, sys_read
        li   t2, 2
        beq  t1, t2, sys_write
        li   t2, 3
        beq  t1, t2, sys_getpid
        li   t2, 4
        beq  t1, t2, preempt    # yield
bad:    li   t1, -1             # no such call, or a bad argument
        sw   t1, 12(t0)
        j    resume

sys_getpid: lw t1, {PID}(t0)
        sw   t1, 12(t0)
        j    resume

sys_exit: sw a0, {XCODE}(t0)
kill:   li   t1, 4              # exited
        sw   t1, 0(t0)
        lw   t1, {STDOUT}(t0)
        beqz t1, kill2
        sw   zero, pwriter(zero)  # the pipe has lost its writer: readers will see end of file
kill2:  call wakeall
        j    schedule

# check that [a1, a1 + a2) lies inside the caller's memory
checkbuf: blt a2, zero, bad
        lw   t1, {LO}(t0)
        blt  a1, t1, bad
        add  t2, a1, a2
        lw   t1, {HI}(t0)
        blt  t1, t2, bad
        ret

sys_read: bnez a0, bad          # fd 0 only
        call checkbuf
        lw   t1, {STDIN}(t0)
        bnez t1, read_pipe
        li   t1, {IO_TAPE}      # the tape: copy bytes until n, or its end
        li   t2, 0
rt1:    bge  t2, a2, rt2
        lw   t3, 0(t1)
        bltz t3, rt2
        add  s0, a1, t2
        sb   t3, 0(s0)
        addi t2, t2, 1
        j    rt1
rt2:    sw   t2, 12(t0)
        j    resume

read_pipe: lw t1, pcount(zero)
        bnez t1, rp0
        lw   t2, pwriter(zero)
        beqz t2, rpeof
        j    block              # empty, and someone may still write: wait
rpeof:  sw   zero, 12(t0)       # empty for good: end of file
        j    resume
rp0:    mv   s0, a2             # m = min(n, count)
        bge  t1, s0, rp1
        mv   s0, t1
rp1:    li   t2, 0
        lw   t3, phead(zero)
rp2:    bge  t2, s0, rp3
        lbu  s2, pipebuf(t3)
        add  s1, a1, t2
        sb   s2, 0(s1)
        addi t3, t3, 1
        andi t3, t3, PMASK
        addi t2, t2, 1
        j    rp2
rp3:    sw   t3, phead(zero)
        lw   t1, pcount(zero)
        sub  t1, t1, s0
        sw   t1, pcount(zero)
        sw   s0, 12(t0)
        call wakeall            # a writer may be waiting for room
        j    resume

sys_write: li t1, 1
        bne  a0, t1, bad        # fd 1 only
        call checkbuf
        lw   t1, {STDOUT}(t0)
        bnez t1, write_pipe
        li   t1, {IO_CONSOLE}   # the console: every byte
        li   t2, 0
wc1:    bge  t2, a2, wc2
        add  s0, a1, t2
        lbu  t3, 0(s0)
        sb   t3, 0(t1)
        addi t2, t2, 1
        j    wc1
wc2:    sw   a2, 12(t0)
        j    resume

write_pipe: lw t1, pcount(zero)
        li   t2, {PIPESZ}
        sub  t2, t2, t1         # room
        bnez t2, wp0
        j    block              # full: wait
wp0:    mv   s0, a2             # m = min(n, room)
        bge  t2, s0, wp1
        mv   s0, t2
wp1:    lw   t3, phead(zero)
        add  t3, t3, t1
        andi t3, t3, PMASK      # the tail
        li   t2, 0
wp2:    bge  t2, s0, wp3
        add  s1, a1, t2
        lbu  s2, 0(s1)
        sb   s2, pipebuf(t3)
        addi t3, t3, 1
        andi t3, t3, PMASK
        addi t2, t2, 1
        j    wp2
wp3:    lw   t1, pcount(zero)
        add  t1, t1, s0
        sw   t1, pcount(zero)
        sw   s0, 12(t0)
        call wakeall            # a reader may be waiting for bytes
        j    resume

block:  lw   t1, {EPC}(t0)      # run the ecall again when woken
        addi t1, t1, -4
        sw   t1, {EPC}(t0)
        li   t1, 3              # blocked
        sw   t1, 0(t0)
        lw   t1, nblock(zero)
        addi t1, t1, 1
        sw   t1, nblock(zero)
        j    schedule

wakeall: la  t1, procs          # every blocked process becomes ready, to try again
        li   t2, NPROC
wa1:    lw   t3, 0(t1)
        li   s0, 3
        bne  t3, s0, wa2
        li   s0, 1
        sw   s0, 0(t1)
wa2:    addi t1, t1, PCBSZ
        addi t2, t2, -1
        bnez t2, wa1
        ret

# ---- the scheduler: round robin, from the process after this one --------------------------
schedule: mv s0, t0
        li   s1, NPROC
sc1:    addi t0, t0, PCBSZ
        la   t1, procs_end
        bne  t0, t1, sc2
        la   t0, procs
sc2:    lw   t1, 0(t0)
        li   t2, 1
        beq  t1, t2, found
        addi s1, s1, -1
        bnez s1, sc1
        halt                    # nothing can run: every process has exited

found:  li   t1, 2              # ready -> running
        sw   t1, 0(t0)
        sw   t0, curpcb(zero)
        beq  t0, s0, same
        lw   t1, nswitch(zero)  # a context switch
        addi t1, t1, 1
        sw   t1, nswitch(zero)
same:   lw   t1, {NDISP}(t0)
        addi t1, t1, 1
        sw   t1, {NDISP}(t0)
        li   t1, QUANTUM
        csrw timer, t1          # a fresh quantum

# ---- back to user mode: the PCB's registers, its bounds, and eret --------------------------
resume: lw   t0, curpcb(zero)
        lw   t1, {EPC}(t0)
        csrw epc, t1
        lw   t1, {LO}(t0)
        csrw lo, t1
        lw   t1, {HI}(t0)
        csrw hi, t1
        li   t1, 2              # after eret: user mode, interrupts on
        csrw status, t1
        lw   ra, 4(t0)
        lw   sp, 8(t0)
        lw   a0, 12(t0)
        lw   a1, 16(t0)
        lw   a2, 20(t0)
        lw   a3, 24(t0)
        lw   a4, 28(t0)
        lw   a5, 32(t0)
        lw   t1, 40(t0)
        lw   t2, 44(t0)
        lw   t3, 48(t0)
        lw   s0, 52(t0)
        lw   s1, 56(t0)
        lw   s2, 60(t0)
        lw   t0, 36(t0)
        eret
kend:

# ---- kernel data -------------------------------------------------------------------------
        .align 4
ksave:  .word 0
curpcb: .word 0
nsys:   .word 0
nswitch: .word 0
ntick:  .word 0
nblock: .word 0
nfault: .word 0
pcount: .word 0
phead:  .word 0
pwriter: .word {pwriter}
        .align 64
procs:
{table}
procs_end:
pipebuf: .space {PIPESZ}
"""


@dataclass
class Proc:
    name: str
    image: bytes                # the process's memory from lo (code and data)
    entry: int
    lo: int
    hi: int
    stdin: str = "tape"
    stdout: str = "console"
    labels: dict = field(default_factory=dict)


def region(k: int) -> tuple[int, int]:
    """Process k's memory: one MiB each, above the kernel's first MiB."""
    return (k + 1) << 20, (k + 2) << 20


def user(name: str, src: str, k: int, stdin: str = "tape", stdout: str = "console", level: int = 2) -> Proc:
    """A Pebble-language program compiled for PebbleOS, placed in region k."""
    from explainer.cs.lang.compiler.driver import compile_program
    lo, hi = region(k)
    c = compile_program(src, level, target="os", origin=lo)
    return Proc(name, c.program.image[lo:], c.program.labels["_start"], lo, hi, stdin, stdout, c.program.labels)


def user_asm(name: str, src: str, k: int, stdin: str = "tape", stdout: str = "console") -> Proc:
    """A process written in assembly (with the user library), placed in region k."""
    from explainer.cs.os.ulib import ULIB
    lo, hi = region(k)
    p = assemble(f".org {lo:#x}\n{ULIB}\n{src}\n        .align 4\n_brk: .word 0\n_heap:\n")
    return Proc(name, p.image[lo:], p.labels["_start"], lo, hi, stdin, stdout, p.labels)


def kernel_source(procs: list[Proc], quantum: int = QUANTUM) -> str:
    rows = []
    for k in range(NPROC):
        w = [0] * (PCB // 4)
        if k < len(procs):
            p = procs[k]
            w[ST // 4] = READY
            w[2] = p.hi                      # sp: the top of its region
            w[EPC_ // 4], w[LO_ // 4], w[HI_ // 4], w[PID // 4] = p.entry, p.lo, p.hi, k + 1
            w[STDIN // 4], w[STDOUT // 4] = KIND[p.stdin], KIND[p.stdout]
        rows.append("        .word " + ", ".join(str(x) for x in w))
    pw = int(any(p.stdout == "pipe" for p in procs))
    return KERNEL.format(NPROC=NPROC, PCB=PCB, quantum=quantum, pmask=PIPESZ - 1, KSTACK=KSTACK, EPC=EPC_, LO=LO_,
                         HI=HI_, PID=PID, STDIN=STDIN, STDOUT=STDOUT, NDISP=NDISP, NSYS=NSYS, XCODE=XCODE,
                         NTICK=NTICK, IO_TAPE=IO_TAPE, IO_CONSOLE=IO_CONSOLE, PIPESZ=PIPESZ, pwriter=pw,
                         table="\n".join(rows))


def boot(procs: list[Proc], tape: bytes = b"", quantum: int = QUANTUM, trace: bool = False) -> OSMachine:
    k = assemble(kernel_source(procs, quantum))
    m = OSMachine(image=k.image, tape=tape, mem_size=MEM, trace=trace)
    for p in procs:
        m.mem[p.lo:p.lo + len(p.image)] = p.image
    m.kernel = k
    m.procs = procs
    return m


def pcbs(m: OSMachine) -> list[dict]:
    """The process table, read out of the kernel's memory."""
    base = m.kernel.labels["procs"]
    out = []
    for k in range(len(m.procs)):
        a = base + k * PCB

        def w(off):
            v = m.word(a + off)
            return v - (1 << 32) if v >> 31 else v
        out.append({"name": m.procs[k].name, "pid": w(PID), "state": STATES[w(ST)], "pc": w(EPC_),
                    "dispatched": w(NDISP), "syscalls": w(NSYS), "ticks": w(NTICK), "exit": w(XCODE),
                    "regs": [w(4 * r) for r in range(16)]})
    return out


def report(m: OSMachine) -> dict:
    L = m.kernel.labels
    return {"syscalls": m.word(L["nsys"]), "switches": m.word(L["nswitch"]), "ticks": m.word(L["ntick"]),
            "blocks": m.word(L["nblock"]), "faults": m.word(L["nfault"]), "usteps": m.usteps, "ksteps": m.ksteps,
            "steps": m.steps, "kernel_words": L["kend"] // 4, "procs": pcbs(m)}


def attribute(m: OSMachine) -> dict:
    """Instructions per process (user mode) and in the kernel, from the trap and eret events: user instructions
    run from each eret to the next trap."""
    from explainer.cs.os.machine import ERET
    who = {p.name: 0 for p in m.procs}
    traps = erets = 0
    cur, start = None, None
    for step, cause, pc, _ in m.events:
        if cause == ERET:
            erets += 1
            cur = next(p.name for p in m.procs if p.lo <= pc < p.hi)
            start = step + 1
        else:
            traps += 1
            if cur is not None:
                who[cur] += step - start
                cur = None
    return {"user": who, "kernel": m.steps - sum(who.values()), "traps": traps, "erets": erets}


def timeline(m: OSMachine) -> list[tuple[int, int, str]]:
    """(start, end, who) for every stretch: a process's name, or "kernel"."""
    from explainer.cs.os.machine import ERET
    out, last, cur = [], 0, "kernel"
    for step, cause, pc, _ in m.events:
        if cause == ERET:
            out.append((last, step + 1, "kernel"))
            cur = next(p.name for p in m.procs if p.lo <= pc < p.hi)
            last = step + 1
        else:
            out.append((last, step, cur))
            last = step
    out.append((last, m.steps, "kernel"))
    return [s for s in out if s[1] > s[0]]
