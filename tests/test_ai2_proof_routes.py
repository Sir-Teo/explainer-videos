import unittest

import numpy as np
from manim import Rectangle

from videos.ai.ai2.s09_logic import proof_edge


class ProofRouteTests(unittest.TestCase):
    def assert_avoids(self, edge, obstacles):
        # Inspect the actual polyline, independently of the route's search.
        anchors = np.asarray(edge.get_anchors())
        for start, end in zip(anchors, anchors[1:]):
            samples = start + (end - start) * np.linspace(0, 1, 401)[:, None]
            for box in obstacles:
                inside = ((samples[:, 0] > box.get_left()[0] - 0.05)
                          & (samples[:, 0] < box.get_right()[0] + 0.05)
                          & (samples[:, 1] > box.get_bottom()[1] - 0.05)
                          & (samples[:, 1] < box.get_top()[1] + 0.05))
                self.assertFalse(inside.any(), "proof edge crosses an unrelated clause")

    def test_long_edge_routes_around_intermediate_clauses(self):
        boxes = {
            "parent": Rectangle(width=1.6, height=0.7).move_to([0, 2, 0]),
            "child": Rectangle(width=1.6, height=0.7).move_to([0, -2, 0]),
            "middle": Rectangle(width=2, height=0.8),
            "left": Rectangle(width=0.7, height=0.8).move_to([-1.5, 0, 0]),
        }
        edge = proof_edge(boxes, "parent", "child")
        self.assertGreater(len(edge.get_anchors()), 2)
        np.testing.assert_allclose(edge.get_start(), boxes["parent"].get_bottom())
        np.testing.assert_allclose(edge.get_tip().get_tip_point(), boxes["child"].get_top())
        self.assert_avoids(edge, [boxes["middle"], boxes["left"]])
        self.assertLess(np.max(np.abs(edge.get_all_points()[:, 0])), 7)

    def test_clear_edge_keeps_direct_connection_and_conclusion_tip(self):
        boxes = {
            "parent": Rectangle(width=1, height=0.5).move_to([-1, 1, 0]),
            "child": Rectangle(width=1, height=0.5).move_to([1, -1, 0]),
            "unrelated": Rectangle(width=1, height=0.5).move_to([-3, 0, 0]),
        }
        edge = proof_edge(boxes, "parent", "child")
        self.assertEqual(len(edge.get_anchors()), 2)
        np.testing.assert_allclose(edge.get_start(), boxes["parent"].get_bottom())
        np.testing.assert_allclose(edge.get_tip().get_tip_point(), boxes["child"].get_top())
        self.assert_avoids(edge, [boxes["unrelated"]])


if __name__ == "__main__":
    unittest.main()
