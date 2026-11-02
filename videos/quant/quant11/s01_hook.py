from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant11.common import GAMMA, OPT, PART, SPOT, THETA, VEGA, load, real_data


class Hook(VoiceoverScene):
    def construct(self):
        s = load("scalp")
        self.title_card()
        self.question()
        self.may2021(s)
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Gamma against theta")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part eleven. Trading options. Part ten priced an option by hedging it. This is the practitioner's part: "
            "how an options trader thinks, what each position is a bet on, and how the desks that make these markets "
            "earn their living, and sometimes get into trouble."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def question(self):
        q = desk_question(r"You are long a straddle, delta-hedged. The stock does not move all week. How do you lose "
                          r"money? And when do you make it?", width=10.6, font_size=28).to_edge(UP, buff=0.5)
        rows = [cmath(r"d\Pi", r"\approx", r"\tfrac12\,\Gamma S^2\left(\frac{dS^2}{S^2} - \sigma_{\text{imp}}^2\,dt\right)"
                      r" + \mathcal{V}\, d\sigma_{\text{imp}}", font_size=36, colors={r"d\Pi": OPT})]
        whys = [why(r"long gamma pays when the stock moves more than implied; theta charges the implied variance every "
                    r"day whether it moves or not; vega marks the book when implied volatility itself moves")]
        step = ladder(self, rows, whys, keep=1, top=1.0, x=-0.4, buff=0.9, edge=6.9)
        with self.voiceover(
            "An interview question from an options desk. You are long a straddle, a call and a put at the same "
            "strike, and you hedge its delta. The stock does not move all week. How do you lose money, and when do "
            "you make it? <bookmark mark='a'/> Part ten's accounting gives the answer in one line. Each day a "
            "hedged option earns one half gamma times the squared move, and pays theta, the implied variance, "
            "whether the stock moves or not. A quiet week bleeds theta. And if implied volatility falls, the "
            "straddle loses its vega too. You make money when the stock moves more than the implied volatility "
            "said it would."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            step(0)
        self.wait(0.4)
        self.clear_scene()

    def may2021(self, s):
        t, S, book = np.asarray(s["t"]), np.asarray(s["S"]), np.asarray(s["book"])
        g1 = axes([0, 30], [50, 110], x_length=6.2, y_length=2.6, ylabel=r"bitcoin, per 100 at the start",
                  xticks=[0, 10, 20, 30], yticks=[60, 80, 100], font_size=16)
        g2 = axes([0, 30], [-6, 6], x_length=6.2, y_length=2.4, xlabel=r"days from 1 May 2021", ylabel=r"hedged "
                  r"straddle P\&L", xticks=[0, 10, 20, 30], yticks=[-5, 0, 5], font_size=16)
        VGroup(g1, g2).arrange(DOWN, buff=0.45).to_edge(LEFT, buff=0.7).shift(DOWN * 0.1)
        ls = curve(g1.ax, t[::2], S[::2], SPOT, stroke_width=2.5)
        k = DashedLine(g1.ax.c2p(0, 100), g1.ax.c2p(30, 100), color=GREY_B, stroke_width=1.5)
        lb = curve(g2.ax, t[::2], np.clip(book[::2], -6, 6), OPT, stroke_width=3)
        z = DashedLine(g2.ax.c2p(0, 0), g2.ax.c2p(30, 0), color=GREY_C, stroke_width=1.5)
        side = VGroup(
            label(rf"bought at DVOL: {100 * s['iv']:.0f}\% implied", font_size=24, color=VEGA),
            label(rf"realized over the month: {100 * s['rv']:.0f}\%", font_size=24, color=GAMMA),
            MathTex(rf"\text{{P\&L: }} {s['pnl']:+.1f}\ \text{{on a premium of }} {s['premium']:.1f}", font_size=28,
                    color=OPT),
            wrapped_label(r"realized was almost twice implied, yet the straddle earned little: the crash carried "
                          r"bitcoin far from the strike, where gamma is small, so the biggest moves paid least", 4.4, 20,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Binance BTCUSDT hourly; Deribit DVOL; hedged every hour, no costs")
        with self.voiceover(
            "Here is the trade, on a real month. On the first of May 2021 you buy a thirty-day at-the-money Bitcoin "
            f"straddle at the market's implied volatility of {100 * s['iv']:.0f} percent, and hedge it every hour. "
            "<bookmark mark='a'/> On the nineteenth, Bitcoin crashed: at its low it had lost almost half its value. "
            f"Over the month it moved at a realized volatility of {100 * s['rv']:.0f} percent, nearly twice what you "
            "paid for. <bookmark mark='b'/> And the straddle made only "
            f"{s['pnl']:.1f} on a premium of {s['premium']:.1f}. The crash carried Bitcoin far from the strike, where "
            "gamma is small, so the biggest moves paid the least. Being right about volatility is not enough; where "
            "the volatility happens matters. That is the kind of thing this part is about."
        ) as vo:
            self.play(FadeIn(g1), Create(k), FadeIn(side[0]), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(ls), FadeIn(side[1]), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(z), Create(lb), FadeIn(side[2]), run_time=2.5)
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Positions as Greeks; gamma against theta; vanna, volga, and what each strategy bets on",
            r"Gamma scalping on a real bitcoin path",
            r"Volatility trading: the premium, and a forecaster's edge, tested",
            r"The market maker's book: quoting, inventory, and the firms that do it",
            r"Expiry and pin risk; dispersion and implied correlation",
            r"India's expiry-day boom, and the SEBI case against Jane Street (allegations, contested)",
            r"Hedging under costs: bands, and a learned hedger",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan. Positions as Greeks, and what each strategy is a bet on. Gamma scalping on a real path. "
            "Volatility trading, and whether a forecast gives an edge. The market maker's book, and the firms that "
            "keep one. Expiry, pin risk and dispersion. India's expiry-day boom, and the regulator's case against "
            "Jane Street, which the firm contests. And hedging when every trade costs money."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=10))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("vol",))
        with self.voiceover(
            "In the House, the volatility desk opened in Part ten. <bookmark mark='a'/> This part gives it its "
            "options quoting engine: the book as Greeks, quotes that lean against inventory, and hedging that knows "
            "what trading costs."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
