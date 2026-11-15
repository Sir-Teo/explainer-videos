"""Monochord's beat, chord and structure listeners (Part 62): tempo, beat tracking, beat scores, chroma, chord
recognition and Viterbi, DTW and online following, self-similarity, novelty and repetition.

    python -m pytest -q tests/music/test_rhythm.py
"""

import numpy as np
import pytest

from explainer.music.monochord.mir import rhythm as RH
from explainer.music.monochord.partkit import organ_tone

SR = 48000


def clicks(times, seconds):
    x = np.zeros(int(seconds * SR))
    rng = np.random.default_rng(0)
    n = int(0.05 * SR)
    for t in times:
        k = int(t * SR)
        x[k:k + n] += rng.standard_normal(n) * np.exp(-np.arange(n) / (0.01 * SR)) * np.hanning(2 * n)[n:]
    return x


def triad(root, minor=False, seconds=1.0):
    return sum(organ_tone(261.63 * 2 ** (t / 12), seconds, partials=5) for t in (root, root + (3 if minor else 4), root + 7))


def test_tempo_and_beats():
    beats = np.arange(0.5, 15.0, 0.6)
    x = clicks(beats, 16.0)
    nv = RH.novelty(x)
    tp = RH.tempo(nv["nov"], nv["hop_s"])
    assert tp["bpm"] == pytest.approx(100.0, rel=0.02)
    est = RH.track_beats(nv["nov"], nv["hop_s"], tp["bpm"])
    assert RH.beat_scores(beats, est)["f"] > 0.9
    # a prior centred elsewhere picks another octave of the same pulse (every second click repeats too)
    assert RH.tempo(nv["nov"], nv["hop_s"], prior_bpm=50.0, prior_octaves=0.3)["bpm"] == pytest.approx(50.0, rel=0.03)


def test_beat_scores_levels():
    ref = np.arange(0, 10, 0.5)
    double = np.arange(0, 10, 0.25)
    s = RH.beat_scores(ref, double)
    assert s["levels"]["double"] > 0.95 and s["f"] < 0.7
    assert RH.beat_scores(ref, ref + 0.25)["levels"]["off-beat"] > 0.9


def test_chroma_and_chords():
    prog = [(0, False), (5, False), (7, False), (9, True)]
    y = np.concatenate([triad(r, m) for r, m in prog])
    C = RH.chroma(y)
    assert C["C"].shape[0] == 12 and np.allclose(np.linalg.norm(C["C"], axis=0), 1.0, atol=1e-6)
    res = RH.recognize(C["C"])
    labels = RH.chord_labels()
    n = C["C"].shape[1]
    got = [labels[res["hmm"][int((k + 0.5) * n / 4)]] for k in range(4)]
    assert got == ["C", "F", "G", "Am"]


def test_viterbi_small():
    # two states, sticky transitions: a single odd frame is smoothed away
    logB = np.log(np.array([[0.9, 0.9, 0.4, 0.9], [0.1, 0.1, 0.6, 0.1]]))
    logA = np.log(np.array([[0.95, 0.05], [0.05, 0.95]]))
    assert RH.viterbi(logB, logA, np.log([0.5, 0.5])).tolist() == [0, 0, 0, 0]


def test_transitions_from_romans():
    A = RH.transitions_from_romans([["I", "IV", "V", "I"], ["I", "V7", "I"]], key=0)
    assert np.allclose(A.sum(axis=1), 1.0)
    assert A[0, 7] > A[0, 9]                     # I goes to V more than to anything unseen
    assert A[7, 0] > A[7, 2]


def test_dtw_and_online():
    rng = np.random.default_rng(1)
    X = np.abs(rng.standard_normal((12, 40)))
    idx = np.repeat(np.arange(40), 2)[:70]       # Y is X played slower
    Y = X[:, idx]
    d = RH.dtw(X, Y)
    assert tuple(d["path"][0]) == (0, 0) and tuple(d["path"][-1]) == (39, 69)
    assert np.all(np.diff(d["path"], axis=0) >= 0)
    on = RH.oltw(X, Y)
    assert np.all(np.diff(on) >= 0)
    assert np.mean(np.abs(on - idx)) < 2.0


def test_structure():
    rng = np.random.default_rng(2)
    va, vb = np.abs(rng.standard_normal(12)), np.abs(rng.standard_normal(12))
    a = va[:, None] + 0.05 * np.abs(rng.standard_normal((12, 20)))
    b = vb[:, None] + 0.05 * np.abs(rng.standard_normal((12, 20)))
    F = np.concatenate([a, b, a], axis=1)
    S = RH.ssm(F)
    M = RH.segment_similarity(S, 20, 3)
    assert RH.labels_from_similarity(M, 0.99) == ["a", "b", "a"]
    nov = RH.checkerboard_novelty(S, half=8)
    assert abs(int(np.argmax(nov[5:-5])) + 5 - 20) <= 2 or abs(int(np.argmax(nov[5:-5])) + 5 - 40) <= 2
