"""Precompute everything numerical, and every sound, in Part 37 of *Music, Built* ("Timelines").

    python -m videos.music.music37.compute              # everything missing (under a minute)
    python -m videos.music.music37.compute --force ewe

Numbers are cached in ``.cache/music37/<name>.json``, sounds in ``.cache/music37/audio/``.  The models are Monochord's
(``explainer/music/monochord/timelines.py``): an iron bell by modal synthesis, Part 9's membranes for the drums, Part 9's
bar for claves and the mbira's tines, Part 8's flute for pipes, Part 35's retuned plucked string for guitar and bass,
and Part 17's model choir.  Every part, pattern and melody played is ours; the timelines are the well-known ones, as
they are commonly transcribed.

Items:
    hook        the standard pattern alone; with a beat in four; with a beat in six (an ear question: where is the beat?)
    scale       the standard pattern as rhythm, and the major scale with the same steps; two rotations as modes
    metrics     evenness, oddity, off-beatness and centrality for a table of timelines; four claves, heard
    ewe         an ensemble of ours in the manner of the Ewe: bell, rattle, three drums and a lead drum, entering in turn
    threetwo    four beats against six in twelve pulses: each alone, together, then with the bell
    hocket      a melody split between two panpipe players by pitch (in the manner of the siku); five pipes of one pitch each
    mbira       one tine without and with its buzz; two interlocking parts, each alone, then together
    inherent    two parts at speed (an ear question: what melody do the high notes make?), slowly, and the melody itself
    clave       tresillo, cinquillo and the habanera; son clave three-two and two-three
    son         a son texture of ours over the clave, layer by layer
    samba       a batucada of ours: surdos, caixa, shaker, tamborim and agogo, entering in turn
    callresp    call and response over the bell: a leader and a chorus (model voices)
    uneven      a beat divided in three: equal, then unequal (illustrative proportions)
    tune        Variation 37: the Tune as an inherent pattern of two mbira parts; then over the standard pattern on claves
    variation   the Variations ledger, row 37
"""

from __future__ import annotations

import numpy as np
from scipy.signal import butter, sosfilt

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import maqam as Q
from explainer.music.monochord import melody as M
from explainer.music.monochord import timelines as T
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.instruments import drumkit as DK
from explainer.music.monochord.instruments import percussion as PC
from explainer.music.monochord.instruments import winds as W
from explainer.music.monochord.partkit import saver

CACHE = Cache("music37")
CLIPS = ClipStore("music37")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
save_synth = saver(CLIPS, LEVEL, kind="synthesized")
P12 = 0.2                                        # a pulse of the twelve-pulse cycle (the cycle is 2.4 s)
P16 = 0.15                                       # a pulse of the sixteen-pulse cycle (also 2.4 s)
STANDARD = T.TIMELINES["standard pattern (12)"]
_C: dict = {}


def arr(y):
    return Clip(np.asarray(y, float), SR)


def cached(key, fn):
    if key not in _C:
        _C[key] = fn()
    return _C[key]


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


# ---------------------------------------------------------------------------------------------------- instruments
BELL_RATIOS = [1.0, 2.18, 3.41, 4.93]


def bell(low=False):
    """An iron bell (the gankogui's two bells, or the agogo's): a modal model with designed ratios."""
    f = 560.0 if low else 840.0
    return cached(("bell", low), lambda: PC.modal([f * r for r in BELL_RATIOS], [1.0, 0.55, 0.3, 0.15], [6.0, 9.0, 14.0, 20.0], 0.7, SR))


def noise_burst(lo, hi, seconds, decay, seed):
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    y = sosfilt(butter(2, [lo, hi], btype="band", fs=SR, output="sos"), rng.standard_normal(n))
    y = y * np.exp(-decay * t) * np.clip(t / 0.002, 0, 1)
    return y / np.abs(y).max()


def rattle(down=False, seed=0):
    """A gourd rattle with a net of beads: struck on the thigh (down, duller) or thrown up against the hand (up)."""
    return cached(("rattle", down, seed % 4), lambda: noise_burst(1500, 5000, 0.12, 35.0, 11 + seed % 4) if down
                  else noise_burst(3500, 9000, 0.08, 55.0, 21 + seed % 4))


def shaker(seed=0):
    return cached(("shaker", seed % 4), lambda: noise_burst(5000, 11000, 0.07, 70.0, 31 + seed % 4))


def clap(seed=0):
    def make():
        y = np.zeros(int(0.15 * SR))
        for k, dt in enumerate((0.0, 0.009, 0.017)):
            b = noise_burst(900, 3200, 0.13, 40.0, 41 + seed % 3 + 5 * k)
            i = int(dt * SR)
            m = min(len(b), len(y) - i)
            y[i:i + m] += (0.7 if k < 2 else 1.0) * b[:m]
        return y / np.abs(y).max()
    return cached(("clap", seed % 3), make)


def drum(f, stroke="open", seconds=0.6):
    """Part 9's membrane: an open tone, a muted 'press' stroke, or a slap struck near the rim."""
    if stroke == "open":
        fn = lambda: PC.drum(f, seconds, at=0.55, damping=6.0)                       # noqa: E731
    elif stroke == "press":
        fn = lambda: PC.drum(f * 1.06, 0.25, at=0.5, damping=45.0)                    # noqa: E731
    else:
        fn = lambda: PC.drum(f * 1.5, 0.3, at=0.92, damping=22.0)                     # noqa: E731
    return cached(("drum", round(f, 2), stroke, seconds), fn)


def pipe(m, seconds=0.32):
    def make():
        y = W.jet_tone(hz(m), seconds + 0.12, attack=0.02, seed=int(m))
        y = y / np.abs(y).max()
        n = len(y)
        env = np.ones(n)
        r = int(0.06 * SR)
        env[-r:] = np.linspace(1, 0, r)
        return y * env
    return cached(("pipe", m, seconds), make)


def tine(m, buzz=0.15, seconds=1.4):
    return cached(("tine", m, buzz, seconds), lambda: T.mbira(hz(m), seconds, buzz))


def pluck(m, seconds=0.8):
    return cached(("pluck", m, seconds), lambda: Q.oud(hz(m), seconds))


def place(parts, sound, times, gain=0.0):
    for t in times:
        parts.append((arr(sound), t, gain))


def cycle_times(onsets_, cycles, pulse, n, start=0.0):
    return [start + c * n * pulse + o * pulse for c in range(cycles) for o in onsets_]


def bounce(parts, end):
    return Clip(mix(parts, duration=end).y, SR).at_level(LEVEL)


# ---------------------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    on = T.onsets(STANDARD)
    cyc = 4
    out = {}
    for name, beats, snd, g in (("bell", [], None, 0.0), ("four", [0, 3, 6, 9], "drum", -3.0), ("six", [0, 2, 4, 6, 8, 10], "clap", -8.0)):
        parts = []
        place(parts, bell(), cycle_times(on, cyc, P12, 12), -4.0)
        if snd == "drum":
            place(parts, drum(95.0), cycle_times(beats, cyc, P12, 12), g)
        elif snd == "clap":
            for i, t in enumerate(cycle_times(beats, cyc, P12, 12)):
                parts.append((arr(clap(i)), t, g))
        c = bounce(parts, cyc * 12 * P12 + 0.8)
        detail = {"bell": "the standard pattern on an iron bell, four cycles",
                  "four": "the standard pattern with a drum on four beats a cycle",
                  "six": "the standard pattern with a clap on six beats a cycle"}[name]
        out[name] = save(f"hook.{name}", c, detail=detail + "; modal and membrane models")
    return {"pattern": STANDARD, "onsets": on, "pulse": P12, "cycles": cyc, "four": [0, 3, 6, 9], "six": [0, 2, 4, 6, 8, 10],
            "steps": T.steps(STANDARD), "clips": out}


def compute_scale() -> dict:
    on = T.onsets(STANDARD)
    major = [60, 62, 64, 65, 67, 69, 71]
    # 1. the bell, two cycles; 2. the scale up, one note on each stroke, twice; 3. both together, twice
    parts, t0 = [], 0.0
    place(parts, bell(), cycle_times(on, 2, P12, 12, t0), -4.0)
    t1 = t0 + 2 * 12 * P12 + 0.6
    for c in range(2):
        for k, o in enumerate(on):
            parts.append((arr(cached(("marimba", major[k]), lambda m=major[k]: PC.marimba(hz(m), 1.0))), t1 + (c * 12 + o) * P12, 0.0))
        if c == 1:
            parts.append((arr(cached(("marimba", 72), lambda: PC.marimba(hz(72), 1.0))), t1 + (c * 12 + 12) * P12, 0.0))
    t2 = t1 + 2 * 12 * P12 + 1.0
    for c in range(2):
        for k, o in enumerate(on):
            parts.append((arr(cached(("marimba", major[k]), lambda m=major[k]: PC.marimba(hz(m), 1.0))), t2 + (c * 12 + o) * P12, 0.0))
    place(parts, bell(), cycle_times(on, 2, P12, 12, t2), -6.0)
    end = t2 + 2 * 12 * P12 + 1.2
    s_ = bounce(parts, end)
    s_.events = {"bell": t0, "scale": t1, "both": t2}
    rots = T.rotations(STANDARD)
    # two rotations as modes: Dorian (start on the second stroke) and Aeolian (the sixth), each as rhythm and scale
    clips2, starts2 = [], {}
    tt = 0.0
    parts = []
    for k, root in ((1, 62), (5, 69)):
        r = rots[k]
        o2 = T.onsets(r["pattern"])
        pcs = [root]
        for st in r["steps"][:-1]:
            pcs.append(pcs[-1] + st)
        starts2[T.MODES[k]] = tt
        for c in range(2):
            for j, o in enumerate(o2):
                m = pcs[j]
                parts.append((arr(cached(("marimba", m), lambda m=m: PC.marimba(hz(m), 1.0))), tt + (c * 12 + o) * P12, 0.0))
        place(parts, bell(), cycle_times(o2, 2, P12, 12, tt), -6.0)
        tt += 2 * 12 * P12 + 1.4
    m_ = bounce(parts, tt)
    m_.events = starts2
    return {"steps": T.steps(STANDARD), "major_steps": [2, 2, 1, 2, 2, 2, 1], "rotations": rots, "modes": T.MODES,
            "intervals": T.interval_content(STANDARD), "euclid": T.metrics(STANDARD)["euclidean"],
            "starts": {"bell": t0, "scale": t1, "both": t2}, "mode_starts": starts2, "pulse": P12, "onsets": on,
            "clips": {"three": save("scale.three", s_, detail="the standard pattern on a bell; the major scale played one note on each of its strokes; both together; modal models"),
                      "modes": save("scale.modes", m_, detail="two rotations of the standard pattern, each with its mode (Dorian on D, Aeolian on A) played on its strokes")}}


def compute_metrics() -> dict:
    rows = []
    for name, p in T.TIMELINES.items():
        m = T.metrics(p)
        rows.append({"name": name, "pattern": p, "n": m["n"], "k": m["k"], "uneven": round(m["evenness"], 3),
                     "euclidean": bool(m["euclidean"]), "oddity": m["oddity"], "offbeat": m["offbeat"]})
    cent = T.centrality()
    parts, t, starts = [], 0.0, {}
    for name in ("son clave (16)", "rumba clave (16)", "bossa nova (16)", "gahu (16)"):
        starts[name] = t
        place(parts, cached(("clave",), lambda: DK.clave()), cycle_times(T.onsets(T.TIMELINES[name]), 2, P16, 16, t), -2.0)
        place(parts, drum(80.0, "press"), cycle_times([0, 4, 8, 12], 2, P16, 16, t), -14.0)
        t += 2 * 16 * P16 + 0.9
    c = bounce(parts, t)
    return {"rows": rows, "centrality": cent, "most_central": min(cent, key=cent.get), "starts": starts, "pulse": P16,
            "offbeat16": T.offbeat_positions(16), "offbeat12": T.offbeat_positions(12),
            "clips": {"claves": save("metrics.claves", c, detail="son clave, rumba clave, bossa nova and gahu, two cycles each, on claves with a soft beat; bar and membrane models")}}


EWE = {   # parts of our own in the manner of an Ewe dance-drumming ensemble, twelve pulses a cycle
    "bell": {"open": T.onsets(STANDARD)},
    "rattle": {"down": [0, 3, 6, 9], "up": [2, 4, 5, 7, 11]},
    "kagan": {"press": [1, 2, 4, 5, 7, 8, 10, 11]},
    "kidi": {"open": [2, 3, 8, 9], "press": [5, 11]},
    "sogo": {"open": [4, 10], "press": [0, 6], "slap": [5]},
}
LEAD = [   # four cycles of a lead-drum phrase of ours: (pulse, stroke)
    [(0, "open"), (2, "open"), (4, "open"), (6, "slap"), (7, "slap")],
    [(0, "open"), (3, "open"), (6, "open"), (9, "open"), (10, "slap"), (11, "slap")],
    [(1, "slap"), (2, "slap"), (4, "open"), (5, "open"), (7, "slap"), (8, "slap"), (10, "open")],
    [(0, "open"), (2, "open"), (3, "slap"), (6, "open"), (8, "open"), (9, "slap"), (11, "slap")],
]
DRUM_F = {"kagan": 330.0, "kidi": 220.0, "sogo": 165.0, "lead": 118.0}


def ewe_layer(parts, name, t0, cycles, gain=0.0):
    pat = EWE[name]
    if name == "bell":
        place(parts, bell(), cycle_times(pat["open"], cycles, P12, 12, t0), -6.0 + gain)
        place(parts, bell(True), cycle_times([0], cycles, P12, 12, t0), -12.0 + gain)
    elif name == "rattle":
        for i, t in enumerate(cycle_times(pat["down"], cycles, P12, 12, t0)):
            parts.append((arr(rattle(True, i)), t, -10.0 + gain))
        for i, t in enumerate(cycle_times(pat["up"], cycles, P12, 12, t0)):
            parts.append((arr(rattle(False, i)), t, -13.0 + gain))
    else:
        for stroke, ons in pat.items():
            place(parts, drum(DRUM_F[name], stroke), cycle_times(ons, cycles, P12, 12, t0), {"kagan": -9.0, "kidi": -6.0, "sogo": -5.0}[name] + gain)


def lead_layer(parts, t0, cycles, gain=0.0):
    for c in range(cycles):
        for o, stroke in LEAD[c % 4]:
            parts.append((arr(drum(DRUM_F["lead"], stroke, 0.8)), t0 + (c * 12 + o) * P12, -2.0 + gain))


def compute_ewe() -> dict:
    order = [("bell", 2), ("rattle", 1), ("kagan", 1), ("kidi", 2), ("sogo", 2), ("lead", 4)]
    total = sum(c for _, c in order)
    parts, entries, t = [], {}, 0.0
    for name, c in order:
        entries[name] = t
        t += c * 12 * P12
    for name, _ in order:
        cycles_left = int(round((t - entries[name]) / (12 * P12)))
        if name == "lead":
            lead_layer(parts, entries[name], cycles_left)
        else:
            ewe_layer(parts, name, entries[name], cycles_left)
    c = bounce(parts, t + 1.0)
    return {"parts": EWE, "lead": LEAD, "entries": entries, "order": [n for n, _ in order], "cycles": total, "pulse": P12,
            "clips": {"layers": save("ewe.layers", c, detail="an ensemble of ours in the manner of Ewe dance drumming: iron bell, gourd rattle, three drums and a lead drum, entering in turn; modal, noise and membrane models")}}


def compute_threetwo() -> dict:
    four, six = [0, 3, 6, 9], [0, 2, 4, 6, 8, 10]
    parts, starts, t = [], {}, 0.0
    for name, a, b, withbell in (("four", True, False, False), ("six", False, True, False), ("both", True, True, False), ("bell", True, True, True)):
        starts[name] = t
        if a:
            place(parts, drum(90.0), cycle_times(four, 2, P12, 12, t), -2.0)
        if b:
            place(parts, drum(260.0, "slap"), cycle_times(six, 2, P12, 12, t), -9.0)
        if withbell:
            place(parts, bell(), cycle_times(T.onsets(STANDARD), 2, P12, 12, t), -7.0)
        t += 2 * 12 * P12 + 0.8
    c = bounce(parts, t)
    on = T.onsets(STANDARD)
    return {"four": four, "six": six, "starts": starts, "pulse": P12, "on_four": [o for o in on if o in four],
            "on_six": [o for o in on if o in six], "on_three": [o for o in on if o in (0, 4, 8)],
            "clips": {"cross": save("threetwo.cross", c, detail="four beats a cycle on a low drum, six on a high one, both together, then with the bell; membrane and modal models")}}


SIKU_IRA = {72, 76, 79, 83}            # C E G B: one row of the panpipe
SIKU_ARKA = {74, 77, 81, 84}           # D F A c: the other


def tune_line(n=14, base=72):
    t = M.corpus([M.THE_TUNE])[0]
    out, a = [], 0.0
    for p, d in list(zip(t.pitches, t.beats))[:n]:
        out.append((base + p, a, float(d)))
        a += d
    return out


def compute_hocket() -> dict:
    mel = tune_line(14)
    beat = 0.42
    ira, arka = T.hocket([p for p, _, _ in mel], [SIKU_IRA, SIKU_ARKA])
    clips = {}
    starts, t, parts = {}, 0.0, []
    for name, which in (("ira", (ira,)), ("arka", (arka,)), ("both", (ira, arka))):
        starts[name] = t
        for part in which:
            for (p, a, d), x in zip(mel, part):
                if x is not None:
                    parts.append((arr(pipe(x, d * beat * 0.92)), t + a * beat, 0.0))
        t += (mel[-1][1] + mel[-1][2]) * beat + 1.0
    c = bounce(parts, t)
    clips["siku"] = save("hocket.siku", c, detail="the Tune's first two phrases split between two panpipe players by pitch, each alone, then together; Part 8's flute model")
    # five pipes, one pitch each, twelve pulses a cycle (ours)
    pipes = {81: [0, 6], 79: [2, 7], 76: [3, 9], 74: [4, 10], 72: [5, 11]}
    order = [81, 79, 76, 74, 72]
    parts, entries, tt = [], {}, 0.0
    for k, m in enumerate(order):
        entries[m] = tt
        tt += (2 if k == 0 else 1) * 12 * P12
    tt += 3 * 12 * P12
    for m in order:
        cyc = int(round((tt - entries[m]) / (12 * P12)))
        place(parts, pipe(m, 0.2), cycle_times(pipes[m], cyc, P12, 12, entries[m]), 0.0)
    c2 = bounce(parts, tt + 0.8)
    clips["pipes"] = save("hocket.pipes", c2, detail="five pipes of one pitch each, entering in turn, making one melody between them (ours); Part 8's flute model")
    combined = [None] * 12
    for m, ps in pipes.items():
        for p in ps:
            combined[p] = m
    return {"melody": [list(x) for x in mel], "beat": beat, "ira": ira, "arka": arka, "starts": starts,
            "pipes": {str(k): v for k, v in pipes.items()}, "order": order, "entries": {str(k): v for k, v in entries.items()},
            "combined": combined, "pulse": P12, "clips": clips}


MB_PULSE = 0.16
KUSHAURA = [(0, 50), (0, 69), (2, 57), (4, 67), (6, 55), (6, 71), (8, 62), (10, 69),
            (12, 52), (12, 67), (14, 59), (16, 64), (18, 55), (18, 71), (20, 62), (22, 67)]


def compute_mbira() -> dict:
    # 1. one tine, no buzz then with buzz
    a = arr(tine(67, 0.0, 1.8)).at_level(LEVEL)
    b = arr(tine(67, 0.18, 1.8)).at_level(LEVEL)
    one = concat([a, b], gap=0.6, names=["plain", "buzz"])
    # 2. two interlocking parts, the second a pulse later and a step lower (ours)
    kutsinhira = [(p + 1, m - (2 if m > 60 else 0)) for p, m in KUSHAURA]
    cyc = 24
    parts, starts, t = [], {}, 0.0
    for name, which in (("kushaura", (KUSHAURA,)), ("kutsinhira", (kutsinhira,)), ("both", (KUSHAURA, kutsinhira))):
        starts[name] = t
        reps = 3 if name == "both" else 2
        for part in which:
            for r in range(reps):
                for p, m in part:
                    parts.append((arr(tine(m)), t + (r * cyc + p) * MB_PULSE, -1.0 if m > 60 else 0.0))
        t += reps * cyc * MB_PULSE + 0.9
    c = bounce(parts, t + 0.6)
    return {"ratios": T.TINE, "f": hz(67), "partials": [hz(67) * r for r in T.TINE], "kushaura": KUSHAURA, "kutsinhira": kutsinhira,
            "cycle": cyc, "pulse": MB_PULSE, "starts": starts,
            "clips": {"tine": save("mbira.tine", one, detail="one mbira tine (a clamped-free bar, Part 9) without and with a bottle-cap buzz"),
                      "parts": save("mbira.parts", c, detail="two interlocking mbira parts of ours, each alone, then together; tine models")}}


TARGET = [72, 74, 76, 79, 76, 74, 72, 67, 69, 72, 74, 72]
LOW = [55, 59, 62, 57]
SPLIT = 66


def compute_inherent() -> dict:
    a, b, target = T.design_inherent(TARGET, LOW, 3)
    n = len(TARGET) * 3
    heard = T.inherent([a, b], SPLIT)
    assert [p for _, p in heard] == TARGET
    fast, slow = 0.1, 0.32
    out = {}

    def render(which, pulse, reps, name, detail):
        parts = []
        for part in which:
            for r in range(reps):
                for i, m in part:
                    parts.append((arr(tine(m, 0.12, 1.0)), (r * n + i) * pulse, -1.5 if m > SPLIT else 0.0))
        out[name] = save(f"inherent.{name}", bounce(parts, reps * n * pulse + 0.9), detail=detail)
    render((a,), fast, 2, "a", "one interlocking part alone, fast; tine model")
    render((b,), fast, 2, "b", "the other part alone, fast; tine model")
    render((a, b), fast, 3, "both", "both parts together, fast: the high notes form a melody neither plays; tine model")
    render((a, b), slow, 1, "slow", "both parts together, slowly: the melody no longer separates; tine model")
    render(([(i, m) for i, m in target],), fast, 2, "target", "the high notes alone: the melody heard; tine model")
    hi_a = [m for _, m in a if m > SPLIT]
    hi_b = [m for _, m in b if m > SPLIT]
    decoys = {"A": [76, 74, 72, 74, 76, 79, 81, 79, 76, 74, 72, 74], "B": TARGET, "C": [72, 72, 76, 76, 79, 79, 76, 74, 72, 74, 72, 67]}
    return {"a": a, "b": b, "target": target, "n": n, "split": SPLIT, "fast": fast, "slow": slow, "high_a": hi_a, "high_b": hi_b,
            "options": decoys, "answer": "B", "rate_fast": 1 / fast, "rate_slow": 1 / slow, "clips": out}


def compute_clave() -> dict:
    out = {}
    parts, starts, t = [], {}, 0.0
    pulse8 = 0.15
    for name in ("tresillo (8)", "cinquillo (8)"):
        starts[name] = t
        place(parts, cached(("clave",), lambda: DK.clave()), cycle_times(T.onsets(T.TIMELINES[name]), 4, pulse8, 8, t), -2.0)
        place(parts, drum(80.0, "press"), cycle_times([0, 4], 4, pulse8, 8, t), -14.0)
        t += 4 * 8 * pulse8 + 0.8
    starts["habanera"] = t
    hab = [0, 3, 4, 6]
    for c in range(4):
        root = [48, 43, 48, 43][c]
        for o, step in zip(hab, (0, 7, 12, 7)):
            parts.append((arr(pluck(root + step, 0.5)), t + (c * 8 + o) * pulse8, 0.0))
    place(parts, cached(("clave",), lambda: DK.clave()), cycle_times(T.onsets(T.TIMELINES["tresillo (8)"]), 4, pulse8, 8, t), -8.0)
    t += 4 * 8 * pulse8 + 0.8
    c = bounce(parts, t)
    out["family"] = save("clave.family", c, detail="the tresillo and the cinquillo on claves, four bars each; the habanera rhythm on a plucked bass over the tresillo")
    parts, s2, t = [], {}, 0.0
    son = T.onsets(T.TIMELINES["son clave (16)"])
    two3 = sorted((o + 8) % 16 for o in son)
    for name, ons in (("three-two", son), ("two-three", two3)):
        s2[name] = t
        place(parts, cached(("clave",), lambda: DK.clave()), cycle_times(ons, 3, P16, 16, t), -2.0)
        place(parts, drum(80.0, "press"), cycle_times([0, 4, 8, 12], 3, P16, 16, t), -14.0)
        t += 3 * 16 * P16 + 0.8
    c2 = bounce(parts, t)
    out["sides"] = save("clave.sides", c2, detail="son clave three-two, then two-three, on claves with a soft beat")
    return {"starts": starts, "sides": s2, "three_two": son, "two_three": two3, "habanera": hab, "pulse8": pulse8, "pulse": P16,
            "clips": out}


SON_CHORDS = [(48, [60, 64, 67]), (53, [60, 65, 69]), (55, [59, 62, 67]), (53, [60, 65, 69])]


def compute_son() -> dict:
    son = T.onsets(T.TIMELINES["son clave (16)"])
    order = [("clave", 2), ("bass", 2), ("conga", 2), ("guitar", 2), ("all", 4)]
    entries, t = {}, 0.0
    for name, c in order:
        entries[name] = t
        t += c * 16 * P16
    total = int(round(t / (16 * P16)))
    parts = []
    place(parts, cached(("clave",), lambda: DK.clave()), cycle_times(son, total, P16, 16), -4.0)
    c0 = int(round(entries["bass"] / (16 * P16)))
    for c in range(c0, total):
        t0 = c * 16 * P16
        root, _ = SON_CHORDS[c % 4]
        nxt, _ = SON_CHORDS[(c + 1) % 4]
        parts.append((arr(pluck(root - 12 + 7, 0.9)), t0 + 6 * P16, 0.0))   # the fifth on the and of two
        parts.append((arr(pluck(nxt - 12, 1.2)), t0 + 12 * P16, 0.0))       # the next chord's root, early
    c1 = int(round(entries["conga"] / (16 * P16)))
    for c in range(c1, total):
        t0 = c * 16 * P16
        parts.append((arr(drum(200.0, "slap")), t0 + 4 * P16, -8.0))
        parts.append((arr(drum(200.0, "press")), t0 + 8 * P16, -12.0))
        parts.append((arr(drum(200.0, "open")), t0 + 14 * P16, -5.0))
        parts.append((arr(drum(200.0, "open")), t0 + 15 * P16, -5.0))
    c2 = int(round(entries["guitar"] / (16 * P16)))
    gpat = [(2, 0), (3, 1), (5, 2), (7, 1), (8, 0), (10, 2), (11, 1), (13, 0)]
    for c in range(c2, total):
        t0 = c * 16 * P16
        _, ch = SON_CHORDS[c % 4]
        for o, k in gpat:
            parts.append((arr(pluck(ch[k] + 12, 0.45)), t0 + o * P16, -6.0))
    c = bounce(parts, t + 1.2)
    return {"entries": entries, "order": [n for n, _ in order], "chords": ["C", "F", "G", "F"], "clave": son, "guitar": gpat,
            "pulse": P16, "cycles": total,
            "clips": {"layers": save("son.layers", c, detail="a son texture of ours over son clave: bass anticipating each chord, conga, and a guitar figure, entering in turn; plucked-string, bar and membrane models")}}


SAMBA_P = 0.13
SAMBA = {
    "surdo2": [0, 8],                    # the higher surdo on the first beat of each bar
    "surdo1": [4, 12],                   # the deeper surdo answers on the second
    "caixa": list(range(16)),
    "shaker": list(range(16)),
    "tamborim": [0, 2, 5, 7, 8, 10, 13, 15],
    "agogo_hi": [0, 3, 6, 10],
    "agogo_lo": [2, 8, 12, 14],
}


def compute_samba() -> dict:
    order = [("surdos", 2), ("caixa", 2), ("shaker", 1), ("tamborim", 2), ("agogo", 2), ("all", 3)]
    entries, t = {}, 0.0
    for name, c in order:
        entries[name] = t
        t += c * 16 * SAMBA_P
    total = int(round(t / (16 * SAMBA_P)))
    parts = []

    def cyc_from(name):
        return int(round(entries[name] / (16 * SAMBA_P)))
    for c in range(total):
        t0 = c * 16 * SAMBA_P
        for o in SAMBA["surdo2"]:
            parts.append((arr(drum(72.0, "open", 0.9)), t0 + o * SAMBA_P, -5.0))
        for o in SAMBA["surdo1"]:
            parts.append((arr(drum(56.0, "open", 1.1)), t0 + o * SAMBA_P, -4.0))
        if c >= cyc_from("caixa"):
            for o in SAMBA["caixa"]:
                acc = o % 4 in (1, 3)
                parts.append((arr(cached(("snare", acc, o % 2), lambda acc=acc, o=o: noise_burst(1800, 7000, 0.09, 45.0, 51 + o % 2))), t0 + o * SAMBA_P, -12.0 if acc else -17.0))
        if c >= cyc_from("shaker"):
            for o in SAMBA["shaker"]:
                parts.append((arr(shaker(o)), t0 + o * SAMBA_P, -15.0 if o % 2 else -12.0))
        if c >= cyc_from("tamborim"):
            for o in SAMBA["tamborim"]:
                parts.append((arr(drum(520.0, "slap")), t0 + o * SAMBA_P, -9.0))
        if c >= cyc_from("agogo"):
            for o in SAMBA["agogo_hi"]:
                parts.append((arr(bell()), t0 + o * SAMBA_P, -10.0))
            for o in SAMBA["agogo_lo"]:
                parts.append((arr(bell(True)), t0 + o * SAMBA_P, -10.0))
    c = bounce(parts, t + 1.2)
    return {"entries": entries, "order": [n for n, _ in order], "parts": SAMBA, "pulse": SAMBA_P, "cycles": total,
            "clips": {"layers": save("samba.layers", c, detail="a batucada of ours: two surdos answering, caixa, shaker, tamborim and agogo, entering in turn; membrane, noise and modal models")}}


CALL = [(67, 0, 2), (69, 2, 1), (72, 3, 2), (69, 5, 1), (67, 6, 3), (64, 9, 3)]
RESP = [(72, 0, 2), (69, 2, 1), (67, 3, 2), (64, 5, 1), (62, 6, 3), (60, 9, 3)]


def compute_callresp() -> dict:
    cyc = 12 * P12
    rounds = 3
    notes_lead, notes_ch = [], []
    for r in range(rounds):
        base = r * 2 * cyc
        call = CALL if r < 2 else [(m + (2 if i == 2 else 0), a, d) for i, (m, a, d) in enumerate(CALL)]
        for m, a, d in call:
            notes_lead.append((m, base + a * P12, d * P12 * 0.95))
        for m, a, d in RESP:
            notes_ch.append((m, base + cyc + a * P12 - (2 * P12 if r == 2 and a == 0 else 0), d * P12 * 0.95 + (2 * P12 if r == 2 and a == 0 else 0)))
    total = rounds * 2 * cyc
    lead = CH.sing(notes_lead, "soprano", "a", seed=1)
    chorus = [CH.sing(notes_ch, "soprano", "O", seed=2), CH.sing([(m - 12, a, d) for m, a, d in notes_ch], "tenor", "O", seed=3),
              CH.sing([(m - 5, a, d) for m, a, d in notes_ch], "alto", "O", seed=4)]
    parts = [(arr(lead), 0.0, 0.0)]
    for k, y in enumerate(chorus):
        parts.append((arr(y), 0.0, (-2.0, -4.0, -5.0)[k]))
    place(parts, bell(), cycle_times(T.onsets(STANDARD), rounds * 2, P12, 12), -12.0)
    place(parts, drum(95.0), cycle_times([0, 3, 6, 9], rounds * 2, P12, 12), -9.0)
    c = bounce(parts, total + 1.2)
    return {"call": CALL, "response": RESP, "rounds": rounds, "cycle": cyc, "pulse": P12, "overlap": 2 * P12,
            "clips": {"song": save_synth("callresp.song", c, detail="a call by one voice answered by a chorus, three times over the bell and a drum, the last answer overlapping the call; model voices, modal and membrane models")}}


UNEVEN = [0.28, 0.33, 0.39]              # illustrative proportions of a beat (ours), short-medium-long


def compute_uneven() -> dict:
    beat = 0.6
    out = {}
    for name, props in (("even", [1 / 3] * 3), ("uneven", UNEVEN)):
        parts = []
        offs = np.concatenate([[0.0], np.cumsum(props)[:-1]])
        for b in range(16):
            for k, o in enumerate(offs):
                st = "slap" if k == 0 and b % 4 else ("open" if k == 0 else "press")
                parts.append((arr(drum(150.0 if st != "slap" else 150.0, st)), (b + o) * beat, -2.0 if k == 0 else -6.0))
        place(parts, drum(70.0, "open", 0.9), [b * beat for b in range(0, 16, 4)], -6.0)
        out[name] = save(f"uneven.{name}", bounce(parts, 16 * beat + 0.8), detail=("a beat divided into three equal parts" if name == "even" else "a beat divided into three unequal parts, short-medium-long (illustrative proportions)") + "; membrane models")
    return {"beat": beat, "even": [1 / 3] * 3, "uneven": UNEVEN, "clips": out}


TUNE_PULSE = 0.12
TUNE_LOW = [55, 60, 64, 59, 62, 57]


def compute_tune() -> dict:
    mel = tune_line(14, 72)
    events = [(int(round(3 * a)), m) for m, a, _ in mel]
    n = int(round(3 * (mel[-1][1] + mel[-1][2])))
    a, b = T.interlock_melody(events, n, TUNE_LOW)
    heard = T.inherent([a, b], SPLIT)
    assert [p for _, p in heard] == [m for m, _, _ in mel]
    hi_a = [m for _, m in a if m > SPLIT]
    hi_b = [m for _, m in b if m > SPLIT]
    sections = [("a", (a,), 1, False), ("b", (b,), 1, False), ("both", (a, b), 2, False), ("claves", (a, b), 2, True)]
    parts, starts, t = [], {}, 0.0
    for name, which, reps, withclaves in sections:
        starts[name] = t
        for part in which:
            for r in range(reps):
                for i, m in part:
                    parts.append((arr(tine(m, 0.12, 1.0)), t + (r * n + i) * TUNE_PULSE, -1.5 if m > SPLIT else 0.0))
        if withclaves:
            place(parts, cached(("clave",), lambda: DK.clave()), cycle_times(T.onsets(STANDARD), reps * n // 12, TUNE_PULSE, 12, t), -8.0)
            place(parts, drum(85.0), cycle_times([0, 3, 6, 9], reps * n // 12, TUNE_PULSE, 12, t), -6.0)
        t += reps * n * TUNE_PULSE + 0.9
    s_ = bounce(parts, t + 0.6)
    s_.events = starts
    return {"a": a, "b": b, "n": n, "events": events, "pulse": TUNE_PULSE, "split": SPLIT, "high_a": hi_a, "high_b": hi_b,
            "starts": starts, "seconds": s_.duration, "melody": [list(x) for x in mel],
            "clips": {"variation": save("tune.variation37", s_, detail="the Tune's first two phrases as an inherent pattern: two interlocking mbira parts, each alone, then together, then over the standard pattern on claves; tine, bar and membrane models")}}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 37, "title": "as an inherent pattern of two interlocking parts, then over the standard pattern", "seconds": round(t["seconds"], 1),
            "measure": f"14 notes heard, {len(t['high_a'])} played by one part and {len(t['high_b'])} by the other; {t['n']} pulses, {round(1 / t['pulse'])} a second",
            "clip": "tune.variation37"}


ITEMS = {"hook": compute_hook, "scale": compute_scale, "metrics": compute_metrics, "ewe": compute_ewe, "threetwo": compute_threetwo,
         "hocket": compute_hocket, "mbira": compute_mbira, "inherent": compute_inherent, "clave": compute_clave, "son": compute_son,
         "samba": compute_samba, "callresp": compute_callresp, "uneven": compute_uneven, "tune": compute_tune, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
