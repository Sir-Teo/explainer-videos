from __future__ import annotations

from datetime import date

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, load, real_data


def _t(s):
    d = date.fromisoformat(s)
    return d.year + (d.timetuple().tm_yday - 1) / 365


class Calibration(VoiceoverScene, ThreeDScene):
    def construct(self):
        L = load("landscape")
        h = load("history")
        self.card()
        self.landscape(L)
        self.history(h)

    def card(self):
        c = chapter_card(8, r"Calibration", r"Which parameters did the market mean?", part=PART)
        with self.voiceover("Chapter eight. Calibration."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def landscape(self, Ld):
        ka, xi = np.log10(np.asarray(Ld["kappa"])), np.log10(np.asarray(Ld["xi"]))
        loss = np.clip(np.asarray(Ld["loss"]), 1.0, 4.0)
        f = RegularGridInterpolator((ka, xi), loss)
        ax = ThreeDAxes(x_range=[ka[0], ka[-1], 0.5], y_range=[xi[0], xi[-1], 0.5], z_range=[1.0, 4.0, 1.0],
                        x_length=7.0, y_length=5.0, z_length=3.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.5)
        surf = Surface(lambda u, v: ax.c2p(u, v, float(f((u, v)))), u_range=[ka[0], ka[-1]], v_range=[xi[0], xi[-1]],
                       resolution=(28, 28), fill_opacity=0.85, stroke_width=0.3, stroke_color=GREY_D)
        surf.set_fill_by_value(axes=ax, colorscale=[(RV, 1.3), (IV, 2.2), (BAD, 3.5)], axis=2)
        floor = np.asarray(Ld["loss"]).argmin(axis=1)
        valley = VMobject(stroke_color=WHITE, stroke_width=4).set_points_smoothly(
            [ax.c2p(ka[i], xi[j], loss[i, j] + 0.03) for i, j in enumerate(floor)])
        best = Ld["best"]
        star = Dot3D(ax.c2p(np.log10(best[1]), np.log10(best[3]), loss.min() + 0.05), radius=0.09, color=YELLOW)
        hint = VGroup(label(r"mean reversion $\kappa$, 0.5 to 30 (log)", font_size=22, color=GREY_A),
                      label(r"vol of vol $\xi$, 0.3 to 8 (log)", font_size=22, color=GREY_A),
                      label(r"height: the best fit error with $v_0, \theta, \rho$ re-optimized", font_size=22,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.4)
        Lm = np.asarray(Ld["loss"])
        i0 = int(np.argmin(np.abs(np.asarray(Ld["kappa"]) - 5.0)))
        along = Lm[i0, floor[i0]]
        txt = VGroup(MathTex(rf"\min = {Lm.min():.2f}\ \text{{at}}\ \kappa = {best[1]:.0f},\ \xi = {best[3]:.1f}",
                             font_size=26, color=YELLOW),
                     MathTex(rf"\kappa = {Ld['kappa'][i0]:.0f}:\ \ {along:.2f}", font_size=26, color=WHITE),
                     label(rf"12 random starts: all 12 end at the same minimum", font_size=20, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DR, buff=0.4)
        src = real_data(r"Heston on the Surface: 225 fits on a 15 by 15 grid", corner=DL)
        self.set_camera_orientation(phi=62 * DEGREES, theta=-130 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint, txt, src)
        self.remove(hint, txt, src)
        with self.voiceover(
            "Calibration is an optimization, and its landscape is worth looking at. Fix Heston's mean reversion and "
            "vol of vol, re-fit the other three parameters, and record the error. Do it on a grid, and here is the "
            "landscape. <bookmark mark='a'/> The minimum is the yellow star. But look at the valley running from it: "
            "a long, curved floor where faster mean reversion and higher vol of vol trade off against each other. "
            f"At a mean reversion of {Ld['kappa'][i0]:.0f} instead of {best[1]:.0f}, the error rises only from "
            f"{Lm.min():.2f} to {along:.2f} points. <bookmark mark='b'/> On this day the optimizer is not fooled: "
            "twelve random starts all end at the same point. But the valley says the data pin down a combination of "
            "the two, not each one. And that has consequences next week."
        ) as vo:
            self.play(FadeIn(hint), FadeIn(src), Create(ax), Create(surf), run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(star), Create(valley), run_time=2)
            self.move_camera(theta=-70 * DEGREES, phi=58 * DEGREES, run_time=max(vo.remaining(1.0) - 6, 2))
            vo.wait_until("b")
            self.play(FadeIn(txt))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, surf, valley, star)), FadeOut(hint),
                                                                  FadeOut(txt), FadeOut(src)], run_time=1.5)
        self.clear_scene()

    def history(self, h):
        rows = h["rows"]
        t = np.array([_t(r["day"]) for r in rows])
        X = np.array([r["x"] for r in rows])
        xt = [2024, 2024.5, 2025, 2025.5, 2026]
        fmt = lambda u: {0: "Jan 24", 1: "Jul 24", 2: "Jan 25", 3: "Jul 25", 4: "Jan 26"}[round((u - 2024) * 2)]  # noqa: E731
        g1 = axes([2024, 2026], [0, 22], x_length=6.2, y_length=2.2, ylabel=r"$\kappa$", xticks=xt, xfmt=fmt,
                  yticks=[0, 10, 20], font_size=15)
        g2 = axes([2024, 2026], [0, 6.5], x_length=6.2, y_length=2.2, ylabel=r"$\xi$", xticks=xt, xfmt=fmt,
                  yticks=[0, 2, 4, 6], font_size=15)
        g3 = axes([2024, 2026], [-0.5, 0.3], x_length=6.2, y_length=2.2, ylabel=r"$\rho$", xticks=xt, xfmt=fmt,
                  yticks=[-0.4, 0, 0.2], font_size=15)
        G = VGroup(g1, g2, g3).arrange(DOWN, buff=0.3).to_edge(LEFT, buff=0.7)
        l1 = curve(g1.ax, t, X[:, 1], VAR, stroke_width=2.2)
        l2 = curve(g2.ax, t, X[:, 3], OPT, stroke_width=2.2)
        l3 = curve(g3.ax, t, X[:, 4], IV, stroke_width=2.2)
        z3 = DashedLine(g3.ax.c2p(2024, 0), g3.ax.c2p(2026, 0), stroke_color=GREY_C, stroke_width=1.2)
        kb = float((X[:, 1] > 19.9).mean())
        fe = float((2 * X[:, 1] * X[:, 2] / X[:, 3] ** 2 < 1).mean())
        rp = float((X[:, 4] > 0).mean())
        side = VGroup(
            wrapped_label(rf"Heston recalibrated every Wednesday to that morning's surface: {len(rows)} weeks, median fit "
                          rf"{h['rmse_median']:.1f} vol points", 4.6, 19, GREY_A),
            MathTex(rf"\kappa\ \text{{moves}}\ {100 * h['median_weekly_change']['kappa']:.0f}\%\ \text{{a week (median)}}",
                    font_size=26, color=VAR),
            label(rf"and sits at its bound of 20 in {100 * kb:.0f}\% of weeks", font_size=20, color=GREY_A),
            MathTex(rf"\text{{Feller fails in}}\ {100 * fe:.0f}\%\ \text{{of weeks}}", font_size=26, color=BAD),
            MathTex(rf"\rho > 0\ \text{{in}}\ {100 * rp:.0f}\%\ \text{{of weeks}}", font_size=26, color=IV),
            wrapped_label(r"a model whose constants change every week is being used as an interpolator, not a "
                          r"description; desks regularize toward last week's values (Cont and Tankov 2004) and watch "
                          r"the hedge, not the fit", 4.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35)
        src = real_data(r"100 weekly surfaces from Deribit trades, 2024--2025")
        with self.voiceover(
            "Recalibrate Heston every Wednesday for two years, and watch the constants. Mean reversion, which the "
            "model says is a fixed property of the world, moves by a quarter in a typical week, and "
            f"spends {100 * kb:.0f} percent of weeks pinned at the upper bound we allowed. <bookmark mark='a'/> The "
            f"vol of vol swings between one and six. Feller's condition fails in {100 * fe:.0f} percent of weeks. "
            "<bookmark mark='b'/> And the correlation, the parameter that sets the skew, is positive in "
            f"{100 * rp:.0f} percent of weeks. That is not noise: in most weeks of these two years, Bitcoin's "
            "thirty-day smile was dearer on the call side than the put side, the tilt Part twelve's autoencoder "
            "learned as its second number. Unlike stocks, Bitcoin's buyers pay up for upside. <bookmark mark='c'/> A model whose constants change every week is being "
            "used to interpolate prices, not to describe the world. That is fine for quoting vanillas. It is "
            "dangerous for hedging and exotics, which depend on those constants staying put. Desks regularize "
            "toward last week's values, and judge a model by its hedges, not its fit."
        ) as vo:
            self.play(FadeIn(G[0]), Create(l1), FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]), FadeIn(src), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(G[1]), Create(l2), FadeIn(side[3]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(G[2]), Create(z3), Create(l3), FadeIn(side[4]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene()
