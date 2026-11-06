"""Part 11's Reasoner: Gettier cases, sensitivity and safety, reliability, margins for error, coherence, the web."""

from explainer.philosophy.reasoner import knowledge as Kn


def test_gettier_cases_are_jtb_without_a_safe_basis():
    for name in Kn.GETTIER_CASES:
        g = Kn.gettier(name)
        assert g["valid"] and g["true"] and g["believed"] and g["justified"]
        assert g["false_lemma"] and not g["nearby_true"]


def test_sensitivity_and_safety():
    v = {r["p"]: r for r in Kn.verdicts(Kn.SCENARIOS["barns"], ["barn", "red barn"])}
    assert not v["barn"]["sensitive"] and v["red barn"]["sensitive"]          # Kripke's abominable conjunction
    v = {r["p"]: r for r in Kn.verdicts(Kn.SCENARIOS["biv"], ["hands", "not_biv"])}
    assert v["hands"]["sensitive"] and v["hands"]["safe"]
    assert not v["not_biv"]["sensitive"] and v["not_biv"]["safe"]           # the checkers disagree
    chute = Kn.verdicts(Kn.SCENARIOS["chute"], ["basement"])[0]
    assert not chute["sensitive"] and chute["safe"]
    for name in ("coins", "clock", "lottery"):
        sc = Kn.SCENARIOS[name]
        r = Kn.verdicts(sc, list(sc.props))[0]
        assert r["true"] and r["believed"] and not r["sensitive"] and not r["safe"]
    z = Kn.zagzebski()
    assert z["step2"]["true"] and not z["step1"]["true"] and not z["safe"]


def test_generality_problem():
    rates = {g["type"]: g["rate"] for g in Kn.generality()}
    assert rates["vision"] > 0.9 and rates["vision from the road in Barn County"] == 0.1
    assert rates["this very look, at this barn"] == 1.0


def test_margins_for_error():
    s = Kn.luminosity_series()
    assert s["gap"] == [10, 11] and s["first_warm"] == 12
    sets = Kn.iterate_k(range(31), lambda w: w <= 20, margin=1, depth=3)
    assert [max(x) for x in sets] == [20, 19, 18, 17]
    assert 19 in sets[1] and 19 not in sets[2]                              # K p without KK p


def test_coherence_and_web():
    f = Kn.coherence_flip()
    assert f["shogenji"][0] > f["shogenji"][1] and f["overlap"][0] > f["overlap"][1]
    assert abs(f["cross"] - 0.5) < 1e-6
    lo = [c for c in f["curve"] if c[0] < 0.5]
    hi = [c for c in f["curve"] if c[0] > 0.5]
    assert all(a < b for _, a, b in lo) and all(a > b for _, a, b in hi)
    assert Kn.revisions() == [["N"], ["K"], ["T"], ["L"], ["notO"]]
    ok, open_ = Kn.lewis_knows(Kn.BANK["possibilities"], {"open, as I saw two weeks ago"}, set())
    assert not ok and len(open_) == 2
