"""The computed score of Psychology, Built (explainer/psychology/score.py)."""

import numpy as np

from explainer.psychology import score


def test_levels_and_peaks():
    for y, target in ((score.theme(), score.THEME_LUFS), (score.close(), score.THEME_LUFS),
                      (score.sting(3), score.STING_LUFS), (score.bed(6.0), score.BED_LUFS)):
        assert y.ndim == 2 and y.shape[1] == 2
        assert abs(score._lufs(y.astype(float)) - target) < 0.05
        assert np.max(np.abs(y)) < 0.5            # far below full scale: the narration is the loud part
        assert np.all(np.abs(y[:10]) < 1e-3)      # every clip fades in: no click


def test_deterministic_and_chapters_differ():
    assert np.array_equal(score.sting(1), score.sting(1))
    assert not np.array_equal(score.sting(1), score.sting(2))


def test_gaps():
    lines = [{"start": 0.5, "duration": 4.0}, {"start": 10.0, "duration": 2.0}]
    assert score.gaps(lines, 20.0) == [(4.5, 10.0), (12.0, 20.0)]
    assert score.gaps(lines, 20.0, skip_tail=6.0) == [(4.5, 10.0)]
    assert score.gaps(lines, 13.0) == [(4.5, 10.0)]        # 1 s at the end is not dead air
    assert score.gaps(lines, 20.0, skip_head=8.0) == [(12.0, 20.0)]   # 2 s left after the card is too short


def test_cues_follow_the_timeline(tmp_path):
    timeline = [
        {"cls": "Hook", "chapter": "A hook", "start": 0.0, "duration": 30.0,
         "lines": [{"start": 0.0, "duration": 30.0}]},
        {"cls": "One", "chapter": "1. One", "start": 30.0, "duration": 40.0,
         "lines": [{"start": 0.2, "duration": 3.0}, {"start": 3.5, "duration": 20.0}, {"start": 30.0, "duration": 9.0}]},
        {"cls": "Outro", "chapter": "Recap", "start": 70.0, "duration": 20.0,
         "lines": [{"start": 0.0, "duration": 19.0}]},
    ]
    out = score.cues(timeline, tmp_path)
    names = [c["label"] for c in out]
    assert names[0] == "score: theme" and names[-1] == "score: close"
    assert "score: sting1" in names
    beds = [c for c in out if c["label"].startswith("score: bed")]
    assert len(beds) == 1 and abs(beds[0]["start"] - (30.0 + 23.5 + score.BED_EDGE)) < 1e-9
    assert beds[0]["start"] + beds[0]["duration"] <= 30.0 + 30.0 - score.BED_EDGE + 0.05
    assert all(c["underscore"] for c in out)
    from explainer.music.monochord.audio import Clip
    assert Clip.read(out[0]["path"]).channels == 2
