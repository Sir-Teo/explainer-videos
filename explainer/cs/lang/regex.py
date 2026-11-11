"""Regular expressions, three ways (Part 12).

* :func:`parse` turns a pattern into a small syntax tree: literals, ``.``, classes ``[a-z]``, concatenation,
  alternation ``|``, ``*``, ``+``, ``?`` and groups; ``\\1`` back-references are parsed too, for the backtracker.
* :func:`thompson` builds Thompson's (1968) NFA, one or two states per syntax node, and :class:`NFA` simulates it on
  *sets* of states: linear time in the text, whatever the pattern.
* :func:`backtrack` is the engine of Perl, Python and PCRE in miniature: it tries alternatives one at a time and
  backs up on failure, and counts its steps, so ``(a+)+b`` on ``aaaa...`` shows its exponential blow-up.
* :func:`derivative` and :func:`matches_by_derivatives` are Brzozowski's (1964) derivatives: the regex for "what is
  left to match after reading c", with smart constructors that keep the terms small.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# syntax
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Node:
    pass


@dataclass(frozen=True)
class Empty(Node):          # matches only the empty string (epsilon)
    pass


@dataclass(frozen=True)
class Never(Node):          # matches nothing (the empty language), used by derivatives
    pass


@dataclass(frozen=True)
class Chars(Node):          # one character from a set; ``neg`` for [^...]; ``any`` for '.'
    chars: frozenset
    neg: bool = False
    label: str = ""

    def ok(self, c: str) -> bool:
        return (c not in self.chars) if self.neg else (c in self.chars)


@dataclass(frozen=True)
class Cat(Node):
    a: Node
    b: Node


@dataclass(frozen=True)
class Alt(Node):
    a: Node
    b: Node


@dataclass(frozen=True)
class Star(Node):
    a: Node


@dataclass(frozen=True)
class Group(Node):          # capturing group (only the backtracker records captures)
    a: Node
    index: int


@dataclass(frozen=True)
class Backref(Node):
    index: int


def lit(c: str) -> Chars:
    return Chars(frozenset(c), label=c)


ANY = Chars(frozenset(), neg=True, label=".")


def plus(a: Node) -> Node:
    return Cat(a, Star(a))


def opt(a: Node) -> Node:
    return Alt(a, Empty())


class RegexError(ValueError):
    pass


def parse(pattern: str) -> Node:
    """Recursive descent over the grammar  alt := cat ('|' cat)* ; cat := rep* ; rep := atom ('*'|'+'|'?')* ."""
    pos = 0
    groups = 0

    def peek():
        return pattern[pos] if pos < len(pattern) else None

    def eat(c=None):
        nonlocal pos
        ch = peek()
        if ch is None or (c is not None and ch != c):
            raise RegexError(f"expected {c!r} at {pos} in {pattern!r}")
        pos += 1
        return ch

    def alt():
        n = cat()
        while peek() == "|":
            eat("|")
            n = Alt(n, cat())
        return n

    def cat():
        parts = []
        while peek() is not None and peek() not in "|)":
            parts.append(rep())
        if not parts:
            return Empty()
        n = parts[0]
        for p in parts[1:]:
            n = Cat(n, p)
        return n

    def rep():
        n = atom()
        while peek() is not None and peek() in "*+?":
            op = eat()
            n = Star(n) if op == "*" else (plus(n) if op == "+" else opt(n))
        return n

    def atom():
        nonlocal groups
        ch = peek()
        if ch == "(":
            eat("(")
            groups += 1
            k = groups
            n = alt()
            eat(")")
            return Group(n, k)
        if ch == ".":
            eat()
            return ANY
        if ch == "[":
            eat("[")
            neg = peek() == "^"
            if neg:
                eat()
            cs = set()
            first = True
            while peek() != "]" or first:
                first = False
                a = eat()
                if a == "\\":
                    a = eat()
                    a = {"n": "\n", "t": "\t", "r": "\r"}.get(a, a)
                if peek() == "-" and pos + 1 < len(pattern) and pattern[pos + 1] != "]":
                    eat("-")
                    b = eat()
                    cs.update(chr(x) for x in range(ord(a), ord(b) + 1))
                else:
                    cs.add(a)
            eat("]")
            text = pattern[start_of_class(pattern, pos):pos]
            return Chars(frozenset(cs), neg=neg, label=text)
        if ch == "\\":
            eat()
            c = eat()
            if c.isdigit():
                return Backref(int(c))
            table = {"d": "0123456789", "w": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_",
                     "s": " \t\n\r"}
            if c in table:
                return Chars(frozenset(table[c]), label="\\" + c)
            return Chars(frozenset({"n": "\n", "t": "\t", "r": "\r"}.get(c, c)), label="\\" + c)
        if ch in "*+?":
            raise RegexError(f"nothing to repeat at {pos} in {pattern!r}")
        return lit(eat())

    n = alt()
    if pos != len(pattern):
        raise RegexError(f"unexpected {peek()!r} at {pos} in {pattern!r}")
    return n


def start_of_class(pattern: str, end: int) -> int:
    k = end - 1
    while k > 0 and pattern[k] != "[":
        k -= 1
    return k


def show(n: Node) -> str:
    """Back to a pattern (fully parenthesized where needed)."""
    if isinstance(n, Empty):
        return "ε"
    if isinstance(n, Never):
        return "∅"
    if isinstance(n, Chars):
        return n.label or "[" + "".join(sorted(n.chars)) + "]"
    if isinstance(n, Group):
        return "(" + show(n.a) + ")"
    if isinstance(n, Backref):
        return f"\\{n.index}"
    if isinstance(n, Star):
        s = show(n.a)
        return (s if _atomic(n.a) else "(" + s + ")") + "*"
    if isinstance(n, Cat):
        parts = []
        for x in (n.a, n.b):
            s = show(x)
            parts.append("(" + s + ")" if isinstance(x, Alt) else s)
        return "".join(parts)
    if isinstance(n, Alt):
        return show(n.a) + "|" + show(n.b)
    raise TypeError(n)


def _atomic(n: Node) -> bool:
    return isinstance(n, (Chars, Group, Empty, Never, Backref)) or (isinstance(n, Star))


def size(n: Node) -> int:
    if isinstance(n, (Cat, Alt)):
        return 1 + size(n.a) + size(n.b)
    if isinstance(n, (Star, Group)):
        return 1 + size(n.a)
    return 1


# ---------------------------------------------------------------------------
# Thompson's construction and set-of-states simulation
# ---------------------------------------------------------------------------
@dataclass
class NFA:
    """States 0..n-1; ``eps[s]`` the ε-successors, ``edges[s]`` a list of (Chars, t); one start, one accept."""
    start: int
    accept: int
    eps: list = field(default_factory=list)
    edges: list = field(default_factory=list)

    @property
    def n(self) -> int:
        return len(self.eps)

    def new(self) -> int:
        self.eps.append([])
        self.edges.append([])
        return len(self.eps) - 1

    def closure(self, states) -> frozenset:
        seen = set(states)
        stack = list(states)
        while stack:
            s = stack.pop()
            for t in self.eps[s]:
                if t not in seen:
                    seen.add(t)
                    stack.append(t)
        return frozenset(seen)

    def step(self, states, c: str) -> frozenset:
        return self.closure({t for s in states for (cs, t) in self.edges[s] if cs.ok(c)})

    def run(self, text: str, trace: bool = False):
        """Whole-string match.  Returns (matched, work, trace). Work sums active-set sizes plus one per step; it is a proxy, not every internal operation."""
        cur = self.closure({self.start})
        work = len(cur)
        seq = [cur] if trace else None
        for c in text:
            cur = self.step(cur, c)
            work += len(cur) + 1
            if trace:
                seq.append(cur)
            if not cur:
                break
        return self.accept in cur, work, seq

    def search(self, text: str) -> tuple[bool, int]:
        """Unanchored search (does any substring match?), still one pass: a new thread starts at every position."""
        start = self.closure({self.start})
        cur = start
        work = len(cur)
        if self.accept in cur:
            return True, work
        for c in text:
            cur = self.step(cur, c) | start
            work += len(cur) + 1
            if self.accept in cur:
                return True, work
        return False, work

    def alphabet(self) -> set:
        out = set()
        for es in self.edges:
            for cs, _ in es:
                if not cs.neg:
                    out |= set(cs.chars)
        return out


def thompson(n: Node) -> NFA:
    """Each node becomes a fragment with one entry and one exit, joined by ε-edges, exactly as in Thompson 1968."""
    m = NFA(0, 0)

    def build(x: Node) -> tuple[int, int]:
        if isinstance(x, Chars):
            s, t = m.new(), m.new()
            m.edges[s].append((x, t))
            return s, t
        if isinstance(x, Empty):
            s, t = m.new(), m.new()
            m.eps[s].append(t)
            return s, t
        if isinstance(x, Never):
            return m.new(), m.new()
        if isinstance(x, Group):
            return build(x.a)
        if isinstance(x, Cat):
            s1, t1 = build(x.a)
            s2, t2 = build(x.b)
            m.eps[t1].append(s2)
            return s1, t2
        if isinstance(x, Alt):
            s, t = m.new(), m.new()
            s1, t1 = build(x.a)
            s2, t2 = build(x.b)
            m.eps[s] += [s1, s2]
            m.eps[t1].append(t)
            m.eps[t2].append(t)
            return s, t
        if isinstance(x, Star):
            s, t = m.new(), m.new()
            s1, t1 = build(x.a)
            m.eps[s] += [s1, t]
            m.eps[t1] += [s1, t]
            return s, t
        if isinstance(x, Backref):
            raise RegexError("this Thompson compiler does not support back-references")
        raise TypeError(x)

    m.start, m.accept = build(n)
    return m


def compile(pattern: str) -> NFA:
    return thompson(parse(pattern))


# ---------------------------------------------------------------------------
# backtracking, as Perl, Python, Java and PCRE do it
# ---------------------------------------------------------------------------
class StepLimit(Exception):
    pass


def backtrack(n: Node, text: str, limit: int = 10 ** 8, anchored: bool = True) -> tuple[bool, int]:
    """Match by trying alternatives in order (greedy stars first) and backing up on failure.  Returns (matched,
    steps).  Continuation-passing naive search; production engines may prune these choices with optimizations."""
    steps = 0
    caps: dict[int, tuple[int, int]] = {}

    def m(x: Node, i: int, k) -> bool:
        nonlocal steps
        steps += 1
        if steps > limit:
            raise StepLimit(steps)
        if isinstance(x, Chars):
            return i < len(text) and x.ok(text[i]) and k(i + 1)
        if isinstance(x, Empty):
            return k(i)
        if isinstance(x, Never):
            return False
        if isinstance(x, Cat):
            return m(x.a, i, lambda j: m(x.b, j, k))
        if isinstance(x, Alt):
            return m(x.a, i, k) or m(x.b, i, k)
        if isinstance(x, Star):
            def again(j):
                return j != i and m(x, j, k)        # an empty iteration may not loop forever
            return m(x.a, i, again) or k(i)
        if isinstance(x, Group):
            old = caps.get(x.index)

            def close(j):
                prev = caps.get(x.index)
                caps[x.index] = (i, j)
                if k(j):
                    return True
                if prev is None:
                    caps.pop(x.index, None)
                else:
                    caps[x.index] = prev
                return False
            ok = m(x.a, i, close)
            if not ok and old is not None:
                caps[x.index] = old
            return ok
        if isinstance(x, Backref):
            if x.index not in caps:
                return False
            a, b = caps[x.index]
            s = text[a:b]
            return text.startswith(s, i) and k(i + len(s))
        raise TypeError(x)

    if anchored:
        ok = m(n, 0, lambda j: j == len(text))
        return ok, steps
    for start in range(len(text) + 1):
        if m(n, start, lambda j: True):
            return True, steps
    return False, steps


# ---------------------------------------------------------------------------
# Brzozowski derivatives
# ---------------------------------------------------------------------------
def nullable(n: Node) -> bool:
    if isinstance(n, (Empty, Star)):
        return True
    if isinstance(n, (Chars, Never)):
        return False
    if isinstance(n, Group):
        return nullable(n.a)
    if isinstance(n, Cat):
        return nullable(n.a) and nullable(n.b)
    if isinstance(n, Alt):
        return nullable(n.a) or nullable(n.b)
    raise TypeError(n)


def _cat(a: Node, b: Node) -> Node:
    if isinstance(a, Never) or isinstance(b, Never):
        return Never()
    if isinstance(a, Empty):
        return b
    if isinstance(b, Empty):
        return a
    return Cat(a, b)


def _alts(n: Node) -> list:
    return _alts(n.a) + _alts(n.b) if isinstance(n, Alt) else [n]


def _alt(a: Node, b: Node) -> Node:
    """Alternation up to associativity, commutativity and idempotence (Brzozowski's similarity), so that the set of
    derivatives of any regex is finite."""
    parts = sorted({x for x in _alts(a) + _alts(b) if not isinstance(x, Never)}, key=repr)
    if not parts:
        return Never()
    n = parts[0]
    for x in parts[1:]:
        n = Alt(n, x)
    return n


def derivative(n: Node, c: str) -> Node:
    """∂c(r): the strings w such that c·w is in L(r)."""
    if isinstance(n, (Empty, Never)):
        return Never()
    if isinstance(n, Chars):
        return Empty() if n.ok(c) else Never()
    if isinstance(n, Group):
        return derivative(n.a, c)
    if isinstance(n, Cat):
        d = _cat(derivative(n.a, c), n.b)
        return _alt(d, derivative(n.b, c)) if nullable(n.a) else d
    if isinstance(n, Alt):
        return _alt(derivative(n.a, c), derivative(n.b, c))
    if isinstance(n, Star):
        return _cat(derivative(n.a, c), n)
    raise TypeError(n)


def matches_by_derivatives(n: Node, text: str, trace: bool = False):
    seq = [n]
    for c in text:
        n = derivative(n, c)
        if trace:
            seq.append(n)
        if isinstance(n, Never):
            break
    ok = nullable(n) and len(seq) >= 1
    return (ok, seq) if trace else ok


def brzozowski_dfa(n: Node, alphabet, limit: int = 10_000):
    """Build a DFA whose states are the distinct derivatives of n (Brzozowski 1964): state 0 is n itself, the
    transition on c goes to the derivative by c, and a state accepts if its regex is nullable."""
    states = [n]
    index = {n: 0}
    delta = []
    k = 0
    while k < len(states):
        r = states[k]
        k += 1
        row = {}
        for c in alphabet:
            d = derivative(r, c)
            if d not in index:
                if len(states) >= limit:
                    raise RuntimeError("too many derivatives")
                index[d] = len(states)
                states.append(d)
            row[c] = index[d]
        delta.append(row)
    return states, delta, {i for i, r in enumerate(states) if nullable(r)}
