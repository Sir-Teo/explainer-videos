"""Checks for the Reasoner's population module (Part 36)."""

from explainer.philosophy.reasoner import population as P


def test_sequence_and_addition():
    s = P.parfit_sequence()
    assert s["best"]["total"] == "Z" and s["best"]["average"] == "A"
    m = P.mere_addition()["verdicts"]
    assert m["average"]["A+ vs A"] == "worse" and m["total"]["C vs A"] == "better"
    assert P.very_repugnant()["units"] == 601


def test_arrhenius_every_view_fails_something():
    t = P.arrhenius_table()
    assert all(t["violations"][v] for v in P.VIEWS)
    assert all(t["table"][v]["dominance"]["holds"] for v in P.VIEWS)


def test_discounting_risk_fanaticism():
    r = P.ramsey()
    assert r["views"]["Stern"]["r"] == 1.4 and r["views"]["Nordhaus"]["r"] == 5.5
    rates = r["weitzman"]["rate"]
    assert all(a >= b for a, b in zip(rates, rates[1:]))
    x = P.existential()
    assert abs(x["constant_gain"] - x["closed_constant"]) < 1e-3 and abs(x["perils_gain"] - x["closed_perils"]) < 0.1
    f = P.fanaticism()
    assert f["peak_bounded"] == 3 and f["discount_breaks_at"] == 10


def test_infinite_and_prices():
    i = P.infinite()
    assert i["dominated_after_swap"] and (i["liminf_ab"], i["liminf_ba"]) == (0, -1)
    assert P.vsl()["vsl"] == 12e6
    c = P.cost_effectiveness()
    assert c["ratio_best_median"] > 10


def test_neutrality_policy_three_qaly():
    assert P.neutrality()["count"] == 6
    c = P.climate_policy()
    assert c["Stern"]["worth_it"] and not c["Nordhaus"]["worth_it"]
    t = P.three_outcomes()
    assert t["person_affecting"]["ratio_23_12"] < 0.02 and t["total"]["ratio_23_12"] > 1e6
    q = P.qaly_allocation()
    assert q["best"]["qalys"] == "aged 30" and q["patients"][0]["priority"] == q["patients"][1]["priority"]
