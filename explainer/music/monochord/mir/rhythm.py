"""Monochord's beat, chord and structure listeners (Part 62, *Beat, Chords and Structure*).

    novelty                                   an onset-strength curve (Part 61's spectral flux), smoothed and centred
    tempogram, tempo                          autocorrelation of the novelty over lags, and the best tempo under a prior
    track_beats                               Ellis's dynamic programme (2007): onsets on the beat, intervals near the period
    beat_scores                               F-measure within 70 ms, and continuity allowing double, half and off-beat
    chroma, chord_templates, recognize        twelve-bin pitch classes; 24 triad templates; frame-wise matching and an HMM
    viterbi                                   the most likely chord sequence under a transition prior
    dtw, oltw                                 dynamic time warping between two feature sequences, offline and online
    ssm, checkerboard_novelty, boundaries     self-similarity, Foote's novelty (2000) and peak-picked section boundaries
    segment_labels                            sections clustered by their mean chroma
    segment_similarity, labels_from_similarity  repetition: phrases compared moment by moment, and labelled

No manim.  Checked in ``tests/music/test_rhythm.py``.
"""

from __future__ import annotations

import math

import numpy as np

from . import transcribe as TR

SR = 48000
NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]


# --------------------------------------------------------------------------------------------- tempo and beats
def novelty(x, sr: int = SR, hop: int = 480) -> dict:
    """Spectral flux with its local mean removed (half-wave rectified), at ``hop`` samples a frame."""
    o = TR.onset_strength(x, sr, hop=hop)
    f = o["odf"]
    k = max(1, int(round(0.25 / o["hop_s"])))
    mean = np.convolve(f, np.ones(2 * k + 1) / (2 * k + 1), mode="same")
    n = np.maximum(f - mean, 0)
    return {"nov": n / (n.max() + 1e-12), "t": o["t"], "hop_s": o["hop_s"]}


def tempogram(nov, hop_s: float, window: float = 6.0, step: float = 0.5, bpm_lo: float = 40.0, bpm_hi: float = 240.0) -> dict:
    """Autocorrelation tempogram: for windows of ``window`` seconds, the normalized autocorrelation of the novelty at
    each lag, mapped to beats a minute."""
    nov = np.asarray(nov, float)
    W = int(window / hop_s)
    S = max(1, int(step / hop_s))
    lags = np.arange(int(60 / bpm_hi / hop_s), int(60 / bpm_lo / hop_s) + 1)
    cols, times = [], []
    for a in range(0, max(1, len(nov) - W), S):
        seg = nov[a:a + W] - nov[a:a + W].mean()
        den = float(seg @ seg) + 1e-12
        cols.append([float(seg[:-l] @ seg[l:]) / den for l in lags])
        times.append((a + W / 2) * hop_s)
    return {"A": np.array(cols).T, "bpm": 60 / (lags * hop_s), "t": np.array(times)}


def tempo(nov, hop_s: float, prior_bpm: float = 120.0, prior_octaves: float = 1.0) -> dict:
    """The global tempo: the autocorrelation of the whole novelty curve, weighted by a log-Gaussian prior centred on
    ``prior_bpm`` (width ``prior_octaves``), which settles the half-or-double ambiguity the way listeners lean."""
    nov = np.asarray(nov, float) - np.mean(nov)
    lags = np.arange(int(60 / 300 / hop_s), int(60 / 30 / hop_s) + 1)
    ac = np.array([float(nov[:-l] @ nov[l:]) for l in lags])
    ac = np.maximum(ac, 0) / (ac.max() + 1e-12)
    bpm = 60 / (lags * hop_s)
    w = np.exp(-0.5 * (np.log2(bpm / prior_bpm) / prior_octaves) ** 2)
    i = int(np.argmax(ac * w))
    return {"bpm": float(bpm[i]), "lags": lags, "ac": ac, "weighted": ac * w, "bpm_axis": bpm}


def track_beats(nov, hop_s: float, bpm: float, tightness: float = 100.0) -> np.ndarray:
    """Ellis (2007): C(t) = O(t) + max over tau of [C(tau) - tightness * log((t - tau) / P)^2], with P the period in
    frames; the best path is traced back from the best final frame.  Returns beat times in seconds."""
    O = np.asarray(nov, float)
    P = 60.0 / bpm / hop_s
    n = len(O)
    C = O.copy()
    back = np.full(n, -1)
    lo, hi = int(round(P / 2)), int(round(2 * P))
    for t in range(lo, n):
        taus = np.arange(max(0, t - hi), t - lo + 1)
        if len(taus) == 0:
            continue
        pen = -tightness * np.log((t - taus) / P) ** 2
        k = int(np.argmax(C[taus] + pen))
        if C[taus[k]] + pen[k] > 0:
            C[t] = O[t] + C[taus[k]] + pen[k]
            back[t] = taus[k]
    last = n - 1 - int(round(P))
    t = int(np.argmax(C[max(0, last):])) + max(0, last)
    out = [t]
    while back[out[-1]] >= 0:
        out.append(int(back[out[-1]]))
    return np.array(out[::-1], float) * hop_s


def beat_scores(ref, est, tol: float = 0.07) -> dict:
    """F-measure within ``tol`` seconds (MIREX's 70 ms), and the share of reference beats matched at the right
    level, or allowing double, half or the off-beat (the AMLt idea, simplified to a matching count)."""
    ref, est = np.asarray(sorted(ref), float), np.asarray(sorted(est), float)
    base = TR.onset_scores(ref.tolist(), est.tolist(), tol)

    def variants(r):
        mids = (r[:-1] + r[1:]) / 2
        yield "same", r
        yield "double", np.sort(np.r_[r, mids])
        yield "half (odd)", r[::2]
        yield "half (even)", r[1::2]
        yield "off-beat", mids
    best = {}
    for name, v in variants(ref):
        best[name] = TR.onset_scores(v.tolist(), est.tolist(), tol)["f"]
    return {"f": base["f"], "precision": base["precision"], "recall": base["recall"], "levels": best,
            "any_level": max(best.values())}


# --------------------------------------------------------------------------------------------- chroma and chords
def chroma(x, sr: int = SR, hop: int = 4800, n_fft: int = 8192, lo_midi: float = 40, hi_midi: float = 96, gamma: float = 10.0) -> dict:
    """Pitch-class energy per frame from a log-frequency spectrogram (one bin a semitone, MIDI 40 to 96), with log
    compression and each frame normalized to unit length."""
    L = TR.logfreq(x, sr, fmin_midi=lo_midi, fmax_midi=hi_midi, per_semitone=1, n_fft=n_fft, hop=hop)
    S = np.log1p(gamma * L["S"] / (L["S"].max() + 1e-12))
    C = np.zeros((12, S.shape[1]))
    for k, m in enumerate(L["midi"]):
        C[int(round(m)) % 12] += S[k]
    C /= np.linalg.norm(C, axis=0, keepdims=True) + 1e-9
    return {"C": C, "t": L["t"], "hop_s": L["hop_s"]}


def chord_labels() -> list:
    return [f"{NAMES[r]}" for r in range(12)] + [f"{NAMES[r]}m" for r in range(12)] + ["N"]


def chord_templates() -> np.ndarray:
    """25 x 12: major and minor triads on every root, and 'no chord' (flat)."""
    T = np.zeros((25, 12))
    for r in range(12):
        T[r, [r, (r + 4) % 12, (r + 7) % 12]] = 1
        T[12 + r, [r, (r + 3) % 12, (r + 7) % 12]] = 1
    T[24] = 0.5
    T = T / np.linalg.norm(T, axis=1, keepdims=True)
    T[24] *= 0.75                      # 'no chord' wins only when no triad fits well
    return T


def viterbi(logB, logA, logpi) -> np.ndarray:
    """The most likely state path: log emission (states x frames), log transitions (from x to), log initial."""
    S, N = logB.shape
    D = logpi + logB[:, 0]
    back = np.zeros((S, N), int)
    for t in range(1, N):
        M = D[:, None] + logA
        back[:, t] = np.argmax(M, axis=0)
        D = M[back[:, t], np.arange(S)] + logB[:, t]
    path = [int(np.argmax(D))]
    for t in range(N - 1, 0, -1):
        path.append(int(back[path[-1], t]))
    return np.array(path[::-1])


def recognize(C, A=None, beta: float = 20.0, self_prob: float = 0.9) -> dict:
    """Chord recognition: frame-wise, the best template by cosine; with an HMM, emissions exp(beta * cosine) and
    transitions ``A`` (25 x 25; default: stay with ``self_prob``, else move uniformly)."""
    T = chord_templates()
    sim = T @ C
    frame = np.argmax(sim, axis=0)
    if A is None:
        A = np.full((25, 25), (1 - self_prob) / 24)
        np.fill_diagonal(A, self_prob)
    logB = beta * sim
    path = viterbi(logB, np.log(A + 1e-12), np.full(25, -math.log(25)))
    return {"frame": frame, "hmm": path, "sim": sim}


def transitions_from_romans(sequences, key: int = 0, self_prob: float = 0.85, floor: float = 1e-3) -> np.ndarray:
    """A 25 x 25 chord transition matrix in a given major key from sequences of Roman numerals (Part 18's chorale
    symbols): bigram counts between diatonic triads (I ii iii IV V vi; sevenths folded into their triads), add-one
    smoothed, mixed with a ``self_prob`` chance of staying put, and a ``floor`` for every other chord."""
    diatonic = {"I": (0, 0), "ii": (2, 1), "iii": (4, 1), "IV": (5, 0), "V": (7, 0), "vi": (9, 1)}
    idx = {k: ((key + r) % 12) + 12 * m for k, (r, m) in diatonic.items()}
    counts = np.ones((25, 25)) * floor
    for seq in sequences:
        roots = []
        for s in seq:
            base = s.rstrip("0123456789")
            if base in idx:
                roots.append(idx[base])
        for a, b in zip(roots, roots[1:]):
            if a != b:
                counts[a, b] += 1
    np.fill_diagonal(counts, 0)
    A = counts / counts.sum(axis=1, keepdims=True) * (1 - self_prob)
    np.fill_diagonal(A, self_prob)
    return A


# --------------------------------------------------------------------------------------------- alignment
def dtw(X, Y, step_weights=(1.0, 1.0, 1.0)) -> dict:
    """Dynamic time warping between feature sequences X (d x n) and Y (d x m) with cosine distance: the cumulative
    cost matrix and the optimal path from (0, 0) to (n-1, m-1)."""
    Xn = X / (np.linalg.norm(X, axis=0, keepdims=True) + 1e-9)
    Yn = Y / (np.linalg.norm(Y, axis=0, keepdims=True) + 1e-9)
    Cst = 1 - Xn.T @ Yn
    n, m = Cst.shape
    D = np.full((n + 1, m + 1), np.inf)
    D[0, 0] = 0
    wd, wv, wh = step_weights
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i, j] = Cst[i - 1, j - 1] + min(wd * D[i - 1, j - 1], wv * D[i - 1, j], wh * D[i, j - 1])
    i, j, path = n, m, [(n - 1, m - 1)]
    while i > 1 or j > 1:
        k = int(np.argmin([D[i - 1, j - 1], D[i - 1, j], D[i, j - 1]]))
        i, j = (i - 1, j - 1) if k == 0 else ((i - 1, j) if k == 1 else (i, j - 1))
        path.append((i - 1, j - 1))
    return {"cost": Cst, "D": D[1:, 1:], "path": np.array(path[::-1])}


def oltw(X, Y, slope: float = 1.0) -> np.ndarray:
    """Online alignment, causal DTW (in the spirit of Dixon's on-line time warping, 2005): as each frame of the live
    performance Y arrives, extend the column of accumulated costs D(i, j) over every score frame i, using only frames
    already heard, and take as the score position the frame with the least cost per step, D(i, j) / (i + j + 2),
    never moving backwards.  Returns, for each live frame, the score frame believed to be playing."""
    Xn = X / (np.linalg.norm(X, axis=0, keepdims=True) + 1e-9)
    Yn = Y / (np.linalg.norm(Y, axis=0, keepdims=True) + 1e-9)
    n = X.shape[1]
    prev = None
    pos, out = 0, []
    steps = np.arange(n)
    for j in range(Y.shape[1]):
        c = 1 - Xn.T @ Yn[:, j]
        col = np.empty(n)
        for i in range(n):
            best = np.inf
            if prev is not None:
                best = min(prev[i], prev[i - 1] if i > 0 else np.inf)
            if i > 0:
                best = min(best, col[i - 1])
            if prev is None and i == 0:
                best = 0.0
            col[i] = c[i] + best
        prev = col
        k = int(np.argmin(col / (steps + j + 2) ** slope))
        pos = max(pos, k)
        out.append(pos)
    return np.array(out)


# --------------------------------------------------------------------------------------------- structure
def ssm(F) -> np.ndarray:
    """Self-similarity: cosine similarity between every pair of frames of features F (d x n)."""
    Fn = F / (np.linalg.norm(F, axis=0, keepdims=True) + 1e-9)
    return Fn.T @ Fn


def checkerboard_novelty(S, half: int = 8) -> np.ndarray:
    """Foote (2000): correlate a Gaussian-tapered checkerboard kernel along the diagonal of a self-similarity matrix;
    peaks are where the music before differs from the music after."""
    k = np.arange(-half, half)
    g = np.exp(-0.5 * ((k + 0.5) / (half / 2)) ** 2)
    K = np.outer(g, g) * np.outer(np.sign(k + 0.5), np.sign(k + 0.5))
    n = S.shape[0]
    P = np.pad(S, half, mode="constant")
    nov = np.array([float(np.sum(P[i:i + 2 * half, i:i + 2 * half] * K)) for i in range(n)])
    nov = np.maximum(nov, 0)
    return nov / (nov.max() + 1e-12)


def boundaries(nov, hop_s: float, min_gap: float = 2.0, delta: float = 0.1) -> np.ndarray:
    return TR.pick_onsets(nov, hop_s, delta=delta, window=min_gap / 2, wait=min_gap)


def segment_labels(F, bounds_frames, threshold: float = 0.9) -> list:
    """Label sections by their mean feature vector: a section gets the label of the first earlier section whose mean
    is within ``threshold`` cosine similarity, else a new letter."""
    edges = [0] + sorted(int(b) for b in bounds_frames) + [F.shape[1]]
    means, labels = [], []
    for a, b in zip(edges, edges[1:]):
        if b <= a:
            continue
        m = F[:, a:b].mean(axis=1)
        m = m / (np.linalg.norm(m) + 1e-9)
        for k, (mm, lab) in enumerate(zip(means, labels)):
            if float(m @ mm) >= threshold:
                labels.append(lab)
                break
        else:
            labels.append("ABCDEFGHIJ"[len(set(labels))])
        means.append(m)
    return labels


def segment_similarity(S, length: int, count: int, start: int = 0) -> np.ndarray:
    """Repetition: for ``count`` segments of ``length`` frames (phrases, from the beats), the mean similarity along
    the diagonal of the self-similarity matrix between each pair, i.e. how alike they are moment by moment, in order."""
    out = np.zeros((count, count))
    for a in range(count):
        for b in range(count):
            out[a, b] = float(np.mean([S[start + a * length + k, start + b * length + k] for k in range(length)]))
    return out


def labels_from_similarity(M, threshold: float = 0.95) -> list:
    """Each segment takes the label of the first earlier segment it resembles above ``threshold``, else a new one."""
    labels = []
    for i in range(len(M)):
        for j in range(i):
            if M[i, j] >= threshold:
                labels.append(labels[j])
                break
        else:
            labels.append("abcdefghij"[len(set(labels))])
    return labels
