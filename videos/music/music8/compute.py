"""Precompute everything numerical, and every sound, in Part 8 of *Music, Built* ("Pipes, Reeds and Voices").

    python -m videos.music.music8.compute              # everything missing (about two minutes)
    python -m videos.music.music8.compute --force reed

Numbers are cached in ``.cache/music8/<name>.json`` (+ ``.npz``), sounds in ``.cache/music8/audio/``.  The
instruments are Monochord's (``explainer/music/monochord/instruments/winds.py``); published values are cited in the
README.

Items:
    hook        a flute and a clarinet of the same length; one voice, two notes
    column      the resonances of a pipe open at both ends and of one closed at one end, from their impedance
    reed        the reed's flow curve; a clarinet's mouthpiece pressure; what happens as the player blows harder
    holes       a tone hole against a cut tube; the register hole and the twelfth
    cone        a cylinder and a cone with a reed: resonances, spectra, and the same note on both
    lips        a trumpet's shape and resonances; which note the lips pick; a call on one length of tube
    jet         a flute's registers against blowing pressure; overblowing; an organ's stops as a sum
    voice       the pulses of the folds, the filter of the tract, three vowels
    vowels      formants of tubes: neutral, and two-tube shapes for 'ah' and 'ee'; the vowel chart; a quiz
    singers     the singer's formant; a soprano's tuned resonance; overtone singing
    tune        Variation 8: the Tune for a flute, a clarinet, a saxophone, a trumpet and a voice
    variation   the Variations ledger, row 8
"""

from __future__ import annotations

import math
from functools import lru_cache

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord.instruments import winds as W
from explainer.music.monochord.partkit import play_tune, saver
from explainer.music.monochord.pitch import cents

CACHE = Cache("music8")
CLIPS = ClipStore("music8")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
C3, C4, C5 = 130.8127826502993, 261.6255653005986, 523.2511306011972
PIPE = 0.60                 # metres: the length of the hook's two pipes
R_CLAR, R_FLUTE = 0.0075, 0.0095


def clip(y, fade=(0.01, 0.06)) -> Clip:
    return Clip(np.asarray(y, dtype=np.float64)).fade(*fade)


def levels(y, tail=0.3) -> dict:
    return W.playing(np.asarray(y, dtype=float), SR, tail)


# ---------------------------------------------------------------------------
# The instruments, each tuned by playing it: a bore is made, blown, measured and trimmed until it sounds the note
# ---------------------------------------------------------------------------
def _trim(make, blow, hz: float, guess: float, rounds: int = 2) -> float:
    length = guess
    for _ in range(rounds):
        got = levels(blow(make(length)), 0.2)["hz"]
        if got <= 0:
            break
        length *= got / hz
    return length


@lru_cache(maxsize=None)
def clarinet_length(hz: float) -> float:
    return _trim(lambda L: W.cylinder(L, R_CLAR), lambda b: W.reed_tone(b, 0.45, 0.5)["p"], hz, W.C / (4 * hz) - 0.6133 * R_CLAR)


@lru_cache(maxsize=None)
def sax_length(hz: float) -> float:
    return _trim(lambda L: W.saxophone(L), lambda b: W.reed_tone(b, 0.45, 0.5, zeta=0.9)["p"], hz, 0.60 * 233.0 / hz)


@lru_cache(maxsize=None)
def trumpet_tube(hz: float) -> float:
    """The length of tubing for which the horn's third resonance, as the lips play it, is hz.  First the resonance
    itself is put a little below the note (lips sound slightly above a resonance), then the horn is blown and
    trimmed, as long as it is sounding the right resonance."""
    fixed = 0.56 + 0.082

    def third(tube):
        return W.trumpet(tube=tube).peaks(1.6 * hz, df=0.5)[2][0]

    tube = fixed + (1.37 - fixed) * 348.0 / hz
    for _ in range(4):
        tube = fixed + (tube - fixed) * third(tube) / (hz / 1.012)
    for _ in range(2):
        got = levels(W.lip_tone(W.trumpet(tube=tube), hz / 1.3, 0.5)["p"], 0.2)["hz"]
        if got <= 0 or abs(cents(got / hz)) > 80:
            break
        tube = fixed + (tube - fixed) * got / hz
    return tube


def flute(hz: float, seconds: float, pressure=1.0) -> np.ndarray:
    return W.jet_tone(hz, seconds, pressure)


def clarinet(hz: float, seconds: float, gamma=0.45) -> np.ndarray:
    return W.reed_tone(W.cylinder(clarinet_length(round(hz, 3)), R_CLAR), gamma, seconds)["sound"]


def saxophone(hz: float, seconds: float, gamma=0.45) -> np.ndarray:
    return W.reed_tone(W.saxophone(sax_length(round(hz, 3))), gamma, seconds, zeta=0.9)["sound"]


def trumpet(hz: float, seconds: float) -> np.ndarray:
    return W.lip_tone(W.trumpet(tube=trumpet_tube(round(hz, 3))), hz / 1.3, seconds)["sound"]


def sung(hz: float, seconds: float, vowel="a", vibrato: float = 25.0, formants=None, **kw) -> np.ndarray:
    """A sung vowel with a singer's slow start and vibrato (cents, at 5.5 Hz, arriving after a third of a second)."""
    n = int(seconds * SR)
    t = np.arange(n) / SR
    onset = np.clip((t - 0.3) / 0.4, 0, 1)
    f0 = hz * 2 ** (onset * vibrato / 1200.0 * np.sin(2 * np.pi * 5.5 * t))
    return W.voice(f0, formants if formants is not None else W.VOWELS[vowel], seconds, **kw)


def overtone_voice(drone: float, harmonics, durs, glide: float = 0.05) -> tuple[np.ndarray, list[float]]:
    """One held note and a second one above it: the tract's second and third resonances are drawn together onto one
    harmonic of the drone at a time."""
    n = int(sum(durs) * SR)
    f1, f2, f3 = np.empty(n), np.empty(n), np.empty(n)
    starts, i = [], 0
    for h, d in zip(harmonics, durs):
        a, b, c = W.overtone_formants(h, drone)
        m = int(d * SR)
        f1[i: i + m], f2[i: i + m], f3[i: i + m] = a, b, c
        starts.append(i / SR)
        i += m
    f1[i:], f2[i:], f3[i:] = f1[i - 1], f2[i - 1], f3[i - 1]
    w = int(glide * SR)
    k = np.ones(w) / w
    sm = lambda x: np.convolve(np.pad(x, (w, w), mode="edge"), k, mode="same")[w:-w]     # noqa: E731
    y = W.voice(drone, [sm(f1), sm(f2), sm(f3)], n / SR, bandwidths=[90.0, 35.0, 35.0, 250.0, 300.0], jitter=0.002)
    return y, starts


# ---------------------------------------------------------------------------
def compute_hook() -> dict:
    fl_bore, cl_bore = W.cylinder(PIPE, R_FLUTE), W.cylinder(PIPE, R_CLAR)
    f_flute = fl_bore.peaks(600, admittance=True)[0][0]
    yf = flute(f_flute, 2.2)
    d = W.reed_tone(cl_bore, 0.45, 2.2)
    a, b = levels(yf), levels(d["p"])
    seq = concat([clip(yf).at_level(LEVEL), clip(d["sound"]).at_level(LEVEL)], gap=0.5, names=["flute", "clarinet"])
    harm = [8, 9, 10, 12, 10, 9, 8]
    yo, starts = overtone_voice(C3, harm, [0.9, 0.55, 0.55, 0.9, 0.55, 0.55, 1.2])
    over = clip(yo, (0.05, 0.25)).at_level(LEVEL)
    over = Clip(over.y, SR, {f"n{k}": t for k, t in enumerate(starts)})
    return {"length": PIPE, "flute_hz": a["hz"], "clarinet_hz": b["hz"], "interval_cents": cents(a["hz"] / b["hz"]),
            "flute_db": a["harmonics_db"], "clarinet_db": levels(d["sound"])["harmonics_db"], "clarinet_inside_db": b["harmonics_db"],
            "drone": C3, "harmonics": harm, "overtone_hz": [h * C3 for h in harm],
            "clips": {"pair": save("hook.pair", seq, level=None, detail="two pipes 60 cm long: blown across the end, and blown through a reed"),
                      "overtone": save("hook.overtone", over, kind="synthesized", level=None, detail="a model voice: one held note, and its overtones picked out one at a time")}}


def compute_column() -> dict:
    f = np.arange(40.0, 2000.0, 1.0)
    stopped, open_ = W.cylinder(PIPE, R_CLAR), W.cylinder(PIPE, R_FLUTE)
    z = np.abs(stopped.impedance(f))
    y = 1.0 / np.abs(open_.impedance(f))
    ps, po = stopped.peaks(2000), open_.peaks(2000, admittance=True)
    flute_len = 0.66
    c4 = W.C / (2 * (flute_len + 2 * 0.6133 * R_FLUTE))
    return {"f": f, "z_stopped_db": 20 * np.log10(z), "y_open_db": 20 * np.log10(y / y.max()) + 20 * np.log10(z.max()),
            "stopped": [p[0] for p in ps][:6], "open": [p[0] for p in po][:6], "length": PIPE,
            "ideal_stopped": W.C / (4 * PIPE), "ideal_open": W.C / (2 * PIPE), "c": W.C,
            "end_correction_mm": 1000 * 0.6133 * R_CLAR,
            "worked": {"flute_length": flute_len, "simple": W.C / (2 * flute_len), "corrected": c4, "middle_c": C4,
                       "clarinet_d3": 146.83, "clarinet_length": W.C / (4 * 146.83)}}


def compute_reed() -> dict:
    bore = W.cylinder(PIPE, R_CLAR)
    dp = np.linspace(-0.2, 1.2, 281)
    d = W.reed_tone(bore, 0.45, 1.0)
    f1 = levels(d["p"])["hz"]
    per = SR / f1
    i0 = len(d["p"]) - int(3.2 * per)
    seg = slice(i0, i0 + int(3 * per))
    gammas = [round(float(g), 2) for g in np.arange(0.24, 0.981, 0.03)]
    rows = []
    for g in gammas:
        r = levels(W.reed_tone(bore, g, 0.9)["p"])
        h = np.array(r["harmonics_db"])
        amps = 10 ** (h / 20.0) if r["amp"] > 1e-3 else np.zeros(10)
        bright = float(np.sum(np.arange(1, 11) * amps) / max(np.sum(amps), 1e-12)) if r["amp"] > 1e-3 else 0.0
        rows.append({"gamma": g, "amp": r["amp"], "hz": r["hz"], "third_db": float(h[2]), "fifth_db": float(h[4]), "brightness": bright})
    speaking = [r for r in rows if r["amp"] > 0.05]
    threshold = next(float(g) for g in np.arange(0.32, 0.41, 0.01) if levels(W.reed_tone(bore, float(g), 3.0)["p"])["amp"] > 0.02)
    # a slow crescendo: the mouth pressure rises steadily from below the threshold
    secs = 5.0
    ramp = np.linspace(0.22, 0.85, int(secs * SR))
    c = W.reed_tone(bore, ramp, secs, attack=0.01)
    env = np.sqrt(np.convolve(c["p"] ** 2, np.ones(960) / 960, mode="same"))
    speak = float(np.argmax(env > 0.05) / SR)
    cres = clip(c["sound"], (0.01, 0.1)).at_level(LEVEL)
    cres = Clip(cres.y, SR, {"start": 0.0, "speaks": speak})
    return {"dp": dp, "flow": W.reed_flow(dp), "zeta": 0.35, "top": 1 / 3,
            "t": np.arange(int(3 * per)) / per, "p": d["p"][seg], "u": d["u"][seg], "gamma": 0.45, "hz": f1,
            "harmonics_db": levels(d["p"])["harmonics_db"], "square_db": [(-20 * math.log10(n) if n % 2 else -120.0) for n in range(1, 11)],
            "rows": rows, "threshold": threshold, "ramp": [0.22, 0.85], "speaks_at": speak, "speaks_gamma": float(ramp[int(speak * SR)]),
            "soft": speaking[0], "loud": rows[-4],
            "clips": {"crescendo": save("reed.crescendo", cres, level=None, detail="a model clarinet, blown steadily harder for five seconds")}}


def compute_holes() -> dict:
    a = R_CLAR
    cut = W.cylinder(0.45, a).peaks(600)[0][0]
    whole = W.cylinder(PIPE, a).peaks(600)[0][0]
    rows = []
    for r in (0.0075, 0.004, 0.002):
        b = W.Bore().tube(0.45, a).hole(r, 0.003).tube(0.15, a)
        f1 = b.peaks(600)[0][0]
        rows.append({"radius_mm": 1000 * r, "hz": f1, "cents_below_cut": cents(cut / f1)})
    plain, reg = W.clarinet(PIPE, a), W.clarinet(PIPE, a, register_hole=True)
    f = np.arange(60.0, 1000.0, 1.0)
    lo = W.reed_tone(plain, 0.45, 1.6)
    hi = W.reed_tone(reg, 0.45, 1.6)
    f_lo, f_hi = levels(lo["p"])["hz"], levels(hi["p"])["hz"]
    seq = concat([clip(lo["sound"]).at_level(LEVEL), clip(hi["sound"]).at_level(LEVEL)], gap=0.35, names=["low", "high"])
    return {"cut_hz": cut, "whole_hz": whole, "rows": rows, "f": f, "z_plain_db": 20 * np.log10(np.abs(plain.impedance(f))),
            "z_register_db": 20 * np.log10(np.abs(reg.impedance(f))), "peaks_plain": [p[0] for p in plain.peaks(1000)][:3],
            "peaks_register": [p[0] for p in reg.peaks(1000)][:3], "low_hz": f_lo, "high_hz": f_hi, "ratio": f_hi / f_lo,
            "interval_cents": cents(f_hi / f_lo), "twelfth_cents": cents(3.0), "hole_at": 0.25,
            "clips": {"register": save("holes.register", seq, level=None, detail="a model clarinet: its lowest note, then the same fingering with the register hole open")}}


def compute_cone() -> dict:
    cyl, sax = W.cylinder(PIPE, R_CLAR), W.saxophone(PIPE)
    bare = W.cone(PIPE, 0.005, 0.03)
    f = np.arange(60.0, 2000.0, 1.0)
    pc, ps, pb = [p[0] for p in cyl.peaks(2000)][:5], [p[0] for p in sax.peaks(2000)][:5], [p[0] for p in bare.peaks(2000)][:5]
    a = levels(W.reed_tone(cyl, 0.45, 1.0)["sound"])
    b = levels(W.reed_tone(sax, 0.45, 1.0, zeta=0.9)["sound"])
    note = 196.0
    ya, yb = saxophone(note, 2.0), clarinet(note, 2.0)
    quiz = concat([clip(ya).at_level(LEVEL), clip(yb).at_level(LEVEL)], gap=0.5, names=["A", "B"])
    xs, rs = sax.profile()
    return {"f": f, "z_cyl_db": 20 * np.log10(np.abs(cyl.impedance(f))), "z_cone_db": 20 * np.log10(np.abs(sax.impedance(f))),
            "peaks_cyl": pc, "peaks_cone": ps, "peaks_bare": pb, "ratios_cyl": [x / pc[0] for x in pc], "ratios_cone": [x / ps[0] for x in ps],
            "ratios_bare": [x / pb[0] for x in pb], "cyl_hz": a["hz"], "cone_hz": b["hz"], "cyl_db": a["harmonics_db"], "cone_db": b["harmonics_db"],
            "length": PIPE, "open_pipe_hz": W.C / (2 * PIPE), "note": note, "cyl_length": clarinet_length(note), "cone_length": sax_length(note),
            "quiz_db": {"A": levels(ya)["harmonics_db"], "B": levels(yb)["harmonics_db"]}, "quiz_answer": "B",
            "profile_x": xs, "profile_r": rs,
            "clips": {"quiz": save("cone.quiz", quiz, level=None, detail="one note on two reed instruments: a cone, then a cylinder")}}


def compute_lips() -> dict:
    tr = W.trumpet()
    plain = W.cylinder(1.37, 0.0058)
    f = np.arange(40.0, 1400.0, 1.0)
    pk, pp = tr.peaks(1400), plain.peaks(1400)
    f0, off = W.harmonicity(pk, lowest=2, count=7)
    xs, rs = tr.profile()
    stairs = []
    for fl in np.arange(150.0, 781.0, 15.0):
        r = levels(W.lip_tone(tr, float(fl), 0.6)["p"], 0.2)
        stairs.append({"lip": float(fl), "hz": r["hz"], "amp": r["amp"]})
    # a call on one length of tube: the lips alone choose the note
    order = [3, 4, 5, 4, 3, 4, 5, 6]
    durs = [0.32, 0.32, 0.6, 0.32, 0.32, 0.32, 0.32, 1.3]
    lipf = np.concatenate([np.full(int(d * SR), pk[k - 1][0] / 1.3) for k, d in zip(order, durs)])
    d = W.lip_tone(tr, lipf, sum(durs), attack=0.03)
    starts = np.concatenate([[0.0], np.cumsum(durs)[:-1]])
    heard = []
    for t0, dd in zip(starts, durs):
        seg = d["p"][int((t0 + 0.5 * dd) * SR): int((t0 + dd) * SR)]
        heard.append(levels(seg, min(0.25, 0.45 * dd))["hz"])
    call = clip(d["sound"], (0.01, 0.12)).at_level(LEVEL)
    call = Clip(call.y, SR, {f"n{k}": float(t) for k, t in enumerate(starts)})
    semi = 2 ** (1 / 12)
    v1, v2, v3 = semi ** 2 - 1, semi - 1, semi ** 3 - 1
    return {"f": f, "z_trumpet_db": 20 * np.log10(np.abs(tr.impedance(f))), "z_plain_db": 20 * np.log10(np.abs(plain.impedance(f))),
            "peaks": [p[0] for p in pk][:9], "plain_peaks": [p[0] for p in pp][:9], "f0": f0, "off_cents": off, "pedal": pk[0][0],
            "tube": tr.length, "profile_x": xs, "profile_r": rs, "stairs": stairs, "order": order, "durs": durs, "heard": heard,
            "targets": [pk[k - 1][0] for k in order],
            "valves": {"semitone": semi - 1, "v1": v1, "v2": v2, "v3": v3, "need_13": semi ** 5 - 1, "have_13": v1 + v3,
                       "sharp_cents": cents((1 + semi ** 5 - 1) / (1 + v1 + v3)), "tube_cm": 148.0,
                       "extra_cm": 148.0 * (semi ** 5 - 1 - v1 - v3)},
            "clips": {"call": save("lips.call", call, level=None, detail="a model trumpet with no valves: eight notes on one length of tube")}}


def compute_jet() -> dict:
    hz = 262.0
    rows = []
    for pr in (0.5, 0.7, 1.0, 1.4, 2.0, 2.5, 3.0, 4.0, 6.0, 9.0):
        r = levels(flute(hz, 0.8, pr), 0.25)
        rows.append({"pressure": pr, "hz": r["hz"], "register": int(round(r["hz"] / hz)), "delay": W.jet_delay(pr)})
    secs = 5.0
    pr = np.geomspace(0.6, 8.0, int(secs * SR))
    y = flute(hz, secs, pr)
    track = []
    for k in range(int(secs / 0.1) - 2):
        seg = y[int(k * 0.1 * SR): int((k * 0.1 + 0.2) * SR)]
        track.append({"t": k * 0.1 + 0.1, "hz": levels(seg, 0.18)["hz"], "pressure": float(pr[int((k * 0.1 + 0.1) * SR)])})
    jump = next(r for r in track if r["hz"] > 1.5 * hz)
    over = clip(y, (0.02, 0.1)).at_level(LEVEL)
    over = Clip(over.y, SR, {"start": 0.0, "jump": jump["t"]})
    # which overblows to the octave?  A: the clarinet (a twelfth).  B: the flute (an octave)
    pipe_f = W.cylinder(PIPE, R_FLUTE).peaks(600, admittance=True)[0][0]
    cl_lo = W.reed_tone(W.clarinet(PIPE, R_CLAR), 0.45, 1.3)["sound"]
    cl_hi = W.reed_tone(W.clarinet(PIPE, R_CLAR, register_hole=True), 0.45, 1.3)["sound"]
    fl_lo, fl_hi = flute(pipe_f, 1.3, 1.0), flute(pipe_f, 1.3, 3.2)
    pair = lambda a, b: concat([clip(a).at_level(LEVEL), clip(b).at_level(LEVEL)], gap=0.12, names=["low", "high"])     # noqa: E731
    quiz = concat([pair(cl_lo, cl_hi), pair(fl_lo, fl_hi)], gap=0.7, names=["A", "B"])
    # an organ: one note, its stops drawn one at a time
    stops = [("8'", 1), ("4'", 2), ("2 2/3'", 3), ("2'", 4), ("1 3/5'", 5)]
    note, each = 196.0, 1.5
    pipes = [clip(flute(note * n, each * (len(stops) - k) + 0.3), (0.03, 0.2)).at_level(LEVEL - 4 - 2.5 * k) for k, (_, n) in enumerate(stops)]
    organ = mix([(c, k * each) for k, c in enumerate(pipes)]).at_level(LEVEL)
    organ = Clip(organ.y, SR, {f"stop{k}": k * each for k in range(len(stops))})
    return {"hz": hz, "rows": rows, "track": track, "jump_pressure": jump["pressure"], "jump_t": jump["t"],
            "first_octave_pressure": next(r["pressure"] for r in rows if r["register"] == 2),
            "quiz": {"A": "clarinet", "B": "flute", "flute_cents": cents(levels(fl_hi)["hz"] / levels(fl_lo)["hz"])}, "quiz_answer": "B",
            "stops": [{"name": n, "harmonic": h, "hz": note * h} for n, h in stops], "organ_note": note,
            "clips": {"overblow": save("jet.overblow", over, level=None, detail="a model flute, one fingering, blown steadily harder"),
                      "quiz": save("jet.quiz", quiz, level=None, detail="two instruments, each on its lowest note and then overblown"),
                      "organ": save("jet.organ", organ, level=None, detail="model flue pipes: one note, five stops drawn one at a time")}}


def compute_voice() -> dict:
    hz = 110.0
    g = W.glottal_pulse(hz, 1.0, jitter=0.0, shimmer=0.0, breath=0.0)
    per = int(SR / hz)
    spec = np.abs(np.fft.rfft(g[: 40 * per] * np.hanning(40 * per)))
    fr = np.fft.rfftfreq(40 * per, 1 / SR)
    harm = np.array([spec[np.argmin(np.abs(fr - n * hz))] for n in range(1, 41)])
    src_db = 20 * np.log10(harm / harm[0])
    slope = float(np.polyfit(np.log2(np.arange(2, 33)), src_db[1:32], 1)[0])
    f = np.linspace(50, 4500, 500)
    env = {v: W.spectrum_envelope(W.VOWELS[v], f) for v in ("a", "i", "u")}
    out = {}
    for v in ("a", "i", "u"):
        y = W.voice(hz, W.VOWELS[v], 1.0, jitter=0.0, shimmer=0.0, breath=0.0)
        sp = np.abs(np.fft.rfft(y[: 40 * per] * np.hanning(40 * per)))
        hv = np.array([sp[np.argmin(np.abs(fr - n * hz))] for n in range(1, 41)])
        out[v] = 20 * np.log10(hv / hv.max())
    buzz = np.diff(W.glottal_pulse(hz, 1.4), prepend=0.0)
    seq = concat([clip(buzz).at_level(LEVEL - 3)] + [clip(sung(hz, 1.4, v, vibrato=0.0)).at_level(LEVEL) for v in ("a", "i", "u")], gap=0.3,
                 names=["source", "a", "i", "u"])
    return {"hz": hz, "pulse_t": np.arange(2 * per) / per, "pulse": g[10 * per: 12 * per], "source_db": src_db, "source_slope": slope,
            "f": f, "env_a": env["a"], "env_i": env["i"], "env_u": env["u"], "out_a": out["a"], "out_i": out["i"], "out_u": out["u"],
            "formants": {v: list(W.VOWELS[v]) for v in ("a", "i", "u")}, "words": {v: W.VOWEL_WORDS[v] for v in ("a", "i", "u")},
            "clips": {"build": save("voice.build", seq, kind="synthesized", level=None, detail="pulses alone; then the same pulses through three filters")}}


def compute_vowels() -> dict:
    shapes = {}
    for name in ("neutral", "a", "i"):
        a1, l1, a2, l2 = W.TWO_TUBE[name]
        shapes[name] = {"areas": [a1, a2], "lengths": [l1, l2], "formants": W.tract_formants(W.two_tube(name))}
    length = 0.175
    quarter = [W.C * (2 * k - 1) / (4 * length) for k in (1, 2, 3)]
    chart = [{"vowel": v, "word": W.VOWEL_WORDS[v], "f1": f[0], "f2": f[1]} for v, f in W.VOWELS.items()]
    order = ["u", "a", "i"]
    quiz = concat([clip(sung(131.0, 1.3, v, vibrato=0.0)).at_level(LEVEL) for v in order], gap=0.4, names=["A", "B", "C"])
    pitches = [98.0, 147.0, 220.0]
    same = concat([clip(sung(p, 1.2, "a", vibrato=0.0)).at_level(LEVEL) for p in pitches], gap=0.3, names=["p0", "p1", "p2"])
    return {"shapes": shapes, "length_cm": 100 * length, "quarter": quarter, "measured": {v: list(W.VOWELS[v]) for v in ("a", "i")},
            "chart": chart, "order": order, "order_words": [W.VOWEL_WORDS[v] for v in order], "pitches": pitches,
            "clips": {"quiz": save("vowels.quiz", quiz, kind="synthesized", level=None, detail="one sung note, three vowels"),
                      "same": save("vowels.same", same, kind="synthesized", level=None, detail="one vowel on three notes")}}


def compute_singers() -> dict:
    f = np.linspace(50, 5000, 600)
    speech = (730.0, 1090.0, 2440.0)
    plain = W.spectrum_envelope(speech, f, higher=(3500.0, 4500.0))
    ring_f, ring_hi = (700.0, 1100.0, 2600.0), (2950.0, 3300.0)
    ring = W.spectrum_envelope(ring_f, f, bandwidths=[80, 90, 100, 110, 120], higher=ring_hi)
    band = (f > 2500) & (f < 3500)
    boost = float(ring[band].max() - plain[band].max())
    hz = 220.0
    ya = sung(hz, 2.2, formants=speech)
    yb = sung(hz, 2.2, formants=ring_f, higher=ring_hi, bandwidths=[80, 90, 100, 110, 120])
    pair = concat([clip(ya).at_level(LEVEL), clip(yb).at_level(LEVEL)], gap=0.5, names=["plain", "ring"])
    # a soprano on a high A, singing 'ee': the first formant is far below the note until she opens her mouth
    top = 880.0
    untuned = float(W.spectrum_envelope((310.0, 2790.0, 3310.0), np.array([top]))[0])
    tuned = float(W.spectrum_envelope((top, 2790.0, 3310.0), np.array([top]))[0])
    # overtone singing: the Tune's first phrase on the harmonics of one drone
    degree_h = {1: 8, 2: 9, 3: 10, 4: 11, 5: 12, 6: 13}
    phrase = [1, 1, 5, 5, 6, 6, 5]
    beats = [1, 1, 1, 1, 1, 1, 2]
    harm = [degree_h[d] for d in phrase]
    durs = [0.55 * b for b in beats]
    durs[-1] += 0.6
    yo, starts = overtone_voice(C3, harm, durs)
    seg = yo[int((starts[2] + 0.1) * SR): int((starts[2] + 0.5) * SR)]
    sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    fr = np.fft.rfftfreq(len(seg), 1 / SR)
    hv = np.array([sp[np.argmin(np.abs(fr - n * C3))] for n in range(1, 25)])
    hv_db = 20 * np.log10(hv / hv.max())
    target = harm[2]
    others = np.delete(hv_db[5:], target - 6)
    over = clip(yo, (0.05, 0.25)).at_level(LEVEL)
    over = Clip(over.y, SR, {f"n{k}": t for k, t in enumerate(starts)})
    just = {4: 4 / 3, 6: 5 / 3}
    return {"f": f, "plain_db": plain, "ring_db": ring, "boost_db": boost, "orchestra_db": -9.0 * np.log2(np.maximum(f, 500.0) / 500.0), "hz": hz,
            "soprano": {"note": top, "f1_speech": 310.0, "untuned_db": untuned, "tuned_db": tuned, "gain_db": tuned - untuned},
            "drone": C3, "degree_harmonic": {str(k): v for k, v in degree_h.items()}, "phrase": phrase, "harmonics": harm,
            "overtone_hz": [h * C3 for h in harm], "spectrum_db": hv_db, "target": target, "prominence_db": float(hv_db[target - 1] - others.max()),
            "off_cents": {"4": cents(11 / 8 / just[4]), "6": cents(13 / 8 / just[6])},
            "clips": {"formant": save("singers.formant", pair, kind="synthesized", level=None, detail="one sung note: a speaking voice's resonances, then a trained singer's"),
                      "overtone": save("singers.overtone", over, kind="synthesized", level=None, detail="a model voice: a drone on C, and the Tune's first phrase in its overtones")}}


def compute_tune() -> dict:
    beat = 0.55
    voices = {
        "flute": lambda hz, dur, e: clip(flute(2 * hz, dur * 0.97), (0.03, 0.06)).at_level(LEVEL - 2),
        "clarinet": lambda hz, dur, e: clip(clarinet(hz, dur * 0.97), (0.02, 0.05)).at_level(LEVEL - 1),
        "saxophone": lambda hz, dur, e: clip(saxophone(hz, dur * 0.97), (0.02, 0.05)).at_level(LEVEL - 2),
        "trumpet": lambda hz, dur, e: clip(trumpet(hz, dur * 0.97), (0.015, 0.05)).at_level(LEVEL - 2),
        "voice": lambda hz, dur, e: clip(sung(hz / 2, dur * 0.99, "a", vibrato=20.0 if dur > 0.8 else 0.0, seed=e["index"]), (0.03, 0.08)).at_level(LEVEL - 1),
    }
    order = list(voices)
    plan = [("flute",), ("clarinet",), ("saxophone",), ("trumpet",), ("voice",), tuple(order)]
    parts = {name: play_tune(lambda hz, dur, e, v=v: v(hz, dur, e), phrases=None, tonic=C4, tail=0.9, beat=beat) for name, v in voices.items()}
    ref = parts["flute"]
    n_all = max(len(c.y) for c in parts.values())
    t_phrase = [ref.events[f"phrase{k}"] for k in range(6)]
    y = np.zeros(n_all)
    for name, c in parts.items():
        gate = np.zeros(n_all)
        for k, who in enumerate(plan):
            if name in who:
                a = int(t_phrase[k] * SR)
                b = int(t_phrase[k + 1] * SR) if k < 5 else n_all
                gate[a:b] = 1.0
        w = int(0.02 * SR)
        gate = np.convolve(gate, np.ones(w) / w, mode="same")
        yy = np.zeros(n_all)
        yy[: len(c.y)] = c.mono
        tutti = np.zeros(n_all)
        tutti[int(t_phrase[5] * SR):] = 1.0
        y += yy * gate * (1.0 - 0.45 * tutti)
    notes = [{**n, "voices": list(plan[n["phrase"]])} for n in ref.notes]
    out = Clip(y, SR, ref.events, notes).at_level(LEVEL)
    # how well in tune the instruments are: each one's six notes, measured
    worst, per = 0.0, {}
    for name, fn, octave in (("flute", flute, 2.0), ("clarinet", clarinet, 1.0), ("saxophone", saxophone, 1.0), ("trumpet", trumpet, 1.0)):
        errs = []
        for r in (1, 9 / 8, 5 / 4, 4 / 3, 3 / 2, 5 / 3):
            hz = C4 * r * octave
            errs.append(cents(levels(fn(hz, 0.6), 0.2)["hz"] / hz))
        per[name] = float(np.max(np.abs(errs)))
        worst = max(worst, per[name])
    return {"clip": save("tune.variation8", out, level=None, detail="a flute, a clarinet, a saxophone, a trumpet and a voice: five valves on five columns of air"),
            "notes": notes, "seconds": out.duration, "plan": [list(p) for p in plan], "order": order, "worst_cents": worst, "per_cents": per,
            "lengths": {"clarinet": [clarinet_length(round(C4 * r, 3)) for r in (1, 5 / 3)], "saxophone": [sax_length(round(C4 * r, 3)) for r in (1, 5 / 3)],
                        "trumpet": [trumpet_tube(round(C4 * r, 3)) for r in (1, 5 / 3)]}}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 8, "title": r"for a flute, a clarinet, a saxophone, a trumpet and a voice: five valves on five columns of air", "seconds": t["seconds"],
            "measure": rf"every wind note within {max(math.ceil(t['worst_cents']), 1)} cents of its pitch", "clip": "tune.variation8"}


ITEMS = {"hook": compute_hook, "column": compute_column, "reed": compute_reed, "holes": compute_holes, "cone": compute_cone, "lips": compute_lips,
         "jet": compute_jet, "voice": compute_voice, "vowels": compute_vowels, "singers": compute_singers, "tune": compute_tune,
         "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
