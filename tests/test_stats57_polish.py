"""Independent calculation and theorem-condition checks for Part 57."""
import math
import numpy as np
import pytest
from scipy import integrate,stats
from videos.stats.stats57 import checked as C
from explainer.stats.kit import conformal as CF


@pytest.mark.parametrize('n,shift',[(5,.7),(10,1.),(50,3.)])
def test_no_atom_coverage_uses_noncentral_t(n,shift):
    result=C.bahadur_savage_coverage(n,.003,shift)
    c=stats.t.isf(.025,n-1)
    delta=shift*math.sqrt(n)
    def integrand(u):
        radius=c*math.sqrt(u/(n-1))
        return (stats.norm.sf(delta-radius)-stats.norm.sf(delta+radius))*stats.chi2.pdf(u,n-1)
    exact=integrate.quad(integrand,0,np.inf,epsabs=1e-90,epsrel=1e-8,limit=300)[0]
    assert result['no_atom_coverage']==pytest.approx(exact,rel=2e-7,abs=1e-90)
    assert result['no_atom_coverage']>0


def test_full_conformal_union_matches_direct_refits_beyond_old_grid():
    rng=np.random.default_rng(571)
    for scale in [1.,20.]:
        X=rng.normal(size=(15,3));y=scale*rng.normal(size=15);x=rng.normal(size=3)
        result=C.full_conformal_ridge(X,y,x,1.,.2)
        for t in np.linspace(-100,100,301):
            Xa=np.vstack([X,x]);ya=np.r_[y,t]
            beta=np.linalg.solve(Xa.T@Xa+np.eye(3),Xa.T@ya)
            residual=np.abs(ya-Xa@beta)
            accepted=np.mean(residual>=residual[-1]-1e-9)>.2
            assert accepted==any(lo<=t<=hi for lo,hi in result['intervals'])
        assert result['length']==pytest.approx(sum(hi-lo for lo,hi in result['intervals']))


def test_full_conformal_can_require_an_unbounded_set():
    X=np.arange(5.)[:,None];y=np.sin(X[:,0])
    result=C.full_conformal_ridge(X,y,np.array([3.]),1.,.01)
    assert result['intervals']==[(-np.inf,np.inf)]


def test_beta_law_small_sample_is_degenerate_at_full_coverage():
    result=C.conformal_coverage_law(4,.1)
    assert result['degenerate'] and result['mean']==result['q05']==result['q95']==1


@pytest.mark.parametrize('n',[8,19,20,99,100])
def test_dual_conditional_calibration_recovers_constant_quantile(n):
    scores=np.arange(n,dtype=float);k=math.ceil((n+1)*.9)
    threshold=C.gcc_group_threshold(scores,np.ones((n,1)),np.ones(1))
    if k>n:assert threshold==np.inf
    else:assert threshold==pytest.approx(scores[k-1],abs=1e-6)


def test_dual_is_permutation_equivariant_with_ties_and_overlaps():
    rng=np.random.default_rng(572);a=rng.integers(0,2,50);b=rng.integers(0,2,50)
    G=np.c_[np.ones(50),a,b];s=rng.integers(0,10,50).astype(float);g=np.array([1.,1,0])
    values=[]
    for t in [0,4,8,20]:
        reference=C.gcc_dual(s,G,g,t)
        order=rng.permutation(50)
        assert C.gcc_dual(s[order],G[order],g,t)==pytest.approx(reference,abs=1e-9)
        values.append(reference)
    assert np.all(np.diff(values)>=-1e-9)


def test_dual_gives_at_least_nominal_empirical_coverage_for_group_indicators():
    rng=np.random.default_rng(573);group=rng.integers(0,2,41);G=np.c_[np.ones(41),group,1-group];s=rng.normal(size=41)
    eta=[]
    for i in range(len(s)):
        keep=np.arange(len(s))!=i
        eta.append(C.gcc_dual(s[keep],G[keep],G[i],s[i]))
    eta=np.array(eta)
    assert np.max(abs(G.T@eta))<1e-8
    for col in G.T:
        assert np.mean(eta[col>0]<.9-1e-9)>=.9


def test_aci_zero_step_matches_inflated_split_quantiles():
    scores=np.abs(np.random.default_rng(574).normal(size=500))
    result=C.aci(scores,gamma=0,window=30,warm=30)
    expected=[CF.conformal_quantile(scores[t-30:t],.1) for t in range(30,500)]
    assert np.array_equal(result['threshold'],expected)


def test_aci_telescopes_for_extreme_sequences_and_empty_whole_sets():
    scores=np.arange(300,dtype=float)
    result=C.aci(scores,alpha=.1,gamma=.2,window=10,warm=10)
    assert result['alpha_final']-.1==pytest.approx(.2*np.sum(.1-result['err']),abs=1e-10)
    assert abs(result['err'].mean()-.1)<=(.9+.2)/(.2*len(result['err']))
    assert np.all((result['alpha_t']>=-.2)&(result['alpha_t']<=1.2))
    assert result['infinite_sets']>0
    assert C.aci(np.zeros(300),alpha=.1,gamma=.2,window=10,warm=10)['empty_sets']>0


def test_crc_rejects_invalid_loss_direction_and_uncertified_fallback():
    with pytest.raises(ValueError,match='nonincreasing'):C.conformal_risk_control([[0,1],[1,1]],[0,1],.1)
    with pytest.raises(ValueError,match='no certified'):C.conformal_risk_control(np.ones((10,2)),[0,1],.1)
    L=np.array([[1,0,0],[1,1,0],[1,0,0]],float)
    assert C.conformal_risk_control(L,[0,.5,1],.3)==1


def test_gaussian_swapped_pair_total_variation_matches_angular_integral():
    ratio=2.5
    # Under the first product law, the likelihood ratio exceeds one when |Z1|<ratio|Z2|.
    mass=2/math.pi*math.atan(ratio)
    reverse_mass=2/math.pi*math.atan(1/ratio)
    assert mass-reverse_mass==pytest.approx(4/math.pi*math.atan(ratio)-1)
