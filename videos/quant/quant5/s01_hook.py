from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import sim
from videos.quant.quant5.common import BM, DRIFT, JUMP, PART, load, pause

K = 100.0


class Hook(VoiceoverScene):
    def construct(self):
        s = load("stoploss")
        self.title_card()
        self.paradox(s)
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"A hedge that cannot lose, and does")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part five. Stochastic calculus. The series' gentle introduction to this subject built Brownian motion, "
            "Itô's lemma and Black and Scholes. This part assumes it, and goes further: the constructions, the proofs, "
            "and the tools a working quant uses, each one checked by simulation. It begins with a puzzle."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def paradox(self, s):
        _, W = sim.brownian(1.0, 1000, 1, seed=70)
        t = np.linspace(0, 1, 1001)
        S = K * np.exp(-0.02 * t + 0.2 * W[0])
        g = axes([0, 1], [80, 125], x_length=7.6, y_length=4.4, xlabel=r"time (years)", ylabel=r"stock price",
                 xticks=[0, 0.5, 1], yticks=[80, 100, 120], font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        strike = DashedLine(ax.c2p(0, K), ax.c2p(1, K), color=GREY_B, stroke_width=2)
        kl = MathTex(r"K = 100", font_size=24, color=GREY_B).next_to(ax.c2p(1, K), RIGHT, buff=0.1)
        above = S > K
        segs = VGroup()
        for i in range(1000):
            col = DRIFT if above[i] else BM
            segs.add(Line(ax.c2p(t[i], S[i]), ax.c2p(t[i + 1], S[i + 1]), stroke_width=3, color=col))
        rule = VGroup(
            label(r"own one share whenever the price is above $K$,", font_size=22, color=DRIFT),
            label(r"none when it is below", font_size=22, color=BM),
            label(r"at expiry you hold exactly what a call pays", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.5)
        rows = s["rows"]
        tab = VGroup(*[MathTex(rf"\text{{{r['n']:,} trades a year: loses }} {r['mean_err']:.2f}".replace(",", "{,}"),
                               font_size=28, color=JUMP) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        tab.next_to(rule, DOWN, buff=0.5).align_to(rule, LEFT)
        price = MathTex(rf"\text{{the call's price: }} {s['call']:.2f}", font_size=30, color=WHITE).next_to(
            tab, DOWN, buff=0.35).align_to(rule, LEFT)
        with self.voiceover(
            "You have sold a call option struck at a hundred, and you want to hedge it as cheaply as possible. "
            "Here is a strategy that looks free. <bookmark mark='a'/> Whenever the stock is above the strike, own "
            "one share. Whenever it falls below, sell it. At expiry, if the stock is above the strike you hold a "
            "share, and if not you hold nothing: exactly what the call pays. You only ever buy or sell at the "
            "strike, so it seems to cost nothing. <bookmark mark='b'/> Simulate it on four thousand paths. Trade "
            "weekly, daily, four thousand times a year: the strategy loses about eight dollars every time, and "
            "trading more often does not help at all. <bookmark mark='c'/> Eight dollars is the price of the call "
            "itself. The free hedge loses exactly what the option is worth. Where does the money go? The answer is "
            "a quantity ordinary calculus has no name for, and it is the subject of this part."
        ) as vo:
            self.play(FadeIn(g), Create(strike), FadeIn(kl))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(sg) for sg in segs], lag_ratio=0.004, run_time=4), FadeIn(rule))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(price))
        self.wait(0.4)
        self.clear_scene()

    def history(self):
        strip = timeline(lit=(1900, 1923, 1944, 1973, 1981, 2018, 2020), font_size=15).shift(UP * 1.6)
        cards = VGroup(
            history_card(1960, r"Girsanov", r"drift is a change of measure", color=QC.IDEA, width=3.1, font_size=18),
            history_card(1990, r"Carr and Jarrow", r"the stop-loss paradox, solved by local time", color=QC.IDEA,
                         width=3.1, font_size=18),
            history_card(1998, r"Lyons", r"rough paths: integration beyond It\^o", color=QC.IDEA, width=3.1,
                         font_size=18),
            history_card(2020, r"negative oil", r"CME switches energy options to Bachelier", color=QC.CRISIS, width=3.1,
                         font_size=18),
        ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.45)
        pc, ans = pause(r"Rebalance 4{,}000 times a year instead of 13. Does the loss shrink?",
                        r"No: about 8 dollars at every frequency. The loss is not a discretisation error.", width=6.0)
        pc.to_corner(UL, buff=0.4)
        ans.next_to(pc, DOWN, buff=0.25).align_to(pc, LEFT)
        with self.voiceover(
            "How we got here. In 1900 Louis Bachelier, five years before Einstein, modelled the Paris bond market with "
            "what we now call Brownian motion. Norbert Wiener built it as a measure on paths in 1923, and Kiyosi Itô "
            "learned to integrate against it in 1944. <bookmark mark='a'/> Igor Girsanov showed in 1960 that a drift is "
            "only a change of measure. Black, Scholes and Merton priced options with this calculus in 1973, and "
            "Harrison and Pliska made martingales the language of pricing in 1981. Carr and Jarrow explained this "
            "part's opening puzzle in 1990, and Terry Lyons pushed integration beyond Itô in 1998. In 2018 volatility "
            "turned out to be rough. <bookmark mark='b'/> And in April 2020 an oil contract settled below zero, and "
            "the exchange had to switch its option model back to Bachelier's. <bookmark mark='c'/> One question to "
            "keep in mind: if you rebalance four thousand times a year instead of thirteen, does the loss shrink? "
            "<bookmark mark='d'/> It does not. The table already said so."
        ) as vo:
            self.play(FadeIn(strip), run_time=2)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards[:3]], lag_ratio=0.5, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(cards[3], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeOut(strip), FadeIn(pc))
            vo.wait_until("d")
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Brownian motion built two ways; reflection; quadratic variation, proved and measured on Bitcoin",
            r"The It\^o integral constructed; the isometry; Stratonovich and Wong--Zakai",
            r"It\^o's lemma proved, in 3D; SDEs: Picard, Euler and Milstein, multilevel Monte Carlo",
            r"Ornstein--Uhlenbeck and CIR fitted by exact likelihood; Fokker--Planck and Feynman--Kac proved",
            r"Girsanov: paths re-weighted, not moved; importance sampling; why volatility is observable",
            r"Martingale representation and Clark--Ocone: why a hedge exists, and when it does not",
            r"Local time and Tanaka: the stop-loss paradox resolved",
            r"Jumps: Poisson, L\'evy--It\^o, the jump hedge; Hawkes processes fitted and tested on Bitcoin",
            r"Fractional Brownian motion, roughness and its caveat; rough paths and signatures",
            r"Industry: negative oil, clearing-house Monte Carlo, adjoints; frontier: neural SDEs",
        ], color=QC.IDEA, font_size=23)
        with self.voiceover(
            "The plan, in eighteen chapters. Brownian motion built two ways, and its quadratic variation proved and "
            "measured. The Itô integral constructed, and Stratonovich's alternative. Itô's lemma proved, and "
            "stochastic differential equations solved and simulated. Mean reversion fitted by exact likelihood, and "
            "the partial differential equations behind it. Girsanov's theorem, and martingale representation, which "
            "says why a hedge exists. Local time, which resolves the puzzle. Jumps, and jumps that cause jumps. "
            "Roughness, rough paths and signatures. Then how desks and clearing houses run all this, and a neural "
            "stochastic differential equation trained on Bitcoin."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=14))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("data",))
        with self.voiceover(
            "In the House, this part builds the simulation library that every pricing desk will use: Brownian "
            "constructions, exact and approximate schemes, jumps, self-exciting processes, rough paths and signatures, "
            "each one tested against theory before anyone prices with it. <bookmark mark='a'/> It sits with the data desk until the volatility desk opens in Part ten."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
