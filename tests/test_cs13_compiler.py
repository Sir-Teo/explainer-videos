"""Part 13: the Pebble compiler, checked against the IR interpreter, the reference word count, brute-force
definitions, and its own fuzzer."""
import copy
import unittest

from explainer.cs.lang import pebble_lang as P
from explainer.cs.lang.compiler import analysis as AN
from explainer.cs.lang.compiler import check as C
from explainer.cs.lang.compiler import driver as D
from explainer.cs.lang.compiler import fuzz as F
from explainer.cs.lang.compiler import interp as IT
from explainer.cs.lang.compiler import lower as L
from explainer.cs.lang.compiler import opt as O
from explainer.cs.lang.compiler import ssa as S
from explainer.cs.pebble import programs as PR

TEXT = ("It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want "
        "of a wife. However little known the feelings or views of such a man may be on his first entering a "
        "neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered "
        "the rightful property of some one or other of their daughters. ") * 3


def module(src=P.JOB, rotate=False):
    prog = P.parse(src)
    return L.lower(prog, C.check(prog), rotate=rotate)


class Front(unittest.TestCase):
    def test_types_and_layout(self):
        info = C.check(P.parse(P.JOB))
        node = info.structs["Node"]
        self.assertEqual(node.size, 16)
        self.assertEqual([node.fields[f][0] for f in ("next", "letters", "length", "count")], [0, 4, 8, 12])

    def test_type_errors(self):
        bad = ["fn main() -> int { var x: int = null; return 0; }",
               "fn main() -> int { return y; }",
               "fn main() -> int { var p: *int = null; return p.f; }",
               "fn f(a: int) -> int { return a; } fn main() -> int { return f(1, 2); }"]
        for src in bad:
            with self.assertRaises(C.TypeError_):
                C.check(P.parse(src))


class Middle(unittest.TestCase):
    def test_interpreter_matches_reference(self):
        tape = PR.job_tape(TEXT)
        for src in (P.JOB, P.JOB_ARRAY):
            self.assertEqual(bytes(IT.run(module(src), tape).out), PR.job_reference(tape))

    def test_ssa_round_trip_and_passes(self):
        tape = PR.job_tape(TEXT)
        ref = PR.job_reference(tape)
        for src in (P.JOB, P.JOB_ARRAY):
            for rot in (False, True):
                m = module(src, rot)
                for f in m.funcs:
                    S.to_ssa(f)
                self.assertEqual(bytes(IT.run(m, tape).out), ref)
                for f in m.funcs:
                    O.optimize(f)
                self.assertEqual(bytes(IT.run(m, tape).out), ref)
                for f in m.funcs:
                    S.from_ssa(f)
                self.assertEqual(bytes(IT.run(m, tape).out), ref)

    def test_dominators_against_definition(self):
        m = module(P.JOB, True)
        for f in m.funcs:
            idom, _ = S.dominators(f)
            labels = [b.label for b in f.blocks]
            entry = labels[0]
            lab = f.labels()

            def reachable_without(d):
                seen, stack = set(), [entry] if entry != d else []
                while stack:
                    x = stack.pop()
                    if x in seen or x == d:
                        continue
                    seen.add(x)
                    stack += lab[x].succs()
                return seen
            for d in labels:
                cut = reachable_without(d)
                for n in labels:
                    self.assertEqual(S.dominates(idom, d, n), n == d or n not in cut, (f.name, d, n))

    def test_ssa_interference_is_chordal(self):
        for name in ("same", "lookup", "printnum", "report", "main"):
            m = module(P.JOB, True)
            f = m.func(name)
            S.to_ssa(f)
            O.optimize(f)
            g = AN.interference_ssa(f)
            ok, order, _ = AN.is_chordal(g)
            self.assertTrue(ok, name)
            col = AN.color_peo(g, order)
            self.assertEqual(max(col.values()) + 1, AN.max_clique_chordal(g))

    def test_liveness_fixed_point(self):
        f = module().func("same")
        IN, OUT, trace, rounds = AN.liveness(f)
        self.assertIn("%i", IN[f.blocks[1].label])
        self.assertEqual(IN[f.blocks[0].label], {"%a", "%b", "%n"})


class Back(unittest.TestCase):
    def test_job_every_level(self):
        tape = PR.job_tape(TEXT)
        ref = PR.job_reference(tape)
        for src in (P.JOB, P.JOB_ARRAY):
            steps = []
            for lv in (0, 1, 2, 3):
                m = D.run(D.compile_program(src, lv), tape)
                self.assertEqual(bytes(m.output), ref, (lv,))
                steps.append(m.steps)
            self.assertGreater(steps[0], steps[1])
            self.assertGreater(steps[1], steps[2])

    def test_fuzz_sample(self):
        for seed in range(12):
            r = F.differential(F.program(seed, funcs=3), max_steps=2_000_000)
            self.assertIn(r["ok"], (True, None), seed)


class Super(unittest.TestCase):
    def test_superoptimizer_and_rules(self):
        import z3

        from explainer.cs.lang.compiler import superopt as SO
        n, progs = SO.search(lambda x: abs(SO.s32(x)), 1, max_len=3, limit=1)
        self.assertEqual(n, 3)
        self.assertTrue(SO.prove(progs[0], lambda x: z3.If(x < 0, -x, x))[0])
        self.assertTrue(SO.check_rule(lambda x: x * 8, lambda x: x << 3)[0])
        ok, cex = SO.check_rule(lambda x: x / 2, lambda x: x >> 1)
        self.assertFalse(ok)
        self.assertEqual((cex[0] // 2 if cex[0] >= 0 else -((-cex[0]) // 2)) == cex[0] >> 1, False)


if __name__ == "__main__":
    unittest.main()
