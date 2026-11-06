from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.algo import geometry as G
from videos.cs.cs22.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, load, mono, words)

ORG = np.array([-2.6, -1.25, 0.0])
XY = 1.45
KZ = 0.42


class Lifting(VoiceoverScene):
    def construct(self):
        self.card()
        self.tour()
        self.determinant()

    def card(self):
        card = chapter_card(7, r"The lifting map", r"Why is Delaunay the shadow of a hull?", lit=(1979, 1986),
                            extra=((1979, r"Brown"), (1986, r"Edelsbrunner--Seidel")), part=PART)
        with self.voiceover("Chapter seven. The lifting map."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tour(self):
        d = load("lifting")
        P = [tuple(p) for p in d["P"]]
        lower = [tuple(int(i) for i in t) for t in d["lower"]]
        th = ValueTracker(-0.5)          # azimuth
        ph = ValueTracker(PI / 2)       # elevation: pi/2 looks straight down
        lam = ValueTracker(0.0)         # how far the points are lifted
        circ = ValueTracker(0.0)        # the lifted circle's visibility
        t0 = lower[len(lower) // 2]
        cx, cy, cr = G._circumcircle(*[P[i] for i in t0])

        def proj(x, y, z):
            a, e = th.get_value(), ph.get_value()
            x1 = x * np.cos(a) - y * np.sin(a)
            y1 = x * np.sin(a) + y * np.cos(a)
            return ORG + np.array([x1 * XY, (y1 * np.sin(e) + z * KZ * np.cos(e)) * XY, 0.0])

        def lifted(i):
            x, y = P[i]
            return proj(x, y, lam.get_value() * (x * x + y * y))

        def scene3d():
            g = VGroup()
            L = lam.get_value()
            if L > 0.01:
                for rho in (0.6, 1.2, 1.8, 2.3):
                    pts = [proj(rho * np.cos(t), rho * np.sin(t), L * rho * rho) for t in np.linspace(0, TAU, 61)]
                    g.add(VMobject(color=GREY_D, stroke_width=1).set_points_as_corners(pts))
                for t in np.linspace(0, TAU, 13)[:-1]:
                    pts = [proj(r_ * np.cos(t), r_ * np.sin(t), L * r_ * r_) for r_ in np.linspace(0, 2.3, 24)]
                    g.add(VMobject(color=GREY_D, stroke_width=1).set_points_as_corners(pts))
            for t in lower:
                g.add(Polygon(*[lifted(i) for i in t], color=YES, stroke_width=1.6).set_fill(YES, 0.12 + 0.2 * L))
            if L > 0.01:
                for t in lower:
                    g.add(Polygon(*[proj(*P[i], 0) for i in t], color=GREY_B, stroke_width=0.8))
            for i in range(len(P)):
                if L > 0.01:
                    g.add(DashedLine(proj(*P[i], 0), lifted(i), color=GREY_D, stroke_width=1, dash_length=0.05))
                g.add(Dot(lifted(i), radius=0.055, color=HEAD))
            c = circ.get_value()
            if c > 0.01:
                ring = [proj(cx + cr * np.cos(t), cy + cr * np.sin(t), 0) for t in np.linspace(0, TAU, 73)]
                g.add(VMobject(color=LAM, stroke_width=2.5, stroke_opacity=c).set_points_as_corners(ring))
                up = [proj(cx + cr * np.cos(t), cy + cr * np.sin(t),
                           L * ((cx + cr * np.cos(t)) ** 2 + (cy + cr * np.sin(t)) ** 2)) for t in np.linspace(0, TAU, 73)]
                g.add(VMobject(color=NO, stroke_width=3, stroke_opacity=c).set_points_as_corners(up))
            return g
        world = always_redraw(scene3d)
        head = label(r"Lift every point onto a paraboloid", font_size=32).to_edge(UP, buff=0.3)
        side = VGroup(
            label(r"the Delaunay triangulation, \ seen from above", font_size=21, color=YES),
            MathTex(r"(x, y) \;\mapsto\; (x,\ y,\ x^2 + y^2)", font_size=30, color=HEAD),
            label(r"the lifted points are in convex position; \\ take the \textbf{lower} hull", font_size=21,
                  color=WHITE),
            label(r"a circle in the plane lifts to a curve \\ on a plane through the paraboloid", font_size=21,
                  color=NO),
            label(r"inside the circle $\iff$ \ below that plane", font_size=21, color=LAM),
            label(r"empty circle $\iff$ every other point above \\ $\iff$ a face of the lower hull", font_size=21,
                  color=YES),
            label(r"so: \ Delaunay $=$ the lower hull's shadow \\ (Brown, 1979; \ in any dimension: \\ "
                  r"Edelsbrunner and Seidel, 1986)", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.35)
        if side.width > 5.3:
            side.width = 5.3
            side.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Here is the most beautiful fact in this part. <bookmark mark='a'/> Take the Delaunay triangulation of "
            "some points, seen from above. <bookmark mark='b'/> Now lift every point straight up, onto the "
            "paraboloid z equals x squared plus y squared. <bookmark mark='c'/> The lifted points sit on a convex "
            "bowl, so all of them are on the three-dimensional convex hull. Look at the hull from below: its faces "
            "are triangles. <bookmark mark='d'/> Why those triangles? Take a circle in the plane. Its points, "
            "lifted, all lie on one plane, because on the circle x squared plus y squared is a linear function of x "
            "and y. <bookmark mark='e'/> A point inside the circle lifts to below that plane, and a point outside "
            "lifts to above it. <bookmark mark='f'/> So a circle through three sites is empty exactly when every "
            "other lifted point is above the plane through those three: exactly when the three lifted points form a "
            "face of the lower hull. <bookmark mark='g'/> The Delaunay triangulation is the shadow of the lower "
            "convex hull of the lifted points. Kevin Brown saw it in 1979, and it holds in every dimension: Delaunay "
            "in d dimensions is a hull in d plus one."
        ) as vo:
            self.play(FadeIn(head))
            self.add(world)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), ph.animate.set_value(0.42), run_time=3.0)
            self.play(lam.animate.set_value(1.0), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), th.animate.set_value(0.9), run_time=5.0, rate_func=smooth)
            vo.wait_until("d")
            self.play(FadeIn(side[3]), circ.animate.set_value(1.0), run_time=1.5)
            self.play(th.animate.set_value(0.2), run_time=3.0)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]), ph.animate.set_value(0.15), run_time=3.0)
            vo.wait_until("g")
            self.play(FadeIn(side[6]), circ.animate.set_value(0.0), ph.animate.set_value(PI / 2),
                      lam.animate.set_value(0.0), run_time=4.0)
        world.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def determinant(self):
        d = load("lifting")
        head = label(r"In-circle is orientation, \ one dimension up", font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            MathTex(r"\mathrm{incircle}(a, b, c, d) = \det\begin{pmatrix} a_x & a_y & a_x^2 + a_y^2 & 1 \\ "
                    r"b_x & b_y & b_x^2 + b_y^2 & 1 \\ c_x & c_y & c_x^2 + c_y^2 & 1 \\ d_x & d_y & d_x^2 + d_y^2 & 1"
                    r"\end{pmatrix}", font_size=30, color=LAM),
            label(r"the 3D orientation test of the four \textbf{lifted} points: \ is $d$'s lift below the plane of the "
                  r"other three?", font_size=22, color=WHITE),
            label(rf"$a = (0, 0)$, \ $b = (4, 0)$, \ $c = (0, 4)$, \ $d = (1, 1)$: \ the $4 \times 4$ determinant is "
                  rf"{d['det4']:.0f}, \ the $3 \times 3$ of chapter 6 is {d['incircle']:.0f}", font_size=22, color=YES),
            label(r"a Lawson flip replaces a reflex edge of the lifted surface by a convex one: \ the surface only goes "
                  r"down, \ so flipping must stop", font_size=22, color=HEAD),
            label(r"and the Voronoi diagram is the upper envelope of the planes tangent to the paraboloid above each "
                  r"site", font_size=22, color=DATA),
            label(rf"checked: \ the lower hull of our {len(d['P'])} lifted points, \ by scipy's 3D hull, \ is exactly "
                  r"\texttt{scipy.spatial.Delaunay}", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "The lifting map also explains the in-circle test. <bookmark mark='a'/> Write the coordinates of four "
            "points with their lifted heights in a four by four determinant. <bookmark mark='b'/> It is the "
            "orientation test in three dimensions, the sign of a volume, asking whether d's lifted point lies below "
            "the plane through the other three. <bookmark mark='c'/> For one example the four by four determinant "
            "and chapter six's three by three both come out at ninety-six, because subtracting the last row reduces "
            "one to the other. <bookmark mark='d'/> It also finishes chapter six: a Lawson flip replaces an edge "
            "where the lifted surface bends up with one where it bends down, so the surface drops with every flip, "
            "and since there are only finitely many triangulations, flipping stops. <bookmark mark='e'/> And the "
            "Voronoi diagram is the same picture turned over: lift each site to a plane tangent to the paraboloid, "
            "and the Voronoi regions are the shadows of the faces of their upper envelope. <bookmark mark='f'/> We "
            "checked the theorem: the lower faces of scipy's hull of our lifted points are exactly scipy's "
            "Delaunay triangulation."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
