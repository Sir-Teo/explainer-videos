"""Independent numerical references for Part 47's asymptotic examples."""
import itertools
import math

import mpmath as mp
import numpy as np
from numpy.testing import assert_allclose
from scipy import integrate, stats

from videos.stats.stats47 import compute as C


def test_hodges_risk_retains_extremely_small_positive_tail():
    n=10000;t=n**.25
    exact=2*(t*stats.norm.pdf(t)+stats.norm.sf(t))
    assert 0<C.hodges_risk(0,n)<1e-19
    assert_allclose(C.hodges_risk(0,n),exact,rtol=1e-12)
    for theta in (.01,.1,.3,1.):
        n=100;threshold=n**-.25
        expected=integrate.quad(lambda z:((0 if abs(theta+z/math.sqrt(n))<threshold else theta+z/math.sqrt(n))-theta)**2*n*stats.norm.pdf(z),-12,12,points=[math.sqrt(n)*(-threshold-theta),math.sqrt(n)*(threshold-theta)],epsabs=1e-11)[0]
        assert_allclose(C.hodges_risk(theta,n),expected,rtol=1e-9)


def test_small_local_radius_does_not_obey_a_unit_minimax_bound():
    h=np.linspace(-.5,.5,1001)
    assert C.hodges_local(h,10**8).max()<.251
    assert_allclose(C.hodges_local([1,2,4,8],10**8),[1,4,16,64])


def test_signed_rank_walsh_identity_and_exact_projection():
    g=np.random.default_rng(471700);n=16;x=g.normal(size=(90000,n))
    ranks=stats.rankdata(abs(x),axis=1)
    W=np.sum(ranks*(x>0),axis=1)
    i,j=np.triu_indices(n)
    assert_allclose(W[:100],np.sum(x[:100,i]+x[:100,j]>0,axis=1))
    projected=C.signed_rank_projection(x)
    theory=n*(n*n+n+1)/12
    assert abs(projected.var()-theory)<.02*theory
    assert abs(np.mean((W-projected)**2)-n*(n-1)/24)<.04*n*(n-1)/24
    # A first-order projection is orthogonal to its remainder.
    assert abs(np.cov(W-projected,projected)[0,1])<.01*theory


def test_conditional_bootstrap_max_cdf_matches_enumeration():
    x=np.array([.1,.3,.55,.6,.9]);n=len(x);k=3;M=x[-1]
    all_max=np.array([max(v) for v in itertools.product(x,repeat=k)])
    exact_gaps=k*(M-all_max)/M
    expected_ks=stats.kstest(exact_gaps,stats.expon.cdf).statistic
    r=C.uniform_max_bootstrap(n,100000,np.random.default_rng(471701),m=k,sample=x)
    assert_allclose(r['ks_exp'],expected_ks,atol=1e-14)
    assert_allclose(r['theory_atom'],1-(1-1/n)**k,rtol=1e-14)
    assert abs(r['atom0']-r['theory_atom'])<.005


def test_m_out_of_n_atom_uses_resample_size():
    n=2000;x=np.linspace(1/n,1,n)
    g=np.random.default_rng(471702)
    regular=C.uniform_max_bootstrap(n,80000,g,sample=x)
    smaller=C.uniform_max_bootstrap(n,80000,g,m=40,sample=x)
    assert regular['theory_atom']>.63
    assert smaller['theory_atom']<.02
    assert smaller['ks_exp']<regular['ks_exp']/10


def test_lugannani_rice_mean_limit_is_continuous_and_stable():
    mp.mp.dps=65;n=5
    for delta in (-.1,-1e-5,-1e-8,0,1e-8,1e-5,.1):
        if delta==0:
            exact=mp.mpf('.5')-1/(3*mp.sqrt(2*mp.pi*n))
        else:
            d=mp.mpf(str(delta));w=mp.sign(d)*mp.sqrt(2*n*(d-mp.log1p(d)));u=mp.sqrt(n)*d
            exact=mp.erfc(w/mp.sqrt(2))/2+mp.exp(-w*w/2)/mp.sqrt(2*mp.pi)*(1/u-1/w)
        assert_allclose(C.lugannani_rice(1+delta,n)['lr'],float(exact),atol=3e-12)


def test_normal_score_efficiencies_match_analytic_cases():
    assert_allclose(C.normal_scores_are('normal'),1,rtol=1e-11)
    assert_allclose(C.normal_scores_are('logistic'),math.pi/3,rtol=1e-11)
    assert_allclose(C.normal_scores_are('Laplace'),4/math.pi,rtol=1e-11)


def test_signed_rank_and_sign_efficiency_need_distinct_assumptions():
    # Symmetric bimodality can make the sign-test efficacy arbitrarily small.
    d=4.;variance=1+d*d;density0=stats.norm.pdf(d)
    assert 4*variance*density0*density0<.001
    assert_allclose(12*3*(5/(4*math.sqrt(3)*math.pi))**2,75/(4*math.pi**2))


def test_order_statistic_interval_probability_is_binomial():
    exact=stats.binom.cdf(14,20,.5)-stats.binom.cdf(5,20,.5)
    assert_allclose(exact,.9586105346679688)


def test_histogram_retains_mass_outside_the_display():
    h=C.histogram(np.array([-2.,0.,.2,.8,1.,3.]),np.array([0.,.5,1.]))
    assert_allclose(h,[2/3,2/3])
    assert_allclose(np.sum(h*.5),4/6)
