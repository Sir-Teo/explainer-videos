from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.opposing_forces.common import (
    FACTSET, label, money, pe_equation, pe_plane, shiller, show_chapter_card, source, tagged, ym,
)


def idx(t, when):
    return int(np.argmin(np.abs(t - when)))


class PriceIdentity(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 1, r"Price $=$ earnings $\times$ multiple")
        self.s = shiller()
        self.numbers()
        self.rectangle()
        self.plane()

    # ------------------------------------------------------------------
    def numbers(self):
        s = self.s
        k = idx(s["t"], ym(2026, 6))
        E, P = s["E"][k], s["P"][k]
        assert 290 < E < 300 and 7300 < P < 7600
        self.k1 = k
        e_l = VGroup(label(r"earnings per share, past 12 months", font_size=30, color=C.EARNINGS),
                     MathTex(rf"E \approx \${E:.0f}", font_size=56, color=C.EARNINGS)).arrange(DOWN, buff=0.2)
        p_l = VGroup(label(r"price of the index", font_size=30, color=C.PRICE),
                     MathTex(rf"P \approx {money(P)}", font_size=56, color=C.PRICE)).arrange(DOWN, buff=0.2)
        VGroup(e_l, p_l).arrange(RIGHT, buff=2.0).move_to(UP * 1.6)
        ratio = MathTex(r"\frac{P}{E}", rf"= \frac{{{money(P)}}}{{{E:.0f}}} \approx {P / E:.1f}", font_size=54).move_to(DOWN * 0.6)
        ratio[0].set_color(C.MULTIPLE)
        meaning = label(rf"investors paid about \${P / E:.0f} for each \$1 of yearly profit", font_size=32, color=C.MULTIPLE)
        meaning.next_to(ratio, DOWN, buff=0.4)
        when = label(r"S\&P 500, June 2026", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        src = source(r"Robert Shiller's monthly S\&P 500 data (reported earnings)")

        with self.voiceover(
            "Let's start with the arithmetic hiding behind every stock-market chart. <bookmark mark='e'/> Add up the "
            "profits of all five hundred companies in the S&P 500 over the past year, per share of the index. That's its "
            "earnings, E: in June, about 295 dollars. <bookmark mark='p'/> The index itself traded around 7,450. That's "
            "the price, P."
        ) as vo:
            self.play(FadeIn(when), FadeIn(src))
            vo.wait_until("e")
            self.play(FadeIn(e_l, shift=UP * 0.2))
            vo.wait_until("p")
            self.play(FadeIn(p_l, shift=UP * 0.2))

        with self.voiceover(
            "Divide one by the other <bookmark mark='r'/> and you get the price-to-earnings ratio, the P/E, also called "
            "the multiple: about 25. <bookmark mark='m'/> Investors were paying about 25 dollars for every dollar of "
            "yearly profit."
        ) as vo:
            vo.wait_until("r")
            self.play(Write(ratio))
            vo.wait_until("m")
            self.play(FadeIn(meaning, shift=UP * 0.2))

        eq = pe_equation(84).move_to(UP * 0.2)
        under = VGroup(label(r"price", font_size=32, color=C.PRICE), label(r"earnings", font_size=32, color=C.EARNINGS),
                       label(r"multiple", font_size=32, color=C.MULTIPLE))
        for u, part in zip(under, (eq[0], eq[2], eq[4])):
            u.next_to(part, DOWN, buff=0.35)
        with self.voiceover(
            "Turn that around and you get an identity that is true by definition: <bookmark mark='a'/> price equals "
            "earnings times the multiple. Every move in the market is some combination of earnings changing and the "
            "multiple changing."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(VGroup(e_l, p_l, ratio, meaning)), Write(eq))
            self.play(LaggedStart(*[FadeIn(u, shift=UP * 0.15) for u in under], lag_ratio=0.25))
        self.clear_scene(extra=[], run_time=0.8)

    # ------------------------------------------------------------------
    def rectangle(self):
        s = self.s
        k0 = idx(s["t"], ym(2025, 6))
        k1 = self.k1
        Es, PEs = s["E"][k0:k1 + 1], s["PE"][k0:k1 + 1]
        e_g, pe_g = Es[-1] / Es[0], PEs[-1] / PEs[0]
        assert 1.30 < e_g < 1.35 and 0.91 < pe_g < 0.95
        corner = np.array([-6.0, -2.9, 0])
        wx, hy = 0.0165, 0.17  # scene units per dollar of earnings / per unit of P/E
        k = ValueTracker(0.0)

        def cur():
            x = k.get_value()
            return np.interp(x, np.arange(len(Es)), Es), np.interp(x, np.arange(len(PEs)), PEs)

        def build():
            E, PE = cur()
            r = Rectangle(width=E * wx, height=PE * hy, stroke_color=C.PRICE, stroke_width=3, fill_color=C.PRICE,
                          fill_opacity=0.25).move_to(corner, aligned_edge=DL)
            el = MathTex(rf"E = \${E:.0f}", font_size=36, color=C.EARNINGS).next_to(r, DOWN, buff=0.15)
            pl = MathTex(rf"P/E = {PE:.1f}", font_size=36, color=C.MULTIPLE).rotate(PI / 2).next_to(r, LEFT, buff=0.15)
            al = MathTex(rf"P = {money(E * PE)}", font_size=44, color=C.PRICE).move_to(r)
            bottom = Line(r.get_corner(DL), r.get_corner(DR), color=C.EARNINGS, stroke_width=7)
            side = Line(r.get_corner(DL), r.get_corner(UL), color=C.MULTIPLE, stroke_width=7)
            return VGroup(r, bottom, side, el, pl, al)

        rect = always_redraw(build)
        date = always_redraw(lambda: label(
            ["June 2025", "July 2025", "Aug 2025", "Sept 2025", "Oct 2025", "Nov 2025", "Dec 2025", "Jan 2026", "Feb 2026",
             "Mar 2026", "Apr 2026", "May 2026", "June 2026"][int(round(k.get_value()))], font_size=34,
            color=GREY_A).to_corner(UR, buff=0.5))
        title = label(r"price $=$ area of a rectangle", font_size=36).to_edge(UP, buff=0.4).shift(LEFT * 2.5)
        with self.voiceover(
            "Here's a way to picture it. <bookmark mark='a'/> Draw a rectangle whose width is earnings and whose height "
            "is the multiple. Its area is the price. <bookmark mark='b'/> Now let's watch the twelve months to June "
            "2026, month by month."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(title), FadeIn(rect))
            vo.wait_until("b")
            self.play(FadeIn(date))

        p_g = e_g * pe_g
        mult = MathTex(rf"\times {e_g:.2f}", r"\quad\times\quad", rf"{pe_g:.2f}", r"\quad=\quad", rf"\times {p_g:.2f}",
                       font_size=44).move_to(RIGHT * 3.4 + UP * 1.2)
        mult[0].set_color(C.EARNINGS)
        mult[2].set_color(C.MULTIPLE)
        mult[4].set_color(C.PRICE)
        words = VGroup(label(r"earnings", font_size=26, color=C.EARNINGS), label(r"multiple", font_size=26, color=C.MULTIPLE),
                       label(r"price", font_size=26, color=C.PRICE))
        for w, part in zip(words, (mult[0], mult[2], mult[4])):
            w.next_to(part, DOWN, buff=0.2)
        with self.voiceover(
            "Earnings surged: <bookmark mark='w'/> the rectangle got about a third wider. But it also got shorter: the "
            "multiple shrank. <bookmark mark='m'/> So the price grew by less than earnings: earnings times 1.33, multiple "
            "times 0.93, price times 1.24. A great year, but the multiple took back a chunk of the earnings gain."
        ) as vo:
            vo.wait_until("w")
            self.play(k.animate.set_value(len(Es) - 1), run_time=6, rate_func=linear)
            vo.wait_until("m")
            self.play(FadeIn(mult), FadeIn(words))
        rect.clear_updaters()
        date.clear_updaters()

        fs = FACTSET
        e2, pe2 = 1 + fs["fwd_eps_chg_q3"] / 100, fs["fwd_pe"] / fs["fwd_pe_june30"]
        assert abs(e2 * pe2 - (1 + fs["price_chg_q3"] / 100)) < 0.003
        mult2 = MathTex(rf"\times {e2:.3f}", r"\quad\times\quad", rf"{pe2:.3f}", r"\quad=\quad", r"\times 1.020",
                        font_size=44).move_to(RIGHT * 3.4 + DOWN * 1.0)
        for i, c in ((0, C.EARNINGS), (2, C.MULTIPLE), (4, C.PRICE)):
            mult2[i].set_color(c)
        cap2 = label(r"June 30 $\to$ Sept 30, 2026 (forward estimates)", font_size=28, color=GREY_A).next_to(mult2, UP, buff=0.3)
        quote = tagged(r"``Price is the residual of the E and the P/E.''", font_size=32, color=YELLOW).move_to(RIGHT * 3.4 + DOWN * 2.6)
        src = source(r"Shiller (trailing year); FactSet Earnings Insight, Oct 2, 2026 (forward)")
        with self.voiceover(
            "And the summer was more lopsided still. <bookmark mark='a'/> From the end of June to the end of September, "
            "analysts raised their estimates of the next twelve months' earnings by 9.3 percent. The forward P/E fell from "
            "20.4 to 19. <bookmark mark='p'/> The price rose just two percent. <bookmark mark='q'/> As Timmer puts it, price "
            "is just the residual of the E and the P/E."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cap2), FadeIn(mult2[:3]), FadeIn(src))
            vo.wait_until("p")
            self.play(FadeIn(mult2[3:]))
            vo.wait_until("q")
            self.play(FadeIn(quote, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def plane(self):
        pl = pe_plane()
        ch, E, PE = pl.ch, pl.E, pl.PE
        k_low, k_turn, k_end = pl.k
        assert 19.5 < PE[k_low] < 21 and 28 < PE[k_turn] < 29.5 and 1.12 < E[k_turn] / E[k_low] < 1.18
        assert 209 < E[k_turn] < 211 and 294 < E[k_end] < 297 and 24.7 < PE[k_end] < 25.7
        n1 = label(rf"2023--24: P/E ${PE[k_low]:.0f} \to {PE[k_turn]:.0f}$,\\earnings ${E[k_low]:.0f} \to {E[k_turn]:.0f}$",
                   font_size=24, color=C.MULTIPLE).move_to(RIGHT * 5.4 + UP * 1.7)
        n2 = label(rf"2025--26: earnings ${E[k_turn]:.0f} \to {E[k_end]:.0f}$,\\P/E ${PE[k_turn]:.0f} \to {PE[k_end]:.0f}$",
                   font_size=24, color=C.EARNINGS).move_to(RIGHT * 5.4 + UP * 0.35)
        src = source(r"Shiller monthly data; trailing reported earnings")

        with self.voiceover(
            "One more picture, which we'll come back to. Put earnings on one axis and the multiple on the other. "
            "<bookmark mark='c'/> Every point on one of these curves has the same price, because earnings times multiple "
            "is the same all along it. Higher curves mean higher prices."
        ) as vo:
            self.play(Create(ch), FadeIn(pl.xl), FadeIn(pl.yl), FadeIn(src))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(c) for c in pl.curves], lag_ratio=0.12), FadeIn(pl.clabels), FadeIn(pl.iso),
                      run_time=2.5)

        with self.voiceover(
            "Here's the real path of the S&P 500. <bookmark mark='a'/> From the bear-market low of October 2022 to the end "
            "of 2024, the dot mostly climbed. Earnings grew modestly, about 15 percent, but the multiple jumped from about "
            "20 to 29. <bookmark mark='n'/> That was a rally driven by the multiple. <bookmark mark='b'/> Since then, it's "
            "the reverse: earnings surged, from 210 dollars to 295, while the multiple fell back to about 25. Both legs "
            "carried the price higher, but with completely different engines."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(pl.dots[0]), FadeIn(pl.tags[0]))
            self.play(Create(pl.leg1), run_time=3, rate_func=linear)
            self.play(FadeIn(pl.dots[1]), FadeIn(pl.tags[1]))
            vo.wait_until("n")
            self.play(FadeIn(n1, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(Create(pl.leg2), run_time=3, rate_func=linear)
            self.play(FadeIn(pl.dots[2]), FadeIn(pl.tags[2]), FadeIn(n2, shift=LEFT * 0.2))

        P_end = E[k_end] * PE[k_end]
        es = np.linspace(E[k_end], E[k_end] * 1.06, 30)
        slide = Arrow(ch.c2p(es[0], P_end / es[0]), ch.c2p(es[-1], P_end / es[-1]), buff=0, color=YELLOW,
                      stroke_width=6, max_tip_length_to_length_ratio=0.35)
        slide_l = tagged(r"since June: sliding along\\a curve of constant price", font_size=26, color=YELLOW)
        slide_l.move_to(RIGHT * 5.4 + DOWN * 1.2)
        with self.voiceover(
            "And since June, the story has sharpened. Earnings estimates kept rising, but the price has gone mostly "
            "sideways for four months. <bookmark mark='s'/> On this map, the market is sliding along a curve of constant "
            "price: almost every step to the right is cancelled by a step down. Something is pulling the multiple down nearly as "
            "fast as earnings push it up. To see what, we need to understand where the multiple comes from."
        ) as vo:
            vo.wait_until("s")
            self.play(GrowArrow(slide), FadeIn(slide_l))
            self.play(Indicate(slide, color=YELLOW, scale_factor=1.1))
        self.clear_scene()
