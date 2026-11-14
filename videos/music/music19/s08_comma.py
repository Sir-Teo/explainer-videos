from __future__ import annotations

import numpy as np

from videos.music.music19.common import *  # noqa: F403


class Comma(SoundScene):
    def construct(self):
        chapter(self, 7, r"The comma it hides", r"Do four minor thirds make an octave?")
        self.quiz()
        self.ladder()
        self.drift()
        self.meaning()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("comma")
        c = clip("comma.thirds")
        ev = d["events"]
        card = listen_card(r"Four minor thirds up from C, \ and then the last note together with the C an octave up. \ "
                           r"Twice: \ once with pure thirds, \ once with the piano's. \ Which time do the two notes agree?", width=10.4)
        with self.voiceover(
            "The diminished seventh is four minor thirds stacked up, and on the piano four minor thirds make exactly "
            "an octave. Does the ear agree? Here are four minor thirds climbing from C, and then the top note sounding "
            "with the C an octave above the start. Twice: first with pure minor thirds, then with the piano's equal "
            "ones. Which time do the two notes agree, the first or the second?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        self.play(FadeOut(card))
        bars = self.ladder_rows()
        self.play(FadeIn(bars.frame), FadeIn(bars.heads))
        with self.listen(c) as snd:
            window(snd, r"pure, \ then equal", kind="synthesized", detail=r"organ tones", corner=DL, tag_corner=DR)
            flash(snd, list(bars.pure), [ev[f"n{k}"] for k in range(1, 5)], hot=WHITE, base=TUNE)
            pulse(snd, bars.gap, ev["both"], ev["equal"] - 0.3, buff=0.1)
            flash(snd, list(bars.equal), [ev["equal"] + 0.8 * k for k in range(1, 5)], hot=WHITE, base=GREY_B)
            pulse(snd, bars.heads[0], 0.0, ev["equal"] - 0.2, buff=0.08)
            pulse(snd, bars.heads[1], ev["equal"], c.duration, buff=0.08)
        with self.voiceover(
            f"The second. With pure thirds, each of ratio six to five, four of them overshoot the octave by "
            f"{say(round(d['four minor thirds']))} cents, more than half a semitone, and the two notes grind against "
            f"each other about {say(round(d['beat_hz']))} times a second. With the piano's thirds, each a quarter of an "
            "octave, the top note lands exactly on C."
        ):
            self.play(FadeIn(bars.gap), FadeIn(bars.gap_label))
        self.wait(0.4)
        self.clear_scene()

    def ladder_rows(self):
        d = load("comma")
        x0, scale = -5.6, 11.0 / 1300.0
        cents_pure = 1200 * np.log2(6 / 5)
        g = VGroup()
        frame = VGroup()
        for c_ in (0, 300, 600, 900, 1200):
            ln = DashedLine([x0 + c_ * scale, 1.9, 0], [x0 + c_ * scale, -1.9, 0], color=DIM, stroke_width=1.5)
            t = label(rf"{c_}", font_size=18, color=GREY_B).next_to(ln, DOWN, buff=0.1)
            frame.add(ln, t)
        frame.add(label(r"cents above C", font_size=20, color=GREY_B).move_to([0, -2.55, 0]))
        heads = VGroup(label(r"pure minor thirds \ (6:5, \ 315.6 cents)", font_size=22, color=TUNE).move_to([x0 + 2.4, 1.55, 0]),
                       label(r"equal minor thirds \ (300 cents)", font_size=22, color=GREY_A).move_to([x0 + 2.0, -0.45, 0]))
        pure = VGroup(*[Rectangle(width=cents_pure * scale - 0.05, height=0.5, stroke_width=0, fill_color=TUNE, fill_opacity=0.8).move_to([x0 + (k + 0.5) * cents_pure * scale, 0.9, 0]) for k in range(4)])
        equal = VGroup(*[Rectangle(width=300 * scale - 0.05, height=0.5, stroke_width=0, fill_color=GREY_B, fill_opacity=0.8).move_to([x0 + (k + 0.5) * 300 * scale, -1.1, 0]) for k in range(4)])
        over = d["four minor thirds"]
        gap = Rectangle(width=over * scale, height=0.7, stroke_color=EAR, stroke_width=3, fill_opacity=0).move_to([x0 + (1200 + over / 2) * scale, 0.9, 0])
        gap_label = label(rf"+{over:.1f} cents", font_size=22, color=EAR).next_to(gap, UP, buff=0.15)
        g.add(frame, heads, pure, equal, gap)
        g.frame, g.heads, g.pure, g.equal, g.gap, g.gap_label = frame, heads, pure, equal, gap, gap_label
        self.add(pure, equal)
        return g

    # ------------------------------------------------------------------
    def ladder(self):
        d = load("comma")
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (rf"four pure minor thirds: \ {1200 + d['four minor thirds']:.1f} cents, \ an octave and {d['four minor thirds']:.1f} cents", WHITE),
            (rf"three pure major thirds: \ {1200 + d['three major thirds']:.1f} cents, \ an octave less {-d['three major thirds']:.1f} cents \ (the diesis)", WHITE),
            (r"Part 6: \ stacks of pure intervals never close the circle", GREY_A),
            (r"the diminished seventh's symmetry exists only in equal temperament", TUNE),
            (r"so does every trapdoor that depends on F$\sharp$ = G$\flat$", TUNE))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"symmetry costs a comma", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            f"So in pure tuning the stack does not close. <bookmark mark='a'/> Four pure minor thirds come to an "
            f"octave and {say(round(d['four minor thirds']))} cents. <bookmark mark='b'/> Three pure major thirds, "
            f"the augmented triad, fall {say(round(-d['three major thirds']))} cents short, a gap called the diesis. "
            "<bookmark mark='c'/> This is Part 6's lesson again: stacks of pure intervals never quite close the circle. "
            "<bookmark mark='d'/> The diminished seventh's perfect symmetry, four equal steps round the octave, exists "
            "only in equal temperament. <bookmark mark='e'/> And so does every trapdoor that depends on F sharp being "
            "the same note as G flat."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def drift(self):
        d = load("comma")
        per = -d["three major thirds"]
        laps = [per * k for k in range(1, 6)]
        ch = columns(laps, [rf"{k}" for k in range(1, 6)], width=5.6, height=2.6, color=WEAK, hot=(4,), hot_color=EAR, fmt="{:.0f}", font_size=22).move_to(LEFT * 3.2 + DOWN * 0.5)
        t = label(r"cents flat after each lap of C, \ E, \ A$\flat$ = G$\sharp$, \ C", font_size=22, color=GREY_A).next_to(ch, UP, buff=0.35)
        x = label(r"laps", font_size=20, color=GREY_B).next_to(ch, DOWN, buff=0.15)
        rows_ = VGroup(*[label(t_, font_size=24, color=c_) for t_, c_ in (
            (r"a choir tunes each chord pure", WHITE),
            (r"C major to E major to A$\flat$ major and home: \ three pure major thirds", WHITE),
            (rf"back on `C', \ {per:.1f} cents lower than it began", EAR),
            (rf"five laps: \ {laps[-1]:.0f} cents, \ about a whole tone flat", TUNE))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 6.4))
        rows_.move_to(RIGHT * 3.5 + DOWN * 0.1)
        with self.voiceover(
            "Here is what that means for singers. <bookmark mark='a'/> A choir without a piano tunes each chord pure, "
            "each major third in the ratio five to four. <bookmark mark='b'/> Let it sing chapter eight's cycle of "
            "chromatic mediants, C major, E major, A flat major, and home, each chord holding one note of the last. "
            f"<bookmark mark='c'/> Three pure major thirds; and the C it comes home to is {say(round(per))} cents lower "
            f"than the C it started on. <bookmark mark='d'/> Five laps, and the choir has sunk {say(round(laps[-1]))} "
            "cents, about a whole tone, with every chord in tune. This is Part 6's comma pump, driven by chromatic "
            "harmony; real choirs compromise, tempering by ear."
        ) as vo:
            self.play(FadeIn(t), FadeIn(ch), FadeIn(x))
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def meaning(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"before about 1700: \ meantone keyboards, \ with G$\sharp$ and A$\flat$ different notes", WHITE),
            (r"some had split black keys, \ to play both", WHITE),
            (r"well temperaments, \ then equal temperament: \ the enharmonic door opens", WHITE),
            (r"choirs and string quartets still tune by ear, \ and drift: \ the comma comes back", GREY_A),
            (r"chromatic harmony is an idea that needs a tuning", TUNE))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"a harmony built on a tuning", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "This had consequences. <bookmark mark='a'/> On the meantone keyboards of the sixteenth and seventeenth "
            "centuries, G sharp and A flat were different notes, and only one of them could be played. "
            "<bookmark mark='b'/> Some instruments had split black keys, front for one, back for the other. "
            "<bookmark mark='c'/> The well temperaments of Bach's time, and then equal temperament, made them one key, "
            "and the enharmonic door opened. <bookmark mark='d'/> Singers and string players still tune by ear, and a "
            "choir that tunes each chord pure through a chain of enharmonic changes drifts in pitch: the comma comes "
            "back. <bookmark mark='e'/> Chromatic harmony is an idea that needs a tuning to make it possible."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
