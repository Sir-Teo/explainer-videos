"""Tests for statkit.gsm, the Gaussian sequence model and lower-bound workbench of Part 50."""

import math

import numpy as np

from explainer.stats.kit import gsm as G


def rng(seed=0):
    return np.random.default_rng(seed)


def test_pinsker_linear_minimax_and_constant():
    a = G.sobolev_weights(4000, 1.0)
    for eps in (0.05, 0.01, 0.002):
        p = G.pinsker(eps, a, 1.0)
        assert abs(p["risk"] - p["bayes"]) < 1e-12  # the Gaussian prior is least favourable for linear rules
        assert abs(eps ** 2 * np.sum(a * np.maximum(p["mu"] - a, 0)) - 1.0) < 1e-9
    # the ratio to Pinsker's asymptotic formula tends to one
    r = [G.pinsker(e, a, 1.0)["risk"] / G.pinsker_asymptotic(e, 1.0, 1.0) for e in (0.05, 0.005, 0.0005)]
    assert r[0] < r[1] < r[2] <= 1.0001 and r[2] > 0.98
    assert abs(G.pinsker_constant(1.0) - 3 ** (1 / 3) * (0.5) ** (2 / 3)) < 1e-12


def test_estimators_on_the_hardest_theta():
    a = G.sobolev_weights(1000, 1.0)
    eps = 0.03
    p = G.pinsker(eps, a, 1.0)
    th = G.hardest_theta(eps, a, 1.0)
    assert abs(np.sum(a ** 2 * th ** 2) - 1.0) < 1e-9
    y = th[None, :] + eps * rng(1).standard_normal((600, len(a)))
    risk = lambda e: float(np.mean(np.sum((e - th) ** 2, axis=1)))  # noqa: E731
    rp = risk(G.est_linear(y, p["shrink"]))
    assert abs(rp - p["risk"]) < 0.08 * p["risk"]  # the linear rule's risk is constant on this theta's orbit
    assert risk(G.est_block_js(y, eps)) < 3 * rp  # adaptive, within a constant
    assert risk(y) > 50 * rp  # no shrinkage is hopeless


def test_divergences():
    assert abs(G.tv_normal(0.0)) < 1e-12
    assert abs(G.kl_normal(2.0) - 2.0) < 1e-12
    for d in (0.1, 0.5, 1.0, 2.0):
        tv, kl, h2 = G.tv_normal(d), G.kl_normal(d), G.hellinger2_normal(d)
        assert tv <= math.sqrt(kl / 2) + 1e-12  # Pinsker's inequality
        assert h2 <= tv <= math.sqrt(2 * h2) + 1e-12  # Le Cam's inequalities (H^2 = 1 - affinity)
    assert G.kl_bernoulli(0.5, 0.5) == 0.0


def test_lower_bounds_scale_with_rate():
    b1, b2 = G.lecam_density_point(1000), G.lecam_density_point(16000)
    ratio = (b1["bound"] / b2["bound"]) / (b1["rate"] / b2["rate"])
    assert 0.6 < ratio < 1.6  # the two-point bound has the rate n^(-2s/(2s+1))
    a1, a2 = G.assouad_holder(1000), G.assouad_holder(16000)
    ratio = (a1["bound"] / a2["bound"]) / (a1["rate"] / a2["rate"])
    assert 0.5 < ratio < 2.0
    vg = G.varshamov_gilbert(24, rng(2), trials=3000)
    assert vg["M"] >= vg["guarantee"]
    P = vg["pts"]
    d = (P[:, None, :] != P[None, :, :]).sum(-1)
    assert d[np.triu_indices(len(P), 1)].min() >= 24 / 8
    assert G.fano_bound(1000, 1.0, 0.1) > 0 and G.fano_bound(2, 1.0, 0.1) == 0.0


def test_lepski_and_detection():
    # Lepski picks a large bandwidth for a flat function and a small one for a sharp kink
    r = rng(3)
    hs = np.array([0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32])
    for f, small in ((lambda x: 0 * x, False), (lambda x: 20 * np.abs(x - 0.5), True)):
        ests, sds = [], []
        for h in hs:
            e, k = G.white_noise_kernel(f, 0.5, h, 4000, r)
            ests.append(e[0])
            sds.append(1 / math.sqrt(k))
        j = G.lepski(np.array(ests), np.array(sds))
        assert (j <= 3) if small else (j >= 4)
    assert abs(G.detection_boundary(0.6) - 0.1) < 1e-12
    assert abs(G.detection_boundary(0.9) - (1 - math.sqrt(0.1)) ** 2) < 1e-12
    null = G.higher_criticism(r.standard_normal((200, 2000)))
    alt = G.higher_criticism(G.sparse_mixture(2000, 0.6, 0.5, r, reps=200))
    assert np.mean(alt > np.quantile(null, 0.95)) > 0.8
    A = G.planted_clique(150, 40, r)
    assert (A == A.T).all() and not A.diagonal().any()
    assert G.degree_stat(A) > 3
