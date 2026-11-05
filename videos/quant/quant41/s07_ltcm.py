from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant41.common import (BAD, FUND_C, GOOD, HURDLE, LEV_C, PART, PRICE_C, SAFE_C, SPIRAL_C, load)


def _t(d):
    d = np.array([int(str(x).replace("-", "")[:8]) for x in d])
    return (d // 10000) + ((d // 100) % 100 - 1) / 12 + (d % 100) / 365


class LTCM(VoiceoverScene):
    def construct(self):
        x = load("ltcm")
        self.card(x)
        self.book(x)
        self.crowd()
        self.spread(x)
        self.rescue()
        self.lessons()
        self.question()

    def card(self, x):
        c = chapter_card(6, r"1998: Long-Term Capital Management", r"What happens when everyone holds the same trade?",
                         part=PART)
        with self.voiceover(
            f"Chapter six, and the answer to the pause: a loss of about {100 * x['wipe']:.1f} percent of its assets, at "
            f"{x['lev']:.0f} times leverage, as reported. And the sellers would have been everyone who held the same "
            "trades, and the banks that had lent against them: which is why the Federal Reserve brought the lenders "
            "together rather than let them run. Part ten told the story of the fund; this chapter is its mechanics."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def book(self, x):
        rows = [cmath(r"\text{assets, equity}", r":", rf"\${x['A']:.0f}\text{{bn}},\ \${x['E']:.1f}\text{{bn}}", font_size=40,
                      colors={r"\text{assets, equity}": LEV_C}),
                cmath(r"\lambda", r"\approx", rf"{x['lev']:.0f}", font_size=44),
                cmath(r"\text{plus}", r":", r"\text{about \$1.25 trillion of derivatives notional}", font_size=36),
                cmath(r"\text{trades}", r":", r"\text{convergence: on-the-run against off-the-run, swap spreads, ...}",
                      font_size=32, colors={r"\text{trades}": PRICE_C})]
        whys = [why(r"early 1998, as the President's Working Group reported in 1999"),
                why(r"a 4\% fall in the value of its assets would erase its capital"),
                why(r"off-balance-sheet swaps and options, financed with almost no initial margin from its dealers"),
                why(r"bets that similar securities would converge in price: small, safe-looking spreads, made worthwhile "
                    r"by leverage")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The book, as reported in nineteen ninety-nine. <bookmark mark='a'/> A hundred and twenty-five billion dollars "
            f"of assets on four point seven billion of capital: <bookmark mark='b'/> about {x['lev']:.0f} times. "
            "<bookmark mark='c'/> Plus about a trillion and a quarter of derivatives, financed with little initial margin. "
            "<bookmark mark='d'/> And the trades were convergence bets: small spreads between similar securities, made "
            "worth having by leverage."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def crowd(self):
        cards = VGroup(
            desk_question(r"the same trades elsewhere", r"dealers' proprietary desks and other funds held similar positions, "
                          r"so the spreads LTCM bet on were crowded", width=12.4, font_size=19),
            desk_question(r"a shock elsewhere", r"Russia's default in August 1998 sent investors to the most liquid "
                          r"securities; every convergence spread widened at once, as reported", width=12.4, font_size=19),
            desk_question(r"correlations went to one", r"positions that looked diversified across markets were the same "
                          r"bet on liquidity: Chapter 3's common holdings, Chapter 2's spiral", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why it failed together. <bookmark mark='a'/> Dealers' own desks and other funds held similar positions, so "
            "the spreads were crowded. <bookmark mark='b'/> Russia's default in August nineteen ninety-eight sent investors "
            "to the most liquid securities, and every convergence spread widened at once, as reported. "
            "<bookmark mark='c'/> Positions that looked diversified across countries and markets were one bet on "
            "liquidity: common holdings, and a spiral."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def spread(self, x):
        t = _t(x["baa"]["d"])
        v = np.asarray(x["baa"]["v"], float)
        g = axes([1998, 1999], [1.4, 3.0], x_length=7.6, y_length=4.0, xlabel=r"1998",
                 ylabel=r"Moody's Baa over the 10-year Treasury, \%", xticks=[1998, 1999], yticks=[1.5, 2.0, 2.5, 3.0],
                 font_size=15).move_to(LEFT * 0.8 + DOWN * 0.2)
        ax = g.ax
        line = curve(ax, t, v, SPIRAL_C, stroke_width=2.5)
        marks = VGroup(label(r"17 Aug: Russia defaults", font_size=17, color=GREY_A),
                       label(r"23 Sep: the recapitalisation", font_size=17, color=SAFE_C))
        marks.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.7).shift(RIGHT * 1.2)
        with self.voiceover(
            "One of the spreads, from public data. <bookmark mark='a'/> The yield of Baa-rated corporate bonds over the "
            f"ten-year Treasury sat near {x['baa']['pre']:.1f} percentage points at the start of August. "
            f"<bookmark mark='b'/> By October it had reached {x['baa']['max']:.1f}, while the Treasury yield fell to "
            f"{x['y10']['min']:.2f} percent as investors fled to it: the flight to quality that every convergence trade "
            "was short."
        ) as vo:
            self.play(FadeIn(g), FadeIn(marks[0]))
            vo.wait_until("a")
            self.play(Create(line), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(marks[1]))
        self.wait(0.4)
        self.clear_scene()

    def rescue(self):
        cards = VGroup(
            desk_question(r"not a bailout", r"on 23 September 1998 fourteen banks, convened by the New York Fed, put in "
                          r"\$3.6 billion for 90\% of the fund; no public money was lent, as the Fed testified", width=12.4,
                          font_size=19),
            desk_question(r"why the creditors agreed", r"liquidating the book at once would have forced them to sell the "
                          r"same positions into the same market: a coordinated fire sale avoided", width=12.4, font_size=19),
            desk_question(r"and the Fed cut rates", r"three times that autumn, as reported; the precedent of rescue was "
                          r"debated for a decade", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The resolution. <bookmark mark='a'/> On the twenty-third of September, fourteen banks, convened by the New "
            "York Fed, put in three point six billion dollars for ninety percent of the fund, with no public money lent, "
            "as the Fed testified. <bookmark mark='b'/> They agreed because liquidating the book at once would have forced "
            "all of them to sell the same positions into the same market: a coordinated fire sale avoided. "
            "<bookmark mark='c'/> And the Fed cut rates three times that autumn, a precedent debated for a decade."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"leverage turns small risks into large ones", r"a 4\% move in assets that rarely moved 4\% "
                          r"ended a fund that its own models said was safe", width=12.4, font_size=19),
            desk_question(r"the counterparty sees only its slice", r"each dealer knew its own exposure, not the whole "
                          r"book: Part 21's argument for margin and central clearing", width=12.4, font_size=19),
            desk_question(r"liquidity is a common factor", r"what looked like many independent bets was one bet on "
                          r"funding, which Part 40's VaR, fitted to calm years, could not see", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three lessons. <bookmark mark='a'/> Leverage turns small risks into large ones: a four percent move in assets "
            "that rarely moved four percent ended the fund. <bookmark mark='b'/> Each lender saw only its own slice of the "
            "book, Part twenty-one's argument for margin and clearing. <bookmark mark='c'/> And liquidity is a common "
            "factor: many independent-looking bets were one bet on funding, which a VaR fitted to calm years could not "
            "see."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"the TED spread, the gap between three-month interbank and Treasury rates, averaged under half a "
                       r"percentage point before 2007. How high did it go in October 2008, and what does it measure?")
        with self.voiceover(
            "Pause and predict. The TED spread, the gap between three-month interbank lending rates and Treasury bills, "
            "averaged under half a percentage point before twenty oh seven. How high did it go in October twenty oh "
            "eight, and what does it measure?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
