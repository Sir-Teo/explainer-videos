import tempfile
import unittest
from pathlib import Path

import numpy as np
from manim import BLUE, Scene, Text, VGroup, tempconfig

from explainer.ai.viz import Cloud3D


class CloudLayoutTests(unittest.TestCase):
    def test_dense_labels_stay_separate_when_the_view_rotates(self):
        rng = np.random.default_rng(3)
        xyz = rng.normal(0, 0.04, (12, 3))
        with tempfile.TemporaryDirectory() as directory:
            with tempconfig({"text_dir": str(Path(directory) / "texts")}):
                cloud = Cloud3D(xyz, [BLUE] * len(xyz),
                                labels={i: Text(f"word{i}", font_size=22) for i in range(len(xyz))})
        for angle in (0, 0.7, 1.8, 3.0):
            cloud.angle.set_value(angle)
            cloud.update()
            labels = list(cloud.label_of.values())
            for i, label in enumerate(labels):
                self.assertGreaterEqual(label.get_left()[0], -6.82)
                self.assertLessEqual(label.get_right()[0], 6.82)
                for other in labels[i + 1:]:
                    dx = min(label.get_right()[0], other.get_right()[0]) - max(label.get_left()[0], other.get_left()[0])
                    dy = min(label.get_top()[1], other.get_top()[1]) - max(label.get_bottom()[1], other.get_bottom()[1])
                    self.assertFalse(dx > 0 and dy > 0, (i, angle))

    def test_callouts_follow_points_when_label_groups_are_detached(self):
        xyz = np.random.default_rng(7).normal(0, 0.08, (8, 3))
        with tempfile.TemporaryDirectory() as directory:
            with tempconfig({"text_dir": str(Path(directory) / "texts")}):
                cloud = Cloud3D(xyz, [BLUE] * len(xyz),
                                labels={i: Text(f"word{i}", font_size=22) for i in range(len(xyz))})
                scene = Scene(skip_animations=True)
                scene.add(cloud)
                scene.remove(cloud.labels)
                scene.add(VGroup(*cloud.label_of.values()))
                cloud.angle.set_value(1.3)
                scene.update_mobjects(0)
        visible = 0
        for i, leader in enumerate(cloud.leaders):
            if leader.get_stroke_opacity() > 0:
                visible += 1
                np.testing.assert_allclose(leader.get_start(), cloud.project(xyz[i])[0], atol=1e-9)
        self.assertGreater(visible, 0)


if __name__ == "__main__":
    unittest.main()
