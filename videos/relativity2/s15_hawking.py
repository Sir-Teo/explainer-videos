from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity2 import spacetime as st
from videos.relativity2.common import (Chart, View3D, clamp_x, curve3d, label, ladder, load, mtex, note, polyline,
                                       redraw, sci, under, zigzag)
from videos.relativity2.geometry import check_near_horizon

HOR, TEMP, ENT = C.CURVATURE, C.TEMPERATURE, C.ENTROPY


class Hawking(VoiceoverScene):
    def construct(self):
        assert check_near_horizon() == "ok"
        self.h = load("hawking")
        self.peeling()
        self.spectrum()
        self.euclid()
        self.cigar()
        self.numbers()

    # ------------------------------------------------------------------
    def peeling(self):
        h = self.h
        ks, arr = h["peel_k"], h["peel_t"]
        gaps = np.diff(arr)
        assert np.allclose(gaps[-3:], 4 * math.log(10), rtol=1e-3)
        ax = Axes(x_range=[0, 10.5, 2], y_range=[0, 95, 20], x_length=5.6, y_length=6.3, tips=False,
                  axis_config={"stroke_color": GREY_B, "font_size": 20},
                  x_axis_config={"numbers_to_include": [2, 4, 6, 8, 10]},
                  y_axis_config={"numbers_to_include": [20, 40, 60, 80]}).move_to([-3.4, -0.35, 0])
        xl = label(r"$r/M$", font_size=22).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = label(r"$\tilde t/M$", font_size=24, color=C.PROPER_TIME).next_to(ax.y_axis, UP, buff=0.1)
        hz = Line(ax.c2p(2, 0), ax.c2p(2, 95), color=HOR, stroke_width=4)
        hzl = label(r"horizon", font_size=22, color=HOR).next_to(ax.c2p(2, 95), RIGHT, buff=0.1)
        rays = VGroup()
        for k_ in ks:
            r0 = 2 * (1 + 10.0 ** -k_)
            r = np.linspace(r0, 10, 400)
            tt = (r - r0) + 4 * np.log((r - 2) / (r0 - 2))
            ok = tt <= 95
            rays.add(polyline(ax, r[ok], tt[ok], color=C.LIGHT, stroke_width=2.5))
        labs = VGroup(*[label(rf"$\epsilon = 10^{{-{k_}}}$", font_size=18, color=C.LIGHT).next_to(ax.c2p(10, arr[i]), RIGHT, buff=0.08)
                        for i, k_ in enumerate(ks) if arr[i] < 95])
        axis, cap = ax, note(r"computed outgoing null rays (Eddington--Finkelstein), launched at $\tilde t = 0$").to_corner(DL, buff=0.2)
        eq = VGroup(
            label(r"rays leaving from $r = 2M(1 + \epsilon)$:", font_size=26),
            mtex(r"\Delta\tilde t = 4M\ln\frac{1}{\epsilon} + \dots", font_size=36, color=C.LIGHT),
            label(r"each factor of 10 closer: $4M\ln 10$ later", font_size=24, color=GREY_A),
            label(r"so the light that escapes late was squeezed", font_size=26),
            label(r"into an exponentially thin layer:", font_size=26),
            mtex(r"v_0 - v \;\propto\; e^{-\kappa u},\qquad \kappa = \frac{1}{4M}", font_size=38, color=TEMP),
        ).arrange(DOWN, buff=0.18).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "In 1974, Hawking applied quantum field theory to a collapsing star, expecting to confirm that black holes "
            "are perfectly black. He found the opposite. Here's the heart of it. <bookmark mark='a'/> Look at light "
            "rays leaving from just outside the horizon. A ray starting a tenth of the horizon radius out escapes "
            "quickly. One starting a hundred times closer takes four M times the log of ten longer, and so on: every "
            "factor of ten closer delays the escape by the same amount. <bookmark mark='b'/> Turn that around. The "
            "light reaching a distant observer late, at time u, left from an exponentially thin layer near the horizon. "
            "Rays arriving later and later trace back to a region squeezed by a factor of e every four M: the past "
            "position of a ray depends exponentially on when it arrives, with rate kappa, the surface gravity."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(axis), FadeIn(xl), Create(hz), FadeIn(hzl), FadeIn(yl), FadeIn(cap))
            self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.35), FadeIn(labs, lag_ratio=0.3),
                      FadeIn(eq[:3]), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(eq[3:], lag_ratio=0.3))
        self.clear_scene()

    # ------------------------------------------------------------------
    def spectrum(self):
        h = self.h
        u, w = h["wave_u"], h["wave"]
        om, Fp, Fm, ratio, boltz = h["omegas"], h["Fp2"], h["Fm2"], h["ratio"], h["boltz"]
        assert np.max(np.abs(np.log(ratio / boltz))) < 0.03
        ax = Axes(x_range=[-3, 6, 1], y_range=[-1.2, 1.2, 1], x_length=6.0, y_length=2.0, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to([-3.3, 1.9, 0])
        wv = polyline(ax, u, w, color=C.LIGHT, stroke_width=2)
        t1 = label(r"$\cos\big(b\,e^{-\kappa u}\big)$: a wave stretched exponentially", font_size=22, color=C.LIGHT).next_to(ax, UP, buff=0.08)
        xl = label(r"$u$", font_size=22).next_to(ax.x_axis, RIGHT, buff=0.08)
        ax2 = Axes(x_range=[0, 2.6, 0.5], y_range=[-7.5, 0.5, 1], x_length=5.8, y_length=3.6, tips=False,
                   axis_config={"stroke_color": GREY_B, "font_size": 20},
                   x_axis_config={"numbers_to_include": [0.5, 1, 1.5, 2, 2.5]},
                   y_axis_config={"numbers_to_include": [-6, -4, -2, 0]}).move_to([-3.3, -1.75, 0])
        dots = VGroup(*[Dot(ax2.c2p(o, math.log10(r)), radius=0.06, color=TEMP) for o, r in zip(om, ratio)])
        line = polyline(ax2, np.linspace(0, 2.55, 50), np.log10(np.exp(-2 * np.pi * np.linspace(0, 2.55, 50))),
                        color=WHITE, stroke_width=2.5)
        t2 = label(r"$\log_{10}\big(|F(-\omega)|^2/|F(\omega)|^2\big)$ vs $\omega/\kappa$", font_size=22).next_to(ax2, UP, buff=0.08)
        ll = label(r"line: $e^{-2\pi\omega/\kappa}$", font_size=22).next_to(ax2.c2p(1.2, -3.2), RIGHT, buff=0.1)
        cap = note(r"dots: the Fourier transform computed numerically").next_to(ax2, DOWN, buff=0.12)
        rows = VGroup(
            label(r"positive frequency in the past", font_size=26),
            label(r"$\rightarrow$ a mixture of positive \emph{and negative}", font_size=26),
            label(r"frequencies for the distant observer:", font_size=26),
            label(r"the vacuum becomes a flow of particles", font_size=26, color=TEMP),
            mtex(r"\frac{|\beta_\omega|^2}{|\alpha_\omega|^2} = e^{-2\pi\omega/\kappa}", font_size=40, color=TEMP),
            mtex(r"\langle n_\omega\rangle = \frac{1}{e^{2\pi\omega/\kappa} - 1}", font_size=40, color=TEMP),
            label(r"a Planck spectrum, at temperature", font_size=26),
            mtex(r"T_H = \frac{\kappa}{2\pi} = \frac{1}{8\pi M}", font_size=44, color=TEMP),
        ).arrange(DOWN, buff=0.16).move_to([3.5, 0.0, 0])
        with self.voiceover(
            "Why does that matter? In quantum field theory, what counts as a particle depends on what counts as a "
            "positive-frequency wave, and that depends on whose clock you use. <bookmark mark='a'/> A wave that "
            "oscillates smoothly in the past reaches the distant observer stretched exponentially: rapid at first, then "
            "frozen. <bookmark mark='b'/> Take its Fourier transform with respect to the observer's time. It isn't "
            "purely positive frequency any more: it contains negative frequencies too, which means particles have been "
            "created from the vacuum. <bookmark mark='c'/> And the ratio of negative to positive is exactly e to the "
            "minus two pi omega over kappa. We computed the transform numerically: the dots fall right on the line. "
            "<bookmark mark='d'/> That's a Boltzmann factor. The particles come out with a thermal, Planck spectrum, at "
            "temperature kappa over two pi: one over eight pi M."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(t1), FadeIn(xl))
            self.play(Create(wv), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(rows[:4], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(Create(ax2), FadeIn(t2), FadeIn(cap))
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.1), Create(line), FadeIn(ll), FadeIn(rows[4]),
                      run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[5:], lag_ratio=0.3))
        self.clear_scene()

    # ------------------------------------------------------------------
    def euclid(self):
        rows = [
            mtex(r"r", r"=", r"2M + \frac{\rho^2}{8M}", font_size=40),
            mtex(r"ds^2", r"\approx", r"-\Big(\frac{\rho}{4M}\Big)^2dt^2 + d\rho^2 + (2M)^2d\Omega^2", font_size=40),
            mtex(r"ds_E^2", r"=", r"\Big(\frac{\rho}{4M}\Big)^2d\tau^2 + d\rho^2", font_size=42),
            mtex(r"\tau", r"\sim", r"\tau + 8\pi M", font_size=44),
            mtex(r"T_H", r"=", r"\frac{1}{8\pi M} = \frac{\hbar c^3}{8\pi G M k_B}", font_size=46),
        ]
        whys = [
            note(r"$\rho$: proper distance from the horizon"),
            note(r"near the horizon: flat spacetime as seen by accelerated observers (Rindler), checked symbolically"),
            note(r"rotate time to imaginary values, $t = -i\tau$: polar coordinates, with angle $\tau/4M$"),
            note(r"no cone at $\rho = 0$ only if the angle runs over $2\pi$: $\tau$ is periodic"),
            note(r"a quantum field periodic in imaginary time with period $\hbar/k_BT$ is at temperature $T$"),
        ]
        rows[4][0].set_color(TEMP)
        rows[4][2].set_color(TEMP)
        under(rows, whys, -0.8)
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.8, buff=0.62)
        hist = note(r"Gibbons \& Hawking (1977)").to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "There's a second, astonishingly short route to the same temperature. <bookmark mark='a'/> Measure "
            "distance from the horizon with rho. <bookmark mark='b'/> Near the horizon, the metric becomes flat "
            "spacetime as described by accelerated observers. <bookmark mark='c'/> Now do something strange: make time "
            "imaginary. The metric becomes rho squared times d tau over four M squared, plus d rho squared, which is "
            "the flat plane in polar coordinates, with tau over four M as the angle."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        with self.voiceover(
            "<bookmark mark='d'/> For the plane to be smooth at the origin, the angle has to go around exactly two pi, "
            "so imaginary time must repeat with period eight pi M. Otherwise the origin is the tip of a cone. "
            "<bookmark mark='e'/> And in quantum statistical mechanics, a system whose fields are periodic in imaginary "
            "time, with period h-bar over k T, is at temperature T. So a black hole has temperature one over eight pi "
            "M, the same answer, as Gibbons and Hawking showed in 1977. With the constants put back, that's this "
            "formula, which is carved on Hawking's memorial stone in Westminster Abbey."
        ) as vo:
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            self.play(FadeIn(hist))
        self.clear_scene()

    # ------------------------------------------------------------------
    def cigar(self):
        h = self.h
        R_s, z_s = h["cigar_smooth_R"], h["cigar_smooth_z"]
        R_c, z_c = h["cigar_cone_R"], h["cigar_cone_z"]
        vl = View3D(center=[-3.4, -1.9, 0], scale=0.36, azimuth=0.4, elevation=0.25)
        vr = View3D(center=[3.4, -1.9, 0], scale=0.36, azimuth=0.4, elevation=0.25)

        def surf(view, R, z, color):
            g = VGroup()
            m = z < 10.5
            R, z = R[m], z[m]
            a = np.linspace(0, 2 * np.pi, 90)
            for k in np.linspace(0, len(R) - 1, 12).round().astype(int)[1:]:
                P = np.stack([R[k] * np.cos(a), R[k] * np.sin(a), np.full_like(a, z[k])], 1)
                g.add(curve3d(view, P, color=color, stroke_width=1.6, sphere_r=None, back_opacity=1.0))
            for ang in np.linspace(0, 2 * np.pi, 20, endpoint=False):
                P = np.stack([R * math.cos(ang), R * math.sin(ang), z], 1)
                g.add(curve3d(view, P, color=color, stroke_width=1.3, sphere_r=None, back_opacity=1.0))
            return g

        S1 = surf(vl, R_s, z_s, TEMP)
        S2 = surf(vr, R_c, z_c, GREY_B)
        l1 = VGroup(label(r"period $8\pi M$: a smooth tip", font_size=28, color=TEMP),
                    label(r"($T = 1/8\pi M$)", font_size=24, color=TEMP)).arrange(DOWN, buff=0.08).move_to([-3.4, 2.9, 0])
        l2 = VGroup(label(r"any other period: a cone", font_size=28, color=GREY_B),
                    label(r"(here $0.55\times 8\pi M$)", font_size=24, color=GREY_B)).arrange(DOWN, buff=0.08).move_to([3.4, 2.9, 0])
        cap = note(r"the $(r, \tau)$ plane of the Euclidean black hole, embedded exactly as a surface of revolution; the tip is the horizon").to_edge(DOWN, buff=0.2)
        clamp_x(cap)
        with self.voiceover(
            "<bookmark mark='a'/> Here's that geometry, the plane of r and imaginary time, embedded exactly as a surface. "
            "Far away, it's a cylinder: imaginary time going around. At the horizon, it closes off. "
            "<bookmark mark='b'/> With the right period, the tip is smooth, like the end of a cigar. "
            "<bookmark mark='c'/> With any other period, it ends in a sharp cone. The geometry itself picks out the "
            "temperature."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cap))
            vo.wait_until("b")
            self.play(Create(S1, lag_ratio=0.02), FadeIn(l1), run_time=2)
            vo.wait_until("c")
            self.play(Create(S2, lag_ratio=0.02), FadeIn(l2), run_time=2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def numbers(self):
        c = load("consts")
        TH, S, life, mc = float(c["T_hawking"]), float(c["S_sun"]), float(c["life_sun"]), float(c["m_cmb"])
        assert abs(TH * 1e8 - 6.17) < 0.01 and abs(S / 1e77 - 1.05) < 0.005 and abs(mc / 1e22 - 4.5) < 0.01
        h = self.h
        Ms, Ts = h["TM_M"], h["TM_T"]
        ax = Axes(x_range=[11, 41, 5], y_range=[-17, 13, 5], x_length=6.0, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_B, "font_size": 20},
                  x_axis_config={"numbers_to_include": [15, 20, 25, 30, 35, 40]},
                  y_axis_config={"numbers_to_include": [-15, -10, -5, 0, 5, 10]}).move_to([-3.4, -0.6, 0])
        xl = label(r"$\log_{10}$ mass (kg)", font_size=22).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = label(r"$\log_{10}$ Hawking temperature (K)", font_size=22, color=TEMP).next_to(ax, UP, buff=0.1)
        cur = polyline(ax, np.log10(Ms), np.log10(Ts), color=TEMP, stroke_width=4)
        cmb = DashedLine(ax.c2p(11, math.log10(2.7255)), ax.c2p(41, math.log10(2.7255)), color=C.LIGHT, stroke_width=2)
        cmbl = label(r"CMB, 2.7 K", font_size=20, color=C.LIGHT).next_to(ax.c2p(41, math.log10(2.7255)), UP + LEFT, buff=0.05)
        pts = VGroup()
        for name, m in ((r"Sun", 1.989e30), (r"Sgr A*", 4.3e6 * 1.989e30), (r"Moon", 7.342e22)):
            T = TH * 1.989e30 / m
            p = ax.c2p(math.log10(m), math.log10(T))
            pts.add(Dot(p, radius=0.07, color=WHITE), label(name, font_size=20).next_to(p, UR, buff=0.05))
        facts = VGroup(
            mtex(rf"T_H = {TH * 1e8:.2f}\times10^{{-8}}\ \text{{K}}\ \Big(\frac{{M_\odot}}{{M}}\Big)", font_size=34, color=TEMP),
            label(r"far colder than the CMB: real black holes grow", font_size=24, color=GREY_A),
            label(r"break-even at $4.5\times10^{22}$ kg, 60\% of the Moon's mass", font_size=24, color=GREY_A),
            mtex(r"S_{BH} = \frac{k_B c^3 A}{4G\hbar}", font_size=36, color=ENT),
            label(rf"one solar mass: $S = {S / 1e77:.2f}\times10^{{77}}\,k_B$", font_size=24, color=ENT),
            label(r"(the Sun itself: $\sim 10^{58}\,k_B$)", font_size=22, color=GREY_A),
            label(rf"evaporation time $\propto M^3$: \ $\sim 10^{{67}}$ years for $M_\odot$", font_size=24),
        ).arrange(DOWN, buff=0.18).move_to([3.5, -0.2, 0])
        with self.voiceover(
            "Put the numbers in. <bookmark mark='a'/> A black hole of one solar mass has a temperature of sixty "
            "billionths of a kelvin, and heavier ones are colder still: far colder than the cosmic microwave "
            "background, so every black hole we know of absorbs more than it emits. Only one lighter than about sixty "
            "percent of the Moon's mass would be hotter than the sky around it. <bookmark mark='b'/> The temperature "
            "fixes the entropy: one quarter of the horizon area, in Planck units. Bekenstein's guess was right, with "
            "the factor now fixed. For a solar-mass black hole, that's ten to the seventy-seven, about ten billion "
            "billion times the entropy of the Sun itself. <bookmark mark='c'/> And a body that radiates loses mass: "
            "left alone, a black hole evaporates, in a time proportional to its mass cubed, around ten to the "
            "sixty-seven years for a solar mass. <bookmark mark='d'/> Whether the information that fell in comes back "
            "out in the radiation, and how, is still one of the deepest open questions in physics."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(cmb), FadeIn(cmbl))
            self.play(Create(cur), FadeIn(pts), FadeIn(facts[:3], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(facts[3:6], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(facts[6]))
        self.clear_scene()
