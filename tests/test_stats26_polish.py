"""Numerical references for the Bayesian analysis in Part 26."""
import numpy as np
import pytest
from scipy import integrate, special, stats
from videos.stats.stats26 import compute as C

Y=np.array([28.,8,-3,7,-1,1,18,12])
S=np.array([15.,10,16,11,9,11,10,18])


def test_three_school_posterior_keeps_the_large_omitted_tail():
    h=C.hier_normal(Y[:3],S[:3])
    ref=C.tau_reference(Y[:3],S[:3])
    cdf=integrate.cumulative_trapezoid(h.post_tau,h.tau,initial=0)
    median=np.interp(.5,cdf/cdf[-1],h.tau)
    assert median==pytest.approx(ref["median"],abs=.002)
    assert 22<median<24
    assert .32<ref["tail_over40"]<.34
    assert ref["tail_over_grid"]<1.5e-5


def test_infinite_range_reference_matches_independent_mean_integral():
    # At finite tau, directly integrate mu, instead of completing the square.
    ratios=[]
    for tau in [1.,8.,25.]:
        v=S[:3]**2+tau**2
        exact=integrate.quad(lambda m:np.prod(stats.norm.pdf(Y[:3],m,np.sqrt(v))),-np.inf,np.inf,
                             epsabs=1e-13,epsrel=1e-9)[0]
        ratios.append(np.log(exact)-C.tau_kernel(tau,Y[:3],S[:3]))
    np.testing.assert_allclose(ratios,np.repeat(ratios[0],3),atol=1e-8)


def test_grid_draws_follow_the_numerical_cdf_without_endpoint_atoms():
    h=C.hier_normal(Y,S)
    draws=h.draws(100_000,np.random.default_rng(126))
    cdf=integrate.cumulative_trapezoid(h.post_tau,h.tau,initial=0)
    values=np.interp(draws["tau"],h.tau,cdf/cdf[-1])
    assert stats.kstest(values,"uniform").pvalue>.001
    assert not np.any(draws["tau"]==0)
    assert draws["theta"].shape==(100_000,8)


def test_invalid_or_improper_grid_inputs_are_explicit():
    with pytest.raises(ValueError):C.hier_normal(Y,S,[0,2,1])
    with pytest.raises(ValueError):C.hier_normal(Y,-S,[0,1])
    with pytest.raises(ValueError):C.tau_reference(Y[:2],S[:2])


def test_information_value_matches_independently_integrated_normal_case():
    mean,var,cost,se=1.3,4.2,2.,1.7
    actual=C.normal_mixture_information([mean],[var],[1.],cost,se)
    pv=var+se**2
    posterior_mean=lambda y:mean+var/pv*(y-mean)
    gain=integrate.quad(lambda y:max(posterior_mean(y)-cost,0)*stats.norm.pdf(y,mean,np.sqrt(pv)),
                         -np.inf,np.inf,epsabs=1e-9)[0]
    now=max(mean-cost,0)
    assert actual["evsi"]==pytest.approx(gain-now,abs=1e-8)
    assert 0<=actual["evsi"]<=actual["evpi"]
    perfect=C.normal_mixture_information([mean],[var],[1.],cost,0)
    assert perfect["evsi"]==pytest.approx(perfect["evpi"])
    useless=C.normal_mixture_information([mean],[var],[1.],cost,1e5)
    assert abs(useless["evsi"])<1e-8


def test_negative_binomial_grid_refines_with_a_proper_prior():
    g=np.random.default_rng(26)
    x=g.negative_binomial(.7,.7/(.7+2.4),300)
    expectations=[]
    for points in [161,241]:
        posterior=C.nb_posterior_grid(x,points)
        weights=posterior["weights"]
        expectations.append([weights.sum(1)@np.exp(posterior["logmu"]),
                             weights.sum(0)@np.exp(posterior["logshape"])])
        assert posterior["edge_mass"]<1e-10
    np.testing.assert_allclose(expectations[0],expectations[1],rtol=1e-5)


def test_correlated_interval_mc_error_uses_independent_dataset_means():
    # Eight perfectly correlated hits per dataset still provide one replication.
    means=np.r_[np.zeros(100),np.ones(900)]
    mc_se=means.std(ddof=1)/np.sqrt(len(means))
    row=C.CoverageRow(26,"hier","8 per dataset","coverage",.95,means.mean(),1000,mc_se=mc_se)
    assert row.se==pytest.approx(mc_se)
    assert row.se>2*np.sqrt(.9*.1/8000)


def test_fixed_p_value_curve_uses_integer_sample_sizes_consistently():
    d=C.compute_lindley()
    ns=np.asarray(d["ns"])
    assert np.all(ns==ns.astype(int))
    z=1.959964
    expected=np.sqrt(1+ns)*np.exp(-.5*z*z*ns/(1+ns))
    np.testing.assert_allclose(d["bf_n"],expected,rtol=2e-14)


def test_total_variation_includes_negative_normal_support_and_positive_tails():
    panel=C.compute_bvm()["panels"][0]
    n=panel["n"];mle=panel["mle"];shape=.5+n*mle
    grid=np.linspace(0,max(20.,mle+15*np.sqrt(mle/n)),200_001)
    full=.5*(np.trapezoid(abs(stats.gamma.pdf(grid,shape,scale=1/n)
                                  -stats.norm.pdf(grid,mle,np.sqrt(mle/n))),grid)
              +stats.norm.cdf(0,mle,np.sqrt(mle/n)))
    assert panel["tv"]==pytest.approx(full,abs=1e-7)
    assert panel["tv"]>.08


def test_large_binomial_bayes_factor_matches_high_precision_reference():
    import mpmath as mp
    d=C.compute_lindley()
    with mp.workdps(60):
        n,s=mp.mpf(d["n"]),mp.mpf(d["s"])
        logbf=mp.loggamma(n+1)-mp.loggamma(s+1)-mp.loggamma(n-s+1)-n*mp.log(2)+mp.log(n+1)
        reference=float(mp.exp(logbf))
    assert d["bf01"]==pytest.approx(reference,rel=2e-6)
