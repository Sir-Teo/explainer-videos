from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, DELTA, GOOD, NET, PART, illustration, load
from videos.quant.quant17.s09_band import trade_map


class Hook(VoiceoverScene):
    def construct(self):
        h = load("hedge")
        self.title_card()
        self.teaser(h)
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"A machine that hedges")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part seventeen. Deep pricing and hedging. Networks that price, calibrate and hedge, trained on the House's "
            "own engines, and checked against them."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def teaser(self, h):
        m = h["mlp_cost"]
        S, P = np.asarray(m["S"]), np.asarray(m["prev"])
        keys = sorted(m["snaps"], key=int)
        g = axes([S[0], S[-1]], [0, 1], x_length=6.0, y_length=4.4, xlabel=r"price", ylabel=r"shares already held",
                 xticks=[90, 100, 110], yticks=[0, 0.5, 1], font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        first = trade_map(ax, S, P, np.asarray(m["snaps"][keys[0]]))
        last = trade_map(ax, S, P, np.asarray(m["snaps"][keys[-1]]))
        ww = VGroup(DashedVMobject(curve(ax, S, np.clip(np.asarray(m["ww_lo"]), 0, 1), WHITE, stroke_width=2.5), num_dashes=30),
                    DashedVMobject(curve(ax, S, np.clip(np.asarray(m["ww_hi"]), 0, 1), WHITE, stroke_width=2.5), num_dashes=30))
        side = VGroup(
            label(r"a network learns to hedge an option", font_size=24),
            label(r"with trading costs, from simulated paths alone", font_size=24, color=GREY_A),
            legend([(GOOD, r"it buys"), (BAD, r"it sells"), (GREY_D, r"it does nothing"),
                    (WHITE, r"the band theory predicts (1997)")], font_size=18),
            firm_card(r"J.P. Morgan, 2022", r"about 70\% of the bank's Euro Stoxx flow options quoted and hedged by "
                      r"machine, as reported", source=r"Risk.net", width=4.6, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        src = illustration(r"the deep hedger of chapter 8: its trade, 15 days before expiry, before and after training")
        with self.voiceover(
            "This is a neural network deciding how to hedge an option when every trade costs money. It sees the price, "
            "the time left and what it already holds. Before training, its decisions are noise. "
            "<bookmark mark='a'/> After training on simulated markets, a dark corridor appears where it does nothing "
            "at all. <bookmark mark='b'/> That corridor is the no-trade band that theory derived in 1997. Nobody told "
            "the network. <bookmark mark='c'/> Machines like this already hedge real books: by 2022, Risk.net reported, "
            "about seventy percent of J.P. Morgan's Euro Stoxx flow options were quoted and hedged by machine."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(first), FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2][:3]))
            vo.wait_until("a")
            self.play(FadeOut(first), FadeIn(last), run_time=2)
            vo.wait_until("b")
            self.play(Create(ww), FadeIn(side[2][3]))
            vo.wait_until("c")
            self.play(FadeIn(side[3], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Learning a pricing formula from prices (Hutchinson, Lo and Poggio 1994)",
            r"The neural calibrator: rough Bergomi in milliseconds, every week of 2024--2025",
            r"Differential machine learning: payoffs and their derivatives",
            r"High dimensions: the deep BSDE solver and deep optimal stopping",
            r"The deep hedger: costs, risk measures, indifference prices, and the band",
            r"Neural SDEs: how far vanillas leave an exotic's price free",
            r"Market generators, judged by the stylized facts; production and model risk",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan. A network that learns a pricing formula from prices. A network that calibrates rough volatility "
            "in milliseconds, used on two years of surfaces. Training on derivatives as well as prices. Pricing in a "
            "hundred dimensions, and learning when to exercise. The deep hedger, its prices, and the band it "
            "rediscovers. Neural models that measure model risk. Machines that invent markets. And what it takes to "
            "let any of them trade."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=10))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("vol", "research"))
        with self.voiceover(
            "In the House, the volatility desk gets a deep hedger, and research gets a market generator. "
            "<bookmark mark='a'/> The finale will use that generator to stress-test the whole firm."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
