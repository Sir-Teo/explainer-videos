"""Behavior contracts for stored-path interpolation and encoded-frame duration."""
import ast
import math
from pathlib import Path
from types import SimpleNamespace

import numpy as np


def exercise(points, fps, duration, alphas):
    path = Path(__file__).resolve().parents[1] / 'videos/ai/ai21/common.py'
    tree = ast.parse(path.read_text())
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'play_path')
    states, plays = [], []
    class Panel:
        def pts(self, positions): return positions.copy()
    class DotSpy:
        def move_to(self, position): self.position = position.copy()
    class Scene:
        def play(self, animation, **kwargs):
            plays.append(kwargs)
            for alpha in alphas:
                animation.fn(animation.dots, alpha)
                states.append(np.array([dot.position for dot in animation.dots]))
    scope = dict(np=np, math=math, config=SimpleNamespace(frame_rate=fps), linear=lambda x: x,
                 UpdateFromAlphaFunc=lambda dots, fn: SimpleNamespace(dots=dots, fn=fn))
    exec(compile(ast.Module([fn], type_ignores=[]), str(path), 'exec'), scope)
    scope['play_path'](Scene(), Panel(), [DotSpy() for _ in range(points.shape[1])], points, duration)
    return states, plays


def test_stored_corner_is_followed_instead_of_cutting_the_endpoint_chord():
    path = np.array([[[0., 0.]], [[2., 0.]], [[2., 2.]]])
    states, _ = exercise(path, 15, 3., [-.1, .25, .5, .75, 1.1])
    np.testing.assert_allclose(np.array(states)[:, 0], [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]])


def test_one_animation_requests_a_whole_number_of_encoded_frames():
    path = np.array([[[0., 0.]], [[1., 1.]]])
    for fps, duration, expected in [(15, .075, 2), (30, .075, 3), (15, 4.2, 63),
                                    (30, 4.2, 126), (15, 3., 45), (30, 3., 90)]:
        _, plays = exercise(path, fps, duration, [0., 1.])
        assert len(plays) == 1
        assert abs(plays[0]['run_time'] * fps - expected) < 1e-9
