"""Independent checks for ensemble variance, tied calibration and sampling assumptions."""
import json
from pathlib import Path
import numpy as np
import pytest
from sklearn.isotonic import IsotonicRegression
from videos.stats.stats34 import compute as C


def test_variance_components_remove_finite_tree_noise():
    g=np.random.default_rng(41)
    shared=g.normal(scale=2,size=(10000,1,2))
    T=shared+g.normal(scale=3,size=(10000,12,2))
    r=C.forest_components(T)
    assert np.mean(r['sigma2'])==pytest.approx(13,rel=.025)
    assert r['rho']==pytest.approx(4/13,abs=.012)
    predicted=(r['rho']+(1-r['rho'])/12)*np.mean(r['sigma2'])
    assert predicted==pytest.approx(np.mean(T.mean(1).var(0,ddof=1)))


@pytest.mark.parametrize('seed',[2,9,17])
def test_tied_isotonic_matches_independent_weighted_reference(seed):
    g=np.random.default_rng(seed)
    x=g.integers(0,8,300)/7;y=g.integers(0,2,300).astype(float)
    sx,fit=C.tied_isotonic(x,y)
    ref=IsotonicRegression(out_of_bounds='clip').fit(x,y)
    np.testing.assert_allclose(fit,ref.predict(sx),atol=1e-13)
    perm=g.permutation(len(x));s2,f2=C.tied_isotonic(x[perm],y[perm])
    np.testing.assert_array_equal(sx,s2);np.testing.assert_allclose(fit,f2)


def test_variance_cache_obeys_bias_variance_identity():
    d=C.load('variance')
    for k,v in d['by_mtry'].items():
        assert v['mse']==pytest.approx(v['forest_var']+v['bias2'],abs=1e-12)
        assert d['curves'][k][4]==pytest.approx((v['rho']+(1-v['rho'])/20)*v['sigma2'])


def test_representative_ppi_draws_target_empirical_population_with_iid_variance():
    # Sampling more observations than population entries requires independent repeated draws.
    y=np.array([0.,1.,4.,9.,16.]);f=.7*y-3;setup=(np.arange(5),y,f,y.mean())
    g=np.random.default_rng(14)
    draws=[C._ppi_rep(g,setup,n=30,N=80) for _ in range(1000)]
    classical=np.array([r[0]['est'] for r in draws])
    pp=np.array([r[2]['est'] for r in draws])
    assert classical.mean()==pytest.approx(y.mean(),abs=.12)
    assert pp.mean()==pytest.approx(y.mean(),abs=.10)
    assert classical.var(ddof=1)==pytest.approx(y.var()/30,rel=.12)
    expected=f.var()/80+(y-f).var()/30
    assert pp.var(ddof=1)==pytest.approx(expected,rel=.12)


def test_primary_breast_cancer_table_matches_museum():
    d=json.loads(Path('tests/fixtures/qa/stats34-polish-20261107/source-data.json').read_text())
    assert (d['rows'],d['features'])==(569,30)
    assert d['feature_max_absolute_error']==0 and d['labels_equal']


def test_study_mcse_is_not_binomial_coverage_uncertainty():
    fractions=np.array([.72,.81,.85,.92,.98])
    assert C.mean_mc_se(fractions)==pytest.approx(fractions.std(ddof=1)/np.sqrt(5))
    assert C.mean_mc_se(fractions)<np.sqrt(fractions.mean()*(1-fractions.mean())/5)
