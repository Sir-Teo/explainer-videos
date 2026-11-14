"""Precompute everything numerical, and every sound, in Part 10 of *Music, Built* ("Writing It Down").

    python -m videos.music.music10.compute              # everything missing (about a minute)
    python -m videos.music.music10.compute --force omr

Numbers are cached in ``.cache/music10/<name>.json`` (+ ``.npz``), sounds in ``.cache/music10/audio/``.  The score
model, its writers and readers and the counting are Monochord's (``explainer/music/monochord/score/``); sources for
the historical notations are in the README.

Items:
    hook        the first line of the notation on the tablet from Ugarit, read two ways
    neumes      the Tune's contour: how many melodies fit it, and three of them
    guido       *Ut queant laxis*: six lines that start on six rising notes
    mensural    one row of marks under the two signs of time; dots and ties
    score       two voices, in parts and in score
    tab         the Tune on a guitar: every fingering, and the one with the least movement
    figured     a figured bass realized twice
    east        the Tune in jianpu and in gongche
    midi        the bytes of a MIDI file; what it forgets; two notes that share a key
    xml         the page as data: MusicXML and MEI, and what survives a round trip
    bits        the bits in each encoding against the bits in the sound; the page played exactly and played well
    omr         a page as pixels, read back; tilted, speckled, straightened
    tune        Variation 10: the Tune read off the page, and then as none of its notations says
    variation   the Variations ledger, row 10
"""

from __future__ import annotations

import math
import subprocess
import tempfile
from fractions import Fraction
from pathlib import Path

import numpy as np

from explainer.ai.cache import Cache
from explainer.music.monochord import EXAMPLE_LEVEL, SR, Clip, ClipStore, concat, mix
from explainer.music.monochord import score as SC
from explainer.music.monochord.instruments import strings as STR
from explainer.music.monochord.instruments import winds as W
from explainer.music.monochord.instruments.plucked import plucked
from explainer.music.monochord.partkit import organ_tone, saver
from explainer.music.monochord.physics.string import String
from explainer.music.monochord.pitch import cents
from explainer.music.monochord.score import codes, figured, mensural, perform, raster, read, tab, write

CACHE = Cache("music10")
CLIPS = ClipStore("music10")
load = CACHE.load

LEVEL = EXAMPLE_LEVEL - 2.5
save = saver(CLIPS, LEVEL, kind="physical model")
C4 = 261.6255653005986
BEAT = 60.0 / 109.0
P = SC.Pitch.parse
BOARD, GUITAR = STR.soundboard(), STR.guitar_body()
NYLON = dict(L=0.65, mu=0.0012, kappa=0.25, sigma0=0.9, sigma1=2.0e-3)
TUNE = SC.tune_score()
PHRASE = 2 * TUNE.bar                                   # a phrase of the Tune is two bars


def clip(y, fade=(0.002, 0.06)) -> Clip:
    return Clip(np.asarray(y, dtype=np.float64)).fade(*fade)


# --- the voices of this part --------------------------------------------------------------------------------------
def string(hz: float, seconds: float, n=None) -> Clip:
    """Part 1's plucked string."""
    return clip(plucked(f1=hz, seconds=seconds + 0.9, beta=0.18), (0.002, 0.25)).at_level(LEVEL)


def piano(hz: float, seconds: float, n=None) -> Clip:
    """Part 7's hammer, string and soundboard; the damper falls when the note's time is up."""
    y = BOARD.play(STR.struck(String.tuned(hz, L=0.62 * (C4 / hz) ** 0.8, mu=6.34e-3, kappa=1.25, sigma0=0.6, sigma1=3.3e-4), velocity=1.6, seconds=seconds + 0.2))
    return clip(y, (0.001, 0.16)).at_level(LEVEL)


def guitar(hz: float, seconds: float, n=None) -> Clip:
    return clip(GUITAR.play(plucked(string=String.tuned(hz, **NYLON), seconds=seconds + 0.8, beta=0.16)), (0.002, 0.3)).at_level(LEVEL)


def flute(hz: float, seconds: float, n=None) -> Clip:
    return clip(W.jet_tone(hz, seconds * 0.95), (0.01, 0.06)).at_level(LEVEL)


def quill(hz: float, seconds: float, n=None) -> Clip:
    """A bright plucked string, for a continuo player's chords."""
    return clip(plucked(f1=hz, seconds=seconds + 0.5, beta=0.09), (0.001, 0.2)).at_level(LEVEL)


def render(notes, voice, extra: float = 0.0) -> Clip:
    """Notes ``{"t", "dur", "hz", "db"}`` played by a voice.  The clip has an event ``n<k>`` at every note."""
    placed, events, rows = [], {}, []
    for k, n in enumerate(notes):
        placed.append((voice(n["hz"], n["dur"] + (extra if k == len(notes) - 1 else 0.0), n), n["t"], n.get("db", 0.0)))
        events[f"n{k}"] = n["t"]
        rows.append({"t": n["t"], "dur": n["dur"], "hz": n["hz"], "midi": n.get("midi", 0)})
    end = notes[-1]["t"] + notes[-1]["dur"]
    c = mix(placed, duration=max(end, max(p[1] + p[0].duration for p in placed)))
    events["end"] = end
    return Clip(c.y, SR, events, rows)


def line(pitches, beats, beat: float = BEAT, t0: float = 0.0, db=None) -> list[dict]:
    """Pitches (names or ``Pitch``) and lengths in beats, as notes."""
    out, t = [], t0
    for k, (p, b) in enumerate(zip(pitches, beats)):
        p = P(p) if isinstance(p, str) else p
        out.append({"t": t, "dur": b * beat, "hz": p.hz(), "midi": p.midi, "db": 0.0 if db is None else db[k]})
        t += b * beat
    return out


def note_times(c: Clip, prefix: str = "") -> list[float]:
    k, out = 0, []
    while f"{prefix}n{k}" in c.events:
        out.append(float(c.events[f"{prefix}n{k}"]))
        k += 1
    return out


def sub_score(first_bar: int, bars: int) -> SC.Score:
    """Some bars of the Tune as a score of their own."""
    ms = TUNE.measures(0)[first_bar: first_bar + bars]
    return SC.Score([SC.Voice([e for m in ms for e in m])], key=0, time=TUNE.time, tempo=TUNE.tempo)


# ---------------------------------------------------------------------------
LINE1 = [("qablite", 3), ("irbute", 1), ("qablite", 3), ("šaḫri", 1), ("išarte", 10)]
PAIRS = {"qablite": (5, 2), "irbute": (2, 7), "šaḫri": (7, 5), "išarte": (2, 6)}       # pairs of strings (after the tablet CBS 10996)
PYTHAGOREAN = [Fraction(1), Fraction(9, 8), Fraction(81, 64), Fraction(4, 3), Fraction(3, 2), Fraction(27, 16), Fraction(243, 128), Fraction(2), Fraction(9, 4)]


def compute_hook() -> dict:
    step = 0.34
    up = [C4 * float(r) for r in PYTHAGOREAN]                     # string 1 is the lowest ...
    down = up[::-1]                                               # ... or the highest
    a_notes, a_words, t = [], [], 0.0
    for word, n in LINE1:                                         # reading A: the two strings together, struck n times
        i, j = PAIRS[word]
        a_words.append(t)
        for _ in range(n):
            a_notes += [{"t": t, "dur": step, "hz": up[i - 1], "db": -3.0}, {"t": t + 0.012, "dur": step, "hz": up[j - 1], "db": -3.0}]
            t += step
    b_notes, b_words, t = [], [], 0.0
    for word, n in LINE1:                                         # reading B: the first string, then the second n times
        i, j = PAIRS[word]
        b_words.append(t)
        b_notes.append({"t": t, "dur": step, "hz": down[i - 1], "db": 0.0})
        t += step
        for _ in range(n):
            b_notes.append({"t": t, "dur": step, "hz": down[j - 1], "db": -1.0})
            t += step
    a, b = render(a_notes, string, 0.4), render(b_notes, string, 0.4)
    seq = concat([a.at_level(LEVEL), b.at_level(LEVEL)], gap=0.9, names=["A", "B"])
    return {"line": [[w, n] for w, n in LINE1], "pairs": {k: list(v) for k, v in PAIRS.items()},
            "words_a": [seq.events["A"] + x for x in a_words], "words_b": [seq.events["B"] + x for x in b_words],
            "strokes_a": sum(n for _, n in LINE1), "strokes_b": sum(n + 1 for _, n in LINE1),
            "clips": {"readings": save("hook.readings", seq, level=None, detail="one line of the tablet, read two ways; neither is a reconstruction")}}


def compute_neumes() -> dict:
    keys = [n.pitch.midi for n in TUNE.voices[0].notes]
    steps = [n.pitch.diatonic - P("C4").diatonic for n in TUNE.voices[0].notes][:7]           # 0 0 4 4 5 5 4
    con = codes.contour(steps)
    counts = {str(k): codes.count_contour(con, k) for k in (6, 7, 8)}
    others, seed = [], 0
    while len(others) < 2:                                         # two more melodies of the hexachord with the same contour
        m = codes.with_contour(con, 6, seed)
        seed += 1
        if m != steps and m not in others and max(m) - min(m) >= 3 and all(sum(a != b for a, b in zip(m, o)) >= 4 for o in others + [steps]):
            others.append(m)
    scale = ["C4", "D4", "E4", "F4", "G4", "A4"]
    beats = [1, 1, 1, 1, 1, 1, 2]
    order = [others[0], steps, others[1]]
    clips_ = [render(line([scale[s] for s in m], beats), string, 0.5).at_level(LEVEL) for m in order]
    seq = concat(clips_, gap=0.7, names=["A", "B", "C"])
    return {"steps": steps, "contour": con, "counts": counts, "whole_tune_octave": codes.count_contour(codes.contour(keys), 8),
            "melodies": order, "names": [[scale[s][0] for s in m] for m in order], "tune_is": "B",
            "contour_bits": 6 * math.log2(3), "pitch_bits": 7 * math.log2(6),
            "times": {nm: [seq.events[f"{nm}.n{k}"] for k in range(7)] for nm in "ABC"},
            "clips": {"three": save("neumes.three", seq, level=None, detail="three melodies with the same ups and downs")}}


HYMN = [("Ut queant laxis", "Ut", "u", ["C3", "D3", "F3", "D3", "E3", "D3"]),
        ("resonare fibris", "re", "E", ["D3", "D3", "C3", "D3", "E3", "E3"]),
        ("Mira gestorum", "mi", "i", ["E3", "F3", "G3", "E3", "D3", "E3", "C3", "D3"]),
        ("famuli tuorum", "fa", "a", ["F3", "G3", "A3", "G3", "F3", "D3", "D3"]),
        ("Solve polluti", "sol", "O", ["G3", "A3", "G3", "F3", "E3", "F3", "G3", "D3"]),
        ("labii reatum", "la", "a", ["A3", "G3", "A3", "F3", "G3", "A3", "A3"]),
        ("Sancte Iohannes", "", "a", ["G3", "F3", "E3", "D3", "C3", "E3", "D3"])]


def compute_guido() -> dict:
    """The hymn sung by Part 8's voice, each line on the vowel of its first syllable."""
    step, breath = 0.34, 0.42
    parts, names, times, lines = [], [], [], []
    for k, (words, syl, vowel, notes) in enumerate(HYMN):
        hz = [P(n).hz() for n in notes]
        dur = [step] * (len(hz) - 1) + [2.2 * step]
        n = int(sum(dur) * SR)
        f = np.zeros(n)
        t, starts = 0.0, []
        for h, d in zip(hz, dur):
            f[int(t * SR): int((t + d) * SR)] = h
            starts.append(t)
            t += d
        f[f == 0] = hz[-1]
        w = int(0.035 * SR)
        f = np.convolve(np.pad(f, w, mode="edge"), np.ones(w) / w, mode="same")[w: w + n]       # the voice slides between its notes
        y = W.voice(f, W.VOWELS[vowel], n / SR, seed=k)
        parts.append(clip(y, (0.04, 0.12)).at_level(LEVEL))
        names.append(f"line{k}")
        times.append(starts)
        lines.append({"words": words, "syllable": syl, "notes": notes, "first": notes[0]})
    seq = concat(parts, gap=breath, names=names)
    firsts = [P(r["first"]).midi for r in lines[:6]]
    return {"lines": lines, "times": [[seq.events[f"line{k}"] + x for x in ts] for k, ts in enumerate(times)],
            "first_steps": [b - a for a, b in zip(firsts, firsts[1:])],                    # 2 2 1 2 2: tone tone semitone tone tone
            "clips": {"hymn": save("guido.hymn", seq, kind="physical model", detail="Part 8's voice; each line on the vowel of its first syllable")}}


def compute_mensural() -> dict:
    marks = "SSSSSSB" * 2
    names = ["C4", "C4", "G4", "G4", "A4", "A4", "G4", "F4", "F4", "E4", "E4", "D4", "D4", "C4"]
    semibreve = 0.40
    out, clips_ = {}, []
    for label_, perfect, group in (("two", False, 2), ("three", True, 3)):
        lengths = mensural.read(marks, perfect)
        starts = np.concatenate([[0], np.cumsum(lengths)[:-1]])
        db = [1.5 if s % group == 0 else -1.5 for s in starts]
        clips_.append(render(line(names, lengths, semibreve, db=db), string, 0.5).at_level(LEVEL))
        out[label_] = {"lengths": lengths, "total": int(sum(lengths)), "starts": [int(s) for s in starts]}
    seq = concat(clips_, gap=0.8, names=["two", "three"])
    examples = {s: mensural.read(s) for s in ("BSB", "BSSB", "BSSSB")}
    ties = {"5/8": [[str(v), d] for v, d in codes.binary_values(Fraction(5, 8))], "7/8": [[str(v), d] for v, d in codes.binary_values(Fraction(7, 8))],
            "11/16": [[str(v), d] for v, d in codes.binary_values(Fraction(11, 16))]}
    return {"marks": marks, "names": names, "positions": [P(n).staff_position("treble") for n in names], **out, "examples": examples,
            "dots": [str(codes.dotted(k)) for k in range(4)], "ties": ties,
            "times": {nm: [seq.events[f"{nm}.n{k}"] for k in range(14)] for nm in ("two", "three")},
            "clips": {"signs": save("mensural.signs", seq, level=None, detail="one row of marks, read in twos and then in threes")}}


BASS = ["C3", "E3", "F3", "E3", "D3", "C3", "G2", "C3"]
FIGURES = ["", "6", "", "6", "6", "", "7", ""]


def compute_score() -> dict:
    mel = sub_score(0, 4)
    top = perform.deadpan(mel)
    low = line(BASS, [2] * 8, db=[-4.0] * 8)
    c = render(top + low, piano, 0.6)
    ev = {f"n{k}": n["t"] for k, n in enumerate(top)}
    ev.update({f"b{k}": n["t"] for k, n in enumerate(low)})
    ev["end"] = c.events["end"]
    duet = Clip(c.y, SR, ev, c.notes)
    return {"bass": BASS, "melody": [n.pitch.name for n in mel.voices[0].notes], "seconds": duet.duration,
            "clips": {"duet": save("score.duet", duet, detail="two voices: the Tune and a bass, on Part 7's piano")}}


def compute_tab() -> dict:
    keys = [n.pitch.midi for n in TUNE.voices[0].notes]
    first = keys[:14]
    best = tab.fingering(first)
    one = [(4, m - tab.GUITAR[4]) for m in first]                        # the same notes, all on the B string
    cost_one = sum(tab._cost(a, b) for a, b in zip(one, one[1:])) + 0.15 * one[0][1]
    c = render(line([SC.Pitch.from_midi(m) for m in first], [1, 1, 1, 1, 1, 1, 2] * 2), guitar, 0.8)
    return {"keys": first, "best": [list(p) for p in best["positions"]], "one_string": [list(p) for p in one], "choices": best["choices"],
            "cost_best": best["cost"], "cost_one": cost_one, "count_phrases": tab.count_fingerings(first), "count_tune": float(tab.count_fingerings(keys)),
            "middle_c": [list(p) for p in tab.positions(60)], "strings": ["E", "A", "D", "G", "B", "e"],
            "clips": {"phrase": save("tab.phrase", c, detail="Part 7's guitar")}}


def compute_figured() -> dict:
    bass = [P(b) for b in BASS]
    a = figured.realize(bass, FIGURES)
    b = figured.realize(bass, FIGURES, top=79)
    chord_t = 0.95

    def played(chords):
        notes = []
        for k, (bs, ch) in enumerate(zip(bass, chords)):
            notes.append({"t": k * chord_t, "dur": chord_t, "hz": bs.hz(), "db": 0.0})
            for j, m in enumerate(ch):
                notes.append({"t": k * chord_t + 0.018 * (j + 1), "dur": chord_t, "hz": SC.Pitch.from_midi(m).hz(), "db": -5.0})
        return render(notes, quill, 0.8).at_level(LEVEL)

    seq = concat([played(a["chords"]), played(b["chords"])], gap=0.9, names=["A", "B"])
    wanted = [[p.name for p in figured.chord(bs, f)] for bs, f in zip(bass, FIGURES)]
    return {"bass": BASS, "figures": FIGURES, "wanted": wanted, "a": [list(c) for c in a["chords"]], "b": [list(c) for c in b["chords"]],
            "a_names": [[SC.Pitch.from_midi(m).name for m in c] for c in a["chords"]], "b_names": [[SC.Pitch.from_midi(m).name for m in c] for c in b["chords"]],
            "choices": a["choices"], "count": float(a["count"]), "parallels": [a["parallels"], b["parallels"]],
            "times": {nm: [seq.events[nm] + k * chord_t for k in range(8)] for nm in "AB"},
            "clips": {"twice": save("figured.twice", seq, level=None, detail="one bass and its figures, filled in twice")}}


def compute_east() -> dict:
    two = sub_score(0, 4)
    high = SC.Score([SC.Voice([SC.Note(SC.Pitch(n.pitch.step, n.pitch.alter, n.pitch.octave + 1), n.dur) for n in two.voices[0].notes])], tempo=TUNE.tempo)
    c = render(perform.deadpan(high, gate=0.96), flute, 0.3)
    degrees = [SC.STEPS.index(n.pitch.step) + 1 for n in two.voices[0].notes]
    return {"jianpu": write.jianpu(two), "degrees": degrees, "beats": [int(n.dur / SC.Q) for n in two.voices[0].notes], "gongche": codes.gongche(two),
            "names": [codes.GONGCHE_NAMES[ch] for ch in codes.gongche(two)],
            "clips": {"flute": save("east.flute", c, detail="Part 8's flute")}}


def compute_midi() -> dict:
    data = write.midi(TUNE)
    first = data.index(bytes([0x90])) - 1                               # the delta time before the first note-on
    per = 9                                                             # delta, note on (3 bytes), delta (2), note off (3)
    groups = [[first + k * per, first + (k + 1) * per] for k in range(4)]
    flat = SC.Score([SC.Voice([SC.Note(P(n), SC.Q) for n in ("Eb4", "G4", "Bb4", "Eb5")])], key=-3)
    back = read.midi(write.midi(flat))
    c4 = C4
    e, gs, ab = c4 * 5 / 4, c4 * 25 / 16, c4 * 8 / 5                    # quarter-comma meantone: its major thirds are pure
    tone = lambda f, s: clip(organ_tone(f, s, partials=6), (0.03, 0.1)).at_level(LEVEL)                    # noqa: E731
    both = lambda f1, f2, s: clip(organ_tone(f1, s, partials=6) + organ_tone(f2, s, partials=6), (0.03, 0.12)).at_level(LEVEL)      # noqa: E731
    seq = concat([tone(gs, 1.1), tone(ab, 1.1), tone(gs, 1.1), tone(ab, 1.1), both(e, gs, 2.2), both(e, ab, 2.2)], gap=0.35,
                 names=["x1", "y1", "x2", "y2", "third", "wolf"])
    return {"bytes": list(data[: first + 4 * per]), "size": len(data), "first": first, "groups": groups, "per_note": per,
            "header": [0, 14], "track": [14, 22], "meta": [22, first], "key_number": data[first + 2], "velocity": data[first + 3],
            "ticks": 480, "written": ["Eb4", "G4", "Bb4", "Eb5"], "read_back": [n.pitch.name for n in back.voices[0].notes], "keys": [P(n).midi for n in ("Eb4", "G4", "Bb4", "Eb5")],
            "g_sharp": gs, "a_flat": ab, "e": e, "equal": P("G#4").hz(), "diesis_cents": cents(ab / gs), "wolf_cents": cents(ab / e), "pure_cents": cents(gs / e),
            "clips": {"pair": save("midi.pair", seq, kind="synthesized", level=None, detail="G sharp and A flat as an organ tuned in quarter-comma meantone has them")}}


def compute_xml() -> dict:
    x, m = write.musicxml(TUNE), write.mei(TUNE)
    words = SC.tune_score(words=True)
    same = read.musicxml(write.musicxml(words))
    kept = [(a.pitch, a.dur, a.lyric) == (b.pitch, b.dur, b.lyric) for a, b in zip(words.voices[0].events, same.voices[0].events)]
    via = read.midi(write.midi(words))
    lost = {"spelling": any(a.pitch != b.pitch for a, b in zip(P_FLAT.voices[0].notes, read.midi(write.midi(P_FLAT)).voices[0].notes)),
            "words": all(n.lyric is None for n in via.voices[0].notes), "keys": [a.pitch.midi for a in words.voices[0].notes] == [b.pitch.midi for b in via.voices[0].notes]}
    xml_note = ("<note>\n  <pitch>\n    <step>C</step>\n    <octave>4</octave>\n  </pitch>\n  <duration>480</duration>\n  <type>quarter</type>\n"
                "  <lyric><text>Twin-</text></lyric>\n</note>")
    mei_note = '<note pname="c" oct="4" dur="4">\n  <verse><syl>Twin-</syl></verse>\n</note>'
    return {"musicxml_bytes": len(x.encode()), "mei_bytes": len(m.encode()), "xml_note": xml_note, "mei_note": mei_note, "midi_note": "00 90 3C 50 83 60 80 3C 00",
            "round_trip_same": bool(all(kept)) and len(kept) == 42, "midi_loses": lost, "notes_per_kb": 42 / (len(x.encode()) / 1000)}


P_FLAT = SC.Score([SC.Voice([SC.Note(P(n), SC.Q) for n in ("Eb4", "G4", "Bb4", "Eb5")])], key=-3)


def _encoded(c: Clip) -> dict:
    """The bytes a sound takes as a plain 16-bit file, and through three codecs (ffmpeg)."""
    out = {}
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "a.wav"
        c.write_pcm16(wav)
        out["WAV"] = wav.stat().st_size
        for name, args, ext in (("FLAC", ["-c:a", "flac"], "flac"), ("MP3", ["-c:a", "libmp3lame", "-b:a", "128k"], "mp3"), ("Opus", ["-c:a", "libopus", "-b:a", "32k"], "opus")):
            dst = Path(tmp) / f"a.{ext}"
            r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), *args, str(dst)], capture_output=True)
            if r.returncode == 0 and dst.exists():
                out[name] = dst.stat().st_size
    return out


def compute_bits() -> dict:
    sizes = codes.sizes(TUNE)
    sizes["gongche"] = len("".join(codes.gongche(TUNE)).encode())
    d = codes.description_bits(TUNE)
    phrases = [tuple((e.pitch.name, e.dur) for e in TUNE.voices[0].events[k: k + 7]) for k in range(0, 42, 7)]
    distinct = sorted(set(phrases), key=phrases.index)
    per_note = d["plain_bits"] // d["notes"]
    structured = len(distinct) * 7 * per_note + len(phrases) * math.ceil(math.log2(len(distinct)))
    page = render(perform.deadpan(TUNE), piano, 0.8)
    audio = _encoded(page.at_level(LEVEL))
    audio_bits = 8 * audio["WAV"]
    # the page, played exactly and played well
    two = sub_score(0, 4)
    live = perform.expressive(two, phrases=[(0, PHRASE), (PHRASE, 2 * PHRASE)], depth=0.2, ritard=Fraction(1), final=0.5, loud=30.0, seed=4)
    dead = perform.deadpan(two, gate=0.97)
    dv = perform.deviations(live)
    x, tempo = perform.tempo_curve(two, [(0, PHRASE), (PHRASE, 2 * PHRASE)], 0.2, Fraction(1), 0.5)
    a, b = render(live, piano, 0.5), render(dead, piano, 0.5)
    seq = concat([a.at_level(LEVEL), b.at_level(LEVEL)], gap=1.0, names=["A", "B"])
    perf_bits = 42 * (7 + 7 + 5)                                        # per note: when (1 ms in ±64), how long, how loud (32 levels)
    return {"sizes": sizes, "audio": audio, "seconds": page.duration, "plain_bits": d["plain_bits"], "entropy_bits": d["entropy_bits"], "bits_per_note": d["entropy_bits_per_note"],
            "structured_bits": structured, "distinct_phrases": len(distinct), "audio_bits": audio_bits, "ratio": audio_bits / d["plain_bits"],
            "ratio_mp3": 8 * audio.get("MP3", 0) / d["plain_bits"], "perf_bits": perf_bits,
            "ms": dv["ms"], "largest_ms": dv["largest_ms"], "db": [n["db"] for n in live], "db_range": dv["db_range"], "stretch": dv["stretch"],
            "tempo_x": x, "tempo": tempo, "last_ratio": live[-1]["dur"] / live[-1]["page_dur"],
            "times": {"A": [seq.events[f"A.n{k}"] for k in range(14)], "B": [seq.events[f"B.n{k}"] for k in range(14)]}, "quiz_answer": "B",
            "clips": {"pair": save("bits.pair", seq, level=None, detail="the same fourteen notes twice: once exactly as written, once by four rules of performance")}}


def compute_omr() -> dict:
    notes = [(n.pitch.staff_position(), bool(n.dur < SC.H)) for n in TUNE.voices[0].notes]
    img = raster.page(notes)
    lines = raster.staff_lines(img)
    clean_read = raster.read_page(img)
    angles = np.round(np.arange(0.0, 2.01, 0.1), 2)
    naive, fixed = [], []
    for a in angles:
        d = raster.distort(img, float(a))
        naive.append(raster.accuracy(raster.read_page(d), notes))
        fixed.append(raster.accuracy(raster.read_page(raster.deskew(d)[0]), notes))
    levels = [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.1, 0.12]
    speck = [float(np.mean([raster.accuracy(raster.read_page(raster.distort(img, 0.0, s, seed=k)), notes) for k in range(6)])) for s in levels]
    # one bad scan of the first four phrases, read and played back
    short = notes[:28]
    small = raster.page(short)
    pick = None
    for seed in range(200):
        d = raster.distort(small, 0.0, 0.065, seed=seed)
        got = raster.read_page(d)
        acc = raster.accuracy(got, short)
        wrong_pitch = sum(a[0] != b[0] for a, b in zip(got, short)) if len(got) == 28 else 0
        if round((1 - acc) * 28) in (4, 5) and len(got) in (28, 29) and (len(got) == 29 or wrong_pitch >= 1):
            pick = (seed, d, got, acc)
            break
    seed, bad, got, acc = pick
    bottom = P("E4").diatonic
    pitches = [SC.Pitch(SC.STEPS[(bottom + p) % 7], 0, (bottom + p) // 7) for p, _ in got]
    c = render(line(pitches, [1 if f else 2 for _, f in got]), piano, 0.6)
    tilted = raster.distort(img, 1.0)
    level, turned = raster.deskew(tilted)
    wrong = round((1 - acc) * len(short))
    import difflib
    flags = [True] * len(got)                                            # which of the notes read are mistakes
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, got, short, autojunk=False).get_opcodes():
        if tag == "equal":
            for i in range(i1, i2):
                flags[i] = False
    truth_names = [n.pitch.name for n in TUNE.voices[0].notes][:28]
    return {"page": img.astype(np.uint8), "profile": raster.row_profile(img), "lines": lines, "clean_accuracy": raster.accuracy(clean_read, notes),
            "tilted": tilted.astype(np.uint8), "tilted_profile": raster.row_profile(tilted), "levelled": level.astype(np.uint8), "turned": turned,
            "angles": angles, "naive": naive, "deskewed": fixed, "speck_levels": levels, "speck_accuracy": speck,
            "breaks_at": float(angles[int(np.argmax(np.asarray(naive) < 0.5))]),
            "bad": bad.astype(np.uint8), "bad_seed": seed, "bad_accuracy": acc, "bad_notes": len(got), "bad_wrong": wrong, "bad_names": [p.name for p in pitches], "bad_keys": [p.midi for p in pitches], "bad_flags": flags, "bad_beats": [1 if f else 2 for _, f in got], "truth_beats": [1 if f else 2 for _, f in short],
            "truth_names": truth_names, "bad_specks": 0.065,
            "clips": {"read": save("omr.read", c, detail="the Tune as read back from a speckled page")}}


def compute_tune() -> dict:
    notes = perform.deadpan(TUNE, gate=0.97)
    last = sub_score(10, 2)                                              # the sixth phrase, played as a person would
    live = perform.expressive(last, phrases=[(0, PHRASE)], depth=0.14, ritard=Fraction(1), final=0.42, seed=7)
    t0 = notes[35]["t"]
    for k, n in enumerate(live):
        notes[35 + k] = {**n, "t": t0 + n["t"], "page_t": t0 + n["page_t"]}
    c = render(notes, piano, 0.9)
    ev = dict(c.events)
    ev.update({f"phrase{p}": notes[7 * p]["page_t"] for p in range(6)})
    ev["end"] = notes[-1]["t"] + notes[-1]["dur"]
    out = Clip(c.y, SR, ev, [{"t": n["t"], "dur": n["dur"], "hz": n["hz"], "midi": n["midi"], "phrase": k // 7} for k, n in enumerate(notes)]).at_level(LEVEL)
    b = load("bits")
    late = [1000.0 * (n["t"] - n["page_t"]) for n in notes[35:]]
    return {"clip": save("tune.variation10", out, level=None, detail="five phrases exactly as written; the sixth as a player would play it"),
            "seconds": out.duration, "late_ms": late, "db": [n["db"] for n in notes[35:]], "last_ratio": notes[-1]["dur"] / notes[-1]["page_dur"],
            "plain_bits": b["plain_bits"], "ratio": b["ratio"],
            "pairs": [["neumes", "Guido's staff"], ["mensural notes", "tablature"], ["gongche", "jianpu"], ["the staff", "a piano roll"], ["MIDI", "MusicXML"], ["none of them"]]}


def compute_variation() -> dict:
    t = load("tune")
    return {"part": 10, "title": r"in ten notations, and then as none of them says", "seconds": t["seconds"],
            "measure": rf"its page is {t['plain_bits']} bits; its sound, \ " + f"{round(t['ratio'], -3):,.0f}".replace(",", "{,}") + " times as many", "clip": "tune.variation10"}


ITEMS = {"hook": compute_hook, "neumes": compute_neumes, "guido": compute_guido, "mensural": compute_mensural, "score": compute_score, "tab": compute_tab,
         "figured": compute_figured, "east": compute_east, "midi": compute_midi, "xml": compute_xml, "bits": compute_bits, "omr": compute_omr,
         "tune": compute_tune, "variation": compute_variation}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
