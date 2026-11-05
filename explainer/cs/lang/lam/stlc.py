"""The simply typed λ-calculus with booleans and naturals (Pierce, *TAPL*, ch. 8–9), for Part 14.

    t = parse(r"(\\x:Nat. succ x) (succ 0)")
    T, d = typecheck(t)          # Nat, and the derivation tree
    trace(t)                     # every small step with the rule that justifies it

* :func:`typecheck` returns the type and the derivation (rule, judgement, premises), so scenes can draw the tree.
* :func:`step` is call-by-value small-step evaluation; a closed term that is neither a value nor able to step is
  *stuck*.
* :func:`gen` builds random closed well-typed terms of a given type; :func:`safety` checks progress and
  preservation on every step of every one of them, and records how many steps each takes to finish (strong
  normalization: all of them do).  :func:`stuck_examples` finds ill-typed terms that get stuck.
* ``fix`` is available as an extension: with it, well-typed terms can run forever.
"""
from __future__ import annotations

import random
import re

BOOL, NAT = ("Bool",), ("Nat",)


def arrow(a, b):
    return ("->", a, b)


def tshow(T) -> str:
    if T[0] == "->":
        a = tshow(T[1])
        if T[1][0] == "->":
            a = f"({a})"
        return f"{a} → {tshow(T[2])}"
    return T[0]


def ttex(T) -> str:
    if T[0] == "->":
        a = ttex(T[1])
        if T[1][0] == "->":
            a = f"({a})"
        return rf"{a} \to {ttex(T[2])}"
    return rf"\mathsf{{{T[0]}}}"


class TypeErr(Exception):
    pass


# -- syntax ----------------------------------------------------------------------------------------------------
def parse(s: str):
    toks = re.findall(r"\\|λ|→|->|:|\.|\(|\)|\d+|[A-Za-z_][A-Za-z0-9_']*", s)
    pos = 0

    def peek():
        return toks[pos] if pos < len(toks) else None

    def take(x=None):
        nonlocal pos
        t = toks[pos]
        if x is not None and t != x:
            raise SyntaxError(f"expected {x}, got {t}")
        pos += 1
        return t

    def typ():
        a = tatom()
        if peek() in ("->", "→"):
            take()
            return arrow(a, typ())
        return a

    def tatom():
        t = take()
        if t == "(":
            T = typ()
            take(")")
            return T
        return {"Bool": BOOL, "Nat": NAT}[t]

    def term():
        if peek() in ("\\", "λ"):
            take()
            x = take()
            take(":")
            T = typ()
            take(".")
            return ("lam", x, T, term())
        if peek() == "if":
            take()
            c = term()
            take("then")
            a = term()
            take("else")
            return ("if", c, a, term())
        t = app()
        return t

    def app():
        t = atom()
        while peek() not in (None, ")", "then", "else"):
            if peek() in ("\\", "λ", "if"):
                t = ("app", t, term())
            else:
                t = ("app", t, atom())
        return t

    def atom():
        t = take()
        if t == "(":
            u = term()
            take(")")
            return u
        if t in ("succ", "pred", "iszero", "fix"):
            return (t, atom())
        if t == "true":
            return ("true",)
        if t == "false":
            return ("false",)
        if t.isdigit():
            u = ("zero",)
            for _ in range(int(t)):
                u = ("succ", u)
            return u
        return ("var", t)

    t = term()
    if pos != len(toks):
        raise SyntaxError("trailing tokens")
    return t


def show(t) -> str:
    k = t[0]
    if k == "var":
        return t[1]
    if k in ("true", "false"):
        return k
    if k == "zero":
        return "0"
    if k == "succ":
        n, u = 1, t[1]
        while u[0] == "succ":
            n, u = n + 1, u[1]
        if u[0] == "zero":
            return str(n)
        return f"succ {_paren(t[1])}"
    if k in ("pred", "iszero", "fix"):
        return f"{k} {_paren(t[1])}"
    if k == "lam":
        return f"λ{t[1]}:{tshow(t[2])}. {show(t[3])}"
    if k == "if":
        return f"if {show(t[1])} then {show(t[2])} else {show(t[3])}"
    f, a = t[1], t[2]
    fs = show(f)
    if f[0] in ("lam", "if"):
        fs = f"({fs})"
    return f"{fs} {_paren(a)}"


def _paren(t):
    s = show(t)
    simple = t[0] in ("var", "true", "false", "zero") or (t[0] == "succ" and s.isdigit())
    return s if simple else f"({s})"


# -- typing, with derivations ----------------------------------------------------------------------------------
def typecheck(t, ctx=None):
    """(type, derivation); a derivation is (rule, context, term, type, [premises])."""
    ctx = ctx or {}

    def d(rule, t, T, prem):
        return (rule, dict(ctx), t, T, prem)

    k = t[0]
    if k == "var":
        if t[1] not in ctx:
            raise TypeErr(f"{t[1]} is not bound")
        return ctx[t[1]], d("T-Var", t, ctx[t[1]], [])
    if k in ("true", "false"):
        return BOOL, d("T-" + k.capitalize(), t, BOOL, [])
    if k == "zero":
        return NAT, d("T-Zero", t, NAT, [])
    if k in ("succ", "pred"):
        T, p = typecheck(t[1], ctx)
        if T != NAT:
            raise TypeErr(f"{k} expects Nat, got {tshow(T)}")
        return NAT, d("T-" + k.capitalize(), t, NAT, [p])
    if k == "iszero":
        T, p = typecheck(t[1], ctx)
        if T != NAT:
            raise TypeErr(f"iszero expects Nat, got {tshow(T)}")
        return BOOL, d("T-IsZero", t, BOOL, [p])
    if k == "if":
        C, p1 = typecheck(t[1], ctx)
        if C != BOOL:
            raise TypeErr(f"if expects a Bool condition, got {tshow(C)}")
        A, p2 = typecheck(t[2], ctx)
        B, p3 = typecheck(t[3], ctx)
        if A != B:
            raise TypeErr(f"branches differ: {tshow(A)} and {tshow(B)}")
        return A, d("T-If", t, A, [p1, p2, p3])
    if k == "lam":
        B, p = typecheck(t[3], {**ctx, t[1]: t[2]})
        T = arrow(t[2], B)
        return T, d("T-Abs", t, T, [p])
    if k == "app":
        F, p1 = typecheck(t[1], ctx)
        A, p2 = typecheck(t[2], ctx)
        if F[0] != "->":
            raise TypeErr(f"applying a {tshow(F)}, which is not a function")
        if F[1] != A:
            raise TypeErr(f"argument is {tshow(A)}, expected {tshow(F[1])}")
        return F[2], d("T-App", t, F[2], [p1, p2])
    if k == "fix":
        F, p = typecheck(t[1], ctx)
        if F[0] != "->" or F[1] != F[2]:
            raise TypeErr("fix expects T → T")
        return F[1], d("T-Fix", t, F[1], [p])
    raise TypeErr(f"unknown term {k}")


def deriv_size(d) -> int:
    return 1 + sum(deriv_size(p) for p in d[4])


# -- evaluation ------------------------------------------------------------------------------------------------
def is_num(t):
    return t[0] == "zero" or (t[0] == "succ" and is_num(t[1]))


def is_value(t):
    return t[0] in ("true", "false", "lam") or is_num(t)


def subst(t, x, s):
    """t[x := s]; s is closed in our uses (call-by-value on closed programs), so no capture can occur."""
    k = t[0]
    if k == "var":
        return s if t[1] == x else t
    if k == "lam":
        return t if t[1] == x else ("lam", t[1], t[2], subst(t[3], x, s))
    if k in ("true", "false", "zero"):
        return t
    return (k,) + tuple(subst(u, x, s) for u in t[1:])


def step(t):
    """One call-by-value step: (term, rule) or None if t is a value or stuck."""
    k = t[0]
    if k == "if":
        c = t[1]
        if c[0] == "true":
            return t[2], "E-IfTrue"
        if c[0] == "false":
            return t[3], "E-IfFalse"
        r = step(c)
        return (("if", r[0], t[2], t[3]), "E-If") if r else None
    if k == "succ":
        r = step(t[1])
        return (("succ", r[0]), "E-Succ") if r else None
    if k == "pred":
        u = t[1]
        if u[0] == "zero":
            return ("zero",), "E-PredZero"
        if u[0] == "succ" and is_num(u[1]):
            return u[1], "E-PredSucc"
        r = step(u)
        return (("pred", r[0]), "E-Pred") if r else None
    if k == "iszero":
        u = t[1]
        if u[0] == "zero":
            return ("true",), "E-IsZeroZero"
        if u[0] == "succ" and is_num(u[1]):
            return ("false",), "E-IsZeroSucc"
        r = step(u)
        return (("iszero", r[0]), "E-IsZero") if r else None
    if k == "app":
        f, a = t[1], t[2]
        if not is_value(f):
            r = step(f)
            return (("app", r[0], a), "E-App1") if r else None
        if not is_value(a):
            r = step(a)
            return (("app", f, r[0]), "E-App2") if r else None
        if f[0] == "lam":
            return subst(f[3], f[1], a), "E-AppAbs"
        return None
    if k == "fix":
        f = t[1]
        if not is_value(f):
            r = step(f)
            return (("fix", r[0]), "E-Fix") if r else None
        if f[0] == "lam":
            return subst(f[3], f[1], t), "E-FixBeta"
        return None
    return None


def trace(t, max_steps=10_000):
    out = [(t, None)]
    for _ in range(max_steps):
        r = step(t)
        if r is None:
            return out
        t = r[0]
        out.append(r)
    return out


def size(t) -> int:
    return 1 + sum(size(u) for u in t[1:] if isinstance(u, tuple) and u and isinstance(u[0], str) and
                   u[0] not in ("->", "Bool", "Nat"))


# -- random well-typed terms; the safety theorems checked -----------------------------------------------------
def gen(T, depth, rng, ctx=()):
    """A random closed (in ctx) term of type T."""
    vars_ = [x for x, U in ctx if U == T]
    opts = []
    if vars_:
        opts.append("var")
    if T == BOOL:
        opts += ["true", "false"] + (["iszero", "if", "app"] * 2 if depth > 0 else [])
    elif T == NAT:
        opts += ["zero"] + (["succ", "pred", "if", "app"] * 2 if depth > 0 else [])
    else:
        opts += ["lam"] + (["if", "app"] if depth > 0 else [])
    c = rng.choice(opts)
    if c == "var":
        return ("var", rng.choice(vars_))
    if c in ("true", "false", "zero"):
        return (c,)
    if c in ("succ", "pred"):
        return (c, gen(NAT, depth - 1, rng, ctx))
    if c == "iszero":
        return ("iszero", gen(NAT, depth - 1, rng, ctx))
    if c == "if":
        return ("if", gen(BOOL, depth - 1, rng, ctx), gen(T, depth - 1, rng, ctx), gen(T, depth - 1, rng, ctx))
    if c == "lam":
        x = f"x{len(ctx)}"
        return ("lam", x, T[1], gen(T[2], max(depth - 1, 0), rng, ctx + ((x, T[1]),)))
    A = rng.choice([BOOL, NAT, arrow(NAT, NAT)])
    return ("app", gen(arrow(A, T), depth - 1, rng, ctx), gen(A, depth - 1, rng, ctx))


def safety(n=2000, depth=5, seed=1):
    """Check progress and preservation on every step of n random closed well-typed terms."""
    rng = random.Random(seed)
    types = [BOOL, NAT, arrow(NAT, NAT), arrow(BOOL, NAT)]
    steps, checked, longest = [], 0, None
    for i in range(n):
        T = types[i % len(types)]
        t = gen(T, depth, rng)
        T0, _ = typecheck(t)
        assert T0 == T
        k = 0
        while True:
            if is_value(t):
                break
            r = step(t)
            assert r is not None, ("progress fails", show(t))          # progress
            t = r[0]
            assert typecheck(t)[0] == T, ("preservation fails", show(t))  # preservation
            k += 1
            checked += 1
            assert k < 100_000
        steps.append(k)
        if longest is None or k > longest[0]:
            longest = (k, i)
    return {"terms": n, "steps_checked": checked, "max_steps": max(steps), "mean_steps": sum(steps) / n,
            "all_terminated": True}


def stuck_examples():
    out = []
    for src in ("if 0 then true else false", "succ true", "pred (iszero 0)", "(true 0)", "iszero (\\x:Nat. x)"):
        t = parse(src)
        tr = trace(t)
        last = tr[-1][0]
        try:
            typecheck(t)
            why = None
        except TypeErr as e:
            why = str(e)
        out.append({"term": src, "stops_at": show(last), "value": is_value(last), "type_error": why})
    return out
