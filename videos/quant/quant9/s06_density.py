from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.zh_text import verbatim
from videos.quant.quant9.common import (ALT, ARB, CALL, FWD, PART, PUT, Q_C, answer_under, load, pause_at, real_data)


class Density(VoiceoverScene):
    def construct(self):
        b, d = load("butterflies"), load("density")
        self.card()
        self.fly()
        self.histogram(b, d)
        self.formula()
        self.slider(b, d)
        self.lab(b)
        self.predict()

    def card(self):
        c = chapter_card(12, r"Butterflies build the density", r"What does the market think could happen?",
                         part=PART)
        with self.voiceover("Chapter twelve. Butterflies build the density."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def fly(self):
        K, h = 100.0, 10.0
        g = axes([70, 130], [-22, 42], x_length=6.2, y_length=4.2, xlabel=r"price at expiry", ylabel=r"payoff",
                 xticks=[90, 100, 110], yticks=[-20, 0, 20, 40], font_size=17)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        xs = np.linspace(70, 130, 241)
        legs = [np.maximum(xs - (K - h), 0), -2 * np.maximum(xs - K, 0), np.maximum(xs - (K + h), 0)]
        cum = np.cumsum(legs, axis=0)
        c1 = curve(ax, xs, cum[0], CALL, stroke_width=4)
        c2 = curve(ax, xs, cum[1], ALT, stroke_width=4)
        c3 = curve(ax, xs, cum[2], Q_C, stroke_width=5)
        tri = Polygon(ax.c2p(90, 0), ax.c2p(100, 10), ax.c2p(110, 0), stroke_width=0, fill_color=Q_C, fill_opacity=0.3)
        side = VGroup(
            MathTex(r"C(K - h) - 2C(K) + C(K + h)", font_size=34, color=Q_C),
            wrapped_label(r"buy a call below, sell two at the strike, buy one above: a tent of height $h$ around $K$, "
                          r"never negative", 4.8, 21, GREY_A),
            wrapped_label(r"it pays only if the price ends near $K$: its price is what the market charges for "
                          r"``ending in this bin'', a state price", 4.8, 21, Q_C),
            wrapped_label(r"so it can never cost less than nothing: that would be an arbitrage", 4.8, 21, ARB),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "Chapter five's state price can be bought with calls. Buy one at ninety. <bookmark "
            "mark='a'/> Sell two at a hundred. <bookmark mark='b'/> Buy one at a hundred and ten: a "
            "tent, the butterfly, paying only near a hundred. <bookmark mark='c'/> Its price is the "
            "price of ending in that bin: a state price, and never below zero."
            " Divided by h squared, the tent has area one: a little bar of a histogram, which is why "
            "bars of different widths can be compared."
        ) as vo:
            self.play(FadeIn(g), Create(c1), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(ReplacementTransform(c1, c2))
            vo.wait_until("b")
            self.play(ReplacementTransform(c2, c3), FadeIn(tri), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def histogram(self, b, d):
        F = b["F"]
        e = d["expiries"][0]
        K, q = np.asarray(e["K"]), np.asarray(e["density"])
        ok = (K > 0.7 * F) & (K < 1.3 * F)
        top = q[ok].max() * 1.15
        g = axes([0.7 * F, 1.3 * F], [0, top], x_length=8.0, y_length=4.4, xlabel=r"bitcoin price at expiry (\$)",
                 ylabel=r"butterfly price $/\,h^2$", xticks=[70000, 80000, 90000, 100000, 110000, 120000],
                 xfmt=lambda u: f"{u / 1000:.0f}k", yticks=[], font_size=16)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        widths = ["8000", "4000", "2000", "1000", "500"]

        def bars(hs):
            fl = b["flies"][hs]
            h = float(hs)
            out = VGroup()
            for k_, v in zip(fl["K"], fl["q"]):
                if not (0.7 * F + h / 2 <= k_ <= 1.3 * F - h / 2):
                    continue
                hgt = max(ax.c2p(0, max(v, 0))[1] - ax.c2p(0, 0)[1], 0.005)
                wdt = ax.c2p(h, 0)[0] - ax.c2p(0, 0)[0]
                out.add(Rectangle(width=wdt * 0.92, height=hgt, stroke_width=0, fill_color=Q_C,
                                  fill_opacity=0.6).move_to(ax.c2p(k_, max(v, 0) / 2)))
            return out

        B = bars(widths[0])
        bl = curve(ax, K[ok], q[ok], WHITE, stroke_width=3)
        hl = ValueTracker(8000)
        hd = DecimalNumber(8000, num_decimal_places=0, group_with_commas=False, font_size=30, color=Q_C)
        hd.add_updater(lambda m: m.set_value(hl.get_value()))
        hr = VGroup(label(r"butterfly width $h$, dollars:", font_size=22, color=Q_C), hd).arrange(RIGHT, buff=0.15)
        hr.to_corner(UR, buff=0.4)
        side = VGroup(
            wrapped_label(r"one butterfly per bin, each priced off the Surface's fitted calls, divided by $h^2$", 4.0,
                          19, GREY_A),
            wrapped_label(r"white: Breeden and Litzenberger's density, the limit as $h \to 0$", 4.0, 19, WHITE),
            MathTex(rf"\int q = {b['mass']:.5f},\quad \int s\, q = " + f"{b['mean']:,.0f}".replace(",", "{,}"), font_size=24,
                    color=Q_C),
            MathTex(rf"F = {F:,.0f}".replace(",", "{,}"), font_size=24, color=FWD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(hr, DOWN, buff=0.35).align_to(hr, LEFT)
        src = real_data(rf"the Surface, expiry {b['expiry']}, {b['T'] * 365:.0f} days")
        with self.voiceover(
            f"Tile the strike axis with butterflies on the Surface, sixteen days out. Each bar is a butterfly's price over its width squared. <bookmark mark='a'/> Halve the width, and again: the bars thin and their tops converge to a smooth curve. <bookmark mark='b'/> The risk-neutral density, Breeden and Litzenberger's limit of 1978. It integrates to {b['mass']:.5f}, and its mean, {b['mean']:,.0f} dollars, is the forward. The identity uses call prices; this numerical reconstruction also uses the fitted SVI specification. The derivative identity is model independent, but these calls are interpolated and extrapolated with SVI. Finite quotes alone do not uniquely determine a density. We use zero discounting for this illustration. Here the Surface dollar curves are undiscounted forward values: inverse Bitcoin premiums times the fitted forward. They are not spot-dollar premiums. A dollar present value also needs the dollar discount factor."
        ) as vo:
            self.play(FadeIn(g), FadeIn(B), FadeIn(hr), FadeIn(side[0]), FadeIn(src))
            vo.wait_until("a")
            for hs in widths[1:]:
                self.play(Transform(B, bars(hs)), hl.animate.set_value(float(hs)), run_time=1.3)
            vo.wait_until("b")
            self.play(Create(bl), FadeIn(side[1]))
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        hd.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def formula(self):
        rows = [cmath(r"C(K)", r"=", r"e^{-rT}\int_K^\infty (s - K)\, q(s)\, ds", font_size=36, colors={r"C(K)": CALL}),
                cmath(r"\frac{\partial C}{\partial K}", r"=", r"-e^{-rT}\int_K^\infty q(s)\, ds = -e^{-rT}\,Q(S_T > K)",
                      font_size=34),
                cmath(r"\frac{\partial^2 C}{\partial K^2}", r"=", r"e^{-rT} q(K)", font_size=38, colors={r"e^{-rT} q(K)": Q_C}),
                cmath(r"\frac{C(K - h) - 2C(K) + C(K + h)}{h^2}", r"\to", r"\frac{\partial^2 C}{\partial K^2}",
                      font_size=34),
                cmath(r"q \ge 0", r"\iff", r"C\ \text{convex};\quad 0 \le Q(S_T > K) \le 1 \iff -e^{-rT} \le C' \le 0",
                      font_size=32, colors={r"q \ge 0": Q_C})]
        whys = [why(r"a call is the discounted $Q$-expectation of its payoff", 21),
                why(r"differentiate under the integral (Leibniz); the boundary term vanishes at $s = K$: a digital", 21),
                why(r"once more: the density (Breeden and Litzenberger 1978)", 21),
                why(r"Taylor: the butterfly is the second difference", 21),
                why(r"necessary shape conditions: decreasing, convex calls with slopes in $[-e^{-rT},0]$; add payoff bounds and correct endpoint limits for a full characterization", 21)]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-0.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "The proof is two derivatives. A call is the discounted expectation of its payoff. <bookmark mark='a'/> Differentiate in the strike: minus the discounted probability of ending above it, a digital's price. <bookmark mark='b'/> Again: the density. <bookmark mark='c'/> And the butterfly over h squared is the second difference, so it converges to it. <bookmark mark='d'/> Necessary static no-arbitrage shape conditions are: calls fall with the strike, their slope is bounded below by minus the discount factor, and they are convex. A worked example: if the call spread between strikes ninety-nine and a hundred and one costs one point one, the probability of finishing above a hundred is about one point one over two, point five five, before discounting. These density formulas assume an absolutely continuous terminal law and enough smoothness. In general the second strike derivative is a measure, and at atoms the digital uses one-sided derivatives. Decreasing convex calls and slope bounds also need the payoff bounds and correct endpoint limits for a full static no-arbitrage characterization. In the call-spread example divide by the discount factor to infer a probability."
        ) as vo:
            step(0, run_time=0.15)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.3)
        self.clear_scene()

    def slider(self, b, d):
        F = b["F"]
        Kf, Cf, dig = np.asarray(b["Kf"]), np.asarray(b["Cf"]), np.asarray(b["digital"])
        e = d["expiries"][0]
        K, q = np.asarray(e["K"]), np.asarray(e["density"])
        g1 = axes([0.75 * F, 1.3 * F], [0, Cf[Kf >= 0.75 * F].max() * 1.05], x_length=6.4, y_length=2.7,
                  ylabel=r"forward call value $C(K)$ (\$)", xticks=[], yticks=[0, 10000, 20000], yfmt=lambda u: f"{u / 1000:.0f}k",
                  font_size=15)
        ok = (K > 0.75 * F) & (K < 1.3 * F)
        g2 = axes([0.75 * F, 1.3 * F], [0, q[ok].max() * 1.15], x_length=6.4, y_length=2.4, ylabel=r"density $q(K)$",
                  xlabel=r"strike $K$", xticks=[80000, 100000, 120000], xfmt=lambda u: f"{u / 1000:.0f}k", yticks=[],
                  font_size=15)
        VGroup(g1, g2).arrange(DOWN, buff=0.4).to_edge(LEFT, buff=0.7).shift(DOWN * 0.1)
        sel = (Kf >= 0.75 * F) & (Kf <= 1.3 * F)
        cc = curve(g1.ax, Kf[sel], Cf[sel], CALL, stroke_width=4)
        dc = curve(g2.ax, K[ok], q[ok], Q_C, stroke_width=4)
        k = ValueTracker(0.85 * F)

        def tangent():
            x = k.get_value()
            c = np.interp(x, Kf, Cf)
            s = -np.interp(x, Kf, dig)
            dx = 0.08 * F
            return VGroup(Line(g1.ax.c2p(x - dx, c - s * dx), g1.ax.c2p(x + dx, c + s * dx), color=ALT, stroke_width=3),
                          Dot(g1.ax.c2p(x, c), radius=0.07, color=ALT),
                          DashedLine(g1.ax.c2p(x, 0), g2.ax.c2p(x, 0), color=GREY_C, stroke_width=1),
                          Dot(g2.ax.c2p(x, np.interp(x, K, q)), radius=0.08, color=Q_C))

        TG = always_redraw(tangent)
        r1 = DecimalNumber(0.5, num_decimal_places=3, font_size=30, color=ALT)
        r1.add_updater(lambda m: m.set_value(float(np.interp(k.get_value(), Kf, dig))))
        r2 = DecimalNumber(1.0, num_decimal_places=2, font_size=30, color=Q_C)
        r2.add_updater(lambda m: m.set_value(float(np.interp(k.get_value(), K, q)) * 1e5))
        side = VGroup(
            VGroup(label(r"minus the slope, $Q(S_T > K)$:", font_size=21, color=ALT), r1).arrange(RIGHT, buff=0.15),
            VGroup(label(r"the curvature, $q(K)$, per \$100{,}000:", font_size=21, color=Q_C), r2).arrange(RIGHT,
                                                                                                         buff=0.15),
            wrapped_label(r"the slope of the call curve is a digital's price; its bend is the density. Where the "
                          r"curve is straightest, the market sees the least probability", 4.4, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Both derivatives on the real call curve: the tangent's slope is the probability of "
            "ending above the strike, the bend is the density. <bookmark mark='a'/> Slide the strike "
            "up: the probability falls fastest where the curve bends most, near the forward; far out, "
            "the curve is straight and the market sees almost nothing."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), Create(cc), Create(dc))
            self.add(TG)
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(k.animate.set_value(1.25 * F), FadeIn(side[2]), run_time=max(vo.remaining(1.0) - 0.5, 4.0),
                      rate_func=linear)
        for m in (TG, r1, r2):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def lab(self, b):
        with verbatim():
            card = lab_card(r"the static checks", [
                "def static_checks(K, C, F, df=1.0, tol=1e-10):",
                "    o = argsort(K); K, C = K[o], C[o]",
                "    slope = diff(C) / diff(K)",
                "    mono  = where(slope > tol)            # call spread < 0",
                "    steep = where(slope < -df - tol)      # steeper than the bond",
                "    fly   = where(diff(slope) < -tol)     # butterfly < 0",
                "    lo = where(C < df * maximum(F - K, 0) - tol)",
                "    hi = where(C > df * F + tol)",
                "    return dict(monotone=mono, butterfly=fly, ...)",
            ], source="explainer/quant/house/arbitrage.py", width=7.6, font_size=17).to_edge(UP, buff=0.4)
        n = len(b["K_raw"])
        outs = [f"static_checks(raw trades, {n} strikes): butterfly={b['raw_fly']}  monotone={b['raw_mono']}",
                f"static_checks(Surface quotes): butterfly={b['mark_fly']}  monotone={b['mark_mono']}",
                f"static_checks(SVI fit, 901 strikes): butterfly={b['svi_fly']}  ok={b['svi_ok']}"]
        verdict = ("Raw prices fail. " if b["raw_fly"] > 0 else "Even the raw prices pass. ")
        with self.voiceover(
            "The House checks these conditions on every surface: positive slopes are call spreads "
            "with negative prices; falling slopes are negative butterflies. <bookmark mark='a'/> On "
            f"the sixteen-day expiry: on {n} strikes from raw trades, {b['raw_fly']} negative "
            f"butterflies; on the Surface's median quotes, {b['mark_fly']}; on the fitted smile, "
            f"{b['svi_fly']}. <bookmark mark='b'/> "
            f"{verdict}"
            "Not free money: the trades come at different moments, inside a bid-ask spread several "
            "butterflies wide. So the House never differentiates raw prices; it fits first."
            " Seven among forty sounds alarming, but neighbouring strikes trade minutes apart, and far "
            "from the money the bid-ask spread is a large fraction of the price."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            with verbatim():
                lab_run(self, card, outs, run_time=2.4, font_size=17)
        self.wait(0.5)
        self.clear_scene()

    def predict(self):
        card = pause_at(r"A butterfly on the screen is offered at $-0.1$: you are paid to take it. What do you trade, "
                        r"and what could go wrong?")
        with self.voiceover(
            "Pause and predict. A butterfly is offered at minus point one. What do you trade, and "
            "what can go wrong? <bookmark mark='a'/> Buy it: you are paid to own a payoff that is "
            "never negative. The risk is execution: all three legs at those prices at once."
            " Next: the density on the real Surface."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, r"buy it: paid 0.1 to own a non-negative payoff; the risk is legging "
                                                r"in: all three prices must be live at once")))
        self.wait(0.4)
        self.clear_scene()
