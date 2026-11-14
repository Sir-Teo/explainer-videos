from __future__ import annotations

import numpy as np

from videos.music.music12.common import *  # noqa: F403


class Gaps(SoundScene):
    def construct(self):
        chapter(self, 2, r"Three gaps", r"Why five, \ seven and twelve?", extra=((1958, r"the three-gap theorem"),))
        self.theorem()
        self.moments()

    # ------------------------------------------------------------------
    def theorem(self):
        d = load("gaps")
        card = history_card(1958, r"the three-gap theorem \ (S\'os, \ Sur\'anyi, \ \'Swierczkowski)", r"mark off equal steps round a circle, \ as many as you like: \ the gaps between the marks have at most three different lengths", width=8.6, font_size=24).to_edge(UP, buff=0.4)
        g = axes([0, 61], [0, 3.6], x_length=11.0, y_length=2.6, xlabel=r"notes in the stack of fifths", ylabel=r"sizes of step", xticks=[5, 7, 12, 17, 29, 41, 53], yticks=[1, 2, 3], font_size=22).move_to(DOWN * 1.4)
        dots = VGroup(*[Dot(g.ax.c2p(n, s), radius=0.055, color=GOOD if s == 2 else GREY_B) for n, s in zip(d["n"], d["sizes"])])
        with self.voiceover(
            "Put marks round a circle by stepping the same distance again and again, as we did with the "
            "fifth. <bookmark mark='a'/> In 1958 three mathematicians proved a conjecture of Hugo "
            "Steinhaus: however many marks you make, and whatever the step, the gaps between neighbouring "
            "marks have at most three different lengths. Never four. <bookmark mark='b'/> Here is the "
            "count for our stack, for every number of notes up to sixty. Mostly there are three sizes. "
            "Now and then there are only two."
        ) as vo:
            marks = octave_circle([(k * 0.585) % 1.0 for k in range(9)], radius=1.3, color=TUNE).move_to(DOWN * 1.2)
            lead = label(r"equal steps round a circle: \ how many sizes of gap?", font_size=32, color=GREY_A).to_edge(UP, buff=0.6)
            self.add(lead, marks.ring)
            self.play(FadeIn(marks.ring), LaggedStart(*[FadeIn(x, scale=2.0) for x in marks.dots], lag_ratio=0.5), run_time=6.0)
            vo.wait_until("a")
            self.play(FadeOut(lead), FadeIn(card))
            vo.wait_until("b")
            self.play(FadeOut(marks))
            self.play(FadeIn(g), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.03), run_time=3.0)
        self.wait(0.3)
        card2 = pause_card(r"Five notes leave two sizes of step. \ Why does adding a sixth make three?", width=8.6).to_edge(UP, buff=0.4)
        with self.voiceover("Before we look at where the twos fall, think about one case. Five notes left two sizes of step. Why did the sixth note make three? Pause for a moment."):
            self.play(FadeOut(card), FadeIn(card2))
        self.wait(2.5)
        row = step_bar([204, 204, 294, 204, 294], width=6.0, height=0.5, colors=(LONG, SHORT, BAD))
        row2 = step_bar([204, 204, 204, 90, 204, 294], width=6.0, height=0.5, colors=(LONG, SHORT, BAD))
        pair = VGroup(row, row2).arrange(DOWN, buff=0.35).to_edge(UP, buff=0.5)
        with self.voiceover(
            "The new note has to land inside one of the wide steps. It cuts that step into a whole tone "
            "and a small remainder of ninety cents. The other wide step is still whole. So for a moment "
            "there are three sizes: the old wide step, the tone, and the remainder. The seventh note "
            "cuts the last wide step the same way, and we are back to two."
        ):
            self.play(FadeOut(card2), FadeIn(pair))
        self.wait(0.4)
        self.play(FadeOut(pair))
        self.g, self.dots = g, dots

    # ------------------------------------------------------------------
    def moments(self):
        d = load("gaps")
        g, dots = self.g, self.dots
        nums = VGroup(*[label(str(n), font_size=40, color=TUNE if n in (5, 7, 12) else GREY_A) for n in d["moments"]]).arrange(RIGHT, buff=0.55).to_edge(UP, buff=0.7)
        notes = VGroup(label(r"17: \ the scale of Arabic theory, \ thirteenth century", font_size=24, color=GREY_A), label(r"53: \ Jing Fang's, \ and Part 6's best equal division", font_size=24, color=GREY_A),
                       label(r"the same numbers as Part 6's continued fraction for the fifth", font_size=24, color=EAR)).arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(nums, DOWN, buff=0.35)
        with self.voiceover(
            "Two sizes of step occur at two, three, five, seven, twelve, seventeen, twenty-nine, forty-one "
            "and fifty-three notes, and nowhere else below sixty. <bookmark mark='a'/> Five, seven and "
            "twelve are in that list because of what a fifth is; no keyboard maker chose them. "
            "<bookmark mark='b'/> And the list goes on to numbers that other musicians did choose. "
            "Seventeen notes to the octave is the scale of medieval Arabic theory. Fifty-three is the "
            "division that Jing Fang found in China two thousand years ago, and that Part 6 found again. "
            "<bookmark mark='c'/> You have met these numbers. They are the denominators that came out of "
            "Part 6's continued fraction for the size of a fifth. A scale with two sizes of step is what "
            "a good rational approximation to the fifth looks like when you play it."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.2), run_time=3.0)
            vo.wait_until("a")
            self.play(*[Indicate(nums[k], color=WHITE) for k in (2, 3, 4)])
            vo.wait_until("b")
            self.play(FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()
