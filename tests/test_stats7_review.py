"""Independent reference checks for the Part 7 numerical examples."""
from fractions import Fraction
from itertools import combinations, permutations
from math import comb, factorial

import numpy as np
import pytest
from scipy.integrate import quad
from scipy import stats

from videos.stats.stats7 import compute


def test_inverse_histogram_retains_tail_mass_and_quantile_mapping():
    d = compute.compute_inverse()
    u = compute.PCG32(11).random(4000)
    draws = stats.expon.ppf(u)
    np.testing.assert_allclose(d['x'], draws[:60], rtol=1e-12)
    expected = np.histogram(draws, d['edges'])[0] / (4000 * np.diff(d['edges']))
    np.testing.assert_allclose(d['hist'], expected)
    assert np.dot(d['hist'], np.diff(d['edges'])) < 1


def test_box_muller_keeps_finite_unclamped_pairs_and_tail_mass():
    d = compute.compute_special()
    z = np.column_stack((d['z1'], d['z2']))[:600]
    np.testing.assert_allclose((z*z).sum(1), -2*np.log(d['u1']), atol=1e-14)
    assert np.isfinite(z).all()
    assert np.max(np.abs(z)) < 4.5  # actual viewport contains every animated pair
    assert np.dot(d['gamma_hist'], np.diff(np.linspace(0,10,41))) < 1


def test_monte_carlo_and_grid_use_identical_actual_budgets():
    d = compute.compute_montecarlo()
    b = d['ball']
    for dim, volume, budget, relative_se in zip(b['d'], b['true'], b['grid_n'], b['mc_err']):
        side = round(1_000_000 ** (1/dim))
        assert budget == side**dim
        hit_probability = volume / 2**dim
        expected = np.sqrt(hit_probability*(1-hit_probability)/budget)/hit_probability
        assert relative_se == pytest.approx(expected)
    assert b['mc_err'][0] == 0
    assert d['est_n'][-1] == 4000
    g = compute.PCG32(31)
    x,y = g.random(4000),g.random(4000)
    assert d['est'][-1] == pytest.approx(4*np.mean(x*x+y*y <= 1))


def test_population_control_is_unbiased_with_claimed_optimal_variance():
    b = 6*(3-np.e)
    mean = np.e-1
    cov = quad(lambda u: (np.exp(u)-mean)*(u-.5),0,1)[0]
    assert b == pytest.approx(cov/(1/12))
    expectation = quad(lambda u: np.exp(u)-b*(u-.5),0,1)[0]
    assert expectation == pytest.approx(mean)
    plain_variance = quad(lambda u:(np.exp(u)-mean)**2,0,1)[0]
    controlled_variance = quad(lambda u:(np.exp(u)-b*(u-.5)-mean)**2,0,1)[0]
    assert controlled_variance == pytest.approx(plain_variance-cov**2/(1/12))


def test_forward_riffle_formula_requires_descents_of_inverse_deck():
    n=4
    counts={p:Fraction(0) for p in permutations(range(n))}
    for cut in range(n+1):
        # Every packet-interleaving has probability 2^-n after binomial cutting.
        for left_positions in combinations(range(n),cut):
            left=iter(range(cut));right=iter(range(cut,n))
            positions=set(left_positions)
            deck=tuple(next(left) if i in positions else next(right) for i in range(n))
            counts[deck] += Fraction(1,2**n)
    eulerian=compute.eulerian_row(n)
    groups=[0]*n
    for deck, probability in counts.items():
        inverse=np.argsort(deck)
        r=1+np.count_nonzero(np.diff(inverse)<0)
        groups[r-1]+=1
        assert probability == Fraction(comb(2+n-int(r),n),2**n)
    assert groups == eulerian
    exact_tv=sum(abs(p-Fraction(1,factorial(n))) for p in counts.values())/2
    grouped_tv=sum(a*abs(Fraction(comb(2+n-r,n),2**n)-Fraction(1,factorial(n))) for r,a in enumerate(eulerian,1))/2
    assert exact_tv == grouped_tv
