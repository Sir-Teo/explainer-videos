from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import rates as R
from videos.quant.quant18.common import BAD, GOOD, PAR, PART, ZERO, ask, illustration, load, surf3d_axes

KEYS = [0.5, 2, 5, 10, 30]


class Immunize(VoiceoverScene, ThreeDScene):
    def construct(self):
        cd = load("curve_day")["20251231"]
        im = load("immunize")
        self.card()
        self.keyrates(cd)
        self.redington(im)
        self.surface(im)

    def card(self):
        c = chapter_card(7, r"Key rates and immunization", r"Is one duration number enough?", part=PART)
        with self.voiceover("Chapter seven. Key rates, and immunizing a pension fund."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def keyrates(self, cd):
        cv = R.Curve(cd["nodes_t"], cd["nodes_z"])

        def note_cf(cpn, T):
            t = np.arange(1, int(2 * T) + 1) / 2
            cf = np.full(len(t), 100 * cpn / 2)
            cf[-1] += 100
            return t, cf
        t10, c10 = note_cf(0.04, 10)
        t2, c2 = note_cf(0.035, 2)
        k10 = R.key_rate_dv01(t10, c10, cv, KEYS)
        k2 = R.key_rate_dv01(t2, c2, cv, KEYS)
        ratio = k10.sum() / k2.sum()
        steep = ratio * k2 - k10
        g = axes([-0.5, 4.5], [-0.1, 0.1], x_length=6.0, y_length=4.2, ylabel=r"DV01 per 100 of the 10-year, \$",
                 xticks=[0, 1, 2, 3, 4], xfmt=lambda v: f"{KEYS[int(v)]:g}\\,\\text{{y}}", yticks=[-0.08, 0, 0.08],
                 font_size=14).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax

        def bars(vals, col, dx=0.0):
            out = VGroup()
            for i, v in enumerate(vals):
                p0, p1 = ax.c2p(i - 0.18 + dx, 0), ax.c2p(i + 0.18 + dx, v)
                h = abs(p1[1] - p0[1])
                out.add(Rectangle(width=p1[0] - p0[0], height=h, stroke_width=0, fill_color=col,
                                  fill_opacity=0.85).move_to([(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0]))
            return out
        b10 = bars(k10, PAR)
        bst = bars(steep, QC.OPTION)
        zero = Line(ax.c2p(-0.5, 0), ax.c2p(4.5, 0), color=GREY_C, stroke_width=1.5)
        side = VGroup(
            label(r"lower one key zero rate by 1 bp, fading to zero at its neighbours", font_size=19, color=GREY_A),
            MathTex(rf"\text{{10-year: }}\sum \text{{key-bump gains}} = {k10.sum():.4f}", font_size=28, color=PAR),
            label(r"a DV01-neutral 2s10s steepener:", font_size=19, color=GREY_A),
            MathTex(rf"\text{{long }}{ratio:.2f}\times\text{{ the 2-year, short the 10-year}}", font_size=26,
                    color=QC.OPTION),
            MathTex(rf"\sum\text{{key-bump gains}} \approx {float(round(steep.sum(), 4)) + 0.0:.4f}", font_size=28, color=QC.OPTION),
            wrapped_label(r"the displayed aggregate key-bump sum cancels, but curve-shape risk remains. Parallel cancellation is first order; convexity, carry and funding can still create P\&L", 5.0, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            f"A key-rate report specifies a local curve perturbation. Here each zero-rate key is lowered one basis point, with a triangular weight fading to zero at its neighbours. These are one-sided finite bump gains. <bookmark mark='a'/> Their sum approximates the ten-year note's parallel sensitivity; finite-bump convexity means it is not an exact derivative identity. Coupon dates distribute some risk across earlier keys. <bookmark mark='b'/> Buying {ratio:.2f} units of the two-year note against one short ten-year note cancels this displayed aggregate key-bump sum by construction. That does not make the portfolio riskless or give it zero profit for every parallel move. It retains curve-shape, higher-order, carry and funding effects. Its direction benefits locally from short yields falling relative to long yields under the specified bumps."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b10], lag_ratio=0.2), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(ReplacementTransform(b10, bst), LaggedStart(*[FadeIn(s_) for s_ in side[2:]], lag_ratio=0.4),
                      run_time=2.5)
        self.add(illustration(r"31 December 2025 curve; 4\% 10y and 3.5\% 2y notes; one-sided key bumps, approximate parallel aggregation"))
        self.wait(0.4)
        self.clear_scene()

    def redington(self, im):
        sh = np.asarray(im["shifts"]) * 100
        par, tw = np.asarray(im["par"]), np.asarray(im["twist"])
        rows = [cmath(r"\text{PV}_A", r"=", r"\text{PV}_L", font_size=40, colors={r"\text{PV}_A": PAR}),
                cmath(r"D_A", r"=", r"D_L", font_size=40, colors={r"D_A": PAR}),
                cmath(r"C_A", r">", r"C_L", font_size=40, colors={r"C_A": GOOD})]
        whys = [why(r"Redington (1952): hold assets worth the liabilities"),
                why(r"with the same duration, so a small parallel move changes both by the same amount"),
                why(rf"strictly greater convexity gives a local surplus under the scalar-yield assumptions; here {im['convexity_assets']:.0f} "
                    rf"against {im['convexity_liab']:.0f}")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-4.6, buff=0.45, edge=6.9)
        g = axes([-3, 3], [-15, 60], x_length=7.0, y_length=4.4, xlabel=r"parallel $a$ or twist $b$, percentage points",
                 ylabel=r"surplus PV, dollars", xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[-10, 0, 20, 40, 60],
                 font_size=13).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        lp = curve(ax, sh, par, GOOD, stroke_width=3)
        lt = curve(ax, sh, tw, BAD, stroke_width=3)
        leg = legend([(GOOD, r"parallel shift"), (BAD, r"a twist about 15 years")], font_size=17).next_to(g, RIGHT,
                                                                                                       buff=0.4)
        k = int(np.argmin(np.abs(sh + 1)))
        head = wrapped_label(r"Fixed zero-coupon example: $\Delta z(T)=a+b(15-T)/10$, with $a,b$ in decimal rates", 12.3, 22).to_edge(UP, buff=0.3)
        info = wrapped_label(rf"100 due in 15 years, initial PV {im['L']:.1f}; 60\% of asset PV in 5y zeros and 40\% in 30y zeros. For $b=-1$ percentage point: 5y rates fall 1 point and 30y rates rise 1.5 points. Surplus falls {abs(tw[k]):.2f}, or {100 * abs(tw[k]) / im['L']:.1f}\% of initial liability PV.", 4.4, 17, GREY_A).next_to(leg, DOWN, buff=0.3, aligned_edge=LEFT)
        info.shift(LEFT * max(0.0, info.get_right()[0] - 6.75))
        with self.voiceover(
            f"Redington's static immunization conditions match present values, <bookmark mark='a'/> match duration with respect to a specified common yield shift, <bookmark mark='b'/> and give assets strictly greater convexity. With suitable smoothness this makes surplus locally nonnegative for small parallel shifts. It is not a general guarantee for every finite curve move. <bookmark mark='c'/> This particular fixed-cash-flow example is stronger: positive five- and thirty-year zero holdings have value weights sixty and forty percent, with mean maturity fifteen. Convexity of the exponential and Jensen's inequality give nonnegative surplus for any parallel shift in this special model. The full plotted parallel and twist values are retained. <bookmark mark='d'/> A twist is different. Our parameter b changes the five-year yield by b and the thirty-year yield by minus one-and-a-half b. For b equal to minus one percentage point, short rates fall one point and long rates rise one-and-a-half. The shortfall is {abs(tw[k]):.2f} dollars, {100 * abs(tw[k]) / im['L']:.1f} percent of initial liability value. Neither the local theorem nor this special parallel-shift result removes twist risk."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.clear_scene()
            self.play(FadeIn(head), FadeIn(g), Create(lp), FadeIn(leg[0]), run_time=2)
            vo.wait_until("d")
            self.play(Create(lt), FadeIn(leg[1]), FadeIn(info), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def surface(self, im):
        S, Tw, Z = np.asarray(im["S"]) * 100, np.asarray(im["Tw"]) * 100, np.asarray(im["surf"])
        ax = surf3d_axes([-3, 3, 1], [-2, 2, 1], [-25, 85, 20], x_length=6.0, y_length=4.6, z_length=3.4)
        ax.shift(RIGHT * 1.0 + DOWN * 0.3)
        from videos.quant.quant18.common import grid_fn
        f = grid_fn(S, Tw, Z)
        surf = Surface(lambda u, v: ax.c2p(u, v, f(u, v)), u_range=(-3, 3), v_range=(-2, 2), resolution=(24, 24),
                       fill_opacity=0.75, stroke_width=0.4, stroke_color=GREY_D, checkerboard_colors=False)
        for face in surf:
            zc = ax.p2c(face.get_center())[2]
            face.set_fill(GOOD if zc >= 0 else BAD, opacity=0.75)
        zero = Surface(lambda u, v: ax.c2p(u, v, 0), u_range=(-3, 3), v_range=(-2, 2), resolution=(2, 2),
                       fill_color=WHITE, fill_opacity=0.12, stroke_width=0, checkerboard_colors=False)
        key = VGroup(wrapped_label(r"parallel a $\pm3$ percentage points (across); twist b $\pm2$ points (back); surplus PV, dollars (up); full 25 by 25 grid", 12.2, 18, GREY_A),
                     legend([(GOOD, r"surplus"), (BAD, r"shortfall")], font_size=17)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.3)
        self.set_camera_orientation(phi=65 * DEGREES, theta=-55 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(key)
        self.remove(key)
        with self.voiceover(
            "The surface uses all values on the saved twenty-five-by-twenty-five shock grid, with interpolation between nodes. Its axes are the parallel parameter a, the twist parameter b defined earlier, and present-value surplus in dollars. Along zero twist, the special positive barbell has nonnegative parallel-shift surplus. <bookmark mark='a'/> With twists, regions of shortfall appear despite matched present value and duration. Matching a finite set of key-rate sensitivities can cancel selected first-order risks; it does not generally close the whole nonlinear shortfall surface. Exact matching of fixed dated asset and liability cash flows under the same credit, currency and discounting assumptions is a stronger condition. No universal worst curve move exists without specifying a shock set or size constraint."
        ) as vo:
            self.play(Create(ax), FadeIn(key))
            self.play(FadeIn(zero), Create(surf), run_time=2.5)
            vo.wait_until("a")
            self.move_camera(theta=-130 * DEGREES, phi=70 * DEGREES, run_time=6)
        q = ask(r"On this specified shock grid, which twist directions produce a shortfall despite parallel immunization?")
        self.add_fixed_in_frame_mobjects(q)
        self.remove(q)
        with self.voiceover('On the specified displayed shock grid, which twist directions produce a shortfall? Explain why parallel immunization does not control them.'):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=0.5)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0, zoom=1.0, frame_center=ORIGIN)
