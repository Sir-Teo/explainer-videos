"""Independent reference checks for the likelihood demonstrations."""
import numpy as np
import pytest
from scipy import optimize, stats
from scipy.special import expit

from videos.stats.stats22 import compute as C
from explainer.stats.kit import mle as M


def test_louis_information_matches_independent_finite_difference_hessian():
    x = np.linspace(-3,5,100)
    theta = [.4,-.3,.8,2.,1.2]
    w = 20*(.4*stats.norm.pdf(x,-.3,.8)+.6*stats.norm.pdf(x,2,1.2))
    actual = C.louis_mixture_information(x,w,theta)
    expected = -M.numerical_hessian(lambda t: M.mix_loglik(x,t,w),theta,h=1e-5)
    np.testing.assert_allclose(actual,expected,atol=2e-4,rtol=2e-5)


def test_logistic_profile_endpoints_match_independent_nuisance_optimization():
    g=np.random.default_rng(22)
    x=g.normal(size=70)
    y=(g.random(70)<expit(-.3+2.5*x)).astype(float)
    fit=C.logistic_slope_tests(x,y)
    lo,hi=C.logistic_profile_ci(x,y)
    for slope in [lo,hi]:
        result=optimize.minimize_scalar(
            lambda a:-np.sum(y*(a+slope*x)-np.logaddexp(0,a+slope*x)),
            bounds=(-30,30),method='bounded',options={'xatol':1e-12})
        assert 2*(fit['ll']+result.fun)==pytest.approx(stats.chi2.ppf(.95,1),abs=1e-7)
    assert lo<fit['b'][1]<hi


def test_separation_is_disclosed_and_profile_has_unbounded_endpoint():
    x=np.arange(-3.,4.)
    y=(x>0).astype(float)
    fit=C.logistic_slope_tests(x,y)
    assert not fit['finite'] and np.isnan(fit['z'])
    lo,hi=C.logistic_profile_ci(x,y)
    assert np.isfinite(lo) and np.isposinf(hi)
    assert C.logistic_profile_ci(x,np.ones(len(x)))==(-np.inf,np.inf)


def test_bootstrap_grouping_retains_all_overflow_observations():
    y=np.array([-100.,-.5,.5,1.5,100.])
    counts=C.binned_counts(y,[0,1,2])
    np.testing.assert_array_equal(counts,[2,1,2])
    assert counts.sum()==len(y)


def test_gamma_profile_mle_and_interval_use_exact_score_and_lr_roots():
    d=C.compute_gamma()
    idx=C.W.sample(150,among=C.W.adult,seed=2201)
    x=C.W.income[idx]/1000
    shape,_,scale=stats.gamma.fit(x,floc=0)
    assert d['n']==len(x)
    assert d['a_hat']==pytest.approx(shape,rel=1e-8)
    assert d['b_hat']==pytest.approx(1/scale,rel=1e-8)
    for a in d['profile_ci']:
        ll=M.gamma_loglik(x,a,a/x.mean())
        assert 2*(d['loglik_max']-ll)==pytest.approx(stats.chi2.ppf(.95,1),abs=1e-8)


def test_midpoint_density_fit_respects_the_scale_constraint():
    x=np.array([-.3,0.,.3,2.,2.3])
    counts=np.array([1.,50.,1.,20.,2.])
    fit=C.midpoint_em(x,counts,[[.5,0,.4,2,.4]],min_sd=.2)
    assert fit['theta'][2]>=.2 and fit['theta'][4]>=.2
    reference=optimize.minimize(lambda t:-M.mix_loglik(x,t,counts),fit['theta'],
        method='Nelder-Mead',bounds=[(.001,.999),(-10,10),(.2,5),(-10,10),(.2,5)],
        options={'maxiter':2000,'xatol':1e-9,'fatol':1e-9})
    assert -reference.fun==pytest.approx(fit['loglik'],abs=2e-6)


def test_geometric_clipping_does_not_flatten_curves_or_bridge_missing_values():
    pieces=C.clipped_segments([0,1,2,3],[0,2,np.nan,0],(0,3,0,1))
    assert len(pieces)==1
    np.testing.assert_allclose(pieces[0][1],[.5,1])

def test_grouped_likelihood_remains_bounded_when_a_midpoint_density_spikes():
    x,w=C.museum.crabs()
    j=int(np.argmax(w))
    theta=[.4,x[j],1e-5,.655,.015]
    small=theta.copy()
    small[2]=1e-12
    assert M.mix_loglik(x,small,w)>M.mix_loglik(x,theta,w)+1000
    assert C.grouped_mix_loglik(C.museum.CRAB_UPPER,w,small)<=0
    assert C.grouped_mix_loglik(C.museum.CRAB_UPPER,w,small)==pytest.approx(
        C.grouped_mix_loglik(C.museum.CRAB_UPPER,w,theta),abs=1e-8)
