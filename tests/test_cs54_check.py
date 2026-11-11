"""Tests for Part 54's model checkers, BDDs and testing instruments (explainer/cs/verify: models, bdd, testing).
Every verdict is checked against an independent computation: path enumeration, brute force over small state
spaces, a closed form, a published count, or a replay of the counterexample on the model."""

from __future__ import annotations

import itertools
import random
import unittest

import numpy as np

from explainer.cs.verify import bdd as D
from explainer.cs.verify import models as M
from explainer.cs.verify import testing as T


# ------------------------------------------------------------------------------------------------ helpers

def replay(m: M.Model, trace: list[dict]) -> list:
    """Re-run a JSON trace on the model: each action must be enabled and lead to the recorded state."""
    s = m.init[0]
    assert trace[0]["action"] is None and m.show(s) == trace[0]["state"]
    states = [s]
    for step in trace[1:]:
        nxt = [t for a, t in m.step(s) if a == step["action"]]
        assert nxt, step["action"]
        s = nxt[0]
        assert m.show(s) == step["state"]
        states.append(s)
    return states


def paths(K: M.Kripke, i: int, length: int):
    """Every path of exactly ``length`` steps from state i (as lists of state ids)."""
    if length == 0:
        yield [i]
        return
    for _, j in K.succ[i]:
        for p in paths(K, j, length - 1):
            yield [i] + p


def brute(K: M.Kripke, f, i: int) -> bool:
    """CTL semantics by enumerating paths of length n (n = number of states: long enough to contain a cycle)."""
    n = K.n
    if isinstance(f, str):
        return f == "true" or (f != "false" and f in K.labels[i])
    op = f[0]
    if op == "not":
        return not brute(K, f[1], i)
    if op == "and":
        return brute(K, f[1], i) and brute(K, f[2], i)
    if op == "or":
        return brute(K, f[1], i) or brute(K, f[2], i)
    if op == "EX":
        return any(brute(K, f[1], j) for _, j in K.succ[i])
    if op == "AX":
        return all(brute(K, f[1], j) for _, j in K.succ[i])
    if op == "EG":
        return any(all(brute(K, f[1], s) for s in p) for p in paths(K, i, n))
    if op == "AG":
        return all(brute(K, f[1], s) for p in paths(K, i, n) for s in p)
    if op == "EF":
        return any(brute(K, f[1], s) for p in paths(K, i, n) for s in p)
    if op == "AF":
        return all(any(brute(K, f[1], s) for s in p) for p in paths(K, i, n))
    if op == "EU":
        for p in paths(K, i, n):
            for s in p:
                if brute(K, f[2], s):
                    return True
                if not brute(K, f[1], s):
                    break
        return False
    if op == "AU":                         # every path meets g, with f until then (paths of length n suffice)
        for p in paths(K, i, n):
            ok = False
            for s in p:
                if brute(K, f[2], s):
                    ok = True
                    break
                if not brute(K, f[1], s):
                    break
            if not ok:
                return False
        return True
    raise ValueError(op)


def fair_brute(K, starts, region, fairness) -> bool:
    """A fair infinite path from a start inside the region exists iff some strongly connected set of region edges,
    reachable from a start within the region, meets every constraint: weak — an A-edge in the set or a vertex with A
    disabled; strong — an A-edge in the set or A disabled at every vertex.  (The edges a path takes infinitely often
    form exactly such a set.)  Enumerated over all edge subsets."""
    edges = [(i, a, j) for i in region for a, j in K.succ[i] if j in region]
    reach = set(s for s in starts if s in region)
    work = list(reach)
    while work:
        i = work.pop()
        for a, j in K.succ[i]:
            if j in region and j not in reach:
                reach.add(j)
                work.append(j)
    edges = [e for e in edges if e[0] in reach]
    for r in range(1, len(edges) + 1):
        for sub in itertools.combinations(edges, r):
            vs = {e[0] for e in sub} | {e[2] for e in sub}
            v0 = next(iter(vs))
            fw = {v0}
            changed = True
            while changed:
                changed = False
                for i, _, j in sub:
                    if i in fw and j not in fw:
                        fw.add(j)
                        changed = True
            bw = {v0}
            changed = True
            while changed:
                changed = False
                for i, _, j in sub:
                    if j in bw and i not in bw:
                        bw.add(i)
                        changed = True
            if fw != vs or bw != vs:
                continue
            ok = True
            for kind, A in fairness:
                if any(a in A for _, a, _ in sub):
                    continue
                dis = [not any(a in A for a, _ in K.succ[v]) for v in vs]
                if not (any(dis) if kind == "weak" else all(dis)):
                    ok = False
                    break
            if ok:
                return True
    return False


# ------------------------------------------------------------------------------------------------ models

class CTL(unittest.TestCase):
    def test_fixpoints_against_path_enumeration(self):
        forms = [("EX", "p"), ("AX", "p"), ("EG", "p"), ("AG", "p"), ("EF", "q"), ("AF", "q"), ("EU", "p", "q"),
                 ("AU", "p", "q"), ("AG", ("EF", "q")), ("EG", ("or", "p", ("not", "q"))),
                 ("AF", ("AG", "p")), ("not", ("EU", ("not", "q"), ("and", "p", "q")))]
        for seed in range(40):
            K = M.build(M.random_model(5, seed))
            for f in forms:
                S = M.sat(K, f)
                for i in range(K.n):
                    self.assertEqual(i in S, brute(K, f, i), (seed, f, i))

    def test_fair_cycles_against_edge_subsets(self):
        rng = random.Random(7)
        for seed in range(60):
            K = M.build(M.random_model(5, seed))
            region = {i for i in range(K.n) if "q" not in K.labels[i]}
            starts = sorted(i for i in range(K.n) if "p" in K.labels[i])
            acts = ["e0", "e1", M.STUTTER]
            fairness = [(rng.choice(["weak", "strong"]), set(rng.sample(acts, rng.randint(1, 2))))
                        for _ in range(rng.randint(0, 2))]
            lasso = M.fair_lasso(K, starts, region, fairness)
            self.assertEqual(lasso is not None, fair_brute(K, starts, region, fairness), (seed, fairness))
            if lasso is not None:
                self.assertIn(lasso["start"], starts)
                self.assertTrue(M.check_lasso(K, lasso, region, fairness))

    def test_show(self):
        self.assertEqual(M.show(M.MUTEX), "AG ¬(cs0 ∧ cs1)")
        self.assertEqual(M.show(("AG", ("imp", "try0", ("AF", "cs0")))), "AG (try0 → AF cs0)")


class Peterson(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = M.peterson_results()

    def test_mutex_and_ctl(self):
        ctl = {c["formula"]: c["holds"] for c in self.r["ctl"]}
        self.assertTrue(ctl["AG ¬(cs0 ∧ cs1)"])
        self.assertFalse(ctl["AG (try0 → AF cs0)"])         # without fairness, P1 may idle and P0 never be scheduled
        self.assertTrue(ctl["AG (try0 → EF cs0)"])
        self.assertTrue(ctl["AG ¬deadlock"])
        # brute force: no reachable state has both in the critical section
        K = M.build(M.peterson())
        self.assertFalse(any(s[0] == 3 and s[1] == 3 for s in K.states))
        # reachable states by a hand enumeration of (pc0, pc1, flag0, flag1, turn) consistent with the code
        cand = [s for s in itertools.product(range(4), range(4), (0, 1), (0, 1), (0, 1))
                if s[2] == (s[0] > 0) and s[3] == (s[1] > 0)]
        self.assertTrue(set(K.states) <= set(cand))
        self.assertEqual(self.r["states"], K.n)

    def test_liveness(self):
        m = M.peterson()
        K = M.build(m)
        unfair = M.response(K, "try0", "cs0")
        self.assertFalse(unfair["holds"])
        region = set(range(K.n)) - M.sat(K, "cs0")
        self.assertTrue(M.check_lasso(K, unfair["lasso"], region, []))
        self.assertTrue(all(st["action"] == "idle1" for st in unfair["cycle"]))
        for r in self.r["response_weak"]:
            self.assertTrue(r["holds"])
        # the weakly fair cycle check agrees with brute force over strongly connected edge sets is covered by
        # CTL.test_fair_cycles_against_edge_subsets; here: weak fairness of P0 alone already suffices for P0
        fair0 = [M.process_fairness(m)[0]]
        self.assertTrue(M.response(K, "try0", "cs0", fair0)["holds"])
        self.assertFalse(M.response(K, "try0", "cs0", [M.process_fairness(m)[1]])["holds"])

    def test_broken(self):
        b = self.r["broken"]
        self.assertFalse(b["mutex"])
        states = replay(M.peterson(broken=True), b["counterexample"])
        self.assertEqual(states[-1][:2], (3, 3))
        # shortest: no state with both in cs at smaller depth (BFS layers recomputed)
        K = M.build(M.peterson(broken=True))
        best = min(K.depth[i] for i, s in enumerate(K.states) if s[0] == 3 and s[1] == 3)
        self.assertEqual(len(b["counterexample"]) - 1, best)

    def test_part33(self):
        p = self.r["part33"]
        self.assertTrue(p["agree"])
        self.assertTrue(p["part33_mutex"])
        self.assertFalse(p["broken_part33_mutex"])


class Philosophers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = M.philosopher_results()

    @staticmethod
    def consistent(n, ordered):
        """Configurations in which no fork is held twice (all of them are reachable)."""
        fs = M.forks(n, ordered)
        c = 0
        for s in itertools.product(range(3), repeat=n):
            held = [0] * n
            for p, (a, b) in enumerate(fs):
                held[a] += s[p] >= 1
                held[b] += s[p] == 2
            c += max(held) <= 1
        return c

    def test_counts(self):
        Mx = np.array([[1, 1, 1], [1, 1, 1], [1, 0, 0]], dtype=object)    # transfer matrix: E then H/E clash
        for row in self.r["rows"]:
            n = row["n"]
            self.assertEqual(row["states"], self.consistent(n, row["ordered"]))
            if not row["ordered"]:
                self.assertEqual(row["states"], int(np.trace(np.linalg.matrix_power(Mx, n))))

    def test_deadlock(self):
        for row in self.r["rows"]:
            n = row["n"]
            self.assertEqual(row["EF_deadlock"], not row["ordered"])
            if not row["ordered"]:
                self.assertEqual(row["deadlocks"], 1)
                self.assertEqual(row["counterexample_length"], n)
                self.assertEqual(sorted(row["counterexample"]), sorted(f"take1_{i}" for i in range(n)))
                m = M.philosophers(n)
                s = m.init[0]
                for a in row["counterexample"]:
                    s = dict(m.step(s))[a]
                self.assertEqual(m.step(s), [])
                self.assertEqual(s, (1,) * n)

    def test_part33(self):
        for r in M.philosophers_vs_part33((2, 3)):
            self.assertEqual(r["part33_deadlock"], r["ours_deadlock"])
            self.assertEqual(r["ours_deadlock"], not r["ordered"])

    def test_starvation(self):
        st = self.r["starvation"]
        self.assertFalse(st["weak"]["holds"])
        self.assertTrue(st["strong"]["holds"])
        m = M.philosophers(3, True)
        K = M.build(m)
        lasso = M.response(K, "hungry0", "eat0", M.philosopher_fairness(m, 3, "weak"))["lasso"]
        region = set(range(K.n)) - M.sat(K, "eat0")
        self.assertTrue(M.check_lasso(K, lasso, region, M.philosopher_fairness(m, 3, "weak")))
        self.assertFalse(M.check_lasso(K, lasso, region, M.philosopher_fairness(m, 3, "strong")))


class TwoPhase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = M.two_phase_results()

    def test_counts(self):
        rows = {row["n"]: row for row in self.r["rows"]}
        for n, row in rows.items():
            self.assertEqual(row["tcommit_states"], 3 ** n + 2 ** n - 1)
            self.assertTrue(row["consistent"])
        self.assertEqual(rows[3]["tcommit_states"], 34)       # TLC on TCommit.tla with three RMs
        self.assertEqual(rows[3]["twophase_states"], 288)     # TLC on TwoPhase.tla with three RMs
        self.assertTrue(all(row["refines"] for row in rows.values() if row["refines"] is not None))

    def test_tcommit_states_by_enumeration(self):
        for n in (2, 3, 4):
            K = M.build(M.tcommit(n))
            ok = {s for s in itertools.product(range(4), repeat=n)
                  if M.COMMITTED not in s or all(x in (M.PREPARED, M.COMMITTED) for x in s)}
            self.assertEqual(set(K.states), ok)

    def test_refinement_detects_a_bad_protocol(self):
        K = M.build(M.two_phase(2, bug="timeout-commit"))
        spec = M.tcommit(2)
        bad = sum(1 for i, out in enumerate(K.succ) for _, j in out
                  if K.states[i][0] != K.states[j][0] and K.states[j][0] not in dict(
                      (t, a) for a, t in spec.step(K.states[i][0])))
        self.assertGreater(bad, 0)

    def test_bug(self):
        b = self.r["bug"]
        self.assertFalse(b["consistent"])
        self.assertEqual(b["length"], 3)
        states = replay(M.two_phase(3, bug="timeout-commit"), b["counterexample"])
        rm = states[-1][0]
        self.assertIn(M.COMMITTED, rm)
        self.assertIn(M.ABORTED, rm)
        self.assertEqual(b["counterexample"][1]["action"], "TMTimeoutCommit")


class RaftLite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = M.raft_results()

    def test_election_safety(self):
        self.assertTrue(self.r["election_safety"])
        self.assertTrue(self.r["EF_leader"])
        K = M.build(M.raft_lite())
        for s in K.states:                    # directly: no two current leaders share a term
            leaders = [t for t, r, _ in s[0] if r == M.LEADER]
            self.assertEqual(len(leaders), len(set(leaders)))
            for t, r, _ in s[0]:
                self.assertLessEqual(t, 2)

    def test_bug(self):
        b = self.r["bug"]
        self.assertFalse(b["election_safety"])
        states = replay(M.raft_lite(bug="forget-vote"), b["counterexample"])
        terms = [t for t, _ in states[-1][2]]
        self.assertEqual(len(terms), len(set(terms)) + 1)
        self.assertEqual(b["counterexample"][-1]["action"][:3], "Win")


# ------------------------------------------------------------------------------------------------ BDDs

def table(B: D.BDD, u: int, n: int) -> list[bool]:
    return [B.evaluate(u, bits) for bits in itertools.product((False, True), repeat=n)]


class BDDs(unittest.TestCase):
    def test_invalid_order_cannot_build_a_false_proof(self):
        b = D.BDD(3)
        u = b.apply("and", b.var(0), b.var(1))
        with self.assertRaises(ValueError):
            b.rename(u, {0: 1, 1: 0})
        with self.assertRaises(ValueError):
            b.var(3)
        model = M.Model("initials", (), [0, 1], [], {})
        with self.assertRaises(RuntimeError):
            M.build(model, limit=1)

    def random_formula(self, B, rng, n, depth):
        """A random formula as (BDD, python function)."""
        if depth == 0 or rng.random() < 0.2:
            v = rng.randrange(n)
            if rng.random() < 0.5:
                return B.var(v), (lambda a, v=v: a[v])
            return B.nvar(v), (lambda a, v=v: not a[v])
        op = rng.choice(list(D.OPS))
        (u, f), (w, g) = self.random_formula(B, rng, n, depth - 1), self.random_formula(B, rng, n, depth - 1)
        return B.apply(op, u, w), (lambda a, f=f, g=g, op=op: D.OPS[op](f(a), g(a)))

    def test_apply_ite_restrict_exists_count(self):
        rng = random.Random(3)
        n = 5
        assigns = list(itertools.product((False, True), repeat=n))
        for _ in range(60):
            B = D.BDD(n)
            u, f = self.random_formula(B, rng, n, 4)
            w, g = self.random_formula(B, rng, n, 3)
            h, k = self.random_formula(B, rng, n, 3)
            self.assertEqual(table(B, u, n), [bool(f(a)) for a in assigns])
            self.assertEqual(B.satcount(u), sum(bool(f(a)) for a in assigns))
            it = B.ite(u, w, h)
            self.assertEqual(table(B, it, n), [bool(g(a)) if f(a) else bool(k(a)) for a in assigns])
            self.assertEqual(it, B.apply("or", B.apply("and", u, w), B.apply("and", B.neg(u), h)))  # canonical
            v = rng.randrange(n)
            for val in (False, True):
                r = B.restrict(u, v, val)
                self.assertEqual(table(B, r, n), [bool(f(a[:v] + (val,) + a[v + 1:])) for a in assigns])
            vs = rng.sample(range(n), 2)
            ex = B.exists(u, vs)

            def ex_f(a):
                return any(f(tuple(bits[vs.index(i)] if i in vs else a[i] for i in range(n)))
                           for bits in itertools.product((False, True), repeat=2))
            self.assertEqual(table(B, ex, n), [bool(ex_f(a)) for a in assigns])
            self.assertEqual(B.and_exists(u, w, vs), B.exists(B.apply("and", u, w), vs))
            self.assertEqual(B.forall(u, vs), B.neg(B.exists(B.neg(u), vs)))
            # reducedness: no node with equal children, no duplicate triples
            for a in B.nodes(u):
                self.assertNotEqual(B.lo[a], B.hi[a])
            self.assertEqual(len(B.unique), len(set(B.unique.values())))

    def test_canonicity(self):
        B = D.BDD(4)
        a, b, c = B.var(0), B.var(1), B.var(2)
        self.assertEqual(B.neg(B.apply("and", a, b)), B.apply("or", B.neg(a), B.neg(b)))
        self.assertEqual(B.apply("and", a, B.apply("or", b, c)),
                         B.apply("or", B.apply("and", a, b), B.apply("and", a, c)))
        self.assertEqual(B.apply("xor", a, a), 0)

    def test_order_effect(self):
        for r in D.order_effect(range(1, 11)):
            self.assertEqual(r["interleaved"], r["interleaved_formula"])
            self.assertEqual(r["separated"], r["separated_formula"])
            self.assertEqual(r["models"], 2 ** r["n"])

    def test_symbolic_matches_explicit(self):
        Mx = np.array([[1, 1, 1], [1, 1, 1], [1, 0, 0]], dtype=object)
        for n in range(2, 9):
            for ordered in (False, True):
                r = D.SymbolicPhilosophers(n, ordered).reach()
                K = M.build(M.philosophers(n, ordered))
                self.assertEqual(r["states"], K.n)
                self.assertEqual(r["iterations"], max(K.depth))
                self.assertEqual(r["deadlock_states"], len(K.deadlocks))
                for layer in r["layers"]:
                    self.assertEqual(layer["states"], sum(1 for d in K.depth if d <= layer["step"]))
        for n in (10, 12):
            r = D.SymbolicPhilosophers(n).reach()
            self.assertEqual(r["states"], int(np.trace(np.linalg.matrix_power(Mx, n))))
            self.assertLess(r["nodes"], 8 * n)
            self.assertEqual(r["deadlock_states"], 1)

    def test_reachable_set_is_the_explicit_set(self):
        sp = D.SymbolicPhilosophers(4)
        r = sp.reach()
        K = M.build(M.philosophers(4))
        for s in itertools.product(range(3), repeat=4):
            bits = [False] * (16)
            for i, x in enumerate(s):
                bits[4 * i] = x >= 1
                bits[4 * i + 2] = x == 2
            self.assertEqual(sp.B.evaluate(r["R"], bits), s in K.index)

    def test_bmc(self):
        for n in range(2, 7):
            r = D.bmc(n)
            self.assertEqual(r["found"]["k"], n)
            self.assertTrue(all(not row["sat"] for row in r["rows"][:-1]))
            m = M.philosophers(n)
            s = m.init[0]
            self.assertEqual(list(s), r["found"]["states"][0])
            for a, nxt in zip(r["found"]["actions"], r["found"]["states"][1:]):
                s = dict(m.step(s))[a]
                self.assertEqual(list(s), nxt)
            self.assertEqual(m.step(s), [])
        r = D.bmc(4, ordered=True)
        self.assertIsNone(r["found"])
        self.assertGreaterEqual(r["kmax"], max(M.build(M.philosophers(4, True)).depth))


# ------------------------------------------------------------------------------------------------ testing

class PropertyBased(unittest.TestCase):
    def minimal(self, prop, inputs):
        """The smallest failing input by brute force (by length, then by total magnitude)."""
        fails = [x for x in inputs if T._fails(prop, x)]
        return min(fails, key=lambda x: (len(x), sum(abs(v) for v in x))) if fails else None

    def test_sort_dedup(self):
        r = T.pbt_results()["sort_dedup"]
        self.assertFalse(r["ok"])
        small = [list(x) for k in range(4) for x in itertools.product(range(-3, 4), repeat=k)]
        self.assertEqual(r["shrunk"], self.minimal(T.prop_sort, small))
        self.assertEqual(r["shrunk"], [0, 0])
        for x in r["steps"]:
            self.assertFalse(T.prop_sort(x))
        self.assertTrue(all(T.prop_sort(c) for c in T.lists(T.ints()).shrink(r["shrunk"])))

    def test_insert(self):
        r = T.pbt_results()["insert"]
        self.assertFalse(r["ok"])
        xs, x = r["shrunk"]
        self.assertEqual((xs, x), ([0], 1))
        # brute force: no failing input with an empty list; with one element the smallest is ([0], 1)
        cands = [(sorted(l), v) for k in range(3) for l in itertools.product(range(-2, 3), repeat=k)
                 for v in range(-2, 3)]
        fails = [c for c in cands if not T.prop_insert(c)]
        size = lambda c: (len(c[0]), sum(map(abs, c[0])) + abs(c[1]))          # noqa: E731
        self.assertEqual(min(map(size, fails)), size((xs, x)))           # as small as any failing input (a tie
        self.assertIn((xs, x), fails)                                    # with ([-1], 0))
        for s in r["steps"]:
            self.assertFalse(T.prop_insert(s))
        gen = T.tuples(T.lists(T.ints()).map(sorted), T.ints())
        self.assertTrue(all(T.prop_insert(c) for c in gen.shrink((xs, x))))       # a local minimum

    def test_passing_property_and_shrinkers(self):
        self.assertTrue(T.forall(lambda xs: sorted(sorted(xs)) == sorted(xs), T.lists(T.ints()))["ok"])
        self.assertEqual(list(T.shrink_int(0)), [])
        for x in (-17, -1, 1, 5, 100):
            cs = list(T.shrink_int(x))
            self.assertEqual(cs[0], 0)
            self.assertTrue(all(abs(c) <= abs(x) for c in cs))
            self.assertNotIn(x, cs)


class Fuzz(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.h = T.hunt()

    def test_planted_bug_is_scoped(self):
        from explainer.cs.lang.compiler import interp as IT
        from explainer.cs.lang.compiler import opt as O
        with T.planted_bug():
            self.assertEqual(O.interp.binop("div", -7, 2), -4)       # floor, wrong for Pebble
            self.assertEqual(O.interp.binop("rem", -7, 256), 249)
            self.assertEqual(O.interp.binop("div", 7, 2), 3)         # agrees when the signs agree
        self.assertIs(O.interp, IT)
        self.assertEqual(IT.binop("div", -7, 2), -3)
        self.assertEqual(IT.binop("rem", -7, 256), -7)

    def test_hunt(self):
        h = self.h
        f = h["found"]
        self.assertIsNotNone(f)
        self.assertTrue(h["clean_agree"])
        from explainer.cs.lang.compiler import fuzz
        with T.planted_bug():
            r = fuzz.differential(f["src"])
        self.assertFalse(r["ok"])
        self.assertEqual([lv for lv in (0, 1, 2, 3) if r[lv] != r["ref"]], f["levels_disagree"])
        self.assertTrue(fuzz.differential(f["src"])["ok"])
        self.assertEqual(h["programs"], f["seed"] + 1)
        for s in range(f["seed"]):                                   # the seeds before it showed nothing
            with T.planted_bug():
                self.assertNotEqual(fuzz.differential(fuzz.program(s))["ok"], False)

    def test_shrink(self):
        f = self.h["found"]
        s = T.shrink_program(f["src"], levels=tuple(f["levels_disagree"]))
        self.assertLess(s["lines"], f["lines"] // 3)
        self.assertTrue(s["clean_ok"])
        self.assertTrue(s["levels_disagree"])
        self.assertTrue(T._interesting(s["src"], "floor-division", (3,), 100_000))
        lines = s["src"].splitlines()
        for i, j in T._units(lines):                                  # 1-minimal over removable units
            self.assertFalse(T._interesting("\n".join(lines[:i] + lines[j:]), "floor-division", (3,), 100_000))


class JobAndCoverage(unittest.TestCase):
    def test_job(self):
        r = T.job_differential()
        self.assertTrue(r["all_agree"])
        from explainer.cs.pebble import programs as PR
        for row, tape in zip(r["rows"], T.JOB_TAPES):
            self.assertEqual(row["output"].encode(), PR.job_reference(tape))

    def test_coverage(self):
        r = T.coverage_results()
        tri = r["triangle_random"]
        rng = random.Random(0)
        rand = [(rng.randint(1, 100), rng.randint(1, 100), rng.randint(1, 100)) for _ in range(300)]
        kinds = [T.triangle(*x) for x in rand]
        self.assertEqual(tri["kinds"], {k: kinds.count(k) for k in set(kinds)})
        self.assertNotIn("equilateral", kinds)
        self.assertIn('return "equilateral"', tri["missed_source"])
        self.assertLess(tri["line_coverage"], 1.0)
        ins = r["insert_unit"]
        self.assertEqual(ins["line_coverage"], 1.0)
        self.assertEqual(ins["branch_coverage"], 1.0)
        self.assertTrue(ins["unit_tests_pass"])
        self.assertFalse(ins["property"]["ok"])

    def test_coverage_counts_lines(self):
        def f(x):
            if x > 0:
                return 1
            return 2
        r = T.coverage(f, [(1,)])
        self.assertEqual((r["lines"], r["lines_hit"], r["branches_hit"]), (3, 2, 1))
        r = T.coverage(f, [(1,), (-1,)])
        self.assertEqual((r["lines_hit"], r["branches_hit"], r["branch_coverage"]), (3, 2, 1.0))


if __name__ == "__main__":
    unittest.main()
