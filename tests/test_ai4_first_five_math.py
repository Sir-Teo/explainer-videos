"""First-five-scene math/geometry fixtures; never import scenes or data loaders.

Only chosen pure helper/function ASTs and numeric assignments run. The fixtures
use tiny synthetic arrays, not Part4 production computations or cached results.
"""
import ast
import math
from pathlib import Path
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'videos/ai/ai4'


def function(path, name):
    return next(n for n in ast.walk(ast.parse(path.read_text()))
                if isinstance(n, ast.FunctionDef) and n.name == name)


def helpers(filename, *names, extra=None):
    namespace = {'np': np, 'math': math, **(extra or {})}
    nodes = [function(PART / filename, name) for name in names]
    module = ast.Module(body=nodes, type_ignores=[])
    assert not any(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(module))
    exec(compile(module, '<isolated-ai4-first-five>', 'exec'), namespace)
    return namespace


def assignment(method, name):
    return next(n for n in method.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))


class LensClipTests(unittest.TestCase):
    def setUp(self):
        self.f = helpers('s04_jacobian.py', 'clip_segment_to_disk')['clip_segment_to_disk']

    def test_both_outside_endpoints_retain_the_crossing_segment(self):
        a, b = self.f([-3, 0, 0], [4, 0, 0], [0, 0, 0], 2)
        np.testing.assert_allclose(a, [-2, 0, 0])
        np.testing.assert_allclose(b, [2, 0, 0])

    def test_inside_endpoints_are_unchanged(self):
        a, b = np.array([.2, .3, 0]), np.array([.7, -.2, 0])
        got = self.f(a, b, [0, 0, 0], 1)
        np.testing.assert_array_equal(got[0], a)
        np.testing.assert_array_equal(got[1], b)

    def test_nonintersecting_segment_omitted(self):
        self.assertIsNone(self.f([-2, 3, 0], [2, 3, 0], [0, 0, 0], 1))

    def test_tangent_and_zero_length_cases(self):
        a, b = self.f([-2, 1, 0], [2, 1, 0], [0, 0, 0], 1)
        np.testing.assert_allclose(a, [0, 1, 0]);np.testing.assert_allclose(b, a)
        self.assertIsNone(self.f([2, 2, 0], [2, 2, 0], [0, 0, 0], 1))
        np.testing.assert_array_equal(self.f([0, 0, 0], [0, 0, 0], [0, 0, 0], 1)[0], [0, 0, 0])

    def test_actual_warp_and_linear_grid_segments_stay_inside_lens_through_zoom(self):
        ns = helpers('s04_jacobian.py', 'warp', 'jac')
        p = np.array([1.2, .6]);j = ns['jac'](*p);center = np.array([4., -1., 0]);R = 2.2
        old_overflow = False
        for radius in np.linspace(1.6, .08, 17):
            scale = R * .62 / radius
            maps = [lambda q: center + scale * (ns['warp'](p + q) - ns['warp'](p)),
                    lambda q: center + scale * np.r_[j @ q, 0]]
            for mapping in maps:
                for t in np.linspace(-radius, radius, 7):
                    for horizontal in [True, False]:
                        points = [mapping(np.array([s, t] if horizontal else [t, s]))
                                  for s in np.linspace(-radius, radius, 30)]
                        old_overflow |= any(np.linalg.norm(q-center) > R for q in points)
                        for a, b in zip(points, points[1:]):
                            clipped = self.f(a, b, center, R*.98)
                            if clipped is None:continue
                            for u in np.linspace(0, 1, 5):
                                q = (1-u)*clipped[0] + u*clipped[1]
                                self.assertLessEqual(np.linalg.norm(q-center), R*.98 + 1e-12)
                            delta = b-a
                            for q in clipped:
                                self.assertLess(np.linalg.norm(np.cross(q-a, delta)), 1e-12)
        self.assertTrue(old_overflow, 'fixture must exercise original lens overflow')


class JacobianMathTests(unittest.TestCase):
    def test_actual_map_jacobian_matches_independent_central_differences(self):
        n = helpers('s04_jacobian.py', 'warp', 'jac');p=np.array([1.2,.6]);h=1e-6
        fd=np.column_stack([(n['warp'](p+h*e)[:2]-n['warp'](p-h*e)[:2])/(2*h) for e in np.eye(2)])
        np.testing.assert_allclose(n['jac'](*p),fd,atol=2e-10)

    def test_norm_product_is_strict_bound_and_maximum_is_directional(self):
        a=np.diag([1.,0]);b=np.diag([0.,1])
        self.assertEqual(np.linalg.norm(a@b,2),0)
        self.assertEqual(np.linalg.norm(a,2)*np.linalg.norm(b,2),1)
        j=np.diag([4.,.25]);self.assertEqual(np.linalg.norm(j,2),4)
        self.assertEqual(np.linalg.norm(j @ np.array([0.,1.])),.25)
        self.assertEqual(np.linalg.norm(j.T,2),np.linalg.norm(j,2))

    def test_dynamic_range_includes_outliers_and_preserves_original_values(self):
        f=helpers('s04_jacobian.py','depth_plot_range')['depth_plot_range']
        d={'gains':[.5,1.]}
        for k in range(2):
            d[f'mean{k}']=np.array([-1.,float(k)])
            d[f'lo{k}']=np.array([-31.1,-2.]);d[f'hi{k}']=np.array([.5,13.2])
        original={k:v.copy() for k,v in d.items() if isinstance(v,np.ndarray)}
        low,high=f(d);self.assertLess(low,-31.1);self.assertGreater(high,13.2)
        for k,v in original.items():np.testing.assert_array_equal(d[k],v)

    def test_zero_scale_in_range_and_nonfinite_data_is_explicit(self):
        f=helpers('s04_jacobian.py','depth_plot_range')['depth_plot_range']
        d={'gains':[1.], 'mean0':[-2.], 'lo0':[-3.], 'hi0':[-1.]}
        low,high=f(d);self.assertLess(low,0);self.assertGreater(high,0)
        d['lo0']=[float('-inf')]
        with self.assertRaisesRegex(ValueError,'finite recorded'):f(d)


class GradientAndUnitsTests(unittest.TestCase):
    def test_both_actual_illustrated_and_measured_points_share_producer_anchor(self):
        tree=ast.parse((PART/'compute.py').read_text())
        p=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign)
                               and any(isinstance(t,ast.Name) and t.id=='BOWL_P0' for t in n.targets)))
        for name in ['surface','contours']:
            node=assignment(function(PART/'s03_gradient.py',name),'p0')
            actual=eval(compile(ast.Expression(node.value),'<actual-scene-anchor>','eval'),{'np':np,'BOWL_P0':p})
            np.testing.assert_array_equal(actual,p)

    def test_surprise_derivative_keeps_base_two_factor(self):
        ns=helpers('s02_derivative.py','s','ds');p=.25;h=1e-6
        self.assertAlmostEqual(ns['ds'](p),(ns['s'](p+h)-ns['s'](p-h))/(2*h),places=8)
        self.assertAlmostEqual(ns['ds'](p),-4/math.log(2))

    def test_finite_chain_intervals_differ_from_local_factors_and_converge(self):
        def ratios(h):
            a=1.;b=(1+h)**2
            return (b-a)/h,(math.exp(b)-math.exp(a))/(b-a)
        finite=np.array(ratios(.12));small=np.array(ratios(1e-5));target=np.array([2.,math.e])
        self.assertGreater(abs(finite[0]-2),.1)
        self.assertTrue(np.all(abs(small-target)<abs(finite-target)/1000))

    def test_cross_entropy_bits_gradient_is_nats_gradient_over_ln_two(self):
        z=np.array([.3,-.2,1.]);target=np.array([0.,1.,0.]);p=np.exp(z-z.max());p/=p.sum()
        def loss(x):return -(target * (x-np.log(np.exp(x).sum()))).sum()/math.log(2)
        h=1e-6;fd=np.array([(loss(z+h*e)-loss(z-h*e))/(2*h) for e in np.eye(3)])
        np.testing.assert_allclose(fd,(p-target)/math.log(2),atol=3e-10)


class LayerAndProvenanceTests(unittest.TestCase):
    def test_display_keeps_signed_roundoff_and_exact_zero(self):
        sci=function(ROOT/'explainer/analysis/__init__.py','sci');ns={'math':math}
        exec(compile(ast.Module(body=[sci],type_ignores=[]),'<actual-sci>','exec'),ns)
        f=helpers('s05_layers.py','gap_tex','eigenvalue_tex',extra={'sci':ns['sci']})['eigenvalue_tex']
        self.assertTrue(f(-2.3e-17).startswith('-'))
        self.assertNotEqual(f(2.3e-17),'0');self.assertEqual(f(0.),'0')
        self.assertEqual(f(-.125), '-0.125')

    def test_layernorm_epsilon_leaves_radial_sensitivity_not_second_exact_null(self):
        x=np.array([1.,2.,4.]);eps=1e-5;sigma=math.sqrt(x.var()+eps);y=(x-x.mean())/sigma;n=len(x)
        j=(np.eye(n)-np.ones((n,n))/n-np.outer(y,y)/n)/sigma
        np.testing.assert_allclose(j@np.ones(n),0,atol=1e-15)
        np.testing.assert_allclose(j@y,(eps/sigma**3)*y,atol=1e-15)
        self.assertGreater(eps/sigma**3,0)

    def test_parameter_models_have_independent_provenance_labels(self):
        f=helpers('s01_hook.py','parameter_count_source')['parameter_count_source']
        d={'provenance':{'gpt2':{'source':'pinned-safetensors-headers'},'qwen3_4b':{'source':'historical-fallback'}}}
        self.assertIn('pinned',f(d,'gpt2'));self.assertIn('historical',f(d,'qwen3_4b'))
        self.assertIn('not a fresh',f(d,'qwen3_4b'))

    def test_unknown_and_legacy_provenance_never_claim_fresh_measurement(self):
        f=helpers('s01_hook.py','parameter_count_source')['parameter_count_source']
        for d in [{},{'provenance':{'gpt2':{'source':'unknown'}}}]:
            self.assertIn('unverified',f(d,'gpt2'));self.assertNotIn('counted from',f(d,'gpt2'))


if __name__=='__main__':unittest.main()
