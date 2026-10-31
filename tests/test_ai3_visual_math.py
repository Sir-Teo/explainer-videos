"""Tiny independent scene/math regressions without importing Part 3 loaders.

Only selected literal tables, NumPy assignments and helper function ASTs run.
No scene is constructed, model imported, cache loaded or measured data computed.
"""
import ast
import math
from pathlib import Path
from types import SimpleNamespace
import unittest

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'videos/ai/ai3'


def method(filename, name):
    tree = ast.parse((PART / filename).read_text())
    return next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == name)


def assignment(body, name):
    return next(n for n in body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))


def execute(nodes, namespace):
    module = ast.Module(body=nodes, type_ignores=[])
    assert not any(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(module))
    exec(compile(module, '<isolated-part3-math>', 'exec'), namespace)
    return namespace


class AttentionShapeTests(unittest.TestCase):
    def test_actual_four_contractions_match_separate_tensor_operations(self):
        rows = ast.literal_eval(assignment(method('s03_einsum.py', 'attention').body, 'lines').value)
        expressions = [row[0] for row in rows]
        # Distinct axis sizes catch accidentally retained/replaced indices.
        b, t, h, e, d = 2, 3, 2, 4, 5
        x = np.arange(b*t*d, dtype=float).reshape(b,t,d)/10
        w = np.arange(d*h*e, dtype=float).reshape(d,h,e)/17
        q = np.einsum(expressions[0], x, w)
        expected_q = np.tensordot(x, w, axes=([2],[0])).transpose(0,2,1,3)
        np.testing.assert_allclose(q, expected_q)
        self.assertEqual(q.shape, (b,h,t,e))
        # Keys have a different sequence length from queries.
        keys = np.arange(b*h*6*e, dtype=float).reshape(b,h,6,e)/29
        scores = np.einsum(expressions[1], q, keys)
        np.testing.assert_allclose(scores, q @ keys.swapaxes(-1,-2))
        self.assertEqual(scores.shape, (b,h,t,6))
        weights = np.exp(scores - scores.max(-1,keepdims=True))
        weights /= weights.sum(-1,keepdims=True)
        values = keys/3
        context = np.einsum(expressions[2], weights, values)
        np.testing.assert_allclose(context, weights @ values)
        out_w = np.arange(h*e*d, dtype=float).reshape(h,e,d)/23
        output = np.einsum(expressions[3], context, out_w)
        flattened = context.transpose(0,2,1,3).reshape(b,t,h*e) @ out_w.reshape(h*e,d)
        np.testing.assert_allclose(output, flattened)
        self.assertEqual(output.shape, (b,t,d))


def parabola_fixture(theta):
    body = method('s02_vectors.py', 'cauchy_schwarz').body
    axes = next(n for n in ast.walk(assignment(body, 'ax'))
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'Axes')
    literals = {}
    for node in body:
        if not isinstance(node, ast.Assign):
            continue
        try:
            ast.literal_eval(node.value)
        except (ValueError, TypeError):
            continue
        execute([node], literals)
    ranges = {k.arg: eval(compile(ast.Expression(k.value), '<actual-axis-range>', 'eval'), {}, literals)
              for k in axes.keywords if k.arg in ('x_range','y_range')}
    ns = {**literals, 'np':np,'math':math,'th':SimpleNamespace(get_value=lambda:theta),
          'C':SimpleNamespace(BITS='test'),
          'ax':SimpleNamespace(plot=lambda f, **kwargs:(f,kwargs['x_range']))}
    helpers = [n for n in body if isinstance(n, ast.FunctionDef) and n.name in ('b_', 'parabola')]
    execute([assignment(body, 'a_'), *helpers],ns)
    f, domain = ns['parabola']()
    return ns['a_'],ns['b_'](),f,domain,ranges


class CauchySchwarzGeometryTests(unittest.TestCase):
    def test_both_parallel_equality_vertices_visible_in_actual_curve_domain(self):
        for theta in (0, math.pi):
            with self.subTest(theta=theta):
                a,b,f,domain,ranges=parabola_fixture(theta)
                vertex=float(a@b/(b@b))
                self.assertLessEqual(ranges['x_range'][0],vertex)
                self.assertGreaterEqual(ranges['x_range'][1],vertex)
                self.assertLessEqual(domain[0],vertex)
                self.assertGreaterEqual(domain[1],vertex)
                self.assertAlmostEqual(f(vertex),0,places=12)

    def test_swept_curve_stays_in_axes_and_is_actual_squared_length(self):
        for theta in np.linspace(0,math.pi,25):
            a,b,f,domain,ranges=parabola_fixture(float(theta))
            self.assertLess(domain[0],domain[1])
            self.assertGreaterEqual(domain[0],ranges['x_range'][0])
            self.assertLessEqual(domain[1],ranges['x_range'][1])
            for t in np.linspace(domain[0],domain[1],41):
                y=f(t)
                self.assertAlmostEqual(y,float(np.sum((a-t*b)**2)),places=11)
                self.assertGreaterEqual(y,ranges['y_range'][0]-1e-12)
                self.assertLessEqual(y,ranges['y_range'][1]+1e-12)


class MuonReplayTests(unittest.TestCase):
    def test_actual_initial_curve_uses_recorded_step_zero_not_sigma1_reference(self):
        body=method('s10_norms.py','muon').body
        spectrum=np.array([4.,3.])
        ns0=spectrum/(np.linalg.norm(spectrum)+1e-7)
        data={'ns_sv':[ns0.tolist(),[1.02,.98]],'g_sv':(spectrum/spectrum[0]).tolist()}
        namespace={'np':np,'gl':data,'ax':None,'xs':np.array([.5,1.5]),
                   'GREY_B':'grey','C':SimpleNamespace(MUON='muon'),
                   'curve':lambda ax,xs,ys,*args,**kwargs:np.asarray(ys)}
        execute([assignment(body,'ns'),assignment(body,'g0'),assignment(body,'first')],namespace)
        np.testing.assert_allclose(namespace['first'],ns0,rtol=0,atol=1e-15)
        self.assertFalse(np.allclose(namespace['first'],data['g_sv']))

    def test_actual_axis_top_contains_every_recorded_iterate(self):
        body=method('s10_norms.py','muon').body
        ns=[np.array([.8,.6]),np.array([1.49,.97]),np.array([.7,1.8])]
        namespace=execute([assignment(body,'y_top')],{'ns':ns})
        self.assertGreater(namespace['y_top'],max(float(x.max()) for x in ns))


class MeasuredVerdictTests(unittest.TestCase):
    def test_power_rate_gap_uses_both_rates_without_claiming_decimal_equality(self):
        body=method('s07_power.py','measured').body
        nodes=[assignment(body,'rate_gap'),assignment(body,'verdict')]
        ns=execute(nodes,{'dg':{'rate_measured':.244,'ratio':.253},
                          'dl':{'rate_measured':.5,'ratio':.5}})
        self.assertAlmostEqual(ns['rate_gap'],.009)
        self.assertIn('within 0.01',ns['verdict'])
        self.assertNotIn('decimal',ns['verdict'])
        ns=execute(nodes,{'dg':{'rate_measured':.25,'ratio':.25},
                          'dl':{'rate_measured':.1,'ratio':.4}})
        self.assertAlmostEqual(ns['rate_gap'],.3)
        self.assertIn('0.300',ns['verdict'])
        self.assertNotIn('within 0.01',ns['verdict'])

    def test_single_random_reference_verdict_includes_equal_and_above_cases(self):
        body=method('s10_norms.py','gpt2').body
        branch=next(n for n in body if isinstance(n,ast.If) and any(
            isinstance(child,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='verdict' for t in child.targets)
            for child in ast.walk(n)))
        for high,phrase in [(100,'below half'),(200,'below this'),(300,'reaches or exceeds'),(400,'reaches or exceeds')]:
            with self.subTest(high=high):
                text=execute([branch],{'hi':high,'rnd':{'stable':300}})['verdict']
                self.assertIn(phrase,text)
                self.assertIn('MLP-shaped random reference',text)
                self.assertNotIn('same shape',text)

    def test_netflix_rebound_and_comparative_endpoint_are_independent(self):
        helper=execute([method('s18_netflix.py','penalty_verdict')],{'np':np})['penalty_verdict']
        reference=np.array([[0,0,.95],[1,0,.90]])
        for series,comparison,rebound in [([1.,.85,.80],'lower than',False),
                                          ([.8,.70,.80],'lower than',True),
                                          ([.8,.90,1.0],'higher than',True),
                                          ([1.,.95,.905],'within 0.01 stars of',False)]:
            with self.subTest(series=series):
                other=np.array([[i,0,y] for i,y in enumerate(series)])
                actual=helper(reference,other)
                self.assertIn(comparison,actual)
                self.assertEqual('rises from its minimum' in actual,rebound)
                self.assertIn('same bias penalty',actual)


class GeneralizedShiftedPMITests(unittest.TestCase):
    def target(self, pair, negatives, k=5):
        centre,context=np.indices(pair.shape)
        centre=np.repeat(centre.ravel(),pair.ravel())
        context=np.repeat(context.ravel(),pair.ravel())
        ns={'np':np,'math':math,'centre':centre,'context':context,
            'neg_np':np.asarray(negatives),'V':len(pair),'K':k}
        names={'mask','pair','nw','pn','tot','seen','target'}
        nodes=[]
        for n in method('compute.py','sgns_exact').body:
            if isinstance(n, ast.For):
                break
            if isinstance(n, ast.Assign):
                target=n.targets[0]
                name=target.id if isinstance(target,ast.Name) else target.value.id if isinstance(target,ast.Subscript) and isinstance(target.value,ast.Name) else None
                if name in names:
                    nodes.append(n)
        return execute(nodes,ns)

    def test_actual_target_stationary_with_smoothed_negatives(self):
        pair=np.array([[60,10],[20,10]],dtype=int)
        context_probability=pair.sum(0)/pair.sum()
        negative=context_probability**.75
        negative/=negative.sum()
        ns=self.target(pair,negative)
        x=ns['target']; sigmoid=1/(1+np.exp(-x))
        # Derivative of independently specified expected SGNS objective.
        positive=pair/pair.sum()
        negative_mass=5*np.outer(pair.sum(1),negative)/pair.sum()
        gradient=positive*(1-sigmoid)-negative_mass*sigmoid
        np.testing.assert_allclose(gradient,0,atol=1e-15)
        ordinary=np.log(pair*pair.sum()/(pair.sum(1)[:,None]*pair.sum(0)[None,:]))-math.log(5)
        self.assertGreater(np.max(np.abs(x-ordinary)),.05)

    def test_ordinary_PMI_is_recovered_only_with_empirical_context_negatives(self):
        pair=np.array([[60,10],[20,10]],dtype=int)
        p_context=pair.sum(0)/pair.sum()
        target=self.target(pair,p_context)['target']
        pmi=np.log(pair*pair.sum()/(pair.sum(1)[:,None]*pair.sum(0)[None,:]))
        np.testing.assert_allclose(target,pmi-math.log(5),atol=1e-15)


def jl_bound_helper():
    tree=ast.parse((PART/'compute.py').read_text())
    delta=ast.literal_eval(assignment(tree.body,'JL_DELTA').value)
    return execute([method('compute.py','jl_bound_eps')],{'np':np,'math':math,'JL_DELTA':delta})['jl_bound_eps']


class JLConfidenceTests(unittest.TestCase):
    def test_actual_inverse_satisfies_explicit_union_failure_probability(self):
        bound=jl_bound_helper()
        for n,k,delta in [(1000,768,.05),(1000,400,.01),(2,100,.001),(1000000,1000,.05)]:
            with self.subTest(n=n,k=k,delta=delta):
                epsilon=bound(k,n,delta)
                self.assertTrue(0<epsilon<1)
                log_failure=math.log(n)+math.log(n-1)-k*(epsilon**2/2-epsilon**3/3)/2
                self.assertLessEqual(log_failure,math.log(delta)+1e-12)
                self.assertAlmostEqual(log_failure,math.log(delta),places=10)

    def test_no_bound_below_one_is_not_presented_as_a_finite_guarantee(self):
        bound=jl_bound_helper()
        n,delta=1000,.05
        limiting_k=12*math.log(n*(n-1)/delta)
        self.assertTrue(math.isnan(bound(math.floor(limiting_k),n,delta)))
        self.assertTrue(0<bound(math.floor(limiting_k)+1,n,delta)<1)

    def test_stricter_confidence_and_smaller_dimension_require_larger_distortion(self):
        bound=jl_bound_helper()
        self.assertGreater(bound(768,1000,.01),bound(768,1000,.05))
        self.assertGreater(bound(400,1000,.05),bound(768,1000,.05))

    def test_invalid_guarantee_parameters_are_rejected(self):
        bound=jl_bound_helper()
        for k,n,delta in [(0,1000,.05),(100.5,1000,.05),(100,1,.05),(100,1000,0),
                          (100,1000,1),(100,1000,float('nan')),(True,1000,.05)]:
            with self.subTest(k=k,n=n,delta=delta):
                with self.assertRaises(ValueError):
                    bound(k,n,delta)


class JLPlotBoundaryTests(unittest.TestCase):
    def helper(self):
        return execute([method('s16_jl.py','worst_plot_data')],{'math':math,'np':np})['worst_plot_data']

    def test_finite_bounds_and_observations_must_be_inside_both_axes(self):
        fine=[dict(k=20,bound_eps=.6,worst=[.3,.7]),
              dict(k=100,bound_eps=float('nan'),worst=[.2,.9]),
              dict(k=200,bound_eps=1.1,worst=[.8,2]),
              dict(k=400,bound_eps=.9,worst=[.4,float('nan')]),
              dict(k=768,bound_eps=.7,worst=[.2,.4]),
              dict(k=2000,bound_eps=.5,worst=[.1,.2])]
        bounds,measured,omitted=self.helper()(fine)
        self.assertEqual([x[2] for x in bounds],[400,768])
        np.testing.assert_allclose([x[0] for x in measured],np.log10([100,768]))
        np.testing.assert_allclose(measured[0][1:],[.2,.9,.55])
        self.assertEqual(omitted,4)
        self.assertTrue(all(1.9<=x<=3 and 0<y<1 for x,y,k in bounds))
        self.assertTrue(all(1.9<=x<=3 and 0<=lo<=mean<=hi<=1 for x,lo,hi,mean in measured))

    def test_measured_axis_boundaries_are_retained_without_inventing_guarantees(self):
        bounds,measured,omitted=self.helper()([
            dict(k=100,bound_eps=float('nan'),worst=[0,1]),
            dict(k=1000,bound_eps=1.,worst=[0,.5])])
        self.assertEqual(bounds,[])
        self.assertEqual(len(measured),2)
        self.assertEqual(omitted,0)

    def test_actual_bound_drawing_handles_zero_one_and_multiple_certified_points(self):
        node=assignment(method('s16_jl.py','worst').body,'c_b')
        ns={'ax':SimpleNamespace(c2p=lambda *point:point),'BOUND':'bound',
            'curve':lambda ax,x,y,*args:('curve',x,y),
            'Dot':lambda point,**kwargs:('dot',point),
            'VGroup':lambda:('empty',)}
        for good,kind in [([], 'empty'), ([(2,.9,100)], 'dot'),
                          ([(2,.9,100),(2.5,.6,316)], 'curve')]:
            with self.subTest(point_count=len(good)):
                actual=execute([node],dict(ns,good=good))['c_b']
                self.assertEqual(actual[0],kind)
                if kind=='dot':
                    self.assertEqual(actual[1],(2,.9))


if __name__ == '__main__':
    unittest.main(verbosity=2)
