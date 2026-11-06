"""Tests for Part 51's transform, rasterizer and curve instruments (explainer/cs/graphics)."""

from __future__ import annotations

import math
import unittest

import numpy as np
from scipy.interpolate import BSpline
from scipy.spatial import Delaunay

from explainer.cs.algo.geometry import orient_float
from explainer.cs.graphics import curves as C
from explainer.cs.graphics import raster as R
from explainer.cs.graphics import transform as T


def rodrigues(axis, deg, v):
    k = np.asarray(axis, float) / np.linalg.norm(axis)
    th = math.radians(deg)
    v = np.asarray(v, float)
    return v * math.cos(th) + np.cross(k, v) * math.sin(th) + k * (k @ v) * (1 - math.cos(th))


class Matrices(unittest.TestCase):
    def test_basic(self):
        np.testing.assert_allclose(T.apply(T.translate(1, 2, 3), [(1, 1, 1)])[0], (2, 3, 4))
        np.testing.assert_allclose(T.apply(T.rotate_z(90), [(1, 0, 0)])[0], (0, 1, 0), atol=1e-12)
        np.testing.assert_allclose(T.apply(T.rotate_x(90), [(0, 1, 0)])[0], (0, 0, 1), atol=1e-12)
        np.testing.assert_allclose(T.apply(T.rotate_y(90), [(0, 0, 1)])[0], (1, 0, 0), atol=1e-12)
        for ax, f in (((1, 0, 0), T.rotate_x), ((0, 1, 0), T.rotate_y), ((0, 0, 1), T.rotate_z)):
            np.testing.assert_allclose(T.apply(f(37), [(0.3, -1.2, 2.0)])[0], rodrigues(ax, 37, (0.3, -1.2, 2.0)))

    def test_order(self):
        d = T.composition_order_demo()
        self.assertEqual(d["rotate_then_translate"][1], [2.0, 1.0, 0.0])     # rotate (1,0) to (0,1), then +2 in x
        self.assertEqual(d["translate_then_rotate"][1], [0.0, 3.0, 0.0])     # (3,0) rotated to (0,3)
        A, B = T.rotate_x(30), T.translate(1, 0, 0)
        p = [(0.5, 0.2, -0.7)]
        np.testing.assert_allclose(T.apply(T.compose(A, B), p), T.apply(A, T.apply(B, p)))


class Projection(unittest.TestCase):
    def test_similar_triangles(self):
        fov, asp, n, f = 50.0, 1.5, 0.5, 20.0
        P = T.perspective(fov, asp, n, f)
        cot = 1 / math.tan(math.radians(fov) / 2)
        x, y, d = 0.7, -0.4, 3.0
        ndc = T.project(P, [(x, y, -d)])[0]
        self.assertAlmostEqual(ndc[0], cot / asp * x / d)
        self.assertAlmostEqual(ndc[1], cot * y / d)
        self.assertAlmostEqual(T.project(P, [(0, 0, -n)])[0][2], -1)
        self.assertAlmostEqual(T.project(P, [(0, 0, -f)])[0][2], 1)
        self.assertAlmostEqual(ndc[2], float(T.ndc_depth(d, n, f)))

    def test_frustum_to_cube(self):
        r = T.frustum_to_cube()
        np.testing.assert_allclose(np.abs(r["corners_ndc"]), 1, atol=1e-12)
        np.testing.assert_allclose(r["frames"][0]["points"], r["corners_eye"])
        np.testing.assert_allclose(r["frames"][-1]["points"], r["corners_ndc"])
        P = np.array(r["matrix"])
        E = np.array(r["corners_eye"])
        for fr in r["frames"][1:-1]:
            M = (1 - fr["t"]) * np.eye(4) + fr["t"] * P
            Q = np.array(fr["points"])
            for a, b in r["edges"]:                      # straight edges stay straight
                m = T.apply(M, [(E[a] + E[b]) / 2])[0]
                self.assertLess(np.linalg.norm(np.cross(m - Q[a], Q[b] - Q[a])), 1e-9)
            for face in ((0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4)):   # flat faces stay flat
                a, b, c, d = Q[list(face)]
                self.assertLess(abs(np.cross(b - a, c - a) @ (d - a)), 1e-9)


class Depth(unittest.TestCase):
    def test_window(self):
        self.assertAlmostEqual(float(T.window_depth(0.1, 0.1, 1000)), 0)
        self.assertAlmostEqual(float(T.window_depth(1000, 0.1, 1000)), 1)

    def test_resolvable(self):
        for r in T.depth_table():
            # (the search differences depths near 1, so it is good to ~1e-9 relative, the rounding of the subtraction)
            self.assertAlmostEqual(r["resolvable"] / r["exact"], 1, places=7)
            # the first-order derivative formula agrees to first order in d k
            self.assertLess(abs(r["derivative"] / r["exact"] - 1), 0.01)
            step = 1 / (2 ** 24 - 1)
            self.assertAlmostEqual((r["window"] - float(T.window_depth(r["distance"] - r["resolvable"], r["near"],
                                                                       r["far"]))) / step, 1, places=6)
        rows = {(r["near"], r["distance"]): r["resolvable"] for r in T.depth_table()}
        self.assertGreater(rows[(0.01, 100)], 99 * rows[(1.0, 100)])     # near x 100 costs precision x ~100

    def test_z_fighting(self):
        tab = {(r["near"], r["bits"]): r for r in T.z_fighting_table()}
        self.assertEqual(tab[(1.0, 24)]["flipped"], 0)
        self.assertGreater(tab[(0.01, 16)]["share"], 0.9)
        self.assertGreater(tab[(0.01, 24)]["share"], tab[(1.0, 24)]["share"])
        self.assertGreater(tab[(1.0, 16)]["share"], tab[(1.0, 24)]["share"])
        # independent estimate: two depths delta apart round to the same integer with probability max(0, 1 - delta/q)
        for (n, b), r in tab.items():
            x = (np.arange(160) + 0.5) / 160 * 2 - 1
            d = 50 + 2 * x
            delta = (T.window_depth(d + 0.01, n, 1000) - T.window_depth(d, n, 1000)) * (2 ** b - 1)
            self.assertAlmostEqual(r["share"], float(np.mean(np.maximum(0, 1 - delta))), delta=0.03)


class Rotations(unittest.TestCase):
    def test_quaternion(self):
        rng = np.random.default_rng(1)
        for _ in range(20):
            ax, ang, v = rng.normal(size=3), rng.uniform(-180, 180), rng.normal(size=3)
            q = T.quat_from_axis_angle(ax, ang)
            np.testing.assert_allclose(T.quat_rotate(q, v), rodrigues(ax, ang, v), atol=1e-12)
            np.testing.assert_allclose(T.quat_to_matrix(q) @ v, rodrigues(ax, ang, v), atol=1e-12)
            np.testing.assert_allclose(T.quat_to_matrix(-q), T.quat_to_matrix(q), atol=1e-12)
            q2 = T.quat_from_axis_angle(rng.normal(size=3), rng.uniform(-180, 180))
            np.testing.assert_allclose(T.quat_to_matrix(T.quat_mul(q2, q)),
                                       T.quat_to_matrix(q2) @ T.quat_to_matrix(q), atol=1e-12)
            np.testing.assert_allclose(T.quat_mul(q, T.quat_conj(q)), (1, 0, 0, 0), atol=1e-12)
        e = (40.0, -25.0, 70.0)
        np.testing.assert_allclose(T.quat_to_matrix(T.quat_from_euler(*e)), T.euler_matrix(*e), atol=1e-12)

    def test_slerp(self):
        a = T.quat_from_axis_angle((0, 0, 1), 10)
        b = T.quat_from_axis_angle((0, 0, 1), 130)
        for t in np.linspace(0, 1, 9):
            np.testing.assert_allclose(T.quat_to_matrix(T.slerp(a, b, t)),
                                       T.quat_to_matrix(T.quat_from_axis_angle((0, 0, 1), 10 + 120 * t)), atol=1e-12)
            # -b is the same rotation: slerp must take the same (shorter) arc
            np.testing.assert_allclose(T.quat_to_matrix(T.slerp(a, -b, t)), T.quat_to_matrix(T.slerp(a, b, t)),
                                       atol=1e-12)
        # the long way round: 10 -> 300 degrees about z is 70 degrees the short way
        c = T.quat_from_axis_angle((0, 0, 1), 300)
        mid = T.quat_to_matrix(T.slerp(a, c, 0.5))
        np.testing.assert_allclose(mid, T.euler_matrix(-25, 0, 0), atol=1e-12)

    def test_gimbal(self):
        for r in T.gimbal_lock():
            s = math.sin(math.radians(r["pitch"]))
            np.testing.assert_allclose(r["singular_values"], [math.sqrt(1 + s), 1, math.sqrt(max(0, 1 - s))],
                                       atol=1e-6)
        ranks = [r["rank"] for r in T.gimbal_lock()]
        self.assertEqual(ranks, [3, 3, 3, 2])

    def test_slerp_vs_euler(self):
        r = T.slerp_vs_euler()
        s, e = r["slerp"], r["euler"]
        np.testing.assert_allclose(s["per_step_deg"], r["geodesic_deg"] / r["steps"], rtol=1e-9)
        self.assertAlmostEqual(s["total_deg"], r["geodesic_deg"], places=6)
        self.assertGreater(e["total_deg"], 1.3 * r["geodesic_deg"])
        self.assertGreater(max(e["per_step_deg"]) - min(e["per_step_deg"]), 1)
        np.testing.assert_allclose(s["path"][0], e["path"][0], atol=1e-12)
        np.testing.assert_allclose(s["path"][-1], e["path"][-1], atol=1e-12)
        np.testing.assert_allclose(np.linalg.norm(s["path"], axis=1), 1)
        self.assertEqual(len(s["path"]), r["steps"] + 1)


class Raster(unittest.TestCase):
    def test_edge_is_orientation(self):
        rng = np.random.default_rng(2)
        for _ in range(50):
            a, b, p = rng.normal(size=(3, 2))
            self.assertEqual(R.edge(a, b, p), orient_float(a, b, p))
            l = R.barycentric(a, b, rng.normal(size=2), p)
            self.assertAlmostEqual(sum(l), 1)
        a, b, c = np.array([0, 0.0]), np.array([4, 0.0]), np.array([0, 3.0])
        p = np.array([1.0, 1.0])
        l = R.barycentric(a, b, c, p)
        np.testing.assert_allclose(l[0] * a + l[1] * b + l[2] * c, p)

    def _count(self, tris, W, H):
        cnt = np.zeros((H, W), int)
        for t in tris:
            m, box = R.coverage(*t, W, H)
            if m is not None:
                i0, i1, j0, j1 = box
                cnt[j0:j1 + 1, i0:i1 + 1] += m
        return cnt

    def test_fill_rule_grid(self):
        # a triangulated grid with every vertex on a pixel centre: many centres lie exactly on edges
        W, H = 40, 30
        tris = []
        xs, ys = np.arange(0.5, 40, 4), np.arange(0.5, 30, 3)
        for x0, x1 in zip(xs, xs[1:]):
            for y0, y1 in zip(ys, ys[1:]):
                tris += [((x0, y0), (x1, y0), (x1, y1)), ((x0, y0), (x1, y1), (x0, y1))]
        cnt = self._count(tris, W, H)
        # the rectangle spans centres [0.5, 36.5] x [0.5, 27.5]; top-left owns the top and left borders; the right and bottom borders of the rectangle are not owned
        self.assertTrue((cnt <= 1).all())
        self.assertEqual(int(cnt.sum()), 36 * 27)
        self.assertTrue((cnt[0:27, 0:36] == 1).all())

    def test_fill_rule_delaunay(self):
        rng = np.random.default_rng(3)
        W, H = 64, 48
        pts = np.r_[rng.uniform(2, 62, (60, 2)) * [1, 0.75], [(1, 1), (63, 1), (63, 47), (1, 47)]]
        pts = np.round(pts * 2) / 2                 # half-integers: centres on vertices and edges
        pts = np.unique(pts, axis=0)
        tri = Delaunay(pts)
        cnt = self._count([pts[s] for s in tri.simplices], W, H)
        self.assertTrue((cnt <= 1).all())           # never owned twice
        cx, cy = np.meshgrid(np.arange(W) + 0.5, np.arange(H) + 0.5)
        strict = (cx > 1) & (cx < 63) & (cy > 1) & (cy < 47)
        self.assertTrue((cnt[strict] == 1).all())   # never missed inside the hull

    def test_rasterize_counters_and_area(self):
        P = T.perspective(60, 4 / 3, 0.1, 100)
        tri = R._tris(P, [(-2, -1.5, -4), (2.2, -1.2, -4), (0, 2, -4)], [(0, 1, 2)], np.eye(3))
        r = R.rasterize(tri, 160, 120)
        c = r["counters"]
        self.assertEqual(c["covered"], c["depth_pass"] + c["depth_fail"])
        self.assertGreaterEqual(c["tested"], c["covered"])
        ndc = T.project(P, [(-2, -1.5, -4), (2.2, -1.2, -4), (0, 2, -4)])
        s = [((x + 1) * 80, (1 - y) * 60) for x, y, _ in ndc]
        area = abs(R.edge(*s)) / 2
        self.assertLess(abs(c["covered"] - area), 0.05 * area)
        cov = r["tri"] >= 0
        np.testing.assert_allclose(r["attr"][cov].sum(1), 1)    # barycentrics sum to one

    def test_clip_near(self):
        clip = np.array([[0, 0, -2, 1.0], [1, 0, 0.5, 1.0], [0, 1, 0.5, 1.0]])   # first vertex in front of near
        out = R.clip_near(clip, np.eye(3))
        self.assertEqual(len(out), 2)
        for Cc, _ in out:
            self.assertTrue((Cc[:, 2] + Cc[:, 3] >= -1e-12).all())

    def test_perspective_correct(self):
        r = R.perspective_correct_demo()
        self.assertEqual(r["wrong_perspective"], 0.0)
        self.assertGreater(r["wrong_affine"], 0.2)
        self.assertLess(r["uv_error_max"], 1e-9)

    def test_barycentric_demo(self):
        r = R.barycentric_demo()
        img = r["image"]
        a, b, c = (np.array(v) for v in r["vertices"])
        j, i = 60, 80
        l = R.barycentric(a, b, c, (i + 0.5, j + 0.5))
        # equal depths, so perspective-correct and screen barycentrics agree
        np.testing.assert_allclose(img[j, i], l, atol=1e-9)


class Shading(unittest.TestCase):
    def test_lighting_formulas(self):
        kd, ks = (0.5, 0.5, 0.5), 0.8
        lt = R.lighting([(0, 0, -1.0)], [(0, 0, 1.0)], light=(0, 0, 0), kd=kd, ks=ks)
        self.assertAlmostEqual(lt["diffuse"][0, 0], 0.5)
        self.assertAlmostEqual(lt["phong"][0, 0], ks)
        self.assertAlmostEqual(lt["blinn"][0, 0], ks)
        # light at alpha from the normal on +x, eye at beta on -x: R.V = cos(alpha - beta), N.H = cos((alpha - beta)/2)
        al, be, s = math.radians(40), math.radians(25), 16
        Pp = np.array([0, 0, 0.0])
        light = 5 * np.array([math.sin(al), 0, math.cos(al)])
        eye = 7 * np.array([-math.sin(be), 0, math.cos(be)])
        lt = R.lighting([Pp], [(0, 0, 1.0)], light, eye=eye, kd=(1, 1, 1), ks=1.0, shininess=s, blinn_shininess=s)
        self.assertAlmostEqual(lt["diffuse"][0, 0], math.cos(al))
        self.assertAlmostEqual(lt["phong"][0, 0], math.cos(al - be) ** s)
        self.assertAlmostEqual(lt["blinn"][0, 0], math.cos((al - be) / 2) ** s)
        dark = R.lighting([Pp], [(0, 0, -1.0)], light, eye=eye)
        self.assertEqual(dark["phong"][0, 0], 0)

    def test_sphere(self):
        V, N, F = R.uv_sphere(10, 20)
        self.assertEqual(len(F), 360)
        for f in F:                                   # outward, counter-clockwise faces
            a, b, c = V[list(f)]
            self.assertGreater(np.cross(b - a, c - a) @ (a + b + c), 0)

    def test_shading_demo(self):
        r = R.shading_demo()
        self.assertGreater(r["max_diff_gouraud_phong"], 0.1)
        self.assertLess(r["rmse_phong"], r["rmse_gouraud"] / 2)
        self.assertEqual(r["triangles"], 360)


class Textures(unittest.TestCase):
    def test_pyramid(self):
        tex = R.checker_texture(64, 8)
        pyr = R.mip_pyramid(tex)
        self.assertEqual([p.shape[0] for p in pyr], [64, 32, 16, 8, 4, 2, 1])
        for p in pyr:
            self.assertAlmostEqual(p.mean(), tex.mean())
        o = R.mip_overhead(128)
        self.assertAlmostEqual(o["overhead"], (4 / 3) * (1 - 4.0 ** -8) - 1)
        self.assertAlmostEqual(o["overhead"], 1 / 3, places=4)

    def test_samplers(self):
        tex = R.checker_texture(16, 4)
        u = np.array([2.5, 5.5, 17.5])
        v = np.array([0.5, 0.5, 0.5])
        np.testing.assert_allclose(R.sample_bilinear(tex, u, v), R.sample_nearest(tex, u, v))   # texel centres
        np.testing.assert_allclose(R.sample_bilinear(tex, np.array([4.0]), np.array([0.5])), [0.5])
        pyr = R.mip_pyramid(tex)
        np.testing.assert_allclose(R.sample_trilinear(pyr, u, v, np.ones(3)), R.sample_bilinear(tex, u, v))
        np.testing.assert_allclose(R.sample_trilinear(pyr, u, v, np.full(3, 1e6)), tex.mean())

    def test_texture_demo(self):
        r = R.texture_demo()
        e = r["rmse"]
        self.assertGreater(e["point"], 2 * e["mip"])
        self.assertGreater(e["point"], 2 * e["ss16"])
        self.assertEqual(r["covered"], r["pixels"])
        self.assertLess(r["uv_raster_error"], 1e-6)


class Visibility(unittest.TestCase):
    def test_zbuffer(self):
        r = R.zbuffer_demo()
        self.assertGreater(r["a_in_front"], 100)
        self.assertGreater(r["b_in_front"], 100)
        self.assertLessEqual(r["zbuffer_wrong"], 3)                # only ties along the intersection line
        self.assertGreaterEqual(r["painter_wrong"], r["b_in_front"] - 3)
        c = r["counters_zbuffer"]
        self.assertEqual(c["covered"], c["depth_pass"] + c["depth_fail"])
        self.assertGreater(c["depth_fail"], 0)


def bernstein(P, t):
    P = np.asarray(P, float)
    n = len(P) - 1
    return sum(math.comb(n, i) * t ** i * (1 - t) ** (n - i) * P[i] for i in range(n + 1))


class Curves(unittest.TestCase):
    def test_de_casteljau(self):
        rng = np.random.default_rng(4)
        for n in range(1, 7):
            P = rng.normal(size=(n + 1, 2))
            for t in np.linspace(0, 1, 11):
                d = C.de_casteljau(P, t)
                np.testing.assert_allclose(d["point"], bernstein(P, t), atol=1e-12)
                self.assertEqual([len(l) for l in d["levels"]], list(range(n + 1, 0, -1)))

    def test_subdivide(self):
        P = [[0, 0], [1, 2], [3, 2.5], [4, 0]]
        for t in (0.5, 0.3):
            s = C.subdivide(P, t)
            for u in np.linspace(0, 1, 7):
                np.testing.assert_allclose(bernstein(s["left"], u), bernstein(P, t * u), atol=1e-12)
                np.testing.assert_allclose(bernstein(s["right"], u), bernstein(P, t + (1 - t) * u), atol=1e-12)

    def test_bspline_vs_scipy(self):
        rng = np.random.default_rng(5)
        for p in (1, 2, 3, 4):
            P = rng.normal(size=(8, 2))
            for knots in (C.uniform_knots(8, p), C.clamped_knots(8, p)):
                ref = BSpline(np.array(knots), P, p)
                ts = np.linspace(knots[p], knots[-p - 1], 23)[:-1]
                np.testing.assert_allclose(C.bspline(P, p, knots, ts), ref(ts), atol=1e-12)
                self.assertAlmostEqual(sum(C.basis(i, p, ts[5], knots) for i in range(8)), 1)
            k = C.clamped_knots(8, p)
            np.testing.assert_allclose(C.bspline(P, p, k, [k[0], k[-1]]), P[[0, -1]], atol=1e-12)

    def test_uniform_cubic_matrix(self):
        P = np.array([[0, 0], [1, 2], [3, 3], [4, 0], [6, -1.0]])
        M = np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]]) / 6
        for s in (0.0, 0.25, 0.7):
            t = 3 + s
            np.testing.assert_allclose(C.bspline(P, 3, C.uniform_knots(5, 3), [t])[0],
                                       np.array([s ** 3, s ** 2, s, 1]) @ M @ P[0:4], atol=1e-12)

    def test_c2(self):
        ctrl = ((0, 0), (1, 2), (3, 3), (4, 0), (6, -1), (7, 2), (9, 3))
        P = np.array(ctrl, float)
        for r in C.bspline_continuity(ctrl):
            self.assertLess(max(r["jump_c0"], r["jump_c1"], r["jump_c2"]), 1e-6)
            self.assertGreater(r["jump_c3"], 1)
            j = int(r["knot"])                     # at knot j: C'' = P[j-3] - 2 P[j-2] + P[j-1]
            np.testing.assert_allclose(r["d2_left"], P[j - 3] - 2 * P[j - 2] + P[j - 1], atol=1e-6)

    def test_catmull_clark(self):
        r = C.catmull_clark(levels=4)
        for lv in r["levels"]:
            k = lv["level"]
            self.assertEqual((lv["V"], lv["E"], lv["F"]), (6 * 4 ** k + 2, 12 * 4 ** k, 6 * 4 ** k))
            self.assertEqual(lv["euler"], 2)
            edges = C._edges(lv["faces"])
            self.assertTrue(all(len(f) == 2 for f in edges.values()))    # still closed
        radii = [lv["corner_radius"] for lv in r["levels"]]
        self.assertTrue(all(a > b for a, b in zip(radii, radii[1:])))
        # hand computation of the mask at a corner: (9 P + 4 sum e + sum f) / 24 = (-1/2, -1/2, -1/2)
        self.assertAlmostEqual(r["limit_radius"], math.sqrt(3) / 2)
        self.assertLess(radii[-1] - r["limit_radius"], 1e-3)
        V, F = C.cube_mesh()
        for _ in range(2):                          # the limit point does not depend on the level
            V, F = C.catmull_clark_step(V, F)
            np.testing.assert_allclose(C.limit_position(V, F, 0), (-0.5, -0.5, -0.5), atol=1e-12)


if __name__ == "__main__":
    unittest.main()
