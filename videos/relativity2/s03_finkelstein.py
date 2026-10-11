from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity2 import spacetime as st
from videos.relativity2.common import (under, Chart, boxed, clipped, label, ladder, load, mtex, note, polyline, redraw,
                                       zigzag)
from videos.relativity2.geometry import check_eddington_finkelstein

INFALLER = C.MATTER


def outgoing_tt(r, r0, t0):
    """EF time t~ along the outgoing radial light ray through (r0, t0): t~ = t0 + (r - r0) + 4 ln|(r-2)/(r0-2)|."""
    return t0 + (r - r0) + 4 * np.log(np.abs((r - 2) / (r0 - 2)))


class Finkelstein(VoiceoverScene):
    def construct(self):
        assert check_eddington_finkelstein() == "ok"
        self.tortoise()
        self.metric()
        self.morph()
        self.rays()

    # ------------------------------------------------------------------
    def tortoise(self):
        rows = [
            mtex(r"0", r"=", r"-\Big(1 - \frac{2M}{r}\Big)dt^2 + \frac{dr^2}{1 - 2M/r}", font_size=40),
            mtex(r"\frac{dt}{dr}", r"=", r"\pm\frac{1}{1 - 2M/r}", font_size=40),
            mtex(r"t", r"=", r"\pm\, r^* + \text{const},\qquad r^* \equiv r + 2M\ln\Big|\frac{r}{2M} - 1\Big|", font_size=40),
        ]
        whys = [
            note(r"a light ray moving radially: $ds^2 = 0$, \ $d\theta = d\phi = 0$"),
            note(r"outgoing ($+$) and ingoing ($-$)"),
            note(r"integrate: $dr^*/dr = 1/(1 - 2M/r)$. \ $r^*$ is the ``tortoise'' coordinate"),
        ]
        rows[1][0].set_color(C.LIGHT)
        rows[2][2].set_color(C.LIGHT)
        x0 = -0.6
        under(rows, whys, x0)
        step = ladder(self, rows, whys, keep=3, top=3.5, x=x0, buff=0.42)
        ax = Axes(x_range=[0, 10, 2], y_range=[-8, 10, 4], x_length=5.0, y_length=2.5, tips=False,
                  axis_config={"stroke_color": GREY_B, "font_size": 20},
                  x_axis_config={"numbers_to_include": [2, 4, 6, 8]},
                  y_axis_config={"numbers_to_include": [-4, 4, 8]}).move_to([-2.6, -2.45, 0])
        rr = np.linspace(2.0001, 10, 400)
        cur = polyline(ax, rr, np.maximum(st.tortoise(rr), -8), color=C.LIGHT, stroke_width=3.5)
        hz = DashedLine(ax.c2p(2, -8), ax.c2p(2, 10), color=C.CURVATURE, stroke_width=2)
        xl = label(r"$r/M$", font_size=22).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = label(r"$r^*/M$", font_size=22, color=C.LIGHT).next_to(ax.y_axis, UP, buff=0.1)
        txt = VGroup(label(r"$r^* \to -\infty$ as $r \to 2M$:", font_size=28),
                     label(r"in the time $t$, light takes forever", font_size=28),
                     label(r"to reach the horizon", font_size=28)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        txt.move_to([3.3, -2.4, 0])
        with self.voiceover(
            "To find better coordinates, follow light. <bookmark mark='a'/> A light ray moving straight in or out has "
            "zero interval. <bookmark mark='b'/> So dt d r is plus or minus one over one minus two M over r. "
            "<bookmark mark='c'/> Integrating, t is plus or minus a new radial coordinate, r star, plus a constant. "
            "Physicists call r star the tortoise coordinate, for a reason you can see in its graph. "
            "<bookmark mark='g'/> As r approaches two M, r star plunges to minus infinity: measured in t, light takes "
            "forever to reach the horizon, like Zeno's tortoise."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("g")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(hz))
            self.play(Create(cur), FadeIn(txt, lag_ratio=0.2), run_time=2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def metric(self):
        rows = [
            mtex(r"v", r"\equiv", r"t + r^*", font_size=42),
            mtex(r"dt", r"=", r"dv - \frac{dr}{1 - 2M/r}", font_size=42),
            mtex(r"ds^2", r"=", r"-\Big(1 - \frac{2M}{r}\Big)dv^2 + 2\,dv\,dr + r^2 d\Omega^2", font_size=44),
        ]
        whys = [
            note(r"ingoing light rays have constant $v$: label events by the ingoing ray they're on"),
            note(r"so substitute this into the Schwarzschild metric"),
            note(r"the $dr^2$ terms cancel exactly: nothing blows up at $r = 2M$"),
        ]
        rows[0][0].set_color(C.LIGHT)
        rows[2][2].set_color(C.METRIC)
        x0 = -1.0
        under(rows, whys, x0)
        step = ladder(self, rows, whys, keep=3, top=3.0, x=x0, buff=0.65)
        checks = VGroup(
            mtex(r"\det g = -r^4\sin^2\theta \neq 0", font_size=34),
            label(r"still a vacuum solution, $R_{\mu\nu} = 0$ (checked symbolically)", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.15).move_to(DOWN * 1.75)
        hist = VGroup(
            label(r"Eddington (1924) wrote this form for another purpose, without remarking on it;", font_size=24,
                  color=GREY_A),
            label(r"Finkelstein (1958) recognized $r = 2M$ as ``a perfect unidirectional membrane''", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "<bookmark mark='a'/> So label events by the ingoing light ray they sit on. Define v equals t plus r star; "
            "it's constant along every ingoing ray. <bookmark mark='b'/> Then dt is d v minus d r over one minus two M "
            "over r. <bookmark mark='c'/> Substitute that into the metric, and something lovely happens: the d r "
            "squared terms cancel exactly, and what's left has nothing that blows up at r equals two M. "
            "<bookmark mark='d'/> The determinant isn't zero there, and it's still a solution of Einstein's equation in "
            "empty space: the same spacetime, in better coordinates. <bookmark mark='h'/> Eddington wrote down this form "
            "in 1924, but didn't remark on it. David Finkelstein rediscovered it in 1958, and saw what it meant."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(checks, lag_ratio=0.2))
            vo.wait_until("h")
            self.play(FadeIn(hist, lag_ratio=0.3))
        self.clear_scene()

    # ------------------------------------------------------------------
    def morph(self):
        """Schwarzschild's (r, t) chart -> Finkelstein's (r, t~ = t + 2M ln|r/2M - 1|): the cones stop closing and
        tip over instead."""
        ch = Chart(center=[-0.2, -0.4, 0], scale=0.62, origin=(5.0, 3.0), box=(-6.4, 6.2, -3.2, 2.9))
        s = ValueTracker(0.0)
        r_lines = [2.5, 3, 4, 5, 6, 8, 10, 12, 14]
        t_lines = np.arange(-6, 18, 2.0)

        def y_of(r, t, sv):
            return t + sv * 2 * np.log(np.abs(r / 2 - 1))

        def grid():
            sv = s.get_value()
            g = VGroup()
            tt = np.linspace(-30, 40, 300)
            for r0 in r_lines:
                g.add(ch.curve(np.full_like(tt, r0), y_of(r0, tt, sv), color=C.METRIC, stroke_width=1.2, opacity=0.5))
            rr = np.linspace(2.0005, 15, 400)
            for t0 in t_lines:
                g.add(ch.curve(rr, y_of(rr, t0, sv), color=C.PROPER_TIME, stroke_width=1.2, opacity=0.5))
            return g

        base_pts = [(r0, t0) for r0 in (2.3, 3.0, 4.0, 6.0, 9.0, 12.5) for t0 in (-2.0, 2.5, 7.0)]

        def cones():
            sv = s.get_value()
            g = VGroup()
            for r0, t0 in base_pts:
                y0 = y_of(r0, t0, sv)
                if not (-2.6 < ch.p(r0, y0)[1] < 2.3):
                    continue
                slopes = [-(r0 - 2 * sv) / (r0 - 2), (r0 + 2 * sv) / (r0 - 2)]  # dy/dr of the ingoing, outgoing rays
                tip = ch.p(r0, y0)
                ends = []
                for k, m in enumerate(slopes):
                    d = np.array([-1.0 if k == 0 else 1.0, (-1.0 if k == 0 else 1.0) * m])
                    if d[1] < 0:  # future-directed: up the page
                        d = -d
                    d = d / np.linalg.norm(d) * 0.55
                    ends.append(tip + np.array([d[0], d[1], 0]))
                g.add(VGroup(Polygon(tip, ends[0], ends[1], stroke_width=0, fill_color=C.LIGHT, fill_opacity=0.28),
                             Line(tip, ends[0], color=C.LIGHT, stroke_width=2), Line(tip, ends[1], color=C.LIGHT,
                                                                                       stroke_width=2)))
            return g

        G, K = redraw(grid), redraw(cones)
        hz = DashedLine(ch.p(2, -2.4), ch.p(2, 9.6), color=C.CURVATURE, stroke_width=3)
        hzl = label(r"$r = 2M$", font_size=24, color=C.CURVATURE).next_to(hz, UP, buff=0.08)
        xl = label(r"$r$", font_size=26).move_to(ch.p(15.8, -2.3))
        yl = always_redraw(lambda: label(r"$t$" if s.get_value() < 0.5 else r"$\tilde t = v - r$", font_size=26,
                                         color=C.PROPER_TIME).move_to([-6.6, 3.0, 0]))
        leg = VGroup(label(r"lines of constant $r$", font_size=22, color=C.METRIC),
                     label(r"lines of constant $t$", font_size=22, color=C.PROPER_TIME),
                     label(r"light cones", font_size=22, color=C.LIGHT)).arrange(RIGHT, buff=0.5).to_corner(DR, buff=0.15)
        eqs = mtex(r"\tilde t", r"=", r"t + 2M\ln\Big|\frac{r}{2M} - 1\Big|", font_size=34).to_corner(UR, buff=0.3)
        eqs.add_background_rectangle(color=BACKGROUND, opacity=0.9, buff=0.08)
        with self.voiceover(
            "Let's see what this does to the picture. <bookmark mark='a'/> Here's the Schwarzschild chart: r across, t "
            "up, with light cones at a few places. Near r equals two M, the cones get narrower and narrower, and close "
            "up. That's what made the horizon look like a wall. <bookmark mark='b'/> Now change the time coordinate to "
            "t tilde, which is v minus r, so that ingoing light always moves at forty-five degrees. "
            "<bookmark mark='c'/> Watch the cones. They stop closing. Instead, as you approach the horizon, they tip "
            "over, toward smaller r. The lines of constant t, which seemed so natural, plunge down at the horizon: "
            "they were the problem all along."
        ) as vo:
            vo.wait_until("a")
            self.add(G)
            self.play(Create(hz), FadeIn(hzl), FadeIn(xl), FadeIn(yl), FadeIn(leg))
            self.add(K)
            vo.wait_until("b")
            self.play(FadeIn(eqs))
            vo.wait_until("c")
            self.play(s.animate.set_value(1.0), run_time=6, rate_func=smooth)
        G.clear_updaters()
        K.clear_updaters()
        yl.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def rays(self):
        d = load("infall")
        ch = Chart(center=[-1.2, -0.3, 0], scale=0.5, origin=(5.0, 6.0), box=(-6.6, 4.0, -3.4, 3.4))
        rr_axis = Line(ch.p(0, -0.6), ch.p(11.5, -0.6), color=GREY_B, stroke_width=2)
        xl = label(r"$r/M$", font_size=22).next_to(rr_axis, RIGHT, buff=0.1)
        ticks = VGroup(*[label(f"{k}", font_size=20).next_to(ch.p(k, -0.6), DOWN, buff=0.08) for k in (0, 2, 4, 6, 8, 10)])
        yl = label(r"$\tilde t$", font_size=26, color=C.PROPER_TIME).move_to(ch.p(-0.9, 12.5))
        sing = zigzag(ch.p(0, -0.6), ch.p(0, 13.6))
        sl = label(r"$r = 0$", font_size=22, color=C.SINGULARITY).next_to(ch.p(0, 13.6), UP, buff=0.05)
        hz = Line(ch.p(2, -0.6), ch.p(2, 13.6), color=C.CURVATURE, stroke_width=4)
        hzl = label(r"horizon", font_size=22, color=C.CURVATURE).next_to(ch.p(2, 13.6), UP, buff=0.05)
        # ingoing rays (45 degrees) and outgoing rays (computed)
        ing = VGroup()
        for v0 in np.arange(2, 26, 2.0):
            r = np.linspace(0, 11.5, 50)
            ing.add(ch.curve(r, v0 - r, color=C.LIGHT, stroke_width=1.4, opacity=0.45))
        outs = VGroup()
        for r0 in (2.6, 3.4, 5.0):
            r = np.linspace(r0, 11.5, 200)
            outs.add(ch.curve(r, outgoing_tt(r, r0, 0.0), color=C.LIGHT, stroke_width=2.6))
        gen = Line(ch.p(2, 0), ch.p(2, 13.6), color=C.LIGHT, stroke_width=2.6)
        ins = VGroup()
        for r0 in (1.85, 1.5, 1.0):
            r = np.linspace(r0, 1e-3, 200)
            ins.add(ch.curve(r, outgoing_tt(r, r0, 0.0), color=C.LIGHT, stroke_width=2.6))
        # the astronaut, smooth through the horizon
        r_i, tt_i = d["r"], d["ttilde"]
        i_h = int(d["i_h"])
        tt_i = tt_i - tt_i[i_h] + 7.0  # (the same fall, started earlier: t~ is only defined up to a constant)
        wl = ch.curve(r_i, tt_i, color=INFALLER, stroke_width=4.5)
        j0 = int(np.argmax(tt_i > 0.3))
        j1 = int(np.argmin(np.abs(r_i - 0.25)))
        k = ValueTracker(0.0)

        def cone():
            j = int(j0 + k.get_value() * (j1 - j0))
            r0, y0 = r_i[j], tt_i[j]
            tip = ch.p(r0, y0)
            m_out = (r0 + 2) / (r0 - 2)
            d_in = np.array([-1.0, 1.0]) / math.sqrt(2) * 0.6
            d_out = np.array([1.0, m_out]) if r0 > 2 else np.array([-1.0, -m_out])
            d_out = d_out / np.linalg.norm(d_out) * 0.6
            a, b = tip + [*d_in, 0], tip + [*d_out, 0]
            return VGroup(Polygon(tip, a, b, stroke_width=0, fill_color=C.LIGHT, fill_opacity=0.35),
                          Line(tip, a, color=C.LIGHT, stroke_width=3), Line(tip, b, color=C.LIGHT, stroke_width=3),
                          Dot(tip, radius=0.08, color=INFALLER))

        Kc = redraw(cone)
        txt = VGroup(
            label(r"outside: outgoing light escapes", font_size=24),
            label(r"at $r = 2M$: it hovers forever", font_size=24, color=C.CURVATURE),
            label(r"inside: even ``outgoing'' light", font_size=24),
            label(r"moves to smaller $r$", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.9, 1.2, 0])
        mem = VGroup(label(r"The horizon is made of light:", font_size=26, color=C.CURVATURE),
                     label(r"a one-way membrane.", font_size=26, color=C.CURVATURE)).arrange(DOWN, aligned_edge=LEFT,
                                                                                        buff=0.1).move_to([4.9, -1.6, 0])
        with self.voiceover(
            "Now draw the black hole in these coordinates. <bookmark mark='a'/> Ingoing light rays are straight lines at "
            "forty-five degrees. <bookmark mark='b'/> Outgoing rays, launched outside the horizon, escape, though the "
            "closer they start to it, the longer they linger. <bookmark mark='c'/> A ray launched outward exactly at r "
            "equals two M stays there forever: the horizon is itself made of light rays, hovering in place. "
            "<bookmark mark='d'/> And inside, even a ray aimed outward moves to smaller r, and ends at r equals zero."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(rr_axis), FadeIn(xl), FadeIn(ticks), FadeIn(yl), Create(sing), FadeIn(sl), Create(hz),
                      FadeIn(hzl))
            self.play(FadeIn(ing))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(o) for o in outs], lag_ratio=0.3), FadeIn(txt[0]), run_time=2)
            vo.wait_until("c")
            self.play(Create(gen), FadeIn(txt[1]))
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(o) for o in ins], lag_ratio=0.3), FadeIn(txt[2:]), run_time=2)
        with self.voiceover(
            "<bookmark mark='w'/> Here's our astronaut again, falling from the station. In these coordinates, their "
            "worldline crosses the horizon smoothly, at a finite time. <bookmark mark='k'/> Follow their light cone "
            "along the way. Outside, part of the future still points outward. At the horizon, the outward edge of the "
            "cone points straight up. Inside, the entire future points toward r equals zero. "
            "<bookmark mark='m'/> The horizon is a one-way membrane: things can cross it inward, and nothing can cross "
            "it outward."
        ) as vo:
            vo.wait_until("w")
            self.play(Create(wl), run_time=2)
            vo.wait_until("k")
            self.add(Kc)
            self.play(k.animate.set_value(1.0), run_time=6, rate_func=linear)
            vo.wait_until("m")
            self.play(FadeIn(mem, lag_ratio=0.3))
        Kc.clear_updaters()
        self.clear_scene()
