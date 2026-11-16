"""Precompute everything numerical, and every sound, in Part 51 of *Music, Built* ("Synthesis I: Oscillators and Filters").

    python -m videos.music.music51.compute              # everything missing (about two minutes)
    python -m videos.music.music51.compute --force hook

Numbers are cached in ``.cache/music51/<name>.json``, sounds in ``.cache/music51/audio/``.  The tools are Monochord's
(``explainer/music/monochord/synth.py``); the hi-hats are Part 40's six square waves (``monochord/song.py``).  Every
oscillator, filter, envelope and drum here is computed; no sampled instrument is played.

Items:
    hook        an ear question: a tone built from 40 sines by hand, and the two-oscillator patch a search found to match
                it, each playing the Tune's first phrase; which is the original?
    partials    a sawtooth built up from 1, 2, 3, 5, 10 and 40 sines
    organ       three Hammond registrations (8' alone, 888000000, all nine) playing the Tune's first phrase; the tempered
                drawbars' errors in cents
    waves       one cycle and the harmonic levels of the sawtooth, square, triangle and a 25 per cent pulse
    sweep       a sawtooth with a ladder low-pass opening and closing, without and with resonance; its spectrogram
    alias       aliasing measured for four sawtooths across six octaves; a naive and a PolyBLEP spectrum; PolyBLEP's
                correction drawn; an ear question (the Tune high up, naive and PolyBLEP: which aliased?)
    ladder      the linear ladder's responses; three ways of running its circuit against the equations at four rates;
                self-oscillation measured
    ladder3     a bass line through the ladder at three resonances
    drive       an ear question: the ladder's equations with every tanh removed, and the full circuit, driven hard
    sing        the filter alone, oscillating, playing the Tune's first phrase
    env         pluck, brass and pad envelopes on the Tune's first phrase
    mod         vibrato, tremolo and a filter wobble
    pwmsync     pulse-width modulation, then hard sync
    unison      a chord on one oscillator a note, then seven detuned ones
    table       eight wavetables and a scan through them; aliasing with and without band-limited tables
    drums       resonators struck: an 808-style kick, snare, clap and hats in a pattern; decay and chirp measured
    toms        the ladder struck near self-oscillation at three cutoffs: a filter as a drum
    fit         fitting a patch: a known patch recovered, the hook's target, the search landscape; an organ that no setting
                matches, heard
    tune51      Variation 51: the Tune switched on, four monophonic tracks recorded one at a time
    variation   the Variations ledger, row 51
"""

from __future__ import annotations

import numpy as np
from scipy.signal import resample_poly, stft

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import dynamics as D
from explainer.music.monochord import song as SONG
from explainer.music.monochord import synth as S
from explainer.music.monochord import tune as T
from explainer.music.monochord.partkit import saver

CACHE = Cache("music51")
CLIPS = ClipStore("music51")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="synthesized")
MAJOR = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
BEAT = 0.5


def C(y) -> Clip:
    return Clip(np.asarray(y, float), SR)


def hz(m: float) -> float:
    return 440.0 * 2 ** ((m - 69) / 12)


def tune_notes(phrases=(0,), base=60, beat=BEAT):
    return [(base + MAJOR[e["degree"]], e["t"], e["dur"]) for e in T.events(beat, list(phrases))]


def norm(y, peak=0.5):
    y = np.asarray(y, float)
    return peak * y / (np.max(np.abs(y)) + 1e-12)


def norm_rms(y, target=0.1):
    return y * target / (np.sqrt(np.mean(np.asarray(y) ** 2)) + 1e-12)


def fade(y, a=0.005, r=0.03):
    y = np.array(y, float)
    n = len(y)
    ka, kr = max(int(a * SR), 1), max(int(r * SR), 1)
    y[:ka] *= np.linspace(0, 1, ka)
    y[n - kr:] *= np.linspace(1, 0, kr)
    return y


# ---------------------------------------------------------------------------------------------------------- a voice
ENVS = {"pluck": dict(a=0.002, d=0.35, s=0.0, r=0.15), "brass": dict(a=0.06, d=0.3, s=0.7, r=0.15),
        "pad": dict(a=0.6, d=0.6, s=0.8, r=1.0), "organ": dict(a=0.005, d=0.05, s=1.0, r=0.05)}


def voice(m: float, dur: float, osc: str = "saw", cutoff: float = 2000.0, res: float = 0.0, env: str = "brass", fenv: float = 0.0,
          fenv_shape: str | None = None, width: float = 0.5, vibrato: float = 0.0, voices: int = 1, detune: float = 18.0, seed: int = 0,
          drive: float = 0.5) -> np.ndarray:
    """One note of a subtractive patch: oscillator, ladder low-pass (its cutoff raised by ``fenv`` octaves at the filter
    envelope's peak), amplifier envelope.  The note sounds for ``dur`` and then releases."""
    e = ENVS[env]
    n = int((dur + e["r"] * 1.2 + 0.02) * SR)
    t = np.arange(n) / SR
    f = hz(m) * 2 ** (vibrato / 1200 * np.sin(2 * np.pi * 5.5 * t) * np.clip((t - 0.25) / 0.3, 0, 1)) if vibrato else hz(m)
    if osc == "saw":
        x = S.unison(hz(m), n, voices, detune, seed=seed) if voices > 1 else S.saw_polyblep(f, n)
    elif osc == "pulse":
        x = S.pulse(f, width, n)
    elif osc == "mix":
        x = 0.6 * S.saw_polyblep(f, n) + 0.6 * S.pulse(f, width, n)
    elif osc == "naive":
        x = S.saw_naive(f, n)
    else:
        raise ValueError(osc)
    amp = S.adsr(n, SR, gate_s=dur, **e)
    if fenv:
        fe = S.adsr(n, SR, gate_s=dur, **ENVS[fenv_shape or env])
        fc = np.minimum(cutoff * 2 ** (fenv * fe), 18000.0)
    else:
        fc = cutoff
    y = S.ladder(drive * x, fc, res)
    return fade(y * amp, 0.001, 0.01)


def line(notes, **kw) -> np.ndarray:
    """A monophonic line of (midi, start, seconds) notes on one patch."""
    parts = [(C(voice(m, d * 0.95, seed=i, **kw)), a, 0.0) for i, (m, a, d) in enumerate(notes)]
    end = max(a + d for _, a, d in notes) + 1.5
    return mix(parts, duration=end).y


# ---------------------------------------------------------------------------------------------------------- items
def target_tone(f: float, n: int, seed: int = 7) -> np.ndarray:
    """The hook's original: forty sines, each set by hand to 1/k times a broad bump near 1.1 kHz and a roll-off above
    3 kHz, with random phases."""
    rng = np.random.default_rng(seed)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for k in range(1, 41):
        fk = k * f
        if fk > 20000:
            break
        a = (1 / k) * (1 + 2.5 * np.exp(-np.log2(fk / 1100) ** 2 / (2 * 0.35 ** 2))) / (1 + (fk / 3000) ** 4)
        y += a * np.sin(2 * np.pi * fk * t + rng.uniform(0, 2 * np.pi))
    return y / np.max(np.abs(y))


TARGET_AMPS_NOTE = "1/k, raised up to 3.5 times near 1.1 kHz, rolled off above 3 kHz"


def phrase_of(tone_fn, notes, env="brass"):
    parts = []
    for m, a, d in notes:
        e = ENVS[env]
        n = int((d * 0.95 + e["r"] * 1.2 + 0.02) * SR)
        parts.append((C(fade(tone_fn(hz(m), n) * S.adsr(n, SR, gate_s=d * 0.95, **e), 0.001, 0.01)), a, 0.0))
    return mix(parts, duration=max(a + d for _, a, d in notes) + 0.6).y


def compute_fit() -> dict:
    f = hz(60)
    tgt = target_tone(f, 8192)
    fit = S.fit_patch(tgt, f)
    known = S.patch(f, 8192, 1400.0, 2.0, 0.5)
    rec = S.fit_patch(known, f)
    org = S.drawbars(f, (8, 8, 8, 0, 0, 0, 0, 0, 0), 8192)
    ofit = S.fit_patch(org, f)
    def spec(y):
        return S.harmonic_levels(y, f).tolist()
    grid = [g for g in fit["grid"] if g[2] == fit["mix"]]
    out = {"f": f, "fit": {k: v for k, v in fit.items() if k != "grid"}, "recovered": {k: v for k, v in rec.items() if k != "grid"},
           "known": {"cutoff": 1400.0, "res": 2.0, "mix": 0.5}, "organ": {k: v for k, v in ofit.items() if k != "grid"},
           "slots": [f / 2 * j for j in range(1, len(spec(tgt)) + 1)], "spec": {"target": spec(tgt), "fit": spec(S.patch(f, 8192, fit["cutoff"], fit["res"], fit["mix"])),
                                                  "organ": spec(org), "organ_fit": spec(S.patch(f, 8192, ofit["cutoff"], ofit["res"], ofit["mix"]))},
           "grid": grid, "cutoffs": sorted({g[0] for g in grid}), "ress": sorted({g[1] for g in grid})}
    n = int(1.6 * SR)
    env = S.adsr(n, SR, gate_s=1.4, **ENVS["organ"])
    o = fade(S.drawbars(f, (8, 8, 8, 0, 0, 0, 0, 0, 0), n) * env)
    p = S.patch(f, n, ofit["cutoff"], ofit["res"], ofit["mix"]) * env
    c = concat([C(norm_rms(o)), C(norm_rms(fade(p)))], gap=0.8, names=["organ", "patch"])
    out["starts"] = {k: float(c.events[k]) for k in ("organ", "patch")}
    out["clips"] = {"organ": save("fit.organ", c, detail="middle C on a computed Hammond registration 888000000, then the closest note the two-oscillator patch can make")}
    return out


def compute_hook() -> dict:
    d = load("fit")
    fit = d["fit"]
    notes = tune_notes()
    orig = phrase_of(lambda f, n: target_tone(f, n), notes)
    patch = phrase_of(lambda f, n: S.patch(f, n, fit["cutoff"], fit["res"], fit["mix"]), notes)
    a, b = norm_rms(orig), norm_rms(patch)
    c = concat([C(b), C(a)], gap=1.0, names=["first", "second"])
    return {"answer": "second", "fit": fit, "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("hook.two", c, detail="the Tune's first phrase on a two-oscillator patch found by search (cutoff, resonance and mix), then on the tone it was matched to: forty sines set by hand")}}


def compute_partials() -> dict:
    ph = np.linspace(0, 2, 400)
    out = {"phase": ph.tolist()}
    for N in (1, 2, 3, 5, 10, 40):
        y = sum((-1) ** (k + 1) * np.sin(2 * np.pi * k * ph) / k for k in range(1, N + 1)) * 2 / np.pi
        out[str(N)] = y.tolist()
    return out


REGS = {"flute": (0, 0, 8, 0, 0, 0, 0, 0, 0), "smith": (8, 8, 8, 0, 0, 0, 0, 0, 0), "full": (8, 8, 8, 8, 8, 8, 8, 8, 8)}


def compute_organ() -> dict:
    notes = tune_notes(beat=0.42)
    clips = []
    for name, reg in REGS.items():
        y = phrase_of(lambda f, n, reg=reg: S.drawbars(f, reg, n), notes, env="organ")
        clips.append(C(norm_rms(y)))
    c = concat(clips, gap=0.7, names=list(REGS))
    cents = [1200 * np.log2(t / p) for t, p in zip(S.drawbar_ratios(True), S.DRAWBAR_RATIOS)]
    return {"regs": {k: list(v) for k, v in REGS.items()}, "names": list(S.DRAWBAR_NAMES), "ratios": list(S.DRAWBAR_RATIOS), "cents": cents,
            "starts": {k: float(c.events[k]) for k in REGS},
            "clips": {"three": save("organ.three", c, detail="the Tune's first phrase on a computed Hammond: the 8' drawbar alone, then 888000000, then all nine drawbars out")}}


def compute_waves() -> dict:
    ph = np.linspace(0, 2, 400)
    out = {"phase": ph.tolist(), "shapes": {}, "levels": {}}
    defs = {"saw": lambda k: (-1) ** (k + 1) / k, "square": lambda k: (1 / k if k % 2 else 0.0),
            "triangle": lambda k: ((-1) ** ((k - 1) // 2) / k ** 2 if k % 2 else 0.0),
            "pulse": lambda k: np.sin(np.pi * k * 0.25) / k}
    for name, amp in defs.items():
        y = sum(amp(k) * np.sin(2 * np.pi * k * ph) if name != "pulse" else amp(k) * np.cos(2 * np.pi * k * (ph - 0.125)) for k in range(1, 41))
        out["shapes"][name] = (y / np.max(np.abs(y))).tolist()
        a = np.array([abs(amp(k)) for k in range(1, 13)])
        out["levels"][name] = (20 * np.log10(np.maximum(a / a[0], 1e-6))).tolist()
    return out


def compute_sweep() -> dict:
    secs = 5.0
    n = int(secs * SR)
    t = np.arange(n) / SR
    x = S.saw_polyblep(hz(45), n)
    fc = 150 * (6000 / 150) ** np.where(t < secs / 2, t / (secs / 2), (secs - t) / (secs / 2))
    a = S.ladder(0.5 * x, fc, 0.0)
    b = S.ladder(0.5 * x, fc, 3.6)
    a, b = fade(norm_rms(a)), fade(norm_rms(b))
    c = concat([C(a), C(b)], gap=0.8, names=["plain", "resonant"])
    f, tt, Z = stft(b, SR, nperseg=2048, noverlap=2048 - 1200)
    P = 20 * np.log10(np.abs(Z) + 1e-9)
    rows = np.geomspace(60, 12000, 110)
    spec = np.array([np.interp(rows, f, P[:, j]) for j in range(P.shape[1])]).T
    spec -= spec.max()
    return {"seconds": secs, "f0": hz(45), "fc": fc[::480].tolist(), "spec": spec.tolist(), "rows": rows.tolist(),
            "starts": {"plain": float(c.events["plain"]), "resonant": float(c.events["resonant"])},
            "clips": {"two": save("sweep.two", c, detail="a 110 Hz sawtooth through the ladder low-pass, its cutoff swept from 150 Hz to 6 kHz and back, first without resonance, then with feedback 3.6")}}


ALIAS_F = (110.0, 220.0, 440.0, 880.0, 1760.0, 3520.0)


def peaks(y, top=24000.0, bins=480):
    Y = 20 * np.log10(np.abs(np.fft.rfft(y * np.hanning(len(y)))) + 1e-9)
    f = np.fft.rfftfreq(len(y), 1 / SR)
    Y -= Y.max()
    edges = np.linspace(0, top, bins + 1)
    return [float(Y[(f >= a) & (f < b)].max()) for a, b in zip(edges[:-1], edges[1:])]


def compute_alias() -> dict:
    n = SR
    curves = {name: [D.alias_energy(fn(f, n), f, SR) for f in ALIAS_F]
              for name, fn in (("naive", S.saw_naive), ("polyblep", S.saw_polyblep), ("blit", S.saw_blit), ("additive", S.saw_additive))}
    curves["polyblep2"] = [D.alias_energy(resample_poly(S.saw_polyblep(f, 2 * n, 2 * SR), 1, 2), f, SR) for f in ALIAS_F]
    f0 = hz(98)
    spec = {"naive": peaks(S.saw_naive(f0, n)), "polyblep": peaks(S.saw_polyblep(f0, n))}
    fs = SR / 12
    k = np.arange(25)
    ph = (k / 12.0 + 0.5 / 12) % 1.0
    blep = {"naive": (2 * ph - 1).tolist(), "polyblep": (2 * ph - 1 - S._polyblep(ph, np.full(len(ph), 1 / 12))).tolist()}
    notes = tune_notes(base=84, beat=0.42)
    a = line(notes, osc="naive", cutoff=18000.0, env="organ", drive=0.3)
    b = line(notes, osc="saw", cutoff=18000.0, env="organ", drive=0.3)
    c = concat([C(norm_rms(a)), C(norm_rms(b))], gap=1.0, names=["first", "second"])
    return {"answer": "first", "freqs": list(ALIAS_F), "curves": curves, "f0": f0, "spec": spec, "harm": [float(f0 * j) for j in range(1, int(24000 / f0) + 1)],
            "blep": blep, "blep_f": fs,
            "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("alias.two", c, detail="the Tune's first phrase two octaves above middle C on a naive digital sawtooth, then on a PolyBLEP sawtooth; no filter")}}


def err_db(y, z):
    return float(10 * np.log10(np.sum((y - z) ** 2) / np.sum(z ** 2)))


def compute_ladder() -> dict:
    f = np.geomspace(20, 20000, 220)
    resp = {str(k): S.ladder_response(1000.0, k, f).tolist() for k in (0.0, 1.0, 2.0, 3.0, 3.8)}
    x = S.saw_polyblep(220.0, 4800)
    ref = S.ladder_ode(x, 1500.0, 3.0)
    rates = (1, 2, 4, 8)
    conv = {"forward": [err_db(S.ladder(x, 1500.0, 3.0, oversample=r, half=False), ref) for r in rates],
            "corrected": [err_db(S.ladder(x, 1500.0, 3.0, oversample=r, half=True), ref) for r in rates],
            "trapezoid": [err_db(S.ladder_trap(x, 1500.0, 3.0, oversample=r), ref) for r in rates]}
    imp = np.zeros(SR)
    imp[0] = 0.01
    osc = {}
    for fc in (220.0, 440.0, 880.0):
        y = S.ladder(imp, fc, 4.3)[SR // 2:]
        zc = np.where((y[:-1] < 0) & (y[1:] >= 0))[0]
        osc[str(int(fc))] = float((len(zc) - 1) / ((zc[-1] - zc[0]) / SR))
    peak = {}
    for k in (3.0, 3.8):
        r = np.array(resp[str(k)])
        i = int(np.argmax(r))
        peak[str(k)] = {"f": float(f[i]), "db": float(r[i])}
    import time
    noise = np.random.default_rng(0).standard_normal(SR) * 0.3
    S.ladder(noise[:64], 1000.0, 3.0, oversample=1, half=False)
    S.ladder_trap(noise[:64], 1000.0, 3.0)
    ta, tb = [], []
    for _ in range(3):
        t0 = time.perf_counter()
        S.ladder(noise, 1000.0, 3.0, oversample=1, half=False)
        ta.append(time.perf_counter() - t0)
        t0 = time.perf_counter()
        S.ladder_trap(noise, 1000.0, 3.0)
        tb.append(time.perf_counter() - t0)
    cost = float(min(tb) / min(ta))
    snap = {"x": x[:480:2].tolist(), "ref": ref[:480:2].tolist(), "fwd": S.ladder(x, 1500.0, 3.0, oversample=1, half=False)[:480:2].tolist()}
    return {"f": f.tolist(), "resp": resp, "rates": list(rates), "conv": conv, "osc": osc, "peak": peak, "dc": {str(k): float(-20 * np.log10(1 + k)) for k in (0, 1, 2, 3, 3.8)},
            "snap": snap, "cost": cost}


def compute_ladder3() -> dict:
    notes = [(m - 24, a, d) for m, a, d in tune_notes(beat=0.36)]
    names = ["k0", "k2", "k37"]
    ys = [line(notes, osc="saw", cutoff=500.0, res=k, env="pluck", fenv=2.0, drive=0.8) for k in (0.0, 2.0, 3.7)]
    c = concat([C(norm_rms(y)) for y in ys], gap=0.7, names=names)
    return {"res": [0.0, 2.0, 3.7], "starts": {k: float(c.events[k]) for k in names},
            "clips": {"three": save("ladder.three", c, detail="the Tune's first phrase two octaves below middle C on a sawtooth through the ladder (500 Hz, opened two octaves by a pluck envelope) with feedback 0, 2 and 3.7")}}


def compute_drive() -> dict:
    notes = [(m - 12, a, d) for m, a, d in tune_notes(beat=0.42)]
    parts_lin, parts_nl = [], []
    for i, (m, a, d) in enumerate(notes):
        n = int((d + 0.2) * SR)
        x = S.saw_polyblep(hz(m), n) * S.adsr(n, SR, gate_s=d * 0.95, **ENVS["brass"])
        parts_lin.append((C(fade(S.ladder(3.0 * x, 900.0, 3.2, nonlinear=False))), a, 0.0))
        parts_nl.append((C(fade(S.ladder(3.0 * x, 900.0, 3.2))), a, 0.0))
    end = notes[-1][1] + notes[-1][2] + 0.5
    lin = mix(parts_lin, duration=end).y
    nl = mix(parts_nl, duration=end).y
    h_lin = D.harmonics(S.ladder(3.0 * S.saw_polyblep(220.0, SR), 900.0, 3.2, nonlinear=False), 220.0, SR, 8)
    h_nl = D.harmonics(S.ladder(3.0 * S.saw_polyblep(220.0, SR), 900.0, 3.2), 220.0, SR, 8)
    c = concat([C(norm_rms(lin)), C(norm_rms(nl))], gap=1.0, names=["first", "second"])
    return {"answer": "second", "h_lin": h_lin, "h_nl": h_nl, "starts": {"first": float(c.events["first"]), "second": float(c.events["second"])},
            "clips": {"two": save("drive.two", c, detail="the Tune's first phrase on a sawtooth driven hard into the ladder (900 Hz, feedback 3.2): first the equations with every tanh removed, then the full circuit; matched in loudness")}}


def compute_sing() -> dict:
    notes = tune_notes(beat=0.5)
    end = notes[-1][1] + notes[-1][2] + 0.3
    n = int(end * SR)
    t = np.arange(n) / SR
    imp = np.zeros(n)
    imp[0] = 0.01
    ratio = load("ladder")["osc"]["440"] / 440.0
    fc = np.full(n, hz(notes[0][0]) / ratio)
    gate = np.zeros(n)
    for m, a, d in notes:
        i0, i1 = int(a * SR), int((a + d) * SR)
        fc[i0:] = hz(m) / ratio
        gate[i0:i1] = 1.0
    y = S.ladder(imp, fc, 4.3)
    sm = np.convolve(gate, np.hanning(int(0.03 * SR)) / np.hanning(int(0.03 * SR)).sum(), mode="same")
    y = fade(y * (0.15 + 0.85 * sm), 0.01, 0.1)
    c = concat([C(norm(y))], names=["sing"])
    return {"ratio": ratio, "notes": [list(nn) for nn in notes],
            "clips": {"one": save("sing.one", c, detail="no oscillator: the ladder alone, its feedback at 4.3 so that it oscillates, its cutoff stepped through the Tune's first phrase")}}


def compute_env() -> dict:
    notes = tune_notes(beat=0.5)
    names = ["pluck", "brass", "pad"]
    ys = [line(notes, osc="saw", cutoff=400.0, res=1.5, env=e, fenv=3.0, drive=0.5) for e in names]
    c = concat([C(norm_rms(y)) for y in ys], gap=0.7, names=names)
    n = int(2.0 * SR)
    curves = {e: S.adsr(n, SR, gate_s=1.0, **ENVS[e])[::400].tolist() for e in names}
    return {"envs": ENVS, "curves": curves, "dt": 400 / SR, "starts": {k: float(c.events[k]) for k in names},
            "clips": {"three": save("env.three", c, detail="the Tune's first phrase on one sawtooth patch (ladder at 400 Hz, opened three octaves by the envelope) with a pluck, a brass and a pad envelope")}}


def compute_mod() -> dict:
    secs = 3.0
    n = int(secs * SR)
    t = np.arange(n) / SR
    f0 = hz(48)
    amp = S.adsr(n, SR, gate_s=secs - 0.2, a=0.02, d=0.2, s=0.9, r=0.15)
    vib = S.ladder(0.5 * S.saw_polyblep(f0 * 2 ** (30 / 1200 * np.sin(2 * np.pi * 5.5 * t)), n), 1800.0, 1.0) * amp
    trem = S.ladder(0.5 * S.saw_polyblep(f0, n), 1800.0, 1.0) * amp * (1 - 0.7 * (0.5 + 0.5 * np.sin(2 * np.pi * 6.0 * t)))
    lfo = 0.5 - 0.5 * np.cos(2 * np.pi * 3.0 * t)
    wob = S.ladder(0.5 * S.saw_polyblep(f0 / 2, n), 150 * (3000 / 150) ** lfo, 3.2) * amp
    names = ["vibrato", "tremolo", "wobble"]
    c = concat([C(fade(norm_rms(v))) for v in (vib, trem, wob)], gap=0.7, names=names)
    tt = t[: int(1.0 * SR):240]
    return {"t": tt.tolist(), "vib": (30 * np.sin(2 * np.pi * 5.5 * tt)).tolist(), "trem": (1 - 0.7 * (0.5 + 0.5 * np.sin(2 * np.pi * 6.0 * tt))).tolist(),
            "wob": (150 * (3000 / 150) ** (0.5 - 0.5 * np.cos(2 * np.pi * 3.0 * tt))).tolist(), "starts": {k: float(c.events[k]) for k in names},
            "clips": {"three": save("mod.three", c, detail="one held sawtooth patch: pitch moved by a 5.5 Hz LFO (vibrato), level moved at 6 Hz (tremolo), then an octave lower with the cutoff swept three times a second (a wobble)")}}


def compute_pwmsync() -> dict:
    secs = 4.0
    n = int(secs * SR)
    t = np.arange(n) / SR
    f0 = hz(48)
    w = 0.5 - 0.42 * (0.5 - 0.5 * np.cos(2 * np.pi * 0.5 * t))
    amp = S.adsr(n, SR, gate_s=secs - 0.2, a=0.02, d=0.2, s=0.9, r=0.15)
    pwm = S.ladder(0.5 * S.pulse(f0, w, n), 4000.0, 0.5) * amp
    os = 4
    ts = np.arange(n * os) / (SR * os)
    slave = f0 * (1 + 4 * (0.5 - 0.5 * np.cos(2 * np.pi * ts / secs)))
    sync = resample_poly(S.sync_saw(f0, slave, n * os, SR * os), 1, os)[:n]
    sync = S.ladder(0.4 * sync, 5000.0, 0.5) * amp
    c = concat([C(fade(norm_rms(pwm))), C(fade(norm_rms(sync)))], gap=0.8, names=["pwm", "sync"])
    widths = {}
    for wd in (0.5, 0.25, 0.1):
        a = np.array([abs(np.sin(np.pi * k * wd)) / k for k in range(1, 21)])
        widths[str(wd)] = (20 * np.log10(np.maximum(a / a.max(), 1e-4))).tolist()
    snaps = {}
    for r in (1.5, 2.5, 3.7):
        m = 2 * 400
        snaps[str(r)] = S.sync_saw(1.0, np.full(m, r), m, 400.0).tolist()
    ph = np.linspace(0, 2, 400)
    master = ((ph % 1.0) * 2 - 1).tolist()
    return {"widths": widths, "snaps": snaps, "master": master, "starts": {"pwm": float(c.events["pwm"]), "sync": float(c.events["sync"])},
            "clips": {"two": save("pwmsync.two", c, detail="a pulse wave whose width swings from 50 to 8 per cent and back (PWM); then a sawtooth hard-synced to C3, its own frequency swept from one to five times C3")}}


def compute_unison() -> dict:
    keys = [48, 52, 55, 60]
    secs = 3.0
    n = int(secs * SR)
    amp = S.adsr(n, SR, gate_s=secs - 0.3, a=0.05, d=0.3, s=0.85, r=0.25)
    one = sum(S.ladder(0.3 * S.saw_polyblep(hz(m), n), 5000.0, 0.3) for m in keys) * amp
    seven = sum(S.ladder(0.3 * S.unison(hz(m), n, 7, 18.0, seed=m), 5000.0, 0.3) for m in keys) * amp
    c = concat([C(fade(norm_rms(one))), C(fade(norm_rms(seven)))], gap=0.8, names=["one", "seven"])
    f8 = 8 * hz(48)
    lines = [f8 * 2 ** ((18 * (2 * v / 6 - 1)) / 1200) for v in range(7)]
    return {"keys": keys, "f8": f8, "lines": lines, "beat_hz": lines[-1] - lines[0], "starts": {"one": float(c.events["one"]), "seven": float(c.events["seven"])},
            "clips": {"two": save("unison.two", c, detail="a C major chord on one sawtooth a note, then on seven a note spread over 36 cents (a supersaw)")}}


def compute_table() -> dict:
    tabs = S.make_tables()
    secs = 5.0
    n = int(secs * SR)
    t = np.arange(n) / SR
    pos = np.where(t < secs / 2, t / (secs / 2), (secs - t) / (secs / 2))
    amp = S.adsr(n, SR, gate_s=secs - 0.2, a=0.05, d=0.2, s=0.9, r=0.15)
    y = S.wavetable(hz(48), tabs, pos, n) * amp
    c = concat([C(fade(norm_rms(y)))], names=["scan"])
    f6 = hz(84)
    full = S.wavetable(f6, tabs, 1.0, SR)
    keep = int(20000 // f6)
    lim = S.make_tables(harmonics=keep)
    limited = S.wavetable(f6, lim, 1.0, SR)
    levels = {}
    for p in (0.0, 0.5, 1.0):
        levels[str(p)] = D.harmonics(S.wavetable(hz(48), tabs, p, SR), hz(48), SR, 16)
    return {"tables": tabs[:, ::16].tolist(), "levels": levels, "f6": f6, "keep": keep,
            "alias": {"full": D.alias_energy(full, f6, SR), "limited": D.alias_energy(limited, f6, SR)},
            "clips": {"scan": save("table.scan", c, detail="a held C3 read from eight stored single cycles, scanned from the sine to the brightest and back over five seconds")}}


def compute_drums() -> dict:
    kick = S.kick_circuit()
    env = np.abs(kick)
    blocks = env[: int(0.9 * SR)].reshape(-1, 480).max(axis=1)
    tb = (np.arange(len(blocks)) + 0.5) * 0.01
    sel = (tb > 0.1) & (tb < 0.8)
    slope = np.polyfit(tb[sel], np.log(blocks[sel]), 1)[0]
    tau = float(-1 / slope)
    seg = kick[: int(0.12 * SR)]
    zc = np.where((seg[:-1] < 0) & (seg[1:] >= 0))[0] / SR
    inst = (1 / np.diff(zc)).tolist()
    snare = S.snare_circuit()
    clap = S.clap_circuit()
    hat = SONG.hat808(False)
    ohat = SONG.hat808(True)
    bpm = 100
    step = 60 / bpm / 4
    pat = {"kick": [0, 3, 8, 10], "snare": [4, 12], "clap": [12], "hat": [0, 2, 4, 6, 8, 10, 12, 14], "ohat": [14]}
    sounds = {"kick": (kick, 0.0), "snare": (snare, -4.0), "clap": (clap, -6.0), "hat": (hat, -12.0), "ohat": (ohat, -14.0)}
    parts = []
    for b in range(4):
        for name, steps in pat.items():
            y, g = sounds[name]
            for s in steps:
                if name == "ohat" and b % 2 == 0:
                    continue
                parts.append((C(y), (16 * b + s) * step, g))
    kit = mix(parts, duration=64 * step + 1.0).y
    c = concat([C(norm(kit, 0.6))], names=["kit"])
    return {"tau": tau, "tau_theory": 2 * 74.0 / (2 * np.pi * 52.0), "chirp": inst[:12], "q": 74.0, "f": 52.0,
            "kick": kick[: int(0.4 * SR):96].tolist(), "clap_env": (np.abs(clap[: int(0.06 * SR)]).reshape(-1, 48).max(axis=1)).tolist(),
            "pattern": pat, "bpm": bpm, "hats": list(SONG.HAT_HZ), "starts": {"kit": 0.0},
            "clips": {"kit": save("drums.kit", c, detail="four bars at 100 beats a minute: a struck resonator as the kick, two resonators and noise as the snare, three noise bursts as the clap, Part 40's six square waves as the hats")}}


def compute_toms() -> dict:
    names = ["low", "mid", "high"]
    out, clips = {}, []
    for name, fc in zip(names, (80.0, 125.0, 190.0)):
        n = int(1.0 * SR)
        x = np.zeros(n)
        x[: int(0.002 * SR)] = 3.0
        y = S.ladder(x, fc, 3.9)
        env = np.abs(y)[: int(0.8 * SR)].reshape(-1, 480).max(axis=1)
        tb = (np.arange(len(env)) + 0.5) * 0.01
        sel = (tb > 0.05) & (tb < 0.6) & (env > 1e-6)
        zc = np.where((y[:-1] < 0) & (y[1:] >= 0))[0] / SR
        fz = 1 / np.diff(zc)
        out[name] = {"fc": fc, "tau": float(-1 / np.polyfit(tb[sel], np.log(env[sel]), 1)[0]), "start_hz": float(fz[0]), "end_hz": float(fz[-1])}
        clips.append(C(fade(norm(y), 0.0005, 0.05)))
    parts = []
    seq = [0, 0, 1, 1, 2, 2, 1, 0]
    for i, s in enumerate(seq):
        parts.append((clips[s], i * 0.3, 0.0))
    roll_ = mix(parts, duration=8 * 0.3 + 1.0)
    c = concat([*clips, roll_], gap=0.5, names=names + ["roll"])
    return {**out, "starts": {k: float(c.events[k]) for k in names + ["roll"]},
            "clips": {"three": save("toms.three", c, needs="headphones or bass-capable speakers", detail="the ladder filter alone, feedback 3.9, struck by a 2 ms pulse at cutoffs 80, 125 and 190 Hz; then a fill on the three")}}


# ---------------------------------------------------------------------------------------------------------- Variation 51
CHORDS = {0: ["I", "I", "IV", "I"], 1: ["IV", "I", "V", "I"], 2: ["I", "IV", "I", "V"], 3: ["I", "IV", "I", "V"], 4: ["I", "I", "IV", "I"], 5: ["IV", "I", "V", "I"]}
ROOTS = {"I": 0, "IV": 5, "V": 7}
TRIADS = {"I": (0, 4, 7), "IV": (5, 9, 12), "V": (7, 11, 14)}


def compute_tune51() -> dict:
    beat = 0.36
    lead = tune_notes(phrases=range(6), base=72, beat=beat)
    bass, arp, pad = [], [], []
    for p in range(6):
        for j, ch in enumerate(CHORDS[p]):
            t0 = (8 * p + 2 * j) * beat
            r = 36 + ROOTS[ch]
            for i, iv in enumerate((0, 7, 12, 7)):
                bass.append((r + iv, t0 + i * beat / 2, beat / 2))
            tri = TRIADS[ch]
            seq = [60 + tri[0], 60 + tri[1], 60 + tri[2], 72 + tri[0], 60 + tri[2], 60 + tri[1], 60 + tri[0], 60 + tri[1]]
            for i, m in enumerate(seq):
                arp.append((m, t0 + i * beat / 4, beat / 4))
            pad.append(([48 + v for v in tri], t0, 2 * beat))
    tracks = {}
    tracks["lead"] = line(lead, osc="mix", cutoff=700.0, res=1.2, env="brass", fenv=2.5, vibrato=18.0, width=0.3, drive=0.45)
    tracks["bass"] = line(bass, osc="pulse", width=0.5, cutoff=300.0, res=2.0, env="pluck", fenv=2.5, drive=0.7)
    tracks["arp"] = line(arp, osc="pulse", width=0.2, cutoff=1500.0, res=1.0, env="pluck", fenv=1.5, drive=0.4)
    pparts = []
    for keys, a, d in pad:
        y = sum(voice(m, d, osc="saw", voices=5, detune=12.0, cutoff=1400.0, res=0.4, env="pad", seed=m) for m in keys)
        pparts.append((C(y), a, 0.0))
    tracks["pad"] = mix(pparts, duration=48 * beat + 2.5).y
    gains = {"lead": 0.0, "bass": -3.0, "arp": -11.0, "pad": -12.0}
    pans = {"lead": 0.0, "bass": 0.0, "arp": 0.45, "pad": -0.35}
    L = max(len(v) for v in tracks.values())
    full = mix([(C(norm_rms(np.r_[v, np.zeros(L - len(v))])), 0.0, gains[k], pans[k]) for k, v in tracks.items()], duration=L / SR)
    solo = C(norm_rms(tracks["lead"][: int(8 * beat * SR + 0.5 * SR)]))
    c = concat([solo, full], gap=0.8, names=["solo", "full"])
    al_pb, al_nv = [], []
    for m in sorted({mm for mm, _, _ in lead}):
        al_pb.append(D.alias_energy(S.saw_polyblep(hz(m), SR), hz(m), SR))
        al_nv.append(D.alias_energy(S.saw_naive(hz(m), SR), hz(m), SR))
    nnotes = len(lead) + len(bass) + len(arp) + len(pad)
    return {"beat": beat, "lead": [list(x) for x in lead], "bass": [list(x) for x in bass], "arp": [list(x) for x in arp],
            "pad": [[k, a, d] for k, a, d in pad], "notes": nnotes, "counts": {"lead": len(lead), "bass": len(bass), "arp": len(arp), "pad": len(pad)},
            "alias_pb": float(np.mean(al_pb)), "alias_naive": float(np.mean(al_nv)), "seconds": c.duration,
            "starts": {"solo": float(c.events["solo"]), "full": float(c.events["full"])},
            "clips": {"variation51": save("tune.variation51", c, detail="the Tune's first phrase on a lead patch alone; then the whole Tune switched on: lead, a pulse bass, a pulse arpeggio and a supersaw pad, each line played one at a time on one patch, then mixed")}}


def compute_variation() -> dict:
    t = load("tune51")
    return {"part": 51, "title": "switched on: four monophonic tracks, one patch each", "seconds": round(t["seconds"], 1),
            "measure": f"{t['notes']} notes on four tracks; the lead's aliasing {-t['alias_pb']:.0f} dB below its harmonics, {-t['alias_naive']:.0f} if naive",
            "clip": "tune.variation51"}


ITEMS = {"fit": compute_fit, "hook": compute_hook, "partials": compute_partials, "organ": compute_organ, "waves": compute_waves,
         "sweep": compute_sweep, "alias": compute_alias, "ladder": compute_ladder, "ladder3": compute_ladder3, "drive": compute_drive,
         "sing": compute_sing, "env": compute_env, "mod": compute_mod, "pwmsync": compute_pwmsync, "unison": compute_unison,
         "table": compute_table, "drums": compute_drums, "toms": compute_toms, "tune51": compute_tune51, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
