from __future__ import annotations

import math

import numpy as np
import sympy as sp

from explainer import *  # noqa: F403
from videos.relativity.common import (View3D, boxed, curve3d, label, ladder, load, mtex, note, part_card, polyline,
                                      sci, stack)
from videos.relativity.geometry import same, schwarzschild, static_spherical


class Schwarzschild(VoiceoverScene):
    def construct(self):
        A, _ = static_spherical()
        assert len(A.nonzero_gammas()) == 9
        Sw, (t, r, th, ph, rs) = schwarzschild()
        assert all(Sw.ricci[i, j] == 0 for i in range(4) for j in range(4))
        assert same(Sw.kretschmann(), 12 * rs**2 / r**6)
        self.card()
        self.ansatz()
        self.ricci()
        self.solve()
        self.numbers()
        self.clocks()
        self.flamm()
        self.cones()

    def card(self):
        c = part_card(4, r"Solutions and tests", r"black holes, orbits, light, and waves")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def ansatz(self):
        prob = VGroup(
            label(r"Outside a static, spherical star: \ $T_{\mu\nu} = 0$", font_size=34),
            mtex(r"R_{\mu\nu} = \kappa\Big(T_{\mu\nu} - \tfrac12 T g_{\mu\nu}\Big) = 0", font_size=40, color=C.CURVATURE),
        ).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.5)
        ans = mtex(r"ds^2", r"=", r"-e^{2\alpha(r)}\,c^2dt^2", r"+", r"e^{2\beta(r)}\,dr^2", r"+",
                   r"r^2\big(d\theta^2 + \sin^2\theta\,d\phi^2\big)", font_size=44)
        ans[2].set_color(C.PROPER_TIME)
        ans[4].set_color(C.METRIC)
        ans.next_to(prob, DOWN, buff=0.8)
        notes = VGroup(
            label(r"static: nothing depends on $t$, no $dt\,dr$ terms", font_size=28, color=GREY_A),
            label(r"spherical: $r$ is defined so the sphere at $r$ has area $4\pi r^2$", font_size=28, color=GREY_A),
            label(r"two unknown functions: $\alpha(r)$ and $\beta(r)$", font_size=30),
        ).arrange(DOWN, buff=0.22).next_to(ans, DOWN, buff=0.6)
        with self.voiceover(
            "Einstein's equation is ten coupled nonlinear partial differential equations, and Einstein himself had "
            "worked only with approximate solutions. The first exact one came within weeks, and its simplicity surprised "
            "him. <bookmark mark='p'/> Take the simplest "
            "situation: empty space outside a static, spherical star. There, T is zero, so the trace-reversed equation "
            "says simply that the Ricci tensor vanishes. <bookmark mark='a'/> Symmetry narrows down the metric enormously. "
            "<bookmark mark='s'/> Static means nothing depends on time. Spherical means the angular part is r squared times "
            "the metric of a sphere, with r defined so that the sphere at r has area four pi r squared. "
            "<bookmark mark='u'/> All that's left unknown are two functions of r: alpha in the time part, and beta in the "
            "radial part."
        ) as vo:
            vo.wait_until("p")
            self.play(FadeIn(prob, lag_ratio=0.3))
            vo.wait_until("a")
            self.play(Write(ans))
            vo.wait_until("s")
            self.play(FadeIn(notes[:2], lag_ratio=0.3))
            vo.wait_until("u")
            self.play(FadeIn(notes[2]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def ricci(self):
        gam = VGroup(
            mtex(r"\Gamma^t{}_{tr} = \alpha'", r"\quad", r"\Gamma^r{}_{tt} = e^{2(\alpha-\beta)}\alpha'", r"\quad",
                 r"\Gamma^r{}_{rr} = \beta'", font_size=30),
            mtex(r"\Gamma^\theta{}_{r\theta} = \Gamma^\phi{}_{r\phi} = \tfrac1r", r"\quad",
                 r"\Gamma^r{}_{\theta\theta} = -r e^{-2\beta}", r"\quad", r"\Gamma^r{}_{\phi\phi} = -r e^{-2\beta}\sin^2\theta",
                 font_size=30),
            mtex(r"\Gamma^\theta{}_{\phi\phi} = -\sin\theta\cos\theta", r"\quad", r"\Gamma^\phi{}_{\theta\phi} = \cot\theta",
                 font_size=30),
        ).arrange(DOWN, buff=0.18).to_edge(UP, buff=0.4)
        gam.set_color(C.CONNECTION)
        gl = note(r"the nonzero Christoffel symbols ($' = d/dr$; units $c = 1$)", font_size=22).next_to(gam, DOWN, buff=0.15)
        ric = VGroup(
            mtex(r"R_{tt}", r"=", r"e^{2(\alpha-\beta)}\Big[\alpha'' + \alpha'^2 - \alpha'\beta' + \tfrac{2}{r}\alpha'\Big]", font_size=38),
            mtex(r"R_{rr}", r"=", r"-\alpha'' - \alpha'^2 + \alpha'\beta' + \tfrac{2}{r}\beta'", font_size=38),
            mtex(r"R_{\theta\theta}", r"=", r"e^{-2\beta}\big[r(\beta' - \alpha') - 1\big] + 1", font_size=38),
            mtex(r"R_{\phi\phi}", r"=", r"\sin^2\theta\; R_{\theta\theta}", font_size=38),
        )
        for rr in ric:
            rr[0].set_color(C.CURVATURE)
        ric = stack(*ric, buff=0.32).next_to(gl, DOWN, buff=0.45)
        chk = note(r"computed symbolically (sympy) from the metric; every other component is zero", font_size=22).next_to(ric, DOWN, buff=0.25)
        with self.voiceover(
            "Now it's just computation, the same machinery we've built, applied to this metric. <bookmark mark='g'/> First "
            "the Christoffel symbols: nine kinds are nonzero. <bookmark mark='r'/> Then the Ricci tensor, through the "
            "formula for Riemann and one contraction. Everything off the diagonal vanishes, and the four diagonal components "
            "are these. They look complicated, but setting them to zero is surprisingly easy."
        ) as vo:
            vo.wait_until("g")
            self.play(FadeIn(gam, lag_ratio=0.2), FadeIn(gl), run_time=2)
            vo.wait_until("r")
            self.play(FadeIn(ric, lag_ratio=0.2), run_time=2.5)
            self.play(FadeIn(chk))
        self.ric = ric
        self.play(FadeOut(VGroup(gam, gl, chk)), ric.animate.scale(0.75).to_edge(UP, buff=0.3))
        self.ric_small = ric

    # ------------------------------------------------------------------
    def solve(self):
        ric = self.ric_small
        rows = [
            mtex(r"e^{2(\beta-\alpha)}R_{tt} + R_{rr}", r"=", r"\tfrac{2}{r}\big(\alpha' + \beta'\big) = 0", font_size=38),
            mtex(r"\beta", r"=", r"-\alpha", font_size=38),
            mtex(r"R_{\theta\theta}", r"=", r"1 - e^{2\alpha}\big(2r\alpha' + 1\big) = 1 - \frac{d}{dr}\big(r e^{2\alpha}\big) = 0",
                 font_size=38),
            mtex(r"e^{2\alpha}", r"=", r"1 - \frac{r_s}{r}", font_size=42),
        ]
        whys = [
            note(r"the second derivatives cancel", font_size=22),
            note(r"(a constant can be absorbed into $t$)", font_size=22),
            note(r"substitute $\beta = -\alpha$", font_size=22),
            note(r"integrate: $r e^{2\alpha} = r - r_s$", font_size=22),
        ]
        for rr in rows:
            rr[0].set_color(C.CURVATURE)
        rows[1][0].set_color(WHITE)
        rows[3][0].set_color(C.PROPER_TIME)
        x0 = -0.8
        for rr, w in zip(rows, whys):
            rr.shift((x0 - rr[1].get_center()[0]) * RIGHT)
            w.next_to(rr, DOWN, buff=0.08).align_to(rr, RIGHT)
        step = ladder(self, rows, whys, keep=4, top=0.9, x=x0, buff=0.55)
        with self.voiceover(
            "<bookmark mark='a'/> Add the first two, with the right factor, and every second derivative cancels, leaving "
            "two over r times alpha prime plus beta prime. <bookmark mark='b'/> So beta is minus alpha. "
            "<bookmark mark='c'/> Substitute that into the angular equation, and it becomes the derivative of r times e to "
            "the two alpha, which must equal one. <bookmark mark='d'/> Integrate: r e to the two alpha is r minus a "
            "constant, which we'll call r s. So e to the two alpha is one minus r s over r."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.clear_scene()
        newton = stack(
            mtex(r"g_{tt}", r"=", r"-\Big(1 - \frac{r_s}{r}\Big)", font_size=40),
            mtex(r"g_{tt}", r"\approx", r"-\Big(1 + \frac{2\Phi}{c^2}\Big) = -\Big(1 - \frac{2GM}{rc^2}\Big)", font_size=40),
            mtex(r"r_s", r"=", r"\frac{2GM}{c^2}", font_size=46),
            buff=0.45,
        ).to_edge(UP, buff=0.5)
        for rr in newton:
            rr[0].set_color(C.PROPER_TIME)
        newton[2][0].set_color(WHITE)
        sol = mtex(r"ds^2", r"=", r"-\Big(1 - \frac{2GM}{rc^2}\Big)c^2dt^2", r"+", r"\frac{dr^2}{1 - \frac{2GM}{rc^2}}", r"+",
                   r"r^2\,d\Omega^2", font_size=48)
        sol[2].set_color(C.PROPER_TIME)
        sol[4].set_color(C.METRIC)
        sb = boxed(sol, color=C.CURVATURE, buff=0.3).next_to(newton, DOWN, buff=0.6)
        hist = label(r"Karl Schwarzschild, letter to Einstein from the Russian front, 22 December 1915", font_size=26,
                     color=GREY_A).next_to(sb, DOWN, buff=0.3)
        birk = label(r"Birkhoff: the \emph{only} spherically symmetric vacuum solution, even if the star pulsates", font_size=26,
                     color=GREY_A).next_to(hist, DOWN, buff=0.2)
        with self.voiceover(
            "What is r s? <bookmark mark='a'/> Far away, the time part of the metric has to match the weak-field form we "
            "found from clocks: minus one plus two phi over c squared, with phi equal to minus G M over r. "
            "<bookmark mark='b'/> So r s is two G M over c squared. <bookmark mark='s'/> This is the Schwarzschild solution, "
            "found by Karl Schwarzschild in December 1915, while he was serving as an artillery officer on the Russian "
            "front. He died the following May. <bookmark mark='k'/> And by Birkhoff's theorem, it's the only spherically "
            "symmetric solution in empty space: even a pulsating star has exactly this field outside it."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(newton[0]))
            self.play(Write(newton[1]))
            vo.wait_until("b")
            self.play(Write(newton[2]))
            vo.wait_until("s")
            self.play(Write(sol), Create(sb[0]), run_time=2)
            self.play(FadeIn(hist))
            vo.wait_until("k")
            self.play(FadeIn(birk))
        self.clear_scene()

    # ------------------------------------------------------------------
    def numbers(self):
        c = load("consts")
        rs_sun, rs_earth = float(c["rs_sun"]), float(c["rs_earth"])
        es, us = float(c["earth_surface"]), float(c["earth_us_per_day"])
        assert abs(rs_sun / 1000 - 2.95) < 0.01 and abs(rs_earth * 1000 - 8.87) < 0.01
        assert abs(es - 6.96e-10) < 0.01e-10 and round(us) == 60
        rows = VGroup(
            mtex(r"\text{Sun:}\quad r_s = 2.95\ \text{km}\quad(\text{radius } 696{,}000\ \text{km})", font_size=36),
            mtex(r"\text{Earth:}\quad r_s = 8.87\ \text{mm}\quad(\text{radius } 6{,}371\ \text{km})", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(UP, buff=0.7)
        clock = mtex(r"\frac{d\tau}{dt}\Big|_{\text{Earth's surface}}", r"=", r"\sqrt{1 - \frac{r_s}{R_\oplus}}",
                     r"\approx", r"1 - " + sci(es, 2), font_size=40)
        clock[0].set_color(C.PROPER_TIME)
        clock.next_to(rows, DOWN, buff=0.8)
        cl = label(r"a clock on the ground loses $\approx 60\ \mu$s per day relative to one far away", font_size=28,
                   color=C.PROPER_TIME).next_to(clock, DOWN, buff=0.3)
        with self.voiceover(
            "How big is r s? <bookmark mark='a'/> For the Sun, about three kilometers, buried deep inside a star seven "
            "hundred thousand kilometers in radius. For the Earth, nine millimeters. <bookmark mark='b'/> So for ordinary "
            "bodies, the corrections are tiny: a clock on the Earth's surface runs slow, relative to one far out in space, "
            "by seven parts in ten billion, about sixty microseconds a day."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows, lag_ratio=0.3))
            vo.wait_until("b")
            self.play(Write(clock), FadeIn(cl))
        self.clear_scene()

    # ------------------------------------------------------------------
    def clocks(self):
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 1.05, 0.25], x_length=7.0, y_length=4.0, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": True, "font_size": 22},
                  x_axis_config={"numbers_to_include": [1, 2, 3, 4, 5, 6]},
                  y_axis_config={"numbers_to_include": [0.25, 0.5, 0.75, 1.0]})
        ax.move_to(DOWN * 0.4)
        xl = MathTex(r"r / r_s", font_size=30).next_to(ax.x_axis, RIGHT, buff=0.2)
        yl = mtex(r"d\tau / dt = \sqrt{1 - r_s/r}", font_size=32, color=C.PROPER_TIME).next_to(ax, UP, buff=0.3)
        r = np.linspace(1.0, 6, 400)
        cur = polyline(ax, r, np.sqrt(1 - 1 / r), color=C.PROPER_TIME, stroke_width=4)
        hz = DashedLine(ax.c2p(1, 0), ax.c2p(1, 1.05), color=C.CURVATURE, stroke_width=3)
        hl = label(r"$r = r_s$", font_size=26, color=C.CURVATURE).next_to(ax.c2p(1, 1.05), UP, buff=0.1)
        with self.voiceover(
            "But the solution itself goes much further. <bookmark mark='a'/> Here's the rate of a clock at rest, as a "
            "function of r. Far away it's one. Closer in, it slows, <bookmark mark='b'/> and at r equals r s, it stops "
            "altogether, as seen from far away. Something strange happens there."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(cur), run_time=2)
            vo.wait_until("b")
            self.play(Create(hz), FadeIn(hl))
        self.clear_scene()

    # ------------------------------------------------------------------
    def flamm(self):
        view = View3D(center=[-2.6, -1.6, 0], scale=0.62, azimuth=0.4, elevation=0.42)

        def z(r):
            return 2 * np.sqrt(np.maximum(r - 1, 0))

        rings = [1.0, 1.1, 1.3, 1.6, 2.0, 2.6, 3.3, 4.2, 5.2, 6.4]
        sheet = VGroup()
        for rr in rings:
            a = np.linspace(0, 2 * np.pi, 140)
            P = np.stack([rr * np.cos(a), rr * np.sin(a), z(rr) * np.ones_like(a)], 1)
            sheet.add(curve3d(view, P, color=C.METRIC, stroke_width=2.2 if rr > 1 else 4, sphere_r=None,
                              back_opacity=1.0))
        for a in np.linspace(0, 2 * np.pi, 24, endpoint=False):
            rr = np.linspace(1.0, 6.4, 80)
            P = np.stack([rr * np.cos(a), rr * np.sin(a), z(rr)], 1)
            sheet.add(curve3d(view, P, color=C.METRIC, stroke_width=1.6, sphere_r=None))
        sheet[0].set_color(C.CURVATURE)
        hor = label(r"$r = r_s$", font_size=26, color=C.CURVATURE).next_to(sheet[0], DOWN, buff=0.15)
        eq = mtex(r"d\ell", r"=", r"\frac{dr}{\sqrt{1 - r_s/r}}", font_size=40)
        eq[0].set_color(C.METRIC)
        txt = VGroup(
            label(r"Space, at one moment, in the equatorial plane:", font_size=28),
            label(r"the circle at $r$ still has circumference $2\pi r$,", font_size=28),
            label(r"but the distance between circles is stretched:", font_size=28),
            eq,
            note(r"Flamm's paraboloid (1916): an embedding of the spatial geometry; not a rubber sheet", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5).shift(UP * 0.8)
        with self.voiceover(
            "Space is curved too, and we can picture it, with care. <bookmark mark='a'/> Take a slice through the "
            "equatorial plane, at one moment of time. Circles around the center still have circumference two pi r, but the "
            "radial distance between neighboring circles is stretched by one over the square root of one minus r s over r. "
            "<bookmark mark='b'/> A two-dimensional surface with exactly those distances is this funnel, Flamm's "
            "paraboloid. Unlike the rubber sheet, it's an honest picture of the geometry of space, and nothing rolls down "
            "it: it only shows that, near r s, there's more room between the circles than flat space allows."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(txt[:4], lag_ratio=0.2), run_time=2)
            vo.wait_until("b")
            self.play(Create(sheet, lag_ratio=0.02), run_time=2.5)
            self.play(FadeIn(hor), FadeIn(txt[4]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def cones(self):
        ax = Axes(x_range=[0, 5, 1], y_range=[0, 4, 1], x_length=7.0, y_length=5.4, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False})
        ax.to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        xl = MathTex(r"r / r_s", font_size=30).next_to(ax.x_axis, RIGHT, buff=0.2)
        yl = MathTex(r"ct", font_size=30, color=C.PROPER_TIME).next_to(ax.y_axis, UP, buff=0.15)
        hz = DashedLine(ax.c2p(1, 0), ax.c2p(1, 4), color=C.CURVATURE, stroke_width=3)
        hl = label(r"horizon", font_size=26, color=C.CURVATURE).next_to(ax.c2p(1, 4), UP, buff=0.1)
        cones = VGroup()
        for r0 in (1.15, 1.5, 2.2, 3.2, 4.4):
            s = 1 - 1 / r0  # dr/(c dt) = +-(1 - r_s/r)
            h = 0.55
            tip = ax.c2p(r0, 1.6)
            a, b = ax.c2p(r0 - s * h, 1.6 + h), ax.c2p(r0 + s * h, 1.6 + h)
            cones.add(VGroup(Polygon(tip, a, b, stroke_width=0, fill_color=C.LIGHT, fill_opacity=0.3),
                             Line(tip, a, color=C.LIGHT, stroke_width=2.5), Line(tip, b, color=C.LIGHT, stroke_width=2.5)))
        eq = mtex(r"\frac{dr}{c\,dt}", r"=", r"\pm\Big(1 - \frac{r_s}{r}\Big)", font_size=40)
        eq[0].set_color(C.LIGHT)
        eq.to_corner(UR, buff=0.6)
        eql = label(r"light, in these coordinates", font_size=26, color=GREY_A).next_to(eq, DOWN, buff=0.15)
        k = mtex(r"R_{\alpha\beta\gamma\delta}R^{\alpha\beta\gamma\delta}", r"=", r"\frac{12\,r_s^2}{r^6}", font_size=38)
        k[0].set_color(C.CURVATURE)
        kl = VGroup(label(r"finite at $r = r_s$: the coordinates fail there, not spacetime", font_size=26, color=GREY_A),
                    label(r"infinite at $r = 0$: a true singularity", font_size=26, color=GREY_A))
        kl.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        VGroup(k, kl).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(eql, DOWN, buff=0.7).to_edge(RIGHT, buff=0.4)
        bh = label(r"Inside $r_s$, every future leads inward. \ A black hole.", font_size=30, color=C.CURVATURE)
        bh.to_edge(DOWN, buff=0.35).shift(RIGHT * 2.6)
        with self.voiceover(
            "<bookmark mark='a'/> Here's what's strange. Draw the paths of light rays, in these coordinates. Far away, light "
            "cones have their usual forty-five degree shape. <bookmark mark='b'/> Closer in, they narrow, and at r s they "
            "close up completely: as seen from far away, light there can't make progress outward. "
            "<bookmark mark='k'/> Is spacetime itself broken at r s? No. The curvature, measured by an invariant like this "
            "one, built from Riemann, is perfectly finite there. It's the coordinates that fail, like longitude at the "
            "North Pole. The real singularity is at r equals zero, where curvature becomes infinite. "
            "<bookmark mark='h'/> But r s is real in another sense: in better coordinates, you find that inside it, every "
            "future direction points inward. Nothing that crosses it can come back out. It's the event horizon of a black "
            "hole."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Write(eq), FadeIn(eql))
            self.play(FadeIn(cones[-1]), FadeIn(cones[-2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cones[:-2][::-1]], lag_ratio=0.4), Create(hz), FadeIn(hl))
            vo.wait_until("k")
            self.play(Write(k), FadeIn(kl))
            vo.wait_until("h")
            self.play(FadeIn(bh))
        self.clear_scene()
