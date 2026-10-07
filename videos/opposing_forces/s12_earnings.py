from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.opposing_forces.common import (
    FACTSET, NOTE, TimeChart, label, shiller, show_chapter_card, source, tagged, window, yoy,
)

# FactSet "Earnings Insight": year-over-year S&P 500 EPS growth, late in each reporting season
# (blended actual + estimates), and the estimate at the start of the quarter where we have it.
QUARTERS = [  # label, growth %, actual?, estimate at start of quarter, report date
    ("Q3 '25", 13.4, True, 7.9, "Nov 21, 2025"),
    ("Q4 '25", 13.2, True, None, "Feb 13, 2026"),
    ("Q1 '26", 27.7, True, 13.0, "May 15, 2026"),
    ("Q2 '26", 52.0, True, 23.1, "Aug 28, 2026"),
    ("Q3 '26", FACTSET["q3_growth"], False, FACTSET["q3_growth_june30"], "Oct 2, 2026"),
    ("Q4 '26", FACTSET["q4_growth"], False, None, "Oct 2, 2026"),
    ("Q1 '27", FACTSET["q1_2027_growth"], False, None, "Oct 2, 2026"),
    ("Q2 '27", FACTSET["q2_2027_growth"], False, None, "Oct 2, 2026"),
]


class EarningsBoom(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 11, r"The other side of the rope: earnings")
        self.quarters()
        self.waves()
        self.derivatives()
        self.peak_multiple()
        self.world()

    # ------------------------------------------------------------------
    def quarters(self):
        base_y, scale, w = -2.6, 0.085, 0.95
        bars, tops, names, starts = VGroup(), VGroup(), VGroup(), VGroup()
        for i, (name, g, actual, start, _) in enumerate(QUARTERS):
            x = -5.4 + i * 1.45
            b = Rectangle(width=w, height=max(0.03, g * scale), stroke_color=C.EARNINGS, stroke_width=2.5,
                          fill_color=C.EARNINGS, fill_opacity=0.85 if actual else 0.15)
            b.move_to([x, base_y, 0], aligned_edge=DOWN)
            bars.add(b)
            tops.add(MathTex(rf"{g:.1f}\%", font_size=28).next_to(b, UP, buff=0.1))
            names.add(Tex(name, font_size=26, color=GREY_A).move_to([x, base_y - 0.32, 0]))
            if start is not None:
                y = base_y + start * scale
                tick = VGroup(DashedLine([x - w / 2 - 0.1, y, 0], [x + w / 2 + 0.1, y, 0], color=YELLOW, stroke_width=3,
                                         dash_length=0.06))
                starts.add(tick)
        axis = Line([-6.1, base_y, 0], [6.3, base_y, 0], color=GREY_B, stroke_width=2)
        title = label(r"S\&P 500 earnings growth, year over year, by quarter", font_size=32).to_edge(UP, buff=0.4)
        legend = VGroup(VGroup(Square(0.25, fill_color=C.EARNINGS, fill_opacity=0.85, stroke_width=0),
                               label(r"reported", font_size=24)).arrange(RIGHT, buff=0.15),
                        VGroup(Square(0.25, fill_color=C.EARNINGS, fill_opacity=0.15, stroke_color=C.EARNINGS, stroke_width=2),
                               label(r"analysts' estimates (Oct 2)", font_size=24)).arrange(RIGHT, buff=0.15),
                        VGroup(DashedLine(ORIGIN, RIGHT * 0.4, color=YELLOW, stroke_width=3, dash_length=0.06),
                               label(r"estimate when the quarter began", font_size=24, color=YELLOW)).arrange(RIGHT, buff=0.15),
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.4).shift(DOWN * 0.7)
        src = source(r"FactSet Earnings Insight, Nov 2025 to Oct 2026")
        with self.voiceover(
            "Now the other side of the rope. <bookmark mark='a'/> Here's S&P 500 earnings growth, quarter by quarter, "
            "compared with a year earlier. Last year, a healthy thirteen percent. <bookmark mark='b'/> Then it took off: "
            "about 28 percent in the first quarter of 2026, <bookmark mark='c'/> and 52 percent in the second, the fastest "
            "since 2021."
        ) as vo:
            self.play(FadeIn(title), Create(axis), FadeIn(names), FadeIn(src))
            vo.wait_until("a")
            self.play(*[GrowFromEdge(bars[i], DOWN) for i in (0, 1)], FadeIn(tops[0]), FadeIn(tops[1]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[2], DOWN), FadeIn(tops[2]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[3], DOWN), FadeIn(tops[3]))

        lo, hi = NOTE["q3_growth"]
        band = Rectangle(width=w + 0.3, height=(hi - lo) * scale, stroke_width=0, fill_color=YELLOW, fill_opacity=0.35)
        band.move_to([bars[4].get_x(), base_y + (lo + hi) / 2 * scale, 0])
        band_l = tagged(r"Timmer: Q3 could\\come in at 30--35\%", font_size=24, color=YELLOW).next_to(band, RIGHT, buff=0.15)
        band_l.shift(UP * 0.9)
        with self.voiceover(
            "And notice how companies keep beating expectations. <bookmark mark='s'/> The dashed lines show what analysts "
            "expected when each quarter began: about thirteen percent for the first quarter, which came in at 28; 23 "
            "percent for the second, which came in at 52. <bookmark mark='e'/> For the third quarter, the one about to be "
            "reported, analysts now expect about 30 percent. <bookmark mark='t'/> If the usual earnings-season bounce of "
            "recent quarters happens again, Timmer figures it could come in at 30 to 35 percent."
        ) as vo:
            vo.wait_until("s")
            self.play(FadeIn(legend), Create(starts))
            vo.wait_until("e")
            self.play(*[GrowFromEdge(bars[i], DOWN) for i in range(4, 8)], *[FadeIn(tops[i]) for i in range(4, 8)])
            vo.wait_until("t")
            self.play(FadeIn(band), FadeIn(band_l))

        rec = VGroup(label(rf"record profit margin: {FACTSET['margin_q2']:.1f}\% in Q2 (FactSet; Timmer: {NOTE['margin']}\%)",
                           font_size=26, color=C.EARNINGS),
                     label(rf"record {FACTSET['positive_guidance']} companies raised Q3 guidance (prior record: "
                           rf"{FACTSET['positive_guidance_prior_record']})", font_size=26, color=C.EARNINGS),
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rec.add_background_rectangle(color=BACKGROUND, opacity=0.9, buff=0.12)
        rec.move_to(RIGHT * 3.6 + UP * 0.75)
        assert FACTSET["positive_guidance"] > FACTSET["positive_guidance_prior_record"]
        with self.voiceover(
            "Profit margins are at a record, and a record number of companies raised their guidance going into the "
            "quarter. <bookmark mark='q'/> Timmer's line: who wants to step in front of a train like that? Then again, "
            "<bookmark mark='w'/> look at the estimates further out. Growth is expected to fade, to near zero by the "
            "middle of next year, partly because the comparisons get so tough."
        ) as vo:
            self.play(FadeIn(rec))
            vo.wait_until("q")
            self.play(Indicate(VGroup(bars[2], bars[3]), color=YELLOW))
            vo.wait_until("w")
            self.play(Indicate(VGroup(bars[6], bars[7]), color=YELLOW))
        self.clear_scene()

    # ------------------------------------------------------------------
    def waves(self):
        s = shiller()
        t, E = s["t"], s["E"]
        g = yoy(t, E)
        t, g = window(t, g, 2011.5)
        ok = np.isfinite(g)
        t, g = t[ok], g[ok]
        assert abs(g[-1] - 32.7) < 0.5
        lo, hi = -40, 60
        ch = TimeChart((2011.5, 2026.9), (lo, hi), width=10.4, height=4.7, x_ticks=range(2012, 2028, 2),
                       y_ticks=[-40, -20, 0, 20, 40, 60], y_fmt=lambda y: rf"{y:g}\%").move_to(DOWN * 0.4)
        zero = ch.hline(0, GREY_B, 1.5)
        yl = ch.y_title(r"trailing 12-month earnings, growth over a year earlier", color=C.EARNINGS)
        line = ch.line(t, np.clip(g, lo, hi), C.EARNINGS, 4)
        off = tagged(r"2021: off the chart\\(rebound from 2020)", font_size=22, color=GREY_A).next_to(ch.c2p(2021.7, hi), DOWN, buff=0.1)
        off.shift(RIGHT * 1.7)
        peaks = [float(t[(t >= a) & (t <= b)][np.argmax(g[(t >= a) & (t <= b)])])
                 for a, b in ((2013.0, 2015.5), (2017.5, 2019.5), (2020.5, 2022.5), (2025.0, 2026.6))]
        assert np.allclose(np.diff(peaks), 4.0, atol=1.0), peaks
        marks = VGroup(*[ch.vline(p, YELLOW, 2) for p in peaks])
        pk_l = tagged(r"crests roughly every four years", font_size=26, color=YELLOW).move_to(ch.c2p(2015.8, 48))
        src = source(r"Shiller monthly data: S\&P 500 trailing reported earnings")
        with self.voiceover(
            "Zoom out, and earnings growth comes in waves. <bookmark mark='a'/> Here's the growth of trailing twelve-month "
            "earnings since 2012. <bookmark mark='p'/> Timmer sees a roughly four-year rhythm in these waves: crests "
            "around 2014, 2018, 2021, and now. Right now, all the waves he tracks are still rising, and all are in double "
            "digits."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ch), Create(zero), FadeIn(yl), FadeIn(src))
            self.play(Create(line), run_time=3, rate_func=linear)
            self.play(FadeIn(off))
            vo.wait_until("p")
            self.play(Create(marks), FadeIn(pk_l))
        self.clear_scene()

    # ------------------------------------------------------------------
    def derivatives(self):
        ax1 = Axes(x_range=[0, 4 * PI, PI], y_range=[-1.3, 1.3, 1], x_length=10.5, y_length=2.4, tips=False,
                   axis_config={"color": GREY_B, "include_ticks": False}).move_to(UP * 1.5)
        ax2 = Axes(x_range=[0, 4 * PI, PI], y_range=[-1.3, 1.3, 1], x_length=10.5, y_length=2.4, tips=False,
                   axis_config={"color": GREY_B, "include_ticks": False}).move_to(DOWN * 1.8)
        g = ax1.plot(np.sin, color=C.EARNINGS, stroke_width=5)
        a = ax2.plot(np.cos, color=YELLOW, stroke_width=5)
        l1 = label(r"earnings growth (how fast earnings rise)", font_size=28, color=C.EARNINGS).next_to(ax1, UP, buff=0.1)
        l1.align_to(ax1, LEFT)
        l2 = label(r"its rate of change: the ``second derivative'' of earnings", font_size=28, color=YELLOW).next_to(ax2, UP, buff=0.1)
        l2.align_to(ax2, LEFT)
        x = ValueTracker(0.0)
        d1 = always_redraw(lambda: Dot(ax1.c2p(x.get_value(), np.sin(x.get_value())), radius=0.1, color=WHITE))
        d2 = always_redraw(lambda: Dot(ax2.c2p(x.get_value(), np.cos(x.get_value())), radius=0.1, color=WHITE))
        vl = always_redraw(lambda: DashedLine(ax1.c2p(x.get_value(), 1.3), ax2.c2p(x.get_value(), -1.3), color=GREY_D,
                                              stroke_width=2))
        p_acc = VGroup(Dot(ax2.c2p(2 * PI, 1), color=YELLOW, radius=0.11),
                       tagged(r"peak acceleration", font_size=24, color=YELLOW).next_to(ax2.c2p(2 * PI, 1), RIGHT, buff=0.2))
        p_g = VGroup(Dot(ax1.c2p(2.5 * PI, 1), color=C.EARNINGS, radius=0.11),
                     tagged(r"peak growth", font_size=24, color=C.EARNINGS).next_to(ax1.c2p(2.5 * PI, 1), UP, buff=0.12))
        lag = tagged(r"a quarter-cycle later: about a year,\\if the cycle is four years", font_size=24).next_to(
            ax1.c2p(2.5 * PI, 1), RIGHT, buff=0.3).shift(UP * 0.25)
        sch = label(r"(schematic)", font_size=22, color=GREY_B).to_corner(DR, buff=0.25)
        with self.voiceover(
            "To see where a wave is heading, Timmer looks at its derivatives, exactly as in calculus. <bookmark mark='a'/> "
            "If earnings growth swings up and down like a wave, <bookmark mark='b'/> then its rate of change, how fast "
            "growth itself is speeding up, is another wave, shifted earlier by a quarter of a cycle. <bookmark mark='c'/> "
            "The acceleration peaks first. <bookmark mark='d'/> Growth keeps rising for a while after that, but at a "
            "slowing pace, and then it crests."
        ) as vo:
            self.play(FadeIn(sch))
            vo.wait_until("a")
            self.play(Create(ax1), FadeIn(l1), Create(g), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(ax2), FadeIn(l2), Create(a), run_time=1.5)
            self.add(vl, d1, d2)
            vo.wait_until("c")
            self.play(x.animate.set_value(2 * PI), run_time=2.5)
            self.play(FadeIn(p_acc))
            vo.wait_until("d")
            self.play(x.animate.set_value(2.5 * PI), run_time=1.5)
            self.play(FadeIn(p_g), FadeIn(lag))

        with self.voiceover(
            "Timmer says a peak in that second derivative is due. In other words: earnings are still growing fast, and "
            "will probably keep growing, but the acceleration is about to turn, and with it, the market's sense that "
            "things can only get better."
        ) as vo:
            self.play(Indicate(p_acc, color=YELLOW))
        for m in (d1, d2, vl):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def peak_multiple(self):
        s = shiller()
        t, E, PE = s["t"], s["E"], s["PE"]
        g, dpe = yoy(t, E), yoy(t, PE)
        m = np.isfinite(g) & np.isfinite(dpe) & (t >= 1960)
        edges = [-np.inf, -10, 0, 10, 20, 30, np.inf]
        names = [r"below $-10\%$", r"$-10$ to $0\%$", r"0 to $10\%$", r"10 to $20\%$", r"20 to $30\%$", r"above $30\%$"]
        med = np.array([np.median(dpe[m & (g >= a) & (g < b)]) for a, b in zip(edges, edges[1:])])
        cnt = [int((m & (g >= a) & (g < b)).sum()) for a, b in zip(edges, edges[1:])]
        assert (np.diff(med) < 0).all() and med[-1] < -20 and med[0] > 30 and min(cnt) > 50
        base_y, scale = 0.0, 0.055
        bars, vals, labs = VGroup(), VGroup(), VGroup()
        for i, v in enumerate(med):
            x = -4.9 + i * 1.95
            col = C.MULTIPLE
            b = Rectangle(width=1.2, height=abs(v) * scale, stroke_width=0, fill_color=col,
                          fill_opacity=0.85 if v < 0 else 0.45)
            b.move_to([x, base_y, 0], aligned_edge=DOWN if v >= 0 else UP)
            bars.add(b)
            vals.add(MathTex(rf"{v:+.0f}\%", font_size=30).next_to(b, UP if v >= 0 else DOWN, buff=0.1))
            labs.add(Tex(names[i], font_size=24, color=C.EARNINGS).move_to([x, base_y + (-0.3 if v >= 0 else 0.3), 0]))
        axis = Line([-6.0, base_y, 0], [6.2, base_y, 0], color=GREY_B, stroke_width=2)
        title = VGroup(label(r"when earnings grew this much over a year\ldots", font_size=30, color=C.EARNINGS),
                       label(r"\ldots the P/E typically changed this much (median, S\&P 500, 1960--2026)", font_size=30,
                             color=C.MULTIPLE)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.35)
        src = source(r"Shiller monthly data: trailing reported earnings and P/E")
        with self.voiceover(
            "Here's why that matters for the multiple. <bookmark mark='a'/> Take every month since 1960, sort them by how "
            "fast earnings grew over the previous year, and look at what happened to the P/E over the same year. "
            "<bookmark mark='b'/> When earnings were shrinking, the multiple usually expanded. <bookmark mark='c'/> When "
            "earnings grew more than thirty percent, the P/E typically fell by about a quarter. <bookmark mark='q'/> As "
            "Timmer puts it, investors don't usually pay top multiples for peak earnings growth."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(title), Create(axis), FadeIn(labs), FadeIn(src))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(bars[i], DOWN) for i in (0, 1)], FadeIn(vals[0]), FadeIn(vals[1]))
            self.play(GrowFromEdge(bars[2], DOWN), FadeIn(vals[2]))
            vo.wait_until("c")
            self.play(*[GrowFromEdge(bars[i], UP) for i in (3, 4, 5)], *[FadeIn(vals[i]) for i in (3, 4, 5)])
            vo.wait_until("q")
            self.play(Indicate(VGroup(bars[5], vals[5]), color=YELLOW))

        why = label(r"partly mechanical: prices look ahead, so they rise before the earnings arrive,\\"
                    r"and the multiple shrinks as earnings catch up", font_size=26, color=GREY_A)
        why.add_background_rectangle(color=BACKGROUND, opacity=0.9, buff=0.1)
        why.to_edge(DOWN, buff=0.55)
        assert NOTE["trailing_pe_change"] == -10
        with self.voiceover(
            "Part of this is mechanical: stock prices look ahead, so they tend to rise before the earnings show up, and "
            "the multiple shrinks as earnings catch up. Either way, with trailing earnings up around thirty percent and "
            "the next twelve months expected to add another twenty, a falling multiple is what history would predict. "
            "Timmer's trailing P/E is down about ten percent from a year ago."
        ) as vo:
            self.play(FadeIn(why))
        self.clear_scene()

    # ------------------------------------------------------------------
    def world(self):
        title = label(r"Around the world (from Timmer's charts)", font_size=36).to_edge(UP, buff=0.5)
        items = VGroup(
            label(r"five-year growth rates of earnings and of payouts\\look to be peaking, in the U.S.\ and globally",
                  font_size=28),
            label(r"Japan and Canada stand out as the winners", font_size=28, color=C.EARNINGS),
            label(rf"U.S.\ payouts (dividends and buybacks) growing about {NOTE['us_payout_cagr']}\% a year:\\"
                  r"``hardly compelling''", font_size=28, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.2)
        with self.voiceover(
            "Timmer sees the same pattern abroad. <bookmark mark='a'/> Five-year growth rates of earnings, and of what "
            "companies pay out to shareholders, look to be peaking, in the U.S. and globally. <bookmark mark='b'/> Japan "
            "and Canada stand out as the winners. <bookmark mark='c'/> U.S. payouts are growing about ten percent a "
            "year, which he calls hardly compelling by comparison."
        ) as vo:
            self.play(FadeIn(title))
            for i, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(items[i], shift=RIGHT * 0.2))
        self.clear_scene()
