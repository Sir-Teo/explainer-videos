from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs31.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, curve, fit_right, gantt, grid_table,
                                   load, time_axis)


class Share(VoiceoverScene):
    def construct(self):
        self.card()
        self.lottery()
        self.unfair()
        self.cfs()

    def card(self):
        card = chapter_card(9, r"Proportional share: \ lottery, \ stride, \ CFS",
                            r"How do you give each job its fair share?", lit=(1994, 2007, 2023),
                            extra=((1994, r"lottery scheduling"), (2007, r"Linux's CFS"), (2023, r"EEVDF")),
                            part=PART)
        with self.voiceover("Chapter nine. Proportional share: lottery, stride, and Linux's completely fair "
                            "scheduler."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def lottery(self):
        d = load("share")
        head = label(r"Tickets: \ A holds 300, \ B holds 100", font_size=34).to_edge(UP, buff=0.3)
        n = len(d["stride"])
        ax = Axes(x_range=[0, n, 30], y_range=[0.5, 1.0, 0.1], x_length=6.6, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)
        xt = VGroup(*[label(str(q), font_size=15, color=GREY_A).next_to(ax.c2p(q, 0.5), DOWN, buff=0.08)
                      for q in range(0, n + 1, 30)])
        yt = VGroup(*[label(f"{y:.1f}", font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.08)
                      for y in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)])
        xl = label(r"quanta", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"A's share so far", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        target = DashedLine(ax.c2p(0, 0.75), ax.c2p(n, 0.75), color=GREY_B, stroke_width=1.5)
        k0 = 4

        def clip(v):
            return [min(max(x, 0.5), 1.0) for x in v[k0:]]
        lots = VGroup(*[curve(ax, list(range(k0 + 1, n + 1)), clip(run), DATA if k == 0 else GREY_B,
                              width=1.8 if k else 2.5, dots=False) for k, run in enumerate(d["lottery"])])
        stride = curve(ax, list(range(k0 + 1, n + 1)), clip(d["stride"]), YES, width=3.0, dots=False)
        notes = VGroup(
            label(r"\textbf{lottery} \ (Waldspurger and Weihl, 1994): \\ each quantum, \ draw a ticket at random",
                  font_size=21, color=DATA),
            label(rf"five runs: \ after {n} quanta, \ A's share \\ is anywhere from "
                  rf"{min(r[-1] for r in d['lottery']):.2f} to {max(r[-1] for r in d['lottery']):.2f}", font_size=21,
                  color=GREY_A),
            label(r"\textbf{stride} \ (1995): \ each job has a stride \\ $L/\textrm{tickets}$ and a pass; \ run the "
                  r"smallest \\ pass, \ add its stride", font_size=21, color=YES),
            label(r"stride is exactly 3 to 1 at every moment, \\ give or take one quantum", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.5).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "Sometimes we want shares, not priorities: three quarters of the machine for A, one quarter for B. "
            "<bookmark mark='a'/> Carl Waldspurger and William Weihl's lottery scheduling, in 1994, gives A three "
            "hundred tickets and B a hundred, and at every quantum draws a ticket at random. <bookmark mark='b'/> On "
            "average A gets three quarters. But in any one run, after a hundred and twenty quanta, A's share might be "
            "anything from two thirds to eighty-five percent. <bookmark mark='c'/> A year later Waldspurger gave the "
            "deterministic version, stride scheduling. Each job's stride is a large number divided by its tickets, "
            "and each job keeps a pass value. Run the job with the smallest pass, and add its stride to it. <bookmark "
            "mark='d'/> Stride keeps the ratio exactly three to one, give or take one quantum, at every moment."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), Create(target))
            vo.wait_until("a")
            self.play(Create(lots[0]), FadeIn(notes[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in lots[1:]], lag_ratio=0.2), FadeIn(notes[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(stride), FadeIn(notes[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def unfair(self):
        d = load("share")
        head = label(r"Randomness is fair only in the long run", font_size=34).to_edge(UP, buff=0.3)
        u = d["unfair"]
        ax = Axes(x_range=[0, 2.4, 0.5], y_range=[0.5, 1.0, 0.1], x_length=6.4, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)
        xt = VGroup(*[label(str(x), font_size=15, color=GREY_A).next_to(ax.c2p(math.log10(x), 0.5), DOWN, buff=0.08)
                      for x in (1, 3, 10, 30, 100)])
        yt = VGroup(*[label(f"{y:.1f}", font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.08)
                      for y in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)])
        xl = label(r"job length, \ in quanta", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"unfairness: \ first finish / second finish \ (1 is fair)", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.1).align_to(ax, LEFT)
        c1 = curve(ax, [math.log10(r["L"]) for r in u], [r["lottery"] for r in u], DATA)
        c2 = curve(ax, [math.log10(r["L"]) for r in u], [r["stride"] for r in u], YES)
        k1 = label(r"lottery \ (200 runs each)", font_size=18, color=DATA).move_to(ax.c2p(1.6, 0.72))
        k2 = label(r"stride", font_size=18, color=YES).move_to(ax.c2p(0.55, 0.95))
        notes = VGroup(
            label(r"two equal jobs, \ equal tickets: \\ they should finish together", font_size=21, color=WHITE),
            label(rf"jobs of 10 quanta: \ lottery {u[3]['lottery']:.2f}, \ stride {u[3]['stride']:.2f}",
                  font_size=21, color=GREY_A),
            label(r"lottery's error shrinks like $1/\sqrt{n}$; \\ stride's like $1/n$", font_size=21, color=HEAD),
            label(r"lottery's strength: \ no state to keep, \\ tickets you can hand to a server you call",
                  font_size=21, color=DATA),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.5).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "How unfair is the lottery? Waldspurger's measure: run two jobs of equal length with equal tickets, and "
            "divide the first finishing time by the second. One means perfectly fair. <bookmark mark='a'/> For jobs "
            "of one quantum, either one finishes first, and the ratio is a half for both methods. <bookmark "
            "mark='b'/> For jobs of ten quanta, the lottery averages eighty-two hundredths, and stride ninety-five. "
            "<bookmark mark='c'/> Random draws even out only slowly, with the error shrinking like one over the "
            "square root of the number of draws; stride's shrinks like one over the number itself. <bookmark "
            "mark='d'/> The lottery has other virtues: it keeps no state, and a client can lend its tickets to a "
            "server that works on its behalf."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Create(c1), Create(c2), FadeIn(k1), FadeIn(k2), run_time=2.0)
            for mk, n_ in zip("bcd", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def cfs(self):
        d = load("share")
        head = label(r"Linux's completely fair scheduler", font_size=36).to_edge(UP, buff=0.3)
        c3 = d["cfs3"]
        g = gantt(c3["segments"], 0, 200, width=10.6, h=0.42, lanes=["a", "b", "c"], font=18).move_to([0.5, 1.5, 0])
        ax = time_axis(g, [0, 40, 80, 120, 160, 200], font=13)
        rules = VGroup(
            label(r"each task's \textbf{virtual runtime} grows as it runs: \ $\Delta v = \Delta t \cdot 1024 / w$, "
                  r"\ $w$ its weight", font_size=20, color=WHITE),
            label(r"always run the task with the smallest $v$; \ keep the tasks in a \textbf{red--black tree} by $v$ "
                  r"\ (Part 17): \ $O(\log n)$", font_size=20, color=YES),
            label(r"a new task starts at the smallest $v$: \ c arrives at tick 40 and joins without a backlog",
                  font_size=20, color=GREY_A),
            label(rf"weights: \ nice 0 is 1024, \ each nice level 1.25$\times$: \ nice 0 against nice 5 gets "
                  rf"{d['cfs_n0'] * 100:.1f}\% \ (expected {d['cfs_expect'] * 100:.1f}\%)", font_size=20, color=HEAD),
            label(r"Ingo Moln\'ar, \ 2007; \ since Linux 6.6 \ (2023) \ \textbf{EEVDF}: \ the same shares, \ plus a "
                  r"virtual deadline for latency", font_size=20, color=LAM),
        ).arrange(DOWN, buff=0.17).next_to(ax, DOWN, buff=0.4)
        with self.voiceover(
            "Linux took a different road to proportional share. Since 2007 its main scheduler, Ingo Molnár's "
            "completely fair scheduler, tracks a virtual runtime for each task. <bookmark mark='a'/> The virtual "
            "runtime grows as the task runs, more slowly for tasks with more weight. <bookmark mark='b'/> The "
            "scheduler always runs the task whose virtual runtime is smallest, and keeps the tasks sorted in a "
            "red-black tree, the balanced tree of Part 17, so the choice takes logarithmic time. <bookmark "
            "mark='c'/> Tasks a and b alternate. When c arrives at tick forty, it starts at the smallest virtual "
            "runtime, not at zero, or it would monopolise the processor while it caught up. <bookmark mark='d'/> The "
            "weights come from the nice value: each level is a factor of one point two five. A task at nice zero "
            "against one at nice five gets seventy-five point four percent, as the weights predict. <bookmark "
            "mark='e'/> In 2023, Linux 6.6 replaced it with EEVDF, an algorithm from 1995 that keeps the same shares "
            "but also gives each task a virtual deadline, so that tasks needing short, frequent slices get them "
            "promptly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g.lane_labels), FadeIn(ax),
                      LaggedStart(*[FadeIn(b) for b in g.bars], lag_ratio=0.05), run_time=2.0)
            for mk, r in zip("abcde", rules):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.wait(0.3)
        self.clear_scene()
