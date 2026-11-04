from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, LEVEL_COLOR, NO, PART, YES, fmt,
                                  load, mono, size_label, staircase_axes)

CHASE_C = ["for (i = 0; i < steps; i++)", "    p = *p;      /* the next address is in the line just read */"]


class Measured(VoiceoverScene):
    def construct(self):
        self.card()
        self.method()
        self.stairs()
        self.bandwidth()

    def card(self):
        card = chapter_card(7, r"This machine's staircase", r"How far away is each level, \ really?", lit=(2007,),
                            extra=((2007, r"Drepper: \ What every programmer should know"),), part=PART)
        with self.voiceover("Chapter seven. This machine's staircase."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def method(self):
        head = label(r"Measuring latency: \ chase a pointer", font_size=36).to_edge(UP, buff=0.4)
        code = VGroup(*[mono(s, 22) for s in CHASE_C]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(UP * 0.9)
        n = 10
        ring = VGroup(*[Square(side_length=0.5, stroke_color=GREY_C, stroke_width=1.5) for _ in range(n)]).arrange(
            RIGHT, buff=0.15).move_to(DOWN * 0.8)
        order = [0, 6, 3, 8, 1, 5, 9, 2, 7, 4]
        arrows = VGroup()
        for k in range(n):
            a, b = ring[order[k]], ring[order[(k + 1) % n]]
            arrows.add(CurvedArrow(a.get_top(), b.get_top(), angle=-0.8 if order[(k + 1) % n] > order[k] else 0.8,
                                   color=DATA, stroke_width=2, tip_length=0.12))
        cap = note(r"one pointer per 64-byte line, \ in a random cycle: \ no prefetcher can guess the next one",
                   font_size=20).next_to(ring, DOWN, buff=0.35)
        rule = label(r"each load needs the last one's value: \ no overlap, \ pure latency", font_size=26,
                     color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "To measure how far away each level really is, we need a program whose every load must wait for the "
            "previous one. <bookmark mark='a'/> Fill a block of memory with pointers, one per cache line, linked in a "
            "random cycle, and follow them: each load's address is the value the last load returned. <bookmark "
            "mark='b'/> Because the order is random, no prefetcher can guess the next line, and because each load "
            "depends on the last, an out-of-order core cannot overlap them. The time per step is the latency of "
            "wherever the line lives. Vary the size of the block, and the latency of each level appears in turn."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(code), FadeIn(ring))
            self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(cap), FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stairs(self):
        st = load("staircase")
        m = st["machine"]
        pts = st["points"]
        head = label(rf"The staircase, \ measured on this computer", font_size=34).to_edge(UP, buff=0.25)
        sub = note(rf"{m['cpu']}; \ lscpu: \ L1d {m['caches'].get('L1d', '?')}, \ L2 {m['caches'].get('L2', '?')}, \ "
                   rf"L3 {m['caches'].get('L3', '?')}", font_size=18).next_to(head, DOWN, buff=0.1)
        ax, ticks = staircase_axes(pts, x_length=10.8, y_length=4.2, ymax=350)
        g = VGroup(ax, ticks).move_to(DOWN * 0.45)
        ax.y_axis.add_numbers([0, 100, 200, 300], font_size=16, num_decimal_places=0)
        yl = note(r"nanoseconds per load", font_size=18).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        dots = VGroup(*[Dot(ax.c2p(np.log2(p["bytes"]), p["ns"]), radius=0.06, color=HEAD) for p in pts])
        line = VMobject(color=HEAD, stroke_width=3).set_points_as_corners([d.get_center() for d in dots])
        by = {p["bytes"]: p["ns"] for p in pts}
        ann = VGroup(
            label(rf"L1: \ {by[16 << 10]:.1f} ns", font_size=20, color=YES).next_to(ax.c2p(13, by[16 << 10]), UP,
                                                                                buff=0.25),
            label(rf"L2: \ {by[256 << 10]:.1f} ns", font_size=20, color=DATA).next_to(ax.c2p(18, by[256 << 10]), UP,
                                                                                  buff=0.5),
            label(rf"{by[2 << 20]:.0f} ns", font_size=20, color=CTRL).next_to(ax.c2p(21, by[2 << 20]), LEFT,
                                                                             buff=0.2),
            label(rf"DRAM: \ {by[8 << 20]:.0f} ns", font_size=20, color=NO).next_to(ax.c2p(23, by[8 << 20]), UP,
                                                                                 buff=0.15),
            label(rf"and page-table walks: \ {by[512 << 20]:.0f} ns", font_size=20, color=NO).next_to(
                ax.c2p(29, by[512 << 20]), LEFT, buff=0.2),
        )
        vm = label(r"lscpu says 33 MB of L3; \ this virtual machine falls off it near 4 MB", font_size=22,
                   color=GREY_A).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Here is the result, measured on the computer that made this video, a virtual machine on an Intel Xeon. "
            "<bookmark mark='a'/> Up to thirty-two kilobytes, a load takes one and a half nanoseconds: the L1 cache, "
            "about four cycles. <bookmark mark='b'/> Up to a megabyte, about four and a half: the L2. <bookmark "
            "mark='c'/> At two megabytes, twenty-five nanoseconds, part of the shared last level. <bookmark "
            "mark='d'/> And from four megabytes on, a hundred forty nanoseconds and climbing: DRAM. Past sixty-four "
            "megabytes it climbs further, to over three hundred, because the address translations themselves stop "
            "fitting in their own cache, the TLB, and every load first walks the page tables in memory. Part 32 "
            "explains that. <bookmark mark='e'/> One surprise: the processor reports thirty-three megabytes of "
            "third-level cache, but this machine falls off it near four. The cache is shared with whatever else runs "
            "on the chip; measured numbers are the ones to trust."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), Create(ax), FadeIn(ticks), FadeIn(yl))
            self.play(Create(line), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.05), run_time=2.5)
            for mk, a in zip("abcd", ann[:4]):
                vo.wait_until(mk)
                self.play(FadeIn(a))
            self.play(FadeIn(ann[4]))
            vo.wait_until("e")
            self.play(FadeIn(vm))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bandwidth(self):
        b = load("bandwidth")["points"]
        head = label(r"Bandwidth: \ reading in order", font_size=36).to_edge(UP, buff=0.3)
        xs = [np.log2(p["bytes"]) for p in b]
        ax = Axes(x_range=[min(xs), max(xs) + 0.5, 2], y_range=[0, 70, 10], x_length=10.5, y_length=4.2, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).move_to(DOWN * 0.4)
        ax.y_axis.add_numbers([0, 20, 40, 60], font_size=16, num_decimal_places=0)
        ticks = VGroup(*[label(size_label(p["bytes"]), font_size=15, color=GREY_B).next_to(
            ax.c2p(np.log2(p["bytes"]), 0), DOWN, buff=0.12) for p in b])
        yl = note(r"gigabytes per second, \ one core", font_size=18).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        bars = VGroup(*[Rectangle(width=0.45, height=4.2 * p["gbs"] / 70, stroke_width=0,
                                  fill_color=YES if p["bytes"] <= 1 << 20 else (CTRL if p["bytes"] <= 8 << 20 else NO),
                                  fill_opacity=0.85).move_to(ax.c2p(np.log2(p["bytes"]), 0), aligned_edge=DOWN)
                        for p in b])
        vals = VGroup(*[label(f"{p['gbs']:.0f}", font_size=16, color=GREY_A).next_to(bar, UP, buff=0.05)
                        for p, bar in zip(b, bars)])
        punch = label(r"in order, \ even DRAM delivers 9 GB/s: \ 64 bytes every 7 ns, \ though each one is 140 ns away",
                      font_size=24, color=HEAD).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Latency is one number; bandwidth is the other. Read a block of memory in order, as fast as possible. "
            "<bookmark mark='a'/> From the caches, about sixty gigabytes a second; from the middle level, about "
            "thirty; from DRAM, about nine. <bookmark mark='b'/> Notice what that means. Nine gigabytes a second is a "
            "sixty-four-byte line every seven nanoseconds, yet each line is a hundred forty nanoseconds away. Reading "
            "in order, the hardware has twenty lines in flight at once, fetched ahead by the prefetcher before "
            "anyone asks. Latency can be hidden; bandwidth cannot be exceeded. Remember that when the Job's table "
            "scans meet real memory."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks), FadeIn(yl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(x, DOWN) for x in bars], lag_ratio=0.1), FadeIn(vals))
            vo.wait_until("b")
            self.play(FadeIn(punch))
        self.wait(0.3)
        self.clear_scene()
