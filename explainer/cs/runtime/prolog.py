"""A tiny Prolog (Part 15, chapter 15): Horn clauses, depth-first SLD resolution and Robinson's unification, the same
unification that inferred types in Part 14.

Terms: a variable is a string starting with a capital letter; a compound is a tuple ``(functor, arg, ...)``; anything
else is a constant.  Lists are ``("cons", head, tail)`` and ``"nil"``.

    solve(PROGRAM_APPEND, ("append", "X", "Y", plist([1, 2, 3])))    # every split of [1, 2, 3]
"""
from __future__ import annotations

import itertools


def is_var(t):
    return isinstance(t, str) and t[:1].isupper()


def walk(t, s):
    while is_var(t) and t in s:
        t = s[t]
    return t


def occurs(v, t, s):
    t = walk(t, s)
    if t == v:
        return True
    return isinstance(t, tuple) and any(occurs(v, a, s) for a in t[1:])


def unify(a, b, s, stats):
    stats["unify"] += 1
    a, b = walk(a, s), walk(b, s)
    if a == b:
        return s
    if is_var(a):
        return None if occurs(a, b, s) else {**s, a: b}
    if is_var(b):
        return None if occurs(b, a, s) else {**s, b: a}
    if isinstance(a, tuple) and isinstance(b, tuple) and a[0] == b[0] and len(a) == len(b):
        for x, y in zip(a[1:], b[1:]):
            s = unify(x, y, s, stats)
            if s is None:
                return None
        return s
    return None


_fresh = itertools.count()


def rename(t, m):
    if is_var(t):
        if t not in m:
            m[t] = f"{t}_{next(_fresh)}"
        return m[t]
    if isinstance(t, tuple):
        return (t[0],) + tuple(rename(a, m) for a in t[1:])
    return t


def resolve(t, s):
    t = walk(t, s)
    if isinstance(t, tuple):
        return (t[0],) + tuple(resolve(a, s) for a in t[1:])
    return t


def solve(program, goal, limit=100):
    """Every answer to goal, as substitutions restricted to goal's variables, with counts of work."""
    stats = {"unify": 0, "resolutions": 0}
    goal_vars = sorted({v for v in _vars(goal)})
    out = []

    def go(goals, s, depth):
        if len(out) >= limit or depth > 200:
            return
        if not goals:
            out.append({v: resolve(v, s) for v in goal_vars})
            return
        g, rest = goals[0], goals[1:]
        for head, body in program:
            m = {}
            h, b = rename(head, m), [rename(x, m) for x in body]
            s2 = unify(g, h, s, stats)
            if s2 is not None:
                stats["resolutions"] += 1
                go(b + rest, s2, depth + 1)
    go([goal], {}, 0)
    return out, stats


def _vars(t):
    if is_var(t):
        yield t
    elif isinstance(t, tuple):
        for a in t[1:]:
            yield from _vars(a)


def plist(xs):
    t = "nil"
    for x in reversed(xs):
        t = ("cons", x, t)
    return t


def unlist(t):
    out = []
    while isinstance(t, tuple) and t[0] == "cons":
        out.append(t[1])
        t = t[2]
    return out if t == "nil" else out + ["|", t]


# append([], Ys, Ys).   append([X|Xs], Ys, [X|Zs]) :- append(Xs, Ys, Zs).
PROGRAM_APPEND = [
    (("append", "nil", "Ys", "Ys"), []),
    (("append", ("cons", "X", "Xs"), "Ys", ("cons", "X", "Zs")), [("append", "Xs", "Ys", "Zs")]),
]

PROGRAM_APPEND_TEXT = """append([], Ys, Ys).
append([X|Xs], Ys, [X|Zs]) :- append(Xs, Ys, Zs)."""
