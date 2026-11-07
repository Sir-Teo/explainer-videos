import math
import numpy as np
import pytest
from scipy import integrate,optimize,special,stats
from videos.stats.stats59 import checked as C


@pytest.mark.parametrize("lam",[0.,1.,12.,1e4])
def test_proximal_map_against_independent_bracket(lam):
    z=np.r_[np.linspace(-10,10,41),100.]
    got=C.prox_logistic(z,lam)
    expected=[value if lam==0 else optimize.brentq(lambda t:t+lam*special.expit(t)-value,
               value-lam,value,xtol=1e-12) for value in z]
    assert np.allclose(got,expected,atol=2e-10,rtol=1e-10)


def test_sur_candes_continuation_does_not_confuse_root_failure_and_phase_transition():
    low=C.sur_candes(.1,math.sqrt(5))
    assert low['alpha']==pytest.approx(1.1678,abs=3e-5)
    assert low['sigma']==pytest.approx(3.3466,abs=4e-5)
    a=C.sur_candes(.3,math.sqrt(5),x0=(1.87,6.35,5.48))
    b=C.sur_candes(.3,math.sqrt(5),x0=(1.87,6.35,5.48),nodes=241)
    assert a['ok'] and b['ok']
    assert a['alpha']>3 and a['kappa_boundary']>.3
    assert a['factor']==pytest.approx(b['factor'],rel=1e-5)
    assert not C.sur_candes(.4,math.sqrt(5))['ok']


def test_existence_boundary_independently_integrated():
    gamma=math.sqrt(5)
    def objective(t):
        return integrate.quad(lambda v:2*special.expit(gamma*v)*stats.norm.pdf(v)
           *((1+(t*v)**2)*stats.norm.sf(t*v)-t*v*stats.norm.pdf(t*v)),
           -10,10,epsabs=1e-11)[0]
    ref=optimize.minimize_scalar(objective,bounds=(0,4),method='bounded').fun
    assert C.mle_exists_boundary(gamma)==pytest.approx(ref,abs=2e-10)
    assert C.mle_exists_boundary(0)==.5


@pytest.mark.parametrize("tau,thr",[(.015,.02),(.2,.3),(1.,1.5),(3.,.7)])
def test_soft_threshold_mse_matches_piecewise_integration(tau,thr):
    eps=.1
    reference=0.
    for truth,weight in [(0.,.9),(1.,.05),(-1.,.05)]:
        edges=sorted([-12.,0.,12.]+[q for q in [(-thr-truth)/tau,(thr-truth)/tau] if -12<q<12])
        reference+=weight*sum(integrate.quad(lambda z:
           (C.soft(truth+tau*z,thr)-truth)**2*stats.norm.pdf(z),a,b,
           epsabs=1e-12)[0] for a,b in zip(edges[:-1],edges[1:]))
    assert C._bg_mse(tau,thr,eps)==pytest.approx(reference,abs=2e-11)


@pytest.mark.parametrize("gamma",[.5,2.])
def test_analytic_ridge_risk_matches_spectral_integrals(gamma):
    a,b=(1-math.sqrt(gamma))**2,(1+math.sqrt(gamma))**2
    for lam in [.01,.125,1.,10.]:
        bias=integrate.quad(lambda x:lam**2/(x+lam)**2*C.mp_density(x,gamma),a,b,
                            epsabs=1e-11)[0]+max(0,1-1/gamma)
        var=integrate.quad(lambda x:x/(x+lam)**2*C.mp_density(x,gamma),a,b,
                           epsabs=1e-11)[0]*gamma
        got=C.ridge_risk(lam,gamma,4)
        assert got['risk']==pytest.approx(4*bias+var,abs=2e-9)


@pytest.mark.parametrize("kind",["complete","quasi"])
def test_nonexistent_mles_not_reported_as_converged(kind):
    if kind=="complete":
        X=np.array([[-2.],[-1.],[1.],[2.]])
        y=np.array([0,0,1,1])
    else:
        X=np.array([[1.,0],[-1.,0],[0,1.],[0,-1.]])
        y=np.array([1,0,1,1])
    assert not C.logistic_mle(X,y)[2]


def test_finite_mle_and_lrt_against_independent_likelihood_optimization():
    rng=np.random.default_rng(123)
    X=rng.normal(size=(180,4));y=(rng.random(180)<special.expit(X@np.array([.5,-.2,0,0]))).astype(float)
    b,ll,ok=C.logistic_mle(X,y)
    result=optimize.minimize(lambda v:np.sum(np.logaddexp(0,X@v)-y*(X@v)),np.zeros(4),
                            jac=lambda v:X.T@(special.expit(X@v)-y),method='BFGS')
    assert ok and ll==pytest.approx(-result.fun,abs=1e-8)
    assert np.allclose(b,result.x,atol=1e-6)
    assert C.lrt_one(X,y,3)['llr2']>=0


def test_bayes_denoiser_does_not_underflow_and_mmse_is_a_bayes_risk():
    assert np.isfinite(C.bayes_denoiser(np.array([-100.,0,100]),.001,.1)).all()
    assert np.array_equal(C.bayes_denoiser(np.array([-100.,0,100]),.001,.1),[-1.,0.,1.])
    # Bayes variance identity: MMSE = E X^2 - E posterior_mean^2.
    tau=.5;eps=.1
    posterior_second=0.
    for truth,weight in [(0,.9),(1,.05),(-1,.05)]:
        posterior_second+=weight*integrate.quad(lambda z:
            C.bayes_denoiser(truth+tau*z,tau,eps)**2*stats.norm.pdf(z),-12,12,epsabs=1e-11)[0]
    assert C.bayes_mmse(tau,eps)==pytest.approx(eps-posterior_second,abs=2e-10)


def test_free_convolution_has_mass_and_correct_first_two_moments():
    x=np.linspace(-4,4,3001)
    result=C.free_semicircle_plus_pm1(x,.25,eta=.0003,return_audit=True)
    d=result['density']
    assert result['max_residual']<1e-9
    assert np.trapezoid(d,x)==pytest.approx(1,abs=.001)
    assert np.trapezoid(x*d,x)==pytest.approx(0,abs=1e-9)
    assert np.trapezoid(x*x*d,x)==pytest.approx(1.25,abs=.003)

def test_lasso_grid_candidates_have_positive_penalty_and_converged_fixed_point():
    result=C.lasso_se_mse(.2,.1,1e-4)
    assert result['penalty']>0
    assert result['fixed_point_residual']<1e-8
    assert 0<result['mse']<.1


def test_converged_amp_matches_independent_lasso_at_calibrated_penalty():
    from explainer.stats.kit.sparse import lasso_cd
    rng=np.random.default_rng(48)
    n,p=150,300
    A=rng.normal(size=(n,p))/math.sqrt(n)
    truth=np.r_[np.ones(15),np.zeros(p-15)]
    y=A@truth+.1*rng.normal(size=n)
    result=C.amp_lasso(A,y,1.5,200)
    x=result['x'];tau=result['tau'][-1]
    penalty=1.5*tau*(1-np.count_nonzero(x)/n)
    assert penalty>0
    reference=lasso_cd(A,y,penalty/n,tol=1e-11,max_sweeps=10000)
    assert np.allclose(x,reference,atol=2e-7)
