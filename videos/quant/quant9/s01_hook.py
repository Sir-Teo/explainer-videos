from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import ARB, CALL, FWD, PART, PUT, Q_C, answer_under, load, pause_at, real_data


class Hook(VoiceoverScene):
    def construct(self):
        p = load("parity")
        self.title_card()
        self.question()
        self.bitcoin(p)
        self.era()
        self.objectives()
        self.house()
        self.predict()

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

    def era(self):
        x0, x1 = -6.4, 6.4

        def X(y):
            return x0 + (x1 - x0) * (y - 1900) / 130

        line = Line([x0, 0, 0], [x1, 0, 0], color=GREY_D, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(y), -0.06, 0], [X(y), 0.06, 0], color=GREY_D),
                                Text(str(y), font_size=13, color=GREY_D).next_to([X(y), 0, 0], DOWN, buff=0.12))
                         for y in range(1900, 2031, 20)])
        events = [
            (1902, r"Farkas: inequalities", Q_C), (1964, r"Arrow: state securities", Q_C),
            (1969, r"Stoll: put--call parity", Q_C), (1973, r"Black--Scholes--Merton", Q_C),
            (1976, r"Ross: options complete markets", Q_C), (1979, r"Cox--Ross--Rubinstein; Harrison--Kreps", Q_C),
            (1981, r"Harrison--Pliska", Q_C), (1994, r"Delbaen--Schachermayer", Q_C),
            (1998, r"Hobson's robust bounds; LTCM", ARB), (2013, r"martingale optimal transport", Q_C),
            (2015, r"Ross recovery", Q_C), (2021, r"GameStop", ARB),
        ]
        dots, labs, leads = VGroup(), VGroup(), VGroup()
        for i, (y, t, c) in enumerate(events):
            d = Dot([X(y), 0, 0], radius=0.07, color=c)
            lvl = [1.0, 2.0, 3.0][i % 3] * (1 if i % 2 == 0 else -1)
            lab = VGroup(MathTex(str(y), font_size=19, color=c), label(t, font_size=17, color=c)).arrange(RIGHT, buff=0.1)
            lab.move_to([X(y), 0.55 * lvl, 0])
            keep_in_frame(lab, margin=0.2)
            dots.add(d)
            labs.add(lab)
            leads.add(Line(d.get_center(), lab.get_bottom() if lvl > 0 else lab.get_top(), color=GREY_C,
                           stroke_width=1, stroke_opacity=0.5))
        head = label(r"How we got here", font_size=34).to_edge(UP, buff=0.35)
        strip = VGroup(line, ticks, dots, leads, labs).shift(DOWN * 0.1)
        with self.voiceover(
            "How we got here. The mathematics is older than the markets: in 1902 Gyula Farkas proved a lemma about "
            "linear inequalities that turns out to be the whole theorem in one period. <bookmark mark='a'/> Kenneth "
            "Arrow priced securities that pay in one state of the world in 1964, Hans Stoll wrote down put-call "
            "parity in 1969, and after Black, Scholes and Merton, Stephen Ross showed in 1976 that options complete "
            "a market. <bookmark mark='b'/> Then the theory: Cox, Ross and Rubinstein's tree and Harrison and Kreps "
            "in 1979, Harrison and Pliska in 1981, Delbaen and Schachermayer's general theorem in 1994. "
            "<bookmark mark='c'/> And then the frontier and the failures: Hobson's model-free bounds and the fall of "
            "Long-Term Capital Management in 1998, martingale optimal transport in 2013, Ross's recovery theorem in "
            "2015, and GameStop in 2021, when borrowing a share became the most expensive part of a trade."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(ticks))
            self.play(GrowFromCenter(dots[0]), FadeIn(labs[0]), Create(leads[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromCenter(dots[i]), FadeIn(labs[i]), Create(leads[i]))
                                    for i in (1, 2, 3, 4)], lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromCenter(dots[i]), FadeIn(labs[i]), Create(leads[i]))
                                    for i in (5, 6, 7)], lag_ratio=0.5), run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromCenter(dots[i]), FadeIn(labs[i]), Create(leads[i]))
                                    for i in (8, 9, 10, 11)], lag_ratio=0.5), run_time=3)
        self.wait(0.4)
        self.clear_scene()

    def predict(self):
        card = pause_at(r"Before chapter one: to spot the arbitrage in the desk question, is $C - P = S - K$ "
                        r"enough, or do you need to know what the stock will do?")
        with self.voiceover(
            "Before chapter one, a question to hold on to. To decide whether the call and put in the desk question "
            "were mispriced, did you need any forecast of the stock? <bookmark mark='a'/> No. Parity needed no "
            "probabilities at all, only prices today. That is the whole spirit of this part: what can be said about "
            "prices with no model of the future."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, r"no forecast needed: parity uses only today's prices; that is what "
                                                r"no-arbitrage arguments are")))
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Parity proved by replication, checked against Bitcoin futures, and where it breaks",
            r"The fundamental theorem in one period: seen in 3D, proved, and decided by a simplex",
            r"State prices, the discount factor and $Q$; Bitcoin's pricing kernel",
            r"The binomial tree: replication, the hedge, convergence to Black--Scholes",
            r"Incomplete markets: super-replication as a linear program and its dual",
            r"Continuous time: Girsanov as reweighting; free lunches, doubling and bubbles",
            r"Changing numeraire: $N(d_1)$ as a probability, Margrabe, Bitcoin as the unit",
            r"Breeden--Litzenberger: butterflies become the density, on the whole Surface",
            r"Ross recovery and its critique; model-free bounds by martingale optimal transport",
            r"Industry and frontier: ETFs, box spreads, LTCM; neural and Sinkhorn transport",
        ], color=QC.IDEA, font_size=23)
        with self.voiceover(
            "The plan. Parity, proved by building it, and checked against Bitcoin futures; then where it breaks. The "
            "fundamental theorem of asset pricing, seen in three dimensions, proved, and decided by a linear program "
            "you will watch pivot. State prices, the discount factor and the risk-neutral measure, with Bitcoin's own "
            "pricing kernel. The binomial tree, its hedge, and its limit. Incomplete markets, where no arbitrage "
            "gives an interval. Continuous time, measure change as reweighting paths, and the free lunches the "
            "theorem has to rule out. Changing the unit of account. The density inside option prices. Ross's "
            "recovery theorem, and bounds with no model at all. And how the industry trades all of this, and where "
            "the research is now."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=14))
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
