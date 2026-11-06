"""Logic as resources: intuitionistic linear logic without exponentials (Girard 1987), decided by proof search.

    from explainer.philosophy.reasoner.linear import provable
    provable(["$", "$ -o coffee"], "coffee")                         # True: spend the dollar
    provable(["$", "$ -o coffee", "$ -o tea"], "coffee * tea")      # False: one dollar buys one drink
    provable(["$", "$ -o (coffee & tea)"], "tea")                    # True: the menu lets you choose

Hypotheses are a multiset and each is used exactly once: there is no weakening (A, B ⊢ A fails) and no
contraction (A ⊢ A ⊗ A fails). Connectives: ``A * B`` (⊗, both, together), ``A -o B`` (⊸, spend A to get B),
``A & B`` (&, either, your choice), ``A + B`` (⊕, one of them, not your choice), ``1``. The sequent calculus is
cut-free and every rule shrinks the sequent, so the backward search below terminates; it returns a proof tree.
"""

from __future__ import annotations

import itertools
import re
from functools import lru_cache

_TOK = re.compile(r"\s*(-o|⊸|⊗|\*|&|\+|⊕|\(|\)|1|[A-Za-z$][A-Za-z0-9_$']*)")
_OPS = {"-o": "lolli", "⊸": "lolli", "*": "tensor", "⊗": "tensor", "&": "with", "+": "plus", "⊕": "plus"}
_PREC = {"lolli": 1, "plus": 2, "with": 3, "tensor": 4}


def parse(s: str):
    toks, pos = [], 0
    s = s.strip()
    while pos < len(s):
        m = _TOK.match(s, pos)
        if not m or m.end() == pos:
            raise ValueError(f"cannot parse {s!r} at {pos}")
        toks.append(m.group(1))
        pos = m.end()
        while pos < len(s) and s[pos].isspace():
            pos += 1
    i = 0

    def atom():
        nonlocal i
        t = toks[i]
        i += 1
        if t == "(":
            e = expr(0)
            assert toks[i] == ")", s
            i += 1
            return e
        if t == "1":
            return ("one",)
        return ("atom", t)

    def expr(mp):
        nonlocal i
        left = atom()
        while i < len(toks) and toks[i] in _OPS and _PREC[_OPS[toks[i]]] >= mp:
            op = _OPS[toks[i]]
            i += 1
            right = expr(_PREC[op] if op == "lolli" else _PREC[op] + 1)
            left = (op, left, right)
        return left

    e = expr(0)
    assert i == len(toks), s
    return e


def show(f, tex: bool = False) -> str:
    sym = {"tensor": r"\otimes", "lolli": r"\multimap", "with": r"\mathbin{\&}", "plus": r"\oplus"} if tex else \
        {"tensor": "⊗", "lolli": "⊸", "with": "&", "plus": "⊕"}
    if f[0] == "atom":
        a = f[1]
        return (r"\$" if a == "$" else rf"\mathit{{{a}}}") if tex else a
    if f[0] == "one":
        return "1"
    a, b = (show(x, tex) for x in f[1:])
    a = f"({a})" if f[1][0] not in ("atom", "one") else a
    b = f"({b})" if f[2][0] not in ("atom", "one") and not (f[0] == "lolli" and f[2][0] == "lolli") else b
    return f"{a} {sym[f[0]]} {b}"


def _key(gamma):
    return tuple(sorted(gamma, key=repr))


def _splits(gamma):
    """Every way of dividing a multiset into two parts (as sorted tuples), without duplicates."""
    seen = set()
    n = len(gamma)
    for mask in range(1 << n):
        a = _key([gamma[i] for i in range(n) if mask >> i & 1])
        b = _key([gamma[i] for i in range(n) if not mask >> i & 1])
        if (a, b) not in seen:
            seen.add((a, b))
            yield a, b


@lru_cache(maxsize=None)
def _prove(gamma: tuple, c):
    """A proof of gamma ⊢ c as (rule, sequent, children), or None."""
    seq = (gamma, c)
    if len(gamma) == 1 and gamma[0] == c:
        return ("id", seq, ())
    if c == ("one",) and not gamma:
        return ("1R", seq, ())
    # right rules
    if c[0] == "lolli":
        p = _prove(_key(gamma + (c[1],)), c[2])
        if p:
            return ("⊸R", seq, (p,))
    if c[0] == "with":
        p, q = _prove(gamma, c[1]), _prove(gamma, c[2])
        if p and q:
            return ("&R", seq, (p, q))
    if c[0] == "tensor":
        for a, b in _splits(gamma):
            p = _prove(a, c[1])
            if p:
                q = _prove(b, c[2])
                if q:
                    return ("⊗R", seq, (p, q))
    if c[0] == "plus":
        for side in (1, 2):
            p = _prove(gamma, c[side])
            if p:
                return ("⊕R", seq, (p,))
    # left rules
    for i, h in enumerate(gamma):
        rest = gamma[:i] + gamma[i + 1:]
        if h == ("one",):
            p = _prove(_key(rest), c)
            if p:
                return ("1L", seq, (p,))
        if h[0] == "tensor":
            p = _prove(_key(rest + (h[1], h[2])), c)
            if p:
                return ("⊗L", seq, (p,))
        if h[0] == "with":
            for side in (1, 2):
                p = _prove(_key(rest + (h[side],)), c)
                if p:
                    return ("&L", seq, (p,))
        if h[0] == "plus":
            p, q = _prove(_key(rest + (h[1],)), c), _prove(_key(rest + (h[2],)), c)
            if p and q:
                return ("⊕L", seq, (p, q))
        if h[0] == "lolli":
            for a, b in _splits(rest):
                p = _prove(a, h[1])
                if p:
                    q = _prove(_key(b + (h[2],)), c)
                    if q:
                        return ("⊸L", seq, (p, q))
    return None


def prove(hyps, goal):
    """The proof tree of hyps ⊢ goal, or None."""
    gamma = _key([parse(h) if isinstance(h, str) else h for h in hyps])
    return _prove(gamma, parse(goal) if isinstance(goal, str) else goal)


def provable(hyps, goal) -> bool:
    return prove(hyps, goal) is not None


def size(p) -> int:
    return 1 + sum(size(q) for q in p[2]) if p else 0


def sequent_tex(seq) -> str:
    gamma, c = seq
    return (", ".join(show(h, True) for h in gamma) + r" \vdash " + show(c, True)).strip()
