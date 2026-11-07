"""Identification, assignment-support and sample-independence checks for Part 62."""
import itertools
import numpy as np
import pytest
from scipy import special
from videos.stats.stats62 import checked as F


def test_frontdoor_cells_and_missing_support():
    a=np.array([0,0,1,1]);m=np.array([0,1,0,1]);y=2*m+1
    o=F.front_door(y,a,m)
    assert o['ate']==0 and np.all(o['cells']==1)
    with pytest.raises(ValueError):F.front_door([1,2],[0,1],[0,1])


def test_relaxed_weight_box_against_all_vertices():
    y=np.array([1.,5,2,8]);t=np.array([0,0,1,1]);ps=np.array([.2,.4,.6,.8])
    oldwidth=0
    for lam in [1,1.5,3]:
        o=F.msm_bounds(y,t,ps,lam);limits={}
        for arm in (0,1):
            values=y[t==arm];e=(ps if arm else 1-ps)[t==arm]
            lo=1+(1/e-1)/lam;hi=1+(1/e-1)*lam
            means=[]
            for bits in itertools.product([False,True],repeat=len(values)):
                w=np.where(bits,hi,lo);means.append(w@values/w.sum())
            limits[arm]=(min(means),max(means))
        assert o['ate_lo']==pytest.approx(limits[1][0]-limits[0][1])
        assert o['ate_hi']==pytest.approx(limits[1][1]-limits[0][0])
        width=o['ate_hi']-o['ate_lo'];assert width>=oldwidth;oldwidth=width
    with pytest.raises(ValueError):F.msm_bounds(y,t,ps,.5)


def test_tsls_identified_moments_and_hc1():
    r=np.random.default_rng(621);n=800;z=r.normal(size=n);u=r.normal(size=n)
    X=np.c_[np.ones(n),z+u];Z=np.c_[np.ones(n),z];y=1+2*X[:,1]+3*u+r.normal(size=n)
    o=F.tsls(y,X,Z);expected=np.linalg.solve(Z.T@X,Z.T@y)
    np.testing.assert_allclose(o['b'],expected,atol=1e-12)
    A=np.linalg.inv(Z.T@X);res=y-X@expected
    variance=A@((Z*res[:,None]**2).T@Z)@A.T*n/(n-2)
    np.testing.assert_allclose(o['V'],variance,atol=1e-12)
    with pytest.raises(ValueError):F.tsls(y,X,np.ones((n,1)))


def test_proximal_first_stage_and_large_sample_effect():
    r=np.random.default_rng(622);n=12000;u=r.normal(size=n);z=u+r.normal(size=n);w=u+r.normal(size=n)
    a=(u+r.normal(size=n)>0).astype(float);y=a+2*u+r.normal(size=n)
    o=F.proximal_2sls(y,a,z,w)
    assert abs(o['effect']-1)<3*o['se']
    assert o['first_stage_robust_f']>100 and 0<o['first_stage_partial_r2']<1


def test_exact_exposure_probabilities_including_isolates():
    adj=np.array([[0,1,0],[1,0,0],[0,0,0]]);p=.3;enumerated=np.zeros((3,4))
    for z in itertools.product([0,1],repeat=3):
        z=np.array(z);prob=p**z.sum()*(1-p)**(3-z.sum())
        enumerated[np.arange(3),F.exposures(z,adj)]+=prob
    pi=F.exposure_probs(adj,p)
    np.testing.assert_allclose(pi,enumerated,atol=1e-15)
    np.testing.assert_allclose(pi[2],[.7,0,.3,0])


def test_spillover_hajek_uses_common_eligible_population():
    adj=np.zeros((5,5),int);adj[0,1]=adj[1,0]=adj[2,3]=adj[3,2]=1
    z=np.array([0,1,0,0,0]);baseline=np.array([0,0,0,0,100.])
    y=baseline+2*z+((adj@z)>0)
    o=F.exposure_hajek(y,z,adj,F.exposure_probs(adj,.3))
    assert o['eligible']['spill']==4
    assert o['spill']==pytest.approx(1)


def test_global_exposure_ht_unbiased_by_assignment_enumeration():
    adj=np.array([[0,1,0],[1,0,0],[0,0,0]]);p=.3;pi=F.exposure_probs(adj,p);target=np.array([3,3,2])
    expected=0.
    for z in itertools.product([0,1],repeat=3):
        z=np.array(z);e=F.exposures(z,adj);y=np.array([1,3,7])+2*z+((adj@z)>0)
        probability=p**z.sum()*(1-p)**(3-z.sum())
        expected+=probability*F.exposure_ht_contrast(y,e,pi,target)
    assert expected==pytest.approx(3-1/3)
    with pytest.raises(ValueError):F.exposure_ht_contrast(y,e,pi,np.array([3,3,3]))


def test_threshold_optimizer_handles_ties_and_constant_rules():
    x=np.array([0,0,1,2,2.]);g=np.array([10,-20,5,2,-1.])
    rule=F.ewm_threshold(x,g)
    candidates=[dict(c=c,s=s) for c in list(np.unique(x))+[np.inf] for s in [-1,1]]
    exact=max(F.policy_value(g,F.apply_rule(x,r)) for r in candidates)
    assert rule['value']==pytest.approx(exact)
    assert F.policy_value(g,F.apply_rule(x,rule))==pytest.approx(exact)
    none=F.ewm_threshold(x,-np.ones(5),directions=(1,))
    assert none['value']==0 and not F.apply_rule(x,none).any()


def test_exact_uniform_policy_gain():
    assert F.uniform_policy_gain(dict(c=.4,s=1))==pytest.approx(.0225)
    assert F.uniform_policy_gain(dict(c=np.inf,s=1))==0
    assert F.uniform_policy_gain(dict(c=np.inf,s=-1))==pytest.approx(-.1)
    for c in [-1,-.3,.4,1]:
        assert F.uniform_policy_gain(dict(c=c,s=1))+F.uniform_policy_gain(dict(c=c,s=-1))==pytest.approx(-.1)


def test_full_history_q_learning_keeps_first_stage_reward():
    r=np.random.default_rng(623);n=12000;x1=r.normal(size=n);a1=r.integers(2,size=n);x2=r.normal(size=n);a2=r.integers(2,size=n)
    y=x2+a2*(x2-.2)+3*a1*x1+r.normal(size=n)
    q=F.q_learning(x1,a1,x2,a2,y)
    assert q['b1'][3]==pytest.approx(3,abs=.08)
    assert -q['b2'][5]/q['b2'][6]==pytest.approx(.2,abs=.08)
    assert q['rule1'](np.array([-1.,1.])).tolist()==[False,True]


def test_pc_stable_skeleton_and_column_permutation():
    r=np.random.default_rng(624);n=6000;x0=r.normal(size=n);x1=x0+r.normal(size=n);x2=x1+r.normal(size=n);x3=r.normal(size=n)
    X=np.c_[x0,x1,x2,x3];o=F.pc_skeleton(X,.001)
    expected=np.zeros((4,4),bool);expected[0,1]=expected[1,0]=expected[1,2]=expected[2,1]=True
    np.testing.assert_array_equal(o['adj'],expected)
    order=np.array([3,2,0,1]);p=F.pc_skeleton(X[:,order],.001)
    np.testing.assert_array_equal(p['adj'],expected[np.ix_(order,order)])
    assert not o['truncated']


def test_varsortability_path_lengths_and_numerical_ties():
    B=np.array([[0,1,1],[0,0,1],[0,0,0]])
    base=np.array([-1.,1.]);X=np.column_stack([base,base*np.sqrt(3),base*np.sqrt(2)])
    assert F.varsortability(X,B)==pytest.approx(.75)
    assert F.varsortability(X/X.std(0),B)==.5


def test_surrogate_index_includes_independent_fit_uncertainty():
    r=np.random.default_rng(625);So=r.normal(size=(100,2));Yo=So@np.array([2.,1.])+r.normal(size=100)*3
    t=np.repeat([0,1],300);Se=r.normal(size=(600,2))+t[:,None]
    o=F.surrogate_index(So,Yo,Se,t)
    assert o['index_fit_variance']>0
    assert o['se']**2==pytest.approx(o['trial_variance']+o['index_fit_variance'])
    assert o['se']>np.sqrt(o['trial_variance'])


def test_checked_logistic_fit():
    r=np.random.default_rng(626);X=r.normal(size=(1000,2));t=(r.random(1000)<special.expit(X@np.array([.4,-.7]))).astype(int)
    p,residual=F.propensity(X,t)
    assert residual<1e-8 and np.all((p>0)&(p<1))
