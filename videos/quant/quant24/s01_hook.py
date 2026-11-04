from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant24.common import (BAD, FCOL, GOOD, MKT, PART, UMD, era_strip, fit_right, illustration,
                                         load)


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.race(load("race"))
        self.crash(load("crash"))
        self.what()
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Factors")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part twenty-four. Factors: the handful of portfolios that, for half a century, have explained most of what "
            "stocks earn, and the first strategies the House scores on data it has never seen."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def race(self, r):
        d = np.asarray(r["date"])
        t = d // 100 + (d % 100 - 0.5) / 12
        g = axes([1963, 2021], [-0.2, 1.7], x_length=8.2, y_length=4.4, xlabel=r"year",
                 ylabel=r"\$1 in July 1963, $\log_{10}$", xticks=[1970, 1980, 1990, 2000, 2010, 2020],
                 yticks=[0, 0.5, 1.0, 1.5], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        names = r["names"]
        lines = VGroup(*[curve(ax, t, np.log10(np.asarray(r["series"][k])), FCOL[k], stroke_width=2.4) for k in names])
        labs = {"MKT": r"the market (less bills)", "SMB": r"size: small minus big", "HML": r"value: high minus low B/M",
                "UMD": r"momentum: up minus down", "RMW": r"profitability: robust minus weak",
                "CMA": r"investment: conservative minus aggressive"}
        rows = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.35, color=FCOL[k], stroke_width=4),
                               label(rf"{labs[k]}: \${r['series'][k][-1]:.1f}", font_size=15, color=FCOL[k])).arrange(
            RIGHT, buff=0.15) for k in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        side = VGroup(rows, wrapped_label(r"monthly excess and long--short returns, compounded, July 1963 to December "
                                          r"2020: each long--short as if fully collateralised, the interest kept aside. "
                                          r"No costs", 3.6, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        side.to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Six dollars, put to work in July 1963. One in the stock market above bills, and five in long-short "
            "portfolios that own one kind of stock and sell another. <bookmark mark='a'/> The market turned its dollar "
            f"into about {r['series']['MKT'][-1]:.0f}. Small stocks against large, value against growth, profitable "
            "against unprofitable, conservative against aggressive investors: each into four or five. "
            f"<bookmark mark='b'/> And momentum, last year's winners against last year's losers, into "
            f"{r['series']['UMD'][-1]:.0f}, with no net money invested at all. These are the classic factors. This "
            "part asks what each one is, how it was found, why it might pay, and whether it still does."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(Create(lines[i]), FadeIn(rows[i])) for i in (0, 1, 2, 4, 5)],
                                  lag_ratio=0.3), run_time=4)
            vo.wait_until("b")
            self.play(Create(lines[3]), FadeIn(rows[3]), run_time=2)
        self.add(illustration(r"Kenneth French's data library: the five factors and momentum"))
        self.wait(0.4)
        self.clear_scene()

    def crash(self, c):
        w = c["w2009"]
        cc = crisis_card(r"March--May 2009", r"The momentum crash",
                         r"as the market rebounded from its March 2009 low, the stocks that had fallen furthest in 2008 "
                         r"(banks, cyclicals: the momentum strategy's short side) rose fastest. In three months the "
                         r"momentum factor lost about half its value while the market gained a quarter",
                         stats=[(rf"{100 * w['cum_umd']:.0f}\%", r"momentum (UMD), March to May 2009"),
                                (rf"+{100 * w['cum_mkt']:.0f}\%", r"the market, the same three months")], width=8.6,
                         font_size=20)
        with self.voiceover(
            "And then there are the months when a factor breaks. In March 2009 the market turned up from its low. "
            "The stocks that had fallen furthest in the crisis, the banks and the cyclicals, were exactly the ones the "
            "momentum strategy was short, and they rose fastest. <bookmark mark='a'/> In three months momentum lost "
            f"about {abs(100 * w['cum_umd']):.0f} percent, while the market gained {100 * w['cum_mkt']:.0f}. A "
            "decade of gains, gone in a spring. Chapter four takes the crash apart."
        ) as vo:
            self.play(FadeIn(cc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(cc, color=BAD, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    def what(self):
        rows = [cmath(r"f_t", r"=", r"R^{\text{long}}_t - R^{\text{short}}_t", font_size=46, colors={r"f_t": GOOD}),
                cmath(r"\mathbb{E}[R^e_i]", r"=", r"\textstyle\sum_k \beta_{ik}\,\mathbb{E}[f_k]", font_size=46,
                      colors={r"\mathbb{E}[R^e_i]": MKT})]
        whys = [why(r"a factor is a portfolio: buy the stocks with a characteristic (small, cheap, rising), sell those "
                    r"without it. Its return is a long--short spread, an excess return with zero net cost"),
                why(r"a factor model says these few spreads price everything: every portfolio's expected excess return "
                    r"is its betas on them times their means (Part 23's APT, with the factors named). Testing that is "
                    r"chapter one")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.9, edge=6.9)
        with self.voiceover(
            "What is a factor? In this part, a portfolio. Rank stocks on some characteristic, small or cheap or "
            "rising, buy the ones that have it and sell the ones that do not. The factor's return is the spread "
            "between the two, an excess return that costs nothing to set up. <bookmark mark='a'/> A factor model then "
            "makes a strong claim: that a few such spreads price everything. Every portfolio's expected excess return "
            "is its betas on the factors times the factors' average returns. Part twenty-three's arbitrage pricing "
            "theory, with the factors finally named."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def history(self):
        I, C = QC.IDEA, QC.CRISIS
        entries = [(1972, r"Black--Jensen--Scholes", I), (1977, r"Basu: P/E", I), (1981, r"Banz: size", I),
                   (1985, r"Rosenberg: B/M", I), (1992, r"Fama--French", I), (1993, r"Jegadeesh--Titman", I),
                   (1997, r"Carhart", I), (2009, r"momentum crash", C), (2012, r"time-series momentum", I),
                   (2013, r"everywhere", I), (2014, r"betting against beta", I), (2015, r"five factors, q", I),
                   (2019, r"China's factors", I), (2020, r"value's low", C), (2022, r"factor momentum", I)]
        strip = era_strip(entries, y0=1968, y1=2026, font_size=14).move_to(DOWN * 0.3)
        head = label(r"How the factors were found", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 5), (5, 10), (10, 15)]
        with self.voiceover(
            "How the factors were found. In the 1970s and early 1980s, as tests of the CAPM: Fischer Black, Michael "
            "Jensen and Myron Scholes found the security market line too flat, Sanjoy Basu that cheap stocks beat their "
            "betas, Rolf Banz that small ones did. <bookmark mark='a'/> Eugene Fama and Kenneth French gathered size "
            "and value into a three-factor model in 1992 and 1993; Narasimhan Jegadeesh and Sheridan Titman documented "
            "momentum; Mark Carhart added it. <bookmark mark='b'/> Then a second wave: momentum's crash, time-series "
            "momentum, value and momentum in every market, betting against beta, five factors and the q-factors, "
            "China's own model, and value's worst decade."
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
            r"Test a factor model: GRS, Fama--MacBeth, and the 25 size--value portfolios",
            r"Size, value, momentum (across stocks and through time), and momentum's crashes",
            r"Profitability and investment; five factors and q; low risk; quality",
            r"Value and momentum everywhere; carry; value's lost decade, measured",
            r"Green returns; factor timing; China's factors; the factor industry",
            r"The Track Record opens: ten factors scored on 2021--2025, once",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: how to test a factor model, and the twenty-five portfolios every model is tested on; size, "
            "value and momentum, and momentum's crashes; profitability, investment and low risk; value and momentum in "
            "every market, and carry; value's lost decade, measured; green returns, factor timing and China; the firms "
            "that sell factors; and at the end, the Track Record opens."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=11))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("research",))
        with self.voiceover(
            "In the House, the research desk builds its first library: the factors, each with its history, its "
            "crashes and its reason. And every result in this part comes from data that ends in December 2020, until "
            "the last chapters, when the sealed years since are opened for the first time."
        ):
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
