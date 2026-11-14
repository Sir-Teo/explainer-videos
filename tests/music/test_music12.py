"""Part 12 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music12.py
"""

from itertools import combinations

import numpy as np
import pytest

from explainer.music.monochord import scales as S
from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music12 import compute
from videos.music.music12.manifest import SCENES

load = compute.load


def test_stacks_and_the_three_gap_theorem():
    s = load("stack")
    sizes = {r["n"]: [round(x) for x in r["sizes"]] for r in s["rows"]}
    assert sizes[5] == [294, 204] and sizes[6] == [294, 204, 90] and sizes[7] == [204, 90] and sizes[12] == [114, 90]
    assert all(len(sizes[n]) == 3 for n in (8, 9, 10, 11)) and s["chain"][:7] == ["F", "C", "G", "D", "A", "E", "B"]
    g = load("gaps")
    assert g["moments"] == [2, 3, 5, 7, 12, 17, 29, 41, 53] and g["all_at_most_three"]
    assert {2, 5, 12, 41, 53} <= set(g["convergent_denominators"])                  # the convergents of Part 6's continued fraction


def test_the_modes():
    m = load("modes")
    assert [r["name"] for r in m["rows"]] == ["Lydian", "Ionian", "Mixolydian", "Dorian", "Aeolian", "Phrygian", "Locrian"]
    assert m["rows"][0]["names"] == ["C", "D", "E", "F♯", "G", "A", "B"] and m["rows"][6]["names"] == ["C", "D♭", "E♭", "F", "G♭", "A♭", "B♭"]
    for a, b in zip(m["rows"], m["rows"][1:]):
        assert sum(x != y for x, y in zip(a["names"], b["names"])) == 1 and a["brightness"] == b["brightness"] + 1
    assert m["same_tune"] == ["Ionian", "Mixolydian"] and m["tune_changed"]["Lydian"] == [4] and m["tune_changed"]["Dorian"] == [3]
    assert m["quiz"] == {"A": "Dorian", "B": "Mixolydian"} and m["quiz_answer"] == "B"


def test_what_is_special_about_the_white_keys():
    w = load("why")
    assert w["formula"] == [0, 2, 4, 5, 7, 9, 11] and w["evenness"]["major"] == pytest.approx(w["evenness_best"], abs=1e-5)
    assert w["evenness_second"] < w["evenness_best"] and w["evenness"]["melodic minor"] < w["evenness_best"]
    assert w["vectors"]["major"] == [2, 5, 4, 3, 6, 1] and w["vectors"]["whole-tone"] == [0, 6, 0, 6, 0, 3] and w["deep"]
    assert w["common"][6] == 6 and w["common"][0] == 2                              # a fifth up keeps six notes; a semitone up, two
    assert all(len(v) == 2 for v in w["myhill"].values()) and w["myhill"]["4"] == [5, 6]
    deep = {S.steps_necklace(S.steps_of(c)) for c in combinations(range(12), 7) if S.is_deep(c)}
    assert deep == {S.steps_necklace(S.MAJOR), (1, 1, 1, 1, 1, 1, 6)}               # two deep sevens; only one of them is even


def test_minor_and_the_other_scales():
    mi = load("minor")
    assert mi["augmented_second"] == 3 and mi["harmonic"][6] == 11 and mi["melodic"][5] == 9 and mi["quiz_answer"] == "B"
    f = load("fewer")
    assert f["transpositions"] == {"pentatonic": 12, "whole-tone": 2, "octatonic": 3, "blues": 12, "major": 12, "chromatic": 1}
    assert f["vectors"]["whole-tone"][4] == 0 and f["vectors"]["pentatonic"][0] == 0 and f["vectors"]["pentatonic"][5] == 0
    h = load("halves")
    assert len(h["tetrachords"]) == 6 and h["scales_of_two_halves"] == 36 and h["melakartas"] == 72 and h["mela_count"] == [2, 6, 6] and h["modes_among"] == 6
    mp = load("maps")
    assert sum(mp["rast"]) == sum(mp["five"]) == sum(mp["major"]) == 1200 and mp["rast_quarters"] == [4, 3, 3, 4, 4, 3, 3]
    assert mp["minor_third"] < mp["rast_third"] < mp["major_third"]


def test_every_scale():
    e = load("every")
    assert e["total"] == e["listed"] == 352 and e["sum"] == 4224 and e["with_tonic"] == 2048
    assert e["counts"] == [1, 1, 6, 19, 43, 66, 80, 66, 43, 19, 6, 1, 1] and len(e["sevens"]) == 66 and e["sevens_with_tonic"] == 462
    assert len(e["plain"]) == 3 and e["diatonic"] in e["plain"] and e["quiz_answer"] == "B" and e["quiz_steps"][1] == [2, 2, 1, 2, 2, 2, 1]
    f = load("frontier")
    dia = [r for r in f["rows"] if r["steps"] == f["diatonic"]][0]
    assert f["roughness_rank"] == 1 and f["of"] == 66
    assert dia["fifths"] == 6 == max(r["fifths"] for r in f["rows"]) and dia["evenness"] == pytest.approx(max(r["evenness"] for r in f["rows"]))
    assert sum(r["fifths"] == 6 for r in f["rows"]) == 1 and f["five_best"] == f["pentatonic"]
    assert f["equal_step"] == pytest.approx(171.4, abs=0.1) and 300 < f["equal_third"] < 400 and 702 - f["equal_fifth"] == pytest.approx(16.2, abs=0.1)


def test_variation_12():
    t = load("tune")
    assert t["names"] == ["Lydian", "Ionian", "Mixolydian", "Dorian", "Aeolian", "Phrygian", "Locrian", "pentatonic", "whole-tone", "octatonic"]
    assert t["lowered"] == 6 and len(t["phrases"]) == 10
    ion, mix = t["phrases"][1], t["phrases"][2]
    assert 11 in {n % 12 for n in ion["under"]} or 11 in {n % 12 for n in t["phrases"][0]["under"]}        # the second voice uses the seventh ...
    assert 10 in {n % 12 for n in mix["under"]}                                                           # ... which is what makes Mixolydian audible
    for ph in t["phrases"]:
        assert all(n % 12 in ph["notes"] for n in ph["melody"] + ph["under"])
    v = load("variation")
    assert v["part"] == 12 and "6 notes" in v["measure"]


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
