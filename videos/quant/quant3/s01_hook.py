from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant3.common import PART, PRICE, VALUE, load, real_data


class Hook(VoiceoverScene):
    def construct(self):
        s = load("shiller")
        self.title_card()
        self.shiller(s)
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"What is a share a claim on?")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part three. Value, accounting and the firm. Parts one and two treated a price as a number that moves "
            "and a thing that trades. But a share is a claim on something: a slice of a company's future cash. If "
            "prices are fair, they should be the value of that cash today. Are they?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def shiller(self, s):
        t = np.asarray(s["t"])
        P, ps = np.asarray(s["price"]), np.asarray(s["pstar"])
        lo, hi = np.log10(min(P.min(), ps.min()) * 0.8), np.log10(max(P.max(), ps.max()) * 1.2)
        g = axes([1871, 2021], [lo, hi], x_length=6.6, y_length=4.8, ylabel=r"S\&P composite, in 2020 dollars (log scale)",
                 xticks=[1880, 1920, 1960, 2000], yticks=[2, 3], xfmt=lambda v: f"{int(v)}",
                 yfmt=lambda v: rf"{10 ** v:,.0f}".replace(",", "{,}"), font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lp = curve(ax, t, np.log10(P), PRICE, stroke_width=2.5)
        ls = curve(ax, t, np.log10(ps), VALUE, stroke_width=4)
        leg = legend([(PRICE, r"the real price"), (VALUE, r"$p^*$: the present value of the dividends actually paid")],
                     font_size=20).to_edge(RIGHT, buff=0.35).shift(UP * 2.4)
        res = VGroup(
            label(r"how much each moves in a year:", font_size=24, color=GREY_A),
            MathTex(rf"\text{{price}}\ {100 * s['sd_dprice']:.1f}\%\qquad p^*\ {100 * s['sd_dpstar']:.1f}\%", font_size=34),
            MathTex(rf"\text{{years with a move above 20\%:}}\ {s['big_moves']}\ \text{{vs}}\ {s['big_moves_pstar']}",
                    font_size=28),
            wrapped_label(r"Shiller (1981), ``Do stock prices move by too much to be justified by subsequent changes in "
                          r"dividends?''", 4.6, 19, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.2)
        src = real_data(rf"Shiller's data, 1871--2020; discount rate {100 * s['r']:.1f}\% real, the average return; "
                        r"$p^*$ in 2020 starts from that year's price")
        with self.voiceover(
            "In 1981 Robert Shiller asked that question with a century of data, and here it is with a century and a "
            "half. The blue line is the American stock market, adjusted for inflation, since 1871. "
            "<bookmark mark='a'/> The gold line is what the market would have been worth if everyone had known, "
            "every year, exactly which dividends would be paid in the future, and valued them at the market's "
            "average return: the present value of the dividends that were actually paid. Shiller called it p star. "
            "<bookmark mark='b'/> If prices were the best forecasts of that value, they should move less than it, "
            "the way a forecast moves less than the thing it forecasts. Instead the price moves "
            f"{s['ratio_changes']:.0f} times as much from year to year: in {s['big_moves']} of these years it "
            "moved more than twenty percent, and p star never did. <bookmark mark='c'/> Either the discount rate "
            "itself moves a great deal, or prices are moved by something other than dividends. That debate earned "
            "Shiller a share of the 2013 Nobel prize, with Eugene Fama and Lars Peter Hansen, and it runs through this part."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg[0]))
            self.play(Create(lp), run_time=3)
            vo.wait_until("a")
            self.play(Create(ls), FadeIn(leg[1]), run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in res[:3]], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(res[3]))
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Time value: present values, annuities, the Gordon growth model, and its sensitivity to the discount rate",
            r"The three statements, read as linked ledgers; accruals; machine-readable filings",
            r"Valuation: discounted cash flow, the cost of capital, multiples and the CAPE",
            r"Capital structure and payout: Modigliani and Miller, dividends and buybacks, equity as a call option",
            r"Earnings surprises and the drift after them; accounting signals that became factors, and their decay",
            r"Corporate events: merger arbitrage, whose payoff is a short put",
            r"When the statements lie: Enron and Wirecard",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan. The arithmetic of time value. The three financial statements, read as linked ledgers. "
            "Valuation by discounted cash flow, the cost of capital, multiples and Shiller's CAPE. Capital "
            "structure and payout, from Modigliani and Miller to buybacks, and equity seen as an option. Earnings "
            "announcements and the drift that follows them, and the accounting signals that became the first "
            "factors, measured, before and after they were published. Merger arbitrage, a strategy that is secretly "
            "an option. And what happens when the statements lie."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=9))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("data",))
        with self.voiceover(
            "In the House, this part extends the data desk with a fundamentals store and a valuation library. "
            "<bookmark mark='a'/> Its rule: a company's numbers are known on the day they were published, not on "
            "the day the quarter ended."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
