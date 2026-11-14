"""Fourteenth-century polyphony as data: what Part 23 counts.

The table ``data/trecento.json.gz`` holds, for each piece, its title, composer, metre and the notes of each voice as
(key number, onset, duration) with times in 24ths of a quarter note of the modern edition.  It was derived once by
:func:`extract` from the MusicXML encodings in the music21 corpus (``music21/corpus/trecento/*``, encoded by
M. S. Cuthbert's students from *Polyphonic Music of the Fourteenth Century*, and ``ciconia``), as Part 17's chorales
were; the music is medieval and in the public domain, and only pitches and times are kept, no encoding.  The pitches
include the editors' accidentals (*musica ficta*), which the manuscripts do not write: chapter 12 of Part 23 is about
exactly that.

    from explainer.music.monochord import trecento
    book = trecento.load()            # a list of Piece
    book[0].grid(2)                   # the voices sampled every eighth note of the edition
"""

from __future__ import annotations

import gzip
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

TICKS = 24                                                         # per quarter note of the edition
DATA = Path(__file__).with_name("data") / "trecento.json.gz"
STEPS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


@dataclass
class Piece:
    name: str                                                     # the file's name, e.g. "PMFC_06-Jacopo-02-Con-Gran-Furor"
    title: str
    composer: str
    time: tuple                                                   # (beats, beat type) at the start
    bar: int                                                      # ticks in the first bar
    voices: list = field(default_factory=list)                    # top to bottom: lists of (key, onset, duration)

    @property
    def length(self) -> int:
        return max(o + d for v in self.voices for _, o, d in v)

    @property
    def genre(self) -> str:
        t = (self.title + " " + self.name).lower()
        for g in ("gloria", "credo", "kyrie", "sanctus", "agnus", "madrigal", "ballata", "caccia"):
            if g in t:
                return g
        return "other"

    def grid(self, per_quarter: int = 1) -> np.ndarray:
        """The voices sampled at a regular grid, shape (n, voices); -1 is a rest."""
        step = TICKS // per_quarter
        n = self.length // step
        out = -np.ones((n, len(self.voices)), dtype=int)
        for j, v in enumerate(self.voices):
            for p, o, d in v:
                out[o // step:(o + d + step - 1) // step, j] = p
        return out

    def onsets(self) -> list[int]:
        return sorted({o for v in self.voices for _, o, _ in v})

    def final(self) -> tuple:
        """The last sonority: the last note of every voice."""
        return tuple(v[-1][0] for v in self.voices if v)


def composer_of(name: str, composer: str) -> str:
    """A clean composer name: dates and sources dropped; volume 24 of PMFC is Ciconia's; blank means anonymous."""
    c = re.sub(r"\(.*?\)", "", composer or "", flags=re.S)
    c = " ".join(c.split()).strip()
    c = re.sub(r"\s+[A-Z]{1,2}-[A-Za-z]+.*$", "", c)                  # a manuscript siglum after the name
    if c.lower().startswith("anonymous") or c.lower().startswith("anon"):
        c = "anonymous"
    if not c:
        c = "Johannes Ciconia" if name.startswith("PMFC_24") else "anonymous"
    if "ciconia" in c.lower():
        c = "Johannes Ciconia"
    return c


def load(path: Path = DATA) -> list[Piece]:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        raw = json.load(f)
    return [Piece(r["name"], " ".join(r["title"].split()), composer_of(r["name"], r["composer"]), tuple(r["time"]), r["bar"],
                  [[tuple(n) for n in v] for v in r["voices"]]) for r in raw]


# ---------------------------------------------------------------------------
# Extraction (run once, from a copy of the music21 corpus)
# ---------------------------------------------------------------------------
def _midi(n) -> int:
    step = n.findtext("pitch/step")
    alter = int(round(float(n.findtext("pitch/alter") or 0)))
    octave = int(n.findtext("pitch/octave"))
    return 12 * (octave + 1) + STEPS[step] + alter


def parse_musicxml(text: str, name: str) -> Piece | None:
    """A piece from partwise MusicXML: every part with notes, its first voice only (chords keep their top note, grace
    notes are skipped, tied notes merged)."""
    root = ET.fromstring(text)
    title = (root.findtext("work/work-title") or root.findtext("movement-title") or name).strip()
    composer = ""
    for c in root.findall("identification/creator"):
        if c.get("type") == "composer":
            composer = (c.text or "").strip()
    time, bar = (4, 4), 0
    voices = []
    for j, part in enumerate(root.findall("part")):
        notes, t, divisions = [], 0, 1
        for k, measure in enumerate(part.findall("measure")):
            a = measure.find("attributes")
            if a is not None:
                divisions = int(a.findtext("divisions") or divisions)
                if j == 0 and k == 0 and a.find("time") is not None:
                    try:
                        time = (int(a.findtext("time/beats")), int(a.findtext("time/beat-type")))
                    except (TypeError, ValueError):
                        pass
            t0 = t
            for el in measure:
                if el.tag == "backup":
                    t -= int(el.findtext("duration")) * TICKS // divisions
                elif el.tag == "forward":
                    t += int(el.findtext("duration")) * TICKS // divisions
                elif el.tag == "note":
                    if el.find("grace") is not None or el.findtext("duration") is None:
                        continue
                    d = int(el.findtext("duration")) * TICKS // divisions
                    if (el.findtext("voice") or "1") != "1":
                        if el.find("chord") is None:
                            t += d
                        continue
                    if el.find("chord") is not None:
                        continue
                    if el.find("rest") is None and el.find("pitch") is not None:
                        p = _midi(el)
                        tied = any(x.get("type") == "stop" for x in el.findall("tie"))
                        if tied and notes and notes[-1][0] == p and notes[-1][1] + notes[-1][2] == t:
                            q, o, dd = notes[-1]
                            notes[-1] = (q, o, dd + d)
                        else:
                            notes.append((p, t, d))
                    t += d
            if j == 0 and k == 0:
                bar = t - t0
        if notes:
            voices.append(notes)
    if len(voices) < 2:
        return None
    # top to bottom by average pitch
    voices.sort(key=lambda v: -np.mean([p for p, _, _ in v]))
    return Piece(name, title, composer, time, bar, voices)


def extract(wheel: str | Path, out: Path = DATA) -> int:
    """Read every ``music21/corpus/trecento/*.xml`` (an .mxl where there is no .xml) and the Ciconia in a music21 wheel,
    and write the table."""
    z = zipfile.ZipFile(Path(wheel))
    names = z.namelist()
    files = {}
    for n in sorted(names):
        if (n.startswith("music21/corpus/trecento/") or n.startswith("music21/corpus/ciconia/")) and n.endswith(".xml"):
            files[Path(n).stem] = z.read(n).decode("utf-8", "ignore")
    for n in sorted(names):
        if n.startswith("music21/corpus/trecento/") and n.endswith(".mxl") and Path(n).stem not in files:
            inner = zipfile.ZipFile(__import__("io").BytesIO(z.read(n)))
            xml = [m for m in inner.namelist() if m.endswith(".xml") and not m.startswith("META-INF")]
            if xml:
                files[Path(n).stem] = inner.read(xml[0]).decode("utf-8", "ignore")
    rows, seen = [], set()
    for name, text in files.items():
        text = re.sub(r"<!DOCTYPE[^>]*>", "", text)
        try:
            pc = parse_musicxml(text, name)
        except ET.ParseError:
            continue
        if pc is None:
            continue
        key = tuple(pc.voices[0][:20])
        if key in seen:                                                # the same piece encoded twice
            continue
        seen.add(key)
        rows.append({"name": pc.name, "title": pc.title, "composer": pc.composer, "time": list(pc.time), "bar": pc.bar,
                     "voices": [[list(n) for n in v] for v in pc.voices]})
    with gzip.open(out, "wt", encoding="utf-8") as f:
        json.dump(rows, f, separators=(",", ":"))
    return len(rows)


if __name__ == "__main__":
    import sys

    print(extract(sys.argv[1]), "pieces")
