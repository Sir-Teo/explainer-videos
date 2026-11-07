"""Independent numerical checks for the comprehensive-exam examples."""
import numpy as np
from numpy.testing import assert_allclose
from scipy import stats
from videos.stats.stats42 import compute as C


def test_classical_partial_r2_matches_reduced_rss():
    g = np.random.default_rng(731)
    x = g.normal(size=(180, 3))
    X = np.column_stack([np.ones(len(x)), x])
    y = x @ [1., -.4, .7] + (1 + x[:, 0]**2)*g.normal(size=len(x))
    b, se, residual, df = C.ols(y, X, classical=True)
    reduced = np.delete(X, 2, axis=1)
    er = y - reduced @ np.linalg.lstsq(reduced, y, rcond=None)[0]
    r2 = ((er@er) - (residual@residual))/(er@er)
    assert_allclose(C.CA.partial_r2(b[2]/se[2], df), r2, rtol=1e-12)
    # A heteroskedasticity-robust t is not this geometric identity.
    br, sr, _, _ = C.ols(y, X)
    assert abs(C.CA.partial_r2(br[2]/sr[2], df)-r2) > .001


def test_full_hierarchical_posterior_against_dense_transformed_grid():
    _, y, sigma = C.museum.eight_schools()
    r = C.eight_schools_posterior(y, sigma)
    # Independent integration on tau=tan(u), not the implementation's adaptive tau quadrature.
    u = np.linspace(0., np.pi/2-1e-5, 120001)
    tau = np.tan(u)
    variance = sigma[None, :]**2 + tau[:, None]**2
    precision = 1/variance
    mu = (precision*y).sum(1)/precision.sum(1)
    logp = -.5*np.log(variance).sum(1) - .5*np.log(precision.sum(1)) - .5*((y-mu[:, None])**2/variance).sum(1)
    measure = np.exp(logp-logp.max())/(np.cos(u)**2)
    normalizer = np.trapezoid(measure, u)
    theta_a = (tau**2*y[0]+sigma[0]**2*mu)/(tau**2+sigma[0]**2)
    reference = np.trapezoid(measure*theta_a, u)/normalizer
    assert_allclose(r['theta'][0], reference, atol=1e-7)
    assert r['mass_above_30'] > .001
    assert_allclose(r['tau_mean'], np.trapezoid(measure*tau,u)/normalizer, atol=1e-6)


def test_board_preserves_actual_replications_and_empirical_mcse():
    hit = np.array([0., 0., 1., 1., 1.])
    row = C.coverage_row('example', 'five datasets', hit)
    assert row.reps == 5
    assert_allclose(row.achieved, .6)
    assert_allclose(row.se, np.sqrt(.6*.4/4))
    assert C.coverage_row('failure', 'five datasets', np.zeros(5)).verdict == 'broken'


def test_cluster_t_agrees_with_independent_equal_variance_t_test():
    z, baseline, y = C.trial_draw(C.rng(914), k_arm=12, m=20)
    result = C.analyse_trial(z, baseline, y)['t']
    cluster_means = y.mean(1)
    reference = stats.ttest_ind(cluster_means[z], cluster_means[~z], equal_var=True)
    assert_allclose(result[0]/result[1], reference.statistic)
    interval = reference.confidence_interval(confidence_level=.9)
    assert_allclose(result[2:], [interval.low, interval.high])


def test_beetle_irls_matches_independent_statsmodels_binomial_fit():
    import statsmodels.api as sm
    x, n, killed = C.museum.bliss()
    design = sm.add_constant(x)
    reference = sm.GLM(np.column_stack([killed, n-killed]), design, family=sm.families.Binomial()).fit(tol=1e-12)
    result = C.compute_p_irls()
    assert_allclose(result['b'], reference.params, atol=1e-7, rtol=0)
    assert_allclose(result['se'], reference.bse, atol=1e-6, rtol=0)
