from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs10.common import (BG, CODE, CORE_COLORS, CTRL, DATA, FUNC, HEAD, NO, PART, YES, load, mono)


class FalseShare(VoiceoverScene):
    def construct(self):
        self.card()
        self.layout()
        self.measure()
        self.fixes()

    def card(self):
        card = chapter_card(4, r"False sharing", r"Can two cores slow each other down without sharing anything?",
                            part=PART)
        with self.voiceover("Chapter four. False sharing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def layout(self):
        head = label(r"Four counters, \ one per thread", font_size=34).to_edge(UP, buff=0.35)
        code = VGroup(mono("long count[4];                 // 32 bytes: one cache line", 20),
                      mono("// thread k, fifty million times:", 20, GREY_B),
                      mono("__atomic_fetch_add(&count[k], 1, __ATOMIC_RELAXED);", 20)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).next_to(head, DOWN, buff=0.35)
        line = VGroup()
        for k in range(8):
            c = CORE_COLORS[k] if k < 4 else GREY_D
            line.add(Rectangle(width=1.0, height=0.6, stroke_color=GREY_C, stroke_width=1.5, fill_color=c,
                               fill_opacity=0.35 if k < 4 else 0.05))
        line.arrange(RIGHT, buff=0).shift(DOWN * 0.4)
        labs = VGroup(*[Text(f"count[{k}]", font="DejaVu Sans Mono", font_size=14, color=WHITE).move_to(line[k])
                        for k in range(4)])
        br = Brace(line, DOWN, color=HEAD)
        bl = label(r"one 64-byte line: \ the unit coherence works in", font_size=20, color=HEAD).next_to(br, DOWN,
                                                                                                         buff=0.1)
        ping = label(r"every increment needs the line Modified \ $\to$ \ it bounces between the four caches",
                     font_size=22, color=NO).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is a trap that catches experienced programmers. Four threads each count something, in an array of "
            "four counters, one per thread. <bookmark mark='a'/> No two threads ever touch the same counter, so "
            "there is no real sharing at all. <bookmark mark='b'/> But coherence does not work in variables. It "
            "works in cache lines, and all four counters fit in one sixty-four-byte line. <bookmark mark='c'/> To "
            "increment its counter, a core needs that line in the Modified state, which means taking it away from "
            "whichever core had it last. The line bounces from cache to cache, fifty million times per thread. "
            "This is false sharing: the hardware sees sharing where the program has none."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code))
            vo.wait_until("a")
            self.play(FadeIn(line), FadeIn(labs))
            vo.wait_until("b")
            self.play(GrowFromCenter(br), FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeIn(ping))
            for k in (1, 2, 3, 0):
                self.play(Indicate(line[k], color=CORE_COLORS[k], scale_factor=1.15), run_time=0.4)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measure(self):
        fs = load("falseshare")["rows"]
        head = label(r"Measured on this computer", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0.5, 4.5, 1], y_range=[0, 90, 20], x_length=7.5, y_length=4.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).shift(DOWN * 0.3 + LEFT * 1.0)
        xt = VGroup(*[label(rf"{n}", font_size=18, color=GREY_B).next_to(ax.c2p(n, 0), DOWN, buff=0.12)
                      for n in (1, 2, 3, 4)])
        yt = VGroup(*[label(rf"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(0.5, v), LEFT, buff=0.1)
                      for v in (0, 20, 40, 60, 80)])
        xl = label(r"threads", font_size=18, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.45)
        yl = label(r"nanoseconds per increment", font_size=18, color=GREY_B).next_to(ax, UP, buff=0.15).align_to(
            ax, LEFT)
        same = VMobject(color=NO, stroke_width=4).set_points_as_corners([ax.c2p(r["threads"], r["same"]) for r in fs])
        pad = VMobject(color=YES, stroke_width=4).set_points_as_corners([ax.c2p(r["threads"], r["padded"])
                                                                         for r in fs])
        sd = VGroup(*[Dot(ax.c2p(r["threads"], r["same"]), color=NO, radius=0.07) for r in fs])
        pd = VGroup(*[Dot(ax.c2p(r["threads"], r["padded"]), color=YES, radius=0.07) for r in fs])
        ls = label(r"counters in one line", font_size=20, color=NO).next_to(ax.c2p(4, fs[3]["same"]), RIGHT, buff=0.15)
        lp = label(r"a line each \ (padded to 64 bytes)", font_size=20, color=YES).next_to(
            ax.c2p(4, fs[3]["padded"]), RIGHT, buff=0.15).shift(UP * 0.25)
        r4 = fs[3]["same"] / fs[3]["padded"]
        punch = label(rf"four threads: \ {fs[3]['same']:.0f} ns against {fs[3]['padded']:.1f} ns, \ {r4:.0f} times "
                      r"slower, \ for nothing", font_size=24, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here it is, measured on this computer. Each thread increments its own counter fifty million times, and "
            "we time one increment. <bookmark mark='a'/> One thread alone: about seven nanoseconds, the cost of an "
            "atomic add on a line the core already owns. <bookmark mark='b'/> Give each counter a line of its own, "
            "by padding it to sixty-four bytes, and the time stays flat however many threads run: there is no "
            "sharing, so there is no traffic. <bookmark mark='c'/> Put the four counters in one line, and every "
            f"increment waits for the line to arrive from another core. With four threads, each increment takes "
            f"{fs[3]['same']:.0f} nanoseconds, {r4:.0f} times longer, though no thread ever reads another's counter."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(sd[0]), FadeIn(pd[0]))
            vo.wait_until("b")
            self.play(Create(pad), FadeIn(pd), FadeIn(lp))
            vo.wait_until("c")
            self.play(Create(same), FadeIn(sd), FadeIn(ls))
            self.play(FadeIn(punch))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fixes(self):
        head = label(r"Finding it, \ and fixing it", font_size=34).to_edge(UP, buff=0.35)
        pts = VGroup(
            mono("struct alignas(64) counter { long n; };    // C++: a line each", 19),
            label(r"pad or align per-thread data to the line size \ (C++17: "
                  r"\texttt{std::hardware\_destructive\_interference\_size})", font_size=21, color=GREY_A),
            label(r"better: \ let each thread count in a local variable, \ and add it in once at the end", font_size=21,
                  color=YES),
            label(r"that is what the Job does: \ private tables, \ combined once", font_size=21, color=YES),
            label(r"finding it: \ \texttt{perf c2c} reports lines that bounce between cores, \ and who touches them",
                  font_size=21, color=DATA),
            label(r"in the wild: \ statistics counters, \ locks packed next to the data they guard, \ arrays of "
                  r"per-thread structs", font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.1)
        with self.voiceover(
            "The fixes are simple once you know. <bookmark mark='a'/> Align or pad each thread's data to a whole cache "
            "line. <bookmark mark='b'/> C++ even has a name for the size to pad to. <bookmark mark='c'/> Better "
            "still, keep per-thread work in local variables, which live in registers or in lines no one else touches, "
            "and combine them once at the end. <bookmark mark='d'/> That is exactly the Job's design: four private "
            "tables, combined once. <bookmark mark='e'/> To find false sharing in a real program, Linux's perf tool "
            "has a mode, c2c, for cache to cache, that reports which lines bounce between cores and which "
            "instructions touch them. <bookmark mark='f'/> The usual culprits are statistics counters, a lock "
            "stored next to the data it protects, and arrays of small per-thread structures."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcdef", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
