"""Mathematical checks for the revised Part 64 experiments."""
import math
import numpy as np
import pytest
from scipy import special,stats
from videos.stats.stats64 import checked as E
from videos.stats.stats64 import compute as C


def test_logistic_normal_truth_quadrature_special_cases():
    q=E.clustered_truth(.8,0,10,100)
    assert q['mean']==pytest.approx(.8,abs=1e-12)
    assert q['icc']==pytest.approx(0,abs=1e-12)
    assert q['sd']==pytest.approx(np.sqrt(.16/1000))
    assert E.clustered_truth(.5,1.2,10,100)['mean']==pytest.approx(.5)


def test_constructed_table_and_truth_gap():
    d=C.compute_leaderboard()
    assert d['acc_a']==.852 and d['acc_b']==.847
    assert d['mcnemar']['n10']==76 and d['mcnemar']['n01']==71
    assert d['ties']>0
    assert d['flip_mcse']>0


def test_two_model_bradley_terry_analytic_solution():
    i=np.ones(100,dtype=int);j=np.zeros(100,dtype=int);y=np.r_[np.ones(70),np.zeros(30)]
    f=E.bt_fit(i,j,y,2)
    assert f['theta'][1]==pytest.approx(np.log(7/3),abs=1e-9)
    assert f['se'][1]**2==pytest.approx(1/(100*.7*.3))
    assert f['score_max']<1e-7


def test_bradley_terry_covariance_reparameterization():
    r=np.random.default_rng(8);d=E.simulate_battles([0,.2,.6],2000,r)
    a=E.bt_fit(d['i'],d['j'],d['y'],3);b=E.bt_fit(d['i'],d['j'],d['y'],3,ref=1)
    assert np.allclose(a['theta']-a['theta'][1],b['theta'])
    c=np.array([0,-1,1]);assert c@a['cov_sandwich']@c==pytest.approx(c@b['cov_sandwich']@c)


def test_bradley_terry_disconnected_and_separated_fail():
    with pytest.raises(ValueError):E.bt_fit([0,0],[1,1],[0,1],3)
    with pytest.raises((ValueError,RuntimeError)):E.bt_fit([0]*30,[1]*30,[1]*30,2)


def test_simultaneous_rank_set_shift_and_covariance():
    f=np.array([0,.2,1.]);V=np.eye(3)*.0001
    assert E.rank_one_set(f,V)==[2]
    assert E.rank_one_set(f+7,V+np.ones((3,3))*3)==[2]
    assert E.rank_one_set(f,np.eye(3)*4)==[0,1,2]


def test_regularized_irt_checked_local_fit():
    r=np.random.default_rng(4);th=np.linspace(-2,2,30);a=r.uniform(.5,2,40);b=r.normal(size=40)
    R=(r.random((30,40))<special.expit(a*(th[:,None]-b))).astype(float)
    f=E.fit_2pl(R,iters=10)
    assert f['projected_score']<2e-3 and np.isfinite(f['objective'])
    assert abs(f['theta'].mean())<1e-12 and f['theta'].std()==pytest.approx(1)
    assert np.corrcoef(th,f['theta'])[0,1]>.85


def test_collapse_generation_index_and_mean():
    d=E.gaussian_collapse(20,5,6000,np.random.default_rng(1))
    assert np.array_equal(d['paths'][:,0],np.ones(6000))
    assert d['paths'][:,1].mean()==pytest.approx(.95,abs=.015)
    assert d['paths'][:,5].mean()==pytest.approx(.95**5,abs=.02)
    assert d['drift']==pytest.approx(special.digamma(19/2)+np.log(2/20))


def test_accumulation_and_replacement_same_initial_moments():
    a=E.gaussian_collapse(20,2,3,np.random.default_rng(3),accumulate=True)
    assert np.array_equal(a['paths'][:,0],np.ones(3))
    assert np.all(a['paths']>0)


def test_watermark_strict_rejection_at_lattice_boundary():
    T,g,z=4,.5,0
    assert E.watermark_power(T,g,0,z)==pytest.approx(stats.binom.sf(2,4,.5))
    assert E.watermark_power(20,.25,2,4,edit_frac=1)==pytest.approx(stats.binom.sf(math.floor(5+4*np.sqrt(3.75)),20,.25))


def test_factuality_ties_empty_responses_and_infinite_threshold():
    d=E.conformal_factuality([[1.],[1.]],[[False],[False]],[[1.,2.]],.5)
    assert d['kept']==[[False,True]]
    e=E.conformal_factuality([[1.]],[[False]],[[100.]],.01)
    assert np.isinf(e['threshold']) and e['kept']==[[False]]


def test_probability_flow_exact_gaussian_initial_marginal():
    z=np.linspace(-3,3,101);sig=np.geomspace(8,.01,400)
    x=E.probability_flow(lambda y,s:-y/(1+s*s),sig,len(z),np.random.default_rng(1),initial=z*np.sqrt(65))
    assert np.max(abs(x-z*np.sqrt(1+.01**2)))<.0005


def test_probability_flow_rejects_invalid_grids():
    with pytest.raises(ValueError):E.probability_flow(lambda y,s:-y,[1,2],3,np.random.default_rng(1))


def test_paired_sbi_exact_conjugate_reference():
    d=E.sbi_comparison(400,8,.9,10000,np.random.default_rng(5))
    assert abs(d['exact']-.9)<.015
    assert all(0<=v<=1 for v in d.values())


def test_mixture_score_finite_difference_and_tweedie():
    y=np.linspace(-3,3,30);mus=np.array([-2,1.5]);w=np.array([.4,.6]);sig=.7;sd=.5
    logpdf=lambda x:np.log(sum(ww*stats.norm.pdf(x,mu,np.sqrt(sig*sig+sd*sd)) for mu,ww in zip(mus,w)))
    assert np.allclose(E.mixture_score(y,sig,mus,sd,w),(logpdf(y+1e-5)-logpdf(y-1e-5))/2e-5,atol=1e-7)


def test_ppi_variance_requires_independent_samples():
    y=np.array([0.,1,1,0]);f=np.array([.1,.8,.6,.3]);u=np.array([.2,.4,.9])
    d=E.ppi_mean_ci(y,f,u)
    assert d['est']==pytest.approx(u.mean()+(y-f).mean())
    assert d['se']**2==pytest.approx(u.var(ddof=1)/3+(y-f).var(ddof=1)/4)
