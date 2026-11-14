"""The Romantic century (Part 27): the Library across six centuries, and the tools that measure its stretching.

The Library is every piece in the music21 corpus that has a date and a composer, read here with all its notes (chords
kept whole, ties merged), beside the collections earlier parts already read (the trecento, Palestrina, Monteverdi,
Bach's chorales, Corelli, Handel, the Classical quartets).  The measures are Part 15's: a key found in each window of
the music by the Krumhansl–Kessler profiles, and then

* *chromaticism*, the share of sounding time on pitch classes outside that window's key (in minor, the natural, harmonic
  and melodic forms all count as inside), and
* *tonal clarity*, how well the best key fits the window (the correlation of the duration-weighted pitch-class
  distribution with the best key's profile).

Also here: thematic transformation, the phrase-arch model of rubato, the mazurka's uneven beats, documented keyboard
ranges and the winds and brass that symphonies call for.  No manim.
"""

from __future__ import annotations

import gzip
import io
import json
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np

from . import key as K

TICKS = 24                                                         # per quarter note
DATA = Path(__file__).with_name("data") / "library.json.gz"
STEPS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
MINOR_SET = frozenset({0, 2, 3, 5, 7, 8, 9, 10, 11})               # natural, harmonic and melodic minor together
MAJOR_SET = frozenset(K.MAJOR_SCALE)

# (corpus path, composer, title, year, kind).  Years are of composition (or first publication where that is how the
# piece is dated); the film's scatter uses them as they stand.
LIBRARY = [
    ("cpebach/h186.mxl", "C. P. E. Bach", "Sonata in A, H. 186, slow movement", 1765, "keyboard"),
    ("weber/concertino_clarinet.mxl", "Weber", "Clarinet Concertino, Op. 26 (with piano)", 1811, "concerto"),
    ("schubert/Lindenbaum.xml", "Schubert", "Der Lindenbaum (Winterreise)", 1827, "song"),
    ("chopin/mazurka06-2.krn", "Chopin", "Mazurka, Op. 6 No. 2", 1830, "keyboard"),
    ("schumann_clara/polonaise_op1n1.mxl", "Clara Schumann", "Polonaise, Op. 1 No. 1", 1831, "keyboard"),
    ("schumann_clara/polonaise_op1n2.mxl", "Clara Schumann", "Polonaise, Op. 1 No. 2", 1831, "keyboard"),
    ("schumann_clara/polonaise_op1n3.mxl", "Clara Schumann", "Polonaise, Op. 1 No. 3", 1831, "keyboard"),
    ("schumann_clara/polonaise_op1n4.mxl", "Clara Schumann", "Polonaise, Op. 1 No. 4", 1831, "keyboard"),
    ("schumann_robert/dichterliebe_no2.xml", "Robert Schumann", "Dichterliebe No. 2", 1840, "song"),
    ("schumann_robert/opus41no1/movement1.mxl", "Robert Schumann", "String Quartet Op. 41 No. 1, i", 1842, "quartet"),
    ("schumann_robert/opus41no1/movement2.mxl", "Robert Schumann", "String Quartet Op. 41 No. 1, ii", 1842, "quartet"),
    ("schumann_robert/opus41no1/movement3.mxl", "Robert Schumann", "String Quartet Op. 41 No. 1, iii", 1842, "quartet"),
    ("schumann_robert/opus41no1/movement4.mxl", "Robert Schumann", "String Quartet Op. 41 No. 1, iv", 1842, "quartet"),
    ("schumann_clara/opus17/movement3.xml", "Clara Schumann", "Piano Trio, Op. 17, iii", 1846, "chamber"),
    ("verdi/laDonnaEMobile.mxl", "Verdi", "La donna è mobile (Rigoletto)", 1851, "song"),
    ("leadSheet/fosterBrownHair.mxl", "Foster", "Jeanie with the Light Brown Hair", 1854, "song"),
    ("liliuokalani/aloha_oe.mxl", "Liliʻuokalani", "Aloha ʻOe", 1878, "song"),
    ("joplin/maple_leaf_rag.mxl", "Joplin", "Maple Leaf Rag", 1899, "keyboard"),
    ("johnson_j_r/lift_every_voice.mxl", "J. R. Johnson", "Lift Every Voice and Sing", 1900, "song"),
    ("schoenberg/opus19/movement2.mxl", "Schoenberg", "Six Little Piano Pieces, Op. 19 No. 2", 1911, "keyboard"),
    ("schoenberg/opus19/movement6.mxl", "Schoenberg", "Six Little Piano Pieces, Op. 19 No. 6", 1911, "keyboard"),
    ("leadSheet/berlinAlexandersRagtime.mxl", "Berlin", "Alexander's Ragtime Band", 1911, "song"),
    ("webern/webern_dormi_jesu_op_16_no_2.mxl", "Webern", "Dormi Jesu, Op. 16 No. 2", 1924, "song"),
]

# Documented keyboard compasses (lowest and highest key numbers), approximate dates.
KEYBOARDS = [
    (1720, "Cristofori's piano (Florence)", 36, 89),
    (1785, "a Viennese fortepiano (Stein, Walter)", 29, 89),
    (1817, "Beethoven's Broadwood", 24, 96),
    (1825, "a Viennese Graf", 24, 101),
    (1850, "an Érard grand", 21, 105),
    (1880, "a Steinway grand: 88 keys", 21, 108),
]

# Winds, brass and timpani that a symphony's score calls for (players, counting doublings once).
ORCHESTRAS = [
    (1759, "Haydn, Symphony No. 1", {"oboes": 2, "bassoon": 1, "horns": 2}),
    (1788, "Mozart, Symphony No. 40 (with clarinets)", {"flute": 1, "oboes": 2, "clarinets": 2, "bassoons": 2, "horns": 2}),
    (1808, "Beethoven, Symphony No. 5", {"piccolo": 1, "flutes": 2, "oboes": 2, "clarinets": 2, "bassoons": 2, "contrabassoon": 1,
                                         "horns": 2, "trumpets": 2, "trombones": 3, "timpani": 1}),
    (1830, "Berlioz, Symphonie fantastique", {"flutes": 2, "oboes": 2, "clarinets": 2, "bassoons": 4, "horns": 4, "trumpets": 2,
                                              "cornets": 2, "trombones": 3, "ophicleides": 2, "timpani": 4}),
    (1876, "Brahms, Symphony No. 1", {"flutes": 2, "oboes": 2, "clarinets": 2, "bassoons": 2, "contrabassoon": 1, "horns": 4,
                                      "trumpets": 2, "trombones": 3, "timpani": 1}),
]


# ---------------------------------------------------------------------------------------------------------- reading
def _midi(n) -> int:
    p = n.find("pitch")
    return 12 * (int(p.findtext("octave")) + 1) + STEPS[p.findtext("step")] + int(float(p.findtext("alter") or 0))


def read_corpus(z: zipfile.ZipFile, path: str) -> str:
    raw = z.read("music21/corpus/" + path)
    if path.endswith(".mxl"):
        inner = zipfile.ZipFile(io.BytesIO(raw))
        names = [m for m in inner.namelist() if not m.startswith("META-INF")]
        raw = inner.read(next(m for m in names if m.endswith((".xml", ".musicxml"))))
    enc = "utf-16" if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else "utf-8"
    text = raw.decode(enc, "ignore")
    text = re.sub(r"<\?xml[^>]*\?>", "", text)
    return re.sub(r"<!DOCTYPE[^>]*>", "", text)


def parse_all(text: str) -> dict:
    """Every note of a partwise MusicXML file, chords whole and ties merged, as (key number, onset, duration) in 24ths of
    a quarter, by part; with the first time signature."""
    root = ET.fromstring(text)
    names = {sp.get("id"): (sp.findtext("part-name") or "").strip() or sp.get("id") for sp in root.iter("score-part")}
    parts, time = {}, None
    for part in root.findall("part"):
        pid = part.get("id")
        t, div, last, shift = 0, 1, 0, 0
        notes, open_ = [], {}
        for measure in part.findall("measure"):
            a = measure.find("attributes")
            if a is not None:
                if a.findtext("divisions"):
                    div = int(float(a.findtext("divisions")))
                if a.find("transpose") is not None:                # a transposing instrument: sounding pitch
                    tr = a.find("transpose")
                    shift = int(float(tr.findtext("chromatic") or 0)) + 12 * int(float(tr.findtext("octave-change") or 0))
                if time is None and a.find("time/beats") is not None:
                    try:
                        time = (int(a.findtext("time/beats").split("+")[0]), int(a.findtext("time/beat-type")))
                    except ValueError:
                        pass
            for el in measure:
                if el.tag == "backup":
                    t -= int(float(el.findtext("duration"))) * TICKS // div
                elif el.tag == "forward":
                    t += int(float(el.findtext("duration"))) * TICKS // div
                elif el.tag == "note":
                    if el.find("grace") is not None or el.findtext("duration") is None:
                        continue
                    d = int(float(el.findtext("duration"))) * TICKS // div
                    chord = el.find("chord") is not None
                    onset = last if chord else t
                    if el.find("rest") is None and el.find("pitch") is not None:
                        p = _midi(el) + shift
                        ties = {x.get("type") for x in el.findall("tie")}
                        k = open_.get(p)
                        if "stop" in ties and k is not None and notes[k][1] + notes[k][2] == onset:
                            q, o, dd = notes[k]
                            notes[k] = (q, o, dd + d)
                        else:
                            notes.append((p, onset, d))
                            k = len(notes) - 1
                        if "start" in ties:
                            open_[p] = k
                        elif p in open_:
                            del open_[p]
                    if not chord:
                        last = t
                        t += d
        label = names.get(pid, pid)
        while label in parts:
            label += "'"
        parts[label] = sorted(notes, key=lambda n: (n[1], n[0]))
    return {"parts": parts, "time": time or (4, 4)}


def parse_kern_all(text: str) -> dict:
    """Every note of a Humdrum **kern file (chords whole, ties merged), by original spine; spine splits (``*^``) and
    merges (``*v``) are followed, so that a split staff's voices stay in their part."""
    from .renaissance import kern_duration, kern_pitch
    cols = None                                         # one dict per column: its part and its running time
    parts: dict = {}
    open_: dict = {}
    time = (4, 4)
    for line in text.splitlines():
        if not line or line.startswith("!"):
            continue
        cells = line.split("\t")
        if line.startswith("**"):
            cols = [{"part": i if c == "**kern" else None, "t": 0} for i, c in enumerate(cells)]
            continue
        if cols is None or len(cells) != len(cols):
            continue
        if line.startswith("*"):
            new = []
            i = 0
            while i < len(cells):
                c = cells[i]
                m = re.match(r"\*M(\d+)/(\d+)", c)
                if m:
                    time = (int(m.group(1)), int(m.group(2)))
                if c == "*^":
                    new += [dict(cols[i]), dict(cols[i])]
                elif c == "*v":
                    j = i
                    while j < len(cells) and cells[j] == "*v":
                        j += 1
                    new.append({"part": cols[i]["part"], "t": max(cols[k]["t"] for k in range(i, j))})
                    i = j
                    continue
                elif c == "*-":
                    pass
                else:
                    new.append(cols[i])
                i += 1
            cols = new
            continue
        if line.startswith("="):
            continue
        for i, c in enumerate(cells):
            col = cols[i]
            if col["part"] is None or c == ".":
                continue
            d = None
            for tok in c.split(" "):
                dd = kern_duration(tok)
                if dd is None:
                    continue
                d = dd
                if "r" in tok:
                    continue
                p = kern_pitch(tok)
                if p is None:
                    continue
                notes = parts.setdefault(col["part"], [])
                key = (col["part"], p)
                if ("_" in tok or "]" in tok) and key in open_:
                    k = open_[key]
                    q, o, du = notes[k]
                    notes[k] = (q, o, du + dd)
                    if "]" in tok:
                        del open_[key]
                else:
                    notes.append((p, col["t"], dd))
                    if "[" in tok:
                        open_[key] = len(notes) - 1
            if d is not None:
                col["t"] += d
    return {"parts": {f"spine {k}": sorted(v, key=lambda n: (n[1], n[0])) for k, v in parts.items()}, "time": time}


def extract_library(wheel, out: Path = DATA) -> dict:
    z = zipfile.ZipFile(Path(wheel))
    rows, skipped = [], []
    for path, composer, title, year, kind in LIBRARY:
        try:
            text = z.read("music21/corpus/" + path).decode("utf-8", "ignore") if path.endswith(".krn") else read_corpus(z, path)
            r = parse_kern_all(text) if path.endswith(".krn") else parse_all(text)
        except Exception as e:                                     # pragma: no cover - reported, not hidden
            skipped.append(f"{path}: {e}")
            continue
        rows.append({"path": path, "composer": composer, "title": title, "year": year, "kind": kind, "time": list(r["time"]),
                     "parts": {k: [list(n) for n in v] for k, v in r["parts"].items() if v}})
    with gzip.open(out, "wt", encoding="utf-8") as f:
        json.dump(rows, f, separators=(",", ":"))
    return {"pieces": len(rows), "skipped": skipped}


def load_library(path: Path = DATA) -> list[dict]:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        raw = json.load(f)
    for r in raw:
        r["parts"] = {k: [tuple(n) for n in v] for k, v in r["parts"].items()}
        r["time"] = tuple(r["time"])
    return raw


def all_notes(parts) -> list:
    """Every note of every part, as (key number, onset, duration), in time order."""
    out = [n for v in (parts.values() if isinstance(parts, dict) else parts) for n in v]
    return sorted(out, key=lambda n: (n[1], n[0]))


# -------------------------------------------------------------------------------------------------------- measures
def in_key(pc: int, key) -> bool:
    rel = (pc - key[0]) % 12
    return rel in (MAJOR_SET if key[1] == "major" else MINOR_SET)


def windows(notes, window: float, hop: float):
    """(start, pitches, weights) for windows of ``window`` quarters every ``hop``, weights the sounding time in the window."""
    if not notes:
        return []
    end = max(o + d for _, o, d in notes) / TICKS
    out = []
    starts = np.arange(0.0, max(end - window, 0.0) + 1e-9, hop) if end > window else [0.0]
    on = np.array([o / TICKS for _, o, _ in notes])
    off = np.array([(o + d) / TICKS for _, o, d in notes])
    pit = np.array([p for p, _, _ in notes])
    for s in starts:
        w = np.clip(np.minimum(off, s + window) - np.maximum(on, s), 0.0, None)
        sel = w > 0
        if sel.sum() >= 3:
            out.append((float(s), pit[sel], w[sel]))
    return out


def measure(notes, window: float = 16.0, hop: float = 8.0) -> dict:
    """Chromaticism and tonal clarity, window by window, and their time-weighted means; with the keys found."""
    chrom, clar, weights, keys = [], [], [], []
    for s, p, w in windows(notes, window, hop):
        dist = K.distribution(list(p), list(w))
        cor = K.correlations(dist)
        best = max(cor, key=cor.get)
        outside = sum(wi for pi, wi in zip(p, w) if not in_key(int(pi) % 12, best))
        chrom.append(outside / w.sum())
        clar.append(cor[best])
        weights.append(w.sum())
        keys.append({"start": s, "key": list(best), "r": float(cor[best])})
    if not chrom:
        return {"chromaticism": float("nan"), "clarity": float("nan"), "keys": [], "windows": 0}
    wt = np.array(weights)
    return {"chromaticism": float(np.average(chrom, weights=wt)), "clarity": float(np.average(clar, weights=wt)),
            "keys": keys, "windows": len(chrom), "per_window": [[float(a), float(b)] for a, b in zip(chrom, clar)]}


def pc_entropy(notes) -> float:
    """Entropy, in bits, of the duration-weighted pitch-class distribution (0 for one pitch class, log2 12 = 3.58 for all
    twelve equally)."""
    h = np.zeros(12)
    for p, _, d in notes:
        h[p % 12] += d
    q = h[h > 0] / h.sum()
    return float(-(q * np.log2(q)).sum())


def register_span(notes) -> int:
    ps = [p for p, _, _ in notes]
    return int(max(ps) - min(ps)) if ps else 0


# ------------------------------------------------------------------------------------------ transformation, rubato
def transform(line, kind: str):
    """The Tune's phrase, transformed as Liszt and Berlioz transformed themes; ``line`` is (key number, beat, beats)."""
    if kind == "original":
        return list(line)
    if kind == "minor":                                            # E becomes E flat, A becomes A flat (C minor)
        return [(p - 1 if (p % 12) in (4, 9, 11) else p, a, d) for p, a, d in line]
    if kind == "augmented":
        return [(p, 2 * a, 2 * d) for p, a, d in line]
    if kind == "waltz":                                            # every pair of beats becomes long-short in three
        out = []
        for p, a, d in line:
            b = int(a)
            out.append((p, 1.5 * (b - b % 2) + (0 if b % 2 == 0 else 2), 2.0 if b % 2 == 0 else 1.0 if d <= 1 else 2.5))
        return out
    if kind == "inverted":
        axis = line[0][0]
        return [(2 * axis - p, a, d) for p, a, d in line]
    if kind == "march":                                            # dotted rhythm, an octave lower
        out = []
        for p, a, d in line:
            out += [(p - 12, a, 0.75 * d), (p - 12, a + 0.75 * d, 0.25 * d)] if d >= 1 else [(p - 12, a, d)]
        return out
    raise ValueError(kind)


def phrase_arch(onsets, phrase: float, depth: float = 0.25, power: float = 2.0) -> np.ndarray:
    """Performance times for score onsets (in beats) under Todd's phrase arch: within each phrase the tempo rises from the
    start, peaks in the middle and falls to the end, ``depth`` the fractional change.  Returns times in beats of the
    plain tempo; the total length of a phrase is unchanged to first order."""
    onsets = np.asarray(onsets, float)
    grid = np.linspace(0, onsets.max() + phrase, int((onsets.max() + phrase) * 48) + 2)
    u = (grid % phrase) / phrase
    tempo = 1.0 + depth * (1.0 - np.abs(2 * u - 1) ** power) - depth * (1 - 1 / (power + 1))
    dt = np.diff(grid, prepend=0.0) / tempo
    t = np.cumsum(dt)
    return np.interp(onsets, grid, t)


def mazurka_beats(onsets, beat_lengths=(0.85, 1.2, 0.95)) -> np.ndarray:
    """Performance times for onsets in a three-beat bar whose beats have the given relative lengths (normalized to
    three): a short first beat and a long second is the pattern measured in many mazurka recordings."""
    b = np.asarray(beat_lengths, float)
    b = 3 * b / b.sum()
    edges = np.concatenate([[0.0], np.cumsum(b)])
    onsets = np.asarray(onsets, float)
    bar, x = np.floor(onsets / 3), onsets % 3
    k = np.minimum(np.floor(x).astype(int), 2)
    return 3 * bar + edges[k] + (x - k) * b[k]


def winds(spec: dict) -> int:
    return int(sum(spec.values()))
