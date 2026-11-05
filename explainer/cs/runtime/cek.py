"""A CEK machine for the λ-core (Felleisen and Friedman 1986): Control, Environment, Kontinuation (Part 15,
chapter 4).

The interpreter of chapter 2 keeps "what to do next" on Python's own stack.  Here it is a data structure: the
continuation is a linked list of frames (``("arg", e, env, k)`` means: then evaluate the argument e and apply).  Each
step looks only at the current control and the top frame, so the machine never recurses, and a continuation can be
captured as a value (``callcc``) and resumed later, any number of times.

    value, stats = run(ml.parse(src))      # stats: steps, the deepest continuation, captured continuations

``callcc f`` calls f with the current continuation k; applying k to v abandons the current continuation and
returns v to the point where callcc was called: an early exit, or an exception, made from nothing else.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Clo:
    param: str
    body: tuple
    env: dict


@dataclass
class Cont:
    k: tuple


@dataclass
class Prim:
    name: str
    f: object


def _depth(k):
    n = 0
    while k is not None:
        n += 1
        k = k[-1]
    return n


def run(prog, env=None, max_steps=10 ** 7):
    stats = {"steps": 0, "max_depth": 0, "captured": 0, "resumed": 0, "mults": 0}

    def binop(op, x, y):
        if op == "*":
            stats["mults"] += 1
        return {"+": lambda: x + y, "-": lambda: x - y, "*": lambda: x * y, "/": lambda: int(x / y),
                "mod": lambda: x - y * int(x / y), "=": lambda: x == y, "<>": lambda: x != y, "<": lambda: x < y,
                "<=": lambda: x <= y, ">": lambda: x > y, ">=": lambda: x >= y}[op]()

    base = {"fst": Prim("fst", lambda p: p[0]), "snd": Prim("snd", lambda p: p[1]),
            "not": Prim("not", lambda b: not b), "callcc": Prim("callcc", None), **(env or {})}
    # top-level definitions become nested lets
    e = prog["body"]
    for kind, name, d in reversed(prog["defs"]):
        e = ("rec" if kind == "rec" else "let", name, d, e)

    # machine state: (mode, x, env, k); mode "eval" (x is an expression) or "ret" (x is a value)
    mode, x, en, k = "eval", e, base, None
    depth_sample = 0
    while True:
        stats["steps"] += 1
        if stats["steps"] > max_steps:
            raise RuntimeError("too many steps")
        if stats["steps"] % 16 == 0:
            d = _depth(k)
            if d > stats["max_depth"]:
                stats["max_depth"] = d
        if mode == "eval":
            t = x[0]
            if t in ("int", "bool"):
                mode, x = "ret", x[1]
            elif t == "unit":
                mode, x = "ret", ()
            elif t == "nil":
                mode, x = "ret", None
            elif t == "var":
                v = en[x[1]]
                mode, x = "ret", (v[0] if isinstance(v, list) else v)
            elif t == "fun":
                mode, x = "ret", Clo(x[1], x[2], en)
            elif t == "app":
                k = ("arg", x[2], en, k)
                x = x[1]
            elif t == "let":
                k = ("let", x[1], x[3], en, k)
                x = x[2]
            elif t == "rec":
                cell = [None]
                en2 = {**en, x[1]: cell}
                cell[0] = Clo(x[2][1], x[2][2], en2)
                x, en = x[3], en2
            elif t == "if":
                k = ("if", x[2], x[3], en, k)
                x = x[1]
            elif t in ("pair", "cons"):
                k = ("pair1", x[2], en, k)
                x = x[1]
            elif t == "match":
                k = ("match", x, en, k)
                x = x[1]
            elif t == "op":
                if x[1] in ("&&", "||"):
                    k = ("short", x[1], x[3], en, k)
                else:
                    k = ("op1", x[1], x[3], en, k)
                x = x[2]
            else:
                raise ValueError(t)
            continue
        # mode == "ret": deliver the value x to the top frame
        if k is None:
            return x, stats
        f = k[0]
        if f == "arg":
            _, a, aen, k2 = k
            k = ("call", x, k2)
            mode, x, en = "eval", a, aen
        elif f == "call":
            _, fn, k2 = k
            k = k2
            if isinstance(fn, Clo):
                mode, x, en = "eval", fn.body, {**fn.env, fn.param: x}
            elif isinstance(fn, Cont):
                stats["resumed"] += 1
                k = fn.k                                  # abandon the current continuation
                mode = "ret"
            elif fn.name == "callcc":
                stats["captured"] += 1
                k = ("call", x, k)                        # apply x to the captured continuation
                mode, x = "ret", Cont(k[2])
            else:
                mode, x = "ret", fn.f(x)
        elif f == "let":
            _, name, body, len_, k2 = k
            mode, x, en, k = "eval", body, {**len_, name: x}, k2
        elif f == "if":
            _, a, b, ien, k2 = k
            mode, x, en, k = "eval", (a if x else b), ien, k2
        elif f == "pair1":
            _, b, pen, k2 = k
            k = ("pair2", x, k2)
            mode, x, en = "eval", b, pen
        elif f == "pair2":
            _, a, k2 = k
            mode, x, k = "ret", (a, x), k2
        elif f == "match":
            _, m, men, k2 = k
            k = k2
            if x is None:
                mode, x, en = "eval", m[2], men
            else:
                mode, x, en = "eval", m[5], {**men, m[3]: x[0], m[4]: x[1]}
        elif f == "op1":
            _, op, b, oen, k2 = k
            k = ("op2", op, x, k2)
            mode, x, en = "eval", b, oen
        elif f == "op2":
            _, op, a, k2 = k
            mode, x, k = "ret", binop(op, a, x), k2
        elif f == "short":
            _, op, b, sen, k2 = k
            if (op == "&&" and not x) or (op == "||" and x):
                mode, k = "ret", k2
            else:
                mode, x, en, k = "eval", b, sen, k2
        else:
            raise ValueError(f)


PRODUCT = r"""
let rec product l = match l with [] -> 1 | h :: t -> h * product t
let product_exit l =
  callcc (fun k ->
    let rec go l = match l with [] -> 1 | h :: t -> if h = 0 then k 0 else h * go t in
    go l)
;;
"""
