"""statkit.sequential (Part 58): the SPRT's exact law, Ville, e-values, confidence sequences, adaptive inference."""

import numpy as np

from explainer.stats.kit import sequential as Q


def test_sprt_exact_matches_simulation_and_wald():
    p0, p1, a, b = 0.5, 0.6, 0.05, 0.1
    rng = np.random.default_rng(1)
    for p in (p0, p1):
        ex = Q.sprt_bernoulli_exact(p, p0, p1, a, b)
        assert ex["unfinished"] < 1e-9
        assert abs(ex["accept_h1"] + ex["accept_h0"] - 1) < 1e-9
        assert abs(ex["stop_n"].sum() - 1) < 1e-9
        sims = [Q.sprt_simulate(rng.random(4000) < p, p0, p1, a, b) for _ in range(3000)]
        acc = np.mean([s["decision"] == 1 for s in sims])
        asn = np.mean([s["n"] for s in sims])
        assert abs(acc - ex["accept_h1"]) < 0.02
        assert abs(asn - ex["asn"]) / ex["asn"] < 0.05
        wa = Q.sprt_wald_approx(p, p0, p1, a, b)
        assert abs(wa["accept_h1"] - ex["accept_h1"]) < 0.03
    # Wald's bounds on the errors: alpha' <= alpha/(1 - beta), beta' <= beta/(1 - alpha)
    assert Q.sprt_bernoulli_exact(p0, p0, p1, a, b)["accept_h1"] <= a / (1 - b) + 1e-12
    assert Q.sprt_bernoulli_exact(p1, p0, p1, a, b)["accept_h0"] <= b / (1 - a) + 1e-12
    fx = Q.fixed_n_binomial(p0, p1, a, b)
    assert fx["size"] <= a and fx["power"] >= 1 - b
    assert Q.sprt_bernoulli_exact(p0, p0, p1, a, b)["asn"] < fx["n"]


def test_ville_and_peeking():
    rng = np.random.default_rng(2)
    v = Q.ville_check(500, 0.3, 0.05, 4000, rng)
    assert v["ville"] <= 0.05 + 0.01
    assert v["peek"] > 0.25
    assert abs(v["end_only"] - 0.05) < 0.015
    c = Q.peeking_curve([1, 10, 100], 0.05, 4000, rng)
    assert c[0] < c[1] < c[2]


def test_evalues():
    # the calibrator integrates to one; e -> p is valid
    from scipy import integrate

    assert abs(integrate.quad(lambda p: Q.calibrate_p_to_e(p, 0.3), 0, 1)[0] - 1) < 1e-6
    rng = np.random.default_rng(3)
    e = Q.calibrate_p_to_e(rng.random(200_000), 0.5)
    assert abs(e.mean() - 1) < 0.02
    # universal inference: E_H0[e] <= 1 and P(e >= 1/alpha) <= alpha
    es = np.array([Q.split_lrt_normal_mean(rng.normal(0, 2, 40), rng) for _ in range(4000)])
    assert np.mean(es >= 20) <= 0.05 + 0.01
    # e-BH on independent nulls and signals controls the FDR
    fdp = []
    for _ in range(400):
        m, k = 100, 20
        x = np.r_[rng.standard_normal(m - k), rng.standard_normal(k) + 3]
        ee = np.exp(2 * x - 2)  # likelihood ratios N(2,1)/N(0,1): e-values under the null
        r = Q.ebh(ee, 0.1)["reject"]
        fdp.append(r[: m - k].sum() / max(1, r.sum()))
    assert np.mean(fdp) <= 0.1


def test_confidence_sequences():
    rng = np.random.default_rng(4)
    T = 2000
    t = np.arange(1, T + 1)
    bern = lambda g, n: (g.random(n) < 0.3).astype(float)  # noqa: E731
    fixed = Q.cs_coverage(lambda x: Q.hoeffding_fixed(np.cumsum(x) / t, t, 0.05), bern, T, 300, 0.3, rng)
    bet = Q.cs_coverage(lambda x: (lambda d: (d["lo"], d["hi"]))(Q.betting_cs(x, 0.05)), bern, T, 120, 0.3, rng)
    mix = Q.cs_coverage(lambda x: Q.normal_mixture_cs(np.cumsum(x) / t, t, 0.05, tau2=1.0, sigma=0.5), bern, T, 300, 0.3, rng)
    assert bet["uniform"] >= 0.93 and mix["uniform"] >= 0.93
    assert fixed["final"] >= 0.95
    assert fixed["uniform"] < bet["uniform"]
    # the betting CS is narrower than the union-bound Hoeffding sequence at the end
    x = bern(rng, T)
    d = Q.betting_cs(x, 0.05)
    lo, hi = Q.hoeffding_union(np.cumsum(x) / t, t, 0.05)
    assert d["hi"][-1] - d["lo"][-1] < hi[-1] - lo[-1]
    # the stitched boundary holds uniformly for Gaussian walks
    S = np.cumsum(rng.standard_normal((2000, T)), 1)
    assert np.mean((S >= Q.stitched_boundary(t, 0.05)[None, :]).any(1)) <= 0.05


def test_changepoints_and_adaptive():
    rng = np.random.default_rng(5)
    x = np.r_[rng.standard_normal(300), rng.standard_normal(200) + 1.5]
    c = Q.cusum(x, 0, 1.5, 6.0)
    assert 300 <= c["alarm"] < 330
    R = Q.bocpd_normal(x, 1 / 200)
    assert np.allclose(R.sum(1), 1)
    assert abs(int(np.argmax(R[-1])) - 200) < 15
    # Thompson sampling biases arm means downward; adaptive weighting restores coverage
    naive_cov = aw_cov = 0
    reps = 150
    means = [0.5, 0.55]
    for _ in range(reps):
        d = Q.thompson_bernoulli(means, 600, rng, floor=0.05, n_mc=100)
        est = Q.arm_estimates(d["arm"], d["y"], d["e"], 2)
        naive_cov += est[0]["naive_lo"] <= means[0] <= est[0]["naive_hi"]
        aw_cov += est[0]["aw_lo"] <= means[0] <= est[0]["aw_hi"]
    assert aw_cov / reps > 0.85
    # off-policy evaluation: IPW is unbiased for the target policy's value
    d = Q.thompson_bernoulli(means, 3000, rng, floor=0.1, n_mc=100)
    P = np.tile([1.0, 0.0], (3000, 1))
    v = Q.policy_value(d["y"], d["arm"], d["e"], P, mhat=np.array([0.5, 0.55]))
    assert abs(v["ipw"] - 0.5) < 4 * v["ipw_se"] and abs(v["dr"] - 0.5) < 4 * v["dr_se"]
