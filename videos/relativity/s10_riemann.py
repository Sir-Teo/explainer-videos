from __future__ import annotations

import math

import numpy as np
import sympy as sp

from explainer import *  # noqa: F403
from videos.relativity.common import (redraw, Globe, View3D, boxed, curve3d, label, load, meridian, mtex, note, polyline,
                                      sphere_points, stack)
from videos.relativity.geometry import first_order, polar_plane, same, sphere, weak_static


def strike(m, color=RED_B):
    return Line(m.get_corner(DL) + LEFT * 0.03, m.get_corner(UR) + RIGHT * 0.03, color=color, stroke_width=3)


class Riemann(VoiceoverScene):
    def construct(self):
        self.per_area()
        self.commutator()
        self.properties()
        self.deviation()
        self.tides()

    # ------------------------------------------------------------------
    def per_area(self):
        d = load("transport")
        A, ang = d["cap_areas"], d["cap_angles"]
        assert np.allclose(A, ang, rtol=1e-6)
        ax = Axes(x_range=[0, 3.2, 1], y_range=[0, 3.2, 1], x_length=4.6, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": True, "font_size": 22,
                               "numbers_to_include": [1, 2, 3]})
        ax.to_edge(LEFT, buff=1.1).shift(DOWN * 0.3)
        xl = label(r"area enclosed $/R^2$", font_size=24).next_to(ax.x_axis, DOWN, buff=0.45)
        yl = label(r"rotation (radians)", font_size=24).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.45)
        line = DashedLine(ax.c2p(0, 0), ax.c2p(3.2, 3.2), color=C.CURVATURE, stroke_width=2.5)
        dots = VGroup(*[Dot(ax.c2p(a, g), radius=0.07, color=C.VECTOR) for a, g in zip(A, ang)])
        sim = note(r"12 loops around polar caps, transport integrated numerically").next_to(ax, UP, buff=0.3)
        right = VGroup(
            label(r"Curvature is rotation per unit area.", font_size=32, color=C.CURVATURE),
            label(r"For a tiny loop spanned by $\delta a^\mu$, then $\delta b^\nu$:", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.3, 1.6, 0])
        eq = mtex(r"\delta V^\rho", r"=", r"-R^\rho{}_{\sigma\mu\nu}", r"\,V^\sigma\,\delta a^\mu\,\delta b^\nu", font_size=44)
        eq[0].set_color(C.VECTOR)
        eq[2].set_color(C.CURVATURE)
        eq.next_to(right, DOWN, buff=0.45).align_to(right, LEFT)
        eql = VGroup(label(r"4 indices: which component changes ($\rho$),", font_size=24, color=GREY_A),
                     label(r"of which component ($\sigma$), around which plane ($\mu\nu$)", font_size=24, color=GREY_A))
        eql.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(eq, DOWN, buff=0.3).align_to(right, LEFT)
        with self.voiceover(
            "Back to curvature. We saw that an arrow carried around a loop comes back rotated. <bookmark mark='p'/> Here's "
            "the rotation for twelve loops of different sizes on a unit sphere, plotted against the area they enclose. "
            "<bookmark mark='l'/> A perfect straight line of slope one: the rotation is proportional to the area, and the "
            "constant of proportionality is the curvature, one over R squared. Curvature is rotation per unit area."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("p")
            self.play(FadeIn(sim), LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.1), run_time=2)
            vo.wait_until("l")
            self.play(Create(line))
            self.play(FadeIn(right[0]))
        with self.voiceover(
            "<bookmark mark='m'/> In more dimensions, a loop can lie in many different planes, and the arrow can be "
            "rotated in many different ways. <bookmark mark='e'/> So for a tiny loop, built by going along delta a and "
            "then delta b, the change in the vector is a linear function of the vector and of both sides of the loop: "
            "<bookmark mark='i'/> a tensor with four indices. One says which component of the change we're looking at, "
            "one which component of the vector caused it, and two describe the plane of the loop. This is the Riemann "
            "curvature tensor."
        ) as vo:
            vo.wait_until("m")
            self.play(FadeIn(right[1]))
            vo.wait_until("e")
            self.play(Write(eq))
            vo.wait_until("i")
            self.play(FadeIn(eql))
        self.clear_scene()

    # ------------------------------------------------------------------
    def commutator(self):
        top = mtex(r"[\nabla_\mu, \nabla_\nu]\,V^\rho", r"=", r"\nabla_\mu\nabla_\nu V^\rho - \nabla_\nu\nabla_\mu V^\rho",
                   font_size=40).to_edge(UP, buff=0.4)
        topl = label(r"going around the loop = doing the two derivatives in both orders", font_size=26,
                     color=GREY_A).next_to(top, DOWN, buff=0.15)
        r1 = MathTex(r"=", r"\partial_\mu\partial_\nu V^\rho", r"-\partial_\nu\partial_\mu V^\rho",
                     r"+\big(\partial_\mu\Gamma^\rho{}_{\nu\sigma}\big)V^\sigma", r"-\big(\partial_\nu\Gamma^\rho{}_{\mu\sigma}\big)V^\sigma",
                     font_size=38)
        r2 = MathTex(r"\phantom{=}", r"+\Gamma^\rho{}_{\nu\sigma}\,\partial_\mu V^\sigma", r"-\Gamma^\rho{}_{\nu\sigma}\,\partial_\mu V^\sigma",
                     r"+\Gamma^\rho{}_{\mu\sigma}\,\partial_\nu V^\sigma", r"-\Gamma^\rho{}_{\mu\sigma}\,\partial_\nu V^\sigma",
                     font_size=38)
        r3 = MathTex(r"\phantom{=}", r"+\Gamma^\rho{}_{\mu\lambda}\Gamma^\lambda{}_{\nu\sigma}V^\sigma",
                     r"-\Gamma^\rho{}_{\nu\lambda}\Gamma^\lambda{}_{\mu\sigma}V^\sigma", font_size=38)
        body = VGroup(r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(topl, DOWN, buff=0.5)
        body.set_x(0)
        for r in (r1, r2, r3):
            for part in r[1:]:
                part.set_color(C.CONNECTION if r'\Gamma' in part.tex_string else WHITE)
        r1[1:3].set_color(WHITE)
        whyx = note(r"(the $-\Gamma^\lambda{}_{\mu\nu}\nabla_\lambda V^\rho$ terms cancel: $\Gamma$ is symmetric)",
                    font_size=22).next_to(body, DOWN, buff=0.3)
        s12 = VGroup(strike(r1[1]), strike(r1[2]))
        s2 = VGroup(*[strike(r2[i]) for i in range(1, 5)])
        why12 = note(r"partial derivatives commute", font_size=22, color=RED_B).next_to(r1[1:3], UP, buff=0.12)
        why2 = note(r"these cancel in pairs", font_size=22, color=RED_B).next_to(r2, RIGHT, buff=0.2)
        if why2.get_right()[0] > 7.0:
            why2.next_to(r2, DOWN, buff=0.05).align_to(r2, RIGHT)
        R = mtex(r"R^\rho{}_{\sigma\mu\nu}", r"=", r"\partial_\mu\Gamma^\rho{}_{\nu\sigma} - \partial_\nu\Gamma^\rho{}_{\mu\sigma}",
                 r"+", r"\Gamma^\rho{}_{\mu\lambda}\Gamma^\lambda{}_{\nu\sigma} - \Gamma^\rho{}_{\nu\lambda}\Gamma^\lambda{}_{\mu\sigma}",
                 font_size=44)
        R[0].set_color(C.CURVATURE)
        R[2].set_color(C.CONNECTION)
        R[4].set_color(C.CONNECTION)
        res = mtex(r"[\nabla_\mu, \nabla_\nu]\,V^\rho", r"=", r"R^\rho{}_{\sigma\mu\nu}", r"\,V^\sigma", font_size=44)
        res[2].set_color(C.CURVATURE)
        with self.voiceover(
            "Let's compute it. Going around a tiny loop, first one way and then the other, amounts to taking covariant "
            "derivatives in two different orders. <bookmark mark='c'/> So the curvature is the commutator of covariant "
            "derivatives: how much the answer depends on the order. <bookmark mark='e'/> Expand both covariant "
            "derivatives using their definition. It's a page of terms, but it collapses beautifully."
        ) as vo:
            vo.wait_until("c")
            self.play(Write(top), FadeIn(topl))
            vo.wait_until("e")
            self.play(FadeIn(r1), FadeIn(r2), FadeIn(r3), FadeIn(whyx), run_time=2)
        with self.voiceover(
            "<bookmark mark='a'/> The second derivatives of V cancel, because partial derivatives commute. "
            "<bookmark mark='b'/> The terms with one derivative of V cancel in pairs. <bookmark mark='c'/> What's left "
            "has no derivatives of V at all: just V, multiplied by a combination of the Christoffel symbols and their "
            "derivatives."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(s12), FadeIn(why12))
            self.play(r1[1:3].animate.set_opacity(0.3))
            vo.wait_until("b")
            self.play(Create(s2), FadeIn(why2))
            self.play(r2[1:].animate.set_opacity(0.3))
            vo.wait_until("c")
            self.play(Indicate(r1[3:], color=C.CURVATURE), Indicate(r3[1:], color=C.CURVATURE))
        R.move_to(DOWN * 0.3)
        res.next_to(R, DOWN, buff=0.6)
        rb = SurroundingRectangle(R, color=C.CURVATURE, buff=0.22, corner_radius=0.1)
        with self.voiceover(
            "<bookmark mark='r'/> That combination is the Riemann tensor: two derivatives of the Christoffel symbols, plus "
            "two products of them. <bookmark mark='s'/> And because the derivatives of V dropped out, the commutator is "
            "just R times V, at a single point. That's why R is a genuine tensor, even though gamma isn't."
        ) as vo:
            vo.wait_until("r")
            self.play(FadeOut(VGroup(r1, r2, r3, s12, s2, why12, why2, whyx)), Write(R), Create(rb))
            vo.wait_until("s")
            self.play(Write(res))
        self.clear_scene()

    # ------------------------------------------------------------------
    def properties(self):
        P, (r, ph) = polar_plane()
        S, (th, ph2, Rr) = sphere()
        assert P.riemann(0, 1, 0, 1) == 0 and same(S.riemann(0, 1, 0, 1), sp.sin(th) ** 2) and same(S.scalar, 2 / Rr**2)
        left = VGroup(
            label(r"Flat $\iff R^\rho{}_{\sigma\mu\nu} = 0$ everywhere", font_size=32, color=C.CURVATURE),
            mtex(r"\text{plane, polar: } \Gamma \neq 0, \ \ R = 0", font_size=34),
            mtex(r"\text{sphere: } R^\theta{}_{\phi\theta\phi} = \sin^2\theta", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        sym = VGroup(
            label(r"Symmetries:", font_size=30),
            mtex(r"R_{\rho\sigma\mu\nu} = -R_{\sigma\rho\mu\nu} = -R_{\rho\sigma\nu\mu} = R_{\mu\nu\rho\sigma}", font_size=34),
            mtex(r"R_{\rho\sigma\mu\nu} + R_{\rho\mu\nu\sigma} + R_{\rho\nu\sigma\mu} = 0", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        count = VGroup(
            mtex(r"\text{independent components: } \frac{n^2(n^2-1)}{12}", font_size=34),
            mtex(r"n = 2:\ 1 \qquad n = 3:\ 6 \qquad n = 4:\ 20", font_size=34, color=C.CURVATURE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        assert [n * n * (n * n - 1) // 12 for n in (2, 3, 4)] == [1, 6, 20]
        col = VGroup(left, sym, count).arrange(DOWN, aligned_edge=LEFT, buff=0.55).to_edge(LEFT, buff=0.7)
        contr = VGroup(
            label(r"Contractions:", font_size=30),
            mtex(r"R_{\mu\nu}", r"=", r"R^\lambda{}_{\mu\lambda\nu}", font_size=40),
            label(r"Ricci tensor (10 components)", font_size=24, color=GREY_A),
            mtex(r"R", r"=", r"g^{\mu\nu}R_{\mu\nu}", font_size=40),
            label(r"Ricci scalar; sphere: $R = 2/R^2$", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.8).shift(UP * 0.3)
        contr[1][0].set_color(C.CURVATURE)
        contr[3][0].set_color(C.CURVATURE)
        with self.voiceover(
            "Riemann is the coordinate-independent test we were looking for. <bookmark mark='f'/> A space is flat exactly "
            "when it vanishes everywhere. The polar plane has nonzero gammas but zero Riemann tensor. The sphere doesn't: "
            "computing from its metric gives R theta phi theta phi equal to sine squared theta. <bookmark mark='s'/> It "
            "has symmetries: antisymmetric in each pair of indices, symmetric under swapping the pairs, and a cyclic "
            "identity. <bookmark mark='n'/> So in n dimensions it has n squared times n squared minus one over twelve "
            "independent components: one for a surface, which is Gauss's curvature, six in three dimensions, and twenty "
            "in four-dimensional spacetime."
        ) as vo:
            vo.wait_until("f")
            self.play(FadeIn(left, lag_ratio=0.3), run_time=2)
            vo.wait_until("s")
            self.play(FadeIn(sym, lag_ratio=0.3))
            vo.wait_until("n")
            self.play(FadeIn(count, lag_ratio=0.3))
        with self.voiceover(
            "<bookmark mark='c'/> Two averages of it will matter most. Contract the first and third indices, and you get "
            "the Ricci tensor, R mu nu, with ten components. <bookmark mark='r'/> Contract again with the inverse metric, "
            "and you get a single number at each point, the Ricci scalar. For a sphere it's two over R squared."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeIn(contr[:3]))
            vo.wait_until("r")
            self.play(FadeIn(contr[3:]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def deviation(self):
        view = View3D(center=[-3.4, -0.5, 0], scale=2.8, azimuth=-math.pi / 2 - 0.25, elevation=0.3)
        globe = Globe(view, grid_opacity=0.15)
        m1, m2 = meridian(-0.16, th0=0.02, th1=np.pi / 2), meridian(0.16, th0=0.02, th1=np.pi / 2)
        k = ValueTracker(0.0)

        def pair():
            n = max(2, int(k.get_value() * 119) + 1)
            a, b = m1[::-1][:n], m2[::-1][:n]
            g = VGroup(curve3d(view, a, color=WHITE, stroke_width=3.5), curve3d(view, b, color=WHITE, stroke_width=3.5))
            g.add(Line(view.point(a[-1]), view.point(b[-1]), color=C.CURVATURE, stroke_width=4))
            return g

        pr = redraw(pair)
        eqs = VGroup(
            label(r"Two geodesics, parallel at the equator:", font_size=28),
            mtex(r"\frac{d^2\xi}{ds^2}", r"=", r"-K\,\xi", font_size=40),
            label(r"they converge: $\xi = \xi_0\cos(s/R)$", font_size=26, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.3, 2.0, 0])
        eqs[1][2].set_color(C.CURVATURE)
        gd = mtex(r"\frac{D^2\xi^\mu}{d\tau^2}", r"=", r"R^\mu{}_{\nu\rho\sigma}", r"\,u^\nu u^\rho\,\xi^\sigma", font_size=42)
        gd[2].set_color(C.CURVATURE)
        gdl = label(r"geodesic deviation: curvature makes free paths converge or diverge", font_size=24,
                    color=GREY_A)
        VGroup(gd, gdl).arrange(DOWN, buff=0.2).next_to(eqs, DOWN, buff=0.7).set_x(3.3)
        with self.voiceover(
            "And now the payoff for physics. <bookmark mark='g'/> Start two geodesics on the equator, both heading north, "
            "parallel. <bookmark mark='c'/> On a sphere they don't stay parallel: their separation shrinks, and they meet "
            "at the pole. <bookmark mark='e'/> The separation, xi, accelerates toward zero at a rate set by the "
            "curvature. <bookmark mark='g2'/> In general, the relative acceleration of two neighboring geodesics is the "
            "Riemann tensor, contracted twice with the velocity, and once with their separation. This is the geodesic "
            "deviation equation."
        ) as vo:
            self.play(FadeIn(globe))
            vo.wait_until("g")
            self.add(pr)
            self.play(FadeIn(eqs[0]))
            vo.wait_until("c")
            self.play(k.animate.set_value(1.0), run_time=3.5)
            vo.wait_until("e")
            self.play(Write(eqs[1]), FadeIn(eqs[2]))
            vo.wait_until("g2")
            self.play(Write(gd), FadeIn(gdl))
        pr.clear_updaters()
        globe.gridlines.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def tides(self):
        W, (t, x, y, z, eps, Phi) = weak_static()
        assert same(first_order(W.riemann(1, 0, 2, 0), eps), eps * sp.diff(Phi, x, y))
        assert same(first_order(W.ricci[0, 0], eps), eps * (sp.diff(Phi, x, 2) + sp.diff(Phi, y, 2) + sp.diff(Phi, z, 2)))
        rows = stack(
            mtex(r"\text{GR, slow particles:}\quad", r"\frac{d^2\xi^i}{dt^2}", r"=", r"-c^2 R^i{}_{0j0}\;\xi^j", font_size=38),
            mtex(r"\text{Newton:}\quad", r"\frac{d^2\xi^i}{dt^2}", r"=", r"-\partial_i\partial_j\Phi\;\xi^j", font_size=38),
            align_index=2, buff=0.45,
        )
        rows[0][3].set_color(C.CURVATURE)
        rows[1][3].set_color(C.GRAV_POTENTIAL)
        rows[0][0].set_color(GREY_A)
        rows[1][0].set_color(GREY_A)
        rows.to_edge(UP, buff=0.5)
        same_ = mtex(r"c^2 R^i{}_{0j0}", r"=", r"\partial_i\partial_j\Phi", font_size=48)
        same_[0].set_color(C.CURVATURE)
        same_[2].set_color(C.GRAV_POTENTIAL)
        sb = boxed(same_, color=C.CURVATURE, buff=0.22).next_to(rows, DOWN, buff=0.5)
        tl = label(r"Tides \emph{are} curvature.", font_size=34, color=C.CURVATURE).next_to(sb, DOWN, buff=0.3)
        d = load("tidal")
        rel, area = d["rel"], d["area"]
        # (a flat ring is a slice: in its plane the tidal terms are (+2, -1) GM/r^3, so its area grows; the third
        # direction's -1 makes the trace vanish, so a 3D ball keeps its volume -- checked on the ball item)
        bv = load("ball")["v_vac"]
        assert abs(bv[len(bv) // 10] - 1) < 1e-3 and area[len(area) // 3] > 1
        zc = np.array([-4.6, -1.55, 0])
        m = 0.88 / float(d["ring"])
        kk = ValueTracker(0.0)
        n = int(np.searchsorted(d["stretch"], 1.6)) + 1  # stop at 1.6x stretch

        def ring():
            i = int(round(kk.get_value() * (n - 1)))
            P = rel[i] * m
            pts = np.concatenate([P, np.zeros((len(P), 1))], 1) + zc
            return VGroup(VMobject(stroke_color=C.CURVATURE, stroke_width=2.5, fill_color=C.CURVATURE, fill_opacity=0.15)
                          .set_points_as_corners([*pts, pts[0]]), *[Dot(p, radius=0.05, color=C.CURVATURE) for p in pts])

        rg = redraw(ring)
        trace = VGroup(
            mtex(r"\text{trace: }\ c^2 R_{00}", r"=", r"\nabla^2\Phi", font_size=36),
            mtex(r"\text{vacuum: } \nabla^2\Phi = 0", r"\ \Rightarrow\ ", r"\text{a ball keeps its volume}", font_size=32),
            mtex(r"\text{in matter: } \nabla^2\Phi = 4\pi G\rho", r"\ \Rightarrow\ ", r"\text{it shrinks}", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.6, -2.3, 0])
        trace[0][0].set_color(C.CURVATURE)
        trace[2][0].set_color(C.MATTER)
        with self.voiceover(
            "Now apply it to slowly moving particles in a weak gravitational field. <bookmark mark='a'/> Their separation "
            "accelerates according to minus c squared times the components of Riemann with two time indices. "
            "<bookmark mark='b'/> Newton's theory has its own version, the tidal acceleration: minus the second "
            "derivatives of the potential times the separation. <bookmark mark='c'/> These must agree, and they do: for "
            "the weak-field metric, R i zero j zero is exactly the second derivative of phi over c squared. The tidal "
            "tensor of Newton is the curvature of spacetime."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]))
            vo.wait_until("c")
            self.play(Write(same_), Create(sb[0]))
            self.play(FadeIn(tl))
        with self.voiceover(
            "<bookmark mark='r'/> Our falling ring is a curvature detector. <bookmark mark='t'/> And its most important "
            "reading is the trace, the sum of the diagonal tidal terms, which is the Ricci component R zero zero: the "
            "Laplacian of phi. <bookmark mark='v'/> In empty space around the Earth, the Laplacian is zero: the stretching "
            "along the fall exactly balances the squeezing in the two sideways directions, so a ball of particles keeps "
            "its volume at first. <bookmark mark='m'/> Inside "
            "matter, it's four pi G rho, and the ring shrinks. Matter shows up in the trace of the curvature. That's the "
            "clue Einstein needed."
        ) as vo:
            vo.wait_until("r")
            self.add(rg)
            self.play(kk.animate.set_value(1.0), run_time=3, rate_func=linear)
            vo.wait_until("t")
            self.play(Write(trace[0]))
            vo.wait_until("v")
            self.play(FadeIn(trace[1]))
            vo.wait_until("m")
            self.play(FadeIn(trace[2]))
        rg.clear_updaters()
        self.clear_scene()
