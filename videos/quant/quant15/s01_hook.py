from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, BARRIER, GOOD, OPT, PART, SPOT, load, real_data, ymd_to_year, axes, data_range, pause_card


class Hook(VoiceoverScene):
    def construct(self):
        m = load("market")
        b = load("book2024")
        self.title_card()
        self.cliff(m, b)
        self.predict()
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"The snowball")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            'Part fifteen: exotics and structured products. We will specify, price and hedge the contingent claims inside a note, then inspect what changes when a barrier is reached.'
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def cliff(self, m, b):
        c = m["csi500"]
        d = np.asarray(c["date"])
        px = np.asarray(c["close"])
        w = (d >= 20210101) & (d <= 20240430)
        t = ymd_to_year(d[w])
        g = axes([2021, 2024.4], [3.5, 8.5], x_length=10.0, y_length=4.6, ylabel=r"CSI 500 ETF (510500)",
                 xticks=[2021, 2022, 2023, 2024], yticks=[4, 5, 6, 7, 8], font_size=16).move_to(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, px[w], SPOT, stroke_width=2.2)
        kis = VGroup()
        for nt in b["notes"]:
            if nt["ki"] is None or nt["ki"] < 20240101:
                continue
            t0 = ymd_to_year([nt["start"]])[0]
            lvl = 0.75 * nt["S0"]
            kis.add(Line(ax.c2p(t0, lvl), ax.c2p(2024.2, lvl), stroke_color=BARRIER, stroke_width=1.4, stroke_opacity=0.7))
        lbl = label(r"2022--2023 stylized notes that knocked in during 2024", font_size=19, color=BARRIER).next_to(
            ax.c2p(2022.3, 4.0), UP, buff=0.05)
        low = int(np.argmin(np.where((d[w] >= 20240101) & (d[w] <= 20240229), px[w], np.inf)))
        dot = Dot(ax.c2p(t[low], px[w][low]), radius=0.09, color=BAD)
        src = real_data(r"Yahoo Finance: China Southern CSI 500 ETF, daily closes; notes: chapter 9's stylized book")
        with self.voiceover(
            "This is the CSI 500 through the daily closes of its 510500 ETF, from 2021. Chinese brokers sold snowball notes linked to such indices; public estimates of their size differ. Our illustration uses a fifteen percent annual coupon, monthly knock-out at 103 percent after three months, daily knock-in below 75 percent, and a two-year limit. <bookmark mark='a'/> These are the levels of our stylized 2022 and 2023 notes that knocked in during 2024. <bookmark mark='b'/> The winter sell-off crossed them. Knock-in records a state, not an immediate realized loss: subsequent recovery or knock-out can still matter. We will price the contractual cash flows and reconstruct a hypothetical hedge on this historical ETF path. It illustrates possible trading pressure; it does not identify the cause of the market fall."
        ) as vo:
            self.play(FadeIn(g), Create(line), FadeIn(src), run_time=3)
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(k) for k in kis], lag_ratio=0.1, run_time=2), FadeIn(lbl))
            vo.wait_until("b")
            self.play(FadeIn(dot, scale=0.5), Flash(dot, color=BAD))
        self.wait(0.5)
        self.clear_scene()

    def predict(self):
        card = pause_card(r"A note advertises 15\% a year with a 75\% knock-in. Which claims fund the coupon, "
                          r"and what margin does the issuer keep?", width=10.8, font_size=34)
        card.move_to(ORIGIN)
        with self.voiceover(
            'Keep a question in mind. A note advertises fifteen percent a year, with conditional repayment and a knock-in a quarter below its starting level. Which contingent claims fund that coupon, and how much margin remains for the issuer? Chapter seven prices our specified contract; the headline rate alone cannot answer.'
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.play(FadeOut(card))

    def history(self):
        events = [
            (1973, r"Merton: the down-and-out call, in the paper that also proves Black--Scholes", QC.IDEA),
            (1979, r"Goldman, Sosin and Gatto: the lookback, an option to buy at the low", QC.IDEA),
            (1987, r"Bankers Trust in Tokyo prices options on the average oil price: ``Asian'' options (as the story is told)",
             QC.IDEA),
            (1990, r"Kemna and Vorst: the geometric average as a control variate", QC.IDEA),
            (1991, r"Reiner and Rubinstein: the barrier family catalogued", QC.IDEA),
            (1995, r"Avellaneda, Levy and Par\'as; Lyons: a price for not knowing the volatility", QC.IDEA),
            (1997, r"Broadie, Glasserman and Kou: barriers watched at the close", QC.IDEA),
            (2016, r"Korea: 37 trillion won of notes on the HSCEI as the index nears their barriers", QC.CRISIS),
            (2018, r"Natixis: a hit of about 260 million euros on Asian equity derivatives", QC.FIRM),
            (2024, r"China's snowballs melt; Korea's HSCEI notes lose again", QC.CRISIS),
        ]
        rows = VGroup(*[VGroup(label(str(y), font_size=24, color=c), label(t, font_size=21, color=GREY_A)).arrange(
            RIGHT, buff=0.3) for y, t, c in events]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        for r in rows:
            r[1].align_to(rows, LEFT).shift(RIGHT * 1.0)
        if rows.width > 12.6:
            rows.scale_to_fit_width(12.6)
        head = label(r"How we got here", font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(head, DOWN, buff=0.3)
        strip = timeline(lit=tuple(y for y, _, _ in events), show_labels=False).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A short history. Merton's 1973 option-pricing paper includes a barrier call. Goldman, Sosin and Gatto priced lookbacks in 1979. <bookmark mark='a'/> Average-price options developed into the Asian family; Kemna and Vorst's geometric control appeared in 1990, followed by Reiner and Rubinstein's barrier formulas. <bookmark mark='b'/> The 1995 uncertain-volatility papers and 1997 discrete-barrier correction made model uncertainty and monitoring explicit. <bookmark mark='c'/> Retail issuance later brought these methods into episodes involving Korea, Natixis and Chinese snowballs. Each public episode has its own contracts and evidence; a shared product label does not make their risks or outcomes identical."
        ) as vo:
            self.play(FadeIn(head), FadeIn(strip), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows[:2]],
                                                                 lag_ratio=0.6, run_time=3))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows[2:5]], lag_ratio=0.6, run_time=3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows[5:7]], lag_ratio=0.6, run_time=2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows[7:]], lag_ratio=0.8, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"A note taken apart: bond, coupon strip, short put, and the issuer's margin; who buys, and what they earned",
            r"Barriers: reflection, the closed form and its PDE, discrete monitoring, static hedges",
            r"Digitals, one-touches and the call-spread hedge; Asians and lookbacks",
            r"The snowball priced: its outcomes, its carry, and the issuer's Greeks in 3D",
            r"January 2024 rebuilt on the real path; Korea's notes in 2016 and 2024; Natixis",
            r"Worst-of payoffs and correlation; cliquets and the risk vega cannot see",
            r"Uncertain volatility; model risk measured on the Surface; dealer flows",
            r"A neural pricer trained on screen; how desks reserve; the frontier",
        ], color=QC.IDEA, font_size=24)
        with self.voiceover(
            'We will take a note apart, price barriers, digitals and averages, then solve a snowball coupon and inspect its Greeks. Historical books illustrate conditional hedge demand. Dependence, cliquets, uncertain volatility and model ranges lead to a pricing proxy, governance and current research. The closing derivation separates a robust one-touch hedge from numerical model comparisons.'
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("vol",))
        with self.voiceover(
            "The House adds an exotics library to its volatility desk. <bookmark mark='a'/> Prices, hedges and valuation uncertainty will be checked separately."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
