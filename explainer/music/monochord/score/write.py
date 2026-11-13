"""Writers: one score, many notations.  Each returns text (or, for MIDI, bytes); what is absent from the output is
what that notation does not record."""

from __future__ import annotations

from fractions import Fraction

from . import ACCIDENTAL, STEPS, Score, value

DIVISIONS = 480          # ticks to a quarter note, in MusicXML and in MIDI


def _ticks(dur: Fraction) -> int:
    t = Fraction(dur) * 4 * DIVISIONS
    if t.denominator != 1:
        raise ValueError(f"{dur} of a whole note is not a whole number of ticks")
    return int(t)


def musicxml(score: Score) -> str:
    """MusicXML (score-partwise): spelling, duration, value, dots, ties, key, metre, clef, words."""
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<score-partwise version="4.0">']
    if score.title:
        out.append(f"  <work><work-title>{score.title}</work-title></work>")
    out.append("  <part-list>")
    for k, v in enumerate(score.voices):
        out.append(f'    <score-part id="P{k + 1}"><part-name>{v.name}</part-name></score-part>')
    out.append("  </part-list>")
    sign = {"treble": ("G", 2), "bass": ("F", 4), "alto": ("C", 3), "tenor": ("C", 4)}
    for k, v in enumerate(score.voices):
        out.append(f'  <part id="P{k + 1}">')
        for m, events in enumerate(score.measures(k)):
            out.append(f'    <measure number="{m + 1}">')
            if m == 0:
                s, line = sign[v.clef]
                out.append(f"      <attributes><divisions>{DIVISIONS}</divisions><key><fifths>{score.key}</fifths></key>"
                           f"<time><beats>{score.time[0]}</beats><beat-type>{score.time[1]}</beat-type></time>"
                           f"<clef><sign>{s}</sign><line>{line}</line></clef></attributes>")
                out.append(f'      <direction><sound tempo="{score.tempo:g}"/></direction>')
            for e in events:
                name, dots = value(e.dur)
                body = "<rest/>" if e.is_rest else (f"<pitch><step>{e.pitch.step}</step>" + (f"<alter>{e.pitch.alter}</alter>" if e.pitch.alter else "")
                                                    + f"<octave>{e.pitch.octave}</octave></pitch>")
                tie = '<tie type="start"/>' if (not e.is_rest and e.tie) else ""
                lyric = f"<lyric><text>{e.lyric}</text></lyric>" if (not e.is_rest and e.lyric) else ""
                out.append(f"      <note>{body}<duration>{_ticks(e.dur)}</duration>{tie}<type>{name}</type>{'<dot/>' * dots}{lyric}</note>")
            out.append("    </measure>")
        out.append("  </part>")
    out.append("</score-partwise>")
    return "\n".join(out) + "\n"


def mei(score: Score) -> str:
    """MEI: the scholars' encoding.  The same facts as MusicXML, arranged as a text to be edited and annotated."""
    dur = {"whole": "1", "half": "2", "quarter": "4", "eighth": "8", "16th": "16", "32nd": "32", "breve": "breve"}
    acc = {-2: "ff", -1: "f", 1: "s", 2: "x"}
    shape = {"treble": ("G", 2), "bass": ("F", 4), "alto": ("C", 3), "tenor": ("C", 4)}
    sig = "0" if score.key == 0 else f"{abs(score.key)}{'s' if score.key > 0 else 'f'}"
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<mei xmlns="http://www.music-encoding.org/ns/mei" meiversion="5.0">',
           f"  <meiHead><fileDesc><titleStmt><title>{score.title}</title></titleStmt><pubStmt/></fileDesc></meiHead>",
           "  <music><body><mdiv><score>",
           f'    <scoreDef keysig="{sig}" meter.count="{score.time[0]}" meter.unit="{score.time[1]}"><staffGrp>']
    for k, v in enumerate(score.voices):
        s, line = shape[v.clef]
        out.append(f'      <staffDef n="{k + 1}" lines="5" clef.shape="{s}" clef.line="{line}"/>')
    out.append("    </staffGrp></scoreDef>")
    out.append("    <section>")
    bars = [score.measures(k) for k in range(len(score.voices))]
    for m in range(max(len(b) for b in bars)):
        out.append(f'      <measure n="{m + 1}">')
        for k, b in enumerate(bars):
            if m >= len(b):
                continue
            items = []
            for e in b[m]:
                name, dots = value(e.dur)
                d = f'dur="{dur[name]}"' + (f' dots="{dots}"' if dots else "")
                if e.is_rest:
                    items.append(f"<rest {d}/>")
                else:
                    a = f' accid="{acc[e.pitch.alter]}"' if e.pitch.alter else ""
                    t = ' tie="i"' if e.tie else ""
                    items.append(f'<note pname="{e.pitch.step.lower()}" oct="{e.pitch.octave}" {d}{a}{t}/>')
            out.append(f'        <staff n="{k + 1}"><layer n="1">{"".join(items)}</layer></staff>')
        out.append("      </measure>")
    out += ["    </section>", "  </score></mdiv></body></music>", "</mei>"]
    return "\n".join(out) + "\n"


def _varlen(n: int) -> bytes:
    out = [n & 0x7F]
    n >>= 7
    while n:
        out.append((n & 0x7F) | 0x80)
        n >>= 7
    return bytes(reversed(out))


def midi(score: Score, velocity: int = 80, gate: float = 1.0) -> bytes:
    """A Standard MIDI File (format 0): which key goes down, when, how hard, and when it comes up.  No spelling, no
    note values, no barlines; the metre and key are kept only as optional remarks."""
    events = []            # (tick, order, bytes)
    for ch, v in enumerate(score.voices):
        held = None
        for t, e in v.onsets():
            if e.is_rest:
                continue
            start, length = _ticks(t), _ticks(e.dur)
            if held is not None and held[0] == e.pitch.midi:          # the second half of a tie: keep the key down
                events = [x for x in events if x is not held[1]]
                off = (start + int(length * gate), 0, bytes([0x80 | ch, e.pitch.midi, 0]))
                events.append(off)
                held = (e.pitch.midi, off) if e.tie else None
                continue
            events.append((start, 1, bytes([0x90 | ch, e.pitch.midi, velocity])))
            off = (start + int(length * gate), 0, bytes([0x80 | ch, e.pitch.midi, 0]))
            events.append(off)
            held = (e.pitch.midi, off) if e.tie else None
    events.sort(key=lambda x: (x[0], x[1]))
    us = int(round(60_000_000 / score.tempo))
    track = bytearray()
    track += _varlen(0) + bytes([0xFF, 0x51, 0x03]) + us.to_bytes(3, "big")
    track += _varlen(0) + bytes([0xFF, 0x58, 0x04, score.time[0], {1: 0, 2: 1, 4: 2, 8: 3, 16: 4}[score.time[1]], 24, 8])
    track += _varlen(0) + bytes([0xFF, 0x59, 0x02, score.key & 0xFF, 0])
    now = 0
    for tick, _, data in events:
        track += _varlen(tick - now) + data
        now = tick
    track += _varlen(0) + bytes([0xFF, 0x2F, 0x00])
    head = b"MThd" + (6).to_bytes(4, "big") + (0).to_bytes(2, "big") + (1).to_bytes(2, "big") + DIVISIONS.to_bytes(2, "big")
    return head + b"MTrk" + len(track).to_bytes(4, "big") + bytes(track)


def abc(score: Score, voice: int = 0) -> str:
    """ABC: a folk musician's notation, typed on one line."""
    unit = Fraction(1, 8) if score.bar < Fraction(3, 4) else Fraction(1, 4)
    key = {0: "C", 1: "G", 2: "D", 3: "A", 4: "E", 5: "B", 6: "F#", 7: "C#", -1: "F", -2: "Bb", -3: "Eb", -4: "Ab", -5: "Db", -6: "Gb", -7: "Cb"}[score.key]
    sharps = {s: 1 for s in "FCGDAEB"[: max(score.key, 0)]}
    sharps.update({s: -1 for s in "BEADGCF"[: max(-score.key, 0)]})

    def note(e):
        mult = e.dur / unit
        length = "" if mult == 1 else (str(mult.numerator) if mult.denominator == 1 else f"{mult.numerator if mult.numerator != 1 else ''}/{mult.denominator}")
        if e.is_rest:
            return "z" + length
        p = e.pitch
        acc = "" if p.alter == sharps.get(p.step, 0) else {-2: "__", -1: "_", 0: "=", 1: "^", 2: "^^"}[p.alter]
        letter = p.step if p.octave <= 4 else p.step.lower()
        marks = "," * max(4 - p.octave, 0) + "'" * max(p.octave - 5, 0)
        return acc + letter + marks + length + ("-" if e.tie else "")

    bars = [" ".join(note(e) for e in m) for m in score.measures(voice)]
    head = f"X:1\nT:{score.title}\nM:{score.time[0]}/{score.time[1]}\nL:{unit.numerator}/{unit.denominator}\nQ:1/4={score.tempo:g}\nK:{key}\n"
    return head + " | ".join(bars) + " |]\n"


def lilypond(score: Score, voice: int = 0) -> str:
    """LilyPond input: a score as a program for an engraver."""
    dur = {"whole": "1", "half": "2", "quarter": "4", "eighth": "8", "16th": "16", "32nd": "32"}

    def note(e):
        name, dots = value(e.dur)
        d = dur[name] + "." * dots
        if e.is_rest:
            return "r" + d
        p = e.pitch
        marks = "'" * max(p.octave - 3, 0) + "," * max(3 - p.octave, 0)
        return p.step.lower() + {-2: "eses", -1: "es", 0: "", 1: "is", 2: "isis"}[p.alter] + marks + d + ("~" if e.tie else "")

    bars = [" ".join(note(e) for e in m) for m in score.measures(voice)]
    return "{ \\time " + f"{score.time[0]}/{score.time[1]} " + " | ".join(bars) + ' \\bar "|." }\n'


def jianpu(score: Score, voice: int = 0, tonic=None) -> str:
    """Numbered notation (jianpu), as plain text: degrees of the scale as digits, a dash for each further beat a note
    is held, an apostrophe for the octave above and a comma for the octave below, bars as in staff notation.  The
    key is stated once (``1=C``); the same digits serve in every key."""
    from . import Pitch, degree_pitch

    line = {0: "C", 1: "G", 2: "D", 3: "A", 4: "E", 5: "B", -1: "F", -2: "Bb", -3: "Eb", -4: "Ab", -5: "Db"}
    ton = tonic or Pitch.parse(line[score.key] + "4")
    beat = Fraction(1, score.time[1])

    def digit(p):
        rel = p.diatonic - ton.diatonic
        octave, deg = divmod(rel, 7)
        natural = degree_pitch(deg + 1, Pitch(ton.step, ton.alter, ton.octave + octave))
        acc = {0: "", 1: "#", -1: "b"}.get(p.midi - natural.midi, "?")
        return acc + str(deg + 1) + ("'" * octave if octave > 0 else "," * (-octave))

    bars = []
    for m in score.measures(voice):
        cells = []
        for e in m:
            n = e.dur / beat
            head = "0" if e.is_rest else digit(e.pitch)
            if n >= 1:
                cells.append(head + " -" * (int(n) - 1) + ("." if n - int(n) == Fraction(1, 2) else ""))
            else:
                cells.append(head + "_" * {Fraction(1, 2): 1, Fraction(1, 4): 2}.get(n, 3))
        bars.append(" ".join(cells))
    return f"1={line[score.key]}  {score.time[0]}/{score.time[1]}  " + " | ".join(bars) + " ||"


def solfege(score: Score, voice: int = 0) -> str:
    """Guido's syllables (with the modern do and ti): pitch as a place in the scale, with no rhythm at all."""
    names = ("do", "re", "mi", "fa", "sol", "la", "ti")
    from . import Pitch
    line = {0: "C", 1: "G", 2: "D", 3: "A", 4: "E", 5: "B", -1: "F", -2: "Bb", -3: "Eb", -4: "Ab", -5: "Db"}
    ton = Pitch.parse(line[score.key] + "4")
    return " ".join(names[(e.pitch.diatonic - ton.diatonic) % 7] for e in score.voices[voice].events if not e.is_rest)
