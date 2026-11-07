"""Independent checks for the numerical claims used in Part 46."""
import math

import numpy as np
from numpy.testing import assert_allclose
from scipy import stats

from videos.stats.stats46 import compute as C
from explainer.stats.kit import testing as T


def test_fieller_is_pivot_inversion_including_transition():
    a,b,va,vb,c=3.,.8,1.,.7,.2
    f=C.fieller(a,b,va,vb,c)
    grid=np.linspace(-20,20,4001)
    expected=(a-grid*b)**2<=stats.norm.ppf(.975)**2*(va-2*grid*c+grid**2*vb)
    actual=(grid<=f['lo'])|(grid>=f['hi']) if f['kind']=='exclusive' else (grid>=f['lo'])&(grid<=f['hi'])
    assert_allclose(actual,expected)
    z=stats.norm.ppf(.975)
    boundary=C.fieller(1.,z,1.,1.)
    assert boundary['kind']=='halfline' and boundary['hi']==np.inf
    assert_allclose(boundary['lo'],(1-z*z)/(2*z))


def test_logistic_centering_preserves_score_and_information():
    dose,n,k=C.museum.bliss();b,V=C._logistic(dose,n,k)
    X=np.c_[np.ones_like(dose),dose];p=stats.logistic.cdf(X@b)
    assert np.max(np.abs(X.T@(k-n*p)))<2e-7
    assert_allclose(V,np.linalg.inv(X.T@((n*p*(1-p))[:,None]*X)),rtol=1e-9)
    assert 1.7 < -b[0]/b[1] < 1.9  # log10 dose, not original dose


def test_poisson_empty_limit_is_empty_even_at_zero_signal():
    f=C.flipflop_intervals(3.,.9,nmax=60)
    assert f['lo'][0]>f['hi'][0]
    n=np.arange(61);hit=(f['lo']<=0)&(f['hi']>=0)
    expected=stats.poisson.pmf(n,3)@hit
    assert_allclose(T.poisson_coverage(f['lo'],f['hi'],3,[0])[0],expected)
    assert not hit[0]


def test_fc_ordering_has_required_probability_on_grid():
    mus=np.array([0.,.13,1.27,2.34,5.1,8.])
    r=T.fc_intervals(3,.9,mu_grid=mus,nmax=80)
    mass=np.sum(r['acc']*stats.poisson.pmf(np.arange(81)[None,:],mus[:,None]+3),axis=1)
    assert np.all(mass>=.9-1e-13)
    best=np.maximum(3,np.arange(81))
    for i,mu in enumerate(mus):
        ratios=np.exp(stats.poisson.logpmf(np.arange(81),mu+3)-stats.poisson.logpmf(np.arange(81),best))
        assert ratios[r['acc'][i]].min()>=ratios[~r['acc'][i]].max()-1e-13


def test_conditional_normal_quadrature_matches_fresh_draws():
    g=np.random.default_rng(460600)
    for delta in (0.,.5,2.,4.):
        exact=C.t2_conditional_exact(delta)
        sim=T.t2_conditional(delta,1+math.sqrt(2),400000,g)
        nsel=400000*sim['share'];se=math.sqrt(exact['conditional']*(1-exact['conditional'])/nsel)
        assert abs(exact['conditional']-sim['conditional'])<5*se
        assert abs(exact['share']-sim['share'])<.003
    k=1+math.sqrt(2)
    assert_allclose(C.t2_conditional_exact(0)['share'],2/math.pi*math.atan(k*math.sqrt(2)),rtol=1e-9)


def test_beta_mixture_calibration_needs_more_than_decreasing_density():
    for p in (.001,.01,.05,.1):
        xi=-1/math.log(p)
        bound=-math.e*p*math.log(p)
        assert_allclose(1/(xi*p**(xi-1)),bound,rtol=1e-13)
        # A uniform alternative on (0, .1) is decreasing, but violates this bound.
        if p==.05: assert .1 < bound


def test_normal_prior_bound_has_analytic_optimizer():
    for p in (.1,.05,.01,.001):
        d=T.berger_sellke(p);z=stats.norm.isf(p/2)
        variance=max(z*z-1,0)
        exact=math.sqrt(1+variance)*math.exp(-z*z*variance/(2*(1+variance)))
        assert_allclose(d['B_norm'],exact,rtol=2e-8)
    d=T.berger_sellke(.05)
    assert_allclose((1-d['all'])/d['all'],math.exp(stats.norm.isf(.025)**2/2),rtol=1e-13)


def test_lilliefors_statistic_uses_same_fitted_sample_sd():
    seed=460601;n=20;reps=90
    r=T.ks_estimated(n,reps,np.random.default_rng(seed))
    x=np.random.default_rng(seed).normal(size=(reps,n))
    independent=np.array([stats.kstest(row,lambda values:stats.norm.cdf((values-row.mean())/row.std(ddof=1))).statistic for row in x])
    assert_allclose(r['D'],independent,atol=1e-14)


def test_randomized_uniform_test_and_threshold_have_same_power():
    n=5;alpha=.05;theta0=1.;c=theta0*(1-alpha)**(1/n)
    for theta in (1.01,2.,10.):
        threshold=1-(c/theta)**n
        randomized=1-(1-alpha)*(theta0/theta)**n
        assert_allclose(threshold,randomized)


def test_neyman_structure_covers_degenerate_margin_slices():
    m,n=8,10;r=T.conditional_test(m,n)['phi']
    assert_allclose([r[0,0],r[m,m+n]],[.05,.05])
    for t in range(m+n+1):
        x=np.arange(max(0,t-n),min(m,t)+1)
        assert_allclose(stats.hypergeom.pmf(x,m+n,m,t)@r[x,t],.05,atol=1e-13)


def test_fiducial_quadrature_is_symmetric_and_has_correct_tail():
    g=np.random.default_rng(460602);phi=.17
    c=C.bf_critical(phi,5,25)
    assert_allclose(c,C.bf_critical(math.pi/2-phi,25,5),rtol=1e-11)
    draws=math.sin(phi)*g.standard_t(4,600000)-math.cos(phi)*g.standard_t(24,600000)
    assert abs(np.mean(np.abs(draws)>c)-.05)<.0015
    assert_allclose(C.bf_critical(0,5,25),stats.t.isf(.025,24),rtol=1e-12)
