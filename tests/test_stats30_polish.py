"""Numerical references for Part 30's robust inference and tuning."""
import itertools
import math

import numpy as np
import pytest
from scipy import integrate, optimize, stats

from explainer.stats.kit import robust as R
from videos.stats.stats30 import compute as C


def test_sn_matches_low_median_excluding_self_definition():
    for n in (2,3,4,5,8,9,10,11,24):
        x=np.random.default_rng(n).normal(size=n)
        # Equivalent robustbase definition: low_i low_{j != i}|x_i-x_j|.
        inside=[]
        for i in range(n):
            gaps=sorted(abs(x[i]-x[j]) for j in range(n) if j!=i)
            inside.append(gaps[(len(gaps)-1)//2])
        raw=sorted(inside)[(n-1)//2]
        correction=[.743,1.851,.954,1.351,.993,1.198,1.005,1.131][n-2] if n<=9 else n/(n-.9) if n%2 else 1
        assert C.sn_scale(x)==pytest.approx(1.1926*correction*raw)
    assert C.sn_scale([2,2,2,2])==0


def test_hl_eight_observation_reference_has_exact_sign_coverage():
    magnitudes=np.array([.7,1.2,2.8,4.1,5.6,6.7,8.2,10.4])
    hits=0
    for signs in itertools.product((-1,1),repeat=8):
        lo,hi=C.hl_interval(magnitudes*np.asarray(signs))
        hits+=lo<=0<=hi
    assert hits==246
    assert hits/256==pytest.approx(.9609375)


def test_small_sample_hl_requires_unbounded_confidence_set():
    assert C.hl_interval([1,2,3,4,5])==(-math.inf,math.inf)
    lo,hi=C.hl_interval(np.arange(1,7,dtype=float))
    assert np.isfinite([lo,hi]).all()


def test_large_sample_hl_uses_exact_signed_rank_reference():
    x=np.random.default_rng(66).normal(size=66)
    lo,hi=C.hl_interval(x)
    w=np.sort(R.walsh_averages(x));k=int(np.searchsorted(w,lo))+1
    distribution=R.signed_rank_null(66)
    assert distribution[:k].sum()<=.025+1e-13
    assert distribution[:k+1].sum()>.025
    assert hi==w[len(w)-k]


def test_catoni_variance_bound_tuning_obeys_exponential_envelope():
    n,v,delta=500,7.6388888889,.001
    L=np.log(2/delta);t=np.sqrt(2*v*L/(n-2*L));alpha=np.sqrt(2*L*(n-2*L)/(n*n*v))
    assert n*(-alpha*t+.5*alpha**2*(v+t*t))+L==pytest.approx(0,abs=1e-12)
    grid=np.linspace(-20,20,1001)
    psi=np.sign(grid)*np.log1p(abs(grid)+grid*grid/2)
    assert np.all(psi<=np.log1p(grid+grid*grid/2)+1e-13)
    assert np.all(psi>=-np.log1p(-grid+grid*grid/2)-1e-13)


def test_catoni_equation_and_location_scale_equivariance():
    x=np.random.default_rng(30).pareto(2.2,150);v=2.2/(1.2**2*.2);delta=.05
    result=C.catoni_with_bound(x,delta,v)
    L=np.log(2/delta);alpha=np.sqrt(2*L*(len(x)-2*L)/(len(x)**2*v))
    u=alpha*(x-result)
    assert np.sum(np.sign(u)*np.log1p(abs(u)+u*u/2))==pytest.approx(0,abs=1e-9)
    assert C.catoni_with_bound(3*x+7,delta,9*v)==pytest.approx(3*result+7,abs=1e-9)
    with pytest.raises(ValueError):C.catoni_with_bound([1,2,3],.001,1)


def test_tukey_break_even_matches_direct_asymptotic_variances():
    e=optimize.brentq(lambda t:C.tukey_efficiency(t)-1,0,.01)
    mixture=lambda x:(1-e)*stats.norm.pdf(x)+e*stats.norm.pdf(x,scale=3)
    delta=integrate.quad(lambda x:abs(x)*mixture(x),-np.inf,np.inf)[0]
    variance=1+8*e;fourth=3+240*e
    cv_sd=(fourth/variance**2-1)/4
    cv_abs=variance/delta**2-1
    assert cv_sd/cv_abs==pytest.approx(1,rel=1e-9)
    assert .0017<e<.0019
