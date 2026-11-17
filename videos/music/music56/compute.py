"""Precompute everything numerical, and every sound, in Part 56 of *Music, Built* ("Recording and Mixing").

    python -m videos.music.music56.compute              # everything missing (a few minutes)
    python -m videos.music.music56.compute --force hook

Numbers are cached in ``.cache/music56/<name>.json``, sounds in ``.cache/music56/audio/``.  The tools are Monochord's
(``explainer/music/monochord/studio.py``, with Part 49's filters and reverberators, Part 50's compressor and Part 55's
head).  The session is ours: Part 8's voice, Part 38's piano, guitar and bass, Part 40's drums, playing the Tune's
first phrases; every microphone, room, console and loudspeaker is simulated.

Items:
    hook        an ear question: the session mixed three ways (close and dry, a wall of sound, a dub): which was the dub?
    history     tracks against years, from the horn to the workstation
    arrays      five stereo pairs: level and time differences, where the images fall, recording angles; three
                instruments on a stage recorded by XY, ORTF and AB, played on loudspeakers (headphones)
    phase       two microphones on one source: comb filters, the 3 : 1 rule; an ear question: a snare's top and bottom
                microphones summed, once with the bottom's polarity wrong
    gain        levels from the air to the converter; a voice recorded too low, right, and too hot
    edit        two takes joined by a butt splice and by a crossfade; crossfade laws on related and unrelated sounds
    pan         the four pan laws, in stereo and in mono
    masking     a masking map of the session's tracks, before and after carving; heard
    dynamics    a vocal compressor, and drums with parallel compression
    depth       a voice placed near, in the middle, and far; a guitar widened by delay, and its comb in mono
    monitor     the mix on studio monitors and on a phone's loudspeaker
    automix     an ear question: our mix against an automatic one; their settings
    tune56      Variation 56: the session's first three phrases mixed three ways
    variation   the Variations ledger, row 56
"""

from __future__ import annotations

import math

import numpy as np
from scipy.signal import fftconvolve

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import effects as E
from explainer.music.monochord import space as SP
from explainer.music.monochord import studio as S
from explainer.music.monochord import tune as T
from explainer.music.monochord import transducer as TR
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.partkit import saver, signoff
from videos.music.music38 import compute as P38
from videos.music.music40 import compute as P40

CACHE = Cache("music56")
CLIPS = ClipStore("music56")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
MAJOR = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
BPM = 100.0
BEAT = 60.0 / BPM
ROOT = {"C": 0, "F": 5, "G": 7}
CHORDS = {0: "CCFC", 1: "FCGC", 2: "CFCG", 3: "CFCG", 4: "CCFC", 5: "FCGC"}   # a chord every two beats, phrase by phrase
TRACKS = ["vox", "piano", "guitar", "bass", "kick", "snare", "hat"]
STAGE = {"vox": 0.0, "piano": 35.0, "guitar": -35.0, "bass": 10.0, "kick": 0.0, "snare": 5.0, "hat": -15.0}   # degrees, + left


def C(y) -> Clip:
    return Clip(np.asarray(y, float), SR)


def norm_rms(y, target=0.1):
    return y * target / (np.sqrt(np.mean(np.asarray(y) ** 2)) + 1e-12)


def norm_lufs(y, target=-23.0):
    return np.asarray(y, float) * 10 ** ((target - S.lufs(y)) / 20)


def fade(y, a=0.005, r=0.08):
    y = np.array(y, float)
    ka, kr = max(int(a * SR), 1), max(int(r * SR), 1)
    y[:ka] *= np.linspace(0, 1, ka)[:, None] if y.ndim == 2 else np.linspace(0, 1, ka)
    y[len(y) - kr:] *= np.linspace(1, 0, kr)[:, None] if y.ndim == 2 else np.linspace(1, 0, kr)
    return y


def headphones(st):
    """A stereo mix heard on two loudspeakers at +-30 degrees, rendered round Part 55's spherical head."""
    st = np.asarray(st, float)
    hl, hr = SP.ear_filters(math.radians(-30), n=256)
    gl, gr = SP.ear_filters(math.radians(30), n=256)
    L = fftconvolve(st[:, 0], hl) + fftconvolve(st[:, 1], gl)
    R = fftconvolve(st[:, 0], hr) + fftconvolve(st[:, 1], gr)
    return np.stack([L, R], axis=1)


# ---------------------------------------------------------------------------------------------- the session
_S: dict = {}


def tune_notes(phrases, base=60, beat=BEAT):
    return [(base + MAJOR[e["degree"]], e["t"], e["dur"]) for e in T.events(beat, list(phrases))]


def chord_tones(sym):
    r = ROOT[sym]
    return [r, r + 4, r + 7]


def session(phrases=(0, 1)) -> dict:
    """The multitrack: each instrument on its own track, as close microphones would hear it (dry), plus a pair of room
    microphones (ORTF) hearing the whole band in a 1.2 s room."""
    key = tuple(phrases)
    if key in _S:
        return _S[key]
    beats = 8 * len(phrases)
    n = int((beats * BEAT + 1.6) * SR)
    dur = n / SR
    parts = {k: [] for k in TRACKS}
    v = CH.sing(tune_notes(phrases), "soprano", "a", seed=1)
    v2 = CH.sing(tune_notes(phrases), "soprano", "a", seed=7, vibrato=5.1)
    syms = "".join(CHORDS[p] for p in phrases)
    for i, sym in enumerate(syms):
        t0 = 2 * i * BEAT
        tones = chord_tones(sym)
        voicing = sorted(55 + (p - 55) % 12 for p in tones) + [67 + (tones[0] - 67) % 12]
        for m in voicing:
            parts["piano"].append((P38.arr(P38.piano(m, 2 * BEAT * 0.95, 0.7)), t0, -4.0))
        arp = [48 + tones[0], 48 + tones[1] + 12 if tones[1] + 48 < 52 else 48 + tones[1], 48 + tones[2], 60 + tones[0]]
        for k in range(4):
            parts["guitar"].append((P38.arr(P38.guitar(arp[k % 4] + 12, BEAT * 0.45)), t0 + k * BEAT / 2, -4.0))
        rt = 36 + ROOT[sym] if ROOT[sym] < 5 else 24 + ROOT[sym]
        parts["bass"].append((P38.arr(P38.bass(rt, BEAT * 0.9)), t0, -2.0))
        parts["bass"].append((P38.arr(P38.bass(rt + 7 if rt + 7 < 48 else rt - 5, BEAT * 0.8)), t0 + BEAT, -4.0))
    for b in range(beats):
        t0 = b * BEAT
        if b % 2 == 0:
            parts["kick"].append((P38.arr(P40.kick()), t0, 0.0))
        else:
            parts["snare"].append((P38.arr(P40.snare(b % 3)), t0, 0.0))
        for k in range(2):
            parts["hat"].append((P38.arr(P40.hat()), t0 + k * BEAT / 2, -2.0 if k == 0 else -6.0))
    tr = {"vox": np.r_[v, np.zeros(max(0, n - len(v)))][:n], "vox2": np.r_[v2, np.zeros(max(0, n - len(v2)))][:n]}
    for k in ("piano", "guitar", "bass", "kick", "snare", "hat"):
        tr[k] = mix(parts[k], duration=dur).y[:n]
    lv = {"vox": -20.0, "vox2": -20.0, "piano": -24.0, "guitar": -26.0, "bass": -22.0, "kick": -22.0, "snare": -24.0, "hat": -32.0}
    for k in tr:
        tr[k] = norm_lufs(tr[k], lv[k])
    room = np.zeros((n, 2))
    for k in TRACKS:
        room += S.pair_render(tr[k], "ORTF", STAGE[k])[:n]
    tail = SP.noise_tail(1.2, 1.6, seed=5, stereo=True, start=0.012)
    wet = np.stack([fftconvolve(room[:, 0], tail[:, 0])[:n], fftconvolve(room[:, 1], tail[:, 1])[:n]], axis=1)
    tr["room"] = norm_lufs(0.5 * room + 1.6 * wet, -22.0)
    _S[key] = {"tracks": tr, "n": n, "beats": beats, "syms": syms}
    return _S[key]


_IR: dict = {}


def chamber(T60=2.4):
    if ("chamber", T60) not in _IR:
        _IR[("chamber", T60)] = SP.noise_tail(T60, min(1.3 * T60, 4.0), seed=11, stereo=True, start=0.02, dark=0.6)
    return _IR[("chamber", T60)]


def spring():
    if "spring" not in _IR:
        h = E.spring_ir(SR, 2.0)
        _IR["spring"] = np.stack([h, np.r_[np.zeros(37), h[:-37]]], axis=1) / math.sqrt(np.sum(h ** 2))
    return _IR["spring"]


CARVE = {"vox": (1.0, 0.0, 110, [("peak", 3000, 1.0, 2.0)]), "piano": (0.0, -0.5, 180, [("peak", 900, 1.2, -4.0), ("peak", 3000, 1.0, -2.0)]),
         "guitar": (-1.0, 0.55, 300, [("peak", 2000, 1.0, 2.0)]), "bass": (0.0, 0.0, None, [("peak", 60, 1.0, -4.0), ("peak", 800, 1.0, -4.0)]),
         "kick": (0.0, 0.0, None, [("peak", 130, 1.2, -6.0), ("peak", 300, 1.5, -5.0)]), "snare": (-1.0, 0.05, 150, [("peak", 400, 1.0, -3.0)]),
         "hat": (-2.0, 0.3, 600, [])}


def carved_channels(tr):
    return [S.Channel(k, tr[k], CARVE[k][0], CARVE[k][1], hpf=CARVE[k][2], eq=list(CARVE[k][3])) for k in TRACKS]


def mix_dry(tr, n):
    ch = carved_channels(tr)
    ch[0].comp = {"threshold": -26, "ratio": 3, "attack_ms": 5, "release_ms": 120}
    ch.append(S.Channel("room", tr["room"], -8.0, 0.0))
    return S.mix(ch, length=n)


def mix_wall(tr, n):
    d = lambda y, ms: S.frac_delay(y, ms * SR / 1000)                       # noqa: E731
    ch = [S.Channel("vox", tr["vox"], 0.0, 0.0, hpf=120, comp={"threshold": -28, "ratio": 4}, sends={"chamber": -2.0}),
          S.Channel("vox2", d(tr["vox2"], 18), -3.0, 0.0, hpf=120, sends={"chamber": -2.0})]
    for i, (ms, g) in enumerate([(0, 0.0), (13, -1.5), (27, -2.5)]):
        ch.append(S.Channel(f"piano{i}", d(tr["piano"], ms), g - 2.0, 0.0, hpf=90, sends={"chamber": 0.0}))
        ch.append(S.Channel(f"guitar{i}", d(tr["guitar"], ms + 7), g - 3.0, 0.0, hpf=150, sends={"chamber": 0.0}))
    ch += [S.Channel("bass", tr["bass"], -1.0, 0.0, sends={"chamber": -12.0}), S.Channel("kick", tr["kick"], -2.0, 0.0, sends={"chamber": -6.0}),
           S.Channel("snare", tr["snare"], 0.0, 0.0, sends={"chamber": 2.0}), S.Channel("hat", tr["hat"], -6.0, 0.0, sends={"chamber": -4.0}),
           S.Channel("room", tr["room"], 0.0, 0.0, width=0.0)]
    comp = S.bus_compressor(threshold=-24.0, ratio=4.0, attack_ms=0.2, release_ms=300.0)

    def master(x):                                    # heavy bus compression, then tape-like saturation
        y = comp(x)
        return np.tanh(2.0 * y / np.max(np.abs(y)))
    return S.mix(ch, buses={"chamber": S.reverb_bus(chamber(2.4) * 0.6)}, master=master, length=n)


def mix_dub(tr, n, beats):
    bar = 4 * BEAT
    end = beats * BEAT

    def vox_mute(t):
        return ((t < 2 * BEAT) | ((t > 8 * BEAT) & (t < 9.5 * BEAT))).astype(float)

    def piano_mute(t):
        return (((t // BEAT) % 4 == 1) & (t % BEAT < 0.25)).astype(float)

    def drum_drop(t):
        return np.where((t > end - bar) & (t < end - bar / 2), 0.0, 1.0)

    ch = [S.Channel("vox", tr["vox"], -1.0, 0.0, hpf=200, eq=[("peak", 1500, 1.2, 3.0)], mute=vox_mute, sends={"echo": 0.0}),
          S.Channel("piano", tr["piano"], -2.0, -0.2, hpf=300, mute=piano_mute, sends={"echo": -2.0, "spring": -4.0}),
          S.Channel("bass", tr["bass"], 5.0, 0.0, eq=[("lowshelf", 120, 0.7, 5.0), ("lowpass", 900, 0.7, 0.0)]),
          S.Channel("kick", tr["kick"], 2.0, 0.0, mute=drum_drop), S.Channel("snare", tr["snare"], 0.0, 0.0, mute=drum_drop, sends={"spring": 2.0, "echo": -8.0}),
          S.Channel("hat", tr["hat"], -5.0, 0.35, hpf=600, mute=drum_drop)]
    return S.mix(ch, buses={"echo": S.echo_bus(0.75 * BEAT, 0.55, 2200.0), "spring": S.reverb_bus(spring() * 0.5)}, length=n + int(2.0 * SR))


def three_mixes(phrases):
    s = session(phrases)
    tr, n = s["tracks"], s["n"]
    out = {"dry": mix_dry(tr, n)["y"], "wall": mix_wall(tr, n)["y"], "dub": mix_dub(tr, n, s["beats"])["y"]}
    return {k: norm_lufs(fade(v), -20.0) for k, v in out.items()}


# ---------------------------------------------------------------------------------------------- items
def measures(y) -> dict:
    y = np.asarray(y, float)
    from explainer.music.monochord import dynamics as D
    return {"correlation": S.correlation(y[:, 0], y[:, 1]), "crest_db": D.crest_db(y.mean(axis=1)), "lufs": S.lufs(y),
            "seconds": len(y) / SR}


def compute_hook() -> dict:
    m = three_mixes((0, 1))
    order = ["wall", "dub", "dry"]
    c = concat([C(headphones(m[k])) for k in order], gap=0.9, names=["first", "second", "third"])
    return {"answer": "second", "order": order, "measures": {k: measures(m[k]) for k in order},
            "starts": {k: float(c.events[k]) for k in ("first", "second", "third")},
            "clips": {"three": save("hook.three", c, detail="headphones: the Tune's first two phrases played by our session band (Part 8's voice, Part 38's piano, guitar and bass, Part 40's drums) and mixed three ways: a wall of sound, a dub, close and dry", needs="headphones")}}


HISTORY = [(1877, 1, "Edison's tinfoil: one horn, one groove"), (1925, 1, "electrical recording: a microphone and an amplifier"),
           (1948, 1, "magnetic tape (Ampex 200): editing with a razor blade"), (1957, 8, "Les Paul's eight-track Ampex"),
           (1967, 4, "Sgt. Pepper: two four-track machines, bounced"), (1974, 24, "24-track two-inch tape"),
           (1982, 24, "Sony's PCM-3324: 24 digital tracks"), (1991, 4, "Pro Tools: four tracks in a computer"),
           (2005, 128, "the workstation: as many tracks as the computer can hold"), (2020, 256, "sessions of hundreds of tracks")]


def compute_history() -> dict:
    return {"rows": [{"year": y, "tracks": t, "what": w} for y, t, w in HISTORY]}


def compute_arrays() -> dict:
    th = np.linspace(-90, 90, 181)
    out = {"theta": th.tolist(), "pairs": {}}
    for k in S.PAIRS:
        c = S.pair_cues(k, th)
        out["pairs"][k] = {"dL": c["dL"].tolist(), "dt": c["dt"].tolist(), "pos": S.image_position(c["dL"], c["dt"]).tolist(),
                           "sra": S.recording_angle(k), **S.PAIRS[k]}
    s = session((0,))
    tr, n = s["tracks"], s["n"]
    stage = {"piano": 40.0, "vox": 0.0, "guitar": -40.0}
    order = ["XY", "ORTF", "AB"]
    segs = []
    for k in order:
        y = sum(S.pair_render(tr[name], k, a)[:n] for name, a in stage.items())
        segs.append(C(headphones(y)))
    c = concat(segs, gap=0.8, names=order)
    out["stage"] = stage
    out["stage_pos"] = {k: {name: float(S.image_position(*[float(v) for v in (S.pair_cues(k, a)["dL"], S.pair_cues(k, a)["dt"])])) for name, a in stage.items()} for k in order}
    out["order"] = order
    out["starts"] = {k: float(c.events[k]) for k in order}
    out["clips"] = {"three": save("arrays.three", c, detail="headphones: our piano 40 degrees left, the voice in the centre and the guitar 40 degrees right, recorded by an XY pair, an ORTF pair and a spaced AB pair (all simulated), played on two loudspeakers rendered round a spherical head", needs="headphones")}
    return out


def snare_mics():
    """A snare's top microphone (the head: body and crack) and bottom microphone (the wires: brighter, and pushed the
    other way, so inverted), as one hit pattern."""
    from scipy.signal import butter, sosfilt
    s = session((0,))
    top = s["tracks"]["snare"]
    wires = sosfilt(butter(2, 1800, btype="high", fs=SR, output="sos"), top)
    bottom = -0.9 * S.frac_delay(0.6 * top + 1.2 * wires, 0.0004 * SR)
    return top, bottom


def lowband_db(y, lo=120.0, hi=400.0):
    P = np.abs(np.fft.rfft(y)) ** 2
    f = np.fft.rfftfreq(len(y), 1 / SR)
    return float(10 * np.log10(P[(f >= lo) & (f < hi)].sum() + 1e-20))


def compute_phase() -> dict:
    f = np.geomspace(20, 20000, 800)
    tau = 2.0 / C_AIR
    combs = {"equal": S.comb_db(f, tau, 1.0).tolist(), "three_to_one": S.comb_db(f, tau, 1 / 3).tolist()}
    top, bottom = snare_mics()
    right = top - bottom                     # the bottom microphone's polarity flipped back
    wrong = top + bottom
    loss = lowband_db(right) - lowband_db(wrong)
    a, b = norm_lufs(right, -22.0), norm_lufs(wrong, -22.0)
    c = concat([C(fade(a)), C(fade(b))], gap=0.8, names=["first", "second"])
    return {"f": f.tolist(), "combs": combs, "tau_ms": 1000 * tau, "notch_hz": 1 / (2 * tau), "extremes": S.comb_extremes(1 / 3),
            "ratio_db": 20 * math.log10(3), "low_loss_db": loss, "answer": "second",
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("phase.two", c, detail="our snare's top and bottom microphones summed (simulated), twice: once with the bottom microphone's polarity flipped back, once left as recorded")}}


C_AIR = 343.0


def compute_gain() -> dict:
    rng = np.random.default_rng(4)
    settings = {"low": 0.0, "right": 28.0, "hot": 52.0}
    rows = {k: S.chain(spl=104.0, sens_mv=12.0, gain_db=g, adc_noise_dbfs=-98.0) for k, g in settings.items()}
    v = session((0,))["tracks"]["vox"]
    v = v / np.max(np.abs(v))
    segs = []
    for k in ("low", "right", "hot"):
        r = rows[k]
        pk = 10 ** (r["peak_dbfs"] / 20)
        noise = rng.standard_normal(len(v)) * 10 ** (r["noise_dbfs"] / 20) * math.sqrt(0.5)
        x = v * pk + noise
        x = np.clip(x, -1.0, 1.0)
        x = S.quantize(x, 16)
        segs.append(C(fade(norm_lufs(x / np.max(np.abs(x)), -22.0))))
    c = concat(segs, gap=0.8, names=["low", "right", "hot"])
    return {"settings": settings, "rows": rows, "spl": 104.0, "sens_mv": 12.0,
            "starts": {k: float(c.events[k]) for k in ("low", "right", "hot")},
            "clips": {"three": save("gain.three", c, detail="Part 8's voice peaking at 104 dB SPL into a simulated condenser microphone and preamplifier at three gains (0, 28 and 52 dB) and a 16-bit converter, each then brought to the same loudness")}}


def compute_edit() -> dict:
    t = np.linspace(0, 1, 201)
    laws = {"linear": S.fade_pair(201, "linear"), "power": S.fade_pair(201, "power")}
    curves = {}
    for k, (fo, fi) in laws.items():
        curves[k] = {"related": (20 * np.log10(fo + fi)).tolist(), "unrelated": (10 * np.log10(fo ** 2 + fi ** 2)).tolist()}
    a = CH.sing(tune_notes((0,)), "soprano", "a", seed=1)
    b = CH.sing(tune_notes((0,)), "soprano", "a", seed=3, vibrato=5.9, depth=0.006)
    cut = int(2.3 * BEAT * SR)
    n = min(len(a), len(b))
    butt = np.r_[a[:cut], b[cut:n]]
    xf = S.crossfade(a[:cut + 240], b[cut - 240:n], 480, "power")
    jump = float(abs(a[cut - 1] - b[cut]) / np.max(np.abs(a)))
    c = concat([C(fade(norm_lufs(butt, -22.0))), C(fade(norm_lufs(xf, -22.0)))], gap=0.8, names=["butt", "crossfade"])
    return {"t": t.tolist(), "curves": curves, "cut_s": cut / SR, "jump": jump, "xfade_ms": 10.0,
            "starts": {"butt": float(c.events["butt"]), "crossfade": float(c.events["crossfade"])},
            "clips": {"two": save("edit.two", c, detail="two takes of the Tune's first phrase by Part 8's voice joined in the middle of a note: a butt splice, then a 10 ms equal-power crossfade")}}


def compute_pan() -> dict:
    p = np.linspace(-1, 1, 101)
    out = {"p": p.tolist(), "laws": {}}
    hard = 0.5                                 # a hard-panned source's mono sum, (1 + 0) / 2
    for law in (0.0, -3.0, -4.5, -6.0):
        gL, gR = S.pan_gains(p, law)
        out["laws"][str(law)] = {"gL": gL.tolist(), "gR": gR.tolist(), "stereo_db": (10 * np.log10(gL ** 2 + gR ** 2)).tolist(),
                                 "mono_db": (20 * np.log10((gL + gR) / 2 / hard)).tolist(), "centre_db": float(20 * np.log10(gL[50])),
                                 "centre_stereo_db": float(10 * np.log10(gL[50] ** 2 + gR[50] ** 2)), "centre_mono_db": float(20 * np.log10((gL[50] + gR[50]) / 2 / hard))}
    return out


def rough_and_carved(phrases=(0, 1)):
    s = session(phrases)
    tr, n = s["tracks"], s["n"]
    rough = [S.Channel(k, tr[k], 0.0, 0.0) for k in TRACKS]
    return S.mix(rough, length=n), S.mix(carved_channels(tr), length=n)


def compute_masking() -> dict:
    r, c_ = rough_and_carved()
    mr = S.masking_map({k: r["stems"][k] for k in TRACKS})
    mc = S.masking_map({k: c_["stems"][k] for k in TRACKS})
    c = concat([C(fade(norm_lufs(r["y"], -20.0))), C(fade(norm_lufs(c_["y"], -20.0)))], gap=0.8, names=["rough", "carved"])
    centres = np.sqrt(mr["edges"][:-1] * mr["edges"][1:])
    return {"tracks": TRACKS, "centres": centres.tolist(), "rough": {k: v.tolist() for k, v in mr["bands"].items()}, "carved": {k: v.tolist() for k, v in mc["bands"].items()},
            "overall": {"rough": mr["overall"], "carved": mc["overall"]},
            "starts": {"rough": float(c.events["rough"]), "carved": float(c.events["carved"])},
            "clips": {"two": save("masking.two", c, detail="our session's seven tracks: a rough mix (every fader at unity, every pan in the centre, no equalization), then carved (panned, high-passed, with cuts where the tracks collide)")}}


def short_spread(y, win_ms=50.0):
    from explainer.music.monochord import dynamics as D
    y = np.asarray(y, float)
    if y.ndim == 2:
        y = y.mean(axis=1)
    L = D.short_term_levels(y, SR, win_ms)
    L = L[L > np.max(L) - 40]
    return float(np.percentile(L, 95) - np.percentile(L, 10))


def compute_dynamics() -> dict:
    from explainer.music.monochord import dynamics as D
    s = session((0, 1))
    tr = s["tracks"]
    v = tr["vox"]
    comp = D.compressor(v, SR, threshold=-26.0, ratio=4.0, attack_ms=5.0, release_ms=120.0)
    vox = {"spread_before": short_spread(v), "spread_after": short_spread(comp["y"]), "gr_max": float(comp["gr_db"].max()),
           "gr_mean": float(comp["gr_db"][np.abs(v) > 1e-4].mean())}
    drums = tr["kick"] + tr["snare"] + tr["hat"]
    smash = D.compressor(drums, SR, threshold=-40.0, ratio=10.0, attack_ms=0.05, release_ms=60.0, makeup=0.0)["y"]
    smash = smash * np.max(np.abs(drums)) / np.max(np.abs(smash))
    par = drums + 10 ** (-6 / 20) * smash
    out = {"vox": vox, "drums": {"crest_dry": D.crest_db(drums), "crest_parallel": D.crest_db(par),
                                 "spread_dry": short_spread(drums), "spread_parallel": short_spread(par)}}
    k = int(4.8 * SR)
    c = concat([C(fade(norm_lufs(drums[:k], -22.0))), C(fade(norm_lufs(par[:k], -22.0)))], gap=0.8, names=["dry", "parallel"])
    out["starts"] = {"dry": float(c.events["dry"]), "parallel": float(c.events["parallel"])}
    out["env"] = {"t": (np.arange(0, k, 480) / SR).tolist(), "dry": D.short_term_levels(drums[:k], SR, 10.0)[: len(range(0, k, 480))].tolist(),
                  "parallel": D.short_term_levels(par[:k], SR, 10.0)[: len(range(0, k, 480))].tolist()}
    out["clips"] = {"two": save("dynamics.two", c, detail="our drums (Part 40's kick, snare and hi-hat) as recorded, then with a heavily compressed copy blended in underneath (parallel compression)")}
    return out


def compute_depth() -> dict:
    s = session((0,))
    tr, n = s["tracks"], s["n"]
    ir = chamber(1.6) * 0.5
    places = {"near": (0.0, -30.0, 0.0, 0.0), "middle": (-5.0, -8.0, -4.0, 12.0), "far": (-10.0, 0.0, -9.0, 25.0)}   # gain, send dB, treble shelf dB, pre-delay ms
    segs, dr = [], {}
    for k, (g, send, shelf, pre) in places.items():
        v = S.frac_delay(tr["vox"], pre * SR / 1000) if pre else tr["vox"]
        ch = [S.Channel("vox", tr["vox"], g, 0.0, eq=[("highshelf", 5000, 0.7, shelf)], sends={"verb": send}),
              S.Channel("piano", tr["piano"], -4.0, -0.5, sends={"verb": -10.0}), S.Channel("bass", tr["bass"], -3.0, 0.0),
              S.Channel("kick", tr["kick"], -4.0, 0.0), S.Channel("snare", tr["snare"], -5.0, 0.05, sends={"verb": -10.0}), S.Channel("hat", tr["hat"], -6.0, 0.3)]
        bus = S.reverb_bus(ir)
        m = S.mix(ch, buses={"verb": lambda x, pre=pre: bus(np.r_[np.zeros((int(pre * SR / 1000), 2)), x][: len(x)])}, length=n + int(1.0 * SR))
        direct = np.sum(m["stems"]["vox"] ** 2)
        wet = 10 ** (send / 10) * np.sum(bus(m["stems"]["vox"]) ** 2)
        dr[k] = float(10 * np.log10(direct / (wet + 1e-20)))
        segs.append(C(fade(headphones(norm_lufs(m["y"], -20.0)))))
        del v
    c = concat(segs, gap=0.8, names=list(places))
    g = tr["guitar"]
    w = S.haas(g, 12.0)
    mono = w.mean(axis=1)
    width = {"correlation": S.correlation(w[:, 0], w[:, 1]), "mono_loss_db": S.mono_loss_db(w[:, 0], w[:, 1]), "notch_hz": 1000 / (2 * 12.0),
             "spacing_hz": 1000 / 12.0}
    c2 = concat([C(fade(headphones(norm_lufs(w, -22.0)))), C(fade(headphones(norm_lufs(np.stack([mono, mono], axis=1), -22.0))))], gap=0.8, names=["wide", "mono"])
    return {"places": {k: {"gain": v[0], "send": v[1], "shelf": v[2], "predelay_ms": v[3]} for k, v in places.items()}, "dr_db": dr, "width": width,
            "starts": {k: float(c.events[k]) for k in places}, "starts_width": {"wide": float(c2.events["wide"]), "mono": float(c2.events["mono"])},
            "clips": {"three": save("depth.three", c, detail="headphones: our voice placed near, in the middle and far behind the same band, by level, treble, reverberation and pre-delay", needs="headphones"),
                      "width": save("depth.width", c2, detail="headphones: our guitar widened by a 12 ms delay between the channels, then the same summed to mono", needs="headphones")}}


def compute_monitor() -> dict:
    from videos.music.music54 import compute as P54
    m = mix_dry(session((0, 1))["tracks"], session((0, 1))["n"])["y"]
    H = P54.speaker_H("phone")
    ph = np.stack([TR.apply_response(m[:, 0], H), TR.apply_response(m[:, 1], H)], axis=1)[: len(m)]
    bass = session((0, 1))["tracks"]["bass"]
    P = np.abs(np.fft.rfft(bass)) ** 2
    f = np.fft.rfftfreq(len(bass), 1 / SR)
    above = float(P[f > 844].sum() / P.sum())
    c = concat([C(fade(headphones(norm_lufs(m, -20.0)))), C(fade(headphones(norm_lufs(ph, -20.0))))], gap=0.8, names=["monitors", "phone"])
    ff = np.geomspace(20, 20000, 300)
    return {"f": ff.tolist(), "phone_db": (20 * np.log10(np.abs(H(ff)) + 1e-9)).tolist(), "bass_above_844": above,
            "starts": {"monitors": float(c.events["monitors"]), "phone": float(c.events["phone"])},
            "clips": {"two": save("monitor.two", c, detail="headphones: our close-and-dry mix on full-range monitors, then on Part 54's simulated phone loudspeaker", needs="headphones")}}


def compute_automix() -> dict:
    s = session((0, 1))
    tr, n = s["tracks"], s["n"]
    am = S.automix({k: tr[k] for k in TRACKS}, lead="vox")
    mach = S.mix(am["channels"], length=n)["y"]
    hand = mix_dry(tr, n)["y"]
    hand_ch = {k: (CARVE[k][0], CARVE[k][1]) for k in TRACKS}
    machine = {c_.name: (round(c_.gain_db, 2), round(c_.pan, 2)) for c_ in am["channels"]}
    mh = S.masking_map({k: v for k, v in mix_dry(tr, n)["stems"].items() if k in TRACKS})
    mm = S.masking_map({k: v for k, v in S.mix(am["channels"], length=n)["stems"].items()})
    c = concat([C(fade(headphones(norm_lufs(hand, -20.0)))), C(fade(headphones(norm_lufs(mach, -20.0))))], gap=0.8, names=["first", "second"])
    return {"answer": "second", "hand": hand_ch, "machine": machine, "loudness": am["loudness"], "centroid": am["centroid"], "low_share": am["low_share"],
            "masked": {"hand": mh["overall"], "machine": mm["overall"]},
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("automix.two", c, detail="headphones: our session mixed by hand (close and dry), then by Monochord's rule-based automatic mixer", needs="headphones")}}


def compute_tune56() -> dict:
    m = three_mixes((0, 1, 2))
    order = ["dry", "wall", "dub"]
    c = concat([C(headphones(m[k])) for k in order], gap=0.9, names=order)
    me = {k: measures(m[k]) for k in order}
    return {"order": order, "measures": me, "echo_s": 0.75 * BEAT, "seconds": c.duration, "starts": {k: float(c.events[k]) for k in order},
            "clips": {"variation56": save("tune.variation56", c, detail="headphones: the Tune's first three phrases by our session band, mixed three ways: close and dry, a wall of sound, a dub", needs="headphones")}}


def compute_variation() -> dict:
    t = load("tune56")
    me = t["measures"]
    return {"part": 56, "title": "the session mixed three ways", "seconds": round(t["seconds"], 1),
            "measure": f"one session, three mixes: crest factor {me['dry']['crest_db']:.0f} dB dry, {me['wall']['crest_db']:.0f} in the wall; the dub's echo every {t['echo_s']:.2f} s",
            "clip": "tune.variation56"}


def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation56", 56)


ITEMS = {"hook": compute_hook, "history": compute_history, "arrays": compute_arrays, "phase": compute_phase, "gain": compute_gain,
         "edit": compute_edit, "pan": compute_pan, "masking": compute_masking, "dynamics": compute_dynamics, "depth": compute_depth,
         "monitor": compute_monitor, "automix": compute_automix, "tune56": compute_tune56, "variation": compute_variation,
         "signoff": compute_signoff}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
