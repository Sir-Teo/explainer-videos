from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.opposing_forces.common import (
    NOTE, TimeChart, at, label, show_chapter_card, source, tagged, ts, window, ym,
)


def bond_price(coupon, y, years=10):
    t = np.arange(1, years + 1)
    return float(np.sum(coupon / (1 + y) ** t) + 100 / (1 + y) ** years)


class BondMarket(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 3, r"Slowly, then all at once")
        self.seesaw()
        self.history()
        self.triangle()
        self.real_vs_inflation()
        self.term_premium()
        self.four_forces()

    # ------------------------------------------------------------------
    def seesaw(self):
        p5 = bond_price(4, 0.05)
        assert abs(p5 - 92.3) < 0.1
        bond = VGroup(RoundedRectangle(width=4.4, height=2.2, corner_radius=0.15, stroke_color=GREY_A, stroke_width=2,
                                       fill_color=GREY_E, fill_opacity=0.4),
                      VGroup(label(r"10-year bond", font_size=32),
                             label(r"pays \$4 a year per \$100", font_size=28, color=GREY_A),
                             label(r"then \$100 back at the end", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.12))
        bond[1].move_to(bond[0])
        bond.move_to(LEFT * 3.6 + UP * 0.9)
        y4 = MathTex(r"\text{new bonds yield } 4\%", r"\;\Rightarrow\;", r"\text{price} = \$100", font_size=36)
        y5 = MathTex(r"\text{new bonds yield } 5\%", r"\;\Rightarrow\;", rf"\text{{price}} \approx \${p5:.0f}", font_size=36)
        for m in (y4, y5):
            m[0].set_color(C.RATE)
            m.move_to(RIGHT * 2.6 + UP * 1.4)
        y5.shift(DOWN * 1.1)
        rule = tagged(r"yields up $\Longleftrightarrow$ bond prices down", font_size=36, color=YELLOW).move_to(DOWN * 1.9)
        with self.voiceover(
            "First, a quick refresher on bonds, because everything that follows runs through them. <bookmark mark='b'/> "
            "A ten-year Treasury bond pays a fixed amount of interest every year, then returns your money. <bookmark "
            "mark='f'/> If new bonds pay four percent, this one is worth its full hundred dollars. <bookmark mark='g'/> "
            "But if new bonds start paying five percent, nobody will pay a hundred dollars for one paying four. Its price "
            "falls, to about 92, until it yields five percent too. <bookmark mark='r'/> So when yields rise, bond prices "
            "fall. A rising-yield market is a falling bond market."
        ) as vo:
            vo.wait_until("b")
            self.play(FadeIn(bond, shift=UP * 0.2))
            vo.wait_until("f")
            self.play(FadeIn(y4))
            vo.wait_until("g")
            self.play(FadeIn(y5, shift=DOWN * 0.2))
            vo.wait_until("r")
            self.play(FadeIn(rule, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        t, v = ts("dgs10_monthly")
        k_hi, k_lo = int(np.argmax(v)), int(np.argmin(v))
        assert 1981 < t[k_hi] < 1982 and 2020 < t[k_lo] < 2021 and v[k_hi] > 15 and v[k_lo] < 0.7
        ch = TimeChart((1962, 2027), (0, 16), width=11.2, height=4.9, x_ticks=range(1965, 2030, 10),
                       y_ticks=[0, 4, 8, 12, 16], y_fmt=lambda y: rf"{y:g}\%").move_to(DOWN * 0.3)
        line = ch.line(t, v, C.RATE, 4)
        yl = ch.y_title(r"10-year Treasury yield (monthly average)", color=C.RATE)
        hi = tagged(rf"1981: {v[k_hi]:.1f}\%", font_size=26, color=C.RATE).next_to(ch.c2p(t[k_hi], v[k_hi]), RIGHT, buff=0.15)
        lo = tagged(rf"2020 low: {v[k_lo]:.1f}\%", font_size=26, color=C.RATE).move_to(ch.c2p(2009.0, 0.9))
        bull = ch.span(t[k_hi], t[k_lo], C.EARNINGS, 0.08)
        bull_l = tagged(r"a 40-year bond bull market", font_size=28, color=C.EARNINGS).move_to(ch.c2p(2001, 12.5))
        bear = ch.span(t[k_lo], 2027, C.RATE, 0.15)
        src = source(r"FRED (DGS10)")
        with self.voiceover(
            "Now zoom out. <bookmark mark='a'/> This is the ten-year Treasury yield since the 1960s. <bookmark mark='h'/> "
            "It peaked above fifteen percent in 1981, <bookmark mark='b'/> then fell for four decades, a forty-year bull "
            "market in bonds, <bookmark mark='l'/> bottoming out in 2020 at well under one percent. <bookmark mark='t'/> "
            "Since then it has turned. Timmer describes rates as being in a secular bear market: not a blip, but a "
            "regime that can last for years."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ch), FadeIn(yl), FadeIn(src))
            self.play(Create(line), run_time=3, rate_func=linear)
            vo.wait_until("h")
            self.play(FadeIn(hi))
            vo.wait_until("b")
            self.play(FadeIn(bull), FadeIn(bull_l))
            vo.wait_until("l")
            self.play(FadeIn(lo))
            vo.wait_until("t")
            self.play(FadeIn(bear))
        self.clear_scene()

    # ------------------------------------------------------------------
    def triangle(self):
        t, v = ts("dgs10_weekly")
        t, v = window(t, v, 2022.75)
        assert v.min() > 3.0
        ch = TimeChart((2022.75, 2026.85), (3.0, 5.6), width=11.0, height=4.9,
                       x_ticks=[2023, 2024, 2025, 2026], y_ticks=[3.0, 3.5, 4.0, 4.5, 5.0, 5.5],
                       y_fmt=lambda y: rf"{y:.1f}\%").move_to(DOWN * 0.35)
        yl = ch.y_title(r"10-year Treasury yield (weekly)", color=C.RATE)
        before = window(t, v, -np.inf, ym(2026, 7, 20))
        after = window(t, v, ym(2026, 7, 13))
        l1, l2 = ch.line(*before, C.RATE, 4), ch.line(*after, C.RATE, 5)
        # Trend lines through the actual pivots: lower highs and higher lows.
        highs = [(ym(2023, 10, 22), at(t, v, ym(2023, 10, 22))), (ym(2025, 1, 12), at(t, v, ym(2025, 1, 12)))]
        lows = [(ym(2024, 9, 15), at(t, v, ym(2024, 9, 15))), (ym(2026, 3, 1), at(t, v, ym(2026, 3, 1)))]
        assert highs[1][1] < highs[0][1] and lows[1][1] > lows[0][1]

        def through(p, q, t_end):
            s = (q[1] - p[1]) / (q[0] - p[0])
            return Line(ch.c2p(p[0], p[1]), ch.c2p(t_end, p[1] + s * (t_end - p[0])), color=YELLOW, stroke_width=3)

        upper, lower = through(*highs, 2026.85), through(*lows, 2026.85)
        dots = VGroup(*[ch.dot(a, b, YELLOW, 0.08) for a, b in highs + lows])
        s_hi = (highs[1][1] - highs[0][1]) / (highs[1][0] - highs[0][0])
        line_jul = highs[0][1] + s_hi * (ym(2026, 7, 26) - highs[0][0])
        assert at(t, v, ym(2026, 7, 26)) > line_jul > at(t, v, ym(2026, 5, 31))
        tri_l = tagged(r"lower highs, higher lows:\\a triangle", font_size=26, color=YELLOW).move_to(ch.c2p(2025.6, 3.3))
        y_now = v[-1]
        assert abs(y_now - NOTE["ten_year"]) < 0.06
        brk = tagged(rf"breakout: ${y_now:.2f}\%$", font_size=28, color=C.RATE).next_to(ch.c2p(t[-1], y_now), LEFT, buff=0.2)
        quote = tagged(r"``Slowly, then all at once''", font_size=32, color=GREY_A).move_to(ch.c2p(2024.6, 5.45))
        src = source(r"FRED (DGS10)")
        with self.voiceover(
            "Zoom in on the last few years. <bookmark mark='a'/> After the surge of 2022 and 2023, the yield spent almost "
            "three years going back and forth. <bookmark mark='p'/> Each high was a little lower than the last, and each "
            "low a little higher: a pattern chart-watchers call a triangle, a market coiling up, undecided."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ch), FadeIn(yl), FadeIn(src))
            self.play(Create(l1), run_time=3, rate_func=linear)
            vo.wait_until("p")
            self.play(FadeIn(dots), Create(upper), Create(lower), FadeIn(tri_l))

        with self.voiceover(
            "Timmer's rule of thumb, technical analysis 101, is that a triangle usually breaks in the direction of the "
            "trend that came before it, and that trend was up. <bookmark mark='b'/> This summer, as the triangle "
            "narrowed, the yield broke out, upward. <bookmark mark='c'/> By early October it was 5.3 percent. Timmer "
            "borrows a line adapted from Hemingway, about how people go bankrupt: <bookmark mark='q'/> slowly, then all at once."
        ) as vo:
            vo.wait_until("b")
            self.play(Create(l2), run_time=2, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(brk))
            vo.wait_until("q")
            self.play(FadeIn(quote))
        self.clear_scene()

    # ------------------------------------------------------------------
    def real_vs_inflation(self):
        series = [("dgs10_weekly", C.RATE, r"nominal 10-year yield"), ("real10_weekly", C.REAL_RATE, r"real yield (TIPS)"),
                  ("breakeven10_weekly", C.INFLATION, r"expected inflation (breakeven)")]
        ch = TimeChart((2019, 2026.85), (-1.5, 6.0), width=10.2, height=4.9, x_ticks=range(2019, 2027),
                       y_ticks=[-1, 0, 1, 2, 3, 4, 5, 6], y_fmt=lambda y: rf"{y:g}\%").move_to(DOWN * 0.3 + LEFT * 0.9)
        eq = MathTex(r"\text{nominal}", r"=", r"\text{real}", r"+", r"\text{expected inflation}", font_size=40)
        eq[0].set_color(C.RATE)
        eq[2].set_color(C.REAL_RATE)
        eq[4].set_color(C.INFLATION)
        eq.to_edge(UP, buff=0.35)
        lines, tags = VGroup(), VGroup()
        for key, col, name in series:
            t, v = ts(key)
            lines.add(ch.line(t, v, col, 4))
            tags.add(tagged(name, font_size=24, color=col))
        tags[0].next_to(ch.c2p(2026.85, 5.31), UP, buff=0.12).shift(LEFT * 1.2)
        tags[1].move_to(ch.c2p(2021.3, -0.25))
        tags[2].move_to(ch.c2p(2024.4, 3.05))
        k0, k1 = ym(2025, 10, 1), ym(2026, 10, 5)
        vals = []
        for key in ("dgs10_daily", "real10_daily", "breakeven10_daily"):
            t, v = ts(key)
            vals.append((at(t, v, k0), at(t, v, k1)))
        dn, dr, db = (b - a for a, b in vals)
        assert abs(dn - 1.19) < 0.03 and abs(dr - 1.18) < 0.03 and abs(db) < 0.05
        table = VGroup(
            label(r"Oct 2025 $\to$ Oct 2026", font_size=28, color=GREY_A),
            label(rf"nominal: ${vals[0][0]:.2f} \to {vals[0][1]:.2f}$ \;(${dn:+.2f}$)", font_size=28, color=C.RATE),
            label(rf"real: ${vals[1][0]:.2f} \to {vals[1][1]:.2f}$ \;(${dr:+.2f}$)", font_size=28, color=C.REAL_RATE),
            label(rf"inflation: ${vals[2][0]:.2f} \to {vals[2][1]:.2f}$ \;(${db:+.2f}$)", font_size=28, color=C.INFLATION),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        table.add_background_rectangle(color=BACKGROUND, opacity=0.9, buff=0.15)
        table.move_to(ch.c2p(2020.75, 4.75))
        src = source(r"FRED (DGS10, DFII10, T10YIE)")
        with self.voiceover(
            "What kind of rise is this? A bond's yield has two parts. <bookmark mark='e'/> The nominal yield is a real "
            "yield, what you earn after inflation, plus the inflation investors expect along the way. And the Treasury "
            "sells inflation-protected bonds, so we can measure both. <bookmark mark='l'/> Here they are."
        ) as vo:
            vo.wait_until("e")
            self.play(Write(eq))
            vo.wait_until("l")
            self.play(Create(ch), FadeIn(src))
            for ln, tg in zip(lines, tags):
                self.play(Create(ln), FadeIn(tg), run_time=1.2)

        with self.voiceover(
            "Over the past year, <bookmark mark='t'/> the ten-year yield rose by about 1.2 percentage points. The real "
            "yield rose by 1.2 points. Expected inflation: essentially unchanged. <bookmark mark='m'/> So this is not "
            "an inflation scare. It's the real price of money that's going up."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(table, shift=LEFT * 0.2))
            vo.wait_until("m")
            self.play(Indicate(table[2], color=C.REAL_RATE), Indicate(lines[1], color=C.REAL_RATE))
        self.clear_scene()

    # ------------------------------------------------------------------
    def term_premium(self):
        t, v = ts("term_premium_monthly")
        t, v = window(t, v, 1990)
        assert abs(100 * v[-1] - NOTE["term_premium_bp"]) < 1
        prior = t[(v >= v[-1]) & (t < 2026)][-1]
        assert 2014 < prior < 2015
        eq = MathTex(r"\text{10-year yield}", r"=", r"\text{expected path of short-term rates}", r"+", r"\text{term premium}",
                     font_size=38).to_edge(UP, buff=0.35)
        eq[0].set_color(C.RATE)
        eq[2].set_color(C.POLICY)
        eq[4].set_color(C.TERM_PREMIUM)
        expl = VGroup(label(r"lend for 10 years at once", font_size=28, color=C.RATE),
                      label(r"or roll over 3-month bills 40 times?", font_size=28, color=C.POLICY),
                      label(r"the extra pay for locking up money is the term premium", font_size=28, color=C.TERM_PREMIUM),
                      ).arrange(DOWN, buff=0.15).move_to(UP * 1.2)
        ch = TimeChart((1990, 2026.85), (-1.6, 3.2), width=10.6, height=3.9, x_ticks=range(1990, 2030, 5),
                       y_ticks=[-1, 0, 1, 2, 3], y_fmt=lambda y: rf"{y:g}\%").move_to(DOWN * 0.95)
        zero = ch.hline(0, GREY_B)
        line = ch.line(t, v, C.TERM_PREMIUM, 4)
        k_lo = int(np.argmin(np.where(t > 2019, v, 9)))
        lo = tagged(rf"2020: ${v[k_lo]:.2f}\%$", font_size=24, color=C.TERM_PREMIUM).next_to(ch.c2p(t[k_lo], v[k_lo]), LEFT, buff=0.2)
        hi = tagged(rf"Sept 2026: ${v[-1]:.2f}\%$\\highest since 2014", font_size=24, color=C.TERM_PREMIUM)
        hi.next_to(ch.c2p(t[-1], v[-1]), UP, buff=0.15).shift(LEFT * 0.8)
        src = source(r"New York Fed, ACM term premium model")
        with self.voiceover(
            "There's a second way to split the ten-year yield. <bookmark mark='e'/> Part of it is simply what investors "
            "expect short-term interest rates, which the Fed controls, to average over the next ten years. <bookmark "
            "mark='x'/> Because instead of lending for ten years, you could keep lending for three months at a time and "
            "roll it over. The rest is the term premium: the extra pay investors demand for locking their money up for "
            "ten years, and bearing whatever happens in between."
        ) as vo:
            vo.wait_until("e")
            self.play(Write(eq))
            vo.wait_until("x")
            self.play(LaggedStart(*[FadeIn(e, shift=UP * 0.15) for e in expl], lag_ratio=0.5), run_time=2.5)

        with self.voiceover(
            "The term premium can't be observed directly, but economists at the New York Fed estimate it with a model. "
            "<bookmark mark='c'/> For most of the 2010s it shrank, and in 2020 it was negative: investors were paying for "
            "the privilege of lending long. <bookmark mark='h'/> Now it's about 0.9 percent, the 89 basis points Timmer "
            "calls a cycle high, the highest since 2014. Lenders want to be paid for holding long-term government debt "
            "again."
        ) as vo:
            self.play(FadeOut(expl), FadeIn(src))
            vo.wait_until("c")
            self.play(Create(ch), Create(zero))
            self.play(Create(line), run_time=2.5, rate_func=linear)
            self.play(FadeIn(lo))
            vo.wait_until("h")
            self.play(FadeIn(hi))
        self.clear_scene()

    # ------------------------------------------------------------------
    def four_forces(self):
        title = label(r"Why are real yields and the term premium rising?", font_size=40).to_edge(UP, buff=0.5)
        names = [r"rising cost\\of the debt", r"no more\\price-blind buyers", r"AI's hunger\\for capital",
                 r"the mortgage\\market"]
        boxes = VGroup()
        for n in names:
            box = RoundedRectangle(width=2.9, height=1.8, corner_radius=0.15, stroke_color=C.RATE, stroke_width=2.5,
                                   fill_color=C.RATE, fill_opacity=0.12)
            boxes.add(VGroup(box, label(n, font_size=30).move_to(box)))
        boxes.arrange(RIGHT, buff=0.35).move_to(UP * 0.5)
        nums = VGroup(*[label(rf"{i + 1}", font_size=30, color=C.RATE).next_to(b, UP, buff=0.12) for i, b in enumerate(boxes)])
        arrow = Arrow(boxes.get_bottom() + DOWN * 0.3, boxes.get_bottom() + DOWN * 1.6, buff=0, color=C.RATE,
                      stroke_width=10)
        out = label(r"higher real yields", font_size=34, color=C.RATE).next_to(arrow, DOWN, buff=0.15)
        with self.voiceover(
            "So what's pushing real yields and the term premium up? Timmer names four forces, all at work at once: "
            "<bookmark mark='a'/> the rising cost of servicing the government's debt; <bookmark mark='b'/> too few "
            "buyers left who buy bonds regardless of price; <bookmark mark='c'/> what he calls reverse crowding out, from "
            "the AI investment boom; <bookmark mark='d'/> and, most recently, a jolt from the mortgage market. <bookmark "
            "mark='e'/> Let's take them one at a time."
        ) as vo:
            self.play(FadeIn(title))
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(boxes[i], shift=UP * 0.2), FadeIn(nums[i]), run_time=0.7)
            vo.wait_until("e")
            self.play(GrowArrow(arrow), FadeIn(out))
        self.clear_scene()
