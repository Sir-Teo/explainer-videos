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
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[:2]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[2:]], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def law(self):
        rows = [cmath(r"\text{average cost fraction}", r"\approx", r"Y_{\rm avg}\,\sigma\,\sqrt{\frac{Q}{V}}", font_size=44,
                      colors={r"Y_{\rm avg}\,\sigma\,\sqrt{\frac{Q}{V}}": COST_C}),
                cmath(r"\text{cost}(Q)", r"\approx", r"Y_{\rm avg}\,\sigma\,\frac{Q^{3/2}}{V^{1/2}}", font_size=38),
                cmath(r"\text{cost}(2Q)", r"=", r"2^{3/2}\,\text{cost}(Q) \approx 2.8\,\text{cost}(Q)", font_size=36,
                      colors={r"2^{3/2}": BAD})]
        whys = [why(r"average execution shortfall scenario; $Q,V$ are currency notionals; the coefficient depends on market, execution and benchmark"),
                why(r"$Q,V$ are currency notionals: money cost is $Q$ times average execution shortfall, not terminal peak impact"),
                why(r"holding the execution scenario fixed, doubling $Q$ multiplies modelled money cost by $2^{3/2}$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A common empirical execution model is a square root. <bookmark mark='a'/> Define average execution shortfall as Y average times daily volatility times square root of participation. The coefficient depends on the market, execution and benchmark. <bookmark mark='b'/> If Q and V are currency notionals, multiplying Q by that average fraction gives money cost proportional to Q to the three-halves power. A terminal peak price displacement is different; integrating a particular square-root peak-impact path gives a two-thirds factor. <bookmark mark='c'/> With the scenario held fixed, doubling quantity multiplies this money cost by about two point eight. Extrapolating to very large participation is uncertain."
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
                cmath(r"\text{average cost fraction}", r"\approx", rf"{100 * sig:.1f}\% \times \sqrt{{{frac:.2f}}} = {100 * c['cost_1m']:.1f}\%",
                      font_size=36, colors={r"\text{average cost fraction}": COST_C})]
        whys = [why(r"separate pooled asset-date medians of ADV and daily volatility, 2018--2020; not one observed coin"),
                why(r"a million-USDT trade at those separately pooled median inputs, spread over the day"),
                why(r"chosen average-cost coefficient $Y_{\rm avg}=1$; USD labels assume USDT parity")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            f"""For a numerical scenario, take separate pooled medians of eligible asset-date observations. <bookmark mark='a'/> ADV is {adv / 1e6:.1f} million USDT and daily volatility is {100 * sig:.1f} percent; these medians need not describe one actual coin. <bookmark mark='b'/> A million-USDT trade has participation {frac:.2f}. <bookmark mark='c'/> With a chosen average-cost coefficient of one, the saved model gives {100 * c['cost_1m']:.1f} percent. This is an illustrative execution-cost assumption, not an observed fill. Dollar labels assume USDT parity."""
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
            desk_question(r"Novy-Marx and Velikov (2016)", r"in their sample and cost model, many low-turnover anomalies survive and higher-turnover rules are more vulnerable", width=12.4, font_size=19),
            desk_question(r"what helps", r"trade less: rebalance only when the position drifts outside a band, buy and "
                          r"hold within it, and give each trade a cost in the optimisation itself", width=12.4, font_size=19),
            desk_question(r"the consequence", r"the paper anomaly is the gross return; the investable one is what is "
                          r"left after the trades it requires", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        head = label(r"Which anomalies survive trading costs?", font_size=28).to_edge(UP, buff=0.4)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "Robert Novy-Marx and Mihail Velikov asked which anomalies survive costs. <bookmark mark='a'/> In their samples and cost models, many low-turnover anomalies survived and high-turnover ones were more vulnerable. <bookmark mark='b'/> What helps is to trade less: a band around the target, inside which you "
            "do not trade, and a cost charged inside the optimisation rather than subtracted afterwards. "
            "<bookmark mark='c'/> The anomaly on paper is gross; the investable one is what is left."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(cards[0]))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2)) if k else self.play(Indicate(cards[0]))
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
            f"""The saved capacity scenario holds signal targets and notional book size fixed. <bookmark mark='a'/> Gross annualised Sharpe is {c['gross_sharpe']:.2f}. <bookmark mark='b'/> Chosen square-root average impact and five basis points of fees give {s5:.2f} at a hundred thousand dollars and {s6:.2f} at a million. Target differences omit portfolio drift, and financing, borrow, spread and delay are incomplete. Sharpe need not fall exactly as square root of size because costs also change its variance. This research-period scenario is not an executable future account."""
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(txt))
            vo.wait_until("a")
            self.play(Create(gross), FadeIn(gl))
            vo.wait_until("b")
            self.play(Create(line), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.2), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    def inside(self):
        rows = [cmath(r"\max_h", r"\ ", r"h^\top\alpha - \tfrac{\gamma}{2}h^\top\Sigma h - \textstyle\sum_i [c_i|\Delta h_i|^{3/2}+\kappa_i|\Delta h_i|]",
                      font_size=32, colors={r"\textstyle\sum_i [c_i|\Delta h_i|^{3/2}+\kappa_i|\Delta h_i|]": COST_C}),
                cmath(r"h=h_0", r"\Longleftrightarrow", r"|\alpha_i-\gamma(\Sigma h_0)_i|\le\kappa_i\quad\forall i", font_size=30),
                cmath(r"\text{quadratic}", r":", r"\tfrac{\lambda}{2}(h - h_0)^\top\Sigma(h - h_0)", font_size=32,
                      colors={r"\tfrac{\lambda}{2}(h - h_0)^\top\Sigma(h - h_0)": IC_C})]
        whys = [why(r"costs inside the optimisation: a convex problem, the three-halves power from the square-root law"),
                why(r"for fixed PSD risk, $\gamma>0$, $c_i,\kappa_i\ge0$: proportional costs give this whole-book no-trade condition"),
                why(r"the tractable stand-in the next chapter uses: quadratic in the trade, scaled by risk; it gives a "
                    r"closed-form answer")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Put costs inside the objective. <bookmark mark='a'/> Under fixed positive-semidefinite risk and nonnegative costs, maximise return less risk, smooth three-halves impact, and a separate proportional cost kappa times absolute trade. <bookmark mark='b'/> The whole current book is optimal precisely when every marginal return less marginal risk lies between minus and plus kappa. Pure three-halves impact has derivative zero at zero: without the proportional term it generically reduces trades but creates no exact no-trade band. <bookmark mark='c'/> A quadratic trade cost is another smooth approximation. It makes the next chapter's linear dynamic model tractable; it does not by itself create an inaction band."
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
                why(r"for small proportional costs in the classical interior diffusion model (Constantinides 1986; "
                    r"Davis and Norman 1990; Shreve and Soner 1994)"),
                why(r"and the cost of the friction, in certainty-equivalent return, like its two-thirds power"),
                why(r"so the band is wide even for tiny costs: cutting costs eightfold only halves it")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "A different, classical proportional-cost model yields a band. <bookmark mark='a'/> For a continuous diffusion with an interior frictionless target and nondegenerate local fluctuations, trade toward the band edge when the position exits. <bookmark mark='b'/> In the small-cost limit, with other coefficients fixed, the leading band half-width scales as kappa to the one-third power. <bookmark mark='c'/> The associated certainty-equivalent loss scales as kappa to the two-thirds power. <bookmark mark='d'/> In that asymptotic regime, cutting kappa eightfold halves the leading band width. These are conditional diffusion asymptotics, distinct from the smooth three-halves impact objective."
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
