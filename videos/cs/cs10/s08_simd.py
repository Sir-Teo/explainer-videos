from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs10.common import (BG, CODE, CORE_COLORS, CTRL, DATA, FUNC, HEAD, NO, PART, YES, bar_chart, load,
                                   mono)


class Simd(VoiceoverScene):
    def construct(self):
        self.card()
        self.flynn()
        self.history()
        self.lanes()
        self.measured()

    def card(self):
        card = chapter_card(7, r"SIMD and vectors", r"Can one instruction do thirty-two things at once?",
                            lit=(1966, 1976), extra=((1966, r"Flynn's taxonomy"), (1976, r"the Cray-1")), part=PART)
        with self.voiceover("Chapter seven. SIMD and vectors."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def flynn(self):
        head = label(r"Flynn's taxonomy \ (1966)", font_size=36).to_edge(UP, buff=0.35)
        cells = {(0, 0): (r"SISD", r"one instruction stream, \\ one data stream: \\ a plain core", GREY_A),
                 (1, 0): (r"SIMD", r"one instruction, \\ many data: \\ vector units, \ GPUs", YES),
                 (0, 1): (r"MISD", r"many instructions, \\ one data: \\ (rare)", GREY_D),
                 (1, 1): (r"MIMD", r"many instruction streams: \\ multicores, \ clusters", DATA)}
        g = VGroup()
        for (c, r), (name, desc, col) in cells.items():
            box = RoundedRectangle(width=4.2, height=1.9, corner_radius=0.12, stroke_color=col, stroke_width=2.2)
            box.move_to([c * 4.5 - 2.25, -r * 2.1 + 0.6, 0])
            t = VGroup(label(name, font_size=30, color=col), label(desc, font_size=19, color=GREY_A)).arrange(
                DOWN, buff=0.15).move_to(box)
            g.add(VGroup(box, t))
        xl = label(r"one data stream $\to$ many", font_size=18, color=GREY_B).next_to(g, DOWN, buff=0.2)
        yl = label(r"one instruction stream $\to$ many", font_size=18, color=GREY_B).rotate(PI / 2).next_to(
            g, LEFT, buff=0.2)
        xl = VGroup(xl, yl)
        with self.voiceover(
            "In 1966 Michael Flynn sorted computers by two questions: how many instruction streams, and how many data "
            "streams. <bookmark mark='a'/> One of each is an ordinary core. <bookmark mark='b'/> Many instruction "
            "streams, each with its own data, is what we have been building: several cores, or several machines. "
            "<bookmark mark='c'/> But there is a cheaper kind of parallelism: one instruction applied to many data at "
            "once. Single instruction, multiple data, SIMD. One decoder, one instruction fetched, and eight or "
            "sixteen or thirty-two arithmetic units doing the same thing to different numbers."
        ) as vo:
            self.play(FadeIn(head))
            for mk, k in zip("abc", (0, 3, 1)):
                vo.wait_until(mk)
                self.play(FadeIn(g[k]))
            self.play(FadeIn(g[2]), FadeIn(xl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        head = label(r"Vectors, \ from the Cray-1 to today", font_size=34).to_edge(UP, buff=0.3)
        items = [(1976, r"Cray-1", 64 * 64, r"vector registers of 64 numbers", NO),
                 (1997, r"MMX", 64, r"64 bits", GREY_B), (1999, r"SSE", 128, r"128 bits", DATA),
                 (2005, r"Arm NEON", 128, r"128 bits", CTRL),
                 (2011, r"AVX", 256, r"256 bits", DATA), (2016, r"AVX-512", 512, r"512 bits", DATA),
                 (2016, r"Arm SVE", 2048, r"128 to 2048 bits, \ chosen by the chip", CTRL),
                 (2021, r"RISC-V V", 2048, r"vector length chosen by the chip", FUNC)]
        rows = VGroup()
        for y, n, bits, d, c in items:
            w = 0.6 + 0.55 * np.log2(bits / 32)
            bar = Rectangle(width=w, height=0.32, stroke_width=0, fill_color=c, fill_opacity=0.75)
            rows.add(VGroup(label(rf"{y}", font_size=19, color=GREY_B), label(n, font_size=21, color=c), bar,
                            label(d, font_size=18, color=GREY_A)))
        rows.arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(DOWN * 0.2)
        for r in rows:
            r[0].move_to([-5.8, r.get_y(), 0])
            r[1].move_to([-4.9, r.get_y(), 0], aligned_edge=LEFT)
            r[2].move_to([-2.4, r.get_y(), 0], aligned_edge=LEFT)
            r[3].next_to(r[2], RIGHT, buff=0.2)
        cray = note(r"the Cray-1: \ 80 MHz, \ 160 megaflops at peak, \ results chained from one vector unit into the "
                    r"next", font_size=18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The idea is old. <bookmark mark='a'/> Seymour Cray's Cray-1, in 1976, had eight vector registers of "
            "sixty-four numbers each, and one instruction could add two whole vectors, with the results streaming "
            "from one unit straight into the next. At eighty megahertz it reached a hundred and sixty million "
            "floating-point operations a second, the fastest computer of its day. <bookmark mark='b'/> Twenty years "
            "later SIMD came to the desktop as short vectors packed into wide registers: Intel's MMX, sixty-four bits, "
            "then SSE, AVX and AVX-512, doubling the width each time. Arm's phones have NEON. <bookmark mark='c'/> "
            "The newest designs, Arm's SVE and RISC-V's vector extension, return to Cray's idea: the program does "
            "not say how wide the vectors are, and each chip chooses, so the same code runs on narrow and wide "
            "machines alike."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(cray))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:6]], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[6]), FadeIn(rows[7]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lanes(self):
        head = label(r"The Job's scan, \ thirty-two entries at a time", font_size=32).to_edge(UP, buff=0.3)
        lens = [3, 5, 2, 4, 7, 3, 5, 9, 4, 2, 6, 5, 3, 8, 4, 5, 2, 3, 6, 4, 5, 7, 3, 2, 4, 10, 5, 3, 6, 4, 2, 5]
        key = 5
        cell = 0.36
        row = VGroup(*[VGroup(Square(side_length=cell, stroke_color=GREY_C, stroke_width=1.2),
                              Text(str(v), font="DejaVu Sans Mono", font_size=15, color=WHITE)) for v in lens])
        for c in row:
            c[1].move_to(c[0])
        row.arrange(RIGHT, buff=0.02).shift(UP * 1.0)
        rl = label(r"32 entry lengths \ (one byte each, \ in their own array)", font_size=18, color=GREY_B).next_to(
            row, UP, buff=0.15)
        bc = VGroup(*[VGroup(Square(side_length=cell, stroke_color=CTRL, stroke_width=1.2),
                             Text(str(key), font="DejaVu Sans Mono", font_size=15, color=CTRL)) for _ in lens])
        for c in bc:
            c[1].move_to(c[0])
        bc.arrange(RIGHT, buff=0.02).next_to(row, DOWN, buff=0.35)
        bl = label(r"the word's length, \ copied into every lane", font_size=18, color=CTRL).next_to(bc, DOWN,
                                                                                                    buff=0.12)
        mask = VGroup(*[VGroup(Square(side_length=cell, stroke_color=YES if v == key else GREY_D, stroke_width=1.2,
                                      fill_color=YES, fill_opacity=0.5 if v == key else 0),
                               Text("1" if v == key else "0", font="DejaVu Sans Mono", font_size=15,
                                    color=WHITE if v == key else GREY_D)) for v in lens])
        for c in mask:
            c[1].move_to(c[0])
        mask.arrange(RIGHT, buff=0.02).next_to(bl, DOWN, buff=0.35)
        ml = label(r"one compare instruction: \ a 32-bit mask of the candidates", font_size=18, color=YES).next_to(
            mask, DOWN, buff=0.12)
        code = VGroup(mono("m = movemask(cmpeq(load32(len + i), set1(L)));", 18),
                      mono("while (m) { j = i + ctz(m); if (same letters) return j; m &= m - 1; }", 18)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here is SIMD applied to the Job. Most of its time goes into scanning the table, and most entries are "
            "rejected on their length alone. <bookmark mark='a'/> So keep the lengths in an array of their own, one "
            "byte each: Part 9's structure of arrays. <bookmark mark='b'/> Copy the length of the word being looked "
            "up into all thirty-two lanes of a 256-bit register. <bookmark mark='c'/> One AVX2 instruction compares "
            "all thirty-two pairs at once, and another squeezes the results into a thirty-two-bit mask. <bookmark "
            f"mark='d'/> Only the entries whose bit is set, here {sum(v == key for v in lens)}, are compared letter "
            "by letter. One iteration "
            "of the loop now does the work of thirty-two."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(row), FadeIn(rl))
            vo.wait_until("b")
            self.play(FadeIn(bc), FadeIn(bl))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(m) for m in mask], lag_ratio=0.02), FadeIn(ml))
            vo.wait_until("d")
            self.play(*[Indicate(row[k], color=YES) for k, v in enumerate(lens) if v == key], FadeIn(code))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        jc = {(r["threads"], r["simd"]): r for r in load("jobc")["rows"]}
        head = label(r"The Job in C, \ on this computer, \ one core", font_size=34).to_edge(UP, buff=0.3)
        a, b = jc[(1, False)]["seconds"], jc[(1, True)]["seconds"]
        ch = bar_chart([a, b], [r"scalar: \ one entry \\ per iteration", r"AVX2: \ thirty-two \\ per iteration"],
                       [GREY_B, YES], height=3.2, bar_w=1.6, gap=1.6, fmt_=lambda v: f"{v:.1f} s",
                       font_size=22).move_to(DOWN * 0.3 + LEFT * 2.2)
        why = VGroup(
            label(rf"{a / b:.1f} times faster, \ not 32", font_size=26, color=HEAD),
            label(r"same-length entries are still \\ compared letter by letter", font_size=20, color=GREY_A),
            label(r"the 58 KB of lengths stream \\ from L2, \ not L1", font_size=20, color=GREY_A),
            label(r"the rest of the program \ (reading, \\ appending) \ is not vectorized: \\ Amdahl again",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(ch, RIGHT, buff=0.8)
        auto = note(r"the same algorithm as Pebble's program, \ the same top twenty: \ checked against the reference",
                    font_size=17).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "We wrote the Job in C with exactly Pebble's algorithm, ran it on all thirty novels on this computer, "
            "and checked its top twenty against the reference. <bookmark mark='a'/> The scalar version, one entry per "
            f"iteration, takes {a:.0f} seconds. <bookmark mark='b'/> The AVX2 version takes {b:.0f}. <bookmark "
            f"mark='c'/> {a / b:.0f} times faster, not thirty-two, and the reasons are instructive. Entries with the "
            "same length as the word still need a letter-by-letter comparison. The lengths array, fifty-eight "
            "kilobytes, is too big for the first-level cache and streams from the second. And the rest of the "
            "program is not vectorized at all. Compilers can vectorize simple loops by themselves, but not this one, "
            "which stops as soon as it finds a match; here the speedup had to be written by hand."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch[0]), FadeIn(ch.names), FadeIn(auto))
            vo.wait_until("a")
            self.play(GrowFromEdge(ch.bars[0], DOWN), FadeIn(ch.vals[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(ch.bars[1], DOWN), FadeIn(ch.vals[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(w) for w in why], lag_ratio=0.4), run_time=3)
        self.wait(0.3)
        self.clear_scene()
