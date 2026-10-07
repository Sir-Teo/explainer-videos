from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.opposing_forces.common import (
    NOTE, TimeChart, at, index_at, label, shiller, show_chapter_card, source, tagged, ts, window, ym,
)


class StealthCorrection(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 10, r"A stealth correction")
        self.weights()
        self.relative()
        self.breadth()
        self.seasons()

    # ------------------------------------------------------------------
    def weights(self):
        # Illustrative only: a few giants and a long tail, roughly the shape of index weights.
        rng = np.random.default_rng(2)
        w = np.sort(1 / np.arange(1, 41) ** 1.1 + rng.uniform(0, 0.01, 40))[::-1]
        w = w / w.sum()

        def bars(weights, color, width=11.0):
            g = VGroup()
            for x in weights:
                g.add(Rectangle(width=max(0.02, width * x), height=0.9, stroke_color=BACKGROUND, stroke_width=1.5,
                                fill_color=color, fill_opacity=0.85))
            return g.arrange(RIGHT, buff=0)

        cap = bars(w, C.PRICE).move_to(UP * 1.3)
        eq = bars(np.full(40, 1 / 40), C.EQUAL_WEIGHT).move_to(DOWN * 1.2)
        cap_l = label(r"cap-weighted S\&P 500: weight $\propto$ company size", font_size=30, color=C.PRICE).next_to(cap, UP, buff=0.2)
        eq_l = label(r"equal-weighted: every company counts the same, the ``average stock''", font_size=30,
                     color=C.EQUAL_WEIGHT).next_to(eq, UP, buff=0.2)
        giants = Brace(VGroup(*cap[:5]), DOWN, color=GREY_A)
        giants_l = label(r"the trillion-dollar club", font_size=26, color=GREY_A).next_to(giants, DOWN, buff=0.1)
        sch = label(r"(schematic weights)", font_size=22, color=GREY_B).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Back to the stock market, and the strange calm we started with. <bookmark mark='c'/> The S&P 500 that "
            "everyone quotes weights each company by its size, its total market value. So a handful of trillion-dollar "
            "giants carry a big share of the index. <bookmark mark='e'/> There's also an equal-weighted version, where "
            "every company counts the same. It's a good gauge of how the average stock is doing."
        ) as vo:
            self.play(FadeIn(sch))
            vo.wait_until("c")
            self.play(FadeIn(cap_l), LaggedStart(*[GrowFromEdge(b, LEFT) for b in cap], lag_ratio=0.03))
            self.play(GrowFromCenter(giants), FadeIn(giants_l))
            vo.wait_until("e")
            self.play(FadeIn(eq_l), LaggedStart(*[GrowFromEdge(b, LEFT) for b in eq], lag_ratio=0.03))
        self.clear_scene()

    # ------------------------------------------------------------------
    def relative(self):
        t, s = ts("spy_daily_2026")
        _, r = ts("rsp_daily_2026")
        t0 = ym(2026, 1, 2)
        k0 = np.searchsorted(t, t0)
        t, s, r = t[k0:], 100 * s[k0:] / s[k0], 100 * r[k0:] / r[k0]
        sj, rj = at(t, s, ym(2026, 6, 30)), at(t, r, ym(2026, 6, 30))
        s_chg, r_chg = s[-1] / sj - 1, r[-1] / rj - 1
        assert 0.04 < s_chg < 0.05 and -0.01 < r_chg < 0.005
        ch = TimeChart((2026.0, 2026.8), (90, 116), width=9.4, height=4.6,
                       x_ticks=[ym(2026, m) for m in (1, 3, 5, 7, 9)],
                       x_fmt=lambda x: ["Jan", "Mar", "May", "July", "Sept"][[ym(2026, m) for m in (1, 3, 5, 7, 9)].index(x)],
                       y_ticks=[90, 95, 100, 105, 110, 115]).move_to(DOWN * 0.4 + LEFT * 0.9)
        yl = ch.y_title(r"2026, indexed to 100 on January 2", color=GREY_A)
        l_s, l_r = ch.line(t, s, C.PRICE, 4), ch.line(t, r, C.EQUAL_WEIGHT, 4)
        t_s = tagged(r"cap-weighted", font_size=26, color=C.PRICE).next_to(ch.c2p(t[-1], s[-1]), RIGHT, buff=0.15)
        t_r = tagged(r"equal-weighted", font_size=26, color=C.EQUAL_WEIGHT).next_to(ch.c2p(t[-1], r[-1]), RIGHT, buff=0.15)
        band = ch.span(ym(2026, 6, 30), t[-1], GREY_B, 0.1)
        nums = tagged(rf"since June 30: cap-weighted ${100 * s_chg:+.1f}\%$, equal-weighted ${100 * r_chg:+.1f}\%$",
                      font_size=26).move_to(ch.c2p(2026.5, 92.3))
        src = source(r"Nasdaq: SPY and RSP exchange-traded funds (prices)")
        with self.voiceover(
            "Here are the two versions in 2026. <bookmark mark='a'/> In blue, the familiar cap-weighted index; in "
            "gold, the equal-weighted one. <bookmark mark='b'/> From the end of June to early October, the big "
            "index rose about four percent. The average stock: down slightly. <bookmark mark='c'/> Timmer's reading: higher borrowing costs "
            "are starting to bite the weaker companies, while the trillion-dollar club shrugs it off, so far, at least."
        ) as vo:
            self.play(Create(ch), FadeIn(yl), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(l_s), Create(l_r), run_time=2.5, rate_func=linear)
            self.play(FadeIn(t_s), FadeIn(t_r))
            vo.wait_until("b")
            self.play(FadeIn(band), FadeIn(nums))
        self.clear_scene()

    # ------------------------------------------------------------------
    def breadth(self):
        tb, b50 = ts("breadth", "above50")
        _, b200 = ts("breadth", "above200")
        k = index_at(tb, ym(2026, 10, 2))
        assert abs(b50[k] - NOTE["above_50dma"]) < 1.5 and abs(b200[k] - NOTE["above_200dma"]) < 4.5
        ti, vi = ts("sp500_daily")
        ti, vi = window(ti, vi, tb[0])
        top = TimeChart((tb[0], 2026.8), (5400, 8000), width=10.4, height=2.0, x_ticks=[], y_ticks=[6000, 7000, 8000],
                        y_fmt=lambda y: f"{y:,.0f}".replace(",", "{,}")).move_to(UP * 1.75)
        bot = TimeChart((tb[0], 2026.8), (0, 100), width=10.4, height=2.6,
                        x_ticks=[ym(2025, m) for m in (1, 4, 7, 10)] + [ym(2026, m) for m in (1, 4, 7, 10)],
                        x_fmt=lambda x: ["Jan '25", "Apr", "July", "Oct", "Jan '26", "Apr", "July", "Oct"][
                            ([ym(2025, m) for m in (1, 4, 7, 10)] + [ym(2026, m) for m in (1, 4, 7, 10)]).index(x)],
                        y_ticks=[0, 25, 50, 75, 100], y_fmt=lambda y: rf"{y:g}\%").move_to(DOWN * 1.55)
        l_i = top.line(ti, vi, C.PRICE, 3)
        t_i = tagged(r"S\&P 500 index", font_size=24, color=C.PRICE).next_to(top.c2p(tb[0], 7600), RIGHT, buff=0.1)
        l50, l200 = bot.line(tb, b50, C.EQUAL_WEIGHT, 3), bot.line(tb, b200, GREY_A, 3)
        t50 = tagged(r"\% of stocks above their 50-day average", font_size=24, color=C.EQUAL_WEIGHT).next_to(
            bot.c2p(tb[0], 96), RIGHT, buff=0.1)
        t200 = tagged(r"\ldots above their 200-day average", font_size=24, color=GREY_A).next_to(t50, RIGHT, buff=0.3)
        d50 = bot.dot(tb[k], b50[k], YELLOW)
        n50 = tagged(rf"Oct 2: {b50[k]:.0f}\%", font_size=24, color=YELLOW).next_to(d50, DOWN, buff=0.12).shift(LEFT * 0.3)
        n200 = tagged(rf"{b200[k]:.0f}\%", font_size=24, color=GREY_A).next_to(bot.c2p(tb[k], b200[k]), UP, buff=0.12).shift(LEFT * 0.3)
        src = source(r"computed from Nasdaq daily closes of 500 members; FRED (SP500)")
        with self.voiceover(
            "Timmer measures this with breadth: the share of stocks trading above their own recent average price. "
            "<bookmark mark='a'/> On top, the index. <bookmark mark='b'/> Below, computed from the daily prices of all "
            "the index's members: the share above their fifty-day average, <bookmark mark='c'/> and above their "
            "two-hundred-day average. <bookmark mark='d'/> By October 2nd, only about a quarter of stocks were above their "
            "fifty-day average, and fewer than half above their two-hundred-day, while the index sat near a record."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(top), FadeIn(src))
            self.play(Create(l_i), FadeIn(t_i), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(bot), Create(l50), FadeIn(t50), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(l200), FadeIn(t200))
            vo.wait_until("d")
            self.play(FadeIn(d50), FadeIn(n50), FadeIn(n200))

        quote = tagged(r"``A stealth correction.''", font_size=34, color=YELLOW).to_edge(UP, buff=0.15).shift(RIGHT * 3.5)
        with self.voiceover(
            "Timmer's phrase for it: <bookmark mark='q'/> a stealth correction. The rising cost of money has the indexes "
            "in a vise. The headline number holds steady, while underneath, most stocks are already falling."
        ) as vo:
            vo.wait_until("q")
            self.play(FadeIn(quote, shift=DOWN * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def seasons(self):
        s = shiller()
        t, P = s["t"], s["P"]
        ret = np.full_like(P, np.nan)
        ret[1:] = 100 * (P[1:] / P[:-1] - 1)
        m = (t >= 1950) & (t < 2026)
        mon = np.round((t - np.floor(t)) * 12).astype(int)
        avg = np.array([np.nanmean(ret[m & (mon == k)]) for k in range(12)])
        assert np.argsort(avg)[:2].tolist() in ([8, 9], [9, 8]) and avg[10] > 1 and avg[11] > 1
        names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        base = DOWN * 1.6
        bars, labs = VGroup(), VGroup()
        for i, a in enumerate(avg):
            col = C.RATE if i in (8, 9) else (C.EARNINGS if i in (10, 11) else GREY_B)
            b = Rectangle(width=0.62, height=max(0.03, abs(a) * 2.2), stroke_width=0, fill_color=col, fill_opacity=0.85)
            x = -5.5 + i * 0.95
            b.move_to([x, base[1], 0], aligned_edge=DOWN if a >= 0 else UP)
            bars.add(b)
            labs.add(Tex(names[i], font_size=24, color=GREY_A).move_to([x, base[1] - 0.35, 0]))
        axis = Line([-6.0, base[1], 0], [5.4, base[1], 0], color=GREY_B, stroke_width=2)
        title = label(r"S\&P 500: average change in the monthly average price, 1950--2025", font_size=32).to_edge(UP, buff=0.5)
        note = tagged(r"the weak stretch ends in mid-October", font_size=28, color=YELLOW).move_to(UP * 1.6 + RIGHT * 2.4)
        src = source(r"Shiller monthly data (changes in monthly average prices)")
        with self.voiceover(
            "There's one more wrinkle: the calendar. <bookmark mark='a'/> Since 1950, measured by monthly average "
            "prices, the stretch from September into October has been the weakest of the year, and November and December "
            "among the strongest. <bookmark mark='b'/> "
            "Timmer notes that this seasonally weak stretch ends in about two weeks, just as earnings season gets going. "
            "If the pressure from rates eases, he thinks the indexes could easily pick up speed again. But for now, as he "
            "puts it: ignore the Fed Model at your peril."
        ) as vo:
            self.play(FadeIn(title), Create(axis), FadeIn(labs), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if a >= 0 else UP) for b, a in zip(bars, avg)], lag_ratio=0.08))
            vo.wait_until("b")
            self.play(FadeIn(note), Indicate(VGroup(bars[8], bars[9]), color=C.RATE))
        self.clear_scene()
