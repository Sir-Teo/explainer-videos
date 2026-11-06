"""Part 15's Reasoner: Laplace, the wheel of reasons, the ravens, confirmation measures, grue, merging, Gold,
Putnam, Ockham, a Solomonoff mixture, MDL, no free lunch, and the straight rule."""

from fractions import Fraction

from explainer.philosophy.reasoner import induction as I


def test_laplace_and_wheel():
    assert I.succession(9, 10) == Fraction(10, 12)
    assert I.sunrise()["odds_against"] == I.sunrise()["days"] + 1
    good = [(r["similar"], r["dissimilar"]) for r in I.hetucakra() if r["verdict"] == "good"]
    assert good == [("all", "none"), ("some", "none")]
    assert sum(r["verdict"] == "contradictory" for r in I.hetucakra()) == 2


def test_ravens_and_measures():
    r = I.ravens()
    assert r["rise_raven"] > 0 and 0 < r["rise_shoe"] < 1e-5 < r["rise_raven"]
    o = I.ordinal_disagreement()
    assert o["difference_prefers"] != o["ratio_prefers"]


def test_grue_and_merging():
    g = I.grue()
    assert g["green_encoding_says_green"] > 0.99 and g["grue_encoding_says_blue"] > 0.99
    m = I.merging()
    assert m["gap"][-1] < 0.03 < m["gap"][0] and m["c"][-1] < 0.51


def test_learning_theory():
    assert I.gold_adversary(I.conservative_learner())["mind_changes"] >= 30
    d = I.putnam_diagonal(I.laplace_predictor)
    assert d["wrong"] == d["n"]
    o = I.ockham()
    assert o["ockham_retractions"] == 0 < o["bold_retractions"]


def test_simplicity_and_lunch():
    run = I.solomonoff_run("011", 18)
    assert all((r["p_one"] > 0.5) == (r["next"] == "1") for r in run[9:])
    assert I.mdl_degree()["best"] == 2
    nfl = I.no_free_lunch()
    assert all(abs(v - 0.5) < 1e-12 for v in nfl["accuracy"].values())
    smooth = I.smooth_world_lunch()["accuracy"]
    assert smooth["nearest neighbour"] > smooth["majority"] > smooth["anti-majority"]
    assert abs(I.straight_rule()["final"] - 0.3) < 0.03


def test_miller_tichy():
    m = I.miller_tichy()
    assert m["false_closer"] == 0 and m["pairs_checked"] == 127 * 254 and m["true_pairs_ordered"] > 0
    L = I.miller_language()
    assert (L["d1"], L["d2"]) == ("1/3", "1") and (L["d1_m"], L["d2_m"]) == ("1", "1/3")


def test_nfl_slice():
    s = I.nfl_slice()
    assert len(s["completions"]) == 16 and s["correct"] == [8, 8, 8, 8]


def test_meta_induction():
    m = I.meta_induction()
    assert max(m["regret"]) <= m["bound"]
    assert m["final_forecaster"] - min(m["final"].values()) <= m["bound"]


def test_explanationist():
    d = I.explanationist(runs=200)
    assert d["ibe"]["t90"] < d["bayes"]["t90"]
    assert d["ibe"]["false90"] > d["bayes"]["false90"] and d["ibe"]["brier"] > d["bayes"]["brier"]


def test_shattering():
    v = I.shattering()
    assert v["thresholds"]["vc"] == 1 and v["intervals"]["vc"] == 2
    assert v["intervals"]["rows"][2]["missing"] == ["101"]


def test_desiderata():
    t = I.desiderata(samples=300)["table"]
    survivors = [n for n, v in t.items() if v["hypothesis symmetry"] and not v["evidence symmetry"]
                 and not v["commutativity"]]
    assert survivors == ["difference", "log likelihood ratio", "Kemeny-Oppenheim"]
