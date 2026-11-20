"""Agora's growth module (Part 20): the Solow model, accounting, convergence and the Ramsey model."""

import numpy as np

from explainer.economics.agora import growth as gr


def test_steady_state_and_golden_rule():
    st = gr.solow_steady(0.2, n=0.01, g=0.02, delta=0.05, alpha=1 / 3)
    # k* solves s k^alpha = (n + g + delta) k
    assert abs(0.2 * st["k"] ** (1 / 3) - 0.08 * st["k"]) < 1e-12
    assert abs(st["ky"] - 0.2 / 0.08) < 1e-12
    gold = gr.golden_rule(alpha=0.3)
    assert abs(gold["s_gold"] - 0.3) < 2e-3
    # at the golden rule the marginal product of capital equals n + g + delta
    st = gr.solow_steady(0.3, alpha=0.3)
    assert abs(st["mpk"] - 0.08) < 1e-9


def test_path_converges_to_the_steady_state_and_speed():
    st = gr.solow_steady(0.25)
    p = gr.solow_path(0.25, 400, k0=0.2 * st["k"])
    assert abs(p["k"][-1] / st["k"] - 1) < 1e-6
    c = gr.convergence_speed(alpha=1 / 3)
    assert abs(c["lambda"] - (2 / 3) * 0.08) < 1e-12
    # the linear half-life and the simulated one agree to within a few years
    assert abs(c["half_life"] - c["half_life_simulated"]) < 4
    assert gr.convergence_speed(alpha=0.75)["half_life"] > 30


def test_saving_raises_the_level_not_the_growth_rate():
    p = gr.solow_path(lambda t: 0.3 if t >= 10 else 0.15, 300, k0=gr.solow_steady(0.15)["k"])
    gy = np.diff(np.log(p["y_per_worker"]))
    assert abs(gy[5] - np.log(1.02)) < 1e-9
    assert gy[12] > 0.03                                   # faster growth during the transition
    assert abs(gy[-1] - np.log(1.02)) < 1e-6               # back to technology's rate
    ratio = p["y"][-1] / p["y"][0]
    assert abs(ratio - 2 ** 0.5) < 1e-4                    # (0.30 / 0.15)^(alpha / (1 - alpha))


def test_growth_accounting_identity():
    rows = []
    for t, y in enumerate(range(2000, 2011)):
        rows.append({"year": y, "rgdpna": 100 * 1.03 ** t, "rnna": 300 * 1.04 ** t, "emp": 10 * 1.01 ** t,
                     "avh": 2000.0, "hc": 2.0 * 1.005 ** t, "labsh": 0.6})
    a = gr.growth_accounting(rows, 2000, 2010)
    assert abs(a["alpha"] - 0.4) < 1e-12
    assert abs(a["capital"] + a["hours"] + a["human_capital"] + a["tfp"] - a["output"]) < 1e-12
    assert abs(a["tfp"] - (np.log(1.03) - 0.4 * np.log(1.04) - 0.6 * (np.log(1.01) + np.log(1.005)))) < 1e-12


def test_development_accounting_and_convergence():
    rng = np.random.default_rng(0)
    rows = []
    for i in range(60):
        A = np.exp(rng.normal(0, 0.8))
        h = np.exp(rng.normal(0.5, 0.3))
        ky = np.exp(rng.normal(1.0, 0.3))
        emp = 10.0
        y = A * h * ky ** 0.5
        rows.append({"countrycode": "USA" if i == 0 else f"C{i}", "rgdpo": y * emp, "emp": emp, "cn": ky * y * emp,
                     "hc": h})
    d = gr.development_accounting(rows, alpha=1 / 3)
    # each country's income is exactly the product of its three factors
    for y, k, h, A in zip(d["y_rel"], d["ky_rel"], d["h_rel"], d["A_rel"]):
        assert abs(y - k * h * A) < 1e-9 * y
    assert 0 < d["share_factors"] < 1
    # a planted convergence speed is recovered by the cross-section regression
    lam, T = 0.02, 30
    y0 = np.exp(rng.normal(8, 1, 400))
    ystar = np.exp(9.0)
    y1 = np.exp(np.log(ystar) + np.exp(-lam * T) * (np.log(y0) - np.log(ystar)))
    c = gr.convergence(y0, y1, T)
    assert abs(c["lambda"] - lam) < 1e-9


def test_lucas_and_ramsey():
    m = gr.mpk_ratio(1.0, 15.0, alpha=0.4)
    assert abs(m["raw"] - 15 ** 1.5) < 1e-9                # Lucas's 58
    assert abs(gr.mpk_ratio(1.0, 15.0, alpha=0.4, h_rich=5.0)["with_human_capital"] - 3 ** 1.5) < 1e-9
    r = gr.ramsey(rho=0.03, theta=2.0, n=0.01, g=0.02, delta=0.05, alpha=1 / 3)
    # the modified golden rule: alpha k^(alpha - 1) = delta + rho + theta g, below the golden rule
    assert abs((1 / 3) * r["k_ss"] ** (-2 / 3) - 0.12) < 1e-9
    assert r["k_ss"] < (1 / 3 / 0.08) ** 1.5
    # the saddle path ends close to the steady state; the missed shots leave it
    assert abs(r["path_k"][-1] / r["k_ss"] - 1) < 0.02
    assert r["path_c"][0] < r["c_ss"]
