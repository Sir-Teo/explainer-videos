from __future__ import annotations

import math

from explainer.quant import *  # noqa: F403
from explainer.quant.house import riskmodel as RM
from videos.quant.quant31.common import BAD, COST_C, GOOD, IC_C, PART, era_strip, load


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.promise()
        self.gap(load("costs"), load("envelope"))
        self.act()
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Risk Models, Costs and Trading Through Time")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part thirty-one. Risk models, costs and trading through time: what a forecast is worth once it has to be "
            "held, measured against a risk model, and traded at a price."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def promise(self):
        naive = RM.fundamental_ir(0.05, 500 * 12)
        per = RM.ir_time_varying(0.05, 0.10, 500)
        real = per * math.sqrt(12)
        left = VGroup(label(r"the fundamental law promises", font_size=24, color=IC_C),
                      MathTex(rf"IR = 0.05\sqrt{{500\times 12}} = {naive:.2f}", font_size=40, color=IC_C)
                      ).arrange(DOWN, buff=0.3)
        right = VGroup(label(r"if the IC itself has a standard deviation of 0.10", font_size=24, color=BAD),
                       MathTex(rf"IR = {real:.2f}", font_size=40, color=BAD)).arrange(DOWN, buff=0.3)
        g = VGroup(left, right).arrange(DOWN, buff=1.0).move_to(UP * 0.3)
        foot = wrapped_label(r"an information coefficient of 0.05, 500 stocks, rebalanced monthly; annual information "
                             r"ratios; the second line is proved in the research chapter", 11.0, 17,
                             GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "A forecast whose rank correlation with next month's returns is five percent: modest skill. Five hundred "
            "stocks, rebalanced monthly. <bookmark mark='a'/> The most quoted formula in active management says the "
            f"information ratio should be {naive:.2f} a year, against the half that Grinold and Kahn call good and the one they "
            "call exceptional. "
            "<bookmark mark='b'/> Now let that five percent wander from month to month, with a standard deviation of ten "
            f"percent, as real forecasts do. The information ratio falls to {real:.2f}. Same average skill, less than "
            "half the reward."
        ) as vo:
            self.play(FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(left, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(right, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def gap(self, c, e):
        cur = {r["aum"]: r["sharpe"] for r in c["curve"]}
        rows = VGroup(
            VGroup(label(r"the time-varying IC", font_size=24, color=IC_C),
                   label(r"the research chapter: an exact formula, checked on the coins", font_size=19, color=GREY_B)),
            VGroup(label(r"costs", font_size=24, color=COST_C),
                   label(rf"one calm-coin signal: Sharpe {c['gross_sharpe']:.2f} gross, {cur[1e5]:.2f} at \$100{{,}}000, "
                         rf"{cur[1e6]:.2f} at \$1 million", font_size=19, color=GREY_B)),
            VGroup(label(r"the risk model itself", font_size=24, color=BAD),
                   label(r"a rule that divides by a forecast variance near zero (Chapter 11)", font_size=19, color=GREY_B)),
        )
        for r_ in rows:
            r_.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(DOWN * 0.1)
        head = label(r"Where the information ratio goes", font_size=32).to_edge(UP, buff=0.6)
        with self.voiceover(
            "This part follows the information ratio from the forecast to the account, and counts what it loses on the "
            "way. <bookmark mark='a'/> First to the forecast's own instability. <bookmark mark='b'/> Then to costs: one "
            f"signal on the coins earns a Sharpe ratio of {c['gross_sharpe']:.2f} before costs, {cur[1e5]:.2f} traded "
            f"with a hundred thousand dollars, and {cur[1e6]:.2f} with a million. <bookmark mark='c'/> And to the risk "
            "model itself: the rule this part registers, opened on five sealed years, failed in a way that teaches how "
            "risk models must be used."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def act(self):
        smap = series_map(current=PART, done=PART - 1)
        with self.voiceover(
            "Where this sits. Part thirty chose weights from estimated means and covariances, once. This part makes the "
            "problem real: the covariance comes from a factor risk model, the weights must be traded, trading costs "
            "money, and the forecasts move while you trade toward them. It is the part of the series closest to what a "
            "systematic desk does every morning: forecast, measure risk, price the trades, and decide how far to move. "
            "Every one of those steps is computed here, on real data, and checked."
        ):
            self.play(FadeIn(smap))
            self.wait(1.0)
        self.clear_scene()

    def history(self):
        I = QC.IDEA
        entries = [(1973, r"Vasicek's betas", I), (1974, r"Rosenberg: factor risk", I), (1989, r"the fundamental law", I),
                   (1997, r"the square-root law", I), (2000, r"Almgren--Chriss", I), (2002, r"the transfer coefficient", I),
                   (2004, r"Berk--Green; a moving IC", I), (2007, r"the quant quake", I),
                   (2013, r"Garleanu--Pedersen", I), (2016, r"anomalies after costs", I), (2017, r"multi-period convex", I),
                   (2018, r"AQR's trading costs", I)]
        strip = era_strip(entries, y0=1970, y1=2022, font_size=12, step=10).move_to(DOWN * 0.3)
        head = label(r"Fifty years of holding a forecast", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 3), (3, 8), (8, 12)]
        with self.voiceover(
            "Oldrich Vasicek showed in 1973 how to shrink an estimated beta; Barr Rosenberg built the first commercial "
            "factor risk models around the same time; and in 1989 Richard Grinold wrote down the fundamental law. "
            "<bookmark mark='a'/> Then the price of trading: the square-root law of market impact, Almgren and Chriss's "
            "optimal execution, the transfer coefficient, Berk and Green's model of why a manager's skill does not reach the "
            "investors, the "
            "information ratio with a moving IC, and the August 2007 quant quake. <bookmark mark='b'/> And the modern "
            "answers: Garleanu and Pedersen's dynamic trading, the anomalies that do not survive costs, convex "
            "multi-period optimization, and AQR's measurement of its own trading costs."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), mk in zip(groups, [None, "a", "b"]):
                if mk:
                    vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.6)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"The fundamental law, the transfer coefficient, and what breadth means",
            r"Factor risk models: exposures, cross-sectional regressions, the bias statistic",
            r"Specific risk and Bayesian betas",
            r"Transaction costs: the square-root law and capacity",
            r"Trading toward a moving target: Garleanu and Pedersen; multi-period optimization",
            r"Alpha combination, decay, crowding and August 2007; P\&L attribution",
            r"For the researcher: the information ratio when the IC moves, exactly",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: the fundamental law and its corrections; how a factor risk model is built and how to test it; "
            "specific risk and shrunk betas; the square-root law of costs, and capacity; trading toward a target that "
            "moves, from Garleanu and Pedersen to multi-period optimization; combining signals; decay, crowding and the "
            "quant quake; attribution; a registered rule opened on sealed years; and an exact formula for the "
            "information ratio when the IC moves."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("portfolio",))
        with self.voiceover(
            "In the House, the portfolio and risk desk gets its risk model, its cost model and its trading rule, and the "
            "arrow from the portfolio desk to execution is drawn for the first time with a price on it."
        ):
            self.play(FadeIn(chart))
        self.wait(0.3)
        self.clear_scene()
