import itertools
import random
import unittest

from explainer.cs.algo import complexity as X


def brute_sat(n, cl):
    return any(X.check([False] + list(a), cl) for a in itertools.product([False, True], repeat=n))


class Complexity(unittest.TestCase):
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

    def test_pratt(self):
        for p in (2, 3, 97, 7919, 1000000007):
            ok, _ = X.verify_pratt(X.pratt(p))
            self.assertTrue(ok)

    def test_schur(self):
        self.assertIsNotNone(X.cdcl(*X.schur_cnf(13, 3))[0])
        self.assertIsNone(X.cdcl(*X.schur_cnf(14, 3))[0])


if __name__ == "__main__":
    unittest.main()
