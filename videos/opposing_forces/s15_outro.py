from __future__ import annotations

from explainer import *  # noqa: F403
from videos.opposing_forces.common import NOTE, label, last


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.watch()
        self.credits()

    # ------------------------------------------------------------------
    def recap(self):
        knot = Dot(ORIGIN, radius=0.22, color=C.PRICE)
        rope = Line(UP * 2.4, DOWN * 2.4, color=GREY_B, stroke_width=6)
        up = Arrow(UP * 0.9, UP * 3.3, buff=0, color=C.EARNINGS, stroke_width=14, max_tip_length_to_length_ratio=0.25)
        dn = Arrow(DOWN * 0.9, DOWN * 3.3, buff=0, color=C.RATE, stroke_width=14, max_tip_length_to_length_ratio=0.25)
        VGroup(rope, up, dn, knot).move_to(LEFT * 4.6)
        up_items = VGroup(label(r"the earnings boom", font_size=32, color=C.EARNINGS),
                          label(r"trailing earnings up about 30\%, Q3 heading for 30\%+", font_size=24),
                          label(r"record margins, record positive guidance", font_size=24),
                          label(r"but growth is near its peak, and peak growth gets a lower multiple", font_size=24,
                                color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        dn_items = VGroup(label(r"the rising cost of capital", font_size=32, color=C.RATE),
                          label(rf"10-year Treasury {last('dgs10_daily'):.2f}\%, real yield {last('real10_daily'):.2f}\%",
                                font_size=24),
                          label(r"four forces: debt service, fewer price-blind buyers,", font_size=24),
                          label(r"AI's demand for capital, mortgage convexity", font_size=24),
                          label(r"and a Fed with one blunt instrument", font_size=24, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        mid = VGroup(MathTex(r"P", r"=", r"E", r"\times", r"\frac{\text{payout}}{r - g}", font_size=44),
                     label(r"price: sideways, while most stocks fall", font_size=26, color=C.PRICE)).arrange(DOWN, buff=0.15)
        mid[0][0].set_color(C.PRICE)
        mid[0][2].set_color(C.EARNINGS)
        mid[0][4].set_color(C.MULTIPLE)
        up_items.move_to(RIGHT * 1.4 + UP * 2.1)
        dn_items.move_to(RIGHT * 1.4 + DOWN * 2.2)
        mid.move_to(RIGHT * 1.0 + DOWN * 0.05)
        with self.voiceover(
            "Let's put the whole argument back together. <bookmark mark='p'/> The price of the market is earnings times "
            "a multiple, and the multiple depends on interest rates, through r minus g. <bookmark mark='u'/> Pulling up: "
            "an earnings boom, with growth around thirty percent, record margins, and companies still beating "
            "estimates, although growth this fast is usually close to its peak. <bookmark mark='d'/> Pulling down: a "
            "rising cost of capital, driven by the cost of the government's debt, fewer price-blind buyers, AI's hunger "
            "for capital, and convexity hedging in the mortgage market, with a Fed that has one blunt instrument for all "
            "of it. <bookmark mark='m'/> The result: an index going sideways, and a stealth correction underneath."
        ) as vo:
            self.play(Create(rope), FadeIn(knot))
            vo.wait_until("p")
            self.play(FadeIn(mid[0]))
            vo.wait_until("u")
            self.play(GrowArrow(up), FadeIn(up_items, shift=DOWN * 0.15))
            vo.wait_until("d")
            self.play(GrowArrow(dn), FadeIn(dn_items, shift=UP * 0.15))
            vo.wait_until("m")
            self.play(FadeIn(mid[1]))
            self.play(knot.animate.shift(UP * 0.12), rate_func=there_and_back, run_time=0.7)
        self.clear_scene()

    # ------------------------------------------------------------------
    def watch(self):
        title = label(r"What would break the stalemate", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(
            label(r"the 10-year yield: if the pressure from rates eases, indexes could re-accelerate", font_size=28,
                  color=C.RATE),
            label(r"Q3 earnings season, starting mid-October: does the boom keep beating?", font_size=28, color=C.EARNINGS),
            label(r"breadth: does the average stock recover, or does the correction spread?", font_size=28,
                  color=C.EQUAL_WEIGHT),
            label(r"the calendar: the seasonally weak stretch ends in mid-October", font_size=28, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(DOWN * 0.1)
        with self.voiceover(
            "So what would break the stalemate? <bookmark mark='a'/> First, rates: if the pressure from the bond market "
            "eases, Timmer thinks the indexes could easily pick up speed again. <bookmark mark='b'/> Second, the earnings "
            "season starting in mid-October: whether the boom keeps beating expectations. <bookmark mark='c'/> Third, "
            "breadth: whether the average stock recovers, or the stealth correction spreads to the giants. <bookmark "
            "mark='d'/> And the calendar, as the seasonally weak stretch comes to an end."
        ) as vo:
            self.play(FadeIn(title))
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(items[i], shift=RIGHT * 0.2), run_time=0.7)
        self.clear_scene()

    # ------------------------------------------------------------------
    def credits(self):
        assert NOTE["sideways_months"] == 4
        lines = VGroup(
            label(r"Based on ``Opposing Forces,'' Jurrien Timmer's weekly note,", font_size=28),
            label(r"week of October 5, 2026 (Fidelity Investments)", font_size=28),
            label(r"views are the author's own, as of that date", font_size=24, color=GREY_A),
            label(r"Data: FRED (St.\ Louis Fed), New York Fed (ACM term premium),", font_size=26),
            label(r"Robert Shiller, U.S.\ Treasury, FactSet Earnings Insight, Nasdaq", font_size=26),
            label(r"Educational explanation only. Not investment advice.", font_size=28, color=YELLOW),
        ).arrange(DOWN, buff=0.25).move_to(UP * 0.3)
        with self.voiceover(
            "This video explained one strategist's view, as of early October 2026, and checked it against public data. "
            "It isn't investment advice. Thanks for watching."
        ) as vo:
            self.play(FadeIn(lines, lag_ratio=0.15), run_time=2)
        self.wait(2.0)
        self.play(FadeOut(lines))
