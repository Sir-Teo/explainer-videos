from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, load


class Causal(VoiceoverScene):
    def construct(self):
        d = load("dml")
        self.card()
        self.designs()
        self.dml(d)

    def card(self):
        c = chapter_card(6, r"Causal inference", r"Does $X$ cause $Y$, or do they only move together?", part=PART)
        with self.voiceover("Chapter six. Causal inference."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def designs(self):
        rng = np.random.default_rng(3)
        # difference in differences: two groups, a policy at t = 0 for the treated
        tt = np.arange(-6, 7)
        ctrl = 1.0 + 0.08 * tt + 0.05 * rng.standard_normal(len(tt))
        trt = 1.4 + 0.08 * tt + np.where(tt >= 0, 0.35, 0) + 0.05 * rng.standard_normal(len(tt))
        g1 = axes([-6, 6], [0.4, 2.6], x_length=3.8, y_length=2.6, xticks=[0], yticks=[], font_size=14)
        a1 = g1.ax
        l1 = VGroup(curve(a1, tt, ctrl, DATA_C, stroke_width=2.5), curve(a1, tt, trt, EST, stroke_width=2.5),
                    DashedLine(a1.c2p(0, 0.4), a1.c2p(0, 2.6), color=GREY_B, stroke_width=1.5))
        # regression discontinuity: an outcome against a ranking variable with a jump at the cutoff
        x = np.linspace(-1, 1, 80)
        y = 0.5 + 0.4 * x + np.where(x >= 0, 0.3, 0) + 0.06 * rng.standard_normal(80)
        g2 = axes([-1, 1], [-0.2, 1.4], x_length=3.8, y_length=2.6, xticks=[0], yticks=[], font_size=14)
        a2 = g2.ax
        l2 = VGroup(*[Dot(a2.c2p(a, b), radius=0.03, color=DATA_C if a < 0 else EST) for a, b in zip(x, y)],
                    DashedLine(a2.c2p(0, -0.2), a2.c2p(0, 1.4), color=GREY_B, stroke_width=1.5))
        # instrument: a diagram
        z = Circle(radius=0.35, color=ALT).set_fill(ALT, 0.15)
        xx = Circle(radius=0.35, color=DATA_C).set_fill(DATA_C, 0.15)
        yy = Circle(radius=0.35, color=EST).set_fill(EST, 0.15)
        u = Circle(radius=0.35, color=BAD).set_fill(BAD, 0.15)
        VGroup(z, xx, yy).arrange(RIGHT, buff=0.9)
        u.next_to(VGroup(xx, yy), UP, buff=0.6)
        lbl = VGroup(MathTex("Z", font_size=28).move_to(z), MathTex("X", font_size=28).move_to(xx),
                     MathTex("Y", font_size=28).move_to(yy), MathTex("U", font_size=28).move_to(u))
        arrows = VGroup(Arrow(z.get_right(), xx.get_left(), buff=0.05, stroke_width=3, color=GREY_A),
                        Arrow(xx.get_right(), yy.get_left(), buff=0.05, stroke_width=3, color=GREY_A),
                        Arrow(u.get_bottom(), xx.get_top(), buff=0.05, stroke_width=2, color=BAD),
                        Arrow(u.get_bottom(), yy.get_top(), buff=0.05, stroke_width=2, color=BAD))
        g3 = VGroup(z, xx, yy, u, lbl, arrows)
        panels = VGroup(
            VGroup(label(r"instrument", font_size=24, color=ALT), g3,
                   wrapped_label(r"$Z$ moves $X$ but touches $Y$ only through $X$; hidden $U$ confounds both", 3.8, 18,
                                 GREY_A)).arrange(DOWN, buff=0.3),
            VGroup(label(r"difference in differences", font_size=24, color=EST), VGroup(g1, l1),
                   wrapped_label(r"compare the change in a treated group with the change in a control group", 3.8, 18,
                                 GREY_A)).arrange(DOWN, buff=0.3),
            VGroup(label(r"regression discontinuity", font_size=24, color=GOOD), VGroup(g2, l2),
                   wrapped_label(r"just above and just below a cutoff, firms are alike except for the treatment: the "
                                 r"Russell 1000/2000 boundary assigns index membership by rank", 3.8, 18, GREY_A)).arrange(
                DOWN, buff=0.3),
        ).arrange(RIGHT, buff=0.5, aligned_edge=UP).move_to(ORIGIN)
        with self.voiceover(
            "Regressions describe; they don't explain. Finance increasingly asks causal questions: does joining an "
            "index raise a stock's price, does a regulation change liquidity? Economists have three classic designs. "
            "<bookmark mark='a'/> An instrument: something that moves the cause but touches the outcome only through "
            "it, which lets you see past a hidden confounder. <bookmark mark='b'/> Difference in differences: compare "
            "how a treated group changed with how an untreated group changed over the same time. "
            "<bookmark mark='c'/> And regression discontinuity: where treatment switches on at a cutoff, compare the "
            "units just either side. In American equities the Russell index boundary is the famous one: the "
            "thousandth-largest stock goes into the large-cap index and the thousand-and-first into the small-cap "
            "index, though the two firms are nearly identical."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(panels[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]))
            vo.wait_until("c")
            self.play(FadeIn(panels[2]))
        self.wait(0.4)
        self.clear_scene()

    def dml(self, d):
        dm, nv = np.asarray(d["dml"]), np.asarray(d["naive"])
        g = axes([0, 1.4], [0, 1], x_length=6.4, y_length=3.6, xlabel=r"estimated effect of $d$ on $y$ (true: 0.3)",
                 yticks=[], xticks=[0, 0.3, 0.6, 0.9, 1.2], font_size=18).to_edge(LEFT, buff=2.6).shift(DOWN * 0.6)
        ax = g.ax
        rng = np.random.default_rng(1)
        a = VGroup(*[Dot(ax.c2p(v, 0.7 + 0.15 * rng.random()), radius=0.05, color=GOOD) for v in dm])
        b = VGroup(*[Dot(ax.c2p(v, 0.2 + 0.15 * rng.random()), radius=0.05, color=BAD) for v in nv])
        true = DashedLine(ax.c2p(0.3, 0), ax.c2p(0.3, 1), color=WHITE, stroke_width=2)
        la = label(r"double ML", font_size=20, color=GOOD).next_to(ax.c2p(0, 0.78), LEFT, buff=0.1)
        lb = label(r"OLS with controls", font_size=20, color=BAD).next_to(ax.c2p(0, 0.28), LEFT, buff=0.1)
        eq = VGroup(
            MathTex(r"y = \theta\,d + g(X) + \varepsilon, \qquad d = m(X) + v", font_size=32),
            label(r"$g$ and $m$ unknown and nonlinear; $X$ drives both the treatment and the outcome", font_size=21,
                  color=GREY_A),
            MathTex(r"\hat\theta = \frac{\sum (d - \hat m)(y - \hat\ell)}{\sum (d - \hat m)^2}", font_size=32, color=GOOD),
            label(r"learn $\hat m = \mathbb{E}[d \mid X]$ and $\hat\ell = \mathbb{E}[y \mid X]$ on the other folds, then regress "
                  r"residual on residual", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.18).to_edge(UP, buff=0.4)
        res = VGroup(
            MathTex(rf"{d['dml_mean']:.3f} \pm {d['dml_sd']:.3f}", font_size=30, color=GOOD),
            MathTex(rf"{d['naive_mean']:.2f}", font_size=30, color=BAD),
            label(r"60 simulated samples of 4{,}000; Chernozhukov et al.\ (2018)", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(g, RIGHT, buff=0.4)
        with self.voiceover(
            "Machine learning enters causal inference through a careful door. Suppose a treatment d affects an "
            "outcome y by an amount theta, but both also depend, in complicated ways, on many controls X. "
            "<bookmark mark='a'/> Plant a true effect of zero point three in simulated data, and run ordinary least "
            "squares with the controls entered linearly. It finds about one point one five, four times too large, "
            "because the linear controls can't absorb the nonlinear confounding. <bookmark mark='b'/> Double machine "
            "learning, from Victor Chernozhukov and coauthors in 2018, learns how the treatment and the outcome each "
            "depend on the controls, using flexible models fitted on other folds of the data, removes those parts, "
            "and regresses what is left of the outcome on what is left of the treatment. <bookmark mark='c'/> It "
            "recovers zero point three, with a valid standard error. The House uses this pattern whenever a machine "
            "learning model is asked a causal question, as Part twenty-seven will."
        ) as vo:
            self.play(FadeIn(eq[0]), FadeIn(eq[1]))
            vo.wait_until("a")
            self.play(FadeIn(g), Create(true), FadeIn(lb), LaggedStart(*[FadeIn(x) for x in b], lag_ratio=0.03))
            self.play(FadeIn(res[1]))
            vo.wait_until("b")
            self.play(FadeIn(eq[2]), FadeIn(eq[3]))
            vo.wait_until("c")
            self.play(FadeIn(la), LaggedStart(*[FadeIn(x) for x in a], lag_ratio=0.03), FadeIn(res[0]), FadeIn(res[2]))
        self.wait(0.4)
        self.clear_scene()
