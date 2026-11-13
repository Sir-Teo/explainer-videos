"""Precompute everything numerical, and every sound, in Part 4 of *Music, Built* ("The Ear").

    python -m videos.music.music4.compute              # everything missing (about a minute)
    python -m videos.music.music4.compute --force pitch

Numbers are cached in ``.cache/music4/<name>.json`` (+ ``.npz``), sounds in ``.cache/music4/audio/``.  The models
of the ear are Monochord's (``explainer/music/monochord/ear.py``); published constants and measurements are cited
in the README.

Items:
    two         two loud tones, and the third tone an active ear adds to them
    outer       the ear canal's resonance and the middle ear's gain
    wave        the travelling wave in a model cochlea: envelopes, a film, the place map, passive against active
    bands       auditory filters: their widths, Fletcher's band-widening experiment, the Tune as a cochleagram
    loud        the threshold of hearing, A-weighting, sones; three tones of equal strength
    mask        what a 1 kHz tone hides: the model's masking pattern, and a test for the ear
    locking     how well the nerve's firing follows the wave, from 250 Hz to 8 kHz
    pitch       the autocorrelation model on a pure tone, a full tone, a tone with no fundamental and a shifted one
    limit       where pitch stops: the Tune's opening at an ordinary height and above five kilohertz
    shepard     a staircase that never ends
    dose        how long is safe at each level
    active      the frontier: one oscillator poised at the edge of oscillation
    tune        Variation 4: the Tune with no fundamentals, and then with no octaves
    nextpart    two pairs of notes for Part 5
    variation   the Variations ledger, row 4
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, QUIET_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import ear
from explainer.music.monochord.dsp import fourier as F
from explainer.music.monochord.instruments.plucked import C3
from explainer.music.monochord.partkit import play_tune, saver, string_note
from explainer.music.monochord.pitch import cents, nearest_note

CACHE = Cache("music4")
CLIPS = ClipStore("music4")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
SOFT = QUIET_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="synthesized")


def tone(y, fade=(0.02, 0.06)) -> Clip:
    return Clip(np.asarray(y, dtype=np.float64)).fade(*fade)


def sine(hz: float, seconds: float, amp: float = 1.0) -> np.ndarray:
    t = np.arange(int(seconds * SR)) / SR
    return amp * np.sin(2 * np.pi * hz * t)


def level_at(y: np.ndarray, hz: float, sr: int = SR) -> float:
    """The level (dB re the strongest line) of a sound's spectrum at one frequency."""
    spec = np.abs(np.fft.rfft(y * np.hanning(len(y))))
    f = np.fft.rfftfreq(len(y), 1 / sr)
    return float(20 * np.log10(max(spec[np.abs(f - hz) < 12].max(), 1e-12) / spec.max()))


# ---------------------------------------------------------------------------
def compute_two() -> dict:
    f1, f2 = 1000.0, 1200.0
    y = sine(f1, 3.0) + sine(f2, 3.0)
    c = tone(y, (0.05, 0.1))
    # what an active oscillator tuned to 800 Hz does with those two tones
    sr = 96_000
    t = np.arange(int(0.2 * sr)) / sr
    out = ear.hopf_run(3.0 * (np.cos(2 * np.pi * f1 * t) + np.cos(2 * np.pi * f2 * t)), sr, 800.0, mu=-1.0, scale=4000.0)
    seg = out[len(out) // 2:]
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    f = np.fft.rfftfreq(len(seg), 1 / sr)
    keep = f < 2000
    return {"f1": f1, "f2": f2, "third": 2 * f1 - f2, "in_the_clip_db": level_at(y[SR:2 * SR], 800.0),
            "ear_f": f[keep], "ear_db": 20 * np.log10(np.maximum(spec[keep] / spec.max(), 1e-6)),
            "ear_third_db": level_at(seg, 800.0, sr), "ear_floor_db": level_at(seg, 700.0, sr),
            "clips": {"tones": save("two.tones", c, level=LEVEL + 2, detail="two pure tones, and nothing else"),
                      "guide": save("two.guide", concat([tone(sine(800.0, 1.2, 0.2)), tone(y, (0.05, 0.1)), tone(sine(800.0, 1.0, 0.2))],
                                                        gap=0.5, names=["guide", "pair", "again"]),
                                    level=LEVEL + 2, detail="a quiet guide tone at 800 Hz, then the two tones, then the guide")}}


def compute_outer() -> dict:
    m = ear.middle_ear()
    f = np.geomspace(100, 12000, 200)
    return {"canal_hz": ear.canal_resonance(), "canal_cm": 100 * ear.CANAL_LENGTH, "middle": m,
            "f": f, "threshold": ear.threshold_db(f), "best_hz": float(f[int(np.argmin(ear.threshold_db(f)))])}


def compute_wave() -> dict:
    tones = [125.0, 250.0, 500.0, 1000.0, 2000.0, 4000.0, 8000.0]
    env = {}
    rows = []
    for hz in tones:
        c = ear.cochlea(hz)
        env[f"env_{int(hz)}"] = (c["envelope"] / c["peak"])[::10]
        rows.append({"hz": hz, "peak_mm": 1000 * c["peak_x"], "resonant_mm": 1000 * c["resonant_x"],
                     "greenwood_hz": float(ear.greenwood(c["peak_x"]))})
    # a film of the wave at 1 kHz: the membrane's shape at 24 moments of one cycle
    c = ear.cochlea(1000.0)
    ph = np.exp(2j * np.pi * np.arange(25) / 24)                # 25 moments: the last is the first again
    frames = np.real(c["displacement"][None, ::10] * ph[:, None]) / c["peak"]
    # the place map of the model, against the measured one
    fs = np.geomspace(125, 12000, 28)
    places = np.array([ear.cochlea(v, n=1200)["peak_x"] for v in fs])
    green = ear.greenwood(places)
    q_passive, q_active = ear.sharpness(2000.0, 0.08), ear.sharpness(2000.0, 0.02)
    a, b = ear.cochlea(2000.0, damping=0.08), ear.cochlea(2000.0, damping=0.02)
    # the same seven tones as sound, each at about the same loudness
    parts = [tone(sine(hz, 0.8, 10 ** (-float(ear.a_weight_db(hz)) / 40))) for hz in tones]
    glide = concat(parts, gap=0.1, names=[f"t{int(hz)}" for hz in tones])
    per_octave = (rows[0]["peak_mm"] - rows[-1]["peak_mm"]) / 6.0
    return {"x_mm": 1000 * c["x"][::10], "rows": rows, **env, "frames": frames, "tones": tones, "mm_per_octave": per_octave,
            "inner": 3500, "outer": 12000, "fibres": 30000,
            "clips": {"glide": save("wave.glide", glide, detail="seven pure tones, each an octave above the last",
                                    needs="the first tone is at 125 Hz: small speakers will lose it")},
            "map_hz": fs, "map_mm": 1000 * places, "map_greenwood_hz": green, "q_passive": q_passive, "q_active": q_active,
            "passive": (a["envelope"] / b["peak"])[::10], "active": (b["envelope"] / b["peak"])[::10],
            "gain_db": 20 * math.log10(b["peak"] / a["peak"]), "length_mm": 1000 * ear.COCHLEA_LENGTH}


def compute_bands() -> dict:
    centres = [250.0, 1000.0, 4000.0]
    f = np.geomspace(80, 12000, 500)
    shapes = {f"shape_{int(c)}": np.maximum(ear.filter_response_db(c, f), -60.0) for c in centres}
    widths = []
    for c in centres:
        g = ear.gammatone(c, SR)
        n = 1 << 18
        h2 = np.abs(np.fft.rfft(g, n)) ** 2
        ff = np.fft.rfftfreq(n, 1 / SR)
        widths.append({"hz": c, "measured": float(h2.sum() * (ff[1] - ff[0]) / h2.max()), "erb": float(ear.erb(c)),
                       "semitones": 12 * math.log2((c + float(ear.erb(c)) / 2) / (c - float(ear.erb(c)) / 2))})
    # Fletcher's experiment (1940): a tone in a band of noise centred on it; widen the band, with the noise's
    # power per hertz held fixed, and measure how strong the tone must be to be heard
    g = ear.gammatone(1000.0, SR)
    n = 1 << 18
    h2 = np.abs(np.fft.rfft(g, n)) ** 2
    ff = np.fft.rfftfreq(n, 1 / SR)
    bw = np.geomspace(10, 2000, 60)
    inside = np.array([h2[(ff > 1000 - w / 2) & (ff < 1000 + w / 2)].sum() * (ff[1] - ff[0]) for w in bw])
    thr = 10 * np.log10(inside / inside[-1])
    knee = float(bw[int(np.argmax(thr > -1.0))])
    # the Tune's opening as the cochlea delivers it
    phrase = play_tune(lambda hz, dur, e: string_note(C3 / hz, dur + 0.3, release=None if e["last"] else dur - 0.04),
                       phrases=[0], tail=1.0).at_level(LEVEL)
    # three pairs of pure tones: 8 Hz apart, 60 Hz apart, 400 Hz apart
    gaps = [8.0, 60.0, 400.0]
    pairs = concat([tone(sine(1000.0, 1.8) + sine(1000.0 + g_, 1.8)) for g_ in gaps], gap=0.4, names=["beats", "rough", "two"])
    # which harmonics of a note does the ear resolve?  those whose neighbours are more than one band away
    resolved = {}
    for f0 in (65.4, 130.8, 261.6, 523.3):
        k = 1
        while float(ear.erb(k * f0)) < f0 and k < 40:
            k += 1
        resolved[f"{f0:g}"] = k - 1
    cf = ear.erb_space(80.0, 6000.0, 64)
    cg = ear.cochleagram(phrase.mono.astype(np.float64), SR, cf, hop=480)
    return {"f": f, **shapes, "widths": widths, "bands_to_16k": float(ear.erb_number(16000.0)),
            "fletcher_bw": bw, "fletcher_db": thr, "fletcher_knee": knee, "erb_1k": float(ear.erb(1000.0)),
            "cochleagram": (cg - cg.max()).astype(np.float32), "cg_lo": 80.0, "cg_hi": 6000.0, "cg_seconds": float(phrase.duration),
            "gaps": gaps, "resolved": resolved, "mm_per_band": 1000 * ear.COCHLEA_LENGTH / float(ear.erb_number(20000.0)),
            "clips": {"phrase": save("bands.phrase", phrase, kind="physical model", level=None),
                      "pairs": save("bands.pairs", pairs, detail="1000 Hz with a second tone 8, 60 and 400 Hz above it")}}


def compute_loud() -> dict:
    f = np.geomspace(20, 16000, 300)
    three = [100.0, 1000.0, 3500.0]
    rows = [{"hz": v, "a_db": float(ear.a_weight_db(v)), "threshold": float(ear.threshold_db(v))} for v in three]
    # three tones with exactly the same pressure
    parts = [tone(sine(v, 1.4)) for v in three]
    gain = (LEVEL - 4) - max(__import__("explainer.music.monochord.loudness", fromlist=["momentary_max"]).momentary_max(p) for p in parts)
    seq = concat([p.gain(gain) for p in parts], gap=0.3, names=["low", "mid", "high"])
    rms = [float(np.sqrt(np.mean(p.gain(gain).mono[4800:-4800] ** 2))) for p in parts]
    phons = np.arange(20, 101, 10)
    secs = 7.0
    tt = np.arange(int(secs * SR)) / SR
    f_lo, f_hi = 100.0, 10000.0
    phase = 2 * np.pi * f_lo * secs / math.log(f_hi / f_lo) * ((f_hi / f_lo) ** (tt / secs) - 1)
    sweep = save("loud.sweep", tone(np.sin(phase), (0.05, 0.1)), level=LEVEL - 5, detail="one tone sliding from 100 Hz to 10,000 at constant pressure",
                 needs="needs bass: it starts at 100 Hz")
    one = string_note(0.5, 1.6).at_level(LEVEL - 9)
    ten = save("loud.ten", concat([one, one.gain(10.0)], gap=0.4, names=["one", "ten"]), kind="physical model", level=None,
               detail="one note, then the same note 10 dB stronger")
    return {"sweep_lo": f_lo, "sweep_hi": f_hi, "sweep_seconds": secs, "sixteen_db": 10 * math.log10(16), "sixteen_times": 16 ** 0.30103,
            "f": f, "threshold": ear.threshold_db(f), "a_weight": ear.a_weight_db(f), "rows": rows,
            "equal_pressure_spread_db": float(20 * math.log10(max(rms) / min(rms))), "quiz_answer": "the first",
            "phons": phons, "sones": ear.sones(phons), "ten_players_db": 10.0, "ten_players_sones": float(ear.sones(50) / ear.sones(40)),
            "clips": {"three": save("loud.three", seq, level=None, detail="three tones of the same pressure",
                                    needs="needs bass: the first tone is at 100 Hz"), "sweep": sweep, "ten": ten}}


def compute_mask() -> dict:
    masker_hz, masker_db = 1000.0, 70.0
    f = np.geomspace(250, 8000, 120)
    thr = ear.masked_threshold(masker_hz, masker_db, f)
    quiet = ear.threshold_db(f)
    probe_db = 43.0
    near, far = 1150.0, 3000.0
    t_near, t_far = (float(ear.masked_threshold(masker_hz, masker_db, v)[0]) for v in (near, far))
    # as sound: the masker a little above the part's level; the probe 27 dB below it
    secs = 1.6
    m = sine(masker_hz, secs)
    drop = 10 ** (-(masker_db - probe_db) / 20)

    def beeps(hz):
        y = sine(hz, secs, drop)
        gate = (np.sin(2 * np.pi * 2.5 * np.arange(len(y)) / SR) > 0).astype(float)      # the probe pulses on and off
        k = int(0.01 * SR)
        gate = np.convolve(gate, np.ones(k) / k, mode="same")
        return y * gate

    ref = tone(m).at_level(LEVEL + 2.3)
    g = ref.mono.max() / np.abs(m).max()
    cases = [tone(beeps(near) * g * 1.0), tone((m + beeps(near)) * g), tone((m + beeps(far)) * g)]
    seq = concat(cases, gap=0.4, names=["alone", "near", "far"])
    return {"masker_hz": masker_hz, "masker_db": masker_db, "f": f, "masked": thr, "quiet": quiet, "probe_db": probe_db,
            "near_hz": near, "far_hz": far, "near_threshold": t_near, "far_threshold": t_far,
            "near_heard": bool(probe_db > t_near), "far_heard": bool(probe_db > t_far),
            "clips": {"demo": save("mask.demo", seq, level=None, detail="a quiet pulsing tone, alone and beside a loud one")}}


def compute_locking() -> dict:
    rng = np.random.default_rng(7)
    rows, waves = [], {}
    for hz in (250.0, 500.0, 1000.0, 2000.0, 4000.0, 8000.0):
        y = sine(hz, 0.25)
        bank = ear.filterbank(y, SR, [hz])
        v = ear.neural(bank, SR)[0][int(0.05 * SR):]
        rate = v / v.max()
        # spikes: more likely the higher the nerve's signal; the timing of each spike within the cycle of the tone
        spikes = np.where(rng.random(len(rate)) < 0.02 * rate)[0]
        phase = 2 * np.pi * hz * spikes / SR
        strength = float(abs(np.sum(rate * np.exp(2j * np.pi * hz * np.arange(len(rate)) / SR))) / np.sum(rate))   # exact, not sampled
        sal = float(ear.pitch(y, SR, lo=50, hi=min(1.5 * hz, 6000))[1])
        rows.append({"hz": hz, "synchrony": strength, "salience": sal, "spikes": int(len(spikes))})
        # where in the cycle the spikes of many fibres fall (a long run, folded onto one cycle)
        long = rate[np.arange(len(rate) * 12) % len(rate)]
        many = np.where(rng.random(len(long)) < 0.05 * long)[0] % len(rate)
        h = np.histogram((hz * many / SR + 0.25 + 1 / 24) % 1.0, bins=12, range=(0, 1))[0].astype(float)
        waves[f"hist_{int(hz)}"] = h / h.max()
        if hz in (250.0, 4000.0):
            per = int(SR / hz * (4 if hz == 250.0 else 64))
            waves[f"drive_{int(hz)}"] = bank[0][int(0.05 * SR): int(0.05 * SR) + per] / np.abs(bank[0]).max()
            waves[f"nerve_{int(hz)}"] = v[:per] / v.max()
            seg = spikes[spikes < per]
            waves[f"spikes_{int(hz)}"] = seg / per
            # ten fibres from the same place: each fires seldom, at its own moments
            xs, ys = [], []
            for fibre in range(10):
                k = np.where(rng.random(per) < 0.03 * rate[:per])[0]
                xs += list(k / per)
                ys += [fibre] * len(k)
            waves[f"raster_x_{int(hz)}"] = np.array(xs)
            waves[f"raster_row_{int(hz)}"] = np.array(ys)
    # two pairs of tones for the ear: the second tone of A is 17 cents higher, of B 5 cents lower
    steps = {"A": 17.0, "B": -5.0}
    pair = lambda c_: concat([tone(sine(1000.0, 0.7)), tone(sine(1000.0 * 2 ** (c_ / 1200), 0.7))], gap=0.12)   # noqa: E731
    jnd = concat([pair(steps["A"]), pair(steps["B"])], gap=0.9, names=["A", "B"])
    return {"rows": rows, **waves, "piano_top_hz": 4186.0, "steps": steps, "b_hz": 1000.0 * 2 ** (steps["B"] / 1200),
            "jnd_cents": 3.5, "jnd_hz": 1000.0 * (2 ** (3.5 / 1200) - 1), "erb_1k": float(ear.erb(1000.0)),
            "clips": {"jnd": save("locking.jnd", jnd, level=LEVEL - 2, detail="two pairs of pure tones near 1000 Hz")}}


def harmonic(f0: float, numbers, seconds: float = 0.4) -> np.ndarray:
    return F.additive(f0, [1.0 if k in numbers else 0.0 for k in range(1, max(numbers) + 1)], seconds, SR)


def compute_pitch() -> dict:
    f0 = C3
    cases = {"pure": [1], "full": list(range(1, 9)), "upper": list(range(4, 9))}
    rows, acfs = [], {}
    for name, nums in cases.items():
        y = harmonic(f0, nums)
        p, sal = ear.pitch(y, SR)
        lags, s = ear.summary_acf(y, SR, max_lag=0.02)
        acfs[f"acf_{name}"] = s[::4]
        rows.append({"name": name, "partials": nums, "pitch": p, "cents": cents(p / f0), "salience": sal,
                     "level_at_f0_db": level_at(y[4800:], f0)})
    lags, _ = ear.summary_acf(harmonic(f0, [1]), SR, max_lag=0.02)
    # Schouten's shifted residue
    t = np.arange(int(0.4 * SR)) / SR
    shifted = sum(np.sin(2 * np.pi * (200.0 * k + 30.0) * t) for k in range(4, 9))
    p_shift = ear.pitch(shifted, SR, lo=120, hi=400)[0]
    plain_ = sum(np.sin(2 * np.pi * 200.0 * k * t) for k in range(4, 9))
    p_plain = ear.pitch(plain_, SR, lo=120, hi=400)[0]
    t2 = np.arange(int(1.4 * SR)) / SR
    shift_clip = concat([tone(sum(np.sin(2 * np.pi * (200.0 * k + d_) * t2) for k in range(4, 9))) for d_ in (0.0, 30.0)],
                        gap=0.35, names=["plain", "shifted"])
    # as sound: all eight partials; the top five; the top five over low noise; the fundamental alone
    secs = 1.5
    full, upper, pure = (harmonic(f0, cases[k], secs) for k in ("full", "upper", "pure"))
    noise = F.colored_noise(int(secs * SR), 0.0, SR, seed=4)
    spec = np.fft.rfft(noise)
    fr = np.fft.rfftfreq(len(noise), 1 / SR)
    spec[fr > 300] = 0
    low = np.fft.irfft(spec, len(noise))
    low = low / np.sqrt(np.mean(low ** 2)) * np.sqrt(np.mean(upper ** 2)) * 0.7
    parts = [tone(full).at_level(LEVEL), tone(upper).at_level(LEVEL)]
    gain = parts[1].mono.max() / np.abs(upper).max()
    parts += [tone((upper + low) * gain), tone(pure).at_level(LEVEL - 4)]
    seq = concat(parts, gap=0.35, names=["full", "upper", "noise", "pure"])
    masked_pitch = ear.pitch(upper + low, SR)[0]
    return {"f0": f0, "note": nearest_note(f0)[0], "rows": rows, "lags_ms": 1000 * lags[::4], **acfs, "period_ms": 1000 / f0,
            "shifted_pitch": p_shift, "shifted_formula": 200.0 + 30.0 / 6.0, "shifted_spacing": 200.0, "plain_pitch": p_plain,
            "shift_cents": cents(p_shift / p_plain), "shift_partials": [200.0 * k + 30.0 for k in range(4, 9)],
            "with_noise_pitch": masked_pitch, "jnd_cents": 3.5, "jnd_db": 1.0,
            "clips": {"missing": save("pitch.missing", seq, level=None, detail="one note, with less and less of its bottom"),
                      "shift": save("pitch.shift", shift_clip, detail="five partials 200 Hz apart; then all five moved up 30 Hz")}}


def compute_limit() -> dict:
    def pure_tune(tonic: float) -> Clip:
        return play_tune(lambda hz, dur, e: tone(F.additive(hz, [1.0], dur * 0.9, SR, attack=0.02), (0.01, 0.06)),
                         phrases=[0], tonic=tonic, tail=0.3, accent=0.0)

    normal, high = pure_tune(523.25), pure_tune(5274.0)
    seq = concat([normal.at_level(LEVEL - 3), high.at_level(LEVEL - 9)], gap=0.6, names=["normal", "high"])
    sal = load("locking")["rows"]
    return {"normal_hz": 523.25, "high_hz": 5274.0, "high_top_hz": 5274.0 * 5 / 3, "salience": sal, "piano_top_hz": 4186.0,
            "normal_notes": normal.notes, "clips": {"tune": save("limit.tune", seq, level=None,
                                                                 detail="pure tones: first near 500 Hz, then above 5,000 (high and thin)")}}


def compute_shepard() -> dict:
    steps = list(range(0, 25))
    parts = [Clip(ear.shepard(s, 0.42)) for s in steps]
    seq = concat(parts, gap=0.03, names=[f"s{s}" for s in steps])
    same = float(np.abs(ear.shepard(0.0) - ear.shepard(12.0)).max())
    # each step's partials: frequency and strength, for the picture
    table = []
    for s in range(13):
        row = []
        for k in range(9):
            f = 27.5 * 2 ** (k + (s % 12) / 12.0)
            row.append([f, math.exp(-0.5 * (math.log2(f / 440.0) / 1.6) ** 2)])
        table.append(row)
    return {"steps": steps, "same_as_start": same, "table": table,
            "clips": {"stairs": save("shepard.stairs", seq, detail="twenty-four steps up, and back where it began")}}


def compute_dose() -> dict:
    levels = [85, 88, 91, 94, 100, 106, 112]
    rows = [{"dba": v, "hours": ear.safe_hours(v)} for v in levels]
    places = [("a quiet library", 40), ("talking", 60), ("city traffic", 85), ("an orchestra, loud, on stage", 95),
              ("a club or a rock concert", 105), ("headphones at full volume", 105)]
    return {"rows": rows, "places": [{"name": n, "dba": v, "hours": ear.safe_hours(v)} for n, v in places],
            "plug_db": 20, "plug_factor": 2 ** (20 / 3)}


def compute_active() -> dict:
    force_db = np.arange(0, 101, 5.0)
    force = 10 ** (force_db / 20) * 1e-5
    active = ear.hopf_response(force, mu=0.0)
    passive = force / 1.0                                   # a damped oscillator with the same response at the top level
    passive = passive * active[-1] / passive[-1]
    out_a, out_p = 20 * np.log10(active / active[-1]), 20 * np.log10(passive / passive[-1])
    slope = float(np.polyfit(force_db, out_a, 1)[0])
    two = load("two")
    return {"in_db": force_db, "active_db": out_a, "passive_db": out_p, "slope": slope, "gain_at_threshold_db": float(out_a[0] - out_p[0]),
            "range_in": 100.0, "range_out": float(out_a[-1] - out_a[0]), "third_db": two["ear_third_db"],
            "q_passive": load("wave")["q_passive"], "q_active": load("wave")["q_active"]}


def compute_tune() -> dict:
    tonic = C3 * 2                                          # the octave above Part 1's string

    def missing(hz, dur, e):
        if e["phrase"] >= 4:                                # the last two phrases: no octave, only the note's class
            step = 12 * math.log2(hz / 27.5)
            return Clip(ear.shepard(step, dur * 0.95)).at_level(LEVEL - 1)
        decays = [1.2 + 0.5 * k for k in range(6)]
        y = F.additive(hz, [0, 0, 1.0, 0.8, 0.6, 0.45], dur + 0.25, SR, decays=decays, attack=0.008)
        return Clip(y).fade(0.002, 0.06).at_level(LEVEL)

    c = play_tune(missing, tonic=tonic, tail=0.8)
    checks, seen = [], set()
    for n in c.notes:
        if n["phrase"] >= 4 or n["name"] in seen:
            continue
        seen.add(n["name"])
        y = F.additive(n["hz"], [0, 0, 1.0, 0.8, 0.6, 0.45], 0.4, SR)
        p, sal = ear.pitch(y, SR, lo=100, hi=700)
        checks.append({"name": n["name"], "hz": n["hz"], "model": p, "cents_off": cents(p / n["hz"]),
                       "at_f0_db": level_at(y[4800:], n["hz"])})
    notes = [{**n, "kind": "shepard" if n["phrase"] >= 4 else "missing"} for n in c.notes]
    c = Clip(c.y, SR, c.events, notes)
    return {"clip": save("tune.variation4", c, detail="partials 3 to 6 only; then Shepard tones"), "notes": notes,
            "checks": checks, "seconds": c.duration, "worst_cents": max(abs(k["cents_off"]) for k in checks),
            "loudest_at_f0_db": max(k["at_f0_db"] for k in checks)}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 4, "title": r"with no fundamentals, then with no octaves: the notes the ear supplies",
            "seconds": t["seconds"],
            "measure": r"the pitch model finds every missing fundamental within a cent",
            "clip": "tune.variation4"}


def compute_nextpart() -> dict:
    def pair(ratio):
        a, b = string_note(0.5, 2.2), string_note(0.5 / ratio, 2.2)
        return mix([(a, 0.0), (b, 0.0)])

    seq = concat([pair(3 / 2).at_level(LEVEL), pair(45 / 32).at_level(LEVEL)], gap=0.4, names=["fifth", "tritone"])
    return {"ratios": [[3, 2], [45, 32]],
            "clips": {"pairs": save("next.pairs", seq, kind="physical model", level=None, detail="two strings together: lengths 2 to 3, then 32 to 45")}}


ITEMS = {"two": compute_two, "outer": compute_outer, "wave": compute_wave, "bands": compute_bands, "loud": compute_loud,
         "mask": compute_mask, "locking": compute_locking, "pitch": compute_pitch, "limit": compute_limit,
         "shepard": compute_shepard, "dose": compute_dose, "active": compute_active, "tune": compute_tune,
         "variation": compute_variation, "nextpart": compute_nextpart}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
