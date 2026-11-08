"""Checks for the Reasoner's aesthetics module (Part 40)."""

from explainer.philosophy.reasoner import aesthetics as A


def test_tuning_and_roughness():
    t = A.tuning()
    assert t["comma_num"] == 531441 and t["comma_den"] == 524288 and abs(t["comma_cents"] - 23.46) < 0.01
    c = A.dissonance_curve()
    assert [m["nearest_just"] for m in c["minima"]] == ["6:5", "5:4", "4:3", "3:2", "5:3", "2:1"]
    assert all(abs(m["off_cents"]) < 1 for m in c["minima"])
    s = A.dissonance_curve(stretch=2.1)
    assert abs(s["minima"][-1]["ratio"] - 2.1) < 0.005


def test_wallpaper_groups():
    w = A.wallpaper()
    assert w["distinct"] == 17 and w["all_seventeen"]


def test_compression_golden_critics():
    c = {x["image"]: x["ratio"] for x in A.compressibility()["images"]}
    assert c["blank"] < c["rule 90"] < c["noise"] and c["rule 30"] >= 1.0
    p = A.compression_progress()
    assert p["rule 30"]["progress"] > 10 * p["noise"]["progress"]
    g = A.golden()
    assert 0.5 < g["p_some_hit"] < 0.9
    k = A.critics(trials=50)
    assert k["correlation"]["true judges"][-1] > 0.99 and k["correlation"]["prejudiced judges"][-1] < 0.7


def test_temperaments_elements_sunflower():
    t = {s["system"]: s for s in A.temperaments()["systems"]}
    assert t["quarter-comma meantone"]["third_error"] == 0.0 and t["Pythagorean"]["major_third"] == 407.82
    e = A.elements("p4m")
    assert sum(c["order"] == 4 for c in e["centres"]) == 8 and e["mirrors"] and e["glides"]
    p = A.phyllotaxis()
    gaps = [x["min_gap"] for x in p["patterns"]]
    assert gaps[1] > gaps[0] and gaps[1] > gaps[2]
