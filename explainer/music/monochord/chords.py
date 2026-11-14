"""Monochord's chords (Part 13, *Intervals and Chords*).

Intervals between written pitches, chords as stacks of thirds, their inversions, figures, symbols and roots, how a
chord is spread over the keyboard, Euler's lattice of fifths and thirds, and a small listener that names a chord
from its sound.

    interval(a, b)                         a written interval: its number, quality, inversion and class
    fifths(pitch)                          a pitch's place on the line of fifths (C is 0, G is 1, F is -1)
    spell(root, kind)                      a chord's notes, correctly spelled; KINDS is the vocabulary
    scale_chords(tonic, size)              the triads or sevenths on the degrees of a major scale, with Roman numerals
    identify(pitches)                      every (root, kind, inversion) that a set of notes can be
    figures(pitches) / figure_name(...)    the intervals above the bass: 6, 6/4, 6/5, 4/3, 4/2
    symbol(...) / parse_symbol(text)       lead-sheet symbols, both ways
    root_saliences(pcs) / root(pcs)        Parncutt's model of a chord's root, and how ambiguous it is
    chord_partials / spacing_roughness     a voicing's roughness, from Part 5's model
    low_limit(semitones)                   the lowest bass note at which an interval stays as clear as a reference
    voicings / nearest_voicing             ways to spread a chord, and the one that moves least from the last
    tonnetz(pc), P, L, R, cycle            Euler's lattice and the three smallest moves between triads
    voice_leading(a, b)                    the least total motion between two chords
    chroma(y, sr) / recognise(chroma)      a chord named from its sound, by matching templates

No manim.  Checked in ``tests/music/test_chords.py``.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product

import numpy as np

from . import consonance as _cons
from .score import SEMITONES, STEPS, Pitch

# ---------------------------------------------------------------------------
# Intervals
# ---------------------------------------------------------------------------
_LINE = {"F": -1, "C": 0, "G": 1, "D": 2, "A": 3, "E": 4, "B": 5}
NUMBER_NAMES = ("unison", "second", "third", "fourth", "fifth", "sixth", "seventh", "octave", "ninth", "tenth", "eleventh", "twelfth", "thirteenth")
_SHORT = {"perfect": "P", "major": "M", "minor": "m", "augmented": "A", "diminished": "d", "doubly augmented": "AA", "doubly diminished": "dd"}
IC_NAMES = ("unison or octave", "semitone or major seventh", "whole tone or minor seventh", "minor third or major sixth", "major third or minor sixth",
            "fourth or fifth", "tritone")


def fifths(p: Pitch) -> int:
    """A written pitch's place on the line of fifths: ... B flat -2, F -1, C 0, G 1, D 2 ... F sharp 6 ..."""
    return _LINE[p.step] + 7 * p.alter


def quality_of(line: int) -> str:
    """The quality of an interval from how far apart its two notes are on the line of fifths (upper minus lower):
    within one step perfect, two to five major (or minor, downwards), six to twelve augmented (diminished)."""
    a = abs(line)
    if a <= 1:
        return "perfect"
    if a <= 5:
        return "major" if line > 0 else "minor"
    if a <= 12:
        return "augmented" if line > 0 else "diminished"
    return "doubly augmented" if line > 0 else "doubly diminished"


@dataclass(frozen=True)
class Interval:
    """A written interval: so many letters up (``steps``; a third is 2) and so many semitones."""
    steps: int
    semitones: int

    @property
    def number(self) -> int:
        return self.steps + 1

    @property
    def line(self) -> int:
        """The distance on the line of fifths.  Seven letters and twelve semitones (an octave) are no distance."""
        s, h = self.steps % 7, self.semitones - 12 * (self.steps // 7)
        natural = (0, 2, 4, 5, 7, 9, 11)[s]
        base = (0, 2, 4, -1, 1, 3, 5)[s]                    # the major or perfect interval of that number
        return base + 7 * (h - natural)

    @property
    def quality(self) -> str:
        if self.steps % 7 == 0 and self.steps > 0 and self.semitones == 12 * (self.steps // 7):
            return "perfect"
        return quality_of(self.line)

    @property
    def name(self) -> str:
        n = NUMBER_NAMES[self.steps] if self.steps < len(NUMBER_NAMES) else f"{self.number}th"
        return f"{self.quality} {n}"

    @property
    def short(self) -> str:
        return f"{_SHORT[self.quality]}{self.number}"

    def simple(self) -> "Interval":
        """Within an octave (an octave itself stays an octave)."""
        if self.steps <= 7:
            return self
        k = (self.steps - 1) // 7
        return Interval(self.steps - 7 * k, self.semitones - 12 * k)

    def invert(self) -> "Interval":
        """What is left of the octave: a third becomes a sixth, major becomes minor, perfect stays perfect."""
        s = self.simple()
        return Interval(7 - s.steps, 12 - s.semitones)

    @property
    def interval_class(self) -> int:
        """Zero to six: the distance between the two notes on a clock of twelve, the shorter way round."""
        d = self.semitones % 12
        return min(d, 12 - d)


def interval(a: Pitch, b: Pitch) -> Interval:
    """The interval from the lower of two written pitches up to the higher."""
    lo, hi = (a, b) if (a.diatonic, a.midi) <= (b.diatonic, b.midi) else (b, a)
    return Interval(hi.diatonic - lo.diatonic, hi.midi - lo.midi)


def interval_class(a: int, b: int) -> int:
    d = (int(b) - int(a)) % 12
    return min(d, 12 - d)


def named(short: str) -> Interval:
    """``"M3"``, ``"P5"``, ``"A4"``, ``"d7"``, ``"m10"``."""
    q, n = short.rstrip("0123456789"), int(short[len(short.rstrip("0123456789")):])
    steps = n - 1
    s, octs = steps % 7, steps // 7
    base = (0, 2, 4, 5, 7, 9, 11)[s] + 12 * octs
    perfect = s in (0, 3, 4)
    shift = {"P": 0, "M": 0, "m": -1, "A": 1, "d": -1 if perfect else -2, "AA": 2, "dd": -2 if perfect else -3}[q]
    if (q == "P") != perfect and q in ("P", "M", "m"):
        raise ValueError(f"there is no {short}")
    return Interval(steps, base + shift)


def above(p: Pitch, iv: Interval | str) -> Pitch:
    iv = named(iv) if isinstance(iv, str) else iv
    return p.up(iv.steps, iv.semitones)


def spell_pc(pc: int, key: int = 0, octave: int = 4) -> Pitch:
    """A spelling for one of the twelve keys of the piano in a key (its number of sharps): the one nearest the key
    on the line of fifths, from five flatward to six sharpward.  In D (2) the key between F and G is F sharp."""
    for line in range(key - 5, key + 7):
        if (7 * line) % 12 == pc % 12:
            alter, idx = divmod(line + 1, 7)
            return Pitch("FCGDAEB"[idx], alter, octave)
    raise AssertionError


# ---------------------------------------------------------------------------
# Chords
# ---------------------------------------------------------------------------
# every member as (letters above the root, semitones above the root)
_M3, _m3, _P5, _d5, _A5 = (2, 4), (2, 3), (4, 7), (4, 6), (4, 8)
KINDS: dict[str, tuple] = {
    "major": ((0, 0), _M3, _P5),
    "minor": ((0, 0), _m3, _P5),
    "diminished": ((0, 0), _m3, _d5),
    "augmented": ((0, 0), _M3, _A5),
    "7": ((0, 0), _M3, _P5, (6, 10)),
    "maj7": ((0, 0), _M3, _P5, (6, 11)),
    "m7": ((0, 0), _m3, _P5, (6, 10)),
    "m7b5": ((0, 0), _m3, _d5, (6, 10)),
    "dim7": ((0, 0), _m3, _d5, (6, 9)),
    "mMaj7": ((0, 0), _m3, _P5, (6, 11)),
    "6": ((0, 0), _M3, _P5, (5, 9)),
    "m6": ((0, 0), _m3, _P5, (5, 9)),
    "sus4": ((0, 0), (3, 5), _P5),
    "sus2": ((0, 0), (1, 2), _P5),
    "5": ((0, 0), _P5),
    "9": ((0, 0), _M3, _P5, (6, 10), (8, 14)),
    "maj9": ((0, 0), _M3, _P5, (6, 11), (8, 14)),
    "m9": ((0, 0), _m3, _P5, (6, 10), (8, 14)),
    "11": ((0, 0), _M3, _P5, (6, 10), (8, 14), (10, 17)),
    "13": ((0, 0), _M3, _P5, (6, 10), (8, 14), (10, 17), (12, 21)),
    "maj13": ((0, 0), _M3, _P5, (6, 11), (8, 14), (10, 17), (12, 21)),
}
TRIADS = ("major", "minor", "diminished", "augmented")
SEVENTHS = ("7", "maj7", "m7", "m7b5", "dim7", "mMaj7")
KIND_NAMES = {"major": "major", "minor": "minor", "diminished": "diminished", "augmented": "augmented", "7": "dominant seventh",
              "maj7": "major seventh", "m7": "minor seventh", "m7b5": "half-diminished seventh", "dim7": "diminished seventh",
              "mMaj7": "minor-major seventh", "6": "added sixth", "m6": "minor sixth", "sus4": "suspended fourth", "sus2": "suspended second",
              "5": "fifth alone", "9": "ninth", "maj9": "major ninth", "m9": "minor ninth", "11": "eleventh", "13": "thirteenth",
              "maj13": "major thirteenth"}
_SUFFIX = {"major": "", "minor": "m", "diminished": "dim", "augmented": "aug", "7": "7", "maj7": "maj7", "m7": "m7", "m7b5": "m7♭5", "dim7": "dim7",
           "mMaj7": "m(maj7)", "6": "6", "m6": "m6", "sus4": "sus4", "sus2": "sus2", "5": "5", "9": "9", "maj9": "maj9", "m9": "m9", "11": "11", "13": "13",
           "maj13": "maj13"}
_PRIORITY = ("major", "minor", "7", "maj7", "m7", "diminished", "augmented", "m7b5", "dim7", "mMaj7", "6", "m6", "sus4", "sus2", "5", "9", "maj9",
             "m9", "11", "13", "maj13")


def offsets(kind: str) -> tuple[int, ...]:
    """A kind of chord as semitones above its root."""
    return tuple(h for _, h in KINDS[kind])


def pcs_of(root: int, kind: str) -> tuple[int, ...]:
    return tuple(sorted({(int(root) + h) % 12 for h in offsets(kind)}))


def spell(root: Pitch | str, kind: str = "major") -> list[Pitch]:
    """A chord's notes above a root, in root position, each with the letter a stack of thirds gives it."""
    r = Pitch.parse(root) if isinstance(root, str) else root
    return [r.up(s, h) for s, h in KINDS[kind]]


def invert(pitches: list[Pitch], times: int = 1) -> list[Pitch]:
    """Put the lowest note on top, ``times`` times: root position, first inversion, second ..."""
    out = sorted(pitches, key=lambda p: p.midi)
    for _ in range(times):
        low = out.pop(0)
        out.append(Pitch(low.step, low.alter, low.octave + 1))
    return out


MAJOR_STEPS = (0, 2, 4, 5, 7, 9, 11)
MINOR_STEPS = (0, 2, 3, 5, 7, 8, 10)
ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII")


def roman(degree: int, kind: str, inversion: int = 0) -> str:
    """A Roman numeral in Weber's manner: capitals for major, small letters for minor, a ring for diminished."""
    r = ROMAN[(degree - 1) % 7]
    third_minor = kind in ("minor", "diminished", "m7", "m7b5", "dim7", "mMaj7", "m6", "m9")
    r = r.lower() if third_minor else r
    mark = {"diminished": "°", "augmented": "+", "m7b5": "ø", "dim7": "°"}.get(kind, "")
    seventh = len(KINDS[kind]) >= 4 and KINDS[kind][3][0] == 6
    fig = (("7", "6/5", "4/3", "4/2") if seventh else ("", "6", "6/4"))[inversion]
    if kind == "maj7" and inversion == 0:
        fig = "maj7"
    return r + mark + fig


def kind_from_offsets(offs) -> str | None:
    s = frozenset(int(o) % 12 for o in offs)
    for k in _PRIORITY:
        if frozenset(o % 12 for o in offsets(k)) == s:
            return k
    return None


def scale_chords(tonic: Pitch | str = "C4", size: int = 3, steps=MAJOR_STEPS) -> list[dict]:
    """The chords made of every other note of a seven-note scale, one on each degree: for the major scale, three
    major triads, three minor and one diminished."""
    t = Pitch.parse(tonic) if isinstance(tonic, str) else tonic
    scale = [t.up(k, steps[k % 7] + 12 * (k // 7)) for k in range(7 + 2 * size)]
    out = []
    for d in range(7):
        notes = [scale[d + 2 * j] for j in range(size)]
        kind = kind_from_offsets([n.midi - notes[0].midi for n in notes])
        out.append({"degree": d + 1, "pitches": notes, "kind": kind, "roman": roman(d + 1, kind), "names": [n.name for n in notes]})
    return out


def identify(pitches) -> list[dict]:
    """Everything a set of notes can be called: for each of its notes taken as the root, the kind of chord (if it
    is one of ``KINDS``) and the inversion (which chord member is in the bass).  Ordered from the plainest name."""
    mids = sorted((p.midi if isinstance(p, Pitch) else int(p)) for p in pitches)
    pcs = sorted({m % 12 for m in mids})
    bass = mids[0] % 12
    out = []
    for r in pcs:
        k = kind_from_offsets([(p - r) % 12 for p in pcs])
        if k is None:
            continue
        members = [(r + h) % 12 for h in offsets(k)]
        out.append({"root": r, "kind": k, "inversion": members.index(bass), "bass": bass})
    out.sort(key=lambda c: (_PRIORITY.index(c["kind"]), c["inversion"]))
    return out


def stack_of_thirds(pitches: list[Pitch]) -> list[Pitch] | None:
    """Rameau's reduction: the same letters rearranged so that each is a third above the one before.  The first is
    the root.  ``None`` if the letters are not every other letter of the scale."""
    letters = sorted({STEPS.index(p.step) for p in pitches})
    by_letter = {STEPS.index(p.step): p for p in sorted(pitches, key=lambda p: -p.midi)}
    for start in letters:
        chain = [(start + 2 * j) % 7 for j in range(len(letters))]
        if sorted(chain) == letters:
            return [by_letter[c] for c in chain]
    return None


def figures(pitches) -> tuple[int, ...]:
    """The numbers a continuo player reads: each upper note's interval above the bass, within an octave, largest
    first (an octave above the bass is the bass again and is left out)."""
    ps = sorted(pitches, key=lambda p: p.midi)
    nums = {((p.diatonic - ps[0].diatonic) % 7) + 1 for p in ps[1:]} - {1}
    return tuple(sorted(nums, reverse=True))


_FIGURE_NAMES = {(5, 3): "5/3", (6, 3): "6", (6, 4): "6/4", (7, 5, 3): "7", (6, 5, 3): "6/5", (6, 4, 3): "4/3", (6, 4, 2): "4/2"}


def figure_name(pitches) -> str:
    """The usual short form of a chord's figures: 6 for 6/3, 4/2 for 6/4/2."""
    f = figures(pitches)
    return _FIGURE_NAMES.get(f, "/".join(str(n) for n in f))


_ACC = {-2: "𝄫", -1: "♭", 0: "", 1: "♯", 2: "𝄪"}


def pitch_label(p: Pitch | int, flats: bool = True) -> str:
    """A note's name without its octave, with real accidental signs."""
    if not isinstance(p, Pitch):
        p = Pitch.from_midi(60 + int(p) % 12, flats=flats)
    return p.step + _ACC[p.alter]


def symbol(root: Pitch | str, kind: str = "major", bass: Pitch | str | None = None) -> str:
    """A lead-sheet symbol: ``C``, ``Am7``, ``F♯m7♭5``, ``C/E``."""
    r = Pitch.parse(root + "4") if isinstance(root, str) and not root[-1].isdigit() else (Pitch.parse(root) if isinstance(root, str) else root)
    s = pitch_label(r) + _SUFFIX[kind]
    if bass is not None:
        b = Pitch.parse(bass + "4") if isinstance(bass, str) and not bass[-1].isdigit() else (Pitch.parse(bass) if isinstance(bass, str) else bass)
        if (b.step, b.alter) != (r.step, r.alter):
            s += "/" + pitch_label(b)
    return s


_PARSE = sorted(((v.replace("♭", "b").replace("(", "").replace(")", ""), k) for k, v in _SUFFIX.items()), key=lambda kv: -len(kv[0]))
_ALIASES = {"min": "m", "-": "m", "M7": "maj7", "Δ": "maj7", "Δ7": "maj7", "ø": "m7b5", "ø7": "m7b5", "°": "dim", "°7": "dim7", "+": "aug", "mmaj7": "mmaj7",
            "min7": "m7", "-7": "m7", "sus": "sus4"}


def parse_symbol(text: str, octave: int = 4) -> dict:
    """Read a lead-sheet symbol: its root, kind, bass and notes.  ``parse_symbol("F#m7b5/A")``."""
    t = text.strip().replace("♯", "#").replace("♭", "b")
    head, _, slash = t.partition("/")
    step, rest = head[0].upper(), head[1:]
    alter = 0
    while rest and rest[0] in "#b":
        alter += 1 if rest[0] == "#" else -1
        rest = rest[1:]
    rest = rest.replace("(", "").replace(")", "")
    rest = _ALIASES.get(rest, rest)
    kind = None
    for suffix, k in _PARSE:
        if rest == suffix:
            kind = k
            break
    if kind is None:
        raise ValueError(f"unknown chord symbol {text!r}")
    root = Pitch(step, alter, octave)
    notes = spell(root, kind)
    bass = None
    if slash:
        b_alter = slash.count("#") - slash.count("b", 1)
        bass = Pitch(slash[0].upper(), b_alter, octave - 1)
    return {"root": root, "kind": kind, "bass": bass, "pitches": notes, "symbol": symbol(root, kind, bass)}


# ---------------------------------------------------------------------------
# Roots (Parncutt 1988, after Terhardt): a note supports a root that lies a unison, fifth, major third, minor
# seventh or major second below it, in that order of strength, as harmonics 1, 3, 5, 7 and 9 support a fundamental.
# ---------------------------------------------------------------------------
ROOT_SUPPORT = {0: 10.0, 7: 5.0, 4: 3.0, 10: 2.0, 2: 1.0}


def root_saliences(pcs, weights=None) -> np.ndarray:
    """How strongly each of the twelve notes is supported as the root of a chord.  ``weights`` can count a note
    more than once (a doubled root)."""
    pcs = [int(p) % 12 for p in pcs]
    w = [1.0] * len(pcs) if weights is None else list(weights)
    out = np.zeros(12)
    for r in range(12):
        out[r] = sum(wi * ROOT_SUPPORT.get((p - r) % 12, 0.0) for p, wi in zip(pcs, w))
    return out


def root(pcs, weights=None) -> dict:
    """The best-supported root, the runner-up, and the chord's root ambiguity (the square root of the sum of all
    saliences over the largest: 1.87 for a major triad, by Parncutt's later weights)."""
    s = root_saliences(pcs, weights)
    order = np.argsort(-s, kind="stable")
    return {"root": int(order[0]), "salience": float(s[order[0]]), "second": int(order[1]), "second_salience": float(s[order[1]]),
            "ambiguity": float(np.sqrt(s.sum() / s.max())), "saliences": s.tolist(), "tied": [int(i) for i in range(12) if abs(s[i] - s.max()) < 1e-9]}


# ---------------------------------------------------------------------------
# Voicing: the same notes, spread differently
# ---------------------------------------------------------------------------
def hz(midi: float) -> float:
    return 440.0 * 2.0 ** ((float(midi) - 69.0) / 12.0)


def chord_partials(midis, n: int = 7, rolloff: float = 0.88, gains=None) -> tuple[np.ndarray, np.ndarray]:
    """Every partial of every note of a voicing (harmonic tones, as in Part 5)."""
    fs, amps = [], []
    for k, m in enumerate(midis):
        f, a = _cons.harmonic_partials(hz(m), n=n, rolloff=rolloff)
        fs.append(f)
        amps.append(a * (1.0 if gains is None else gains[k]))
    return np.concatenate(fs), np.concatenate(amps)


def spacing_roughness(midis, n: int = 7, rolloff: float = 0.88) -> float:
    """The roughness of a voicing by Part 5's model (Plomp and Levelt's curve, summed over every pair of partials)."""
    return float(_cons.roughness(*chord_partials(midis, n=n, rolloff=rolloff)))


def dyad_by_register(semitones: int, basses, n: int = 7, rolloff: float = 0.88) -> np.ndarray:
    """An interval's roughness with its lower note on each of ``basses`` (MIDI numbers)."""
    return np.array([spacing_roughness([b, b + semitones], n=n, rolloff=rolloff) for b in basses])


def low_limit(semitones: int, reference: float | None = None, lo: int = 21, hi: int = 84, n: int = 7, rolloff: float = 0.88) -> int:
    """The lowest bass note (MIDI) from which upwards an interval is never rougher than ``reference``: by default
    the roughness of a major third on middle C.  Below it, the two notes' low partials fall inside one critical
    band."""
    ref = spacing_roughness([60, 64], n=n, rolloff=rolloff) if reference is None else reference
    r = dyad_by_register(semitones, range(lo, hi + 1), n=n, rolloff=rolloff)
    bad = np.nonzero(r > ref)[0]
    return lo if len(bad) == 0 else int(lo + bad[-1] + 1)


def voicings(pcs, low: int = 36, high: int = 84, voices: int = 4, bass: int | None = None, max_gap: int = 24) -> list[tuple[int, ...]]:
    """Every way to give ``voices`` notes between ``low`` and ``high`` to a chord so that each of its notes is
    there at least once, no two voices share a key, and neighbours are no more than ``max_gap`` apart.  ``bass``
    fixes the lowest note's pitch class."""
    pcs = sorted({int(p) % 12 for p in pcs})
    keys = [m for m in range(low, high + 1) if m % 12 in pcs]
    out = []

    def grow(cur):
        if len(cur) == voices:
            if {m % 12 for m in cur} == set(pcs):
                out.append(tuple(cur))
            return
        for m in keys:
            if cur and (m <= cur[-1] or m - cur[-1] > max_gap):
                continue
            if not cur and bass is not None and m % 12 != bass % 12:
                continue
            grow(cur + [m])

    grow([])
    return out


def motion(a, b) -> int:
    """Total semitones moved, voice by voice, between two voicings of the same number of voices."""
    return int(sum(abs(int(x) - int(y)) for x, y in zip(a, b)))


def nearest_voicing(prev, pcs, low: int | None = None, high: int | None = None, bass: int | None = None) -> tuple[int, ...]:
    """The voicing of ``pcs`` that moves least from ``prev`` (same number of voices), keeping every chord note."""
    prev = tuple(int(m) for m in prev)
    lo = (min(prev) - 7) if low is None else low
    hi_ = (max(prev) + 7) if high is None else high
    cands = voicings(pcs, lo, hi_, voices=len(prev), bass=bass)
    if not cands:
        raise ValueError("no voicing in range")
    return min(cands, key=lambda v: (motion(prev, v), abs(sum(v) - sum(prev))))


def voice_leading(a, b) -> dict:
    """The least total motion (in semitones, on the clock of twelve) that carries one chord's notes onto another's
    of the same size, and how each note moves."""
    a, b = [int(x) % 12 for x in a], [int(x) % 12 for x in b]
    if len(a) != len(b):
        raise ValueError("chords of one size only")
    best = None
    for perm in permutations(b):
        moves = [((y - x + 6) % 12) - 6 for x, y in zip(a, perm)]
        cost = sum(abs(m) for m in moves)
        if best is None or cost < best[0]:
            best = (cost, moves, perm)
    return {"cost": int(best[0]), "moves": [int(m) for m in best[1]], "to": [int(x) for x in best[2]]}


# ---------------------------------------------------------------------------
# The Tonnetz (Euler 1739): fifths along one axis, major thirds along the other
# ---------------------------------------------------------------------------
def tonnetz(pc: int) -> tuple[int, int]:
    """One place for a note on the lattice: ``a`` fifths and ``b`` major thirds from C, with b in (-1, 0, 1)."""
    pc = int(pc) % 12
    for b in (0, 1, -1):
        for a in range(-1, 3):
            if (7 * a + 4 * b) % 12 == pc:
                return a, b
    raise AssertionError


def at(a: int, b: int) -> int:
    """The note ``a`` fifths and ``b`` major thirds from C."""
    return (7 * a + 4 * b) % 12


Triad = tuple          # (root pitch class, "major" | "minor")


def triad_pcs(t: Triad) -> tuple[int, int, int]:
    r, k = t
    return (r % 12, (r + (4 if k == "major" else 3)) % 12, (r + 7) % 12)


def P(t: Triad) -> Triad:
    """Parallel: C major to C minor.  The third moves a semitone."""
    return (t[0], "minor" if t[1] == "major" else "major")


def R(t: Triad) -> Triad:
    """Relative: C major to A minor.  The fifth moves a whole tone."""
    return ((t[0] + 9) % 12, "minor") if t[1] == "major" else ((t[0] + 3) % 12, "major")


def L(t: Triad) -> Triad:
    """Leading-note exchange: C major to E minor.  The root moves a semitone."""
    return ((t[0] + 4) % 12, "minor") if t[1] == "major" else ((t[0] + 8) % 12, "major")


MOVES = {"P": P, "L": L, "R": R}


def cycle(start: Triad, word: str) -> list[Triad]:
    """Apply the moves of ``word`` over and over until the first triad returns: ``"PL"`` gives six triads,
    ``"PR"`` eight, ``"LR"`` all twenty-four."""
    out, cur, k = [start], start, 0
    while True:
        cur = MOVES[word[k % len(word)]](cur)
        k += 1
        if cur == start and k % len(word) == 0:
            return out
        out.append(cur)
        if k > 200:
            raise RuntimeError("no cycle")


def triad_name(t: Triad, flats: bool = True) -> str:
    return pitch_label(t[0], flats=flats) + ("" if t[1] == "major" else "m")


def tonnetz_distance(a: Triad, b: Triad) -> int:
    """The fewest P, L and R moves from one triad to another."""
    seen, frontier, d = {a}, [a], 0
    while frontier:
        if b in frontier:
            return d
        nxt = []
        for t in frontier:
            for f in (P, L, R):
                u = f(t)
                if u not in seen:
                    seen.add(u)
                    nxt.append(u)
        frontier, d = nxt, d + 1
    raise AssertionError


# ---------------------------------------------------------------------------
# A listener: a chord named from its sound
# ---------------------------------------------------------------------------
def chroma(y, sr: int, lo: float = 55.0, hi: float = 2000.0, n_fft: int | None = None) -> np.ndarray:
    """How much of a sound's energy lies on each of the twelve notes, octaves folded together: the spectrum's
    magnitude between ``lo`` and ``hi``, each bin given to the nearest note."""
    y = np.asarray(y, dtype=np.float64)
    if y.ndim > 1:
        y = y.mean(axis=-1) if y.shape[-1] <= 2 else y.mean(axis=0)
    n = len(y) if n_fft is None else n_fft
    spec = np.abs(np.fft.rfft(y[:n] * np.hanning(min(n, len(y))), n))
    f = np.fft.rfftfreq(n, 1.0 / sr)
    keep = (f >= lo) & (f <= hi)
    midi = 69.0 + 12.0 * np.log2(f[keep] / 440.0)
    near = np.round(midi)
    close = np.abs(midi - near) < 0.35
    out = np.zeros(12)
    np.add.at(out, (near[close].astype(int)) % 12, spec[keep][close] ** 2)
    return out / max(float(out.sum()), 1e-30)


def templates(kinds=("major", "minor"), harmonics: int = 1, decay: float = 0.6) -> dict:
    """What each chord's chroma should look like: its notes (``harmonics=1``), or its notes with the notes their
    first few harmonics fall on, each ``decay`` of the one before."""
    out = {}
    for r, k in product(range(12), kinds):
        v = np.zeros(12)
        for h in offsets(k):
            for j in range(1, harmonics + 1):
                v[(r + h + int(round(12 * np.log2(j)))) % 12] += decay ** (j - 1)
        out[(r, k)] = v / np.linalg.norm(v)
    return out


def recognise(c, kinds=("major", "minor"), harmonics: int = 1) -> dict:
    """The chord whose template is closest to a chroma vector (largest cosine), with the runner-up."""
    c = np.asarray(c, dtype=np.float64)
    c = c / max(float(np.linalg.norm(c)), 1e-30)
    scores = sorted(((float(v @ c), key) for key, v in templates(kinds, harmonics).items()), reverse=True)
    return {"root": scores[0][1][0], "kind": scores[0][1][1], "score": scores[0][0], "second": {"root": scores[1][1][0], "kind": scores[1][1][1], "score": scores[1][0]}}
