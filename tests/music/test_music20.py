"""Part 20 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music20.py
"""

import numpy as np
import pytest

from explainer.music.monochord import canon as K
from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music20 import compute
from videos.music.music20.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def lines(rows):
    return [[tuple(x) for x in r] for r in rows]


def test_rounds_and_canons():
    r = load("rounds")
    assert r["n_tunes"] == 54 and r["known_ranks"] == {"Frère Jacques": 1, "Row, Row, Row Your Boat": 3, "Three Blind Mice": 4}
    c = load("canons")
    assert c["counts"]["fifth"] == 1378924 and c["counts"]["fourth"] == 479936 and c["total_melodies"] == 738663910
    assert min(c["counts"], key=c["counts"].get) == "fourth"
    for ex in c["examples"].values():
        assert ex["faults"]["dissonant"] == 0 and ex["faults"]["parallels"] == 0


def test_forms_invertible_augment_crab():
    f = load("forms")
    assert f["checked"] and [x[0] for x in f["forms"]["I"]] == [72, 72, 65, 65, 64, 64, 65]
    i = load("invertible")["lines"]
    assert i["plain"]["faults_original"]["dissonant"] == 0 and i["plain"]["faults_inverted"]["dissonant"] == 2
    assert i["safe"]["faults_inverted"]["dissonant"] == 0
    assert load("augment")["faults"]["dissonant"] == 3
    cr = load("crab")
    assert cr["counts"]["12"] == 193459554 and cr["melody"][:3] == [60, 67, 69] and cr["faults"]["dissonant"] == 0
    assert round(cr["counts"]["12"] / cr["counts"]["10"]) == 25


def test_rising_answers_exposition_stretto():
    ri = load("rising")
    assert ri["faults"]["dissonant"] == 0 and ri["laps"] == 7
    a = load("answers")
    assert [x[0] for x in a["real"]][:3] == [79, 79, 86] and [x[0] for x in a["tonal"]][:3] == [79, 79, 84]
    e = load("exposition")
    assert e["faults"]["dissonant"] == 0 and e["faults"]["parallels"] == 0 and e["faults"]["beats"] == 16
    s = load("stretto")
    assert len(s["all"]) == 11 and s["best"]["delay"] == 2.0 and s["best"]["interval"] == -5
    assert s["faults_three"]["dissonant"] == 0 and s["with_stretto"] == 41 and s["royal"]["earliest"] == 23.0
    assert len(s["by_inversion"]) == 15 and sum(1 for x in s["by_inversion"] if x["delay"] <= 2) == 6
    ep = load("episode")
    assert ep["faults"]["dissonant"] == 0 and ep["faults"]["parallels"] == 0 and ep["fragment"] == [67, 69, 67, 71]
    assert [x[0] for x in load("forms")["real_inversion"]] == [72, 72, 65, 65, 63, 63, 65]
    c = load("canons")
    assert c["counts"]["octave"] == c["counts_below"]["octave"] and c["counts_below"]["ninth"] < c["counts"]["ninth"]


def test_variation_20():
    t = load("tune")
    assert t["canon_faults"]["dissonant"] == 2 and t["canon_faults"]["beats"] == 46
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 20][0]
    assert v["part"] == 20 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)


def test_hook_builds_from_the_royal_theme_without_a_warm_cache(monkeypatch):
    from explainer.music.sound import Clip

    played = []
    def render(lines, **kwargs):
        played.extend(lines)
        return Clip(np.zeros(24000), events={f"v0.n{k}": float(k) for k in range(len(lines[0]))})

    monkeypatch.setattr(compute, "play_lines", render)
    monkeypatch.setattr(compute, "save", lambda *args, **kwargs: {"test": True})
    result = compute.compute_hook()
    assert played == [K.line(K.ROYAL_THEME, K.ROYAL_RHYTHM)]
    assert result["theme"] == compute.rows(played[0])
    assert len(result["times"]) == len(K.ROYAL_THEME)
