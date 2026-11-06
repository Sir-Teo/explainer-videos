"""The user library every PebbleOS process is linked with (Part 31): the C runtime's start, and ``getc``/``putc``
buffered over the ``read`` and ``write`` system calls, as C's stdio buffers them (which is why ``getc`` is
traditionally a macro: a system call per byte would cost a trap per byte).

System calls: the number in ``a5``, arguments in ``a0..a2``, the result in ``a0``; the kernel preserves every other
register.
"""
from __future__ import annotations

BUFSZ = 4096
SYS_EXIT, SYS_READ, SYS_WRITE, SYS_GETPID, SYS_YIELD = 0, 1, 2, 3, 4
SYSCALLS = {SYS_EXIT: "exit", SYS_READ: "read", SYS_WRITE: "write", SYS_GETPID: "getpid", SYS_YIELD: "yield"}

ULIB = f"""
# ulib: the start of every process, and buffered getc and putc
_start: call main
        call __flush
        li   a5, {SYS_EXIT}
        li   a0, 0
        ecall                   # exit(0): never returns
__getc: la   t0, __in
        lw   t1, 0(t0)          # the next byte to hand out
        lw   t2, 4(t0)          # how many the last read gave
        bge  t1, t2, __fill
        add  t3, t0, t1
        lbu  a0, 8(t3)
        addi t1, t1, 1
        sw   t1, 0(t0)
        ret
__fill: li   a0, 0              # read(0, buffer, {BUFSZ})
        addi a1, t0, 8
        li   a2, {BUFSZ}
        li   a5, {SYS_READ}
        ecall
        ble  a0, zero, __eof
        la   t0, __in
        sw   zero, 0(t0)
        sw   a0, 4(t0)
        j    __getc
__eof:  li   a0, -1
        ret
__putc: la   t0, __out
        lw   t1, 0(t0)
        add  t2, t0, t1
        sb   a0, 4(t2)
        addi t1, t1, 1
        sw   t1, 0(t0)
        li   t2, {BUFSZ}
        beq  t1, t2, __flush
        ret
__flush: la  t0, __out          # write(1, buffer, n), again until all of it is taken
        lw   t1, 0(t0)
        li   t2, 0
__fl:   bge  t2, t1, __fdone
        li   a0, 1
        add  a1, t0, t2
        addi a1, a1, 4
        sub  a2, t1, t2
        li   a5, {SYS_WRITE}
        ecall
        bltz a0, __fdone
        add  t2, t2, a0
        j    __fl
__fdone: sw  zero, 0(t0)
        ret
alloc:  la   t0, _brk
        lw   t1, 0(t0)
        bnez t1, _have
        la   t1, _heap
_have:  addi a0, a0, 3
        andi a0, a0, -4
        add  t2, t1, a0
        sw   t2, 0(t0)
        mv   a0, t1
        ret
        .align 4
__in:   .word 0, 0
        .space {BUFSZ}
__out:  .word 0
        .space {BUFSZ}
"""
