from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.opposing_forces.common import NOTE, TimeChart, label, show_chapter_card, source, tagged, ts, window

FRANCE, GERMANY = BLUE_B, GREY_A  # local to this chapter


class RversusG(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 8, r"Is the economy running hot?")
        self.growth()
        self.r_minus_g()
        self.france()
        self.verdict()

    # ------------------------------------------------------------------
    def growth(self):
        tq, q = ts("real_gdp_growth")
        tp, p = ts("potential_growth")
        tq, q = window(tq, q, 2022)
        tp, p = window(tp, p, 2022, 2028.9)
        assert q.min() > 0 and q.max() < 5
        assert 2.0 < q[-1] < 2.4 and 2.1 < p[np.searchsorted(tp, 2026.5)] < 2.3
        ch = TimeChart((2022, 2029), (0, 5), width=10.0, height=4.6, x_ticks=range(2022, 2030),
                       y_ticks=[0, 1, 2, 3, 4, 5], y_fmt=lambda y: rf"{y:g}\%").move_to(DOWN * 0.4 + LEFT * 0.6)
        zero = VMobject()
        yl = ch.y_title(r"real GDP growth, year over year", color=C.GROWTH)
        l_q = ch.line(tq, q, C.GROWTH, 4)
        l_p = DashedVMobject(ch.line(tp, p, WHITE, 3), num_dashes=60)
        t_p = tagged(r"potential growth (CBO)", font_size=24).next_to(ch.c2p(2027.5, p[-1]), DOWN, buff=0.15)
        survey = Rectangle(width=ch.c2p(2029, 0)[0] - ch.c2p(2026, 0)[0], height=ch.c2p(0, 2.2)[1] - ch.c2p(0, 2.1)[1] + 0.06,
                           stroke_width=0, fill_color=YELLOW, fill_opacity=0.7)
        survey.move_to((ch.c2p(2026, 2.15) + ch.c2p(2029, 2.15)) / 2)
        t_s = tagged(r"economists' forecasts for 2026--28:\\$2.1$--$2.2\%$ (Bloomberg survey, per Timmer)", font_size=24,
                     color=YELLOW).next_to(survey, UP, buff=0.9).shift(LEFT * 0.6)
        t_q = tagged(rf"Q2 2026: {q[-1]:.1f}\%", font_size=26, color=C.GROWTH).next_to(ch.c2p(tq[-1], q[-1]), DOWN, buff=0.4)
        t_q.shift(LEFT * 0.8)
        src = source(r"FRED (GDPC1, GDPPOT)")
        with self.voiceover(
            "There's a more comforting explanation for rising real yields, and Timmer takes it seriously: maybe the "
            "economy is simply running hot, so money is in demand for good reasons. <bookmark mark='a'/> But apart from "
            "strong surveys of purchasing managers, he doesn't see it in the data. <bookmark mark='g'/> Real growth over "
            "the past year: about 2.2 percent. <bookmark mark='p'/> The Congressional Budget Office's estimate of the "
            "economy's long-run potential: also about 2.2. <bookmark mark='s'/> And economists surveyed by Bloomberg "
            "expect 2.1 to 2.2 percent a year through 2028. Decent. Not booming."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ch), Create(zero), FadeIn(yl), FadeIn(src))
            vo.wait_until("g")
            self.play(Create(l_q), run_time=2)
            self.play(FadeIn(t_q))
            vo.wait_until("p")
            self.play(Create(l_p), FadeIn(t_p))
            vo.wait_until("s")
            self.play(FadeIn(survey), FadeIn(t_s))
        self.clear_scene()

    # ------------------------------------------------------------------
    def r_minus_g(self):
        tr, r = ts("real10_monthly")
        tp, p = ts("potential_growth")
        tp, p = window(tp, p, 2003, 2026.8)
        gi = np.interp(tr, tp, p)
        gap = r - gi
        assert gap[-1] > 0.5 and not ((gap > 0) & (tr > 2010.5) & (tr < 2026)).any()
        r_now = ts("real10_daily")[1][-1]
        assert abs(r_now - NOTE["real_ten_year"]) < 0.06
        ch = TimeChart((2003, 2026.9), (-1.5, 3.5), width=10.4, height=4.6, x_ticks=range(2004, 2028, 4),
                       y_ticks=[-1, 0, 1, 2, 3], y_fmt=lambda y: rf"{y:g}\%").move_to(DOWN * 0.45)
        eq = MathTex(r"b' - b", r"\;\approx\;", r"(", r"r", r"-", r"g", r")\,b", r"\;+\;", r"\text{primary deficit}",
                     font_size=40).to_edge(UP, buff=0.3)
        eq[3].set_color(C.REAL_RATE)
        eq[5].set_color(C.GROWTH)
        l_r = ch.line(tr, r, C.REAL_RATE, 4)
        l_g = ch.line(tp, p, C.GROWTH, 4)
        t_r = tagged(r"$r$: 10-year real yield", font_size=26, color=C.REAL_RATE).move_to(ch.c2p(2012.5, -1.15))
        t_g = tagged(r"$g$: potential growth", font_size=26, color=C.GROWTH).move_to(ch.c2p(2013, 2.45))
        span = ch.span(2010.9, 2025.9, C.GROWTH, 0.07)
        t_span = tagged(r"$r < g$ for 15 years", font_size=26, color=C.GROWTH).move_to(ch.c2p(2018.5, 3.15))
        now = tagged(rf"now: $r = {r_now:.2f}\%$, $g \approx {gi[-1]:.1f}\%$", font_size=26).move_to(ch.c2p(2023.6, 0.55))
        src = source(r"FRED (DFII10, GDPPOT)")
        with self.voiceover(
            "Remember r minus g, from the debt arithmetic? <bookmark mark='m'/> Let's measure it: the real yield on "
            "ten-year Treasuries, against the economy's potential growth rate. <bookmark mark='s'/> From about 2011 to "
            "2025, r sat below g, often far below. That's the world where government debt quietly shrinks relative to the "
            "economy. <bookmark mark='n'/> Now r is about 2.9 percent, and g is about 2.2. For the first time since 2010, "
            "the real cost of borrowing for ten years is above the economy's growth rate."
        ) as vo:
            self.play(Write(eq))
            vo.wait_until("m")
            self.play(Create(ch), FadeIn(src))
            self.play(Create(l_g), FadeIn(t_g), Create(l_r), FadeIn(t_r), run_time=2.5)
            vo.wait_until("s")
            self.play(FadeIn(span), FadeIn(t_span))
            vo.wait_until("n")
            self.play(FadeIn(now), Indicate(VGroup(eq[3], eq[4], eq[5]), color=YELLOW))

        caveat = tagged(r"the government still pays a lower average rate on its old debt,\\"
                        r"but each new dollar now costs more, after inflation, than the economy grows", font_size=26,
                        color=GREY_A).to_corner(DL, buff=0.2)
        with self.voiceover(
            "The government still pays a lower average rate on its older debt, so this isn't an emergency today. But "
            "every new dollar it borrows now costs more, after inflation, than the economy is expected to grow. Timmer "
            "calls that a warning sign for both the budget and for growth."
        ) as vo:
            self.play(FadeIn(caveat, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def france(self):
        tf, f = ts("france10")
        td, d = ts("germany10")
        assert abs(f[-1] - 4.0) < 0.01 and (f[(tf > 2008.75) & (tf < 2026)] < f[-1]).all()
        ch = TimeChart((2006, 2026.8), (-1.0, 5.0), width=10.4, height=4.6, x_ticks=range(2006, 2028, 4),
                       y_ticks=[-1, 0, 1, 2, 3, 4, 5], y_fmt=lambda y: rf"{y:g}\%").move_to(DOWN * 0.4)
        yl = ch.y_title(r"10-year government bond yields", color=GREY_A)
        tf2, f2 = window(tf, f, 2006)
        td2, d2 = window(td, d, 2006)
        l_f, l_d = ch.line(tf2, f2, FRANCE, 4), ch.line(td2, d2, GERMANY, 3)
        t_f = tagged(r"France", font_size=28, color=FRANCE).next_to(ch.c2p(2023.3, 4.3), UP, buff=0.1)
        t_d = tagged(r"Germany", font_size=28, color=GERMANY).move_to(ch.c2p(2024.6, 1.6))
        gap = d[-1]
        note = tagged(rf"France: {f[-1]:.1f}\%, highest since 2008\\{f[-1] - gap:.1f} points above Germany", font_size=26,
                      color=FRANCE).move_to(ch.c2p(2014.5, 4.3))
        src = source(r"FRED / OECD (IRLTLT01FRM156N, IRLTLT01DEM156N)")
        with self.voiceover(
            "If fiscal risk is the story, you'd expect bond markets to punish weak government balance sheets most. "
            "Timmer's exhibit A is France. <bookmark mark='a'/> French ten-year yields are around four percent, the highest "
            "since 2008, <bookmark mark='b'/> and France now pays about eight-tenths of a point more than Germany to "
            "borrow for ten years, a gap that was usually far narrower over the past decade. The same rising rates hurt anyone with a weak "
            "balance sheet: indebted governments, lower-quality companies, and most consumers."
        ) as vo:
            self.play(Create(ch), FadeIn(yl), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(l_d), Create(l_f), FadeIn(t_f), FadeIn(t_d), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.clear_scene()

    # ------------------------------------------------------------------
    def verdict(self):
        core = label(r"fiscal risk", font_size=54, color=C.DEBT)
        amp = VGroup(label(r"amplified by", font_size=30, color=GREY_A),
                     label(r"AI crowding out", font_size=36, color=C.EARNINGS),
                     label(r"convexity hedging", font_size=36, color=C.MORTGAGE)).arrange(DOWN, buff=0.25)
        g = VGroup(core, amp).arrange(DOWN, buff=0.6).move_to(UP * 0.4)
        arrow = Arrow(g.get_bottom() + DOWN * 0.1, g.get_bottom() + DOWN * 1.1, buff=0, color=C.REAL_RATE, stroke_width=8)
        out = label(r"higher real yields", font_size=34, color=C.REAL_RATE).next_to(arrow, DOWN, buff=0.15)
        with self.voiceover(
            "So Timmer's verdict: the main reason real yields are rising is not a booming economy. <bookmark mark='f'/> "
            "It's fiscal risk, <bookmark mark='a'/> amplified by AI's appetite for capital and by convexity hedging in the "
            "mortgage market. That's a less comfortable reason for rates to rise, because it doesn't come with faster "
            "growth to pay for it."
        ) as vo:
            vo.wait_until("f")
            self.play(FadeIn(core, scale=1.1))
            vo.wait_until("a")
            self.play(FadeIn(amp, shift=UP * 0.2))
            self.play(GrowArrow(arrow), FadeIn(out))
        self.clear_scene()
