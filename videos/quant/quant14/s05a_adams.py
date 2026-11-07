from __future__ import annotations

import numpy as np

from videos.quant.quant14.common import axes, data_range, skew_range
from scipy.interpolate import RegularGridInterpolator

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import (BAD, IV, MODEL_COL, OPT, PART, ROUGH, RV, VAR, illustration, load, pause,
                                         real_data)


class Adams(VoiceoverScene, ThreeDScene):
    def construct(self):
        a = load("adams_conv")
        p = load("rh_profile9")
        self.card()
        self.derive()
        self.live(a)
        self.lab(a)
        self.surface(a)
        self.profile(p)

    def card(self):
        c = chapter_card(8, r"Solving it: the fractional Adams scheme", r"How is a fractional equation solved, and how "
                         r"much does the Surface care about $H$?", part=PART)
        with self.voiceover("Chapter eight. Solving it: the fractional Adams scheme, and the H profile."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"h(t)", r"=", r"\frac{1}{\Gamma(\alpha)}\int_0^t (t - s)^{\alpha - 1}F\big(h(s)\big)\,ds", font_size=38,
                      colors={r"h(t)": ROUGH}),
                cmath(r"h^P_{k + 1}", r"=", r"\frac{\Delta^\alpha}{\Gamma(\alpha + 1)}\sum_{j = 0}^{k}\big((k + 1 - j)^\alpha - "
                      r"(k - j)^\alpha\big)F(h_j)", font_size=34, colors={r"h^P_{k + 1}": GREY_A}),
                cmath(r"h_{k + 1}", r"=", r"\frac{\Delta^\alpha}{\Gamma(\alpha + 2)}\Big(F(h^P_{k + 1}) + \sum_{j = 0}^{k}"
                      r"a_{j, k + 1}F(h_j)\Big)", font_size=34, colors={r"h_{k + 1}": ROUGH}),
                cmath(r"\text{cost}", r"=", r"O(n^2)\ \text{for } n \text{ steps}\quad(\text{an ODE: } O(n))", font_size=36,
                      colors={r"\text{cost}": GREY_A})]
        whys = [why(r"the fractional Riccati equation written as a Volterra integral equation"),
                why(r"predictor: $F$ held constant on each cell, the kernel integrated exactly (product rectangle rule)"),
                why(r"corrector: $F$ linear between grid points (product trapezoid rule), with the predictor at the new "
                    r"point; Diethelm, Ford and Freed (2002)"),
                why(r"every new point needs the whole past: the memory sum")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.0, buff=0.7, edge=6.9)
        with self.voiceover(
            "How do you solve an equation with a fractional derivative? Write it as an integral equation: h at time "
            "t is the fractional integral of F of h. <bookmark mark='a'/> Then march along a grid, the way an "
            "ordinary differential equation solver does, but integrating the kernel exactly. The predictor holds F "
            "constant on each past cell. <bookmark mark='b'/> The corrector treats F as linear between grid points, "
            "and uses the predictor at the new point: a product trapezoid rule. This is the fractional Adams scheme "
            "of Kai Diethelm, Neville Ford and Alan Freed. <bookmark mark='c'/> The difference from an ordinary "
            "solver: every new point needs the whole past. That memory sum makes n steps cost n squared."
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

    def live(self, a):
        hr = np.asarray(a["trace_re"])
        pr = np.asarray(a["pred_re"])
        n = hr.shape[1] - 1
        T = a["trace_T"]
        t = np.linspace(0, T, n + 1) * 365
        lo, hi = float(min(hr.min(), pr.min())), float(max(hr.max(), pr.max(), 0.0))
        g = axes([0, T * 365], [lo, hi], x_length=9.0, y_length=4.6, xlabel=r"days", ylabel=r"$\mathrm{Re}\,h(u, t)$",
                 xticks=[0, 10, 20, 30], yticks=[round(lo, 1), 0], font_size=15).move_to(DOWN * 0.3 + LEFT * 1.2)
        ax = g.ax
        cols = [interpolate_color(ManimColor(IV), ManimColor(ROUGH), i / 9) for i in range(10)]
        k = ValueTracker(0)

        def lines():
            kk = int(k.get_value())
            grp = VGroup()
            for i in range(10):
                if kk >= 1:
                    grp.add(VMobject(stroke_color=cols[i], stroke_width=2.2).set_points_as_corners(
                        [ax.c2p(t[j], hr[i, j]) for j in range(kk + 1)] + ([ax.c2p(t[kk], hr[i, kk])] if kk == 0 else [])))
            return grp

        def fan():
            kk = int(k.get_value())
            grp = VGroup()
            if 1 <= kk < n:
                tgt = ax.c2p(t[kk + 1], pr[9, kk + 1])
                for j in range(0, kk + 1, max(1, kk // 12)):
                    grp.add(Line(ax.c2p(t[j], hr[9, j]), tgt, stroke_color=YELLOW, stroke_width=1,
                                 stroke_opacity=0.35))
                grp.add(Dot(tgt, radius=0.06, color=GREY_A), Dot(ax.c2p(t[kk + 1], hr[9, kk + 1]), radius=0.07, color=YELLOW))
            return grp

        L = always_redraw(lines)
        Fn = always_redraw(fan)
        leg = legend([(IV, r"$u = 1$"), (ROUGH, r"$u = 10$"), (YELLOW, r"the memory: every past point feeds the next"),
                      (GREY_A, r"predictor (grey), corrector (yellow)")], font_size=16).to_edge(RIGHT, buff=0.3)
        src = illustration(r"$H = 0.1$, 40 steps over 30 days, real parts; the House's \texttt{frac\_riccati}")
        with self.voiceover(
            "Watch it run, for ten frequencies u at once, over thirty days. At each step, the yellow lines are the "
            "memory: every earlier point is pulled into the next one. The grey dot is the predictor's guess, the "
            "yellow dot the corrected value. <bookmark mark='a'/> An ordinary differential equation would need only "
            "the last point. Here the whole fan of history arrives at every step, which is why rough models were "
            "once called slow, and why a few milliseconds is still an achievement."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(src), FadeIn(L), FadeIn(Fn))
            self.play(k.animate.set_value(n - 1), run_time=max(vo.remaining(0.0) - 0.5, 6), rate_func=linear)
        L.clear_updaters()
        Fn.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def lab(self, a):
        card = lab_card(r"the fractional Adams scheme", [
            "for k in range(n):",
            "    jj = j[: k + 1]",
            "    bw = dt**alpha / ga1 * ((k+1-jj)**alpha - (k-jj)**alpha)",
            "    hp = Fh[:, : k + 1] @ bw                    # predictor",
            "    aw = np.empty(k + 1)",
            "    aw[0] = k**(alpha+1) - (k-alpha) * (k+1)**alpha",
            "    aw[1:] = ((k-jj[1:]+2)**(alpha+1) + (k-jj[1:])**(alpha+1)",
            "              - 2 * (k-jj[1:]+1)**(alpha+1))",
            "    aw *= dt**alpha / ga2",
            "    h[:, k+1] = Fh[:, : k+1] @ aw + dt**alpha / ga2 * F(hp)",
            "    Fh[:, k+1] = F(h[:, k+1])                   # corrector",
        ], source="explainer/quant/house/rough.py: frac_riccati", width=8.4).to_edge(UP, buff=0.25).to_edge(LEFT, buff=0.4)
        conv = a["conv"]
        outs = ["steps n    " + "  ".join(f"{c['n']:>7d}" for c in conv),
                "max error  " + "  ".join(f"{c['err']:7.1e}" for c in conv),
                f"observed order {a['order']:.2f};  H = 1/2 against Heston's closed form: {a['heston_err']:.0e}"]
        match = ("to better than one part in a million" if a["heston_err"] < 1e-6 else
                 "to within a few parts in a million" if a["heston_err"] < 1e-5 else "closely, though not exactly")
        q = pause(r"Double the number of Adams steps. By how much does the error shrink?", width=4.6,
                  font_size=20).to_corner(UR, buff=0.3)
        with self.voiceover(
            f"The House's code: the predictor weights, the corrector weights, and the update, a few lines for all frequencies at once. <bookmark mark='a'/> Pause and predict: double the number of steps. By how much does the error shrink? <bookmark mark='b'/> Run it against a solution with sixteen hundred steps. The error falls by about three each time the steps double: an observed order of {a['order']:.1f}. And with H set to one half, the scheme matches Heston's closed-form characteristic function {match}. The fitted order is specific to this parameter set, frequency grid and sixteen-hundred-step reference; it is not a universal Adams convergence theorem."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("b")
            lab_run(self, card, outs, run_time=3, font_size=17)
        self.wait(0.5)
        self.clear_scene()

    def surface(self, a):
        ug = np.asarray(a["u_grid"])
        Tg = np.log10(np.asarray(a["T_grid"]))
        Z = {k: np.asarray(v).T for k, v in a["absphi"].items()}   # (u, T)
        ax = ThreeDAxes(x_range=[0, ug[-1], 5], y_range=[Tg[0], 0, 1], z_range=[0, 1, 0.5], x_length=6.4, y_length=5.0,
                        z_length=3.0, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False})
        ax.shift(DOWN * 0.4)

        def surf(key, col):
            f = RegularGridInterpolator((ug, Tg), Z[key])
            s = Surface(lambda u, v: ax.c2p(u, v, float(f((u, v)))), u_range=[ug[0], ug[-1]], v_range=[Tg[0], Tg[-1]],
                        resolution=(24, 16), fill_opacity=0.8, stroke_width=0.3, stroke_color=GREY_D)
            s.set_fill(col, opacity=0.8)
            return s

        s5, s1 = surf("0.5", VAR), surf("0.1", ROUGH)
        hint = VGroup(label(r"frequency $u$ (0 to 25)", font_size=20, color=GREY_A),
                      label(r"maturity: 2 days to 1 year (log)", font_size=20, color=GREY_A),
                      label(r"height: $|\varphi(u, T)|$", font_size=20, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).to_corner(UL, buff=0.3)
        tag = label(r"$H = \tfrac12$ (Heston)", font_size=26, color=VAR).to_corner(UR, buff=0.4)
        tag2 = label(r"$H = 0.1$", font_size=26, color=ROUGH).to_corner(UR, buff=0.4)
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint, tag)
        self.remove(hint, tag)
        with self.voiceover(
            """Here is the modulus of the computed characteristic function over frequency and maturity, first at the Heston limit. At zero frequency a normalized characteristic function equals one. <bookmark mark='a'/> Now change H to one tenth while holding the other parameters fixed. The numerical modulus changes. It describes attenuation in Fourier space, but it cannot identify the sign of skewness: reflecting a distribution leaves this modulus unchanged. Nor does a lower ridge alone prove a wider distribution in every sense. The complex characteristic function, and then actual option prices, contain the smile information."""
        ) as vo:
            self.play(FadeIn(hint), FadeIn(tag), Create(ax), FadeIn(s5), run_time=2)
            self.move_camera(theta=-80 * DEGREES, run_time=3)
            vo.wait_until("a")
            self.add_fixed_in_frame_mobjects(tag2)
            self.remove(tag2)
            self.play(Transform(s5, s1), FadeOut(tag), FadeIn(tag2), run_time=3)
            self.move_camera(theta=-30 * DEGREES, phi=70 * DEGREES, run_time=max(vo.remaining(0.0) - 0.5, 2))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0,
                         added_anims=[FadeOut(VGroup(ax, s5)), FadeOut(hint), FadeOut(tag2)], run_time=1.2)
        self.clear_scene()

    def profile(self, p):
        rows = p["rows"]
        Hs = np.array([r["H"] for r in rows])
        E = np.array([r["rmse"] for r in rows])
        free = p["free"]
        er = data_range(E, [free["rmse"]])
        g = axes([0, 0.52], list(er), x_length=6.0, y_length=4.0, xlabel=r"$H$, held fixed (other five refitted)",
                 ylabel=r"error on the Surface (vol points)", xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5],
                 yticks=[1, 2, 3, 4], font_size=15).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        t = ValueTracker(0)
        dots = always_redraw(lambda: VGroup(*[Dot(ax.c2p(h, e), radius=0.07, color=MODEL_COL["rough Heston"])
                                              for h, e in zip(Hs[: int(t.get_value()) + 1], E[: int(t.get_value()) + 1])]))
        line = curve(ax, Hs, E, MODEL_COL["rough Heston"], stroke_width=2.5)
        star = Star(n=5, outer_radius=0.14, color=YELLOW, fill_opacity=1).move_to(ax.c2p(free["H"], free["rmse"]))
        ts = Rectangle(width=ax.c2p(0.12, 0)[0] - ax.c2p(0.08, 0)[0], height=4.0, stroke_width=0, fill_color=RV,
                       fill_opacity=0.25).move_to(ax.c2p(0.10, sum(er) / 2))
        tsl = label(r"time series: $H \approx 0.08$--$0.12$", font_size=16, color=RV).next_to(ts, UP, buff=0.05)
        # error by expiry at three H values
        days = sorted(int(d) for d in rows[0]["by_expiry"])
        pick = [r for r in rows if abs(r["H"] - 0.05) < 1e-9 or abs(r["H"] - 0.2) < 1e-9 or abs(r["H"] - 0.5) < 1e-9]
        expiry_top = 1.08 * max(v for r in pick for v in r["by_expiry"].values())
        g2 = axes([-0.5, len(days) - 0.5], [0, expiry_top], x_length=5.0, y_length=3.2, xlabel=r"expiry (days)",
                  ylabel=r"error by expiry", xticks=list(range(len(days))), xfmt=lambda u: f"{days[int(round(u))]}",
                  yticks=[0, 5, 10], font_size=13).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)
        cols = [ROUGH, IV, VAR]
        bars = VGroup()
        for j, (r, c) in enumerate(zip(pick, cols)):
            for i, d in enumerate(days):
                v = r["by_expiry"][str(d)]
                bars.add(Rectangle(width=0.18, height=max(g2.ax.c2p(0, v)[1] - g2.ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                   fill_color=c, fill_opacity=0.85).move_to(g2.ax.c2p(i - 0.2 + 0.2 * j, v / 2)))
        leg2 = legend([(c, rf"$H = {r['H']:g}$") for r, c in zip(pick, cols)], font_size=15).arrange(RIGHT, buff=0.25).next_to(
            g2, UP, buff=0.15)
        e05 = next(r for r in rows if abs(r["H"] - 0.05) < 1e-9)
        e01 = next(r for r in rows if abs(r["H"] - 0.1) < 1e-9)
        src = real_data(r"the Surface, 10 December 2025; 9 fits of rough Heston, Adams + COS", corner=DL)
        with self.voiceover(
            f"""Fix H at nine values and refit the other five parameters. <bookmark mark='a'/> Error is {e05['rmse']:.2f} at H of point zero five, {e01['rmse']:.2f} at one tenth, and {free['rmse']:.2f} at the free fit's H of {free['H']:.2f}. The green range describes time-series proxy estimates, not a confidence interval for risk-neutral H. <bookmark mark='b'/> Expiry bars preserve all errors, including the largest short-date mismatch. These local numerical fits on one date favor larger H under this objective and budget; they do not identify a universal market H. Next: a possible order-flow mechanism."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(ts), FadeIn(tsl), FadeIn(dots))
            self.play(t.animate.set_value(len(Hs) - 1), run_time=5, rate_func=linear)
            vo.wait_until("a")
            self.play(Create(line), FadeIn(star))
            vo.wait_until("b")
            self.play(FadeIn(g2), FadeIn(leg2), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03))
        dots.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
