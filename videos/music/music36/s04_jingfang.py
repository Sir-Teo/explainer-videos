from __future__ import annotations

import numpy as np

from videos.music.music36.common import *  # noqa: F403


class JingFang(SoundScene):
    def construct(self):
        chapter(self, 3, r"Jing Fang's sixty", r"How many fifths before you come home?")
        self.chart()
        self.hear()
        self.later()
        self.equal()
        self.fifty3()
        self.zhumethod()

    # ------------------------------------------------------------------
    def chart(self):
        d = load("jingfang")
        gaps = d["gaps"]
        ax = Axes(x_range=[0, 60, 10], y_range=[-60, 60, 20], x_length=10.4, y_length=3.6, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 15}).move_to(DOWN * 0.3)
        dots = VGroup(*[Dot(ax.c2p(i + 1, g), radius=0.05 if abs(g) > 25 else 0.09, color=TUNE if abs(g) < 25 else GREY_B) for i, g in enumerate(gaps)])
        tags = VGroup(*[label(rf"{b['n']}: \ {b['gap']:+.1f}", font_size=16, color=TUNE).next_to(ax.c2p(b["n"], b["gap"]), UP, buff=0.12) for b in d["best"][:3]])
        xl = label(r"number of pure fifths", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.3)
        yl = label(r"cents from a whole number of octaves", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.15)
        head = label(r"how close does a chain of fifths come to closing?", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "In the first century BCE the scholar Jing Fang carried the chain of fifths far beyond twelve, to sixty pitches. "
            "<bookmark mark='a'/> The program repeats his computation: for each number of pure fifths, how far from a whole "
            "number of octaves does it land? <bookmark mark='b'/> Twelve fifths miss by twenty-three and a half cents. "
            "Forty-one miss by under twenty. And fifty-three fifths come within three and a half cents of thirty-one octaves, "
            "nearly closed. Jing Fang noticed it: his fifty-fourth pitch fell almost exactly on his first."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.03), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(tags))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("jingfang")
        c = clip("jingfang.two")
        cells = VGroup(VGroup(label(r"12 fifths", font_size=28, color=GREY_A), label(rf"23.5 cents off: \ beats {d['beat12']:.1f} times a second", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.2),
                       VGroup(label(r"53 fifths", font_size=28, color=TUNE), label(rf"3.6 cents off: \ beats {d['beat53']:.2f} times a second", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.2)).arrange(RIGHT, buff=2.0).move_to(UP * 0.3)
        head = label(r"hear the gap", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Hear the difference. Middle C sounded with the note twelve pure fifths away, brought back into the same octave: "
            "the two beat about three and a half times a second. Then with the note fifty-three fifths away: it beats about "
            "once every two seconds, so nearly in tune that only patience hears the drift."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"12 fifths, \ then 53", kind="synthesized", detail=r"additive tones", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], d["starts"]["12"], d["starts"]["53"] - 0.5, buff=0.1)
            pulse(snd, cells[1], d["starts"]["53"], c.duration, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def later(self):
        items = [
            (r"Qian Lezhi \ (5th century) \ extended the chain to 360 pitches", WHITE),
            (r"He Chengtian \ (5th century) \ spread the comma over twelve steps: \ an approach to equal temperament", WHITE),
            (r"Zhu Zaiyu \ (1584): \ twelve-tone equal temperament computed to many digits", TUNE),
            (r"published about the same time as Simon Stevin's in Europe", WHITE),
            (r"Part 33's continued fractions explain why 12, \ 41 and 53 keep appearing", GREY_A),
        ]
        rows_scene(self, r"after Jing Fang", items,
                   "The search went on for centuries. <bookmark mark='b'/> In the fifth century Qian Lezhi extended the chain to "
                   "three hundred and sixty pitches, <bookmark mark='c'/> and He Chengtian spread the comma over twelve steps, an "
                   "approach towards equal temperament. <bookmark mark='d'/> In 1584 the prince Zhu Zaiyu computed twelve-tone "
                   "equal temperament exactly, to many digits, <bookmark mark='e'/> at about the same time as Simon Stevin in "
                   "Europe. <bookmark mark='f'/> Part 33's continued fractions explain why twelve, forty-one and fifty-three keep "
                   "appearing.", marks="cdef")

    # ------------------------------------------------------------------
    def equal(self):
        d = load("zhu")
        c = clip("zhu.two")
        cells = VGroup(label(r"Pythagorean: \ third 408 cents", font_size=24, color=TUNE), label(r"equal: \ third 400 cents", font_size=24, color=BLUE)).arrange(RIGHT, buff=0.8)
        cells.scale_to_fit_width(min(cells.width, 12.4)).move_to(UP * 0.3)
        head = label(r"Pythagorean against equal temperament", font_size=27, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Hear what Zhu Zaiyu's equal temperament changes. The pentatonic up and down, then C with its third, first in Pythagorean tuning, with a third of four hundred and eight cents, then in equal temperament, with four hundred. The melody hardly changes; the third, sounded together, beats a little less."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"Pythagorean, \ then equal", detail=r"plucked string and additive tones", corner=DL, tag_corner=DR)
            ks = ['pyth', 'et']
            for i, k in enumerate(ks):
                end = d["starts"][ks[i + 1]] - 0.4 if i < len(ks) - 1 else c.duration
                pulse(snd, cells[i], d["starts"][k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def zhumethod(self):
        items = [
            (r"equal temperament needs the twelfth root of two: \ 1.059463...", WHITE),
            (r"Zhu Zaiyu took square roots and a cube root on a large abacus", WHITE),
            (r"his values are correct to about 25 digits", WHITE),
            (r"he also built instruments and wrote out dances to match", TUNE),
            (r"his theory was admired, \ and largely ignored in court practice", GREY_A),
        ]
        rows_scene(self, r"how Zhu Zaiyu computed it", items,
                   "How did Zhu Zaiyu do it? <bookmark mark='b'/> Equal temperament needs the twelfth root of two, about one point oh five nine four six. <bookmark mark='c'/> He took square roots and a cube root by hand, reportedly on a very large abacus, <bookmark mark='d'/> and his values are correct to about twenty-five digits. <bookmark mark='e'/> He also built instruments and wrote out dances to go with his theory. <bookmark mark='f'/> His work was admired, and largely ignored in the court's actual practice, which kept its older tunings.", marks="cdef")

    # ------------------------------------------------------------------
    def fifty3(self):
        items = [
            (r"53 appears again in Mercator's 17th-century work and in Turkish theory \ (Part 35)", WHITE),
            (r"41 and 53 are denominators of the fifth's continued fraction \ (Part 33)", WHITE),
            (r"three cultures, \ the same arithmetic: \ the fifth's irrationality forces it", WHITE),
            (r"what differs is what each made of it: \ ritual, \ a keyboard, \ a theory of commas", TUNE),
            (r"mathematics is shared; \ music is not", GREY_A),
        ]
        rows_scene(self, r"fifty-three elsewhere", items,
                   "Fifty-three keeps returning. <bookmark mark='b'/> It appears again in Nicholas Mercator's work in seventeenth-century England and in the Turkish theory of Part 35. <bookmark mark='c'/> Forty-one and fifty-three are denominators of the fifth's continued fraction, as Part 33 showed, <bookmark mark='d'/> so three cultures meeting the same arithmetic is no coincidence: the fifth's irrationality forces it. <bookmark mark='e'/> What differs is what each made of it: a ritual cosmology, a keyboard, a theory of commas. <bookmark mark='f'/> The mathematics is shared; the music is not.", marks="cdef")
