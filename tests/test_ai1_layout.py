import tempfile
import unittest
from pathlib import Path

import numpy as np
from manim import tempconfig

from videos.ai.ai1.common import letter_bars


class LetterBarTests(unittest.TestCase):
    def test_labels_do_not_rescale_bars_or_shift_their_baseline(self):
        with tempfile.TemporaryDirectory() as directory:
            with tempconfig({"text_dir": str(Path(directory) / "texts")}):
                chart = letter_bars(np.ones(27) / 27, width=12, height=3.4, base=(0, -2.3))
        for i, bar in enumerate(chart.bars):
            self.assertAlmostEqual(bar.height, 3.4)
            self.assertAlmostEqual(bar.get_bottom()[1], -2.3)
            self.assertAlmostEqual(bar.get_x(), -6 + (i + 0.5) * 12 / 27)


if __name__ == "__main__":
    unittest.main()
