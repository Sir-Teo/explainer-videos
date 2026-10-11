from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity2 import spacetime as st
from videos.relativity2.common import (clamp_x, under, boxed, label, ladder, load, mtex, note, part_card, polyline, redraw, sci)

INFALLER = C.MATTER


class Infall(VoiceoverScene):
    def construct(self):
        d = load("infall")
        assert abs(float(d["r0"]) - 10) < 1e-12
        assert abs(float(d["tau_h"]) - 33.70) < 0.01 and abs(float(d["tau_s"]) - 35.12) < 0.01
        self.d = d
        self.card()
        self.derive()
        self.clocks()
        self.signals()
        self.inside()

    def card(self):
        c = part_card("I", r"Horizons and singularities", r"what happens when you fall in")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def derive(self):
        title = label(r"Falling straight in, from rest at $r_0$", font_size=36).to_corner(UL, buff=0.4)
        rows = [
            mtex(r"E", r"=", r"\Big(1 - \frac{2M}{r}\Big)\frac{dt}{d\tau}", font_size=40),
            mtex(r"-1", r"=", r"-\Big(1 - \frac{2M}{r}\Big)\dot t^2 + \frac{\dot r^2}{1 - 2M/r}", font_size=40),
            mtex(r"\dot r^2", r"=", r"E^2 - \Big(1 - \frac{2M}{r}\Big)", font_size=40),
            mtex(r"\dot r^2", r"=", r"\frac{2M}{r} - \frac{2M}{r_0}", font_size=44),
            mtex(r"r", r"=", r"\frac{r_0}{2}(1 + \cos\eta),\qquad \tau = \sqrt{\frac{r_0^3}{8M}}\,(\eta + \sin\eta)",
                 font_size=40),
        ]
        whys = [
            note(r"conserved, because the metric doesn't depend on $t$ (part 1, Mercury)"),
            note(r"the four-velocity has length $-1$: $g_{\mu\nu}\dot x^\mu \dot x^\nu = -1$, \ $\dot{} = d/d\tau$"),
            note(r"substitute $\dot t = E/(1 - 2M/r)$"),
            note(r"at rest at $r_0$: \ $E^2 = 1 - 2M/r_0$. \ Newton's energy equation, exactly"),
            note(r"a cycloid: it reaches $r = 2M$, and $r = 0$, at finite $\tau$"),
        ]
        rows[0][0].set_color(INFALLER)
        rows[3][0].set_color(INFALLER)
        rows[4][2][-25:].set_color(C.PROPER_TIME)
        x0 = -0.8
        under(rows, whys, x0)
        step = ladder(self, rows, whys, keep=4, top=2.5, x=x0, buff=0.6)
        with self.voiceover(
            "Picture an astronaut stepping off a space station that hovers at r equals ten M, and falling straight in. "
            "We already have the tools. <bookmark mark='a'/> Because the metric doesn't change with time, the quantity E "
            "is conserved along the fall: it's the energy per unit mass, as measured from far away. "
            "<bookmark mark='b'/> And the four-velocity always has length minus one. <bookmark mark='c'/> Substituting "
            "the first equation into the second gives the radial speed. <bookmark mark='d'/> Starting from rest, it's "
            "exactly Newton's energy equation, with proper time playing the role of time."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        with self.voiceover(
            "<bookmark mark='e'/> Its solution is a cycloid, written with a parameter eta. Nothing special happens at r "
            "equals two M. The astronaut's watch reads a finite time when they cross it, and a finite time when they "
            "reach r equals zero."
        ) as vo:
            vo.wait_until("e")
            step(4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def clocks(self):
        d = self.d
        r, tau = d["r"], d["tau"]
        t_tau, t = d["t_tau"], d["t"]
        tau_h, tau_s = float(d["tau_h"]), float(d["tau_s"])
        ax1 = Axes(x_range=[0, 40, 10], y_range=[0, 10, 2], x_length=5.6, y_length=2.6, tips=False,
                   axis_config={"stroke_color": GREY_B, "font_size": 20},
                   x_axis_config={"numbers_to_include": [10, 20, 30, 40]},
                   y_axis_config={"numbers_to_include": [2, 4, 6, 8, 10]}).move_to([3.4, 1.55, 0])
        ax2 = Axes(x_range=[0, 80, 20], y_range=[0, 10, 2], x_length=5.6, y_length=2.6, tips=False,
                   axis_config={"stroke_color": GREY_B, "font_size": 20},
                   x_axis_config={"numbers_to_include": [20, 40, 60, 80]},
                   y_axis_config={"numbers_to_include": [2, 4, 6, 8, 10]}).move_to([3.4, -2.05, 0])
        l1 = label(r"$r$ vs the astronaut's own time $\tau$", font_size=24, color=C.PROPER_TIME).next_to(ax1, UP, buff=0.12)
        l2 = label(r"$r$ vs the station's time $t$", font_size=24, color=GREY_A).next_to(ax2, UP, buff=0.12)
        u1 = label(r"$\tau / M$", font_size=20).next_to(ax1.x_axis, RIGHT, buff=0.1)
        u2 = label(r"$t / M$", font_size=20).next_to(ax2.x_axis, RIGHT, buff=0.1)
        hz1 = DashedLine(ax1.c2p(0, 2), ax1.c2p(40, 2), color=C.CURVATURE, stroke_width=2)
        hz2 = DashedLine(ax2.c2p(0, 2), ax2.c2p(80, 2), color=C.CURVATURE, stroke_width=2)
        c1 = polyline(ax1, tau, r, color=C.PROPER_TIME, stroke_width=3.5)
        ok = t < 80
        c2 = polyline(ax2, t[ok], r[: len(t)][ok], color=GREY_A, stroke_width=3.5)
        k = ValueTracker(0.0)

        def tau_now():
            return k.get_value() * tau_s

        def dot1():
            tt = tau_now()
            return Dot(ax1.c2p(tt, float(np.interp(tt, tau, r))), radius=0.07, color=INFALLER)

        def dot2():
            tt = tau_now()
            if tt >= t_tau[-1]:
                return VGroup()
            tc = float(np.interp(tt, t_tau, t))
            if tc > 80:
                return VGroup()
            return Dot(ax2.c2p(tc, float(np.interp(tt, tau, r))), radius=0.07, color=INFALLER)

        # left: the scene in space (a radial line, not to scale in angle)
        cen = np.array([-3.6, -0.3, 0])
        sc = 0.3
        hole = Circle(radius=2 * sc, color=C.CURVATURE, stroke_width=3, fill_color=BLACK, fill_opacity=1).move_to(cen)
        hl = label(r"$r = 2M$", font_size=22, color=C.CURVATURE).next_to(hole, DOWN, buff=0.08)
        station = Square(side_length=0.28, color=C.PROPER_TIME, fill_opacity=0.6).move_to(cen + RIGHT * 10 * sc)
        stl = label(r"station, $r = 10M$", font_size=22, color=C.PROPER_TIME).next_to(station, DOWN, buff=0.12)

        def astronaut():
            rr = float(np.interp(tau_now(), tau, r))
            return Dot(cen + RIGHT * rr * sc, radius=0.09, color=INFALLER)

        A1, A2, A3 = redraw(dot1), redraw(dot2), redraw(astronaut)
        rd_tau = VGroup(label(r"astronaut's watch:", font_size=26), DecimalNumber(0, num_decimal_places=1, font_size=30,
                        color=C.PROPER_TIME), label(r"$M$", font_size=26)).arrange(RIGHT, buff=0.12)
        rd_tau.move_to([-3.6, 2.6, 0])
        rd_tau[1].add_updater(lambda m: m.set_value(tau_now()))

        def tc_val():
            tt = tau_now()
            return float(np.interp(tt, t_tau, t)) if tt < t_tau[-1] else 1e9

        def station_clock():
            tc = tc_val()
            txt = rf"station clock: \ ${tc:.1f}\,M$" if tc < 999 else r"station clock: \ $\infty$"
            return label(txt, font_size=26).move_to([-3.6, 2.0, 0])

        rd_t = redraw(station_clock)
        inf = mtex(r"t \to \infty", font_size=36, color=GREY_A).move_to(ax2.c2p(70, 4.0))
        nums = VGroup(
            mtex(r"\tau(2M) = 33.7M,\qquad \tau(0) = 35.1M", font_size=30, color=C.PROPER_TIME),
            label(r"for 10 $M_\odot$ ($M = 49\ \mu$s): 1.66 ms to the horizon,", font_size=22, color=GREY_A),
            label(r"then 70 $\mu$s more", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.1).move_to([-3.6, -2.75, 0])
        clamp_x(nums)
        with self.voiceover(
            "Let's watch it, with two clocks. <bookmark mark='a'/> On top, the astronaut's distance from the center "
            "against their own watch: a smooth fall, through r equals two M, and on to zero, in about thirty-five M. "
            "<bookmark mark='b'/> Below, the same fall against the station's clock, which runs at the rate of "
            "coordinate time t. <bookmark mark='g'/> Here the astronaut slows down as they approach two M, and never "
            "quite gets there: t grows without bound. <bookmark mark='n'/> For a black hole of ten solar masses, M is "
            "forty-nine microseconds, so the whole trip takes under two milliseconds of the astronaut's time."
        ) as vo:
            self.play(FadeIn(hole), FadeIn(hl), FadeIn(station), FadeIn(stl), FadeIn(rd_tau), FadeIn(rd_t))
            self.add(A3)
            vo.wait_until("a")
            self.play(Create(ax1), FadeIn(l1), FadeIn(u1), Create(hz1))
            self.play(Create(c1), run_time=1.5)
            self.add(A1)
            vo.wait_until("b")
            self.play(Create(ax2), FadeIn(l2), FadeIn(u2), Create(hz2))
            self.play(Create(c2), run_time=1.5)
            self.add(A2)
            vo.wait_until("g")
            self.play(k.animate.set_value(tau_h / tau_s * 0.995), run_time=4.5, rate_func=linear)
            self.play(FadeIn(inf), k.animate.set_value(1.0), run_time=1.5, rate_func=linear)
            vo.wait_until("n")
            self.play(FadeIn(nums, lag_ratio=0.3))
        for m in (A1, A2, A3, rd_tau[1], rd_t):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def signals(self):
        d = self.d
        r, t = d["r"][: len(d["t"])], d["t"]
        er, et, rt = d["emit_r"], d["emit_t"], d["recv_t"]
        ax = Axes(x_range=[0, 11, 2], y_range=[0, 90, 20], x_length=5.6, y_length=6.2, tips=False,
                  axis_config={"stroke_color": GREY_B, "font_size": 20},
                  x_axis_config={"numbers_to_include": [2, 4, 6, 8, 10]},
                  y_axis_config={"numbers_to_include": [20, 40, 60, 80]}).move_to([-3.3, -0.25, 0])
        xl = label(r"$r/M$", font_size=22).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = label(r"station time $t/M$", font_size=22).next_to(ax.y_axis, UP, buff=0.1)
        hz = DashedLine(ax.c2p(2, 0), ax.c2p(2, 90), color=C.CURVATURE, stroke_width=2.5)
        stw = Line(ax.c2p(10, 0), ax.c2p(10, 90), color=C.PROPER_TIME, stroke_width=4)
        ok = t < 90
        wl = polyline(ax, r[ok], t[ok], color=INFALLER, stroke_width=4)
        rays = VGroup()
        ticks = VGroup()
        for re_, te_, tr_ in zip(er, et, rt):
            if tr_ > 90:
                continue
            rr = np.linspace(re_, 10, 60)
            tt = te_ + st.tortoise(rr) - st.tortoise(re_)
            rays.add(polyline(ax, rr, tt, color=C.LIGHT, stroke_width=2))
            ticks.add(Line(ax.c2p(9.7, tr_), ax.c2p(10.3, tr_), color=C.LIGHT, stroke_width=3))
        n_vis = len(rays)
        assert n_vis >= 12
        lab = clamp_x(note(r"flashes every $0.4M$ of the astronaut's time; outgoing light rays computed exactly").next_to(ax, DOWN, buff=0.2))
        # redshift
        zt, oz = d["z_t"], d["one_z"]
        ax2 = Axes(x_range=[0, 160, 40], y_range=[0, 30, 10], x_length=5.4, y_length=3.6, tips=False,
                   axis_config={"stroke_color": GREY_B, "font_size": 20},
                   x_axis_config={"numbers_to_include": [40, 80, 120, 160]},
                   y_axis_config={"numbers_to_include": [10, 20, 30]}).move_to([3.6, 0.3, 0])
        sel = zt < 160
        zc = polyline(ax2, zt[sel], np.log(oz[sel]), color=C.LIGHT, stroke_width=3.5)
        zl = label(r"$\ln(1+z)$ of the light received", font_size=22, color=C.LIGHT).next_to(ax2, UP, buff=0.12)
        xl2 = label(r"$t/M$", font_size=20).next_to(ax2.x_axis, RIGHT, buff=0.1)
        slope = float(d["slope"])
        assert abs(slope - 0.25) < 0.002
        law = mtex(r"1 + z", r"\;\propto\;", r"e^{\,t/4M}", font_size=40, color=C.LIGHT).next_to(ax2, DOWN, buff=0.35)
        ex = label(r"10 $M_\odot$: \ $4M = 0.2$ ms. \ The image freezes, reddens, and fades.", font_size=24,
                   color=GREY_A).next_to(law, DOWN, buff=0.2)
        with self.voiceover(
            "So what does the station actually see? <bookmark mark='a'/> Draw it on a spacetime diagram: distance "
            "across, the station's time up. The astronaut's worldline bends over and runs up along r equals two M. "
            "<bookmark mark='b'/> Now suppose they send a flash of light back to the station every so often, by their "
            "own watch. <bookmark mark='c'/> The flashes arrive further and further apart. A flash sent exactly at r "
            "equals two M never arrives at all: that outgoing light ray stays at r equals two M forever."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(hz), Create(stw))
            self.play(Create(wl), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(x) for x in rays[:6]], lag_ratio=0.3), FadeIn(ticks[:6]), FadeIn(lab),
                      run_time=2)
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(x) for x in rays[6:]], lag_ratio=0.3), FadeIn(ticks[6:]), run_time=3)
        with self.voiceover(
            "<bookmark mark='z'/> The light also arrives stretched. Its redshift grows, and at late times it grows "
            "exponentially: the wavelength increases by a factor of e every four M of the station's time. "
            "<bookmark mark='e'/> For a ten-solar-mass black hole, that's a fifth of a millisecond. To the station, "
            "the astronaut seems to freeze at the horizon, turn red, and fade from view almost instantly, while the "
            "astronaut, by their own watch, simply falls through."
        ) as vo:
            vo.wait_until("z")
            self.play(Create(ax2), FadeIn(zl), FadeIn(xl2))
            self.play(Create(zc), run_time=2)
            self.play(Write(law))
            vo.wait_until("e")
            self.play(FadeIn(ex))
        self.clear_scene()

    # ------------------------------------------------------------------
    def inside(self):
        c = load("consts")
        t10, tsg, tm87 = float(c["taumax_10"]), float(c["taumax_sgra"]), float(c["taumax_m87"])
        g10, gsg, gm87 = float(c["tide_10"]) / 9.81, float(c["tide_sgra"]) / 9.81, float(c["tide_m87"]) / 9.81
        assert abs(t10 * 1e6 - 155) < 0.5 and abs(tsg - 66.5) < 0.1 and abs(tm87 / 3600 - 27.9) < 0.05
        assert abs(g10 / 2.1e7 - 1) < 0.03 and abs(gsg / 1.1e-4 - 1) < 0.05 and abs(gm87 / 5.0e-11 - 1) < 0.03
        top = VGroup(
            mtex(r"\tau_{\max}(2M \to 0)", r"=", r"\pi M", font_size=44),
            label(r"the longest you can last inside, however you fire your rockets (falling from rest at the horizon)",
                  font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.45)
        top[0][2].set_color(C.PROPER_TIME)
        tide = VGroup(
            mtex(r"\Delta a", r"=", r"\frac{2M}{r^3}\,L", font_size=40),
            label(r"the tidal stretch across a body of length $L$ (part 1: geodesic deviation)", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.12).next_to(top, DOWN, buff=0.4)
        tide[0][2].set_color(C.CURVATURE)
        hdr = VGroup(label(r"", font_size=26), label(r"$\pi M$", font_size=26, color=C.PROPER_TIME),
                     label(r"tidal stretch across 2 m at $r = 2M$", font_size=26, color=C.CURVATURE))
        rows = [
            (r"10 $M_\odot$", r"155 $\mu$s", r"$2\times10^{7}\ g$: torn apart"),
            (r"Sagittarius A$^*$, $4.3\times10^6 M_\odot$", r"67 s", r"$10^{-4}\ g$"),
            (r"M87$^*$, $6.5\times10^9 M_\odot$", r"28 hours", r"$5\times10^{-11}\ g$: unnoticeable"),
        ]
        table = VGroup(hdr)
        for a_, b_, c_ in rows:
            table.add(VGroup(label(a_, font_size=26), label(b_, font_size=26, color=C.PROPER_TIME),
                             label(c_, font_size=26, color=C.CURVATURE)))
        cols = [-4.2, 0.4, 3.9]
        for i, row in enumerate(table):
            for j, m in enumerate(row):
                m.move_to([cols[j], -0.45 - 0.62 * i, 0])
        line = Line([-6.6, -0.75, 0], [6.6, -0.75, 0], color=GREY_C, stroke_width=1.5)
        concl = label(r"Locally, the horizon is an ordinary place. \ What's wrong is the coordinates.", font_size=30
                      ).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Two more facts about the inside. <bookmark mark='a'/> Once you've crossed, the longest you can possibly "
            "survive, by your own watch, is pi M, and firing rockets only shortens it. <bookmark mark='b'/> And what "
            "you feel is tides: the difference in acceleration across your body, two M over r cubed times your height. "
            "<bookmark mark='c'/> For a stellar black hole, at the horizon that's twenty million g's, and you'd be "
            "torn apart well before you reached it. <bookmark mark='d'/> But tides shrink with the square of the mass. "
            "At the horizon of the black hole in the center of our galaxy, they're a ten-thousandth of a g, and at the "
            "giant one in M87, utterly unnoticeable, and you'd have more than a day before the end. "
            "<bookmark mark='e'/> So locally, the horizon is an ordinary place. What breaks there is our coordinates."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(top[0]), FadeIn(top[1]))
            vo.wait_until("b")
            self.play(FadeIn(tide, lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(hdr), Create(line), FadeIn(table[1]))
            vo.wait_until("d")
            self.play(FadeIn(table[2]))
            self.play(FadeIn(table[3]))
            vo.wait_until("e")
            self.play(FadeIn(concl))
        self.clear_scene()
