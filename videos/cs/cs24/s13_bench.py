from __future__ import annotations

import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs24.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, load, mono)


class Benchmarking(VoiceoverScene):
    def construct(self):
        self.card()
        self.spread()
        self.traps()

    def card(self):
        card = chapter_card(12, r"Benchmarking honestly", r"How do you know your measurement is real?",
                            lit=(2009, 2013), extra=((2009, r"Mytkowicz et al."), (2013, r"Stabilizer")), part=PART)
        with self.voiceover("Chapter twelve. Benchmarking honestly."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def spread(self):
        b = load("bench")
        runs = b["runs"]
        head = label(r"The same program, \ thirty times", font_size=34).to_edge(UP, buff=0.3)
        lo, hi = 34.0, 56.0
        ax = NumberLine(x_range=[lo, hi, 2], length=10.0, color=GREY_D, include_numbers=False).move_to(UP * 0.6)
        ticks = VGroup(*[mono(f"{v:.0f}", 15, GREY_B).next_to(ax.n2p(v), DOWN, buff=0.12) for v in range(34, 57, 4)])
        ml = label(r"milliseconds", font_size=18, color=GREY_A).next_to(ticks, DOWN, buff=0.1)
        rng = random.Random(2)
        first = VGroup(*[Dot(ax.n2p(min(hi, r[0] * 1000)) + UP * (0.9 + 0.5 * rng.random()), radius=0.05, color=NO)
                         for r in runs])
        warm = VGroup(*[Dot(ax.n2p(min(hi, min(r[1:]) * 1000)) + UP * (0.15 + 0.5 * rng.random()), radius=0.05,
                            color=YES) for r in runs])
        kl = VGroup(label(r"first repetition, \ cold", font_size=18, color=NO),
                    label(r"best of the next five, \ warm", font_size=18, color=YES)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax, UP, buff=1.6).align_to(ax, LEFT)
        notes = VGroup(
            label(rf"cold runs average {b['first_mean'] * 1000:.1f} ms, \ warm {b['warm_mean'] * 1000:.1f} ms: \ "
                  r"caches, \ branch predictors, \ page faults and clock speed all warm up", font_size=21, color=NO),
            label(rf"warm runs still spread from {b['warm_min'] * 1000:.1f} to {b['warm_max'] * 1000:.1f} ms \ "
                  rf"(standard deviation {b['warm_sd'] * 1000:.1f} ms): \ report a distribution, \ not one number",
                  font_size=21, color=YES),
            label(r"compare medians with confidence intervals; \ repeat until the interval is small enough to decide",
                  font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Every number in this part came from a stopwatch, so it is fair to ask how far to trust them. <bookmark "
            "mark='a'/> Here is one small program run thirty times, timing the same loop six times inside each run. "
            "<bookmark mark='b'/> The first repetition is consistently slower, about a quarter, because the caches, "
            "the branch predictors and the page tables start cold, and the processor may still be raising its clock. "
            "Warm up before you measure. <bookmark mark='c'/> Even warm, the runs spread by more than ten percent. "
            "A single timing is an anecdote. Report the distribution, compare medians with confidence intervals, and "
            "keep repeating until the intervals are narrow enough to decide."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks), FadeIn(ml))
            vo.wait_until("a")
            self.play(FadeIn(kl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(dd) for dd in first], lag_ratio=0.03), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(dd) for dd in warm], lag_ratio=0.03), FadeIn(notes[1]), FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def traps(self):
        b = load("bench")
        pads = b["pads"]
        head = label(r"Two traps", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 4096, 1024], y_range=[30, 50, 5], x_length=6.0, y_length=3.0,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=1.0).shift(UP * 0.4)
        xt = VGroup(*[mono(str(v), 14, GREY_B).next_to(ax.c2p(v, 30), DOWN, buff=0.1) for v in range(0, 4097, 1024)])
        yt = VGroup(*[mono(str(v), 14, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in range(30, 51, 5)])
        xl = label(r"bytes of environment variables", font_size=18, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"median ms, \ 5 runs", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        pts = VGroup(*[Line(ax.c2p(p["pad"], p["min"] * 1000), ax.c2p(p["pad"], p["max"] * 1000), color=GREY_C,
                            stroke_width=1.5) for p in pads])
        med = VGroup(*[Dot(ax.c2p(p["pad"], p["median"] * 1000), radius=0.05, color=HEAD) for p in pads])
        code_ = VGroup(*[mono(t, 18, c) for t, c in (("s = 0;", WHITE), ("for (i = 1; i <= 1e8; i++)", WHITE),
                                                      ("    s += i * i % 7;", WHITE), ("// s never used", NO))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).to_edge(RIGHT, buff=0.9).shift(UP * 1.2)
        side = VGroup(
            label(rf"unused: \ {b['dead_s'] * 1e6:.0f} $\mu$s \ (the compiler deleted the loop)", font_size=20,
                  color=NO),
            label(rf"result kept: \ {b['live_s'] * 1000:.0f} ms", font_size=20, color=YES),
            label(r"benchmark libraries add a \texttt{DoNotOptimize} sink", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(code_, DOWN, buff=0.3).align_to(code_, LEFT)
        notes = VGroup(
            label(rf"\textbf{{layout bias}}: \ only the environment's size changed, \ and the median moved by up to "
                  rf"{(b['pad_spread'] - 1) * 100:.0f}\%", font_size=21, color=HEAD),
            label(r"Mytkowicz, \ Diwan, \ Hauswirth and Sweeney (2009): \ environment size and link order can flip "
                  r"a conclusion; \ Stabilizer (2013) randomizes layout", font_size=20, color=GREY_A),
            label(r"\textbf{dead code}: \ a benchmark whose result is unused may measure nothing at all", font_size=21,
                  color=NO),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Two traps catch experienced engineers. <bookmark mark='a'/> The first is layout. We ran the same "
            "binary with nothing changed except the size of its environment variables, which shifts where the stack "
            "begins. The median moved by up to twenty-two percent. On a shared cloud machine part of that is noise from "
            "neighbours, and that is the point: without randomized layouts and many repetitions, a change of that "
            "size cannot be told apart from luck. "
            "<bookmark mark='b'/> Todd Mytkowicz and colleagues showed in 2009 that such accidents, the environment's "
            "size and even the order of object files at link time, can turn a measured speedup into a slowdown. "
            "Charlie Curtsinger and Emery Berger's Stabilizer re-randomizes the layout during a run, so that "
            "differences can be tested statistically. <bookmark mark='c'/> The second trap is the optimizer. This "
            "loop's result is never used, so the compiler deleted it: a hundred million iterations in a "
            "microsecond. <bookmark mark='d'/> Keep the result, and the same loop takes a hundred and twenty "
            "milliseconds. A benchmark whose output is unused may be measuring nothing."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(pts), FadeIn(med),
                      FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(code_), FadeIn(side[0]), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()
