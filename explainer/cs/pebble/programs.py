"""Pebble-32 programs written by hand in Part 6, reused (and rewritten faster) by later parts.

* ``SUM``: 1 + 2 + ... + n, the first loop.
* ``HELLO``: a string to the console device.
* ``JOB_V0``: the Job, version 0 (videos/cs/SYLLABUS.md 2.2): read text from the tape, fold it to lower case, split
  it into words of letters, keep every distinct word in an unsorted table (a linear search per word), then print
  the twenty most frequent words with their counts.  :func:`job_reference` is the same computation in Python.
* ``TM_INTERP``: a Turing-machine interpreter; the machine is a table of words, the tape an array of bytes.
* ``SELFMOD``: sums an array the way EDSAC programmers did before index registers, by rewriting the address field
  of its own load instruction.
"""

from __future__ import annotations

import re

import numpy as np

from .isa import IO_BASE, IO_CONSOLE, IO_TAPE

SUM = """
        li   a0, 10          # n
        li   a1, 0           # the sum
loop:   add  a1, a1, a0      # sum += n
        addi a0, a0, -1      # n -= 1
        bnez a0, loop        # until n = 0
        halt                 # a1 = 55
"""

ARRAY_SUM = """
        la   t0, array       # t0: a pointer to the current element
        li   t1, 100         # t1: elements left
        li   a0, 0           # a0: the sum
loop:   lw   t2, 0(t0)       # load an element
        add  a0, a0, t2      # add it
        addi t0, t0, 4       # the next word
        addi t1, t1, -1
        bnez t1, loop
        halt                 # a0 = 1 + 2 + ... + 100 = 5050
        .align 4
array:  .word {words}
""".replace("{words}", ", ".join(str(k) for k in range(1, 101)))

HELLO = f"""
        la   t0, msg         # the string
        li   t1, {IO_CONSOLE:#x}  # the console device
next:   lbu  a0, 0(t0)       # one byte
        beqz a0, done        # a zero byte ends the string
        sb   a0, 0(t1)       # storing it prints it
        addi t0, t0, 1
        j    next
done:   halt
msg:    .asciiz "Hello from Pebble!\\n"
"""

TOP = 20
TABLE, POOL = 0x10000, 0x80000

JOB_V0 = f"""
# The Job, version 0: count the words on the tape, print the {TOP} most common.
# the table: one 12-byte entry per distinct word (pointer to its letters, length, count), in order of first use
        li   s0, {TABLE}       # s0: the table
        li   s1, 0           # s1: entries in it
        li   s2, {POOL}        # s2: the string pool; the word being read is built at its end
        li   a1, 0           # a1: letters in the current word
        li   t3, {IO_TAPE:#x}  # t3: the tape device
read:   lw   a0, 0(t3)       # the next byte, or -1 at the end
        blt  a0, zero, eof
        addi t0, a0, -65     # 'A'..'Z' -> 'a'..'z'
        sltiu t1, t0, 26
        beqz t1, lower
        addi a0, a0, 32
lower:  addi t0, a0, -97     # a letter?
        sltiu t1, t0, 26
        beqz t1, sep
        add  t2, s2, a1      # append it to the word
        sb   a0, 0(t2)
        addi a1, a1, 1
        j    read
sep:    beqz a1, read        # a separator ends a word, if there is one
        call word
        li   a1, 0
        j    read
eof:    beqz a1, report
        call word

# the report: {TOP} times, find the largest count (the first such word), print it, and mark it done
report: li   a0, {TOP}
        li   a4, {IO_CONSOLE:#x}
rloop:  beqz a0, done
        mv   t0, s0
        li   a2, 0
        li   a3, 0           # best count so far
find:   beq  a2, s1, got
        lw   t1, 8(t0)
        bge  a3, t1, fnext   # only a strictly larger count replaces the best
        mv   a3, t1
        mv   t3, t0
fnext:  addi t0, t0, 12
        addi a2, a2, 1
        j    find
got:    beqz a3, done        # fewer than {TOP} words
        lw   t1, 0(t3)       # print the word
        lw   t2, 4(t3)
pw:     beqz t2, pcount
        lbu  a5, 0(t1)
        sb   a5, 0(a4)
        addi t1, t1, 1
        addi t2, t2, -1
        j    pw
pcount: li   a5, 32          # a space, the count, a newline
        sb   a5, 0(a4)
        mv   t1, a3
        call printnum
        li   a5, 10
        sb   a5, 0(a4)
        sub  t1, zero, a3    # mark it printed
        sw   t1, 8(t3)
        addi a0, a0, -1
        j    rloop
done:   halt

# word: look up the a1 letters at s2; count it, or add it to the end of the table
word:   mv   t0, s0
        li   a2, 0
scan:   beq  a2, s1, insert
        lw   t1, 4(t0)       # same length?
        bne  t1, a1, next
        lw   t2, 0(t0)
        li   a3, 0
cmp:    beq  a3, a1, found   # every letter matched
        add  a4, t2, a3
        lbu  a4, 0(a4)
        add  a5, s2, a3
        lbu  a5, 0(a5)
        bne  a4, a5, next
        addi a3, a3, 1
        j    cmp
found:  lw   t1, 8(t0)
        addi t1, t1, 1
        sw   t1, 8(t0)
        ret
next:   addi t0, t0, 12
        addi a2, a2, 1
        j    scan
insert: sw   s2, 0(t0)       # the letters stay where they were read
        sw   a1, 4(t0)
        li   t1, 1
        sw   t1, 8(t0)
        add  s2, s2, a1
        addi s1, s1, 1
        ret

# printnum: t1 in decimal to the console at a4, by subtracting powers of ten (Pebble has no divide yet)
printnum: la  t0, pow10
        li   a2, 0           # a digit printed yet?
pnext:  lw   t2, 0(t0)
        beqz t2, pend
        li   a5, 48          # '0'
psub:   bltu t1, t2, pdig
        sub  t1, t1, t2
        addi a5, a5, 1
        j    psub
pdig:   li   a1, 48
        bne  a5, a1, pout    # a nonzero digit
        bnez a2, pout        # or a zero after one
        li   a1, 1
        beq  t2, a1, pout    # or the last digit
        j    pskip
pout:   sb   a5, 0(a4)
        li   a2, 1
pskip:  addi t0, t0, 4
        j    pnext
pend:   ret
        .align 4
pow10:  .word 1000000000, 100000000, 10000000, 1000000, 100000, 10000, 1000, 100, 10, 1, 0
"""


def job_tape(text: str) -> bytes:
    """The bytes the Job reads: the text as UTF-8 (letters outside a-z, A-Z are separators)."""
    return text.encode("utf-8")


WORD = re.compile(rb"[a-z]+")


def job_words(tape: bytes) -> list[bytes]:
    return WORD.findall(tape.lower())


def job_reference(tape: bytes, top: int = TOP) -> bytes:
    """What JOB_V0 prints: the most common words, ties broken by first appearance."""
    counts: dict[bytes, int] = {}
    for w in job_words(tape):
        counts[w] = counts.get(w, 0) + 1
    order = {w: i for i, w in enumerate(counts)}
    best = sorted(counts, key=lambda w: (-counts[w], order[w]))[:top]
    return b"".join(w + b" " + str(counts[w]).encode() + b"\n" for w in best)


def job_features(tape: bytes, top: int = TOP) -> dict[str, int]:
    """The events whose counts determine JOB_V0's running time, computed from the text without running it: bytes,
    letters, capitals, words, distinct words, table entries scanned, same-length entries compared, letters matched
    in those comparisons, and the report's work (entries examined, best-so-far replacements, letters and digit
    steps printed).  Every path through the program costs a fixed number of instructions, so the step count is an
    exact linear function of these (checked against the emulator in Part 6's compute)."""
    words = job_words(tape)
    index: dict[bytes, int] = {}
    counts: dict[bytes, int] = {}
    by_len: dict[int, int] = {}
    rank: dict[bytes, int] = {}  # same-length entries before it in the table
    prefix: dict[tuple, int] = {}  # (length, prefix) -> earlier entries of that length starting so
    lcp_sum: dict[bytes, int] = {}  # sum of common-prefix lengths with the earlier same-length entries
    scanned = same = matched = 0
    for w in words:
        i = index.get(w)
        if i is None:
            n = len(w)
            scanned += len(index)
            same += by_len.get(n, 0)
            rank[w] = by_len.get(n, 0)
            acc = 0
            for k in range(1, n + 1):
                key = (n, w[:k])
                acc += prefix.get(key, 0)
                prefix[key] = prefix.get(key, 0) + 1
            lcp_sum[w] = acc
            matched += acc
            index[w] = len(index)
            counts[w] = 1
            by_len[n] = by_len.get(n, 0) + 1
        else:
            scanned += i + 1
            same += rank[w] + 1
            matched += lcp_sum[w] + len(w)
            counts[w] += 1
    # the report, as the program does it
    vals = list(counts.values())
    names = list(counts)
    rep = {"passes": 0, "scan": 0, "best": 0, "letters": 0, "subs": 0, "nonzero": 0, "inner_zero": 0,
           "leading_zero": 0, "early": 0}
    for _ in range(top):
        best, bi = 0, -1
        for j, c in enumerate(vals):
            if c > best:
                best, bi = c, j
                rep["best"] += 1
        rep["scan"] += len(vals)
        if best == 0:
            rep["early"] = 1
            break
        rep["passes"] += 1
        rep["letters"] += len(names[bi])
        started = False
        for d in str(best).rjust(10, "0"):
            rep["subs"] += int(d)
            if d != "0":
                rep["nonzero"] += 1
                started = True
            elif started:
                rep["inner_zero"] += 1
            else:
                rep["leading_zero"] += 1
        vals[bi] = -best
    arr = np.frombuffer(tape, dtype=np.uint8)
    caps = int(((arr >= 65) & (arr <= 90)).sum())
    letters = caps + int(((arr >= 97) & (arr <= 122)).sum())
    pending = int(bool(tape) and (65 <= tape[-1] <= 90 or 97 <= tape[-1] <= 122))
    return {"bytes": len(tape), "letters": letters, "caps": caps, "words": len(words), "distinct": len(index),
            "scanned": scanned, "same_length": same, "matched": matched, "eof_pending": pending,
            **{"rep_" + k: v for k, v in rep.items()}}


def job_cycles(f: dict[str, int]) -> int:
    """JOB_V0's exact instruction count from :func:`job_features`: each path's cost read off the listing (``li``
    and ``la`` assemble to two instructions, every other line to one)."""
    B, L, W, D = f["bytes"], f["letters"], f["words"], f["distinct"]
    main = 10 + 8 * B + f["caps"] + 4 * L + (B - L) + 4 * (W - f["eof_pending"]) + 3 + f["eof_pending"]
    word = 3 * W + 6 * f["scanned"] + 9 * f["same_length"] + 8 * f["matched"] - 4 * (W - D) + 9 * D
    passes = f["rep_passes"]
    printnum = 77 * passes + 4 * f["rep_subs"] + 6 * f["rep_nonzero"] + 7 * f["rep_inner_zero"] \
        + 8 * f["rep_leading_zero"]
    report = 4 + 23 * passes + 6 * f["rep_scan"] + 2 * f["rep_best"] + 6 * f["rep_letters"] + printnum
    if f["rep_early"]:
        report += 6 + 1 + 1 + 1  # the last pass finds nothing: rloop, setup, the end of the scan, got, halt
    else:
        report += 2  # rloop's exit and halt
    return main + word + report


TM_INTERP = """
# A Turing-machine interpreter.  The machine: for state s and symbol b, the word at rules + 8 s + 4 b holds
# (next state << 16) | (move << 8) | write, move 1 = right, 255 = left; next state 255 halts.
# The tape: one byte per cell, the head starting in the middle.
        la   s0, rules
        la   s1, tape
        li   t0, 512
        add  s1, s1, t0      # s1: the head
        li   s2, 0           # s2: the state
        li   a0, 0           # a0: steps
        li   t3, 255
step:   lbu  t0, 0(s1)       # the symbol under the head
        slli t1, s2, 3       # rules + 8 state + 4 symbol
        slli t2, t0, 2
        add  t1, t1, t2
        add  t1, t1, s0
        lw   t1, 0(t1)
        andi t2, t1, 255     # write
        sb   t2, 0(s1)
        srli t2, t1, 8       # move
        andi t2, t2, 255
        beq  t2, t3, left
        addi s1, s1, 1
        j    moved
left:   addi s1, s1, -1
moved:  srli s2, t1, 16      # the next state
        addi a0, a0, 1
        bne  s2, t3, step
        la   t0, tape        # count the 1s
        li   t1, 1024
        li   a1, 0
count:  lbu  t2, 0(t0)
        add  a1, a1, t2
        addi t0, t0, 1
        addi t1, t1, -1
        bnez t1, count
        halt                 # a0 = steps, a1 = ones
        .align 4
rules:  {rules}
tape:   .space 1024
"""


def tm_program(tm) -> str:
    """TM_INTERP with a 2-symbol machine's table (explainer.cs.turing.TM) filled in."""
    states = [s for s in tm.states if s not in ("H", "Z", "halt")]
    num = {s: i for i, s in enumerate(states)}
    words = []
    for s in states:
        for sym in ("_", "1"):
            r = tm.match(s, (sym,))
            if r is None:
                words.append((255 << 16) | (1 << 8) | (1 if sym == "1" else 0))
                continue
            write = 1 if (r[2][0] == "1" or (r[2][0] == "=" and sym == "1")) else 0
            move = 1 if r[3][0] == "R" else 255
            nxt = 255 if r[4] in ("H", "Z", "halt") else num[r[4]]
            words.append((nxt << 16) | (move << 8) | write)
    return TM_INTERP.replace("{rules}", ".word " + ", ".join(str(w) for w in words))


SELFMOD = """
# Sum an array without an index register, as on EDSAC: the load instruction's own address field is the index.
        la   s0, array
        li   a1, 0           # the sum
        li   a2, 8           # elements left
        la   s1, load        # the instruction we rewrite
load:   lw   t0, 0(s0)       # its offset: rewritten
        add  a1, a1, t0
        lw   t1, 0(s1)       # the load, as data
        addi t1, t1, 4       # offset + 4
        sw   t1, 0(s1)       # back, as code
        addi a2, a2, -1
        bnez a2, load
        halt                 # a1 = 3 + 1 + 4 + 1 + 5 + 9 + 2 + 6 = 31
        .align 4
array:  .word 3, 1, 4, 1, 5, 9, 2, 6
"""


# ---------------------------------------------------------------------------
# Part 7's benchmarks: programs whose branches behave in different ways
# ---------------------------------------------------------------------------
def _words(vals) -> str:
    vals = list(vals)
    return "\n".join("        .word " + ", ".join(str(int(v)) for v in vals[k:k + 16]) for k in range(0, len(vals), 16))


def _bytes(vals) -> str:
    vals = list(vals)
    return "\n".join("        .byte " + ", ".join(str(int(v)) for v in vals[k:k + 32]) for k in range(0, len(vals), 32))


def insertion_sort(values) -> str:
    """Sort words in place: the inner loop's exit depends on the data."""
    return f"""
        la   s0, arr
        li   s1, {len(values)}
        li   t0, 1            # i
outer:  bge  t0, s1, done
        slli t1, t0, 2
        add  t1, t1, s0       # &a[i]
        lw   a0, 0(t1)        # the key
        mv   t2, t1
inner:  beq  t2, s0, place
        lw   a1, -4(t2)
        bge  a0, a1, place    # the data decides
        sw   a1, 0(t2)
        addi t2, t2, -4
        j    inner
place:  sw   a0, 0(t2)
        addi t0, t0, 1
        j    outer
done:   halt
        .align 4
arr:
{_words(values)}
"""


def sieve(n: int) -> str:
    """Count the primes below n (Eratosthenes, marking from p*p: uses mul)."""
    return f"""
        la   s0, flags
        li   s1, {n}
        li   t0, 2
        li   a0, 0            # primes found
outer:  bge  t0, s1, done
        add  t1, s0, t0
        lbu  t2, 0(t1)
        bnez t2, next         # crossed off?
        addi a0, a0, 1
        mul  t3, t0, t0
        bge  t3, s1, next
mark:   add  t1, s0, t3
        li   t2, 1
        sb   t2, 0(t1)
        add  t3, t3, t0
        blt  t3, s1, mark
next:   addi t0, t0, 1
        j    outer
done:   halt
flags:  .space {n}
"""


def threshold(data, passes: int = 1, branchless: bool = False) -> str:
    """Sum the bytes that are at least 128: the sorted-array puzzle.  ``branchless`` turns the if into arithmetic:
    a mask of all ones or all zeros from the comparison."""
    body = """        sltiu t3, t2, 128     # 1 if small
        addi t3, t3, -1       # all ones if big, 0 if small
        and  t3, t3, t2
        add  a0, a0, t3""" if branchless else """        sltiu t3, t2, 128
        bnez t3, skip         # the data decides
        add  a0, a0, t2
skip:"""
    return f"""
        la   s0, data
        li   s1, {len(data)}
        li   s2, {passes}
        li   a0, 0            # the sum
pass:   mv   t0, s0
        mv   t1, s1
loop:   lbu  t2, 0(t0)
{body}
        addi t0, t0, 1
        addi t1, t1, -1
        bnez t1, loop
        addi s2, s2, -1
        bnez s2, pass
        halt
data:
{_bytes(data)}
"""


def fib(n: int) -> str:
    """Recursive Fibonacci: calls and returns, nested deep (the return-address stack)."""
    return f"""
        li   a0, {n}
        call fib
        halt
fib:    li   t0, 2
        blt  a0, t0, base     # fib(0) = 0, fib(1) = 1
        addi sp, sp, -12
        sw   ra, 0(sp)
        sw   a0, 4(sp)
        addi a0, a0, -1
        call fib
        sw   a0, 8(sp)
        lw   a0, 4(sp)
        addi a0, a0, -2
        call fib
        lw   t0, 8(sp)
        add  a0, a0, t0
        lw   ra, 0(sp)
        addi sp, sp, 12
base:   ret
"""


def correlated(iterations: int, noise: int = 3) -> str:
    """Branch A tests a random bit; ``noise`` branches test other random bits; branch B tests A's bit again.  B is
    unpredictable alone, and certain given the outcome noise + 1 branches back.  The bits are the top bits of a
    linear congruential generator (x <- 1103515245 x + 12345, with Part 7's mul): unlike an LFSR's, they cannot be
    read off the outcomes of earlier branches."""
    noise_code = "\n".join(f"""        srli t2, s0, {29 - k}
        andi t2, t2, 1
        beqz t2, n{k}         # noise
        addi a1, a1, 1
n{k}:""" for k in range(noise))
    return f"""
        li   s0, 12345        # the generator's state
        li   s1, {iterations}
        li   s2, 1103515245
        li   a0, 0
        li   a1, 0
loop:   mul  s0, s0, s2       # the next random number
        addi s0, s0, 12345
        srli t0, s0, 30
        andi t0, t0, 1        # a random bit x
        beqz t0, a_no         # branch A: on x
        addi a2, a2, 1
a_no:
{noise_code}
        beqz t0, b_no         # branch B: on x again
        addi a0, a0, 1
b_no:   addi s1, s1, -1
        bnez s1, loop
        halt
"""


def parity(iterations: int, noise: int = 2) -> str:
    """Branches A and C test two independent random bits x and y; ``noise`` branches test others; branch B tests
    x xor y.  B is certain given A and C, but not linearly: no perceptron weights separate it (Minsky and Papert's
    XOR), while a table indexed by the history learns it."""
    noise_code = "\n".join(f"""        srli t2, s0, {28 - k}
        andi t2, t2, 1
        beqz t2, n{k}         # noise
        addi a1, a1, 1
n{k}:""" for k in range(noise))
    return f"""
        li   s0, 12345        # the generator's state
        li   s1, {iterations}
        li   s2, 1103515245
        li   a0, 0
        li   a1, 0
loop:   mul  s0, s0, s2       # the next random number
        addi s0, s0, 12345
        srli t0, s0, 30
        andi t0, t0, 1        # x
        srli t1, s0, 29
        andi t1, t1, 1        # y
        beqz t0, a_no         # branch A: on x
        addi a2, a2, 1
a_no:   beqz t1, c_no         # branch C: on y
        addi a3, a3, 1
c_no:
{noise_code}
        xor  t3, t0, t1
        beqz t3, b_no         # branch B: on x xor y
        addi a0, a0, 1
b_no:   addi s1, s1, -1
        bnez s1, loop
        halt
"""


def decimal(limit: int, use_div: bool) -> str:
    """Print 1 .. limit in decimal: by repeated subtraction of powers of ten (as the Job does), or with div and rem."""
    head = f"""
        li   s0, 1
        li   s1, {limit + 1}
        li   s2, {IO_CONSOLE:#x}
"""
    if use_div:
        return head + """        li   a5, 10
        la   a4, bufend
num:    mv   t0, s0
        mv   t1, a4
dig:    rem  t2, t0, a5       # the last digit
        div  t0, t0, a5
        addi t2, t2, 48
        addi t1, t1, -1
        sb   t2, 0(t1)
        bnez t0, dig
out:    lbu  t2, 0(t1)
        sb   t2, 0(s2)
        addi t1, t1, 1
        bne  t1, a4, out
        sb   a5, 0(s2)        # a newline
        addi s0, s0, 1
        bne  s0, s1, num
        halt
buf:    .space 12
bufend:
"""
    return head + """        la   a4, pow10
num:    mv   t1, s0
        mv   t0, a4
        li   a2, 0            # a digit printed yet?
pnext:  lw   t2, 0(t0)
        beqz t2, pend
        li   a5, 48
psub:   bltu t1, t2, pdig
        sub  t1, t1, t2
        addi a5, a5, 1
        j    psub
pdig:   li   a1, 48
        bne  a5, a1, pout
        bnez a2, pout
        li   a1, 1
        beq  t2, a1, pout
        j    pskip
pout:   sb   a5, 0(s2)
        li   a2, 1
pskip:  addi t0, t0, 4
        j    pnext
pend:   li   a5, 10
        sb   a5, 0(s2)
        addi s0, s0, 1
        bne  s0, s1, num
        halt
        .align 4
pow10:  .word 1000000000, 100000000, 10000000, 1000000, 100000, 10000, 1000, 100, 10, 1, 0
"""


# ---------------------------------------------------------------------------
# Part 8: Spectre, variant 1 (Kocher et al., 2019), against Pebble's out-of-order core
# ---------------------------------------------------------------------------
SPECTRE_ARRAY1 = 0x4000  # 16 bytes the victim may read, all zero; the secret follows in the same 64-byte line
SPECTRE_SIZE = 0x5000  # the victim's bound, on a line of its own
SPECTRE_PROBE = 0x10000  # 256 lines of 64 bytes: one per possible byte value


def spectre(n_secret: int, mitigation: str | None = None, train: int = 6) -> str:
    """Leak ``n_secret`` bytes stored after array1 through a bounds check, one byte a round:

    train the check with in-bounds calls; flush the bound from the cache, so the check takes a whole memory access;
    call with an out-of-bounds index; then time a read of every probe line, and print the index of the fastest.
    ``mitigation``: "fence" puts a speculation barrier (a read of the cycle counter) after the check; "mask" clamps
    the index with arithmetic that depends on the bound (Linux's array_index_nospec)."""
    if mitigation == "fence":
        guard = """        lw   t3, 8(a5)           # a barrier: nothing younger runs until the check has committed
"""
    elif mitigation == "mask":
        guard = """        sltu t3, a0, t2          # 1 if in bounds
        sub  t3, zero, t3        # all ones if in bounds, else zero
        and  a0, a0, t3          # an out-of-bounds index becomes 0, even on a wrong path
"""
    else:
        guard = ""
    return f"""
        li   s0, {SPECTRE_ARRAY1}
        li   s1, {SPECTRE_SIZE}
        li   s2, {SPECTRE_PROBE}
        li   a5, {IO_BASE:#x}
        li   a1, 0               # which secret byte
        li   a2, {n_secret}
        li   t1, 256
rounds: beq  a1, a2, done
        li   t0, 0               # flush the probe lines
flush:  slli t2, t0, 6
        add  t2, t2, s2
        sw   t2, 12(a5)          # (model device) evict this line
        addi t0, t0, 1
        bne  t0, t1, flush
        li   t0, {train}         # train the bounds check: in-bounds calls
train:  andi a0, t0, 15
        call victim
        addi t0, t0, -1
        bnez t0, train
        sw   s1, 12(a5)          # evict the bound: the next check waits for memory
        lw   t2, 8(a5)           # a barrier, so the eviction happens before the call (x86 needs mfence here)
        addi a0, a1, 16          # the attack: an index past the end of array1
        call victim
        li   t0, 1               # time every probe line but line 0 (array1 holds zeros)
        li   a3, 0x7fffffff
        li   a4, 0
time:   slli t2, t0, 6
        add  t2, t2, s2
        lw   t3, 8(a5)           # the cycle counter
        lbu  a0, 0(t2)
        lw   a0, 8(a5)
        sub  a0, a0, t3
        bgeu a0, a3, slower
        mv   a3, a0
        mv   a4, t0
slower: addi t0, t0, 1
        bne  t0, t1, time
        sb   a4, 0(a5)           # print the byte whose line was fast
        addi a1, a1, 1
        j    rounds
done:   halt
victim: lw   t2, 0(s1)           # array1_size
        bgeu a0, t2, out         # the bounds check
{guard}        add  t3, s0, a0
        lbu  t3, 0(t3)           # array1[x]
        slli t3, t3, 6
        add  t3, t3, s2
        lbu  t3, 0(t3)           # probe[array1[x] * 64]
out:    ret
"""


def spectre_image(secret: bytes, mitigation: str | None = None, train: int = 6) -> bytes:
    """The assembled attack with its data: array1 (zeros), the secret after it, and the bound 16."""
    from .asm import assemble

    img = bytearray(assemble(spectre(len(secret), mitigation, train)).image)
    img.extend(bytes(max(0, SPECTRE_SIZE + 4 - len(img))))
    img[SPECTRE_ARRAY1 + 16: SPECTRE_ARRAY1 + 16 + len(secret)] = secret
    img[SPECTRE_SIZE: SPECTRE_SIZE + 4] = (16).to_bytes(4, "little")
    return bytes(img)
