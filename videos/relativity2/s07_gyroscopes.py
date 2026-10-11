from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity2.common import (View3D, clamp_x, curve3d, label, ladder, load, mtex, note, part_card, redraw,
                                       under)

SPIN = C.SPIN
GYRO = C.VECTOR


class Gyroscopes(VoiceoverScene):
    def construct(self):
        self.card()
        self.gravitomagnetism()
        self.dragging()
        self.geodetic()
        self.cone()
        self.gpb()

    def card(self):
        c = part_card("II", r"Spinning spacetime", r"gyroscopes, frame dragging, and the Kerr black hole")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def gravitomagnetism(self):
        rows = [
            mtex(r"\Box\,\bar h_{\mu\nu}", r"=", r"-16\pi\,T_{\mu\nu}", font_size=42),
            mtex(r"\nabla^2\bar h_{00}", r"=", r"-16\pi\rho\quad\Rightarrow\quad \bar h_{00} = -4\Phi", font_size=40),
            mtex(r"\nabla^2\bar h_{0i}", r"=", r"16\pi\,\rho\, v_i", font_size=42),
            mtex(r"h_{0i}", r"=", r"-\frac{2\,(\mathbf{J}\times\mathbf{x})_i}{r^3}\quad\Rightarrow\quad g_{t\phi} = -\frac{2J\sin^2\theta}{r}",
                 font_size=40),
        ]
        whys = [
            note(r"part 1's linearized field equation ($G = c = 1$)"),
            note(r"a static source: Newton's $\nabla^2\Phi = 4\pi\rho$ again"),
            note(r"a moving source: mass currents $T_{0i} = -\rho v_i$ source the $0i$ part, like currents source $\mathbf{A}$ in magnetism"),
            note(r"far from a body with angular momentum $\mathbf{J}$: the analogue of a magnetic dipole's field"),
        ]
        rows[0][2].set_color(C.MATTER)
        rows[2][2].set_color(C.MATTER)
        rows[3][0].set_color(SPIN)
        rows[3][2].set_color(SPIN)
        under(rows, whys, -1.4)
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.4, buff=0.62)
        name = label(r"gravitomagnetism: moving mass makes a ``magnetic'' part of gravity", font_size=28, color=SPIN)
        name.to_edge(DOWN, buff=0.4)
        q = label(r"What changes when the mass moves, or spins?", font_size=40)
        with self.voiceover(
            "In part one, Mercury and the bending of light came from a mass sitting still. What changes when the mass "
            "moves, or spins? <bookmark mark='a'/> Go back to the linearized field equation. <bookmark mark='b'/> For a "
            "static source, the time-time part gives Newton's potential. <bookmark mark='c'/> But a moving source also "
            "has momentum, and mass currents feed the time-space part of the metric, through exactly the equation "
            "electric currents use to make a magnetic vector potential. <bookmark mark='d'/> Far from a spinning body, "
            "the solution has the shape of a magnetic dipole's field, with the angular momentum J playing the role of "
            "the magnetic moment."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(FadeOut(q), run_time=0.5)
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(FadeIn(name))
        self.clear_scene()

    # ------------------------------------------------------------------
    def dragging(self):
        eq = VGroup(
            mtex(r"\frac{d\phi}{dt}\Big|_{L=0}", r"=", r"\omega = -\frac{g_{t\phi}}{g_{\phi\phi}} = \frac{2J}{r^3}", font_size=40),
            label(r"something dropped with zero angular momentum circles anyway: frame dragging", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.35)
        eq[0][0].set_color(SPIN)
        lt = VGroup(
            mtex(r"\boldsymbol{\Omega}_{\rm LT}", r"=", r"\frac{1}{r^3}\Big[3(\mathbf{J}\cdot\hat{\mathbf{r}})\hat{\mathbf{r}} - \mathbf{J}\Big]",
                 font_size=38),
            label(r"a gyroscope's spin precesses at this rate: Lense \& Thirring (1918)", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.12).next_to(eq, DOWN, buff=0.3).to_edge(LEFT, buff=0.6)
        lt[0][0].set_color(GYRO)
        # dipole picture in a meridian plane: field lines r = C sin^2 theta, and Omega arrows
        cen = np.array([3.1, -1.2, 0])
        R = 0.65
        earth = Circle(radius=R, color=C.MATTER, stroke_width=3, fill_color=C.MATTER, fill_opacity=0.25).move_to(cen)
        axis = Arrow(cen + DOWN * 1.1, cen + UP * 1.35, buff=0, color=SPIN, stroke_width=5)
        jl = mtex(r"\mathbf{J}", font_size=34, color=SPIN).next_to(axis.get_end(), UP, buff=0.05)
        lines = VGroup()
        th = np.linspace(0.02, np.pi - 0.02, 200)
        for Cc in (1.2, 1.7, 2.4, 3.4):
            r = Cc * np.sin(th) ** 2
            for sgn in (1, -1):
                P = np.stack([cen[0] + sgn * r * np.sin(th), cen[1] + r * np.cos(th), 0 * th], 1)
                P = P[r > R * 1.02]
                P = P[(P[:, 1] < 2.0) & (P[:, 1] > -3.8)]
                if len(P) > 2:
                    lines.add(VMobject(stroke_color=GYRO, stroke_width=1.6, stroke_opacity=0.55).set_points_as_corners(P))
        arrows = VGroup()
        for (x, y) in [(0, 1.25), (0, -1.25), (1.3, 0), (-1.3, 0), (1.0, 0.9), (-1.0, 0.9), (1.0, -0.9), (-1.0, -0.9),
                       (1.9, 0.0), (-1.9, 0.0)]:
            p = np.array([x, y])
            r = np.linalg.norm(p)
            rh = p / r
            J = np.array([0, 1.0])
            Om = (3 * (J @ rh) * rh - J) / r**3
            Om = Om / np.linalg.norm(Om) * min(0.55, 0.5 * np.linalg.norm(Om) ** 0.4)
            a = Arrow(cen + [x, y, 0], cen + [x + Om[0], y + Om[1], 0], buff=0, color=GYRO, stroke_width=4,
                      max_tip_length_to_length_ratio=0.35)
            arrows.add(a)
        sense = VGroup(label(r"over the poles: with the spin", font_size=22, color=GYRO),
                       label(r"at the equator: against it", font_size=22, color=GYRO)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        sense.move_to([-3.6, -2.6, 0])
        with self.voiceover(
            "This gravitomagnetic field has two effects. <bookmark mark='a'/> First, it drags things around. Drop "
            "something with zero angular momentum near a spinning body, and it doesn't fall straight in: it circles, "
            "with angular velocity two J over r cubed. Spacetime itself is being dragged around by the rotation. "
            "<bookmark mark='b'/> Second, it twists gyroscopes. A gyroscope's spin axis precesses at a rate with the "
            "shape of a dipole field, worked out by Lense and Thirring in 1918. <bookmark mark='c'/> Over the poles, "
            "the gyroscope is dragged along with the rotation; at the equator, the other way."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(eq, lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(lt, lag_ratio=0.2))
            self.play(FadeIn(earth), GrowArrow(axis), FadeIn(jl))
            self.play(Create(lines), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), FadeIn(sense), run_time=2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def geodetic(self):
        g = load("gpb")
        taus, ang = g["spin_tau"], g["spin_ang"]
        geo10 = float(g["geo_10"])
        assert abs(math.degrees(geo10) - 58.8) < 0.1
        r = 10.0
        up = math.sqrt(1 / r**3) / math.sqrt(1 - 3 / r)
        cen = np.array([-3.0, -0.4, 0])
        Rs = 2.3
        hole = Circle(radius=0.46, color=C.CURVATURE, stroke_width=3, fill_color=BLACK, fill_opacity=1).move_to(cen)
        orbit = Circle(radius=Rs, color=GREY_B, stroke_width=1.5).move_to(cen)
        k = ValueTracker(0.0)

        def gyro():
            j = int(k.get_value() * (len(taus) - 1))
            phi = up * taus[j]
            pos = cen + Rs * np.array([math.cos(phi), math.sin(phi), 0])
            a = phi + ang[j]
            d = 0.75 * np.array([math.cos(a), math.sin(a), 0])
            grp = VGroup(Arrow(pos - d / 2, pos + d / 2, buff=0, color=GYRO, stroke_width=6,
                               max_tip_length_to_length_ratio=0.3),
                         Dot(pos, radius=0.07, color=WHITE))
            return grp

        G = redraw(gyro)
        start = Arrow(cen + Rs * RIGHT - 0.375 * RIGHT, cen + Rs * RIGHT + 0.375 * RIGHT, buff=0, color=GYRO,
                      stroke_width=4, max_tip_length_to_length_ratio=0.3).set_opacity(0.35)
        eq = VGroup(
            mtex(r"\Delta\phi_{\rm geodetic}", r"=", r"2\pi\Big(1 - \sqrt{1 - \tfrac{3M}{r}}\Big)", font_size=38),
            label(r"per circular orbit, exactly; \ $\approx 3\pi M/r$ in weak gravity", font_size=24, color=GREY_A),
            mtex(r"r = 10M:\quad 58.8^\circ \text{ per orbit}", font_size=34, color=GYRO),
            note(r"computed: the spin vector parallel-transported around the orbit"),
            note(r"(near the Earth, $3\pi M/r \approx 2\times10^{-9}$: exaggerated $\sim 10^{8}\times$)"),
        ).arrange(DOWN, buff=0.18).move_to([3.4, 0.4, 0])
        eq[0][0].set_color(GYRO)
        with self.voiceover(
            "There's a second, larger effect on gyroscopes, which doesn't need rotation at all. <bookmark mark='a'/> "
            "Send a gyroscope around a mass in a circular orbit, its spin axis pointing outward to start. A gyroscope "
            "is the best definition of a fixed direction we have: its spin is parallel transported along its worldline. "
            "<bookmark mark='b'/> Yet after one orbit, it no longer points where it started. <bookmark mark='c'/> "
            "Computed exactly, it has turned by two pi times one minus the square root of one minus three M over r, "
            "in the direction of the orbit: fifty-nine degrees per orbit at r equals ten M. This is geodetic "
            "precession, predicted by Willem de Sitter in 1916."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hole), Create(orbit))
            self.add(G)
            self.play(FadeIn(start))
            vo.wait_until("b")
            self.play(k.animate.set_value(1.0), run_time=6, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(eq, lag_ratio=0.2))
        G.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def cone(self):
        g = load("gpb")
        P, Vs = g["flamm_path"], g["flamm_vecs"]
        flamm10 = float(g["flamm_10"])
        wedge = math.degrees(flamm10)
        assert abs(wedge - 38.0) < 0.1 and abs(wedge - math.degrees(2 * math.pi * (1 - math.sqrt(0.8)))) < 1e-4
        view = View3D(center=[-3.6, -0.9, 0], scale=0.26, azimuth=0.5, elevation=0.5)
        rr = np.linspace(2, 14, 120)
        zz = 2 * np.sqrt(2 * (rr - 2))
        surf = VGroup()
        a = np.linspace(0, 2 * np.pi, 120)
        for r0 in (2.0, 3.0, 5.0, 7.5, 10.0, 12.5):
            z0 = 2 * math.sqrt(2 * (r0 - 2))
            Q = np.stack([r0 * np.cos(a), r0 * np.sin(a), np.full_like(a, z0)], 1)
            surf.add(curve3d(view, Q, color=C.METRIC, stroke_width=1.5 if r0 != 10.0 else 3.5, sphere_r=None,
                             back_opacity=1.0))
        for ph in np.linspace(0, 2 * np.pi, 20, endpoint=False):
            Q = np.stack([rr * math.cos(ph), rr * math.sin(ph), zz], 1)
            surf.add(curve3d(view, Q, color=C.METRIC, stroke_width=1.2, sphere_r=None, back_opacity=1.0))
        vecs = VGroup()
        for i in range(0, len(P) - 1, 30):
            S0, _ = view.project(P[i][None])
            S1, _ = view.project((P[i] + 2.4 * Vs[i])[None])
            vecs.add(Arrow(S0[0], S1[0], buff=0, color=GYRO, stroke_width=4, max_tip_length_to_length_ratio=0.3))
        hdr = label(r"the space part: parallel transport on Flamm's paraboloid (space at one moment)", font_size=26)
        hdr.to_edge(UP, buff=0.3)
        # the tangent cone along the circle, unrolled: a flat sector missing a wedge of 2 pi (1 - sqrt(1 - 2M/r))
        cen = np.array([3.6, -0.55, 0])
        Rsec = 1.95
        gap = flamm10
        sector = AnnularSector(inner_radius=0, outer_radius=Rsec, angle=2 * np.pi - gap, start_angle=np.pi / 2 + gap / 2,
                               color=C.METRIC, fill_opacity=0.15, stroke_width=2, stroke_color=C.METRIC).move_arc_center_to(cen)
        miss = AnnularSector(inner_radius=0, outer_radius=Rsec, angle=gap, start_angle=np.pi / 2 - gap / 2,
                             fill_opacity=0.0, stroke_width=2, stroke_color=GREY_C).move_arc_center_to(cen)
        arc_pts = []
        par = VGroup()
        for t in np.linspace(np.pi / 2 + gap / 2 + 0.05, np.pi / 2 + 2 * np.pi - gap / 2 - 0.05, 9):
            p = cen + 0.75 * Rsec * np.array([math.cos(t), math.sin(t), 0])
            arc_pts.append(p)
            par.add(Arrow(p, p + 0.55 * RIGHT, buff=0, color=GYRO, stroke_width=4, max_tip_length_to_length_ratio=0.3))
        wl = label(rf"missing wedge: ${wedge:.0f}^\circ$", font_size=26, color=GYRO).next_to(miss, UP, buff=0.1)
        txt = VGroup(
            label(r"in the unrolled (flat) cone, transported arrows stay parallel;", font_size=22),
            label(r"glue the edges back, and the last one is turned by the wedge", font_size=22),
        ).arrange(DOWN, buff=0.08).move_to([3.6, -3.25, 0])
        frac = VGroup(
            label(r"at $r = 10M$: \ $38^\circ$ of the $59^\circ$", font_size=26),
            label(r"weak gravity: exactly $\tfrac23$ from curved space,", font_size=26, color=C.METRIC),
            label(r"$\tfrac13$ from warped time", font_size=26, color=C.PROPER_TIME),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([-3.6, -3.05, 0])
        with self.voiceover(
            "Where does that turning come from? Part of it is the curvature of space. <bookmark mark='a'/> Here's "
            "Flamm's paraboloid from part one: the geometry of space around the mass at one moment. Transport a vector "
            "around the circle at r equals ten M, staying on the surface. <bookmark mark='b'/> Near that circle, the "
            "surface is like a cone. Cut the cone open and unroll it, and you get a flat sheet with a wedge missing. On "
            "the flat sheet, parallel transport is trivial: the arrows stay parallel. But when you glue the edges back "
            "together, the last arrow is turned relative to the first, by the angle of the missing wedge, thirty-eight "
            "degrees here. <bookmark mark='c'/> In weak gravity, curved space supplies exactly two thirds of the "
            "geodetic effect, and the warping of time the other third."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hdr), Create(surf, lag_ratio=0.02), run_time=2)
            self.play(LaggedStart(*[GrowArrow(v) for v in vecs], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(sector), Create(miss))
            self.play(LaggedStart(*[GrowArrow(v) for v in par], lag_ratio=0.15), FadeIn(wl), FadeIn(txt), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(frac, lag_ratio=0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def gpb(self):
        c = load("consts")
        geo, fd = float(c["gpb_geo"]), float(c["gpb_fd"])
        assert abs(geo - 6606) < 3 and abs(fd - 39.2) < 0.3
        hdr = VGroup(label(r"Gravity Probe B (launched 20 April 2004)", font_size=36),
                     label(r"four gyroscopes in a 642 km polar orbit, pointed at the star IM Pegasi", font_size=26,
                           color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.35)

        def panel(x, title, pred, meas, err, unit_max, col, lab_pred, lab_meas):
            ax = Axes(x_range=[0, 2, 1], y_range=[0, unit_max, unit_max / 4], x_length=3.0, y_length=3.0, tips=False,
                      axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to([x, -0.55, 0])
            b1 = Rectangle(width=0.7, height=ax.c2p(0, pred)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=col,
                           fill_opacity=0.8)
            b1.move_to(ax.c2p(0.55, 0), aligned_edge=DOWN)
            b2 = Rectangle(width=0.7, height=ax.c2p(0, meas)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=WHITE,
                           fill_opacity=0.75)
            b2.move_to(ax.c2p(1.45, 0), aligned_edge=DOWN)
            eb = VGroup(Line(ax.c2p(1.45, meas - err), ax.c2p(1.45, meas + err), color=WHITE, stroke_width=3),
                        Line(ax.c2p(1.3, meas - err), ax.c2p(1.6, meas - err), color=WHITE, stroke_width=3),
                        Line(ax.c2p(1.3, meas + err), ax.c2p(1.6, meas + err), color=WHITE, stroke_width=3))
            t = label(title, font_size=26, color=col).next_to(ax, UP, buff=0.15)
            l1 = label(lab_pred, font_size=22, color=col).next_to(b1, DOWN, buff=0.12)
            l2 = label(lab_meas, font_size=22).next_to(b2, DOWN, buff=0.12)
            return VGroup(ax, b1, t, l1), VGroup(b2, eb, l2)

        p1, m1 = panel(-3.2, r"geodetic (mas/yr)", 6606.1, 6601.8, 18.3, 7000, GYRO, r"GR: 6606", r"6602 $\pm$ 18")
        p2, m2 = panel(3.2, r"frame dragging (mas/yr)", 39.2, 37.2, 7.2, 50, SPIN, r"GR: 39.2", r"37.2 $\pm$ 7.2")
        hair = note(r"39 milliarcseconds per year: the width of a human hair seen from about half a kilometer").to_edge(DOWN, buff=0.75)
        sat = note(r"laser-ranged satellites (LAGEOS, LARES) see their orbital planes dragged by the predicted amount, within a few percent").to_edge(DOWN, buff=0.35)
        calc = note(rf"our numbers: {geo:.0f} and {fd:.1f} mas/yr, from $\tfrac32 M^{{3/2}}/r^{{5/2}}$ and $J/2r^3$ (toward IM Peg)").next_to(hdr, DOWN, buff=0.15)
        with self.voiceover(
            "Both effects were measured in orbit. <bookmark mark='a'/> Gravity Probe B, launched in 2004, carried four "
            "gyroscopes around the Earth in a polar orbit, pointed at a guide star. <bookmark mark='b'/> General "
            "relativity predicts that their axes should turn by six thousand six hundred milliarcseconds a year from "
            "geodetic precession, <bookmark mark='c'/> and by thirty-nine milliarcseconds a year, sideways, from the "
            "Earth's frame dragging: about the width of a human hair seen from half a kilometer away. "
            "<bookmark mark='d'/> The measurements: six thousand six hundred and two, plus or minus eighteen, and "
            "thirty-seven, plus or minus seven. Laser-tracked satellites see the Earth drag their orbits as well. Space "
            "really is dragged around by rotating mass."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hdr, lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(p1), FadeIn(calc))
            vo.wait_until("c")
            self.play(FadeIn(p2), FadeIn(hair))
            vo.wait_until("d")
            self.play(FadeIn(m1), FadeIn(m2), FadeIn(sat))
        self.clear_scene()
