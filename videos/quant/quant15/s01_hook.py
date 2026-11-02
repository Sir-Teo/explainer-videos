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
        src = real_data(r"Yahoo Finance: China Southern CSI 500 ETF, daily closes; notes: chapter 5's stylized book")
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

    def objectives(self):
        card = objectives_card([
            r"The structuring business: a bond plus options, sold as one, and the issuer's margin",
            r"Barriers: the reflection principle, discrete monitoring and the BGK correction",
            r"Digitals and the call-spread hedge; Asians with a control variate; lookbacks",
            r"The snowball: fair coupon, the knock-in cliff, and the dealer's delta and vega",
            r"January 2024 rebuilt on the real path; Korea's HSCEI-linked notes",
            r"Worst-of and correlation; uncertain volatility and model reserves",
            r"A neural pricer for the whole book",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan. The business: who builds notes, who buys them, and the margin in between. Barriers, digitals "
            "and averages, and why some are easy to price and impossible to hedge. The snowball itself, priced and "
            "taken apart. January 2024, rebuilt on the real path, and Korea's version of the same story. Correlation, "
            "model uncertainty, and a neural network that reprices a whole book in microseconds."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows],
                                                     lag_ratio=0.5, run_time=10))
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
