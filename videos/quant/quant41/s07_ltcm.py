from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant41.common import ladder
from videos.quant.quant41.common import (BAD, FUND_C, GOOD, HURDLE, LEV_C, PART, PRICE_C, SAFE_C, SPIRAL_C, load)


def _t(d):
    from videos.quant.quant41.common import calendar_year
    return calendar_year(d)


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
            f"""Chapter six. Dividing reported capital of four point seven billion dollars by assets of one hundred twenty-five billion gives {100 * x['wipe']:.1f} percent. A uniform asset-value fall of that size exhausts equity under fixed debt, at {x['lev']:.0f} times leverage. It is not a spread-basis-point threshold or a full derivatives loss model: those need duration, convexity, offsets and financing terms. Common positions and counterparty exposures made a rapid liquidation dangerous, helping motivate a privately financed recapitalization facilitated by the New York Fed."""
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
                why('gross derivatives notional is a scale measure, not net market exposure, loss-at-risk or assets that can be added to the balance sheet'),
                why(r"bets that similar securities would converge in price: small, safe-looking spreads, made worthwhile "
                    r"by leverage")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            f"""The book as historically reported. <bookmark mark='a'/> One hundred twenty-five billion dollars of assets and four point seven billion of capital. <bookmark mark='b'/> That is about {x['lev']:.0f} times balance-sheet leverage. <bookmark mark='c'/> Gross derivatives notional was about one point two five trillion dollars. Notional measures contractual scale, not net market exposure or a loss amount, and cannot simply be added to balance-sheet assets. <bookmark mark='d'/> Positions included convergence trades between related securities. Their risks depended on sensitivities, basis, crowding and financing, rather than the apparent small spread alone."""
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
            desk_question(r"a shock elsewhere", "Russia's default in August 1998 sent investors to the most liquid securities; many convergence positions suffered together; individual spreads and sensitivities differed", width=12.4, font_size=19),
            desk_question('common liquidity exposure', r"positions that looked diversified across markets were the same "
                          r"bet on liquidity: Chapter 3's common holdings, Chapter 2's spiral", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why apparently diversified positions can suffer together. <bookmark mark='a'/> Other funds and dealers held similar relative-value positions, making liquidation crowded. <bookmark mark='b'/> Russia's August nineteen ninety-eight default accompanied a broad flight toward liquidity; many convergence positions lost together. This is not evidence that every spread widened or every correlation equaled one. <bookmark mark='c'/> Shared funding and liquidation exposure can connect positions across countries and asset classes, even without identical underlying cash flows."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
                else:
                    self.play(Indicate(cards[0], color=HURDLE, scale_factor=1.0))
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
            f"""One descriptive public yield difference. <bookmark mark='a'/> Baa corporate yields minus the ten-year Treasury were near {x['baa']['pre']:.1f} percentage points at the selected early-August observation. <bookmark mark='b'/> The difference reached {x['baa']['max']:.1f}, while the Treasury yield's annual minimum was {x['y10']['min']:.2f} percent. Those peaks and lows need not occur on the same day. The series combines credit, liquidity and maturity effects; it is not LTCM's complete book or evidence that every convergence trade had identical exposure."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(marks[0]), Create(line))
            vo.wait_until("a")
            self.play(Indicate(line, color=HURDLE), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(marks[1]))
        self.wait(0.4)
        self.clear_scene()

    def rescue(self):
        cards = VGroup(
            desk_question('privately funded recapitalization', r"on 23 September 1998 fourteen banks, convened by the New York Fed, put in "
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
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
                else:
                    self.play(Indicate(cards[0], color=HURDLE, scale_factor=1.0))
        self.wait(0.4)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"leverage turns small risks into large ones", "the 4\\% uniform-loss bridge illustrates thin equity; it does not reproduce the fund's realized multi-instrument losses", width=12.4, font_size=19),
            desk_question(r"the counterparty sees only its slice", r"each dealer knew its own exposure, not the whole "
                          r"book: Part 21's argument for margin and central clearing", width=12.4, font_size=19),
            desk_question(r"liquidity is a common factor", r"what looked like many independent bets was one bet on "
                          r"funding, which Part 40's VaR, fitted to calm years, could not see", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three lessons. <bookmark mark='a'/> Thin equity amplifies asset losses. The roughly four-percent uniform-loss calculation is a balance-sheet bridge, not a reconstruction of LTCM's actual trading losses. <bookmark mark='b'/> Each lender saw only part of the aggregate book, complicating counterparty risk management. <bookmark mark='c'/> Funding and liquidation can be common risk factors. Calm-window risk estimates can miss their stressed behavior; neither diversification nor a low recent VaR proves that exit liquidity will remain available."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
                else:
                    self.play(Indicate(cards[0], color=HURDLE, scale_factor=1.0))
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
        self.wait(6.0)
        self.clear_scene()
