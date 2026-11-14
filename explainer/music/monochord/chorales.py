"""Bach's four-part chorales as data: what Part 17 counts, harmonizes and tests against.

The table ``data/chorales.json.gz`` holds, for each chorale, its key signature, mode and metre, the start of every
bar, and the notes of the four voices as (key number, onset, duration, fermata) with times in 24ths of a quarter
note.  It was derived once by :func:`extract` from the MusicXML encodings in the music21 corpus
(``music21/corpus/bach/*.mxl``, M. S. Cuthbert and others), keeping only chorales with exactly four voices; the
music is Bach's and in the public domain, and only pitches, times and fermatas are kept, no encoding.

    from explainer.music.monochord import chorales
    book = chorales.load()           # a list of Chorale
    book[0].grid(2)                  # the four voices sampled every eighth note
"""

from __future__ import annotations

import gzip
import io
import json
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

TICKS = 24                                                         # per quarter note
DATA = Path(__file__).with_name("data") / "chorales.json.gz"
STEPS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
VOICES = ("soprano", "alto", "tenor", "bass")


@dataclass
class Chorale:
    name: str                                                     # e.g. "bwv66.6"
    fifths: int                                                   # key signature: sharps (+) or flats (-)
    mode: str                                                     # "major" or "minor" as encoded (may be "")
    time: tuple                                                   # (beats, beat type)
    bars: list                                                    # bar starts, in ticks (a pickup bar starts below 0)
    voices: list = field(default_factory=list)                    # four lists of (key, onset, duration, fermata)

    @property
    def length(self) -> int:
        return max(o + d for v in self.voices for _, o, d, _ in v)

    @property
    def tonic(self) -> int:
        """The pitch class of home: the key signature's major tonic, or its relative minor."""
        major = (7 * self.fifths) % 12
        return (major + 9) % 12 if self.mode == "minor" else major

    def sounding(self, voice: int, t: int):
        for p, o, d, _ in self.voices[voice]:
            if o <= t < o + d:
                return p
        return None

    def grid(self, per_quarter: int = 1) -> np.ndarray:
        """The four voices sampled at a regular grid (``per_quarter`` points a quarter note), shape (n, 4); -1 is a
        rest."""
        step = TICKS // per_quarter
        n = self.length // step
        out = -np.ones((n, 4), dtype=int)
        for j, v in enumerate(self.voices):
            for p, o, d, _ in v:
                out[o // step:(o + d + step - 1) // step, j] = p
        return out

    def beats(self) -> list:
        """The chords on the beats (quarter notes, or the beat of the metre): (tick, (s, a, t, b), fermata)."""
        beat = TICKS * 4 // self.time[1]
        if self.time[1] == 8 and self.time[0] % 3 == 0:
            beat *= 3
        out = []
        ferm = {o for v in self.voices for _, o, _, f in v if f}
        first = min(o for _, o, _, _ in self.voices[0])
        for t in range(first, self.length, beat):
            ch = tuple(self.sounding(j, t) for j in range(4))
            if None not in ch:
                out.append((t, ch, any(t <= f < t + beat for f in ferm)))
        return out

    def phrases(self) -> list:
        """Phrase ends: the onsets of the soprano's notes under a fermata."""
        return [o for _, o, _, f in self.voices[0] if f]


def melody_key(c: Chorale, n: int = 8) -> tuple:
    """A fingerprint of a chorale's tune: the first ``n`` moves of its soprano on the beats, repeated notes merged,
    so that the same tune in another key or with other passing notes has the same key."""
    s = [ch[0] for _, ch, _ in c.beats()]
    s = [x for i, x in enumerate(s) if i == 0 or x != s[i - 1]]
    return tuple(s[i + 1] - s[i] for i in range(min(n, len(s) - 1)))


def tunes(book) -> dict:
    """The chorales grouped by tune: {fingerprint: [chorale, ...]}."""
    out: dict = {}
    for c in book:
        out.setdefault(melody_key(c), []).append(c)
    return out


def split(book, every: int = 5, offset: int = 0) -> tuple[list, list]:
    """Train and test chorales, split by tune (every ``every``-th tune is held out), so that no tune in the test set
    has been seen, in any setting, in training."""
    groups = sorted(tunes(book).values(), key=lambda g: g[0].name)
    test = [c for k, g in enumerate(groups) if k % every == offset for c in g]
    names = {c.name for c in test}
    return [c for c in book if c.name not in names], test


def load(path: Path = DATA) -> list[Chorale]:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        raw = json.load(f)
    return [Chorale(r["name"], r["fifths"], r["mode"], tuple(r["time"]), r["bars"], [[tuple(n) for n in v] for v in r["voices"]]) for r in raw]


# ---------------------------------------------------------------------------
# Extraction (run once, from a copy of the music21 corpus)
# ---------------------------------------------------------------------------
def _midi(n) -> int:
    step = n.findtext("pitch/step")
    alter = int(float(n.findtext("pitch/alter") or 0))
    octave = int(n.findtext("pitch/octave"))
    return 12 * (octave + 1) + STEPS[step] + alter


def parse_musicxml(text: str, name: str) -> Chorale | None:
    """A chorale from partwise MusicXML: four parts, one voice each (a second note in a chord is dropped, grace notes
    are skipped, tied notes merged).  None if the file does not have exactly four parts."""
    root = ET.fromstring(text)
    parts = root.findall("part")
    if len(parts) != 4:
        return None
    fifths, mode, time = 0, "", (4, 4)
    voices, bars = [], []
    for j, part in enumerate(parts):
        notes, t, divisions = [], 0, 1
        starts = []
        for measure in part.findall("measure"):
            a = measure.find("attributes")
            if a is not None:
                divisions = int(a.findtext("divisions") or divisions)
                if j == 0 and a.find("key") is not None and not starts:
                    fifths = int(a.findtext("key/fifths"))
                    mode = a.findtext("key/mode") or ""
                if j == 0 and a.find("time") is not None and not starts:
                    time = (int(a.findtext("time/beats")), int(a.findtext("time/beat-type")))
            starts.append(t)
            for el in measure:
                if el.tag == "backup":
                    t -= int(el.findtext("duration")) * TICKS // divisions
                elif el.tag == "forward":
                    t += int(el.findtext("duration")) * TICKS // divisions
                elif el.tag == "note":
                    if el.find("grace") is not None:
                        continue
                    if (el.findtext("voice") or "1") != "1":
                        if el.find("chord") is None:
                            t += int(el.findtext("duration")) * TICKS // divisions
                        continue
                    if el.find("chord") is not None:
                        continue
                    d = int(el.findtext("duration")) * TICKS // divisions
                    if el.find("rest") is None:
                        p = _midi(el)
                        ferm = el.find("notations/fermata") is not None
                        tied = any(x.get("type") == "stop" for x in el.findall("tie"))
                        if tied and notes and notes[-1][0] == p and notes[-1][1] + notes[-1][2] == t:
                            q, o, dd, f = notes[-1]
                            notes[-1] = (q, o, dd + d, f or ferm)
                        else:
                            notes.append((p, t, d, ferm))
                    t += d
        voices.append(notes)
        if j == 0:
            bars = starts
    bar_len = TICKS * 4 * time[0] // time[1]
    if len(bars) > 1 and bars[1] - bars[0] < bar_len:              # a pickup bar: count from where it would have begun
        shift = bar_len - (bars[1] - bars[0])
        voices = [[(p, o + shift, d, f) for p, o, d, f in v] for v in voices]
        bars = [0] + [b + shift for b in bars[1:]]
        bars[0] = 0
    return Chorale(name, fifths, mode, time, bars, voices)


def extract(wheel: str | Path, out: Path = DATA) -> int:
    """Read every ``music21/corpus/bach/*.mxl`` in a music21 wheel (or directory) and write the table."""
    wheel = Path(wheel)
    files = {}
    if wheel.is_dir():
        for f in sorted(wheel.glob("*.mxl")):
            files[f.stem] = f.read_bytes()
    else:
        z = zipfile.ZipFile(wheel)
        for n in sorted(z.namelist()):
            if n.startswith("music21/corpus/bach/") and n.endswith(".mxl"):
                files[Path(n).stem] = z.read(n)
    rows = []
    for name, data in files.items():
        m = zipfile.ZipFile(io.BytesIO(data))
        xml = [n for n in m.namelist() if n.endswith((".xml", ".musicxml")) and not n.startswith("META")]
        if not xml:
            continue
        try:
            c = parse_musicxml(m.read(xml[0]).decode("utf-8"), name)
        except (ET.ParseError, ValueError, KeyError, TypeError):
            continue
        if c is None or any(len(v) < 8 for v in c.voices):
            continue
        rows.append({"name": c.name, "fifths": c.fifths, "mode": c.mode, "time": list(c.time), "bars": c.bars,
                     "voices": [[list(map(int, n[:3])) + [int(n[3])] for n in v] for v in c.voices]})
    out.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(out, "wt", encoding="utf-8") as f:
        json.dump(rows, f, separators=(",", ":"))
    return len(rows)


if __name__ == "__main__":
    import sys

    print(extract(sys.argv[1]), "chorales")
