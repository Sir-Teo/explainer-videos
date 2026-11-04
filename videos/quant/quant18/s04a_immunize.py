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
        c = chapter_card(7, r"Key rates and immunization", r"Is one duration number enough?", lit=(1952,), part=PART)
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
                out.add(Rectangle(width=p1[0] - p0[0], height=max(h, 0.01), stroke_width=0, fill_color=col,
                                  fill_opacity=0.85).move_to([(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0]))
            return out
        b10 = bars(k10, PAR)
        bst = bars(steep, QC.OPTION)
        zero = Line(ax.c2p(-0.5, 0), ax.c2p(4.5, 0), color=GREY_C, stroke_width=1.5)
        side = VGroup(
            label(r"bump one key rate by 1 bp, fading to zero at its neighbours", font_size=19, color=GREY_A),
            MathTex(rf"\text{{10-year note: }}\sum \text{{key DV01s}} = {k10.sum():.4f}", font_size=28, color=PAR),
            label(r"a DV01-neutral 2s10s steepener:", font_size=19, color=GREY_A),
            MathTex(rf"\text{{long }}{ratio:.2f}\times\text{{ the 2-year, short the 10-year}}", font_size=26,
                    color=QC.OPTION),
            MathTex(rf"\text{{parallel DV01}} = {steep.sum():+.4f}", font_size=28, color=QC.OPTION),
            wrapped_label(r"zero in one number, large in two: it makes money if the 2-year falls against the "
                          r"10-year, and nothing if both move together", 5.0, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "One duration number assumes the whole curve moves in parallel. It does not. So desks bump one point of "
            "the curve at a time, a key rate, letting the bump fade to zero at the neighbouring key rates. "
            "<bookmark mark='a'/> A ten-year note's risk sits almost all at the ten-year key; the key-rate DV01s add "
            "up to its ordinary DV01. <bookmark mark='b'/> Now a classic curve trade: buy the two-year and sell the "
            f"ten-year, {ratio:.1f} times as much two-year so the DV01s cancel. Its duration is zero. Its key-rate "
            "risk is not: it gains if two-year yields fall relative to ten-year ones, a steepening, and has no "
            "exposure if both move together. One number would have called it riskless."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b10], lag_ratio=0.2), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(ReplacementTransform(b10, bst), LaggedStart(*[FadeIn(s_) for s_ in side[2:]], lag_ratio=0.4),
                      run_time=2.5)
        self.add(illustration(r"curve: 31 December 2025; notes: 4\% 10-year, 3.5\% 2-year"))
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
                why(rf"and more convexity, so any parallel move leaves a surplus: here {im['convexity_assets']:.0f} "
                    rf"against {im['convexity_liab']:.0f}")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-4.6, buff=0.45, edge=6.9)
        g = axes([-3, 3], [-12, 12], x_length=6.4, y_length=3.4, xlabel=r"move, percentage points",
                 ylabel=r"surplus, per liability of $L$", xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[-10, 0, 10],
                 font_size=13).to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.8)
        ax = g.ax
        lp = curve(ax, sh, np.clip(par, -12, 12), GOOD, stroke_width=3)
        lt = curve(ax, sh, np.clip(tw, -12, 12), BAD, stroke_width=3)
        leg = legend([(GOOD, r"parallel shift"), (BAD, r"a twist about 15 years")], font_size=17).next_to(g, RIGHT,
                                                                                                       buff=0.4)
        k = int(np.argmin(np.abs(sh + 1)))
        info = wrapped_label(rf"a liability of 100 due in 15 years (PV {im['L']:.1f}), funded {100 * (1 - im['w2']):.0f}"
                             rf"\% with 5-year and {100 * im['w2']:.0f}\% with 30-year zeros. A one-point twist that "
                             rf"lowers short rates and raises long ones costs {abs(tw[k]):.1f}", 4.6, 17,
                             GREY_A).next_to(leg, DOWN, buff=0.3, aligned_edge=LEFT)
        with self.voiceover(
            "In 1952 the actuary Frank Redington asked how a life office could hold assets that would always cover "
            "its promises. His answer: match the present value, <bookmark mark='a'/> match the duration, "
            "<bookmark mark='b'/> and hold more convexity than the liabilities. Then any parallel move of rates "
            "leaves a surplus. <bookmark mark='c'/> Here is a pension promise of a hundred, due in fifteen years, "
            "funded with five-year and thirty-year zeros, a barbell. Under parallel moves the surplus is never "
            "negative: a smile. <bookmark mark='d'/> But twist the curve, short rates down and long rates up, and "
            f"a one-point twist costs {abs(tw[k]):.1f}, {100 * abs(tw[k]) / im['L']:.0f} percent of the liability's value. "
            "Immunization protects against "
            "the one move the curve rarely makes alone. Fisher and Weil extended it to sloped curves in 1971; the "
            "twist risk remains."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(g), Create(lp), FadeIn(leg[0]), run_time=2)
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
        surf = Surface(lambda u, v: ax.c2p(u, v, f(u, v)), u_range=(-3, 3), v_range=(-2, 2), resolution=(24, 16),
                       fill_opacity=0.75, stroke_width=0.4, stroke_color=GREY_D, checkerboard_colors=False)
        for face in surf:
            zc = ax.p2c(face.get_center())[2]
            face.set_fill(GOOD if zc >= 0 else BAD, opacity=0.75)
        zero = Surface(lambda u, v: ax.c2p(u, v, 0), u_range=(-3, 3), v_range=(-2, 2), resolution=(2, 2),
                       fill_color=WHITE, fill_opacity=0.12, stroke_width=0, checkerboard_colors=False)
        key = VGroup(label(r"parallel move (across), twist (back), surplus (up)", font_size=19, color=GREY_A),
                     legend([(GOOD, r"surplus"), (BAD, r"shortfall")], font_size=17)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.3)
        self.set_camera_orientation(phi=65 * DEGREES, theta=-55 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(key)
        self.remove(key)
        with self.voiceover(
            "The whole picture: the barbell's surplus over every combination of a parallel move and a twist. Along "
            "the zero-twist line it is the smile you saw, never below the floor. <bookmark mark='a'/> Turn it, and a "
            "red valley opens along the twist axis: whole regions where a fund with perfect duration matching is short "
            "of money. Key-rate matching, cash flow by cash flow, closes it; one number cannot."
        ) as vo:
            self.play(Create(ax), FadeIn(key))
            self.play(FadeIn(zero), Create(surf), run_time=2.5)
            vo.wait_until("a")
            self.move_camera(theta=-130 * DEGREES, phi=70 * DEGREES, run_time=6)
        q = ask(r"your fund is immunized against parallel moves. Which shape of curve move hurts it most?")
        self.add_fixed_in_frame_mobjects(q)
        self.remove(q)
        with self.voiceover("Which shape of curve move hurts an immunized fund the most?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=0.5)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0, zoom=1.0, frame_center=ORIGIN)
