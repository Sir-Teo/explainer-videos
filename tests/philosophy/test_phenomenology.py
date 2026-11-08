"""Tests for the Reasoner's phenomenology module (Part 29)."""

from explainer.philosophy.reasoner import phenomenology as H


def test_adumbrations_and_variation():
    a = H.adumbrations(n=2000)
    assert a["max_at_once"] == 3 and a["all_six"]
    assert H.visible_faces([2, 0, 0]) == ["+x"] and len(H.visible_faces([2, 2, 2])) == 3
    assert len(H.cube_profile(30, 20)) == 3
    e = {r["property"]: r for r in H.eidetic(n=2000)["rows"]}
    assert e["angles sum to 180"]["invariant"] and e["at least two acute angles"]["invariant"]
    assert not e["obtuse"]["invariant"] and not e["acute"]["invariant"]


def test_retention():
    r = H.retention()
    assert r["melodies"] == 120 and r["distinct"] == {"knife": 5, "window": 20, "retention": 120}
    assert r["decoded"] == 120


def test_frame_problem():
    c = H.axiom_counts()["rows"]
    assert c[1]["frame_axioms"] == 1000 and c[1]["ssa"] == 50
    r = H.robots(irrelevant=(0, 3))
    assert r["r1_outcome"]["bomb_out"] and r["plan"] == ["open_door", "remove_bomb", "pull_wagon_out"]
    assert r["rows"][1]["expanded"] > r["rows"][0]["expanded"] == r["rows"][1]["expanded_relevant"]


def test_vehicles_and_recurrence():
    b = H.braitenberg()["vehicles"]
    assert b["2b"]["min_dist"] < b["2a"]["min_dist"] and b["3a"]["final_dist"] < 2
    rc = H.recurrence(sizes=range(5, 10))
    assert all(t is not None for t in rc["periods"].values())
    assert all(x["closest"] > 0 for x in rc["simmel"])


def test_circle_procrustes_gaming_dictionary():
    h = H.hermeneutic()["texts"]
    assert all(r["final"] > 0.99 for r in h["the boatman's text"]["runs"])
    assert [r["final"] for r in h["a text that cannot answer back"]["runs"]] == [0.1, 0.9]
    p = H.procrustes()
    assert p["same_nn"] and p["resid"] < 1e-9 and p["cos_change"] < 1e-9 and abs(p["coord_corr"]) < 0.5
    g = H.gaming()
    assert g["precision_after"] < 0.8 and g["accepted_after"] > g["accepted_before"]
    d = H.dictionary()
    assert d["grounding_size"] == 3 and all(c[-1] in c[:-1] for c in d["chains"].values())
