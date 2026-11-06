"""Part 14's Reasoner: AGM revision, iterated revision, Gärdenfors's impossibility, conditionals and triviality,
default logic, System Z, KLM, and Dung's argumentation."""

from explainer.philosophy.reasoner import argue as G
from explainer.philosophy.reasoner import cond as C
from explainer.philosophy.reasoner import revision as R


def test_agm():
    t = R.postulate_table()
    assert all(v["holds"] for v in t["spheres (a ranking)"].values())
    assert all(v["holds"] for v in t["Dalal (distance)"].values())
    assert not t["Satoh (set inclusion)"]["K*8"]["holds"]
    rank = {w: i for i, w in enumerate(R.worlds(("p", "q")))}
    assert R.identities_hold(rank) == {"levi": True, "harper": True}
    bm = R.book_and_magazine()
    assert bm["revision"] == ["~bm"] and bm["update"] == ["~bm", "~b~m"]


def test_iterated_and_gardenfors():
    t = R.dp_table()
    assert all(v["holds"] for v in t["natural (Boutilier)"].values())
    assert all(v["holds"] for v in t["lexicographic (Nayak)"].values())
    assert not t["amnesic"]["DP2"]["holds"]
    demo = R.iterate_demo()
    assert demo["natural"]["still believes f"] and not demo["amnesic"]["still believes f"]
    assert R.gardenfors()["survivors"] == []


def test_conditionals():
    for name, v in C.classic_models().items():
        assert all(v["premises_hold"]) and not v["conclusion_holds"] and v["material_valid"], name
    assert C.cem_stalnaker()["cem"]
    assert C.lewis_proof()["contradiction"]
    assert C.triviality_search()["winners"] == []
    assert C.triviality_search(("AC", "~AC", "~A~C"))["winners"]           # trivial: no A-and-not-C world
    d = C.imaging_demo()
    assert abs(d["P_A(C)"] - 0.6) < 1e-9 and abs(d["P(C|A)"] - 0.5) < 1e-9


def test_defeasible():
    assert G.tweety()["penguin_flies"] == [False]
    assert len(G.nixon()["extensions"]) == 2
    q = {(x["a"], x["b"]): x["holds"] for x in G.penguins()["queries"]}
    assert q[("b", "f")] and q[("p", "~f")] and q[("b & r", "f")] and not q[("p", "w")]
    k = G.klm_table()
    assert k["ranked"]["Rational Monotonicity"]["holds"] and not k["preferential"]["Rational Monotonicity"]["holds"]
    assert not k["ranked"]["Monotonicity"]["holds"]


def test_argumentation():
    t = G.argue_table()
    assert t["reinstatement"]["grounded"] == ["a", "c"]
    assert t["mutual attack"]["preferred"] == [["a"], ["b"]] and t["mutual attack"]["grounded"] == []
    assert t["odd cycle"]["stable"] == []
    assert t["trial"]["grounded"] == ["P1", "P2", "P3"]
