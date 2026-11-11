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

    def test_optimizer_keeps_guarded_loads_guarded(self):
        # The loop is entered, but its inner condition is false. Hoisting *p
        # would introduce a trap into this well-typed, defined source program.
        src = """
        fn guarded(p: *int, n: int) -> int {
            var i: int = 0;
            var total: int = 0;
            while i < n {
                if i == 1 { total = total + *p; }
                i = i + 1;
            }
            return total;
        }
        fn main() -> int { return guarded(null, 1); }
        """
        for rotate in (False, True):
            with self.subTest(rotate=rotate):
                m = module(src, rotate)
                self.assertEqual(IT.run(m).result, 0)
                for f in m.funcs:
                    S.to_ssa(f)
                    O.optimize(f)
                    S.from_ssa(f)
                self.assertEqual(IT.run(m).result, 0)

    def test_licm_respects_overlapping_access_widths(self):
        from explainer.cs.lang.compiler.ir import Block, Func, I, Module

        # Load in the header, not a conditional body: the alias rule itself
        # must reject hoisting, independently of the control-flow restriction.
        for store_width, load_width in ((1, 4), (4, 1)):
            with self.subTest(store=store_width, load=load_width):
                m = Module([Func('main', [], [
                    Block('entry', [I('gaddr', '%p', k='word'), I('br', k='header')]),
                    Block('header', [I('phi', '%i', [0, '%next'], ['entry', 'body']),
                                     I('phi', '%sum', [0, '%acc'], ['entry', 'body']),
                                     I('load', '%word', ['%p'], (load_width, 0)),
                                     I('bin', '%more', ['%i', 2], 'lt'),
                                     I('cbr', args=['%more'], k=('body', 'exit'))]),
                    Block('body', [I('bin', '%acc', ['%sum', '%word'], 'add'),
                                   I('bin', '%next', ['%i', 1], 'add'),
                                   I('store', args=['%p', '%next'], k=(store_width, 0)),
                                   I('br', k='header')]),
                    Block('exit', [I('ret', args=['%sum'])]),
                ])], {'word': (4, 4, 0)})
                self.assertEqual(IT.run(m).result, 1)
                O.licm(m.funcs[0])
                self.assertEqual(IT.run(m).result, 1)

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



class CacheSafety(unittest.TestCase):
    def test_compiler_cache_entry_and_cli_revision_checks(self):
        import contextlib
        import hashlib
        import io
        import json
        import sys
        import tempfile
        from pathlib import Path
        from unittest.mock import patch
        from tools.qa_series import StaleDataError, require_current_cache
        from videos.cs.cs13 import compute as C13

        calls = []
        def produce():
            calls.append(True)
            return {"observed": 7}

        with tempfile.TemporaryDirectory() as folder:
            cache = C13.CompilerCache("cs13")
            cache.dir = Path(folder)
            with patch.object(C13, "CACHE", cache), patch.dict(C13.ITEMS, {"passes": produce}):
                target = cache.path("passes")
                target.write_text('{"observed": 99}')
                original = hashlib.sha256(target.read_bytes()).hexdigest()
                with self.assertRaises(StaleDataError):
                    require_current_cache(C13, "cs13", target, "passes")
                self.assertEqual(calls, [])
                self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), original)
                with patch.object(sys, "argv", ["compute.py", "passes"]), contextlib.redirect_stdout(io.StringIO()):
                    cache.main(C13.ITEMS)
                    cache.main(C13.ITEMS)
                self.assertEqual(len(calls), 1)
                self.assertTrue(C13.cache_current("passes"))
                self.assertEqual(C13.load("passes")["observed"], 7)
                data = json.loads(target.read_text())
                data["_compiler_data_revision"] = "a different compiler revision"
                target.write_text(json.dumps(data))
                before_rejection = target.read_bytes()
                with self.assertRaises(StaleDataError):
                    require_current_cache(C13, "cs13", target, "passes")
                self.assertEqual(target.read_bytes(), before_rejection)
                self.assertEqual(len(calls), 1)
                self.assertEqual(C13.load("passes")["observed"], 7)
                self.assertEqual(len(calls), 2)
                self.assertTrue(C13.cache_current("passes"))


if __name__ == "__main__":
    unittest.main()
