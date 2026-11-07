"""Independent checks for empirical quantiles and certified transport computations."""
import itertools
import math
import numpy as np
import pytest
from scipy import stats
from videos.stats.stats61 import checked as O


def test_step_quantile_barycenter_exact_moments():
    samples=[[0,10],[1,2,3]];w=np.array([.3,.7])
    a=O.quantile_atoms(samples,w)
    assert a['mass'].sum()==pytest.approx(1)
    assert a['mean']==pytest.approx(.3*5+.7*2)
    # On sixths of the unit interval the empirical quantile values are explicit.
    values=.3*np.array([0,0,0,10,10,10])+.7*np.array([1,1,2,2,3,3])
    assert a['sd']==pytest.approx(values.std())
    assert len(a['mass'])==4  # Common breakpoints merged, not 6 equal-grid observations.


def test_wasserstein_decomposition_matches_full_empirical_integral():
    x=np.array([0,2,5.]);y=np.array([-1,1,2,8.])
    d=O.quantile_decomposition(x,y)
    assert d['total']==pytest.approx(O.wasserstein_1d(x,y,2)**2)
    assert abs(d['residual'])<1e-12 and d['shape']>=0
    assert d['location']==pytest.approx((x.mean()-y.mean())**2)
    assert d['spread']==pytest.approx((x.std()-y.std())**2)


def test_barycenter_location_scale_and_variance_inequality():
    z=np.array([-2,-1,0,1,3.]);s=[1+2*z,4+3*z]
    a=O.quantile_atoms(s,[.25,.75]);b=O.quantile_atoms([1+2*z,np.array([0,4,10])],[.25,.75])
    assert a['sd']==pytest.approx(2.75*z.std())
    assert b['sd']<=.25*np.std(s[0])+.75*np.std([0,4,10])+1e-12


def test_lp_against_permutation_enumeration_and_dual():
    r=np.random.default_rng(611);C=r.uniform(size=(4,4));a=np.full(4,.25)
    o=O.kantorovich_lp(a,a,C)
    exact=min(C[np.arange(4),p].mean() for p in itertools.permutations(range(4)))
    assert o['cost']==pytest.approx(exact)
    assert abs(o['audit']['duality_gap'])<1e-10
    assert o['audit']['marginal_residual']<1e-10
    with pytest.raises(ValueError):O.kantorovich_lp([.5,.6],[1],np.zeros((2,1)))


def test_sinkhorn_relative_entropy_objective_and_residuals():
    a=np.array([.2,.3,.5]);b=np.array([.4,.6]);C=np.array([[0,2],[1,3],[4,.2]])
    o=O.sinkhorn(a,b,C,.4,10000,1e-11);P=o['P']
    divergence=np.sum(np.where(P>0,P*np.log(P/(a[:,None]*b)),0))
    assert o['obj']==pytest.approx(np.sum(P*C)+.4*divergence)
    assert o['audit']['converged'] and o['audit']['marginal_l1']<1e-11
    assert abs(o['audit']['primal_dual_difference'])<1e-9
    with pytest.raises(RuntimeError):O.sinkhorn(a,b,C,.01,1,1e-14)
    with pytest.raises(ValueError):O.sinkhorn(a,b,C,0)


def test_sinkhorn_cost_translation_and_independent_limit():
    a=np.array([.3,.7]);b=np.array([.6,.4]);C=np.array([[0,1],[2,0.]])
    first=O.sinkhorn(a,b,C,.8);second=O.sinkhorn(a,b,C+3,.8)
    np.testing.assert_allclose(first['P'],second['P'],atol=1e-10)
    assert second['obj']-first['obj']==pytest.approx(3,abs=1e-8)
    np.testing.assert_allclose(O.sinkhorn(a,b,C,1e6)['P'],a[:,None]*b,atol=1e-6)


def test_squared_cost_sinkhorn_limit_is_squared_mean_gap():
    X=np.array([[-1.],[1.]]);Y=np.array([[-2.],[2.]])
    assert O.sinkhorn_divergence(X,Y,1e5)==pytest.approx(0,abs=1e-4)
    assert O.sinkhorn_divergence(X,Y+3,1e5)==pytest.approx(9,abs=1e-4)
    assert O.sinkhorn_divergence(X,X,.5)==pytest.approx(0,abs=1e-12)


def test_entropic_map_barycentric_projection_at_training_points():
    X=np.array([[-1.,0],[0,1],[2,1]]);Y=np.array([[-2,1],[1,2],[3,0.]])
    eps=.4;a=np.full(3,1/3)
    plan=O.sinkhorn(a,a,O.cost_matrix(X,Y,2)/2,eps,50000,1e-11)
    T=O.entropic_map(X,Y,eps)
    np.testing.assert_allclose(T(X),(plan['P']/plan['P'].sum(1)[:,None])@Y,atol=1e-8)
    assert T.audit['converged']


def test_gaussian_ula_matches_direct_recursion_and_stationary_bias():
    Sig=np.array([[1.,.7],[.7,1.]]);mu=np.array([1.,-2.]);m0=np.array([4.,0]);S0=np.eye(2)*.2;h=.03
    M=np.eye(2)-h*np.linalg.inv(Sig);m,S=m0.copy(),S0.copy()
    for _ in range(40):m=mu+M@(m-mu);S=M@S@M.T+2*h*np.eye(2)
    exact=O.gaussian_ula(m0,S0,mu,Sig,h,40)
    np.testing.assert_allclose(exact[0],m,atol=1e-12);np.testing.assert_allclose(exact[1],S,atol=1e-12)
    stationary=O.gaussian_ula(mu,Sig,mu,Sig,h,10000)[1]
    assert np.linalg.eigvalsh(stationary-Sig).min()>0
    with pytest.raises(ValueError):O.gaussian_ula(m0,S0,mu,Sig,1.,40)


def test_rank_energy_randomized_ties_control_identical_null():
    r=np.random.default_rng(612);rejections=0
    X=np.zeros((8,2))
    for _ in range(160):
        p=O.rank_energy_test(X,X,r,99)['p'];assert .01<=p<=1
        rejections+=p<=.05
    assert rejections<=16
    with pytest.raises(ValueError):O.rank_energy_test(X,X,r,99,np.zeros((16,2)))


def test_rate_harness_records_empirical_standard_error():
    o=O.empirical_rate(2,[5,10],4,np.random.default_rng(613))
    np.testing.assert_allclose(o['W'],np.mean(o['draws'],axis=1))
    np.testing.assert_allclose(o['mcse'],np.std(o['draws'],axis=1,ddof=1)/2)


def test_gaussian_barycenter_fixed_point_and_failure():
    covs=[np.array([[2.,.4],[.4,1.]]),np.array([[1.,-.3],[-.3,3.]])]
    S=O.gaussian_barycenter(covs);root=O.sqrtm_psd(S)
    np.testing.assert_allclose(S,sum(O.sqrtm_psd(root@c@root) for c in covs)/2,atol=1e-10)
    with pytest.raises(RuntimeError):O.gaussian_barycenter(covs,iters=1,tol=1e-16)
    with pytest.raises(ValueError):O.gaussian_barycenter([np.diag([-1,2])])
