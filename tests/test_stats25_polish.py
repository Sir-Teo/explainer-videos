"""Independent numerical checks for Part 25's assumptions and local corrections."""
import numpy as np
import pytest
from scipy import integrate, special, stats
from videos.stats.stats25 import compute as C
from explainer.stats.kit import mixed as MX, shrink as SH


def test_unequal_cluster_design_effect_matches_full_covariance():
    sizes=np.array([2,4,9,3]);rho=.27
    groups=np.repeat(np.arange(len(sizes)),sizes)
    covariance=(1-rho)*np.eye(len(groups))+rho*(groups[:,None]==groups)
    variance=covariance.sum()/len(groups)**2
    assert C.cluster_mean_design_effect(sizes,rho)==pytest.approx(variance*len(groups))
    assert C.cluster_mean_design_effect(np.array([5,5,5]),rho)==pytest.approx(1+4*rho)
    assert C.cluster_mean_design_effect(sizes,rho)>1+(sizes.mean()-1)*rho


@pytest.mark.parametrize("sizes,rho", [([], .2), ([0,2],.2), ([3,4],1.1)])
def test_invalid_cluster_mean_model_rejected(sizes,rho):
    with pytest.raises(ValueError):
        C.cluster_mean_design_effect(sizes,rho)


def test_arcsine_shrinkage_target_and_factor_are_on_transformed_scale():
    d=C.compute_baseball()
    y=np.asarray(d["y"]);estimate=np.asarray(d["js"])
    transform=lambda p:np.sqrt(45)*np.arcsin(2*p-1)
    target=transform(y).mean()
    np.testing.assert_allclose(transform(estimate)-target,(1-d["B"])*(transform(y)-target),atol=2e-15)
    assert d["target"]!=pytest.approx(d["grand"],abs=1e-4)
    assert d["ratio"]==pytest.approx(3.5003453225070116)


def test_noncentral_chisquare_risk_is_below_correctly_named_bound():
    p=10
    for radius in [0.,2.,5.]:
        inverse=integrate.quad(lambda x:stats.ncx2.pdf(x,p,radius**2)/x,0,np.inf,epsabs=1e-11)[0]
        risk=p-(p-2)**2*inverse
        bound=p-(p-2)**2/(p-2+radius**2)
        assert risk<=bound+1e-9
        if radius==0:assert risk==pytest.approx(2,abs=1e-9)


def test_hausman_does_not_turn_invalid_variance_into_huge_statistic():
    assert C.hausman_scalar(.3,-.01) is None
    assert C.hausman_scalar(.3,0.) is None
    assert C.hausman_scalar(.3,.02)==pytest.approx(4.5)
    with pytest.raises(ValueError):C.hausman_scalar(np.nan,1.)


def test_adaptive_logistic_integral_matches_independent_gauss_hermite():
    eta=np.full(4,.5);y=np.ones(4);sigma=1.5
    actual=C.logistic_normal_integral(eta,y,sigma)
    nodes,weights=np.polynomial.hermite.hermgauss(160)
    u=np.sqrt(2)*sigma*nodes
    likelihood=np.exp((y[:,None]*(eta[:,None]+u)-np.logaddexp(0,eta[:,None]+u)).sum(0))
    expected=weights@likelihood/np.sqrt(np.pi)
    post=weights@(likelihood*special.expit(eta[0]+u))/(weights@likelihood)
    assert actual["loglik"]==pytest.approx(np.log(expected),abs=1e-9)
    assert actual["posterior_probability"]==pytest.approx(post,abs=1e-9)
    assert abs(actual["posterior_probability"]-special.expit(.5+actual["mode"]))>.001


def test_fitted_agq_likelihood_matches_independent_integration():
    g=np.random.default_rng(2205)
    groups=np.repeat(np.arange(15),8)
    x=g.normal(size=len(groups))
    X=np.column_stack([np.ones(len(x)),x])
    y=g.binomial(1,special.expit(-.3+.8*x+g.normal(0,1.2,15)[groups]))
    fit=MX.glmm_logit(y,X,groups,nagq=30)
    reference=sum(C.logistic_normal_integral(X[groups==k]@fit["beta"],y[groups==k],fit["sigma"])["loglik"]
                  for k in np.unique(groups))
    assert fit["loglik"]==pytest.approx(reference,abs=1e-7)


def test_hartung_knapp_can_be_narrower_than_normal_interval():
    fit=SH.meta(np.array([.99,1.,1.01,1.,.99]),np.full(5,.2))
    assert np.ptp(fit["ci_hk"])<np.ptp(fit["ci_dl"])


def test_viewport_clipping_keeps_crossings_without_boundary_flattening():
    segments=C.clipped_segments([-2,0,2],[0,0,0],[-1,1,-1,1])
    assert len(segments)==2
    points=np.array(segments)
    assert points.min(axis=(0,1))[0]==-1
    assert points.max(axis=(0,1))[0]==1
    assert not C.clipped_segments([0,1,2],[0,np.nan,0],[-1,3,-1,1])
