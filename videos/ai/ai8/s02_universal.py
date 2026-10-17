from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import HINGE, NEURON, curve, load


class Universal(VoiceoverScene):
    def construct(self):
        self.card()
        self.neuron()
        self.hinges()

    def card(self):
        card = chapter_card(1, r"One layer can do anything", r"What can a sum of bent lines draw?", part=8, lit=(1958,))
        with self.voiceover("Chapter one. What one layer can do."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def neuron(self):
        ins = VGroup(*[Circle(radius=0.28, color=GREY_B, stroke_width=3).move_to([-5.2, 1.6 - 1.1 * k, 0]) for k in range(4)])
        il = VGroup(*[MathTex(rf"x_{k + 1}", font_size=30).move_to(ins[k]) for k in range(4)])
        body = Circle(radius=0.55, color=NEURON, stroke_width=4).move_to([-2.4, 0.0, 0])
        arrows = VGroup(*[Arrow(ins[k].get_right(), body.get_left() + 0.12 * (1.5 - k) * UP, buff=0.05, color=GREY_C,
                                stroke_width=2.5) for k in range(4)])
        wl = VGroup(*[MathTex(rf"w_{k + 1}", font_size=26, color=C.BITS).move_to(arrows[k].point_from_proportion(0.45) + UP * 0.2)
                      for k in range(4)])
        sig = MathTex(r"\Sigma", font_size=40).move_to(body)
        out = Arrow(body.get_right(), body.get_right() + RIGHT * 1.4, buff=0.05, color=NEURON, stroke_width=4)
        colors = {r"\mathbf{w}\cdot\mathbf{x} + b": C.BITS}
        f = cmath(r"\text{out}", "=", r"\max\big(0,\;", r"\mathbf{w}\cdot\mathbf{x} + b", r"\big)", colors=colors,
                  font_size=40).move_to([3.6, 2.2, 0])
        fl = label(r"a weighted sum, \ then a bend: \ ReLU", font_size=26, color=GREY_A).next_to(f, DOWN, buff=0.2)
        ax = Axes(x_range=[-2, 2, 1], y_range=[-0.5, 2, 1], x_length=4.0, y_length=2.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.6, -1.2, 0])
        relu = VMobject(color=NEURON, stroke_width=5).set_points_as_corners([ax.c2p(-2, 0), ax.c2p(0, 0), ax.c2p(2, 2)])
        hl = label(r"one unit, \ along one input: \ a hinge", font_size=24, color=NEURON).next_to(ax, DOWN, buff=0.15)
        cite_ = cite(r"F.~Rosenblatt, \textit{The Perceptron} (1958); \ V.~Nair \& G.~Hinton, ReLU (2010)", corner=DR)
        with self.voiceover(
            "A neural network is built from one kind of part. A unit takes some numbers, <bookmark mark='a'/> "
            "multiplies each by a weight and adds them up, plus a constant, exactly like part five's logistic "
            "regression, <bookmark mark='b'/> and then bends the result: below zero becomes zero. That bend is called "
            "a ReLU. <bookmark mark='c'/> Along any one input, a unit is a hinge: flat, then rising."
        ) as vo:
            self.play(FadeIn(ins), FadeIn(il), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), FadeIn(wl), Create(body), FadeIn(sig))
            vo.wait_until("b")
            self.play(GrowArrow(out), Write(f), FadeIn(fl))
            vo.wait_until("c")
            self.play(Create(ax), Create(relu), FadeIn(hl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hinges(self):
        h = load("hinges")
        xs, y = np.asarray(h["xs"]), np.asarray(h["y"])
        ns = [int(n) for n in h["ns"]]
        ax = Axes(x_range=[-3, 3, 1], y_range=[-2.2, 2.2, 1], x_length=8.4, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-1.4, -0.6, 0])
        tgt = DashedVMobject(curve(ax, xs, y, WHITE, 3), num_dashes=70)
        tl = label(r"the target \ (illustrative)", font_size=24, color=GREY_A).next_to(ax.c2p(-3, 2.2), DR, buff=0.1)

        def fit(n):
            return curve(ax, xs, np.clip(np.asarray(h[f"fit{n}"]), -2.2, 2.2), HINGE, 5)

        def parts(n):
            P = np.asarray(h[f"parts{n}"])
            return VGroup(*[curve(ax, xs, np.clip(p, -2.2, 2.2), NEURON, 1.6).set_stroke(opacity=0.55) for p in P])

        def knots(n):
            return VGroup(*[Line(ax.c2p(k, -2.2), ax.c2p(k, -2.0), color=HINGE, stroke_width=3)
                            for k in np.asarray(h[f"knots{n}"])])

        nv = Integer(ns[0], font_size=40, color=HINGE)
        nl = VGroup(label(r"hinges:", font_size=32), nv).arrange(RIGHT, buff=0.2).move_to([0, 2.2, 0]).align_to([3.4, 0, 0], LEFT)
        ev = DecimalNumber(h[f"err{ns[0]}"], num_decimal_places=3, font_size=32, color=C.SURPRISE)
        el = VGroup(label(r"typical miss:", font_size=26, color=GREY_A), ev).arrange(RIGHT, buff=0.15).next_to(nl, DOWN, buff=0.3)
        el.align_to(nl, LEFT)
        colors = {r"\max(0,\, x - k_i)": NEURON}
        f = cmath(r"f(x) \approx a + b x +", r"\sum_i", r"c_i", r"\max(0,\, x - k_i)", colors=colors, font_size=34)
        f.to_edge(UP, buff=0.35).shift(LEFT * 1.4)
        thm = label(r"universal approximation: \\ enough units, \\ any continuous curve", font_size=28, color=C.BITS)
        thm.next_to(el, DOWN, buff=0.6).align_to(nl, LEFT)
        cite_ = cite(r"G.~Cybenko (1989); \ K.~Hornik, M.~Stinchcombe \& H.~White (1989)", corner=DR)
        cur_fit, cur_parts, cur_knots = fit(ns[0]), parts(ns[0]), knots(ns[0])
        with self.voiceover(
            "Add hinges together, each with its own position and slope, and you can draw any curve you like. "
            "<bookmark mark='a'/> Two hinges: a crude zigzag. <bookmark mark='b'/> Four. Eight. Sixteen. Sixty-four, "
            "and the miss is down to about one part in a thousand. <bookmark mark='c'/> That's the universal "
            "approximation theorem, from 1989: one layer of enough units can approximate any continuous function. "
            "It says a network can represent the answer. It doesn't say how many units it takes, or whether training "
            "will find them."
        ) as vo:
            self.play(Create(ax), Create(tgt), FadeIn(tl), Write(f))
            vo.wait_until("a")
            self.play(FadeIn(cur_parts), Create(cur_fit), FadeIn(cur_knots), FadeIn(nl), FadeIn(el))
            vo.wait_until("b")
            for n in ns[1:]:
                nf, np_, nk = fit(n), parts(n), knots(n)
                self.play(Transform(cur_fit, nf), FadeOut(cur_parts), FadeIn(np_), Transform(cur_knots, nk),
                          ChangeDecimalToValue(nv, n), ChangeDecimalToValue(ev, h[f"err{n}"]), run_time=1.2)
                cur_parts = np_
            vo.wait_until("c")
            self.play(FadeIn(thm), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()
