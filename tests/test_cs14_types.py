"""Part 14: the λ-calculus strategies, the simply typed calculus and its safety theorems, Hindley–Milner inference
and the Job in the λ-core, and propositions as types."""
import unittest

from explainer.cs.lam import App, Var, alpha_eq, church, parse, unchurch
from explainer.cs.lang.lam import logic as LG
from explainer.cs.lang.lam import ml as M
from explainer.cs.lang.lam import reduce as R
from explainer.cs.lang.lam import stlc as S
from explainer.cs.pebble import programs as PR

TEXT = ("It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want "
        "of a wife. However little known the feelings or views of such a man may be on his first entering a "
        "neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered "
        "the rightful property of some one or other of their daughters. ") * 2


class Untyped(unittest.TestCase):
    def test_church_arithmetic(self):
        L = R.lib
        for m in range(4):
            for n in range(4):
                for op, f in (("plus", m + n), ("times", m * n)):
                    k, t = R.run(R.apply(L(op), church(m), church(n)))
                    self.assertEqual(unchurch(t), f)
            k, t = R.run(R.apply(L("pred"), church(m)))
            self.assertEqual(unchurch(t), max(m - 1, 0))

    def test_strategies_and_sharing(self):
        t = R.apply(parse(r"\x y. x"), Var("a"), R.lib("omega"))
        self.assertEqual(R.run(t, "normal")[0], 2)
        self.assertIsNone(R.run(t, "applicative", max_steps=200)[0])
        dbl = R.apply(parse(r"\pl x. pl x (pl x x)"), R.lib("plus"))
        arg = R.apply(R.lib("times"), church(3), church(3))
        name = R.read_number(R.apply(dbl, arg), "name")
        need = R.read_number(R.apply(dbl, arg), "need")
        self.assertEqual(name[0], need[0])
        self.assertEqual(name[0], 27)
        self.assertGreater(name[1]["beta"], need[1]["beta"])

    def test_confluence(self):
        for src in (r"(\x. x x) ((\y. y) z)", r"(\x y. y x) ((\a. a) b) ((\c. c) d)"):
            self.assertTrue(R.confluent(parse(src)))
            nodes, _, normal = R.graph(parse(src))
            self.assertEqual(len(normal), 1)


class Typed(unittest.TestCase):
    def test_typing_and_eval(self):
        t = S.parse(r"(\f:Nat->Nat. \x:Nat. f (f x)) (\y:Nat. succ y) 3")
        T, d = S.typecheck(t)
        self.assertEqual(T, S.NAT)
        self.assertEqual(S.show(S.trace(t)[-1][0]), "5")

    def test_safety(self):
        r = S.safety(300, 5, seed=3)
        self.assertTrue(r["all_terminated"])

    def test_stuck_terms_are_ill_typed(self):
        for e in S.stuck_examples():
            self.assertFalse(e["value"])
            self.assertIsNotNone(e["type_error"])


class Inference(unittest.TestCase):
    def test_principal_types(self):
        cases = {"fun x -> x": "'a -> 'a", "fun f -> fun x -> f (f x)": "('a -> 'a) -> 'a -> 'a",
                 "fun f g x -> f (g x)": "('a -> 'b) -> ('c -> 'a) -> 'c -> 'b",
                 "let id = fun x -> x in (id 1, id true)": "int * bool"}
        for src, want in cases.items():
            t, _ = M.infer_expr(M.parse_expr(src))
            self.assertEqual(M.show_type(t), want, src)
        with self.assertRaises(M.TypeErr):
            M.infer_expr(M.parse_expr("fun x -> x x"))
        with self.assertRaises(M.TypeErr):
            M.infer_expr(M.parse_expr("fun f -> (f 1, f true)"))

    def test_job_in_the_core(self):
        tape = PR.job_tape(TEXT)
        prog = M.parse(M.JOB_ML + "\n;; job text")
        types, body, _ = M.infer_program(prog, env={"text": M.T("list", M.INT)})
        self.assertIn(("bump", "'a -> ('a * int) list -> ('a * int) list"), types)
        r = M.evaluate(prog, env={"text": M.from_list(list(tape))})
        self.assertEqual(M.job_output(r), PR.job_reference(tape))

    def test_exponential_types(self):
        sizes = [M.type_size(M.infer_expr(M.parse_expr(M.exp_let(n)))[0]) for n in range(1, 5)]
        self.assertEqual(sizes, [2 ** (2 ** n) + 1 for n in range(1, 5)])


class CurryHoward(unittest.TestCase):
    def test_table(self):
        rows = {r["name"]: r for r in LG.table()}
        for r in rows.values():
            self.assertTrue(r["classical"])
            self.assertTrue((r["program"] is None) != (r["countermodel"] is None), r["name"])
        for name in ("excluded middle", "double negation elim", "Peirce's law"):
            self.assertIsNone(rows[name]["program"])
        self.assertIsNotNone(rows["not not excluded middle"]["program"])


if __name__ == "__main__":
    unittest.main()
