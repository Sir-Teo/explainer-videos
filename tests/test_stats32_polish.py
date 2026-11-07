"""Independent checks for Part 32's preprocessing, integration and uncertainty repairs."""
import numpy as np
import pytest
from scipy import integrate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler,PolynomialFeatures,FunctionTransformer
from sklearn.linear_model import Lasso
from videos.stats.stats32 import compute as C


def test_quadratic_cv_matches_independent_sklearn_pipeline():
    g=np.random.default_rng(401);X=g.normal(size=(50,10));X[:,1]=g.integers(1,3,50)
    X[:10,0]+=8  # exposes fitting a global scaler before validation
    y=2*X[:,0]*X[:,2]+X[:,4]+g.normal(size=50)
    names=['age','sex','bmi','bp','tc','ldl','hdl','tch','ltg','glu']
    folds=np.arange(50)%5;lams=np.array([2.,.5,.1])
    actual=C.quadratic_cv(X,y,names,lams,folds);errors=[]
    powers=PolynomialFeatures(2,include_bias=False).fit(X).powers_
    keep=np.flatnonzero(~((powers[:,1]==2)&(powers.sum(1)==2)))
    for k in range(5):
        tr,te=folds!=k,folds==k;row=[]
        for lam in lams:
            pipe=make_pipeline(StandardScaler(),PolynomialFeatures(2,include_bias=False),
                               FunctionTransformer(lambda z:z[:,keep]),StandardScaler(),
                               Lasso(alpha=lam,tol=1e-12,max_iter=30000))
            pipe.fit(X[tr],y[tr]);row.append(np.mean((y[te]-pipe.predict(X[te]))**2))
        errors.append(row)
    assert actual['fold_errors']==pytest.approx(np.array(errors),abs=1e-7)


@pytest.mark.parametrize('tau',[.01,.1,1.,10.])
def test_horseshoe_angle_integral_matches_weighted_kappa_quadrature(tau):
    ys=np.array([-8.,-1.,0.,.1,2.,8.]);reference=[]
    for y in ys:
        def integrand(k,power):
            return k**power*np.exp(-k*y*y/2)/(1+(tau*tau-1)*k)
        den=integrate.quad(integrand,0,1,args=(0,),weight='alg',wvar=(0,-.5),epsabs=1e-10)[0]
        num=integrate.quad(integrand,0,1,args=(1,),weight='alg',wvar=(0,-.5),epsabs=1e-10)[0]
        reference.append(y*(1-num/den))
    assert C.horseshoe_mean_quad(ys,tau)==pytest.approx(reference,abs=2e-9)


def test_pooled_interval_mcse_accounts_for_shared_dataset_outcomes():
    # Eight perfectly correlated intervals per dataset are one independent trial.
    hits=np.r_[np.full(80,8),np.zeros(20)];counts=np.full(100,8)
    assert C.ratio_mcse(hits,counts)==pytest.approx(np.sqrt(.8*.2/99))
    assert C.ratio_mcse(hits,counts)>2.8*np.sqrt(.8*.2/800)


def test_random_denominator_mcse_matches_dataset_bootstrap():
    g=np.random.default_rng(402);counts=g.integers(0,15,100)
    prob=g.beta(3,1,size=100);hits=g.binomial(counts,prob)
    indices=g.integers(0,100,size=(30000,100))
    boot=hits[indices].sum(1)/counts[indices].sum(1)
    assert C.ratio_mcse(hits,counts)==pytest.approx(boot.std(ddof=1),rel=.035)


def test_softimpute_full_observation_matches_closed_form_nuclear_prox():
    g=np.random.default_rng(403);Y=g.normal(size=(8,6));lam=1.3
    result=C.soft_impute_checked(Y,np.ones(Y.shape,bool),lam)
    U,s,Vt=np.linalg.svd(Y,full_matrices=False);expected=(U*np.maximum(s-lam,0))@Vt
    assert result['Z']==pytest.approx(expected,abs=1e-12)
