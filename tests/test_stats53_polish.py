"""Independent checks for the Bayesian experiments and numerical claims in Part 53."""
import math
import numpy as np
import pytest
from scipy import integrate,stats
from videos.stats.stats53 import compute as C
from explainer.stats.kit import bnp as B


def test_boundary_normal_tv_is_one_against_continuous_beta():
    assert C.bvm_tv_beta(0,10)==1
    assert C.bvm_tv_beta(10,10)==1
    # A continuous posterior assigns probability zero to the degenerate-normal singleton.
    assert stats.beta(1,11).cdf(0)==0


def test_interior_beta_normal_tv_by_independent_dense_integration():
    n,k=80,23;p=k/n;sd=math.sqrt(p*(1-p)/n)
    x=np.linspace(-.1,1.1,200001)
    want=.5*np.trapezoid(abs(stats.beta.pdf(x,k+1,n-k+1)-stats.norm.pdf(x,p,sd)),x)
    assert C.bvm_tv_beta(k,n)==pytest.approx(want,abs=2e-8)


def test_selected_alpha_risk_differs_from_frozen_weight_surrogate():
    # For coordinate 2, choose the rough prior exactly when its observed noise is large.
    n=10;c=1.5;r=np.random.default_rng(923);Z=r.normal(size=(120000,2));Y=Z/math.sqrt(n)
    alpha=np.where(abs(Z[:,1])>c,.5,3.)
    lam=np.column_stack([np.ones(len(alpha)),2.**(-1-2*alpha)])
    loss=C.posterior_mean_squared_loss(Y,np.zeros(2),n,lam)
    wh=n*2**-2/(1+n*2**-2);wl=n*2**-7/(1+n*2**-7);w1=n/(1+n)
    tail_second=2*(c*stats.norm.pdf(c)+stats.norm.sf(c))
    exact=(w1*w1+wh*wh*tail_second+wl*wl*(1-tail_second))/n
    frozen=(w1*w1+wh*wh*2*stats.norm.sf(c)+wl*wl*(1-2*stats.norm.sf(c)))/n
    assert abs(loss.mean()-exact)<5*loss.std(ddof=1)/math.sqrt(len(loss))
    assert exact>1.2*frozen


def test_growing_gap_truth_has_empty_fixed_ratio_windows_and_future_energy():
    th=C.inconvenient_truth(10000,1.)
    # N_j:1,4,64,4096. A rho=8 window after the previous block misses the next one.
    N=128;rho=8
    assert not np.any(th[N-1:rho*N])
    assert np.any(th[rho*N:])
    assert 2**(4*5)/2**(3*4)>2**(3*4)/2**(2*3) # gap ratio grows


def test_hyperrectangle_regular_truth_is_not_at_sobolev_boundary():
    k=np.arange(1,100001);th=B.sobolev_truth(len(k),1.)
    assert np.max(abs(th)*k**1.5)<=1
    energy=k*k*th*th
    # The positive energy added on each multiplicative block does not vanish.
    assert energy[9999:99999].sum()>1


def test_reference_radius_matches_one_dimensional_chisquare():
    ref=C.credible_radii(20,1,[1.],reps=30000)
    exact=stats.chi2.ppf(.95,1)/21
    assert abs(ref['q'][0]/exact-1)<.04
    assert ref['lo'][0]<=ref['q'][0]<=ref['hi'][0]
    lo,hi=ref['order_statistic_indices']
    assert stats.binom.cdf(hi-1,30000,.95)-stats.binom.cdf(lo-1,30000,.95)>=.95-1e-12


def test_empirical_mcse_respects_dataset_level_dependence():
    fractions=np.array([0.,1.]*30)
    got=C.empirical_mcse(fractions)
    pooled=math.sqrt(.25/(60*10))
    assert got>3*pooled
    assert got==pytest.approx(np.std(fractions,ddof=1)/math.sqrt(60))


@pytest.mark.parametrize('mean',[-100.,0.,100.])
def test_spike_slab_atom_is_not_lost_outside_slab_bracket(mean):
    assert C.spike_slab_interval(.001,mean,1)==(0.,0.)


def test_spike_slab_quantiles_include_jump_and_normal_limits():
    lo,hi=C.spike_slab_interval(1.,3.,2.)
    assert (lo,hi)==pytest.approx(stats.norm.ppf([.025,.975],3,math.sqrt(2)))
    assert C.spike_slab_interval(0.,100,1)==(0.,0.)
    assert C.spike_slab_interval(.5,2,1)[0]==0


@pytest.mark.parametrize('y',[0.,2.5,6.,10.])
def test_horseshoe_gaussian_mixture_quantiles_against_adaptive_integral(y):
    tau=.1
    density=lambda u:math.exp(-.5*(1-u*u)*y*y)/(tau*tau+(1-tau*tau)*u*u)
    normalizer=integrate.quad(density,0,1,epsabs=1e-12)[0]
    mean=integrate.quad(lambda u:u*u*y*density(u),0,1,epsabs=1e-12)[0]/normalizer
    fit=C.horseshoe_posterior(y,tau)
    assert fit['mean']==pytest.approx(mean,abs=1e-9)
    for bound,want in [(fit['lo'],.025),(fit['hi'],.975)]:
        val=integrate.quad(lambda u:stats.norm.cdf((bound-u*u*y)/u)*density(u),0,1,epsabs=1e-12)[0]/normalizer
        assert val==pytest.approx(want,abs=1e-8)
