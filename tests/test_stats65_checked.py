"""Independent numerical references and design checks for the dissertation rerun."""
import itertools
import math
import numpy as np
import pytest
from scipy import integrate,stats
from videos.stats.stats65 import checked as T
from videos.stats.stats65 import compute as C
from explainer.stats.kit.conformal import weighted_quantile_conformal


def test_abs_tilt_tv_against_piecewise_quadrature():
    for b,mu in itertools.product([-.8,0,.5,1.4],[0,.5,1.5]):
        z=2*np.exp(b*b/2)*stats.norm.cdf(b)
        density=lambda x:np.exp(b*abs(x))*stats.norm.pdf(x)/z
        val=integrate.quad(lambda x:abs(density(x)-stats.norm.pdf(x,mu)),-12,0,epsabs=1e-9,limit=200)[0]
        val+=integrate.quad(lambda x:abs(density(x)-stats.norm.pdf(x,mu)),0,12,epsabs=1e-9,limit=200)[0]
        assert T.tv_abs_tilt(b,mu)==pytest.approx(val/2,abs=1e-7)


def test_abs_tilt_at_zero_equals_normal_shift_tv():
    for mu in [0,.3,1,3]:assert T.tv_abs_tilt(0,mu)==pytest.approx(T.tv_gauss_shift(0,mu))


def test_batched_quantile_matches_scalar_weighted_measure():
    r=np.random.default_rng(3);s=r.random(41);wc=np.exp(r.normal(size=41));wt=np.exp(r.normal(size=50))
    expected=[weighted_quantile_conformal(s,wc,w,.1) for w in wt]
    assert np.allclose(T.halfwidths(s,wc,wt,.1),expected)


def test_batched_quantile_scale_invariance_extreme_common_factor():
    s=np.array([0.,1,3]);w=np.array([1.,2,3]);wt=np.array([1.,100.])
    a=T.halfwidths(s,w,wt,.2)
    assert np.array_equal(a,T.halfwidths(s,w*1e250,wt*1e250,.2))
    assert np.array_equal(a,T.halfwidths(s,w*1e-250,wt*1e-250,.2))


def test_infinite_interval_needs_only_alpha_test_mass():
    s=np.arange(9.)
    # Test weight 2 is far less than calibration sum 9, but normalized mass 2/11>.1.
    assert np.isinf(T.halfwidths(s,np.ones(9),np.array([2.]),.1)[0])
    assert np.isfinite(T.halfwidths(s,np.ones(9),np.array([.5]),.1)[0])


def test_constant_weight_quantile_is_unweighted_conformal():
    x=np.arange(20.)/10;y=T.mean_fn(x)+np.arange(20.)
    a=T.weighted_interval(x,y,None,[0,1],.1)
    b=T.weighted_interval(x,y,lambda z:np.ones(len(z)),[0,1],.1)
    assert np.array_equal(a,b) and a[0]==18


def test_nonpositive_weights_rejected():
    with pytest.raises(ValueError):T.halfwidths([1,2],[0,1],[1],.1)
    with pytest.raises(ValueError):T.halfwidths([1,2],[1,1],[np.inf],.1)


def test_checked_logistic_tilt_and_score():
    r=np.random.default_rng(4);w=T.logistic_weights(r.normal(size=5000),1+r.normal(size=5000))
    assert w.score_residual<1e-8
    assert w.coef[1]==pytest.approx(1,abs=.08)


def test_study_has_gap_mc_error_and_coverage_decomposition():
    d=T.study([1.5],[1.],['oracle','estimated'],60,100,100,.1,np.random.default_rng(5))
    for row in d:
        assert row['coverage']==pytest.approx(row['finite_covered_mass']+row['inf'])
        assert row['gap_mcse']>0 and row['mcse']>0
        assert row['coverage']>=row['bound']-4*row['gap_mcse']


def test_empirical_source_target_ratio_has_same_conditional_law():
    # Identical X rows can have different Y; selection depends on X and preserves Y|X.
    x=np.array([20.,20,70,70]);pi=T.selection_probs(x);p=pi/pi.sum();q=(1-pi)/(1-pi).sum();w=(1-pi)/pi
    assert np.allclose(p*w/(p@w),q)
    assert p[0]/p[:2].sum()==q[0]/q[:2].sum()==.5


def test_tv_bound_pinsker_and_normalized_empirical_target():
    for d in [0,.3,1,3]:assert T.tv_gauss_shift(0,d)<=d/2+1e-12
    p=np.array([.2,.8]);q=np.array([.8,.2]);tv=.5*np.sum(abs(p-q))
    assert tv==pytest.approx(max(abs(sum(p[list(a)])-sum(q[list(a)])) for k in range(3) for a in itertools.combinations(range(2),k)))


def test_application_design_separates_five_samples():
    # Scope is part of the saved scientific contract, not a national coverage claim.
    d=C.load('nhanes')
    assert d['n_aux_each']==1000 and d['n_test']==3000
    assert d['n_train']==1093 and d['n_cal']==1094
    assert 'independent IID draws with replacement' in d['scope']
    assert d['max_logistic_score']<1e-8
    assert d['bound']==pytest.approx(.9-d['mean_tv'])


def test_board_rows_use_empirical_replicate_mcse():
    board=C.load('board')['rows'];study=C.load('study')['rows'];app=C.load('nhanes')
    none=next(r for r in study if r['mu']==r['gamma']==1 and r['method']=='none')
    assert board[0]['mc_se']==none['mcse']
    assert board[2]['mc_se']==app['mcse']['none']
    assert all(r['se']==r['mc_se'] for r in board)


def test_full_board_refuses_to_publish_partial_course(monkeypatch):
    monkeypatch.setattr(C,'load_all',lambda **kwargs:[])
    with pytest.raises(RuntimeError,match='missing parts'):
        C.compute_fullboard()


@pytest.mark.parametrize("change", ["none", "modified", "missing", "added", "contributor", "legacy"])
def test_cached_full_board_validates_historical_inputs(tmp_path, monkeypatch, change):
    from types import SimpleNamespace
    import hashlib
    source = tmp_path / "board.json"
    source.write_text("original historical rows")
    data = {"rows": [{"part": 1}], "input_hashes": [
        {"file": str(source), "sha256": hashlib.sha256(source.read_bytes()).hexdigest()}]}
    paths = [source]
    monkeypatch.setattr(C, "CACHE", SimpleNamespace(load=lambda name: data))
    monkeypatch.setattr(C, "_board_parts", lambda: {1, 2} if change == "contributor" else {1})
    monkeypatch.setattr(C, "_historical_inputs", lambda: paths)
    if change == "modified":
        source.write_text("updated historical rows")
    elif change == "missing":
        source.unlink()
    elif change == "added":
        extra = tmp_path / "new-board.json"
        extra.write_text("new contributor")
        paths.append(extra)
    elif change == "legacy":
        del data["input_hashes"]
    if change == "none":
        assert C.load("fullboard") is data
    else:
        with pytest.raises(RuntimeError, match="stale or incomplete"):
            C.load("fullboard")
    # Other computation items do not inherit full-course dependencies.
    assert C.load("study") is data
