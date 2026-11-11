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
            "For excess or long-short factor returns, normalise the mean of a linear discount factor to one. Zero pricing errors imply that means equal covariances times b. This linear kernel need not stay positive. <bookmark mark='a'/> The plug-in loading is inverse covariance times means, also the tangency-portfolio direction under unrestricted weights. The computed F times b is a portfolio return, not the discount factor itself. Estimated means and small covariance eigenvalues make the weights noisy. The published-predictor panel also selects complete histories using later missingness, so this is not a reconstructed real-time opportunity set."
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
                why('isotropic ridge illustration in chosen factor units; a precise posterior interpretation requires a specified prior'),
                why(r"in the principal components $q_k$ of $\Sigma$ (variances $\lambda_k$), each direction's loading is "
                    r"shrunk by $\lambda_k/(\lambda_k + \gamma)$: the low-variance directions, where a small mean is a "
                    r"huge Sharpe ratio, are shrunk the most")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "Kozak, Nagel and Santosh motivate shrinkage through beliefs about plausible mean-variance opportunities. This code illustrates isotropic ridge in the original factor units; it is not an exact reproduction of every paper specification. <bookmark mark='a'/> The covariance plus gamma identity is solved against the mean vector. Rescaling factor columns changes this isotropic prior. <bookmark mark='b'/> In principal components, each unshrunk loading is multiplied by its eigenvalue over eigenvalue plus gamma. Small-variance directions are shrunk more under this rule. The exact Bayesian interpretation and mapping from kappa require a specified prior and moment convention."
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
        g = axes([-1.6, 0.6], [-1.15, 1.05], x_length=7.6, y_length=4.4, xlabel=r"$\log_{10}\kappa$ (prior Sharpe ratio, a "
                 r"year): more shrinkage to the left", ylabel=r"cross-sectional $R^2$", xticks=[-1.5, -1, -0.5, 0, 0.5],
                 yticks=[-1.0, -0.5, 0, 0.5, 1.0], font_size=13).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lx = np.log10(kap)
        li = curve(ax, lx, r2i, NOISE, stroke_width=2.5)
        lc = curve(ax, lx, r2c, SDF, stroke_width=3.5)
        jb = int(np.argmax(r2c))
        dot = Dot(ax.c2p(lx[jb], r2c[jb]), color=SDF, radius=0.09)
        side = VGroup(
            legend([(NOISE, r"in sample"), (SDF, 'held-block score; future folds used')], font_size=16),
            MathTex(rf"\kappa^* \approx {k['best_kappa']:.2f}\ \text{{a year}},\ R^2_{{oos}} = {r2c[jb]:.2f}", font_size=22,
                    color=SDF),
            wrapped_label('154 predictors, 1973--2020. Full-window penalty calibration and selection; internal fold score, not chronological forecasting', 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The original illustration chooses kappa by three-fold cross-validation of average-return pricing fit. Each fold is a consecutive block, but fitting uses the other blocks, including future months when evaluating an earlier block. Full-sample covariance also calibrates the penalty grid. <bookmark mark='a'/> The training fit improves as shrinkage vanishes. <bookmark mark='b'/> The displayed fold score penalises unstable fitting, but its maximiser is selected on the entire research window. This is an internal selection diagnostic, not a chronological forecast or an independent test. Neither a small grid nor a hump-shaped curve eliminates selection uncertainty."
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
            desk_question(r"why blocks of months", 'Contiguous folds group months, but the other blocks include future observations; no chronological forecast, purging or gap is implemented', width=12.0, font_size=20),
            desk_question(r"why the cross-sectional $R^2$", 'A fold pricing-fit score compares held-block means with its covariance times fitted loadings. It is an internal moment-fit diagnostic, not chronological return prediction', width=12.0, font_size=20),
            desk_question(r"what the choice is", 'One of twenty kappa values is selected through2020. The chosen later split is not independent; a small grid does not preclude material selection bias', width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Three qualifications to the original selection. <bookmark mark='a'/> Contiguous blocks keep neighbouring months together, but fitting on the other folds still uses future observations for earlier validation. There is no chronological forecast, purging or gap. <bookmark mark='b'/> The cross-sectional R squared measures held-block average-return pricing fit, not a realised trading forecast. <bookmark mark='c'/> Choosing among twenty kappa values still creates selection uncertainty. Full-window penalty calibration and later use of this selected kappa prevent the subsequent date split from being an independent validation."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
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
        side = wrapped_label('largest loadings scaled by factor volatility; short-term reversal leads. High turnover can make trading and borrow costs material, but no implementation cost is measured here. These statistical weights are not a feasible-fund certificate', 3.4, 16,
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
        foot = wrapped_label('Retrospective selected split: kappa uses all research months; complete-history universe uses data through2023. Split scale fitted early; later weights fixed. No independent validation or feasible-net-return claim',
                             12.0, 17, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The original split fits weights on 1973 through 2000 and evaluates them in 2001 through 2020. Kappa was chosen using the whole research window, and the universe uses complete histories through 2023. <bookmark mark='a'/> This is a retrospectively selected split with hyperparameter and universe information from the later window, not independent validation or reconstructed real-time availability. <bookmark mark='b'/> The split scales portfolios using the fitting window. The separate full-window series uses full-window volatility scaling. Both omit realistic financing, borrow, costs and capital constraints. No corrected strategy or new test is substituted."
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
            desk_question(r"sparse in what?", 'KNS compare L1 sparsity in characteristic and principal-component coordinates; their empirical finding is not universal nonexistence of characteristic-sparse SDFs', width=12.0, font_size=20),
            desk_question(r"paper returns", r"the predictors are their papers' portfolios, many equal-weighted, rebalanced "
                          r"monthly, short microcaps: a Sharpe ratio of four is a statement about the data, not about a "
                          r"fund", width=12.0, font_size=20),
            desk_question(r"the House's version", r"one parameter, chosen by cross-validation on the research window, "
                          r"twenty values tried: twenty trials on the counter (chapter 11)", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Three qualifications. <bookmark mark='a'/> Sparse representations depend on the coordinate system; conclusions about characteristic versus component sparsity are empirical paper findings, not a theorem that one representation always wins. <bookmark mark='b'/> The plotted factor portfolio is a research-return combination, with missing financing, borrow, costs, capacity and capital constraints. Its covariance normalization does not make it a feasible fund. <bookmark mark='c'/> Twenty shrinkage settings are in the existing local ledger. The future-complete universe, future CV folds and full-window hyperparameter choice remain inherited selection, even though this review adds no trials or scores."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask('when can ridge help later performance? Which directions does the isotropic rule shrink most, and does this selected split establish universal improvement?')
        with self.voiceover('Under what assumptions can ridge shrinkage improve later-window performance, and which directions does this isotropic rule shrink most? Does the preserved selected split establish that it always beats the unshrunk portfolio?'):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
