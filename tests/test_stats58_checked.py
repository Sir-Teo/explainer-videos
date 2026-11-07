"""Regression checks for the scientific failures found in the Part 58 audit."""
import itertools
import math

import numpy as np
import pytest
from scipy import integrate, stats

from videos.stats.stats58 import checked as C


def test_sprt_tail_certificate_contains_enumerated_truncation():
    p = .17
    d = C.sprt_bernoulli_exact(p, .1, .2, .05, .1, n_max=9)
    en, remaining, acc1 = 0., 0., 0.
    for bits in itertools.product((0, 1), repeat=9):
        weight = p**sum(bits)*(1-p)**(9-sum(bits))
        z = C.sprt_simulate(bits, .1, .2, .05, .1)
        en += weight*z["n"]
        remaining += weight*(z["decision"] == -1)
        acc1 += weight*(z["decision"] == 1)
    assert d["asn_lower"] == pytest.approx(en)
    assert d["unfinished"] == pytest.approx(remaining)
    assert d["accept_h1"] == pytest.approx(acc1)
    assert d["accept_h1"]+d["accept_h0"]+d["unfinished"] == pytest.approx(1)


@pytest.mark.parametrize("p", [0., .04, .1, .15, .2, .32, 1.])
def test_sprt_tail_precision_and_wald_identity(p):
    d = C.sprt_bernoulli_exact(p, .1, .2, .05, .1)
    assert d["asn_upper"]-d["asn_lower"] < 2e-7
    assert d["accept_h1"]+d["accept_h0"]+d["unfinished"] == pytest.approx(1, abs=3e-14)
    # Independent simulation validates both the decision and stopping-time scale.
    r = np.random.default_rng(8900)
    paths = [C.sprt_simulate(r.random(1200)<p,.1,.2,.05,.1) for _ in range(1000)]
    ns = np.array([q["n"] for q in paths])
    assert ns.mean() == pytest.approx(d["asn"], abs=5*ns.std(ddof=1)/np.sqrt(len(ns))+.05)


def test_continuum_cell_hull_contains_fine_exact_betting_set():
    x = np.random.default_rng(12).beta(2, 7, 70)
    coarse = C.betting_cs(x, .05, grid=np.linspace(0,1,21))
    # Independent direct wealth on candidate points between the coarse nodes.
    m = np.linspace(.000123,.999877,801)
    kp = np.ones(len(m)); km = np.ones(len(m)); alive = np.ones(len(m),bool)
    history = []
    prior_residuals = []
    for i,y in enumerate(x):
        mu = (.5+sum(history))/(i+1) if i else .5
        var = (.25+sum(prior_residuals))/(i+1) if i else .25
        lam = np.sqrt(2*np.log(40)/(var*(i+1)*np.log(i+2)))
        kp *= 1+np.minimum(lam,.5/m)*(y-m)
        km *= 1-np.minimum(lam,.5/(1-m))*(y-m)
        alive &= (kp+km)/2 < 20
        if alive.any():
            assert coarse["lo"][i] <= m[alive].min()
            assert coarse["hi"][i] >= m[alive].max()
        history.append(y)
        prior_residuals.append((y-mu)**2)


@pytest.mark.parametrize("value", [0., 1.])
def test_endpoint_means_are_never_lost_for_constant_data(value):
    d = C.betting_cs(np.full(60,value), .05)
    assert np.all(d["lo"] <= value)
    assert np.all(d["hi"] >= value)


def test_off_grid_mean_survives_before_any_possible_crossing():
    # A true mean below the old .001 candidate-grid boundary.
    for p in (.0004, .9996):
        d = C.betting_cs([float(p>.5)],.05)
        assert d["lo"][0] <= p <= d["hi"][0]


def test_invalid_candidate_grid_rejected():
    with pytest.raises(ValueError):
        C.betting_cs([0,1], .05, grid=[.001,.5,.999])


def test_true_assignment_floor_and_conditional_score_expectation():
    r = np.random.default_rng(14)
    d = C.thompson_bernoulli([0.,1.],300,r,floor=.05,n_mc=3)
    assert d["e"].min() >= .05
    assert np.allclose(d["e"].sum(1),1)
    # Enumerate next action and reward conditional on each auxiliary-draw state.
    means, prediction = np.array([.2,.7]), np.array([.9,.1])
    for e in d["e"][::13]:
        expected = np.zeros(2)
        for a in (0,1):
            for y in (0,1):
                score = prediction.copy()
                score[a] += (y-prediction[a])/e[a]
                expected += e[a]*(means[a] if y else 1-means[a])*score
        assert np.allclose(expected,means)


def test_cusum_censoring_is_reported_at_requested_horizon():
    d = C.cusum_arl(0.,0.,1.,1e6,7,np.random.default_rng(1),t_max=5)
    assert d["censored"] == 7
    assert np.array_equal(d["run_lengths"],np.full(7,5))
    assert d["mean"] == 5


def test_smooth_boundaries_converge_and_spend_five_percent():
    p,b,_ = C.sequential_boundaries(5)
    assert C.crossing_probs([p]*5,nodes=320).sum() == pytest.approx(.05,abs=2e-10)
    assert C.crossing_probs(b,nodes=320).sum() == pytest.approx(.05,abs=2e-10)
    assert p == pytest.approx(2.413,abs=.003)


def test_batched_peeking_matches_full_stream_rng():
    ns=[1,10,31]
    r=np.random.default_rng(3)
    X=r.standard_normal((521,31))
    Z=np.abs(np.cumsum(X,1)/np.sqrt(np.arange(1,32)))
    expected=[(Z[:,:n].max(1)>=stats.norm.isf(.025)).mean() for n in ns]
    assert np.array_equal(C.peeking_curve(ns,.05,521,np.random.default_rng(3)),expected)


def test_universal_inference_uses_actual_null_supremum():
    x=np.linspace(-2,3,40)
    r=np.random.default_rng(8); o=r.permutation(len(x))
    a,b=x[o[:20]],x[o[20:]]
    num=stats.norm.logpdf(b,a.mean(),a.std()+1e-12).sum()
    # Optimize log sigma independently rather than reusing the closed form.
    from scipy.optimize import minimize_scalar
    optimum=minimize_scalar(lambda z:-stats.norm.logpdf(b,0,np.exp(z)).sum(),
                            bounds=(-5,5),method="bounded",
                            options={"xatol":1e-12})
    expected=np.exp(num+optimum.fun)
    assert C.split_lrt_normal_mean(x,np.random.default_rng(8)) == pytest.approx(expected,rel=2e-12)
