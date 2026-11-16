from __future__ import annotations

import numpy as np

from videos.music.music21.common import *  # noqa: F403


class Golden(SoundScene):
    def construct(self):
        chapter(self, 10, r"The golden section, \ tested", r"Do composers divide their pieces at 0.618?", extra=((1995, r"Putz on Mozart's sonatas"),))
        self.claims()
        self.base_rate()
        self.climaxes()

    # ------------------------------------------------------------------
    def claims(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"the golden section: \ divide a whole so that whole : larger = larger : smaller", WHITE),
            (r"the larger part: \ 0.618 of the whole", TUNE),
            (r"claimed for Bartók \ (Lendvai), \ Debussy \ (Howat), \ Mozart \ (Putz, \ 1995)", WHITE),
            (r"Mozart: \ exposition against development and recapitulation, \ near 0.618", WHITE),
            (r"the question is not whether some ratios are near 0.618: \ it is how often they would be by chance", EAR))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"a famous proportion", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A claim about form appears in many books. <bookmark mark='a'/> The golden section divides a whole so that "
            "the whole is to the larger part as the larger is to the smaller, <bookmark mark='b'/> which puts the "
            "division at 0.618 of the way through. <bookmark mark='c'/> It has been found in Bartók by Ernő Lendvai, in "
            "Debussy by Roy Howat, and in Mozart by John Putz, who in 1995 measured Mozart's piano sonatas. "
            "<bookmark mark='d'/> In many sonata movements, he found, the development and recapitulation together take "
            "up close to 0.618 of the whole. <bookmark mark='e'/> The question a statistician asks is not whether some "
            "ratios lie near 0.618. It is how often they would by chance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def base_rate(self):
        d = load("golden")
        s = load("sonata")
        W = 9.0
        axis = Line(LEFT * W / 2, RIGHT * W / 2, color=GREY_B, stroke_width=2).move_to(UP * 0.6)

        def x(v):
            return axis.get_left()[0] + W * v

        ticks = VGroup(*[VGroup(Line([x(v), axis.get_y() - 0.1, 0], [x(v), axis.get_y() + 0.1, 0], color=GREY_B), label(rf"{v:.2f}".rstrip("0").rstrip("."), font_size=18, color=GREY_B).move_to([x(v), axis.get_y() - 0.35, 0])) for v in (0, 0.25, 0.5, 0.75, 1.0)])
        plaus = Rectangle(width=W * 0.25, height=0.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.3).move_to([x(0.625), axis.get_y(), 0])
        gold = Rectangle(width=W * 0.04, height=0.7, stroke_width=0, fill_color=TUNE, fill_opacity=0.85).move_to([x(d["phi"]), axis.get_y(), 0])
        ours = Triangle(color=EAR, fill_opacity=1.0).scale(0.15).rotate(PI).move_to([x(s["golden"]["rest"]), axis.get_y() + 0.55, 0])
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"illustrative null: \ uniform larger-part ratio from 0.5 to 0.75", BLUE),
            (r"0.618, \ give or take 0.02: \ a band 0.04 wide", TUNE),
            (rf"under this null: \ {100 * d['base_rate']:.0f} hits in a hundred", WHITE),
            (rf"this part's sonata, \ illustrative section ratio: \ {s['golden']['rest']:.3f}", EAR))]).arrange(DOWN, buff=0.33, aligned_edge=LEFT).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            f"Here is the chance. <bookmark mark='a'/> In a piece with two parts, the larger part is almost never less than half the whole, and rarely more than three quarters: for this illustrative null, assume it is uniformly distributed over that range. <bookmark mark='b'/> Call it a hit if it lies within two hundredths of 0.618, a band four hundredths wide. <bookmark mark='c'/> Then chance alone gives a hit {say(round(100 * d['base_rate']))} times in a hundred, about one piece in six; a simulation of two hundred thousand random divisions agrees. Under this assumed uniform null, the chance of at least one hit increases with the number examined. <bookmark mark='d'/> And this part's own miniature sonata, whose displayed section lengths give an illustrative near match: its development and recapitulation take {say(s['golden']['rest'], 3)} of the whole. A hit."
        ) as vo:
            self.play(Create(axis), FadeIn(ticks), FadeIn(plaus), FadeIn(rows_[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(gold), FadeIn(rows_[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows_[2]))
            vo.wait_until("d")
            self.play(FadeIn(ours), FadeIn(rows_[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def climaxes(self):
        d = load("golden")
        pos = d["positions"]
        bins = [sum(1 for p in pos if lo <= p < hi) for lo, hi in ((0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.01))]
        ch = columns(bins, [r"0--0.2", r"0.2--0.4", r"0.4--0.6", r"0.6--0.8", r"0.8--1"], width=6.6, height=2.6, color=WEAK, hot=(), hot_color=TUNE, fmt="{:.0f}", font_size=20).move_to(LEFT * 2.6 + DOWN * 0.5)
        t = label(r"where each tune's highest note first arrives, \ as a share of its length", font_size=21, color=GREY_A).next_to(ch, UP, buff=0.4)
        side = VGroup(label(rf"{d['in_first_half']} of {d['n']} climaxes in the first half", font_size=24, color=WHITE),
                      label(rf"within 0.02 of 0.618: \ {d['hits']} \ (uniform reference: \ about {d['expected_uniform']:.0f})", font_size=24, color=TUNE),
                      label(r"this comparison does not show intentional design", font_size=24, color=EAR)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 4.0 + DOWN * 0.2)
        with self.voiceover(
            f"The tunes can be tested too. Mark where each tune's highest note first arrives. <bookmark mark='a'/> {say(d['in_first_half'])} of the {say(d['n'])} climaxes come in the first half, as Part 14 found: these tunes leap up early and spend the rest coming down. <bookmark mark='b'/> Just {say(d['hits'])} fall within two hundredths of 0.618, about the {say(round(d['expected_uniform']))} that chance would put there. <bookmark mark='c'/> Proportion matters in music, but this small illustration does not establish intentional golden-section design or refute every published claim; conclusions depend on the null model, chosen landmarks and multiple comparisons."
        ) as vo:
            self.play(FadeIn(ch), FadeIn(t))
            for mark, r in zip("abc", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
