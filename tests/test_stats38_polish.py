"""Independent spectral and Gaussian-conditioning references for the Part 38 examples."""
import numpy as np
import pytest
from scipy import signal, stats
from explainer.stats.kit import ts as T
from videos.stats.stats38 import compute as C


@pytest.mark.parametrize('n',[127,128])
def test_spectral_normalization_matches_two_sided_scipy(n):
    x=np.random.default_rng(n).normal(size=n)
    ref=signal.periodogram(x,fs=1,detrend='constant',return_onesided=False,scaling='density')[1]
    result=T.periodogram(x)
    np.testing.assert_allclose(result['I'],ref[1:n//2+1],atol=1e-13)
    size=32
    _,welch=signal.welch(x-x.mean(),fs=1,window=np.hanning(size),nperseg=size,noverlap=size//2,detrend=False,return_onesided=False,scaling='density')
    np.testing.assert_allclose(T.welch(x,size)['S'],welch[1:size//2+1],atol=1e-13)


def gaussian_reference(F,H,Q,R,m0,P0,n):
    k=len(m0);means=[];cov=np.zeros((n*k,n*k));last=P0.copy();m=m0.copy()
    for t in range(n):
        m=F@m;means.append(m.copy());last=F@last@F.T+Q;cov[t*k:(t+1)*k,t*k:(t+1)*k]=last
        for j in range(t):
            cross=F@cov[(t-1)*k:t*k,j*k:(j+1)*k]
            cov[t*k:(t+1)*k,j*k:(j+1)*k]=cross;cov[j*k:(j+1)*k,t*k:(t+1)*k]=cross.T
    D=np.kron(np.eye(n),H);mu=np.asarray(means).ravel()
    return mu,cov,D,D@cov@D.T+np.kron(np.eye(n),R)


def test_multivariate_filter_and_smoother_match_full_joint_conditioning_with_gaps():
    F=np.array([[1,.3],[0,.8]]);H=np.array([[1,.2],[.1,1]])
    Q=np.array([[.3,.02],[.02,.1]]);R=np.array([[.8,.1],[.1,.5]])
    m0=np.array([1.,-.4]);P0=np.array([[2.,.2],[.2,1.]])
    n=8;mu,K,D,V=gaussian_reference(F,H,Q,R,m0,P0,n)
    y=np.random.default_rng(23).multivariate_normal(D@mu,V).reshape(n,2);y[2,0]=np.nan;y[4,:]=np.nan
    kf=T.kalman(y,F,H,Q,R,m0,P0);sm=T.rts(kf)
    observed=np.flatnonzero(np.isfinite(y.ravel()))
    def condition(idx):
        cross=K@D[idx].T;sol=np.linalg.solve(V[np.ix_(idx,idx)],y.ravel()[idx]-(D@mu)[idx])
        return mu+cross@sol,K-cross@np.linalg.solve(V[np.ix_(idx,idx)],cross.T)
    all_m,all_cov=condition(observed)
    np.testing.assert_allclose(sm['ms'].ravel(),all_m,atol=1e-12)
    for t in range(n):
        block=slice(2*t,2*t+2);idx=observed[observed<2*(t+1)];m,P=condition(idx)
        np.testing.assert_allclose(kf['mf'][t],m[block],atol=1e-12)
        np.testing.assert_allclose(kf['Pf'][t],P[block,block],atol=1e-12)
        np.testing.assert_allclose(sm['Ps'][t],all_cov[block,block],atol=1e-12)
        if t<n-1:np.testing.assert_allclose(sm['cross'][t],all_cov[2*t+2:2*t+4,block],atol=1e-12)
    ll=stats.multivariate_normal.logpdf(y.ravel()[observed],mean=(D@mu)[observed],cov=V[np.ix_(observed,observed)])
    assert kf['loglik']==pytest.approx(ll,abs=1e-11)


def test_persistence_comparison_uses_identical_future_shocks():
    rw,ar,shocks=C.paired_persistence(120,.9,np.random.default_rng(44))
    np.testing.assert_allclose(np.diff(rw),shocks[1:],atol=1e-14)
    np.testing.assert_allclose(ar[1:]-.9*ar[:-1],shocks[1:],atol=1e-14)


def test_fractional_mean_variance_matches_full_toeplitz_quadratic_form():
    from scipy.linalg import toeplitz
    n=91;rho=T.arfima_acf(.4,n-1)
    direct=np.ones(n)@toeplitz(rho)@np.ones(n)/n**2
    formula=(1+2*np.sum((1-np.arange(1,n)/n)*rho[1:]))/n
    assert formula==pytest.approx(direct,abs=1e-14)


def test_nile_fixed_variance_shift_matches_independent_gls_profile():
    d=C.load('kalman');y=np.asarray(d['y']);n=len(y);q,r=d['q'],d['r']
    V=1e7+q*np.minimum.outer(np.arange(1,n+1),np.arange(1,n+1))+r*np.eye(n)
    h=(np.asarray(d['years'])>=1899).astype(float);res=y-y[0]
    den=h@np.linalg.solve(V,h);delta=h@np.linalg.solve(V,res)/den
    assert d['shift']==pytest.approx(delta,abs=1.01)
    # The teaching grid is two units wide; this compares the same fixed-nuisance objective.
    gain=2*d['shift']*(h@np.linalg.solve(V,res))-d['shift']**2*den
    assert d['lr_shift']==pytest.approx(gain,abs=1e-6)


def test_histogram_mass_keeps_out_of_view_draws_in_denominator():
    for name,key in [('unitroot','hist'),('coint','t_hist')]:
        d=C.load(name)
        assert sum(d[key])+d['hist_outside']==d['hist_n']
        assert d['hist_outside']>=0
    assert C.load('coint')['hist_outside']>0


def test_primary_series_agree_with_independent_r_sources():
    import json
    from pathlib import Path
    d=json.loads(Path('tests/fixtures/qa/stats38-polish-20261107/source-data.json').read_text())
    assert [r['rows'] for r in d]==[663,1860,100]
    assert d[0]['max_error']==d[2]['max_error']==0
    assert all(v==0 for v in d[1]['max_error'].values())
