from __future__ import annotations

import math

import numpy as np
import sympy as sp

from explainer import *  # noqa: F403
from videos.relativity.common import (redraw, Globe, View3D, boxed, curve3d, label, ladder, latitude, load, mtex, note,
                                      sphere_points, stack)
from videos.relativity.geometry import first_order, polar_plane, same, sphere, weak_static


class Geodesics(VoiceoverScene):
    def construct(self):
        self.straightest()
        self.derive()
        self.on_sphere()
        self.not_tensor()
        self.newton()

    # ------------------------------------------------------------------
    def straightest(self):
        d = load("sgeo")
        assert abs(float(d["arc_lat"]) - 0.785) < 1e-3 and abs(float(d["arc_gc"]) - 0.723) < 1e-3
        view = View3D(center=[-3.3, -0.5, 0], scale=2.9, azimuth=-math.pi / 4 - math.pi / 2, elevation=1.15)
        globe = Globe(view, grid_opacity=0.18)
        lat = math.radians(60)
        A = sphere_points(np.pi / 2 - lat, 0.0)
        B = sphere_points(np.pi / 2 - lat, np.pi / 2)
        arc_lat = latitude(np.pi / 2 - lat, ph0=0, ph1=np.pi / 2, n=120)
        om = math.acos(A @ B)
        t = np.linspace(0, 1, 120)[:, None]
        arc_gc = (np.sin((1 - t) * om) * A + np.sin(t * om) * B) / math.sin(om)
        c_lat = redraw(lambda: DashedVMobject(curve3d(view, arc_lat, color=GOLD_A, stroke_width=4)[0], num_dashes=24))
        c_gc = redraw(lambda: curve3d(view, arc_gc, color=WHITE, stroke_width=5))
        dots = redraw(lambda: VGroup(Dot(view.point(A), radius=0.08), Dot(view.point(B), radius=0.08)))
        info = VGroup(
            label(r"two points at $60^\circ$ N, $90^\circ$ apart:", font_size=30),
            mtex(r"\text{along the latitude: }", r"0.785\,R", font_size=34, color=GOLD_A),
            mtex(r"\text{great circle: }", r"0.723\,R", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, 1.2, 0])
        rule = VGroup(label(r"A \emph{geodesic}: a path whose length is stationary.", font_size=30, color=C.METRIC),
                      label(r"(In spacetime: whose proper time is.)", font_size=28, color=C.PROPER_TIME)).arrange(DOWN, buff=0.15)
        rule.next_to(info, DOWN, buff=0.7)
        with self.voiceover(
            "Free particles in flat spacetime move on straight worldlines. In curved spacetime, what's the straightest "
            "possible path? <bookmark mark='p'/> On a sphere, take two cities on the sixtieth parallel, ninety degrees "
            "of longitude apart. <bookmark mark='l'/> Following the parallel takes zero point seven eight five times the "
            "radius. <bookmark mark='g'/> The great circle, which bulges toward the pole, is shorter: zero point seven two "
            "three. It's the shortest path, and it's also the straightest: an ant walking it never turns left or right. "
            "<bookmark mark='r'/> We'll define a geodesic as a path whose length, or in spacetime whose proper time, is "
            "stationary: it doesn't change, to first order, if you wiggle the path a little."
        ) as vo:
            self.play(FadeIn(globe))
            vo.wait_until("p")
            self.add(dots)
            self.play(FadeIn(info[0]))
            vo.wait_until("l")
            self.add(c_lat)
            self.play(FadeIn(info[1]))
            vo.wait_until("g")
            self.add(c_gc)
            self.play(FadeIn(info[2]))
            vo.wait_until("r")
            self.play(FadeIn(rule))
        for m in (c_lat, c_gc, dots, globe.gridlines):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        title = label(r"The geodesic equation", font_size=36).to_corner(UL, buff=0.4)
        rows = [
            mtex(r"S", r"=", r"\int \tfrac12\, g_{\mu\nu}(x)\, \dot x^\mu \dot x^\nu \, d\lambda", font_size=38),
            mtex(r"0", r"=", r"\frac{d}{d\lambda}\frac{\partial L}{\partial \dot x^\sigma} - \frac{\partial L}{\partial x^\sigma}",
                 font_size=38),
            mtex(r"0", r"=", r"\frac{d}{d\lambda}\big(g_{\sigma\nu}\dot x^\nu\big)", r"-",
                 r"\tfrac12\,\partial_\sigma g_{\mu\nu}\,\dot x^\mu \dot x^\nu", font_size=38),
            mtex(r"0", r"=", r"g_{\sigma\nu}\ddot x^\nu", r"+", r"\partial_\mu g_{\sigma\nu}\,\dot x^\mu\dot x^\nu", r"-",
                 r"\tfrac12\,\partial_\sigma g_{\mu\nu}\,\dot x^\mu \dot x^\nu", font_size=38),
            mtex(r"0", r"=", r"g_{\sigma\nu}\ddot x^\nu", r"+",
                 r"\tfrac12\big(\partial_\mu g_{\sigma\nu} + \partial_\nu g_{\sigma\mu} - \partial_\sigma g_{\mu\nu}\big)\dot x^\mu\dot x^\nu",
                 font_size=38),
            mtex(r"0", r"=", r"\ddot x^\lambda", r"+", r"\Gamma^\lambda{}_{\mu\nu}\,\dot x^\mu \dot x^\nu", font_size=46),
        ]
        whys = [
            note(r"the ``energy'' of the path; its stationary paths are geodesics", font_size=22),
            note(r"Euler--Lagrange", font_size=24),
            note(r"$\partial L/\partial \dot x^\sigma = g_{\sigma\nu}\dot x^\nu$", font_size=24),
            note(r"product rule: $g$ changes along the path", font_size=24),
            note(r"split the middle term symmetrically in $\mu\nu$", font_size=24),
            note(r"multiply by $g^{\lambda\sigma}$", font_size=24),
        ]
        rows[5][4].set_color(C.CONNECTION)
        rows[4][4].set_color(C.CONNECTION)
        x0 = -1.2
        for r, w in zip(rows, whys):
            r.shift((x0 - r[1].get_center()[0]) * RIGHT)
            w.next_to(r, DOWN, buff=0.08).align_to(r, RIGHT)
        step = ladder(self, rows, whys, keep=4, top=2.3, x=x0, buff=0.62)
        gam = mtex(r"\Gamma^\lambda{}_{\mu\nu}", r"=", r"\tfrac12\, g^{\lambda\sigma}\big(\partial_\mu g_{\sigma\nu} + "
                   r"\partial_\nu g_{\sigma\mu} - \partial_\sigma g_{\mu\nu}\big)", font_size=40)
        gam[0].set_color(C.CONNECTION)
        gam.to_edge(DOWN, buff=0.5)
        gname = label(r"Christoffel symbols (1869)", font_size=26, color=C.CONNECTION).next_to(gam, UP, buff=0.2)
        with self.voiceover(
            "Let's find the equation a geodesic satisfies. <bookmark mark='a'/> It's easiest to work with this integral: "
            "one half g mu nu times the velocity twice, along a path with parameter lambda. Its stationary paths are the "
            "geodesics, traversed at constant speed. <bookmark mark='b'/> The condition for a stationary path is the "
            "Euler–Lagrange equation, <bookmark mark='c'/> and differentiating the Lagrangian gives g sigma nu x dot nu "
            "for the first part, and half the derivative of the metric for the second."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        with self.voiceover(
            "<bookmark mark='d'/> Now take the derivative along the path. The velocity changes, giving the acceleration "
            "term, and the metric changes too, because we're moving through a region where it varies. "
            "<bookmark mark='e'/> The middle term is summed over mu and nu against a symmetric product, so we can split it "
            "into two equal halves with mu and nu swapped. <bookmark mark='f'/> Finally, multiply by the inverse metric "
            "to free the acceleration."
        ) as vo:
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            vo.wait_until("f")
            step(5)
        with self.voiceover(
            "<bookmark mark='g'/> This is the geodesic equation. The acceleration, in coordinates, equals minus these "
            "coefficients times the velocity squared. The coefficients, built from first derivatives of the metric, are "
            "the Christoffel symbols, gamma. <bookmark mark='h'/> If the metric is constant, they vanish, and geodesics are "
            "straight lines."
        ) as vo:
            vo.wait_until("g")
            self.play(Write(gam), FadeIn(gname))
            self.play(Circumscribe(rows[5], color=C.CONNECTION))
            vo.wait_until("h")
            self.play(Indicate(gam[2], color=C.METRIC))
        self.clear_scene()

    # ------------------------------------------------------------------
    def on_sphere(self):
        S, (th, ph, R) = sphere()
        assert same(S.gamma[0][1][1], -sp.sin(th) * sp.cos(th)) and same(S.gamma[1][0][1], sp.cos(th) / sp.sin(th))
        d = load("sgeo")
        curves = d["curves"]
        start = d["start"]
        view = View3D(center=[-3.4, -0.4, 0], scale=2.7, azimuth=-0.2, elevation=0.4)
        globe = Globe(view, grid_opacity=0.18)
        k = ValueTracker(0.0)

        def fan():
            n = max(2, int(k.get_value() * (curves.shape[1] - 1)) + 1)
            return VGroup(*[curve3d(view, P[:n], color=WHITE, stroke_width=2.8, back_opacity=0.3) for P in curves])

        fan_m = redraw(fan)
        sdot = redraw(lambda: Dot(view.point(start), radius=0.08, color=C.VECTOR))
        gs = VGroup(
            mtex(r"\Gamma^\theta{}_{\phi\phi} = -\sin\theta\cos\theta", font_size=38, color=C.CONNECTION),
            mtex(r"\Gamma^\phi{}_{\theta\phi} = \Gamma^\phi{}_{\phi\theta} = \cot\theta", font_size=38, color=C.CONNECTION),
            note(r"(all others zero; computed from $ds^2 = R^2(d\theta^2 + \sin^2\theta\,d\phi^2)$)", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, 1.9, 0])
        eqs = VGroup(
            mtex(r"\ddot\theta - \sin\theta\cos\theta\,\dot\phi^2 = 0", font_size=38),
            mtex(r"\ddot\phi + 2\cot\theta\,\dot\theta\,\dot\phi = 0", font_size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(gs, DOWN, buff=0.6).align_to(gs, LEFT)
        meet = VGroup(label(r"integrated in 12 directions:", font_size=24, color=GREY_A),
                      label(r"great circles, all meeting at the antipode", font_size=24, color=GREY_A))
        meet.arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(eqs, DOWN, buff=0.45).align_to(gs, LEFT)
        with self.voiceover(
            "Let's try it on the sphere. <bookmark mark='g'/> Plugging its metric into the formula, only two kinds of "
            "Christoffel symbols survive. <bookmark mark='e'/> So geodesics obey these two equations. <bookmark mark='f'/> "
            "Start at one point, pick a direction, and integrate them numerically. Do it in twelve directions, and each "
            "solution is a great circle. <bookmark mark='m'/> And notice: they leave the starting point spreading apart, "
            "but they all meet again on the far side. Straight lines that start out diverging, then converge. Hold on to "
            "that: it's the curvature, showing up in the geodesics."
        ) as vo:
            self.play(FadeIn(globe))
            self.add(sdot)
            vo.wait_until("g")
            self.play(FadeIn(gs, lag_ratio=0.2))
            vo.wait_until("e")
            self.play(Write(eqs))
            vo.wait_until("f")
            self.add(fan_m)
            self.play(k.animate.set_value(0.55), run_time=3, rate_func=linear)
            self.play(FadeIn(meet))
            vo.wait_until("m")
            self.play(k.animate.set_value(1.0), view.az.animate.set_value(0.9), view.el.animate.set_value(-0.1),
                      run_time=4)
        for m in (fan_m, sdot, globe.gridlines):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def not_tensor(self):
        P, (r, ph) = polar_plane()
        assert same(P.gamma[0][1][1], -r) and same(P.gamma[1][0][1], 1 / r) and P.scalar == 0
        flat = VGroup(
            label(r"The flat plane in polar coordinates:", font_size=32),
            mtex(r"\Gamma^r{}_{\phi\phi} = -r, \qquad \Gamma^\phi{}_{r\phi} = \frac1r", font_size=40, color=C.CONNECTION),
            label(r"Not zero, in flat space: $\Gamma$ is not a tensor.", font_size=32),
        ).arrange(DOWN, buff=0.35).move_to(UP * 1.7)
        lif = VGroup(
            label(r"At any point, coordinates can be chosen with", font_size=32),
            mtex(r"g_{\mu\nu} = \eta_{\mu\nu}, \qquad \partial_\lambda g_{\mu\nu} = 0 \quad\Rightarrow\quad "
                 r"\Gamma^\lambda{}_{\mu\nu} = 0", font_size=40),
            label(r"locally inertial coordinates: the equivalence principle, as mathematics", font_size=30,
                  color=C.CURVATURE),
        ).arrange(DOWN, buff=0.3).next_to(flat, DOWN, buff=0.8)
        lif[1][0][:4].set_color(C.METRIC)
        with self.voiceover(
            "One warning about these symbols. <bookmark mark='f'/> In polar coordinates on a flat plane, the Christoffel "
            "symbols aren't zero. Gamma measures how the coordinate grid itself bends and stretches, not whether the space "
            "is curved. Unlike a tensor, it can be nonzero in one coordinate system and zero in another. "
            "<bookmark mark='l'/> In fact, at any single point of any curved space, you can always choose coordinates in "
            "which the metric is the flat one and its first derivatives vanish, so every gamma is zero there. "
            "<bookmark mark='e'/> In spacetime, those are the coordinates of a freely falling observer. This is the "
            "equivalence principle, written as mathematics: at a point, gravity can be transformed away."
        ) as vo:
            vo.wait_until("f")
            self.play(FadeIn(flat, lag_ratio=0.2))
            vo.wait_until("l")
            self.play(FadeIn(lif[:2], lag_ratio=0.2))
            vo.wait_until("e")
            self.play(FadeIn(lif[2]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def newton(self):
        W, (t, x, y, z, eps, Phi) = weak_static()
        assert same(first_order(W.gamma[1][0][0], eps), eps * sp.diff(Phi, x))
        rows = stack(
            mtex(r"\frac{d^2x^i}{d\tau^2}", r"=", r"-\Gamma^i{}_{\mu\nu}\frac{dx^\mu}{d\tau}\frac{dx^\nu}{d\tau}", font_size=40),
            mtex(r"\frac{d^2x^i}{dt^2}", r"\approx", r"-\Gamma^i{}_{00}\,c^2", font_size=40),
            mtex(r"\Gamma^i{}_{00}", r"=", r"-\tfrac12\,\partial_i g_{00}", r"=", r"\frac{\partial_i\Phi}{c^2}", font_size=40),
            mtex(r"\frac{d^2\mathbf x}{dt^2}", r"=", r"-\nabla\Phi", font_size=48),
            buff=0.45,
        )
        rows[0][2].set_color(C.CONNECTION)
        rows[1][2].set_color(C.CONNECTION)
        rows[2][0].set_color(C.CONNECTION)
        rows[2][4].set_color(C.GRAV_POTENTIAL)
        rows[3][2].set_color(C.GRAV_POTENTIAL)
        rows.move_to([-1.2, 0.1, 0])
        whys = VGroup(
            note(r"geodesic equation, space components", font_size=24),
            note(r"slow: $dx^0/d\tau \approx c$ dominates; $d\tau \approx dt$", font_size=24),
            note(r"static, weak: $g_{00} = -(1 + 2\Phi/c^2)$", font_size=24),
            note(r"Newton", font_size=24),
        )
        for w_, r_ in zip(whys, rows):
            w_.next_to(r_, RIGHT, buff=0.4)
        box = SurroundingRectangle(rows[3], color=C.GRAV_POTENTIAL, buff=0.18, corner_radius=0.1)
        with self.voiceover(
            "Now apply the geodesic equation to a slowly moving particle in the weak, static field we found earlier. "
            "<bookmark mark='a'/> Look at the space components of the acceleration. <bookmark mark='b'/> For a slow "
            "particle, the time component of the velocity, about c, is enormous compared with the others, so only the "
            "gamma with two time indices matters. <bookmark mark='c'/> And with g zero zero equal to minus one plus two "
            "phi over c squared, that gamma is just the gradient of phi over c squared. <bookmark mark='d'/> The result: "
            "the acceleration is minus the gradient of phi. Newton's law, from the geodesic equation."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(Write(rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(Write(rows[3]), FadeIn(whys[3]), Create(box))
        concl = label(r"The ``force of gravity'' lives in $\Gamma$: real, but removable by falling. Curvature is what isn't.",
                      font_size=28, color=C.CONNECTION).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "So the Newtonian force of gravity lives in the Christoffel symbols. That explains why it can be transformed "
            "away by falling: gamma isn't a tensor, and in freely falling coordinates it vanishes. <bookmark mark='c'/> "
            "What can't be transformed away is curvature. To detect it, we need to compare directions at different "
            "points, and that requires one more tool."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeIn(concl))
        self.clear_scene()
