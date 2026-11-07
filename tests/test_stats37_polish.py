"""Independent references for exact IV inversion and trend/bounds uncertainty."""
import numpy as np
import pytest
from scipy import optimize, stats
from explainer.stats.kit import quasi as Q
from videos.stats.stats37 import compute as C


@pytest.mark.parametrize('seed,strength',[(1,.02),(2,.02),(3,.02),(4,.5),(5,.5)])
def test_matrix_free_ar_agrees_with_independent_f_tests_and_dense_inversion(seed,strength):
    g=np.random.default_rng(seed);n=150
    Z=g.normal(size=(n,2));X=g.normal(size=(n,2));u=g.normal(size=n)
    d=strength*Z[:,0]+u+g.normal(size=n);y=.7*d+u
    grid=np.linspace(-10,10,21)
    result=C.matrix_free_ar_set(y,d,Z,X,grid=grid)
    ref=Q.ar_set(y,d,Z,X)
    assert result['kind']==ref['kind']
    if ref['lo'] is not None:
        np.testing.assert_allclose([result['lo'],result['hi']],[ref['lo'],ref['hi']],atol=1e-9)
    for b,p in zip(grid,result['p']):
        assert p==pytest.approx(Q.anderson_rubin(y,d,Z,X,b)['p'],abs=1e-12)
        assert Q.ar_covers(result,b)==(p>=.1)


def test_matrix_free_ar_handles_zero_first_stage_and_large_sample():
    g=np.random.default_rng(637);n=20000
    z=g.normal(size=n);y=g.normal(size=n)
    # A dense n-by-n projection would need 3.2 GB for this trivial set.
    result=C.matrix_free_ar_set(y,np.zeros(n),z)
    expected='line' if Q.anderson_rubin(y,np.zeros(n),z)['p']>=.1 else 'empty'
    assert result['kind']==expected


def test_joint_trend_interval_has_correct_gaussian_sampling_scale():
    e=np.arange(-5,2);k=len(e);V=.02*(np.eye(k)+np.ones((k,k)))
    # All coefficients share a reference mean; its normalized coefficient is zero.
    ref=np.flatnonzero(e==-1)[0];V[ref]=0;V[:,ref]=0
    truth=.2*(e+1)+(e>=0)*1.
    g=np.random.default_rng(638);draws=g.multivariate_normal(truth,V,size=4000)
    covered=[];centers=[]
    for b in draws:
        r=C.trend_sensitivity(e,b,V,0.)
        covered.append(r['ci'][0]<=1<=r['ci'][1]);centers.append(r['mid'])
    assert .88<np.mean(covered)<.92
    assert np.std(centers,ddof=1)==pytest.approx(C.trend_sensitivity(e,truth,V,0.)['se'],rel=.04)


def test_relative_bounds_account_for_pre_jump_sampling_error():
    e=np.arange(-4,1);V=.01*(np.eye(len(e))+np.ones((len(e),len(e))))
    ref=np.flatnonzero(e==-1)[0];V[ref]=0;V[:,ref]=0
    truth=.2*(e+1)+(e==0)*1.
    g=np.random.default_rng(639);covered=[]
    for b in g.multivariate_normal(truth,V,size=2000):
        r=C.relative_sensitivity(e,b,V,1.)
        assert r['pre_jump_upper']>=r['max_pre_jump']
        covered.append(r['ci'][0]<=1<=r['ci'][1])
    assert np.mean(covered)>=.89


def test_fractional_lee_bounds_agree_with_linear_programming():
    y=np.array([0.,3.,9.,20.,1.,1.,40.]);t=np.array([1,1,1,1,0,0,0],bool)
    selected=np.array([1,1,1,0,1,1,0],bool)
    r=C.fractional_lee_bounds(y,t,selected)
    mass=8/3;v=y[t & selected]
    low=optimize.linprog(v,A_eq=[np.ones(3)],b_eq=[mass],bounds=[(0,1)]*3,method='highs')
    high=optimize.linprog(-v,A_eq=[np.ones(3)],b_eq=[mass],bounds=[(0,1)]*3,method='highs')
    assert low.success and high.success
    assert r['lo']==pytest.approx(low.fun/mass-1)
    assert r['hi']==pytest.approx(-high.fun/mass-1)
    reverse=C.fractional_lee_bounds(y,~t,selected)
    assert [reverse['lo'],reverse['hi']]==pytest.approx([-r['hi'],-r['lo']])


def test_employment_truth_is_a_potential_outcome_contrast():
    d=C.load('bounds')
    g=C.rng(3710);n=4000
    g.choice(n,n//2,replace=False)
    u=g.random(n)
    assert d['truth_emp']==pytest.approx(np.mean((u>=.6)&(u<.72)))
    assert d['truth_emp']==pytest.approx(.12325)


def test_synthetic_control_prefit_filter_retains_the_same_rank_statistic():
    d=C.load('synth')
    kept=[p for p in d['placebo'] if p['pre']<=2*d['rmspe_pre']]
    assert len(kept)==d['filtered_n']==29
    assert sum(p['ratio']>=d['ratio'] for p in kept)==d['filtered_rank']==3
    assert d['filtered_p']==pytest.approx(3/29)
