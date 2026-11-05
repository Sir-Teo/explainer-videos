from __future__ import annotations

from explainer.quant import *  # noqa: F403
from explainer.quant.house import risk as R
from videos.quant.quant40.common import (
    BAD,
    ES_C,
    GOOD,
    HIT_C,
    MODEL_C,
    PART,
    TAIL_C,
    VAR_C,
    house_lab,
    load,
)


class House(VoiceoverScene):
    def construct(self):
        self.answer()
        self.card()
        self.sheet(load("backtest"), load("evt"), load("depend"), load("stress"), load("ra"), load("learned"))
        self.report(load("backtest"), load("stress"), load("ra"), load("liq"))
        self.governance()
        self.desks()
        self.lab()
        self.lab2()
        self.lab3()
        self.lab4()
        self.module()
        self.test()

    def answer(self):
        rows = [cmath(r"\text{1. ES}", r":", r"\text{how bad the bad days are}", font_size=36, colors={r"\text{1. ES}": ES_C}),
                cmath(r"\text{2. the backtest}", r":", r"\text{exceptions, their clustering, } Z_2", font_size=36,
                      colors={r"\text{2. the backtest}": HIT_C}),
                cmath(r"\text{3. the stress}", r":", r"\text{the worst scenario, and the dependence bound}", font_size=36,
                      colors={r"\text{3. the stress}": BAD})]
        whys = [why(r"VaR says how often; ES says how much, and it is the coherent one (Chapter 2)"),
                why(r"a forecast without its track record is an opinion: the count, the independence test and the "
                    r"shortfall test over the last year and the last decade (Chapter 3)"),
                why(r"what the model cannot see: the historical and reverse stress losses, and how much rests on the "
                    r"dependence assumed (Chapters 6 and 7)")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The answer to the pause. <bookmark mark='a'/> First, the expected shortfall: how bad the bad days are. "
            "<bookmark mark='b'/> Second, the backtest: the exceptions, whether they cluster, and the shortfall test. "
            "<bookmark mark='c'/> Third, the stress: the worst historical and reverse-stress losses, and how much of the "
            "number rests on the dependence assumed."
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

    def card(self):
        c = chapter_card(10, r"Rule 40: a risk number is a forecast", r"What must accompany a risk number before anyone "
                         r"acts on it?", part=PART)
        with self.voiceover("Chapter ten. The House's fortieth rule belongs to its risk function, which now reports on "
                            "every desk. It treats every risk number the way the series has treated every return: as a "
                            "forecast, to be tested."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, b, e, d, s, ra, L):
        n, g = b["methods"]["normal"], b["methods"]["gjr_fhs"]
        p0 = d["pairs"][0]
        r2 = [x for x in ra["rows"] if x["theta"] == 2.0][0]
        rows = [(r"normal VaR, 1928--2020: exceeded; Z$_2$", rf"{100 * n['rate']:.2f}\%,\ {n['z2']:+.2f}", BAD),
                (r"GJR-filtered HS: exceeded; Kupiec $p$", rf"{100 * g['rate']:.2f}\%,\ {g['kupiec_p']:.2f}", GOOD),
                (r"tail exponent of daily losses (GPD)", rf"{1 / e['xi']:.1f}", TAIL_C),
                (r"banks and insurers, joint worst 1\%: data, Gaussian", rf"{p0['emp']['0.01']:.2f},\ {p0['gauss']['0.01']:.2f}", TAIL_C),
                (r"\$10m loss: most plausible scenario, std devs", rf"{s['rev'][1]['distance']:.1f}", BAD),
                (r"worst-case VaR over sum of VaRs, Pareto(2)", rf"{r2['worst_lo'] / r2['comonotonic']:.2f}", VAR_C),
                (r"network against GJR, 1991--2020 pinball", rf"{L['models']['network']['pinball']:.2f}\ \text{{vs}}\ "
                 rf"{L['models']['gjr_fhs']['pinball']:.2f}", MODEL_C)]
        hx = [-2.2, 4.8]
        tab = VGroup()
        for j, (txt, val, col) in enumerate(rows):
            y = 2.4 - 0.62 * j
            tab.add(VGroup(label(txt, font_size=16, color=col).move_to([hx[0], y, 0]),
                           MathTex(val, font_size=24).move_to([hx[1], y, 0])))
        title = label(r"The risk function's first sheet", font_size=28).to_edge(UP, buff=0.25)
        foot = wrapped_label(r"computed in this part from Kenneth French's daily US market, factor and industry returns, "
                             r"1926--2020 (the research window; the hold-out is not opened), and simulation; none is advice",
                             12.0, 15, GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The first sheet. <bookmark mark='a'/> A normal VaR exceeded twice as often as promised, with a shortfall "
            "test far in the red, and a GARCH-filtered one that passes. A tail exponent near five. Joint crashes far more "
            "common than the Gaussian copula allows. A ten-million-dollar day eight standard deviations away. A worst "
            "case for dependence seventy percent above the sum of the VaRs. And a learned model that did not beat the "
            "filter."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def report(self, b, s, ra, q):
        g = b["methods"]["gjr_fhs"]
        es1 = q["es975_10d"] / 10 ** 0.5 * q["pos"]
        r2 = [x for x in ra["rows"] if x["theta"] == 2.0][0]
        lines = VGroup(
            label(r"Evening risk report: \$100m US equity book (illustrative)", font_size=24, color=QC.HOUSE),
            label(rf"VaR 99\%, 1 day (history since 2010)   ........   \${q['var_m']:.2f}m", font_size=19, color=VAR_C),
            label(rf"ES 97.5\%, 1 day   ........   \${es1:.2f}m", font_size=19, color=ES_C),
            label(rf"backtest: {100 * g['rate']:.2f}\% exceeded since 1928; independence $p$ = {g['ind_p']:.2f}; "
                  rf"$Z_2$ = {g['z2']:+.2f}", font_size=17, color=HIT_C),
            label(rf"stress: 19 Oct 1987 replayed \${s['scen'][0]['loss_m']:.1f}m; \$10m reverse stress at "
                  rf"{s['rev'][1]['distance']:.1f} std devs", font_size=17, color=BAD),
            label(rf"dependence: worst case up to {r2['worst_lo'] / r2['comonotonic']:.1f}$\times$ the sum of VaRs for "
                  r"heavy-tailed sleeves", font_size=17, color=TAIL_C),
            label(r"liquidity: 20\% of a day's volume, about 0.45 of a day's volatility to exit", font_size=17,
                  color=MODEL_C)).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        box = SurroundingRectangle(lines, buff=0.35, color=QC.HOUSE, corner_radius=0.15)
        VGroup(box, lines).move_to(ORIGIN)
        with self.voiceover(
            "So the House's evening report has a shape. <bookmark mark='a'/> The VaR, and beside it the shortfall. "
            "<bookmark mark='b'/> The forecaster's own track record: how often it was exceeded, whether the exceptions "
            "clustered, and the shortfall test. <bookmark mark='c'/> The stress losses, the dependence bound and the cost "
            "of getting out. A reader who sees only the first line knows least."
        ) as vo:
            self.play(Create(box), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(lines[1:3]))
            vo.wait_until("b")
            self.play(FadeIn(lines[3]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lines[4:]], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def governance(self):
        cards = VGroup(
            desk_question(r"independence", r"the risk function reports to the board, not to the desks it measures "
                          r"(Part 34's controls)", width=12.0, font_size=19),
            desk_question(r"model validation", r"every risk model is re-estimated, backtested and challenged by people who "
                          r"did not build it, before and after it goes live", width=12.0, font_size=19),
            desk_question(r"limits in ES, checked in VaR", r"desks are limited by expected shortfall and stress loss; "
                          r"VaR's exceptions are the alarm that the model has drifted", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And around it. <bookmark mark='a'/> The risk function reports to the board, not to the desks it measures. "
            "<bookmark mark='b'/> Every model is validated by people who did not build it, before and after it goes "
            "live. <bookmark mark='c'/> And desks are limited in shortfall and stress loss, while VaR's exceptions serve "
            "as the alarm that the model has drifted."
        ) as vo:
            for k_, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def desks(self):
        cards = VGroup(
            desk_question(r"the volatility and market-making desks", r"short gamma and inventory: VaR by full "
                          r"revaluation, with volatility as a risk factor (Chapter 1's straddles, Part 38's maker)",
                          width=12.0, font_size=18),
            desk_question(r"the statistical and systematic books", r"crowding and correlation shifts: tail dependence "
                          r"and reverse stress across positions that look diversified (Parts 32 and 33)", width=12.0,
                          font_size=18),
            desk_question(r"the digital-assets desk", r"venue and stablecoin exposure as stress items with their own "
                          r"limits, outside the VaR (Part 39's Rule 39)", width=12.0, font_size=18),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What the rule means for the House's desks. <bookmark mark='a'/> The volatility and market-making desks are "
            "short gamma and carry inventory: their VaR needs full revaluation, with volatility as a risk factor. "
            "<bookmark mark='b'/> The statistical and systematic books look diversified until correlations shift: they "
            "need tail dependence and reverse stress. <bookmark mark='c'/> And the digital-assets desk's venue and "
            "stablecoin exposures are stress items with limits of their own, outside the VaR."
        ) as vo:
            for k_, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"Christoffersen's independence test", R.christoffersen, "a, b = I[:-1], I[1:]", 6, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapter three's timing test. Count the four kinds of consecutive pairs of days, quiet then quiet, quiet then "
            "exception, and so on, and compare the chance of an exception after an exception with the chance after a "
            "quiet day."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab2(self):
        card = house_lab(r"Peaks over threshold", R.evt_var_es, "v = u + beta / xi", 2, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapter four in two lines: the quantile of the fitted generalised Pareto tail, and its shortfall."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab3(self):
        card = house_lab(r"The most plausible scenario", R.reverse_stress, "s2 = float(w @ S @ w)", 3, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapter six's reverse stress test: the portfolio's variance, the scenario proportional to sigma times w, and "
            "its distance."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab4(self):
        card = house_lab(r"The rearrangement algorithm", R.rearrangement, "rest = X.sum(1) - X[:, j]", 5, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "And Chapter seven: for each column, the sum of the others, and the column re-sorted to run against it."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("portfolio",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{rolling\_forecasts}, \texttt{caviar\_fit}, \texttt{quantile\_mlp}", r"forecasting"),
            (r"\texttt{kupiec}, \texttt{christoffersen}, \texttt{acerbi\_szekely\_z2}, \texttt{fz0}", r"backtesting"),
            (r"\texttt{gpd\_fit}, \texttt{reverse\_stress}, \texttt{rearrangement}", r"tails and uncertainty"),
        ]
        tab = VGroup(*[VGroup(label(a_, font_size=15, color=QC.HOUSE), label(b_, font_size=15, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a_, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 9.6)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 40: every risk number the House reports is a forecast, shown with its own backtest; "
                             r"expected shortfall sits beside VaR; and every report carries the stress loss and the "
                             r"dependence bound that the model cannot see.", 12.4, 17, QC.HOUSE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The tools this part adds. <bookmark mark='a'/> Forecasting, backtesting, and tails and uncertainty. "
            "<bookmark mark='b'/> And the fortieth rule. Every risk number the House reports is a forecast, shown with "
            "its own backtest. Expected shortfall sits beside VaR. And every report carries the stress loss and the "
            "dependence bound that the model cannot see."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.5)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"a VaR model with no exceptions in a year", r"ask whether it is good or merely conservative, "
                          r"and look at a decade, not a year (Chapter 3)", width=12.0, font_size=19),
            desk_question(r"a portfolio whose risk fell after diversifying", r"ask whether the measure is VaR, and whether "
                          r"the new positions sit just beyond its quantile (Chapter 2)", width=12.0, font_size=19),
            desk_question(r"a credit book modelled with a Gaussian copula", r"ask for its joint exceedances, and what a "
                          r"$t$ copula or the dependence bound would say (Chapters 5 and 7)", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The rule against three cases. <bookmark mark='a'/> A VaR model with no exceptions in a year: ask whether it "
            "is good or merely conservative, and look at a decade. <bookmark mark='b'/> A portfolio whose risk fell when "
            "it diversified: ask whether the measure is VaR, and whether the new positions sit just beyond its quantile. "
            "<bookmark mark='c'/> A credit book modelled with a Gaussian copula: ask for its joint exceedances, and what "
            "the dependence bound would say."
        ) as vo:
            for k_, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
