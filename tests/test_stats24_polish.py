"""Reference checks for the local Part 24 calculations."""
import numpy as np
import pytest
import statsmodels.api as sm
from scipy import special,stats
from videos.stats.stats24 import compute as C

@pytest.mark.parametrize("link,ref",[
    ("logit",sm.families.links.Logit()),
    ("probit",sm.families.links.Probit()),
    ("cloglog",sm.families.links.CLogLog()),
])
def test_safeguarded_irls_matches_reference_grouped_likelihood(link,ref):
    X,x,n,k=C.bliss_X()
    f=C.glm_fit(X,k/n,C.G.family("binomial",link),n=n,start=np.zeros(2))
    r=sm.GLM(np.column_stack([k,n-k]),X,family=sm.families.Binomial(ref)).fit(tol=1e-12)
    np.testing.assert_allclose(f.coef,r.params,rtol=2e-7)
    np.testing.assert_allclose(f.se(),r.bse,rtol=2e-6)
    assert np.max(np.diff(f.deviance_path)) < 1e-8
    assert np.max(abs(f.path[-1]-f.coef)) == 0

def test_line_search_handles_an_overshooting_poisson_start():
    g=np.random.default_rng(103)
    X=sm.add_constant(g.normal(size=200))
    y=g.poisson(np.exp(.4+.5*X[:,1]))
    f=C.glm_fit(X,y,C.G.family("poisson"),start=np.array([-4.,0.]))
    r=sm.GLM(y,X,family=sm.families.Poisson()).fit()
    assert max(f.halvings)>0
    np.testing.assert_allclose(f.coef,r.params,rtol=1e-8)
    assert np.max(np.diff(f.deviance_path)) < 1e-8

@pytest.mark.parametrize("cs,ref",[
    ("independence",sm.cov_struct.Independence()),
    ("exchangeable",sm.cov_struct.Exchangeable()),
])
def test_analytic_working_inverse_matches_statsmodels_gee(cs,ref):
    g=np.random.default_rng(986)
    groups=np.repeat(np.arange(45),g.integers(5,15,size=45))
    x=g.normal(size=len(groups));u=g.normal(0,.6,45)[groups]
    X=sm.add_constant(x)
    y=g.binomial(1,special.expit(-.2+.7*x+u))
    actual=C.gee_logistic(X,y,groups,cs)
    expected=sm.GEE(y,X,groups,family=sm.families.Binomial(),cov_struct=ref).fit()
    np.testing.assert_allclose(actual["coef"],expected.params,rtol=2e-4,atol=1e-6)
    np.testing.assert_allclose(actual["se_robust"],expected.bse,rtol=3e-3)
    assert actual["score_norm"] < 1e-6

def test_calibration_retains_counts_and_endpoint_uncertainty_under_ties():
    p=np.repeat([.2,.8],[10,10]);y=np.r_[np.zeros(10),np.ones(10)]
    d=C.calibration_bins(p,y,10)
    assert sum(d["count"]) == len(y)
    assert np.isfinite(d["pred"]).all()
    assert all(lo<hi for lo,hi in zip(d["lo"],d["hi"]))
    for n,obs,lo,hi in zip(d["count"],d["obs"],d["lo"],d["hi"]):
        # Independent Wilson result from statsmodels.
        from statsmodels.stats.proportion import proportion_confint
        np.testing.assert_allclose([lo,hi],proportion_confint(n*obs,n,method="wilson"),atol=1e-15)

def test_invalid_correlation_is_not_silently_independence():
    with pytest.raises(ValueError):
        C.gee_logistic(np.ones((4,1)),np.array([0,1,0,1]),np.array([0,0,1,1]),"typo")
