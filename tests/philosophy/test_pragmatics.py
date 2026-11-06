"""Tests for the Reasoner's pragmatics toolkit (Part 28)."""

from explainer.philosophy.reasoner import pragmatics as G


def test_tractatus_family_and_quus():
    o = G.operation_n()
    assert o["count"] == 16 and o["max_steps"] == 3
    f = G.family()
    assert f["common"] == [] and f["connected"]
    pq = G.plus_quus(n_history=300)
    assert pq["agree"] == 300 and pq["plus_68_57"] == 125 and pq["quus_68_57"] == 5
    assert pq["rival_bounds_below_200"] > 100


def test_quine_and_charity():
    p = G.proxy(n_sentences=120)
    assert p["same_truth_value"] == p["sentences"] == 120 and p["predicates_changed"] > 0
    assert G.gavagai()["same_assent"]
    c = G.charity()
    assert c["best_is_truth"] and c["best_agree"] < c["observations"]


def test_rsa():
    rg = G.reference_game()
    assert rg["L1"][0][0] > rg["L1"][0][1]          # 'blue' -> the blue square
    sc = G.scalar()
    some = sc["L1"][1]
    assert some[3] < 0.05 and abs(some[1] - some[2]) < 1e-6   # 'some' -> not all


def test_signalling_and_vectors():
    s = G.signalling(2, rounds=1500, runs=40)
    assert s["mean_final"] > 0.9
    v = G.vectors()
    assert v["nearest"]["cat"][0][0] == "dog"
    pr = G.probe()
    assert pr["category_right"] >= 14 and pr["fiction_right"] <= 3


def test_sweep_recursion_scorekeeping():
    sw = G.charity_sweep(noises=(0.0, 2 / 3), trials=30)
    assert sw["rows"][0]["right"] == 30 and sw["rows"][1]["right"] < 15
    lv = G.recursion()
    assert lv["blue_square"][1] == 0.6 and all(a <= b for a, b in zip(lv["blue_square"], lv["blue_square"][1:]))
    assert all(a > b for a, b in zip(lv["some_all"], lv["some_all"][1:]))
    sk = G.scorekeeping()["moves"]
    assert sk[2]["score"]["A"]["red"] and not sk[-1]["score"]["A"]["red"] and sk[-1]["score"]["A"]["west"]
    assert not sk[-1]["score"]["B"]["red"]
    assert abs(G._mutual_info([[1, 0, 0], [1, 0, 0], [0, 1, 0]]) - 0.9183) < 1e-3
    assert G.analogies()["rows"][0]["right"]
