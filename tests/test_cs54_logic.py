"""Tests for Part 54's logic instruments (explainer/cs/verify: hoare, absint, lcf).  Every SAT verdict is checked
against brute force over all inputs at small widths, every abstract state against concrete runs, every theorem
against truth tables."""

from __future__ import annotations

import inspect
import itertools
import json
import random
import unittest

from explainer.cs.verify import absint as A
from explainer.cs.verify import hoare as H
from explainer.cs.verify import lcf as L


def brute_valid(formula, w):
    """(valid?, a counterexample) by trying every signed w-bit assignment of the free variables."""
    names = H.free_vars(formula)
    rng = range(-(1 << (w - 1)), 1 << (w - 1))
    for vals in itertools.product(rng, repeat=len(names)):
        env = dict(zip(names, vals))
        if not H.evaluate(formula, env, w):
            return False, env
    return True, None


def all_programs():
    progs = {k: f() for k, f in H.EXAMPLES.items()}
    progs["binsearch_buggy"] = H.binary_search_program("(lo + hi) >> 1")
    for i, (mid, pre, _) in enumerate(H.MIDPOINTS):
        progs[f"mid{i}"] = H.midpoint_program(mid, pre)
    return progs


# ------------------------------------------------------------------------------------------- hoare

class Syntax(unittest.TestCase):
    TEXTS = ["x + y - (x + y - y) == Y", "(lo + hi) >> 1", "lo + ((hi - lo) >>> 1) < hi", "-x * (y + 3) != -5",
             "a < 1 ==> b < c ==> !(d == e) || f >= g && h <= i", "!(!(a < b))",
             "(a < 0 ==> b < 0) ==> c < 0", "x - (y - z) > 0"]

    def test_round_trip(self):
        for t in self.TEXTS:
            e = H.parse(t)
            self.assertEqual(H.parse(H.show(e)), e, t)

    def test_precedence(self):
        self.assertEqual(H.parse("a + b >> 1"), ("ashr", ("add", ("var", "a"), ("var", "b"))))
        self.assertEqual(H.parse("x < 1 ==> y < 2 ==> z < 3")[2][0], "implies")
        self.assertEqual(H.show(H.parse("(a + b) >> 1 < c")), "(a + b) >> 1 < c")

    def test_sorts(self):
        with self.assertRaises(TypeError):
            H.parse("(a < b) + 1")
        with self.assertRaises(SyntaxError):
            H.parse("x >> 2")

    def test_wrap(self):
        self.assertEqual(H.wrap(32768, 16), -32768)
        self.assertEqual(H.evaluate(H.parse("x + y"), {"x": 32767, "y": 1}, 16), -32768)
        self.assertEqual(H.evaluate(H.parse("x >>> 1"), {"x": -2}, 4), 7)
        self.assertEqual(H.evaluate(H.parse("x >> 1"), {"x": -3}, 4), -2)


class Encoder(unittest.TestCase):
    """The bit-blaster agrees with the concrete semantics on every pair of 4-bit inputs."""
    W = 4
    TERMS = ["x + y", "x - y", "x * y", "-x", "x >> 1", "x >>> 1", "(x + y) >> 1"]
    PROPS = ["x < y", "x <= y", "x > y", "x >= y", "x == y", "x != y"]

    def test_terms_and_props(self):
        rng = range(-8, 8)
        for t in self.TERMS + self.PROPS:
            e = H.parse(t)
            for a, b in itertools.product(rng, rng):
                env = {"x": a, "y": b}
                v = H.evaluate(e, env, self.W)
                fixed = ("and", ("eq", H.var("x"), H.const(a)), ("eq", H.var("y"), H.const(b)))
                goal = ("eq", e, H.const(v)) if isinstance(v, int) and not isinstance(v, bool) else (e if v else ("not", e))
                r = H.check_vc(("implies", fixed, goal), self.W)
                self.assertEqual(r["status"], "valid", (t, a, b))

    def test_constants(self):
        self.assertEqual(H.check_vc("true", 4)["status"], "valid")
        self.assertEqual(H.check_vc("false", 4)["status"], "invalid")
        self.assertEqual(H.check_vc("x + 1 > x", 4)["counterexample"], {"x": 7})


class VCs(unittest.TestCase):
    def test_every_vc_against_brute_force(self):
        for w in (4,):
            for name, prog in all_programs().items():
                for v in H.vcs(prog):
                    r = H.check_vc(v["formula"], w)
                    valid, _ = brute_valid(v["formula"], w)
                    self.assertEqual(r["status"], "valid" if valid else "invalid", (name, v["name"], w))
                    if r["counterexample"] is not None:
                        self.assertFalse(H.evaluate(v["formula"], r["counterexample"], w))

    def test_midpoints_at_six_bits(self):
        for mid, pre, _ in H.MIDPOINTS:
            f = H.vcs(H.midpoint_program(mid, pre))[0]["formula"]
            self.assertEqual(H.check_vc(f, 6)["status"] == "valid", brute_valid(f, 6)[0], mid)

    def test_wp_matches_execution(self):
        """For loop-free programs, pre ==> wp(body, post) holds at a state iff running the body from it ends in
        post (when pre holds)."""
        w = 4
        for name in ["max", "swap", "mid0", "mid1", "mid2", "mid3", "mid4"]:
            prog = all_programs()[name]
            f = H.vcs(prog)[0]["formula"]
            names = H.free_vars(f)
            for vals in itertools.product(range(-8, 8), repeat=len(names)):
                env = dict(zip(names, vals))
                ok = (not H.evaluate(prog["pre"], env, w)) or H.evaluate(prog["post"], H.run(prog["body"], env, w), w)
                self.assertEqual(H.evaluate(f, env, w), ok, (name, env))

    def test_proved_loops_run_correctly(self):
        """Programs whose VCs are all valid at 4 bits terminate and meet their post on every input."""
        w = 4
        gauss = H.gauss_program()
        self.assertTrue(H.verify(gauss, w)["proved"])
        for n in range(0, 8):
            env = H.run(gauss["body"], {"n": n}, w, fuel=1000)
            self.assertTrue(H.evaluate(gauss["post"], env, w))
            self.assertEqual(env["s"], H.wrap(n * (n + 1) // 2, w))
        bs = H.binary_search_program()
        self.assertTrue(H.verify(bs, w)["proved"])
        rnd = random.Random(0)
        for lo, hi in itertools.product(range(0, 8), range(0, 8)):
            if lo <= hi:
                for _ in range(5):
                    env = H.run(bs["body"], {"lo": lo, "hi": hi}, w, choose=lambda x, e: rnd.choice([0, 1]),
                                fuel=1000)
                    self.assertEqual(env["lo"], env["hi"])

    def test_variant_catches_nontermination(self):
        prog = H.program("stuck", [H.while_("i < n", "true", [H.assign("i", "i + 0")], variant="n - i")])
        r = {v["name"]: v["status"] for v in H.verify(prog, 4)["vcs"]}
        self.assertEqual(r["loop 1: variant decreases"], "invalid")

    def test_swap_needs_wraparound_only(self):
        r = H.verify(H.swap_program(), 16)
        self.assertTrue(r["proved"])

    def test_flow(self):
        prog = H.swap_program()
        steps = H.flow(prog)
        self.assertEqual([s["line"] for s in steps], [3, 2, 1, 0])
        self.assertEqual(steps[0]["after"], "x == Y && y == X")
        self.assertEqual(steps[0]["before"], "x - y == Y && y == X")
        self.assertEqual(steps[2]["before"], H.show(H.wp(prog["body"], prog["post"])))
        for a, b in zip(steps, steps[1:]):
            self.assertEqual(a["before"], b["after"])
        g = H.flow(H.gauss_program())
        self.assertEqual(g[0]["after"], H.show(H.gauss_program()["body"][2][2]))     # the body starts from inv


class Bloch(unittest.TestCase):
    def test_midpoint_study(self):
        rows = H.midpoint_study(16)
        self.assertEqual([r["status"] for r in rows], ["invalid", "valid", "valid", "invalid", "valid"])
        d = rows[0]["detail"]
        self.assertTrue(0 <= d["lo"] < d["hi"] <= 32767)
        self.assertGreater(d["true_sum"], 32767)                       # the overflow is the only way to fail
        self.assertEqual(d["wrapped_sum"], d["true_sum"] - 65536)
        self.assertEqual(d["mid"], d["wrapped_sum"] >> 1)
        self.assertFalse(d["lo"] <= d["mid"] < d["hi"])
        d3 = rows[3]["detail"]
        self.assertGreater(d3["true_diff"], 32767)
        json.dumps(rows)

    def test_valid_midpoints_sampled_at_16_bits(self):
        rnd = random.Random(1)
        for mid, pre, _ in [H.MIDPOINTS[i] for i in (1, 2, 4)]:
            prog = H.midpoint_program(mid, pre)
            for _ in range(5000):
                lo, hi = sorted(rnd.sample(range(-32768, 32768), 2))
                env = {"lo": lo, "hi": hi}
                if H.evaluate(prog["pre"], env, 16):
                    m = H.run(prog["body"], env, 16)["mid"]
                    self.assertTrue(lo <= m < hi, (mid, lo, hi, m))

    def test_buggy_loop_counterexample_is_real(self):
        prog = H.binary_search_program("(lo + hi) >> 1")
        res = H.verify(prog, 16)
        bad = [v for v in res["vcs"] if v["status"] == "invalid"]
        self.assertTrue(bad)
        pres = next(v for v in bad if "preserved" in v["name"])
        cex = pres["counterexample"]
        cvar = next(k for k in cex if k.startswith("c'"))
        with self.assertRaises(H.AssertionFailed):
            H.run(prog["body"], {"lo": cex["lo"], "hi": cex["hi"]}, 16, choose=lambda x, e: cex[cvar])
        self.assertTrue(H.verify(H.binary_search_program(), 16)["proved"])


# ------------------------------------------------------------------------------------------- absint

def rand_interval(rnd):
    lo = -A.INF if rnd.random() < 0.2 else rnd.randint(-20, 20)
    hi = A.INF if rnd.random() < 0.2 else rnd.randint(-20, 20)
    return (lo, hi) if lo <= hi else (hi, lo)


def sample(iv, rnd):
    lo = iv[0] if iv[0] != -A.INF else iv[1] - 30 if iv[1] != A.INF else -30
    hi = iv[1] if iv[1] != A.INF else lo + 30
    return rnd.randint(int(lo), int(hi))


class Intervals(unittest.TestCase):
    def test_lattice_laws(self):
        rnd = random.Random(2)
        for _ in range(2000):
            a, b = rand_interval(rnd), rand_interval(rnd)
            j = A.join(a, b)
            self.assertTrue(A.leq(a, j) and A.leq(b, j))
            m = A.meet(a, b)
            self.assertTrue(A.leq(m, a) and A.leq(m, b))
            self.assertTrue(A.leq(j, A.widen(a, j)))
            if A.leq(b, a):
                n = A.narrow(a, b)
                self.assertTrue(A.leq(b, n) and A.leq(n, a))

    def test_transfer_soundness(self):
        rnd = random.Random(3)
        terms = [H.parse(t) for t in ["x + y", "x - y", "x * y", "-x", "x >> 1", "x * x - y"]]
        conds = [H.parse(t) for t in ["x < y", "x <= 3", "y > x", "x == y", "x != 2", "!(x < y) || y == 1",
                                      "x < y ==> x > 0"]]
        for _ in range(1500):
            s = {"x": rand_interval(rnd), "y": rand_interval(rnd)}
            env = {k: sample(v, rnd) for k, v in s.items()}
            for t in terms:
                v = H.evaluate(t, env, None)
                iv = A.aeval(t, s)
                self.assertTrue(iv[0] <= v <= iv[1], (t, s, env, iv))
            for c in conds:
                if H.evaluate(c, env, None):
                    self.assertTrue(A.contains(A.afilter(s, c), env), (c, s, env))

    def test_counter_iterations(self):
        plain = A.analyze(A.counter_program(), widen=False)
        self.assertEqual(plain["loops"][0]["ascending"], 101)
        self.assertEqual(plain["loops"][0]["head"], {"x": [0, 100]})
        wid = A.analyze(A.counter_program(), widen=True)
        loop = wid["loops"][0]
        self.assertEqual(loop["ascending"], 2)
        asc = [t["head"] for t in wid["trace"] if t["phase"] == "ascending"]
        self.assertEqual(asc, [{"x": [0, "+inf"]}, {"x": [0, "+inf"]}])
        self.assertEqual(loop["head"], {"x": [0, 100]})                 # narrowed back
        self.assertEqual(wid["exit"], {"x": [100, 100]})
        self.assertTrue(wid["asserts"][0]["proved"])
        json.dumps(A.examples())

    def test_relational_gap(self):
        g = A.relational_gap()
        self.assertEqual(g["reachable"], [[i, 2 * i] for i in range(11)])
        self.assertFalse(g["no_widen_converged"])
        self.assertEqual([c["j"][1] for c in g["no_widen_climb"][:5]], [0, 2, 4, 6, 8])
        self.assertEqual(g["widen_head"], {"i": [0, 10], "j": [0, "+inf"]})
        self.assertFalse(g["assert_proved"])

    def check_sound(self, prog, envs, choose=None):
        for widen in (False, True):
            r = A.analyze(prog, widen=widen, max_iter=200)["_raw"]
            for env in envs:
                try:
                    c = A.concrete_states(prog, env, choose=choose)
                except H.Blocked:
                    continue
                for line, seen in c["points"].items():
                    for e in seen:
                        self.assertTrue(A.contains(r["points"][line], e), (prog["name"], widen, line, e))
                for line, seen in c["heads"].items():
                    for e in seen:
                        self.assertTrue(A.contains(r["heads"][line], e), (prog["name"], widen, line, e))
                if c["exit"] is not None:
                    self.assertTrue(A.contains(r["exit"], c["exit"]))

    def test_soundness_examples(self):
        self.check_sound(A.counter_program(), [{}])
        self.check_sound(A.two_counter_program(), [{}])
        self.check_sound(A.bounded_program(), [{"n": n} for n in range(-3, 55)])

    def test_soundness_random_programs(self):
        rnd = random.Random(4)
        vs = ["a", "b", "c"]

        def expr(d=0):
            r = rnd.random()
            if d > 1 or r < 0.3:
                return rnd.choice(vs + [str(rnd.randint(-5, 5))])
            op = rnd.choice(["+", "-", "*", ">> 1"])
            return f"(({expr(d + 1)}) >> 1)" if op == ">> 1" else f"({expr(d + 1)} {op} {expr(d + 1)})"

        def cond():
            return f"{expr(1)} {rnd.choice(['<', '<=', '>', '>=', '==', '!='])} {expr(1)}"

        def block(depth, counters):
            out = []
            for _ in range(rnd.randint(1, 3)):
                r = rnd.random()
                if r < 0.5 or depth > 1:
                    out.append(H.assign(rnd.choice(vs), expr()))
                elif r < 0.75:
                    out.append(H.if_(cond(), block(depth + 1, counters), block(depth + 1, counters)))
                elif r < 0.85:
                    out.append(H.assume(cond()))
                else:
                    k = f"k{len(counters)}"
                    counters.append(k)
                    out += [H.assign(k, "0"),
                            H.while_(f"{k} < {rnd.randint(1, 6)}", "true",
                                     block(depth + 1, counters) + [H.assign(k, f"{k} + 1")])]
            return out

        for i in range(60):
            prog = H.program(f"random {i}", block(0, []))
            envs = [{v: rnd.randint(-10, 10) for v in vs} for _ in range(15)]
            self.check_sound(prog, envs)


# ------------------------------------------------------------------------------------------- lcf

class Kernel(unittest.TestCase):
    def test_theorems(self):
        p = L.proofs()
        self.assertEqual(p["and_comm"]["theorem"], "⊢ A ∧ B ⇒ B ∧ A")
        self.assertEqual(p["imp_trans"]["theorem"], "⊢ (A ⇒ B) ∧ (B ⇒ C) ⇒ A ⇒ C")
        self.assertEqual(p["peirce"]["theorem"], "⊢ ((A ⇒ B) ⇒ A) ⇒ A")
        for name, r in p.items():
            self.assertTrue(r["closed"], name)
            self.assertTrue(r["tautology"], name)                       # sound classically
            self.assertEqual(r["tree"]["sequent"], r["theorem"])
            for s in r["steps"]:
                self.assertTrue(all(q < s["id"] for q in s["premises"]))
            # intuitionistic proofs hold in the Kripke model; Peirce (classical) fails there
            self.assertEqual(r["holds_in_kripke_countermodel"], not r["classical"], name)
        self.assertTrue(p["peirce"]["classical"])
        json.dumps(p)

    def test_excluded_middle_fails_intuitionistically(self):
        em = L.Or(L.A, L.Not(L.A))
        self.assertTrue(L.tautology(em))
        self.assertFalse(L.kripke_holds(em, 0, **L.KRIPKE_PEIRCE))

    def test_refusals(self):
        for r in L.illegal_steps():
            self.assertTrue(r["refused"], r["attempt"])
        with self.assertRaises(L.KernelError):
            L.or_elim(L.assume(L.Or(L.A, L.B)), L.assume(L.A), L.assume(L.B))
        with self.assertRaises(L.KernelError):
            L.bot_elim(L.assume(L.A), L.B)

    def test_hypotheses_are_tracked(self):
        th = L.imp_elim(L.assume(L.Imp(L.A, L.B)), L.assume(L.A))
        self.assertEqual(th.hyps, frozenset({L.Imp(L.A, L.B), L.A}))
        th2 = L.imp_intro(L.A, th)
        self.assertEqual(th2.hyps, frozenset({L.Imp(L.A, L.B)}))
        self.assertEqual(th2.concl, L.Imp(L.A, L.B))

    def test_kernel_size(self):
        k = L.kernel_size()
        self.assertLess(k["kernel_lines"], k["module_lines"] / 2)
        src = inspect.getsource(L).splitlines()
        begin = next(i for i, ln in enumerate(src) if ln.startswith("# ---- KERNEL BEGIN"))
        end = next(i for i, ln in enumerate(src) if ln.startswith("# ---- KERNEL END"))
        for rule in L.RULES + ["Thm"]:
            start = inspect.getsourcelines(getattr(L, rule))[1] - 1
            self.assertTrue(begin < start < end, rule)


if __name__ == "__main__":
    unittest.main()
