"""Independent probability and regression references for the Part 44 lab."""
import numpy as np
from numpy.testing import assert_allclose, assert_array_equal
from scipy import stats
import statsmodels.api as sm
from videos.stats.stats44 import compute as C
from explainer.stats.kit import chains as CH


def test_borel_same_half_meridian_has_two_different_limits():
    g=np.random.default_rng(771);n=800_000;eps=.025
    d=C.sphere_conditioning(g.uniform(-1,1,n),g.uniform(-np.pi,np.pi,n),eps)
    # Each neighborhood tends to exactly the same y=0, x>0 half-meridian.
    for key in ('wedge','band'):
        assert np.all(d['x'][d[key]]>0)
        assert np.max(abs(d['y'][d[key]]))<=eps
    # Integrate the limiting densities analytically on |phi|<=pi/4.
    for key,p in [('wedge',np.sin(np.pi/4)),('band',.5)]:
        sample=d['angle'][d[key]]
        observed=np.mean(abs(sample)<=np.pi/4)
        assert abs(observed-p)<6*np.sqrt(p*(1-p)/len(sample))+.001


def test_finite_urn_is_uniform_lattice_and_ks_uses_both_cdf_sides():
    for steps in (1,5,25,600):
        k=np.arange(steps+1)
        assert_allclose(stats.betabinom.pmf(k,steps,1,1),np.full(steps+1,1/(steps+1)),atol=2e-14)
    for counts in ([1,1,1],[0,3,0],[3,0,1,2]):
        counts=np.array(counts);cdf=np.r_[0,np.cumsum(counts)/counts.sum()]
        ref=np.max(abs(cdf-np.linspace(0,1,len(cdf))))
        assert_allclose(C.uniform_lattice_ks(counts),ref,atol=1e-15)


def test_walk_maximum_includes_time_zero():
    assert_array_equal(C.walk_maximum([[-1.,-2.,-3.],[-1.,2.,1.]]),[0.,2.])


def test_coverage_uncertainty_uses_actual_independent_replicates():
    covered=np.array([True,False,True,True,False,False,True])
    row=C.coverage_row('reference','seven independent runs',covered)
    assert row.reps==7
    assert_allclose(row.mc_se,stats.sem(covered.astype(float)),atol=1e-15)
    assert_allclose(row.achieved,4/7,atol=1e-15)


def test_ar1_intercept_fits_match_statsmodels():
    y=C.ar1_paths(.7,80,5,np.random.default_rng(912))
    phi,se=C.ar1_fit_many(y)
    for i,series in enumerate(y):
        ref=sm.OLS(series[1:],sm.add_constant(series[:-1])).fit()
        assert_allclose([phi[i],se[i]],[ref.params[1],ref.bse[1]],atol=1e-12)


def test_dickey_fuller_no_constant_matches_independent_regressions():
    n,reps,seed=40,5,723
    result=CH.dickey_fuller(n,reps,np.random.default_rng(seed))
    innovations=np.random.default_rng(seed).standard_normal((reps,n))
    for i,e in enumerate(innovations):
        y=np.r_[0.,np.cumsum(e)]
        ref=sm.OLS(np.diff(y),y[:-1,None]).fit()
        assert_allclose(result['t'][i],ref.tvalues[0],atol=1e-12)
        assert_allclose(result['n_rho'][i],n*ref.params[0],atol=1e-12)
        assert_allclose(2*np.dot(y[:-1],e),y[-1]**2-np.dot(e,e),atol=1e-12)


def test_viewport_histogram_does_not_renormalize_omitted_tails():
    h,e=C.histogram_density([-9.,.1,.4,.9,20.],bins=2,range=(0,1))
    assert_allclose(np.sum(h*np.diff(e)),3/5)
