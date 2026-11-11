import itertools
import random
import unittest

from explainer.cs.algo import proofs as P


class Proofs(unittest.TestCase):
    def test_fingerprints(self):
        rng = random.Random(1)
        n = 200
        q = P.next_prime(n * n)
        x = [rng.randrange(2) for _ in range(n)]
        self.assertTrue(all(P.fingerprint_eq(x, x, q, rng)[0] for _ in range(50)))
        y = x[:]
        y[17] ^= 1
        wrong = sum(P.fingerprint_eq(x, y, q, rng)[0] for _ in range(2000))
        self.assertLess(wrong / 2000, 3 * n / q)

    def test_restriction_and_depth(self):
        rng = random.Random(2)
        for _ in range(30):
            n = 6
            f = P.dnf_random(n, 4, 3, rng)
            rho = P.random_restriction(n, 0.5, rng)
            g = P.restrict(f, rho)
            free = [v for v in range(n) if v not in rho]
            tab = P.truth_table(g, free)
            for m in range(1 << len(free)):
                x = {v: rho[v] for v in rho}
                x.update({v: bool(m >> i & 1) for i, v in enumerate(free)})
                self.assertEqual(tab[m], P.dnf_eval(f, x))
            self.assertLessEqual(P.dt_depth(tab, len(free)), len(free))
        self.assertEqual(P.dt_depth((False, True, True, False), 2), 2)   # xor
        self.assertEqual(P.dt_depth((False, False, True, True), 2), 1)   # x_1

    def test_sumcheck(self):
        rng = random.Random(3)
        for _ in range(10):
            n = 4
            cl = [rng.sample([1, 2, 3, 4, -1, -2, -3, -4], 3) for _ in range(4)]
            cl = [c for c in cl if len({abs(l) for l in c}) == 3] or [[1, 2, 3]]
            true = P.count_sat(cl, n)
            ok, _, _ = P.sumcheck(cl, n, 101, true, rng)
            self.assertTrue(ok)
        caught = sum(not P.sumcheck([[1, 2, -3], [-1, 3, 4]], 4, 10007, 3, rng, cheat=True)[0] for _ in range(50))
        self.assertGreaterEqual(caught, 49)

    def test_zero_knowledge(self):
        rng = random.Random(4)
        edges = [(0, 1), (1, 2), (2, 0), (2, 3)]
        good = [0, 1, 2, 0]
        caught, rev = P.zk_colouring(4, edges, good, 200, rng)
        self.assertIsNone(caught)
        self.assertTrue(all(a != b for a, b in rev))
        bad = [0, 1, 2, 2]
        caught, _ = P.zk_colouring(4, edges, bad, 500, rng)
        self.assertIsNotNone(caught)

    def test_blr(self):
        n = 4
        lin = [bin(5 & x).count("1") & 1 for x in range(1 << n)]
        self.assertEqual(P.blr_rejection(lin, n), 0.0)
        self.assertEqual(P.distance_to_linear(lin, n), 0.0)
        g = lin[:]
        g[3] ^= 1
        self.assertGreater(P.blr_rejection(g, n), 0)

    def test_vertex_cover(self):
        rng = random.Random(5)
        for _ in range(20):
            n = 9
            edges = [(u, v) for u, v in itertools.combinations(range(n), 2) if rng.random() < 0.3]
            best = next(k for k in range(n + 1) if P.vc_brute(edges, n, k)[0] is not None)
            c, _ = P.vc_branch(edges, best)
            self.assertIsNotNone(c)
            self.assertTrue(all(u in c or v in c for u, v in edges))
            self.assertIsNone(P.vc_branch(edges, best - 1)[0] if best else None)

    def test_permanent_and_det(self):
        rng = random.Random(6)
        for n in range(1, 7):
            A = [[rng.randrange(-2, 3) for _ in range(n)] for _ in range(n)]
            self.assertEqual(P.permanent_ryser(A), P.permanent_brute(A))
        self.assertEqual(P.det_bareiss([[2, 1], [7, 4]]), 1)

    def test_fine_grained(self):
        self.assertTrue(P.ov_brute([0b101, 0b011], [0b010]))
        self.assertFalse(P.ov_brute([0b111], [0b001, 0b010]))
        self.assertEqual(sum(P.three_sum([-5, 1, 4, 10, 2])), 0)
        self.assertIsNone(P.three_sum([1, 2, 3]))


class TestAverage(unittest.TestCase):
    def test_planted_and_rho(self):
        rng = random.Random(1)
        adj, S = P.planted_clique(300, 60, rng)
        self.assertTrue(all((adj[u] >> v) & 1 for u in S for v in S if u != v))
        self.assertEqual(P.degree_recover(adj, 60), S)
        n = P.next_prime(10 ** 6) * P.next_prime(2 * 10 ** 6)
        f, _ = P.pollard_rho(n, random.Random(2))
        self.assertTrue(1 < f < n and n % f == 0)




class TestUgOv(unittest.TestCase):
    def test_ug(self):
        rng = random.Random(3)
        edges, planted = P.ug_instance(50, 120, 5, 0.0, rng)
        self.assertEqual(P.ug_value(edges, planted, 5), 1.0)
        self.assertEqual(P.ug_value(edges, P.ug_propagate(50, edges, 5, 0), 5), 1.0)

    def test_sat_to_ov(self):
        for s in range(6):
            rng = random.Random(s)
            cl = [[rng.choice([-1, 1]) * v for v in rng.sample(range(1, 11), 3)] for _ in range(45)]
            A, B = P.sat_to_ov(cl, 10)
            sat = any(all(any(((bits >> (abs(l) - 1)) & 1) == (l > 0) for l in c) for c in cl)
                      for bits in range(1 << 10))
            self.assertEqual(P.ov_brute(A, B), sat)


class TestPit(unittest.TestCase):
    def test_vandermonde(self):
        rng = random.Random(4)
        for _ in range(50):
            xs = [rng.randrange(10007) for _ in range(6)]
            self.assertTrue(P.vandermonde_test(xs, 10007))
        self.assertEqual(P.det_mod([[2, 1], [1, 3]], 7), 5)
        self.assertLess(sum(P.vandermonde_test([rng.randrange(10007) for _ in range(6)], 10007, True)
                            for _ in range(200)), 10)

import hashlib
import itertools
import math
from fractions import Fraction


class TestContracts(unittest.TestCase):
    def test_binomial_endpoints_and_exact_rational_reference(self):
        for k in range(21):
            for numerator,denominator in [(0,1),(1,1),(1,3),(2,5)]:
                q=Fraction(numerator,denominator)
                for threshold in [-2,0,k//2,k,k+1]:
                    exact=sum((Fraction(math.comb(k,i))*q**i*(1-q)**(k-i)
                               for i in range(max(0,threshold),k+1)),Fraction(0))
                    self.assertAlmostEqual(P.binom_tail(k,float(q),threshold),float(exact),places=12)
        for args in [(-1,0.5,1),(True,0.5,1),(2,float('nan'),1),(2,-0.1,1),(2,0.5,0.5)]:
            with self.assertRaises(ValueError): P.binom_tail(*args)

    def test_field_interpolation_and_fingerprint_contracts(self):
        for prime in [2,3,97,1000003,(1<<61)-1]: self.assertTrue(P.is_prime(prime))
        for composite in [0,1,4,561,3215031751,341550071728321]: self.assertFalse(P.is_prime(composite))
        with self.assertRaises(ValueError): P.is_prime(318665857834031151167461)
        for prime in [2,3,7,97]:
            degree=min(3,prime-1);coeffs=list(range(1,degree+2))
            ys=[sum(c*x**i for i,c in enumerate(coeffs))%prime for x in range(degree+1)]
            for x in range(prime): self.assertEqual(P.lagrange_eval(ys,x,prime),sum(c*x**i for i,c in enumerate(coeffs))%prime)
        for args in [([],0,97),([1,2],1,4),([1,2,3],0,2)]:
            with self.assertRaises(ValueError): P.lagrange_eval(*args)
        with self.assertRaises(ValueError): P.fingerprint_eq([1],[1,0],97,random.Random(1))
        with self.assertRaises(ValueError): P.fingerprint_eq([2],[1],97,random.Random(1))
        # Every r in the field, independently of the instrument's RNG.
        class Fixed:
            def __init__(self,r): self.r=r
            def randrange(self,q): return self.r
        x=[1,0,0,1];y=[0,1,0,0];p=7
        wrong=sum(P.fingerprint_eq(x,y,p,Fixed(r))[0] for r in range(p))
        self.assertLessEqual(wrong,len(x)-1)

    def test_constant_and_repeated_variable_sumcheck(self):
        cases=[(0,[]),(0,[[]]),(1,[]),(1,[[]]),(1,[[1,1,1]]*3),(2,[[1,-1],[2,2]])]
        for n,clauses in cases:
            truth=sum(all(any(bits[abs(l)-1]==(l>0) for l in c) for c in clauses)
                      for bits in itertools.product((False,True),repeat=n))
            for seed in range(8):
                ok,rounds,log=P.sumcheck(clauses,n,97,truth,random.Random(seed))
                self.assertTrue(ok,(n,clauses,seed));self.assertEqual(rounds,n)
                self.assertEqual(log[-1]['final'],log[-1]['claim'])
                for row in log[:-1]:
                    self.assertEqual((row['g'][0]+row['g'][1])%97,row['previous'])
                    self.assertEqual(len(row['g']),row['degree_bound']+1)
        with self.assertRaises(ValueError): P.sumcheck([[1]]*5,1,5,1,random.Random(0))
        with self.assertRaises(ValueError): P.sumcheck([[0]],1,97,1,random.Random(0))
        with self.assertRaises(ValueError): P.honest_message([[1,1]],1,97,[],1)

    def test_public_hash_commitment_transcript_and_empty_game(self):
        trace=[];caught,pairs=P.zk_colouring(3,[(0,1),(1,2),(0,2)],[0,1,2],20,random.Random(7),trace=trace)
        self.assertIsNone(caught);self.assertEqual(len(trace),20)
        for row,pair in zip(trace,pairs):
            self.assertEqual(tuple(o['colour'] for o in row['openings']),pair)
            self.assertNotEqual(*pair)
            self.assertEqual(row['edge'],[o['vertex'] for o in row['openings']])
            for opening in row['openings']:
                h=hashlib.sha256(bytes.fromhex(opening['nonce'])+bytes([opening['colour']])).hexdigest()
                self.assertEqual(h,row['commitments'][opening['vertex']])
        self.assertEqual(P.zk_colouring(0,[],[],5,random.Random(0)),(None,[]))
        with self.assertRaises(ValueError): P.zk_colouring(2,[(0,1)],[0,3],1,random.Random(0))

    def test_all_three_bit_blr_functions_against_fourier_identity(self):
        n=3;N=1<<n
        for bits in itertools.product((0,1),repeat=N):
            spectrum=[sum((1 if bits[x]==(a&x).bit_count()%2 else -1) for x in range(N)) for a in range(N)]
            distance=Fraction(N-max(spectrum),2*N)
            rejection=Fraction(1,2)-Fraction(sum(c**3 for c in spectrum),2*N**3)
            self.assertEqual(P.distance_to_linear(bits,n),float(distance))
            self.assertEqual(P.blr_rejection(bits,n),float(rejection))
        for fn in [P.dt_depth,P.blr_rejection,P.distance_to_linear]:
            with self.assertRaises(ValueError): fn([0,1,1],2)

    def test_all_five_vertex_covers_and_kernel_equivalence(self):
        n=5;possible=list(itertools.combinations(range(n),2))
        for mask in range(1<<len(possible)):
            edges=[e for i,e in enumerate(possible) if mask>>i&1]
            for k in range(n+1):
                witnesses=[set(S) for r in range(k+1) for S in itertools.combinations(range(n),r)
                           if all(u in S or v in S for u,v in edges)]
                cover,nodes=P.vc_branch(edges,k)
                self.assertEqual(cover is not None,bool(witnesses))
                if cover is not None:
                    self.assertLessEqual(len(cover),k)
                    self.assertTrue(all(u in cover or v in cover for u,v in edges))
                kernel=P.buss_kernel(edges,k)
                if kernel is None: self.assertFalse(witnesses)
                else:
                    forced,rest,budget=kernel
                    possible_rest=any(all(u in S or v in S for u,v in rest)
                                      for r in range(budget+1) for S in itertools.combinations(range(n),r))
                    self.assertEqual(possible_rest,bool(witnesses))
                    self.assertLessEqual(len(rest),budget*budget)
                    self.assertEqual(len(forced)+budget,k)
        self.assertIsNotNone(P.buss_kernel([(0,1)]*10,1))
        self.assertIsNotNone(P.buss_kernel([(0,1)]*3+[(1,2)]*3,1))
        self.assertEqual(P.vc_brute([],2,5)[0],[0,1])
        with self.assertRaises(ValueError): P.vc_branch([(0,1)],-1)
        with self.assertRaises(ValueError): P.buss_kernel([(0,0)],1)

    def test_empty_and_exact_determinants(self):
        self.assertEqual(P.permanent_ryser([]),1);self.assertEqual(P.det_bareiss([]),1)
        def reference(A):
            M=[[Fraction(v) for v in row] for row in A];d=Fraction(1)
            for i in range(len(M)):
                pivot=next((r for r in range(i,len(M)) if M[r][i]),None)
                if pivot is None: return 0
                if pivot!=i: M[i],M[pivot]=M[pivot],M[i];d=-d
                q=M[i][i];d*=q
                for r in range(i+1,len(M)):
                    factor=M[r][i]/q
                    M[r]=[a-factor*b for a,b in zip(M[r],M[i])]
            return int(d)
        rng=random.Random(81)
        for n in range(8):
            for _ in range(10):
                A=[[rng.randrange(-9,10) for _ in range(n)] for _ in range(n)]
                d=reference(A);self.assertEqual(P.det_bareiss(A),d)
                for prime in [2,7,97]: self.assertEqual(P.det_mod(A,prime),d%prime)
        for fn in [P.det_bareiss,P.permanent_ryser]:
            with self.assertRaises(ValueError): fn([[1,2]])

    def test_unique_simple_graph_and_corruption_count(self):
        for n in range(1,9):
            for m in {n-1,n*(n-1)//2}:
                for eps in [0,0.3,1]:
                    edges,labels=P.ug_instance(n,m,3,eps,random.Random(90+n))
                    self.assertEqual(len(edges),m)
                    self.assertEqual(len({tuple(sorted((a,b))) for a,b,c in edges}),m)
                    self.assertEqual(sum((labels[b]-labels[a]-c)%3!=0 for a,b,c in edges),round(eps*m))
                    if eps==0:
                        for root in range(n): self.assertEqual(P.ug_value(edges,P.ug_propagate(n,edges,3,root),3),1)
        with self.assertRaises(ValueError): P.ug_instance(2,2,3,0,random.Random(0))
        with self.assertRaises(ValueError): P.ug_instance(3,3,1,0.5,random.Random(0))

    def test_bounded_rho_and_empty_walksat_clauses(self):
        for n in [0,1,2,3,97]:
            with self.assertRaises(ValueError): P.pollard_rho(n,random.Random(0))
        self.assertEqual(P.pollard_rho(8051,random.Random(0),max_steps=0),(None,0))
        self.assertEqual(P.pollard_rho(8051,random.Random(0),max_steps=2),(None,2))
        for n in [4,9,15,49,8051,1000003*2000003]:
            factor,steps=P.pollard_rho(n,random.Random(3),max_steps=20000)
            self.assertTrue(1<factor<n and n%factor==0);self.assertLessEqual(steps,20000)
        best,a=P.walksat(2,[[],[1],[-2]],random.Random(1),flips=30)
        self.assertEqual(best,sum(any(a[abs(l)]==(l>0) for l in c) for c in [[],[1],[-2]]))
        self.assertEqual(best,2)


if __name__ == '__main__':
    unittest.main()
