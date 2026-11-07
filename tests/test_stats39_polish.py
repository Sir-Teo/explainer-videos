"""Spatial validation: held-out outcomes, coherent priors and independent Gaussian formulas."""
import numpy as np
import pytest
from explainer.stats.kit import spatial as SP
from videos.stats.stats39 import compute as C


@pytest.mark.parametrize('shape',[(4,3),(5,7),(9,6)])
def test_lattice_scale_matches_exact_precision_inverse(shape):
    nx,ny=shape;kappa=.43
    Q=SP.gmrf_precision(nx,ny,kappa).toarray()
    covariance=np.linalg.inv(Q)
    scale=C.lattice_marginal_variance(nx,ny,kappa)
    assert scale==pytest.approx(np.trace(covariance)/(nx*ny),rel=1e-12)
    assert np.trace(np.linalg.inv(Q*scale))/(nx*ny)==pytest.approx(1.,rel=1e-12)


def test_sparse_lattice_conditioning_matches_dense_covariance_conditioning():
    Q=SP.gmrf_precision(7,5,.5)*C.lattice_marginal_variance(7,5,.5)
    K=np.linalg.inv(Q.toarray());observed=np.array([0,4,9,17,30]);y=np.array([.2,-.5,1.,.8,-1.])
    ref=K[:,observed]@np.linalg.solve(K[np.ix_(observed,observed)]+.09*np.eye(5),y)
    np.testing.assert_allclose(SP.gmrf_condition(Q,observed,y,.09),ref,atol=1e-12)


def test_withheld_outcomes_cannot_change_fold_covariance_or_predictions():
    g=np.random.default_rng(97);xy=g.random((45,2));trend=g.normal(size=45)
    K=SP.matern(SP.dists(xy),1.,.25,1.5)+.2*np.eye(45)
    y=1+2*trend+g.multivariate_normal(np.zeros(45),K);test=np.arange(45)%5==0
    first=C.kriging_fold(xy,y,trend,test)
    changed=y.copy();changed[test]+=1000*g.normal(size=test.sum())
    second=C.kriging_fold(xy,changed,trend,test)
    np.testing.assert_array_equal(first[0],second[0]);np.testing.assert_array_equal(first[1],second[1])
    for key in ['rho','sigma2','tau2']:assert first[2][key]==second[2][key]


def test_universal_kriging_matches_independent_constrained_blup_system():
    g=np.random.default_rng(71);xy=g.random((25,2));x0=g.random((7,2));x=g.normal(size=25);xt=g.normal(size=7);z=g.normal(size=25)
    cov=lambda d: SP.matern(d,1.3,.25,1.5)
    K=cov(SP.dists(xy))+.2*np.eye(25);cross=cov(SP.dists(xy,x0))
    F=np.column_stack([np.ones(25),x]);F0=np.column_stack([np.ones(7),xt])
    system=np.block([[K,F],[F.T,np.zeros((2,2))]])
    solution=np.linalg.solve(system,np.vstack([cross,F0.T]));weights=solution[:25]
    expected=1.3-2*np.sum(weights*cross,axis=0)+np.sum(weights*(K@weights),axis=0)
    result=SP.krige(xy,z,x0,cov,x,xt,nugget=.2)
    np.testing.assert_allclose(result['pred'],weights.T@z,atol=1e-12)
    np.testing.assert_allclose(result['var'],expected,atol=1e-12)


def test_spatial_board_mcse_uses_independent_field_fractions():
    values=np.array([.62,.77,.85,.95,.99])
    assert C.mean_mc_se(values)==pytest.approx(values.std(ddof=1)/np.sqrt(len(values)))


@pytest.mark.parametrize('nu',[.5,1.5,2.5])
def test_circulant_embedding_preserves_covariance_instead_of_clipping_negative_modes(nu):
    lam=C.circulant_embedding(60,40,.1,1.,1.,nu)
    assert lam.min()>=0
    implied=np.fft.ifft2(lam).real
    offsets=np.arange(20)*.1
    np.testing.assert_allclose(implied[0,:20],SP.matern(offsets,1.,1.,nu),atol=1e-10)
    assert implied[0,0]==pytest.approx(1.,abs=1e-10)


def test_independent_spatial_source_tables_match_at_documented_storage_precision():
    import json
    from pathlib import Path
    rows=json.loads(Path('docs/qa/evidence/stats39-polish-20261107/source-data.json').read_text())
    assert [r['rows'] for r in rows]==[155,3103,176,578,13]
    for row in rows[:2]:assert max(row['maximum_absolute_error_by_column'].values())<=5.00001e-6
    assert rows[2]['maximum_absolute_error']<=.5
    for row in rows[3:]:assert row['maximum_absolute_error']<=5.00001e-6
