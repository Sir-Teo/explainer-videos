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
        with self.voiceover(
            "Chapter six. Average memory access time."
        ):
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
        keys = label("serial lookup + additional miss penalty; \\ execution overlap is separate",
                     font_size=26, color=HEAD).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Define hit time and miss penalty before calculating an average. <bookmark mark='a'/> In this serial "
            "one-level model every demand access pays the hit lookup time, and a fraction m also pays an additional "
            "miss penalty. <bookmark mark='b'/> Four cycles plus five percent of an additional two hundred cycles "
            "gives fourteen cycles. The miss-penalty contribution is ten cycles per access, compared with four "
            "cycles of lookup cost on every access. If two hundred already included the lookup, the arithmetic would "
            "need a different definition. <bookmark mark='c'/> Capacity, associativity and organization can trade "
            "miss ratio, latency, area and energy. AMAT summarizes this access model; it does not by itself predict "
            "execution time when misses overlap or bandwidth becomes limiting."
        ) as vo:
            self.play(FadeIn(head))
            self.play(Write(f))
            vo.wait_until("a")
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
        f = MathTex(r"\text{AMAT} = t_1 + m_1 \big( \Delta t_2 + m_2 \big( \Delta t_3 + m_3\, \Delta t_4 \big)\big)",
                    font_size=44).move_to(UP * 1.4)
        cumulative = np.maximum.accumulate([pts[k] for k in (16 << 10, 512 << 10, 2 << 20, 64 << 20)])
        l1, l2, l3, dram = np.diff(np.r_[0, cumulative])
        m1, m2, m3 = 0.10, 0.20, 0.30
        amat = l1 + m1 * (l2 + m2 * (l3 + m3 * dram))
        ex = MathTex(rf"= {l1:.1f} + 0.1\,\big({l2:.1f} + 0.2\,\big({l3:.0f} + 0.3 \times {dram:.0f}\big)\big) "
                     rf"\approx {amat:.1f}\ \text{{ns}}", font_size=36).next_to(f, DOWN, buff=0.45)
        cap = note("nonnegative increments from cumulative samples; \\ illustrative conditional miss rates", font_size=18).next_to(
            ex, DOWN, buff=0.2)
        punch = VGroup(
            label(rf"largest cumulative sample: \ {cumulative[-1] / l1:.0f} times first; \ modeled mean: \ {amat / l1:.1f} "
                  r"times first", font_size=24, color=YES),
            label("a serial access expectation, \\ without overlap or bandwidth costs", font_size=24, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The serial formula nests across levels when lower-level miss ratios are conditional on reaching that "
            "level. <bookmark mark='a'/> The displayed timing illustration starts from cumulative pointer-chase "
            "samples, then takes nonnegative increments between them. Adding each cumulative latency again would "
            "double-count earlier lookup time. We choose the miss ratios for illustration; they are not measured "
            "typical rates for this host. <bookmark mark='b'/> The resulting weighted average can be much smaller "
            "than the largest delay when few requests reach that delay. The sample points do not isolate hardware "
            "cache levels, and this simple expectation omits overlap, queuing, prefetch costs and write traffic. Use "
            "it to reason about assumptions, then test actual workloads."
        ) as vo:
            self.play(FadeIn(head), Write(f))
            self.play(Write(ex), FadeIn(cap))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(punch))
        self.wait(0.3)
        self.clear_scene()
