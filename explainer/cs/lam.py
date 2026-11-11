"""The untyped λ-calculus (Church 1936): terms, capture-avoiding substitution, normal-order reduction (Part 1;
Part 14 builds on it).

    t = parse(r"(\\m n f x. m f (n f x)) (\\f x. f (f x)) (\\f x. f (f (f x)))")
    steps = normalize(t)          # every term on the way, with the redex that was reduced
    show(steps[-1].term)          # '\\f x. f (f (f (f (f x))))'
    church(5) == steps[-1].term   # alpha-equivalence

Terms are tuples: ('var', name), ('lam', name, body), ('app', fun, arg).  Normal order reduces the leftmost
outermost redex first, which finds a normal form whenever one exists (the standardization theorem, Part 14).
"""

from __future__ import annotations

import re
from dataclasses import dataclass


def Var(x):
    return ("var", x)


def Lam(x, b):
    return ("lam", x, b)


def App(f, a):
    return ("app", f, a)


# -- parsing -------------------------------------------------------------------------
def parse(s: str):
    toks = re.findall(r"\\|λ|\.|\(|\)|[A-Za-z_][A-Za-z0-9_']*", s)
    pos = 0

    def peek():
        return toks[pos] if pos < len(toks) else None

    def take():
        nonlocal pos
        pos += 1
        return toks[pos - 1]

    def term():
        if peek() in ("\\", "λ"):
            take()
            names = []
            while peek() != ".":
                names.append(take())
            take()
            body = term()
            for x in reversed(names):
                body = Lam(x, body)
            return body
        t = atom()
        while peek() not in (None, ")"):
            t = App(t, term() if peek() in ("\\", "λ") else atom())
        return t

    def atom():
        tok = take()
        if tok == "(":
            t = term()
            assert take() == ")"
            return t
        return Var(tok)

    t = term()
    assert pos == len(toks), f"trailing tokens in {s!r}"
    return t


# -- printing --------------------------------------------------------------------------
def show(t, lam="\\") -> str:
    """Minimal parentheses; nested abstractions merged (\\f x. ...)."""
    k = t[0]
    if k == "var":
        return t[1]
    if k == "lam":
        names, b = [t[1]], t[2]
        while b[0] == "lam":
            names.append(b[1])
            b = b[2]
        return f"{lam}{' '.join(names)}. {show(b, lam)}"
    f, a = t[1], t[2]
    fs = show(f, lam)
    if f[0] == "lam":
        fs = f"({fs})"
    as_ = show(a, lam)
    if a[0] != "var":
        as_ = f"({as_})"
    return f"{fs} {as_}"


def tex(t, colors: dict | None = None, path=(), redex=None) -> str:
    """A term as LaTeX (math mode), the redex at ``redex`` (a path) wrapped in \\colorbox-free colour markers that
    scenes split on: {{...}} around it."""
    k = t[0]
    here = redex is not None and tuple(path) == tuple(redex)
    if k == "var":
        s = t[1]
    elif k == "lam":
        names, b, p = [t[1]], t[2], list(path) + [1]
        while b[0] == "lam" and not (redex is not None and tuple(p) == tuple(redex)):
            names.append(b[1])
            b, p = b[2], p + [1]
        s = r"\lambda " + r"\,".join(names) + r".\," + tex(b, colors, p, redex)
    else:
        f, a = t[1], t[2]
        fs = tex(f, colors, list(path) + [0], redex)
        if f[0] == "lam":
            fs = rf"({fs})"
        as_ = tex(a, colors, list(path) + [1], redex)
        if a[0] != "var":
            as_ = rf"({as_})"
        s = rf"{fs}\;{as_}"
    return f"{{{{{s}}}}}" if here else s


# -- substitution and reduction -----------------------------------------------------------
def free(t) -> set:
    if t[0] == "var":
        return {t[1]}
    if t[0] == "lam":
        return free(t[2]) - {t[1]}
    return free(t[1]) | free(t[2])


def _fresh(x, avoid):
    base = x.rstrip("'")
    n = base + "'"
    while n in avoid:
        n += "'"
    return n


def subst(t, x, s):
    """t[x := s], renaming bound variables that would capture a free variable of s."""
    if t[0] == "var":
        return s if t[1] == x else t
    if t[0] == "app":
        return App(subst(t[1], x, s), subst(t[2], x, s))
    y, b = t[1], t[2]
    if y == x:
        return t
    if y in free(s) and x in free(b):
        z = _fresh(y, free(s) | free(b) | {x})
        b = subst(b, y, Var(z))
        y = z
    return Lam(y, subst(b, x, s))


def find_redex(t, path=()):
    """The path to the leftmost outermost redex, or None (normal form)."""
    if t[0] == "app":
        if t[1][0] == "lam":
            return tuple(path)
        p = find_redex(t[1], list(path) + [0])
        return p if p is not None else find_redex(t[2], list(path) + [1])
    if t[0] == "lam":
        return find_redex(t[2], list(path) + [1])
    return None


def at(t, path):
    for i in path:
        t = t[1 + i] if t[0] == "app" else t[2]
    return t


def replace(t, path, new):
    if not path:
        return new
    i, rest = path[0], path[1:]
    if t[0] == "app":
        return App(replace(t[1], rest, new), t[2]) if i == 0 else App(t[1], replace(t[2], rest, new))
    return Lam(t[1], replace(t[2], rest, new))


def beta(t, path):
    r = at(t, path)
    (_, x, body), arg = r[1], r[2]
    return replace(t, path, subst(body, x, arg))


@dataclass
class StepRec:
    term: tuple
    redex: tuple | None  # the redex reduced to reach the next term


def normalize(t, max_steps: int = 10_000) -> list[StepRec]:
    out = []
    for _ in range(max_steps):
        p = find_redex(t)
        out.append(StepRec(t, p))
        if p is None:
            return out
        t = beta(t, p)
    raise RuntimeError("no normal form within max_steps")


def alpha_eq(a, b, env_a=None, env_b=None, depth=0) -> bool:
    env_a, env_b = env_a or {}, env_b or {}
    if a[0] != b[0]:
        return False
    if a[0] == "var":
        return env_a.get(a[1], a[1]) == env_b.get(b[1], b[1])
    if a[0] == "lam":
        return alpha_eq(a[2], b[2], {**env_a, a[1]: f"#{depth}"}, {**env_b, b[1]: f"#{depth}"}, depth + 1)
    return alpha_eq(a[1], b[1], env_a, env_b, depth) and alpha_eq(a[2], b[2], env_a, env_b, depth)


def church(n: int):
    body = Var("x")
    for _ in range(n):
        body = App(Var("f"), body)
    return Lam("f", Lam("x", body))


def unchurch(t) -> int | None:
    if t[0] != "lam" or t[2][0] != "lam":
        return None
    f, x, b = t[1], t[2][1], t[2][2]
    n = 0
    while b[0] == "app" and b[1] == ("var", f):
        n, b = n + 1, b[2]
    return n if b == ("var", x) else None


PLUS = r"\m n f x. m f (n f x)"
TIMES = r"\m n f. m (n f)"
POW = r"\m n. n m"
SUCC = r"\n f x. f (n f x)"
TRUE, FALSE = r"\x y. x", r"\x y. y"
OMEGA = r"(\x. x x) (\x. x x)"
Y = r"\f. (\x. f (x x)) (\x. f (x x))"
