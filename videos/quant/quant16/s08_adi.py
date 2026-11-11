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
        ax = ThreeDAxes(x_range=[60, 140, 20], y_range=[0, 0.2, 0.05], z_range=[0, 1, 0.5], x_length=7.0, y_length=5.0,
                        z_length=3.0, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False,
                                                               "stroke_width": 2})
        ax.shift(DOWN * 0.4)

        def surf(Z, lo, hi, colors):
            f = RegularGridInterpolator((v, S), np.asarray(Z))
            zmin, zmax = float(np.min(Z)), float(np.max(Z))
            sc = lambda z: (z - zmin) / (zmax - zmin) if zmax > zmin else 0.0  # noqa: E731
            sf = Surface(lambda x, y: ax.c2p(x, y, sc(float(f((y, x))))), u_range=[60, 140], v_range=[0, 0.2],
                         resolution=(32, 16), fill_opacity=0.85, stroke_width=0.3, stroke_color="#0E1117",
                         checkerboard_colors=False)
            sf.set_fill_by_value(axes=ax, colorscale=list(zip(colors, [0, 0.5, 1])), axis=2)
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
                      label(r"up: shape only; each surface separately scaled to $[0,1]$", font_size=21, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        names = [label(t, font_size=26, color=c).to_corner(UR, buff=0.4) for t, c in
                 ((r"price", OPT), (r"delta $\partial_S u$", DELTA), (r"gamma $\partial_{SS} u$", QC.GAMMA),
                  (r"variance-state derivative $\partial_v u$", QC.VEGA))]
        def tex_number(value):
            if value == 0 or 0.001 <= abs(value) < 1000:
                return f"{value:.3g}"
            mantissa, exponent = f"{value:.2e}".split("e")
            return mantissa + r"\times 10^{" + str(int(exponent)) + "}"

        for i, key in enumerate(("u", "delta", "gamma", "vega")):
            actual = np.asarray(ag[key])
            names[i] = VGroup(names[i], label(rf"actual range: ${tex_number(actual.min())}$ to ${tex_number(actual.max())}$",
                                             font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=RIGHT, buff=0.15).to_corner(UR, buff=0.4)
        stage = [label(r"sweep 1: implicit along $S$, one row of the grid at a time", font_size=22, color=QC.THETA),
                 label(r"sweep 2: implicit along $v$, one column at a time", font_size=22, color=GOOD)]
        for st in stage:
            st.to_edge(DOWN, buff=0.3)
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=0.85)
        fixed(self, hint, *names, *stage)
        with self.voiceover(
            "Heston adds variance as a state variable. The nonuniform grid crowds stock nodes around the strike and variance nodes near zero, where boundary behaviour can require resolution. <bookmark mark='a'/> A directional correction solves a tridiagonal system along each stock row. <bookmark mark='b'/> Another solves along each variance column. <bookmark mark='c'/> The tilted surface shows the computed solution's shape. Height is separately rescaled from zero to one for each surface; the displayed actual minimum and maximum preserve its units and range. These heights must not be compared as if they shared price units. <bookmark mark='d'/> Finite differences on the computed surface estimate delta, gamma and the variance-state derivative. The last is partial u over partial v, not the usual volatility vega. These extra differences are cheap, but their accuracy still depends on the numerical solution and grid."
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
                    r"systems: $O(N)$ directional work, avoiding a global 2D factorization; some multigrid solvers can also achieve $O(N)$"),
                why(r"Douglas with a mixed term is generally first order in time; Craig--Sneyd with $\vartheta=\frac12$ is second order under suitable regularity and boundary treatment. "
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
        bar_yr = data_range([np.log10(r["err"]) for r in rows])
        baseline = bar_yr[0]
        g = axes([0, 4], bar_yr, x_length=5.4, y_length=4.0, xlabel=r"grid (price $\times$ variance points)",
                 ylabel=r"error against COS ($\log_{10}$)", xticks=[1, 2, 3],
                 xfmt=lambda v: [r"40\times20", r"80\times40", r"160\times80"][int(round(v)) - 1], yticks=[-3, -2, -1, 0, 1],
                 font_size=14).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i, n in enumerate((40, 80, 160), 1):
            for dx, uni, col in ((-0.17, True, BAD), (0.17, False, GOOD)):
                r = next(x for x in rows if x["nS"] == n and x["uniform"] == uni)
                y = np.log10(r["err"])
                bars.add(Rectangle(width=0.3, height=abs(ax.c2p(0, y)[1] - ax.c2p(0, baseline)[1]), stroke_width=0,
                                   fill_color=col, fill_opacity=0.8).move_to(ax.c2p(i + dx, baseline), aligned_edge=DOWN))
        leg = legend([(BAD, r"uniform grid"), (GOOD, r"sinh grid (in 't Hout--Foulon)")], font_size=16)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        e = {(r["nS"], r["uniform"]): r["err"] for r in rows}
        h = loglog(*data_range(np.log10([r["nS"] for r in a["rows"]])),
                   *data_range(np.log10([r["err"] for r in a["rows"]])), r"price points", r"error, Douglas and Craig--Sneyd", x_length=4.4,
                   y_length=2.8, xt=[2], yt=[-4, -2, 0], font_size=13).to_edge(RIGHT, buff=0.6).shift(UP * 1.25)
        cols = {"do": BAD, "cs": GOOD}
        lines = VGroup()
        for sch in ("do", "cs"):
            rr = [r for r in a["rows"] if r["scheme"] == sch]
            lines.add(polyline(h.ax, np.log10([r["nS"] for r in rr]), np.log10([r["err"] for r in rr]),
                               cols[sch], radius=0.04))
        leg2 = legend([(BAD, r"Douglas"), (GOOD, r"Craig--Sneyd")], font_size=14).next_to(h, DOWN, buff=0.15).align_to(h, LEFT)
        best = min(a["rows"], key=lambda r: r["err"])
        side = MathTex(rf"{best['nS']}\times{best['nv']}:\ {best['price']:.4f}\ \text{{vs COS}}\ {a['ref']:.4f}\ "
                       rf"({best['time']:.1f}\,\text{{s}})", font_size=24, color=GOOD).next_to(leg2, DOWN, buff=0.25)
        side.align_to(h, LEFT)
        q = predict(r"Why crowd the variance grid near $v = 0$?", width=4.4, font_size=20).to_corner(DR, buff=0.2)
        with self.voiceover(
            f"The reference is a numerical COS price, rather than an exact oracle. With forty by twenty nodes, the uniform-grid discrepancy is {e[(40, True)]:.2f}, while the stretched-grid discrepancy is {e[(40, False)]:.3f}. At one hundred and sixty stock nodes the ratio is {e[(160, True)] / e[(160, False)]:.0f}. Domain, boundary, time, space and reference errors all enter this comparison. <bookmark mark='a'/> Both directional schemes improve over these saved grids. Their ranking is case-dependent; the best displayed discrepancy is {best['err']:.4f} in {best['time']:.1f} recorded seconds. It is not a general accuracy or timing guarantee. <bookmark mark='b'/> When Feller's condition fails, zero variance is attainable, and near-zero behaviour can make variance-grid resolution important. This does not imply positive time spent exactly at zero or that curvature is always maximal there. Next, characteristic-function pricing."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2, run_time=2.5))
            vo.wait_until("a")
            self.play(FadeIn(h), Create(lines), FadeIn(leg2), FadeIn(side))
            vo.wait_until("b")
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
