from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.opposing_forces.common import TimeChart, label, show_chapter_card, source, tagged, ts, window

COUPON = 0.06  # the illustrative pool's mortgage rate


def pool_price(y: float, prepay: bool = True, c: float = COUPON, n: int = 360) -> float:
    """Price of a 30-year pool of fixed-rate mortgages (per $100), discounted at yield ``y``.

    A schematic model: borrowers refinance faster the further market rates fall below their
    own rate (an S-curve in annual prepayment speed, from 5% up to 50%).  With ``prepay=False``
    it is the same loan with no option to repay early.
    """
    r = c / 12
    pay = 100 * r / (1 - (1 + r) ** -n)
    cpr = 0.05 + 0.45 / (1 + np.exp(-(c - y - 0.005) / 0.005)) if prepay else 0.0
    smm = 1 - (1 - cpr) ** (1 / 12)
    t = np.arange(1, n + 1)
    bal, price = 100.0, 0.0
    disc = (1 + y / 12) ** -t
    for k in range(n):
        if bal < 1e-9:
            break
        interest = bal * r
        sched = min(bal, pay - interest)
        pre = (bal - sched) * smm
        price += (interest + sched + pre) * disc[k]
        bal -= sched + pre
    return price


def duration(y: float, prepay: bool = True) -> float:
    h = 1e-4
    return -(pool_price(y + h, prepay) - pool_price(y - h, prepay)) / (2 * h) / pool_price(y, prepay)


class Convexity(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 7, r"Force 4: the mortgage market")
        self.option()
        self.curves()
        self.hedging()
        self.mortgage_rates()

    # ------------------------------------------------------------------
    def option(self):
        house = VGroup(Polygon([-0.9, 0, 0], [0.9, 0, 0], [0, 0.8, 0], stroke_color=C.MORTGAGE, stroke_width=4),
                       Square(1.4, stroke_color=C.MORTGAGE, stroke_width=4).shift(DOWN * 0.7))
        house.move_to(LEFT * 4.6 + UP * 0.6)
        facts = VGroup(label(r"the typical U.S. mortgage: 30 years, fixed rate", font_size=32, color=C.MORTGAGE),
                       label(r"and the borrower can repay it early, any time, without penalty", font_size=30),
                       label(r"rates fall $\Rightarrow$ homeowners refinance", font_size=30, color=GREY_A),
                       label(r"mortgages are pooled into bonds: mortgage-backed securities", font_size=30, color=GREY_A),
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 1.3 + UP * 0.4)
        with self.voiceover(
            "Force number four comes from an odd feature of American home loans. <bookmark mark='a'/> The typical "
            "mortgage has a fixed rate for thirty years, <bookmark mark='b'/> and the homeowner can pay it off early, any "
            "time, with no penalty. <bookmark mark='c'/> So when rates fall, people refinance. <bookmark mark='d'/> "
            "Those mortgages are bundled into bonds, mortgage-backed securities, owned by banks, funds and the Fed. And "
            "the homeowner's right to refinance is an option that the bond's owner has, in effect, sold them."
        ) as vo:
            self.play(Create(house))
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(facts[i], shift=RIGHT * 0.2), run_time=0.7)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        ys = np.linspace(0.035, 0.09, 56)
        mbs = np.array([pool_price(y) for y in ys])
        bond = np.array([pool_price(y, prepay=False) for y in ys])
        d_lo, d_hi = duration(COUPON - 0.01), duration(COUPON + 0.01)
        assert d_lo < 3 and d_hi > 5 and duration(COUPON - 0.01, False) > 9
        assert duration(0.05) < 1.2 and duration(0.072) > 6  # "from about one year to more than six"
        ch = TimeChart((3.5, 9.0), (70, 140), width=8.4, height=5.2, x_ticks=[4, 5, 6, 7, 8, 9],
                       x_fmt=lambda v: rf"{v:g}\%", y_ticks=[70, 80, 90, 100, 110, 120, 130, 140]).move_to(LEFT * 2.0 + DOWN * 0.3)
        xl = label(r"market interest rate", font_size=26, color=C.RATE).next_to(ch, DOWN, buff=0.1).align_to(ch.x_axis, RIGHT)
        yl = ch.y_title(r"price, per \$100 of loans", color=GREY_A)
        l_bond = ch.line(ys * 100, bond, GREY_A, 4)
        l_mbs = ch.line(ys * 100, mbs, C.MORTGAGE, 6)
        t_bond = tagged(r"if borrowers couldn't refinance", font_size=24, color=GREY_A).next_to(ch.c2p(3.9, 128), RIGHT, buff=0.1)
        t_mbs = tagged(r"mortgage bond", font_size=26, color=C.MORTGAGE).move_to(ch.c2p(4.4, 96))
        cap = tagged(r"upside capped:\\borrowers refinance", font_size=24, color=C.MORTGAGE).move_to(ch.c2p(4.7, 109))
        sch = label(r"(schematic model: 6\% mortgages, refinancing speeds up as rates fall)", font_size=22,
                    color=GREY_B).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Here's what that option does to the bond. <bookmark mark='g'/> In grey: what a pool of six percent mortgages "
            "would be worth if nobody could refinance. When rates fall, its price climbs, and the curve bends upward, "
            "which is a pleasant property called convexity. <bookmark mark='m'/> Now the real thing. When rates fall, "
            "homeowners refinance and pay the loans back at face value, <bookmark mark='c'/> so the bond's price can "
            "barely rise. When rates rise, nobody refinances, and the price falls. The curve bends the wrong way. That's "
            "negative convexity: you lose on the way down and don't win on the way up."
        ) as vo:
            self.play(Create(ch), FadeIn(xl), FadeIn(yl), FadeIn(sch))
            vo.wait_until("g")
            self.play(Create(l_bond), FadeIn(t_bond), run_time=2)
            vo.wait_until("m")
            self.play(Create(l_mbs), FadeIn(t_mbs), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(cap))

        y = ValueTracker(5.0)

        def tangent():
            yv = y.get_value() / 100
            p = pool_price(yv)
            slope = -duration(yv) * p / 100  # price change per percentage point
            a, b = yv * 100 - 0.8, yv * 100 + 0.8
            return VGroup(Line(ch.c2p(a, p + slope * (a - yv * 100)), ch.c2p(b, p + slope * (b - yv * 100)), color=YELLOW,
                               stroke_width=4), Dot(ch.c2p(yv * 100, p), radius=0.08, color=YELLOW))

        tan = always_redraw(tangent)
        read = always_redraw(lambda: VGroup(
            MathTex(rf"\text{{rate}} = {y.get_value():.1f}\%", font_size=34, color=C.RATE),
            MathTex(rf"\text{{duration}} \approx {duration(y.get_value() / 100):.1f} \text{{ years}}", font_size=34,
                    color=YELLOW)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 4.6 + UP * 1.6))
        dl = label(r"duration: how much the price moves\\when rates move (the slope)", font_size=26, color=GREY_A)
        dl.move_to(RIGHT * 4.6 + UP * 0.1)
        with self.voiceover(
            "The slope of that curve is what bond investors call duration: how sensitive the price is to rates. "
            "<bookmark mark='a'/> When rates are low, the mortgage bond behaves like a short-term bond, because everyone is "
            "expected to refinance soon. <bookmark mark='b'/> But as rates rise past the mortgage rate, refinancing "
            "stops, the loans are expected to last much longer, and the duration stretches out, from about one year to "
            "more than six. Owners suddenly hold far more interest-rate risk than they signed up for."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tan), FadeIn(read), FadeIn(dl))
            vo.wait_until("b")
            self.play(y.animate.set_value(7.2), run_time=4, rate_func=smooth)
        tan.clear_updaters()
        read.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def hedging(self):
        nodes = [r"rates rise", r"mortgage bonds' duration\\stretches out", r"hedgers sell Treasuries\\to cut their risk",
                 r"Treasury prices fall"]
        cols = [C.RATE, C.MORTGAGE, C.MORTGAGE, C.RATE]
        pos = [UP * 2.1, RIGHT * 3.9, DOWN * 2.1, LEFT * 3.9]
        boxes = VGroup()
        for n, c, p in zip(nodes, cols, pos):
            b = label(n, font_size=32, color=c)
            b.add_background_rectangle(color=BACKGROUND, opacity=1, buff=0.12)
            boxes.add(b.move_to(p + DOWN * 0.2))
        arcs = VGroup()
        for i in range(4):
            a, b = boxes[i], boxes[(i + 1) % 4]
            arcs.add(CurvedArrow(a.get_center() + (b.get_center() - a.get_center()) * 0.3,
                                 b.get_center() - (b.get_center() - a.get_center()) * 0.3, angle=-PI / 4, color=GREY_B,
                                 stroke_width=4))
        with self.voiceover(
            "And that creates another feedback loop. <bookmark mark='a'/> Rates rise. <bookmark mark='b'/> Mortgage "
            "bonds' duration stretches out. <bookmark mark='c'/> The big holders, and the companies that service "
            "mortgages, often hedge their risk, so to get back to their target they sell Treasuries, or make equivalent "
            "trades in the swap market. <bookmark mark='d'/> That selling pushes Treasury prices down, <bookmark "
            "mark='e'/> which means yields go up further. Rate moves get amplified. This is called convexity hedging, "
            "and it has turned modest bond selloffs into sharp ones before."
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
        self.clear_scene()

    # ------------------------------------------------------------------
    def mortgage_rates(self):
        t, v = ts("mortgage_weekly")
        t, v = window(t, v, 2019)
        k_lo = int(np.argmin(np.where(t > 2025.8, v, 99)))
        assert 2026.1 < t[k_lo] < 2026.25 and 5.9 < v[k_lo] < 6.05 and abs(v[-1] - 7.28) < 0.01
        assert (v[(t > 2022.75) & (t < t[k_lo] - 0.01)] > v[k_lo]).all()  # lowest in more than three years
        assert v[(t > 2023.5) & (t < 2024.5)].max() >= v[-1] and v[(t > 2024) & (t < 2026.7)].max() < v[-1]
        ch = TimeChart((2019, 2026.85), (2.0, 8.5), width=10.4, height=4.8, x_ticks=range(2019, 2027),
                       y_ticks=[2, 3, 4, 5, 6, 7, 8], y_fmt=lambda y: rf"{y:g}\%").move_to(DOWN * 0.35)
        yl = ch.y_title(r"30-year fixed mortgage rate", color=C.MORTGAGE)
        before = window(t, v, -np.inf, t[k_lo])
        after = window(t, v, t[k_lo])
        l1, l2 = ch.line(*before, C.MORTGAGE, 4), ch.line(*after, C.MORTGAGE, 6)
        lo = tagged(rf"Feb 2026: {v[k_lo]:.2f}\%", font_size=26).next_to(ch.c2p(t[k_lo], v[k_lo]), DOWN, buff=0.15)
        hi = tagged(rf"Oct 1: {v[-1]:.2f}\%\\highest since 2023", font_size=26, color=C.MORTGAGE)
        hi.next_to(ch.c2p(t[-1], v[-1]), LEFT, buff=0.25).shift(UP * 0.3)
        src = source(r"FRED (MORTGAGE30US, Freddie Mac)")
        with self.voiceover(
            "Here's the trigger. <bookmark mark='a'/> Early this year, mortgage rates dipped to about six percent, the "
            "lowest in more than three years. <bookmark mark='b'/> By October first they were back above seven, the highest "
            "since 2023. A swing like that, over a few months, is exactly what sets off convexity hedging. Timmer counts it "
            "as the most recent of the four forces: a negative convexity event from the mortgage market."
        ) as vo:
            self.play(Create(ch), FadeIn(yl), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(l1), run_time=2.5, rate_func=linear)
            self.play(FadeIn(lo))
            vo.wait_until("b")
            self.play(Create(l2), run_time=1.5, rate_func=linear)
            self.play(FadeIn(hi))
        self.clear_scene()
