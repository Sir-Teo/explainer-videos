from __future__ import annotations

import numpy as np

from videos.stats.stats28.common import *  # noqa: F403


class AIC(VoiceoverScene):
    def construct(self):
        self.card()
        self.cp()
        self.kl()
        self.derivation()
        self.tic()
        self.aicc()
        self.bench()
        self.deltas()

    def card(self):
        card = chapter_card(2, r"Cp and AIC", r"Estimate the optimism, \ add it back", lit=(1973,), part=PART)
        with self.voiceover("Chapter two. Mallows's Cp and Akaike's information criterion."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def cp(self):
        rows = [
            cmath(r"C_p", r"=", r"\overline{\text{err}} + 2 d\, \hat\sigma^2/n", font_size=32),
            cmath(r"\hat\sigma^2", r":", r"\text{from the biggest model}", font_size=30),
            cmath(r"E\,C_p", r"=", r"E\,\text{err}_{\text{in}}", font_size=32),
            cmath(r"\text{choose}", r":", r"\text{the smallest } C_p", font_size=30),
        ]
        rows[0][2].set_color(AICC)
        whys = [why(r"Mallows (1973): \ training error plus optimism"), why(r"unbiased only under an adequate variance model"),
                why(r"an unbiased estimate of prediction error"), why(r"for linear models with squared error")]
        with self.voiceover(
            "<bookmark mark='a'/> The direct cure: estimate the optimism and add it back. Colin Mallows's Cp is the "
            "training error plus two d sigma squared over n, <bookmark mark='b'/> with a noise-variance estimate, "
            "often from a sufficiently rich full model. <bookmark mark='c'/> With fixed linear fits and an unbiased "
            "noise estimate, its expectation is prediction error for new responses at the same design points, "
            "<bookmark mark='d'/> so choosing the model with the smallest Cp aims at the best predictor. It is "
            "chapter one's optimism, made into a criterion."
        ) as vo:
            intro=label('Cp adds a variance-based optimism estimate to training error',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def kl(self):
        rows = [
            cmath(r"\mathrm{KL}(g \,\|\, f_\theta)", r"=", r"E_g \log g(Y) - E_g \log f(Y \mid \theta)", font_size=30),
            cmath(r"\text{goal}", r":", r"\text{maximize } E_{\text{new}}\, \log f(Y_{\text{new}} \mid \hat\theta(y))", font_size=30),
            cmath(r"\ell(\hat\theta)", r":", r"\text{over-estimates it, \ by about } k", font_size=30),
            cmath(r"\text{AIC}", r"=", r"-2\ell(\hat\theta) + 2k", font_size=34),
        ]
        rows[3][2].set_color(AICC)
        whys = [why(r"distance from the truth $g$ to the model"), why(r"the expected log score of new data"),
                why(r"the same optimism, \ on the log scale"), why(r"Akaike (1973)")]
        with self.voiceover(
            "<bookmark mark='a'/> Hirotugu Akaike generalized it beyond squared error. Measure how far a fitted model is "
            "from the unknown truth g by the Kullback–Leibler divergence. <bookmark mark='b'/> Up to a constant that is the "
            "same for every model, minimizing it means maximizing the expected log density of new data under the fitted "
            "model, the log score of Part 24. <bookmark mark='c'/> The maximized log likelihood estimates that, but "
            "optimistically, because the same data chose theta hat: by about k, the number of parameters. "
            "<bookmark mark='d'/> Correct for it, multiply by minus two, and you have AIC."
        ) as vo:
            intro=label('AIC targets expected predictive log loss for a fixed regular candidate',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def derivation(self):
        rows = [
            cmath(r"\ell(\theta_0)", r"\approx", r"\ell(\hat\theta) - \tfrac12 (\hat\theta - \theta_0)^\top I_n (\hat\theta - \theta_0)", font_size=28),
            cmath(r"E\,\ell_{\text{new}}(\hat\theta)", r"\approx", r"E\,\ell_{\text{new}}(\theta_0) - \tfrac12 E (\hat\theta - \theta_0)^\top I_n (\hat\theta - \theta_0)", font_size=26),
            cmath(r"E (\hat\theta - \theta_0)^\top I_n (\hat\theta - \theta_0)", r"=", r"\mathrm{tr}(I_n I_n^{-1}) = k", font_size=28),
            cmath(r"E\,\ell(\hat\theta) - E\,\ell_{\text{new}}(\hat\theta)", r"\approx", r"\tfrac k2 + \tfrac k2 = k", font_size=30),
        ]
        rows[3][2].set_color(AICC)
        whys = [why(r"Taylor at the MLE"), why(r"Taylor at the truth $\theta_0$"), why(r"a $\chi^2_k$ in expectation, \ Part 22"),
                why(r"half above the truth, \ half below")]
        with self.voiceover(
            "<bookmark mark='a'/> Where k comes from, in two Taylor expansions. The log likelihood at the truth is the "
            "maximized log likelihood minus half a quadratic form in the estimation error. <bookmark mark='b'/> The new data's "
            "expected log likelihood at the estimate is its value at the truth minus the same quadratic form. "
            "<bookmark mark='c'/> That quadratic form is, in expectation, Part 22's chi-squared with k degrees of freedom: it "
            "averages k. <bookmark mark='d'/> So the training log likelihood sits k over two above the truth's, and the new "
            "data's k over two below it: an optimism of k in total, when the model is correct."
        ) as vo:
            intro=label('Two local expansions give the regular AIC optimism term',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def tic(self):
        d = load("tic")
        rows = [
            cmath(r"\text{model wrong}", r":", r"E(\hat\theta - \theta^*)^\top K (\hat\theta - \theta^*) = \mathrm{tr}(J K^{-1})/n", font_size=28),
            cmath(r"\text{TIC}", r"=", r"-2\ell(\hat\theta) + 2\,\mathrm{tr}(\hat J \hat K^{-1})", font_size=30),
            cmath(r"\text{doctor visits, \ Poisson}", r":", rf"\mathrm{{tr}}(\hat J \hat K^{{-1}}) = {d['tic_visits']:.1f}, \ \ k = {d['k']}", font_size=28),
            cmath(r"\text{Poisson data}", r":", rf"{d['tic_poisson']:.2f}", font_size=30),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"Part 22's sandwich: \ $J \ne K$"), why(r"Takeuchi (1976)"),
                why(rf"variance {d['var']:.1f} vs mean {d['mean']:.1f}: \ overdispersed"), why(r"the correct model: \ about $k$")]
        with self.voiceover(
            "<bookmark mark='a'/> AIC's k assumes the model is right. If it isn't, Part 22's sandwich appears: the "
            "quadratic form averages the trace of J times K inverse, where J is the variance of the score and K the "
            "expected curvature. <bookmark mark='b'/> Kei Takeuchi's criterion uses that trace as the penalty. "
            "<bookmark mark='c'/> A Poisson regression for the World's doctor visits, intercept and age, has two "
            "parameters, but Takeuchi's penalty is nine point five, because the visits are far more variable than a "
            "Poisson allows. <bookmark mark='d'/> Fitted to data that really are Poisson, the same trace is one point"
            " eight, close to two. In practice the estimated penalty is noisy and relies on regularity and suitable "
            "independent observations. It corrects an expected log-score bias; it does not repair every model defect."
        ) as vo:
            self.add(simulated_tag())
            intro=label('Misspecified-model curvature changes the predictive penalty',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def aicc(self):
        rows = [
            cmath(r"\text{AICc}", r"=", r"\text{AIC} + \dfrac{2k(k+1)}{n - k - 1}", font_size=32),
            cmath(r"\text{why}", r":", r"\text{the Taylor argument fails when } k/n \text{ is not small}", font_size=30),
            cmath(r"\text{correct Gaussian linear regression}", r":", r"\text{fixed candidate, unknown variance; } n>k+1", font_size=30),
            cmath(r"\text{rule}", r":", r"\text{use AICc unless } n/k > 40", font_size=30),
        ]
        rows[0][2].set_color(AICC)
        whys = [why(r"a small-sample correction"), why(r"AIC then favours too-big models"), why(r"Sugiura (1978)"),
                why(r"Burnham \& Anderson's advice")]
        with self.voiceover(
            "<bookmark mark='a'/> With small samples AIC is itself optimistic about big models. The corrected AICc "
            "adds two k times k plus one over n minus k minus one. <bookmark mark='b'/> The Taylor argument assumes k"
            " is small relative to n; when it isn't, AIC chooses models that are too large. <bookmark mark='c'/> For "
            "correctly specified Gaussian linear regression with unknown variance and n greater than k plus one, this"
            " is an exact correction for each fixed candidate, from Nariaki Sugiura, and Clifford Hurvich and "
            "Chih-Ling Tsai. <bookmark mark='d'/> Kenneth Burnham and David Anderson's advice: use AICc unless n is "
            "more than about forty times k."
        ) as vo:
            intro=label('AICc is model-specific; the Gaussian formula needs residual degrees of freedom',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bench(self):
        d = load("prostate")
        crit = d["crit"]
        mis = [c["aic"] - 2 * (c["size"] + 2) for c in crit]
        k = [c["size"] + 2 for c in crit]
        Bn = CriterionBench(mis, k, [str(c["size"]) for c in crit], penalty_per_k=2.0, width=7.6, height=4.2,
                            center=[-2.0, 0.4, 0], y_max=70, colors={"misfit": TRAIN, "penalty": AICC, "total": PATH})
        xl = label(r"predictors in the best subset of each size", font_size=22, color=GREY_A).next_to(Bn.names, DOWN, buff=0.2)
        best = crit[Bn.stack.best]
        rows = fit_rows(VGroup(
            label(r"Stamey's 67 training men; \ best subset of each size", font_size=22),
            label(r"teal: \ $-2\ell$ above the best fit", font_size=22, color=TRAIN),
            label(r"blue: \ AIC's penalty, \ $2k$", font_size=22, color=AICC),
            label(rf"AIC chooses {best['size']}: \ {', '.join(best['subset'])}", font_size=20, color=PATH),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The model-selection bench, on real data: Stamey's prostate cancer study, "
            "sixty-seven men in the training set, log PSA predicted from eight clinical measures, with the best "
            "subset of each size. <bookmark mark='b'/> Teal is each model's misfit, minus twice its log likelihood "
            "above the best one's; it shrinks as predictors are added. <bookmark mark='c'/> Blue is AIC's penalty, "
            "two per parameter. <bookmark mark='d'/> Their sum is smallest at seven predictors, everything except "
            "gleason. These are searched fits; a penalty based on their coefficient counts alone does not account for"
            " the whole subset-search procedure."
        ) as vo:
            self.add(prostate_tag())
            self.play(FadeIn(Bn.axes_), FadeIn(Bn.names), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in Bn.stack.fit], lag_ratio=0.1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in Bn.stack.pen], lag_ratio=0.1), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(Bn.stack.dots), Create(Bn.stack.ring), FadeIn(rows[3]))
        self.clear_scene()

    def deltas(self):
        d = load("prostate")
        crit = d["crit"]
        aic = np.array([c["aic"] for c in crit])
        dl = aic - aic.min()
        order = np.argsort(dl)
        hdr = [r"\textbf{size}", r"\textbf{$\Delta$AIC}", r"\textbf{Akaike weight}", r"\textbf{relative support: best / candidate}"]
        w = np.exp(-dl / 2)
        w /= w.sum()
        body = [[f"{crit[i]['size']}", f"{dl[i]:.1f}", f"{w[i]:.2f}", f"{np.exp(dl[i] / 2):.1f}"] for i in order[:6]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.28, colors=[GREY_A] + [None] * 6)
        for r in tb[1:]:
            r[1].set_color(AICC)
        tb.move_to([0, 0.7, 0])
        foot = fit_rows(VGroup(
            label(r"compare the same observations and likelihood scale; \ searched fits add selection optimism", font_size=22),
            label(r"Burnham \& Anderson: \ $\Delta < 2$, \ substantial support; \ $4$--$7$, \ less; \ $> 10$, \ essentially none", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> AIC differences are meaningful for comparable likelihoods on the same data and "
            "response scale. The absolute value depends on the likelihood convention. Here are the six best sizes, "
            "ranked by their difference from the best. <bookmark mark='b'/> Six predictors are half a unit behind "
            "seven, four a little over one, five and eight under two. Burnham and Anderson's rule of thumb: models "
            "within two of the best have substantial support, those four to seven behind considerably less, and those"
            " more than ten behind essentially none. Five models here are within two: AIC has a favourite, but not a "
            "winner."
        ) as vo:
            self.add(prostate_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tb[1:]], lag_ratio=0.3), FadeIn(foot[1]), run_time=3.0)
        self.clear_scene()
