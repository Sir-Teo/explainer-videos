from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant30.common import BAD, EST_C, GOOD, HURDLE, PART, REAL_C, TRUE_C, fit_right, illustration, load


class Michaud(VoiceoverScene):
    def construct(self):
        m = load("michaud")
        self.card()
        self.recipe()
        self.frontiers(m)
        self.cloud(m)
        self.why_()
        self.question()

    def card(self):
        c = chapter_card(1, r"Error maximisation", r"What does the optimizer do with the errors in its inputs?", part=PART)
        with self.voiceover("Chapter one. Markowitz gave us the recipe in 1952: feed in expected returns and covariances, "
                            "and out comes the best portfolio. What does the optimizer do with the errors in its inputs?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def recipe(self):
        rows = [cmath(r"\min_w", r"\ ", r"w^\top\Sigma w\quad \text{s.t.}\ w^\top\mu = m,\ w^\top 1 = 1", font_size=34,
                      colors={r"\min_w": TRUE_C}),
                cmath(r"w(m)", r"=", r"\Sigma^{-1}(\lambda 1 + \gamma\mu),\quad \sigma^2(m) = \frac{A m^2 - 2Bm + C}{AC - B^2}",
                      font_size=30, colors={r"w(m)": TRUE_C}),
                cmath(r"\hat w", r"=", r"w(m;\ \hat\mu, \hat\Sigma)", font_size=34, colors={r"\hat w": EST_C})]
        whys = [why(r"the least risky fully invested portfolio with mean $m$ (Markowitz 1952)"),
                why(r"Lagrange multipliers give the weights in closed form; with $A = 1^\top\Sigma^{-1}1$, "
                    r"$B = 1^\top\Sigma^{-1}\mu$, $C = \mu^\top\Sigma^{-1}\mu$ the frontier is a hyperbola (Merton 1972)"),
                why(r"in practice $\mu$ and $\Sigma$ are estimated, and the optimizer treats the estimates as the truth")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The recipe. <bookmark mark='a'/> Find the least risky fully invested portfolio with a given mean. "
            "<bookmark mark='b'/> Lagrange multipliers give the weights in closed form, and the set of best portfolios, "
            "the frontier, is a hyperbola. <bookmark mark='c'/> But the means and covariances are estimated, and the "
            "optimizer cannot tell an estimate from the truth."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def _axes(self):
        g = axes([0, 0.08], [0, 0.02], x_length=7.4, y_length=4.6, xlabel=r"volatility, per month",
                 ylabel=r"expected excess return, per month", xticks=[0, 0.04, 0.08], yticks=[0, 0.01, 0.02],
                 xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=15)
        return g.move_to(LEFT * 1.8 + DOWN * 0.2)

    def frontiers(self, m):
        g = self._axes()
        ax = g.ax
        t = np.asarray(m["targets"], float)
        true = curve(ax, np.asarray(m["true"]), t, TRUE_C, stroke_width=4)
        ests = VGroup(*[curve(ax, np.clip(np.asarray(e), 0, 0.08), t, EST_C, stroke_width=1.5).set_stroke(opacity=0.6)
                        for e in m["sims"]["60"]["est"]])
        leg = legend([(TRUE_C, r"the true frontier"), (EST_C, r"frontiers estimated from 5 years")], font_size=15
                     ).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(r"the truth: the means and covariance of the 49 French industries' monthly excess returns, "
                             r"1970--2020; each estimate: 60 months simulated from it", 3.4, 15, GREY_A
                             ).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "An experiment with a known truth. <bookmark mark='a'/> Take the forty-nine American industry portfolios, "
            "and declare their means and covariance from 1970 to 2020 to be the truth. Here is the true frontier. "
            "<bookmark mark='b'/> Now draw five years of returns from that truth, estimate, and draw the frontier the "
            "estimates imply. Twelve such draws. Every estimated frontier lies far to the left of the true one: each "
            "promises the same return at a fraction of the risk."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(side), FadeIn(illustration(r"simulated from the industries")))
            vo.wait_until("a")
            self.play(Create(true), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(e) for e in ests], lag_ratio=0.1, run_time=3))
        self.wait(0.4)
        self.clear_scene()

    def cloud(self, m):
        g = self._axes()
        ax = g.ax
        t = np.asarray(m["targets"], float)
        true = curve(ax, np.asarray(m["true"]), t, TRUE_C, stroke_width=4)
        pts = np.asarray(m["sims"]["60"]["pts"], float)
        rng = np.random.default_rng(0)
        idx = rng.choice(len(pts), min(150, len(pts)), replace=False)
        promise = VGroup(*[Dot(ax.c2p(min(p[2], 0.079), min(p[3], 0.0199)), radius=0.04, color=EST_C, fill_opacity=0.6)
                           for p in pts[idx]])
        real = VGroup(*[Dot(ax.c2p(min(p[0], 0.079), float(np.clip(p[1], 0.0, 0.0199))), radius=0.04, color=REAL_C,
                            fill_opacity=0.6) for p in pts[idx]])
        med = np.median(pts, axis=0)
        leg = legend([(EST_C, r"what it promises"), (REAL_C, r"what it delivers")], font_size=15).to_edge(
            RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        side = VGroup(MathTex(rf"\text{{promised}}:\ {100 * med[3]:.1f}\%\ \text{{at}}\ {100 * med[2]:.1f}\%", font_size=22,
                              color=EST_C),
                      MathTex(rf"\text{{delivered}}:\ {100 * med[1]:.2f}\%\ \text{{at}}\ {100 * med[0]:.1f}\%", font_size=22,
                              color=REAL_C),
                      wrapped_label(r"medians of 300 draws; each the portfolio targeting 1\% a month on its own "
                                    r"estimates", 3.4, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(
            leg, DOWN, buff=0.35)
        fit_right(side)
        pm, pv, dm, dv = 100 * med[3], 100 * med[2], 100 * med[1], 100 * med[0]
        ratio = med[0] / med[2]
        with self.voiceover(
            "Now ask each estimated optimizer for a portfolio earning one percent a month, and then judge it under the "
            "truth. <bookmark mark='a'/> In red, what each one promised: about one percent at a volatility of "
            f"{pv:.1f} percent, better than the true frontier allows. <bookmark mark='b'/> In blue, what it delivered: "
            f"a median of {dm:.2f} percent a month at {dv:.1f} percent volatility, {ratio:.0f} times the risk it "
            "promised, and below the true frontier. Richard Michaud called mean-variance optimization an error "
            "maximizer: it seeks out the assets whose estimates are most flattering, which are the ones most likely "
            "to be wrong."
        ) as vo:
            self.play(FadeIn(g), Create(true), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in promise], lag_ratio=0.01, run_time=2), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in real], lag_ratio=0.01, run_time=2), FadeIn(side[1]),
                      FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def why_(self):
        cards = VGroup(
            desk_question(r"errors in the means matter most", r"a small error in an expected return moves the weights "
                          r"far more than the same error in a variance (Best and Grauer 1991; Chopra and Ziemba 1993: "
                          r"roughly ten times)", width=12.4, font_size=19),
            desk_question(r"the inverse amplifies", r"$\Sigma^{-1}$ multiplies by one over the smallest eigenvalues, "
                          r"which are the worst estimated: the optimizer leans hardest on the directions it knows least",
                          width=12.4, font_size=19),
            desk_question(r"in-sample, the promise always looks good", r"the estimated frontier is optimistic by "
                          r"construction; the research chapter measures by how much", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why it happens. <bookmark mark='a'/> Errors in the means do the most damage: Vijay Chopra and William Ziemba "
            "found them roughly ten times as costly as the same errors in variances. <bookmark mark='b'/> And the "
            "inverse of the covariance multiplies by one over its smallest eigenvalues, the ones estimated worst, so the "
            "optimizer leans hardest on the directions it knows least. <bookmark mark='c'/> In sample, the promise always "
            "looks good. The research chapter measures exactly how much it lies."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"with 20 years of data instead of 5, will the estimated frontiers move toward the true one, and "
                       r"by how much?")
        with self.voiceover(
            "Pause and predict. With twenty years of data instead of five, how far do the estimated frontiers move "
            "toward the truth?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
