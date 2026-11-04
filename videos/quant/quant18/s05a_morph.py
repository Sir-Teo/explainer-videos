from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant18.common import PART, ZERO, ask, grid_fn, illustration, load, surf3d_axes


class Morph(VoiceoverScene, ThreeDScene):
    def construct(self):
        m = load("morph")
        self.card()
        self.movie(m)
        self.eras(m)
        self.surface(m)

    def card(self):
        c = chapter_card(9, r"Five decades of the curve", r"How has the price of time moved since 1972?", part=PART)
        with self.voiceover("Chapter nine. Five decades of the curve."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def movie(self, m):
        t, Y = np.asarray(m["t"]), np.asarray(m["Y"], float)
        mats = np.arange(1, 31)
        g = axes([0, 30], [0, 16], x_length=8.6, y_length=4.8, xlabel=r"maturity, years",
                 ylabel=r"zero-coupon yield, \% (continuous)", xticks=[0, 5, 10, 20, 30], yticks=[0, 4, 8, 12, 16],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        tr = ValueTracker(0)

        def cur():
            i = int(tr.get_value())
            ok = ~np.isnan(Y[i])
            y = Y[i][ok]
            col = QC.LOSS if y[-1] < y[0] else ZERO
            return curve(ax, mats[ok], y, col, stroke_width=4)

        def ghost():
            i = int(tr.get_value())
            out = VGroup()
            for j in range(max(0, i - 24), i, 3):
                ok = ~np.isnan(Y[j])
                out.add(curve(ax, mats[ok], Y[j][ok], GREY_C, stroke_width=1.2).set_stroke(opacity=0.25 + 0.5 * (j - i + 24)
                                                                                           / 24))
            return out
        cv = always_redraw(cur)
        gh = always_redraw(ghost)

        def date_tex():
            x = t[int(tr.get_value())]
            y = int(x)
            mo = int(round((x - y) * 12)) + 1
            return MathTex(rf"{y}\text{{-}}{min(mo, 12):02d}", font_size=44).to_corner(UR, buff=0.6)
        dt = always_redraw(date_tex)
        y10 = always_redraw(lambda: MathTex(rf"10\text{{y}}:\ {Y[int(tr.get_value())][9]:.2f}\%", font_size=32,
                                            color=ZERO).next_to(dt, DOWN, buff=0.3, aligned_edge=RIGHT))
        leg = legend([(ZERO, r"upward-sloping"), (QC.LOSS, r"inverted: 10-year below 1-year")],
                     font_size=17).to_corner(DR, buff=0.5).shift(UP * 0.5)
        n = len(t)
        i81 = int(np.argmin(np.abs(t - m["y10_max"]["t"])))
        i20 = int(np.argmin(np.abs(t - m["y10_min"]["t"])))
        with self.voiceover(
            "Here is the zero-coupon curve at the end of every month since 1972, from the Fed's fitted file; the longest "
            "maturity grows as the Treasury issued longer bonds. Red means inverted. <bookmark mark='a'/> The seventies: "
            "inflation, and a curve that keeps lifting. Then Paul Volcker. By "
            f"{int(m['y10_max']['t'])} the ten-year zero yield reached {m['y10_max']['y']:.1f} percent, and the curve "
            "inverted hard. <bookmark mark='b'/> Then forty years of decline, with an inversion before each "
            "recession: 1989, 2000, 2006, 2019. <bookmark mark='c'/> In the pandemic summer of 2020 the ten-year touched "
            f"{m['y10_min']['y']:.2f} percent. <bookmark mark='d'/> And then 2022: the fastest rise in four decades, "
            "and the long inversion of 2023 and 2024."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            self.add(gh, cv, dt, y10)
            vo.wait_until("a")
            self.play(tr.animate.set_value(i81), run_time=6, rate_func=linear)
            vo.wait_until("b")
            self.play(tr.animate.set_value(int(np.argmin(np.abs(t - 2019.9)))), run_time=10, rate_func=linear)
            vo.wait_until("c")
            self.play(tr.animate.set_value(i20), run_time=2, rate_func=linear)
            vo.wait_until("d")
            self.play(tr.animate.set_value(n - 1), run_time=5, rate_func=linear)
        for mob in (cv, gh, dt, y10):
            mob.clear_updaters()
        self.add(illustration(r"the Fed's GSW curve, month ends, 1972--2025"))
        self.wait(0.4)
        self.clear_scene()

    def eras(self, m):
        mats = np.arange(1, 31)
        g = axes([0, 30], [0, 16], x_length=8.0, y_length=4.8, xlabel=r"maturity, years", ylabel=r"\%",
                 xticks=[0, 5, 10, 20, 30], yticks=[0, 4, 8, 12, 16], font_size=14).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        names = list(m["eras"])
        cols = [interpolate_color(ManimColor(QC.LOSS), ManimColor(QC.SPOT), i / (len(names) - 1)) for i in range(len(names))]
        lines, items = VGroup(), []
        for nm, col in zip(names, cols):
            y = np.asarray(m["eras"][nm]["y"], float)
            ok = ~np.isnan(y)
            lines.add(curve(ax, mats[ok], y[ok], col, stroke_width=3))
            items.append((col, rf"{nm}"))
        leg = legend(items, font_size=17).to_edge(RIGHT, buff=0.5)
        stat = wrapped_label(rf"inverted (10-year below 1-year) on {100 * m['inverted_share']:.0f}\% of days since 1972",
                             3.4, 18, GREY_A).next_to(leg, DOWN, buff=0.4, aligned_edge=LEFT)
        with self.voiceover(
            "Nine moments, side by side. The 1981 peak, a curve inverted at fifteen percent. The ordinary upward "
            "slopes of the nineties. The flat curve of 2000 before the dot-com bust. The crisis, and the long "
            "flattening at the zero bound. The pandemic low. <bookmark mark='a'/> And the inverted curve of 2023, "
            "before the curve of today. Across all those days, the curve was inverted on about "
            f"{100 * m['inverted_share']:.0f} percent of them. Every shape a model must produce is in this picture."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[AnimationGroup(Create(l_), FadeIn(r_)) for l_, r_ in zip(lines, leg)],
                                             lag_ratio=0.5, run_time=9))
            vo.wait_until("a")
            self.play(FadeIn(stat))
        self.wait(0.4)
        self.clear_scene()

    def surface(self, m):
        t, Y = np.asarray(m["t"]), np.asarray(m["Y"], float)
        mats = np.arange(1, 16)
        Z = Y[:, :15]
        sel = np.arange(0, len(t), 3)
        f = grid_fn(mats, t[sel], Z[sel])
        ax = surf3d_axes([1972, 2026, 10], [1, 15, 2], [0, 16, 4], x_length=7.4, y_length=4.2, z_length=3.4)
        ax.shift(RIGHT * 0.9 + DOWN * 0.3)
        surf = Surface(lambda u, v: ax.c2p(u, v, f(v, u)), u_range=(t[0], t[-1]), v_range=(1, 15), resolution=(60, 12),
                       fill_opacity=0.85, stroke_width=0.3, stroke_color=GREY_D, checkerboard_colors=False)
        surf.set_fill_by_value(axes=ax, colorscale=[(QC.SPOT, 0), (QC.DELTA, 7), (QC.LOSS, 14)], axis=2)
        key = VGroup(label(r"date (across), maturity 1--15 years (back), yield (up)", font_size=19, color=GREY_A),
                     label(r"colour: the yield, blue low to red high", font_size=17, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UL, buff=0.3)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-70 * DEGREES, zoom=0.9)
        self.add_fixed_in_frame_mobjects(key)
        self.remove(key)
        with self.voiceover(
            "And the whole history as one landscape: date across, maturity going back, yield up. The Volcker mountain, "
            "the forty-year slope down, the flat plain at zero, and the cliff of 2022. <bookmark mark='a'/> Turned "
            "edge-on, each slice through the maturities is a curve; and the slices look alike. The ridge moves up and "
            "down together, tilts, and occasionally bends. That observation, made precise, is the next chapter."
        ) as vo:
            self.play(Create(ax), FadeIn(key))
            self.play(Create(surf), run_time=3)
            vo.wait_until("a")
            self.move_camera(theta=-15 * DEGREES, phi=75 * DEGREES, run_time=6)
        q = ask(r"on this curve an inversion came before each of the seven US recessions since 1973; the long one of "
                r"2022--24 has had none so far. Is an inversion a forecast, or a cause?")
        self.add_fixed_in_frame_mobjects(q)
        self.remove(q)
        with self.voiceover("On this curve, an inversion came before each of the seven American recessions since 1973, "
                            "and the long inversion of 2022 to 2024 has had none so far. Is an inversion a forecast, or "
                            "a cause?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=0.5)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0, zoom=1.0, frame_center=ORIGIN)
