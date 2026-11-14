from __future__ import annotations

import numpy as np

from videos.music.music11.common import *  # noqa: F403


class Divide(SoundScene):
    def construct(self):
        chapter(self, 4, r"Dividing the beat", r"How is a beat cut up?")
        self.cuts()
        self.clock()
        self.compound()

    # ------------------------------------------------------------------
    def cuts(self):
        c = clip("divide.four")
        cols = VGroup()
        for parts, name in ((1, r"one"), (2, r"two"), (3, r"three: \ a triplet"), (4, r"four")):
            st = sticks(parts, width=1.7, height=0.9)
            cols.add(VGroup(st, label(name, font_size=26, color=GREY_A)).arrange(DOWN, buff=0.35))
        cols.arrange(RIGHT, buff=1.1, aligned_edge=DOWN).scale(1.3).move_to(UP * 0.9)
        with self.voiceover(
            "Below the beat, the question is how to cut it. Part 10's note values cut by two: a quarter "
            "note is two eighths, or four sixteenths. <bookmark mark='a'/> To cut a beat in three, "
            "notation borrows three eighths and marks them with a small figure three: a triplet, three "
            "in the time of two. Listen to one beat cut each way, four beats at a time, over a bass drum "
            "that keeps the beat."
        ) as vo:
            self.play(FadeIn(cols[0]), FadeIn(cols[1]), FadeIn(cols[3]))
            vo.wait_until("a")
            self.play(FadeIn(cols[2]))
        with self.listen(c) as snd:
            window(snd, r"a beat cut in one, \ two, \ three, \ four", detail=r"bass drum and wood block, \ modelled", corner=DL, tag_corner=DR)
            for j, parts in enumerate((1, 2, 3, 4)):
                t0 = snd.time_of(f"d{parts}")
                pulse(snd, cols[j], t0, t0 + 2.35, buff=0.15)
                for b in range(4):
                    snd.wait_until(t0 + b * 0.6)
                    self.play(cols[j][0].animate(rate_func=there_and_back).scale(1.12), run_time=0.25)
        self.wait(0.2)
        self.cols = cols

    # ------------------------------------------------------------------
    def clock(self):
        d = load("divide")
        cols = self.cols
        ms = d["ms"]
        vals = [ms["quarter"], ms["eighth"], ms["triplet"], ms["sixteenth"]]
        nums = VGroup(*[label(rf"{v:.0f} ms", font_size=30, color=TIME).next_to(col, DOWN, buff=0.35) for v, col in zip(vals, cols)])
        head = label(rf"at {d['bpm']:.0f} beats to the minute", font_size=28, color=GREY_A).next_to(cols, UP, buff=0.5)
        with self.voiceover(
            "On a clock, those cuts get short quickly. At the Tune's tempo, a hundred and nine beats to "
            f"the minute, a beat lasts {say(ms['quarter'])} milliseconds; half of it, {say(ms['eighth'])}; "
            f"a third, {say(ms['triplet'])}; a quarter of it, {say(ms['sixteenth'])}."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.5), run_time=5.0)
        card = pause_card(r"At 120 beats to the minute, \ how long does one note of a triplet last?", width=8.4).move_to(DOWN * 2.3)
        with self.voiceover("Try one. At a hundred and twenty beats to the minute, how long does one note of a triplet last? Pause, and work it out."):
            self.play(FadeIn(card))
        self.wait(2.5)
        ans = MathTex(r"\frac{60}{120} = 0.5 \text{ s}, \qquad \frac{500 \text{ ms}}{3} \approx 167 \text{ ms}", font_size=40).move_to(DOWN * 2.3)
        with self.voiceover(
            "Sixty over a hundred and twenty is half a second for the beat, and a third of that is a "
            f"hundred and sixty-seven milliseconds. Remember the floor we found in chapter one: about a "
            "hundred milliseconds. So at a fast tempo, sixteenth notes are as quick as rhythm gets, and "
            "that is one reason fast music is written in simpler values."
        ):
            self.play(FadeOut(card), FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compound(self):
        left = VGroup(label(r"simple metres", font_size=32, color=TUNE), label(r"the beat is cut in two", font_size=26, color=GREY_A),
                      VGroup(sticks(2, width=1.4), sticks(2, width=1.4)).arrange(RIGHT, buff=0.5), MathTex(r"\tfrac24 \quad \tfrac34 \quad \tfrac44", font_size=48)).arrange(DOWN, buff=0.4).scale(1.25).move_to(LEFT * 3.4)
        right = VGroup(label(r"compound metres", font_size=32, color=TUNE), label(r"the beat is cut in three", font_size=26, color=GREY_A),
                       VGroup(sticks(3, width=1.6, tuplet=False), sticks(3, width=1.6, tuplet=False)).arrange(RIGHT, buff=0.5), MathTex(r"\tfrac68 \quad \tfrac98 \quad \tfrac{12}{8}", font_size=48)).arrange(DOWN, buff=0.4).scale(1.25).move_to(RIGHT * 3.4)
        with self.voiceover(
            "If every beat of a piece is cut in three, writing a figure three over each one is a "
            "nuisance, so the notation changes the beat instead. <bookmark mark='a'/> In simple meters, "
            "two-four, three-four, four-four, the beat is a plain note and splits in two. "
            "<bookmark mark='b'/> In compound meters, six-eight, nine-eight, twelve-eight, the beat is a "
            "dotted note and splits in three. Two beats to the bar, each of three: that is six-eight, "
            "the meter of a jig, and of a lullaby."
        ) as vo:
            self.play(FadeIn(left[0]), FadeIn(right[0]))
            vo.wait_until("a")
            self.play(FadeIn(left[1:]))
            vo.wait_until("b")
            self.play(FadeIn(right[1:]))
        self.wait(0.4)
        self.clear_scene()
