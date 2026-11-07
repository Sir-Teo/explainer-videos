"""Independent references for the Part 45 estimation examples."""
import numpy as np
from numpy.testing import assert_allclose
from scipy import stats
from scipy.integrate import quad
from scipy.optimize import minimize
from videos.stats.stats45 import compute as C
from explainer.stats import museum


def test_midrange_halfwidth_matches_order_statistic_integral():
    for n in (2,5,10):
        c=C.uniform_midrange_halfwidth(n)
        # Joint density of the min a and max b in a unit-width interval.
        # Parameterize the order statistics on [0,1], centered at 1/2.
        coverage=quad(lambda a:quad(lambda b:n*(n-1)*(b-a)**(n-2),
                     max(a,1-2*c-a),min(1,1+2*c-a))[0]
                     if min(1,1+2*c-a)>max(a,1-2*c-a) else 0.,0,1,points=[.5-c,.5+c])[0]
        assert_allclose(coverage,.9,atol=2e-8)


def test_conditional_midrange_pivot_is_uniform_at_every_range():
    g=np.random.default_rng(4921);x=g.random((120_000,5))
    width=1-(x.max(1)-x.min(1));error=(x.max(1)+x.min(1))/2-.5
    standardized=2*error/width
    for lo,hi in ((0,.3),(.3,.5),(.5,.7),(.7,1)):
        select=(width>=lo)&(width<hi);sample=standardized[select]
        assert len(sample)>1000
        assert abs(np.mean(abs(sample)<=.9)-.9)<6*np.sqrt(.09/len(sample))


def test_poisson_mixture_certificate_against_dense_directional_scores():
    counts=np.asarray(museum.INSURANCE_CLAIMS,float);fit=C.poisson_mixture(counts)
    x=np.arange(len(counts));m=stats.poisson.pmf(x[:,None],np.asarray(fit['grid'])[None,:])@fit['w']
    dense=np.linspace(0,7,15001)
    score=((counts/counts.sum())/m)@stats.poisson.pmf(x[:,None],dense[None,:])
    assert score.max()<=1+fit['kkt_gap_per_observation']+1e-10
    assert fit['loglik_gap_bound']<.001
    assert_allclose(np.sum(fit['w']),1,atol=1e-14)
    assert np.all(np.diff(fit['post_mean'])>=-1e-12)


def test_poisson_mixture_beats_independent_fixed_grid_convex_fit():
    counts=np.array([40.,12.,5.,1.]);fit=C.poisson_mixture(counts)
    atoms=np.linspace(0,3,61);L=stats.poisson.pmf(np.arange(4)[:,None],atoms[None,:])
    def objective(w):
        m=L@w
        return -np.dot(counts,np.log(m)),-(counts/m)@L
    result=minimize(objective,np.full(len(atoms),1/len(atoms)),jac=True,method='SLSQP',
                    bounds=[(0,1)]*len(atoms),constraints=[dict(type='eq',fun=lambda w:w.sum()-1)],
                    options=dict(ftol=1e-10,maxiter=2000))
    assert result.success
    assert fit['loglik']>=-result.fun-1e-6


def test_relative_scale_loss_uses_inverse_moments_not_posterior_mean():
    # Unknown normal mean with right Haar dmu dsigma/sigma, n=10 and SSE=18.
    posterior=stats.invgamma(a=4.5,scale=9.)
    inverse1=posterior.expect(lambda variance:1/variance)
    inverse2=posterior.expect(lambda variance:1/variance**2)
    assert_allclose(inverse1/inverse2,18/11,rtol=1e-10)
    assert_allclose(posterior.mean(),18/7,rtol=1e-12)
    assert abs(posterior.mean()-inverse1/inverse2)>.5


def test_oracle_population_risk_equals_independent_two_component_loss_integral():
    def estimate(x):
        odds=np.exp(np.clip(4*x-8,-700,700))/9
        return 4*odds/(1+odds)
    direct=.9*quad(lambda x:estimate(x)**2*stats.norm.pdf(x),-15,15,epsabs=1e-11)[0]
    direct+=.1*quad(lambda x:(estimate(x)-4)**2*stats.norm.pdf(x-4),-15,20,epsabs=1e-11)[0]
    assert_allclose(C.oracle_normal_risk(),direct,atol=1e-11)


def test_coverage_error_uses_actual_conditionally_selected_runs():
    hits=np.array([True,True,False,True,False])
    row=C.coverage_row('reference','five independent instrument-selected samples',hits)
    assert row.reps==5
    assert_allclose(row.mc_se,stats.sem(hits.astype(float)),atol=1e-15)


def test_pitman_integral_includes_peaks_outside_a_median_window():
    samples=[np.array([-2.,-.7,.1,.3,4.]),np.array([-100.,-.2,.4,1.1,30.])]
    for sample in samples:
        for name,logf in [('normal',lambda z:-z*z/2),('Laplace',lambda z:-abs(z)),('Cauchy',lambda z:-np.log1p(z*z))]:
            center=np.median(sample)
            offset=np.sum(logf(sample-center))
            density=lambda t:np.exp(np.sum(logf(sample-t))-offset)
            den=quad(density,-np.inf,np.inf,epsabs=1e-10,limit=500)[0]
            num=quad(lambda t:(t-center)*density(t),-np.inf,np.inf,epsabs=1e-10,limit=500)[0]
            reference=center+num/den
            computed=C.pitman_estimate(sample,name)
            assert_allclose(computed,reference,atol=4e-4)
