"""Independent numerical checks for the Part 56 selective-inference examples."""
import math
import numpy as np
import pytest
from scipy import integrate, special, stats
from videos.stats.stats56 import checked as C


def test_extreme_truncated_normal_endpoints_have_correct_pivots():
    for y,a,b in [(1e-8,0,np.inf),(40.2,40,np.inf),(2.6,1,3)]:
        lo,hi=C.truncnorm_interval(y,1,a,b)
        assert np.isfinite([lo,hi]).all()
        assert C.truncnorm_sf(y,lo,1,a,b)==pytest.approx(.025,abs=2e-9)
        assert C.truncnorm_sf(y,hi,1,a,b)==pytest.approx(.975,abs=2e-9)
    assert C.truncnorm_interval(1e-8,1,0,np.inf)[0] < -1e8


def test_truncated_pivot_matches_scipy_and_reflection():
    for mu in [-7,0,4,12]:
        got=C.truncnorm_sf(2.6,mu,1,1,3)
        assert got==pytest.approx(stats.truncnorm.sf(2.6,1-mu,3-mu,loc=mu),abs=2e-12)
        assert got+C.truncnorm_sf(-2.6,-mu,1,-3,-1)==pytest.approx(1,abs=2e-12)
    assert np.isfinite(C._log_mass(-1e-18,1e-18))


def test_polyhedron_is_invariant_to_extreme_positive_row_scaling():
    A=np.array([[1.,0],[-1.,0],[0,1.]])
    b=np.array([3.,-1,2]);y=np.array([2.,1.]);eta=np.array([1.,0])
    reference=C.polyhedral_limits(A,b,y,eta)
    scale=np.array([1e-20,1e20,1e-9])
    assert C.polyhedral_limits(A*scale[:,None],b*scale,y,eta)==reference
    with pytest.raises(ValueError):C.polyhedral_limits(A,b,[2.,3.],eta)


def test_lasso_solution_satisfies_kkt_and_event_along_contrast():
    rng=np.random.default_rng(102);X=rng.normal(size=(35,6));y=2*X[:,0]+rng.normal(size=35)
    ev=C.lasso_event(X,y,4);assert np.all(ev['A']@y<=ev['b']+1e-8)
    eta=ev['pinv'][0];lim=C.polyhedral_limits(ev['A'],ev['b'],y,eta)
    c=eta/(eta@eta);z=y-c*(eta@y)
    for t in np.linspace(lim['stat']-4,lim['stat']+4,15):
        fits=C.lasso_event(X,z+c*t,4)
        same=np.array_equal(fits['E'],ev['E']) and np.array_equal(fits['signs'],ev['signs'])
        assert same==(lim['lo']<t<lim['hi'])


def test_winner_singleton_reduces_to_ordinary_interval():
    w=C.winner_conditional([1.2])
    assert [w['lo'],w['hi']]==pytest.approx(stats.norm.interval(.95,loc=1.2))
    assert w['median_unbiased']==pytest.approx(1.2)


def test_hybrid_is_contained_in_projection_even_at_rounded_boundaries():
    rng=np.random.default_rng(5602)
    for K in [1,10,6033]:
        for _ in range(25):
            y=rng.normal(size=K);h=C.winner_hybrid(y)
            assert h['projection'][0]<=h['lo']<=h['hi']<=h['projection'][1]


def test_randomized_survival_matches_direct_integration():
    for y,mu,gamma in [(2.2,-3,.5),(1.,-2,1.),(3.,2.,2.)]:
        numerator=integrate.quad(lambda v:stats.norm.pdf(v-mu)*special.ndtr((v-2)/gamma),y,np.inf,epsabs=1e-13)[0]
        expected=numerator/special.ndtr((mu-2)/math.hypot(1,gamma))
        assert C.randomized_sf(y,mu,2,1,gamma,True)==pytest.approx(expected,abs=2e-9)


def test_randomized_interval_endpoints_match_independent_quadrature():
    iv=C.threshold_selective(1.,2,gamma=.5)
    assert iv['lo'] < -7  # outside the former fixed location grid
    assert C.randomized_sf(1.,iv['lo'],2,1,.5,True)==pytest.approx(.025,abs=1e-7)
    assert C.randomized_sf(1.,iv['hi'],2,1,.5,True)==pytest.approx(.975,abs=1e-7)


def test_analytic_clustering_region_matches_direct_reclustering():
    rng=np.random.default_rng(5609)
    for n in [4,8,20,40]:
        for _ in range(12):
            x=rng.normal(size=n);r=C.clustering_region(x)
            for phi in np.r_[np.linspace(0,10,81),r['d']]:
                perturbed=x+(phi-r['d'])*r['nu']/r['nn']
                same=np.array_equal(C.two_means_1d(perturbed),r['labels'])
                inside=any(a<=phi<=b for a,b in r['intervals'])
                assert same==inside


def test_clustering_pvalue_matches_integrated_selection_region():
    x=np.array([-2.,-1.4,-.8,.2,1.3,2.1]);r=C.clustering_pvalues(x)
    sd=r['sd']
    denominator=sum(integrate.quad(lambda v:stats.norm.pdf(v/ sd)/sd,a,b)[0] for a,b in r['intervals'])
    numerator=sum(integrate.quad(lambda v:stats.norm.pdf(v/sd)/sd,max(a,r['d']),b)[0] for a,b in r['intervals'] if b>r['d'])
    assert r['selective']==pytest.approx(numerator/denominator,abs=2e-10)


def test_known_variance_cluster_pivots_are_calibrated_under_gaussian_null():
    rng=np.random.default_rng(56111)
    ps=np.array([C.clustering_pvalues(rng.normal(size=20))['selective'] for _ in range(600)])
    assert stats.kstest(ps,'uniform').pvalue>.001
    assert abs(np.mean(ps<.05)-.05)<4*math.sqrt(.05*.95/len(ps))


def test_knockoff_covariance_and_lasso_swap_flip():
    rng=np.random.default_rng(5701);S=np.array([[1,.4],[.4,1]])
    X=rng.multivariate_normal([0,0],S,30000);Xk=C.gaussian_knockoffs(X,S,rng)
    observed=np.cov(np.c_[X,Xk],rowvar=False)
    assert np.allclose(observed[:2,:2],observed[2:,2:],atol=.025)
    assert np.allclose(observed[:2,2:]-S,np.diag(np.diag(observed[:2,2:]-S)),atol=.025)
    y=X[:100]@np.array([1.,0])+rng.normal(size=100)
    W=C.lasso_W(X[:100],Xk[:100],y,.1)
    a,b=X[:100].copy(),Xk[:100].copy();a[:,0],b[:,0]=b[:,0].copy(),a[:,0].copy()
    assert C.lasso_W(a,b,y,.1)==pytest.approx(W*np.array([-1,1]),abs=2e-7)


def test_conformal_joint_guarantee_does_not_imply_conditional_null_validity():
    # n=9, all scores tied, IID rare null labels. p=(1+Bin(9,.1))/10.
    conditional=stats.binom.cdf(0,9,.1)
    joint=.1*conditional
    assert conditional>.1
    assert joint<=.1


def test_ratio_standard_error_uses_independent_datasets():
    counts=np.array([1.,3,2,4]);hits=np.array([1.,0,2,4]);p=hits.sum()/counts.sum()
    expected=np.std((hits-p*counts)/counts.mean(),ddof=1)/2
    assert C.ratio_mcse(hits,counts)==pytest.approx(expected)
