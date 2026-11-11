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
        card = chapter_card(2, r"Pipelining, \ like laundry", 'How can throughput rise without reducing latency?', part=PART)
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
            label('$t$: logic work; $o$: assumed register overhead (70 ps); equal stages, no stalls', font_size=22, color=GREY_A),
            label(r"each register adds $o$ to the latency, \ and the speedup approaches $k$ only while $t/k \gg o$",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Let one instruction's logic take time t, split into k equal stages. <bookmark mark='a'/> Assume each "
            "pipeline register adds overhead o, seventy picoseconds in this teaching model. The cycle is t over k plus "
            "o. <bookmark mark='b'/> One instruction's latency is k cycles: t plus k times o, so adding stages "
            "increases it. <bookmark mark='c'/> Ideal steady-state throughput improves by t plus o divided by t over k "
            "plus o, compared with the one-stage baseline. As k grows, this approaches one plus t over o, exactly the "
            "limit in the equation. It approaches k only while stage work greatly exceeds register overhead. Balanced "
            "stages and no stalls are essential assumptions."
        ) as vo:
            self.play(FadeIn(head))
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
            label(rf"assumed cycle: \ the slowest stage $+$ 70 ps \\ $=$ {fmt(st['period_ps'])} ps, \ "
                  rf"{st['mhz']:.0f} MHz", font_size=24, color=CLOCK),
            label(rf"Part 6's single cycle: \ {fmt(st['single_ps'])} ps", font_size=22, color=GREY_A),
            label(rf"so the clock is {st['clock_ratio']:.2f} times faster, \ not 5", font_size=26, color=HEAD),
            label(r"the memories set the pace; \ EX, \ with the whole ALU, \\ needs only "
                  rf"{st['stages']['EX']['ps']:.0f} ps \ (Part 9 attacks the memories)", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).shift(UP * 0.2)
        with self.voiceover(
            "Stages need not be equal. <bookmark mark='a'/> These bars are a teaching budget: assumed one-nanosecond "
            "memories, sampled unit-delay ALU settling, structural register-read depth, and estimated mux and control "
            "costs. They are not physical timing results for a fabricated pipeline. <bookmark mark='b'/> Under those "
            "assumptions, the slowest stage plus seventy picoseconds gives one point one three nanoseconds, about "
            "eight hundred and eighty-five megahertz. The assumed single-cycle budget is two point six three "
            "nanoseconds, so the clock ratio is about two point three, not five. <bookmark mark='c'/> The budget "
            "suggests memory is the bottleneck. A real implementation needs timing analysis, routing and memory "
            "characterization before claiming that clock."
        ) as vo:
            self.play(FadeIn(head))
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
        fl = label('$b$: fixed miss events per instruction; \\\\ assume each loses $k-1$ cycles',
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
        dot = Dot(ax.c2p(kstar, (d['L_ps'] / kstar + d['o_ps']) * (1 + d['b'] * (kstar - 1))), color=HEAD, radius=0.08)
        dl = label(rf"$k^* \approx {kstar:.0f}$", font_size=24, color=HEAD).next_to(dot, UP, buff=0.15)
        deriv = VGroup(
            MathTex(r"\frac{dT}{dk} = -\frac{t(1-b)}{k^2} + b\,o = 0", font_size=32, color=GREY_A),
            MathTex(r"k^* = \sqrt{\frac{t\,(1-b)}{b\,o}}", font_size=40, color=HEAD),
            label(rf"with $t = {d['L_ps']:.0f}$ ps, \ $o = {d['o_ps']:.0f}$ ps \\ and the Job's measured "
                  rf"$b = {d['b']:.3f}$:", font_size=22, color=GREY_A),
            MathTex(rf"k^* \approx {kstar:.0f}", font_size=40, color=YES),
            label('fixed $b$, equal splits, penalty $k-1$: \\\\ continuous model optimum, not a hardware design', font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.8 + DOWN * 0.75)
        with self.voiceover(
            "Deeper is not always better. <bookmark mark='a'/> Consider a deliberately simple model: equally "
            "splittable logic, fixed register overhead o, and a fixed fraction b of instructions each losing k minus "
            "one cycles. Time per instruction is the cycle multiplied by one plus b times k minus one. <bookmark "
            "mark='b'/> Holding b fixed produces this curve: short pipelines have long cycles; very deep ones pay "
            "overhead and larger flushes. Real predictors and stage balances can change with depth. <bookmark "
            "mark='c'/> Differentiating gives the displayed continuous optimum, about thirty-seven for these inputs. "
            "An integer design must compare nearby feasible depths. This is a model exercise, not an optimal hardware "
            "design or a prediction of Pentium 4's stage count."
        ) as vo:
            self.play(FadeIn(head))
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
