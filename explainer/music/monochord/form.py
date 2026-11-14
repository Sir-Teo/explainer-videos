"""Form (Part 21): what returns, and where the sections are.

Features over time (chroma from notes or from audio), self-similarity matrices, Foote's novelty curve and its
peaks, boundary scores within a tolerance, labels for sections by similarity, repetition rates for tunes, and the
statistics behind golden-section claims.  No manim here.
"""

from __future__ import annotations

import math

import numpy as np

from .dsp import fourier as FT


# ---------------------------------------------------------------------------
# Features
# ---------------------------------------------------------------------------
def chroma_notes(events, step: float = 0.5, total: float | None = None) -> np.ndarray:
    """A 12 x T chroma matrix from notes ``(midi, onset, duration)``: each column the share of sounding time each pitch
    class has in that step."""
    total = total or max(a + d for _, a, d in events)
    T = int(math.ceil(total / step - 1e-9))
    C = np.zeros((12, T))
    for p, a, d in events:
        k0, k1 = a / step, (a + d) / step
        for k in range(int(math.floor(k0)), min(T, int(math.ceil(k1)))):
            overlap = min(k + 1, k1) - max(k, k0)
            if overlap > 0:
                C[int(p) % 12, k] += overlap
    return C


def chroma_audio(y, sr: float, hop: float = 0.1, n: int = 8192, fmin: float = 60.0, fmax: float = 2000.0) -> tuple[np.ndarray, np.ndarray]:
    """A 12 x T chroma matrix from sound: a short-time spectrum every ``hop`` seconds, each bin's energy given to the
    pitch class nearest its frequency (between ``fmin`` and ``fmax``).  Returns ``(times, C)``."""
    h = max(1, int(hop * sr))
    f, t, S = FT.stft(y, sr, n=n, hop=h)
    P = np.abs(S) ** 2
    keep = (f >= fmin) & (f <= fmax)
    pc = (np.round(12 * np.log2(f[keep] / 440.0)).astype(int) + 9) % 12
    C = np.zeros((12, P.shape[1]))
    for k in range(12):
        C[k] = P[keep][pc == k].sum(axis=0)
    C = np.log1p(100.0 * C / (C.max() + 1e-12))
    return t, C


def smooth(C: np.ndarray, width: int = 4) -> np.ndarray:
    if width <= 1:
        return C
    k = np.ones(width) / width
    return np.vstack([np.convolve(row, k, mode="same") for row in C])


# ---------------------------------------------------------------------------
# Self-similarity and novelty
# ---------------------------------------------------------------------------
def ssm(C: np.ndarray) -> np.ndarray:
    """Cosine self-similarity: entry (i, j) is how alike moments i and j are (1 identical, 0 nothing shared)."""
    X = C / (np.linalg.norm(C, axis=0, keepdims=True) + 1e-12)
    return X.T @ X


def checkerboard(L: int, taper: float = 0.4) -> np.ndarray:
    """Foote's kernel: +1 in the two blocks where past is like past and future like future, -1 where past meets
    future, under a Gaussian taper; 2L x 2L."""
    s = np.concatenate([-np.ones(L), np.ones(L)])
    K = np.outer(s, s)
    x = (np.arange(2 * L) - L + 0.5) / (taper * L)
    g = np.exp(-0.5 * x ** 2)
    return K * np.outer(g, g)


def novelty(S: np.ndarray, L: int = 8, taper: float = 0.4) -> np.ndarray:
    """Slide the checkerboard along the diagonal of a self-similarity matrix: high where the music before a moment
    is like itself, the music after it is like itself, and the two are unlike each other (Foote, 2000)."""
    K = checkerboard(L, taper)
    n = S.shape[0]
    P = np.pad(S, L, mode="constant")
    out = np.zeros(n)
    for i in range(n):
        out[i] = float(np.sum(P[i: i + 2 * L, i: i + 2 * L] * K))
    out = np.maximum(out, 0.0)
    return out / (out.max() + 1e-12)


def peaks(x: np.ndarray, min_gap: int = 8, threshold: float = 0.2, edge: int = 2) -> list[int]:
    """Local maxima above ``threshold``, at least ``min_gap`` apart (the stronger kept), not within ``edge`` of the ends."""
    cand = [i for i in range(1, len(x) - 1) if x[i] >= x[i - 1] and x[i] > x[i + 1] and x[i] >= threshold and edge <= i < len(x) - edge]
    cand.sort(key=lambda i: -x[i])
    out = []
    for i in cand:
        if all(abs(i - j) >= min_gap for j in out):
            out.append(i)
    return sorted(out)


def boundary_score(found, truth, tol: float) -> dict:
    """Precision, recall and F of found boundaries against true ones, each true boundary matched at most once
    within ``tol`` (the usual hit-rate measure)."""
    found, truth = sorted(found), sorted(truth)
    used, hits = set(), 0
    for f in found:
        best = None
        for j, t in enumerate(truth):
            if j in used or abs(f - t) > tol:
                continue
            if best is None or abs(f - t) < abs(f - truth[best]):
                best = j
        if best is not None:
            used.add(best)
            hits += 1
    p = hits / len(found) if found else 0.0
    r = hits / len(truth) if truth else 0.0
    f1 = 2 * p * r / (p + r) if p + r else 0.0
    return {"hits": hits, "precision": p, "recall": r, "f": f1}


def label_sections(S: np.ndarray, bounds, threshold: float = 0.85) -> list[str]:
    """Letters for the sections between boundaries: a section takes the letter of the first earlier section whose
    mean similarity to it (along the best-aligned diagonal) exceeds ``threshold``, else a new letter."""
    edges = [0] + list(bounds) + [S.shape[0]]
    segs = [(a, b) for a, b in zip(edges, edges[1:]) if b > a]
    labels = []

    def sim(s1, s2):
        (a1, b1), (a2, b2) = s1, s2
        n = min(b1 - a1, b2 - a2)
        if n <= 0:
            return 0.0
        return float(np.mean([S[a1 + k, a2 + k] for k in range(n)]))

    for i, s in enumerate(segs):
        lab = None
        for j in range(i):
            if sim(segs[j], s) >= threshold:
                lab = labels[j]
                break
        labels.append(lab or chr(ord("A") + len(set(labels))))
    return labels


# ---------------------------------------------------------------------------
# Repetition
# ---------------------------------------------------------------------------
def phrases(m) -> list[list[tuple[int, float]]]:
    """A tune's phrases as (pitch, beats) pairs."""
    ends = [0] + list(m.phrase_ends or [len(m.pitches)])
    return [list(zip(m.pitches[a:b], m.beats[a:b])) for a, b in zip(ends, ends[1:]) if b > a]


def repetition(m) -> dict:
    """How much of a tune repeats: the share of its phrases (and of its beats) that are an exact repeat, or a
    transposed repeat, of an earlier phrase."""
    ph = phrases(m)
    exact = trans = 0
    beats_rep = 0.0
    seen = []
    for p in ph:
        shape = tuple((a - p[0][0], b) for a, b in p)
        if any(p == q for q in seen):
            exact += 1
            beats_rep += sum(b for _, b in p)
        elif any(shape == tuple((a - q[0][0], b) for a, b in q) for q in seen):
            trans += 1
            beats_rep += sum(b for _, b in p)
        seen.append(p)
    total = sum(m.beats)
    return {"phrases": len(ph), "exact": exact, "transposed": trans, "share_phrases": (exact + trans) / max(1, len(ph)),
            "share_beats": beats_rep / total if total else 0.0}


def form_letters(m) -> str:
    """The tune's phrase plan in letters: equal phrases share a letter; a transposed repeat gets a prime."""
    ph = phrases(m)
    letters, shapes, out = [], [], []
    for p in ph:
        shape = tuple((a - p[0][0], b) for a, b in p)
        if p in letters:
            out.append(out[letters.index(p)].rstrip("'"))
        elif shape in shapes:
            out.append(out[shapes.index(shape)].rstrip("'") + "'")
        else:
            out.append(chr(ord("A") + len({x.rstrip("'") for x in out})))
        letters.append(p)
        shapes.append(shape)
    return " ".join(out)


# ---------------------------------------------------------------------------
# The golden section
# ---------------------------------------------------------------------------
PHI = (math.sqrt(5) - 1) / 2                         # 0.618...


def golden_base_rate(lo: float = 0.5, hi: float = 0.75, tol: float = 0.02) -> float:
    """If the larger part of a two-part division is anywhere between ``lo`` and ``hi`` of the whole, uniformly, the
    chance that it falls within ``tol`` of the golden section by accident."""
    return max(0.0, min(hi, PHI + tol) - max(lo, PHI - tol)) / (hi - lo)


def golden_hits(ratios, tol: float = 0.02) -> int:
    return sum(1 for r in ratios if abs(r - PHI) <= tol)


def climax_positions(tunes) -> list[float]:
    """Where in each tune its highest note first arrives, as a share of its length in beats."""
    out = []
    for m in tunes:
        on = np.concatenate([[0.0], np.cumsum(m.beats)])
        k = int(np.argmax(m.pitches))
        out.append(float(on[k] / on[-1]))
    return out


def repeated_share(pitches, beats, n: int = 4, transposed: bool = True) -> float:
    """The share of a tune's notes that belong to an ``n``-note figure (pitches, or intervals if ``transposed``, with
    durations) already heard earlier in the same tune: how much of it is a repeat."""
    P, B = list(pitches), list(beats)
    if len(P) <= n:
        return 0.0

    def key(i):
        seg = P[i - n + 1: i + 1]
        dur = tuple(B[i - n + 1: i + 1])
        return (tuple(b - a for a, b in zip(seg, seg[1:])) if transposed else tuple(seg)) + dur

    seen, covered = {}, set()
    for i in range(n - 1, len(P)):
        k = key(i)
        if k in seen and seen[k] <= i - n:
            covered.update(range(i - n + 1, i + 1))
        seen.setdefault(k, i)
    return len(covered) / len(P)


def shuffled_share(pitches, beats, n: int = 4, trials: int = 200, seed: int = 0) -> float:
    rng = np.random.default_rng(seed)
    P, B = np.array(pitches), np.array(beats)
    out = []
    for _ in range(trials):
        idx = rng.permutation(len(P))
        out.append(repeated_share(P[idx].tolist(), B[idx].tolist(), n))
    return float(np.mean(out))
