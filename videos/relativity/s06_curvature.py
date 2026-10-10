from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity.common import (Globe, View3D, arrow3d, curve3d, great_arc, label, latitude, load, mtex,
                                      note, part_card, sphere_points, stack)
from videos.relativity.geometry import polar_plane, same, sphere

OCTANT_AZ = -3 * math.pi / 4  # the azimuth that turns the octant x, y, z > 0 toward the viewer


def small_circle(p, eps, n=48):
    """Points at angular distance eps around the unit vector p, on the unit sphere."""
    p = np.asarray(p, float)
    a = np.cross(p, [0, 0, 1]) if abs(p[2]) < 0.99 else np.cross(p, [1, 0, 0])
    a /= np.linalg.norm(a)
    b = np.cross(p, a)
    t = np.linspace(0, 2 * np.pi, n)[:, None]
    return math.cos(eps) * p + math.sin(eps) * (np.cos(t) * a + np.sin(t) * b)


def right_angle_mark(view, p, u, v, s=0.16, color=WHITE):
    """A small square corner at p between tangent directions u and v (3D, on the unit sphere)."""
    pts = np.array([p + s * u, p + s * u + s * v, p + s * v])
    pts /= np.linalg.norm(pts, axis=1, keepdims=True)
    return curve3d(view, pts, color=color, stroke_width=3.5)


class IntrinsicCurvature(VoiceoverScene):
    def construct(self):
        S, (th, ph, R) = sphere()
        assert same(S.g[1, 1], R**2 * __import__("sympy").sin(th) ** 2)
        P, _ = polar_plane()
        assert P.scalar == 0
        self.card()
        self.ant()
        self.metrics()
        self.tissot()
        self.triangle()
        self.transport()

    def card(self):
        c = part_card(2, r"The mathematics of curvature", r"measured from the inside")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def ant(self):
        view = View3D(center=[-3.3, -0.4, 0], scale=2.5, azimuth=-0.6, elevation=0.45)
        globe = Globe(view)
        title = label(r"Gauss's \emph{Theorema Egregium} (1827)", font_size=36).to_corner(UL, buff=0.45)
        # the ant walks a wiggly path on the front of the sphere
        s = np.linspace(0, 1, 300)
        front = -np.pi / 2 + 0.45  # the longitude facing the viewer while the globe turns from -0.6 to -0.3
        th_path = 1.25 + 0.38 * np.sin(3 * np.pi * s) - 0.25 * s
        ph_path = front - 0.9 + 1.8 * s
        path = sphere_points(th_path, ph_path)
        k = ValueTracker(0.0)

        def ant():
            i = int(k.get_value() * (len(path) - 1))
            return Dot(view.point(path[i]), radius=0.07, color=C.VECTOR)

        trail = always_redraw(lambda: curve3d(view, path[: max(2, int(k.get_value() * (len(path) - 1)) + 1)],
                                              color=C.VECTOR, stroke_width=3))
        dot = always_redraw(ant)
        claim = VGroup(
            label(r"Curvature can be measured", font_size=32),
            label(r"by someone who never leaves the surface:", font_size=32),
            label(r"only lengths and angles \emph{within} it.", font_size=32, color=C.METRIC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.4, 0.9, 0])
        inside = label(r"Spacetime: we live inside it too.", font_size=32, color=C.CURVATURE)
        inside.next_to(claim, DOWN, buff=0.6).align_to(claim, LEFT)
        with self.voiceover(
            "To describe curved spacetime, we need a way to talk about curvature that doesn't rely on stepping outside. "
            "For surfaces, Carl Friedrich Gauss found one in 1827. <bookmark mark='a'/> Picture an ant on a sphere. It "
            "can't leave the surface, and it can't see the third dimension. All it can do is measure distances and "
            "angles along the surface. <bookmark mark='c'/> Gauss proved that this is enough: the curvature of a surface "
            "is determined entirely by measurements made inside it. He was so pleased that he called it the remarkable "
            "theorem."
        ) as vo:
            self.play(FadeIn(globe), FadeIn(title))
            vo.wait_until("a")
            self.add(trail, dot)
            self.play(k.animate.set_value(1.0), view.az.animate.set_value(-0.3), run_time=vo.until("c"), rate_func=linear)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in claim], lag_ratio=0.3), run_time=2)
        with self.voiceover(
            "Spacetime is the same situation, one dimension up, and with time thrown in. <bookmark mark='i'/> We live "
            "inside it. There's no outside to look from. So everything we build from now on will be built from "
            "measurements made within."
        ) as vo:
            vo.wait_until("i")
            self.play(FadeIn(inside, shift=UP * 0.15))
        for m in (trail, dot, globe.gridlines):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def metrics(self):
        head = label(r"The metric: lengths from coordinates", font_size=40).to_edge(UP, buff=0.45)
        gen = mtex(r"ds^2", r"=", r"g_{ij}(x)", r"\,dx^i\,dx^j", font_size=52)
        gen[2].set_color(C.METRIC)
        gen.next_to(head, DOWN, buff=0.5)
        rows = VGroup(
            mtex(r"\text{plane, Cartesian:}", r"\quad ds^2", r"=", r"dx^2 + dy^2", font_size=40),
            mtex(r"\text{plane, polar:}", r"\quad ds^2", r"=", r"dr^2 + r^2\,d\phi^2", font_size=40),
            mtex(r"\text{sphere:}", r"\quad ds^2", r"=", r"R^2\big(d\theta^2 + \sin^2\!\theta\,d\phi^2\big)",
                 font_size=40),
        )
        for r in rows:
            r[0].set_color(GREY_A)
            r[3].set_color(C.METRIC)
        rows.arrange(DOWN, buff=0.7)
        for r in rows[1:]:
            r.shift((rows[0][2].get_center()[0] - r[2].get_center()[0]) * RIGHT)
        rows.next_to(gen, DOWN, buff=0.7)
        mats = VGroup(
            mtex(r"g_{ij} = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}", font_size=36, color=C.METRIC),
            mtex(r"g_{ij} = \begin{pmatrix} 1 & 0 \\ 0 & r^2 \end{pmatrix}", font_size=36, color=C.METRIC),
            mtex(r"g_{ij} = \begin{pmatrix} R^2 & 0 \\ 0 & R^2\sin^2\theta \end{pmatrix}", font_size=36,
                 color=C.METRIC),
        )
        for m, r in zip(mats, rows):
            m.next_to(r, RIGHT, buff=0.6)
        grp = VGroup(rows, mats)
        if grp.width > 13.4:
            grp.scale_to_fit_width(13.4)
        grp.set_x(0)
        with self.voiceover(
            "The basic measurement is distance. <bookmark mark='g'/> Label the points of a surface with coordinates, "
            "and the distance between two nearby points is given by a formula like this: d s squared equals g i j, d x i, "
            "d x j, summed over i and j. The coefficients g i j are called the metric. They convert steps in the "
            "coordinates into real distances."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("g")
            self.play(Write(gen))
        with self.voiceover(
            "<bookmark mark='a'/> On a flat plane in ordinary coordinates, it's Pythagoras: d x squared plus d y squared. "
            "<bookmark mark='b'/> The same plane in polar coordinates gives d r squared plus r squared d phi squared, "
            "because a step in angle covers more ground far from the center. <bookmark mark='c'/> And on a sphere of "
            "radius R, with theta measured down from the north pole and phi around the equator, a step in phi covers "
            "less and less ground as you approach a pole: that's the sine squared theta."
        ) as vo:
            for m, r, mt in zip("abc", rows, mats):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.2), FadeIn(mt), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tissot(self):
        """The metric as a field of ellipses: equal circles on the globe, drawn in the (phi, latitude) chart."""
        view = View3D(center=[-4.3, -0.5, 0], scale=2.2, azimuth=-0.35, elevation=0.4)
        globe = Globe(view, grid_opacity=0.25)
        eps = 0.19
        lats = np.radians([-60, -30, 0, 30, 60])
        lons = np.radians(np.arange(-150, 180, 45))
        circles3d = []
        for la in lats:
            for lo in lons:
                p = sphere_points(np.pi / 2 - la, lo)
                circles3d.append(small_circle(p, eps))
        g3d = always_redraw(lambda: VGroup(*[curve3d(view, P, color=C.METRIC, stroke_width=2.2, back_opacity=0.0)
                                            for P in circles3d]))
        ax = Axes(x_range=[-np.pi, np.pi, np.pi / 2], y_range=[-np.pi / 2, np.pi / 2, np.pi / 4], x_length=7.6,
                  y_length=3.8, tips=False, axis_config={"stroke_color": GREY_B, "include_ticks": False})
        ax.move_to([2.95, -0.55, 0])
        frame = SurroundingRectangle(ax, buff=0, color=GREY_C, stroke_width=1.5)
        xl = MathTex(r"\phi", font_size=30).next_to(ax, DOWN, buff=0.15)
        yl = label(r"latitude", font_size=24, color=GREY_A).rotate(PI / 2).next_to(ax, LEFT, buff=0.15)
        ell = VGroup()
        for la in lats:
            for lo in lons:
                th = np.pi / 2 - la
                a = np.linspace(0, 2 * np.pi, 60)
                xs = lo + eps * np.cos(a) / np.sin(th)
                ys = la + eps * np.sin(a)
                pts = ax.c2p(xs, ys).T
                m = VMobject(stroke_color=C.METRIC, stroke_width=2.2)
                m.set_points_as_corners(pts)
                ell.add(m)
        clip_note = note(r"each shape: every point at distance $\varepsilon$ from its center").next_to(frame, UP, buff=0.3)
        mat = mtex(r"g_{ij} = R^2\begin{pmatrix} 1 & 0 \\ 0 & \sin^2\theta \end{pmatrix}", font_size=32,
                   color=C.METRIC).to_corner(UR, buff=0.45)
        with self.voiceover(
            "Here's a way to see a metric. <bookmark mark='a'/> On the globe, draw little circles, every point at the same "
            "small distance epsilon from a center. They're all the same size. <bookmark mark='b'/> Now flatten the globe "
            "onto a map, with longitude across and latitude up. In map coordinates, those identical circles become "
            "ellipses, wider and wider toward the poles, because near a pole you need a big change in longitude to "
            "travel a short distance. <bookmark mark='c'/> That field of ellipses is the metric: at every point, it tells "
            "you which coordinate steps have the same real length."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(globe))
            self.add(g3d)
            self.play(view.az.animate.set_value(0.25), run_time=vo.until("b"), rate_func=smooth)
            self.play(Create(frame), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(clip_note))
            self.play(LaggedStart(*[Create(e) for e in ell], lag_ratio=0.02), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(mat))
        g3d.clear_updaters()
        globe.gridlines.clear_updaters()

        flat = VGroup(
            label(r"But a changing metric doesn't mean curvature:", font_size=30),
            mtex(r"ds^2 = dr^2 + r^2\,d\phi^2", font_size=36, color=C.METRIC),
            label(r"is the flat plane, in polar coordinates.", font_size=30),
        ).arrange(DOWN, buff=0.2)
        with self.voiceover(
            "But careful. A metric that varies from place to place doesn't, by itself, mean the space is curved. "
            "<bookmark mark='f'/> The polar-coordinate metric varies too, and it describes a perfectly flat plane. "
            "Coordinates can make a flat space look complicated. So we need a test for curvature that doesn't care "
            "which coordinates we use."
        ) as vo:
            self.play(FadeOut(VGroup(ell, frame, ax, xl, yl, clip_note, mat)))
            flat.move_to([2.8, 0, 0])
            vo.wait_until("f")
            self.play(FadeIn(flat, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def triangle(self):
        view = View3D(center=[-2.6, -0.5, 0], scale=2.9, azimuth=OCTANT_AZ, elevation=0.55)
        globe = Globe(view, grid_opacity=0.2)
        N, A, B = np.array([0, 0, 1.0]), np.array([1.0, 0, 0]), np.array([0, 1.0, 0])
        edges = [great_arc(N, A), great_arc(A, B), great_arc(B, N)]
        tri = always_redraw(lambda: VGroup(*[curve3d(view, E, color=WHITE, stroke_width=4) for E in edges]))
        marks = always_redraw(lambda: VGroup(
            right_angle_mark(view, N, A - N * (A @ N), B - N * (B @ N), color=C.CURVATURE),
            right_angle_mark(view, A, N, B, color=C.CURVATURE),
            right_angle_mark(view, B, A, N, color=C.CURVATURE)))
        steps = VGroup(
            label(r"Start at the north pole, walk straight down to the equator,", font_size=26),
            label(r"turn $90^\circ$, walk a quarter of the way around,", font_size=26),
            label(r"turn $90^\circ$, walk straight back to the pole.", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.45)
        sum_ = mtex(r"90^\circ + 90^\circ + 90^\circ", r"=", r"270^\circ", font_size=42)
        sum_[2].set_color(C.CURVATURE)
        sum_.move_to([3.6, 0.6, 0])
        excess = mtex(r"\text{excess}", r"=", r"\alpha+\beta+\gamma-180^\circ", r"=", r"\frac{\text{area}}{R^2}",
                      font_size=36)
        excess[4].set_color(C.CURVATURE)
        excess.next_to(sum_, DOWN, buff=0.5).set_x(3.4)
        check = mtex(r"\text{octant: } \frac{4\pi R^2/8}{R^2} = \frac{\pi}{2} = 90^\circ", font_size=32,
                     color=GREY_A).next_to(excess, DOWN, buff=0.35)
        gb = mtex(r"\alpha+\beta+\gamma-\pi = \iint K\,dA", font_size=34, color=C.CURVATURE)
        gb.next_to(check, DOWN, buff=0.45)
        gbl = note(r"Gauss--Bonnet: $K$ = Gaussian curvature $= 1/R^2$ on a sphere").next_to(gb, DOWN, buff=0.15)
        with self.voiceover(
            "Here's the first test: triangles. <bookmark mark='a'/> Start at the north pole and walk straight down to the "
            "equator. <bookmark mark='b'/> Turn ninety degrees and walk a quarter of the way around the equator. "
            "<bookmark mark='c'/> Turn ninety degrees again and walk straight back to the pole. Every side is a straight "
            "line, as far as the ant can tell: it never turned while walking. <bookmark mark='d'/> And when it arrives, "
            "it meets its starting path at another right angle."
        ) as vo:
            self.play(FadeIn(globe))
            self.add(tri)
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            vo.wait_until("d")
            self.add(marks)
            self.play(FadeOut(steps), view.az.animate.set_value(OCTANT_AZ + 0.25), run_time=1.5)
        with self.voiceover(
            "<bookmark mark='s'/> The angles add up to two hundred and seventy degrees, not one eighty. "
            "<bookmark mark='e'/> And the excess isn't random. It equals the triangle's area divided by R squared: "
            "<bookmark mark='o'/> this triangle covers one eighth of the sphere, and one eighth of four pi R squared, "
            "over R squared, is pi over two: exactly ninety degrees. <bookmark mark='g'/> In general, the angle excess is "
            "the total curvature inside the triangle. The ant can measure angles and areas, so the ant can measure "
            "curvature."
        ) as vo:
            vo.wait_until("s")
            self.play(Write(sum_))
            vo.wait_until("e")
            self.play(Write(excess))
            vo.wait_until("o")
            self.play(FadeIn(check))
            vo.wait_until("g")
            self.play(Write(gb), FadeIn(gbl))
        self.tri_view, self.tri_globe, self.tri_edges = view, globe, (tri, marks)
        self.play(FadeOut(VGroup(sum_, excess, check, gb, gbl)))

    # ------------------------------------------------------------------
    def transport(self):
        view, globe = self.tri_view, self.tri_globe
        tri, marks = self.tri_edges
        d = load("transport")
        paths = d["tri_paths"].reshape(-1, 3)
        vecs = d["tri_vecs"].reshape(-1, 3)
        assert abs(abs(float(d["tri_turn"])) - 90) < 0.01
        k = ValueTracker(0.0)
        L = 0.42

        def arrow():
            i = int(round(k.get_value() * (len(paths) - 1)))
            return arrow3d(view, paths[i], L * vecs[i], color=C.VECTOR, stroke_width=6)

        ghost = arrow3d(view, paths[0], L * vecs[0], color=C.VECTOR, stroke_width=4).set_opacity(0.35)
        arr = always_redraw(arrow)
        rule = VGroup(
            label(r"\textbf{Parallel transport}", font_size=32, color=C.VECTOR),
            label(r"carry an arrow along the path,", font_size=28),
            label(r"never turning it relative to the surface", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.45)
        res = mtex(r"\text{rotation}", r"=", r"90^\circ", r"=", r"\text{angle excess}", font_size=38)
        res[2].set_color(C.VECTOR)
        res[4].set_color(C.CURVATURE)
        res.move_to([3.4, -0.6, 0])
        with self.voiceover(
            "Here's a second test, and it's the one we'll turn into a machine. <bookmark mark='a'/> Give the ant an arrow "
            "to carry, and a rule: never rotate it relative to the surface. Walking along a straight line, that means "
            "the arrow keeps a fixed angle to the direction of travel. <bookmark mark='w'/> Watch it go around the "
            "triangle. Down the first side, pointing along the path. Along the equator, it now points sideways, because "
            "the path turned but the arrow didn't. Then back up to the pole."
        ) as vo:
            self.play(FadeIn(rule))
            vo.wait_until("a")
            self.add(arr)
            self.add(ghost)
            vo.wait_until("w")
            self.play(k.animate.set_value(1.0), run_time=vo.remaining() + 1.5, rate_func=linear)
        with self.voiceover(
            "<bookmark mark='r'/> The arrow comes home rotated by ninety degrees: exactly the angle excess. On a flat "
            "page, an arrow carried around any loop this way comes back unchanged. On a curved surface, it comes back "
            "rotated by the curvature enclosed. <bookmark mark='m'/> This is the idea we'll make precise. The rotation per "
            "unit area, at every point and in every orientation, packaged into one object computed from the metric alone: "
            "the Riemann curvature tensor. To build it, we first need the language of tensors."
        ) as vo:
            vo.wait_until("r")
            self.play(Write(res))
            self.play(Indicate(res[2], color=C.VECTOR))
            vo.wait_until("m")
            self.play(view.az.animate.set_value(OCTANT_AZ - 0.15), run_time=2)
        for m in (arr, tri, marks, globe.gridlines):
            m.clear_updaters()
        self.clear_scene()
