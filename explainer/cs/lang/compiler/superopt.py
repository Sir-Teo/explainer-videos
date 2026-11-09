"""A superoptimizer and a rule checker for Part 13's Frontier chapter.

* :func:`search` explores a restricted Pebble instruction vocabulary in increasing body length, keeping
  candidates that agree with the target on finite test inputs. Prefixes with equal test observations are merged;
  that pruning is incomplete, so a first-found length is not a minimum-length certificate. The caller must use
  :func:`prove` to check each candidate against a 32-bit SMT specification. Testing finds candidates; logic checks
  the encoded function, not timing, memory, physical registers or a complete external toolchain.
* :func:`check_rule` proves or refutes a rewrite rule over 32-bit machine integers (the idea of Alive, Lopes et al.
  2015, which found bugs in LLVM's peephole optimizer this way): ``x * 8 → x << 3`` holds for every x;
  ``x / 2 → x >> 1`` does not, and z3 says which x breaks it.
"""
from __future__ import annotations

import itertools

import z3

MASK = 0xFFFF_FFFF


def s32(v):
    v &= MASK
    return v - (1 << 32) if v & 0x8000_0000 else v


RR = {
    "add": lambda a, b: (a + b) & MASK, "sub": lambda a, b: (a - b) & MASK, "and": lambda a, b: a & b,
    "or": lambda a, b: a | b, "xor": lambda a, b: a ^ b, "sll": lambda a, b: (a << (b & 31)) & MASK,
    "srl": lambda a, b: a >> (b & 31), "sra": lambda a, b: (s32(a) >> (b & 31)) & MASK,
    "slt": lambda a, b: int(s32(a) < s32(b)), "sltu": lambda a, b: int(a < b),
    "mul": lambda a, b: (a * b) & MASK,
}
RI = [("addi", 1), ("addi", -1), ("xori", -1), ("srai", 31), ("srli", 31), ("srai", 1), ("srli", 1), ("slli", 1),
      ("sltiu", 1), ("andi", 1), ("slti", 1)]


def ri(op, a, imm):
    if op == "addi":
        return (a + imm) & MASK
    if op == "xori":
        return a ^ (imm & MASK)
    if op == "andi":
        return a & (imm & MASK)
    if op == "srai":
        return (s32(a) >> imm) & MASK
    if op == "srli":
        return a >> imm
    if op == "slli":
        return (a << imm) & MASK
    if op == "sltiu":
        return int(a < (imm & MASK))
    if op == "slti":
        return int(s32(a) < imm)
    raise KeyError(op)


EDGE = [0, 1, 2, 3, 7, 0x7FFF_FFFF, 0x8000_0000, 0x8000_0001, 0xFFFF_FFFF, 0xFFFF_FFFE, 12345, 0xDEAD_BEEF,
        100, 0xFFFF_FF9C, 64, 65]


def search(target, arity: int = 1, max_len: int = 3, ops=None, tests=None, limit: int = 5):
    """Return finite-test candidates at the first found length, with no minimality/completeness guarantee.

    Inputs are unsigned 32-bit words. A program lists (op, dst, a, b_or_imm) over registers x, y, zero,
    t1, t2... The caller must separately prove semantic equivalence with :func:`prove`.
    """
    import random
    rng = random.Random(1)
    if tests is None:
        if arity == 1:
            tests = [(v,) for v in EDGE] + [(rng.getrandbits(32),) for _ in range(16)]
        else:
            vals = EDGE[:10]
            tests = [(a, b) for a in vals[:6] for b in vals[:6]] + [(rng.getrandbits(32), rng.getrandbits(32))
                                                                    for _ in range(24)]
    want = tuple(target(*t) & MASK for t in tests)
    names = ["x", "y"][:arity]
    base = {"zero": tuple(0 for _ in tests)}
    for k, n in enumerate(names):
        base[n] = tuple(t[k] for t in tests)
    ops = ops or list(RR)
    found = []

    def steps(regs):
        vals = list(regs.items())
        for op in ops:
            f = RR[op]
            for (na, va), (nb, vb) in itertools.product(vals, vals):
                yield (op, na, nb), tuple(f(a, b) for a, b in zip(va, vb))
        for op, imm in RI:
            for na, va in vals:
                yield (op, na, imm), tuple(ri(op, a, imm) for a in va)

    for length in range(1, max_len + 1):
        # depth-first over prefixes of length-1, then try every last step
        def dfs(regs, prog, depth):
            if depth == length - 1:
                for ins, v in steps(regs):
                    if v == want:
                        found.append(prog + [(ins[0], f"t{depth + 1}", ins[1], ins[2])])
                        if len(found) >= limit:
                            return True
                return False
            seen = set(regs.values())
            for ins, v in steps(regs):
                if v in seen:
                    continue
                seen.add(v)
                nr = dict(regs)
                nr[f"t{depth + 1}"] = v
                if dfs(nr, prog + [(ins[0], f"t{depth + 1}", ins[1], ins[2])], depth + 1):
                    return True
            return False
        dfs(dict(base), [], 0)
        if found:
            return length, found
    return None, []


def z3_eval(prog, inputs: dict):
    env = dict(inputs)
    env["zero"] = z3.BitVecVal(0, 32)
    one, zero = z3.BitVecVal(1, 32), z3.BitVecVal(0, 32)
    for op, dst, a, b in prog:
        A = env[a]
        if op in RR:
            B = env[b]
            r = {"add": A + B, "sub": A - B, "and": A & B, "or": A | B, "xor": A ^ B,
                 "sll": A << (B & 31), "srl": z3.LShR(A, B & 31), "sra": A >> (B & 31),
                 "slt": z3.If(A < B, one, zero), "sltu": z3.If(z3.ULT(A, B), one, zero), "mul": A * B}[op]
        else:
            imm = z3.BitVecVal(b & MASK, 32)
            r = {"addi": A + imm, "xori": A ^ imm, "andi": A & imm, "srai": A >> b, "srli": z3.LShR(A, b),
                 "slli": A << b, "sltiu": z3.If(z3.ULT(A, imm), one, zero),
                 "slti": z3.If(A < imm, one, zero)}[op]
        env[dst] = r
    return env[prog[-1][1]]


def prove(prog, spec, arity: int = 1):
    """Is prog equal to spec (a function of z3 32-bit vectors) for every input?  Returns (True, None) or (False,
    counterexample)."""
    xs = [z3.BitVec(n, 32) for n in ("x", "y")[:arity]]
    out = z3_eval(prog, dict(zip(("x", "y"), xs)))
    s = z3.Solver()
    s.add(out != spec(*xs))
    if s.check() == z3.unsat:
        return True, None
    m = s.model()
    return False, [m.eval(x, model_completion=True).as_signed_long() for x in xs]


def check_rule(lhs, rhs, arity: int = 1):
    """Prove lhs == rhs over 32-bit integers, or return a counterexample (signed values)."""
    xs = [z3.BitVec(n, 32) for n in ("x", "y")[:arity]]
    s = z3.Solver()
    s.add(lhs(*xs) != rhs(*xs))
    if s.check() == z3.unsat:
        return True, None
    m = s.model()
    return False, [m.eval(x, model_completion=True).as_signed_long() for x in xs]


def show(prog) -> list:
    out = []
    for op, dst, a, b in prog:
        out.append(f"{op:<5} {dst}, {a}, {b}")
    return out
