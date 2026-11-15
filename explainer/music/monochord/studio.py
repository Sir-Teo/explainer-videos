"""Monochord's studio (Part 56 of *Music, Built*): stereo microphone pairs and the images they make, two microphones on
one source, gain staging, crossfades, the mixer (pan laws, equalizers, compressors, sends and buses), a masking map,
width, and an automatic mixer.

    pair_cues(kind, theta)                  a far source's level and time differences at a stereo pair
    image_position(dL, dt)                  where the phantom image falls (a time-intensity trading rule)
    recording_angle(kind)                   the stage width a pair maps onto the loudspeakers
    pair_render(x, kind, theta, sr)         a mono source recorded by a pair (two channels)
    comb_db(f, delay, g)                    two copies of a sound, one delayed and weaker, summed
    chain(...)                              levels and noise from the air to the converter
    quantize(x, bits)                       a converter's rounding
    crossfade(a, b, n, law)                 joining two takes
    pan_gains(p, centre_db)                 the four pan laws in use (0, -3, -4.5 and -6 dB in the centre)
    Channel, mix(...)                       a console: gain, pan, high-pass, EQ, compression, sends, buses, a master
    band_energy(y, sr)                      power in ERB-spaced bands, frame by frame
    masking_map(stems, sr)                  for each track and band, how much of its energy the rest of the mix covers
    ms_encode / ms_decode, correlation, mono_loss_db, haas    width and its costs
    automix(stems, sr)                      a rule-based mix: loudness, panning by brightness, high-passes, unmasking

No manim here.  Checked in ``tests/music/test_studio.py``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from scipy.signal import fftconvolve, lfilter

from explainer.music.monochord import dynamics as D
from explainer.music.monochord import effects as E
from explainer.music.monochord import loudness as LN
from explainer.music.monochord import Clip

SR = 48000
C = 343.0

# --------------------------------------------------------------------------------------------- stereo pairs
# pattern A (1 omni, 0.5 cardioid, 0 figure-8), each capsule's angle off the centre line (degrees), spacing (m)
PAIRS = {
    "XY": {"A": 0.5, "angle": 45.0, "spacing": 0.0},
    "Blumlein": {"A": 0.0, "angle": 45.0, "spacing": 0.0},
    "ORTF": {"A": 0.5, "angle": 55.0, "spacing": 0.17},
    "NOS": {"A": 0.5, "angle": 45.0, "spacing": 0.30},
    "AB": {"A": 1.0, "angle": 0.0, "spacing": 0.60},
}
L100 = 15.0      # dB of level difference that puts an image in one loudspeaker (Simonsen's figure, as Williams used it)
T100 = 1.1       # ms of time difference that does the same (likewise; other studies give up to 18 dB and 1.5 ms)


def pair_cues(kind: str, theta_deg):
    """A far source at ``theta_deg`` (positive to the left of the centre line): the level difference left minus right
    (dB) and how much earlier it reaches the left capsule (ms)."""
    p = PAIRS[kind]
    th = np.radians(np.asarray(theta_deg, float))
    a = math.radians(p["angle"])
    gL = p["A"] + (1 - p["A"]) * np.cos(th - a)
    gR = p["A"] + (1 - p["A"]) * np.cos(th + a)
    dL = 20 * np.log10(np.maximum(np.abs(gL), 1e-4) / np.maximum(np.abs(gR), 1e-4))
    dt = 1000 * p["spacing"] * np.sin(th) / C
    return {"gL": gL, "gR": gR, "dL": np.clip(dL, -40, 40), "dt": dt}


def image_position(dL, dt, l100: float = L100, t100: float = T100):
    """Where a phantom image falls between two loudspeakers, as a fraction from -1 (right) to 1 (left): level and time
    differences traded linearly and added, as in Williams's and Sengpiel's charts; a rule of thumb, not a law."""
    return np.clip(np.asarray(dL, float) / l100 + np.asarray(dt, float) / t100, -1.0, 1.0)


def recording_angle(kind: str) -> float:
    """The stereophonic recording angle: the stage width (degrees) whose edges land exactly in the loudspeakers;
    180 or more means the pair never pushes a source fully to one side."""
    th = np.linspace(0, 90, 9001)
    c = pair_cues(kind, th)
    pos = image_position(c["dL"], c["dt"])
    hit = np.nonzero(pos >= 1.0 - 1e-9)[0]
    return float(2 * th[hit[0]]) if len(hit) else 180.0


def frac_delay(x, d: float) -> np.ndarray:
    """Delay by ``d`` samples (fractional, by linear interpolation)."""
    x = np.asarray(x, float)
    n = np.arange(len(x)) - d
    return np.interp(n, np.arange(len(x)), x, left=0.0, right=0.0)


def pair_render(x, kind: str, theta_deg: float, sr: float = SR) -> np.ndarray:
    """A mono source at ``theta_deg`` recorded by the pair: two channels (left, right), each with its capsule's gain
    and arrival time."""
    c = pair_cues(kind, theta_deg)
    half = float(c["dt"]) / 2000 * sr
    L = float(c["gL"]) * frac_delay(x, 2 - half + 40)
    R = float(c["gR"]) * frac_delay(x, 2 + half + 40)
    return np.stack([L, R], axis=1)


# --------------------------------------------------------------------------------------------- two microphones, one source
def comb_db(f, delay_s: float, g: float):
    """|1 + g e^{-j 2 pi f tau}| in dB: a sound summed with a copy delayed by tau and scaled by g."""
    f = np.asarray(f, float)
    return 20 * np.log10(np.abs(1 + g * np.exp(-2j * np.pi * f * delay_s)) + 1e-12)


def comb_extremes(g: float):
    return 20 * math.log10(1 + g), 20 * math.log10(max(1 - g, 1e-12))


# --------------------------------------------------------------------------------------------- gain staging
def dbu(volts):
    return 20 * np.log10(np.asarray(volts, float) / 0.7746)


def chain(spl: float = 94.0, sens_mv: float = 2.0, ein_dbu: float = -128.0, gain_db: float = 50.0, fs_dbu: float = 18.0,
          adc_noise_dbfs: float = -112.0, room_db: float = 30.0) -> dict:
    """Levels from the air to the converter.  A microphone of sensitivity ``sens_mv`` (mV per pascal, 94 dB SPL) hears a
    source of ``spl`` dB; the preamplifier adds ``gain_db`` and its own noise (``ein_dbu``, referred to its input); the
    converter reaches full scale at ``fs_dbu`` and has a floor of its own.  The room's noise, ``room_db`` SPL, rides
    along."""
    mic = float(dbu(sens_mv / 1000 * 10 ** ((spl - 94) / 20)))
    room = float(dbu(sens_mv / 1000 * 10 ** ((room_db - 94) / 20)))
    pre = mic + gain_db
    peak_dbfs = pre - fs_dbu
    pre_noise = 10 * math.log10(10 ** ((ein_dbu + gain_db) / 10) + 10 ** ((room + gain_db) / 10)) - fs_dbu
    noise = 10 * math.log10(10 ** (pre_noise / 10) + 10 ** (adc_noise_dbfs / 10))
    return {"mic_dbu": mic, "pre_dbu": pre, "peak_dbfs": peak_dbfs, "headroom_db": -peak_dbfs, "noise_dbfs": noise,
            "snr_db": peak_dbfs - noise, "clips": peak_dbfs > 0}


def quantize(x, bits: int) -> np.ndarray:
    q = 2.0 ** (1 - bits)
    return np.clip(np.round(np.asarray(x, float) / q) * q, -1.0, 1.0 - q)


# --------------------------------------------------------------------------------------------- editing
def fade_pair(n: int, law: str = "power"):
    t = (np.arange(n) + 0.5) / n
    if law == "linear":
        return 1 - t, t
    return np.cos(np.pi * t / 2), np.sin(np.pi * t / 2)


def crossfade(a, b, n: int, law: str = "power") -> np.ndarray:
    """``a`` then ``b``, overlapping by ``n`` samples (n = 0: a butt splice)."""
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    if n <= 0:
        return np.r_[a, b]
    fo, fi = fade_pair(n, law)
    mid = a[-n:] * fo + b[:n] * fi
    return np.r_[a[:-n], mid, b[n:]]


# --------------------------------------------------------------------------------------------- the console
def pan_gains(p, centre_db: float = -3.0):
    """p from -1 (left) to 1 (right).  0 dB: a balance control (the centre at full level in both); -3 dB: constant
    power; -6 dB: constant amplitude (linear); -4.5 dB: their geometric mean."""
    p = np.asarray(p, float)
    if centre_db == 0.0:
        return np.minimum(1.0, 1 - p), np.minimum(1.0, 1 + p)
    lin = ((1 - p) / 2, (1 + p) / 2)
    pw = (np.cos(np.pi * (p + 1) / 4), np.sin(np.pi * (p + 1) / 4))
    if centre_db == -6.0:
        return lin
    if centre_db == -3.0:
        return pw
    if centre_db == -4.5:
        return np.sqrt(lin[0] * pw[0]), np.sqrt(lin[1] * pw[1])
    raise ValueError(centre_db)


@dataclass
class Channel:
    name: str
    y: np.ndarray
    gain_db: float = 0.0
    pan: float = 0.0                       # -1 left .. 1 right (for a stereo channel: its balance)
    hpf: float | None = None
    eq: list = field(default_factory=list)  # [(kind, f0, q, gain_db)]
    comp: dict | None = None               # dynamics.compressor's arguments
    sends: dict = field(default_factory=dict)   # bus name -> dB
    mute: object = None                     # None, or a function of time (s) -> gain (0..1), for mutes and rides
    width: float = 1.0                      # for a stereo channel: 0 mono .. 1 as recorded .. 2 wider


def channel_strip(ch: Channel, sr: float = SR) -> np.ndarray:
    """One channel through its strip, before the fader and pan: high-pass, EQ, compression.  Stereo stays stereo."""
    y = np.asarray(ch.y, float)
    stereo = y.ndim == 2
    chans = [y[:, 0], y[:, 1]] if stereo else [y]
    out = []
    for x in chans:
        if ch.hpf:
            b, a = E.biquad("highpass", ch.hpf, sr, 0.7071)
            x = lfilter(b, a, lfilter(b, a, x))
        for kind, f0, q, g in ch.eq:
            b, a = E.biquad(kind, f0, sr, q, g)
            x = lfilter(b, a, x)
        out.append(x)
    if ch.comp:
        det = np.max(np.abs(np.stack(out)), axis=0)
        r = D.compressor(det, sr, **ch.comp)
        gain = r["y"] / np.maximum(det, 1e-12)
        gain = np.where(det > 1e-9, gain, 1.0)
        out = [x * gain for x in out]
    return np.stack(out, axis=1) if stereo else out[0]


def place(y, pan: float, law: float = -3.0, width: float = 1.0) -> np.ndarray:
    """A mono signal panned, or a stereo one balanced and narrowed or widened (by mid-side)."""
    y = np.asarray(y, float)
    if y.ndim == 1:
        gL, gR = pan_gains(pan, law)
        return np.stack([gL * y, gR * y], axis=1)
    M, S = ms_encode(y[:, 0], y[:, 1])
    L, R = ms_decode(M, width * S)
    gL, gR = pan_gains(pan, 0.0)
    return np.stack([gL * L, gR * R], axis=1)


def mix(channels, buses=None, law: float = -3.0, master=None, sr: float = SR, length: int | None = None) -> dict:
    """The console.  Each channel: strip, fader, mute or ride, pan; post-fader sends feed the buses (each a function of
    a stereo array returning a stereo array, a reverb or an echo); everything is summed and passed through ``master``
    (a function, or None).  Returns the mix and each channel's contribution ("stems", after fader and pan)."""
    buses = buses or {}
    n = length or max(len(c.y) for c in channels)
    total = np.zeros((n, 2))
    sends = {k: np.zeros((n, 2)) for k in buses}
    stems = {}
    t = np.arange(n) / sr
    for ch in channels:
        y = channel_strip(ch, sr)
        y = y[:n] if len(y) >= n else (np.r_[y, np.zeros((n - len(y),) + y.shape[1:])])
        y = y * 10 ** (ch.gain_db / 20)
        if ch.mute is not None:
            g = np.asarray(ch.mute(t), float)
            y = y * (g[:, None] if y.ndim == 2 else g)
        st = place(y, ch.pan, law, ch.width)
        stems[ch.name] = st
        total += st
        for bus, db in ch.sends.items():
            sends[bus] += st * 10 ** (db / 20)
    for k, fn in buses.items():
        r = np.asarray(fn(sends[k]), float)[:n]
        total[: len(r)] += r
        stems["bus:" + k] = r
    if master is not None:
        total = np.asarray(master(total), float)
    return {"y": total, "stems": stems}


def reverb_bus(ir_stereo):
    """A send bus that convolves with a stereo impulse response (one per side)."""
    h = np.asarray(ir_stereo, float)

    def fn(x):
        m = x.mean(axis=1)
        return np.stack([fftconvolve(m, h[:, 0])[: len(m)], fftconvolve(m, h[:, 1])[: len(m)]], axis=1)
    return fn


def echo_bus(delay_s: float, feedback: float = 0.45, tone_hz: float = 2500.0, sr: float = SR, pingpong: bool = True):
    """A tape echo: a delay whose repeats come back through a low-pass, each ``feedback`` times the last, alternating
    sides if ``pingpong``."""
    d = int(round(delay_s * sr))
    b, a = E.biquad("lowpass", tone_hz, sr, 0.7071)

    def fn(x):
        m = x.mean(axis=1)
        out = np.zeros((len(m), 2))
        rep = m.copy()
        for k in range(1, 40):
            rep = lfilter(b, a, np.r_[np.zeros(d), rep[:-d]]) * (feedback if k > 1 else 1.0)
            if np.max(np.abs(rep)) < 1e-4:
                break
            side = (k % 2) if pingpong else None
            if side is None:
                out += rep[:, None] * 0.7071
            else:
                out[:, side] += rep
        return out
    return fn


def bus_compressor(**kw):
    def fn(x):
        det = np.max(np.abs(x), axis=1)
        r = D.compressor(det, SR, **kw)
        g = np.where(det > 1e-9, r["y"] / np.maximum(det, 1e-12), 1.0)
        return x * g[:, None]
    return fn


# --------------------------------------------------------------------------------------------- masking
def band_edges(n: int = 24, lo: float = 50.0, hi: float = 12000.0) -> np.ndarray:
    """``n`` bands equally spaced on the ERB-number scale (Glasberg and Moore)."""
    e = lambda f: 21.4 * np.log10(1 + 0.00437 * f)                          # noqa: E731
    ie = lambda x: (10 ** (x / 21.4) - 1) / 0.00437                         # noqa: E731
    return ie(np.linspace(e(lo), e(hi), n + 1))


def band_energy(y, sr: float = SR, edges=None, nfft: int = 2048, hop: int = 1024) -> np.ndarray:
    """Power in each band (rows) for each frame (columns), from a Hann-windowed STFT of a mono signal."""
    y = np.asarray(y, float)
    if y.ndim == 2:
        y = y.mean(axis=1)
    edges = band_edges() if edges is None else edges
    w = np.hanning(nfft)
    frames = max(1, 1 + (len(y) - nfft) // hop)
    f = np.fft.rfftfreq(nfft, 1 / sr)
    idx = [np.nonzero((f >= a) & (f < b))[0] for a, b in zip(edges[:-1], edges[1:])]
    out = np.zeros((len(idx), frames))
    for j in range(frames):
        P = np.abs(np.fft.rfft(y[j * hop: j * hop + nfft] * w)) ** 2 if j * hop + nfft <= len(y) else np.zeros(len(f))
        for i, k in enumerate(idx):
            out[i, j] = P[k].sum() if len(k) else 0.0
    return out


def masking_map(stems: dict, sr: float = SR, edges=None, margin_db: float = 0.0) -> dict:
    """For each track and band: the fraction of the track's energy that falls in time-frequency cells where the rest of
    the mix is stronger by more than ``margin_db`` (the cells an ideal binary mask would give away).  Stereo stems are
    judged side by side and pooled, so that panning can unmask.  A simple, explicit stand-in for partial loudness."""
    edges = band_edges() if edges is None else edges
    sides = [0, 1] if any(np.asarray(v).ndim == 2 for v in stems.values()) else [None]
    num = {k: 0.0 for k in stems}
    den = {k: 0.0 for k in stems}
    for sd in sides:
        E_ = {}
        for k, v in stems.items():
            v = np.asarray(v, float)
            x = v if sd is None else (v[:, sd] if v.ndim == 2 else v / math.sqrt(2))
            E_[k] = band_energy(x, sr, edges)
        total = sum(E_.values())
        for k, e in E_.items():
            masked = (total - e) > e * 10 ** (margin_db / 10)
            num[k] = num[k] + (e * masked).sum(axis=1)
            den[k] = den[k] + e.sum(axis=1)
    bands = {k: num[k] / (den[k] + 1e-20) for k in stems}
    overall = {k: float(np.sum(num[k]) / (np.sum(den[k]) + 1e-20)) for k in stems}
    return {"edges": edges, "bands": bands, "overall": overall}


# --------------------------------------------------------------------------------------------- width
def ms_encode(L, R):
    L, R = np.asarray(L, float), np.asarray(R, float)
    return (L + R) / 2, (L - R) / 2


def ms_decode(M, S):
    return M + S, M - S


def correlation(L, R) -> float:
    L, R = np.asarray(L, float), np.asarray(R, float)
    return float(np.sum(L * R) / math.sqrt(np.sum(L * L) * np.sum(R * R) + 1e-20))


def mono_loss_db(L, R) -> float:
    """How much quieter the mono sum (L + R)/2 is than the stereo pair's average power: 0 dB for identical channels,
    -3 dB for unrelated ones, minus infinity for opposite ones."""
    L, R = np.asarray(L, float), np.asarray(R, float)
    m = (L + R) / 2
    return float(10 * math.log10(np.mean(m ** 2) / ((np.mean(L ** 2) + np.mean(R ** 2)) / 2) + 1e-20))


def haas(x, ms: float, sr: float = SR) -> np.ndarray:
    """The same signal in both channels, one ``ms`` late: wide in stereo, a comb in mono."""
    x = np.asarray(x, float)
    return np.stack([x, frac_delay(x, ms * sr / 1000)], axis=1)


# --------------------------------------------------------------------------------------------- automatic mixing
def lufs(y, sr: float = SR) -> float:
    y = np.asarray(y, float)
    if y.ndim == 1:
        y = np.stack([y, y], axis=1) / math.sqrt(2)
    return LN.integrated(Clip(y, int(sr)))


def centroid(y, sr: float = SR) -> float:
    y = np.asarray(y, float)
    if y.ndim == 2:
        y = y.mean(axis=1)
    P = np.abs(np.fft.rfft(y)) ** 2
    f = np.fft.rfftfreq(len(y), 1 / sr)
    return float((f * P).sum() / (P.sum() + 1e-20))


def automix(stems: dict, sr: float = SR, lead: str | None = None, lead_db: float = 3.0, spread: float = 0.6) -> dict:
    """A rule-based mix, after the rules engineers state and De Man and Reiss tested: every track to the same loudness
    (the lead ``lead_db`` louder); the lead and every track with a tenth of its energy below 150 Hz in the centre,
    the rest spread alternately left and right, further out the brighter they are (by spectral centroid); a high-pass at 80 Hz on every track whose centroid
    is above 400 Hz; and a 3 dB cut at 250 Hz on the bright tracks, where the bass and the rest collide.  Returns the
    channels it would use."""
    names = list(stems)
    loud = {k: lufs(stems[k], sr) for k in names}
    cen = {k: centroid(stems[k], sr) for k in names}
    low = {k: low_share(stems[k], sr) for k in names}
    order = sorted(names, key=lambda k: cen[k])
    target = float(np.median(list(loud.values())))
    chans, side = [], -1
    others = [k for k in order if k != lead]
    for i, k in enumerate(order):
        g = target - loud[k] + (lead_db if k == lead else 0.0)
        if k == lead or low[k] > 0.1:
            pan = 0.0
        else:
            rank = others.index(k) / max(len(others) - 1, 1)
            pan = side * spread * (0.4 + 0.6 * rank)
            side = -side
        bright = cen[k] > 400.0
        chans.append(Channel(k, stems[k], gain_db=g, pan=pan, hpf=80.0 if bright else None,
                             eq=[("peak", 250.0, 1.0, -3.0)] if bright else []))
    return {"channels": chans, "loudness": loud, "centroid": cen, "low_share": low}


def low_share(y, sr: float = SR, f: float = 150.0) -> float:
    """The fraction of a track's energy below ``f``: bass and kick drums keep to the centre."""
    y = np.asarray(y, float)
    if y.ndim == 2:
        y = y.mean(axis=1)
    P = np.abs(np.fft.rfft(y)) ** 2
    ff = np.fft.rfftfreq(len(y), 1 / sr)
    return float(P[ff < f].sum() / (P.sum() + 1e-20))
