from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs10.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, NO, PART, YES, load)

SERIES = [("transistors", r"transistors \ (thousands)", DATA), ("specint", r"single-thread performance", YES),
          ("frequency", r"clock \ (MHz)", NO), ("watts", r"power \ (watts)", CTRL), ("cores", r"cores", FUNC)]


def trend_axes(x_length=10.5, y_length=4.6):
    ax = Axes(x_range=[1970, 2022, 10], y_range=[0, 7.4, 1], x_length=x_length, y_length=y_length, tips=False,
              axis_config={"color": GREY_C, "font_size": 16})
    xt = VGroup(*[label(str(y), font_size=16, color=GREY_B).next_to(ax.c2p(y, 0), DOWN, buff=0.12)
                  for y in range(1970, 2021, 10)])
    yt = VGroup(*[label(rf"$10^{{{k}}}$", font_size=16, color=GREY_B).next_to(ax.c2p(1970, k), LEFT, buff=0.12)
                  for k in range(0, 8)])
    return ax, xt, yt


def trend_dots(ax, pts, color, r=0.035):
    return VGroup(*[Dot(ax.c2p(x, np.log10(max(y, 1))), radius=r, color=color, fill_opacity=0.85) for x, y in pts])


class Hook(VoiceoverScene):
    def construct(self):
        self.trends()
        self.job()
        self.preview()
        self.plan()

    # ------------------------------------------------------------------
    def trends(self):
        tr = load("trends")
        head = label(r"Fifty years of microprocessors", font_size=36).to_edge(UP, buff=0.3)
        ax, xt, yt = trend_axes()
        ax.shift(DOWN * 0.35)
        xt.shift(DOWN * 0.35)
        yt.shift(DOWN * 0.35)
        dots = {k: trend_dots(ax, tr["series"][k], c) for k, _, c in SERIES}
        legend = VGroup(*[VGroup(Dot(radius=0.06, color=c), label(t, font_size=17, color=c)).arrange(RIGHT, buff=0.1)
                          for _, t, c in SERIES]).arrange(RIGHT, buff=0.35).next_to(head, DOWN, buff=0.2)
        src = note(r"data: \ Karl Rupp's compilation \ (CC BY 4.0), \ after Horowitz, \ Labonte, \ Shacham, \ "
                   r"Olukotun, \ Hammond and Batten", font_size=15).to_edge(DOWN, buff=0.12)
        x05 = ax.c2p(2005, 0)[0]
        mark = DashedLine([x05, ax.c2p(0, 0)[1], 0], [x05, ax.c2p(0, 7.2)[1], 0], color=HEAD, stroke_width=2)
        mlab = label(r"2005", font_size=20, color=HEAD).next_to(mark, UP, buff=0.05)
        g = tr["clock_growth"]
        rate = label(rf"clock: \ +{100 * g['1985-2004']:.0f}\% a year to 2004, \ then {100 * g['2006-2021']:+.1f}\%",
                     font_size=22, color=NO).move_to(ax.c2p(1990, 6.6))
        with self.voiceover(
            "Here are fifty years of microprocessors, each dot one chip, on a logarithmic scale. <bookmark mark='a'/> "
            "The number of transistors on a chip doubled about every two years, as Gordon Moore predicted, and it "
            "still does. <bookmark mark='b'/> The speed of a single thread followed it for thirty years. <bookmark "
            "mark='c'/> So did the clock: from under a megahertz to over three gigahertz, a third faster every year. "
            "<bookmark mark='d'/> And power rose with them, to about a hundred watts. <bookmark mark='e'/> Then, "
            "around 2005, three of the curves bent. The clock stopped: since then it has not grown at all. Power hit a "
            "ceiling. Single-thread speed slowed to a crawl. <bookmark mark='f'/> And a new curve appeared: the number "
            "of cores. The transistors kept coming, and the only way left to use them was more processors on each "
            "chip."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(src))
            for mk, (k, _, c) in zip("abcd", SERIES[:4]):
                vo.wait_until(mk)
                self.play(FadeIn(legend[[s[0] for s in SERIES].index(k)]),
                          LaggedStart(*[FadeIn(d) for d in dots[k]], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("e")
            self.play(Create(mark), FadeIn(mlab))
            self.play(FadeIn(rate))
            vo.wait_until("f")
            self.play(FadeIn(legend[4]), LaggedStart(*[FadeIn(d) for d in dots["cores"]], lag_ratio=0.02),
                      run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def job(self):
        sp = load("split")
        four = next(r for r in sp["rows"] if r["p"] == 4)
        led = sp["ledger"]
        head = label(r"The Job, \ on more than one core", font_size=36).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(rf"one out-of-order Pebble core: \ {led[3]['seconds']:.1f} seconds for thirty novels", font_size=27,
                  color=GREY_A),
            label(r"four cores: \ split the books four ways, \ count, \ and combine the counts", font_size=27,
                  color=DATA),
            label(r"the obvious way to combine them \ throws away much of the gain", font_size=27, color=NO),
            label(rf"done well: \ {four['speedup']['partitioned']:.1f} times faster \ on 4 cores", font_size=30,
                  color=YES),
            label(r"how can four cores be more than four times faster?", font_size=27, color=HEAD),
        ).arrange(DOWN, buff=0.4).move_to(DOWN * 0.1)
        with self.voiceover(
            "And the Job. <bookmark mark='a'/> On one of Part 8's out-of-order cores, with Part 9's real caches, "
            "counting the words of thirty novels takes fifty-seven seconds. <bookmark mark='b'/> With four cores, the "
            "plan is simple: give each core a quarter of the books, let each count its own, and combine the four sets "
            "of counts. <bookmark mark='c'/> The obvious way of combining them throws away much of what the cores "
            "gained. <bookmark mark='d'/> Done well, the four cores finish nearly five times faster than one. "
            "<bookmark mark='e'/> More than four times faster, on four cores. By the end of this part you will know "
            "how that is possible, and why it is a warning as much as a triumph."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def preview(self):
        head = label(r"By the end of this part", font_size=40).to_edge(UP, buff=0.4)
        facts = VGroup(
            label(r"why the clock stopped: \ the power wall", font_size=27, color=NO),
            label(r"caches that agree, \ and memory that reorders: \ measured on this machine", font_size=27,
                  color=DATA),
            label(r"vectors and GPUs: \ one instruction, \ many data", font_size=27, color=CTRL),
            label(r"the theory: \ work, \ span, \ Brent's theorem, \ scans, \ sorting networks", font_size=27,
                  color=HEAD),
            label(r"the Job on four cores: \ ledger row 4", font_size=27, color=COST),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is where this part goes. <bookmark mark='a'/> Why the clock stopped: the physics of the power wall. "
            "<bookmark mark='b'/> What goes wrong when several cores share memory: caches that must be kept in "
            "agreement, and memory operations that appear out of order, with both effects measured on this computer. "
            "<bookmark mark='c'/> Parallelism inside one core: vector instructions, and the graphics processor. "
            "<bookmark mark='d'/> The theory: work and span, Brent's theorem, the parallel prefix that Part 4's adder "
            "already used, and networks that sort. <bookmark mark='e'/> And the Job on four cores, for the ledger's "
            "next row."
        ) as vo:
            self.play(FadeIn(head))
            for mk, f in zip("abcde", facts):
                vo.wait_until(mk)
                self.play(FadeIn(f, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Parallel Machines", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"the power wall; \ multicore and shared memory",
            r"cache coherence: \ MESI; \ false sharing",
            r"memory consistency: \ store buffers, \ litmus tests, \ fences; \ atomic instructions",
            r"SIMD and vectors; \ GPUs, \ warps and divergence",
            r"work and span; \ Brent's theorem; \ parallel prefix; \ sorting networks",
            r"Amdahl and Gustafson; \ PRAM, \ BSP, \ networks; \ the Job, \ ledger row 4",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 10 of Computer Science, Built, the last part of Act Two, Making It Fast. <bookmark "
            "mark='a'/> In this part: the power wall, and the multicore chips it forced. Cache coherence, the MESI "
            "protocol, and false sharing. Memory consistency: store buffers, litmus tests and fences, and the atomic "
            "instructions that locks are built from. Vector instructions, and graphics processors. The theory of "
            "parallel algorithms: work and span, Brent's theorem, parallel prefix and sorting networks. Amdahl's law "
            "and Gustafson's answer, the models of parallel computers and the networks inside supercomputers. And "
            "the Job, on four cores."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.4)
        self.clear_scene()
