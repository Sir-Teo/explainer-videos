"""Precompute everything numerical, and every sound, in Part 1 of *Music, Built* ("One String").

    python -m videos.music.music1.compute              # everything missing (under a minute)
    python -m videos.music.music1.compute --force pluck

Numbers are cached in ``.cache/music1/<name>.json`` (+ ``.npz``), sounds in ``.cache/music1/audio/<item>.<clip>.wav``
with their events; scenes call ``load(name)`` and ``clip(name)``.  Every string here is simulated on this computer by
Monochord (``explainer/music/monochord``); the dates and the attributions are the published ones, cited in the README.

Items:
    hammers     the legend's numbers (12, 9, 8, 6), what they give as lengths and as hanging weights, the weights
                that are needed instead (Vincenzo Galilei), an illustrative anvil, and the Tune's first phrase
    ratios      the monochord: the open string and its stops at 1/2, 2/3 and 3/4, each simulated and its pitch
                measured; the pairs as sound; a which-is-the-fifth question
    mersenne    the pitch against length, tension and mass on simulated strings, the exponents fitted to twenty-four
                random strings, and a guitar's top string worked out
    pulse       pulses travelling, reflecting and passing through each other; the wave speed measured; the sound
                of a string let go from a bump
    beads       the string as a row of beads on a thread: the modes of 5, 15 and 199 beads, and how each sounds
    dalembert   the plucked ideal string over one period by finite differences and by d'Alembert's formula, the two
                travelling halves, and the largest difference between the routes
    modes       the first eight modes, their notes, each as a tone; a finger laid at 1/2 and at 1/3 of a ringing
                string, simulated: which partials survive
    fourier     the pluck as a sum of modes: partial sums, how fast the error falls, and the sums as sound
    pluck       the same note plucked at 1/2, 1/3, 1/5 and 1/10: predicted and simulated partial levels, the sounds
    overtones   one pluck taken apart: each partial's frequency, nearest note and level; each alone, and added back
    coincide    two strings at 2:1, 3:2, 4:3 and a tritone: which partials meet; a fifth mistuned by 12 cents and
                the beat it makes
    real        real strings: the decay of each partial (simulated, against the model's rate) and the sharpening of
                the upper partials by stiffness
    nonlinear   the frontier: a hard pluck stretches the string and sounds sharp (Kirchhoff-Carrier), the glide
                measured; the exact conservation of energy by the ideal scheme; a missing mode stays missing here
    tune        Variation 1: the Tune on one simulated string, with each note's measured pitch
    variation   the Variations ledger, row 1
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, QUIET_LEVEL, SR, Clip, ClipStore, concat, mix, tune
from explainer.music.monochord.dsp import f0_autocorr, partials
from explainer.music.monochord.instruments import MONOCHORD_STRING, anvil, plucked, pure_tone, released
from explainer.music.monochord.instruments.plucked import C3, pluck_partials
from explainer.music.monochord.loudness import integrated, momentary_max, true_peak_db
from explainer.music.monochord.physics import (String, dalembert, energy, pluck_modes, pluck_shape, simulate,
                                               sine_coefficients, stretch_gamma)
from explainer.music.monochord.pitch import cents, nearest_note

CACHE = Cache("music1")
CLIPS = ClipStore("music1")
load = CACHE.load

STRING = MONOCHORD_STRING          # a metre of 0.5 mm steel wire, C3 when open
IDEAL = STRING.with_(kappa=0.0, sigma0=0.0, sigma1=0.0)
EA = 2.0e11 * math.pi * 0.00025 ** 2   # Young's modulus of steel times the wire's cross-section, N
# A string plucked near its end gives a narrow pulse at the bridge once a period: bright, and with peaks far above
# its loudness.  Part 1's examples are therefore set 2.5 LU under the series' usual level, so that every clip keeps
# clear of the true-peak ceiling and all of them are equally loud.
LEVEL = EXAMPLE_LEVEL - 2.5
SOFT = QUIET_LEVEL - 2.5
BETA = 0.11                        # where the monochord is plucked, as a fraction of the sounding length:
#                                    near the end, so that the first eight partials are all strong


def note(stop: float = 1.0, seconds: float = 2.0, beta: float = BETA, release: float | None = None, **kw) -> Clip:
    """One pluck of the monochord with its bridge at ``stop``."""
    return Clip(plucked(seconds=seconds, stop=stop, beta=beta, release=release, **kw)).fade(0.002, 0.04)


def save(name: str, clip: Clip, kind: str = "physical model", level: float = LEVEL, **more) -> dict:
    """Level a clip, label it, store it, and return what the JSON keeps about it."""
    clip = clip.at_level(level).label(kind, **more)
    CLIPS.save(name, clip)
    return {"name": name, "seconds": clip.duration, "level": momentary_max(clip), "true_peak_db": true_peak_db(clip),
            "events": clip.events}


def measured_f0(string: String, beta: float = 0.2371 * 0.9, seconds: float = 0.5) -> float:
    """Simulate the string by finite differences and read its pitch off the motion (autocorrelation)."""
    run = simulate(string, lambda x: pluck_shape(x, string.L, beta, 1e-3), seconds, sr=SR)
    return f0_autocorr(run.pickup, run.sr, 0.45 * string.f1, 2.2 * string.f1)


def tex_frac(fr) -> str:
    fr = Fraction(fr)
    return rf"\tfrac{{{fr.numerator}}}{{{fr.denominator}}}" if fr.denominator != 1 else str(fr.numerator)


# ---------------------------------------------------------------------------
def compute_hammers() -> dict:
    weights = [12, 9, 8, 6]
    pairs = {"octave": (12, 6), "fifth": (12, 8), "fourth": (12, 9)}
    as_weights = {}
    for name, (a, b) in pairs.items():
        r = math.sqrt(a / b)
        heavy, light = STRING.with_(T=STRING.T * a / 6), STRING.with_(T=STRING.T * b / 6)
        m = measured_f0(heavy) / measured_f0(light)
        as_weights[name] = {"weights": [a, b], "ratio": r, "cents": cents(r), "measured_ratio": m,
                            "measured_cents": cents(m), "wanted_cents": cents(a / b)}
    needed = {"octave": [4, 1], "fifth": [9, 4], "fourth": [16, 9]}
    # the anvil of the story: four hammers, one block (illustrative)
    strikes = [Clip(anvil(w / 6.0)).fade(0.0005, 0.2) for w in weights]
    a = concat(strikes, gap=0.05, names=[f"h{w}" for w in weights])
    info = {"anvil": save("hammers.anvil", a, "illustrative")}
    # weights hung on the string: 6 units, then 12 (the legend says an octave), then 24 (what an octave takes)
    w6 = note(seconds=1.7)
    w12 = Clip(plucked(seconds=1.7, string=STRING.with_(T=STRING.T * 2))).fade(0.002, 0.04)
    w24 = Clip(plucked(seconds=2.4, string=STRING.with_(T=STRING.T * 4))).fade(0.002, 0.04)
    info["weights"] = save("hammers.weights", concat([w6, w12], gap=0.12, names=["w6", "w12"]))
    info["four"] = save("hammers.four", concat([w6, w24], gap=0.12, names=["w6", "w24"]))
    # the Tune's first phrase, for the cold open
    info["opening"] = save("hammers.opening", tune_clip(phrases=[0], tail=1.6))
    return {"weights": weights, "as_weights": as_weights, "needed": needed, "clips": info,
            "f_w6": measured_f0(STRING), "f_w12": measured_f0(STRING.with_(T=STRING.T * 2)),
            "f_w24": measured_f0(STRING.with_(T=STRING.T * 4))}


# ---------------------------------------------------------------------------
STOPS = {"octave": Fraction(1, 2), "fifth": Fraction(2, 3), "fourth": Fraction(3, 4)}


def pair_clip(stop: float, first: float = 1.0) -> Clip:
    """The string at ``first``, then at ``stop``, then the two together (as two strings)."""
    a, b = note(first, 1.5), note(stop, 1.5)
    both = mix([(note(first, 3.0), 0.0, 0.0, -0.3), (note(stop, 3.0), 0.0, 0.0, 0.3)])
    return concat([a, b, both], gap=0.15, names=["a", "b", "both"])


def compute_ratios() -> dict:
    f_open = measured_f0(STRING)
    rows, info = {}, {}
    for name, stop in STOPS.items():
        f = measured_f0(STRING.with_(L=STRING.L * float(stop)))
        rows[name] = {"stop": [stop.numerator, stop.denominator], "hz": f, "ratio": f / f_open,
                      "ideal": float(1 / stop), "cents_off": cents(f / f_open / float(1 / stop))}
        info[name] = save(f"ratios.{name}", pair_clip(float(stop)), needs="headphones for the left-right split")
    info["open"] = save("ratios.open", note(1.0, 3.0))
    quiz = concat([concat([note(1.0, 1.1), note(0.75, 1.6)], gap=0.05, names=["a", "b"]),
                   concat([note(1.0, 1.1), note(2 / 3, 1.6)], gap=0.05, names=["a", "b"])], gap=0.7, names=["A", "B"])
    info["quiz"] = save("ratios.quiz", quiz)
    info["tone"] = save("ratios.tone", concat([note(0.75, 1.3), note(2 / 3, 1.8)], gap=0.08, names=["fourth", "fifth"]))
    return {"open_hz": f_open, "formula_hz": STRING.f1, "rows": rows, "clips": info,
            "tone": {"ratio": [9, 8], "cents": cents(Fraction(9, 8))}, "quiz_answer": "B"}


# ---------------------------------------------------------------------------
def compute_mersenne() -> dict:
    base = IDEAL
    lengths = [1.0, 0.9, 0.8, 0.75, 2 / 3, 0.6, 0.5]
    tensions = [1.0, 1.5, 2.0, 3.0, 4.0]
    masses = [1.0, 2.0, 4.0]
    sweep = {
        "length": [{"x": L, "hz": measured_f0(base.with_(L=base.L * L)), "law": base.f1 / L} for L in lengths],
        "tension": [{"x": T, "hz": measured_f0(base.with_(T=base.T * T)), "law": base.f1 * math.sqrt(T)}
                    for T in tensions],
        "mass": [{"x": m, "hz": measured_f0(base.with_(mu=base.mu * m)), "law": base.f1 / math.sqrt(m)}
                 for m in masses],
    }
    rng = np.random.default_rng(1)
    rows, fs, table = [], [], []
    for _ in range(24):
        L, T, mu = rng.uniform(0.3, 1.2), rng.uniform(30, 200), rng.uniform(0.0005, 0.008)
        f = measured_f0(String(L=L, T=T, mu=mu))
        rows.append([1.0, math.log(L), math.log(T), math.log(mu)])
        fs.append(math.log(f))
        table.append({"L": L, "T": T, "mu": mu, "hz": f, "law": math.sqrt(T / mu) / (2 * L)})
    A, y = np.array(rows), np.array(fs)
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ coef
    worst = max(abs(cents(r["hz"] / r["law"])) for r in table)
    # a guitar's top string: 0.010 inch plain steel, 648 mm, E4
    d, Lg, fg = 0.010 * 0.0254, 0.648, 329.63
    mu_g = 7850.0 * math.pi * (d / 2) ** 2
    Tg = mu_g * (2 * Lg * fg) ** 2
    guitar = {"L": Lg, "mu_g_per_m": mu_g * 1000, "hz": fg, "T": Tg, "kgf": Tg / 9.80665,
              "c": math.sqrt(Tg / mu_g), "octave_T": 4 * Tg, "octave_kgf": 4 * Tg / 9.80665}
    info = {
        "length": save("mersenne.length", concat([note(L, 1.0) for L in (1.0, 0.75, 2 / 3, 0.5)], gap=0.06,
                                                 names=["l0", "l1", "l2", "l3"])),
        "tension": save("mersenne.tension", concat(
            [Clip(plucked(seconds=1.0, string=STRING.with_(T=STRING.T * k))).fade(0.002, 0.04) for k in (1, 2, 3, 4)],
            gap=0.06, names=["t1", "t2", "t3", "t4"])),
        "mass": save("mersenne.mass", concat(
            [Clip(plucked(seconds=1.3, string=STRING.with_(mu=STRING.mu * k, T=STRING.T))).fade(0.002, 0.04)
             for k in (1, 4)], gap=0.06, names=["m1", "m4"])),
    }
    return {"sweep": sweep, "exponents": {"L": coef[1], "T": coef[2], "mu": coef[3]}, "constant": math.exp(coef[0]),
            "rms_cents": 1200 / math.log(2) * float(np.sqrt(np.mean(resid ** 2))), "worst_cents": worst,
            "strings": len(table), "table": table, "guitar": guitar, "clips": info,
            "string": {"L": STRING.L, "T": STRING.T, "mu_g_per_m": STRING.mu * 1000, "c": STRING.c, "f1": STRING.f1,
                       "kgf": STRING.T / 9.80665}}


# ---------------------------------------------------------------------------
def bump(x, centre: float, width: float) -> np.ndarray:
    return np.exp(-0.5 * ((np.asarray(x) - centre) / width) ** 2)


def odd_periodic(shape, L: float):
    """The odd, 2L-periodic extension of a shape on [0, L]: what a wave sees when both ends are fixed."""
    def F(z):
        z = np.mod(z, 2 * L)
        return np.where(z <= L, shape(np.minimum(z, L)), -shape(np.clip(2 * L - z, 0, L)))
    return F


def compute_pulse() -> dict:
    N, L, c = 400, 1.0, 1.0
    x = np.linspace(0, L, N + 1)
    frames = 241
    t = np.linspace(0, 2.0, frames)            # one round trip, in units of L / c

    def shape(z):
        return bump(z, 0.25, 0.035)

    def periodic(p):
        """A pulse repeated every 2L: with its mirror image it keeps both ends still for all time."""
        return lambda z: p(np.mod(z + L, 2 * L) - L) + p(np.mod(z + L, 2 * L) + L)

    P = periodic(lambda z: bump(z, 0.25, 0.035))
    Q = periodic(lambda z: bump(z, 0.75, 0.035))
    X, T = x[None, :], c * t[:, None]
    right = P(X - T) - P(-X - T)                               # one pulse sent to the right, and its reflections
    split = dalembert(shape, L, c, x, t)                       # the same bump released from rest: two halves
    cross = right + 0.7 * (Q(X + T) - Q(-X + T))               # a second pulse sent to meet it
    # the same experiment on the monochord's string by finite differences, to measure the speed
    run = simulate(IDEAL, lambda z: 1e-3 * bump(z, 0.2, 0.02), 0.0025, N=600, snapshot_every=1)
    i0, i1 = int(0.3 * 600), int(0.75 * 600)
    t0 = run.t_snap[np.argmax(run.snaps[:, i0])]
    t1 = run.t_snap[np.argmax(run.snaps[:, i1])]
    speed = (run.x[i1] - run.x[i0]) / (t1 - t0)
    # and what the bump sounds like when the monochord's string is let go from it
    bump_clip = save("pulse.bump", Clip(released(lambda z: bump(z, 0.25, 0.035) * (z > 0) * (z < 1), 3.0)).fade(0.002, 0.05),
                     level=LEVEL - 2.0)
    return {"x": x, "t": t, "right": right, "split": split, "cross": cross, "clips": {"bump": bump_clip},
            "speed_measured": float(speed), "speed_formula": IDEAL.c, "round_trip_ms": 2000 * IDEAL.L / IDEAL.c,
            "period_ms": 1000 / IDEAL.f1, "sound_in_air": 343.0}


def beaded(N: int, seconds: float = 2.4, beta: float = BETA) -> tuple[np.ndarray, np.ndarray]:
    """The monochord's string as N - 1 beads on a weightless thread (N segments), plucked and let go: its sound at
    the bridge, and the frequencies of its modes.  A row of beads has exactly N - 1 modes, mode n at
    ``(c N / pi L) sin(n pi / 2N)``: the low ones nearly harmonic, the high ones flat (Lagrange, 1759)."""
    s = STRING
    n = np.arange(1, N)
    hz = (s.c * N / (np.pi * s.L)) * np.sin(n * np.pi / (2 * N))
    hz = hz[hz < 18_000]
    n = n[: len(hz)]
    l = np.arange(N + 1)
    shape = pluck_shape(l / N, 1.0, beta, 1.0)
    a = (2.0 / N) * (np.sin(np.pi * np.outer(n, l) / N) @ shape)        # the pluck in the beads' own modes
    force = a * N * np.sin(n * np.pi / N)                                # the pull of the first thread on the bridge
    t = np.arange(int(seconds * SR)) / SR
    dec = s.sigma0 + s.sigma1 * (2 * np.pi * hz / s.c) ** 2
    y = np.zeros(len(t))
    for i in range(len(n)):
        y += force[i] * np.exp(-dec[i] * t) * np.cos(2 * np.pi * hz[i] * t)
    return (y / np.abs(y).max()).astype(np.float32), hz


def compute_beads() -> dict:
    rows, clips = {}, []
    counts = [6, 16, 200]
    for N in counts:
        y, hz = beaded(N)
        rows[str(N)] = {"segments": N, "beads": N - 1, "modes": int(len(hz)),
                        "flat_cents": [cents(float(hz[k]) / ((k + 1) * STRING.f1)) for k in range(min(len(hz), 12))],
                        "hz": [float(v) for v in hz[:12]]}
        clips.append(Clip(y).fade(0.002, 0.1))
    info = {"three": save("beads.three", concat(clips, gap=0.15, names=[f"n{N}" for N in counts]))}
    return {"counts": counts, "rows": rows, "clips": info}


def compute_dalembert() -> dict:
    N = 240
    s = IDEAL
    out = {}
    for key, beta in (("b20", 0.2), ("b50", 0.5)):
        def shape(z, beta=beta):
            return pluck_shape(z, s.L, beta, 1.0)
        run = simulate(s, shape, 1.0 / s.f1 + 1e-9, N=N, snapshot_every=2)
        exact = dalembert(shape, s.L, s.c, run.x, run.t_snap)
        F = odd_periodic(shape, s.L)
        out[key] = run.snaps
        out[key + "_right"] = 0.5 * F(run.x[None, :] - s.c * run.t_snap[:, None])
        out[key + "_left"] = 0.5 * F(run.x[None, :] + s.c * run.t_snap[:, None])
        out[key + "_error"] = float(np.abs(run.snaps - exact).max())
    out.update({"x": run.x / s.L, "frames": len(run.t_snap), "dt": float(run.t_snap[1]), "period": 1.0 / s.f1,
                "courant": run.courant, "beads": N - 1, "rate": run.sr})
    return out


# ---------------------------------------------------------------------------
def compute_modes() -> dict:
    n = np.arange(1, 9)
    hz_ideal = IDEAL.f1 * n
    table = []
    for k, f in zip(n, hz_ideal):
        name, off = nearest_note(float(f))
        table.append({"n": int(k), "hz": float(f), "hz_stiff": float(STRING.mode_freq(k)), "note": name,
                      "cents": off, "ratio_to_previous": f"{k}:{k - 1}" if k > 1 else ""})
    tones = [Clip(pure_tone(float(f), 0.85, decay=1.2)).fade(0.01, 0.08) for f in hz_ideal]
    info = {"series": save("modes.series", concat(tones, gap=0.05, names=[f"m{k}" for k in n]), "synthesized")}
    touch = {}
    for key, where, harmonic in (("half", 0.5, 2), ("third", 1 / 3, 3)):
        run = simulate(STRING, lambda x: pluck_shape(x, STRING.L, 0.137, 1e-3), 3.0, sr=SR, damper=(where, 6.0, 1.0))
        cen = STRING.mode_freq(np.arange(1, 10))
        before = partials(run.force[int(0.55 * SR): int(0.95 * SR)], SR, STRING.f1, 9, centers=cen)
        after = partials(run.force[int(1.5 * SR): int(1.9 * SR)], SR, STRING.f1, 9, centers=cen)
        ref = max(p["db"] for p in before)
        touch[key] = {"where": where, "harmonic": harmonic, "before_db": [p["db"] - ref for p in before],
                      "after_db": [p["db"] - ref for p in after], "at": 1.0,
                      "pitch_after": f0_autocorr(run.force[int(1.5 * SR): int(2.2 * SR)], SR, 100, 900)}
        y = run.force / np.abs(run.force).max()
        info[key] = save(f"modes.touch_{key}", Clip(y, events={"touch": 1.0}).fade(0.002, 0.3))
    return {"table": table, "touch": touch, "clips": info}


def compute_fourier() -> dict:
    beta = 0.2
    x = np.linspace(0, 1, 401)
    target = pluck_shape(x, 1.0, beta, 1.0)
    a = pluck_modes(200, beta, 1.0)
    modes = np.sin(np.pi * np.outer(np.arange(1, 201), x))
    partial = np.cumsum(a[:, None] * modes, axis=0)          # row N-1 is the sum of the first N modes
    err = np.abs(partial - target[None, :]).max(axis=1)
    counts = [1, 2, 3, 5, 10, 30, 100]
    slope = float(np.polyfit(np.log(np.arange(20, 201)), np.log(err[19:]), 1)[0])
    # the same sums as sound: the monochord's string plucked at the same point, with only its first N modes
    heard = [1, 2, 3, 5, 10, 30]
    steps = [Clip(plucked(seconds=1.0, beta=beta, only=list(range(1, N + 1)))).fade(0.003, 0.08) for N in heard]
    steps.append(note(1.0, 2.2, beta=beta))
    info = {"build": save("fourier.build", concat(steps, gap=0.08, names=[f"n{N}" for N in heard] + ["all"]))}
    return {"x": x, "target": target, "a": a[:30], "counts": counts, "sums": partial[[c - 1 for c in counts]],
            "heard": heard, "heard_sums": partial[[c - 1 for c in heard]], "clips": info,
            "terms": a[:8, None] * modes[:8], "error": err, "error_slope": slope, "beta": beta,
            "numeric": sine_coefficients(target, 8)}


# ---------------------------------------------------------------------------
PLUCKS = {"b50": 0.5, "b33": 1 / 3, "b20": 0.2, "b10": 0.1}


def compute_pluck() -> dict:
    count = 16
    n = np.arange(1, count + 1)
    rows, info = {}, {}
    for key, beta in PLUCKS.items():
        shape_db = 20 * np.log10(np.maximum(np.abs(np.sin(n * np.pi * beta)) / n ** 2, 1e-9))
        force_db = 20 * np.log10(np.maximum(np.abs(np.sin(n * np.pi * beta)) / n, 1e-9))
        run = simulate(STRING, lambda x, beta=beta: pluck_shape(x, STRING.L, beta, 1e-3), 0.25, sr=SR)
        W = 0.1  # the stretch of sound analysed; each partial fades a little inside it, by the model's own rate
        got = partials(run.force[: int(W * SR)], SR, STRING.f1, count, centers=STRING.mode_freq(n), search=0.3)
        meas = np.array([p["db"] for p in got])
        fade = STRING.mode_decay(n) * W
        force_db = force_db + 20 * np.log10((1 - np.exp(-fade)) / fade)
        ref_m, ref_f = meas.max(), force_db.max()
        strong = force_db - ref_f > -30
        rows[key] = {"beta": beta, "shape_db": (shape_db - shape_db.max()).tolist(),
                     "force_db": (force_db - ref_f).tolist(), "measured_db": (meas - ref_m).tolist(),
                     "worst_db": float(np.abs((meas - ref_m) - (force_db - ref_f))[strong].max()),
                     "missing": [int(k) for k in n if abs(math.sin(k * math.pi * beta)) < 1e-9]}
        info[key] = save(f"pluck.{key}", note(1.0, 2.0, beta=beta))
    betas = [0.5, 0.4, 0.3, 0.2, 0.12, 0.07]
    info["sweep"] = save("pluck.sweep", concat([note(1.0, 0.95, beta=b) for b in betas], gap=0.05,
                                               names=[f"p{i}" for i in range(len(betas))]))
    info["quiz"] = save("pluck.quiz", concat([note(1.0, 1.6, beta=0.1), note(1.0, 1.6, beta=0.5)], gap=0.5,
                                             names=["A", "B"]))
    return {"rows": rows, "sweep_betas": betas, "clips": info, "quiz_answer": "B", "count": count}


def compute_overtones() -> dict:
    p = pluck_partials(STRING, BETA)
    table = []
    for k in range(10):
        f = float(p["hz"][k])
        name, off = nearest_note(f)
        table.append({"n": k + 1, "hz": f, "note": name, "cents": off,
                      "db": float(20 * np.log10(max(abs(p["force"][k]), 1e-9))), "decay": float(p["decay"][k]),
                      "t60": float(6.908 / p["decay"][k])})
    whole = note(1.0, 3.2)
    info = {"whole": save("overtones.whole", whole)}
    each = [Clip(plucked(seconds=0.85, only=[k])).fade(0.01, 0.08).at_level(LEVEL) for k in range(1, 9)]
    info["each"] = save("overtones.each", concat(each, gap=0.05, names=[f"p{k}" for k in range(1, 9)]),
                        detail="each partial raised to the same loudness")
    probe = Clip(pure_tone(float(p["hz"][2]), 1.3, decay=0.6)).fade(0.02, 0.15).gain(-12)
    info["find"] = save("overtones.find", concat([probe, note(1.0, 3.0)], gap=0.5, names=["tone", "pluck"]))
    chord = [t["note"] for t in table[3:6]]
    return {"table": table, "clips": info, "beta": BETA, "chord": chord, "open_note": table[0]["note"]}


# ---------------------------------------------------------------------------
INTERVALS = {"octave": Fraction(2, 1), "fifth": Fraction(3, 2), "fourth": Fraction(4, 3), "tritone": Fraction(45, 32)}


def two(ratio: float, seconds: float = 3.2) -> Clip:
    lo, hi = note(1.0, seconds), note(1.0 / ratio, seconds)
    return mix([(lo, 0.0, 0.0, -0.3), (hi, 0.0, 0.0, 0.3)])


def compute_coincide() -> dict:
    f = IDEAL.f1
    rows, info = {}, {}
    for name, r in INTERVALS.items():
        lower = [f * n for n in range(1, 13)]
        upper = [f * float(r) * m for m in range(1, 13) if f * float(r) * m <= lower[-1] * 1.0001]
        meets = [(n, m) for n in range(1, 13) for m in range(1, 13) if Fraction(n) == r * m]
        near = sorted(((abs(cents(lo / up)), n, m) for n, lo in enumerate(lower, 1) for m, up in enumerate(upper, 1)
                       if 1e-9 < abs(cents(lo / up)) < 100), key=lambda z: z[0])
        rows[name] = {"ratio": [r.numerator, r.denominator], "cents": cents(r), "lower": lower, "upper": upper,
                      "meets": meets, "count": len(meets),
                      "near_misses": [{"cents": c_, "n": n, "m": m, "beat_hz": abs(lower[n - 1] - upper[m - 1])}
                                      for c_, n, m in near[:4]]}
        seq = concat([note(1.0, 1.2), note(float(1 / r), 1.2), two(float(r))], gap=0.12, names=["lo", "hi", "both"])
        info[name] = save(f"coincide.{name}", seq, needs="headphones for the left-right split")
    off = 12.0
    r_bad = 1.5 * 2 ** (off / 1200)
    beat = abs(3 * f - 2 * f * r_bad)
    pair = Clip(0.5 * (pure_tone(3 * f, 3.0) + pure_tone(2 * f * r_bad, 3.0))).fade(0.02, 0.2)
    seq = concat([pair.at_level(SOFT + 3), two(r_bad, 4.0).at_level(LEVEL), two(1.5, 4.0).at_level(LEVEL)],
                 gap=0.4, names=["pair", "mistuned", "pure"])
    info["beats"] = save("coincide.beats", seq, needs="headphones for the left-right split")
    return {"rows": rows, "clips": info, "mistuned": {"cents": off, "ratio": r_bad, "beat_hz": beat,
                                                       "lower_partial": 3, "upper_partial": 2,
                                                       "hz": [3 * f, 2 * f * r_bad]}}


# ---------------------------------------------------------------------------
def compute_real() -> dict:
    count = 12
    n = np.arange(1, count + 1)
    run = simulate(STRING, lambda x: pluck_shape(x, STRING.L, BETA, 1e-3), 2.0, sr=SR)
    cen = STRING.mode_freq(n)
    win, starts = int(0.25 * SR), [int(0.05 * SR), int(0.85 * SR)]
    a = partials(run.force[starts[0]: starts[0] + win], SR, STRING.f1, count, centers=cen)
    b = partials(run.force[starts[1]: starts[1] + win], SR, STRING.f1, count, centers=cen)
    dt = (starts[1] - starts[0]) / SR
    measured = [(p["db"] - q["db"]) / 20 * math.log(10) / dt for p, q in zip(a, b)]
    model = STRING.mode_decay(n).tolist()
    stiff = STRING.with_(kappa=STRING.kappa * 6.0)       # a wire six times as stiff: a thin rod more than a string
    rows = []
    for k in n:
        rows.append({"n": int(k), "decay_measured": float(measured[k - 1]), "decay_model": float(model[k - 1]),
                     "t60": float(6.908 / model[k - 1]),
                     "sharp_cents": cents(float(STRING.mode_freq(k)) / (k * STRING.f1)),
                     "sharp_cents_stiff": cents(float(stiff.mode_freq(k)) / (k * stiff.f1)),
                     "measured_hz": a[k - 1]["hz"]})
    good = [r for r in rows if r["n"] <= 8]
    info = {
        "ideal": save("real.ideal", Clip(plucked(seconds=2.6, string=IDEAL)).fade(0.002, 0.25)),
        "damped": save("real.damped", note(1.0, 2.6)),
        "stiff": save("real.stiff", Clip(plucked(seconds=2.6, string=stiff)).fade(0.002, 0.1)),
    }
    return {"rows": rows, "B": STRING.B, "B_stiff": stiff.B, "clips": info,
            "decay_worst_rel": max(abs(r["decay_measured"] / r["decay_model"] - 1) for r in good),
            "measured_sharp_8": cents(a[7]["hz"] / (8 * a[0]["hz"])), "wire_mm": 0.5}


def glide(signal: np.ndarray, string: String, win: float = 0.12, hop: float = 0.06) -> tuple[list, list]:
    """The frequency of the lowest partial in successive windows."""
    times, f = [], []
    n, h = int(win * SR), int(hop * SR)
    for i in range(0, len(signal) - n, h):
        times.append((i + n / 2) / SR)
        f.append(partials(signal[i:i + n], SR, string.f1, 1, search=0.2)[0]["hz"])
    return times, f


def compute_nonlinear() -> dict:
    s = STRING
    out, info = {}, {}
    g = stretch_gamma(s, EA)
    for key, h in (("soft", 1e-3), ("hard", 1e-2)):
        run = simulate(s, lambda x, h=h: pluck_shape(x, s.L, BETA, h), 2.6, sr=SR, EA=EA, headroom=1.3)
        times, f = glide(run.pickup, s)
        mean_t = [float(run.tension[int((t - 0.06) * SR): int((t + 0.06) * SR)].mean()) for t in times]
        ref = float(s.mode_freq(1))
        out[key] = {"height_mm": h * 1000, "times": times, "cents": [cents(v / ref) for v in f],
                    "estimate_cents": [cents(math.sqrt(v)) for v in mean_t],
                    "tension_start": float(run.tension[0]),
                    "static_formula": 1 + g * h * h / (BETA * (1 - BETA) * s.L),
                    "start_cents": cents(f[0] / ref), "end_cents": cents(f[-1] / ref)}
        y = run.force / np.abs(run.force).max()
        info[key] = save(f"nonlinear.{key}", Clip(y).fade(0.002, 0.3))
    # the ideal scheme conserves its energy exactly
    ideal = simulate(IDEAL, lambda x: pluck_shape(x, IDEAL.L, BETA, 1e-3), 0.1, N=300, snapshot_every=1)
    e = energy(ideal.snaps, IDEAL, ideal.sr)
    # a mode with a node at the plucking point: does stretching bring it back?  Pluck at 1/3 and follow the third
    # mode's amplitude, read off the string's shape (its sine coefficient), with and without the stretching.
    def third_mode(ea):
        r = simulate(s, lambda x: pluck_shape(x, s.L, 1 / 3, 1e-2), 0.5, sr=SR, EA=ea, headroom=1.3,
                     snapshot_every=24)
        a = np.array([sine_coefficients(shape, 3) for shape in r.snaps])
        return float(np.abs(a[:, 2]).max() / np.abs(a[:, 0]).max())

    third = {"stretching": third_mode(EA), "linear": third_mode(0.0)}
    return {"runs": out, "clips": info, "gamma": g, "EA": EA, "steps": len(e),
            "energy_drift": float(np.abs(e / e[0] - 1).max()),
            "third_mode": third}


# ---------------------------------------------------------------------------
def tune_clip(beat: float = 0.55, phrases=None, tail: float = 2.2) -> Clip:
    """The Tune on the monochord: one string, one movable bridge.  Each note is a pluck with the bridge at
    ``1 / ratio`` of the string; the string is stilled 40 ms before the bridge moves for the next note."""
    ev = tune.events(beat, phrases)
    placed, notes, events = [], [], {}
    for k, e in enumerate(ev):
        stop = float(1 / e["ratio"])
        last = k == len(ev) - 1
        dur = e["dur"] + (tail if last else 0.0)
        y = plucked(seconds=dur + 0.05, stop=stop, beta=BETA, release=None if last else e["dur"] - 0.04)
        accent = 0.0 if k % 2 == 0 else -1.5      # the second of each pair a little softer, as a hand does it
        placed.append((Clip(y).fade(0.002, 0.03 if not last else 0.5), e["t"], accent))
        events[f"n{k}"] = e["t"]
        notes.append({"t": e["t"], "dur": e["dur"], "hz": C3 * float(e["ratio"]), "name": e["name"],
                      "degree": e["degree"], "ratio": [e["ratio"].numerator, e["ratio"].denominator],
                      "stop": stop, "phrase": e["phrase"]})
    c = mix(placed)
    events.update({f"phrase{p}": min(n["t"] for n in notes if n["phrase"] == p) for p in {n["phrase"] for n in notes}})
    events["end"] = ev[-1]["t"] + ev[-1]["dur"]
    return Clip(c.y, SR, events, notes)


def compute_tune() -> dict:
    c = tune_clip()
    info = save("tune.variation1", c)
    stored = CLIPS.load("tune.variation1")
    checks, seen = [], set()
    for nrow in stored.notes:
        if nrow["name"] in seen:
            continue
        seen.add(nrow["name"])
        a = int((nrow["t"] + 0.06) * SR)
        b = int((nrow["t"] + min(nrow["dur"], 0.5) - 0.02) * SR)
        f = f0_autocorr(stored.mono[a:b], SR, 0.6 * nrow["hz"], 1.6 * nrow["hz"])
        checks.append({"name": nrow["name"], "ratio": nrow["ratio"], "stop": nrow["stop"], "hz": f})
    f_open = next(k["hz"] for k in checks if k["name"] == "C")
    for k in checks:   # each note's interval above the open string, against the ratio it was stopped at
        k["interval_cents"] = cents(k["hz"] / f_open)
        k["cents_off"] = cents(k["hz"] / f_open / (k["ratio"][0] / k["ratio"][1]))
    return {"clip": info, "notes": stored.notes, "checks": checks, "seconds": stored.duration,
            "stops": sorted({round(n["stop"], 6) for n in stored.notes}, reverse=True), "open_hz": f_open,
            "open_sharp_cents": cents(f_open / STRING.f1),
            "worst_cents": max(abs(k["cents_off"]) for k in checks), "integrated_lufs": integrated(stored)}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 1, "title": r"on one simulated string: six positions of one bridge",
            "seconds": t["seconds"], "key": "C", "beat": 0.55,
            "measure": rf"every interval within {max(t['worst_cents'], 0.1):.1f} cents of its ratio",
            "clip": "tune.variation1"}


ITEMS = {"hammers": compute_hammers, "ratios": compute_ratios, "mersenne": compute_mersenne, "pulse": compute_pulse,
         "beads": compute_beads, "dalembert": compute_dalembert, "modes": compute_modes, "fourier": compute_fourier, "pluck": compute_pluck,
         "overtones": compute_overtones, "coincide": compute_coincide, "real": compute_real,
         "nonlinear": compute_nonlinear, "tune": compute_tune, "variation": compute_variation}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
