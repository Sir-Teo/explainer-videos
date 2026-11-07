"""Independent checks of the explicit minimax constructions used in Part 50."""
import math
import unittest
import numpy as np
from scipy import integrate, stats
from videos.stats.stats50 import compute as C
from explainer.stats.kit import gsm as G


class MinimaxRepairs(unittest.TestCase):
    def test_density_pair_is_normalized_positive_and_in_class(self):
        for w in (.1,.3,.5):
            x=np.linspace(-5,5,50001);f0,f1,h=C.lecam_density_pair(x,w)
            self.assertGreaterEqual(f1.min(),0)
            mass=integrate.quad(lambda t:float(C.lecam_density_pair(np.array([t]),w)[1][0]),-10,10,points=[-w,w,1-w,1+w],epsabs=1e-10)[0]
            self.assertAlmostEqual(mass,1.,places=9)
            for order in (0,1,2):
                values=f1
                for _ in range(order):values=np.gradient(values,x)
                self.assertLess(np.max(np.abs(values[100:-100])),1.001)
            self.assertAlmostEqual(C.lecam_density_pair(np.array([0.]),w)[1][0]-stats.norm.pdf(0),h,places=14)

    def test_density_chi_square_against_adaptive_quadrature(self):
        result=C.lecam_density_point(4000);w=result['w']
        def integrand(x):
            p,q,_=C.lecam_density_pair(np.array([x]),w)
            return float((q[0]-p[0])**2/p[0])
        exact=sum(integrate.quad(integrand,a,b,epsabs=1e-14)[0] for a,b in [(-w,w),(1-w,1+w)])
        self.assertAlmostEqual(result['chi2'],exact,places=13)
        tv=integrate.quad(lambda x:abs(float(C.lecam_density_pair(np.array([x]),w)[1][0]-stats.norm.pdf(x)))/2,-w,1+w,points=[w,1-w],epsabs=1e-12)[0]
        self.assertLessEqual(tv,math.sqrt(exact)+1e-12)

    def test_projection_minimax_constant(self):
        ratios=[]
        for eps in (.01,.001,.0001):
            N=np.arange(0,10001);risk=N*eps**2+1/(N+1.)**2
            pinsker=G.pinsker(eps,G.sobolev_weights(10000,1.),1.)['risk']
            ratios.append(risk.min()/pinsker)
        self.assertLess(abs(ratios[-1]-3**(2/3)),.01)
        self.assertAlmostEqual((3**(2/3))**1.5,3.)

    def test_gaussian_prior_is_not_supported_on_ellipsoid(self):
        a=G.sobolev_weights(100,1.);p=G.pinsker(.03,a,1.)
        energy=np.sum(a*a*p['prior_var'])
        self.assertAlmostEqual(energy,1.,places=11)
        draws=np.random.default_rng(10).normal(size=(5000,len(a)))*np.sqrt(p['prior_var'])
        outside=np.mean(np.sum((draws*a)**2,axis=1)>1.)
        self.assertGreater(outside,.2)

    def test_assouad_kl_and_integrated_separation(self):
        n=83
        for s in (1.,2.):
            d=C.assouad_holder(n,s);m=d['m'];h=d['h'];x=np.arange(1,n+1)/n
            divergences=[]
            for j in range(m):
                u=2*m*(x-(j+.5)/m)
                b=np.maximum(1-np.abs(u),0) if s==1 else C.polynomial_bump(u)
                divergences.append(np.dot(h*b,h*b)/2)
            self.assertAlmostEqual(max(divergences),d['max_neighbour_kl'],places=12)
            fun=(lambda u:max(1-abs(u),0)) if s==1 else (lambda u:float(C.polynomial_bump(u)))
            sep=integrate.quad(lambda u:(h*fun(u))**2,-1,1,epsabs=1e-13)[0]/(2*m)
            self.assertAlmostEqual(sep,d['coordinate_l2_separation_squared'],places=13)
            self.assertAlmostEqual(d['bound'],m*sep*(1-d['tv_upper'])/8,places=14)

    def test_lepski_can_recover_after_a_failed_candidate(self):
        self.assertEqual(C.lepski(np.array([0.,1.,3.,1.5]),np.array([1.,1.,.9,.8]),2.),3)

    def test_higher_criticism_against_direct_cdf_supremum(self):
        x=np.array([-1.,-.2,.3,1.,2.,3.]);n=len(x);p=stats.norm.sf(x)
        grid=np.unique(np.r_[1/n,.5,p[(p>=1/n)&(p<=.5)]])
        reference=max([0.]+[math.sqrt(n)*((p<=t).mean()-t)/math.sqrt(t*(1-t)) for t in grid])
        self.assertAlmostEqual(float(C.higher_criticism(x)[0]),reference)
        self.assertTrue(np.isfinite(C.higher_criticism(np.full(20,100.))).all())
        self.assertGreater(C.higher_criticism(np.full(20,100.))[0],10.)
        self.assertEqual(C.higher_criticism(np.full(20,-100.))[0],0.)

    def test_normal_kde_mse_against_simulation(self):
        n,h,reps=80,.3,5000
        values=C.kde_at(np.random.default_rng(7).normal(size=(reps,n)),0,h)
        errors=(values-stats.norm.pdf(0))**2
        self.assertLess(abs(errors.mean()-C.kde_normal_mse(n,h)),4*errors.std(ddof=1)/math.sqrt(reps))

    def test_fixed_window_risks_are_bias_squared_plus_noise(self):
        f=lambda x:2*x*x+3*x;n=70;x0=.5;hs=np.array([.03,.1,.2])
        x=np.arange(1,n+1)/n;values=C.fixed_window_risks(f,x0,n,hs)
        for h,value in zip(hs,values):
            ix=np.abs(x-x0)<=h;truth=f(x0)
            expected=(np.mean(2*x[ix]**2+3*x[ix])-truth)**2+1/ix.sum()
            self.assertAlmostEqual(value,expected)

    def test_bias_aware_gaussian_interval_controls_worst_bias(self):
        f=lambda x:np.sin(2*np.pi*x)+2*np.exp(-200*(x-.5)**2)
        x=np.arange(1,2001)/2000;L1=2*math.pi+40*math.exp(-.5);L2=4*math.pi**2+800
        for h in (.005,.02,.08):
            radius,bias=C.bias_aware_radius(x,.5,h,L1,L2)
            ix=np.abs(x-.5)<=h;actual=abs(f(x[ix]).mean()-2.)
            self.assertLessEqual(actual,bias+1e-12)
            se=1/math.sqrt(ix.sum())
            coverage=stats.norm.cdf((radius-bias)/se)-stats.norm.cdf((-radius-bias)/se)
            self.assertGreaterEqual(coverage,.95-1e-12)

    def test_planted_clique_edge_count_matches_binomial_law(self):
        generator=np.random.default_rng(17);n,k,reps=12,5,5000;N=n*(n-1)//2;m=k*(k-1)//2
        values=np.array([G.planted_clique(n,k,generator).sum()/2 for _ in range(reps)])
        self.assertLess(abs(values.mean()-(m+(N-m)/2)),4*math.sqrt((N-m)/4/reps))
        self.assertLess(abs(values.var()-(N-m)/4),1.)

    def test_fast_packing_matches_candidate_by_candidate(self):
        seed,d,trials=12,10,100
        generator=np.random.default_rng(seed);points=[]
        for _ in range(trials):
            v=generator.integers(0,2,d)
            if all(np.sum(v!=u)>=d/8 for u in points):points.append(v)
        fast=C.varshamov_gilbert(d,np.random.default_rng(seed),trials)
        np.testing.assert_array_equal(fast['pts'],points)

if __name__=='__main__':unittest.main()
