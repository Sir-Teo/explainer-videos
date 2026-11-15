"""Monochord's round trip (Part 68): the line transcriber, the edit distance, the stage measures and the suite's helpers,
each against something computed another way.

    python -m pytest -q tests/music/test_roundtrip.py
"""

import math

import numpy as np
import pytest

from explainer.music.monochord import SR
from explainer.music.monochord import roundtrip as RT
from explainer.music.monochord.partkit import organ_tone
from explainer.music.monochord.mir import transcribe as TR


def line(keys, beat=0.5, ring=0.0):
    """Organ tones, one per beat; with ``ring`` each rings on that long under the next, dying away (a release)."""
    y = np.zeros(int((len(keys) * beat + ring + 1.0) * SR))
    for i, m in enumerate(keys):
        z = organ_tone(float(TR.midi_hz(m)), beat * 0.85 + ring, partials=6, rolloff=0.7)
        k = int(0.01 * SR)
        if ring:
            z *= np.exp(-np.arange(len(z)) / SR / 0.4)                          # struck, then dying away
        z[:k] *= np.linspace(0, 1, k)
        z[-k:] *= np.linspace(1, 0, k)
        a = int(i * beat * SR)
        y[a:a + len(z)] += z[: len(y) - a]
    return y / np.max(np.abs(y)) * 0.8


TUNE = [72, 72, 79, 79, 81, 81, 79, 77, 77, 76, 76, 74, 74, 72]


def test_edit_distance_against_brute_cases():
    assert RT.edit_distance("kitten", "sitting") == 3
    assert RT.edit_distance([], [1, 2, 3]) == 3 and RT.edit_distance([1, 2], [1, 2]) == 0
    full = list(range(42))
    assert RT.edit_distance(full[:1] + full[2:], full) == 1                    # one missed note costs one
    # the edit distance is a metric: symmetric, and the triangle inequality holds on random strings
    rng = np.random.default_rng(0)
    for _ in range(30):
        a, b, c = (list(rng.integers(0, 3, rng.integers(0, 8))) for _ in range(3))
        assert RT.edit_distance(a, b) == RT.edit_distance(b, a)
        assert RT.edit_distance(a, c) <= RT.edit_distance(a, b) + RT.edit_distance(b, c)


def test_the_line_comes_back_from_clean_tones():
    y = line(TUNE)
    for method in ("onset", "yin"):
        est = RT.monophonic_notes(y, method=method, compress=10.0)
        assert [m for m, _, _ in est] == TUNE, method
        assert max(abs(a - 0.5 * i) for i, (_, a, _) in enumerate(est)) < 0.03


def test_reading_the_onset_survives_a_ringing_previous_note():
    # each tone rings on under the next; what changed at the onset is still the new note (Part 68 shows, on the
    # piano of Part 38, that YIN over the whole note is pulled between the two)
    for ring in (0.3, 0.6):
        on = RT.monophonic_notes(line(TUNE, ring=ring), method="onset", compress=10.0, delta=0.2)
        assert RT.edit_distance([m for m, _, _ in on], TUNE) <= 1, ring


def test_back_to_score_recovers_a_strict_line():
    notes = [(m, 0.5 * i, 0.5 * i + 0.45) for i, m in enumerate(TUNE)]
    b = RT.back_to_score(notes)
    assert b["keys"] == TUNE and all(v == 1.0 for v in b["values"][:-1]) and b["bpm"] == pytest.approx(120, rel=0.05)
    e = RT.score_errors(b["keys"], b["values"], TUNE, [1.0] * len(TUNE))
    assert e["pitch"] == 0 and e["score"] <= 1


def test_stage_measures():
    t = np.arange(SR) / SR
    sine = np.sin(2 * np.pi * 440 * t)
    assert RT.crest_db(sine) == pytest.approx(20 * math.log10(math.sqrt(2)), abs=0.01)
    score = [(60, 0.5 * i, 0.5 * i + 0.4) for i in range(8)]
    slow = [(m, 1.1 * a, 1.1 * b) for m, a, b in score]
    assert RT.timing_rms_ms(slow, score, 0.5) == pytest.approx(0.0, abs=1e-6)  # a steady tempo change is not rubato
    dry = sine
    assert RT.late_to_early_db(dry + 0.5 * dry, dry) == pytest.approx(20 * math.log10(0.5), abs=0.01)
    y = np.r_[np.zeros(SR), sine]
    assert RT.noise_floor_db(y + 1e-4 * np.random.default_rng(0).standard_normal(len(y))) < -60


def test_suite_helpers():
    rng = np.random.default_rng(1)
    P = rng.normal(size=(12, 2))
    X = RT.mds2(P)
    d = lambda A: np.linalg.norm(A[:, None] - A[None], axis=2)
    assert np.allclose(d(X), d(P), atol=1e-8)                                   # classical scaling keeps 2-D distances
    o = RT.nearest_order(P, 3)
    assert o[0] == 3 and sorted(o) == list(range(12))
    pts = np.c_[np.arange(10.0), np.zeros(10)]                                  # points on a line: nearest-next walks it
    assert RT.path_length(pts, RT.nearest_order(pts, 0)) == pytest.approx(9.0)
    y = np.r_[np.zeros(SR // 2), 0.3 * np.sin(2 * np.pi * 220 * np.arange(3 * SR) / SR)]
    e = RT.excerpt(y, SR, seconds=1.0, rms=0.1)
    assert len(e) == SR and np.sqrt(np.mean(e ** 2)) == pytest.approx(0.1, rel=1e-6) and abs(e[0]) < 0.05


def test_superflux_reduces_to_spectral_flux_and_ignores_flicker():
    t = np.arange(2 * SR) / SR
    y = np.sin(2 * np.pi * 500 * t) * (t > 0.7)
    assert np.allclose(RT.superflux(y, SR, lag=1, width=1)["odf"], TR.onset_strength(y, SR)["odf"], atol=1e-9)   # Part 61's flux
    # a band switching on and off every 20 ms (two frames), then a note at 1 s: how far the note stands above the flicker
    gate = (np.floor(t / 0.02) % 2).astype(float)
    y = 0.1 * np.sin(2 * np.pi * 3000 * t) * gate + 0.3 * np.sin(2 * np.pi * 440 * t) * (t > 1.0)
    i = int(1.0 / 0.01) + 5

    def contrast(o):
        return o[i - 3:i + 4].max() / (np.median(o[20:90]) + 1e-12)

    assert contrast(TR.onset_strength(y, SR)["odf"]) < 20 and contrast(RT.superflux(y, SR, lag=3)["odf"]) > 1000
