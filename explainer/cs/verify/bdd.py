"""Reduced ordered binary decision diagrams (Bryant 1986) and symbolic model checking (Part 54, chapter 7).

    B = BDD(4)                              # variables 0..3, ordered by index
    f = B.apply("and", B.var(0), B.apply("or", B.var(1), B.nvar(2)))
    B.satcount(f), B.size(f), B.exists(f, [1]), B.restrict(f, 0, True)

A node is (variable, low child, high child); the **unique table** guarantees that no two nodes have the same triple
and no node has equal children, so equal Boolean functions are the same node (canonicity: equivalence is a pointer
comparison).  ``apply`` is Bryant's recursive Shannon expansion with a memo table, ``ite`` the if-then-else every
connective reduces to (Brace, Rudell and Bryant 1990), ``and_exists`` the relational product ∃v. f ∧ g that image
computation is built on (Burch, Clarke, McMillan, Dill and Hwang, "Symbolic model checking: 10^20 states and
beyond", 1990).

Symbolic reachability: the dining philosophers of :mod:`explainer.cs.verify.models`, with two bits per philosopher
(holds its first fork, holds its second), current and next copies of every bit interleaved in the order; the
transition relation is one partition per command, T_a(x, x') = guard ∧ effect ∧ frame; the image of a set S is
∃x. S(x) ∧ T_a(x, x'), renamed back to x, and reachability iterates images to a fixpoint (breadth first).  The
counts must equal the explicit-state counts where both run.

Bounded model checking (Biere, Cimatti, Clarke and Zhu 1999): unroll the transition relation k steps into CNF,
ask "is a deadlock reachable in exactly k steps?" of Part 26's CDCL solver, and increase k.
"""

from __future__ import annotations

import sys
import time

sys.setrecursionlimit(max(sys.getrecursionlimit(), 20000))

OPS = {
    "and": lambda a, b: a and b, "or": lambda a, b: a or b, "xor": lambda a, b: a != b,
    "iff": lambda a, b: a == b, "imp": lambda a, b: (not a) or b, "nand": lambda a, b: not (a and b),
    "nor": lambda a, b: not (a or b), "diff": lambda a, b: a and not b,
}


class BDD:
    """A shared ROBDD manager over variables 0..nvars-1, ordered by index (0 at the root)."""

    def __init__(self, nvars: int, names=None):
        self.nvars = nvars
        self.names = list(names) if names is not None else [f"x{i}" for i in range(nvars)]
        self.v = [nvars, nvars]          # node -> variable (terminals sit below every variable)
        self.lo = [0, 1]
        self.hi = [0, 1]
        self.unique: dict = {}
        self.memo: dict = {}

    FALSE, TRUE = 0, 1

    # ---- construction
    def mk(self, v: int, lo: int, hi: int) -> int:
        if lo == hi:
            return lo
        k = (v, lo, hi)
        u = self.unique.get(k)
        if u is None:
            u = len(self.v)
            self.v.append(v)
            self.lo.append(lo)
            self.hi.append(hi)
            self.unique[k] = u
        return u

    def var(self, i: int) -> int:
        return self.mk(i, 0, 1)

    def nvar(self, i: int) -> int:
        return self.mk(i, 1, 0)

    def lit(self, i: int, val: bool) -> int:
        return self.var(i) if val else self.nvar(i)

    # ---- operations
    def apply(self, op: str, u: int, w: int) -> int:
        """Bryant's apply: the BDD of u <op> w."""
        f = OPS[op]
        memo = self.memo

        def go(a, b):
            if a <= 1 and b <= 1:
                return int(f(bool(a), bool(b)))
            if op == "and":
                if a == 0 or b == 0:
                    return 0
                if a == 1:
                    return b
                if b == 1 or a == b:
                    return a
            elif op == "or":
                if a == 1 or b == 1:
                    return 1
                if a == 0:
                    return b
                if b == 0 or a == b:
                    return a
            k = (op, a, b)
            r = memo.get(k)
            if r is not None:
                return r
            va, vb = self.v[a], self.v[b]
            v = min(va, vb)
            a0, a1 = (self.lo[a], self.hi[a]) if va == v else (a, a)
            b0, b1 = (self.lo[b], self.hi[b]) if vb == v else (b, b)
            r = self.mk(v, go(a0, b0), go(a1, b1))
            memo[k] = r
            return r
        return go(u, w)

    def neg(self, u: int) -> int:
        return self.apply("xor", u, 1)

    def conj(self, us) -> int:
        r = 1
        for u in us:
            r = self.apply("and", r, u)
        return r

    def disj(self, us) -> int:
        r = 0
        for u in us:
            r = self.apply("or", r, u)
        return r

    def ite(self, f: int, g: int, h: int) -> int:
        """if f then g else h, by the standard triple recursion."""
        memo = self.memo

        def go(f, g, h):
            if f == 1:
                return g
            if f == 0:
                return h
            if g == h:
                return g
            if g == 1 and h == 0:
                return f
            k = ("ite", f, g, h)
            r = memo.get(k)
            if r is not None:
                return r
            v = min(self.v[f], self.v[g], self.v[h])

            def cof(x, b):
                if self.v[x] != v:
                    return x
                return self.hi[x] if b else self.lo[x]
            r = self.mk(v, go(cof(f, 0), cof(g, 0), cof(h, 0)), go(cof(f, 1), cof(g, 1), cof(h, 1)))
            memo[k] = r
            return r
        return go(f, g, h)

    def restrict(self, u: int, var: int, val: bool) -> int:
        """u with variable ``var`` fixed to ``val`` (the cofactor)."""
        memo = {}

        def go(a):
            if a <= 1 or self.v[a] > var:
                return a
            if a in memo:
                return memo[a]
            if self.v[a] == var:
                r = self.hi[a] if val else self.lo[a]
            else:
                r = self.mk(self.v[a], go(self.lo[a]), go(self.hi[a]))
            memo[a] = r
            return r
        return go(u)

    def exists(self, u: int, vars_) -> int:
        """∃ vars_. u."""
        vs = frozenset(vars_)
        memo = {}

        def go(a):
            if a <= 1:
                return a
            if a in memo:
                return memo[a]
            lo, hi = go(self.lo[a]), go(self.hi[a])
            r = self.apply("or", lo, hi) if self.v[a] in vs else self.mk(self.v[a], lo, hi)
            memo[a] = r
            return r
        return go(u)

    def forall(self, u: int, vars_) -> int:
        return self.neg(self.exists(self.neg(u), vars_))

    def and_exists(self, u: int, w: int, vars_) -> int:
        """The relational product ∃ vars_. (u ∧ w), without building u ∧ w first."""
        vs = frozenset(vars_)
        memo = {}

        def go(a, b):
            if a == 0 or b == 0:
                return 0
            if a == 1 and b == 1:
                return 1
            k = (a, b) if a <= b else (b, a)
            r = memo.get(k)
            if r is not None:
                return r
            va, vb = self.v[a], self.v[b]
            v = min(va, vb)
            a0, a1 = (self.lo[a], self.hi[a]) if va == v else (a, a)
            b0, b1 = (self.lo[b], self.hi[b]) if vb == v else (b, b)
            if v in vs:
                r0 = go(a0, b0)
                r = 1 if r0 == 1 else self.apply("or", r0, go(a1, b1))
            else:
                r = self.mk(v, go(a0, b0), go(a1, b1))
            memo[k] = r
            return r
        return go(u, w)

    def rename(self, u: int, mapping: dict) -> int:
        """Substitute variables by others; the mapping must preserve the order on u's support (it does for
        next -> current state when each next bit sits just below its current bit)."""
        memo = {}

        def go(a):
            if a <= 1:
                return a
            if a in memo:
                return memo[a]
            r = self.mk(mapping.get(self.v[a], self.v[a]), go(self.lo[a]), go(self.hi[a]))
            memo[a] = r
            return r
        return go(u)

    # ---- inspection
    def nodes(self, u: int) -> set:
        seen, work = set(), [u]
        while work:
            a = work.pop()
            if a <= 1 or a in seen:
                continue
            seen.add(a)
            work += [self.lo[a], self.hi[a]]
        return seen

    def size(self, u: int) -> int:
        """Internal (non-terminal) nodes of u."""
        return len(self.nodes(u))

    def support(self, u: int) -> set:
        return {self.v[a] for a in self.nodes(u)}

    def satcount(self, u: int, vars_=None) -> int:
        """Satisfying assignments of u over ``vars_`` (default: all variables), which must include u's support."""
        vs = sorted(range(self.nvars) if vars_ is None else vars_)
        pos = {v: k for k, v in enumerate(vs)}
        m = len(vs)
        if not self.support(u) <= set(vs):
            raise ValueError("support outside the counted variables")
        memo = {}

        def p(a):
            return m if a <= 1 else pos[self.v[a]]

        def go(a):
            if a <= 1:
                return a
            if a in memo:
                return memo[a]
            r = go(self.lo[a]) << (p(self.lo[a]) - p(a) - 1)
            r += go(self.hi[a]) << (p(self.hi[a]) - p(a) - 1)
            memo[a] = r
            return r
        return go(u) << p(u)

    def evaluate(self, u: int, assign) -> bool:
        while u > 1:
            u = self.hi[u] if assign[self.v[u]] else self.lo[u]
        return bool(u)

    def one_sat(self, u: int) -> dict | None:
        if u == 0:
            return None
        out = {}
        while u > 1:
            if self.lo[u] != 0:
                out[self.v[u]] = False
                u = self.lo[u]
            else:
                out[self.v[u]] = True
                u = self.hi[u]
        return out


# --------------------------------------------------------------------------------------- variable order effect

def equality_bdd(n: int, interleaved: bool) -> tuple[BDD, int]:
    """x1 = y1 ∧ … ∧ xn = yn, with the order x1 y1 x2 y2 … (interleaved) or x1 … xn y1 … yn (separated)."""
    B = BDD(2 * n)
    xs = [2 * i for i in range(n)] if interleaved else list(range(n))
    ys = [2 * i + 1 for i in range(n)] if interleaved else list(range(n, 2 * n))
    f = 1
    for x, y in zip(xs, ys):
        f = B.apply("and", f, B.apply("iff", B.var(x), B.var(y)))
    return B, f


def order_effect(ns=range(1, 13)) -> list[dict]:
    """Node counts (internal nodes) of the equality BDD under both orders, with the closed forms 3n (interleaved:
    one x node and two y nodes per pair) and 3·2^n − 3 (separated: a complete tree on x, then 2^(n−k+1) distinct
    y-suffix checks at the k-th y level)."""
    out = []
    for n in ns:
        Bi, fi = equality_bdd(n, True)
        Bs, fs = equality_bdd(n, False)
        out.append({"n": n, "interleaved": Bi.size(fi), "separated": Bs.size(fs), "interleaved_formula": 3 * n,
                    "separated_formula": 3 * 2 ** n - 3, "models": Bi.satcount(fi)})
    return out


# ------------------------------------------------------------------------------------ symbolic philosophers

def _forks(n, ordered):
    from explainer.cs.verify.models import forks
    return forks(n, ordered)


class SymbolicPhilosophers:
    """Philosopher i has bits h_i (holds its first fork) and e_i (holds its second, i.e. eats).  BDD variables, in
    order: h_0, h_0', e_0, e_0', h_1, h_1', … (current and next interleaved)."""

    def __init__(self, n: int, ordered: bool = False):
        self.n = n
        self.fs = _forks(n, ordered)
        self.B = B = BDD(4 * n)
        self.cur = [4 * i + d for i in range(n) for d in (0, 2)]
        self.nxt = [c + 1 for c in self.cur]
        self.to_cur = {c + 1: c for c in self.cur}
        self.parts = []                              # (action, guard over current, relation T_a(x, x'))
        for i, (a, b) in enumerate(self.fs):
            g1 = B.conj([B.nvar(self.h(i))] + self.free(a))
            g2 = B.conj([B.var(self.h(i)), B.nvar(self.e(i))] + self.free(b))
            g3 = B.var(self.e(i))
            self.parts.append((f"take1_{i}", g1, self.rel(g1, {self.h(i): True})))
            self.parts.append((f"take2_{i}", g2, self.rel(g2, {self.e(i): True})))
            self.parts.append((f"release_{i}", g3, self.rel(g3, {self.h(i): False, self.e(i): False})))
        self.init = B.conj(B.nvar(c) for c in self.cur)

    def h(self, i):
        return 4 * i

    def e(self, i):
        return 4 * i + 2

    def free(self, f):
        """Fork f is free: no philosopher holds it as a first fork (h) or as a second (e)."""
        out = []
        for p, (a, b) in enumerate(self.fs):
            if a == f:
                out.append(self.B.nvar(self.h(p)))
            if b == f:
                out.append(self.B.nvar(self.e(p)))
        return out

    def rel(self, guard, effect: dict) -> int:
        B = self.B
        parts = [guard]
        for c in self.cur:
            if c in effect:
                parts.append(B.lit(c + 1, effect[c]))
            else:
                parts.append(B.apply("iff", B.var(c), B.var(c + 1)))
        return B.conj(parts)

    def image(self, S: int) -> int:
        B = self.B
        out = 0
        for _, _, T in self.parts:
            out = B.apply("or", out, B.rename(B.and_exists(S, T, self.cur), self.to_cur))
        return out

    def reach(self) -> dict:
        """Breadth-first symbolic reachability to the fixpoint."""
        B = self.B
        t0 = time.perf_counter()
        R = frontier = self.init
        layers = [{"step": 0, "states": B.satcount(R, self.cur), "nodes": B.size(R)}]
        while True:
            new = B.apply("diff", self.image(frontier), R)
            if new == 0:
                break
            R = B.apply("or", R, new)
            frontier = new
            layers.append({"step": len(layers), "states": B.satcount(R, self.cur), "nodes": B.size(R),
                           "frontier_nodes": B.size(new)})
        dead = B.apply("and", R, B.conj(B.neg(g) for _, g, _ in self.parts))
        return {"n": self.n, "states": B.satcount(R, self.cur), "nodes": B.size(R), "iterations": len(layers) - 1,
                "relation_nodes": sum(B.size(T) for _, _, T in self.parts),
                "deadlock_states": B.satcount(dead, self.cur), "layers": layers, "manager_nodes": len(B.v),
                "seconds": round(time.perf_counter() - t0, 3), "R": R}


def symbolic_table(ns=range(2, 17), explicit_upto: int = 8) -> list[dict]:
    """Reachable states and BDD sizes of the philosophers for n = 2..16, naive and ordered, with the explicit-state
    count beside them for n ≤ explicit_upto."""
    from explainer.cs.verify import models
    rows = []
    for n in ns:
        for ordered in (False, True):
            r = SymbolicPhilosophers(n, ordered).reach()
            r.pop("R")
            r.pop("layers")
            r["ordered"] = ordered
            if n <= explicit_upto:
                r["explicit"] = models.build(models.philosophers(n, ordered)).n
            rows.append(r)
    return rows


# ------------------------------------------------------------------------------------- bounded model checking

def bmc_cnf(n: int, k: int, ordered: bool = False):
    """CNF for "the philosophers reach a deadlock in exactly k steps": state bits h_i^t, e_i^t for t = 0..k (all
    false at t = 0), one selector per command and step (at least one per step; a selector forces its guard at t,
    its effect at t + 1 and every other bit unchanged), and every guard false at step k.  Returns (variables,
    clauses, info for decoding)."""
    fs = _forks(n, ordered)
    nb = 2 * n

    def x(t, b):                     # bit b: 2i is h_i, 2i + 1 is e_i
        return 1 + t * nb + b
    acts = []                        # (name, guard literals as (bit, value), effect {bit: value})
    for i, (a, b) in enumerate(fs):
        def free(f):
            out = []
            for p, (fa, fb) in enumerate(fs):
                if fa == f:
                    out.append((2 * p, False))
                if fb == f:
                    out.append((2 * p + 1, False))
            return out
        acts.append((f"take1_{i}", [(2 * i, False)] + free(a), {2 * i: True}))
        acts.append((f"take2_{i}", [(2 * i, True), (2 * i + 1, False)] + free(b), {2 * i + 1: True}))
        acts.append((f"release_{i}", [(2 * i + 1, True)], {2 * i: False, 2 * i + 1: False}))
    A = len(acts)
    base = (k + 1) * nb

    def sel(t, j):
        return base + 1 + t * A + j
    nvars = base + k * A
    cls = [[-x(0, b)] for b in range(nb)]
    for t in range(k):
        cls.append([sel(t, j) for j in range(A)])
        for j, (_, guard, eff) in enumerate(acts):
            s = sel(t, j)
            for b, val in guard:
                cls.append([-s, x(t, b) if val else -x(t, b)])
            for b in range(nb):
                if b in eff:
                    cls.append([-s, x(t + 1, b) if eff[b] else -x(t + 1, b)])
                else:
                    cls.append([-s, -x(t, b), x(t + 1, b)])
                    cls.append([-s, x(t, b), -x(t + 1, b)])
    for _, guard, _ in acts:
        cls.append([(-x(k, b) if val else x(k, b)) for b, val in guard])
    return nvars, cls, {"x": x, "sel": sel, "acts": [a[0] for a in acts], "nb": nb}


def decode(model, k: int, info: dict, n: int) -> dict:
    states = []
    for t in range(k + 1):
        st = []
        for i in range(n):
            h, e = model[info["x"](t, 2 * i)], model[info["x"](t, 2 * i + 1)]
            st.append(2 if e else 1 if h else 0)
        states.append(st)
    acts = [next(a for j, a in enumerate(info["acts"]) if model[info["sel"](t, j)]) for t in range(k)]
    return {"states": states, "actions": acts}


def bmc(n: int, ordered: bool = False, kmax: int | None = None) -> dict:
    """Increase k from 0 until the deadlock is found (or kmax, default n + 2, is passed); each k is one call to
    Part 26's ``cdcl``.  For a bound at least the reachability diameter a run of UNSATs is a proof (every
    reachable state has a shortest path no longer than the diameter)."""
    from explainer.cs.algo.complexity import cdcl, check
    kmax = n + 2 if kmax is None else kmax
    rows = []
    found = None
    for k in range(kmax + 1):
        t0 = time.perf_counter()
        nv, cls, info = bmc_cnf(n, k, ordered)
        model, st = cdcl(nv, cls)
        row = {"k": k, "vars": nv, "clauses": len(cls), "sat": model is not None, "conflicts": st["conflicts"],
               "decisions": st["decisions"], "seconds": round(time.perf_counter() - t0, 3)}
        rows.append(row)
        if model is not None:
            assert check(model, cls)
            found = {"k": k, **decode(model, k, info, n)}
            break
    return {"n": n, "ordered": ordered, "rows": rows, "found": found, "kmax": kmax}


def all_results() -> dict:
    # n = 8 is left out: refuting k = 7 (a counting argument, which resolution is bad at) took 143 s here
    return {"order": order_effect(), "symbolic": symbolic_table(), "bmc": [bmc(n) for n in range(2, 8)],
            "bmc_ordered": [bmc(n, ordered=True) for n in (3, 5)]}
