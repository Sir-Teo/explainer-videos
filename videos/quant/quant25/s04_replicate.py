from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant25.common import BAD, GOOD, HURDLE, NOISE, PART, SDF, TRUE, ask, fit_right, illustration, load


class Replicate(VoiceoverScene):
    def construct(self):
        z = load("zoo")
        self.card()
        self.crisis()
        self.osap()
        self.howto()
        self.scatter(z)
        self.choices()
        self.microcaps()
        self.jkp()

    def card(self):
        c = chapter_card(3, r"Replication and open-source asset pricing", r"If you rebuild a published factor, do you get "
                         r"the paper's result?", lit=(2020, 2022, 2023), part=PART)
        with self.voiceover("Chapter three. Does the zoo replicate? Two famous answers that disagree, and the open data "
                            "that lets anyone check."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def crisis(self):
        cc = crisis_card(r"2020", r"Replicating anomalies",
                         r"Hou, Xue and Zhang rebuilt 452 anomalies with one common method: NYSE breakpoints, so that "
                         r"microcaps do not set the portfolios, and value weights. 65\% failed to reach $|t| = 1.96$, "
                         r"including 96\% of the trading-frictions anomalies; with a hurdle of 2.78, 82\% failed. The "
                         r"survivors' magnitudes were much smaller than originally reported",
                         stats=[(r"65\%", r"fail $|t| \ge 1.96$"), (r"82\%", r"fail $|t| \ge 2.78$")], width=8.8,
                         font_size=20)
        with self.voiceover(
            "In 2020 Kewei Hou, Chen Xue and Lu Zhang rebuilt four hundred and fifty-two anomalies with one common "
            "recipe: breakpoints from the New York Stock Exchange, so that tiny stocks do not dominate, and value "
            "weights. <bookmark mark='a'/> Sixty-five percent failed to reach a t-statistic of two, almost all of the "
            "anomalies based on trading frictions among them. With a hurdle of two point eight, eighty-two percent "
            "failed. A replication crisis, it seemed, like psychology's."
        ) as vo:
            self.play(FadeIn(cc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(cc, color=BAD, scale_factor=1.03))
        self.add(illustration(r"Hou, Xue and Zhang, Review of Financial Studies (2020), abstract"))
        self.wait(0.4)
        self.clear_scene()

    def osap(self):
        cards = VGroup(
            desk_question(r"open source", r"Chen and Zimmermann (2022): code and data for over 200 predictors, each rebuilt "
                          r"as its original paper built it: the same weighting, breakpoints, sample and holding period",
                          width=12.0, font_size=20),
            desk_question(r"two questions, not one", r"'does the paper's own result reproduce?' (Chen and Zimmermann) and "
                          r"'does the effect survive a common, conservative method?' (Hou, Xue and Zhang)", width=12.0,
                          font_size=20),
            desk_question(r"why it matters", r"anyone can now check a claim, extend it, and count the predictors: the "
                          r"zoo has a census", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Andrew Chen and Tom Zimmermann answered differently. <bookmark mark='a'/> They published open-source code "
            "and data for more than two hundred predictors, each rebuilt exactly as its original paper built it, with "
            "the paper's own weighting, breakpoints and sample. <bookmark mark='b'/> That separates two questions that "
            "had been merged: does the paper's own result reproduce, and does the effect survive a common, "
            "conservative method? <bookmark mark='c'/> And it gives the zoo a census anyone can check. It is the data "
            "this part uses."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def howto(self):
        cards = VGroup(
            desk_question(r"the returns", r"one column per predictor: the long--short portfolio as its paper built it, "
                          r"monthly, from 1926 where the data allow, in percent", width=12.0, font_size=20),
            desk_question(r"the documentation", r"for each predictor: authors, journal, year, the paper's sample and "
                          r"$t$-statistic, the weighting and quantiles, the data category, and notes on any differences",
                          width=12.0, font_size=20),
            desk_question(r"what it allows", 'original-paper sample years and next-calendar-year post-publication windows, computed the same way: the decay, the tests and the SDF of this part', width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "The public release contains monthly predictor returns and documentation. <bookmark mark='a'/> Each return column follows the documented published strategy, with reconstruction differences and modern data revisions. <bookmark mark='b'/> The metadata include publication year, original sample years and reported t-statistic. The original-sample mask uses those years, without an extra December 2020 cap. <bookmark mark='c'/> The post-publication mask begins in the following calendar year, ends by December 2020 and requires twenty-four finite months. These are published, selected predictors. Later chapters additionally select a complete-history universe using observations through 2023, so none of these labels reconstructs a pristine real-time research process."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def scatter(self, z):
        r = [x for x in z["recs"] if x["t_op"]]
        a, b = np.array([x["t_op"] for x in r]), np.array([x["t_in"] for x in r])
        g = axes([0, 17], [-2.5, 15.5], x_length=6.4, y_length=4.6, xlabel=r"$t$ reported in the original paper",
                 ylabel=r"$t$ reproduced, original sample", xticks=[0, 4, 8, 12, 16], yticks=[-2, 0, 4, 8, 12, 15],
                 font_size=13).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.045,
                            color=TRUE if y > 1.96 else BAD, fill_opacity=0.8) for x, y in zip(a, b)])
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(15, 15), color=GREY_B, stroke_width=1.5)
        h = DashedLine(ax.c2p(0, 1.96), ax.c2p(17, 1.96), color=HURDLE, stroke_width=1.5)
        side = VGroup(
            MathTex(rf"\text{{reproduced}}\ t > 1.96:\ {100 * np.mean(b > 1.96):.0f}\%", font_size=24, color=TRUE),
            MathTex(rf"\text{{median ratio}}:\ {np.median(b / a):.2f}", font_size=24),
            MathTex(rf"\text{{correlation}}:\ {np.corrcoef(a, b)[0, 1]:.2f}", font_size=24),
            wrapped_label(r"each dot a predictor with a reported $t$ (188). Most land a little below the diagonal: the "
                          r"same signal, rebuilt from the same kind of data, usually comes out slightly weaker than "
                          r"published", 3.4, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Here is the first question answered. Each dot is a predictor: the t-statistic its paper reported, against "
            "the one Chen and Zimmermann get rebuilding it. <bookmark mark='a'/> Eighty-eight percent reproduce a "
            "t-statistic above two. Most land a little below the diagonal, typically at about nine tenths of the "
            "published value: rebuilt from today's version of the data, a signal usually comes out slightly weaker "
            "than its authors reported. The papers mostly describe what is in the data. Whether it is a premium is a "
            "different question."
        ) as vo:
            self.play(FadeIn(g), Create(diag), Create(h))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.01), FadeIn(side), run_time=2.5)
        self.add(illustration(r"Open Source Asset Pricing 2024.10: SignalDoc and long--short returns"))
        self.wait(0.4)
        self.clear_scene()

    def choices(self):
        rows = [cmath(r"\text{result}", r"=", r"f(\text{signal},\ \text{weights},\ \text{breakpoints},\ \text{microcaps},\ "
                      r"\text{sample},\ \text{holding})", font_size=34, colors={r"\text{result}": BAD})]
        whys = [why(r"most of the gap between the two answers is construction: equal weights and all-stock breakpoints let "
                    r"thousands of microcaps, a few percent of the market's value, drive the result. Value weights and "
                    r"NYSE breakpoints shrink many anomalies toward zero, especially those based on trading frictions, "
                    r"which live in illiquid stocks (Part 26's costs)")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "So why did Hou, Xue and Zhang find failure? Mostly construction. A result depends on the signal and also "
            "on the weights, the breakpoints, the treatment of microcaps, the sample and the holding period. Equal "
            "weights with breakpoints from all stocks let thousands of microcaps, a few percent of the market's value, "
            "drive the result. With value weights and exchange breakpoints, many anomalies shrink toward zero, above "
            "all those based on trading frictions, which live in the stocks that are hardest to trade."
        ) as vo:
            step(0)
        self.wait(0.4)
        self.clear_scene()

    def microcaps(self):
        rows = [cmath(r"\text{microcaps}", r"=", r"\text{below the NYSE 20th size percentile}", font_size=40,
                      colors={r"\text{microcaps}": BAD}),
                cmath(r"\approx 60\%\ \text{of stocks}", r"\leftrightarrow", r"\approx 3\%\ \text{of market value}", font_size=40)]
        whys = [why(r"Fama and French (2008), 'Dissecting anomalies': the smallest stocks, by NYSE breakpoints, are most of "
                    r"the stocks in the sample and almost none of its value"),
                why(r"in an equal-weighted sort they are most of each portfolio; in a value-weighted one they barely count. "
                    r"Their bid--ask spreads and borrowing costs are also the largest, so a premium that lives there is the "
                    r"hardest to collect")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "How much do microcaps matter? Eugene Fama and Kenneth French defined them as stocks below the twentieth "
            "percentile of exchange-listed size. <bookmark mark='a'/> They are about three in five of all stocks and "
            "about three percent of the market's value. In an equal-weighted portfolio they are most of the holdings; "
            "value-weighted, they barely count. They also have the widest spreads and the hardest borrowing, so a "
            "premium that lives in them is the hardest to collect."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def jkp(self):
        cards = VGroup(
            desk_question(r"Jensen, Kelly and Pedersen (2023)", r"153 factors in 93 countries; a Bayesian model of "
                          r"replication. Most factors replicate (on CAPM alphas, not raw returns), cluster into 13 themes, "
                          r"and work out of sample abroad", width=12.0, font_size=20),
            desk_question(r"the decomposition", r"the gap to 35\% comes from the test (alphas against raw returns), from "
                          r"multiple-testing adjustments that ignore the factors' common themes, and from the hurdle",
                          width=12.0, font_size=20),
            desk_question(r"and more factors help", r"in their model, evidence that many related factors work strengthens "
                          r"each one: a zoo of cousins is evidence for the family", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Then the counter-argument. <bookmark mark='a'/> Theis Jensen, Bryan Kelly and Lasse Pedersen built a "
            "hundred and fifty-three factors in ninety-three countries and a Bayesian model of replication. Most "
            "factors replicate, measured by their CAPM alphas; they cluster into thirteen themes; and they work out of "
            "sample abroad. <bookmark mark='b'/> They traced the gap with Hou, Xue and Zhang to the choice of test, to "
            "corrections that treat related factors as unrelated, and to the hurdle. <bookmark mark='c'/> And in "
            "their model, many related factors working is evidence for each of them: a zoo of cousins supports the "
            "family. Both papers are careful. They answer different questions."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"an anomaly has $t = 4$ equal-weighted and $t = 1.2$ value-weighted with NYSE breakpoints. Is it real? "
                r"Would you trade it, and how big?")
        with self.voiceover("An anomaly has a t-statistic of four equal-weighted, and one point two value-weighted with "
                            "exchange breakpoints. Is it real? Would you trade it, and how big?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
