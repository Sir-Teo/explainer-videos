"""Clips, the loudness meter and the spectrum tools.

    python -m pytest -q tests/music/test_audio.py
"""

import re
import shutil
import subprocess

import numpy as np
import pytest

from explainer.music.monochord import SR, Clip, ClipStore, concat, mix, silence
from explainer.music.monochord.dsp import f0_autocorr, partials, stft_db
from explainer.music.monochord.loudness import integrated, true_peak_db


def sine(hz, secs, amp=1.0, phase=0.0):
    t = np.arange(int(secs * SR)) / SR
    return (amp * np.sin(2 * np.pi * hz * t + phase)).astype(np.float32)


def test_wav_round_trip(tmp_path):
    rng = np.random.default_rng(0)
    for y in (rng.uniform(-1, 1, 1000), rng.uniform(-1, 1, (1000, 2))):
        c = Clip(y)
        c.write(tmp_path / "a.wav")
        assert np.array_equal(Clip.read(tmp_path / "a.wav").y, c.y)
        c.write_pcm16(tmp_path / "b.wav")
        assert np.abs(Clip.read(tmp_path / "b.wav").y - c.y).max() < 2.6 / 32768  # rounding, dither, 32767/32768


def test_store_keeps_events(tmp_path):
    store = ClipStore("x", tmp_path)
    c = Clip(sine(440, 0.2), events={"a": 0.1}, notes=[{"t": 0.0, "dur": 0.2, "hz": 440.0, "name": "A4"}])
    store.save("tone.a", c.label("synthesized"))
    back = store.load("tone.a")
    assert back.events == {"a": 0.1} and back.notes[0]["name"] == "A4" and back.meta["label"] == "synthesized"
    assert not store.has("tone.b")


def test_concat_and_mix_carry_time():
    a = Clip(sine(440, 0.5), events={"x": 0.25})
    b = Clip(sine(660, 0.25), events={"x": 0.1})
    c = concat([a, b], gap=0.5, names=["a", "b"])
    assert c.duration == pytest.approx(1.25)
    assert c.events["a.x"] == pytest.approx(0.25) and c.events["b"] == pytest.approx(1.0)
    assert c.events["b.x"] == pytest.approx(1.1)
    m = mix([(a, 0.0), (b, 1.0, -6.0, 1.0)])
    assert m.channels == 2 and m.duration == pytest.approx(1.25)
    assert np.abs(m.y[int(1.1 * SR):, 0]).max() < 1e-6  # panned hard right: nothing on the left
    assert np.abs(m.y[: int(0.4 * SR), 0] - a.y[: int(0.4 * SR)] * np.sqrt(0.5)).max() < 1e-6


def test_fade_removes_the_step():
    c = Clip(np.ones(SR // 10, np.float32)).fade(0.01, 0.01)
    assert c.y[0] == 0 and abs(c.y[-1]) < 0.01 and c.y[SR // 20] == 1


def test_constant_power_placement():
    c = Clip(sine(1000, 1.0, 0.5))
    assert np.sum(c.stereo ** 2) == pytest.approx(np.sum(c.y ** 2), rel=1e-6)


def test_loudness_of_reference_tones():
    """EBU Tech 3341: a 1 kHz stereo sine at -23 dBFS reads -23.0 LUFS; one channel alone reads 3 LU lower."""
    a = 10 ** (-23 / 20)
    s = sine(1000, 20.0, a)
    assert integrated(Clip(np.stack([s, s], axis=1))) == pytest.approx(-23.0, abs=0.05)
    assert integrated(Clip(s)) == pytest.approx(-26.01, abs=0.05)
    assert integrated(Clip(s).at_lufs(-18.0)) == pytest.approx(-18.0, abs=0.01)
    assert integrated(silence(3.0)) == -np.inf


def test_gating_ignores_the_quiet_stretch():
    """Tech 3341 case 3: 10 s at -36, 60 s at -23, 10 s at -36 dBFS reads -23.0 LUFS."""
    lo, hi = 10 ** (-36 / 20), 10 ** (-23 / 20)
    s = np.concatenate([sine(1000, 10, lo), sine(1000, 60, hi), sine(1000, 10, lo)])
    assert integrated(Clip(np.stack([s, s], axis=1))) == pytest.approx(-23.0, abs=0.1)


@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg not installed")
def test_meter_agrees_with_ffmpeg(tmp_path):
    rng = np.random.default_rng(1)
    t = np.arange(12 * SR) / SR
    env = 0.02 + 0.3 * (np.sin(2 * np.pi * 0.21 * t) > 0.2) + 0.1 * (np.sin(2 * np.pi * 1.3 * t) > 0.7)
    left = env * rng.standard_normal(len(t)) * 0.3 + 0.1 * np.sin(2 * np.pi * 110 * t)
    right = env * rng.standard_normal(len(t)) * 0.2 + 0.2 * np.sin(2 * np.pi * 3100 * t) * (t > 6)
    for y in (np.stack([left, right], axis=1), left):
        c = Clip(np.clip(y, -1, 1))
        c.write(tmp_path / "m.wav")
        err = subprocess.run(["ffmpeg", "-nostats", "-i", str(tmp_path / "m.wav"), "-af", "ebur128=peak=true",
                              "-f", "null", "-"], capture_output=True, text=True).stderr
        summary = err[err.rindex("Summary:"):]
        ref = float(re.search(r"I:\s+(-?[\d.]+) LUFS", summary).group(1))
        peak = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", summary).group(1))
        assert integrated(c) == pytest.approx(ref, abs=0.1)
        assert true_peak_db(c) == pytest.approx(peak, abs=0.3)


def test_true_peak_between_samples():
    # a sine at a quarter of the sample rate, sampled 45 degrees off its crests: samples reach 0.707, the wave 1.0
    c = Clip(sine(SR / 4, 0.5, 1.0, np.pi / 4))
    assert c.peak == pytest.approx(np.sqrt(0.5), abs=1e-3)
    assert true_peak_db(c) == pytest.approx(0.0, abs=0.15)


def test_partials_and_pitch():
    y = sine(220.5, 1.0, 0.5) + sine(441.0, 1.0, 0.25) + sine(661.5, 1.0, 0.05)
    p = partials(y, SR, 220.0, 3)
    assert [round(q["hz"], 1) for q in p] == [220.5, 441.0, 661.5]
    assert [round(q["db"], 1) for q in p] == [-6.0, -12.0, -26.0]
    assert f0_autocorr(y, SR) == pytest.approx(220.5, rel=1e-4)
    t, f, S = stft_db(y, SR)
    assert S.shape == (len(f), len(t)) and abs(f[np.argmax(S[:, len(t) // 2])] - 220.5) < f[1]
