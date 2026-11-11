from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import factors as FA
from videos.quant.quant24.common import BAD, FCOL, GOOD, HML, PART, UMD, house_lab, load


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("race"), load("crash"), load("everywhere"), load("valuedecade"))
        self.lab()
        self.module()
        self.test()

    def card(self):
        c = chapter_card(14, r"Rule 24: the factor library", r"What must the House know before it holds a factor?",
                         part=PART)
        with self.voiceover("Chapter fourteen. The House's twenty-fourth rule, and the factor library it opens for the "
                            "research desk."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, r, c, e, v):
        rows = [(r"momentum: Sharpe ratio, skewness, worst month", rf"{c['raw']['sharpe']:.2f},\ {c['raw']['skew']:.1f},\ "
                                                                rf"{100 * c['raw']['worst']:.0f}\%", UMD),
                ('momentum: lagged monthly-volatility rule', rf"{c['scaled']['sharpe']:.2f},\ {c['scaled']['skew']:.1f},\ "
                                                          rf"{100 * c['scaled']['worst']:.0f}\%", GOOD),
                (r"value, 2007--2020", rf"{100 * v['stats_0720']['mean']:.1f}\%\ \text{{a year}},\ "
                                       rf"{100 * v['dd']['max']:.0f}\%\ \text{{drawdown}}", HML),
                (r"value and momentum, all markets: correlation", rf"{e['global']['corr']:.2f}", BAD),
                (r"their 50/50 mix: Sharpe ratio", rf"{e['global']['combo']['sharpe']:.2f}", QC.HOUSE),
                (r"registration and holdout accounting", r"\text{conceptual; sealed experiment excluded}", QC.HOUSE)]
        hx = [-2.2, 3.8]
        tab = VGroup()
        for j, (a, b, col) in enumerate(rows):
            y = 2.1 - 0.62 * j
            tab.add(VGroup(label(a, font_size=19, color=col).move_to([hx[0], y, 0]), MathTex(b, font_size=26).move_to(
                [hx[1], y, 0])))
        title = label(r"The factor library's first sheet", font_size=28).to_edge(UP, buff=0.4)
        foot = wrapped_label(r"every number computed in this part from public data; none is a forecast, and none is "
                             r"advice", 12.0, 18, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The factor library's first sheet. <bookmark mark='a'/> Momentum combines a positive historical Sharpe ratio with severe negative skewness. The six-month monthly-volatility rule improves this sample's Sharpe and tail measures, but still loses substantially. Value suffers a deep fourteen-year drawdown. The international value-momentum mix diversifies this sample. The final row records only the scope of the conceptual accounting chapter: the sealed experiment is excluded and no holdout score is reported."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.35), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"Factors, in the House", FA.vol_scaled, "for t in range(window", 3,
                         extra=((FA.factor_momentum, "past = np.prod", 4), (FA.drawdown, "w = cumulative", 4)), width=9.4)
        card.to_edge(UP, buff=0.6)
        with self.voiceover(
            'Three unchanged library excerpts. Volatility scaling uses six previous monthly returns, annualised by the square root of twelve, a twelve-percent target and a three-times cap. Factor momentum uses past twelve-month signs and equal factor exposures, not covariance-aware risk parity. Drawdown starts its running peak at the first observed compounded value, so an initial loss before that peak can be omitted. Statistics drop missing rows, while cumulative indices zero-fill them. Lagged inputs in revised public histories do not certify actual historical data availability; costs and funding remain omitted.'
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("research",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{stats}, \texttt{drawdown}, \texttt{cumulative}", r"what a factor is judged by"),
            (r"\texttt{alpha}, \texttt{model\_test}", 'alpha tests; legacy inference proxies'),
            (r"\texttt{two\_by\_three}", 'one-cross-section 2 x 3 illustration'),
            (r"\texttt{vol\_scaled}, \texttt{conditional\_beta}", r"momentum's crash, measured and damped"),
            (r"\texttt{factor\_momentum}, \texttt{value\_spread}, \texttt{equal\_risk}", r"timing, and the default book"),
            ('\\texttt{ddm\\_bm}; registration design', 'DDM toy; sealed experiment excluded'),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=16, color=QC.HOUSE), label(b_, font_size=16, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 7.4)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label('Rule 24: every factor the House holds is defined as published, before its data are seen; is judged by its whole path (its worst month, its worst decade, the state in which it crashes), not by its average; is held inside a diversified book, sized by risk, and timed only at the margin; and has a predeclared evaluation plan. This review reports no sealed score.', 12.4, 20,
                             QC.HOUSE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The library supports descriptive statistics, alpha tests, toy sorts, crash analysis and timing. <bookmark mark='a'/> Its inverse-volatility allocation equalises standalone volatility budgets; it is not covariance-aware equal risk contribution. The legacy inference outputs need their covariance qualifications. <bookmark mark='b'/> Rule twenty-four: define an evaluation plan before accessing new outcomes, inspect the whole path and failure states, budget implementation risk and diversify. This review makes no new registration and reports no sealed score. Diversification reduces some risks without guaranteeing survival."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"momentum, spring 2009", 'judged by its crash state, not its Sharpe ratio: in a bear market the rebound beta is an ex-post estimate; lagged volatility sizing reduces exposure without a crash guarantee', width=12.0,
                          font_size=19),
            desk_question(r"value, 2007--2020", 'diversification and advance disclosure may help; neither prevents ruin nor guarantees client retention', width=12.0, font_size=19),
            desk_question(r"size after 1981", r"defined as published and scored honestly: the premium's fall after "
                          r"discovery is in the record, not explained away", width=12.0, font_size=19),
            desk_question(r"green, 2012--2020", 'popularity shocks can affect realised returns; distinguish conditional expected premia from repricing', width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.22)
        if cards.height > 6.8:
            cards.scale_to_fit_height(6.8)
        with self.voiceover(
            "Apply the rule to these cases. <bookmark mark='a'/> Momentum's rebound beta is estimated after grouping months by the contemporaneous market sign. Lagged volatility scaling can reduce exposure, without forecasting the rebound or guaranteeing protection. <bookmark mark='b'/> Diversification and advance disclosure may help a value investor endure tracking error, but prevent neither insolvency nor withdrawals. <bookmark mark='c'/> The size split records weaker returns after 1981, without identifying publication as the cause. <bookmark mark='d'/> Green preference shocks can affect realised returns; a backtest alone cannot identify the expected premium. These are evaluation questions, not survival guarantees."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c", "d")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
