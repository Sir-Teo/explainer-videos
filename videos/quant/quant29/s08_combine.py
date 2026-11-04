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
                      r"IC \to \frac{c}{\sqrt\rho}", font_size=32, colors={r"N_{\text{eff}}": COMB})]
        whys = [why(r"$N$ standardised signals, each with the same IC and the same correlation with each other"),
                why(r"the covariance of the sum with the return adds up $N$ times; its variance has $N$ diagonal terms and "
                    r"$N(N - 1)$ cross terms"),
                why(r"the number of independent signals the $N$ are worth: correlation, not the count, sets the ceiling")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The arithmetic. <bookmark mark='a'/> Take N signals, each with the same information coefficient c, and the "
            "same correlation rho with one another. Average them. <bookmark mark='b'/> The average's correlation with the "
            "return is N c over the square root of N plus N times N minus one times rho. <bookmark mark='c'/> So N "
            "signals are worth N over one plus N minus one times rho independent ones, and as N grows that tends to one "
            "over rho. The combined IC can never exceed c over the square root of rho, however many alphas you mine."
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
        Ns = np.logspace(0, 4, 60)
        top = 10.0
        g = axes([0, 4], [0, top], x_length=7.2, y_length=4.4, xlabel=r"alphas combined, $N$ (log scale)",
                 ylabel=r"combined IC, in units of one alpha's $c$", xticks=[0, 1, 2, 3, 4], yticks=[0, 5, 10],
                 xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        lines = VGroup(*[curve(ax, np.log10(Ns), np.clip(np.sqrt(Ns / (1 + (Ns - 1) * r)), 0, top), col, stroke_width=3)
                         for r, col in zip(rhos, RHO_COL)])
        leg = legend([(col, rf"$\rho = {r:.2f}$" + (r": our top 40" if k == 3 else ""))
                      for k, (r, col) in enumerate(zip(rhos, RHO_COL))], font_size=15).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(rf"with $\rho = 0.3$ the ceiling is $1/\sqrt{{0.3}} = {1 / np.sqrt(0.3):.2f}$ times one "
                             rf"alpha; with our $\rho = {c['rho']:.2f}$, ${1 / np.sqrt(c['rho']):.2f}$", 3.4, 15,
                             GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Draw it. <bookmark mark='a'/> With independent signals, the green line, the combined IC grows like the "
            "square root of N without limit: a hundred alphas are ten times one. <bookmark mark='b'/> With even a "
            "little correlation the curve flattens. At rho of point three, the ceiling is less than twice a single "
            "alpha's IC. <bookmark mark='c'/> And the forty best of our random formulas have an average correlation of "
            f"{c['rho']:.2f} with one another: however many of their kind we add, the combined IC stays under "
            f"{1 / np.sqrt(c['rho']):.1f} times one of them."
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
            "Here are the forty, as a correlation matrix of their daily long-short returns. <bookmark mark='a'/> It is "
            "mostly red. We already dropped every formula that was a near-copy of one we kept, and still the forty move "
            "together. They are cousins: the calm-coin pattern, the price level, dollar volume, written in forty "
            "different ways."
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
        g = axes([0, k + 0.5], [0, top], x_length=7.0, y_length=4.4, xlabel=r"principal component", ylabel=r"eigenvalue",
                 xticks=[1, 5, 10], yticks=[0, top / 2, top], font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.36, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                  fill_color=BAD if i == 0 else COMB, fill_opacity=0.85).move_to(
            ax.c2p(i + 1, 0), aligned_edge=DOWN) for i, v in enumerate(eig[:k])])
        rows = [MathTex(rf"\lambda_1 / \textstyle\sum\lambda = {100 * eig[0] / eig.sum():.0f}\%", font_size=28, color=BAD),
                MathTex(r"N_{\text{eff}} = \frac{(\sum\lambda_i)^2}{\sum\lambda_i^2}" + rf" = {c['n_eff']:.1f}", font_size=28,
                        color=COMB),
                wrapped_label(r"the participation ratio: how many equal, independent directions would give the same "
                              r"spread of eigenvalues", 3.4, 15, GREY_A)]
        side = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            "Count the directions. <bookmark mark='a'/> The correlation matrix's eigenvalues say how much of the forty "
            f"alphas' movement lies along each independent direction. The first alone carries "
            f"{100 * eig[0] / eig.sum():.0f} percent. <bookmark mark='b'/> A standard way to count effective directions, "
            f"the participation ratio, gives {c['n_eff']:.1f}. Forty mined alphas: about three bets."
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
            "And the weights. A desk could weight the alphas equally, or estimate the best weights from the data, by "
            "mean-variance. <bookmark mark='a'/> In the training years, estimated weights always look best, and better "
            f"the more alphas they get: a Sharpe ratio of {r40['mv_train']:.1f} with forty. <bookmark mark='b'/> On 2020 "
            f"they fall apart beyond a handful: with forty alphas, {r40['mv_valid']:+.2f}. <bookmark mark='c'/> Equal "
            f"weights, which estimate nothing, held {r40['ew_valid']:.2f}. The research chapter derives why."
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
