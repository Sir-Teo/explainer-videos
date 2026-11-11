from __future__ import annotations

import numpy as np

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs40.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, trace)


class Estimation(VoiceoverScene):
    def construct(self):
        self.card()
        self.lognormal()
        self.schedule()
        self.cone()
        self.practice()

    def card(self):
        card = chapter_card(10, r"Estimates", r"Why is software always late?", lit=(1979, 1979),
                            extra=((1979, r"Kahneman and Tversky: \ the planning fallacy"),), part=PART)
        with self.voiceover("Chapter ten. Estimates."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def lognormal(self):
        head = label(r"One task", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 20, 5], [0, 0.17, 0.05], x_length=7.0, y_length=3.4, x_label=r"days", y_label=r"probability",
                 xticks=(0, 5, 10, 15, 20), yticks=(0.05, 0.1, 0.15)).move_to([-2.4, -0.3, 0])
        ax = g.ax
        mu, s = np.log(5.0), 0.6

        def pdf(x):
            return float(np.exp(-(np.log(x) - mu) ** 2 / (2 * s * s)) / (x * s * np.sqrt(2 * np.pi))) if x > 0 else 0
        curve = ax.plot(pdf, x_range=[0.2, 20, 0.05], color=HEAD, stroke_width=3)
        med = DashedLine(ax.c2p(5, 0), ax.c2p(5, pdf(5)), color=YES)
        mean_x = float(np.exp(mu + s * s / 2))
        mean = DashedLine(ax.c2p(mean_x, 0), ax.c2p(mean_x, pdf(mean_x)), color=NO)
        ml = label(r"median: \ 5 days", font_size=18, color=YES).next_to(ax.c2p(5, pdf(5)), UP, buff=0.1).shift(
            LEFT * 0.6)
        mnl = label(rf"mean: \ {mean_x:.1f} days", font_size=18, color=NO).next_to(ax.c2p(mean_x, pdf(mean_x)),
                                                                                RIGHT, buff=0.15)
        notes = VGroup(
            wrapped_label(r"task durations are skewed: \ a task can finish a little early, \ or very late \ "
                          r"(lognormal; \ the spread here is $\sigma = 0.6$)", 4.8, font_size=19, color=WHITE),
            wrapped_label(r"an honest ``most likely'' estimate is the median, \ but the work adds up as means", 4.8,
                          font_size=19, color=NO),
            wrapped_label(r"the \textbf{planning fallacy} \ (Kahneman and Tversky, 1979): \ we plan from the best "
                          r"case of the task in front of us, \ not from how long such tasks took", 4.8,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.2, -0.2, 0])
        with self.voiceover(
            "Estimates fail in a consistent direction, and a picture of one task explains much of it. "
            "<bookmark mark='a'/> How long a task takes is skewed: it can finish a little early, or very late, when "
            "something unexpected turns up. A lognormal shape fits such durations well. "
            "<bookmark mark='b'/> If the most likely value, the median, is five days, the mean is six, because of "
            "the long right tail. An honest estimate gives the median; the schedule experiences the mean. "
            "<bookmark mark='c'/> And people anchor on the best case of the task in front of them rather than on "
            "how long similar tasks took before: Daniel Kahneman and Amos Tversky called it the planning fallacy. "
            "It survives experience: people who know their last projects ran late still expect this one to be on "
            "time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(curve), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(med), FadeIn(ml), Create(mean), FadeIn(mnl), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def schedule(self):
        e = load("estimate")
        head = label(r"Twenty tasks, \ a hundred thousand times", font_size=34).to_edge(UP, buff=0.3)
        rows = []
        for r in e["serial"]:
            rows.append([rf"$\sigma = {r['sigma']}$", r"one after another", f"{r['plan']:.0f}", f"{r['p50']:.0f}",
                         f"{r['p80']:.0f}", f"{r['p95']:.0f}", f"{r['on_time'] * 100:.0f}\\%"])
        for r in e["parallel"][1:]:
            rows.append([rf"$\sigma = {r['sigma']}$", rf"{r['parallel']} streams in parallel", f"{r['plan']:.0f}",
                         f"{r['p50']:.0f}", f"{r['p80']:.0f}", f"{r['p95']:.0f}", f"{r['on_time'] * 100:.0f}\\%"])
        tab = grid_table([r"spread", r"how", r"plan \ (days)", r"P50", r"P80", r"P95", r"on time"], rows,
                         widths=[1.6, 3.4, 1.7, 1.2, 1.2, 1.2, 1.4], row_h=0.48, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.55).set_x(0)
        for i in range(1, len(rows) + 1):
            tab.cells[i][6].set_color(NO)
            tab.cells[i][2].set_color(HEAD)
        lines = VGroup(
            wrapped_label(r"the plan adds up medians, \ five days a task; \ the work adds up draws from the tail", 12.4,
                          font_size=21, color=WHITE),
            wrapped_label(r"parallel streams make it worse: \ the project ends when the \textit{slowest} stream "
                          r"ends \ (a maximum, \ like the fan-out tail of Part 39)", 12.4, font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Now plan a project of twenty such tasks, each with a median of five days, and simulate it a hundred "
            "thousand times. <bookmark mark='a'/> Done one after another, the plan says a hundred days. With a "
            "modest spread the project meets the plan only about a quarter of the time; with the spread we drew, "
            "one time in eight; with a wide spread, one in twenty-five, and the bad cases run to two and a half "
            "times the plan. <bookmark mark='b'/> Splitting the work into parallel streams makes it worse: the "
            "project ends when its slowest stream ends, a maximum, like the fan-out tail of Part 39. With four "
            "streams the plan is met one time in a hundred."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule),
                      *[FadeIn(VGroup(*tab.cells[i])) for i in range(1, 4)], FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(VGroup(*tab.cells[i])) for i in range(4, len(rows) + 1)], FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def practice(self):
        head = label(r"Estimating honestly", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"give a range or a percentile, \ not a date: \ ``80\% by the 15th''", 12.4, font_size=24,
                          color=YES),
            wrapped_label(r"\textbf{reference-class forecasting} \ (Flyvbjerg): \ start from how long similar projects "
                          r"actually took, \ then adjust", 12.4, font_size=24, color=HEAD),
            wrapped_label(r"cut scope, \ not quality; \ and re-estimate from measured throughput \ (Little's law "
                          r"again)", 12.4, font_size=24, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "What helps? <bookmark mark='a'/> Give a range, or a percentile, instead of a date: eighty percent "
            "likely by the fifteenth. <bookmark mark='b'/> Bent Flyvbjerg's reference-class forecasting starts from "
            "how long similar projects actually took, before looking at the details of this one. "
            "<bookmark mark='c'/> When the date is fixed, cut scope rather than "
            "quality, and re-estimate from the throughput you have actually measured."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def cone(self):
        head = label(r"The cone of uncertainty", font_size=36).to_edge(UP, buff=0.3)
        stages = [(r"initial concept", 0.25, 4.0), (r"approved definition", 0.5, 2.0),
                  (r"requirements done", 0.67, 1.5), (r"interface design done", 0.8, 1.25),
                  (r"detailed design done", 0.9, 1.1), (r"finished", 1.0, 1.0)]
        g = axes([0, 5.4, 1], [-2.1, 2.1, 1], x_length=8.6, y_length=4.2, y_label=r"actual effort / estimate "
                 r"\ (log scale)", yticks=(-2, -1, 0, 1, 2), fy=lambda v: {-2: "0.25", -1: "0.5", 0: "1", 1: "2",
                                                                          2: "4"}[int(v)]).move_to([-1.0, -0.4, 0])
        ax = g.ax
        top = trace(ax, [(i, math.log2(hi)) for i, (_, lo, hi) in enumerate(stages)], NO, width=3)
        bot = trace(ax, [(i, math.log2(lo)) for i, (_, lo, hi) in enumerate(stages)], NO, width=3)
        mid = DashedLine(ax.c2p(0, 0), ax.c2p(5, 0), color=GREY_B)
        names = VGroup(*[label(n, font_size=15, color=GREY_A).rotate(0.5).move_to(ax.c2p(i, -2.1) + DOWN * 0.45)
                         for i, (n, _, _) in enumerate(stages)])
        note = wrapped_label(r"Boehm \ (1981) \ and McConnell \ (2006): \ at the first idea, \ the real effort is "
                             r"anywhere from a quarter to four times the estimate; \ the range narrows only as "
                             r"decisions are made, \ not as time passes", 3.6, font_size=18, color=WHITE).move_to(
            [5.2, 0.2, 0])
        with self.voiceover(
            "Uncertainty also has a shape over the life of a project. <bookmark mark='a'/> Barry Boehm, and later "
            "Steve McConnell, summarized it as a cone. At the first idea, the final effort is anywhere from a "
            "quarter of the estimate to four times it. By the time the product is defined, half to double; with "
            "requirements complete, within fifty percent; with the design detailed, within ten. "
            "<bookmark mark='b'/> The cone narrows only as decisions are actually made, not as time passes. A "
            "project that defers its decisions stays at the wide end however long it runs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(mid), FadeIn(names))
            vo.wait_until("a")
            self.play(Create(top), Create(bot), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, KERN, LAM)
