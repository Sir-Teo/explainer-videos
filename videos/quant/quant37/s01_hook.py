from __future__ import annotations

import math


from explainer.quant import *  # noqa: F403
from videos.quant.quant37.common import (GOOD, HURDLE, PART, era_strip, load)


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.question()
        self.claims(load("aggregate"), load("latent"), load("rl"), load("ac"))
        self.stakes()
        self.act()
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Market Impact and Execution")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part thirty-seven. Market impact and execution: how much a large order moves the price against the trader "
            "who sends it, and how to send it so that it costs the least."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def question(self):
        a = math.sqrt(0.40 / 0.10) * 30
        rows = VGroup(label(r"buying 10\% of a day's volume costs 30 bp", font_size=26),
                      label(r"what does 40\% cost?", font_size=26, color=HURDLE),
                      label(r"linear: 120 bp", font_size=24, color=GREY_B),
                      label(rf"the square-root law: $30 \times \sqrt{{4}} = {a:.0f}$ bp", font_size=24, color=GOOD))
        rows.arrange(DOWN, buff=0.35).move_to(UP * 0.3)
        with self.voiceover(
            "A question asked of execution traders. <bookmark mark='a'/> Buying a tenth of a day's volume in a stock "
            "costs thirty basis points of impact. What does buying four tenths cost? <bookmark mark='b'/> A straight "
            "line says a hundred and twenty. <bookmark mark='c'/> Almost every large data set of real orders says "
            f"{a:.0f}: impact grows like the square root of the size. Why it does, and what that implies for how to "
            "trade, is this part."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.wait(0.4)
        self.clear_scene()

    def claims(self, ag, lt, rl, ac):
        r = rl["res"]
        cards = VGroup(
            desk_question(r"impact is concave, on Bitcoin and in a model", rf"a minute's price move grows like signed "
                          rf"volume to the power {ag['slope']:.2f}; in the latent order book the exponent falls from "
                          rf"{lt['slope_small']:.1f} to {lt['slope_large']:.2f} as orders grow", width=12.4, font_size=19),
            desk_question(r"the schedule is a theorem", r"Almgren and Chriss for risk; Obizhaeva and Wang for a book that "
                          r"recovers: blocks at the ends and a steady rate between, proved in the research chapter",
                          width=12.4, font_size=19),
            desk_question(r"learning, honestly measured", rf"a Q-learning executor in the House's simulator costs "
                          rf"{r['Q-learning']['mean']:.1f} half-ticks against TWAP's {r['TWAP']['mean']:.1f}",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What this part finds. <bookmark mark='a'/> Impact is concave: on Bitcoin, a minute's price move grows like "
            f"the signed volume to the power {ag['slope']:.2f}, and in a model of latent liquidity the exponent falls "
            f"from one to about {lt['slope_large']:.2f} as orders grow. <bookmark mark='b'/> The best schedule is a "
            "theorem: Almgren and Chriss's for a trader who fears risk, and Obizhaeva and Wang's for a book that "
            "recovers, proved here. <bookmark mark='c'/> And a learned executor, honestly measured, did not beat the "
            f"plainest schedule: {r['Q-learning']['mean']:.1f} half-ticks against TWAP's {r['TWAP']['mean']:.1f}."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def stakes(self):
        cards = VGroup(
            desk_question(r"capacity", r"a strategy's capacity is where its impact eats its alpha; Part 31's square root "
                          r"set the House's sizes", width=12.4, font_size=19),
            desk_question(r"the largest cost", r"for a fund that trades large, impact dwarfs fees and spreads: the "
                          r"difference between a good and a poor execution can be several basis points on every "
                          r"rebalance", width=12.4, font_size=19),
            desk_question(r"a whole industry", r"brokers' algorithms, transaction-cost analysis and the routing of "
                          r"orders between venues exist because of this one curve", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why it matters. <bookmark mark='a'/> A strategy's capacity is the size at which its impact eats its alpha: "
            "Part thirty-one's square root already set the House's sizes. <bookmark mark='b'/> For a fund that trades "
            "large, impact is the largest cost it pays, far above fees and spreads. <bookmark mark='c'/> And a whole "
            "industry, brokers' algorithms, transaction-cost analysis and order routing, exists because of one curve."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def act(self):
        smap = series_map(current=PART, done=PART - 1)
        with self.voiceover(
            "Where this sits. Part thirty-five asked who trades with whom; Part thirty-six opened the order book. This "
            "part sends a large order through it, and Part thirty-eight sits on the other side, as the market maker who "
            "absorbs it."
        ):
            self.play(FadeIn(smap))
            self.wait(1.0)
        self.clear_scene()

    def history(self):
        I = QC.IDEA
        entries = [(1972, r"block trades", I), (1988, r"implementation shortfall", I), (1998, r"Bertsimas--Lo", I),
                   (2000, r"Almgren--Chriss", I), (2004, r"the propagator", I), (2010, r"no dynamic arbitrage", I),
                   (2011, r"the square-root law", I), (2013, r"Obizhaeva--Wang", I), (2015, r"latent liquidity", I),
                   (2016, r"invariance", I), (2021, r"deep RL execution", I)]
        strip = era_strip(entries, y0=1970, y1=2027, font_size=12, step=10).move_to(DOWN * 0.3)
        head = label(r"Fifty years of market impact", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 4), (4, 8), (8, 11)]
        with self.voiceover(
            "Fifty years of the subject. Alan Kraus and Hans Stoll measured the impact of block trades in 1972; André "
            "Perold defined implementation shortfall; Dimitris Bertsimas and Andrew Lo, then Robert Almgren and Neil "
            "Chriss, posed execution as optimal control. <bookmark mark='a'/> Then the propagator, Jim Gatheral's "
            "no-dynamic-arbitrage conditions, the square-root law measured across markets, and Obizhaeva and Wang's "
            "resilient book. <bookmark mark='b'/> And latent liquidity, microstructure invariance, and reinforcement "
            "learning."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), mk in zip(groups, [None, "a", "b"]):
                if mk:
                    vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.6)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Metaorders, implementation shortfall, and what public data shows",
            r"The square-root law, and latent liquidity that explains it",
            r"The propagator: impact that decays, and the efficiency puzzle",
            r"No dynamic arbitrage: which impact models are allowed",
            r"Almgren--Chriss and Obizhaeva--Wang schedules",
            r"A learned executor in the House's simulator; the algorithms and TCA",
            r"For the researcher: the optimal schedule under transient impact, proved",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: metaorders and what public data shows; the square-root law and latent liquidity; the "
            "propagator; which impact models are allowed; Almgren and Chriss, then Obizhaeva and Wang; a learned "
            "executor, the algorithms brokers sell, and transaction-cost analysis; and the optimal schedule under "
            "transient impact, proved."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("execution", "research"))
        with self.voiceover(
            "In the House, the execution desk opens: it receives every order the portfolio desks send, schedules it, "
            "and reports what it cost."
        ):
            self.play(FadeIn(chart))
        self.wait(0.3)
        self.clear_scene()
