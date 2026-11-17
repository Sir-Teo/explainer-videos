"""Precompute everything numerical, and every sound, in Part 45 of *Music, Built* ("The Scene").

    python -m videos.music.music45.compute              # everything missing (about a minute)
    python -m videos.music.music45.compute --force timbre

Numbers are cached in ``.cache/music45/<name>.json``, sounds in ``.cache/music45/audio/``.  The tools are Monochord's
(``explainer/music/monochord/scene.py``).  The demonstrations are built the way the classic experiments built them:
sine tones, harmonic complexes, noise, Shepard tones (all synthesized), with Part 7's piano and the series' other
instruments where a real timbre matters.  The scale illusion is in stereo and wants headphones.

Items:
    hook        the scale illusion (stereo): what each ear gets, and what is heard
    aba         ABA- triplets at four combinations of interval and speed
    boundary    the streaming model fitted to van Noorden's boundary
    inter       an ear question: a tune interleaved with another, then released by register
    compound    implied polyphony: one line, slow then fast
    mistune     a harmonic complex with its 4th harmonic mistuned by 0, 1, 3 and 8 per cent
    onset       the same complex with the 4th harmonic starting with the rest, then 80 ms early
    cont        a glide with a gap, silent, then filled with noise
    fuse        two voices in parallel fifths, then in contrary motion
    timbre      a timbre space of the series' instruments
    shepard     an ear question: 24 rising steps of Shepard tones
    each        the scale illusion's two ears, one at a time
    fission     a fast ABA- sequence below the fission boundary
    ambig       a long ABA- sequence in the ambiguous region
    fate        harmonics given a vibrato together: common fate
    place       one harmonic moved to one ear
    melcont     a melody interrupted by silence, then by noise
    bounce      a rising and a falling scale crossing
    tstream     one pitch alternating between two timbres, slow then fast
    octaves     the Tune with its notes in random octaves
    risset      a Shepard-Risset glissando
    memory      two pitch-memory trials
    tune        Variation 45: the Tune hidden in another line, then released by timbre and by register
    variation   the Variations ledger, row 45
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import melody as M
from explainer.music.monochord import orchestra as O
from explainer.music.monochord import scene as SC
from explainer.music.monochord import screen as SCR
from explainer.music.monochord import tune as T
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.partkit import saver, signoff
from videos.music.music38 import compute as P38

CACHE = Cache("music45")
CLIPS = ClipStore("music45")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
save_synth = saver(CLIPS, LEVEL, kind="synthesized")
arr = P38.arr
piano, bass = P38.piano, P38.bass


def sine(m, seconds, sr=SR):
    t = np.arange(int(seconds * sr)) / sr
    env = np.clip(t / 0.01, 0, 1) * np.clip((seconds - t) / 0.02, 0, 1)
    return env * np.sin(2 * np.pi * float(SC.hz(m)) * t)


# ---------------------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    s = SC.scale_illusion(60)
    ioi = 0.25
    parts = []
    for rep in range(2):
        for i, (r, l) in enumerate(zip(s["right"], s["left"])):
            t0 = rep * 8 * ioi + i * ioi
            parts.append((Clip(sine(r, 0.24), SR), t0, 0.0, 1.0))
            parts.append((Clip(sine(l, 0.24), SR), t0, 0.0, -1.0))
    c = Clip(mix(parts, duration=16 * ioi + 0.6).y, SR)
    return {**s, "ioi": ioi, "leap_right": SC.leaps(s["right"]), "leap_heard": SC.leaps(s["heard_high"]),
            "clips": {"stereo": save_synth("hook.stereo", c, detail="Deutsch's scale illusion: the C major scale up and down at once, successive tones alternating between the ears; sine tones, stereo", needs="headphones")}}


ABA = [("3 semitones, slow", 3, 0.15), ("12 semitones, slow", 12, 0.15), ("6 semitones, slow", 6, 0.15), ("6 semitones, fast", 6, 0.06)]


def compute_aba() -> dict:
    fit = SC.fit_boundary(SC.VAN_NOORDEN_TCB)
    clips, out = [], []
    for name, st, trt in ABA:
        cyc = max(6, int(2.4 / (4 * trt)))
        clips.append(Clip(SC.aba(st, trt, cyc, f_a=1000.0), SR))
        out.append({"name": name, "semitones": st, "trt": trt, "model_streams": SC.streams(st, trt, f_a=1000.0, tau=1.0, width=fit["k"]),
                    "boundary_st": float(SC.boundary(trt, 1000.0, tau=1.0, width=fit["k"]))})
    c = concat(clips, gap=0.9, names=[o["name"] for o in out])
    return {"cases": out, "starts": {o["name"]: float(c.events[o["name"]]) for o in out},
            "clips": {"four": save_synth("aba.four", c, detail="ABA- triplets of sine tones on A = 1 kHz: B 3, 12 and 6 semitones above A, slow, then 6 semitones fast")}}


def compute_boundary() -> dict:
    fit = SC.fit_boundary(SC.VAN_NOORDEN_TCB)
    trt = np.linspace(0.04, 0.17, 60)
    return {"points": SC.VAN_NOORDEN_TCB, "fission": SC.VAN_NOORDEN_FB, "k": fit["k"], "rms_st": fit["rms_st"],
            "trt": trt.tolist(), "model": SC.boundary(trt, 1000.0, tau=1.0, width=fit["k"]).tolist()}


def compute_inter() -> dict:
    fj = [x for x in M.corpus() if x.name == "Frère Jacques"][0]
    tune = [67 + p for p in fj.pitches[:16]]
    rng = np.random.default_rng(7)
    lo, hi = min(tune) - 1, max(tune) + 2
    distr = []
    scale = [x for x in range(lo - 4, hi + 5) if x % 12 in (0, 2, 4, 5, 7, 9, 11)]
    for i, m in enumerate(tune):                                  # a distractor in the same register, crossing at every note
        j = scale.index(m) + (2 if i % 2 == 0 else -2) + int(rng.integers(-1, 2)) * 0
        distr.append(int(scale[j]))
    ioi = 0.11
    def line(a, b, shift_b=0, timbre_b="piano"):
        p = []
        for i, (x, y) in enumerate(zip(a, b)):
            p.append((arr(piano(x, 0.2, 0.7)), 2 * i * ioi, 0.0))
            if timbre_b == "piano":
                p.append((arr(piano(y + shift_b, 0.2, 0.7)), (2 * i + 1) * ioi, 0.0))
        return Clip(mix(p, duration=2 * len(a) * ioi + 0.6).y, SR)
    same = line(tune, distr)
    apart = line(tune, distr, shift_b=-19)
    c = concat([same, same, apart], gap=0.9, names=["same", "again", "apart"])
    return {"tune": tune, "distractor": distr, "crossings": SC.crossings(tune, distr), "crossings_apart": SC.crossings(tune, [d - 19 for d in distr]),
            "ioi": ioi, "answer": "Frère Jacques", "starts": {k: float(c.events[k]) for k in ("same", "again", "apart")},
            "clips": {"three": save("inter.three", c, detail="a familiar tune interleaved note by note with another line in the same register, twice, then with the other line an octave and a half lower; Part 7's piano")}}


def compute_compound() -> dict:
    """Implied polyphony: one line alternating between a moving lower part and a repeated upper note, slow then fast."""
    low = [55, 57, 59, 60, 62, 60, 59, 57]
    line = []
    for x in low:
        line += [x, 72]
    clips = []
    for ioi in (0.32, 0.11):
        p = [(arr(piano(m, max(ioi * 1.1, 0.15), 0.7)), i * ioi, 0.0) for i, m in enumerate(line * 2)]
        clips.append(Clip(mix(p, duration=len(line) * 2 * ioi + 0.6).y, SR))
    c = concat(clips, gap=0.9, names=["slow", "fast"])
    return {"line": line, "iois": [0.32, 0.11], "starts": {k: float(c.events[k]) for k in ("slow", "fast")},
            "clips": {"two": save("compound.two", c, detail="one line of ours alternating between a moving lower part and a repeated high C, slow, then fast; Part 7's piano")}}


def compute_mistune() -> dict:
    ms = [0.0, 0.01, 0.03, 0.08]
    clips = [Clip(SC.harmonic_complex(200.0, 10, 1.2, m, 4), SR) for m in ms]
    c = concat(clips, gap=0.5, names=[f"{int(100 * m)}" for m in ms])
    return {"mistunes": ms, "cents": [float(1200 * np.log2(1 + m)) for m in ms], "pop": [SC.pop_out(m) for m in ms],
            "starts": {f"{int(100 * m)}": float(c.events[f"{int(100 * m)}"]) for m in ms},
            "clips": {"four": save_synth("mistune.four", c, detail="ten equal harmonics of 200 Hz, the 4th mistuned by 0, 1, 3 and 8 per cent")}}


def compute_onset() -> dict:
    a = Clip(SC.harmonic_complex(200.0, 10, 1.2, 0.0, 4, 0.0), SR)
    b = Clip(SC.harmonic_complex(200.0, 10, 1.2, 0.0, 4, 0.08), SR)
    c = concat([a, b], gap=0.6, names=["together", "early"])
    return {"lead": 0.08, "starts": {k: float(c.events[k]) for k in ("together", "early")},
            "clips": {"two": save_synth("onset.two", c, detail="ten harmonics of 200 Hz starting together, then with the 4th starting 80 ms early")}}


def compute_cont() -> dict:
    a = Clip(SC.continuity(0.15, "silence"), SR)
    b = Clip(SC.continuity(0.15, "noise"), SR)
    c = concat([a, b], gap=0.7, names=["silence", "noise"])
    return {"gap": 0.15, "starts": {k: float(c.events[k]) for k in ("silence", "noise")},
            "clips": {"two": save_synth("cont.two", c, detail="a rising glide with a 150 ms gap left silent, then filled with louder noise")}}


def compute_fuse() -> dict:
    top = [72, 74, 76, 77, 79, 77, 76, 74, 72]
    par = [m - 7 for m in top]
    con = [65, 64, 62, 60, 59, 60, 62, 64, 65]
    beat = 0.4
    def two(a, b):
        p = []
        for i, (x, y) in enumerate(zip(a, b)):
            p.append((arr(O.note("violin", x, beat * 0.97)), i * beat, 0.0))
            p.append((arr(O.note("violin", y, beat * 0.97)), i * beat, 0.0))
        return Clip(mix(p, duration=len(a) * beat + 0.5).y, SR)
    c = concat([two(top, par), two(top, con)], gap=0.8, names=["parallel", "contrary"])
    f0 = float(SC.hz(60))
    fus = {"parallel": float(np.mean([O.fusion([("violin", a, 1.0), ("violin", b, 1.0)], float(SC.hz(b)), cents=20) for a, b in zip(top, par)])),
           "contrary": float(np.mean([O.fusion([("violin", a, 1.0), ("violin", b, 1.0)], float(SC.hz(min(a, b))), cents=20) for a, b in zip(top, con)]))}
    return {"top": top, "parallel": par, "contrary": con, "fusion": fus, "beat": beat,
            "starts": {k: float(c.events[k]) for k in ("parallel", "contrary")},
            "clips": {"two": save_synth("fuse.two", c, detail="two violin lines a fifth apart moving in parallel, then the same upper line against a lower one in contrary motion; additive, from the bowed-string spectrum")}}


def instruments():
    """One note of each of the series' instruments, with its fundamental."""
    chip = SCR.Chip()
    out = {
        "piano": (np.asarray(piano(60, 1.5, 0.8)), SC.hz(60)),
        "plucked string": (np.asarray(bass(48, 1.5)), SC.hz(48)),
        "flute": (O.note("flute", 72, 1.5), SC.hz(72)),
        "clarinet": (O.note("clarinet", 60, 1.5), SC.hz(60)),
        "saxophone": (O.note("saxophone", 60, 1.5), SC.hz(60)),
        "trumpet, soft": (O.note("trumpet p", 60, 1.5), SC.hz(60)),
        "trumpet, loud": (O.note("trumpet f", 60, 1.5), SC.hz(60)),
        "horn": (O.note("horn", 60, 1.5), SC.hz(60)),
        "violin": (O.note("violin", 67, 1.5), SC.hz(67)),
        "celesta": (O.note("celesta", 72, 1.5), SC.hz(72)),
        "chip pulse": (chip.pulse(float(SC.hz(60)), 1.5, 0.25, 12) * np.clip(np.arange(int(1.5 * SR)) / SR / 0.003, 0, 1), SC.hz(60)),
        "chip triangle": (chip.triangle(float(SC.hz(60)), 1.5) * np.clip(np.arange(int(1.5 * SR)) / SR / 0.003, 0, 1), SC.hz(60)),
        "voice": (CH.sing([(60, 0.0, 1.4)], part="tenor", vowel="a"), SC.hz(60)),
    }
    return out


def compute_timbre() -> dict:
    ins = instruments()
    feats = {k: SC.features(y, float(f0)) for k, (y, f0) in ins.items()}
    space = SC.timbre_space(feats)
    order = list(ins)
    clips = [Clip(np.asarray(ins[k][0], float) / np.abs(ins[k][0]).max(), SR).fade(0.002, 0.08) for k in order]
    clips = [Clip(c.y[: int(0.9 * SR)], SR).fade(0.0, 0.08) for c in clips]
    c = concat(clips, gap=0.25, names=order)
    return {"features": feats, "space": space, "starts": {k: float(c.events[k]) for k in order},
            "clips": {"tour": save_synth("timbre.tour", c, detail="one note on each of the series' instruments: piano, plucked string, the additive orchestra, the chip, the model voice")}}


def compute_shepard() -> dict:
    y = SC.shepard(25, 1.0)
    c = Clip(y, SR)
    return {"steps": 25, "step_st": 1.0, "tone": 0.35, "gap": 0.05, "answer": "the same", "centre": 6.0, "sigma": 1.6, "base": 20.0,
            "clips": {"steps": save_synth("shepard.steps", c, detail="25 Shepard tones, each a semitone above the last: partials an octave apart under a fixed bell-shaped envelope")}}


def compute_tune() -> dict:
    ev = T.events(0.12, [0, 1])
    major = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
    tune = []
    for e in ev:
        reps = max(1, int(round(e["dur"])))
        tune += [72 + major[e["degree"]]] * reps
    rng = np.random.default_rng(45)
    lo, hi = min(tune) - 2, max(tune) + 2
    scale = [x for x in range(lo - 4, hi + 5) if x % 12 in (0, 2, 4, 5, 7, 9, 11)]
    distr = [int(scale[scale.index(m) + (2 if i % 2 == 0 else -2)]) for i, m in enumerate(tune)]
    chip = SCR.Chip()
    ioi = 0.12
    def render(mode):
        p = []
        for i, (x, y) in enumerate(zip(tune, distr)):
            p.append((arr(piano(x, 0.22, 0.7)), 2 * i * ioi, 0.0))
            if mode == "same":
                p.append((arr(piano(y, 0.22, 0.7)), (2 * i + 1) * ioi, 0.0))
            elif mode == "timbre":
                p.append((Clip(chip.pulse(float(SC.hz(y)), 0.2, 0.125, 8), SR), (2 * i + 1) * ioi, -6.0))
            else:
                p.append((Clip(chip.pulse(float(SC.hz(y - 24)), 0.2, 0.125, 8), SR), (2 * i + 1) * ioi, -6.0))
        return Clip(mix(p, duration=2 * len(tune) * ioi + 0.6).y, SR)
    c = concat([render("same"), render("timbre"), render("register")], gap=1.0, names=["hidden", "timbre", "register"])
    return {"tune": tune, "distractor": distr, "ioi": ioi, "crossings": SC.crossings(tune, distr), "seconds": c.duration,
            "starts": {k: float(c.events[k]) for k in ("hidden", "timbre", "register")},
            "clips": {"variation45": save_synth("tune.variation45", c, detail="the Tune's first two phrases interleaved with a line of ours on the same piano, then the other line on the chip's thin pulse, then two octaves lower; Part 7's piano and our chip")}}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 45, "title": "hidden in another line, then released by timbre and by register", "seconds": round(t["seconds"], 1),
            "measure": f"{len(t['tune'])} notes of the Tune interleaved with {len(t['distractor'])} others; the two lines cross {t['crossings']} times",
            "clip": "tune.variation45"}


# ---------------------------------------------------------------------------------------------------- more demonstrations
def compute_each() -> dict:
    s = SC.scale_illusion(60)
    ioi = 0.25
    out = []
    for side, pan in (("left", -1.0), ("right", 1.0)):
        parts = [(Clip(sine(m, 0.24), SR), i * ioi, 0.0, pan) for i, m in enumerate(s[side])]
        out.append(Clip(mix(parts, duration=8 * ioi + 0.4).y, SR))
    c = concat(out, gap=0.8, names=["left", "right"])
    return {"left": s["left"], "right": s["right"], "ioi": ioi, "starts": {k: float(c.events[k]) for k in ("left", "right")},
            "clips": {"two": save_synth("each.two", c, detail="the scale illusion's left ear alone, then its right ear alone; sine tones, stereo", needs="headphones")}}


def compute_fission() -> dict:
    c = Clip(SC.aba(1.0, 0.06, 14, f_a=1000.0), SR)
    return {"semitones": 1.0, "trt": 0.06, "fission": SC.VAN_NOORDEN_FB,
            "clips": {"fast": save_synth("fission.fast", c, detail="ABA- triplets, B one semitone above A = 1 kHz, 60 ms apart: fast, but below the fission boundary")}}


def compute_ambig() -> dict:
    fit = SC.fit_boundary(SC.VAN_NOORDEN_TCB)
    trt, st = 0.09, 6.0
    c = Clip(SC.aba(st, trt, 30, f_a=1000.0), SR)
    return {"trt": trt, "semitones": st, "boundary": float(SC.boundary(trt, 1000.0, tau=1.0, width=fit["k"])), "fission": SC.VAN_NOORDEN_FB,
            "clips": {"long": save_synth("ambig.long", c, detail="ABA- triplets, B six semitones above A = 1 kHz, 90 ms apart, thirty times: inside the ambiguous region")}}


def compute_fate() -> dict:
    f0, n, sec = 200.0, 10, 3.0
    t = np.arange(int(sec * SR)) / SR
    def tone(vib):
        y = np.zeros_like(t)
        for k in range(1, n + 1):
            moving = vib and k in (3, 5, 7)
            dev = (0.02 * np.sin(2 * np.pi * 5.5 * t) * np.clip((t - 1.0) / 0.3, 0, 1)) if moving else 0.0
            y += np.sin(2 * np.pi * np.cumsum(k * f0 * (1 + dev)) / SR)
        env = np.clip(t / 0.03, 0, 1) * np.clip((sec - t) / 0.05, 0, 1)
        return Clip(env * y / np.abs(env * y).max(), SR)
    c = concat([tone(False), tone(True)], gap=0.7, names=["still", "moving"])
    return {"moving": [3, 5, 7], "from": 1.0, "starts": {k: float(c.events[k]) for k in ("still", "moving")},
            "clips": {"two": save_synth("fate.two", c, detail="ten harmonics of 200 Hz held still, then with harmonics 3, 5 and 7 given a vibrato after one second")}}


def compute_place() -> dict:
    f0, sec = 200.0, 2.4
    t = np.arange(int(sec * SR)) / SR
    env = np.clip(t / 0.03, 0, 1) * np.clip((sec - t) / 0.05, 0, 1)
    rest = sum(np.sin(2 * np.pi * k * f0 * t) for k in range(1, 11) if k != 4) * env
    four = np.sin(2 * np.pi * 4 * f0 * t) * env
    a = Clip(mix([(Clip(rest / 9, SR), 0.0, 0.0, 0.0), (Clip(four / 9, SR), 0.0, 0.0, 0.0)], duration=sec).y, SR)
    b = Clip(mix([(Clip(rest / 9, SR), 0.0, 0.0, 0.0), (Clip(four / 9, SR), 0.0, 0.0, 1.0)], duration=sec).y, SR)
    c = concat([a, b], gap=0.7, names=["centre", "right"])
    return {"starts": {k: float(c.events[k]) for k in ("centre", "right")},
            "clips": {"stereo": save_synth("place.stereo", c, detail="ten harmonics of 200 Hz all in the centre, then with the 4th harmonic moved to the right ear; stereo")}}


def compute_melcont() -> dict:
    ev = T.events(0.5, [0])
    major = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
    rng = np.random.default_rng(3)
    clips = []
    for filler in ("silence", "noise"):
        parts = []
        for e in ev:
            y = np.asarray(O.note("flute", 72 + major[e["degree"]], e["dur"] * 0.5 * 0.98), float)
            if e["i"] in (1, 3, 5):
                n = len(y)
                g0, g1 = int(n * 0.4), int(n * 0.4) + int(0.12 * SR)
                y = y.copy()
                y[g0:g1] = 0.0 if filler == "silence" else 0.0
                if filler == "noise":
                    parts.append((Clip(rng.uniform(-1, 1, g1 - g0) * 0.9, SR), e["t"] + g0 / SR, -2.0))
            parts.append((Clip(y, SR), e["t"], 0.0))
        clips.append(Clip(mix(parts, duration=ev[-1]["t"] + ev[-1]["dur"] * 0.5 + 0.5).y, SR))
    c = concat(clips, gap=0.8, names=["silence", "noise"])
    return {"interrupted": [1, 3, 5], "gap": 0.12, "starts": {k: float(c.events[k]) for k in ("silence", "noise")},
            "clips": {"two": save_synth("melcont.two", c, detail="the Tune's first phrase on the additive flute with 120 ms cut out of three notes, left silent, then filled with noise")}}


def compute_bounce() -> dict:
    up = [60, 62, 64, 65, 67, 69, 71, 72]
    down = up[::-1]
    ioi = 0.2
    parts = []
    for i, (a, b) in enumerate(zip(up, down)):
        parts.append((Clip(sine(a, 0.18), SR), i * ioi, 0.0))
        parts.append((Clip(sine(b, 0.18), SR), i * ioi, 0.0))
    c = Clip(mix(parts * 1, duration=8 * ioi + 0.4).y, SR)
    c = concat([c, c], gap=0.6, names=["one", "two"])
    return {"up": up, "down": down, "ioi": ioi,
            "clips": {"cross": save_synth("bounce.cross", c, detail="a rising and a falling scale of sine tones played together, crossing in the middle, twice")}}


def compute_tstream() -> dict:
    chip = SCR.Chip()
    clips = []
    for ioi in (0.3, 0.09):
        parts = []
        n = int(3.0 / ioi)
        for i in range(n):
            if i % 2 == 0:
                parts.append((arr(piano(67, max(ioi * 1.2, 0.15), 0.7)), i * ioi, 0.0))
            else:
                parts.append((Clip(chip.pulse(float(SC.hz(67)), ioi * 0.8, 0.125, 9), SR), i * ioi, -6.0))
        clips.append(Clip(mix(parts, duration=n * ioi + 0.4).y, SR))
    c = concat(clips, gap=0.8, names=["slow", "fast"])
    return {"iois": [0.3, 0.09], "starts": {k: float(c.events[k]) for k in ("slow", "fast")},
            "clips": {"two": save_synth("tstream.two", c, detail="one pitch, G4, alternating between Part 7's piano and the chip's thin pulse, slow then fast")}}


def compute_octaves() -> dict:
    ev = T.events(0.42, [0, 1])
    major = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
    rng = np.random.default_rng(1972)
    shifts = [int(rng.choice([-12, 0, 12])) for _ in ev]
    shifts[0] = 0
    clips = []
    for sh in ([0] * len(ev), shifts):
        p = [(arr(piano(60 + major[e["degree"]] + s, e["dur"] * 0.42, 0.7)), e["t"], 0.0) for e, s in zip(ev, sh)]
        clips.append(Clip(mix(p, duration=ev[-1]["t"] + 1.0).y, SR))
    c = concat(clips[::-1], gap=0.9, names=["scrambled", "plain"])
    return {"shifts": shifts, "starts": {k: float(c.events[k]) for k in ("scrambled", "plain")},
            "clips": {"two": save("octaves.two", c, detail="the Tune's first two phrases with each note in a random octave, then as written; Part 7's piano")}}


def compute_risset() -> dict:
    sec = 12.0
    t = np.arange(int(sec * SR)) / SR
    y = np.zeros_like(t)
    rate = 1 / 6.0                                                 # an octave every six seconds
    for o in range(9):
        x = (o + rate * t) % 9.0
        amp = np.exp(-((x - 4.5) ** 2) / (2 * 1.5 ** 2))
        f = 30.0 * 2 ** x
        y += amp * np.sin(2 * np.pi * np.cumsum(f) / SR)
    y *= np.clip(t / 0.5, 0, 1) * np.clip((sec - t) / 0.5, 0, 1)
    return {"seconds": sec, "octave_s": 6.0, "clips": {"glide": save_synth("risset.glide", Clip(y / np.abs(y).max(), SR), detail="a Shepard-Risset glissando: octave-spaced partials gliding upward under a fixed envelope, an octave every six seconds, for twelve seconds")}}


def compute_memory() -> dict:
    rng = np.random.default_rng(1970)
    trials = []
    clips = []
    for same in (True, False):
        test = 67
        comp = test if same else test + 1
        inter = [int(x) for x in rng.choice([60, 62, 64, 65, 66, 68, 69, 71, 72, 74], 6, replace=False)]
        p = [(Clip(sine(test, 0.3), SR), 0.0, 0.0)]
        for i, m in enumerate(inter):
            p.append((Clip(sine(m, 0.3), SR), 1.5 + i * 0.4, -2.0))
        p.append((Clip(sine(comp, 0.3), SR), 1.5 + 6 * 0.4 + 1.2, 0.0))
        clips.append(Clip(mix(p, duration=5.6).y, SR))
        trials.append({"same": same, "test": test, "comparison": comp, "between": inter})
    c = concat(clips, gap=1.0, names=["first", "second"])
    return {"trials": trials, "starts": {k: float(c.events[k]) for k in ("first", "second")},
            "clips": {"two": save_synth("memory.two", c, detail="two pitch-memory trials after Deutsch (1970): a tone, six other tones, then a tone that is the same or a semitone higher; sine tones")}}


def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation45", 45)


ITEMS = {"hook": compute_hook, "aba": compute_aba, "boundary": compute_boundary, "inter": compute_inter, "compound": compute_compound, "mistune": compute_mistune,
         "onset": compute_onset, "cont": compute_cont, "fuse": compute_fuse, "timbre": compute_timbre, "shepard": compute_shepard,
         "tune": compute_tune, "variation": compute_variation, "each": compute_each, "fission": compute_fission, "ambig": compute_ambig, "fate": compute_fate,
         "place": compute_place, "melcont": compute_melcont, "bounce": compute_bounce, "tstream": compute_tstream, "octaves": compute_octaves,
         "risset": compute_risset, "memory": compute_memory,
         "signoff": compute_signoff}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
