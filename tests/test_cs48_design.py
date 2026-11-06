import unittest

from explainer.cs.design import blocks, keys


class Blocks(unittest.TestCase):
    def test_maglev_balanced(self):
        t = blocks.maglev_table([f"b{i}" for i in range(7)], M=251)
        counts = [t.count(i) for i in range(7)]
        self.assertLessEqual(max(counts) - min(counts), 1)

    def test_che_close_to_lru(self):
        trace, p = blocks.zipf_trace(100_000, 20_000, 0.9)
        self.assertAlmostEqual(blocks.lru_hits(trace.tolist(), 500), blocks.che(p, 500), delta=0.03)

    def test_stampede(self):
        self.assertGreater(blocks.stampede()["recomputations"], 10 * blocks.stampede(early=True)["recomputations"])

    def test_token_bucket_envelope(self):
        arr = [i * 0.01 for i in range(2000)]
        out = blocks.token_bucket(arr, rate=5.0, burst=10)
        self.assertTrue(blocks.envelope_ok(out, 5.0, 10)[0])


class Keys(unittest.TestCase):
    def test_curves_are_bijections(self):
        for f in (keys.morton, keys.hilbert):
            self.assertEqual(sorted(f(x, y, 3) for x in range(8) for y in range(8)), list(range(64)))

    def test_hilbert_adjacent(self):
        pts = keys.curve_points(3)["hilbert"]
        self.assertTrue(all(abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1 for a, b in zip(pts, pts[1:])))

    def test_geohash(self):
        self.assertTrue(keys.geohash(51.5072, -0.1276).startswith("gcpv"))

    def test_birthday(self):
        self.assertAlmostEqual(keys.birthday(ns=(2.71e18,))[0]["p"], 0.5, delta=0.01)


if __name__ == "__main__":
    unittest.main()
