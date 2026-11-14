"""Sixteenth-century polyphony as data: what Part 24 counts.

The table ``data/renaissance.json.gz`` holds Palestrina's Mass movements and Monteverdi's madrigals (Books 3 to 5), each
as its title, composer, work, metre and the notes of each voice, top to bottom, as (key number, onset, duration) in 24ths
of a quarter note of the edition.  It was derived once by :func:`extract` from the music21 corpus
(``music21/corpus/palestrina/*.krn``, Humdrum encodings of the Masses, and ``music21/corpus/monteverdi/*.mxl``), as
Part 17's chorales and Part 23's fourteenth-century pieces were; the music is in the public domain, and only pitches
and times are kept.  Accidentals are as encoded, editorial ones included.

    from explainer.music.monochord import renaissance
    book = renaissance.load()                  # a list of trecento.Piece, with .work and .book filled in
"""

from __future__ import annotations

import gzip
import io
import json
import re
import zipfile
from pathlib import Path

from .trecento import TICKS, Piece, parse_musicxml

DATA = Path(__file__).with_name("data") / "renaissance.json.gz"
STEPS = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}


def kern_pitch(tok: str) -> int | None:
    """A **kern pitch: c is middle C (60), cc the C above, C the C below, CC two below; # sharp, - flat."""
    m = re.search(r"([a-gA-G])\1*", tok)
    if not m:
        return None
    letters = m.group(0)
    low = letters[0].lower()
    if letters[0].islower():
        octave = 4 + (len(letters) - 1)
    else:
        octave = 3 - (len(letters) - 1)
    p = 12 * (octave + 1) + STEPS[low]
    p += tok.count("#") - tok.count("-")
    return p


def kern_duration(tok: str) -> int | None:
    """Ticks of a **kern duration: 1 a whole note, 2 a half, 0 a breve, 00 a long, dots multiply."""
    m = re.match(r"\[?\(?\{?(\d+)(\.*)", tok)
    if not m:
        return None
    num, dots = m.group(1), len(m.group(2))
    whole = 4 * TICKS
    if num == "0":
        base = 2 * whole
    elif num == "00":
        base = 4 * whole
    elif num == "000":
        base = 8 * whole
    else:
        base = whole / int(num)
    d = base
    add = base
    for _ in range(dots):
        add /= 2
        d += add
    return int(round(d))


def parse_kern(text: str, name: str) -> Piece | None:
    """A piece from a Humdrum file whose spines are all **kern and never split.  Ties are merged; chords keep their
    first note; grace notes are skipped."""
    lines = text.splitlines()
    ref = {}
    for ln in lines:
        if ln.startswith("!!!"):
            k, _, v = ln[3:].partition(":")
            ref[k.strip()] = v.strip()
    data = [ln for ln in lines if ln and not ln.startswith("!")]
    if not data or not data[0].startswith("**"):
        return None
    heads = data[0].split("\t")
    if any(h != "**kern" for h in heads):
        return None
    n = len(heads)
    voices = [[] for _ in range(n)]
    t = [0] * n
    meter = None
    bar = 0
    for ln in data[1:]:
        cells = ln.split("\t")
        if len(cells) != n:
            return None                                                  # a spine split: skip the piece
        if cells[0].startswith("*"):
            if any(c in ("*^", "*v") for c in cells):
                return None
            for c in cells:
                mm = re.match(r"\*M(\d+)/(\d+)", c)
                if mm and meter is None:
                    meter = (int(mm.group(1)), int(mm.group(2)))
            continue
        if cells[0].startswith("="):
            continue
        for j, c in enumerate(cells):
            if c == ".":
                continue
            tok = c.split(" ")[0]
            if "q" in tok:                                              # grace note
                continue
            d = kern_duration(tok)
            if d is None:
                continue
            if "r" not in tok:
                p = kern_pitch(tok)
                if p is not None:
                    tied = ("]" in tok or "_" in tok)
                    if tied and voices[j] and voices[j][-1][0] == p and voices[j][-1][1] + voices[j][-1][2] == t[j]:
                        q, o, dd = voices[j][-1]
                        voices[j][-1] = (q, o, dd + d)
                    else:
                        voices[j].append((p, t[j], d))
            t[j] += d
    voices = [v for v in voices if v]
    if len(voices) < 2:
        return None
    meter = meter or (4, 2)
    bar = int(4 * TICKS * meter[0] / meter[1])
    voices.sort(key=lambda v: -sum(p for p, _, _ in v) / len(v))
    title = ref.get("OTL", name)
    pc = Piece(name, title, "Giovanni Pierluigi da Palestrina" if "Palestrina" in ref.get("COM", "") else ref.get("COM", ""), meter, bar, voices)
    pc.work = ref.get("OPR", "")
    return pc


def load(path: Path = DATA) -> list[Piece]:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        raw = json.load(f)
    out = []
    for r in raw:
        pc = Piece(r["name"], r["title"], r["composer"], tuple(r["time"]), r["bar"], [[tuple(n) for n in v] for v in r["voices"]])
        pc.work = r.get("work", "")
        pc.book = r.get("book", 0)
        out.append(pc)
    return out


def extract(wheel: str | Path, out: Path = DATA) -> dict:
    z = zipfile.ZipFile(Path(wheel))
    rows = []
    skipped = 0
    for nm in sorted(z.namelist()):
        if nm.startswith("music21/corpus/palestrina/") and nm.endswith(".krn"):
            pc = parse_kern(z.read(nm).decode("latin-1"), Path(nm).stem)
            if pc is None:
                skipped += 1
                continue
            rows.append({"name": pc.name, "title": pc.title, "composer": pc.composer, "work": pc.work, "book": 0,
                         "time": list(pc.time), "bar": pc.bar, "voices": [[list(x) for x in v] for v in pc.voices]})
        elif nm.startswith("music21/corpus/monteverdi/") and nm.endswith(".mxl") and "_old" not in nm:
            inner = zipfile.ZipFile(io.BytesIO(z.read(nm)))
            xml = [m for m in inner.namelist() if m.endswith(".xml") and not m.startswith("META-INF")]
            if not xml:
                skipped += 1
                continue
            raw = inner.read(xml[0])
            enc = "utf-16" if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else "utf-8"
            text = raw.decode(enc, "ignore")
            text = re.sub(r"<\?xml[^>]*\?>", "", text)
            text = re.sub(r"<!DOCTYPE[^>]*>", "", text)
            try:
                pc = parse_musicxml(text, Path(nm).stem)
            except Exception:                                           # an encoding the reader cannot parse
                pc = None
            if pc is None:
                skipped += 1
                continue
            book = int(Path(nm).stem.split(".")[1])
            rows.append({"name": pc.name, "title": " ".join(pc.title.split()), "composer": "Claudio Monteverdi", "work": f"Book {book}", "book": book,
                         "time": list(pc.time), "bar": pc.bar, "voices": [[list(x) for x in v] for v in pc.voices]})
    with gzip.open(out, "wt", encoding="utf-8") as f:
        json.dump(rows, f, separators=(",", ":"))
    return {"pieces": len(rows), "skipped": skipped}


if __name__ == "__main__":
    import sys

    print(extract(sys.argv[1]))
