"""Readers: what comes back from each notation, and so what it kept."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from fractions import Fraction

from . import Note, Pitch, Rest, Score, Voice


def musicxml(text: str) -> Score:
    """The MusicXML that :func:`write.musicxml` writes (one voice to a part, no chords)."""
    root = ET.fromstring(text)
    score = Score(title=(root.findtext("work/work-title") or ""))
    names = {p.get("id"): (p.findtext("part-name") or "") for p in root.iter("score-part")}
    clefs = {("G", "2"): "treble", ("F", "4"): "bass", ("C", "3"): "alto", ("C", "4"): "tenor"}
    for part in root.iter("part"):
        voice = Voice(name=names.get(part.get("id"), ""))
        divisions = 1
        for measure in part.iter("measure"):
            a = measure.find("attributes")
            if a is not None:
                divisions = int(a.findtext("divisions") or divisions)
                if a.find("key") is not None:
                    score.key = int(a.findtext("key/fifths"))
                if a.find("time") is not None:
                    score.time = (int(a.findtext("time/beats")), int(a.findtext("time/beat-type")))
                if a.find("clef") is not None:
                    voice.clef = clefs[(a.findtext("clef/sign"), a.findtext("clef/line"))]
            s = measure.find("direction/sound")
            if s is not None and s.get("tempo"):
                score.tempo = float(s.get("tempo"))
            for n in measure.iter("note"):
                dur = Fraction(int(n.findtext("duration")), 4 * divisions)
                if n.find("rest") is not None:
                    voice.events.append(Rest(dur))
                else:
                    p = Pitch(n.findtext("pitch/step"), int(n.findtext("pitch/alter") or 0), int(n.findtext("pitch/octave")))
                    tie = any(t.get("type") == "start" for t in n.iter("tie"))
                    voice.events.append(Note(p, dur, tie=tie, lyric=n.findtext("lyric/text")))
        score.voices.append(voice)
    return score


def _varlen(data: bytes, i: int) -> tuple[int, int]:
    n = 0
    while True:
        b = data[i]
        i += 1
        n = (n << 7) | (b & 0x7F)
        if not b & 0x80:
            return n, i


def midi(data: bytes, flats: bool = False) -> Score:
    """A Standard MIDI File back into a score, as far as that can be done.  The keys and the times come back.  The
    spellings are a guess (sharps, unless ``flats``), and the note values are whatever the times happen to be."""
    assert data[:4] == b"MThd"
    division = int.from_bytes(data[12:14], "big")
    i = 14
    assert data[i: i + 4] == b"MTrk"
    end = i + 8 + int.from_bytes(data[i + 4: i + 8], "big")
    i += 8
    score = Score()
    tick, status, on, notes = 0, 0, {}, []
    while i < end:
        delta, i = _varlen(data, i)
        tick += delta
        if data[i] == 0xFF:
            kind = data[i + 1]
            length, j = _varlen(data, i + 2)
            body = data[j: j + length]
            if kind == 0x51:
                score.tempo = 60_000_000 / int.from_bytes(body, "big")
            elif kind == 0x58:
                score.time = (body[0], 2 ** body[1])
            elif kind == 0x59:
                score.key = body[0] - 256 if body[0] > 127 else body[0]
            i = j + length
            continue
        if data[i] & 0x80:
            status = data[i]
            i += 1
        key, vel = data[i], data[i + 1]
        i += 2
        if status & 0xF0 == 0x90 and vel > 0:
            on[key] = tick
        elif status & 0xF0 in (0x80, 0x90) and key in on:
            notes.append((on.pop(key), tick, key))
    notes.sort()
    voice, now = Voice(), 0
    for start, stop, key in notes:
        if start > now:
            voice.events.append(Rest(Fraction(start - now, 4 * division)))
        voice.events.append(Note(Pitch.from_midi(key, flats), Fraction(stop - start, 4 * division)))
        now = stop
    score.voices.append(voice)
    return score
