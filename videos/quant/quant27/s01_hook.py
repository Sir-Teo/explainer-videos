from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import (BAD, COIN, COMPLEX, GOOD, HURDLE, LINEAR, MOM, NET, PART, TREE, era_strip,
                                         fit_right, illustration, load)


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.headline()
        self.paradox(load("snr"))
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Machine Learning for Returns")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part twenty-seven. Machine learning for returns: what models with thousands or millions of parameters can "
            "learn from prices, what they cannot, and how to tell the difference."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def headline(self):
        card = firm_card(r"Gu, Kelly and Xiu (2020)", r"`Empirical asset pricing via machine learning': about 30,000 US "
                         r"stocks, 1957--2016, 94 characteristics each and their interactions; linear models, trees and "
                         r"neural networks trained on 18 years, tuned on 12, tested on the 30 after"
                         .replace("30,000", "30{,}000"),
                         numbers=((r"0.40\%", r"a month: the best network's out-of-sample $R^2$"),
                                  (r"1.35", r"Sharpe ratio, value-weighted long-short"),
                                  (r"2.45", r"equal-weighted"), (r"0.61", r"the same strategy from OLS")),
                         source=r"Gu, Kelly and Xiu, \textit{Review of Financial Studies} 33 (2020)", kind=r"Paper file",
                         width=10.6, font_size=22)
        card.move_to(ORIGIN)
        with self.voiceover(
            "In 2020 Shihao Gu, Bryan Kelly and Dacheng Xiu published the paper that brought machine learning into "
            "mainstream asset pricing. About thirty thousand American stocks, sixty years, ninety-four characteristics "
            "each. <bookmark mark='a'/> Their best neural network explained four tenths of one percent of the variance "
            "of a stock's monthly return. Ninety-nine point six percent was left unexplained. <bookmark mark='b'/> And "
            "yet a portfolio that bought the stocks it liked best and sold those it liked least earned a Sharpe ratio "
            "of one point three five with value weights, and two point four five with equal weights, more than twice "
            "what the same strategy earned from a linear regression."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def paradox(self, s):
        r2 = np.asarray(s["r2"]) * 100
        g = axes([0, 5], [0, 4.0], x_length=7.4, y_length=4.2, xlabel=r"monthly predictive $R^2$, \%",
                 ylabel=r"the Sharpe ratio it can buy, annualised", xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 1, 2, 3, 4],
                 font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        lines = [curve(ax, r2, np.asarray(s["single"]), MOM, stroke_width=3)]
        cols = {"10": TREE, "100": NET, "1000": COMPLEX}
        for n_, c in cols.items():
            y = np.asarray(s["breadth"][n_])
            k = y <= 4.0
            lines.append(curve(ax, r2[k], y[k], c, stroke_width=3))
        leg = legend([(MOM, r"timing one asset"), (TREE, r"10 independent bets a month"),
                      (NET, r"100"), (COMPLEX, r"1{,}000")], font_size=15)
        side = VGroup(leg, MathTex(rf"R^2 = 1\%:\ SR = {s['sr_at_1pct']:.2f}\ \text{{for one asset}}", font_size=22,
                                   color=MOM),
                      wrapped_label(r"$SR \approx \sqrt{12\,n\,R^2/(1 - R^2)}$ for $n$ independent bets a month. A "
                                    r"forecast that is almost always wrong about any one asset can be right on average "
                                    r"about a thousand", 3.5, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        side.to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "How can so little explanation earn so much? <bookmark mark='a'/> Time one asset with a forecast whose R "
            "squared is one percent a month, and the best Sharpe ratio you can expect is about a third. "
            "<bookmark mark='b'/> But spread the same weak forecast across many assets whose errors are independent, "
            "and the Sharpe ratio grows with the square root of the number of bets. A hundred bets a month at one "
            "percent each is worth more than three. That is the arithmetic every quantitative equity fund lives on: "
            "almost always wrong about any one stock, right on average about a thousand."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(*[Create(l_) for l_ in lines[1:]], FadeIn(side[0]), FadeIn(side[2]), run_time=2.5)
        self.add(illustration(r"the fundamental law of active management (Grinold 1989), as arithmetic"))
        self.wait(0.4)
        self.clear_scene()

    def history(self):
        I, C = QC.IDEA, QC.CRISIS
        entries = [(1986, r"backpropagation", I), (1996, r"the lasso", I), (2001, r"random forests; boosting", I),
                   (2007, r"random features", I), (2012, r"deep nets win ImageNet", I), (2017, r"the transformer", I),
                   (2018, r"Lopez de Prado's toolkit", I), (2019, r"double descent", I),
                   (2020, r"Gu--Kelly--Xiu", I), (2021, r"autoencoder pricing", I), (2023, r"images of prices", I),
                   (2024, r"virtue of complexity; deep SDFs", I), (2025, r"Nagel; AIPM; Kronos", I)]
        strip = era_strip(entries, y0=1983, y1=2027, font_size=13).move_to(DOWN * 0.3)
        head = label(r"Machine learning reaches the cross-section", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 6), (6, 10), (10, 13)]
        with self.voiceover(
            "The tools are older than the finance. Backpropagation was popularised in 1986; the lasso came in 1996; "
            "random forests and gradient boosting in 2001; random features in 2007; and in 2012 deep networks began "
            "winning at images, and in 2017 the transformer arrived. <bookmark mark='a'/> Marcos Lopez de Prado's "
            "practitioner's toolkit appeared in 2018, double descent was named in 2019, and in 2020 Gu, Kelly and Xiu "
            "brought the whole repertoire to the cross-section of stock returns. <bookmark mark='b'/> Since then: "
            "autoencoders, images of price charts, models with more parameters than observations, adversarial "
            "discount factors and transformers across assets; and, in 2025, a forceful critique and the first "
            "foundation models trained on market data."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), m in zip(groups, [None, "a", "b"]):
                if m:
                    vo.wait_until(m)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.6)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Why returns are a low signal-to-noise problem, and what that does to every model",
            r"The model zoo on a survivorship-free coin panel: linear, trees, networks; where the edge lives",
            r"The virtue of complexity, double descent, and the critique that reread them",
            r"For the researcher: Marchenko--Pastur and the exact risk of ridge(less) regression, proved and simulated",
            r"Autoencoders, adversarial SDFs, attention across assets, images of prices",
            r"A pocket foundation model; the practitioner's toolkit; conformal intervals",
            r"Two firms from the public record; the models registered and opened on 2021--2025",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: why return prediction is a problem of tiny signals in loud noise, and what that does to every "
            "model; the whole model zoo, run on every coin Binance has ever listed, dead or alive; where the edge "
            "lives; the virtue of complexity and its critics; the theorem behind both, proved; four modern "
            "architectures; a small foundation model of our own, tested on markets it never saw; the practitioner's tools; intervals with guarantees; two firms "
            "from the public record; and the models, registered and opened on sealed years."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("research",))
        with self.voiceover(
            "In the House, the research desk gets a model shop: every learner in this part, built from scratch, "
            "validated as Part twenty-six demands, and counted. Nothing it produces is believed for its in-sample fit; "
            "only for what it does on data it has not seen."
        ):
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
