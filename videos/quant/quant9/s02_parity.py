from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import ALT, ARB, CALL, FWD, PART, PUT, Q_C, load, real_data


class Parity(VoiceoverScene):
    def construct(self):
        self.card()
        self.borrow()
        self.gamestop()
        self.box()

    def card(self):
        c = chapter_card(1, r"Arbitrage, parity, and where it breaks", r"When is a free lunch not free?", part=PART)
        with self.voiceover("Chapter one. Arbitrage, parity, and where it breaks."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def borrow(self):
        rows = [cmath(r"\text{arbitrage}", r":", r"\text{cost} \le 0,\quad \text{payoff} \ge 0,\quad \text{payoff} > 0 "
                      r"\text{ sometimes}", font_size=34, colors={r"\text{arbitrage}": ARB}),
                cmath(r"C - P", r"=", r"S\,e^{-hT} - K e^{-rT}", font_size=38, colors={r"C - P": CALL}),
                cmath(r"h", r"=", r"-\frac{1}{T}\log\frac{C - P + K e^{-rT}}{S}", font_size=36, colors={r"h": PUT})]
        whys = [why(r"no money down, no chance of loss, some chance of gain; the law of one price follows: equal "
                    r"payoffs, equal prices"),
                why(r"parity assumes you can short the stock; if borrowing it costs a fee $h$ a year, the forward is "
                    r"lower and puts are dearer"),
                why(r"read backwards, option prices reveal the borrow fee: Ofek, Richardson and Whitelaw (2004) found "
                    r"parity's violations where shorting was hardest")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "An arbitrage is a trade that costs nothing, can never lose, and sometimes wins. If none exist, two "
            "things with the same payoff must have the same price: the law of one price. <bookmark mark='a'/> "
            "Parity assumes you can sell the stock short, and shorting means borrowing it from someone who owns "
            "it. When shares are scarce, lenders charge a fee, and the fee works like a dividend you must pay: the "
            "forward is lower, and puts are dearer than calls. <bookmark mark='b'/> Turn the formula around and "
            "option prices reveal the borrowing fee. In 2004 Eli Ofek, Matthew Richardson and Robert Whitelaw "
            "showed that parity's apparent violations line up with how hard a stock is to short. They are not free "
            "money; they are a price."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def gamestop(self):
        card = crisis_card(
            r"January 2021", r"GameStop",
            r"A video-game retailer, heavily shorted, became the favourite of a Reddit forum. Its share price rose "
            r"about 2{,}700\% from its intraday low on 8 January to its intraday high on 28 January, then fell more "
            r"than 86\% into early February. The hedge fund Melvin Capital, short the stock, took a \$2.75 billion "
            r"injection from Citadel and Point72 and lost 53\% in January. Brokers restricted buying on 28 January. "
            r"The SEC's staff found that enthusiasm, not short sellers buying to cover, sustained the rise.",
            stats=[(r"\approx 2{,}700\%", r"low on 8 Jan.\ to high on 28 Jan."), (r"> 86\%", r"the fall into "
                                                                                       r"February"),
                   (r"\$2.75\text{bn}", r"for Melvin Capital")],
            width=11.0, font_size=25)
        card.move_to(ORIGIN)
        src = note(r"SEC staff report on equity and options market structure conditions in early 2021 (October "
                   r"2021); Reuters", font_size=18, color=GREY_B).to_corner(DR, buff=0.25)
        with self.voiceover(
            "In January 2021 the stock of GameStop, a video-game retailer that many funds had sold short, became the "
            "favourite of a Reddit forum. According to the SEC's staff report, its price rose about two thousand "
            "seven hundred percent from its low on the eighth of January to its high on the twenty-eighth, then fell "
            "more than eighty-six percent into February. The hedge fund Melvin Capital, short the stock, needed two "
            "point seven five billion dollars from Citadel and Point72, and lost fifty-three percent in the month. "
            "The SEC's staff found that buying to cover short positions was not what sustained the rise; it was "
            "enthusiasm. For anyone who wanted to bet against it, parity says where to look: when borrowing shares "
            "is costly or impossible, that cost appears in the price of puts."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(src))
        self.wait(0.5)
        self.clear_scene()

    def box(self):
        rows = [cmath(r"\text{box}", r"=", r"(C_{K_1} - C_{K_2}) - (P_{K_1} - P_{K_2})", font_size=36,
                      colors={r"\text{box}": Q_C}),
                cmath(r"\text{payoff}", r"=", r"K_2 - K_1 \quad\text{always}\quad\Rightarrow\quad \text{price} = "
                      r"(K_2 - K_1)\,e^{-rT}", font_size=34)]
        whys = [why(r"a long call spread and a short put spread: two parities stacked; the stock cancels"),
                why(r"a box is a loan; its price is the market's interest rate, and funds use boxes to borrow and lend "
                    r"through the options exchange")]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=-0.6, buff=0.9, edge=6.9)
        warn = wrapped_label(r"but only with European exercise: in early 2019 a Robinhood customer's box of American "
                             r"options went badly wrong when the short leg was exercised early; Robinhood then "
                             r"banned box spreads, saying they are ``often mistaken for an arbitrage opportunity''",
                             12.0, 22, ARB).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Stack two parities and the stock cancels. A long call spread and a short put spread between the same "
            "two strikes is called a box, and it pays the difference between the strikes in every state of the "
            "world. <bookmark mark='a'/> So a box is a loan, and its price is an interest rate; funds use boxes to "
            "borrow and lend through the options exchange. <bookmark mark='b'/> But the argument needs European "
            "exercise. In early 2019 a Robinhood customer built a box from American options, the short leg was "
            "exercised early, and the customer lost far more than the trade seemed to risk. Robinhood then banned box spreads, "
            "saying they are often mistaken for an arbitrage opportunity. Every no-arbitrage argument comes with "
            "assumptions, and the market tests them."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(warn))
        self.wait(0.4)
        self.clear_scene()
