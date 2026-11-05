"""The untyped λ-calculus beyond normal order (Part 14).

* :func:`redexes` lists every redex; :func:`step` reduces by a named strategy (normal, applicative, by name, by value);
  :func:`run` counts the steps each strategy needs, or reports that it never stops.
* :func:`lazy_eval` is an environment machine with thunks, so call-by-need's sharing can be counted: how many
  times an argument is evaluated under call-by-name, call-by-value and call-by-need.
* :func:`graph` is the whole reduction graph of a small term (every way to reduce it, terms identified up to α),
  which shows Church–Rosser confluence; :func:`develop` is a complete development (Takahashi's t*), the parallel
  step that makes the diamond close in one move.
* :func:`debruijn` writes a term with indices instead of names.
* ``LIB`` holds the Church encodings: booleans, numerals, pairs, the predecessor by Kleene's pairing trick, lists,
  and the fixed-point combinators Y and Z.
"""
from __future__ import annotations

from collections import deque

from explainer.cs.lam import App, Lam, Var, alpha_eq, at, beta, church, free, parse, replace, show, subst, unchurch

# -- Church encodings ------------------------------------------------------------------------------------------
LIB = {
    "true": r"\t f. t",
    "false": r"\t f. f",
    "and": r"\p q. p q p",
    "or": r"\p q. p p q",
    "not": r"\p t f. p f t",
    "if": r"\b x y. b x y",
    "succ": r"\n f x. f (n f x)",
    "plus": r"\m n f x. m f (n f x)",
    "times": r"\m n f. m (n f)",
    "pow": r"\m n. n m",
    "iszero": r"\n. n (\z t f. f) (\t f. t)",
    "pair": r"\a b s. s a b",
    "fst": r"\p. p (\a b. a)",
    "snd": r"\p. p (\a b. b)",
    # Kleene's trick: count up pairs (n-1, n) from (0, 0), keep the first
    "pred": r"\n. (\p. p (\a b. a)) (n (\p. (\a b s. s a b) ((\p. p (\a b. b)) p) ((\n f x. f (n f x)) ((\p. p (\a b. b)) p))) ((\a b s. s a b) (\f x. x) (\f x. x)))",
    "nil": r"\c n. n",
    "cons": r"\h t c n. c h (t c n)",
    "Y": r"\f. (\x. f (x x)) (\x. f (x x))",
    "Z": r"\f. (\x. f (\v. x x v)) (\x. f (\v. x x v))",
    "omega": r"(\x. x x) (\x. x x)",
}


def lib(name):
    return parse(LIB[name])


def apply(*ts):
    t = ts[0]
    for a in ts[1:]:
        t = App(t, a)
    return t


def num(n):
    return church(n)


def size(t) -> int:
    if t[0] == "var":
        return 1
    if t[0] == "lam":
        return 1 + size(t[2])
    return 1 + size(t[1]) + size(t[2])


# -- redexes and strategies ------------------------------------------------------------------------------------
def redexes(t, path=()):
    """Every redex, as paths, in left-to-right order of their position in the printed term."""
    out = []
    if t[0] == "app":
        if t[1][0] == "lam":
            out.append(tuple(path))
        out += redexes(t[1], list(path) + [0])
        out += redexes(t[2], list(path) + [1])
    elif t[0] == "lam":
        out += redexes(t[2], list(path) + [1])
    return out


def _innermost(t, path=()):
    """Leftmost innermost redex (applicative order)."""
    if t[0] == "app":
        p = _innermost(t[1], list(path) + [0])
        if p is not None:
            return p
        p = _innermost(t[2], list(path) + [1])
        if p is not None:
            return p
        if t[1][0] == "lam":
            return tuple(path)
    elif t[0] == "lam":
        return _innermost(t[2], list(path) + [1])
    return None


def _weak(t, path=(), by_value=False):
    """Weak reduction (never under λ): leftmost outermost (by name) or with arguments first (by value)."""
    if t[0] != "app":
        return None
    f, a = t[1], t[2]
    if f[0] == "lam":
        if by_value and a[0] == "app":
            p = _weak(a, list(path) + [1], by_value)
            if p is not None:
                return p
        return tuple(path)
    p = _weak(f, list(path) + [0], by_value)
    if p is not None:
        return p
    if by_value:
        return _weak(a, list(path) + [1], by_value)
    return None


def choose(t, strategy: str):
    from explainer.cs.lam import find_redex
    if strategy == "normal":
        return find_redex(t)
    if strategy == "applicative":
        return _innermost(t)
    if strategy == "name":
        return _weak(t)
    if strategy == "value":
        return _weak(t, by_value=True)
    raise KeyError(strategy)


def step(t, strategy="normal"):
    p = choose(t, strategy)
    return None if p is None else beta(t, p)


def run(t, strategy="normal", max_steps=2000, max_size=20000):
    """(steps, final term) or (None, last term) if it did not stop within the limits."""
    for n in range(max_steps):
        p = choose(t, strategy)
        if p is None:
            return n, t
        t = beta(t, p)
        if size(t) > max_size:
            return None, t
    return None, t


# -- an environment machine with thunks: by name, by value, by need -------------------------------------------
class Diverge(Exception):
    pass


class _Thunk:
    __slots__ = ("term", "env", "value", "forced")

    def __init__(self, term, env):
        self.term, self.env, self.value, self.forced = term, env, None, 0


def lazy_eval(t, mode="need", prims=None, fuel=200000):
    """Evaluate t to weak head normal form with closures.  ``prims`` maps free variable names to Python values
    (numbers, or functions of one argument), so Church numerals can be read back as ``n succ 0``.  Returns
    (value, stats) with stats counting β-steps and how often each argument expression was evaluated."""
    stats = {"beta": 0, "evals": 0}
    budget = [fuel]

    def force(th):
        if mode == "need" and th.value is not None:
            return th.value
        th.forced += 1
        stats["evals"] += 1
        v = ev(th.term, th.env)
        if mode == "need":
            th.value = v
        return v

    def ev(t, env):
        budget[0] -= 1
        if budget[0] < 0:
            raise Diverge()
        k = t[0]
        if k == "var":
            x = t[1]
            if x in env:
                v = env[x]
                return force(v) if isinstance(v, _Thunk) else v
            if prims and x in prims:
                return prims[x]
            raise NameError(x)
        if k == "lam":
            return ("clo", t[1], t[2], env)
        f = ev(t[1], env)
        if mode == "value":
            stats["evals"] += 1
            arg = ev(t[2], env)
        else:
            arg = _Thunk(t[2], env)
        return applyv(f, arg)

    def applyv(f, arg):
        if callable(f):
            a = force(arg) if isinstance(arg, _Thunk) else arg
            return f(a)
        if not (isinstance(f, tuple) and f[0] == "clo"):
            raise TypeError("applying a non-function")
        stats["beta"] += 1
        _, x, body, env = f
        return ev(body, {**env, x: arg})

    import sys
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old, 20000))
    try:
        v = ev(t, {})
    except RecursionError:
        raise Diverge() from None
    finally:
        sys.setrecursionlimit(old)
    return v, stats


def read_number(t, mode="value"):
    """A Church numeral's value, by applying it to a Python successor and zero."""
    from explainer.cs.lam import App as A
    term = A(A(t, Var("__succ")), Var("__zero"))
    v, st = lazy_eval(term, mode, prims={"__succ": lambda k: k + 1, "__zero": 0})
    return v, st


# -- the reduction graph, confluence and complete developments ------------------------------------------------
def debruijn(t, env=()):
    """Nameless form: λ.λ.1 (0 1) for \\f x. f x ... as a nested tuple; free variables keep their names."""
    k = t[0]
    if k == "var":
        return ("var", env.index(t[1])) if t[1] in env else ("free", t[1])
    if k == "lam":
        return ("lam", debruijn(t[2], (t[1],) + env))
    return ("app", debruijn(t[1], env), debruijn(t[2], env))


def show_db(d) -> str:
    k = d[0]
    if k == "var":
        return str(d[1])
    if k == "free":
        return d[1]
    if k == "lam":
        return "λ. " + show_db(d[1])
    f, a = d[1], d[2]
    fs = show_db(f)
    if f[0] == "lam":
        fs = f"({fs})"
    as_ = show_db(a)
    if a[0] in ("app", "lam"):
        as_ = f"({as_})"
    return f"{fs} {as_}"


def graph(t, limit=200):
    """Breadth-first over every one-step reduct.  Returns (nodes, edges, normal) with nodes a list of terms (the
    first is t), edges (i, j, path) and normal the indices of normal forms."""
    key = {debruijn(t): 0}
    nodes, edges = [t], []
    q = deque([0])
    while q and len(nodes) < limit:
        i = q.popleft()
        for p in redexes(nodes[i]):
            u = beta(nodes[i], p)
            k = debruijn(u)
            if k not in key:
                key[k] = len(nodes)
                nodes.append(u)
                q.append(key[k])
            edges.append((i, key[k], p))
    normal = [i for i, n in enumerate(nodes) if not redexes(n)]
    return nodes, edges, normal


def develop(t):
    """Takahashi's complete development t*: contract every redex present in t, innermost first."""
    k = t[0]
    if k == "var":
        return t
    if k == "lam":
        return Lam(t[1], develop(t[2]))
    f, a = t[1], t[2]
    if f[0] == "lam":
        return subst(develop(f[2]), f[1], develop(a))
    return App(develop(f), develop(a))


def confluent(t, limit=200) -> bool:
    """Every pair of reducts in the graph has a common reduct (checked on the finite graph)."""
    nodes, edges, _ = graph(t, limit)
    succ = {i: set() for i in range(len(nodes))}
    for i, j, _ in edges:
        succ[i].add(j)

    def reach(i):
        seen, st = {i}, [i]
        while st:
            x = st.pop()
            for y in succ[x]:
                if y not in seen:
                    seen.add(y)
                    st.append(y)
        return seen
    R = {i: reach(i) for i in range(len(nodes))}
    return all(R[a] & R[b] for a in range(len(nodes)) for b in range(len(nodes)))
