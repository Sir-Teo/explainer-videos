"""Orthogonal scene stages keep distances throughout and preserve final maps.

Read only the small matrix/animation expressions with AST; no Part 3 import,
model, cache, scene, renderer or LaTeX process is needed.
"""
import ast
import math
from pathlib import Path
import unittest

import numpy as np


PART = Path(__file__).resolve().parents[1] / 'videos/ai/ai3'


def execute(nodes, scope):
    module = ast.Module(body=nodes, type_ignores=[])
    assert not any(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(module))
    exec(compile(module, '<part3-rotation-expression>', 'exec'), scope)


def scene_method(filename, name):
    tree = ast.parse((PART / filename).read_text())
    return tree, next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == name)


def assigned(node, name):
    return isinstance(node, ast.Assign) and any(
        isinstance(t, ast.Name) and t.id == name
        or isinstance(t, ast.Tuple) and any(isinstance(x, ast.Name) and x.id == name for x in t.elts)
        for t in node.targets
    )


def turn(target, angle, about_point):
    return ('turn', float(angle), np.array(about_point, dtype=float), target)


def matrix_action(matrix, target, about_point=None):
    return ('matrix', np.array(matrix, dtype=float),
            np.zeros(3) if about_point is None else np.array(about_point, dtype=float), target)


def at_phase(action, alpha):
    kind, value, pivot, _ = action
    if kind == 'turn':
        angle = alpha * value
        matrix = np.array([[math.cos(angle), -math.sin(angle)],
                           [math.sin(angle), math.cos(angle)]])
    else:
        # ApplyMatrix's straight point interpolation is valid for the stretch,
        # but this path violates distance invariance if used for a true turn.
        matrix = (1 - alpha) * np.eye(2) + alpha * value
    return matrix, pivot[:2]


class RotationPathsTest(unittest.TestCase):
    def assert_rigid_path(self, action, expected_matrix, pivot):
        points = np.array([[.3, -.9], [1.4, .6], [-.7, .2], [.8, 1.2]]) + pivot[:2]
        radii = np.linalg.norm(points - pivot[:2], axis=1)
        distances = np.linalg.norm(points[:, None] - points[None, :], axis=2)
        for alpha in np.linspace(0, 1, 41):
            matrix, actual_pivot = at_phase(action, float(alpha))
            np.testing.assert_allclose(actual_pivot, pivot[:2], atol=1e-14)
            moved = (points - actual_pivot) @ matrix.T + actual_pivot
            np.testing.assert_allclose(np.linalg.norm(moved - actual_pivot, axis=1), radii, atol=1e-13)
            np.testing.assert_allclose(np.linalg.norm(moved[:, None] - moved[None, :], axis=2),
                                       distances, atol=1e-13)
        np.testing.assert_allclose(at_phase(action, 1)[0], expected_matrix, atol=1e-14)

    def test_svd_turns_preserve_distances_and_exact_factorization(self):
        tree, method = scene_method('s08_svd.py', 'three_moves')
        scope = dict(np=np, math=math)
        execute([n for n in tree.body if assigned(n, 'A')
                 or isinstance(n, ast.FunctionDef) and n.name == 'svd2'], scope)
        u, singular_values, vt = scope['svd2'](scope['A'])
        branch = next(n for n in ast.walk(method) if assigned(n, 'move'))
        endpoint = np.eye(2)
        for k, matrix in enumerate((vt, np.diag(singular_values), u)):
            with self.subTest(stage=k):
                stage = dict(scope, k=k, M=matrix, g=object(), ORIGIN=np.zeros(3),
                             Rotate=turn, ApplyMatrix=matrix_action)
                execute([branch], stage)
                if k != 1:
                    self.assertGreater(np.linalg.det(matrix), 0)
                    self.assert_rigid_path(stage['move'], matrix, np.zeros(3))
                endpoint = at_phase(stage['move'], 1)[0] @ endpoint
        np.testing.assert_allclose(endpoint, scope['A'], atol=1e-14)

    def test_spectral_turns_preserve_distances_and_symmetric_map(self):
        _, method = scene_method('s06_eigen.py', 'symmetric')
        helper = ast.parse((PART / 'common.py').read_text())
        scope = dict(np=np, math=math, PI=math.pi)
        execute([next(n for n in helper.body if isinstance(n, ast.FunctionDef) and n.name == 'rot')], scope)
        for name in ('S', 'lam', 'Lm', 'Qr'):
            execute([next(n for n in method.body if assigned(n, name))], scope)
        branch = next(n for n in ast.walk(method) if assigned(n, 'move'))
        endpoint = np.eye(2)
        for k, matrix in enumerate((scope['Qr'], scope['Lm'], scope['Qr'].T)):
            stage = dict(scope, k=k, M=matrix, g=object(), ORIGIN=np.zeros(3),
                         Rotate=turn, ApplyMatrix=matrix_action)
            execute([branch], stage)
            if k != 1:
                self.assert_rigid_path(stage['move'], matrix, np.zeros(3))
            endpoint = at_phase(stage['move'], 1)[0] @ endpoint
        np.testing.assert_allclose(endpoint, scope['S'], atol=1e-14)

    def test_both_composition_orders_rotate_grid_and_shapes_about_panel_pivot(self):
        _, method = scene_method('s04_matrices.py', 'composition')
        scope = dict(np=np)
        execute([n for n in method.body if assigned(n, 'R') or assigned(n, 'S')], scope)
        branch = next(n for n in ast.walk(method) if isinstance(n, ast.If)
                      and ast.unparse(n.test) == 'M is R')
        for j, (first, second) in enumerate(((scope['R'], scope['S']), (scope['S'], scope['R']))):
            pivot = np.array([-3.5 + 7 * j, -.4, 0])
            endpoint = [np.eye(2), np.eye(2)]
            for matrix in (first, second):
                stage = dict(scope, M=matrix, c=pivot, g=['grid', 'square', 'i', 'j'],
                             PI=math.pi, Rotate=turn, ApplyMatrix=matrix_action, anims=[])
                execute([branch], stage)
                self.assertEqual(len(stage['anims']), 2)
                for i, action in enumerate(stage['anims']):
                    if matrix is scope['R']:
                        self.assert_rigid_path(action, matrix, pivot)
                    endpoint[i] = at_phase(action, 1)[0] @ endpoint[i]
            for actual in endpoint:
                np.testing.assert_allclose(actual, second @ first, atol=1e-14)


if __name__ == '__main__':
    unittest.main()
