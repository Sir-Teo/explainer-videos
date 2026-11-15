"""Part 65 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music65.py
"""

import numpy as np
import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music65 import compute
from videos.music.music65.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_corpus_and_counting():
    c = load("corpus")
    assert c["hymn_tunes"] < c["tunes"] and c["test"] <= c["hymn_tunes"]
    m = load("markov")
    b = {int(k): v for k, v in m["bits"].items()}
    assert m["best"] == 2 and b[2] < b[0] and b[2] < b[8]
    s = load("surprise")
    assert min(s["markov_at_ends"], s["markov_after_ends"]) > s["markov_mean"]   # the boundaries surprise


def test_copying_trade():
    d = load("copy")
    o = d["orders"]
    assert o["1"]["share8"] < 0.05 < 0.8 < o["8"]["share8"] and o["8"]["longest"] > 3 * d["bach"]["longest"]
    assert o["2"]["share8"] < d["bach"]["share8"] < o["3"]["share8"]    # said in Chapter 3
    assert d["sample_copy"]["length"] >= 20


def test_constraints_and_recombination():
    c = load("constrained")
    assert c["p_legal"] < 0.02 and c["end"][2] and c["end"][0] % 12 == 0 and c["end"][1] >= 8
    r = load("recombine")
    assert len({s for s, _ in r["sources"]}) == 4 and r["share8"] > 0.5


def test_transformer_and_temperature():
    t = load("transformer")
    assert t["aug"]["bits"] < t["plain"]["bits"]                         # transposed copies help
    assert t["overtrained"]["share8"] > t["aug"]["share8"]               # trained too long, it recites
    assert t["memorized"]["copy"]["length"] >= 16
    tp = load("temperature")["rows"]
    temps = sorted(tp, key=float)
    assert tp[temps[0]]["chromatic"] < tp[temps[1]]["chromatic"] < tp[temps[-1]]["chromatic"]
    assert tp[temps[1]]["kl"] < min(tp[temps[0]]["kl"], tp[temps[-1]]["kl"])       # closest to Bach at T = 1
    assert tp[temps[0]]["cadence"] > max(tp[temps[1]]["cadence"], tp[temps[-1]]["cadence"])
    assert max(r["share8"] for r in tp.values()) < 0.05
    h = load("harmony")
    assert h["parallels"] == 0


def test_judges_and_quiz():
    j = load("judge")["rows"]
    assert j["order 8"]["share8"] > j["transformer"]["share8"] and j["recombined"]["share8"] > 0.5
    q = load("copyquiz")
    assert q["copied"] > q["copied_new"] + 0.3


def test_variation_65():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 65][0]
    assert v["part"] == 65 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)
    t = load("tune65")
    assert len(t["continuations"]) == 5 and all(len(c) > 0 for c in t["continuations"])


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
