from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity.common import View3D, boxed, label, load, mtex, note, polyline, stack


def cloud(view: View3D, P, color, r=0.055):
    """Project a 3D point cloud with depth cues (nearer: bigger, brighter)."""
    S, depth = view.project(P)
    order = np.argsort(depth)
    g = VGroup()
    dmin, dmax = -1.6, 1.6
    for i in order:
        f = np.clip((depth[i] - dmin) / (dmax - dmin), 0, 1)
        g.add(Dot(S[i], radius=r * (0.7 + 0.6 * f), color=color, fill_opacity=0.35 + 0.65 * f))
    return g


class Meaning(VoiceoverScene):
    def construct(self):
        self.statement()
        self.balls()
        self.weyl()
        self.cosmos()

    # ------------------------------------------------------------------
    def statement(self):
        q = VGroup(
            label(r"Take a small ball of freely falling test particles, initially at rest relative to each other.",
                  font_size=30),
            label(r"The rate at which it begins to shrink is proportional to its volume times", font_size=30),
            label(r"the energy density at its center, plus the pressures in the $x$, $y$ and $z$ directions.",
                  font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(UP, buff=0.6)
        who = note(r"after John Baez and Emory Bunn, \emph{The Meaning of Einstein's Equation} (2005)").next_to(q, DOWN, buff=0.25)
        eq = mtex(r"\frac{\ddot V}{V}\Big|_{t=0}", r"=", r"-4\pi G\,\Big(\rho + \frac{p_x + p_y + p_z}{c^2}\Big)",
                  font_size=50)
        eq[0].set_color(C.CURVATURE)
        eq[2].set_color(C.MATTER)
        eb = boxed(eq, color=C.CURVATURE, buff=0.3).next_to(who, DOWN, buff=0.6)
        why = VGroup(
            mtex(r"\frac{\ddot V}{V} = -c^2 R_{00}", font_size=34, color=C.CURVATURE),
            label(r"(sum of the three tidal stretch rates)", font_size=24, color=GREY_A),
            mtex(r"c^2 R_{00} = 4\pi G\Big(\rho + \frac{3p}{c^2}\Big)", font_size=34),
            label(r"(the trace-reversed field equation)", font_size=24, color=GREY_A),
        )
        VGroup(VGroup(why[0], why[1]).arrange(DOWN, buff=0.1), VGroup(why[2], why[3]).arrange(DOWN, buff=0.1)).arrange(
            RIGHT, buff=1.2).next_to(eb, DOWN, buff=0.55)
        with self.voiceover(
            "What does Einstein's equation actually say? Ten coupled nonlinear equations are hard to picture, but there's a "
            "beautiful way to say it in one sentence, due to John Baez and Emory Bunn. <bookmark mark='q'/> Take a small "
            "ball of freely falling test particles, initially at rest relative to each other. The rate at which it begins "
            "to shrink is proportional to its volume, times the energy density at its center, plus the pressure in the x "
            "direction, plus the pressure in the y direction, plus the pressure in the z direction."
        ) as vo:
            vo.wait_until("q")
            self.play(FadeIn(q, lag_ratio=0.3), FadeIn(who), run_time=3)
            self.play(Write(eq), Create(eb[0]))
        with self.voiceover(
            "<bookmark mark='a'/> We've already done the work to see why. The ball's volume responds to the trace of the "
            "tidal tensor, which is c squared R zero zero. <bookmark mark='b'/> And the trace-reversed field equation says "
            "that, for a fluid, c squared R zero zero is four pi G times rho plus three p over c squared. Remarkably, "
            "Baez and Bunn show that this one sentence, applied to every small ball in every freely falling frame, is "
            "equivalent to the whole of Einstein's equation."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(VGroup(why[0], why[1])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(why[2], why[3])))
        self.clear_scene()

    # ------------------------------------------------------------------
    def balls(self):
        d = load("ball")
        vac, mat, vv, vm = d["vac"], d["mat"], d["v_vac"], d["v_mat"]
        n = len(d["ts"])
        last = int(round(0.4 * (n - 1)))
        assert abs(d["ts"][last] - 0.48) < 0.01 and abs(vv[last] - 1) < 0.035 and vm[last] < 0.9
        vl = View3D(center=[-3.6, 0.0, 0], scale=1.15, azimuth=0.5, elevation=0.25)
        vr = View3D(center=[3.6, 0.0, 0], scale=1.15, azimuth=0.5, elevation=0.25)
        k = ValueTracker(0.0)

        def left():
            i = int(round(k.get_value() * (n - 1)))
            return cloud(vl, vac[i], C.CURVATURE)

        def right():
            i = int(round(k.get_value() * (n - 1)))
            return cloud(vr, mat[i], C.MATTER)

        L, R = always_redraw(left), always_redraw(right)
        tl = label(r"empty space, near a planet", font_size=30).move_to([-3.6, 3.1, 0])
        tr = label(r"inside matter (a cloud of dust)", font_size=30).move_to([3.6, 3.1, 0])
        planet = Arc(radius=5.5, start_angle=PI / 2 - 0.35, angle=0.7, color=C.MATTER, stroke_width=6)
        planet.move_to([-3.6, -3.6, 0])
        pl = label(r"planet $\downarrow$", font_size=24, color=C.MATTER).move_to([-1.4, -3.55, 0])

        def readout(view_center, vals, color):
            h = MathTex(r"V/V_0 =", font_size=34, color=color)
            dn = DecimalNumber(1.0, num_decimal_places=2, font_size=34, color=color)
            g = VGroup(h, dn).arrange(RIGHT, buff=0.15).move_to(view_center + DOWN * 2.6)

            def upd(m):
                i = int(round(k.get_value() * (n - 1)))
                m.set_value(vals[i])

            dn.add_updater(upd)
            return g, dn

        rl, dl = readout(vl.center, vv, C.CURVATURE)
        rr, dr = readout(vr.center, vm, C.MATTER)
        sim = note(r"computed: Newtonian free fall of 320 test particles (tidal regime)").to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Let's watch it. <bookmark mark='a'/> On the left, a ball of test particles in empty space, falling toward a "
            "planet below. <bookmark mark='b'/> On the right, a ball inside a uniform cloud of dust. Release both. "
            "<bookmark mark='c'/> In empty space, the energy density is zero, so the volume doesn't change at first. The "
            "ball does change shape: tides stretch it toward the planet and squeeze it sideways, into an egg of almost "
            "exactly the same volume. <bookmark mark='d'/> Inside matter, the ball shrinks, at exactly the rate four pi G rho."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tl), FadeIn(planet), FadeIn(pl))
            self.add(L, rl)
            vo.wait_until("b")
            self.play(FadeIn(tr), FadeIn(sim))
            self.add(R, rr)
            vo.wait_until("c")
            # (to t = 0.48: the vacuum ball's volume is constant to order t^3, V = 1 - t^4/2 + ...)
            self.play(k.animate.set_value(0.25), vl.az.animate.set_value(0.8), vr.az.animate.set_value(0.8),
                      run_time=vo.until("d"), rate_func=linear)
            self.play(k.animate.set_value(0.4), vl.az.animate.set_value(1.1), vr.az.animate.set_value(1.1),
                      run_time=vo.remaining() + 0.5, rate_func=linear)
        for m in (L, R, dl, dr):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def weyl(self):
        top = mtex(r"\text{Riemann}\ (20)", r"=", r"\text{Weyl}\ (10)", r"+", r"\text{Ricci}\ (10)", font_size=46)
        top[0].set_color(C.CURVATURE)
        top[4].set_color(C.MATTER)
        top.move_to(UP * 2.2)
        rows = VGroup(
            VGroup(label(r"Weyl:", font_size=32), label(r"changes shape, keeps volume. Tides, gravitational waves.", font_size=30)),
            VGroup(label(r"Ricci:", font_size=32, color=C.MATTER), label(r"changes volume. Fixed, point by point, by the matter there.", font_size=30)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.3)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(top, DOWN, buff=0.7)
        count = VGroup(
            label(r"10 equations $-$ 4 Bianchi identities $=$ 6 that evolve the geometry;", font_size=30),
            label(r"the remaining freedom is the choice of 4 coordinates (like gauge freedom in electromagnetism).", font_size=28,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.2).next_to(rows, DOWN, buff=0.8)
        with self.voiceover(
            "This splits curvature into two kinds. <bookmark mark='t'/> Riemann's twenty components divide into ten that "
            "make up the Ricci tensor and ten more called the Weyl tensor. <bookmark mark='w'/> Weyl curvature changes the "
            "shape of the ball but not its volume: that's tides, and as we'll see, gravitational waves. "
            "<bookmark mark='r'/> Ricci curvature changes the volume, and Einstein's equation ties it directly to the "
            "matter at that point. The matter only fixes half of the curvature. The other half can travel through empty "
            "space. <bookmark mark='c'/> And of the ten equations, the Bianchi identity makes four automatic, leaving six "
            "that drive the geometry forward in time; the remaining four functions just reflect our freedom to choose "
            "coordinates."
        ) as vo:
            vo.wait_until("t")
            self.play(Write(top))
            vo.wait_until("w")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("r")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(count, lag_ratio=0.3))
        self.clear_scene()

    # ------------------------------------------------------------------
    def cosmos(self):
        d = load("cosmo")
        a, t = d["a"], d["t"]
        age, t_acc, z_acc = float(d["age"]), float(d["t_acc"]), float(d["z_acc"])
        assert abs(age - 13.8) < 0.05 and abs(t_acc - 7.7) < 0.05 and abs(z_acc - 0.63) < 0.01
        fr = mtex(r"\frac{\ddot R}{R}", r"=", r"-\frac{4\pi G}{3}\Big(\rho + \frac{3p}{c^2}\Big)", r"+", r"\frac{\Lambda c^2}{3}",
                  font_size=44)
        fr[0].set_color(C.CURVATURE)
        fr[2].set_color(C.MATTER)
        fr[4].set_color(C.LAMBDA)
        fr.to_edge(UP, buff=0.4)
        frl = label(r"the ball is any region of a uniform universe: Friedmann's acceleration equation", font_size=26,
                    color=GREY_A).next_to(fr, DOWN, buff=0.2)
        ax = Axes(x_range=[0, 20, 5], y_range=[0, 2.0, 0.5], x_length=6.4, y_length=4.0, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": True, "font_size": 22},
                  x_axis_config={"numbers_to_include": [5, 10, 15, 20]},
                  y_axis_config={"numbers_to_include": [0.5, 1.0, 1.5, 2.0]})
        ax.to_edge(LEFT, buff=0.9).shift(DOWN * 0.9)
        xl = label(r"billions of years since the Big Bang", font_size=24).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = label(r"size of the ball (today $= 1$)", font_size=24).next_to(ax.y_axis, UP, buff=0.15)
        ok = t <= 20
        curve = polyline(ax, t[ok], a[ok], color=WHITE, stroke_width=4)
        now = Dot(ax.c2p(age, 1.0), radius=0.08, color=WHITE)
        nowl = label(r"today, 13.8", font_size=24).next_to(now, RIGHT, buff=0.15).shift(DOWN * 0.15)
        a_acc = float(d["a_acc"])
        acc = Dot(ax.c2p(t_acc, a_acc), radius=0.08, color=C.LAMBDA)
        accl = label(r"starts to accelerate: 7.7 billion years", font_size=24, color=C.LAMBDA).next_to(acc, RIGHT, buff=0.15).shift(DOWN * 0.2)
        dec = label(r"matter: decelerating", font_size=24, color=C.MATTER).move_to(ax.c2p(3.5, 1.15))
        tt = ValueTracker(0.5)
        center = np.array([3.9, -0.9, 0])
        rng = np.random.default_rng(2)
        gal = rng.normal(size=(70, 2))
        gal = gal / np.linalg.norm(gal, axis=1, keepdims=True) * np.sqrt(rng.uniform(0, 1, (70, 1)))

        def galaxies():
            s = float(np.interp(tt.get_value(), t, a)) * 1.6
            g = VGroup(Circle(radius=s, color=GREY_B, stroke_width=2).move_to(center))
            g.add(*[Dot(center + s * np.array([x, y, 0]), radius=0.045, color=WHITE) for x, y in gal])
            return g

        gm = always_redraw(galaxies)
        marker = always_redraw(lambda: Dot(ax.c2p(tt.get_value(), float(np.interp(tt.get_value(), t, a))), radius=0.07,
                                           color=YELLOW))
        lam = label(r"vacuum energy has $p = -\rho c^2$: \ $\rho + 3p/c^2 < 0$ \ repels", font_size=26,
                    color=C.LAMBDA).to_edge(DOWN, buff=0.3)
        params = note(r"flat $\Lambda$CDM, Planck 2018: $H_0 = 67.4$, $\Omega_m = 0.315$").next_to(ax, UP, buff=0.5).align_to(ax, LEFT)
        with self.voiceover(
            "Finally, apply the same sentence to the biggest ball there is. <bookmark mark='f'/> In a universe filled "
            "uniformly with matter, any region is a ball of freely falling particles: the galaxies. Its radius obeys this "
            "equation, Friedmann's acceleration equation. Matter and pressure make the expansion slow down. "
            "<bookmark mark='l'/> But the cosmological constant behaves like an energy density with negative pressure, "
            "minus rho c squared, and then rho plus three p is negative: it makes the expansion speed up."
        ) as vo:
            vo.wait_until("f")
            self.play(Write(fr[:3]), FadeIn(frl))
            vo.wait_until("l")
            self.play(Write(fr[3:]), FadeIn(lam))
        with self.voiceover(
            "<bookmark mark='p'/> Here's the size of such a ball over cosmic history, for the measured contents of our "
            "universe. <bookmark mark='d'/> For its first seven or eight billion years, the matter won, and the expansion "
            "decelerated. <bookmark mark='a'/> About seven point seven billion years after the Big Bang, the matter had "
            "thinned out enough for the cosmological constant to take over, and the expansion began to accelerate, as "
            "astronomers discovered in 1998."
        ) as vo:
            vo.wait_until("p")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(params))
            self.add(gm, marker)
            vo.wait_until("d")
            self.play(Create(curve), tt.animate.set_value(t_acc), FadeIn(dec), run_time=3, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(acc), FadeIn(accl))
            self.play(tt.animate.set_value(age), run_time=2.5, rate_func=linear)
            self.play(FadeIn(now), FadeIn(nowl), tt.animate.set_value(19.5), run_time=2.5, rate_func=linear)
        gm.clear_updaters()
        marker.clear_updaters()
        self.clear_scene()
