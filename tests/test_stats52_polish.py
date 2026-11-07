"""Independent checks of Part 52's finite-sample guarantees and optimization."""
import math
import numpy as np
import pytest
from scipy import integrate,linalg,stats
from videos.stats.stats52 import compute as C
from explainer.stats.kit import hdstat as H


def test_gaussian_penalty_has_stated_conditional_union_bound():
    r=np.random.default_rng(42)
    X=r.normal(size=(100,7))*np.arange(1,8)
    lam=C.lasso_lambda(X,2,.03)
    sd=2*np.linalg.norm(X,axis=0)/100
    assert np.sum(2*stats.norm.sf(lam/(2*sd)))<=.03
    assert lam==pytest.approx(2*sd.max()*math.sqrt(2*math.log(14/.03)))


def test_lasso_solution_satisfies_independent_kkt_conditions():
    r=np.random.default_rng(9);X=r.normal(size=(80,120))
    beta=np.zeros(120);beta[:3]=[1,2,-1];y=X@beta+r.normal(size=80)
    lam=C.lasso_lambda(X);b=C.checked_lasso(X,y,lam)
    grad=X.T@(X@b-y)/80
    assert np.allclose(grad[b!=0],-lam*np.sign(b[b!=0]),atol=1e-7)
    assert np.max(abs(grad[b==0]),initial=0)<=lam+1e-7


def test_irrepresentability_violation_is_not_impossible_finite_recovery():
    # A full-rank, normalized design with irrepresentable value 1.2.
    Gram=np.array([[1,0,.6],[0,1,.6],[.6,.6,1.]])
    X=math.sqrt(3)*np.linalg.cholesky(Gram).T
    beta=np.array([1.,1.,0]);lam=.1
    noise=3*lam*np.linalg.solve(X.T,[1.,1.,0])
    y=X@beta+noise
    assert H.irrepresentable(X,np.array([0,1]),np.ones(2))>1
    b=C.checked_lasso(X,y,lam)
    assert np.allclose(b,beta,atol=1e-8)  # constructed noise satisfies exact KKT


def test_nuclear_decomposability_needs_both_row_and_column_orthogonality():
    A=np.diag([1.,0.]);B=np.array([[0.,1.],[0,0]])
    assert np.sum(A*B)==0
    assert np.linalg.norm(A+B,'nuc')<np.linalg.norm(A,'nuc')+np.linalg.norm(B,'nuc')
    D=np.diag([0.,2.]);assert np.linalg.norm(A+D,'nuc')==3


def test_svd_ols_covariance_matches_qr_without_normal_equation_inverse():
    r=np.random.default_rng(12);X=r.normal(size=(120,8));X-=X.mean(0)
    X[:,-1]=X[:,0]+1e-5*X[:,-1];y=r.normal(size=120);y-=y.mean()
    b,cov,condition=C.full_model_ols(X,y)
    Q,R=np.linalg.qr(X);want=linalg.solve_triangular(R,Q.T@y)
    Ri=linalg.solve_triangular(R,np.eye(8));sigma2=np.sum((y-X@want)**2)/(120-8-1)
    assert condition>1e5
    assert np.allclose(b,want,rtol=1e-8,atol=1e-7)
    assert np.allclose(cov,sigma2*Ri@Ri.T,rtol=1e-8,atol=1e-7)


def test_rank_deficient_model_does_not_report_unique_coefficient_intervals():
    x=np.arange(8.)-3.5
    with pytest.raises(ArithmeticError,match='rank deficient'):
        C.full_model_ols(np.column_stack([x,x]),x)


def test_mp_stieltjes_against_independent_density_integration():
    gamma=.5;a,b=H.mp_edges(gamma)
    for z in [-2+.3j,1+.5j,4+.2j]:
        want=integrate.quad_vec(lambda x:H.mp_pdf(x,gamma)/(x-z),a,b,epsabs=1e-10)[0]
        assert H.mp_stieltjes(z,gamma)==pytest.approx(want,abs=1e-9)


def test_fredholm_cutoff_and_quadrature_convergence():
    s=np.array([-6.,-2.,0.,2.,4.])
    for beta in [1,2]:
        # The default finite cutoff is accurate here, but not machine-precision certified.
        assert np.max(abs(H.tracy_widom_cdf(s,beta)-H.tracy_widom_cdf(s,beta,m=96,L=24)))<2e-5


def test_spike_delta_method_derivative_matches_finite_difference():
    for ell in [1.,3.,8.]:
        gamma=.5;h=1e-5
        fd=(H.spike_eigenvalue(ell+h,gamma)-H.spike_eigenvalue(ell-h,gamma))/(2*h)
        assert fd==pytest.approx(1-gamma/ell**2,rel=1e-8)


def test_fully_observed_nuclear_penalty_matches_closed_form_prox():
    r=np.random.default_rng(72);M=r.normal(size=(9,7));lam=.8
    fit=C.soft_impute_checked(M,np.ones_like(M,bool),lam)
    U,d,Vh=np.linalg.svd(M,full_matrices=False)
    assert np.allclose(fit['Z'],(U*np.maximum(d-lam,0))@Vh,atol=1e-10)


def test_masked_nuclear_penalty_fixed_point_certificate():
    r=np.random.default_rng(73);M=r.normal(size=(12,2))@r.normal(size=(2,10));obs=r.random(M.shape)<.6
    fit=C.soft_impute_checked(M,obs,.4)
    W=np.where(obs,M,fit['Z']);U,d,Vh=np.linalg.svd(W,full_matrices=False)
    residual=np.linalg.norm(fit['Z']-(U*np.maximum(d-.4,0))@Vh)/max(1,np.linalg.norm(fit['Z']))
    assert residual<2e-7


def test_nearly_collinear_sparse_coefficients_remain_weakly_identified():
    r=np.random.default_rng(74);x=r.normal(size=500);z=r.normal(size=500)
    X=np.column_stack([x,x+.001*z]);X-=X.mean(0);X/=X.std(0)
    beta=np.array([1.,-1.]);shift=np.linalg.norm(X@beta)
    # Two sparse models change a coefficient by one yet their joint Gaussian laws have TV <.02.
    tv=2*stats.norm.cdf(shift/2)-1
    assert tv<.02 and np.linalg.cond(X)>1000
    # No pair of narrow disjoint intervals can each be uniformly 95% honest over both models.
    assert 1-tv>2*.05


def test_board_narration_calls_renderer_with_bookmark_groups(monkeypatch):
    from videos.stats.stats52 import s10_tracy as scene
    captured=[]
    monkeypatch.setattr(scene,'board_rows',lambda *args:[])
    monkeypatch.setattr(scene,'show_board',lambda *args:captured.append(args))
    scene.TracyWidom.board(object())
    assert len(captured)==1 and len(captured[0])==4
    assert captured[0][3]==[("a",[0]),("b",[1])]
    assert '<bookmark' in captured[0][2]
