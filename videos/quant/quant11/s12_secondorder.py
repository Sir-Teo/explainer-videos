from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import bs
from videos.quant.quant11.common import (ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, axes3d, fixed, hint3d, load, pause,
                                         real_data, surf)

T30 = 30 / 365


def vega_pt(K, s):
    return float(bs.greeks(100.0, K, T30, s)["vega"]) / 100


class SecondOrder(VoiceoverScene, ThreeDScene):
    def construct(self):
        so = load("secondorder")
        self.card()
        self.vega_surface(so)
        self.derive(so)
        self.vv(so)
        self.weekly(so)

    def card(self):
        c = chapter_card(4, r"Vega, vanna, volga", r"What do the risk reversal and the butterfly price?", part=PART)
        with self.voiceover("Chapter four. Vega, vanna and volga: the risk reversal and the butterfly."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def vega_surface(self, so):
        ax = axes3d([60, 140, 20], [0.2, 1.0, 0.2], [0, 12, 4], x_length=7.6, y_length=5.0, z_length=3.2)
        sf = surf(ax, lambda K, s: vega_pt(K, s), (60, 140), (0.2, 1.0), [(QC.SPOT, 0.5), (VEGA, 5), (QC.LOSS, 11)],
                  resolution=(26, 18), opacity=0.7)
        s0 = 0.5
        kp = 100 * so["k25p"] / so["F"]
        kc = 100 * so["k25c"] / so["F"]
        flags = VGroup()
        for K, c in ((kp, QC.LOSS), (100.0, WHITE), (kc, QC.GAIN)):
            p = ax.c2p(K, s0, vega_pt(K, s0))
            flags.add(VGroup(Line(ax.c2p(K, s0, 0), p, color=c, stroke_width=3), Dot3D(p, radius=0.07, color=c)))
        ridge = VMobject(stroke_color=YELLOW, stroke_width=5).set_points_as_corners(
            [ax.c2p(100, s, vega_pt(100, s)) + OUT * 0.04 for s in np.linspace(0.2, 1.0, 30)])
        wing = VMobject(stroke_color=QC.GAIN, stroke_width=5).set_points_as_corners(
            [ax.c2p(kc, s, vega_pt(kc, s)) + OUT * 0.04 for s in np.linspace(0.2, 1.0, 30)])
        hint = hint3d((r"strike (spot 100)", SPOT), (r"implied volatility $\sigma$", VEGA),
                      (r"vega per vol point, 30 days", OPT))
        cap = VGroup(label(r"along $\sigma$ at the money: flat, volga $\approx 0$", font_size=21, color=YELLOW),
                     label(r"along $\sigma$ in a wing: rising, volga $> 0$", font_size=21, color=QC.GAIN),
                     label(r"across strikes: the tilt is vanna, opposite in the two wings", font_size=21, color=ALT),
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DL, buff=0.35)
        self.set_camera_orientation(phi=66 * DEGREES, theta=-58 * DEGREES, zoom=0.9)
        fixed(self, hint, cap)
        with self.voiceover(
            "Chapter one's Taylor series had two cross terms. To see them, draw vega itself as a surface, over the "
            "strike and the implied volatility, for a thirty-day option. <bookmark mark='a'/> Three flags: the "
            "twenty-five delta put, the at-the-money option, and the twenty-five delta call, the three options an "
            "options desk quotes a smile with. <bookmark mark='b'/> Walk along the volatility axis at the money, in "
            "yellow: vega barely changes. Its slope in volatility, volga, is close to zero. <bookmark mark='c'/> In "
            "the wings, in green, vega climbs as volatility rises: volga is positive, and a wing option gets longer "
            "volatility as volatility rises. <bookmark mark='d'/> And across the strikes, the surface tilts one way "
            "on the put side and the other on the call side: that tilt is vanna, how delta changes when volatility "
            "moves."
        ) as vo:
            self.play(Create(ax), FadeIn(hint), run_time=1.2)
            self.play(Create(sf), run_time=2.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(f_) for f_ in flags], lag_ratio=0.4, run_time=2))
            vo.wait_until("b")
            self.play(Create(ridge), FadeIn(cap[0]))
            vo.wait_until("c")
            self.play(Create(wing), FadeIn(cap[1]))
            vo.wait_until("d")
            self.play(FadeIn(cap[2]))
            self.move_camera(theta=-25 * DEGREES, phi=70 * DEGREES, run_time=max(vo.remaining(1.0) - 0.3, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, added_anims=[FadeOut(VGroup(ax, sf, flags, ridge, wing)),
                                                                             FadeOut(hint), FadeOut(cap)], run_time=1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self, so):
        rows = [
            cmath(r"\partial_\sigma d_1", r"=", r"-\frac{d_2}{\sigma}", font_size=38),
            cmath(r"\text{vanna} = \partial_\sigma \Delta", r"=", r"-\varphi(d_1)\,\frac{d_2}{\sigma},\qquad "
                  r"\text{volga} = \partial_\sigma \mathcal{V} = \mathcal{V}\,\frac{d_1 d_2}{\sigma}", font_size=34,
                  colors={r"\text{vanna} = \partial_\sigma \Delta": ALT}),
            cmath(r"d_1 d_2\big|_{K = F}", r"=", r"-\tfrac14\sigma^2\tau \approx 0;\qquad d_1 = \pm 0.674 "
                  r"\text{ at } 25\Delta \Rightarrow \text{volga} > 0", font_size=34),
            cmath(r"RR", r"=", r"\sigma_{25C} - \sigma_{25P},\qquad BF = \tfrac12(\sigma_{25C} + \sigma_{25P}) - "
                  r"\sigma_{\text{ATM}}", font_size=34, colors={r"RR": VEGA}),
        ]
        whys = [why(r"differentiate $d_1 = (\ln F/K + \tfrac12\sigma^2\tau)/(\sigma\sqrt\tau)$ in $\sigma$"),
                why(r"the chain rule on $\Delta = N(d_1)$ and on $\mathcal{V} = S\varphi(d_1)\sqrt\tau$"),
                why(r"at the money $d_1$ and $d_2$ straddle zero; at 25 delta both sit on the same side, about two "
                    r"thirds of a standard deviation out"),
                why(r"the market's quotes: the risk reversal is the price of vanna (it is long one wing, short the "
                    r"other), the butterfly the price of volga")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-0.4, buff=0.55, edge=6.9)
        pc = pause(r"Same vega: an at-the-money straddle, or a 25-delta strangle. Which has more volga?", width=5.0,
                   font_size=21)
        with self.voiceover(
            "The algebra is two lines. Differentiate d one in volatility: minus d two over sigma. "
            "<bookmark mark='a'/> The chain rule then gives vanna, minus the normal density times d two over sigma, "
            "and volga, vega times d one d two over sigma. <bookmark mark='b'/> At the money, d one and d two "
            "straddle zero and their product is tiny, so volga is almost zero, the flat yellow line. At twenty-five "
            "delta both sit about two thirds of a standard deviation out on the same side, and volga is positive. "
            "<bookmark mark='c'/> That is why desks quote the smile with two numbers besides the at-the-money "
            "volatility. The risk reversal, the call wing's volatility minus the put wing's, is long one wing and "
            "short the other: it is the market's price of vanna. The butterfly, the average wing minus the "
            "middle, is the price of volga. <bookmark mark='d'/> Pause and predict: for the same vega, which has more "
            "volga, a straddle or a strangle? The strangle: it is made of wings."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(pc))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vv(self, so):
        ks = np.asarray(so["ks"])
        vv, ss = np.asarray(so["vv"]), np.asarray(so["ssvi"])
        X = np.asarray(so["x"])
        F = so["F"]
        g = axes([-0.4, 0.4], [0.3, 0.75], x_length=6.6, y_length=3.6, xlabel=r"log-moneyness $\ln K/F$",
                 ylabel=r"30-day implied vol", xticks=[-0.4, -0.2, 0, 0.2, 0.4], yticks=[0.4, 0.5, 0.6, 0.7],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.6)
        ax = g.ax
        ls = curve(ax, ks, np.clip(ss, 0.3, 0.75), VEGA, stroke_width=3)
        kp, kc = np.log(so["k25p"] / F), np.log(so["k25c"] / F)
        pil = VGroup(*[Dot(ax.c2p(k, v), radius=0.08, color=c) for k, v, c in
                       ((kp, so["s25p"], QC.LOSS), (0.0, so["atm"], WHITE), (kc, so["s25c"], QC.GAIN))])
        tr = ValueTracker(0)
        lv = always_redraw(lambda: curve(ax, ks[:max(int(tr.get_value()), 2)],
                                         np.clip(vv[:max(int(tr.get_value()), 2)], 0.3, 0.75), OPT, stroke_width=4))
        # the pillar weights at the strike being priced, as three live bars
        wb = axes([0, 3], [-1.2, 1.6], x_length=3.0, y_length=2.0, ylabel=r"weights $x_i(K)$", yticks=[-1, 0, 1],
                  font_size=15).to_corner(UR, buff=0.5).shift(LEFT * 0.4)

        def wbars():
            i = int(np.clip(tr.get_value(), 0, len(ks) - 1))
            gr = VGroup()
            for j, c in enumerate((QC.LOSS, WHITE, QC.GAIN)):
                v = float(np.clip(X[i, j], -1.2, 1.6))
                a, b = wb.ax.c2p(j + 0.5, 0), wb.ax.c2p(j + 0.5, v)
                gr.add(Rectangle(width=0.5, height=max(abs(b[1] - a[1]), 0.01), stroke_width=0, fill_color=c,
                                 fill_opacity=0.85).move_to((a + b) / 2))
            return gr
        wbs = always_redraw(wbars)
        eq = MathTex(r"C^{VV}(K) = C^{BS}(K) + \sum_{i=1}^{3} x_i(K)\left[C_i^{\text{mkt}} - C_i^{BS}\right]",
                     font_size=30).to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.5)
        eq2 = MathTex(r"\sum_i x_i\,(\mathcal{V}_i, \text{vanna}_i, \text{volga}_i) = (\mathcal{V}, \text{vanna}, "
                      r"\text{volga})(K)", font_size=26, color=GREY_A).next_to(eq, DOWN, buff=0.15).align_to(eq, LEFT)
        good = so["rmse_in"] < 1.0
        verdict = (rf"between the 10-delta strikes: within {so['rmse_in']:.2f} vol points of the fitted smile; in the "
                   rf"far wings, off by up to {so['maxerr_wing']:.0f}" if good else
                   rf"between the 10-delta strikes: off by {so['rmse_in']:.1f} vol points")
        side = VGroup(
            label(rf"RR $= {100 * so['rr']:+.1f}$, BF $= {100 * so['bf']:+.1f}$ vol points", font_size=22, color=VEGA),
            wrapped_label(verdict, 4.2, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(wb, DOWN, buff=0.35).align_to(wb, LEFT).shift(LEFT * 0.6)
        leg = legend([(VEGA, r"the SSVI smile (Part 12)"), (OPT, r"vanna--volga from three quotes")],
                     font_size=17).next_to(g, UP, buff=0.05).align_to(g, RIGHT)
        src = real_data(r"the Surface, 10 December 2025: 25-delta strikes solved on the SSVI smile")
        vsay = (f"Between the ten-delta strikes the rebuilt smile sits within {so['rmse_in']:.2f} volatility points of "
                f"the fitted one; out in the far wings it misses by up to {so['maxerr_wing']:.0f}." if good else
                f"Here it misses by {so['rmse_in']:.1f} volatility points even between the ten-delta strikes.")
        with self.voiceover(
            "Can three quotes rebuild a whole smile? That is the vanna-volga method, the foreign-exchange desks' "
            "workhorse, written down by Antonio Castagna and Fabio Mercurio in 2007. Price every strike at the flat "
            "at-the-money volatility, then add a hedge: amounts of the three pillar options chosen so that, together, "
            "they have the strike's own vega, vanna and volga. <bookmark mark='a'/> Each strike gets three weights, "
            "solved from a three by three system; here they are, sweeping across the strikes, and the price "
            "correction they carry becomes the magenta smile. <bookmark mark='b'/> On the Surface day the risk "
            f"reversal was {100 * so['rr']:+.1f} points and the butterfly {100 * so['bf']:+.1f}. {vsay} Three numbers "
            "carry most of a smile; the wings need more."
        ) as vo:
            self.play(FadeIn(eq), FadeIn(eq2), FadeIn(g), FadeIn(src), Create(ls), FadeIn(leg[0]))
            self.play(FadeIn(pil), FadeIn(wb))
            vo.wait_until("a")
            self.add(lv, wbs)
            self.play(tr.animate.set_value(len(ks) - 1), FadeIn(leg[1]), run_time=vo.until("b"), rate_func=linear)
            self.play(FadeIn(side))
        lv.clear_updaters()
        wbs.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def weekly(self, so):
        rr, bf = np.asarray(so["weekly_rr"]) * 100, np.asarray(so["weekly_bf"]) * 100
        S = np.asarray(so["weekly_S"]) / 1000
        n = len(rr)
        x = np.arange(n)
        g1 = axes([0, n], [30, 130], x_length=8.2, y_length=1.8, ylabel=r"bitcoin, thousand dollars", yticks=[50, 100],
                  font_size=15)
        g2 = axes([0, n], [-12, 8], x_length=8.2, y_length=2.6, xlabel=r"weeks from January 2024 (Wednesdays)",
                  ylabel=r"30-day risk reversal and butterfly, vol points", xticks=[0, 25, 50, 75, 100],
                  yticks=[-10, -5, 0, 5], font_size=15)
        VGroup(g1, g2).arrange(DOWN, buff=0.4).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        tr = ValueTracker(0.0)
        l1 = tracing(g1.ax, x, S, tr, SPOT, stroke_width=2.5)
        l2 = tracing(g2.ax, x, np.clip(rr, -12, 8), tr, VEGA, stroke_width=3)
        l3 = tracing(g2.ax, x, np.clip(bf, -12, 8), tr, ALT, stroke_width=2.5)
        z = DashedLine(g2.ax.c2p(0, 0), g2.ax.c2p(n, 0), color=GREY_C, stroke_width=1.5)
        leg = legend([(VEGA, r"risk reversal (call wing $-$ put wing)"), (ALT, r"butterfly")], font_size=17).next_to(
            g2, UP, buff=0.02).align_to(g2, RIGHT)
        share = so["share_rr_neg"]
        verdict = (rf"put skew (RR $< 0$) in only {100 * share:.0f}\% of weeks: in 2024--25 bitcoin's smile leaned to "
                   r"the calls in rallies" if share < 0.5 else rf"put skew in {100 * share:.0f}\% of weeks")
        side = VGroup(wrapped_label(verdict, 3.8, 20, VEGA),
                      wrapped_label(rf"the butterfly averaged {100 * so['bf_mean']:+.1f} points: the wings always cost "
                                    r"more than the middle", 3.8, 20, ALT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        side.to_edge(RIGHT, buff=0.4)
        src = real_data(r"Part 12's weekly Deribit smiles (SSVI), 2024--2025; Binance")
        wsay = (f"Unlike an equity index, whose puts are always dearer, Bitcoin's risk reversal was negative in only "
                f"{100 * share:.0f} percent of these weeks: in rallies the market paid up for calls." if share < 0.5
                else f"Like an equity index, Bitcoin's risk reversal was negative in {100 * share:.0f} percent of weeks.")
        with self.voiceover(
            "Now two years of these two numbers, every Wednesday, under Bitcoin's price. <bookmark mark='a'/> "
            f"{wsay} The butterfly stayed positive: the wings always cost more than the middle. A trader who sells a "
            "risk reversal is selling vanna; one who sells a butterfly is selling volga. Part twelve models how the "
            "whole smile moves."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), Create(z), FadeIn(leg), FadeIn(src))
            self.add(l1, l2, l3)
            self.play(tr.animate.set_value(n - 1), run_time=vo.until("a") + 3, rate_func=linear)
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()
