"""Context-free grammars and their parsers (Part 12).

A :class:`Grammar` is a list of productions ``(lhs, rhs-tuple)``, written in text as ``E -> E + T | T`` (symbols
separated by spaces; ``ε`` or nothing for the empty string; a symbol is a nonterminal if it appears on a left-hand
side).  On top of it:

* :meth:`Grammar.first`, :meth:`Grammar.follow`, :func:`ll1_table` (with its conflicts) and :func:`ll1_parse`;
* LR: :func:`lr0_automaton`, :func:`slr_table`, :func:`lr1_automaton`, :func:`lalr_automaton`, :func:`lr_table`
  and :func:`lr_parse` with a shift/reduce trace (Knuth 1965; DeRemer 1969, 1971);
* general parsing: :func:`to_cnf` and :func:`cyk` (which also counts parse trees, to exhibit ambiguity), and
  :func:`earley` (1970), which handles every CFG, ambiguous or left-recursive.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

EPS = "ε"
END = "$"


@dataclass
class Grammar:
    prods: list                         # [(lhs, (sym, ...))]
    start: str = ""
    nonterms: list = field(default_factory=list)

    def __post_init__(self):
        if not self.start:
            self.start = self.prods[0][0]
        seen = []
        for a, _ in self.prods:
            if a not in seen:
                seen.append(a)
        self.nonterms = seen

    @classmethod
    def parse(cls, text: str, start: str = "") -> "Grammar":
        prods = []
        for line in text.strip().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            lhs, rhs = line.split("->", 1)
            for alt in (" " + rhs + " ").split(" | "):
                syms = tuple(s for s in alt.split() if s != EPS)
                prods.append((lhs.strip(), syms))
        return cls(prods, start)

    @property
    def terms(self) -> list:
        out = []
        for _, r in self.prods:
            for s in r:
                if s not in self.nonterms and s not in out:
                    out.append(s)
        return out

    def is_nt(self, s: str) -> bool:
        return s in self.nonterms

    def alts(self, a: str) -> list:
        return [r for l, r in self.prods if l == a]

    def augmented(self) -> "Grammar":
        s = self.start + "'"
        return Grammar([(s, (self.start,))] + list(self.prods), s)

    # --- FIRST and FOLLOW -------------------------------------------------
    def nullable(self) -> set:
        nul = set()
        changed = True
        while changed:
            changed = False
            for a, r in self.prods:
                if a not in nul and all(s in nul for s in r):
                    nul.add(a)
                    changed = True
        return nul

    def first(self) -> dict:
        nul = self.nullable()
        F = {a: set() for a in self.nonterms}
        changed = True
        while changed:
            changed = False
            for a, r in self.prods:
                before = len(F[a])
                for s in r:
                    if self.is_nt(s):
                        F[a] |= F[s]
                        if s not in nul:
                            break
                    else:
                        F[a].add(s)
                        break
                changed |= len(F[a]) != before
        return F

    def first_of(self, seq, F=None, nul=None) -> tuple[set, bool]:
        F = F if F is not None else self.first()
        nul = nul if nul is not None else self.nullable()
        out = set()
        for s in seq:
            if self.is_nt(s):
                out |= F[s]
                if s not in nul:
                    return out, False
            else:
                out.add(s)
                return out, False
        return out, True

    def follow(self) -> dict:
        F, nul = self.first(), self.nullable()
        W = {a: set() for a in self.nonterms}
        W[self.start].add(END)
        changed = True
        while changed:
            changed = False
            for a, r in self.prods:
                for i, s in enumerate(r):
                    if not self.is_nt(s):
                        continue
                    before = len(W[s])
                    f, all_nul = self.first_of(r[i + 1:], F, nul)
                    W[s] |= f
                    if all_nul:
                        W[s] |= W[a]
                    changed |= len(W[s]) != before
        return W


def show_prod(p) -> str:
    a, r = p
    return f"{a} → {' '.join(r) if r else EPS}"


# ---------------------------------------------------------------------------
# LL(1)
# ---------------------------------------------------------------------------
def ll1_table(g: Grammar):
    """table[A][t] = list of production indices (more than one is a conflict)."""
    F, nul, W = g.first(), g.nullable(), g.follow()
    table = {a: defaultdict(list) for a in g.nonterms}
    for i, (a, r) in enumerate(g.prods):
        f, all_nul = g.first_of(r, F, nul)
        for t in f:
            table[a][t].append(i)
        if all_nul:
            for t in W[a]:
                table[a][t].append(i)
    conflicts = [(a, t, ps) for a in table for t, ps in table[a].items() if len(ps) > 1]
    return table, conflicts


def ll1_parse(g: Grammar, tokens, trace: bool = False):
    table, conflicts = ll1_table(g)
    if conflicts:
        raise ValueError(f"not LL(1): {conflicts[0]}")
    toks = list(tokens) + [END]
    stack = [END, g.start]
    i = 0
    steps = []
    tree_stack = []
    while stack:
        top = stack.pop()
        t = toks[i]
        if trace:
            steps.append((list(stack) + [top], toks[i:], ""))
        if top == END:
            ok = t == END
            return (ok, steps) if trace else ok
        if g.is_nt(top):
            ps = table[top].get(t, [])
            if not ps:
                return (False, steps) if trace else False
            a, r = g.prods[ps[0]]
            if trace:
                steps[-1] = (steps[-1][0], steps[-1][1], show_prod(g.prods[ps[0]]))
            stack.extend(reversed(r))
        else:
            if top != t:
                return (False, steps) if trace else False
            if trace:
                steps[-1] = (steps[-1][0], steps[-1][1], f"match {t}")
            i += 1
    return (False, steps) if trace else False


def remove_left_recursion(g: Grammar) -> Grammar:
    """Immediate left recursion  A → A α | β   becomes   A → β A',  A' → α A' | ε."""
    prods = []
    for a in g.nonterms:
        rec = [r[1:] for r in g.alts(a) if r and r[0] == a]
        non = [r for r in g.alts(a) if not r or r[0] != a]
        if not rec:
            prods += [(a, r) for r in non]
            continue
        a2 = a + "'"
        prods += [(a, tuple(r) + (a2,)) for r in non]
        prods += [(a2, tuple(r) + (a2,)) for r in rec] + [(a2, ())]
    return Grammar(prods, g.start)


# ---------------------------------------------------------------------------
# LR
# ---------------------------------------------------------------------------
def _closure0(g: Grammar, items):
    items = set(items)
    stack = list(items)
    while stack:
        p, d = stack.pop()
        r = g.prods[p][1]
        if d < len(r) and g.is_nt(r[d]):
            for q, (a, _) in enumerate(g.prods):
                if a == r[d] and (q, 0) not in items:
                    items.add((q, 0))
                    stack.append((q, 0))
    return frozenset(items)


def _automaton(g: Grammar, start_items, closure, goto_key):
    states = [closure(start_items)]
    index = {states[0]: 0}
    trans = {}
    k = 0
    while k < len(states):
        I = states[k]
        syms = []
        for it in I:
            p, d = it[0], it[1]
            r = g.prods[p][1]
            if d < len(r) and r[d] not in syms:
                syms.append(r[d])
        for X in syms:
            J = closure(goto_key(I, X))
            if J not in index:
                index[J] = len(states)
                states.append(J)
            trans[(k, X)] = index[J]
        k += 1
    return states, trans


def lr0_automaton(g: Grammar):
    """g must be augmented (production 0 is  S' → S)."""
    def goto(I, X):
        return {(p, d + 1) for (p, d) in I if d < len(g.prods[p][1]) and g.prods[p][1][d] == X}
    return _automaton(g, {(0, 0)}, lambda its: _closure0(g, its), goto)


def _closure1(g: Grammar, items, F, nul):
    items = set(items)
    stack = list(items)
    while stack:
        p, d, la = stack.pop()
        r = g.prods[p][1]
        if d < len(r) and g.is_nt(r[d]):
            f, all_nul = g.first_of(r[d + 1:], F, nul)
            las = set(f) | ({la} if all_nul else set())
            for q, (a, _) in enumerate(g.prods):
                if a == r[d]:
                    for b in las:
                        if (q, 0, b) not in items:
                            items.add((q, 0, b))
                            stack.append((q, 0, b))
    return frozenset(items)


def lr1_automaton(g: Grammar):
    F, nul = g.first(), g.nullable()

    def goto(I, X):
        return {(p, d + 1, la) for (p, d, la) in I if d < len(g.prods[p][1]) and g.prods[p][1][d] == X}
    return _automaton(g, {(0, 0, END)}, lambda its: _closure1(g, its, F, nul), goto)


def lalr_automaton(g: Grammar):
    """Merge LR(1) states with the same core (DeRemer's LALR(1), as yacc builds it)."""
    states, trans = lr1_automaton(g)
    core = lambda I: frozenset((p, d) for (p, d, _) in I)
    cores = []
    which = []
    for I in states:
        c = core(I)
        if c not in cores:
            cores.append(c)
        which.append(cores.index(c))
    merged = [set() for _ in cores]
    for I, w in zip(states, which):
        merged[w] |= I
    t2 = {(which[s], X): which[t] for (s, X), t in trans.items()}
    return [frozenset(m) for m in merged], t2


def lr_table(g: Grammar, states, trans, kind: str):
    """ACTION and GOTO.  kind: 'lr0', 'slr' (reduce on FOLLOW), or 'lr1' (reduce on the item's lookahead, for both
    canonical LR(1) and LALR states).  Returns (action, goto, conflicts)."""
    W = g.follow() if kind == "slr" else None
    action = [defaultdict(set) for _ in states]
    goto = [dict() for _ in states]
    for (s, X), t in trans.items():
        if g.is_nt(X):
            goto[s][X] = t
        else:
            action[s][X].add(("s", t))
    terms = g.terms + [END]
    for s, I in enumerate(states):
        for it in I:
            p, d = it[0], it[1]
            r = g.prods[p][1]
            if d == len(r):
                if p == 0:
                    action[s][END].add(("acc", 0))
                    continue
                if kind == "lr0":
                    las = terms
                elif kind == "slr":
                    las = W[g.prods[p][0]]
                else:
                    las = [it[2]]
                for t in las:
                    action[s][t].add(("r", p))
    conflicts = []
    for s, row in enumerate(action):
        for t, acts in row.items():
            if len(acts) > 1:
                kinds = sorted(a[0] for a in acts)
                conflicts.append((s, t, "shift/reduce" if "s" in kinds else "reduce/reduce", sorted(acts)))
    return action, goto, conflicts


def lr_parse(g: Grammar, action, goto, tokens, trace: bool = False, prefer_shift: bool = False):
    """The LR driver: a stack of states; shift, reduce by a production, or accept.  With ``prefer_shift`` a
    shift/reduce conflict is resolved as yacc does (shift: the dangling else binds to the nearest if)."""
    toks = list(tokens) + [END]
    stack = [0]
    syms = []
    trees = []
    i = 0
    steps = []
    while True:
        s, t = stack[-1], toks[i]
        acts = action[s].get(t, set())
        if not acts:
            return (False, steps, None) if trace else False
        if len(acts) > 1:
            shifts = [a for a in acts if a[0] == "s"]
            if not (prefer_shift and shifts):
                raise ValueError(f"conflict in state {s} on {t}: {sorted(acts)}")
            act = shifts[0]
        else:
            act = next(iter(acts))
        if trace:
            steps.append((list(stack), list(syms), toks[i:], act))
        if act[0] == "s":
            stack.append(act[1])
            syms.append(t)
            trees.append(t)
            i += 1
        elif act[0] == "r":
            a, r = g.prods[act[1]]
            n = len(r)
            kids = trees[len(trees) - n:] if n else []
            if n:
                del stack[-n:], syms[-n:], trees[-n:]
            stack.append(goto[stack[-1]][a])
            syms.append(a)
            trees.append((a, kids))
        else:
            return (True, steps, trees[-1]) if trace else True


# ---------------------------------------------------------------------------
# CYK and Earley
# ---------------------------------------------------------------------------
def to_cnf(g: Grammar) -> Grammar:
    """Chomsky normal form: A → B C or A → a (and S → ε if needed), via START, TERM, BIN, DEL, UNIT."""
    prods = [(a, tuple(r)) for a, r in g.prods]
    start = g.start + "₀"
    prods = [(start, (g.start,))] + prods
    nts = {a for a, _ in prods}
    # TERM: terminals inside long right-hand sides get their own nonterminal
    tname = {}
    out = []
    for a, r in prods:
        if len(r) >= 2:
            nr = []
            for s in r:
                if s not in nts:
                    if s not in tname:
                        tname[s] = f"T_{s}"
                    nr.append(tname[s])
                else:
                    nr.append(s)
            out.append((a, tuple(nr)))
        else:
            out.append((a, r))
    out += [(n, (s,)) for s, n in tname.items()]
    nts |= set(tname.values())
    # BIN: split long right-hand sides
    prods, k = [], 0
    for a, r in out:
        while len(r) > 2:
            k += 1
            n = f"{a}_{k}"
            prods.append((a, (r[0], n)))
            nts.add(n)
            a, r = n, r[1:]
        prods.append((a, r))
    # DEL: remove ε-productions
    nul = set()
    changed = True
    while changed:
        changed = False
        for a, r in prods:
            if a not in nul and all(s in nul for s in r):
                nul.add(a)
                changed = True
    new = set()
    for a, r in prods:
        opts = [[]]
        for s in r:
            opts = [o + [s] for o in opts] + ([list(o) for o in opts] if s in nul else [])
        for o in opts:
            if o or a == start:
                new.add((a, tuple(o)))
    prods = sorted(new, key=lambda p: (p[0] != start, p))
    # UNIT: remove A → B
    unit = {a: {a} for a in nts}
    changed = True
    while changed:
        changed = False
        for a, r in prods:
            if len(r) == 1 and r[0] in nts:
                for x in list(unit):
                    if a in unit[x] and r[0] not in unit[x]:
                        unit[x].add(r[0])
                        changed = True
    final = set()
    for x in nts:
        for b in unit[x]:
            for a, r in prods:
                if a == b and not (len(r) == 1 and r[0] in nts):
                    final.add((x, r))
    final = sorted(final, key=lambda p: (p[0] != start, p))
    used = {start}
    changed = True
    while changed:
        changed = False
        for a, r in final:
            if a in used:
                for s in r:
                    if s in nts and s not in used:
                        used.add(s)
                        changed = True
    return Grammar([p for p in final if p[0] in used], start)


def cyk(g: Grammar, tokens, count: bool = True):
    """g in CNF.  table[i][l] maps each nonterminal deriving tokens[i:i+l] to its number of parse trees (big
    integers: the counts show ambiguity growing like the Catalan numbers).  Returns (table, trees for start)."""
    n = len(tokens)
    T = [[defaultdict(int) for _ in range(n + 1)] for _ in range(n)]
    unary = defaultdict(list)
    binary = []
    for a, r in g.prods:
        if len(r) == 1:
            unary[r[0]].append(a)
        elif len(r) == 2:
            binary.append((a, r[0], r[1]))
    for i, t in enumerate(tokens):
        for a in unary[t]:
            T[i][1][a] += 1
    for l in range(2, n + 1):
        for i in range(n - l + 1):
            cell = T[i][l]
            for k in range(1, l):
                L, Rr = T[i][k], T[i + k][l - k]
                if not L or not Rr:
                    continue
                for a, b, c in binary:
                    if b in L and c in Rr:
                        cell[a] += L[b] * Rr[c] if count else 1
    trees = T[0][n].get(g.start, 0) if n else int(any(r == () for a, r in g.prods if a == g.start))
    return T, trees


def earley(g: Grammar, tokens):
    """Earley's recognizer.  Items are (production, dot, origin).  Returns (accepted, chart) where chart[k] is
    the list of items in set k, in the order added."""
    gg = g.augmented()
    n = len(tokens)
    chart = [[] for _ in range(n + 1)]
    sets = [set() for _ in range(n + 1)]

    def add(k, it):
        if it not in sets[k]:
            sets[k].add(it)
            chart[k].append(it)

    add(0, (0, 0, 0))
    nul = gg.nullable()
    for k in range(n + 1):
        j = 0
        while j < len(chart[k]):
            p, d, o = chart[k][j]
            j += 1
            r = gg.prods[p][1]
            if d < len(r):
                X = r[d]
                if gg.is_nt(X):                                   # predict
                    for q, (a, _) in enumerate(gg.prods):
                        if a == X:
                            add(k, (q, 0, k))
                    if X in nul:                                  # Aycock–Horspool fix for nullable symbols
                        add(k, (p, d + 1, o))
                elif k < n and tokens[k] == X:                    # scan
                    add(k + 1, (p, d + 1, o))
            else:                                                 # complete
                a = gg.prods[p][0]
                for (q, e, oo) in list(chart[o]):
                    rq = gg.prods[q][1]
                    if e < len(rq) and rq[e] == a:
                        add(k, (q, e + 1, oo))
    return (0, 1, 0) in sets[n], chart, gg
