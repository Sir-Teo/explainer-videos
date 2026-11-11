from __future__ import annotations

import random
import statistics

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
        samples=[r[0]*1000 for r in runs]+[statistics.median(r[1:])*1000 for r in runs]
        step=max(1,math.ceil((max(samples)-min(samples))/8))
        lo=math.floor(min(samples)/step)*step-step;hi=math.ceil(max(samples)/step)*step+step
        ax = NumberLine(x_range=[lo, hi, step], length=11.0, color=GREY_D, include_numbers=False).move_to(UP * 0.6)
        ticks = VGroup(*[mono(f"{v:.0f}", 15, GREY_B).next_to(ax.n2p(v), DOWN, buff=0.12) for v in range(lo,hi+1,step)])
        ml = label(r"milliseconds", font_size=18, color=GREY_A).next_to(ticks, DOWN, buff=0.1)
        rng = random.Random(2)
        first = VGroup(*[Dot(ax.n2p(r[0] * 1000) + UP * (0.9 + 0.5 * rng.random()), radius=0.05, color=NO)
                         for r in runs])
        warm = VGroup(*[Dot(ax.n2p(statistics.median(r[1:]) * 1000) + UP * (0.15 + 0.5 * rng.random()), radius=0.05,
                            color=YES) for r in runs])
        kl = VGroup(label(r"first observation", font_size=18, color=NO),
                    label(r"median of the later five", font_size=18, color=YES)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax, UP, buff=1.6).align_to(ax, LEFT)
        notes = VGroup(
            label('first versus later median: matched summaries; causes are not isolated', font_size=21, color=NO),
            label('all thirty processes retained; plot includes every current observation',
                  font_size=21, color=YES),
            label('predefine the sample plan; interleave variants; report sampling uncertainty',
                  font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            'The benchmark demonstration records thirty process runs, with six observations in each. <bookmark '
            "mark='a'/> We retain every observation and compare the first with the median of the later five, so "
            "a single sample is not compared with a selected minimum. <bookmark mark='b'/> Any "
            'first-versus-later difference can have several causes. These clocks alone do not establish a '
            "cold-cache effect or a particular change in processor frequency. <bookmark mark='c'/> The plot uses "
            'an axis that contains all current observations. For a controlled comparison, choose a sample plan '
            'in advance, randomize or interleave variants, and report uncertainty and the sampling unit. '
            'Repeating until a preferred confidence interval appears requires a valid sequential procedure; '
            'ordinary fixed-sample intervals do not justify optional stopping.'
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
        low=min(p['min']*1000 for p in pads);high=max(p['max']*1000 for p in pads)
        step=max(1,math.ceil((high-low)/5));ylo=math.floor(low/step)*step-step;yhi=math.ceil(high/step)*step+step
        ax = Axes(x_range=[0, 4096, 1024], y_range=[ylo, yhi, step], x_length=6.0, y_length=3.0,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=1.0).shift(UP * 0.4)
        xt = VGroup(*[mono(str(v), 14, GREY_B).next_to(ax.c2p(v, ylo), DOWN, buff=0.1) for v in range(0, 4097, 1024)])
        yt = VGroup(*[mono(str(v), 14, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in range(ylo,yhi+1,step)])
        xl = label(r"bytes of environment variables", font_size=18, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"ms: \ median of 5 runs, \ and the range", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
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
            label('observed spread with shuffled PAD sizes; shared-host and ASLR effects remain', font_size=21, color=HEAD),
            label(r"Mytkowicz, \ Diwan, \ Hauswirth and Sweeney (2009): \ environment size and link order can flip "
                  r"a conclusion; \ Stabilizer (2013) randomizes layout", font_size=20, color=GREY_A),
            label(r"\textbf{dead code}: \ a benchmark whose result is unused may measure nothing at all", font_size=21,
                  color=NO),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Two traps illustrate why controls matter. <bookmark mark='a'/> We vary an environment variable's "
            'size with a fixed, shuffled execution schedule, retaining five process runs per size. The observed '
            'spread also includes shared-host variation and uncontrolled address randomization, so it does not '
            "isolate a causal layout effect. <bookmark mark='b'/> Mytkowicz and colleagues studied measurement "
            "bias from layout choices. Curtsinger and Berger's Stabilizer samples layouts during execution; our "
            "small demonstration does not reproduce that system. <bookmark mark='c'/> The second trap is "
            'dead-code elimination. The unused loop has no observable result; inspect the retained assembly '
            "alongside its clock interval. <bookmark mark='d'/> The kept version has an independently checked "
            'exact sum. Its measured time is shown rather than quoted from an earlier host. A benchmark needs '
            'both observable work and a correctness check.'
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
