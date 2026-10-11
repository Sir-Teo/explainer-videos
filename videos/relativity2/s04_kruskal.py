from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity2 import spacetime as st
from videos.relativity2.common import (under, Chart, View3D, clipped, curve3d, label, ladder, load, mtex, note, redraw,
                                       zigzag_curve)
from videos.relativity2.geometry import check_kruskal

INFALLER = C.MATTER


def schw_screen(r, t):
    """Where the Schwarzschild chart of region I sits on screen before the morph."""
    return np.stack([0.4 + (np.asarray(r) - 2) * 1.9, 0.42 * np.asarray(t), 0 * np.asarray(r)], -1)


class Kruskal(VoiceoverScene):
    def construct(self):
        assert check_kruskal() == "ok"
        self.kch = Chart(center=[0, -0.35, 0], scale=1.25, origin=(0, 0), box=(-6.9, 6.9, -3.6, 3.3))
        self.derive()
        self.morph()
        self.regions()
        self.infall()
        self.bridge()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            mtex(r"ds^2", r"=", r"-\Big(1 - \frac{2M}{r}\Big)du\,dv + r^2d\Omega^2,\qquad u \equiv t - r^*", font_size=38),
            mtex(r"U", r"=", r"-e^{-u/4M},\qquad V = e^{v/4M}", font_size=40),
            mtex(r"UV", r"=", r"-e^{r^*/2M} = \Big(1 - \frac{r}{2M}\Big)e^{r/2M}", font_size=40),
            mtex(r"ds^2", r"=", r"-\frac{32M^3}{r}e^{-r/2M}\,dU\,dV + r^2d\Omega^2", font_size=40),
            mtex(r"ds^2", r"=", r"\frac{32M^3}{r}e^{-r/2M}\big(-dT^2 + dX^2\big) + r^2d\Omega^2", font_size=40),
        ]
        whys = [
            note(r"use both null coordinates; but the outgoing one, $u$, runs to $+\infty$ at the horizon"),
            note(r"exponentiate, squeezing infinite ranges into finite ones"),
            note(r"$r$ depends only on the product $UV$; \ $r = 2M \Leftrightarrow UV = 0$"),
            note(r"finite and nonzero at $r = 2M$ (checked symbolically)"),
            note(r"$T = (V + U)/2$, \ $X = (V - U)/2$: \ light moves at $45^\circ$, everywhere"),
        ]
        for r in rows:
            r[0].set_color(C.METRIC)
        rows[1][0].set_color(C.LIGHT)
        rows[2][0].set_color(C.LIGHT)
        x0 = -1.4
        under(rows, whys, x0)
        step = ladder(self, rows, whys, keep=4, top=3.1, x=x0, buff=0.62)
        hist = note(r"Martin Kruskal and George Szekeres, independently, 1960").to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Finkelstein's coordinates see through the horizon, but only for things falling in. To see the whole "
            "spacetime, use both kinds of light rays. <bookmark mark='a'/> With u equal to t minus r star, constant "
            "along outgoing rays, the metric is just minus one minus two M over r, times d u d v. But u runs off to "
            "infinity at the horizon. <bookmark mark='b'/> So squeeze it: define capital U and V as exponentials of u "
            "and v. <bookmark mark='c'/> Their product depends only on r, and vanishes exactly at the horizon."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        with self.voiceover(
            "<bookmark mark='d'/> In U and V, the metric's factor is finite, and nonzero, at r equals two M. "
            "<bookmark mark='e'/> And with T and X, the sum and difference, it's the flat metric of special relativity "
            "times a positive factor. So light travels at forty-five degrees everywhere in this picture. "
            "<bookmark mark='h'/> These are the coordinates Martin Kruskal and George Szekeres found, independently, "
            "in 1960."
        ) as vo:
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            vo.wait_until("h")
            self.play(FadeIn(hist))
        self.clear_scene()

    # ------------------------------------------------------------------
    def morph(self):
        ch = self.kch
        s = ValueTracker(0.0)
        r_vals = [2.05, 2.25, 2.5, 3.0, 3.5, 4.0, 4.6]
        t_vals = [-6, -4, -2, 0, 2, 4, 6]

        def lines():
            sv = s.get_value()
            g = VGroup()
            tt = np.linspace(-26, 26, 500)
            for r0 in r_vals:
                U, V = st.kruskal_exterior(tt, np.full_like(tt, r0))
                T, X = st.TX(U, V)
                P = (1 - sv) * schw_screen(np.full_like(tt, r0), tt) + sv * ch.p(X, T)
                g.add(clipped(P, color=C.METRIC, stroke_width=2))
            rr = np.linspace(2.0002, 4.8, 400)
            for t0 in t_vals:
                U, V = st.kruskal_exterior(np.full_like(rr, t0), rr)
                T, X = st.TX(U, V)
                P = (1 - sv) * schw_screen(rr, np.full_like(rr, t0)) + sv * ch.p(X, T)
                g.add(clipped(P, color=C.PROPER_TIME, stroke_width=2))
            return g

        L = redraw(lines)
        rl = VGroup(*[label(f"${r0:g}M$", font_size=18, color=C.METRIC).move_to(schw_screen(r0, 0) + [0.12, -3.35, 0])
                      for r0 in (2.5, 3.0, 4.0)])
        hdr = label(r"region outside the horizon, in Schwarzschild's $(r, t)$", font_size=26).to_edge(UP, buff=0.3)
        hdr2 = label(r"the same lines, in Kruskal's $(X, T)$", font_size=26).to_edge(UP, buff=0.3)
        leg = VGroup(label(r"constant $r$", font_size=22, color=C.METRIC),
                     label(r"constant $t$", font_size=22, color=C.PROPER_TIME)).arrange(RIGHT, buff=0.5).to_corner(DL, buff=0.25)
        with self.voiceover(
            "Let's see how the familiar picture fits inside this one. <bookmark mark='a'/> Here's the outside of the "
            "black hole in Schwarzschild's coordinates: blue lines of constant r, teal lines of constant t. "
            "<bookmark mark='b'/> Now move every point to its place in Kruskal's coordinates. <bookmark mark='c'/> "
            "Lines of constant r become hyperbolas. Lines of constant t become straight lines through the origin, like "
            "the spokes of a fan. All of Schwarzschild time, from minus infinity to plus infinity, fits inside a wedge, "
            "and the edges of the wedge, where t is infinite, are the lines X equals plus or minus T: the horizon."
        ) as vo:
            vo.wait_until("a")
            self.add(L)
            self.play(FadeIn(hdr), FadeIn(leg), FadeIn(rl))
            vo.wait_until("b")
            self.play(FadeOut(rl), FadeOut(hdr), FadeIn(hdr2))
            vo.wait_until("c")
            self.play(s.animate.set_value(1.0), run_time=6, rate_func=smooth)
        L.clear_updaters()
        self.morphed = VGroup(L, leg, hdr2)

    # ------------------------------------------------------------------
    def regions(self):
        ch = self.kch
        L, leg, hdr2 = self.morphed
        self.play(FadeOut(hdr2))
        Tm = 2.6
        h1 = Line(ch.p(-Tm, -Tm), ch.p(Tm, Tm), color=C.CURVATURE, stroke_width=3.5)
        h2 = Line(ch.p(-Tm, Tm), ch.p(Tm, -Tm), color=C.CURVATURE, stroke_width=3.5)
        xs = np.linspace(-1.6, 1.6, 300)
        top = zigzag_curve(ch.p(xs, np.sqrt(1 + xs**2)))
        bot = zigzag_curve(ch.p(xs, -np.sqrt(1 + xs**2)))
        other = VGroup()
        # mirror images of the exterior grid: region III (X -> -X), and the interior grids (II, IV)
        tt = np.linspace(-26, 26, 500)
        for r0 in [2.05, 2.25, 2.5, 3.0, 3.5, 4.0, 4.6]:
            U, V = st.kruskal_exterior(tt, np.full_like(tt, r0))
            T, X = st.TX(U, V)
            other.add(ch.curve(-X, T, color=C.METRIC, stroke_width=2, opacity=0.55))
        rr = np.linspace(2.0002, 4.8, 400)
        for t0 in [-6, -4, -2, 0, 2, 4, 6]:
            U, V = st.kruskal_exterior(np.full_like(rr, t0), rr)
            T, X = st.TX(U, V)
            other.add(ch.curve(-X, T, color=C.PROPER_TIME, stroke_width=2, opacity=0.55))
        interior = VGroup()
        for r0 in (0.5, 1.0, 1.5, 1.9):
            c0 = st.UV_of_r(r0)  # T^2 - X^2 = U V
            x = np.linspace(-3, 3, 300)
            interior.add(ch.curve(x, np.sqrt(c0 + x * x), color=C.METRIC, stroke_width=2))
            interior.add(ch.curve(x, -np.sqrt(c0 + x * x), color=C.METRIC, stroke_width=2, opacity=0.55))
        for t0 in (-6, -3, 0, 3, 6):
            k = math.tanh(t0 / 4)  # inside: X / T = tanh(t / 4M)
            T = np.linspace(0, 1.6, 50)
            interior.add(ch.curve(k * T, T, color=C.PROPER_TIME, stroke_width=2))
            interior.add(ch.curve(k * T, -T, color=C.PROPER_TIME, stroke_width=2, opacity=0.55))
        labs = VGroup(
            label(r"I: our universe", font_size=24).move_to(ch.p(3.3, 0.45)),
            label(r"II: black hole", font_size=24, color=C.CURVATURE).move_to(ch.p(0, 1.85)),
            label(r"III: another exterior", font_size=24, color=GREY_A).move_to(ch.p(-3.3, 0.45)),
            label(r"IV: white hole", font_size=24, color=GREY_A).move_to(ch.p(0, -1.85)),
        )
        for m in labs:
            m.add_background_rectangle(color=BACKGROUND, opacity=0.8, buff=0.05)
        sing_l = label(r"$r = 0$", font_size=22, color=C.SINGULARITY).move_to(ch.p(1.95, 2.45))
        hor_l = label(r"$r = 2M$", font_size=22, color=C.CURVATURE).move_to(ch.p(2.4, 1.85)).rotate(PI / 4)
        with self.voiceover(
            "And now we can see what lies beyond. <bookmark mark='h'/> The horizon is the pair of diagonal lines, made "
            "of light rays, just as we found. <bookmark mark='i'/> Above them is the inside of the black hole, region "
            "two, where lines of constant r are hyperbolas again, but now horizontal ones, ending at the singularity, r "
            "equals zero, which is also a hyperbola. <bookmark mark='o'/> The equations, solved in full, also contain "
            "two more regions: a mirror-image exterior on the left, and below, a white hole, a region that things can "
            "only leave. This is the maximally extended Schwarzschild spacetime."
        ) as vo:
            vo.wait_until("h")
            self.play(Create(h1), Create(h2), FadeIn(hor_l))
            vo.wait_until("i")
            self.play(FadeIn(interior[::2]), Create(top), FadeIn(sing_l), FadeIn(labs[0]), FadeIn(labs[1]), run_time=2)
            vo.wait_until("o")
            self.play(FadeIn(other), FadeIn(interior[1::2]), Create(bot), FadeIn(labs[2]), FadeIn(labs[3]), run_time=2)
        self.diagram = VGroup(L, leg, h1, h2, top, bot, other, interior, labs, sing_l, hor_l)

    # ------------------------------------------------------------------
    def infall(self):
        ch = self.kch
        d = load("infall")
        U, V = d["U"].copy(), d["V"].copy()
        # the same fall, begun at a different Schwarzschild time (a boost in Kruskal coordinates), so it crosses the
        # horizon near the middle of the picture
        k_h = int(d["i_h"])
        f = 1.35 / V[k_h]
        U, V = U / f, V * f
        T, X = st.TX(U, V)
        ok = (T * T - X * X) < 0.999
        wl = ch.curve(X[ok], T[ok], color=INFALLER, stroke_width=5)
        j = int(np.argmin(np.abs(st.r_of_UV(U * V) - 1.2)))
        tip = ch.p(X[j], T[j])
        cone = VGroup(Polygon(tip, ch.p(X[j] - 1.2, T[j] + 1.2), ch.p(X[j] + 1.2, T[j] + 1.2), stroke_width=0,
                              fill_color=C.LIGHT, fill_opacity=0.25),
                      Line(tip, ch.p(X[j] - 1.2, T[j] + 1.2), color=C.LIGHT, stroke_width=2.5),
                      Line(tip, ch.p(X[j] + 1.2, T[j] + 1.2), color=C.LIGHT, stroke_width=2.5),
                      Dot(tip, radius=0.08, color=INFALLER))
        cones = VGroup()
        for (x0, t0) in ((3.4, -1.2), (2.6, 0.5), (-3.0, 0.0), (0.0, 1.0), (0.0, -1.1)):
            p = ch.p(x0, t0)
            cones.add(VGroup(Polygon(p, ch.p(x0 - 0.3, t0 + 0.3), ch.p(x0 + 0.3, t0 + 0.3), stroke_width=0,
                                     fill_color=C.LIGHT, fill_opacity=0.35),
                             Line(p, ch.p(x0 - 0.3, t0 + 0.3), color=C.LIGHT, stroke_width=2),
                             Line(p, ch.p(x0 + 0.3, t0 + 0.3), color=C.LIGHT, stroke_width=2)))
        quote = VGroup(label(r"Inside, $r$ is a time:", font_size=28, color=C.CURVATURE),
                       label(r"the singularity is not a place,", font_size=26),
                       label(r"but a moment in your future.", font_size=26)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        quote.to_corner(UR, buff=0.3).shift(LEFT * 0.1)
        quote.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.1)
        with self.voiceover(
            "<bookmark mark='c'/> Light cones are forty-five degrees everywhere, so causality is easy to read. "
            "<bookmark mark='w'/> Here's our astronaut's worldline: it crosses the horizon smoothly, and ends on the "
            "singularity. <bookmark mark='k'/> Look at their light cone inside. Every direction in it hits the "
            "singularity. Inside the black hole, the lines of constant r run sideways: r has become a time coordinate. "
            "The singularity isn't a place you could steer around. It's a moment in your future, as unavoidable as "
            "next Tuesday."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeIn(cones, lag_ratio=0.2))
            vo.wait_until("w")
            self.play(Create(wl), run_time=2)
            vo.wait_until("k")
            self.play(FadeIn(cone), FadeOut(cones))
            self.play(FadeIn(quote))
        self.clear_scene()

    # ------------------------------------------------------------------
    def bridge(self):
        b = load("bridge")
        Ts, R, Z = b["T"], b["r"], b["z"]
        ch = Chart(center=[-4.0, -0.3, 0], scale=0.85, origin=(0, 0), box=(-6.9, -1.0, -3.0, 2.6))
        Tm = 2.3
        h = VGroup(Line(ch.p(-Tm, -Tm), ch.p(Tm, Tm), color=C.CURVATURE, stroke_width=2.5),
                   Line(ch.p(-Tm, Tm), ch.p(Tm, -Tm), color=C.CURVATURE, stroke_width=2.5))
        xs = np.linspace(-1.9, 1.9, 300)
        sing = VGroup(zigzag_curve(ch.p(xs, np.sqrt(1 + xs**2)), amp=0.04),
                      zigzag_curve(ch.p(xs, -np.sqrt(1 + xs**2)), amp=0.04))
        Tt = ValueTracker(0.0)

        def slice_line():
            T = Tt.get_value()
            return Line(ch.p(-2.5, T), ch.p(2.5, T), color=C.METRIC, stroke_width=4)

        SL = redraw(slice_line)
        view = View3D(center=[3.1, -0.45, 0], scale=0.44, azimuth=0.3, elevation=0.35)

        def surface():
            T = abs(Tt.get_value())
            i = int(np.clip(np.searchsorted(Ts, T), 0, len(Ts) - 1))
            keep = R[i] <= 6.0
            r, z = R[i][keep], Z[i][keep]
            rho = np.concatenate([r[::-1], r])
            zz = np.concatenate([-z[::-1], z])
            g = VGroup()
            a = np.linspace(0, 2 * np.pi, 90)
            for kk in np.linspace(0, len(rho) - 1, 15).round().astype(int):
                P = np.stack([rho[kk] * np.cos(a), rho[kk] * np.sin(a), np.full_like(a, zz[kk])], 1)
                g.add(curve3d(view, P, color=C.METRIC, stroke_width=1.6, sphere_r=None))
            for ang in np.linspace(0, 2 * np.pi, 20, endpoint=False):
                P = np.stack([rho * math.cos(ang), rho * math.sin(ang), zz], 1)
                g.add(curve3d(view, P, color=C.METRIC, stroke_width=1.2, sphere_r=None))
            th = np.stack([r[0] * np.cos(a), r[0] * np.sin(a), 0 * a], 1)
            g.add(curve3d(view, th, color=C.CURVATURE, stroke_width=3.5, sphere_r=None))
            return g

        S = redraw(surface)
        rd = VGroup(label(r"throat radius", font_size=24, color=C.CURVATURE),
                    DecimalNumber(2.0, num_decimal_places=2, font_size=28, color=C.CURVATURE),
                    label(r"$M$", font_size=24)).arrange(RIGHT, buff=0.1).move_to([-4.0, -3.3, 0])
        rd[1].add_updater(lambda m: m.set_value(float(np.interp(abs(Tt.get_value()), Ts, b["rmin"]))))
        hdr = label(r"space at one Kruskal time $T$: \ an Einstein--Rosen bridge", font_size=28).to_edge(UP, buff=0.3)
        cap = note(r"exact embedding of the slice $T = \mathrm{const}$ (radius $r$, out to $6M$)").to_corner(DR, buff=0.2)
        fw = VGroup(label(r"Fuller \& Wheeler (1962): it pinches off", font_size=24, color=GREY_A),
                    label(r"before even light can cross", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.08)
        fw.move_to([-4.0, 2.75, 0])
        ray_x = np.linspace(1.3, -0.2, 50)
        ray = ch.curve(ray_x, 0.2 + (1.3 - ray_x), color=C.LIGHT, stroke_width=3)
        with self.voiceover(
            "This picture also contains a wormhole. <bookmark mark='a'/> Take a slice of constant Kruskal time T. At T "
            "equals zero, it runs from the other exterior on the left, through r equals two M, to ours on the right. "
            "<bookmark mark='b'/> Its geometry, embedded as a surface, is two copies of Flamm's funnel from part one, "
            "joined at the throat: the Einstein–Rosen bridge, a tunnel between two universes. <bookmark mark='c'/> But "
            "it isn't static. Move the slice up in T, and the throat shrinks, and pinches off, at the singularity. "
            "<bookmark mark='d'/> Running backward, it was born from the white hole's singularity. It closes too fast "
            "for anything, even light, to get through: a light ray sent across ends on the singularity."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(h), FadeIn(sing), FadeIn(hdr))
            self.add(SL)
            vo.wait_until("b")
            self.add(S)
            self.play(FadeIn(rd), FadeIn(cap))
            vo.wait_until("c")
            self.play(Tt.animate.set_value(0.98), view.az.animate.set_value(0.9), run_time=4, rate_func=smooth)
            vo.wait_until("d")
            self.play(Tt.animate.set_value(-0.98), view.az.animate.set_value(1.6), run_time=4, rate_func=smooth)
            self.play(Tt.animate.set_value(0.0), FadeIn(fw), run_time=2)
            self.play(Create(ray))
        for m in (SL, S, rd[1]):
            m.clear_updaters()
        with self.voiceover(
            "Is any of this real? The extra regions are there because Schwarzschild's solution describes a black hole "
            "that has existed forever. Real black holes form from collapsing stars, and to see what that changes, we "
            "need one more way of drawing spacetime."
        ):
            pass
        self.clear_scene()
