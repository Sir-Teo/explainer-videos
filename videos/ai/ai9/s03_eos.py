from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import curve, load

ETA_COLORS = [C.TRUE_P, C.MODEL_Q]


class EdgeOfStability(VoiceoverScene):
    def construct(self):
        self.card()
        self.rule()
        self.edge()

    def card(self):
        card = chapter_card(2, r"The edge of stability", r"How big can a step be?", part=9)
        with self.voiceover("Chapter two. The edge of stability."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def rule(self):
        ax = Axes(x_range=[-2, 2, 1], y_range=[0, 3, 1], x_length=5.4, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False})
        ax.move_to([-3.4, -0.6, 0])
        lam = 1.5
        par = ax.plot(lambda x: 0.5 * lam * x * x, x_range=[-2, 2], color=GREY_B, stroke_width=3)

        def bounces(eta, x0=1.6, n=7):
            xs = [x0]
            for _ in range(n):
                xs.append(xs[-1] * (1 - eta * lam))
            pts = []
            for a, b in zip(xs, xs[1:]):
                pts += [ax.c2p(a, 0.5 * lam * a * a), ax.c2p(b, 0.5 * lam * b * b)]
            return VMobject(stroke_width=3).set_points_as_corners(pts)

        good = bounces(1.0).set_color(C.INTERVAL)
        bad = bounces(1.42, x0=1.0, n=6).set_color(C.SURPRISE)  # grows by 1.13 a bounce; stopped before it leaves the bowl
        colors = {r"\lambda": C.BITS, r"\eta": C.MODEL_Q}
        f = cmath(r"x", r"\;\to\;", r"(1 - ", r"\eta", r"\,", r"\lambda", r")\,x", colors=colors, font_size=40)
        f.move_to([3.2, 2.0, 0])
        fl = label(r"one step on a bowl of curvature $\lambda$", font_size=24, color=GREY_A).next_to(f, DOWN, buff=0.2)
        cond = cmath(r"\text{stable only if}\;", r"\lambda", r"\;<\;", r"2 / \eta", colors={r"\lambda": C.BITS, r"2 / \eta": C.MODEL_Q},
                     font_size=40).next_to(fl, DOWN, buff=0.6)
        notes = VGroup(label(r"$\eta\lambda < 2$: \ it settles", font_size=26, color=C.INTERVAL),
                       label(r"$\eta\lambda > 2$: \ every step overshoots further", font_size=26, color=C.SURPRISE))
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(cond, DOWN, buff=0.5).set_x(3.2)
        with self.voiceover(
            "Start with the simplest possible case: a bowl with curvature lambda, and a step of size eta. Each step "
            "multiplies the distance from the bottom by one minus eta times lambda. <bookmark mark='a'/> If that's "
            "between minus one and one, the steps shrink and settle. <bookmark mark='b'/> If eta times lambda is "
            "more than two, each step overshoots further than the last, and it blows up. So for a given step size, "
            "gradient descent can only live where the curvature is below two over eta."
        ) as vo:
            self.play(Create(ax), Create(par), Write(f), FadeIn(fl))
            vo.wait_until("a")
            self.play(Create(good), FadeIn(notes[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(bad), FadeIn(notes[1]), run_time=2.0)
            self.play(Write(cond))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def edge(self):
        e = load("eos")
        etas = [float(x) for x in e["etas"]]
        top = max(2 / min(etas) * 1.4, max(float(np.asarray(e[f"curve{eta}"])[:, 2].max()) for eta in etas) * 1.1)
        ax = Axes(x_range=[0, 4000, 1000], y_range=[0, top, 10], x_length=8.4, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.4, -0.5, 0])
        xl = label(r"steps of full-batch gradient descent", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yn = label(r"sharpness: \ the Hessian's largest eigenvalue", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15)
        yn.align_to(ax, LEFT)
        groups = VGroup()
        for eta, col in zip(etas, ETA_COLORS):
            c = np.asarray(e[f"curve{eta}"])
            line = DashedLine(ax.c2p(0, 2 / eta), ax.c2p(4000, 2 / eta), color=col, stroke_width=2)
            ll = label(rf"$2/\eta = {2 / eta:.0f}$", font_size=24, color=col).next_to(line, UP, buff=0.05).align_to(line, RIGHT)
            groups.add(VGroup(curve(ax, c[:, 0], c[:, 2], col, 3.5), line, ll))
        names = VGroup(*[label(rf"$\eta = {eta}$", font_size=26, color=col) for eta, col in zip(etas, ETA_COLORS)])
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.6, 1.8, 0])
        note_ = label(r"training raises the curvature \\ until it reaches $2/\eta$, \\ and then stays at the edge", font_size=26,
                      color=C.BITS).next_to(names, DOWN, buff=0.5).align_to(names, LEFT)
        how = label(r"measured numerically, \ as in Part 3", font_size=22, color=GREY_A).next_to(note_, DOWN, buff=0.35).align_to(names, LEFT)
        col = VGroup(names, note_, how)
        if col.get_right()[0] > 6.8:  # keep the column inside the frame
            col.shift(LEFT * (col.get_right()[0] - 6.8))
        cite_ = cite(r"J.~Cohen, S.~Kaur, Y.~Li, J.~Z.~Kolter \& A.~Talwalkar (2021)", corner=DR)
        # sharpness in a picture: a tightly curved valley and a gently curved one
        bowls = VGroup(*[FunctionGraph(lambda x, k=k: 0.5 * k * x * x, x_range=[-(2 / k) ** 0.5, (2 / k) ** 0.5],
                                       color=col, stroke_width=3) for k, col in ((6.0, C.SURPRISE), (1.0, C.INTERVAL))])
        bowls.arrange(RIGHT, buff=0.6)
        bowls.add(label(r"large $\lambda$", font_size=22, color=C.SURPRISE).next_to(bowls[0], DOWN, buff=0.1),
                  label(r"small $\lambda$", font_size=22, color=C.INTERVAL).next_to(bowls[1], DOWN, buff=0.1))
        sharp = gloss(r"sharpness", r"how tightly the valley curves \\ along its steepest direction: \ the $\lambda$ of "
                      r"the bowl", bowls, corner=UR, width=4.4, color=C.BITS)
        with self.voiceover(
            "Now a real network: the spirals from part eight, trained with the full gradient at two step sizes. "
            "Track the sharpness, the Hessian's largest eigenvalue, from part three: how tightly the valley curves "
            "along its steepest direction, the lambda of that bowl. <bookmark mark='a'/> It climbs, "
            "and climbs, until it hits two over eta, and then it stays there, hovering at the edge, while the loss "
            "keeps going down. <bookmark mark='b'/> Double the step size, and the network settles at half the "
            "sharpness. Training doesn't avoid the edge of stability: it seeks it out. Cohen and colleagues found "
            "this in 2021, and nobody had expected it."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yn), FadeIn(cite_), FadeIn(how))
            self.play(FadeIn(sharp, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(sharp))
            self.play(Create(groups[0][0]), Create(groups[0][1]), FadeIn(groups[0][2]), FadeIn(names[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(groups[1][0]), Create(groups[1][1]), FadeIn(groups[1][2]), FadeIn(names[1]), run_time=3.0)
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()
