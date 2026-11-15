from __future__ import annotations

import numpy as np

from videos.music.music48.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.reveal()
        self.question()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.two")
        card = listen_card(r"The Tune, \ twice. \ One version was stored as 16-bit numbers, \ 48,000 a second. \ "
                           r"The other as single bits, \ ones and zeros, \ 3 million a second. \ Which is the one-bit version?", width=10.4)
        with self.voiceover(
            "A question for your ears. The Tune, twice. One version was stored as sixteen-bit numbers, forty-eight thousand of "
            "them a second. The other was stored as single bits, ones and zeros, three million a second. Which is the "
            "one-bit version?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=3.0, height=1.2, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=24, color=WHITE)).arrange(ORIGIN)
                         for t in (r"first", r"second")]).arrange(RIGHT, buff=1.6).move_to(UP * 0.8)
        strip = bits_strip(d["bits"][:256], width=11.0, height=0.6).move_to(DOWN * 1.4)
        cap = label(r"256 of the three million bits a second", font_size=16, color=GREY_A).next_to(strip, DOWN, buff=0.25)
        self.play(FadeOut(card), FadeIn(boxes), FadeIn(ghost(strip, 0.25)), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two versions", kind="synthesized", detail=r"Part 7's piano, \ converted", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reveal(self):
        d = load("hook")
        r = d["residue_db"]
        sig = d["signal_db"]
        x0, W = -4.0, 8.0
        def X(db):
            return x0 + W * (db + 110) / 100
        axis = VGroup(Line([x0, -1.4, 0], [x0 + W, -1.4, 0], color=GREY_B, stroke_width=1.5),
                      *[VGroup(Line([X(v), -1.48, 0], [X(v), -1.32, 0], color=GREY_B), label(f"{v}", font_size=15, color=GREY_A).move_to([X(v), -1.7, 0])) for v in (-100, -80, -60, -40, -20, 0)],
                      label(r"level, \ dB below the loudest a sample can be", font_size=16, color=GREY_A).move_to([x0 + W / 2, -2.1, 0]))
        rows_ = VGroup()
        for i, (name, v, col) in enumerate(((r"the music", sig, WHITE), (r"error of the one-bit version", r["one bit"], TUNE), (r"error of the 16-bit version", r["16 bits"], BLUE))):
            y = 1.3 - 0.8 * i
            rows_.add(VGroup(label(name, font_size=19, color=col).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT),
                             Rectangle(width=X(v) - x0, height=0.4, stroke_width=0, fill_color=col, fill_opacity=0.8).move_to([(x0 + X(v)) / 2, y, 0]),
                             label(rf"{v:.0f} dB", font_size=18, color=col).move_to([X(v) + 0.5, y, 0])))
        head = label(r"the one-bit version was the first", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The one-bit version was the first. If you could not tell, you are in good company: almost nobody can. "
            f"<bookmark mark='a'/> Measure the difference from the original instead. The music sits at {say(sig)} decibels. "
            f"<bookmark mark='b'/> The one-bit version's error is at {say(r['one bit'])}, <bookmark mark='c'/> the sixteen-bit "
            f"version's at {say(r['16 bits'])}. Both errors are so far below the music that they are hidden under it. A stream "
            "of yes-or-no answers, three million a second, carries the music as well as a CD does. This part shows why."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(ghost(rows_, 0.2)))
            for mark, rr in zip("abc", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(rr))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def question(self):
        items = [
            (r"every sound in this series is a list of numbers, \ 48,000 a second", WHITE),
            (r"how can a list of numbers hold a smooth wave, \ and everything between the samples?", WHITE),
            (r"how many numbers a second, \ and how precise must each one be?", WHITE),
            (r"what goes wrong, \ how do we hear it, \ and how is it hidden?", WHITE),
            (r"and how can one bit do the work of sixteen?", TUNE),
        ]
        rows_scene(self, r"the questions", items,
                   "Every sound in this series has been a list of numbers, forty-eight thousand a second. "
                   "<bookmark mark='b'/> How can a list of numbers hold a smooth wave, and everything between the samples? "
                   "<bookmark mark='c'/> How many numbers a second do we need, and how precise must each one be? "
                   "<bookmark mark='d'/> What goes wrong, how do we hear it, and how is it hidden? <bookmark mark='e'/> And how "
                   "can one bit do the work of sixteen?", marks="bcde")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"why 44,100 samples a second",
            r"the sampling theorem, \ proved and heard",
            r"aliasing, \ and the myth of the stair-step",
            r"quantization, \ six decibels a bit, \ and dither",
            r"noise shaping, \ and one-bit conversion",
            r"jitter, \ resampling, \ and the high-resolution debate",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. Why forty-four thousand one hundred samples a second. <bookmark mark='b'/> The sampling "
            "theorem, proved and heard. <bookmark mark='c'/> Aliasing, and the myth of the stair-step. <bookmark mark='d'/> "
            "Quantization, six decibels a bit, and dither. <bookmark mark='e'/> Noise shaping, and one-bit conversion. "
            "<bookmark mark='f'/> And jitter, resampling, and the high-resolution debate."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
