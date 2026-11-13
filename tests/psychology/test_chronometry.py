"""Psyche's stage models of reaction time (Part 1) against their closed forms."""

import numpy as np
import pytest

from explainer.psychology.psyche import chronometry as ch


def test_moments_are_those_of_summed_gammas():
    m = ch.donders_models()["b"]
    x = m.sample(400_000, np.random.default_rng(1))
    assert x.mean() == pytest.approx(m.mean, rel=2e-3)
    assert x.var() == pytest.approx(m.var, rel=2e-2)
    assert ((x - x.mean()) ** 3).mean() == pytest.approx(m.third, rel=6e-2)
    assert m.mean == pytest.approx(284.0) and ch.donders_models()["c"].mean == pytest.approx(237.0)


def test_density_integrates_and_matches_a_histogram():
    m = ch.donders_models()["c"]
    t = np.linspace(80, 600, 2081)
    p = m.pdf(t)
    assert np.trapezoid(p, t) == pytest.approx(1.0, abs=1e-4)
    assert np.trapezoid(p * t, t) == pytest.approx(m.mean, abs=0.05)
    x = m.sample(300_000, np.random.default_rng(2))
    h, e = np.histogram(x, bins=np.linspace(150, 400, 51), density=True)
    assert np.abs(m.pdf((e[1:] + e[:-1]) / 2) - h).max() < 0.04 * h.max()


def test_a_single_gamma_density_is_exact():
    from scipy import stats

    s = ch.Stage("x", 120.0, 0.5)
    t = np.linspace(1, 500, 400)
    assert np.allclose(ch.StageModel((s,)).pdf(t), stats.gamma.pdf(t, 4, scale=30), atol=2e-5)


def test_subtraction_recovers_the_inserted_stages():
    M = ch.donders_models(discriminate=36, choose=47)
    rng = np.random.default_rng(3)
    out = ch.subtraction(*(M[k].sample(20_000, rng) for k in "abc"))
    assert abs(out["discriminate"] - 36) < 4 * out["discriminate_se"]
    assert abs(out["choose"] - 47) < 4 * out["choose_se"]


def test_two_models_with_the_same_means_disagree_about_the_stages():
    pure, prepared = ch.donders_models(), ch.prepared_models()
    for k in "abc":
        assert pure[k].mean == pytest.approx(prepared[k].mean)
    stage = {s.name: s.mean for s in prepared["b"].stages}
    assert stage["choose"] != pytest.approx(47.0) and stage["discriminate"] != pytest.approx(36.0)


def test_insertion_test_accepts_insertion_and_rejects_a_changed_stage():
    rng = np.random.default_rng(4)
    M = ch.donders_models()
    ok = ch.insertion_test(M["a"].sample(6000, rng), M["c"].sample(6000, rng), n_boot=400)
    assert ok["z_var"] < 2 and ok["stage_cv"] == pytest.approx(0.6, abs=0.08)
    # a "longer" task whose other stages became less variable: its variance is below the shorter task's
    quiet = M["a"].with_stage("sense", cv=0.02).with_stage("respond", cv=0.02).insert(
        ch.Stage("extra", 30.0, 0.1), before="respond")
    bad = ch.insertion_test(M["a"].sample(6000, rng), quiet.sample(6000, rng), n_boot=400)
    assert bad["d_mean"] > 0 and bad["z_var"] > 5


def test_additive_factors():
    b = ch.donders_models()["b"]
    assert ch.interaction(ch.factorial_means(b, "sense", 1.3, "choose", 1.6)) == pytest.approx(0.0, abs=1e-9)
    same = ch.interaction(ch.factorial_means(b, "choose", 1.3, "choose", 1.6))
    assert same == pytest.approx(47 * 0.3 * 0.6)


def test_hick_fit_recovers_a_planted_law():
    n = np.arange(1, 11)
    fit = ch.hick_fit(n, ch.hick(n, 180.0, 150.0))
    assert fit["intercept"] == pytest.approx(180.0) and fit["per_bit"] == pytest.approx(150.0)
    assert fit["r2"] == pytest.approx(1.0)


def test_exgaussian_density_and_fit():
    t = np.linspace(-200, 3000, 64001)
    assert np.trapezoid(ch.exgauss_pdf(t, 300, 30, 80), t) == pytest.approx(1.0, abs=1e-6)
    x = ch.exgauss_sample(20_000, 300, 30, 80, np.random.default_rng(5))
    fit = ch.fit_exgauss(x)
    assert fit["mu"] == pytest.approx(300, abs=3) and fit["sigma"] == pytest.approx(30, abs=3)
    assert fit["tau"] == pytest.approx(80, abs=4)


def test_helmholtz_arithmetic():
    assert ch.conduction_speed(50, 0.0020) == pytest.approx(25.0)
    assert ch.conduction_speed(60, 0.0014) == pytest.approx(42.857, abs=1e-3)
