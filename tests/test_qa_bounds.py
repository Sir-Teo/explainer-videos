import unittest

import numpy as np

from manim import MovingCamera, Rectangle, ThreeDCamera, VGroup

from tools.qa_series import visible_text_bounds


class BoundsTests(unittest.TestCase):
    def test_visible_glyphs_survive_transparent_container(self):
        glyph = Rectangle(width=2, height=1, fill_opacity=1).move_to([8, 0, 0])
        container = VGroup(glyph)
        container.fill_opacity = 0
        self.assertEqual(visible_text_bounds(container), [7, 9, -0.5, 0.5])

    def test_invisible_reservation_does_not_expand_bounds(self):
        glyph = Rectangle(width=2, height=1, fill_opacity=1)
        hidden = Rectangle(width=2, height=1).move_to([9, 0, 0]).set_opacity(0)
        self.assertEqual(visible_text_bounds(VGroup(glyph, hidden)), [-1, 1, -0.5, 0.5])

    def test_floor_label_uses_projected_screen_position(self):
        camera = ThreeDCamera(phi=np.pi / 2, theta=-np.pi / 2)
        label = Rectangle(width=1, height=0.2, fill_opacity=1)
        label.rotate(np.pi / 2, axis=np.array([1, 0, 0])).move_to([0, -5, 0])
        self.assertLess(visible_text_bounds(label)[2], -4)
        bounds = visible_text_bounds(label, camera)
        self.assertGreater(bounds[2], -1)
        self.assertLess(bounds[3], 1)

    def test_fixed_screen_label_ignores_3d_zoom(self):
        camera = ThreeDCamera(zoom=0.25)
        label = Rectangle(width=2, height=1, fill_opacity=1).move_to([8, 0, 0])
        camera.add_fixed_in_frame_mobjects(label)
        self.assertEqual(visible_text_bounds(label, camera), [7, 9, -0.5, 0.5])

    def test_moving_camera_accounts_for_pan_and_zoom(self):
        camera = MovingCamera()
        camera.frame.scale(0.5).move_to([10, 0, 0])
        label = Rectangle(width=1, height=0.5, fill_opacity=1).move_to([10, 0, 0])
        np.testing.assert_allclose(visible_text_bounds(label, camera), [-1, 1, -0.5, 0.5])


if __name__ == "__main__":
    unittest.main()
