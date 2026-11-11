from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant18.common import PART, ZERO, ask, grid_fn, illustration, load, surf3d_axes


def month_index(t):
    """Recover calendar months from the original year/month/day encoding."""
    t = np.asarray(t, float)
    years = np.floor(t).astype(int)
    months0 = np.clip(np.floor((t - years) * 12 + 1e-8).astype(int), 0, 11)
    return years * 12 + months0


def inversion_summary(m):
    Y = np.asarray(m["Y"], float)
    valid = np.isfinite(Y[:, 9]) & np.isfinite(Y[:, 0])
    negative = valid & (Y[:, 9] < Y[:, 0])
    return int(negative.sum()), int(valid.sum())


class Morph(VoiceoverScene, ThreeDScene):
    def construct(self):
        m = load("morph")
        self.card()
        self.movie(m)
        self.eras(m)
        self.recessions(m)
        self.surface(m)

    def card(self):
        c = chapter_card(9, r"Five decades of the curve", r"How has the price of time moved since 1972?", part=PART)
        with self.voiceover("Chapter nine. Five decades of the curve."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def movie(self, m):
        t, Y = np.asarray(m["t"]), np.asarray(m["Y"], float)
        mats = np.arange(1, 31)
        g = axes([0, 30], [0, 18], x_length=8.6, y_length=4.8, xlabel=r"maturity, years",
                 ylabel=r"zero-coupon yield, \% (continuous)", xticks=[0, 5, 10, 20, 30], yticks=[0, 4, 8, 12, 16],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        tr = ValueTracker(0)

        def cur():
            i = int(tr.get_value())
            ok = np.isfinite(Y[i])
            y = Y[i][ok]
            col = QC.LOSS if Y[i, 9] < Y[i, 0] else ZERO
            return curve(ax, mats[ok], y, col, stroke_width=4)

        def ghost():
            i = int(tr.get_value())
            out = VGroup()
            for j in range(max(0, i - 24), i, 3):
                ok = np.isfinite(Y[j])
                out.add(curve(ax, mats[ok], Y[j][ok], GREY_C, stroke_width=1.2).set_stroke(opacity=0.25 + 0.5 * (j - i + 24)
                                                                                           / 24))
            return out
        cv = always_redraw(cur)
        gh = always_redraw(ghost)

        def date_tex():
            x = t[int(tr.get_value())]
            mi = int(month_index([x])[0])
            y, mo = mi // 12, mi % 12 + 1
            return MathTex(rf"{y}\text{{-}}{min(mo, 12):02d}", font_size=44).to_corner(UR, buff=0.6)
        dt = always_redraw(date_tex)
        y10 = always_redraw(lambda: MathTex(rf"10\text{{y}}:\ {Y[int(tr.get_value())][9]:.2f}\%", font_size=32,
                                            color=ZERO).next_to(dt, DOWN, buff=0.3, aligned_edge=RIGHT))
        leg = legend([(ZERO, r"10-year at least 1-year"), (QC.LOSS, r"inverted: 10-year below 1-year")],
                     font_size=17).to_corner(DR, buff=0.5).shift(UP * 0.5)
        n = len(t)
        i81 = int(np.argmin(np.abs(t - m["y10_max"]["t"])))
        i20 = int(np.argmin(np.abs(t - m["y10_min"]["t"])))
        with self.voiceover(
            f"This animation samples the saved month-end GSW estimates from January 1972 through December 2025. Only available maturities are drawn; missing long maturities are omitted. Red consistently means the ten-year zero yield is below the one-year yield. <bookmark mark='a'/> In the saved month-end sample, the ten-year maximum is {m['y10_max']['y']:.1f} percent in {int(m['y10_max']['t'])}. This is not a daily record calculation. <bookmark mark='b'/> Yields subsequently declined over much of the following decades, with substantial reversals and several inversions. <bookmark mark='c'/> The month-end ten-year minimum is {m['y10_min']['y']:.2f} percent in 2020. <bookmark mark='d'/> The later rise and the 2022-to-2024 inversion follow. The animation moves quickly across month ends, with quarterly grey traces from the preceding two years; each saved month is not necessarily a separate visible video frame."
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
        g = axes([0, 30], [0, 18], x_length=8.0, y_length=4.8, xlabel=r"maturity, years", ylabel=r"\%",
                 xticks=[0, 5, 10, 20, 30], yticks=[0, 4, 8, 12, 16], font_size=14).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        names = list(m["eras"])
        cols = [interpolate_color(ManimColor(QC.LOSS), ManimColor(QC.SPOT), i / (len(names) - 1)) for i in range(len(names))]
        lines, items = VGroup(), []
        for nm, col in zip(names, cols):
            y = np.asarray(m["eras"][nm]["y"], float)
            ok = np.isfinite(y)
            lines.add(curve(ax, mats[ok], y[ok], col, stroke_width=3))
            items.append((col, rf"{nm}"))
        leg = legend(items, font_size=17).to_edge(RIGHT, buff=0.5)
        n_inv, n_valid = inversion_summary(m)
        stat = wrapped_label(rf"10-year below 1-year: {n_inv}/{n_valid} paired month ends ({100 * n_inv / n_valid:.1f}\%), 1972--2025",
                             3.4, 18, GREY_A).next_to(leg, DOWN, buff=0.4, aligned_edge=LEFT)
        stat.shift(LEFT * max(0.0, stat.get_right()[0] - 6.75))
        with self.voiceover(
            f"Nine selected snapshots compare different levels, slopes and curvature. They include the high-yield era, later lower-yield curves, the pandemic and the 2023 inversion. They are examples, not an exhaustive set of shapes a future model must generate. <bookmark mark='a'/> The last snapshot is December 2025. Recomputing the ten-year-minus-one-year definition from this same saved monthly panel gives {n_inv} inverted observations out of {n_valid}, or {100 * n_inv / n_valid:.1f} percent. This is a fraction of paired month ends, not a daily inversion frequency."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[AnimationGroup(Create(l_), FadeIn(r_)) for l_, r_ in zip(lines, leg)],
                                             lag_ratio=0.5, run_time=9))
            vo.wait_until("a")
            self.play(FadeIn(stat))
        self.wait(0.4)
        self.clear_scene()

    def recessions(self, m):
        t, Y = np.asarray(m["t"]), np.asarray(m["Y"], float)
        spr = (Y[:, 9] - Y[:, 0]) * 100
        # NBER peaks are the last expansion month; shade the following month
        # through the trough month. Leads below refer to the peak month.
        peak_trough = [(197311, 197503), (198001, 198007), (198107, 198211),
                       (199007, 199103), (200103, 200111), (200712, 200906), (202002, 202004)]
        to_index = lambda ym: (ym // 100) * 12 + ym % 100 - 1
        cycles = [((to_index(p) + 1) / 12, (to_index(q) + 1) / 12) for p, q in peak_trough]
        mi = month_index(t)
        g = axes([1972, 2026], [-400, 400], x_length=9.0, y_length=4.2, xlabel=r"year",
                 ylabel=r"10-year minus 1-year zero yield, bp", xticks=[1980, 1990, 2000, 2010, 2020],
                 yticks=[-400, -200, 0, 200, 400], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        bands = VGroup(*[Rectangle(width=ax.c2p(b, 0)[0] - ax.c2p(a, 0)[0], height=ax.c2p(0, 400)[1] - ax.c2p(0, -400)[1],
                                   stroke_width=0, fill_color=GREY_B, fill_opacity=0.22).move_to(
            [(ax.c2p(a, 0)[0] + ax.c2p(b, 0)[0]) / 2, (ax.c2p(0, 400)[1] + ax.c2p(0, -400)[1]) / 2, 0]) for a, b in cycles])
        zero = Line(ax.c2p(1972, 0), ax.c2p(2026, 0), color=WHITE, stroke_width=1.5)
        finite = np.isfinite(spr)
        line = curve(ax, t[finite], spr[finite], ZERO, stroke_width=2.5)
        neg = VGroup(*[Dot(ax.c2p(a, b), radius=0.025, color=QC.LOSS) for a, b in zip(t, spr) if b < 0])
        leads = []
        for peak, _ in peak_trough:
            p = to_index(peak)
            w = (mi < p) & (mi >= p - 36) & finite
            k = np.flatnonzero(w & (spr < 0))
            leads.append(int(p - mi[k[0]]) if len(k) else None)
        txt = ", ".join(str(x) for x in leads if x is not None)
        side = VGroup(
            wrapped_label(r"grey: NBER contraction months, dated retrospectively", 3.4, 18, GREY_B),
            wrapped_label(rf"Lead to peak, using first negative month in available prior 36 months: {txt}", 3.4, 18, GREY_A),
            wrapped_label(r"First lookback is left-censored; windows overlap. Seven selected peaks do not measure forecast accuracy or false positives.", 3.4, 18,
                          QC.LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        lo, hi = min(x for x in leads if x is not None), max(x for x in leads if x is not None)
        with self.voiceover(
            f"The full monthly ten-year-minus-one-year spread is plotted, including its trough below minus three hundred basis points. Grey bands mark the NBER contraction months after each peak through its trough; those dates are determined retrospectively. <bookmark mark='a'/> For each of seven selected peaks, find the first negative spread in the available thirty-six preceding calendar months. This rule produces leads of {txt} months to the peak. The first lookback is left-censored by the 1972 sample start, and the two early-eighties windows overlap. <bookmark mark='b'/> These seven selected outcomes are neither independent trials nor a forecast score. We have not tabulated all false positives, fixed a real-time decision rule, or evaluated an untouched forecast sample. Association alone does not identify a causal effect of inversion."
        ) as vo:
            self.play(FadeIn(g), FadeIn(bands), Create(zero), Create(line), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(neg), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.add(illustration(r"the Fed's GSW curve, month ends; recession dates: NBER"))
        self.wait(0.4)
        self.clear_scene()

    def surface(self, m):
        t, Y = np.asarray(m["t"]), np.asarray(m["Y"], float)
        mats = np.arange(1, 16)
        Z = Y[:, :15]
        sel = np.unique(np.r_[np.arange(0, len(t), 3), len(t) - 1])
        assert np.isfinite(Z[sel]).all()
        f = grid_fn(mats, t[sel], Z[sel])
        ax = surf3d_axes([1972, 2026, 10], [1, 15, 2], [0, 18, 4], x_length=7.4, y_length=4.2, z_length=3.4)
        ax.shift(RIGHT * 0.9 + DOWN * 0.3)
        surf = Surface(lambda u, v: ax.c2p(u, v, f(v, u)), u_range=(t[sel][0], t[sel][-1]), v_range=(1, 15), resolution=(60, 12),
                       fill_opacity=0.85, stroke_width=0.3, stroke_color=GREY_D, checkerboard_colors=False)
        surf.set_fill_by_value(axes=ax, colorscale=[(QC.SPOT, 0), (QC.DELTA, 7), (QC.LOSS, 14)], axis=2)
        key = VGroup(label(r"date (across), maturity 1--15 years (back), yield (up)", font_size=19, color=GREY_A),
                     label(r"quarterly samples plus final month; bilinear interpolation; colour gives yield", font_size=17, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UL, buff=0.3)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-70 * DEGREES, zoom=0.9)
        self.add_fixed_in_frame_mobjects(key)
        self.remove(key)
        with self.voiceover(
            "This landscape shows only the one-through-fifteen-year maturities. It uses every third saved month plus the final December 2025 observation, bilinearly interpolated onto a sixty-by-twelve rendering mesh. No missing maturity is filled in, and the date range stays within the sampled grid. The height is yield, with the full sampled range retained. <bookmark mark='a'/> Many slices share broad level, slope and bend movements. That motivates a statistical factor description; it does not establish stable future loadings or explain the economic causes of those movements."
        ) as vo:
            self.play(Create(ax), FadeIn(key))
            self.play(Create(surf), run_time=3)
            vo.wait_until("a")
            self.move_camera(theta=-15 * DEGREES, phi=75 * DEGREES, run_time=6)
        q = ask(r"What additional evidence would distinguish a useful real-time inversion forecast from a causal effect?")
        self.add_fixed_in_frame_mobjects(q)
        self.remove(q)
        with self.voiceover('What additional evidence would distinguish a useful real-time inversion forecast from a causal effect?'):
            self.play(FadeIn(q))
        self.wait(2.5)
        self.clear_scene()
        q.to_edge(UP, buff=0.6)
        answer = wrapped_label(r"Forecast: fixed rule, all alarms, real-time data, untouched outcomes and uncertainty. Causation: a credible identification design beyond historical association.", 11.8, 26, QC.DELTA).move_to(ORIGIN)
        self.add_fixed_in_frame_mobjects(q, answer)
        self.remove(q, answer)
        with self.voiceover("A forecast needs a fixed rule, all alarms, real-time data, untouched outcomes and uncertainty. A causal claim additionally needs a credible identification design beyond historical association."):
            self.play(FadeIn(q), FadeIn(answer))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=0.5)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0, zoom=1.0, frame_center=ORIGIN)
