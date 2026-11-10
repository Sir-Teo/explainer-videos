"""Part 19's instruments against brute force and known values."""

from __future__ import annotations

import math
import random
import sys
import unittest
from itertools import combinations

import numpy as np

from explainer.cs.algo import paradigms as P


class Greedy(unittest.TestCase):
    def test_activity_selection_is_optimal(self):
        rng = random.Random(1)
        for _ in range(200):
            ivs = []
            for _ in range(rng.randrange(1, 14)):
                s = rng.randrange(0, 40)
                ivs.append((s, s + rng.randrange(1, 12)))
            self.assertEqual(len(P.activity_selection(ivs, "finish")), P.max_compatible(ivs))

    def test_huffman_kraft_and_optimality(self):
        freq = {"a": 45, "b": 13, "c": 12, "d": 16, "e": 9, "f": 5}         # CLRS's example: cost 224
        L = P.huffman(freq)
        self.assertAlmostEqual(sum(2.0 ** -l for l in L.values()), 1.0)
        self.assertEqual(sum(freq[s] * L[s] for s in freq), 224)

    def test_coins(self):
        self.assertEqual(len(P.coin_greedy(6, [1, 3, 4])), 3)
        self.assertEqual(len(P.coin_dp(6, [1, 3, 4])), 2)

    def test_matroid_greedy_on_forests(self):
        rng = random.Random(2)
        n = 6
        edges = [(u, v, rng.random()) for u, v in combinations(range(n), 2)]
        g = P.greedy_max_weight(edges, lambda e: e[2], P.forest_independent(n))
        best = 0
        for k in range(n):
            for sub in combinations(edges, k):
                if P.forest_independent(n)(list(sub)):
                    best = max(best, sum(e[2] for e in sub))
        self.assertAlmostEqual(sum(e[2] for e in g), best)


class Multiply(unittest.TestCase):
    def test_karatsuba(self):
        rng = random.Random(3)
        for _ in range(50):
            x, y = rng.randrange(10 ** 60), rng.randrange(10 ** 45)
            c = [0]
            out = P.karatsuba(P.to_digits(x), P.to_digits(y), c)
            self.assertEqual(P.from_digits(P._carry(out)), x * y)

    def test_karatsuba_count(self):
        for k in range(1, 8):
            n = 2 ** k
            c = [0]
            P.karatsuba([9] * n, [9] * n, c)
            self.assertEqual(c[0], 3 ** k)

    def test_strassen(self):
        rng = np.random.default_rng(4)
        A, B = rng.standard_normal((128, 128)), rng.standard_normal((128, 128))
        self.assertTrue(np.allclose(P.strassen(A, B, cutoff=16), A @ B))
        self.assertEqual(P.strassen_counts(8)[0], 7 ** 3)

    def test_fft(self):
        rng = random.Random(5)
        a = [complex(rng.random(), rng.random()) for _ in range(64)]
        self.assertTrue(np.allclose(P.fft(a), P.dft(a)))
        self.assertTrue(np.allclose(P.ifft(P.fft(a)), a))
        self.assertEqual(P.poly_mul_fft([1, 2, 3], [4, 5]), [4, 13, 22, 15])

    def test_ntt_and_bigmul(self):
        a = [3, 1, 4, 1, 5, 9, 2, 6]
        self.assertEqual(P.ntt(P.ntt(a), invert=True), a)
        rng = random.Random(6)
        x, y = rng.randrange(10 ** 5000), rng.randrange(10 ** 4000)
        self.assertEqual(P.fft_bigmul(x, y), x * y)

    def test_pi(self):
        self.assertEqual(str(P.chudnovsky(50)), "314159265358979323846264338327950288419716939937510")


class DivideAndDP(unittest.TestCase):
    def test_closest_pair(self):
        rng = random.Random(7)
        pts = [(rng.random(), rng.random()) for _ in range(300)]
        d, _, n, k = P.closest_pair(pts)
        self.assertAlmostEqual(d, P.closest_brute(pts)[0])
        self.assertLess(n, 300 * 299 // 2 // 5)
        self.assertLessEqual(k, 7)

    def test_edit_distance(self):
        D, ops, _ = P.edit_distance("kitten", "sitting")
        self.assertEqual(D[-1][-1], 3)
        self.assertEqual(sum(o != "=" for o in ops), 3)
        self.assertEqual(P.lcs("ABCBDAB", "BDCABA")[0], 4)

    def test_knapsack(self):
        rng = random.Random(8)
        items = [(rng.randrange(1, 20), rng.randrange(1, 30)) for _ in range(12)]
        W = 50
        best = 0
        for mask in range(1 << len(items)):
            w = sum(items[i][0] for i in range(len(items)) if mask >> i & 1)
            if w <= W:
                best = max(best, sum(items[i][1] for i in range(len(items)) if mask >> i & 1))
        self.assertEqual(P.knapsack(items, W)[0], best)

    def test_matrix_chain(self):
        self.assertEqual(P.matrix_chain([30, 35, 15, 5, 10, 20, 25])[0], 15125)          # CLRS 14.2

    def test_optimal_bst(self):
        rng = random.Random(9)
        p = [rng.random() for _ in range(30)]
        a, ia = P.optimal_bst(p)
        b, ib = P.optimal_bst(p, knuth=True)
        self.assertAlmostEqual(a, b)
        self.assertLess(ib, ia)

    def test_tree_mis(self):
        rng = random.Random(10)
        n = 14
        parent = {v: rng.randrange(v) for v in range(1, n)}
        children = {}
        for v, p in parent.items():
            children.setdefault(p, []).append(v)
        w = [rng.randrange(1, 10) for _ in range(n)]
        self.assertEqual(P.tree_mis(children, 0, w), P.tree_mis_brute(n, list(parent.items()), w))

    def test_fib(self):
        self.assertEqual(P.fib_naive_calls(20), (6765, 21891))
        self.assertEqual(P.fib_memo_calls(20)[0], 6765)


class Search(unittest.TestCase):
    def test_queens(self):
        self.assertEqual(P.queens(8)[0], 92)
        self.assertEqual(P.queens(8, bitmask=False)[0], 92)

    def test_sudoku(self):
        g = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
        out, nodes, ups, nsol = P.solve_sudoku(g)
        self.assertEqual(nsol, 1)
        for i, ch in enumerate(g):
            if ch != "0":
                self.assertEqual(out[i], ch)
        for r in range(9):
            self.assertEqual(set(out[9 * r:9 * r + 9]), set("123456789"))
        self.assertEqual(P.sudoku_naive(g.replace("0", "."))[0], out)

    def test_max_subarray(self):
        rng = random.Random(11)
        for _ in range(50):
            a = [rng.randrange(-20, 20) for _ in range(rng.randrange(1, 40))]
            r = P.maxsub_cubic(a)
            self.assertEqual(P.maxsub_quadratic(a), r)
            self.assertEqual(P.maxsub_divide(a), r)
            self.assertEqual(P.maxsub_kadane(a), r)


class Regression(unittest.TestCase):
 def test_finish_scheduling_and_negative_matching(self):
  intervals=[(2*i,2*i+1) for i in reversed(range(20000))]
  self.assertEqual(P.activity_selection(intervals),list(reversed(intervals)))
  edges=[(0,1,-9),(1,2,4),(2,3,3),(0,3,2)]
  optimum=max(sum(e[2] for e in subset) for size in range(5) for subset in combinations(edges,size) if P.matching_independent(subset))
  self.assertEqual(P.max_weight_matching_brute(edges),optimum)

 def test_full_integer_convolution_certificate_rejects_corruption(self):
  from videos.cs.cs19.measurements import convolution_checker
  a=np.array([9999,3,0,9998,27]);b=np.array([17,9999,4,0])
  check,certificate=convolution_checker(a,b)
  expected=np.zeros(certificate['padded_length'])
  expected[:len(a)+len(b)-1]=np.convolve(a,b)
  check(expected)
  for index in (0,len(a)+len(b)-2):
   bad=expected.copy();bad[index]+=1
   with self.assertRaises(AssertionError):check(bad)

 def test_stale_cache_guard_precedes_upgrade(self):
  import tempfile
  from pathlib import Path
  from unittest.mock import Mock,patch
  from tools.qa_series import require_current_cache,StaleDataError
  from videos.cs.cs19 import compute as C
  with tempfile.TemporaryDirectory() as directory:
   cache=C.ParadigmCache('cs19');cache.dir=Path(directory)
   cache.save('fib',{'schema':1})
   producer=Mock(return_value={'schema':C.SCHEMAS['fib'],'rows':[]})
   with patch.object(C,'CACHE',cache),patch.dict(C.ITEMS,{'fib':producer}):
    with self.assertRaises(StaleDataError):require_current_cache(C,'cs19',cache.path('fib'),'fib')
    producer.assert_not_called()
    self.assertEqual(cache.load('fib')['schema'],2)
    self.assertEqual(cache.load('fib')['schema'],2)
    producer.assert_called_once()

 def test_coins_unreachable_and_input_domain(self):
  self.assertIsNone(P.coin_dp(3,[2]));self.assertEqual(P.coin_dp(0,[]),[]);self.assertIsNone(P.coin_dp(1,[]))
  for f in (P.coin_dp,P.coin_greedy):
   for a,c in [(-1,[1]),(2,[0,1]),(3,[-1,2]),(1.5,[1])]:
    with self.assertRaises(ValueError):f(a,c)
  for coins in ([1,3,4],[2,5],[3,7,9]):
   ref=[0]+[math.inf]*50
   for a in range(1,51):ref[a]=min([ref[a-c]+1 for c in coins if c<=a]+[math.inf])
   for a in range(51):
    out=P.coin_dp(a,coins)
    if math.isinf(ref[a]):self.assertIsNone(out)
    else:self.assertEqual(sum(out),a);self.assertEqual(len(out),ref[a])
 def test_huffman_and_independent_set_empty_negative(self):
  self.assertEqual(P.huffman({}),{});self.assertEqual(P.huffman({'x':2}),{'x':1})
  with self.assertRaises(ValueError):P.huffman({'x':-1})
  self.assertEqual(P.greedy_max_weight(['a'],lambda e:-2,lambda xs:True),[])
  self.assertEqual(P.greedy_max_weight([1,2,3],lambda e:e-2,lambda xs:len(xs)<=2),[3,2])
 def test_actual_school_multiplication_products(self):
  c=[0];a=[0,2,0,3];b=[0,4,5];out=P.school_mul(a,b,c)
  self.assertEqual(c[0],6);self.assertEqual(P.from_digits(out),P.from_digits(a)*P.from_digits(b))
  c=[0];P.school_mul([0,0],[2,3],c);self.assertEqual(c,[0])
 def test_executed_counters_exclude_zero_products_and_initialized_bst_cells(self):
  count=[0];P.karatsuba([0,1],[2,3],count)
  self.assertEqual(count,[2])  # three scalar leaves, one skipped zero-left product
  for n in range(1,8):
   _,trials=P.optimal_bst([1/n]*n)
   self.assertEqual(trials,n*(n+1)*(n+2)//6-n)  # singleton cells are initialized
 def test_digit_and_cutoff_guards_prevent_loops(self):
  for args in [(-1,10),(5,1),(3,0)]:
   with self.assertRaises(ValueError):P.to_digits(*args)
  with self.assertRaises(ValueError):P._carry([-1])
  with self.assertRaises(ValueError):P.karatsuba([1],[2],cutoff=0)
  for x,y in [(0,0),(0,876),(999,999),(1234,5678)]:self.assertEqual(P.from_digits(P._carry(P.karatsuba(P.to_digits(x),P.to_digits(y)))),x*y)
 def test_fft_radix_domain_and_empty_polynomial(self):
  self.assertEqual(P.fft([]),[]);self.assertEqual(P.ifft([]),[]);self.assertEqual(P.poly_mul_fft([],[1,2]),[])
  for n in (3,5,6,7,9):
   with self.assertRaises(ValueError):P.fft(list(range(n)))
  for n in (1,2,4,8,32):
   a=np.arange(n);self.assertTrue(np.allclose(P.fft(a),np.fft.fft(a)));self.assertTrue(np.allclose(P.ifft(P.fft(a)),a))
 def test_ntt_modulus_length_and_root(self):
  self.assertEqual(P.ntt([]),[])
  for args in [([1,2,3],998244353,3),([1,2,3,4],15,2),([1,2,3,4],17,1),([1]*32,17,3)]:
   with self.assertRaises(ValueError):P.ntt(*args)
  for mod,root,n in [(17,3,8),(40961,3,1024),(998244353,3,32)]:
   a=[(i*i+7)%mod for i in range(n)];self.assertEqual(P.ntt(P.ntt(a,mod,root),mod,root,True),a)
 def test_floating_multiplier_domain_and_actual_products(self):
  for args in [(-1,2,4),(2,3,0),(2,3,16),(2,3,2.5)]:
   with self.assertRaises(ValueError):P.fft_bigmul(*args)
  rng=random.Random(97)
  for chunk in (1,2,3,4):
   for x,y in [(0,0),(0,999),(10**1000-1,10**999-1),(rng.randrange(10**3000),rng.randrange(10**2500))]:self.assertEqual(P.fft_bigmul(x,y,chunk),x*y)
 def test_strassen_dimension_guard_and_small_products(self):
  for n in (0,3,6):
   with self.assertRaises(ValueError):P.strassen(np.ones((n,n)),np.ones((n,n)))
  with self.assertRaises(ValueError):P.strassen(np.ones((2,3)),np.ones((2,3)))
  with self.assertRaises(ValueError):P.strassen(np.eye(2),np.eye(2),cutoff=0)
  A=np.arange(64).reshape(8,8);self.assertTrue(np.array_equal(P.strassen(A,A,cutoff=1),A@A))
 def test_deep_tree_iterative_and_invalid_graph(self):
  before=sys.getrecursionlimit();n=20001;self.assertEqual(P.tree_mis({i:[i+1] for i in range(n-1)},0,[1]*n),(n+1)//2);self.assertEqual(sys.getrecursionlimit(),before)
  for children in ({0:[0]},{0:[1,2],1:[2]}):
   with self.assertRaises(ValueError):P.tree_mis(children,0,[1,2,3])
  self.assertEqual(P.tree_mis({},0,[-4]),0)
 def test_dlx_restores_every_link_on_early_return(self):
  x=P.DLX(3,[[0],[1],[2],[0,1],[1,2],[0,2],[0,1,2]])
  arrays=lambda:tuple(tuple(getattr(x,a)) for a in ['L','R','U','D','C','S','row_of'])
  before=arrays();first=x.solve(limit=1);self.assertEqual(arrays(),before);self.assertEqual(x.solve(limit=1),first);self.assertEqual(arrays(),before)
  sols=x.solve(limit=20);expected=[]
  rows=[[0],[1],[2],[0,1],[1,2],[0,2],[0,1,2]]
  for mask in range(1<<len(rows)):
   got=[c for i,row in enumerate(rows) if mask>>i&1 for c in row]
   if sorted(got)==[0,1,2]:expected.append(tuple(i for i in range(len(rows)) if mask>>i&1))
  self.assertEqual({tuple(sorted(s)) for s in sols},set(expected));self.assertEqual(arrays(),before);self.assertGreater(x.updates,0);self.assertEqual(x.updates%4,0)
 def test_sudoku_rejects_inconsistent_complete_board(self):
  self.assertEqual(P.solve_sudoku('1'*81),(None,0,0,0));self.assertEqual(P.sudoku_naive('1'*81),(None,0))
  for s in ('','0'*80,'0'*80+'x'):
   for f in (P.solve_sudoku,P.sudoku_naive):
    with self.assertRaises(ValueError):f(s)
  solved='534678912672195348198342567859761423426853791713924856961537284287419635345286179';self.assertEqual(P.solve_sudoku(solved)[0],solved);self.assertEqual(P.solve_sudoku(solved)[3],1)
 def test_certified_pi_interval_and_original_off_by_one_cases(self):
  import mpmath as mp
  mp.mp.dps=350
  for digits in range(301):
   cert={};out=P.chudnovsky(digits,certificate=cert)
   self.assertEqual(out,int(mp.pi*10**digits));self.assertEqual(cert['lower_floor'],out);self.assertEqual(cert['upper_floor'],out)
  for digits in (-1,2.5):
   with self.assertRaises(ValueError):P.chudnovsky(digits)
 def test_maxsub_empty_and_dp_size_contracts(self):
  for f in (P.maxsub_cubic,P.maxsub_quadratic,P.maxsub_divide,P.maxsub_kadane):
   with self.assertRaises(ValueError):f([])
  self.assertEqual(P.matrix_chain([]),(0,''));self.assertEqual(P.matrix_chain([2]),(0,''))
  for f in (P.fib_naive_calls,P.fib_memo_calls,P.queens):
   with self.assertRaises(ValueError):f(-1)

if __name__ == "__main__":
    unittest.main()
