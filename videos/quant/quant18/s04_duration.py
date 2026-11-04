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
        beam_y = -0.2
        X0, W = -5.6, 10.6

        def X(t):
            return X0 + W * t / 10.5

        def build(t, pv, mac, col):
            beam = Line([X(0), beam_y, 0], [X(10.5), beam_y, 0], color=GREY_B, stroke_width=4)
            cap = 3.0
            small = pv[:-1].max() if len(pv) > 1 else pv.max()
            scale = 1.2 / small if small > 1e-9 else cap / pv.max()
            hs = [min(v * scale, cap) for v in pv]
            bars = VGroup(*[Rectangle(width=0.18, height=max(h, 0.02), stroke_width=0, fill_color=col,
                                      fill_opacity=0.85).move_to([X(a), beam_y + max(h, 0.02) / 2 + 0.03, 0])
                            for a, h in zip(t, hs)])
            top = MathTex(rf"{pv[-1]:.1f}" + (r"\ \text{(bar cut)}" if pv[-1] * scale > cap else ""), font_size=22,
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
        head = label(r"present value of each payment, standing on a time line", font_size=24).to_edge(UP, buff=0.5)
        sub_a = label(r"a 10-year bond, 4.5\% coupon, yield 4.5\%", font_size=20, color=PAR).next_to(head, DOWN, buff=0.2)
        sub_b = label(r"a 10-year zero-coupon bond", font_size=20, color=ZERO).next_to(head, DOWN, buff=0.2)
        with self.voiceover(
            "Macaulay's idea, from 1938. Stand each payment's present value on a time line, like weights on a beam. "
            "<bookmark mark='a'/> The point where the beam balances is the bond's duration: the average time you wait "
            f"for its money, weighted by value. The principal at the end outweighs every coupon, which is why its bar is cut. "
            f"For a ten-year bond paying four and a half percent it is "
            f"{rows[0][2]:.2f} years, not ten, because the coupons pay you back along the way. <bookmark mark='b'/> A "
            "zero-coupon bond pays everything at the end, so its beam balances exactly at its maturity."
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
                why(r"Taylor's theorem to second order: the convexity $C = P''/P$ is the bend; it always helps a holder"),
                why(r"the desk's unit: dollars per basis point per 100 of face. Positions are added up in DV01s, not "
                    r"in face amounts")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "Now why the balance point matters. Write the price as a function of the yield. <bookmark mark='a'/> "
            "Differentiate: each payment's sensitivity to the yield is proportional to its time, so the slope of the "
            "price, per dollar of price, is that same value-weighted average time, divided by one plus half the yield. "
            "That is modified duration. <bookmark mark='b'/> To second order, the bend: convexity. A bond loses less "
            "when yields rise, and gains more when they fall, than the straight line says. <bookmark mark='c'/> On a "
            "desk all of this is quoted as DV01: the dollars a position makes or loses for one basis point."
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
        g = axes([0, 12], [40, 220], x_length=7.4, y_length=4.8, xlabel=r"yield, \%", ylabel=r"price of a 30-year, "
                 r"4\% bond", xticks=[0, 2, 4, 6, 8, 10, 12], yticks=[50, 100, 150, 200], font_size=14).to_edge(
            LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        P = np.asarray(c30["P"])
        m = (P > 40) & (P < 220)
        lp = curve(ax, ys[m], P[m], PAR, stroke_width=4)
        tg = np.asarray(c30["tangent"])
        mt = (tg > 40) & (tg < 220)
        lt = curve(ax, ys[mt], tg[mt], TAN, stroke_width=2.5)
        qd = np.asarray(c30["quad"])
        mq = (qd > 40) & (qd < 220)
        lq = DashedVMobject(curve(ax, ys[mq], qd[mq], CONV, stroke_width=2.5), num_dashes=50)
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
            "Here it is for a thirty-year bond paying four percent, priced at par. The curve is the exact price at "
            "every yield. <bookmark mark='a'/> Duration is the tangent at today's yield: "
            f"{c30['modified']:.1f} percent per point. <bookmark mark='b'/> The real price bends away from the "
            "tangent, above it on both sides; the parabola with convexity hugs it. <bookmark mark='c'/> If yields "
            f"rise a full point, the tangent predicts a loss of {abs(mv['+0.01']['duration']):.1f}; the bond actually "
            f"loses {abs(mv['+0.01']['exact']):.1f}. If they fall a point, it gains {mv['-0.01']['exact']:.1f}, not "
            f"{abs(mv['-0.01']['duration']):.1f}. Convexity is on the holder's side both ways."
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
        note_ = wrapped_label(r"SVB's held-to-maturity book: duration 6.2 years (Fed review); the 6-year zero yield's "
                              r"rise through 2022 from the Fed's curve; book value from the 10-K", 12.0, 19,
                              GREY_A).next_to(rows_g, DOWN, buff=0.4)
        with self.voiceover(
            "The desk question every rates interview starts with. A ten-year zero-coupon bond yields four percent. "
            f"Its price is {z['price']:.2f}; its Macaulay duration is ten, its modified duration ten over one point "
            f"oh four, {z['modified']:.2f}; so one basis point costs about six and a half cents per hundred. "
            "<bookmark mark='a'/> Now the hook. Silicon Valley Bank's held-to-maturity book had a duration of six "
            f"point two years. The six-year yield rose {v['dy6_2022_pct']:.2f} points in 2022. Duration times the "
            f"move times the book: about {v['est_loss']:.1f} billion dollars. <bookmark mark='b'/> The bank "
            f"reported {rep:.2f}, against equity of {eq:.2f}. One line of arithmetic, done in public, showed a bank "
            "that was, at market prices, nearly worthless."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(FadeIn(rows_g[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows_g[1]), FadeIn(note_))
        p = ask(r"two bonds have the same yield and duration; one has more convexity. Which should cost more, and why "
                r"does convexity cost money?")
        with self.voiceover("And one to think about. Two bonds with the same yield and duration, one more convex. Which "
                            "should cost more, and why does convexity cost money?"):
            self.play(FadeIn(p))
        self.wait(0.5)
        self.clear_scene()
