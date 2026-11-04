from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, box, fmt,
                                  load, mono)


class Deep(VoiceoverScene):
    def construct(self):
        self.card()
        self.race()
        self.power()

    def card(self):
        card = chapter_card(12, r"Deeper, \ and the end of the race", r"Why did clock rates stop rising?",
                            lit=(2000, 2004), extra=((2000, r"Pentium 4: 20 stages"), (2004, r"31 stages; Tejas cancelled")), part=PART)
        with self.voiceover("Chapter twelve. Deeper, and the end of the race."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def race(self):
        d = load("depth")
        head = label(r"The megahertz race", font_size=38).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[1992, 2024, 4], y_range=[0, 6500, 1000], x_length=7.6, y_length=4.2, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).move_to(LEFT * 2.0 + DOWN * 0.4)
        ax.x_axis.add_numbers(list(range(1996, 2025, 8)), font_size=16, num_decimal_places=0, group_with_commas=False)
        ax.y_axis.add_numbers(list(range(1000, 7000, 1000)), font_size=16, num_decimal_places=0)
        yl = note(r"top desktop clock, \ MHz \ (approximate)", font_size=20).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        pts = VGroup(*[Dot(ax.c2p(y, f), radius=0.06, color=CLOCK) for y, f, _ in d["history"]])
        hp = [ax.c2p(y, f) for y, f, _ in d["history"]]
        line = VMobject(color=CLOCK, stroke_width=2.5).set_points_as_corners(hp[:6])
        line1 = VMobject(color=CLOCK, stroke_width=2.5).set_points_as_corners(hp[5:7])
        line2 = VMobject(color=CLOCK, stroke_width=2.5).set_points_as_corners(hp[6:])
        p4 = [(y, f, n) for y, f, n in d["history"] if "Prescott" in n][0]
        pl = label(r"Pentium 4 \\ Prescott, \ 31 stages", font_size=18, color=NO).next_to(ax.c2p(p4[0], p4[1]), UP,
                                                                                     buff=0.15)
        stages = VGroup(*[label(rf"{n}: \ {k} stages", font_size=20, color=GREY_A) for n, k in d["stages"]]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).move_to(RIGHT * 4.0 + UP * 1.2)
        story = VGroup(
            label(r"deeper pipelines, \ shorter stages, \ higher clocks: \\ the number that sold computers", font_size=20,
                  color=GREY_A),
            label(r"2004: \ Intel cancels Tejas, \ the next, \ deeper Pentium 4", font_size=20, color=NO),
            label(r"2006: \ Core 2, \ 14 stages, \ a lower clock, \ faster", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 4.0 + DOWN * 1.2)
        with self.voiceover(
            "Chapter two's model says deeper pipelines pay, up to a point. In the 1990s the industry followed it. "
            "<bookmark mark='a'/> Clock rates rose from sixty-six megahertz in 1993 to a gigahertz by 2000, partly from "
            "faster transistors, and partly from cutting the work into more, shorter stages. <bookmark mark='b'/> "
            "Intel's Pentium 4 of 2000 had twenty stages, and its 2004 Prescott version thirty-one, close to the "
            "optimum our model found for Pebble, reaching three point eight gigahertz. Megahertz sold computers. "
            "<bookmark mark='c'/> Then the race stopped. In 2004 Intel cancelled the Pentium 4's successor, and in 2006 "
            "it replaced the whole line with the Core 2: fourteen stages, a lower clock, and faster programs. Clock "
            "rates have crept up only slowly since. Something other than the pipeline model had become the limit."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(line), LaggedStart(*[FadeIn(p) for p in pts[:6]], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(line1), FadeIn(pts[6]), FadeIn(pl), FadeIn(stages[:3]), FadeIn(story[0]))
            vo.wait_until("c")
            self.play(Create(line2), FadeIn(pts[7:]), FadeIn(stages[3]), FadeIn(story[1]), FadeIn(story[2]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def power(self):
        head = label(r"The power wall", font_size=38).to_edge(UP, buff=0.35)
        eq = MathTex(r"P", r"\approx", r"\alpha", r"\,C\,", r"V^2", r"f", font_size=56).move_to(UP * 1.7)
        eq[0].set_color(NO)
        eq[4].set_color(HEAD)
        eq[5].set_color(CLOCK)
        terms = VGroup(
            label(r"$\alpha$: \ how often a wire switches; \ $C$: \ how much it holds; \ $V$: \ the supply voltage; \ "
                  r"$f$: \ the clock", font_size=22, color=GREY_A),
        ).next_to(eq, DOWN, buff=0.3)
        pts = VGroup(
            label(r"Dennard scaling \ (1974): \ shrink a transistor, \ lower $V$ with it, \ and power per area stays "
                  r"constant", font_size=24, color=YES),
            label(r"by about 2005, \ $V$ could fall no further \ (leakage), \ so every extra GHz cost power", font_size=24,
                  color=NO),
            label(r"a deep pipeline makes it worse: \ more registers clocked, \ more work thrown away per mistake",
                  font_size=24, color=NO),
            label(r"the transistors kept coming \ (Moore's law); \ the industry spent them on more cores \ (Part 10)",
                  font_size=24, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The limit was heat. <bookmark mark='a'/> The power a chip burns switching its wires is roughly the "
            "activity, times the capacitance, times the voltage squared, times the clock frequency. "
            "<bookmark mark='b'/> For thirty years, Dennard scaling, from Robert Dennard of Part 5's memory cell, kept "
            "this in check: each new generation shrank the transistors and lowered the voltage with them, so a chip of "
            "the same size used about the same power while running faster. <bookmark mark='c'/> Around 2005 the voltage "
            "could not go much lower without the transistors leaking current even when off, and every extra gigahertz "
            "now cost power directly, a hundred watts and more in a desktop chip. Deep pipelines made it worse: more "
            "pipeline registers clocked every cycle, more speculative work thrown away. <bookmark mark='d'/> Moore's law "
            "still delivered more transistors, so the industry spent them differently: several processor cores on one "
            "chip, each at a modest clock, which is where Part 10 goes."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(terms))
            vo.wait_until("b")
            self.play(FadeIn(pts[0]))
            vo.wait_until("c")
            self.play(FadeIn(pts[1]), Indicate(eq[4], color=HEAD))
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()
