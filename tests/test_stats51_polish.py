"""Independent edge cases for the probability guarantees presented in Part 51."""
import math
import numpy as np
import pytest
from scipy import optimize, stats
from videos.stats.stats51 import compute as C


def test_chernoff_closed_support_endpoint():
    assert C.chernoff_binomial([.6], 5, .4)[0] == pytest.approx(.4**5)
    assert C.chernoff_binomial([.61], 5, .4)[0] == 0
    assert np.array_equal(C.chernoff_binomial([0,.01],5,0),[1,0])
    assert np.array_equal(C.chernoff_binomial([0,.01],5,1),[1,0])


def test_exact_lattice_tail_without_threshold_fudge():
    t = .25
    assert C.binomial_mean_tail([t],4,.25)[0] == pytest.approx(stats.binom.sf(1,4,.25))
    assert C.binomial_mean_tail([np.nextafter(t,np.inf)],4,.25)[0] == pytest.approx(stats.binom.sf(2,4,.25))


def test_chernoff_dominates_enumerated_tail():
    for p in (.02,.3,.5,.9):
        # thresholds chosen from actual lattice probabilities, plus the support endpoint
        t = np.unique(np.r_[np.arange(21)/20-p,1-p])
        t = t[t>=0]
        assert np.all(C.binomial_mean_tail(t,20,p)<=C.chernoff_binomial(t,20,p)+1e-13)


def test_jl_all_pairs_failure_probability():
    for N in (2,200,10000):
        for eps in (.1,.3,1):
            k = C.jl_dimension_confidence(N,eps,.05)
            assert N*(N-1)*math.exp(-k*eps**2/8)<=.05


def test_exact_cone_projection_against_scalar_optimization():
    r=np.random.default_rng(913)
    g=r.normal(size=(35,11))
    # The convex objective is checked by independent bounded scalar minimization.
    for s in (1,4,11):
        got=C.l1_polar_distance_squared(g,s)
        want=[]
        for row in g:
            f=lambda t: ((row[:s]-t)**2).sum()+(np.maximum(abs(row[s:])-t,0)**2).sum()
            fit=optimize.minimize_scalar(f,bounds=(0,20),method='bounded',options={'xatol':1e-12})
            want.append(min(f(0),fit.fun))
        assert np.allclose(got,want,atol=1e-9,rtol=1e-9)


def test_one_dimensional_cone_and_full_support_halfspace():
    g=np.array([[-3.],[2.],[0.]])
    assert np.array_equal(C.l1_polar_distance_squared(g,1),[9,0,0])
    r=np.random.default_rng(38);g=r.normal(size=(20000,7))
    d=C.l1_polar_distance_squared(g,7)
    expected=np.sum(g*g,axis=1)-np.maximum(g.sum(axis=1),0)**2/7
    assert np.allclose(d,expected)
    assert abs(d.mean()-6.5)<5*d.std(ddof=1)/math.sqrt(len(d))


def test_basis_pursuit_solver_failure_is_not_a_recovery_failure(monkeypatch):
    from types import SimpleNamespace
    monkeypatch.setattr(C.optimize,'linprog',lambda *a,**k:SimpleNamespace(success=False,message='numerical failure'))
    with pytest.raises(RuntimeError,match='numerical failure'):
        C.checked_basis_pursuit(np.eye(2),np.ones(2))


def test_basis_pursuit_feasible_unique_example():
    A=np.array([[1.,0.,.2],[0.,1.,.3]])
    x=C.checked_basis_pursuit(A,np.array([1.,0.]))
    assert np.allclose(x,[1,0,0],atol=1e-8)


def test_empirical_bernstein_uses_unbiased_sample_variance():
    m=np.array([0,.02,.5,1])
    w=C.interval_halfwidths(m)[2]
    expected=np.sqrt(2*m*(1-m)*200/199*math.log(80)/200)+7*math.log(80)/(3*199)
    assert np.allclose(w,expected)


def test_distribution_free_intervals_against_all_binomial_outcomes():
    k=np.arange(201);m=k/200
    for p in np.linspace(0,1,301):
        for half in C.interval_halfwidths(m)[1:]:
            coverage=stats.binom.pmf(k,200,p)[abs(m-p)<=half].sum()
            assert coverage>=.95-1e-13


def test_empirical_orlicz_log_domain_known_laws():
    assert C.psi_norm_empirical(np.array([-1.,1.]),2)==pytest.approx(1/math.sqrt(math.log(2)))
    assert C.psi_norm_empirical(np.zeros(4),1)==0
    x=np.array([0,1.,10000.])
    norm=C.psi_norm_empirical(x,2)
    assert np.exp((x/norm)**2).mean()==pytest.approx(2)
