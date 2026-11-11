import contextlib
import io
import unittest
import itertools
from fractions import Fraction

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
        self.assertEqual(top, "".join(D[i][1] for i in seq))
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

    def test_search_boundaries_and_independent_shortest_matches(self):
        self.assertEqual(C.pcp_search([('a','a')],0)['status'],'depth-limit')
        self.assertIsNone(C.pcp_search([('a','a')],0)['match'])
        self.assertEqual(C.pcp_search([('a','a')],max_nodes=0)['status'],'node-limit')
        self.assertEqual(C.pcp_search([('a','b')])['status'],'exhausted')
        self.assertEqual(C.pcp_search([('a','aa')],4)['status'],'depth-limit')
        for first in (-1,1,True):
            with self.assertRaises(ValueError):C.pcp_search([('a','a')],first=first)
        words=['0','1','01']
        pairs=list(itertools.product(words,repeat=2))
        for D in itertools.combinations(pairs,2):
            expected=None
            for n in range(1,5):
                if any(''.join(D[i][0] for i in s)==''.join(D[i][1] for i in s)
                       for s in itertools.product(range(2),repeat=n)):
                    expected=n;break
            r=C.pcp_search(D,4)
            self.assertEqual(len(r['match']) if r['match'] else None,expected)

    def test_tm_status_and_left_boundary_model(self):
        rules={('q','1'):('a','1','L')}
        r=C.run_tm_trace(rules,'q','a','1')
        self.assertEqual(r['status'],'rejected-left-boundary')
        D=C.tm_to_mpcp(rules,'q','a','1','1')
        self.assertIsNone(C.pcp_search(D,20,first=0)['match'])
        rules={('q','1'):('a','1','R')}
        r=C.run_tm_trace(rules,'q','a','1',0)
        self.assertEqual(r['status'],'step-limit')
        self.assertEqual(len(r['configurations']),1)
        self.assertEqual(C.run_tm_trace({},'q','a','1')['status'],'rejected-missing-rule')
        with self.assertRaises(ValueError):C.tm_to_mpcp(rules,'q','1','1','1')

    def test_wang_budget_and_wrap(self):
        self.assertEqual(C.wang_tile([(0,0,0,0)],2,2,limit=0),(None,0,False))
        g,n,done=C.wang_tile([(0,0,0,0)],2,2,limit=4,periodic=True)
        self.assertTrue(done);self.assertEqual(n,4);self.assertEqual(g,[[0,0],[0,0]])
        self.assertEqual(C.wang_tile([(0,1,0,0)],1,1,periodic=True),(None,1,True))
        for n,m in [(0,2),(2,-1),(True,1)]:
            with self.assertRaises(ValueError):C.wang_tile([],n,m)

    def test_positive_domains_and_finite_run_status(self):
        for n in (0,-1,1.0,True):
            with self.assertRaises(ValueError):C.collatz(n)
            with self.assertRaises(ValueError):C.fractran([Fraction(1)],n,3)
        with self.assertRaises(TimeoutError):C.collatz(27,10)
        self.assertEqual(C.collatz(1,0),(0,1))
        trace=[];r=C.fractran_run([Fraction(3,2)],2,10,trace=trace)
        self.assertEqual((r['status'],r['steps'],r['final'],trace),('halted',1,3,[0]))
        self.assertEqual(C.fractran_run([Fraction(1)],2,0)['status'],'step-limit')
        with self.assertRaises(ValueError):C.fractran([Fraction(-1)],2,2)
        for fn in (C.pi_digits,C.thue_morse):
            with self.assertRaises(ValueError):fn(-1)
            self.assertEqual(fn(0),'')
        for D in (0,-2,2.0,True):
            with self.assertRaises(ValueError):C.pell(D)
        self.assertIsNone(C.pell(4))
        with self.assertRaises(ValueError):C.shoelace([])

    def test_backward_quine_exercise(self):
        from explainer.cs.lang.compiler import driver as Dr
        src=C.pebble_backward_quine();r=Dr.run(Dr.compile_program(src,2),b'')
        self.assertEqual(bytes(r.output),src.encode()[::-1])

    def test_wrapped_producer_preserves_displayed_quine(self):
        from videos.cs.cs25 import compute as M
        data=M.ITEMS['quines']()
        self.assertEqual(data['python'],C.python_quine())
        self.assertIn('python_version',data)
        with self.assertRaises(AssertionError):M._producer('collision',lambda:dict(schema=99))()


if __name__ == "__main__":
    unittest.main()
