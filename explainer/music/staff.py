"""An engraver for Monochord's scores: staff notation drawn in manim, every note a mobject of its own.

    staff = Staff(score, width=11.5, systems=2)        # lays the whole voice out on two systems
    staff.notes[k]                                     # the k-th note (head, stem, flag, dot, accidental)
    staff.x_at(when) / staff.point_at(when)            # where a moment of the score (in whole notes) is on the page
    staff.cursor()                                     # a playhead; ``staff.follow(cursor, score)`` drives it from a sound

It draws one voice to a staff: clefs (treble, bass, alto), key and time signatures, notes from a whole to a
sixteenth with dots, stems, flags and beams, accidentals by the usual rules, ledger lines, rests, ties, barlines
and words.  Since Part 13 a voice's event can be a chord: its heads share a stem, a second puts one head on the
other side of it, and accidentals take columns so that none touches another (``note.heads``, low to high, can be
coloured one by one).  ``GrandStaff`` sets two voices on a treble and a bass staff, joined by a brace, with the
same moment at the same place across the page.  Noteheads, stems, beams and flags are drawn; clefs, accidentals,
the shorter rests and the digits come from a font that has the Unicode musical symbols (FreeSerif on this
machine).  It is not a full engraver (no second voice on a staff, no slurs), and where the series needs those it
will grow.
"""

from __future__ import annotations

import subprocess
from fractions import Fraction
from functools import lru_cache

import numpy as np
from manim import (DOWN, LEFT, RIGHT, UP, WHITE, ArcBetweenPoints, Brace, CubicBezier, Dot, Ellipse, Line, Polygon, Rectangle, Text, VGroup,
                   VMobject)

from explainer.music.monochord.score import Score, pitches_of, value


def _base(dur: Fraction) -> Fraction:
    """The undotted value of a duration: a dotted quarter's is a quarter."""
    _, dots = value(dur)
    return Fraction(dur) / (Fraction(1), Fraction(3, 2), Fraction(7, 4))[dots]

TREBLE, BASS, ALTO = "\U0001D11E", "\U0001D122", "\U0001D121"
SHARP, FLAT, NATURAL, DOUBLE_SHARP, DOUBLE_FLAT = "♯", "♭", "♮", "\U0001D12A", "\U0001D12B"
REST = {Fraction(1, 4): "\U0001D13D", Fraction(1, 8): "\U0001D13E", Fraction(1, 16): "\U0001D13F"}
SHARP_POS = {"treble": (8, 5, 9, 6, 3, 7, 4), "bass": (6, 3, 7, 4, 1, 5, 2), "alto": (7, 4, 8, 5, 2, 6, 3)}
FLAT_POS = {"treble": (4, 7, 3, 6, 2, 5, 1), "bass": (2, 5, 1, 4, 0, 3, -1), "alto": (3, 6, 2, 5, 1, 4, 0)}
SHARP_ORDER, FLAT_ORDER = "FCGDAEB", "BEADGCF"


@lru_cache(maxsize=1)
def music_font() -> str:
    """A font on this machine that has the Unicode musical symbols (the treble clef, U+1D11E)."""
    try:
        out = subprocess.run(["fc-list", ":charset=1d11e", "family"], capture_output=True, text=True, timeout=20).stdout
    except Exception:
        out = ""
    names = [line.split(",")[0].strip() for line in out.splitlines() if line.strip()]
    for want in ("FreeSerif", "Bravura Text", "Noto Music", "Symbola"):
        if want in names:
            return want
    for n in names:
        if "Unifont" not in n:
            return n
    raise RuntimeError("no font with musical symbols found: install GNU FreeFont (fonts-freefont-ttf), Noto Music or Bravura Text")


def glyph(char: str, height: float, color=WHITE) -> Text:
    g = Text(char, font=music_font(), font_size=96, color=color)
    g.scale(height / g.height)
    return g


class Staff(VGroup):
    """One voice of a score on a five-line staff.  ``space`` is the distance between two lines; everything else is
    measured in it.  ``systems`` breaks the music into that many lines of equal numbers of bars."""

    def __init__(self, score: Score, voice: int = 0, width: float = 11.5, space: float = 0.2, systems: int = 1, color=WHITE, line_color=None,
                 show_clef: bool = True, show_key: bool = True, show_time: bool = True, lyrics: bool = True, system_gap: float = 10.5,
                 bars=None, final_bar: bool = True, lyric_size: int = 22, proportional: bool = False, lead: float | None = None,
                 carry: bool = True, **kw):
        super().__init__(**kw)
        self.carry = carry                                     # False: every event is spelled afresh from the key (a row of separate chords)
        self.proportional, self.lead = proportional, lead      # for staves that must line up: room in proportion to time, notes from a fixed x
        self.score, self.voice_index, self.space, self.color = score, voice, space, color
        self.line_color = line_color or color
        self.clef_name = score.voices[voice].clef
        all_bars = score.measures(voice)
        first = 0
        if bars is not None:
            first, stop = bars
            all_bars = all_bars[first:stop]
        self.notes, self.rests, self.events, self.barlines, self.systems = [], [], [], VGroup(), VGroup()
        self._track = []                                   # (time in whole notes, point) for every event, in order
        per = int(np.ceil(len(all_bars) / systems))
        start = score.bar * first
        for k in range(systems):
            chunk = all_bars[k * per: (k + 1) * per]
            if not chunk:
                break
            sys_ = self._system(chunk, start, width, first_system=(k == 0), last=(k == systems - 1) and final_bar,
                                show_clef=show_clef, show_key=show_key, show_time=show_time and k == 0, lyrics=lyrics, lyric_size=lyric_size)
            sys_.shift(DOWN * k * system_gap * space)
            self.systems.add(sys_)
            start += sum((e.dur for bar in chunk for e in bar), Fraction(0))
        self.add(self.systems)
        self.end_time = start

    # ------------------------------------------------------------------ geometry
    def _y(self, pos: float) -> float:
        return (pos - 4) * self.space / 2.0                # the middle line is at y = 0

    def _system(self, bars, t0, width, first_system, last, show_clef, show_key, show_time, lyrics, lyric_size) -> VGroup:
        s, col = self.space, self.color
        g = VGroup()
        left = -width / 2
        lines = VGroup(*[Line([left, self._y(2 * i), 0], [left + width, self._y(2 * i), 0], color=self.line_color, stroke_width=1.6) for i in range(5)])
        g.add(lines)
        g.lines = lines
        x = left + 0.5 * s
        if show_clef:
            c = self._clef()
            c.move_to([x + c.width / 2, c.get_y(), 0])
            g.add(c)
            g.clef = c
            x += c.width + 0.7 * s
        if show_key and self.score.key:
            ks = self._key_signature(x)
            g.add(ks)
            x = ks.get_right()[0] + 0.8 * s
        if show_time:
            ts = self._time_signature(x)
            g.add(ts)
            x = ts.get_right()[0] + 1.0 * s
        x += 0.8 * s
        if self.lead is not None:
            x = left + self.lead
        # spacing: every event gets room that grows with its length, but more slowly
        room = (lambda d: 3.6 * s * float(d) / 0.25) if self.proportional else (lambda d: 2.6 * s * (float(d) / 0.25) ** 0.55 + 1.3 * s)          # noqa: E731
        natural = sum(room(e.dur) for bar in bars for e in bar) + len(bars) * 1.6 * s
        avail = left + width - x - (0.6 * s if last else 0.2 * s)
        k = avail / natural
        t = t0
        state_key = self._key_alters()
        for b, bar in enumerate(bars):
            alters = dict(state_key)
            group_notes = []
            for e in bar:
                if not self.carry:
                    alters = dict(state_key)
                w = room(e.dur) * k
                cx = x + 0.9 * s * k + 0.6 * s
                if e.is_rest:
                    r = self._rest(e.dur, cx)
                    g.add(r)
                    self.rests.append(r)
                    self.events.append(r)
                    r.time, r.dur = t, e.dur
                else:
                    n = self._note(e, cx, alters)
                    g.add(n)
                    self.notes.append(n)
                    self.events.append(n)
                    n.time, n.dur, n.event = t, e.dur, e
                    group_notes.append(n)
                    if lyrics and e.lyric:
                        word = Text(e.lyric, font_size=lyric_size, color=col).scale(0.6)
                        word.move_to([cx, self._y(-6.0), 0])
                        g.add(word)
                        n.lyric = word
                self._track.append((t, self.events[-1], g))
                t += e.dur
                x += w
            self._beam(group_notes, g)
            x += 0.8 * s * k
            final = last and b == len(bars) - 1
            bl = Line([x, self._y(0), 0], [x, self._y(8), 0], color=self.line_color, stroke_width=1.8)
            if final:
                bl = VGroup(Line([left + width - 0.45 * s, self._y(0), 0], [left + width - 0.45 * s, self._y(8), 0], color=self.line_color, stroke_width=1.8),
                            Line([left + width, self._y(0), 0], [left + width, self._y(8), 0], color=self.line_color, stroke_width=6))
            elif b == len(bars) - 1:
                bl = Line([left + width, self._y(0), 0], [left + width, self._y(8), 0], color=self.line_color, stroke_width=1.8)
            g.add(bl)
            self.barlines.add(bl)
            x += 0.8 * s * k
        self._ties(g)
        self._track.append((t, None, g))
        g.t0, g.t1 = t0, t
        return g

    # ------------------------------------------------------------------ signs
    def _clef(self) -> VMobject:
        s = self.space
        if self.clef_name == "treble":
            c = glyph(TREBLE, 7.3 * s, self.color)
            c.move_to([0, self._y(4.55), 0])                 # the curl sits round the G line
        elif self.clef_name == "bass":
            c = glyph(BASS, 3.35 * s, self.color)
            c.move_to([0, self._y(5.35), 0])                 # the dots straddle the F line
        else:
            c = glyph(ALTO, 4.0 * s, self.color)
            c.move_to([0, self._y(4), 0])
        return c

    def _accidental(self, alter: int) -> VMobject:
        s = self.space
        if alter == 1:
            return glyph(SHARP, 2.7 * s, self.color)
        if alter == -1:
            f = glyph(FLAT, 2.45 * s, self.color)
            f.shift(UP * 0.55 * s)                           # a flat's bowl, not its middle, sits on the note
            return f
        if alter == 0:
            return glyph(NATURAL, 2.7 * s, self.color)
        if alter == 2:
            return glyph(DOUBLE_SHARP, 1.1 * s, self.color)
        f = glyph(DOUBLE_FLAT, 2.45 * s, self.color)
        f.shift(UP * 0.55 * s)
        return f

    def _key_alters(self) -> dict:
        k = self.score.key
        out = {st: 0 for st in "CDEFGAB"}
        for st in (SHARP_ORDER[:k] if k > 0 else FLAT_ORDER[:-k] if k < 0 else ""):
            out[st] = 1 if k > 0 else -1
        return out

    def _key_signature(self, x: float) -> VGroup:
        s, k = self.space, self.score.key
        g = VGroup()
        table = SHARP_POS if k > 0 else FLAT_POS
        for i in range(abs(k)):
            a = self._accidental(1 if k > 0 else -1)
            a.shift([x + (i + 0.5) * 1.05 * s - a.get_center()[0], self._y(table[self.clef_name][i]), 0])
            g.add(a)
        return g

    def _time_signature(self, x: float) -> VGroup:
        s = self.space
        top = Text(str(self.score.time[0]), font=music_font(), weight="BOLD", font_size=96, color=self.color)
        bot = Text(str(self.score.time[1]), font=music_font(), weight="BOLD", font_size=96, color=self.color)
        for d, pos in ((top, 6), (bot, 2)):
            d.scale(1.9 * s / d.height)
            d.move_to([x + max(top.width, bot.width) / 2, self._y(pos), 0])
        return VGroup(top, bot)

    # ------------------------------------------------------------------ notes and rests
    def _head(self, dur: Fraction, at) -> VMobject:
        s = self.space
        base = _base(dur)
        if base >= 1:
            outer = Ellipse(width=1.75 * s, height=1.0 * s, color=self.color, stroke_width=0, fill_color=self.color, fill_opacity=1)
            inner = Ellipse(width=0.85 * s, height=0.62 * s, stroke_width=0, fill_color="#0B0E14", fill_opacity=1).rotate(-0.9)
            h = VGroup(outer, inner)
        elif base >= Fraction(1, 2):
            outer = Ellipse(width=1.32 * s, height=0.92 * s, color=self.color, stroke_width=0, fill_color=self.color, fill_opacity=1).rotate(0.36)
            inner = Ellipse(width=1.02 * s, height=0.42 * s, stroke_width=0, fill_color="#0B0E14", fill_opacity=1).rotate(0.36)
            h = VGroup(outer, inner)
        else:
            h = VGroup(Ellipse(width=1.32 * s, height=0.92 * s, color=self.color, stroke_width=0, fill_color=self.color, fill_opacity=1).rotate(0.36))
        h.move_to(at)
        h.base = base
        return h

    def _note(self, e, cx: float, alters: dict) -> VGroup:
        pitches = pitches_of(e)
        if len(pitches) > 1:
            return self._chord(e, pitches, cx, alters)
        s, col = self.space, self.color
        pos = e.pitch.staff_position(self.clef_name)
        at = np.array([cx, self._y(pos), 0.0])
        n = VGroup()
        head = self._head(e.dur, at)
        n.head, n.pos, n.x = head, pos, cx
        n.pos_lo = n.pos_hi = pos
        n.heads = [head]
        n.pitches = pitches
        n.ink = head[0]                                    # the part of the head that takes a colour (a hollow head has a hole)
        # ledger lines
        ledgers = VGroup()
        for p in list(range(-2, pos - 1, -2)) + list(range(10, pos + 1, 2)):
            ledgers.add(Line([cx - 1.05 * s, self._y(p), 0], [cx + 1.05 * s, self._y(p), 0], color=self.line_color, stroke_width=1.6))
        n.add(ledgers)
        n.ledgers = ledgers
        n.add(head)
        # the stem
        n.stem = None
        n.up = pos < 4
        if head.base < 1:
            n.stem = self._stem(n, 3.5 * s)
            n.add(n.stem)
        # an accidental, if this bar does not already say so
        n.accidental = None
        if alters.get(e.pitch.step, 0) != e.pitch.alter:
            a = self._accidental(e.pitch.alter)
            a.shift([cx - 1.25 * s - a.get_center()[0], at[1], 0])
            n.add(a)
            n.accidental = a
            alters[e.pitch.step] = e.pitch.alter
        # dots
        dots = 0 if head.base == e.dur else (1 if e.dur / head.base == Fraction(3, 2) else 2)
        for d in range(dots):
            n.add(Dot([cx + (1.15 + 0.55 * d) * s, self._y(pos + (1 if pos % 2 == 0 else 0)), 0], radius=0.16 * s, color=col))
        n.flags = VGroup()
        n.add(n.flags)
        n.beamed = False
        return n

    def _chord(self, e, pitches, cx: float, alters: dict) -> VGroup:
        """Several heads on one stem.  ``n.heads`` are the parts that take a colour, from the lowest note up."""
        s, col = self.space, self.color
        poss = [p.staff_position(self.clef_name) for p in pitches]
        lo, hi = poss[0], poss[-1]
        base = _base(e.dur)
        n = VGroup()
        n.up = (4 - lo) > (hi - 4)                          # the note farthest from the middle line decides
        wide = (1.62 if base >= 1 else 1.2) * s
        # a second cannot sit in one column: the upper note goes right of the stem, the lower one left of it
        side = [0] * len(poss)
        order = range(len(poss)) if n.up else range(len(poss) - 1, -1, -1)
        prev = None
        for i in order:
            if prev is not None and abs(poss[i] - poss[prev]) == 1 and side[prev] == 0:
                side[i] = 1 if n.up else -1
            prev = i
        ledgers = VGroup()
        left = cx - 1.05 * s - (wide if -1 in side else 0.0)
        right = cx + 1.05 * s + (wide if 1 in side else 0.0)
        for pl in list(range(-2, lo - 1, -2)) + list(range(10, hi + 1, 2)):
            ledgers.add(Line([left, self._y(pl), 0], [right, self._y(pl), 0], color=self.line_color, stroke_width=1.6))
        n.add(ledgers)
        n.ledgers = ledgers
        inks, holes = VGroup(), VGroup()
        for pos, sd in zip(poss, side):
            h = self._head(e.dur, np.array([cx + sd * wide, self._y(pos), 0.0]))
            h[0].base = base
            inks.add(h[0])
            if len(h) > 1:
                holes.add(h[1])
        n.add(inks, holes)
        n.ink, n.heads, n.holes = inks, list(inks), holes
        anchor = 0 if n.up else len(poss) - 1               # where the stem begins; never a displaced head
        n.head = inks[anchor]
        n.pos, n.pos_lo, n.pos_hi, n.x, n.pitches = (hi if n.up else lo), lo, hi, cx, pitches
        n.stem = None
        if base < 1:
            n.stem = self._stem(n, 3.5 * s)
            n.add(n.stem)
        # accidentals, from the top note down, each in the nearest column where it touches no other
        n.accidentals, columns = VGroup(), []
        n.accidental = None
        x0 = cx - 1.25 * s - (wide if -1 in side else 0.0)
        for i in range(len(pitches) - 1, -1, -1):
            pch = pitches[i]
            if alters.get(pch.step, 0) == pch.alter:
                continue
            alters[pch.step] = pch.alter
            c = 0
            while c < len(columns) and any(abs(poss[i] - q) < 6 for q in columns[c]):
                c += 1
            if c == len(columns):
                columns.append([])
            columns[c].append(poss[i])
            acc = self._accidental(pch.alter)
            acc.shift([x0 - 1.0 * s * c - acc.get_center()[0], self._y(poss[i]), 0])
            n.accidentals.add(acc)
        n.add(n.accidentals)
        if len(n.accidentals):
            n.accidental = n.accidentals
        dots = 0 if base == e.dur else (1 if e.dur / base == Fraction(3, 2) else 2)
        used = set()
        for pos in poss:
            dp = pos if pos % 2 else (pos + 1 if pos + 1 not in used else pos - 1)
            if dp in used:
                continue
            used.add(dp)
            for d in range(dots):
                n.add(Dot([cx + (1.15 + 0.55 * d) * s + (wide if 1 in side else 0.0), self._y(dp), 0], radius=0.16 * s, color=col))
        n.flags = VGroup()
        n.add(n.flags)
        n.beamed = False
        return n

    def _stem_start(self, n, up: bool) -> np.ndarray:
        """Where a note's stem leaves its heads: beside the lowest head for a stem up, the highest for a stem down."""
        s = self.space
        c = np.array([n.x, self._y(n.pos_lo if up else n.pos_hi), 0.0])
        return c + (RIGHT * 0.61 * s + UP * 0.12 * s if up else LEFT * 0.61 * s + DOWN * 0.12 * s)

    def _stem(self, n, length: float) -> Line:
        a = self._stem_start(n, n.up)
        far = self._y(n.pos_hi if n.up else n.pos_lo) + (0.12 * self.space if n.up else -0.12 * self.space)
        end = np.array([a[0], far + (length if n.up else -length), 0.0])
        return Line(a, end, color=self.color, stroke_width=1.8)

    def _flag(self, n, count: int) -> None:
        s = self.space
        tip = n.stem.get_end()
        sgn = -1.0 if n.up else 1.0                       # a flag hangs back towards the head
        for i in range(count):
            p0 = tip + UP * sgn * 0.75 * s * i
            n.flags.add(CubicBezier(p0, p0 + RIGHT * 0.2 * s + UP * sgn * 0.9 * s, p0 + RIGHT * 1.15 * s + UP * sgn * 1.2 * s, p0 + RIGHT * 0.85 * s + UP * sgn * 2.4 * s,
                                    color=self.color, stroke_width=2.6))

    def _beam(self, notes, g: VGroup) -> None:
        """Join the eighths and sixteenths of a bar that share a beat; give the rest of them flags."""
        s = self.space
        beat = Fraction(3, 8) if (self.score.time[1] == 8 and self.score.time[0] % 3 == 0) else Fraction(1, 4)
        groups, cur = [], []
        for n in notes:
            short = n.head.base <= Fraction(1, 8)
            same = cur and (n.time // beat == cur[-1].time // beat) and cur[-1].time + cur[-1].dur == n.time
            if short and (same or not cur):
                cur.append(n)
            else:
                if cur:
                    groups.append(cur)
                cur = [n] if short else []
        if cur:
            groups.append(cur)
        for grp in groups:
            if len(grp) == 1:
                self._flag(grp[0], 1 if grp[0].head.base == Fraction(1, 8) else 2)
                continue
            up = float(np.mean([(n.pos_lo + n.pos_hi) / 2 for n in grp])) < 4
            ys = []
            for n in grp:                                  # all stems one way, long enough to reach a common beam
                n.up = up
            first, lastn = grp[0], grp[-1]
            far = (lambda n: n.pos_hi) if up else (lambda n: n.pos_lo)                                          # noqa: E731
            slope = float(np.clip((far(lastn) - far(first)) * s / 2 / max(lastn.x - first.x, 1e-6), -0.25, 0.25))
            ext = (max(far(n) for n in grp) if up else min(far(n) for n in grp))
            y_ref = self._y(ext) + (3.4 * s if up else -3.4 * s)
            x_ref = max(grp, key=far).x if up else min(grp, key=far).x
            for n in grp:
                n.remove(n.stem)
                a = self._stem_start(n, up)
                yb = y_ref + slope * (a[0] - x_ref)
                n.stem = Line(a, np.array([a[0], yb, 0.0]), color=self.color, stroke_width=1.8)
                n.add(n.stem)
                n.beamed = True
                ys.append(n.stem.get_end())
            th = 0.5 * s * (-1 if up else 1)
            beam = Polygon(ys[0], ys[-1], ys[-1] + UP * th, ys[0] + UP * th, stroke_width=0, fill_color=self.color, fill_opacity=1)
            g.add(beam)
            for i, n in enumerate(grp):                    # a second beam for sixteenths: joined to a neighbour, or a stub
                if n.head.base > Fraction(1, 16):
                    continue
                j = i + 1 if (i + 1 < len(grp) and grp[i + 1].head.base <= Fraction(1, 16)) else None
                p = ys[i] + UP * 1.5 * th
                if j is not None:
                    q = ys[j] + UP * 1.5 * th
                elif i > 0 and grp[i - 1].head.base <= Fraction(1, 16):
                    continue
                else:
                    d = 1.0 if i == 0 else -1.0
                    q = p + np.array([d * 1.0 * s, slope * d * 1.0 * s, 0.0])
                g.add(Polygon(p, q, q + UP * th, p + UP * th, stroke_width=0, fill_color=self.color, fill_opacity=1))

    def _rest(self, dur: Fraction, cx: float) -> VMobject:
        s = self.space
        base = _base(dur)
        if base >= 1:
            r = VGroup(Rectangle(width=1.3 * s, height=0.5 * s, stroke_width=0, fill_color=self.color, fill_opacity=1).move_to([cx, self._y(6) - 0.25 * s, 0]))
        elif base == Fraction(1, 2):
            r = VGroup(Rectangle(width=1.3 * s, height=0.5 * s, stroke_width=0, fill_color=self.color, fill_opacity=1).move_to([cx, self._y(4) + 0.25 * s, 0]))
        else:
            ch = REST.get(base, REST[Fraction(1, 16)])
            h = {Fraction(1, 4): 3.0, Fraction(1, 8): 1.9}.get(base, 2.6) * s
            r = VGroup(glyph(ch, h, self.color).move_to([cx, self._y(4), 0]))
        if base != dur:
            r.add(Dot([cx + 1.1 * s, self._y(5), 0], radius=0.16 * s, color=self.color))
        r.x = cx
        return r

    def _ties(self, g: VGroup) -> None:
        s = self.space
        mine = [n for n in self.notes if n in g.submobjects]
        for a, b in zip(mine, mine[1:]):
            if not a.event.tie:
                continue
            shared = [pch for pch in a.pitches if pch in b.pitches]
            for j, pch in enumerate(shared):
                ha, hb = a.heads[a.pitches.index(pch)], b.heads[b.pitches.index(pch)]
                below = (a.pos < 4) if len(shared) == 1 else (j < (len(shared) + 1) // 2)       # in a chord: lower ties curve down, upper up
                off = (DOWN if below else UP) * 0.75 * s
                p, q = ha.get_center() + off + RIGHT * 0.5 * s, hb.get_center() + off + LEFT * 0.5 * s
                g.add(ArcBetweenPoints(p, q, angle=(0.9 if below else -0.9), color=self.color, stroke_width=2.2))

    # ------------------------------------------------------------------ time on the page
    def _where(self, entry) -> np.ndarray:
        _, mob, g = entry
        y = g.lines.get_center()[1]
        if mob is None:                                    # the end of a system
            return np.array([g.lines.get_right()[0] - 0.3 * self.space, y, 0.0])
        x = mob.head.get_center()[0] if hasattr(mob, "head") else mob.get_center()[0]
        return np.array([x, y, 0.0])

    def point_at(self, when) -> np.ndarray:
        """Where the moment ``when`` (whole notes from the start of the score) falls: on the middle line of the
        staff, between the events on either side of it.  At a line break the point runs to the end of its staff
        and then jumps to the next system."""
        when = float(when)
        tr = self._track
        if when <= float(tr[0][0]):
            return self._where(tr[0])
        for e0, e1 in zip(tr, tr[1:]):
            if float(e0[0]) <= when <= float(e1[0]) and float(e1[0]) > float(e0[0]):
                p0 = self._where(e0)
                p1 = self._where(e1) if e0[2] is e1[2] else self._where((e1[0], None, e0[2]))
                return p0 + (p1 - p0) * (when - float(e0[0])) / float(e1[0] - e0[0])
        return self._where(tr[-1])

    def x_at(self, when) -> float:
        return float(self.point_at(when)[0])

    def cursor(self, color="#F5C542", stroke_width: float = 3.0) -> Line:
        """A playhead: a line across the staff, at the start."""
        h = 6.5 * self.space
        c = Line(DOWN * h, UP * h, color=color, stroke_width=stroke_width)
        c.move_to(self.point_at(float(self._track[0][0])))
        return c

    def follow(self, tempo: float | None = None, t0: float = 0.0):
        """``fn(mob, t)`` for ``snd.drive``: moves a cursor so that it is over the note that is sounding, for a
        sound that plays the score from ``t0`` seconds at ``tempo`` quarter notes a minute (the score's own by
        default)."""
        qpm = tempo or self.score.tempo
        start = float(self._track[0][0])

        def fn(m, t):
            when = start + max(t - t0, 0.0) * qpm / 240.0
            return m.move_to(self.point_at(min(when, float(self.end_time))))

        return fn

    def note_at(self, when) -> int:
        """The index of the note sounding at ``when`` (whole notes), or -1."""
        for k, n in enumerate(self.notes):
            if float(n.time) <= float(when) < float(n.time + n.dur):
                return k
        return -1


class GrandStaff(VGroup):
    """Two voices of a score on a treble and a bass staff, joined by a brace: a keyboard's page.  Both staves give
    time the same room, so the same moment is at the same place across the page.  ``upper`` and ``lower`` are the
    two :class:`Staff` objects; ``notes_at(k)`` gives the k-th event of each."""

    def __init__(self, score: Score, voices=(0, 1), width: float = 11.5, space: float = 0.2, gap: float = 9.0, lead: float | None = None,
                 color=WHITE, line_color=None, brace: bool = True, **kw):
        super().__init__()
        lead = (4.6 + 1.05 * abs(score.key) + (2.6 if kw.get("show_time", True) else 0.0)) * space if lead is None else lead
        self.space = space
        self.upper = Staff(score, voices[0], width=width, space=space, proportional=True, lead=lead, color=color, line_color=line_color, **kw)
        self.lower = Staff(score, voices[1], width=width, space=space, proportional=True, lead=lead, color=color, line_color=line_color, **kw)
        self.lower.shift(self.upper.systems[0].lines.get_center() - self.lower.systems[0].lines.get_center() + DOWN * gap * space)
        self.add(self.upper, self.lower)
        lc = line_color or color
        top, bot = self.upper.systems[0].lines, self.lower.systems[0].lines
        x = top.get_left()[0]
        self.joins = VGroup(Line([x, top.get_top()[1], 0], [x, bot.get_bottom()[1], 0], color=lc, stroke_width=1.8))
        for bu, bl in zip(self.upper.barlines, self.lower.barlines):                 # barlines run through both staves
            self.joins.add(Line([bu.get_right()[0], top.get_bottom()[1], 0], [bl.get_right()[0], bot.get_top()[1], 0], color=lc, stroke_width=1.8))
        self.add(self.joins)
        if brace:
            self.brace = Brace(Line([x, bot.get_bottom()[1], 0], [x, top.get_top()[1], 0]), direction=LEFT, buff=0.06, color=color)
            self.add(self.brace)

    def notes_at(self, k: int) -> tuple:
        return self.upper.notes[k], self.lower.notes[k]

    def point_at(self, when) -> np.ndarray:
        p, q = self.upper.point_at(when), self.lower.point_at(when)
        return (p + q) / 2

    def cursor(self, color="#F5C542", stroke_width: float = 3.0) -> Line:
        top, bot = self.upper.systems[0].lines, self.lower.systems[0].lines
        h = (top.get_top()[1] - bot.get_bottom()[1]) / 2 + 1.2 * self.space
        c = Line(DOWN * h, UP * h, color=color, stroke_width=stroke_width)
        c.move_to(self.point_at(float(self.upper._track[0][0])))
        return c

    def follow(self, tempo: float | None = None, t0: float = 0.0):
        qpm = tempo or self.upper.score.tempo
        start = float(self.upper._track[0][0])

        def fn(m, t):
            when = start + max(t - t0, 0.0) * qpm / 240.0
            return m.move_to(self.point_at(min(when, float(self.upper.end_time))))

        return fn
