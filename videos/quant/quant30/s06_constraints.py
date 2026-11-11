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
        self.oos(load("rolling"))
        self.norms()
        self.question()

    def card(self):
        c = chapter_card(5, r"Constraints as shrinkage", r"Why does forbidding short sales make a portfolio better?",
                         part=PART)
        with self.voiceover('Chapter five. Constraints can regularize fitted portfolio weights, but they also remove feasible choices. Why can a restriction help under estimation error, and what does its exact covariance identity prove?'):
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
            f"""The last ten years of research data give a concrete example. <bookmark mark='a'/> Unconstrained GMV has {c['short_sum']:.2f} dollars short per dollar net invested. <bookmark mark='b'/> The long-only solution holds {c['n_pos']} industries. Restrictions can reduce estimation sensitivity, but with the population covariance known, adding a constraint cannot lower the unconstrained minimum variance. Any future benefit is an estimation and implementation question, not a theorem of dominance."""
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
                why(r"adjust rows and columns using binding-constraint multipliers; full-space positive definiteness is unnecessary"),
                why(rf"Jagannathan and Ma (2003): the long-only portfolio is exactly the unconstrained one for the "
                    rf"modified matrix (here they agree to {c['jm_match']:.0e})")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Jagannathan and Ma's algebra. <bookmark mark='a'/> For positive-definite input covariance and a unit budget, write stationarity, nonnegative multipliers and complementarity at the long-only optimum. <bookmark mark='b'/> Subtract half the multiplier-vector outer products from the covariance. A positive multiplier marks a binding constraint, not necessarily an asset shorted in the full unconstrained solution. <bookmark mark='c'/> The adjusted matrix has the same curvature as the original on zero-budget directions, so the same weights minimise its quadratic over all unit-budget weights. It need not be positive definite on the whole space. The stored numerical agreement is shown on screen."
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
            desk_question(r"the joint covariance system", r"weights depend jointly on all estimated covariances; entries that look "
                          r"large need not be errors", width=12.4, font_size=19),
            desk_question(r"what the constraint does", r"positive multipliers lower adjusted rows and columns; regularization of the "
                          r"unit-budget problem, without a future performance guarantee", width=12.4, font_size=19),
            desk_question(r"the price", r"if a large covariance is real, the constraint throws away a true hedge; "
                          r"with good estimates (Chapter 4), the constraint matters less", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Interpret the identity with care. <bookmark mark='a'/> Shorts arise from the whole estimated covariance system, not a rule that every large covariance must be an error. <bookmark mark='b'/> Positive lower-bound multipliers reduce the corresponding adjusted entries. On the unit-budget affine set, the correction is equivalent to a linear penalty, with original curvature preserved. <bookmark mark='c'/> This can regularize noisy weights but may discard useful hedges. Out-of-sample improvement depends on the population, estimates and trading costs; it is not guaranteed by the algebra."
        ) as vo:
            self.add(cards[0])
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def oos(self, ro):
        rows = []
        for W in ("60", "120"):
            r = ro["res"][W]
            rows.append((W, r["sample GMV"], r["long-only GMV"], r["LW const-corr GMV"]))
        hx = [-4.0, -1.0, 1.6, 4.2]
        head = VGroup(label(r"realised volatility", font_size=18, color=GREY_B), label(r"sample GMV", font_size=18, color=EST_C),
                      label(r"long only", font_size=18, color=SHRINK_C), label(r"shrunk", font_size=18, color=GOOD))
        tab = VGroup(head)
        for W, a, b, c in rows:
            tab.add(VGroup(label(rf"{int(W) // 12}-year windows", font_size=19),
                           *[MathTex(rf"{100 * x['vol']:.1f}\%\ ({x['sharpe']:.2f})", font_size=24) for x in (a, b, c)]))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.4 - 0.9 * j, 0])
        foot = wrapped_label(r"the 49 industries, 1980--2020, rebalanced monthly; Sharpe ratios in brackets", 11.0, 16,
                             GREY_A).to_edge(DOWN, buff=0.8)
        a60, b60 = ro["res"]["60"]["sample GMV"], ro["res"]["60"]["long-only GMV"]
        with self.voiceover(
            "Out of sample, on the industries. <bookmark mark='a'/> With five-year windows the unconstrained sample "
            f"portfolio realised {100 * a60['vol']:.1f} percent volatility; long only, {100 * b60['vol']:.1f}: the "
            "constraint did as much as formal shrinkage. With ten-year windows the gap narrows, as there is less noise "
            "for the constraint to remove."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def norms(self):
        rows = [cmath(r"\min_w", r"\ ", r"w^\top\hat\Sigma w\quad\text{s.t.}\ 1^\top w = 1,\ \|w\|_1 \le c", font_size=32,
                      colors={r"\min_w": SHRINK_C}),
                cmath(r"c = 1", r":", r"\text{long only};\qquad c = \infty:\ \text{unconstrained}", font_size=30),
                cmath(r"\|w\|_2^2 \le c", r":", r"\hat\Sigma \to \hat\Sigma + \nu I,\ \text{shrinkage toward the identity}",
                      font_size=30)]
        whys = [why(r"DeMiguel, Garlappi, Nogales and Uppal (2009): bound the total gross exposure instead of forbidding "
                    r"shorts"),
                why(r"a family between the two extremes, tuned by cross-validation"),
                why('a squared-weight bound gives ridge regularisation toward the identity; its constraint multiplier is not the Ledoit--Wolf estimated intensity')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Other constraints regularize different features. <bookmark mark='a'/> A gross-exposure bound controls the L1 norm of fully invested weights, as studied by DeMiguel and coauthors. <bookmark mark='b'/> At unit net investment, an L1 bound of one forces nonnegative weights. Intermediate bounds still require a tuning policy. <bookmark mark='c'/> A squared-L2 upper bound adds a nonnegative diagonal term through its multiplier: ridge covariance regularization, equivalent up to scale to an identity blend when the input trace is positive. The chosen multiplier need not equal a Ledoit-Wolf intensity."
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
