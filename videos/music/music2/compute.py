"""Precompute everything numerical, and every sound, in Part 2 of *Music, Built* ("Waves in Air").

    python -m videos.music.music2.compute              # everything missing (about two minutes)
    python -m videos.music.music2.compute --force bottle

Numbers are cached in ``.cache/music2/<name>.json`` (+ ``.npz``), sounds in ``.cache/music2/audio/``.  The air is
simulated by Monochord's second layer (``explainer/music/monochord/physics/air.py``): parcels of gas that obey the
gas law, sound in a plane, sound in a tube.  Dates and attributions are the published ones (README, Sources).

Items:
    krakatoa    the hook's numbers (distances and the times sound needs to cover them) and the Tune's first phrase
                on bottles
    vacuum      Boyle's jar: how much quieter a source is as the air is pumped out
    parcels     a pulse and a tone in a row of parcels; how small the motion of audible sound is
    speed       the speed of sound from the gas law alone (Newton's and Laplace's), its change with temperature, a
                pipe cold and warm
    decibel     levels: steps of 6 dB, one string and ten, two questions for the ear
    spread      spreading in a plane and in space (the inverse-square law), a note at 1, 2, 4 and 8 metres
    diffraction a wall: what gets round it at each frequency; the Tune in the open and behind the wall
    interfere   two sources: the pattern, and a walk across it
    tubes       open and stopped pipes against their formulas; the end correction of a pipe in the plane; the pipes
                as sound
    bottle      Helmholtz's resonator: formula, exact two-tube root and simulation; filling a bottle; six bottles
                tuned for the Tune
    impedance   reflection where a tube changes width; a horn against a sudden opening; air and water
    doppler     a source that passes: the heard pitch; Buys Ballot's train; a picture of the crowded wavefronts
    nonlinear   the frontier: a loud wave steepens (the gas chain against Fubini's solution); soft and loud brass
    tune        Variation 2: the Tune on six bottles
    variation   the Variations ledger, row 2
"""

from __future__ import annotations

import math
from functools import lru_cache

import numpy as np
from scipy.signal import fftconvolve
from scipy.special import hankel1

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, QUIET_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord.loudness import momentary_max
from explainer.music.monochord.partkit import envelope, play_tune, resample, saver, string_note
from explainer.music.monochord.physics import air
from explainer.music.monochord.pitch import cents, nearest_note

CACHE = Cache("music2")
CLIPS = ClipStore("music2")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
SOFT = QUIET_LEVEL - 2.5
save = saver(CLIPS, LEVEL)
ROOM = 20.0                         # degrees Celsius, unless a chapter says otherwise
C = air.speed(ROOM)
RNG = np.random.default_rng(1883)


def push(width: float = 1.2e-3):
    """One short push of pressure (a raised cosine ``width`` seconds long), as ``fn(t)``."""
    def fn(t):
        return 0.5 * (1 - math.cos(2 * math.pi * t / width)) if 0 <= t < width else 0.0
    return fn


def response(area, length: float, left: str, right: str, seconds: float = 0.7, celsius: float = ROOM,
             radiation: float = 0.02, q_loss: float = 6.0, where: float | None = None, sr: float = 192_000.0,
             n: int | None = None) -> np.ndarray:
    """What comes out of the mouth of a tube given one push inside it, at 48 kHz."""
    run = air.tube(area, length, seconds, push(), where=0.3 * length if where is None else where, left=left,
                   right=right, sr=sr, celsius=celsius, q_loss=q_loss, radiation=radiation, n=n)
    y = resample(run.radiated, sr, SR)
    return y / max(np.abs(y).max(), 1e-12)


def breath(ir: np.ndarray, seconds: float, seed: int = 0) -> np.ndarray:
    """A tube blown across: the noise of a breath through the tube's response."""
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    noise = rng.standard_normal(n)
    env = np.minimum(1.0, np.arange(n) / (0.08 * SR)) * np.minimum(1.0, (n - np.arange(n)) / (0.15 * SR))
    return fftconvolve(noise * env, ir)[: n + len(ir) // 2]


def q_of(ir: np.ndarray, hz: float) -> float:
    """The quality factor of a response's resonance at ``hz``, from how fast it dies away."""
    spec = np.fft.rfft(ir)
    f = np.fft.rfftfreq(len(ir), 1 / SR)
    spec[(f < 0.8 * hz) | (f > 1.25 * hz)] = 0
    from scipy.signal import hilbert

    e = np.abs(hilbert(np.fft.irfft(spec, len(ir))))
    i0 = int(np.argmax(e))
    i1 = i0 + int(np.argmax(e[i0:] < e[i0] * math.exp(-2)))
    tau = (i1 - i0) / SR / 2.0
    return math.pi * hz * tau


# ---------------------------------------------------------------------------
# The bottle of the part (used by the hook, by its own chapter and by the Variation)
# ---------------------------------------------------------------------------
BOTTLE = {"neck_r": 0.009, "neck_len": 0.060, "body_r": 0.030, "volume": 330e-6}
BOTTLE["neck_area"] = math.pi * BOTTLE["neck_r"] ** 2
BOTTLE["body_area"] = math.pi * BOTTLE["body_r"] ** 2
BOTTLE["body_len"] = BOTTLE["volume"] / BOTTLE["body_area"]
# the air just outside each end of the neck moves with it: 0.61 r outside (Levine and Schwinger, 1948), 0.85 r inside
BOTTLE["neck_eff"] = BOTTLE["neck_len"] + (0.61 + 0.85) * BOTTLE["neck_r"]


def bottle_hz(fill: float) -> float:
    """The note of the bottle with the fraction ``fill`` of its body under water (the two-tube root)."""
    b = BOTTLE
    return air.bottle_exact(b["neck_area"], b["neck_eff"], b["body_area"], b["body_len"] * (1 - fill))


def bottle_ir(fill: float, seconds: float = 0.7) -> np.ndarray:
    return _bottle_ir(round(float(fill), 6), seconds)


@lru_cache(maxsize=64)
def _bottle_ir(fill: float, seconds: float) -> np.ndarray:
    b = BOTTLE
    lb = b["body_len"] * (1 - fill)
    # a grid that fits the neck exactly and the body as nearly as a grid can (within a few hundredths of a millimetre)
    best = min(range(56, 79), key=lambda k: abs(lb / (b["neck_eff"] / k) - round(lb / (b["neck_eff"] / k))))
    h = b["neck_eff"] / best
    n_body = max(4, int(round(lb / h)))
    edge = (n_body - 0.5) * h + 0.5 * h
    return response(lambda x: b["body_area"] if x < edge else b["neck_area"], (n_body + best) * h, "closed", "open",
                    seconds, radiation=0.006, q_loss=4.0, where=0.5 * lb, sr=384_000.0, n=n_body + best)


def fill_for(hz: float) -> float:
    from scipy.optimize import brentq

    return brentq(lambda f: bottle_hz(f) - hz, 0.0, 0.93)


def bottle_note(fill: float, seconds: float, slap: bool = True, seed: int = 0) -> Clip:
    ir = bottle_ir(fill)
    y = ir[: int(seconds * SR)] if slap else breath(ir, seconds, seed)
    return Clip(y).fade(0.001, 0.03)


# ---------------------------------------------------------------------------
def compute_krakatoa() -> dict:
    # Published: the Royal Society's report (Symons, 1888).  Computed: the times.
    places = [("Batavia (Jakarta)", 160), ("Perth", 3110), ("Rodrigues", 4800)]
    c_obs = 0.5 * (674 + 726) * 0.44704          # the report's 674 to 726 miles an hour, in m/s
    rows = [{"place": n, "km": km, "hours": km * 1000 / c_obs / 3600} for n, km in places]
    circuit = 40_030_000 / c_obs / 3600
    tonic = bottle_hz(0.0)
    phrase = play_tune(lambda hz, dur, e: bottle_note(fill_for(hz), dur + 0.25).at_level(LEVEL), phrases=[0],
                       tonic=tonic, tail=0.6)
    return {"rows": rows, "speed_obs": c_obs, "mph": [674, 726], "circuit_hours": circuit, "passages": 7,
            "days": 5, "clips": {"opening": save("krakatoa.opening", phrase)}}


def compute_vacuum() -> dict:
    # A small source of fixed motion radiates power in proportion to the density of the air round it, and at one
    # temperature the density is proportional to the pressure: ten times less air, ten decibels less sound.
    rows = [{"atm": a, "db": 10 * math.log10(a)} for a in (1.0, 0.1, 0.01, 0.001)]
    note = string_note(1.0, 1.25).at_level(LEVEL)
    seq = concat([note.gain(r["db"]) for r in rows], gap=0.1, names=[f"p{i}" for i in range(len(rows))])
    # anything springy carries sound: the speed is always sqrt(stiffness / density)
    R = 8.314462
    media = [
        {"name": "air", "how": r"$\sqrt{\gamma R T / M}$", "speed": math.sqrt(1.4 * R * 293.15 / 0.028964), "computed": True},
        {"name": "helium", "how": r"the same law, a lighter gas", "speed": math.sqrt((5 / 3) * R * 293.15 / 0.0040026), "computed": True},
        {"name": "water", "how": r"measured (20$^\circ$C)", "speed": 1481.0, "computed": False},
        {"name": "a steel rod", "how": r"$\sqrt{E / \rho}$", "speed": math.sqrt(200e9 / 7850.0), "computed": True},
    ]
    return {"rows": rows, "media": media, "helium_ratio": media[1]["speed"] / media[0]["speed"],
            "clips": {"jar": save("vacuum.jar", seq, level=None, detail="level by the computed law")}}


def compute_parcels() -> dict:
    rho, c = air.density(ROOM), C
    sizes = []
    for name, db in (("a quiet room", 30), ("talking", 60), ("an orchestra, loud", 100), ("pain", 130)):
        p = air.pressure_of(db)
        u = p * math.sqrt(2) / (rho * c)                   # peak particle velocity
        sizes.append({"name": name, "db": db, "pa": p, "atm": p / air.P_ATM, "mm_s": u * 1000,
                      "nm_1khz": u / (2 * math.pi * 1000) * 1e9})
    # a pulse in a row of parcels (the film's first picture of sound): displacement of every 10th parcel
    n = 601
    run = air.gas_chain(3.0, n, lambda t: 6.0 * math.exp(-((t - 0.6e-3) / 0.22e-3) ** 2), 0.0075, celsius=ROOM,
                        snapshot_every=40)
    pulse = run.snaps[:, ::10]
    # a steady tone: displacement and pressure a quarter of a cycle apart (analytic, for the picture)
    x = np.linspace(0, 1, 61)
    ph = np.linspace(0, 2 * np.pi, 49)
    xi = np.sin(2 * np.pi * 2 * x[None, :] - ph[:, None])
    pr = -np.cos(2 * np.pi * 2 * x[None, :] - ph[:, None])       # pressure is minus the slope of the displacement
    one_pa = {"mm_s": 1000.0 / (rho * c), "w_m2_at_1pa_rms": 1.0 / (rho * c)}
    return {"sizes": sizes, "one_pa": one_pa, "pulse": pulse, "pulse_dt": run.snap_dt, "pulse_scale": float(np.abs(pulse).max()),
            "tone_xi": xi, "tone_p": pr, "rho": rho, "c": c, "z": rho * c}


def _chain_speed(law: str) -> float:
    def pulse(t):
        return 0.01 * math.exp(-((t - 0.4e-3) / 0.12e-3) ** 2)

    run = air.gas_chain(6.0, 3001, pulse, 0.017, law=law, celsius=0.0, probes=(500, 2000))
    t = []
    for v in run.velocity:
        i = int(np.argmax(v))
        a, b, cc = v[i - 1], v[i], v[i + 1]
        t.append((i + 0.5 * (a - cc) / (a - 2 * b + cc)) * run.dt)
    return 1500 * run.h / (t[1] - t[0])


def compute_speed() -> dict:
    newton, laplace = _chain_speed("isothermal"), _chain_speed("adiabatic")
    temps = [{"c": t, "speed": air.speed(t)} for t in (-10, 0, 10, 20, 30, 37)]
    # a pipe that sounds middle C in a room at 20 degrees, played cold and warm
    L = C / (2 * 261.63)
    cold_t, warm_t = 5.0, 30.0
    tones, hz = {}, {}
    for name, t in (("cold", cold_t), ("room", ROOM), ("warm", warm_t)):
        ir = response(2e-4, L, "open", "open", 0.9, celsius=t)
        tones[name] = Clip(ir[: int(0.8 * SR)]).fade(0.001, 0.05)
        hz[name] = float(air.resonances(ir, SR, 1, 100, 600)[0])
    seq = concat([tones["cold"], tones["cold"], tones["warm"], tones["warm"]], gap=0.12, names=["c1", "c2", "w1", "w2"])
    return {"newton_sim": newton, "laplace_sim": laplace, "newton": air.speed(0.0, "isothermal"),
            "laplace": air.speed(0.0), "short": 1 - air.speed(0.0, "isothermal") / air.speed(0.0),
            "newton_ft": 979, "measured_ft": 1142, "temps": temps, "pipe_len": L, "pipe_hz": hz,
            "cold": cold_t, "warm": warm_t, "cents": cents(hz["warm"] / hz["cold"]),
            "cents_formula": cents(air.speed(warm_t) / air.speed(cold_t)), "per_degree": cents(air.speed(21) / air.speed(20)),
            "clips": {"pipe": save("speed.pipe", seq)}}


def compute_decibel() -> dict:
    marks = [("the quietest sound a young ear hears, at 1 kHz", 0), ("a whisper", 30), ("talking, at a metre", 60),
             ("an orchestra at full cry, in the stalls", 100), ("pain", 130)]
    rows = [{"name": n, "db": db, "pa": air.pressure_of(db), "w_m2": air.I_REF * 10 ** (db / 10)} for n, db in marks]
    note = string_note(1.0, 1.1).at_level(LEVEL)
    steps = concat([note.gain(-6.0 * k) for k in range(4)], gap=0.1, names=[f"s{k}" for k in range(4)])
    # one string, two strings, ten strings: plucks that are not in step add their powers
    def many(k: int, seconds: float = 2.2, seed: int = 0) -> Clip:
        rng = np.random.default_rng(10 + k + 100 * seed)
        placed = []
        for _ in range(k):
            stop = 2 ** (rng.normal(0, 10) / 1200)           # each string a few cents off, each pluck its own place
            one = string_note(stop, seconds, beta=float(rng.uniform(0.08, 0.2))).at_level(LEVEL - 10.5)
            placed.append((one, float(rng.uniform(0, 0.03))))
        return mix(placed)

    def power(c: Clip) -> float:
        return float(np.mean(c.mono[: 2 * SR].astype(np.float64) ** 2))

    groups = {k: many(k) for k in (1, 2, 10)}                # every string as loud as every other; room for ten
    measured = {k: 10 * math.log10(power(c) / power(groups[1])) for k, c in groups.items()}
    # strings that are nearly in tune add like dice: one group may come out louder or softer than the rule, the
    # average of many groups does not
    trials = 24
    mean = {k: 10 * math.log10(np.mean([power(many(k, seed=j + 1)) / power(many(1, seed=j + 1)) for j in range(trials)]))
            for k in (2, 10)}
    choir = concat([groups[1], groups[2], groups[10]], gap=0.15, names=["one", "two", "ten"])
    # the ear question: which pair is the bigger step?
    quiz = concat([concat([note.gain(-9), note.gain(-6)], gap=0.08, names=["a", "b"]),
                   concat([note.gain(-9), note.gain(-3)], gap=0.08, names=["a", "b"])], gap=0.7, names=["A", "B"])
    return {"rows": rows, "measured": {str(k): v for k, v in measured.items()},
            "mean": {str(k): float(v) for k, v in mean.items()}, "trials": trials,
            "expected": {str(k): 10 * math.log10(k) for k in (1, 2, 10)}, "quiz_answer": "B", "quiz_db": [3, 6],
            "clips": {"steps": save("decibel.steps", steps, level=None, detail="each half the pressure of the last"),
                      "choir": save("decibel.choir", choir, level=None),
                      "quiz": save("decibel.quiz", quiz, level=None)}}


def compute_spread() -> dict:
    # in a plane: a tone from a point, heard at three distances
    hz = 600.0
    dist = [0.8, 1.6, 3.2]
    f = air.fdtd2d(8.0, 8.0, 0.02, 0.022, sources=[(4.0, 4.0, air.tone_burst(hz))],
                   receivers=[(4.0 + r, 4.0) for r in dist])
    tail = slice(int(0.015 / f.dt), None)
    amp2 = [float(np.abs(f.receivers[k][tail]).max()) for k in range(3)]
    plane = float(np.polyfit(np.log(dist), np.log(amp2), 1)[0])
    # in space: a tube whose area grows as the square of the distance is one ray of a point source
    run = air.tube(lambda x: 4 * math.pi * (x + 0.2) ** 2, 12.0, 0.03, air.ricker(800.0), where=0.0, left="closed",
                   right="closed", sr=96_000, snapshot_every=1)
    peak = np.abs(run.snaps).max(axis=0)
    r = run.x + 0.2
    pick = [int(np.argmin(np.abs(r - v))) for v in (1.0, 2.0, 4.0, 8.0)]
    space = float(np.polyfit(np.log(r[pick]), np.log(peak[pick]), 1)[0])
    levels = [20 * math.log10(peak[i] / peak[pick[0]]) for i in pick]
    # the picture: a pulse spreading in the plane
    pic = air.fdtd2d(8.0, 6.0, 0.02, 0.016, sources=[(4.0, 3.0, air.ricker(500.0))], snapshot_every=8, snap_stride=2)
    note = string_note(1.0, 1.1).at_level(LEVEL)
    walk = concat([note.gain(v) for v in levels], gap=0.1, names=[f"r{k}" for k in range(4)])
    busker = {"at_1m": 90.0, "metres": 32.0, "doublings": 5, "level": 90.0 - 20 * math.log10(32.0)}
    return {"plane_exponent": plane, "space_exponent": space, "busker": busker, "space_levels": levels, "space_r": [1, 2, 4, 8],
            "per_doubling_db": 20 * math.log10(2.0) * -space, "frames": pic.snaps, "frames_dt": pic.snap_dt,
            "extent": [8.0, 6.0], "hz": hz,
            "clips": {"walk": save("spread.walk", walk, level=None, detail="at 1, 2, 4 and 8 metres")}}


EXTENT_W = (10.0, 7.5)          # the plane of the wall, metres
WALL_X, WALL_TOP = 5.0, 4.0


def _wall(X, Y):
    return (np.abs(X - WALL_X) < 0.05) & (Y < WALL_TOP)


def maekawa(hz: float, src, rec) -> float:
    """Maekawa's chart for a thin screen (1968), as the usual formula: the loss in dB from the Fresnel number."""
    edge = (WALL_X, WALL_TOP)
    delta = math.dist(src, edge) + math.dist(edge, rec) - math.dist(src, rec)
    return -10 * math.log10(3 + 20 * (2 * delta * hz / C))


def compute_diffraction() -> dict:
    src, rec = (3.0, 2.0), (7.0, 1.6)
    runs = {}
    for name, solid in (("free", None), ("wall", _wall)):
        runs[name] = air.fdtd2d(*EXTENT_W, 0.02, 0.06, sources=[(*src, air.ricker(700.0))], solid=solid,
                                receivers=[rec], sponge=50)
    dt = runs["free"].dt
    n = 1 << 15
    hz = np.fft.rfftfreq(n, dt)
    spec = {k: np.abs(np.fft.rfft(v.receivers[0], n)) for k, v in runs.items()}
    band = (hz >= 80) & (hz <= 1700)
    loss = 20 * np.log10(spec["wall"][band] / spec["free"][band])
    # smooth over a third of an octave: what a listener with a musical note for a source gets
    fb = hz[band]
    smooth = np.array([np.mean(loss[(fb > f / 2 ** (1 / 6)) & (fb < f * 2 ** (1 / 6))]) for f in fb])
    table = [{"hz": f, "wavelength": C / f, "db": float(np.interp(f, fb, smooth)), "maekawa": maekawa(f, src, rec)}
             for f in (125, 250, 500, 1000, 1500)]
    # the picture: a low tone and a high tone meeting the wall
    frames = {}
    for name, f in (("low", 170.0), ("high", 1360.0)):
        r = air.fdtd2d(*EXTENT_W, 0.025, 0.04, sources=[(*src, air.tone_burst(f))], solid=_wall, snapshot_every=10,
                       snap_stride=2, sponge=40)
        frames[name] = r.snaps
    solid = r.solid[::2, ::2]
    # the sound: the Tune's first phrase on Part 1's string, in the open and behind the wall
    phrase = play_tune(lambda h_, dur, e: string_note(130.81 / h_, dur + 0.3, release=None if e["last"] else dur - 0.04),
                       phrases=[0], tail=1.0).at_level(LEVEL)
    y = phrase.mono.astype(np.float64)
    Y = np.fft.rfft(y)
    fy = np.fft.rfftfreq(len(y), 1 / SR)
    g = 10 ** (np.interp(np.clip(fy, fb[0], fb[-1]), fb, smooth) / 20)
    behind = Clip(np.fft.irfft(Y * g, len(y)), SR, phrase.events, phrase.notes)
    both = concat([phrase, behind], gap=0.5, names=["open", "behind"])
    return {"table": table, "hz": fb[::4], "loss": smooth[::4], "low": frames["low"], "high": frames["high"],
            "solid": solid, "frames_dt": r.snap_dt, "extent": list(EXTENT_W), "source": src, "listener": rec,
            "low_hz": 170.0, "high_hz": 1360.0, "wall_x": WALL_X, "wall_top": WALL_TOP,
            "worst_vs_maekawa": max(abs(t["db"] - t["maekawa"]) for t in table),
            "drop_db": momentary_max(behind) - momentary_max(phrase),
            "clips": {"wall": save("diffraction.wall", both, level=None, detail="the wall's measured effect, applied")}}


def compute_interfere() -> dict:
    hz, gap = 850.0, 1.2
    s1, s2 = (4.0 - gap / 2, 1.8), (4.0 + gap / 2, 1.8)
    run = air.fdtd2d(8.0, 7.0, 0.02, 0.034, sources=[(*s1, air.tone_burst(hz)), (*s2, air.tone_burst(hz))],
                     snapshot_every=4, snap_stride=2, sponge=50)
    per = int(round(1 / hz / run.snap_dt))
    last = run.snaps[-3 * per:]
    rms = np.sqrt((last.astype(np.float64) ** 2).mean(axis=0))
    y_line = 4.81                                           # the centre of a row of cells
    row = rms[int(y_line / (run.h * 2))]
    xs = (2 * np.arange(len(row)) + 0.5) * run.h            # every second cell was kept
    k = 2 * math.pi * hz / C
    r1 = np.hypot(xs - s1[0], y_line - s1[1])
    r2 = np.hypot(xs - s2[0], y_line - s2[1])
    exact = np.abs(hankel1(0, k * r1) + hankel1(0, k * r2))
    inner = (xs > 1.0) & (xs < 7.0)
    a, b = row[inner] / row[inner].max(), exact[inner] / exact[inner].max()
    # a walk along that line at one metre a second: what a microphone hears
    secs = 6.0
    t = np.arange(int(secs * SR)) / SR
    pos = 1.0 + t
    env = np.interp(pos, xs[inner], b)
    tone = np.sin(2 * math.pi * hz * t) * env
    walk = Clip(tone).fade(0.05, 0.1)
    frames = run.snaps[-2 * per - 1:]
    extra = 0.34                                            # a seat 34 cm nearer one loudspeaker than the other
    comb = {"extra": extra, "nulls": [(2 * k + 1) * C / (2 * extra) for k in range(3)], "peaks": [k * C / extra for k in (1, 2)]}
    return {"hz": hz, "gap": gap, "wavelength": C / hz, "sources": [s1, s2], "comb": comb, "line_y": y_line, "x": xs[inner],
            "sim": a, "exact": b, "worst": float(np.abs(a - b).max()), "rms": rms.astype(np.float32),
            "frames": frames, "extent": [8.0, 7.0], "walk_env": env[:: SR // 100], "walk_secs": secs,
            "quiet_db": float(20 * np.log10(b.min() / b.max())),
            "clips": {"walk": save("interfere.walk", walk, kind="synthesized", level=SOFT,
                                   detail="its level from the computed field")}}


def compute_tubes() -> dict:
    L = C / (2 * 261.63)                                    # open at both ends: middle C
    rows = {}
    for name, stopped in (("open", False), ("stopped", True)):
        run = air.tube(2e-4, L, 0.5, air.ricker(500.0), where=0.23 * L, left="closed" if stopped else "open",
                       right="open", probe=0.31 * L)
        got = air.resonances(run.pressure, run.sr, count=4, fmin=60, fmax=1500)
        want = air.pipe_modes(L, len(got), stopped=stopped)
        rows[name] = {"sim": got.tolist(), "formula": want.tolist(), "worst_cents": float(np.abs(1200 * np.log2(got / want)).max()),
                      "notes": [nearest_note(float(v))[0] for v in want]}
    # mode shapes (pressure) for the pictures
    x = np.linspace(0, 1, 121)
    shape_open = np.array([np.sin(n * np.pi * x) for n in (1, 2, 3)])
    shape_stopped = np.array([np.cos((2 * n - 1) * np.pi * x / 2) for n in (1, 2, 3)])
    # a pipe in the plane, stopped at one end and opening into free space: how much longer does it sound?
    w, Lp = 0.10, 0.60

    def channel(X, Y):
        wall = (np.abs(Y - 1.5) > w / 2) & (np.abs(Y - 1.5) < w / 2 + 0.05) & (X > 0.8) & (X < 0.8 + Lp)
        back = (np.abs(Y - 1.5) < w / 2 + 0.05) & (X > 0.75) & (X <= 0.8)
        return wall | back

    f2 = air.fdtd2d(3.2, 3.0, 0.01, 0.09, sources=[(0.9, 1.5, air.ricker(300.0))], solid=channel, receivers=[(0.86, 1.5)])
    f1 = float(air.resonances(f2.receivers[0][int(0.006 / f2.dt):], 1 / f2.dt, 1, 60, 220)[0])
    eff = C / (4 * f1)
    drive = air.fdtd2d(3.2, 3.0, 0.01, 0.045, sources=[(0.9, 1.5, air.tone_burst(f1, ramp=4))], solid=channel,
                       snapshot_every=6, snap_stride=1)
    per = int(round(1 / f1 / drive.snap_dt))
    frames = drive.snaps[-per - 1:, 100:200, 40:240]         # one period, round the pipe
    solid = drive.solid[100:200, 40:240]
    # the pipes as sound: one push of air inside
    ir_open = response(2e-4, L, "open", "open", 0.9)
    ir_stop = response(2e-4, L, "closed", "open", 0.9)
    ir_half = response(2e-4, L / 2, "closed", "open", 0.9)
    def tok(ir, s=0.8):
        return Clip(ir[: int(s * SR)]).fade(0.001, 0.05)

    pair = concat([tok(ir_open), tok(ir_open), tok(ir_stop), tok(ir_stop)], gap=0.12, names=["o1", "o2", "s1", "s2"])
    blown = concat([Clip(breath(ir_open, 1.6, 1)).fade(0.01, 0.2), Clip(breath(ir_stop, 1.6, 2)).fade(0.01, 0.2)],
                   gap=0.2, names=["open", "stopped"])
    quiz = concat([concat([tok(ir_half), tok(ir_half)], gap=0.12), concat([tok(ir_open), tok(ir_open)], gap=0.12)],
                  gap=0.7, names=["A", "B"])
    def harmonics(ir, f0):
        from explainer.music.monochord.dsp import partials

        db = np.array([row["db"] for row in partials(ir[: int(0.5 * SR)], SR, f0, count=6)])
        return (10 ** ((db - db.max()) / 20)).tolist()

    clar_len = 0.60                                         # the part of a clarinet's tube that counts, roughly
    worked = {"flute_len": C / (2 * 261.63), "clar_len": clar_len, "clar_hz": C / (4 * clar_len),
              "clar_note": nearest_note(C / (4 * clar_len))[0], "clar_real": 146.83,
              "as_open": C / (2 * clar_len), "as_open_note": nearest_note(C / (2 * clar_len))[0]}
    return {"L": L, "rows": rows, "shape_open": shape_open, "shape_stopped": shape_stopped, "worked": worked,
            "quiz_partials": {"A": harmonics(ir_half, 261.63), "B": harmonics(ir_open, 261.63)}, "plane_f1": f1, "plane_len": Lp, "plane_width": w,
            "plane_eff": eff, "plane_extra": eff - Lp, "plane_extra_widths": (eff - Lp) / w, "plane_ideal": C / (4 * Lp),
            "frames": frames, "solid": solid, "extent": [2.0, 1.0], "q_open": q_of(ir_open, 261.63),
            "half_hz": float(air.resonances(ir_half, SR, 1, 100, 600)[0]),
            "open_hz": float(air.resonances(ir_open, SR, 1, 100, 600)[0]), "quiz_answer": "A",
            "clips": {"pair": save("tubes.pair", pair), "blown": save("tubes.blown", blown),
                      "quiz": save("tubes.quiz", quiz)}}


def compute_bottle() -> dict:
    b = BOTTLE
    lumped = air.helmholtz(b["neck_area"], b["neck_eff"], b["volume"])
    exact = bottle_hz(0.0)
    ir = bottle_ir(0.0)
    sim = float(air.resonances(ir, SR, 1, 60, 500)[0])
    fills = np.linspace(0.0, 0.8, 9)
    sweep = [{"fill": float(f), "exact": bottle_hz(float(f)),
              "lumped": air.helmholtz(b["neck_area"], b["neck_eff"], b["volume"] * (1 - f)),
              "sim": float(air.resonances(bottle_ir(float(f), 0.4), SR, 1, 60, 900)[0])} for f in fills]
    slap = Clip(ir[: int(0.9 * SR)]).fade(0.001, 0.05)
    blow = Clip(breath(ir, 2.2, 7)).fade(0.01, 0.2)
    empty = concat([slap, slap, blow], gap=0.15, names=["slap1", "slap2", "blown"])
    three = concat([bottle_note(f, 0.9) for f in (0.0, 0.3, 0.6)], gap=0.1, names=["f0", "f1", "f2"])
    return {"bottle": {k: float(v) for k, v in b.items()}, "lumped": lumped, "exact": exact, "sim": sim,
            "sim_cents": cents(sim / exact), "lumped_cents": cents(lumped / exact), "note": nearest_note(sim)[0],
            "q": q_of(ir, sim), "sweep": sweep, "three_hz": [bottle_hz(f) for f in (0.0, 0.3, 0.6)],
            "clips": {"empty": save("bottle.empty", empty), "fills": save("bottle.fills", three)}}


def compute_impedance() -> dict:
    z_air, z_water = air.impedance(ROOM), 998.0 * 1481.0
    through = 4 * z_air * z_water / (z_air + z_water) ** 2
    # a pulse in a pipe that suddenly becomes four times as wide: how much comes back?
    s1, s2 = 1e-4, 4e-4
    run = air.tube(lambda x: s1 if x < 2.0 else s2, 4.0, 0.0115, air.ricker(1500.0), where=0.0, left="closed",
                   right="closed", sr=192_000, snapshot_every=8)
    trace = run.snaps[:, int(1.0 / run.h)]                  # a microphone a metre before the step
    half = int(0.0065 / run.snap_dt)
    incident, back = np.abs(trace[:half]).max(), trace[half:][int(np.argmax(np.abs(trace[half:])))]
    r_sim = float(back / incident) * float(np.sign(trace[:half][int(np.argmax(np.abs(trace[:half])))]))
    r_formula = (s1 - s2) / (s1 + s2)
    # a horn against a sudden opening: the same pipe into the same wide pipe, with and without a flare
    def flared(x):
        if x < 1.5:
            return s1
        if x < 2.5:
            return s1 * (16.0 ** (x - 1.5))
        return 16 * s1

    def sudden(x):
        return s1 if x < 2.0 else 16 * s1

    got = {}
    for name, fn in (("sudden", sudden), ("horn", flared)):
        rr = air.tube(fn, 6.0, 0.016, air.ricker(500.0), where=0.0, left="closed", right="closed", sr=192_000,
                      snapshot_every=8)
        late = rr.snaps[-1]
        e_tot = float(np.sum(late ** 2 * np.array([fn(v) for v in rr.x])))
        wide = rr.x > 2.6
        e_wide = float(np.sum(late[wide] ** 2 * np.array([fn(v) for v in rr.x[wide]])))
        got[name] = {"through": e_wide / e_tot, "frames": rr.snaps[::4], "x": rr.x}
    theory_sudden = 4 * 16 / (1 + 16) ** 2
    return {"z_air": z_air, "z_water": z_water, "through_water": through, "through_water_db": 10 * math.log10(through),
            "r_sim": r_sim, "r_formula": r_formula, "sudden": got["sudden"]["through"], "horn": got["horn"]["through"],
            "sudden_formula": theory_sudden, "gain_db": 10 * math.log10(got["horn"]["through"] / got["sudden"]["through"]),
            "frames_sudden": got["sudden"]["frames"], "frames_horn": got["horn"]["frames"], "x": got["horn"]["x"],
            "step_frames": run.snaps[::3], "step_x": run.x, "wavelength": C / 500.0}


def compute_doppler() -> dict:
    hz, d = 392.0, 6.0
    horn = (1.0, 0.5, 0.33, 0.2)
    passes, curves = {}, {}
    for name, v in (("slow", 14.0), ("train", None), ("fast", 28.0)):
        if v is None:                                   # the speed that gives a semitone up and a semitone down
            v = C * (2 ** (2 / 12) - 1) / (2 ** (2 / 12) + 1)
        y, heard = air.passing_source(hz, v, d, 6.0, harmonics=horn)
        passes[name] = Clip(y).fade(0.3, 0.3)
        up, down = air.doppler(hz, v)
        curves[name] = {"v": v, "kmh": v * 3.6, "heard": heard[:: SR // 100].tolist(), "up": up, "down": down,
                        "cents": cents(up / down), "env": envelope(passes[name]).tolist()}
    demo = passes["train"]
    quiz = concat([passes["fast"].trim(1.2, 4.8), passes["slow"].trim(1.2, 4.8)], gap=0.6, names=["A", "B"])
    # the picture: a source crossing the plane at four tenths of the speed of sound
    mach = 0.4
    path = lambda t: (0.8 + mach * C * t, 3.0)                      # noqa: E731
    pic = air.fdtd2d(8.0, 6.0, 0.02, 0.042, moving=(path, air.tone_burst(700.0, ramp=1)), snapshot_every=10,
                     snap_stride=2)
    return {"hz": hz, "closest": d, "curves": curves, "quiz_answer": "A", "mach": mach, "frames": pic.snaps,
            "frames_dt": pic.snap_dt, "extent": [8.0, 6.0], "path_start": 0.8, "path_speed": mach * C,
            "ballot_kmh": curves["train"]["kmh"],
            "clips": {"pass": save("doppler.pass", demo, kind="synthesized", detail="a horn passing at 6 metres"),
                      "quiz": save("doppler.quiz", quiz, kind="synthesized")}}


def compute_nonlinear() -> dict:
    hz, u0 = 1000.0, 8.0
    xs = air.shock_distance(u0, hz, celsius=ROOM)
    h = 0.5e-3
    n = int(2.0 * xs / h)
    sig = [0.02, 0.3, 0.6, 0.9]
    probes = [max(2, int(s * xs / h)) for s in sig]
    run = air.gas_chain(n * h, n + 1, lambda t: u0 * math.sin(2 * math.pi * hz * t) * min(1.0, t * hz / 2), 0.012,
                        celsius=ROOM, probes=probes, courant=0.25)
    m = int(round(1 / hz / run.dt))
    t = np.arange(4 * m) * run.dt
    waves, harm = [], []
    for s, v in zip(sig, run.velocity):
        seg = v[-4 * m:]
        got = [abs(2 * np.mean(seg * np.exp(-2j * np.pi * k * hz * t))) / u0 for k in range(1, 7)]
        harm.append({"sigma": s, "sim": got, "fubini": [float(air.fubini(k, s)) for k in range(1, 7)]})
        ph = np.angle(np.mean(seg * np.exp(-2j * np.pi * hz * t)))            # line the periods up on their phase
        one = seg[-m:] / u0
        shift = int(round((-ph - np.pi / 2) / (2 * np.pi) * m)) % m
        waves.append(np.roll(one, shift)[:: max(1, m // 240)][:240])
    worst = max(abs(a - b) for row in harm for a, b in zip(row["sim"][:3], row["fubini"][:3]))
    # in a trombone: the pressure at the mouthpiece, and how far the wave must go before it breaks
    rho = air.density(ROOM)
    horn = []
    for name, pa in (("soft", 500.0), ("medium", 2500.0), ("fortissimo", 10_000.0)):
        horn.append({"name": name, "pa": pa, "db": air.spl(pa / math.sqrt(2)), "u0": pa / (rho * C),
                     "shock_m": air.shock_distance(pa / (rho * C), 500.0, ROOM)})
    # the sound: the simulated waveform of the gentle and of the steep wave, repeated at the pitch of a trombone's B flat
    f0 = 233.08
    def tone(wave, seconds=1.6):
        per = np.asarray(wave, dtype=np.float64)
        ph = (np.arange(int(seconds * SR)) * f0 / SR) % 1.0
        y = np.interp(ph * len(per), np.arange(len(per) + 1), np.append(per, per[0]))
        return Clip(y - y.mean()).fade(0.03, 0.12).at_level(LEVEL)

    pair = concat([tone(waves[0]), tone(waves[-1])], gap=0.25, names=["soft", "loud"])
    return {"hz": hz, "u0": u0, "db": air.spl(u0 * rho * C / math.sqrt(2)), "shock_m": xs, "sigma": sig,
            "waves": np.array(waves), "harmonics": harm, "worst": worst, "horn": horn, "tube_m": 2.7,
            "clips": {"brass": save("nonlinear.brass", pair, level=None,
                                    detail="the simulated wave shape, repeated; equal loudness")}}


def compute_tune() -> dict:
    tonic = bottle_hz(0.0)
    fills, checks = {}, []
    c = play_tune(lambda hz, dur, e: bottle_note(fills.setdefault(e["degree"], fill_for(hz)), dur + 0.3).at_level(LEVEL),
                  tonic=tonic, tail=0.8)
    for degree, fill in sorted(fills.items()):
        ir = bottle_ir(fill)
        got = float(air.resonances(ir, SR, 1, 60, 900)[0])
        want = next(n["hz"] for n in c.notes if n["degree"] == degree)
        checks.append({"degree": degree, "name": next(n["name"] for n in c.notes if n["degree"] == degree),
                       "fill": fill, "ml": fill * BOTTLE["volume"] * 1e6, "hz": got, "want": want,
                       "cents_off": cents(got / want)})
    notes = [{**n, "fill": fills[n["degree"]]} for n in c.notes]
    c = Clip(c.y, SR, c.events, notes)
    info = save("tune.variation2", c)
    return {"clip": info, "notes": notes, "checks": checks, "seconds": c.duration, "tonic": tonic,
            "tonic_note": nearest_note(tonic)[0], "worst_cents": max(abs(k["cents_off"]) for k in checks)}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 2, "title": r"on six bottles, tuned by how much water is in them",
            "seconds": t["seconds"], "key": t["tonic_note"],
            "measure": r"every bottle within 1 cent of its note" if t["worst_cents"] <= 1.0 else
            rf"every bottle within {t['worst_cents']:.0f} cents of its note",
            "clip": "tune.variation2"}


ITEMS = {"krakatoa": compute_krakatoa, "vacuum": compute_vacuum, "parcels": compute_parcels, "speed": compute_speed,
         "decibel": compute_decibel, "spread": compute_spread, "diffraction": compute_diffraction,
         "interfere": compute_interfere, "tubes": compute_tubes, "bottle": compute_bottle,
         "impedance": compute_impedance, "doppler": compute_doppler, "nonlinear": compute_nonlinear,
         "tune": compute_tune, "variation": compute_variation}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
