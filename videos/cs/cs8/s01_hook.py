from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, YES, OooChart, bar_chart,
                                  fmt, load, phase_legend)


class Hook(WatchScene):
    def construct(self):
        self.waiting()
        self.overtake()
        self.title(PART)

    # ------------------------------------------------------------------
    def waiting(self):
        d = load("hook")["miss"]["in order"]
        head = label("One-entry issue queue: \\ a blocked head delays later dispatch", font_size=34).to_edge(
            UP, buff=0.3)
        ch = OooChart(d["timeline"], cw=0.098, ch=0.3, label_width=2.4, label_size=14, c0=0, heads_every=10)
        ch.move_to(DOWN * 0.35)
        leg = phase_legend(font_size=17).to_edge(DOWN, buff=0.25)
        lw = ch.rows[4]
        miss = label(r"a cache miss: \ 60 cycles", font_size=22, color=INF).next_to(ch.bars[4], UP, buff=0.04)
        total = label(rf"{d['cycles']} cycles", font_size=26, color=NO).next_to(ch, RIGHT, buff=0.2).shift(DOWN * 1.8)
        with self.voiceover(
            "Start with a short program on this part's functional core, constrained to a one-entry issue queue. "
            "That forces instructions to start in program order. Rows are instructions; time runs to the right. "
            "<bookmark mark='a'/> The fifth instruction loads from a cold cache line. We assign a sixty-cycle miss "
            "latency. <bookmark mark='b'/> The next add needs that value and must wait. <bookmark "
            "mark='c'/> Several later instructions do not depend on the missing value. They still have their own "
            "dependencies and resource requirements, but this in-order configuration cannot pass the waiting add. "
            "Their useful work is delayed behind it. <bookmark mark='d'/> This recorded run takes eighty-one cycles "
            "for sixteen instructions, including setup and halt. It illustrates head-of-line blocking under the "
            "model's chosen resources and timing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch.heads), LaggedStart(*[FadeIn(r) for r in ch.rows], lag_ratio=0.05))
            self.play(FadeIn(leg), LaggedStart(*[FadeIn(VGroup(ch.bars[i], ch.commits[i])) for i in range(4)],
                                               lag_ratio=0.2))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(ch.bars[4], ch.commits[4])), Indicate(lw, color=INF), FadeIn(miss))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(ch.bars[5], ch.commits[5])))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(ch.bars[i], ch.commits[i])) for i in range(6, ch.n)],
                                  lag_ratio=0.15), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(total))
        self.wait(0.3)
        self.inorder = VGroup(ch, miss, total)
        self.play(FadeOut(head), FadeOut(leg), self.inorder.animate.scale(0.62).to_corner(UL, buff=0.3).shift(DOWN * 0.5))

    # ------------------------------------------------------------------
    def overtake(self):
        d = load("hook")["miss"]["out of order"]
        head = label("Out of order: \\ ready work competes for finite resources", font_size=32).to_edge(
            UP, buff=0.25)
        ch = OooChart(d["timeline"], cw=0.098, ch=0.3, label_width=2.4, label_size=14, c0=0, heads_every=10)
        ch.scale(0.62).to_corner(DR, buff=0.3).shift(UP * 0.2)
        total = label(rf"{d['cycles']} cycles", font_size=24, color=YES).next_to(ch, UP, buff=0.12).align_to(ch, RIGHT)
        keys = VGroup(
            label(r"the independent work runs \textit{during} the miss", font_size=24, color=FUNC),
            label("architectural results retire in program order", font_size=24, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DL, buff=0.4)
        with self.voiceover(
            "Now use the normal issue queue and ready-instruction selection on the same functional core. <bookmark "
            "mark='a'/> An instruction can start when its operands, execution resources and ordering rules allow. "
            "The load still misses, and its dependent add still waits. Later independent work can overlap the miss, "
            "while dependencies among those later instructions remain. <bookmark mark='b'/> Completed results wait "
            "for in-order architectural retirement, shown in blue. When the load finishes, the waiting add executes "
            "and the core retires the completed work in order. <bookmark mark='c'/> This run takes seventy cycles "
            "instead of eighty-one. The comparison changes queue capacity and scheduling freedom; it does not make "
            "every later instruction immediately ready or reproduce every feature of a physical processor."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(ch.heads), LaggedStart(*[FadeIn(r) for r in ch.rows], lag_ratio=0.04))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in ch.bars], lag_ratio=0.08), run_time=2.0)
            self.play(FadeIn(keys[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in ch.commits], lag_ratio=0.08), FadeIn(keys[1]))
            vo.wait_until("c")
            self.play(FadeIn(total))
        self.wait(0.3)
        self.clear_scene()




