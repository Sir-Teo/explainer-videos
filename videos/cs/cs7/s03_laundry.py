from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, STAGE_COLOR, STAGES,
                                  YES, box, fmt, laundry_strip, load)


class Laundry(VoiceoverScene):
    def construct(self):
        self.card()
        self.laundry()
        self.formulas()
        self.unbalanced()
        self.depth()

    def card(self):
        card = chapter_card(2, r"Pipelining, \ like laundry", r"How can every instruction finish sooner without any "
                            r"getting faster?", part=PART)
        with self.voiceover("Chapter two. Pipelining, like laundry."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def laundry(self):
        head = label(r"Four loads of laundry", font_size=38).to_edge(UP, buff=0.35)
        seq = laundry_strip(4, pipelined=False, w=0.62, h=0.42).move_to(UP * 1.2, aligned_edge=LEFT).to_edge(LEFT,
                                                                                                         buff=0.8)
        pip = laundry_strip(4, pipelined=True, w=0.62, h=0.42).to_edge(LEFT, buff=0.8).shift(DOWN * 1.4)
        sl = label(r"one at a time: \ 16 hours", font_size=24, color=NO).next_to(seq, RIGHT, buff=0.3).shift(UP * 0.4)
        pl = label(r"overlapped: \ 7 hours", font_size=24, color=YES).next_to(pip, RIGHT, buff=0.3).shift(UP * 0.4)
        each = label(r"each load still takes 4 hours: \ \textit{latency} unchanged; \\ a load finishes every hour: "
                     r"\ \textit{throughput} four times higher", font_size=24, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Patterson and Hennessy's textbook pictures pipelining as a laundry. <bookmark mark='a'/> Each load needs four steps, "
            "say an hour each: wash, dry, fold and put away. Done one load at a time, four loads take sixteen hours. "
            "<bookmark mark='b'/> But the washer is free as soon as the first load moves to the dryer. Start the "
            "second load then, and the third an hour later, and four loads are finished in seven hours. "
            "<bookmark mark='c'/> Notice what did not change: each load still takes four hours from dirty to put away. "
            "The time for one job, the latency, is the same. What improved is the throughput, the number of jobs "
            "finished per hour, which in the steady state is four times higher. A processor does not need any single "
            "instruction to finish sooner; it needs many of them to finish per second."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in seq], lag_ratio=0.05), run_time=2.5)
            self.play(FadeIn(sl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in pip], lag_ratio=0.05), run_time=2.5)
            self.play(FadeIn(pl))
            vo.wait_until("c")
            self.play(FadeIn(each))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def formulas(self):
        head = label(r"$k$ stages, \ and the cost of a register", font_size=36).to_edge(UP, buff=0.35)
        f = VGroup(
            MathTex(r"t_{\text{cycle}} = \frac{t}{k} + o", font_size=40, color=CLOCK),
            MathTex(r"\text{latency} = k\left(\frac{t}{k} + o\right) = t + k\,o", font_size=40, color=NO),
            MathTex(r"\text{speedup} = \frac{t + o}{t/k + o} \ \xrightarrow{\ k \to \infty\ } \ \frac{t + o}{o}",
                    font_size=40, color=YES),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.3)
        notes = VGroup(
            label(r"$t$: \ the work of one instruction; \ $o$: \ a pipeline register's overhead \ (setup and "
                  r"clock-to-Q, \ 70 ps)", font_size=22, color=GREY_A),
            label(r"each register adds $o$ to the latency, \ and the speedup approaches $k$ only while $t/k \gg o$",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In a processor the steps are stages of logic. Suppose one instruction's work takes time t, and we cut it "
            "into k equal stages. <bookmark mark='a'/> Each stage then takes t over k, plus a fixed overhead o for the "
            "pipeline register at its end: the setup and clock-to-Q times of Part 5, seventy picoseconds here. That is "
            "the cycle. <bookmark mark='b'/> The latency of one instruction grows: k cycles, so t plus k times o. "
            "<bookmark mark='c'/> But one instruction finishes per cycle, so the speedup over doing it all in one "
            "cycle is t plus o, over t over k plus o. It approaches k while the stages are long compared with the "
            "overhead, and it can never exceed t over o, however many stages you cut: the registers themselves become "
            "the bottleneck."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f[0]))
            vo.wait_until("b")
            self.play(Write(f[1]))
            vo.wait_until("c")
            self.play(Write(f[2]))
            self.play(FadeIn(notes))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def unbalanced(self):
        st = load("stages")
        head = label(r"Pebble's five stages are not equal", font_size=36).to_edge(UP, buff=0.35)
        scale = 4.0 / max(v["ps"] for v in st["stages"].values())
        bars = VGroup()
        for k, s in enumerate(STAGES):
            v = st["stages"][s]
            h = v["ps"] * scale
            r = Rectangle(width=1.1, height=h, stroke_width=0, fill_color=STAGE_COLOR[s], fill_opacity=0.65)
            r.move_to([-4.6 + 1.6 * k, -2.0 + h / 2, 0])
            nm = label(s, font_size=26, color=STAGE_COLOR[s]).next_to(r, DOWN, buff=0.15)
            ps = label(rf"{fmt(v['ps'])} ps", font_size=20, color=GREY_A).next_to(r, UP, buff=0.1)
            bars.add(VGroup(r, nm, ps))
        line = DashedLine([-5.4, -2.0 + max(v["ps"] for v in st["stages"].values()) * scale, 0],
                          [2.5, -2.0 + max(v["ps"] for v in st["stages"].values()) * scale, 0], color=NO,
                          stroke_width=2)
        notes = VGroup(
            label(rf"the cycle: \ the slowest stage $+$ 70 ps \\ $=$ {fmt(st['period_ps'])} ps, \ "
                  rf"{st['mhz']:.0f} MHz", font_size=24, color=CLOCK),
            label(rf"Part 6's single cycle: \ {fmt(st['single_ps'])} ps", font_size=22, color=GREY_A),
            label(rf"so the clock is {st['clock_ratio']:.2f} times faster, \ not 5", font_size=26, color=HEAD),
            label(r"the memories set the pace; \ EX, \ with the whole ALU, \\ needs only "
                  rf"{st['stages']['EX']['ps']:.0f} ps \ (Part 9 attacks the memories)", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).shift(UP * 0.2)
        with self.voiceover(
            "Real stages are never equal, and the clock must wait for the slowest. <bookmark mark='a'/> Here are "
            "Pebble's five, timed with the gate delays of Part 5 and the netlists of Parts 4 and 6. Fetch and the data "
            "memory stage each contain a one-nanosecond memory access. Decode and register read take about a hundred "
            "picoseconds; the ALU stage, with Part 4's whole prefix adder, three hundred and fifty; write-back almost "
            "nothing. <bookmark mark='b'/> So the cycle is the memory stage plus the register overhead: one point one "
            "three nanoseconds, eight hundred and eighty-five megahertz. Against Part 6's two point six three, the "
            "clock is two point three times faster, not five. <bookmark mark='c'/> The ALU stage could do three times "
            "as much work in the time it is given. Balancing a pipeline means cutting where the time is, and here the "
            "time is in the memories, which is why Part 9's caches matter so much."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.2),
                      *[FadeIn(b[1]) for b in bars], run_time=2.0)
            self.play(*[FadeIn(b[2]) for b in bars])
            vo.wait_until("b")
            self.play(Create(line), FadeIn(notes[0]), FadeIn(notes[1]))
            self.play(FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(Indicate(bars[2], color=YES), FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def depth(self):
        d = load("depth")
        head = label(r"How many stages?", font_size=38).to_edge(UP, buff=0.3)
        f = MathTex(r"T(k) = \left(\frac{t}{k} + o\right)\bigl(1 + b\,(k - 1)\bigr)", font_size=36,
                    color=CODE).move_to(UP * 2.2 + LEFT * 2.6)
        fl = label(r"$b$: \ the fraction of instructions that waste the whole pipeline \\ (mispredicted branches)",
                   font_size=20, color=GREY_A).next_to(f, DOWN, buff=0.15).align_to(f, LEFT)
        ks = np.array(d["k"])
        ts = np.array(d["time_ps"])
        ax = Axes(x_range=[0, 80, 10], y_range=[0, 900, 300], x_length=6.0, y_length=3.4, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18, "include_numbers": True}).move_to(LEFT * 2.4 +
                                                                                                  DOWN * 1.2)
        xl = note(r"stages $k$", font_size=20).next_to(ax, DOWN, buff=0.3)
        yl = note(r"ps per instruction", font_size=20).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        curve = VMobject(color=YES, stroke_width=3).set_points_as_corners([ax.c2p(k, min(t, 900)) for k, t in
                                                                           zip(ks, ts)])
        kstar = d["kstar"]
        dot = Dot(ax.c2p(kstar, d["t_at_kstar"]), color=HEAD, radius=0.08)
        dl = label(rf"$k^* \approx {kstar:.0f}$", font_size=24, color=HEAD).next_to(dot, UP, buff=0.15)
        deriv = VGroup(
            MathTex(r"\frac{dT}{dk} = -\frac{t(1-b)}{k^2} + b\,o = 0", font_size=32, color=GREY_A),
            MathTex(r"k^* = \sqrt{\frac{t\,(1-b)}{b\,o}}", font_size=40, color=HEAD),
            label(rf"with $t = {d['L_ps']:.0f}$ ps, \ $o = {d['o_ps']:.0f}$ ps \\ and the Job's measured "
                  rf"$b = {d['b']:.3f}$:", font_size=22, color=GREY_A),
            MathTex(rf"k^* \approx {kstar:.0f}", font_size=40, color=YES),
            label(r"fewer if hazards are more common, \\ more if registers are cheaper", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.8 + DOWN * 0.75)
        with self.voiceover(
            "So why not cut the work into a hundred stages? Because deeper pipelines lose more when they guess wrong. "
            "<bookmark mark='a'/> A mispredicted branch throws away everything fetched behind it, roughly one "
            "instruction per stage. If a fraction b of instructions cause that, the time per instruction is the cycle, "
            "t over k plus o, times one plus b times k minus one. <bookmark mark='b'/> Plot it with this part's "
            "numbers. Few stages: the cycle is long. Many stages: the overhead and the flushes dominate. In between, a "
            "minimum. <bookmark mark='c'/> Set the derivative to zero and the best depth comes out as the square root "
            "of t times one minus b, over b times o. With Pebble's work per instruction, its register overhead, and "
            "the misprediction rate measured on the Job, the optimum is about "
            "thirty-seven stages, if the work could be cut that finely. Hold on to that number: in 2004 Intel shipped "
            "a processor with thirty-one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(curve), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(deriv[0]))
            self.play(FadeIn(deriv[1]))
            self.play(FadeIn(deriv[2]), FadeIn(deriv[3]), FadeIn(dot), FadeIn(dl))
            self.play(FadeIn(deriv[4]))
        self.wait(0.3)
        self.clear_scene()
