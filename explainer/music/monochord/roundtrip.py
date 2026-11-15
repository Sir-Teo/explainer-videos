"""The round trip (Part 68): a melody from a score to sound and back to a score, and the measurements on the way.

The way back for one line is Part 61's two monophonic tools put together: onsets picked from the onset strength,
and in each note the median of YIN's pitch over its first stretch, rounded to the nearest key.  Each stage of the way
down is measured by the quantity that stage changes: timing, reverberation, noise, crest factor, bandwidth.  The
suite's helpers cut an excerpt from each Variation and order excerpts by how far apart they sound.
"""

from __future__ import annotations

import math

import numpy as np

from . import SR
from .mir import transcribe as TR


# ---------------------------------------------------------------------------------------------- the way back
def superflux(y, sr: int = SR, hop: int = 480, n_fft: int = 2048, compress: float = 1000.0, lag: int = 3, width: int = 3) -> dict:
    """Onset strength after Böck and Widmer's SuperFlux (2013): the rise of each bin's log-compressed magnitude above
    the maximum, over ``width`` neighbouring bins and the last ``lag`` frames, of what came before.  Energy that flickers from frame
    to frame (a coder's bands switching on and off) or wavers between bins (vibrato) does not count as a rise; a new
    note, louder than anything just before it, does.  ``lag`` = 1 and ``width`` = 1 give Part 61's spectral flux."""
    from scipy.ndimage import maximum_filter1d
    x = np.asarray(y, float)
    x = np.r_[np.zeros(n_fft // 2), x, np.zeros(n_fft // 2)]
    n = 1 + (len(x) - n_fft) // hop
    fr = np.lib.stride_tricks.as_strided(x, (n, n_fft), (x.strides[0] * hop, x.strides[0])) * np.hanning(n_fft)[None, :]
    L = np.log1p(compress * np.abs(np.fft.rfft(fr, axis=1)))
    ref = maximum_filter1d(L, size=width, axis=1)
    ref = np.r_[ref[:1], ref[:-1]]                                       # the frame before ...
    if lag > 1:                                                          # ... or the loudest of the last ``lag``
        ref = maximum_filter1d(ref, size=lag, axis=0, origin=(lag - 1) // 2)
    flux = np.maximum(L - ref, 0).sum(axis=1)
    return {"odf": flux / max(flux.max(), 1e-12), "t": np.arange(len(flux)) * hop / sr, "hop_s": hop / sr}


def analyse(y, sr: int = SR, fmin: float = 150.0, fmax: float = 1200.0) -> dict:
    """What ``monophonic_notes`` reads, computed once: YIN's pitch track and a log-frequency spectrogram, both of the
    signal padded with 0.1 s of silence (so that a note at time 0 has an onset)."""
    y = np.r_[np.zeros(int(0.1 * sr)), np.asarray(y, float)]
    return {"yin": TR.yin(y, sr, fmin=fmin, fmax=fmax, hop=480),
            "spec": TR.logfreq(y, sr, fmin_midi=40.0, fmax_midi=110.0, per_semitone=3, n_fft=4096, hop=480)}


def monophonic_notes(y, sr: int = SR, fmin: float = 150.0, fmax: float = 1200.0, delta: float = 0.07, wait: float = 0.12,
                     floor_db: float = -35.0, compress: float = 1000.0, rise_db: float = 0.0, method: str = "onset",
                     analysis: dict | None = None, lag: int = 1) -> list:
    """One line from audio: ``[(key, onset s, offset s)]``.  Onsets are picked from the onset strength (Part 61, scaled
    by its 99th percentile so that one click cannot flatten the rest; with ``lag`` > 1, SuperFlux's) and
    kept (if ``rise_db`` > 0) where the level 50 ms later is at least ``rise_db`` above the level 30 ms before; each note runs to the next
    onset (or until its level falls ``floor_db`` below the loudest moment).  Its key is, with ``method="yin"``, the
    commonest rounded YIN pitch from 40 ms in to 70 % of the note; with ``method="onset"``, the candidate whose
    harmonics (Part 61's harmonic sum) gained the most energy across the onset, so that a previous note still ringing
    through its release does not pull the reading."""
    pad = int(0.1 * sr)
    yp = np.r_[np.zeros(pad), np.asarray(y, float)]
    hop = 480
    an = analysis if analysis is not None else analyse(y, sr, fmin, fmax)
    o = TR.onset_strength(yp, sr, hop=hop, compress=compress) if lag <= 1 else superflux(yp, sr, hop=hop, compress=compress, lag=lag)
    # scaled by its 99th percentile, not its maximum: one click (a coder's artefact) must not flatten every onset
    odf = np.minimum(o["odf"] / (np.quantile(o["odf"], 0.99) + 1e-12), 1.0)
    on = TR.pick_onsets(odf, o["hop_s"], delta=delta, wait=wait)
    p = an["yin"]
    f0, t = np.asarray(p["f0"], float), np.asarray(p["t"], float)
    voiced = np.isfinite(f0) & (np.asarray(p["aperiodicity"]) < 0.3)
    env = np.sqrt(np.convolve(yp ** 2, np.ones(hop) / hop, mode="same"))[::hop]
    te = np.arange(len(env)) * hop / sr
    top = env.max() + 1e-12
    lvl = lambda x: 20 * np.log10(np.interp(x, te, env) / top + 1e-12)
    if rise_db > 0:
        on = [a for a in on if lvl(a + 0.05) - lvl(a - 0.03) >= rise_db]
    S, bins, ts = an["spec"]["S"], an["spec"]["midi"], an["spec"]["t"]
    lo_m, hi_m = int(math.ceil(TR.hz_midi(fmin))), int(math.floor(TR.hz_midi(fmax)))
    cands = np.arange(lo_m, hi_m + 1)
    notes = []
    for i, a in enumerate(on):
        b = on[i + 1] if i + 1 < len(on) else t[-1]
        quiet = np.where((te > a) & (te < b) & (20 * np.log10(env / top + 1e-12) < floor_db))[0]
        if len(quiet):
            b = te[quiet[0]]
        if method == "yin":
            sel = (t >= a + 0.04) & (t <= a + 0.7 * (b - a)) & voiced
            if sel.sum() < 2:
                continue
            keys, counts = np.unique(np.round(TR.hz_midi(f0[sel])).astype(int), return_counts=True)
            m = int(keys[np.argmax(counts)])
        else:
            after = (ts >= a + 0.03) & (ts <= a + min(0.12, 0.8 * (b - a)))
            before = (ts >= a - 0.08) & (ts <= a - 0.01)
            if after.sum() == 0:
                continue
            gain = S[:, after].mean(axis=1) - (S[:, before].mean(axis=1) if before.any() else 0.0)
            sal = TR.salience(np.maximum(gain, 0.0)[:, None], bins, cands)[:, 0]
            if sal.max() <= 0:
                continue
            m = int(cands[int(np.argmax(sal))])
        notes.append((m, float(a) - pad / sr, float(b) - pad / sr))
    return notes


def edit_distance(a, b) -> int:
    """Levenshtein's distance between two sequences: insertions, deletions and substitutions each cost one."""
    D = np.arange(len(b) + 1)
    for i, x in enumerate(a, 1):
        prev, D[0] = D[0], i
        for j, z in enumerate(b, 1):
            prev, D[j] = D[j], min(D[j] + 1, D[j - 1] + 1, prev + (x != z))
    return int(D[-1])


def back_to_score(notes) -> dict:
    """A transcribed line quantized with a drifting tempo (Part 61): its keys, its note values in beats, its tempo."""
    if len(notes) < 3:
        return {"keys": [int(n[0]) for n in notes], "values": [1.0] * len(notes), "bpm": float("nan")}
    q = TR.quantize_tracking(notes)
    return {"keys": [int(n[0]) for n in notes], "values": [float(v) for v in q["durations"]], "bpm": float(np.median(q["tempo"]) * 60)}


def score_errors(keys, values, want_keys, want_values) -> dict:
    """Edit distances to the written score: of the keys alone, and of (key, value) pairs."""
    return {"pitch": edit_distance(list(keys), list(want_keys)),
            "score": edit_distance(list(zip(keys, values)), list(zip(want_keys, want_values)))}


# ---------------------------------------------------------------------------------------------- the way down, measured
def timing_rms_ms(perf, score, beat: float) -> float:
    """How far a performance's onsets sit from the score's after the best single tempo (least squares through 0)."""
    p = np.array([n[1] for n in perf], float)
    s = np.array([n[1] for n in score], float)
    k = float(p @ s / (s @ s))
    return float(np.sqrt(np.mean((p - k * s) ** 2)) * 1000)


def late_to_early_db(wet, dry, sr: int = SR) -> float:
    """What a room adds: the energy of (wet - dry), the reverberation, against the dry sound's, in dB."""
    r = np.asarray(wet, float)[: len(dry)] - np.asarray(dry, float)[: len(wet)]
    return float(10 * math.log10(np.sum(r ** 2) / (np.sum(np.asarray(dry, float) ** 2) + 1e-20) + 1e-20))


def crest_db(y) -> float:
    """Peak over RMS, in dB: what a limiter takes away."""
    y = np.asarray(y, float)
    return float(20 * math.log10(np.max(np.abs(y)) / (np.sqrt(np.mean(y ** 2)) + 1e-20)))


def noise_floor_db(y, sr: int = SR, block: float = 0.05) -> float:
    """The quietest 5 % of 50 ms blocks, in dB below the loudest block."""
    y = np.asarray(y, float)
    n = int(block * sr)
    e = np.sqrt(np.mean(y[: len(y) // n * n].reshape(-1, n) ** 2, axis=1)) + 1e-12
    return float(20 * math.log10(np.quantile(e, 0.05) / e.max()))


def bandwidth_hz(y, sr: int = SR, drop_db: float = 60.0) -> float:
    """The highest frequency whose long-term level is within ``drop_db`` of the spectrum's peak."""
    y = np.asarray(y, float)
    n = 8192
    fr = np.lib.stride_tricks.sliding_window_view(y, n)[:: n // 2]
    P = np.mean(np.abs(np.fft.rfft(fr * np.hanning(n), axis=1)) ** 2, axis=0)
    f = np.fft.rfftfreq(n, 1 / sr)
    L = 10 * np.log10(P / P.max() + 1e-30)
    L = np.convolve(L, np.ones(9) / 9, mode="same")
    ok = np.where(L > -drop_db)[0]
    return float(f[ok[-1]]) if len(ok) else 0.0


# ---------------------------------------------------------------------------------------------- the suite
def excerpt(y, sr: int = SR, seconds: float = 8.5, rms: float = 0.1, threshold: float = 0.05) -> np.ndarray:
    """``seconds`` of a clip from its first sound (where its 10 ms envelope first passes ``threshold`` of its peak),
    as mono, levelled to ``rms`` and then lowered if its peak would pass 0.9."""
    y = np.asarray(y, float)
    y = y.mean(axis=1) if y.ndim == 2 else y
    k = max(1, int(0.01 * sr))
    env = np.convolve(np.abs(y), np.ones(k) / k, mode="same")
    i0 = int(np.argmax(env > threshold * env.max()))
    n = int(seconds * sr)
    seg = np.pad(y[i0:i0 + n], (0, max(0, n - len(y[i0:i0 + n]))))
    seg = seg / (np.sqrt(np.mean(seg ** 2)) + 1e-12) * rms
    return seg * min(1.0, 0.9 / (np.max(np.abs(seg)) + 1e-12))


def path_length(E, order) -> float:
    E = np.asarray(E, float)
    return float(np.sum(np.linalg.norm(np.diff(E[list(order)], axis=0), axis=1)))


def nearest_order(E, start: int = 0) -> list:
    """Greedy nearest neighbour: from ``start``, always to the closest piece not yet played."""
    E = np.asarray(E, float)
    left = set(range(len(E))) - {start}
    out = [start]
    while left:
        cur = E[out[-1]]
        j = min(left, key=lambda i: float(np.linalg.norm(E[i] - cur)))
        out.append(j)
        left.remove(j)
    return out


def mds2(E) -> np.ndarray:
    """Classical (Torgerson) scaling of points to two dimensions."""
    E = np.asarray(E, float)
    D2 = np.sum((E[:, None] - E[None]) ** 2, axis=2)
    n = len(E)
    J = np.eye(n) - 1.0 / n
    w, V = np.linalg.eigh(-0.5 * J @ D2 @ J)
    return V[:, -2:][:, ::-1] * np.sqrt(np.maximum(w[-2:][::-1], 0))
