"""Semantic analysis for the Pebble language (Part 13, chapter 3): scopes, symbol tables, types, struct layout.

Types are :class:`explainer.cs.lang.pebble_lang.Type`.  Sizes: ``int`` 4, ``char`` 1, pointers 4, arrays n × element,
structs laid out in field order with natural alignment (so ``Node`` is 16 bytes, exactly Part 11's node).  The rules
are C's, simplified:

* ``int`` and ``char`` mix freely in arithmetic (characters widen to int; an int stored into a char is truncated);
* a pointer may be compared with a pointer or ``null``; ``p + i`` and ``p[i]`` scale by the element size;
* ``x.f`` works on a struct or a pointer to one (Go's automatic dereference);
* ``alloc(n)`` returns a pointer of no particular type, assignable to any pointer, as does ``null``;
* the builtins are ``getc() -> int``, ``putc(c: int)`` and ``alloc(n: int) -> *any``.

:func:`check` annotates every expression node with ``.ty`` (and lvalues with ``.lv``) and returns an :class:`Info`
with the struct layouts, globals and function signatures, or raises :class:`TypeError_` naming the line.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from explainer.cs.lang import pebble_lang as P
from explainer.cs.lang.pebble_lang import Type

INT = Type("int")
CHAR = Type("char")
ANYPTR = Type("ptr", None)          # null and alloc's result


class TypeError_(ValueError):
    pass


@dataclass
class StructInfo:
    name: str
    fields: dict            # name -> (offset, Type)
    size: int
    align: int


@dataclass
class FuncSig:
    name: str
    params: list            # [(name, Type)]
    ret: Type | None
    builtin: bool = False


@dataclass
class Info:
    structs: dict = field(default_factory=dict)
    globals: dict = field(default_factory=dict)     # name -> Type
    funcs: dict = field(default_factory=dict)       # name -> FuncSig
    locals: dict = field(default_factory=dict)      # function name -> {unique name: Type}
    address_taken: dict = field(default_factory=dict)  # function name -> set of unique local names

    def size(self, t: Type) -> int:
        if t.kind == "int" or t.kind == "ptr":
            return 4
        if t.kind == "char":
            return 1
        if t.kind == "array":
            return t.n * self.size(t.of)
        if t.kind == "struct":
            return self.structs[t.name].size
        raise TypeError_(f"no size for {t}")

    def align(self, t: Type) -> int:
        if t.kind in ("int", "ptr"):
            return 4
        if t.kind == "char":
            return 1
        if t.kind == "array":
            return self.align(t.of)
        return self.structs[t.name].align


BUILTINS = {
    "getc": FuncSig("getc", [], INT, True),
    "putc": FuncSig("putc", [("c", INT)], None, True),
    "alloc": FuncSig("alloc", [("n", INT)], ANYPTR, True),
}


def same(a: Type, b: Type) -> bool:
    if a.kind != b.kind:
        return False
    if a.kind == "ptr":
        return a.of is None or b.of is None or same(a.of, b.of)
    if a.kind == "array":
        return a.n == b.n and same(a.of, b.of)
    if a.kind == "struct":
        return a.name == b.name
    return True


def is_scalar(t: Type) -> bool:
    return t.kind in ("int", "char")


def assignable(dst: Type, src: Type) -> bool:
    if is_scalar(dst) and is_scalar(src):
        return True
    if dst.kind == "ptr" and src.kind == "ptr":
        return same(dst, src)
    return False


def check(prog: P.Program) -> Info:
    info = Info()
    # structs, in order (a struct may contain pointers to any struct, values only of earlier ones)
    for s in prog.structs:
        off, al, fields = 0, 1, {}
        for fname, ft in s.fields:
            if ft.kind == "struct" and ft.name not in info.structs:
                raise TypeError_(f"struct {s.name}: field {fname} has incomplete type {ft}")
            a = 4 if ft.kind == "ptr" else info.align(ft)
            off = (off + a - 1) // a * a
            fields[fname] = (off, ft)
            off += 4 if ft.kind == "ptr" else info.size(ft)
            al = max(al, a)
        info.structs[s.name] = StructInfo(s.name, fields, (off + al - 1) // al * al, al)
    for g in prog.globals:
        if g.init is not None and not isinstance(g.init, (P.Num, P.Null, P.CharLit)) and not (
                isinstance(g.init, P.Unary) and g.init.op == "-" and isinstance(g.init.e, P.Num)):
            raise TypeError_(f"global {g.name}: initializer must be a constant")
        info.globals[g.name] = g.type
    info.funcs.update(BUILTINS)
    for f in prog.funcs:
        if f.name in info.funcs:
            raise TypeError_(f"function {f.name} defined twice")
        info.funcs[f.name] = FuncSig(f.name, f.params, f.ret)
    if "main" not in info.funcs:
        raise TypeError_("no function main")
    for f in prog.funcs:
        Checker(info, f).run()
    return info


class Checker:
    def __init__(self, info: Info, f: P.Func):
        self.info, self.f = info, f
        self.scopes: list[dict] = []
        self.locals: dict = {}
        self.taken: set = set()
        self.loop = 0
        self.counter = 0

    def run(self):
        self.scopes.append({})
        for name, t in self.f.params:
            self.declare(name, t, None)
        self.block(self.f.body, new_scope=False)
        self.info.locals[self.f.name] = self.locals
        self.info.address_taken[self.f.name] = self.taken

    # --- scopes ----------------------------------------------------------
    def declare(self, name: str, t: Type, node) -> str:
        if name in self.scopes[-1]:
            raise TypeError_(f"in {self.f.name}: {name} declared twice in one block")
        u = name if name not in self.locals else f"{name}.{self.counter}"
        self.counter += 1
        self.scopes[-1][name] = u
        self.locals[u] = t
        if node is not None:
            node.unique = u
        return u

    def lookup(self, name: str):
        for s in reversed(self.scopes):
            if name in s:
                return ("local", s[name], self.locals[s[name]])
        if name in self.info.globals:
            return ("global", name, self.info.globals[name])
        if name in self.info.funcs:
            return ("func", name, None)
        raise TypeError_(f"in {self.f.name}: {name} is not declared")

    # --- statements --------------------------------------------------------
    def block(self, b: P.Block, new_scope=True):
        if new_scope:
            self.scopes.append({})
        for s in b.stmts:
            self.stmt(s)
        if new_scope:
            self.scopes.pop()

    def stmt(self, s):
        if isinstance(s, P.Var):
            if s.init is not None:
                t = self.expr(s.init)
                if not assignable(s.type, t):
                    raise TypeError_(f"in {self.f.name}: cannot initialize {s.name}: {s.type} with {t}")
            self.declare(s.name, s.type, s)
        elif isinstance(s, P.Assign):
            t = self.expr(s.target)
            if not getattr(s.target, "lv", False):
                raise TypeError_(f"in {self.f.name}: cannot assign to that")
            v = self.expr(s.value)
            if not assignable(t, v):
                raise TypeError_(f"in {self.f.name}: cannot assign {v} to {t}")
        elif isinstance(s, P.ExprStmt):
            self.expr(s.e)
        elif isinstance(s, P.Block):
            self.block(s)
        elif isinstance(s, P.If):
            self.cond(s.cond)
            self.block(s.then)
            if s.els is not None:
                self.stmt(s.els)
        elif isinstance(s, P.While):
            self.cond(s.cond)
            self.loop += 1
            self.block(s.body)
            self.loop -= 1
        elif isinstance(s, P.Return):
            want = self.f.ret
            if s.e is None:
                if want is not None:
                    raise TypeError_(f"in {self.f.name}: return needs a value")
            else:
                t = self.expr(s.e)
                if want is None or not assignable(want, t):
                    raise TypeError_(f"in {self.f.name}: cannot return {t}")
        elif isinstance(s, (P.Break, P.Continue)):
            if not self.loop:
                raise TypeError_(f"in {self.f.name}: break or continue outside a loop")
        else:
            raise TypeError_(f"unknown statement {s}")

    def cond(self, e):
        t = self.expr(e)
        if not (is_scalar(t) or t.kind == "ptr"):
            raise TypeError_(f"in {self.f.name}: a condition must be a number or a pointer, not {t}")

    # --- expressions ---------------------------------------------------------
    def expr(self, e) -> Type:
        t = self._expr(e)
        e.ty = t
        return t

    def _expr(self, e) -> Type:
        if isinstance(e, P.Num):
            return INT
        if isinstance(e, P.CharLit):
            return INT
        if isinstance(e, P.Str):
            raise TypeError_("string literals are not supported yet")
        if isinstance(e, P.Null):
            return ANYPTR
        if isinstance(e, P.SizeOf):
            e.size = self.info.size(e.type)
            return INT
        if isinstance(e, P.Name):
            kind, u, t = self.lookup(e.id)
            if kind == "func":
                raise TypeError_(f"in {self.f.name}: {e.id} is a function")
            e.kind, e.unique = kind, u
            e.lv = True
            return t
        if isinstance(e, P.Unary):
            if e.op == "&":
                t = self.expr(e.e)
                if not getattr(e.e, "lv", False):
                    raise TypeError_(f"in {self.f.name}: & needs something with an address")
                root = e.e
                while isinstance(root, (P.Index, P.Field)) and getattr(root, "in_place", False):
                    root = root.a if isinstance(root, P.Index) else root.e
                if isinstance(root, P.Name) and root.kind == "local":
                    self.taken.add(root.unique)
                return Type("ptr", t)
            if e.op == "*":
                t = self.expr(e.e)
                if t.kind != "ptr" or t.of is None:
                    raise TypeError_(f"in {self.f.name}: * needs a typed pointer, not {t}")
                e.lv = True
                return t.of
            t = self.expr(e.e)
            if e.op == "-" and is_scalar(t):
                return INT
            if e.op == "!" and (is_scalar(t) or t.kind == "ptr"):
                return INT
            raise TypeError_(f"in {self.f.name}: bad operand {t} for {e.op}")
        if isinstance(e, P.Binary):
            if e.op in ("&&", "||"):
                self.cond(e.l)
                self.cond(e.r)
                return INT
            a, b = self.expr(e.l), self.expr(e.r)
            if e.op in ("==", "!=", "<", "<=", ">", ">="):
                if (is_scalar(a) and is_scalar(b)) or (a.kind == "ptr" and b.kind == "ptr" and same(a, b)):
                    e.unsigned = a.kind == "ptr"
                    return INT
                raise TypeError_(f"in {self.f.name}: cannot compare {a} with {b}")
            if is_scalar(a) and is_scalar(b):
                return INT
            if e.op in ("+", "-") and a.kind == "ptr" and a.of is not None and is_scalar(b):
                e.scale = self.info.size(a.of)
                return a
            raise TypeError_(f"in {self.f.name}: bad operands {a} {e.op} {b}")
        if isinstance(e, P.Call):
            if not isinstance(e.f, P.Name):
                raise TypeError_("only named functions can be called")
            sig = self.info.funcs.get(e.f.id)
            if sig is None:
                raise TypeError_(f"in {self.f.name}: no function {e.f.id}")
            if len(e.args) != len(sig.params):
                k = len(sig.params)
                raise TypeError_(f"in {self.f.name}: {e.f.id} takes {k} argument{'' if k == 1 else 's'}, "
                                 f"not {len(e.args)}")
            for a, (_, pt) in zip(e.args, sig.params):
                at = self.expr(a)
                if not assignable(pt, at):
                    raise TypeError_(f"in {self.f.name}: argument {at} for parameter {pt} of {e.f.id}")
            e.sig = sig
            return sig.ret if sig.ret is not None else Type("void")
        if isinstance(e, P.Index):
            a = self.expr(e.a)
            i = self.expr(e.i)
            if not is_scalar(i):
                raise TypeError_(f"in {self.f.name}: an index must be a number")
            if a.kind == "array":
                e.in_place = True           # the element lives inside the array's storage
                e.lv = True
                e.scale = self.info.size(a.of)
                return a.of
            if a.kind == "ptr" and a.of is not None:
                e.in_place = False
                e.lv = True
                e.scale = self.info.size(a.of)
                return a.of
            raise TypeError_(f"in {self.f.name}: cannot index {a}")
        if isinstance(e, P.Field):
            t = self.expr(e.e)
            st, via = None, None
            if t.kind == "struct":
                st, via = t, "value"
            elif t.kind == "ptr" and t.of is not None and t.of.kind == "struct":
                st, via = t.of, "pointer"
            if st is None:
                raise TypeError_(f"in {self.f.name}: {t} has no fields")
            si = self.info.structs[st.name]
            if e.name not in si.fields:
                raise TypeError_(f"in {self.f.name}: {st.name} has no field {e.name}")
            e.offset, ft = si.fields[e.name]
            e.via = via
            e.in_place = via == "value"
            e.lv = True
            return ft
        raise TypeError_(f"unknown expression {e}")
