from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import ARB, CALL, FWD, PART, PUT, Q_C, load, real_data


class Hook(VoiceoverScene):
    def construct(self):
        p = load("parity")
        self.title_card()
        self.question()
        self.bitcoin(p)
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"One price")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part nine. No arbitrage. The toolkit is complete, and the derivatives act begins with one idea, from "
            "which the rest of option pricing follows: two ways to get the same payoff must cost the same."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def question(self):
        q = desk_question(r"A call costs 10 and a put 7, both struck at 100 with the same expiry. The stock is at 103 "
                          r"and interest rates are zero. Is there an arbitrage?", width=10.6, font_size=28)
        q.to_edge(UP, buff=0.5)
        rows = [cmath(r"C - P", r"=", r"S - K e^{-rT}", font_size=40, colors={r"C - P": CALL}),
                cmath(r"10 - 7", r"=", r"103 - 100", font_size=40, colors={r"10 - 7": CALL})]
        whys = [why(r"a call minus a put pays $S_T - K$ in every state: exactly a forward; so it must cost what a "
                    r"forward costs (Stoll 1969)"),
                why(r"both sides are 3: no arbitrage. At a put price of 6, buy the put, sell the call, buy the stock, "
                    r"borrow 99: lock in 1")]
        step = ladder(self, rows, whys, keep=2, top=1.0, x=-0.6, buff=0.95, edge=6.9)
        with self.voiceover(
            "A question from a trading-desk interview. A call costs ten and a put seven, both struck at a hundred, "
            "with the same expiry. The stock is at a hundred and three, and interest rates are zero. Is there an "
            "arbitrage? <bookmark mark='a'/> Own the call and sell the put. At expiry you receive the stock price "
            "minus a hundred, whatever happens: exactly the payoff of a forward. So the two must cost the same; "
            "this is put-call parity, written down by Hans Stoll in 1969. <bookmark mark='b'/> Here both sides "
            "are three: no arbitrage. If the put were six, you would buy it, sell the call, buy the stock and "
            "borrow ninety-nine, and lock in one dollar for nothing."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def bitcoin(self, p):
        ex = p["expiries"]
        T = np.array([e["T"] for e in ex]) * 365
        rate = np.array([e["rate"] for e in ex])
        n = np.array([e["n"] for e in ex])
        g = axes([0, 200], [0, 0.06], x_length=6.4, y_length=3.8, xlabel=r"days to expiry",
                 ylabel=r"forward over spot, as an annual rate", xticks=[0, 50, 100, 150, 200],
                 yticks=[0, 0.02, 0.04, 0.06], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(t, r), radius=0.04 + 0.04 * np.sqrt(k / n.max()), color=FWD)
                        for t, r, k in zip(T, rate, n)])
        side = VGroup(
            MathTex(r"C - P = 1 - \frac{K}{F}", font_size=36, color=CALL),
            wrapped_label(r"Deribit's options are paid in bitcoin; a call and a put at one strike, traded within ten "
                          r"minutes, reveal the forward $F$", 4.4, 20, GREY_A),
            label(rf"{p['n_pairs']} pairs on 10 December 2025", font_size=24, color=FWD),
            wrapped_label(rf"they agree with their expiry's median to {p['trade_p50']:.1f} basis points "
                          rf"(half of them), {p['trade_p90']:.1f} (nine in ten)", 4.4, 20, GREY_A),
            wrapped_label(r"the rate rises from 3\% to almost 5\% a year: crypto's own interest rate, set by "
                          r"leveraged longs paying to borrow (Part 2's funding rate)", 4.4, 20, Q_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Deribit BTC option trades, 10 December 2025, 00:00--12:00 UTC (the Surface)")
        with self.voiceover(
            "Parity is not just an exam question; it is how traders read the market. On Deribit, the largest "
            "Bitcoin options exchange, options are paid in Bitcoin, and parity takes this form. Every call and put "
            "at the same strike, traded within ten minutes of each other, reveals the forward price the market is "
            f"using. <bookmark mark='a'/> On the day of our Surface there were {p['n_pairs']} such pairs. Half of "
            f"them agree with their expiry's median to within {p['trade_p50']:.1f} basis points: parity holds, to "
            "the width of the bid-ask spread. <bookmark mark='b'/> And the forwards say something. Above the spot "
            "price, they imply an interest rate that rises from three percent a year to almost five: Bitcoin's own "
            "rate of interest, paid by leveraged buyers, the funding rate of Part two, read from option prices."
        ) as vo:
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(src))
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(side[2]), FadeIn(side[3]), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(FadeIn(side[4]), Indicate(dots, color=Q_C, scale_factor=1.2))
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Arbitrage, the law of one price, put--call parity, and where it breaks",
            r"The fundamental theorem in one period, proved with a separating hyperplane",
            r"State prices, the stochastic discount factor, and the risk-neutral measure",
            r"The binomial tree; complete and incomplete markets; super-replication as a linear program",
            r"Continuous time: Harrison--Kreps, Harrison--Pliska, Delbaen--Schachermayer; changing numeraire",
            r"The density inside the Surface; Ross recovery and its critique; model-free bounds",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan. Arbitrage and the law of one price, and where parity breaks. The fundamental theorem of "
            "asset pricing, proved in one period with a picture. State prices, the discount factor, and the "
            "risk-neutral measure. The binomial tree, and what happens when a market is incomplete. The theorem in "
            "continuous time. And three things you can read from option prices: the market's probability density, "
            "what Ross's recovery theorem claims, and bounds that need no model at all."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=9))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("data",))
        with self.voiceover(
            "In the House, this part builds the arbitrage checker. <bookmark mark='a'/> From now on, every surface of "
            "prices the House reads passes through it before any model is fitted, and the volatility desk, opening "
            "next part, never trades against a surface that fails it."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
