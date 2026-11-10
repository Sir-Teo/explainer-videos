"""Independent numerical checks for study-level multiplicity QA."""
import json
from pathlib import Path
import numpy as np
import pytest
from scipy import stats
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler
from videos.stats.stats33 import compute as C
from explainer.stats import museum


def test_fold_preprocessing_and_predictions_match_independent_pipeline():
    g=np.random.default_rng(913);X=g.normal(size=(51,7));X[-1]*=40
    y=X[:,0]*.7+g.normal(size=51);lams=np.array([1.,.2,.04])
    got=C.fold_scaled_cv(X,y,lams,K=4,rng=np.random.default_rng(44));errors=[]
    for test in got['folds']:
        train=np.setdiff1d(np.arange(len(y)),test)
        scale=StandardScaler().fit(X[train]);a=scale.transform(X[train]);b=y[train]-y[train].mean()
        errors.append([np.mean((y[test]-(Lasso(alpha=lam,fit_intercept=False,tol=1e-12,max_iter=100000).fit(a,b).predict(scale.transform(X[test]))+y[train].mean()))**2) for lam in lams])
    expected=np.average(errors,axis=0,weights=[len(t) for t in got['folds']])
    np.testing.assert_allclose(got['mse'],expected,rtol=2e-8,atol=2e-8)


def test_empty_selection_contributes_zero_noncoverage():
    assert C._fcr_rep(C.rng(2),m=100,m1=0,q=0)==(1.,1.,0,0.)


def test_board_mcse_uses_study_level_variation():
    d=C.load('board')
    samples=list(d['fdp_replicates'].values())+[np.array(d['fcr_replicates'])[:,k] for k in (0,1)]
    for row,values in zip(d['rows'],samples):
        assert row['reps']==len(values)==1000
        assert row['achieved']==pytest.approx(np.mean(values))
        assert row['se']==pytest.approx(np.std(values,ddof=1)/np.sqrt(len(values)))


def test_clipped_storey_estimator_is_not_conservative_in_expectation():
    # With m=1, lambda=.5, an exact uniform null gives estimate 0 or 2.
    assert .5*0+.5*2==1
    assert .5*min(1,0)+.5*min(1,2)<1


def test_local_fdr_density_matches_independent_poisson_glm():
    import statsmodels.api as sm
    _,z=museum.prostate_z();d=C.MT.locfdr(z);x=d['mids'];u=(x-x.mean())/x.std()
    B=np.vander(u,N=8,increasing=True)
    ref=sm.GLM(d['counts'],B,family=sm.families.Poisson()).fit(maxiter=500,tol=1e-12)
    assert ref.converged
    np.testing.assert_allclose(d['f'],ref.predict(B)/(len(z)*d['width']),rtol=1e-10,atol=1e-12)


def test_prostate_reference_t_z_conversion():
    t,z=museum.prostate_z()
    np.testing.assert_allclose(z,stats.norm.ppf(stats.t.cdf(t,100)),rtol=0,atol=1e-6)
    reference=json.loads(Path('tests/fixtures/qa/stats33-polish-20261107/source-data.json').read_text())
    assert reference['genes']==6033 and reference['samples']==102
    assert reference['t_max_absolute_error']<6e-7 and reference['z_max_absolute_error']<6e-7


def test_knockoff_empirical_uncertainty_includes_all_twenty_studies():
    d=C.load('knock')
    for name,v in d['replicates'].items():
        assert len(v)==20
        assert d['mc_se'][name]==pytest.approx(np.std(v,ddof=1)/np.sqrt(20))


def test_publication_rule_matches_positive_direction_selection():
    g=np.random.default_rng(41);s=C.MT.publication_sim(1000,.0,g,publish_null=0)
    np.testing.assert_array_equal(s['published'],(s['p']<.05)&(s['est']>0))
