"""Satisfiability for Part 2: DPLL on random 3-SAT, a small CDCL solver, and circuits turned into clauses.

* :func:`random_3sat`: m clauses of three distinct variables out of n, each negated with probability 1/2
  (the model of Mitchell, Selman & Levesque 1992).
* :func:`dpll`: Davis-Putnam-Logemann-Loveland (1962): unit propagation, and branching on the variable that occurs
  most in the shortest open clauses (a Jeroslow-Wang score), with chronological backtracking. Counts decisions.
* :class:`CDCL`: conflict-driven clause learning (Marques-Silva & Sakallah's GRASP, 1996; Chaff's watched literals
  and VSIDS, 2001): two watched literals, first-UIP learning, activity-based branching, phase saving and Luby
  restarts. Small and plain, in Python; it also records its first conflict for drawing.
* :class:`Circuit`: gates as variables, Tseitin's clauses for each gate, and miters that ask whether two circuits
  ever disagree; adders (ripple-carry and Kogge-Stone) to compare.
"""

from __future__ import annotations

import numpy as np
from numba import njit


def random_3sat(rng, n: int, m: int) -> np.ndarray:
    out = np.empty((m, 3), np.int64)
    for i in range(m):
        v = rng.choice(n, 3, replace=False) + 1
        s = rng.integers(0, 2, 3) * 2 - 1
        out[i] = v * s
    return out


def occurrence_lists(clauses: np.ndarray, n: int):
    """CSR lists of the clauses holding each literal; literal l is slot 2|l| + (l < 0)."""
    m = clauses.shape[0]
    lits = clauses.reshape(-1)
    slot = 2 * np.abs(lits) + (lits < 0)
    order = np.argsort(slot, kind="stable")
    cls = (np.arange(m).repeat(clauses.shape[1]))[order]
    start = np.zeros(2 * n + 3, np.int64)
    np.add.at(start, slot + 1, 1)
    return np.cumsum(start), cls.astype(np.int64)


@njit(cache=True)
def _assign(var, val, value, nsat, nfalse, start, occ, trail, tl):
    value[var] = val
    trail[tl] = var
    tl += 1
    pos_slot = 2 * var  # literal +var
    neg_slot = 2 * var + 1
    true_slot = pos_slot if val == 1 else neg_slot
    false_slot = neg_slot if val == 1 else pos_slot
    for k in range(start[true_slot], start[true_slot + 1]):
        nsat[occ[k]] += 1
    for k in range(start[false_slot], start[false_slot + 1]):
        nfalse[occ[k]] += 1
    return tl


@njit(cache=True)
def _unassign(var, value, nsat, nfalse, start, occ):
    val = value[var]
    pos_slot = 2 * var
    neg_slot = 2 * var + 1
    true_slot = pos_slot if val == 1 else neg_slot
    false_slot = neg_slot if val == 1 else pos_slot
    for k in range(start[true_slot], start[true_slot + 1]):
        nsat[occ[k]] -= 1
    for k in range(start[false_slot], start[false_slot + 1]):
        nfalse[occ[k]] -= 1
    value[var] = -1


@njit(cache=True)
def _propagate(clauses, value, nsat, nfalse, start, occ, trail, tl, qhead):
    """Unit propagation from trail[qhead:]. Returns (conflict?, new trail length)."""
    k = clauses.shape[1]
    while qhead < tl:
        var = trail[qhead]
        qhead += 1
        false_slot = 2 * var + 1 if value[var] == 1 else 2 * var
        for j in range(start[false_slot], start[false_slot + 1]):
            c = occ[j]
            if nsat[c] > 0:
                continue
            if nfalse[c] == k:
                return True, tl
            if nfalse[c] == k - 1:  # unit: find the open literal
                for t in range(k):
                    l = clauses[c, t]
                    v = abs(l)
                    if value[v] == -1:
                        tl = _assign(v, 1 if l > 0 else 0, value, nsat, nfalse, start, occ, trail, tl)
                        break
    return False, tl


@njit(cache=True)
def dpll(clauses, n, start, occ, max_decisions):
    """Returns (status, decisions): status 1 satisfiable, 0 unsatisfiable, -1 gave up."""
    m, k = clauses.shape
    value = np.full(n + 1, -1, np.int64)
    nsat = np.zeros(m, np.int64)
    nfalse = np.zeros(m, np.int64)
    trail = np.empty(n + 1, np.int64)
    lim = np.empty(n + 2, np.int64)
    dvar = np.empty(n + 2, np.int64)
    dval = np.empty(n + 2, np.int64)
    flipped = np.zeros(n + 2, np.bool_)
    tl = 0
    level = 0
    qhead = 0
    decisions = 0
    score = np.zeros(2 * n + 2)
    while True:
        conflict, tl2 = _propagate(clauses, value, nsat, nfalse, start, occ, trail, tl, qhead)
        qhead = tl2
        tl = tl2
        if conflict:
            while True:
                if level == 0:
                    return 0, decisions
                while tl > lim[level]:  # undo this level, its decision included
                    tl -= 1
                    _unassign(trail[tl], value, nsat, nfalse, start, occ)
                if not flipped[level]:
                    flipped[level] = True
                    qhead = tl
                    tl = _assign(dvar[level], 1 - dval[level], value, nsat, nfalse, start, occ, trail, tl)
                    break
                level -= 1
            continue
        # all clauses satisfied?
        done = True
        for c in range(m):
            if nsat[c] == 0:
                done = False
                break
        if done:
            return 1, decisions
        if decisions >= max_decisions:
            return -1, decisions
        # Jeroslow-Wang on the open clauses: 2^-(open literals)
        score[:] = 0.0
        for c in range(m):
            if nsat[c] > 0:
                continue
            w = 2.0 ** (-(k - nfalse[c]))
            for t in range(k):
                l = clauses[c, t]
                v = abs(l)
                if value[v] == -1:
                    score[2 * v + (1 if l < 0 else 0)] += w
        best, bv, bval = -1.0, -1, 1
        for v in range(1, n + 1):
            if value[v] != -1:
                continue
            s = score[2 * v] + score[2 * v + 1]
            if s > best:
                best, bv = s, v
                bval = 1 if score[2 * v] >= score[2 * v + 1] else 0
        decisions += 1
        level += 1
        lim[level] = tl
        dvar[level] = bv
        dval[level] = bval
        flipped[level] = False
        qhead = tl
        tl = _assign(bv, bval, value, nsat, nfalse, start, occ, trail, tl)


def solve_dpll(clauses: np.ndarray, n: int, max_decisions=10**9):
    start, occ = occurrence_lists(clauses, n)
    return dpll(clauses, n, start, occ, max_decisions)


# ---------------------------------------------------------------------------
# CDCL
# ---------------------------------------------------------------------------
def _luby(i: int) -> int:
    k = 1
    while (1 << k) - 1 < i:
        k += 1
    while True:
        if i == (1 << k) - 1:
            return 1 << (k - 1)
        if (1 << (k - 1)) <= i < (1 << k) - 1:
            i = i - (1 << (k - 1)) + 1
            k = 1
            while (1 << k) - 1 < i:
                k += 1
        else:
            k -= 1


class CDCL:
    """Clauses are lists of nonzero ints (DIMACS literals). ``solve()`` returns True/False and fills ``model``;
    ``stats`` counts decisions, conflicts, propagations and learned clauses."""

    def __init__(self, n_vars: int, clauses, restart_base=100, record_first_conflict=False):
        self.n = n_vars
        self.clauses: list[list[int]] = []
        self.watches: dict[int, list[int]] = {l: [] for v in range(1, n_vars + 1) for l in (v, -v)}
        self.value = [0] * (n_vars + 1)  # 0 open, 1 true, -1 false
        self.level = [0] * (n_vars + 1)
        self.reason: list[int | None] = [None] * (n_vars + 1)
        self.trail: list[int] = []
        self.lim: list[int] = []
        self.act = [0.0] * (n_vars + 1)
        self.inc = 1.0
        self.phase = [False] * (n_vars + 1)
        self.qhead = 0
        self.stats = {"decisions": 0, "conflicts": 0, "propagations": 0, "learned": 0}
        self.restart_base = restart_base
        self.record = record_first_conflict
        self.first_conflict = None
        self.unsat = False
        self.units: list[int] = []
        for c in clauses:
            c = sorted(set(c), key=abs)
            if any(-l in c for l in c):
                continue
            if len(c) == 0:
                self.unsat = True
            elif len(c) == 1:
                self.units.append(c[0])
            else:
                self._add(c)

    def _add(self, c) -> int:
        i = len(self.clauses)
        self.clauses.append(list(c))
        self.watches[c[0]].append(i)
        self.watches[c[1]].append(i)
        return i

    def lit_value(self, l: int) -> int:
        v = self.value[abs(l)]
        return v if l > 0 else -v

    def _enqueue(self, l: int, reason) -> None:
        v = abs(l)
        self.value[v] = 1 if l > 0 else -1
        self.level[v] = len(self.lim)
        self.reason[v] = reason
        self.trail.append(l)

    def _propagate(self):
        while self.qhead < len(self.trail):
            l = self.trail[self.qhead]
            self.qhead += 1
            self.stats["propagations"] += 1
            fl = -l
            ws = self.watches[fl]
            i = 0
            while i < len(ws):
                ci = ws[i]
                c = self.clauses[ci]
                if c[0] == fl:
                    c[0], c[1] = c[1], c[0]
                if self.lit_value(c[0]) == 1:
                    i += 1
                    continue
                found = False
                for k in range(2, len(c)):
                    if self.lit_value(c[k]) != -1:
                        c[1], c[k] = c[k], c[1]
                        self.watches[c[1]].append(ci)
                        ws[i] = ws[-1]
                        ws.pop()
                        found = True
                        break
                if found:
                    continue
                if self.lit_value(c[0]) == -1:
                    return ci
                self._enqueue(c[0], ci)
                i += 1
        return None

    def _analyze(self, confl: int):
        """First UIP: resolve the conflict clause with reasons of the current level until one literal of that level
        remains. Returns (learned clause, backjump level)."""
        seen = [False] * (self.n + 1)
        learnt = [0]
        counter = 0
        p = None
        idx = len(self.trail) - 1
        cl = self.clauses[confl]
        cur = len(self.lim)
        steps = []
        while True:
            for q in (cl if p is None else [x for x in cl if x != p]):
                v = abs(q)
                if not seen[v] and self.level[v] > 0:
                    seen[v] = True
                    self.act[v] += self.inc
                    if self.level[v] == cur:
                        counter += 1
                    else:
                        learnt.append(q)
            while not seen[abs(self.trail[idx])]:
                idx -= 1
            p = self.trail[idx]
            idx -= 1
            counter -= 1
            seen[abs(p)] = False
            if counter == 0:
                break
            r = self.reason[abs(p)]
            cl = self.clauses[r]
            steps.append(r)
        learnt[0] = -p
        bt = 0
        if len(learnt) > 1:
            j = max(range(1, len(learnt)), key=lambda i: self.level[abs(learnt[i])])
            learnt[1], learnt[j] = learnt[j], learnt[1]
            bt = self.level[abs(learnt[1])]
        self.inc *= 1.05
        if self.inc > 1e100:
            self.act = [a * 1e-100 for a in self.act]
            self.inc *= 1e-100
        return learnt, bt, steps

    def _backtrack(self, lvl: int):
        if len(self.lim) > lvl:
            for l in self.trail[self.lim[lvl]:][::-1]:
                v = abs(l)
                self.phase[v] = l > 0
                self.value[v] = 0
                self.reason[v] = None
            del self.trail[self.lim[lvl]:]
            del self.lim[lvl:]
            self.qhead = len(self.trail)

    def _decide(self):
        best, bv = -1.0, 0
        for v in range(1, self.n + 1):
            if self.value[v] == 0 and self.act[v] > best:
                best, bv = self.act[v], v
        return bv

    def solve(self, max_conflicts=10**7) -> bool | None:
        if self.unsat:
            return False
        for l in self.units:
            if self.lit_value(l) == -1:
                return False
            if self.lit_value(l) == 0:
                self._enqueue(l, None)
        if self._propagate() is not None:
            return False
        restarts, budget = 1, self.restart_base * _luby(1)
        since = 0
        while True:
            confl = self._propagate()
            if confl is not None:
                self.stats["conflicts"] += 1
                since += 1
                if not self.lim:
                    return False
                if self.record and self.first_conflict is None:
                    self.first_conflict = self._snapshot(confl)
                learnt, bt, _ = self._analyze(confl)
                self._backtrack(bt)
                if len(learnt) == 1:
                    self._enqueue(learnt[0], None)
                else:
                    ci = self._add(learnt)
                    self.stats["learned"] += 1
                    self._enqueue(learnt[0], ci)
                if self.record and self.first_conflict is not None and "learned" not in self.first_conflict:
                    self.first_conflict["learned"] = list(learnt)
                    self.first_conflict["backjump"] = bt
                if self.stats["conflicts"] >= max_conflicts:
                    return None
                continue
            if since >= budget:
                restarts += 1
                budget = self.restart_base * _luby(restarts)
                since = 0
                self._backtrack(0)
                continue
            v = self._decide()
            if v == 0:
                self.model = [self.value[i] == 1 for i in range(self.n + 1)]
                return True
            self.stats["decisions"] += 1
            self.lim.append(len(self.trail))
            self._enqueue(v if self.phase[v] else -v, None)

    def _snapshot(self, confl: int) -> dict:
        """The trail at the first conflict: each assigned literal with its level and reason clause."""
        return {"trail": [(l, self.level[abs(l)], None if self.reason[abs(l)] is None else
                           list(self.clauses[self.reason[abs(l)]])) for l in self.trail],
                "conflict": list(self.clauses[confl])}


# ---------------------------------------------------------------------------
# Circuits
# ---------------------------------------------------------------------------
class Circuit:
    """Boolean gates as SAT variables, each defined by Tseitin's clauses."""

    def __init__(self):
        self.n = 0
        self.clauses: list[list[int]] = []
        self._true = None

    def var(self) -> int:
        self.n += 1
        return self.n

    def true(self) -> int:
        if self._true is None:
            self._true = self.var()
            self.clauses.append([self._true])
        return self._true

    def AND(self, a, b):
        z = self.var()
        self.clauses += [[-z, a], [-z, b], [z, -a, -b]]
        return z

    def OR(self, a, b):
        z = self.var()
        self.clauses += [[z, -a], [z, -b], [-z, a, b]]
        return z

    def XOR(self, a, b):
        z = self.var()
        self.clauses += [[-z, a, b], [-z, -a, -b], [z, -a, b], [z, a, -b]]
        return z

    def ripple_adder(self, A, B):
        """Sum bits of A + B (n bits each, least significant first), carries rippling up."""
        s, c = [], None
        for a, b in zip(A, B):
            p = self.XOR(a, b)
            if c is None:
                s.append(p)
                c = self.AND(a, b)
            else:
                s.append(self.XOR(p, c))
                c = self.OR(self.AND(a, b), self.AND(p, c))
        return s

    def kogge_stone_adder(self, A, B, bug_at: int | None = None):
        """Sum bits by a parallel-prefix (Kogge-Stone, 1973) carry network. ``bug_at``: at that bit, the first level
        of the network combines with the neighbour's propagate signal instead of its own (an off-by-one slip)."""
        n = len(A)
        g = [self.AND(a, b) for a, b in zip(A, B)]
        p = [self.XOR(a, b) for a, b in zip(A, B)]
        G, P = g[:], p[:]
        d = 1
        while d < n:
            G2, P2 = G[:], P[:]
            for i in range(d, n):
                t = self.AND(P[i - d] if (bug_at == i and d == 1) else P[i], G[i - d])
                G2[i] = self.OR(G[i], t)
                P2[i] = self.AND(P[i], P[i - d])
            G, P = G2, P2
            d *= 2
        s = [p[0]] + [self.XOR(p[i], G[i - 1]) for i in range(1, n)]
        return s

    def array_multiplier(self, A, B):
        """The low bits of A * B by shift-and-add (rows of partial products, ripple adders)."""
        n = len(A)
        acc = [self.AND(A[0], b) for b in B][:n]
        for i in range(1, n):
            row = [self.AND(A[i], B[j]) for j in range(n - i)]
            hi = self.ripple_adder(acc[i:], row)
            acc = acc[:i] + hi
        return acc

    def miter(self, X, Y):
        """A clause saying 'some output bit differs': satisfiable exactly when the circuits disagree somewhere."""
        diffs = [self.XOR(x, y) for x, y in zip(X, Y)]
        self.clauses.append(diffs)
        return diffs


def eval_adder_bits(bits_a, bits_b) -> list[int]:
    a = sum(b << i for i, b in enumerate(bits_a))
    b = sum(b << i for i, b in enumerate(bits_b))
    s = (a + b) % (1 << len(bits_a))
    return [(s >> i) & 1 for i in range(len(bits_a))]
