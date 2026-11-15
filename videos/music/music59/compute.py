"""Precompute everything numerical, and every sound, in Part 59 of *Music, Built* ("Live Sound").

    python -m videos.music.music59.compute              # everything missing (a few minutes)
    python -m videos.music.music59.compute --force hook

Numbers are cached in ``.cache/music59/<name>.json``, sounds in ``.cache/music59/audio/``.  The tools are Monochord's
(``explainer/music/monochord/live.py``, with Part 49's image-source room and Part 55's head).  The music is Part 56's
session and Part 8's voice; every stadium, loudspeaker, crowd and car park is simulated.

Items:
    hook        an ear question: a band heard from the stands over a screaming crowd, through a 1965 stadium PA and a
                modern system
    feedback    a microphone and a loudspeaker in a hall: the loop's response, the gain before feedback, the howl
                predicted and found, ringing out; an ear question (which was closest to howling?)
    arrays      field maps and level against distance for a point source, a straight line array and a curved one;
                the curved array heard at 10, 40 and 80 m
    subs        a cardioid pair of subwoofers; behind the stage, heard
    delay       a delay tower, its delay and its temperature drift; an ear question (which was aligned?)
    air         ISO 9613-1 absorption; the mix at 10 and 100 m
    measure     a transfer function measured with music, its coherence and delay
    wireless    a channel plan free of third-order intermodulation, against an evenly spaced one
    sti         the speech transmission index against reverberation and noise; heard
    dose        noise doses for an audience, a crew and a musician
    tune59      Variation 59: the Tune at an arena: front of house, the back row, the car park
    variation   the Variations ledger, row 59
"""

from __future__ import annotations

import math

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat
from explainer.music.monochord import effects as E
from explainer.music.monochord import live as LV
from explainer.music.monochord import space as SP
from explainer.music.monochord import tune as T
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.partkit import saver
from videos.music.music56 import compute as P56

CACHE = Cache("music59")
CLIPS = ClipStore("music59")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
MAJOR = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}


def C(y) -> Clip:
    return Clip(np.asarray(y, float), SR)


def fade(y, a=0.005, r=0.08):
    y = np.array(y, float)
    ka, kr = max(int(a * SR), 1), max(int(r * SR), 1)
    y[:ka] *= np.linspace(0, 1, ka)[:, None] if y.ndim == 2 else np.linspace(0, 1, ka)
    y[len(y) - kr:] *= np.linspace(1, 0, kr)[:, None] if y.ndim == 2 else np.linspace(1, 0, kr)
    return y


def rms(y):
    return float(np.sqrt(np.mean(np.asarray(y, float) ** 2)) + 1e-20)


def at_db(y, db):
    """Scale to an RMS of ``db`` dBFS."""
    return np.asarray(y, float) * 10 ** (db / 20) / rms(y)


_V: dict = {}


def mix(phrases=(0, 1)):
    if phrases not in _V:
        s = P56.session(phrases)
        m = P56.mix_dry(s["tracks"], s["n"])["y"].mean(axis=1)
        _V[phrases] = m / np.max(np.abs(m))
    return _V[phrases]


def voice(phrases=(0,)):
    key = ("v", phrases)
    if key not in _V:
        notes = [(60 + MAJOR[e["degree"]], e["t"], e["dur"]) for e in T.events(0.5, list(phrases))]
        v = CH.sing(notes, "soprano", "a", seed=1)
        _V[key] = v / np.max(np.abs(v))
    return _V[key]


def crowd(seconds, seed=0):
    """A screaming stadium crowd: a broad roar plus thousands of overlapping shrieks (band-limited noise bursts with a
    pitch glide near 1.5 to 3 kHz)."""
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    roar = sosfilt(butter(2, [200, 2500], btype="band", fs=SR, output="sos"), rng.standard_normal(n))
    shrieks = np.zeros(n)
    t = np.arange(int(0.6 * SR)) / SR
    for _ in range(int(seconds * 40)):
        i = int(rng.integers(0, n - len(t)))
        f0 = rng.uniform(1300, 3000)
        glide = f0 * (1 + rng.uniform(-0.15, 0.25) * t / t[-1])
        s = np.sin(2 * np.pi * np.cumsum(glide) / SR) * np.exp(-((t - 0.3) / 0.18) ** 2) * rng.uniform(0.3, 1.0)
        shrieks[i:i + len(t)] += s
    return at_db(roar, -20) + at_db(shrieks, -20)


def arena(seconds=1.8, T60=2.5, seed=0):
    return SP.noise_tail(T60, seconds, seed=seed, start=0.02, dark=0.7)


def in_hall(x, T60, wet_db, seed=0):
    h = arena(min(1.3 * T60 + 0.3, 6.0), T60, seed)
    wet = fftconvolve(x, h)[: len(x)]
    return x + 10 ** (wet_db / 20) * wet * rms(x) / (rms(wet) + 1e-20)


# ---------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    m = mix((0, 1))
    n = len(m)
    old = sosfilt(butter(4, [350, 3500], btype="band", fs=SR, output="sos"), m)          # a 1965 stadium horn system
    old = np.tanh(3 * old / np.max(np.abs(old))) * 0.5
    old = in_hall(old, 3.5, 0.0, 1)
    new = in_hall(m, 2.5, -10.0, 2)
    cr = crowd(n / SR, 3)
    a = at_db(old, -26) + cr
    b = at_db(new, -12) + cr
    c = concat([C(fade(a)), C(fade(b))], gap=0.9, names=["first", "second"])
    return {"answer": "first", "snr": {"1965": -6.0, "modern": 8.0},
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("hook.two", c, detail="Part 56's session heard from the stands of a stadium over a screaming crowd (simulated): through a 1965-style horn system, band-limited and overdriven, then through a modern full-range system")}}


def hall_ir():
    return E.room_ir((20.0, 14.0, 8.0), (6.0, 6.0, 3.0), (1.5, 7.5, 1.6), alpha=0.25, sr=SR, seconds=1.0)


def compute_feedback() -> dict:
    ir = hall_ir()
    fb = LV.feedback(ir)
    ro = LV.ring_out(ir, 6)
    f = fb["f"]
    k = (f >= 100) & (f <= 8000)
    step = max(1, int(k.sum() / 1500))
    n = 1 << int(math.ceil(math.log2(len(ir) * 4)))
    H = np.fft.rfft(ir, n)
    ff = np.fft.rfftfreq(n, 1 / SR)
    sel = (ff >= 100) & (ff <= 8000)
    re_db = 20 * np.log10(np.clip(H[sel].real, 1e-6, None))
    # the loop run in time: a clap, at three margins below the edge, and one just above
    rng = np.random.default_rng(1)
    clap = np.zeros(int(2.4 * SR))
    clap[:240] = rng.standard_normal(240) * np.hanning(240) * 0.3
    rings = {}
    for name, margin in (("m6", -6.0), ("m2", -2.0), ("m05", -0.5)):
        y = LV.closed_loop(clap, ir, fb["max_gain_db"] + margin, 2.4)
        rings[name] = y
    tail = {k_: float(10 * np.log10(np.mean(v[int(1.0 * SR):] ** 2) / np.mean(v[:int(0.2 * SR)] ** 2))) for k_, v in rings.items()}
    order = ["m6", "m05", "m2"]
    c = concat([C(fade(rings[k_] / np.max(np.abs(rings[k_])))) for k_ in order], gap=0.8, names=["first", "second", "third"])
    v = voice((0,))
    over = LV.closed_loop(np.r_[0.05 * v, np.zeros(int(1.5 * SR))], ir, fb["max_gain_db"] + 0.6)
    over = over / np.max(np.abs(over))
    Y = np.abs(np.fft.rfft(over[-int(1.0 * SR):]))
    fy = np.fft.rfftfreq(int(1.0 * SR), 1 / SR)
    found = float(fy[np.argmax(Y * (fy > 100))])
    c2 = concat([C(fade(over))], gap=0.0, names=["howl"])
    # ringing out heard: the same voice at the same gain (0.5 dB under the original edge), before and after six notches
    from scipy.signal import lfilter
    from explainer.music.monochord import effects as EF
    ir_ro = ir.copy()
    for r_ in ro[1:]:
        b_, a_ = EF.biquad("peak", r_["cut_hz"], SR, 10.0, -9.0)
        ir_ro = lfilter(b_, a_, ir_ro)
    src = np.r_[0.05 * v, np.zeros(int(1.0 * SR))]
    before = LV.closed_loop(src, ir, fb["max_gain_db"] - 0.5)
    after = LV.closed_loop(src, ir_ro, fb["max_gain_db"] - 0.5)
    g_ = 1 / max(np.max(np.abs(before)), np.max(np.abs(after)))
    c3 = concat([C(fade(before * g_)), C(fade(after * g_))], gap=0.8, names=["before", "after"])
    pag = LV.pag_nag(d0=20.0, d1=6.0, ds=0.3, d2=12.0)
    return {"max_gain_db": fb["max_gain_db"], "howl_hz": fb["howl_hz"], "peak_hz": fb["peak_hz"], "peak_gain_db": fb["peak_gain_db"], "found_hz": found,
            "f": ff[sel][::step].tolist(), "mag_db": (20 * np.log10(np.abs(H[sel]) + 1e-12))[::step].tolist(), "re_db": re_db[::step].tolist(),
            "ringout": ro, "tail_db": tail, "answer": "second", "order": order, "pag": pag,
            "starts": {k_: float(c.events[k_]) for k_ in ("first", "second", "third")},
            "starts_ro": {"before": float(c3.events["before"]), "after": float(c3.events["after"])},
            "clips": {"ringout": save("feedback.ringout", c3, detail="Part 8's voice through the same loop 0.5 dB under the edge, before ringing out and after six narrow notches at the frequencies that would howl"),
                      "three": save("feedback.three", c, detail="a clap into a microphone whose loudspeaker shares a simulated hall with it, at three gains below the edge of feedback (6, 0.5 and 2 dB), in that order"),
                      "howl": save("feedback.howl", c2, detail="Part 8's voice into the same loop with the gain 0.6 dB past the edge: the howl builds at the frequency Nyquist's criterion predicts")}}


def compute_arrays() -> dict:
    xs = np.linspace(1, 90, 180)
    ys = np.linspace(-2, 18, 60)
    n_el, sp = 24, 0.35
    straight, _ = LV.line_array(n_el, sp, (0.0, 14.0))
    splay = [0.3] * 10 + [0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.2]
    curved, _ = LV.line_array(n_el, sp, (0.0, 14.0), splay)
    cy = float(np.mean([p_[1] for p_ in straight]))
    point = [(0.0, cy)]

    def third(fn, f):
        """Power-averaged over a third of an octave (nine frequencies), as a measurement would be, so that single-frequency
        interference nulls do not decide the answer."""
        fs = f * 2 ** (np.linspace(-1, 1, 9) / 6)
        return 10 * np.log10(np.mean([10 ** (np.asarray(fn(ff)) / 10) for ff in fs], axis=0))
    maps = {"point": third(lambda ff: LV.field(point, ff, xs, ys), 1000.0).tolist(),
            "straight": third(lambda ff: LV.field(straight, ff, xs, ys), 1000.0).tolist(),
            "curved": third(lambda ff: LV.field(curved, ff, xs, ys), 1000.0).tolist()}
    dists = np.geomspace(2, 200, 160)
    curves, per_doubling = {}, {}
    for f in (250.0, 1000.0, 4000.0):
        pt = third(lambda ff: LV.field(point, ff, dists, [cy], air=False)[0], f)
        li = third(lambda ff: LV.field(straight, ff, dists, [cy], air=False)[0], f)
        curves[str(int(f))] = {"point": pt.tolist(), "line": li.tolist()}
        at = lambda c, x: float(np.interp(x, dists, c))                                       # noqa: E731
        per_doubling[str(int(f))] = {"point": (at(pt, 4) - at(pt, 64)) / 4, "line_near": (at(li, 4) - at(li, 16)) / 2, "line_far": (at(li, 64) - at(li, 128))}
    length = n_el * sp
    transition = {str(int(f)): length ** 2 * f / (2 * LV.C) for f in (250.0, 1000.0, 4000.0)}
    m = mix((0,))
    segs = []
    lc = np.array(curves["1000"]["line"])
    for dd in (10.0, 40.0, 80.0):
        lvl = float(np.interp(dd, dists, lc) - np.interp(10.0, dists, lc))
        y = LV.air_filter(m, dd) * 10 ** (lvl / 20)
        y = in_hall(y, 2.5, -14 + 12 * math.log10(dd / 10), int(dd))
        segs.append(C(fade(y)))
    c = concat(segs, gap=0.8, names=["d10", "d40", "d80"])
    levels = {str(int(dd)): float(np.interp(dd, dists, lc) - np.interp(10.0, dists, lc)) for dd in (10, 40, 80)}
    return {"xs": xs.tolist(), "ys": ys.tolist(), "maps": maps, "dists": dists.tolist(), "curves": curves, "per_doubling": per_doubling,
            "transition": transition, "length": length, "spacing": sp, "n": n_el, "half_wave_hz": LV.C / (2 * sp), "levels": levels,
            "straight": straight, "curved": curved, "splay": splay, "starts": {k: float(c.events[k]) for k in ("d10", "d40", "d80")},
            "clips": {"three": save("arrays.three", c, detail="Part 56's mix from a line array (simulated), heard at 10, 40 and 80 m: the array's level, the air's absorption and the arena's reverberation at each seat")}}


def compute_subs() -> dict:
    f = np.geomspace(25, 200, 200)
    r = LV.cardioid_sub(f, 0.9)
    m = mix((0, 1))
    lowpass = butter(4, 120, fs=SR, output="sos")
    sub = sosfilt(lowpass, m)
    top = m - sub
    F = np.fft.rfftfreq(len(m), 1 / SR)
    S = np.fft.rfft(sub)
    back_gain = np.interp(F, f, 10 ** (r["back_db"] / 20), left=10 ** (r["back_db"][0] / 20), right=10 ** (r["back_db"][-1] / 20))
    front_gain = np.interp(F, f, 10 ** (r["front_db"] / 20), left=10 ** (r["front_db"][0] / 20), right=10 ** (r["front_db"][-1] / 20))
    behind_plain = sub + 0.3 * top
    behind_card = np.fft.irfft(S * back_gain, len(m)) + 0.3 * top
    g = 1 / max(np.max(np.abs(behind_plain)), 1e-9)
    c = concat([C(fade(behind_plain * g)), C(fade(behind_card * g))], gap=0.8, names=["plain", "cardioid"])
    i63 = int(np.argmin(abs(f - 63)))
    return {"f": f.tolist(), "front_db": r["front_db"].tolist(), "back_db": r["back_db"].tolist(), "spacing": 0.9, "delay_ms": 0.9 / LV.C * 1000,
            "at63": {"front": float(r["front_db"][i63]), "back": float(r["back_db"][i63])},
            "starts": {"plain": float(c.events["plain"]), "cardioid": float(c.events["cardioid"])},
            "clips": {"two": save("subs.two", c, detail="Part 56's mix heard behind the stage (simulated): ordinary subwoofers, then a cardioid pair whose rear output cancels", needs="bass")}}


def compute_delay() -> dict:
    d_main, d_tower = 90.0, 30.0
    dt = LV.delay_time(d_main, d_tower)
    drift = {str(tc): LV.delay_time(d_main, d_tower, tc) - dt for tc in (10, 20, 30)}
    v = voice((0,))
    n = len(v) + int(0.5 * SR)
    main_arr = (d_main / LV.C)
    def render(tower_delay):
        y = np.zeros(n)
        i_main = int(main_arr * SR)
        i_tower = int((tower_delay + d_tower / LV.C) * SR)
        y[i_main:i_main + len(v)] += 0.45 * v[: n - i_main]
        y[i_tower:i_tower + len(v)] += 1.0 * v[: n - i_tower]
        return in_hall(y, 1.2, -16.0, 5)[int(0.05 * SR):]
    wrong = render(0.0)
    right = render(dt)
    order = ["right", "wrong"]
    seg = {"right": right, "wrong": wrong}
    c = concat([C(fade(seg[k] / np.max(np.abs(seg[k])))) for k in order], gap=0.8, names=["first", "second"])
    return {"d_main": d_main, "d_tower": d_tower, "delay_ms": 1000 * dt, "drift_ms": {k: 1000 * v_ for k, v_ in drift.items()},
            "c": {str(tc): LV.speed_of_sound(tc) for tc in (0, 10, 20, 30)}, "answer": "first", "order": order,
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("delay.two", c, detail="Part 8's voice heard 90 m from the stage and 30 m from a delay tower (simulated): the tower delayed correctly, then not delayed at all")}}


def compute_air() -> dict:
    f = np.geomspace(100, 20000, 200)
    curves = {k: LV.air_absorption_db_per_m(f, t_, rh).tolist() for k, (t_, rh) in {"20C 50%": (20, 50), "30C 20%": (30, 20), "10C 80%": (10, 80)}.items()}
    loss100 = {str(ff): float(LV.air_absorption_db_per_m(ff) * 100) for ff in (1000, 4000, 8000, 16000)}
    m = mix((0,))
    near = LV.air_filter(m, 10.0)
    far = LV.air_filter(m, 100.0)
    c = concat([C(fade(near)), C(fade(far * rms(near) / rms(far)))], gap=0.8, names=["near", "far"])
    return {"f": f.tolist(), "curves": curves, "loss100": loss100,
            "starts": {"near": float(c.events["near"]), "far": float(c.events["far"])},
            "clips": {"two": save("air.two", c, detail="Part 56's mix after 10 m and after 100 m of air at 20 degrees and 50 per cent humidity (ISO 9613-1), matched in loudness")}}


def compute_measure() -> dict:
    rng = np.random.default_rng(4)
    ir = hall_ir()[: int(0.25 * SR)]
    delay = int(0.0234 * SR)
    ir = np.r_[np.zeros(delay), ir]
    x = mix((0, 1, 2))
    y = fftconvolve(x, ir)[: len(x)] + 0.003 * rng.standard_normal(len(x))
    tf = LV.transfer_function(x, y, 32768)
    f = tf["f"]
    sel = (f >= 30) & (f <= 16000)
    idx = np.unique(np.geomspace(1, sel.sum() - 1, 500).astype(int))
    fs = f[sel][idx]
    true = np.abs(np.fft.rfft(ir, 32768))[sel][idx]
    return {"f": fs.tolist(), "mag_db": (20 * np.log10(np.abs(tf["H"][sel][idx]) + 1e-12)).tolist(), "true_db": (20 * np.log10(true + 1e-12)).tolist(),
            "coherence": tf["coherence"][sel][idx].tolist(), "delay_ms": 1000 * tf["delay_s"], "true_delay_ms": 1000 * float(np.argmax(np.abs(ir))) / SR}


def compute_wireless() -> dict:
    tv = [(482.0, 488.0), (512.0, 518.0), (530.0, 536.0)]
    plan = LV.plan_channels(470.0, 542.0, 24, exclude=tv)
    even = [470.0 + 0.5 * i for i in range(24)]
    prods = LV.imd3(even)
    hits = sum(1 for c in even if any(abs(p - c) < 0.1 for p in prods))
    prods_plan = LV.imd3(plan)
    hits_plan = sum(1 for c in plan if any(abs(p - c) < 0.1 for p in prods_plan))
    return {"plan": plan, "tv": tv, "even": even, "hits_even": hits, "hits_plan": hits_plan, "n_products_plan": len(prods_plan),
            "band": [470.0, 542.0]}


def compute_sti() -> dict:
    Ts = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0]
    snrs = [-3.0, 0.0, 3.0, 6.0, 10.0, 15.0, 30.0]
    grid = [[LV.sti(t_, s_) for s_ in snrs] for t_ in Ts]
    v = voice((0, 1))
    rng = np.random.default_rng(6)
    conds = {"good": (0.8, 25.0), "fair": (2.5, 10.0), "bad": (5.0, 0.0)}
    segs = []
    for k, (t_, s_) in conds.items():
        y = in_hall(v, t_, 10 * math.log10(max(t_, 0.3) / 0.5) * 1.2 - 3, 7)
        noise = sosfilt(butter(2, [200, 6000], btype="band", fs=SR, output="sos"), rng.standard_normal(len(y)))
        y = y + noise * rms(y) * 10 ** (-s_ / 20) / rms(noise)
        segs.append(C(fade(y)))
    c = concat(segs, gap=0.8, names=list(conds))
    return {"T": Ts, "snr": snrs, "grid": grid, "conds": {k: {"T": v_[0], "snr": v_[1], "sti": LV.sti(*v_)} for k, v_ in conds.items()},
            "starts": {k: float(c.events[k]) for k in conds},
            "clips": {"three": save("sti.three", c, detail="Part 8's voice in three simulated spaces: reverberation 0.8 s with noise 25 dB down, 2.5 s with noise 10 dB down, 5 s with noise as loud as the voice")}}


def compute_dose() -> dict:
    rows = [{"who": "a fan at the barrier, 2 hours at 104 dBA", "levels": [104], "hours": [2]},
            {"who": "a fan mid-arena, 2 hours at 98 dBA", "levels": [98], "hours": [2]},
            {"who": "the same fan with 15 dB earplugs", "levels": [83], "hours": [2]},
            {"who": "a front-of-house engineer: soundcheck and show at 96 dBA, 5 hours", "levels": [96], "hours": [5]},
            {"who": "a drummer: 2 hours at 105 dBA, in-ear monitors at 88", "levels": [88], "hours": [2]}]
    for r in rows:
        r["dose"] = LV.dose(r["levels"], r["hours"])
    return {"rows": rows, "allowed": {str(L_): LV.allowed_hours(L_) * 60 for L_ in (85, 88, 91, 94, 97, 100, 103, 106)}}


def compute_tune59() -> dict:
    m = mix((0, 1, 2))
    segs = []
    names = ["foh", "back", "carpark"]
    foh = in_hall(m, 2.5, -14.0, 11)
    back = in_hall(LV.air_filter(m, 100.0), 2.5, -4.0, 12) * 10 ** (-8 / 20)
    wall = sosfilt(butter(2, 180, fs=SR, output="sos"), m)                      # through a concrete wall: the mass law leaves the bass
    car = in_hall(LV.air_filter(wall, 200.0), 1.0, -8.0, 13) * 10 ** (-26 / 20)
    traffic = sosfilt(butter(2, [60, 900], btype="band", fs=SR, output="sos"), np.random.default_rng(9).standard_normal(len(m)))
    car = car + at_db(traffic, 20 * np.log10(rms(car)) - 4)
    lv = {"foh": 0.0, "back": 20 * math.log10(rms(back) / rms(foh)), "carpark": 20 * math.log10(rms(car) / rms(foh))}
    for y in (foh, back, car):
        segs.append(C(fade(y)))
    c = concat(segs, gap=0.8, names=names)
    return {"names": names, "levels_db": lv, "seconds": c.duration, "starts": {k: float(c.events[k]) for k in names},
            "clips": {"variation59": save("tune.variation59", c, detail="Part 56's session playing the Tune in a simulated arena: at the mixing desk, in the back row 100 m away, and in the car park outside behind a concrete wall; levels as heard", needs="bass")}}


def compute_variation() -> dict:
    t = load("tune59")
    return {"part": 59, "title": "at an arena: front of house, the back row, the car park", "seconds": round(t["seconds"], 1),
            "measure": f"the back row {-t['levels_db']['back']:.0f} dB down, the car park {-t['levels_db']['carpark']:.0f} dB down and mostly bass",
            "clip": "tune.variation59"}


ITEMS = {"hook": compute_hook, "feedback": compute_feedback, "arrays": compute_arrays, "subs": compute_subs, "delay": compute_delay,
         "air": compute_air, "measure": compute_measure, "wireless": compute_wireless, "sti": compute_sti, "dose": compute_dose,
         "tune59": compute_tune59, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
