import tempfile
import unittest
from pathlib import Path

import numpy as np
from manim import tempconfig

from videos.ai.ai1.common import letter_bars, wrap_words
from videos.ai.ai1.s08_cross_entropy import density_ceiling, gaussian_density


class LetterBarTests(unittest.TestCase):
    def test_labels_do_not_rescale_bars_or_shift_their_baseline(self):
        with tempfile.TemporaryDirectory() as directory:
            with tempconfig({"text_dir": str(Path(directory) / "texts")}):
                chart = letter_bars(np.ones(27) / 27, width=12, height=3.4, base=(0, -2.3))
        for i, bar in enumerate(chart.bars):
            self.assertAlmostEqual(bar.height, 3.4)
            self.assertAlmostEqual(bar.get_bottom()[1], -2.3)
            self.assertAlmostEqual(bar.get_x(), -6 + (i + 0.5) * 12 / 27)


class GuessingTextTests(unittest.TestCase):
    def test_wrapping_preserves_every_character_for_rank_alignment(self):
        for text in ("", "word ", "  one  two   ", "one\ntwo", "one\ttwo", "abcdefgh"):
            with self.subTest(text=text):
                self.assertEqual("".join(wrap_words(text, 5)), text)

    def test_shannon_sentence_keeps_the_established_line_breaks(self):
        from videos.ai.ai1.compute import SHANNON_SENTENCE

        self.assertEqual(wrap_words(SHANNON_SENTENCE, 36), [
            "there is no reverse on a motorcycle ",
            "a friend of mine found this out ",
            "rather dramatically the other day",
        ])


class KLDensityTests(unittest.TestCase):
    def test_narrow_bell_keeps_its_probability_mass_instead_of_flattening(self):
        x = np.linspace(-4, 4, 10001)
        density = gaussian_density(x, 0, 0.2)
        self.assertGreater(density.max(), 0.7)
        self.assertAlmostEqual(float(np.sum((density[:-1] + density[1:]) * np.diff(x) / 2)), 1.0, places=6)

    def test_shared_scale_contains_all_intermediate_fits(self):
        # The narrowest bell can occur before convergence, in either panel.
        left = np.array([[0, 1.0, 2], [0, 0.15, 1], [0, 2.0, 0]])
        right = np.array([[1, 0.8, 2], [2, 0.6, 0]])
        ceiling = density_ceiling(np.array([0.2, 0.8]), left, right)
        for path in (left, right):
            for mean, sigma, _ in path:
                self.assertGreater(ceiling, float(gaussian_density([mean], mean, sigma)[0]))
        self.assertGreater(ceiling, 0.8)


if __name__ == "__main__":
    unittest.main()
