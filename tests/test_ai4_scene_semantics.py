"""Bounded Part4 consumer regressions: execute actual helper ASTs, never scene loaders."""
import ast
import math
from pathlib import Path
import unittest
import numpy as np

PART = Path(__file__).resolve().parents[1] / 'videos/ai/ai4'


def helpers(filename):
    tree = ast.parse((PART / filename).read_text())
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    namespace = {'np': np, 'math': math}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(PART / filename), 'exec'), namespace)
    return namespace


class VCurveSceneTests(unittest.TestCase):
    def setUp(self):
        self.f = helpers('s11_vcurve.py')

    def test_actual_aggregate_optimum_lies_on_median_counterexample(self):
        errors = np.array([[0.,100.,2.],[2.,0.,100.],[1.,100.,0.]])
        median = np.median(errors, axis=0)
        hs = np.array([.01,.1,1.])
        actual = self.f['aggregate_minimum'](hs, median)
        self.assertEqual(actual, {'index':0,'h':.01,'error':1.})
        self.assertNotEqual(actual['h'],np.median(hs[np.argmin(errors,axis=1)]))
        self.assertEqual(actual['error'],median[actual['index']])
        tree=ast.parse((PART/'s11_vcurve.py').read_text())
        dots=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='Dot']
        self.assertTrue(any('yy[i]' in ast.unparse(n) and 'hs[i]' in ast.unparse(n) for n in dots))

    def test_zero_optimum_and_all_invalid_are_not_log_failures(self):
        self.assertEqual(self.f['aggregate_minimum']([1,2],[1,0])['error'],0)
        self.assertIsNone(self.f['aggregate_minimum']([1,2],[np.nan,-1]))
        logs,count=self.f['error_window']([0,1e-20,1e-8,2,np.nan,-1],-14,0)
        np.testing.assert_allclose(logs[:4],[-14,-14,-8,0])
        self.assertTrue(np.isnan(logs[4:]).all())
        self.assertEqual(count,{'floor':2,'ceiling':1,'omitted':2})

    def test_prediction_far_outside_model_does_not_claim_agreement(self):
        self.assertIn('factor of 1000.0',self.f['prediction_verdict']([1000,1]))
        self.assertNotIn('order of magnitude',self.f['prediction_verdict']([1000,1]))
        self.assertIn('within a factor of three',self.f['prediction_verdict']([2,.5]))
        self.assertIn('unavailable',self.f['prediction_verdict']([np.nan,1]))


class CheckpointSceneTests(unittest.TestCase):
    def test_nonmatching_reference_and_candidate_ratios_are_reported(self):
        f=helpers('s12_memory.py')['checkpoint_verdict']
        interval,scaling=f(256,2,3,[16,64],[1,80])
        self.assertIn('outside',interval)
        self.assertIn('0.25 to 10.00',scaling)
        self.assertNotIn('close',scaling)
        self.assertIn('lies in',f(256,15,17,[16],[4])[0])
        self.assertIn('No finite',f(256,15,17,[],[])[1])

    def test_storage_work_and_gradient_claims_are_separated(self):
        source=(PART/'s12_memory.py').read_text()
        self.assertIn('recomputation overhead',source)
        self.assertIn('total work',source)
        self.assertNotIn('to the last bit',source)
        self.assertIn('not process or allocator memory',source)
        self.assertNotIn('identical every way',source)


class NewtonSceneTests(unittest.TestCase):
    def setUp(self): self.f=helpers('s13_newton.py')

    def result(self,status='converged',criterion='gradient norm < threshold'):
        return dict(status=status,first_hit_step=4 if status=='converged' else None,
                    cap=12,iterations=12,threshold=1e-10,criterion=criterion)

    def test_real_status_branches_distinguish_criterion_and_censoring(self):
        f=self.f['convergence_summary']
        self.assertIn('gradient norm',f(self.result(),'Newton'))
        self.assertIn('objective gap',f(self.result(),'Gradient descent'))
        self.assertIn('censored',f(self.result('capped'),'Newton'))
        self.assertNotIn('first meets',f(self.result('nonfinite'),'Newton'))
        self.assertIn('unavailable',f(self.result('capped','objective-gap comparison unavailable: numerical reference not stationary'),'Gradient descent'))

    def test_correct_digits_do_not_claim_improvement_when_errors_increase(self):
        self.assertIn('do not increase',self.f['digit_summary']([1e-5,1e-3,1e-1]))
        self.assertIn('counts increase',self.f['digit_summary']([1e-1,1e-3,1e-6]))
        self.assertIn('unavailable',self.f['digit_summary']([0,np.nan]))
        self.assertNotIn('quadratic',self.f['digit_summary']([1e-1,1e-3,1e-6]))

    def test_conservative_one_over_L_is_not_the_largest_descent_step(self):
        L=4.;x=2.;eta=1.5/L
        f=lambda x:L*x*x/2
        self.assertAlmostEqual(f(x-eta*L*x)/f(x),.25)
        source=(PART/'s13_newton.py').read_text()
        self.assertNotIn('largest step that is always safe',source)
        self.assertIn('Hessian is positive definite',source)

    def test_trajectory_ranges_include_all_finite_recorded_states(self):
        xr,yr=self.f['trajectory_bounds']([[0,0],[3,-4],[np.nan,8]],[[2,5]],[[-2,1]])
        self.assertLess(xr[0],-2);self.assertGreater(xr[1],3)
        self.assertLess(yr[0],-4);self.assertGreater(yr[1],5)
        self.assertEqual(self.f['trajectory_bounds']([[np.nan,np.inf]]),((-1.,1.),(-1.,1.)))

    def test_actual_error_curve_uses_final_inclusive_recorded_steps(self):
        tree=ast.parse((PART/'s13_newton.py').read_text())
        race=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='race')
        assignment=next(n for n in race.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='t_gd' for t in n.targets))
        ns={'np':np,'d':{'gd_err_steps':[0,50,75]}}
        exec(compile(ast.Module(body=[assignment],type_ignores=[]),'<actual-newton-error-steps>','exec'),ns)
        np.testing.assert_array_equal(ns['t_gd'],[1,51,76])

    def test_objective_window_preserves_invalid_gaps_and_discloses_boundaries(self):
        logs,floor,ceiling,invalid=self.f['objective_window']([0,1e-15,.01,3,-1,np.nan])
        np.testing.assert_allclose(logs[:4],[-12,-12,-2,0])
        self.assertTrue(np.isnan(logs[4:]).all())
        self.assertEqual((floor,ceiling,invalid),(2,1,2))


class HVPSceneTests(unittest.TestCase):
    def setUp(self):
        self.f=helpers('s14_hvp.py')
        self.thresholds=dict(negative_relative=.01,flat_relative=.01,outlier_relative=.1,scale='spectral_radius')

    def test_signed_dominant_target_uses_absolute_denominator(self):
        p=self.f['power_comparison']([-1.,-1.9,-2.],[-2.,1.])
        self.assertTrue(p['available']);self.assertEqual(p['target'],-2.)
        np.testing.assert_allclose(p['relative'],[.5,.05,0],atol=1e-15)
        self.assertEqual(self.f['power_comparison']([2.],[2.,2.,1.])['target'],2.)

    def test_tied_signs_zero_and_empty_cannot_assert_power_convergence(self):
        for ev in ([-2.,2.],[0.,0.],[np.nan]):
            p=self.f['power_comparison']([0.,1.],ev)
            self.assertFalse(p['available']);self.assertTrue(np.isnan(p['relative']).all())
        self.assertFalse(self.f['power_comparison']([np.nan],[-2.,1.])['available'])

    def test_radius_normalization_contains_negative_magnitude_dominance(self):
        s=self.f['spectrum_state']([-3.,1.],self.thresholds)
        np.testing.assert_allclose(s['normalized'],[-1.,1/3])
        self.assertEqual(s['negative'],1);self.assertEqual(s['high_positive'],1)
        self.assertTrue((np.abs(s['normalized'])<=1).all())

    def test_threshold_boundaries_and_zero_spectrum_match_producer_contract(self):
        s=self.f['spectrum_state']([-1.,-.01,0.,.01,.1,1.,np.nan],self.thresholds)
        self.assertEqual(s['negative'],1);self.assertEqual(s['high_positive'],1)
        self.assertEqual(s['flat'],.5);self.assertEqual(s['omitted'],1)
        z=self.f['spectrum_state']([0.,0.],self.thresholds)
        self.assertEqual((z['rho'],z['negative'],z['high_positive'],z['flat']),(0.,0,0,1.))
        self.assertIsNone(self.f['spectrum_state']([np.nan],self.thresholds)['flat'])

    def test_adverse_endpoint_verdicts_remain_honest(self):
        state=self.f['spectrum_state']
        a=state([-1.,1.],self.thresholds);b=state([-2.,-1.,1.],self.thresholds)
        self.assertIn('increases',self.f['curvature_verdict'](a,b))
        self.assertIn('increases',self.f['radius_verdict'](a,b))
        self.assertIn('decreases',self.f['curvature_verdict'](b,a))
        self.assertIn('both endpoints',self.f['radius_verdict'](a,a))
        self.assertIn('both endpoints',self.f['curvature_verdict'](a,a))

    def test_final_checkpoint_precedes_final_bookmark(self):
        tree=ast.parse((PART/'s14_hvp.py').read_text())
        replay=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='replay')
        with_node=next(n for n in replay.body if isinstance(n,ast.With))
        loop=next(n for n in with_node.body if isinstance(n,ast.For))
        self.assertNotIn('wait_until',ast.unparse(loop))
        self.assertEqual(ast.unparse(with_node.body[-1]),"vo.wait_until('c')")

    def test_actual_loss_marker_uses_same_step_plus_one_as_curve(self):
        tree=ast.parse((PART/'s14_hvp.py').read_text())
        replay=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='replay')
        selected=[]
        for n in replay.body:
            if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ('okc','loss_display','lc') for t in ast.walk(n.targets[0])):
                selected.append(n)
        ns={'np':np,'math':math,'cv':np.array([[0,1.],[30,.5]]),'C':type('Colors',(),{'LOSS':'test'}),
            'a1':type('Axes',(),{'c2p':staticmethod(lambda x,y:(x,y))})(),
            'displayed_logs':self.f['displayed_logs'],'curve':lambda ax,x,y,*args:(x,y),
            'keep':[0,30],'d':{'loss0':1.,'loss1':.5}}
        execute=ast.Module(body=selected+[next(n for n in replay.body if isinstance(n,ast.FunctionDef) and n.name=='mpos')],type_ignores=[])
        exec(compile(execute,'<actual-hessian-marker-and-curve>','exec'),ns)
        for i in range(2):
            self.assertAlmostEqual(ns['mpos'](i)[0],ns['lc'][0][i])
            self.assertAlmostEqual(ns['mpos'](i)[1],ns['lc'][1][i])
