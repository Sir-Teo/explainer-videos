import contextlib
import io
import unittest

from explainer.cs.algo import computability as C


class Computability(unittest.TestCase):
    def test_quines(self):
        q = C.python_quine()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec(q, {})
        self.assertEqual(buf.getvalue(), q)

    def test_pebble_quine(self):
        from explainer.cs.lang.compiler import driver as Dr
        src = C.pebble_quine()
        r = Dr.run(Dr.compile_program(src, 2), b"")
        self.assertEqual(bytes(r.output).decode(), src)

    def test_pcp(self):
        seq, _ = C.pcp_solve([("b", "ca"), ("a", "ab"), ("ca", "a"), ("abc", "c")], 10)
        D = [("b", "ca"), ("a", "ab"), ("ca", "a"), ("abc", "c")]
        self.assertEqual("".join(D[i][0] for i in seq), "".join(D[i][1] for i in seq))
        seq, _ = C.pcp_solve([("ab", "a"), ("ba", "b")], 8)
        self.assertIsNone(seq)     # the top always stays longer

    def test_tm_reduction(self):
        # a machine that accepts strings starting with 1: q reads 1 -> accept
        rules = {("q", "1"): ("a", "1", "R"), ("q", "0"): ("r", "0", "R"), ("q", "_"): ("r", "_", "R")}
        D = C.tm_to_mpcp(rules, "q", "a", "10", "01")
        seq, _ = C.pcp_solve(D, 40, first=0)
        self.assertIsNotNone(seq)
        top = "".join(D[i][0] for i in seq)
        self.assertTrue(top.startswith(C.run_tm_history(rules, "q", "a", "10")))

    def test_wang(self):
        g, _, _ = C.wang_tile(C.JEANDEL_RAO, 10, 10)
        self.assertIsNotNone(g)
        T = C.JEANDEL_RAO
        for r in range(10):
            for c in range(10):
                if c:
                    self.assertEqual(T[g[r][c - 1]][1], T[g[r][c]][3])
                if r:
                    self.assertEqual(T[g[r - 1][c]][2], T[g[r][c]][0])
        for n in range(1, 5):
            g, _, done = C.wang_tile(T, n, n, periodic=True)
            self.assertIsNone(g)
            self.assertTrue(done)

    def test_numbers(self):
        self.assertEqual(C.pell(61), (1766319049, 226153980))
        self.assertEqual([p for _, p in C.fractran(C.PRIMEGAME, 2, 3000)], [2, 3, 5, 7, 11])
        self.assertEqual(C.collatz(27), (111, 9232))
        self.assertEqual(C.pi_digits(10), "3141592653")
        self.assertAlmostEqual(C.shoelace(C.hat_polygon()), 8 * 3 ** 0.5)


if __name__ == "__main__":
    unittest.main()
