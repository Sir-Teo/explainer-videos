"""The machines of Computer Science, Built, Part 1, and the answers to its problems."""

import itertools
import unittest

from explainer.cs import lam
from explainer.cs.turing import BLANK, CHAMPIONS, TM, run, run_fast
from videos.cs.cs1.machines import (ADD3, PALINDROME, PALINDROME2, UNARY_ADD, compile_two_counters, encode, godel,
                                    run_universal, single_tape_cost, ungodel)

# Problem 1: binary increment, head on the leftmost digit
INCREMENT = TM([
    ("A", "0", "0", "R", "A"),
    ("A", "1", "1", "R", "A"),
    ("A", BLANK, BLANK, "L", "C"),
    ("C", "1", "0", "L", "C"),
    ("C", "0", "1", "S", "H"),
    ("C", BLANK, "1", "S", "H"),
], start="A", name="binary increment")


class Part1Machines(unittest.TestCase):
    def test_unary_add(self):
        r = run(UNARY_ADD, "111+11")
        self.assertTrue(r.halted)
        self.assertEqual(r.tape(0).strip(BLANK), "11111")

    def test_palindromes_one_and_two_tapes(self):
        for n in range(0, 9):
            for w in map("".join, itertools.product("01", repeat=n)):
                want = "accept" if w == w[::-1] else "reject"
                self.assertEqual(run(PALINDROME, w).state, want, w)
                two = run(PALINDROME2, (w, ""))
                self.assertEqual(two.state, want, w)
                self.assertEqual(two.steps, 3 * n + 3, w) if want == "accept" else None

    def test_single_tape_simulation_runs_the_same_machine(self):
        c = single_tape_cost(PALINDROME2, ("0110", ""))
        self.assertEqual(c["steps"], run(PALINDROME2, ("0110", "")).steps)
        self.assertEqual(c["state"], "accept")
        self.assertGreater(c["moves"], c["steps"])

    def test_universal_machine_on_champions(self):
        for n in (2, 3, 4):
            m = TM.parse(CHAMPIONS[n][0])
            direct = run(m)
            u = run_universal(m)
            self.assertTrue(u.halted)
            self.assertEqual(direct.steps, CHAMPIONS[n][1])
            self.assertEqual(u.tape(1), direct.tape(0))
            self.assertEqual(u.ones(1), CHAMPIONS[n][2])
        self.assertEqual(run_universal(TM.parse(CHAMPIONS[4][0])).steps, 13_938)  # problem 6
        self.assertTrue(encode(TM.parse(CHAMPIONS[2][0])).endswith("#"))

    def test_fast_runner_matches_the_reference(self):
        for n in (2, 3, 4):
            m = TM.parse(CHAMPIONS[n][0])
            f = run_fast(m, 10_000)
            self.assertTrue(f["halted"])
            self.assertEqual((f["steps"], f["ones"]), CHAMPIONS[n][1:3])

    def test_two_counters_compute_what_three_do(self):
        two = compile_two_counters(ADD3)
        for a, b in ((0, 0), (1, 2), (3, 4)):
            r = two.run([godel([a, b, 0]), 0])
            self.assertEqual(ungodel(r["regs"][0], 3), ADD3.run([a, b])["regs"])
            self.assertEqual(r["regs"][1], 0)

    def test_lambda_arithmetic(self):
        def norm(op, a, b):
            t = lam.parse(f"({getattr(lam, op)}) ({lam.show(lam.church(a))}) ({lam.show(lam.church(b))})")
            return lam.normalize(t)

        plus = norm("PLUS", 2, 3)
        self.assertEqual(lam.unchurch(plus[-1].term), 5)
        self.assertEqual(len(plus) - 1, 6)
        times = norm("TIMES", 2, 2)  # problem 5
        self.assertEqual(lam.unchurch(times[-1].term), 4)
        self.assertEqual(len(times) - 1, 7)

    def test_problem_1_increment(self):
        for n in range(1, 8):
            r = run(INCREMENT, "1" * n)
            self.assertEqual(r.tape(0), "1" + "0" * n)
            self.assertEqual(r.steps, 2 * n + 2)
        for k in range(0, 40):
            r = run(INCREMENT, format(k, "b"))
            self.assertEqual(int(r.tape(0), 2), k + 1)


if __name__ == "__main__":
    unittest.main()
