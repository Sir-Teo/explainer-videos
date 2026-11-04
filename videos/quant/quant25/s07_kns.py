from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant25.common import BAD, GOOD, HURDLE, NOISE, PART, SDF, TRUE, ask, fit_right, illustration, load


class KNS(VoiceoverScene):
    def construct(self):
        k = load("kns")
        self.card()
        self.sdf()
        self.prior()
        self.twodir()
        self.path(k)
        self.blocks()
        self.weights(k)
        self.split(k)
        self.notes()

    def card(self):
        c = chapter_card(6, r"Shrinking the cross-section", r"Can a discount factor load on every factor at once?",
                         lit=(2020,), part=PART)
        with self.voiceover("Chapter six. Instead of choosing a few factors, use all of them, and shrink."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sdf(self):
        rows = [cmath(r"m_t", r"=", r"1 - b^\top (F_t - \mathbb{E}F),\quad \mathbb{E}[m\,F] = 0\ \Rightarrow\ \mu = \Sigma b",
                      font_size=38, colors={r"m_t": SDF}),
                cmath(r"\hat b", r"=", r"\hat\Sigma^{-1}\hat\mu", font_size=44, colors={r"\hat b": BAD})]
        whys = [why(r"Part 23's discount factor, linear in $N$ long--short factors: pricing them exactly needs mean returns "
                    r"equal to covariances times $b$, the SDF's loadings"),
                why(r"the plug-in answer is the tangency portfolio again. With 154 factors and 576 months it has 154 "
                    r"loadings estimated from very noisy means, and the inverse covariance magnifies the noise in the "
                    r"smallest directions")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Write Part twenty-three's discount factor as linear in all the factors at once. Pricing them exactly "
            "requires their mean returns to equal their covariances times the loadings b. <bookmark mark='a'/> The "
            "plug-in solution is the tangency portfolio again: the inverse covariance times the means. With a hundred "
            "and fifty-four factors and five hundred and seventy-six months, that is a hundred and fifty-four "
            "loadings from very noisy means, and the inverse covariance magnifies the noise in exactly the directions "
            "with the least risk."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def prior(self):
        rows = [cmath(r"\mu", r"\sim", r"N\Big(0,\ \frac{\kappa^2}{\text{tr}\,\Sigma}\,\Sigma^2\Big)", font_size=42,
                      colors={r"\mu": GOOD}),
                cmath(r"\hat b", r"=", r"(\Sigma + \gamma I)^{-1}\bar\mu,\quad \gamma = \frac{\text{tr}\,\Sigma}{T\kappa^2}",
                      font_size=42, colors={r"\hat b": SDF}),
                cmath(r"\hat b", r"=", r"\textstyle\sum_k \frac{\lambda_k}{\lambda_k + \gamma}\,\frac{q_k^\top\bar\mu}"
                      r"{\lambda_k}\,q_k", font_size=40)]
        whys = [why(r"Kozak, Nagel and Santosh (2020): a prior that the factors' expected returns are proportional to "
                    r"their risk, so that no direction offers an implausibly high Sharpe ratio; $\kappa$ is the prior's "
                    r"root expected squared Sharpe ratio"),
                why(r"the posterior mean is ridge regression of the means on the covariance: one parameter $\gamma$, set by "
                    r"$\kappa$"),
                why(r"in the principal components $q_k$ of $\Sigma$ (variances $\lambda_k$), each direction's loading is "
                    r"shrunk by $\lambda_k/(\lambda_k + \gamma)$: the low-variance directions, where a small mean is a "
                    r"huge Sharpe ratio, are shrunk the most")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "Serhiy Kozak, Stefan Nagel and Shrihari Santosh added a prior: that the factors' expected returns are "
            "proportional to their risk, so that no combination of them offers an absurdly high Sharpe ratio. One "
            "number, kappa, the prior's root expected squared Sharpe ratio, sets how much is plausible. "
            "<bookmark mark='a'/> The posterior mean of b is a ridge regression: the covariance plus gamma times the "
            "identity, inverted, times the means. <bookmark mark='b'/> In principal components the meaning is clear. "
            "Each direction's loading is multiplied by its variance over its variance plus gamma. The low-variance "
            "directions, where a tiny mean return would be a huge Sharpe ratio, are shrunk hardest."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def twodir(self):
        hx = [-3.8, -1.0, 1.6, 4.2]
        heads = [r"direction", r"variance $\lambda_k$", r"unshrunk loading", r"$\gamma = 0.001$"]
        tab = VGroup(VGroup(*[label(h_, font_size=18, color=GREY_A).move_to([x, 1.8, 0]) for h_, x in zip(heads, hx)]))
        for i, (nm, lam) in enumerate(((r"a big component", 0.01), (r"a tiny component", 0.0001))):
            y = 1.1 - 0.7 * i
            b0 = 0.002 / lam
            b1 = lam / (lam + 0.001) * b0
            tab.add(VGroup(label(nm, font_size=19).move_to([hx[0], y, 0]), MathTex(f"{lam}", font_size=26).move_to([hx[1], y, 0]),
                           MathTex(f"{b0:.1f}", font_size=26, color=BAD).move_to([hx[2], y, 0]),
                           MathTex(f"{b1:.2f}", font_size=26, color=SDF).move_to([hx[3], y, 0])))
        foot = wrapped_label(r"both directions earn the same 0.2\% a month. The tiny one does it with a hundredth of the "
                             r"variance, a Sharpe ratio ten times higher, so the plug-in SDF bets a hundred times more on it. "
                             r"Shrinkage cuts that bet by a factor of eleven and the big one's by a tenth: it distrusts "
                             r"high Sharpe ratios that rest on little variance", 12.0, 17, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Two directions, in numbers. Both earn two tenths of a percent a month. One has a variance of one percent, "
            "the other a hundredth of that. <bookmark mark='a'/> The plug-in discount factor loads one hundred times "
            "more on the small direction, because the same mean on a hundredth of the variance is a Sharpe ratio ten "
            "times higher. <bookmark mark='b'/> With gamma at a thousandth, the big direction keeps nine tenths of its "
            "loading and the small one keeps one eleventh. Shrinkage distrusts exactly the high Sharpe ratios that rest "
            "on very little variance, which is where estimation error hides."
        ) as vo:
            self.play(FadeIn(tab[0]), *[FadeIn(r_[:2]) for r_ in tab[1:]])
            vo.wait_until("a")
            self.play(*[FadeIn(r_[2]) for r_ in tab[1:]])
            vo.wait_until("b")
            self.play(*[FadeIn(r_[3]) for r_ in tab[1:]], FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def path(self, k):
        kap, r2c, r2i = np.asarray(k["kappas"]), np.asarray(k["r2_cv"]), np.asarray(k["r2_in"])
        g = axes([-1.6, 0.6], [-0.4, 1.0], x_length=7.6, y_length=4.4, xlabel=r"$\log_{10}\kappa$ (prior Sharpe ratio, a "
                 r"year): more shrinkage to the left", ylabel=r"cross-sectional $R^2$", xticks=[-1.5, -1, -0.5, 0, 0.5],
                 yticks=[-0.4, 0, 0.4, 0.8], font_size=13).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lx = np.log10(kap)
        li = curve(ax, lx, r2i, NOISE, stroke_width=2.5)
        lc = curve(ax, lx, np.maximum(r2c, -0.4), SDF, stroke_width=3.5)
        jb = int(np.argmax(r2c))
        dot = Dot(ax.c2p(lx[jb], r2c[jb]), color=SDF, radius=0.09)
        side = VGroup(
            legend([(NOISE, r"in sample"), (SDF, r"out of sample (3-fold, by block)")], font_size=16),
            MathTex(rf"\kappa^* \approx {k['best_kappa']:.2f}\ \text{{a year}},\ R^2_{{oos}} = {r2c[jb]:.2f}", font_size=22,
                    color=SDF),
            wrapped_label(r"154 predictors, 1973--2020. In sample, less shrinkage always fits better. Out of sample the fit "
                          r"peaks in the middle and collapses toward the plug-in tangency at the right", 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Choose kappa by cross-validation. Fit on two thirds of the months, and score the held-out third by how "
            "much of its average returns the discount factor explains. <bookmark mark='a'/> In sample, less shrinkage "
            "always fits better, rising toward a perfect fit. <bookmark mark='b'/> Out of sample, the fit rises, "
            "peaks near a prior Sharpe ratio of about one a year, explaining about thirty percent of the held-out "
            "means, and then collapses as the shrinkage vanishes and the estimate becomes the noisy tangency. The "
            "shape is Part six's lesson about overfitting, drawn for asset pricing."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(li), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lc), FadeIn(dot), FadeIn(side[1]), FadeIn(side[2]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def blocks(self):
        cards = VGroup(
            desk_question(r"why blocks of months", r"returns are autocorrelated and regimes last years; random months would "
                          r"put a crisis in both the fitting and the testing set and flatter the fit", width=12.0, font_size=20),
            desk_question(r"why the cross-sectional $R^2$", r"the SDF's job is to explain average returns: the metric asks "
                          r"how much of the held-out means $\Sigma b$ reproduces, the pricing analogue of an out-of-sample "
                          r"forecast", width=12.0, font_size=20),
            desk_question(r"what the choice is", r"one number from a grid of twenty: few enough choices that the "
                          r"cross-validation cannot itself overfit badly", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Three details of that cross-validation. <bookmark mark='a'/> The folds are blocks of consecutive months, "
            "not random months: returns cluster in regimes, and random months would put the same crisis in both the "
            "fitting and the testing set. <bookmark mark='b'/> The score is the cross-sectional R squared, how much of "
            "the held-out average returns the discount factor reproduces: the pricing version of an out-of-sample "
            "forecast. <bookmark mark='c'/> And the choice is one number from a grid of twenty, few enough that the "
            "cross-validation cannot itself overfit badly."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def weights(self, k):
        top = k["b_top"][:8]
        g = axes([-0.6, len(top) - 0.4], [0, 0.32], x_length=8.4, y_length=4.0, xlabel=r"", ylabel=r"loading $\times$ "
                 r"volatility", xticks=[], yticks=[0, 0.1, 0.2, 0.3], font_size=13).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        ax = g.ax
        grp = VGroup()
        for i, (nm, v) in enumerate(top):
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, abs(v))[1]
            grp.add(VGroup(Rectangle(width=0.6, height=y1 - y0, stroke_width=0, fill_color=SDF if v > 0 else BAD,
                                     fill_opacity=0.85).move_to([ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]),
                           label(nm.replace("_", r"\_"), font_size=13, color=GREY_A).rotate(0.6).next_to(ax.c2p(i, 0), DOWN,
                                                                                                      buff=0.25)))
        side = wrapped_label(r"the largest loadings of the chosen SDF, scaled by each factor's volatility. Short-term "
                             r"reversal leads: a high-turnover strategy whose paper return would shrink most after costs "
                             r"(Part 26). The SDF is a statistical object; it is not yet a tradable fund", 3.4, 16,
                             GREY_A).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "What does the chosen discount factor load on? <bookmark mark='a'/> Short-term reversal leads by far, then "
            "industry momentum, a measure of efficiency, quarterly profitability and intermediate momentum. Short-term "
            "reversal turns over its whole portfolio every month, so its paper return is the one most exposed to "
            "trading costs. The discount factor is a statistical object that prices the zoo. It is not yet a fund."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in grp], lag_ratio=0.2), FadeIn(side), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def split(self, k):
        sp = k["split"]
        hx = [-3.8, -0.8, 1.8, 4.4]
        heads = [r"portfolio (10\% volatility on 1973--2000)", r"Sharpe, 1973--2000", r"Sharpe, 2001--2020", r"kept"]
        tab = VGroup(VGroup(*[label(h_, font_size=16, color=GREY_A).move_to([x, 2.0, 0]) for h_, x in zip(heads, hx)]))
        for i, (key, nm, col) in enumerate((("tan", r"plug-in tangency, $\hat\Sigma^{-1}\hat\mu$", BAD),
                                            ("kns", r"shrinkage SDF ($\kappa^*$)", SDF), ("ew", r"all 154, equal weights", GOOD))):
            a, b = sp[f"{key}_in"]["sharpe"], sp[f"{key}_oos"]["sharpe"]
            y = 1.3 - 0.7 * i
            tab.add(VGroup(label(nm, font_size=18, color=col).move_to([hx[0], y, 0]),
                           MathTex(f"{a:.1f}", font_size=28).move_to([hx[1], y, 0]),
                           MathTex(f"{b:.2f}", font_size=28, color=col).move_to([hx[2], y, 0]),
                           MathTex(rf"{100 * b / a:.0f}\%", font_size=26).move_to([hx[3], y, 0])))
        foot = wrapped_label(r"fitted on 1973--2000, held through 2001--2020, paper returns before costs. The more a "
                             r"portfolio is optimised, the bigger its in-sample illusion and the larger the share it gives "
                             r"back; but even out of sample, shrinkage and optimisation beat equal weights here, before costs",
                             12.0, 17, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "A test inside the research window: fit on 1973 to 2000, hold through 2001 to 2020. <bookmark mark='a'/> "
            "The plug-in tangency claims a Sharpe ratio of fifteen in sample, an obvious illusion, and keeps about a "
            "sixth of it. The shrinkage discount factor claims six and keeps about a third. Equal weights claim less "
            "than three and keep almost half. <bookmark mark='b'/> The more a portfolio is optimised, the more it "
            "gives back. And yet, out of sample and before costs, the optimised portfolios still did better than equal "
            "weights here. The zoo's paper returns are very large, which is a warning in itself."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab[1:]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def notes(self):
        cards = VGroup(
            desk_question(r"sparse in what?", r"KNS add an L1 penalty: sparsity in the original characteristics fits "
                          r"badly, but a few principal components carry most of the SDF: 'characteristics-sparse' SDFs "
                          r"do not exist, 'PC-sparse' ones do", width=12.0, font_size=20),
            desk_question(r"paper returns", r"the predictors are their papers' portfolios, many equal-weighted, rebalanced "
                          r"monthly, short microcaps: a Sharpe ratio of four is a statement about the data, not about a "
                          r"fund", width=12.0, font_size=20),
            desk_question(r"the House's version", r"one parameter, chosen by cross-validation on the research window, "
                          r"twenty values tried: twenty trials on the counter (chapter 11)", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Three notes. <bookmark mark='a'/> Kozak, Nagel and Santosh also tried an L1 penalty, to make the discount "
            "factor sparse. Sparse in the original characteristics, it fits badly; sparse in principal components, it "
            "works: a few components carry most of it. <bookmark mark='b'/> These are paper returns, many "
            "equal-weighted, rebalanced monthly, short tiny stocks: a Sharpe ratio of four is a statement about the "
            "data, not about a fund. <bookmark mark='c'/> And the House's version has one parameter, chosen among "
            "twenty values on the research window: twenty trials on the counter, in chapter eleven."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"why does ridge shrinkage hurt the in-sample fit but help out of sample, and which directions of the "
                r"factor space does it trust least?")
        with self.voiceover("Why does ridge shrinkage hurt the in-sample fit but help out of sample, and which directions "
                            "of the factor space does it trust least?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
