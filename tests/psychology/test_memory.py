"""Psyche's memory module (Part 20): forgetting laws, free-recall statistics, SAM, CMR and its likelihood, Hopfield
networks, ACT-R, recognition ROCs and pattern separation; and the two open datasets the part fits."""

import numpy as np
import pytest

from explainer.psychology import archive, opendata
from explainer.psychology.psyche import memory as M


def test_ebbinghaus_formula_matches_his_column():
    e = archive.EBBINGHAUS_1885.data
    mine = M.ebbinghaus_formula(e["minutes"], e["k"], e["c"])
    assert np.allclose(mine, e["calculated"], atol=1.0)


def test_power_beats_exponential_on_his_savings():
    e = archive.EBBINGHAUS_1885.data
    f = M.fit_forgetting(e["minutes"], e["saving"])
    assert f["power"]["sse"] < f["exponential"]["sse"] / 5
    assert f["ebbinghaus"]["sse"] < f["exponential"]["sse"] / 5


def test_lag_crp_worked_example():
    # the sequence of chapter 3 and problem 2: 16, 15, 14, 1, 2, 9
    lags, crp = M.lag_crp([[16, 15, 14, 1, 2, 9]], 16, max_lag=2)
    d = dict(zip(lags, crp))
    assert d[1] == pytest.approx(1 / 2)  # 1 -> 2 taken; possible after 1 and after 2
    assert d[-1] == pytest.approx(2 / 3)  # 16 -> 15, 15 -> 14 taken; possible after 16, 15 and 14
    assert np.isnan(d[0])


def test_spc_and_pfr():
    R = np.array([[16, 15, 1, 0], [1, 2, 0, 0], [16, 0, 0, 0], [3, 3, 99, 0]])
    s, p = M.spc(R, 16), M.pfr(R, 16)
    assert s[15] == pytest.approx(0.5) and s[0] == pytest.approx(0.5) and s[2] == pytest.approx(0.25)
    assert p.sum() == pytest.approx(1.0) and p[15] == pytest.approx(0.5)


def test_drift_keeps_context_unit_length():
    rng = np.random.default_rng(0)
    c = rng.standard_normal(20)
    c /= np.linalg.norm(c)
    for beta in (0.1, 0.5, 0.95):
        x = rng.standard_normal(20)
        assert np.linalg.norm(M._drift(c, x, beta)) == pytest.approx(1.0)
    e = np.zeros(20)
    e[0] = 1.0
    c0 = np.zeros(20)
    c0[1] = 1.0  # orthogonal input: rho = sqrt(1 - beta^2)
    out = M._drift(c0, e, 0.6)
    assert out[1] == pytest.approx(np.sqrt(1 - 0.36)) and out[0] == pytest.approx(0.6)


def test_cmr_likelihood_matches_its_simulation():
    p = {"B_enc": 0.8, "B_rec": 0.7, "B_start": 0.1, "gamma_fc": 0.2, "phi_s": 3.0, "phi_d": 1.0, "tau": 0.8,
         "stop_s": 0.05, "stop_r": 0.25}
    sim = M.cmr_simulate(8, 20000, p, np.random.default_rng(3))
    first = sim[:, 0]
    for k in (1, 8):  # the probability of the one-recall sequence "k, then stop", by likelihood and by simulation
        lik = np.exp(M.cmr_loglik(p, [[k]], 8))
        freq = np.mean((first == k) & (sim[:, 1] == 0))
        assert lik == pytest.approx(freq, abs=0.01)


def test_sam_contiguity_is_symmetric_and_cmr_leans_forward():
    s = M.recall_summary(M.sam_simulate(16, 3000, rng=np.random.default_rng(1)), 16, max_lag=1)
    assert abs(s["crp"][2] - s["crp"][0]) < 0.06
    c = M.recall_summary(M.cmr_simulate(16, 3000, {"gamma_fc": 0.1, "B_enc": 0.9, "B_rec": 0.9, "tau": 1.0},
                                        np.random.default_rng(1)), 16, max_lag=1)
    assert c["crp"][2] > c["crp"][0] + 0.05


def test_hopfield_capacity_collapses_near_0138():
    h = M.hopfield_capacity(200, [0.05, 0.25], trials=30, rng=np.random.default_rng(0))
    assert h["recalled"][0] > 0.9 and h["recalled"][1] < 0.2


def test_actr_activation_is_a_power_law_sum():
    a1 = M.actr_activation([0.0], 100.0)
    assert a1 == pytest.approx(np.log(100.0 ** -0.5))
    assert M.actr_activation([0.0, 50.0], 100.0) > a1  # practice adds
    assert M.actr_recall(-0.5) == pytest.approx(0.5)


def test_roc_intercepts():
    F, H = M.dual_process_roc(0.3, 1.0, criteria=[10.0])
    assert H[0] == pytest.approx(0.3, abs=1e-6) and F[0] < 1e-6  # recollection alone at the strictest criterion
    F2, H2 = M.uvsd_roc(1.0, 1.25, criteria=[-10.0, 10.0])
    assert H2[0] > 0.999 and H2[1] < 1e-6


def test_pattern_separation():
    out = M.pattern_separation([0.5, 1.0], pairs=20, rng=np.random.default_rng(0))
    assert out[0] < 0.45 and out[1] == pytest.approx(1.0)


def test_peers_open_data():
    if not opendata.available("peers_free_recall"):
        pytest.skip("PEERS could not be fetched")
    d = opendata.peers_free_recall()
    assert d["recalls"].shape == (3528, 24) and len(np.unique(d["subject"])) == 126
    s = M.recall_summary(d["recalls"], 16, max_lag=1)
    assert s["spc"][-1] > s["spc"][0] > s["spc"][7]  # recency, primacy, the middle
    assert s["pfr"][-1] > 0.4 and s["crp"][2] > s["crp"][0]  # starts at the end; leans forward


def test_murre_open_data():
    if not opendata.available("murre_2021"):
        pytest.skip("Murre's workbook could not be fetched")
    S = opendata.murre_2021()["scores"]
    assert S.shape == (16, 4)
    assert np.allclose(S.mean(0), [9.25, 9.8125, 6.9375, 5.0])
    eff = (S[:, 0] + S[:, 3]) / 2 - (S[:, 1] + S[:, 2]) / 2
    assert eff.mean() == pytest.approx(-1.25)


def test_battery_task_six():
    from explainer.psychology import battery

    t = battery.run("recall", {"B_enc": 0.9, "B_rec": 0.9, "gamma_fc": 0.1, "tau": 1.0}, 400, seed=3)
    assert len(t) == 400 and t.extra["recalls"].shape == (400, 16)
    s = M.recall_summary(t.extra["recalls"], 16, max_lag=1)
    assert s["spc"][-1] > s["spc"][7] and s["crp"][2] > s["crp"][0]
