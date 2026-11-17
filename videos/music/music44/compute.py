"""Precompute everything numerical, and every sound, in Part 44 of *Music, Built* ("Music for Picture and Play").

    python -m videos.music.music44.compute              # everything missing (about two minutes)
    python -m videos.music.music44.compute --force game

Numbers are cached in ``.cache/music44/<name>.json``, sounds in ``.cache/music44/audio/``.  The tools are Monochord's
(``explainer/music/monochord/screen.py``).  The instruments are Part 7's piano and Part 38's plucked bass (physical
models), Part 41's additive orchestra, Part 40's drums, Part 17's model voice, and a sound chip of ours.  Clips that mix
the additive orchestra in are labelled synthesized.  Every cue, game and score is ours; film and game scores are
described, never played.

Items:
    scene       the animated scene's hit points and the tempo that hits them
    hook        an ear question: the comic score cut to the picture, and the same score 0.6 s late
    three       one scene, three scores: comic, suspense, heroic
    sync        an ear question: a door slam 120 ms early, in sync, 120 ms late
    motif       our motive as a leitmotif in three moods
    harmony     four progressions of film harmony: the chromatic mediants, Lydian, the minor iv
    mix         music against dialogue, before and after ducking
    game        a simulated game and its adaptive score
    switch      one change heard switching at once and at the bar line
    quantise    transition delays when switching at once, on the beat, the bar or the phrase
    duty        the chip's pulse at three duty cycles
    noise       the chip's noise channel, long and short, and noise drums
    arp         an ear question: a chord on three channels, then on one (an arpeggio)
    chip        the Tune on the chip
    tune        Variation 44: the Tune as a cue on a hit point, as a leitmotif in three moods, as an adaptive loop
    variation   the Variations ledger, row 44
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import orchestra as O
from explainer.music.monochord import screen as S
from explainer.music.monochord import tune as T
from explainer.music.monochord.instruments import choir as CH
from explainer.music.monochord.partkit import saver, signoff
from videos.music.music38 import compute as P38
from videos.music.music40 import compute as P40

CACHE = Cache("music44")
CLIPS = ClipStore("music44")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
save_synth = saver(CLIPS, LEVEL, kind="synthesized")
arr = P38.arr
piano, bass = P38.piano, P38.bass
_C: dict = {}

HITS = [3.20, 7.95, 11.40]          # the door opens; the figure reaches the edge; it lands
START = 0.5                          # the cue's first downbeat
END = 13.5
MOTIVE = [(64, 0.0, 0.5), (62, 0.5, 0.5), (60, 1.0, 1.0), (67, 2.0, 2.0)]     # Part 42's motive


def cached(key, fn):
    if key not in _C:
        _C[key] = fn()
    return _C[key]


def inst(name, m, seconds):
    seconds = round(max(seconds, 0.08), 2)
    return cached(("o", name, m, seconds), lambda: O.note(name, m, seconds))


def sect(name, m, seconds, players=6, seed=0):
    seconds = round(max(seconds, 0.1), 2)
    return cached(("s", name, m, seconds, players, seed), lambda: O.section(name, m, seconds, players=players, seed=seed))


def place(parts, end):
    return Clip(mix(parts, duration=end).y, SR)


def bpm_for_scene():
    r = S.find_tempo(HITS, start=START, lo=70, hi=160, tol_frames=1.0)
    best = min(r["solutions"], key=lambda s: s["worst_frames"])
    return r, best


# --------------------------------------------------------------------------------------------------------- scores
def comic(bpm, offset=0.0):
    """Mickey-mousing: a walking staccato bass and piano on every beat, a door 'creak' chord, a teetering trill,
    a falling glide, a landing thump.  Everything lands on the beats the tempo was chosen for."""
    beat = 60.0 / bpm
    parts = []
    t, k = START, 0
    walk = [48, 52, 55, 52]
    while t < HITS[1] - 0.05:
        parts.append((arr(bass(walk[k % 4], beat * 0.4)), t + offset, -2.0))
        parts.append((arr(piano(72 + [0, 4, 7, 4][k % 4], beat * 0.3, 0.7)), t + offset + beat / 2, -4.0))
        t += beat
        k += 1
    for m in (60, 63, 66, 69):                                     # the door: a diminished chord stab
        parts.append((arr(piano(m + 12, 0.6, 1.0)), HITS[0] + offset, -1.0))
    tr = HITS[1]
    while tr < HITS[1] + 1.0:                                       # teetering: a trill
        for m in (79, 81):
            parts.append((arr(piano(m, 0.09, 0.6)), tr + offset, -5.0))
            tr += 0.09
    n = int((HITS[2] - (HITS[1] + 1.0)) * SR)                       # the fall: a falling glide, synthesized
    tt = np.arange(n) / SR
    f = 1200 * (180 / 1200) ** (tt / tt[-1])
    glide = 0.4 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.clip(tt / 0.05, 0, 1)
    parts.append((Clip(glide, SR), HITS[1] + 1.0 + offset, -8.0))
    parts.append((arr(P40.kick()), HITS[2] + offset, 2.0))         # the landing
    for m in (48, 55, 60, 64):
        parts.append((arr(piano(m, 1.5, 0.8)), HITS[2] + offset, -2.0))
    return place(parts, END + offset)


def suspense(bpm):
    beat = 60.0 / bpm
    parts = [(arr(sect("cello", 36, HITS[1] - START, 6, 1)), START, -3.0), (arr(sect("cello", 37, HITS[1] - START, 6, 2)), START, -6.0)]
    t = START
    while t < HITS[2] - 0.1:                                       # a heartbeat on every beat
        parts.append((arr(P40.k808(0.25)), t, -8.0))
        t += beat
    parts.append((arr(sect("violin", 78, HITS[2] - HITS[0], 8, 3)), HITS[0], -14.0))   # a high, thin tremolo from the door on
    parts.append((arr(sect("violin", 79, HITS[2] - HITS[1], 8, 4)), HITS[1], -14.0))
    for m in (36, 42, 48):                                         # the door: a low tritone stab
        parts.append((arr(inst("horn", m, 1.2)), HITS[0], -4.0))
    for m in (43, 49, 55):                                         # the edge: the stab a fourth higher
        parts.append((arr(inst("horn", m, 1.6)), HITS[1], -4.0))
    parts.append((arr(P40.k808(1.2)), HITS[2], 3.0))
    parts.append((arr(sect("cello", 30, 2.0, 6, 5)), HITS[2], -2.0))
    return place(parts, END)


def heroic(bpm):
    beat = 60.0 / bpm
    parts = []
    chords = [(48, 55, 60, 64), (53, 57, 60, 65), (48, 55, 60, 64), (55, 59, 62, 67)]
    t, k = START, 0
    while t < HITS[2] - 0.1:
        ch = chords[(k // 2) % 4]
        for m in ch:
            parts.append((arr(sect("violin" if m > 55 else "cello", m, beat * 0.95, 4, k + m)), t, -9.0))
        t += beat
        k += 1
    mot = [(m + 7, a, d) for m, a, d in MOTIVE]                    # the motive, in the horn, from the door
    for m, a, d in mot:
        parts.append((arr(inst("horn", m, d * beat * 0.95)), HITS[0] + a * beat, -1.0))
    for m, a, d in mot:
        parts.append((arr(inst("trumpet f", m + 5, d * beat * 0.95)), HITS[1] + a * beat, -3.0))
    for m in (48, 52, 55, 60, 64, 67):
        parts.append((arr(inst("horn" if m < 60 else "trumpet f", m, 2.0)), HITS[2], -2.0))
    parts.append((arr(P40.kick()), HITS[2], 0.0))
    return place(parts, END)


# ---------------------------------------------------------------------------------------------------------- items
def compute_scene() -> dict:
    r, best = bpm_for_scene()
    whole, eighths = best["click"]
    per = 60.0 / best["bpm"]
    clickbpm = S.click_bpm(whole, eighths)
    cerr = [abs(((h - START) / (60.0 / clickbpm)) - round((h - START) / (60.0 / clickbpm))) * (60.0 / clickbpm) * S.FPS for h in HITS]
    sub = S.find_tempo(HITS, start=START, lo=70, hi=160, tol_frames=1.0, subdivision=2)
    return {"hits": HITS, "start": START, "end": END, "frames": [S.frames(h) for h in HITS], "curve_bpm": r["bpm"][::10], "curve_worst": r["worst"][::10],
            "solutions": r["solutions"], "best": best, "click_bpm": clickbpm, "click_err_frames": cerr, "beat": per,
            "eighth_solutions": len(sub["solutions"]), "variable": S.variable_click(HITS, [4, 11, 16], START),
            "events": ["the door opens", "the edge", "the landing"],
            "clips": {"comic": save_synth("scene.comic", comic(best["bpm"]), detail="the comic score of ours at the tempo that hits all three actions; Part 7's piano, a plucked bass, a synthesized glide, Part 9's drum"),
                      "variable": save("scene.variable", comic_variable(S.variable_click(HITS, [4, 11, 16], START))[0], detail="the comic score's walking line on a variable click, the tempo changing slightly at each hit; Part 7's piano, a plucked bass, Part 9's drum")}}


def comic_variable(tempos, beats=(4, 11, 16)):
    """The comic score's walking line with its tempo changed at each hit, so every hit lands exactly."""
    parts = []
    t, k, seg = START, 0, 0
    walk = [48, 52, 55, 52]
    b_edges = [0] + list(beats)
    while k < beats[-1]:
        seg = next(i for i in range(len(beats)) if k < beats[i])
        beat = 60.0 / tempos[seg]
        if t < HITS[1] - 0.05:
            parts.append((arr(bass(walk[k % 4], beat * 0.4)), t, -2.0))
            parts.append((arr(piano(72 + [0, 4, 7, 4][k % 4], beat * 0.3, 0.7)), t + beat / 2, -4.0))
        t += beat
        k += 1
    for m in (60, 63, 66, 69):
        parts.append((arr(piano(m + 12, 0.6, 1.0)), HITS[0], -1.0))
    parts.append((arr(P40.kick()), HITS[2], 2.0))
    for m in (48, 55, 60, 64):
        parts.append((arr(piano(m, 1.5, 0.8)), HITS[2], -2.0))
    return place(parts, END), t


def compute_hook() -> dict:
    bpm = bpm_for_scene()[1]["bpm"]
    a = comic(bpm)
    b = comic(bpm, offset=0.6)
    c = concat([a, b], gap=1.2, names=["first", "second"])
    return {"bpm": bpm, "offset": 0.6, "answer": "first", "starts": {k: float(c.events[k]) for k in ("first", "second")},
            "clips": {"two": save_synth("hook.two", c, detail="the comic score of ours cut to the scene, then the same score starting 0.6 s late; Part 7's piano, a plucked bass, a synthesized glide, Part 9's drum")}}


def compute_three() -> dict:
    bpm = bpm_for_scene()[1]["bpm"]
    c = concat([comic(bpm), suspense(bpm), heroic(bpm)], gap=1.2, names=["comic", "suspense", "heroic"])
    return {"bpm": bpm, "starts": {k: float(c.events[k]) for k in ("comic", "suspense", "heroic")},
            "clips": {"three": save_synth("three.three", c, detail="one scene scored three ways: comic, suspense, heroic; Part 7's piano, the additive orchestra, Part 40's drums")}}


def compute_sync() -> dict:
    out = []
    order = [("early", -0.12), ("in sync", 0.0), ("late", 0.12)]
    seq = [order[i] for i in (2, 0, 1)]
    for name, off in seq:
        parts = [(arr(P40.kick()), 1.0 + off, 0.0), (arr(piano(48, 0.8, 1.0)), 1.0 + off, -6.0)]
        out.append(place(parts, 2.2))
    c = concat(out, gap=0.6, names=[n for n, _ in seq])
    return {"order": [n for n, _ in seq], "offsets": [o for _, o in seq], "slam": 1.0, "answer": "third",
            "itu": {"lead_ms": 45, "lag_ms": 125},
            "starts": {n: float(c.events[n]) for n, _ in seq},
            "clips": {"three": save("sync.three", c, detail="a door slam, three times: the sound 120 ms late, 120 ms early, in sync; Part 9's drum and Part 7's piano")}}


def compute_motif() -> dict:
    beat = 0.42
    moods = {}
    p = []                                                          # heroic: horn, dotted, major, strings
    for m, a, d in [(64, 0, 0.75), (62, 0.75, 0.25), (60, 1.0, 1.0), (67, 2.0, 2.0)]:
        p.append((arr(inst("horn", m, d * beat * 0.95)), a * beat, 0.0))
    for m in (48, 55, 64):
        p.append((arr(sect("cello" if m < 55 else "violin", m, 4 * beat, 4, m)), 0.0, -9.0))
    moods["heroic"] = place(p, 4 * beat + 0.8)
    p, b2 = [], 0.8                                                 # tender: flute, slow, over a soft string chord
    for m, a, d in MOTIVE:
        p.append((arr(inst("flute", m + 12, d * b2 * 0.97)), a * b2, 0.0))
    for m in (53, 57, 60):
        p.append((arr(sect("violin", m, 4 * b2, 4, m)), 0.0, -12.0))
    moods["tender"] = place(p, 4 * b2 + 0.8)
    p, b3 = [], 0.6                                                 # menacing: low, minor, the fifth bent to a tritone
    for m, a, d in [(51, 0, 0.5), (50, 0.5, 0.5), (48, 1.0, 1.0), (54, 2.0, 2.0)]:
        p.append((arr(sect("cello", m - 12, d * b3 * 0.97, 6, m)), a * b3, 0.0))
    p.append((arr(P40.k808(1.0)), 2.0 * b3, -6.0))
    moods["menacing"] = place(p, 4 * b3 + 1.2)
    c = concat(list(moods.values()), gap=0.9, names=list(moods))
    return {"moods": list(moods), "starts": {k: float(c.events[k]) for k in moods},
            "versions": {"heroic": [[64, 0, 0.75], [62, 0.75, 0.25], [60, 1.0, 1.0], [67, 2.0, 2.0]], "tender": [list(n) for n in MOTIVE],
                         "menacing": [[51, 0, 0.5], [50, 0.5, 0.5], [48, 1.0, 1.0], [54, 2.0, 2.0]]},
            "clips": {"three": save_synth("motif.three", c, detail="our motive as a leitmotif: heroic (horn), tender (flute), menacing (low strings, minor, a tritone); the additive orchestra")}}


PROG = {"chromatic mediant: C to A flat": [(48, 55, 60, 64), (44, 51, 60, 63), (48, 55, 60, 64)],
        "chromatic mediant: C to E": [(48, 55, 60, 64), (52, 59, 64, 68), (48, 55, 60, 64)],
        "Lydian: C and D over C": [(48, 55, 60, 64), (48, 54, 62, 66), (48, 55, 60, 64)],
        "the minor iv: C, F minor, C": [(48, 55, 60, 64), (53, 56, 60, 65), (48, 55, 60, 64)]}


def compute_harmony() -> dict:
    clips = []
    for name, chs in PROG.items():
        p = []
        for i, ch in enumerate(chs):
            for m in ch:
                p.append((arr(sect("violin" if m >= 55 else "cello", m, 1.5, 5, m + i)), 1.4 * i, -4.0))
            p.append((arr(inst("horn", ch[-1], 1.3)), 1.4 * i, -6.0))
        clips.append(place(p, 1.4 * len(chs) + 0.8))
    c = concat(clips, gap=0.8, names=list(PROG))
    return {"names": list(PROG), "chords": {k: [list(x) for x in v] for k, v in PROG.items()}, "starts": {k: float(c.events[k]) for k in PROG},
            "clips": {"four": save_synth("harmony.four", c, detail="four progressions of film harmony on strings and horn: two chromatic mediants, a Lydian II over I, the minor iv; the additive orchestra")}}


def babble(seconds=6.0, seed=1):
    """Dialogue stand-in: Part 17's model voice moving through vowels with a speaking pitch contour, in phrases with
    pauses (it sings vowels, it does not speak words)."""
    rng = np.random.default_rng(seed)
    out = np.zeros(int(seconds * SR))
    t = 0.3
    vowels = ["a", "E", "i", "O", "u", "ae", "V", "I"]
    while t < seconds - 1.0:
        dur = rng.uniform(1.0, 1.8)
        notes, a = [], 0.0
        while a < dur:
            d = rng.uniform(0.12, 0.22)
            notes.append((int(45 + rng.integers(-2, 4)), a, d))
            a += d
        y = np.zeros(int((dur + 0.4) * SR))
        for k in range(0, len(notes), 3):
            seg = notes[k:k + 3]
            s0 = seg[0][1]
            v = CH.sing([(m, a - s0, d) for m, a, d in seg], part="tenor", vowel=vowels[int(rng.integers(len(vowels)))], seed=k, tail=0.05)
            i0 = int(s0 * SR)
            y[i0:i0 + len(v)] += v[: len(y) - i0]
        i0 = int(t * SR)
        out[i0:i0 + len(y)] += y[: len(out) - i0]
        t += dur + rng.uniform(0.4, 0.8)
    return out / np.abs(out).max()


def compute_mix() -> dict:
    sec = 7.0
    dia = babble(sec)
    p = []
    for i, ch in enumerate([(48, 55, 64, 67), (53, 57, 65, 69), (55, 59, 62, 67), (48, 55, 64, 72)]):
        for m in ch:
            p.append((arr(sect("violin" if m >= 55 else "cello", m, 1.8, 5, m + i)), 1.75 * i, -2.0))
    for j, (m, a, d) in enumerate([(72, 0, 1), (74, 1, 1), (76, 2, 2), (79, 4, 1), (77, 5, 1), (76, 6, 2), (74, 8, 2), (72, 10, 4)]):
        p.append((arr(inst("horn", m, d * 0.44)), a * 0.44, 0.0))
    music = place(p, sec).y[: len(dia)]
    music = music / np.abs(music).max()
    dia = dia * 0.6
    r = S.duck(music * 0.9, dia, depth_db=10.0)
    before = Clip(music * 0.9 + dia, SR)
    after = Clip(r["music"] + dia, SR)
    c = concat([before, after], gap=1.0, names=["before", "after"])
    g = r["gain"][:: SR // 20]
    env = S.envelope(dia)[:: SR // 20]
    return {"ratio_before_db": r["ratio_before_db"], "ratio_after_db": r["ratio_after_db"], "gain_db": (20 * np.log10(g)).tolist(),
            "dialogue_env": (env / env.max()).tolist(), "step": 0.05, "depth_db": 10.0,
            "starts": {k: float(c.events[k]) for k in ("before", "after")},
            "clips": {"two": save_synth("mix.two", c, detail="a model voice babbling vowels over strings and horn, then the music ducked 10 dB under it; Part 17's voice, the additive orchestra")}}


STATE_C = {"explore": (60, [(48, 55, 64), (45, 52, 60), (41, 48, 57), (43, 50, 59)]),
           "danger": (60, [(36, 43, 51), (36, 42, 51), (36, 43, 51), (35, 42, 50)]),
           "combat": (60, [(36, 43, 51), (39, 46, 55), (41, 48, 56), (43, 50, 55)]),
           "victory": (60, [(48, 55, 64), (53, 57, 65), (55, 59, 62), (48, 55, 64)])}


def render_game(game, plan, score):
    """Play the adaptive score: from each switch, that state's segment, looped; each bar's layers from the intensity
    plan: 1 pad, 2 bass, 3 drums, 4 melody."""
    beat, bar = score.beat, score.bar
    parts = []
    sw = plan["switches"]
    layers = plan["layers"]
    nbars = int(game.length / bar) + 1
    for b in range(nbars):
        t0 = b * bar
        cur = [s for s in sw if s["switch"] <= t0 + 1e-6][-1]["state"]
        li = layers[min(int(t0 / plan["grid_step"]), len(layers) - 1)]
        ch = STATE_C[cur][1][b % 4]
        for m in ch:                                               # layer 1: the pad
            parts.append((arr(sect("violin" if m >= 48 else "cello", m + 12, bar * 0.98, 3, b + m)), t0, -10.0))
        if li >= 2:                                                # layer 2: bass on beats 1 and 3 (eighths in combat)
            step = beat / 2 if cur == "combat" else 2 * beat
            t = t0
            while t < t0 + bar - 1e-6:
                parts.append((arr(bass(ch[0], step * 0.8)), t, -3.0))
                t += step
        if li >= 3:                                                # layer 3: drums
            for k in range(4):
                parts.append((arr(P40.kick()), t0 + k * beat if (k % 2 == 0 or cur == "combat") else t0 + k * beat + beat / 2, -6.0))
                if k % 2 == 1:
                    parts.append((arr(P40.snare(b + k)), t0 + k * beat, -8.0))
        if li >= 4:                                                # layer 4: the motive in the brass
            for m, a, d in MOTIVE:
                parts.append((arr(inst("trumpet f" if cur == "combat" else "horn", m + (0 if cur != "danger" else -1), d * beat * 0.95)), t0 + a * beat, -4.0))
    for s in sw[1:]:                                               # stingers at the moment of each change
        if s["stinger"]:
            ch = STATE_C[s["state"]][1][0]
            for m in ch:
                parts.append((arr(inst("trumpet f" if s["state"] != "danger" else "horn", m + 24, 0.5)), s["event"], -5.0))
    return place(parts, game.length + 1.5)


def compute_game() -> dict:
    game = S.simulate(3, 48.0)
    score = S.Score(120.0)
    plan = S.adapt(game, score, "bar")
    c = render_game(game, plan, score)
    return {"times": game.times, "states": game.states, "intensity": game.intensity.tolist()[::2], "length": game.length,
            "switches": plan["switches"], "layers": plan["layers"][::2], "grid": 0.2, "bpm": score.bpm, "bar": score.bar,
            "mean_delay": plan["mean_delay"], "max_delay": plan["max_delay"],
            "clips": {"play": save_synth("game.play", c, detail="48 seconds of a simulated game scored adaptively: segments by state, layers by intensity, stingers at each change; the additive orchestra, Part 7's piano and bass, Part 40's drums")}}


def compute_switch() -> dict:
    """One change, explore to combat at 5.3 s, heard switching at once and at the next bar (with a stinger)."""
    score = S.Score(120.0)
    clips, out = [], {}
    for name, q, sting in (("at once", "now", False), ("at the bar, with a stinger", "bar", True)):
        g = S.Game(times=[0.0, 5.3], states=["explore", "combat"], intensity=None, length=10.0)
        grid = np.arange(0, 10.0, 0.1)
        g.intensity = np.where(grid < 5.3, 0.45, 1.0)
        plan = S.adapt(g, score, q, stingers=sting)
        clips.append(render_game(g, plan, score))
        out[name] = {"switch": plan["switches"][1]["switch"], "delay": plan["switches"][1]["delay"]}
    c = concat(clips, gap=1.0, names=list(out))
    return {"cases": out, "event": 5.3, "bar": score.bar, "starts": {k: float(c.events[k]) for k in out},
            "clips": {"two": save_synth("switch.two", c, detail="exploring turns to combat at 5.3 s: the music switching at once, then at the next bar line with a stinger at the moment of the change; the additive orchestra, piano, bass, drums")}}


def compute_quantise() -> dict:
    out = {}
    rng = np.random.default_rng(0)
    score = S.Score(120.0)
    for q in ("now", "beat", "bar", "phrase"):
        delays = []
        for seed in range(200):
            g = S.simulate(seed, 120.0)
            delays += [s["delay"] for s in S.adapt(g, score, q)["switches"][1:]]
        unit = {"now": 0.0, "beat": score.beat, "bar": score.bar, "phrase": score.bar * score.segment_bars}[q]
        out[q] = {"mean": float(np.mean(delays)), "max": float(np.max(delays)), "expected": S.expected_delay(unit), "n": len(delays)}
    return {"quantise": out, "bpm": 120.0}


def compute_duty() -> dict:
    chip = S.Chip()
    clips = [Clip(chip.pulse(440.0, 1.2, d, 12), SR).fade(0.005, 0.05) for d in (0.5, 0.25, 0.125)]
    c = concat(clips, gap=0.5, names=["50", "25", "12.5"])
    return {"duties": [0.5, 0.25, 0.125], "harmonics": {str(d): S.pulse_harmonics(d, 12).tolist() for d in (0.5, 0.25, 0.125)},
            "starts": {k: float(c.events[k]) for k in ("50", "25", "12.5")},
            "clips": {"three": save_synth("duty.three", c, detail="A4 on the chip's pulse channel at duty cycles of 50, 25 and 12.5 per cent")}}


def compute_noise() -> dict:
    """The noise channel: a 15-bit shift register in its long mode (hiss) and short mode (a metallic, pitched buzz)."""
    chip = S.Chip()
    clips = [Clip(chip.noise(1.0, period=4, vol=11, short=False), SR).fade(0.005, 0.05), Clip(chip.noise(1.0, period=4, vol=11, short=True), SR).fade(0.005, 0.05),
             Clip(np.concatenate([chip.noise(0.15, period=2, vol=12, decay=0.04), np.zeros(int(0.1 * SR)), chip.noise(0.15, period=8, vol=12, decay=0.06),
                                  np.zeros(int(0.1 * SR)), chip.noise(0.3, period=16, vol=12, decay=0.12)]), SR)]
    c = concat(clips, gap=0.5, names=["long", "short", "drums"])
    return {"starts": {k: float(c.events[k]) for k in ("long", "short", "drums")},
            "clips": {"three": save_synth("noise.three", c, detail="the chip's noise channel: the shift register's long mode, its short mode, then three noise drums of different periods and decays")}}


def compute_arp() -> dict:
    chip = S.Chip()
    f = [O.hz(m) for m in (60, 64, 67)]
    three = chip.pulse(f[0], 1.6, 0.5, 9) + chip.pulse(f[1], 1.6, 0.25, 9) + chip.triangle(f[2] / 2, 1.6)
    one = chip.arpeggio(f, 1.6, 0.25, 12, rate=60.0)
    c = concat([Clip(three, SR).fade(0.005, 0.05), Clip(one, SR).fade(0.005, 0.05)], gap=0.7, names=["first", "second"])
    return {"chord": [60, 64, 67], "rate": 60.0, "answer": "second", "starts": {k: float(c.events[k]) for k in ("first", "second")},
            "clips": {"quiz": save_synth("arp.quiz", c, detail="a C major chord on the chip: two pulse channels and the triangle at once, then one pulse channel cycling the three notes 60 times a second")}}


def chip_tune(beat=0.3, phrases=None):
    chip = S.Chip()
    ev = T.events(beat, phrases)
    end = ev[-1]["t"] + ev[-1]["dur"] + 0.4
    n = int(end * SR)
    y = np.zeros(n)
    major = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
    chords = {0: (60, 64, 67), 5: (65, 69, 72), 7: (67, 71, 74)}
    for e in ev:
        m = 72 + major[e["degree"]]
        s = chip.pulse(O.hz(m), e["dur"] * 0.85, 0.5, 11)
        i0 = int(e["t"] * SR)
        y[i0:i0 + len(s)] += s[: n - i0]
        root = {1: 0, 3: 0, 5: 0, 4: 5, 6: 5, 2: 7, 7: 7}[e["degree"]]
        ch = chords[root]
        a = chip.arpeggio([O.hz(x) for x in ch], e["dur"], 0.25, 5)
        y[i0:i0 + len(a)] += a[: n - i0]
        b = chip.triangle(O.hz(36 + root), e["dur"] * 0.9)
        y[i0:i0 + len(b)] += b[: n - i0]
        if e["i"] % 2 == 0:
            d = chip.noise(0.08, period=4, vol=8, decay=0.03)
            y[i0:i0 + len(d)] += d[: n - i0]
    return Clip(y / np.abs(y).max() * 0.9, SR)


def compute_chip() -> dict:
    c = chip_tune(0.3, [0, 1])
    return {"seconds": c.duration, "clips": {"tune": save_synth("chip.tune", c, detail="the Tune's first two phrases on the chip: melody on a pulse, chords as arpeggios, bass on the triangle, noise drums")}}


def compute_tune() -> dict:
    # 1. the Tune as a cue whose last note lands on a hit point at 9.0 s: the tempo that makes 14 beats fill it
    hit = 9.0
    beat = (hit - 0.5) / 14.0
    ev = T.events(beat, [0, 1])
    major = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
    p = []
    for e in ev:
        p.append((arr(inst("flute", 72 + major[e["degree"]], e["dur"] * 0.95 if e["i"] < 13 else 1.6)), 0.5 + e["t"], -2.0))
    for i, ch in enumerate([(48, 55, 64), (53, 57, 65), (48, 55, 64), (53, 57, 65), (48, 55, 64), (55, 59, 62), (48, 55, 64)]):
        for m in ch:
            p.append((arr(sect("violin" if m >= 55 else "cello", m, 2 * beat, 3, m + i)), 0.5 + 2 * beat * i, -9.0))
    p.append((arr(P40.kick()), hit, 0.0))
    for m in (48, 55, 60, 64, 67, 72):
        p.append((arr(inst("horn" if m < 60 else "trumpet f", m, 1.6)), hit, -3.0))
    cue = place(p, hit + 2.0)
    # 2. the Tune's first phrase as a leitmotif in three moods
    first = [(major[d], a, b) for (d, b), a in zip(T.PHRASES[0], np.cumsum([0] + [b for _, b in T.PHRASES[0]][:-1]))]
    moods = []
    p = [(arr(inst("horn", 60 + m, b * 0.33 * 0.95)), a * 0.33, 0.0) for m, a, b in first]
    p += [(arr(sect("cello", 48, 8 * 0.33, 4, 1)), 0.0, -8.0)]
    moods.append(place(p, 8 * 0.33 + 0.6))
    p = [(arr(inst("flute", 72 + m, b * 0.6 * 0.97)), a * 0.6, 0.0) for m, a, b in first]
    p += [(arr(sect("violin", x, 8 * 0.6, 4, x)), 0.0, -12.0) for x in (53, 57, 60)]
    moods.append(place(p, 8 * 0.6 + 0.6))
    minor = {0: 0, 7: 6, 9: 8}
    p = [(arr(sect("cello", 36 + minor.get(m, m), b * 0.5 * 0.97, 6, int(a * 10))), a * 0.5, 0.0) for m, a, b in first]
    p += [(arr(P40.k808(1.0)), 0.0, -8.0)]
    moods.append(place(p, 8 * 0.5 + 1.0))
    mo = concat(moods, gap=0.5, names=["heroic", "tender", "menacing"])
    # 3. an adaptive loop: the first two phrases looped while the intensity rises; a layer added each pass
    loop = []
    lb = 0.3
    for k in range(4):
        p = []
        for e in T.events(lb, [0, 1]):
            if k >= 3:
                p.append((arr(inst("trumpet f", 72 + major[e["degree"]], e["dur"] * 0.9)), e["t"], -4.0))
            p.append((arr(piano(72 + major[e["degree"]], e["dur"] * 0.9, 0.7)), e["t"], -2.0))
            if k >= 1 and e["i"] % 2 == 0:
                p.append((arr(bass(48 + (0 if e["degree"] in (1, 3, 5) else 7), lb * 1.6)), e["t"], -2.0))
            if k >= 2:
                p.append((arr(P40.hat()), e["t"], -10.0))
                if e["i"] % 4 == 2:
                    p.append((arr(P40.snare(e["i"])), e["t"], -8.0))
                if e["i"] % 4 == 0:
                    p.append((arr(P40.kick()), e["t"], -6.0))
        loop.append(place(p, 16 * lb))
    lo = concat(loop, gap=0.0, names=["pass1", "pass2", "pass3", "pass4"])
    c = concat([cue, mo, lo], gap=1.0, names=["cue", "moods", "loop"])
    return {"hit": hit, "beat": beat, "bpm": 60.0 / beat, "frames_per_beat": S.frames(beat), "click": list(S.click(60.0 / beat)[:2]),
            "seconds": c.duration, "starts": {k: float(c.events[k]) for k in ("cue", "moods", "loop")},
            "mood_starts": {k: float(c.events["moods"] + mo.events[k]) for k in ("heroic", "tender", "menacing")},
            "pass_starts": [float(c.events["loop"] + lo.events[f"pass{k}"]) for k in range(1, 5)],
            "clips": {"variation44": save_synth("tune.variation44", c, detail="the Tune as a cue landing on a hit point, as a leitmotif in three moods, and as an adaptive loop gaining a layer each pass; the additive orchestra, Part 7's piano and bass, Part 40's drums")}}


def compute_variation() -> dict:
    t = load("tune")
    w, e = t["click"]
    return {"part": 44, "title": "as a cue on a hit point, as a leitmotif in three moods, as an adaptive loop", "seconds": round(t["seconds"], 1),
            "measure": f"the cue's 14 beats at {t['bpm']:.1f} bpm (a {w}-{e} click) land its last note on the 9.0 s hit; the loop adds a layer each pass",
            "clip": "tune.variation44"}


def compute_signoff() -> dict:
    """The part's last sound: the opening of its Variation, under the next part's title."""
    load("variation")
    return signoff(CLIPS, "tune.variation44", 44)


ITEMS = {"scene": compute_scene, "hook": compute_hook, "three": compute_three, "sync": compute_sync, "motif": compute_motif,
         "harmony": compute_harmony, "mix": compute_mix, "game": compute_game, "switch": compute_switch, "quantise": compute_quantise, "duty": compute_duty, "noise": compute_noise,
         "arp": compute_arp, "chip": compute_chip, "tune": compute_tune, "variation": compute_variation,
         "signoff": compute_signoff}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
