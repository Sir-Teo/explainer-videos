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


class Race(WatchScene):
    def construct(self):
        self.card()
        self.race()
        self.table()

    def card(self):
        self.chapter(5, r"The adders, raced", r"Which adder is fastest, and what does it cost?", lit=(1962,), part=PART, said="Chapter five. The adders, raced.")



    # ------------------------------------------------------------------
    def race(self):
        self.ask(r"Which adder do real 64-bit processors use?", [r"ripple carry", r"a prefix tree", r"carry select"], 1,
                 say="Which of these adders is inside the processor you're watching on?",
                 reveal="A prefix tree, tuned to the length of its wires.")
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
