"""Independent numerical/reference checks for the Part 35 examples."""
import math
import numpy as np
import pytest
from scipy import integrate, stats
from explainer.stats.kit import causal as CA
from explainer.stats.world import World
from videos.stats.stats35 import compute as C


def test_exact_pilot_matches_scipy_enumeration():
    d=C.load('fisher');y=np.array(d['y']);z=np.array(d['z'])
    # SciPy defines two-sided tails differently; use the same absolute statistic
    # with a one-sided permutation tail to compare the randomization question.
    ref=stats.permutation_test((y[z],y[~z]),lambda a,b: abs(a.mean()-b.mean()),
                              permutation_type='independent',n_resamples=np.inf,alternative='greater')
    assert len(ref.null_distribution)==math.comb(12,6)
    assert d['p']==pytest.approx(ref.pvalue,abs=1e-13)
    assert d['ci_enumerated'] and d['big_p']==pytest.approx((1+d['big_extreme'])/(1+d['big_reps']))


def test_two_look_crossing_matches_scalar_conditional_normal_integral():
    c=stats.norm.ppf(.975);rho=math.sqrt(.5);sd=math.sqrt(1-rho*rho)
    inside=integrate.quad(lambda x:stats.norm.pdf(x)*(stats.norm.cdf((c-rho*x)/sd)
                          -stats.norm.cdf((-c-rho*x)/sd)),-c,c,epsabs=1e-13)[0]
    assert C.crossing_probs([c,c]).sum()==pytest.approx(1-inside,abs=2e-12)


def test_sequential_boundaries_converge_and_match_published_values():
    a=C.sequential_boundaries(nodes=80);b=C.sequential_boundaries(nodes=160)
    for x,y in zip(a,b):np.testing.assert_allclose(x,y,atol=2e-10,rtol=0)
    assert b[0]==pytest.approx(2.4132,abs=.00005)
    np.testing.assert_allclose(b[1],[4.5617,3.2256,2.6337,2.2809,2.0401],atol=.00005)
    np.testing.assert_allclose(b[2],[4.8769,3.3570,2.6803,2.2898,2.0310],atol=.00005)
    assert C.crossing_probs([b[0]]*5).sum()==pytest.approx(.05,abs=1e-10)


def test_subgroup_contrast_changes_sign_when_subgroup_and_complement_swap():
    n0=np.array([700,7700]);n1=np.array([710,7690])
    z=C.subgroup_interaction_z([95,900],n0,[65,720],n1)
    assert z[0]==pytest.approx(-z[1],abs=1e-12)
    # Under a common risk difference, its repeated-sampling scale is one.
    g=np.random.default_rng(83);values=[]
    for _ in range(12000):
        a=g.binomial(n0,.118);b=g.binomial(n1,.094)
        values.append(C.subgroup_interaction_z(a,n0,b,n1)[0])
    assert np.std(values,ddof=1)==pytest.approx(1,abs=.025)
    assert np.mean(np.abs(values)>1.96)==pytest.approx(.05,abs=.006)


def test_unadjusted_school_icc_includes_shared_background():
    w=World();d=C.load('cluster')
    # Write the score as a common school component plus independent pupil noise.
    common_var=.35**2+(.45*.45)**2
    individual_var=.85**2+(.30*.9)**2
    assert d['icc']==pytest.approx(common_var/(common_var+individual_var))
    assert d['deff']==pytest.approx(1+(d['mean_size']-1)*d['icc'])
    assert d['effect']==20


def test_interference_truth_is_exact_average_of_fixed_potential_outcomes():
    w=World();d=C.load('interfere');e=w.epidemic
    for key,s in [('0',.3),('1',.7)]:
        p=e['rate'][e['town']]*(1-.6*s)
        y0=(e['u']<p).mean();y1=(e['u']<.4*p).mean()
        assert d['truth'][key]['y0']==pytest.approx(y0)
        assert d['truth'][key]['y1']==pytest.approx(y1)
        assert d['truth'][key]['all']==pytest.approx((1-s)*y0+s*y1)


def test_board_uses_nominal_reference_mc_uncertainty():
    d=C.load('board')
    assert len(d['rows'])==11
    for row in d['rows']:
        assert row['reps'] in (1000,4000,20000)
        assert row['se']==pytest.approx(math.sqrt(row['nominal']*(1-row['nominal'])/row['reps']))
