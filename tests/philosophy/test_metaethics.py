"""Checks for the Reasoner's metaethics module (Part 37)."""

from explainer.philosophy.reasoner import metaethics as M


def test_schurz_pattern():
    s = M.schurz_table()
    rows = {r["name"]: r for r in s["rows"]}
    assert s["hume_pattern_holds"]
    assert rows["Prior's tea: p, so p or Oq"]["valid"] and rows["Prior's tea: p, so p or Oq"]["idle"]
    assert not rows["ought from is: p, so Op"]["valid"]
    assert rows["a logical ought: so O(q or not q)"]["theorem"]


def test_norm_world_pairs_and_equilibrium():
    g = M.norm_world_pairs()
    assert g["valid"] and (g["n_pairs"], g["n_left"]) == (8, 2)
    e = M.re_experiments()
    assert e["base"]["keep"] == ["DDE", "S", "F", "H"] and e["greene"]["keep"] == ["U", "S"]


def test_debunking():
    d = M.debunking()
    assert d["corr_fitness"] > 0.7 and abs(d["corr_independent"]) < 0.2 < d["corr_third_factor"]
