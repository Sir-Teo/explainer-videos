"""Independent numerical checks for the Part 31 scientific repairs."""
import numpy as np
import pytest
from scipy import stats
from sklearn.covariance import graphical_lasso
from sklearn.mixture import GaussianMixture
from scipy.linalg import subspace_angles
from explainer.stats import museum
from explainer.stats.kit import multi as M
from videos.stats.stats31 import compute as C


def test_unique_road_weights_and_euclidean_reconstruction():
    d=C.compute_towns()
    edges=[tuple(e) for e in d['edges']]
    assert len(edges)==len(set(edges))
    assert all(a<b for a,b in edges)
    assert np.min(d['road_factors'])>=1.1
    assert np.max(d['road_factors'])<=1.3
    assert 1.43<d['detour']<1.45
    assert .54<d['rmse']<.56
    assert d['exact_rmse']<1e-10


@pytest.mark.parametrize('lam',[.05,.3,.5])
def test_offdiagonal_glasso_agrees_with_sklearn(lam):
    _,R,_=museum.harman74()
    result=C.graphical_lasso_offdiag(R,lam)
    covariance,precision=graphical_lasso(R,lam,tol=1e-9,enet_tol=1e-12,max_iter=1000)
    assert result['covariance']==pytest.approx(covariance,abs=3e-7)
    assert result['precision']==pytest.approx(precision,abs=3e-7)
    assert np.diag(result['covariance'])==pytest.approx(np.diag(R),abs=1e-12)
    assert result['kkt_max']<2e-7


def test_internal_mahalanobis_scaled_beta_reference():
    # Independent QR projection draws give the fitted residual leverage law.
    g=np.random.default_rng(301)
    X=g.normal(size=(6000,30,3));X-=X.mean(axis=1,keepdims=True)
    Q,_=np.linalg.qr(X)
    distances=29*np.sum(Q[:,0,:]**2,axis=1)
    theoretical=29**2/30*stats.beta.ppf(.975,1.5,13.)
    assert np.mean(distances>theoretical)==pytest.approx(.025,abs=.007)
    d=C.compute_mahal();n=50;p=4
    assert d['cut_fitted']==pytest.approx((n-1)**2/n*stats.beta.ppf(.975,p/2,(n-p-1)/2))
    # Exact sample identity differs from independent known-parameter chi-square draws.
    assert sum(d['d2'])==pytest.approx((n-1)*p)


def test_wishart_mean_checked_at_monte_carlo_precision():
    d=C.compute_wishart()
    z=(np.array(d['mean'])-d['S'])/d['mean_mcse']
    assert np.max(np.abs(z))<4.5
    assert d['var11']==pytest.approx(d['th11'],rel=.025)
    assert d['var12']==pytest.approx(d['th12'],rel=.025)
    assert d['mp_ab']==pytest.approx([(1-np.sqrt(50/99))**2,(1+np.sqrt(50/99))**2])


def test_factor_rotation_order_preserves_fitted_covariance():
    d=C.compute_fa();raw=np.array(d['loadings_raw']);L=np.array(d['loadings']);T=np.array(d['rotation'])
    assert raw@T==pytest.approx(L,abs=1e-12)
    assert T.T@T==pytest.approx(np.eye(4),abs=1e-12)
    assert raw@raw.T==pytest.approx(L@L.T,abs=1e-12)
    strengths=np.array(d['group_strength'])
    assert strengths.argmax(1).tolist()==[0,1,2,3]
    assert all(f['converged'] and not f['heywood'] for f in d['fits'].values())
    assert d['fits']['4']['p']<.05<d['fits']['5']['p']


def test_returned_gmm_likelihood_and_responsibilities_match_independent_evaluator():
    X,_,_=museum.iris();d=C.gmm_em_checked(X,3,C.rng(1967))
    ref=GaussianMixture(n_components=3,covariance_type='full')
    ref.weights_=d['weights'];ref.means_=d['means'];ref.covariances_=d['covs']
    ref.precisions_cholesky_=np.array([np.linalg.cholesky(np.linalg.inv(s)) for s in d['covs']])
    assert d['loglik']==pytest.approx(ref.score_samples(X).sum(),abs=1e-9)
    assert d['resp']==pytest.approx(ref.predict_proba(X),abs=1e-10)
    assert d['bic']==pytest.approx(ref.bic(X),abs=1e-9)
    assert d['converged'] and np.all(d['weights']>0)


def test_canonical_correlations_equal_centered_column_space_cosines():
    _,L,_=museum.lifecycle();X=L[:,[1,2]];Y=L[:,[0,3,4]]
    cosines=np.sort(np.cos(subspace_angles(X-X.mean(0),Y-Y.mean(0))))[::-1]
    assert M.cca(X,Y)['r']==pytest.approx(cosines,abs=1e-12)
