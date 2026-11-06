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
        self.history(s)
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"A hedge that cannot lose, and does")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            'Part five. Stochastic calculus. We build the constructions and proofs, check them by simulation, and'
            ' start with a hedging puzzle.'
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
            wrapped_label(r"own one share whenever the price is above $K$,", 4.3, 21, DRIFT),
            label(r"none when it is below", font_size=21, color=BM),
            wrapped_label(r"the share position alone omits the cash account", 4.3, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.5)
        rows = s["rows"]
        cells = [label(r"intervals/year", font_size=18), label(r"mean shortfall", font_size=18, color=JUMP)]
        for row in rows:
            cells += [MathTex(f"{row['n']:,}".replace(",", "{,}"), font_size=25),
                      MathTex(f"{row['mean_err']:.2f}", font_size=25, color=JUMP)]
        tab = VGroup(*cells).arrange_in_grid(rows=len(rows) + 1, cols=2, col_alignments="rr", buff=(0.5, 0.12))
        tab.next_to(rule, DOWN, buff=0.35).align_to(rule, LEFT)
        price = MathTex(rf"\text{{the call's price: }} {s['call']:.2f}", font_size=30, color=WHITE).next_to(
            tab, DOWN, buff=0.8).align_to(rule, LEFT)
        with self.voiceover(
            f'You have sold a call struck at a hundred and want to hedge it as cheaply as possible. Here'
            f" is a strategy that looks free. <bookmark mark='a'/> Own one share whenever the stock is "
            f'above the strike, and none when it is below. The share position matches the call’s '
            f'exposure at expiry, but its cash account must also be funded. In an ideal continuous rule '
            f'every switch seems to occur at the strike, so the total hedge looks free. <bookmark '
            f"mark='b'/> Simulate it on four thousand paths. Trade weekly, daily, four thousand times a "
            f"year: its average shortfall is about {s['call']:.0f}"
            f' dollars at every sampling frequency. Individual paths differ; trading more often does not'
            f" remove the average shortfall. <bookmark mark='c'/> {s['call']:.0f}"
            f' dollars is the price of the call itself. Where does the money go? The answer is a '
            f'quantity ordinary calculus has no name for, and it is the subject of this part.'
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

    def history(self, s):
        strip = timeline(lit=(1900, 1923, 1944, 1973, 1981, 2018, 2020), font_size=15).shift(UP * 1.6)
        cards = VGroup(
            history_card(1960, r"Girsanov", r"drift is a change of measure", color=QC.IDEA, width=3.1, font_size=18),
            history_card(1990, r"Carr and Jarrow", r"the stop-loss paradox, solved by local time", color=QC.IDEA,
                         width=3.1, font_size=18),
            history_card(1998, r"Lyons", r"rough paths: integration beyond It\^o", color=QC.IDEA, width=3.1,
                         font_size=18),
            history_card(2020, r"negative oil", (
                                                    'CME switches energy-option margin valuation to Bachelier'
                                                ), color=QC.CRISIS, width=3.1,
                         font_size=18),
        ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.45)
        pc, ans = pause(r"Rebalance 4{,}000 times a year instead of 13. Does the loss shrink?",
                        f"No: mean shortfall about {s['call']:.0f} dollars at every frequency. The loss is not a discretisation error.", width=6.0)
        pc.to_corner(UL, buff=0.4)
        ans.next_to(pc, DOWN, buff=0.25).align_to(pc, LEFT)
        with self.voiceover(
            'How we got here. Bachelier modelled markets with Brownian motion in 1900; Wiener constructed its '
            "path measure in 1923; Itô its integral in 1944. <bookmark mark='a'/> Girsanov changed finite-horizon"
            ' drift by reweighting paths. Option pricing followed in 1973; Carr and Jarrow resolved this hedge in'
            " 1990, and Lyons developed rough paths in 1998. <bookmark mark='b'/> In April 2020, negative oil "
            "prices made CME switch its energy-option margin model to Bachelier. <bookmark mark='c'/> From "
            'thirteen to four thousand rebalancing intervals a year: does the average shortfall shrink? <bookmark'
            " mark='d'/> No. The next chapters explain why."
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
            r"It\^o's lemma proved, in 3D; SDEs: existence by Picard iteration, Euler and Milstein with their orders",
            (
                'OU solved; CIR transition pseudo-likelihood on monthly means; density and pricing PDEs'
            ),
            r"Girsanov: paths re-weighted, not moved; importance sampling; why volatility is observable",
            r"Martingale representation and Clark--Ocone: why a hedge exists, and when it does not",
            r"Local time and Tanaka: the stop-loss paradox resolved",
            r"Jumps: Poisson, L\'evy--It\^o, the jump hedge; Hawkes processes fitted and tested on Bitcoin",
            r"Fractional Brownian motion, roughness and its caveat; rough paths and signatures",
            r"Industry: negative oil and Bachelier, clearing-house Monte Carlo, model validation; frontier: neural SDEs",
        ], color=QC.IDEA, font_size=23)
        with self.voiceover(
            'The plan: Brownian motion and its calculus. Stochastic equations and their PDEs. Measure changes, '
            'representation and local time. Jumps and clustering. Roughness, signatures and their practical '
            'limits. Then industry models, a neural-SDE experiment and realized variance’s central limit theorem.'
        ):
            self.play(FadeIn(card.head), FadeIn(VGroup(*card.rows[:3])), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows[3:]],
                                 lag_ratio=0.5, run_time=8))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("data",))
        with self.voiceover(
            'In the House, this part builds the simulation library every pricing desk will use, each routine '
            "tested against theory. <bookmark mark='a'/> It sits with the data desk until the volatility desk "
            'opens in Part ten.'
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
