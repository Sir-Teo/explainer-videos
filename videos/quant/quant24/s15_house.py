from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import factors as FA
from videos.quant.quant24.common import BAD, FCOL, GOOD, HML, PART, UMD, house_lab, load


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("race"), load("crash"), load("everywhere"), load("valuedecade"), load("envelope"))
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

    def sheet(self, r, c, e, v, env):
        rows = [(r"momentum: Sharpe ratio, skewness, worst month", rf"{c['raw']['sharpe']:.2f},\ {c['raw']['skew']:.1f},\ "
                                                                rf"{100 * c['raw']['worst']:.0f}\%", UMD),
                (r"momentum scaled to constant volatility", rf"{c['scaled']['sharpe']:.2f},\ {c['scaled']['skew']:.1f},\ "
                                                          rf"{100 * c['scaled']['worst']:.0f}\%", GOOD),
                (r"value, 2007--2020", rf"{100 * v['stats_0720']['mean']:.1f}\%\ \text{{a year}},\ "
                                       rf"{100 * v['dd']['max']:.0f}\%\ \text{{drawdown}}", HML),
                (r"value and momentum, all markets: correlation", rf"{e['global']['corr']:.2f}", BAD),
                (r"their 50/50 mix: Sharpe ratio", rf"{e['global']['combo']['sharpe']:.2f}", QC.HOUSE),
                (r"ten classic factors: average Sharpe, research to 2021--25",
                 rf"{np.mean([x['research']['sharpe'] for x in env['rows'].values()]):.2f}\ \to\ "
                 rf"{np.mean([x['holdout']['sharpe'] for x in env['rows'].values()]):.2f}", QC.HOUSE)]
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
            "The factor library's first sheet. <bookmark mark='a'/> Momentum: the best Sharpe ratio of the classic "
            "American factors and the worst skewness, a month of minus fifty-three percent. Scaled to constant "
            "volatility, a better ratio and a far gentler tail. Value: fourteen years of losses and a drawdown of "
            "fifty-seven percent. Value and momentum, negatively correlated in every market, and a mix with a Sharpe "
            "ratio above one. And the first five sealed years: the classic factors' average Sharpe ratio down by about "
            "a third, as published anomalies decay."
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
            "Three excerpts from the new library. Volatility scaling: each month, the factor's realised volatility over "
            "the previous six months, and a position of the target divided by it, capped at three. Factor momentum: "
            "each factor's compounded return over the past year, and its sign. And the drawdown: the path's running "
            "peak, and how far below it the path has fallen. Each uses only what was known at the time, which is the "
            "House's first rule, applied. And the drawdown is there because this part's most important numbers were "
            "not averages: they were the worst month, the worst decade, and the depth of the fall."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("research",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{stats}, \texttt{drawdown}, \texttt{cumulative}", r"what a factor is judged by"),
            (r"\texttt{alpha}, \texttt{model\_test}", r"spanning, GRS, Fama--MacBeth"),
            (r"\texttt{two\_by\_three}", r"the Fama--French construction"),
            (r"\texttt{vol\_scaled}, \texttt{conditional\_beta}", r"momentum's crash, measured and damped"),
            (r"\texttt{factor\_momentum}, \texttt{value\_spread}, \texttt{equal\_risk}", r"timing, and the default book"),
            (r"\texttt{ddm\_bm}; \texttt{track.record}", r"why the factors exist; the Track Record"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=16, color=QC.HOUSE), label(b_, font_size=16, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 7.4)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 24: every factor the House holds is defined as published, before its data are seen; is "
                             r"judged by its whole path (its worst month, its worst decade, the state in which it crashes), "
                             r"not by its average; is held inside a diversified book, sized by risk, and timed only at the "
                             r"margin; and is scored on the Track Record once, whatever that shows.", 12.4, 20,
                             QC.HOUSE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The library, on the research desk. <bookmark mark='a'/> Statistics and drawdowns; alphas, spanning and the "
            "joint tests; the Fama-French construction; momentum's crash, measured and damped; timing and the "
            "default book; the dividend discount model's reason for the factors; and the Track Record itself. "
            "<bookmark mark='b'/> And the twenty-fourth rule. Every factor the House holds is defined as published, "
            "before its data are seen. It is judged by its whole path, its worst month, its worst decade, and the state "
            "in which it crashes, not by its average. It is held inside a diversified book, sized by risk, and timed "
            "only at the margin. And it is scored on the Track Record once, whatever that shows."
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
            desk_question(r"momentum, spring 2009", r"judged by its crash state, not its Sharpe ratio: in a bear market its "
                          r"beta is about $-1$; sized by risk, the position was already halved before April", width=12.0,
                          font_size=19),
            desk_question(r"value, 2007--2020", r"inside a diversified book, the lost decade was a drag, not a ruin; a "
                          r"long-only client warned of a decade of tracking error stays", width=12.0, font_size=19),
            desk_question(r"size after 1981", r"defined as published and scored honestly: the premium's fall after "
                          r"discovery is in the record, not explained away", width=12.0, font_size=19),
            desk_question(r"green, 2012--2020", r"a premium measured while a characteristic became popular is a "
                          r"repricing; the rule asks for the reason before the backtest", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.22)
        if cards.height > 6.8:
            cards.scale_to_fit_height(6.8)
        with self.voiceover(
            "Hold the rule against this part's cases. <bookmark mark='a'/> Momentum in the spring of 2009: judged by "
            "its crash state, its beta of minus one after a bear market was visible, and sized by risk its position "
            "had already been halved. <bookmark mark='b'/> Value's lost decade: inside a diversified book, a drag "
            "rather than a ruin, and a client warned in advance of a decade of tracking error might stay. "
            "<bookmark mark='c'/> Size after its discovery: defined as published and scored honestly, its fall is in "
            "the record. <bookmark mark='d'/> And green returns: a premium measured while a characteristic became "
            "popular is a repricing, and the rule asks for the reason first. None of this predicts the next five "
            "years. It decides what the House can survive in them."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c", "d")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
