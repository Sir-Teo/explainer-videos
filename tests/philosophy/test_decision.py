"""Tests for the Reasoner's decision module (Part 33)."""

from explainer.philosophy.reasoner import decision as D


def test_pump_stpete_triangle():
    assert D.money_pump()["paid"] == 0.15
    s = D.st_petersburg(plays=10 ** 5)
    assert s["eu_log2"] == 2.0 and s["ce"] == 4.0 and s["means"][-1] > s["means"][0]
    assert D.triangle_lines()["slope"] == 1.5


def test_allais_ellsberg_prospect():
    a = D.allais()
    assert a["both_ok"] == 0 and a["reu_pattern"]
    e = D.ellsberg()
    assert e["both_ok"] == 0 and e["maxmin_pattern"]
    f = {r["prospect"]: r for r in D.prospect()["fourfold"]}
    assert f["5% chance of 100"]["ce"] > 5 and f["95% chance of 100"]["ce"] < 95
    assert f["5% chance of -100"]["ce"] < -5 and f["95% chance of -100"]["ce"] > -95


def test_kelly_pasadena_newcomb():
    k = D.kelly(paths=200)
    assert k["f_star"] == 0.2
    g = {f: v["g"] for f, v in k["by_f"].items()}
    assert g["0.2"] > g["0.1"] > 0 > g["0.4"] > g["0.6"]
    p = D.pasadena(terms=60000)
    assert abs(p["natural"] - p["ln2"]) < 1e-3 and abs(p["two_one"] - p["three_halves_ln2"]) < 1e-3
    n = D.newcomb()
    assert n["one_mean"] > n["two_mean"]


def test_edt_cdt_dynamic_good_envelopes():
    s = D.smoking_lesion()
    assert s["edt_choice"] == "abstain" and s["cdt_choice"] == "smoke"
    assert D.damascus()["ratifiable"] == []
    h = D.hitchhiker()
    assert h["policy_pay"] > h["policy_refuse"] and h["in_town_pay"] < h["in_town_refuse"]
    u = D.ulysses()
    assert u["naive"] == "wrecked" and u["sophisticated"] == "past the sirens, bound"
    g = D.good_theorem(problems=500)
    assert g["negative"] == 0 and g["reu_counterexample"] is not None
    e = D.two_envelopes()
    assert abs(e["proper_total"]) < 1e-9 and all(r["gain"] > 0 for r in e["broome"])


def test_psychopath_button_splits_the_theories():
    d = D.psychopath_button()
    assert d["cdt_choice"] == "press" and d["edt_choice"] == "refrain"
    assert d["cdt_press"] == 4.5 and d["cdt_press_once_decided"] == -89.0


def test_hyperbolic_discounting_reverses():
    d = D.discounting()
    assert d["exp_consistent"] and d["hyp_pick"][0] == "sooner" and d["hyp_pick"][-1] == "later"
    assert d["hyp_switch_day"] == 9


def test_voi_example_is_jensen_gap():
    v = D.voi_example()
    assert v["voi"] > 0 and v["act_now"] == "no umbrella" and v["act_rain"] == "stay in"
    assert abs(v["p_says_rain"] * v["q_rain"] + (1 - v["p_says_rain"]) * v["q_dry"] - v["prior"]) < 1e-3


def test_revealed_framing_twins():
    r = D.revealed_preference()
    assert r["consistent"]["garp"] and not r["inconsistent"]["garp"]
    assert r["consistent"]["ccei"] == 1.0 and 0.9 < r["inconsistent"]["ccei"] < 0.92
    a = D.asian_disease()
    assert a["gain_frame_choice"] == "A" and a["loss_frame_choice"] == "D"
    t = D.twin_pd()
    assert t["threshold"] == 0.7143 and t["dominance_gain"] == [2, 1]
