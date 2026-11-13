"""Precompute everything numerical, and every sound, in Part 7 of *Music, Built* ("Strings, Hammers and Bows").

    python -m videos.music.music7.compute              # everything missing (under a minute)
    python -m videos.music.music7.compute --force bow

Numbers are cached in ``.cache/music7/<name>.json`` (+ ``.npz``), sounds in ``.cache/music7/audio/``.  The
instruments are Monochord's (``explainer/music/monochord/instruments/strings.py``); published values are cited in
the README.

Items:
    three       the cold open: four notes plucked, struck and bowed
    body        a string's force on its bridge, bare and through a guitar's body; a knock on the body; the body's response
    twomass     the guitar's two lowest resonances from a plate, a hole and a box of air
    ks          Karplus and Strong's algorithm: a note, and the Tune's opening
    hammer      a felt hammer on a stiff string at three speeds: contact, force, spectrum, brightness
    stiff       the stiff string's partials against whole multiples; a real and a 'straightened' piano note
    unison      one string, two in perfect unison, two a cent apart: the double decay
    bow         the string under the bow: stick and slip, the Helmholtz motion, a sawtooth on the bridge
    schelleng   the least and greatest bow force at eight bow positions, against Schelleng's formulas; three bowings
    violin      the violin's body: its response, a bowed note without and with vibrato
    tune        Variation 7: the Tune for plucked, struck and bowed strings
    variation   the Variations ledger, row 7
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord.dsp import fourier as F
from explainer.music.monochord.instruments import strings as S
from explainer.music.monochord.instruments.plucked import plucked
from explainer.music.monochord.partkit import play_tune, saver
from explainer.music.monochord.physics.string import String
from explainer.music.monochord.pitch import cents

CACHE = Cache("music7")
CLIPS = ClipStore("music7")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
C3, C4 = 130.8127826502993, 261.6255653005986
GUITAR, VIOLIN, BOARD = S.guitar_body(), S.violin_body(), S.soundboard()
NYLON = dict(L=0.65, mu=0.0012, kappa=0.25, sigma0=0.9, sigma1=2.0e-3)      # a guitar's string: light, flexible, lossy


def guitar(hz: float, seconds: float, beta: float = 0.16, body: bool = True, release: float | None = None) -> np.ndarray:
    force = plucked(string=String.tuned(hz, **NYLON), seconds=seconds, beta=beta, release=release)
    return GUITAR.play(force) if body else force


def piano_string(hz: float) -> String:
    """A plain steel string for a note near middle C: shorter as the note rises, as in a real scale."""
    return String.tuned(hz, L=0.62 * (C4 / hz) ** 0.8, mu=6.34e-3, kappa=1.25, sigma0=0.6, sigma1=3.3e-4)


def piano(hz: float, seconds: float, velocity: float = 1.6, board: bool = True) -> np.ndarray:
    y = S.struck(piano_string(hz), velocity=velocity, seconds=seconds)
    return BOARD.play(y) if board else y


def vibrato(y: np.ndarray, depth_cents: float = 25.0, rate: float = 5.6, sr: int = SR) -> np.ndarray:
    """Slide a sound's pitch up and down (the player's finger rocking on the string) by reading it at a wavering speed."""
    t = np.arange(len(y)) / sr
    onset = np.clip((t - 0.25) / 0.4, 0, 1)                       # vibrato comes in after the note has started
    speed = 2 ** (onset * depth_cents / 1200.0 * np.sin(2 * np.pi * rate * t))
    pos = np.cumsum(speed) - speed[0]
    return np.interp(pos, np.arange(len(y)), y, right=0.0)


def violin(hz: float, seconds: float, bow: S.Bow | None = None, body: bool = True, vib: bool = True) -> np.ndarray:
    y = S.bowed_note(hz, seconds, bow or S.Bow(speed=0.2, force=0.55, at=0.1))
    if vib:
        y = vibrato(y)
    return VIOLIN.play(y) if body else y


def clip(y, fade=(0.003, 0.05)) -> Clip:
    return Clip(np.asarray(y, dtype=np.float64)).fade(*fade)


def spectrum_db(y: np.ndarray, f_max: float, n: int = 400, sr: int = SR):
    spec = np.abs(np.fft.rfft(y * np.hanning(len(y))))
    f = np.fft.rfftfreq(len(y), 1 / sr)
    grid = np.linspace(0, f_max, n)
    db = 20 * np.log10(np.maximum(np.interp(grid, f, spec) / spec.max(), 1e-6))
    return grid, db


# ---------------------------------------------------------------------------
def compute_three() -> dict:
    notes = [C4, C4, C4 * 1.5, C4 * 1.5]
    beat = 0.55

    def phrase(voice):
        return mix([(voice(hz), k * beat) for k, hz in enumerate(notes)])

    g = phrase(lambda hz: clip(guitar(hz / 2, 1.2)).at_level(LEVEL)).at_level(LEVEL)
    p = phrase(lambda hz: clip(piano(hz, 1.2)).at_level(LEVEL)).at_level(LEVEL)
    v = phrase(lambda hz: clip(violin(hz, beat * 0.96), (0.01, 0.05)).at_level(LEVEL)).at_level(LEVEL)
    seq = concat([g, p, v], gap=0.35, names=["plucked", "struck", "bowed"])
    return {"clips": {"three": save("three.notes", seq, level=None, detail="four notes: plucked, struck, bowed")}}


def compute_body() -> dict:
    hz = 110.0
    bare = guitar(hz, 2.6, body=False)
    full = guitar(hz, 2.6)
    seq = concat([clip(bare).at_level(LEVEL), clip(full).at_level(LEVEL)], gap=0.5, names=["bare", "body"])
    tap = clip(GUITAR.tap(0.7), (0.0005, 0.1))
    taps = concat([tap.at_level(LEVEL), tap.at_level(LEVEL)], gap=0.25, names=["t1", "t2"])
    f = np.geomspace(60, 6000, 500)
    fb, sb = spectrum_db(bare[2400:2400 + 48000], 3000.0)
    _, sf = spectrum_db(full[2400:2400 + 48000], 3000.0)
    # how long each lasts: time for the level to fall 20 dB
    def t20(y):
        e = np.sqrt(np.convolve(y ** 2, np.ones(2400) / 2400, mode="same"))
        k0 = int(np.argmax(e))
        below = np.flatnonzero(e[k0:] < e[k0] / 10)
        return float(below[0] / SR) if below.size else float(len(y) / SR)

    return {"hz": hz, "f": f, "response": GUITAR.response_db(f), "spec_f": fb, "spec_bare": sb, "spec_body": sf,
            "modes": [[m[0], m[1]] for m in GUITAR.modes[:8]], "t20_bare": t20(bare), "t20_body": t20(full),
            "clips": {"pair": save("body.pair", seq, level=None, detail="the force on a guitar's bridge, bare; then through the body"),
                      "tap": save("body.tap", taps, level=None, detail="two knocks on the bridge of the model guitar")}}


def compute_twomass() -> dict:
    t = S.two_mass()
    closed = S.two_mass(hole_radius=1e-4)                           # the hole taped shut: the plate alone
    f = np.linspace(50, 300, 600)
    two = S.Body([(t["lower"], 18.0, 1.0), (t["upper"], 22.0, -1.3)])
    db = two.response_db(f)
    between = (f > t["lower"]) & (f < t["upper"])
    dip = float(f[between][int(np.argmin(db[between]))])
    return {**t, "f": f, "db": db, "dip": dip, "low_e": 82.41, "identity_left": t["lower"] ** 2 + t["upper"] ** 2,
            "identity_right": t["helmholtz"] ** 2 + t["plate"] ** 2, "closed_upper": closed["upper"], "volume_l": 14.0, "hole_cm": 8.6}


def compute_ks() -> dict:
    hz = 196.0
    note = clip(S.karplus_strong(hz, 2.2), (0.001, 0.2))
    tune = play_tune(lambda f, dur, e: clip(S.karplus_strong(f, dur + 0.5, seed=e["index"]), (0.001, 0.15)), phrases=[0], tonic=C4 / 2, tail=1.0)
    seq = concat([note.at_level(LEVEL), tune.at_level(LEVEL)], gap=0.5, names=["note", "tune"])
    n = int(round(SR / hz - 0.5))
    rng = np.random.default_rng(0)
    first = rng.uniform(-1, 1, n)
    y = S.karplus_strong(hz, 2.3)
    lap_numbers = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]
    laps = [y[k * n: (k + 1) * n] for k in lap_numbers]
    return {"hz": hz, "delay": n, "true_hz": S.ks_pitch(hz), "off_cents": cents(S.ks_pitch(hz) / hz), "laps": np.array(laps), "lap_numbers": lap_numbers,
            "clips": {"ks": save("ks.demo", seq, kind="synthesized", level=None, detail="Karplus and Strong's algorithm: one note, then the Tune's opening")}}


def compute_hammer() -> dict:
    speeds = [0.5, 1.5, 4.0]
    names = ["soft", "medium", "hard"]
    rows, forces, levels = [], {}, {}
    for v, nm in zip(speeds, names):
        d = S.hammer_strike(velocity=v)
        keep = d["t"] < 0.004
        forces[f"force_{nm}"] = d["force"][keep][::8]
        levels[f"levels_{nm}"] = S.partial_levels(d)[:16]
        rows.append({"name": nm, "velocity": v, "contact_ms": 1000 * d["contact"], "peak_force": d["peak_force"], "centroid": S.strike_centroid(d),
                     "energy_mj": 1000 * d["energy_in"], "rebound": -d["hammer_out"]})
    t = S.hammer_strike(velocity=1.5)["t"]
    t = t[t < 0.004][::8]
    # the three as they are (louder is louder), and a soft and a hard blow brought to the same loudness
    raw = [BOARD.play(S.struck(velocity=v, seconds=1.6)) * (v / speeds[-1]) ** 0.9 for v in speeds]
    peak = max(np.abs(r).max() for r in raw)
    dyn = concat([clip(r / peak) for r in raw], gap=0.25, names=names)
    quiz = concat([clip(piano(C4, 1.8, velocity=4.0)).at_level(LEVEL), clip(piano(C4, 1.8, velocity=0.5)).at_level(LEVEL)], gap=0.5, names=["A", "B"])
    h = S.Hammer()
    return {"rows": rows, "t_ms": 1000 * t, **forces, **levels, "hammer": {"mass_g": 1000 * h.mass, "p": h.p, "at": h.at}, "weak_partial": round(1 / h.at),
            "string": {"L": S.PIANO_C4.L, "T": S.PIANO_C4.T, "B": S.PIANO_C4.B}, "quiz_answer": "A",
            "force_ratio": rows[2]["peak_force"] / rows[0]["peak_force"], "speed_ratio": speeds[2] / speeds[0],
            "clips": {"dynamics": save("hammer.dynamics", dyn, level=LEVEL + 1.5, detail="middle C struck softly, moderately and hard"),
                      "quiz": save("hammer.quiz", quiz, level=None, detail="two notes at the same loudness: one struck hard, one softly")}}


def compute_stiff() -> dict:
    d = S.hammer_strike(velocity=1.6)
    n = d["n"][:20]
    sharp = np.array([cents(float(f) / (k * d["hz"][0])) for k, f in zip(n, d["hz"][:20])])
    # the same note with its partials moved onto whole multiples
    t = np.arange(int(2.4 * SR)) / SR
    amp = np.abs(d["slope"]) * np.sqrt(d["q"] ** 2 + ((d["v"] + d["decay"] * d["q"]) / d["omega_d"]) ** 2)
    real = sum(a * np.exp(-s * t) * np.sin(2 * np.pi * f * t) for a, s, f in zip(amp, d["decay"], d["hz"]))
    straight = sum(a * np.exp(-s * t) * np.sin(2 * np.pi * k * d["hz"][0] * t) for a, s, k in zip(amp, d["decay"], d["n"]))
    seq = concat([clip(BOARD.play(straight)).at_level(LEVEL), clip(BOARD.play(real)).at_level(LEVEL)], gap=0.5, names=["A", "B"])
    rows = [{"n": int(k), "hz": float(f), "cents": float(c)} for k, f, c in zip(n, d["hz"][:20], sharp)]
    bass = S.PIANO_C4.B * 4
    return {"B": S.PIANO_C4.B, "rows": rows, "n": n, "cents": sharp, "seventh_cents": float(sharp[6]), "sixteenth_cents": float(sharp[15]), "quiz_answer": "B",
            "diameter_mm": 1.0, "length_cm": 62.0, "tension_n": S.PIANO_C4.T,
            "clips": {"pair": save("stiff.pair", seq, level=None, detail="one piano note twice: partials on whole multiples, then where a stiff string puts them")}}


def compute_unison() -> dict:
    cases = [("one", dict(single=True)), ("unison", dict(detune_cents=0.0, unequal=0.0)), ("apart", dict(detune_cents=1.0, unequal=0.03))]
    curves, rows = {}, []
    for nm, kw in cases:
        d = S.pair(seconds=6.0, **kw)
        curves[f"db_{nm}"] = d["db"][::4]
        rows.append({"name": nm, "rates": d["rates"], "at_1s": float(np.interp(1.0, d["t"], d["db"])), "at_5s": float(np.interp(5.0, d["t"], d["db"]))})
    t = S.pair(single=True)["t"][::4]
    sounds = [S.pair_sound(0.0, 4.2, single=True), S.pair_sound(0.0, 4.2, unequal=0.0), S.pair_sound(1.0, 4.2)]
    scale = [0.5, 1.0, 1.0]                                          # two strings start with twice the force of one
    seq = concat([clip(BOARD.play(y) * s, (0.002, 0.3)) for y, s in zip(sounds, scale)], gap=0.3, names=[c[0] for c in cases])
    apart = S.pair(1.0, unequal=0.03)
    early = (np.interp(0.5, apart["t"], apart["db"]) - apart["db"][0]) / 0.5
    late = (np.interp(5.5, apart["t"], apart["db"]) - np.interp(3.5, apart["t"], apart["db"])) / 2.0
    return {"t": t, **curves, "rows": rows, "early_db_s": float(early), "late_db_s": float(late), "detune_cents": 1.0, "beat_hz": apart["beat_hz"],
            "clips": {"three": save("unison.three", seq, level=LEVEL + 1.0, detail="one string; two in perfect unison; two a cent apart")}}


def compute_bow() -> dict:
    b = S.Bow(speed=0.2, force=0.5, at=0.1)
    d = S.bowed(196.0, b, seconds=1.5)
    r = S.bow_regime(d)
    p = d["period"]
    sl = slice(-2 * p, None)
    step = max(p // 240, 1)
    x = d["bridge"][-40 * p:]
    spec = np.abs(np.fft.rfft(x - x.mean()))
    harm = [20 * math.log10(spec[40 * n] / spec[40]) for n in range(1, 13)]
    raw = S.bowed_note(196.0, 1.6, b)
    seq = concat([clip(raw, (0.01, 0.05)).at_level(LEVEL - 3), clip(VIOLIN.play(raw), (0.01, 0.05)).at_level(LEVEL)], gap=0.4, names=["bare", "body"])
    pl = S.hammer_strike(velocity=1.5)
    return {"beta": d["beta"], "speed": b.speed, "force": b.force, "regime": r, "t": np.arange(2 * p)[::step] / p, "v": d["v"][sl][::step], "friction": d["friction"][sl][::step],
            "bridge": d["bridge"][sl][::step] / np.abs(d["bridge"][sl]).max(), "slipping": d["slipping"][sl][::step], "harmonics_db": harm,
            "sawtooth_db": [-20 * math.log10(n) for n in range(1, 13)], "flyback": float(d["v"][sl][d["slipping"][sl] > 0.5].mean()),
            "expected_flyback": -b.speed * (1 - d["beta"]) / d["beta"], "mu_s": b.mu_s, "mu_d": b.mu_d,
            "clips": {"pair": save("bow.pair", seq, level=None, detail="the force on a violin's bridge, bare; then through the body")}}


def compute_schelleng() -> dict:
    betas = [0.04, 0.055, 0.075, 0.1, 0.13, 0.17, 0.22, 0.28]
    rows = [S.bow_limits(b) for b in betas]
    fit = lambda key: float(np.polyfit(np.log([r["beta"] for r in rows[1:7]]), np.log([r[key] for r in rows[1:7]]), 1)[0])     # noqa: E731
    mid = rows[3]
    forces = {"light": mid["min"] / 6, "right": 0.43 * mid["max"], "heavy": mid["max"] * 4}
    sounds, regimes = [], {}
    for nm, f in forces.items():
        bow = S.Bow(speed=0.2, force=f, at=0.1)
        kw = dict(press=f) if nm == "light" else {}
        regimes[nm] = S.bow_regime(S.bowed(196.0, bow, seconds=1.5, **kw))
        y = S.bowed_note(196.0, 1.5, bow, **kw)
        sounds.append(clip(VIOLIN.play(y), (0.01, 0.05)).at_level(LEVEL - (4 if nm == "light" else 0)))
    order = ["heavy", "right", "light"]
    seq = concat([sounds[list(forces).index(k)] for k in order], gap=0.4, names=["A", "B", "C"])
    return {"rows": rows, "slope_max": fit("max"), "slope_min": fit("min"), "forces": forces, "regimes": regimes, "order": order,
            "max_ratio": [r["max"] / r["schelleng_max"] for r in rows], "min_ratio": [r["min"] / r["schelleng_min"] for r in rows],
            "clips": {"three": save("schelleng.three", seq, level=None, detail="one note bowed three ways: too hard, well, too lightly")}}


def compute_violin() -> dict:
    f = np.geomspace(190, 8000, 600)
    db = VIOLIN.response_db(f)
    hz = 440.0
    raw = S.bowed_note(hz, 2.4, S.Bow(speed=0.2, force=0.55, at=0.1))
    plain, alive = VIOLIN.play(raw), VIOLIN.play(vibrato(raw, 30.0))
    seq = concat([clip(plain, (0.01, 0.08)).at_level(LEVEL), clip(alive, (0.01, 0.08)).at_level(LEVEL)], gap=0.4, names=["still", "vibrato"])
    # how much each of the first ten partials changes in level as the pitch swings 30 cents either way
    swing = []
    for n in range(1, 11):
        lo, hi = VIOLIN.response_db([n * hz * 2 ** (-30 / 1200)])[0], VIOLIN.response_db([n * hz * 2 ** (30 / 1200)])[0]
        swing.append(float(hi - lo))
    return {"f": f, "db": db - db.max(), "modes": {"A0": 275.0, "B1-": 460.0, "B1+": 540.0, "hill": 2500.0}, "hz": hz, "swing_db": swing,
            "largest_swing": float(np.max(np.abs(swing))), "strings": {"G": 196.0, "D": 293.66, "A": 440.0, "E": 659.26},
            "clips": {"vibrato": save("violin.vibrato", seq, level=None, detail="one bowed note through the violin's body: held still, then with vibrato")}}


def compute_tune() -> dict:
    beat = 0.55
    voices = {"plucked": lambda hz, dur, e: clip(guitar(hz / 2, dur + 0.9)).at_level(LEVEL - 1),
              "struck": lambda hz, dur, e: clip(piano(hz, dur + 0.9)).at_level(LEVEL - 1),
              "bowed": lambda hz, dur, e: clip(violin(hz * 2, dur * 0.97), (0.012, 0.05)).at_level(LEVEL - 2)}
    plan = [("plucked",), ("struck",), ("bowed",), ("plucked", "bowed"), ("struck", "bowed"), ("plucked", "struck", "bowed")]
    parts = {}
    for name, voice in voices.items():
        ph = [k for k, who in enumerate(plan) if name in who]
        parts[name] = play_tune(lambda hz, dur, e, voice=voice: voice(hz, dur, e), phrases=None, tonic=C4, tail=1.2, beat=beat)
    # keep each voice only in its phrases
    ref = parts["plucked"]
    t_phrase = [ref.events[f"phrase{k}"] for k in range(6)] + [ref.events["end"] + 1.2]
    y = np.zeros(len(ref.y))
    notes = []
    for name, c in parts.items():
        gate = np.zeros(len(ref.y))
        for k, who in enumerate(plan):
            if name in who:
                a, b = int(t_phrase[k] * SR), int(t_phrase[k + 1] * SR) if k < 5 else len(gate)
                gate[a:b] = 1.0
        w = int(0.03 * SR)
        gate = np.convolve(gate, np.ones(w) / w, mode="same")
        yy = c.mono.astype(np.float64)
        y[: len(yy)] += yy[: len(y)] * gate[: len(yy)] * (0.8 if name == "bowed" else 1.0)
    for n in ref.notes:
        notes.append({**n, "voices": list(plan[n["phrase"]])})
    out = Clip(y, SR, ref.events, notes)
    return {"clip": save("tune.variation7", out, detail="a guitar, a piano and a violin, all from one string"), "notes": notes, "seconds": out.duration,
            "plan": [list(p) for p in plan], "models": 3}


def compute_variation() -> dict:
    t = load("tune")
    b = load("bow")
    worst = max(abs(a - s) for a, s in zip(b["harmonics_db"][:8], b["sawtooth_db"][:8]))
    return {"part": 7, "title": r"for plucked, struck and bowed strings: a guitar, a piano and a violin built from one string", "seconds": t["seconds"],
            "measure": rf"the bowed string's force is a sawtooth to within {max(worst, 0.1):.1f} dB", "clip": "tune.variation7"}


ITEMS = {"three": compute_three, "body": compute_body, "twomass": compute_twomass, "ks": compute_ks, "hammer": compute_hammer, "stiff": compute_stiff,
         "unison": compute_unison, "bow": compute_bow, "schelleng": compute_schelleng, "violin": compute_violin, "tune": compute_tune,
         "variation": compute_variation}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
