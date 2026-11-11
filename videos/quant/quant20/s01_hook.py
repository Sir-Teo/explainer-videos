from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, PART, RISKY, ZERO, era_strip, illustration, load


class Hook(VoiceoverScene):
    def construct(self):
        s = load("spreads")
        self.title_card()
        self.lehman(s)
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"What a promise is worth")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part twenty. Credit. Every bond so far has paid in full. Now the borrower may not, and the price of a "
            "promise depends on who made it."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def lehman(self, s):
        t, v = np.asarray(s["daily_t"]), np.asarray(s["daily"])
        g = axes([2006, 2010], [0, 7], x_length=7.4, y_length=4.4, xlabel=r"year",
                 ylabel=r"Moody's Baa yield minus the 10-year Treasury, \%", xticks=[2006, 2007, 2008, 2009, 2010],
                 yticks=[0, 2, 4, 6], font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        sel = (t >= 2006) & (t <= 2010)
        line = curve(ax, t[sel], v[sel], RISKY, stroke_width=2.6)
        mk = s["max"]
        md = mk["date"]
        top = Dot(ax.c2p(md // 10000 + (md // 100 % 100 - 1) / 12 + (md % 100) / 365, mk["v"]), color=BAD, radius=0.08)
        leh = DashedLine(ax.c2p(2008 + 8.5 / 12, 0), ax.c2p(2008 + 8.5 / 12, 7), color=GREY_B, stroke_width=2)
        cc = crisis_card(r"15 September 2008", r"Lehman Brothers files for bankruptcy",
                         'the 10 October auction fixed recovery at 8.625 cents: covered CDS protection paid 91.375\\% of notional, before premiums, netting and counterparty performance',
                         stats=[(r"8.625", r"cents on the dollar, the auction's final price"),
                                (rf"{mk['v']:.2f}\%", r"the Baa spread at its peak, 4 December 2008")],
                         width=5.0, font_size=19).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            f"On September fifteenth, two thousand eight, Lehman Brothers filed for bankruptcy. <bookmark mark='a'/> The October tenth CDS auction set a final price of eight point six two five percent of par. Covered auction-settled protection had a gross loss payment of ninety-one point three seven five percent of notional, before premiums, netting, hedges and counterparty performance. <bookmark mark='b'/> Across the market, the saved Baa-minus-ten-year-Treasury series reached {mk['v']:.2f} percent that December. This broad yield gap includes expected credit losses, risk premia and other frictions. It frames our question: how should we value a promise whose maker might fail to pay?"
        ) as vo:
            self.play(FadeIn(g), Create(leh), Create(line), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(cc))
            vo.wait_until("b")
            self.play(FadeIn(top, scale=1.5))
        self.add(illustration(r"FRED: BAA10Y; Creditex and Markit, Lehman CDS auction results (10 October 2008)"))
        self.wait(0.5)
        self.clear_scene()

    def history(self):
        I, F, C, R_ = QC.IDEA, QC.FIRM, QC.CRISIS, QC.HOUSE
        entries = [(1968, r"Altman's Z", I), (1974, r"Merton", I), (1976, r"Black--Cox", I), (1994, r"Leland", I),
                   (1994, 'early modern CDS', F), (1995, r"Jarrow--Turnbull", I), (1999, r"Duffie--Singleton", I),
                   (2000, r"Li's copula", I), (2001, r"Enron; Shumway", C), (2003, r"Basel II's formula", R_),
                   (2007, r"subprime", C), (2008, r"Lehman", C), (2009, r"the Big Bang", R_),
                   (2012, r"the London Whale", C), (2020, r"the dash for cash", C), (2024, r"private credit", F)]
        strip = era_strip(entries, y0=1964, y1=2027, font_size=15).move_to(DOWN * 0.3)
        head = label(r"How we got here", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 4), (4, 9), (9, 13), (13, 16)]
        with self.voiceover(
            "How we got here. In 1968 Edward Altman predicted bankruptcy from five accounting ratios. In 1974 Robert Merton priced a company's debt as an option on its assets; in 1976 Black and Cox let default come early, and in 1994 Hayne Leland let the firm choose when. <bookmark mark='a'/> The same year a team at J.P. Morgan wrote a widely cited early modern credit default swap; credit-risk transfer existed earlier. Jarrow and Turnbull, then Duffie and Singleton, modelled default as a random clock; in 2000 David Li tied many clocks together with a copula; and in 2001, the year Enron failed, Tyler Shumway turned bankruptcy prediction into a hazard model. <bookmark mark='b'/> In 2003 Michael Gordy gave the Basel capital formula its foundation. Then subprime, Lehman, and in 2009 the swap market's standardization, the Big Bang. <bookmark mark='c'/> Since then, the London Whale in 2012, the dash for cash of March 2020, and the rise of private credit."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), m in zip(groups, [None, "a", "b", "c"]):
                if m:
                    vo.wait_until(m)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"What a credit spread measures, from a century of corporate bond yields",
            r"Structural models: Merton, distance to default from prices and filings, first passage",
            r"Reduced form: default as a random clock; the credit default swap, priced and bootstrapped",
            r"Accounting scores and validation: Altman, logit and trees on a fixed synthetic population",
            r"Portfolios: Vasicek's large pool, bank capital, copulas, CDO tranches",
            r"From the record: 2008's senior tranches, the London Whale, March 2020",
            r"Private credit and its marks",
        ], color=QC.IDEA)
        with self.voiceover(
            'The plan: corporate credit spreads; structural models and their assumptions; retrospective asset-value fits from prices and filings; default intensity, recovery and the credit default swap; bankruptcy-label design and a fixed synthetic comparison of Altman, logit and boosted trees; then large portfolios, capital and tranches. We also examine three episodes from the public record and the interpretation of private-credit marks. No sealed issuer experiment is opened in this review.'
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("credit",))
        with self.voiceover(
            "In the House, the credit desk opens: default probabilities from prices and from accounts, a swap "
            "pricer, and the portfolio models that set a bank's capital."
        ):
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["credit"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
