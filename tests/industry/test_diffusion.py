"""The Bass diffusion model (Part 7): its shape, its peak and a fit that recovers known parameters."""

import numpy as np

from explainer.industry.works.diffusion import bass, early_forecast, fit_bass, peak_year


def test_bass_is_an_s_curve_to_its_ceiling():
    t = np.arange(0, 80)
    f = bass(t, 0.02, 0.4, 0.8)
    assert f[0] == 0 and abs(f[-1] - 0.8) < 1e-6
    assert np.all(np.diff(f) > 0)
    new = np.diff(f)
    assert abs(np.argmax(new) + 0.5 - peak_year(0.02, 0.4)) < 1.0  # most new adopters near ln(q/p)/(p+q)


def test_fit_recovers_known_parameters():
    t = np.arange(0, 30)
    s = 100 * bass(t, 0.02, 0.4, 0.85)
    f = fit_bass(t + 1980, s)
    assert abs(f["p"] - 0.02) < 0.003 and abs(f["q"] - 0.4) < 0.02 and abs(f["m"] - 85) < 1 and f["rmse"] < 0.1


def test_early_forecast_needs_enough_points():
    t = np.arange(0, 30)
    s = 100 * bass(t, 0.02, 0.4, 0.85)
    e = early_forecast(t + 1980, s, 25)
    assert e is not None and e["cut"] < 1980 + 30
    assert early_forecast(t[:3] + 1980, s[:3], 25) is None


def test_fixed_ceiling_fit_recovers_the_truth_and_shows_the_early_fan():
    from explainer.industry.works.diffusion import bass, fit_bass_fixed_m
    yrs = np.arange(1960, 1990, dtype=float)
    s = bass(yrs - 1958, 0.02, 0.45, 80.0)
    f = fit_bass_fixed_m(yrs, s, 80.0)
    assert abs(f["p"] - 0.02) < 2e-3 and abs(f["q"] - 0.45) < 2e-2 and f["rmse"] < 1e-3
    # on the first few years only, a wrong ceiling still fits closely: the early points cannot pin m down
    early = yrs < 1964
    wrong = fit_bass_fixed_m(yrs[early], s[early], 40.0)
    assert wrong["rmse"] < 0.5
