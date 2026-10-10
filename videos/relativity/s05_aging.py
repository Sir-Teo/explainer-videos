from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity.common import (redraw, View3D, boxed, curve3d, label, load, mtex, note, polyline, rgba, stack)

C_LIGHT = 299_792_458.0
G0 = 9.81
UNIT = 1e-16  # proper-time differences are shown in units of 1e-16 s


def excess(h, T=2.0):
    """tau - T for the parabola of peak height h, in seconds."""
    return (2 / 3 * G0 * h * T - 8 * h * h / (3 * T)) / C_LIGHT**2


class MaximalAging(VoiceoverScene):
    def construct(self):
        self.setup_diagram()
        self.sweep()
        self.competition()
        self.other_shapes()
        self.derivation()
        self.rubber_sheet()
        self.tides()

    # ------------------------------------------------------------------
    def setup_diagram(self):
        d = load("aging")
        self.d = d
        T = 2.0
        assert abs(float(d["h_star"]) - 4.905) < 1e-3
        assert abs(float(d["tau_star"]) / UNIT - 3.57) < 0.01
        assert np.allclose(d["closed"], [excess(h) for h in d["hs"]])
        facts = VGroup(
            label(r"1.\ \ Free objects follow worldlines of \emph{maximal proper time}.", font_size=32),
            label(r"2.\ \ Clocks higher up run faster: \ $d\tau/dt = 1 + gz/c^2$.", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        with self.voiceover(
            "We now have two facts. <bookmark mark='a'/> First, free objects follow worldlines of maximal proper time. "
            "<bookmark mark='b'/> Second, near the Earth, clocks run faster the higher they are. Let's put them together "
            "and see what happens."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(facts[0], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(facts[1], shift=RIGHT * 0.2))
        self.play(FadeOut(facts))

        ax = Axes(x_range=[0, 2, 0.5], y_range=[-1, 13, 2], x_length=6.0, y_length=5.2, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": True, "font_size": 22},
                  x_axis_config={"numbers_to_include": [0.5, 1, 1.5, 2]},
                  y_axis_config={"numbers_to_include": [2, 4, 6, 8, 10, 12]})
        ax.to_edge(LEFT, buff=0.9).shift(DOWN * 0.35)
        xl = label(r"time (s)", font_size=24).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = label(r"height (m)", font_size=24).next_to(ax.y_axis, UP, buff=0.15)
        # background: clock rate grows with height
        p0, p1 = ax.c2p(0, 0), ax.c2p(2, 13)
        h_img = 120
        z = np.linspace(13, 0, h_img)[:, None] * np.ones((1, 8))
        col = np.array(ManimColor(C.PROPER_TIME).to_rgb())
        img = rgba(np.ones((h_img, 8, 3)) * col, 0.05 + 0.3 * z / 13)
        bg = ImageMobject(img).stretch_to_fit_width(p1[0] - p0[0]).stretch_to_fit_height(p1[1] - p0[1])
        bg.move_to((p0 + p1) / 2)
        bgl = label(r"clocks tick faster $\uparrow$", font_size=24, color=C.PROPER_TIME).next_to(ax.c2p(2, 12.5), LEFT, buff=0.1)
        A, B = Dot(ax.c2p(0, 0), radius=0.08), Dot(ax.c2p(2, 0), radius=0.08)
        Al = label(r"thrown", font_size=22).next_to(A, DOWN, buff=0.35)
        Bl = label(r"caught", font_size=22).next_to(B, DOWN, buff=0.35)
        self.ax, self.T = ax, T
        self.h = ValueTracker(0.0)
        ts = np.linspace(0, T, 120)

        def path():
            hh = self.h.get_value()
            return polyline(ax, ts, 4 * hh * ts * (T - ts) / T**2, color=WHITE, stroke_width=4)

        self.path = redraw(path)

        # right: excess proper time vs peak height
        rax = Axes(x_range=[0, 12, 2], y_range=[-4, 4, 2], x_length=5.0, y_length=4.2, tips=False,
                   axis_config={"stroke_color": GREY_B, "include_ticks": True, "font_size": 22},
                   x_axis_config={"numbers_to_include": [2, 4, 6, 8, 10, 12]},
                   y_axis_config={"numbers_to_include": [-4, -2, 2, 4]})
        rax.to_edge(RIGHT, buff=0.7).shift(DOWN * 0.6)
        rxl = label(r"peak height (m)", font_size=24).next_to(rax.x_axis, DOWN, buff=0.4)
        ryl = mtex(r"\tau - T \ \ (10^{-16}\,\text{s})", font_size=26, color=C.PROPER_TIME).next_to(rax, UP, buff=0.2)
        hs = d["hs"]
        curve = polyline(rax, hs, d["excess"] / UNIT, color=C.PROPER_TIME, stroke_width=4)
        self.rax, self.curve = rax, curve
        self.rlabels = VGroup(rxl, ryl)
        dot = redraw(lambda: Dot(rax.c2p(self.h.get_value(), excess(self.h.get_value()) / UNIT), radius=0.08,
                                        color=WHITE))
        head = MathTex(r"\tau - T =", font_size=34, color=C.PROPER_TIME)
        val = DecimalNumber(0, num_decimal_places=2, font_size=34, include_sign=True, color=C.PROPER_TIME)
        unit = MathTex(r"\times 10^{-16}\ \text{s}", font_size=34, color=C.PROPER_TIME)
        ro = VGroup(head, val, unit).arrange(RIGHT, buff=0.15).to_corner(UR, buff=0.45)
        val.add_updater(lambda m: m.set_value(excess(self.h.get_value()) / UNIT))
        self.ro, self.val, self.dot = ro, val, dot

        with self.voiceover(
            "Throw a ball straight up, and catch it two seconds later at the same spot. <bookmark mark='d'/> On a "
            "spacetime diagram, with time across and height up, that's two events: the throw and the catch. "
            "<bookmark mark='c'/> And the background is shaded by how fast clocks run: faster the higher you go. "
            "<bookmark mark='q'/> Now ask: of all the worldlines that connect these two events, which one has the most "
            "proper time? <bookmark mark='z'/> Staying on the ground is one option. We'll measure every other path "
            "against it: tau minus T, the extra time a clock riding along would record."
        ) as vo:
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(A), FadeIn(B), FadeIn(Al), FadeIn(Bl))
            vo.wait_until("c")
            self.add(bg, ax, A, B)
            self.play(FadeIn(bg), FadeIn(bgl))
            vo.wait_until("q")
            self.add(self.path)
            vo.wait_until("z")
            self.play(Create(rax), FadeIn(rxl), FadeIn(ryl), FadeIn(ro))
            self.add(dot)

    # ------------------------------------------------------------------
    def sweep(self):
        h = self.h
        hs_tr = VGroup()
        with self.voiceover(
            "<bookmark mark='u'/> Go a little higher, and the clock spends its time where time runs faster: it gains. "
            "<bookmark mark='v'/> Go higher still and it gains more, up to a point. <bookmark mark='w'/> But to get high "
            "and come back in two seconds, the ball must move fast, and moving clocks run slow. Go too high, and the "
            "speed costs more than the height gains: <bookmark mark='x'/> at twelve meters, the clock actually loses time."
        ) as vo:
            self.play(Create(self.curve), run_time=1.0)
            vo.wait_until("u")
            self.play(h.animate.set_value(2.0), run_time=2)
            vo.wait_until("v")
            self.play(h.animate.set_value(4.0), run_time=2)
            vo.wait_until("w")
            self.play(h.animate.set_value(8.0), run_time=2.5)
            vo.wait_until("x")
            self.play(h.animate.set_value(12.0), run_time=2)
        hstar = float(self.d["h_star"])
        tstar = float(self.d["tau_star"]) / UNIT
        vline = DashedLine(self.rax.c2p(hstar, -4), self.rax.c2p(hstar, 4), color=GREY_B, stroke_width=2)
        mx = label(r"maximum at $h = 4.9$ m", font_size=26).next_to(self.rax.c2p(hstar, tstar), UP, buff=0.25)
        newton = VGroup(label(r"Newton: thrown up at 9.8 m/s,", font_size=26),
                        label(r"a ball peaks at $h = \tfrac12 g t^2 = 4.9$ m", font_size=26)).arrange(DOWN, buff=0.1)
        newton.next_to(self.ro, DOWN, buff=0.3).align_to(self.ro, RIGHT)
        with self.voiceover(
            "<bookmark mark='m'/> Somewhere in between there's a best height. It comes out at four point nine meters, where "
            "the ball's clock gains about three and a half times ten to the minus sixteen seconds. <bookmark mark='n'/> "
            "And four point nine meters is exactly how high Newton says a ball rises if it's in the air for two "
            "seconds. <bookmark mark='p'/> The path of maximal proper time is the path the ball actually takes."
        ) as vo:
            vo.wait_until("m")
            self.play(h.animate.set_value(hstar), run_time=2.5)
            self.play(Create(vline), FadeIn(mx))
            vo.wait_until("n")
            self.play(FadeIn(newton))
            vo.wait_until("p")
            self.play(Indicate(self.path, color=C.PROPER_TIME))
        self.mx, self.vline, self.newton = mx, vline, newton

    # ------------------------------------------------------------------
    def competition(self):
        rax = self.rax
        hs = np.linspace(0, 12, 200)
        T = self.T
        gain = (2 / 3 * G0 * hs * T) / C_LIGHT**2 / UNIT
        cost = -(8 * hs**2 / (3 * T)) / C_LIGHT**2 / UNIT
        okg, okc = gain <= 4, cost >= -4
        cg = polyline(rax, hs[okg], gain[okg], color=C.PROPER_TIME, stroke_width=2.5).set_stroke(opacity=0.7)
        cc = polyline(rax, hs[okc], cost[okc], color=RED_B, stroke_width=2.5).set_stroke(opacity=0.8)
        cg = DashedVMobject(cg, num_dashes=30)
        cc = DashedVMobject(cc, num_dashes=30)
        eq = mtex(r"\tau - T", r"\approx", r"\frac{1}{c^2}\int g z\,dt", r"-", r"\frac{1}{c^2}\int \tfrac12 v^2\,dt",
                  font_size=34)
        eq[0].set_color(C.PROPER_TIME)
        eq[2].set_color(C.PROPER_TIME)
        eq[4].set_color(RED_B)
        eq.to_corner(UR, buff=0.35)
        b1 = Brace(eq[2], DOWN, buff=0.1, color=C.PROPER_TIME)
        b1l = label(r"height: faster clocks", font_size=22, color=C.PROPER_TIME).next_to(b1, DOWN, buff=0.05)
        b2 = Brace(eq[4], DOWN, buff=0.1, color=RED_B)
        b2l = label(r"speed: slower clocks", font_size=22, color=RED_B).next_to(b2, DOWN, buff=0.05)
        with self.voiceover(
            "<bookmark mark='e'/> Here's the bookkeeping. To first order, the extra time is the integral of g z over c "
            "squared, the gain from height, <bookmark mark='g'/> which grows in proportion to how high you go, "
            "<bookmark mark='c'/> minus the integral of half v squared over c squared, the cost of speed, which grows like "
            "the square of the height. A gain that grows linearly, minus a cost that grows quadratically: their "
            "difference has a single maximum."
        ) as vo:
            self.play(FadeOut(self.newton), FadeOut(self.ro))
            vo.wait_until("e")
            self.play(Write(eq))
            vo.wait_until("g")
            self.play(GrowFromCenter(b1), FadeIn(b1l), Create(cg))
            vo.wait_until("c")
            self.play(GrowFromCenter(b2), FadeIn(b2l), Create(cc))
        self.comp = VGroup(eq, b1, b1l, b2, b2l, cg, cc)

    # ------------------------------------------------------------------
    def other_shapes(self):
        d = self.d
        ax, T = self.ax, self.T
        oex = d["others_excess"] / UNIT
        tstar = float(d["tau_star"]) / UNIT
        assert np.all(oex < tstar)
        cols = [GREY_B, LIGHT_PINK, GOLD_A]
        names = [r"hover", r"lopsided", r"too high"]
        paths = VGroup(*[polyline(ax, d["t"][::20], z[::20], color=c, stroke_width=3) for z, c in zip(d["others"], cols)])
        rows = VGroup(*[mtex(rf"\text{{{n}:}}\ \ {v:+.2f}", font_size=30, color=c) for n, v, c in zip(names, oex, cols)])
        rows.add(mtex(rf"\text{{Newton's parabola:}}\ \ {tstar:+.2f}", font_size=30, color=WHITE))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.9, 0.2, 0])
        rhead = mtex(r"\tau - T\ \ (10^{-16}\,\text{s})", font_size=30, color=C.PROPER_TIME).next_to(rows, UP, buff=0.4)
        rows_bg = VGroup(rhead)
        with self.voiceover(
            "It isn't just parabolas. <bookmark mark='o'/> Any other way of getting from the throw to the catch, "
            "hovering at the top, rising slowly and falling fast, or going too high, records less proper time. Among all "
            "possible paths, the ball's real one is the longest-lived."
        ) as vo:
            self.play(FadeOut(self.comp), FadeOut(self.mx), FadeOut(self.vline), FadeOut(self.rax), FadeOut(self.curve),
                      FadeOut(self.dot), FadeOut(self.rlabels))
            vo.wait_until("o")
            self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.3), FadeIn(rows_bg), FadeIn(rows, lag_ratio=0.2),
                      run_time=2.5)
        self.path.clear_updaters()
        self.dot.clear_updaters()
        self.val.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def derivation(self):
        rows = stack(
            mtex(r"\tau", r"=", r"\int \sqrt{\Big(1 + \frac{2\Phi}{c^2}\Big) - \frac{v^2}{c^2}}\;dt", font_size=40),
            mtex(r"\tau", r"\approx", r"\int \Big(1 + \frac{\Phi}{c^2} - \frac{v^2}{2c^2}\Big)\,dt", font_size=40),
            mtex(r"-mc^2\,\tau", r"\approx", r"\int \Big(\tfrac12 m v^2 - m\Phi\Big)\,dt \;-\; mc^2 T", font_size=40),
            buff=0.5,
        )
        for r in rows:
            r[0].set_color(C.PROPER_TIME)
        rows.move_to(UP * 0.9)
        why = VGroup(
            note(r"from $ds^2 = -(1+2\Phi/c^2)c^2dt^2 + d\mathbf{x}^2$", font_size=24).next_to(rows[0], RIGHT, buff=0.3),
            note(r"$\sqrt{1+\epsilon} \approx 1 + \epsilon/2$", font_size=24).next_to(rows[1], RIGHT, buff=0.3),
            note(r"multiply by $-mc^2$", font_size=24).next_to(rows[2], RIGHT, buff=0.3),
        )
        for w in why:
            if w.get_right()[0] > 7.0:
                w.shift((7.0 - w.get_right()[0]) * RIGHT + DOWN * 0.45)
        lag = Brace(rows[2][2], DOWN, color=C.POTENTIAL)
        lagl = label(r"Newton's action: kinetic minus potential energy", font_size=26, color=C.POTENTIAL).next_to(lag, DOWN, buff=0.1)
        res = mtex(r"\delta\tau = 0", r"\;\Longleftrightarrow\;", r"m\,\ddot{\mathbf x} = -m\,\nabla\Phi", font_size=44)
        res[2].set_color(C.POTENTIAL)
        res.to_edge(DOWN, buff=0.6)
        rb = SurroundingRectangle(res, color=C.PROPER_TIME, buff=0.2, corner_radius=0.1)
        with self.voiceover(
            "Now let's prove it in general. <bookmark mark='a'/> The proper time of any path is the integral of d tau, the "
            "square root of minus d s squared over c squared, using the metric we just found: one plus two phi over c squared, minus v "
            "squared over c squared, all under the root. <bookmark mark='b'/> Both corrections are tiny, so expand the "
            "square root to first order. <bookmark mark='c'/> Now multiply by minus m c squared. What's inside the "
            "integral is one half m v squared minus m phi: kinetic energy minus potential energy. That's exactly the "
            "action of Newtonian mechanics, plus a constant."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(why[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]), FadeIn(why[1]))
            vo.wait_until("c")
            self.play(Write(rows[2]), FadeIn(why[2]))
            self.play(GrowFromCenter(lag), FadeIn(lagl))
        with self.voiceover(
            "And the principle of least action says Newton's laws are what you get when that action is stationary. "
            "<bookmark mark='r'/> So making the proper time stationary gives m times acceleration equals minus m times "
            "the gradient of phi: Newton's law of gravity. <bookmark mark='m'/> Notice that the mass cancels from both "
            "sides, so every object falls the same way. That isn't a coincidence anymore: the path depends only on the "
            "geometry. Gravity, for slow objects, is nothing but the warping of time."
        ) as vo:
            vo.wait_until("r")
            self.play(Write(res), Create(rb))
            vo.wait_until("m")
            self.play(Indicate(res[2], color=C.POTENTIAL))
        self.clear_scene()

    # ------------------------------------------------------------------
    def rubber_sheet(self):
        view = View3D(center=[-3.7, -0.4, 0], scale=0.88, azimuth=0.3, elevation=0.95)

        def zf(r):
            return -2.2 / np.sqrt(r * r + 0.55)

        sheet = VGroup()
        for rr in np.linspace(0.5, 3.4, 9):
            a = np.linspace(0, 2 * np.pi, 120)
            P = np.stack([rr * np.cos(a), rr * np.sin(a), zf(rr) * np.ones_like(a)], 1)
            sheet.add(curve3d(view, P, color=C.METRIC, stroke_width=1.6, sphere_r=None))
        for a in np.linspace(0, 2 * np.pi, 20, endpoint=False):
            rr = np.linspace(0.5, 3.4, 60)
            P = np.stack([rr * np.cos(a), rr * np.sin(a), zf(rr)], 1)
            sheet.add(curve3d(view, P, color=C.METRIC, stroke_width=1.6, sphere_r=None))
        ball = Circle(radius=0.42, color=C.MATTER, fill_opacity=0.9).move_to(view.point([0, 0, zf(0.5) + 0.3]))
        tag = label(r"the popular picture", font_size=30, color=GREY_A).next_to(sheet, UP, buff=0.2)
        cons = VGroup(
            label(r"It explains gravity\ldots\ using gravity.", font_size=30),
            label(r"It shows curved \emph{space}.", font_size=30),
            label(r"For slow objects, curved \emph{time} dominates:", font_size=30, color=C.PROPER_TIME),
            label(r"space's share is $\sim v^2/c^2 \approx 10^{-15}$ for a thrown ball.", font_size=30, color=C.PROPER_TIME),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.5, 0.0, 0])
        with self.voiceover(
            "This is worth pausing on, <bookmark mark='p'/> because you may have seen general relativity pictured as a "
            "ball sitting in a stretched rubber sheet. <bookmark mark='a'/> That picture is misleading in two ways. "
            "First, it explains gravity using gravity: the marble rolls down the dip because something pulls it down. "
            "<bookmark mark='b'/> Second, it shows curved space. <bookmark mark='c'/> But what makes an apple fall is "
            "curved time. Space is warped too, but for slow objects its effect is smaller by a factor of v squared over c "
            "squared: about ten to the minus fifteen, for a thrown ball."
        ) as vo:
            vo.wait_until("p")
            self.play(Create(sheet, lag_ratio=0.02), FadeIn(ball), FadeIn(tag), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(cons[0]))
            vo.wait_until("b")
            self.play(FadeIn(cons[1]))
            vo.wait_until("c")
            self.play(FadeIn(cons[2]), FadeIn(cons[3]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def tides(self):
        d = load("tidal")
        pos, rel = d["pos"], d["rel"]
        R_E = 6.371e6
        n_show = int(np.searchsorted(d["stretch"], 1.6)) + 1  # stop at 1.6x: later the ring becomes a needle
        stretch, squeeze = float(d["stretch"][n_show - 1]), float(d["squeeze"][n_show - 1])
        assert 1.55 < stretch < 1.65 and squeeze < 0.85
        # left: the Earth and the falling ring (true scale)
        s = 0.55 / R_E
        earth_c = np.array([-4.2, -3.0, 0])
        earth = Circle(radius=R_E * s, color=C.MATTER, fill_opacity=0.35, stroke_width=3).move_to(earth_c)
        el = label(r"Earth", font_size=24, color=C.MATTER).next_to(earth, RIGHT, buff=0.15)
        k = ValueTracker(0.0)
        n = n_show

        def ring_left():
            i = int(round(k.get_value() * (n - 1)))
            P = pos[i, 1:] * s
            pts = np.concatenate([P, np.zeros((len(P), 1))], 1) + earth_c
            return VGroup(*[Dot(p, radius=0.025, color=C.CURVATURE) for p in pts])

        left = redraw(ring_left)
        # right: the same ring seen from its freely falling center, magnified
        zc = np.array([2.6, -0.2, 0])
        m = 1.45 / float(d["ring"])

        def ring_right():
            i = int(round(k.get_value() * (n - 1)))
            P = rel[i] * m
            pts = np.concatenate([P, np.zeros((len(P), 1))], 1) + zc
            g = VGroup(VMobject(stroke_color=C.CURVATURE, stroke_width=2, stroke_opacity=0.5).set_points_as_corners(
                [*pts, pts[0]]))
            g.add(*[Dot(p, radius=0.07, color=C.CURVATURE) for p in pts])
            return g

        right = redraw(ring_right)
        circle0 = DashedVMobject(Circle(radius=1.45, color=GREY_B, stroke_width=2).move_to(zc), num_dashes=40)
        center = Dot(zc, radius=0.05, color=WHITE)
        frame = label(r"seen from the freely falling center (magnified)", font_size=24, color=GREY_A).move_to([zc[0], 3.3, 0])
        down = Arrow(zc + RIGHT * 2.9 + UP * 0.6, zc + RIGHT * 2.9 + DOWN * 0.6, buff=0, color=GREY_B, stroke_width=3)
        downl = label(r"to Earth", font_size=22, color=GREY_B).next_to(down, DOWN, buff=0.1)
        lab = VGroup(label(r"stretched along the fall", font_size=26, color=C.CURVATURE),
                     label(r"squeezed sideways", font_size=26, color=C.CURVATURE)).arrange(DOWN, buff=0.12)
        lab.to_edge(DOWN, buff=0.35).set_x(zc[0])
        with self.voiceover(
            "One more step. In a rocket, the same speeding up of clocks with height appears in perfectly flat spacetime, "
            "so it can't be the whole story of a real gravitational field. What can a falling observer never get rid of? "
            "<bookmark mark='r'/> Release a ring of free particles high above the Earth. <bookmark mark='f'/> Each one falls "
            "toward the center of the Earth, along a slightly different line, and the near side is pulled a little harder "
            "than the far side. <bookmark mark='z'/> From the ring's own falling center, there's no gravity at all, except "
            "this: the ring stretches along the direction of the fall and squeezes sideways."
        ) as vo:
            vo.wait_until("r")
            self.play(FadeIn(earth), FadeIn(el))
            self.add(left)
            vo.wait_until("f")
            self.play(Create(circle0), FadeIn(center), FadeIn(frame), GrowArrow(down), FadeIn(downl))
            self.add(right)
            vo.wait_until("z")
            self.play(k.animate.set_value(1.0), run_time=vo.remaining() + 1.0, rate_func=linear)
            self.play(FadeIn(lab))
        with self.voiceover(
            "These are tides, the same effect that raises the oceans. A freely falling observer can cancel gravity at one "
            "point, but not its variation from point to point: nearby free paths converge or spread apart. That's the "
            "true, unremovable signature of gravity. <bookmark mark='c'/> And in geometry, the way that nearby straight "
            "lines converge or spread apart has a name: curvature. To say what that means for spacetime, we need some "
            "mathematics."
        ) as vo:
            vo.wait_until("c")
            self.play(lab.animate.set_color(C.CURVATURE).scale(1.05))
        left.clear_updaters()
        right.clear_updaters()
        self.clear_scene()
