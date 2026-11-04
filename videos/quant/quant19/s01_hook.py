from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant19.common import BAD, PART, POLICY, ZERO, era_strip, illustration, load


class Hook(VoiceoverScene):
    def construct(self):
        y = load("y1994")
        self.title_card()
        self.massacre(y)
        self.orange(y)
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"When the curve moves")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part nineteen. Term-structure models. Part eighteen built the curve as a snapshot; now it moves, at "
            "random, and the options on it get prices."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def massacre(self, y):
        t, y2, y10 = np.asarray(y["t"]), np.asarray(y["y2"]), np.asarray(y["y10"])
        ft, ff = np.asarray(y["ff_t"]), np.asarray(y["ff"])
        g = axes([1993.45, 1996], [2, 9], x_length=7.6, y_length=4.4, xlabel=r"year", ylabel=r"percent",
                 xticks=[1994, 1995], yticks=[2, 4, 6, 8], font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lf = curve(ax, ft, ff, POLICY, stroke_width=3)
        l2 = curve(ax, t, y2, QC.SPOT, stroke_width=2.5)
        l10 = curve(ax, t, y10, ZERO, stroke_width=2.5)
        leg = legend([(POLICY, r"fed funds target"), (QC.SPOT, r"2-year zero yield"), (ZERO, r"10-year zero yield")],
                     font_size=18).to_edge(RIGHT, buff=0.5).shift(UP * 1.6)
        k0, k1 = int(np.searchsorted(t, 1994.0)), int(np.searchsorted(t, 1994.99))
        side = VGroup(
            wrapped_label(r"4 February 1994: the first hike in five years, a quarter point; six more followed, to 6\% "
                          r"by February 1995", 4.0, 19, POLICY),
            MathTex(rf"\Delta y^{{(2)}}_{{1994}} = {y2[k1] - y2[k0]:+.2f},\quad \Delta y^{{(10)}}_{{1994}} = "
                    rf"{y10[k1] - y10[k0]:+.2f}", font_size=28),
            wrapped_label(r"``the great bond massacre'', as a Fortune article called it that October", 4.0, 19, BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(leg, DOWN, buff=0.5, aligned_edge=LEFT)
        side.shift(LEFT * max(0.0, side.get_right()[0] - 6.75))
        with self.voiceover(
            "February 1994. The Federal Reserve raised rates for the first time in five years, by a quarter of a "
            "point. <bookmark mark='a'/> Then six more times, to six percent by February 1995. "
            "<bookmark mark='b'/> The two-year yield rose "
            f"{y2[k1] - y2[k0]:.1f} points in 1994 and the ten-year {y10[k1] - y10[k0]:.1f}. Bond prices fell across the "
            "world; that October a Fortune article called it the great bond massacre."
        ) as vo:
            self.play(FadeIn(g), Create(lf), FadeIn(leg[0]), FadeIn(side[0]), run_time=2)
            vo.wait_until("a")
            self.play(Create(l2), Create(l10), FadeIn(leg[1]), FadeIn(leg[2]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.add(illustration(r"FRED: DFEDTAR; the Fed's GSW curve"))
        self.wait(0.4)
        self.clear_scene()

    def orange(self, y):
        p = y["pool"]
        cc = crisis_card(r"6 December 1994", r"Orange County files for bankruptcy",
                         rf"the county treasurer's investment pools borrowed against their bonds by reverse repo, "
                         rf"roughly {p['leverage']:.2f} times their deposits, and bought more notes, many of them "
                         r"inverse floaters, whose coupons fall when rates rise. A bet that rates would stay low",
                         stats=[(rf"\${p['assets']}\,\text{{bn}}", r"securities, June 1994"),
                                (rf"\${p['equity']}\,\text{{bn}}", r"participants' deposits"),
                                (rf"\${p['repo']}\,\text{{bn}}", r"reverse repo"),
                                (r"\$1.5\text{--}1.7\,\text{bn}", r"reported loss")], width=7.6, font_size=21)
        cc.to_edge(LEFT, buff=0.4)
        lo, hi = p["implied_duration"]
        side = VGroup(
            wrapped_label(rf"chapter 6 of Part 18, backwards: a loss of \$1.5--1.7 bn on \${p['assets']} bn, after a "
                          rf"{100 * y['dy5']:.1f}-point rise in the 5-year yield, means an average duration of "
                          rf"{lo:.1f}--{hi:.1f} years", 4.4, 19, GREY_A),
            wrapped_label(r"Pause and predict: what did a 1994 option on rates need to know that a bond's duration does "
                          r"not tell you?", 4.4, 21, QC.IDEA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The most famous casualty was Orange County, California. Its treasurer ran investment pools for the county "
            f"and its towns: about {p['equity']} billion dollars of their money, borrowed against by reverse repo to "
            f"hold {p['assets']} billion of securities, by the SEC's account, many of them inverse floaters, whose "
            "coupons fall when rates rise. <bookmark mark='a'/> The losses were reported at one and a half to one point "
            "seven billion dollars, and on the sixth of December 1994 the county filed for bankruptcy. Part eighteen's "
            f"arithmetic, run backwards, says the pool's duration was about {lo:.0f} to {hi:.0f} years. "
            "<bookmark mark='b'/> But a duration is a single number for a single, sudden move. To price an option on "
            "rates you need to know how the whole curve can move, and how likely each path is. That is a "
            "term-structure model."
        ) as vo:
            self.play(FadeIn(cc))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
        self.add(illustration(r"SEC administrative proceedings on the Orange County pools; reported losses vary by source"))
        self.wait(0.5)
        self.clear_scene()

    def history(self):
        I, F, C, R_ = QC.IDEA, QC.FIRM, QC.CRISIS, QC.HOUSE
        entries = [(1976, r"Black: options on futures", I), (1977, r"Vasicek", I), (1985, r"Cox--Ingersoll--Ross", I),
                   (1986, r"Ho--Lee", I), (1989, r"Jamshidian", I), (1990, r"Hull--White", I), (1992, r"HJM", I),
                   (1994, r"the bond massacre", C), (1996, r"Duffie--Kan", I), (1997, r"LIBOR market model", I),
                   (2001, r"Longstaff--Schwartz", I), (2002, r"SABR", I), (2005, r"Cochrane--Piazzesi", I),
                   (2008, r"two curves", R_), (2014, r"the ECB below zero", C), (2019, r"FMM for SOFR", I),
                   (2020, r"Bachelier", R_)]
        strip = era_strip(entries, y0=1972, y1=2026, font_size=15).move_to(DOWN * 0.3)
        head = label(r"How we got here", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 5), (5, 10), (10, 13), (13, 17)]
        with self.voiceover(
            "How we got here. In 1976 Fischer Black priced options on futures, the formula still used to quote caps and "
            "swaptions. In 1977 Oldrich Vasicek wrote the short rate as a mean-reverting random walk; in 1985 Cox, "
            "Ingersoll and Ross kept it positive; in 1986 Ho and Lee fitted a model to the whole curve. "
            "<bookmark mark='a'/> Farshid Jamshidian priced bond options in such models in 1989; Hull and White "
            "generalized Vasicek in 1990; Heath, Jarrow and Morton in 1992 modelled the entire forward curve at once. "
            "Then 1994 tested them all. In 1996 Duffie and Kan unified the affine models, and in 1997 the LIBOR market "
            "model made the market's own Black formulas consistent. <bookmark mark='b'/> In 2001 Longstaff and Schwartz "
            "gave callable products a simulation method; in 2002 SABR gave the smile a model; in 2005 Cochrane and "
            "Piazzesi found one factor that forecasts bond returns. <bookmark mark='c'/> Then the world changed: two "
            "curves after 2008, the European Central Bank's negative rates from 2014, a forward model for SOFR in 2019, and in 2020 "
            "options priced in absolute, Bachelier volatility."
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
            r"Short-rate models fitted to the bill rate: Vasicek, CIR, and the affine family",
            r"Hull--White fitted exactly to today's curve, its volatility calibrated to the curve's history",
            r"HJM: why the drift of every forward rate is fixed by its volatility, simulated with Part 18's factors",
            r"Caps, floors and swaptions; Black against Bachelier; negative rates; SABR for rates",
            r"Market models for LIBOR and SOFR; Bermudan swaptions and their exercise boundary",
            r"Two curves after 2008; what forecasts bond returns, tested on a sealed hold-out",
            r"Mortgages: prepayment and negative convexity",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan, in seven steps: short-rate models, fitted to data; Hull and White, fitted to today's curve; the "
            "HJM condition; the market's options and how they are quoted, including at negative rates; market models "
            "and callable swaptions; the curves after 2008 and what forecasts bond returns; and mortgages, the "
            "largest negatively convex market in the world."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("rates",))
        with self.voiceover(
            "In the House, the rates desk gets its option pricers: every one fitted to the curve built in Part "
            "eighteen, and every one checked against a second method."
        ):
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["rates"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
