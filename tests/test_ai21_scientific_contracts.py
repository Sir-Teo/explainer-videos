"""Small independent analytic checks; never train models or load production caches."""
import ast
import importlib.util
import math
from pathlib import Path

import numpy as np

PART = Path(__file__).resolve().parents[1] / 'videos/ai/ai21'


def functions(filename, names):
    tree = ast.parse((PART / filename).read_text())
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    scope = {'np': np, 'math': math, 'SMAX': 80., 'SMIN': .002}
    exec(compile(ast.Module(nodes, type_ignores=[]), filename, 'exec'), scope)
    return scope


def test_midpoint_data_prediction_update_has_correct_endpoints():
    s = functions('exact.py', {'sigmas', 'solve'})
    z = np.array([[.2, -.4], [.8, 1.2]])
    target = np.array([.7, -.3])
    got, nfe = s['solve'](lambda x, sigma: np.broadcast_to(target, x.shape), z, 'dpm2', 8)
    # Exact integration of x'=(x-D)/sigma when D is constant.
    expected = .002 * z + (1 - .002 / 80) * target
    np.testing.assert_allclose(got, expected, atol=1e-12)
    assert nfe == 16


def test_dsm_consumers_convert_noise_terms_to_half_squared_score_error():
    tree = ast.parse((PART / 's05_dsm.py').read_text())
    fn = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'check')
    assignments = [n for n in fn.body if isinstance(n, ast.Assign)
                   and isinstance(n.targets[0], ast.Name) and n.targets[0].id in {'scale', 'T'}]
    times = [.2, .5, .8]
    eps_error = np.array([[2., -1.], [1., 3.], [-2., 4.]])
    terms = np.ones((2, 3, 4)) * np.sum(eps_error ** 2, axis=1)[None, :, None]
    scope = {'np': np, 'ts': times, 'seeds': [0], 'd': {'terms_s0': terms}}
    exec(compile(ast.Module(assignments, type_ignores=[]), 'actual-consumer', 'exec'), scope)
    for j, t in enumerate(times):
        score_error = -eps_error[j] / math.sin(math.pi * t / 2)
        np.testing.assert_allclose(scope['T'][0][:, j], .5 * (score_error @ score_error))


def test_path_animation_preserves_first_and_last_positions_for_all_path_lengths():
    from types import SimpleNamespace
    scope = functions('common.py', {'play_path'})
    scope.update(config=SimpleNamespace(frame_rate=15), linear=lambda x: x,
                 UpdateFromAlphaFunc=lambda dots, fn: SimpleNamespace(dots=dots, fn=fn))
    class PanelSpy:
        def pts(self, points): return points.copy()
    class DotSpy:
        def move_to(self, position): self.position = position.copy()
    class SceneSpy:
        def __init__(self): self.states = []
        def play(self, animation, **kwargs):
            for alpha in [0., .25, .5, .75, 1.]:
                animation.fn(animation.dots, alpha)
                self.states.append(np.array([dot.position for dot in animation.dots]))
    for n in [2, 50, 51, 52]:
        points = np.arange(n * 4, dtype=float).reshape(n, 2, 2)
        original = points.copy(); scene = SceneSpy()
        scope['play_path'](scene, PanelSpy(), [DotSpy(), DotSpy()], points, duration=4.2)
        np.testing.assert_array_equal(scene.states[0], points[0])
        np.testing.assert_array_equal(scene.states[-1], points[-1])
        np.testing.assert_array_equal(points, original)


def test_text_metric_ranges_handle_both_separated_orders_and_overlap():
    s = functions('s18_textlm.py', {'comparison_verdict', 'intervals_overlap'})
    verdict = s['comparison_verdict']
    assert verdict([3, 3.1], [2, 2.1]).startswith("the autoregressive model's exact loss is lower")
    assert verdict([2, 2.1], [3, 3.1]).startswith('the diffusion bound is lower')
    assert 'overlap' in verdict([2, 3], [2.5, 3.5])
    # The old 3*max(SE) predicate falsely treated these disjoint intervals as overlapping.
    assert not s['intervals_overlap']([0, 2.5], [1, 1])
    assert s['intervals_overlap']([0, 2], [1, 1])


def test_enumerated_discrete_bound_matches_independent_joint_entropy():
    spec = importlib.util.spec_from_file_location('discrete_only', PART / 'discrete.py')
    d = importlib.util.module_from_spec(spec); spec.loader.exec_module(d)
    out = d.compute_discrete()
    entropy = -(d.PI * np.log2(d.PI)).sum()
    marginal = d.PI.copy()
    for _ in range(d.L - 1):
        entropy += marginal @ (-(d.P * np.log2(d.P)).sum(axis=1))
        marginal = marginal @ d.P
    assert abs(out['exact_cont'] - entropy / d.L) < 1e-12
    for kind in out['kinds']:
        assert abs(out[f'{kind}_cont'] - out[f'{kind}_anyorder']) < 1e-12


def test_all_samplers_begin_in_the_same_physical_edm_state():
    # The denoiser API always receives x_EDM, even when a solver stores VP coordinates.
    scope = functions('exact.py', {'rng', 'sigmas', 'solve'})
    z = np.array([[.2, -.4], [.8, 1.2]])
    for kind in ['euler_vp', 'ddim', 'heun', 'dpm2', 'dpmpp2m', 'ddpm']:
        observed = []
        def denoiser(x, sigma):
            observed.append((x.copy(), sigma))
            return np.zeros_like(x)
        scope['solve'](denoiser, z, kind, 1)
        np.testing.assert_allclose(observed[0][0], 80 * z, rtol=0, atol=1e-10)
        np.testing.assert_allclose(observed[0][1], 80., rtol=0, atol=1e-10)
