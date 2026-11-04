import numpy as np
import pytest

from explainer.stats.kit.estimation import (TANK_ESTIMATORS, capture, mom_sd, newton, observed_information, tank_game,
                                            umvue_sd)


def test_capture_rows_are_distinct_and_in_range():
    rng = np.random.Generator(np.random.PCG64(1))
    s = capture(rng, 50, 7, 500)
    assert s.shape == (500, 7)
    assert s.min() >= 1 and s.max() <= 50
    assert all(len(set(r)) == 7 for r in s)
    # each serial equally likely: the mean serial is (N + 1)/2
    assert abs(s.mean() - 25.5) < 0.5


def test_capture_offset_and_weights():
    rng = np.random.Generator(np.random.PCG64(2))
    s = capture(rng, 20, 3, 200, offset=1000)
    assert s.min() >= 1001 and s.max() <= 1020
    w = capture(rng, 20, 3, 2000, weights=np.linspace(1, 3, 20))
    assert w.mean() > 10.5 + 1.0  # newer (higher) serials favoured


@pytest.mark.parametrize("name", ["mom", "umvue", "range"])
def test_unbiased_estimators_are_unbiased(name):
    r = tank_game(TANK_ESTIMATORS[name], N=300, k=6, reps=40_000, seed=3)
    assert abs(r["bias"]) < 4 * r["bias_mcse"] + 0.5


def test_max_is_biased_low_and_umvue_wins():
    rs = {n: tank_game(f, N=300, k=6, reps=20_000, seed=4) for n, f in TANK_ESTIMATORS.items()}
    assert rs["max"]["bias"] < -30
    assert rs["umvue"]["rmse"] < min(rs[n]["rmse"] for n in ("mom", "max", "range"))


def test_exact_sds_match_simulation():
    for k in (3, 6, 12):
        u = tank_game(TANK_ESTIMATORS["umvue"], N=300, k=k, reps=30_000, seed=k)
        m = tank_game(TANK_ESTIMATORS["mom"], N=300, k=k, reps=30_000, seed=k)
        assert u["sd"] == pytest.approx(umvue_sd(300, k), rel=0.03)
        assert m["sd"] == pytest.approx(mom_sd(300, k), rel=0.03)


def test_offset_breaks_the_textbook_estimators_but_not_range():
    u = tank_game(TANK_ESTIMATORS["umvue"], model="offset", reps=5000, seed=5)
    r = tank_game(TANK_ESTIMATORS["range"], model="offset", reps=5000, seed=5)
    assert u["bias"] > 1000
    assert abs(r["bias"]) < 4 * r["bias_mcse"] + 1


def test_unknown_model():
    with pytest.raises(ValueError):
        tank_game(TANK_ESTIMATORS["max"], model="spies")


def test_newton_and_curvature_on_poisson():
    n, S = 200, 122  # Bortkiewicz's horse kicks
    path = newton(lambda l: S / l - n, lambda l: -S / l ** 2, 0.3)
    assert path[-1] == pytest.approx(0.61, abs=1e-10)
    J = observed_information(lambda l: S * np.log(l) - n * l, 0.61)
    assert J == pytest.approx(S / 0.61 ** 2, rel=1e-5)
