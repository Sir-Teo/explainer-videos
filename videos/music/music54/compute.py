"""Precompute everything numerical, and every sound, in Part 54 of *Music, Built* ("Microphones and Loudspeakers").

    python -m videos.music.music54.compute              # everything missing (about a minute)
    python -m videos.music.music54.compute --force hook

Numbers are cached in ``.cache/music54/<name>.json``, sounds in ``.cache/music54/audio/``.  The tools are Monochord's
(``explainer/music/monochord/transducer.py``); the voice is Part 8's, the piano Part 7's, the groove Part 50's (Part 40's
drums and a plucked bass).  Every microphone, line, box and loudspeaker is simulated.

Items:
    hook        an ear question: the Tune sung into a measurement microphone and into a pair of headphones used backwards
    patterns    the first-order family drawn, with directivity, rear rejection and nulls
    capture     a voice in front, a piano behind, a room around: picked up by an omni, a cardioid and a figure-8
    rotate      a singer walking once round a cardioid
    proximity   a figure-8 at 1 m, 15 cm and 5 cm from a singer: the bass rise, drawn and heard
    noise       thermal noise, a preamplifier's floor, a dynamic microphone's equivalent noise
    hum         a line picking up mains hum: unbalanced, then balanced with 1 per cent imbalance
    driver      a woofer's Thiele-Small parameters; sealed and vented boxes simulated and checked against Small's and
                Thiele's closed forms; impedance curves
    speakers    a groove through a phone's speaker, a sealed bookshelf and a vented floor-stander
    horn        an exponential horn's throat resistance against a bare cone's
    crossover   Butterworth sections summed in phase and inverted, and Linkwitz-Riley
    xover       music through Butterworth sections in phase, then Linkwitz-Riley
    anc         an aircraft-cabin drone at the ear, without and with an adaptive canceller (filtered-x LMS)
    beam        two singers, one microphone and an eight-microphone array steered at one of them
    tune54      Variation 54: the Tune through three microphone patterns and three loudspeakers
    variation   the Variations ledger, row 54
"""

from __future__ import annotations

import math

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import effects as E
from explainer.music.monochord import transducer as TD
from explainer.music.monochord import tune as T
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.partkit import saver
from videos.music.music38 import compute as P38
from videos.music.music50 import compute as P50

CACHE = Cache("music54")
CLIPS = ClipStore("music54")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
save_synth = saver(CLIPS, LEVEL, kind="synthesized")
MAJOR = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}


def C(y) -> Clip:
    return Clip(np.asarray(y, float), SR)


def tune_notes(phrases=(0,), base=60, beat=0.5):
    return [(base + MAJOR[e["degree"]], e["t"], e["dur"]) for e in T.events(beat, list(phrases))]


def norm_rms(y, target=0.1):
    return y * target / (np.sqrt(np.mean(np.asarray(y) ** 2)) + 1e-12)


def fade(y, a=0.005, r=0.05):
    y = np.array(y, float)
    ka, kr = max(int(a * SR), 1), max(int(r * SR), 1)
    y[:ka] *= np.linspace(0, 1, ka)
    y[len(y) - kr:] *= np.linspace(1, 0, kr)
    return y


def db(x):
    return 10 * math.log10(np.mean(np.asarray(x) ** 2) + 1e-30)


_V = {}


def tenor(phrases=(0,), base=48, beat=0.5):
    key = (tuple(phrases), base, beat)
    if key not in _V:
        y = CH.sing(tune_notes(phrases, base, beat), "tenor", "a")
        _V[key] = 0.5 * y / np.max(np.abs(y))
    return _V[key]


def piano_chords(seconds, beat=0.5, base=48):
    parts = []
    t = 0.0
    prog = [(0, 4, 7), (5, 9, 12), (0, 4, 7), (7, 11, 14)]
    j = 0
    while t < seconds:
        for iv in prog[j % 4]:
            parts.append((C(np.asarray(P38.piano(base + iv, 2 * beat), float)), t, -3.0))
        t += 2 * beat
        j += 1
    y = mix(parts, duration=seconds + 0.5).y[: int(seconds * SR)]
    return 0.5 * y / np.max(np.abs(y))


HP = TD.Driver(fs=110.0, Qes=1.2, Qms=2.5, Vas=0.00015, Sd=0.0011, Re=32.0)


def compute_hook() -> dict:
    v = tenor()
    ref = v
    hp = TD.apply_response(v, lambda f: TD.headphone_as_mic(f, HP) / TD.headphone_as_mic(np.array([1000.0]), HP)[0])
    c = concat([C(norm_rms(fade(ref))), C(norm_rms(fade(hp)))], gap=1.0, names=["first", "second"])
    f = np.geomspace(20, 20000, 200)
    H = 20 * np.log10(np.abs(TD.headphone_as_mic(f, HP)) / np.abs(TD.headphone_as_mic(np.array([1000.0]), HP)[0]))
    return {"answer": "second", "f": f.tolist(), "H": H.tolist(), "hp": {"fs": HP.fs, "Bl": HP.Bl, "Mms": HP.Mms},
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("hook.two", c, detail="the Tune's first phrase sung by Part 8's voice, picked up by an ideal measurement microphone, then by a small headphone driver used as a microphone (simulated)")}}


def compute_patterns() -> dict:
    th = np.linspace(0, 2 * np.pi, 361)
    out = {"theta": th.tolist(), "names": list(TD.PATTERNS)}
    for k, A in TD.PATTERNS.items():
        out[k] = {"r": np.abs(TD.pattern(A, th)).tolist(), "sign": np.sign(TD.pattern(A, th)).tolist(), **{kk: (None if (isinstance(vv, float) and not np.isfinite(vv)) else vv) for kk, vv in TD.directivity(A).items()}}
    return out


def room_ir(seconds=0.9, seed=3):
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    y = rng.standard_normal(n) * np.exp(-t / 0.12) * np.clip(t / 0.01, 0, 1)
    y = sosfilt(butter(2, [150, 6000], btype="band", fs=SR, output="sos"), y)
    return y / np.sqrt(np.sum(y ** 2))


def capture(A, voice, behind, room_gain=0.35, behind_angle=160.0):
    """A microphone of pattern A: the voice on axis, the second source at ``behind_angle``, and diffuse room sound,
    which a directional microphone picks up in proportion to its random-energy efficiency."""
    g_b = TD.pattern(A, math.radians(behind_angle))
    ree = TD.directivity(A)["REE"]
    room = fftconvolve(voice + behind, room_ir())[: len(voice)]
    return voice + g_b * behind + room_gain * math.sqrt(ree) * room


def compute_capture() -> dict:
    v = tenor()
    n = len(v)
    pno = piano_chords(n / SR)[:n] * 0.9
    out, clips, names = {}, [], []
    for name in ("omni", "cardioid", "figure-8"):
        A = TD.PATTERNS[name]
        y = capture(A, v, pno)
        back = TD.pattern(A, math.radians(160))
        out[name] = {"rear_db": 20 * math.log10(abs(back)) if abs(back) > 1e-9 else -99.0, "ree": TD.directivity(A)["REE"]}
        clips.append(C(norm_rms(fade(y))))
        names.append(name)
    c = concat(clips, gap=0.7, names=names)
    return {**out, "starts": {k: float(c.events[k]) for k in names},
            "clips": {"three": save("capture.three", c, detail="Part 8's voice singing in front of the microphone, Part 7's piano behind it, in a lively room: an omnidirectional, a cardioid and a figure-8 microphone (simulated)")}}


def compute_rotate() -> dict:
    """A singer walking once round a cardioid microphone in six seconds: the level follows the pattern."""
    v = tenor(phrases=(0, 1), beat=0.42)
    n = len(v)
    t = np.arange(n) / SR
    secs = n / SR
    ang = 2 * np.pi * t / secs
    g = TD.pattern(0.5, ang)
    y = v * g
    c = concat([C(fade(0.5 * y / np.max(np.abs(y))))], names=["walk"])
    return {"seconds": secs, "clips": {"one": save("rotate.one", c, detail="Part 8's voice singing while walking once round a cardioid microphone, starting in front (simulated)")}}


def compute_proximity() -> dict:
    f = np.geomspace(20, 20000, 200)
    curves = {}
    for r in (1.0, 0.15, 0.05):
        curves[str(r)] = {"fig8": (20 * np.log10(np.abs(TD.proximity(f, r, 0.0)))).tolist(),
                          "card": (20 * np.log10(np.abs(TD.proximity(f, r, 0.5)))).tolist()}
    v = tenor()
    clips = []
    for r in (1.0, 0.15, 0.05):
        y = TD.apply_response(v, lambda ff, r=r: TD.proximity(ff, r, 0.0))
        y = sosfilt(butter(1, 30, btype="high", fs=SR, output="sos"), y)
        clips.append(C(norm_rms(fade(y))))
    c = concat(clips, gap=0.7, names=["far", "near", "close"])
    at = {str(r): float(20 * np.log10(abs(TD.proximity(np.array([100.0]), r, 0.0)[0]))) for r in (1.0, 0.15, 0.05)}
    return {"f": f.tolist(), "curves": curves, "at100": at, "starts": {k: float(c.events[k]) for k in ("far", "near", "close")},
            "clips": {"three": save("proximity.three", c, detail="Part 8's tenor voice through a figure-8 microphone 1 m, 15 cm and 5 cm away (simulated), matched in loudness")}}


def compute_noise() -> dict:
    vn = TD.thermal_noise(200.0)
    ein = 20 * math.log10(vn / 0.7746)
    sens = 0.002
    sig94 = 20 * math.log10(sens / 0.7746)
    eq_spl = 94 - (sig94 - ein)
    return {"vn_uv": vn * 1e6, "ein_dbu": ein, "sens_mv": 1000 * sens, "sig94_dbu": sig94, "eq_spl": eq_spl,
            "condenser_self": 10.0, "quiet_room": 25.0}


def hum_wave(n, f0=50.0):
    t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * k * f0 * t + 0.3 * k) / k ** 0.6 for k in (1, 3, 5, 7, 9, 11))


def compute_hum() -> dict:
    v = tenor()
    n = len(v)
    h = 0.05 * hum_wave(n)
    un = TD.balanced(v, h, balanced_line=False)
    bal = TD.balanced(v, h, imbalance=0.01)
    hum_un = db(un - v)
    hum_bal = db(bal - v)
    c = concat([C(fade(0.3 * un / np.max(np.abs(un)))), C(fade(0.3 * bal / np.max(np.abs(un))))], gap=0.8, names=["unbalanced", "balanced"])
    return {"rejection_db": hum_un - hum_bal, "hum_un": hum_un - db(v), "hum_bal": hum_bal - db(v),
            "starts": {"unbalanced": float(c.events["unbalanced"]), "balanced": float(c.events["balanced"])},
            "clips": {"two": save("hum.two", c, detail="Part 8's voice down a long cable beside a mains transformer: an unbalanced line, then a balanced one whose two conductors pick up the hum within 1 per cent of each other", level=None)}}


WOOFER = TD.Driver()
SPEAKERS = {
    "phone": (TD.Driver(fs=750.0, Qes=1.0, Qms=3.0, Vas=0.000002, Sd=0.00012, Re=8.0), {"kind": "sealed", "Vb": 0.000002}, 9000.0),
    "bookshelf": (TD.Driver(fs=55.0, Qes=0.45, Qms=4.0, Vas=0.012, Sd=0.013, Re=6.0), {"kind": "sealed", "Vb": 0.010}, 18000.0),
    "floor": (TD.Driver(fs=32.0, Qes=0.39, Qms=4.0, Vas=0.090, Sd=0.034, Re=6.0), {"kind": "vented", "Vb": 0.060, "fb": 32.0}, 20000.0),
}


def speaker_H(name):
    d, box, top = SPEAKERS[name]
    ref = np.abs(TD.response(d, np.array([2000.0]), box)["U"])[0] * 2000.0

    def H(f):
        r = TD.response(d, f, box)
        g = r["U"] * 1j * f / ref
        return g / (1 + 1j * f / top) ** 2
    return H


def compute_driver() -> dict:
    d = WOOFER
    f = np.geomspace(10, 2000, 600)
    out = {"ts": {"fs": d.fs, "Qes": d.Qes, "Qms": d.Qms, "Qts": d.Qts, "Vas_l": 1000 * d.Vas, "Sd_cm2": 1e4 * d.Sd, "Re": d.Re,
                  "Bl": d.Bl, "Mms_g": 1000 * d.Mms, "Cms_mm_per_N": 1000 * d.Cms, "Rms": d.Rms}, "f": f.tolist()}
    checks = []
    curves = {}
    for Vb in (0.020, 0.050, 0.200):
        r = TD.response(d, f, {"kind": "sealed", "Vb": Vb})
        al = TD.sealed_alignment(d, Vb)
        checks.append({"Vb_l": 1000 * Vb, "sim_f3": TD.f_minus(f, r["spl"]), "formula_f3": al["f3"], "Qtc": al["Qtc"], "fc": al["fc"]})
        curves[f"sealed{int(1000 * Vb)}"] = (r["spl"] - r["spl"][-1]).tolist()
    d4 = d.with_(Qes=0.383, Qms=1e6)
    b4 = TD.vented_b4(d4)
    r4 = TD.response(d4, f, {"kind": "vented", "Vb": b4["Vb"], "fb": b4["fb"], "Ql": 1e6})
    curves["b4"] = (r4["spl"] - r4["spl"][-1]).tolist()
    sealed_b4 = TD.response(d4, f, {"kind": "sealed", "Vb": b4["Vb"]})
    curves["b4_sealed_same_box"] = (sealed_b4["spl"] - sealed_b4["spl"][-1]).tolist()
    b4c = {"Vb_l": 1000 * b4["Vb"], "fb": b4["fb"], "sim_f3": TD.f_minus(f, r4["spl"]), "formula_f3": b4["f3"],
           "ripple": float(np.max(r4["spl"][f > 1.2 * b4["f3"]] - r4["spl"][-1])), "sealed_f3": TD.f_minus(f, sealed_b4["spl"])}
    Z = {"baffle": np.abs(TD.response(d, f)["Z"]).tolist(), "sealed": np.abs(TD.response(d, f, {"kind": "sealed", "Vb": 0.050})["Z"]).tolist(),
         "vented": np.abs(TD.response(d, f, {"kind": "vented", "Vb": 0.050, "fb": 38.0})["Z"]).tolist()}
    sens = TD.response(d, np.array([500.0]))["spl"][0]
    return {**out, "checks": checks, "b4": b4c, "curves": curves, "Z": Z, "sens_1w1m": float(sens)}


def compute_speakers() -> dict:
    g = P50.groove(bars=2, bpm=96)
    names = ["phone", "bookshelf", "floor"]
    f = np.geomspace(20, 20000, 300)
    curves, f3 = {}, {}
    clips = []
    for nm in names:
        H = speaker_H(nm)
        resp = 20 * np.log10(np.abs(H(f)) + 1e-12)
        curves[nm] = resp.tolist()
        ref = float(np.median(resp[(f > 1500) & (f < 4000)]))
        above = np.where(resp >= ref - 3)[0]
        f3[nm] = float(f[above[0]])
        y = TD.apply_response(g, H)
        clips.append(C(norm_rms(fade(y))))
    c = concat(clips, gap=0.8, names=names)
    return {"f": f.tolist(), "curves": curves, "f3": f3, "starts": {k: float(c.events[k]) for k in names},
            "params": {k: {"fs": SPEAKERS[k][0].fs, "Sd_cm2": 1e4 * SPEAKERS[k][0].Sd, "box": SPEAKERS[k][1]} for k in names},
            "clips": {"three": save("speakers.three", c, detail="a groove of Part 40's drums and a plucked bass played through three simulated loudspeakers: a phone's, a sealed bookshelf speaker, a vented floor-stander; matched in loudness")}}


def compute_horn() -> dict:
    f = np.geomspace(20, 5000, 300)
    S = 0.005
    m = 4.0
    Rh, fc = TD.horn_throat(f, S, m)
    a = math.sqrt(S / math.pi)
    Rp = TD.piston_resistance(f, a)
    rhoc = TD.RHO * TD.C / S
    return {"f": f.tolist(), "horn": (Rh / rhoc).tolist(), "piston": (Rp / (TD.RHO * TD.C * S) ).tolist(), "fc": fc, "S": S, "m": m,
            "gain_200": float(10 * math.log10((Rh / rhoc)[np.argmin(abs(f - 200))] / (Rp / (TD.RHO * TD.C * S))[np.argmin(abs(f - 200))]))}


def compute_crossover() -> dict:
    f = np.geomspace(100, 40000, 400)
    out = {"f": f.tolist(), "fc": 2000.0}
    for k in ("bw2", "bw2_inv", "lr4"):
        lp, hp, s = TD.crossover(f, k, 2000.0)
        out[k] = {"lp": (20 * np.log10(np.abs(lp))).tolist(), "hp": (20 * np.log10(np.abs(hp))).tolist(), "sum": np.maximum(20 * np.log10(np.abs(s) + 1e-9), -40).tolist(),
                  "at_fc": float(20 * np.log10(abs(TD.crossover(np.array([2000.0]), k, 2000.0)[2][0]) + 1e-12))}
    return out


def compute_xover() -> dict:
    """Music through a two-way crossover at 2 kHz with ideal drivers: second-order Butterworth sections in phase (a hole
    at the crossover), then Linkwitz-Riley (flat)."""
    v = tenor()
    n = len(v)
    pno = piano_chords(n / SR)[:n]
    x = v + 0.6 * pno
    rng = np.random.default_rng(4)
    x = x + 0.02 * sosfilt(butter(2, 1500, btype="high", fs=SR, output="sos"), rng.standard_normal(n))
    a = TD.apply_response(x, lambda f: TD.crossover(f, "bw2", 2000.0)[2])
    b = TD.apply_response(x, lambda f: TD.crossover(f, "lr4", 2000.0)[2])
    c = concat([C(norm_rms(fade(a))), C(norm_rms(fade(b)))], gap=0.8, names=["hole", "flat"])
    return {"starts": {"hole": float(c.events["hole"]), "flat": float(c.events["flat"])},
            "clips": {"two": save_synth("xover.two", c, detail="a voice and piano through a two-way crossover at 2 kHz: Butterworth sections in phase, then Linkwitz-Riley")}}


def compute_anc() -> dict:
    rng = np.random.default_rng(1)
    secs = 8.0
    n = int(secs * SR)
    t = np.arange(n) / SR
    drone = sum(np.sin(2 * np.pi * k * 92.0 * t + 0.7 * k) / k for k in range(1, 7))
    rumble = sosfilt(butter(2, 400, fs=SR, output="sos"), rng.standard_normal(n)) * 3.0
    hiss = sosfilt(butter(2, [2000, 8000], btype="band", fs=SR, output="sos"), rng.standard_normal(n)) * 0.25
    outside = drone + rumble + hiss
    prim = np.zeros(120)
    prim[72] = 0.8
    prim[73] = 0.3
    at_ear = fftconvolve(outside, prim)[:n]
    # some of the noise at the ear never passes the outside microphone (it comes through the seat and the frame)
    at_ear = at_ear + 0.08 * sosfilt(butter(2, 300, fs=SR, output="sos"), np.random.default_rng(9).standard_normal(n)) * 3.0
    # the anti-noise speaker reaches the ear through a short, band-limited path: it cannot make highs
    imp = np.zeros(64)
    imp[8] = 1.0
    sec = sosfilt(butter(2, 900, fs=SR, output="sos"), imp)
    ref_mic = outside + 0.02 * rng.standard_normal(n)
    r = TD.fxlms(at_ear, ref_mic, sec, taps=160, mu=0.005)
    e = r["e"]
    tail = slice(n - 3 * SR, n)
    bands = []
    for lo, hi in ((50, 200), (200, 500), (500, 1000), (1000, 2000), (2000, 8000)):
        sos = butter(4, [lo, hi], btype="band", fs=SR, output="sos")
        bands.append({"lo": lo, "hi": hi, "atten": db(sosfilt(sos, e[tail])) - db(sosfilt(sos, at_ear[tail]))})
    conv = []
    for k in range(0, n, SR // 4):
        seg = slice(k, k + SR // 4)
        conv.append(db(e[seg]) - db(at_ear[seg]))
    voice = tenor()
    vv = np.r_[voice, np.zeros(max(0, 3 * SR - len(voice)))][: 3 * SR] * 0.25
    off = at_ear[tail] + vv
    on = e[tail] + vv
    m = max(np.max(np.abs(off)), np.max(np.abs(on)))
    c = concat([C(0.4 * off / m), C(0.4 * on / m)], gap=0.8, names=["off", "on"])
    return {"bands": bands, "total": db(e[tail]) - db(at_ear[tail]), "converge": conv, "starts": {"off": float(c.events["off"]), "on": float(c.events["on"])},
            "clips": {"two": save_synth("anc.two", c, detail="an aircraft-cabin drone at the ear with a voice singing over it, the canceller off, then on after it has adapted (simulated filtered-x LMS)", level=None)}}


def compute_beam() -> dict:
    a = tenor()
    b = CH.sing([(m + 7, t0 + 0.25, d) for m, t0, d in tune_notes((1,), base=55)], "soprano", "a")
    b = 0.5 * b / np.max(np.abs(b))
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    pos = np.arange(8) * 0.05 - 0.175
    sig = []
    for x in pos:
        da = 0.0
        tb = x * math.sin(math.radians(40)) / TD.C
        sig.append(a + TD.apply_response(b, lambda f, tb=tb: np.exp(-2j * np.pi * f * tb)))
    single = sig[3]
    beam = TD.delay_and_sum(sig, pos, 0.0)
    rej = db(TD.delay_and_sum([TD.apply_response(b, lambda f, tb=x * math.sin(math.radians(40)) / TD.C: np.exp(-2j * np.pi * f * tb)) for x in pos], pos, 0.0)) - db(b)
    ang = np.linspace(-90, 90, 181)
    pat = {str(fr): [float(TD.array_gain(np.array([fr]), pos, 0.0, a_)[0]) for a_ in ang] for fr in (500, 1000, 2000, 4000)}
    c = concat([C(norm_rms(fade(single))), C(norm_rms(fade(beam)))], gap=0.8, names=["single", "array"])
    return {"angles": ang.tolist(), "pattern": pat, "rejection_db": rej, "positions": pos.tolist(),
            "starts": {"single": float(c.events["single"]), "array": float(c.events["array"])},
            "clips": {"two": save_synth("beam.two", c, detail="two of Part 8's voices, a tenor straight ahead and a soprano 40 degrees to the side: one microphone, then eight in a line 5 cm apart, delayed and summed towards the tenor (simulated)")}}


def compute_tune54() -> dict:
    v = tenor()
    n = len(v)
    pno = piano_chords(n / SR)[:n] * 0.9
    segs, names = [], []
    flat = speaker_H("floor")
    for name in ("omni", "cardioid", "figure-8"):
        y = capture(TD.PATTERNS[name], v, pno)
        segs.append(norm_rms(fade(y)))
        names.append(name)
    card = capture(TD.PATTERNS["cardioid"], v, pno)
    for sp in ("phone", "bookshelf", "floor"):
        y = TD.apply_response(card, speaker_H(sp))
        segs.append(norm_rms(fade(y)))
        names.append(sp)
    keys = ["mic_omni", "mic_cardioid", "mic_fig8", "spk_phone", "spk_bookshelf", "spk_floor"]
    c = concat([C(s_) for s_ in segs], gap=0.6, names=keys)
    d = load("speakers")
    rear = 20 * math.log10(abs(TD.pattern(0.5, math.radians(160))))
    return {"names": keys, "seconds": c.duration, "starts": {k: float(c.events[k]) for k in keys}, "phone_f3": d["f3"]["phone"],
            "floor_f3": d["f3"]["floor"], "cardioid_170": rear,
            "clips": {"variation54": save("tune.variation54", c, detail="the Tune's first phrase sung with a piano behind the singer: picked up by an omni, a cardioid and a figure-8; then the cardioid's version through a phone's speaker, a bookshelf speaker and a floor-stander (all simulated)")}}


def compute_variation() -> dict:
    t = load("tune54")
    return {"part": 54, "title": "through three microphone patterns and three loudspeakers", "seconds": round(t["seconds"], 1),
            "measure": f"a cardioid takes the piano behind it {-t['cardioid_170']:.0f} dB down; the phone's speaker reaches down to {t['phone_f3']:.0f} Hz, the floor-stander to {t['floor_f3']:.0f}",
            "clip": "tune.variation54"}


ITEMS = {"hook": compute_hook, "patterns": compute_patterns, "capture": compute_capture, "proximity": compute_proximity, "noise": compute_noise,
         "hum": compute_hum, "driver": compute_driver, "speakers": compute_speakers, "horn": compute_horn, "crossover": compute_crossover,
         "rotate": compute_rotate, "xover": compute_xover, "anc": compute_anc, "beam": compute_beam, "tune54": compute_tune54, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
