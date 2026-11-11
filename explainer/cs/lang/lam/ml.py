"""A small ML ("λ-core") with Hindley–Milner type inference, for Parts 14 and 15.

    prog = parse(JOB_ML)
    types = infer_program(prog)        # the principal type of every top-level definition
    value = evaluate(prog, env={"text": codes})

Syntax, OCaml-flavoured: ``let x = e in e``, ``let rec f x y = e in e``, ``fun x y -> e``, ``if e then e else
e``, ``match e with [] -> e | h :: t -> e``, pairs ``(a, b)`` with ``fst``/``snd``, lists ``[]``, ``[a; b]`` and
``h :: t``, integers, booleans and operators ``+ - * / mod = <> < <= > >= && ||``.  A program is a sequence of
``let``/``let rec`` definitions, then ``;;`` and an expression.

Inference is Algorithm W in the efficient form (destructive unification on type variables with levels, Rémy
1992); :func:`infer` can record a trace of every unification and binding for the scenes.  ``=`` is polymorphic
structural equality, as in ML.
"""
from __future__ import annotations

import itertools
import re
import sys

# -- syntax ----------------------------------------------------------------------------------------------------
TOKEN = re.compile(r'\s*(?:(\d+)|("(?:[^"\\]|\\.)*")|(;;|->|::|<>|<=|>=|&&|\|\||[-+*/=<>()\[\];,|_])|([A-Za-z_][A-Za-z0-9_\']*))')
KEYWORDS = {"let", "rec", "in", "fun", "if", "then", "else", "match", "with", "true", "false", "mod", "and"}


def lex(src: str):
    src = re.sub(r"\(\*.*?\*\)", " ", src, flags=re.S)
    out, pos = [], 0
    while True:
        m = TOKEN.match(src, pos)
        if not m or m.end() == pos:
            if src[pos:].strip():
                raise SyntaxError(f"bad character near {src[pos:pos + 20]!r}")
            break
        pos = m.end()
        n, s, op, name = m.groups()
        if n:
            out.append(("int", int(n)))
        elif s:
            out.append(("str", bytes(s[1:-1], "utf-8").decode("unicode_escape")))
        elif op:
            out.append(("op", op))
        elif name in KEYWORDS:
            out.append(("kw", name))
        else:
            out.append(("id", name))
    out.append(("eof", None))
    return out


class Parser:
    def __init__(self, src):
        self.t = lex(src)
        self.i = 0

    def peek(self, k=0):
        return self.t[self.i + k]

    def take(self, kind=None, val=None):
        tok = self.t[self.i]
        if (kind and tok[0] != kind) or (val is not None and tok[1] != val):
            raise SyntaxError(f"expected {val or kind}, got {tok}")
        self.i += 1
        return tok

    def at(self, kind, val=None):
        tok = self.t[self.i]
        return tok[0] == kind and (val is None or tok[1] == val)

    def program(self):
        defs = []
        while self.at("kw", "let"):
            save = self.i
            d = self.binding()
            if self.at("kw", "in"):
                self.i = save
                break
            defs.append(d)
            if self.at("op", ";;"):
                self.take()
        body = self.expr() if not self.at("eof") else ("var", defs[-1][1]) if defs else ("int", 0)
        self.take("eof")
        return {"defs": defs, "body": body}

    def binding(self):
        self.take("kw", "let")
        rec = False
        if self.at("kw", "rec"):
            self.take()
            rec = True
        name = self.take("id")[1]
        params = []
        while self.at("id") or self.at("op", "("):
            if self.at("op", "("):
                self.take()
                self.take("op", ")")
                params.append("_unit")
            else:
                params.append(self.take("id")[1])
        self.take("op", "=")
        e = self.expr()
        for p in reversed(params):
            e = ("fun", p, e)
        return ("rec" if rec else "let", name, e)

    def expr(self):
        if self.at("kw", "let"):
            kind, name, e = self.binding()
            self.take("kw", "in")
            body = self.expr()
            return (kind, name, e, body)
        if self.at("kw", "fun"):
            self.take()
            params = []
            while self.at("id"):
                params.append(self.take("id")[1])
            self.take("op", "->")
            e = self.expr()
            for p in reversed(params):
                e = ("fun", p, e)
            return e
        if self.at("kw", "if"):
            self.take()
            c = self.expr()
            self.take("kw", "then")
            a = self.expr()
            self.take("kw", "else")
            b = self.expr()
            return ("if", c, a, b)
        if self.at("kw", "match"):
            self.take()
            e = self.expr()
            self.take("kw", "with")
            if self.at("op", "|"):
                self.take()
            self.take("op", "[")
            self.take("op", "]")
            self.take("op", "->")
            nil = self.expr_nomatch()
            self.take("op", "|")
            h = self.take("id")[1] if self.at("id") else (self.take("op", "_") and "_")
            self.take("op", "::")
            tl = self.take("id")[1] if self.at("id") else (self.take("op", "_") and "_")
            self.take("op", "->")
            cons = self.expr()
            return ("match", e, nil, h, tl, cons)
        return self.binop(0)

    def expr_nomatch(self):
        # the [] branch of a match ends at the next |
        return self.binop(0)

    LEVELS = [("||",), ("&&",), ("=", "<>", "<", "<=", ">", ">="), ("::",), ("+", "-"), ("*", "/", "mod")]

    def binop(self, lvl):
        if lvl == len(self.LEVELS):
            return self.app()
        ops = self.LEVELS[lvl]
        left = self.binop(lvl + 1)
        while (self.peek()[0] == "op" and self.peek()[1] in ops) or (self.peek() == ("kw", "mod") and "mod" in ops):
            op = self.take()[1]
            if op == "::":
                right = self.binop(lvl)          # right associative
                return ("cons", left, right)
            right = self.binop(lvl + 1)
            left = ("op", op, left, right)
        return left

    def app(self):
        f = self.atom()
        while self.starts_atom():
            f = ("app", f, self.atom())
        return f

    def starts_atom(self):
        k, v = self.peek()
        return k in ("int", "str", "id") or (k == "kw" and v in ("true", "false")) or (k == "op" and v in ("(", "["))

    def atom(self):
        k, v = self.take()
        if k == "int":
            return ("int", v)
        if k == "str":
            e = ("nil",)
            for c in reversed(v.encode()):
                e = ("cons", ("int", c), e)
            return e
        if k == "id":
            return ("var", v)
        if k == "kw" and v in ("true", "false"):
            return ("bool", v == "true")
        if v == "(":
            if self.at("op", ")"):
                self.take()
                return ("unit",)
            e = self.expr()
            if self.at("op", ","):
                self.take()
                e2 = self.expr()
                self.take("op", ")")
                return ("pair", e, e2)
            self.take("op", ")")
            return e
        if v == "[":
            items = []
            while not self.at("op", "]"):
                items.append(self.expr())
                if self.at("op", ";"):
                    self.take()
            self.take("op", "]")
            e = ("nil",)
            for it in reversed(items):
                e = ("cons", it, e)
            return e
        if v == "-":
            return ("op", "-", ("int", 0), self.atom())
        raise SyntaxError(f"unexpected {k} {v}")


def parse(src: str):
    return Parser(src).program()


def parse_expr(src: str):
    p = Parser(src)
    e = p.expr()
    p.take("eof")
    return e


# -- types -----------------------------------------------------------------------------------------------------
class TVar:
    _ids = itertools.count()

    def __init__(self, level):
        self.id = next(TVar._ids)
        self.level = level
        self.link = None          # bound to a type once unified

    def __repr__(self):
        return f"'t{self.id}"


class TGen:
    """A quantified variable in a type scheme."""
    def __init__(self, k):
        self.k = k


def T(name, *args):
    return ("con", name, tuple(args))


INT, BOOL, UNIT = T("int"), T("bool"), T("unit")


def fn(a, b):
    return T("->", a, b)


def prune(t):
    while isinstance(t, TVar) and t.link is not None:
        t = t.link
    return t


class TypeErr(Exception):
    pass


def show_type(t, names=None) -> str:
    names = {} if names is None else names

    def nm(v):
        if v not in names:
            k = len(names)
            names[v] = "'" + (chr(97 + k) if k < 26 else f"t{k}")
        return names[v]

    def go(t, prec=0):
        t = prune(t)
        if isinstance(t, TVar):
            return nm(t.id)
        if isinstance(t, TGen):
            return nm(("g", t.k))
        _, name, args = t
        if name == "->":
            s = f"{go(args[0], 2)} -> {go(args[1], 1)}"
            return f"({s})" if prec >= 2 else s
        if name == "*":
            s = f"{go(args[0], 3)} * {go(args[1], 3)}"
            return f"({s})" if prec >= 3 else s
        if name == "list":
            return f"{go(args[0], 4)} list"
        return name
    return go(t)


def type_size(t, memo=None) -> int:
    """Number of leaves of the type written out as a tree (shared subterms counted every time they occur)."""
    memo = {} if memo is None else memo
    t = prune(t)
    if isinstance(t, (TVar, TGen)):
        return 1
    if id(t) in memo:
        return memo[id(t)]
    s = sum(type_size(a, memo) for a in t[2]) if t[2] else 1
    memo[id(t)] = s
    return s


class Infer:
    def __init__(self, trace=False):
        self.trace = [] if trace else None
        self.unify_calls = 0
        self.names = {}

    def log(self, kind, *items):
        if self.trace is not None:
            self.trace.append((kind,) + tuple(show_type(x, self.names) if not isinstance(x, str) else x
                                              for x in items))

    def occurs(self, v, t, seen=None):
        seen = set() if seen is None else seen
        t = prune(t)
        if t is v:
            return True
        if isinstance(t, TVar):
            if t.level > v.level:
                t.level = v.level              # keep levels sound for generalization
            return False
        if isinstance(t, tuple):
            if id(t) in seen:
                return False
            seen.add(id(t))
            return any(self.occurs(v, a, seen) for a in t[2])
        return False

    def unify(self, a, b):
        self.unify_calls += 1
        a, b = prune(a), prune(b)
        if a is b:
            return
        if isinstance(a, TVar):
            if self.occurs(a, b):
                raise TypeErr(f"infinite type: {show_type(a)} = {show_type(b)}")
            self.log("bind", a, b)
            a.link = b
            return
        if isinstance(b, TVar):
            return self.unify(b, a)
        if a[1] != b[1] or len(a[2]) != len(b[2]):
            raise TypeErr(f"cannot match {show_type(a)} with {show_type(b)}")
        self.log("unify", a, b)
        for x, y in zip(a[2], b[2]):
            self.unify(x, y)

    def generalize(self, t, level):
        mapping, memo = {}, {}

        def go(t):
            t = prune(t)
            if isinstance(t, TVar):
                if t.level > level:
                    if t not in mapping:
                        mapping[t] = TGen(len(mapping))
                    return mapping[t]
                return t
            if isinstance(t, tuple):
                if id(t) not in memo:            # keep shared subterms shared: types can be exponentially big
                    memo[id(t)] = (("con", t[1], tuple(go(a) for a in t[2])), t)
                return memo[id(t)][0]
            return t
        return ("scheme", go(t), len(mapping))

    def instantiate(self, sch, level):
        if not (isinstance(sch, tuple) and sch[0] == "scheme"):
            return sch
        fresh = [TVar(level) for _ in range(sch[2])]
        memo = {}

        def go(t):
            if isinstance(t, TGen):
                return fresh[t.k]
            if isinstance(t, tuple):
                if id(t) not in memo:
                    memo[id(t)] = (("con", t[1], tuple(go(a) for a in t[2])), t)
                return memo[id(t)][0]
            return t
        return go(sch[1])

    def infer(self, e, env, level):
        k = e[0]
        if k == "int":
            return INT
        if k == "bool":
            return BOOL
        if k == "unit":
            return UNIT
        if k == "var":
            if e[1] not in env:
                raise TypeErr(f"unbound variable {e[1]}")
            return self.instantiate(env[e[1]], level)
        if k == "fun":
            a = TVar(level)
            self.log("assume", e[1], a)
            b = self.infer(e[2], {**env, e[1]: a}, level)
            return fn(a, b)
        if k == "app":
            f = self.infer(e[1], env, level)
            a = self.infer(e[2], env, level)
            r = TVar(level)
            self.unify(f, fn(a, r))
            return r
        if k == "let":
            t = self.infer(e[2], env, level + 1)
            sch = self.generalize(t, level)
            self.log("generalize", e[1], self.instantiate(sch, level))
            return self.infer(e[3], {**env, e[1]: sch}, level)
        if k == "rec":
            v = TVar(level + 1)
            t = self.infer(e[2], {**env, e[1]: v}, level + 1)
            self.unify(v, t)
            sch = self.generalize(t, level)
            return self.infer(e[3], {**env, e[1]: sch}, level)
        if k == "if":
            self.unify(self.infer(e[1], env, level), BOOL)
            a = self.infer(e[2], env, level)
            self.unify(a, self.infer(e[3], env, level))
            return a
        if k == "pair":
            return T("*", self.infer(e[1], env, level), self.infer(e[2], env, level))
        if k == "nil":
            return T("list", TVar(level))
        if k == "cons":
            h = self.infer(e[1], env, level)
            t = self.infer(e[2], env, level)
            self.unify(t, T("list", h))
            return t
        if k == "match":
            s = self.infer(e[1], env, level)
            a = TVar(level)
            self.unify(s, T("list", a))
            r = self.infer(e[2], env, level)
            env2 = {**env, e[3]: a, e[4]: s}
            self.unify(r, self.infer(e[5], env2, level))
            return r
        if k == "op":
            op = e[1]
            x, y = self.infer(e[2], env, level), self.infer(e[3], env, level)
            if op in ("+", "-", "*", "/", "mod"):
                self.unify(x, INT)
                self.unify(y, INT)
                return INT
            if op in ("<", "<=", ">", ">="):
                self.unify(x, INT)
                self.unify(y, INT)
                return BOOL
            if op in ("=", "<>"):
                self.unify(x, y)
                return BOOL
            if op in ("&&", "||"):
                self.unify(x, BOOL)
                self.unify(y, BOOL)
                return BOOL
        raise TypeErr(f"cannot type {k}")


def builtins_env():
    a, b = TGen(0), TGen(1)
    return {
        "fst": ("scheme", fn(T("*", a, b), a), 2),
        "snd": ("scheme", fn(T("*", a, b), b), 2),
        "not": fn(BOOL, BOOL),
    }


def infer_expr(e, env=None, trace=False):
    I = Infer(trace)
    env = {**builtins_env(), **(env or {})}
    t = I.infer(e, env, 1)
    return t, I


def infer_program(prog, env=None, trace=False):
    """Principal types of every top-level definition, in order, as strings; and the body's type."""
    I = Infer(trace)
    env = {**builtins_env(), **(env or {})}
    out = []
    for kind, name, e in prog["defs"]:
        if kind == "rec":
            v = TVar(2)
            t = I.infer(e, {**env, name: v}, 2)
            I.unify(v, t)
        else:
            t = I.infer(e, env, 2)
        sch = I.generalize(t, 1)
        env[name] = sch
        out.append((name, show_type(I.instantiate(sch, 1))))
    body = I.infer(prog["body"], env, 2)
    return out, show_type(body), I


# -- evaluation ------------------------------------------------------------------------------------------------
class Closure:
    __slots__ = ("param", "body", "env")

    def __init__(self, param, body, env):
        self.param, self.body, self.env = param, body, env


NIL = None


def to_list(v):
    out = []
    while v is not None:
        out.append(v[0])
        v = v[1]
    return out


def from_list(xs):
    v = None
    for x in reversed(xs):
        v = (x, v)
    return v


def evaluate(prog, env=None, stats=None):
    """Call-by-value evaluation with environments; lists are cons cells (head, tail) and None.  ``stats`` counts
    applications and allocations (cons cells, pairs, closures)."""
    st = stats if stats is not None else {}
    st.setdefault("apps", 0)
    st.setdefault("alloc", 0)
    E = {"fst": lambda p: p[0], "snd": lambda p: p[1], "not": lambda b: not b, **(env or {})}
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 200000))

    def ev(e, env):
        k = e[0]
        if k == "int" or k == "bool":
            return e[1]
        if k == "unit":
            return ()
        if k == "var":
            v = env[e[1]]
            return v[0] if isinstance(v, list) else v
        if k == "fun":
            st["alloc"] += 1
            return Closure(e[1], e[2], env)
        if k == "app":
            f = ev(e[1], env)
            a = ev(e[2], env)
            st["apps"] += 1
            if callable(f):
                return f(a)
            return ev(f.body, {**f.env, f.param: a})
        if k == "let":
            return ev(e[3], {**env, e[1]: ev(e[2], env)})
        if k == "rec":
            cell = [None]
            env2 = {**env, e[1]: cell}
            cell[0] = ev(e[2], env2)
            return ev(e[3], env2)
        if k == "if":
            return ev(e[2], env) if ev(e[1], env) else ev(e[3], env)
        if k == "pair":
            st["alloc"] += 1
            return (ev(e[1], env), ev(e[2], env))
        if k == "nil":
            return None
        if k == "cons":
            st["alloc"] += 1
            return (ev(e[1], env), ev(e[2], env))
        if k == "match":
            v = ev(e[1], env)
            if v is None:
                return ev(e[2], env)
            return ev(e[5], {**env, e[3]: v[0], e[4]: v[1]})
        if k == "op":
            op = e[1]
            if op == "&&":
                return ev(e[2], env) and ev(e[3], env)
            if op == "||":
                return ev(e[2], env) or ev(e[3], env)
            x, y = ev(e[2], env), ev(e[3], env)
            if op == "+":
                return x + y
            if op == "-":
                return x - y
            if op == "*":
                return x * y
            if op == "/":
                return int(x / y)
            if op == "mod":
                return x - y * int(x / y)
            if op == "=":
                return x == y
            if op == "<>":
                return x != y
            if op == "<":
                return x < y
            if op == "<=":
                return x <= y
            if op == ">":
                return x > y
            if op == ">=":
                return x >= y
        raise ValueError(k)

    env_ = dict(E)
    for kind, name, e in prog["defs"]:
        if kind == "rec":
            cell = [None]
            env_[name] = cell
            cell[0] = ev(e, env_)
        else:
            env_[name] = ev(e, env_)
    return ev(prog["body"], env_)


# -- the Job, in the λ-core ------------------------------------------------------------------------------------
JOB_ML = r"""
(* The Job in the λ-core: count the words of a text (a list of character codes), print the twenty most frequent.
   Not one type is written down; inference finds them all. *)

let rec rev_onto l acc = match l with [] -> acc | h :: t -> rev_onto t (h :: acc)
let rev l = rev_onto l []

let lower c = if c >= 65 && c <= 90 then c + 32 else c
let is_letter c = c >= 97 && c <= 122

(* split into words, each a list of codes, in order *)
let rec words cs cur acc =
  match cs with
    [] -> rev (match cur with [] -> acc | h :: t -> rev cur :: acc)
  | c :: rest ->
      let c = lower c in
      if is_letter c then words rest (c :: cur) acc
      else (match cur with [] -> words rest [] acc | h :: t -> words rest [] (rev cur :: acc))

(* add one to w's count, or append (w, 1): the table stays in order of first use *)
let rec bump w table =
  match table with
    [] -> [(w, 1)]
  | p :: rest -> if fst p = w then (w, snd p + 1) :: rest else p :: bump w rest

let rec count ws table = match ws with [] -> table | w :: rest -> count rest (bump w table)

(* a stable insertion sort, most frequent first; ties keep their order of first use *)
let rec insert x l =
  match l with [] -> [x] | y :: ys -> if snd x >= snd y then x :: l else y :: insert x ys
let rec sort l = match l with [] -> [] | h :: t -> insert h (sort t)

let rec take n l = if n = 0 then [] else (match l with [] -> [] | h :: t -> h :: take (n - 1) t)

let job text = take 20 (sort (count (words text [] []) []))
"""


def job_output(result) -> bytes:
    """Format the Job's result (a list of (word, count) pairs) exactly as the other Jobs print it."""
    out = bytearray()
    for w, n in to_list(result):
        out += bytes(to_list(w)) + b" " + str(n).encode() + b"\n"
    return bytes(out)


def exp_let(n: int) -> str:
    """The classic doubly exponential example: each f_k applies f_{k-1} twice to a pair-building function."""
    lines = ["let f0 = fun x -> (x, x) in"]
    for k in range(1, n + 1):
        lines.append(f"let f{k} = fun y -> f{k - 1} (f{k - 1} y) in")
    lines.append(f"f{n}")
    return "\n".join(lines)
