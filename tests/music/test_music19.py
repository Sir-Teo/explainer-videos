"""Part 19 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music19.py
"""

import pytest

from explainer.music.monochord import fourpart as F
from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music19 import compute
from videos.music.music19.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def no_parallels(chords):
    return not any(F.parallels(a, b) for a, b in zip(chords, chords[1:]))


def test_applied_mixture_and_the_predominants():
    a = load("applied")
    assert a["bach_beats"] == 10014 and sum(a["bach"].values()) == 934 and round(100 * a["bach_share"]) == 9
    assert max(a["bach"], key=a["bach"].get) == "II"
    assert no_parallels(a["chords"])
    mx = load("mixture")
    assert sum(mx["bach"].values()) == 70 and mx["bach"]["♭VII"] == 54
    assert mx["final"]["0 major"] == 105 and mx["final"]["0 major"] + mx["final"]["0 minor"] == 116
    assert no_parallels(mx["picardy"]["Picardy"]) and mx["picardy"]["Picardy"][-1][0] % 12 == 4
    n = load("neapolitan")
    assert sorted({p % 12 for p in n["neapolitan"][1]}) == [1, 5, 8] and n["neapolitan"][1][3] % 12 == 5   # N6: F in the bass
    s = load("sixths")
    for name in ("Italian", "French", "German"):
        ch = s[name]["chords"]
        assert ch[1][3] % 12 == 8 and 6 in {p % 12 for p in ch[1]} and ch[2][3] % 12 == 7            # A♭ bass, F♯ above, to G


def test_dim7_trapdoor_and_comma():
    d = load("dim7")
    assert [r["name"] for r in d["resolutions"]] == ["C minor", "E♭ minor", "F♯ minor", "A minor"]
    for r in d["resolutions"]:
        first, res = r["chords"]
        assert sorted({p % 12 for p in first}) == [2, 5, 8, 11]
        assert first[3] % 12 == r["leading"] and res[3] - first[3] == 1                                # the bass rises a semitone
    t = load("trapdoor")
    assert t["same"] and {p % 12 for p in t["home"][2]} == {p % 12 for p in t["away"][2]}
    c = load("comma")
    assert round(c["four minor thirds"], 1) == 62.6 and round(c["three major thirds"], 1) == -41.1 and round(c["beat_hz"]) == 10


def test_mediants_paths_tension_and_tristan():
    m = load("mediants")
    assert m["names"] == ["C", "Cm", "A♭", "A♭m", "E", "Em", "C"] and m["voice_leading"] == [1] * 6
    p = load("paths")
    assert sum(v == 1 for v in p["pivots"].values()) == 11 and sum(v == 1 for v in p["chromatic"].values()) == 19
    t = load("tension")
    assert max(t["diatonic"]["tension"]) == 7 and max(t["mixture"]["tension"]) == 19 and max(t["trapdoor"]["tension"]) == 18
    assert t["examples"] == {"I-V": 5, "I-ii": 8, "I-vi": 7, "C to F# major": 23}
    tr = load("tristan")
    assert tr["half_dim"] and tr["voice_leading"]["cost"] == 2 and len(tr["readings"]) == 4


def test_variation_19():
    t = load("tune")
    for name, v in t["versions"].items():
        assert v["parallels"] == []
        mel = v["melody"]
        for k, ch in enumerate(v["chords"]):
            here = [p for p, a, d in mel if 2 * k <= a < 2 * k + 2]
            assert ch[0] == here[0]                                                   # the Tune's note on top of every chord
    assert t["outside_c"] == 13
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 19][0]
    assert v["part"] == 19 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
