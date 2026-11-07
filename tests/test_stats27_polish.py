"""Independent numerical references for Part 27's computational examples."""
import numpy as np
import pytest
from scipy import integrate, stats
from videos.stats.stats27 import compute as C
from explainer.stats.kit import ppl as P


def test_school_grid_matches_infinite_range_reference():
    h=C.schools_grid()
    reference=C.schools_reference()
    q=C.grid_quantile(h,[.05,.5,.95])
    np.testing.assert_allclose(q,[reference['q05'],reference['median'],reference['q95']],atol=2e-5)
    assert reference['tail_over80']<1e-5


def test_school_density_matches_independent_multivariate_normal_marginal():
    h=C.schools_grid()
    ratios=[]
    for tau in [0.,3.,15.]:
        expected=stats.multivariate_normal.logpdf(C.Y8,cov=np.diag(C.S8**2+tau*tau)+25*np.ones((8,8)))+stats.halfcauchy.logpdf(tau,scale=5)
        ratios.append(np.log(np.interp(tau,h.tau,h.post_tau))-expected)
    np.testing.assert_allclose(ratios,np.repeat(ratios[0],3),atol=2e-8)


def test_grid_widens_for_large_prior_predictive_scales():
    y=np.array([-1000.,700,2200,-900,400,1900,-300,1600])
    h=C.schools_grid(y,C.S8)
    assert h.tau[-1]>40_000
    q=C.grid_quantile(h,[.05,.5,.95])
    assert q[1]>500
    # A denser independent log-tau integral agrees without truncation at 80.
    def density_logtau(u):
        t=np.exp(u)
        return np.exp(stats.multivariate_normal.logpdf(y,cov=np.diag(C.S8**2+t*t)+25*np.ones((8,8)))+stats.halfcauchy.logpdf(t,scale=5)+u+80)
    norm=integrate.quad(density_logtau,-20,20,epsabs=1e-10,epsrel=1e-7)[0]
    cdf=integrate.quad(density_logtau,-20,np.log(q[1]),epsabs=1e-10,epsrel=1e-7)[0]/norm
    assert cdf==pytest.approx(.5,abs=2e-5)


def test_grid_draws_have_no_boundary_atom_and_keep_the_normal_mean_prior():
    h=C.schools_grid();g=np.random.default_rng(2726)
    d=h.draws(80_000,g)
    cdf=integrate.cumulative_trapezoid(h.post_tau,h.tau,initial=0)
    values=np.interp(d['tau'],h.tau,cdf/cdf[-1])
    assert stats.kstest(values,'uniform').pvalue>.001
    assert not np.any(d['tau']==0)
    tau=d['tau'];w=1/(C.S8**2+tau[:,None]**2);var=1/(w.sum(1)+1/25)
    z=(d['mu']-var*(w*C.Y8).sum(1))/np.sqrt(var)
    assert abs(z.mean())<.015
    assert z.std()==pytest.approx(1,abs=.015)


def test_centered_and_noncentered_densities_include_the_effect_jacobian():
    mu,tau,z=.6,2.3,np.linspace(-1,1,8)
    centered=C.schools_model(True);noncentered=C.schools_model(False)
    uc=np.r_[mu,np.log(tau),mu+tau*z]
    un=np.r_[mu,np.log(tau),z]
    assert noncentered.log_density(un)==pytest.approx(centered.log_density(uc)+8*np.log(tau),abs=1e-10)


def test_nonidentity_mass_leapfrog_is_reversible_and_preserves_energy_to_order():
    model=P.Model({'x':(2,'real')},lambda p:P.normal_lpdf(p['x'],0,np.array([.3,2.])))
    q=np.array([.2,-.5]);p=np.array([.4,1.2]);inv=np.array([.09,4.])
    lp,g=model.logp_grad(q)
    q1,p1,lp1,g1=P.leapfrog(model,q,p,g,.02,inv)
    q2,p2,_,_=P.leapfrog(model,q1,-p1,g1,.02,inv)
    np.testing.assert_allclose(q2,q,atol=1e-14);np.testing.assert_allclose(p2,-p,atol=1e-14)
    h0=-lp+.5*np.sum(inv*p*p);h1=-lp1+.5*np.sum(inv*p1*p1)
    assert abs(h1-h0)<1e-5


def test_importance_tail_standard_error_has_an_analytic_reference():
    d=C.load('importance')['tail'];a,mu,n=3.,3.15,2000
    ordinary=np.sqrt(stats.norm.sf(a)*(1-stats.norm.sf(a))/n)
    shifted=np.sqrt((np.exp(mu*mu)*stats.norm.sf(a+mu)-stats.norm.sf(a)**2)/n)
    assert d['sd_naive']==pytest.approx(ordinary,rel=.2)
    assert d['sd_is']==pytest.approx(shifted,rel=.2)
    assert 10<ordinary/shifted<20


def test_fixed_gaussian_mean_field_optimum_uses_precision_diagonals():
    rho=.9;precision=np.linalg.inv([[1.,rho],[rho,1.]])
    sd=1/np.sqrt(np.diag(precision))
    np.testing.assert_allclose(sd,np.sqrt(1-rho*rho))
    # The finite stochastic optimizer in the film is an approximation to this optimum.
    assert .43<sd[0]<.44


def test_cftp_small_ising_marginal_matches_enumerated_distribution():
    g=np.random.default_rng(2727);beta=.25
    states=np.array([[(mask>>j)&1 for j in range(4)] for mask in range(16)])*2-1
    states=states.reshape(-1,2,2)
    energy=np.sum(states*(np.roll(states,1,axis=1)+np.roll(states,1,axis=2)),axis=(1,2))
    weights=np.exp(beta*energy);weights/=weights.sum()
    exact=float(weights@((states.mean(axis=(1,2)))**2))
    values=[]
    for _ in range(1500):
        out=P.cftp_ising(2,beta,g)
        assert out['mags'][-1,0]==out['mags'][-1,1]
        values.append(out['state'].mean()**2)
    error=np.std(values,ddof=1)/np.sqrt(len(values))
    assert abs(np.mean(values)-exact)<4*error


def test_interrupted_coverage_simulation_resumes_the_identical_random_stream(tmp_path,monkeypatch):
    from explainer.ai.cache import Cache
    cache=Cache('test-stats27-resume');cache.dir=tmp_path/'reference'
    monkeypatch.setattr(C,'CACHE',cache)
    monkeypatch.setattr(C,'save_rows',lambda *args:None)
    reference=C.compute_board(reps=2)
    cache.dir=tmp_path/'interrupted'
    original=C.P.sample;calls=0
    def interrupted(*args,**kwargs):
        nonlocal calls
        calls+=1
        if calls==3:raise RuntimeError('simulated interruption after the first completed dataset')
        return original(*args,**kwargs)
    monkeypatch.setattr(C.P,'sample',interrupted)
    with pytest.raises(RuntimeError,match='simulated interruption'):
        C.compute_board(reps=2)
    monkeypatch.setattr(C.P,'sample',original)
    resumed=C.compute_board(reps=2)
    assert resumed==reference
