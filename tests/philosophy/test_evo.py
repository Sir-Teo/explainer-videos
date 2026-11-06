import numpy as np

from explainer.philosophy.reasoner import evo as Ev


def test_price_identity():
    d = Ev.price_check()
    assert d["identity_error"] < 1e-9
    assert d["selection"] > 0 > d["transmission"]


def test_hawk_dove_ess():
    h = Ev.hawk_dove(2, 3)
    assert abs(h["p_star"] - 2 / 3) < 1e-12 and abs(h["payoff_tie"]) < 1e-12
    assert all(v["stability_margin"] > 0 for v in h["invasion"].values())
    assert all(abs(t[-1] - 2 / 3) < 0.02 for t in h["trajectories"])


def test_hamilton():
    for r, b, c in ((0.5, 3, 1), (0.25, 3, 1), (0.5, 1.5, 1)):
        d = Ev.hamilton_from_price(r, b, c)
        assert abs(d["cov"] - d["formula"]) < 1e-12
    up = Ev.hamilton_sim(0.5, 3, 1)
    down = Ev.hamilton_sim(0.25, 3, 1)
    assert up["traj"][-1] > 0.9 and down["traj"][-1] < 0.05


def test_multilevel_simpson():
    m = Ev.multilevel()
    assert m["within"] < 0 < m["between"] and m["delta"] > 0 and m["check"] < 1e-12
    assert all(g["w_alt"] < g["w_self"] for g in m["groups"])


def test_code_and_parsimony():
    c = Ev.code_information()
    assert c["outputs"] == 21 and abs(c["entropy"] - 4.218) < 1e-3
    d = Ev.parsimony_demo()
    s = d["scores"]
    assert s["nested"] == d["min_possible"] == 8 and s["alt1"] > 8 and s["alt2"] > s["alt1"]
    assert d["gains"]["diapsid skull"] == ["lizard", "pigeon"] and d["gains"]["opposable thumb"] == ["chimp"]


def test_rps_cycles():
    t = np.array(Ev.rps()["traj"])
    assert np.allclose(t.sum(1), 1) and t.min() > 0


def test_life_definitions_and_entropy():
    d = Ev.life_definitions()
    assert d["alive"]["NASA (Joyce)"] == ["bacterium"]
    assert "mule" not in d["alive"]["reproduces"] and "mule" in d["alive"]["metabolizes"]
    assert "bacterium" not in d["contested"] and len(d["contested"]) == len(d["cases"]) - 1
    e = Ev.entropy_budget()
    assert e["body"] > 0 and abs(e["earth"] - (e["earth_out"] - e["earth_in"])) < 1
    assert 5e14 < e["earth"] < 7e14


def test_conway_glider():
    g = Ev.conway_glider()
    assert g["period"] == 4 and g["shift"] == [1, 1] and set(g["population"]) == {5}
    blinker = np.zeros((5, 5), int)
    blinker[2, 1:4] = 1
    assert np.array_equal(Ev.life_step(Ev.life_step(blinker)), blinker)


def test_eye_drift_fisher():
    e = Ev.eye_generations()
    assert round(e["steps"]) == 1829 and abs(e["generations"] - 363992) < 1
    assert abs(Ev.kimura_fix(100, 0.0) - 0.01) < 1e-12 and Ev.kimura_fix(100, 0.05) > 9 * Ev.kimura_fix(100, 0.0)
    d = Ev.wright_fisher(runs=6000, paths=4)
    for v in d["fix"].values():
        assert abs(v["sim"] - v["kimura"]) < 5 * max(v["se"], 1e-3)
    f = Ev.fisher_theorem()
    assert f["max_error"] < 1e-12 and f["var"][-1] < f["var"][0] / 50


def test_relatedness_parity_shadow():
    r = Ev.relatedness_table()["rows"]
    assert r["full sisters (diploid)"] == 0.5 and r["sister to sister (haplodiploid)"] == 0.75
    assert r["sister to brother (haplodiploid)"] == 0.25 and r["brother to sister (haplodiploid)"] == 0.5
    p = Ev.parity_demo()
    assert abs(p["both vary"]["gene"] - p["both vary"]["diet"]) < 1e-12
    assert p["diet fixed"]["gene"] == 1.0 and p["gene fixed"]["gene"] == 0.0
    s = Ev.shadow()
    assert abs(s["xstar"] - 0.2) < 1e-12 and s["threshold"] == 0.5 and abs(Ev.shadow(w=0.9)["xstar"] - 1 / 17) < 1e-12
    assert s["trajs"][1][-1] < 0.01 and s["trajs"][2][-1] > 0.99


def test_signalling_learns():
    d = Ev.lewis_signalling(n=2, rounds=1000, runs=20)
    assert d["curve"][-1] > d["curve"][0] + 0.15 and d["final_mean"] > 0.85
