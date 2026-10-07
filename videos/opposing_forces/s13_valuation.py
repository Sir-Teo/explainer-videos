from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.opposing_forces.common import (
    FACTSET, NOTE, TimeChart, label, last, pe_plane, shiller, show_chapter_card, source, tagged, window,
)


class Valuation(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 12, r"Is this a bubble?")
        self.engines()
        self.forward()
        self.three_fed_models()

    # ------------------------------------------------------------------
    def engines(self):
        pl = pe_plane()
        self.add(pl, pl.iso)
        bubble = tagged(r"bubbles live here:\\the multiple doing the work", font_size=26, color=C.MULTIPLE)
        bubble.move_to(RIGHT * 5.3 + UP * 1.3)
        now = tagged(r"this cycle, lately:\\earnings doing the work", font_size=26, color=C.EARNINGS).move_to(RIGHT * 5.3 + DOWN * 0.6)
        with self.voiceover(
            "So is this a bubble? Timmer's answer: whatever this cycle is, it isn't a bubble, because bubbles are about "
            "valuation. <bookmark mark='a'/> Remember this map. A bubble is when the price climbs because the multiple "
            "keeps expanding, investors paying more and more for each dollar of profit. <bookmark mark='b'/> That's "
            "roughly what happened in the first two years of this bull market, when multiples soared while earnings "
            "lagged. <bookmark mark='c'/> Lately, it's been the reverse: earnings doing the work, the multiple shrinking."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(pl.dots[0]), FadeIn(pl.tags[0]))
            vo.wait_until("b")
            self.play(Create(pl.leg1), FadeIn(pl.dots[1]), FadeIn(pl.tags[1]), FadeIn(bubble), run_time=2)
            vo.wait_until("c")
            self.play(Create(pl.leg2), FadeIn(pl.dots[2]), FadeIn(pl.tags[2]), FadeIn(now), run_time=2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def forward(self):
        pts = [("Feb 13", FACTSET["fwd_pe_feb13"]), ("June 30", FACTSET["fwd_pe_june30"]), ("Oct 2", FACTSET["fwd_pe"])]
        base_y, scale = -2.4, 0.19
        bars, tops, names = VGroup(), VGroup(), VGroup()
        for i, (n, v) in enumerate(pts):
            x = -5.0 + i * 1.6
            b = Rectangle(width=1.0, height=v * scale, stroke_width=0, fill_color=C.MULTIPLE, fill_opacity=0.85)
            b.move_to([x, base_y, 0], aligned_edge=DOWN)
            bars.add(b)
            tops.add(MathTex(rf"{v:.1f}", font_size=30).next_to(b, UP, buff=0.1))
            names.add(Tex(n, font_size=24, color=GREY_A).move_to([x, base_y - 0.3, 0]))
        avg = FACTSET["fwd_pe_10y_avg"]
        avg_line = DashedLine([-5.8, base_y + avg * scale, 0], [-1.0, base_y + avg * scale, 0], color=WHITE, stroke_width=2)
        avg_l = label(rf"10-year average: {avg}", font_size=24).next_to(avg_line, RIGHT, buff=0.1)
        head1 = label(r"S\&P 500 forward P/E, 2026 (FactSet)", font_size=28, color=C.MULTIPLE).move_to([-3.4, 2.6, 0])
        cmp = VGroup(label(r"Timmer's figures:", font_size=28),
                     label(rf"cap-weighted forward P/E: {NOTE['fwd_pe_cap']}", font_size=30, color=C.PRICE),
                     label(rf"equal-weighted forward P/E: {NOTE['fwd_pe_equal']}", font_size=30, color=C.EQUAL_WEIGHT),
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.9, 0.9, 0])
        s = shiller()
        cape = s["CAPE"][np.isfinite(s["CAPE"])][-1]
        cape00 = np.nanmax(s["CAPE"][(s["t"] > 1999) & (s["t"] < 2001)])
        assert 40 < cape < 42 and 43.5 < cape00 < 45
        cape_l = VGroup(label(r"but Shiller's CAPE, which averages ten years", font_size=26, color=GREY_A),
                        label(r"of inflation-adjusted earnings:", font_size=26, color=GREY_A),
                        label(rf"{cape:.1f} today, vs.\ {cape00:.1f} at the 2000 peak", font_size=28, color=C.MULTIPLE),
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.9, -1.5, 0])
        src = source(r"FactSet Earnings Insight; Timmer's note; Shiller data")
        with self.voiceover(
            "By the usual yardstick, prices relative to the next twelve months of expected earnings, valuations look "
            "unremarkable. <bookmark mark='a'/> FactSet's forward P/E has fallen from 21.5 in February to 19, right around "
            "its ten-year average. <bookmark mark='b'/> Timmer puts the cap-weighted index at 19.7 times forward earnings, "
            "and the equal-weighted one at just 17.3."
        ) as vo:
            self.play(FadeIn(head1), FadeIn(names), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), FadeIn(tops))
            self.play(Create(avg_line), FadeIn(avg_l))
            vo.wait_until("b")
            self.play(FadeIn(cmp, shift=LEFT * 0.2))

        with self.voiceover(
            "To be fair, not every measure is so relaxed. <bookmark mark='c'/> Shiller's CAPE, which compares prices with "
            "ten years of inflation-adjusted earnings, is above 40, not far below its 2000 peak, partly because recent "
            "earnings have grown so fast that a ten-year average lags far behind them. Which measure you trust matters, "
            "and that's why Timmer checks the Fed Model three different ways."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeIn(cape_l, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def three_fed_models(self):
        y10 = last("dgs10_daily")
        fwd = 100 / NOTE["fwd_pe_cap"] - y10
        trail_now = 100 / FACTSET["trailing_pe"] - y10
        s = shiller()
        t = s["t"]
        fm = 100 / s["PE"] - s["GS10"]
        ecy = 100 * s["ECY"]
        ecy_now = ecy[np.isfinite(ecy)][-1]
        crash = (t > 2008.5) & (t < 2010.5)  # earnings collapsed: the ratio is meaningless there
        last_lower = t[np.isfinite(fm) & (fm <= trail_now) & (t < 2024) & ~crash][-1]
        ecy_lower = t[np.isfinite(ecy) & (ecy <= ecy_now) & (t < 2026)][-1]
        assert -0.4 < fwd < 0 and -1.6 < trail_now < -1.2 and 2002 < last_lower < 2003 and 2001.9 < ecy_lower < 2002.5
        title = label(r"The Fed Model, three ways: stocks' earnings yield minus the bond yield", font_size=32).to_edge(UP, buff=0.35)
        top = TimeChart((1960, 2027), (-5, 6), width=10.6, height=2.1, x_ticks=[], y_ticks=[-4, 0, 4],
                        y_fmt=lambda y: rf"{y:g}").move_to(UP * 1.3)
        bot = TimeChart((1960, 2027), (-2, 11), width=10.6, height=2.1, x_ticks=range(1960, 2030, 10),
                        y_ticks=[0, 5, 10], y_fmt=lambda y: rf"{y:g}").move_to(DOWN * 1.65)
        tt, vv = window(t, fm, 1960)
        tt2, vv2 = window(t, ecy, 1960)
        clip = (tt < 2008.5) | (tt > 2010.5)
        l_top = VGroup(top.line(tt[tt < 2008.6], vv[tt < 2008.6], C.MULTIPLE, 3), top.line(tt[tt > 2010.4], vv[tt > 2010.4], C.MULTIPLE, 3))
        assert clip.sum() > 700
        l_bot = bot.line(tt2, vv2, C.MULTIPLE, 3)
        z1, z2 = top.hline(0, GREY_B, 1.5), bot.hline(0, GREY_B, 1.5)
        n1 = label(r"trailing earnings yield $-$ 10-year Treasury yield (points)", font_size=22, color=C.MULTIPLE).next_to(
            top.c2p(1960, 6), UR, buff=0.05)
        n2 = label(r"CAPE earnings yield $-$ real bond yield (Shiller's ``excess CAPE yield'')", font_size=22,
                   color=C.MULTIPLE).next_to(bot.c2p(1960, 11), UR, buff=0.05)
        d_top = top.dot(2026.76, trail_now, YELLOW)
        d_bot = bot.dot(2026.76, ecy_now, YELLOW)
        lt = tagged(rf"now: ${trail_now:.1f}$, lowest since 2002\\(apart from the 2009 earnings collapse)", font_size=22,
                    color=YELLOW).move_to(top.c2p(2014.5, -3.1))
        lb = tagged(rf"now: ${ecy_now:.2f}$, lowest since 2002", font_size=22, color=YELLOW).move_to(bot.c2p(2015, -0.6))
        danger = VGroup(tagged(r"1987", font_size=22, color=C.RATE).next_to(top.c2p(1987.7, -4.4), RIGHT, buff=0.08),
                        tagged(r"2000", font_size=22, color=C.RATE).next_to(top.c2p(2000.0, -3.2), DOWN, buff=0.08))
        fwd_l = tagged(rf"forward version: $1/{NOTE['fwd_pe_cap']} - {y10:.2f}\% \approx {fwd:.1f}$ points: roughly even",
                       font_size=24).to_corner(DL, buff=0.2)
        src = source(r"Shiller data; FRED (DGS10); FactSet trailing P/E", font_size=18)
        with self.voiceover(
            "The Fed Model again: stocks' earnings yield minus the bond yield. Above zero, stocks pay more than bonds; "
            "below zero, less. <bookmark mark='f'/> Using forward earnings, the gap is roughly zero: about 5.1 percent "
            "against 5.3. <bookmark mark='t'/> Using the past year's earnings, it's about minus 1.4 points: the lowest since "
            "2002, setting aside 2009, when earnings briefly collapsed. <bookmark mark='d'/> The real danger zones were "
            "1987 and 2000. <bookmark mark='c'/> And the version Shiller computes, from CAPE and real yields, is down to "
            "about half a point, also its lowest since 2002."
        ) as vo:
            self.play(FadeIn(title), FadeIn(src))
            vo.wait_until("f")
            self.play(FadeIn(fwd_l))
            vo.wait_until("t")
            self.play(Create(top), Create(z1), FadeIn(n1))
            self.play(Create(l_top), run_time=2)
            self.play(FadeIn(d_top), FadeIn(lt))
            vo.wait_until("d")
            self.play(FadeIn(danger))
            vo.wait_until("c")
            self.play(Create(bot), Create(z2), FadeIn(n2))
            self.play(Create(l_bot), run_time=2)
            self.play(FadeIn(d_bot), FadeIn(lb))

        with self.voiceover(
            "So, depending on which version you use, the market is either still fine, or getting close to the danger "
            "zone. One caution about the classic version: earnings tend to grow with inflation, so an earnings yield is "
            "closer to a real return, yet it gets compared with a bond yield that includes inflation. That's why the CAPE "
            "version, measured against real yields, is the more careful one. "
            "Either way, the direction is the same. Earnings are strong, but rates are squeezing what investors will pay "
            "for them."
        ) as vo:
            self.play(Indicate(VGroup(d_top, d_bot), color=YELLOW))
        self.clear_scene()
