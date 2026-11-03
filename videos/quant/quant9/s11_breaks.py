from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import ARB, CALL, FWD, PART, PUT, Q_C, answer_under, load, pause_at, real_data

# Palm and 3Com, 2 March 2000 (Lamont and Thaler 2003, JPE 111(2); Chicago Booth Review)
PALM, COM3, RATIO = 95.06, 81.81, 1.525
PALM_16MAR, SYNTH_16MAR = 55.25, 39.12


class Breaks(VoiceoverScene):
    def construct(self):
        p = load("parity")
        self.card()
        self.borrow()
        self.palm()
        self.gamestop()
        self.box(p)
        self.predict()

    def card(self):
        c = chapter_card(2, r"Where parity breaks", r"What does a violation of parity put a price on?",
                         lit=(2021,), part=PART)
        with self.voiceover("Chapter two. Where parity breaks."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def borrow(self):
        rows = [cmath(r"\text{A}:\ C + K e^{-rT}", r"\ \longrightarrow\ ", r"\max(S_T, K)", font_size=34,
                      colors={r"\text{A}:\ C + K e^{-rT}": CALL}),
                cmath(r"\text{B}:\ P + e^{-hT}\,\text{shares, lent}", r"\ \longrightarrow\ ", r"\max(S_T, K)",
                      font_size=34, colors={r"\text{B}:\ P + e^{-hT}\,\text{shares, lent}": PUT}),
                cmath(r"C - P", r"=", r"S e^{-hT} - K e^{-rT}", font_size=38, colors={r"C - P": CALL}),
                cmath(r"h", r"=", r"-\frac{1}{T}\ln\frac{C - P + K e^{-rT}}{S}", font_size=36, colors={r"h": ARB})]
        whys = [why(r"the call pays $S_T - K$ above the strike; the bond tops it up to $K$ below", 21),
                why(r"a share lent out earns the borrow fee $h$, so $e^{-hT}$ shares grow to one; the put tops it up "
                    r"below $K$", 21),
                why(r"equal payoffs, equal prices: the fee acts like a dividend the short seller pays", 21),
                why(r"read parity backwards: option prices reveal the fee (Ofek, Richardson and Whitelaw 2004)", 21)]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=0.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "Parity assumed you can sell short, and shorting means borrowing the share, for a fee h "
            "when shares are scarce. Redo the replication. A is a call plus a bond paying the strike: "
            "worth the larger of stock and strike. <bookmark mark='a'/> B is a put plus a fraction of "
            "a share, lent out; the fee grows it to one share by expiry. <bookmark mark='b'/> Same "
            "payoff, same price: the fee acts like a dividend. <bookmark mark='c'/> Read backwards, "
            "option prices reveal the fee. Ofek, Richardson and Whitelaw showed in 2004 that parity's "
            "violations sit where shorting is hardest. They are not free money; they are a price."
            " A worked number: a share at fifty-five, with a fee of thirty percent a year and three "
            "months to go, enters parity as fifty-five times e to the minus point oh seven five: "
            "about fifty-one, not fifty-five."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    def palm(self):
        g = axes([0, 4], [-110, 160], x_length=6.0, y_length=5.2, ylabel=r"dollars per 3Com share, 2 March 2000",
                 xticks=[], yticks=[-50, 0, 50, 100, 150], font_size=16)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.15)
        ax = g.ax
        hold = RATIO * PALM
        stub = COM3 - hold
        b1 = Rectangle(width=1.0, height=ax.c2p(0, COM3)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=FWD,
                       fill_opacity=0.85).move_to(ax.c2p(0.9, COM3 / 2))
        b2 = Rectangle(width=1.0, height=ax.c2p(0, hold)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=CALL,
                       fill_opacity=0.85).move_to(ax.c2p(2.0, hold / 2))
        b3 = Rectangle(width=1.0, height=ax.c2p(0, 0)[1] - ax.c2p(0, stub)[1], stroke_width=0, fill_color=ARB,
                       fill_opacity=0.85).move_to(ax.c2p(3.1, stub / 2))
        zero = Line(ax.c2p(0, 0), ax.c2p(4, 0), color=GREY_C, stroke_width=2)
        l1 = VGroup(label(r"one 3Com share", font_size=17, color=FWD), MathTex(rf"\${COM3:.2f}", font_size=24,
                                                                             color=FWD)).arrange(DOWN, buff=0.06)
        l1.next_to(b1, UP, buff=0.08)
        l2 = VGroup(label(rf"the {RATIO} Palm shares inside it", font_size=17, color=CALL),
                    MathTex(rf"{RATIO} \times {PALM:.2f} = \${hold:.2f}", font_size=22, color=CALL)).arrange(DOWN, buff=0.06)
        l2.next_to(b2, UP, buff=0.08)
        l3 = VGroup(MathTex(rf"-\${abs(stub):.2f}" if stub < 0 else rf"\${stub:.2f}", font_size=24, color=ARB),
                    label(r"everything else 3Com owned", font_size=17, color=ARB)).arrange(DOWN, buff=0.06)
        l3.next_to(b3, DOWN, buff=0.08)
        gap = 1 - SYNTH_16MAR / PALM_16MAR
        side = VGroup(
            wrapped_label(r"3Com sold 5\% of Palm and promised the rest to its own shareholders: about 1.525 Palm "
                          r"shares for each 3Com share", 5.0, 20, GREY_A),
            wrapped_label(r"the market valued the rest of 3Com at about $-\$22$ billion; Palm's short interest "
                          r"reached 147.6\% of its float", 5.0, 20, ARB),
            VGroup(label(r"16 March 2000:", font_size=20, color=GREY_A),
                   MathTex(rf"\text{{Palm }} \${PALM_16MAR:.2f},\ \ \text{{synthetic short via options }} "
                           rf"\${SYNTH_16MAR:.2f}", font_size=24, color=PUT)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            wrapped_label(rf"a gap of {100 * gap:.0f}\% of the share price: what borrowing a Palm share cost over the "
                          r"options' life, read from parity", 5.0, 20, Q_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.45)
        src = real_data(r"Lamont and Thaler (2003), \textit{JPE} 111(2); Chicago Booth Review; Cochrane (2002), NBER w8987")
        with self.voiceover(
            "The famous case. On the second of March 2000, 3Com sold five percent of Palm to the "
            "public and promised the rest to its own shareholders: about one and a half Palm shares "
            "per 3Com share. <bookmark mark='a'/> Palm closed at ninety-five dollars, so the Palm "
            f"inside each 3Com share was worth about {hold:.0f}. <bookmark mark='b'/> 3Com closed at "
            f"eighty-two. The rest of 3Com was priced at minus {abs(stub):.0f} dollars a share, minus "
            "twenty-two billion in all. <bookmark mark='c'/> Buying 3Com and shorting Palm needed "
            "Palm shares to borrow, and short interest reached a hundred and forty-seven percent of "
            "the float. Parity priced the scarcity: on the sixteenth of March, a short built from "
            "options cost thirty-nine dollars against fifty-five for the share. Lamont and Thaler "
            "documented it in 2003."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side[0]), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowFromEdge(b2, DOWN), FadeIn(l2))
            vo.wait_until("b")
            self.play(GrowFromEdge(b1, DOWN), FadeIn(l1))
            self.play(GrowFromEdge(b3, UP), FadeIn(l3), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            self.play(FadeIn(side[3]))
        self.wait(0.3)
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
            "In January 2021, GameStop, heavily shorted, became a Reddit favourite. The SEC's staff "
            "report: up about two thousand seven hundred percent from low to high in January, then "
            "down over eighty-six percent. Melvin Capital, short the stock, needed two point seven "
            "five billion dollars from Citadel and Point72. When borrowing shares is costly or "
            "impossible, that cost shows up in the price of puts."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(src))
        self.wait(0.5)
        self.clear_scene()

    def box(self, p):
        rows = [cmath(r"\text{box}", r"=", r"(C_{K_1} - C_{K_2}) - (P_{K_1} - P_{K_2})", font_size=36,
                      colors={r"\text{box}": Q_C}),
                cmath(r"\text{payoff}", r"=", r"K_2 - K_1 \quad\text{always}\quad\Rightarrow\quad \text{price} = "
                      r"(K_2 - K_1)\,e^{-rT}", font_size=34)]
        whys = [why(r"a long call spread and a short put spread: two parities stacked; the stock and the borrow fee "
                    r"cancel"),
                why(r"a box is a loan; its price is the market's interest rate, and funds use boxes to borrow and lend "
                    r"through the options exchange (chapter 17)")]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=-0.6, buff=0.9, edge=6.9)
        warn = wrapped_label(r"but only with European exercise: in early 2019 a Robinhood customer's box of American "
                             r"options went badly wrong when the short leg was exercised early; Robinhood then "
                             r"banned box spreads, saying they are ``often mistaken for an arbitrage opportunity''",
                             12.0, 22, ARB).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Stack two parities and the stock, and its fee, cancel: a long call spread and a short "
            "put spread, a box, pays the strike difference in every state. <bookmark mark='a'/> So a "
            "box is a loan, and its price is an interest rate; chapter seventeen shows who trades it. "
            "<bookmark mark='b'/> But only with European exercise. In 2019 a Robinhood customer's box "
            "of American options was exercised early and lost far more than it seemed to risk; "
            "Robinhood then banned box spreads."
            " A worked example: strikes a hundred and a hundred and ten, one year, four percent. The "
            "box pays ten for sure, so it costs ten times e to the minus point oh four, about nine "
            "sixty-one; buying it is lending at four percent."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(warn))
        self.wait(0.4)
        self.clear_scene()

    def predict(self):
        card = pause_at(r"The stub was negative for weeks. Why did no one simply buy 3Com and short Palm until the "
                        r"gap closed?")
        with self.voiceover(
            "Pause and predict. The stub stayed negative for weeks. Why not buy 3Com, short Palm, and "
            "wait? <bookmark mark='a'/> The short leg was scarce, costly and recallable, and "
            "convergence has no deadline: in thirty percent of eighty-two negative stubs from 1985 to "
            "2000, the link was severed before the gap closed."
            " Next: the rule behind every one of these trades, seen as geometry."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, r"the short leg: scarce, costly, recallable shares; and in 30\% of 82 "
                                                r"negative-stub cases (1985--2000) the link was severed before "
                                                r"convergence (Mitchell, Pulvino and Stafford 2002)")))
        self.wait(0.4)
        self.clear_scene()
