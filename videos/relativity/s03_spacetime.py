from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity.common import redraw, boxed, label, light_cone, mtex, note, part_card, st_axes, stack


def clip_segment(f, x0, x1, t0, t1, n=200):
    """Points of the curve (x, f(x)) for x in [x0, x1] that fall inside t in [t0, t1]."""
    xs = np.linspace(x0, x1, n)
    ts = f(xs)
    ok = (ts >= t0) & (ts <= t1)
    return xs[ok], ts[ok]


class Spacetime(VoiceoverScene):
    def construct(self):
        self.card()
        self.diagram()
        self.boost()
        self.proper_time()
        self.twins()
        self.notation()

    def card(self):
        c = part_card(1, r"Gravity is geometry", r"spacetime, clocks, and falling")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def diagram(self):
        g = st_axes(x_range=(-3.2, 3.2), t_range=(0, 3.5), unit=1.3)
        g.move_to(DOWN * 0.55)
        ax = g.ax
        head = label(r"Special relativity (1905): one spacetime", font_size=36).to_edge(UP, buff=0.35)
        rest = Line(ax.c2p(-2.4, 0), ax.c2p(-2.4, 3.5), color=WHITE, stroke_width=4)
        moving = Line(ax.c2p(0.8, 0), ax.c2p(0.8 + 0.45 * 3.5, 3.5), color=C.METRIC, stroke_width=4)
        light = Line(ax.c2p(-2.0, 0), ax.c2p(1.5, 3.5), color=C.LIGHT, stroke_width=4)
        lr = label(r"at rest", font_size=26).next_to(rest.get_end(), LEFT, buff=0.15).shift(DOWN * 0.3)
        lm = label(r"moving at $0.45c$", font_size=26, color=C.METRIC).next_to(moving.get_end(), RIGHT, buff=0.15).shift(DOWN * 0.3)
        ll = label(r"light: $45^\circ$", font_size=26, color=C.LIGHT).next_to(light.get_end(), LEFT, buff=0.2).shift(DOWN * 0.3)
        ev = Dot(ax.c2p(-1.0, 1.6), radius=0.08)
        evl = label(r"an event: \emph{here}, \emph{now}", font_size=24).next_to(ev, LEFT, buff=0.12)
        with self.voiceover(
            "Before gravity, we need the stage it plays out on. Special relativity, Einstein's theory from 1905, treats space "
            "and time as a single four-dimensional spacetime. <bookmark mark='d'/> We'll draw it with one space "
            "direction across and time going up, with time multiplied by the speed of light, c, so both axes are "
            "measured in meters. <bookmark mark='e'/> A point is an event: a place and a moment. <bookmark mark='w'/> "
            "The history of an object is a line, its worldline. Something at rest goes straight up. "
            "<bookmark mark='m'/> Something moving tilts. <bookmark mark='l'/> And light moves at forty-five degrees, "
            "one meter of distance per meter of time."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(g[1:]))
            vo.wait_until("e")
            self.play(FadeIn(ev), FadeIn(evl))
            vo.wait_until("w")
            self.play(FadeOut(ev), FadeOut(evl), Create(rest), FadeIn(lr))
            vo.wait_until("m")
            self.play(Create(moving), FadeIn(lm))
            vo.wait_until("l")
            self.play(Create(light), FadeIn(ll))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def boost(self):
        g = st_axes(x_range=(-3.0, 3.0), t_range=(-0.2, 3.4), unit=1.05)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        eta = ValueTracker(0.0)
        T0, T1, X0, X1 = -0.2, 3.4, -3.0, 3.0

        def grid():
            e = eta.get_value()
            ch, sh = math.cosh(e), math.sinh(e)
            G = VGroup()
            for k in np.arange(-3, 4):
                # constant ct' = k:  ct ch - x sh = k  ->  ct = (k + x sh) / ch
                xs, ts = clip_segment(lambda x: (k + x * sh) / ch, X0, X1, T0, T1)
                if len(xs) > 1:
                    G.add(Line(ax.c2p(xs[0], ts[0]), ax.c2p(xs[-1], ts[-1]), color=C.METRIC, stroke_width=1.5,
                               stroke_opacity=0.9 if k == 0 else 0.35))
                # constant x' = k:  x ch - ct sh = k  ->  x = (k + ct sh) / ch, parametrize by ct
                ts2 = np.linspace(T0, T1, 200)
                xs2 = (k + ts2 * sh) / ch
                ok = (xs2 >= X0) & (xs2 <= X1)
                if ok.sum() > 1:
                    a, b = np.nonzero(ok)[0][[0, -1]]
                    G.add(Line(ax.c2p(xs2[a], ts2[a]), ax.c2p(xs2[b], ts2[b]), color=C.METRIC, stroke_width=1.5,
                               stroke_opacity=0.9 if k == 0 else 0.35))
            return G

        grid_m = redraw(grid)
        cone = VGroup(DashedLine(ax.c2p(0, 0), ax.c2p(3.0, 3.0), color=C.LIGHT, stroke_width=2),
                      DashedLine(ax.c2p(0, 0), ax.c2p(-3.0, 3.0), color=C.LIGHT, stroke_width=2))
        # hyperbola -(ct)^2 + x^2 = -s2 through the event
        P = np.array([0.7, 1.6])
        s2 = P[1] ** 2 - P[0] ** 2
        hyp_x = np.linspace(-2.6, 2.6, 200)
        hyp = VMobject(color=C.PROPER_TIME, stroke_width=3).set_points_smoothly(
            [ax.c2p(x, math.sqrt(s2 + x * x)) for x in hyp_x])

        def event_pos():
            # the event as seen in the boosted frame keeps ct'^2 - x'^2; we move the event *with* the boost so that
            # its primed coordinates stay fixed while it slides along the hyperbola
            e = eta.get_value()
            ch, sh = math.cosh(e), math.sinh(e)
            x = P[0] * ch + P[1] * sh
            t = P[1] * ch + P[0] * sh
            return x, t

        ev = redraw(lambda: Dot(ax.c2p(*event_pos()), radius=0.08, color=WHITE))

        heads = VGroup(MathTex(r"ct =", font_size=34), MathTex(r"x =", font_size=34),
                       MathTex(r"-(ct)^2 + x^2 =", font_size=34, color=C.PROPER_TIME))
        heads.arrange(DOWN, aligned_edge=RIGHT, buff=0.3).move_to([3.0, 0.1, 0])
        vals = VGroup(*[DecimalNumber(0, num_decimal_places=2, font_size=34, include_sign=False) for _ in range(3)])
        vals[2].set_color(C.PROPER_TIME)

        def upd(i):
            def f(m):
                x, t = event_pos()
                v = (t, x, -(t * t) + x * x)[i]
                m.set_value(v)
                m.next_to(heads[i], RIGHT, buff=0.2)
            return f

        for i, v in enumerate(vals):
            v.add_updater(upd(i))
            v.update()  # waits freeze frames when no updater is time-based: show the right value from the start
        ro = VGroup(heads, vals)

        inv = mtex(r"\Delta s^2", r"=", r"-(c\,\Delta t)^2 + \Delta x^2 + \Delta y^2 + \Delta z^2", font_size=36)
        inv[0].set_color(C.PROPER_TIME)
        inv.to_corner(UR, buff=0.45)
        same = label(r"the same for every inertial observer", font_size=26, color=GREY_A).next_to(inv, DOWN, buff=0.15)
        with self.voiceover(
            "Different observers, moving relative to each other, slice spacetime differently. <bookmark mark='g'/> Here's "
            "the coordinate grid of one observer. <bookmark mark='b'/> Here's what it looks like for someone moving to the "
            "right: their time axis tilts toward the light ray, and so does their space axis. They disagree about which "
            "events are simultaneous, and about distances and durations."
        ) as vo:
            self.play(Create(ax), FadeIn(g[1:]), FadeIn(cone))
            vo.wait_until("g")
            self.add(grid_m)
            vo.wait_until("b")
            self.play(eta.animate.set_value(0.55), run_time=2.5)
            self.play(eta.animate.set_value(-0.4), run_time=2.5)
            self.play(eta.animate.set_value(0.0), run_time=1.5)
        with self.voiceover(
            "But there's one thing they all agree on. <bookmark mark='i'/> Take two events, and compute minus c delta t "
            "squared plus delta x squared, plus delta y squared plus delta z squared. This combination, the spacetime "
            "interval, is the same for every observer. <bookmark mark='p'/> Pick an event. As we change observers, its "
            "time and space coordinates change, <bookmark mark='h'/> but the event only ever slides along this hyperbola, "
            "and the interval stays fixed. It's the spacetime version of distance, with one crucial minus sign."
        ) as vo:
            vo.wait_until("i")
            self.play(Write(inv), FadeIn(same))
            vo.wait_until("p")
            self.add(ev, ro)
            vo.wait_until("h")
            self.play(Create(hyp))
            self.play(eta.animate.set_value(0.6), run_time=2.2)
            self.play(eta.animate.set_value(-0.5), run_time=2.6)
            self.play(eta.animate.set_value(0.0), run_time=1.6)
        for m in (grid_m, ev, *vals):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def proper_time(self):
        rows = stack(
            mtex(r"c^2\,d\tau^2", r"=", r"-ds^2", r"=", r"c^2\,dt^2 - dx^2", font_size=44),
            mtex(r"d\tau", r"=", r"dt\,\sqrt{1 - v^2/c^2}", font_size=44),
        )
        rows[0][0].set_color(C.PROPER_TIME)
        rows[1][0].set_color(C.PROPER_TIME)
        rows.move_to(UP * 1.2)
        tau = mtex(r"\tau", r"=", r"\int d\tau", font_size=44)
        tau[0].set_color(C.PROPER_TIME)
        tau.next_to(rows, DOWN, buff=0.7)
        cap = label(r"a clock measures the spacetime length of its own worldline", font_size=30, color=C.PROPER_TIME)
        cap.next_to(tau, DOWN, buff=0.35)
        with self.voiceover(
            "For two events along the worldline of a clock, the interval has a direct meaning. <bookmark mark='a'/> Minus "
            "the interval, divided by c squared, is the square of the time that clock measures between them: its proper "
            "time, tau. "
            "<bookmark mark='b'/> For a clock moving at speed v, d tau is d t times the square root of one minus v squared "
            "over c squared. Moving clocks run slow. <bookmark mark='c'/> Add it up along the whole worldline, and a "
            "clock's reading is simply the length of its path through spacetime, measured with this minus-sign geometry."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]))
            vo.wait_until("c")
            self.play(Write(tau), FadeIn(cap))
        self.clear_scene()

    # ------------------------------------------------------------------
    def twins(self):
        g = st_axes(x_range=(-0.5, 5.0), t_range=(0, 10.4), unit=0.6, x_label=r"x\ (\text{light-years})",
                    t_label=r"ct\ (\text{years})")
        ax = g.ax
        g.shift(np.array([-3.9, -3.25, 0]) - ax.c2p(0, 0))
        A, B = ax.c2p(0, 0), ax.c2p(0, 10)
        home = Line(A, B, color=WHITE, stroke_width=4)
        turn = ax.c2p(4, 5)
        trav = VMobject(color=C.METRIC, stroke_width=4).set_points_as_corners([A, turn, B])
        dA, dB = Dot(A, radius=0.08), Dot(B, radius=0.08)
        ticks_home = VGroup(*[Dot(ax.c2p(0, k), radius=0.05, color=C.PROPER_TIME) for k in range(1, 10)])
        # traveler: v = 0.8, gamma = 5/3: one year of proper time = 5/3 years of coordinate time
        tk = []
        for k in range(1, 6):
            t = k * 5 / 3
            x = 0.8 * t if t <= 5 else 4 - 0.8 * (t - 5)
            tk.append(Dot(ax.c2p(x, t), radius=0.05, color=C.PROPER_TIME))
        ticks_trav = VGroup(*tk)
        lh = label(r"stays home: 10 years", font_size=26).next_to(ax.c2p(0, 7.5), LEFT, buff=0.15)
        lt = label(r"travels at $0.8c$: 6 years", font_size=26, color=C.METRIC).next_to(turn, RIGHT, buff=0.15)
        others = VGroup()
        taus = []
        for v in (0.3, 0.6, 0.95):
            others.add(VMobject(color=C.METRIC, stroke_width=2, stroke_opacity=0.45).set_points_as_corners(
                [A, ax.c2p(5 * v, 5), B]))
            taus.append(10 * math.sqrt(1 - v * v))
        assert [f"{x:.1f}" for x in taus] == ["9.5", "8.0", "3.1"]
        table = VGroup(*[mtex(rf"v = {v}c:\ \ \tau = {t:.1f}\ \text{{yr}}", font_size=30, color=C.PROPER_TIME)
                         for v, t in zip((0, 0.3, 0.6, 0.8, 0.95), [10.0] + taus[:2] + [6.0] + taus[2:])])
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.6, 1.0, 0])
        rule = label(r"The straight worldline has the \emph{most} proper time.", font_size=32, color=C.PROPER_TIME)
        rule2 = label(r"Free particles maximize $\tau$.", font_size=32)
        VGroup(rule, rule2).arrange(DOWN, buff=0.2).move_to([3.4, -2.2, 0])
        with self.voiceover(
            "That minus sign has a famous consequence. <bookmark mark='a'/> Take two events at the same place, ten years "
            "apart. <bookmark mark='h'/> One twin stays home, on the straight worldline between them, and ages ten years. "
            "<bookmark mark='t'/> The other flies out at eight tenths the speed of light, turns around, and comes back. "
            "Their path is bent, and along each leg their clock ticks at only six tenths the rate. They return having "
            "aged six years."
        ) as vo:
            self.play(Create(ax), FadeIn(g[1:]))
            vo.wait_until("a")
            self.play(FadeIn(dA), FadeIn(dB))
            vo.wait_until("h")
            self.play(Create(home), FadeIn(lh))
            self.play(LaggedStart(*[FadeIn(d) for d in ticks_home], lag_ratio=0.15))
            vo.wait_until("t")
            self.play(Create(trav), FadeIn(lt), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(d) for d in ticks_trav], lag_ratio=0.2))
        with self.voiceover(
            "<bookmark mark='o'/> Every bent path between the same two events ages less, and the faster the trip, the "
            "less. <bookmark mark='r'/> In ordinary geometry, a straight line is the shortest path. In spacetime, "
            "because of the minus sign, a straight worldline is the longest: it has the most proper time. And straight "
            "worldlines are what free particles follow. <bookmark mark='f'/> So here's a law of motion that will "
            "survive into general relativity: a free particle moves so as to maximize its proper time. Keep it in mind, "
            "because it's how gravity is about to sneak in."
        ) as vo:
            vo.wait_until("o")
            self.play(LaggedStart(*[Create(o) for o in others], lag_ratio=0.2), FadeIn(table, lag_ratio=0.1), run_time=2)
            vo.wait_until("r")
            self.play(FadeIn(rule))
            vo.wait_until("f")
            self.play(FadeIn(rule2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def notation(self):
        line1 = mtex(r"ds^2", r"=", r"-c^2dt^2 + dx^2 + dy^2 + dz^2", font_size=44)
        coords = mtex(r"x^\mu = (x^0, x^1, x^2, x^3) = (ct, x, y, z)", font_size=36, color=GREY_A)
        line2 = mtex(r"ds^2", r"=", r"\eta_{\mu\nu}\,dx^\mu dx^\nu", font_size=48)
        line2[2].set_color(C.METRIC)
        eta = mtex(r"\eta_{\mu\nu} = \begin{pmatrix} -1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 "
                   r"\end{pmatrix}", font_size=34, color=C.METRIC)
        summ = label(r"Einstein's convention: an index repeated up and down is summed over $0,1,2,3$", font_size=26,
                     color=GREY_A)
        col = VGroup(line1, coords, line2).arrange(DOWN, buff=0.5).move_to([-1.6, 0.8, 0])
        eta.next_to(col, RIGHT, buff=0.8)
        summ.to_edge(DOWN, buff=1.4)
        gx = mtex(r"\eta_{\mu\nu}", r"\;\longrightarrow\;", r"g_{\mu\nu}(x)", font_size=52)
        gx[0].set_color(C.METRIC)
        gx[2].set_color(C.METRIC)
        gx.to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Let's write the interval in the notation we'll use from now on. <bookmark mark='c'/> Label the four "
            "coordinates x zero through x three, with x zero equal to c t. <bookmark mark='e'/> Then d s squared is eta "
            "mu nu, d x mu, d x nu, where eta is this diagonal matrix: minus one for time, plus one for each direction of "
            "space. <bookmark mark='s'/> And we use Einstein's summation convention: whenever an index appears once up "
            "and once down, it's summed over all four values. Sixteen terms, most of them zero, written in one line."
        ) as vo:
            self.play(Write(line1))
            vo.wait_until("c")
            self.play(FadeIn(coords))
            vo.wait_until("e")
            self.play(Write(line2), FadeIn(eta))
            vo.wait_until("s")
            self.play(FadeIn(summ))
        with self.voiceover(
            "Eta is the metric of flat spacetime: the same matrix at every point. <bookmark mark='g'/> Here's the idea we "
            "are building toward: gravity is what happens when this matrix is replaced by a metric g mu nu that varies "
            "from place to place."
        ) as vo:
            vo.wait_until("g")
            self.play(FadeOut(summ), Write(gx))
            self.play(Circumscribe(gx[2], color=C.METRIC))
        self.clear_scene()
