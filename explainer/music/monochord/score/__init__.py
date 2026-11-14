"""Monochord's score: music as symbols (Part 10, *Writing It Down*).

A score here is what a page of music is: spelled pitches (C sharp is not D flat), exact durations (fractions of a
whole note, never seconds), voices, a key, a metre and a tempo.  It knows nothing about sound; ``performed`` turns
it into the times and frequencies that the rest of Monochord plays.

    Pitch, Note, Chord, Rest, Voice, Score  the model (a Chord is several pitches struck together, Part 13)
    tune_score()                            the Tune, as a score
    write.musicxml / mei / midi / abc / lilypond / jianpu      what each notation keeps
    read.musicxml / midi                    and what comes back

No manim.  Checked in ``tests/music/test_score.py`` (round trips; what MIDI forgets).  The writers and readers
are for single lines: of a chord they write the lowest note.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from fractions import Fraction

from .. import tune as _tune
from ..pitch import midi_to_hz

STEPS = "CDEFGAB"
SEMITONES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
ACCIDENTAL = {-2: "bb", -1: "b", 0: "", 1: "#", 2: "##"}
VALUE_NAMES = {Fraction(1): "whole", Fraction(1, 2): "half", Fraction(1, 4): "quarter", Fraction(1, 8): "eighth", Fraction(1, 16): "16th",
               Fraction(1, 32): "32nd", Fraction(2): "breve"}
W = Fraction(1)
H, Q, E8, S16 = Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 16)


@dataclass(frozen=True)
class Pitch:
    """A written pitch: a letter, an alteration (-1 flat, +1 sharp) and an octave (C4 is middle C)."""
    step: str
    alter: int = 0
    octave: int = 4

    @staticmethod
    def parse(name: str) -> "Pitch":
        """``"C4"``, ``"F#3"``, ``"Bb5"``, ``"Ebb2"``."""
        step, rest = name[0].upper(), name[1:]
        alter = 0
        while rest and rest[0] in "#b♯♭":
            alter += 1 if rest[0] in "#♯" else -1
            rest = rest[1:]
        return Pitch(step, alter, int(rest))

    @staticmethod
    def from_midi(number: int, flats: bool = False) -> "Pitch":
        """A spelling for a key of the piano.  The key does not say which: that is what MIDI forgets."""
        octave, pc = divmod(int(number), 12)
        table = (("C", 0), ("D", -1), ("D", 0), ("E", -1), ("E", 0), ("F", 0), ("G", -1), ("G", 0), ("A", -1), ("A", 0), ("B", -1), ("B", 0)) if flats else \
                (("C", 0), ("C", 1), ("D", 0), ("D", 1), ("E", 0), ("F", 0), ("F", 1), ("G", 0), ("G", 1), ("A", 0), ("A", 1), ("B", 0))
        step, alter = table[pc]
        return Pitch(step, alter, octave - 1)

    @property
    def midi(self) -> int:
        return 12 * (self.octave + 1) + SEMITONES[self.step] + self.alter

    @property
    def diatonic(self) -> int:
        """Letters above C0: the pitch's height on a staff, ignoring accidentals."""
        return 7 * self.octave + STEPS.index(self.step)

    @property
    def name(self) -> str:
        return f"{self.step}{ACCIDENTAL[self.alter]}{self.octave}"

    def hz(self, a4: float = 440.0) -> float:
        """In twelve-tone equal temperament; a tuning from Part 6 can be used instead in ``performed``."""
        return midi_to_hz(self.midi, a4)

    def staff_position(self, clef: str = "treble") -> int:
        """Half-spaces above the bottom line of the staff (0 is the bottom line, 8 the top)."""
        bottom = {"treble": Pitch("E", 0, 4), "bass": Pitch("G", 0, 2), "alto": Pitch("F", 0, 3), "tenor": Pitch("D", 0, 3)}[clef]
        return self.diatonic - bottom.diatonic

    def up(self, steps: int, semitones: int) -> "Pitch":
        """The pitch a written interval above: so many letters, so many semitones (a major third is 2 and 4)."""
        d = self.diatonic + steps
        octave, idx = divmod(d, 7)
        natural = 12 * (octave + 1) + SEMITONES[STEPS[idx]]
        return Pitch(STEPS[idx], self.midi + semitones - natural, octave)


@dataclass(frozen=True)
class Note:
    pitch: Pitch
    dur: Fraction                      # in whole notes
    tie: bool = False                  # tied to the next note of the same pitch
    lyric: str | None = None

    @property
    def is_rest(self) -> bool:
        return False


@dataclass(frozen=True)
class Chord:
    """Several pitches struck together, for one duration.  Kept from the lowest up."""
    pitches: tuple
    dur: Fraction
    tie: bool = False
    lyric: str | None = None

    def __post_init__(self):
        object.__setattr__(self, "pitches", tuple(sorted(self.pitches, key=lambda p: (p.midi, p.diatonic))))

    @property
    def is_rest(self) -> bool:
        return False

    @property
    def pitch(self) -> Pitch:
        """The lowest note: the bass."""
        return self.pitches[0]


def pitches_of(e) -> tuple:
    """An event's pitches: one for a note, several for a chord, none for a rest."""
    if e.is_rest:
        return ()
    return tuple(getattr(e, "pitches", None) or (e.pitch,))


@dataclass(frozen=True)
class Rest:
    dur: Fraction

    @property
    def is_rest(self) -> bool:
        return True


def value(dur: Fraction) -> tuple[str, int]:
    """A duration's name and its number of dots: 3/8 is a dotted quarter."""
    dur = Fraction(dur)
    for dots, factor in ((0, Fraction(1)), (1, Fraction(3, 2)), (2, Fraction(7, 4))):
        base = dur / factor
        if base in VALUE_NAMES:
            return VALUE_NAMES[base], dots
    raise ValueError(f"no single note value lasts {dur} of a whole note")


@dataclass
class Voice:
    events: list = field(default_factory=list)
    name: str = ""
    clef: str = "treble"

    @property
    def length(self) -> Fraction:
        return sum((e.dur for e in self.events), Fraction(0))

    def onsets(self) -> list[tuple[Fraction, object]]:
        out, t = [], Fraction(0)
        for e in self.events:
            out.append((t, e))
            t += e.dur
        return out

    @property
    def notes(self) -> list[Note]:
        return [e for e in self.events if not e.is_rest]


@dataclass
class Score:
    voices: list = field(default_factory=list)
    key: int = 0                       # sharps (+) or flats (-) in the key signature
    time: tuple = (4, 4)
    tempo: float = 109.0               # quarter notes a minute
    title: str = ""

    @property
    def bar(self) -> Fraction:
        return Fraction(self.time[0], self.time[1])

    @property
    def length(self) -> Fraction:
        return max((v.length for v in self.voices), default=Fraction(0))

    def measures(self, voice: int = 0) -> list[list]:
        """A voice cut at the barlines.  A note that crosses a barline is split and tied, as an engraver would."""
        out, cur, room = [], [], self.bar
        for e in self.voices[voice].events:
            left = e.dur
            while left > 0:
                take = min(left, room)
                last = take == left
                if e.is_rest:
                    cur.append(Rest(take))
                else:
                    cur.append(replace(e, dur=take, tie=(e.tie if last else True), lyric=e.lyric if left == e.dur else None))
                left -= take
                room -= take
                if room == 0:
                    out.append(cur)
                    cur, room = [], self.bar
        if cur:
            out.append(cur)
        return out

    def seconds(self, whole_notes) -> float:
        return float(whole_notes) * 4 * 60.0 / self.tempo

    def performed(self, voice: int = 0, hz=None) -> list[dict]:
        """What a player does with the page: for every sounding note its start and length in seconds and its
        frequency (``hz(pitch)``; equal temperament by default).  Tied notes are joined; a chord gives one entry
        for each of its notes."""
        out, open_ties = [], {}
        for t, e in self.voices[voice].onsets():
            if e.is_rest:
                open_ties = {}
                continue
            still = {}
            for p in pitches_of(e):
                if p in open_ties:
                    k = open_ties[p]
                    out[k]["dur"] += self.seconds(e.dur)
                else:
                    k = len(out)
                    out.append({"t": self.seconds(t), "dur": self.seconds(e.dur), "pitch": p, "midi": p.midi, "hz": (hz or Pitch.hz)(p)})
                if e.tie:
                    still[p] = k
            open_ties = still
        return out


MAJOR = (0, 2, 4, 5, 7, 9, 11)


def degree_pitch(degree: int, tonic: Pitch) -> Pitch:
    """The pitch of a degree of the major scale on ``tonic`` (1 is the tonic), correctly spelled."""
    return tonic.up(degree - 1, MAJOR[(degree - 1) % 7] + 12 * ((degree - 1) // 7))


def key_of(tonic: Pitch) -> int:
    """The key signature of the major key on a tonic: its place on the line of fifths (C is 0, G is 1, F is -1)."""
    line = {"F": -1, "C": 0, "G": 1, "D": 2, "A": 3, "E": 4, "B": 5}
    return line[tonic.step] + 7 * tonic.alter


def quick(items, dur: Fraction = W, clef: str = "treble", key: int = 0, time: tuple | None = None, tempo: float = 109.0) -> Score:
    """A one-voice score from names: ``"C4"`` is a note, ``["C4", "E4", "G4"]`` a chord, ``None`` a rest, and
    ``(item, dur)`` gives one its own length.  With no ``time`` the whole row is one bar."""
    events = []
    for it in items:
        d = dur
        if isinstance(it, tuple) and len(it) == 2 and isinstance(it[1], Fraction):
            it, d = it
        if it is None:
            events.append(Rest(d))
        elif isinstance(it, (list, tuple)):
            events.append(Chord(tuple(Pitch.parse(n) if isinstance(n, str) else n for n in it), d))
        else:
            events.append(Note(Pitch.parse(it) if isinstance(it, str) else it, d))
    total = sum((e.dur for e in events), Fraction(0))
    if time is None:
        time = (int(total * 4), 4) if (total * 4).denominator == 1 else (int(total * 8), 8)
    return Score([Voice(events, clef=clef)], key=key, time=time, tempo=tempo)


def tune_score(tonic: str = "C4", unit: Fraction = Q, time: tuple = (4, 4), tempo: float = 109.0, words: bool = False) -> Score:
    """The Tune as a score: one voice, one note value to the beat."""
    t = Pitch.parse(tonic)
    lyr = list(_tune.WORDS)
    events = [Note(degree_pitch(d, t), unit * b, lyric=(lyr[k] if words and k < len(lyr) else None)) for k, (d, b) in enumerate(_tune.TUNE)]
    return Score([Voice(events, name="the Tune")], key=key_of(t), time=time, tempo=tempo, title="Ah! vous dirai-je, maman")
