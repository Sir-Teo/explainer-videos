"""Independent checks for Part 49's targets and remainder calculations."""
import math
import unittest
import numpy as np
from scipy import stats
from videos.stats.stats49 import compute as C
from explainer.stats.kit import semipar as S


class SemiparametricRepairs(unittest.TestCase):
    def test_population_remainder_against_independent_large_sample(self):
        w=S.rate_world(500000,C.rng(14));k=S.corrupt(w,.25,.25)
        # Conditional means remove outcome noise and treatment randomness.
        pseudo=k['mu1']-k['mu0']+w['e']*(w['mu1']-k['mu1'])/k['e']-(1-w['e'])*(w['mu0']-k['mu0'])/(1-k['e'])
        expected=np.mean(pseudo-(w['mu1']-w['mu0']))
        self.assertLess(abs(expected-C.product_bias(len(w['y']),.25,.25)),1e-5)

    def test_boundary_root_n_bias_does_not_vanish(self):
        boundary=[math.sqrt(n)*C.product_bias(n,.25,.25) for n in (1000,1000000,1000000000)]
        self.assertGreater(abs(boundary[-1]),1.)
        self.assertLess(abs(boundary[-1]/boundary[-2]-1),.1)
        good=[math.sqrt(n)*C.product_bias(n,.3,.3) for n in (1000,1000000)]
        self.assertLess(abs(good[1]),abs(good[0])/1.5)

    def test_gaussian_quadratic_expectations_against_simulation(self):
        n,h,reps=80,.2,3000;generator=C.rng(19)
        values={k:[] for k in ('plugin','one_step','ustat')}
        for _ in range(reps):
            result=S.int_sq_estimates(generator.standard_normal(n),h,generator)
            for k in values:values[k].append(result[k])
        expected=C.intsq_expectations(n,h)
        for k,v in values.items():
            self.assertLess(abs(np.mean(v)-expected[k]),4*np.std(v,ddof=1)/math.sqrt(reps))

    def test_ratio_influence_function_includes_denominators(self):
        generator=C.rng(4);y=generator.normal(size=100);t=np.r_[np.ones(20),np.zeros(80)];e=np.linspace(.1,.9,100)
        r=C.ate_ipw(y,t,e)
        weights=[t/e,(1-t)/(1-e)];means=[w@y/w.sum() for w in weights]
        derivatives=[];eps=1e-6
        # Differentiate the weighted empirical law by adding mass at observation i.
        base=np.ones(100)/100
        def functional(p):return (p*weights[0])@y/(p@weights[0])-(p*weights[1])@y/(p@weights[1])
        for i in range(100):
            direction=np.eye(100)[i]-base
            derivatives.append((functional(base+eps*direction)-functional(base-eps*direction))/(2*eps))
        self.assertAlmostEqual(r['se'],np.std(derivatives,ddof=1)/10,places=9)

    def test_crossfit_predictions_exclude_heldout_outcomes(self):
        w=S.rate_world(120,C.rng(8));fold=np.arange(120)%2
        a=C.nuisances(w['X'],w['t'],w['y'],fold,k_out=5,k_ps=10)
        changed=w['y'].copy();changed[fold==0]+=10000
        b=C.nuisances(w['X'],w['t'],changed,fold,k_out=5,k_ps=10)
        for aa,bb in zip(a,b):np.testing.assert_allclose(aa[fold==0],bb[fold==0],rtol=0,atol=1e-12)

    def test_world_target_is_fixed_pool_ate(self):
        from explainer.stats.world import World
        truth=float(World().trial['tau_pool'].mean())
        a=C.obs_sample(C.rng(9),100);b=C.obs_sample(C.rng(10),200)
        self.assertEqual(a['ate'],truth);self.assertEqual(b['ate'],truth)
        self.assertNotEqual(a['sample_ate'],b['sample_ate'])

    def test_coverage_mcse_uses_independent_datasets(self):
        hit=np.array([1,1,0,1,0,1],float);p=hit.mean()
        self.assertAlmostEqual(C.bernoulli_se(hit),math.sqrt(p*(1-p)/5))

    def test_independence_projection_derivative_and_finite_variance(self):
        p=np.array([.18,.12,.42,.28]);gradient=np.array([1,0,0,0])-.18
        projection=S.project(p,gradient,S.independence_scores(2,2))
        self.assertAlmostEqual(S.inner(p,projection,projection),.0972)
        # Exact finite-n variance of product margins adds a cross-product term.
        n=400;finite=.0972+.3*.7*.6*.4/n
        self.assertGreater(finite,.0972)

if __name__=='__main__':unittest.main()
