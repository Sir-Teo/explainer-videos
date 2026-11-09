from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, REFERENCE_GHZ, YES, fmt, load)


class Wall(VoiceoverScene):
    def construct(self):
        self.card()
        self.gap()
        self.ratio()
        self.pyramid()

    def card(self):
        card = chapter_card(1, r"The memory wall", r"Why is memory so far away?", lit=(1995,),
                            extra=((1995, r"Wulf and McKee"),), part=PART)
        with self.voiceover(
            "Chapter one. The memory wall."
        ):
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
        lm = label("DRAM latency improvement: \\ illustrative 7\\% per year", font_size=20, color=NO).next_to(ax.c2p(1996, 0.47), DOWN,
                                                                                      buff=0.2)
        gap = DoubleArrow(ax.c2p(2004, 0.75), ax.c2p(2004, 3.75), color=HEAD, buff=0.05, stroke_width=3)
        gl = label(r"the gap", font_size=22, color=HEAD).next_to(gap, RIGHT, buff=0.1)
        quote = label(r"Wulf and McKee, \ 1995: \ ``Hitting the memory wall: \ implications of the obvious''",
                      font_size=22, color=HIST).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "These curves illustrate a historical divergence; they are extrapolations from stated growth rates, not "
            "a new measurement series. <bookmark mark='a'/> Processor performance improved rapidly in the selected "
            "era, with changes in clocks, parallel execution and other design choices. <bookmark mark='b'/> DRAM "
            "access latency improved more slowly. The red curve represents improvement in latency, so rising means "
            "shorter access time, not increasing delay. <bookmark mark='c'/> Compounding different rates creates a "
            "widening ratio. The precise gap depends on the interval, workload and definitions. <bookmark mark='d'/> "
            "Wulf and McKee's 1995 memory-wall argument explains why memory stalls can consume an increasing share "
            "of execution. It does not imply that every program eventually has the same bottleneck."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yl), FadeIn(cap))
            self.play(Create(cpu), FadeIn(lc), run_time=2.0)
            vo.wait_until("a")
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
        ghz = REFERENCE_GHZ
        pts = {p["bytes"]: p["ns"] for p in st["points"]}
        l1, dram = pts[16 << 10], pts[64 << 20]
        head = label(r"The wall is a ratio", font_size=38).to_edge(UP, buff=0.4)
        lines = VGroup(
            label(rf"16 KiB / 64 MiB walks: \ {l1:.1f} ns / {dram:.0f} ns: \ {dram / l1:.0f} times", font_size=26,
                  color=GREY_A),
            label(rf"at assumed 885 MHz: \ large-set proxy {j['clocks']['pebble']['latencies'][3]} cycles",
                  font_size=26, color=DATA),
            label(rf"at illustrative {ghz:g} GHz: \ the same proxy {j['clocks']['comparison clock']['latencies'][3]} "
                  r"cycles", font_size=26, color=NO),
            label(r"the faster the core, \ the higher the wall: \ the answer is a hierarchy", font_size=28,
                  color=HEAD),
        ).arrange(DOWN, buff=0.45).move_to(DOWN * 0.1)
        with self.voiceover(
            "Nanoseconds become core cycles only after a clock is specified. <bookmark mark='a'/> The displayed "
            "small-set and large-set times come from this host's dependent random walks. They are effective access "
            "times, not isolated SRAM-cell and DRAM-chip timings. <bookmark mark='b'/> Multiply nanoseconds by the "
            "assumed Pebble frequency to obtain its cycle budget. The hierarchy model assigns capacities and uses "
            "selected timing points as calibration proxies. <bookmark mark='c'/> A faster illustrative reference "
            "clock turns the same nanoseconds into more cycles. That reference is not a measured frequency of this "
            "host. <bookmark mark='d'/> Caches and overlap can reduce exposed waiting, but dependencies, throughput "
            "and memory-system limits determine how much. A single latency ratio does not predict program speedup."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(l, shift=UP * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pyramid(self):
        head = label(r"The hierarchy: \ small and fast, \ big and cheap", font_size=36).to_edge(UP, buff=0.35)
        levels = [(r"registers", r"about 1 KiB", r"in the core", YES, 1.6),
                  (r"L1 \ / \ L2 caches", r"32 KiB \ / \ 1 MiB per core", r"SRAM on the chip", YES, 3.0),
                  (r"L3", r"tens of MiB, \ shared", r"SRAM on the chip", DATA, 4.4),
                  (r"DRAM", "GiB to TiB \\ (examples)", "capacity, placement and product vary", CTRL, 5.8),
                  (r"SSD", r"terabytes", "nonvolatile flash storage", INF, 7.2),
                  (r"disk", r"tens of terabytes", "magnetic storage; workload matters", NO, 8.6)]
        g = VGroup()
        for k, (name, size, cost, col, w) in enumerate(levels):
            r = Rectangle(width=w, height=0.62, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.18)
            t = label(name, font_size=22, color=WHITE).move_to(r)
            g.add(VGroup(r, t))
        g.arrange(DOWN, buff=0.06).move_to(LEFT * 1.6 + DOWN * 0.2)
        sides = VGroup()
        for (name, size, cost, col, w), row in zip(levels, g):
            side = label(rf"{size} \quad {cost}", font_size=19, color=col)
            available = 6.6 - row.get_right()[0] - 0.3
            if side.width > available:
                side.scale_to_fit_width(available)
            sides.add(side.next_to(row, RIGHT, buff=0.3))
        arrow = Arrow(g.get_corner(UL) + LEFT * 0.25, g.get_corner(DL) + LEFT * 0.25,
                      color=GREY_B, stroke_width=3)
        al = label(r"slower, \\ bigger, \\ cheaper", font_size=18, color=GREY_B).next_to(arrow, LEFT, buff=0.06)
        if al.get_left()[0] < -6.8:
            al.shift(RIGHT * (-6.8 - al.get_left()[0]))
        cap = note("illustrative capacities and technologies; \\ costs vary", font_size=18).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "A hierarchy trades capacity, access time, bandwidth, energy and cost. <bookmark mark='a'/> Registers "
            "sit near execution units; caches commonly use SRAM. Six-transistor cells are a familiar SRAM example, "
            "not a universal implementation rule. The sizes shown are illustrative and vary by processor. <bookmark "
            "mark='b'/> DRAM commonly uses a transistor and capacitor per cell; flash and magnetic storage offer "
            "other capacity and persistence tradeoffs. Package placement, stacked memory, controllers and interfaces "
            "affect performance. Retail prices change with date, capacity and product class. <bookmark mark='c'/> "
            "The goal is to keep useful data close enough for the workload. Neither a fixed cost ratio between "
            "layers nor a single pyramid describes every computer."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(VGroup(r, sd)) for r, sd in zip(g[:3], sides[:3])], lag_ratio=0.3))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(r, sd)) for r, sd in zip(g[3:], sides[3:])], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(GrowArrow(arrow), FadeIn(al), FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()
