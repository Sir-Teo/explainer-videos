from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant31.common import BAD, COST_C, GOOD, HURDLE, IC_C, PART, fit_right, load


class Costs(VoiceoverScene):
    def construct(self):
        c = load("costs")
        self.card()
        self.shortfall()
        self.law()
        self.worked(c)
        self.aqr()
        self.anomalies()
        self.capacity(c)
        self.inside()
        self.band()
        self.question()

    def card(self):
        c = chapter_card(4, r"Transaction costs and the square-root law", r"What does it cost to trade a forecast, and "
                         r"how does the cost grow with size?", part=PART)
        with self.voiceover("Chapter four. The fundamental law is gross of costs. Every bet it counts must be placed, and "
                            "placing it moves the price against you."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def shortfall(self):
        parts = [(r"fees and commissions", r"known in advance; a few basis points", GREY_B),
                 (r"half the bid--ask spread", r"paid by whoever demands immediacy", HURDLE),
                 (r"market impact", r"the price moves while, and because, you trade", COST_C),
                 (r"delay and opportunity", r"the trades you did not finish, and the move while you waited", QC.OPTION)]
        rows = VGroup()
        for nm, d, col in parts:
            rows.add(VGroup(label(nm, font_size=24, color=col), label(d, font_size=18, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.2 + LEFT * 0.5)
        head = label(r"Implementation shortfall: paper return minus real return", font_size=30).to_edge(UP, buff=0.5)
        foot = wrapped_label(r"Perold (1988): measure against the price when the decision was made, so that every cost, "
                             r"including the trades not done, is counted", 11.4, 17, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Andre Perold gave the right accounting in 1988: implementation shortfall, the paper portfolio's return minus "
            "the real one, measured from the price when the decision was made. <bookmark mark='a'/> It has four pieces. "
            "Fees, known in advance. Half the bid-ask spread, paid by whoever wants to trade now. <bookmark mark='b'/> "
            "Market impact: the price moves while, and because, you trade. And the opportunity cost of trades not "
            "finished. For a large fund, impact is most of the bill."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[:2]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[2:]], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def law(self):
        rows = [cmath(r"\frac{\Delta P}{P}", r"\approx", r"Y\,\sigma\,\sqrt{\frac{Q}{V}}", font_size=44,
                      colors={r"Y\,\sigma\,\sqrt{\frac{Q}{V}}": COST_C}),
                cmath(r"\text{cost}(Q)", r"\approx", r"Y\,\sigma\,\frac{Q^{3/2}}{V^{1/2}}", font_size=38),
                cmath(r"\text{cost}(2Q)", r"=", r"2^{3/2}\,\text{cost}(Q) \approx 2.8\,\text{cost}(Q)", font_size=36,
                      colors={r"2^{3/2}": BAD})]
        whys = [why(r"the impact of a metaorder of $Q$ shares, against daily volume $V$ and daily volatility $\sigma$: "
                    r"$Y$ is of order one; found across stocks, futures, options and bitcoin (Torre 1997; Almgren et al. "
                    r"2005; T\'oth et al. 2011)"),
                why(r"the cost in money is the quantity times the price move: it grows with the power three halves"),
                why(r"so doubling a fund's size almost triples its costs: the reason every strategy has a capacity")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The most robust regularity in market microstructure. <bookmark mark='a'/> The price impact of a large order, "
            "split into many small trades over a day, is proportional to the daily volatility times the square root of "
            "the order's size as a fraction of daily volume. It was documented at Barra in the nineteen nineties, "
            "measured by Almgren and coauthors in 2005 on stocks, found by Toth and coauthors in 2011 on futures, and since "
            "on options and bitcoin. Part thirty-seven explains why it is a square root. <bookmark mark='b'/> In money, the cost "
            "is the size times the impact, so it grows with the power three halves. <bookmark mark='c'/> Double the "
            "fund, and its costs almost triple. That is why every strategy has a capacity."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def worked(self, c):
        adv, sig = c["median_adv"], c["median_sigma"]
        frac = 1e6 / adv
        rows = [cmath(r"V", r"=", rf"\${adv / 1e6:.1f}\ \text{{million a day}},\quad \sigma = {100 * sig:.1f}\%", font_size=34),
                cmath(r"Q", r"=", rf"\$1\ \text{{million}} = {100 * frac:.0f}\%\ \text{{of a day's volume}}", font_size=34),
                cmath(r"\frac{\Delta P}{P}", r"\approx", rf"{100 * sig:.1f}\% \times \sqrt{{{frac:.2f}}} = {100 * c['cost_1m']:.1f}\%",
                      font_size=36, colors={r"\frac{\Delta P}{P}": COST_C})]
        whys = [why(r"the median eligible coin, 2018--2020: its 20-day average volume in USDT and its daily volatility"),
                why(r"a million-dollar order in that coin, spread over the day"),
                why(r"with $Y = 1$: almost three percent of the price, every time the position is traded")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "In the coins of Part twenty-nine. <bookmark mark='a'/> The median eligible coin traded about "
            f"{adv / 1e6:.1f} million dollars a day, with a daily volatility of {100 * sig:.1f} percent. "
            f"<bookmark mark='b'/> A million-dollar order is {100 * frac:.0f} percent of a day's volume. "
            f"<bookmark mark='c'/> The square-root law prices it at about {100 * c['cost_1m']:.1f} percent, every time. A "
            "signal whose edge is a fraction of a percent a day cannot pay that."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def aqr(self):
        card = firm_card(r"Trading costs, measured from the inside", r"Frazzini, Israel and Moskowitz (2018) studied "
                         r"\$1.7 trillion of one large manager's own executions (their firm's, as reported) across 21 equity markets over 19 years: costs about an "
                         r"order of magnitude smaller than earlier academic estimates, dominated by market impact, which "
                         r"rises less than proportionally with size",
                         numbers=((r"\$1.7\ \text{tn}", r"of the firm's live trades"), (r"21", r"developed equity markets"),
                                  (r"19\ \text{yrs}", r"of executions")),
                         source=r"Frazzini, Israel and Moskowitz, Trading Costs, working paper (2018)", kind=r"Firm file",
                         width=10.6, font_size=22).move_to(UP * 0.2)
        with self.voiceover(
            "How large are costs in practice? Academic studies long had to guess, from public trade data, which trades "
            "belonged to one order. In 2018 Andrea Frazzini, Ronen Israel and Tobias Moskowitz, then at AQR, published the "
            "costs of a large manager's own executions, reported to be their firm's: one point seven trillion dollars of trades in twenty-one markets over "
            "nineteen years. They found costs about an order of magnitude smaller than earlier academic estimates, "
            "dominated by market impact, rising less than proportionally with size, as the square-root law says. "
            "Patient, careful execution changes the answer to whether an anomaly survives."
        ):
            self.play(FadeIn(card))
            self.wait(1.0)
        self.clear_scene()

    def anomalies(self):
        cards = VGroup(
            desk_question(r"Novy-Marx and Velikov (2016)", r"anomalies with low turnover (value, size, profitability) "
                          r"survive realistic costs; the high-turnover ones (short-term reversal, industry momentum, many "
                          r"monthly-rebalanced signals) mostly do not", width=12.4, font_size=19),
            desk_question(r"what helps", r"trade less: rebalance only when the position drifts outside a band, buy and "
                          r"hold within it, and give each trade a cost in the optimisation itself", width=12.4, font_size=19),
            desk_question(r"the consequence", r"the paper anomaly is the gross return; the investable one is what is "
                          r"left after the trades it requires", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Robert Novy-Marx and Mihail Velikov asked which anomalies survive costs. <bookmark mark='a'/> Those that trade "
            "rarely, such as value, size and profitability, survive; the high-turnover ones, such as short-term reversal, "
            "mostly do not. <bookmark mark='b'/> What helps is to trade less: a band around the target, inside which you "
            "do not trade, and a cost charged inside the optimisation rather than subtracted afterwards. "
            "<bookmark mark='c'/> The anomaly on paper is gross; the investable one is what is left."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def capacity(self, c):
        cur = c["curve"]
        xs = np.array([math.log10(r["aum"]) for r in cur])
        ys = np.array([r["sharpe"] for r in cur])
        g = axes([5, 9], [-15, 2], x_length=7.4, y_length=4.4, xlabel=r"assets under management, dollars",
                 ylabel=r"Sharpe ratio after costs", xticks=[5, 6, 7, 8, 9], yticks=[-15, -10, -5, 0],
                 xfmt=lambda v: f"10^{{{int(v)}}}", font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(5, 0), ax.c2p(9, 0), color=GREY_C, stroke_width=1.5)
        gross = DashedLine(ax.c2p(5, c["gross_sharpe"]), ax.c2p(9, c["gross_sharpe"]), color=GOOD, stroke_width=2)
        gl = label(rf"gross {c['gross_sharpe']:.2f}", font_size=16, color=GOOD).next_to(ax.c2p(9, c["gross_sharpe"]), UP,
                                                                                        buff=0.1).shift(LEFT * 0.6)
        line = curve(ax, xs, ys, COST_C, stroke_width=4)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=COST_C) for a, b in zip(xs, ys)])
        txt = wrapped_label(rf"the calm-coin signal (long low-volatility coins, short high), a daily turnover of "
                            rf"{100 * c['turnover']:.0f}\% of the book; square-root impact with $Y = 1$ plus 5 bp of fees; "
                            r"2018--2020", 4.0, 16, GREY_A).to_edge(RIGHT, buff=0.4).shift(UP * 0.8)
        fit_right(txt)
        s5, s6 = ys[0], ys[1]
        with self.voiceover(
            "A capacity curve. The signal is the low-volatility effect from Chapter two: long the calm coins, short the "
            f"wild ones, rebalanced daily, turning over {100 * c['turnover']:.0f} percent of the book a day. "
            f"<bookmark mark='a'/> Before costs, a Sharpe ratio of {c['gross_sharpe']:.2f}. <bookmark mark='b'/> With "
            f"a hundred thousand dollars, {s5:.2f}. With a million, {s6:.2f}. Beyond that the costs exceed the edge many "
            "times over, and the curve falls as the square root of size. A strategy's capacity is where this curve "
            "crosses the return you need, and for daily signals in thin markets it is small."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(txt))
            vo.wait_until("a")
            self.play(Create(gross), FadeIn(gl))
            vo.wait_until("b")
            self.play(Create(line), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.2), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    def inside(self):
        rows = [cmath(r"\max_h", r"\ ", r"h^\top\alpha - \tfrac{\gamma}{2}h^\top\Sigma h - \textstyle\sum_i c_i\,|h_i - h_{i,0}|^{3/2}",
                      font_size=32, colors={r"\textstyle\sum_i c_i\,|h_i - h_{i,0}|^{3/2}": COST_C}),
                cmath(r"h_i", r"=", r"h_{i,0}\ \text{ unless the gain clears the marginal cost}", font_size=30),
                cmath(r"\text{quadratic}", r":", r"\tfrac{\lambda}{2}(h - h_0)^\top\Sigma(h - h_0)", font_size=32,
                      colors={r"\tfrac{\lambda}{2}(h - h_0)^\top\Sigma(h - h_0)": IC_C})]
        whys = [why(r"costs inside the optimisation: a convex problem, the three-halves power from the square-root law"),
                why(r"a no-trade region appears around the current holdings: small improvements are not worth their cost"),
                why(r"the tractable stand-in the next chapter uses: quadratic in the trade, scaled by risk; it gives a "
                    r"closed-form answer")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "So costs belong inside the optimisation. <bookmark mark='a'/> Maximise expected return, less risk, less the "
            "cost of moving from today's holdings, with the three-halves power of the square-root law. It is still a "
            "convex problem. <bookmark mark='b'/> Its solution leaves most positions untouched: around today's "
            "holdings there is a region where no trade is worth its cost. <bookmark mark='c'/> And a quadratic cost, "
            "scaled by risk, is the stand-in that makes the dynamic problem solvable in closed form, which is the next "
            "chapter."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def band(self):
        rows = [cmath(r"|h - h^*|", r"\le", r"\delta\ \Rightarrow\ \text{do not trade}", font_size=36),
                cmath(r"\delta", r"\propto", r"\kappa^{1/3}", font_size=42, colors={r"\kappa^{1/3}": COST_C}),
                cmath(r"\text{loss of utility}", r"\propto", r"\kappa^{2/3}", font_size=36),
                cmath(r"\kappa \to \kappa/8", r":", r"\delta \to \delta/2", font_size=34)]
        whys = [why(r"with a proportional cost $\kappa$ per dollar traded, the optimal policy is a band around the "
                    r"frictionless target: trade only to its edge when the position leaves it"),
                why(r"for small costs the band's half-width grows like the cube root of the cost (Constantinides 1986; "
                    r"Davis and Norman 1990; Shreve and Soner 1994)"),
                why(r"and the cost of the friction, in certainty-equivalent return, like its two-thirds power"),
                why(r"so the band is wide even for tiny costs: cutting costs eightfold only halves it")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "A classical result about the no-trade region. <bookmark mark='a'/> With a cost proportional to the dollars "
            "traded, the optimal policy is a band around the frictionless target: do nothing inside it, and trade only "
            "to its edge when the position drifts out. <bookmark mark='b'/> For small costs, the band's half-width grows "
            "like the cube root of the cost. George Constantinides described the band in 1986, Mark Davis and Andrew "
            "Norman characterised it exactly, and Steven Shreve and Mete Soner derived the cube-root law. <bookmark mark='c'/> The utility lost to the friction "
            "grows like the two-thirds power. <bookmark mark='d'/> So the band is wide even when costs are tiny: cut "
            "costs eightfold and it only halves. Small costs change behaviour a lot and welfare only a little."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a strategy nets 6\% a year at \$100 million, after costs of 2\% a year. Under the square-root "
                       r"law, what does it net at \$400 million?")
        with self.voiceover(
            "Pause and predict. A strategy nets six percent a year at a hundred million dollars, after costs of two "
            "percent. Under the square-root law, what does it net at four hundred million?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
