"""From the checked syntax tree to three-address code (Part 13, chapter 4).

Scalar locals whose address is never taken become virtual registers named after them (``%count``); everything
else, arrays, structs and address-taken scalars, gets a stack slot reached through ``faddr``.  Conditions are lowered
with jumps, so ``a && b`` evaluates ``b`` only when ``a`` holds; comparisons that feed a branch produce 0 or 1 here
and are fused into a single branch instruction by instruction selection.
"""
from __future__ import annotations

from explainer.cs.lang import pebble_lang as P
from explainer.cs.lang.compiler import check as C
from explainer.cs.lang.compiler.ir import Block, Func, I, Module, remove_unreachable

CMPOP = {"<": "lt", "<=": "le", ">": "gt", ">=": "ge", "==": "eq", "!=": "ne"}
BINOP = {"+": "add", "-": "sub", "*": "mul", "/": "div", "%": "rem"}


def lower(prog: P.Program, info: C.Info | None = None, rotate: bool = False) -> Module:
    info = info or C.check(prog)
    globs = {}
    for g in prog.globals:
        init = None
        if g.init is not None:
            e = g.init
            init = 0 if isinstance(e, P.Null) else (e.value if isinstance(e, (P.Num, P.CharLit)) else -e.e.value)
        globs[g.name] = (info.size(g.type), max(4, info.align(g.type)), init)
    funcs = [Lowerer(info, f, rotate).run() for f in prog.funcs]
    return Module(funcs, globs, info)


class Lowerer:
    def __init__(self, info: C.Info, f: P.Func, rotate: bool = False):
        self.info, self.f = info, f
        self.rotate = rotate
        self.locals = info.locals[f.name]
        self.taken = info.address_taken[f.name]
        self.blocks: list[Block] = []
        self.cur: Block | None = None
        self.n = 0
        self.slots: dict = {}
        self.loops: list = []

    # --- helpers ---------------------------------------------------------
    def tmp(self) -> str:
        self.n += 1
        return f"%t{self.n}"

    def label(self, hint="L") -> str:
        self.n += 1
        return f"{hint}{self.n}"

    def start(self, label: str):
        self.cur = Block(label)
        self.blocks.append(self.cur)

    def emit(self, op, dst=None, args=None, k=None) -> I:
        ins = I(op, dst, list(args or []), k)
        if self.cur.ins and self.cur.ins[-1].op in ("br", "cbr", "ret"):
            self.start(self.label("dead"))     # code after a return or break: unreachable, removed later
        self.cur.ins.append(ins)
        return ins

    def in_memory(self, u: str) -> bool:
        t = self.locals[u]
        return u in self.taken or t.kind in ("array", "struct")

    def slot(self, u: str):
        if u not in self.slots:
            t = self.locals[u]
            self.slots[u] = (self.info.size(t), max(4, self.info.align(t)))
        return u

    # --- functions ---------------------------------------------------------
    def run(self) -> Func:
        self.start("entry")
        params = []
        for name, t in self.f.params:
            v = f"%{name}"
            params.append(v)
            if self.in_memory(name):
                a = self.tmp()
                self.emit("faddr", a, k=self.slot(name))
                self.emit("store", None, [a, v], (self.info.size(t), 0))
        self.block(self.f.body)
        if not (self.cur.ins and self.cur.ins[-1].op in ("br", "cbr", "ret")):
            self.emit("ret", None, [0] if self.f.ret is not None else [])
        fn = Func(self.f.name, params, self.blocks, self.slots, self.f.ret is not None)
        remove_unreachable(fn)
        return fn

    # --- statements --------------------------------------------------------
    def block(self, b: P.Block):
        for s in b.stmts:
            self.stmt(s)

    def stmt(self, s):
        if isinstance(s, P.Var):
            u = s.unique
            if self.in_memory(u):
                self.slot(u)
                if s.init is not None:
                    self.assign_mem(*self.addr_of_local(u), self.locals[u], s.init)
            else:
                v = self.expr(s.init) if s.init is not None else 0
                self.emit("copy", f"%{u}", [v])
        elif isinstance(s, P.Assign):
            self.assign(s.target, s.value)
        elif isinstance(s, P.ExprStmt):
            self.expr(s.e, want=False)
        elif isinstance(s, P.Block):
            self.block(s)
        elif isinstance(s, P.If):
            then, after = self.label("then"), self.label("endif")
            els = self.label("else") if s.els is not None else after
            self.cond(s.cond, then, els)
            self.start(then)
            self.block(s.then)
            self.emit("br", k=after)
            if s.els is not None:
                self.start(els)
                self.stmt(s.els)
                self.emit("br", k=after)
            self.start(after)
        elif isinstance(s, P.While) and self.rotate:
            # loop inversion: test once on entry, then at the bottom, so each trip runs one branch, not two
            body, latch, after = self.label("body"), self.label("latch"), self.label("endwhile")
            self.cond(s.cond, body, after)
            self.start(body)
            self.loops.append((latch, after))
            self.block(s.body)
            self.loops.pop()
            self.emit("br", k=latch)
            self.start(latch)
            self.cond(s.cond, body, after)
            self.start(after)
        elif isinstance(s, P.While):
            head, body, after = self.label("while"), self.label("body"), self.label("endwhile")
            self.emit("br", k=head)
            self.start(head)
            self.cond(s.cond, body, after)
            self.start(body)
            self.loops.append((head, after))
            self.block(s.body)
            self.loops.pop()
            self.emit("br", k=head)
            self.start(after)
        elif isinstance(s, P.Return):
            self.emit("ret", None, [self.expr(s.e)] if s.e is not None else [])
        elif isinstance(s, P.Break):
            self.emit("br", k=self.loops[-1][1])
        elif isinstance(s, P.Continue):
            self.emit("br", k=self.loops[-1][0])
        else:
            raise NotImplementedError(s)

    def assign(self, target, value):
        if isinstance(target, P.Name) and target.kind == "local" and not self.in_memory(target.unique):
            self.emit("copy", f"%{target.unique}", [self.expr(value)])
            return
        base, off = self.addr(target)
        self.assign_mem(base, off, target.ty, value)

    def assign_mem(self, base, off, t, value):
        if t.kind in ("struct", "array"):
            raise NotImplementedError("struct and array assignment")
        v = self.expr(value)
        self.emit("store", None, [base, v], (self.info.size(t), off))

    # --- addresses -----------------------------------------------------------
    def addr_of_local(self, u: str):
        a = self.tmp()
        self.emit("faddr", a, k=self.slot(u))
        return a, 0

    def addr(self, e):
        """(base operand, constant offset) of an lvalue that lives in memory."""
        if isinstance(e, P.Name):
            if e.kind == "global":
                a = self.tmp()
                self.emit("gaddr", a, k=e.unique)
                return a, 0
            return self.addr_of_local(e.unique)
        if isinstance(e, P.Unary) and e.op == "*":
            return self.expr(e.e), 0
        if isinstance(e, P.Field):
            if e.via == "pointer":
                return self.expr(e.e), e.offset
            base, off = self.addr(e.e)
            return base, off + e.offset
        if isinstance(e, P.Index):
            if e.in_place:
                base, off = self.addr(e.a)
            else:
                base, off = self.expr(e.a), 0
            i = self.expr(e.i)
            if isinstance(i, int):
                return base, off + i * e.scale
            scaled = i
            if e.scale != 1:
                scaled = self.tmp()
                self.emit("bin", scaled, [i, e.scale], "mul")
            a = self.tmp()
            self.emit("bin", a, [base, scaled], "add")
            return a, off
        raise NotImplementedError(f"address of {e}")

    # --- expressions -----------------------------------------------------------
    def expr(self, e, want=True):
        if isinstance(e, (P.Num, P.CharLit)):
            return e.value
        if isinstance(e, P.Null):
            return 0
        if isinstance(e, P.SizeOf):
            return e.size
        if isinstance(e, P.Name):
            if e.kind == "local" and not self.in_memory(e.unique):
                return f"%{e.unique}"
            return self.load(e)
        if isinstance(e, (P.Field, P.Index)) or (isinstance(e, P.Unary) and e.op == "*"):
            return self.load(e)
        if isinstance(e, P.Unary):
            if e.op == "&":
                base, off = self.addr(e.e)
                if off == 0:
                    return base
                d = self.tmp()
                self.emit("bin", d, [base, off], "add")
                return d
            v = self.expr(e.e)
            d = self.tmp()
            self.emit("un", d, [v], "neg" if e.op == "-" else "not")
            return d
        if isinstance(e, P.Binary):
            if e.op in ("&&", "||"):
                return self.bool_value(e)
            a, b = self.expr(e.l), self.expr(e.r)
            d = self.tmp()
            if e.op in CMPOP:
                op = CMPOP[e.op]
                if getattr(e, "unsigned", False) and op not in ("eq", "ne"):
                    op += "u"
                self.emit("bin", d, [a, b], op)
            elif getattr(e, "scale", 1) != 1 and e.op in ("+", "-"):
                s = self.tmp()
                self.emit("bin", s, [b, e.scale], "mul")
                self.emit("bin", d, [a, s], BINOP[e.op])
            else:
                self.emit("bin", d, [a, b], BINOP[e.op])
            return d
        if isinstance(e, P.Call):
            name = e.f.id
            args = [self.expr(a) for a in e.args]
            if name == "getc":
                d = self.tmp()
                self.emit("getc", d)
                return d
            if name == "putc":
                self.emit("putc", None, args)
                return 0
            d = self.tmp() if (e.sig.ret is not None) else None
            self.emit("call", d, args, name)
            return d if d is not None else 0
        raise NotImplementedError(e)

    def load(self, e):
        t = e.ty
        if t.kind in ("array", "struct"):
            raise NotImplementedError("using a whole array or struct as a value")
        base, off = self.addr(e)
        d = self.tmp()
        self.emit("load", d, [base], (self.info.size(t), off))
        return d

    def bool_value(self, e):
        d = self.tmp()
        yes, no, done = self.label("true"), self.label("false"), self.label("bool")
        self.cond(e, yes, no)
        self.start(yes)
        self.emit("copy", d, [1])
        self.emit("br", k=done)
        self.start(no)
        self.emit("copy", d, [0])
        self.emit("br", k=done)
        self.start(done)
        return d

    def cond(self, e, yes: str, no: str):
        if isinstance(e, P.Binary) and e.op == "&&":
            mid = self.label("and")
            self.cond(e.l, mid, no)
            self.start(mid)
            self.cond(e.r, yes, no)
            return
        if isinstance(e, P.Binary) and e.op == "||":
            mid = self.label("or")
            self.cond(e.l, yes, mid)
            self.start(mid)
            self.cond(e.r, yes, no)
            return
        if isinstance(e, P.Unary) and e.op == "!":
            self.cond(e.e, no, yes)
            return
        v = self.expr(e)
        self.emit("cbr", None, [v], (yes, no))
