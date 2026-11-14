"""Psyche's genes module against closed forms and its own planted answers."""

import math

import numpy as np
import pytest

from explainer.psychology.psyche import genes as G


def rng(seed):
    return np.random.default_rng(seed)


def test_one_locus_gives_three_classes_and_many_give_a_bell():
    k, p = G.allele_sum(1)
    assert list(k) == [0, 1, 2] and p == pytest.approx([0.25, 0.5, 0.25])
    k, p = G.allele_sum(50)
    assert p.sum() == pytest.approx(1.0) and k[p.argmax()] == 50
    mean, var = (k * p).sum(), ((k - 50) ** 2 * p).sum()
    assert mean == pytest.approx(50.0) and var == pytest.approx(25.0)


def test_twins_recover_the_planted_components():
    d = G.twin_study(30_000, 30_000, 0.5, 0.2, 0.3, rng=rng(1))
    assert d.r_mz == pytest.approx(0.7, abs=0.015) and d.r_dz == pytest.approx(0.45, abs=0.02)
    f = G.falconer(d.r_mz, d.r_dz)
    assert f["h2"] == pytest.approx(0.5, abs=0.05) and f["c2"] == pytest.approx(0.2, abs=0.05)
    fit = G.ace_fit(d)
    assert fit["a2"] == pytest.approx(0.5, abs=0.04) and fit["c2"] == pytest.approx(0.2, abs=0.04)
    assert fit["a2"] + fit["c2"] + fit["e2"] == pytest.approx(1.0)


def test_falconer_is_the_textbook_arithmetic():
    f = G.falconer(0.86, 0.60)
    assert f["h2"] == pytest.approx(0.52) and f["c2"] == pytest.approx(0.34) and f["e2"] == pytest.approx(0.14)
    assert G.falconer_se(0.7, 0.45, 100, 100) > 3 * G.falconer_se(0.7, 0.45, 1000, 1000) * 0.99


def test_each_broken_assumption_moves_the_estimate_the_way_theory_says():
    base = dict(a2=0.5, c2=0.2, e2=0.3)
    f = lambda **kw: G.falconer(*(lambda d: (d.r_mz, d.r_dz))(G.twin_study(30_000, 30_000, **{**base, **kw})))  # noqa: E731
    assert f(mz_extra=0.5, rng=rng(2))["h2"] > 0.7            # identical twins treated more alike: h2 too high
    a = f(assort=0.5, rng=rng(3))
    assert a["h2"] < 0.5 and a["c2"] > 0.22                   # assortative mating: h2 too low, c2 too high
    d = G.twin_study(30_000, 30_000, 0.3, 0.0, 0.3, d2=0.4, rng=rng(4))
    fd = G.falconer(d.r_mz, d.r_dz)
    assert fd["h2"] > 0.7 and fd["c2"] < -0.1                 # dominance: h2 above the truth, a negative c2
    g = f(rge=0.6, rng=rng(5))
    assert g["c2"] > 0.3                                       # parents' genes in the home are read as home


def test_an_ace_fit_keeps_the_variances_non_negative():
    d = G.twin_study(4_000, 4_000, 0.3, 0.0, 0.3, d2=0.4, rng=rng(6))
    fit = G.ace_fit(d)
    assert fit["c2"] == pytest.approx(0.0, abs=1e-3) and fit["a2"] > 0.6


def test_adoption_correlations_are_c2_half_h2_and_h2():
    out = G.adoption_study(80_000, 0.5, 0.2, 0.3, rng=rng(7))
    assert out["adoptive_siblings"] == pytest.approx(0.2, abs=0.015)
    assert out["parent_child_apart"] == pytest.approx(0.25, abs=0.015)
    assert out["mz_apart"] == pytest.approx(0.5, abs=0.015)
    placed = G.adoption_study(80_000, 0.5, 0.2, 0.3, placement=0.5, rng=rng(7))
    assert placed["mz_apart"] == pytest.approx(0.6, abs=0.015)


def test_the_midparent_slope_is_the_heritability():
    mid, child = G.midparent_offspring(100_000, 0.6, 0.4, rng(8))
    assert np.polyfit(mid, child, 1)[0] == pytest.approx(0.6, abs=0.015)


def test_two_fields_differ_for_no_genetic_reason():
    f = G.two_fields(20_000, h2_within=0.9, gap=3.0, rng=rng(9))
    assert f["h2_rich"] == pytest.approx(0.9, abs=0.01) and f["h2_poor"] == pytest.approx(0.9, abs=0.01)
    assert f["gap"] == pytest.approx(3.0, abs=0.05) and abs(f["genetic_gap"]) < 0.05


def test_power_and_sample_size_agree():
    n = G.n_for_r2(0.0002)
    assert 38_000 < n < 40_500
    assert G.power_for_r2(n, 0.0002) == pytest.approx(0.8, abs=0.005)
    assert G.power_for_r2(1_000, 0.0002) < 0.08
    assert G.n_for_r2(0.0002, alpha=5e-8) > 4 * n


def test_a_flexible_analysis_of_a_null_gene_finds_something_a_third_of_the_time():
    out = [G.candidate_gene_study(600, rng(100 + i)) for i in range(600)]
    planned = np.mean([o["planned"] < 0.05 for o in out])
    anything = np.mean([o["smallest"] < 0.05 for o in out])
    assert planned == pytest.approx(0.05, abs=0.025) and 0.25 < anything < 0.5
    assert len(out[0]["p"]) == 18


def test_gwas_hits_are_real_and_grow_with_the_sample():
    X = G.simulate_genotypes(12_000, 1_000, rng(10))
    y, beta = G.polygenic_trait(X, 0.5, 100, rng(11))
    small, large = G.gwas(X[:1_500], y[:1_500]), G.gwas(X, y)
    line = 0.05 / 1_000
    hs, hl = small["p"] < line, large["p"] < line
    assert hl.sum() > 3 * max(hs.sum(), 1)
    assert (hl & (beta == 0)).sum() <= 2                        # at most a couple of false hits in a thousand tests
    assert np.corrcoef(large["beta"][beta != 0], beta[beta != 0])[0, 1] > 0.9


def test_a_polygenic_score_predicts_about_what_the_formula_says():
    X = G.simulate_genotypes(16_000, 1_000, rng(12))
    y, _ = G.polygenic_trait(X, 0.5, 1_000, rng(13))
    res = G.gwas(X[:12_000], y[:12_000])
    s = G.polygenic_score(X[12_000:], res["beta"])
    r2 = np.corrcoef(s, y[12_000:])[0, 1] ** 2
    assert r2 == pytest.approx(G.expected_r2(12_000, 1_000, 0.5), abs=0.05)
    assert G.expected_r2(10 ** 9, 1_000, 0.5) == pytest.approx(0.5, abs=1e-3)


def test_within_family_estimates_drop_the_nurture_and_the_stratification():
    out = G.sibling_design(200_000, rng(14), direct=0.3, nurture=0.4)
    assert out["within"] == pytest.approx(0.3, abs=0.01) and out["population"] == pytest.approx(0.5, abs=0.01)
    assert out["ratio"] == pytest.approx(0.6, abs=0.03)
    strat = G.sibling_design(200_000, rng(15), direct=0.3, nurture=0.0, strata_gap=1.0, strata_env=1.0)
    assert strat["within"] == pytest.approx(0.3, abs=0.01) and strat["population"] > 0.45


def test_stratification_makes_an_association_out_of_nothing():
    out = G.stratified_association(6_000, rng(16))
    assert out["pooled"] < 1e-10 and out["within_a"] > 0.01 and out["within_b"] > 0.01


def test_embryo_gain_is_the_expected_maximum_times_the_within_family_spread():
    assert G.expected_max(1) == pytest.approx(0.0, abs=1e-9)
    assert G.expected_max(2) == pytest.approx(1 / math.sqrt(math.pi), abs=1e-6)
    assert G.expected_max(10) == pytest.approx(1.5388, abs=1e-3)
    assert G.embryo_gain(10, 0.05) == pytest.approx(1.5388 * 15 * math.sqrt(0.025), abs=0.01)
    assert G.embryo_gain(100, 0.05) < 2 * G.embryo_gain(10, 0.05)   # ten times the embryos, less than twice the gain


def test_strangers_share_a_handful_of_traits_from_a_long_list():
    out = G.coincidences(np.full(150, 0.05), 20_000, rng(17))
    assert out["expected"] == pytest.approx(7.5) and out["matches"].mean() == pytest.approx(7.5, abs=0.1)
