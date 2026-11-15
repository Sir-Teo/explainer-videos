from __future__ import annotations

from math import log2

import numpy as np

from videos.music.music33.common import *  # noqa: F403


def fifth_circle(n, radius=1.25, color=TUNE):
    g = VGroup(Circle(radius=radius, color=DIM, stroke_width=1.5))
    pts = sorted(((k * log2(1.5)) % 1.0, k) for k in range(n))
    for x, k in pts:
        ang = PI / 2 - x * TAU
        g.add(Dot(radius * np.array([np.cos(ang), np.sin(ang), 0]), radius=0.08, color=color if k else WHITE))
    xs = np.array([p[0] for p in pts])
    gaps = np.diff(np.concatenate([xs, [xs[0] + 1]])) * 1200
    g.sizes = sorted({round(float(x), 1) for x in gaps})
    return g


class Mos(SoundScene):
    def construct(self):
        chapter(self, 3, r"Stacks of fifths", r"Why five, \ seven and twelve notes?", extra=((1975, r"Wilson's moments of symmetry"),))
        self.stacks()
        self.three_gaps()
        self.fractions()
        self.hear()
        self.golden()

    # ------------------------------------------------------------------
    def stacks(self):
        cells = VGroup()
        for n in range(2, 13):
            g = fifth_circle(n, radius=0.62)
            two = len(g.sizes) == 2
            for m in g[1:]:
                m.set_color(TUNE if two else GREY_B)
            cap = label(rf"{n}: \ {len(g.sizes)} sizes", font_size=16, color=TUNE if two else GREY_A).next_to(g, DOWN, buff=0.15)
            cells.add(VGroup(g, cap))
        cells.arrange_in_grid(rows=2, buff=(0.45, 0.45)).move_to(DOWN * 0.2)
        head = label(r"stack fifths from C and fold them into one octave: \ how many sizes of step?", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Start at C and stack pure fifths, folding each new note back into one octave, as Part 12 did. After each new note, "
            "look at the gaps round the circle. <bookmark mark='a'/> With two, three, five, seven and twelve notes there are "
            "exactly two sizes of step; these are the gold circles. With four, six, eight or more notes up to eleven, there "
            "are three. The sizes that give two steps are the ones music uses: the pentatonic, the diatonic and the chromatic "
            "scale. Erv Wilson called them moments of symmetry."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells[:3]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells[3:]], lag_ratio=0.2), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def three_gaps(self):
        items = [
            (r"the three-gap theorem \ (Steinhaus's conjecture; \ S\'os, \ \'Swierczkowski, \ about 1958)", WHITE),
            (r"n points of a stack of any generator on a circle leave at most three different gaps", WHITE),
            (r"and when there are three, \ the largest is the sum of the other two", WHITE),
            (r"so a scale built by stacking always has two or three step sizes: \ never a jumble", TUNE),
            (r"the sizes with only two are the well-formed scales: \ Carey and Clampitt \ (1989)", GREY_A),
        ]
        rows_scene(self, r"never more than three", items,
                   "There is a theorem behind the picture. <bookmark mark='b'/> The three-gap theorem, conjectured by Steinhaus "
                   "and proved around 1958: <bookmark mark='c'/> stack any step round a circle and the points leave at most three "
                   "different gaps, <bookmark mark='d'/> and when there are three, the largest is the sum of the other two. "
                   "<bookmark mark='e'/> So a scale built by stacking is never a jumble of step sizes. <bookmark mark='f'/> The "
                   "sizes with just two steps are what Norman Carey and David Clampitt called well-formed scales.", marks="cdef")

    # ------------------------------------------------------------------
    def fractions(self):
        d = load("mos")
        conv = [(a, b) for a, b in d["convergents"] if b > 1][:6]
        cells = VGroup(*[VGroup(label(rf"$\tfrac{{{a}}}{{{b}}}$", font_size=34, color=TUNE if b in (2, 5, 12, 41, 53) else WHITE),
                                label(rf"{b} notes", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.2) for a, b in conv]).arrange(RIGHT, buff=0.9).move_to(UP * 0.6)
        sizes = label(r"moments of symmetry up to 60: \ " + r", \ ".join(str(x) for x in d["sizes"]), font_size=22, color=WHITE).next_to(cells, DOWN, buff=0.7)
        cap = label(rf"the fifth is {d['fifth_log']:.5f} of an octave: \ its continued fraction's convergents give 12 \ ($\tfrac{{7}}{{12}}$), \ 41 and 53", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.7)
        head = label(r"continued fractions of the fifth", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Which sizes, and why? A pure fifth is {say(d['fifth_log'], 4)} of an octave, an irrational number. "
            "<bookmark mark='a'/> Its continued fraction gives the best approximations by fractions: one half, three fifths, "
            "seven twelfths, twenty-four forty-firsts, thirty-one fifty-thirds. <bookmark mark='b'/> The denominators, "
            "together with sums of neighbouring ones, are exactly the sizes with two step sizes: two, three, five, seven, "
            "twelve, seventeen, twenty-nine, forty-one, fifty-three. Twelve notes work because seven twelfths of an octave is "
            "very close to a fifth; fifty-three, studied in China and by Mercator, is closer still."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells[:3]))
            vo.wait_until("a")
            self.play(FadeIn(cells[3:]), FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(sizes))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("mos")
        c = clip("mos.three")
        cells = VGroup()
        for n, nm in (("5", r"C D E G A"), ("7", r"C D E F$\sharp$ G A B"), ("12", r"all twelve")):
            g = fifth_circle(int(n), radius=1.1)
            st = d["steps"][n]
            cells.add(VGroup(g, label(rf"{n} fifths: \ {nm}", font_size=19, color=TUNE), label(rf"steps {st[0]:.0f} and {st[1]:.0f} cents", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.25))
        cells.arrange(RIGHT, buff=1.0).move_to(DOWN * 0.1)
        head = label(r"three moments of symmetry, \ heard as scales from C", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Hear three of them. Five fifths from C make the pentatonic scale, with steps of about two hundred and three "
            "hundred cents. Seven make a scale with an F sharp, the Lydian mode, with whole tones and semitones. Twelve make "
            "every key on the piano, with two sizes of semitone that equal temperament then makes equal."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"5, \ 7, \ 12 fifths", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            ks = ["5", "7", "12"]
            for i, k in enumerate(ks):
                end = d["starts"][ks[i + 1]] - 0.5 if i < 2 else c.duration
                pulse(snd, cells[i], d["starts"][k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def golden(self):
        d = load("golden")
        rows_ = text_rows([
            (r"stack the golden ratio's fraction of a circle, \ 0.618..., \ instead of the fifth", WHITE),
            (r"two step sizes at: \ " + r", \ ".join(str(x) for x in d["sizes"]), TUNE),
            (r"the Fibonacci numbers: \ the golden ratio's continued fraction is all ones", WHITE),
            (r"its convergents are ratios of Fibonacci numbers: \ 1/2, \ 2/3, \ 3/5, \ 5/8 ...", WHITE),
            (r"chapter 6 meets the same numbers in Sanskrit metre", GREY_A),
        ], font_size=24)
        head = label(r"another generator: \ the golden ratio", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Try another generator. <bookmark mark='a'/> Stack the golden ratio's fraction of a circle, nought point six one "
            "eight, instead of the fifth. <bookmark mark='b'/> Two step sizes appear at two, three, five, eight, thirteen, "
            "twenty-one, thirty-four and fifty-five points. <bookmark mark='c'/> These are the Fibonacci numbers, because the "
            "golden ratio's continued fraction is the simplest of all, every term a one. <bookmark mark='d'/> Its best "
            "approximations are ratios of neighbouring Fibonacci numbers. <bookmark mark='e'/> Chapter six meets the same "
            "numbers in Sanskrit poetry."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
