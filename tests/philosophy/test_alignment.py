"""Checks for the Reasoner's alignment module (Part 42)."""


from explainer.philosophy.reasoner import alignment as A


def test_goodhart_bends_over_only_with_heavy_tails():
    g = A.goodhart(ns=(1, 8, 512, 4096), trials=1500)
    light, heavy = g["light"]["true"], g["heavy"]["true"]
    assert light == sorted(light)                      # Gaussian error: more pressure, more true value
    assert heavy[1] > 0.4 and heavy[-1] < 0.1           # heavy tails: rises, then falls back to the mean


def test_no_free_lunch_pairs_reproduce_the_policy():
    d = A.no_free_lunch()
    assert all(p["error"] < 1e-12 for p in d["pairs"])
    assert {p["best"] for p in d["pairs"]} == {"tea", "water", None}


def test_off_switch_rational_human_never_discourages_deference():
    for mu in (-1.5, -0.2, 0.0, 0.7, 2.0):
        for s in (0.0, 0.5, 2.0):
            v = A.off_switch_values(mu, s)
            assert v["incentive"] >= -1e-12
            if s == 0:
                assert abs(v["incentive"]) < 1e-12
    assert A.off_switch_values(0.5, 1.0, 0.5)["incentive"] < 0


def test_power_seeking_fractions_approach_k_over_k_plus_one():
    d = A.power_seeking(samples=20000)
    assert abs(d["to_hub"] - 0.75) < 0.02
    assert d["power"]["hub"] > d["power"]["off"]


def test_lob_axiom_characterizes_strict_partial_orders():
    rows = A.lob_frames(3)["rows"]
    assert [r["lob_valid"] for r in rows] == [1, 3, 19]
    assert all(r["agree"] == r["frames"] for r in rows)
    assert rows[-1]["four_valid"] == 171 and rows[-1]["T_valid"] == 64


def test_modal_combat_lobian_cooperation():
    t = A.modal_combat()["table"]
    assert t["FairBot|FairBot"] == "C" and t["FairBot|DefectBot"] == "D"
    assert t["PrudentBot|CooperateBot"] == "D" and t["PrudentBot|PrudentBot"] == "C" and t["PrudentBot|FairBot"] == "C"
