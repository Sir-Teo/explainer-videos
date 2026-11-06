"""Floyd-Hoare logic and weakest preconditions (Part 54), with every verification condition checked by bit-blasting
it to CNF and handing its negation to Part 26's SAT solver.

    parse(text)                        an expression or assertion in a small C-like syntax, as a tuple tree
    show(e, unicode=False)             print it back, with the fewest parentheses
    assign / if_ / while_ / assert_ / assume / havoc / program
                                       a tiny imperative language as Python data
    evaluate(e, env, w) / run(...)     its concrete semantics over signed w-bit integers (two's complement,
                                       wrap-around); w=None gives mathematical integers (used by absint.py)
    wp(stmts, post)                    Dijkstra's weakest precondition (loops contribute their invariant)
    vcs(prog)                          the verification conditions: pre => wp(body, post), and for every loop
                                       "established" (in the first), "preserved", "exit gives what follows", and with
                                       a variant "non-negative" and "decreases"
    BitBlaster                         Tseitin encoding of w-bit terms: ripple-carry adders, shift-add multiplier,
                                       comparators; a formula becomes one literal
    check_vc(f, w)                     f is valid iff CNF(not f) is UNSAT under cdcl; a SAT model decodes to a
                                       counterexample, which is re-checked by concrete evaluation
    verify(prog, w)                    every VC of a program with its status, variables, clauses, solve time
    listing(prog) / flow(prog)         the program line by line, and assertions flowing backward through it
    EXAMPLES / midpoint_study(w)       max, swap without a temporary, Gauss's summation loop, binary search's
                                       midpoint (Bloch 2006) and its loop with the in-bounds assertion
    gauss_scaling()                    multiplier VCs get hard fast: solve time against the word width

The language: ``x = e``; ``if c: ... else: ...``; ``while c`` with a user-given invariant and optional variant;
``assert p``; ``assume p``; ``havoc x`` (x gets an arbitrary value, used to model an unknown comparison).  Terms: +,
-, * (low w bits), unary -, ``e >> 1`` (arithmetic shift right by one: floor division by 2) and ``e >>> 1``
(logical shift), integer constants; assertions: < <= > >= == != (signed), ``!``, ``&&``, ``||``, ``==>``.

After Hoare, "An axiomatic basis for computer programming" (CACM 1969); Floyd, "Assigning meanings to programs"
(1967); Dijkstra, *A Discipline of Programming* (1976); Kroening and Strichman, *Decision Procedures* (2nd ed.,
2016), ch. 6 (bit-vectors); Bloch, "Nearly all binary searches and mergesorts are broken" (Google Research blog,
2006).
"""

from __future__ import annotations

import re
import time

from explainer.cs.algo.complexity import cdcl

# ------------------------------------------------------------------------------------------- syntax

TRUE, FALSE = ("true",), ("false",)
_CMP = {"<": "lt", "<=": "le", ">": "gt", ">=": "ge", "==": "eq", "!=": "ne"}
_CMP_TEXT = {v: k for k, v in _CMP.items()}
_UNI = {"lt": "<", "le": "≤", "gt": ">", "ge": "≥", "eq": "=", "ne": "≠",
        "and": "∧", "or": "∨", "not": "¬", "implies": "⇒"}
_ASCII = {"and": "&&", "or": "||", "not": "!", "implies": "==>", **_CMP_TEXT}
_ARITH = {"add": "+", "sub": "-", "mul": "*"}
_PREC = {"implies": 1, "or": 2, "and": 3, "not": 4, "lt": 5, "le": 5, "gt": 5, "ge": 5, "eq": 5, "ne": 5,
         "ashr": 6, "lshr": 6, "add": 7, "sub": 7, "mul": 8, "neg": 9, "var": 10, "const": 10, "true": 10,
         "false": 10}
BOOL_OPS = {"true", "false", "and", "or", "not", "implies", *_CMP.values()}
_TOKEN = re.compile(r"\s*(==>|>>>|>>|<=|>=|==|!=|&&|\|\||[-+*<>!()]|\d+|[A-Za-z_][A-Za-z_0-9']*)")


def var(name):
    return ("var", name)


def const(n):
    return ("const", n)


def tokenize(text: str) -> list[str]:
    out, pos, text = [], 0, text.strip()
    while pos < len(text):
        m = _TOKEN.match(text, pos)
        if not m:
            raise SyntaxError(f"bad token at {text[pos:]!r}")
        out.append(m.group(1))
        pos = m.end()
    return out


class _Parser:
    """Precedence climbing, loosest first: ==> (right-assoc), ||, &&, !, comparisons, shifts (C: looser than +),
    + and -, *, unary minus."""

    def __init__(self, text):
        self.t, self.i = tokenize(text), 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def take(self, want=None):
        tok = self.peek()
        if tok is None or (want is not None and tok != want):
            raise SyntaxError(f"expected {want!r}, got {tok!r}")
        self.i += 1
        return tok

    def implies(self):
        a = self.or_()
        if self.peek() == "==>":
            self.take()
            return ("implies", a, self.implies())
        return a

    def or_(self):
        a = self.and_()
        while self.peek() == "||":
            self.take()
            a = ("or", a, self.and_())
        return a

    def and_(self):
        a = self.not_()
        while self.peek() == "&&":
            self.take()
            a = ("and", a, self.not_())
        return a

    def not_(self):
        if self.peek() == "!":
            self.take()
            return ("not", self.not_())
        return self.cmp()

    def cmp(self):
        a = self.shift()
        if self.peek() in _CMP:
            op = _CMP[self.take()]
            return (op, a, self.shift())
        return a

    def shift(self):
        a = self.add()
        while self.peek() in (">>", ">>>"):
            op = "ashr" if self.take() == ">>" else "lshr"
            self.take("1")
            a = (op, a)
        return a

    def add(self):
        a = self.mul()
        while self.peek() in ("+", "-"):
            op = "add" if self.take() == "+" else "sub"
            a = (op, a, self.mul())
        return a

    def mul(self):
        a = self.unary()
        while self.peek() == "*":
            self.take()
            a = ("mul", a, self.unary())
        return a

    def unary(self):
        if self.peek() == "-":
            self.take()
            e = self.unary()
            return ("const", -e[1]) if e[0] == "const" else ("neg", e)
        return self.atom()

    def atom(self):
        tok = self.take()
        if tok == "(":
            e = self.implies()
            self.take(")")
            return e
        if tok.isdigit():
            return ("const", int(tok))
        if tok in ("true", "false"):
            return (tok,)
        if re.fullmatch(r"[A-Za-z_][A-Za-z_0-9']*", tok):
            return ("var", tok)
        raise SyntaxError(f"unexpected {tok!r}")


def _sort(e):
    """'bool' or 'int'; raises TypeError on an ill-sorted tree."""
    op = e[0]
    if op in ("var", "const"):
        return "int"
    if op in ("true", "false"):
        return "bool"
    want = "bool" if op in ("and", "or", "not", "implies") else "int"
    for sub in e[1:]:
        if _sort(sub) != want:
            raise TypeError(f"{op} expects {want} operands: {e}")
    return "bool" if op in BOOL_OPS else "int"


def parse(text):
    """Parse an expression or assertion; tuples pass through unchanged."""
    if isinstance(text, tuple):
        return text
    p = _Parser(text)
    e = p.implies()
    if p.peek() is not None:
        raise SyntaxError(f"trailing {p.peek()!r} in {text!r}")
    _sort(e)
    return e


def show(e, unicode: bool = False) -> str:
    """Print with the fewest parentheses our parser needs (and always around a shifted sum, for the reader)."""
    sym = _UNI if unicode else _ASCII

    def go(e, need):
        op = e[0]
        p = _PREC[op]
        if op == "var":
            s = e[1]
        elif op == "const":
            s = str(e[1])
            p = 10 if e[1] >= 0 else 9
        elif op in ("true", "false"):
            s = op
        elif op == "neg":
            s = "-" + go(e[1], 9)
        elif op in ("ashr", "lshr"):
            s = go(e[1], 8) + (" >> 1" if op == "ashr" else " >>> 1")
        elif op == "not":
            s = sym["not"] + go(e[1], 10 if e[1][0] != "not" else 4)
        elif op == "implies":
            s = f"{go(e[1], p + 1)} {sym[op]} {go(e[2], p)}"
        elif op in _ARITH or op in ("and", "or"):
            s = f"{go(e[1], p)} {_ARITH.get(op) or sym[op]} {go(e[2], p + 1)}"
        else:                                   # comparison: non-associative
            s = f"{go(e[1], p + 1)} {sym[op]} {go(e[2], p + 1)}"
        return f"({s})" if p < need else s

    return go(e, 0)


def free_vars(e) -> list[str]:
    out = []

    def go(e):
        if e[0] == "var":
            if e[1] not in out:
                out.append(e[1])
        else:
            for sub in e[1:]:
                if isinstance(sub, tuple):
                    go(sub)
    go(e)
    return out


def subst(e, name, repl):
    """e[name := repl] (no binders in our assertions, so no capture)."""
    if e[0] == "var":
        return repl if e[1] == name else e
    if e[0] in ("const", "true", "false"):
        return e
    return (e[0],) + tuple(subst(s, name, repl) for s in e[1:])


def conj(a, b):
    if a == TRUE:
        return b
    if b == TRUE:
        return a
    return ("and", a, b)


def imp(a, b):
    if a == TRUE or b == TRUE:
        return b
    return ("implies", a, b)


def neg(a):
    return a[1] if a[0] == "not" else ("not", a)


def conjuncts(e) -> list:
    return conjuncts(e[1]) + conjuncts(e[2]) if e[0] == "and" else [e]


# ------------------------------------------------------------------------------------------- statements

def assign(x, e):
    return ("assign", x, parse(e))


def if_(c, then, other=()):
    return ("if", parse(c), list(then), list(other))


def while_(c, inv, body, variant=None):
    return ("while", parse(c), parse(inv), list(body), None if variant is None else parse(variant))


def assert_(p):
    return ("assert", parse(p))


def assume(p):
    return ("assume", parse(p))


def havoc(x):
    return ("havoc", x)


def program(name, body, pre="true", post="true", note=""):
    return {"name": name, "pre": parse(pre), "post": parse(post), "body": list(body), "note": note}


# ------------------------------------------------------------------------------------------- semantics

def wrap(v: int, w):
    """Two's complement: the signed w-bit integer congruent to v (identity when w is None)."""
    if w is None:
        return v
    m = 1 << w
    v &= m - 1
    return v - m if v >> (w - 1) else v


def evaluate(e, env: dict, w):
    """Value of e (an int, or a bool for an assertion) in env, over signed w-bit integers."""
    op = e[0]
    if op == "var":
        return env[e[1]]
    if op == "const":
        return wrap(e[1], w)
    if op == "true":
        return True
    if op == "false":
        return False
    if op == "and":
        return evaluate(e[1], env, w) and evaluate(e[2], env, w)
    if op == "or":
        return evaluate(e[1], env, w) or evaluate(e[2], env, w)
    if op == "implies":
        return (not evaluate(e[1], env, w)) or evaluate(e[2], env, w)
    if op == "not":
        return not evaluate(e[1], env, w)
    a = evaluate(e[1], env, w)
    if op == "neg":
        return wrap(-a, w)
    if op == "ashr":
        return a >> 1                                   # Python's >> floors, like an arithmetic shift
    if op == "lshr":
        if w is None:
            if a < 0:
                raise ValueError(">>> of a negative mathematical integer")
            return a >> 1
        return wrap((a & ((1 << w) - 1)) >> 1, w)
    b = evaluate(e[2], env, w)
    if op == "add":
        return wrap(a + b, w)
    if op == "sub":
        return wrap(a - b, w)
    if op == "mul":
        return wrap(a * b, w)
    return {"lt": a < b, "le": a <= b, "gt": a > b, "ge": a >= b, "eq": a == b, "ne": a != b}[op]


class AssertionFailed(Exception):
    pass


class Blocked(Exception):
    """An ``assume`` was false: this execution is not one the specification talks about."""


class OutOfFuel(Exception):
    pass


def run(stmts, env: dict, w, choose=None, fuel: int = 100_000, visit=None) -> dict:
    """Execute concretely; returns the final environment.  ``choose(x, env)`` supplies havoc values; ``visit(stmt,
    env, where)`` is called before every statement (where='before') and at every loop test (where='head')."""
    env = dict(env)
    budget = [fuel]

    def tick():
        budget[0] -= 1
        if budget[0] < 0:
            raise OutOfFuel()

    def block(ss):
        for s in ss:
            tick()
            if visit:
                visit(s, env, "before")
            k = s[0]
            if k == "assign":
                env[s[1]] = evaluate(s[2], env, w)
            elif k == "havoc":
                env[s[1]] = choose(s[1], env)
            elif k == "assert":
                if not evaluate(s[1], env, w):
                    raise AssertionFailed(show(s[1]))
            elif k == "assume":
                if not evaluate(s[1], env, w):
                    raise Blocked(show(s[1]))
            elif k == "if":
                block(s[2] if evaluate(s[1], env, w) else s[3])
            elif k == "while":
                while True:
                    tick()
                    if visit:
                        visit(s, env, "head")
                    if not evaluate(s[1], env, w):
                        break
                    block(s[3])
            else:
                raise ValueError(k)
    block(stmts)
    return env


# ------------------------------------------------------------------------------------------- wp and VCs

def _loops(stmts, out=None):
    out = [] if out is None else out
    for s in stmts:
        if s[0] == "while":
            out.append(s)
            _loops(s[3], out)
        elif s[0] == "if":
            _loops(s[2], out)
            _loops(s[3], out)
    return out


class _VCGen:
    _KIND = {"preserved": 1, "exit": 2, "variant >= 0": 3, "variant decreases": 4}

    def __init__(self, stmts):
        self.number = {id(s): i + 1 for i, s in enumerate(_loops(stmts))}
        self.side = []
        self.k = 0

    def fresh(self, base):
        self.k += 1
        return f"{base}'{self.k}"

    def wp(self, stmts, Q, collect=True):
        for s in reversed(stmts):
            Q = self.wp1(s, Q, collect)
        return Q

    def wp1(self, s, Q, collect=True):
        k = s[0]
        if k == "assign":
            return subst(Q, s[1], s[2])
        if k == "havoc":
            return subst(Q, s[1], var(self.fresh(s[1])))     # fresh => universally quantified in the VC
        if k == "assert":
            return conj(s[1], Q)
        if k == "assume":
            return imp(s[1], Q)
        if k == "if":
            return conj(imp(s[1], self.wp(s[2], Q, collect)), imp(neg(s[1]), self.wp(s[3], Q, collect)))
        if k == "while":
            _, c, inv, body, variant = s
            if collect:
                n = self.number[id(s)]
                ic = conj(inv, c)
                self.side.append((n, "preserved", imp(ic, self.wp(body, inv))))
                self.side.append((n, "exit", imp(conj(inv, neg(c)), Q)))
                if variant is not None:
                    self.side.append((n, "variant >= 0", imp(ic, ("ge", variant, const(0)))))
                    v0 = var(self.fresh("V"))
                    self.side.append((n, "variant decreases",
                                      imp(conj(ic, ("eq", v0, variant)),
                                          self.wp(body, ("lt", variant, v0), collect=False))))
            return inv
        raise ValueError(k)


def wp(stmts, post):
    """Dijkstra's weakest precondition of a statement list (a loop contributes its invariant; its side conditions
    are what ``vcs`` adds)."""
    return _VCGen(stmts).wp(stmts, parse(post), collect=False)


def vcs(prog: dict) -> list[dict]:
    """The verification conditions of a program: each a closed formula (free variables universally quantified)."""
    g = _VCGen(prog["body"])
    main = imp(prog["pre"], g.wp(prog["body"], prog["post"]))
    loops = bool(g.number)
    out = [{"name": "pre ==> wp(body, post)" + ("  (first loop invariant established)" if loops else ""),
            "formula": main}]
    for n, kind, f in sorted(g.side, key=lambda t: (t[0], _VCGen._KIND[t[1]])):
        label = {"preserved": "invariant preserved by the body", "exit": "invariant and exit give what follows",
                 "variant >= 0": "variant is non-negative in the body",
                 "variant decreases": "variant decreases"}[kind]
        out.append({"name": f"loop {n}: {label}", "formula": f})
    for v in out:
        v["text"] = show(v["formula"])
        v["unicode"] = show(v["formula"], unicode=True)
    return out


# ------------------------------------------------------------------------------------------- bit-blasting

class BitBlaster:
    """Tseitin encoding of w-bit terms into CNF over DIMACS literals.  Variable 1 is the constant TRUE (asserted by a
    unit clause), so FALSE is -1.  Gates fold constants and are hash-consed; terms are memoized, so a shared subterm
    such as (lo + hi) >> 1 is built once.  Bit vectors are lists of literals, least significant bit first."""

    def __init__(self, w: int):
        self.w = w
        self.n = 1
        self.T, self.F = 1, -1
        self.clauses = [[1]]
        self.vars: dict[str, list[int]] = {}
        self._gates: dict = {}
        self._terms: dict = {}

    def fresh(self) -> int:
        self.n += 1
        return self.n

    def AND(self, a, b):
        if a == self.F or b == self.F or a == -b:
            return self.F
        if a == self.T or a == b:
            return b
        if b == self.T:
            return a
        key = ("and", min(a, b), max(a, b))
        if key not in self._gates:
            v = self.fresh()
            self.clauses += [[-v, a], [-v, b], [v, -a, -b]]
            self._gates[key] = v
        return self._gates[key]

    def OR(self, a, b):
        return -self.AND(-a, -b)

    def XOR(self, a, b):
        if a == self.F:
            return b
        if b == self.F:
            return a
        if a == self.T:
            return -b
        if b == self.T:
            return -a
        if a == b:
            return self.F
        if a == -b:
            return self.T
        key = ("xor", min(abs(a), abs(b)), max(abs(a), abs(b)))
        flip = (a < 0) != (b < 0)
        if key not in self._gates:
            x, y = key[1], key[2]
            v = self.fresh()
            self.clauses += [[-v, x, y], [-v, -x, -y], [v, -x, y], [v, x, -y]]
            self._gates[key] = v
        return -self._gates[key] if flip else self._gates[key]

    # ---- words
    def word(self, name):
        if name not in self.vars:
            self.vars[name] = [self.fresh() for _ in range(self.w)]
        return self.vars[name]

    def constant(self, n):
        n &= (1 << self.w) - 1
        return [self.T if (n >> i) & 1 else self.F for i in range(self.w)]

    def add(self, xs, ys, carry=None):
        """Ripple-carry adder: s_i = x_i ^ y_i ^ c_i, c_{i+1} = x_i y_i | c_i (x_i ^ y_i)."""
        c = self.F if carry is None else carry
        out = []
        for x, y in zip(xs, ys):
            t = self.XOR(x, y)
            out.append(self.XOR(t, c))
            c = self.OR(self.AND(x, y), self.AND(c, t))
        return out

    def sub(self, xs, ys):
        return self.add(xs, [-y for y in ys], carry=self.T)       # x + ~y + 1

    def mul(self, xs, ys):
        """Shift-and-add: the low w bits of the product."""
        acc = [self.F] * self.w
        for i, y in enumerate(ys):
            part = [self.F] * i + [self.AND(y, x) for x in xs[: self.w - i]]
            acc = self.add(acc, part)
        return acc

    def ult(self, xs, ys):
        """Unsigned x < y, decided from the least significant bit up: the highest differing bit wins."""
        lt = self.F
        for x, y in zip(xs, ys):
            lt = self.OR(self.AND(-x, y), self.AND(-self.XOR(x, y), lt))
        return lt

    def slt(self, xs, ys):
        """Signed x < y: flip both sign bits, then compare unsigned."""
        return self.ult(xs[:-1] + [-xs[-1]], ys[:-1] + [-ys[-1]])

    def eq(self, xs, ys):
        r = self.T
        for x, y in zip(xs, ys):
            r = self.AND(r, -self.XOR(x, y))
        return r

    # ---- expressions
    def term(self, e) -> list[int]:
        if e in self._terms:
            return self._terms[e]
        op = e[0]
        if op == "var":
            r = self.word(e[1])
        elif op == "const":
            r = self.constant(e[1])
        elif op == "neg":
            r = self.sub(self.constant(0), self.term(e[1]))
        elif op == "ashr":
            a = self.term(e[1])
            r = a[1:] + [a[-1]]
        elif op == "lshr":
            r = self.term(e[1])[1:] + [self.F]
        elif op in ("add", "sub", "mul"):
            a, b = self.term(e[1]), self.term(e[2])
            r = getattr(self, op)(a, b)
        else:
            raise TypeError(f"not a term: {e}")
        self._terms[e] = r
        return r

    def prop(self, e) -> int:
        """One literal equivalent to the assertion e."""
        if e in self._terms:
            return self._terms[e]
        op = e[0]
        if op == "true":
            r = self.T
        elif op == "false":
            r = self.F
        elif op == "not":
            r = -self.prop(e[1])
        elif op == "and":
            r = self.AND(self.prop(e[1]), self.prop(e[2]))
        elif op == "or":
            r = self.OR(self.prop(e[1]), self.prop(e[2]))
        elif op == "implies":
            r = self.OR(-self.prop(e[1]), self.prop(e[2]))
        else:
            a, b = self.term(e[1]), self.term(e[2])
            r = {"lt": lambda: self.slt(a, b), "gt": lambda: self.slt(b, a),
                 "le": lambda: -self.slt(b, a), "ge": lambda: -self.slt(a, b),
                 "eq": lambda: self.eq(a, b), "ne": lambda: -self.eq(a, b)}[op]()
        self._terms[e] = r
        return r

    def value(self, lit, model) -> bool:
        return model[lit] if lit > 0 else not model[-lit]

    def decode(self, name, model) -> int:
        bits = self.vars[name]
        return wrap(sum(1 << i for i, b in enumerate(bits) if self.value(b, model)), self.w)


def check_vc(formula, w: int, max_conflicts=None) -> dict:
    """Is the formula true for every assignment of signed w-bit values to its free variables?  Bit-blast it, assert
    its negation, run cdcl: UNSAT means valid, a model is a counterexample (checked again by concrete evaluation)."""
    formula = parse(formula)
    bb = BitBlaster(w)
    lit = bb.prop(formula)
    clauses = bb.clauses + [[-lit]]
    t0 = time.perf_counter()
    model, stats = cdcl(bb.n, clauses, max_conflicts=max_conflicts)
    dt = time.perf_counter() - t0
    status = {"unsat": "valid", "sat": "invalid", "unknown": "unknown"}[stats["status"]]
    cex = None
    if model is not None:
        cex = {name: bb.decode(name, model) for name in free_vars(formula)}
        if evaluate(formula, cex, w):
            raise AssertionError("SAT model does not falsify the formula: encoder bug")
    return {"status": status, "w": w, "vars": bb.n, "clauses": len(clauses), "seconds": round(dt, 4),
            "conflicts": stats["conflicts"], "decisions": stats["decisions"], "counterexample": cex}


def verify(prog: dict, w: int = 16) -> dict:
    """Generate the program's VCs and discharge each with the SAT solver.  For an invalid VC, ``failing`` lists
    the conjuncts of its conclusion that the counterexample falsifies."""
    out = []
    for v in vcs(prog):
        r = check_vc(v["formula"], w)
        row = {"name": v["name"], "text": v["text"], "unicode": v["unicode"], **r}
        if r["counterexample"] is not None:
            f = v["formula"]
            concl = f[2] if f[0] == "implies" else f
            row["failing"] = [show(c) for c in conjuncts(concl) if not evaluate(c, r["counterexample"], w)]
        out.append(row)
    return {"name": prog["name"], "w": w, "pre": show(prog["pre"]), "post": show(prog["post"]),
            "listing": listing(prog), "vcs": out, "proved": all(r["status"] == "valid" for r in out)}


# ------------------------------------------------------------------------------------------- listing and flow

def _code(s):
    k = s[0]
    if k == "assign":
        return f"{s[1]} = {show(s[2])}"
    if k == "havoc":
        return f"havoc {s[1]}"
    if k in ("assert", "assume"):
        return f"{k} {show(s[1])}"
    if k == "if":
        return f"if {show(s[1])}:"
    if k == "while":
        return f"while {show(s[1])}:"
    raise ValueError(k)


def _lines(stmts, depth, out, ids):
    for s in stmts:
        ids[id(s)] = len(out) + 1
        row = {"line": len(out) + 1, "depth": depth, "code": _code(s), "kind": s[0]}
        if s[0] == "while":
            row["invariant"] = show(s[2])
            row["variant"] = None if s[4] is None else show(s[4])
        out.append(row)
        if s[0] == "if":
            _lines(s[2], depth + 1, out, ids)
            if s[3]:
                out.append({"line": len(out) + 1, "depth": depth, "code": "else:", "kind": "else"})
                _lines(s[3], depth + 1, out, ids)
        elif s[0] == "while":
            _lines(s[3], depth + 1, out, ids)
    return out


def line_numbers(stmts) -> dict:
    """id(statement) -> its 1-based line in ``listing``."""
    ids = {}
    _lines(stmts, 0, [], ids)
    return ids


def listing(prog) -> list[dict]:
    """The program as numbered lines: {line, depth, code, kind} (+ invariant and variant on a while line)."""
    return _lines(prog["body"], 0, [], {})


def flow(prog, unicode: bool = False) -> list[dict]:
    """Assertions flowing backward: in animation order (last line first), each step gives the line, its code, the
    assertion after it and the one wp puts before it.  A loop's body starts from its invariant; an if's branches
    flow first, then merge at the if line.  The last step compares the precondition with the computed one."""
    g = _VCGen(prog["body"])
    ids = line_numbers(prog["body"])
    steps = []

    def go(stmts, Q):
        for s in reversed(stmts):
            if s[0] == "if":
                go(s[2], Q)
                go(s[3], Q)
            elif s[0] == "while":
                go(s[3], s[2])
            P = g.wp1(s, Q, collect=False)
            steps.append({"line": ids[id(s)], "code": _code(s), "after": show(Q, unicode),
                          "before": show(P, unicode)})
            Q = P
        return Q

    top = go(prog["body"], prog["post"])
    steps.append({"line": 0, "code": "{pre}", "after": show(top, unicode), "before": show(prog["pre"], unicode)})
    return steps


# ------------------------------------------------------------------------------------------- the examples

def max_program():
    return program("max(a, b)",
                   [if_("a >= b", [assign("m", "a")], [assign("m", "b")])],
                   post="m >= a && m >= b && (m == a || m == b)")


def swap_program():
    return program("swap without a temporary",
                   [assign("x", "x + y"), assign("y", "x - y"), assign("x", "x - y")],
                   pre="x == X && y == Y", post="x == Y && y == X",
                   note="X and Y are ghost variables naming the initial values; the sum may overflow, and wrap-"
                        "around undoes it, so the swap is correct for all w-bit values")


def gauss_program():
    return program("Gauss's summation loop",
                   [assign("i", "0"), assign("s", "0"),
                    while_("i < n", "0 <= i && i <= n && s + s == i * (i + 1)",
                           [assign("i", "i + 1"), assign("s", "s + i")], variant="n - i")],
                   pre="0 <= n", post="s + s == n * (n + 1)",
                   note="s = 1 + 2 + ... + n; 2s = n(n + 1) holds modulo 2^w, so the proof is about wrap-around "
                        "arithmetic and needs no bound on n")


def midpoint_program(mid="(lo + hi) >> 1", pre="0 <= lo && lo < hi"):
    return program(f"mid = {mid}", [assign("mid", mid)], pre=pre, post="lo <= mid && mid < hi")


def binary_search_program(mid="lo + ((hi - lo) >> 1)"):
    """Binary search's control skeleton over [lo, hi): the comparison with the array is an unknown boolean c (havoc),
    so the proof covers every array.  The assertion is the array access a[mid] staying in bounds."""
    return program(f"binary search loop, mid = {mid}",
                   [while_("lo < hi", "0 <= lo && lo <= hi",
                           [assign("mid", mid), assert_("lo <= mid && mid < hi"), havoc("c"),
                            if_("c > 0", [assign("lo", "mid + 1")], [assign("hi", "mid")])],
                           variant="hi - lo")],
                   pre="0 <= lo && lo <= hi", post="lo == hi")


EXAMPLES = {"max": max_program, "swap": swap_program, "gauss": gauss_program,
            "binsearch": binary_search_program}

MIDPOINTS = [("(lo + hi) >> 1", "0 <= lo && lo < hi", "Bloch's bug (Java's (low + high) / 2, 2006)"),
             ("lo + ((hi - lo) >> 1)", "0 <= lo && lo < hi", "Bloch's first fix"),
             ("(lo + hi) >>> 1", "0 <= lo && lo < hi", "Bloch's second fix: the unsigned shift reads the carry"),
             ("lo + ((hi - lo) >> 1)", "lo < hi", "first fix without lo >= 0: hi - lo can overflow"),
             ("lo + ((hi - lo) >>> 1)", "lo < hi", "for any signed lo < hi: hi - lo read as unsigned")]


def midpoint_study(w: int = 16) -> list[dict]:
    """Each midpoint formula against the spec lo <= mid < hi, over all signed w-bit lo, hi.  A counterexample is
    reported with the true sum, the wrapped sum and the midpoint the program computes."""
    out = []
    for mid, pre, note in MIDPOINTS:
        prog = midpoint_program(mid, pre)
        v = vcs(prog)[0]
        r = check_vc(v["formula"], w)
        row = {"mid": mid, "pre": pre, "note": note, "vc": v["text"], "vc_unicode": v["unicode"], **r}
        cex = r["counterexample"]
        if cex is not None:
            lo, hi = cex["lo"], cex["hi"]
            row["detail"] = {"lo": lo, "hi": hi, "true_sum": lo + hi, "wrapped_sum": wrap(lo + hi, w),
                             "true_diff": hi - lo, "wrapped_diff": wrap(hi - lo, w),
                             "mid": run(prog["body"], {"lo": lo, "hi": hi}, w)["mid"]}
        out.append(row)
    return out


def gauss_scaling(widths=(4, 6, 8, 10)) -> list[dict]:
    """Solve time of Gauss's preservation and exit VCs as the word grows: they compare two multipliers, the classic
    hard case for SAT (at w = 12 each takes about a minute, at 16 several minutes, on one loaded core)."""
    vs = vcs(gauss_program())[1:3]
    out = []
    for w in widths:
        rs = [check_vc(v["formula"], w) for v in vs]
        out.append({"w": w, "status": [r["status"] for r in rs], "clauses": [r["clauses"] for r in rs],
                    "conflicts": [r["conflicts"] for r in rs], "seconds": round(sum(r["seconds"] for r in rs), 3)})
    return out


WIDTHS = {"gauss": 8}          # the multiplier VCs; every other program is proved at the full width


def examples(w: int = 16) -> dict:
    """Everything the scenes show: each example verified at width w (Gauss's loop at min(w, 8), see gauss_scaling),
    the midpoint study, the buggy binary search loop, and the backward flow for swap, max and Gauss."""
    progs = {k: f() for k, f in EXAMPLES.items()}
    progs["binsearch_buggy"] = binary_search_program("(lo + hi) >> 1")
    return {"w": w,
            "programs": {k: verify(p, min(w, WIDTHS.get(k, w))) for k, p in progs.items()},
            "midpoints": midpoint_study(w),
            "gauss_scaling": gauss_scaling(),
            "flow": {k: flow(progs[k], unicode=True) for k in ("swap", "max", "gauss")}}
