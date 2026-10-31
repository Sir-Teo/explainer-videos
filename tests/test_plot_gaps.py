import unittest

import numpy as np
from manim import Axes, BLUE

from explainer.ai.viz import curve
from videos.ai.ai10.common import seed_band


class PlotGapTests(unittest.TestCase):
    def test_missing_pole_does_not_join_opposite_branches(self):
        ax = Axes(x_range=[-3, 3], y_range=[-3, 3])
        for smooth in (False, True):
            with self.subTest(smooth=smooth):
                line = curve(ax, [-2, -1, 0, 1, 2], [-.5, -1, np.nan, 1, .5], BLUE, smooth=smooth)
                paths = line.get_subpaths()
                self.assertEqual(len(paths), 2)
                self.assertTrue(np.isfinite(line.points).all())
                self.assertLess(max(ax.p2c(p)[0] for p in paths[0]), 0)
                self.assertGreater(min(ax.p2c(p)[0] for p in paths[1]), 0)

    def test_zoom_keeps_original_seed_mean_and_omits_off_scale_values(self):
        ax = Axes(x_range=[0, 4], y_range=[0, .08])
        # Clipping each seed before averaging would fabricate a 6% first point.
        runs = [[.04, .03, .04, .03], [.20, .05, .08, .05]]
        plot = seed_band(ax, [0, 1, 2, 3], runs, BLUE, ylim=(0, .08))
        anchors = plot[1].get_start_anchors()
        values = np.array([ax.p2c(p)[:2] for p in anchors])
        self.assertAlmostEqual(values[0, 0], 1)
        self.assertAlmostEqual(values[0, 1], .04)
        self.assertAlmostEqual(values[1, 1], .06)


if __name__ == "__main__":
    unittest.main()
