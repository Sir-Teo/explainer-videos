from __future__ import annotations

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, DELTA, GOOD, OPT, PART, fixed, illustration, load, loglog, polyline, predict, axes, data_range, pause_card, flat_camera


class ADI(VoiceoverScene, ThreeDScene):
    def construct(self):
        a = load("adi")
        ag = load("adi_grid")
        self.card()
        self.sweeps(ag)
        self.split()
        self.grids(a, ag)

    def card(self):
        c = chapter_card(14, r"ADI for Heston", r"How do you step a two-dimensional PDE without a huge matrix?", part=PART)
        with self.voiceover("Chapter fourteen. ADI for Heston: two dimensions, one direction at a time."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sweeps(self, ag):
        S, v = np.asarray(ag["S"]), np.asarray(ag["v"])
        ax = ThreeDAxes(x_range=[60, 140, 20], y_range=[0, 0.2, 0.05], z_range=[0, 45, 15], x_length=7.0, y_length=5.0,
                        z_length=3.0, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False,
                                                               "stroke_width": 2})
        ax.shift(DOWN * 0.4)

        def surf(Z, lo, hi, colors):
            f = RegularGridInterpolator((v, S), np.asarray(Z))
            zmin, zmax = float(np.min(Z)), float(np.max(Z))
            sc = lambda z: lo + (hi - lo) * (z - zmin) / (zmax - zmin + 1e-12)  # noqa: E731
            sf = Surface(lambda x, y: ax.c2p(x, y, sc(float(f((y, x))))), u_range=[60, 140], v_range=[0, 0.2],
                         resolution=(32, 16), fill_opacity=0.85, stroke_width=0.3, stroke_color="#0E1117",
                         checkerboard_colors=False)
            sf.set_fill_by_value(axes=ax, colorscale=list(zip(colors, [lo, (lo + hi) / 2, hi])), axis=2)
            return sf

        price = surf(ag["u"], 0, 45, [QC.SPOT, QC.OPTION, QC.LOSS])
        delta = surf(ag["delta"], 0, 40, [QC.SPOT, DELTA, QC.LOSS])
        gamma = surf(ag["gamma"], 0, 40, [QC.SPOT, QC.GAMMA, QC.LOSS])
        vega = surf(ag["vega"], 0, 40, [QC.SPOT, QC.VEGA, QC.LOSS])
        gS = [s for s in ag["gridS"] if 60 <= s <= 140]
        gv = [x for x in ag["gridv"] if x <= 0.2]
        rows = VGroup(*[Line(ax.c2p(60, y, 0), ax.c2p(140, y, 0), stroke_color=GREY_B, stroke_width=1) for y in gv])
        cols = VGroup(*[Line(ax.c2p(x, 0, 0), ax.c2p(x, 0.2, 0), stroke_color=GREY_B, stroke_width=1) for x in gS])
        hint = VGroup(label(r"across: spot $S$", font_size=21, color=GREY_A),
                      label(r"back: variance $v$", font_size=21, color=GREY_A),
                      label(r"up: the Heston call $u(S, v)$", font_size=21, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        names = [label(t, font_size=26, color=c).to_corner(UR, buff=0.4) for t, c in
                 ((r"price", OPT), (r"delta $\partial_S u$", DELTA), (r"gamma $\partial_{SS} u$", QC.GAMMA),
                  (r"vega $\partial_v u$ (to variance)", QC.VEGA))]
        stage = [label(r"sweep 1: implicit along $S$, one row of the grid at a time", font_size=22, color=QC.THETA),
                 label(r"sweep 2: implicit along $v$, one column at a time", font_size=22, color=GOOD)]
        for st in stage:
            st.to_edge(DOWN, buff=0.3)
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=0.85)
        fixed(self, hint, *names, *stage)
        with self.voiceover(
            "Stochastic volatility adds a dimension: Heston's price is a function of the spot and of the variance. "
            "Seen from above, the House's grid is not uniform. The price lines crowd around the strike and the "
            "variance lines crowd near zero, where the solution bends fastest. <bookmark mark='a'/> Each time step "
            "is done in two sweeps. First, implicitly along the price, a small tridiagonal system for every row of "
            "the grid. <bookmark mark='b'/> Then implicitly along the variance, one system per column. "
            "<bookmark mark='c'/> Tilt the camera and the solution appears: the price surface, rising with spot and "
            "with variance. <bookmark mark='d'/> And because the grid holds the whole surface, the Greeks come free: "
            "delta, gamma and the sensitivity to variance, read off by differences."
        ) as vo:
            self.play(FadeIn(hint), Create(rows), Create(cols), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(stage[0]), LaggedStart(*[Indicate(r_, color=QC.THETA, scale_factor=1.0) for r_ in rows],
                                                    lag_ratio=0.08, run_time=3))
            vo.wait_until("b")
            self.play(FadeOut(stage[0]), FadeIn(stage[1]),
                      LaggedStart(*[Indicate(c_, color=GOOD, scale_factor=1.0) for c_ in cols], lag_ratio=0.05, run_time=3))
            vo.wait_until("c")
            self.play(FadeOut(stage[1]), Create(ax))
            self.move_camera(phi=65 * DEGREES, theta=-60 * DEGREES, added_anims=[Create(price), FadeIn(names[0])],
                             run_time=3)
            vo.wait_until("d")
            for k, sf in enumerate((delta, gamma, vega), 1):
                self.play(ReplacementTransform(price if k == 1 else (delta, gamma)[k - 2], sf), FadeOut(names[k - 1]),
                          FadeIn(names[k]), run_time=1.6)
                self.wait(0.6)
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, vega, rows, cols)), FadeOut(hint),
                                                                  FadeOut(names[3])], run_time=1.5)
        self.clear_scene()
        flat_camera(self)

    def split(self):
        rows = [
            cmath(r"\partial_\tau u", r"=", r"\tfrac12 vS^2u_{SS} + \rho\xi vS\,u_{Sv} + \tfrac12\xi^2 v\,u_{vv} + rSu_S + "
                  r"\kappa(\theta - v)u_v - ru", font_size=30, colors={r"\partial_\tau u": OPT}),
            cmath(r"A", r"=", r"A_0 + A_1 + A_2\quad(\text{mixed},\ S\text{-direction},\ v\text{-direction})", font_size=32),
            cmath(r"Y_0", r"=", r"U^n + \Delta\tau\,AU^n,\quad (I - \vartheta\Delta\tau A_j)\,Y_j = Y_{j-1} - "
                  r"\vartheta\Delta\tau A_jU^n,\ j = 1, 2", font_size=30, colors={r"Y_0": QC.THETA}),
            cmath(r"\hat Y_0", r"=", r"Y_0 + \tfrac12\Delta\tau\,(A_0Y_2 - A_0U^n),\ \text{then the two implicit sweeps again}",
                  font_size=30, colors={r"\hat Y_0": GOOD}),
            cmath(r"S_i", r"=", r"K + c\,\sinh\xi_i\ \ (\xi_i\ \text{uniform}),\quad v_j = d\,\sinh\eta_j", font_size=32,
                  colors={r"S_i": DELTA}),
        ]
        whys = [why(r"Heston's pricing equation (Part 13): Feynman--Kac on the two-dimensional state"),
                why(r"split the operator by direction; the correlation's mixed derivative is $A_0$"),
                why(r"Douglas: explicit predictor, then one implicit correction per direction, each a set of tridiagonal "
                    r"systems: $O(N)$ work per step, against far more for a sparse two-dimensional solve"),
                why(r"Craig and Sneyd (1988): correct the explicit mixed term; second order with $\vartheta = \tfrac12$. "
                    r"In 't Hout and Foulon (2010) compared this with MCS and Hundsdorfer--Verwer"),
                why(r"spacing $\propto \cosh\xi$, smallest at $K$ (and near $v = 0$); three-point weights on uneven "
                    r"spacing keep second order if the map is smooth")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-4.2, buff=0.5, edge=6.9)  # short left sides: room on the right
        with self.voiceover(
            "The scheme. Heston's pricing equation has second derivatives in price and in variance, and a mixed "
            "derivative from their correlation. <bookmark mark='a'/> Split its operator into three: the mixed part, "
            "the price direction and the variance direction. <bookmark mark='b'/> Douglas's scheme takes an explicit "
            "step with everything, then corrects implicitly in one direction at a time. Each correction is a stack of "
            "tridiagonal systems, linear in the number of grid points. <bookmark mark='c'/> The mixed term stays "
            "explicit, which costs accuracy; Ian Craig and Andrew Sneyd's 1988 scheme corrects it with one more "
            "explicit stage and a second pair of sweeps. Karel in 't Hout and Sean Foulon compared the variants on "
            "Heston in 2010. <bookmark mark='d'/> And the grid: uniform in a stretched coordinate, mapped through a "
            "hyperbolic sine, so the points crowd where the action is."
        ) as vo:
            for i, mk in enumerate("abcd"):
                step(i)
                vo.wait_until(mk)
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def grids(self, a, ag):
        rows = ag["rows"]
        g = axes([0, 4], [-3, 1], x_length=5.4, y_length=4.0, xlabel=r"grid (price $\times$ variance points)",
                 ylabel=r"error against COS ($\log_{10}$)", xticks=[1, 2, 3],
                 xfmt=lambda v: [r"40\times20", r"80\times40", r"160\times80"][int(round(v)) - 1], yticks=[-3, -2, -1, 0, 1],
                 font_size=14).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i, n in enumerate((40, 80, 160), 1):
            for dx, uni, col in ((-0.17, True, BAD), (0.17, False, GOOD)):
                r = next(x for x in rows if x["nS"] == n and x["uniform"] == uni)
                y = np.log10(r["err"])
                bars.add(Rectangle(width=0.3, height=abs(ax.c2p(0, y)[1] - ax.c2p(0, -3)[1]), stroke_width=0,
                                   fill_color=col, fill_opacity=0.8).move_to(ax.c2p(i + dx, -3), aligned_edge=DOWN))
        leg = legend([(BAD, r"uniform grid"), (GOOD, r"sinh grid (in 't Hout--Foulon)")], font_size=16)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        e = {(r["nS"], r["uniform"]): r["err"] for r in rows}
        h = loglog(np.log10(15), np.log10(220), -4, 0, r"price points", r"error, Douglas and Craig--Sneyd", x_length=4.4,
                   y_length=2.8, xt=[2], yt=[-4, -2, 0], font_size=13).to_edge(RIGHT, buff=0.6).shift(UP * 1.25)
        cols = {"do": BAD, "cs": GOOD}
        lines = VGroup()
        for sch in ("do", "cs"):
            rr = [r for r in a["rows"] if r["scheme"] == sch]
            lines.add(polyline(h.ax, np.log10([r["nS"] for r in rr]), np.clip(np.log10([max(r["err"], 1e-6) for r in rr]), -4, 0),
                               cols[sch], radius=0.04))
        leg2 = legend([(BAD, r"Douglas"), (GOOD, r"Craig--Sneyd")], font_size=14).next_to(h, DOWN, buff=0.15).align_to(h, LEFT)
        best = min(a["rows"], key=lambda r: r["err"])
        side = MathTex(rf"{best['nS']}\times{best['nv']}:\ {best['price']:.4f}\ \text{{vs COS}}\ {a['ref']:.4f}\ "
                       rf"({best['time']:.1f}\,\text{{s}})", font_size=24, color=GOOD).next_to(leg2, DOWN, buff=0.25)
        side.align_to(h, LEFT)
        q = predict(r"Why crowd the variance grid near $v = 0$?", width=4.4, font_size=20).to_corner(DR, buff=0.2)
        with self.voiceover(
            "Does the stretching matter? Measured against the exact Fourier price: on a forty by twenty grid, a "
            f"uniform grid is off by {e[(40, True)]:.2f}; the stretched grid by {e[(40, False)]:.3f}, "
            f"{e[(40, True)] / e[(40, False)]:.0f} times better. At a hundred and sixty points the gap is "
            f"{e[(160, True)] / e[(160, False)]:.0f} times. <bookmark mark='a'/> On the stretched grid both schemes "
            "converge fast. Here, with Feller's condition broken and strong correlation, Douglas is slightly ahead; in "
            "'t Hout and Foulon found the ranking depends on the case, which is why desks keep several. The finest "
            f"grid prices the call to {best['err']:.4f} in {best['time']:.1f} seconds on one core. "
            "<bookmark mark='b'/> Pause and predict: why crowd the variance near zero? Because the variance spends "
            "time there when Feller's condition fails, and the solution bends most sharply there."
            " When the characteristic function is known, there is a faster road still. Next: Fourier."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2, run_time=2.5))
            vo.wait_until("a")
            self.play(FadeIn(h), Create(lines), FadeIn(leg2), FadeIn(side))
            vo.wait_until("b")
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
