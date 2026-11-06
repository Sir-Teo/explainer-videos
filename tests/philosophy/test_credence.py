"""Part 13's Reasoner: Dutch books, accuracy, scoring rules, conditioning, indifference, dilation, stability,
Sleeping Beauty and Doomsday."""

from explainer.philosophy.reasoner import credence as Cr


def test_dutch_book_and_accuracy():
    W = ["w1", "w2"]
    props = {"A": {"w1"}, "notA": {"w2"}}
    book = Cr.dutch_book(W, props, {"A": 0.6, "notA": 0.6})
    assert book and abs(book["sure_loss"] - 0.2) < 1e-6 and all(v < 0 for v in book["payoff"].values())
    assert Cr.coherent(W, props, {"A": 0.6, "notA": 0.4})
    d = Cr.dominance([0.5, 0.4, 0.3])
    assert d["dominates"] and abs(sum(d["projection"]) - 1) < 1e-9


def test_scoring_rules():
    for rule in ("brier", "log", "spherical"):
        assert abs(Cr.best_report(rule, 0.7) - 0.7) < 0.002
    assert Cr.best_report("linear", 0.7) > 0.99                      # the linear rule is improper
    f = Cr.forecasters()
    assert min(f, key=lambda k: f[k]["brier"]) == "calibrated"


def test_conditioning():
    book = Cr.diachronic_book(0.5, 0.6, 0.4)
    assert all(abs(v + 0.1) < 1e-9 for v in book.values())
    j = Cr.jeffrey(Cr.JEFFREY_CLOTH["prior"], Cr.JEFFREY_CLOTH["post"], Cr.JEFFREY_CLOTH["sold"])
    assert abs(j["old"] - 0.56) < 1e-9 and abs(j["new"] - 0.42) < 1e-9
    p = Cr.maxent_die(4.5)
    assert abs(sum(k * x for k, x in zip(range(1, 7), p)) - 4.5) < 1e-9 and p == sorted(p)


def test_indifference_and_imprecision():
    b = Cr.bertrand(40000)
    for v in b.values():
        assert abs(v["freq"] - v["exact"]) < 0.01
    d = Cr.dilation()
    assert d["before"] == [0.5, 0.5] and d["after"] == [0.0, 1.0]


def test_belief_and_self_location():
    assert Cr.lottery()["believe_each"] and not Cr.lottery()["believe_all"]
    assert Cr.stable_sets({"a": 0.54, "b": 0.34, "c": 0.1, "d": 0.02})[0] == ["a"]
    s = Cr.sleeping_beauty(20000)
    assert abs(s["heads_per_experiment"] - 0.5) < 0.02 and abs(s["heads_per_awakening"] - 1 / 3) < 0.02
    dd = Cr.doomsday()
    assert dd["ssa_soon"] > 0.99 and abs(dd["sia_soon"] - 0.5) < 1e-9
