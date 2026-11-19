"""Agora's social choice module (Part 18)."""

from explainer.economics.agora import choice as ch
from explainer.economics.island import truths

T = truths(18)
PROF = [(n, tuple(r)) for n, r in T["playit"]["profile"]]


def test_five_rules_five_winners_without_ties():
    w = ch.all_rules(PROF)
    assert [w[k] for k in ("plurality", "runoff", "instant runoff", "Borda", "Condorcet")] == list("ABCDE")
    assert sum(n for n, _ in PROF) == 38
    pts = sorted(ch.borda(PROF)["points"].values(), reverse=True)
    assert pts[0] > pts[1]


def test_condorcet_cycle_and_agendas():
    m = ch.majority_cycle()
    assert all(v == 2 for _, _, v in m["cycle"])
    assert m["agendas"] == {"A": 2, "B": 2, "C": 2}
    assert ch.transitivity_violation(m["profile"]) == [("A", "B", "C")]


def test_borda_fails_independence_and_blocs_can_manipulate():
    v = ch.iia_violation(PROF)
    a, b = v["pair"]
    assert (v["before"].index(a) < v["before"].index(b)) == (v["after"].index(a) < v["after"].index(b))
    assert (v["ranking_before"].index(a) < v["ranking_before"].index(b)) != \
        (v["ranking_after"].index(a) < v["ranking_after"].index(b))
    m = ch.manipulations(PROF, "Borda")
    assert m and all(m_["truth"].index(m_["new_winner"]) < m_["truth"].index(m_["honest_winner"]) for m_ in m)


def test_median_voter_and_pivot():
    sp = ch.single_peaked(**T["peaks"])
    assert sp["condorcet"] == sp["median"] == 3.0
    g = ch.geanakoplos_pivot(**T["arrow"])
    assert g["pivot"] == T["arrow"]["dictator"]


def test_welfare_veil_and_compensation():
    w = ch.welfare(T["incomes"])
    a = [w["atkinson"][e] for e in (0.0, 0.5, 1.0, 2.0, 5.0)]
    assert a == sorted(a) and a[0] == 0.0
    assert abs(w["ede"][1.0] - 20.0) < 1e-9
    v = ch.veil(T["veil"]["A"], T["veil"]["B"])
    assert v["rawls"] == "A" and v["harsanyi"][0.0] == "B" and v["harsanyi"][20.0] == "A"
    s = ch.scitovsky()
    assert s["1_to_2"] and s["2_to_1"]
