"""Tests for Part 51's ray tracing, BRDF and path tracing instruments (explainer/cs/graphics: ray, brdf, path).  Each
formula is checked against an independent computation: a closed form, a linear solve, brute force or quadrature."""

from __future__ import annotations

import math
import unittest

import numpy as np

from explainer.cs.graphics import brdf as B
from explainer.cs.graphics import path as P
from explainer.cs.graphics import ray as R


def _unit(rng, n):
    v = rng.standard_normal((n, 3))
    return v / np.linalg.norm(v, axis=1, keepdims=True)


class Intersections(unittest.TestCase):
    def test_sphere_known(self):
        t = R.ray_sphere([[0, 0, 0], [0, 0, 5], [0, 3, 0]], [[0, 0, 1], [0, 0, 1], [0, 0, 1]], [0, 0, 5], 1.0)
        self.assertAlmostEqual(t[0], 4.0)  # from outside: the near root
        self.assertAlmostEqual(t[1], 1.0)  # from the centre: the far root
        self.assertTrue(np.isinf(t[2]))  # a miss
        # a non-unit direction scales t
        self.assertAlmostEqual(R.ray_sphere([0, 0, 0], [0, 0, 2.0], [0, 0, 5], 1.0), 2.0)

    def test_sphere_brute_force(self):
        rng = np.random.default_rng(1)
        O = rng.uniform(-3, 3, (300, 3))
        D = _unit(rng, 300)
        c, r = np.array([0.2, -0.1, 0.3]), 1.3
        t = R.ray_sphere(O, D, c, r)
        # march each ray in small steps and find the first sign change of |p - c| - r
        s = np.linspace(1e-6, 12, 120_001)
        for i in range(300):
            g = np.linalg.norm(O[i] + s[:, None] * D[i] - c, axis=1) - r
            ch = np.nonzero(np.sign(g[1:]) != np.sign(g[:-1]))[0]
            if len(ch) == 0:
                self.assertTrue(np.isinf(t[i]))
            else:
                self.assertLess(abs(t[i] - s[ch[0]]), 2e-4)

    def test_moller_trumbore_vs_solve(self):
        rng = np.random.default_rng(2)
        n = 2000
        v0, v1, v2 = (rng.uniform(-1, 1, (n, 3)) for _ in range(3))
        O = rng.uniform(-2, 2, (n, 3))
        target = v0 + rng.uniform(-0.3, 1, (n, 1)) * (v1 - v0) + rng.uniform(-0.3, 1, (n, 1)) * (v2 - v0)
        D = target - O
        t, u, v, hit = R.moller_trumbore(O, D, v0, v1, v2)
        # independent: solve [-d, e1, e2] [t, u, v]^T = o - v0
        M = np.stack([-D, v1 - v0, v2 - v0], -1)
        x = np.linalg.solve(M, (O - v0)[..., None])[..., 0]
        ok = (x[:, 1] >= 0) & (x[:, 2] >= 0) & (x[:, 1] + x[:, 2] <= 1) & (x[:, 0] > 0)
        np.testing.assert_array_equal(hit, ok)
        np.testing.assert_allclose(t[hit], x[hit, 0], rtol=1e-9)
        np.testing.assert_allclose(u, x[:, 1], atol=1e-9)
        np.testing.assert_allclose(v, x[:, 2], atol=1e-9)
        self.assertGreater(hit.mean(), 0.2)

    def test_snell_and_fresnel(self):
        rng = np.random.default_rng(3)
        n = np.array([0, 0, 1.0])
        for eta in (1 / 1.5, 1.5):
            d = -_unit(rng, 500) * np.array([1, 1, 1])
            d[:, 2] = -np.abs(d[:, 2])
            t, cos_t, tir = R.refract(d, n, eta)
            sin_i = np.sqrt(1 - d[:, 2] ** 2)
            ok = ~tir
            np.testing.assert_allclose(np.linalg.norm(t[ok], axis=1), 1, atol=1e-12)
            np.testing.assert_allclose(np.sqrt(1 - t[ok, 2] ** 2), eta * sin_i[ok], atol=1e-12)  # n1 sin = n2 sin
            np.testing.assert_array_equal(tir, eta * sin_i > 1)
        self.assertAlmostEqual(float(R.schlick(1.0, 1.0, 1.5)), 0.04)
        self.assertAlmostEqual(float(R.fresnel_dielectric(1.0, 1.0, 1.5)), 0.04)
        self.assertAlmostEqual(float(R.schlick(0.0, 1.0, 1.5)), 1.0)
        c = np.linspace(0, 1, 501)
        self.assertLess(np.abs(R.schlick(c, 1, 1.5) - R.fresnel_dielectric(c, 1, 1.5)).max(), 0.04)


class Bvh(unittest.TestCase):
    def test_mesh_and_builder_contracts(self):
        self.assertEqual(R.terrain(6).shape, (6, 3, 3))
        for n in (0, 1, 5):
            with self.assertRaises(ValueError):
                R.terrain(n)
        for kwargs in ({"method": "typo"}, {"max_leaf": 0}, {"nbins": 1}):
            with self.assertRaises(ValueError):
                R.build_bvh(R.terrain(2), **kwargs)
        with self.assertRaises(ValueError):
            R.build_bvh(np.empty((0, 3, 3)))

    def test_matches_brute_force(self):
        O, D = R.camera_rays(24)
        for tris in (R.terrain(2000, seed=5), R.icosphere(3, 0.4) + np.array([0.5, 0.5, 0.0])):
            tb, hb = R.brute_force(tris, O, D)
            for method in ("sah", "median"):
                tree = R.build_bvh(tris, method)
                t, h, visits, tests = R.traverse(tree, O, D)
                fin = np.isfinite(tb)
                np.testing.assert_array_equal(np.isfinite(t), fin)
                np.testing.assert_allclose(t[fin], tb[fin], rtol=1e-12)
                self.assertLess(tests.mean(), len(tris) / 20)
                # every triangle is in exactly one leaf
                self.assertEqual(sorted(tree["idx"].tolist()), list(range(len(tris))))
                self.assertEqual(int(tree["count"][tree["count"] > 0].sum()), len(tris))

    def test_terrain_size(self):
        for n in (100, 1000, 10_000):
            self.assertEqual(len(R.terrain(n)), n)
        self.assertEqual(len(R.icosphere(2)), 320)

    def test_scaling(self):
        rows = R.bvh_experiment(ns=(1000, 100_000), n_side=32, check_rays=128)
        small, big = rows
        self.assertEqual(big["brute_tests"], 100_000)
        for r in rows:
            self.assertEqual(r["agree"], 1.0)
            self.assertLessEqual(r["sah_tests"], r["median_tests"] * 1.05)
        # 100x the triangles: brute force does 100x the work; the BVH's node visits grow like log n
        self.assertLess(big["sah_visits"] / small["sah_visits"], 3.0)
        self.assertLess(big["sah_tests"], 10)


class Whitted(unittest.TestCase):
    def test_render(self):
        r = R.whitted(40, 30)
        c = r["counts"]
        self.assertEqual(c["primary"], 1200)
        self.assertGreater(c["shadow"], 0)
        self.assertGreater(c["reflection"], 0)
        self.assertGreater(c["refraction"], 0)
        self.assertEqual(c["total"], c["primary"] + c["shadow"] + c["reflection"] + c["refraction"])
        self.assertEqual(r["image"].shape, (30, 40, 3))
        self.assertTrue(np.all(np.isfinite(r["image"])) and r["image"].min() >= 0)
        self.assertEqual(r["tir"], 0)  # a ray that enters a sphere can always leave it (symmetric angles)


class Brdfs(unittest.TestCase):
    def test_closed_form_albedos(self):
        z = B.direction(0)
        self.assertAlmostEqual(B.albedo_quadrature("lambert", 1.0, B.direction(50)), 1.0, places=6)
        for n in (1, 10, 100):  # normalized Phong reflects everything at normal incidence
            self.assertAlmostEqual(B.albedo_quadrature("phong", n, z), 1.0, places=5)

    def test_ggx_normalization_and_masking(self):
        for a in (0.1, 0.4, 1.0):
            area = B.sphere_integral(lambda h: B.ggx_d(h[..., 2], a) * np.clip(h[..., 2], 0, None), 2048, 32,
                                     upper_only=True)
            self.assertAlmostEqual(area, 1.0, places=6)
        # Smith's G1 is the one that makes the projected visible microfacet area equal the projected macro-surface
        # area: integral G1(v) max(0, v.h) D(h) dw_h = cos theta_v (Heitz 2014)
        for a, th in ((0.3, 60), (0.8, 75), (0.5, 0)):
            v = B.direction(th)
            val = B.sphere_integral(lambda h: B.smith_g1(v[2], a) * np.clip(B._dot(h, v), 0, None) *
                                    B.ggx_d(h[..., 2], a), 1024, 1024, upper_only=True)
            self.assertAlmostEqual(val, math.cos(math.radians(th)), places=4)

    def test_white_furnace(self):
        rows = B.white_furnace(roughness=(0.1, 1.0), view_deg=(0, 60), exponents=(10,), samples=100_000)
        for r in rows:
            if r["model"] != "blinn_phong":  # (n + 8) / 8 pi is only approximately normalized
                self.assertLessEqual(r["quad"], 1.0 + 1e-6)
            self.assertLess(abs(r["mc"] - r["quad"]), 4 * r["mc_se"] + 1e-3)
        q = {(r["model"], r["param"], r["theta_deg"]): r["quad"] for r in rows}
        self.assertGreater(q[("ggx", 0.1, 0.0)], 0.98)  # smooth: nearly no loss
        self.assertLess(q[("ggx", 1.0, 0.0)], 0.4)  # rough: single scattering loses most of the energy
        self.assertAlmostEqual(q[("lambert", 1.0, 60.0)], 1.0, places=6)
        self.assertAlmostEqual(q[("phong", 10.0, 0.0)], 1.0, places=5)

    def test_reciprocity(self):
        for m, err in B.reciprocity(2000).items():
            self.assertLess(err, 1e-12, m)

    def test_pdfs_integrate_to_one(self):
        for k, v in B.pdf_integrals().items():
            self.assertAlmostEqual(v, 1.0, delta=2e-3, msg=k)

    def test_samplers_follow_their_pdfs(self):
        rng = np.random.default_rng(4)
        N = 400_000
        u1, u2 = rng.random(N), rng.random(N)
        w, p = B.sample_cosine_hemisphere(u1, u2)
        self.assertAlmostEqual(w[:, 2].mean(), 2 / 3, delta=3e-3)  # E[cos] under cos / pi
        np.testing.assert_allclose(p, B.pdf_cosine_hemisphere(w))
        w, p = B.sample_uniform_hemisphere(u1, u2)
        self.assertAlmostEqual(w[:, 2].mean(), 1 / 2, delta=3e-3)
        ax = B._normalize(np.array([0.3, 0.4, 0.8]))
        for n in (5, 50):
            w, p = B.sample_phong_lobe(ax, n, u1, u2)
            np.testing.assert_allclose(np.linalg.norm(w, axis=1), 1, atol=1e-12)
            self.assertAlmostEqual((w @ ax).mean(), (n + 1) / (n + 2), delta=2e-3)
        w, p = B.sample_cone(ax, 0.9, u1, u2)
        self.assertGreaterEqual((w @ ax).min(), 0.9 - 1e-12)
        self.assertAlmostEqual((w @ ax).mean(), 0.95, delta=1e-3)
        wo = B.direction(40)
        for a in (0.2, 0.7):
            w, p = B.sample_ggx(wo, a, u1, u2)
            np.testing.assert_allclose(p, B.pdf_ggx(w, wo, a), rtol=1e-9)
            est = np.clip(w[:, 2], 0, None) / p  # E[g / p] = integral g dw = pi for g = cos+
            self.assertAlmostEqual(est.mean() / math.pi, 1.0, delta=4 * est.std() / math.sqrt(N) / math.pi + 1e-3)

    def test_mis(self):
        rows = B.mis_experiment(trials=1500)
        cell = {(r["n"], r["r"]): r for r in rows}
        for r in rows:
            for k, v in r["mean"].items():  # every estimator is unbiased
                self.assertLess(abs(v - r["exact"]) / r["exact"], 6 * r[f"rel_rmse_{k}"] / math.sqrt(1500) + 1e-3)
            self.assertLess(r["rel_rmse_power"], 0.15)  # MIS never fails
            self.assertLess(r["rel_rmse_balance"], 0.15)
        self.assertGreater(cell[(10, 0.05)]["rel_rmse_brdf"], 1.0)  # BRDF sampling misses a small light
        self.assertGreater(cell[(1000, 1.0)]["rel_rmse_light"], 0.5)  # light sampling misses a sharp lobe
        # small light: L ~ f(w_r) cos(theta_r) times the light's solid angle 2 pi (1 - cos theta_max)
        r = cell[(10, 0.05)]
        cm = math.sqrt(1 - (0.05 / 3) ** 2)
        self.assertAlmostEqual(r["exact"] / (12 / (2 * math.pi) * math.cos(math.pi / 4) * 2 * math.pi * (1 - cm)), 1,
                               delta=2e-3)


def _view_factor_corner(a, b, c):
    """View factor from a differential area to a parallel a x b rectangle with one corner straight above at height c
    (Howell's catalogue of configuration factors, B-3)."""
    A, Bb = a / c, b / c
    sa, sb = math.sqrt(1 + A * A), math.sqrt(1 + Bb * Bb)
    return (A / sa * math.atan(Bb / sa) + Bb / sb * math.atan(A / sb)) / (2 * math.pi)


def _view_factor(x, z, x0, x1, z0, z1, c):
    """Point (x, z) below a parallel rectangle [x0, x1] x [z0, z1] at height c, by superposing corner rectangles."""
    def corner(xa, za):
        sx, sz = np.sign(xa - x), np.sign(za - z)
        return sx * sz * _view_factor_corner(abs(xa - x), abs(za - z), c)
    return corner(x1, z1) - corner(x0, z1) - corner(x1, z0) + corner(x0, z0)


class PathTracer(unittest.TestCase):
    def test_furnace_neumann_series_exact(self):
        # every surface albedo 0.5 and emitting 1: bounce k is exactly 0.5^k, and with cosine sampling every path
        # carries exactly that, so there is no noise at all
        r = P.render(4, 16, 16, 0, nee=False, roulette=False, max_depth=6, bins=8, scene=P.furnace_scene(0.5))
        for k in range(7):
            np.testing.assert_allclose(r["bounces"][k], 0.5 ** k, atol=1e-12)
        np.testing.assert_allclose(r["bounces"][7], 0, atol=1e-15)
        np.testing.assert_allclose(r["image"], r["bounces"].sum(0))

    def test_furnace_with_nee_roulette_uniform(self):
        sc = P.furnace_scene(0.5, light=True)
        for kw in ({"nee": True, "roulette": True}, {"nee": True, "roulette": False, "cosine": False}):
            M = np.array([P.render(32, 16, 16, s, max_depth=6, bins=8, scene=sc, **kw)["bounce_mean"]
                          for s in range(8)])
            mean, se = M.mean(0), M.std(0, ddof=1) / math.sqrt(8)
            for k in range(7):
                self.assertLess(abs(mean[k] - 0.5 ** k), 4.5 * se[k] + 1e-9, (kw, k))

    def test_direct_lighting_closed_form(self):
        # without spheres, a floor point sees the whole light: bounce 1 = rho Le F with F the point-to-rectangle view
        # factor (Lambertian: L_o = rho / pi * Le * pi F)
        sc = P.cornell_scene(spheres=False)
        W = H = 32
        r = P.render(1024, W, H, 7, scene=sc)
        eye, fw, rt, up, th = P._camera(sc["camera"], W, H)
        lr = sc["rects"][sc["light"]]
        for py, px in ((29, 16), (27, 12), (30, 22), (28, 19)):
            vals = []
            for jy in (0.25, 0.75):  # average the closed form over the pixel
                for jx in (0.25, 0.75):
                    sx = (2 * (px + jx) / W - 1) * th
                    sy = (1 - 2 * (py + jy) / H) * th
                    d = fw + sx * rt + sy * up
                    p = eye + (-eye[1] / d[1]) * d
                    vals.append(_view_factor(p[0], p[2], lr["lo"][0], lr["hi"][0], lr["lo"][1], lr["hi"][1],
                                             lr["pos"]))
            expect = 0.73 * np.array(lr["emit"]) * np.mean(vals)
            np.testing.assert_allclose(r["bounces"][1][py, px], expect, rtol=0.03)

    def test_bounce_zero_is_the_light(self):
        r = P.render(16, 64, 64, 0)
        b0 = r["bounces"][0]
        self.assertAlmostEqual(float(b0.max()), 17.0, places=9)  # a pixel entirely on the light sees L_e exactly
        self.assertGreater(r["bounce_mean"][1], r["bounce_mean"][2])
        self.assertGreater(r["bounce_mean"][2], r["bounce_mean"][3])

    def test_roulette_unbiased(self):
        res = P.roulette_check(renders=6, spp=16, W=16, H=16)
        self.assertLess(abs(res["z"]), 4)
        self.assertLess(res["path_length_rr"], res["path_length_no_rr"])

    def test_convergence_and_strategies(self):
        ref = P.reference(1024, 32, 32)
        c = P.convergence((1, 4, 16, 64), ref=ref, W=32, H=32)
        self.assertGreater(c["slope_surfaces"], -0.65)
        self.assertLess(c["slope_surfaces"], -0.35)
        rows = {r["name"]: r for r in P.sampling_comparison(16, ref=ref, W=32, H=32)}
        self.assertLess(rows["cosine + NEE"]["rmse_surfaces"], rows["cosine, no NEE"]["rmse_surfaces"])
        self.assertLess(rows["uniform + NEE"]["rmse_surfaces"], rows["uniform, no NEE"]["rmse_surfaces"])

    def test_denoise(self):
        ref = P.reference(512, 64, 64)
        d = P.denoise_experiment(16, ref=ref, W=64, H=64)
        self.assertLess(d["rmse_surfaces_after"], 0.8 * d["rmse_surfaces_before"])
        # a constant image with a constant g-buffer is a fixed point of the filter
        g = {k: np.ones((8, 8, 3)) * 0.5 for k in ("normal", "albedo", "position")}
        np.testing.assert_allclose(P.denoise(np.full((8, 8, 3), 0.3), g), 0.3)

    def test_srgb(self):
        x = np.array([[[0.0, 0.5, 1.0]]])
        np.testing.assert_array_equal(P.to_srgb8(x, curve="clip")[0, 0], [0, 188, 255])
        np.testing.assert_array_equal(P.to_srgb8(np.array([[[1.0, 1e9, 0.002]]]))[0, 0], [188, 255, 7])


if __name__ == "__main__":
    unittest.main()
