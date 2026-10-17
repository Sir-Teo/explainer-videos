from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import TEST, TRAIN, curve, load


class DoubleDescent(VoiceoverScene):
    def construct(self):
        self.card()
        self.curve()

    def card(self):
        card = chapter_card(4, r"Double descent", r"What happens past the point of fitting everything?", part=7)
        with self.voiceover("Chapter four. Double descent."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def curve(self):
        d = load("double")
        ps, te, tr = (np.asarray(d[k]) for k in ("ps", "test", "train"))
        n = int(d["n"])
        lx = np.log10(ps)
        ylo, yhi = -1.0, 2.0
        ax = Axes(x_range=[1, 3.8, 1], y_range=[0, yhi - ylo, 1], x_length=9.0, y_length=4.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.0, -0.6, 0])
        xl = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for t, v in (("10", 1), ("100", 2), ("1{,}000", 3))])
        yl = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=22, color=GREY_B).next_to(ax.c2p(1, v - ylo), LEFT, buff=0.1)
                      for v in range(int(ylo), int(yhi) + 1)])
        xn = label(r"$p$: \ random features per page", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.5)
        yn = label(r"squared error on new pages", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        k_n = int(np.argmin(np.abs(ps - n)))
        k_min1 = int(np.argmin(te[:k_n]))

        def seg(a, b):
            return curve(ax, lx[a:b], np.clip(np.log10(te[a:b]), ylo, yhi) - ylo, TEST, 5)

        part1, part2, part3 = seg(0, k_n - 2), seg(k_n - 3, k_n + 3), seg(k_n + 2, len(ps))
        nline = DashedLine(ax.c2p(math.log10(n), 0), ax.c2p(math.log10(n), yhi - ylo), color=WHITE, stroke_width=2)
        nl = label(rf"$p = n = {n}$: \\ as many features as pages", font_size=24, color=WHITE)
        nl.next_to(nline.get_top(), RIGHT, buff=0.15).shift(DOWN * 0.3)
        trc = curve(ax, lx, np.clip(np.log10(np.maximum(tr, 10 ** ylo)), ylo, yhi) - ylo, TRAIN, 3)
        trl = label(r"training pages: \ fitted exactly past $n$", font_size=22, color=TRAIN)
        trl = VGroup(Line(ORIGIN, RIGHT * 0.5, color=TRAIN, stroke_width=3), trl).arrange(RIGHT, buff=0.15)
        trl.next_to(ax.c2p(1.1, 2.55), RIGHT, buff=0)  # a key in the empty top left, off the curves
        low = Dot(ax.c2p(lx[k_min1], math.log10(te[k_min1]) - ylo), radius=0.08, color=TEST)
        final = Dot(ax.c2p(lx[-1], math.log10(te[-1]) - ylo), radius=0.08, color=TEST)
        floor = DashedLine(ax.c2p(1, math.log10(te[k_min1]) - ylo), ax.c2p(3.8, math.log10(te[k_min1]) - ylo), color=TEST,
                           stroke_width=1.5).set_stroke(opacity=0.5)
        classic = label(r"the classical U", font_size=26, color=TEST).next_to(low, UP, buff=0.35)
        modern = label(r"and down again", font_size=26, color=TEST).next_to(final, UP, buff=0.3).shift(LEFT * 0.4)
        colors = {r"\boldsymbol{\beta}": C.MODEL_Q}
        mn = cmath(r"\min", r"\|", r"\boldsymbol{\beta}", r"\|", r"\;\text{ among all exact fits}", colors=colors,
                   font_size=32).to_corner(UR, buff=0.4)
        cite_ = cite(r"M.~Belkin, D.~Hsu, S.~Ma \& S.~Mandal (2019); \ P.~Nakkiran et al.\ (2020)", corner=UL)
        assert te[-1] < te[k_min1] and te[k_n] > 10 * te[k_min1]
        feats, fits = self.features_picture(), self.min_norm_picture()
        with self.voiceover(
            "Here's the curve that came back. Turn each page into p random features: each feature is a fixed random "
            "mix of the seventy word rates, passed through a bend that zeroes anything negative. Only the weights on "
            "the features are learned, by least squares. <bookmark mark='m'/> When there are more features than "
            "pages, many fits match every training page exactly, so take the one with the smallest weights: of all "
            "the curves through the points, the calmest. <bookmark mark='a'/> With few features, the error on new "
            "pages falls, then "
            "rises again as p approaches the number of pages: the classical U. <bookmark mark='b'/> At exactly "
            f"{n} features, as many as there are pages, the fit is forced through every point, and the error "
            "explodes. <bookmark mark='c'/> And then, past it, the error comes back down, lower than the bottom of "
            "the U."
        ) as vo:
            self.play(FadeIn(feats[0]), FadeIn(feats[2]), FadeIn(cite_))
            self.play(Create(feats[1]), FadeIn(feats[3]), run_time=1.5)
            self.play(Create(feats[4]), FadeIn(feats[5]))
            vo.wait_until("m")
            self.play(FadeIn(fits[0]), FadeIn(mn))
            self.play(Create(fits[1]), FadeIn(fits[3]))
            self.play(Create(fits[2]), FadeIn(fits[4]))
            vo.wait_until("a")
            self.play(FadeOut(feats), FadeOut(fits))
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(xn), FadeIn(yn))
            self.play(Create(part1), run_time=2.0)
            self.play(FadeIn(low), FadeIn(classic))
            vo.wait_until("b")
            self.play(Create(nline), FadeIn(nl), Create(part2), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(part3), run_time=2.0)
            self.play(Create(floor), FadeIn(final), FadeIn(modern))
        with self.voiceover(
            "More parameters than data, and better on new data. Belkin and colleagues named it double descent in "
            "2019, and it turns up in deep networks too. <bookmark mark='a'/> The training error is zero all along "
            "the second descent, so it can't be what decides. What decides is which of the many exact fits you "
            "get, and the smallest one is the simplest. Gradient descent, as part nine shows, quietly prefers fits "
            "like that."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(trc), FadeIn(trl))
        self.wait(0.3)
        self.clear_scene()

    @staticmethod
    def features_picture() -> VGroup:
        """What a random feature is: the 70 word rates, mixed by fixed random weights and bent (ReLU) into p features;
        only the weights from the features to the prediction are learned. Parts: inputs, fixed lines, features,
        their labels, learned lines, their label."""
        def column(n, x, color, r=0.11):
            dots = VGroup(*[Circle(radius=r, color=color, stroke_width=2.5) for _ in range(n)])
            dots.arrange(DOWN, buff=0.16)
            dots.insert(n // 2, MathTex(r"\vdots", font_size=26, color=color))
            return dots.arrange(DOWN, buff=0.12).move_to([x, 0.1, 0])

        ins, fs = column(6, -6.0, GREY_B), column(8, -3.6, C.BITS)
        out = Circle(radius=0.16, color=C.MODEL_Q, stroke_width=3).move_to([-1.5, 0.1, 0])
        ci = [m for m in ins if isinstance(m, Circle)]
        cf = [m for m in fs if isinstance(m, Circle)]
        fixed = VGroup(*[Line(a.get_right(), b.get_left(), color=GREY_D, stroke_width=1.2) for a in ci for b in cf])
        learned = VGroup(*[Line(b.get_right(), out.get_left(), color=C.MODEL_Q, stroke_width=2.5) for b in cf])
        li = label(r"$70$ word rates", font_size=22, color=GREY_B).next_to(ins, DOWN, buff=0.25)
        lf = label(r"$p$ random features", font_size=22, color=C.BITS).next_to(fs, DOWN, buff=0.25)
        lm = label(r"fixed random mix, \\ then a bend", font_size=20, color=GREY_B).next_to(fixed, UP, buff=0.2)
        ll = label(r"learned weights", font_size=20, color=C.MODEL_Q).next_to(learned, UP, buff=0.2)
        return VGroup(ins, fixed, fs, VGroup(li, lf, lm), VGroup(learned, out), ll)

    @staticmethod
    def min_norm_picture() -> VGroup:
        """Two curves through the same four points: one with big weights, wild; the smallest-weight one, calm.
        Parts: axes and points, the wild fit, the calm fit, their two labels."""
        xs_, ys_ = np.array([-1.5, -0.5, 0.5, 1.5]), np.array([0.3, -0.25, 0.35, 0.05])
        calm_c = np.polyfit(xs_, ys_, 3)
        ax = Axes(x_range=[-1.8, 1.8, 1], y_range=[-1.3, 1.3, 1], x_length=4.6, y_length=2.8, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([3.7, 0.1, 0])
        calm = ax.plot(lambda t: np.polyval(calm_c, t), x_range=[-1.8, 1.8], color=C.MODEL_Q, stroke_width=4)
        wild = ax.plot(lambda t: np.polyval(calm_c, t) + 0.9 * math.sin(2 * math.pi * (t + 1.5)), x_range=[-1.8, 1.8],
                       color=C.SURPRISE, stroke_width=2.5)
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=WHITE) for a, b in zip(xs_, ys_)])
        lw = label(r"exact fit, \ big weights", font_size=22, color=C.SURPRISE)
        lc = label(r"exact fit, \ smallest weights", font_size=22, color=C.MODEL_Q)
        VGroup(lw, lc).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(ax, DOWN, buff=0.2)
        return VGroup(VGroup(ax, pts), wild, calm, lw, lc)
