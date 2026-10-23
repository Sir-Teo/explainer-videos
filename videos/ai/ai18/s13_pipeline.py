from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.common import (BWD, COMM, F, FWD, GPU, PART, WGT, fill_gantt, gantt, load, take_away)


class Pipeline(VoiceoverScene):
    def construct(self):
        self.card()
        self.gpipe()
        self.bubble()
        self.one_f_one_b()
        self.better()

    def card(self):
        card = chapter_card(12, r"Pipeline parallelism", r"Cut the model into stages: \ how much time is lost "
                            r"waiting?", part=PART)
        with self.voiceover("Chapter twelve. Pipeline parallelism."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def _chart(self, name, y=0.2, width=11.0):
        Pp = load("pipeline")
        r = Pp[name]
        g = gantt(r["ops"], Pp["p"], r["total"], width=width, row_h=0.46)
        g.move_to([0.4, y, 0])
        return g, r

    def _key(self, split=False):
        items = [(FWD, r"forward"), (BWD, r"backward" if not split else r"backward, input"), ]
        if split:
            items.append((WGT, r"backward, weights"))
        k = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=c, fill_opacity=0.95),
                            label(t, font_size=18, color=c)).arrange(RIGHT, buff=0.1) for c, t in items])
        return k.arrange(RIGHT, buff=0.5)

    # ------------------------------------------------------------------
    def gpipe(self):
        Pp = load("pipeline")
        p, m = Pp["p"], Pp["m"]
        stages = VGroup()
        for s in range(p):
            box = RoundedRectangle(width=2.2, height=0.9, corner_radius=0.1, stroke_color=GPU, stroke_width=2)
            t = label(rf"GPU {s}: \ layers ${8 * s + 1}$--${8 * s + 8}$", font_size=18, color=GPU).move_to(box)
            stages.add(VGroup(box, t))
        stages.arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.5)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, color=GREY_B, stroke_width=2.5)
                          for a, b in zip(stages, stages[1:])])
        sch = note(r"schematic: \ a $32$-layer model on $4$ GPUs", font_size=18).next_to(stages, DOWN, buff=0.12)
        g, r = self._chart("gpipe", y=-1.2)
        key = self._key().next_to(g, DOWN, buff=0.3)
        tl = label(rf"GPipe: \ ${m}$ micro-batches, \ all forward, \ then all backward", font_size=22,
                   color=GREY_A).next_to(g, UP, buff=0.2).align_to(g, LEFT)
        hist = cite(r"Huang et al., GPipe (Google, 2019); \ times: \ forward $1$, backward $2$; \ simulated",
                    corner=DR, font_size=17)
        with self.voiceover(
            "Tensor parallelism cuts every layer. Pipeline parallelism cuts the model the other way: the first "
            "eight layers on one GPU, the next eight on another, and so on, each GPU a stage. "
            "<bookmark mark='a'/> The trouble is obvious: while the first stage works on a batch, the others wait. "
            "Google's GPipe, in 2019, cut each batch into micro-batches, so that the stages can work on different "
            f"ones at once. <bookmark mark='b'/> Here is GPipe's schedule, simulated exactly: {p} stages, {m} "
            "micro-batches, a backward pass taking twice as long as a forward. Time runs left to right. "
            "<bookmark mark='c'/> The micro-batches fill the pipeline going forward, it drains, then the backward "
            "passes fill it again in reverse. The grey corners are GPUs waiting: the pipeline bubble."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(s_) for s_ in stages], lag_ratio=0.2), FadeIn(arrows), FadeIn(sch))
            vo.wait_until("a")
            self.play(*[Indicate(s_, color=GPU) for s_ in stages[1:]])
            vo.wait_until("b")
            self.play(FadeIn(g.lanes), FadeIn(g.names), FadeIn(key), FadeIn(tl), FadeIn(hist))
            vo.wait_until("c")
            fill_gantt(self, g, run_time=5.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bubble(self):
        Pp = load("pipeline")
        p, m = Pp["p"], Pp["m"]
        colors = {r"p": GPU, r"m": FWD}
        rows = [
            cmath(r"T_{\text{busy}}", r"=", r"m\,(t_F + t_B)", colors=colors, font_size=32),
            cmath(r"T", r"=", r"(m + p - 1)\,(t_F + t_B)", colors=colors, font_size=32),
            cmath(r"\text{bubble}", r"=", r"1 - \frac{T_{\text{busy}}}{T}", r"=", r"\frac{p - 1}{m + p - 1}",
                  colors=colors, font_size=34),
        ]
        whys = [why(r"each GPU does every micro-batch once", font_size=20),
                why(r"the last micro-batch waits $p-1$ stages to start, \ each way", font_size=20),
                why(r"the share of time spent waiting", font_size=20)]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-2.4, buff=0.45, edge=6.9)
        sw = Pp["sweep"]
        g = axes([2, 7], [0, 0.85], x_length=5.4, y_length=2.8, xlabel=r"micro-batches $m$",
                 ylabel=r"bubble \ (share of time)", xticks=[2, 3, 4, 5, 6, 7], yticks=[0, 0.4, 0.8],
                 xfmt=lambda v: f"{2 ** int(v)}", center=[-1.6, -1.65, 0], font_size=18)
        cols = {4: GPU, 8: C.PROB, 16: COMM}
        curves, dots = VGroup(), VGroup()
        for pp, c in cols.items():
            ms = np.linspace(2, 7, 60)
            curves.add(curve(g.ax, ms, (pp - 1) / (2 ** ms + pp - 1), c, 2.5))
            dots.add(VGroup(*[Dot(g.ax.c2p(math.log2(r_["m"]), r_["bubble"]), radius=0.06, color=c)
                              for r_ in sw if r_["p"] == pp]))
        lg = legend([(c, rf"$p = {pp}$") for pp, c in cols.items()], font_size=18).next_to(g, RIGHT, buff=0.3)
        err = max(abs(r_["bubble"] - r_["formula"]) for r_ in sw)
        if err < 1e-9:
            fit = "Every dot sits exactly on its line."
        else:
            fit = f"The dots sit within {err:.4f} of the lines."
        here = label(rf"our chart: \ $p = {p}$, \ $m = {m}$: \ ${100 * Pp['gpipe']['bubble']:.1f}\%$", font_size=22,
                     color=WHITE).next_to(lg, DOWN, buff=0.4).align_to(lg, LEFT)
        rule = label(rf"GPipe's rule: \ $m \ge 4p$ makes it small", font_size=20, color=GREY_A).next_to(here, DOWN,
                                                                                                  buff=0.2)
        rule.align_to(lg, LEFT)
        with self.voiceover(
            "How big is the bubble? Each GPU is busy for m micro-batches, a forward and a backward each. "
            "<bookmark mark='a'/> But the whole schedule takes longer: the last micro-batch can't start on the last "
            "stage until it has passed the p minus one stages before, and the same on the way back. "
            "<bookmark mark='b'/> So the share of time wasted is p minus one, over m plus p minus one. "
            f"<bookmark mark='c'/> For our chart, {100 * Pp['gpipe']['bubble']:.1f} percent. Here is the bubble against "
            "the number of micro-batches, the formula as lines and our simulated schedules as dots. " + fit +
            " More micro-batches shrink it; GPipe's authors found four per stage enough."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(g), FadeIn(here))
            self.play(*[Create(c_) for c_ in curves], FadeIn(lg), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(d_, lag_ratio=0.2) for d_ in dots], lag_ratio=0.3), FadeIn(rule))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def one_f_one_b(self):
        Pp = load("pipeline")
        p, m = Pp["p"], Pp["m"]
        g0, r0 = self._chart("gpipe", y=1.7, width=10.0)
        g1, r1 = self._chart("1f1b", y=-1.3, width=10.0)
        t0 = label(r"GPipe", font_size=22, color=GREY_A).next_to(g0, UP, buff=0.12).align_to(g0, LEFT)
        t1 = label(r"1F1B: \ one forward, one backward, \ alternating", font_size=22, color=GREY_A)
        t1.next_to(g1, UP, buff=0.12).align_to(g1, LEFT)
        mem = VGroup(
            label(rf"micro-batches held at once, \ GPU 0: \ GPipe ${int(r0['peak'][0])}$, \ 1F1B "
                  rf"${int(r1['peak'][0])}$", font_size=22, color=FWD),
            label(rf"bubble: \ ${100 * r0['bubble']:.1f}\%$ \ and \ ${100 * r1['bubble']:.1f}\%$", font_size=22,
                  color=GREY_A),
        ).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.35)
        src = cite(r"Narayanan et al., PipeDream (2019, 2021)", corner=UR, font_size=17)
        same = abs(r0["bubble"] - r1["bubble"]) < 1e-9
        with self.voiceover(
            "GPipe has a second problem: memory. Each stage keeps the activations of every micro-batch it has run "
            "forward until that micro-batch comes back. <bookmark mark='a'/> The 1F1B schedule, from Microsoft's "
            "PipeDream work, starts each micro-batch's backward pass as soon as it can, alternating one forward with "
            "one backward. <bookmark mark='b'/> " + ("The bubble is exactly the same: " if same else "The bubble: ") +
            f"{100 * r1['bubble']:.1f} percent. But the first GPU never holds more than {int(r1['peak'][0])} "
            f"micro-batches at once, the number of stages, instead of all {m}. Memory no longer grows with the number "
            "of micro-batches, so you can use many of them, and the bubble shrinks."
        ) as vo:
            self.play(FadeIn(g0), FadeIn(t0), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(g1.lanes), FadeIn(g1.names), FadeIn(t1))
            fill_gantt(self, g1, run_time=4.5)
            vo.wait_until("b")
            self.play(FadeIn(mem, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def better(self):
        Pp = load("pipeline")
        p, m = Pp["p"], Pp["m"]
        gi, ri = self._chart("interleaved", y=1.75, width=10.0)
        gz, rz = self._chart("zb", y=-1.0, width=10.0 * Pp["zb"]["total"] / (Pp["1f1b"]["total"]))
        gz.align_to(gi, LEFT)
        ti = label(rf"interleaved: \ two chunks per GPU \ (light: \ the second) \ $\to$ \ bubble "
                   rf"${100 * ri['bubble']:.1f}\%$", font_size=20, color=GREY_A).next_to(gi, UP, buff=0.1)
        ti.align_to(gi, LEFT)
        tz = label(rf"zero bubble (ZB-H1): \ the weight gradients fill the gaps \ $\to$ \ ${100 * rz['bubble']:.1f}\%$",
                   font_size=20, color=GREY_A).next_to(gz, UP, buff=0.1).align_to(gz, LEFT)
        key = self._key(split=True).next_to(gz, DOWN, buff=0.25)
        dual = VGroup(
            label(r"DeepSeek-V3's DualPipe: \ micro-batches enter from both ends; \ bubble "
                  r"$(\tfrac{p}{2} - 1)(t_{F\&B} + t_B - 3\,t_W)$, \ two copies of the weights", font_size=20,
                  color=COMM),
        ).to_edge(DOWN, buff=0.3)
        src = cite(r"Narayanan et al.\ (2021); \ Qi et al.\ (ICLR 2024); \ DeepSeek-AI (2024), Table 2; \ simulated",
                   corner=UR, font_size=16)
        f = Pp["formula"]
        with self.voiceover(
            "Two more tricks cut the bubble itself. <bookmark mark='a'/> Interleaving: give each GPU two smaller "
            "chunks of layers instead of one, so a micro-batch visits every GPU twice. The ramp-up takes half as "
            f"long, and the bubble falls to {100 * ri['bubble']:.1f} percent. Llama 3 used this. "
            "<bookmark mark='b'/> Zero bubble, from Sea AI Lab in 2023: split the backward pass in two. The gradient "
            "for the input is urgent, because the stage before is waiting for it; the gradient for the weights is "
            "not, so it can be postponed into the gaps. With equal times for the three, the bubble falls to a third "
            f"of 1F1B's: {100 * rz['bubble']:.1f} percent, at the same memory. <bookmark mark='c'/> DeepSeek-V3 went "
            "further with DualPipe: micro-batches enter the pipeline from both ends at once, and each GPU overlaps "
            "one direction's computation with the other's communication. In its bubble's formula, p over two minus one "
            "stages replace p minus one, at the price of keeping two copies of the weights."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(gi.lanes), FadeIn(gi.names), FadeIn(ti))
            fill_gantt(self, gi, run_time=3.5)
            vo.wait_until("b")
            self.play(FadeIn(gz.lanes), FadeIn(gz.names), FadeIn(tz), FadeIn(key))
            fill_gantt(self, gz, run_time=3.5)
            vo.wait_until("c")
            self.play(FadeIn(dual, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
