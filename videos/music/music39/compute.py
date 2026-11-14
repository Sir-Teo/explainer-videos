"""Precompute everything numerical, and every sound, in Part 39 of *Music, Built* ("Changes").

    python -m videos.music.music39.compute              # everything missing (under a minute)
    python -m videos.music.music39.compute --force improv

Numbers are cached in ``.cache/music39/<name>.json``, sounds in ``.cache/music39/audio/``.  The tools are Monochord's
(``explainer/music/monochord/changes.py`` and Part 38's ``blues.py``); the instruments are Part 38's: Part 7's piano,
the retuned plucked string for bass, a modal ride cymbal, filtered-noise hi-hat, and additive horns (labelled
synthesized).  Chord progressions of well-known tunes are used as lead sheets give them; no melody of theirs is played.
Every line, head and voicing heard is ours or the program's.

Items:
    hook        Giant Steps' sixteen bars of changes, comped (an ear question: how many keys?)
    fast        the improviser over Giant Steps' changes at the original tempo
    formula     a ii-V-I figure of ours in three keys
    scales      five chords on C, each with its chord scale played over it
    echo        a toy free duo: figures answered a fourth higher and backwards, with no changes
    contrafact  rhythm changes' A section: a head of ours, then the improviser
    bebop       descending eighths over C7: the mixolydian, then the bebop scale
    enclose     a target reached three ways: plain, enclosed, double-chromatic
    avoid       a held F over Cmaj7, then a held E
    modal       a modal vamp of ours in D and E-flat dorian with quartal voicings, and the improviser over it
    thirds      ii-V-I in C, then Coltrane's substitute through A-flat and E
    reharm      a phrase of ours harmonised three ways
    improv      the improviser and a random line over the jazz blues (an ear question: which is which?)
    tune        Variation 39: the Tune as a bebop head, an improvised chorus, its opening through three keys a third apart
    variation   the Variations ledger, row 39
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import blues as BL
from explainer.music.monochord import changes as CH
from explainer.music.monochord import melody as M
from explainer.music.monochord.partkit import saver
from videos.music.music38 import compute as P38

CACHE = Cache("music39")
CLIPS = ClipStore("music39")
load = CACHE.load
LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
save_synth = saver(CLIPS, LEVEL, kind="synthesized")
arr = P38.arr
piano, bass, ride, hat, horn = P38.piano, P38.bass, P38.ride, P38.hat, P38.horn


def full(sym):
    """Lead-sheet triads (B, Eb) as major sevenths, for the chord tools."""
    return sym if any(sym.endswith(q) for q in ("7", "m", "6", "dim7", "m7b5")) else sym + "maj7"


def fullchanges(changes):
    return [[full(s) for s in bar] for bar in changes]


def comp(parts, changes, bpm, start=0.0, gain=0.0, ride_on=True, walk=False, rhythm="charleston"):
    """Bass, ride and hi-hat, and shell voicings (guide tones) on the piano, from bars of chord symbols."""
    ch = fullchanges(changes)
    beat = 60.0 / bpm
    seq = BL.beats_of(ch)
    nb = len(ch)
    gt = BL.guide_tones(seq, lo=55, hi=70)
    if walk:
        wb = BL.walking_bass(ch)
        for i in range(nb * 4):
            parts.append((arr(bass(wb[i], beat * 0.95)), start + i * beat, -2.0 + gain))
    else:
        for i in range(nb * 4):
            if i == 0 or seq[i] != seq[i - 1] or i % 2 == 0:
                r = BL.chord(seq[i])["root"]
                parts.append((arr(bass(36 + r if r < 8 else 24 + r, beat * 1.9)), start + i * beat, -2.0 + gain))
    if ride_on:
        for b in range(nb):
            ts = BL.swing_times(P38.RIDE_PATTERN, bpm) + start + b * 4 * beat
            for j, t in enumerate(ts):
                parts.append((arr(ride(P38.RIDE_PATTERN[j] % 4 == 2)), t, -17.0 + gain))
            for k in (1, 3):
                parts.append((arr(hat()), start + (b * 4 + k) * beat, -19.0 + gain))
    for i in range(nb * 4):
        newchord = i == 0 or seq[i] != seq[i - 1]
        if newchord:
            t = start + i * beat
            for m in (gt["upper"][i], gt["lower"][i]):
                parts.append((arr(piano(m, beat * 1.6, 0.7)), t, -8.0 + gain))
    return gt


def line_parts(parts, notes, bpm, start=0.0, inst="sax", gain=0.0, ratio=None):
    """Eighth-note lines [(key, eighth)] swung by Part 38's model."""
    if not notes:
        return
    beat = 60.0 / bpm
    es = [e for _, e in notes]
    ts = BL.swing_times(es, bpm, ratio) + start
    for k, ((m, e), t) in enumerate(zip(notes, ts)):
        if k + 1 < len(notes) and notes[k + 1][1] == e + 1:
            dur = ts[k + 1] - t
        else:
            dur = beat * 0.5
        if inst == "piano":
            parts.append((arr(piano(m, max(dur, 0.1) * 1.05, 1.0)), t, gain))
        else:
            parts.append((arr(horn(m, max(dur, 0.1) * 0.95, inst)), t, gain))


def bounce(parts, end):
    return Clip(mix(parts, duration=end).y, SR).at_level(LEVEL)


def rows(notes):
    return [[int(m), int(e)] for m, e in notes]


# ---------------------------------------------------------------------------------------------------------- items
def compute_hook() -> dict:
    bpm = 150
    parts = []
    comp(parts, CH.GIANT_STEPS, bpm)
    kc = CH.key_centres(fullchanges(CH.GIANT_STEPS))
    c = bounce(parts, 16 * 4 * 60 / bpm + 1.5)
    return {"bpm": bpm, "changes": CH.GIANT_STEPS, "chords": len(CH.symbols(CH.GIANT_STEPS)), "keys": kc, "answer": 3,
            "original_bpm": 286,
            "clips": {"giant": save("hook.giant", c, detail="the sixteen bars of changes of Giant Steps (Coltrane, 1959), as lead sheets give them, comped at 150 beats a minute: guide tones on piano, bass and ride; no melody")}}


def compute_fast() -> dict:
    """The improviser over Giant Steps' changes at the original tempo (about 286 beats a minute)."""
    bpm = 286
    ch = fullchanges(CH.GIANT_STEPS)
    line = CH.improvise(ch, seed=5, rest_prob=0.1)
    parts = []
    comp(parts, CH.GIANT_STEPS, bpm)
    line_parts(parts, line, bpm, 0.0, "piano", -1.0)
    c = bounce(parts, 16 * 4 * 60 / bpm + 1.2)
    return {"bpm": bpm, "line": rows(line), "judge": CH.judge(line, ch), "changes": CH.GIANT_STEPS,
            "clips": {"giant": save("fast.giant", c, detail="the program's line over the changes of Giant Steps at 286 beats a minute, on Part 7's piano, with comping, bass and ride; no melody of the tune")}}


FORMULA = [(77, 0), (76, 1), (74, 2), (72, 3), (71, 4), (74, 5), (77, 6), (81, 7), (79, 8), (77, 9), (76, 10), (74, 11), (72, 12)]   # ours: a ii-V-I figure in C


def compute_formula() -> dict:
    bpm = 150
    beat = 60.0 / bpm
    parts, starts, t = [], {}, 0.0
    keys = [("C", 0), ("F", 5), ("Bb", -2)]
    for name, k in keys:
        starts[name] = t
        ch = [[BL.transpose("Dm7", k % 12), BL.transpose("G7", k % 12)], [BL.transpose("Cmaj7", k % 12)]]
        comp(parts, ch, bpm, start=t)
        line_parts(parts, [(m + k, e) for m, e in FORMULA], bpm, t, "sax", -1.0)
        t += 8 * beat + 0.6
    c = bounce(parts, t + 0.8)
    return {"bpm": bpm, "formula": rows(FORMULA), "keys": [k for k, _ in keys], "shifts": [s for _, s in keys], "starts": starts,
            "clips": {"keys": save_synth("formula.keys", c, detail="a ii-V-I figure of ours in C, then F, then B-flat, as players practise formulas through the keys; an additive saxophone over piano, bass and ride")}}


def compute_scales() -> dict:
    bpm = 120
    beat = 60.0 / bpm
    parts, starts, t = [], {}, 0.0
    order = ["Cmaj7", "C7", "Cm7", "Cm7b5", "Cdim7"]
    for s_ in order:
        starts[s_] = t
        cs = CH.chord_scale(s_)
        c = BL.chord(s_)
        for m in (48,) + tuple(55 + (p - 55) % 12 for p in c["pcs"][1:]):
            parts.append((arr(piano(m, 4.2 * beat, 0.6)), t, -8.0))
        sc = sorted(60 + (p - 60) % 12 for p in cs["scale"]) + [72]
        for k, m in enumerate(sc):
            parts.append((arr(piano(m, beat * 0.5, 0.9)), t + k * beat * 0.5, -1.0))
        t += (len(sc) * 0.5 + 1.0) * beat + 0.4
    cl = bounce(parts, t + 0.6)
    return {"bpm": bpm, "order": order, "starts": starts,
            "clips": {"five": save("scales.five", cl, detail="five chords on C, each held while its chord scale is played up over it: ionian, mixolydian, dorian, locrian, whole-half; Part 7's piano")}}


def compute_echo() -> dict:
    """Free playing, as a toy: no changes; a saxophone plays a short figure (random steps from all twelve notes), then
    a piano answers with the same figure a fourth higher and backwards, and the next figure starts from where the answer
    ended.  It listens, in the crudest way: the one thing the improviser of chapter 8 cannot do."""
    bpm = 150
    rng = np.random.default_rng(8)
    calls, answers = [], []
    m = 67
    e = 0
    for k in range(5):
        n = int(rng.integers(4, 7))
        fig = []
        for j in range(n):
            m = int(np.clip(m + rng.choice([-3, -2, -1, 1, 2, 3, 5, -5]), 58, 80))
            fig.append((m, e + j))
        calls.append(fig)
        e += n + 1
        ans = [(p + 5, e + j) for j, (p, _) in enumerate(reversed(fig))]
        answers.append(ans)
        e += n + 2
        m = ans[-1][0] - 5
    parts = []
    for fig in calls:
        line_parts(parts, fig, bpm, 0.0, "sax", -1.0)
    for ans in answers:
        line_parts(parts, ans, bpm, 0.0, "piano", 0.0)
    beat = 60.0 / bpm
    for b in range(0, e // 2 + 2, 2):
        parts.append((arr(ride(False)), b * beat, -18.0))
    c = bounce(parts, e * beat / 2 + 1.5)
    return {"bpm": bpm, "calls": [rows(f) for f in calls], "answers": [rows(a) for a in answers], "eighths": e,
            "clips": {"duo": save_synth("echo.duo", c, detail="a toy free duo of ours: a saxophone's figures, each answered by the piano a fourth higher and backwards; no chord changes; additive saxophone, Part 7's piano, a ride cymbal")}}


HEAD_SEED = 3


def compute_contrafact() -> dict:
    bpm = 180
    ch = CH.RHYTHM_A
    head = CH.improvise(fullchanges(ch), seed=HEAD_SEED, rest_prob=0.1)
    solo = CH.improvise(fullchanges(ch), seed=HEAD_SEED + 1)
    parts = []
    comp(parts, ch + ch, bpm, walk=True)
    line_parts(parts, head, bpm, 0.0, "sax", -2.0)
    line_parts(parts, solo, bpm, 8 * 4 * 60 / bpm, "piano", -2.0)
    c = bounce(parts, 16 * 4 * 60 / bpm + 1.5)
    return {"bpm": bpm, "changes": ch, "head": rows(head), "solo": rows(solo), "judge_head": CH.judge(head, fullchanges(ch)),
            "clips": {"rhythm": save_synth("contrafact.rhythm", c, detail="the A section of rhythm changes (chords only): a line by the program on an additive saxophone, then on Part 7's piano, over bass, ride and comping")}}


def compute_bebop() -> dict:
    bpm = 132
    claim = CH.bebop_claim("C7")
    plain = CH.landing(CH.chord_scale("C7")["scale"], BL.chord("C7")["pcs"], 82, -1, 16)
    bebop = CH.landing(CH.bebop_scale("C7"), BL.chord("C7")["pcs"], 82, -1, 16)
    parts, starts, t = [], {}, 0.0
    for name, L in (("plain", plain), ("bebop", bebop)):
        starts[name] = t
        comp(parts, [["C7"], ["C7"]], bpm, start=t, walk=False)
        line_parts(parts, [(m, e) for e, m in enumerate(L["line"])], bpm, t, "piano", -1.0)
        t += 8 * 60 / bpm + 1.0
    c = bounce(parts, t + 0.5)
    major = CH.bebop_claim("C6")
    return {"bpm": bpm, "claim": claim, "major": {"bebop_all": major["bebop_all"], "scale": major["bebop_scale"]}, "plain": plain, "bebop": bebop,
            "starts": starts,
            "clips": {"two": save("bebop.two", c, detail="sixteen eighth notes down from B-flat over C7: the mixolydian scale, then the bebop scale; Part 7's piano with bass and ride")}}


def compute_enclose() -> dict:
    bpm = 120
    # Dm7 | G7 | Cmaj7: the line reaches E (the third of Cmaj7) on the downbeat of bar 3, three ways
    ways = {"plain": [(74, 0), (77, 2), (81, 4), (79, 6), (77, 8), (74, 10), (71, 12), (74, 14), (76, 16)],
            "enclosed": [(74, 0), (77, 2), (81, 4), (79, 6), (77, 8), (74, 10), (71, 12), (77, 14), (75, 15), (76, 16)],
            "double": [(74, 0), (77, 2), (81, 4), (79, 6), (77, 8), (74, 10), (78, 12), (77, 13), (74, 14), (75, 15), (76, 16)]}
    parts, starts, t = [], {}, 0.0
    for name, L in ways.items():
        starts[name] = t
        comp(parts, [["Dm7"], ["G7"], ["Cmaj7"]], bpm, start=t)
        line_parts(parts, L, bpm, t, "sax", -1.0)
        t += 12 * 60 / bpm + 0.8
    c = bounce(parts, t + 0.5)
    return {"bpm": bpm, "ways": {k: rows(v) for k, v in ways.items()}, "target": 76, "starts": starts,
            "clips": {"three": save_synth("enclose.three", c, detail="a line of ours reaching E on the downbeat of Cmaj7 three ways: plainly, by an enclosure (above, below, target) and by a double chromatic enclosure; an additive saxophone over piano, bass and ride")}}


def compute_avoid() -> dict:
    parts = []
    for k, (top, t0) in enumerate(((77, 0.0), (76, 3.6))):
        for m in (48, 55, 59, 64):
            parts.append((arr(piano(m, 2.5, 0.7)), t0, -4.0))
        parts.append((arr(horn(top, 2.6, "sax")), t0 + 0.3, -2.0))
    c = bounce(parts, 7.6)
    cs = CH.chord_scale("Cmaj7")
    return {"times": [0.0, 3.6], "tops": [77, 76], "scale": cs,
            "table": {s: CH.chord_scale(s) for s in ("Cmaj7", "C7", "Cm7", "Cm7b5", "Cdim7")},
            "clips": {"two": save_synth("avoid.two", c, detail="a held F over a C major seventh chord, then a held E: an additive saxophone over Part 7's piano")}}


QUARTAL = [52, 57, 62, 67, 71]                                     # E A D G B: fourths and a third, over D: ours


def compute_modal() -> dict:
    bpm = 140
    beat = 60.0 / bpm
    form = [["Dm7"]] * 8 + [["Ebm7"]] * 4 + [["Dm7"]] * 4
    parts = []
    for b, bar in enumerate(form):
        shift = 1 if bar[0] == "Ebm7" else 0
        t0 = b * 4 * beat
        if b % 2 == 0:
            for m in QUARTAL:
                parts.append((arr(piano(m + shift, beat * 2.5, 0.75)), t0 + 2.5 * beat, -8.0))
        parts.append((arr(bass(38 + shift, beat * 0.95)), t0, -1.0))
        parts.append((arr(bass(45 + shift, beat * 0.95)), t0 + 2 * beat, -3.0))
        ts = BL.swing_times(P38.RIDE_PATTERN, bpm) + t0
        for j, t in enumerate(ts):
            parts.append((arr(ride(P38.RIDE_PATTERN[j] % 4 == 2)), t, -17.0))
        for k in (1, 3):
            parts.append((arr(hat()), t0 + k * beat, -19.0))
    line = CH.improvise(form, seed=7, rest_prob=0.25)
    line_parts(parts, line, bpm, 0.0, "sax", -3.0)
    c = bounce(parts, len(form) * 4 * beat + 1.5)
    return {"bpm": bpm, "form": form, "quartal": QUARTAL, "line": rows(line), "judge": CH.judge(line, form),
            "so_what_bars": len(CH.SO_WHAT),
            "clips": {"vamp": save_synth("modal.vamp", c, detail="a modal vamp of ours: D dorian, E-flat dorian, D dorian, with quartal piano voicings, bass and ride, and the program's line on an additive saxophone")}}


def compute_thirds() -> dict:
    bpm = 120
    plain = [["Dm7"], ["G7"], ["Cmaj7"], ["Cmaj7"]]
    col = CH.coltrane("C")
    colt = [[col[0], col[1]], [col[2], col[3]], [col[4], col[5]], [col[6]]]
    parts, starts, t = [], {}, 0.0
    lines = {}
    for name, ch in (("plain", plain), ("coltrane", colt)):
        starts[name] = t
        for rep in range(2):
            comp(parts, ch, bpm, start=t + rep * 16 * 60 / bpm)
        L = CH.improvise(ch + ch, seed=11)
        lines[name] = rows(L)
        line_parts(parts, L, bpm, t, "piano", -2.0)
        t += 2 * 16 * 60 / bpm + 1.0
    c = bounce(parts, t + 0.5)
    kc = CH.key_centres(colt)
    return {"bpm": bpm, "plain": plain, "coltrane": colt, "starts": starts, "lines": lines, "keys": kc,
            "giant_keys": CH.key_centres(fullchanges(CH.GIANT_STEPS)),
            "clips": {"two": save("thirds.two", c, detail="ii-V-I in C, then Coltrane's substitute (Dm7 Eb7 Abmaj7 B7 Emaj7 G7 Cmaj7), each twice with the program's line on Part 7's piano, over bass and ride")}}


REHARM_PHRASE = [(72, 0, 2), (76, 2, 2), (79, 4, 2), (77, 6, 2), (76, 8, 2), (74, 10, 2), (72, 12, 4)]   # ours, in beats


def compute_reharm() -> dict:
    bpm = 96
    beat = 60.0 / bpm
    mel = [m for m, _, _ in REHARM_PHRASE]
    schemes = {k: CH.reharmonise(mel, k) for k in ("diatonic", "secondary", "tritone")}
    parts, starts, t = [], {}, 0.0
    for name, chords in schemes.items():
        starts[name] = t
        for (m, a, d), s in zip(REHARM_PHRASE, chords):
            parts.append((arr(horn(m, d * beat * 0.95, "sax")), t + a * beat, -1.0))
            c = BL.chord(s)
            r = c["root"]
            parts.append((arr(bass(36 + r if r < 8 else 24 + r, d * beat * 0.95)), t + a * beat, -2.0))
            for p in c["pcs"][1:]:
                parts.append((arr(piano(55 + (p - 55) % 12, d * beat * 0.9, 0.6)), t + a * beat, -9.0))
        t += 16 * beat + 1.0
    c = bounce(parts, t + 0.5)
    return {"bpm": bpm, "phrase": [list(x) for x in REHARM_PHRASE], "schemes": schemes, "starts": starts,
            "clips": {"three": save_synth("reharm.three", c, detail="a phrase of ours harmonised three ways: diatonic chords, with secondary dominants, with tritone substitutes; an additive saxophone over Part 7's piano and bass")}}


def compute_improv() -> dict:
    bpm = 160
    ch = BL.twelve_bar("C", "jazz")
    imp = CH.improvise(ch, seed=21)
    rnd = CH.random_line(ch, seed=21)
    order = {"A": "random", "B": "improviser"}
    parts, starts, t = [], {}, 0.0
    for key in ("A", "B"):
        starts[key] = t
        comp(parts, ch, bpm, start=t, walk=True)
        line_parts(parts, rnd if order[key] == "random" else imp, bpm, t, "piano", -1.0)
        t += 12 * 4 * 60 / bpm + 1.0
    c = bounce(parts, t + 0.5)
    stats = {}
    for name, f in (("improviser", lambda s: CH.improvise(ch, seed=s)), ("scale", lambda s: CH.random_line(ch, seed=s)),
                    ("chromatic", lambda s: CH.random_line(ch, seed=s, scale=False))):
        js = [CH.judge(f(s), ch) for s in range(50)]
        stats[name] = {k: float(np.mean([j[k] for j in js])) for k in ("on_beat_chord_tones", "guide_at_changes", "in_scale", "steps")}
    return {"bpm": bpm, "changes": ch, "improviser": rows(imp), "random": rows(rnd), "order": order, "answer": "B",
            "starts": starts, "judge_imp": CH.judge(imp, ch), "judge_rnd": CH.judge(rnd, ch), "stats": stats,
            "clips": {"pair": save("improv.pair", c, detail="two lines over a jazz blues in C on Part 7's piano: one with notes drawn at random from each chord's scale, one by the program's improviser; walking bass, ride and comping")}}


def tune_line(n=14, base=72):
    t = M.corpus([M.THE_TUNE])[0]
    out, a = [], 0.0
    for p, d in list(zip(t.pitches, t.beats))[:n]:
        out.append((base + p, a, float(d)))
        a += d
    return out


TUNE_CHANGES = [["Cmaj7"], ["Am7", "D7"], ["Dm7", "G7"], ["Em7", "A7"], ["Dm7", "G7"], ["Cmaj7", "A7"], ["Dm7", "G7"], ["Cmaj7"]]


def bebop_head(mel):
    """The Tune as a bebop head: each of its notes held on beat 1 or 3 (a Tune beat becomes two), and the eighths
    before the next note enclose it (a scale tone above, a semitone below)."""
    head = []
    for k, (m, a, d) in enumerate(mel):
        e = int(round(4 * a))
        span = int(round(4 * d))
        nxt = mel[k + 1][0] if k + 1 < len(mel) else None
        head.append((m, e))
        if nxt is None:
            continue
        if span >= 8:
            head += [(m + 2, e + 4), (m, e + 5)]
        head += [(nxt + (2 if nxt % 12 in (0, 2, 5, 7, 9) else 1), e + span - 2), (nxt - 1, e + span - 1)]
    return sorted(head, key=lambda x: x[1])


THIRD_CYCLE = [["Cmaj7", "Eb7"], ["Abmaj7", "B7"], ["Emaj7", "G7"], ["Cmaj7"]] * 2


def compute_tune() -> dict:
    bpm = 168
    beat = 60.0 / bpm
    mel = tune_line(14, 72)
    head = bebop_head(mel)
    parts = []
    comp(parts, TUNE_CHANGES, bpm, walk=True)
    line_parts(parts, head, bpm, 0.0, "sax", -1.0)
    # 2. an improvised chorus over the same changes, twice through
    solo = CH.improvise(TUNE_CHANGES + TUNE_CHANGES, seed=39)
    t1 = 8 * 4 * beat
    comp(parts, TUNE_CHANGES + TUNE_CHANGES, bpm, start=t1, walk=True)
    line_parts(parts, solo, bpm, t1, "piano", -1.0)
    # 3. the Tune's opening (do do sol sol, then la la sol) carried through three tonics a major third apart
    t2 = t1 + 16 * 4 * beat
    comp(parts, THIRD_CYCLE, bpm, start=t2, walk=True)
    cyc = []
    for rep in range(2):
        b0 = rep * 4 * 8                                        # eighths
        for bar, tonic in enumerate((72, 68, 76)):
            e = b0 + bar * 8
            cyc += [(tonic, e), (tonic, e + 1), (tonic + 7, e + 2), (tonic + 7, e + 3)]
        e = b0 + 3 * 8
        cyc += [(81, e), (81, e + 2), (79, e + 4)] if rep == 0 else [(77, e), (76, e + 2), (72, e + 4)]
    line_parts(parts, cyc, bpm, t2, "sax", -1.0)
    end = t2 + 8 * 4 * beat + 1.5
    c = Clip(mix(parts, duration=end).y, SR).at_level(LEVEL)
    j_solo = CH.judge(solo, fullchanges(TUNE_CHANGES + TUNE_CHANGES))
    j_head = CH.judge(head, fullchanges(TUNE_CHANGES))
    return {"bpm": bpm, "melody": [list(x) for x in mel], "head": rows(head), "solo": rows(solo), "changes": TUNE_CHANGES,
            "third": THIRD_CYCLE, "cycle_line": rows(cyc), "keys": CH.key_centres(THIRD_CYCLE),
            "starts": {"head": 0.0, "solo": t1, "thirds": t2}, "judge_solo": j_solo, "judge_head": j_head, "seconds": c.duration,
            "clips": {"variation": save_synth("tune.variation39", c, detail="the Tune as a bebop head on an additive saxophone, an improvised chorus by the program on Part 7's piano, then the Tune's opening carried through C, A-flat and E over third-cycle changes; bass, ride and comping")}}


def compute_variation() -> dict:
    t = load("tune")
    j = t["judge_solo"]
    return {"part": 39, "title": "as a bebop head, with an improvised chorus, then through three keys a major third apart", "seconds": round(t["seconds"], 1),
            "measure": f"the program's chorus: {round(100 * j['on_beat_chord_tones'])}% of beats on chord tones, guide tones at {round(100 * j['guide_at_changes'])}% of changes",
            "clip": "tune.variation39"}


ITEMS = {"hook": compute_hook, "fast": compute_fast, "echo": compute_echo, "formula": compute_formula, "scales": compute_scales, "contrafact": compute_contrafact, "bebop": compute_bebop, "enclose": compute_enclose, "avoid": compute_avoid,
         "modal": compute_modal, "thirds": compute_thirds, "reharm": compute_reharm, "improv": compute_improv, "tune": compute_tune,
         "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
