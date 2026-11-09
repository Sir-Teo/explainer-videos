"""Computer Science, Built, Part 3: the circuits behind the scenes, and the problem answers."""

import itertools
import unittest

import numpy as np

from explainer.cs.pebble.hdl import Circuit, exhaustive
from videos.cs.cs3 import compute as c


class Part3(unittest.TestCase):
    def test_post(self):
        rows = {r["name"]: r for r in c.compute_post()["rows"]}
        self.assertTrue(rows["NAND"]["complete"] and rows["NOR"]["complete"])
        self.assertFalse(rows["AND"]["complete"] or rows["XOR"]["complete"])
        xor_and = [t for t in c.NAMES if c.NAMES[t] in ("XOR", "AND")]
        self.assertFalse(c.complete(xor_and))
        self.assertTrue(c.complete(xor_and + [0b1111]))  # problem 2

    def test_nandmin(self):
        got = {r["name"]: r["nands"] for r in c.compute_nandmin()["rows"]}
        self.assertEqual((got["NOT x"], got["AND"], got["OR"], got["XOR"], got["XNOR"]), (1, 2, 3, 4, 5))

    def test_kmap_problem_3(self):
        m = [1, 3, 4, 5, 9, 11, 12, 13]
        primes = c.quine_mccluskey(m, 4)
        self.assertEqual(sorted(c.term_str(p, 4) for p in primes), ["B'D", "BC'", "C'D"])
        cover = [p for p in primes if c.term_str(p, 4) in ("B'D", "BC'")]  # C'D is a prime but redundant
        self.assertTrue(all((x in m) == any(c.covers(p, x) for p in cover) for x in range(16)))

    def test_monotone_count_problem_4(self):
        pts = list(itertools.product((0, 1), repeat=3))
        n = sum(1 for tt in range(256) if all(
            (tt >> (4 * a[0] + 2 * a[1] + a[2])) & 1 <= (tt >> (4 * b[0] + 2 * b[1] + b[2])) & 1
            for a in pts for b in pts if all(x <= y for x, y in zip(a, b))))
        self.assertEqual(n, 20)

    def test_hand_nand_mux_problem_6(self):
        k = Circuit("4-to-1 mux in NANDs")
        d = k.input("d", 4)
        s = k.input("s", 2)

        def mux(sel, nsel, a, b):
            return k.nand(k.nand(a, nsel), k.nand(b, sel))

        ns0, ns1 = k.nand(s[0], s[0]), k.nand(s[1], s[1])
        lo, hi = mux(s[0], ns0, d[0], d[1]), mux(s[0], ns0, d[2], d[3])
        k.output("y", mux(s[1], ns1, lo, hi))
        self.assertEqual(k.counts()["NAND"], 11)
        c.check(k, lambda i: {"y": (i["d"] >> i["s"]) & 1})
        self.assertEqual(c.mux_n(2).to_nand().counts()["NAND"], 24)

    def test_blocks_verified(self):
        rows = {r["name"]: r for r in c.compute_blocks()["rows"]}
        self.assertEqual(rows["4-bit comparator"]["gates"], 21)
        self.assertEqual(rows["8-bit parity tree"]["depth"], 3)

    def test_census_includes_one_gate_negations(self):
        # Independent one-gate oracle: evaluate all 16 gate truth tables by row.
        # Constants/input wires cost zero; both pins may choose the same wire.
        full = 255
        inputs = [sum(1 << row for row in range(8) if row >> bit & 1) for bit in range(3)]
        free = {0, full, *inputs}
        one_gate = set(free)
        for a, b, table in itertools.product(free, free, range(16)):
            one_gate.add(sum(((table >> (2 * ((a >> row) & 1) + ((b >> row) & 1))) & 1) << row
                             for row in range(8)))
        got = c.compute_census()
        self.assertEqual(got["not_costs"], [1, 1, 1])
        self.assertEqual(got["hist"][1], len(one_gate - free))
        self.assertEqual(got["hist"], [5, 33, 114, 80, 24])
        # Full independent enumeration saved with the QA evidence packet.
        self.assertEqual(got["states"], [33, 828, 20360, 528991])
        self.assertEqual(sum(got["hist"]), 256)

    def test_bdd_orders(self):
        out = c.compute_bdd()
        self.assertTrue(all(r["good"] == 2 * r["k"] + 2 and r["bad"] == 2 ** (r["k"] + 1) for r in out["rows"]))

    def test_hazard(self):
        g = c.compute_glitch()
        self.assertIn(0, g["before"]["f"])
        self.assertNotIn(0, g["after"]["f"])


if __name__ == "__main__":
    unittest.main()
