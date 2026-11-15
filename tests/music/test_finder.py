"""Monochord's finders (Part 63): fingerprints, the hash index and its votes, the false-match arithmetic, the content
embedding, implicit ALS, recall, the feedback loop and playlists.

    python -m pytest -q tests/music/test_finder.py
"""

import numpy as np
import pytest

from explainer.music.monochord.mir import finder as F
from explainer.music.monochord.partkit import organ_tone

SR = 48000


def piece(seed, seconds=12.0):
    rng = np.random.default_rng(seed)
    y = np.zeros(int(seconds * SR))
    t = 0.0
    while t < seconds - 0.5:
        d = float(rng.choice([0.25, 0.5]))
        z = organ_tone(110 * 2 ** (int(rng.integers(0, 48)) / 12), d, partials=3 + seed % 5, rolloff=0.6 + 0.07 * (seed % 4))
        k = int(t * SR)
        y[k:k + len(z)] += z[: len(y) - k]
        t += d
    return y


def test_peaks_and_hashes():
    S = F.spectrogram(F.to_8k(piece(0, 4.0), SR))
    pts = F.peaks(S)
    assert len(pts) > 20 and np.all(np.diff(pts[:, 0]) >= 0)
    hs = F.hashes(pts)
    assert all(0 <= h < 2 ** 24 for h, _ in hs)


def test_index_finds_excerpts_with_offset():
    idx = F.Index()
    songs = [piece(s) for s in range(6)]
    for k, y in enumerate(songs):
        idx.add(f"song{k}", y, SR)
    rng = np.random.default_rng(1)
    for k in range(6):
        a = 3.0
        q = songs[k][int(a * SR):int((a + 5) * SR)]
        q = q + rng.standard_normal(len(q)) * np.std(q) * 0.1            # about 20 dB of noise
        r = idx.query(q, SR)
        assert r[0]["track"] == f"song{k}"
        assert r[0]["offset_s"] == pytest.approx(a, abs=0.1)              # within three 32 ms frames
        assert r[0]["votes"] > (r[1]["votes"] if len(r) > 1 else 0)


def test_false_match_arithmetic():
    fm = F.false_match_rate(bits=24, query_hashes=400, db_hashes=2 ** 24, tracks=100, offsets=100)
    assert fm["chance_hits"] == pytest.approx(400.0)
    assert fm["per_bin"] == pytest.approx(0.04)
    assert fm["p_some_bin_at_least"][10] < 1e-6 < fm["p_some_bin_at_least"][2]


def test_embedding_and_classifiers():
    e = F.embed(piece(0, 3.0), SR)
    assert e.shape == (62,) and np.all(np.isfinite(e))
    X = np.r_[np.random.default_rng(0).normal(0, 1, (30, 3)), np.random.default_rng(1).normal(3, 1, (30, 3))]
    y = np.r_[np.zeros(30), np.ones(30)].astype(int)
    assert np.mean(F.knn_predict(X, y, X, k=3) == y) > 0.9
    w = F.logistic(X, y)
    assert np.mean(F.logistic_predict(w, X) == y) > 0.9


def test_als_beats_popularity_on_structured_tastes():
    L = F.listeners(n_users=200, n_items=120, seed=3, popularity=0.3)
    train, held = F.split(L["R"], 0.2, seed=1)
    fit = F.implicit_als(train, k=8, iters=8)
    S = fit["X"] @ fit["Y"].T
    pop = np.tile(train.sum(axis=0), (train.shape[0], 1)).astype(float)
    assert F.recall_at_k(S, held, train) > F.recall_at_k(pop, held, train) > F.recall_at_k(np.random.default_rng(0).random(S.shape), held, train)


def test_feedback_loop_concentrates_plays():
    r = F.feedback_loop(n_users=150, n_items=80, rounds=10, seed=2)
    assert r["gini"][-1] > r["gini_own"][-1] and r["top1"] > r["top1_own"]


def test_playlist_shortens_the_path():
    X = np.random.default_rng(4).normal(0, 1, (25, 5))
    order = F.playlist(X)
    assert sorted(order) == list(range(25))
    assert F.path_length(X, order) < F.path_length(X, list(range(25)))
