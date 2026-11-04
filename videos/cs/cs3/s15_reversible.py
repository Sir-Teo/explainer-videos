from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs3.common import COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, YES


class Reversible(VoiceoverScene):
    def construct(self):
        self.card()
        self.forgetting()
        self.toffoli()
        self.future()

    def card(self):
        card = chapter_card(14, r"Gates that forget nothing", r"Does computing have to cost energy?", part=PART)
        with self.voiceover("Chapter fourteen. Gates that forget nothing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def forgetting(self):
        head = label(r"An AND gate forgets", font_size=38).to_edge(UP, buff=0.35)
        ins = VGroup(*[MathTex(s, font_size=36, color=DATA) for s in ("00", "01", "10", "11")]).arrange(
            DOWN, buff=0.45).move_to(LEFT * 3.0 + DOWN * 0.2)
        outs = VGroup(MathTex("0", font_size=40, color=GREY_B), MathTex("1", font_size=40, color=YES)).arrange(
            DOWN, buff=1.4).move_to(RIGHT * 0.0 + DOWN * 0.2)
        arrows = VGroup(*[Arrow(ins[k].get_right(), outs[1 if k == 3 else 0].get_left(), buff=0.15, stroke_width=3,
                                color=GREY_C, max_tip_length_to_length_ratio=0.08) for k in range(4)])
        q = label(r"output 0: \ which of three inputs was it?", font_size=26, color=NO).next_to(outs, RIGHT, buff=0.6)
        kT = 1.380649e-23 * 300 * math.log(2)
        land = VGroup(label(r"Landauer (1961): \ erasing one bit of information \\ must release at least", font_size=26,
                            color=GREY_A),
                      MathTex(r"k_B T \ln 2 \approx " + f"{kT * 1e21:.1f}" + r"\times 10^{-21}\ \text{J}", font_size=36,
                              color=COST),
                      note(r"at room temperature; \ today's gates spend roughly a million times more", font_size=22)
                      ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "One last question about gates, and a glimpse of the end of the series. <bookmark mark='a'/> An and gate "
            "takes four possible inputs to two possible outputs. Three different inputs all give zero. "
            "<bookmark mark='b'/> Seeing a zero, you cannot tell which of them it was: the gate has destroyed "
            "information. <bookmark mark='c'/> In 1961 Rolf Landauer, at IBM, argued that destroying information has a "
            "physical price. Erasing one bit must release at least k T log two of heat, about three zeptojoules at room "
            "temperature. Real gates spend about a million times more than that, so the limit is far away, but it is a "
            "law of physics, not of engineering."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ins), FadeIn(outs))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(q))
            vo.wait_until("c")
            self.play(FadeIn(land, lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def toffoli(self):
        head = label(r"The Toffoli gate: \ reversible, \ and universal", font_size=36).to_edge(UP, buff=0.35)
        rows = VGroup()
        for k in range(8):
            a, b, c = (k >> 2) & 1, (k >> 1) & 1, k & 1
            c2 = c ^ (a & b)
            hot = a & b
            rows.add(VGroup(MathTex(f"{a}{b}{c}", font_size=32, color=DATA),
                            MathTex(r"\mapsto", font_size=30, color=GREY_C),
                            MathTex(f"{a}{b}{c2}", font_size=32, color=HEAD if hot else DATA)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, buff=0.16).move_to(LEFT * 3.6 + DOWN * 0.3)
        rule = MathTex(r"(a, b, c) \mapsto (a,\ b,\ c \oplus ab)", font_size=40, color=CTRL).move_to(RIGHT * 2.8 + UP * 1.6)
        txt = VGroup(label(r"a permutation of the 8 states: \ nothing is lost, \ run it twice to undo it", font_size=26,
                           color=GREY_A),
                     label(r"set $c = 1$: \ the third output is $\overline{ab}$ \ $=$ \ NAND", font_size=26, color=YES),
                     label(r"so reversible gates can compute anything, \\ if you keep the extra outputs (Bennett, 1973)",
                           font_size=26, color=HEAD),
                     label(r"Fredkin's gate: \ swap $b$ and $c$ \ when $a = 1$", font_size=24, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.32).next_to(rule, DOWN, buff=0.45)
        with self.voiceover(
            "Can you compute without forgetting? <bookmark mark='a'/> Tommaso Toffoli's gate has three inputs and three "
            "outputs. The first two pass straight through; the third is flipped exactly when the first two are both "
            "one. <bookmark mark='b'/> Its table is a shuffle of the eight states: every output comes from exactly one "
            "input, so nothing is lost, and applying it twice gives back what you started with. "
            "<bookmark mark='c'/> Feed it a constant one on the third wire, and the third output is not a and b: a "
            "NAND. So by chapter five, reversible gates can compute anything, as Charles Bennett showed in 1973, as "
            "long as you keep the extra outputs instead of throwing them away. Edward Fredkin's gate is another: it "
            "swaps its last two wires when the first is one, and it never changes how many ones there are, so it "
            "can be pictured as billiard balls bouncing through a maze, a model Fredkin and Toffoli proposed in 1982."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rule))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.12), FadeIn(txt[0]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(txt[1]), Indicate(VGroup(rows[6], rows[7]), color=HEAD))
            self.play(FadeIn(txt[2]), FadeIn(txt[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def future(self):
        head = label(r"Why this comes back", font_size=38).to_edge(UP, buff=0.4)
        lines = VGroup(*[label(t, font_size=28, color=c) for t, c in (
            (r"quantum computers must be reversible: \ their gates are rotations, \ which can always be undone",
             INF),
            (r"the Toffoli gate is one of them, \ and Part 53 simulates a small quantum computer with it", HEAD),
            (r"the same move, \ keeping what you would have thrown away, \\ turns up in undo logs and journaling "
             r"file systems \ (Parts 34 and 35)", GREY_A),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to(DOWN * 0.1)
        with self.voiceover(
            "This is not just a curiosity. <bookmark mark='a'/> A quantum computer must be reversible: its gates are "
            "rotations of a state, and every rotation can be undone. <bookmark mark='b'/> The Toffoli gate is one of its "
            "standard gates, and in Part 53 we will simulate a small quantum computer, Toffoli gates included. "
            "<bookmark mark='c'/> And the idea of keeping what you would have thrown away, so you can go back, appears "
            "much higher up the tower, in the logs that let databases and file systems undo a crash."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abc", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
