"""Independent model-selection, predictive and quadrature references for Part 28."""
import numpy as np
import pytest
from scipy import integrate,stats
import statsmodels.api as sm
from videos.stats.stats28 import compute as C


def test_covariance_df_and_mc_error_match_a_gaussian_projection():
    g=np.random.default_rng(2801)
    X=np.column_stack([np.ones(24),g.normal(size=(24,3))]);mu=X@np.array([1.,.3,-.2,.8])
    fit=lambda x,y:x@np.linalg.lstsq(x,y,rcond=None)[0]
    value,error=C.covariance_df(fit,X,mu,.7,4000,g)
    assert abs(value-4)<4*error
    assert error==pytest.approx(np.sqrt(2*4/4000),rel=.1)


def test_safeguarded_poisson_fit_matches_independent_glm():
    g=np.random.default_rng(2802)
    X=np.column_stack([np.ones(250),g.normal(size=250)])
    y=g.poisson(np.exp(X@np.array([.8,-.6])))
    expected=sm.GLM(y,X,family=sm.families.Poisson()).fit()
    np.testing.assert_allclose(C.poisson_mle(X,y),expected.params,atol=1e-9)
    with pytest.raises(ValueError):C.poisson_mle(X,np.zeros(len(y)))


def test_independent_school_loo_is_the_proper_prior_predictive():
    _,y,s=C.museum.eight_schools();d=C.load('loo')['separate']
    terms=[]
    for obs,se in zip(y,s):
        integral=integrate.quad(lambda theta:stats.norm.pdf(obs,theta,se)*stats.norm.pdf(theta,0,100),
                                 -np.inf,np.inf,epsabs=1e-12)[0]
        terms.append(np.log(integral))
    assert d['exact']==pytest.approx(sum(terms),abs=1e-8)
    assert d['elpd']-d['exact']>5
    assert d['waic']-d['exact']>8


def test_hierarchical_loo_matches_independent_contrast_density_integration():
    _,y,s=C.museum.eight_schools()
    def log_normalizer(y,s):
        # Integrating a flat mean is the Gaussian density of differences from y[0].
        def kernel(tau):
            v=s*s+tau*tau
            return stats.multivariate_normal.logpdf(y[1:]-y[0],cov=np.diag(v[1:])+v[0]*np.ones((len(y)-1,len(y)-1)))
        shift=max(kernel(t) for t in [0,3,10,30])
        z=integrate.quad(lambda t:np.exp(kernel(t)-shift),0,np.inf,epsabs=1e-11,epsrel=1e-9)[0]
        return np.log(z)+shift
    full=log_normalizer(y,s)
    exact=[full-log_normalizer(np.delete(y,i),np.delete(s,i)) for i in range(len(y))]
    np.testing.assert_allclose(C.load('loo')['hierarchical']['exact_i'],exact,atol=1e-6)


def test_loo_comparison_uses_paired_refit_contributions():
    d=C.load('loo');delta=np.asarray(d['pooled']['exact_i'])-np.asarray(d['hierarchical']['exact_i'])
    assert d['comparison']['pooled_minus_hierarchical']==pytest.approx(d['pooled']['exact']-d['hierarchical']['exact'])
    assert d['comparison']['paired_se']==pytest.approx(np.sqrt(len(delta))*delta.std(ddof=1))


def test_full_regular_prior_integral_matches_independent_double_quadrature():
    x=np.random.default_rng(2804).normal(1.8,.55,18)
    baseline=stats.norm.logpdf(x).sum()
    def integrand(mean,logsd):
        return np.exp(stats.norm.logpdf(x,mean,np.exp(logsd)).sum()-baseline)/8
    exact=integrate.dblquad(integrand,-1,1,lambda _: -2,lambda _:2,epsabs=1e-7,epsrel=1e-9)[0]
    assert C.regular_log_evidence_ratio(x)==pytest.approx(np.log(exact),abs=1e-8)


def test_singular_grid_resolves_both_axes_against_adaptive_integration():
    x=np.random.default_rng(2805).normal(size=20)
    def integrand(a,b):
        return np.exp(np.log1p(a*np.expm1(b*x-.5*b*b)).sum())/4
    exact=integrate.dblquad(integrand,-2,2,lambda _:0,lambda _:1,epsabs=1e-9,epsrel=1e-8)[0]
    assert C.mixture_log_evidence_ratio(x)==pytest.approx(np.log(exact),abs=.002)
    assert max(v['log_evidence_difference'] for v in C.load('rlct')['refinement'])<.0011


def test_penalized_fold_scaling_matches_independent_sklearn_pipeline():
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import Lasso
    from sklearn.model_selection import GridSearchCV
    X,y,train,_=C.museum.prostate();X,y=X[train],y[train]
    folds=C.Le.kfold(len(y),10,C.rng(1989))
    splits=[(np.setdiff1d(np.arange(len(y)),test),test) for test in folds]
    model=make_pipeline(StandardScaler(),Lasso(tol=1e-10,max_iter=100000))
    fit=GridSearchCV(model,{'lasso__alpha':np.geomspace(.002,1.,40)},cv=splits,scoring='neg_mean_squared_error').fit(X,y)
    assert fit.best_params_['lasso__alpha']==pytest.approx(C.load('prostate')['pen']['lasso']['lam'])


def test_test_set_uncertainty_uses_paired_case_losses():
    d=C.load('prostate');reference=np.asarray(d['tests']['full']['test_errors'])
    for record in list(d['tests'].values())+list(d['pen'].values()):
        errors=np.asarray(record['test_errors']);delta=errors-reference
        assert errors.mean()==pytest.approx(record['test'])
        assert record['paired_se_full']==pytest.approx(delta.std(ddof=1)/np.sqrt(30))
    assert d['tests']['aic']['paired_se_full']<.01
    assert d['tests']['aic']['test_se']>.1


def test_fixed_candidate_single_scores_match_the_analytic_population_score():
    # A training-selected sign remains independent of held-out cases, and symmetry gives the same risk.
    expected=-.5*np.log(2*np.pi)-.5*(5+4)
    np.testing.assert_allclose(C.load('averaging')['score_best'],expected,atol=.025)
    assert C.load('averaging')['stack'][-1]<.53


def test_loo_pit_retains_distance_without_an_iid_p_value_claim():
    for record in C.load('prostate_pit').values():
        assert 'ks_p' not in record
        assert 0<=record['ks_distance']<=1
        assert 'not calibrated' in record['ks_scope']
