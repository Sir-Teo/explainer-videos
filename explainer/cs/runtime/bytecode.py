"""The λ-core compiled to a stack bytecode (Part 15, chapters 2–4).

    prog = ml.parse(src)
    code = compile_program(prog)       # functions, globals, and the main code
    code.listing("bump")               # a human-readable disassembly of one function
    tape = code.encode()               # the bytes the Pebble VM's loader reads before the text

Values are 32-bit words with a one-bit tag: an integer ``n`` is ``2n + 1``; a pointer to the heap object at word
address ``a`` is ``2a``; ``0`` is the empty list (address 0 is never used).  ``false`` and ``()`` are the integer 0,
``true`` is 1.  Return addresses and saved frame pointers are stored on the stack as tagged integers, so the
collector can scan the whole stack without knowing where the frames are.

Functions are **closure-converted**: a ``fun`` becomes a code block plus the list of its free variables, and a
closure is a heap object holding the code's index and copies of those values (flat closures).  A chain
``fun x -> fun y -> e`` becomes one function of arity 2, and a call whose callee is known (a ``let``-bound
function) passes all its arguments at once; other calls pass one argument at a time and the VM builds partial
applications when a closure wants more (the *eval/apply* model, Marlow and Peyton Jones 2004).  A call in tail
position reuses the caller's frame (``TAILCALL``), so ``words`` and ``count`` run in constant stack.

Frame layout, from the frame pointer ``bp`` up::

    bp-1      the closure being run
    bp+0..    arguments, then the other locals (``nlocals`` slots in all)
    bp+nl     the caller's bp, tagged
    bp+nl+1   the return pc, tagged
    ...       the operand stack
"""
from __future__ import annotations

import struct
from dataclasses import dataclass, field

OPS = ["HALT", "CONST", "LOCAL", "SETLOCAL", "FREE", "GLOBAL", "SETGLOBAL", "POP", "JMP", "JF", "ADD", "SUB", "MUL",
       "DIV", "MOD", "EQ", "NE", "LT", "LE", "GT", "GE", "NOT", "CONS", "PAIR", "FST", "SND", "JNIL", "HEAD", "TAIL",
       "CLOSURE", "CALL", "TAILCALL", "RET", "GETC", "PUTC", "SELF"]
OP = {name: k for k, name in enumerate(OPS)}

# heap object kinds (the low four bits of a header; the field count is the rest)
CONS, PAIR, CLOS, PAP, FWD = 1, 2, 3, 4, 15
KIND_NAME = {CONS: "cons", PAIR: "pair", CLOS: "closure", PAP: "partial application"}

NIL, FALSE, TRUE, UNIT = 0, 1, 3, 1


def tag(n: int) -> int:
    return 2 * n + 1


def untag(v: int) -> int:
    return v >> 1


BINOP = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV", "mod": "MOD", "=": "EQ", "<>": "NE", "<": "LT", "<=": "LE",
         ">": "GT", ">=": "GE"}
PRIMS = {"fst": "FST", "snd": "SND", "not": "NOT", "getc": "GETC", "putc": "PUTC"}


@dataclass
class Fn:
    name: str
    arity: int
    params: list
    body: tuple
    free: list = field(default_factory=list)       # names captured, in closure order
    code: list = field(default_factory=list)       # (op, arg) with labels unresolved
    nlocals: int = 0
    entry: int = 0
    self_name: str | None = None


def free_vars(e, bound=frozenset()) -> list:
    """Free variables of e in order of first occurrence."""
    out: list = []

    def go(e, b):
        k = e[0]
        if k == "var":
            if e[1] not in b and e[1] not in out:
                out.append(e[1])
        elif k == "fun":
            go(e[2], b | {e[1]})
        elif k == "app":
            go(e[1], b)
            go(e[2], b)
        elif k == "let":
            go(e[2], b)
            go(e[3], b | {e[1]})
        elif k == "rec":
            go(e[2], b | {e[1]})
            go(e[3], b | {e[1]})
        elif k == "if":
            for x in e[1:]:
                go(x, b)
        elif k in ("pair", "cons"):
            go(e[1], b)
            go(e[2], b)
        elif k == "match":
            go(e[1], b)
            go(e[2], b)
            go(e[5], b | {e[3], e[4]})
        elif k == "op":
            go(e[2], b)
            go(e[3], b)
    go(e, set(bound))
    return out


def uncurry(e):
    params = []
    while e[0] == "fun":
        params.append(e[1])
        e = e[2]
    return params, e


def spine(e):
    args = []
    while e[0] == "app":
        args.append(e[2])
        e = e[1]
    return e, list(reversed(args))


class CompileError(ValueError):
    pass


@dataclass
class Program:
    fns: list
    globals: list            # names
    main: Fn
    code: list               # (op, arg), resolved, main first
    names: dict = field(default_factory=dict)   # pc -> function name, for listings

    def fn(self, name):
        return next(f for f in self.fns if f.name == name)

    def listing(self, name: str) -> list[str]:
        f = self.main if name == "main" else self.fn(name)
        end = min([g.entry for g in self.fns + [self.main] if g.entry > f.entry] + [len(self.code)])
        out = []
        for pc in range(f.entry, end):
            op, arg = self.code[pc]
            out.append(f"{pc:5d}  {OPS[op]:<9}{self._arg(op, arg)}")
        return out

    def _arg(self, op, arg):
        name = OPS[op]
        if name == "CONST":
            return "[]" if arg == 0 else str(untag(arg))
        if name in ("LOCAL", "SETLOCAL", "FREE", "JMP", "JF", "JNIL", "CALL", "RET"):
            return str(arg)
        if name in ("GLOBAL", "SETGLOBAL"):
            return self.globals[arg]
        if name == "CLOSURE":
            return f"{self.fns[arg & 0xFFFF].name}, {arg >> 16} free"
        if name == "TAILCALL":
            return f"{arg & 0xFF}"
        return ""

    def encode(self) -> bytes:
        """The program as the Pebble VM's loader reads it: counts, the function table, then 5-byte instructions."""
        out = bytearray(struct.pack("<iiii", len(self.code), len(self.fns), len(self.globals), self.main.nlocals))
        for f in self.fns:
            out += struct.pack("<iii", f.entry, f.arity, f.nlocals)
        for op, arg in self.code:
            out += bytes([op]) + struct.pack("<i", arg)
        return bytes(out)


def compile_program(prog) -> Program:
    fns: list[Fn] = []
    gnames = [name for _, name, _ in prog["defs"]]
    gindex = {n: k for k, n in enumerate(gnames)}
    garity = {}
    for kind, name, e in prog["defs"]:
        ps, _ = uncurry(e)
        if ps:
            garity[name] = len(ps)

    counter = iter(range(1, 10 ** 9))

    def compile_fn(f: Fn, tail_body: bool = True):
        scope = {p: ("local", k) for k, p in enumerate(f.params)}
        for k, v in enumerate(f.free):
            scope[v] = ("free", k)
        if f.self_name:
            scope[f.self_name] = ("self",)
        ar = dict(getattr(f, "_arity", {}))
        st = {"depth": len(f.params), "max": len(f.params)}
        code = f.code

        def label():
            return ("L", next(counter))

        def emit(op, arg=0):
            code.append((op, arg))

        def place(lab):
            code.append(("label", lab))

        def new_local():
            k = st["depth"]
            st["depth"] += 1
            st["max"] = max(st["max"], st["depth"])
            return k

        def load(name, scope):
            where = scope.get(name)
            if where is None:
                if name in gindex:
                    emit("GLOBAL", gindex[name])
                    return
                raise CompileError(f"unbound variable {name} in {f.name}")
            if where[0] == "local":
                emit("LOCAL", where[1])
            elif where[0] == "free":
                emit("FREE", where[1])
            else:
                emit("SELF")

        def arity_of(name, scope, ar):
            if name in scope:
                return ar.get(name)
            return garity.get(name)

        def closure(e, scope, ar, self_name=None, name="λ"):
            ps, body = uncurry(e)
            bound = set(ps) | ({self_name} if self_name else set())
            fv = [v for v in free_vars(body, bound) if v in scope or v not in gindex]
            fv = [v for v in fv if v not in PRIMS or v in scope]
            g = Fn(name=name, arity=len(ps), params=ps, body=body, free=fv, self_name=self_name)
            g._arity = {self_name: len(ps)} if self_name else {}
            for v in fv:
                if v in ar:
                    g._arity[v] = ar[v]
            fns.append(g)
            idx = len(fns) - 1
            for v in fv:
                load(v, scope)
            emit("CLOSURE", idx | (len(fv) << 16))
            compile_fn(g)

        def ex(e, scope, ar, tail):
            k = e[0]
            if k == "int":
                emit("CONST", tag(e[1]))
            elif k == "bool":
                emit("CONST", TRUE if e[1] else FALSE)
            elif k == "unit":
                emit("CONST", UNIT)
            elif k == "nil":
                emit("CONST", NIL)
            elif k == "var":
                if e[1] in PRIMS and e[1] not in scope and e[1] not in gindex:
                    raise CompileError(f"primitive {e[1]} used as a value")
                load(e[1], scope)
            elif k == "fun":
                closure(e, scope, ar, name=f"{f.name}.λ")
            elif k == "app":
                head, args = spine(e)
                if head[0] == "var" and head[1] in PRIMS and head[1] not in scope and head[1] not in gindex:
                    p = PRIMS[head[1]]
                    if p == "GETC":
                        emit("GETC")
                    else:
                        ex(args[0], scope, ar, False)
                        emit(p)
                    rest = args[1:]
                    if rest:
                        raise CompileError("primitive applied to too many arguments")
                    if tail:
                        emit("RET", -1)
                    return
                n = arity_of(head[1], scope, ar) if head[0] == "var" else None
                ex(head, scope, ar, False)
                groups = []
                if n and n <= len(args):
                    groups.append(args[:n])
                    groups += [[a] for a in args[n:]]
                else:
                    groups = [[a] for a in args]
                for gi, grp in enumerate(groups):
                    for a in grp:
                        ex(a, scope, ar, False)
                    if tail and gi == len(groups) - 1:
                        emit("TAILCALL", len(grp))
                        emit("RET", -1)        # reached only when the VM runs without tail calls
                    else:
                        emit("CALL", len(grp))
                return
            elif k == "let":
                ex(e[2], scope, ar, False)
                slot = new_local()
                emit("SETLOCAL", slot)
                ar2 = dict(ar)
                ps, _ = uncurry(e[2])
                if ps:
                    ar2[e[1]] = len(ps)
                else:
                    ar2.pop(e[1], None)
                ex(e[3], {**scope, e[1]: ("local", slot)}, ar2, tail)
                st["depth"] = slot
                return
            elif k == "rec":
                if e[2][0] != "fun":
                    raise CompileError("let rec must bind a function")
                closure(e[2], scope, ar, self_name=e[1], name=e[1])
                slot = new_local()
                emit("SETLOCAL", slot)
                ps, _ = uncurry(e[2])
                ex(e[3], {**scope, e[1]: ("local", slot)}, {**ar, e[1]: len(ps)}, tail)
                st["depth"] = slot
                return
            elif k == "if":
                lf, le = label(), label()
                ex(e[1], scope, ar, False)
                emit("JF", lf)
                ex(e[2], scope, ar, tail)
                if not tail:
                    emit("JMP", le)
                place(lf)
                ex(e[3], scope, ar, tail)
                place(le)
                return
            elif k == "pair":
                ex(e[1], scope, ar, False)
                ex(e[2], scope, ar, False)
                emit("PAIR")
            elif k == "cons":
                ex(e[1], scope, ar, False)
                ex(e[2], scope, ar, False)
                emit("CONS")
            elif k == "match":
                ln, le = label(), label()
                ex(e[1], scope, ar, False)
                s = new_local()
                emit("SETLOCAL", s)
                emit("LOCAL", s)
                emit("JNIL", ln)
                h, t = new_local(), new_local()
                emit("LOCAL", s)
                emit("HEAD")
                emit("SETLOCAL", h)
                emit("LOCAL", s)
                emit("TAIL")
                emit("SETLOCAL", t)
                ar2 = {x: y for x, y in ar.items() if x not in (e[3], e[4])}
                ex(e[5], {**scope, e[3]: ("local", h), e[4]: ("local", t)}, ar2, tail)
                if not tail:
                    emit("JMP", le)
                st["depth"] = s + 1
                place(ln)
                ex(e[2], scope, ar, tail)
                place(le)
                st["depth"] = s
                return
            elif k == "op":
                op = e[1]
                if op in ("&&", "||"):
                    lshort, le = label(), label()
                    ex(e[2], scope, ar, False)
                    if op == "&&":
                        emit("JF", lshort)
                        ex(e[3], scope, ar, False)
                        emit("JMP", le)
                        place(lshort)
                        emit("CONST", FALSE)
                    else:
                        lfalse = label()
                        emit("JF", lfalse)
                        emit("CONST", TRUE)
                        emit("JMP", le)
                        place(lfalse)
                        ex(e[3], scope, ar, False)
                    place(le)
                else:
                    ex(e[2], scope, ar, False)
                    ex(e[3], scope, ar, False)
                    emit(BINOP[op])
            else:
                raise CompileError(f"cannot compile {k}")
            if tail:
                emit("RET", -1)

        ex(f.body, scope, ar, tail_body)
        f.nlocals = st["max"]

    # main: the top-level definitions, then the body
    main = Fn(name="main", arity=0, params=[], body=None)
    def main_compile():
        code = main.code
        for kind, name, e in prog["defs"]:
            ps, body = uncurry(e)
            if ps:
                body_fn = Fn(name=name, arity=len(ps), params=ps, body=body)
                fns.append(body_fn)
                code.append(("CLOSURE", len(fns) - 1))
                code.append(("SETGLOBAL", gindex[name]))
                compile_fn(body_fn)
            else:
                g = Fn(name=f"init {name}", arity=0, params=[], body=e)
                compile_fn(g, tail_body=False)
                code.extend(g.code)
                main.nlocals = max(main.nlocals, g.nlocals)
                code.append(("SETGLOBAL", gindex[name]))
        g = Fn(name="body", arity=0, params=[], body=prog["body"])
        compile_fn(g, tail_body=False)
        code.extend(g.code)
        code.append(("HALT", 0))
        main.nlocals = max(main.nlocals, g.nlocals)
    main_compile()

    # link: main first, then every function; resolve labels (each function's labels are its own)
    flat: list = []
    names = {}

    def link(f):
        f.entry = len(flat)
        names[f.entry] = f.name
        where = {}
        pc = len(flat)
        for op, arg in f.code:
            if op == "label":
                where[arg] = pc
            else:
                pc += 1
        for op, arg in f.code:
            if op == "label":
                continue
            if op in ("JMP", "JF", "JNIL"):
                arg = where[arg]
            if op == "RET":
                arg = f.nlocals
            if op == "TAILCALL":
                arg = arg | (f.nlocals << 8)
            flat.append((OP[op], arg))
    link(main)
    for f in fns:
        link(f)
    return Program(fns=fns, globals=gnames, main=main, code=flat, names=names)


# the Job's driver: read the text with getc, run the Job, print the table
DRIVER_ML = r"""
let rec read acc = let c = getc () in if c < 0 then rev acc else read (c :: acc)
let rec print_num n = if n < 10 then putc (n + 48) else let u = print_num (n / 10) in putc (n mod 10 + 48)
let rec print_word w = match w with [] -> () | c :: t -> let u = putc c in print_word t
let rec print_all l =
  match l with
    [] -> ()
  | p :: t -> let u = print_word (fst p) in let v = putc 32 in let x = print_num (snd p) in let y = putc 10 in
              print_all t
;;
print_all (job (read []))
"""


def job_source() -> str:
    from explainer.cs.lang.lam.ml import JOB_ML
    return JOB_ML + DRIVER_ML


def job_program() -> Program:
    from explainer.cs.lang.lam import ml
    return compile_program(ml.parse(job_source()))
