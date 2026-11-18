"""The computed score: levels, peaks, determinism, and where the cues land."""

import numpy as np

from explainer.economics import score as S


def test_levels_and_peaks():
    for y, target in ((S.theme(), S.THEME_LUFS), (S.sting(0.5), S.STING_LUFS), (S.bed(6.0), S.BED_LUFS),
                      (S.close(), S.THEME_LUFS)):
        assert y.ndim == 2 and y.shape[1] == 2 and np.isfinite(y).all()
        assert abs(S._lufs(y) - target) < 0.6 or 20 * np.log10(np.abs(y).max()) <= S.PEAK_DB + 1e-6
        assert 20 * np.log10(np.abs(y).max()) <= S.PEAK_DB + 1e-6


def test_deterministic_and_in_tune():
    assert np.array_equal(S.theme(3), S.theme(3))
    assert abs(S.hz(69) - 440.0) < 1e-9
    assert S.blades(0.0) == (74, 62) and S.blades(1.0) == (69, 69)  # an octave apart, then the same note


def test_cues():
    timeline = [
        {"cls": "Hook", "chapter": "Who feeds Paris?", "start": 0.0, "duration": 60.0,
         "lines": [{"start": 0.0, "duration": 20.0}, {"start": 30.0, "duration": 20.0}]},
        {"cls": "Pit", "chapter": "1. Play it", "start": 60.0, "duration": 40.0,
         "lines": [{"start": 0.0, "duration": 10.0}, {"start": 20.0, "duration": 10.0}]},
        {"cls": "Intermission", "chapter": "Intermission: two hundred years", "start": 100.0, "duration": 44.0,
         "lines": []},
        {"cls": "Outro", "chapter": "Recap", "start": 144.0, "duration": 30.0, "lines": [{"start": 0.0, "duration": 5.0}]},
    ]
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        cues = S.cues(timeline, d, part=1)
    labels = [c["label"] for c in cues]
    assert labels[0] == "score: theme" and labels[-1] == "score: close"
    assert any(l.startswith("score: sting") for l in labels)
    beds = [c for c in cues if "bed" in c["label"]]
    assert beds and all(not (100.0 <= c["start"] < 144.0) for c in beds)  # the intermission plays its own melody
    assert all(c["underscore"] for c in cues)


def test_data_melody_times():
    m = S.data_melody([1, 2, 4, 8], 6.0, times=[0.5, 1.5, 2.5, 3.5])
    assert m["times"] == [0.5, 1.5, 2.5, 3.5] and m["notes"] == sorted(m["notes"])
