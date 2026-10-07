from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.opposing_forces.common import (
    NOTE, TimeChart, at, label, shiller, show_chapter_card, source, tagged, ts, window, ym, yoy,
)

PAST1, PAST2 = BLUE_B, PURPLE_A  # the 2017-18 and 2021-22 loops (local to this chapter)


def smooth(v, n=3):
    out = np.full_like(v, np.nan)
    for i in range(n - 1, len(v)):
        out[i] = np.mean(v[i - n + 1:i + 1])
    return out


class Clock(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 13, r"Where are we on the clock?")
        self.schematic()
        self.real_loops()
        self.analogs()
        self.secular()

    # ------------------------------------------------------------------
    def schematic(self):
        R = 2.6
        circle = Circle(radius=R, color=GREY_B, stroke_width=2).move_to(DOWN * 0.3)
        c = circle.get_center()
        h = Line(c + LEFT * (R + 0.3), c + RIGHT * (R + 0.3), color=GREY_B, stroke_width=2)
        v = Line(c + DOWN * (R + 0.3), c + UP * (R + 0.3), color=GREY_B, stroke_width=2)
        nums = VGroup(*[Tex(str(n), font_size=34, color=GREY_A).move_to(c + (R + 0.35) * np.array([np.sin(a), np.cos(a), 0]))
                        for n, a in ((12, 0), (3, PI / 2), (6, PI), (9, 3 * PI / 2))])
        up = label(r"earnings rising", font_size=26, color=C.EARNINGS).next_to(v, UP, buff=0.95)
        dn = label(r"earnings falling", font_size=26, color=C.EARNINGS).next_to(v, DOWN, buff=0.45)
        lf = label(r"money\\easing", font_size=26, color=C.POLICY).next_to(h, LEFT, buff=0.55)
        rt = label(r"money\\tightening", font_size=26, color=C.RATE).next_to(h, RIGHT, buff=0.55)
        quads = VGroup(
            label(r"9--12\\earnings $\uparrow$\\multiples $\uparrow$", font_size=26).move_to(c + np.array([-1.2, 1.15, 0])),
            label(r"12--3\\earnings $\uparrow$\\multiples $\downarrow$", font_size=26).move_to(c + np.array([1.2, 1.15, 0])),
            label(r"3--6\\the bear\\market zone", font_size=26).move_to(c + np.array([1.2, -1.15, 0])),
            label(r"6--9\\recovery,\\priced early", font_size=26).move_to(c + np.array([-1.2, -1.15, 0])),
        )
        arc = Arc(radius=R + 0.6, start_angle=PI - 0.45, angle=-PI / 2 + 0.6, color=YELLOW, stroke_width=5, arc_center=c)
        arc.add_tip(tip_length=0.25, tip_width=0.25)
        with self.voiceover(
            "Timmer ties it all together with what he calls his clock. <bookmark mark='a'/> Up means earnings are rising; "
            "down, falling. <bookmark mark='b'/> Left means financial conditions are easing: money getting cheaper. Right "
            "means tightening. <bookmark mark='c'/> Markets tend to travel around it clockwise."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(v), FadeIn(up), FadeIn(dn))
            vo.wait_until("b")
            self.play(Create(h), FadeIn(lf), FadeIn(rt))
            vo.wait_until("c")
            self.play(Create(circle), FadeIn(nums), Create(arc))

        with self.voiceover(
            "<bookmark mark='a'/> From nine to twelve o'clock, earnings are rising and money is easy: both engines push "
            "prices up. <bookmark mark='b'/> From twelve to three, earnings are still rising, but money is tightening, so "
            "the multiple pushes the other way. <bookmark mark='c'/> From three to six, both turn against you. <bookmark "
            "mark='d'/> And from six to nine, earnings are still falling, but easier money lets prices recover early. "
            "<bookmark mark='e'/> Timmer's clock has been moving from the nine-to-twelve quadrant into twelve-to-three: "
            "rising earnings, held back by tightening financial conditions. That is this whole video, in one picture."
        ) as vo:
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(quads[[0, 1, 2, 3][i]]), run_time=0.6)
            vo.wait_until("e")
            self.play(Indicate(quads[1], color=YELLOW, scale_factor=1.15))
        self.clear_scene()

    # ------------------------------------------------------------------
    def real_loops(self):
        s = shiller()
        t, E = s["t"], s["E"]
        g = smooth(yoy(t, E))
        tr, rr = ts("real10_monthly")
        dr = np.full_like(rr, np.nan)
        dr[12:] = rr[12:] - rr[:-12]
        x = smooth(np.interp(t, tr, dr, left=np.nan, right=np.nan))
        lo, hi = -40, 60
        ch = TimeChart((-1.6, 2.6), (lo, hi), width=8.6, height=5.4, x_ticks=[-1, 0, 1, 2],
                       x_fmt=lambda v: rf"${v:+g}$" if v else "0", y_ticks=[-40, -20, 0, 20, 40, 60],
                       y_fmt=lambda y: rf"{y:g}\%").move_to(LEFT * 1.4 + DOWN * 0.25)
        x0, y0 = ch.hline(0, GREY_B, 2, dashed=False), Line(ch.c2p(0, lo), ch.c2p(0, hi), color=GREY_B, stroke_width=2)
        xl = label(r"change in 10-year real yield over the past year (points): tightening $\to$", font_size=24,
                   color=C.RATE).next_to(ch, DOWN, buff=0.05)
        yl = ch.y_title(r"earnings growth over the past year (3-month average, clipped at 60\%)", color=C.EARNINGS, font_size=24)

        def loop(a, b, col):
            m = (t >= a) & (t <= b) & np.isfinite(x) & np.isfinite(g)
            xs, ys = x[m], np.clip(g[m], lo, hi)
            path = ch.line(xs, ys, col, 4)
            tip = Arrow(ch.c2p(xs[-2], ys[-2]), ch.c2p(xs[-1], ys[-1]), buff=0, color=col, stroke_width=4,
                        max_tip_length_to_length_ratio=1.0, tip_length=0.2)
            return VGroup(path, tip), xs, ys

        L1, xs1, ys1 = loop(2016.0, 2019.1, PAST1)
        L2, xs2, ys2 = loop(2020.4, 2022.95, PAST2)
        L3, xs3, ys3 = loop(2024.4, 2026.45, YELLOW)
        # Clockwise check for the 2021-22 loop: up the left side, across the top, down the right side.
        assert xs2[0] < 0 and ys2[0] < 0 and ys2.max() == hi and xs2[-1] > 1 and ys2[-1] < 0
        t1 = tagged(r"2016--18", font_size=24, color=PAST1).next_to(ch.c2p(xs1[-1], ys1[-1]), RIGHT, buff=0.1)
        t2 = tagged(r"2020--22", font_size=24, color=PAST2).next_to(ch.c2p(xs2[-1], ys2[-1]), DOWN, buff=0.1)
        t3 = tagged(r"2024 to mid-2026", font_size=24, color=YELLOW).move_to(ch.c2p(-0.95, 13))
        k0, k1 = ym(2025, 10, 1), ym(2026, 10, 5)
        rt, rv = ts("real10_daily")
        dr_now = at(rt, rv, k1) - at(rt, rv, k0)
        now = ch.dot(dr_now, NOTE["trailing_eps_growth"], YELLOW, 0.11)
        now_l = tagged(rf"Oct 2026: real yields ${dr_now:+.1f}$,\\earnings about $+{NOTE['trailing_eps_growth']}\%$",
                       font_size=24, color=YELLOW).next_to(now, UP, buff=0.12)
        jump = Arrow(ch.c2p(xs3[-1], ys3[-1]), now.get_center(), buff=0.1, color=YELLOW, stroke_width=3, tip_length=0.18)
        jump.set_stroke(opacity=0.7)
        quads = VGroup(tagged(r"9--12", font_size=24).move_to(ch.c2p(-1.2, 52)), tagged(r"12--3", font_size=24).move_to(ch.c2p(2.2, 52)),
                       tagged(r"3--6", font_size=24).move_to(ch.c2p(2.2, -33)), tagged(r"6--9", font_size=24).move_to(ch.c2p(-1.2, -33)))
        src = source(r"Shiller (earnings); FRED (DFII10); latest point uses Timmer's $+30\%$")
        with self.voiceover(
            "We can draw the clock with real data. <bookmark mark='a'/> Up the side: how fast earnings have grown over "
            "the past year. Across: how much the real ten-year yield has changed over the past year, a simple gauge of "
            "tightening. <bookmark mark='b'/> Here's 2020 to 2022: earnings collapsed while rates fell, then earnings "
            "roared back while money stayed easy, then rates shot up while earnings were still rising, and finally "
            "earnings rolled over. A full clockwise loop. <bookmark mark='c'/> 2016 to 2018 traced a smaller loop "
            "the same way."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ch), Create(x0), Create(y0), FadeIn(xl), FadeIn(yl), FadeIn(quads), FadeIn(src))
            vo.wait_until("b")
            self.play(Create(L2), run_time=4, rate_func=linear)
            self.play(FadeIn(t2))
            vo.wait_until("c")
            self.play(Create(L1), run_time=3, rate_func=linear)
            self.play(FadeIn(t1))

        with self.voiceover(
            "<bookmark mark='a'/> And here's this cycle, up to the middle of 2026: earnings accelerating in the upper "
            "left. <bookmark mark='b'/> Since then, real yields have jumped more than a point, pushing the market to the "
            "right, into twelve to three. Timmer says the market keeps following the 2017 to 2018 and the 2021 to 2022 "
            "playbooks closely."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(L3), run_time=2.5, rate_func=linear)
            self.play(FadeIn(t3))
            vo.wait_until("b")
            self.play(Create(jump), FadeIn(now), FadeIn(now_l))
        self.clear_scene()

    # ------------------------------------------------------------------
    def analogs(self):
        t, v = ts("spy_weekly")

        def drawdown(a, b):
            m = (t >= a) & (t <= b)
            vv = v[m]
            return float((vv / np.maximum.accumulate(vv) - 1).min())

        d18, d22 = drawdown(2018.3, 2019.1), drawdown(2021.7, 2022.95)
        assert -0.20 < d18 < -0.17 and -0.26 < d22 < -0.24
        cols = VGroup(
            VGroup(label(r"2017--18", font_size=36, color=PAST1),
                   label(r"earnings boom (tax cuts)", font_size=26), label(r"Fed hiking, shrinking its balance sheet", font_size=26),
                   label(r"then: a drop of nearly 20\% in late 2018", font_size=26, color=C.RATE)),
            VGroup(label(r"2021--22", font_size=36, color=PAST2),
                   label(r"earnings boom (reopening)", font_size=26), label(r"Fed pivots hard to tightening", font_size=26),
                   label(r"then: a bear market of about 25\% in 2022", font_size=26, color=C.RATE)),
        )
        for col in cols:
            col.arrange(DOWN, buff=0.22)
        cols.arrange(RIGHT, buff=1.2).move_to(UP * 0.4)
        caution = label(r"Analogs, not forecasts: history rhymes loosely,\\and Timmer doesn't call for a bear market.",
                        font_size=26, color=GREY_A).to_edge(DOWN, buff=0.6)
        src = source(r"Nasdaq (SPY weekly closes)")
        with self.voiceover(
            "It's worth remembering what those playbooks looked like. <bookmark mark='a'/> In 2017 and 2018, a tax-cut "
            "earnings boom ran into a Fed that was raising rates and shrinking its balance sheet. Late in 2018, stocks fell "
            "nearly twenty percent. <bookmark mark='b'/> In 2021 and 2022, a reopening earnings boom ran into a Fed "
            "that pivoted hard to tightening, and 2022 brought a bear market of about twenty-five percent. <bookmark "
            "mark='c'/> Analogs aren't forecasts, and Timmer doesn't call for a bear market. But in both, the twelve to "
            "three phase is where rates won the tug of war for a while."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(cols[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cols[1], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(caution))
        self.clear_scene()

    # ------------------------------------------------------------------
    def secular(self):
        s = shiller()
        t, real = s["t"], s["P"] / s["CPI"]
        ok = np.isfinite(real)
        t, real = t[ok], real[ok]
        real = real / real[-1]

        def cagr(a, b):
            ia, ib = int(np.argmin(abs(t - a))), int(np.argmin(abs(t - b)))
            return 100 * ((real[ib] / real[ia]) ** (1 / (t[ib] - t[ia])) - 1)

        bulls = [(1949.5, 1966.0), (1982.6, 2000.7), (2009.2, t[-1])]
        rets = [cagr(a, b) for a, b in bulls]
        avg = cagr(1900, t[-1])
        assert all(r > 9 for r in rets) and 2 < avg < 3.5
        ch = TimeChart((1900, 2027), (0.008, 1.5), width=10.8, height=4.8, x_ticks=range(1900, 2030, 20), log_y=True,
                       y_ticks=[0.01, 0.1, 1.0], y_fmt=lambda y: {0.01: r"1\%", 0.1: r"10\%", 1.0: r"100\%"}[y],
                       ).move_to(DOWN * 0.45)
        yl = ch.y_title(r"S\&P 500, after inflation, log scale (today $=$ 100\%)", color=C.PRICE)
        line = ch.line(*window(t, real, 1900), C.PRICE, 3)
        spans = VGroup(*[ch.span(a, b, C.EARNINGS, 0.15) for a, b in bulls])
        tags = VGroup(*[tagged(rf"{int(a)}--{'' if i == 2 else int(b)}\\${r:.0f}\%$/yr", font_size=22, color=C.EARNINGS).move_to(
            ch.c2p((a + b) / 2, 0.012)) for i, ((a, b), r) in enumerate(zip(bulls, rets))])
        tags[2].shift(LEFT * 0.25)
        avg_l = tagged(rf"long-run average since 1900: about ${avg:.0f}\%$ a year", font_size=24).move_to(ch.c2p(1935, 0.6))
        src = source(r"Shiller data: real price, excluding dividends")
        with self.voiceover(
            "Finally, the biggest picture. <bookmark mark='a'/> Here's the S&P 500 since 1900, after inflation, on a log "
            "scale. Long stretches of strong gains, secular bull markets, alternate with long stretches of going "
            "nowhere. <bookmark mark='b'/> From 1949 to 1966, and from 1982 to 2000, prices rose ten to twelve percent a "
            "year after inflation, against a long-run average of about three. <bookmark mark='c'/> By Timmer's count, "
            "which he admits is a minority view, the current secular bull began in 2009. That makes it about seventeen "
            "years old, about as long as the last two, and he thinks it's in the final innings of above-average returns."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ch), FadeIn(yl), FadeIn(src))
            self.play(Create(line), run_time=3, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(spans[:2]), FadeIn(tags[:2]), FadeIn(avg_l))
            vo.wait_until("c")
            self.play(FadeIn(spans[2]), FadeIn(tags[2]))
        assert NOTE["secular_bull_start"] == 2009

        quote = tagged(r"``Consider harvesting those betas while the sun is shining!''", font_size=34, color=YELLOW)
        quote.to_edge(UP, buff=0.12)
        with self.voiceover(
            "Which leads to his closing line: <bookmark mark='q'/> consider harvesting those betas while the sun is "
            "shining. Beta is the return you get just from being exposed to the market. Harvesting it means collecting "
            "those gains, and rebalancing, while conditions are still good, rather than assuming the best returns will last "
            "forever."
        ) as vo:
            vo.wait_until("q")
            self.play(FadeIn(quote, shift=DOWN * 0.2))
        self.clear_scene()
