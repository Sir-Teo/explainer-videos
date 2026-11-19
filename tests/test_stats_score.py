"""The computed score of *Statistics, Built* (explainer/stats/score.py): deterministic, at its levels, never under the
narration except where it is meant to be (the stings under the chapter titles), and placed on the marks the watch
kit records (videos/stats/SYLLABUS.md 1.2)."""

import numpy as np
import pytest

from explainer.stats import score

TIMELINE = [
    {"video": "stats12", "cls": "Hook", "chapter": "Ceres, lost and found", "start": 0.0, "duration": 120.0,
     "lines": [{"start": 0.0, "duration": 40.0}, {"start": 50.0, "duration": 60.0}],
     "marks": [{"name": "title", "time": 111.0}]},
    {"video": "stats12", "cls": "Principle", "chapter": "1. The principle", "start": 120.0, "duration": 240.0,
     "lines": [{"start": 0.3, "duration": 2.0}, {"start": 6.0, "duration": 5.0}, {"start": 20.0, "duration": 150.0},
               {"start": 200.0, "duration": 6.0}],
     "marks": [{"name": "card", "time": 0.0}, {"name": "countdown:3", "time": 11.5},
               {"name": "reveal", "time": 200.2}, {"name": "strike", "time": 180.0}]},
    {"video": "stats12", "cls": "Outro", "chapter": "Recap, problems, and the road ahead", "start": 360.0,
     "duration": 60.0, "lines": [{"start": 0.0, "duration": 30.0}, {"start": 40.0, "duration": 10.0}],
     "marks": [{"name": "countdown:4", "time": 31.0}]},
]


def speech(timeline):
    return [(s["start"] + x["start"], s["start"] + x["start"] + x["duration"]) for s in timeline for x in s["lines"]]


def test_the_stages_match_the_series():
    from explainer.stats import MILESTONES, STAGES

    assert [r for _, r in STAGES] == score.STAGE_PARTS
    assert tuple(sorted(MILESTONES)) == score.MILESTONES
    assert [score.stage(p) for p in (1, 10, 11, 20, 21, 42, 43, 55, 56, 65)] == [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]


def test_the_board():
    assert score.path(5, 4) == [1, -1, 1, -1]
    times = score.fall_times(6, 1.8)
    gaps = np.diff([0.0] + times)
    assert times[-1] == pytest.approx(1.8) and all(np.diff(gaps) < 0)  # a falling ball: the pegs come faster
    b = score.bell(6)
    assert [s for s, _ in b] == [-6, -4, -2, 0, 2, 4, 6] and sum(w for _, w in b) == pytest.approx(1.0)
    assert max(b, key=lambda x: x[1])[0] == 0  # the centre bin, the tonic, is the loudest note of the bell
    assert score.pitch(0) == pytest.approx(261.6256) and score.pitch(5) == pytest.approx(2 * 261.6256)
    assert score.pitch(3) == pytest.approx(261.6256 * 2 ** (7 / 12))  # G4: the pentatonic's fourth step


@pytest.mark.parametrize("make,target", [(lambda: score.theme(12), score.THEME_LUFS),
                                         (lambda: score.sting(5, 30), score.STING_LUFS),
                                         (lambda: score.pulse(3, 44), score.PULSE_LUFS),
                                         (lambda: score.chime(60), score.CHIME_LUFS),
                                         (lambda: score.thud(2), score.CHIME_LUFS),
                                         (lambda: score.bed(6.0), score.BED_LUFS),
                                         (lambda: score.close(65), score.THEME_LUFS)])
def test_levels_and_determinism(make, target):
    a, b = make(), make()
    assert np.array_equal(a, b)
    assert abs(score.lufs(a) - target) < 0.05
    assert np.abs(a).max() < 0.5  # far below full scale: the narration owns the headroom
    assert abs(float(a.mean())) < 1e-3  # no offset


def test_each_stage_has_its_own_instrument():
    clips = [score.sting(3, part) for part in (5, 15, 30, 50, 60)]
    for i in range(len(clips)):
        for j in range(i + 1, len(clips)):
            assert not np.allclose(clips[i], clips[j])
    assert np.allclose(score.sting(3, 1), score.sting(3, 10))  # one instrument through a stage


def test_cues(tmp_path):
    cues = score.cues(TIMELINE, tmp_path)
    by = {c["label"]: c for c in cues}
    assert by["score: theme_p12"]["start"] == pytest.approx(111.0)  # at the title, after the cold open
    assert by["score: sting1_s1"]["start"] == pytest.approx(120.05)
    assert by["score: pulse3_s1"]["start"] == pytest.approx(131.5)
    assert by["score: pulse4_s1"]["start"] == pytest.approx(391.0)
    assert by["score: chime_s1"]["start"] == pytest.approx(320.2)
    assert by["score: thud_s1"]["start"] == pytest.approx(300.0)
    close = by["score: close_p12"]
    assert close["start"] + close["duration"] == pytest.approx(420.0)
    assert [c["start"] for c in cues] == sorted(c["start"] for c in cues)
    talk = speech(TIMELINE)
    beds = [c for c in cues if c["label"].startswith("score: bed")]
    assert beds  # the dead air in the chapter and the problems' pause get one
    for c in beds:  # beds only in silence, never under a voice or another cue
        a, b = c["start"], c["start"] + c["duration"]
        assert all(b <= s or a >= e for s, e in talk), c
        others = [o for o in cues if o is not c and not o["label"].startswith("score: close")]
        assert all(b <= o["start"] or a >= o["start"] + o["duration"] for o in others), c
    assert all((tmp_path / score.VERSION / p.split("/")[-1]).exists() for p in [c["path"] for c in cues])


def test_no_title_mark_puts_the_theme_first(tmp_path):
    tl = [dict(TIMELINE[0], marks=[])] + TIMELINE[1:]
    cues = score.cues(tl, tmp_path)
    assert cues[0]["label"] == "score: theme_p12" and cues[0]["start"] == 0.0


def test_build_finds_the_score():
    import importlib
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
    build = importlib.import_module("build")
    assert build.series_score("stats12") is score


def test_chapter_numbers():
    assert score.chapter_number("7. The bootstrap") == 7
    assert score.chapter_number("III. Testing and asymptotics: Problems 5-6") == 3
    assert score.chapter_number("IV. Empirical processes") == 4 and score.chapter_number("IX. x") == 9
    assert score.chapter_number("Ceres, lost and found") is None
    assert score.chapter_number("Recap, problems, and the road ahead") is None
