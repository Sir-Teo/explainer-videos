from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant1.common import BTC, GAIN, LOSS, PART, REAL, TAIL, bars, day_text, load, real_data, sci


class Crisis(VoiceoverScene):
    def construct(self):
        k = load("crisis2020")
        self.card()
        self.days(k)
        self.files(k)

    def card(self):
        c = chapter_card(13, r"March 2020", r"How rare was the worst week in a generation?", lit=(1987, 2008, 2020),
                         part=PART)
        with self.voiceover("Chapter thirteen. March 2020."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def _panel(self, d, r, col, title, lim):
        n = len(r)
        g = axes([0, n], [-lim, lim * 0.6], x_length=5.9, y_length=3.4, ylabel=title, font_size=17,
                 yticks=[-lim, -lim / 2, 0], yfmt=lambda v: f"{100 * v:.0f}\\%" if v else "0")
        ax = g.ax
        bb = bars(ax, np.arange(n) + 0.5, r, ax.x_length / n * 0.75, col, LOSS)
        # month ticks
        ticks = VGroup()
        for i, x in enumerate(d):
            if int(x) % 100 in (1, 2, 3) and (i == 0 or int(d[i - 1]) // 100 != int(x) // 100):
                ticks.add(label([r"", r"Jan", r"Feb", r"Mar", r"Apr"][(int(x) // 100) % 100], font_size=18,
                                color=GREY_B).next_to(ax.c2p(i, -lim), DOWN, buff=0.1))
        return g, bb, ticks

    def days(self, k):
        du, ru = np.asarray(k["us_window_d"]), np.asarray(k["us_window_r"])
        db, rb = np.asarray(k["btc_window_d"]), np.asarray(k["btc_window_r"])
        g1, b1, t1 = self._panel(du, ru, REAL, r"US market, daily", 0.14)
        g2, b2, t2 = self._panel(db, rb, BTC, r"Bitcoin, daily", 0.42)
        left = VGroup(g1, b1, t1)
        right = VGroup(g2, b2, t2)
        VGroup(left, right).arrange(RIGHT, buff=0.8).shift(DOWN * 0.4)
        iu = int(np.argmin(ru))
        ib = int(np.argmin(rb))
        lu = MathTex(rf"{100 * k['us_ret']:.1f}\%", font_size=30, color=TAIL)
        lu.next_to(b1[iu].get_bottom(), RIGHT, buff=0.15).shift(UP * 0.25)
        lb = MathTex(rf"{100 * k['btc_ret']:.1f}\%", font_size=30, color=TAIL)
        lb.next_to(b2[ib].get_bottom(), RIGHT, buff=0.15).shift(UP * 0.25)
        du_l = label(day_text(k["us_date"]), font_size=20, color=TAIL).next_to(lu, DOWN, buff=0.05).align_to(lu, LEFT)
        db_l = label(day_text(k["btc_date"]), font_size=20, color=TAIL).next_to(lb, DOWN, buff=0.05).align_to(lb, LEFT)
        src = real_data(r"Ken French's daily US market (value-weighted); Binance BTC/USDT, daily close to close (UTC)")
        with self.voiceover(
            "The crisis file for this part. In February 2020 a new virus spread out of China, and in the first three "
            "weeks of March the world's markets fell faster than ever before. Here are the daily returns of the "
            "American market, February to April. <bookmark mark='a'/> Three of the worst days in its history came "
            "within a week: the 9th, the 12th, and Monday the 16th of March, when it fell "
            f"{abs(100 * k['us_ret']):.0f} percent. Even Treasury bonds were sold, in a scramble for cash, until "
            "the Federal Reserve stepped in. <bookmark mark='b'/> Bitcoin, sold as digital gold, a refuge, had "
            f"its worst day on Thursday the 12th: {abs(100 * k['btc_ret']):.0f} percent, close to close, as leveraged "
            "positions on crypto exchanges were forcibly closed and selling fed on itself."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(t1), FadeIn(src))
            self.play(LaggedStart(*[GrowFromEdge(b_, UP if v < 0 else DOWN) for b_, v in zip(b1, ru)], lag_ratio=0.03,
                                  run_time=3))
            vo.wait_until("a")
            self.play(Indicate(b1[iu], color=TAIL), FadeIn(lu), FadeIn(du_l))
            vo.wait_until("b")
            self.play(FadeIn(g2), FadeIn(t2))
            self.play(LaggedStart(*[GrowFromEdge(b_, UP if v < 0 else DOWN) for b_, v in zip(b2, rb)], lag_ratio=0.03,
                                  run_time=3))
            self.play(Indicate(b2[ib], color=TAIL), FadeIn(lb), FadeIn(db_l))
        self.wait(0.4)
        self.clear_scene()

    def files(self, k):
        c1 = crisis_card(r"16 March 2020", r"The US market",
                         rf"against its own volatility over the year before ({100 * k['us_trail_sd']:.2f}\% a day)",
                         stats=[(rf"{abs(k['us_z']):.1f}\,\sigma", r"the fall"),
                                (sci(k["us_gauss_years"]), r"years between such days, bell curve"),
                                (rf"{k['us_tail_years']:.0f}", r"years, under the tail fitted to 1926--2019")],
                         width=6.3, font_size=24)
        c2 = crisis_card(r"12 March 2020", r"Bitcoin",
                         rf"against its own volatility over the year before ({100 * k['btc_trail_sd']:.1f}\% a day)",
                         stats=[(rf"{abs(k['btc_z']):.1f}\,\sigma", r"the fall"),
                                (r"10^{" + f"{int(np.floor(np.log10(k['btc_gauss_years'])))}" + r"}",
                                 r"years between such days, bell curve"),
                                (rf"{k['btc_tail_years']:.0f}", r"years, under the tail fitted to 2017--2020")],
                         width=6.3, font_size=24)
        pair = VGroup(c1, c2).arrange(RIGHT, buff=0.35, aligned_edge=UP).to_edge(UP, buff=0.5)
        lesson = VGroup(
            label(r"Measured against a bell curve: impossible, many times over.", font_size=26, color=GREY_A),
            label(r"Measured against the tails of chapter 5: the kind of day a career should expect.", font_size=26,
                  color=QC.IDEA),
            label(r"The same arithmetic for 19 October 1987 is in Part 10.", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.2).next_to(pair, DOWN, buff=0.6)
        with self.voiceover(
            "Measure them as this part has taught. Against the market's own volatility over the year before, the "
            f"16th of March was a {abs(k['us_z']):.1f} standard deviation fall. A bell curve says a day like that "
            f"comes about once in {k['us_gauss_years'] / 1e15:.0f} thousand trillion years. <bookmark mark='a'/> The "
            "power-law tail fitted to "
            "the ninety-four years before it says: about once every "
            f"{k['us_tail_years']:.0f} years. <bookmark mark='b'/> Bitcoin's fall was {abs(k['btc_z']):.0f} standard "
            "deviations, a number with no meaning for a bell curve: a waiting time with "
            f"{int(np.floor(np.log10(k['btc_gauss_years'])))} zeros. Its own tail says "
            f"roughly once every {k['btc_tail_years']:.0f} years. <bookmark mark='c'/> Impossible under one model, "
            "routine under another, and the difference between them is the difference between a fund that survives "
            "and one that doesn't. Part ten does the same arithmetic for the 19th of October 1987."
        ) as vo:
            self.play(FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("a")
            self.wait(0.5)
            vo.wait_until("b")
            self.play(FadeIn(c2, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x) for x in lesson], lag_ratio=0.5))
        self.wait(0.4)
        self.clear_scene()
