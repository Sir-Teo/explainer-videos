from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.compute import load

P_COLORS = [C.SURPRISE, C.BITS, C.INTERVAL]


def curve(ax, xs, ys, color, stroke_width=3) -> VMobject:
    return VMobject(color=color, stroke_width=stroke_width).set_points_smoothly([ax.c2p(x, y) for x, y in zip(xs, ys)])


class Horizon(VoiceoverScene):
    def construct(self):
        self.card()
        self.compound()
        self.doubling()

    def card(self):
        card = chapter_card(2, r"Long horizons", r"Why are long tasks so hard?", part=18)
        with self.voiceover("Chapter two. Long horizons."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def compound(self):
        h = load("horizon")
        ns = np.asarray(h["ns"], float)
        ps = [float(p) for p in h["ps"]]
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 1, 0.25], x_length=8.4, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.4, -0.4, 0])
        xt = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for t, v in (("1", 0), ("10", 1), ("100", 2), ("1{,}000", 3), ("10{,}000", 4))])
        yt = VGroup(*[MathTex(rf"{int(100 * v)}\%", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in (0, 0.5, 1)])
        xn = label(r"steps in the task \ (log scale)", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"chance of finishing it", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        lines = VGroup(*[curve(ax, np.log10(ns), np.asarray(h[f"succ{p:g}"]), c_, 4) for p, c_ in zip(ps, P_COLORS)])
        keys = VGroup(*[label(rf"each step right ${100 * p:g}\%$ of the time", font_size=24, color=c_) for p, c_ in zip(ps, P_COLORS)])
        keys.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.4, 1.6, 0])
        colors = {r"p": C.BITS, r"n": C.TRUE_P}
        f = cmath(r"P(\text{done})", "=", r"p", r"^{\,", r"n", r"}", colors=colors, font_size=44).move_to([4.4, -0.4, 0])
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(4, 0.5), color=GREY_D, stroke_width=1.5)
        v99 = 0.99 ** 100
        # a task as a chain of steps, schematic: each must go right; one slip and the rest never happen
        n_st = 9
        st_d = VGroup(*[Dot([0.38 * i, 0, 0], radius=0.09, color=GREY_C) for i in range(n_st)])
        st_l = Line(st_d[0].get_center(), st_d[-1].get_center(), color=GREY_D, stroke_width=2)
        st_t = VGroup(label(r"start", font_size=18, color=GREY_B).next_to(st_d[0], DOWN, buff=0.15),
                      label(r"finish", font_size=18, color=GREY_B).next_to(st_d[-1], DOWN, buff=0.15))
        hz = gloss(r"horizon", r"how many steps a task takes, \\ from start to finish", picture=VGroup(st_l, st_d, st_t),
                   corner=DR, width=3.6, color=C.TRUE_P)
        hz_d = hz[1][2][1]
        slip = 6  # schematic: the step that goes wrong
        with self.voiceover(
            "Agents work in long chains of steps: read a page, click, write code, run it, read the error. "
            "<bookmark mark='h'/> How many steps a task takes, from start to finish, is its horizon, and every "
            "step has to go right. <bookmark mark='a'/> If each step succeeds with probability p, a task of n steps "
            "succeeds with p to the n. <bookmark mark='b'/> At ninety percent per step, a ten-step task already "
            f"fails two times in three. At ninety-nine percent, a hundred-step task succeeds only {100 * v99:.0f} "
            "percent of the time. Small errors compound."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), Create(half))
            vo.wait_until("h")
            self.play(FadeIn(hz))
            self.play(LaggedStart(*[d_.animate.set_color(P_COLORS[2]) for d_ in hz_d[:slip]], lag_ratio=0.25), run_time=1.5)
            self.play(hz_d[slip].animate.set_color(C.SURPRISE).scale(1.5), *[d_.animate.set_opacity(0.25) for d_ in hz_d[slip + 1:]],
                      run_time=0.6)
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), FadeIn(keys), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def doubling(self):
        h = load("horizon")
        pr, hl = np.asarray(h["p_range"]), np.asarray(h["half_len"])
        err = 1 - pr
        ax = CornerAxes(x_range=[-4, -0.3, 1], y_range=[0, 4, 1], x_length=7.6, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.8, -0.4, 0])
        xt = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for t, v in ((r"0.01\%", -4), (r"0.1\%", -3), (r"1\%", -2), (r"10\%", -1))])
        yt = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(-4, v), LEFT, buff=0.1)
                      for t, v in (("1", 0), ("10", 1), ("100", 2), ("1{,}000", 3), ("10{,}000", 4))])
        xn = label(r"error rate per step \ (log scale)", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"the task length it finishes half the time", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        c = curve(ax, np.log10(err), np.log10(hl), C.BITS, 4)
        f = cmath(r"n_{1/2} \;=\; \frac{\ln 2}{-\ln p} \;\approx\; \frac{0.69}{1 - p}", font_size=36).move_to([4.4, 1.4, 0])
        fl = label(r"halve the error per step, \\ double the task length", font_size=26, color=C.BITS).next_to(f, DOWN, buff=0.35)
        metr = label(r"METR (2025): \ the length of tasks AI agents \\ finish half the time has doubled \\ about every seven months "
                     r"since 2019", font_size=22, color=GREY_A).next_to(fl, DOWN, buff=0.5)
        cite_ = cite(r"T.~Kwa et al.\ (METR), \textit{Measuring AI Ability to Complete Long Tasks} (2025)", corner=DR)
        with self.voiceover(
            "Turn it around: how long a task can an agent finish half the time? <bookmark mark='a'/> It's about "
            "zero point seven divided by the error rate per step. Halve the errors, and the reachable task length "
            "doubles. <bookmark mark='b'/> METR measured exactly this for real AI agents, on tasks timed by how long "
            "they take people: the length agents finish half the time has doubled about every seven months, for six "
            "years. Reliability per step is what buys long horizons."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn))
            vo.wait_until("a")
            self.play(Create(c), Write(f), FadeIn(fl), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(metr), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()
