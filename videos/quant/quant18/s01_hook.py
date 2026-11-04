from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant18.common import BAD, PART, ZERO, era_strip, illustration, load


class Hook(VoiceoverScene):
    def construct(self):
        v = load("svb")
        self.title_card()
        self.teaser(v)
        self.question(v)
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"The price of time")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part eighteen. Money, bonds and the curve. What a central bank actually sets, what a bond's price says "
            "about every future date, and how the whole curve of interest rates moves."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def teaser(self, v):
        t, y6, mark = np.asarray(v["t"]), np.asarray(v["y6"]), np.asarray(v["mark"])
        f = v["facts"]
        htm = f["HeldToMaturitySecurities"]["2022-12-31"]
        loss = f["HeldToMaturitySecuritiesAccumulatedUnrecognizedHoldingLoss"]["2022-12-31"]
        eq = f["StockholdersEquity"]["2022-12-31"]
        top = axes([2022, 2023.2], [0, 5], x_length=6.2, y_length=2.0, ylabel=r"6-year zero yield, \%",
                   xticks=[2022, 2023], yticks=[0, 2.5, 5], font_size=14)
        bot = axes([2022, 2023.2], [-20, 2], x_length=6.2, y_length=3.0, xlabel=r"date",
                   ylabel=r"mark of a 6.2-year book of \$91 bn, \$ bn", xticks=[2022, 2023], yticks=[-20, -10, 0],
                   font_size=14)
        VGroup(top, bot).arrange(DOWN, buff=0.35, aligned_edge=LEFT).to_edge(LEFT, buff=0.7)
        m = t <= 2023.2
        yl = curve(top.ax, t[m], y6[m], ZERO, stroke_width=3)
        ml = curve(bot.ax, t[m], mark[m] * -1, BAD, stroke_width=3)
        eqline = DashedLine(bot.ax.c2p(2022, -eq), bot.ax.c2p(2023.2, -eq), color=WHITE, stroke_width=2)
        eqlab = label(rf"minus the bank's equity, \${eq:.1f} bn", font_size=16, color=WHITE).next_to(
            eqline, UP, buff=0.06).align_to(eqline, LEFT)
        side = VGroup(
            label(r"Silicon Valley Bank, 31 December 2022", font_size=24),
            wrapped_label(r"held to maturity: Treasuries and agency mortgage bonds, safe from default", 5.0, 20, GREY_A),
            MathTex(rf"\text{{book value}}\ \ {htm:.1f}\ \ \text{{fair value}}\ \ "
                    rf"{f['HeldToMaturitySecuritiesFairValue']['2022-12-31']:.1f}", font_size=28),
            MathTex(rf"\text{{unrealized loss}}\ \ {loss:.2f}\ \ \text{{vs equity}}\ \ {eq:.2f}", font_size=28,
                    color=BAD),
            label(r"\$ billion, from its 10-K (EDGAR XBRL)", font_size=17, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.45)
        src = illustration(r"yields: the Fed's fitted Treasury curve (GSW); mark: duration $\times$ yield change")
        with self.voiceover(
            "At the end of 2022, Silicon Valley Bank held ninety-one billion dollars of bonds it meant to keep until "
            "they matured: Treasuries and government-backed mortgage bonds, with essentially no risk of default. "
            "<bookmark mark='a'/> Through 2022 the six-year Treasury yield rose by "
            f"{v['dy6_2022_pct']:.1f} percentage points. "
            "<bookmark mark='b'/> A book with a duration of six point two years loses about six point two percent of "
            "its value for every point the yield rises. Here is that mark, day by day. <bookmark mark='c'/> By its own "
            f"10-K, the loss at year end was {loss:.2f} billion dollars. The bank's equity was {eq:.2f} billion."
        ) as vo:
            self.play(FadeIn(top), FadeIn(bot), FadeIn(side[0]), FadeIn(side[1]), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(yl), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(ml), FadeIn(side[2]), run_time=3)
            vo.wait_until("c")
            self.play(Create(eqline), FadeIn(eqlab), FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.5)
        self.clear_scene()

    def question(self, v):
        r = v["review"]
        q = VGroup(label(r"Nothing defaulted. The bank still failed.", font_size=34),
                   wrapped_label(rf"8 March 2023: it sold \${r['afs_sold_bn']} bn of bonds at a \${r['afs_loss_bn']} bn "
                                 rf"loss. 9 March: depositors withdrew over \${r['outflow_mar9_bn']} bn. 10 March: "
                                 r"closed (Federal Reserve review, April 2023)", 11.0, 24, GREY_A),
                   label(r"Pause and predict: how does the safest asset in the world sink a bank?", font_size=28,
                         color=QC.IDEA)).arrange(DOWN, buff=0.5)
        with self.voiceover(
            "Nothing defaulted, and the bank still failed. On the eighth of March 2023 it sold twenty-one billion of "
            "bonds at a loss of one point eight billion. The next day depositors pulled out over forty billion "
            "dollars, and on the tenth it was closed. <bookmark mark='a'/> A question to carry through the part: how "
            "does the safest asset in the world sink a bank? Chapter six gives the arithmetic, and chapter eighteen "
            "tells the story."
        ) as vo:
            self.play(FadeIn(q[0]), FadeIn(q[1]))
            vo.wait_until("a")
            self.play(FadeIn(q[2]))
        self.wait(0.5)
        self.clear_scene()

    def history(self):
        I, F, C, R_ = QC.IDEA, QC.FIRM, QC.CRISIS, QC.HOUSE
        entries = [(1938, r"Macaulay: duration", I), (1952, r"Redington: immunization", I),
                   (1979, r"Volcker targets money", F), (1987, r"Nelson--Siegel", I),
                   (1991, r"level, slope, curvature; Salomon's auction scandal", I), (1993, r"Taylor rule", I),
                   (1994, r"LTCM founded", F), (2008, r"interest on reserves", R_), (2012, r"LIBOR scandal", C),
                   (2017, r"SOFR chosen", R_), (2019, r"repo spike", C), (2022, r"gilts and LDI; QT", C),
                   (2023, r"SVB", C), (2025, r"QT ends", R_)]
        strip = era_strip(entries, y0=1935, y1=2028, font_size=16).move_to(DOWN * 0.3)
        head = label(r"How we got here", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 2), (2, 7), (7, 10), (10, 14)]
        with self.voiceover(
            "How we got here. In 1938 Frederick Macaulay defined duration, the average time you wait for a bond's "
            "money. In 1952 the actuary Frank Redington showed how to immunize a pension fund against rates. "
            "<bookmark mark='a'/> In 1979 Paul Volcker's Fed let rates go where they had to, and the curve became the "
            "thing to model: Nelson and Siegel fitted it in 1987, and Litterman and Scheinkman found in 1991 that "
            "three factors move it. That year Salomon Brothers' bond desk was caught breaking the Treasury's auction "
            "rules; in 1993 John Taylor wrote down a rule for the policy rate; in 1994 Salomon's former arbitrage "
            "chief founded Long-Term Capital Management. <bookmark mark='b'/> In 2008 the Fed began paying interest "
            "on reserves, which changed how it sets rates. LIBOR's manipulation came out in 2012, and in 2017 a new "
            "benchmark, SOFR, was chosen to replace it. <bookmark mark='c'/> Then the plumbing broke, again and again: "
            "the repo spike of 2019, Britain's pension funds in 2022, Silicon Valley Bank in 2023. And in December "
            "2025 the Fed stopped shrinking its balance sheet."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), m in zip(groups, [None, "a", "b", "c"]):
                if m:
                    vo.wait_until(m)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.4),
                          run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Money: what the Fed sets, the floor system, QE and QT, and Taylor's rule",
            r"Bonds: yields, zero and forward rates, day counts; a curve bootstrapped from Treasury's quotes",
            r"Duration and convexity, key rates, and Redington's immunization",
            r"Fitting the curve (Nelson--Siegel--Svensson) and fifty years of it; level, slope and curvature",
            r"Swaps, Treasury futures, repo and SOFR: the instruments a rates desk trades",
            r"Expectations against the term premium, re-estimated; what FOMC days do to the curve",
            r"Relative value: a butterfly, pre-registered and tested on a sealed hold-out",
            r"Two crises from public records: the gilt spiral of 2022 and Silicon Valley Bank",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan, in eight steps: money and the central bank; bonds and the curve built from real quotes; "
            "duration, convexity and immunization; the curve fitted and its fifty-year history, and the three factors "
            "that move it; the instruments a rates desk trades; what the curve expects and what it charges for "
            "waiting; one relative-value trade, tested honestly; and two crises, from the public record."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=14))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("rates",))
        with self.voiceover(
            "In the House, the rates desk opens. Its first tool is a curve builder that every later part prices off: "
            "credit, macro, and the firm's own funding. <bookmark mark='a'/> And its first rule is about how a rates "
            "position is measured."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["rates"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
