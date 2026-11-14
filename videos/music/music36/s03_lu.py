from __future__ import annotations

import numpy as np

from videos.music.music36.common import *  # noqa: F403


class Lu(SoundScene):
    def construct(self):
        chapter(self, 2, r"Twelve pitches from a pipe", r"How do you generate a scale by cutting?")
        self.rule()
        self.hear()
        self.twelve()
        self.chromatic()
        self.months()
        self.huangzhong()

    # ------------------------------------------------------------------
    def rule(self):
        d = load("lu")
        rows_ = VGroup()
        for x in d["lu"][:7]:
            rows_.add(VGroup(label(rf"step {x['k']}", font_size=18, color=GREY_A), label(rf"length {x['length']}", font_size=20, color=WHITE),
                             label(rf"{x['cents']:.0f} cents", font_size=20, color=TUNE)).arrange(RIGHT, buff=0.6))
        rows_.arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(LEFT * 1.5 + DOWN * 0.3)
        side = VGroup(*[label(s, font_size=20, color=c_) for s, c_ in (
            (r"\textit{sanfen sunyi}: \ take away a third, \ add a third", WHITE),
            (r"$\times\tfrac23$: \ a fifth up; \ $\times\tfrac43$: \ a fourth down", TUNE),
            (r"the same chain of fifths as Pythagoras \ (Part 6)", GREY_A))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.move_to(RIGHT * 4.2)
        head = label(r"the rule of three: \ a pipe of length 81", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Chinese theory generated its pitches by a rule for cutting pipes or strings, recorded by the third century BCE. "
            "<bookmark mark='a'/> Start with a length of eighty-one. Take away a third: fifty-four, a fifth higher. Add a "
            "third: seventy-two, a fourth lower. Take away a third, add a third, alternately. <bookmark mark='b'/> Each step "
            "multiplies by two thirds or four thirds, up a fifth or down a fourth, <bookmark mark='c'/> the same chain of "
            "fifths Part 6 built for Pythagoras, found independently. Eighty-one was chosen because it can be divided by "
            "three four times."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_))
            for mark, r in zip("abc", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("lu")
        c = clip("lu.five")
        names = ["gong", "shang", "jue", "zhi", "yu", "gong"]
        cells = VGroup(*[VGroup(label(n, font_size=24, color=TUNE), label(rf"{cc:.0f}", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.15)
                         for n, cc in zip(names, d["first5"] + [1200.0])]).arrange(RIGHT, buff=0.8).move_to(UP * 0.3)
        head = label(r"the first five, \ folded into one octave", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"the pentatonic scale, \ C D E G A: \ the core of Chinese melody", font_size=22, color=GREY_A).to_edge(DOWN, buff=1.1)
        with self.voiceover(
            "Fold the first five pitches into one octave and they are the pentatonic scale, the notes named gong, shang, jue, "
            "zhi and yu: in Western letters C, D, E, G and A, with Pythagorean thirds. Listen."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"gong, \ shang, \ jue, \ zhi, \ yu", detail=r"a plucked-string model", corner=DL, tag_corner=DR)
            for i in range(6):
                pulse(snd, cells[i], i * d["unit"], (i + 1) * d["unit"] - 0.03, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def twelve(self):
        d = load("lu")
        L = 11.0
        line = Line(LEFT * L / 2, RIGHT * L / 2, color=GREY_B).move_to(UP * 0.4)
        ticks = VGroup(*[Line([-L / 2 + L * c / 1200, 0.15, 0], [-L / 2 + L * c / 1200, 0.65, 0], color=TUNE if i < 5 else BLUE, stroke_width=4) for i, c in enumerate(sorted(d["twelve"], key=lambda c: c))])
        et = VGroup(*[Line([-L / 2 + L * k / 12, -0.05, 0], [-L / 2 + L * k / 12, 0.2, 0], color=GREY_B, stroke_width=1) for k in range(13)])
        rows_ = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"twelve steps give the twelve \textit{l\"u}: \ a chromatic scale of Pythagorean semitones", WHITE),
            (rf"but the twelfth step misses the octave by {d['comma']:.1f} cents: \ the Pythagorean comma", EAR),
            (r"the circle does not close: \ the same problem every tuning system meets \ (Part 6)", GREY_A))]).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.6)
        head = label(r"twelve steps: \ the twelve l\"u", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Keep going. <bookmark mark='a'/> Twelve steps give the twelve lü, a chromatic scale of two sizes of semitone. "
            "<bookmark mark='b'/> But the thirteenth pitch misses the starting note's octave by twenty-three and a half cents, "
            "the Pythagorean comma. <bookmark mark='c'/> The circle does not close, the same problem every tuning system "
            "meets. Chinese theorists spent two thousand years on it."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(ticks), FadeIn(et))
            for mark, r in zip("abc", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chromatic(self):
        d = load("twelve")
        c = clip("twelve.chromatic")
        cells = VGroup(label(r"semitones of 90 and 114 cents, \ alternating unevenly", font_size=24, color=TUNE)).arrange(RIGHT, buff=0.8)
        cells.scale_to_fit_width(min(cells.width, 12.4)).move_to(UP * 0.3)
        head = label(r"the twelve l\"u, \ in order", font_size=27, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            'Here are all twelve lü in rising order. The semitones are not equal: some are ninety cents and some one hundred and fourteen, the limma and the apotome of Pythagorean tuning. Listen for the slight unevenness as the scale climbs.'
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"the twelve l\"u", detail=r"a plucked-string model", corner=DL, tag_corner=DR)
            ts = [0.0]
            for i, t0 in enumerate(ts):
                end = ts[i + 1] - 0.05 if i + 1 < len(ts) else c.duration
                pulse(snd, cells[i % len(cells)], t0, end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def huangzhong(self):
        items = [
            (r"the first pitch, \ \textit{huangzhong}, \ the `yellow bell', \ was the reference for the whole system", WHITE),
            (r"its pitch pipe's length also served as a standard of measure: \ length, \ volume, \ weight", WHITE),
            (r"new dynasties often reset it: \ fixing the pitch was a political act", WHITE),
            (r"music, \ measure and cosmic order were tied together in court ritual", TUNE),
            (r"Part 6's concert pitch, \ with an empire behind it", GREY_A),
        ]
        rows_scene(self, r"the yellow bell", items,
                   "The first pitch had a name and a role. <bookmark mark='b'/> It was called huangzhong, the yellow bell, and it was the reference for the whole system. <bookmark mark='c'/> Its pitch pipe's length also served as a standard of measure, for length, volume and weight. <bookmark mark='d'/> New dynasties often reset it, so that fixing the pitch was a political act, a sign that the new ruler had brought the world back into order. <bookmark mark='e'/> Music, measure and cosmic order were tied together in court ritual. <bookmark mark='f'/> It is Part 6's concert pitch, with an empire behind it.", marks="cdef")

    # ------------------------------------------------------------------
    def months(self):
        items = [
            (r"the twelve l\"u were matched to the twelve months of the year", WHITE),
            (r"each month had its pitch, \ used in its rituals", WHITE),
            (r"some texts describe pitch pipes buried to detect the seasons' qi", WHITE),
            (r"music as part of a correlative cosmology: \ notes, \ seasons, \ colours, \ directions", TUNE),
            (r"Part 23's medieval Europe also tied music to the cosmos: \ \textit{musica mundana}", GREY_A),
        ]
        rows_scene(self, r"pitches and the calendar", items,
                   "The pitches belonged to a larger order. <bookmark mark='b'/> The twelve lü were matched to the twelve months of the year, <bookmark mark='c'/> each month with its pitch, sounded in its rituals. <bookmark mark='d'/> Some old texts describe pitch pipes buried in the ground to detect the arrival of each season. <bookmark mark='e'/> Music was part of a correlative cosmology in which notes, seasons, colours and directions answered one another. <bookmark mark='f'/> Part 23's medieval Europe tied music to the cosmos too, as the music of the spheres.", marks="cdef")
