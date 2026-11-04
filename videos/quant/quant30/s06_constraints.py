from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant30.common import BAD, EST_C, GOOD, HURDLE, PART, SHRINK_C, fit_right, load


class Constraints(VoiceoverScene):
    def construct(self):
        c = load("constraints")
        self.card()
        self.weights(c)
        self.kkt(c)
        self.meaning()
        self.question()

    def card(self):
        c = chapter_card(5, r"Constraints as shrinkage", r"Why does forbidding short sales make a portfolio better?",
                         part=PART)
        with self.voiceover("Chapter five. Practitioners have long added constraints to their optimizers, no short sales, "
                            "position limits, and found that the portfolios got better, not worse. Why should a "
                            "restriction help?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def weights(self, c):
        cols = c["columns"]
        wu, wl = np.asarray(c["w_unc"]), np.asarray(c["w_long"])
        order = np.argsort(wu)
        top = float(np.ceil(np.abs(wu).max() * 10) / 10)
        g = axes([-0.5, 48.5], [-top, top], x_length=11.0, y_length=4.4, xlabel=r"the 49 industries, sorted by the "
                 r"unconstrained weight", ylabel=r"weight", xticks=[], yticks=[-top, 0, top], yfmt=lambda v: f"{v:+.1f}",
                 font_size=15).move_to(DOWN * 0.3)
        ax = g.ax

        def bars(w, col, op, dx=0.0):
            out = VGroup()
            for k, i in enumerate(order):
                v = float(w[i])
                h = abs(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1])
                if h < 0.005:
                    continue
                r = Rectangle(width=0.09, height=h, stroke_width=0, fill_color=col, fill_opacity=op)
                r.move_to([ax.c2p(k + dx, 0)[0], (ax.c2p(0, 0)[1] + ax.c2p(0, v)[1]) / 2, 0])
                out.add(r)
            return out
        bu, bl = bars(wu, EST_C, 0.85, -0.15), bars(wl, SHRINK_C, 0.95, 0.15)
        leg = legend([(EST_C, r"unconstrained minimum variance"), (SHRINK_C, r"long only")], font_size=15
                     ).to_corner(UR, buff=0.35)
        with self.voiceover(
            "The minimum-variance portfolio of the forty-nine industries, from the last ten years of research data. "
            "<bookmark mark='a'/> Unconstrained, it is long some industries and short others, with "
            f"{c['short_sum']:.2f} dollars of short positions for every dollar invested. <bookmark mark='b'/> Forbid "
            f"short sales and only {c['n_pos']} industries keep any weight. The constrained portfolio looks cruder, and "
            "in study after study it does better out of sample."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bu], lag_ratio=0.02))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bl], lag_ratio=0.02))
        self.wait(0.4)
        self.clear_scene()

    def kkt(self, c):
        rows = [cmath(r"2\Sigma w - \gamma 1 - \lambda", r"=", r"0,\quad \lambda_i \ge 0,\ \lambda_i w_i = 0", font_size=32,
                      colors={r"2\Sigma w - \gamma 1 - \lambda": HURDLE}),
                cmath(r"\tilde\Sigma", r"=", r"\Sigma - \tfrac12(\lambda 1^\top + 1\lambda^\top)", font_size=34,
                      colors={r"\tilde\Sigma": SHRINK_C}),
                cmath(r"w_{\ge 0}(\Sigma)", r"=", r"w_{\text{GMV}}(\tilde\Sigma)", font_size=34,
                      colors={r"w_{\ge 0}(\Sigma)": SHRINK_C})]
        whys = [why(r"the Karush--Kuhn--Tucker conditions of the long-only problem: a multiplier $\lambda_i$ for each "
                    r"weight held at zero"),
                why(r"subtract the multipliers from the covariances of the assets that wanted to be shorted"),
                why(rf"Jagannathan and Ma (2003): the long-only portfolio is exactly the unconstrained one for the "
                    rf"modified matrix (here they agree to {c['jm_match']:.0e})")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Ravi Jagannathan and Tongshu Ma explained it in 2003. <bookmark mark='a'/> Write the conditions for the "
            "long-only optimum: one multiplier for every weight that is held at zero. <bookmark mark='b'/> Now subtract "
            "those multipliers from the covariances of the assets the optimizer wanted to short. <bookmark mark='c'/> "
            "The long-only portfolio is exactly the unconstrained minimum-variance portfolio of that modified matrix. "
            "We checked it on the industries: the two sets of weights agree to the sixth decimal."
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

    def meaning(self):
        cards = VGroup(
            desk_question(r"why shorts appear", r"an asset is shorted when its estimated covariances with the others are "
                          r"high, and high estimates are often high errors", width=12.4, font_size=19),
            desk_question(r"what the constraint does", r"it lowers exactly those covariances: shrinkage aimed at the "
                          r"estimates the optimizer was about to exploit", width=12.4, font_size=19),
            desk_question(r"the price", r"if a large covariance is real, the constraint throws away a true hedge; "
                          r"with good estimates (Chapter 4), the constraint matters less", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What it means. <bookmark mark='a'/> The optimizer shorts an asset when its estimated covariances with the "
            "others are high, and unusually high estimates are often unusually large errors. <bookmark mark='b'/> The "
            "constraint lowers exactly those covariances: it is shrinkage, aimed precisely at the estimates the optimizer "
            "was about to exploit. <bookmark mark='c'/> The price: when a large covariance is real, the constraint throws "
            "away a true hedge. With a well-shrunk matrix the constraint matters less."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"an upper bound $w_i \le 5\%$ is added as well. Which covariances does its multiplier change, and "
                       r"in which direction?")
        with self.voiceover(
            "Pause and predict. Add an upper limit of five percent on every weight. Which covariances does its multiplier "
            "change, and in which direction?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
