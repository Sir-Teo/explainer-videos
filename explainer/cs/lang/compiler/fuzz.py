"""Random programs for differential testing, in the spirit of Csmith (Yang, Chen, Eide and Regehr, 2011): every
program generated here is well defined in the Pebble language (loops are bounded, indices are reduced into range,
pointers only ever point at globals or into arrays that are alive), so any two correct implementations must print
the same bytes.  :func:`differential` runs one program through the IR interpreter and through the compiler at
every level on the emulator, and reports any disagreement (Part 13, chapter 15).
"""
from __future__ import annotations

import random

from explainer.cs.lang import pebble_lang as P


class Gen:
    def __init__(self, seed: int, funcs: int = 4, depth: int = 3):
        self.r = random.Random(seed)
        self.nf = funcs
        self.depth = depth
        self.n = 0

    def name(self, p="v"):
        self.n += 1
        return f"{p}{self.n}"

    def lit(self):
        r = self.r.random()
        if r < 0.6:
            return str(self.r.randint(0, 20))
        if r < 0.8:
            return str(self.r.randint(-100, 100)).replace("-", "- ") if False else f"(0 - {self.r.randint(1, 100)})"
        return str(self.r.choice([127, 255, 256, 1023, 65535, 131071, 262143, 1 << 20, 2147483647]))

    def expr(self, scope, d, fi):
        r = self.r.random()
        if d <= 0 or r < 0.25:
            if scope and self.r.random() < 0.7:
                return self.r.choice(scope)
            return self.lit()
        if r < 0.65:
            op = self.r.choice(["+", "-", "*", "/", "%", "+", "-", "*"])
            if op in ("/", "%"):          # e*e + 1 is never 0 or -1 modulo 2^32: no trap, no overflow
                d2 = self.expr(scope, d - 1, fi)
                return f"({self.expr(scope, d - 1, fi)} {op} ({d2} * {d2} + 1))"
            return f"({self.expr(scope, d - 1, fi)} {op} {self.expr(scope, d - 1, fi)})"
        if r < 0.8:
            op = self.r.choice(["<", "<=", ">", ">=", "==", "!=", "&&", "||"])
            return f"({self.expr(scope, d - 1, fi)} {op} {self.expr(scope, d - 1, fi)})"
        if r < 0.87:
            return f"(-{self.expr(scope, d - 1, fi)})" if self.r.random() < 0.5 else f"(!{self.expr(scope, d - 1, fi)})"
        if r < 0.95 and fi > 1:
            g = self.r.randint(1, fi - 1)
            return f"f{g}({self.expr(scope, d - 1, fi)}, {self.expr(scope, d - 1, fi)})"
        return self.r.choice(["g0", "g1", "g2", "arr[" + self.idx(scope, fi) + "]"]) if fi else "g0"

    def idx(self, scope, fi):
        return f"(({self.expr(scope, 1, fi)}) % 8 + 8) % 8"

    def stmts(self, scope, d, fi, budget):
        out = []
        for _ in range(self.r.randint(1, budget)):
            out += self.stmt(scope, d, fi)
        return out

    def stmt(self, scope, d, fi):
        r = self.r.random()
        if r < 0.3 or d <= 0:
            if scope and self.r.random() < 0.6:
                return [f"{self.r.choice(scope)} = {self.expr(scope, self.depth, fi)};"]
            tgt = self.r.choice(["g0", "g1", "g2", "arr[" + self.idx(scope, fi) + "]", "*gp", "buf[" +
                                 self.idx(scope, fi) + "]"])
            return [f"{tgt} = {self.expr(scope, self.depth, fi)};"]
        if r < 0.45:
            v = self.name()
            scope.append(v)
            return [f"var {v}: int = {self.expr(scope[:-1], self.depth, fi)};"]
        if r < 0.65:
            c = self.expr(scope, 2, fi)
            body = self.stmts(list(scope), d - 1, fi, 3)
            out = [f"if {c} {{"] + ["    " + s for s in body] + ["}"]
            if self.r.random() < 0.5:
                eb = self.stmts(list(scope), d - 1, fi, 3)
                out[-1] = "} else {"
                out += ["    " + s for s in eb] + ["}"]
            return out
        if r < 0.85:
            i = self.name("i")
            n = self.r.randint(0, 3)
            inner = list(scope) + [i]
            body = self.stmts(list(inner), d - 1, fi, 3)
            if self.r.random() < 0.2:
                body.append(f"if {self.expr(inner, 1, fi)} {{ break; }}")
            return [f"var {i}: int = 0;", f"while {i} < {n} {{"] + ["    " + s for s in body] + \
                [f"    {i} = {i} + 1;", "}"]
        if r < 0.92:
            return [f"gp = &arr[{self.idx(scope, fi)}];"] if self.r.random() < 0.5 else ["gp = &g1;"]
        v = self.name()
        scope.append(v)
        return [f"var {v}: int = {self.expr(scope[:-1], self.depth, fi)};",
                f"if {v} > 1000 {{ return {v} % 1000; }}"]

    def program(self) -> str:
        lines = ["var g0: int = 1;", "var g1: int = 2;", "var g2: int = 3;", "var arr: [8]int;", "var buf: [8]char;",
                 "var gp: *int = null;", ""]
        for fi in range(1, self.nf + 1):
            scope = ["a", "b"]
            body = self.stmts(scope, 2, fi, 6)
            lines.append(f"fn f{fi}(a: int, b: int) -> int {{")
            lines += ["    " + s for s in body]
            lines.append(f"    return {self.expr(scope, 2, fi)};")
            lines.append("}")
        lines += ["", "fn out(v: int) {", "    putc(v % 256); putc((v / 256) % 256); putc((v / 65536) % 256);",
                  "    putc((v / 16777216) % 256);", "}", "",
                  "fn main() -> int {", "    gp = &g1;"]
        for _ in range(4):
            fi = self.r.randint(1, self.nf)
            lines.append(f"    out(f{fi}({self.lit()}, {self.lit()}));")
        lines += ["    out(g0); out(g1); out(g2);", "    var k: int = 0;",
                  "    while k < 8 { out(arr[k]); out(buf[k]); k = k + 1; }", "    return 0;", "}"]
        return "\n".join(lines)


def program(seed: int, **kw) -> str:
    return Gen(seed, **kw).program()


def differential(src: str, levels=(0, 1, 2, 3), max_steps: int = 2_000_000) -> dict:
    """Run src through the IR interpreter and the compiler at each level.  Returns {'ref': bytes, level: bytes or
    an error string}; 'ok' is True when every level printed what the interpreter printed."""
    from explainer.cs.lang.compiler import check as C
    from explainer.cs.lang.compiler import driver as D
    from explainer.cs.lang.compiler import interp as IT
    from explainer.cs.lang.compiler import lower as L

    prog = P.parse(src)
    info = C.check(prog)
    m = L.lower(prog, info)
    try:
        ref = bytes(IT.run(m, b"", max_steps=max_steps).out)
    except IT.Stuck as e:
        return {"ok": None, "ref": f"stuck: {e}"}
    out = {"ref": ref}
    ok = True
    for lv in levels:
        try:
            c = D.compile_program(src, lv)
            r = bytes(D.run(c, b"", max_steps=max_steps * 8).output)
        except Exception as e:                     # noqa: BLE001 — any failure is a finding
            r = f"{type(e).__name__}: {e}"
        out[lv] = r
        ok &= r == ref
    out["ok"] = ok
    return out
