"""Resolution for Part 2 (Robinson 1965): propositional and first-order clauses, refutation by saturation.

A literal is (sign, predicate, args) with args a tuple of terms; a term is a variable (a string starting with a
lower-case letter), a constant (upper-case), or a function application (name, args). A clause is a frozenset of
literals. :func:`refute` adds the negated goal and resolves pairs of clauses level by level until it derives the
empty clause, recording every clause made and the two parents of each, so the proof can be drawn as a tree.
"""

from __future__ import annotations

import itertools


def is_var(t) -> bool:
    return isinstance(t, str) and t[:1].islower()


def substitute(t, s: dict):
    if is_var(t):
        return substitute(s[t], s) if t in s else t
    if isinstance(t, tuple):
        return (t[0], tuple(substitute(a, s) for a in t[1]))
    return t


def occurs(v, t, s) -> bool:
    t = substitute(t, s)
    if t == v:
        return True
    return isinstance(t, tuple) and any(occurs(v, a, s) for a in t[1])


def unify(x, y, s: dict | None):
    """Most general unifier of two terms (or argument tuples), extending ``s``; None if there is none."""
    if s is None:
        return None
    x, y = substitute(x, s), substitute(y, s)
    if x == y:
        return s
    if is_var(x):
        return None if occurs(x, y, s) else {**s, x: y}
    if is_var(y):
        return None if occurs(y, x, s) else {**s, y: x}
    if isinstance(x, tuple) and isinstance(y, tuple) and len(x) == 2 and isinstance(x[1], tuple):
        if x[0] != y[0] or len(x[1]) != len(y[1]):
            return None
        for a, b in zip(x[1], y[1]):
            s = unify(a, b, s)
            if s is None:
                return None
        return s
    if isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        for a, b in zip(x, y):
            s = unify(a, b, s)
        return s
    return None


def lit(sign: bool, pred: str, *args):
    return (sign, pred, tuple(args))


def show_term(t) -> str:
    if isinstance(t, tuple):
        return f"{t[0]}({', '.join(show_term(a) for a in t[1])})"
    return t


def show_lit(l) -> str:
    sign, p, args = l
    body = p if not args else f"{p}({', '.join(show_term(a) for a in args)})"
    return body if sign else "¬" + body


def show_clause(c) -> str:
    if not c:
        return "□"
    return " ∨ ".join(show_lit(l) for l in sorted(c, key=lambda l: (l[1], not l[0], str(l[2]))))


def _rename(c, k: int):
    """Standardize apart: give the clause's variables fresh names."""
    def ren(t):
        if is_var(t):
            return f"{t}_{k}"
        if isinstance(t, tuple):
            return (t[0], tuple(ren(a) for a in t[1]))
        return t
    return frozenset((s, p, tuple(ren(a) for a in args)) for s, p, args in c)


def _clean(c):
    """Rename variables to x, y, z, ... in order of appearance (so equal clauses compare equal)."""
    names, out = {}, []
    order = sorted(c, key=lambda l: (l[1], not l[0], str(l[2])))

    def ren(t):
        if is_var(t):
            if t not in names:
                names[t] = "xyzuvw"[len(names)] if len(names) < 6 else f"v{len(names)}"
            return names[t]
        if isinstance(t, tuple):
            return (t[0], tuple(ren(a) for a in t[1]))
        return t
    for s, p, args in order:
        out.append((s, p, tuple(ren(a) for a in args)))
    return frozenset(out)


def resolvents(c1, c2, k: int):
    """Every binary resolvent of two clauses, with the unifier used."""
    a = _rename(c1, 2 * k)
    b = _rename(c2, 2 * k + 1)
    out = []
    key = lambda l: (l[1], not l[0], str(l[2]))  # noqa: E731  a fixed order: the same run in every process
    for l1 in sorted(a, key=key):
        for l2 in sorted(b, key=key):
            if l1[0] != l2[0] and l1[1] == l2[1] and len(l1[2]) == len(l2[2]):
                s = unify(list(l1[2]), list(l2[2]), {})
                if s is None:
                    continue
                rest = [l for l in a if l != l1] + [l for l in b if l != l2]
                new = frozenset((sg, p, tuple(substitute(t, s) for t in args)) for sg, p, args in rest)
                if any((not sg, p, args) in new for sg, p, args in new):
                    continue  # a tautology: useless
                out.append((_clean(new), {v: show_term(substitute(t, s)) for v, t in s.items()}))
    return out


def refute(kb, negated_goal, strategy="saturate", max_clauses=20000):
    """Resolution refutation. ``strategy``: 'saturate' resolves every pair, level by level; 'support' (Wos,
    Robinson & Carson 1965, the set of support) only resolves pairs with at least one clause descended from the
    negated goal. Returns a record of every clause made (text, parents, level, unifier) and whether □ was found."""
    clauses = [_clean(c) for c in kb] + [_clean(c) for c in negated_goal]
    info = [{"text": show_clause(c), "parents": None, "level": 0, "goal": i >= len(kb), "sub": {}}
            for i, c in enumerate(clauses)]
    index = {c: i for i, c in enumerate(clauses)}
    support = {i for i in range(len(clauses)) if info[i]["goal"]}
    level, new_from = 0, 0
    tried = set()
    while len(clauses) < max_clauses:
        level += 1
        added = []
        n = len(clauses)
        for i, j in itertools.combinations(range(n), 2):
            if (i, j) in tried:
                continue
            if max(i, j) < new_from:
                continue
            tried.add((i, j))
            if strategy == "support" and i not in support and j not in support:
                continue
            for r, sub in resolvents(clauses[i], clauses[j], len(tried)):
                if r in index:
                    continue
                index[r] = len(clauses) + len(added)
                added.append((r, i, j, sub))
                if not r:
                    break
            if added and not added[-1][0]:
                break
        if not added:
            return {"clauses": info, "found": False, "levels": level}
        new_from = n
        for r, i, j, sub in added:
            k = len(clauses)
            clauses.append(r)
            info.append({"text": show_clause(r), "parents": [i, j], "level": level,
                         "goal": i in support or j in support, "sub": sub})
            if i in support or j in support:
                support.add(k)
            if not r:
                return {"clauses": info, "found": True, "levels": level, "made": len(clauses),
                        "proof": proof_of(info, k)}
    return {"clauses": info, "found": False, "levels": level}


def proof_of(info, k) -> list[int]:
    """The clauses the derivation of clause k actually uses, parents before children."""
    out, stack = [], [k]
    seen = set()
    while stack:
        i = stack.pop()
        if i in seen:
            continue
        seen.add(i)
        out.append(i)
        if info[i]["parents"]:
            stack.extend(info[i]["parents"])
    return sorted(out)
