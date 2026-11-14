"""Precompute everything numerical, and every sound, in Part 11 of *Music, Built* ("Rhythm and Meter").

    python -m videos.music.music11.compute              # everything missing (about a minute)
    python -m videos.music.music11.compute --force swing

Numbers are cached in ``.cache/music11/<name>.json`` (+ ``.npz``), sounds in ``.cache/music11/audio/``.  The rhythm
engine is Monochord's (``explainer/music/monochord/rhythm.py``), the kit is Part 9's struck things cut short
(``instruments/drumkit.py``); published findings are cited in the README.

Items:
    hook        sixteen identical clicks, measured
    tempo       clicks from one every two and a half seconds to fifty a second; two tempos five per cent apart
    meter       metres as nested groupings; the beat a pulse finder gives the Tune, and its taps
    accent      three ways to mark every third sound; loud-soft and long-short pairs with no beginning
    divide      a beat cut in one, two, three and four
    sync        four rhythms and their syncopation; two to compare
    hemiola     six eighths as two threes and as three twos; three against two, and four against three
    additive    seven as 2+2+3, 2+3+2 and 3+2+2; how many ways for each length
    swing       eighths at ratios of one, two and three to one; the ratio a short note of 100 ms gives at each tempo
    continuum   three against two, sped up until it is a perfect fifth
    frontier    the telephone game on rhythms, for two listeners with different expectations; one chain to hear
    tune        Variation 11: the Tune straight, as a waltz, in five, in seven, swung, and with hemiola
    variation   the Variations ledger, row 11
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import rhythm as R
from explainer.music.monochord import tune as TUNE
from explainer.music.monochord.instruments import drumkit as K
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.partkit import organ_tone, saver
from explainer.music.monochord.physics.string import String
from explainer.music.monochord.pitch import cents

CACHE = Cache("music11")
CLIPS = ClipStore("music11")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
C4 = 261.6255653005986
BOARD = STR.soundboard()
FOUR = (2, 2, 2, 2)
KIT = {"kick": K.kick(), "tom": K.tom(), "block": K.woodblock(), "clave": K.clave(), "rim": K.rim(), "hat": K.hat()}


def clip(y, fade=(0.0005, 0.02)) -> Clip:
    return Clip(np.asarray(y, dtype=np.float64)).fade(*fade)


def piano(hz: float, seconds: float) -> Clip:
    y = BOARD.play(STR.struck(String.tuned(hz, L=0.62 * (C4 / hz) ** 0.8, mu=6.34e-3, kappa=1.25, sigma0=0.6, sigma1=3.3e-4), velocity=1.6, seconds=seconds + 0.2))
    return clip(y, (0.001, 0.16)).at_level(LEVEL)


def hits(rows, duration: float | None = None, events=None) -> Clip:
    """``rows``: (sound name, time, gain dB).  A clip with the given events."""
    placed = [(clip(KIT[name]), float(t), float(g)) for name, t, g in rows]
    end = max(t + len(KIT[name]) / SR for name, t, _ in rows)
    c = mix(placed, duration=max(end, duration or 0.0))
    return Clip(c.y, SR, dict(events or {}), [])


def pattern_rows(name: str, pattern: str, pulse: float, gain: float = 0.0, t0: float = 0.0, repeat: int = 1, accents=None) -> list:
    """A pattern string on a grid of ``pulse`` seconds, as rows for :func:`hits`.  ``accents``: gains for positions."""
    p = pattern.replace(" ", "")
    rows = []
    for r in range(repeat):
        for i in R.onsets(p):
            rows.append((name, t0 + (r * len(p) + i) * pulse, gain + (accents or {}).get(i, 0.0)))
    return rows


# ---------------------------------------------------------------------------
def compute_hook() -> dict:
    n, gap = 16, 0.5
    c = hits([("block", k * gap, 0.0) for k in range(n)], duration=n * gap + 0.3, events={f"c{k}": k * gap for k in range(n)})
    y = c.mono
    levels = [10 * math.log10(float(np.mean(y[int(k * gap * SR): int((k * gap + 0.2) * SR)] ** 2))) for k in range(n)]
    return {"count": n, "gap": gap, "bpm": 60.0 / gap, "times": [k * gap for k in range(n)], "spread_db": max(levels) - min(levels),
            "clips": {"clicks": save("hook.clicks", c, detail="sixteen identical strokes on a wood block")}}


def compute_tempo() -> dict:
    rate0, rate1, seconds = 0.4, 50.0, 26.0
    t = R.accelerando(rate0, rate1, seconds)
    y = R.clicks(t, seconds + 0.3, width=0.0005)
    g = math.log(rate1 / rate0) / seconds
    when = lambda rate: math.log(rate / rate0) / g                    # noqa: E731
    ev = {"pulse": when(1 / 1.8), "fast": when(10.0), "tone": when(20.0), "end": seconds}
    sweep = Clip(Clip(y).fade(0.001, 0.05).y, SR, ev, [])
    grid = np.linspace(0, seconds, 200)
    a = hits([("block", k * 0.6, 0.0) for k in range(9)], duration=9 * 0.6)
    b = hits([("block", k * 0.6 / 1.05, 0.0) for k in range(9)], duration=9 * 0.6 / 1.05)
    pair = concat([a.at_level(LEVEL), b.at_level(LEVEL)], gap=1.0, names=["A", "B"])
    return {"rate0": rate0, "rate1": rate1, "seconds": seconds, "times": t, "grid": grid, "rate": rate0 * np.exp(g * grid), "zones": ev,
            "limits": {"slowest_s": 1.8, "fastest_s": 0.1, "tone_hz": 20.0, "preferred_s": 0.55},
            "bpm_a": 100.0, "bpm_b": 105.0, "quiz_answer": "B",
            "clips": {"sweep": save("tempo.sweep", sweep, kind="synthesized", detail="clicks that speed up from one every 2.5 seconds to fifty a second"),
                      "pair": save("tempo.pair", pair, level=None, detail="nine strokes, twice: two tempos five per cent apart")}}


def compute_meter() -> dict:
    ev = TUNE.events(0.55, phrases=[0, 1])
    times = [e["t"] for e in ev]
    r = R.pulse(times)
    taps = [r["phase"] + k * r["period"] for k in range(int((times[-1] + 1.1 - r["phase"]) / r["period"]) + 1)]
    placed = [(piano(C4 * float(e["ratio"]), e["dur"]), e["t"], 0.0) for e in ev] + [(clip(KIT["block"]).at_level(LEVEL), t, -7.0) for t in taps]
    c = mix(placed)
    events = {f"n{k}": t for k, t in enumerate(times)}
    events.update({f"tap{k}": t for k, t in enumerate(taps)})
    tap = Clip(c.y, SR, events, [])
    return {"four": R.meter_weights(FOUR), "three_four": R.meter_weights((3, 2)), "six_eight": R.meter_weights((2, 3)),
            "periods": r["periods"], "scores": r["scores"] / r["scores"].max(), "period": r["period"], "bpm": r["bpm"], "phase": r["phase"],
            "taps": taps, "notes": times, "true_beat": 0.55,
            "clips": {"tap": save("meter.tap", tap, detail="the Tune on Part 7's piano; a wood block on the beat that the pulse finder chose")}}


def tone(hz: float, seconds: float, db: float = 0.0) -> Clip:
    return clip(organ_tone(hz, seconds, partials=5), (0.008, 0.03)).at_level(LEVEL).gain(db)


def compute_accent() -> dict:
    step = 0.36
    loud = mix([(tone(392.0, 0.2, 0.0 if k % 3 == 0 else -9.0), k * step) for k in range(12)])
    long_ = mix([(tone(392.0, 0.32 if k % 3 == 0 else 0.12), k * step) for k in range(12)])
    high = mix([(tone(523.25 if k % 3 == 0 else 392.0, 0.2), k * step) for k in range(12)])
    three = concat([loud.at_level(LEVEL), long_.at_level(LEVEL), high.at_level(LEVEL)], gap=0.8, names=["loud", "long", "high"])

    def faded(c: Clip, seconds: float = 2.4) -> Clip:                 # no beginning and no end: the pairs have to be heard, not counted
        y = c.mono.copy()
        n = int(seconds * SR)
        ramp = np.linspace(0.0, 1.0, n) ** 2
        y[:n] *= ramp
        y[-n:] *= ramp[::-1]
        return Clip(y)

    a = mix([(tone(440.0, 0.2, 0.0 if k % 2 == 0 else -9.0), k * 0.3) for k in range(27)])
    rows, t = [], 0.0
    for k in range(27):
        d = 0.3 if k % 2 == 0 else 0.1
        rows.append((tone(440.0, d), t))
        t += d + 0.09
    b = mix(rows)
    law = concat([faded(a).at_level(LEVEL), faded(b).at_level(LEVEL)], gap=1.0, names=["A", "B"])
    return {"step": step, "answers": {"A": "the loud one begins a pair", "B": "the long one ends a pair"},
            "times": {nm: [three.events[nm] + k * step for k in range(12)] for nm in ("loud", "long", "high")},
            "clips": {"three": save("accent.three", three, kind="synthesized", level=None, detail="twelve tones, three times: every third is louder, then longer, then higher"),
                      "law": save("accent.law", law, kind="synthesized", level=None, detail="pairs that fade in: loud and soft, then long and short")}}


def compute_divide() -> dict:
    beat = 0.6
    rows, events = [], {}
    for j, parts in enumerate((1, 2, 3, 4)):
        t0 = j * 4 * beat
        events[f"d{parts}"] = t0
        for b in range(4):
            rows.append(("kick", t0 + b * beat, -2.0))
            for i in range(parts):
                rows.append(("block", t0 + b * beat + i * beat / parts, 0.0 if i == 0 else -4.0))
    c = hits(rows, duration=16 * beat + 0.3, events=events)
    bpm = 109.0
    q = 60.0 / bpm
    return {"beat": beat, "bpm": bpm, "ms": {"quarter": 1000 * q, "eighth": 500 * q, "triplet": 1000 * q / 3, "sixteenth": 250 * q},
            "pause": {"bpm": 120, "triplet_ms": 500.0 / 3},
            "clips": {"four": save("divide.four", c, detail="a beat cut in one, two, three and four: bass drum and wood block")}}


PATTERNS = [("every beat", "x...x...x...x..."), ("son clave", "x..x..x...x.x..."), ("bossa nova", "x..x..x...x..x.."), ("every off-beat", "..x...x...x...x.")]
QUIZ = {"A": "x...x.x...x.x...", "B": "x..x..x..x..x.x."}


def compute_sync() -> dict:
    pulse = 0.125
    beats = "x...x...x...x..."
    parts, names = [], []
    for k, (_, p) in enumerate(PATTERNS):
        rows = pattern_rows("kick", beats, pulse, -4.0, repeat=2) + pattern_rows("clave", p, pulse, 0.0, repeat=2)
        parts.append(hits(rows, duration=32 * pulse).at_level(LEVEL))
        names.append(f"s{k}")
    four = concat(parts, gap=0.6, names=names)
    quiz = concat([hits(pattern_rows("kick", beats, pulse, -4.0, repeat=2) + pattern_rows("clave", QUIZ[k], pulse, 0.0, repeat=2), duration=32 * pulse).at_level(LEVEL) for k in "AB"],
                  gap=0.9, names=["A", "B"])
    idx = {k: R.syncopation(p, FOUR) for k, p in QUIZ.items()}
    offs = "..x...x...x...x."
    rows = pattern_rows("clave", offs, pulse, 0.0, repeat=4) + pattern_rows("kick", beats, pulse, -3.0, t0=32 * pulse, repeat=2)
    flip = hits(rows, duration=64 * pulse + 0.3, events={"alone": 0.0, "drum": 32 * pulse})
    return {"weights": R.meter_weights(FOUR), "pulse": pulse, "flip_times": [(r * 16 + i) * pulse for r in range(4) for i in R.onsets(offs)], "flip_beats": [32 * pulse + k * 4 * pulse for k in range(8)], "patterns": [{"name": n, "pattern": p, "index": R.syncopation(p, FOUR)} for n, p in PATTERNS],
            "quiz": QUIZ, "quiz_index": idx, "quiz_answer": max(idx, key=idx.get), "starts": [four.events[n] for n in names],
            "clips": {"four": save("sync.four", four, level=None, detail="four rhythms on a clave over a steady bass drum"),
                      "quiz": save("sync.quiz", quiz, level=None, detail="two rhythms over the same bass drum"),
                      "flip": save("sync.flip", flip, detail="strokes half a second apart; then a bass drum between them")}}


def compute_hemiola() -> dict:
    pulse = 0.2
    rows, events = [], {}
    for bar in range(8):
        t0 = bar * 6 * pulse
        events[f"bar{bar}"] = t0
        starts = (0, 3) if bar % 2 == 0 else (0, 2, 4)
        for i in range(6):
            rows.append(("block", t0 + i * pulse, -6.0))
        for i in starts:
            rows.append(("kick", t0 + i * pulse, 0.0))
    bars = hits(rows, duration=48 * pulse + 0.3, events=events)
    # three against two, then four against three
    cyc = 1.2
    rows, events, t = [], {}, 0.0
    for name, n_cyc, low, high in (("two", 2, True, False), ("three", 2, False, True), ("both", 4, True, True)):
        events[name] = t
        for c in range(n_cyc):
            if low:
                rows += [("tom", t + c * cyc + k * cyc / 2, 0.0) for k in range(2)]
            if high:
                rows += [("clave", t + c * cyc + k * cyc / 3, -2.0) for k in range(3)]
        t += n_cyc * cyc
    t += 0.6
    events["four_three"] = t
    cyc2 = 1.6
    for c in range(4):
        rows += [("tom", t + c * cyc2 + k * cyc2 / 3, 0.0) for k in range(3)]
        rows += [("clave", t + c * cyc2 + k * cyc2 / 4, -2.0) for k in range(4)]
    events["end"] = t + 4 * cyc2
    poly = hits(rows, duration=t + 4 * cyc2 + 0.3, events=events)
    p32, p43 = R.polyrhythm(3, 2), R.polyrhythm(4, 3)
    base = "x..x..x...x.x..."
    on = set(R.onsets(base))
    meets = [len(on & {(i + k) % 16 for i in on}) for k in range(16)]                 # strokes that coincide when the copy starts k pulses late
    sp, shifts = 0.125, [0, 2, 8]
    parts = []
    for k in shifts:
        rws = pattern_rows("clave", base, sp, 0.0, repeat=2) + pattern_rows("rim", R.rotate(base, -k), sp, -2.0, repeat=2) + pattern_rows("kick", "x.......x.......", sp, -6.0, repeat=2)
        parts.append(hits(rws, duration=32 * sp).at_level(LEVEL))
    canon = concat(parts, gap=0.6, names=[f"k{k}" for k in shifts])
    return {"canon_base": base, "canon_meets": meets, "canon_shifts": shifts, "canon_starts": [canon.events[f"k{k}"] for k in shifts], "canon_pulse": sp,
            "canon_copies": [R.rotate(base, -k) for k in shifts], "pulse": pulse, "six_eight": R.meter_weights((2, 3)), "three_four": R.meter_weights((3, 2)), "cycle": cyc, "cycle2": cyc2,
            "p32": p32, "p43": p43, "hemiola_index": R.syncopation("x.x.x.", (2, 3)),
            "clips": {"bars": save("hemiola.bars", bars, detail="six pulses to the bar, grouped 3 + 3 and 2 + 2 + 2 in turn"),
                      "poly": save("hemiola.poly", poly, detail="two in a cycle, three in a cycle, both; then four against three"),
                      "canon": save("hemiola.canon", canon, level=None, detail="one rhythm against a copy of itself that starts 0, 2 and 8 pulses late")}}


def compute_additive() -> dict:
    pulse = 0.19
    comps = R.compositions(7)
    parts, names = [], []
    for k, comp in enumerate(comps):
        starts = np.concatenate([[0], np.cumsum(comp)[:-1]])
        rows = []
        for bar in range(4):
            t0 = bar * 7 * pulse
            rows += [("block", t0 + i * pulse, -7.0) for i in range(7)]
            rows += [("kick" if j == 0 else "tom", t0 + s * pulse, 0.0 if j == 0 else -2.0) for j, s in enumerate(starts)]
        parts.append(hits(rows, duration=28 * pulse).at_level(LEVEL))
        names.append(f"c{k}")
    seq = concat(parts, gap=0.6, names=names)
    return {"pulse": pulse, "sevens": [list(c) for c in comps], "counts": {str(n): len(R.compositions(n)) for n in range(4, 13)},
            "nines": [list(c) for c in R.compositions(9)], "starts": [seq.events[n] for n in names],
            "clips": {"seven": save("additive.seven", seq, level=None, detail="seven pulses to the bar, three ways")}}


def compute_swing() -> dict:
    beat = 0.5
    ratios = [1.0, 2.0, 3.0]
    parts, names, times = [], [], []
    for k, r in enumerate(ratios):
        sw = R.swing(8, beat, r)
        rows = [("hat", t, 0.0 if j % 2 == 0 else -3.0) for j, t in enumerate(sw)]
        rows += [("kick", b * beat, -1.0) for b in (0, 2, 4, 6)] + [("rim", b * beat, -4.0) for b in (1, 3, 5, 7)]
        parts.append(hits(rows, duration=8 * beat).at_level(LEVEL))
        names.append(f"r{k}")
        times.append(sw)
    seq = concat(parts, gap=0.7, names=names)
    bpm = np.linspace(100, 330, 47)
    b = 60.0 / bpm
    short = 0.1
    ratio = np.clip((b - short) / short, 1.0, 3.5)
    return {"beat": beat, "ratios": ratios, "starts": [seq.events[n] for n in names], "times": times,
            "long_ms": [1000 * beat * r / (1 + r) for r in ratios], "short_ms": [1000 * beat / (1 + r) for r in ratios],
            "bpm": bpm, "ratio": ratio, "short": short, "triplet_bpm": 60.0 / (3 * short), "straight_bpm": 60.0 / (2 * short), "slow_ratio": 3.5,
            "clips": {"three": save("swing.three", seq, level=None, kind="synthesized", detail="eighth notes on a hi-hat: even, two to one, three to one")}}


def compute_continuum() -> dict:
    rate0, rate1, ramp, hold = 0.75, 100.0, 24.0, 2.6
    g = math.log(rate1 / rate0) / ramp
    total_cycles = rate0 * (math.exp(g * ramp) - 1.0) / g + rate1 * hold

    def when(cycles):                                                # the time at which so many cycles have gone by
        c = np.asarray(cycles, dtype=float)
        knee = rate0 * (math.exp(g * ramp) - 1.0) / g
        return np.where(c <= knee, np.log(1.0 + np.minimum(c, knee) * g / rate0) / g, ramp + (c - knee) / rate1)

    two = when(np.arange(0, int(total_cycles * 2)) / 2.0)
    three = when(np.arange(0, int(total_cycles * 3)) / 3.0)
    seconds = ramp + hold
    y = R.clicks(two, seconds, 1.0, width=0.0006) + R.clicks(three, seconds, 0.8, width=0.0003)
    tail = y[int((ramp + 0.3) * SR): int((seconds - 0.1) * SR)]
    spec = np.abs(np.fft.rfft(tail * np.hanning(len(tail))))
    freqs = np.fft.rfftfreq(len(tail), 1 / SR)
    f2 = float(freqs[int(np.argmax(spec * (np.abs(freqs - 200.0) < 20)))])
    f3 = float(freqs[int(np.argmax(spec * (np.abs(freqs - 300.0) < 20)))])
    rate_at = lambda t: rate0 * math.exp(g * min(t, ramp))            # noqa: E731
    t20 = math.log((20.0 / 3.0) / rate0) / g
    ev = {"t20": t20, "hold": ramp, "end": seconds}
    c = Clip(Clip(y).fade(0.001, 0.08).y, SR, ev, [])
    grid = np.linspace(0, seconds, 240)
    pats = {"A": "x.......", "B": "x..x..x."}
    harm, pieces, names = {}, [], []
    for speed, cyc, reps in (("slow", 1.0, 2), ("fast", 1.0 / 110.0, 132)):
        for nm, pt in pats.items():
            ts = [(r + i / 8.0) * cyc for r in range(reps) for i in R.onsets(pt)]
            yy = R.clicks(ts, reps * cyc + 0.05, width=0.0004)
            piece = Clip(yy).fade(0.002, 0.03)
            pieces.append(piece.at_peak(-9.0) if speed == "slow" else piece.at_level(LEVEL))        # a lone click has a peak, not a loudness
            names.append(f"{speed}{nm}")
    for nm, pt in pats.items():                                      # the strength of each harmonic of the cycle: the pattern's Fourier series
        on8 = np.array(R.onsets(pt))
        harm[nm] = [float(abs(np.exp(-2j * np.pi * h * on8 / 8.0).sum()) / len(on8)) for h in range(1, 13)]
    timbre = concat(pieces, gap=0.5, names=names)
    return {"timbre_patterns": pats, "timbre_harmonics": harm, "timbre_hz": 110.0, "timbre_events": {n: timbre.events[n] for n in names},
            "rate0": rate0, "rate1": rate1, "ramp": ramp, "hold": hold, "two": two[two < seconds], "three": three[three < seconds], "grid": grid,
            "rate": np.array([rate_at(t) for t in grid]), "f2": f2, "f3": f3, "cents": cents(f3 / f2), "t20": t20, "events": ev,
            "clips": {"fifth": save("continuum.fifth", c, kind="synthesized", detail="three clicks against two, from a slow rhythm to a hundred cycles a second"),
                      "timbre": save("continuum.timbre", timbre, kind="synthesized", level=None, detail="two patterns of clicks, once a second and then 110 times a second")}}


def compute_frontier() -> dict:
    pk = np.array([R.simplex_point(r) for r in R.INTEGER_RHYTHMS])
    rng = np.random.default_rng(3)
    seeds = rng.dirichlet([1, 1, 1], 420)
    seeds = seeds[seeds.min(axis=1) > 0.12][:240]
    w_a = np.array([1.0 if set(r) <= {1, 2} else 0.02 for r in R.INTEGER_RHYTHMS])
    w_b = np.array([1.0 if (3 in r or r == (1, 1, 1)) else 0.02 for r in R.INTEGER_RHYTHMS])
    a, b = R.iterate(seeds, pk, w_a, 5, seed=1), R.iterate(seeds, pk, w_b, 5, seed=1)
    near = lambda pts: float(R.nearest_ratio(pts, pk)[:, 1].mean())                                   # noqa: E731
    share = lambda pts, w: float(np.mean(w[R.nearest_ratio(pts, pk)[:, 0].astype(int)] > 0.5))       # noqa: E731
    # one chain to hear: a seed far from every whole-number rhythm
    far = int(np.argmax(R.nearest_ratio(a[0], pk)[:, 1] * (R.nearest_ratio(a[5], pk)[:, 1] < 0.03)))
    chain = a[:, far, :]
    cycle = 1.8
    parts, names = [], []
    for k in (0, 1, 2, 5):
        t, rows = 0.0, []
        for rep in range(2):
            for frac in chain[k]:
                rows.append(("clave", t, 0.0))
                t += frac * cycle
        rows.append(("clave", t, 0.0))
        parts.append(hits(rows, duration=t + 0.5).at_level(LEVEL))
        names.append(f"round{k}")
    seq = concat(parts, gap=0.5, names=names)
    end = R.INTEGER_RHYTHMS[int(R.nearest_ratio(chain[5:6], pk)[0, 0])]
    return {"peaks": pk, "ratios": [list(r) for r in R.INTEGER_RHYTHMS], "weights_a": w_a, "weights_b": w_b, "a": a, "b5": b[5], "seeds": len(seeds),
            "near": [near(a[k]) for k in range(6)], "share_a": share(a[5], w_a), "share_b": share(b[5], w_b), "cross": share(a[5], w_b),
            "chain": chain, "chain_end": list(end), "chain_start_ms": [float(1000 * cycle * f) for f in chain[0]], "chain_end_ms": [float(1000 * cycle * f) for f in chain[5]],
            "rounds_heard": [0, 1, 2, 5], "starts": [seq.events[n] for n in names], "cycle": cycle,
            "clips": {"chain": save("frontier.chain", seq, level=None, detail="one rhythm, tapped back and played again: rounds 0, 1, 2 and 5 of a simulated chain")}}


# the Tune's six phrases, each in its own metre: (name, seconds per pulse, pulses in a bar, groups, bars, [(start pulse, length)])
PLANS = [
    ("four", "4/4", 0.55, 4, (1, 1, 1, 1), 2, [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 2)]),
    ("waltz", "3/4", 0.40, 3, (1, 1, 1), 4, [(0, 2), (2, 1), (3, 2), (5, 1), (6, 2), (8, 1), (9, 3)]),
    ("five", "5/4", 0.30, 5, (3, 2), 4, [(0, 3), (3, 2), (5, 3), (8, 2), (10, 3), (13, 2), (15, 5)]),
    ("seven", "7/8", 0.21, 7, (2, 2, 3), 3, [(0, 2), (2, 2), (4, 3), (7, 2), (9, 2), (11, 3), (14, 7)]),
    ("swung", "4/4, swung", 0.40, 8, (2, 2, 2, 2), 2, [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 2)]),
    ("hemiola", "6/8 and 3/4", 0.20, 6, None, 4, [(0, 3), (3, 3), (6, 2), (8, 2), (10, 2), (12, 3), (15, 9)]),
]


def compute_tune() -> dict:
    placed, events, phrases, notes_out = [], {}, [], []
    t0, i = 0.0, 0
    for k, (name, sig, pulse, per_bar, groups, bars, notes) in enumerate(PLANS):
        degs = TUNE.PHRASES[k]
        n_pulses = per_bar * bars

        def at(p):                                                   # the time of pulse p of this phrase (swung: every second eighth is late)
            if name == "swung":
                return t0 + (p // 2) * 2 * pulse + (2 * pulse * 2.0 / 3.0 if p % 2 else 0.0)
            return t0 + p * pulse

        events[f"phrase{k}"] = t0
        for (deg, _), (start, length) in zip(degs, notes):
            hz = C4 * float(TUNE.DEGREE_RATIO[deg])
            dur = at(start + length) - at(start) if start + length <= n_pulses else t0 + n_pulses * pulse - at(start)
            placed.append((piano(hz, dur), at(start), 0.0))
            events[f"n{i}"] = at(start)
            notes_out.append({"t": at(start), "dur": dur, "hz": hz, "phrase": k})
            i += 1
        accents = []
        for bar in range(bars):
            g = groups if groups is not None else ((3, 3) if bar % 2 == 0 else (2, 2, 2))
            starts = np.concatenate([[0], np.cumsum(g)[:-1]]) if name != "swung" else np.array([0, 2, 4, 6])
            for j, s in enumerate(starts):
                p = bar * per_bar + int(s)
                which = "kick" if j == 0 else ("rim" if name == "swung" and j % 2 else "tom" if name in ("five", "seven", "hemiola") else "block")
                placed.append((clip(KIT[which]).at_level(LEVEL), at(p), -6.0 if which != "kick" else -4.0))
                accents.append(at(p) - t0)
            if name in ("swung", "seven", "five", "hemiola"):
                for p in range(per_bar):
                    placed.append((clip(KIT["hat"]).at_level(LEVEL), at(bar * per_bar + p), -13.0))
        phrases.append({"name": name, "signature": sig, "pulse": pulse, "per_bar": per_bar, "bars": bars, "groups": list(groups) if groups else [[3, 3], [2, 2, 2]],
                        "t0": t0, "seconds": n_pulses * pulse, "accents": accents, "pulses": [at(p) - t0 for p in range(n_pulses)]})
        t0 += n_pulses * pulse
    events["end"] = t0
    c = mix(placed, duration=t0 + 1.2)
    out = Clip(c.y, SR, events, notes_out).at_level(LEVEL)
    return {"clip": save("tune.variation11", out, level=None, detail="six phrases, six ways of counting: Part 7's piano and this part's kit"),
            "seconds": out.duration, "phrases": phrases, "signatures": [p["signature"] for p in phrases], "bar_pulses": [p["per_bar"] for p in phrases]}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 11, "title": r"straight, as a waltz, in five, in seven, swung, and with a hemiola", "seconds": t["seconds"],
            "measure": r"its bars are counted in 4, 3, 5 and 7, and in six two ways", "clip": "tune.variation11"}


ITEMS = {"hook": compute_hook, "tempo": compute_tempo, "meter": compute_meter, "accent": compute_accent, "divide": compute_divide, "sync": compute_sync,
         "hemiola": compute_hemiola, "additive": compute_additive, "swing": compute_swing, "continuum": compute_continuum, "frontier": compute_frontier,
         "tune": compute_tune, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
