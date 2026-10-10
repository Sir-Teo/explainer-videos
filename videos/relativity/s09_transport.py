from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity.common import (redraw, Globe, View3D, arrow3d, boxed, curve3d, label, latitude, load, mtex, note,
                                      stack)
from videos.relativity.geometry import polar_plane, same

O = np.array([-3.6, -0.5, 0.0])  # origin of the polar coordinates on screen
RP = 2.2  # radius of the probe circle


class ParallelTransport(VoiceoverScene):
    def construct(self):
        self.constant_field()
        self.covariant()
        self.compatibility()
        self.transport_rule()
        self.latitudes()
        self.foucault()

    # ------------------------------------------------------------------
    def constant_field(self):
        P, (r, ph) = polar_plane()
        assert same(P.gamma[0][1][1], -r) and same(P.gamma[1][0][1], 1 / r)
        field = VGroup()
        for x in np.arange(-6.6, -0.2, 0.9):
            for y in np.arange(-3.4, 2.8, 0.9):
                p = np.array([x, y, 0])
                field.add(Arrow(p, p + RIGHT * 0.55, buff=0, color=C.VECTOR, stroke_width=3,
                                max_tip_length_to_length_ratio=0.3).set_opacity(0.45))
        rings = VGroup(*[Circle(radius=rr, color=GREY_D, stroke_width=1.5).move_to(O) for rr in (1.0, 2.2, 3.4)])
        spokes = VGroup(*[Line(O, O + 3.6 * np.array([math.cos(a), math.sin(a), 0]), color=GREY_D, stroke_width=1.5)
                          for a in np.linspace(0, 2 * np.pi, 12, endpoint=False)])
        frame = Rectangle(width=6.9, height=6.6).move_to([-3.45, -0.35, 0])
        phi = ValueTracker(0.6)

        def probe():
            a = phi.get_value()
            p = O + RP * np.array([math.cos(a), math.sin(a), 0])
            er = np.array([math.cos(a), math.sin(a), 0])
            ep = np.array([-math.sin(a), math.cos(a), 0])
            g = VGroup(
                Arrow(p, p + 0.9 * er, buff=0, color=GREY_A, stroke_width=5, max_tip_length_to_length_ratio=0.25),
                Arrow(p, p + 0.9 * ep, buff=0, color=GREY_A, stroke_width=5, max_tip_length_to_length_ratio=0.25),
                Arrow(p, p + 1.1 * RIGHT, buff=0, color=C.VECTOR, stroke_width=7, max_tip_length_to_length_ratio=0.25),
                Dot(p, radius=0.07),
            )
            g.add(MathTex(r"\mathbf e_r", font_size=28).move_to(p + 1.2 * er))
            g.add(MathTex(r"\hat{\mathbf e}_\phi", font_size=28).move_to(p + 1.2 * ep))
            return g

        pr = redraw(probe)
        head = label(r"Comparing vectors at different points", font_size=36).to_corner(UR, buff=0.45)
        eq = mtex(r"\mathbf V", r"=", r"V^r\,\mathbf e_r + V^\phi\,\mathbf e_\phi", font_size=40)
        eq[0].set_color(C.VECTOR)
        eq.move_to([3.6, 2.4, 0])
        sol = mtex(r"V^r = \cos\phi, \qquad V^\phi = -\frac{\sin\phi}{r}", font_size=38, color=C.VECTOR)
        sol.next_to(eq, DOWN, buff=0.4)
        heads = VGroup(MathTex(r"V^r =", font_size=36, color=C.VECTOR), MathTex(r"V^\phi =", font_size=36, color=C.VECTOR))
        heads.arrange(DOWN, aligned_edge=RIGHT, buff=0.3).next_to(sol, DOWN, buff=0.5).shift(LEFT * 0.6)
        dv = VGroup(*[DecimalNumber(0, num_decimal_places=2, font_size=36, include_sign=True, color=C.VECTOR) for _ in range(2)])
        for i, m in enumerate(dv):
            def upd(mm, i=i):
                a = phi.get_value()
                mm.set_value(math.cos(a) if i == 0 else -math.sin(a) / RP)
                mm.next_to(heads[i], RIGHT, buff=0.2)
            m.add_updater(upd)
            m.update()
        bad = mtex(r"\partial_\phi V^r = -\sin\phi \neq 0", font_size=38).next_to(heads, DOWN, buff=0.6).set_x(3.6)
        badl = label(r"\ldots for a field that doesn't change at all", font_size=26, color=GREY_A).next_to(bad, DOWN, buff=0.15)
        with self.voiceover(
            "To detect curvature, we need to compare vectors at different points, and that turns out to be surprisingly "
            "subtle. <bookmark mark='f'/> Here's the simplest possible vector field: the same arrow, pointing right, "
            "everywhere on a flat plane. Its rate of change is zero. <bookmark mark='p'/> But describe it in polar "
            "coordinates. At each point, the basis vectors point outward and around, and they rotate as you go around. "
            "<bookmark mark='c'/> So the components of our constant arrow, V r and V phi, keep changing."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("f")
            self.play(LaggedStart(*[GrowArrow(a) for a in field], lag_ratio=0.005), run_time=1.5)
            vo.wait_until("p")
            self.play(Create(rings), Create(spokes))
            self.add(pr)
            self.play(FadeOut(head), Write(eq))
            vo.wait_until("c")
            self.play(FadeIn(sol), FadeIn(heads))
            self.add(dv)
            self.play(phi.animate.set_value(0.6 + 2 * np.pi), run_time=vo.remaining() + 1.5, rate_func=linear)
        with self.voiceover(
            "<bookmark mark='b'/> Take the ordinary partial derivative of a component, and you get something nonzero, "
            "for a field that isn't changing at all. The partial derivative of components mixes up two things: how the "
            "vector changes, and how the basis changes. Only the first is physical."
        ) as vo:
            vo.wait_until("b")
            self.play(Write(bad), FadeIn(badl))
        for m in (pr, *dv):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def covariant(self):
        rows = stack(
            mtex(r"\partial_\mu \mathbf V", r"=", r"\partial_\mu\big(V^\nu\,\mathbf e_\nu\big)", font_size=40),
            mtex(r"\partial_\mu \mathbf V", r"=", r"\big(\partial_\mu V^\nu\big)\,\mathbf e_\nu", r"+",
                 r"V^\nu\,\partial_\mu\mathbf e_\nu", font_size=40),
            mtex(r"\partial_\mu \mathbf V", r"=", r"\big(\partial_\mu V^\lambda\big)\,\mathbf e_\lambda", r"+",
                 r"V^\nu\,\Gamma^\lambda{}_{\mu\nu}\,\mathbf e_\lambda", font_size=40),
            buff=0.45,
        )
        rows.move_to([-0.9, 1.6, 0])
        rows[1][4].set_color(C.CONNECTION)
        rows[2][4].set_color(C.CONNECTION)
        whys = VGroup(
            note(r"vector = components $\times$ basis", font_size=24).next_to(rows[0], RIGHT, buff=0.4),
            note(r"product rule: the basis changes too", font_size=24).next_to(rows[1], RIGHT, buff=0.4),
            note(r"define $\Gamma$: $\ \partial_\mu \mathbf e_\nu = \Gamma^\lambda{}_{\mu\nu}\,\mathbf e_\lambda$", font_size=24).next_to(rows[2], RIGHT, buff=0.4),
        )
        for w in whys:
            if w.get_right()[0] > 7.0:
                w.shift((7.0 - w.get_right()[0]) * RIGHT)
        cov = mtex(r"\nabla_\mu V^\lambda", r"=", r"\partial_\mu V^\lambda", r"+", r"\Gamma^\lambda{}_{\mu\nu}\,V^\nu",
                   font_size=52)
        cov[4].set_color(C.CONNECTION)
        cov[0].set_color(C.VECTOR)
        cb = boxed(cov, color=C.CONNECTION, buff=0.25).next_to(rows, DOWN, buff=0.6).set_x(0)
        name = label(r"the covariant derivative", font_size=28, color=C.CONNECTION).next_to(cb, DOWN, buff=0.15)
        check = mtex(r"\nabla_\phi V^r", r"=", r"\partial_\phi\cos\phi", r"+", r"\Gamma^r{}_{\phi\phi}\,V^\phi", r"=",
                     r"-\sin\phi", r"+", r"(-r)\Big(-\frac{\sin\phi}{r}\Big)", r"=", r"0", font_size=34)
        check[4].set_color(C.CONNECTION)
        check[8].set_color(C.CONNECTION)
        check[10].set_color(C.VECTOR)
        check.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "So let's separate them. <bookmark mark='a'/> Write the vector as components times basis vectors. "
            "<bookmark mark='b'/> Its derivative has two parts, by the product rule: the change in the components, and "
            "the change in the basis vectors. <bookmark mark='c'/> The change of a basis vector is itself a vector, so it's "
            "some combination of the basis vectors, and the coefficients are exactly the Christoffel symbols. That's "
            "what gamma really is: how the basis turns and stretches from point to point."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
        with self.voiceover(
            "<bookmark mark='d'/> Collect the components, and you get the covariant derivative: the partial derivative, "
            "plus a gamma term that corrects for the turning basis. Unlike the partial derivative, it's a tensor. "
            "<bookmark mark='e'/> Check it on our constant field: the derivative of V r around the circle was minus sine "
            "phi, and the gamma term is plus sine phi. They cancel. The covariant derivative of a constant field is zero, "
            "as it should be."
        ) as vo:
            vo.wait_until("d")
            self.play(Write(cov), Create(cb[0]), FadeIn(name))
            vo.wait_until("e")
            self.play(Write(check), run_time=2.5)
            self.play(Indicate(check[10], color=C.VECTOR))
        self.clear_scene()

    # ------------------------------------------------------------------
    def compatibility(self):
        a = mtex(r"\nabla_\mu\,\omega_\nu = \partial_\mu\omega_\nu - \Gamma^\lambda{}_{\mu\nu}\,\omega_\lambda", font_size=40)
        a.move_to(UP * 2.4)
        al = note(r"one $+\Gamma$ per upper index, one $-\Gamma$ per lower index", font_size=24).next_to(a, DOWN, buff=0.15)
        b = mtex(r"\nabla_\rho\, g_{\mu\nu}", r"=", r"0", font_size=46)
        b[0].set_color(C.METRIC)
        bl = label(r"lengths and angles are preserved when vectors are carried along", font_size=28, color=GREY_A)
        c = mtex(r"\Gamma^\lambda{}_{\mu\nu}", r"=", r"\Gamma^\lambda{}_{\nu\mu}", font_size=40)
        cl = label(r"no twisting (torsion-free)", font_size=28, color=GREY_A)
        g1 = VGroup(b, bl).arrange(RIGHT, buff=0.5)
        g2 = VGroup(c, cl).arrange(RIGHT, buff=0.5)
        VGroup(g1, g2).arrange(DOWN, buff=0.45, aligned_edge=LEFT).next_to(al, DOWN, buff=0.7)
        arrow = MathTex(r"\Downarrow", font_size=48).next_to(VGroup(g1, g2), DOWN, buff=0.3)
        res = mtex(r"\Gamma^\lambda{}_{\mu\nu}", r"=", r"\tfrac12\,g^{\lambda\sigma}\big(\partial_\mu g_{\sigma\nu} + "
                   r"\partial_\nu g_{\sigma\mu} - \partial_\sigma g_{\mu\nu}\big)", font_size=42)
        res[0].set_color(C.CONNECTION)
        res.next_to(arrow, DOWN, buff=0.3)
        resl = label(r"the same $\Gamma$ as in the geodesic equation (Levi-Civita)", font_size=26,
                     color=C.CONNECTION).next_to(res, DOWN, buff=0.2)
        with self.voiceover(
            "<bookmark mark='a'/> Covectors get a minus gamma term instead, and a general tensor gets one correction per "
            "index. <bookmark mark='b'/> Now, which gamma is the right one on a curved space? We ask for two natural "
            "things. First, carrying vectors around shouldn't change their lengths or the angles between them: the "
            "covariant derivative of the metric is zero. <bookmark mark='c'/> Second, no twisting: gamma is symmetric in "
            "its lower indices. <bookmark mark='d'/> Write out the first condition three times with the indices "
            "permuted, add two and subtract the third, and gamma is forced to be exactly the Christoffel formula we found "
            "from geodesics. Straightness and parallelism come from the same object, built from the metric."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(a), FadeIn(al))
            vo.wait_until("b")
            self.play(FadeIn(g1, shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(g2, shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(arrow), Write(res))
            self.play(FadeIn(resl))
        self.clear_scene()

    # ------------------------------------------------------------------
    def transport_rule(self):
        pt = mtex(r"\frac{dV^\mu}{d\lambda}", r"+", r"\Gamma^\mu{}_{\nu\rho}\,\frac{dx^\nu}{d\lambda}\,V^\rho", r"=", r"0",
                  font_size=48)
        pt[0].set_color(C.VECTOR)
        pt[2].set_color(C.CONNECTION)
        pt.move_to(UP * 1.4)
        ptl = label(r"\emph{parallel transport} along a curve $x^\mu(\lambda)$: no covariant change", font_size=30,
                    color=GREY_A).next_to(pt, DOWN, buff=0.3)
        geo = mtex(r"V^\mu = \frac{dx^\mu}{d\lambda}", r"\quad\Longrightarrow\quad", r"\ddot x^\mu + "
                   r"\Gamma^\mu{}_{\nu\rho}\,\dot x^\nu\dot x^\rho = 0", font_size=40)
        geo.next_to(ptl, DOWN, buff=0.8)
        geol = label(r"a geodesic carries its own direction along: it never turns", font_size=30,
                     color=C.METRIC).next_to(geo, DOWN, buff=0.3)
        with self.voiceover(
            "With the covariant derivative we can finally say what it means to carry a vector along a path without "
            "turning it. <bookmark mark='p'/> Along a curve, the vector's covariant rate of change is zero: its components "
            "change only as much as needed to keep up with the turning basis. This is parallel transport, the ant's rule "
            "from the triangle, as an equation. <bookmark mark='g'/> And if the vector you carry is the curve's own "
            "velocity, you get back the geodesic equation. A geodesic is a curve that parallel transports its own "
            "direction: it never turns."
        ) as vo:
            vo.wait_until("p")
            self.play(Write(pt), FadeIn(ptl))
            vo.wait_until("g")
            self.play(Write(geo), FadeIn(geol))
        self.clear_scene()

    # ------------------------------------------------------------------
    def latitudes(self):
        d = load("transport")
        th0s = np.degrees(d["lat_th0"])
        hol = np.degrees(d["lat_holonomy"])
        assert np.allclose(th0s, [30, 60, 90, 120]) and abs(hol[1] - 180) < 1e-6 and abs(hol[0] - 48.2) < 0.05
        view = View3D(center=[-3.2, -0.6, 0], scale=2.9, azimuth=-0.3, elevation=1.05)
        globe = Globe(view, grid_opacity=0.15)
        k = ValueTracker(0.0)
        which = {"i": 1}

        def arrow():
            i = which["i"]
            P, Vv = d["lat_paths"][i], d["lat_vecs"][i]
            j = int(round(k.get_value() * (len(P) - 1)))
            return arrow3d(view, P[j], 0.38 * Vv[j], color=C.VECTOR, stroke_width=6)

        arr = redraw(arrow)
        paths = [redraw(lambda i=i: curve3d(view, d["lat_paths"][i], color=WHITE, stroke_width=3.5))
                 for i in range(2)]
        ghosts = [arrow3d(view, d["lat_paths"][i][0], 0.38 * d["lat_vecs"][i][0], color=C.VECTOR, stroke_width=4)
                  .set_opacity(0.35) for i in range(2)]
        info = VGroup(
            mtex(r"\text{rotation after one loop}", r"=", r"2\pi\,(1 - \cos\theta_0)", r"=", r"\frac{\text{cap area}}{R^2}",
                 font_size=34),
        ).to_corner(UR, buff=0.45)
        info[0][2].set_color(C.VECTOR)
        info[0][4].set_color(C.CURVATURE)
        rows = VGroup(
            mtex(r"\theta_0 = 60^\circ:", r"\ \ 180^\circ", font_size=36),
            mtex(r"\theta_0 = 30^\circ:", r"\ \ 48^\circ", font_size=36),
            mtex(r"\theta_0 = 90^\circ\ (\text{equator}):", r"\ \ 0^\circ", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(info, DOWN, buff=0.6).align_to(info, LEFT).shift(RIGHT * 1.2)
        for r in rows:
            r[1].set_color(C.VECTOR)
        eqn = label(r"(the equator is a geodesic: nothing turns)", font_size=24, color=GREY_A).next_to(rows, DOWN, buff=0.2).align_to(rows, LEFT)
        with self.voiceover(
            "Let's watch parallel transport on the sphere. <bookmark mark='a'/> Carry an arrow once around the circle sixty "
            "degrees down from the north pole, following the rule exactly: here, the transport equation is integrated "
            "numerically. <bookmark mark='m'/> Halfway around, the arrow has already swung far from where it started, "
            "relative to the directions north and east. <bookmark mark='e'/> And when it gets back, it's pointing the "
            "opposite way: rotated by a hundred and eighty degrees."
        ) as vo:
            self.play(FadeIn(globe))
            self.add(paths[1])
            vo.wait_until("a")
            self.add(ghosts[1], arr)
            self.play(k.animate.set_value(0.5), run_time=vo.until("e") - 0.2, rate_func=linear)
            self.play(k.animate.set_value(1.0), run_time=vo.remaining() + 1.0, rate_func=linear)
        with self.voiceover(
            "<bookmark mark='f'/> In general, around the circle at angle theta zero from the pole, the arrow turns by "
            "two pi times one minus cosine theta zero, which is the area of the polar cap inside the loop, divided by R "
            "squared. <bookmark mark='r'/> Sixty degrees: a half turn. <bookmark mark='s'/> Thirty degrees: forty-eight "
            "degrees. <bookmark mark='t'/> And around the equator, which is itself a geodesic, no rotation at all."
        ) as vo:
            vo.wait_until("f")
            self.play(Write(info))
            vo.wait_until("r")
            self.play(FadeIn(rows[0]))
            vo.wait_until("s")
            which["i"] = 0
            self.remove(ghosts[1])
            self.add(paths[0], ghosts[0])
            k.set_value(0.0)
            self.play(FadeIn(rows[1]), k.animate.set_value(1.0), run_time=3, rate_func=linear)
            vo.wait_until("t")
            self.play(FadeIn(rows[2]), FadeIn(eqn))
        for m in (arr, *paths, globe.gridlines):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def foucault(self):
        d = load("transport")
        deg, hours = float(d["foucault_deg"]), float(d["foucault_hours"])
        assert round(deg) == 271 and round(hours) == 32
        disk = Circle(radius=2.2, color=GREY_B, stroke_width=2, fill_color="#16202B", fill_opacity=1).move_to([-3.3, -0.3, 0])
        marks = VGroup(*[Line(disk.get_center() + 2.0 * np.array([math.cos(a), math.sin(a), 0]),
                              disk.get_center() + 2.2 * np.array([math.cos(a), math.sin(a), 0]), color=GREY_B)
                         for a in np.linspace(0, 2 * np.pi, 24, endpoint=False)])
        ang = ValueTracker(0.0)
        swing = redraw(lambda: Line(disk.get_center() + 1.9 * np.array([math.cos(PI / 2 - ang.get_value()), math.sin(PI / 2 - ang.get_value()), 0]),
                                           disk.get_center() - 1.9 * np.array([math.cos(PI / 2 - ang.get_value()), math.sin(PI / 2 - ang.get_value()), 0]),
                                           color=C.VECTOR, stroke_width=6))
        bob = Dot(disk.get_center(), radius=0.12, color=WHITE)
        tl = label(r"Foucault's pendulum, Paris (1851)", font_size=34).move_to([0.4, 2.9, 0], aligned_edge=LEFT)
        rows = VGroup(
            label(r"The Earth carries it around its latitude circle once a day;", font_size=28),
            label(r"its swing plane is parallel transported.", font_size=28),
            mtex(r"360^\circ \times \sin(48.85^\circ)", r"\approx", r"271^\circ \text{ per day}", font_size=36),
            label(r"a full turn every 32 hours", font_size=28, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tl, DOWN, buff=0.6).align_to(tl, LEFT)
        rows[2][2].set_color(C.VECTOR)
        with self.voiceover(
            "You can see this experiment in a museum. <bookmark mark='p'/> A Foucault pendulum, first hung in Paris in "
            "1851, swings back and forth in a plane that the pendulum keeps as parallel as it can. "
            "<bookmark mark='e'/> The Earth's rotation carries it around its circle of latitude once a day, so the swing "
            "plane is parallel transported around that circle, <bookmark mark='r'/> and relative to the floor it turns "
            "by three hundred and sixty degrees times the sine of the latitude: about two hundred and seventy degrees a "
            "day in Paris."
        ) as vo:
            vo.wait_until("p")
            self.play(FadeIn(disk), FadeIn(marks), FadeIn(tl), FadeIn(bob))
            self.add(swing)
            vo.wait_until("e")
            self.play(FadeIn(rows[:2]))
            vo.wait_until("r")
            self.play(FadeIn(rows[2:]), ang.animate.set_value(math.radians(deg)), run_time=4)
        swing.clear_updaters()
        self.clear_scene()
