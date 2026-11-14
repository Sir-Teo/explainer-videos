"""The Baroque as programs: what Part 25 computes.

    Galilei      a string's pitch against its tension: the weights for an octave are 4:1, not 2:1.
    Corpus       a few Baroque pieces kept as lines: Corelli's trio-sonata Grave, Handel's aria, from the music21
                 corpus's encodings (``data/baroque.json.gz``).
    Figures      the figures a continuo player would read, worked out from the upper parts; realized again by Part 10's
                 realizer and compared with what the composer wrote.
    Ritornello   returns of an opening theme anywhere, at any transposition.
    Keys         the major third and fifth of every key in a temperament: key character as arithmetic.
    Ornaments    trills, mordents, appoggiaturas, turns; notes inégales and double-dotting as rhythm transforms.

    from explainer.music.monochord import baroque as B
    B.weights_for(2.0)                     # 4.0
"""

from __future__ import annotations

import gzip
import io
import json
import math
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np

from .tuning import Tuning

TICKS = 24
DATA = Path(__file__).with_name("data") / "baroque.json.gz"
STEPS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


# ---------------------------------------------------------------------------
# Galilei: tension and pitch
# ---------------------------------------------------------------------------
def string_hz(tension: float, length: float = 0.65, mass_per_m: float = 6.0e-4) -> float:
    """Mersenne's law (1636): f = sqrt(T / mu) / 2L."""
    return math.sqrt(tension / mass_per_m) / (2.0 * length)


def weights_for(ratio: float) -> float:
    """The ratio of hanging weights that makes two equal strings sound a frequency ratio: its square."""
    return ratio ** 2


# ---------------------------------------------------------------------------
# Corpus: pieces as lines
# ---------------------------------------------------------------------------
def _midi(n) -> int:
    return 12 * (int(n.findtext("pitch/octave")) + 1) + STEPS[n.findtext("pitch/step")] + int(round(float(n.findtext("pitch/alter") or 0)))


def parse_lines(text: str) -> dict:
    """Every (part, staff) of a partwise MusicXML file as one line of (key number, onset, duration) in 24ths of a
    quarter: chords keep their top note on an upper staff and their bottom note on a lower one; ties are merged;
    other voices on the staff are dropped where they overlap."""
    root = ET.fromstring(text)
    names = {sp.get("id"): (sp.findtext("part-name") or "").strip() for sp in root.iter("score-part")}
    lines = {}
    for part in root.findall("part"):
        pid = part.get("id")
        t, divisions = 0, 1
        cur = {}
        last_start = {}
        for measure in part.findall("measure"):
            a = measure.find("attributes")
            if a is not None and a.findtext("divisions"):
                divisions = int(a.findtext("divisions"))
            for el in measure:
                if el.tag == "backup":
                    t -= int(el.findtext("duration")) * TICKS // divisions
                elif el.tag == "forward":
                    t += int(el.findtext("duration")) * TICKS // divisions
                elif el.tag == "note":
                    if el.find("grace") is not None or el.findtext("duration") is None:
                        continue
                    d = int(el.findtext("duration")) * TICKS // divisions
                    staff = el.findtext("staff") or "1"
                    key = (pid, staff)
                    chord = el.find("chord") is not None
                    onset = last_start.get(key, t) if chord else t
                    if el.find("rest") is None and el.find("pitch") is not None:
                        p = _midi(el)
                        notes = cur.setdefault(key, [])
                        tied = any(x.get("type") == "stop" for x in el.findall("tie"))
                        if chord and notes and notes[-1][1] == onset:
                            q, o, dd = notes[-1]
                            keep = max(q, p) if staff == "1" else min(q, p)
                            notes[-1] = (keep, o, dd)
                        elif tied and notes and notes[-1][0] == p and notes[-1][1] + notes[-1][2] == onset:
                            q, o, dd = notes[-1]
                            notes[-1] = (q, o, dd + d)
                        elif notes and notes[-1][1] + notes[-1][2] > onset:
                            pass                                          # an overlapping second voice: dropped
                        else:
                            notes.append((p, onset, d))
                    if not chord:
                        last_start[key] = t
                        t += d
        for (pid_, staff), notes in cur.items():
            label = names.get(pid_, pid_) + ("" if staff == "1" else f" (staff {staff})")
            lines[label] = notes
    return lines


def extract(wheel, out: Path = DATA) -> int:
    z = zipfile.ZipFile(Path(wheel))
    wanted = {"corelli": "music21/corpus/corelli/opus3no1/1grave.xml", "handel": "music21/corpus/handel/rinaldo/Lascia_chio_pianga.mxl"}
    rows = []
    for name, path in wanted.items():
        raw = z.read(path)
        if path.endswith(".mxl"):
            inner = zipfile.ZipFile(io.BytesIO(raw))
            xml = [m for m in inner.namelist() if m.endswith(".xml") and not m.startswith("META-INF")][0]
            raw = inner.read(xml)
        enc = "utf-16" if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else "utf-8"
        text = re.sub(r"<\?xml[^>]*\?>", "", raw.decode(enc, "ignore"))
        text = re.sub(r"<!DOCTYPE[^>]*>", "", text)
        lines = parse_lines(text)
        rows.append({"name": name, "lines": {k: [list(n) for n in v] for k, v in lines.items()}})
    with gzip.open(out, "wt", encoding="utf-8") as f:
        json.dump(rows, f, separators=(",", ":"))
    return len(rows)


def load(path: Path = DATA) -> dict:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        raw = json.load(f)
    return {r["name"]: {k: [tuple(n) for n in v] for k, v in r["lines"].items()} for r in raw}


def sounding(line, t: int):
    for p, o, d in line:
        if o <= t < o + d:
            return p
        if o > t:
            return None
    return None


# ---------------------------------------------------------------------------
# Figures from the upper parts
# ---------------------------------------------------------------------------
def figure_of(bass: int, uppers) -> str:
    """The figure a continuo player would need for these upper notes over this bass, from their intervals in
    semitones: '' for a root-position triad (or less), 6, 6/4, 7, 6/5, 4/3, 4/2; a sharp or flat third is left to the
    key (the realizer works in the key)."""
    ics = {(u - bass) % 12 for u in uppers if u is not None and u > bass}
    third = bool(ics & {3, 4})
    fourth = 5 in ics
    fifth = 7 in ics or 6 in ics
    sixth = bool(ics & {8, 9})
    seventh = bool(ics & {10, 11})
    second = bool(ics & {1, 2})
    if seventh:
        return "7"
    if second and fourth:
        return "4/2"
    if sixth and fifth:
        return "6/5"
    if sixth and fourth and third:
        return "4/3"
    if sixth and fourth:
        return "6/4"
    if sixth:
        return "6"
    return ""


def figured_line(bass, uppers) -> list[tuple]:
    """For every note of the bass: (bass note, onset, duration, figure from what the upper parts sound at its onset)."""
    return [(p, o, d, figure_of(p, [sounding(u, o) for u in uppers])) for p, o, d in bass]


def agreement(realized, bass, uppers) -> dict:
    """How far a realization's chords agree with the composer's upper parts, onset by onset: the share of the
    composer's pitch classes that the realization also has, and how often the top notes coincide."""
    shared = total = tops = 0
    for ch, (p, o, d) in zip(realized, bass):
        real = [sounding(u, o) for u in uppers]
        real = [x for x in real if x is not None]
        if not real:
            continue
        want = {x % 12 for x in real}
        have = {x % 12 for x in ch}
        shared += len(want & have)
        total += len(want)
        tops += int(max(ch) % 12 == max(real) % 12)
    return {"pitch_classes": shared / max(total, 1), "top": tops / max(len(bass), 1)}


# ---------------------------------------------------------------------------
# Ritornello: returns of an opening theme, at any transposition
# ---------------------------------------------------------------------------
def intervals(line) -> list[int]:
    ps = [p for p, _, _ in line]
    return [b - a for a, b in zip(ps, ps[1:])]


def ritornello_returns(line, head: int = 8, tolerance: int = 1, gap: int = 4) -> list[dict]:
    """Every place where the line's first ``head`` melodic intervals come back (allowing ``tolerance`` mismatches),
    with the transposition and the onset; later returns must be at least ``gap`` notes apart."""
    iv = intervals(line)
    probe = iv[:head]
    out = []
    k = 0
    while k + head <= len(iv):
        miss = sum(1 for a, b in zip(iv[k:k + head], probe) if a != b)
        if miss <= tolerance and (not out or k - out[-1]["index"] >= gap):
            out.append({"index": k, "onset": line[k][1], "transpose": line[k][0] - line[0][0], "misses": miss})
            k += head
        else:
            k += 1
    return out


# ---------------------------------------------------------------------------
# Keys in a temperament
# ---------------------------------------------------------------------------
KEY_NAMES = ("C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B")


def key_colours(t: Tuning) -> list[dict]:
    """For every major key: its major third and fifth in cents (from the tonic up), and how far each is from pure."""
    out = []
    for k, name in enumerate(KEY_NAMES):
        c0 = t.cents[k]
        third = (t.cents[(k + 4) % 12] - c0) % 1200
        fifth = (t.cents[(k + 7) % 12] - c0) % 1200
        out.append({"key": name, "third": third, "fifth": fifth, "third_error": third - 1200 * math.log2(5 / 4),
                    "fifth_error": fifth - 1200 * math.log2(3 / 2)})
    return out


# ---------------------------------------------------------------------------
# Ornaments and rhythm transforms
# ---------------------------------------------------------------------------
def trill(p: int, onset: float, dur: float, upper: int = 2, n: int = 8, turn: bool = True) -> list[tuple]:
    """A Baroque trill: starting on the upper note, alternating, ending on the main note (with a turn below if
    ``turn``)."""
    k = n + (2 if turn else 0)
    step = dur / k
    out = []
    for i in range(n):
        out.append((p + upper if i % 2 == 0 else p, onset + i * step, step))
    if turn:
        out += [(p - (1 if (p % 12) in (0, 5) else 2), onset + n * step, step), (p, onset + (n + 1) * step, step)]
    out[-1] = (out[-1][0], out[-1][1], dur - (out[-1][1] - onset))
    return out


def mordent(p: int, onset: float, dur: float, lower: int = 1) -> list[tuple]:
    s = min(dur / 4, 0.125)
    return [(p, onset, s), (p - lower, onset + s, s), (p, onset + 2 * s, dur - 2 * s)]


def appoggiatura(p: int, onset: float, dur: float, from_above: int = 2) -> list[tuple]:
    """On the beat, taking half the note's value (the usual rule for an undotted note)."""
    return [(p + from_above, onset, dur / 2), (p, onset + dur / 2, dur / 2)]


def inegale(notes, ratio: float = 2.0, unit: float = 0.5) -> list[tuple]:
    """Notes inégales: pairs of equal short notes (each ``unit`` long, beginning on a multiple of 2*unit) played long
    then short in ``ratio``."""
    out = []
    for p, o, d in notes:
        if abs(d - unit) < 1e-9:
            pos = (o / unit) % 2
            if abs(pos) < 1e-9:
                d2 = 2 * unit * ratio / (ratio + 1)
                out.append((p, o, d2))
                continue
            if abs(pos - 1) < 1e-9:
                d1 = 2 * unit * ratio / (ratio + 1)
                out.append((p, o - unit + d1, 2 * unit - d1))
                continue
        out.append((p, o, d))
    return out


def double_dot(notes, short: float = 0.5) -> list[tuple]:
    """Overdotting: a dotted note followed by its short partner is lengthened so the partner is half as long."""
    out = list(notes)
    for i in range(len(out) - 1):
        p, o, d = out[i]
        q, o2, d2 = out[i + 1]
        if abs(d2 - short) < 1e-9 and abs(d - 3 * short) < 1e-9 and abs(o + d - o2) < 1e-9:
            out[i] = (p, o, d + short / 2)
            out[i + 1] = (q, o2 + short / 2, short / 2)
    return out


DANCES = {
    "allemande": {"metre": "4/4", "tempo": "moderate", "pattern": [0.5, 0.5, 0.5, 0.5, 1, 1], "pickup": 0.25},
    "courante": {"metre": "3/2", "tempo": "moderate, shifting between 3/2 and 6/4", "pattern": [1.5, 0.5, 1, 1, 2], "pickup": 0.5},
    "sarabande": {"metre": "3/4", "tempo": "slow, weight on the second beat", "pattern": [1, 2, 1, 1, 1], "pickup": 0.0},
    "gigue": {"metre": "6/8", "tempo": "fast", "pattern": [0.75, 0.25, 0.5, 0.75, 0.25, 0.5], "pickup": 0.0},
}
