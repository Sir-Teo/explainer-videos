"""Independent numerical checks for the Part 40 teaching studies."""
import math
import numpy as np
import pytest
from scipy.integrate import quad
from scipy.stats import gamma
from statsmodels.duration.survfunc import SurvfuncRight
from explainer.stats.kit import survival as SV
from videos.stats.stats40 import compute as C


def test_delayed_entry_matches_independent_statsmodels_risk_sets():
    cohort = dict(age=np.full(20, 60), male=np.zeros(20), sbp=np.full(20, 130.), bmi=np.full(20, 27.))
    d = C.delayed_entry_sample(cohort, np.random.default_rng(1), population=30_000, observed=3000)
    assert np.all(d['exit'] > d['entry'])
    assert np.all(d['exit'] - d['entry'] <= 15 + 1e-12)
    ours = SV.kaplan_meier(d['exit'], d['event'], entry=d['entry'])
    reference = SurvfuncRight(d['exit'], d['event'], entry=d['entry'])
    np.testing.assert_allclose(ours['t'], reference.surv_times)
    np.testing.assert_allclose(ours['surv'], reference.surv_prob, atol=1e-12)
    ages = np.arange(45, 90)
    truth = np.array([np.mean(d['lifetime'] > a) for a in ages])
    adjusted = SV.km_at(ours, ages)
    naive = SV.km_at(SV.kaplan_meier(d['exit'], d['event']), ages)
    assert np.max(np.abs(adjusted - truth)) < .05
    assert np.max(naive - truth) > .1


def test_sixty_year_old_survival_matches_gamma_quadrature():
    d = C.compute_life()
    W = C.World()
    for t in (5., 15., 25.):
        r1 = .006 * np.exp(W.CVD_SBP * (130 - 140) + W.CVD_MALE)
        r2 = .006 * np.exp(W.OTHER_MALE)
        h1 = r1 * np.expm1(W.CVD_GOMPERTZ * t) / W.CVD_GOMPERTZ
        h2 = r2 * np.expm1(W.OTHER_GOMPERTZ * t) / W.OTHER_GOMPERTZ
        integral = quad(lambda z: np.exp(-z*h1-h2) * gamma.pdf(z, 1/W.FRAILTY_VAR, scale=W.FRAILTY_VAR), 0, np.inf)[0]
        assert d['S60'][int(t*4)] == pytest.approx(integral, abs=1e-10)
    m = d['median60']
    h1 = .006*np.exp(-.2+W.CVD_MALE)*np.expm1(W.CVD_GOMPERTZ*m)/W.CVD_GOMPERTZ
    h2 = .006*np.exp(W.OTHER_MALE)*np.expm1(W.OTHER_GOMPERTZ*m)/W.OTHER_GOMPERTZ
    assert (1+W.FRAILTY_VAR*h1)**(-1/W.FRAILTY_VAR)*np.exp(-h2) == pytest.approx(.5, abs=1e-12)


def test_counting_compensator_is_exact_integrated_exposure():
    d = C.compute_counting()
    g = C.rng(4002)
    times = np.minimum(g.exponential(1., 50), g.uniform(0, 2.5, 50))
    for i in (1, 57, 144, 250):
        horizon = d['grid'][i]
        intervals = np.unique(np.r_[0, times[times < horizon], horizon])
        expected = sum((b-a)*np.sum(times > (a+b)/2) for a,b in zip(intervals[:-1], intervals[1:]))
        assert d['Lam'][i] == pytest.approx(expected, abs=1e-12)
    assert sum(d['hist']) + d['M_outside_hist'] == 4000


def test_calibration_mc_se_preserves_independent_dataset_count():
    per_dataset = np.array([.7, .9, .8, 1.])
    expected = math.sqrt(sum((x-per_dataset.mean())**2 for x in per_dataset)/(len(per_dataset)*(len(per_dataset)-1)))
    assert C.mean_mc_se(per_dataset) == pytest.approx(expected, rel=1e-15)
