"""Precompute everything numerical, and every sound, in Part 49 of *Music, Built* ("Filters, Delay and Reverb").

    python -m videos.music.music49.compute              # everything missing (a few minutes; the plate takes longest)
    python -m videos.music.music49.compute --force room

Numbers are cached in ``.cache/music49/<name>.json``, sounds in ``.cache/music49/audio/``.  The tools are Monochord's
(``explainer/music/monochord/effects.py``).  The dry sounds are Part 7's piano, Part 40's drums and pad (physical models
and additive synthesis); every filter, room, plate and spring is computed here.  No recorded impulse response is used.

Items:
    hook        an ear question: the Tune in a simulated tiled room and in Schroeder's arithmetic room; which is which?
    conv        a four-sample signal convolved with a four-tap response, step by step
    onepole     the one-pole low-pass: impulse response, frequency response, its pole
    biquads     the cookbook filters' responses; a peaking filter's poles and zeros; Butterworth by bilinear transform
    eq          an ear question: a groove through a low-pass, a high-pass and a peaking boost, shuffled
    phase       an ear question: a snare dry and through 60 all-passes; the all-passes' group delay
    combs       feedforward and feedback combs; a noise burst through a feedback comb becomes a pitch
    mods        a pad through a flanger, a chorus and a phaser
    room        a tiled room by the image-source method: impulse response, energy decay, RT60 against Sabine and Eyring
    sweep       the room measured by an exponential sweep, with and without a little distortion in the loudspeaker
    schroeder   Schroeder's reverberator and a feedback delay network: impulse responses and echo density
    plate       a steel plate by finite differences: impulse response, its decay, and its dispersion
    spring      a spring as a dispersive loop: impulse response and its chirps
    echo        the Tune convolved with a two-tap response: itself and an echo 180 ms later
    ring        clicks through a band-pass whose poles sit close to the circle: they ring at 440 Hz
    bands       reverberation time in octave bands for the room, the plate, the network and Schroeder's reverberator
    cathedral   snare hits and a chord in a cathedral made of eight long delay lines (RT60 set to 5 s)
    tune49      Variation 49: the Tune dry, in the tiled room, on the plate, on the spring and in a cathedral
    variation   the Variations ledger, row 49
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import effects as F
from explainer.music.monochord import tune as T
from explainer.music.monochord.dsp.fourier import stft
from explainer.music.monochord.partkit import saver, signoff
from videos.music.music38 import compute as P38
from videos.music.music40 import compute as P40

CACHE = Cache("music49")
CLIPS = ClipStore("music49")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
save_synth = saver(CLIPS, LEVEL, kind="synthesized")
arr = P38.arr
piano = P38.piano
MAJOR = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
ROOM = {"dims": (2.6, 2.1, 2.5), "src": (0.6, 0.7, 1.5), "mic": (1.9, 1.4, 1.4), "alpha": 0.05}


def tune_signal(phrases=(0,), beat=0.42, tail=0.3) -> np.ndarray:
    p = []
    ev = T.events(beat, list(phrases))
    for e in ev:
        p.append((arr(piano(60 + MAJOR[e["degree"]], e["dur"] * 0.9, 0.75)), e["t"], 0.0))
    end = ev[-1]["t"] + ev[-1]["dur"]
    y = mix(p, duration=end + tail).y
    return 0.5 * y / np.abs(y).max()


def C(y) -> Clip:
    return Clip(np.asarray(y, float), SR)


def wet(x, ir, mix_=0.6, tail=1.5):
    y = F.convolve(x, ir)[: len(x) + int(tail * SR)]
    d = np.concatenate([x, np.zeros(len(y) - len(x))])
    y = y / np.max(np.abs(y)) * np.max(np.abs(x))
    return (1 - mix_) * d + mix_ * y


def impulse(seconds):
    x = np.zeros(int(seconds * SR))
    x[0] = 1.0
    return x


_ROOM_IR = {}
_PLATE = {}


def plate():
    if "p" not in _PLATE:
        _PLATE["p"] = F.plate_ir(seconds=2.5)
    return _PLATE["p"]


def room_ir():
    if "ir" not in _ROOM_IR:
        _ROOM_IR["ir"] = F.room_ir(ROOM["dims"], ROOM["src"], ROOM["mic"], ROOM["alpha"], SR, 1.6)
    return _ROOM_IR["ir"]


# ---------------------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    x = tune_signal()
    a = wet(x, room_ir(), 0.6, 1.6)
    s_ir = F.schroeder(impulse(2.0), SR, F.rt60(room_ir(), SR))
    b = wet(x, s_ir, 0.6, 1.6)
    c = concat([C(b), C(a)], gap=1.0, names=["first", "second"])
    return {"order": ["Schroeder", "room"], "answer": "first", "rt60_room": F.rt60(room_ir(), SR),
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save_synth("hook.two", c, detail="the Tune's first phrase on Part 7's piano through Schroeder's four combs and two all-passes, then through a simulated tiled room (image sources), both with the same reverberation time")}}


def compute_conv() -> dict:
    x = [1.0, 0.5, -0.3, 0.8]
    h = [1.0, 0.0, 0.6, 0.3]
    y = np.convolve(x, h)
    rows = [[float(x[k] * hh) for hh in h] for k in range(len(x))]
    return {"x": x, "h": h, "y": y.tolist(), "rows": rows}


def compute_onepole() -> dict:
    a = 0.9
    n = 40
    imp = F.onepole(np.r_[1.0, np.zeros(n - 1)], a)
    f = np.geomspace(20, 24000, 200)
    r = F.response([1 - a], [1, -a], SR, f)
    return {"a": a, "impulse": imp.tolist(), "f": f.tolist(), "db": r["db"], "pole": a, "cut_hz": float(-SR / (2 * np.pi) * math.log(a))}


def compute_biquads() -> dict:
    f = np.geomspace(20, 24000, 300)
    specs = {"lowpass": ("lowpass", 1000, 0.7071, 0.0), "highpass": ("highpass", 1000, 0.7071, 0.0), "peak": ("peak", 1000, 1.0, 9.0),
             "lowshelf": ("lowshelf", 200, 0.7071, 6.0), "highshelf": ("highshelf", 5000, 0.7071, 6.0)}
    out = {}
    for k, (kind, f0, q, g) in specs.items():
        b, a = F.biquad(kind, f0, SR, q, g)
        out[k] = F.response(b, a, SR, f)
        out[k]["spec"] = [kind, f0, q, g]
    b, a = F.butter2_bilinear(1000, SR)
    from scipy.signal import butter
    bs, as_ = butter(2, 1000, fs=SR)
    out["butter_match"] = float(np.max(np.abs(np.r_[b - bs, a - as_])))
    out["f"] = f.tolist()
    return out


def groove(bars=2, bpm=100):
    parts = []
    P40.drums(parts, "rock", bpm, bars, gain=-1.0)
    beat = 60 / bpm
    for i, m in enumerate([36, 36, 43, 41] * bars):
        parts.append((arr(P38.bass(m, beat * 0.9)), i * beat, -2.0))
    for e in T.events(beat / 2, [0]):
        parts.append((arr(piano(72 + MAJOR[e["degree"]], e["dur"] * 0.9, 0.7)), e["t"], -3.0))
    y = mix(parts, duration=bars * 4 * beat + 0.6).y
    return 0.5 * y / np.abs(y).max()


EQ = {"low-pass at 800 Hz": ("lowpass", 800, 0.7071, 0.0), "high-pass at 2 kHz": ("highpass", 2000, 0.7071, 0.0),
      "a 12 dB boost at 1 kHz": ("peak", 1000, 1.5, 12.0)}
EQ_ORDER = ["high-pass at 2 kHz", "a 12 dB boost at 1 kHz", "low-pass at 800 Hz"]


def compute_eq() -> dict:
    from scipy.signal import lfilter
    g = groove()
    clips = [C(g)]
    for k in EQ_ORDER:
        b, a = F.biquad(*((EQ[k][0], EQ[k][1], SR, EQ[k][2], EQ[k][3])))
        clips.append(C(lfilter(b, a, g)))
    c = concat(clips, gap=0.8, names=["dry", "first", "second", "third"])
    return {"order": EQ_ORDER, "starts": {k: float(c.events[k]) for k in ("dry", "first", "second", "third")},
            "clips": {"four": save("eq.four", c, detail="a groove on Part 40's drums, a plucked bass and Part 7's piano: dry, then through a high-pass at 2 kHz, a 12 dB peak at 1 kHz and a low-pass at 800 Hz")}}


def compute_phase() -> dict:
    s = arr(P40.snare(0)).y
    s = np.r_[s, np.zeros(int(0.3 * SR))]
    coeffs = [-0.9] * 60
    y = F.allpass_chain(s, coeffs)
    hits = []
    for v in (s, y):
        z = np.r_[v, np.zeros(int(0.2 * SR))]
        hits.append(C(np.concatenate([z, z])))
    c = concat(hits, gap=1.0, names=["first", "second"])
    f = np.geomspace(30, 20000, 200)
    gd = np.zeros(len(f))
    for cc in coeffs[:1]:
        gd = F.group_delay([cc, 1.0], [1.0, cc], SR, f) * len(coeffs)
    mag_s = np.abs(np.fft.rfft(np.r_[s, np.zeros(SR)]))
    mag_y = np.abs(np.fft.rfft(np.r_[y, np.zeros(SR)]))[: len(mag_s)]
    return {"answer": "second", "f": f.tolist(), "group_delay_ms": (1000 * gd).tolist(), "stages": len(coeffs),
            "mag_ratio_db_max": float(np.max(np.abs(20 * np.log10((mag_y[1:2000] + 1e-9) / (mag_s[1:2000] + 1e-9))))),
            "dry": s[:int(0.12 * SR):4].tolist(), "wet": y[:int(0.12 * SR):4].tolist(),
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("phase.two", c, detail="a snare from Part 40 struck twice, dry, then struck twice through 60 first-order all-passes, which change no frequency's level, only its delay")}}


def compute_combs() -> dict:
    f = np.geomspace(20, 24000, 600)
    D = 48
    ff = F.response(np.r_[1.0, np.zeros(D - 1), 0.9], [1.0], SR, f)
    a = np.zeros(D + 1)
    a[0], a[D] = 1.0, -0.9
    fb = F.response([1.0], a, SR, f)
    rng = np.random.default_rng(49)
    burst = np.r_[rng.uniform(-1, 1, int(0.02 * SR)), np.zeros(int(1.5 * SR))]
    Dp = int(round(SR / 220.0))
    pitched = F.comb_fb(burst, Dp, 0.985)
    c = concat([C(burst[: int(0.4 * SR)]), C(pitched)], gap=0.8, names=["burst", "comb"])
    return {"D": D, "f": f.tolist(), "ff": ff["db"], "fb": fb["db"], "Dp": Dp, "pitch": SR / Dp,
            "starts": {"burst": float(c.events["burst"]), "comb": float(c.events["comb"])},
            "clips": {"two": save_synth("combs.two", c, detail="a 20 ms burst of noise, then the same burst through a feedback comb 218 samples long with gain 0.985: a pitch of 220 Hz")}}


def compute_mods() -> dict:
    p = arr(P40.pad([0, 4, 7], 4.0, base=60, bright=4000)).y * 0.5
    fl = F.flanger(p, SR, depth_ms=4.0, base_ms=0.5, rate=0.3, mix=0.8, feedback=0.6)
    ch = F.chorus(p, SR, voices=3)
    ph = F.phaser(p, SR, stages=8, rate=0.35)
    c = concat([C(fl), C(ch), C(ph)], gap=0.8, names=["flanger", "chorus", "phaser"])
    return {"order": ["flanger", "chorus", "phaser"], "starts": {k: float(c.events[k]) for k in ("flanger", "chorus", "phaser")},
            "clips": {"three": save_synth("mods.three", c, detail="a C major pad (Part 40's additive pad) through a flanger (a swept 0.5-4.5 ms comb with feedback), a three-voice chorus (15-25 ms), and an eight-stage phaser")}}


def compute_room() -> dict:
    ir = room_ir()
    e = F.edc(ir)
    dims, a = ROOM["dims"], ROOM["alpha"]
    t60 = F.rt60(ir, SR)
    early = []
    nz = np.flatnonzero(np.abs(ir[: int(0.03 * SR)]) > 0.08)
    last = -100
    for i in nz:
        if i - last > 10:
            early.append([float(i / SR * 1000), float(ir[i])])
            last = i
    x = tune_signal()
    c = concat([C(np.r_[x, np.zeros(int(1.0 * SR))]), C(wet(x, ir, 0.6, 1.6))], gap=1.0, names=["dry", "room"])
    L = np.array(dims)
    V = float(L.prod())
    S = float(2 * (L[0] * L[1] + L[1] * L[2] + L[0] * L[2]))
    return {"dims": list(dims), "alpha": a, "V": V, "S": S, "rt60": t60, "sabine": F.sabine(dims, a), "eyring": F.eyring(dims, a),
            "ir": ir[: int(0.25 * SR):24].tolist(), "edc": e[: int(1.6 * SR):240].tolist(), "early": early[:12],
            "direct_ms": float(np.linalg.norm(np.array(ROOM["src"]) - np.array(ROOM["mic"])) / F.C_AIR * 1000),
            "starts": {"dry": float(c.events["dry"]), "room": float(c.events["room"])},
            "clips": {"two": save_synth("room.two", c, detail="the Tune's first phrase on Part 7's piano, dry, then in a simulated tiled room 2.6 by 2.1 by 2.5 m (image sources, 5% absorption)")}}


def compute_sweep() -> dict:
    f1, f2, T_ = 20.0, 20000.0, 3.0
    s = 0.5 * F.ess(f1, f2, T_, SR)
    inv = F.ess_inverse(f1, f2, T_, SR) * 2.0
    ir = room_ir()
    rng = np.random.default_rng(1)
    rec = F.convolve(s, ir) + 1e-4 * rng.standard_normal(len(s) + len(ir) - 1)
    got = F.convolve(rec, inv)
    k0 = len(s) - 1
    est = got[k0:k0 + len(ir)]
    from scipy.signal import butter, sosfiltfilt
    band = butter(4, [25.0, 19000.0], btype="band", fs=SR, output="sos")
    ref = sosfiltfilt(band, ir)[: int(0.5 * SR)]
    e5 = est[: int(0.5 * SR)]
    gain = float(np.dot(ref, e5) / np.dot(e5, e5))
    err = float(10 * np.log10(np.sum((gain * e5 - ref) ** 2) / np.sum(ref ** 2)))
    est = est / np.max(np.abs(est))
    rec_d = F.convolve(np.tanh(2.5 * s) / 2.5, ir)
    got_d = F.convolve(rec_d, inv)
    win = got_d[k0 - int(0.8 * SR):k0 + int(0.2 * SR)]
    win = win / np.max(np.abs(win))
    harm = [float(-T_ * math.log(k) / math.log(f2 / f1)) for k in (2, 3, 4, 5)]
    c = C(np.r_[s[: int(1.6 * SR)] * 0.6, np.zeros(int(0.2 * SR))])
    return {"f1": f1, "f2": f2, "T": T_, "error_db": err, "est": est[: int(0.25 * SR):24].tolist(), "true": ir[: int(0.25 * SR):24].tolist(),
            "distorted": np.abs(win[::48]).tolist(), "harmonic_s": harm, "sweep_head": s[: int(0.05 * SR)].tolist(),
            "clips": {"sweep": save_synth("sweep.sweep", c, detail="the first 1.6 seconds of an exponential sine sweep from 20 Hz to 20 kHz in 3 seconds")}}


def compute_schroeder() -> dict:
    t60 = 2.0
    s = F.schroeder(impulse(2.5), SR, t60)
    d = F.fdn(impulse(2.5), SR, t60, damping=0.15)
    ir = room_ir()
    out = {"t60": t60, "rt_schroeder": F.rt60(s, SR), "rt_fdn": F.rt60(d, SR),
           "density": {"schroeder": F.echo_density(s, SR)[:40].tolist(), "fdn": F.echo_density(d, SR)[:40].tolist(), "room": F.echo_density(ir, SR)[:40].tolist()},
           "ir_s": (s[: int(0.15 * SR):12] / np.max(np.abs(s))).tolist(), "ir_f": (d[: int(0.15 * SR):12] / np.max(np.abs(d))).tolist(),
           "combs_ms": list(F.SCHROEDER_COMBS_MS), "allpass": [list(x) for x in F.SCHROEDER_ALLPASS], "fdn_ms": list(F.FDN_MS)}
    claps = np.zeros(int(2.4 * SR))
    for k in range(4):
        sn = arr(P40.snare(k)).y
        i = int(k * 0.5 * SR)
        claps[i:i + len(sn)] += sn[: len(claps) - i]
    a = wet(claps, s, 0.55, 2.0)
    b = wet(claps, d, 0.55, 2.0)
    c = concat([C(a), C(b)], gap=1.0, names=["schroeder", "fdn"])
    out["starts"] = {"schroeder": float(c.events["schroeder"]), "fdn": float(c.events["fdn"])}
    out["clips"] = {"two": save_synth("schroeder.two", c, detail="four snare hits from Part 40 through Schroeder's reverberator, then through an eight-line feedback delay network, both set to 2 seconds")}
    return out


def compute_plate() -> dict:
    p = plate()
    ir = p["ir"]
    f, t, S = stft(ir[: int(0.12 * SR)], SR, n=512, hop=64)
    mag = 20 * np.log10(np.abs(S) + 1e-9)
    mag = mag - mag.max()
    keep = f <= 12000
    x = tune_signal()
    c = C(wet(x, ir, 0.55, 2.0))
    return {"rt60": F.rt60(ir, SR), "kappa": p["kappa"], "h": p["h"], "grid": p["grid"], "mu": p["mu"],
            "ir": ir[: int(0.12 * SR):6].tolist(), "edc": F.edc(ir)[::240].tolist(),
            "spec": np.clip(mag[keep][::2], -60, 0).round(1).tolist(), "spec_f": f[keep][::2].tolist(), "spec_t": t.tolist(),
            "clips": {"tune": save_synth("plate.tune", c, detail="the Tune's first phrase on Part 7's piano through a simulated 2 by 1 m steel plate, 0.5 mm thick (finite differences)")}}


def compute_spring() -> dict:
    ir = F.spring_ir(seconds=2.0)
    f, t, S = stft(ir[: int(0.25 * SR)], SR, n=512, hop=128)
    mag = 20 * np.log10(np.abs(S) + 1e-9)
    mag = mag - mag.max()
    keep = f <= 8000
    hit = np.zeros(int(2.5 * SR))
    sn = arr(P40.snare(3)).y
    hit[: len(sn)] = sn
    pl = arr(P38.bass(45, 0.6)).y
    hit[int(1.0 * SR):int(1.0 * SR) + len(pl)] += pl[: len(hit) - int(1.0 * SR)]
    c = C(wet(hit, ir, 0.6, 1.5))
    return {"rt60": F.rt60(ir, SR, -5, -20), "ir": ir[: int(0.25 * SR):12].tolist(),
            "spec": np.clip(mag[keep][::2], -60, 0).round(1).tolist(), "spec_f": f[keep][::2].tolist(), "spec_t": t.tolist(),
            "clips": {"hit": save_synth("spring.hit", c, detail="a snare hit from Part 40 and a plucked bass note through a simulated spring: a loop of 80 dispersive all-passes, 35 ms long")}}


def compute_echo() -> dict:
    x = tune_signal()
    h = np.zeros(int(0.18 * SR) + 1)
    h[0], h[-1] = 1.0, 0.6
    y = F.convolve(x, h)
    c = concat([C(np.r_[x, np.zeros(int(0.3 * SR))]), C(y)], gap=1.0, names=["dry", "echo"])
    return {"delay_ms": 180, "gain": 0.6, "starts": {"dry": float(c.events["dry"]), "echo": float(c.events["echo"])},
            "clips": {"two": save("echo.two", c, detail="the Tune's first phrase on Part 7's piano, dry, then convolved with two taps: itself, and a copy 180 ms later at 0.6")}}


def compute_ring() -> dict:
    from scipy.signal import lfilter
    x = np.zeros(int(3.0 * SR))
    for k in range(4):
        x[int(k * 0.7 * SR)] = 1.0
    out, info = [], {}
    for q in (2.0, 50.0):
        b, a = F.biquad("bandpass", 440.0, SR, q)
        y = lfilter(b, a, x)
        out.append(C(y / np.max(np.abs(y)) * 0.6))
        r = float(np.abs(np.roots(a)).max())
        info[str(int(q))] = {"pole_radius": r, "ring_ms": float(-1000 / (SR * math.log(r)))}
    c = concat(out, gap=0.8, names=["wide", "narrow"])
    return {"info": info, "starts": {"wide": float(c.events["wide"]), "narrow": float(c.events["narrow"])},
            "clips": {"two": save_synth("ring.two", c, detail="four clicks through a band-pass at 440 Hz with Q 2, then with Q 50, whose poles sit close to the unit circle")}}


def octave_rt60(ir, sr, centres=(125, 250, 500, 1000, 2000, 4000)):
    from scipy.signal import butter, sosfiltfilt
    out = {}
    for fc in centres:
        sos = butter(3, [fc / math.sqrt(2), min(fc * math.sqrt(2), sr / 2 * 0.95)], btype="band", fs=sr, output="sos")
        y = sosfiltfilt(sos, ir)
        try:
            out[str(fc)] = F.rt60(y, sr, -5, -25)
        except Exception:
            out[str(fc)] = None
    return out


def compute_bands() -> dict:
    sch = F.schroeder(impulse(2.5), SR, 2.0)
    fd = F.fdn(impulse(2.5), SR, 2.0, damping=0.15)
    pl = plate()["ir"]
    L = np.array(ROOM["dims"])
    V = float(L.prod())
    t = F.rt60(room_ir(), SR)
    return {"room": octave_rt60(room_ir(), SR), "plate": octave_rt60(pl, SR), "fdn": octave_rt60(fd, SR), "schroeder": octave_rt60(sch, SR),
            "schroeder_freq": float(2000 * math.sqrt(t / V)), "V": V, "rt60": t}


_CATH = {}


def cathedral():
    if "c" not in _CATH:
        _CATH["c"] = F.fdn(impulse(6.0), SR, 5.0, delays_ms=tuple(3 * m for m in F.FDN_MS), damping=0.2)
    return _CATH["c"]


def compute_cathedral() -> dict:
    x = np.zeros(int(6.5 * SR))
    for k in range(3):
        sn = arr(P40.snare(k)).y
        i = int(k * 0.6 * SR)
        x[i:i + len(sn)] += sn[: len(x) - i]
    ch = sum(arr(piano(m, 1.5, 0.7)).y for m in (48, 55, 60, 64))
    i = int(2.4 * SR)
    x[i:i + len(ch)] += 0.5 * ch[: len(x) - i] / np.max(np.abs(ch))
    y = wet(x, cathedral(), 0.7, 4.0)
    ir = cathedral()
    return {"rt60": F.rt60(ir, SR), "delays_ms": [3 * m for m in F.FDN_MS], "first_ms": 3 * F.FDN_MS[0],
            "clips": {"hits": save_synth("cathedral.hits", C(y), detail="three snare hits from Part 40 and a C major chord on Part 7's piano in a cathedral made of eight delay lines from 88 to 219 ms, fed back through a Hadamard matrix (RT60 set to 5 s)")}}


def compute_tune49() -> dict:
    x = tune_signal()
    rooms = {}
    rooms["dry"] = np.r_[x, np.zeros(int(0.8 * SR))]
    rooms["tiled room"] = wet(x, room_ir(), 0.6, 1.6)
    pl = plate()["ir"]
    rooms["plate"] = wet(x, pl, 0.55, 2.0)
    rooms["spring"] = wet(x, F.spring_ir(seconds=2.0), 0.6, 1.6)
    cath = cathedral()
    rooms["cathedral"] = wet(x, cath, 0.65, 4.0)
    names = list(rooms)
    c = concat([C(rooms[k]) for k in names], gap=0.6, names=names)
    rt = {"tiled room": F.rt60(room_ir(), SR), "plate": F.rt60(pl, SR), "spring": F.rt60(F.spring_ir(seconds=2.0), SR, -5, -20),
          "cathedral": F.rt60(cath, SR)}
    return {"names": names, "rt60": rt, "seconds": c.duration, "starts": {k: float(c.events[k]) for k in names},
            "clips": {"variation49": save_synth("tune.variation49", c, detail="the Tune's first phrase on Part 7's piano: dry, in a simulated tiled room, on a simulated steel plate, on a simulated spring, and in a cathedral made by a feedback delay network")}}


def compute_variation() -> dict:
    t = load("tune49")
    r = t["rt60"]
    return {"part": 49, "title": "dry, then in a tiled room, on a plate, on a spring and in a cathedral", "seconds": round(t["seconds"], 1),
            "measure": f"reverberation time {r['tiled room']:.1f} s in the room, {r['plate']:.1f} s on the plate, {r['spring']:.1f} s on the spring, {r['cathedral']:.1f} s in the cathedral",
            "clip": "tune.variation49"}


def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation49", 49)


ITEMS = {"hook": compute_hook, "conv": compute_conv, "onepole": compute_onepole, "biquads": compute_biquads, "eq": compute_eq,
         "phase": compute_phase, "combs": compute_combs, "mods": compute_mods, "room": compute_room, "sweep": compute_sweep,
         "schroeder": compute_schroeder, "plate": compute_plate, "spring": compute_spring, "echo": compute_echo, "ring": compute_ring,
         "bands": compute_bands, "cathedral": compute_cathedral, "tune49": compute_tune49,
         "variation": compute_variation,
         "signoff": compute_signoff}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
