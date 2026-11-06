"""Checks for the Reasoner's games module (Part 34)."""

from explainer.philosophy.reasoner import games as G


def test_equilibria_and_best_responses():
    t = G.equilibria_table()
    assert [len(t[n]["equilibria"]) for n in G.GAMES] == [1, 1, 3, 3, 3]
    br = G.best_responses()
    assert (br["q_star"], br["p_star"]) == (0.3333, 0.6667)


def test_commons_and_public_goods():
    c = G.commons()
    assert c["rows"][0]["share_of_best"] == 1.0 and c["rows"][-1]["share_of_best"] < 0.05
    pg = G.public_goods()
    assert pg["free"][-1] < 0.2 < 0.8 < pg["sanctioned"][-1]


def test_centipede_correlated_zd():
    c = G.centipede()
    assert c["backward_takes_everywhere"] and c["qre"][-1]["ends_at"][0] == 1.0
    ce = G.correlated_chicken()
    assert ce["best_payoff"] == [5.25, 5.25]
    z = G.zero_determinant(n_opponents=300)
    assert abs(z["ratio_min"] - 3) < 1e-3 and abs(z["equalized_max"] - 2) < 1e-6


def test_bargaining_shapley_mechanisms():
    b = G.bargaining()
    assert b["nash_x"] == 0.6667 and b["ks_x"] == 0.618
    s = G.shapley_examples()
    assert s["glove"]["L"] == 0.6667 and s["shap"] == {"x1": 1.0, "x2": 1.0, "x3": 1.0}
    g = G.gsp_vcg()
    assert g["vcg_revenue"] == 2.4
    m = G.gale_shapley()
    assert m["stable"] and m["proposer_optimal"] and m["student_gains_by_lying"] == 0


def test_shadow_and_folk_theorem():
    sh = G.shadow()
    assert sh["grim"]["threshold_grid"] == 0.5 and sh["tft"]["threshold_grid"] == 0.67
    assert abs(sh["tft"]["threshold"] - 2 / 3) < 1e-12 and sh["tft"]["argbest"][60] == "DCDCC"
    f = G.folk_theorem(max_len=5)
    pts = {tuple(p["u"]): p["delta"] for p in f["points"]}
    assert pts[(3.0, 3.0)] == 0.5 and pts[(2.5, 2.5)] == 0.25
    assert all(u > 1 and v > 1 for u, v in pts)
