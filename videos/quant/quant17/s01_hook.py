from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, DELTA, GOOD, NET, PART, illustration, load


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
        sf = h["band"]["surface"]
        S = np.asarray(sf["S"])
        tau = np.asarray(sf["tau"])
        k = int(np.argmin(np.abs(tau - 0.5)))
        lo, hi = np.asarray(sf["lo"])[k], np.asarray(sf["hi"])[k]
        wl, wh = np.asarray(sf["ww_lo"])[k], np.asarray(sf["ww_hi"])[k]
        dl = (lo + hi) / 2
        g = axes([S[0], S[-1]], [0, 1], x_length=6.4, y_length=4.4, xlabel=r"price, 15 days before expiry",
                 ylabel=r"shares held against one short call", xticks=[90, 100, 110], yticks=[0, 0.5, 1],
                 font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        top = ax.plot_line_graph(S, np.clip(hi, 0, 1), add_vertex_dots=False, line_color=NET, stroke_width=3)
        bot = ax.plot_line_graph(S, np.clip(lo, 0, 1), add_vertex_dots=False, line_color=NET, stroke_width=3)
        fill = Polygon(*[ax.c2p(a, b) for a, b in zip(S, np.clip(hi, 0, 1))],
                       *[ax.c2p(a, b) for a, b in zip(S[::-1], np.clip(lo, 0, 1)[::-1])], stroke_width=0,
                       fill_color=NET, fill_opacity=0.25)
        ww = VGroup(DashedVMobject(curve(ax, S, np.clip(wl, 0, 1), WHITE, stroke_width=2), num_dashes=30),
                    DashedVMobject(curve(ax, S, np.clip(wh, 0, 1), WHITE, stroke_width=2), num_dashes=30))
        rows = h["band"]["rows"]
        r5 = next(r for r in rows if abs(r["cost"] - 0.005) < 1e-9)
        side = VGroup(
            label(r"a network learns where not to trade", font_size=24),
            label(r"when every trade costs 0.5\%", font_size=22, color=GREY_A),
            legend([(NET, r"the band it learned: inside, do nothing"), (WHITE, r"the band theory derived in 1997")],
                   font_size=18),
            MathTex(rf"\text{{price to charge: }}{r5['deep']['price']:.2f}\ \ \text{{vs}}\ \ {r5['delta']['price']:.2f}"
                    rf"\ \text{{hedging daily}}", font_size=26, color=NET),
            firm_card(r"J.P. Morgan, 2022", r"about 70\% of the bank's Euro Stoxx flow options quoted and hedged by "
                      r"machine, as reported", source=r"Risk.net", width=4.6, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.5)
        src = illustration(r"the deep hedger of chapters 7 and 8; a 30-day at-the-money call, 20\% volatility")
        with self.voiceover(
            "This is a neural network learning to hedge an option when every trade costs half a percent. It learns "
            "a corridor around the hedge: inside it, do nothing; outside it, trade back to the nearest edge. "
            "<bookmark mark='a'/> Theory derived such a corridor in 1997, for small costs. The network's is "
            "narrower, and on the same simulated paths it needs a lower price: "
            f"{r5['deep']['price']:.2f} against {r5['delta']['price']:.2f} for hedging every day. "
            "<bookmark mark='b'/> Machines like this already hedge real books: by 2022, Risk.net reported, about "
            "seventy percent of J.P. Morgan's Euro Stoxx flow options were quoted and hedged by machine."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]), FadeIn(side[1]))
            self.play(FadeIn(fill), Create(top), Create(bot), FadeIn(side[2][0]), run_time=2)
            vo.wait_until("a")
            self.play(Create(ww), FadeIn(side[2][1]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[4], shift=UP * 0.2))
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
            "hundred dimensions, and learning when to exercise. The deep hedger, its prices, and where it learns not "
            "to trade. Neural models that measure model risk. Machines that invent markets. And what it takes to "
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
