"""Psyche's choice module (Part 26)."""
import numpy as np
import pytest

from explainer.psychology.psyche import choice as C


def test_expected_value_and_lottery_checks():
    L = C.lottery((0.3, 100), (0.7, 0))
    assert C.ev(L) == pytest.approx(30.0)
    with pytest.raises(ValueError):
        C.lottery((0.5, 1), (0.4, 0))


def test_st_petersburg():
    assert np.allclose(C.st_petersburg_ev(5), [1, 2, 3, 4, 5])
    # log utility: the buying price solves sum 2^-k log(w - c + 2^k) = log w and rises slowly with wealth
    p = [C.st_petersburg_ce(w) for w in (10, 1_000, 1_000_000)]
    assert p[0] < p[1] < p[2] < 25
    k = np.arange(1, 200)
    assert (0.5 ** k * np.log(10 - p[0] + 2.0 ** k)).sum() == pytest.approx(np.log(10), abs=1e-9)


def test_triangle_and_parallel_lines():
    out = (0.0, 2400.0, 2500.0)
    A = C.lottery((0.33, 2500), (0.66, 2400), (0.01, 0))
    B = C.lottery((1.0, 2400))
    Cc = C.lottery((0.33, 2500), (0.67, 0))
    D = C.lottery((0.34, 2400), (0.66, 0))
    pa, pb, pc, pd = (np.array(C.triangle(L, out)) for L in (A, B, Cc, D))
    assert np.allclose(pa - pb, pc - pd)
    # any utility: EU(A) - EU(B) equals EU(C) - EU(D)
    for u in (np.sqrt, np.log1p, lambda x: x):
        assert C.eu(A, u) - C.eu(B, u) == pytest.approx(C.eu(Cc, u) - C.eu(D, u))
    assert C.eu_slope(0, 1, 1.08) == pytest.approx(12.5)


def test_weighting_functions():
    p = np.linspace(0, 1, 101)
    for w in (C.w_tk(p, 0.61), C.w_prelec(p, 0.65)):
        assert w[0] == pytest.approx(0, abs=1e-12) and w[-1] == pytest.approx(1)
        assert np.all(np.diff(w) > 0)
    assert C.w_tk(0.01, 0.61) > 0.01 and C.w_tk(0.9, 0.61) < 0.9
    assert np.allclose(C.w_tk(p, 1.0), p)


def test_cpt_reduces_and_batch_matches():
    L = C.lottery((0.2, 50), (0.5, -10), (0.3, 5))
    # no curvature, no loss aversion, linear weights: expected value
    assert C.cpt(L, 1, 1, 1, 1, 1) == pytest.approx(C.ev(L))
    lots = [L, C.lottery((1.0, 3)), C.lottery((0.5, -100), (0.5, 100))]
    P, X = C.pad(lots)
    assert np.allclose(C.cpt_batch(P, X), [C.cpt(x) for x in lots])
    # dominance: moving probability to a better outcome raises the value
    assert C.cpt(C.lottery((0.025, 100), (0.025, 99.9), (0.95, 0))) < C.cpt(C.lottery((0.05, 100), (0.95, 0)))


def test_fourfold_and_framing():
    f = C.fourfold(probs=(0.05, 0.95))
    assert f["gain_ce"][0] > 5 and f["gain_ce"][1] < 95  # seeks risk at low p, avoids it at high p
    assert f["loss_ce"][0] < -5 and f["loss_ce"][1] > -95
    fr = C.framing()
    assert fr["saved_choice"] == "sure" and fr["die_choice"] == "risky"
    assert C.ce(C.lottery((1.0, 42.0))) == pytest.approx(42.0)


def test_fit_recovers_parameters():
    rng = np.random.default_rng(3)
    lots_a, lots_b = [], []
    for _ in range(400):
        p = rng.uniform(0.05, 0.95)
        lots_a.append(C.lottery((p, rng.uniform(-50, 50)), (1 - p, rng.uniform(-50, 50))))
        q = rng.uniform(0.05, 0.95)
        lots_b.append(C.lottery((q, rng.uniform(-50, 50)), (1 - q, rng.uniform(-50, 50))))
    A, B = C.pad(lots_a), C.pad(lots_b)
    truth = np.array([0.8, 1.8, 0.65, 0.7, 0.3])
    y = C.predict("cpt", truth, A, B)
    fit = C.fit_model("cpt", A, B, y)
    assert fit["mse"] < 1e-4
    assert fit["params"]["lam"] == pytest.approx(1.8, rel=0.15)
    cv = C.cv_models(A, B, y, models=("ev", "cpt"), k=4)
    assert cv["cpt"] < cv["ev"] < cv["mean"]


def test_bayes_and_frequencies():
    assert C.bayes(0.15, 0.8, 0.2) == pytest.approx(12 / 29)
    nf = C.natural_frequencies(1000, 0.01, 0.8, 0.096)
    assert (nf["sick"], nf["true_pos"], nf["false_pos"]) == (10, 8, 95)


def test_take_the_best_wins_with_little_data():
    r = C.heuristics_cv((8, 4, 2, 1, 0.5, 0.25), (8, 80), reps=80, noise=3.0, seed=1)
    assert r["ttb"][0] > r["regression"][0]
    assert r["regression"][1] > r["regression"][0]


def test_hot_hand_bias_exact():
    assert C.streak_exact(4, 1)["expected"] == pytest.approx(17 / 42)
    assert C.streak_exact(10, 1)["expected"] < 0.5
    s = C.streak_sim(4, 1, reps=200_000, seed=2)
    assert s["expected"] == pytest.approx(17 / 42, abs=0.01)


def test_discounting_reversal():
    t = C.reversal_delay(100, 110, 4, 0.05)
    assert t == pytest.approx(20.0)
    v = lambda a, d: a * C.discount(d, k=0.05)  # noqa: E731
    assert v(100, t - 1) > v(110, t + 3) and v(100, t + 1) < v(110, t + 5)
    d = np.arange(0, 60)
    e = C.discount(d, "exponential", delta=0.97)
    assert np.allclose(e[1:] / e[:-1], 0.97)
    assert C.discount(0, "beta_delta") == 1.0 and C.discount(1, "beta_delta", beta=0.7, delta=1.0) == 0.7


def test_experience_and_sampling():
    assert C.p_never_seen(0.1, 7) == pytest.approx(0.9 ** 7)
    p = C.sample_choices(C.lottery((0.1, 32), (0.9, 0)), 3, 7, reps=50_000, seed=1)
    assert p == pytest.approx(1 - 0.9 ** 7, abs=0.01)  # risky chosen exactly when the 32 was seen
    v = C.dbs_value([0, 5, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    assert np.allclose(v, [0.0, 0.45, 0.95])


def test_battery_gambles():
    from explainer.psychology import battery
    t = battery.run("gambles", {}, 400, seed=1)
    assert len(t) == 400 and set(np.unique(t.condition)) <= {"gain", "loss", "frame_saved", "frame_die", "delay"}
    g = (t.condition == "gain") & (t.extra["p"] == 0.05) & (t.extra["sure"] >= 45)
    assert t.correct[g].mean() < 0.5  # a sure 45 or more beats 100 at 5%
