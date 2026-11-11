"""Part 12: the regex engines, the automata constructions, the grammar algorithms and the Pebble language front
end, each checked against something that does not share its code (Python's re, brute-force enumeration, known
textbook counts)."""
import itertools
import random
import re
import unittest

from explainer.cs.lang import automata as A
from explainer.cs.lang import grammar as G
from explainer.cs.lang import pebble_lang as P
from explainer.cs.lang import regex as R

PATTERNS = ["a(b|c)*d", "(a|b)*abb", "[a-c]+x?", "(ab|a)*", "a.c", "(a*)*b", "x[^ab]y", "", "(a|ε)b".replace("ε", ""),
            "((a|b)(a|b))*", "a+b+|c"]


class Regex(unittest.TestCase):
    def test_engines_agree_with_python(self):
        rng = random.Random(12)
        for p in PATTERNS:
            n = R.parse(p)
            m = R.thompson(n)
            d = A.minimize(A.subset(m, "abcdxy"))
            for _ in range(400):
                s = "".join(rng.choice("abcdxy") for _ in range(rng.randint(0, 8)))
                want = re.fullmatch(p, s) is not None
                self.assertEqual(m.run(s)[0], want, (p, s))
                self.assertEqual(R.backtrack(n, s)[0], want, (p, s))
                self.assertEqual(R.matches_by_derivatives(n, s), want, (p, s))
                self.assertEqual(d.run(s), want, (p, s))

    def test_control_character_escapes_against_python(self):
        for pattern in [r"\n", r"\r", r"\t", r"[\n\r\t]+", r"a\nb", r"\n|\r"]:
            node = R.parse(pattern)
            nfa = R.thompson(node)
            dfa = A.from_regex(pattern, "abnrt\n\r\t")
            for text in ["", "n", "r", "t", "\n", "\r", "\t", "\n\r", "a\nb", "anb"]:
                expected = re.fullmatch(pattern, text) is not None
                with self.subTest(pattern=pattern, text=text):
                    self.assertEqual(nfa.run(text)[0], expected)
                    self.assertEqual(R.backtrack(node, text)[0], expected)
                    self.assertEqual(R.matches_by_derivatives(node, text), expected)
                    self.assertEqual(dfa.run(text), expected)

    def test_search(self):
        m = R.compile("ab+c")
        self.assertTrue(m.search("xxabbbcyy")[0])
        self.assertFalse(m.search("xxabbbyy")[0])

    def test_backtracking_blows_up_and_thompson_does_not(self):
        n = R.parse("(a+)+b")
        steps = [R.backtrack(n, "a" * k)[1] for k in (8, 10, 12)]
        self.assertGreater(steps[1], 3.5 * steps[0])
        self.assertGreater(steps[2], 3.5 * steps[1])
        work = [R.thompson(n).run("a" * k)[1] for k in (100, 200)]
        self.assertLess(work[1], 2.2 * work[0])

    def test_backreferences(self):
        n = R.parse(r"(a*)b\1")
        self.assertTrue(R.backtrack(n, "aabaa")[0])
        self.assertFalse(R.backtrack(n, "aaba")[0])
        with self.assertRaises(R.RegexError):
            R.thompson(n)


class Automata(unittest.TestCase):
    def test_wildcard_determinization_requires_an_alphabet(self):
        for pattern in [".", "[^a]", "a.*b"]:
            with self.subTest(pattern=pattern):
                with self.assertRaisesRegex(ValueError, "explicit finite alphabet"):
                    A.from_regex(pattern)
                dfa = A.from_regex(pattern, "abx")
                for n in range(4):
                    for text in map("".join, itertools.product("abx", repeat=n)):
                        self.assertEqual(dfa.run(text), re.fullmatch(pattern, text) is not None)

    def test_boolean_products_with_different_alphabets(self):
        a, b = A.from_regex("a+"), A.from_regex("b+")
        for operation in [lambda x,y:x and y, lambda x,y:x or y,
                          lambda x,y:x != y, lambda x,y:x and not y]:
            combined = A.product(a, b, operation)
            self.assertEqual(set(combined.alphabet), {"a", "b"})
            for n in range(4):
                for text in map("".join, itertools.product("ab", repeat=n)):
                    left = re.fullmatch("a+", text) is not None
                    right = re.fullmatch("b+", text) is not None
                    self.assertEqual(combined.run(text), operation(left, right), text)

    def test_nth_from_end_needs_two_to_the_n(self):
        for n in range(1, 9):
            nfa = R.compile(A.nth_from_end(n))
            m = A.minimize(A.subset(nfa, "01"))
            self.assertEqual(m.n, 2 ** n)
            for w in map("".join, itertools.product("01", repeat=n + 2)):
                self.assertEqual(m.run(w), w[-n] == "1")

    def test_myhill_nerode_witness(self):
        n = 4
        m = A.minimize(A.from_regex(A.nth_from_end(n), "01"))
        for u, v in itertools.combinations(map("".join, itertools.product("01", repeat=n)), 2):
            z = A.distinguishing_suffix(u, v, n)
            self.assertNotEqual(m.run(u + z), m.run(v + z))

    def test_state_elimination_round_trip(self):
        for p in ["(a|b)*abb", "a(b|c)*d", "(ab|a)*", "(a|b)*a(a|b)"]:
            m = A.minimize(A.from_regex(p))
            back = A.minimize(A.from_regex(A.to_regex(m).replace("|)", "|ε)"), m.alphabet))
            self.assertTrue(A.equivalent(m, back)[0], p)

    def test_minimal_is_unique(self):
        a = A.minimize(A.from_regex("(a|b)*abb"))
        b = A.minimize(A.from_regex("(b|a)*(ab)b|((a|b)*a)(ab)b"))     # the same language, written differently
        self.assertEqual((a.n, b.n), (4, 4))
        self.assertTrue(A.equivalent(a, b)[0])
        c = A.minimize(A.from_regex("(a|b)*ab"))
        ok, witness = A.equivalent(a, c)
        self.assertFalse(ok)
        self.assertNotEqual(a.run(witness), c.run(witness))


EXPR = """
E -> E + T | T
T -> T * F | F
F -> ( E ) | id
"""


class Grammars(unittest.TestCase):
    def test_first_follow(self):
        g = G.Grammar.parse(EXPR)
        self.assertEqual(g.first()["E"], {"(", "id"})
        self.assertEqual(g.follow()["T"], {"+", "*", ")", "$"})

    def test_ll1_after_removing_left_recursion(self):
        g = G.Grammar.parse(EXPR)
        self.assertTrue(G.ll1_table(g)[1])
        g2 = G.remove_left_recursion(g)
        self.assertFalse(G.ll1_table(g2)[1])
        self.assertTrue(G.ll1_parse(g2, "id + id * ( id + id )".split()))
        self.assertFalse(G.ll1_parse(g2, "id + * id".split()))

    def test_lr_family_textbook_counts(self):
        g = G.Grammar.parse(EXPR).augmented()
        s0, t0 = G.lr0_automaton(g)
        s1, t1 = G.lr1_automaton(g)
        sl, tl = G.lalr_automaton(g)
        self.assertEqual((len(s0), len(s1), len(sl)), (12, 22, 12))
        self.assertTrue(G.lr_table(g, s0, t0, "lr0")[2])          # LR(0) has conflicts
        a, go, cf = G.lr_table(g, s0, t0, "slr")
        self.assertFalse(cf)
        self.assertTrue(G.lr_parse(g, a, go, "id * ( id + id )".split()))
        self.assertFalse(G.lr_parse(g, a, go, "id * + id".split()))

    def test_lalr_but_not_slr(self):
        g = G.Grammar.parse("""
S -> L = R | R
L -> * R | id
R -> L
""").augmented()
        s0, t0 = G.lr0_automaton(g)
        self.assertTrue(G.lr_table(g, s0, t0, "slr")[2])
        sl, tl = G.lalr_automaton(g)
        self.assertFalse(G.lr_table(g, sl, tl, "lr1")[2])

    def test_ambiguity_is_catalan(self):
        g = G.to_cnf(G.Grammar.parse("E -> E + E | E * E | id"))
        cat = [1, 1, 2, 5, 14, 42, 132, 429]
        for n in range(1, 9):
            toks = " + ".join(["id"] * n).split()
            self.assertEqual(G.cyk(g, toks)[1], cat[n - 1])

    def test_cyk_and_earley_agree_with_brute_force(self):
        text = "S -> a S b | S S | ε"
        g = G.Grammar.parse(text)
        cnf = G.to_cnf(g)

        def balanced(w):
            d = 0
            for c in w:
                d += 1 if c == "a" else -1
                if d < 0:
                    return False
            return d == 0
        for k in range(0, 9):
            for w in itertools.product("ab", repeat=k):
                want = balanced(w)
                self.assertEqual(G.cyk(cnf, list(w))[1] > 0, want, w)
                self.assertEqual(G.earley(g, list(w))[0], want, w)


class PebbleLanguage(unittest.TestCase):
    def test_lexer_maximal_munch(self):
        kinds = [t.kind for t in P.lex("a->b >= c > = d==e // done\n x")]
        self.assertEqual(kinds, ["ident", "->", "ident", ">=", "ident", ">", "=", "ident", "==", "ident", "ident",
                                 "$"])
        self.assertEqual([t.kind for t in P.lex("while whiles")], ["while", "ident", "$"])

    def test_precedence_and_associativity(self):
        cases = {"a + b * c - d": "((a + (b * c)) - d)", "1 - 2 - 3": "((1 - 2) - 3)",
                 "a < b == c && d || e": "((((a < b) == c) && d) || e)", "-x.f[2] * *p": "((-x.f[2]) * (*p))",
                 "!f(x, y + 1)[3].g": "(!f(x, (y + 1))[3].g)"}
        for src, want in cases.items():
            self.assertEqual(P.show(P.parse_expr(src)), want)

    def test_the_job_parses_both_ways(self):
        prog = P.parse(P.JOB)
        self.assertEqual([f.name for f in prog.funcs], ["same", "lookup", "printnum", "report", "main"])
        g = G.Grammar.parse(P.BNF).augmented()
        s, t = G.lalr_automaton(g)
        a, go, cf = G.lr_table(g, s, t, "lr1")
        self.assertFalse(cf)
        self.assertTrue(G.lr_parse(g, a, go, [tk.kind for tk in P.lex(P.JOB)[:-1]]))

    def test_errors_name_the_place(self):
        with self.assertRaises(P.ParseError) as e:
            P.parse("fn f() { var x: int = ; }")
        self.assertIn("line 1", str(e.exception))


if __name__ == "__main__":
    unittest.main()
