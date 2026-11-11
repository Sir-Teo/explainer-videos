from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs4.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, KIND_COLOR, LIMIT, NO, PART, WIRE, YES,
                                  axis_plot, load)

NAMES = {"ripple": r"ripple", "carry-skip": r"carry-skip", "carry-select": r"carry-select",
         "brent-kung": r"Brent--Kung", "sklansky": r"Sklansky", "kogge-stone": r"Kogge--Stone"}


def block(w, h, text, color=CTRL, font_size=22):
    b = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=color, stroke_width=2.2, fill_color=BG,
                         fill_opacity=1)
    return VGroup(b, MathTex(text, font_size=font_size, color=color).move_to(b))


class Race(VoiceoverScene):
    def construct(self):
        self.card()
        self.select()
        self.skip()
        self.race()
        self.table()

    def card(self):
        card = chapter_card(5, r"The adders, raced", r"Which adder is fastest, and what does it cost?", lit=(1962,),
                            part=PART)
        with self.voiceover("Chapter five. The adders, raced."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def select(self):
        head = label(r"Carry-select: \ compute both answers, \ pick one later", font_size=36).to_edge(UP, buff=0.35)
        sizes = [1, 2, 3, 4, 5]
        blocks, muxes, links = VGroup(), VGroup(), VGroup()
        x = 5.6
        for k, w in enumerate(sizes):
            width = 0.45 * w + 0.5
            x -= width / 2
            if k == 0:
                b = block(width, 0.8, rf"{w}\text{{ bit}}", color=DATA).move_to([x, 0.6, 0])
                blocks.add(VGroup(b))
            else:
                b0 = block(width, 0.6, r"c = 0", color=GREY_B, font_size=20).move_to([x, 1.1, 0])
                b1 = block(width, 0.6, r"c = 1", color=GREY_B, font_size=20).move_to([x, 0.3, 0])
                m = block(width, 0.5, r"\text{mux}", color=HEAD, font_size=20).move_to([x, -0.7, 0])
                blocks.add(VGroup(b0, b1))
                muxes.add(m)
            x -= width / 2 + 0.35
        for k in range(1, len(sizes)):
            src = blocks[0][0].get_bottom() if k == 1 else muxes[k - 2].get_left()
            dst = muxes[k - 1].get_right()
            links.add(Line(src + (DOWN * 0.0), dst, color=HEAD, stroke_width=3))
        labs = VGroup(*[MathTex(rf"{w}", font_size=22, color=GREY_B).next_to(blocks[k], UP, buff=0.15)
                        for k, w in enumerate(sizes)])
        why = VGroup(
            label(r"each block adds its bits twice, \ for carry-in 0 and for carry-in 1, \ in parallel", font_size=26,
                  color=GREY_A),
            label(r"the real carry arrives \ and only chooses: \ one multiplexer per block", font_size=26, color=HEAD),
            label(r"blocks of 1, 2, 3, ... bits: \ ripple inside a block and the chain of choices \ finish together",
                  font_size=26, color=GREY_A),
            MathTex(r"1 + 2 + \cdots + k = n \ \Rightarrow \ k \approx \sqrt{2n}: \quad \text{delay } O(\sqrt n)",
                    font_size=32, color=CODE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Before the prefix trees, engineers found cheaper ways to stop waiting. <bookmark mark='a'/> Split the "
            "adder into blocks. Every block except the first adds its bits twice, once assuming the carry coming in is "
            "zero and once assuming it is one, both at the same time. <bookmark mark='b'/> When the real carry finally "
            "arrives, there is nothing left to add: it just chooses between two finished answers, with one "
            "multiplexer per block. <bookmark mark='c'/> Make the blocks grow, one bit, two, three, so that each "
            "block's internal ripple finishes just as the choosing chain reaches it. With k blocks covering n bits, k "
            "is about the square root of two n, and the delay grows like the square root of n. This is the "
            "carry-select adder, from 1962, at the cost of doing most of the work twice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(blocks, labs)))
            vo.wait_until("a")
            self.play(Indicate(blocks, scale_factor=1.02), FadeIn(why[0]))
            vo.wait_until("b")
            self.play(FadeIn(muxes), Create(links), FadeIn(why[1]))
            vo.wait_until("c")
            self.play(FadeIn(why[2]), FadeIn(why[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def skip(self):
        d = load("adders")
        r32 = {r["kind"]: r for r in d["rows"] if r["n"] == 32}
        head = label(r"Carry-skip, \ and a path that is never taken", font_size=36).to_edge(UP, buff=0.35)
        blocks = VGroup(*[block(1.9, 0.8, r"4\text{-bit ripple}", color=DATA, font_size=22) for _ in range(4)]).arrange(
            LEFT, buff=0.9).move_to(UP * 1.2)
        byp = VGroup()
        for b in blocks:
            p = block(0.9, 0.5, r"P = \textstyle\prod p_i", color=HEAD, font_size=18).next_to(b, DOWN, buff=0.45)
            byp.add(p)
        chain = VGroup(*[Arrow(blocks[i].get_left(), blocks[i + 1].get_right(), buff=0.05, color=WIRE, stroke_width=3,
                               max_tip_length_to_length_ratio=0.25) for i in range(3)])
        skips = VGroup(*[CurvedArrow(byp[i].get_left() + DOWN * 0.1, byp[i + 1].get_right() + DOWN * 0.1, angle=-0.6,
                                     color=HEAD, stroke_width=3) for i in range(3)])
        t1 = label(r"if every bit of a block propagates, \ its carry-in skips straight out", font_size=26,
                   color=HEAD).next_to(byp, DOWN, buff=0.55)
        cmp = VGroup(
            label(rf"32 bits: \ the longest path through the gates is \ {r32['carry-skip']['depth']} deep", font_size=28,
                  color=NO),
            label(rf"that path is false: \ largest observed delay \ {r32['carry-skip']['settle']}", font_size=28,
                  color=YES),
            note(r"a long carry skips the middle blocks; \ a block that ripples did not need its carry-in: \ a "
                 r"\textit{false path}", font_size=22),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A second trick is cheaper still. <bookmark mark='a'/> Keep ripple blocks of four bits, but give each one a "
            "bypass. If every bit in a block propagates, which one and gate detects straight from the inputs, a "
            "multiplexer passes the block's carry-in straight to its carry-out, skipping the ripple inside. "
            "<bookmark mark='b'/> This adder holds a lesson about timing. Count the longest path through its gates, "
            "and at thirty-two bits it is eighty-one deep, worse than the ripple adder. But simulate it, with every "
            "gate taking one unit of time, on chosen carry patterns and random inputs: the largest delay observed is "
            "twenty-nine. Sampling is not a proof of the maximum. <bookmark mark='c'/> The long path is false: whenever a carry would ripple through a block, "
            "that block was generating or killing its own carry anyway. Timing tools that only count gates "
            "overestimate such circuits, and a whole subfield, false-path analysis, exists to find them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(blocks), Create(chain))
            vo.wait_until("a")
            self.play(FadeIn(byp), Create(skips), FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeIn(cmp[0]))
            self.play(FadeIn(cmp[1]))
            vo.wait_until("c")
            self.play(FadeIn(cmp[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def race(self):
        d = load("adders")
        rows = d["rows"]
        head = label(r"Measured: \ gate delays and gates, \ 4 to 64 bits", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[2, 6, 1], y_range=[0, 130, 32], x_length=5.4, y_length=4.4, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18},
                  y_axis_config={"include_numbers": True}).move_to(LEFT * 3.3 + DOWN * 0.5)
        xl = VGroup(*[MathTex(str(2 ** k), font_size=20, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.15)
                      for k in range(2, 7)])
        t1 = note(r"delay (gate delays) \ against bits \ (log scale)", font_size=20).next_to(ax, UP, buff=0.12)
        ax2 = Axes(x_range=[2, 6, 1], y_range=[0, 1200, 300], x_length=5.4, y_length=4.4, tips=False,
                   axis_config={"color": GREY_C, "font_size": 18},
                   y_axis_config={"include_numbers": True}).move_to(RIGHT * 3.4 + DOWN * 0.5)
        xl2 = VGroup(*[MathTex(str(2 ** k), font_size=20, color=GREY_B).next_to(ax2.c2p(k, 0), DOWN, buff=0.15)
                       for k in range(2, 7)])
        t2 = note(r"gates \ against bits \ (log scale)", font_size=20).next_to(ax2, UP, buff=0.12)
        curves, curves2, keys = VGroup(), VGroup(), VGroup()
        for kind in NAMES:
            rs = sorted([r for r in rows if r["kind"] == kind], key=lambda r: r["n"])
            xs = [np.log2(r["n"]) for r in rs]
            curves.add(axis_plot(xs, [r["settle"] for r in rs], ax, KIND_COLOR[kind]))
            curves2.add(axis_plot(xs, [r["gates"] for r in rs], ax2, KIND_COLOR[kind]))
            keys.add(label(NAMES[kind], font_size=22, color=KIND_COLOR[kind]))
        keys.arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Now race them. Every adder here is a netlist from this series' hardware library, checked against Python's "
            "integers on every input at eight bits and on thousands of chosen inputs up to sixty-four, then timed gate "
            "by gate. <bookmark mark='a'/> On the left, delay against width. The ripple adder climbs in a straight "
            "line; carry-skip and carry-select bend like square roots; the three prefix adders barely rise, adding a "
            "couple of gate delays each time the width doubles. <bookmark mark='b'/> On the right, the bill. The ripple "
            "adder is cheapest, Kogge-Stone grows like n log n and costs more than three times as much at sixty-four "
            "bits, and carry-select pays for its duplicated work. Brent-Kung costs half again as much as the ripple, "
            "and is five times faster."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(t1), FadeIn(keys))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.2), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(ax2), FadeIn(xl2), FadeIn(t2))
            self.play(LaggedStart(*[Create(c) for c in curves2], lag_ratio=0.2), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        d = load("adders")
        r64 = {r["kind"]: r for r in d["rows"] if r["n"] == 64}
        head = label(r"64-bit adders, \ side by side", font_size=36).to_edge(UP, buff=0.35)
        rows = VGroup(VGroup(*[label(t, font_size=24, color=GREY_B) for t in (r"design", r"gates",
                                                                              r"deepest path", r"observed delay")]))
        for kind in NAMES:
            r = r64[kind]
            rows.add(VGroup(label(NAMES[kind], font_size=26, color=KIND_COLOR[kind]),
                            MathTex(str(r["gates"]), font_size=30, color=GREY_A),
                            MathTex(str(r["depth"]), font_size=30, color=NO if r["depth"] > r["settle"] + 5 else GREY_A),
                            MathTex(str(r["settle"]), font_size=30, color=YES)))
        for i, r in enumerate(rows):
            for j, m in enumerate(r):
                m.move_to([-4.2 + [0, 2.9, 5.3, 7.8][j], 1.9 - 0.55 * i, 0])
        foot = VGroup(
            label(r"a 64-bit Kogge--Stone adder settles in 15 gate delays, \ against the ripple adder's 129", font_size=26,
                  color=HEAD),
            note(r"real processors add 64 bits in well under a cycle, \ with prefix trees tuned to their wires "
                 r"(Han--Carlson, \ Ling adders, \ sparse trees)", font_size=22),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "At sixty-four bits, the numbers side by side. <bookmark mark='a'/> The ripple adder: three hundred and "
            "twenty gates, a hundred and twenty-nine delays. Kogge-Stone: about a thousand gates, fifteen delays, "
            "almost nine times faster for three and a half times the gates. <bookmark mark='b'/> That trade, spending "
            "area to buy time, is the theme of every chapter on hardware in this series. Real processors make it every "
            "time: their adders are prefix trees, tuned to the length of their wires, and they add sixty-four bits in "
            "a fraction of a clock cycle. Pebble's arithmetic unit will use Kogge-Stone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows[1:]], lag_ratio=0.25), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
