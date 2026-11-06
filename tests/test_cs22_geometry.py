"""Tests for explainer/cs/algo/geometry.py (Part 22 of Computer Science, Built)."""

import math
import random
import unittest

import numpy as np

from explainer.cs.algo import geometry as G


def _norm(h):
    k = h.index(min(h))
    return h[k:] + h[:k]


class Predicates(unittest.TestCase):
    def test_exact_and_adaptive(self):
        rng = random.Random(0)
        for _ in range(2000):
            p, q, r = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(3)]
            s, _ = G.orient_adaptive(p, q, r)
            self.assertEqual(s, G.orient_exact(p, q, r))
        # nearly collinear: the float sign is sometimes wrong, the adaptive one never
        fl, ex = G.kettner_grid((0.5, 0.5), (12.0, 12.0), (24.0, 24.0), 64)
        self.assertGreater(int((fl != ex).sum()), 0)
        xs = [0.5]
        for _ in range(63):
            xs.append(math.nextafter(xs[-1], math.inf))
        for j in range(0, 64, 7):
            for i in range(0, 64, 5):
                s, _ = G.orient_adaptive((xs[i], xs[j]), (12.0, 12.0), (24.0, 24.0))
                self.assertEqual(s, ex[j, i])

    def test_incircle(self):
        a, b, c = (0, 0), (4, 0), (0, 4)
        self.assertEqual(G.incircle_exact(a, b, c, (1, 1)), 1)
        self.assertEqual(G.incircle_exact(a, b, c, (4, 4)), 0)
        self.assertEqual(G.incircle_exact(a, b, c, (5, 5)), -1)


class Hulls(unittest.TestCase):
    def test_all_hulls_agree(self):
        rng = random.Random(1)
        for n in (3, 10, 200, 2000):
            P = [(rng.randint(0, 10 ** 6), rng.randint(0, 10 ** 6)) for _ in range(n)]
            ref = _norm(G.monotone_chain(P))
            for f in (G.jarvis, G.graham, G.quickhull):
                self.assertEqual(_norm(f(P)), ref, f.__name__)
            self.assertEqual(_norm(G.chan(P)[0]), ref)

    def test_hull_sorts(self):
        xs = random.Random(2).sample(range(-1000, 1000), 50)
        h = G.monotone_chain([(x, x * x) for x in xs])
        lo = h.index(min(h))
        self.assertEqual([p[0] for p in h[lo:] + h[:lo]], sorted(xs))


class Sweep(unittest.TestCase):
    def test_bentley_ottmann(self):
        rng = random.Random(3)
        segs = []
        for _ in range(80):
            a = (rng.random(), rng.random())
            segs.append((a, (a[0] + rng.uniform(0.02, 0.5), rng.random())))
        bo, ev, tests, _ = G.bentley_ottmann(segs)
        br = G.brute_intersections(segs)
        self.assertEqual(sorted((i, j) for i, j, _ in bo), sorted((i, j) for i, j, _ in br))
        self.assertEqual(ev, 2 * len(segs) + len(br))


class Polygons(unittest.TestCase):
    def test_ears_and_guards(self):
        for seed in range(5):
            poly = G.star_polygon(30, seed=seed)
            if G.polygon_area2(poly) < 0:
                poly = poly[::-1]
            tris, _ = G.ear_clip(poly)
            self.assertEqual(len(tris), len(poly) - 2)
            area = sum(abs(G.polygon_area2([poly[i] for i in t])) for t in tris)
            self.assertEqual(area, abs(G.polygon_area2(poly)))
            col = G.fisk_colouring(len(poly), tris)
            for t in tris:
                self.assertEqual(sorted(col[i] for i in t), [0, 1, 2])
            self.assertLessEqual(min(col.count(c) for c in range(3)), len(poly) // 3)

    def test_comb(self):
        P = G.comb(6)
        self.assertEqual(len(P), 3 * 6 + 2)
        self.assertGreater(G.polygon_area2(P), 0)


class Triangulations(unittest.TestCase):
    def test_delaunay_three_ways(self):
        rng = random.Random(4)
        P = [(rng.randint(0, 10 ** 6), rng.randint(0, 10 ** 6)) for _ in range(300)]
        ref = G.lifting_delaunay(P)
        D = G.delaunay(P)
        self.assertEqual(D.triangles(), ref)
        self.assertEqual(G.fortune(P)["triangles"], ref)
        T = G.sweep_triangulation(P)
        self.assertEqual(len(T), len(ref))
        L, flips, _ = G.lawson(P, T)
        self.assertEqual(L, ref)
        self.assertGreaterEqual(G.min_angle(P, L), G.min_angle(P, T))

    def test_beach_line(self):
        sites = [(0.0, 5.0), (3.0, 4.0)]
        ys = G.beach_line(sites, 1.0, np.array([0.0, 3.0]))
        self.assertAlmostEqual(ys[0], min(G._parabola_y(s, 0.0, 1.0) for s in sites))


class LpAndSearch(unittest.TestCase):
    def test_seidel(self):
        from scipy.optimize import linprog
        rng = random.Random(5)
        H = []
        for _ in range(150):
            t = rng.uniform(0, 2 * math.pi)
            H.append((math.cos(t), math.sin(t), 1 + rng.random()))
        for c in ((1.0, 0.3), (-0.2, 1.0), (-1.0, -1.0)):
            x, _, _ = G.seidel_lp(H, c)
            r = linprog([-c[0], -c[1]], A_ub=[h[:2] for h in H], b_ub=[h[2] for h in H], bounds=[(None, None)] * 2)
            self.assertAlmostEqual(c[0] * x[0] + c[1] * x[1], -r.fun, places=6)

    def test_kdtree(self):
        P = np.random.default_rng(0).random((3000, 2))
        T = G.KDTree(P)
        got = sorted(T.range((0.2, 0.3), (0.35, 0.5)))
        want = sorted(np.flatnonzero(np.all((P >= (0.2, 0.3)) & (P <= (0.35, 0.5)), axis=1)).tolist())
        self.assertEqual(got, want)
        for q in ((0.1, 0.9), (0.5, 0.5)):
            self.assertEqual(T.nearest(q)[0], int(np.argmin(((P - q) ** 2).sum(1))))

    def test_trapezoids(self):
        segs = [((0, 0), (4, 1)), ((1, 3), (5, 4)), ((6, 0), (8, 2))]
        _, nt = G.vertical_decomposition(segs, (-1, -1, 10, 6))
        self.assertEqual(nt, 3 * len(segs) + 1)


class Misc(unittest.TestCase):
    def test_ham_sandwich(self):
        rng = random.Random(6)
        red = [(rng.randint(0, 100), rng.randint(0, 100)) for _ in range(9)]
        blue = [(rng.randint(0, 100), rng.randint(0, 100)) for _ in range(9)]
        p, q, _ = G.ham_sandwich(red, blue)
        self.assertIsNotNone(p)

    def test_cspace_path(self):
        robot = [(0, 0), (2, 0), (1, 2)]
        obs = [[(3, 3), (6, 3), (6, 6), (3, 6)]]
        cs = [G.minkowski_cspace(o, robot) for o in obs]
        path, length, _ = G.visibility_path((0, 0), (8, 8), cs)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (8, 8))
        self.assertGreaterEqual(length, math.dist((0, 0), (8, 8)))


if __name__ == "__main__":
    unittest.main()
