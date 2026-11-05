"""Finite automata (Part 12): the subset construction, minimization, state elimination, and the classic examples.

A :class:`DFA` has states 0..n-1, an explicit alphabet, a total transition table ``delta[s][a]`` and a set of
accepting states.  :func:`subset` turns an NFA from :mod:`regex` into a DFA (Rabin and Scott 1959), :func:`minimize`
merges indistinguishable states (Moore's partition refinement; Hopcroft's n log n refinement gives the same result),
and :func:`to_regex` goes back by eliminating states (Kleene's theorem, the McNaughton–Yamada / Brzozowski–McCluskey
route).  :func:`nth_from_end` builds the language whose DFA must have 2ⁿ states.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from explainer.cs.lang import regex as R


@dataclass
class DFA:
    alphabet: list
    delta: list                 # delta[s] = {symbol: state}
    start: int
    accept: set
    names: list = field(default_factory=list)   # optional: what each state stands for (an NFA set, a class...)

    @property
    def n(self) -> int:
        return len(self.delta)

    def run(self, text, trace=False):
        s = self.start
        seq = [s]
        for c in text:
            s = self.delta[s].get(c)
            if s is None:
                return (False, seq) if trace else False
            seq.append(s)
        return (s in self.accept, seq) if trace else s in self.accept

    def reachable(self) -> "DFA":
        order, seen = [self.start], {self.start}
        k = 0
        while k < len(order):
            s = order[k]
            k += 1
            for a in self.alphabet:
                t = self.delta[s][a]
                if t not in seen:
                    seen.add(t)
                    order.append(t)
        idx = {s: i for i, s in enumerate(order)}
        return DFA(list(self.alphabet), [{a: idx[self.delta[s][a]] for a in self.alphabet} for s in order], 0,
                   {idx[s] for s in order if s in self.accept},
                   [self.names[s] for s in order] if self.names else [])


def subset(nfa: R.NFA, alphabet=None) -> DFA:
    """The subset construction: each DFA state is the set of NFA states the simulation could be in."""
    alphabet = sorted(alphabet if alphabet is not None else nfa.alphabet())
    start = nfa.closure({nfa.start})
    index = {start: 0}
    sets = [start]
    delta = []
    k = 0
    while k < len(sets):
        S = sets[k]
        k += 1
        row = {}
        for a in alphabet:
            T = nfa.step(S, a)
            if T not in index:
                index[T] = len(sets)
                sets.append(T)
            row[a] = index[T]
        delta.append(row)
    return DFA(alphabet, delta, 0, {i for i, S in enumerate(sets) if nfa.accept in S}, sets)


def from_regex(pattern: str, alphabet=None) -> DFA:
    return subset(R.compile(pattern), alphabet)


def minimize(d: DFA, trace: bool = False):
    """Moore's algorithm: start from {accepting, rejecting} and split blocks until every block's states agree on
    which block each symbol leads to.  The result is the unique smallest DFA (Myhill–Nerode)."""
    d = d.reachable()
    block = [1 if s in d.accept else 0 for s in range(d.n)]
    rounds = [list(block)]
    while True:
        sig = [(block[s],) + tuple(block[d.delta[s][a]] for a in d.alphabet) for s in range(d.n)]
        ids = {}
        new = []
        for s in range(d.n):
            if sig[s] not in ids:
                ids[sig[s]] = len(ids)
            new.append(ids[sig[s]])
        if len(set(new)) == len(set(block)):
            block = new
            break
        block = new
        rounds.append(list(block))
    # renumber so that the start state is 0
    order = []
    for s in [d.start] + list(range(d.n)):
        if block[s] not in order:
            order.append(block[s])
    ren = {b: i for i, b in enumerate(order)}
    n = len(order)
    delta = [None] * n
    names = [[] for _ in range(n)]
    for s in range(d.n):
        b = ren[block[s]]
        names[b].append(s)
        if delta[b] is None:
            delta[b] = {a: ren[block[d.delta[s][a]]] for a in d.alphabet}
    m = DFA(list(d.alphabet), delta, 0, {ren[block[s]] for s in d.accept}, names)
    return (m, rounds) if trace else m


def equivalent(a: DFA, b: DFA) -> tuple[bool, str | None]:
    """Breadth-first search of the product automaton for a string accepted by exactly one; None if equivalent."""
    from collections import deque
    alphabet = sorted(set(a.alphabet) | set(b.alphabet))
    seen = {(a.start, b.start): ""}
    q = deque([(a.start, b.start)])
    while q:
        s, t = q.popleft()
        w = seen[(s, t)]
        if (s in a.accept) != (t in b.accept):
            return False, w
        for c in alphabet:
            nxt = (a.delta[s].get(c, -1) if s >= 0 else -1, b.delta[t].get(c, -1) if t >= 0 else -1)
            if nxt not in seen:
                seen[nxt] = w + c
                q.append(nxt)
    return True, None


def complement(d: DFA) -> DFA:
    return DFA(list(d.alphabet), [dict(r) for r in d.delta], d.start, set(range(d.n)) - set(d.accept), d.names)


def product(a: DFA, b: DFA, op=lambda x, y: x and y) -> DFA:
    alphabet = sorted(set(a.alphabet) & set(b.alphabet))
    index = {(a.start, b.start): 0}
    pairs = [(a.start, b.start)]
    delta = []
    k = 0
    while k < len(pairs):
        s, t = pairs[k]
        k += 1
        row = {}
        for c in alphabet:
            p = (a.delta[s][c], b.delta[t][c])
            if p not in index:
                index[p] = len(pairs)
                pairs.append(p)
            row[c] = index[p]
        delta.append(row)
    acc = {i for i, (s, t) in enumerate(pairs) if op(s in a.accept, t in b.accept)}
    return DFA(alphabet, delta, 0, acc, pairs)


# ---------------------------------------------------------------------------
# the classic blow-up and the Myhill–Nerode argument
# ---------------------------------------------------------------------------
def nth_from_end(n: int) -> str:
    """Strings over {0,1} whose n-th symbol from the end is 1: an (n+1)-state NFA, a 2ⁿ-state minimal DFA."""
    return "(0|1)*1" + "(0|1)" * (n - 1)


def distinguishing_suffix(u: str, v: str, n: int) -> str:
    """For two different n-bit strings, a suffix that puts a 1 in the n-th-from-end position of one and a 0 in the
    other: the Myhill–Nerode witness that they need different states."""
    for i in range(n):
        if u[i] != v[i]:
            return "0" * i
    raise ValueError("u == v")


# ---------------------------------------------------------------------------
# DFA to regex by state elimination
# ---------------------------------------------------------------------------
def _u(a, b):
    if a is None:
        return b
    if b is None or a == b:
        return a
    return f"{a}|{b}"


def _paren(x):
    if x is None:
        return None
    if len(x) == 1 or (x.startswith("(") and _balanced_outer(x)):
        return x
    return f"({x})"


def _balanced_outer(x):
    depth = 0
    for i, c in enumerate(x):
        depth += c == "("
        depth -= c == ")"
        if depth == 0 and i < len(x) - 1:
            return False
    return True


def _c(*xs):
    if any(x is None for x in xs):
        return None
    out = "".join(_paren(x) if "|" in x else x for x in xs if x != "")
    return out


def _star(x):
    if x is None or x == "":
        return ""
    return _paren(x) + "*"


def to_regex(d: DFA, order=None, trace: bool = False):
    """Generalized NFA with a new start and accept state; remove the original states one at a time, replacing each
    path p → q → r by p → r labelled  R(p,q) R(q,q)* R(q,r)."""
    S, F = "S", "F"
    states = list(range(d.n))
    R_ = {}
    for s in states:
        for a in d.alphabet:
            t = d.delta[s][a]
            R_[(s, t)] = _u(R_.get((s, t)), a)
    R_[(S, d.start)] = ""
    for f in d.accept:
        R_[(f, F)] = _u(R_.get((f, F)), "")
    steps = []
    for q in (order or states):
        loop = _star(R_.get((q, q)))
        ins = [p for (p, x) in list(R_) if x == q and p != q]
        outs = [r for (x, r) in list(R_) if x == q and r != q]
        for p in ins:
            for r in outs:
                new = _c(R_[(p, q)], loop, R_[(q, r)])
                R_[(p, r)] = _u(R_.get((p, r)), new)
        for k in [k for k in R_ if q in k]:
            del R_[k]
        if trace:
            steps.append((q, dict(R_)))
    out = R_.get((S, F))
    return (out, steps) if trace else out


# ---------------------------------------------------------------------------
# pushdown automata
# ---------------------------------------------------------------------------
@dataclass
class PDA:
    """A nondeterministic pushdown automaton.  ``rules``: (state, input or '', pop or '', next state, push) where
    ``push`` is a string whose first character ends up on top.  Acceptance by final state with the input used up."""
    rules: list
    start: str
    accept: set
    bottom: str = "$"

    def run(self, w: str, max_steps: int = 100_000):
        """Breadth-first search over configurations (state, position, stack).  Returns (accepted, path) where
        path is the list of configurations of one accepting run (or the longest run tried)."""
        from collections import deque
        start = (self.start, 0, self.bottom)
        prev = {start: None}
        q = deque([start])
        steps = 0
        while q:
            cfg = q.popleft()
            steps += 1
            if steps > max_steps:
                break
            s, i, st = cfg
            if s in self.accept and i == len(w):
                path = []
                while cfg is not None:
                    path.append(cfg)
                    cfg = prev[cfg]
                return True, path[::-1]
            for (p, a, b, t, push) in self.rules:
                if p != s:
                    continue
                if a and (i >= len(w) or w[i] != a):
                    continue
                if b and not st.startswith(b):
                    continue
                nst = push + (st[len(b):] if b else st)
                if len(nst) > 2 * len(w) + 3:
                    continue
                nxt = (t, i + (1 if a else 0), nst)
                if nxt not in prev:
                    prev[nxt] = cfg
                    q.append(nxt)
        return False, []


ANBN = PDA([("p", "a", "", "p", "A"), ("p", "", "", "q", ""), ("q", "b", "A", "q", ""), ("q", "", "$", "f", "$")],
           "p", {"f"})
PALINDROMES = PDA([("p", "a", "", "p", "a"), ("p", "b", "", "p", "b"), ("p", "", "", "q", ""),
                   ("p", "a", "", "q", ""), ("p", "b", "", "q", ""),
                   ("q", "a", "a", "q", ""), ("q", "b", "b", "q", ""), ("q", "", "$", "f", "$")], "p", {"f"})
