"""Psyche's reasoning module, Part 24: syllogisms by brute force and four accounts of people's answers; optimal
data selection; the Tower of Hanoi's state space, a goal stack and a hill-climber; the nine dots; structure
mapping; rotation fits; causal power; everyday predictions; and the two open datasets."""

import numpy as np
import pytest

from explainer.psychology import opendata
from explainer.psychology.psyche import reason as R


def test_valid_syllogisms():
    valid = [t for t in R.TASKS if R.valid_conclusions(t) != ["NVC"]]
    assert len(R.TASKS) == 64 and len(valid) == 27  # with existential presupposition
    assert "Aac" in R.valid_conclusions("AA1") and "Iac" in R.valid_conclusions("AA1")
    assert R.valid_conclusions("EA1") == ["Oca"]
    assert R.valid_conclusions("II1") == ["NVC"]
    assert R.valid_conclusions("IE1") == ["Oac"]


def test_accounts_and_parsing():
    assert R.predict("AE1", "atmosphere") == ["Eac"]
    assert R.predict("IA2", "phm") == ["Ica"]
    assert R.predict("EA4", "matching") == ["Eac", "Eca"]
    code, resp = R.parse_ccobra("Some;models;managers/All;models;clerks", "Some;managers;clerks")
    assert code == "IA4" and resp == "Iac"
    T = R.response_table(["AA1", "AA1"], ["Aac", "NVC"])
    assert T.shape == (64, 9) and T[0, 0] == pytest.approx(0.5)
    s = R.score(np.tile(np.eye(9)[0], (64, 1)), "logic")
    assert 0 <= s["coverage"] <= 1 and 0 <= s["hits"] <= 1


def test_selection_information_order():
    g = R.selection_information(0.1, 0.2)
    assert g["p"] > g["q"] > g["not-q"] > g["not-p"] >= 0
    # the not-q card's value depends only on P(p); the q card's falls as q becomes common
    assert R.selection_information(0.1, 0.9)["not-q"] == pytest.approx(g["not-q"])
    assert R.selection_information(0.1, 0.9)["q"] < g["not-q"]


def test_hanoi():
    S, E = R.hanoi_graph(3)
    assert len(S) == 27 and len(E) == 39
    assert len(R.hanoi_shortest((0, 0, 0), (2, 2, 2))) - 1 == 7
    g = R.goal_stack_solver(4)
    assert len(g["moves"]) == 15 and g["states"][-1] == (2, 2, 2, 2)
    assert int(np.argmax(g["latency"])) == 0
    p = R.hill_climb(3, rng=0)
    assert p[-1] == (2, 2, 2) and len(p) - 1 >= 7
    pos = R.hanoi_layout(3)
    assert len({tuple(np.round(v, 6)) for v in pos.values()}) == 27


def test_nine_dots():
    assert R.nine_dots(0, 2) == []
    out = R.nine_dots(-1, 3)
    assert len(out) == 16 and len(R.nine_dots(-2, 4)) == 16


def test_structure_map():
    base = [("cause", ("divide", "army"), ("converge", "army", "fortress")), ("command", "general", "army")]
    targ = [("cause", ("divide", "rays"), ("converge", "rays", "tumour")), ("command", "doctor", "rays")]
    m = R.structure_map(base, targ)
    assert m["mapping"]["army"] == "rays" and m["mapping"]["fortress"] == "tumour"
    assert m["mapping"]["general"] == "doctor"


def test_rotation_and_causes_and_everyday():
    a = np.repeat([0, 60, 120, 180], 10).astype(float)
    rt = 1000 + 10 * a
    f = R.rotation_fit(a, rt)
    assert f["slope"] == pytest.approx(10) and f["rate"] == pytest.approx(100)
    sim = R.rotation_model([0, 90], rate=90, t0=500, n=4000, rng=np.random.default_rng(0))
    assert sim[:, 0].mean() == pytest.approx(500) and sim[:, 1].mean() == pytest.approx(1500, rel=0.03)
    t = [[60, 40], [20, 80]]
    assert R.delta_p(t) == pytest.approx(0.4) and R.causal_power(t) == pytest.approx(0.5)
    assert R.predict_total(10, "power", gamma=1.0) == pytest.approx(20)
    assert 70 < R.predict_total(20, "gauss", mu=75, sigma=16) < 80
    assert R.predict_total(90, "gauss", mu=75, sigma=16) > 90


def test_open_data():
    if not (opendata.available("ragni_2016") and opendata.available("ganis_kievit_2015")):
        pytest.skip("the open data could not be fetched")
    s = opendata.syllogisms_ragni2016()
    assert len(s["id"]) == 8896 and len(np.unique(s["id"])) == 139
    m = opendata.mental_rotation()
    assert len(m["rt"]) == 5184 and len(np.unique(m["subject"])) == 54
    assert set(np.unique(m["angle"])) == {0.0, 50.0, 100.0, 150.0}
    ok = m["same"] & m["correct"]
    assert np.mean(m["rt"][ok & (m["angle"] == 150)]) > np.mean(m["rt"][ok & (m["angle"] == 0)]) + 1000
