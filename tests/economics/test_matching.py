"""Agora's matching module (Part 17)."""

from explainer.economics.agora import matching as mt
from explainer.economics.island import truths

T = truths(17)


def _market():
    p = T["playit"]
    students = {k: list(v) for k, v in p["students"].items()}
    schools = {s: list(p["lottery"]) for s in p["capacity"]}
    return students, schools, dict(p["capacity"])


def test_boston_punishes_truth_and_deferred_acceptance_does_not():
    students, schools, cap = _market()
    assert mt.boston(students, schools, cap)["match"]["you"] == "loft"
    gets = {tuple(r["report"]): r["gets"] for r in mt.outcomes_by_report("you", students, schools, cap, "boston")}
    assert gets[("kiln", "boatyard", "loft")] == "kiln"
    da = mt.deferred_acceptance(students, schools, cap)["match"]
    assert da["you"] == "kiln"
    rank = students["you"]
    for r in mt.outcomes_by_report("you", students, schools, cap, "da"):
        assert rank.index(r["gets"]) >= rank.index(da["you"])          # no report does better than the truth
    assert ("you", "kiln") in mt.blocking_pairs(mt.boston(students, schools, cap)["match"], students, schools, cap)
    assert not mt.blocking_pairs(da, students, schools, cap)


def test_board_has_three_stable_matchings_and_each_side_gets_its_best():
    b = T["board"]
    pa = {k: list(v) for k, v in b["apprentices"].items()}
    pw = {k: list(v) for k, v in b["workshops"].items()}
    st = mt.all_stable(pa, pw)
    assert len(st) == 3
    da = mt.deferred_acceptance(pa, pw)
    assert da["match"] == st[0]["match"] and da["rounds"] == 6
    wd = mt.deferred_acceptance(pw, pa)["match"]
    assert {a: w for w, a in wd.items()} == st[-1]["match"]


def test_ttc_kidneys_and_pivotal():
    h = {k: list(v) for k, v in T["huts"].items()}
    t = mt.top_trading_cycles(h)
    assert t["alloc"] == {"ana": "bo", "bo": "ana", "chidi": "dara", "dara": "chidi"}
    k = T["kidneys"]
    r = mt.kidney_exchange({p: set(v) for p, v in k["compat"].items()}, k["max_cycle"],
                           {d: set(v) for d, v in k["altruists"].items()}, k["max_chain"])
    assert (r["pairs_only"], r["cycles"], r["with_chains"]) == (2, 6, 8)
    pv = mt.pivotal(**T["bridge"])
    assert pv["build"] and pv["tax"] == [15.0, 0.0, 0.0, 0.0]


def test_bilateral_trade_and_assignment_core():
    b = mt.bilateral_trade(draws=100000)
    assert abs(b["exact"]["double"] / b["exact"]["efficient"] - 27 / 32) < 1e-12
    assert abs(b["sim"]["efficient"] - 1 / 6) < 0.003
    g = mt.assignment_game(T["assignment"]["values"])
    assert g["total"] == 15.0 and g["assign"] == [1, 0]
    assert abs(sum(g["seller_optimal"]["sellers"]) - 14.0) < 1e-6
    assert abs(sum(g["buyer_optimal"]["buyers"]) - 13.0) < 1e-6


def test_lottery_study_needs_type_controls():
    p = dict(T["lottery"])
    p.pop("reps")
    r = mt.lottery_study(**p)
    assert r["offer_rate"]["siblings"] == 1.0 and r["offer_rate"]["others"] < 0.2
    assert abs(r["iv_type_controls"] - r["effect"]) < 0.1
    assert r["iv_no_controls"] < 0.2 and r["ols_everyone"] > 0.6
