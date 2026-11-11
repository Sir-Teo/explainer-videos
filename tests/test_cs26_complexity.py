import itertools
import random
import unittest

from explainer.cs.algo import complexity as X


def brute_sat(n, cl):
    return any(all(any(a[abs(l) - 1] == (l > 0) for l in c) for c in cl)
               for a in itertools.product([False, True], repeat=n))


class Complexity(unittest.TestCase):
    def test_empty_tautological_and_repeated_clauses(self):
        for n, cl in [(0, []), (0, [[]]), (1, [[1, -1]]), (1, [[1, 1], [-1]]),
                      (2, [[], [1, 2]]), (2, [[1, -1], [2, 2]])]:
            expected = brute_sat(n, cl)
            model, stats = X.cdcl(n, (iter(c) for c in cl))
            self.assertEqual(stats['status'], 'sat' if expected else 'unsat')
            self.assertEqual(model is not None, expected)
            self.assertEqual(X.dpll(n, cl)[0] is not None, expected)

    def test_rejects_invalid_solver_domains_and_budgets(self):
        for fn in (X.cdcl, X.dpll, X.to_3sat):
            for n, cl in [(-1, []), (True, []), (1, [[0]]), (1, [[2]]), (1, [[True]])]:
                with self.subTest(fn=fn.__name__, n=n, cl=cl), self.assertRaises(ValueError):
                    fn(n, cl)
        for opts in ({'restart_base': 0}, {'max_conflicts': 0}, {'max_conflicts': -1}):
            with self.assertRaises(ValueError):
                X.cdcl(2, [[1, 2]], **opts)
        with self.assertRaises(ValueError):
            X.dpll(1, [], max_nodes=0)
        with self.assertRaises(ValueError):
            X.check([False], [[1]])

    def test_budget_unknown_is_not_unsat(self):
        # All four binary clauses are UNSAT, but one conflict is insufficient
        # for this run to finish its refutation. None alone is ambiguous.
        model, st = X.cdcl(2, [[1, 2], [1, -2], [-1, 2], [-1, -2]], max_conflicts=1)
        self.assertIsNone(model)
        self.assertEqual(st['status'], 'unknown')
        self.assertEqual(X.cdcl(2, [[1, 2], [1, -2], [-1, 2], [-1, -2]])[1]['status'], 'unsat')

    def test_cdcl_against_brute_force(self):
        rng = random.Random(7)
        for _ in range(300):
            n = rng.randint(1, 11)
            cl = X.random_ksat(n, rng.randint(1, 55), min(3, n), rng)
            model, st = X.cdcl(n, cl)
            self.assertEqual(model is not None, brute_sat(n, cl))
            if model is not None:
                self.assertTrue(X.check(model, cl))
            d, _ = X.dpll(n, cl)
            self.assertEqual(d is not None, model is not None)

    def test_to_3sat(self):
        rng = random.Random(3)
        for _ in range(100):
            n = rng.randint(2, 8)
            cl = [rng.sample([v * rng.choice((1, -1)) for v in range(1, n + 1)], rng.randint(1, n))
                  for _ in range(rng.randint(1, 12))]
            n2, cl3 = X.to_3sat(n, cl)
            self.assertTrue(all(len(c) <= 3 for c in cl3))
            self.assertEqual(brute_sat(n, cl), X.cdcl(n2, cl3)[0] is not None)

    def test_independent_set_clique_cover(self):
        rng = random.Random(5)
        for _ in range(40):
            n = rng.randint(3, 6)
            cl = X.random_ksat(n, rng.randint(2, 9), 3, rng)
            verts, edges, lit, k = X.sat_to_is(cl)
            model, _ = X.cdcl(n, cl)
            if model is None:
                continue
            S = X.is_from_model(cl, model)
            self.assertEqual(len(S), k)
            self.assertTrue(X.is_independent(S, edges))
            comp = X.is_to_clique(verts, edges)
            es = set(comp) | {(b, a) for a, b in comp}
            self.assertTrue(all((u, v) in es for u, v in itertools.combinations(S, 2)))
            self.assertTrue(X.is_cover(X.is_to_vc(verts, S), edges))

    def test_three_colouring(self):
        rng = random.Random(11)
        for _ in range(30):
            n = rng.randint(3, 6)
            cl = X.random_ksat(n, rng.randint(2, 14), 3, rng)
            V, E = X.sat_to_3col(n, cl)
            nv, ccl, var = X.coloring_cnf(V, E, 3)
            cm, _ = X.cdcl(nv, ccl)
            self.assertEqual(cm is not None, brute_sat(n, cl))
            if cm is not None:
                col = X.decode_coloring(V, cm, var, 3)
                self.assertTrue(all(col[u] != col[v] for u, v in E))
                model = [False] + [col[f"x{v}"] == col["T"] for v in range(1, n + 1)]
                self.assertTrue(X.check(model, cl))

    def test_subset_sum(self):
        rng = random.Random(2)
        for _ in range(30):
            n = rng.randint(2, 5)
            cl = X.random_ksat(n, rng.randint(1, 6), min(3, n), rng)
            nums, target = X.sat_to_subset_sum(n, cl)
            model, _ = X.cdcl(n, cl)
            names = list(nums)
            found = any(sum(nums[x] for x in S) == target
                        for r in range(len(names) + 1) for S in itertools.combinations(names, r))
            self.assertEqual(found, model is not None)
            if model is not None:
                self.assertEqual(sum(nums[x] for x in X.subset_from_model(n, cl, model, nums)), target)

    def test_reduction_boundary_and_duplicate_witnesses(self):
        self.assertEqual(X.sat_to_subset_sum(0, []), ({}, 0))
        for fn in (X.sat_to_3col, X.sat_to_subset_sum):
            with self.assertRaises(ValueError):
                fn(4, [[1, 2, 3, 4]])
        for cl in ([[1, 1, 1]], [[1, -1, 1]], [[], [1]]):
            V, E = X.sat_to_3col(1, cl)
            self.assertEqual(X.cdcl(*X.coloring_cnf(V, E, 3)[:2])[0] is not None, brute_sat(1, cl))
            nums, target = X.sat_to_subset_sum(1, cl)
            for value in (False, True):
                model = [False, value]
                if all(any(value == (l > 0) for l in c) for c in cl):
                    chosen = X.subset_from_model(1, cl, model, nums)
                    self.assertEqual(sum(nums[k] for k in chosen), target)

    def test_or_gadget_all_projected_inputs(self):
        # Independent backtracking of graph colours; no SAT solver or CNF
        # encoder is used to certify the complete input/output relation.
        V, E = X.sat_to_3col(3, [[1, 2, 3]])
        for values in itertools.product((False, True), repeat=3):
            fixed = {'T': 1, 'F': 0, 'B': 2}
            for i, value in enumerate(values, 1):
                fixed[f'x{i}'] = int(value)
                fixed[f'~x{i}'] = int(not value)
            rest = [v for v in V if v not in fixed]
            found = False
            for colors in itertools.product(range(3), repeat=len(rest)):
                col = {**fixed, **dict(zip(rest, colors))}
                if all(col[u] != col[v] for u, v in E):
                    found = True
                    break
            self.assertEqual(found, any(values), values)

    def test_cook_levin(self):
        ntm = {"states": ["q", "a"], "start": "q", "accept": "a", "blank": "_", "alphabet": ["0", "1", "_"],
               "delta": {("q", "0"): [("q", "0", 1)], ("q", "1"): [("q", "1", 1), ("a", "1", 1)]}}
        for w in ("0010", "0000", "1", "000"):
            nv, cl, info = X.cook_levin(ntm, w, len(w) + 2)
            model, _ = X.cdcl(nv, cl)
            self.assertEqual(model is not None, "1" in w)

    def test_space_and_games(self):
        adj = {i: {i + 1} for i in range(15)}
        adj[15] = set()
        ok, calls, depth = X.savitch(adj, 0, 15, 16)
        self.assertTrue(ok)
        self.assertFalse(X.savitch(adj, 15, 0, 16)[0])
        self.assertTrue(X.tqbf([("A", 1), ("E", 2)], [[1, 2], [-1, -2]])[0])
        self.assertFalse(X.tqbf([("E", 2), ("A", 1)], [[1, 2], [-1, -2]])[0])
        # a path 0-1-2: player 2 moves to 1, player 1 moves to 2, player 2 is stuck
        self.assertTrue(X.geography({0: [1], 1: [2], 2: []}, 0)[0])
        self.assertFalse(X.geography({0: [1], 1: []}, 0)[0])

    def test_zero_step_reachability_and_quantifier_domains(self):
        g = {0: [1], 1: []}
        self.assertFalse(X.savitch(g, 0, 1, 0)[0])
        self.assertTrue(X.savitch(g, 0, 0, 0)[0])
        self.assertTrue(X.savitch(g, 0, 1, 1)[0])
        with self.assertRaises(ValueError):
            X.savitch(g, 0, 1, -1)
        for quants, cl in [([('Q', 1)], [[1]]), ([('E', 1), ('A', 1)], [[1]]),
                           ([('A', 2)], [[1]]), ([('E', 0)], [])]:
            with self.assertRaises(ValueError):
                X.tqbf(quants, cl)
        self.assertEqual(X.geography({'a': ['b'], 'b': [-7], -7: []}, 'a')[0], True)
        with self.assertRaises(ValueError):
            X.geography({0: [1]}, 0)

    def test_pratt_malformed_and_composite_certificates(self):
        for n in (0, 1, 9, 341, 561, 2 ** 64 + 13):
            with self.assertRaises(ValueError):
                X.pratt(n)
        for c in ({}, {'p': 1}, {'p': 3, 'g': 2, 'factors': [{'p': 1}]},
                  {'p': 9, 'g': 2, 'factors': [{'p': 2}]}, {'p': 2, 'factors': []}):
            self.assertFalse(X.verify_pratt(c)[0])
        cert = X.pratt(97)
        cert['factors'].append(cert)
        self.assertFalse(X.verify_pratt(cert)[0])

    def test_empty_famous_instances(self):
        self.assertEqual(X.schur_cnf(0, 3), (0, []))
        self.assertEqual(X.pythagorean_cnf(0), (0, []))
        with self.assertRaises(ValueError):
            X.schur_cnf(3, 0)

    def test_independent_rup_checker_rejects_false_proofs(self):
        from videos.cs.cs26.computational_references import check_rup
        self.assertTrue(check_rup([[1], [-1]], ['d 1 0', '0'])['checked'])
        for proof in (['2 0', '0'], ['0 0', '0'], ['0']):
            with self.assertRaises(AssertionError):
                check_rup([[1]], proof)

    def test_tableau_rejects_invalid_input_and_time(self):
        machine = {'states': ['q', 'a'], 'start': 'q', 'accept': 'a', 'blank': '_',
                   'alphabet': ['0', '_'], 'delta': {('q', '0'): [('a', '0', 0)]}}
        for w, t in [('0', 0), ('1', 3), ('000000', 1)]:
            with self.assertRaises(ValueError):
                X.cook_levin(machine, w, t)
        self.assertEqual(X.cdcl(*X.cook_levin(machine, '0', 1)[:2])[1]['status'], 'unsat')
        self.assertEqual(X.cdcl(*X.cook_levin(machine, '0', 2)[:2])[1]['status'], 'sat')

    def test_pratt(self):
        for p in (2, 3, 97, 7919, 1000000007):
            ok, _ = X.verify_pratt(X.pratt(p))
            self.assertTrue(ok)

    def test_schur(self):
        self.assertIsNotNone(X.cdcl(*X.schur_cnf(13, 3))[0])
        self.assertIsNone(X.cdcl(*X.schur_cnf(14, 3))[0])


if __name__ == "__main__":
    unittest.main()
