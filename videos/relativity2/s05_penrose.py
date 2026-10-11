from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity2 import spacetime as st
from videos.relativity2.common import (Chart, clipped, label, ladder, load, mtex, note, redraw, under, zigzag,
                                       zigzag_curve)
from videos.relativity2.geometry import check_penrose

INFALLER = C.MATTER
PI = math.pi


class Penrose(VoiceoverScene):
    def construct(self):
        assert check_penrose() == "ok"
        self.idea()
        self.minkowski()
        self.schwarzschild()
        self.collapse()

    # ------------------------------------------------------------------
    def idea(self):
        rows = [
            mtex(r"ds^2", r"=", r"-dt^2 + dr^2 + r^2d\Omega^2 = -du\,dv + r^2d\Omega^2", font_size=40),
            mtex(r"u", r"=", r"\tan\tilde u,\qquad v = \tan\tilde v,\qquad \tilde u, \tilde v \in \big(-\tfrac{\pi}{2}, \tfrac{\pi}{2}\big)",
                 font_size=40),
            mtex(r"ds^2", r"=", r"\frac{1}{\cos^2\tilde u\,\cos^2\tilde v}\Big(-d\tilde u\,d\tilde v + \tfrac14\sin^2(\tilde v - \tilde u)\,d\Omega^2\Big)",
                 font_size=40),
            mtex(r"d\tilde s^2", r"=", r"-d\tilde u\,d\tilde v + \tfrac14\sin^2(\tilde v - \tilde u)\,d\Omega^2", font_size=40),
        ]
        whys = [
            note(r"flat spacetime, in null coordinates $u = t - r$, \ $v = t + r$"),
            note(r"squeeze each infinite range into a finite one"),
            note(r"$du = d\tilde u / \cos^2\tilde u$ (checked symbolically)"),
            note(r"drop the overall factor: angles, and so light cones, are unchanged; infinity is now a finite place"),
        ]
        rows[3][0].set_color(C.METRIC)
        under(rows, whys, -1.6)
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-1.6, buff=0.6)
        hist = note(r"Roger Penrose (1963--64); Brandon Carter (1966)").to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Kruskal's picture still runs off to infinity in every direction. Roger Penrose found a way to fit all of "
            "spacetime, infinity included, on a finite page. <bookmark mark='a'/> Start with flat spacetime, in the "
            "null coordinates u and v. <bookmark mark='b'/> Squeeze each of them with an arctangent, so their infinite "
            "ranges become finite. <bookmark mark='c'/> The metric picks up a factor that blows up at the edges. "
            "<bookmark mark='d'/> Now the trick: throw that factor away. Multiplying a metric by a positive function "
            "changes lengths, but not angles, so light cones keep their shape, and the causal structure, who can "
            "signal whom, is exactly preserved. What's left is a finite picture of an infinite spacetime."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(FadeIn(hist))
        self.clear_scene()

    # ------------------------------------------------------------------
    def minkowski(self):
        s = ValueTracker(0.0)
        flat = Chart(center=[-4.6, -2.2, 0], scale=0.55, origin=(0, 0))
        pen = Chart(center=[-2.4, -0.25, 0], scale=1.15, origin=(0, 0))
        t_vals = np.arange(-8, 9, 1.0)
        r_vals = np.arange(1, 13, 1.0)

        def scr(t, r):
            T, R = st.penrose_minkowski(t, r)
            return (1 - s.get_value()) * flat.p(r, t) + s.get_value() * pen.p(R, T)

        def grid():
            g = VGroup()
            rr = np.linspace(0, 400, 1500)
            rr = np.concatenate([np.linspace(0, 20, 400), np.geomspace(20, 4000, 300)])
            for t0 in t_vals:
                g.add(clipped(scr(np.full_like(rr, t0), rr), color=C.PROPER_TIME, stroke_width=1.5, opacity=0.7))
            tt = np.concatenate([-np.geomspace(4000, 20, 300), np.linspace(-20, 20, 400), np.geomspace(20, 4000, 300)])
            for r0 in r_vals:
                g.add(clipped(scr(tt, np.full_like(tt, r0)), color=C.METRIC, stroke_width=1.5, opacity=0.7))
            g.add(clipped(scr(tt, np.zeros_like(tt)), color=GREY_A, stroke_width=3))
            return g

        G = redraw(grid)
        hdr = label(r"flat spacetime: $t$ up, $r$ across (one line per unit of $t$ and of $r$)", font_size=26)
        hdr.to_edge(UP, buff=0.3)
        edges = VGroup(
            Line(pen.p(0, -PI), pen.p(PI, 0), color=C.LIGHT, stroke_width=3),
            Line(pen.p(PI, 0), pen.p(0, PI), color=C.LIGHT, stroke_width=3),
        )
        labs = VGroup(
            mtex(r"i^+", font_size=36).next_to(pen.p(0, PI), UP, buff=0.08),
            mtex(r"i^-", font_size=36).next_to(pen.p(0, -PI), DOWN, buff=0.08),
            mtex(r"i^0", font_size=36).next_to(pen.p(PI, 0), RIGHT, buff=0.1),
            mtex(r"\mathcal{I}^+", font_size=36, color=C.LIGHT).move_to(pen.p(PI / 2 + 0.38, PI / 2 + 0.38)),
            mtex(r"\mathcal{I}^-", font_size=36, color=C.LIGHT).move_to(pen.p(PI / 2 + 0.38, -PI / 2 - 0.38)),
        )
        expl = VGroup(
            label(r"$i^+$: where every inertial observer ends up", font_size=24),
            label(r"$i^-$: where they all came from", font_size=24),
            label(r"$i^0$: spatial infinity", font_size=24),
            label(r"$\mathcal{I}^+$ (``scri plus''): where light rays end", font_size=24, color=C.LIGHT),
            label(r"$\mathcal{I}^-$: where they come from", font_size=24, color=C.LIGHT),
            label(r"light still moves at $45^\circ$", font_size=24, color=C.LIGHT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.9, 0.0, 0])
        k = ValueTracker(0.0)

        def movers():
            g = VGroup()
            T, R = st.penrose_minkowski(np.array([math.tan(PI / 2 * (2 * k.get_value() - 1) * 0.999)]), np.array([3.0]))
            g.add(Dot(pen.p(R[0], T[0]), radius=0.08, color=INFALLER))
            return g

        tt = np.tan(np.linspace(-PI / 2 * 0.999, PI / 2 * 0.999, 400))
        T, R = st.penrose_minkowski(tt, np.full_like(tt, 1.0))
        obs = pen.curve(R, T, color=INFALLER, stroke_width=4)
        ray = VGroup(Line(pen.p(0.8, -PI + 0.8), pen.p(0, -PI + 1.6), color=C.LIGHT, stroke_width=3),
                     Line(pen.p(0, -PI + 1.6), pen.p(PI - 0.8, 0.8), color=C.LIGHT, stroke_width=3))
        ray0 = Line(pen.p(PI - 0.8, -0.8), pen.p(0.8, -PI + 0.8), color=C.LIGHT, stroke_width=3)
        with self.voiceover(
            "Here's what that does to flat spacetime. <bookmark mark='a'/> A grid of lines, one per unit of time and of "
            "distance, stretching off forever. <bookmark mark='b'/> Apply the squeeze. <bookmark mark='c'/> The whole "
            "infinite half-plane folds into a triangle. Every line of constant r runs from one point at the bottom to "
            "one point at the top: that's where every inertial observer comes from, and goes to. Lines of constant t "
            "all meet at the far corner, spatial infinity. <bookmark mark='d'/> And the two diagonal edges are where "
            "light rays come from and go to, called scri minus and scri plus. Light still moves at forty-five degrees, "
            "so you can read off at a glance what can influence what."
        ) as vo:
            vo.wait_until("a")
            self.add(G)
            self.play(FadeIn(hdr))
            vo.wait_until("b")
            self.play(FadeOut(hdr))
            vo.wait_until("c")
            self.play(s.animate.set_value(1.0), run_time=6, rate_func=smooth)
            G.clear_updaters()
            self.play(FadeIn(labs[:3]), FadeIn(expl[:3], lag_ratio=0.2), Create(obs))
            vo.wait_until("d")
            self.play(Create(edges), FadeIn(labs[3:]), FadeIn(expl[3:], lag_ratio=0.2))
            self.play(Create(ray0), run_time=0.8)
            self.play(Create(ray), run_time=1.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def schwarzschild(self):
        kch = Chart(center=[0, -0.35, 0], scale=1.25, origin=(0, 0), box=(-6.9, 6.9, -3.6, 3.3))
        pch = Chart(center=[0, -0.25, 0], scale=1.6, origin=(0, 0))
        s = ValueTracker(0.0)

        def place(U, V):
            T, X = st.TX(U, V)
            Tp, Xp = st.penrose(U, V)
            return (1 - s.get_value()) * kch.p(X, T) + s.get_value() * pch.p(Xp, Tp)

        tt = np.concatenate([-np.geomspace(300, 8, 200), np.linspace(-8, 8, 200), np.geomspace(8, 300, 200)])
        rr = np.concatenate([np.linspace(2.0002, 6, 300), np.geomspace(6, 500, 200)])
        ext_r = [2.2, 2.6, 3.0, 4.0, 6.0, 10.0]
        ext_t = [-8, -4, -2, 0, 2, 4, 8]

        def grid():
            g = VGroup()
            for sx in (1, -1):  # region I and its mirror image X -> -X, region III: (U, V) -> (V, U)
                for r0 in ext_r:
                    U, V = st.kruskal_exterior(tt, np.full_like(tt, r0))
                    g.add(clipped(place(U if sx > 0 else V, V if sx > 0 else U), color=C.METRIC, stroke_width=1.8))
                for t0 in ext_t:
                    U, V = st.kruskal_exterior(np.full_like(rr, t0), rr)
                    g.add(clipped(place(U if sx > 0 else V, V if sx > 0 else U), color=C.PROPER_TIME, stroke_width=1.8))
            for sy in (1, -1):  # region II (black hole) and IV (white hole)
                rin = np.linspace(1e-3, 1.9998, 300)
                for r0 in (0.6, 1.2, 1.7):
                    c0 = st.UV_of_r(r0)
                    U = np.concatenate([np.geomspace(1e-4, 1, 150), np.geomspace(1, 1e4, 150)]) * math.sqrt(c0)
                    V = c0 / U
                    g.add(clipped(place(sy * U, sy * V), color=C.METRIC, stroke_width=1.8))
                for t0 in (-4, 0, 4):
                    U, V = st.kruskal_interior(np.full_like(rin, t0), rin)
                    g.add(clipped(place(sy * U, sy * V), color=C.PROPER_TIME, stroke_width=1.8))
            return g

        def frame_lines():
            g = VGroup()
            big = np.geomspace(1e-4, 1e4, 300)
            g.add(clipped(place(0 * big, big), color=C.CURVATURE, stroke_width=4))
            g.add(clipped(place(-big, 0 * big), color=C.CURVATURE, stroke_width=4))
            g.add(clipped(place(0 * big, -big), color=C.CURVATURE, stroke_width=4))
            g.add(clipped(place(big, 0 * big), color=C.CURVATURE, stroke_width=4))
            for sy in (1, -1):
                U = np.concatenate([np.geomspace(1e-4, 1, 150), np.geomspace(1, 1e4, 150)])
                P = place(sy * U, sy / U)
                P = P[(np.abs(P[:, 0]) < 6.9) & (np.abs(P[:, 1]) < 3.6)]
                if len(P) > 3:
                    g.add(zigzag_curve(P, amp=0.04))
            return g

        G, F = redraw(grid), redraw(frame_lines)
        hdr = label(r"Kruskal's diagram $\rightarrow$ squeeze $U$ and $V$ with arctangents", font_size=26).to_edge(UP, buff=0.25)
        with self.voiceover(
            "Now do the same to the black hole. <bookmark mark='a'/> Start from Kruskal's diagram, and squeeze U and V "
            "with arctangents. <bookmark mark='b'/> The exterior becomes a diamond, the black hole a triangle on top, "
            "and the singularity, which was a hyperbola, becomes a straight horizontal line: r equals zero is where "
            "the arctangents of U and V add up to pi over two."
        ) as vo:
            self.add(G, F)
            vo.wait_until("a")
            self.play(FadeIn(hdr))
            vo.wait_until("b")
            self.play(s.animate.set_value(1.0), FadeOut(hdr), run_time=5, rate_func=smooth)
        G.clear_updaters()
        F.clear_updaters()
        labs = VGroup(
            mtex(r"i^+", font_size=30).next_to(pch.p(PI / 2, PI / 2), UR, buff=0.04),
            mtex(r"i^0", font_size=30).next_to(pch.p(PI, 0), RIGHT, buff=0.08),
            mtex(r"i^-", font_size=30).next_to(pch.p(PI / 2, -PI / 2), DR, buff=0.04),
            mtex(r"\mathcal{I}^+", font_size=30, color=C.LIGHT).move_to(pch.p(3 * PI / 4 + 0.3, PI / 4 + 0.3)),
            mtex(r"\mathcal{I}^-", font_size=30, color=C.LIGHT).move_to(pch.p(3 * PI / 4 + 0.3, -PI / 4 - 0.3)),
            label(r"I", font_size=30).move_to(pch.p(PI / 2, 0.0)),
            label(r"II", font_size=30, color=C.CURVATURE).move_to(pch.p(0, PI / 2 - 0.45)),
            label(r"III", font_size=30, color=GREY_A).move_to(pch.p(-PI / 2, 0.0)),
            label(r"IV", font_size=30, color=GREY_A).move_to(pch.p(0, -PI / 2 + 0.45)),
        )
        for m in labs[5:]:
            m.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.05)
        scri = VGroup(Line(pch.p(PI / 2, PI / 2), pch.p(PI, 0), color=C.LIGHT, stroke_width=3),
                      Line(pch.p(PI, 0), pch.p(PI / 2, -PI / 2), color=C.LIGHT, stroke_width=3),
                      Line(pch.p(-PI / 2, PI / 2), pch.p(-PI, 0), color=C.LIGHT, stroke_width=3, stroke_opacity=0.5),
                      Line(pch.p(-PI, 0), pch.p(-PI / 2, -PI / 2), color=C.LIGHT, stroke_width=3, stroke_opacity=0.5))
        d = load("infall")
        U, V = d["U"], d["V"]
        k_h = int(d["i_h"])
        f = 1.35 / V[k_h]
        U, V = U / f, V * f
        Tp, Xp = st.penrose(U, V)
        ok = U * V < 0.9995
        wl = pch.curve(Xp[ok], Tp[ok], color=INFALLER, stroke_width=5)
        esc = Line(pch.p(1.9, -0.2), pch.p(1.9 + 1.0, -0.2 + 1.0), color=C.LIGHT, stroke_width=3)
        trap = Line(pch.p(0.6, 0.85), pch.p(0.6 + 0.35, 0.85 + 0.35), color=C.LIGHT, stroke_width=3)
        with self.voiceover(
            "<bookmark mark='a'/> This is the Penrose diagram of the Schwarzschild black hole. Our universe is the "
            "diamond on the right, with its own infinities: scri plus, where outgoing light ends up, and future and "
            "past timelike infinity. <bookmark mark='b'/> Here's the astronaut. <bookmark mark='c'/> And now the "
            "definition of a black hole becomes visual: it's the region from which no light ray can reach scri plus. "
            "<bookmark mark='d'/> Light from here gets out. Light from inside the horizon can only go up, into the "
            "singularity."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(scri), FadeIn(labs, lag_ratio=0.1), run_time=2)
            vo.wait_until("b")
            self.play(Create(wl), run_time=2)
            vo.wait_until("d")
            self.play(Create(esc))
            self.play(Create(trap))
        self.clear_scene()

    # ------------------------------------------------------------------
    def collapse(self):
        # Left: exact exterior (Kruskal) of a star that sits at r = 5M and then collapses.  Right: the standard
        # (schematic) Penrose diagram of gravitational collapse.
        c = load("collapse")
        U, V = c["U"], c["V"]
        kch = Chart(center=[-4.6, -1.3, 0], scale=0.78, origin=(0, 0), box=(-6.9, -0.5, -3.6, 2.7))
        T, X = st.TX(U, V)
        ok = U * V < 0.999
        surf = kch.curve(X[ok], T[ok], color=C.MATTER, stroke_width=5)
        # shade the star: everything to the left of its surface
        # shade the star: the region to the left of its surface, inside the panel
        vis = ok & (kch.p(X, T)[:, 1] > -3.6) & (kch.p(X, T)[:, 0] < -0.5)
        Ps = kch.p(X[vis], T[vis])
        x_left = -6.9
        poly_pts = [np.array([x_left, Ps[0, 1], 0])] + list(Ps) + [np.array([x_left, Ps[-1, 1], 0])]
        star = Polygon(*poly_pts, stroke_width=0, fill_color=C.MATTER, fill_opacity=0.18)
        hz = kch.curve(np.linspace(float(X[np.argmin(np.abs(U))]), 2.9, 50), np.linspace(float(X[np.argmin(np.abs(U))]), 2.9, 50),
                       color=C.CURVATURE, stroke_width=4)
        xs = np.linspace(float(X[ok][-1]), 2.6, 200)
        sing = zigzag_curve(kch.p(xs, np.sqrt(1 + xs**2)), amp=0.04)
        kl = VGroup(label(r"the star's surface (computed)", font_size=22, color=C.MATTER),
                    label(r"exact exterior, Kruskal coordinates", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.08)
        kl.to_corner(UL, buff=0.25)
        st_l = label(r"star", font_size=26, color=C.MATTER).move_to(kch.p(-1.2, -0.6))
        hz_l = label(r"horizon", font_size=22, color=C.CURVATURE).move_to(kch.p(2.6, 1.9))
        # schematic Penrose diagram of collapse
        o = np.array([1.2, -3.2, 0])
        sc = 1.0
        y_s = 0.55 * PI

        def P(x, y):
            return o + sc * np.array([x, y + PI, 0]) * 1.0

        im = P(0, -PI)
        i0 = P(PI, 0)
        ip = P(PI - y_s, y_s)
        center = Line(im, P(0, y_s), color=GREY_A, stroke_width=3)
        scri_m = Line(im, i0, color=C.LIGHT, stroke_width=3)
        scri_p = Line(i0, ip, color=C.LIGHT, stroke_width=3)
        sing2 = zigzag(P(0, y_s), ip)
        hor = Line(P(0, 2 * y_s - PI), ip, color=C.CURVATURE, stroke_width=4)
        # star surface: from i^- curving up to meet the singularity inside the horizon
        tt = np.linspace(0, 1, 100)
        sx = 0.9 * np.sin(PI * tt * 0.95) * (1 - 0.55 * tt) + 0.05 * tt
        sy = -PI + tt * (y_s + PI)
        surf2 = VMobject(stroke_color=C.MATTER, stroke_width=5).set_points_smoothly([P(x, y) for x, y in zip(sx, sy)])
        fill2 = Polygon(*[P(x, y) for x, y in zip(sx, sy)], P(0, y_s), stroke_width=0, fill_color=C.MATTER,
                        fill_opacity=0.18)
        labs2 = VGroup(
            mtex(r"i^-", font_size=28).next_to(im, DOWN, buff=0.06),
            mtex(r"i^0", font_size=28).next_to(i0, RIGHT, buff=0.06),
            mtex(r"i^+", font_size=28).next_to(ip, UR, buff=0.04),
            mtex(r"\mathcal{I}^+", font_size=28, color=C.LIGHT).next_to(Line(i0, ip).get_center(), UR, buff=0.05),
            mtex(r"\mathcal{I}^-", font_size=28, color=C.LIGHT).next_to(Line(im, i0).get_center(), DR, buff=0.05),
            label(r"$r = 0$ (center)", font_size=20, color=GREY_A).next_to(center, LEFT, buff=0.08).shift(DOWN * 0.8),
            label(r"event horizon", font_size=22, color=C.CURVATURE).next_to(hor.get_center(), RIGHT, buff=0.15).shift(DOWN * 0.15),
        )
        sch = note(r"schematic: Penrose diagram of a collapsing star").next_to(P(PI / 2, -PI), DOWN, buff=0.35)
        with self.voiceover(
            "But real black holes weren't always there: they form when a star collapses. <bookmark mark='a'/> Here's a "
            "star that sits at r equals five M and then collapses. Outside its surface, by Birkhoff's theorem, the "
            "geometry is exactly Schwarzschild's, so this part of the picture is exact. Inside is the star itself, not "
            "empty space. <bookmark mark='b'/> So the left half of Kruskal's diagram, with the white hole, the other "
            "universe and the wormhole, is simply covered up by the star, and never exists. <bookmark mark='c'/> The "
            "standard Penrose diagram of a collapse looks like this: the star's surface falls through the horizon and "
            "meets the singularity, and outside, everything is as before."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(kl), Create(surf), run_time=2)
            self.play(Create(hz), Create(sing), FadeIn(hz_l))
            vo.wait_until("b")
            self.play(FadeIn(star), FadeIn(st_l))
            vo.wait_until("c")
            self.play(Create(center), Create(scri_m), Create(scri_p), FadeIn(sch))
            self.play(FadeIn(fill2), Create(surf2), Create(sing2), FadeIn(labs2[:6]), run_time=2)
        with self.voiceover(
            "<bookmark mark='h'/> And look at where the event horizon is. It's the boundary of the region that can "
            "never send light to scri plus, and it starts at the center of the star, before the surface has reached "
            "r equals two M: a horizon grows outward from the center, through matter that hasn't yet noticed anything. "
            "<bookmark mark='t'/> To know where the event horizon is today, you need to know the entire future. "
            "Nothing local marks it."
        ) as vo:
            vo.wait_until("h")
            self.play(Create(hor), FadeIn(labs2[6]), run_time=2)
        with self.voiceover(
            "That leaves the singularity. Every picture so far has been perfectly spherical. Maybe, in a real, lumpy "
            "collapse, the matter would miss the center and bounce back out? For decades, many physicists thought so."
        ):
            pass
        self.clear_scene()
