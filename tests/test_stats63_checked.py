"""Checks of privacy calibration, release scope and the causal toy."""
import itertools
import math
import numpy as np
import pytest
from scipy import stats
from videos.stats.stats63 import checked as P
from videos.stats.stats63 import compute as C


def test_gaussian_delta_stable_and_exact():
    for eps in [0.,1.,20.,1000.]:
        d=P.gaussian_delta(5,1,eps)
        assert 0<=d<=1
    assert P.gaussian_delta(1,0,2)==0
    s=P.gaussian_sigma_analytic(1,1,1e-5)
    assert P.gaussian_delta(s,1,1)==pytest.approx(1e-5,abs=1e-12)


def test_continuous_rdp_optimum_equals_zcdp_conversion():
    rho=20;delta=1e-5
    alpha=1+np.sqrt(np.log(1/delta)/rho)
    assert P.rdp_gaussian_eps(1,5,1000,delta)==pytest.approx(rho*alpha+np.log(1/delta)/(alpha-1))


def test_replace_one_clipped_gradient_sensitivity():
    # Opposite labels at w=0 attain 2C with a large identical covariate.
    X=np.array([[10.],[10.]])
    grads=(.5-np.array([0.,1.]))[:,None]*X
    grads/=np.maximum(1,np.linalg.norm(grads,axis=1))[:,None]
    assert np.linalg.norm(grads[0]-grads[1])==2
    o=P.dp_logistic_gd(np.ones((3,1)),[0,1,0],.1,10,1,1,np.random.default_rng(1))
    assert o['sensitivity']==2
    assert 10*o['sensitivity']**2/(2*o['sigma']**2)==pytest.approx(.1)


def test_feature_transform_does_not_depend_on_other_records():
    x=np.arange(30)[None,:].astype(float)
    assert np.array_equal(P.fixed_features(x)[0],P.fixed_features(np.vstack([x,np.ones((1,30))*1e9]))[0])
    assert np.max(abs(P.fixed_features(x)))<=1


def test_integer_projection_matches_brute_force_optimum():
    for v in [np.array([-3.,1.,5.]),np.array([.4,.4,.4]),np.array([2.,2.,2.])]:
        out=P.integer_total_projection(v,4)
        opt=min(sum((np.array(c)-v)**2) for c in itertools.product(range(5),repeat=3) if sum(c)==4)
        assert sum((out-v)**2)==pytest.approx(opt)
        assert out.sum()==4 and min(out)>=0


def test_zero_integer_projection_and_invalid_total():
    assert np.array_equal(P.integer_total_projection([-5,2],0),[0,0])
    with pytest.raises(ValueError):P.integer_total_projection([1,2],1.2)


def test_private_interval_raw_center_with_clipped_variance_only():
    class Noise:
        def laplace(self,*args):return -20.
    o=P.private_proportion([0]*10,.1,Noise())
    assert o['p']==-2
    assert sum(o['aware'])/2==pytest.approx(-2)
    assert (o['aware'][1]-o['aware'][0])/2==pytest.approx(stats.norm.ppf(.975)*np.sqrt(2))


def test_exact_local_mse_and_simulation_mc_error():
    o=P.mean_mse_central_local(100,1,100000,np.random.default_rng(8))
    assert abs(o['central']-(.21/100+2/100**2))<5*o['central_mcse']
    assert abs(o['local']-o['local_exact'])<5*o['local_mcse']


def test_census_integer_totals_and_bias_conservation():
    d=C.compute_census()
    assert d['max_total_error']==0 and d['neg_post']==0
    assert sum(r['n']*r['bias_post'] for r in d['rows'])==pytest.approx(0,abs=1e-10)


def test_counterfactual_invariance_on_independent_evaluation():
    d=C.compute_cfair()
    assert d['n_train']==10000 and d['n']==20000
    assert d['residual']['counterfactual_max_change']<1e-14
    assert d['priors']['counterfactual_mean_change']>.05


def test_multicalibration_patch_replay_and_cell_scope():
    pred=np.array([.2]*100+[.8]*100); y=np.array([1]*100+[0]*100); groups=[np.ones(200,dtype=bool)]
    m=P.multicalibrate(pred,y,groups,alpha=.02,min_n=20,n_bins=5)
    assert np.allclose(m['pred'],P.apply_patches(pred,groups,m['patches'],5))
    assert P.max_calibration_gap(m['pred'],y,groups,5,20)<=.02


def test_fairness_identity_all_nonzero_cells():
    y=np.array([0,0,0,1,1,1]);scores=np.array([1,0,0,1,1,0]);g=np.array(['a']*6)
    r=P.group_rates(scores,y,g,.5)['a']
    assert P.chouldechova_fpr(r['base'],r['ppv'],r['fnr'])==pytest.approx(r['fpr'])
    # PPV=1 does not imply perfect classification: false negatives may remain.
    assert P.chouldechova_fpr(.5,1,.5)==0


def test_gaussian_testing_tradeoff_matches_power():
    assert 1-P.tradeoff_gaussian(np.array([.05]),np.sqrt(2*2.63))[0]==pytest.approx(stats.norm.cdf(np.sqrt(5.26)-stats.norm.ppf(.95)))


def test_risk_crossover_balances_terms():
    d,eps,delta=1000,1,1e-5;n=d*np.log(1/delta)/eps**2
    assert d/n==pytest.approx(d*d*np.log(1/delta)/(n*n*eps*eps))
