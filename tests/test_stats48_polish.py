"""Independent checks of Part 48's local numerical repairs."""
import itertools
import math
import unittest
import numpy as np
from videos.stats.stats48 import compute as C
from explainer.stats.kit import empirical as EK


class EmpiricalRepairs(unittest.TestCase):
    def test_walk_spectrum_against_exhaustive_paths(self):
        for n in range(1,12):
            paths=np.array(list(itertools.product((-1,1),repeat=n)))
            truth=np.abs(np.cumsum(paths,axis=1)).max(axis=1).mean()
            self.assertAlmostEqual(C.walk_max_abs_expectation(n),truth,places=11)

    def test_walk_large_limit(self):
        value=C.walk_max_abs_expectation(2000)/math.sqrt(2000)
        self.assertLess(abs(value-math.sqrt(math.pi/2)),.025)

    def test_chaining_positive_part_and_full_tail(self):
        full=C.chaining_bound(200)
        for levels in (1,5,20,40):
            bound=C.chaining_bound(levels)
            self.assertGreater(bound['terms'][1],0)
            self.assertGreaterEqual(bound['bound']+1e-13,sum(full['terms']))
            self.assertLessEqual(sum(bound['terms']),sum(full['terms'])+1e-13)
        self.assertGreater(full['bound'],math.sqrt(2/math.pi))

    def test_histogram_retains_outside_mass(self):
        v=np.array([-2.,.2,.7,2.]);edges=np.array([0.,.5,1.])
        self.assertAlmostEqual(float(np.sum(C.hist(v,edges)*np.diff(edges))),.5)

    def test_tied_bootstrap_against_explicit_resampling(self):
        x=np.array([1.,1.,1.,2.,4.,4.]);B=2000
        idx=C.rng(11).integers(0,len(x),size=(B,len(x)))
        grid=np.unique(x);fn=np.array([(x<=t).mean() for t in grid])
        db=np.max(np.abs(np.array([[(row<=t).mean() for t in grid] for row in x[idx]])-fn),axis=1)
        self.assertEqual(C.bootstrap_ks_quantile(x,C.rng(11),B),np.quantile(db,.95))

    def test_constant_sample_has_zero_resampling_process(self):
        for f in (C.bootstrap_ks_quantile,C.multiplier_ks_quantile):
            self.assertEqual(f(np.ones(10),C.rng(4),B=200),0.)

    def test_tied_multiplier_against_direct_weighted_indicators(self):
        x=np.array([1.,1.,2.,3.,3.]);B=1000
        weights=C.rng(32).standard_normal((B,len(x)))
        proc=np.array([weights@((x<=t)-(x<=t).mean())/len(x) for t in np.unique(x)])
        expected=np.quantile(np.max(np.abs(proc),axis=0),.95)
        self.assertAlmostEqual(C.multiplier_ks_quantile(x,C.rng(32),B),expected,places=14)

    def test_classifier_sup_against_dense_grid(self):
        generator=C.rng(25)
        for _ in range(20):
            x=np.sort(generator.random(15));y=generator.integers(0,2,15)
            grid=np.unique(np.r_[np.linspace(0,1,10001),x,np.nextafter(x,-np.inf),.3])
            empirical=np.mean((x[None,:]>grid[:,None])!=y,axis=1)
            truth=np.max(np.abs(empirical-(.2+.6*np.abs(grid-.3))))
            self.assertAlmostEqual(C.threshold_sup(x,y),truth,places=12)

    def test_band_monte_carlo_uncertainty(self):
        result=C.band_coverage(8,50,33)
        for key in ('kolmogorov','exact','dkw','bootstrap','multiplier'):
            p=result[key]
            self.assertAlmostEqual(result['mc_se'][key],math.sqrt(p*(1-p)/49),places=14)

    def test_grenander_nonnegative_decreasing_and_integrates(self):
        from explainer.stats.kit import smooth
        g=smooth.grenander(C.rng(20).exponential(size=200))
        self.assertTrue(np.all(np.diff(g['density'])<=1e-12))
        self.assertTrue(np.all(g['density']>=0))
        self.assertAlmostEqual(float(np.dot(np.diff(g['knots']),g['density'])),1.,places=13)

if __name__=='__main__':unittest.main()
