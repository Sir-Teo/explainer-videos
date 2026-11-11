"""The Job, version 1 (Part 11): the same algorithm as Part 6's JOB_V0, written the way a compiler would, in four
files linked by Pebble's linker.

    main.s    _start: read words into a buffer in its stack frame, look each one up, then report
    table.s   lookup(word, len): find the word in a linked list of heap nodes, or append a new node
              report(top): print the `top` most common words
    alloc.s   alloc(n): a bump allocator over a heap in .bss
    io.s      getc, putc, printnum (with a stack-allocated digit buffer: Pebble has div since Part 7)

The calling convention (Part 11, chapter 4): arguments and results in a0..a5, the return address in ra; t0..t3 are
caller-saved, s0..s2 callee-saved; sp stays 16-byte aligned, and a function that calls another saves ra in its frame.
A node is 16 bytes: next, letters, length, count.  The list is kept in order of first appearance (a tail pointer),
so ties break the way JOB_V0's do and the output is byte-for-byte the same.
"""

from __future__ import annotations

from .isa import IO_CONSOLE, IO_TAPE
from .programs import TOP

IO_S = f"""
# io.s: the tape and the console
        .globl getc
        .globl putc
        .globl printnum
        .text
getc:   li   t0, {IO_TAPE:#x}
        lw   a0, 0(t0)        # the next byte, or -1
        ret
putc:   li   t0, {IO_CONSOLE:#x}
        sb   a0, 0(t0)
        ret
# printnum(n): n >= 0 in decimal.  The digits come out last first, so they are kept in a buffer in this frame.
printnum:
        addi sp, sp, -32      # frame: ra, s0, s1, and 16 bytes of digits
        sw   ra, 28(sp)
        sw   s0, 24(sp)
        sw   s1, 20(sp)
        mv   s0, a0
        li   s1, 0            # digits stored
pdig:   li   t1, 10
        rem  t2, s0, t1
        div  s0, s0, t1
        addi t2, t2, 48
        add  t3, sp, s1
        sb   t2, 0(t3)
        addi s1, s1, 1
        bnez s0, pdig
pout:   addi s1, s1, -1
        add  t3, sp, s1
        lbu  a0, 0(t3)
        call putc
        bnez s1, pout
        lw   s1, 20(sp)
        lw   s0, 24(sp)
        lw   ra, 28(sp)
        addi sp, sp, 32
        ret
"""

ALLOC_S = """
# alloc.s: a bump allocator; nothing is ever freed
        .globl alloc
        .text
alloc:  la   t0, brk
        lw   t1, 0(t0)        # the first free byte
        bnez t1, have
        la   t1, heap         # first call: the heap starts at `heap`
have:   addi a0, a0, 3        # round the request up to a word
        andi a0, a0, -4
        add  t2, t1, a0
        sw   t2, 0(t0)
        mv   a0, t1
        ret
        .data
brk:    .word 0
        .bss
heap:   .space 393216
"""

TABLE_S = f"""
# table.s: the word table as a linked list of 16-byte nodes: next, letters, length, count
        .globl lookup
        .globl report
        .text
# lookup(a0 = letters, a1 = length): count the word, or append a node for it
lookup: addi sp, sp, -16
        sw   ra, 12(sp)
        sw   s0, 8(sp)
        sw   s1, 4(sp)
        sw   s2, 0(sp)
        mv   s0, a0
        mv   s1, a1
        la   t0, head
        lw   t0, 0(t0)        # t0: the current node
scan:   beqz t0, new
        lw   t1, 8(t0)        # same length?
        bne  t1, s1, next
        lw   t2, 4(t0)
        li   t3, 0
cmp:    beq  t3, s1, found
        add  a2, t2, t3
        lbu  a2, 0(a2)
        add  a3, s0, t3
        lbu  a3, 0(a3)
        bne  a2, a3, next
        addi t3, t3, 1
        j    cmp
found:  lw   t1, 12(t0)
        addi t1, t1, 1
        sw   t1, 12(t0)
        j    out
next:   lw   t0, 0(t0)
        j    scan
new:    li   a0, 16           # a node
        call alloc
        mv   s2, a0
        mv   a0, s1           # its letters, copied: the caller's buffer is reused
        call alloc
        li   t3, 0
copy:   beq  t3, s1, link
        add  a2, s0, t3
        lbu  a2, 0(a2)
        add  a3, a0, t3
        sb   a2, 0(a3)
        addi t3, t3, 1
        j    copy
link:   sw   zero, 0(s2)
        sw   a0, 4(s2)
        sw   s1, 8(s2)
        li   t1, 1
        sw   t1, 12(s2)
        la   t0, tail
        lw   t1, 0(t0)
        sw   s2, 0(t0)        # tail = node
        beqz t1, first
        sw   s2, 0(t1)        # old tail.next = node
        j    out
first:  la   t0, head
        sw   s2, 0(t0)
out:    lw   s2, 0(sp)
        lw   s1, 4(sp)
        lw   s0, 8(sp)
        lw   ra, 12(sp)
        addi sp, sp, 16
        ret

# report(a0 = top): print the most common words, ties to the first seen; printed nodes get their count negated
report: addi sp, sp, -16
        sw   ra, 12(sp)
        sw   s0, 8(sp)
        sw   s1, 4(sp)
        sw   s2, 0(sp)
        mv   s0, a0
rloop:  beqz s0, rdone
        la   t0, head
        lw   t0, 0(t0)
        li   s1, 0            # best count
        li   s2, 0            # best node
find:   beqz t0, got
        lw   t1, 12(t0)
        bge  s1, t1, fnext
        mv   s1, t1
        mv   s2, t0
fnext:  lw   t0, 0(t0)
        j    find
got:    beqz s1, rdone
        lw   t1, 4(s2)        # print the letters
        lw   t2, 8(s2)
pw:     beqz t2, pcount
        lbu  a0, 0(t1)
        addi sp, sp, -16      # t1, t2 are caller-saved: keep them across putc
        sw   t1, 4(sp)
        sw   t2, 0(sp)
        call putc
        lw   t2, 0(sp)
        lw   t1, 4(sp)
        addi sp, sp, 16
        addi t1, t1, 1
        addi t2, t2, -1
        j    pw
pcount: li   a0, 32
        call putc
        mv   a0, s1
        call printnum
        li   a0, 10
        call putc
        sub  t1, zero, s1
        sw   t1, 12(s2)
        addi s0, s0, -1
        j    rloop
rdone:  lw   s2, 0(sp)
        lw   s1, 4(sp)
        lw   s0, 8(sp)
        lw   ra, 12(sp)
        addi sp, sp, 16
        ret
        .data
head:   .word 0
tail:   .word 0
"""

MAIN_S = f"""
# main.s: read words into a buffer on the stack; look each one up; report
        .globl _start
        .text
_start: addi sp, sp, -272     # frame: ra, s0, s1, and a 256-byte word buffer at 0(sp)
        sw   ra, 268(sp)
        sw   s0, 264(sp)
        sw   s1, 260(sp)
        li   s0, 0            # s0: letters in the current word
read:   call getc
        blt  a0, zero, eof
        addi t0, a0, -65      # 'A'..'Z' -> 'a'..'z'
        sltiu t1, t0, 26
        beqz t1, lower
        addi a0, a0, 32
lower:  addi t0, a0, -97      # a letter?
        sltiu t1, t0, 26
        beqz t1, sep
        add  t2, sp, s0       # append it to the buffer (no bounds check: see chapter 13)
        sb   a0, 0(t2)
        addi s0, s0, 1
        j    read
sep:    beqz s0, read
        mv   a0, sp
        mv   a1, s0
        call lookup
        li   s0, 0
        j    read
eof:    beqz s0, rep
        mv   a0, sp
        mv   a1, s0
        call lookup
rep:    li   a0, {TOP}
        call report
        halt
"""

FILES = {"main.s": MAIN_S, "table.s": TABLE_S, "alloc.s": ALLOC_S, "io.s": IO_S}


def build():
    """Assemble the four files and link them (main first, so _start is at address 0)."""
    from .link import assemble_object, link

    objs = [assemble_object(src, name.replace(".s", ".o")) for name, src in FILES.items()]
    return objs, link(objs)
