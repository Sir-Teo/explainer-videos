"""Checks for the Reasoner's ethics module (Part 35)."""

from explainer.philosophy.reasoner import ethics as E


def test_harsanyi_and_distributions():
    h = E.harsanyi()
    assert h["ex_ante"]["50:50 mixture"] > h["ex_ante"]["sure (1, 0)"] == h["ex_ante"]["sure (0, 1)"]
    assert h["utilitarian"] == [0.5, 0.75]
    d = E.distributions()["rows"]
    assert d["levelled down"]["gini"] == 0 < d["before levelling"]["gini"]
    assert d["levelled down"]["prioritarian"] < d["before levelling"]["prioritarian"]


def test_promises_and_maxims():
    p = {r["f"]: r for r in E.promise_world()["rows"]}
    assert p[0.0]["lent_rounds"] == 40 and p[1.0]["lent_rounds"] == 1
    kinds = [r["kind"] for r in E.maxims()["rows"]]
    assert kinds.count("false positive") == 2 and kinds.count("false negative") == 1


def test_paradox_trolley_transmitter_uncertainty():
    assert [r["verdict"] for r in E.deontology_paradox()["rows"]][-1] == "refrain"
    t = {r["case"]: r for r in E.trolley()["rows"]}
    assert t["switch"]["double_effect"] == "permissible" and t["footbridge"]["double_effect"] == "impermissible"
    tr = E.transmitter()["rows"]
    assert tr[0]["relevance"] == "save Jones" and tr[2]["relevance"] == "help the many"
    m = E.moral_uncertainty()
    assert m["two"]["results"]["raw"]["choice"] == "do nothing" and m["two"]["results"]["variance"]["choice"] == "push"


def test_levels_monster_pond():
    t = E.two_level(n=50000)
    assert t["ideal"] > t["curves"]["0.0"]["act"][-1] and t["curves"]["0.0"]["act"][-1] < 0
    assert t["curves"]["0.5"]["act_below_rule_at"] < t["curves"]["0.0"]["act_below_rule_at"]
    m = E.utility_monster()
    assert m["best"]["utilitarian"]["monster"] == round(m["utilitarian_exact"], 2) == 90.91
    assert m["best"]["maximin"]["monster"] < 1 < m["best"]["prioritarian"]["monster"] < 50
    p = E.pond()
    assert p["best_gift"] == 24750 and p["world"]["full_compliance_gift"] == 44550


def test_taurek_and_particularism():
    rows = {r["policy"]: r for r in E.taurek()["rows"]}
    assert rows["fair coin"]["expected_saved"] == 3 and rows["weighted lottery"]["p_many"] == 0.8333
    q = E.particularism()
    assert q["atomistic"]["acc"] < 0.7 and q["with_defeaters"]["acc"] == 1.0
    assert q["atomistic"]["weights"] == [0, 0, -1] and q["with_defeaters"]["weights"] == [1, -2, 1, -1, -2, 2]


def test_adaptive_preferences():
    a = E.adaptive_preferences()
    assert a["final"]["capability"] == 0.2 and a["final"]["desire"] > 0.95 and a["lowest_desire"] < 0.35


def test_humanity_and_moral_information():
    h = E.humanity_test()
    assert h["act_matches"] == 7 and h["attitude_matches"] == 6
    m = E.moral_information()
    assert m["variance"]["at_0.6"] == 0.8 and m["raw"]["peak_p"] == 0.96
    assert min(min(m[k]["voi"]) for k in ("raw", "range", "variance")) >= 0
