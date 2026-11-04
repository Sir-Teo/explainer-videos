from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant23.common import BAD, MKT, PART, SDF, TAN, era_strip, fit_right, illustration, load


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.dollar(load("hook"))
        self.question()
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"What risk is worth")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part twenty-three. Risk and return. Act Three asked what things must cost. Act Four asks what they pay, "
            "and why."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def dollar(self, h):
        t, s, b = np.asarray(h["t"]), np.asarray(h["stocks"]), np.asarray(h["bills"])
        g = axes([1926, 2026], [0, 4.6], x_length=8.2, y_length=4.4, xlabel=r"year", ylabel=r"\$1 in July 1926, $\log_{10}$",
                 xticks=[1930, 1950, 1970, 1990, 2010], yticks=[0, 1, 2, 3, 4], font_size=14).to_edge(LEFT, buff=0.5).shift(
            DOWN * 0.3)
        ax = g.ax
        ls = curve(ax, t, np.log10(s), MKT, stroke_width=2.6)
        lb = curve(ax, t, np.log10(b), TAN, stroke_width=2.6)
        side = VGroup(
            legend([(MKT, r"US stocks (the market)"), (TAN, r"one-month Treasury bills")], font_size=17),
            MathTex(rf"\text{{stocks}}:\ \${h['end_stocks']:,.0f}\ \ ({100 * h['cagr_s']:.1f}\%\ \text{{a year}})"
                    .replace(",", "{,}"), font_size=24, color=MKT),
            MathTex(rf"\text{{bills}}:\ \${h['end_bills']:.0f}\ \ ({100 * h['cagr_b']:.1f}\%\ \text{{a year}})", font_size=24,
                    color=TAN),
            wrapped_label(r"nominal, dividends reinvested, no costs or taxes, to December 2025. The gap is the equity "
                          r"premium: about seven points a year, for a century", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "A dollar put into the American stock market in July 1926, dividends reinvested. <bookmark mark='a'/> By "
            f"the end of 2025 it was worth about {h['end_stocks'] / 1000:.1f} thousand dollars. <bookmark mark='b'/> The "
            f"same dollar in one-month Treasury bills: about {h['end_bills']:.0f}. Ten percent a year against three, "
            "for a century. That gap is the equity premium, and it is the central number of this part. Why is it so "
            "large? Is it a reward for risk, and if so for which risk? Or is it a mistake that a careful investor could "
            "have exploited?"
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(ls), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(lb), FadeIn(side[2]), FadeIn(side[3]), run_time=2)
        self.add(illustration(r"Kenneth French's data library: the market and the one-month bill"))
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        rows = [cmath(r"\mathbb{E}[R^i] - R^f", r"=", r"\beta_i\,\lambda", font_size=48, colors={r"\mathbb{E}[R^i] - R^f": MKT}),
                cmath(r"p", r"=", r"\mathbb{E}[m\,x]", font_size=48, colors={r"p": SDF})]
        whys = [why(r"every model in this part has this shape: an asset's expected excess return is its exposure to some "
                    r"risk, times the price of that risk. The argument is always about which risk"),
                why(r"and every one of them is a choice of $m$, the stochastic discount factor: the single equation "
                    r"behind all of asset pricing (chapter 4)")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.9, edge=6.9)
        with self.voiceover(
            "Every theory in this part has the same shape. An asset's expected return above cash is its exposure to "
            "some risk, beta, times the price the market charges for that risk, lambda. The argument is always about "
            "which risk: the market's, consumption's, a bank's capital, or none at all. <bookmark mark='a'/> And every "
            "one of them is a special case of a single equation: the price of anything is the expectation of its "
            "payoff times a discount factor. By chapter four we will have it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def history(self):
        I, F, C, R_ = QC.IDEA, QC.FIRM, QC.CRISIS, QC.HOUSE
        entries = [(1952, r"Markowitz", I), (1958, r"Tobin", I), (1964, r"Sharpe's CAPM", I), (1973, r"Merton: ICAPM", I),
                   (1976, r"Ross: APT", I), (1978, r"Lucas", I), (1981, r"Shiller", I), (1982, r"Hansen--Singleton", I),
                   (1985, r"Mehra--Prescott", I), (1991, r"Hansen--Jagannathan", I), (1997, r"limits of arbitrage", I),
                   (2000, r"the dot-com peak", C), (2006, r"rare disasters", I), (2017, r"intermediaries", I),
                   (2021, r"inelastic markets", I)]
        strip = era_strip(entries, y0=1948, y1=2026, font_size=14).move_to(DOWN * 0.3)
        head = label(r"How we got here", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 5), (5, 10), (10, 15)]
        with self.voiceover(
            "How we got here. In 1952 Harry Markowitz turned diversification into mathematics; James Tobin added cash; "
            "William Sharpe and others derived the capital asset pricing model; Robert Merton and Stephen Ross allowed "
            "for many risks. <bookmark mark='a'/> Robert Lucas priced assets from consumption, Robert Shiller showed "
            "that prices move too much for the dividends behind them, Lars Hansen built the tools to test it all, and "
            "Rajnish Mehra and Edward Prescott found that the equity premium is far too large for any reasonable "
            "aversion to risk. <bookmark mark='b'/> Then the limits of arbitrage, the dot-com bubble, rare disasters, "
            "and the newest answers: that intermediaries' balance sheets, and inelastic demand, set prices."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), m in zip(groups, [None, "a", "b"]):
                if m:
                    vo.wait_until(m)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Markowitz's frontier by Lagrange; cash and the tangency; why estimated frontiers disappoint",
            r"The CAPM derived, and the flat line the data draw instead",
            r"One equation, $p = E[mx]$; Hansen--Jagannathan bounds; APT and ICAPM",
            r"Consumption, GMM, and the equity premium puzzle; habits, long-run risk, disasters",
            r"Shiller's excess volatility; intermediaries; demand systems and inelastic markets",
            r"Behaviour, the limits of arbitrage, and bubbles",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: the frontier of risk and return, derived, and why the estimated one disappoints; the capital "
            "asset pricing model and the flat line the data draw instead; the one equation behind all of it, and the "
            "bound it puts on any model; consumption, and the puzzle it cannot solve; prices that move too much; "
            "intermediaries and inelastic markets; and behaviour, the limits of arbitrage, and bubbles."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=11))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("research",))
        with self.voiceover(
            "In the House, the research desk opens. Its first product is not a strategy, but a framework: what "
            "expected return any position should earn, for the risk it bears."
        ):
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
