from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import (ACT_C, BAD, COST_C, GOOD, HURDLE, LUCK_C, MKT_C, PART, REC_C, SKILL_C, comma,
                                         load)


class Journey(VoiceoverScene):
    def construct(self):
        self.card()
        self.act1()
        self.act2()
        self.act3()
        self.act4()
        self.act5()
        self.act6()
        self.act7()
        self.counts(load("record"))
        self.question()

    def card(self):
        c = chapter_card(9, r"The House's journey", r"What did each act build, and what did it prove?", part=PART)
        with self.voiceover(
            "Chapter nine, and the answer to the pause, act by act. Each act built desks for the House and proved at "
            "least one theorem per part, then checked it by simulation or data. This is the list, briefly, as a map of "
            "what the House now knows."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def _act(self, title, built, proved):
        return VGroup(
            label(title, font_size=26, color=QC.IDEA),
            desk_question(r"built", built, width=12.4, font_size=19),
            desk_question(r"proved", proved, width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.3)

    def act1(self):
        g = self._act(r"Act I, foundations: Parts 1 to 8",
                      r"the fair game and point-in-time data; accounting and the firm; martingales and measure; "
                      r"stochastic calculus; econometrics; volatility; decisions and control",
                      r"the variance ratio's law; Kupiec's test by Wilks; Ohlson's valuation; the law of the iterated "
                      r"logarithm; the error in realised variance; predictive regressions near a unit root; Clark and "
                      r"West; estimation risk in Merton's rule")
        with self.voiceover(
            "Act one, foundations. <bookmark mark='a'/> It built the fair game and the discipline of point-in-time "
            "data, accounting, martingales, stochastic calculus, econometrics, volatility and control. "
            "<bookmark mark='b'/> And it proved, among others, the law of the variance ratio, the test behind Part "
            "two's margins, how far a fair walk can wander, the error in realised variance, and how much estimation "
            "costs a Merton investor. Its lesson for the House: nothing is known before it was known, and a prediction is "
            "worthless until it is tested."
        ) as vo:
            self.play(FadeIn(g[0]))
            vo.wait_until("a")
            self.play(FadeIn(g[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(g[2], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def act2(self):
        g = self._act(r"Act II, derivatives: Parts 9 to 17",
                      r"the arbitrage checker, Black--Scholes and the options desk, the Surface and its models, from "
                      r"Heston to rough Bergomi; exotics; a pricing engine; deep hedging",
                      r"arbitrage with frictions; when to rebalance a hedge; demand-based option prices; the density "
                      r"from noisy prices; moment explosions; how fast rough simulation converges; model-free one-touch "
                      r"bounds; the regression basis in least squares; error bounds for deep solvers")
        with self.voiceover(
            "Act two, derivatives. <bookmark mark='a'/> The arbitrage checker, Black and Scholes and an options desk, "
            "the Surface and every model fitted to it, exotics, a pricing engine and deep hedging. "
            "<bookmark mark='b'/> And theorems on arbitrage with frictions, the optimal band for rebalancing a hedge, "
            "option prices driven by demand, moment explosions in the wings, the convergence of rough simulation, and "
            "error bounds for deep solvers. Its lesson: a price is only as good as its hedge, and every model's "
            "error must be measured on the same scoreboard."
        ) as vo:
            self.play(FadeIn(g[0]))
            vo.wait_until("a")
            self.play(FadeIn(g[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(g[2], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def act3(self):
        g = self._act(r"Act III, rates, credit and macro: Parts 18 to 22",
                      r"the curve builder and the rates desk; term-structure models; the credit desk; XVA and clearing; "
                      r"FX, commodities and the basis",
                      r"why the curve's factors look like level, slope and curvature; shadow rates at the lower bound; "
                      r"the granularity adjustment; wrong-way risk bounds by optimal transport; the theory of storage")
        with self.voiceover(
            "Act three, rates, credit and macro. <bookmark mark='a'/> A curve builder and a rates desk, term-structure "
            "models, a credit desk, XVA and clearing, and FX and commodities. <bookmark mark='b'/> And theorems on why "
            "the curve's factors look like level, slope and curvature, shadow rates at the lower bound, concentration "
            "in a credit book, bounds on wrong-way risk, and the economics of storage. Its lesson: the safest assets have the most "
            "structure, and the credit desk's worst losses come from what its counterparties do together."
        ) as vo:
            self.play(FadeIn(g[0]))
            vo.wait_until("a")
            self.play(FadeIn(g[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(g[2], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def act4(self):
        g = self._act(r"Act IV, asset pricing: Parts 23 to 25",
                      r"risk and return; the factor library and the first rows of the Track Record; the factor zoo and "
                      r"its shrinkage SDF",
                      r"bubbles from disagreement (Harrison and Kreps); where momentum profits come from; how many "
                      r"anomalies are real, with Benjamini and Hochberg proved")
        with self.voiceover(
            "Act four, asset pricing. <bookmark mark='a'/> Risk and return, the factor library, where the Track Record "
            "opened its first rows, and the factor zoo. <bookmark mark='b'/> And theorems on bubbles from "
            "disagreement, the decomposition of momentum's profits, and how many published anomalies are real. "
            "Its lesson: most of what predicts returns is compensation for risk, and most of the rest is luck."
        ) as vo:
            self.play(FadeIn(g[0]))
            vo.wait_until("a")
            self.play(FadeIn(g[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(g[2], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def act5(self):
        g = self._act(r"Act V, the craft: Parts 26 to 34",
                      r"the backtest protocol and the trial counter; machine learning; text and language models; an "
                      r"alpha factory; portfolio construction; a risk model and a trader; macro books; stat arb; the firm",
                      r"inference on the winner; ridgeless regression's risk; how many documents a text signal needs; "
                      r"estimation risk in mined alphas; minimum variance; the trade-rate formula; the trend identity; "
                      r"the small-cost band law; when a drawdown stop fires")
        with self.voiceover(
            "Act five, the quant's craft. <bookmark mark='a'/> The backtest protocol and the trial counter, machine "
            "learning, text and language models, an alpha factory, portfolios, a risk model and a trader, macro "
            "books, statistical arbitrage, and the firm itself. <bookmark mark='b'/> And theorems on inference for "
            "the winner of many backtests, the risk of interpolating models, how much text a signal needs, mined "
            "alphas, the optimal trading rate, trend's identity, the band law for costs, and drawdown stops. "
            "Its lesson: count every trial, and charge every trade."
        ) as vo:
            self.play(FadeIn(g[0]))
            vo.wait_until("a")
            self.play(FadeIn(g[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(g[2], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def act6(self):
        g = self._act(r"Act VI, the market's machinery: Parts 35 to 39",
                      r"who trades with whom; the order book; execution; market making, ETFs and the speed race; crypto "
                      r"and DeFi",
                      r"Kyle's continuous auction; the microprice theorem; the optimal schedule under transient impact; "
                      r"the sniping equilibrium; loss-versus-rebalancing for liquidity providers")
        with self.voiceover(
            "Act six, the market's machinery. <bookmark mark='a'/> Who trades with whom, the order book, execution, "
            "market making and the speed race, and crypto and decentralised finance. <bookmark mark='b'/> And theorems "
            "on Kyle's continuous auction, the microprice, the optimal schedule under transient impact, the sniping "
            "equilibrium, and what liquidity providers lose to arbitrage. Its lesson: "
            "every trade has someone on the other side, who usually knows something."
        ) as vo:
            self.play(FadeIn(g[0]))
            vo.wait_until("a")
            self.play(FadeIn(g[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(g[2], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def act7(self):
        g = self._act(r"Act VII, the system: Parts 40 to 43",
                      r"the risk function; liquidity stress and crisis files; agents, simulators and the collusion "
                      r"audit; the finale's record",
                      r"what can be backtested (elicitability); the clearing vector; herding's law and when collusion "
                      r"lasts; Storey's estimator and Berk and Green's no-persistence theorem")
        with self.voiceover(
            "And Act seven, the system. <bookmark mark='a'/> A risk function, liquidity stress and the crisis files, "
            "agents, simulators and the collusion audit, and this part's record. <bookmark mark='b'/> With theorems on "
            "what can be backtested, the clearing vector, herding and collusion, and, in this part's research "
            "chapter, how to count skill and where it goes. Its lesson: the system "
            "is more fragile than any of its parts, and the market is the default."
        ) as vo:
            self.play(FadeIn(g[0]))
            vo.wait_until("a")
            self.play(FadeIn(g[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(g[2], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def counts(self, r):
        rows = VGroup(
            label(r"43 parts, 7 acts, a research chapter in each part from Part 1", font_size=24, color=QC.IDEA),
            label(rf"{r['n_registered']} strategies and forecasts registered; {r['n_rows']} Track Record rows", font_size=24,
                  color=REC_C),
            label(rf"{comma(r['trials'])} configurations on the trial counter", font_size=24, color=HURDLE),
            label(r"one sealed hold-out, 2021--2025, opened once for each row", font_size=24, color=SKILL_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(UP * 0.2)
        nr, nt, tr = r["n_registered"], r["n_rows"], r["trials"]
        with self.voiceover(
            "And the count. <bookmark mark='a'/> Forty-three parts in seven acts, each with a research chapter. "
            f"<bookmark mark='b'/> {nr} strategies and forecasts registered, {nt} of them rows of the Track Record. "
            f"<bookmark mark='c'/> {tr:,.0f} configurations counted. <bookmark mark='d'/> And one sealed hold-out, "
            "opened once for each row, and never again."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"forty-two rules later, what should the House's last rule be?")
        with self.voiceover(
            "Pause and predict. Forty-two rules later, what should the House's last rule be?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
