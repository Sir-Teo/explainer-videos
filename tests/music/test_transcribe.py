"""Monochord's first listeners (Part 61): YIN, autocorrelation, the log-frequency spectrogram, salience, onsets,
NMF, note and frame scores, quantization, and the small network.

    python -m pytest -q tests/music/test_transcribe.py
"""

import numpy as np
import pytest

from explainer.music.monochord.mir import transcribe as TR

SR = 48000


def tone(f0, seconds=1.0, partials=(1.0, 0.5, 0.3), start=0.0):
    t = np.arange(int(seconds * SR)) / SR
    return sum(a * np.sin(2 * np.pi * f0 * (k + 1) * t + k) for k, a in enumerate(partials))


def test_difference_function_is_exact():
    rng = np.random.default_rng(0)
    fr = rng.standard_normal((3, 60))
    d = TR._difference(fr, 30, 25)
    direct = np.array([[np.sum((f[:30] - f[tau:tau + 30]) ** 2) for tau in range(25)] for f in fr])
    assert np.allclose(d, direct)


def test_yin_and_acf():
    x = tone(220.3, partials=(1.0, 0.5))
    y = TR.yin(x, SR)
    assert np.median(y["f0"]) == pytest.approx(220.3, rel=2e-4)
    assert np.median(y["aperiodicity"]) < 0.05
    # a missing fundamental: partials 2..6 of 200 Hz
    mf = tone(200.0, partials=(0.0, 1.0, 0.8, 0.6, 0.5, 0.4))
    assert np.median(TR.yin(mf, SR)["f0"]) == pytest.approx(200.0, rel=1e-3)
    assert np.median(TR.acf_f0(x, SR)["f0"]) == pytest.approx(220.3, rel=5e-3)
    truth = np.full(10, 100.0)
    assert TR.gross_error(np.r_[np.full(8, 101.0), 200.0, np.nan], truth) == pytest.approx(0.2)


def test_logfreq_and_salience():
    x = tone(TR.midi_hz(69), seconds=0.6)
    L = TR.logfreq(x, SR)
    peak = L["midi"][np.argmax(L["S"][:, 5:20].mean(axis=1))]
    assert peak == pytest.approx(69, abs=0.34)
    sal = TR.salience(L["S"][:, 5:20], L["midi"], np.arange(48, 85)).mean(axis=1)
    assert 48 + int(np.argmax(sal)) in (57, 69)          # the note, or its octave below, which shares its partials


def test_onsets():
    x = np.zeros(SR * 2)
    for t0 in (0.3, 0.8, 1.4):
        k = int(t0 * SR)
        n = int(0.3 * SR)
        x[k:k + n] += np.sin(2 * np.pi * 440 * np.arange(n) / SR) * np.exp(-np.arange(n) / (0.08 * SR)) * np.hanning(2 * n)[n:]
    o = TR.onset_strength(x, SR)
    est = TR.pick_onsets(o["odf"], o["hop_s"])
    s = TR.onset_scores([0.3, 0.8, 1.4], est.tolist())
    assert s["f"] == pytest.approx(1.0)
    assert TR.onset_scores([0.0, 1.0], [0.02, 0.5, 1.2])["hits"] == 1


def test_nmf():
    rng = np.random.default_rng(1)
    W = rng.random((30, 4))
    H = rng.random((4, 50))
    V = W @ H
    r = TR.nmf(V, rank=4, iters=300, seed=2)
    assert all(b <= a + 1e-6 for a, b in zip(r["cost"], r["cost"][1:]))          # the divergence never increases
    assert r["cost"][-1] < 1e-2 * r["cost"][0]
    s = TR.nmf(V, W=W / W.sum(axis=0), fix_W=True, iters=400)
    assert np.allclose(s["W"] @ s["H"], V, rtol=0.05, atol=1e-3)


def test_notes_and_scores():
    A = np.zeros((3, 50))
    A[1, 10:30] = 1.0
    A[2, 5:7] = 1.0                                           # too short to be a note
    notes = TR.activations_to_notes(A, [60, 61, 62], 0.02, on=0.5, min_dur=0.06)
    assert notes == [(61, pytest.approx(0.2), pytest.approx(0.6))]
    ref = [(60, 0.0, 0.5), (64, 0.5, 1.0), (67, 1.0, 1.5)]
    est = [(60, 0.03, 0.5), (64, 0.58, 1.0), (67, 1.0, 1.2), (72, 1.0, 1.5)]
    s = TR.note_scores(ref, est)
    assert (s["hits"], s["precision"], s["recall"]) == (2, 0.5, pytest.approx(2 / 3))
    assert TR.note_scores(ref, est, offsets=True)["hits"] == 1
    R = TR.roll(ref, [60, 64, 67], 0.1, 16)
    assert TR.frame_scores(R, R)["f"] == pytest.approx(1.0)


def test_quantize():
    beats = [0, 1, 2, 3, 4, 5, 6, 8]
    rng = np.random.default_rng(3)
    notes = [(60, 0.5 * b + float(rng.normal(0, 0.01)), 0.5 * b + 0.4) for b in beats]
    q = TR.quantize(notes, divisions=2)
    assert q["beats"] == pytest.approx(beats)
    assert 60 * q["bps"] == pytest.approx(120, rel=0.05)


def test_quantize_tracking_follows_rubato():
    beats = [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12]
    t, notes = 0.0, []
    for k in range(len(beats)):
        notes.append((60, t, t + 0.3))
        if k + 1 < len(beats):
            t += (beats[k + 1] - beats[k]) * 0.5 * (1 + 0.15 * np.sin(2 * np.pi * k / len(beats)))   # rubato of 15 %
    assert TR.quantize(notes, divisions=2)["beats"] != pytest.approx(beats)                          # one tempo cannot fit
    q = TR.quantize_tracking(notes)
    assert q["beats"] == pytest.approx(beats)
    assert max(q["tempo"]) > 1.1 * min(q["tempo"])                                                   # and the tempo moved


def test_network_learns_a_toy_task():
    pytest.importorskip("torch")
    from explainer.music.monochord.mir import neural as NN
    rng = np.random.default_rng(0)
    S = rng.random((20, 400)) * 0.05
    Y = np.zeros((400, 2))
    S[3, 100:200] += 1.0
    Y[100:200, 0] = 1
    S[12, 250:350] += 1.0
    Y[250:350, 1] = 1
    X = NN.features(S, context=1)
    fit = NN.train(X, Y, hidden=32, epochs=40, seed=0)
    P = NN.predict(fit, X)
    assert ((P > 0.5).T == (Y > 0.5)).mean() > 0.97
