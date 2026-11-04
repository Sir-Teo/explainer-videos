from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import rates as R
from videos.quant.quant18.common import FWD, PAR, PART, ZERO, ask, illustration, load


class Bonds(VoiceoverScene):
    def construct(self):
        c = load("curve_day")["20251231"]
        self.card()
        self.flows(c)
        self.algebra()
        self.three(c)
        self.conventions()

    def card(self):
        c = chapter_card(4, r"Bonds, yields and forwards", r"What does one price say about every future date?",
                         lit=(1938,), part=PART)
        with self.voiceover("Chapter four. Bonds, yields, and forward rates."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def flows(self, c):
        curve_ = R.Curve(c["nodes_t"], c["nodes_z"])
        t = np.arange(1, 21) / 2
        cf = np.r_[np.full(19, 2.0), 102.0]
        pv = cf * curve_.df(t)
        g = axes([0, 10.5], [0, 4.2], x_length=10.0, y_length=4.2, xlabel=r"years from today",
                 ylabel=r"cash flow per 100 (bar height capped)", xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 2, 4],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        ax = g.ax

        def bar(x, h, col, op=0.85):
            h = min(h, 4.0)
            p0, p1 = ax.c2p(x - 0.17, 0), ax.c2p(x + 0.17, h)
            return Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.01), stroke_width=0, fill_color=col,
                             fill_opacity=op).move_to((p0 + p1) / 2)
        raw = VGroup(*[bar(a, b, PAR) for a, b in zip(t, cf)])
        disc = VGroup(*[bar(a, b, ZERO) for a, b in zip(t, pv)])
        big = MathTex(r"102", font_size=24, color=PAR).next_to(raw[-1], UP, buff=0.08)
        bigp = MathTex(rf"{pv[-1]:.1f}", font_size=24, color=ZERO).next_to(disc[-1], UP, buff=0.08)
        price = float(pv.sum())
        y = R.bond_yield(price, 0.04, 10)
        side = VGroup(
            MathTex(r"P = \sum_i \mathrm{CF}_i\, Z(t_i)", font_size=36),
            MathTex(rf"= {price:.2f}", font_size=36, color=ZERO),
            MathTex(rf"\text{{yield}} = {100 * y:.2f}\%", font_size=32, color=PAR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.4)
        head = label(r"a 10-year Treasury, 4\% coupon, paid twice a year", font_size=22).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A Treasury note is a promise of dated payments. This one pays a four percent coupon, two dollars every "
            "six months for ten years, and its hundred dollars of principal at the end. <bookmark mark='a'/> Each "
            "payment is worth less than its face value today, because it comes later. Multiply each one by the "
            "discount factor for its date, the price today of one dollar paid then, and the bars shrink. "
            f"<bookmark mark='b'/> Add them up: on the last trading day of 2025, off Treasury's own curve, this note "
            f"was worth {price:.2f}. <bookmark mark='c'/> The yield is the single rate that, applied to every "
            f"payment, gives the same price: {100 * y:.2f} percent. It is an average over the dates, and like any "
            "average it hides the shape."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), LaggedStart(*[GrowFromEdge(b, DOWN) for b in raw], lag_ratio=0.05),
                      FadeIn(big), run_time=2.5)
            vo.wait_until("a")
            self.play(*[Transform(a_, b_) for a_, b_ in zip(raw, disc)], Transform(big, bigp), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.add(illustration(r"discount factors bootstrapped from Treasury's par yields of 31 December 2025 (chapter 5)"))
        self.wait(0.4)
        self.clear_scene()

    def algebra(self):
        rows = [cmath(r"Z(t)", r"=", r"e^{-z(t)\,t}", font_size=44, colors={r"Z(t)": ZERO}),
                cmath(r"Z(t_2)", r"=", r"Z(t_1)\,e^{-f(t_1, t_2)(t_2 - t_1)}", font_size=42, colors={r"Z(t_2)": ZERO}),
                cmath(r"f(t_1, t_2)", r"=", r"\frac{z(t_2)\,t_2 - z(t_1)\,t_1}{t_2 - t_1}", font_size=42,
                      colors={r"f(t_1, t_2)": FWD}),
                cmath(r"f(t)", r"=", r"z(t) + t\,z'(t)", font_size=44, colors={r"f(t)": FWD})]
        whys = [why(r"the zero-coupon yield $z(t)$: the rate earned on a single payment at $t$, continuously "
                    r"compounded"),
                why(r"no arbitrage: lending to $t_2$ must equal lending to $t_1$ and then rolling at the rate you can "
                    r"lock in today, the forward rate"),
                why(r"take logs: the forward is what the longer zero adds over the shorter one, per year"),
                why(r"let $t_2 \to t_1$: the instantaneous forward. It sits above the zero curve where the curve rises, "
                    r"below where it falls: a marginal rate against an average one")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-2.2, buff=0.55, edge=6.9)
        with self.voiceover(
            "So name the pieces. The discount factor for date t is e to the minus z of t times t, where z is the "
            "zero-coupon yield: what a single payment at t earns. <bookmark mark='a'/> Lending to year two must cost "
            "the same as lending to year one and then rolling over at a rate you can lock in today. That locked-in "
            "rate is the forward rate. <bookmark mark='b'/> Take logarithms, and the forward is what the longer zero "
            "adds over the shorter one, per year. <bookmark mark='c'/> Shrink the interval to nothing, and the "
            "instantaneous forward is the zero rate plus t times its slope. Where the curve rises, forwards lie "
            "above it, as a marginal cost lies above a rising average cost."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def three(self, c):
        s = np.asarray(c["s"])
        z, f = np.asarray(c["zero"]) * 100, np.asarray(c["fwd"]) * 100
        cv = R.Curve(c["nodes_t"], c["nodes_z"])
        Tp = np.linspace(1, 30, 59)
        par = np.array([cv.par(x) for x in Tp]) * 100
        g = axes([0, 30], [3, 6.5], x_length=8.4, y_length=4.6, xlabel=r"maturity, years", ylabel=r"percent",
                 xticks=[0, 5, 10, 20, 30], yticks=[3, 4, 5, 6], font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lz = curve(ax, s, np.clip(z, 3, 6.5), ZERO, stroke_width=3.5)
        lf = curve(ax, s, np.clip(f, 3, 6.5), FWD, stroke_width=3)
        lp = curve(ax, Tp, np.clip(par, 3, 6.5), PAR, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(a, 100 * b), radius=0.05, color=PAR) for a, b in zip(c["tenor"], c["par"])
                        if a >= 1])
        leg = legend([(PAR, r"par yields (Treasury's quotes: dots)"), (ZERO, r"zero-coupon yields"),
                      (FWD, r"instantaneous forwards")], font_size=18).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        k1, k2 = int(np.argmin(np.abs(s - 15))), int(np.argmin(np.abs(s - 25)))
        tip = wrapped_label(rf"the bootstrap's forwards are steps: flat between quoted maturities, jumping at each one. "
                            rf"{f[k1]:.2f}\% from 10 to 20 years, {f[k2]:.2f}\% from 20 to 30, as the zero curve "
                            rf"flattens. Chapter 8 fits a smooth curve instead", 3.8, 18, GREY_A).next_to(
            leg, DOWN, buff=0.4, aligned_edge=LEFT)
        with self.voiceover(
            "Three curves from the same day, the last of 2025. In blue, the par yields: the coupon at which a new "
            "bond of each maturity would price at a hundred; the dots are Treasury's own quotes. <bookmark mark='a'/> "
            "In violet, the zero-coupon yields derived from them, in the next chapter. <bookmark mark='b'/> And in "
            "orange, the forwards: the rate for one more instant of lending, at each future date. They are the most "
            "sensitive of the three; every change in the zero curve's slope shows up in them. <bookmark mark='c'/> "
            "Here they are steps: flat between the quoted maturities, jumping at each one, because the simplest way to "
            f"fill the gaps assumes a constant forward between them. {f[k1]:.2f} percent from ten to twenty years, "
            f"{f[k2]:.2f} from twenty to thirty, where the zero curve flattens out. Chapter eight fits a smooth curve "
            "instead."
        ) as vo:
            self.play(FadeIn(g), Create(lp), FadeIn(dots), FadeIn(leg[0]), run_time=2)
            vo.wait_until("a")
            self.play(Create(lz), FadeIn(leg[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lf), FadeIn(leg[2]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(tip))
        self.add(illustration(r"Treasury's daily par yield curve, 31 December 2025; bootstrapped by the House"))
        self.wait(0.4)
        self.clear_scene()

    def conventions(self):
        rows = [
            (r"US Treasury notes and bonds", r"semiannual coupons, actual/actual: days counted exactly"),
            (r"corporate and agency bonds, swap fixed legs", r"30/360: every month thirty days"),
            (r"money markets, SOFR, swap floating legs", r"actual/360: a year of 360 days, so 365 days earn a bit more"),
            (r"Treasury bills", r"quoted as a discount from par; the bond-equivalent yield converts"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=21, color=PAR), label(b, font_size=21, color=GREY_A)).arrange(
            RIGHT, buff=0.5) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 5.4)
        comp = VGroup(MathTex(r"\big(1 + \tfrac{y}{2}\big)^2 = e^{z}", font_size=40),
                      label(r"the same rate in two compoundings: 4\% semiannual is 3.96\% continuous", font_size=21,
                            color=GREY_A)).arrange(DOWN, buff=0.2)
        head = label(r"Conventions: the same promise, quoted differently", font_size=30).to_edge(UP, buff=0.5)
        VGroup(tab, comp).arrange(DOWN, buff=0.7).next_to(head, DOWN, buff=0.5)
        if tab.width > 13:
            tab.scale_to_fit_width(13)
        with self.voiceover(
            "Before computing anything, conventions, which cause more real errors on desks than models do. A rate "
            "means nothing until you say how it compounds and how days are counted. <bookmark mark='a'/> Treasuries "
            "pay twice a year and count actual days. Corporate bonds and the fixed side of a swap pretend every month "
            "has thirty days. Money markets, SOFR and the floating side of a swap count actual days over a three "
            "hundred and sixty day year. And bills are quoted as a discount, not a yield. <bookmark mark='b'/> Four "
            "percent compounded twice a year is three point nine six continuously compounded; the Fed's fitted curve "
            "uses the second, Treasury's quotes the first."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(comp))
        q = ask(r"a 2-year zero yields 4\%, a 3-year zero 4.5\% (continuous). What one-year rate can you lock in for "
                r"year three?")
        with self.voiceover("Try one. A two-year zero yields four percent, a three-year zero four and a half. What rate "
                            "can you lock in today for the third year?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
