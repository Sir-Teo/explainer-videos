from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import BAD, COMB, GOOD, HURDLE, PART, TRAIN_C, VALID_C, fit_right, load

RHO_COL = [GOOD, QC.DELTA, QC.OPTION, BAD]


class Combine(VoiceoverScene):
    def construct(self):
        c = load("combine")
        self.card()
        self.law()
        self.ceiling(c)
        self.heat(c)
        self.spectrum(c)
        self.sharpes(c)
        self.residual()
        self.question()

    def card(self):
        c = chapter_card(7, r"Combining weak alphas", r"Ten thousand weak signals: how strong is their sum?", part=PART)
        with self.voiceover("Chapter seven. No desk trades one mined alpha. It trades a combination of hundreds or "
                            "thousands, each weak. How strong is their sum?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def law(self):
        rows = [cmath(r"s", r"=", r"\tfrac1N\textstyle\sum_{i=1}^N s_i,\qquad \operatorname{Corr}(s_i, r) = c,\quad "
                      r"\operatorname{Corr}(s_i, s_j) = \rho", font_size=30, colors={r"s": COMB}),
                cmath(r"\operatorname{Corr}(s, r)", r"=", r"\frac{N c}{\sqrt{N + N(N - 1)\rho}} = c\sqrt{\frac{N}{1 + (N - 1)\rho}}",
                      font_size=32, colors={r"\operatorname{Corr}(s, r)": HURDLE}),
                cmath(r"N_{\text{eff}}", r"=", r"\frac{N}{1 + (N - 1)\rho} \ \xrightarrow{N \to \infty}\ \frac1\rho,\qquad "
                      r"IC \to \frac{c}{\sqrt\rho}\quad(\rho>0)", font_size=32, colors={r"N_{\text{eff}}": COMB})]
        whys = [why(r"$N$ standardised signals, each with the same IC and the same correlation with each other"),
                why(r"the covariance of the sum with the return adds up $N$ times; its variance has $N$ diagonal terms and "
                    r"$N(N - 1)$ cross terms"),
                why(r"variance-based breadth, not independent trials; joint feasibility requires $c^2N\le 1+(N-1)\rho$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Start with a population model, not an inference about our forty selected formulas. <bookmark mark='a'/> Standardise the signals and target, assume equal signal-target correlation c and equal pairwise correlation rho, and use a jointly positive semidefinite covariance matrix. <bookmark mark='b'/> The average's correlation is c times square root N over one plus N minus one times rho. Its square cannot exceed one: feasibility requires c squared N no larger than one plus N minus one times rho. <bookmark mark='c'/> For positive rho the variance-based breadth approaches one over rho. The formal IC limit is c over square root rho only along feasible models. With zero rho, fixed nonzero c cannot continue to arbitrarily large N. Statistical independence and independent trials do not follow from this breadth measure."
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

    def ceiling(self, c):
        rhos = [0.0, 0.05, 0.3, round(c["rho"], 2)]
        Ns = np.logspace(0, 2, 60)
        top = 10.0
        g = axes([0, 2], [0, top], x_length=7.2, y_length=4.4, xlabel=r"alphas combined, $N$ (log scale)",
                 ylabel=r"combined IC, in units of one alpha's $c$", xticks=[0, 1, 2], yticks=[0, 5, 10],
                 xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        lines = VGroup(*[curve(ax, np.log10(Ns), np.sqrt(Ns / (1 + (Ns - 1) * r)), col, stroke_width=3)
                         for r, col in zip(rhos, RHO_COL)])
        leg = legend([(col, rf"$\rho = {r:.2f}$" + (r": toy matched to mean return correlation" if k == 3 else ""))
                      for k, (r, col) in enumerate(zip(rhos, RHO_COL))], font_size=15).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        ceil_ = 1 / np.sqrt(c["rho"])
        side = wrapped_label(rf"with $\rho = 0.3$ the ceiling is $1/\sqrt{{0.3}} = {1 / np.sqrt(0.3):.2f}$ times one "
                             rf"alpha; with our $\rho = {c['rho']:.2f}$, ${1 / np.sqrt(c['rho']):.2f}$", 3.4, 15,
                             GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"""Draw the population amplification factor through one hundred signals. <bookmark mark='a'/> The uncorrelated reference rises from one to ten on this displayed domain; a feasible target correlation still bounds the combined IC by one. <bookmark mark='b'/> With rho0.3 the formal large-N multiplier is about1.83. <bookmark mark='c'/> Our selected formulas have average training return correlation {c['rho']:.2f}, giving the illustrative equicorrelation multiplier {ceil_:.1f}. Actual pairwise correlations and target ICs differ, and return correlation is not the same object as signal correlation. This matched toy curve does not prove a ceiling for their realised or future performance."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(lines[0]))
            vo.wait_until("b")
            self.play(Create(lines[1]), Create(lines[2]))
            vo.wait_until("c")
            self.play(Create(lines[3]), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def heat(self, c):
        C = np.asarray(c["corr"], float)
        n = C.shape[0]
        cell = 4.8 / n
        sq = VGroup()
        for i in range(n):
            for j in range(n):
                v = float(np.clip(C[i, j], -1, 1))
                col = interpolate_color(ManimColor(GREY_E), ManimColor(BAD if v > 0 else QC.SPOT), min(abs(v), 1.0))
                sq.add(Square(side_length=cell, stroke_width=0, fill_color=col, fill_opacity=1).move_to(
                    [(j - n / 2 + 0.5) * cell, (n / 2 - i - 0.5) * cell, 0]))
        sq.move_to(LEFT * 2.4 + DOWN * 0.2)
        title = label(r"correlations of the 40 alphas' daily long-short returns, 2018--19", font_size=18,
                      color=GREY_B).next_to(sq, UP, buff=0.2)
        side = VGroup(MathTex(rf"\bar\rho = {c['rho']:.2f}", font_size=32, color=BAD),
                      wrapped_label(r"red: positive, blue: negative. The alphas are the 40 best random formulas by "
                                    r"training IC, after dropping any whose signal correlates above 0.9 with one already "
                                    r"kept", 3.6, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        fit_right(side)
        with self.voiceover(
            "These are training correlations of forty selected long-short return series. <bookmark mark='a'/> Selection first ranks formulas by absolute training IC, then rejects a candidate when its ranked training signal has absolute correlation above0.9 with a previously kept signal. Correlation below that threshold is not independence or a proof of residual alpha. Many return series still move together. Missing component returns are zero-filled for this matrix; it is a descriptive training calculation, not an identified set of independent economic bets."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(FadeIn(sq, lag_ratio=0.001, run_time=2), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def spectrum(self, c):
        eig = np.asarray(c["eig"], float)
        k = 12
        top = float(np.ceil(eig[0] / 5) * 5)
        g = axes([0, k + 0.5], [0, top], x_length=7.0, y_length=4.4, xlabel=r"principal component (first 12 of 40)", ylabel=r"eigenvalue",
                 xticks=[1, 5, 10], yticks=[0, top / 2, top], font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.36, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                  fill_color=BAD if i == 0 else COMB, fill_opacity=0.85).move_to(
            ax.c2p(i + 1, 0), aligned_edge=DOWN) for i, v in enumerate(eig[:k])])
        rows = [MathTex(rf"\lambda_1 / \textstyle\sum\lambda = {100 * eig[0] / eig.sum():.0f}\%", font_size=28, color=BAD),
                MathTex(r"N_{\text{eff}} = \frac{(\sum\lambda_i)^2}{\sum\lambda_i^2}" + rf" = {c['n_eff']:.1f}", font_size=28,
                        color=COMB),
                wrapped_label(r"participation ratio measures covariance concentration; orthogonal components are "
                              r"not necessarily independent", 3.4, 15, GREY_A)]
        side = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        share1 = 100 * eig[0] / eig.sum()
        fit_right(side)
        with self.voiceover(
            f"""Count covariance directions. <bookmark mark='a'/> The first eigenvalue carries {share1:.0f} percent of the trace of this training correlation matrix. Orthogonal principal components are uncorrelated in that sample; they need not be statistically independent. <bookmark mark='b'/> The participation ratio is {c['n_eff']:.1f}. It measures concentration of eigenvalues. It is not an independent-trial count, a number of causal factors or proof that forty selected formulas are three independent bets."""
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def sharpes(self, c):
        rows = c["rows"]
        Ks = np.array([r["K"] for r in rows], float)
        x = np.log10(Ks)
        series = [("mv_train", TRAIN_C, r"estimated weights, on 2018--19 (fitted)"),
                  ("mv_valid", BAD, r"estimated weights, on 2020"),
                  ("ew_valid", VALID_C, r"equal weights, on 2020")]
        ys = np.array([[r[k] for r in rows] for k, _, _ in series])
        lo = float(np.floor(min(0.0, ys.min()) * 2) / 2)
        top = float(np.ceil(ys.max() * 2) / 2)
        g = axes([0, x[-1] + 0.05], [lo, top], x_length=7.2, y_length=4.4, xlabel=r"alphas combined, $K$ (log scale)",
                 ylabel=r"Sharpe ratio, annualised, before costs", xticks=list(x), yticks=[lo, 0, top],
                 xfmt=lambda v: f"{10 ** v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(x[-1], 0), color=GREY_B, stroke_width=1.2)
        lines = VGroup(*[VGroup(curve(ax, x, y, col, stroke_width=3), *[Dot(ax.c2p(a, b), radius=0.05, color=col)
                                                                         for a, b in zip(x, y)])
                         for y, (_, col, _) in zip(ys, series)])
        leg = legend([(col, t) for _, col, t in series], font_size=15).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        r40 = rows[-1]
        with self.voiceover(
            f"""Compare weighting conventions for training-selected formulas. <bookmark mark='a'/> The fitted forty-formula combination has training annualised Sharpe {r40['mv_train']:.1f}. Reusing the selection and estimation data makes it optimistic; an estimated optimum need not dominate every comparator under different constraints or missingness rules. <bookmark mark='b'/> Its labelled2020 validation Sharpe is {r40['mv_valid']:+.2f}. <bookmark mark='c'/> Equal weighting gives {r40['ew_valid']:.2f}, but the component formulas were still selected using training data. Equal weighting averages finite returns, while weighted application zero-fills individual missing returns; the comparison is not otherwise identical executable accounting. Selection, mean estimation and covariance estimation all matter. The research chapter isolates a simpler model."""
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(lines[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lines[2]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def residual(self):
        rows = [cmath(r"s_{\text{new}}", r"=", r"B\,s_{\text{lib}} + e", font_size=34, colors={r"s_{\text{new}}": COMB}),
                cmath(r"IC(e)", r"=", r"\operatorname{Corr}(e, r)", font_size=34, colors={r"IC(e)": HURDLE}),
                cmath(r"IC^2_{\text{lib} + \text{new}}", r"=", r"IC^2_{\text{lib}} + \frac{\operatorname{Cov}(e, r)^2}{\operatorname{Var}(e)\operatorname{Var}(r)}",
                      font_size=30, colors={r"IC^2_{\text{lib} + \text{new}}": GOOD})]
        whys = [why(r"regress the new signal on the library's signals, day by day across the assets; $e$ is what is new"),
                why(r"the residual's own IC: the only part of the new alpha the library does not already have"),
                why(r"for the best linear combination, the squared IC rises by exactly the residual's squared covariance "
                    r"with the target over residual variance times target variance; a population Pearson projection identity")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "For a population linear projection, ask what is new. <bookmark mark='a'/> Project a centred new signal on the existing library using the same distribution and finite second moments. The residual is orthogonal to that library. <bookmark mark='b'/> Its covariance with the target captures an additional linear direction when residual variance is positive. <bookmark mark='c'/> The increase in the best squared multiple Pearson correlation is residual covariance squared divided by residual variance times target variance. This is a projection identity, not a finite-sample selected-alpha significance test. Rank transformations must be defined before projection to interpret it as rank-based prediction; re-ranking a fitted residual changes the problem. Estimated residuals and weights require fresh validation."
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
        q = pause_card(r"10{,}000 alphas, each with out-of-sample IC 0.01, average correlation 0.3. What is the IC of "
                       r"their equal-weighted combination?")
        with self.voiceover(
            "Pause and predict. Ten thousand alphas, each with an out-of-sample IC of one percent, and an average "
            "correlation of point three. What is the IC of their average?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
