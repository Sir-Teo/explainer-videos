from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.opposing_forces.common import (
    FACTSET, NOTE, TimeChart, at, data, index_at, label, source, tagged, ts, window, ym,
)


def money(v):
    return f"{v:,.0f}".replace(",", "{,}")


class Hook(VoiceoverScene):
    def construct(self):
        self.summer()
        self.beneath()
        self.tug_of_war()
        self.roadmap()

    # ------------------------------------------------------------------
    def summer(self):
        t, v = ts("sp500_daily")
        t, v = window(t, v, ym(2026, 1, 1))
        assert v.min() > 6200 and v.max() < 8400
        ch = TimeChart((2026.0, 2026.8), (6200, 8400), width=10.4, height=5.0,
                       x_ticks=[ym(2026, m) for m in (1, 3, 5, 7, 9)],
                       x_fmt=lambda x: ["Jan", "Mar", "May", "July", "Sept"][[ym(2026, m) for m in (1, 3, 5, 7, 9)].index(x)],
                       y_ticks=[6400, 6800, 7200, 7600, 8000, 8400], y_fmt=money).move_to(DOWN * 0.35 + LEFT * 0.3)
        title = label(r"S\&P 500 in 2026", font_size=34, color=C.PRICE).to_corner(UL, buff=0.45)
        price = ch.line(t, v, C.PRICE, 4)
        t0, t1 = ym(2026, 6, 1), ym(2026, 10, 2)
        p0, p1 = at(t, v, t0), at(t, v, t1)
        side = window(t, v, t0, t1)[1]
        assert abs(p1 / p0 - 1) < 0.02 and side.max() / side.min() < 1.08
        band = ch.span(t0, ym(2026, 10, 6), C.PRICE, 0.12)
        band_l = tagged(r"four months, going nowhere", font_size=28, color=C.PRICE).next_to(band, UP, buff=0.12)
        src = source(r"FRED (SP500); FactSet Earnings Insight, Oct 2, 2026")

        with self.voiceover(
            "Over the summer of 2026, Wall Street analysts raised their estimates of what S&P 500 companies will earn "
            "over the next twelve months by more than nine percent. <bookmark mark='p'/> The stock market's response? "
            "<bookmark mark='s'/> For four months, the index went essentially nowhere."
        ) as vo:
            self.play(FadeIn(title), Create(ch), FadeIn(src))
            vo.wait_until("p")
            self.play(Create(price), run_time=3, rate_func=linear)
            vo.wait_until("s")
            self.play(FadeIn(band), FadeIn(band_l, shift=DOWN * 0.15))

        tj, ts_ = ym(2026, 6, 30), ym(2026, 9, 30)
        pj, ps = at(t, v, tj), at(t, v, ts_)
        up = 1 + FACTSET["fwd_eps_chg_q3"] / 100
        held = DashedLine(ch.c2p(tj, pj), ch.c2p(ts_, pj * up), color=C.EARNINGS, stroke_width=5, dash_length=0.12)
        held_l = tagged(r"if investors had paid the same multiple:\\earnings estimates $+9.3\%$", font_size=26,
                        color=C.EARNINGS).move_to(ch.c2p(2026.5, 8250))
        gap = DoubleArrow(ch.c2p(ts_ + 0.012, pj * up), ch.c2p(ts_ + 0.012, ps), buff=0, color=C.MULTIPLE,
                          stroke_width=4, tip_length=0.18)
        gap_l = tagged(r"the multiple\\shrank", font_size=26, color=C.MULTIPLE).next_to(gap, RIGHT, buff=0.12)
        assert 8000 < pj * up < 8300 and 7600 < ps < 7700
        with self.voiceover(
            "If investors had kept paying the same price for each dollar of expected earnings, <bookmark mark='h'/> the "
            "index would have climbed along this line. <bookmark mark='g'/> Instead, the price they're willing to pay, "
            "the multiple, shrank, and ate up most of the earnings gain."
        ) as vo:
            vo.wait_until("h")
            self.play(FadeOut(band_l), Create(held), FadeIn(held_l))
            vo.wait_until("g")
            self.play(GrowFromCenter(gap), FadeIn(gap_l))
        self.clear_scene()

    # ------------------------------------------------------------------
    def beneath(self):
        b = data()["breadth"]
        flags = b["snapshot_above50"]
        share = 100 * sum(flags) / len(flags)
        assert b["snapshot_date"] == "2026-10-02" and abs(share - NOTE["above_50dma"]) < 1.5
        rng = np.random.default_rng(5)
        order = rng.permutation(len(flags))
        cells = VGroup()
        for i in range(len(flags)):
            on = flags[order[i]]
            cells.add(Square(0.21, stroke_width=0, fill_color=C.EQUAL_WEIGHT if on else GREY_D,
                             fill_opacity=0.95 if on else 0.55))
        cells.arrange_in_grid(20, 25, buff=0.05).move_to(LEFT * 2.6 + DOWN * 0.2)
        n_on = sum(flags)
        title = label(r"the 500 stocks of the S\&P 500, October 2, 2026", font_size=30).to_edge(UP, buff=0.45)
        key = VGroup(
            VGroup(Square(0.25, stroke_width=0, fill_color=C.EQUAL_WEIGHT, fill_opacity=0.95),
                   label(rf"above its 50-day average: {n_on}", font_size=28, color=C.EQUAL_WEIGHT)).arrange(RIGHT, buff=0.2),
            VGroup(Square(0.25, stroke_width=0, fill_color=GREY_D, fill_opacity=0.55),
                   label(rf"below it: {len(flags) - n_on}", font_size=28, color=GREY_A)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 4.3 + UP * 0.6)
        t, v = ts("sp500_daily")
        p_oct5 = at(t, v, ym(2026, 10, 5))
        prior = v[:index_at(t, ym(2026, 10, 5))].max()
        gap = 100 * (1 - p_oct5 / prior)
        assert 0 < gap < 0.5
        idx_l = label(rf"meanwhile, the index (Oct 5):\\within ${gap:.1f}\%$ of its record high", font_size=28, color=C.PRICE)
        idx_l.next_to(key, DOWN, buff=0.7).align_to(key, LEFT)
        src = source(r"Nasdaq daily closes of 500 members; FRED (SP500)")
        with self.voiceover(
            "And underneath that calm surface, something stranger was happening. <bookmark mark='g'/> Here are the "
            "stocks in the S&P 500. <bookmark mark='l'/> A stock is lit if its price is above its own average of the past "
            "fifty trading days, a simple sign that it has been rising lately. <bookmark mark='n'/> In early October, only "
            "about one in four were lit, <bookmark mark='i'/> even though the index itself sat within a fraction of a "
            "percent of its record high. The average stock was falling, while the giants at the top held the index up."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("g")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.002, run_time=2))
            vo.wait_until("l")
            self.play(FadeIn(key[0]), FadeIn(src))
            vo.wait_until("n")
            self.play(FadeIn(key[1]))
            self.play(Indicate(key[0], color=C.EQUAL_WEIGHT))
            vo.wait_until("i")
            self.play(FadeIn(idx_l, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def tug_of_war(self):
        knot = Dot(ORIGIN + DOWN * 0.1, radius=0.22, color=C.PRICE)
        rope = Line(UP * 2.6, DOWN * 2.6, color=GREY_B, stroke_width=6)
        up = Arrow(UP * 1.0, UP * 3.4, buff=0, color=C.EARNINGS, stroke_width=14, max_tip_length_to_length_ratio=0.25)
        dn = Arrow(DOWN * 1.2, DOWN * 3.6, buff=0, color=C.RATE, stroke_width=14, max_tip_length_to_length_ratio=0.25)
        up_l = label(r"an earnings boom", font_size=38, color=C.EARNINGS).next_to(up, RIGHT, buff=0.3).shift(DOWN * 0.3)
        dn_l = label(r"a rising cost of capital", font_size=38, color=C.RATE).next_to(dn, RIGHT, buff=0.3).shift(UP * 0.3)
        knot_l = label(r"price", font_size=34, color=C.PRICE).next_to(knot, LEFT, buff=0.3)
        note = VGroup(label(r"``Opposing Forces''", font_size=40),
                      label(r"Jurrien Timmer, Fidelity Investments", font_size=30, color=GREY_A),
                      label(r"weekly note, week of October 5, 2026", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.15)
        note.to_corner(UL, buff=0.5)
        VGroup(rope, up, dn, knot, up_l, dn_l, knot_l).shift(RIGHT * 1.5)
        with self.voiceover(
            "That's the puzzle at the heart of a weekly note by Jurrien Timmer, Fidelity's director of global macro, "
            "<bookmark mark='n'/> for the week of October 5th, 2026. He called it Opposing Forces. His argument: the "
            "market is being pulled apart. <bookmark mark='u'/> On one side, an enormous earnings boom. <bookmark "
            "mark='d'/> On the other, a rising cost of capital: interest rates, driven higher by forces that have little "
            "to do with the stock market. <bookmark mark='p'/> And the price sits in the middle, the result of the tug "
            "of war."
        ) as vo:
            vo.wait_until("n")
            self.play(FadeIn(note, shift=DOWN * 0.2))
            vo.wait_until("u")
            self.play(Create(rope), FadeIn(knot), GrowArrow(up), FadeIn(up_l))
            vo.wait_until("d")
            self.play(GrowArrow(dn), FadeIn(dn_l))
            vo.wait_until("p")
            self.play(FadeIn(knot_l), knot.animate.shift(UP * 0.15), rate_func=there_and_back, run_time=0.8)
            self.play(knot.animate.shift(DOWN * 0.12), rate_func=there_and_back, run_time=0.8)
        self.clear_scene()

    # ------------------------------------------------------------------
    def roadmap(self):
        items = VGroup(*[label(s, font_size=34) for s in [
            r"1.\ the arithmetic linking prices, profits, and interest rates",
            r"2.\ why bond yields are rising: four forces",
            r"3.\ who gets hurt, and the Fed's dilemma",
            r"4.\ the earnings boom, and why peak growth gets a lower multiple",
            r"5.\ is it a bubble? and where are we in the cycle?",
        ]]).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(UP * 0.4)
        disc = label(r"An explanation of one strategist's view as of October 2026,\\"
                     r"checked against public data. Not investment advice.", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In this video, we'll unpack that argument piece by piece, and check each claim against public data. "
            "<bookmark mark='a'/> First, the simple arithmetic that links stock prices, profits, and interest rates. "
            "<bookmark mark='b'/> Then, why bond yields are rising: Timmer points to four separate forces. <bookmark "
            "mark='c'/> Who gets hurt, and why the Federal Reserve is stuck. <bookmark mark='d'/> The earnings boom itself, "
            "and why markets rarely pay up for peak growth. <bookmark mark='e'/> And finally: is this a bubble, and where "
            "are we in the cycle? <bookmark mark='x'/> One note: this explains one strategist's view as of early "
            "October 2026. It is not investment advice."
        ) as vo:
            for i, m in enumerate("abcde"):
                vo.wait_until(m)
                self.play(FadeIn(items[i], shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("x")
            self.play(FadeIn(disc))
        self.clear_scene()

        card = VGroup(label(r"Opposing Forces", font_size=72),
                      label(r"booming earnings vs.\ the rising cost of money", font_size=38, color=GREY_A)).arrange(DOWN, buff=0.4)
        card[0][0][:8].set_color(C.EARNINGS)
        card[0][0][8:].set_color(C.RATE)
        self.play(FadeIn(card, scale=1.05), run_time=1.2)
        self.wait(2.5)
        self.play(FadeOut(card))
