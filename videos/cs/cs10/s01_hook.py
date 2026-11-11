from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs10.common import (BG, CLOCK, CODE, CORE_COLORS, COST, CTRL, DATA, FUNC, HEAD, NO, PART, YES,
                                   core_box, load)

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
            (
            "Here are fifty years of microprocessors, each dot one chip, on a logarithmic scale. <bookmark "
            "mark='a'/> Across this historical sample, transistor counts rise roughly exponentially. Moore "
            "described a manufacturing trend, not a physical law or a promise for every chip. <bookmark "
            "mark='b'/> The speed of a single thread followed it for thirty years. <bookmark mark='c'/> So did "
            "the clock: from under a megahertz to over three gigahertz, roughly a third faster per year in the "
            "fitted 1985 to 2004 sample. <bookmark mark='d'/> And power rose with them, to about a hundred watts. "
            "<bookmark mark='e'/> Then, around 2005, three of the curves bent. Clock growth slowed sharply in the "
            "later sample. Power budgets constrained further scaling, while single-thread performance continued "
            "improving more slowly. <bookmark mark='f'/> And a new curve appeared: the number of cores. The "
            "transistors kept coming, and designers increasingly spent them on more cores, larger caches and "
            "specialized units."
        )
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
        head = label(r"The Job, \ on more than one core", font_size=36).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(rf"Part 8 fitted one-core baseline: \ {sp['one']['seconds']:.1f} seconds for thirty novels", font_size=26,
                  color=GREY_A),
            label(r"four cores: \ word-aligned text shards, \ private tables, \ then merge", font_size=25,
                  color=DATA),
            label(r"the obvious way to combine them \ throws away much of the gain", font_size=27, color=NO),
            label(rf"conditional compute-cost model: \ {four['speedup']['partitioned']:.1f} times faster \ on 4 cores", font_size=27,
                  color=YES),
            label(r"how can four cores be more than four times faster?", font_size=27, color=HEAD),
        )
        for line, y in zip(lines, (2.65, 1.9, -1.45, -2.15, -2.9)):
            line.move_to(UP * y)
        baseline = Rectangle(width=10.2, height=0.1, stroke_width=0, fill_color=GREY_B,
                             fill_opacity=0.6).move_to(UP * 2.25)
        shards, cores, tables, links = VGroup(), VGroup(), VGroup(), VGroup()
        for k, x in enumerate((-4.2, -1.4, 1.4, 4.2)):
            color = CORE_COLORS[k]
            piece = Rectangle(width=2.65, height=0.23, stroke_color=color, fill_color=color,
                              fill_opacity=0.55).move_to([x, 1.25, 0])
            core = core_box(k, w=2.0, h=0.65, font_size=20).move_to([x, 0.45, 0])
            rows = VGroup(*[Rectangle(width=1.6, height=0.18, stroke_color=color, stroke_width=1.2,
                                      fill_color=color, fill_opacity=0.12) for _ in range(3)]).arrange(DOWN, buff=0)
            rows.move_to([x, -0.5, 0])
            tag = label(r"private table", font_size=16, color=color).next_to(rows, DOWN, buff=0.1)
            shards.add(piece); cores.add(core); tables.add(VGroup(rows, tag))
            links.add(Arrow(piece.get_bottom(), core.get_top(), buff=0.04, color=color, stroke_width=2),
                      Arrow(core.get_bottom(), rows.get_top(), buff=0.04, color=color, stroke_width=2))
        with self.voiceover(
            (
            "And the Job. <bookmark mark='a'/> On one of Part 8's out-of-order cores, the fitted corpus model "
            "projects about fifty-seven seconds to count thirty novels. Part 9 added a conditional memory "
            "estimate, not a physical multicore measurement. <bookmark mark='b'/> With four cores, the plan is "
            "simple: give each core a word-aligned quarter of the text, let each count its own, and combine the "
            "four sets of counts. <bookmark mark='c'/> The obvious way of combining them throws away much of what "
            "the cores gained. <bookmark mark='d'/> With partitioned merging, the cost model projects nearly five "
            "times the one-core speed. <bookmark mark='e'/> More than four times faster, on four cores. By the "
            "end of this part you will know how changing the total work produces that apparent superlinear gain, "
            "and which costs the projection leaves out."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]), FadeIn(baseline), run_time=0.65)
            for mk, l in zip("abcde", lines):
                vo.wait_until(mk)
                if mk == "a":
                    self.play(Indicate(baseline, color=HEAD), run_time=0.5)
                elif mk == "b":
                    self.play(FadeIn(l), FadeIn(shards), FadeIn(cores), FadeIn(tables), Create(links), run_time=1.0)
                else:
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
            "Here is the route from hardware limits to correct parallel programs. <bookmark mark='a'/> First, the power wall and why rapid clock scaling slowed. <bookmark mark='b'/> Then shared memory: a coherence protocol simulated step by step, followed by host measurements of false sharing and store buffering. <bookmark mark='c'/> Next, SIMD inside a core and the throughput-oriented GPU. <bookmark mark='d'/> Then the theory: work and span, a scheduling bound, scans and sorting networks. <bookmark mark='e'/> Finally, the Job on four cores: a conditional model and a separate compiled host experiment, with their costs kept explicit."
        ) as vo:
            self.play(FadeIn(head), run_time=0.5)
            for mk, f in zip('abcde', facts):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(f, shift=UP * 0.1), run_time=0.6 if mk == 'a' else 1.0)
                if mk == 'a':
                    vo.wait_until(mk)
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
