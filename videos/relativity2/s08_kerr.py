from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity2 import spacetime as st
from videos.relativity2.common import (View3D, clamp_x, curve3d, label, load, mtex, note, polyline, redraw, spheroid,
                                       zigzag_curve)
from videos.relativity2.geometry import check_kerr

SPIN, HOR = C.SPIN, C.CURVATURE


class Kerr(VoiceoverScene):
    def construct(self):
        res = check_kerr()
        assert res["ricci_flat"]
        self.metric()
        self.anatomy()
        self.band()
        self.circles()

    # ------------------------------------------------------------------
    def metric(self):
        m = mtex(r"ds^2", r"=", r"-\Big(1 - \frac{2Mr}{\Sigma}\Big)dt^2", r"-\frac{4Mar\sin^2\theta}{\Sigma}\,dt\,d\phi",
                 r"+\frac{\Sigma}{\Delta}dr^2 + \Sigma\,d\theta^2", font_size=40)
        m2 = mtex(r"+\Big(r^2 + a^2 + \frac{2Ma^2r\sin^2\theta}{\Sigma}\Big)\sin^2\theta\,d\phi^2", font_size=40)
        defs = mtex(r"\Sigma = r^2 + a^2\cos^2\theta,\qquad \Delta = r^2 - 2Mr + a^2,\qquad a = \frac{J}{M}", font_size=34)
        m[2].set_color(C.PROPER_TIME)
        m[3].set_color(SPIN)
        m[4].set_color(C.METRIC)
        m2.set_color(C.METRIC)
        g = VGroup(m, m2, defs).arrange(DOWN, buff=0.25).to_edge(UP, buff=0.4)
        m2.align_to(m[2], LEFT)
        hist = label(r"Roy Kerr, 1963; written this way by Boyer \& Lindquist, 1967", font_size=24,
                     color=GREY_A).next_to(g, DOWN, buff=0.25)
        checks = VGroup(
            label(r"$R_{\mu\nu} = 0$: a vacuum solution (all ten components checked, exactly, with sympy)", font_size=26),
            label(r"$a \to 0$: Schwarzschild", font_size=26),
            label(r"$M \to 0$: flat spacetime, in spheroidal coordinates (Riemann $= 0$)", font_size=26),
            label(r"$r \to \infty$: \ $g_{t\phi} \to -2J\sin^2\theta/r$, the gravitomagnetic field of any spinning body",
                  font_size=26, color=SPIN),
            label(r"no hair: the \emph{only} stationary vacuum black holes (Carter 1971, Robinson 1975)", font_size=26,
                  color=HOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).next_to(hist, DOWN, buff=0.4)
        with self.voiceover(
            "<bookmark mark='a'/> Real stars rotate, and a collapsing star spins faster and faster, like a skater "
            "pulling in their arms. So real black holes spin. The spacetime of a spinning black hole wasn't found until 1963, "
            "when Roy Kerr discovered this: the Kerr metric, with mass M and angular momentum J equal to M times a. "
            "<bookmark mark='b'/> Like Schwarzschild's, it's a solution of Einstein's equation in empty space; our "
            "symbolic code confirms that all ten components of its Ricci tensor vanish. <bookmark mark='c'/> With no "
            "spin, it's Schwarzschild. With no mass, it's flat spacetime in unusual coordinates. And far away, its "
            "time-space term is exactly the gravitomagnetic field we just derived. <bookmark mark='d'/> Remarkably, "
            "it's the only possibility: every stationary black hole in empty space is a Kerr black hole, described by "
            "just two numbers. Black holes have no hair."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(m), Write(m2), run_time=5)
            self.play(FadeIn(defs), FadeIn(hist))
            vo.wait_until("b")
            self.play(FadeIn(checks[0]))
            vo.wait_until("c")
            self.play(FadeIn(checks[1:4], lag_ratio=0.4), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(checks[4]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def anatomy(self):
        """A meridional cross-section (the x-z plane, Kerr-Schild Cartesian coordinates) as the spin grows."""
        cen = np.array([3.2, -0.3, 0])
        sc = 1.45
        A = ValueTracker(0.02)
        th = np.linspace(0, np.pi, 200)

        def section(r_of_th, a):
            r = r_of_th(th)
            x, z = np.sqrt(r * r + a * a) * np.sin(th), r * np.cos(th)
            right = np.stack([cen[0] + sc * x, cen[1] + sc * z, 0 * x], 1)
            left = np.stack([cen[0] - sc * x[::-1], cen[1] + sc * z[::-1], 0 * x], 1)
            return np.concatenate([right, left])

        def bodies():
            a = A.get_value()
            rp, rm = st.r_plus(a), st.r_minus(a)
            g = VGroup()
            ergo = section(lambda t_: st.r_ergo(a, t_), a)
            hor = section(lambda t_: np.full_like(t_, rp), a)
            g.add(Polygon(*ergo, stroke_color=SPIN, stroke_width=3, fill_color=SPIN, fill_opacity=0.22))
            g.add(Polygon(*hor, stroke_color=HOR, stroke_width=4, fill_color=BLACK, fill_opacity=1))
            if a > 0.1:
                g.add(Polygon(*section(lambda t_: np.full_like(t_, rm), a), stroke_color=GREY_B, stroke_width=2,
                              fill_opacity=0).set_stroke(opacity=0.8))
            for sx in (1, -1):
                g.add(Dot(cen + sc * np.array([sx * a, 0, 0]), radius=0.07, color=C.SINGULARITY))
            return g

        B = redraw(bodies)
        axis = Line(cen + DOWN * 3.3, cen + UP * 3.3, color=GREY_C, stroke_width=1.5)
        spin = Arrow(cen + UP * 2.75, cen + UP * 3.4, buff=0, color=SPIN, stroke_width=5)
        labs = VGroup(label(r"spin axis", font_size=20, color=GREY_B).next_to(cen + UP * 3.3, LEFT, buff=0.1))
        eqs = VGroup(
            label(r"horizons, where $\Delta = 0$:", font_size=26),
            mtex(r"r_\pm = M \pm \sqrt{M^2 - a^2}", font_size=36, color=HOR),
            label(r"ergosurface, where $g_{tt} = 0$:", font_size=26),
            mtex(r"r_E = M + \sqrt{M^2 - a^2\cos^2\theta}", font_size=36, color=SPIN),
            label(r"ring singularity, where $\Sigma = 0$:", font_size=26),
            mtex(r"r = 0,\ \theta = \tfrac{\pi}{2}\ \text{(a ring of radius } a)", font_size=34, color=C.SINGULARITY),
            label(r"$a > M$: no horizon at all, a naked singularity", font_size=24, color=GREY_A),
            label(r"(cosmic censorship conjecture: nature forbids it)", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(LEFT, buff=0.5)
        rd = VGroup(mtex(r"a/M =", font_size=32, color=SPIN), DecimalNumber(0.02, num_decimal_places=2, font_size=32,
                                                                              color=SPIN)).arrange(RIGHT, buff=0.12)
        rd.to_corner(UR, buff=0.35)
        rd[1].add_updater(lambda m: m.set_value(A.get_value()))
        key = VGroup(label(r"outer horizon", font_size=20, color=HOR), label(r"inner horizon", font_size=20, color=GREY_B),
                     label(r"ergosphere", font_size=20, color=SPIN), label(r"ring singularity", font_size=20,
                                                                          color=C.SINGULARITY)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        key.next_to(rd, DOWN, buff=0.2).align_to(rd, RIGHT)
        cap = note(r"a slice through the spin axis, in Kerr--Schild coordinates ($x^2 + y^2 = (r^2 + a^2)\sin^2\theta$, $z = r\cos\theta$)")
        cap.to_corner(DR, buff=0.2)
        with self.voiceover(
            "What does a Kerr black hole look like? Here's a slice through it, containing the spin axis. "
            "<bookmark mark='a'/> The horizon is where g r r blows up, where Delta vanishes. That happens at two radii, "
            "r plus and r minus. <bookmark mark='b'/> Let's turn up the spin. As a grows, the outer horizon shrinks, "
            "from two M toward M, and an inner horizon appears inside it. <bookmark mark='c'/> Outside the horizon "
            "there's a new surface, where g t t vanishes, which touches the horizon at the poles and bulges out at the "
            "equator: the boundary of the ergosphere. <bookmark mark='d'/> And the singularity is no longer a point: "
            "it's a ring, of radius a, here cut in two places. <bookmark mark='e'/> If a exceeded M, there'd be no "
            "horizon at all, and the singularity would be naked, visible from outside. Penrose conjectured that nature "
            "never allows that. This cosmic censorship conjecture is still unproven, but no generic process that "
            "violates it is known."
        ) as vo:
            self.add(axis, B)
            self.play(GrowArrow(spin), FadeIn(labs), FadeIn(rd), FadeIn(key), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(eqs[:2]))
            vo.wait_until("b")
            self.play(A.animate.set_value(0.95), run_time=6, rate_func=smooth)
            vo.wait_until("c")
            self.play(FadeIn(eqs[2:4]))
            vo.wait_until("d")
            self.play(FadeIn(eqs[4:6]))
            vo.wait_until("e")
            self.play(FadeIn(eqs[6:]), A.animate.set_value(0.998), run_time=2.5)
        for mob in (B, rd[1]):
            mob.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def band(self):
        d = load("kerr_orbits")
        a = float(d["band_a"])
        r, lo, hi, z = d["band_r"], d["band_min"], d["band_max"], d["band_zamo"]
        ax = Axes(x_range=[1.4, 4.0, 0.5], y_range=[-0.6, 0.6, 0.2], x_length=7.4, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_B, "font_size": 20},
                  x_axis_config={"numbers_to_include": [1.5, 2, 2.5, 3, 3.5, 4]},
                  y_axis_config={"numbers_to_include": [-0.4, -0.2, 0.2, 0.4]}).move_to([-1.3, -0.7, 0])
        xl = label(r"$r/M$ (equator, $a = 0.9M$)", font_size=22).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = label(r"$\Omega = d\phi/dt$ allowed for something at fixed $r$", font_size=22).next_to(ax, UP, buff=0.45)
        top = polyline(ax, r, hi, color=SPIN, stroke_width=3)
        bot = polyline(ax, r, lo, color=SPIN, stroke_width=3)
        pts = [ax.c2p(x, y) for x, y in zip(r, hi)] + [ax.c2p(x, y) for x, y in zip(r[::-1], lo[::-1])]
        fill = Polygon(*pts, stroke_width=0, fill_color=SPIN, fill_opacity=0.25)
        zero = DashedLine(ax.c2p(1.4, 0), ax.c2p(4.0, 0), color=GREY_B, stroke_width=1.5)
        ergo = DashedLine(ax.c2p(2.0, -0.6), ax.c2p(2.0, 0.6), color=SPIN, stroke_width=2.5)
        hor = DashedLine(ax.c2p(st.r_plus(a), -0.6), ax.c2p(st.r_plus(a), 0.6), color=HOR, stroke_width=2.5)
        el = label(r"ergosurface", font_size=20, color=SPIN).next_to(ax.c2p(2.0, 0.6), UP, buff=0.05)
        hl = label(r"horizon", font_size=20, color=HOR).next_to(ax.c2p(st.r_plus(a), 0.6), UP, buff=0.05)
        cond = VGroup(
            mtex(r"g_{tt} + 2\Omega\, g_{t\phi} + \Omega^2 g_{\phi\phi} < 0", font_size=32),
            label(r"(a timelike worldline)", font_size=22, color=GREY_A),
            label(r"inside the ergosurface,", font_size=24),
            label(r"$\Omega = 0$ is not allowed:", font_size=24),
            label(r"nothing can stand still", font_size=24, color=SPIN),
            mtex(r"\Omega_H = \frac{a}{r_+^2 + a^2}", font_size=32, color=HOR),
            label(r"the horizon rotates", font_size=22, color=HOR),
        ).arrange(DOWN, buff=0.14).move_to([5.0, 0.0, 0])
        assert np.all(lo[r < 1.99] > 0) and abs(lo[np.argmin(np.abs(r - 2))]) < 2e-3
        with self.voiceover(
            "The ergosphere is where frame dragging becomes irresistible. <bookmark mark='a'/> Ask: at a fixed radius, "
            "how fast can something orbit, as seen from far away? For its worldline to be timelike, slower than light, "
            "its angular velocity Omega has to make this quadratic negative, which confines it to a band. "
            "<bookmark mark='b'/> Far out, the band includes zero, and in either direction you can go is fine. "
            "<bookmark mark='c'/> At the ergosurface, the lower edge reaches zero. Inside, the whole band is positive: "
            "no rocket, however powerful, can hold you still relative to the distant stars. You must rotate with the "
            "hole. <bookmark mark='d'/> At the horizon, the band closes to a single value, Omega H: the horizon itself "
            "rotates rigidly at that rate."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(zero), FadeIn(cond[:2]))
            vo.wait_until("b")
            self.play(FadeIn(fill), Create(top), Create(bot), run_time=2)
            vo.wait_until("c")
            self.play(Create(ergo), FadeIn(el), FadeIn(cond[2:5]))
            vo.wait_until("d")
            self.play(Create(hor), FadeIn(hl), FadeIn(cond[5:]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def circles(self):
        """Where light emitted at each point of the equatorial plane is after a short coordinate time dt: a circle of
        radius sqrt(g_tphi^2/g_phiphi - g_tt) dt, displaced prograde by -g_tphi dt / sqrt(g_phiphi) (in local proper
        lengths).  It contains its source exactly when g_tt < 0."""
        cen = np.array([0.0, -0.3, 0])
        sc = 0.78
        A = ValueTracker(0.0)
        dt = 0.8
        pts = [(r0, ph0) for r0 in (1.55, 1.8, 2.4, 3.2, 4.1) for ph0 in np.linspace(0, 2 * np.pi, 8 if r0 > 2.5 else 6,
                                                                                   endpoint=False)]

        def light():
            a = A.get_value()
            g = VGroup()
            rp = st.r_plus(a)
            g.add(Circle(radius=rp * sc, color=HOR, stroke_width=3, fill_color=BLACK, fill_opacity=1).move_to(cen))
            g.add(DashedVMobject(Circle(radius=2 * sc, color=SPIN, stroke_width=2.5).move_to(cen), num_dashes=50))
            for r0, ph0 in pts:
                if r0 <= rp * 1.02:
                    continue
                gtt, gtp, gpp, S, D = st.kerr_metric(r0, math.pi / 2, a)
                rad = math.sqrt(max(gtp * gtp / gpp - gtt, 0)) * dt
                yc = -gtp / math.sqrt(gpp) * dt
                p = cen + sc * r0 * np.array([math.cos(ph0), math.sin(ph0), 0])
                tang = np.array([-math.sin(ph0), math.cos(ph0), 0])
                c0 = p + sc * yc * tang
                inside = gtt < 0
                g.add(Circle(radius=sc * rad, color=C.LIGHT, stroke_width=2,
                             fill_color=C.LIGHT, fill_opacity=0.18).move_to(c0))
                g.add(Dot(p, radius=0.045, color=WHITE if inside else C.SINGULARITY))
            return g

        L = redraw(light)
        rd = VGroup(mtex(r"a/M =", font_size=32, color=SPIN), DecimalNumber(0.0, num_decimal_places=2, font_size=32,
                                                                             color=SPIN)).arrange(RIGHT, buff=0.12)
        rd.to_corner(UL, buff=0.4)
        rd[1].add_updater(lambda m: m.set_value(A.get_value()))
        leg = VGroup(label(r"each circle: where a flash from the dot has reached", font_size=22, color=C.LIGHT),
                     label(r"after a short time $dt$ (equatorial plane, seen from above)", font_size=22, color=C.LIGHT),
                     label(r"dashed: the ergosurface", font_size=22, color=SPIN),
                     label(r"red dots: the flash can't even reach its source", font_size=22, color=C.SINGULARITY)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_corner(UR, buff=0.3)
        cap = note(r"computed from the Kerr metric in Boyer--Lindquist coordinates ($r$ as radius, $t$ of a distant observer)")
        cap.to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Here's a way to see the dragging directly. <bookmark mark='a'/> In the equatorial plane, set off a flash "
            "of light at each dot, and draw where the light has reached a moment later. Without spin, each flash is a "
            "circle around its source. <bookmark mark='b'/> Turn up the spin. The circles are swept around in the "
            "direction of rotation, most strongly near the hole. <bookmark mark='c'/> Inside the ergosurface, every "
            "circle is carried completely off its source: even light can't move against the rotation, or even stay "
            "put. That's why it's called the ergosphere, from the Greek for work: as we'll see next, energy can be "
            "extracted from it."
        ) as vo:
            vo.wait_until("a")
            self.add(L)
            self.play(FadeIn(rd), FadeIn(leg[:2]), FadeIn(cap))
            vo.wait_until("b")
            self.play(A.animate.set_value(0.95), FadeIn(leg[2:]), run_time=5, rate_func=smooth)
        L.clear_updaters()
        rd[1].clear_updaters()
        self.clear_scene()
