from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, BARRIER, GOOD, OPT, PART, SPOT, load, real_data, ymd_to_year


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
            "Part fifteen. Exotics and structured products: the options that banks build into notes and sell to "
            "savers, and what happens when the market finds their barriers."
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
        lbl = label(r"knock-in levels of notes sold in 2022--2023", font_size=19, color=BARRIER).next_to(
            ax.c2p(2022.3, 4.0), UP, buff=0.05)
        low = int(np.argmin(np.where((d[w] >= 20240101) & (d[w] <= 20240229), px[w], np.inf)))
        dot = Dot(ax.c2p(t[low], px[w][low]), radius=0.09, color=BAD)
        src = real_data(r"Yahoo Finance: China Southern CSI 500 ETF, daily closes; notes: chapter 9's stylized book")
        with self.voiceover(
            "This is China's CSI 500 index, through its largest fund, from 2021. Over those years Chinese brokers "
            "sold a note called the snowball, tens of billions of dollars of it by some estimates. It paid around "
            "fifteen percent a year, unless the index fell by about a quarter. <bookmark mark='a'/> Here are the knock-in levels of notes sold in "
            "2022 and 2023. <bookmark mark='b'/> In January 2024 the index went through them, and the snowballs "
            "melted. This part is about how such products are built, priced and hedged, and why their hedges move "
            "the market they are written on."
        ) as vo:
            self.play(FadeIn(g), Create(line), FadeIn(src), run_time=3)
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(k) for k in kis], lag_ratio=0.1, run_time=2), FadeIn(lbl))
            vo.wait_until("b")
            self.play(FadeIn(dot, scale=0.5), Flash(dot, color=BAD))
        self.wait(0.5)
        self.clear_scene()

    def predict(self):
        card = pause_card(r"A note pays 15\% a year unless the index falls by a quarter. Is 15\% a gift, a fair price, "
                          r"or a bargain for the bank?", width=9.0)
        with self.voiceover(
            "Before we start, a question to hold on to. A note pays fifteen percent a year, unless the index falls by "
            "a quarter. Is that a gift, a fair price, or a bargain for the bank? Chapter seven answers it with a "
            "simulation."
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
            "How we got here. Exotic options are as old as option pricing. In 1973, in the same paper that proves "
            "Black and Scholes, Robert Merton priced a call that dies at a barrier. In 1979 Barry Goldman, Howard Sosin "
            "and Mary Ann Gatto priced the lookback, the right to buy at the lowest price. <bookmark mark='a'/> In "
            "1987, as the story is told, two Bankers Trust traders in Tokyo priced options on the average price of "
            "crude oil, and called them Asian. Angelien Kemna and Ton Vorst found their control variate in 1990, and "
            "Eric Reiner and Mark Rubinstein catalogued the barrier family in 1991. <bookmark mark='b'/> In 1995 Marco "
            "Avellaneda, Arnon Levy and Antonio Parás, and independently Terry Lyons, priced the uncertainty of "
            "volatility itself, and in 1997 Mark Broadie, Paul Glasserman and Steven Kou fixed barriers that are "
            "watched only at the close. <bookmark mark='c'/> Then the products reached savers. In January 2016 "
            "Korea's regulators counted thirty-seven trillion won of notes on Hong Kong's index of Chinese companies "
            "as it fell toward their barriers. In 2018 Natixis took a hit of about two hundred and sixty million euros "
            "on structured products sold in Asia, mostly Korean autocallables. And in 2024 China's snowballs melted, while Korea's savers lost again."
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
            "The plan. We take a note apart into priced pieces, and look at what its buyers actually earned. "
            "Barriers, derived two ways and hedged without trading; digitals, touches and averages. The snowball, "
            "priced, simulated and turned into Greeks you can walk around. January 2024 and Korea's notes, rebuilt on "
            "the real paths. Correlation, cliquets, and the risk a single volatility cannot see. Then model risk: "
            "uncertain volatility, models that agree on vanillas and disagree on exotics, and the hedging flows of a "
            "whole book. And finally a neural pricer trained on screen, how banks reserve for all this, and the "
            "frontier."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("vol",))
        with self.voiceover(
            "In the House, the volatility desk builds its exotics pricer. <bookmark mark='a'/> And it learns what every "
            "issuer learns: the hard part is not the price, it is the hedge."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
