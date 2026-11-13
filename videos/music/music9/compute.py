"""Precompute everything numerical, and every sound, in Part 9 of *Music, Built* ("Drums, Bars and Bells").

    python -m videos.music.music9.compute              # everything missing (under a minute)
    python -m videos.music.music9.compute --force bars

Numbers are cached in ``.cache/music9/<name>.json`` (+ ``.npz``), sounds in ``.cache/music9/audio/``.  The
instruments are Monochord's (``explainer/music/monochord/instruments/percussion.py``); published values are cited in
the README.

Items:
    hook        a string and a drum on the same note
    skin        the modes of a round skin: Bessel zeros, shapes, where it is struck
    timpani     a bare skin, an estimate of the air's load, a kettledrum's measured modes; which has a pitch
    tabla       a skin loaded at its centre: the modes against the weight of the patch
    bars        a free bar: uniform, and with the arch of a marimba and of a xylophone cut under it
    bells       a tuned bell's partials; the note the ear gives it, with and without its prime; a major-third bell
    plates      Chladni's figures on a square plate (Ritz's approximation)
    gongs       gongs whose pitch falls or rises as they die away; a cymbal's crowd of partials
    pan         a steelpan note built partial by partial
    shape       two drums of different shape with one spectrum; a square of the same area; Weyl's count
    tune        Variation 9: the Tune for marimba, bells, steelpan and kettledrums
    variation   the Variations ledger, row 9
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import ear
from explainer.music.monochord.instruments import percussion as P
from explainer.music.monochord.partkit import play_tune, saver, string_note
from explainer.music.monochord.pitch import cents

CACHE = Cache("music9")
CLIPS = ClipStore("music9")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
C3, C4, C5 = 130.8127826502993, 261.6255653005986, 523.2511306011972


def clip(y, fade=(0.001, 0.08)) -> Clip:
    return Clip(np.asarray(y, dtype=np.float64)).fade(*fade)


def heard(y, lo=60.0, hi=1200.0) -> tuple[float, float]:
    """The pitch Part 4's model of the ear gives a sound, and how sure it is."""
    n = min(len(y), int(0.5 * SR))
    return ear.pitch(np.asarray(y[int(0.02 * SR): n], dtype=float), SR, lo=lo, hi=hi)


# ---------------------------------------------------------------------------
def compute_hook() -> dict:
    hz = C3
    s = string_note(1.0, 2.0)
    d = clip(P.drum(hz, 2.0, at=0.45))
    seq = concat([s.at_level(LEVEL), d.at_level(LEVEL)], gap=0.5, names=["string", "drum"])
    modes = P.drum_modes(8)
    ps, pd = heard(s.mono), heard(d.mono)
    return {"hz": hz, "string": [1, 2, 3, 4, 5, 6, 7, 8], "drum": [r["ratio"] for r in modes], "string_salience": ps[1], "drum_salience": pd[1],
            "clips": {"pair": save("hook.pair", seq, level=None, detail="Part 1's string, then a round drum whose lowest mode is the same note")}}


def compute_skin() -> dict:
    modes = P.drum_modes(12)
    shapes = {f"shape{k}": np.nan_to_num(P.drum_shape(r["m"], r["n"], 81), nan=0.0) for k, r in enumerate(modes[:6])}
    mask = ~np.isnan(P.drum_shape(0, 1, 81))
    centre, off = P.strike_amounts(modes, 0.0), P.strike_amounts(modes, 0.6)
    hz = 110.0
    a = clip(P.drum(hz, 1.6, at=0.0)).at_level(LEVEL)
    b = clip(P.drum(hz, 1.6, at=0.6)).at_level(LEVEL)
    seq = concat([b, a], gap=0.5, names=["A", "B"])
    from scipy.special import jn_zeros
    return {"modes": modes, **shapes, "mask": mask.astype(float), "centre": centre, "off": off, "hz": hz,
            "zeros": {"j01": float(jn_zeros(0, 1)[0]), "j11": float(jn_zeros(1, 1)[0])}, "minor_sixth_cents": cents(modes[1]["ratio"] / 1.6),
            "quiz_answer": "B",
            "clips": {"where": save("skin.where", seq, level=None, detail="one drum struck twice: off centre, then dead centre")}}


def compute_timpani() -> dict:
    rows = P.air_loaded()
    measured = P.TIMPANI_MEASURED
    series = [1.0, 1.5, 2.0, 2.5, 3.0]
    off = lambda rs: [cents(r / s) for r, s in zip(rs, series)]      # noqa: E731
    hz = 165.0                                                     # the kettledrum's note: its (1,1) mode
    bare = P.drum(hz / 1.593, 2.0, at=0.75)                        # a bare skin with the same (1,1) mode
    kettle = P.drum(hz, 2.0, tuned="timpani")
    pb, pk = heard(bare, 40.0, 400.0), heard(kettle, 40.0, 400.0)
    seq = concat([clip(bare).at_level(LEVEL), clip(kettle).at_level(LEVEL)], gap=0.5, names=["A", "B"])
    beat = 0.55
    notes = [C3, C3, C3 * 1.5, C3 * 1.5]
    phrase = mix([(clip(P.drum(f, 1.4, tuned="timpani")).at_level(LEVEL), k * beat) for k, f in enumerate(notes)]).at_level(LEVEL)
    phrase = Clip(phrase.y, SR, {f"n{k}": k * beat for k in range(4)})
    return {"plain": [r["plain_ratio"] for r in rows], "estimate": [r["loaded_ratio"] for r in rows], "measured": measured, "series": series,
            "off_plain": off([r["plain_ratio"] for r in rows]), "off_estimate": off([r["loaded_ratio"] for r in rows]), "off_measured": off(measured),
            "hz": hz, "bare_pitch": pb[0], "bare_salience": pb[1], "kettle_pitch": pk[0], "kettle_salience": pk[1], "quiz_answer": "B",
            "clips": {"pair": save("timpani.pair", seq, level=None, detail="a bare skin, then a kettledrum, tuned alike"),
                      "notes": save("timpani.notes", phrase, level=None, detail="four notes on model kettledrums")}}


def compute_tabla() -> dict:
    patch, density = 0.4, 9.76
    bare = P.drum_modes(9)
    rows = P.tabla_modes(patch, density, 9)
    ds = np.arange(1.0, 16.01, 0.5)
    miss = [P.harmonic_misfit([r["ratio"] for r in P.tabla_modes(patch, float(d), 9)]) for d in ds]
    best = float(ds[int(np.argmin(miss))])
    hz = 196.0
    fb = [hz * r["ratio"] for r in bare]
    fl = [hz * r["ratio"] for r in rows]
    amps = [1.0, 0.8, 0.6, 0.5, 0.4, 0.35, 0.25, 0.2, 0.15]
    dec = [3.0 + 0.8 * k for k in range(9)]
    ya, yb = P.modal(fb, amps, dec, 1.8), P.modal(fl, amps, dec, 1.8)
    seq = concat([clip(ya).at_level(LEVEL), clip(yb).at_level(LEVEL)], gap=0.5, names=["bare", "loaded"])
    return {"patch": patch, "density": density, "bare": bare, "rows": rows, "densities": ds, "misfit": miss, "best_density": best,
            "bare_misfit": P.harmonic_misfit([r["ratio"] for r in bare]), "loaded_misfit": P.harmonic_misfit([r["ratio"] for r in rows]),
            "bare_salience": heard(ya)[1], "loaded_salience": heard(yb)[1],
            "clips": {"pair": save("tabla.pair", seq, level=None, detail="a round skin with the same nine modes sounding: bare, then with a heavy patch at its centre")}}


def compute_bars() -> dict:
    uniform, shapes = P.bar_modes(np.ones(240), count=4, shapes=True)
    mar, xyl = P.tune_bar(4.0), P.tune_bar(3.0)
    x = (np.arange(240) + 0.5) / 240
    hz = C4
    plain = P.marimba(hz, 1.8, tuned=False, soft=0.4)
    tuned = P.modal([hz * r for r in mar["ratios"][:3]], np.array([1.0, 0.28, 0.1]) * P.mallet([hz * r for r in mar["ratios"][:3]], 0.4), [2.4, 9.0, 18.0], 1.8)
    seq = concat([clip(plain).at_level(LEVEL), clip(tuned).at_level(LEVEL)], gap=0.5, names=["A", "B"])
    two_octaves = cents(mar["ratios"][1] / 4.0)
    # the same carved bar under a soft mallet and a hard one: the blow lasts longer or shorter
    fm = [hz * r for r in mar["ratios"][:4]]
    base = np.array([1.0, 0.6, 0.45, 0.3])
    soft_w, hard_w = base * P.mallet(fm, 1.6), base * P.mallet(fm, 0.25)
    decs = [2.4, 9.0, 18.0, 30.0]
    mal = concat([clip(P.modal(fm, soft_w, decs, 1.6)).at_level(LEVEL), clip(P.modal(fm, hard_w, decs, 1.6)).at_level(LEVEL)], gap=0.5, names=["soft", "hard"])
    return {"uniform": uniform, "x": x, "shape0": shapes[0], "shape1": shapes[1], "shape2": shapes[2],
            "marimba": {"depth": mar["depth"], "width": mar["width"], "ratios": [float(v) for v in mar["ratios"]], "lowered": float(mar["lowered"]),
                        "octaves_down": -math.log2(mar["lowered"])},
            "xylophone": {"depth": xyl["depth"], "ratios": [float(v) for v in xyl["ratios"]], "lowered": float(xyl["lowered"])},
            "profile_marimba": P.arch(mar["depth"], 0.6, power=3.0), "profile_xylophone": P.arch(xyl["depth"], 0.6, power=3.0),
            "uniform_intervals": [cents(r) for r in uniform], "hz": hz, "two_octave_error": two_octaves, "quiz_answer": "B",
            "worked": {"half_length": 4.0, "half_thickness": 0.5},
            "mallets": {"soft_ms": 1.6, "hard_ms": 0.25, "soft_db": [float(20 * np.log10(max(v, 1e-6) / soft_w[0])) for v in soft_w],
                        "hard_db": [float(20 * np.log10(max(v, 1e-6) / hard_w[0])) for v in hard_w]},
            "clips": {"pair": save("bars.pair", seq, level=None, detail="one note on two wooden bars: a plain bar, then a bar with an arch cut beneath it"),
                      "mallets": save("bars.mallets", mal, level=None, detail="one carved bar, struck with a soft mallet and then a hard one")}}


def compute_bells() -> dict:
    prime = C4
    parts = P.bell_partials(prime)
    y = P.bell(prime, 4.0)
    f = [q["hz"] for q in parts]
    a = [q["amp"] for q in parts]
    dec = [d * (prime / 262.0) ** 0.5 for _, _, _, d in P.BELL]
    keep = [k for k, q in enumerate(parts) if q["name"] != "prime"]
    y_no = P.modal([f[k] for k in keep], [a[k] for k in keep], [dec[k] for k in keep], 4.0, attack=0.002)
    upper = [k for k, q in enumerate(parts) if q["name"] in ("nominal", "twelfth", "upper octave")]
    y_up = P.modal([f[k] for k in upper], [a[k] for k in upper], [dec[k] for k in upper], 4.0, attack=0.002)
    p_all, p_no, p_up = heard(y, 100.0, 700.0), heard(y_no, 100.0, 700.0), heard(y_up, 100.0, 700.0)
    strike = concat([clip(y[: int(2.6 * SR)], (0.001, 0.4)).at_level(LEVEL), clip(y_up[: int(2.6 * SR)], (0.001, 0.4)).at_level(LEVEL - 3)], gap=0.4, names=["whole", "three"])
    five = [k for k, q in enumerate(parts) if q["name"] in ("hum", "prime", "tierce", "quint", "nominal")]
    singles = [clip(P.modal([f[k]], [1.0], [1.6], 1.0), (0.004, 0.25)).at_level(LEVEL - 4) for k in five]
    apart = concat(singles + [clip(y[: int(2.8 * SR)], (0.001, 0.4)).at_level(LEVEL)], gap=0.12, names=[parts[k]["name"] for k in five] + ["all"])
    major = P.bell(prime, 4.0, tierce=1.25)
    # which bell is the old kind?  A: the major third.  B: the minor third.
    chord = lambda t: mix([(clip(P.bell(prime * r, 3.0, tierce=t), (0.001, 0.5)).at_level(LEVEL), 0.0) for r in (1.0, 1.25, 1.5)]).at_level(LEVEL)      # noqa: E731
    quiz = concat([clip(major[: int(2.6 * SR)], (0.001, 0.4)).at_level(LEVEL), clip(y[: int(2.6 * SR)], (0.001, 0.4)).at_level(LEVEL)], gap=0.4, names=["A", "B"])
    chords = concat([chord(1.2), chord(1.25)], gap=0.5, names=["minor", "major"])
    return {"prime": prime, "partials": parts, "heard": p_all[0], "heard_without_prime": p_no[0], "heard_upper_only": p_up[0],
            "heard_cents": cents(p_all[0] / prime), "without_cents": cents(p_no[0] / prime), "upper_cents": cents(p_up[0] / prime),
            "tierce_cents": cents(1.2), "major_cents": cents(1.25), "quiz_answer": "B",
            "clips": {"apart": save("bells.apart", apart, kind="synthesized", level=None, detail="a bell's five lowest partials, one at a time; then the bell"),
                      "strike": save("bells.strike", strike, kind="synthesized", level=None, detail="a bell from its measured partials; then only three of them, at two, three and four times its note"),
                      "quiz": save("bells.quiz", quiz, kind="synthesized", level=None, detail="two bells on the same note: one with a major third among its partials, one with a minor"),
                      "chords": save("bells.chords", chords, kind="synthesized", level=None, detail="a major chord on three minor-third bells, then on three major-third bells")}}


def compute_plates() -> dict:
    figs = [(1, 1, 1), (2, 0, -1), (2, 0, 1), (2, 1, 1), (3, 1, -1), (3, 1, 1), (4, 2, 1), (5, 2, -1)]
    out = {f"fig{k}": P.chladni(m, n, s, 141) for k, (m, n, s) in enumerate(figs)}
    return {**out, "figs": [{"m": m, "n": n, "sign": s, "pitch": P.chladni_pitch(m, n)} for m, n, s in figs]}


def compute_gongs() -> dict:
    hz = 220.0
    t = np.linspace(0, 3.0, 300)
    down, up = P.gong(hz, 3.0, glide=0.12), P.gong(hz * 1.6, 2.4, glide=-0.10, decay=1.8)
    seq = concat([clip(down, (0.001, 0.3)).at_level(LEVEL), clip(up, (0.001, 0.3)).at_level(LEVEL)], gap=0.5, names=["falls", "rises"])
    # a cymbal: hundreds of modes, evenly crowded in frequency, the high ones arriving a moment late
    rng = np.random.default_rng(9)
    n = 420
    f = np.sort(rng.uniform(280.0, 13000.0, n))
    tt = np.arange(int(3.0 * SR)) / SR
    y = np.zeros(len(tt))
    for fk in f:
        late = 0.004 + 0.05 * (fk / 13000.0)                      # energy takes time to reach the high modes
        env = (1 - np.exp(-tt / late)) * np.exp(-tt * (0.9 + 2.2 * fk / 13000.0))
        y += (1.0 / math.sqrt(n)) * env * np.sin(2 * np.pi * fk * tt + rng.uniform(0, 2 * np.pi))
    crash = clip(y, (0.001, 0.4)).at_level(LEVEL)
    return {"hz": hz, "t": t, "down": P.gong_pitch(hz, 0.12, t), "up": P.gong_pitch(hz * 1.6, -0.10, t, 1.8), "down_cents": cents(1.12), "up_cents": cents(0.90),
            "cymbal_modes": n, "cymbal_lo": 280.0, "cymbal_hi": 13000.0,
            "clips": {"pair": save("gongs.pair", seq, kind="synthesized", level=None, detail="two gongs: one whose pitch falls as it dies away, one whose pitch rises"),
                      "crash": save("gongs.crash", crash, kind="synthesized", level=None, detail="a sketch of a cymbal: 420 partials with no pattern, the high ones arriving late")}}


def compute_pan() -> dict:
    hz = 392.0
    t = np.arange(int(1.6 * SR)) / SR
    env = np.clip(t / 0.002, 0, 1)
    one = env * np.exp(-2.2 * t) * np.sin(2 * np.pi * hz * t)
    two = one + 0.55 * env * (1 - np.exp(-t / 0.03)) * np.exp(-3.0 * t) * np.sin(2 * np.pi * 2 * hz * t)
    three = P.steelpan(hz, 1.6)
    rough = one + 0.55 * env * np.exp(-3.0 * t) * np.sin(2 * np.pi * 2.27 * hz * t) + 0.25 * env * np.exp(-4.0 * t) * np.sin(2 * np.pi * 3.41 * hz * t)
    seq = concat([clip(x).at_level(LEVEL) for x in (rough, one, two, three)], gap=0.35, names=["untuned", "one", "two", "three"])
    return {"hz": hz, "partials": [1, 2, 3, 4], "untuned": [1.0, 2.27, 3.41],
            "clips": {"build": save("pan.build", seq, kind="synthesized", level=None, detail="one steelpan note: before tuning; then its partials tuned and added one by one")}}


def compute_shape() -> dict:
    import matplotlib.tri as mtri

    n = 24
    count = 12
    w1, xy1, v1 = P.membrane_eigs(P.GWW_1, count, n, shapes=True)
    w2, xy2, v2 = P.membrane_eigs(P.GWW_2, count, n, shapes=True)
    fine = P.membrane_eigs(P.GWW_1, 5, 40)
    side = math.sqrt(3.5)
    sq = sorted((np.pi / side) ** 2 * (a * a + b * b) for a in range(1, 8) for b in range(1, 8))[:count]

    def raster(xy, v, k, grid=121):
        gx = np.linspace(0, 3, grid)
        gxx, gyy = np.meshgrid(gx, gx)
        tri = mtri.Triangulation(xy[:, 0], xy[:, 1])
        z = mtri.LinearTriInterpolator(tri, v[k])(gxx, gyy)
        return np.nan_to_num(np.asarray(z.filled(np.nan)), nan=0.0)

    from matplotlib.path import Path
    gx = np.linspace(0, 3, 121)
    gxx, gyy = np.meshgrid(gx, gx)
    inside = lambda poly: Path(np.array(list(poly) + [poly[0]], float)).contains_points(np.c_[gxx.ravel(), gyy.ravel()]).reshape(gxx.shape).astype(float)      # noqa: E731
    modes = {}
    for k in (0, 1, 4):
        modes[f"a{k}"] = raster(xy1, v1, k) * inside(P.GWW_1)
        modes[f"b{k}"] = raster(xy2, v2, k) * inside(P.GWW_2)
    # sound: every drum with its lowest mode on the same note, each mode as loud as the last
    hz = 98.0
    amps = [1.0 / (1 + 0.25 * k) for k in range(count)]
    dec = [3.0 + 0.9 * k for k in range(count)]
    tone = lambda w: clip(P.modal(list(hz * np.sqrt(np.asarray(w) / w1[0])), amps, dec, 1.6)).at_level(LEVEL)      # noqa: E731
    seq = concat([tone(w1), tone(sq), tone(w2)], gap=0.5, names=["A", "B", "C"])
    lam = np.linspace(1.0, 320.0, 200)
    many = P.membrane_eigs(P.GWW_1, 70, 16)
    counts = [int(np.sum(many < x)) for x in lam]
    return {"drum1": [list(q) for q in P.GWW_1], "drum2": [list(q) for q in P.GWW_2], "area": P.polygon_area(P.GWW_1), "perimeter": P.polygon_perimeter(P.GWW_1),
            "eigs1": w1, "eigs2": w2, "largest_gap": float(np.abs(w1 - w2).max()), "driscoll": [2.53794, 3.65551, 5.17556], "ours": fine[:3] / 4.0,
            "ratios": np.sqrt(w1 / w1[0]), "square": sq, "square_ratios": list(np.sqrt(np.asarray(sq) / sq[0])), "side": side,
            **modes, "lam": lam, "counted": counts, "weyl": P.weyl(3.5, P.polygon_perimeter(P.GWW_1), lam), "quiz_answer": "B",
            "clips": {"three": save("shape.three", seq, level=None, detail="three drums of the same area, each sounding its twelve lowest modes")}}


def compute_tune() -> dict:
    beat = 0.55
    voices = {
        "marimba": lambda hz, dur, e: clip(P.marimba(hz, dur + 0.9)).at_level(LEVEL - 1),
        "bells": lambda hz, dur, e: clip(P.bell(hz * 2, dur + 1.6, slow=2.2), (0.001, 0.5)).at_level(LEVEL - 3),
        "steelpan": lambda hz, dur, e: clip(P.steelpan(hz, dur + 1.0)).at_level(LEVEL - 1),
    }
    plan = [("marimba",), ("bells",), ("steelpan",), ("marimba", "kettledrums"), ("bells", "steelpan"), ("marimba", "bells", "steelpan", "kettledrums")]
    parts = {name: play_tune(lambda hz, dur, e, v=v: v(hz, dur, e), phrases=None, tonic=C4, tail=1.5, beat=beat) for name, v in voices.items()}
    ref = parts["marimba"]
    # kettledrums: two of them, on the tonic and the dominant, on the first beat of each pair
    drums = []
    for k, nt in enumerate(ref.notes):
        if k % 2 == 0:
            low = C3 * (1.5 if nt["degree"] in (5, 2) else 1.0)
            drums.append((clip(P.drum(low, 1.3, tuned="timpani")).at_level(LEVEL - 2), nt["t"]))
    kd = mix(drums, duration=ref.duration)
    parts["kettledrums"] = Clip(kd.y, SR, ref.events, ref.notes)
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
        w = int(0.01 * SR)
        gate = np.convolve(gate, np.ones(w) / w, mode="same")
        yy = np.zeros(n_all)
        yy[: len(c.y)] = c.mono
        y += yy * gate
    notes = [{**n, "voices": list(plan[n["phrase"]])} for n in ref.notes]
    out = Clip(y, SR, ref.events, notes).at_level(LEVEL)
    b = load("bars")
    return {"clip": save("tune.variation9", out, level=None, detail="a marimba, bells, a steelpan and kettledrums: none of them a string or a pipe"),
            "notes": notes, "seconds": out.duration, "plan": [list(p) for p in plan], "order": ["marimba", "bells", "steelpan", "kettledrums"],
            "bar_ratios": list(b["marimba"]["ratios"][:3])}


def compute_variation() -> dict:
    t = load("tune")
    r = t["bar_ratios"]
    return {"part": 9, "title": r"for marimba, bells, steelpan and kettledrums: four instruments that had to be tuned against their nature", "seconds": t["seconds"],
            "measure": rf"its marimba's bars have overtones at {r[1]:.2f} and {r[2]:.1f} times their notes", "clip": "tune.variation9"}


ITEMS = {"hook": compute_hook, "skin": compute_skin, "timpani": compute_timpani, "tabla": compute_tabla, "bars": compute_bars, "bells": compute_bells,
         "plates": compute_plates, "gongs": compute_gongs, "pan": compute_pan, "shape": compute_shape, "tune": compute_tune, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
