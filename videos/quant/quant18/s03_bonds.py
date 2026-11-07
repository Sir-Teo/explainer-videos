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
        coupon = np.full(len(t), 2.0)
        coupon_pv = coupon * curve_.df(t)
        principal_pv = 100.0 * float(curve_.df(10.0))
        g = axes([0, 10.5], [0, 2.4], x_length=7.4, y_length=3.5, xlabel=r"years from valuation",
                 ylabel=r"coupon per 100 face", xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 1, 2], font_size=14)
        g.move_to(LEFT * 2.1 + DOWN * 0.1)
        principal = axes([0, 1], [0, 110], x_length=1.6, y_length=3.5, ylabel=r"principal per 100 face",
                         xticks=[], yticks=[0, 50, 100], font_size=14).move_to(RIGHT * 4.8 + DOWN * 0.1)

        def bar(ax, x, h, width, col):
            a, b = ax.c2p(x-width/2, 0), ax.c2p(x+width/2, h)
            return Rectangle(width=abs(b[0]-a[0]), height=abs(b[1]-a[1]), stroke_width=0,
                             fill_color=col, fill_opacity=0.85).move_to((a+b)/2)

        raw = VGroup(*[bar(g.ax, x, 2.0, 0.28, PAR) for x in t])
        disc = VGroup(*[bar(g.ax, x, h, 0.28, ZERO) for x,h in zip(t,coupon_pv)])
        raw_principal = bar(principal.ax, 0.5, 100.0, 0.5, PAR)
        disc_principal = bar(principal.ax, 0.5, principal_pv, 0.5, ZERO)
        big = MathTex(r"100", font_size=24, color=PAR).next_to(raw_principal, UP, buff=0.08)
        bigp = MathTex(rf"{principal_pv:.1f}", font_size=24, color=ZERO).next_to(disc_principal, UP, buff=0.08)
        price = float(coupon_pv.sum()+principal_pv)
        y = R.bond_yield(price, 0.04, 10, freq=2)
        total = MathTex(rf"P=\sum_i\mathrm{{CF}}_i Z(t_i)={price:.2f}", font_size=32, color=ZERO).move_to([-2.0,-2.7,0])
        ytm = MathTex(rf"\mathrm{{YTM}}={100*y:.2f}\%", font_size=30, color=PAR).move_to([4.3,-2.7,0])
        head = wrapped_label(r"Hypothetical 10-year, 4\% coupon bond: regular semiannual payments, valued on a coupon date", 12.2, 23).to_edge(UP,buff=0.3)
        source = wrapped_label(r"Simplified bootstrap from Treasury CMT par-curve points, 31 December 2025; model cash flows and price, no accrued interest",12.4,16,GREY_B).to_edge(DOWN,buff=0.25)
        with self.voiceover(f"Consider a hypothetical ten-year bond with a four-percent annual coupon paid semiannually, valued on a regular coupon date with no accrued interest. The left panel shows all twenty two-dollar coupons; the separate right panel shows the full hundred-dollar principal. No bar is capped. <bookmark mark='a'/> Discount each dated payment using this illustrative curve. Its positive rates make the present values smaller here; negative rates need not do that. <bookmark mark='b'/> Using our simplified bootstrap from Treasury's published December thirty-first, 2025 par-curve points gives a model price of {price:.2f} per hundred. This is not an observed quote for an identified Treasury security. <bookmark mark='c'/> The nominal semiannual yield to maturity is the single discount-rate root reproducing that price: {100 * y:.2f} percent. It is a nonlinear internal rate of return, not an arithmetic average of zero rates or a guaranteed realized holding return.") as vo:
            self.play(FadeIn(head),FadeIn(g),FadeIn(principal),FadeIn(source),LaggedStart(*[GrowFromEdge(x,DOWN) for x in raw],lag_ratio=0.04),GrowFromEdge(raw_principal,DOWN),FadeIn(big),run_time=2.5)
            vo.wait_until("a")
            self.play(*[Transform(a,b) for a,b in zip(raw,disc)],Transform(raw_principal,disc_principal),Transform(big,bigp),run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(total))
            vo.wait_until("c")
            self.play(FadeIn(ytm))
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
                why(r"where the curve is differentiable and $t>0$, take $t_2 \to t_1$. At interpolation knots use one-sided limits; above the zero where its slope is positive, "
                    r"below where it falls: a marginal rate against an average one")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-2.2, buff=0.55, edge=6.9)
        with self.voiceover(
            "Let a positive discount factor for one unit at date t be Z of t, and define its continuously compounded zero yield by minus log Z divided by t. <bookmark mark='a'/> In a frictionless single-currency setting with matching credit and collateral terms and feasible borrowing and lending, ratios of discount factors determine a forward loan rate fixed today. That rate is not generally the future short rate's physical expectation. <bookmark mark='b'/> Taking logs gives the difference in zero-yield-times-maturity divided by the lending interval. <bookmark mark='c'/> At positive maturities where the curve is differentiable, the instantaneous forward equals the zero rate plus maturity times its derivative. It exceeds the zero there exactly when that derivative is positive. At piecewise interpolation knots the derivative can jump, so one-sided values or a numerical convention are needed."
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
        lz = curve(ax, s, z, ZERO, stroke_width=3.5)
        lf = curve(ax, s, f, FWD, stroke_width=3)
        lp = curve(ax, Tp, par, PAR, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(a, 100 * b), radius=0.05, color=PAR) for a, b in zip(c["tenor"], c["par"])
                        if a >= 1])
        leg = legend([(PAR, r"par curve; dots are Treasury CMT points"), (ZERO, r"zero-coupon yields"),
                      (FWD, r"instantaneous forwards")], font_size=18).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        k1, k2 = int(np.argmin(np.abs(s - 15))), int(np.argmin(np.abs(s - 25)))
        tip = wrapped_label(rf"piecewise-flat forwards away from nodes; plotted samples join finite-difference values. "
                            rf"{f[k1]:.2f}\% from 10 to 20 years, {f[k2]:.2f}\% from 20 to 30, under this interpolation rule. Chapter 8 uses a smooth parametric fit", 3.3, 18, GREY_A).next_to(
            leg, DOWN, buff=0.4, aligned_edge=LEFT)
        tip.shift(LEFT * max(0.0, tip.get_right()[0] - 6.75))
        with self.voiceover(
            f"These curves use December thirty-first, 2025 inputs. The blue dots are Treasury constant-maturity par-curve points, derived from indicative bid-side quotations, not necessarily yields on individual securities. The connecting par curve is our simplified construction. <bookmark mark='a'/> Violet shows zero rates from our short-node convention and coupon bootstrap; it does not reproduce Treasury's official monotone-convex methodology. <bookmark mark='b'/> Orange shows sampled finite-difference forwards. Differentiating a curve amplifies changes in its slope, and forwards contain risk-premium and convention effects as well as expectations. <bookmark mark='c'/> Linear interpolation of zero yield times maturity produces flat forwards between nodes. The displayed samples connect numerical values, including central-difference conventions near knots. The interior ten-to-twenty-year forward is {f[k1]:.2f} percent, and the twenty-to-thirty-year one is {f[k2]:.2f}, under this particular interpolation."
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
        entries = [
            (r"Treasury fixed-rate notes/bonds",r"regular semiannual payments; actual/actual conventions"),
            (r"USD corporate bonds; swaps",r"often 30/360 for bonds; swap fixed-leg day count is product-specific"),
            (r"SOFR and USD SOFR OIS",r"ACT/360 calendar-day weighting; payment, observation and lookback rules matter"),
            (r"Treasury bills and CMT points",r"discount and investment-yield quotes differ; CMT par points need not equal an individual security's yield"),
        ]
        tab = VGroup()
        for i,(a,b) in enumerate(entries):
            yy=1.9-0.95*i
            tab.add(VGroup(wrapped_label(a,4.4,21,PAR).move_to([-4.3,yy,0]),wrapped_label(b,7.0,20,GREY_A).move_to([2.0,yy,0])))
        head = label(r"Contract-specific conventions",font_size=32).to_edge(UP,buff=0.4)
        comp = VGroup(MathTex(r"(1+y/2)^2=e^z",font_size=38),wrapped_label(r"4\% nominal semiannual is about 3.96\% continuous for the same one-year accumulation",11.8,21,GREY_A)).arrange(DOWN,buff=0.2).move_to(DOWN*2.4)
        with self.voiceover("A rate quotation needs a compounding rule, day count, payment calendar and price convention. Those details depend on the contract. <bookmark mark='a'/> Fixed-rate Treasury notes and bonds normally pay semiannually with actual-over-actual conventions. Many dollar corporate bonds use thirty-over-three-sixty. Swap fixed-leg day counts depend on currency and product; a SOFR overnight-indexed swap commonly uses actual-over-three-sixty on both legs. SOFR compounding weights each fixing by its applicable calendar days. Treasury bills have bank-discount and investment-yield quotations, which should not be confused with the published CMT par curve. <bookmark mark='b'/> A four-percent nominal rate compounded semiannually corresponds to about three-point-nine-six percent continuously compounded. GSW model zero yields and Treasury bond-equivalent par rates use different conventions; changing the quote convention does not change a specified discount factor.") as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in tab],lag_ratio=0.35))
            vo.wait_until("b")
            self.play(FadeIn(comp))
        self.clear_scene()
        question=wrapped_label(r"Pause and predict: $z(2)=4\%$, $z(3)=4.5\%$, continuously compounded. What one-year forward rate is locked for year three?",11.8,29,QC.IDEA).shift(UP*0.8)
        result=MathTex(r"f(2,3)=\frac{3\times4.5\%-2\times4\%}{3-2}=5.5\%",font_size=42,color=FWD).shift(DOWN*1.1)
        with self.voiceover('Pause and predict: continuously compounded zero rates are four percent at two years and four-and-a-half percent at three years. What continuously compounded one-year forward rate is locked for the third year under the matching discount-curve assumptions?'):
            self.play(FadeIn(question))
        self.wait(2.5)
        with self.voiceover('The one-year forward is five-and-a-half percent: three times four-and-a-half, minus two times four. This is a rate implied by discount-factor ratios, not a forecast of the realized short rate.'):
            self.play(FadeIn(result))
        self.wait(0.5)
        self.clear_scene()
