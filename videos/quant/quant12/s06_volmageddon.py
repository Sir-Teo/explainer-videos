from __future__ import annotations

from datetime import date

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, illustration, load, real_data


def _t(d):
    d = int(d)
    x = date(d // 10000, (d // 100) % 100, d % 100)
    return x.year + (x.timetuple().tm_yday - 1) / 365


class Volmageddon(VoiceoverScene):
    def construct(self):
        v = load("volmageddon")
        self.card()
        self.file(v)
        self.mechanics(v)
        self.dealers()

    def card(self):
        c = chapter_card(6, r"Volmageddon, and dealer gamma", r"What happens when everyone is short volatility?",
                         part=PART)
        with self.voiceover("Chapter six. Volmageddon, and dealer gamma."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def file(self, v):
        card = crisis_card(
            r"5 February 2018", r"Volmageddon",
            r"After a year of record calm, the VIX more than doubled in a single day. XIV, an exchange-traded note that "
            r"paid the daily inverse of short-term VIX futures and had been a favourite of individual investors, lost "
            r"more than 90\% of its value after the close; the next day its issuer, Credit Suisse, announced it would "
            r"redeem the note.",
            stats=[(rf"{v['before']:.2f} \to {v['after']:.2f}", r"the VIX, 2 to 5 February"),
                   (rf"+{100 * v['jump']:.0f}\%", r"its largest one-day rise on record"), (r"> 90\%", r"XIV's loss")],
            width=11.0, font_size=25)
        card.move_to(ORIGIN)
        src = note(r"FRED (VIXCLS); facts from the public record", font_size=18, color=GREY_B).to_corner(DR, buff=0.25)
        with self.voiceover(
            "On Monday the fifth of February 2018, after a year of record calm, the VIX more than doubled in a day, "
            f"from {v['before']:.0f} to {v['after']:.0f}. XIV, an exchange-traded note that paid the inverse of the "
            "daily change in short-term VIX futures, and a favourite of individual investors through the calm, lost "
            "more than ninety percent of its value after the close. The next day its issuer, Credit Suisse, "
            "announced it would redeem the note."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(src))
        self.wait(0.5)
        self.clear_scene()

    def mechanics(self, v):
        t = np.array([_t(d) for d in v["date"]])
        x = np.asarray(v["vix"])
        g = axes([2017.4, 2018.5], [5, 40], x_length=6.4, y_length=3.8, ylabel=r"the VIX", xticks=[2017.5, 2018.0, 2018.5],
                 xfmt=lambda u: {2017.5: "Jul 2017", 2018.0: "Jan 2018", 2018.5: "Jul 2018"}[round(u * 2) / 2],
                 yticks=[10, 20, 30, 40], font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        line = curve(g.ax, t, x, IV, stroke_width=2.5)
        side = VGroup(
            wrapped_label(r"a short-volatility note promises the inverse of each day's move in VIX futures; to keep that "
                          r"promise it must buy futures after they rise, near the close", 4.4, 20, GREY_A),
            wrapped_label(r"so a spike forces the issuer, and every similar fund, to buy the same contracts at the same "
                          r"moment, pushing them higher: the hedging is the shock's amplifier", 4.4, 20, BAD),
            wrapped_label(r"and in calm times, VIX futures sit above spot and roll down toward it: short-volatility "
                          r"funds earn that roll, a variance premium with a crash attached", 4.4, 20, OPT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = real_data(r"FRED: CBOE VIX, daily close")
        with self.voiceover(
            "Here is the VIX through that year: long and low, then a spike. <bookmark mark='a'/> The notes made it "
            "worse. A fund that promises the inverse of each day's move in VIX futures must buy futures after they "
            "rise, near the close, to keep its promise. When they spiked, every such fund had to buy the same "
            "contracts at the same moment, and the buying pushed them higher still. <bookmark mark='b'/> What had "
            "they been earning in the calm? VIX futures normally sit above spot and drift down toward it as they "
            "expire. Shorting them collects that roll: the variance risk premium of the next chapter, with a crash "
            "attached."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(line), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def dealers(self):
        rows = [cmath(r"\text{GEX}", r"=", r"\sum_i \Gamma_i\, S^2 \cdot \text{(dealer position)}_i", font_size=36,
                      colors={r"\text{GEX}": LV})]
        whys = [why(r"if dealers are long gamma, their hedging sells rallies and buys dips, damping moves; short "
                    r"gamma, they chase moves and amplify them")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.6, buff=0.8, edge=6.9)
        notes = VGroup(
            wrapped_label(r"Baltussen, Da, Lammers and Martens (2021): in some 60 futures markets since 1974, when hedgers "
                          r"are short gamma, the last half hour continues the day's move (intraday momentum)", 11.0, 21,
                          GREY_A),
            wrapped_label(r"same-day expiries (0DTE) on the S\&P 500 grew to over 40\% of its option volume by 2023; "
                          r"studies disagree on whether they move the index (Bandi, Fusari and Ren\`o 2023; Dim, Eraker "
                          r"and Vilkov 2024)", 11.0, 21, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "The same mechanism runs every day in stock options. Dealers who sell options hedge them, and the sign of "
            "their gamma decides which way their hedging pushes. <bookmark mark='a'/> Long gamma, they sell rallies "
            "and buy dips, and calm the market; short gamma, they chase it. Guido Baltussen and coauthors found, in "
            "some sixty futures markets over nearly fifty years, that when hedgers are short gamma, the last half hour of trading continues the "
            "day's move. And options that expire the same day, now a large share of S&P 500 options volume, have "
            "made the question urgent; the research so far disagrees on how much they move the market."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(n_) for n_ in notes], lag_ratio=0.5, run_time=3))
        self.wait(0.4)
        self.clear_scene()
