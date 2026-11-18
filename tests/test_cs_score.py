"""The computed score of *Computer Science, Built* (explainer/cs/score.py): it never plays under narration except
the stings and the theme it is meant to, it is deterministic, and it sits where the standard says (SYLLABUS 1.2)."""

import numpy as np
import pytest

from explainer.cs import score

TIMELINE = [
    {"video": "cs7", "cls": "Hook", "chapter": "Five instructions at once", "start": 0.0, "duration": 90.0,
     "lines": [{"start": 0.0, "duration": 20.0}, {"start": 30.0, "duration": 40.0}],
     "marks": [{"name": "title", "time": 72.0}]},
    {"video": "cs7", "cls": "IronLaw", "chapter": "1. The iron law", "start": 90.0, "duration": 200.0,
     "lines": [{"start": 3.0, "duration": 60.0}, {"start": 70.0, "duration": 100.0}],
     "marks": [{"name": "countdown", "time": 64.0}]},
    {"video": "cs7", "cls": "Outro", "chapter": "Recap", "start": 290.0, "duration": 60.0,
     "lines": [{"start": 0.0, "duration": 50.0}], "marks": []},
]


def speech(timeline):
    return [(s["start"] + x["start"], s["start"] + x["start"] + x["duration"]) for s in timeline for x in s["lines"]]


def test_bits_and_tempo():
    assert score.bits(5) == [0, 2] and score.bits(7) == [0, 1, 2] and score.bits(8) == [3]
    assert score.tempo(7) > score.tempo(6) and score.tempo(10) > score.tempo(9) and score.tempo(11) == score.tempo(1)


@pytest.mark.parametrize("make,target", [(lambda: score.theme(7), score.THEME_LUFS),
                                         (lambda: score.sting(5), score.STING_LUFS),
                                         (lambda: score.pulse(3), score.PULSE_LUFS),
                                         (lambda: score.bed(6.0), score.BED_LUFS),
                                         (lambda: score.close(7), score.THEME_LUFS)])
def test_levels_and_determinism(make, target):
    a, b = make(), make()
    assert np.array_equal(a, b)
    assert abs(score._lufs(a) - target) < 0.05
    assert np.abs(a).max() < 0.5  # far below full scale: the narration owns the headroom


def test_cues(tmp_path):
    cues = score.cues(TIMELINE, tmp_path)
    by = {c["label"]: c for c in cues}
    assert by["score: theme_120"]["start"] == pytest.approx(72.0)  # at the title, after the cold open
    assert by["score: sting1"]["start"] == pytest.approx(90.05)
    assert by["score: pulse3"]["start"] == pytest.approx(154.0)
    assert cues[-1]["label"].startswith("score: close") and cues[-1]["start"] + cues[-1]["duration"] == \
        pytest.approx(350.0)
    talk = speech(TIMELINE)
    for c in cues:
        if c["label"].startswith("score: bed"):  # beds only in silence, never under a voice or another cue
            a, b = c["start"], c["start"] + c["duration"]
            assert all(b <= s or a >= e for s, e in talk), c
            others = [o for o in cues if o is not c and not o["label"].startswith("score: close")]
            assert all(b <= o["start"] or a >= o["start"] + o["duration"] for o in others), c
    assert all((tmp_path / score.VERSION).joinpath(p.split("/")[-1]).exists() for p in [c["path"] for c in cues])
