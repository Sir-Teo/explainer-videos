"""Reference checks for the Part 43 limit-law lab."""
import numpy as np
from numpy.testing import assert_allclose
from scipy import stats, optimize
from scipy.integrate import quad
from videos.stats.stats43 import compute as C


def test_return_aggregation_discards_incomplete_final_blocks():
    data=np.arange(1.,24.)
    assert_allclose(C.aggregate_returns(data,5),[15.,40.,65.,90.])
    assert_allclose(C.aggregate_returns(data,20),[210.])


def test_lattice_distances_have_independent_point_mass_reference():
    result=C.normal_lattice_distances([0.],[1.])
    assert_allclose(result['wasserstein'],np.sqrt(2/np.pi),atol=1e-14)
    assert_allclose(result['levy'],optimize.brentq(lambda e:stats.norm.sf(e)-e,0,1),atol=1e-12)
    assert_allclose(result['ky_fan'],optimize.brentq(lambda e:2*stats.norm.sf(e)-e,0,1),atol=1e-12)


def test_lattice_wasserstein_against_independent_normal_cell_quadrature():
    atoms=np.array([-2.,-.1,.6,3.])
    p=np.array([.1,.2,.5,.2])
    edges=stats.norm.ppf(np.r_[0.,np.cumsum(p)])
    ref=0.
    for i,a in enumerate(atoms):
        ref+=quad(lambda z:abs(a-z)*stats.norm.pdf(z),edges[i],edges[i+1],epsabs=1e-11)[0]
    result=C.normal_lattice_distances(atoms,p)
    assert_allclose(result['wasserstein'],ref,atol=1e-8)
    assert result['levy']<=result['ky_fan']


def test_urn_inclusive_integer_boundaries_against_enumeration():
    for n in [2,25,50,100,125]:
        k=np.arange(n+1)
        # Multiply by 50n: equality is kept exactly at integer boundary.
        outside=np.abs(50*k-30*n)>=n
        ref=stats.binom.pmf(k,n,.6)[outside].sum()
        assert_allclose(C.urn_tail(n),ref,atol=1e-14)
    certificate=C.urn_sizes(1/1001)
    safe=certificate['safe_from']
    assert C.urn_tail(safe-1)>1/1001
    assert np.max(C.urn_tail(np.arange(safe,certificate['checked_through']+1)))<=1/1001


def test_maximum_supremum_matches_independent_exponential_stationary_point():
    for n in [10,100,1000]:
        # derivative vanishes when (1-t/n)^(n-1)=exp(-t).
        root=optimize.brentq(lambda t:(n-1)*np.log1p(-t/n)+t,.01,min(n-.001,10.))
        reference=np.exp(-root)-(1-root/n)**n
        assert_allclose(C.maximum_distance('exponential',n),reference,atol=1e-12)
        assert_allclose(C.maximum_distance('pareto',n),reference,atol=1e-12)


def test_viewport_histogram_preserves_omitted_tail_mass():
    density,edges=C.histogram_density(np.array([-10.,.1,.2,.8,10.]),bins=2,range=(0.,1.))
    assert_allclose(np.sum(density*np.diff(edges)),3/5)
