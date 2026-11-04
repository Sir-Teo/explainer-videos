"""The World (explainer.stats.world) is the series' laboratory: its truth must be reproducible, stable as blocks are
added, and what the scenes say it is (videos/stats/SYLLABUS.md, section 2)."""

import unittest
import zlib

import numpy as np

from explainer.stats import museum
from explainer.stats.world import World


class WorldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w = World()

    def test_reproducible_from_the_seed(self):
        a, b = World(), World()
        np.testing.assert_array_equal(a.height[:1000], b.height[:1000])
        np.testing.assert_array_equal(a.sample(50, among=a.adult, seed=3), b.sample(50, among=b.adult, seed=3))

    def test_blocks_are_independent_streams(self):
        # a block's stream depends only on the seed and the block's name, so adding or using other blocks first
        # cannot change it
        fresh = World()
        _ = fresh.clinic, fresh.families  # touch other blocks first
        np.testing.assert_array_equal(fresh.income[:2000], self.w.income[:2000])
        g = np.random.Generator(np.random.PCG64(np.random.SeedSequence([1662, zlib.crc32(b"sex")])))
        np.testing.assert_array_equal(self.w.male, g.random(self.w.n) < 0.5)

    def test_population_shape(self):
        w = self.w
        self.assertEqual(w.n, 1_000_000)
        self.assertEqual(len(np.unique(w.town)), 200)
        h = w.height[w.adult]
        self.assertAlmostEqual(float(w.height[w.adult & w.male].mean()), 176.0, delta=0.1)
        self.assertAlmostEqual(float(w.height[w.adult & ~w.male].mean()), 163.0, delta=0.1)
        self.assertTrue(np.all(np.isnan(w.income[~w.adult])))
        y = w.income[w.adult]
        self.assertGreater(y.mean(), np.median(y))  # the Pareto tail drags the mean above the median
        self.assertAlmostEqual(w.truth("mean_height"), float(h.mean()))

    def test_pareto_tail_exponent_is_recovered(self):
        y = np.sort(self.w.income[self.w.adult])
        top = y[-2001:]
        hill = 1 / np.mean(np.log(top[1:] / top[0]))
        self.assertAlmostEqual(hill, World.PARETO_ALPHA, delta=0.25)

    def test_families_match_their_documented_correlation(self):
        f = self.w.families
        r = np.corrcoef((f["z_father"] + f["z_mother"]) / 2, f["z_child"])[0, 1]
        expected = World.HERITABLE * np.sqrt((1 + World.ASSORTATIVE) / 2)
        self.assertAlmostEqual(r, expected, delta=0.01)

    def test_clinic_shows_simpsons_reversal(self):
        c = self.w.clinic
        t, r, s = c["treated"], c["recovered"], c["severe"]
        for group in (s, ~s):
            self.assertGreater(r[t & group].mean(), r[~t & group].mean())
        self.assertLess(r[t].mean(), r[~t].mean())

    def test_sample_is_without_replacement_and_inside_the_pool(self):
        idx = self.w.sample(500, among=self.w.adult, seed=11)
        self.assertEqual(len(np.unique(idx)), 500)
        self.assertTrue(self.w.adult[idx].all())


class MuseumTests(unittest.TestCase):
    def test_arbuthnot_every_year_more_boys(self):
        self.assertEqual(len(museum.ARB_MALES), 82)
        self.assertTrue(all(m > f for m, f in zip(museum.ARB_MALES, museum.ARB_FEMALES)))
        self.assertEqual(museum.ARB_BURIALS[museum.ARB_YEARS.index(1665)], 97306)

    def test_stigler_chest_table(self):
        self.assertEqual(sum(museum.CHEST_COUNT), 5732)
        self.assertEqual(len(museum.CHEST_IN), len(museum.CHEST_COUNT))

    def test_anscombe_shares_its_statistics(self):
        stats = []
        for x, y in museum.ANSCOMBE.values():
            x, y = np.array(x, float), np.array(y, float)
            stats.append((x.mean(), y.mean(), x.var(ddof=1), np.corrcoef(x, y)[0, 1]))
        for s in stats[1:]:
            np.testing.assert_allclose(s, stats[0], atol=0.01)


if __name__ == "__main__":
    unittest.main()
