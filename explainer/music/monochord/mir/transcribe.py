"""Monochord's first listeners (Part 61, *Pitch, Onsets and Transcription*).

Act XI turns the chain around: sound in, notes out.  Monochord has what the field lacks, unlimited audio with a
perfect answer key, because it rendered the audio itself.

    yin, acf_f0, gross_error            one voice's pitch, by YIN (de Cheveigné and Kawahara, 2002) and by plain
                                        autocorrelation, and how often each is wrong by more than 20 %
    logfreq                             a spectrogram on a log-frequency axis (a few bins a semitone)
    salience                            harmonic summation: how much each candidate pitch is supported by its partials
    onset_strength, pick_onsets         spectral flux and peak picking
    nmf, note_templates                 non-negative matrix factorization by multiplicative updates (Lee and Seung);
                                        one spectral template per pitch, learnt from isolated notes
    activations_to_notes, roll          from activations (or a network's probabilities) to notes, and back
    note_scores, frame_scores           precision, recall and F-measure, note by note (onset within 50 ms) and frame
                                        by frame, as mir_eval computes them
    quantize                            from performed times to a score's beats

No manim; torch only in ``neural.py``.  Checked in ``tests/music/test_transcribe.py``.
"""

from __future__ import annotations

import math

import numpy as np

SR = 48000


def midi_hz(m):
    return 440.0 * 2.0 ** ((np.asarray(m, float) - 69.0) / 12.0)


def hz_midi(f):
    return 69.0 + 12.0 * np.log2(np.asarray(f, float) / 440.0)


# --------------------------------------------------------------------------------------------- one voice's pitch
def _frames(x, n, hop):
    x = np.asarray(x, float)
    count = max(1, 1 + (len(x) - n) // hop)
    idx = np.arange(n)[None, :] + hop * np.arange(count)[:, None]
    return x[idx]


def _difference(fr, W, taus=None):
    """d(tau) = sum_{j<W} (x_j - x_{j+tau})^2 for tau < ``taus`` (default W), for every frame (rows), by FFT."""
    taus = W if taus is None else taus
    n = fr.shape[1]
    N = 1 << int(math.ceil(math.log2(2 * n)))
    F = np.fft.rfft(fr, N)
    r = np.fft.irfft(F * np.conj(np.fft.rfft(np.pad(fr[:, :W], ((0, 0), (0, n - W))), N)), N)[:, :taus]   # sum_{j<W} x_{j+tau} x_j
    sq = np.cumsum(fr ** 2, axis=1)
    e0 = sq[:, W - 1][:, None]                                                  # sum_{j<W} x_j^2
    t = np.arange(taus)
    hi = sq[:, np.minimum(t + W - 1, n - 1)]
    lo = np.where(t > 0, sq[:, np.maximum(t - 1, 0)], 0.0)
    return e0 + (hi - lo) - 2 * r                                               # + sum_{j<W} x_{j+tau}^2


def yin(x, sr: int = SR, fmin: float = 60.0, fmax: float = 1000.0, hop: int = 480, threshold: float = 0.1) -> dict:
    """YIN: the difference function, normalized by its cumulative mean, and the first dip under ``threshold``
    (else the first local minimum within 15 % of the lowest, as implementations do, since in noise the lowest dip is
    often at twice the period), refined by parabolic interpolation.  Returns times, f0 (Hz) and the dip's depth
    (an aperiodicity: near 0 for a clean periodic frame)."""
    L = int(math.ceil(sr / fmin)) + 2                 # lags searched
    W = 2 * L                                         # the integration window
    n = W + L
    fr = _frames(x, n, hop)
    d = _difference(fr, W, L)
    taus = np.arange(L)
    cm = np.cumsum(d[:, 1:], axis=1) / taus[1:]
    dn = np.ones_like(d)
    dn[:, 1:] = d[:, 1:] / np.maximum(cm, 1e-12)
    tmin = max(2, int(sr / fmax))
    f0 = np.full(len(fr), np.nan)
    ap = np.ones(len(fr))
    for i in range(len(fr)):
        row = dn[i]
        below = np.where(row[tmin:L - 1] < threshold)[0]
        if len(below):
            t = tmin + below[0]
            while t + 1 < L - 1 and row[t + 1] < row[t]:
                t += 1
        else:                           # no dip under the threshold: the first local minimum near the lowest one
            seg = row[tmin:L - 1]
            g = float(seg.min())
            mins = [k for k in range(1, len(seg) - 1) if seg[k] <= seg[k - 1] and seg[k] <= seg[k + 1] and seg[k] <= g * 1.15 + 0.02]
            t = tmin + (mins[0] if mins else int(np.argmin(seg)))
        a, b, c = row[t - 1], row[t], row[t + 1]
        den = a - 2 * b + c
        shift = 0.5 * (a - c) / den if abs(den) > 1e-12 else 0.0
        f0[i] = sr / (t + shift)
        ap[i] = b
    times = (np.arange(len(fr)) * hop + W / 2) / sr          # the centre of the integration window
    return {"t": times, "f0": f0, "aperiodicity": ap}


def acf_f0(x, sr: int = SR, fmin: float = 60.0, fmax: float = 1000.0, hop: int = 480) -> dict:
    """Plain autocorrelation of the whole frame (the same frames as ``yin``): the lag of the largest r(tau) between
    1/fmax and 1/fmin."""
    L = int(math.ceil(sr / fmin)) + 2
    W = 2 * L
    n = W + L
    fr = _frames(x, n, hop)
    N = 1 << int(math.ceil(math.log2(2 * n)))
    F = np.fft.rfft(fr, N)
    r = np.fft.irfft(np.abs(F) ** 2, N)[:, :L]
    tmin = max(2, int(sr / fmax))
    t = tmin + np.argmax(r[:, tmin:L - 1], axis=1)
    f0 = np.empty(len(fr))
    for i, k in enumerate(t):
        a, b, c = r[i, k - 1], r[i, k], r[i, k + 1]
        den = a - 2 * b + c
        f0[i] = sr / (k + (0.5 * (a - c) / den if abs(den) > 1e-12 else 0.0))
    return {"t": (np.arange(len(fr)) * hop + n / 2) / sr, "f0": f0}


def gross_error(f0, truth) -> float:
    """The share of voiced frames whose estimate is off by more than 20 % (the usual gross pitch error)."""
    f0, truth = np.asarray(f0, float), np.asarray(truth, float)
    ok = np.isfinite(truth) & (truth > 0)
    est = np.where(np.isfinite(f0), f0, 0.0)
    return float(np.mean(np.abs(est[ok] - truth[ok]) > 0.2 * truth[ok]))


# --------------------------------------------------------------------------------------------- spectra
def logfreq(x, sr: int = SR, fmin_midi: float = 36.0, fmax_midi: float = 108.0, per_semitone: int = 3, n_fft: int = 4096,
            hop: int = 960) -> dict:
    """A magnitude spectrogram on a log-frequency axis: triangular filters centred ``per_semitone`` to a semitone
    from ``fmin_midi`` to ``fmax_midi``, applied to a Hann STFT.  Returns S (bins x frames), the bins' MIDI pitches,
    the frame times."""
    x = np.asarray(x, float)
    x = np.r_[np.zeros(n_fft // 2), x, np.zeros(n_fft // 2)]
    fr = _frames(x, n_fft, hop) * np.hanning(n_fft)[None, :]
    mag = np.abs(np.fft.rfft(fr, axis=1)).T                       # (n_fft/2 + 1) x frames
    freqs = np.fft.rfftfreq(n_fft, 1 / sr)
    centres = np.arange(fmin_midi * per_semitone, fmax_midi * per_semitone + 1) / per_semitone
    fc = midi_hz(centres)
    lo, hi = midi_hz(centres - 1 / per_semitone), midi_hz(centres + 1 / per_semitone)
    Wt = np.zeros((len(centres), len(freqs)))
    for k in range(len(centres)):
        up = (freqs - lo[k]) / max(fc[k] - lo[k], 1e-9)
        down = (hi[k] - freqs) / max(hi[k] - fc[k], 1e-9)
        w = np.clip(np.minimum(up, down), 0, None)
        if w.sum() == 0:                                           # narrower than a bin: take the nearest bin
            w[int(np.argmin(np.abs(freqs - fc[k])))] = 1.0
        Wt[k] = w / w.sum()
    S = Wt @ mag
    return {"S": S, "midi": centres, "t": np.arange(S.shape[1]) * hop / sr, "hop_s": hop / sr}


def salience(S, bins_midi, cands, harmonics: int = 8, alpha: float = 0.8) -> np.ndarray:
    """Harmonic summation (after Klapuri, 2006): the salience of candidate pitch m is the sum, over its first
    ``harmonics`` partials h, of alpha^(h-1) times the spectrum at the bin nearest m + 12 log2 h."""
    S = np.asarray(S, float)
    out = np.zeros((len(cands), S.shape[1]))
    for i, m in enumerate(cands):
        for h in range(1, harmonics + 1):
            target = m + 12 * math.log2(h)
            k = int(np.argmin(np.abs(bins_midi - target)))
            if abs(bins_midi[k] - target) < 0.5:
                out[i] += alpha ** (h - 1) * S[k]
    return out


def onset_strength(x, sr: int = SR, hop: int = 480, n_fft: int = 2048, compress: float = 1000.0) -> dict:
    """Spectral flux: the sum over bins of the half-wave rectified increase of log-compressed magnitude,
    log(1 + C |X|), from one frame to the next."""
    x = np.asarray(x, float)
    x = np.r_[np.zeros(n_fft // 2), x, np.zeros(n_fft // 2)]
    fr = _frames(x, n_fft, hop) * np.hanning(n_fft)[None, :]
    L = np.log1p(compress * np.abs(np.fft.rfft(fr, axis=1)))
    flux = np.r_[0.0, np.maximum(np.diff(L, axis=0), 0).sum(axis=1)]
    return {"odf": flux / max(flux.max(), 1e-12), "t": np.arange(len(flux)) * hop / sr, "hop_s": hop / sr}


def pick_onsets(odf, hop_s: float, delta: float = 0.07, window: float = 0.1, wait: float = 0.05) -> np.ndarray:
    """Peak picking: a frame is an onset if it is the largest within ``window`` seconds either side, exceeds the
    local mean by ``delta``, and comes at least ``wait`` seconds after the last onset."""
    odf = np.asarray(odf, float)
    w = max(1, int(round(window / hop_s)))
    out, last = [], -1e9
    for i in range(len(odf)):
        a, b = max(0, i - w), min(len(odf), i + w + 1)
        if odf[i] == odf[a:b].max() and odf[i] >= odf[max(0, i - 2 * w):b].mean() + delta and (i - last) * hop_s >= wait:
            out.append(i)
            last = i
    return np.array(out, float) * hop_s


def onset_scores(ref, est, tol: float = 0.05) -> dict:
    """Precision, recall and F of onset times, each reference matched at most once within ``tol`` seconds."""
    ref, est = sorted(ref), sorted(est)
    used = [False] * len(est)
    hit = 0
    for r in ref:
        best, bi = tol + 1e-9, -1
        for j, e in enumerate(est):
            if not used[j] and abs(e - r) <= best:
                best, bi = abs(e - r), j
        if bi >= 0:
            used[bi] = True
            hit += 1
    p = hit / max(len(est), 1)
    r_ = hit / max(len(ref), 1)
    return {"precision": p, "recall": r_, "f": 2 * p * r_ / max(p + r_, 1e-12), "hits": hit}


# --------------------------------------------------------------------------------------------- NMF
def nmf(V, W=None, rank: int | None = None, iters: int = 150, fix_W: bool = False, seed: int = 0, beta: float = 1.0,
        sparsity: float = 0.0) -> dict:
    """V (bins x frames) ~ W H with W, H >= 0, by Lee and Seung's multiplicative updates for the beta divergence
    (beta = 1: Kullback-Leibler, 2: Euclidean).  With ``fix_W`` only the activations H are learnt (supervised
    transcription).  ``sparsity`` adds an L1 penalty on H.  Returns W, H and the divergence after each iteration."""
    V = np.asarray(V, float) + 1e-12
    rng = np.random.default_rng(seed)
    if W is None:
        W = rng.random((V.shape[0], rank)) + 0.1
    W = np.array(W, float)
    H = rng.random((W.shape[1], V.shape[1])) + 0.1
    cost = []
    for _ in range(iters):
        WH = W @ H + 1e-12
        H *= (W.T @ (V * WH ** (beta - 2))) / (W.T @ WH ** (beta - 1) + sparsity + 1e-12)
        if not fix_W:
            WH = W @ H + 1e-12
            W *= ((V * WH ** (beta - 2)) @ H.T) / (WH ** (beta - 1) @ H.T + 1e-12)
            s = W.sum(axis=0, keepdims=True) + 1e-12
            W /= s
            H *= s.T
        WH = W @ H + 1e-12
        if beta == 1.0:
            cost.append(float(np.sum(V * np.log(V / WH) - V + WH)))
        else:
            cost.append(float(0.5 * np.sum((V - WH) ** 2)))
    return {"W": W, "H": H, "cost": cost}


def note_templates(spectra: dict) -> tuple[np.ndarray, list]:
    """One template per pitch: the mean spectrum of an isolated note (bins x frames, frames where it sounds),
    normalized to sum one.  ``spectra`` maps MIDI pitch to its spectrogram."""
    keys = sorted(spectra)
    W = np.stack([np.asarray(spectra[k], float).mean(axis=1) for k in keys], axis=1)
    return W / (W.sum(axis=0, keepdims=True) + 1e-12), keys


def activations_to_notes(A, pitches, hop_s: float, on: float = 0.5, off: float | None = None, min_dur: float = 0.06,
                         rel: bool = False) -> list:
    """Notes from activations or probabilities A (pitches x frames): a note starts where A rises above ``on`` and
    ends where it falls below ``off`` (hysteresis; ``off`` defaults to on / 2); notes shorter than ``min_dur`` are
    dropped.  With ``rel``, thresholds are fractions of A's largest value.  A re-attack (a rise of A by half after a
    dip) starts a new note.  Returns [(midi, onset s, offset s)]."""
    A = np.asarray(A, float)
    scale = A.max() if rel and A.max() > 0 else 1.0
    on_t = on * scale
    off_t = (off if off is not None else on / 2) * scale
    notes = []
    for i, p in enumerate(pitches):
        a = A[i]
        k, n = 0, len(a)
        while k < n:
            if a[k] >= on_t:
                s = k
                low = a[k]
                k += 1
                while k < n and a[k] >= off_t:
                    low = min(low, a[k])
                    if a[k] - low > 0.5 * on_t and a[k] > a[k - 1] and k - s > 2:     # a re-attack
                        break
                    k += 1
                if (k - s) * hop_s >= min_dur:
                    notes.append((int(p), s * hop_s, k * hop_s))
            else:
                k += 1
    return sorted(notes, key=lambda z: (z[1], z[0]))


def roll(notes, pitches, hop_s: float, frames: int) -> np.ndarray:
    R = np.zeros((len(pitches), frames))
    idx = {int(p): i for i, p in enumerate(pitches)}
    for m, a, b in notes:
        if int(m) in idx:
            R[idx[int(m)], int(round(a / hop_s)):max(int(round(b / hop_s)), int(round(a / hop_s)) + 1)] = 1
    return R


def note_scores(ref, est, onset_tol: float = 0.05, offsets: bool = False, offset_ratio: float = 0.2) -> dict:
    """Note-level precision, recall and F (as mir_eval.transcription computes them, with a greedy matching in onset
    order): a note is found if its pitch is the same and its onset within ``onset_tol``; with ``offsets``, its offset
    must also be within max(50 ms, ``offset_ratio`` of the reference note's length)."""
    ref = sorted(ref, key=lambda z: z[1])
    est = sorted(est, key=lambda z: z[1])
    used = [False] * len(est)
    hit = 0
    for m, a, b in ref:
        best, bi = None, -1
        for j, (m2, a2, b2) in enumerate(est):
            if used[j] or int(m2) != int(m) or abs(a2 - a) > onset_tol:
                continue
            if offsets and abs(b2 - b) > max(0.05, offset_ratio * (b - a)):
                continue
            if best is None or abs(a2 - a) < best:
                best, bi = abs(a2 - a), j
        if bi >= 0:
            used[bi] = True
            hit += 1
    p = hit / max(len(est), 1)
    r = hit / max(len(ref), 1)
    return {"precision": p, "recall": r, "f": 2 * p * r / max(p + r, 1e-12), "hits": hit, "ref": len(ref), "est": len(est)}


def frame_scores(ref_roll, est_roll) -> dict:
    R, E = np.asarray(ref_roll) > 0.5, np.asarray(est_roll) > 0.5
    tp = float((R & E).sum())
    p = tp / max(E.sum(), 1)
    r = tp / max(R.sum(), 1)
    return {"precision": p, "recall": r, "f": 2 * p * r / max(p + r, 1e-12)}


# --------------------------------------------------------------------------------------------- toward a score
def quantize(notes, divisions: int = 2, tempos=None) -> dict:
    """Performed notes to a score: try each tempo (beats a second), snap every onset to the nearest 1/``divisions``
    of a beat, and keep the tempo and phase with the smallest squared error (with a mild prior near 120 beats a minute,
    since half and double the tempo fit almost as well: the tempo-octave ambiguity); durations become the gap to the next
    onset on the grid (the last note's, its performed length).  Returns beats, durations in beats, the tempo, error."""
    on = np.array(sorted(n[1] for n in notes))
    if tempos is None:
        tempos = np.linspace(0.8, 3.0, 221)
    best = None
    for bps in tempos:
        for phase in np.linspace(0, 1 / (bps * divisions), 8, endpoint=False):
            pos = (on - on[0] + phase) * bps * divisions
            err = float(np.mean(((pos - np.round(pos)) / (bps * divisions)) ** 2))       # in seconds squared
            pen = err + 5e-4 * abs(math.log(bps / 2.0))            # a prior near 120 beats a minute: half and double fit too
            if best is None or pen < best[0]:
                best = (pen, bps, phase, err)
    _, bps, phase, err = best
    grid = np.round((on - on[0] + phase) * bps * divisions) / divisions
    grid -= grid[0]
    last = sorted(notes, key=lambda z: z[1])[-1]
    durs = np.r_[np.diff(grid), max(1.0 / divisions, round((last[2] - last[1]) * bps * divisions) / divisions)]
    return {"beats": grid.tolist(), "durations": durs.tolist(), "bps": float(bps), "error": err}
