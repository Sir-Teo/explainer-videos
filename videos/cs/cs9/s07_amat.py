from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, fmt, load)


class Amat(VoiceoverScene):
    def construct(self):
        self.card()
        self.formula()
        self.levels()

    def card(self):
        card = chapter_card(6, r"Average memory access time", r"What does a hierarchy cost, on average?", part=PART)
        with self.voiceover("Chapter six. Average memory access time."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def formula(self):
        head = label(r"One level", font_size=38).to_edge(UP, buff=0.4)
        f = MathTex(r"\text{AMAT}", r"=", r"t_{\text{hit}}", r"+", r"m", r"\times", r"t_{\text{penalty}}",
                    font_size=56).move_to(UP * 1.0)
        f[2].set_color(YES)
        f[4].set_color(NO)
        f[6].set_color(INF)
        ex = MathTex(r"= 4 + 0.05 \times 200 = 14 \text{ cycles}", font_size=42).next_to(f, DOWN, buff=0.5)
        keys = label(r"hit time, \ miss rate, \ miss penalty: \ three knobs, \ and every design trades them",
                     font_size=26, color=HEAD).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "How long does a memory access take, on average? <bookmark mark='a'/> Every access pays the hit time of "
            "the cache. A fraction m of them, the miss rate, also pay the miss penalty: the time to fetch the line "
            "from wherever it is. <bookmark mark='b'/> With a four-cycle cache that misses five percent of the time "
            "in front of a two-hundred-cycle memory, the average is fourteen cycles: the five percent of misses cost "
            "two and a half times as much as all the hits together. <bookmark mark='c'/> Three knobs, and every cache "
            "design trades them: a bigger cache lowers the miss rate but raises the hit time; more ways the same."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(Write(ex))
            vo.wait_until("c")
            self.play(FadeIn(keys))
        self.wait(0.3)
        self.clear_scene()

    def levels(self):
        st = load("staircase")
        pts = {p["bytes"]: p["ns"] for p in st["points"]}
        head = label(r"Many levels: \ the penalty is the next level's AMAT", font_size=34).to_edge(UP, buff=0.35)
        f = MathTex(r"\text{AMAT} = t_1 + m_1 \big( t_2 + m_2 \big( t_3 + m_3\, t_{\text{DRAM}} \big)\big)",
                    font_size=44).move_to(UP * 1.4)
        l1, l2, l3, dram = pts[16 << 10], pts[256 << 10], pts[2 << 20], pts[8 << 20]
        m1, m2, m3 = 0.10, 0.20, 0.30
        amat = l1 + m1 * (l2 + m2 * (l3 + m3 * dram))
        ex = MathTex(rf"= {l1:.1f} + 0.1\,\big({l2:.1f} + 0.2\,\big({l3:.0f} + 0.3 \times {dram:.0f}\big)\big) "
                     rf"\approx {amat:.1f}\ \text{{ns}}", font_size=36).next_to(f, DOWN, buff=0.45)
        cap = note(r"this machine's measured latencies \ (chapter 7); \ illustrative miss rates", font_size=20).next_to(
            ex, DOWN, buff=0.2)
        punch = VGroup(
            label(rf"DRAM is {dram / l1:.0f} times slower than L1, \ yet the average access is only {amat / l1:.1f} "
                  r"times slower", font_size=26, color=YES),
            label(r"if each level catches most of what the one above misses", font_size=26, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "With several levels, the formula nests: the miss penalty of each level is the average access time of "
            "the level below it. <bookmark mark='a'/> Put in this machine's measured latencies, which the next "
            "chapter measures, and some typical miss rates: ten percent of accesses miss L1, a fifth of those miss "
            "L2, and so on. <bookmark mark='b'/> The average comes to about three and a half nanoseconds. DRAM is ninety times "
            "slower than L1, yet the average access is less than three times slower, as long as each level catches "
            "most of what the level above it misses. That is the whole bet of a memory hierarchy."
        ) as vo:
            self.play(FadeIn(head), Write(f))
            vo.wait_until("a")
            self.play(Write(ex), FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(punch))
        self.wait(0.3)
        self.clear_scene()
