from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant22.common import BAD, FOR, PART, USD, era_strip, fit_right, illustration, load


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.snb(load("snb"))
        self.counted()
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"A floor that broke")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part twenty-two. Currencies, commodities, and the basis: the prices of moving money across borders, and "
            "of moving oil and gas across time."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def snb(self, s):
        t, v = np.asarray(s["t"]), np.asarray(s["eurchf"])
        g = axes([2010, 2017], [0.9, 1.45], x_length=8.0, y_length=4.4, xlabel=r"year", ylabel=r"Swiss francs per euro",
                 xticks=[2010, 2012, 2014, 2016], yticks=[1.0, 1.1, 1.2, 1.3, 1.4], font_size=14).to_edge(
            LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        k = int(np.argmin(np.abs(t - 2015.04)))
        line_a = curve(ax, t[:k], v[:k], USD, stroke_width=2.6)
        line_b = curve(ax, t[k - 1:], v[k - 1:], BAD, stroke_width=2.6)
        floor = DashedLine(ax.c2p(2011.68, 1.2), ax.c2p(2015.04, 1.2), color=FOR, stroke_width=2.5)
        fl = label(r"the 1.20 floor, from 6 September 2011", font_size=16, color=FOR).next_to(ax.c2p(2011.7, 1.2), UP,
                                                                                          buff=0.1).shift(RIGHT * 1.2)
        side = VGroup(
            MathTex(rf"14\ \text{{Jan 2015}}:\ {s['before']:.4f}", font_size=26),
            MathTex(rf"15\ \text{{Jan 2015}}:\ {s['on']:.4f}\ \ ({100 * s['move']:+.1f}\%)", font_size=26, color=BAD),
            MathTex(rf"\text{{about }} {abs(s['z_move']):.0f}\ \text{{daily standard deviations}}", font_size=24,
                    color=BAD),
            wrapped_label(r"the Fed's noon rates in New York. The Swiss National Bank had capped the franc at 1.20 per "
                          r"euro for three years, buying euros without limit; at 10:30 in Zurich it stopped, and cut its "
                          r"deposit rate to $-0.75\%$", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "In September 2011, with money fleeing the euro crisis into Swiss francs, the Swiss National Bank promised "
            "that a euro would never cost less than one franc twenty. <bookmark mark='a'/> For three years it kept the "
            "promise by printing francs and buying euros, without limit, and the rate sat on the floor. "
            "<bookmark mark='b'/> On the fifteenth of January 2015, at half past ten in Zurich, it stopped. Within "
            "minutes the euro was worth less than ninety centimes; by noon in New York it had settled "
            f"{abs(100 * s['move']):.0f} percent lower, a move of about {abs(s['z_move']):.0f} standard deviations of "
            "the previous three years' daily changes. Nothing in the history of that rate said it could happen."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line_a), Create(floor), FadeIn(fl), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(line_b), LaggedStart(*[FadeIn(x_) for x_ in side], lag_ratio=0.4), run_time=2)
        self.add(illustration(r"FRED: DEXSZUS, DEXUSEU (noon buying rates); SNB press release, 15 January 2015"))
        self.wait(0.5)
        self.clear_scene()

    def counted(self):
        cards = VGroup(
            desk_question(r"FXCM", r"a large US retail broker: its clients' accounts went negative by about "
                          r"\$275 million in minutes, more than the broker's capital; it survived on a \$300 million "
                          r"loan from Leucadia the next day (FXCM's 2015 annual report)", width=12.0, font_size=21),
            desk_question(r"Alpari UK", r"a London broker, insolvent within a day; its clients' losses exceeded their "
                          r"deposits", width=12.0, font_size=21),
            desk_question(r"the lesson", r"a peg turns a currency's risk into a step: no volatility for years, then all "
                          r"of it at once. Every model calibrated to the calm said a 1.20 floor was a sure thing",
                          width=12.0, font_size=21),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "The losses landed on whoever had treated the floor as a law of nature. <bookmark mark='a'/> At FXCM, a "
            "large American retail broker, clients' accounts went negative by about two hundred and seventy-five "
            "million dollars within minutes, more than the broker could absorb; it survived on a three hundred "
            "million dollar loan arranged the next day. <bookmark mark='b'/> Alpari's British arm was insolvent within "
            "a day. <bookmark mark='c'/> A peg does not remove a currency's risk. It stores it, and releases it all at "
            "once. That is the first lesson of this part: in currencies and commodities, the price you see is often "
            "held in place by someone's balance sheet, and the risk is what happens when they let go."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def history(self):
        I, F, C, R_ = QC.IDEA, QC.FIRM, QC.CRISIS, QC.HOUSE
        entries = [(1983, r"Garman--Kohlhagen", I), (1984, r"Fama's puzzle", I), (1986, r"oil's collapse", C),
                   (1992, r"Black Wednesday", C), (1997, r"TIPS", R_), (2006, r"Amaranth; Gorton--Rouwenhorst", C),
                   (2007, r"vanna--volga", I), (2008, r"CIP breaks", C), (2015, r"the Swiss franc", C),
                   (2018, r"Du--Tepper--Verdelhan", I), (2020, r"negative oil; the basis trade", C),
                   (2022, r"Europe's gas crisis", C), (2024, r"the yen carry unwind", C)]
        strip = era_strip(entries, y0=1980, y1=2027, font_size=15).move_to(DOWN * 0.3)
        head = label(r"How we got here", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 5), (5, 9), (9, 13)]
        with self.voiceover(
            "How we got here. In 1983 Mark Garman and Steven Kohlhagen priced currency options with two interest rates. "
            "In 1984 Eugene Fama found that interest rates predict currencies the wrong way round. In 1986 oil "
            "collapsed, and the new crude futures market priced it. In 1992 sterling was forced out of Europe's "
            "exchange-rate mechanism. <bookmark mark='a'/> America began selling inflation-protected bonds in 1997. In "
            "2006 a hedge fund lost about six billion dollars on natural gas, and Gary Gorton and Geert Rouwenhorst "
            "showed what commodity futures had paid investors. In 2008 covered interest parity, a rule as close to "
            "arbitrage as finance has, stopped holding. <bookmark mark='b'/> Then the franc, a published account of the "
            "parity's failure, oil below zero, the basis trade's unwind in March 2020, Europe's gas crisis, and in "
            "2024, the yen."
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
            r"Covered interest parity derived, measured on 30 years of sterling, and its breakdown after 2008",
            r"Uncovered parity, Fama's puzzle and the carry trade, with its crashes",
            r"FX options: Garman--Kohlhagen, four deltas, the smile from three quotes, vanna--volga",
            r"Pegs and attacks: a first-generation model, Black Wednesday, the franc",
            r"Commodities: storage and convenience, the roll, gas and power, negative oil and Bachelier",
            r"The Treasury basis trade, from futures positions; inflation breakevens and their premium",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: covered interest parity, derived and then measured, and why it broke; uncovered parity, the "
            "puzzle, and the carry trade that lives on it; currency options, with two interest rates and four ways to "
            "say delta, and the smile built from three quotes; pegs and how they are attacked; then commodities: "
            "storage, the roll, gas and power, and the day oil went negative; the Treasury basis trade; and "
            "inflation, priced by the bond market."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=11))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("macro",))
        with self.voiceover(
            "In the House, the macro desk opens: currencies, commodities and inflation, and the trades that connect "
            "them to the rates desk's bonds."
        ):
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["macro"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
