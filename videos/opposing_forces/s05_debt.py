from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.opposing_forces.common import (
    NOTE, TimeChart, data, label, show_chapter_card, source, tagged, ts, window,
)


class Debt(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 4, r"Force 1: the cost of the debt")
        self.level()
        self.cost()
        self.rollover()
        self.loop()
        self.dynamics()

    # ------------------------------------------------------------------
    def level(self):
        t, v = ts("debt_quarterly")
        pen = data()["debt_penny"]
        pre, now = pen["pre_covid"], pen["last"]
        assert now > NOTE["debt_trillions"] and now - pre > NOTE["debt_since_covid"] and pen["last_date"] == "2026-10-05"
        ch = TimeChart((2000, 2027), (0, 45), width=9.4, height=4.8, x_ticks=range(2000, 2030, 5),
                       y_ticks=[0, 10, 20, 30, 40], y_fmt=lambda y: rf"\${y:g}\text{{T}}").move_to(DOWN * 0.35 + LEFT * 0.8)
        yl = ch.y_title(r"U.S. federal debt, trillions of dollars", color=C.DEBT)
        line = ch.line(np.append(t, 2026.76), np.append(v, now), C.DEBT, 5)
        area = ch.area(np.append(t, 2026.76), np.append(v, now), C.DEBT, 0.15)
        d0 = ch.dot(2019.997, pre, WHITE)
        d1 = ch.dot(2026.76, now, WHITE)
        l0 = tagged(rf"end of 2019: \${pre:.1f}T", font_size=26).next_to(d0, LEFT, buff=0.15).shift(UP * 0.25)
        l1 = tagged(rf"Oct 5, 2026: \${now:.1f}T", font_size=26).next_to(d1, LEFT, buff=0.15).shift(UP * 0.2)
        brace = BraceBetweenPoints(ch.c2p(2026.95, pre), ch.c2p(2026.95, now), RIGHT, color=C.DEBT)
        bl = label(rf"$+\${now - pre:.0f}$T\\since COVID", font_size=28, color=C.DEBT).next_to(brace, RIGHT, buff=0.1)
        src = source(r"FRED (GFDEBTN); U.S. Treasury, Debt to the Penny")
        with self.voiceover(
            "Force number one: the government's debt. <bookmark mark='a'/> In August, total federal debt passed 40 "
            "trillion dollars. <bookmark mark='b'/> At the end of 2019 it was 23 trillion, <bookmark mark='c'/> so it has grown "
            "by about 17 trillion dollars since COVID."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ch), FadeIn(yl), FadeIn(src))
            self.play(Create(line), FadeIn(area), run_time=2.5)
            self.play(FadeIn(d1), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(d0), FadeIn(l0))
            vo.wait_until("c")
            self.play(GrowFromCenter(brace), FadeIn(bl))
        self.clear_scene()

    # ------------------------------------------------------------------
    def cost(self):
        t, v = ts("interest_pct_gdp")
        k = int(np.argmax(np.where(t > 2024, v, 0)))
        low = int(np.argmin(np.where((t >= 2021) & (t < 2022), v, 9)))
        prior = t[(v >= v[k]) & (t < 2024)][-1]
        assert abs(v[k] - NOTE["debt_service_gdp"]) < 0.1 and 1997 < prior < 1999 and 2.2 < v[low] < 2.5
        ch = TimeChart((1960, 2027), (0, 5.5), width=10.6, height=4.6, x_ticks=range(1960, 2030, 10),
                       y_ticks=[0, 1, 2, 3, 4, 5], y_fmt=lambda y: rf"{y:g}\%").move_to(DOWN * 0.4)
        yl = ch.y_title(r"federal interest payments, \% of GDP", color=C.DEBT)
        line = ch.line(t, v, C.DEBT, 4)
        lo = tagged(rf"{int(t[low])}: {v[low]:.1f}\%", font_size=26, color=C.DEBT).next_to(ch.c2p(t[low], v[low]), DOWN, buff=0.15)
        hi = tagged(rf"late 2025: {v[k]:.1f}\%\\highest since 1998", font_size=26, color=C.DEBT)
        hi.next_to(ch.c2p(t[k], v[k]), UP, buff=0.2).shift(LEFT * 1.0)
        src = source(r"FRED (A091RC1Q027SBEA, GDP)")
        with self.voiceover(
            "But Timmer's point is that the size of the debt is old news. <bookmark mark='a'/> What's new is the cost of "
            "carrying it. <bookmark mark='b'/> Here's what the government pays in interest each year, as a share of the "
            "whole economy. In 2021, with rates near zero, it was about two and a third percent. <bookmark mark='c'/> Now "
            "it's about four percent, the highest since the late 1990s. Interest is now one of the biggest items in the "
            "federal budget."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ch), FadeIn(yl), FadeIn(src))
            vo.wait_until("b")
            self.play(Create(line), run_time=2.5, rate_func=linear)
            self.play(FadeIn(lo))
            vo.wait_until("c")
            self.play(FadeIn(hi))
        self.clear_scene()

    # ------------------------------------------------------------------
    def rollover(self):
        # A schematic: the debt as a stack of bonds that mature and get refinanced at today's rate.
        old = [1.5, 1.2, 2.1, 0.9, 1.6, 2.4, 1.1, 1.8, 2.0, 1.3]
        new = 5.0
        cells = VGroup()
        for r in old:
            c = Rectangle(width=2.6, height=0.42, stroke_color=BACKGROUND, stroke_width=2,
                          fill_color=interpolate_color(ManimColor(C.EARNINGS), ManimColor(C.RATE), r / 5.5), fill_opacity=0.85)
            c.add(MathTex(rf"{r:.1f}\%", font_size=26).move_to(c))
            cells.add(c)
        cells.arrange(DOWN, buff=0.04).move_to(LEFT * 4.2 + DOWN * 0.2)
        head = label(r"the debt, as a stack of bonds", font_size=28, color=GREY_A).next_to(cells, UP, buff=0.25)
        avg = ValueTracker(float(np.mean(old)))
        avg_l = always_redraw(lambda: MathTex(rf"\text{{average rate}} = {avg.get_value():.2f}\%", font_size=36,
                                              color=C.DEBT).move_to(RIGHT * 2.7 + UP * 1.9))
        mkt = MathTex(r"\text{new bonds pay today's rate} \approx 5\%", font_size=34, color=C.RATE).move_to(RIGHT * 2.7 + UP * 1.0)
        sch = label(r"(schematic)", font_size=24, color=GREY_B).next_to(cells, DOWN, buff=0.2)
        with self.voiceover(
            "Why does the cost keep climbing even when rates stop rising? <bookmark mark='a'/> Picture the debt as a "
            "stack of bonds, each locked in at the rate that applied when it was sold. Many were sold when rates were "
            "near zero. <bookmark mark='b'/> But bonds mature, and the government has to borrow again to repay them, at "
            "today's rate."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in cells], lag_ratio=0.08), FadeIn(sch))
            self.play(FadeIn(avg_l))
            vo.wait_until("b")
            self.play(FadeIn(mkt))

        with self.voiceover(
            "So one by one, <bookmark mark='r'/> cheap old bonds get replaced by expensive new ones, and the average rate "
            "on the whole stack drifts up toward the market rate. That takes years, which means the interest bill keeps "
            "growing long after market rates stop rising."
        ) as vo:
            vo.wait_until("r")
            for i in range(len(old)):
                top = cells[0]
                fresh = Rectangle(width=2.6, height=0.42, stroke_color=BACKGROUND, stroke_width=2,
                                  fill_color=interpolate_color(ManimColor(C.EARNINGS), ManimColor(C.RATE), new / 5.5),
                                  fill_opacity=0.85)
                fresh.add(MathTex(rf"{new:.1f}\%", font_size=26).move_to(fresh))
                fresh.move_to(cells[-1])
                rates = old[i + 1:] + [new] * (i + 1)
                self.play(FadeOut(top, shift=UP * 0.4 + LEFT * 0.6), cells[1:].animate.shift(UP * 0.46),
                          FadeIn(fresh, shift=UP * 0.2), avg.animate.set_value(float(np.mean(rates))),
                          run_time=0.45 if i > 1 else 0.8)
                cells.remove(top)
                cells.add(fresh)
        self.clear_scene()

        t, v = ts("avg_rate_on_debt")
        t2, v2 = ts("dgs10_monthly")
        t2, v2 = window(t2, v2, 2000)
        ch = TimeChart((2000, 2027), (0, 7), width=10.4, height=4.8, x_ticks=range(2000, 2030, 5),
                       y_ticks=[0, 1, 2, 3, 4, 5, 6, 7], y_fmt=lambda y: rf"{y:g}\%").move_to(DOWN * 0.35)
        l_avg = ch.line(t, v, C.DEBT, 5)
        l_mkt = ch.line(t2, v2, C.RATE, 3).set_stroke(opacity=0.8)
        k_lo = int(np.argmin(v))
        assert 2020 < t[k_lo] < 2021.5 and 1.8 < v[k_lo] < 2.0 and 3.1 < v[-1] < 3.4
        tag_a = tagged(rf"average rate the government pays: {v[k_lo]:.1f}\% $\to$ {v[-1]:.1f}\%", font_size=26,
                       color=C.DEBT).move_to(ch.c2p(2007.5, 0.5))
        tag_m = tagged(r"10-year market yield", font_size=26, color=C.RATE).next_to(ch.c2p(2026.5, v2[-1]), UP, buff=0.15)
        tag_m.shift(LEFT * 1.4)
        src = source(r"FRED (A091RC1Q027SBEA, GFDEBTN, DGS10)")
        with self.voiceover(
            "Here's the real thing. <bookmark mark='a'/> The average rate the government pays on its debt bottomed at "
            "under two percent in 2020. It's now above three. <bookmark mark='m'/> And the market rate for new ten-year "
            "borrowing is above five. The gap between the two lines is cost that hasn't arrived yet."
        ) as vo:
            self.play(Create(ch), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(l_avg), run_time=2)
            self.play(FadeIn(tag_a))
            vo.wait_until("m")
            self.play(Create(l_mkt), FadeIn(tag_m), run_time=2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def loop(self):
        t, v = ts("deficit_pct_gdp")
        assert -6.5 < v[-1] < -5.5 and t[-1] >= 2025
        nodes = [r"higher rates", r"bigger interest bill", r"bigger deficits", r"more bonds to sell"]
        cols = [C.RATE, C.DEBT, C.DEBT, C.DEBT]
        pos = [UP * 2.0, RIGHT * 3.6, DOWN * 2.0, LEFT * 3.6]
        boxes = VGroup()
        for n, c, p in zip(nodes, cols, pos):
            b = label(n, font_size=34, color=c)
            b.add_background_rectangle(color=BACKGROUND, opacity=1, buff=0.12)
            boxes.add(b.move_to(p + DOWN * 0.2))
        arcs = VGroup()
        for i in range(4):
            a, b = boxes[i], boxes[(i + 1) % 4]
            arcs.add(CurvedArrow(a.get_center() + (b.get_center() - a.get_center()) * 0.28,
                                 b.get_center() - (b.get_center() - a.get_center()) * 0.28, angle=-PI / 4, color=GREY_B,
                                 stroke_width=4))
        defl = tagged(rf"deficit: about {abs(v[-1]):.0f}\% of GDP (fiscal 2025),\\with no recession", font_size=26,
                      color=C.DEBT).to_corner(DR, buff=0.5).shift(UP * 0.35)
        with self.voiceover(
            "And this can feed on itself. <bookmark mark='a'/> Higher rates <bookmark mark='b'/> mean a bigger interest "
            "bill. <bookmark mark='c'/> A bigger interest bill means bigger deficits, <bookmark mark='d'/> which means "
            "more bonds to sell, <bookmark mark='e'/> and selling more bonds pushes rates higher still. <bookmark "
            "mark='f'/> With the deficit already around six percent of GDP in an economy that isn't in recession, bond "
            "investors notice."
        ) as vo:
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                anims = [FadeIn(boxes[i], scale=0.9)]
                if i:
                    anims.append(Create(arcs[i - 1]))
                self.play(*anims, run_time=0.7)
            vo.wait_until("e")
            self.play(Create(arcs[3]))
            self.play(Indicate(boxes[0], color=C.RATE))
            vo.wait_until("f")
            self.play(FadeIn(defl), FadeIn(source(r"FRED (FYFSGDA188S)")))
        self.clear_scene()

    # ------------------------------------------------------------------
    def dynamics(self):
        steps = VGroup(
            MathTex(r"b", r"=", r"\frac{\text{debt}}{\text{GDP}}", font_size=46),
            MathTex(r"\text{next year:}\quad", r"b' = b\,\frac{1+r}{1+g} + \text{primary deficit}", font_size=44),
            MathTex(r"b' - b", r"\;\approx\;", r"(", r"r", r"-", r"g", r")\,b", r"\;+\;", r"\text{primary deficit}",
                    font_size=50),
        ).arrange(DOWN, buff=0.6).move_to(UP * 0.5)
        steps[0][0].set_color(C.DEBT)
        steps[2][3].set_color(C.REAL_RATE)
        steps[2][5].set_color(C.GROWTH)
        legend = VGroup(label(r"$r$: interest rate on the debt", font_size=28, color=C.REAL_RATE),
                        label(r"$g$: growth rate of the economy", font_size=28, color=C.GROWTH),
                        label(r"primary deficit: borrowing for everything except interest", font_size=26, color=GREY_A),
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UL, buff=0.4)
        box = SurroundingRectangle(steps[2][2:7], color=YELLOW, buff=0.1)
        cases = VGroup(label(r"$r < g$: the debt melts, relative to the economy, on its own", font_size=30, color=C.GROWTH),
                       label(r"$r > g$: it snowballs, even with a balanced budget", font_size=30, color=C.REAL_RATE)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "There's a simple piece of arithmetic that tells you when debt becomes a problem. <bookmark mark='a'/> What "
            "matters isn't the debt itself, but the debt compared with the size of the economy that has to carry it. "
            "<bookmark mark='b'/> Each year, the debt grows with the interest rate r, plus any new borrowing beyond the "
            "interest, while the economy grows at its own rate, g. <bookmark mark='c'/> Work through the division, and the change in the debt "
            "ratio comes out as r minus g, times the debt, plus the deficit before interest."
        ) as vo:
            self.play(FadeIn(legend))
            vo.wait_until("a")
            self.play(Write(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1], shift=DOWN * 0.2))
            vo.wait_until("c")
            self.play(TransformMatchingShapes(steps[1][1].copy(), steps[2]))

        with self.voiceover(
            "Everything hinges on that first term. <bookmark mark='y'/> When the interest rate is below the growth rate, "
            "debt shrinks relative to the economy all by itself. <bookmark mark='z'/> When it's above, the debt snowballs, "
            "even if the rest of the budget balances. Hold on to r minus g: in a few minutes we'll measure it."
        ) as vo:
            self.play(Create(box))
            vo.wait_until("y")
            self.play(FadeIn(cases[0], shift=UP * 0.2))
            vo.wait_until("z")
            self.play(FadeIn(cases[1], shift=UP * 0.2))
        self.clear_scene()
