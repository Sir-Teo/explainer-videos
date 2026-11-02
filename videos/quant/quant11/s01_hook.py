from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant11.common import GAMMA, OPT, PART, SPOT, THETA, VEGA, load, pause, real_data


class Hook(VoiceoverScene):
    def construct(self):
        s = load("scalp")
        self.title_card()
        self.question()
        self.may2021(s)
        self.history()
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
        t, S, book = np.asarray(s["t"])[::2], np.asarray(s["S"])[::2], np.asarray(s["book"])[::2]
        gam, the = np.asarray(s["gamma"])[::2], np.asarray(s["theta"])[::2]
        g1 = axes([0, 30], [50, 110], x_length=6.4, y_length=2.7, ylabel=r"bitcoin, per 100 at the start",
                  xticks=[0, 10, 20, 30], yticks=[60, 80, 100], font_size=16)
        g1.to_corner(UL, buff=0.5).shift(DOWN * 0.1)
        k = DashedLine(g1.ax.c2p(0, 100), g1.ax.c2p(30, 100), color=GREY_B, stroke_width=1.5)
        kl = label(r"strike", font_size=16, color=GREY_B).next_to(g1.ax.c2p(30, 100), RIGHT, buff=0.08)
        tr = ValueTracker(0.0)
        path = tracing(g1.ax, t, S, tr, SPOT, stroke_width=2.5)
        head = always_redraw(lambda: Dot(g1.ax.c2p(at_index(t, tr), at_index(S, tr)), radius=0.06, color=SPOT))
        day = always_redraw(lambda: MathTex(rf"\text{{day}}\ {at_index(t, tr):.0f}", font_size=26, color=GREY_A)
                            .next_to(g1, DOWN, buff=0.15).align_to(g1, LEFT))
        led = HedgeLedger(gam, the, book, tr, scale=8.0, half_width=2.0, font_size=20)
        led.move_to(DOWN * 2.2 + RIGHT * 0.3)
        side = VGroup(
            label(rf"bought at DVOL: {100 * s['iv']:.0f}\% implied", font_size=24, color=VEGA),
            label(rf"realized over the month: {100 * s['rv']:.0f}\%", font_size=24, color=GAMMA),
            MathTex(rf"\text{{P\&L: }} {s['pnl']:+.1f}\ \text{{on a premium of }} {s['premium']:.1f}", font_size=28,
                    color=OPT),
            wrapped_label(r"the crash carried bitcoin far from the strike, where gamma is small: the gamma bar stops "
                          r"growing just when the moves are biggest", 4.4, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_corner(UR, buff=0.45)
        pc = pause(r"Realized volatility was nearly twice what you paid for. Did the straddle double its money?",
                   width=4.6, font_size=21).next_to(side[1], DOWN, buff=0.3).align_to(side, LEFT)
        src = real_data(r"Binance BTCUSDT hourly; Deribit DVOL; hedged every hour, no costs")
        with self.voiceover(
            "Here is the trade, on a real month. On the first of May 2021 you buy a thirty-day at-the-money Bitcoin "
            f"straddle at the market's implied volatility of {100 * s['iv']:.0f} percent, and hedge it every hour. "
            "Watch the ledger fill: gamma's earnings, theta's bill, and the book. "
            "<bookmark mark='a'/> On the nineteenth, Bitcoin crashed: at its low it had lost almost half its value. "
            f"Over the month it moved at a realized volatility of {100 * s['rv']:.0f} percent, nearly twice what you "
            "paid for. Pause, and predict: did the straddle double its money? <bookmark mark='b'/> It made only "
            f"{s['pnl']:.1f} on a premium of {s['premium']:.1f}. Look at the gamma bar: it grew while Bitcoin wandered "
            "near the strike, and almost stopped once the crash had carried it far away, where gamma is small. "
            "Being right about volatility is not enough; where the volatility happens matters. That is the kind of "
            "thing this part is about."
        ) as vo:
            self.play(FadeIn(g1), Create(k), FadeIn(kl), FadeIn(side[0]), FadeIn(src), FadeIn(led))
            self.add(path, head, day)
            self.play(tr.animate.set_value(len(t) * 0.6), run_time=vo.until("a"), rate_func=linear)
            self.play(tr.animate.set_value(len(t) - 1), FadeIn(side[1]), FadeIn(pc), run_time=vo.until("b"),
                      rate_func=linear)
            self.play(FadeOut(pc), FadeIn(side[2]))
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def history(self):
        strip = timeline(lit=(1973, 1985, 1987, 2000, 2018, 2020, 2021, 2024)).to_edge(DOWN, buff=0.9)
        head = label(r"How we got here", font_size=34, color=GREY_A).to_edge(UP, buff=0.4)
        cards = VGroup(
            history_card(1973, r"the CBOE opens", r"listed options with standard strikes; within a few years "
                         r"traders carry sheets of model values onto the floor", color=QC.IDEA, width=3.1, font_size=18),
            history_card(1985, r"Glosten--Milgrom; Leland", r"why a market maker's spread exists; what hedging costs",
                         color=QC.IDEA, width=3.1, font_size=18),
            history_card(1987, r"Black Monday", r"index puts repriced for good; Susquehanna was founded months before",
                         color=QC.CRISIS, width=3.1, font_size=18),
            history_card(2018, r"short volatility breaks", r"February 2018; and in March 2020, a fund family's "
                         r"`hedged' options strategy", color=QC.CRISIS, width=3.1, font_size=18),
        ).arrange(RIGHT, buff=0.22, aligned_edge=UP).next_to(head, DOWN, buff=0.35)
        if cards.width > 13.2:
            cards.scale_to_fit_width(13.2)
        with self.voiceover(
            "How did options become a trade in volatility? In 1973 the Chicago Board Options Exchange opened, with "
            "standard contracts, the same year Black and Scholes published, and within a few years traders carried "
            "printed sheets of the model's values onto the floor. <bookmark mark='a'/> In 1985 Lawrence Glosten and Paul "
            "Milgrom explained why a market maker's spread exists, and Hayne Leland what hedging costs. "
            "<bookmark mark='b'/> In 1987 Black Monday repriced index puts for good, months after Susquehanna was "
            "founded to make options markets. <bookmark mark='c'/> Then the decades of selling volatility, and the "
            "days it broke: February 2018, and March 2020. In 2021 retail traders discovered short-dated options, and in 2024 "
            "India, home of the world's largest derivatives exchange by contracts traded, began to rein in its own "
            "boom."
        ) as vo:
            self.play(FadeIn(head), FadeIn(strip), FadeIn(cards[0], shift=UP * 0.2), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[3], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Positions as Greeks; a real day's P\&L explained; vanna, volga, and what each structure bets on",
            r"Gamma scalping on a real path; how often to hedge",
            r"The volatility premium in option returns; a forecaster's edge, tested; how much to bet",
            r"Making a market: the spread, inventory, and a market maker that learns; hedging the book",
            r"Expiry, pinning and early exercise; dispersion and implied correlation",
            r"India's expiry-day boom, and the SEBI case against Jane Street (allegations, contested)",
            r"A crisis file, the industry, and the frontier",
        ], color=QC.IDEA, font_size=24)
        with self.voiceover(
            "The plan. Positions as Greeks, a real day's profit and loss explained term by term, and what each "
            "structure is a bet on. Gamma scalping on a real path, and how often to hedge. The volatility premium, a "
            "forecaster's edge, and how much to bet. Making a market: the spread, inventory, a market maker that "
            "learns, and hedging the book. Expiry, pinning, early exercise and dispersion. India's expiry-day boom, "
            "and the regulator's case against Jane Street, which the firm contests. Then a crisis file, the "
            "industry, and the frontier."
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
