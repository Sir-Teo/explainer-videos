"""A reference interpreter for the IR: what a program means, against which every pass and the machine code are
checked (Part 13's differential tests, and chapter 15's fuzzer).

Memory is a flat little-endian byte array, as on Pebble: globals from address 64, the heap (``alloc``) above them,
the stack growing down from the top.  Arithmetic wraps at 32 bits; division truncates toward zero, as Pebble's
``div`` does; division by zero is undefined in the language and traps here, as it does on Pebble.
"""
from __future__ import annotations

from explainer.cs.lang.compiler.ir import Module, is_var

MASK = 0xFFFF_FFFF


def s32(v: int) -> int:
    v &= MASK
    return v - (1 << 32) if v & 0x8000_0000 else v


def binop(op: str, a: int, b: int) -> int:
    a, b = s32(a), s32(b)
    ua, ub = a & MASK, b & MASK
    if op == "add":
        return s32(a + b)
    if op == "sub":
        return s32(a - b)
    if op == "mul":
        return s32(a * b)
    if op == "div":
        if b == 0:
            raise Stuck("division by zero")
        q = abs(a) // abs(b)
        return s32(q if (a >= 0) == (b >= 0) else -q)
    if op == "rem":
        if b == 0:
            raise Stuck("division by zero")
        q = binop("div", a, b)
        return s32(a - q * b)
    if op == "and":
        return s32(a & b)
    if op == "or":
        return s32(a | b)
    if op == "xor":
        return s32(a ^ b)
    if op == "shl":
        return s32(ua << (ub & 31))
    if op == "shr":
        return s32(ua >> (ub & 31))
    if op == "sar":
        return s32(a >> (ub & 31))
    return int({"lt": a < b, "le": a <= b, "gt": a > b, "ge": a >= b, "eq": a == b, "ne": a != b,
                "ltu": ua < ub, "leu": ua <= ub, "gtu": ua > ub, "geu": ua >= ub}[op])


class Stuck(RuntimeError):
    pass


class Interp:
    def __init__(self, m: Module, tape: bytes = b"", mem_size: int = 1 << 20, max_steps: int = 50_000_000):
        self.m = m
        self.tape, self.tp = tape, 0
        self.mem = bytearray(mem_size)
        self.out = bytearray()
        self.steps = 0
        self.max_steps = max_steps
        self.counts: dict = {}
        self.gaddr = {}
        a = 64
        for name, (size, align, init) in m.globals.items():
            a = (a + align - 1) // align * align
            self.gaddr[name] = a
            if init is not None:
                self.mem[a:a + 4] = (init & MASK).to_bytes(4, "little")
            a += size
        self.brk = (a + 15) // 16 * 16
        self.sp = mem_size
        self.funcs = {f.name: f for f in m.funcs}

    def load(self, addr: int, size: int) -> int:
        addr &= MASK
        if addr + size > len(self.mem) or addr < 64:
            raise Stuck(f"load from {addr:#x}")
        if size == 4:
            return s32(int.from_bytes(self.mem[addr:addr + 4], "little"))
        return self.mem[addr]

    def store(self, addr: int, size: int, v: int):
        addr &= MASK
        if addr + size > len(self.mem) or addr < 64:
            raise Stuck(f"store to {addr:#x}")
        if size == 4:
            self.mem[addr:addr + 4] = (v & MASK).to_bytes(4, "little")
        else:
            self.mem[addr] = v & 0xFF

    def run(self, entry: str = "main"):
        return self.call(entry, [])

    def call(self, name: str, args: list) -> int:
        if name == "alloc":
            n = (args[0] + 3) // 4 * 4
            p = self.brk
            self.brk += n
            if self.brk > self.sp - 4096:
                raise Stuck("out of heap")
            return p
        f = self.funcs[name]
        env = dict(zip(f.params, args))
        frame = {}
        sp0 = self.sp
        for slot, (size, align) in f.slots.items():
            self.sp = (self.sp - size) // max(align, 4) * max(align, 4)
            frame[slot] = self.sp
            self.mem[self.sp:self.sp + size] = bytes(size)
        lab = f.labels()
        b, prev = f.blocks[0], None
        val = lambda x: env[x] if is_var(x) else x
        while True:
            phis = [i for i in b.ins if i.op == "phi"]
            if phis:
                new = {}
                for i in phis:
                    new[i.dst] = val(i.args[i.k.index(prev)])
                env.update(new)
            for i in b.ins:
                op = i.op
                if op == "phi":
                    continue
                self.steps += 1
                if self.steps > self.max_steps:
                    raise Stuck("too many steps")
                self.counts[op] = self.counts.get(op, 0) + 1
                if op == "const":
                    env[i.dst] = i.k
                elif op == "copy":
                    env[i.dst] = val(i.args[0])
                elif op == "bin":
                    env[i.dst] = binop(i.k, val(i.args[0]), val(i.args[1]))
                elif op == "un":
                    v = val(i.args[0])
                    env[i.dst] = s32(-v) if i.k == "neg" else int(v == 0)
                elif op == "load":
                    size, off = i.k
                    env[i.dst] = self.load(val(i.args[0]) + off, size)
                elif op == "store":
                    size, off = i.k
                    self.store(val(i.args[0]) + off, size, val(i.args[1]))
                elif op == "gaddr":
                    env[i.dst] = self.gaddr[i.k]
                elif op == "faddr":
                    env[i.dst] = frame[i.k]
                elif op == "call":
                    r = self.call(i.k, [val(a) for a in i.args])
                    if i.dst:
                        env[i.dst] = r
                elif op == "getc":
                    if self.tp < len(self.tape):
                        env[i.dst] = self.tape[self.tp]
                        self.tp += 1
                    else:
                        env[i.dst] = -1
                elif op == "putc":
                    self.out.append(val(i.args[0]) & 0xFF)
                elif op == "br":
                    prev, b = b.label, lab[i.k]
                    break
                elif op == "cbr":
                    prev, b = b.label, lab[i.k[0] if val(i.args[0]) != 0 else i.k[1]]
                    break
                elif op == "ret":
                    self.sp = sp0
                    return s32(val(i.args[0])) if i.args else 0
                else:
                    raise Stuck(f"unknown op {op}")


def run(m: Module, tape: bytes = b"", **kw) -> Interp:
    it = Interp(m, tape, **kw)
    it.result = it.run()
    return it
