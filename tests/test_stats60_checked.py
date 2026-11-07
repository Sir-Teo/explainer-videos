"""Independent boundary, identification and inferential checks for Part 60."""
import itertools
import math

import numpy as np
import pytest
from scipy import optimize, special, stats

from videos.stats.stats60 import checked as H


def test_depth_against_critical_halfplanes_and_affine_map():
    r=np.random.default_rng(601)
    X=np.r_[r.normal(size=(16,2)), [[0,0],[1,0],[-1,0]]]
    P=np.r_[r.normal(size=(12,2)), [[0,0],[1,0],[7,9]]]
    expected=[]
    for p in P:
        v=X-p
        angles=np.mod(np.arctan2(v[:,1],v[:,0])+math.pi/2,2*math.pi)
        angles=np.sort(np.r_[angles, np.mod(angles+math.pi,2*math.pi)])
        mids=(angles+np.r_[angles[1:],angles[0]+2*math.pi])/2
        normals=np.column_stack([np.cos(np.r_[angles,mids]),np.sin(np.r_[angles,mids])])
        expected.append(np.min(np.sum(v@normals.T>=-1e-11,axis=0))/len(X))
    np.testing.assert_allclose(H.tukey_depth_2d(P,X),expected)
    A=np.array([[2.,.7],[-.4,1.3]])
    np.testing.assert_allclose(H.tukey_depth_2d(P@A+3,X@A+3),expected)


def test_depth_coincident_and_grid_scope():
    assert H.tukey_depth_2d([[2,2]],np.full((6,2),2))[0]==1
    X=np.array([[0,0],[1,0],[0,1],[1,1]])
    d=H.tukey_median_2d(X,12)
    assert 'approximate' in d['scope']
    assert d['depth']==H.tukey_depth_2d([d['median']],X)[0]


def test_weighted_ci_reduces_to_mean_sem():
    y=np.array([1,2,4,9,11.])
    o=H.weighted_mean_ci(y,np.ones(5))
    assert o['mean']==y.mean()
    assert o['se']==pytest.approx(stats.sem(y))
    with pytest.raises(ValueError):H.weighted_mean_ci(y,-np.ones(5))


def test_joint_ratio_interval_on_gaussian_model():
    r=np.random.default_rng(602);means=[];ses=[];covered=[]
    for _ in range(120):
        xs=r.normal(size=(500,1));xt=r.normal(.45,1,size=(800,1))
        y=2*xs[:,0]+r.normal(size=500)
        o=H.ratio_weighted_mean_ci(xs,y,xt)
        means.append(o['mean']);ses.append(o['se']);covered.append(o['lo']<=.9<=o['hi'])
        assert o['logistic_score_residual']<1e-8
    assert abs(np.mean(means)-.9)<.04
    assert .75<np.mean(np.square(ses))/np.var(means,ddof=1)<1.3
    assert .89<np.mean(covered)<=1


def test_bbse_projection_consistency_and_nonidentification():
    labels=np.r_[np.zeros(10,int),np.ones(10,int)]
    pred=np.r_[np.zeros(8,int),np.ones(2,int),np.zeros(3,int),np.ones(7,int)]
    for target,q1 in [(np.zeros(10,int),0),(np.ones(10,int),1),([0,1]*5,.6)]:
        o=H.bbse_weights(pred,labels,target,2)
        assert o['q'][1]==pytest.approx(q1)
        np.testing.assert_allclose(o['w']*np.array([.5,.5]),o['q'])
    with pytest.raises(ValueError):H.bbse_weights(np.zeros(20,int),labels,[0,1],2)
    with pytest.raises(ValueError):H.bbse_weights([0,0],[0,0],[0,1],2)


def test_multiclass_bbse():
    y=np.repeat(np.arange(3),20)
    pred=y.copy();pred[[0,20,40]]=[1,2,0]
    o=H.bbse_weights(pred,y,np.repeat(np.arange(3),[10,20,30]),3)
    assert np.all(o['q']>=0) and o['q'].sum()==pytest.approx(1)
    assert o['moment_residual']<1e-7


@pytest.mark.parametrize('function',[H.dro_chi2,H.dro_kl])
def test_dro_primal_dual_and_scaling(function):
    l=np.array([.1,.2,1,4,4.])
    previous=l.mean()
    for rho in [0,1e-5,.03,.2,1,10]:
        o=function(l,rho,True)
        assert o['q'].sum()==pytest.approx(1)
        assert np.min(o['q'])>=0 and o['divergence']<=rho+1e-8
        assert -1e-8<=o['gap']<1e-7
        assert previous-1e-8<=o['value']<=4+1e-8
        assert function(7+3*l,rho)==pytest.approx(7+3*o['value'],abs=1e-7)
        previous=o['value']
    assert function(np.ones(5),2)==1


@pytest.mark.parametrize('function,divergence',[
    (H.dro_chi2,lambda q:.5*np.mean((len(q)*q-1)**2)),
    (H.dro_kl,lambda q:np.sum(special.xlogy(q,len(q)*q)))])
def test_dro_against_independent_constrained_primal(function,divergence):
    l=np.array([.2,.8,1.5,4.]);rho=.2
    fit=optimize.minimize(lambda q:-q@l,np.full(4,.25),bounds=[(1e-12,1)]*4,
        constraints=[{'type':'eq','fun':lambda q:q.sum()-1},
                     {'type':'ineq','fun':lambda q:rho-divergence(q)}],
        method='SLSQP',options={'ftol':1e-12,'maxiter':1000})
    assert fit.success
    assert function(l,rho)==pytest.approx(-fit.fun,abs=1e-7)


def test_empirical_subgroup_membership():
    l=np.array([.1,.3,2,4,7,10.]);mask=np.array([0,0,0,1,1,1],bool)
    p=mask.mean()
    assert H.dro_chi2(l,.5*(1/p-1))>=l[mask].mean()-1e-9
    assert H.dro_kl(l,-np.log(p))>=l[mask].mean()-1e-9


def test_anchor_against_dense_projection_and_identified_iv():
    r=np.random.default_rng(603);A=np.c_[np.ones(100),r.normal(size=100)]
    X=np.c_[np.ones(100),A[:,1]+r.normal(size=100)];y=X@np.array([1,2])+r.normal(size=100)
    P=A@np.linalg.pinv(A)
    for gamma in [0,.3,1,10]:
        W=np.eye(100)-(1-np.sqrt(gamma))*P
        np.testing.assert_allclose(H.anchor_regression(X,y,A,gamma),np.linalg.lstsq(W@X,W@y,rcond=None)[0],atol=1e-10)
    iv=np.linalg.solve(A.T@X,A.T@y)
    np.testing.assert_allclose(H.anchor_regression(X,y,A,1e9),iv,atol=1e-7)


def test_icp_gaussian_parent_test_and_intersection():
    r=np.random.default_rng(604);rejects=0
    for _ in range(160):
        env=np.repeat(np.arange(3),80);x=r.normal(env,1);y=1.5*x+r.normal(size=240)
        child=y+env+r.normal(size=240)
        o=H.icp(np.c_[x,child],y,env)
        rejects+=o['pvals']['(0,)']<=.05
        assert set(o['estimate'])<=set.intersection(*(set(a) for a in o['accepted'])) if o['accepted'] else not o['estimate']
    assert rejects<=16  # 10% is >3 Monte Carlo SE above nominal 5%.
    with pytest.raises(ValueError):H.icp(np.ones((20,1)),np.arange(20),np.zeros(20))


def test_em_fixed_point_posterior_consistency():
    p=np.array([.7,.3]);pred=np.r_[np.ones(620),np.zeros(380)]
    l1=np.where(pred,.8,.2);l0=np.where(pred,.2,.8)
    post=.3*l1/(.3*l1+.7*l0)
    o=H.em_label_shift(np.c_[1-post,post],p)
    assert o['converged'] and o['residual']<1e-12
    assert o['q'][1]==pytest.approx(.7,abs=1e-9)
    np.testing.assert_allclose(o['posterior'].mean(0),o['q'],atol=1e-12)


def test_mmd_signed_u_statistic_and_degenerate_null():
    X=np.array([[0.],[1.],[2.]])
    assert H.mmd2(X,X)<0  # Independent-pair U statistic may be negative.
    o=H.mmd_test(np.ones((4,2)),np.ones((5,2)),np.random.default_rng(605),30)
    assert o['mmd2']==0 and o['p']==1


def test_classifier_randomization_enumerates_fixed_balanced_labels():
    prediction=np.array([1,1,0,0,0,0]);left=prediction[:3];right=prediction[3:]
    o=H.classifier_holdout_test(left,right)
    choices=list(itertools.combinations(range(6),3))
    exact=np.mean([prediction[list(c)].sum()>=left.sum() for c in choices])
    assert o['p_acc']==pytest.approx(exact)
    assert o['acc']==5/6


def test_quantile_interval_binomial_coverage():
    n=400;q=.99;lo,hi=H.quantile_interval(np.arange(n),q)
    # Rank boundaries are determined by Binomial(n,q), not Gaussian quantile SE.
    k=int(lo)+1;l=int(hi)+1
    assert stats.binom.cdf(l-1,n,q)-stats.binom.cdf(k-1,n,q)>=.95
