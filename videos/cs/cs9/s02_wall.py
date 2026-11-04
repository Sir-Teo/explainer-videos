from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, fmt, load)


class Wall(VoiceoverScene):
    def construct(self):
        self.card()
        self.gap()
        self.ratio()

    def card(self):
        card = chapter_card(1, r"The memory wall", r"Why is memory so far away?", lit=(1995,),
                            extra=((1995, r"Wulf and McKee"),), part=PART)
        with self.voiceover("Chapter one. The memory wall."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def gap(self):
        head = label(r"Processors against DRAM, \ 1980 to 2005", font_size=36).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[1980, 2006, 5], y_range=[0, 4.2, 1], x_length=9.5, y_length=4.4, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18}).move_to(DOWN * 0.3 + LEFT * 0.8)
        ax.x_axis.add_numbers(list(range(1980, 2006, 5)), font_size=16, group_with_commas=False)
        yl = VGroup(*[label(t, font_size=16, color=GREY_B).next_to(ax.c2p(1980, e), LEFT, buff=0.1)
                      for e, t in ((0, "1"), (1, "10"), (2, "100"), (3, "1,000"), (4, "10,000"))])
        cap = note(r"improvement since 1980 \ (log scale; \ growth rates as Hennessy and Patterson give them)",
                   font_size=18).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)

        def grow(rates):
            xs, ys, v = [], [], 0.0
            for yr in range(1980, 2006):
                xs.append(yr)
                ys.append(v)
                r = next(r for (a, b), r in rates.items() if a <= yr < b)
                v += np.log10(r)
            return VMobject(stroke_width=4).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, ys)])

        cpu = grow({(1980, 1986): 1.25, (1986, 2006): 1.52}).set_color(DATA)
        mem = grow({(1980, 2006): 1.07}).set_color(NO)
        lc = label(r"processor performance: \ +25\%, \ then +52\% a year", font_size=20, color=DATA).next_to(
            ax.c2p(1994, 2.6), LEFT, buff=0.1)
        lm = label(r"DRAM latency: \ about +7\% a year", font_size=20, color=NO).next_to(ax.c2p(1996, 0.47), DOWN,
                                                                                      buff=0.2)
        gap = DoubleArrow(ax.c2p(2004, 0.75), ax.c2p(2004, 3.75), color=HEAD, buff=0.05, stroke_width=3)
        gl = label(r"the gap", font_size=22, color=HEAD).next_to(gap, RIGHT, buff=0.1)
        quote = label(r"Wulf and McKee, \ 1995: \ ``Hitting the memory wall: \ implications of the obvious''",
                      font_size=22, color=HIST).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "For thirty years two curves pulled apart. <bookmark mark='a'/> Processors got faster at about a quarter "
            "a year in the early 1980s, then, through the pipelining and out-of-order execution of the last two "
            "parts, at about half again every year until 2003. <bookmark mark='b'/> The time to read a word from "
            "DRAM, main memory, improved by about seven percent a year. DRAM got enormously bigger and cheaper, but "
            "not much quicker. <bookmark mark='c'/> On a log scale, the gap between the curves grows to a factor of "
            "hundreds. <bookmark mark='d'/> In 1995 William Wulf and Sally McKee pointed out the obvious consequence: "
            "if the gap keeps growing, eventually every program waits on memory and processor speed stops mattering. "
            "They called it the memory wall."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yl), FadeIn(cap))
            vo.wait_until("a")
            self.play(Create(cpu), FadeIn(lc), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(mem), FadeIn(lm), run_time=2.0)
            vo.wait_until("c")
            self.play(GrowFromCenter(gap), FadeIn(gl))
            vo.wait_until("d")
            self.play(FadeIn(quote))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ratio(self):
        st = load("staircase")
        j = load("job")
        ghz = st["machine"]["ghz"]
        pts = {p["bytes"]: p["ns"] for p in st["points"]}
        l1, dram = pts[16 << 10], pts[8 << 20]
        head = label(r"The wall is a ratio", font_size=38).to_edge(UP, buff=0.4)
        lines = VGroup(
            label(rf"this machine: \ L1 {l1:.1f} ns, \ DRAM {dram:.0f} ns: \ {dram / l1:.0f} times slower", font_size=26,
                  color=GREY_A),
            label(rf"at Pebble's 885 MHz, \ DRAM is {j['clocks']['pebble']['latencies'][3]} cycles away",
                  font_size=26, color=DATA),
            label(rf"at this machine's {ghz:g} GHz, \ the same DRAM is {j['clocks']['this machine']['latencies'][3]} "
                  r"cycles away", font_size=26, color=NO),
            label(r"the faster the core, \ the higher the wall: \ the answer is a hierarchy", font_size=28,
                  color=HEAD),
        ).arrange(DOWN, buff=0.45).move_to(DOWN * 0.1)
        with self.voiceover(
            "The wall is a ratio, not a number. <bookmark mark='a'/> On this machine, the first-level cache answers "
            "in one and a half nanoseconds and DRAM in a hundred forty: about ninety times slower. <bookmark "
            "mark='b'/> To Pebble's out-of-order core, running at eight hundred eighty-five megahertz, DRAM is a "
            "hundred sixty-six cycles away. <bookmark mark='c'/> To this machine's own core, ticking three times "
            "faster, the same DRAM is five hundred twenty-five cycles away. <bookmark mark='d'/> Every speed-up of "
            "the core makes memory look further off. The answer, which every computer since the 1960s has used in "
            "some form, is not one memory but a hierarchy: small and fast near the core, large and slow further out, "
            "and the hope that most accesses find what they need nearby. Why that hope is usually justified is the "
            "next chapter."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
