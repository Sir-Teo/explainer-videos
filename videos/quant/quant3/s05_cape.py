from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant3.common import CASH, PART, PRICE, VALUE, load, real_data

C_ = {r"P": PRICE, r"E_1": VALUE, r"b": CASH, r"r": QC.IMPLIED, r"g": CASH}


class CAPE(VoiceoverScene):
    def construct(self):
        c = load("cape")
        self.card()
        self.multiples()
        self.series(c)
        self.scatter(c)

    def card(self):
        c = chapter_card(4, r"Multiples and the CAPE", r"Is the market expensive?", part=PART)
        with self.voiceover("Chapter four. Multiples, and Shiller's CAPE."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def multiples(self):
        rows = [cmath(r"P", r"=", r"\frac{D_1}{r - g}", r"=", r"\frac{b\,E_1}{r - g}", colors=C_, font_size=42),
                cmath(r"\frac{P}{E_1}", r"=", r"\frac{b}{r - g}", colors=C_, font_size=46)]
        whys = [why(r"Gordon, with dividends a fraction $b$ of earnings: the payout ratio"),
                why(r"a P/E is a compressed DCF: a high multiple means low $r$ or high $g$")]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=-2.6, buff=0.9, edge=6.9)
        ev = VGroup(
            MathTex(r"\frac{\text{EV}}{\text{EBITDA}}", font_size=40),
            wrapped_label(r"enterprise value (equity plus debt minus cash) over earnings before interest, tax, "
                          r"depreciation and amortisation: compares firms however they are financed", 7.4, 23, GREY_A),
        ).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "Analysts rarely run a full DCF for every stock. They use multiples, and a multiple is a DCF folded "
            "up. Take Gordon's formula, and write the dividend as a fraction b of earnings, the payout ratio. "
            "<bookmark mark='a'/> Divide by earnings, and the price-to-earnings ratio is the payout over r minus g. "
            "A high P/E is a bet on low discount rates or high growth, nothing more. <bookmark mark='b'/> When firms "
            "carry different amounts of debt, the desk uses enterprise value, the whole firm, over earnings before "
            "interest, tax and depreciation, so that leverage does not distort the comparison."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(ev))
        self.wait(0.4)
        self.clear_scene()

    def series(self, c):
        t, v = np.asarray(c["cape_series_t"]), np.asarray(c["cape_series"])
        g = axes([1880, 2021], [0, 46], x_length=10.6, y_length=4.6, ylabel=r"CAPE: real price over ten years of real "
                 r"earnings", xticks=[1900, 1930, 1960, 1990, 2020], yticks=[0, 10, 20, 30, 40],
                 xfmt=lambda x: f"{int(x)}", font_size=18).move_to(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, v, PRICE, stroke_width=2.5)
        mean = DashedLine(ax.c2p(1880, c["mean_cape"]), ax.c2p(2021, c["mean_cape"]), color=GREY_B, stroke_width=2)
        mlab = label(rf"average {c['mean_cape']:.0f}", font_size=20, color=GREY_B).next_to(mean, RIGHT, buff=0.1)
        marks = VGroup()
        for when, val, txt in [(1929.67, 32.6, r"Sept.\ 1929: 32.6"), (1920.92, 4.8, r"Dec.\ 1920: 4.8"),
                               (1982.5, 6.6, r"1982: 6.6"), (1999.92, 44.2, r"Dec.\ 1999: 44.2"),
                               (2020.92, c["cape_now"], rf"Dec.\ 2020: {c['cape_now']:.1f}")]:
            d = Dot(ax.c2p(when, val), radius=0.06, color=YELLOW)
            lab = label(txt, font_size=19, color=YELLOW).next_to(d, UP if val > 20 else DOWN, buff=0.1)
            marks.add(VGroup(d, lab))
        marks[4][1].next_to(marks[4][0], LEFT, buff=0.1).shift(UP * 0.15)
        src = real_data(r"Shiller's data; CAPE from Campbell and Shiller (1988, 1998)")
        with self.voiceover(
            "One year of earnings is noisy: they collapse in recessions and make the P/E spike. In 1988 John "
            "Campbell and Robert Shiller smoothed them, dividing the real price by the average of ten years of real "
            "earnings: the cyclically adjusted P/E, or CAPE. Here it is since 1881. <bookmark mark='a'/> Its long "
            f"average is about {c['mean_cape']:.0f}. It reached thirty-three in September 1929, and forty-four in "
            "December 1999, its highest ever. It fell below five in 1920 and below seven in 1982. "
            "<bookmark mark='b'/> At the end of 2020, where our research window closes, it stood at nearly thirty-four."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            self.play(Create(line), run_time=3)
            vo.wait_until("a")
            self.play(Create(mean), FadeIn(mlab))
            self.play(LaggedStart(*[FadeIn(m) for m in marks[:4]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(marks[4]))
        self.wait(0.4)
        self.clear_scene()

    def scatter(self, c):
        x, y, t = np.log(np.asarray(c["cape"])), np.asarray(c["fwd"]), np.asarray(c["t"])
        g = axes([np.log(4), np.log(50)], [-0.08, 0.22], x_length=6.4, y_length=5.0,
                 xlabel=r"CAPE at the start (log scale)", ylabel=r"real return a year over the next ten years",
                 xticks=list(np.log([5, 10, 20, 40])), xfmt=lambda u: f"{np.exp(u):.0f}",
                 yticks=[-0.05, 0, 0.05, 0.10, 0.15, 0.20], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=18)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        cols = color_gradient([QC.SPOT, QC.IDEA], 8)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.022, color=cols[min(int((tt - 1881) / 130 * 8), 7)],
                            fill_opacity=0.7) for a, b, tt in zip(x, y, t)])
        xs = np.linspace(np.log(4.5), np.log(48), 50)
        fit = curve(ax, xs, c["intercept"] + c["slope"] * xs, WHITE, stroke_width=3)
        now = np.log(c["cape_now"])
        vline = DashedLine(ax.c2p(now, -0.08), ax.c2p(now, 0.22), color=QC.HOUSE, stroke_width=2)
        pred = Dot(ax.c2p(now, c["pred_now"]), radius=0.1, color=QC.HOUSE)
        side = VGroup(
            label(r"each dot: a month from 1881 to 2010, and the", font_size=21, color=GREY_A),
            label(r"real total return over the following ten years", font_size=21, color=GREY_A),
            MathTex(rf"R^2 = {c['r2']:.2f}", font_size=36),
            label(rf"{c['n']:,} starting months, but only about {c['n_indep']} independent decades".replace(",", "{,}"),
                  font_size=21, color=QC.LOSS),
            MathTex(rf"\text{{Dec.\ 2020: CAPE }} {c['cape_now']:.1f} \Rightarrow {100 * c['pred_now']:.1f}\%"
                    r"\text{ a year}", font_size=30, color=QC.HOUSE),
            label(r"sealed: the envelope opens on 2021--2030 in the finale", font_size=21, color=QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35)
        leg = VGroup(Dot(radius=0.05, color=cols[0]), label(r"1880s", font_size=17, color=GREY_B),
                     Dot(radius=0.05, color=cols[-1]), label(r"2000s", font_size=17, color=GREY_B)).arrange(RIGHT, buff=0.1)
        leg.next_to(g, UP, buff=0.05).align_to(g, RIGHT)
        with self.voiceover(
            "Does the CAPE tell you anything? Plot each month's CAPE against the real return of the next ten "
            "years. <bookmark mark='a'/> The cloud slopes down: high valuations have been followed by low decades, "
            "and low ones by high decades. The fit explains about a third of the variation in ten-year returns. "
            "<bookmark mark='b'/> But be careful with the count. There are over fifteen hundred dots, and each "
            "shares nine years and eleven months of its future with its neighbour. There are only about thirteen "
            "independent decades here, and with thirteen observations a slope this clear is far less certain than "
            "it looks. Part six makes that precise; it is Stambaugh's bias and the problem of overlapping "
            "observations. <bookmark mark='c'/> Read off the line at the end of 2020: a CAPE near thirty-four "
            "predicted a real return of about half a percent a year for the 2020s. That forecast goes into the "
            "sealed envelope. We will open it in the finale, against what actually happened."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(side[:2]))
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.002, run_time=3))
            vo.wait_until("a")
            self.play(Create(fit), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
            vo.wait_until("c")
            self.play(Create(vline), FadeIn(pred), FadeIn(side[4]))
            self.play(FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene()
