"""Precompute everything numerical, and every sound, in Part 19 of *Music, Built* ("Chromatic Harmony").

    python -m videos.music.music19.compute              # everything missing (a minute or two)
    python -m videos.music.music19.compute --force trapdoor

Numbers are cached in ``.cache/music19/<name>.json``, sounds in ``.cache/music19/audio/``.  Chromatic harmony is
Monochord's (``explainer/music/monochord/chromatic.py``); applied dominants are counted in Part 17's chorales; every
example is played on Part 7's piano (a struck stiff string through a soundboard), and the commas on pure tones.

Items:
    hook        the opening of Tristan und Isolde (1859), twice, a minor third apart
    applied     applied dominants: a chain of them in C, heard; how often Bach uses them
    mixture     chords borrowed from the minor, heard
    neapolitan  the Neapolitan sixth, heard
    sixths      the Italian, French and German sixths, each resolving to the dominant
    dim7        one diminished seventh resolved four ways
    trapdoor    a German sixth that goes home, and the same chord that goes to D flat
    comma       pure thirds that do not close the octave, heard against equal temperament
    mediants    chromatic mediants and the hexatonic cycle
    paths       the fewest steps from C major to every key, by pivots alone and with chromatic chords
    tension     Lerdahl's chord distance along three progressions
    tristan     four readings of the Tristan chord; its voice leading
    tune        Variation 19: the Tune with mixture, with the Neapolitan, and through a diminished-seventh trapdoor
    variation   the Variations ledger, row 19
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import chorales as BC
from explainer.music.monochord import chords as CH
from explainer.music.monochord import chromatic as X
from explainer.music.monochord import fourpart as F
from explainer.music.monochord import melody as M
from explainer.music.monochord import tuning as TU
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.partkit import organ_tone, saver
from explainer.music.monochord.physics.string import String

CACHE = Cache("music19")
CLIPS = ClipStore("music19")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
BOARD = STR.soundboard()
C4 = 261.6255653005986
_NOTES: dict = {}
BEAT = 0.75


def hz(m: float) -> float:
    return 440.0 * 2.0 ** ((m - 69) / 12.0)


def piano(m: float, seconds: float, velocity: float = 1.4) -> Clip:
    key = (round(m, 3), round(seconds, 3), velocity)
    if key not in _NOTES:
        f = hz(m)
        y = BOARD.play(STR.struck(String.tuned(f, L=0.62 * (C4 / f) ** 0.8, mu=6.34e-3, kappa=1.25, sigma0=0.6, sigma1=3.3e-4), velocity=velocity, seconds=seconds + 0.3))
        _NOTES[key] = Clip(np.asarray(y, dtype=float)).fade(0.001, 0.2).at_level(LEVEL)
    return _NOTES[key]


def play(events, tail: float = 1.4) -> Clip:
    """Events (key number, start beat, beats[, gain dB]); one event mark per distinct start (``t{k}``)."""
    placed, ev, starts = [], {}, sorted({e[1] for e in events})
    for e in events:
        m, a, d = e[:3]
        g = e[3] if len(e) > 3 else 0.0
        placed.append((piano(m, d * BEAT), a * BEAT, g))
    for k, a in enumerate(starts):
        ev[f"t{k}"] = a * BEAT
    end = max(a + d for _, a, d, *_ in events) * BEAT
    ev["end"] = end
    return Clip(mix(placed, duration=end + tail).y, SR, ev, [])


def chords_events(chords, beats: float = 2.0, start: float = 0.0, melody_gain: float = 0.0) -> list:
    out = []
    for k, ch in enumerate(chords):
        for j, m in enumerate(sorted(ch, reverse=True)):
            out.append((int(m), start + k * beats, beats, melody_gain if j == 0 else -3.0))
    return out


def seq(clips: dict) -> Clip:
    return concat([c.at_level(LEVEL) for c in clips.values()], gap=1.0, names=list(clips))


def voice(prev, pcs, bass, top=None, lo=55, hi=81, full: bool = False):
    """Upper voices for a chord over a bass by the shortest way from ``prev`` (and with ``top`` on top if given).
    Every note of the chord is sounded if possible; a seventh chord may otherwise leave out its fifth (never with
    ``full``)."""
    keys = [m for m in range(max(lo, bass + 1), hi + 1) if m % 12 in pcs]
    needs = [set(pcs)] if (full or len(pcs) == 3) else [set(pcs), {pcs[0], pcs[1], pcs[3]}]
    for need in needs:
        best, bc = None, 1e9
        for t in keys:
            for a in keys:
                if a <= t or a - t > 12:
                    continue
                for s in keys:
                    if s <= a or s - a > 12 or (top is not None and s != top):
                        continue
                    if not {s % 12, a % 12, t % 12, bass % 12} >= need:
                        continue
                    cand = (s, a, t, bass)
                    c = sum(abs(x - y) for x, y in zip(cand[:3], prev[:3])) + (50 * len(F.parallels(prev, cand)) if len(prev) == 4 else 0)
                    if c < bc:
                        best, bc = cand, c
        if best is not None:
            return best
    raise ValueError(f"no voicing for {pcs} over {bass}")


def realize(plan, start=(72, 67, 64, 48)) -> list[tuple]:
    """``plan``: (pitch classes, bass key number[, top key number]) per chord."""
    out, prev = [], start
    for p in plan:
        pcs, bass = p[0], p[1]
        top = p[2] if len(p) > 2 else None
        ch = voice(prev, list(pcs), bass, top)
        out.append(ch)
        prev = ch
    return out


def rows(chords) -> list:
    return [[int(x) for x in c] for c in chords]


# ---------------------------------------------------------------------------
def compute_hook() -> dict:
    """The prelude's first phrase, simplified to its harmony: a lone A (cellos), the Tristan chord with the oboe's
    G sharp rising to A, A sharp and B, the resolution to E7; then the same a minor third higher."""
    def phrase(t, start):
        lone = [(57 + t, start, 1.5, 2.0)]
        chord = [(53 + t, start + 1.5, 3.0), (59 + t, start + 1.5, 3.0), (63 + t, start + 1.5, 3.0)]
        oboe = [(68 + t, start + 1.5, 2.0, 2.0), (69 + t, start + 3.5, 0.5, 2.0), (70 + t, start + 4.0, 0.5, 2.0), (71 + t, start + 4.5, 3.0, 2.0)]
        res = [(52 + t, start + 4.5, 3.0), (56 + t, start + 4.5, 3.0), (62 + t, start + 4.5, 3.0)]
        return lone + chord + oboe + res
    a = play(phrase(0, 0.0))
    b = play(phrase(3, 0.0))
    s = concat([a.at_level(LEVEL), b.at_level(LEVEL)], gap=1.6, names=["first", "second"])
    return {"first": {"tristan": [53, 59, 63, 68], "resolution": [52, 56, 62, 71]}, "second": {"tristan": [56, 62, 66, 71], "resolution": [55, 59, 65, 74]},
            "starts": {k: float(s.events[k]) for k in ("first", "second")},
            "chord_at": [float(s.events["first.t1"]), float(s.events["second.t1"])], "resolve_at": [float(s.events["first.t4"]), float(s.events["second.t4"])],
            "clips": {"tristan": save("hook.tristan", s, level=None, detail="the opening of Tristan und Isolde (Wagner, 1859), reduced to its harmony: Part 7's piano")}}


def compute_applied() -> dict:
    # a chain of applied dominants in C: I, V7/IV, IV, V7/V, V, V7/vi, vi, V7/ii, ii, V7, I
    plan = [((0, 4, 7), 48), (X.applied_dominant(5), 48), ((5, 9, 0), 41), (X.applied_dominant(7), 50), ((7, 11, 2), 43),
            (X.applied_dominant(9), 52), ((9, 0, 4), 45), (X.applied_dominant(2), 45), ((2, 5, 9), 50), ((7, 11, 2, 5), 43), ((0, 4, 7), 48)]
    chords = realize(plan)
    c = play(chords_events(chords, beats=1.5))
    s = concat([c.at_level(LEVEL)], gap=0.0, names=["chain"])
    names = ["I", "V7/IV", "IV", "V7/V", "V", "V7/vi", "vi", "V7/ii", "ii", "V7", "I"]
    # how often Bach's major chorales put an applied dominant on a beat: a major chord or dominant seventh on 1, 2, 3 or 6
    b = BC.load()
    hits, beats = Counter(), 0
    for ch in b:
        if ch.mode != "major":
            continue
        for x in F.beat_labels(ch):
            beats += 1
            lab = x["label"]
            if lab and lab[0] in (0, 2, 4, 9) and lab[1] in ("major", "7"):
                if lab[0] == 0 and lab[1] == "major":
                    continue
                hits[F.roman((lab[0], lab[1], 0), "major")] += 1
    return {"chords": rows(chords), "names": names, "times": [float(s.events[f"chain.t{k}"]) for k in range(len(chords))],
            "bach": dict(hits), "bach_beats": beats, "bach_share": sum(hits.values()) / beats,
            "clips": {"chain": save("applied.chain", s, level=None, detail="a chain of applied dominants in C major: Part 7's piano")}}


def compute_mixture() -> dict:
    b = X.borrowed(0)
    plans = {"iv": [((0, 4, 7), 48), (b["iv"], 41), ((0, 4, 7), 48)],
             "flat6": [((0, 4, 7), 48), (b["♭VI"], 44), (b["♭VII"], 46), ((0, 4, 7), 48)],
             "flat3": [((0, 4, 7), 48), (b["♭III"], 51), ((5, 9, 0), 53), ((7, 11, 2, 5), 43), ((0, 4, 7), 48)]}
    out, clips = {}, {}
    for name, plan in plans.items():
        chords = realize(plan)
        out[name] = rows(chords)
        clips[name] = play(chords_events(chords, beats=2.0))
    s = seq(clips)
    times = {n: [float(s.events[f"{n}.t{k}"]) for k in range(len(out[n]))] for n in out}
    return {"chords": out, "names": {"iv": ["I", "iv", "I"], "flat6": ["I", "♭VI", "♭VII", "I"], "flat3": ["I", "♭III", "IV", "V7", "I"]},
            "times": times, "starts": {n: float(s.events[n]) for n in out},
            "clips": {"three": save("mixture.three", s, level=None, detail="three borrowings from C minor in C major: iv; flat VI and flat VII; flat III: Part 7's piano")}}


def compute_neapolitan() -> dict:
    plan = [((0, 3, 7), 48), (X.neapolitan(0), 53), ((7, 11, 2, 5), 43), ((0, 3, 7), 48)]
    plain = [((0, 3, 7), 48), ((5, 8, 0), 53), ((7, 11, 2, 5), 43), ((0, 3, 7), 48)]
    ch_n, ch_p = realize(plan), realize(plain)
    s = concat([play(chords_events(ch_p)).at_level(LEVEL), play(chords_events(ch_n)).at_level(LEVEL)], gap=1.0, names=["iv", "N"])
    return {"plain": rows(ch_p), "neapolitan": rows(ch_n), "starts": {k: float(s.events[k]) for k in ("iv", "N")},
            "times": {k: [float(s.events[f"{k}.t{j}"]) for j in range(4)] for k in ("iv", "N")},
            "clips": {"pair": save("neapolitan.pair", s, level=None, detail="in C minor: i, iv6, V7, i; then i, the Neapolitan sixth, V7, i: Part 7's piano")}}


def compute_sixths() -> dict:
    six = X.augmented_sixths(0)
    out, clips = {}, {}
    for name in ("Italian", "French", "German"):
        pcs = six[name]
        first = voice((72, 67, 63, 48), list(pcs[1:]) + [pcs[0]], 44, full=True)
        v = voice(first, [7, 11, 2], 43)
        chords = [voice((72, 67, 63, 48), [0, 3, 7], 48), first, v]
        out[name] = {"chords": rows(chords), "pcs": list(pcs)}
        clips[name] = play(chords_events(chords))
    s = seq(clips)
    for name in out:
        out[name]["times"] = [float(s.events[f"{name}.t{k}"]) for k in range(3)]
        out[name]["start"] = float(s.events[name])
    return {**out, "clips": {"three": save("sixths.three", s, level=None, detail="the Italian, French and German sixths in C minor, each resolving to V: Part 7's piano")}}


def compute_dim7() -> dict:
    d = X.dim7(11)                                        # B D F A♭
    targets = [((0, "minor"), 48), ((3, "minor"), 51), ((6, "minor"), 42), ((9, "minor"), 45)]
    clips, out = {}, []
    for (tonic, mode), bass in targets:
        lead_pc = (tonic + 11) % 12
        lead_bass = lead_pc + 48 if lead_pc + 48 <= 55 else lead_pc + 36
        first = voice((74, 71, 65, 50), list(d), lead_bass, full=True)
        res = voice(first, [tonic, (tonic + 3) % 12, (tonic + 7) % 12], bass)
        out.append({"key": [tonic, mode], "name": X.key_name((tonic, mode)), "leading": lead_pc, "chords": rows([first, res])})
        clips[X.key_name((tonic, mode))] = play(chords_events([first, res]))
    s = seq(clips)
    for o in out:
        o["start"] = float(s.events[o["name"]])
        o["times"] = [float(s.events[f"{o['name']}.t{k}"]) for k in range(2)]
    return {"chord": list(d), "resolutions": out, "eight": [[r["key"][0], r["key"][1]] for r in X.dim7_resolutions(d)],
            "clips": {"four": save("dim7.four", s, level=None, detail="one diminished seventh, B D F A flat, resolved to C, E flat, F sharp and A minor: Part 7's piano")}}


def compute_trapdoor() -> dict:
    ger = X.augmented_sixths(0)["German"]                  # A♭ C E♭ F♯
    home = realize([((0, 4, 7), 48), ((5, 9, 0), 53), (ger, 44), ((0, 4, 7), 43), ((7, 11, 2, 5), 43), ((0, 4, 7), 48)])
    away = realize([((0, 4, 7), 48), ((5, 9, 0), 53), (ger, 44), ((1, 5, 8), 49), ((6, 10, 1), 54), ((8, 0, 3, 6), 44), ((1, 5, 8), 49)])
    s = concat([play(chords_events(home)).at_level(LEVEL), play(chords_events(away)).at_level(LEVEL)], gap=1.2, names=["home", "away"])
    return {"home": rows(home), "away": rows(away), "home_names": ["I", "IV", "Ger+6", "I6/4", "V7", "I"],
            "away_names": ["I", "IV", "V7 of D♭", "D♭: I", "IV", "V7", "I"], "same": X.german_as_dominant(0)["same"],
            "times": {k: [float(s.events[f"{k}.t{j}"]) for j in range(len(v))] for k, v in (("home", home), ("away", away))},
            "starts": {k: float(s.events[k]) for k in ("home", "away")},
            "clips": {"two": save("trapdoor.two", s, level=None, detail="a German sixth in C that resolves home; the same chord heard as the dominant seventh of D flat: Part 7's piano")}}


def compute_comma() -> dict:
    d = X.enharmonic_drift()
    f0 = hz(48)
    # four pure minor thirds up from C3, one after another, then the last note together with the octave it stands for
    steps = [f0 * float(Fraction(6, 5) ** k) for k in range(5)]
    octave = f0 * 2                                       # four minor thirds stand for one octave (4 x 3 semitones)
    tones, ev = [], {}
    for k, f in enumerate(steps):
        ev[f"n{k}"] = k * 0.8
        tones.append((Clip(organ_tone(f, 0.75, partials=6, rolloff=0.7)).fade(0.02, 0.1), k * 0.8, 0.0))
    t_last = len(steps) * 0.8 + 0.4
    ev["both"] = t_last
    tones.append((Clip(organ_tone(steps[-1], 3.0, partials=6, rolloff=0.7)).fade(0.02, 0.2), t_last, 0.0))
    tones.append((Clip(organ_tone(octave, 3.0, partials=6, rolloff=0.7)).fade(0.02, 0.2), t_last, 0.0))
    eq = [(Clip(organ_tone(f0 * 2 ** (3 * k / 12), 0.75, partials=6, rolloff=0.7)).fade(0.02, 0.1), t_last + 3.6 + k * 0.8, 0.0) for k in range(5)]
    ev["equal"] = t_last + 3.6
    tones += eq
    tones.append((Clip(organ_tone(f0 * 2, 3.0, partials=6, rolloff=0.7)).fade(0.02, 0.2), t_last + 3.6 + 4.4, 0.0))
    tones.append((Clip(organ_tone(f0 * 2, 3.0, partials=6, rolloff=0.7)).fade(0.02, 0.2), t_last + 3.6 + 4.4, 0.0))
    ev["equal_both"] = t_last + 3.6 + 4.4
    c = Clip(mix(tones, duration=t_last + 3.6 + 4.4 + 3.4).y, SR, ev, []).at_level(LEVEL)
    beat_hz = abs(steps[-1] - octave)
    return {**d, "beat_hz": float(beat_hz), "freqs": [float(f) for f in steps], "octave": float(octave),
            "events": {k: float(v) for k, v in ev.items()},
            "clips": {"thirds": save("comma.thirds", c, level=None, kind="synthesized", detail="four pure minor thirds from C, and the C they should reach, together; then the same in equal temperament: organ tones")}}


def compute_mediants() -> dict:
    cyc = X.hexatonic((0, "major"))
    chords, prev = [], (72, 67, 64, 48)
    for (r, kind) in cyc:
        pcs = list(X.triad(r, kind))
        ch = voice(prev, pcs, 36 + ((r - 36) % 12) + (12 if (36 + (r % 12)) < 40 else 0))
        chords.append(ch)
        prev = ch
    vls = [X.voice_leading(X.triad(*a), X.triad(*b))["cost"] for a, b in zip(cyc, cyc[1:])]
    med = [(0, "major"), (4, "major"), (8, "major"), (0, "major")]
    mch, prev = [], (72, 67, 64, 48)
    for (r, kind) in med:
        ch = voice(prev, list(X.triad(r, kind)), 36 + (r % 12) + (12 if (r % 12) < 4 else 0))
        mch.append(ch)
        prev = ch
    s = concat([play(chords_events(mch)).at_level(LEVEL), play(chords_events(chords)).at_level(LEVEL)], gap=1.2, names=["thirds", "hexatonic"])
    return {"cycle": [[r, k] for r, k in cyc], "names": [CH.triad_name(t) for t in cyc], "voice_leading": vls, "chords": rows(chords),
            "mediants": rows(mch), "mediant_names": ["C", "E", "A♭", "C"],
            "times": {"thirds": [float(s.events[f"thirds.t{k}"]) for k in range(len(mch))], "hexatonic": [float(s.events[f"hexatonic.t{k}"]) for k in range(len(chords))]},
            "starts": {k: float(s.events[k]) for k in ("thirds", "hexatonic")},
            "clips": {"cycles": save("mediants.cycles", s, level=None, detail="C, E, A flat, C major; then the hexatonic cycle C, c, A flat, a flat, E, e, C: Part 7's piano")}}


def compute_paths() -> dict:
    out = {}
    for chrom in (False, True):
        d = X.distances((0, "major"), chrom)
        out["chromatic" if chrom else "pivots"] = {X.key_name(k): v for k, v in d["dist"].items()}
        if chrom:
            out["routes"] = {X.key_name(k): [[X.key_name(a), X.key_name(b), how] for a, b, how in r] for k, r in d["routes"].items()}
        else:
            out["routes_pivots"] = {X.key_name(k): [[X.key_name(a), X.key_name(b), how] for a, b, how in r] for k, r in d["routes"].items()}
    return out


def compute_tension() -> dict:
    C = (0, "major")
    diatonic = [(0, "major", C), (9, "minor", C), (2, "minor", C), (7, "7", C), (0, "major", C)]
    chromatic = [(0, "major", C), (8, "major", C), (1, "major", (5, "minor")), (7, "7", C), (0, "major", C)]
    trap = [(0, "major", C), (5, "major", C), (8, "7", (1, "major")), (1, "major", (1, "major")), (8, "7", (1, "major")), (1, "major", (1, "major"))]
    out = {}
    for name, prog in (("diatonic", diatonic), ("mixture", chromatic), ("trapdoor", trap)):
        out[name] = {"tension": X.tension_curve(prog), "chords": [[r, k, list(key)] for r, k, key in prog]}
    out["examples"] = {"I-V": X.chord_distance((0, "major", C), (7, "major", C)), "I-ii": X.chord_distance((0, "major", C), (2, "minor", C)),
                       "I-vi": X.chord_distance((0, "major", C), (9, "minor", C)), "C to F# major": X.chord_distance((0, "major", C), (6, "major", (6, "major")))}
    return out


def compute_tristan() -> dict:
    vl = X.tristan_voice_leading()
    return {"readings": X.TRISTAN_READINGS, "voice_leading": vl, "chord": list(X.TRISTAN["chord"]), "resolution": list(X.TRISTAN["resolution"]),
            "half_dim": sorted(p % 12 for p in X.TRISTAN["chord"]) == sorted(X.triad(5, "m7b5"))}


# Variation 19: the Tune's two phrases three times, a chord to each half bar
VAR = {
    "mixture": {"plan": [((0, 4, 7), 48), ((3, 7, 10), 51), ((5, 9, 0), 53), ((0, 4, 7, 10), 48), ((5, 8, 0), 53), ((9, 1, 4, 7), 49), ((7, 11, 2, 5), 43), ((0, 4, 7), 48)],
                "names": ["I", "♭III", "IV", "V7/IV", "iv", "V6/5 of ii", "V7", "I"], "shift": [0] * 8},
    "neapolitan": {"plan": [((0, 3, 7), 48), ((3, 7, 10), 51), ((2, 6, 9, 0), 50), ((7, 11, 2), 43), ((1, 5, 8), 53), ((0, 4, 7), 43), ((7, 11, 2, 5), 43), ((0, 4, 7), 48)],
                   "names": ["i", "♭III", "V7/V", "V", "N6", "I6/4", "V7", "I"], "shift": [0] * 8},
    "trapdoor": {"plan": [((0, 4, 7), 48), ((4, 7, 11), 52), ((9, 0, 4), 45), ((7, 10, 1, 4), 46), ((1, 5, 8), 53), ((8, 0, 3), 48), ((3, 7, 10, 1), 51), ((8, 0, 3), 44)],
                 "names": ["I", "iii", "vi", "vii°7 of A♭", "A♭: IV6", "I6", "V7", "I"], "shift": [0, 0, 0, 0, -4, -4, -4, -4]},
}


def compute_tune() -> dict:
    tune = M.corpus()[0]
    pitches, beats = tune.pitches[:14], tune.beats[:14]
    out, clips = {}, {}
    for name, v in VAR.items():
        mel, t = [], 0.0
        for k, (p, bt) in enumerate(zip(pitches, beats)):
            half = int(t // 2)
            m = 72 + p + v["shift"][half]
            if name == "neapolitan" and half == 0:
                m = 72 + p - (1 if p % 12 in (4, 9) else 0)
            mel.append((m, t, bt))
            t += bt
        chords, prev = [], (67, 64, 60, 48)
        for k, (pcs, bass) in enumerate(v["plan"]):
            top = next(m for m, a, d in mel if 2 * k <= a < 2 * k + 2)
            assert top % 12 in pcs, (name, k, top, pcs)
            ch = voice(prev, list(pcs), bass, top)
            chords.append(ch)
            prev = ch
        events = [(m, a, d, 1.0) for m, a, d in mel] + [(x, 2 * k, 2.0, -3.0) for k, ch in enumerate(chords) for x in ch[1:]]
        clips[name] = play(events)
        out[name] = {"melody": [[int(m), float(a), float(d)] for m, a, d in mel], "chords": rows(chords), "names": v["names"],
                     "parallels": [k for k, (a, b) in enumerate(zip(chords, chords[1:])) if F.parallels(a, b)]}
    s = seq(clips)
    for name in out:
        out[name]["start"] = float(s.events[name])
        out[name]["times_c"] = [float(s.events[name]) + 2 * k * BEAT for k in range(8)]
    outside = sum(1 for v in VAR.values() for pcs, _ in v["plan"] if not set(pcs) <= set(X.MAJOR))
    return {"versions": out, "order": list(out), "seconds": s.duration, "outside_c": outside, "clip": {"name": "tune.variation19", "seconds": s.duration},
            "clips": {"variation": save("tune.variation19", s, level=None, detail="the Tune with mixture and applied dominants; with the Neapolitan; and through a diminished-seventh trapdoor into A flat: Part 7's piano")}}


def compute_variation() -> dict:
    t = load("tune")
    n_par = sum(len(v["parallels"]) for v in t["versions"].values())
    return {"part": 19, "title": r"with borrowed chords, with the Neapolitan, and through a diminished-seventh trapdoor into A$\flat$", "seconds": round(t["seconds"], 2),
            "measure": rf"24 chords, {t['outside_c']} of them outside C major; one chord carries the Tune four keys away; {n_par} parallels", "clip": "tune.variation19"}


ITEMS = {"hook": compute_hook, "applied": compute_applied, "mixture": compute_mixture, "neapolitan": compute_neapolitan, "sixths": compute_sixths,
         "dim7": compute_dim7, "trapdoor": compute_trapdoor, "comma": compute_comma, "mediants": compute_mediants, "paths": compute_paths,
         "tension": compute_tension, "tristan": compute_tristan, "tune": compute_tune, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
