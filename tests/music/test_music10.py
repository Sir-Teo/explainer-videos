"""Part 10 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music10.py
"""

import numpy as np
import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music10 import compute
from videos.music.music10.manifest import SCENES

load = compute.load


def test_the_tablet_and_the_neumes():
    h = load("hook")
    assert [n for _, n in h["line"]] == [3, 1, 3, 1, 10] and h["strokes_a"] == 18 and h["strokes_b"] == 23
    assert len(h["words_a"]) == len(h["words_b"]) == 5 and h["words_b"][0] > h["words_a"][-1]
    n = load("neumes")
    assert n["contour"] == [0, 1, 0, 1, 0, -1] and n["counts"] == {"6": 85, "7": 175, "8": 322}
    assert n["whole_tune_octave"] > 3e8 and n["melodies"][1] == n["steps"] and n["tune_is"] == "B"
    for m in n["melodies"]:                                                   # all three fit the signs
        assert [(b > a) - (b < a) for a, b in zip(m, m[1:])] == n["contour"]
    assert n["contour_bits"] == pytest.approx(9.5, abs=0.05) and n["pitch_bits"] == pytest.approx(18.1, abs=0.05)


def test_guido_and_franco():
    g = load("guido")
    assert [r["first"] for r in g["lines"][:6]] == ["C3", "D3", "E3", "F3", "G3", "A3"] and g["first_steps"] == [2, 2, 1, 2, 2]
    assert [r["syllable"] for r in g["lines"][:6]] == ["Ut", "re", "mi", "fa", "sol", "la"]
    m = load("mensural")
    assert m["two"]["total"] == 16 and m["three"]["total"] == 18                                  # the same marks: eight beats a phrase, or nine
    assert m["examples"] == {"BSB": [2, 1, 3], "BSSB": [3, 1, 2, 3], "BSSSB": [3, 1, 1, 1, 3]}
    assert m["dots"] == ["1", "3/2", "7/4", "15/8"] and m["ties"]["5/8"] == [["1/2", 0], ["1/8", 0]] and m["ties"]["7/8"] == [["1/2", 2]]


def test_what_to_do():
    t = load("tab")
    assert t["middle_c"] == [[2, 10], [3, 5], [4, 1]] and t["count_phrases"] == 2125764 and 2.1e19 < t["count_tune"] < 2.2e19
    assert max(f for _, f in t["best"]) <= 5 and t["cost_one"] > 1.8 * t["cost_best"]
    assert [compute.tab.GUITAR[s] + f for s, f in t["best"]] == t["keys"] == [compute.tab.GUITAR[s] + f for s, f in t["one_string"]]
    f = load("figured")
    assert f["count"] > 6e6 and f["parallels"] == [0, 0] and f["a"] != f["b"]
    for chords in (f["a_names"], f["b_names"]):
        for want, got, bass in zip(f["wanted"], chords, f["bass"]):
            assert {w[:-1] for w in want} <= {g[:-1] for g in got} <= {w[:-1] for w in want} | {bass[:-1]}


def test_numbers_and_bytes():
    e = load("east")
    assert e["jianpu"].startswith("1=C") and "1 1 5 5 | 6 6 5 - | 4 4 3 3 | 2 2 1 -" in e["jianpu"]
    assert "".join(e["gongche"]) == "上上六六五五六凡凡工工尺尺上"
    m = load("midi")
    assert m["size"] == 425 and m["per_note"] == 9 and m["key_number"] == 60 and m["velocity"] == 80
    assert bytes(m["bytes"][m["first"]: m["first"] + 9]).hex(" ") == "00 90 3c 50 83 60 80 3c 00"
    assert m["written"] == ["Eb4", "G4", "Bb4", "Eb5"] and m["read_back"] == ["D#4", "G4", "A#4", "D#5"]
    assert m["diesis_cents"] == pytest.approx(41.06, abs=0.01) and m["g_sharp"] < m["equal"] < m["a_flat"]
    assert m["pure_cents"] == pytest.approx(386.3, abs=0.1) and m["wolf_cents"] == pytest.approx(427.4, abs=0.1)
    x = load("xml")
    assert x["round_trip_same"] and x["midi_loses"] == {"spelling": True, "words": True, "keys": True}


def test_the_count():
    b = load("bits")
    s, a = b["sizes"], b["audio"]
    assert s["gongche"] < s["jianpu"] < s["MIDI"] < s["MEI"] < s["MusicXML"] < a["Opus"] < a["MP3"] < a["FLAC"] < a["WAV"]
    assert b["plain_bits"] == 168 and b["structured_bits"] == 96 and b["distinct_phrases"] == 3
    assert b["audio_bits"] == pytest.approx(b["seconds"] * 48000 * 16, rel=1e-3) and 1.2e5 < b["ratio"] < 1.35e5
    assert 5.5 < a["WAV"] / a["MP3"] < 6.5 and 15 < a["WAV"] / a["Opus"] < 17
    assert b["quiz_answer"] == "B" and 40 < b["largest_ms"] < 100 and 6 < b["db_range"] < 10 and 1.4 < b["last_ratio"] < 1.6
    assert b["perf_bits"] == 42 * 19 and 2.0e4 < b["audio_bits"] / (b["perf_bits"] + b["plain_bits"]) < 2.4e4
    dead = np.diff(b["times"]["B"])
    assert np.allclose(dead[:6], dead[0]) and not np.allclose(np.diff(b["times"]["A"])[:6], dead[0], atol=0.005)       # B is the machine


def test_reading_the_page_back():
    o = load("omr")
    assert o["clean_accuracy"] == 1.0 and len(o["lines"]) == 15
    naive, fixed = np.asarray(o["naive"]), np.asarray(o["deskewed"])
    assert o["breaks_at"] == pytest.approx(0.4) and (naive[:4] > 0.95).all() and (naive[4:] == 0).all() and (fixed > 0.95).all()
    sp = np.asarray(o["speck_accuracy"])
    assert sp[0] == 1.0 and sp[-1] < 0.1 and (np.diff(sp) <= 0.01).all()
    assert o["bad_wrong"] == sum(o["bad_flags"]) == 4 and o["bad_notes"] == 29
    wrong = [k for k, f in enumerate(o["bad_flags"]) if f]
    extra = [k for k in wrong if o["bad_names"][k] == "F4"]                    # one note that is not on the page ...
    assert len(extra) == 1 and all(o["bad_beats"][k] == 2 for k in wrong if k not in extra)       # ... and three quarters read as halves


def test_variation_10():
    t = load("tune")
    assert len(t["pairs"]) == 6 and sum(len(p) for p in t["pairs"][:5]) == 10
    assert t["late_ms"][0] == 0 and max(abs(m) for m in t["late_ms"]) > 20 and t["last_ratio"] > 1.4
    v = load("variation")
    assert v["part"] == 10 and "168 bits" in v["measure"] and "127" in v["measure"]


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
