from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import rates as R
from videos.quant.quant18.common import BAD, CONV, PAR, PART, ZERO, ask, illustration, load

TAN = QC.DELTA


class Duration(VoiceoverScene):
    def construct(self):
        b = load("bonds")
        self.card()
        self.seesaw()
        self.derive()
        self.curve_(b)
        self.desk(b, load("svb"))

    def card(self):
        c = chapter_card(6, r"Duration and convexity", r"How much does a bond lose when rates rise?", lit=(1938,),
                         part=PART)
        with self.voiceover("Chapter six. Duration and convexity: the arithmetic behind the hook."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def seesaw(self):
        y = 0.045
        rows = []
        for T, cpn in ((10, 0.045), (10, 0.0)):
            t = np.arange(1, 2 * T + 1) / 2
            cf = np.full(len(t), 100 * cpn / 2)
            cf[-1] += 100
            pv = cf * (1 + y / 2) ** (-2 * t)
            rows.append((t, pv, float(np.sum(t * pv) / pv.sum())))
        beam_y = -0.6
        X0, W = -5.6, 10.6

        def X(t):
            return X0 + W * t / 10.5

        def build(t, pv, mac, col):
            beam = Line([X(0), beam_y, 0], [X(10.5), beam_y, 0], color=GREY_B, stroke_width=4)
            total = float(np.sum(pv))
            hs = 3.0 * np.asarray(pv) / total
            bars = VGroup(*[Rectangle(width=0.18, height=float(h), stroke_width=0, fill_color=col,
                                      fill_opacity=0.85).move_to([X(a), beam_y + h / 2 + 0.03, 0])
                            for a, h in zip(t, hs) if h > 0])
            top = MathTex(rf"{100 * pv[-1] / total:.1f}\%", font_size=22,
                          color=col).next_to(bars[-1], UP, buff=0.08)
            bars.add(top)
            fulcrum = Triangle(color=WHITE, fill_opacity=1).scale(0.22).move_to([X(mac), beam_y - 0.25, 0])
            lab = MathTex(rf"D_{{\text{{Mac}}}} = {mac:.2f}\ \text{{years}}", font_size=30).next_to(fulcrum, DOWN,
                                                                                                buff=0.75)
            ticks = VGroup(*[MathTex(str(k), font_size=18, color=GREY_B).move_to([X(k), beam_y - 0.9, 0])
                             for k in (0, 2, 4, 6, 8, 10)])
            return VGroup(beam, bars, fulcrum, lab, ticks)
        a = build(*rows[0], PAR)
        b = build(*rows[1], ZERO)
        head = label(r"present-value weights on a time line: full weights sum to one", font_size=24).to_edge(UP, buff=0.5)
        sub_a = label(r"a 10-year bond, 4.5\% coupon, yield 4.5\%", font_size=20, color=PAR).next_to(head, DOWN, buff=0.2)
        sub_b = label(r"a 10-year zero-coupon bond", font_size=20, color=ZERO).next_to(head, DOWN, buff=0.2)
        with self.voiceover(
            f"Macaulay's 1938 duration is the present-value-weighted mean payment time for specified fixed cash flows. Here every height is proportional to its complete present-value weight, normalized to sum to one for each bond; zero cash flows have no bar. <bookmark mark='a'/> The balance point is {rows[0][2]:.2f} years for this ten-year, four-and-a-half-percent coupon bond at the same nominal yield. Coupons bring some value forward, so its Macaulay duration is below maturity. <bookmark mark='b'/> A zero-coupon bond has one positive payment. Its entire normalized weight is at maturity, so Macaulay duration equals ten years. Modified duration is a different derivative quantity and depends on the yield convention."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub_a), FadeIn(a[0]), FadeIn(a[4]),
                      LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in a[1][:-1]], lag_ratio=0.05), FadeIn(a[1][-1]),
                      run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(a[2], shift=UP * 0.3), Write(a[3]))
            vo.wait_until("b")
            self.play(ReplacementTransform(a, b), ReplacementTransform(sub_a, sub_b), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"P(y)", r"=", r"\sum_i \mathrm{CF}_i \big(1 + \tfrac{y}{2}\big)^{-2t_i}", font_size=40,
                      colors={r"P(y)": PAR}),
                cmath(r"-\frac{1}{P}\frac{dP}{dy}", r"=", r"\frac{1}{1 + y/2}\ \frac{\sum_i t_i\,\mathrm{PV}_i}{P} = "
                      r"\frac{D_{\text{Mac}}}{1 + y/2} = D", font_size=38, colors={r"-\frac{1}{P}\frac{dP}{dy}": TAN}),
                cmath(r"\frac{\Delta P}{P}", r"\approx", r"-D\,\Delta y + \tfrac12\,C\,(\Delta y)^2", font_size=42,
                      colors={r"\frac{\Delta P}{P}": WHITE}),
                cmath(r"\text{DV01}", r"=", r"D \times P \times 0.0001", font_size=40, colors={r"\text{DV01}": BAD})]
        whys = [why(r"price from yield, semiannual compounding"),
                why(r"differentiate: each payment's sensitivity is its time, so the slope is the value-weighted average "
                    r"time, Macaulay's duration, over one period's growth: modified duration $D$"),
                why(r"a local Taylor expansion. For fixed nonnegative cash flows and admissible yield, $C=P''/P>0$; options, changing cash flows and large shocks need separate treatment"),
                why(r"the first-order dollar change for a 1bp yield fall per 100 face. Add signed dollar sensitivities only under consistent currency, curve and bump conventions")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "For fixed, nonnegative bullet-bond cash flows on a regular semiannual schedule, write price as a function of the nominal semiannual yield, with one plus half the yield positive. <bookmark mark='a'/> Differentiating gives modified duration: Macaulay duration divided by one plus half the yield. This is sensitivity to the specified yield coordinate, not automatically to every curve shape. <bookmark mark='b'/> The second derivative gives convexity. Positive convexity puts this fixed-cash-flow price above its tangent. The quadratic expansion is local; it does not guarantee accuracy for large moves, and embedded options can change cash flows and effective convexity. <bookmark mark='c'/> Duration times price times one basis point is a positive first-order gain for a yield fall; a rise has the opposite sign. Actual finite changes include higher orders. Positions require signed dollar exposures and consistent bump conventions before aggregation."
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

    def curve_(self, b):
        ys = np.asarray(b["y"]) * 100
        c30 = b["curves"]["30"]
        P, tg, qd = (np.asarray(c30[k]) for k in ["P", "tangent", "quad"])
        all_values = np.concatenate([P, tg, qd])
        lo = 50.0 * np.floor(np.min(all_values[np.isfinite(all_values)]) / 50.0)
        hi = 50.0 * np.ceil(np.max(all_values[np.isfinite(all_values)]) / 50.0)
        g = axes([0, 12], [lo, hi], x_length=6.8, y_length=4.8, xlabel=r"yield, \%", ylabel=r"price of a 30-year, "
                 r"4\% bond", xticks=[0, 2, 4, 6, 8, 10, 12], yticks=list(np.arange(lo, hi + 1, 50)), font_size=14).to_edge(
            LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        lp = curve(ax, ys, P, PAR, stroke_width=4)
        lt = curve(ax, ys, tg, TAN, stroke_width=2.5)
        lq = DashedVMobject(curve(ax, ys, qd, CONV, stroke_width=2.5), num_dashes=50)
        dot = Dot(ax.c2p(4, 100), color=WHITE)
        mv = b["move30"]
        side = VGroup(
            MathTex(rf"D = {c30['modified']:.2f},\quad C = {c30['convexity']:.0f}", font_size=30),
            label(r"yields up 1 point:", font_size=20, color=GREY_A),
            MathTex(rf"\text{{exact}}\ {mv['+0.01']['exact']:+.2f},\ \ \text{{duration}}\ {mv['+0.01']['duration']:+.2f},"
                    rf"\ \ \text{{with }}C\ {mv['+0.01']['with_convexity']:+.2f}", font_size=24),
            label(r"yields down 1 point:", font_size=20, color=GREY_A),
            MathTex(rf"\text{{exact}}\ {mv['-0.01']['exact']:+.2f},\ \ \text{{duration}}\ {mv['-0.01']['duration']:+.2f},"
                    rf"\ \ \text{{with }}C\ {mv['-0.01']['with_convexity']:+.2f}", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35)
        leg = legend([(PAR, r"price"), (TAN, r"duration's tangent"), (CONV, r"with convexity")], font_size=18).next_to(
            side, UP, buff=0.4, aligned_edge=LEFT)
        with self.voiceover(
            f"This fixed four-percent coupon bond has thirty years remaining and is at par when its nominal yield is four percent. The full saved zero-to-twelve-percent yield range is displayed, including every exact-price, tangent and quadratic value. <bookmark mark='a'/> Modified duration at the base yield is {c30['modified']:.2f}: a small one-percentage-point rise gives a first-order loss of about that percent. <bookmark mark='b'/> The exact positive-cash-flow price lies above the tangent. The quadratic correction is a local improvement, not a uniformly accurate formula; far away the linear approximation even becomes negative, which is not a physical bond price. <bookmark mark='c'/> A one-point rise produces an exact price loss of {abs(mv['+0.01']['exact']):.2f} per hundred against the tangent's {abs(mv['+0.01']['duration']):.2f}. A one-point fall gives {mv['-0.01']['exact']:.2f}. This comparison is with one bond's local tangent, not a theorem about the market prices of different bonds."
        ) as vo:
            self.play(FadeIn(g), Create(lp), FadeIn(leg[0]), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(dot), Create(lt), FadeIn(leg[1]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lq), FadeIn(leg[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side[1:]], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def desk(self, b, v):
        z = b["zero10"]
        q = desk_question(r"A 10-year zero yields 4\% (annual). Duration? Price change for +1 bp?",
                          rf"price $100/1.04^{{10}} = {z['price']:.2f}$; Macaulay duration 10, modified "
                          rf"$10/1.04 = {z['modified']:.2f}$; DV01 $= {z['modified']:.2f} \times {z['price']:.2f} "
                          rf"\times 0.0001 = {z['dv01']:.4f}$ per 100: one basis point up costs about 6.5 cents",
                          width=12.0, font_size=25).to_edge(UP, buff=0.5)
        f = v["facts"]
        htm = f["HeldToMaturitySecurities"]["2022-12-31"]
        rep = f["HeldToMaturitySecuritiesAccumulatedUnrecognizedHoldingLoss"]["2022-12-31"]
        eq = f["StockholdersEquity"]["2022-12-31"]
        rows = [cmath(r"\Delta V", r"\approx", rf"-D \times \Delta y \times V = -{v['duration']} \times "
                      rf"{v['dy6_2022_pct'] / 100:.4f} \times {htm:.1f}", font_size=36, colors={r"\Delta V": BAD}),
                cmath(r"", r"=", rf"-{v['est_loss']:.1f}\ \text{{bn}}\quad(\text{{reported }} {rep:.2f};\ \text{{equity }}"
                      rf"{eq:.2f})", font_size=36, colors={r"=": WHITE})]
        rows_g = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(q, DOWN, buff=0.7)
        note_ = wrapped_label(r"SVBFG fixed-notional linear proxy: reported duration treated as constant modified sensitivity to a 6-year GSW yield. Gross HTM fair-value gap is separate; taxes, liability values, mortgage optionality and other assets are omitted", 12.0, 19,
                              GREY_A).next_to(rows_g, DOWN, buff=0.4)
        with self.voiceover(
            f"For a ten-year zero with four-percent annual compounding, the price is {z['price']:.2f} per hundred. Macaulay duration is ten and modified duration is {z['modified']:.2f}, giving a first-order loss of about six-and-a-half cents for a one-basis-point rise. <bookmark mark='a'/> Return to the opening proxy: fix SVB Financial Group's year-end held-to-maturity notional, use six-point-two as an approximate modified sensitivity, and apply the {v['dy6_2022_pct']:.2f}-point change in the six-year fitted Treasury yield. The rough asset loss is {v['est_loss']:.1f} billion dollars. <bookmark mark='b'/> The separate reported gross held-to-maturity fair-value gap was {rep:.2f} billion against holding-company book equity of {eq:.2f}. Comparing them highlights rate risk, but it is not a complete economic-equity calculation or an insolvency certificate. Taxes, the values of deposits and other assets, funding, prepayment and hedges also matter."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(FadeIn(rows_g[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows_g[1]), FadeIn(note_))
        p = ask(r"Do equal yield and duration plus more convexity determine a bond's price? What other assumptions are needed?")
        with self.voiceover('Pause and predict: two bonds share a yield and duration, but one has more convexity. Do those facts alone determine which costs more? Consider cash-flow scale, options, risk, carry and the pricing model.'):
            self.play(FadeIn(p))
        self.wait(0.5)
        self.clear_scene()
