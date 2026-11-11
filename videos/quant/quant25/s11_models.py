from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant25.common import BAD, GOOD, HURDLE, NOISE, PART, SDF, TRUE, ask, fit_right, illustration, load


class Models(VoiceoverScene):
    def construct(self):
        m = load("models")
        self.card()
        self.insight()
        self.mislead()
        self.named(m)
        self.scatter(m)
        self.top(m)
        self.ff2018()
        self.bayes()
        self.lesson()

    def card(self):
        c = chapter_card(10, r"Comparing models", r"Which factor model is best, and how would you know?", lit=(2018,),
                         part=PART)
        with self.voiceover("Chapter ten. Not whether a model is true, but which of several is best."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def insight(self):
        rows = [cmath(r"\text{GRS}(f; R)", r"\propto", r"SR^2(f, R) - SR^2(f)", font_size=40, colors={r"\text{GRS}(f; R)": BAD}),
                cmath(r"f_A \succ_{\rm MV} f_B", r"\iff", r"SR^2(f_A) > SR^2(f_B)", font_size=42, colors={r"f_A \succ_{\rm MV} f_B": GOOD})]
        whys = [why('With matching moments and unrestricted weights, the squared-Sharpe gain measures the conditional mean-alpha gap. GRS also has model-specific finite-sample scaling; preserved proxies are not exact tests'),
                why('Barillas and Shanken (2017, 2018): traded-factor comparison can use the factors themselves. On a common union and consistent moments, higher attainable squared Sharpe leaves a smaller mean-variance gap; this is not universal model truth or exact payoff spanning')]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Part twenty-four related conditional mean alpha to the gain in maximum squared Sharpe. This needs matching moments and unrestricted portfolio weights; the finite-sample GRS statistic also has model-specific scaling. <bookmark mark='a'/> Barillas and Shanken show how traded-factor models can be compared using the factors themselves. For a common union opportunity set and consistent moments, the factors with higher attainable squared Sharpe leave a smaller mean-variance gap. That criterion does not prove a risk-based explanation, exact payoff spanning, superiority for every constrained investor, or a fresh out-of-sample winner. Estimation and model selection uncertainty remain."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def mislead(self):
        cards = VGroup(
            desk_question(r"test assets built from a model's own sorts", r"the 25 size--value portfolios flatter the "
                          r"three-factor model, because SMB and HML were built from the same sorts", width=12.0, font_size=20),
            desk_question(r"assets with a strong factor structure", r"Lewellen, Nagel and Shanken: almost any factor "
                          r"correlated with size and value 'prices' the 25 portfolios with a high cross-sectional $R^2$",
                          width=12.0, font_size=20),
            desk_question(r"the remedy", r"compare traded-factor models by the Sharpe ratio their factors reach, and test "
                          r"on assets the modeller did not choose", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Why can test assets mislead? <bookmark mark='a'/> When they are built from a model's own sorts, they "
            "flatter it: the twenty-five size and value portfolios suit the three-factor model because its factors "
            "were built from the same sorts. <bookmark mark='b'/> And when the assets have a strong factor structure, "
            "almost any factor correlated with that structure appears to price them, with a high R squared, as "
            "Lewellen, Nagel and Shanken showed with deliberately meaningless factors. <bookmark mark='c'/> The "
            "remedy is the Sharpe-ratio comparison, and test assets the modeller did not choose."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def named(self, m):
        nm = m["named"]
        order = ["CAPM", "FF3", "Carhart", "FF5", "FF6", "q4", "q5"]
        hx = [-4.4, -1.6, 0.8, 3.4]
        heads = [r"model", r"$SR^2$, 1967--1993", r"$SR^2$, 1967--2020", r"Sharpe, 1994--2020"]
        tab = VGroup(VGroup(*[label(h_, font_size=17, color=GREY_A).move_to([x, 2.6, 0]) for h_, x in zip(heads, hx)]))
        names = {"CAPM": r"CAPM", "FF3": r"Fama--French 3", "Carhart": r"Carhart 4", "FF5": r"Fama--French 5",
                 "FF6": r"Fama--French 5 + UMD", "q4": r"q-factor (4)", "q5": r"q5 (+ expected growth)"}
        for i, k in enumerate(order):
            r_ = nm[k]
            y = 2.0 - 0.55 * i
            tab.add(VGroup(label(names[k], font_size=18).move_to([hx[0], y, 0]),
                           MathTex(f"{r_['sh2_in']:.2f}", font_size=24).move_to([hx[1], y, 0]),
                           MathTex(f"{r_['sh2_full']:.2f}", font_size=24).move_to([hx[2], y, 0]),
                           MathTex(f"{r_['sr_out']:.2f}", font_size=24, color=GOOD if r_["sr_out"] > 0.6 else WHITE).move_to(
                               [hx[3], y, 0])))
        foot = wrapped_label(r"annualised. The squared Sharpe ratio of each model's tangency portfolio, in the first half "
                             r"and over the whole window; and the Sharpe ratio of the first half's tangency weights held "
                             r"through the second half. q5 leads, mostly through its expected-growth factor", 12.0, 16,
                             GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The table preserves seven named models on the same observed calendar. <bookmark mark='a'/> Maximum squared Sharpe uses sample covariance with denominator T minus one, in the earlier window and the full window. <bookmark mark='b'/> The later-window column holds the earlier tangency weights fixed but uses standard deviation with denominator T. These finite-sample conventions differ. Modern published factors, especially expected growth, are backfilled histories rather than reconstructed historical forecasts. The saved ranking is conditional evidence about this panel, not a historically blind contest."
        ) as vo:
            self.play(FadeIn(tab[0]), *[FadeIn(r_[0]) for r_ in tab[1:]])
            vo.wait_until("a")
            self.play(*[FadeIn(r_[1:3]) for r_ in tab[1:]])
            vo.wait_until("b")
            self.play(*[FadeIn(r_[3]) for r_ in tab[1:]], FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def scatter(self, m):
        g = axes([0, 9], [-0.2, 1.8], x_length=7.0, y_length=4.4, xlabel=r"$SR^2$ in 1967--1993", ylabel=r"Sharpe ratio, "
                 r"1994--2020", xticks=[0, 2, 4, 6, 8], yticks=[0, 0.5, 1.0, 1.5], font_size=13).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        allm = m.get("all")
        side = VGroup(
            MathTex(rf"{m['n_models']}\ \text{{models}}", font_size=26),
            MathTex(rf"\text{{rank correlation}}:\ {m['rank_corr']:.2f}", font_size=24, color=GOOD),
            wrapped_label('every subset of ten factors (Fama--French five, momentum, and the four q-factors beyond the market) that includes the market, up to six factors. retrospective rank association on selected backfilled histories; choosing later-window leaders uses the evaluation window itself',
                          3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.04, color=SDF, fill_opacity=0.7)
                        for x, y in allm])
        with self.voiceover(
            "The original search considers ten factor columns, including expected growth. Market is mandatory and a model may contain at most six factors, giving three hundred and eighty-two candidate subsets. <bookmark mark='a'/> Each dot compares earlier-window attainable squared Sharpe with later returns from the earlier fitted weights. Every candidate shares the selected modern factor histories.  The scatter shows estimation and ranking uncertainty. Picking the later-window leader uses those same evaluation outcomes, so its reported performance is selected rather than a fresh validation."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.05), FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def top(self, m):
        hx = [-2.4, 2.4, 4.8]
        tab = VGroup(VGroup(label(r"best five in sample", font_size=18, color=GREY_A).move_to([hx[0], 2.4, 0]),
                            label(r"$SR^2$ in", font_size=18, color=GREY_A).move_to([hx[1], 2.4, 0]),
                            label(r"Sharpe out", font_size=18, color=GREY_A).move_to([hx[2], 2.4, 0])))
        for i, r_ in enumerate(m["top_in"][:5]):
            y = 1.8 - 0.5 * i
            tab.add(VGroup(label(r", ".join(r_["model"]), font_size=17).move_to([hx[0], y, 0]),
                           MathTex(f"{r_['sh2_in']:.2f}", font_size=22).move_to([hx[1], y, 0]),
                           MathTex(f"{r_['sr_out']:.2f}", font_size=22).move_to([hx[2], y, 0])))
        foot = wrapped_label(r"every top model mixes families: size, a profitability factor, an investment factor, expected "
                             r"growth. No published model is in the top five; their pieces are", 12.0, 17,
                             GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "The table ranks candidates by the earlier fitting window and retains their saved later-window results. <bookmark mark='a'/> The search family contains three hundred and eighty-two subsets of ten columns, with market mandatory and no more than six factors.  A separate top-out list chooses on the later window itself. Its winner is selected on that window, while even the earlier-ranked list inherits backfilled published-factor construction. Neither ranking is a posterior probability that a model is true, an exact spanning test, or a cost-adjusted investment recommendation."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def ff2018(self):
        rows = [cmath(r"SR^2(\text{MKT, SMB, HML, RMW}_{cp}, \text{CMA, UMD})", r">", r"SR^2(\text{FF5})", font_size=36,
                      colors={r"SR^2(\text{MKT, SMB, HML, RMW}_{cp}, \text{CMA, UMD})": GOOD})]
        whys = [why(r"Fama and French (2018), 'Choosing factors', used exactly this criterion on their own models: adding "
                    r"momentum, and measuring profitability with cash rather than accounting earnings, raised the squared "
                    r"Sharpe ratio. They warned that the gains are small and partly in-sample, and kept the five-factor "
                    r"model as a benchmark")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "Fama and French used the same criterion on their own models. In 'Choosing factors' they found that "
            "adding momentum, and measuring profitability with cash flows rather than accounting earnings, raised the "
            "squared Sharpe ratio. And they warned that such gains are small and partly in sample, the same caution "
            "the near-ties above demand."
        ) as vo:
            step(0)
        self.wait(0.4)
        self.clear_scene()

    def bayes(self):
        rows = [cmath(r"\Pr(\mathcal M_j \mid \text{data})", r"=", r"\frac{\Pr(\text{data} \mid \mathcal M_j)\,\Pr(\mathcal M_j)}"
                      r"{\sum_k \Pr(\text{data} \mid \mathcal M_k)\,\Pr(\mathcal M_k)}", font_size=38,
                      colors={r"\Pr(\mathcal M_j \mid \text{data})": SDF})]
        whys = [why('Bayesian marginal likelihood and model averaging are conditional on priors, likelihood and candidate set. Published large-space findings do not certify a universal dense SDF or an unconditional true-model probability')]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            'Bayesian model comparison places a prior over models and their parameters, then weights them by marginal likelihood under a specified return model. Published work explores very large model spaces and model averaging. Those probabilities are conditional on priors, likelihood, candidate set and observed selection; they are not unconditional probabilities of economic truth. Isotropic ridge is a continuous shrinkage estimate and is not automatically the same operation as averaging a discrete subset model space. No new Bayesian market comparison is fitted here.'
        ) as vo:
            step(0)
        self.wait(0.4)
        self.clear_scene()

    def lesson(self):
        cards = VGroup(
            desk_question(r"compare by Sharpe, not by test assets", 'common-union traded-factor mean-variance comparison needs consistent moments and unrestricted weights; test-asset choice can mislead', width=12.0, font_size=20),
            desk_question(r"average, do not choose", 'near ties motivate uncertainty analysis and prespecified averaging or shrinkage; neither method automatically wins future performance', width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Two conditional lessons. <bookmark mark='a'/> Compare traded-factor mean-variance opportunity sets on consistent moments and a common union, while retaining estimation, publication and selection uncertainty. <bookmark mark='b'/> Near ties can motivate prespecified shrinkage or averaging, but weights, priors and validation remain choices. Neither discrete model averaging nor ridge automatically wins out of sample, and choosing among them after the same evaluation requires fresh evidence."
        ) as vo:
            for i, mk in enumerate(("a", "b")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"model A beats model B on the 25 size--value portfolios, but B's factors reach a higher squared Sharpe "
                r"ratio. Which is better, and why can the test assets mislead?")
        with self.voiceover("Model A beats model B on the twenty-five size and value portfolios, but B's factors reach a "
                            "higher squared Sharpe ratio. Which is better, and why can the test assets mislead?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
