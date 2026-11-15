"""Precompute everything numerical, and every sound, in Part 57 of *Music, Built* ("Mastering and Loudness").

    python -m videos.music.music57.compute              # everything missing (a few minutes)
    python -m videos.music.music57.compute --force hook

Numbers are cached in ``.cache/music57/<name>.json``, sounds in ``.cache/music57/audio/``.  The tools are Monochord's
(``explainer/music/monochord/master.py`` and the series' own meter, ``loudness.py``).  The music is Part 56's session,
mixed close and dry, and earlier parts' Variations; every master, meter, codec-free delivery and record is simulated.

Items:
    hook        an ear question: the same mix mastered gently and for the loudness war, played at the same loudness:
                which was limited harder?
    meters      K-weighting, a VU and a peak meter on a drum hit, gated block loudness, and our meter against ffmpeg's;
                a low and a high tone at the same RMS, heard
    truepeak    a sine whose samples miss its peaks; a clipped master's inter-sample overs
    limiter     clipping against look-ahead limiting at the same loudness, heard
    war         one mix mastered at six loudness targets: true peak, PLR, LRA, crest factor, flat-topped samples; three
                heard as mastered
    norm        the same three normalized to -14 LUFS, as a streaming service would play them (an ear question)
    matched     an ear question: the same master twice, the second 1 dB louder
    dither      a fading piano note at 8 bits: rounded, dithered, and dithered with noise shaping
    vinyl       the RIAA curve, groove excursions, and a record played without its de-emphasis
    chain       our mastering chain, stage by stage
    series      this series' own levels, measured
    tune57      Variation 57: an album side of Variations, then one war-mastered beside itself, level-matched
    variation   the Variations ledger, row 57
"""

from __future__ import annotations

import importlib
import json
import math
import subprocess
import tempfile
from pathlib import Path

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, QUIET_LEVEL, SR, Clip, ClipStore, concat
from explainer.music.monochord import loudness as LN
from explainer.music.monochord import master as MS
from explainer.music.monochord.partkit import saver
from videos.music.music38 import compute as P38
from videos.music.music56 import compute as P56

CACHE = Cache("music57")
CLIPS = ClipStore("music57")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
TARGETS = [-20.0, -17.0, -14.0, -11.0, -9.0, -7.0]


def C(y) -> Clip:
    return Clip(np.asarray(y, float), SR)


def fade(y, a=0.005, r=0.08):
    y = np.array(y, float)
    ka, kr = max(int(a * SR), 1), max(int(r * SR), 1)
    y[:ka] *= np.linspace(0, 1, ka)[:, None] if y.ndim == 2 else np.linspace(0, 1, ka)
    y[len(y) - kr:] *= np.linspace(1, 0, kr)[:, None] if y.ndim == 2 else np.linspace(1, 0, kr)
    return y


def to_lufs(y, target):
    return np.asarray(y, float) * 10 ** ((target - MS.lufs(y)) / 20)


_M: dict = {}


def the_mix(phrases=(0, 1, 2)):
    """Part 56's session, mixed close and dry, at -20 LUFS: the material every master starts from."""
    if phrases not in _M:
        s = P56.session(phrases)
        _M[phrases] = to_lufs(P56.mix_dry(s["tracks"], s["n"])["y"], -20.0)
    return _M[phrases]


_MS: dict = {}


def mastered(target, phrases=(0, 1, 2)):
    key = (target, phrases)
    if key not in _MS:
        _MS[key] = MS.master(the_mix(phrases), target)
    return _MS[key]


def flat_fraction(y, ceiling_db=-1.0):
    c = 10 ** (ceiling_db / 20)
    return float(np.mean(np.max(np.abs(np.asarray(y)), axis=1) > c * 10 ** (-0.1 / 20)))


def envelope(y, n=400):
    m = np.max(np.abs(np.asarray(y)), axis=1)
    k = len(m) // n
    return np.max(m[: k * n].reshape(n, k), axis=1).tolist()


# ---------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    gentle = mastered(-14.0)
    war = mastered(-7.0)
    a, b = to_lufs(gentle["y"], -18.0), to_lufs(war["y"], -18.0)
    c = concat([C(fade(a)), C(fade(b))], gap=0.9, names=["first", "second"])
    return {"answer": "second", "gentle": {"lufs": gentle["lufs"], "tp": gentle["true_peak"], "plr": MS.plr(gentle["y"]), "gr_max": float(-gentle["gain_db"].min())},
            "war": {"lufs": war["lufs"], "tp": war["true_peak"], "plr": MS.plr(war["y"]), "gr_max": float(-war["gain_db"].min())},
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("hook.two", c, detail="Part 56's session mixed close and dry, then mastered twice by Monochord's chain: gently, to -14 LUFS, and for the loudness war, to -7 LUFS; both then played at the same loudness", needs="headphones")}}


def ffmpeg_measure(y) -> dict:
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "x.wav"
        C(MS.stereo(y)).write(p)
        err = subprocess.run(["ffmpeg", "-nostats", "-i", str(p), "-af", "ebur128=peak=true", "-f", "null", "-"], text=True, capture_output=True).stderr
    s = err[err.rindex("Summary:"):]
    import re
    return {"I": float(re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1)), "TP": float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", s).group(1)),
            "LRA": float(re.search(r"LRA:\s+(-?[\d.]+) LU", s).group(1))}


def compute_meters() -> dict:
    f = np.geomspace(20, 20000, 400)
    k = MS.k_response(f)
    # a mix with a quiet first phrase: the gates at work
    m = the_mix((0, 1))
    half = int(len(m) * 0.45)
    quiet = m.copy()
    quiet[:half] *= 10 ** (-14 / 20)
    quiet = np.r_[np.zeros((int(1.5 * SR), 2)), quiet]
    b = MS.blocks(quiet)
    # VU and PPM on a snare hit
    sn = P56.session((0,))["tracks"]["snare"][: int(1.2 * SR)]
    vu, pp = MS.vu(sn), MS.ppm(sn)
    step = 240
    # our meter against ffmpeg's
    checks = []
    for name, y in (("the mix", m), ("a gentle master", mastered(-14.0)["y"]), ("a war master", mastered(-7.0)["y"]), ("quiet start", quiet)):
        ff = ffmpeg_measure(y)
        checks.append({"name": name, "ours_I": MS.lufs(y), "ffmpeg_I": ff["I"], "ours_TP": MS.true_peak_db(y), "ffmpeg_TP": ff["TP"],
                       "ours_LRA": MS.loudness_range(y), "ffmpeg_LRA": ff["LRA"]})
    # two tones at the same RMS
    t = np.arange(int(2.5 * SR)) / SR
    env = np.clip(t / 0.05, 0, 1) * np.clip((2.5 - t) / 0.1, 0, 1)
    lo = 0.1 * math.sqrt(2) * np.sin(2 * np.pi * 60 * t) * env
    hi = 0.1 * math.sqrt(2) * np.sin(2 * np.pi * 2000 * t) * env
    c = concat([C(lo), C(hi)], gap=0.6, names=["low", "high"])
    return {"f": f.tolist(), "k_db": k.tolist(), "blocks": {"t": b["t"], "lk": np.clip(b["lk"], -80, 0).tolist(), "abs": b["abs_gate"], "rel": b["rel_gate"],
                                                           "kept": b["kept"].tolist(), "integrated": b["integrated"], "ungated": b["ungated"]},
            "drum": {"t": (np.arange(0, len(sn), step) / SR).tolist(), "wave": (sn[::step] / np.max(np.abs(sn))).tolist(), "vu": vu[::step].tolist(), "ppm": pp[::step].tolist(),
                     "peak": MS.sample_peak_db(sn)},
            "checks": checks, "tones": {"low": MS.lufs(lo), "high": MS.lufs(hi)},
            "starts": {"low": float(c.events["low"]), "high": float(c.events["high"])},
            "clips": {"two": save("meters.two", c, detail="a 60 Hz tone and a 2 kHz tone with the same RMS level, one after the other")}}


def compute_truepeak() -> dict:
    n = 64
    t = np.arange(n)
    phase = math.pi / 4
    s = np.sin(2 * np.pi * t / 4 + phase)
    s = s / np.max(np.abs(s))                    # samples reach 0 dBFS
    fine = np.arange(0, n, 1 / 16)
    cont = np.sin(2 * np.pi * fine / 4 + phase) / np.max(np.abs(np.sin(2 * np.pi * t / 4 + phase)))
    tp = MS.true_peak_db(np.tile(s, 200))
    m = the_mix()
    hot = m * 10 ** ((-7.0 - MS.lufs(m)) / 20)
    clipped = MS.clipper(hot, -0.1)
    lim = mastered(-7.0)["y"]
    return {"samples": s[:16].tolist(), "fine_t": fine[: 16 * 16].tolist(), "fine": cont[: 16 * 16].tolist(), "sine_tp": tp,
            "clipped": {"sample": MS.sample_peak_db(clipped), "true": MS.true_peak_db(clipped), "lufs": MS.lufs(clipped)},
            "limited": {"sample": MS.sample_peak_db(lim), "true": MS.true_peak_db(lim), "lufs": MS.lufs(lim)}}


def compute_limiter() -> dict:
    m = the_mix((0, 1))
    hot = m * 10 ** ((-8.0 - MS.lufs(m)) / 20)
    lim = MS.limiter(hot, -1.0)
    # a clipper pushed to the same loudness
    g = 0.0
    for _ in range(8):
        cl = MS.clipper(hot * 10 ** (g / 20), -1.0)
        g += MS.lufs(lim["y"]) - MS.lufs(cl)
    cl = MS.clipper(hot * 10 ** (g / 20), -1.0)
    k = int(4.8 * SR)
    seg = slice(int(1.2 * SR), int(1.2 * SR) + int(0.6 * SR))
    c = concat([C(fade(cl[:k])), C(fade(lim["y"][:k]))], gap=0.8, names=["clipped", "limited"])
    step = 48
    return {"lufs": MS.lufs(lim["y"]), "clip_tp": MS.true_peak_db(cl), "lim_tp": MS.true_peak_db(lim["y"]), "flat_clip": flat_fraction(cl), "gr_max": float(-lim["gain_db"].min()),
            "zoom": {"t": (np.arange(seg.start, seg.stop, step) / SR).tolist(), "in": hot[seg, 0][::step].tolist(), "clip": cl[seg, 0][::step].tolist(),
                     "lim": lim["y"][seg, 0][::step].tolist(), "gain": lim["gain_db"][seg][::step].tolist()},
            "starts": {"clipped": float(c.events["clipped"]), "limited": float(c.events["limited"])},
            "clips": {"two": save("limiter.two", c, detail="Part 56's mix pushed to about -8 LUFS twice: by a clipper, then by Monochord's look-ahead limiter, at the same loudness")}}


def compute_war() -> dict:
    rows, env = [], {}
    from explainer.music.monochord import dynamics as D
    for tg in TARGETS:
        r = mastered(tg)
        y = r["y"]
        rows.append({"target": tg, "lufs": r["lufs"], "tp": r["true_peak"], "plr": MS.plr(y), "lra": MS.loudness_range(y),
                     "crest": D.crest_db(y.mean(axis=1)), "drive": r["drive_db"], "gr_max": float(-r["gain_db"].min())})
        env[str(tg)] = envelope(y)
    segs = [C(fade(mastered(tg)["y"])) for tg in (-20.0, -14.0, -8.0)]
    c = concat(segs, gap=0.8, names=["m20", "m14", "m8"])
    return {"rows": rows, "env": env, "mix_lra": MS.loudness_range(the_mix()), "starts": {k: float(c.events[k]) for k in ("m20", "m14", "m8")},
            "clips": {"three": save("war.three", c, detail="Part 56's mix mastered to -20, -14 and -8 LUFS integrated, played as mastered (each louder than the last)", needs="headphones")}}


def compute_norm() -> dict:
    order = [-8.0, -20.0, -14.0]
    segs, gains = [], {}
    for tg in order:
        r = MS.normalize(mastered(tg)["y"], -14.0, allow_up=True)
        gains[str(tg)] = r["gain_db"]
        segs.append(C(fade(r["y"])))
    c = concat(segs, gap=0.8, names=["first", "second", "third"])
    return {"answer": "first", "order": order, "gains": gains, "starts": {k: float(c.events[k]) for k in ("first", "second", "third")},
            "clips": {"three": save("norm.three", c, detail="the masters at -8, -20 and -14 LUFS, each given the gain a streaming service would (to -14 LUFS, raised no further than -1 dBTP allows)")}}


def compute_matched() -> dict:
    y = mastered(-14.0, (0, 1))["y"]
    a = to_lufs(y, -18.0)
    b = a * 10 ** (1.0 / 20)
    c = concat([C(fade(a)), C(fade(b))], gap=0.8, names=["first", "second"])
    return {"answer": "the same", "difference_db": 1.0, "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("matched.two", c, detail="the same gentle master twice, the second exactly 1 dB louder")}}


def compute_dither() -> dict:
    note = np.asarray(P38.piano(60, 2.4, 0.8), float)
    note = 0.5 * note / np.max(np.abs(note))
    tail = note * np.exp(-np.arange(len(note)) / SR * 1.2)
    bits = 8
    r = MS.quantize(tail, bits)
    d = MS.tpdf_dither(tail, bits, np.random.default_rng(1))
    s = MS.shaped(tail, bits, np.random.default_rng(2))

    def err_spec(e):
        k = int(0.8 * SR)
        E_ = np.abs(np.fft.rfft(e[k:k + 16384] * np.hanning(16384))) ** 2
        f = np.fft.rfftfreq(16384, 1 / SR)
        bands = np.geomspace(50, 20000, 60)
        out = []
        for lo, hi in zip(bands[:-1], bands[1:]):
            sel = (f >= lo) & (f < hi)
            out.append(float(10 * np.log10(E_[sel].mean() + 1e-20)))
        return np.sqrt(bands[:-1] * bands[1:]).tolist(), out
    fr, er = err_spec(r - tail)
    _, ed = err_spec(d - tail)
    _, es = err_spec(s - tail)
    gain = 10 ** (18 / 20)                 # turned up afterwards, as a listener would to hear a quiet fade
    c = concat([C(fade(gain * r)), C(fade(gain * d)), C(fade(gain * s))], gap=0.8, names=["rounded", "dithered", "shaped"])
    return {"bits": bits, "f": fr, "err": {"rounded": er, "dithered": ed, "shaped": es},
            "snr_16": 6.02 * 16 + 1.76, "snr_24": 6.02 * 24 + 1.76,
            "starts": {k: float(c.events[k]) for k in ("rounded", "dithered", "shaped")},
            "clips": {"three": save("dither.three", c, detail="a piano note from Part 38 dying away, reduced to 8 bits (to make the effect audible) by rounding, with TPDF dither, and with dither and noise shaping; each turned up 18 dB")}}


def compute_vinyl() -> dict:
    f = np.geomspace(20, 20000, 300)
    riaa = MS.riaa_db(f)
    exc = MS.groove_excursion_um(f)
    from scipy.signal import lfilter
    (bp, ap), (bc, ac) = MS.riaa_filters()
    m = the_mix((0, 1))
    cut = lfilter(bc, ac, m, axis=0)
    flat = to_lufs(cut, -20.0)                    # played back with no de-emphasis
    right = to_lufs(lfilter(bp, ap, cut, axis=0), -20.0)
    c = concat([C(fade(flat)), C(fade(right))], gap=0.8, names=["flat", "riaa"])
    return {"f": f.tolist(), "riaa": riaa.tolist(), "excursion_um": exc.tolist(), "at": {"20": float(MS.riaa_db(20.0)), "20000": float(MS.riaa_db(20000.0))},
            "exc_50": float(MS.groove_excursion_um(50.0)), "exc_5k": float(MS.groove_excursion_um(5000.0)),
            "starts": {"flat": float(c.events["flat"]), "riaa": float(c.events["riaa"])},
            "clips": {"two": save("vinyl.two", c, detail="Part 56's mix cut with the RIAA pre-emphasis and played back without its de-emphasis, then with it (simulated filters)")}}


def compute_chain() -> dict:
    m = the_mix((0, 1))
    eq = MS.tilt(m, 1.0)
    gl = MS.glue(eq)
    fin = MS.master(m, -10.0)["y"]
    stages = {"mix": m, "eq": eq, "glue": gl, "limited": fin}
    from explainer.music.monochord import dynamics as D
    st = {k: {"lufs": MS.lufs(v), "tp": MS.true_peak_db(v), "crest": D.crest_db(v.mean(axis=1))} for k, v in stages.items()}
    c = concat([C(fade(m)), C(fade(gl)), C(fade(fin))], gap=0.8, names=["mix", "glue", "limited"])
    return {"stages": st, "starts": {k: float(c.events[k]) for k in ("mix", "glue", "limited")},
            "clips": {"three": save("chain.three", c, detail="Part 56's mix as delivered, after a tilt and gentle bus compression, and after the limiter at -10 LUFS, each at its own level")}}


def compute_series() -> dict:
    h = CLIPS.load("hook.two")
    return {"narration_lufs": -16.0, "example_level": EXAMPLE_LEVEL, "quiet_level": QUIET_LEVEL, "part_level": LEVEL, "ceiling_dbtp": -1.0,
            "narration_limit": 20 * math.log10(0.75), "hook": {"momentary_max": LN.momentary_max(h), "integrated": LN.integrated(h), "tp": LN.true_peak_db(h)}}


VARS = [("music52", "tune52", "tune.variation52"), ("music53", "tune53", "tune.variation53"), ("music54", "tune54", "tune.variation54"),
        ("music55", "tune55", "tune.variation55")]


def variation_clip(part, item, name):
    mod = importlib.import_module(f"videos.music.{part}.compute")
    if not mod.CLIPS.has(name):
        mod.CACHE.load(item)
    return mod.CLIPS.load(name)


def compute_tune57() -> dict:
    side = []
    names = []
    for part, item, name in VARS:
        y = variation_clip(part, item, name).stereo
        y = np.asarray(y, float)[: int(8.0 * SR)]
        side.append(C(fade(to_lufs(y, -16.0), 0.02, 0.6)))
        names.append(part)
    gentle = mastered(-14.0, (0, 1))["y"][: int(7.0 * SR)]
    war = mastered(-6.0, (0, 1))["y"][: int(7.0 * SR)]
    pair = [C(fade(to_lufs(gentle, -16.0))), C(fade(to_lufs(war, -16.0)))]
    c = concat(side + pair, gap=0.7, names=names + ["gentle", "war"])
    return {"side": names, "seconds": c.duration, "war_plr": MS.plr(war), "gentle_plr": MS.plr(gentle), "starts": {k: float(c.events[k]) for k in names + ["gentle", "war"]},
            "clips": {"variation57": save("tune.variation57", c, detail="headphones: an album side of four Variations (Parts 52 to 55), each eight seconds, matched at -16 LUFS; then Variation 56's session mastered gently and war-mastered, matched in loudness")}}


def compute_variation() -> dict:
    t = load("tune57")
    return {"part": 57, "title": "an album side, and one war-mastered beside itself", "seconds": round(t["seconds"], 1),
            "measure": f"four Variations at -16 LUFS; the war master's peak-to-loudness ratio {t['war_plr']:.1f} dB against {t['gentle_plr']:.1f}",
            "clip": "tune.variation57"}


ITEMS = {"hook": compute_hook, "meters": compute_meters, "truepeak": compute_truepeak, "limiter": compute_limiter, "war": compute_war,
         "norm": compute_norm, "matched": compute_matched, "dither": compute_dither, "vinyl": compute_vinyl, "chain": compute_chain,
         "series": compute_series, "tune57": compute_tune57, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
