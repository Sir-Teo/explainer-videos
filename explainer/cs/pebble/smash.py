"""The stack smash, on Pebble (Part 11, chapter 13): a greeting program with an unchecked copy, an input that
overwrites the saved return address, and three defences.

    exe = build()                         # the vulnerable program, linked
    tape = exploit(exe)                   # shellcode + padding + the buffer's own address
    m = run(exe, tape)                    # prints "hello, ..." and then "pwned"
    run(exe, tape, canary=True)           # the epilogue finds the canary changed: "*** stack smashing detected ***"
    run(exe, tape, nx=True)               # the stack is not executable: the jump into the buffer faults

``greet`` keeps a 64-byte buffer at the bottom of its 80-byte frame and the saved return address at 76(sp).
``gets`` copies the input up to a newline with no bound (C's ``gets``, removed from the language in 2011).  The
attack fills the buffer with code, pads it to byte 76, and writes the buffer's address over the return address:
``ret`` then jumps into the input.  The address is fixed because nothing randomises the stack (ASLR, chapter 10).
"""

from __future__ import annotations

from .asm import assemble
from .emu import Machine, MachineError
from .isa import IO_CONSOLE, IO_TAPE
from .link import assemble_object, link, load

FRAME = 80
RA_OFF = 76
CANARY_OFF = 72


def source(canary: bool = False) -> str:
    pro = (f"        la   t0, guard\n        lw   t0, 0(t0)\n        sw   t0, {CANARY_OFF}(sp)\n" if canary else "")
    epi = (f"        la   t0, guard\n        lw   t0, 0(t0)\n        lw   t1, {CANARY_OFF}(sp)\n"
           "        bne  t0, t1, smashed\n" if canary else "")
    return f"""
        .globl _start
        .text
_start: call greet
        la   a0, bye
        call puts
        halt
greet:  addi sp, sp, -{FRAME}
        sw   ra, {RA_OFF}(sp)
{pro}        mv   a0, sp
        call gets              # no bound: the bug
        la   a0, hello
        call puts
        mv   a0, sp
        call puts
{epi}        lw   ra, {RA_OFF}(sp)
        addi sp, sp, {FRAME}
        ret
smashed: la  a0, alarm
        call puts
        halt
# gets(a0): copy the input up to a newline into a0, and end it with a zero byte
gets:   li   t1, {IO_TAPE:#x}
gnext:  lw   t2, 0(t1)
        blt  t2, zero, gend
        li   t3, 10
        beq  t2, t3, gend
        sb   t2, 0(a0)
        addi a0, a0, 1
        j    gnext
gend:   sb   zero, 0(a0)
        ret
puts:   li   t1, {IO_CONSOLE:#x}
pnext:  lbu  t2, 0(a0)
        beqz t2, pend
        sb   t2, 0(t1)
        addi a0, a0, 1
        j    pnext
pend:   ret
        .data
hello:  .asciiz "hello, "
bye:    .asciiz "\\nbye\\n"
alarm:  .asciiz "\\n*** stack smashing detected ***\\n"
        .align 4
guard:  .word 0x5ca1ab1e
"""


def build(canary: bool = False):
    return link([assemble_object(source(canary), "greet.o")])


SHELLCODE = f"""
        li   t0, {IO_CONSOLE:#x}
        li   t1, 112        # p
        sb   t1, 0(t0)
        li   t1, 119        # w
        sb   t1, 0(t0)
        li   t1, 110        # n
        sb   t1, 0(t0)
        li   t1, 101        # e
        sb   t1, 0(t0)
        li   t1, 100        # d
        sb   t1, 0(t0)
        halt
"""


def frame_sp(exe, argv=("greet",)) -> int:
    """Where greet's frame will be: run the program on harmless input and catch sp at greet's first instruction."""
    m = load(exe, argv=list(argv), tape=b"x\n")
    greet = exe.symbols.get("greet")
    if greet is None:  # local label: find it by the first instruction after _start's call
        greet = _local(exe, "greet")
    while not m.halted:
        if m.pc == greet:
            return m.regs[2] - FRAME
        m.step()
    raise RuntimeError("greet never ran")


def _local(exe, name):
    # the executable keeps only global symbols; the object knows greet's offset in its text
    obj = assemble_object(source(), "greet.o")
    return obj.symbols[name].offset


def exploit(exe, argv=("greet",)) -> bytes:
    code = assemble(SHELLCODE).image
    assert len(code) <= RA_OFF, "shellcode too long"
    buf = frame_sp(exe, argv)
    pad = b"A" * (RA_OFF - len(code))
    payload = code + pad + buf.to_bytes(4, "little")
    assert b"\n" not in payload, "the payload must not contain a newline"
    return payload + b"\n"


class NXMachine(Machine):
    """A machine whose stack (the top 64 KiB) cannot be executed: fetching an instruction there faults."""

    def step(self):
        if self.pc >= self.mem_size - (1 << 16):
            raise MachineError(f"execute from the stack at {self.pc:#x}: no-execute fault")
        return super().step()


def run(exe, tape: bytes, nx: bool = False, argv=("greet",), limit: int = 200_000):
    m = load(exe, argv=list(argv), tape=tape)
    if nx:
        m.__class__ = NXMachine
    fault = None
    try:
        while not m.halted and m.steps < limit:
            m.step()
    except MachineError as e:
        fault = str(e)
    return {"output": bytes(m.output).decode("latin-1"), "fault": fault, "steps": m.steps, "halted": m.halted}
