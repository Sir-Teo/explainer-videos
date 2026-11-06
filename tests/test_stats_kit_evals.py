"""statkit.evals (Part 64): benchmark error bars, paired comparisons, arenas, IRT, holdout reuse, model-judged labels,
model collapse, conformal factuality, watermarks, amortized posteriors, diffusion and marketplace experiments."""

import math

import numpy as np
from scipy import stats

from explainer.stats.kit import evals as E


def test_cluster_se_and_paired():
    rng = np.random.default_rng(1)
    # with singleton clusters the cluster-robust SE is the iid SE up to the G/(G-1) and ddof factors
    x = (rng.random(500) < 0.7).astype(float)
    a, c = E.mean_se(x), E.cluster_se(x, np.arange(500))
    assert abs(a["se"] - c["se"]) / a["se"] < 1e-9
    # clustering inflates the SE by about sqrt(design effect)
    b = E.clustered_benchmark(200, 10, 0.8, 1.2, rng)
    assert E.cluster_se(b["x"], b["cluster"])["se"] > 1.4 * E.mean_se(b["x"])["se"]
    assert E.design_effect(10, 0.1) == 1.9
    # correlated models: the paired SE is smaller than the unpaired one, and McNemar uses only discordant pairs
    u, v = E.correlated_pair(5000, 0.85, 0.84, 0.8, rng)
    pc = E.paired_compare(u, v)
    assert pc["se_paired"] < 0.85 * pc["se_unpaired"] and pc["corr"] > 0.3
    m = E.mcnemar(u, v)
    assert m["n10"] - m["n01"] == int(u.sum() - v.sum())
    assert E.mcnemar([1, 1, 0], [1, 1, 0])["p"] == 1.0


def test_winners_curse_and_max_normal():
    assert abs(E.expected_max_normal(2) - 1 / math.sqrt(math.pi)) < 1e-6
    rng = np.random.default_rng(2)
    w = E.winners_curse(20, 1000, 0.85, 4000, rng)
    assert abs(w["bias"] - w["approx"]) < 0.002


def test_bradley_terry_elo_and_style():
    rng = np.random.default_rng(3)
    theta = np.array([0.0, 0.4, -0.3, 0.9])
    s = E.simulate_battles(theta, 40000, rng)
    f = E.bt_fit(s["i"], s["j"], s["y"], 4)
    assert np.all(np.abs(f["theta"] - theta) < 4 * np.maximum(f["se"], 1e-9) + 1e-12)
    assert np.allclose(f["se"][1:], f["se_sandwich"][1:], rtol=0.1)
    b = E.bt_bootstrap(s["i"][:4000], s["j"][:4000], s["y"][:4000], 4, 100, rng)
    g = E.bt_fit(s["i"][:4000], s["j"][:4000], s["y"][:4000], 4)
    assert np.allclose(b.std(0)[1:], g["se"][1:], rtol=0.3)
    # Elo on a logistic scale tracks the strengths roughly, but depends on the order of battles
    e1 = E.elo(s["i"], s["j"], s["y"], 4)
    o = rng.permutation(len(s["y"]))
    e2 = E.elo(s["i"][o], s["j"][o], s["y"][o], 4)
    assert not np.allclose(e1, e2) and np.argmax(e1) == 3
    # style control recovers strengths when votes favour long answers
    # each answer's length varies around its model's mean; model 2 writes long answers
    mean_len = np.array([0, 0, 1.0, 0])
    n = len(s["y"])
    st = ((mean_len[s["i"]] + 0.5 * rng.standard_normal(n)) - (mean_len[s["j"]] + 0.5 * rng.standard_normal(n)))[:, None]
    y = (rng.random(len(s["y"])) < 1 / (1 + np.exp(-(theta[s["i"]] - theta[s["j"]] + 0.8 * st[:, 0])))).astype(float)
    raw = E.bt_fit(s["i"], s["j"], y, 4)["theta"]
    ctl = E.bt_style_fit(s["i"], s["j"], y, 4, st)
    assert raw[2] > theta[2] + 0.5 and abs(ctl["theta"][2] - theta[2]) < 0.1 and abs(ctl["gamma"][0] - 0.8) < 0.1


def test_irt():
    rng = np.random.default_rng(4)
    M, J = 80, 400
    th = rng.standard_normal(M)
    a = np.exp(rng.normal(0, 0.3, J))
    b = rng.normal(0, 1, J)
    R = (rng.random((M, J)) < 1 / (1 + np.exp(-a[None] * (th[:, None] - b[None])))).astype(float)
    f = E.fit_2pl(R, iters=20)
    assert np.corrcoef(f["theta"], th)[0, 1] > 0.97 and np.corrcoef(f["b"], b)[0, 1] > 0.9
    t = E.irt_ability(R[0], f["a"], f["b"])
    assert abs(E.irt_accuracy(t, f["a"], f["b"]) - R[0].mean()) < 0.03


def test_holdout_and_judges():
    rng = np.random.default_rng(5)
    o = E.adaptive_overfit(2000, 2000, [200], rng, "reuse")
    assert o["holdout"][0] > 0.55 and abs(o["fresh"][0] - 0.5) < 0.04
    assert E.thresholdout(0.6, 0.6, 0.04, 0.0, rng) == 0.6
    t = (rng.random(200000) < 0.7).astype(float)
    f = E.judged_labels(t, 0.95, 0.8, rng)
    assert abs(f.mean() - (0.7 * 0.95 + 0.3 * 0.2)) < 0.005
    p = E.ppi_mean_ci(t[:2000], f[:2000], f[2000:])
    assert abs(p["est"] - 0.7) < 4 * p["se"]


def test_collapse_and_factuality():
    rng = np.random.default_rng(6)
    c = E.gaussian_collapse(10, 50, 2000, rng)
    assert abs(c["paths"][:, 10].mean() - 0.9 ** 10) < 0.03
    assert abs(c["drift"] - (stats.chi2(9).expect(np.log) - math.log(10))) < 1e-9 and c["drift"] < 0
    cs, ct = E.claim_responses(400, 6, 0.8, 2.0, rng)
    ts, tt = E.claim_responses(2000, 6, 0.8, 2.0, rng)
    o = E.conformal_factuality(cs, ct, ts, 0.1)
    safe = np.mean([all(t for k, t in zip(kk, tr) if k) for kk, tr in zip(o["kept"], tt)])
    assert safe > 0.87


def test_watermark_sbi_diffusion_market():
    assert abs(E.green_prob(0.5, 0.0) - 0.5) < 1e-12
    assert E.watermark_power(200, 0.25, 2.0, 4.0) > 0.99 > E.watermark_power(5, 0.25, 2.0, 4.0)
    assert E.watermark_power(100, 0.25, 2.0, 4.0, edit_frac=1.0) < 0.001
    assert abs(E.watermark_z(25, 100, 0.25)) < 1e-12
    rng = np.random.default_rng(7)
    assert E.amortized_posterior_coverage(4000, 2, 0.9, 4000, rng) > 0.87
    # Tweedie: a single Gaussian N(0, 1) noised by sigma = 1 has E[x | y] = y / 2
    y = np.linspace(-2, 2, 5)
    assert np.allclose(E.tweedie(y, 1.0, E.mixture_score(y, 1.0, [0.0], 1.0, [1.0])), y / 2)
    # the probability-flow sampler reproduces a Gaussian
    x = E.probability_flow(lambda z, s: E.mixture_score(z, s, [0.0], 1.0, [1.0]), np.geomspace(10, 0.01, 200), 20000, rng)
    assert abs(x.std() - 1) < 0.03
    m = E.market_ab(4000, 1800, 0.4, 0.5, 0.5, rng)
    assert m["naive"] > m["global"] + 0.05
